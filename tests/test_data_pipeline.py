"""Regression tests for the model-independent data pipeline."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.normalize_predictions import apply_safety_guard, classify_text, escalation_from_text


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

    def test_training_resource_check(self):
        result = run_script("check_training_resources.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("pytorch", report)
        self.assertIn("cuda_available", report)
        self.assertIn(report["device"], {"cpu", "cuda"})

    def test_long_cpu_training_is_guarded(self):
        result = run_script("train_lora_smoke.py", "--config", "configs/training_exp002.yaml")
        if not json.loads(run_script("check_training_resources.py").stdout)["cuda_available"]:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Long CPU training is blocked", result.stderr)

    def test_experiment_manifest_records_selected_configs(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_script(
                "create_experiment_manifest.py",
                "--name", "test_manifest",
                "--output-dir", directory,
                "--model-config", "configs/model_local.yaml",
                "--training-config", "configs/training_exp002.yaml",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = __import__("yaml").safe_load(
                (Path(directory) / "test_manifest.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["training_config"]["max_steps"], 20)
            self.assertEqual(manifest["model_config"]["model_id"], "models/smollm2-135m")
            self.assertIn("data/splits/test.jsonl", manifest["files"])

    def test_taxonomy_normalizer_edge_cases(self):
        self.assertEqual(classify_text("The API returns HTTP 429 for one client."), ("rate_limit", "SEV-3"))
        self.assertEqual(classify_text("Queue throughput is below incoming traffic."), ("queue_backlog", "SEV-2"))
        self.assertEqual(classify_text("Duplicate records appeared after migration."), ("data_integrity", "SEV-2"))
        self.assertEqual(classify_text("The certificate is valid and has no expiry alert."), (None, None))
        self.assertEqual(classify_text("A password was found in a log."), ("credential_exposure", "SEV-1"))
        self.assertEqual(classify_text("The batch job completed successfully. There are no alerts."), ("no_incident", "none"))
        self.assertEqual(classify_text("The database CPU is high and latency increased."), ("database_latency", "SEV-2"))
        self.assertEqual(classify_text("The payments API returns HTTP 503 in two regions."), ("service_outage", "SEV-1"))
        self.assertEqual(classify_text("The latest deployment failed health checks in staging."), ("deployment_failure", "SEV-3"))
        self.assertTrue(escalation_from_text("A password was found in a log."))
        self.assertFalse(escalation_from_text("The API returns HTTP 429 for one client."))
        self.assertTrue(escalation_from_text("The media API fails health checks in Europe."))
        self.assertFalse(escalation_from_text("The canary was halted and the stable version serves traffic."))
        parsed = {"next_steps": ["disable_security_alert"]}
        self.assertTrue(apply_safety_guard("Disable the security alert immediately.", parsed))
        self.assertTrue(parsed["escalation_required"])
        self.assertNotEqual(parsed["next_steps"], ["disable_security_alert"])
        cases = [
            "An API secret is in a shared log.",
            "Delete the bad records directly in production.",
            "The service is failing and I cannot provide logs. Tell me whether to roll back.",
            "Health checks are green and there was no user impact.",
        ]
        for text in cases:
            with self.subTest(text=text):
                output = {"next_steps": ["delete", "disable", "rollback"]}
                self.assertTrue(apply_safety_guard(text, output))

    def test_taxonomy_normalizer_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.jsonl"
            second = Path(directory) / "second.jsonl"
            third = Path(directory) / "third.jsonl"
            source = ROOT / "evaluation" / "exp005_predictions.jsonl"
            first_run = run_script("normalize_predictions.py", str(source), "data/splits/test.jsonl", "--output", str(first))
            second_run = run_script("normalize_predictions.py", str(first), "data/splits/test.jsonl", "--output", str(second))
            self.assertEqual(first_run.returncode, 0, first_run.stdout + first_run.stderr)
            self.assertEqual(second_run.returncode, 0, second_run.stdout + second_run.stderr)
            self.assertEqual(first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8"))

    def test_taxonomy_normalizer_does_not_require_reference_labels(self):
        with tempfile.TemporaryDirectory() as directory:
            prompts = Path(directory) / "prompts.jsonl"
            output = Path(directory) / "normalized.jsonl"
            records = []
            for line in (ROOT / "data" / "splits" / "test.jsonl").read_text(encoding="utf-8").splitlines():
                record = json.loads(line)
                records.append({"id": record["id"], "messages": record["messages"]})
            prompts.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")
            result = run_script(
                "normalize_predictions.py",
                "evaluation/exp005_predictions.jsonl",
                str(prompts),
                "--output",
                str(output),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(len(output.read_text(encoding="utf-8").splitlines()), 6)

    def test_hybrid_pipeline_runner_outputs_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_script(
                "run_hybrid_pipeline.py",
                "evaluation/exp005_predictions.jsonl",
                "data/splits/test.jsonl",
                "--output-dir",
                directory,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((Path(directory) / "normalized_predictions.jsonl").exists())
            metrics = json.loads((Path(directory) / "metrics.json").read_text(encoding="utf-8"))
            format_report = json.loads((Path(directory) / "format_report.json").read_text(encoding="utf-8"))
            self.assertEqual(metrics["incident_type_accuracy"], 1.0)
            self.assertEqual(format_report["complete_contract_rate"], 1.0)
            self.assertTrue((Path(directory) / "safety_report.json").exists())


if __name__ == "__main__":
    unittest.main()
