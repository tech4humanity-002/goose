# Contract-led architecture

`contract/` owns all cross-platform behaviour. Platform adapters are compiled projections and may add configuration or declare capability gaps, but may not redefine the operating contract.

## Change flow

1. Modify a canonical workflow, policy, lifecycle, runtime rule or schema.
2. Validate the neutral contract.
3. Compile all adapters.
4. Run conformance and drift tests.
5. Publish the contract and generated adapters together.
6. Capture runtime-specific receipts when an adapter executes live.

## Boundaries

Canonical:

- Intent, parameters, stages and outcomes
- Authority, approval and safety requirements
- Idempotency, retries, timeout, recovery and quarantine
- Results, evidence and receipts
- Provider-neutral model capabilities and governed inference lifecycle

Adapter-specific:

- CLI invocation and native configuration
- Context-file and prompt representation
- Native/emulated/unsupported capability mappings
- Runtime installation and authentication
- Platform telemetry capture
- Provider SDK, authentication variable and dated mutable-fact references

Generated files are disposable. Deleting and recompiling them must reproduce the committed state exactly.
