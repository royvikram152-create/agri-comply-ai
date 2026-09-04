# AGRICOMPLY AI

> **Agentic Agricultural Export Documentation & Deterministic Compliance Engine**

AGRICOMPLY AI is an enterprise-grade agentic compliance workflow system for international agricultural trade. It combines specialized autonomous AI agents, destination-specific Regulatory Retrieval-Augmented Generation (RAG), and a deterministic Compliance Firewall to validate export shipments against complex regulatory frameworks. By decoupling non-deterministic AI document extraction and knowledge retrieval from deterministic compliance evaluation, AGRICOMPLY AI eliminates AI hallucination risk in regulatory enforcement, provides end-to-end evidence provenance, supports non-destructive What-If simulations, and enforces strict human-in-the-loop approval gates before export clearance.

---

## Quick Start (30-Second Setup)

### 1. Clone & Set Up Backend
```bash
# Clone the repository
git clone https://github.com/royvikram152-create/agri-comply-ai.git
cd agri-comply-ai

# Activate Python environment & start FastAPI backend
$env:PYTHONPATH="backend"
backend/venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

### 2. Set Up & Launch Frontend
```bash
# In a new terminal window
cd frontend
npm install
npm run dev
```

### 3. Access Application
- **Frontend Web Application**: [http://localhost:3000](http://localhost:3000)
- **Backend Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Backend Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## Table of Contents
1. [Problem Statement](#2-problem-statement)
2. [Solution & Agentic Workflow](#3-solution)
3. [Full System Architecture](#4-full-system-architecture)
4. [Architecture Layer Breakdown](#5-architecture-explanation)
5. [Agent-by-Agent Architecture](#6-agent-by-agent-architecture)
6. [End-to-End Application Flow](#7-end-to-end-application-flow)
7. [Primary Demo Scenario (SHP-MANGO-001)](#8-primary-demo-scenario)
8. [What-If Simulation Engine](#9-what-if-simulation)
9. [Deterministic Compliance Firewall](#10-deterministic-compliance-firewall)
10. [Why Regulatory RAG?](#11-why-rag)
11. [Why NOT an LLM-Only Chatbot?](#12-why-not-an-llm-only-chatbot)
12. [Evidence Provenance Chain](#13-evidence-provenance)
13. [Deterministic Assessment Confidence](#14-assessment-confidence)
14. [State Machine Specification](#15-state-machine)
15. [Compliance Score vs. Assessment Confidence](#16-compliance-vs-confidence)
16. [Export Document Package Validation](#17-document-validation)
17. [Authoritative Regulatory Framework](#18-regulatory-sources)
18. [Technology Stack](#19-technology-stack)
19. [Repository Structure](#20-repository-structure)
20. [API Architecture & Endpoints](#21-api-architecture)
21. [Local Development Guide](#22-local-development)
22. [Automated Test Suite & Build Verification](#23-testing)
23. [Zero-Cost Serverless Deployment Architecture](#24-deployment)
24. [Zero-Cost Infrastructure Model](#25-zero-cost-architecture)
25. [Security & Reliability Principles](#26-security--reliability-principles)
26. [System Limitations & Boundary Conditions](#27-limitations)
27. [Future Roadmap](#28-future-scope)
28. [Hackathon Differentiators](#29-hackathon-differentiators)
29. [Judge Live Demo Sequence](#30-judge-demo-flow)
30. [Judge Technical Q&A](#31-judge-qa)
31. [One-Minute Elevator Pitch](#32-one-minute-pitch)
32. [2–3 Minute Spoken Demo Script](#33-23-minute-demo-script)
33. [Demo Credentials & Seed Data](#35-demo-credentials--data)
34. [Final Verified Project Status](#36-final-project-status)

---

## 2. Problem Statement

Cross-border agricultural trade requires navigate a complex web of international regulations, phytosanitary mandates, pesticide Maximum Residue Limits (MRLs), and mandatory documentation. Agricultural exporters and producers face severe operational friction:

* **Fragmented Regulatory Information**: Exporters must manually cross-reference destination country standards (e.g., EU Regulations, USDA APHIS, Codex Alimentarius), farm treatment logs, NABL-accredited lab analysis certificates, phytosanitary certificates, packing lists, and commercial invoices.
* **Asymmetric Destination Rules**: A chemical application or heat treatment accepted in one market may cause immediate border rejection, shipment destruction, or import bans in another (e.g., EU MRLs under Regulation (EC) No 396/2005).
* **Catastrophic Failure Costs**: A single missing document or residue threshold violation results in held containers, spoiled perishable cargo, heavy demurrage fees, and financial loss.
* **Failure of LLM-Only Chatbots**: Standard conversational LLMs cannot be trusted to enforce regulatory compliance. LLMs hallucinate numbers, misapply legal clauses, lack deterministic validation, cannot hold state, and fail to provide auditable legal provenance required by regulatory authorities.

AGRICOMPLY AI directly addresses the hackathon challenge by bridging agentic document processing with a zero-hallucination deterministic compliance firewall.

---

## 3. Solution

AGRICOMPLY AI replaces fragile manual verification with a multi-agent orchestration engine paired with a deterministic evaluation pipeline and human oversight gates.

### High-Level Agentic & Compliance Workflow

```text
Exporter / User
       │
       ▼
[ Exporter Interaction Agent ] ── (Extracts Intent & Metadata)
       │
       ▼
[ Agent Orchestrator Pipeline ]
       │
       ├─► [ Regulatory Retrieval Agent ] ──► (Queries EU Regulations Knowledge Base / RAG)
       │
       ├─► [ Farm Record Check Agent ] ───► (Evaluates Pesticide Residues & Active Ingredients)
       │
       ├─► [ Document Assembly Agent ] ───► (Validates Phytosanitary, Quality & Commercial Docs)
       │
       └─► [ Gap Reporting Agent ] ───────► (Identifies Gaps & Generates Remediation Steps)
       │
       ▼
[ Deterministic Compliance Firewall ] ── (Evaluates Rules, Computes Index & Assigns Risk)
       │
       ▼
[ State Machine Engine ] ──► Initial Status: HOLD (75/100)
       │
       ├─► [ Upload Remediation Evidence ] (Lab Test: 0.31 mg/kg)
       │         │
       │         ▼
       │   [ Re-Evaluation Pipeline ] ──► Upgraded Status: READY_FOR_APPROVAL (100/100)
       │         │
       │         ▼
       │   [ Human Approval Gate ] ───► Final Status: APPROVED_FOR_EXPORT
       │
       └─► [ Non-Destructive What-If Simulation Engine ] (Test hypothetical scenarios safely)
