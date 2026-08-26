import json
import hashlib
import subprocess
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = ("goose", "aider", "codex", "claude-code", "gemini-cli")


class ContractConformanceTest(unittest.TestCase):
    def run_ok(self, *command):
        return subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)

    def test_contract_and_generated_adapters_conform(self):
        result = self.run_ok("python3", "conformance/validate_contract.py")
        data = json.loads(result.stdout)
        self.assertEqual("PASS", data["status"])
        self.assertEqual(16, data["workflows"])
        self.assertEqual(1, data["profiles"])
        self.assertEqual(5, data["adapters"])

    def test_compiler_is_deterministic_and_clean(self):
        def adapter_digest():
            digest = hashlib.sha256()
            for path in sorted((ROOT / "adapters").rglob("*")):
                if path.is_file():
                    digest.update(str(path.relative_to(ROOT)).encode() + b"\0" + path.read_bytes())
            return digest.hexdigest()

        before = adapter_digest()
        self.run_ok("python3", "compiler/compile_adapters.py")
        after = adapter_digest()
        self.assertEqual(before, after)
        self.run_ok("python3", "compiler/compile_adapters.py", "--check")

    def test_every_workflow_dry_runs_on_every_adapter(self):
        workflows = sorted(path.stem for path in (ROOT / "contract/workflows").glob("*.yaml"))
        self.assertEqual(16, len(workflows))
        for workflow_id in workflows:
            workflow = yaml.safe_load((ROOT / "contract/workflows" / f"{workflow_id}.yaml").read_text())
            parameters = []
            for parameter in workflow["parameters"]:
                value = "redacted-validation-idempotency" if parameter["key"] == "idempotency_key" else f"validation-{parameter['key']}"
                parameters.extend(["--param", f"{parameter['key']}={value}"])
            for adapter in ADAPTERS:
                result = self.run_ok("python3", "runtime/run_adapter.py", "--adapter", adapter, "--workflow", workflow_id, *parameters, "--dry-run")
                self.assertEqual("PASS", json.loads(result.stdout)["status"])

    def test_platform_gaps_are_explicit(self):
        for adapter in ADAPTERS:
            declaration = yaml.safe_load((ROOT / "adapters" / adapter / "adapter.yaml").read_text())
            self.assertEqual("1.4.0", declaration["contract_version"])
            self.assertIn("native_features", declaration)
            self.assertIn("emulated_features", declaration)
            self.assertIn("unsupported_capabilities", declaration)

    def test_gemini_profile_is_current_governed_and_generated_everywhere(self):
        profile = yaml.safe_load((ROOT / "contract/platforms/gemini.yaml").read_text())
        self.assertEqual("google-genai", profile["sdk"]["python_package"])
        self.assertIn("google-generativeai", profile["sdk"]["legacy_packages"])
        self.assertTrue(profile["mutable_facts"]["refresh_before_use"])
        self.assertEqual("GEMINI_API_KEY", profile["authentication"]["environment_variable"])
        for adapter in ADAPTERS:
            generated = (ROOT / "adapters" / adapter / "generated/profiles/gemini.md").read_text()
            self.assertIn("google-genai` (latest-compatible)", generated)
            self.assertIn("never the operating system", generated)
            self.assertIn("Refresh before use: `true`", generated)

    def test_gemini_profile_rejects_stale_pack_claims(self):
        canonical = "\n".join(path.read_text() for path in (ROOT / "contract").rglob("*") if path.is_file())
        self.assertNotIn("gemini-1.5", canonical.lower())
        self.assertNotRegex(canonical.lower(), r"60 requests per minute|2m tokens|8,?192 tokens")
        self.assertNotRegex(canonical.lower(), r"\$[0-9]+(?:\.[0-9]+)?\s*/\s*(?:1m|million) tokens")

    def test_historical_receipt_does_not_define_current_contract(self):
        historical = json.loads((ROOT / "receipts/runtime-integrity-v1.2.0.json").read_text())
        self.assertEqual("1.2.0", historical["schema_version"])
        self.assertEqual("contract", yaml.safe_load((ROOT / "STATUS.yaml").read_text())["canonical_contract"]["source"].rstrip("/"))


if __name__ == "__main__":
    unittest.main()
