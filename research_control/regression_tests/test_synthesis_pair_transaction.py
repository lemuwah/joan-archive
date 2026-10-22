#!/usr/bin/env python3
"""Regression requirements for safe publication of paired synthesis ledgers.

These tests use isolated temporary files and never touch the real ledgers.
"""

import importlib.util
import os
import tempfile
import threading
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "tools/synthesis_workflow/synthesize_legacy_pages.py"

spec = importlib.util.spec_from_file_location("synthesis_pair_transaction_test", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load synthesis script: {SCRIPT}")

synthesis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synthesis)


def setup_fixture(root: Path):
    people = root / "people"
    people.mkdir()
    (people / "sample.md").write_text("# Synthetic page\n", encoding="utf-8")

    observations = root / "data/research/legacy_observations.jsonl"
    proposals = root / "data/research/synthesis_proposals.jsonl"
    observations.parent.mkdir(parents=True)

    old_observations = b'{"observation_id":"OLD-OBS","value":"preserve"}\n'
    old_proposals = b'{"proposal_id":"OLD-PROP","human_disposition":"KEEP"}\n'
    observations.write_bytes(old_observations)
    proposals.write_bytes(old_proposals)

    return people, observations, proposals, old_observations, old_proposals


def test_second_publication_failure_preserves_recovery_evidence():
    old_paths = (
        synthesis.ROOT,
        synthesis.PEOPLE_DIR,
        synthesis.OBSERVATIONS,
        synthesis.PROPOSALS,
    )

    try:
        with tempfile.TemporaryDirectory(prefix="synthesis-pair-transaction-") as temp:
            root = Path(temp)
            people, observations, proposals, old_obs, old_prop = setup_fixture(root)

            synthesis.ROOT = root
            synthesis.PEOPLE_DIR = people
            synthesis.OBSERVATIONS = observations
            synthesis.PROPOSALS = proposals

            real_replace = os.replace
            def fail_second_replace(source, destination):
                if Path(destination) == proposals:
                    raise OSError("simulated second-ledger publication failure")
                return real_replace(source, destination)

            failure_observed = False
            with patch.object(os, "replace", side_effect=fail_second_replace):
                try:
                    synthesis.build(check=False)
                except OSError as error:
                    if "simulated second-ledger publication failure" not in str(error):
                        raise
                    failure_observed = True

            if not failure_observed:
                raise AssertionError(
                    "The simulated second-ledger publication failure did not occur"
                )

            # A failed pair publication must either leave both originals
            # intact or retain a journal containing both exact originals.
            journal_files = list(
                (root / "data/research").glob("*synthesis*transaction*.json")
            )
            pair_unchanged = (
                observations.read_bytes() == old_obs
                and proposals.read_bytes() == old_prop
            )

            if not pair_unchanged:
                if len(journal_files) != 1:
                    raise AssertionError(
                        "Partial publication requires exactly one recovery journal"
                    )

                import base64
                import json

                journal = json.loads(
                    journal_files[0].read_text(encoding="utf-8")
                )
                originals = journal.get("originals")
                if not isinstance(originals, dict):
                    raise AssertionError("Journal has no originals mapping")

                required = {
                    "legacy_observations.jsonl": old_obs,
                    "synthesis_proposals.jsonl": old_prop,
                }
                for filename, expected_bytes in required.items():
                    encoded = originals.get(filename)
                    if not isinstance(encoded, str):
                        raise AssertionError(
                            f"Journal is missing original bytes for {filename}"
                        )
                    try:
                        actual_bytes = base64.b64decode(
                            encoded, validate=True
                        )
                    except Exception as error:
                        raise AssertionError(
                            f"Invalid original-byte encoding for {filename}"
                        ) from error
                    if actual_bytes != expected_bytes:
                        raise AssertionError(
                            f"Journal does not preserve exact original bytes for {filename}"
                        )

    finally:
        (
            synthesis.ROOT,
            synthesis.PEOPLE_DIR,
            synthesis.OBSERVATIONS,
            synthesis.PROPOSALS,
        ) = old_paths



