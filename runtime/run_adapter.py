#!/usr/bin/env python3
"""Resolve one canonical workflow and execute it through a selected adapter."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{ " + key + " }}", value).replace("{{" + key + "}}", value)
    return text


def build_prompt(workflow: dict, values: dict[str, str]) -> str:
    missing = [p["key"] for p in workflow["parameters"] if p["requirement"] == "required" and p["key"] not in values]
    if missing:
        raise ValueError("missing required parameters: " + ", ".join(missing))
    lines = [f"# {workflow['title']}", "", render(workflow["instructions"], values), "", "Required stages:"]
    for step in workflow["steps"]:
        lines.append(f"- {step['workflow']}: {step['description']} bindings={render(json.dumps(step['bindings']), values)}")
    lines.extend(["", "Return a structured result conforming to contract/schemas/result.schema.json and record evidence for contract/schemas/receipt.schema.json."])
    return "\n".join(lines)


def command(adapter: str, workflow_id: str, prompt: str, temp: Path, params: list[str]):
    if adapter == "aider":
        message = temp / "message.md"
        message.write_text(prompt)
        return ["aider", "--message-file", str(message)]
    if adapter == "codex":
        return ["codex", "exec", prompt]
    if adapter == "claude-code":
        return ["claude", "-p", prompt]
    if adapter == "gemini-cli":
        return ["gemini", "-p", prompt]
    recipe = ROOT / "adapters/goose/generated/recipes" / f"{workflow_id}.yaml"
    result = ["goose"]
    if (uri := __import__("os").environ.get("T4H_BAD_MCP_URI")):
        result += ["--with-streamable-http-extension", uri]
    elif (cmd := __import__("os").environ.get("T4H_BAD_MCP_CMD")):
        result += ["--with-extension", cmd]
    result += ["run", "--recipe", str(recipe)]
    for item in params:
        result += ["--params", item]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", required=True, choices=["goose", "aider", "codex", "claude-code", "gemini-cli"])
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--param", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    values = dict(item.split("=", 1) for item in args.param)
    source = ROOT / "contract/workflows" / f"{args.workflow}.yaml"
    if not source.is_file():
        raise SystemExit(f"unknown workflow: {args.workflow}")
    workflow = yaml.safe_load(source.read_text())
    prompt = build_prompt(workflow, values)
    with tempfile.TemporaryDirectory() as directory:
        cmd = command(args.adapter, args.workflow, prompt, Path(directory), args.param)
        if args.dry_run:
            print(json.dumps({"status": "PASS", "adapter": args.adapter, "workflow": args.workflow, "command": cmd[:2], "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()}, indent=2))
            return 0
        if not shutil.which(cmd[0]):
            raise SystemExit(f"required runtime is not installed: {cmd[0]}")
        started = dt.datetime.now(dt.timezone.utc)
        result = subprocess.run(cmd, text=True)
        completed = dt.datetime.now(dt.timezone.utc)
        print(json.dumps({"adapter": args.adapter, "workflow": args.workflow, "exit_code": result.returncode, "started_at": started.isoformat(), "completed_at": completed.isoformat()}))
        return result.returncode


if __name__ == "__main__":
    sys.exit(main())
