# Threat Model

| Threat | Control |
|---|---|
| Prompt injection | AI output cannot bypass deterministic policy |
| Excessive privilege | Privileged access is blocked/escalated |
| Unknown application | Fail-closed review |
| Stolen token | No tokens in source; short-lived lab credentials |
| Unauthorized automation | Human approval required |
| Over-provisioning | Department/application policy |
| Access accumulation | Entitlement analysis |
| AI hallucination | Structured output + policy validation |
| Secret leakage | `.env` and tokens excluded from Git |
| Unsafe writes | PowerShell defaults to dry-run |

## Security principle

The AI layer is treated as an untrusted decision-support component, not an
identity authority.
