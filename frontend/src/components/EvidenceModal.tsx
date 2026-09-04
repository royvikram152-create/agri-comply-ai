import React from 'react';
import { X, ExternalLink, ShieldAlert, FileText, Scale, Database, CheckCircle2, ArrowRight } from 'lucide-react';
import { ComplianceFinding } from '../types';

interface EvidenceModalProps {
  isOpen: boolean;
  onClose: () => void;
  finding: ComplianceFinding | null;
  overallStatus: string;
}

export const EvidenceModal: React.FC<EvidenceModalProps> = ({ isOpen, onClose, finding, overallStatus }) => {
  if (!isOpen || !finding) return null;

  const sourceType = (finding as any).source_type || 'OFFICIAL SOURCE';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-md p-4 animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-2xl w-full shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-800/90 border-b border-slate-700/60 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="font-bold text-slate-100 text-lg">Official Evidence Provenance Chain</h3>
                <span className={`px-2 py-0.5 text-[10px] font-extrabold rounded-full border ${
                  sourceType === 'OFFICIAL SOURCE'
                    ? 'bg-blue-500/20 text-blue-300 border-blue-500/40'
                    : 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                }`}>
                  {sourceType}
                </span>
              </div>
              <p className="text-xs text-slate-400">Traceable deterministic compliance evaluation chain</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6 max-h-[80vh] overflow-y-auto">
          {/* Visual Evidence Chain Flow */}
          <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-4">
            <div className="text-xs font-semibold uppercase tracking-wider text-emerald-400">Deterministic Evaluation Flow</div>
            
            {/* Step 1: Decision */}
            <div className="flex items-start space-x-3">
              <div className="mt-1 p-1.5 rounded-md bg-rose-500/20 text-rose-400">
                <ShieldAlert className="w-4 h-4" />
              </div>
              <div className="flex-1">
                <div className="text-xs text-slate-400">1. System Decision</div>
                <div className="text-sm font-bold text-rose-400">{finding.status === 'FAIL' ? 'STATUS: HOLD / FAIL' : 'STATUS: PASS'}</div>
                <div className="text-xs text-slate-300 mt-0.5">{finding.reason}</div>
              </div>
            </div>

            <div className="pl-4 text-slate-600"><ArrowRight className="w-4 h-4 rotate-90" /></div>

            {/* Step 2: Actual Data & Allowed Limit */}
            <div className="flex items-start space-x-3">
              <div className="mt-1 p-1.5 rounded-md bg-amber-500/20 text-amber-400">
                <FileText className="w-4 h-4" />
              </div>
              <div className="flex-1 space-y-1">
                <div className="text-xs text-slate-400">2. Empirical Farm / Document Data</div>
                <div className="text-sm font-semibold text-amber-300">Actual: {finding.actual_data}</div>
                {(finding as any).allowed_limit && (
                  <div className="text-xs text-slate-300">
                    Allowed Threshold: <strong className="text-emerald-400">{(finding as any).allowed_limit}</strong> | Difference: <strong className="text-rose-400">{(finding as any).difference}</strong>
                  </div>
                )}
              </div>
            </div>

            <div className="pl-4 text-slate-600"><ArrowRight className="w-4 h-4 rotate-90" /></div>

            {/* Step 3: Applicable Requirement */}
            <div className="flex items-start space-x-3">
              <div className="mt-1 p-1.5 rounded-md bg-blue-500/20 text-blue-400">
                <Scale className="w-4 h-4" />
              </div>
              <div className="flex-1">
                <div className="text-xs text-slate-400">3. Applicable Regulatory Threshold / Rule</div>
                <div className="text-sm font-medium text-slate-200">{finding.applicable_requirement}</div>
              </div>
            </div>

            <div className="pl-4 text-slate-600"><ArrowRight className="w-4 h-4 rotate-90" /></div>

            {/* Step 4: Source Provenance */}
            <div className="flex items-start space-x-3">
              <div className="mt-1 p-1.5 rounded-md bg-emerald-500/20 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <div className="flex-1">
                <div className="text-xs text-slate-400">4. Authoritative Source Provenance</div>
                <div className="text-sm font-medium text-emerald-400">{finding.source_evidence}</div>
                {finding.source_url && (
                  <a
                    href={finding.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center text-xs text-emerald-400 hover:text-emerald-300 underline mt-1"
                  >
                    View Official EC / EFSA Regulation Document <ExternalLink className="w-3 h-3 ml-1" />
                  </a>
                )}
              </div>
            </div>
          </div>

          {/* Actionable Remediation Box */}
          <div className="bg-emerald-950/30 border border-emerald-500/30 p-4 rounded-xl">
            <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-1">Recommended Action</h4>
            <p className="text-sm text-emerald-100">{finding.recommended_action}</p>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-slate-800/80 border-t border-slate-700/60 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-sm font-medium transition"
          >
            Close Provenance View
          </button>
        </div>
      </div>
    </div>
  );
};
