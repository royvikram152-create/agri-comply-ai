import React from 'react';
import { RemediationSummary } from '../types';
import { ArrowRight, CheckCircle2, ShieldAlert, Sparkles, FileText } from 'lucide-react';

interface WhatChangedCardProps {
  summary: RemediationSummary | null;
  onSimulateRemediation?: () => void;
  loading?: boolean;
}

export const WhatChangedCard: React.FC<WhatChangedCardProps> = ({ summary, onSimulateRemediation, loading }) => {
  if (!summary) {
    return (
      <div className="bg-gradient-to-br from-slate-800/90 to-slate-900 border border-slate-700/80 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-100 text-lg">Phase H: "What Changed?" Remediation Workflow</h3>
              <p className="text-xs text-slate-400">Simulate uploading a passing lab residue test (0.31 mg/kg) to trigger real backend compliance re-evaluation.</p>
            </div>
          </div>
          {onSimulateRemediation && (
            <button
              onClick={onSimulateRemediation}
              disabled={loading}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-sm font-semibold shadow-lg shadow-emerald-900/30 flex items-center space-x-2 transition disabled:opacity-50"
            >
              <FileText className="w-4 h-4" />
              <span>{loading ? 'Re-evaluating Pipeline...' : 'Upload Passing Residue Test'}</span>
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-slate-800/90 to-slate-900 border border-emerald-500/30 rounded-2xl p-6 shadow-2xl relative overflow-hidden">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            <Sparkles className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h3 className="font-bold text-emerald-400 text-lg">Remediation Transition: "What Changed?"</h3>
            <p className="text-xs text-slate-300">Actual backend state machine re-evaluation result</p>
          </div>
        </div>
        <span className="px-3 py-1 bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-bold rounded-full uppercase tracking-wider">
          REMEDIATED
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-950/70 p-4 rounded-xl border border-slate-800">
        {/* BEFORE */}
        <div className="bg-rose-950/30 border border-rose-500/30 p-4 rounded-lg">
          <div className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-2 flex items-center">
            <ShieldAlert className="w-4 h-4 mr-1" /> BEFORE (INITIAL STATE)
          </div>
          <div className="text-2xl font-bold text-rose-300">{summary.before.status}</div>
          <div className="text-xs text-slate-300 mt-1">Score: {summary.before.compliance_score} / 100</div>
          <div className="text-xs text-rose-400 mt-1 font-semibold">Residue: {summary.before.residue_value} mg/kg (FAIL)</div>
        </div>

        {/* ACTION */}
        <div className="bg-blue-950/30 border border-blue-500/30 p-4 rounded-lg flex flex-col justify-center">
          <div className="text-xs font-bold text-blue-400 uppercase tracking-wider mb-2 flex items-center">
            <FileText className="w-4 h-4 mr-1" /> ACTION TAKEN
          </div>
          <div className="text-sm font-bold text-blue-200">{summary.action.document_name}</div>
          <div className="text-xs text-emerald-400 mt-1 font-semibold">New Residue: {summary.action.new_residue_value} {summary.action.unit} (PASS)</div>
        </div>

        {/* AFTER */}
        <div className="bg-emerald-950/30 border border-emerald-500/30 p-4 rounded-lg">
          <div className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2 flex items-center">
            <CheckCircle2 className="w-4 h-4 mr-1" /> AFTER (RE-EVALUATED)
          </div>
          <div className="text-2xl font-bold text-emerald-300">{summary.after.status}</div>
          <div className="text-xs text-slate-300 mt-1">Score: {summary.after.compliance_score} / 100</div>
          <div className="text-xs text-emerald-400 mt-1 font-semibold">0 Critical Gaps - Ready for Approval</div>
        </div>
      </div>

      <div className="mt-4 p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-xs text-emerald-300 font-medium flex items-center">
        <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-400 flex-shrink-0" />
        {summary.transition_summary}
      </div>
    </div>
  );
};