```

### The 5 Specialized Autonomous Agents
1. **Exporter Interaction Agent**: Parses exporter natural language inputs, shipment metadata, consignment sizes, destination parameters, and urgency constraints.
2. **Regulatory Retrieval Agent**: Executes BM25 keyword RAG search over authoritative regulatory text (e.g., EUR-Lex, EU Pesticides Database, Regulation (EC) No 396/2005) to pull exact legal requirements and provenance links.
3. **Farm Record Check Agent**: Validates pre-harvest farm treatment logs, active ingredient applications, spray dates, pre-harvest intervals (PHI), and laboratory residue metrics against target limits.
4. **Document Assembly Agent**: Performs cross-document integrity checks on Phytosanitary Certificates, Quality Certificates, Commercial Invoices, Packing Lists, and Residue Test Reports for presence, validity, and expiration dates.
5. **Gap Reporting Agent**: Analyzes compliance failures, flags missing mandatory evidence, ranks critical vs. warning gaps, and produces clear, actionable remediation protocols for the exporter.

---

## 4. Full System Architecture

```text
+-----------------------------------------------------------------------------------+
|                                 FRONTEND LAYER                                    |
|   +---------------------------------------------------------------------------+   |
|   |                       React 18 + Vite + TypeScript                        |   |
|   |   - Dashboard View           - Detailed Evidence Drawer                   |   |
|   |   - Interactive Flow Engine  - Non-Destructive What-If Modal              |   |
|   |   - Human Approval Gate      - Audit Trail & Provenance Timeline          |   |
|   |   - Tailwind CSS + Lucide Icons + Radix UI Primitives                     |   |
|   +---------------------------------------------------------------------------+   |
+------------------------------------------┬----------------------------------------+
                                           │ HTTP / REST API (JSON)
                                           ▼
+-----------------------------------------------------------------------------------+
|                                  BACKEND API LAYER                                |
|   +---------------------------------------------------------------------------+   |
|   |                             FastAPI Framework                             |   |
|   |   /api/v1/shipments      /api/v1/compliance      /api/v1/documents        |   |
|   |   /api/v1/remediate      /api/v1/what-if         /api/v1/approvals        |   |
|   |   /api/v1/agents         /api/v1/audit           /api/v1/health           |   |
|   +---------------------------------------------------------------------------+   |
+------------------------------------------┬----------------------------------------+
                                           │
                                           ▼
+-----------------------------------------------------------------------------------+
|                              AGENT ORCHESTRATION LAYER                            |
|   +---------------------------------------------------------------------------+   |
|   |                        Multi-Agent Orchestrator                           |   |
|   |   1. Exporter Interaction Agent (Metadata Parsing & Natural Language)     |   |
|   |   2. Regulatory Retrieval Agent (BM25 RAG & Legal Citation Lookup)       |   |
|   |   3. Farm Record Check Agent    (Chemical Residue & Treatment Logs)       |   |
|   |   4. Document Assembly Agent    (Cross-Document Package Validation)       |   |
|   |   5. Gap Reporting Agent        (Remediation Protocol Ranking)            |   |
|   +---------------------------------------------------------------------------+   |
+------------------------------------------┬----------------------------------------+
                                           │
                    +----------------------+----------------------+
                    │                                             │
                    ▼                                             ▼
+---------------------------------------+     +-------------------------------------+
|      REGULATORY KNOWLEDGE LAYER       |     |       COMPLIANCE & RISK LAYER       |
|   - Local Regulatory RAG Knowledge    |     |   - Deterministic Rule Engine       |
|   - EUR-Lex & EU Pesticides Database  |     |   - Hard Compliance Firewall        |
|   - Official Citation Provenance      |     |   - State Machine Transition Engine |
|   - Reg (EC) 396/2005 & 2019/2072     |     |   - Assessment Confidence Engine    |
+---------------------------------------+     +-------------------------------------+
                    │                                             │
                    +----------------------+----------------------+
                                           │
                                           ▼
