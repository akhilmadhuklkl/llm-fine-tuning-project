"""Run one incident through the local constrained hybrid pipeline."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Triage one IT incident locally")
    parser.add_argument("text", help="Incident description")
    parser.add_argument("--model-config", default="configs/model_qwen_local.yaml")
    parser.add_argument("--adapter-dir", default="models/qwen2.5-0.5b-lora-exp005")
    parser.add_argument("--max-new-tokens", type=int, default=384)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        prompts = root / "prompt.jsonl"
        raw = root / "raw.jsonl"
        normalized = root / "normalized.jsonl"
        safety_report = root / "safety_report.json"
        prompts.write_text(
            json.dumps({"id": "local-incident", "messages": [{"role": "user", "content": args.text}]}) + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            [sys.executable, "scripts/run_baseline.py", "--model-config", args.model_config,
             "--prompts", str(prompts), "--max-new-tokens", str(args.max_new_tokens),
             "--adapter-dir", args.adapter_dir, "--constrain-json", "--output", str(raw)],
            check=True,
        )
        subprocess.run(
            [sys.executable, "scripts/normalize_predictions.py", str(raw), str(prompts), "--output", str(normalized)],
            check=True,
        )
        subprocess.run(
            [sys.executable, "scripts/check_safety_outputs.py", str(normalized), "--output", str(safety_report)],
            check=True,
        )
        result = json.loads(normalized.read_text(encoding="utf-8").splitlines()[0])
        print(result["response"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
