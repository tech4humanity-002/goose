import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RuntimeIntegrityTest(unittest.TestCase):
    def test_all_recipes_resolve_and_execute(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / "receipt.json"
            subprocess.run(
                ["python3", "scripts/validate_runtime_integrity.py", "--receipt", str(receipt), "--timestamp", "2026-08-26T09:00:00Z"],
                cwd=ROOT,
                check=True,
            )
            data = json.loads(receipt.read_text())
            self.assertEqual("PASS", data["verification_status"])
            self.assertEqual(15, data["recipe_count"])
            self.assertEqual([], data["errors"])

    def test_schemas_are_json(self):
        schemas = list((ROOT / "schemas").glob("*.json"))
        self.assertGreaterEqual(len(schemas), 5)
        for schema in schemas:
            self.assertIn("$schema", json.loads(schema.read_text()))

    def test_committed_receipt_is_redacted_and_complete(self):
        receipt = json.loads((ROOT / "receipts/runtime-integrity-v1.2.0.json").read_text())
        self.assertEqual("PASS", receipt["verification_status"])
        self.assertEqual(15, receipt["recipe_count"])
        self.assertEqual([], receipt["errors"])
        self.assertEqual("UNPROVEN_NOT_INSTALLED", receipt["goose_runtime"])
        self.assertTrue(receipt["redactions"])

    def test_installer_is_local_only_and_preserves_bad_mcp_injection(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            fake_bin = home / "fake-bin"
            fake_bin.mkdir()
            goose = fake_bin / "goose"
            goose.write_text(
                "#!/usr/bin/env bash\n"
                "if [[ ${1:-} == recipe && ${2:-} == validate ]]; then exit 0; fi\n"
                "if [[ ${1:-} == --version ]]; then echo 'goose-test'; exit 0; fi\n"
                "exit 0\n"
            )
            goose.chmod(0o755)
            env = os.environ.copy()
            env.update({"HOME": str(home), "PATH": f"{fake_bin}:{env['PATH']}", "T4H_AUTO_CREATE_REPO": "1"})
            subprocess.run(["bash", "scripts/install.sh"], cwd=ROOT, env=env, check=True, capture_output=True, text=True)
            wrapper = home / "bin/t4h-goose"
            text = wrapper.read_text()
            self.assertIn("--with-streamable-http-extension", text)
            self.assertIn("--with-extension", text)
            self.assertNotIn("gh repo", (home / ".config/goose/t4h-goose/scripts/install.sh").read_text())
            conflict = env | {"T4H_BAD_MCP_URI": "https://redacted.invalid", "T4H_BAD_MCP_CMD": "redacted-command"}
            result = subprocess.run([str(wrapper), "--version"], env=conflict, capture_output=True, text=True)
            self.assertEqual(64, result.returncode)


if __name__ == "__main__":
    unittest.main()
