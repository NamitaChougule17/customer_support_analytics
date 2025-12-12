from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Call(BaseModel):
    id: str
    agent: Optional[str] = None
    issue_type: Optional[str] = None
    transcript: Optional[str] = None
    sentiment: Optional[str] = None
    tone: Optional[str] = None
    resolution_status: Optional[str] = None
    call_duration: Optional[int] = None
    summary: Optional[str] = None
    frustration_score: Optional[float] = None
    created_at: Optional[datetime] = None


class SentimentStat(BaseModel):
    sentiment: str
    count: int


class ToneStat(BaseModel):
    tone: str
    count: int


class IssueStat(BaseModel):
    issue_type: str
    count: int


class SummaryStats(BaseModel):
    total_calls: int
    resolved_calls: int
    unresolved_calls: int
    avg_duration: float
    avg_frustration: float
