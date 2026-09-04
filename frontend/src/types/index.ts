export type ShipmentStatus = 
  | 'CREATED' 
  | 'ANALYZING' 
  | 'REVIEW_REQUIRED' 
  | 'HOLD' 
  | 'READY_FOR_APPROVAL' 
  | 'APPROVED' 
  | 'REJECTED';

export interface ExporterProfile {
  exporter_id: string;
  name: string;
  origin_country: string;
  registration_number: string;
}

export interface Shipment {
  id: string;
  tracking_number: string;
  crop: string;
  variety: string;
  origin: string;
  destination: string;
  quantity_kg: number;
  deadline_days: number;
  created_at: string;
  updated_at: string;
  status: ShipmentStatus;
  exporter: ExporterProfile;
  compliance_score: number;
  assessment_confidence: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
}

export interface ComplianceFinding {
  id: string;
  category: 'REGULATORY' | 'FARM_RECORD' | 'DOCUMENT' | 'DEADLINE';
  title: string;
  severity: 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  status: 'PASS' | 'FAIL' | 'WARNING';
  reason: string;
  actual_data: string;
  applicable_requirement: string;
  source_evidence: string;
  source_url?: string;
  recommended_action: string;
  deadline_impact_days: number;
  resolved: boolean;
}

export interface ComplianceResult {
  shipment_id: string;
  overall_status: ShipmentStatus;
  decision_reason: string;
  compliance_score: number;
  assessment_confidence: number;
  risk_level: string;
  findings: ComplianceFinding[];
  summary: {
    pass: number;
    fail: number;
    warning: number;
  };
  evaluated_at: string;
}

export interface TimelineStep {
  step: number;
  label: string;
  status: 'COMPLETED' | 'PENDING' | 'SKIPPED' | 'SCHEDULED';
  description: string;
}

export interface RiskAssessment {
  shipment_id: string;
  risk_score: number;
  risk_level: string;
  deadline_days_remaining: number;
  estimated_remediation_days: number;
  deadline_buffer_days: number;
  timeline_steps: TimelineStep[];
}

export interface Document {
  id: string;
  shipment_id: string;
  document_type: string;
  file_name: string;
  uploaded_at: string;
  status: 'VALID' | 'EXPIRED' | 'CONTRADICTION' | 'MISSING' | 'PENDING';
  issue_date?: string;
  expiry_date?: string;
  extracted_fields: Record<string, any>;
}

export interface AuditEvent {
  id: string;
  shipment_id: string;
  event_type: string;
  agent_name?: string;
  title: string;
  description: string;
  metadata: Record<string, any>;
  timestamp: string;
}

export interface RemediationSummary {
  shipment_id: string;
  before: {
    status: string;
    compliance_score: number;
    critical_gaps: number;
    residue_value: number;
  };
  action: {
    type: string;
    document_name: string;
    new_residue_value: number;
    unit: string;
  };
  after: {
    status: string;
    compliance_score: number;
    critical_gaps: number;
    residue_value: number;
  };
  transition_summary: string;
}

export interface AgentInfo {
  name: string;
  description: string;
  role: string;
  type: string;
  status: string;
}
