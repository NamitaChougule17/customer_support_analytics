from fastapi import APIRouter
from typing import List

from Backend.supabase_client import get_supabase_client
from Backend.models.call_model import (
    SentimentStat,
    ToneStat,
    IssueStat,
    SummaryStats,
)

router = APIRouter(prefix="/stats", tags=["stats"])

def _fetch_all_calls():
    supabase = get_supabase_client()
    resp = supabase.table("support_calls").select("*").execute()
    return resp.data or []

@router.get("/summary", response_model=SummaryStats)
def get_summary_stats():
    rows = _fetch_all_calls()

    total = len(rows)
    resolved = sum(r["resolution_status"] == "resolved" for r in rows)
    unresolved = total - resolved

    durations = [r["call_duration"] for r in rows if r.get("call_duration") is not None]
    avg_duration = sum(durations) / len(durations) if durations else 0.0

    fr = [r["frustration_score"] for r in rows if r.get("frustration_score") is not None]
    avg_frustration = sum(fr) / len(fr) if fr else 0.0

    return SummaryStats(
        total_calls=total,
        resolved_calls=resolved,
        unresolved_calls=unresolved,
        avg_duration=round(avg_duration, 2),
        avg_frustration=round(avg_frustration, 2),
    )

@router.get("/sentiment", response_model=List[SentimentStat])
def sentiment_stats():
    rows = _fetch_all_calls()
    counts = {}

    for r in rows:
        s = r.get("sentiment") or "unknown"
        counts[s] = counts.get(s, 0) + 1

    return [SentimentStat(sentiment=k, count=v) for k, v in counts.items()]

@router.get("/tone", response_model=List[ToneStat])
def tone_stats():
    rows = _fetch_all_calls()
    counts = {}

    for r in rows:
        t = r.get("tone") or "unknown"
        counts[t] = counts.get(t, 0) + 1

    return [ToneStat(tone=k, count=v) for k, v in counts.items()]

@router.get("/issues", response_model=List[IssueStat])
def issue_stats():
    rows = _fetch_all_calls()
    counts = {}

    for r in rows:
        issue = r.get("issue_type") or "unknown"
        counts[issue] = counts.get(issue, 0) + 1

    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    return [IssueStat(issue_type=k, count=v) for k, v in sorted_items]