+-----------------------------------------------------------------------------------+
|                         HUMAN CONTROL & OBSERVABILITY LAYER                        |
|   +---------------------------------------------------------------------------+   |
|   |   - Human Approval Gate (Strictly blocks export on critical gaps)         |   |
|   |   - Complete Audit Trail (Immutable event log of all actions/agent runs)  |   |
|   |   - Source Provenance Links (EFSA / EUR-Lex legal text mapping)           |   |
|   |   - Non-Destructive What-If Simulation Sandbox Engine                     |   |
|   +---------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------+
```

---

## 5. Architecture Explanation

* **Frontend Layer**: Built with React 18, Vite, TypeScript, and Tailwind CSS. It provides a real-time reactive UI displaying compliance indices, confidence scores, evidence provenance drawers, interactive remediation triggers, human approval controls, and What-If simulation modals.
* **API Layer**: Implemented using FastAPI with Pydantic validation schemas. Exposes RESTful endpoints handling shipment analysis, evidence retrieval, remediation re-evaluations, human approval submissions, and audit trail queries.
* **Agent Orchestration Layer**: Manages the multi-agent pipeline. Executes agents sequentially and in parallel, collating structured findings from exporter inputs, regulatory corpora, farm records, and export documents.
* **Regulatory RAG Layer**: Uses a lightweight BM25 retrieval algorithm over indexed regulatory knowledge bases (e.g., EU Fresh Mango Regulations). Provides direct legal citations without relying on LLM internal parametric memory.
* **Farm Evidence Layer**: Inspects farm spray logs and chemical application data (e.g., active ingredient application, dosage rates, spray dates) and evaluates chemical residue test figures against operational thresholds.
* **Document Layer**: Inspects the export document bundle, verifying presence, validity dates, issue dates, and cross-document field consistency across mandatory certificates.
* **Compliance Firewall**: The core deterministic rule engine. Enforces binary PASS/FAIL criteria on critical rules (e.g., MRL thresholds, mandatory certificate checks). It computes the 0–100 Compliance Score and dictates state machine eligibility independently of AI confidence or LLM prose.
* **Human Approval Layer**: Ensures final legal clearance for export remains strictly under human control. Human approval is programmatically blocked by the system whenever unresolved critical compliance gaps exist.
* **Audit/Evidence Layer**: Persists an immutable log of all pipeline executions, evidence sources, legal citations, document uploads, remediation transitions, and human approval signatures.

---

## 6. Agent-by-Agent Architecture

### 1. Exporter Interaction Agent
* **Purpose**: Serves as the front door for exporter input parsing and shipment metadata structuring.
* **Inputs**: Raw shipment creation payloads (crop, variety, origin, destination, consignment quantity, target deadline, exporter profile).
* **Processing**: Validates schema completeness, formats geographic trade pairs (e.g., India $\rightarrow$ EU), and assigns operational urgency ratings.
* **Outputs**: Structured `Shipment` object with initialized metadata and baseline tracking IDs.
* **Interaction**: Passes structured shipment metadata to the Regulatory Retrieval Agent and Orchestrator.
* **Separation Rationale**: Isolates raw user input ingestion and natural language handling from downstream regulatory analysis.

### 2. Regulatory Retrieval Agent
* **Purpose**: Retrieves target destination regulatory requirements and authoritative legal citations using RAG.
* **Inputs**: Shipment crop (`Mango`), origin (`India`), destination (`European Union`).
* **Processing**: Performs BM25 score matching against indexed legal text (EUR-Lex, EU Pesticides Database, Regulation (EC) No 396/2005, Regulation (EU) 2019/2072).
* **Outputs**: Array of matching regulatory requirements, legal clause references, official citation URLs, and baseline operational thresholds.
* **Interaction**: Feeds ground-truth regulatory constraints to the Farm Record Agent, Document Agent, and Compliance Engine.
* **Separation Rationale**: Decouples legal knowledge retrieval from compliance evaluation, allowing knowledge base updates without touching core rule logic.

### 3. Farm Record Check Agent
* **Purpose**: Audits farm chemical treatment records and chemical residue analysis reports.
* **Inputs**: Farm treatment logs, active ingredient applications (`Imidacloprid`), chemical residue test results (`0.82 mg/kg` or remediated `0.31 mg/kg`).
* **Processing**: Performs deterministic comparison against operational evaluation thresholds (e.g., `0.50 mg/kg` demo threshold).
* **Outputs**: Structured chemical compliance findings, residue delta values, active ingredient status, and MRL compliance flags.
* **Interaction**: Sends structured chemical findings to the Compliance Firewall and Gap Reporting Agent.
* **Separation Rationale**: Keeps agricultural chemical domain logic separate from document assembly and general regulatory retrieval.

### 4. Document Assembly Agent
* **Purpose**: Validates the presence, validity, and cross-document consistency of required trade documentation.
* **Inputs**: Uploaded shipment documents (`PHYTOSANITARY_CERT`, `QUALITY_CERT`, `COMMERCIAL_INVOICE`, `PACKING_LIST`, `RESIDUE_TEST_REPORT`).
* **Processing**: Verifies document type coverage against destination mandatory document sets, checks expiry dates against shipment deadlines, and validates document status.
* **Outputs**: Document package completeness metrics, missing document lists, expired document warnings, and validation findings.
* **Interaction**: Supplies document validation results to the Compliance Firewall and Assessment Confidence Engine.
* **Separation Rationale**: Separates administrative export documentation checking from agricultural lab/farm record verification.

### 5. Gap Reporting Agent
* **Purpose**: Ranks compliance failures and formulates structured remediation protocols.
* **Inputs**: Failed findings from Farm Record Agent, missing document alerts from Document Agent, and rule violations from Compliance Engine.
* **Processing**: Categorizes gaps into `CRITICAL` (blocks export) vs. `WARNING` (advisory), ranks remediation priority, and generates step-by-step resolution instructions.
* **Outputs**: Prioritized compliance gap reports and actionable exporter remediation recommendations.
* **Interaction**: Formats output for display in the frontend UI and logs remediation steps in the Audit Trail.
* **Separation Rationale**: Keeps user-facing advisory and remediation planning separate from strict, neutral rule evaluation.

---

## 7. End-to-End Application Flow

1. **Dashboard Entry**: User opens the AGRICOMPLY AI web interface at `http://localhost:3000`.
2. **Select Shipment**: User clicks on seed shipment `SHP-MANGO-001` (Alphonso Mangoes, India $\rightarrow$ EU).
3. **Inspect Readiness**: User reviews initial status badge (**`HOLD`**), Compliance Score (**75/100**), and Assessment Confidence (**94%**).
4. **Trigger Orchestration**: System executes the 5-agent pipeline via `POST /api/v1/shipments/SHP-MANGO-001/analyze`.
5. **Regulatory Evidence Retrieval**: Regulatory Agent retrieves Regulation (EC) No 396/2005 rules and EU Pesticides Database citations.
6. **Farm Record Audit**: Farm Agent detects initial Imidacloprid residue level of **0.82 mg/kg** exceeding the demo evaluation threshold (**0.50 mg/kg**).
7. **Document Assembly Check**: Document Agent verifies Phytosanitary Certificate, Commercial Invoice, Packing List, and Quality Certificate.
8. **Gap Detection**: Gap Agent flags `CRIT-MRL-01`: *Imidacloprid residue (0.82 mg/kg) exceeds threshold*.
9. **Deterministic Evaluation**: Compliance Firewall evaluates rules, sets score to 75/100, assigns `HIGH` risk level, and enforces `HOLD` status.
10. **Human Approval Blocked**: User attempts to click "Approve Shipment"; system displays error: *"Human Approval BLOCKED: Cannot approve shipment while 1 critical compliance gap exists."*
11. **Inspect Evidence & Provenance**: User opens "View Evidence" drawer to inspect actual data (`0.82 mg/kg`), legal requirement, official citation source URL, and exact rule evaluation.
12. **Simulate/Upload Remediation**: User clicks "Upload Passing Residue Test" to simulate uploading an NABL lab report showing **0.31 mg/kg**.
13. **Re-Evaluation Pipeline**: Backend receives `POST /api/v1/shipments/SHP-MANGO-001/remediate`, updates farm records, appends valid lab document, re-runs orchestrator pipeline.
14. **Status Upgrade**: Compliance Firewall re-evaluates `CRIT-MRL-01` to `PASS`, upgrades score to **100/100**, sets risk level to `LOW`, and transitions status to **`READY_FOR_APPROVAL`**.
15. **Human Approval Gate**: Exporter Compliance Officer reviews cleared evidence, inputs reviewer name ("Inspector Vikram Roy"), adds comments, and clicks "Approve Shipment".
16. **Final Clearance**: Backend handles `POST /api/v1/shipments/SHP-MANGO-001/approval`, updating status to **`APPROVED_FOR_EXPORT`**.
17. **What-If Simulation**: User clicks "What-If Simulation" modal and tests a hypothetical residue value of `0.82 mg/kg`. The simulation outputs `HOLD` (72/100 score) while leaving the real shipment state safely **`APPROVED_FOR_EXPORT`** (100/100).
18. **Audit Trail Verification**: User opens "Audit Trail" tab to review the complete, timestamped, immutable event timeline covering creation, initial hold, remediation, re-evaluation, and final human approval.

---

## 8. Primary Demo Scenario

The application includes a fully pre-configured seed scenario (`SHP-MANGO-001`) modeled after real-world Indian fresh mango exports to the European Union.

### Initial Consignment State
* **Shipment ID**: `SHP-MANGO-001`
* **Exporter**: Royal Agri Exports Ltd (`EXP-IND-908`, APEDA Reg: `APEDA/2024/IND-908`)
* **Commodity**: Fresh Mango (Variety: Alphonso)
* **Trade Route**: India (`IND`) $\rightarrow$ European Union (`EU`)
* **Quantity**: 2,000 kg
* **Deadline**: 7 Days
* **Initial Residue**: Imidacloprid @ **0.82 mg/kg**
* **Initial Compliance Index**: **75 / 100**
* **Initial Risk Level**: `HIGH`
* **Initial Status**: **`HOLD`**
* **Critical Gap**: Rule `CRIT-MRL-01` Failed (Residue 0.82 mg/kg > 0.50 mg/kg demo evaluation limit)

