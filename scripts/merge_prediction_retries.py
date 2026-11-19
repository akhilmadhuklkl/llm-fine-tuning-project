"""Replace selected prediction records with validated targeted retries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base")
    parser.add_argument("retry")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    retries = {record["id"]: record for record in read_records(Path(args.retry))}
    merged = [retries.get(record["id"], record) for record in read_records(Path(args.base))]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in merged), encoding="utf-8")
    print(f"Merged {len(retries)} retry record(s) into {len(merged)} prediction(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
