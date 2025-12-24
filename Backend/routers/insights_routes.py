from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from Backend.supabase_client import get_supabase_client
from config import USE_AI

# Optional AI import (won't break backend if AI deps aren't installed)
try:
    from Backend.AI.ai_insights_generation import generate_insights_with_ai
except Exception:
    generate_insights_with_ai = None


router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/{call_id}")
def get_insights(call_id: str) -> Dict[str, Any]:
    supabase = get_supabase_client()

    resp = (
        supabase.table("support_calls")
        .select("*")
        .eq("id", call_id)
        .single()
        .execute()
    )

    call = resp.data
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    sentiment = (call.get("sentiment") or "").lower()
    tone = (call.get("tone") or "").lower()
    frustration = float(call.get("frustration_score") or 0.0)
    resolved = call.get("resolution_status") == "resolved"

    # Rule-based scoring (default)

    if frustration >= 0.7 or sentiment == "negative" or tone in {"angry", "frustrated"}:
        risk = "high"
    elif frustration >= 0.4 or sentiment == "neutral":
        risk = "medium"
    else:
        risk = "low"

    recommendation = "No action needed."
    if risk == "high":
        recommendation = "Escalate to senior support and send follow-up email."
    elif risk == "medium":
        recommendation = "Schedule follow-up check-in with the customer."

    if not resolved:
        recommendation += " Ensure the main issue is actually resolved."

    short_summary = call.get("summary") or "Customer support interaction."

    # AI override (optional)

    if USE_AI and generate_insights_with_ai:
        try:
            ai = generate_insights_with_ai(call)
            if isinstance(ai, dict):
                # Override only if AI actually returned values
                risk = ai.get("risk_level") or risk
                short_summary = ai.get("summary") or short_summary
                recommendation = ai.get("recommended_action") or recommendation
        except Exception:
            # If AI fails, keep rule-based output (do not break endpoint)
            pass


    return {
        "id": call_id,
        "risk_level": risk,
        "sentiment": sentiment,
        "tone": tone,
        "frustration_score": frustration,
        "resolved": resolved,
        "suggested_action": recommendation,
        "short_summary": short_summary,
    }
