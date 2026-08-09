# Microsoft Graph Integration

## Purpose

This integration enriches the local IAM decision engine with live Microsoft
Entra identity context.

### Read flow

```text
Request
  |
  v
GraphClient
  |
  +--> User profile
  +--> Group membership
  +--> Application assignments
  +--> Directory role assignments
  |
  v
Identity Context
  |
  v
Risk + Policy + AI
```

## Safe lab approach

1. Do not commit tokens, secrets, certificates or `.env` files.
2. Start with read-only Graph permissions.
3. Use a dedicated lab identity.
4. Validate all reads before enabling any write operation.
5. Keep write permissions separate from the read-only workflow.
6. Human approval remains mandatory.

`GRAPH_ACCESS_TOKEN` is expected as an environment variable for the Python
client. The repository intentionally contains no real token.
