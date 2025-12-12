// src/components/IssueChart.tsx
import React from "react";
import type { DistributionItem } from "../api/types";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface Props {
  data: DistributionItem[];
}

const IssueChart: React.FC<Props> = ({ data }) => (
  <div className="card">
    <h2>Issue Type Distribution</h2>
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <XAxis dataKey="label" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar
            dataKey="count"
            fill="#FF9580"
            radius={[6, 6, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  </div>
);

export default IssueChart;
