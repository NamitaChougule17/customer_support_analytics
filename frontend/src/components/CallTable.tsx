// src/components/CallTable.tsx
import React from "react";
import type { SupportCall } from "../api/types";

interface CallTableProps {
  calls: SupportCall[];
  selectedId?: string;
  onSelect: (call: SupportCall) => void;
}

const CallTable: React.FC<CallTableProps> = ({ calls, selectedId, onSelect }) => {
  return (
    <div className="card">
      <h2>Recent Calls</h2>
      <div className="table-wrapper">
        <table className="calls-table">
          <thead>
            <tr>
              <th>Agent</th>
              <th>Issue</th>
              <th>Sentiment</th>
              <th>Tone</th>
              <th>Resolution</th>
              <th>Duration (sec)</th>
            </tr>
          </thead>
          <tbody>
            {calls.map((call) => (
              <tr
                key={call.id}
                className={call.id === selectedId ? "selected-row" : ""}
                onClick={() => onSelect(call)}
              >
                <td>{call.agent}</td>
                <td>{call.issue_type}</td>
                <td className={`pill pill-${call.sentiment}`}>
                  {call.sentiment}
                </td>
                <td>{call.tone}</td>
                <td>{call.resolution_status}</td>
                <td>{call.call_duration}</td>
              </tr>
            ))}
            {calls.length === 0 && (
              <tr>
                <td colSpan={6} style={{ textAlign: "center" }}>
                  No calls found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CallTable;