def test_recovery_restores_both_original_ledgers_after_partial_publish():
    old_paths = (
        synthesis.ROOT,
        synthesis.PEOPLE_DIR,
        synthesis.OBSERVATIONS,
        synthesis.PROPOSALS,
    )
    try:
        with tempfile.TemporaryDirectory(prefix="synthesis-pair-recovery-") as temp:
            root = Path(temp)
            people, observations, proposals, old_obs, old_prop = setup_fixture(root)
            synthesis.ROOT = root
            synthesis.PEOPLE_DIR = people
            synthesis.OBSERVATIONS = observations
            synthesis.PROPOSALS = proposals

            intended_obs = b'{"observation_id":"NEW-OBS"}\\n'
            intended_prop = b'{"proposal_id":"NEW-PROP"}\\n'
            real_replace = os.replace

            def fail_proposals(source, destination):
                if Path(destination) == proposals:
                    raise OSError("simulated proposals publication failure")
                return real_replace(source, destination)

            with patch.object(os, "replace", side_effect=fail_proposals):
                try:
                    synthesis._publish_ledger_pair(intended_obs, intended_prop)
                except OSError as error:
                    if "proposals publication failure" not in str(error):
                        raise
                else:
                    raise AssertionError("Expected simulated publication failure")

            journal = synthesis.transaction_journal_path()
            if not journal.exists():
                raise AssertionError("Partial publication did not retain its journal")
            if observations.read_bytes() != intended_obs:
                raise AssertionError("Test did not create the intended partial state")
            if proposals.read_bytes() != old_prop:
                raise AssertionError("Failed proposals write unexpectedly changed the ledger")

            synthesis._recover_transaction()

            if observations.read_bytes() != old_obs:
                raise AssertionError("Recovery did not restore original observations bytes")
            if proposals.read_bytes() != old_prop:
                raise AssertionError("Recovery did not preserve original proposals bytes")
            if journal.exists():
                raise AssertionError("Verified recovery did not clear its journal")
    finally:
        (
            synthesis.ROOT,
            synthesis.PEOPLE_DIR,
            synthesis.OBSERVATIONS,
            synthesis.PROPOSALS,
        ) = old_paths



def test_recovery_refuses_to_overwrite_unexpected_ledger_bytes():
    old_paths = (
        synthesis.ROOT,
        synthesis.PEOPLE_DIR,
        synthesis.OBSERVATIONS,
        synthesis.PROPOSALS,
    )
    try:
        with tempfile.TemporaryDirectory(prefix="synthesis-pair-conflict-") as temp:
            root = Path(temp)
            people, observations, proposals, old_obs, old_prop = setup_fixture(root)
            synthesis.ROOT = root
            synthesis.PEOPLE_DIR = people
            synthesis.OBSERVATIONS = observations
            synthesis.PROPOSALS = proposals

            intended_obs = b'{"observation_id":"INTENDED-OBS"}\\n'
            intended_prop = b'{"proposal_id":"INTENDED-PROP"}\\n'
            synthesis._write_transaction_journal(intended_obs, intended_prop)

            unexpected = b'{"observation_id":"UNEXPECTED-NEW-CONTENT"}\\n'
            observations.write_bytes(unexpected)
            journal = synthesis.transaction_journal_path()

            try:
                synthesis._recover_transaction()
            except RuntimeError as error:
                if "Unexpected current bytes" not in str(error):
                    raise
            else:
                raise AssertionError(
                    "Recovery accepted unexpected ledger content"
                )

            if observations.read_bytes() != unexpected:
                raise AssertionError(
                    "Recovery overwrote unexpected observations content"
                )
            if proposals.read_bytes() != old_prop:
                raise AssertionError(
                    "Recovery changed the untouched proposals ledger"
                )
            if not journal.exists():
                raise AssertionError(
                    "Recovery removed its journal despite an unresolved conflict"
                )
    finally:
        (
            synthesis.ROOT,
            synthesis.PEOPLE_DIR,
            synthesis.OBSERVATIONS,
            synthesis.PROPOSALS,
        ) = old_paths



