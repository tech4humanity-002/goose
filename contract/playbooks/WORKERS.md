# T4H Workers: Goose Scheduler vs T4H Worker Plane

There are two distinct concepts:

1. **Goose schedule**: `goose schedule add/list/run-now/remove` schedules a Goose recipe on the local Goose runtime.
2. **T4H worker plane**: `worker_list_schedules`, `worker_schedule`, `worker_status`, `worker_trigger` are bad-mcp capabilities and must be verified against the live T4H control plane.

Do not treat one as proof of the other.

For a local Goose scheduled recipe:

```bash
goose schedule add --schedule-id t4h-proof --cron "0 0 * * * *" --recipe-source ./recipes/evidence/t4h-proof.yaml
goose schedule list
goose schedule run-now --schedule-id t4h-proof
```

Use the T4H worker recipe when the requested workflow specifically targets the T4H worker control plane.
