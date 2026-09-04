import { Shipment, ComplianceResult, RiskAssessment, Document, AuditEvent, RemediationSummary, AgentInfo } from '../types';

const getApiBase = (): string => {
  const envUrl = import.meta.env.VITE_API_URL;
  if (!envUrl) return '/api';
  const cleanUrl = envUrl.endsWith('/') ? envUrl.slice(0, -1) : envUrl;
  return cleanUrl.endsWith('/api') ? cleanUrl : `${cleanUrl}/api`;
};

const API_BASE = getApiBase();

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchShipments(): Promise<Shipment[]> {
  const res = await fetch(`${API_BASE}/shipments`);
  if (!res.ok) throw new Error('Failed to fetch shipments');
  return res.json();
}

export async function fetchShipment(id: string): Promise<Shipment> {
  const res = await fetch(`${API_BASE}/shipments/${id}`);
  if (!res.ok) throw new Error('Failed to fetch shipment');
  return res.json();
}

export async function createShipment(data: {
  crop: string;
  variety?: string;
  origin: string;
  destination: string;
  quantity_kg: number;
  deadline_days: number;
}): Promise<Shipment> {
  const res = await fetch(`${API_BASE}/shipments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create shipment');
  return res.json();
}

export async function analyzeShipment(id: string): Promise<{ compliance_result: ComplianceResult; shipment: Shipment }> {
  const res = await fetch(`${API_BASE}/shipments/${id}/analyze`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to analyze shipment');
  return res.json();
}

export async function remediateShipment(id: string, residueValue: number = 0.31): Promise<RemediationSummary> {
  const res = await fetch(`${API_BASE}/shipments/${id}/remediate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ residue_value: residueValue }),
  });
  if (!res.ok) throw new Error('Failed to remediate shipment');
  return res.json();
}

export async function fetchCompliance(id: string): Promise<{
  shipment: Shipment;
  compliance_result: ComplianceResult;
  risk_assessment: RiskAssessment;
  remediation_history?: RemediationSummary;
}> {
  const res = await fetch(`${API_BASE}/shipments/${id}/compliance`);
  if (!res.ok) throw new Error('Failed to fetch compliance');
  return res.json();
}

export async function fetchDocuments(id: string): Promise<Document[]> {
  const res = await fetch(`${API_BASE}/shipments/${id}/documents`);
  if (!res.ok) throw new Error('Failed to fetch documents');
  return res.json();
}

export async function fetchEvidenceChain(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/shipments/${id}/evidence`);
  if (!res.ok) throw new Error('Failed to fetch evidence chain');
  return res.json();
}

export async function fetchAuditTrail(id: string): Promise<AuditEvent[]> {
  const res = await fetch(`${API_BASE}/shipments/${id}/audit`);
  if (!res.ok) throw new Error('Failed to fetch audit trail');
  return res.json();
}

export async function submitHumanApproval(id: string, data: { reviewer: string; action: 'APPROVE' | 'REJECT' | 'REQUEST_CORRECTION'; comments: string }) {
  const res = await fetch(`${API_BASE}/shipments/${id}/approval`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errData = await res.json();
    throw new Error(errData.detail || 'Failed to submit approval');
  }
  return res.json();
}

export async function simulateWhatIf(id: string, data: { destination: string; deadline_days: number; residue_value: number }) {
  const res = await fetch(`${API_BASE}/shipments/${id}/what-if`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to run simulation');
  return res.json();
}

export async function fetchAgents(): Promise<AgentInfo[]> {
  const res = await fetch(`${API_BASE}/agents`);
  if (!res.ok) throw new Error('Failed to fetch agents');
  return res.json();
}
