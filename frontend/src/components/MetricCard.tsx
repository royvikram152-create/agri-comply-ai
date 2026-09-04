import React, { ReactNode } from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: ReactNode;
  trend?: string;
  badgeColor?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({ title, value, subtitle, icon, badgeColor = 'bg-slate-800' }) => {
  return (
    <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 shadow-lg backdrop-blur-sm">
      <div className="flex items-center justify-between">
        <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider">{title}</span>
        <div className={`p-2 rounded-lg ${badgeColor} text-slate-200`}>
          {icon}
        </div>
      </div>
      <div className="mt-3">
        <div className="text-2xl font-bold text-slate-100 tracking-tight">{value}</div>
        {subtitle && <div className="text-xs text-slate-400 mt-1 font-medium">{subtitle}</div>}
      </div>
    </div>
  );
};
