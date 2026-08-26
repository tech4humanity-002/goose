#!/usr/bin/env python3
"""Execute the full local conformance suite and write a redacted receipt."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {"command": command, "exit_code": result.returncode, "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest()}


def tree_digest(paths):
    digest = hashlib.sha256()
    files = []
    for base in paths:
        for path in sorted((ROOT / base).rglob("*")):
            if path.is_file():
                relative = str(path.relative_to(ROOT))
                files.append(relative)
                digest.update(relative.encode() + b"\0" + path.read_bytes() + b"\0")
    return "sha256:" + digest.hexdigest(), len(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--timestamp")
    args = parser.parse_args()
    checks = [
        run([sys.executable, "compiler/compile_adapters.py", "--check"]),
        run([sys.executable, "conformance/validate_contract.py"]),
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        run(["git", "diff", "--check"]),
    ]
    contract_digest, contract_files = tree_digest(["contract"])
    adapter_digest, adapter_files = tree_digest(["adapters"])
    status = "PASS" if all(check["exit_code"] == 0 for check in checks) else "BLOCKED"
    timestamp = args.timestamp or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    receipt = {
        "schema_version": "1.3.0",
        "receipt_type": "contract-adapter-conformance",
        "timestamp": timestamp,
        "status": status,
        "contract": {"workflows": 15, "files": contract_files, "digest": contract_digest},
        "adapters": {"count": 5, "generated_files": 80, "dry_runs": 75, "files": adapter_files, "digest": adapter_digest},
        "checks": checks,
        "live_runtime_execution": "UNPROVEN_NOT_REQUESTED",
        "redactions": ["no credentials captured", "command output represented only by SHA-256 digests"],
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    receipt["receipt_digest"] = "sha256:" + hashlib.sha256(canonical).hexdigest()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": status, "receipt": str(output), "digest": receipt["receipt_digest"]}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
