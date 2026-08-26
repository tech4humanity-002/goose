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


def load_profiles():
    rows = []
    for path in sorted((ROOT / "contract/platforms").glob("*.yaml")):
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


def profile_markdown(platform: str, source: Path, profile: dict) -> str:
    relative = str(source.relative_to(ROOT))
    header = generated_header(relative, digest(source))
    capabilities = "\n".join(f"- `{name}`: {binding}" for name, binding in profile["capability_bindings"].items())
    boundaries = "\n".join(f"- {rule}" for rule in profile["boundaries"])
    sources = "\n".join(f"- `{name}`: {url}" for name, url in profile["mutable_facts"]["sources"].items())
    legacy = ", ".join(f"`{name}`" for name in profile["sdk"]["legacy_packages"]) or "None"
    return f"""<!-- {header.replace(chr(10), ' | ').strip()} -->
# {profile['provider']} {profile['id']} platform profile

Adapter target: `{platform}`

Contract version: `{profile['contract_version']}`

{profile['role']}

## SDK and authentication

- Python package: `{profile['sdk']['python_package']}` ({profile['sdk']['version_policy']})
- Legacy packages prohibited for new work: {legacy}
- Credential variable: `{profile['authentication']['environment_variable']}`

## Capability bindings

{capabilities}

## Runtime boundaries

{boundaries}

## Mutable provider facts

Checked: `{profile['mutable_facts']['checked_at']}`

Review due: `{profile['mutable_facts']['review_due']}`

Refresh before use: `{str(profile['mutable_facts']['refresh_before_use']).lower()}`

{sources}
"""


def expected_files():
    workflows = load_workflows()
    profiles = load_profiles()
    contract_version = yaml.safe_load((ROOT / "contract/manifest.yaml").read_text(encoding="utf-8"))["contract_version"]
    expected = {}
    for platform in PLATFORMS:
        adapter = yaml.safe_load((ROOT / "adapters" / platform / "adapter.yaml").read_text(encoding="utf-8"))
        manifest = {
            "generated": True,
            "adapter": platform,
            "contract_version": contract_version,
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
        for source, profile in profiles:
            key = f"adapters/{platform}/generated/profiles/{profile['id']}.md"
            expected[key] = profile_markdown(platform, source, profile)
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
        print(json.dumps({"status": "PASS", "generated_files": len(expected), "workflows": len(load_workflows()), "profiles": len(load_profiles())}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
