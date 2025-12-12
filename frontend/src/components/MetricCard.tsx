// src/components/MetricCard.tsx
import React from "react";

interface MetricCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ label, value, subtitle }) => (
  <div className="metric-card">
    <div className="metric-label">{label}</div>
    <div className="metric-value">{value}</div>
    {subtitle && <div className="metric-subtitle">{subtitle}</div>}
  </div>
);

export default MetricCard;
