"""Required daily research stages must fail closed before auto-publication."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "daily-research-sweep.yml"

REQUIRED_STAGES = (
    "Run four-agent orchestration",
    "Build outward document-ecology search bundle",
    "Route completed research findings",
)
COMMIT_STEP = "Commit results directly to main"


def workflow_step_body(workflow: str, step_name: str) -> str:
    pattern = (
        r"(?ms)^      - name: "
        + re.escape(step_name)
        + r"\n(?P<body>.*?)(?=^      - name: |\Z)"
    )
    match = re.search(pattern, workflow)
    if not match:
        raise AssertionError(f"Required workflow step is missing: {step_name}")
    return match.group("body")


class DailySweepWorkflowFailureBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_required_stages_do_not_tolerate_failure(self):
        for stage in REQUIRED_STAGES:
            with self.subTest(stage=stage):
                body = workflow_step_body(self.workflow, stage)
                self.assertNotRegex(
                    body,
                    r"(?m)^\s*continue-on-error:\s*true\s*$",
                    f"{stage} must fail the workflow if it fails",
                )

    def test_commit_step_follows_all_required_stages(self):
        commit_pos = self.workflow.find(f"- name: {COMMIT_STEP}")
        self.assertGreaterEqual(commit_pos, 0, "Commit step is missing")

        for stage in REQUIRED_STAGES:
            with self.subTest(stage=stage):
                stage_pos = self.workflow.find(f"- name: {stage}")
                self.assertGreaterEqual(stage_pos, 0, f"Missing stage: {stage}")
                self.assertLess(
                    stage_pos,
                    commit_pos,
                    f"{stage} must precede the commit step",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