### Remediation Action
* **Action**: Exporter submits updated NABL-accredited Laboratory Residue Analysis Report (`NABL_Lab_Residue_Test_Report_PASS.pdf`).
* **New Residue Measurement**: Imidacloprid @ **0.31 mg/kg**
* **Re-Evaluation Compliance Index**: **100 / 100**
* **Re-Evaluation Risk Level**: `LOW`
* **Upgraded Status**: **`READY_FOR_APPROVAL`**

### Final Human Clearance
* **Action**: Compliance Officer performs formal review and executes human approval.
* **Final Status**: **`APPROVED_FOR_EXPORT`**

> [!NOTE]
> **Demo Data Transparency**: The threshold value of `0.50 mg/kg` used in the demo scenario serves as an operational demo evaluation limit. The official legal EU MRL framework is established under Regulation (EC) No 396/2005.

---

## 9. What-If Simulation

AGRICOMPLY AI features a dedicated, non-destructive What-If Simulation Engine (`POST /api/v1/shipments/{id}/what-if`).

```text
                                [ User What-If Request ]
                                           │
                                           ▼
                       [ Non-Destructive Simulation Engine ]
                                           │
             +-----------------------------+-----------------------------+
             │                                                           │
             ▼                                                           ▼
[ Evaluates Hypothetical Inputs ]                        [ Reads Real Shipment State ]
- Target Residue: 0.82 mg/kg                              - Status: APPROVED_FOR_EXPORT
- Destination: European Union                             - Score: 100/100
- Deadline: 7 Days                                        - Real Confidence: 94%
             │                                                           │
             ▼                                                           │
[ Simulated Outcome Calculated ]                                         │
- Status: HOLD                                                           │
- Score: 72/100                                                          │
- Sim Confidence: 89%                                                    │
             │                                                           │
             +-----------------------------+-----------------------------+
                                           │
                                           ▼
                       [ Returns Both in API Response ]
                       - Real State: UNMUTATED (APPROVED)
                       - Simulated State: HOLD (72/100)
```

### Key Properties
* **Zero Side-Effects**: Runs hypothetical parameter adjustments against an isolated instance of the compliance engine without mutating the persisted database state.
* **Immediate Feedback**: Exporters can instantly test "What happens if residue is 0.82 mg/kg?" or "What if the destination changes?" without risking shipment status rollback.
* **Demonstrated State Isolation**: Even when an approved shipment runs a What-If simulation producing `HOLD`, the actual live shipment remains securely **`APPROVED_FOR_EXPORT`**.

---

## 10. Deterministic Compliance Firewall

A cornerstone of AGRICOMPLY AI’s architecture is the strict segregation between AI-driven task execution and deterministic regulatory decision-making.

```text
[ AI & RAG LAYER ]                            [ DETERMINISTIC FIREWALL LAYER ]
- Parse exporter text                         - Evaluate hard numerical rules
- Retrieve legal text (BM25)    ──► Structured ──► - Execute binary PASS/FAIL checks  ──► [ Compliance Score: 100/100 ]
- Extract document fields           Facts     - Check required document sets      ──► [ Status: READY_FOR_APPROVAL ]
- Summarize findings                          - Enforce state transitions
                                                           │
                                                           ▼
                                               [ HUMAN APPROVAL GATE ]
                                               - Final Inspector Sign-off        ──► [ Status: APPROVED_FOR_EXPORT ]
```

### Architectural Guarantees
1. **Zero Hallucination in Compliance**: LLMs and AI agents are **NEVER** permitted to calculate scores, declare compliance, or issue export clearance directly.
2. **Explicit Rule Specifications**: Rules are coded as deterministic Python evaluations (e.g., `residue_value <= threshold`, `document_type in uploaded_docs`, `expiry_date >= deadline`).
3. **Auditable Decision Boundaries**: Every score deduction and status flag is tied directly to a named rule ID (`CRIT-MRL-01`, `CRIT-DOC-01`, `WARN-EXP-01`).

---

## 11. Why Regulatory RAG?

AGRICOMPLY AI employs Retrieval-Augmented Generation over a curated local regulatory knowledge base rather than relying on LLM parametric memory.

* **Destination Specificity**: Import requirements depend heavily on exact origin-destination trade pairs. RAG dynamically injects precise destination legal requirements into the pipeline context.
* **Ground-Truth Citations**: RAG retrieves exact legal references (e.g., *Regulation (EC) No 396/2005 Article 18*, *Regulation (EU) 2019/2072 Annex VII*), enabling direct link provenance for auditors.
* **Mitigation of Hallucination**: AI models frequently invent numerical limits or cite non-existent legal clauses. RAG grounds all reasoning strictly in fetched authoritative text.
* **Dynamic Updateability**: Regulatory frameworks change frequently. RAG allows updating the regulatory corpus instantly without re-training or fine-tuning AI models.

---

## 12. Why NOT an LLM-Only Chatbot?

| Feature / Capability | Standard LLM Chatbot | AGRICOMPLY AI Engine |
| :--- | :---: | :---: |
| **Regulatory Grounding** | Generic parametric memory (prone to hallucination) | Direct BM25 RAG over official legal corpora |
| **Compliance Decision Logic** | Non-deterministic text generation | Deterministic Rule Firewall & Hard Threshold Engine |
| **Evidence Provenance** | None (cannot trace sources reliably) | Full provenance chain linked to legal database URLs |
| **State Management** | Ephemeral chat transcript | Formally defined state machine with persisted history |
| **Document Validation** | Text summary only | Cross-document package verification & expiry matching |
| **Remediation Workflow** | Generic suggestions | Automated gap ranking & step-by-step re-evaluation |
| **Human Approval Control** | None (AI makes unvalidated claims) | Programmatic Human Approval Gate blocking invalid sign-offs |
| **Audit Trail** | Unstructured chat history | Immutable, structured audit event log |
| **What-If Simulation** | Textual guesswork | Isolated, non-destructive simulation engine |
| **Assessment Confidence** | Arbitrary text output | Multi-dimensional evidence quality calculation (0–100%) |
| **Reproducibility** | Variable across runs (temperature dependent) | 100% deterministic & reproducible rule evaluations |

---

## 13. Evidence Provenance

Every compliance evaluation result displayed by AGRICOMPLY AI contains an auditable, end-to-end evidence provenance chain.

```text
[ Final Decision: FAIL / HOLD ]
             │
             ▼
[ Actual Evidence Data: Residue = 0.82 mg/kg (Active Ingredient: Imidacloprid) ]
             │
             ▼
[ Applicable Rule: CRIT-MRL-01 (Operational Threshold: 0.50 mg/kg) ]
             │
             ▼
[ Authoritative Legal Source: Regulation (EC) No 396/2005 (EU Harmonised MRL Framework) ]
             │
             ▼
[ Source Badge: OFFICIAL SOURCE / EU Pesticides Database ]
```

### Visual Source Badging
* **`OFFICIAL SOURCE`**: Applied to verified legal citations sourced from official regulatory bodies (e.g., EUR-Lex, EFSA, EU Pesticides Database).
* **`DEMO DATA`**: Applied to operational demo thresholds or simulated test data to maintain complete legal clarity and transparency.

---

## 14. Assessment Confidence

