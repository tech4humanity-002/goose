<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-start.yaml | Source SHA-256: acf1992b25ec8b922a4c7aa32cbd7ecf82d6f8ee4d7a1f6c764b87389254affe | -->
# T4H Start and Orient

Platform: `aider`  
Canonical workflow: `t4h-start`  
Contract version: `1.3.0`

## Parameters

- None

## Required stages

- None

## Operating instruction

Operate as a T4H Goose session. Read the project .goosehints and T4H operating rules. Inspect the current workspace and available tools. Treat callable bad-mcp tools as callable but not necessarily authorised because the current scope registry is PARTIAL. Report READY, READY WITH WARNINGS, or BLOCKED. Do not mutate infrastructure or external systems during orientation.

## Execution contract

- Maximum turns: 75
- Timeout: 300 seconds
- Maximum retries: 0
- Backoff: []
- Recovery: `report_blocked`
- Required outputs: readiness-status, blockers, warnings, structured-result

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
