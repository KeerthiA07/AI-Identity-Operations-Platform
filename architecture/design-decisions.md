# Key Design Decisions

## 1. AI is not the authorization authority
LLMs are probabilistic. The deterministic policy engine is the security gate.

## 2. Fail closed
Unknown applications and unresolved policy conditions are reviewed rather than
automatically approved.

## 3. Human-in-the-loop
Every identity-changing action requires approval in the demo workflow.

## 4. Read before write
The system enriches identity context before any proposed action.

## 5. Offline-first
The repository can be demonstrated without credentials or paid APIs.

## 6. Vendor-specific integration is isolated
Entra/Graph code sits under `automation/graph`, allowing the core policy logic
to remain vendor-neutral.
