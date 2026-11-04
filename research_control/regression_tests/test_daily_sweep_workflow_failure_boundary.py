"""Daily research workflow must preserve hard gates and report partial runs."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "daily-research-sweep.yml"

HARD_GATES = (
    "Run daily multi-perspective sweep",
    "Validate sweep output before orchestration",
)

DOWNSTREAM_STAGES = {
    "Run four-agent orchestration": "orchestration",
    "Build outward document-ecology search bundle": "document_ecology",
    "Route completed research findings": "findings",
}


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

    def test_initial_sweep_and_validation_remain_hard_gates(self):
        for stage in HARD_GATES:
            with self.subTest(stage=stage):
                body = workflow_step_body(self.workflow, stage)
                self.assertNotRegex(
                    body,
                    r"(?m)^\s*continue-on-error:\s*true\s*$",
                    f"{stage} must fail closed",
                )

    def test_downstream_stages_continue_and_have_outcome_ids(self):
        for stage, step_id in DOWNSTREAM_STAGES.items():
            with self.subTest(stage=stage):
                body = workflow_step_body(self.workflow, stage)
                self.assertIn(f"id: {step_id}", body)
                self.assertRegex(
                    body,
                    r"(?m)^\s*continue-on-error:\s*true\s*$",
                    f"{stage} must allow later stages to run",
                )

    def test_status_report_records_all_downstream_outcomes(self):
        body = workflow_step_body(
            self.workflow, "Report downstream stage outcomes"
        )
        self.assertIn("id: run_status", body)
        self.assertIn("if: always()", body)
        self.assertIn('status="COMPLETE"', body)
        self.assertIn('status="PARTIAL"', body)
        self.assertIn("GITHUB_STEP_SUMMARY", body)

        for step_id in DOWNSTREAM_STAGES.values():
            self.assertIn(f"steps.{step_id}.outcome", body)

    def test_outputs_publish_through_review_pr_not_direct_commit(self):
        report_pos = self.workflow.find(
            "- name: Report downstream stage outcomes"
        )
        pr_pos = self.workflow.find(
            "- name: Open pull request for automated research outputs"
        )

        self.assertGreaterEqual(report_pos, 0, "Status report is missing")
        self.assertGreater(pr_pos, report_pos, "PR must follow status report")

        body = workflow_step_body(
            self.workflow, "Open pull request for automated research outputs"
        )
        self.assertIn("peter-evans/create-pull-request@v7", body)
        self.assertIn("steps.run_status.outputs.status", body)
        self.assertIn("add-paths:", body)
        self.assertNotIn("git add -A", self.workflow)
        self.assertNotIn("Commit results directly to main", self.workflow)


if __name__ == "__main__":
    unittest.main(verbosity=2)
