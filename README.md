# AI-Powered Identity Security Operations Platform

> An identity-security decision and automation platform built around Microsoft Entra ID that combines identity context, entitlement analysis, deterministic policy evaluation, risk detection, AI-assisted recommendations, JML workflows, and human-controlled automation.

---

## 1. Why I Built This

Traditional IAM operations often require analysts to manually correlate:

- User identity and business context
- Department and job role
- Existing groups and entitlements
- Privileged directory roles
- Requested application access
- Manager approval
- Suspicious identity activity

This can lead to excessive access, inconsistent decisions, slow JML processing, and weak auditability.

This project demonstrates a controlled identity-security pipeline that combines these signals into an explainable security decision.

---

## 2. Core Architecture

```text
                    Microsoft Entra ID
                           |
                           v
                  Identity Context
                           |
                           v
                 Entitlement Analysis
                           |
                           v
                     Risk Analysis
                           |
                 +---------+---------+
                 |                   |
                 v                   v
           Policy Engine         AI Analysis
                 |                   |
                 +---------+---------+
                           |
                           v
                  Security Decision
                           |
              +------------+------------+
              |            |            |
           APPROVE       REVIEW       BLOCK
                           |
                           v
                   Human Approval
                           |
                           v
                Controlled Automation
                           |
                           v
                    Entra ID / Graph
```

### Security Design Principle

**AI is advisory. It does not authorize identity changes.**

The deterministic policy engine remains the authorization control, while identity-changing actions require human approval.

---

# 3. What the Platform Can Detect

## 3.1 Normal Access Request

Example:

```text
User Department  : Finance
Application      : LAB-APP-FINANCE
Access Level     : Standard
Manager Approval : Present
```

Result:

```text
Decision   : APPROVE
Risk       : LOW
Risk Score : 0
Action     : GRANT_APPLICATION_ACCESS
```

## 3.2 Department / Application Mismatch

Example:

```text
User Department : Finance
Application     : LAB-APP-HR
```

Result:

```text
Decision   : REVIEW
Risk       : MEDIUM
Risk Score : 40
Action     : PERFORM_ACCESS_REVIEW
```

Reason:

> User department `Finance` does not match application department `HR`.

The application is also classified as high sensitivity.

## 3.3 Excessive Access

The platform detects combinations such as:

```text
Privileged Directory Role
          +
Existing Application Access
          +
Cross-Department Entitlements
```

Example result:

```text
Decision   : REVIEW
Risk       : HIGH
Risk Score : 50
Action     : PERFORM_ACCESS_REVIEW
```

The access-review engine can classify entitlements as:

- `KEEP`
- `REVIEW`

## 3.4 Identity Threat Detection Context

The ITDR scenario combines:

- Impossible travel
- Multiple failed sign-ins
- Unexpected privileged activation

Example:

```text
Risk Score : 90
Risk Level : CRITICAL
```

Recommended investigation areas include:

- Privileged role activation
- Sign-in locations
- Authentication failures
- Authentication methods
- Possible session revocation

---

# 4. JML Automation

The platform includes **Joiner, Mover, and Leaver** scenarios.

### Joiner

```text
Employee joins
     |
     v
Validate identity
     |
     v
Determine baseline access
     |
     v
Human approval
     |
     v
Provision approved access
```

### Mover

```text
Department changes
     |
     v
Compare previous/current context
     |
     v
Identify stale entitlements
     |
     v
Review removal/addition
     |
     v
Human approval
```

### Leaver

```text
Termination
     |
     v
Confirm identity
     |
     v
Disable / revoke workflow
     |
     v
Human approval
     |
     v
Record evidence
```

---

# 5. Real Microsoft Entra ID Integration

The platform was tested against a **Microsoft Entra lab tenant using Microsoft Graph**.

The real identity context included a synthetic lab identity with:

```text
Department : Finance
Job Title  : Finance Analyst
```

Example lab entitlements:

```text
LAB-SG-FINANCE
LAB-DG-FINANCE-USERS
LAB-SG-CA-PILOT
```

