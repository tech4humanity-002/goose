#!/usr/bin/env python3
"""Validate neutral contract integrity and adapter conformance."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")


def main():
    errors = []
    workflows = {}
    for path in sorted((ROOT / "contract/workflows").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        workflow_id = data.get("id")
        if workflow_id in workflows:
            errors.append(f"duplicate workflow id: {workflow_id}")
        workflows[workflow_id] = (path, data)
        if data.get("schema_version") != "1.0.0" or data.get("contract_version") != "1.3.0":
            errors.append(f"{path}: version mismatch")
        parameter_keys = {p["key"] for p in data.get("parameters", [])}
        unknown = set(TOKEN.findall(data.get("instructions", ""))) - parameter_keys
        if unknown:
            errors.append(f"{path}: undeclared placeholders {sorted(unknown)}")
        retry = data.get("execution", {}).get("retry", {})
        for key in ("max_retries", "timeout_seconds", "backoff_seconds", "recovery"):
            if key not in retry:
                errors.append(f"{path}: retry missing {key}")
        if "structured-result" not in data.get("outputs", []):
            errors.append(f"{path}: structured-result missing")

    for workflow_id, (path, data) in workflows.items():
        parent_params = {p["key"] for p in data.get("parameters", [])}
        for step in data.get("steps", []):
            child_id = step["workflow"]
            if child_id not in workflows:
                errors.append(f"{path}: missing child workflow {child_id}")
                continue
            child = workflows[child_id][1]
            required = {p["key"] for p in child.get("parameters", []) if p["requirement"] == "required"}
            if required - set(step.get("bindings", {})):
                errors.append(f"{path}: incomplete bindings for {child_id}")
            for value in step.get("bindings", {}).values():
                unknown = set(TOKEN.findall(str(value))) - parent_params
                if unknown:
                    errors.append(f"{path}: child binding uses undeclared {sorted(unknown)}")

    manifest = yaml.safe_load((ROOT / "contract/manifest.yaml").read_text())
    for platform in manifest["generated_adapters"]:
        adapter = ROOT / "adapters" / platform
        if not adapter.is_dir():
            errors.append(f"missing adapter: {platform}")
        if not (adapter / "adapter.yaml").is_file():
            errors.append(f"missing adapter declaration: {platform}")

    drift = subprocess.run([sys.executable, "compiler/compile_adapters.py", "--check"], cwd=ROOT, capture_output=True, text=True)
    if drift.returncode:
        errors.append(f"generated adapter drift: {drift.stdout.strip()}")

    result = {"status": "PASS" if not errors else "BLOCKED", "workflows": len(workflows), "adapters": len(manifest["generated_adapters"]), "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
