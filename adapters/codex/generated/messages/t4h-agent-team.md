<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-agent-team.yaml | Source SHA-256: 73d970e6f350e6f16505dbe05dba0c99f80814355b9c94f41e05b889fd9f8dd6 | -->
# T4H Agent Team

Platform: `codex`  
Canonical workflow: `t4h-agent-team`  
Contract version: `1.4.0`

## Parameters

- `objective` (required): Objective for the specialist agent team.
- `idempotency_key` (optional): Stable delegation replay-protection key.

## Required stages

- None

## Operating instruction

Coordinate specialist agents for: {{ objective }}. Derive or record an idempotency key and inspect active equivalent work before spawning. Determine whether delegation adds value. If agent tools are live and authorised, discover suitable agents, spawn only the minimum required specialists, communicate explicit objectives, collect results, and reconcile them within the timeout and budget. Use consensus only for a real multi-agent decision. Preserve agent IDs and correlation IDs. Reap or quarantine timed-out agents when supported and name a recovery owner otherwise. Never claim success merely because agents were spawned. Emit structured result and receipt records.

## Execution contract

- Maximum turns: 75
- Timeout: 900 seconds
- Maximum retries: 1
- Backoff: [10]
- Recovery: `terminate_or_quarantine_agents`
- Required outputs: agent-ids, consensus, proof, structured-result, receipt

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