Administrative Unit:

```text
LAB-AU-BANGALORE
```

The identity context is normalized before being passed to the security decision pipeline.

The live integration is intentionally read-oriented and separated from the decision engine.

> Real tenant identifiers, tokens, credentials, and personal/company data should not be published.

---

# 6. Security Architecture

| Control | Implementation |
|---|---|
| Least privilege | Business context and existing entitlements are evaluated |
| Fail-closed | Unknown applications are not automatically approved |
| Human-in-the-loop | Identity-changing actions require approval |
| AI separation | AI recommendations cannot authorize access |
| Privileged-access detection | Existing privileged roles increase risk |
| Read-first design | Entra enrichment is separated from write automation |
| Dry-run automation | PowerShell workflows default to safe execution |
| Auditability | Decisions are represented as structured JSON |
| Secret protection | Credentials are excluded from source control |

---

# 7. Technology Stack

| Area | Technology |
|---|---|
| Identity | Microsoft Entra ID |
| Identity API | Microsoft Graph |
| Core Engine | Python |
| Automation | PowerShell |
| AI Layer | Structured AI analysis + deterministic fallback |
| IAM | IAM / IGA / JML |
| Security | Least Privilege / PIM / ITDR concepts |
| Testing | Python `unittest` |
| Version Control | Git / GitHub |

---

# 8. Project Structure

```text
AI-Identity-Operations-Platform/
|
+-- ai/
|   +-- AI analysis
|   +-- prompts
|   +-- decision schema
|
+-- architecture/
|   +-- system architecture
|   +-- data flow
|   +-- threat model
|   +-- design decisions
|   +-- demo runbook
|   +-- portfolio case study
|
+-- automation/
|   +-- Microsoft Graph automation
|   +-- PowerShell JML workflows
|
+-- engine/
|   +-- identity context
|   +-- access analysis
|   +-- risk analysis
|   +-- policy engine
|   +-- JML engine
|   +-- ITDR engine
|   +-- access review
|
+-- integrations/
|   +-- Microsoft Entra integration
|   +-- Graph client
|   +-- identity normalization
|   +-- real-tenant runners
|
+-- scenarios/
|   +-- Joiner
|   +-- Mover
|   +-- Leaver
|   +-- Excessive access
|   +-- Suspicious sign-in
|
+-- tests/
|   +-- policy tests
|   +-- scenario tests
|   +-- end-to-end tests
|
+-- run_platform.py
+-- run_scenario.py
+-- README.md
```

---

# 9. Validation

The automated test suite validates the core security workflow.

Current validation:

```text
10 tests
10 passed
0 failed
```

Validated scenarios include:

- Valid Finance access request
- Department mismatch
- Missing manager approval
- Privileged request
- Unknown application
- End-to-end offline pipeline
- ITDR high-risk scenario
- Joiner
- Mover
- Leaver

Run:

```powershell
python -m unittest discover -s tests -v
```

---

# 10. Running the Platform

## Offline Mode

No external API or LLM is required.

```powershell
python run_platform.py
```

## Scenario Testing

```powershell
python run_scenario.py joiner
python run_scenario.py mover
python run_scenario.py leaver
python run_scenario.py excessive_access
python run_scenario.py suspicious_signin
```

## Microsoft Entra Mode

The live identity pipeline collects and normalizes identity context from Microsoft Entra ID through Microsoft Graph.

```powershell
python integrations\entra\run_real_platform.py USER_UPN
```

Test a specific application:

```powershell
python integrations\entra\run_real_platform.py USER_UPN LAB-APP-HR
```

---

# 11. AI Security Model

The AI layer is deliberately constrained.

```text
Identity Context
       |
       v
Security Analysis
       |
       v
AI Recommendation
       |
       v
Deterministic Policy Engine
       |
       v
Human Approval
       |
       v
Automation
```

The AI component can recommend:

- Decision
- Risk level
- Reasoning
- Recommended action
- Investigation guidance

It **cannot independently authorize an identity change**.

