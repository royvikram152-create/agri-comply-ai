import React, { useState } from 'react';
import { X, Sliders, Play, CheckCircle2, ShieldAlert } from 'lucide-react';
import { simulateWhatIf } from '../api/client';

interface WhatIfModalProps {
  isOpen: boolean;
  onClose: () => void;
  shipmentId: string;
  currentStatus?: string;
  currentScore?: number;
}

export const WhatIfModal: React.FC<WhatIfModalProps> = ({
  isOpen,
  onClose,
  shipmentId,
  currentStatus = 'HOLD',
  currentScore = 72,
}) => {
  const [destination, setDestination] = useState('European Union');
  const [deadlineDays, setDeadlineDays] = useState(7);
  const [residueValue, setResidueValue] = useState(0.82);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const res = await simulateWhatIf(shipmentId, {
        destination,
        deadline_days: deadlineDays,
        residue_value: residueValue,
      });
      setResult(res);
    } catch (err) {
      console.error('What-if error:', err);
    } finally {
      setLoading(false);
    }
  };

  const realShipmentInfo = result?.current_real_shipment || {
    status: currentStatus,
    compliance_score: currentScore,
    residue_value: currentStatus === 'APPROVED' || currentStatus === 'READY_FOR_APPROVAL' ? 0.31 : 0.82,
    unit: 'mg/kg'
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-xl w-full shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-800/90 border-b border-slate-700/60 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-indigo-500/20 text-indigo-400">
              <Sliders className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-100 text-lg">What-If Analysis Simulation</h3>
              <p className="text-xs text-slate-400">Non-destructive parameter trade scenario modeling</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Destination</label>
              <select
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-xs text-slate-200"
              >
                <option value="European Union">European Union</option>
                <option value="United Kingdom">United Kingdom</option>
                <option value="United States">United States</option>
                <option value="UAE / Gulf Region">UAE / Gulf Region</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Deadline (Days)</label>
              <input
                type="number"
                value={deadlineDays}
                onChange={(e) => setDeadlineDays(Number(e.target.value))}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-xs text-slate-200"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Simulated Residue (mg/kg)</label>
              <input
                type="number"
                step="0.01"
                value={residueValue}
                onChange={(e) => setResidueValue(Number(e.target.value))}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-xs text-slate-200"
              />
            </div>
          </div>

          <button
            onClick={handleSimulate}
            disabled={loading}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-indigo-900/30 flex items-center justify-center space-x-2 transition"
          >
            <Play className="w-4 h-4" />
            <span>{loading ? 'Simulating Pipeline...' : 'Run Non-Destructive Simulation'}</span>
          </button>

          {result && (
            <div className="mt-4 p-4 bg-slate-950 border border-indigo-500/30 rounded-xl space-y-3">
              <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Simulation Outcome vs Current Real Shipment</div>
              <div className="grid grid-cols-2 gap-4 text-xs">
                {/* Current Real Shipment (Dynamic Persisted State) */}
                <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg">
                  <div className="text-slate-400 font-semibold">Current Real Shipment</div>
                  <div className={`text-sm font-bold mt-1 ${realShipmentInfo.status === 'APPROVED' || realShipmentInfo.status === 'READY_FOR_APPROVAL' ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {realShipmentInfo.status}
                  </div>
                  <div className="text-slate-300 text-[11px] mt-0.5 font-medium">Score: {realShipmentInfo.compliance_score} / 100</div>
                  <div className="text-slate-400 text-[10px] mt-0.5">Residue: {realShipmentInfo.residue_value} {realShipmentInfo.unit || 'mg/kg'}</div>
                </div>

                {/* Simulated Scenario */}
                <div className="p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-lg">
                  <div className="text-emerald-400 font-semibold">Simulated Scenario</div>
                  <div className={`text-sm font-bold mt-1 ${result.simulated_outcome.status === 'READY_FOR_APPROVAL' ? 'text-emerald-300' : 'text-rose-400'}`}>
                    {result.simulated_outcome.status}
                  </div>
                  <div className="text-emerald-300 text-[11px] mt-0.5 font-medium">Simulated Score: {result.simulated_outcome.compliance_score} / 100</div>
                  <div className="text-slate-300 text-[10px] mt-0.5">Simulated Residue: {result.parameters.residue_value} mg/kg</div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-slate-800/80 border-t border-slate-700/60 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-xs font-medium transition"
          >
            Close Simulation
          </button>
        </div>
      </div>
    </div>
  );
};
