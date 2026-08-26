#!/usr/bin/env bash
set -u
PASS=0; WARN=0; FAIL=0
pass(){ echo "PASS  $1"; PASS=$((PASS+1)); }
warn(){ echo "WARN  $1"; WARN=$((WARN+1)); }
fail(){ echo "FAIL  $1"; FAIL=$((FAIL+1)); }
echo "T4H GOOSE DOCTOR"
if command -v goose >/dev/null 2>&1; then pass "Goose installed: $(goose --version 2>/dev/null | head -1)"; else fail "Goose installed"; fi
if command -v git >/dev/null 2>&1; then pass "Git installed"; else fail "Git installed"; fi
[[ -f "$HOME/.config/goose/config.yaml" ]] && pass "Goose config present" || warn "Goose config absent; run goose configure"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -d "$ROOT/recipes" ]]; then pass "Recipe directory present"; else fail "Recipe directory"; fi
if command -v goose >/dev/null 2>&1; then
  while IFS= read -r -d '' f; do
    if goose recipe validate "$f" >/dev/null 2>&1; then pass "Recipe valid: ${f#$ROOT/}"; else fail "Recipe invalid: ${f#$ROOT/}"; fi
  done < <(find "$ROOT/recipes" -type f -name '*.yaml' -print0)
else warn "Recipe validation deferred until Goose is installed"; fi
if [[ -n "${T4H_BAD_MCP_URI:-}" ]]; then pass "T4H_BAD_MCP_URI supplied"; else warn "bad-mcp transport not configured; not guessed"; fi
warn "bad-mcp authoritative scope registry is PARTIAL during control-plane migration"
warn "87 callable tools are inventory evidence, not proven grants"
echo "SUMMARY: PASS=$PASS WARN=$WARN FAIL=$FAIL"
if [[ $FAIL -eq 0 ]]; then echo "STATUS: READY WITH WARNINGS"; exit 0; else echo "STATUS: BLOCKED"; exit 1; fi
