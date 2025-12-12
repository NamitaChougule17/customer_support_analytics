from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from Backend.supabase_client import get_supabase_client

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
    frustration = call.get("frustration_score") or 0.0
    resolved = call.get("resolution_status") == "resolved"

    # --- Rule-based scoring ---
    if frustration >= 0.7 or sentiment == "negative" or tone in {"angry", "frustrated"}:
        risk = "high"
    elif frustration >= 0.4 or sentiment == "neutral":
        risk = "medium"
    else:
        risk = "low"

    # --- Recommendation ---
    recommendation = "No action needed."
    if risk == "high":
        recommendation = "Escalate to senior support and send follow-up email."
    elif risk == "medium":
        recommendation = "Schedule follow-up check-in with the customer."

    if not resolved:
        recommendation += " Ensure the main issue is actually resolved."

    return {
        "id": call_id,
        "risk_level": risk,
        "sentiment": sentiment,
        "tone": tone,
        "frustration_score": frustration,
        "resolved": resolved,
        "suggested_action": recommendation,
        "short_summary": call.get("summary") or "Customer support interaction.",
    }
