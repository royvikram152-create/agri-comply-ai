import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertTriangle, RefreshCw, Play, Info, Search, FileCode, Check } from 'lucide-react';
import { Document, Shipment } from '../types';
import { uploadRealDocument, processShipment, reprocessShipment } from '../api/client';

interface DocumentUploadPanelProps {
  shipment: Shipment;
  documents: Document[];
  onRefresh: () => void;
}

export const DocumentUploadPanel: React.FC<DocumentUploadPanelProps> = ({
  shipment,
  documents,
  onRefresh,
}) => {
  const [selectedType, setSelectedType] = useState<string>('AUTO');
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [processingStep, setProcessingStep] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);
  const [expandedDocId, setExpandedDocId] = useState<string | null>(null);

  const handleFileUpload = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    setUploading(true);
    setError(null);

    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        await uploadRealDocument(shipment.id, file, selectedType === 'AUTO' ? undefined : selectedType);
      }
      onRefresh();
    } catch (err: any) {
      setError(err.message || 'File upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleProcess = async () => {
    setProcessing(true);
    setError(null);
    setProcessingStep(1);

    try {
      // Step simulation for 5 agents & firewall
      const interval = setInterval(() => {
        setProcessingStep((prev) => (prev < 6 ? prev + 1 : prev));
      }, 500);

      if (shipment.status === 'HOLD' || shipment.status === 'DOCUMENTS_PENDING') {
        await processShipment(shipment.id);
      } else {
        await reprocessShipment(shipment.id);
      }

      clearInterval(interval);
      setProcessingStep(6);
      setTimeout(() => {
        setProcessing(false);
        onRefresh();
      }, 600);
    } catch (err: any) {
      setError(err.message || 'Failed to process documents');
      setProcessing(false);
    }
  };

  const isReprocess = shipment.status === 'HOLD' || shipment.status === 'READY_FOR_APPROVAL' || shipment.status === 'APPROVED';

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between border-b border-slate-700 pb-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            <span>Document Bundle & Real Extraction Engine</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Upload PDF, DOCX, TXT, CSV, or JSON export documents. Extracted values and page provenance directly feed the Compliance Firewall.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={handleProcess}
            disabled={processing || uploading || documents.length === 0}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all shadow-lg flex items-center gap-2 ${
              processing || uploading || documents.length === 0
                ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-900/30'
            }`}
          >
            {processing ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Running 5 Agents...</span>
              </>
            ) : isReprocess ? (
              <>
                <RefreshCw className="w-4 h-4" />
                <span>Reprocess Shipment</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                <span>Process Documents</span>
              </>
            )}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Upload Drag & Drop Zone */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-1 space-y-3">
          <label className="block text-xs font-medium text-slate-400 uppercase tracking-wider">
            Target Document Type
          </label>
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 text-sm focus:outline-none focus:border-emerald-500"
          >
            <option value="AUTO">🤖 Auto-Detect Document Type</option>
            <option value="RESIDUE_TEST_REPORT">Pesticide Residue / Lab Test</option>
            <option value="PHYTOSANITARY_CERT">Phytosanitary Certificate</option>
            <option value="COMMERCIAL_INVOICE">Commercial Invoice</option>
            <option value="PACKING_LIST">Packing List</option>
            <option value="QUALITY_CERT">Quality Certificate</option>
            <option value="FARM_TREATMENT_RECORD">Farm Treatment Record</option>
            <option value="CERTIFICATE_OF_ORIGIN">Certificate of Origin</option>
            <option value="SUPPORTING_DOC">Supporting Document</option>
          </select>

          <label className="border-2 border-dashed border-slate-700 hover:border-emerald-500/50 bg-slate-900/50 hover:bg-slate-900 rounded-xl p-4 flex flex-col items-center justify-center text-center cursor-pointer transition-all">
            <UploadCloud className="w-8 h-8 text-emerald-400 mb-2" />
            <span className="text-sm font-medium text-slate-200">
              {uploading ? 'Parsing Bytes...' : 'Drag & Drop or Browse Files'}
            </span>
            <span className="text-xs text-slate-400 mt-1">Accepted: PDF, DOCX, TXT, CSV, JSON</span>
            <input
              type="file"
              multiple
              accept=".pdf,.docx,.txt,.csv,.json,.log"
              onChange={(e) => handleFileUpload(e.target.files)}
              className="hidden"
            />
          </label>
        </div>

        {/* Uploaded Documents List */}
        <div className="md:col-span-2 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
              Uploaded Documents ({documents.length})
            </span>
          </div>

          {documents.length === 0 ? (
            <div className="border border-slate-700/60 rounded-xl p-8 text-center bg-slate-900/30">
              <FileCode className="w-8 h-8 text-slate-500 mx-auto mb-2" />
              <p className="text-sm text-slate-400">No documents uploaded for this shipment yet.</p>
              <p className="text-xs text-slate-500 mt-1">Upload PDF lab tests, invoices, packing lists, or phytosanitary certificates.</p>
            </div>
          ) : (
            <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
              {documents.map((doc) => {
                const isExpanded = expandedDocId === doc.id;
                const format = doc.file_format || doc.file_name.split('.').pop()?.toUpperCase() || 'FILE';

                return (
                  <div
                    key={doc.id}
                    className="bg-slate-900/80 border border-slate-700/80 rounded-lg p-3 hover:border-slate-600 transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="px-2 py-1 bg-slate-800 border border-slate-700 text-xs font-mono font-semibold text-emerald-400 rounded">
                          {format}
                        </span>
                        <div>
                          <div className="text-sm font-medium text-slate-200 flex items-center gap-2">
                            <span>{doc.file_name}</span>
                            <span className="text-xs px-2 py-0.5 bg-slate-800 text-slate-400 rounded border border-slate-700">
                              {doc.document_type}
                            </span>
                          </div>
                          <div className="text-xs text-slate-400 mt-0.5 flex items-center gap-3">
                            <span>Uploaded: {doc.issue_date || 'Just now'}</span>
                            {doc.extracted_fields?.residue_value && (
                              <span className="text-emerald-400 font-mono">
                                Residue: {doc.extracted_fields.residue_value} mg/kg
                              </span>
                            )}
                            {doc.extracted_fields?.quantity_kg && (
                              <span className="text-indigo-400 font-mono">
                                Qty: {doc.extracted_fields.quantity_kg} kg
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      <button
                        onClick={() => setExpandedDocId(isExpanded ? null : doc.id)}
                        className="text-xs text-slate-400 hover:text-emerald-400 underline"
                      >
                        {isExpanded ? 'Hide Evidence' : 'View Extracted Evidence'}
                      </button>
                    </div>

                    {/* Expanded Detail & Provenance */}
                    {isExpanded && (
                      <div className="mt-3 pt-3 border-t border-slate-800 space-y-2 text-xs">
                        <div className="font-semibold text-slate-300">Extracted Structured Fields & Page Provenance:</div>
                        <div className="grid grid-cols-2 gap-2 bg-slate-950 p-3 rounded-lg border border-slate-800">
                          {Object.keys(doc.extracted_fields || {}).length === 0 ? (
                            <div className="text-slate-500 col-span-2">No fields extracted.</div>
                          ) : (
                            Object.entries(doc.extracted_fields).map(([k, v]) => {
                              const prov = doc.provenance_map?.[k];
                              return (
                                <div key={k} className="border-b border-slate-900 pb-1">
                                  <span className="text-slate-400 capitalize">{k.replace('_', ' ')}: </span>
                                  <span className="text-slate-200 font-mono font-semibold">{String(v)}</span>
                                  {prov?.source_page && prov.source_page !== 'N/A' && (
                                    <span className="ml-2 px-1.5 py-0.5 bg-slate-800 text-emerald-400 text-[10px] rounded border border-slate-700">
                                      {prov.source_page}
                                    </span>
                                  )}
                                </div>
                              );
                            })
                          )}
                        </div>
                        {doc.extracted_text && (
                          <div className="mt-2 text-slate-400 bg-slate-950 p-2 rounded border border-slate-800 font-mono text-[11px] max-h-24 overflow-y-auto">
                            <span className="text-slate-500 block mb-1">Raw Text Snippet:</span>
                            {doc.extracted_text}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Processing Animation Modal / Bar */}
      {processing && (
        <div className="bg-slate-900 border border-slate-700 rounded-xl p-4 space-y-3">
          <div className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center justify-between">
            <span>5-Agent Execution & Deterministic Firewall Pipeline</span>
            <span className="text-emerald-400 font-mono">{Math.round((processingStep / 6) * 100)}%</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-6 gap-2 text-xs">
            {[
              { step: 1, label: 'Exporter Agent' },
              { step: 2, label: 'Regulatory RAG' },
              { step: 3, label: 'Farm Record Check' },
              { step: 4, label: 'Document Assembly' },
              { step: 5, label: 'Gap Reporting' },
              { step: 6, label: 'Compliance Firewall' },
            ].map((st) => {
              const done = processingStep >= st.step;
              return (
                <div
                  key={st.step}
                  className={`p-2 rounded border text-center transition-all ${
                    done
                      ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300'
                      : 'bg-slate-950 border-slate-800 text-slate-500'
                  }`}
                >
                  <div className="flex items-center justify-center gap-1 font-semibold">
                    {done ? <Check className="w-3 h-3 text-emerald-400" /> : <div className="w-2 h-2 rounded-full bg-slate-600 animate-pulse" />}
                    <span>{st.label}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
