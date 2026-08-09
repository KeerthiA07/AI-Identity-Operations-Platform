# Security Notes

This is a portfolio/lab implementation.

## Never commit
- access tokens
- client secrets
- certificates/private keys
- production UPNs
- tenant IDs if they expose your environment
- company/customer data

## Production hardening that would be required
- managed identity/workload identity instead of long-lived secrets
- Key Vault or equivalent secrets management
- separate read/write applications
- approval/ITSM integration
- idempotent Graph operations
- retry and throttling handling
- centralized audit logging
- SIEM integration
- stronger schema validation
- formal access review and SoD rules
- RBAC/PIM for the automation identity
- monitoring and alerting
