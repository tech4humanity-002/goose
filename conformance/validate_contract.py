#!/usr/bin/env python3
"""Validate neutral contract integrity and adapter conformance."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")


def schema_errors(instance, schema, location="$"):
    """Validate the strict JSON Schema subset used by this repository."""
    errors = []
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{location}: expected {schema['const']!r}")
    expected = schema.get("type")
    matches = {
        "object": isinstance(instance, dict),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
        "integer": isinstance(instance, int) and not isinstance(instance, bool),
    }
    if expected in matches and not matches[expected]:
        return errors + [f"{location}: expected {expected}"]
    if isinstance(instance, dict):
        required = set(schema.get("required", []))
        errors.extend(f"{location}: missing {key}" for key in sorted(required - set(instance)))
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        if additional is False:
            errors.extend(f"{location}: unexpected {key}" for key in sorted(set(instance) - set(properties)))
        for key, value in instance.items():
            child_schema = properties.get(key, additional if isinstance(additional, dict) else None)
            if child_schema:
                errors.extend(schema_errors(value, child_schema, f"{location}.{key}"))
        if len(instance) < schema.get("minProperties", 0):
            errors.append(f"{location}: too few properties")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{location}: too few items")
        if isinstance(schema.get("items"), dict):
            for index, value in enumerate(instance):
                errors.extend(schema_errors(value, schema["items"], f"{location}[{index}]"))
        if "contains" in schema and not any(not schema_errors(value, schema["contains"]) for value in instance):
            errors.append(f"{location}: contains requirement not met")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{location}: string too short")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{location}: pattern mismatch")
    if isinstance(instance, int) and instance < schema.get("minimum", instance):
        errors.append(f"{location}: below minimum")
    return errors


def main():
    errors = []
    manifest = yaml.safe_load((ROOT / "contract/manifest.yaml").read_text())
    contract_version = manifest["contract_version"]
    workflow_schema = json.loads((ROOT / "contract/schemas/workflow.schema.json").read_text())
    workflows = {}
    for path in sorted((ROOT / "contract/workflows").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        workflow_id = data.get("id")
        if workflow_id in workflows:
            errors.append(f"duplicate workflow id: {workflow_id}")
        workflows[workflow_id] = (path, data)
        if data.get("schema_version") != "1.0.0" or data.get("contract_version") != contract_version:
            errors.append(f"{path}: version mismatch")
        errors.extend(f"{path}: schema violation: {error}" for error in schema_errors(data, workflow_schema))
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

    capability_schema = json.loads((ROOT / "contract/schemas/capability.schema.json").read_text())
    capability_names = set()
    for path in sorted((ROOT / "contract/capabilities").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        errors.extend(f"{path}: schema violation: {error}" for error in schema_errors(data, capability_schema))
        capability_names.update(data.get("capabilities", {}))

    profile_schema = json.loads((ROOT / "contract/schemas/platform-profile.schema.json").read_text())
    profiles = {}
    for path in sorted((ROOT / "contract/platforms").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        profiles[data.get("id")] = data
        errors.extend(f"{path}: schema violation: {error}" for error in schema_errors(data, profile_schema))
        unknown = set(data.get("capability_bindings", {})) - capability_names
        if unknown:
            errors.append(f"{path}: unknown capabilities {sorted(unknown)}")
        mutable = data.get("mutable_facts", {})
        if mutable.get("refresh_before_use") is not True:
            errors.append(f"{path}: mutable facts must refresh before use")
        try:
            if date.fromisoformat(mutable["review_due"]) < date.fromisoformat(mutable["checked_at"]):
                errors.append(f"{path}: review_due precedes checked_at")
        except (KeyError, TypeError, ValueError):
            errors.append(f"{path}: invalid mutable fact dates")

    for platform in manifest["generated_adapters"]:
        adapter = ROOT / "adapters" / platform
        if not adapter.is_dir():
            errors.append(f"missing adapter: {platform}")
        if not (adapter / "adapter.yaml").is_file():
            errors.append(f"missing adapter declaration: {platform}")

    drift = subprocess.run([sys.executable, "compiler/compile_adapters.py", "--check"], cwd=ROOT, capture_output=True, text=True)
    if drift.returncode:
        errors.append(f"generated adapter drift: {drift.stdout.strip()}")

    result = {"status": "PASS" if not errors else "BLOCKED", "workflows": len(workflows), "profiles": len(profiles), "adapters": len(manifest["generated_adapters"]), "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
