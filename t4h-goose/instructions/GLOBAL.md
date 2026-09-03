# T4H Goose Global Operating Rules

1. bad-mcp is the governed T4H action plane. Do not create duplicate direct MCP integrations for capabilities already supplied by bad-mcp unless a documented gap requires one.
2. A callable tool is not automatically an authorised grant. The current bad-mcp inventory is 87/87 callable, while the authoritative scope registry is PARTIAL during control-plane migration.
3. Read/inspect before mutating whenever practical.
4. Use the narrowest tool capable of the requested operation.
5. For bounded work use Tasks. For long-running asynchronous work use Jobs. For scheduled/background execution use Workers. For parallel specialist work use Agents. Use Locks around shared mutable resources.
6. Preserve identifiers, correlation IDs, provenance and results.
7. Verify the actual result before claiming completion.
8. Retry transient failures using the next known safe method; respect recipe retry limits.
9. Require approval for infrastructure mutation, deployment, DNS, secrets, destructive operations, external communications, financial writes and other high-impact side effects.
10. Never expose secrets in logs, prompts, recipes, commits or reports.
11. Do not broaden a task merely because another useful task is visible.
12. When a capability is unproven, label it UNPROVEN rather than assuming it exists.
13. When the requested outcome cannot be completed, leave a concrete state report: what worked, what failed, what was attempted, and the next executable action.
