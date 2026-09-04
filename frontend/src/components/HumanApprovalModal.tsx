import React, { useState } from 'react';
import { X, ShieldCheck, ShieldAlert, CheckCircle, XCircle, RefreshCw } from 'lucide-react';
import { submitHumanApproval } from '../api/client';

interface HumanApprovalModalProps {
  isOpen: boolean;
  onClose: () => void;
  shipmentId: string;
  currentStatus: string;
  hasCriticalGaps: boolean;
  onApprovalComplete: () => void;
}

export const HumanApprovalModal: React.FC<HumanApprovalModalProps> = ({
  isOpen,
  onClose,
  shipmentId,
  currentStatus,
  hasCriticalGaps,
  onApprovalComplete,
}) => {
  const [reviewer, setReviewer] = useState('Senior Export Compliance Officer (APEDA/EU)');
  const [action, setAction] = useState<'APPROVE' | 'REJECT' | 'REQUEST_CORRECTION'>('APPROVE');
  const [comments, setComments] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (hasCriticalGaps && action === 'APPROVE') {
      setError('Cannot approve shipment while critical compliance gaps exist!');
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await submitHumanApproval(shipmentId, { reviewer, action, comments });
      onApprovalComplete();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Approval submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-lg w-full shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-800/90 border-b border-slate-700/60 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-lg ${hasCriticalGaps ? 'bg-rose-500/20 text-rose-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
              {hasCriticalGaps ? <ShieldAlert className="w-5 h-5" /> : <ShieldCheck className="w-5 h-5" />}
            </div>
            <div>
              <h3 className="font-bold text-slate-100 text-lg">Human Approval Gate</h3>
              <p className="text-xs text-slate-400">Final mandatory sign-off before export dispatch</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {hasCriticalGaps && (
            <div className="p-4 bg-rose-950/40 border border-rose-500/30 rounded-xl text-xs text-rose-300 font-semibold flex items-start space-x-2">
              <ShieldAlert className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
              <span>APPROVAL BLOCKED: Shipment has unresolved CRITICAL compliance gaps. You must upload remediated lab tests before approving.</span>
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-900/50 border border-red-500 text-red-200 text-xs rounded-xl font-medium">
              {error}
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">
              Reviewer Name & Title
            </label>
            <input
              type="text"
              value={reviewer}
              onChange={(e) => setReviewer(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-slate-100 text-sm focus:outline-none focus:border-brand-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Select Decision Action
            </label>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setAction('APPROVE')}
                disabled={hasCriticalGaps}
                className={`px-3 py-2 rounded-xl text-xs font-bold border flex items-center justify-center space-x-1.5 transition ${
                  action === 'APPROVE'
                    ? 'bg-emerald-600 text-white border-emerald-500 shadow-md'
                    : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-750'
                } ${hasCriticalGaps ? 'opacity-40 cursor-not-allowed' : ''}`}
              >
                <CheckCircle className="w-4 h-4" />
                <span>Approve</span>
              </button>

              <button
                type="button"
                onClick={() => setAction('REQUEST_CORRECTION')}
                className={`px-3 py-2 rounded-xl text-xs font-bold border flex items-center justify-center space-x-1.5 transition ${
                  action === 'REQUEST_CORRECTION'
                    ? 'bg-amber-600 text-white border-amber-500 shadow-md'
                    : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-750'
                }`}
              >
                <RefreshCw className="w-4 h-4" />
                <span>Correction</span>
              </button>

              <button
                type="button"
                onClick={() => setAction('REJECT')}
                className={`px-3 py-2 rounded-xl text-xs font-bold border flex items-center justify-center space-x-1.5 transition ${
                  action === 'REJECT'
                    ? 'bg-red-600 text-white border-red-500 shadow-md'
                    : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-750'
                }`}
              >
                <XCircle className="w-4 h-4" />
                <span>Reject</span>
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">
              Reviewer Comments / Observations
            </label>
            <textarea
              rows={3}
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              placeholder="Enter official sign-off notes or required remediation instructions..."
              className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-slate-100 text-sm focus:outline-none focus:border-brand-500"
            />
          </div>

          {/* Footer buttons */}
          <div className="pt-3 border-t border-slate-800 flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm font-medium transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting || (hasCriticalGaps && action === 'APPROVE')}
              className="px-5 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white font-bold rounded-lg text-sm shadow-lg shadow-brand-900/30 transition"
            >
              {submitting ? 'Submitting...' : 'Confirm Decision'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
