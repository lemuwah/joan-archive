"""Regression tests for durable daily sweep publication."""

import json
import tempfile
import unittest
from argparse import Namespace
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import sweep


class SweepPublicationTests(unittest.TestCase):
    def setUp(self):
        self.people = [{
            "name": "John Greene of Quidnessett",
            "page": "test-person.md",
            "text": "# John Greene of Quidnessett\\n",
        }]
        self.atom = SimpleNamespace(
            value="John Greene", field="name", status="TEST_ONLY"
        )

    def args(self, output, run_date="2099-01-01"):
        return Namespace(
            date=run_date, output=str(output), rows=1, delay=0,
            max_queries=1, dry_run=True,
        )

    def run_patched(self, args, query_text=None):
        query_patch = (
            patch.object(sweep, "query_text", side_effect=query_text)
            if query_text is not None else nullcontext()
        )
        with (
            patch.object(sweep, "person_names", return_value=self.people),
            patch.object(sweep, "discovery_name_atoms", return_value=[self.atom]),
            query_patch,
        ):
            return sweep.run(args)

    def test_existing_result_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            result = output / "2099-01-01.jsonl"
            original = "preserve this exact history\\n"
            result.write_text(original, encoding="utf-8")

            with self.assertRaises(FileExistsError):
                self.run_patched(self.args(output))

            self.assertEqual(result.read_text(encoding="utf-8"), original)
            self.assertFalse((output / "2099-01-01.summary.json").exists())

    def test_existing_summary_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            summary = output / "2099-01-01.summary.json"
            original = '{"preserve": true}\\n'
            summary.write_text(original, encoding="utf-8")

            with self.assertRaises(FileExistsError):
                self.run_patched(self.args(output))

            self.assertEqual(summary.read_text(encoding="utf-8"), original)
            self.assertFalse((output / "2099-01-01.jsonl").exists())

    def test_interrupted_run_does_not_publish_final_or_temp_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)

            def interrupt(*_args):
                raise RuntimeError("simulated interruption")

            with self.assertRaisesRegex(RuntimeError, "simulated interruption"):
                self.run_patched(self.args(output), query_text=interrupt)

            self.assertFalse((output / "2099-01-01.jsonl").exists())
            self.assertFalse((output / "2099-01-01.summary.json").exists())
            self.assertEqual(
                list(output.iterdir()), [],
                "ordinary exceptions must clean temporary publication files",
            )

    def test_summary_publication_failure_rolls_back_only_our_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            result = output / "2099-01-01.jsonl"
            summary = output / "2099-01-01.summary.json"
            original_summary = '{"another_run": true}\n'
            original_link = sweep.os.link
            link_calls = 0

            def fail_second_link(source_path, destination_path):
                nonlocal link_calls
                link_calls += 1
                if link_calls == 2:
                    # Simulate another writer winning the summary filename race.
                    summary.write_text(original_summary, encoding="utf-8")
                    raise FileExistsError("simulated summary publication race")
                return original_link(source_path, destination_path)

            with patch.object(sweep.os, "link", side_effect=fail_second_link):
                with self.assertRaisesRegex(
                    FileExistsError, "simulated summary publication race"
                ):
                    self.run_patched(self.args(output))

            self.assertEqual(link_calls, 2)
            self.assertFalse(result.exists(), "our partial result must be rolled back")
            self.assertEqual(
                summary.read_text(encoding="utf-8"),
                original_summary,
                "the competing writer's summary must remain untouched",
            )
            self.assertEqual(
                list(output.iterdir()),
                [summary],
                "staging files must be cleaned up after publication failure",
            )

    def test_successful_dry_run_publishes_matching_outputs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            result, summary = self.run_patched(self.args(output))

            records = [
                json.loads(line)
                for line in result.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            summary_data = json.loads(summary.read_text(encoding="utf-8"))

            self.assertEqual(len(records), 1)
            self.assertEqual(summary_data["queries_run"], len(records))
            self.assertEqual(records[0]["status"], "DRY_RUN")
            self.assertEqual(
                sorted(p.name for p in output.iterdir()),
                ["2099-01-01.jsonl", "2099-01-01.summary.json"],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
