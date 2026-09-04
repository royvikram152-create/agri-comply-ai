import React, { useEffect, useState } from 'react';
import { fetchCompliance, fetchAuditTrail, fetchDocuments, analyzeShipment, remediateShipment } from '../api/client';
import { Shipment, ComplianceResult, RiskAssessment, Document, AuditEvent, RemediationSummary, ComplianceFinding } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { MetricCard } from '../components/MetricCard';
import { EvidenceModal } from '../components/EvidenceModal';
import { WhatChangedCard } from '../components/WhatChangedCard';
import { HumanApprovalModal } from '../components/HumanApprovalModal';
import { WhatIfModal } from '../components/WhatIfModal';
import { Timeline } from '../components/Timeline';
import {
  ArrowLeft,
  Play,
  FileSearch,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  FileText,
  Sliders,
  UserCheck,
  ExternalLink,
  Bot,
  Calendar,
  Sparkles,
} from 'lucide-react';

interface ShipmentDetailProps {
  shipmentId: string;
  onBack: () => void;
}

export const ShipmentDetail: React.FC<ShipmentDetailProps> = ({ shipmentId, onBack }) => {
  const [data, setData] = useState<{
    shipment: Shipment;
    compliance_result: ComplianceResult;
    risk_assessment: RiskAssessment;
    remediation_history?: RemediationSummary;
  } | null>(null);

  const [documents, setDocuments] = useState<Document[]>([]);
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [remediating, setRemediating] = useState(false);

  // Modals state
  const [selectedFinding, setSelectedFinding] = useState<ComplianceFinding | null>(null);
  const [showApprovalModal, setShowApprovalModal] = useState(false);
  const [showWhatIfModal, setShowWhatIfModal] = useState(false);

  const loadAll = async () => {
    setLoading(true);
    try {
      const compData = await fetchCompliance(shipmentId);
      const docs = await fetchDocuments(shipmentId);
      const audit = await fetchAuditTrail(shipmentId);
      setData(compData);
      setDocuments(docs);
      setAuditEvents(audit);
    } catch (err) {
      console.error('Error loading detail:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, [shipmentId]);

  const handleRunPipeline = async () => {
    setAnalyzing(true);
    try {
      await analyzeShipment(shipmentId);
      await loadAll();
    } catch (err) {
      console.error('Pipeline error:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleRemediateResidue = async () => {
    setRemediating(true);
    try {
      await remediateShipment(shipmentId, 0.31);
      await loadAll();
    } catch (err) {
      console.error('Remediation error:', err);
    } finally {
      setRemediating(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex items-center space-x-3 text-emerald-400 font-bold">
          <FileSearch className="w-6 h-6 animate-spin" />
          <span>Loading Deterministic Compliance Intelligence...</span>
        </div>
      </div>
    );
  }

  const { shipment, compliance_result, risk_assessment, remediation_history } = data;
  const criticalGapsCount = compliance_result?.findings?.filter(f => f.severity === 'CRITICAL' && f.status === 'FAIL').length || 0;
  const hasCriticalGaps = criticalGapsCount > 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Top Nav Action Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center space-x-2 text-xs font-semibold text-slate-400 hover:text-slate-200 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </button>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowWhatIfModal(true)}
            className="px-3.5 py-2 bg-slate-800 hover:bg-slate-750 text-indigo-300 border border-indigo-500/30 text-xs font-semibold rounded-xl flex items-center space-x-1.5 transition"
          >
            <Sliders className="w-4 h-4" />
            <span>What-If Simulation</span>
          </button>

          <button
            onClick={handleRunPipeline}
            disabled={analyzing}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow-lg flex items-center space-x-1.5 transition disabled:opacity-50"
          >
            <Play className={`w-4 h-4 ${analyzing ? 'animate-spin' : ''}`} />
            <span>{analyzing ? 'Executing Agents...' : 'Re-Run 5-Agent Pipeline'}</span>
          </button>

          <button
            onClick={() => setShowApprovalModal(true)}
            className={`px-4 py-2 text-xs font-bold rounded-xl shadow-lg flex items-center space-x-1.5 transition ${
              hasCriticalGaps
                ? 'bg-slate-800 text-slate-500 border border-slate-700 cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-900/30'
            }`}
          >
            <UserCheck className="w-4 h-4" />
            <span>Human Approval Gate</span>
          </button>
        </div>
      </div>

      {/* Shipment Header Banner */}
      <div className="bg-slate-950 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-3">
              <h2 className="text-2xl font-extrabold text-slate-100 font-mono tracking-tight">{shipment.id}</h2>
              <StatusBadge status={shipment.status} size="lg" />
            </div>
            <p className="text-xs text-slate-400 mt-1 font-medium">
              {shipment.exporter.name} • {shipment.crop} ({shipment.variety}) • {shipment.origin} → {shipment.destination} • {shipment.quantity_kg.toLocaleString()} kg
            </p>
          </div>

          <div className="flex items-center space-x-6 text-right">
            <div>
              <div className="text-[10px] text-slate-500 uppercase font-extrabold tracking-wider">Compliance Index</div>
              <div className="text-2xl font-black text-emerald-400">{shipment.compliance_score} / 100</div>
            </div>
            <div className="h-8 w-px bg-slate-800"></div>
            <div>
              <div className="text-[10px] text-slate-500 uppercase font-extrabold tracking-wider">Deadline Buffer</div>
              <div className="text-2xl font-black text-amber-400 flex items-center">
                <Calendar className="w-5 h-5 mr-1" />
                {shipment.deadline_days} Days
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Agent Workflow Execution Status Row */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-4 shadow-lg">
        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center">
          <Bot className="w-4 h-4 mr-1.5 text-emerald-400" />
          5 Specialized Agents Execution Pipeline
        </div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
          <div className="p-2.5 bg-slate-900 border border-emerald-500/30 rounded-xl text-center">
            <div className="text-emerald-400 font-bold">1. Exporter Agent</div>
            <div className="text-[10px] text-slate-400 mt-0.5">Metadata Parsed</div>
          </div>
          <div className="p-2.5 bg-slate-900 border border-emerald-500/30 rounded-xl text-center">
            <div className="text-emerald-400 font-bold">2. Regulatory Agent</div>
            <div className="text-[10px] text-slate-400 mt-0.5">EU RAG Retrieved</div>
          </div>
          <div className={`p-2.5 bg-slate-900 border rounded-xl text-center ${hasCriticalGaps ? 'border-rose-500/50 bg-rose-950/20' : 'border-emerald-500/30'}`}>
            <div className={`font-bold ${hasCriticalGaps ? 'text-rose-400' : 'text-emerald-400'}`}>3. Farm Agent</div>
            <div className="text-[10px] text-slate-400 mt-0.5">{hasCriticalGaps ? 'Residue Exceeded' : 'Pass'}</div>
          </div>
          <div className="p-2.5 bg-slate-900 border border-emerald-500/30 rounded-xl text-center">
            <div className="text-emerald-400 font-bold">4. Document Agent</div>
            <div className="text-[10px] text-slate-400 mt-0.5">Checklist Verified</div>
          </div>
          <div className="p-2.5 bg-slate-900 border border-emerald-500/30 rounded-xl text-center">
            <div className="text-emerald-400 font-bold">5. Gap Agent</div>
            <div className="text-[10px] text-slate-400 mt-0.5">Remediation Rank</div>
          </div>
        </div>
      </div>

      {/* Phase H: "What Changed?" Remediation Card */}
      <WhatChangedCard
        summary={remediation_history || null}
        onSimulateRemediation={handleRemediateResidue}
        loading={remediating}
      />

      {/* Main Grid Section: Findings & Evidence vs Timeline & Documents */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2-Cols: Compliance Findings & Evidence */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-950/60 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-100 text-base uppercase tracking-wider flex items-center">
                <ShieldAlert className="w-5 h-5 mr-2 text-amber-400" />
                Compliance Findings & Rule Evaluations
              </h3>
              <span className="text-xs text-slate-400 font-medium">
                {compliance_result?.findings?.length || 0} Evaluated Checks
              </span>
            </div>

            <div className="space-y-3">
              {compliance_result?.findings?.map((finding, idx) => {
                const isFail = finding.status === 'FAIL';
                return (
                  <div
                    key={finding.id || idx}
                    className={`p-4 rounded-xl border transition ${
                      isFail
                        ? 'bg-rose-950/20 border-rose-500/40 text-slate-200'
                        : 'bg-slate-900/60 border-slate-800 text-slate-300'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-center space-x-2">
                        {isFail ? (
                          <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0" />
                        ) : (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                        )}
                        <span className="font-bold text-sm text-slate-100">{finding.title}</span>
                        <span className={`text-[10px] px-2 py-0.5 rounded-md font-extrabold uppercase ${
                          finding.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400' : 'bg-slate-800 text-slate-400'
                        }`}>
                          {finding.severity}
                        </span>
                      </div>

                      <button
                        onClick={() => setSelectedFinding(finding)}
                        className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-emerald-400 border border-emerald-500/30 rounded-lg text-xs font-semibold flex items-center space-x-1 transition"
                      >
                        <ExternalLink className="w-3 h-3" />
                        <span>Why? / View Evidence</span>
                      </button>
                    </div>

                    <p className="mt-2 text-xs text-slate-300 leading-relaxed">{finding.reason}</p>

                    <div className="mt-3 flex items-center justify-between text-[11px] pt-2 border-t border-slate-800/60">
                      <span className="text-slate-400 font-mono">Rule: {finding.applicable_requirement}</span>
                      <span className="text-emerald-400 font-medium">Source: {finding.source_evidence}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Export Documents Checklist */}
          <div className="bg-slate-950/60 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <h3 className="font-bold text-slate-100 text-base uppercase tracking-wider mb-4 flex items-center">
              <FileText className="w-5 h-5 mr-2 text-blue-400" />
              Validated Export Documentation Package ({documents.length})
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {documents.map((doc) => (
                <div key={doc.id} className="p-3.5 bg-slate-900 border border-slate-800 rounded-xl flex items-center justify-between">
                  <div>
                    <div className="text-xs font-bold text-slate-200">{doc.document_type}</div>
                    <div className="text-[11px] text-slate-400 truncate max-w-[180px]">{doc.file_name}</div>
                  </div>
                  <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold rounded-full">
                    {doc.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right 1-Col: Audit Trail Timeline */}
        <div className="space-y-6">
          <div className="bg-slate-950/60 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <h3 className="font-bold text-slate-100 text-base uppercase tracking-wider mb-4 flex items-center">
              <Bot className="w-5 h-5 mr-2 text-emerald-400" />
              Audit Trail & Execution Log
            </h3>
            <Timeline events={auditEvents} />
          </div>
        </div>
      </div>

      {/* Modals */}
      <EvidenceModal
        isOpen={!!selectedFinding}
        onClose={() => setSelectedFinding(null)}
        finding={selectedFinding}
        overallStatus={shipment.status}
      />

      <HumanApprovalModal
        isOpen={showApprovalModal}
        onClose={() => setShowApprovalModal(false)}
        shipmentId={shipment.id}
        currentStatus={shipment.status}
        hasCriticalGaps={hasCriticalGaps}
        onApprovalComplete={loadAll}
      />

      <WhatIfModal
        isOpen={showWhatIfModal}
        onClose={() => setShowWhatIfModal(false)}
        shipmentId={shipment.id}
        currentStatus={shipment.status}
        currentScore={shipment.compliance_score}
      />
    </div>
  );
};
