# AI-Powered Identity Operations & JML Automation Platform

## Portfolio positioning

A security-controlled identity operations platform that combines Microsoft
Entra identity context, deterministic IAM policy evaluation, risk analysis,
AI-assisted recommendations, JML workflows and controlled automation.

**Primary implementation:** Microsoft Entra ID + Microsoft Graph + Python +
PowerShell.

**Supporting concepts:** IGA, JML, RBAC, least privilege, PIM, ITDR, ITSM,
human-in-the-loop approval.

> AI is advisory. The deterministic policy engine remains the authorization
> control. Identity-changing actions require human approval.

---

## 1. Business problem

Enterprise IAM teams frequently process access requests and JML events using
manual checks. This creates:
- excessive access accumulation
- inconsistent approvals
- delayed provisioning/deprovisioning
- weak audit evidence
- difficult identity investigations

This project demonstrates a controlled workflow that turns an identity request
into an explainable risk decision and a proposed action.

---

## 2. Architecture

```text
HR / IAM Request
      |
      v
Identity Context -----> Microsoft Graph / Entra
      |
      v
Access Analysis + Risk Analysis
      |
      v
AI Recommendation
      |
      v
Deterministic Policy Engine
      |
      +------ APPROVE
      +------ REVIEW
      +------ BLOCK
      |
      v
Human Approval
      |
      v
Controlled Graph / PowerShell Automation
      |
      v
Entra ID
      |
      v
Audit Evidence
```

---

## 3. Security controls

- Least privilege
- Fail-closed behavior for unknown applications
- Separation of AI recommendation from authorization
- Human-in-the-loop approval
- Explicit privileged-access blocking
- Read-only Graph enrichment before write automation
- Dry-run default for PowerShell actions
- No secrets in source control
- Structured JSON decisions for auditability

---

## 4. JML use cases

### Joiner
Validate the employee, derive baseline access, request approval, then provision
only approved entitlements.

### Mover
Compare old and new business context, identify stale access, remove
unnecessary entitlements and grant approved new access.

### Leaver
Confirm termination, disable identity/revoke sessions through an approved
workflow, remove access and record evidence.

---

## 5. Identity security use cases

### Access request
Department + application + approval + existing entitlements -> policy decision.

### Excessive access
Detect high group/application counts and privileged roles.

### Identity incident
Use suspicious sign-in / privilege signals as investigation context.

### Access review
Use existing entitlements and business context to recommend KEEP/REMOVE/REVIEW.

---

## 6. Repository structure

```text
ai/                    AI prompts and decision schema
architecture/           Architecture, threat model and portfolio diagrams
automation/             Graph client and PowerShell workflows
data/                   Synthetic lab data
engine/                 Policy, context, access and risk engines
reports/                Generated evidence
scenarios/              JML and identity-risk scenarios
tests/                  Automated tests
run_platform.py         End-to-end offline runner
```

---

## 7. Run the project locally

Python 3.10+ recommended.

```powershell
python run_platform.py
```

Run unit tests:

```powershell
python -m unittest discover -s tests -v
```

Run the policy engine directly:

```powershell
python engine\policy_engine.py
```

No external API key is required for the offline mode.

---

## 8. Microsoft Graph mode

The Graph client is intentionally separated from the local decision engine.

Use a lab token only through an environment variable:

```powershell
$env:GRAPH_ACCESS_TOKEN="..."
```

Then use `automation/graph/graph_client.py`.

Start with read-only identity enrichment. Do not grant broad write permissions
until the complete workflow has been validated.

---

## 9. AI mode

Without an LLM configuration, the project uses a deterministic fallback so the
demo remains reproducible.

Optional provider configuration:

```text
LLM_API_URL=
LLM_API_KEY=
LLM_MODEL=
```

The AI output must remain structured and cannot override the policy engine.

---

## 10. Interview explanation

### 30-second answer

> "I designed an AI-assisted identity operations platform around Microsoft
> Entra ID. It enriches access requests with identity context, analyzes current
> entitlements and risk, produces an explainable AI recommendation, and then
> passes the recommendation through a deterministic policy engine. Only after
> human approval can a controlled Graph or PowerShell workflow make an identity
> change. I deliberately separated AI from authorization so the system follows
> least privilege, fail-closed behavior and auditability."

### Why not let AI directly provision access?

> "Because an LLM is probabilistic. Authorization needs deterministic controls.
> I use AI for analysis and recommendations, while the policy engine and human
> approval remain the security boundary."

---

## 11. Portfolio evidence to capture

Capture:
1. Architecture diagram
2. Entra lab configuration
3. Graph read result
4. Access request input
5. Policy decision
6. AI recommendation
7. Human approval state
8. JML Joiner/Mover/Leaver runs
9. Excessive-access detection
10. Audit report
11. Automated test results
12. GitHub repository structure

Do not publish real tenant IDs, UPNs, tokens, certificates or company data.
Use synthetic lab identities.

---

## 12. Limitations

This repository contains a safe, offline-first implementation. Live Entra
writes and an external LLM are intentionally not enabled by default. The
production version would add stronger secrets management, approval/ITSM
integration, centralized logging, retry/idempotency controls and formal
access-governance workflows.