AGRICOMPLY AI implements a deterministic `AssessmentConfidenceEngine` (`backend/app/compliance/confidence_engine.py`) that calculates an explicit **AI Assessment Confidence** percentage metric (0–100%).

### Multi-Dimensional Scoring Formula

$$\text{Confidence Score} = \text{Meta} + \text{RAG} + \text{Farm} + \text{Doc} + \text{Provenance}$$

| Evidence Dimension | Maximum Weight | Evaluated Parameters |
| :--- | :---: | :--- |
| **1. Metadata Completeness** | **20 Points** | Crop, origin, destination, consignment weight, deadline, exporter ID |
| **2. Regulatory RAG Coverage** | **25 Points** | Presence and depth of matching legal corpus findings |
| **3. Farm Record Quality** | **20 Points** | Active ingredient tracking, spray logs, chemical residue metrics |
| **4. Document Set Package** | **20 Points** | Completeness of mandatory export certificate set (4/4 docs) |
| **5. Citation Quality** | **9 Points** | Direct mapping to verified EUR-Lex / EFSA legal database records |
| **TOTAL MAX CONFIDENCE** | **94% (Seed)** | *(Primary demo seed score: $20 + 25 + 20 + 20 + 9 = \mathbf{94\%}$)* |

> [!IMPORTANT]
> **Metric Semantics & Tooltip Disclaimer**: Assessment Confidence measures the *completeness and structural quality of available evidence*. It **DOES NOT** represent a probability of legal compliance, does **NOT** predict regulatory approval, and is **STRICTLY ISOLATED** from the deterministic Compliance Firewall.

---

## 15. State Machine

The lifecycle of export shipments is governed by a strict, single-direction state machine.

```text
   +-------------------+
   |      CREATED      |
   +---------┬---------+
             │
             ▼
   +-------------------+       Unresolved Critical Gaps
   |       HOLD        | ◄──────────────────────────────────+
   +---------┬---------+                                    │
             │                                              │
             │ Upload Passing Evidence                      │
             ▼                                              │ Re-Evaluation
   +-------------------+                                    │ Discovers
   | READY_FOR_APPROVAL| ───────────────────────────────────+ Critical Gap
   +---------┬---------+
             │
             │ Human Approval Executed
             ▼
   +-------------------+
   |APPROVED_FOR_EXPORT|  (Terminal Final Clearance)
   +-------------------+
```

### State Definitions & Transition Criteria
* **`CREATED`**: Initial shipment entry prior to orchestration execution.
* **`HOLD`**: Assigned when one or more `CRITICAL` compliance gaps exist (e.g., residue exceeding threshold). Human approval is programmatically blocked.
* **`READY_FOR_APPROVAL`**: Assigned when all `CRITICAL` gaps are cleared. Human Approval Gate is unlocked.
* **`APPROVED_FOR_EXPORT`**: Assigned only when an authorized human compliance officer signs off via the Approval Gate.
* **`REJECTED`**: Assigned if human inspector explicitly rejects shipment clearance.

*Note: The What-If Simulation Engine executes in an isolated sandbox and never mutates this state machine.*

---

## 16. Compliance vs. Confidence

AGRICOMPLY AI maintains a clear operational distinction between Compliance Index, Assessment Confidence, Risk Level, and Final Decision:

| Metric | Primary Purpose | Scale / Type | Deterministic? | Influences Approval? |
| :--- | :--- | :--- | :---: | :---: |
| **Compliance Index** | Quantitative measure of rule satisfaction | 0 – 100 Score | **YES** | **YES** (Must be 100 for Ready status) |
| **Assessment Confidence** | Structural completeness of evidence package | 0 – 100 % | **YES** | **NO** (Informational UI metric only) |
| **Risk Level** | Categorical risk rating for inspection probability | `LOW` / `MEDIUM` / `HIGH` | **YES** | **YES** |
| **Final Decision** | Regulatory clearance status | `HOLD` / `APPROVED_FOR_EXPORT` | **YES** | **YES** (Enforced by State Machine) |

### Example Seed Shipment Values
* **Compliance Index**: `100 / 100` *(post-remediation)*
* **AI Assessment Confidence**: `94%`
* **Risk Level**: `LOW`
* **Final Decision**: `APPROVED_FOR_EXPORT`

---

## 17. Document Validation

The Document Assembly Agent validates five core agricultural export document types:

1. **`PHYTOSANITARY_CERT`**: Phytosanitary Certificate issued by National Plant Protection Organization (NPPO/PQIS).
2. **`QUALITY_CERT`**: GlobalGAP / Export Quality Inspection Certificate.
3. **`COMMERCIAL_INVOICE`**: Export Commercial Invoice specifying exporter/consignee details.
4. **`PACKING_LIST`**: Consignment packing breakdown, net/gross weight, and packaging types.
5. **`RESIDUE_TEST_REPORT`**: NABL-accredited Laboratory Pesticide Residue Test Analysis Report.

### Verification Logic
* **Presence Validation**: Verifies all mandatory document types required for the target trade pair are present.
* **Temporal Validation**: Verifies document issue date $\le$ current date and expiry date $\ge$ shipment deadline.
* **Status Enforcement**: Flags missing, expired, or invalid documents as compliance gaps.

---

## 18. Regulatory Sources

AGRICOMPLY AI references official European Union plant health and pesticide regulatory frameworks:

* **Regulation (EC) No 396/2005**: European Parliament and Council Regulation on maximum residue levels of pesticides in or on food and feed of plant and animal origin.
* **Regulation (EU) 2019/2072**: Commission Implementing Regulation establishing uniform conditions for the implementation of Regulation (EU) 2016/2031 on protective measures against pests of plants.
* **Regulation (EU) 2017/625**: Official Controls Regulation governing border control posts and official export checks.
* **EU Pesticides Database & EFSA**: European Food Safety Authority scientific evaluations and harmonized residue databases.

---

## 19. Technology Stack

| Component | Technology | Version / Specification |
| :--- | :--- | :--- |
| **Frontend Framework** | React | `18.3.1` |
| **Frontend Build Tool** | Vite | `5.4.21` |
| **Language (Frontend)** | TypeScript | `5.5.3` |
| **Styling & UI** | Tailwind CSS + Lucide Icons | `3.4.1` / `0.344.0` |
| **Backend Framework** | FastAPI | `0.115.0` |
| **Language (Backend)** | Python | `3.13.11` |
| **Data Validation** | Pydantic | `2.9.0` |
| **WSGI / ASGI Server** | Uvicorn | `0.30.0` |
| **RAG Retriever** | Local BM25 Engine | Custom Python Implementation |
| **Automated Testing** | Pytest | `9.1.1` |
| **Deployment Platform** | Vercel Serverless | `@vercel/python` + Static Hosting |
| **Version Control** | Git / GitHub | `main` branch |

---

## 20. Repository Structure

