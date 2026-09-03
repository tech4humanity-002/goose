#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PASS=0; WARN=0; FAIL=0
pass(){ echo "PASS  $1"; PASS=$((PASS+1)); }
warn(){ echo "WARN  $1"; WARN=$((WARN+1)); }
fail(){ echo "FAIL  $1"; FAIL=$((FAIL+1)); }

command -v goose >/dev/null 2>&1 && pass "Goose installed" || fail "Goose installed"
python3 "$ROOT/conformance/validate_contract.py" >/dev/null 2>&1 && pass "Canonical contract and adapters conform" || fail "Contract conformance"
[[ -d "$ROOT/adapters/goose/generated/recipes" ]] && pass "Generated Goose recipes present" || fail "Generated Goose recipes"
if [[ -n "${T4H_BAD_MCP_URI:-}" && -n "${T4H_BAD_MCP_CMD:-}" ]]; then
  fail "Configure exactly one bad-mcp transport"
elif [[ -n "${T4H_BAD_MCP_URI:-}${T4H_BAD_MCP_CMD:-}" ]]; then
  pass "bad-mcp transport supplied"
else
  warn "bad-mcp transport not configured"
fi
echo "SUMMARY: PASS=$PASS WARN=$WARN FAIL=$FAIL"
[[ $FAIL -eq 0 ]]
