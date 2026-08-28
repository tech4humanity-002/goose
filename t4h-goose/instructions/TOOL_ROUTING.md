# T4H Goose Tool Routing

- Local code/files: Goose Developer + filesystem tools.
- Git/local repository: Git tooling.
- Remote repository/GitHub: bad-mcp Git/GitHub tools where available.
- T4H infrastructure/cloud: bad-mcp AWS/infrastructure/deployment tools.
- Long-running execution: job_create/job_get/job_list/job_result.
- Bounded owned work: task_create/task_claim/task_complete.
- Background/scheduled work: worker_list_schedules/worker_schedule/worker_status/worker_trigger.
- Parallel specialist work: agent_list/agent_spawn/agent_message/agent_inbox/agent_consensus.
- Shared mutable resources: lock_acquire/lock_release.
- Evidence and verification: check_* and run_mission_proof.
- Persistent graph knowledge: memory/OIKOS.

The catalogue is not the live capability boundary. Callable bad-mcp tools are not proven grants while the authoritative scope registry is PARTIAL.