```text
agri-comply-ai/
├── README.md                           # Main Project Documentation
├── DEPLOYMENT.md                       # Deployment Guide & Architecture Setup
├── vercel.json                         # Vercel Monorepo Deployment Configuration
├── api/
│   └── index.py                        # Vercel Serverless Gateway Entrypoint
├── backend/
│   ├── requirements.txt                # Python Backend Dependencies
│   ├── vercel.json                     # Standalone Backend Deployment Config
│   ├── app/
│   │   ├── main.py                     # FastAPI Application Initialization & Routes
│   │   ├── config.py                   # Application Settings & Environment Config
│   │   ├── agents/                     # 5 Specialized Autonomous Agents
│   │   │   ├── base_agent.py           # Base Agent Class Definition
│   │   │   ├── exporter_agent.py       # Exporter Interaction Agent
│   │   │   ├── regulatory_agent.py     # Regulatory Retrieval Agent
│   │   │   ├── farm_record_agent.py    # Farm Record Check Agent
│   │   │   ├── document_agent.py       # Document Assembly Agent
│   │   │   └── gap_reporting_agent.py  # Gap Reporting Agent
│   │   ├── api/                        # FastAPI REST API Routers
│   │   │   ├── health.py               # GET /api/v1/health
│   │   │   ├── shipments.py            # GET/POST /api/v1/shipments, /remediate, /what-if
│   │   │   ├── documents.py            # GET/POST /api/v1/shipments/{id}/documents
│   │   │   ├── compliance.py           # GET /api/v1/shipments/{id}/compliance, /evidence
│   │   │   ├── agents.py               # GET /api/v1/agents
│   │   │   ├── approvals.py            # POST /api/v1/shipments/{id}/approval
│   │   │   └── audit.py                # GET /api/v1/shipments/{id}/audit
│   │   ├── compliance/                 # Deterministic Decision & Rule Firewall Engine
│   │   │   ├── rule_engine.py          # Deterministic Compliance Firewall
│   │   │   ├── decision_engine.py      # Status & Score Evaluator
│   │   │   ├── risk_engine.py          # Categorical Risk Assessment Engine
│   │   │   └── confidence_engine.py    # Deterministic Assessment Confidence Engine
│   │   ├── database/                   # Seed Data & In-Memory Store
│   │   │   └── store.py                # Database Store & Seed Shipment Storage
│   │   ├── models/                     # Pydantic Schemas & Domain Models
│   │   │   ├── shipment.py             # Shipment & Exporter Schemas
│   │   │   ├── compliance.py           # Compliance & Rule Finding Schemas
│   │   │   ├── document.py             # Document & Expiry Schemas
│   │   │   ├── farm_record.py          # Farm Treatment & Residue Schemas
│   │   │   ├── approval.py             # Human Approval Schemas
│   │   │   └── audit.py                # Audit Trail Event Schemas
│   │   ├── orchestration/              # Multi-Agent Orchestration Engine
│   │   │   └── orchestrator.py         # Agent Pipeline Orchestrator
│   │   └── rag/                        # Knowledge Base & Retrieval System
│   │       ├── knowledge_base.py       # EU Regulatory Text Corpus
│   │       └── retriever.py            # BM25 RAG Retriever Engine
│   └── tests/                          # Automated Pytest Test Suite
│       ├── test_agents.py              # Agent Unit Tests
│       ├── test_api.py                 # REST API & Integration Tests
│       └── test_compliance.py          # Compliance Firewall Unit Tests
└── frontend/
    ├── package.json                    # Node.js Dependencies & Scripts
    ├── vite.config.ts                  # Vite Bundler & Proxy Configuration
    ├── tailwind.config.js              # Tailwind CSS Styling Rules
    ├── src/
    │   ├── App.tsx                     # Main Application Shell & Navigation
    │   ├── main.tsx                    # React Entrypoint Rendering
    │   ├── api/                        # API Client Services
    │   │   └── client.ts               # Axios/Fetch REST API Client Wrapper
    │   ├── components/                 # Reusable UI Components
    │   │   ├── Navbar.tsx              # Top Header Navigation Bar
    │   │   ├── WhatIfModal.tsx         # What-If Simulation Sandbox Modal
    │   │   ├── EvidenceDrawer.tsx      # Evidence Provenance Drawer Modal
    │   │   └── RemediationModal.tsx    # Residue Test Upload Remediation Modal
    │   ├── pages/                      # Application Page Views
    │   │   ├── Dashboard.tsx           # Consignment Overview & Metrics Grid
    │   │   ├── ShipmentDetail.tsx      # Detailed Compliance & Evidence Control Center
    │   │   └── AuditTrailPage.tsx      # Immutable Event Timeline View
    │   └── types/                      # TypeScript Interface Definitions
    │       └── index.ts                # Shipment, Finding, & Audit Types
    └── dist/                           # Production Static Build Output
```

---

## 21. API Architecture

The FastAPI backend exposes the following RESTful API endpoints under `/api/v1`:

| Method | Endpoint Path | Description | State Mutating? |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/health` | System health check and mode indicator | No |
| `GET` | `/api/v1/shipments` | List all registered export shipments | No |
| `POST` | `/api/v1/shipments` | Register a new export shipment consignment | **Yes** |
| `GET` | `/api/v1/shipments/{id}` | Retrieve details for a specific shipment | No |
| `POST` | `/api/v1/shipments/{id}/analyze` | Execute the 5-agent compliance analysis pipeline | **Yes** |
| `POST` | `/api/v1/shipments/{id}/remediate` | Upload passing residue test & re-evaluate compliance | **Yes** |
| `POST` | `/api/v1/shipments/{id}/what-if` | Run isolated, non-destructive What-If simulation | No |
| `GET` | `/api/v1/shipments/{id}/compliance` | Get complete compliance results & risk analysis | No |
| `GET` | `/api/v1/shipments/{id}/evidence` | Get auditable evidence chain & legal RAG corpus | No |
| `GET` | `/api/v1/shipments/{id}/documents` | List uploaded export document bundle | No |
| `POST` | `/api/v1/shipments/{id}/documents` | Upload a new document to shipment bundle | **Yes** |
| `POST` | `/api/v1/shipments/{id}/approval` | Perform human approval or rejection sign-off | **Yes** |
| `GET` | `/api/v1/shipments/{id}/audit` | Retrieve complete, timestamped audit trail log | No |
| `GET` | `/api/v1/agents` | List active agent metadata and operational status | No |

---

## 22. Local Development

### Environment Requirements
* Python `3.13+`
* Node.js `18+` & npm `9+`
* Windows PowerShell, macOS Terminal, or Linux Shell

### Backend Launch Instructions
```powershell
# Set PYTHONPATH environment variable and launch Uvicorn server
$env:PYTHONPATH="backend"
backend/venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```
*Backend API runs at `http://localhost:8000`. Swagger API docs accessible at `http://localhost:8000/docs`.*

### Frontend Launch Instructions
```bash
# Navigate to frontend directory and start Vite development server
cd frontend
npm run dev
```
*Frontend web app runs at `http://localhost:3000` with automatic `/api` proxying to `http://localhost:8000`.*

---

## 23. Testing

