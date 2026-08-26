#!/usr/bin/env python3
"""Compile the neutral T4H contract into deterministic platform adapters."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ("goose", "aider", "codex", "claude-code", "gemini-cli")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_header(source: str, source_digest: str) -> str:
    return f"GENERATED FILE — DO NOT EDIT\nSource: {source}\nSource SHA-256: {source_digest}\n"


def load_workflows():
    rows = []
    for path in sorted((ROOT / "contract/workflows").glob("*.yaml")):
        rows.append((path, yaml.safe_load(path.read_text(encoding="utf-8"))))
    return rows


def prompt_markdown(platform: str, source: Path, workflow: dict) -> str:
    relative = str(source.relative_to(ROOT))
    header = generated_header(relative, digest(source))
    params = "\n".join(f"- `{p['key']}` ({p['requirement']}): {p['description']}" for p in workflow["parameters"]) or "- None"
    steps = "\n".join(f"- `{s['workflow']}`: {s['description']}" for s in workflow["steps"]) or "- None"
    retry = workflow["execution"]["retry"]
    return f"""<!-- {header.replace(chr(10), ' | ').strip()} -->
# {workflow['title']}

Platform: `{platform}`  
Canonical workflow: `{workflow['id']}`  
Contract version: `{workflow['contract_version']}`

## Parameters

{params}

## Required stages

{steps}

## Operating instruction

{workflow['instructions'].strip()}

## Execution contract

- Maximum turns: {workflow['execution']['max_turns']}
- Timeout: {retry['timeout_seconds']} seconds
- Maximum retries: {retry['max_retries']}
- Backoff: {retry['backoff_seconds']}
- Recovery: `{retry['recovery']}`
- Required outputs: {', '.join(workflow['outputs'])}

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
"""


def goose_recipe(source: Path, workflow: dict) -> str:
    relative = str(source.relative_to(ROOT))
    data = {
        "version": workflow["contract_version"],
        "title": workflow["title"],
        "description": workflow["purpose"],
        "parameters": workflow["parameters"],
        "instructions": workflow["instructions"],
        "prompt": f"Execute canonical workflow {workflow['id']} using its supplied parameters.",
        "settings": {"max_turns": workflow["execution"]["max_turns"]},
        "retry": workflow["execution"]["retry"],
    }
    if workflow["steps"]:
        data["sub_recipes"] = [
            {
                "name": step["workflow"],
                "path": f"./{step['workflow']}.yaml",
                "description": step["description"],
                "values": step["bindings"],
            }
            for step in workflow["steps"]
        ]
    header = generated_header(relative, digest(source))
    return "".join(f"# {line}\n" for line in header.rstrip().splitlines()) + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def expected_files():
    workflows = load_workflows()
    expected = {}
    for platform in PLATFORMS:
        adapter = yaml.safe_load((ROOT / "adapters" / platform / "adapter.yaml").read_text(encoding="utf-8"))
        manifest = {
            "generated": True,
            "adapter": platform,
            "contract_version": "1.3.0",
            "workflow_count": len(workflows),
            "workflows": [row[1]["id"] for row in workflows],
            "unsupported_capabilities": adapter.get("unsupported_capabilities", []),
        }
        expected[f"adapters/{platform}/generated/manifest.yaml"] = yaml.safe_dump(manifest, sort_keys=False)
        for source, workflow in workflows:
            if platform == "goose":
                key = f"adapters/goose/generated/recipes/{workflow['id']}.yaml"
                expected[key] = goose_recipe(source, workflow)
            else:
                key = f"adapters/{platform}/generated/messages/{workflow['id']}.md"
                expected[key] = prompt_markdown(platform, source, workflow)
    return expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failures = []
    expected = expected_files()
    for relative, content in expected.items():
        path = ROOT / relative
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if args.check:
        known = set(expected)
        for platform in PLATFORMS:
            generated = ROOT / "adapters" / platform / "generated"
            if generated.exists():
                for path in generated.rglob("*"):
                    if path.is_file() and str(path.relative_to(ROOT)) not in known:
                        failures.append(str(path.relative_to(ROOT)))
        if failures:
            print(json.dumps({"status": "DRIFT", "files": sorted(set(failures))}, indent=2))
            return 1
        print(json.dumps({"status": "PASS", "generated_files": len(expected), "workflows": 15}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
