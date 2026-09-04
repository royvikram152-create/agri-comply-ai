import React from 'react';
import { Shipment } from '../types';
import { MetricCard } from '../components/MetricCard';
import { StatusBadge } from '../components/StatusBadge';
import { Package, ShieldAlert, CheckCircle2, ArrowRight, Activity, Calendar, Sparkles, UserCheck } from 'lucide-react';

interface DashboardProps {
  shipments: Shipment[];
  onSelectShipment: (id: string) => void;
  onNewShipmentClick: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ shipments, onSelectShipment, onNewShipmentClick }) => {
  const totalCount = shipments.length;
  const holdCount = shipments.filter(s => s.status === 'HOLD' || s.status === 'DOCUMENTS_PENDING').length;
  const readyCount = shipments.filter(s => s.status === 'READY_FOR_APPROVAL' || s.status === 'APPROVED').length;
  const avgScore = shipments.length > 0 ? (shipments.reduce((acc, s) => acc + s.compliance_score, 0) / shipments.length).toFixed(1) : '0';

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">Enterprise Export Compliance Overview</h2>
          <p className="text-xs text-slate-400 mt-1">Real-time agentic document extraction, cross-document contradiction checks, and deterministic compliance firewall.</p>
        </div>
        <button
          onClick={onNewShipmentClick}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-emerald-900/40 flex items-center space-x-2 transition cursor-pointer"
        >
          <Package className="w-4 h-4" />
          <span>+ Create New Shipment</span>
        </button>
      </div>

      {/* Metric Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Shipments"
          value={totalCount}
          subtitle="Monitored in system"
          icon={<Package className="w-5 h-5 text-indigo-400" />}
          badgeColor="bg-indigo-500/10 border border-indigo-500/20"
        />
        <MetricCard
          title="Hold / Pending Docs"
          value={holdCount}
          subtitle="Requires documents/remediation"
          icon={<ShieldAlert className="w-5 h-5 text-rose-400" />}
          badgeColor="bg-rose-500/10 border border-rose-500/20"
        />
        <MetricCard
          title="Ready / Approved"
          value={readyCount}
          subtitle="Cleared for export"
          icon={<CheckCircle2 className="w-5 h-5 text-emerald-400" />}
          badgeColor="bg-emerald-500/10 border border-emerald-500/20"
        />
        <MetricCard
          title="Avg Compliance Score"
          value={`${avgScore} / 100`}
          subtitle="Deterministic index"
          icon={<Activity className="w-5 h-5 text-amber-400" />}
          badgeColor="bg-amber-500/10 border border-amber-500/20"
        />
      </div>

      {/* Active Shipments Table */}
      <div className="bg-slate-950/60 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <h3 className="font-bold text-slate-100 text-sm tracking-wide uppercase">Active Export Shipments</h3>
          <span className="text-xs text-slate-400">Click shipment to upload real documents & inspect readiness</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/80 text-slate-400 uppercase font-semibold border-b border-slate-800">
              <tr>
                <th className="py-3.5 px-4">Shipment ID</th>
                <th className="py-3.5 px-4">Type</th>
                <th className="py-3.5 px-4">Crop / Variety</th>
                <th className="py-3.5 px-4">Trade Route</th>
                <th className="py-3.5 px-4">Quantity</th>
                <th className="py-3.5 px-4">Deadline</th>
                <th className="py-3.5 px-4">Score</th>
                <th className="py-3.5 px-4">Status</th>
                <th className="py-3.5 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-200">
              {shipments.map((s) => {
                const isDemo = s.id === 'SHP-MANGO-001' || s.is_demo === true;
                return (
                  <tr key={s.id} className="hover:bg-slate-900/50 transition">
                    <td className="py-4 px-4 font-mono font-bold text-slate-100">{s.id}</td>
                    <td className="py-4 px-4">
                      {isDemo ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                          <Sparkles className="w-3 h-3" /> DEMO SHIPMENT
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          <UserCheck className="w-3 h-3" /> USER SHIPMENT
                        </span>
                      )}
                    </td>
                    <td className="py-4 px-4 font-semibold text-slate-200">
                      {s.crop} <span className="text-slate-400 font-normal">({s.variety})</span>
                    </td>
                    <td className="py-4 px-4 font-medium text-slate-300">
                      {s.origin} → {s.destination}
                    </td>
                    <td className="py-4 px-4 font-medium text-slate-300">{s.quantity_kg.toLocaleString()} kg</td>
                    <td className="py-4 px-4 text-slate-300 font-medium">
                      <span className="flex items-center">
                        <Calendar className="w-3.5 h-3.5 mr-1 text-amber-400" />
                        {s.deadline_days} Days
                      </span>
                    </td>
                    <td className="py-4 px-4 font-bold text-emerald-400">{s.compliance_score} / 100</td>
                    <td className="py-4 px-4">
                      <StatusBadge status={s.status} size="sm" />
                    </td>
                    <td className="py-4 px-4 text-right">
                      <button
                        onClick={() => onSelectShipment(s.id)}
                        className="px-3 py-1.5 bg-emerald-600/20 hover:bg-emerald-600 text-emerald-400 hover:text-white border border-emerald-500/30 rounded-lg text-xs font-semibold inline-flex items-center space-x-1 transition"
                      >
                        <span>{s.status === 'DOCUMENTS_PENDING' ? 'Upload & Process' : 'Inspect Readiness'}</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