def test_malformed_journal_root_is_rejected_and_preserved():
    old_paths = (
        synthesis.ROOT,
        synthesis.PEOPLE_DIR,
        synthesis.OBSERVATIONS,
        synthesis.PROPOSALS,
    )
    try:
        with tempfile.TemporaryDirectory(prefix="synthesis-pair-bad-journal-") as temp:
            root = Path(temp)
            people, observations, proposals, old_obs, old_prop = setup_fixture(root)
            synthesis.ROOT = root
            synthesis.PEOPLE_DIR = people
            synthesis.OBSERVATIONS = observations
            synthesis.PROPOSALS = proposals

            journal = synthesis.transaction_journal_path()
            malformed_root = b'[]'
            journal.write_bytes(malformed_root)

            try:
                synthesis._recover_transaction()
            except RuntimeError as error:
                if "Unsupported or invalid transaction journal" not in str(error):
                    raise
            else:
                raise AssertionError("Recovery accepted a non-object journal root")

            if journal.read_bytes() != malformed_root:
                raise AssertionError("Recovery changed the malformed journal")
            if observations.read_bytes() != old_obs:
                raise AssertionError("Recovery changed original observations")
            if proposals.read_bytes() != old_prop:
                raise AssertionError("Recovery changed original proposals")
    finally:
        (
            synthesis.ROOT,
            synthesis.PEOPLE_DIR,
            synthesis.OBSERVATIONS,
            synthesis.PROPOSALS,
        ) = old_paths


def test_unresolved_transaction_blocks_another_write():
    old_paths = (
        synthesis.ROOT,
        synthesis.PEOPLE_DIR,
        synthesis.OBSERVATIONS,
        synthesis.PROPOSALS,
    )
    try:
        with tempfile.TemporaryDirectory(prefix="synthesis-pair-guard-") as temp:
            root = Path(temp)
            people, observations, proposals, _, _ = setup_fixture(root)
            synthesis.ROOT = root
            synthesis.PEOPLE_DIR = people
            synthesis.OBSERVATIONS = observations
            synthesis.PROPOSALS = proposals

            synthesis._write_transaction_journal(
                b'{"observation_id":"INTENDED-OBS"}\\n',
                b'{"proposal_id":"INTENDED-PROP"}\\n',
            )
            journal = synthesis.transaction_journal_path()
            if not journal.exists():
                raise AssertionError("Expected transaction journal was not written")

            for check in (False, True):
                try:
                    synthesis.build(check=check)
                except RuntimeError as error:
                    if "Unresolved synthesis transaction" not in str(error):
                        raise
                else:
                    raise AssertionError(
                        f"build(check={check}) did not block an unresolved transaction"
                    )

            if not journal.exists():
                raise AssertionError("Build guard unexpectedly removed the journal")
    finally:
        (
            synthesis.ROOT,
            synthesis.PEOPLE_DIR,
            synthesis.OBSERVATIONS,
            synthesis.PROPOSALS,
        ) = old_paths



def test_process_lock_serializes_and_releases():
    old_root = synthesis.ROOT
    try:
        with tempfile.TemporaryDirectory(prefix="synthesis-process-lock-") as temp:
            synthesis.ROOT = Path(temp)
            entered = threading.Event()
            acquired = threading.Event()

            def contender():
                entered.set()
                with synthesis.synthesis_process_lock():
                    acquired.set()

            with synthesis.synthesis_process_lock():
                worker = threading.Thread(target=contender, daemon=True)
                worker.start()
                if not entered.wait(2):
                    raise AssertionError("Contender thread did not start")
                if acquired.wait(0.2):
                    raise AssertionError("Second thread entered while lock was held")

            worker.join(2)
            if worker.is_alive() or not acquired.is_set():
                raise AssertionError("Second thread did not acquire released lock")

            try:
                with synthesis.synthesis_process_lock():
                    raise ValueError("simulated failure")
            except ValueError:
                pass

            with synthesis.synthesis_process_lock():
                pass
    finally:
        synthesis.ROOT = old_root


def main():
    test_second_publication_failure_preserves_recovery_evidence()
    test_recovery_restores_both_original_ledgers_after_partial_publish()
    test_recovery_refuses_to_overwrite_unexpected_ledger_bytes()
    test_malformed_journal_root_is_rejected_and_preserved()
    test_unresolved_transaction_blocks_another_write()
    test_process_lock_serializes_and_releases()
    print("SYNTHESIS PAIR TRANSACTION TESTS: PASS")


if __name__ == "__main__":
    main()
