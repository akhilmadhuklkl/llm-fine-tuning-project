"""Serve the local custom incident-triage UI and API."""

from __future__ import annotations

import json
import argparse
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "ui"


class Handler(SimpleHTTPRequestHandler):
    MAX_BODY_BYTES = 16 * 1024

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI), **kwargs)

    def do_POST(self):
        if self.path != "/api/triage":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > self.MAX_BODY_BYTES:
                raise ValueError("Request body must be between 1 and 16384 bytes")
            payload = json.loads(self.rfile.read(length))
            text = str(payload.get("text", "")).strip()
            if not text or len(text) > 2000:
                raise ValueError("Incident text must contain 1–2000 characters")
            completed = subprocess.run(
                [sys.executable, "scripts/triage_incident.py", text, "--max-new-tokens", "128"],
                cwd=ROOT, capture_output=True, text=True, timeout=180, check=True,
            )
            response = None
            for line in reversed(completed.stdout.splitlines()):
                try:
                    response = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue
            if response is None:
                raise RuntimeError("The triage process returned no JSON response")
            self._write_json(200, response)
        except subprocess.TimeoutExpired:
            self._write_json(504, {"error": "Triage timed out; check that the local model is available."})
        except Exception as exc:
            self._write_json(500, {"error": str(exc)})

    def _write_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8501)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Incident Triage UI: http://127.0.0.1:{args.port}")
    server.serve_forever()
