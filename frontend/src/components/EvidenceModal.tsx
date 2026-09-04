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

  const getSourceBadgeStyle = (type: string) => {
    switch (type) {
      case 'OFFICIAL SOURCE':
        return 'bg-blue-500/20 text-blue-300 border-blue-500/40';
      case 'DEMO DATA':
        return 'bg-purple-500/20 text-purple-300 border-purple-500/40';
      case 'APPLICATION/DOCUMENT RULE':
      default:
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
    }
  };

  const isMissingDoc = finding.category === 'DOCUMENT' && (
    finding.title.toLowerCase().includes('missing') ||
    finding.reason.toLowerCase().includes('missing') ||
    (finding.actual_data && finding.actual_data.toLowerCase().startsWith('no uploaded document'))
  );

  const isMissingResidue = finding.actual_data === "Could not extract this field from uploaded evidence." ||
    (finding.reason && finding.reason.toLowerCase().includes('could not extract'));

  let docName = (finding as any).document_type || '';
  if (!docName && finding.title) {
    const match = finding.title.match(/\(([^)]+)\)/);
    if (match) {
      docName = match[1];
    } else {
      docName = finding.title;
    }
  }

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
                <span className={`px-2.5 py-0.5 text-[10px] font-extrabold rounded-full border ${getSourceBadgeStyle(sourceType)}`}>
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
                <div className={`text-sm font-bold ${finding.status === 'FAIL' ? 'text-rose-400' : 'text-emerald-400'}`}>
                  {finding.status === 'FAIL' ? 'STATUS: HOLD / FAIL' : `STATUS: ${finding.status}`}
                </div>
                <div className="text-xs text-slate-300 mt-0.5">{finding.reason}</div>
              </div>
            </div>

            <div className="pl-4 text-slate-600"><ArrowRight className="w-4 h-4 rotate-90" /></div>

            {/* Step 2: Actual Evidence */}
            <div className="flex items-start space-x-3">
              <div className={`mt-1 p-1.5 rounded-md ${
                isMissingDoc || isMissingResidue ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
              }`}>
                <FileText className="w-4 h-4" />
              </div>
              <div className="flex-1 space-y-1">
                <div className="text-xs text-slate-400">2. Actual Evidence</div>

                {isMissingDoc ? (
                  <div className="bg-slate-900/90 p-3 rounded-lg border border-rose-500/30 space-y-1">
                    <div className="text-xs text-slate-400">
                      Document: <strong className="text-slate-200 font-mono">{docName}</strong>
                    </div>
                    <div className="text-xs font-bold text-rose-400">
                      Status: MISSING
                    </div>
                    <div className="text-xs text-slate-300">
                      Evidence found: <span className="text-rose-300">{finding.actual_data}</span>
                    </div>
                  </div>
                ) : isMissingResidue ? (
                  <div className="bg-slate-900/90 p-3 rounded-lg border border-rose-500/30 space-y-1">
                    <div className="text-xs font-bold text-rose-400">
                      Status: MISSING LABORATORY RESIDUE EVIDENCE
                    </div>
                    <div className="text-xs text-slate-300">
                      Evidence found: <span className="text-rose-300">{finding.actual_data}</span>
                    </div>
                  </div>
                ) : finding.category === 'DOCUMENT' ? (
                  <div className="bg-slate-900/90 p-3 rounded-lg border border-emerald-500/30 space-y-1">
                    <div className="text-xs text-slate-400">
                      Document: <strong className="text-slate-200 font-mono">{(finding as any).document_type || docName}</strong>
                    </div>
                    <div className="text-xs font-bold text-emerald-400">
                      Status: {finding.status === 'PASS' ? 'PRESENT / VALID' : finding.status}
                    </div>
                    {(finding as any).file_name && (
                      <div className="text-xs text-slate-300">
                        Filename: <span className="font-mono text-emerald-300">{(finding as any).file_name}</span>
                      </div>
                    )}
                    <div className="text-xs text-slate-300">
                      Extracted Evidence: <span className="text-slate-200">{finding.actual_data}</span>
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="text-sm font-semibold text-amber-300">Actual: {finding.actual_data}</div>
                    {(finding as any).allowed_limit && (
                      <div className="text-xs text-slate-300 mt-1">
                        Allowed Threshold: <strong className="text-emerald-400">{(finding as any).allowed_limit}</strong>
                        {(finding as any).difference && (
                          <> | Difference: <strong className="text-rose-400">{(finding as any).difference}</strong></>
                        )}
                      </div>
                    )}
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
                    View Official Regulation Document <ExternalLink className="w-3 h-3 ml-1" />
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
