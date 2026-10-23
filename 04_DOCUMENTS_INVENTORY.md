# 04 — Research Documents Inventory (`04_DOCUMENTS_INVENTORY.md`)

This document catalogues all verified research reports, technical specifications, and academic documents available in the MailSentra workspace.

---

## A. Page Title
**Research Documentation & Publications Catalogue**

## B. Page Introduction
This section provides an audited inventory of the formal documentation produced throughout the lifecycle of the MailSentra research project. Documents are categorized by research stage and classified according to their availability and public suitability.

---

## C. Research Document Inventory Table

| # | Exact Document Title | Research Stage | Category | File Format | Source Workspace Path | Availability Status | Public Suitability | Brief Description |
|---|---|---|---|---|---|---|---|---|
| **D-01** | **Common Thesis Evidence Base** | Final Stage | Thesis Documentation | DOCX / ZIP | `common_thesis_evidence/COMMON_THESIS_EVIDENCE_BASE.docx` | `AVAILABLE` | `NEEDS REVIEW` | Comprehensive 12-chapter evidence base compiling empirical data, architectures, and evaluation results. |
| **D-02** | **Project Overview & Executive Summary** | Final Stage | Technical Report | Markdown | `common_thesis_evidence/00_PROJECT_OVERVIEW.md` | `AVAILABLE` | `AVAILABLE` | Verified technical overview of components, runtime configurations, live health, and cross-document audits. |
| **D-03** | **Background, Stakeholders & SDG Context** | Domain / Analysis | Context Analysis | Markdown | `common_thesis_evidence/01_BACKGROUND_STAKEHOLDERS_SDG.md` | `AVAILABLE` | `AVAILABLE` | Detailed context on cyber attack vectors, simulated actors, and Sustainable Development Goal mappings. |
| **D-04** | **Problem Definition & Objectives** | Proposal / Scope | Research Scope | Markdown | `common_thesis_evidence/02_PROBLEM_AND_OBJECTIVES.md` | `AVAILABLE` | `AVAILABLE` | Formal problem statements, root cause analysis, component mapping, and objective traceability matrices. |
| **D-05** | **Integrated Solution & Architecture** | Architecture | Technical Design | Markdown | `common_thesis_evidence/03_SOLUTION_AND_ARCHITECTURE.md` | `AVAILABLE` | `AVAILABLE` | Full architectural specification, data flow lifecycles, trust boundaries, and workflow sequence diagrams. |
| **D-06** | **Component Integration & Interfaces** | Integration | Integration Report | Markdown | `common_thesis_evidence/04_INTEGRATION_AND_INTERFACES.md` | `AVAILABLE` | `AVAILABLE` | Detailed analysis of microservice integration challenges, interface contracts, and failure handling. |
| **D-07** | **System Architecture Specification** | Architecture | Architecture Spec | Markdown | `docs/SYSTEM_ARCHITECTURE.md` | `AVAILABLE` | `AVAILABLE` | Concise architectural overview outlining port bindings, data boundaries, and ML model ownership. |
| **D-08** | **Integrated Testing, Evaluation & Validation** | Evaluation | Test Report | Markdown | `common_thesis_evidence/06_TESTING_AND_EVALUATION.md` | `AVAILABLE` | `AVAILABLE` | Empirical test records, including 854 pytest runs, 8 live scenarios, and latency benchmarks. |
| **D-09** | **Research Contributions Matrix** | Final Stage | Academic Reference | Markdown | `docs/RESEARCH_CONTRIBUTIONS.md` | `AVAILABLE` | `AVAILABLE` | Explicit delineation of scientific and engineering contributions across C1, C2, C3, and Orchestrator. |
| **D-10** | **Academic Limitations Document** | Final Stage | Research Evaluation | Markdown | `docs/LIMITATIONS.md` | `AVAILABLE` | `AVAILABLE` | Transparent documentation of prototype boundaries, concurrency limits, and operational scope. |
| **D-11** | **Future Research Directions** | Final Stage | Research Roadmap | Markdown | `docs/FUTURE_WORK.md` | `AVAILABLE` | `AVAILABLE` | Roadmap detailing containerization, hardware acceleration, multi-user deployments, and SIEM integration. |
| **D-12** | **Component 02 Technical Design Document** | Design / PP1 | Design Document | PDF / DOCX | `Draft-C-2-Test/Documents/Component2_Defense_Awareness_Technical_Design.pdf` | `AVAILABLE` | `NEEDS REVIEW` | Detailed design specification for Component 02 defense policies and awareness algorithms. |
| **D-13** | **Machine Learning Research Report (C2)** | Research / Analysis | ML Study | Markdown | `Draft-Component02/Draft-C-2-Test/docs/ML_RESEARCH_REPORT.md` | `AVAILABLE` | `AVAILABLE` | Empirical analysis documenting the negative result of ML vs. deterministic awareness selection. |
| **D-14** | **Component 01 Phase 12 Final Evaluation** | Evaluation / PP2 | ML Evaluation | JSON / MD | `Draft-Component01/artifacts/runs/phase12_final_evaluation.json` | `AVAILABLE` | `AVAILABLE` | Automated performance metrics for DistilBERT text classification on held-out external corpora. |
| **D-15** | **Three-Component Integration Plan** | Integration | Engineering Plan | Markdown | `INTEGRATION_PLAN.md` | `AVAILABLE` | `AVAILABLE` | 24-section architectural roadmap detailing multi-service isolation and testing procedures. |
| **D-16** | **Live API Contract Catalogue** | Integration | Interface Spec | Markdown | `LIVE_API_CONTRACTS.md` | `AVAILABLE` | `AVAILABLE` | Verified JSON request and response payloads across all four microservice endpoints. |
| **D-17** | **Final Project Validation Report** | Verification | Audit Report | Markdown | `FINAL_PROJECT_VALIDATION.md` | `AVAILABLE` | `AVAILABLE` | Quality assurance sign-off recording clean-install regression and live test execution. |
| **D-18** | **Viva Voce Cheat Sheet** | Examination | Exam Guide | Markdown | `VIVA_CHEAT_SHEET.md` | `AVAILABLE` | `AVAILABLE` | Technical defense reference answering anticipated examiner inquiries regarding platform decisions. |

---

## D. Document Classification Definitions
- **`AVAILABLE`**: The file exists at a verified path in the repository and has been validated.
- **`PENDING`**: A documented document whose official formatted copy is undergoing compilation.
- **`NEEDS REVIEW`**: Contains extensive internal or academic drafting details that should be reviewed prior to public publication.
- **`RESTRICTED`**: Confidential internal material (e.g., private keys, raw tokens, unscrubbed logs). *Note: Zero restricted documents exist in the public catalogue.*

---

## E. Suggested Content Blocks
- **Document Library Grid:** Filterable by category (Architecture, Testing, Evaluation, Design).
- **Document Detail Modals / Download Badges:** Format badge (PDF, Markdown, DOCX), stage tag, and synopsis.
- **Academic Publication Callout:** Highlighting the Common Thesis Evidence Base and Technical Summaries.

---

## F. Missing Information (Requires Manual Input)
- Formal university thesis repository handles or persistent DOI identifiers (`M-08`).
- Formal publication status of any derived workshop or conference papers (`M-08`).

---

## G. Supporting Evidence References
- `SUBMISSION_INDEX.md`: Lines 7–35
- `common_thesis_evidence/10_EVIDENCE_REGISTER.md`: Parts 1 & 2
- Directory listings of `docs/`, `common_thesis_evidence/`, and component directories.
