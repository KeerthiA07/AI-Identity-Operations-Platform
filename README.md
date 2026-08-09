# AI-Powered Identity Security Operations Platform

> An identity-security decision and automation platform built around Microsoft Entra ID that combines identity context, entitlement analysis, deterministic policy evaluation, risk detection, AI-assisted recommendations, JML workflows, and human-controlled automation.

![Microsoft Entra ID](https://img.shields.io/badge/Microsoft%20Entra%20ID-Identity%20Security-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PowerShell](https://img.shields.io/badge/PowerShell-Automation-blue)
![Microsoft Graph](https://img.shields.io/badge/Microsoft%20Graph-API-blue)
![Tests](https://img.shields.io/badge/Tests-10%2F10-success)

---

## Why I built this

Traditional IAM operations often require analysts to manually correlate:

- user identity information
- department and job role
- existing groups and entitlements
- privileged roles
- requested application access
- approval status
- suspicious identity activity

This creates opportunities for excessive access, inconsistent decisions,
slow JML processing and weak auditability.

This project demonstrates how those signals can be combined into a controlled
identity-security decision pipeline.

---

# Core idea

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
       +----------------+
       |                |
       v                v
Policy Engine       AI Analysis
       |                |
       +-------+--------+
               |
               v
       Security Decision
               |
       +-------+-------+
       |       |       |
     APPROVE REVIEW  BLOCK
               |
               v
       Human Approval
               |
               v
    Controlled Automation
               |
               v
        Entra ID / Graph
Security design principle

AI is advisory. It does not authorize identity changes.

The deterministic policy engine remains the authorization control.

Identity-changing actions require human approval.

This prevents a probabilistic AI component from becoming the security boundary.

What the platform can detect
1. Normal access request

Example:

User Department : Finance
Application     : LAB-APP-FINANCE
Access Level    : Standard
Manager Approval: Present

Result:

Decision   : APPROVE
Risk       : LOW
Risk Score : 0
Action     : GRANT_APPLICATION_ACCESS
2. Department/application mismatch

Example:

User Department : Finance
Application     : LAB-APP-HR

Result:

Decision   : REVIEW
Risk       : MEDIUM
Risk Score : 40
Action     : PERFORM_ACCESS_REVIEW

Reason:

User department 'Finance' does not match application department 'HR'.
Application is classified as high sensitivity.

This demonstrates business-context-aware access control rather than simply
checking whether a user requested access.

3. Excessive access

The platform can identify combinations such as:

Privileged directory role
        +
Existing application access
        +
Cross-department entitlements

Example result:

Decision   : REVIEW
Risk       : HIGH
Risk Score : 50
Action     : PERFORM_ACCESS_REVIEW

The access-review engine can classify entitlements as:

KEEP
REVIEW

based on identity and business context.

4. Identity threat detection context

The ITDR scenario combines signals such as:

Impossible travel
Multiple failed sign-ins
Unexpected privileged activation

Example:

Risk Score : 90
Risk Level : CRITICAL

Recommended investigation includes reviewing:

privileged role activation
sign-in locations
authentication failures
authentication methods
possible session revocation
JML automation

The platform includes Joiner, Mover and Leaver scenarios.

Joiner
Employee joins
     ↓
Validate identity
     ↓
Determine baseline access
     ↓
Human approval
     ↓
Provision approved access
Mover
Department changes
     ↓
Compare previous/current context
     ↓
Identify stale entitlements
     ↓
Review removal/addition
     ↓
Human approval
Leaver
Termination
     ↓
Confirm identity
     ↓
Disable/revoke workflow
     ↓
Human approval
     ↓
Record evidence
Real Microsoft Entra ID integration

The platform was tested against a Microsoft Entra lab tenant using Microsoft Graph.

The real identity context included:

User:
LAB-USER-FIN01

Department:
Finance

Job Title:
Finance Analyst

Groups:
LAB-SG-FINANCE
LAB-DG-FINANCE-USERS
LAB-SG-CA-PILOT

Administrative Unit:
LAB-AU-BANGALORE

The identity context is normalized before being passed to the security
decision pipeline.

The live integration is intentionally read-oriented and separated from the
decision engine.

Security architecture

The platform follows several security principles:

Least privilege
Fail-closed behavior
Human-in-the-loop approval
Separation of AI recommendation and authorization
Privileged-access detection
Read-only identity enrichment before write automation
Dry-run automation by default
Structured decision records
No secrets committed to source control
Technology stack
Area	Technology
Identity	Microsoft Entra ID
Identity API	Microsoft Graph
Core engine	Python
Automation	PowerShell
AI layer	Structured AI analysis + deterministic fallback
IAM	IAM / IGA / JML
Security	Least Privilege / PIM / ITDR concepts
Testing	Python unittest
Version control	Git / GitHub
Project architecture
ai/
    AI analysis, prompts and decision schema

architecture/
    System architecture
    Data flow
    Threat model
    Design decisions
    Demo runbook
    Portfolio case study

automation/
    Microsoft Graph automation
    PowerShell JML workflows

engine/
    Identity context
    Access analysis
    Risk analysis
    Policy engine
    JML engine
    ITDR engine
    Access review

integrations/
    Microsoft Entra integration
    Graph client
    Identity normalization
    Real-tenant runners

scenarios/
    Joiner
    Mover
    Leaver
    Excessive access
    Suspicious sign-in

tests/
    Policy tests
    Scenario tests
    End-to-end tests
Validation

The automated test suite currently validates:

10 tests
10 passed
0 failed

Validated scenarios include:

Valid Finance access request
Department mismatch
Missing manager approval
Privileged request
Unknown application
End-to-end offline pipeline
ITDR high-risk scenario
Joiner
Mover
Leaver

Run:

python -m unittest discover -s tests -v
Running the platform
Offline mode

No external API or LLM is required.

python run_platform.py
Scenario testing
python run_scenario.py joiner
python run_scenario.py mover
python run_scenario.py leaver
python run_scenario.py excessive_access
python run_scenario.py suspicious_signin
Microsoft Entra mode

The live identity pipeline can collect and normalize identity context from
Microsoft Entra ID through Microsoft Graph.

Example:

python integrations\entra\run_real_platform.py USER_UPN

Example application test:

python integrations\entra\run_real_platform.py USER_UPN LAB-APP-HR
AI security model

The AI layer is deliberately constrained.

Identity Context
      ↓
Security Analysis
      ↓
AI Recommendation
      ↓
Deterministic Policy Engine
      ↓
Human Approval
      ↓
Automation

The AI component can recommend:

decision
risk level
reasoning
recommended action
investigation guidance

It cannot independently authorize an identity change.

If the AI provider is unavailable, the platform uses a deterministic fallback so
the security workflow remains reproducible.

Threat model considerations

The architecture considers risks including:

excessive privilege
privilege accumulation
unauthorized application access
suspicious sign-ins
AI recommendation misuse
accidental identity modification
credential exposure
over-permissioned automation

The project intentionally separates:

Analysis
   ≠
Authorization
   ≠
Execution

This separation is a core security control.

Important limitations

This is a portfolio/lab implementation, not a production IAM platform.

Production deployment would require additional controls such as:

enterprise secrets management
centralized logging/SIEM integration
ITSM approval integration
stronger authorization boundaries
retry and idempotency controls
production-grade identity governance
formal access certification workflows
comprehensive monitoring and alerting

Live identity-changing operations are intentionally not enabled by default.

Portfolio value

This project demonstrates practical experience across:

Identity Security

Microsoft Entra ID
IAM
IGA concepts
JML
RBAC
Least Privilege
Privileged access
ITDR

Security Engineering

Policy-as-code
Risk scoring
Security decision pipelines
Fail-closed design
Human approval controls
Auditability

Automation

Microsoft Graph
Python
PowerShell
Structured JSON workflows

AI Security

AI-assisted analysis
Deterministic authorization
Human-in-the-loop AI
AI failure fallback
30-second interview explanation

I built an AI-assisted identity security operations platform around Microsoft Entra ID. It collects real identity context through Microsoft Graph, analyzes existing entitlements and requested access, evaluates risk and business policy, and produces an explainable security decision. AI is used only for analysis and recommendation; authorization remains deterministic and identity-changing actions require human approval. I also implemented JML, excessive-access and ITDR scenarios and validated the platform with automated tests.

Security note

Never commit:

.env
access tokens
client secrets
API keys
certificates
real employee identities
production tenant information

Use synthetic lab identities and environment variables for credentials.


## Step 2 — Save it

Open:

```text
README.md