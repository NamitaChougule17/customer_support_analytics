// src/api/client.ts
import axios from "axios";
import type {
  SupportCall,
  SummaryStats,
  DistributionItem,
  Insight,
} from "./types";

// Use /api prefix for Vercel deployment, or custom URL for development
const getBaseURL = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  // In production (Vercel), use /api prefix
  if (import.meta.env.PROD) {
    return "/api";
  }
  // In development, use local backend
  return "http://127.0.0.1:8000";
};

const api = axios.create({
  baseURL: getBaseURL(),
});

// ---------------- CALLS ----------------

export async function getCalls(): Promise<SupportCall[]> {
  const res = await api.get<SupportCall[]>("/calls/");
  return res.data;
}

export async function getCallById(id: string): Promise<SupportCall> {
  const res = await api.get<SupportCall>(`/calls/${id}`);
  return res.data;
}

// ---------------- SUMMARY ----------------

export async function getSummaryStats(): Promise<SummaryStats> {
  const res = await api.get<SummaryStats>("/stats/summary");
  return res.data;
}

// ---------------- DISTRIBUTIONS ----------------

export async function getSentimentStats(): Promise<DistributionItem[]> {
  const res = await api.get<any[]>("/stats/sentiment");
  return res.data.map(item => ({
    label: item.sentiment,
    count: item.count,
  }));
}

export async function getToneStats(): Promise<DistributionItem[]> {
  const res = await api.get<any[]>("/stats/tone");
  return res.data.map(item => ({
    label: item.tone,
    count: item.count,
  }));
}

export async function getIssueStats(): Promise<DistributionItem[]> {
  const res = await api.get<any[]>("/stats/issues");
  return res.data.map(item => ({
    label: item.issue_type,
    count: item.count,
  }));
}

// ---------------- INSIGHTS ----------------

export async function getInsights(callId: string): Promise<Insight> {
  const res = await api.get<any>(`/insights/${callId}`);

  return {
    call_id: callId,
    risk_level: res.data.risk_level,
    summary: res.data.short_summary,               
    recommended_action: res.data.suggested_action, 
    frustration_score: res.data.frustration_score,
  };
}
