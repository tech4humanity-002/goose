<!-- GENERATED FILE — DO NOT EDIT | Source: contract/workflows/t4h-recipe-review-worker.yaml | Source SHA-256: d124320b3fd303a87035c6d95d4b45b4696a3e3e4daf61097658ba9b6da6b5d9 | -->
# T4H Recipe Review Worker

Platform: `gemini-cli`  
Canonical workflow: `t4h-recipe-review-worker`  
Contract version: `1.4.0`

## Parameters

- `review_date` (required): Current review date in YYYY-MM-DD format.

## Required stages

- None

## Operating instruction

Run the T4H recipe review process for {{ review_date }}.

1. Read registry/recipe-index.yaml.
2. Identify recipes where review_due <= {{ review_date }} or status is OVERDUE.
3. Validate each due recipe using the Goose recipe validation command where available.
4. Inspect referenced subrecipes and confirm every referenced path exists.
5. Check required resources/extensions and known limitations.
6. Produce a review report listing PASS, WARN, BLOCKED and OVERDUE items.
7. If the T4H worker plane is available, record the review job/result and correlation identifier.
8. Do not silently modify recipes or extend review dates merely to clear a warning.

The authoritative scope registry remains PARTIAL; do not interpret callable bad-mcp tools as proven grants.

## Execution contract

- Maximum turns: 80
- Timeout: 300 seconds
- Maximum retries: 0
- Backoff: []
- Recovery: `report_blocked`
- Required outputs: review-report, overdue-list, validation-results, structured-result

Return a result conforming to `contract/schemas/result.schema.json` and preserve evidence required by `contract/schemas/receipt.schema.json`.
