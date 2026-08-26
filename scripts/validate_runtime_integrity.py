#!/usr/bin/env python3
"""Validate and deterministically dry-run every T4H Goose recipe."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.2.0"
PLACEHOLDER = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()


def render(value, parameters):
    if isinstance(value, str):
        return PLACEHOLDER.sub(lambda m: str(parameters[m.group(1)]), value)
    if isinstance(value, dict):
        return {key: render(item, parameters) for key, item in value.items()}
    if isinstance(value, list):
        return [render(item, parameters) for item in value]
    return value


def sample_parameters(recipe):
    values = {}
    for parameter in recipe.get("parameters", []):
        key = parameter["key"]
        if "default" in parameter:
            values[key] = parameter["default"]
        elif key == "idempotency_key":
            values[key] = "redacted-validation-idempotency-key"
        else:
            values[key] = f"validation-{key}"
    return values


def validate_recipe_shape(path, recipe, errors):
    required = {"version", "title", "description", "instructions", "prompt", "settings"}
    missing = required - set(recipe or {})
    if missing:
        errors.append(f"{path}: missing {sorted(missing)}")
        return
    if str(recipe["version"]) != VERSION:
        errors.append(f"{path}: version {recipe['version']} != {VERSION}")
    keys = [p.get("key") for p in recipe.get("parameters", [])]
    if len(keys) != len(set(keys)):
        errors.append(f"{path}: duplicate parameter keys")
    available = set(keys)
    used = set(PLACEHOLDER.findall(recipe["instructions"] + "\n" + recipe["prompt"]))
    unknown = used - available
    if unknown:
        errors.append(f"{path}: undeclared placeholders {sorted(unknown)}")
    retry = recipe.get("retry")
    if retry:
        for field in ("max_retries", "timeout_seconds", "backoff_seconds", "recovery"):
            if field not in retry:
                errors.append(f"{path}: retry missing {field}")


def execute_recipe(path, recipe, errors):
    parameters = sample_parameters(recipe)
    rendered_prompt = render(recipe["prompt"], parameters)
    rendered_instructions = render(recipe["instructions"], parameters)
    if PLACEHOLDER.search(rendered_prompt + rendered_instructions):
        errors.append(f"{path}: unresolved top-level placeholder")
    children = []
    for sub in recipe.get("sub_recipes", []):
        child_path = (path.parent / sub["path"]).resolve()
        try:
            child_path.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path}: subrecipe escapes repository: {sub['path']}")
            continue
        if not child_path.is_file():
            errors.append(f"{path}: missing subrecipe {sub['path']}")
            continue
        child = load_yaml(child_path)
        required_child = {p["key"] for p in child.get("parameters", []) if p.get("requirement") == "required"}
        supplied = set(sub.get("values", {}))
        missing = required_child - supplied
        if missing:
            errors.append(f"{path}: {sub['name']} missing values {sorted(missing)}")
            continue
        child_values = render(sub["values"], parameters)
        child_text = render(child["prompt"] + "\n" + child["instructions"], child_values)
        if PLACEHOLDER.search(child_text):
            errors.append(f"{path}: {sub['name']} has unresolved placeholder")
        children.append(str(child_path.relative_to(ROOT)))
    return {
        "recipe": str(path.relative_to(ROOT)),
        "prompt_sha256": hashlib.sha256(rendered_prompt.encode()).hexdigest(),
        "instructions_sha256": hashlib.sha256(rendered_instructions.encode()).hexdigest(),
        "resolved_subrecipes": children,
        "status": "PASS",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--timestamp", default=None, help="ISO timestamp; omit for current UTC")
    args = parser.parse_args()
    errors = []

    for schema_path in sorted((ROOT / "schemas").glob("*.json")):
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{schema_path}: invalid JSON schema: {exc}")

    catalogue = load_yaml(ROOT / "registry/recipe_catalogue.yaml")
    index = load_yaml(ROOT / "registry/recipe-index.yaml")
    catalogue_paths = [f"recipes/{item}" for item in catalogue["recipes"]]
    filesystem_paths = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "recipes").rglob("*.yaml"))
    index_paths = [item["path"] for item in index["recipes"]]

    if str(catalogue["version"]) != VERSION or str(index["version"]) != VERSION:
        errors.append("registry version mismatch")
    if sorted(catalogue_paths) != filesystem_paths:
        errors.append("catalogue and filesystem recipe sets differ")
    if sorted(index_paths) != filesystem_paths:
        errors.append("index and filesystem recipe sets differ")
    if len(index_paths) != len(set(index_paths)):
        errors.append("duplicate paths in recipe index")
    ids = [item["id"] for item in index["recipes"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate IDs in recipe index")

    executions = []
    for relative in filesystem_paths:
        path = ROOT / relative
        recipe = load_yaml(path)
        validate_recipe_shape(path.relative_to(ROOT), recipe, errors)
        executions.append(execute_recipe(path, recipe, errors))

    for item in index["recipes"]:
        recipe = load_yaml(ROOT / item["path"])
        if str(item["version"]) != str(recipe["version"]):
            errors.append(f"{item['id']}: index/file version mismatch")
        if "structured-result" not in item["outputs"]:
            errors.append(f"{item['id']}: structured-result output missing")

    timestamp = args.timestamp or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    body = {
        "schema_version": VERSION,
        "suite": "runtime-integrity-local-contract-execution",
        "timestamp": timestamp,
        "execution_mode": "deterministic-local-dry-run",
        "goose_runtime": "UNPROVEN_NOT_INSTALLED",
        "recipe_count": len(executions),
        "recipes": executions,
        "errors": errors,
        "verification_status": "PASS" if not errors else "BLOCKED",
        "redactions": ["parameter values replaced with deterministic validation placeholders", "no credentials recorded"],
    }
    body["result_digest"] = "sha256:" + hashlib.sha256(canonical(body)).hexdigest()
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": body["verification_status"], "recipes": len(executions), "errors": errors, "digest": body["result_digest"]}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