AGRICOMPLY AI includes an automated test suite verifying agent behaviors, API endpoints, deterministic firewall rules, state machine transitions, What-If isolation, and audit logging.

### Execute Backend Test Suite
```powershell
$env:PYTHONPATH="backend"; backend/venv/Scripts/python -m pytest backend/tests -v
```

### Current Test Suite Output (14 / 14 Tests Passing)
```text
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-9.1.1, pluggy-1.6.0
collected 14 items

backend/tests/test_agents.py::test_exporter_agent_extraction PASSED      [  7%]
backend/tests/test_agents.py::test_regulatory_agent_retrieval PASSED     [ 14%]
backend/tests/test_agents.py::test_farm_record_agent_deterministic_comparison PASSED [ 21%]
backend/tests/test_agents.py::test_document_agent_validation PASSED      [ 28%]
backend/tests/test_api.py::test_health_endpoint PASSED                   [ 35%]
backend/tests/test_api.py::test_list_shipments PASSED                    [ 42%]
backend/tests/test_api.py::test_get_shipment_details PASSED              [ 50%]
backend/tests/test_api.py::test_initial_082_residue_produces_hold PASSED [ 57%]
backend/tests/test_api.py::test_remediation_031_upgrades_to_ready_for_approval PASSED [ 64%]
backend/tests/test_api.py::test_human_approval_transitions_to_approved PASSED [ 71%]
backend/tests/test_api.py::test_non_destructive_what_if_does_not_mutate_real_confidence PASSED [ 78%]
backend/tests/test_api.py::test_audit_trail_preserves_remediation_and_approval_events PASSED [ 85%]
backend/tests/test_compliance.py::test_deterministic_rule_engine_evaluation PASSED [ 92%]
backend/tests/test_compliance.py::test_passing_compliance_decision PASSED [100%]

============================== 14 passed in 1.14s ==============================
```

### Verify Production Frontend Build
```bash
cd frontend
npm run build
```
*Build output: `vite v5.4.21 building for production... ✓ built in 8.45s` with zero TypeScript or syntax errors.*

---

## 24. Deployment

AGRICOMPLY AI is configured for production deployment on **Vercel** as two independent projects or a monorepo setup:

```text
                                  GitHub Repository
                        royvikram152-create/agri-comply-ai
                                         │
                    +--------------------+--------------------+
                    │                                         │
                    ▼                                         ▼
         Vercel Project 1:                         Vercel Project 2:
       agri-comply-frontend                     agri-comply-backend
      (React Static Vite SPA)                  (Python Serverless API)
                    │                                         │
                    ▼                                         ▼
      Root Directory: frontend/                Root Directory: backend/
      Build Command: npm run build             Framework: FastAPI / Python 3.13
      Env Var: VITE_API_URL                    Entrypoint: api/index.py
```

### Key Deployment Configurations
* **Frontend SPA Rewrites**: Configured via `frontend/vercel.json` to route all traffic to `index.html`.
* **Dynamic API Targeting**: `frontend/src/api/client.ts` uses `import.meta.env.VITE_API_URL` in production, falling back to relative `/api` in local development.
* **Serverless Entrypoint**: `api/index.py` exposes the FastAPI `app` instance for `@vercel/python` serverless execution.

---

## 25. Zero-Cost Architecture

AGRICOMPLY AI is specifically engineered to operate with **$0 infrastructure overhead**:

* **Serverless Execution**: Runs on Vercel's free serverless tier for Python backends and static hosting for React frontends.
* **Zero Paid LLM Dependencies**: Uses a local BM25 RAG engine and rule-based agent extraction for full demo functionality without requiring paid OpenAI or Anthropic API keys.
* **In-Memory Store**: Uses an efficient, zero-latency in-memory state store eliminating database hosting costs for demo environments.

---

## 26. Security & Reliability Principles

* **Deterministic Enforcement**: Eliminates non-deterministic LLM output from critical compliance decisions.
* **Human Approval Control**: Strict programmatic guards ensure AI can never clear a shipment without authorized human inspector approval.
* **Non-Destructive Simulation**: What-If simulation engine is completely sandboxed from production data.
* **Immutable Audit Trail**: All state changes, remediation actions, and approval decisions create permanent audit records.
* **Zero API Key Leaks**: Application runs securely without committing API keys or hardcoded production credentials.

---

## 27. Limitations

* **Demo Regulatory Scope**: Knowledge base is tailored to EU agricultural import regulations for fresh mangoes. Real-world commercial deployment requires expanding the regulatory RAG corpus across additional crops and destination markets.
* **Operational Thresholds**: Evaluation threshold (`0.50 mg/kg`) used in demo scenarios represents an operational testing limit. Exporters must verify exact current statutory MRLs via EUR-Lex before real-world trade.
* **Document Extraction Scope**: Document analysis in the demo environment evaluates structured metadata and field presence. Commercial deployment would integrate production OCR models (e.g., AWS Textract, Azure Document Intelligence).
* **Regulatory Advice Disclaimer**: AGRICOMPLY AI is an automated workflow compliance tool and does **not** provide legal advice. Exporters must consult official government trade authorities for official clearance.

---

## 28. Future Scope

* **Multinational Trade Pair Expansion**: Broadening the RAG corpus to cover US (USDA APHIS), UK (DEFRA), Japan (MAFF), and Middle East (SFDA) import rules across diverse agricultural commodities (grapes, rice, spices).
* **Live Regulatory Monitoring**: Continuous automated scrapers syncing real-time updates from EUR-Lex and EFSA databases.
* **Enterprise Identity & Role-Based Access Control (RBAC)**: Multi-tenant exporter portals with Granular Inspector, Exporter, and Lab Technician permissions.
* **Production Document OCR Engine**: Full document intelligence pipeline extracting unstructured text directly from scanned PDF certificates.

---

## 29. Hackathon Differentiators

1. **Decoupled Deterministic Firewall**: Decouples non-deterministic AI retrieval from 100% deterministic rule enforcement.
2. **5-Agent Autonomous Orchestration**: Specialized multi-agent pipeline targeting specific trade verification domains.
3. **Regulatory RAG Grounding**: Anchors all recommendations in authoritative legal corpora (EUR-Lex) with clickable source links.
4. **End-to-End Evidence Provenance**: Traces every PASS/FAIL result back to exact farm records, lab tests, and legal text.
5. **Interactive Remediation Loop**: Real-time "What Changed?" workflow updating compliance status upon valid evidence submission.
6. **Programmatic Human Approval Gate**: AI supports but never replaces final human inspector sign-off.
7. **Non-Destructive What-If Simulation**: Risk-free sandbox testing of hypothetical residue levels without mutating live state.
8. **Multi-Dimensional Assessment Confidence**: Explicit evidence completeness metric (0–94%) distinct from compliance score.
9. **Immutable Audit Event Timeline**: Complete observability log tracking all agent runs and human decisions.
10. **Zero-Cost Production Ready**: Serverless architecture ready for deployment with zero API cost constraints.

---

## 30. Judge Demo Flow

