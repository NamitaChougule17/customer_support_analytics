// src/pages/DashboardPage.tsx
import React, { useEffect, useState } from "react";
import {
  getCalls,
  getSummaryStats,
  getSentimentStats,
  getToneStats,
  getIssueStats,
  getInsights,
} from "../api/client";
import type {
  SupportCall,
  SummaryStats,
  DistributionItem,
  Insight,
} from "../api/types";
import MetricCard from "../components/MetricCard";
import CallTable from "../components/CallTable";
import CallDetails from "../components/CallDetails";
import SentimentChart from "../components/SentimentChart";
import ToneChart from "../components/ToneChart";
import IssueChart from "../components/IssueChart";

// ✅ SAFETY FUNCTION — prevents crashes when summary values are null/undefined
function safeToFixed(value: number | null | undefined, digits: number): string {
  if (value == null || Number.isNaN(value)) return "-";
  return value.toFixed(digits);
}

const DashboardPage: React.FC = () => {
  const [calls, setCalls] = useState<SupportCall[]>([]);
  const [summary, setSummary] = useState<SummaryStats | null>(null);
  const [sentimentStats, setSentimentStats] = useState<DistributionItem[]>([]);
  const [toneStats, setToneStats] = useState<DistributionItem[]>([]);
  const [issueStats, setIssueStats] = useState<DistributionItem[]>([]);
  const [selectedCall, setSelectedCall] = useState<SupportCall | undefined>();
  const [insight, setInsight] = useState<Insight | undefined>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError(null);

        const [callsRes, summaryRes, sentimentRes, toneRes, issueRes] =
          await Promise.all([
            getCalls(),
            getSummaryStats(),
            getSentimentStats(),
            getToneStats(),
            getIssueStats(),
          ]);

        setCalls(callsRes);
        setSummary(summaryRes);
        setSentimentStats(sentimentRes);
        setToneStats(toneRes);
        setIssueStats(issueRes);

        if (callsRes.length > 0) {
          const first = callsRes[0];
          setSelectedCall(first);
          const insightRes = await getInsights(first.id);
          setInsight(insightRes);
        }
      } catch (err) {
        console.error(err);
        setError("Failed to load data from API.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  const handleSelectCall = async (call: SupportCall) => {
    setSelectedCall(call);
    try {
      const insightRes = await getInsights(call.id);
      setInsight(insightRes);
    } catch (err) {
      console.error(err);
      setInsight(undefined);
    }
  };

  if (loading) {
    return <div className="page-centered">Loading dashboard…</div>;
  }

  if (error) {
    return <div className="page-centered error">{error}</div>;
  }

  return (
    <div className="dashboard-layout">
      <section className="metrics-row">
        <MetricCard label="Total Calls" value={summary?.total_calls ?? 0} />
        <MetricCard
          label="Resolved"
          value={summary?.resolved_calls ?? 0}
          subtitle="calls"
        />
        <MetricCard
          label="Unresolved"
          value={summary?.unresolved_calls ?? 0}
          subtitle="calls"
        />

        {/* ✅ FIXED — now always safe */}
        <MetricCard
          label="Avg Duration"
          value={`${safeToFixed(summary?.average_duration, 1)} sec`}
        />

        {/* ✅ FIXED — now always safe */}
        <MetricCard
          label="Avg Frustration"
          value={safeToFixed(summary?.average_frustration, 2)}
        />
      </section>

      <section className="charts-row">
        <SentimentChart data={sentimentStats} />
        <ToneChart data={toneStats} />
        <IssueChart data={issueStats} />
      </section>

      <section className="bottom-row">
        <div className="bottom-left">
          <CallTable
            calls={calls}
            selectedId={selectedCall?.id}
            onSelect={handleSelectCall}
          />
        </div>
        <div className="bottom-right">
          <CallDetails call={selectedCall} insight={insight} />
        </div>
      </section>
    </div>
  );
};

export default DashboardPage;
