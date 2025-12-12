// src/api/types.ts

export interface SupportCall {
  id: string;
  agent: string;
  issue_type: string;
  transcript: string;
  sentiment: string;
  tone: string;
  resolution_status: string;
  call_duration: number;
  summary?: string;
  frustration_score?: number;
  created_at: string;
}

export interface SummaryStats {
  total_calls: number;
  resolved_calls: number;
  unresolved_calls: number;
  average_duration: number;
  average_frustration: number;
}

export interface DistributionItem {
  label: string;
  count: number;
}

export interface Insight {
  call_id: string;
  risk_level: string;
  summary: string;
  recommended_action: string;
  frustration_score?: number;
}
