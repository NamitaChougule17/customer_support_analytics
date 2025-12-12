from fastapi import APIRouter, HTTPException
from typing import List

from Backend.supabase_client import get_supabase_client
from Backend.models.call_model import Call

router = APIRouter(prefix="/calls", tags=["calls"])

@router.get("/", response_model=List[Call])
def list_calls(limit: int = 50, offset: int = 0):
    supabase = get_supabase_client()
    resp = (
        supabase.table("support_calls")
        .select("*")
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return resp.data or []

@router.get("/{call_id}", response_model=Call)
def get_call(call_id: str):
    supabase = get_supabase_client()
    resp = (
        supabase.table("support_calls")
        .select("*")
        .eq("id", call_id)
        .single()
        .execute()
    )
    if not resp.data:
        raise HTTPException(status_code=404, detail="Call not found")

    return resp.data