If the AI provider is unavailable, the platform uses a deterministic fallback so the workflow remains reproducible.

---

# 12. Threat Model

The architecture considers:

- Excessive privilege
- Privilege accumulation
- Unauthorized application access
- Suspicious sign-ins
- AI recommendation misuse
- Accidental identity modification
- Credential exposure
- Over-permissioned automation

A core design separation is:

```text
Analysis
   !=
Authorization
   !=
Execution
```

This separation is a primary security control.

---

# 13. Production Limitations

This is a **portfolio/lab implementation**, not a production IAM platform.

A production deployment would require:

- Enterprise secrets management
- Centralized logging and SIEM integration
- ITSM approval integration
- Stronger authorization boundaries
- Retry and idempotency controls
- Production-grade identity governance
- Formal access certification workflows
- Comprehensive monitoring and alerting

Live identity-changing operations are intentionally not enabled by default.

---

# 14. Portfolio Value

### Identity Security

- Microsoft Entra ID
- IAM
- IGA concepts
- JML
- RBAC
- Least privilege
- Privileged access
- ITDR

### Security Engineering

- Policy-as-code
- Risk scoring
- Security decision pipelines
- Fail-closed design
- Human approval controls
- Auditability

### Automation

- Microsoft Graph
- Python
- PowerShell
- Structured JSON workflows

### AI Security

- AI-assisted security analysis
- Deterministic authorization
- Human-in-the-loop AI
- AI failure fallback

---

# 15. 30-Second Interview Explanation

> I built an AI-assisted identity security operations platform around Microsoft Entra ID. It collects identity context through Microsoft Graph, analyzes existing entitlements and requested access, evaluates risk and business policy, and produces an explainable security decision. AI is used only for analysis and recommendation; authorization remains deterministic, and identity-changing actions require human approval. I also implemented JML, excessive-access, access-review, and ITDR scenarios and validated the platform with automated tests.

### Why Not Let AI Provision Access Directly?

> An LLM is probabilistic, while authorization needs deterministic controls. I therefore use AI for analysis and recommendations, while the policy engine and human approval remain the security boundary.

---

# 16. Portfolio Evidence

Capture:

1. Architecture diagram
2. Entra lab configuration
3. Microsoft Graph read result
4. Access request input
5. Policy decision
6. AI recommendation
7. Human approval state
8. Joiner/Mover/Leaver runs
9. Excessive-access detection
10. Audit report
11. Automated test results
12. GitHub repository structure

Use synthetic lab identities in screenshots.

Do not publish:

- Real tenant IDs
- Access tokens
- Client secrets
- API keys
- Certificates
- Real employee identities
- Production tenant information
- Company-confidential data

---

# 17. Security Notes

Never commit:

```text
.env
Access tokens
Client secrets
API keys
Certificates
Production identity data
Company-confidential information
```

Use environment variables or a proper secrets-management solution for credentials.

---

# 18. Project Status

| Capability | Status |
|---|---|
| Offline policy engine | Complete |
| Risk analysis | Complete |
| AI recommendation | Complete |
| JML scenarios | Complete |
| ITDR scenario | Complete |
| Excessive-access detection | Complete |
| Microsoft Entra read integration | Complete |
| Identity normalization | Complete |
| Automated tests | Complete |
| GitHub repository | Complete |
| Live identity-changing automation | Intentionally disabled |

---

# 19. Next Development Phase

Planned improvements:

- GitHub Actions CI/CD
- Structured audit evidence
- Approval workflow simulation
- ITSM integration
- Centralized security logging
- Stronger production authorization controls
- Idempotent automation

---

## Core Security Principle

```text
Real Entra Identity Context
          |
          v
Identity / Entitlement Analysis
          |
          v
Risk + Policy Evaluation
          |
          v
AI-Assisted Security Recommendation
          |
          v
Human Approval
          |
          v
Controlled Automation
          |
          v
Audit Evidence
```

The key differentiator is the separation of **analysis, authorization, and execution**.
