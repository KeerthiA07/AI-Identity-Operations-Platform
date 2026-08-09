"""AI-assisted identity analysis.

Default mode is offline and deterministic so the project is runnable without
an API key. An external LLM can be enabled through environment variables.
The LLM is never the final authorization authority.
"""
from __future__ import annotations
import json
import os
from urllib import request as urlrequest


SYSTEM_PROMPT = """You are an IAM security analyst.
Analyze identity access requests using least privilege, separation of duties,
JML context, existing entitlements and risk signals.
Return JSON only with:
decision, risk, confidence, reasons, recommended_action, requires_human_approval.
Never recommend bypassing policy or granting privileged access automatically.
"""


def deterministic_analysis(request_data: dict, identity: dict, policy: dict, risk: dict) -> dict:
    reasons = []
    reasons.extend(policy.get("reasons", []))
    reasons.extend(risk.get("signals", []))

    if policy["decision"] == "APPROVE":
        recommendation = "Access aligns with the identity's business context and policy."
    elif policy["decision"] == "REVIEW":
        recommendation = "Access requires human review because one or more policy conditions are unresolved."
    else:
        recommendation = "Access should not be automatically granted because the request presents a high-risk or privileged condition."

    confidence = 0.96 if policy["decision"] != "REVIEW" else 0.90
    return {
        "decision": policy["decision"],
        "risk": policy["risk"],
        "confidence": confidence,
        "reasons": reasons,
        "recommended_action": policy["recommended_action"],
        "summary": recommendation,
        "requires_human_approval": True,
        "provider": "deterministic-fallback",
    }


def analyze(request_data: dict, identity: dict, policy: dict, risk: dict) -> dict:
    """Use optional LLM provider; otherwise use safe deterministic fallback."""
    api_url = os.getenv("LLM_API_URL")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "identity-security-model")

    if not api_url or not api_key:
        return deterministic_analysis(request_data, identity, policy, risk)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps({
                "request": request_data,
                "identity": identity,
                "policy_decision": policy,
                "risk": risk,
            })},
        ],
        "temperature": 0,
    }

    req = urlrequest.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urlrequest.urlopen(req, timeout=20) as response:
            raw = json.loads(response.read().decode("utf-8"))
        # Provider-specific extraction is intentionally isolated here.
        content = raw["choices"][0]["message"]["content"]
        result = json.loads(content)
        result["requires_human_approval"] = True
        result["provider"] = "external-llm"
        return result
    except Exception as exc:
        fallback = deterministic_analysis(request_data, identity, policy, risk)
        fallback["llm_error"] = str(exc)
        return fallback
