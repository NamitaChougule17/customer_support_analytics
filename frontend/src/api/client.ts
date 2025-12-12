// src/api/client.ts
import axios from "axios";
import type {
  SupportCall,
  SummaryStats,
  DistributionItem,
  Insight,
} from "./types";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

export async function getCalls(): Promise<SupportCall[]> {
  const res = await api.get<SupportCall[]>("/calls/");
  return res.data;
}

export async function getCallById(id: string): Promise<SupportCall> {
  const res = await api.get<SupportCall>(`/calls/${id}`);
  return res.data;
}

export async function getSummaryStats(): Promise<SummaryStats> {
  const res = await api.get<SummaryStats>("/stats/summary");
  return res.data;
}

export async function getSentimentStats(): Promise<DistributionItem[]> {
  const res = await api.get<DistributionItem[]>("/stats/sentiment");
  return res.data;
}

export async function getToneStats(): Promise<DistributionItem[]> {
  const res = await api.get<DistributionItem[]>("/stats/tone");
  return res.data;
}

export async function getIssueStats(): Promise<DistributionItem[]> {
  const res = await api.get<DistributionItem[]>("/stats/issues");
  return res.data;
}

export async function getInsights(callId: string): Promise<Insight> {
  const res = await api.get<Insight>(`/insights/${callId}`);
  return res.data;
}
