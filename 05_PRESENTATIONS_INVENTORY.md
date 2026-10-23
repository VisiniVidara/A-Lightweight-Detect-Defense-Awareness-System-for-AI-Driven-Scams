# 05 — Research Presentations Inventory (`05_PRESENTATIONS_INVENTORY.md`)

This document catalogues the formal slide decks, demonstrations, and oral defense presentations associated with the MailSentra research project.

---

## A. Page Title
**Research Presentations & Slide Decks**

## B. Page Introduction
This section catalogues the official academic presentations prepared throughout the research project lifecycle. It provides presentation outlines, research milestones addressed, demonstration walkthroughs, and slide availability statuses.

---

## C. Research Presentations Catalogue Table

| # | Presentation Title | Research Stage | Primary Objective & Scope | Presumed Date | Format | Source / Reference | Availability Status | Brief Description |
|---|---|---|---|---|---|---|---|---|
| **P-01** | **Project Proposal Presentation** | Proposal | Concept defense, problem definition, literature survey, and division of research responsibilities. | Early 2026 | PPTX / PDF | `ACAD-M01` Milestone | `PENDING` | Slides defining the multi-modal email security gap, research aim, and component boundaries. |
| **P-02** | **Progress Presentation 1 (PP1)** | Mid-Term 1 | Algorithmic design, dataset collection, baseline model architectures, and initial ML evaluations. | Mid 2026 | PPTX / PDF | `ACAD-M02` Milestone | `PENDING` | Focuses on DistilBERT fine-tuning, EfficientNet-B2 transfer learning, and initial C2 contracts. |
| **P-03** | **Progress Presentation 2 (PP2)** | Mid-Term 2 | Standalone prototype validation, preliminary user interfaces, and early cross-modal integration plans. | Late Mid 2026 | PPTX / PDF | `ACAD-M03` Milestone | `PENDING` | Covers individual component performance benchmarks, Thunderbird extension prototypes, and silo remediation. |
| **P-04** | **Final Assessment & Demonstration Presentation** | Final Stage | Complete system demonstration, end-to-end multi-modal triaging, fail-safe proofs, and empirical evaluation. | October 2026 | PPTX / PDF / Live | `DEMO_GUIDE.md`, `PHASE7_DASHBOARD_DEMO.md` | `AVAILABLE / READY` | Comprehensive slide deck and live demonstration script guiding examiners through the 8 live attack scenarios. |
| **P-05** | **Viva Voce / Oral Defense Deck** | Final Defense | High-level architectural defense, critical scrutiny of limitations, negative ML findings, and future roadmap. | October 2026 | PPTX / PDF | `VIVA_CHEAT_SHEET.md`, `SUBMISSION_INDEX.md` | `AVAILABLE / READY` | Structured defense deck addressing examiner questions on dependency isolation, Grad-CAM, and fail-safe design. |
| **P-06** | **Live System Walkthrough & Examiner Guide** | Demonstration | Interactive demonstration guide covering SOC dashboard and Thunderbird MailExtension. | October 2026 | Markdown / Interactive | `DEMO_GUIDE.md`, `DEMO_CHECKLIST.md` | `AVAILABLE` | Step-by-step technical script walking through live benign, phishing, steganographic, and corrupted emails. |

---

## D. Live Demonstration Scenarios Catalogue (Available for Presentation)

The project includes an executable demonstration suite with 6 built-in scenario fixtures ready for oral evaluation:

1. **Scenario 1 — Benign Email Ingestion:** Demonstrates baseline operation, sub-second response, and synthesized notice guidance (`RULE-006`).
2. **Scenario 2 — Spear-Phishing Threat:** Demonstrates fine-tuned DistilBERT classification, URL threat intel matching, and prominent user warning (`RULE-009`).
3. **Scenario 3 — Benign Message with Clean Attachment:** Validates parallel multi-modal inspection where both text and image are verified clean.
4. **Scenario 4 — Cross-Modal Steganography Escalation:** Demonstrates the core research thesis: a benign-text email (score 6.0) is autonomously escalated to `THREAT_DETECTED` based on hidden visual payloads identified by EfficientNet-B2 and Grad-CAM.
5. **Scenario 5 — Combined Multi-Modal Attack:** Shows simultaneous text deception and image steganography, triggering multi-factor severity arbitration.
6. **Scenario 6 — Corrupted Attachment Fault Injection:** Verifies fail-safe resiliency: corrupted images produce `partial` and `analysis_incomplete` states, proving the system **never fails open**.

---

## E. Suggested Content Blocks
- **Presentation Cards Grid:** Grouped into Milestone Presentations, Final Defense, and Live Demos.
- **Interactive Slide Viewer / Download Links:** Placeholders for `.pptx` and `.pdf` slide deck downloads.
- **Demonstration Walkthrough Stepper:** Interactive visual step-through of the 6 core demonstration scenarios with expected examiner outputs.

---

## F. Missing Information (Requires Manual Input)
- Uploaded presentation files (`.pptx` or `.pdf`) from original student submissions (`M-14`).
- Recorded video demonstration links or screencasts, if produced during the academic semester (`M-14`).

---

## G. Supporting Evidence References
- `DEMO_GUIDE.md`: Lines 1–150 (Scenario descriptions and expected UI outcomes)
- `DEMO_CHECKLIST.md`: Lines 1–40 (Pre-flight steps and verification checklist)
- `VIVA_CHEAT_SHEET.md`: Lines 1–80 (Examiner Q&A and defense talking points)
- `orchestrator/app/main.py`: Lines 359–388 (Demo fixture mapping endpoints)
