// src/components/CallDetails.tsx
import React from "react";
import type  { Insight, SupportCall } from "../api/types";

interface CallDetailsProps {
  call?: SupportCall;
  insight?: Insight;
}

const CallDetails: React.FC<CallDetailsProps> = ({ call, insight }) => {
  if (!call) {
    return (
      <div className="card">
        <h2>Call Details</h2>
        <p>Select a call from the table to view details.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Call Details</h2>

      <div className="details-section">
        <h3>Metadata</h3>
        <p><strong>Agent:</strong> {call.agent}</p>
        <p><strong>Issue:</strong> {call.issue_type}</p>
        <p><strong>Sentiment:</strong> {call.sentiment}</p>
        <p><strong>Tone:</strong> {call.tone}</p>
        <p><strong>Resolution:</strong> {call.resolution_status}</p>
        <p><strong>Duration:</strong> {call.call_duration} sec</p>
      </div>

      <div className="details-section">
        <h3>Transcript</h3>
        <div className="transcript-box">{call.transcript}</div>
      </div>

      {insight && (
        <div className="details-section">
          <h3>AI / Rule-Based Insights</h3>
          <p><strong>Risk level:</strong> {insight.risk_level}</p>
          <p><strong>Summary:</strong> {insight.summary}</p>
          <p><strong>Recommended action:</strong> {insight.recommended_action}</p>
          {insight.frustration_score !== undefined && (
            <p>
              <strong>Frustration score:</strong> {insight.frustration_score.toFixed(2)}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default CallDetails;
