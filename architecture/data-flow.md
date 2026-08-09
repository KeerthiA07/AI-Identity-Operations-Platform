# Data Flow

1. Request enters as JSON/ITSM event.
2. Identity context is loaded from Entra or synthetic fixture.
3. Access analyzer evaluates existing entitlements.
4. Risk engine calculates deterministic risk signals.
5. AI generates a structured recommendation.
6. Policy engine validates the request and determines the allowed state.
7. Human approval is required for identity-changing operations.
8. Graph/PowerShell executes only approved actions.
9. Result is written to an evidence report.
