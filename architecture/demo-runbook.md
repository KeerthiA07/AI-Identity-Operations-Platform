# Demo Runbook

## Baseline

```powershell
python run_platform.py
```

Expected: LOW risk, policy APPROVE, execution remains PENDING_HUMAN_APPROVAL.

## JML

```powershell
python run_scenario.py joiner
python run_scenario.py mover
python run_scenario.py leaver
```

## Identity risk

```powershell
python run_scenario.py excessive_access
python run_scenario.py suspicious_signin
```

## Automated tests

```powershell
python -m unittest discover -s tests -v
```

## Portfolio screenshots

Capture the terminal output for:
1. Baseline access request
2. HR -> Finance mismatch
3. Missing approval
4. Privileged access block
5. Excessive access
6. Suspicious sign-in
7. JML mover
8. JML leaver
9. Unit tests
10. Architecture diagram

Blur/replace any real tenant identifiers before publishing.
