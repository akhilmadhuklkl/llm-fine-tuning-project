"""Regression tests for the model-independent data pipeline."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, f"scripts/{script}", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class DataPipelineTests(unittest.TestCase):
    def test_raw_dataset_schema(self):
        result = run_script("validate_dataset.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_each_split_schema(self):
        for split in ("train", "validation", "test"):
            with self.subTest(split=split):
                result = run_script("validate_dataset.py", f"data/splits/{split}.jsonl")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_categories_do_not_overlap(self):
        categories = {}
        for split in ("train", "validation", "test"):
            path = ROOT / "data" / "splits" / f"{split}.jsonl"
            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            categories[split] = {record["category"] for record in records}
        self.assertEqual(categories["train"] & categories["validation"], set())
        self.assertEqual(categories["train"] & categories["test"], set())
        self.assertEqual(categories["validation"] & categories["test"], set())

    def test_prepared_chat_dataset(self):
        result = run_script("validate_chat_dataset.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_quality_checks(self):
        for script in ("check_duplicates.py", "check_sensitive_data.py", "check_quality_rules.py"):
            with self.subTest(script=script):
                result = run_script(script)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unified_quality_gate(self):
        result = run_script("run_quality_gate.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_prediction_contract_checker(self):
        valid = {
            "id": "valid-1",
            "response": json.dumps({
                "severity": "SEV-3",
                "incident_type": "service_degradation",
                "affected_services": ["search-api"],
                "observed_facts": ["latency is high"],
                "hypotheses": ["dependency is slow"],
                "next_steps": ["check dependency latency"],
                "escalation_required": False,
            }),
        }
        invalid = {"id": "invalid-1", "response": '{"severity":"SEV-3"}'}
        with tempfile.TemporaryDirectory() as directory:
            predictions = Path(directory) / "predictions.jsonl"
            report = Path(directory) / "report.json"
            predictions.write_text(
                json.dumps(valid) + "\n" + json.dumps(invalid) + "\n", encoding="utf-8"
            )
            result = run_script(
                "check_prediction_format.py", str(predictions), "--output", str(report)
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(summary["valid_json"], 2)
            self.assertEqual(summary["complete_contracts"], 1)
            self.assertEqual(summary["failures"][0]["reason"], "missing_fields")


if __name__ == "__main__":
    unittest.main()