```text
Step 1: Dashboard Overview
  └─► Open http://localhost:3000 -> View SHP-MANGO-001 -> Point out HOLD status & 75/100 initial score.

Step 2: Inspect Initial Failure
  └─► Click "View Evidence" -> Show CRIT-MRL-01 failure: Imidacloprid 0.82 mg/kg > 0.50 mg/kg limit.
  └─► Highlight OFFICIAL SOURCE badge & link to Regulation (EC) No 396/2005.

Step 3: Human Approval Gate Test
  └─► Click "Approve Shipment" -> Show system error blocking approval due to active critical gap.

Step 4: Remediation Workflow
  └─► Click "Upload Passing Residue Test" -> Upload lab report with 0.31 mg/kg residue.
  └─► Watch real-time re-evaluation -> Score upgrades to 100/100 -> Status moves to READY_FOR_APPROVAL.

Step 5: Human Approval Clearance
  └─► Enter inspector details ("Inspector Vikram Roy") -> Submit approval -> Status updates to APPROVED_FOR_EXPORT.

Step 6: Non-Destructive What-If Test
  └─► Open "What-If Simulation" -> Test hypothetical 0.82 mg/kg residue -> Observe HOLD (72/100) simulation result.
  └─► Close modal -> Confirm real shipment remains safely APPROVED_FOR_EXPORT (100/100).

Step 7: Audit Trail & Confidence Check
  └─► Open "Audit Trail" tab -> Demonstrate complete event log from creation to approval.
  └─► Hover over AI Assessment Confidence (94%) tooltip -> Explain evidence completeness vs. compliance index.
```

---

## 31. Judge Q&A

**Q: What part of this system is actually AI vs. Deterministic?**  
*A: Non-deterministic AI handles natural language interaction, document field parsing, regulatory RAG retrieval, and gap remediation synthesis. The Compliance Firewall, state machine transitions, score calculations, and approval gates are 100% deterministic Python rules.*

**Q: Why not use an LLM for the whole compliance check?**  
*A: LLMs hallucinate numbers, lack mathematical determinism, cannot guarantee rule enforcement, and change outputs across runs. International agricultural trade requires strict legal auditability that only a deterministic firewall can provide.*

**Q: Can the AI approve a shipment automatically?**  
*A: No. The AI can evaluate evidence and transition status to `READY_FOR_APPROVAL`, but final export clearance strictly requires explicit human sign-off via the Human Approval Gate.*

**Q: What is the difference between Compliance Index and Assessment Confidence?**  
*A: Compliance Index (0–100) measures whether shipment evidence satisfies statutory regulatory rules. Assessment Confidence (94%) measures the structural completeness and quality of available evidence (metadata, RAG coverage, farm logs, document package, citations).*

**Q: Is 0.50 mg/kg an official EU legal MRL?**  
*A: In our primary demo scenario, 0.50 mg/kg is an operational demo evaluation limit. Official statutory EU MRL limits are governed by Regulation (EC) No 396/2005, which our provenance system explicitly links to.*

**Q: Does What-If simulation modify live production shipment data?**  
*A: No. What-If simulations execute against an isolated instance of the compliance engine in memory and never mutate persisted shipment database records.*

---

## 32. One-Minute Pitch

> "Every day, millions of dollars in perishable agricultural exports are delayed or destroyed at international borders due to fragmented compliance documentation and mismatched chemical residue limits.
> 
> Standard LLM chatbots cannot solve this—they hallucinate legal rules and lack deterministic enforcement.
> 
> AGRICOMPLY AI solves this by pairing 5 specialized autonomous AI agents with a zero-hallucination Deterministic Compliance Firewall. Our system parses exporter inputs, retrieves ground-truth EU regulations via RAG, audits farm residue logs, validates export document packages, and pinpoints compliance gaps.
> 
> When gaps are detected, our remediation engine guides exporters to upload passing lab tests, upgrading status in real-time while maintaining strict human-in-the-loop approval gates, immutable audit trails, and risk-free What-If sandbox simulations.
> 
> AGRICOMPLY AI delivers fast, zero-cost, auditable compliance assurance for global trade."

---

## 33. 2–3 Minute Demo Script

*(Presenter speaking while navigating the web application)*

> **[0:00 - 0:30] Introduction & Initial State**  
> *"Welcome to AGRICOMPLY AI. Today we are looking at shipment `SHP-MANGO-001`—a 2,000 kg consignment of Alphonso Mangoes bound from India to the European Union. Notice the initial status is **HOLD** with a Compliance Score of **75/100**. Our system has executed a 5-agent pipeline, retrieving relevant EU regulations under Regulation (EC) No 396/2005. If I try to approve this shipment right now as a human inspector... the system programmatically blocks me because an active critical gap exists."*

> **[0:30 - 1:15] Evidence Provenance & Gap Analysis**  
> *"Let's inspect the evidence drawer. Here we see our Farm Record Agent detected an Imidacloprid residue level of **0.82 mg/kg**, exceeding our operational threshold of **0.50 mg/kg**. Notice the **OFFICIAL SOURCE** badge—every compliance decision is linked directly to authoritative legal citations in the EU Pesticides Database."*

> **[1:15 - 2:00] Remediation & Human Sign-off**  
> *"Now let's resolve this gap. The exporter uploads a new NABL-accredited laboratory residue test report showing a passing level of **0.31 mg/kg**. I click 'Upload Passing Test'. The system immediately executes a re-evaluation pipeline. The Compliance Score jumps to **100/100**, and the status upgrades to **READY_FOR_APPROVAL**. Now, as authorized compliance inspector 'Vikram Roy', I execute human approval... and the shipment receives official clearance: **APPROVED_FOR_EXPORT**."*

> **[2:00 - 2:45] What-If Simulation & Audit Trail**  
> *"Finally, let's test our non-destructive What-If simulation. What if an exporter wants to test a hypothetical residue level of 0.82 mg/kg? The simulation calculates a status of **HOLD** (72/100 score)... but when I close the sandbox, our actual live shipment remains safely **APPROVED_FOR_EXPORT**. Everything is recorded in our immutable Audit Trail tab with exact timestamps. Thank you!"*

---

## 35. Demo Credentials & Seed Data

* **Authentication**: The demo application operates without login constraints for frictionless evaluation.
* **Seed Shipment ID**: `SHP-MANGO-001`
* **Exporter**: Royal Agri Exports Ltd (`EXP-IND-908`)
* **Commodity**: Fresh Mango (Variety: Alphonso)
* **Route**: India (`IND`) $\rightarrow$ European Union (`EU`)
* **Consignment Quantity**: 2,000 kg

---

## 36. Final Verified Project Status

* **Backend Test Suite**: **14 / 14 Tests Passing** (`pytest -v` clean execution)
* **Frontend Build**: **100% Clean Production Build** (`npm run build` completed with zero errors)
* **Git Repository Status**: Clean `main` branch synced with remote repository `royvikram152-create/agri-comply-ai`
* **Application Integrity**: Decoupled multi-agent architecture, deterministic firewall, RAG retriever, What-If engine, and human approval gates fully operational.
