# AGRICOMPLY AI
> **Agentic Export Documentation & Compliance Copilot**

AGRICOMPLY AI is an enterprise-grade prototype designed to automate agricultural export documentation analysis, check farm treatment records against international regulatory limits, validate export certificates, identify compliance gaps, and enforce a **deterministic compliance firewall** prior to shipping deadlines.

---

## 🏛 Core Architectural Principle

> **AI must NEVER directly decide legal compliance.**

- **AI & Specialized Agents**: Handle natural-language extraction, document field parsing, regulatory query retrieval, gap aggregation, and evidence explanation.
- **Deterministic Engine**: Performs hard PASS/FAIL evaluations, pesticide MRL numerical comparisons, document expiration checks, cross-document quantity contradiction detection, risk score calculation, and shipment status transitions.
- **Human Approval Gate**: A mandatory control layer requiring sign-off from a Senior Export Officer before dispatch.

---

## 🤖 5 Specialized Agents

1. **Exporter Interaction Agent**: Parses natural language exporter queries (e.g. *"I am exporting mangoes from India to the EU next week"*) and extracts structured crop, origin, destination, deadline, and quantity metadata.
2. **Regulatory Retrieval Agent**: Runs zero-cost local BM25/TF-IDF RAG search over an authoritative EU regulatory knowledge base, retaining source provenance (EC 396/2005 & EU 2019/2072).
3. **Farm Record Check Agent**: Evaluates farm treatment records and pesticide residue levels (e.g., active ingredient *Imidacloprid*) deterministically against EU Maximum Residue Limit (MRL) thresholds.
4. **Document Assembly Agent**: Validates Phytosanitary Certificates, Quality Certificates, Commercial Invoices, and Packing Lists for presence, expiration, and cross-document net weight consistency.
5. **Gap Reporting Agent**: Aggregates multi-agent findings, ranks severity (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), and generates evidence-backed remediation recommendations.

---

## 🛠 Technology Stack

- **Backend**: Python 3.13, FastAPI, Pydantic V2, SQLAlchemy, SQLite (local) / In-Memory Store (Vercel serverless).
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React icons.
- **RAG & Retrieval**: Local BM25/TF-IDF scoring engine with full provenance retention.
- **AI Abstraction**: Zero-cost fallback mode (works 100% without paid APIs) + optional Ollama local LLM integration.
- **Testing**: Pytest suite covering agents, compliance rules, and REST API endpoints.

---

## 🚀 How to Run Locally

### 1. Run Backend API
```bash
# Set PYTHONPATH to backend folder
$env:PYTHONPATH="backend"

# Launch Uvicorn server
backend/venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```
Backend running at: `http://localhost:8000` (Docs at `http://localhost:8000/docs`).

### 2. Run Frontend
```bash
cd frontend
npm run dev
```
Frontend running at: `http://localhost:3000`.

### 3. Run Backend Tests
```bash
$env:PYTHONPATH="backend"
backend/venv/Scripts/python -m pytest backend/tests
```

---

## 🎬 Primary Demo Sequence for Judging

### Primary Demo Scenario:
- **Crop**: Mango (*Alphonso*)
- **Origin**: India
- **Destination**: European Union
- **Shipment ID**: `SHP-MANGO-001`
- **Deadline**: 7 Days

### Step-by-Step Demo Flow:

1. **Initial Inspection (`HOLD` state)**:
   - Navigate to `SHP-MANGO-001`.
   - Observe **Shipment Readiness**: Status is `⚠ HOLD (CRITICAL GAPS)` and Compliance Index is `72.0 / 100`.
   - Observe the **5 Agents execution pipeline** status.
   - Farm Record Check Agent detected Imidacloprid residue at `0.82 mg/kg` exceeding the EU MRL limit of `0.50 mg/kg` by `+0.32 mg/kg`.

2. **Evidence Chain Provenance ("Why?" Button)**:
   - Click **"Why? / View Evidence"** on the MRL breach finding.
   - Inspect the complete 4-step provenance chain: `DECISION` → `ACTUAL DATA (0.82 mg/kg)` → `APPLICABLE RULE (EU EC 396/2005 <= 0.50 mg/kg)` → `OFFICIAL SOURCE (EFSA Database Entry #402)`.

3. **Phase E — Human Approval Gate (Blocked)**:
   - Click **Human Approval Gate**.
   - Observe that the **Approve** button is **disabled** with an alert: *"APPROVAL BLOCKED: Shipment has unresolved CRITICAL compliance gaps."*

4. **Phase H — "What Changed?" Remediation Workflow**:
   - Click **"Upload Passing Residue Test"** button on the "What Changed?" card.
   - The backend simulates uploading NABL lab report `0.31 mg/kg` (PASS) and re-runs the orchestrator.
   - Observe the real-time transition:
     - **BEFORE**: `HOLD` (Score: 72.0, 1 Critical Gap)
     - **ACTION**: `NABL_Lab_Residue_Test_Report_PASS.pdf` (0.31 mg/kg)
     - **AFTER**: `READY_FOR_APPROVAL` (Score: 100.0, 0 Critical Gaps)

5. **Phase E — Human Approval Granted**:
   - Click **Human Approval Gate** again.
   - Now **Approve** is enabled! Select **Approve** and submit sign-off comments.
   - Shipment status transitions cleanly to **`APPROVED FOR EXPORT`**.

6. **Audit Trail Timeline**:
   - View the Audit Trail timeline recording every agent execution, rule evaluation, upload, and human approval timestamp.

7. **Phase K — What-If Simulation**:
   - Click **What-If Simulation** to test alternative destinations and deadlines non-destructively.

---

## 📊 Implementation Status

| Feature | Status | Details |
|---|---|---|
| **5 Specialized Agents** | `IMPLEMENTED` | Exporter, Regulatory, Farm, Document, Gap agents |
| **Deterministic Compliance Firewall** | `IMPLEMENTED` | Hard rule engine & non-negotiable status logic |
| **EU RAG Knowledge Base** | `IMPLEMENTED` | Local BM25/TF-IDF retriever with provenance |
| **"What Changed?" Remediation** | `IMPLEMENTED` | Real backend transition from `HOLD` to `READY` |
| **Human Approval Gate** | `IMPLEMENTED` | Real control gate disabled during critical gaps |
| **Evidence Provenance Chain** | `IMPLEMENTED` | Full 4-step evidence trace modal |
| **Audit Trail Timeline** | `IMPLEMENTED` | Complete chronological audit log |
| **What-If Simulation Mode** | `IMPLEMENTED` | Non-destructive scenario modeling |
| **Vercel Serverless Config** | `IMPLEMENTED` | `vercel.json` + `api/index.py` zero-cost deployment |
| **Pytest Suite** | `IMPLEMENTED` | 11 unit tests covering agents, rules, and APIs |
