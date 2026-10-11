# 00 — Project Analysis & Verified System Overview

**Investigation Date:** 2026-10-10  
**Project Workspace:** `C:\Users\User\Desktop\New folder (2)\Integration`  
**Investigation Standard:** Empirical verification via repository source inspection, runtime query, and test execution.

---

## 1. Project Identification & Title Disambiguation

The investigation confirms that the project repository uses four distinct names across different subsystems. For academic rigor and web presentation, the title hierarchy is established as follows:

| Context | Name Identified | Evidence Location | Status |
|---|---|---|---|
| **System Codename / Shorthand** | **MailSentra** (or **MailSentra-RP**) | `README.md:1`, `VERSION.txt:1`, `orchestrator/README.md:1` | VERIFIED |
| **Descriptive Academic Title** | **Multi-Modal Email Threat Detection & Defense Platform** | `START_SYSTEM.bat:3`, `orchestrator/app/main.py:40`, Runtime `GET /api/system-info` | VERIFIED (Live Service Response) |
| **Client Extension Title** | **MailSentra Unified Email Threat & Steganography Shield** | `unified-thunderbird/manifest.json:3` | VERIFIED |
| **Comprehensive Research Formulation** | **MailSentra: A Multi-Modal Email Threat Detection, Steganography Analysis, and Policy-Driven Defense Platform** | Synthesis of research capabilities across components | RECOMMENDED MASTER TITLE |

- **Project Abbreviation:** MailSentra-RP / MailSentra
- **System Version:** 1.0 (Research Prototype)
- **Deployment & Operating Mode:** Local Multi-Service (`127.0.0.1:8000–8003`), Shadow / Advisory Mode (`execution_state: "shadow_only"`)
- **Target OS / Environment:** Windows 10/11 x64, Python 3.11.9 runtime across four isolated virtual environments.

---

## 2. Component Inventory & The "Four-Component" Question

A critical requirement of the academic investigation is verifying the number of active research components.

> **CRITICAL VERIFIED FINDING (M-01):**  
> The repository contains **THREE active research components** plus **ONE integration coordination gateway** (Orchestrator + Unified Client + Dashboard).  
> An exhaustive search for any fourth student component (`Component 04`, `Component 4`, `fourth component`) returned **0 matches** across the entire codebase and documentation.  
> As required by the research guidelines, **no fourth component is fabricated**. The Orchestrator acts as the fourth technical engineering unit.

### Component Summary Table

| Component | Research Subproblem | Main Method / Technology | Inputs | Outputs | Integration Role | Status |
|---|---|---|---|---|---|---|
| **Component 01 (C1)** | Deceptive email text, sender infrastructure abuse, malicious links, and header anomalies | Fine-tuned DistilBERT + Heuristic Prefilter (DNS, SPF/DKIM, lookalike domains) + Stylometric AI-authorship profiling + Hybrid Risk Scorer | Structured JSON or RFC 822 EML: Headers, text body, HTML body, URLs, attachment metadata (no bytes) | Hybrid threat score (0–100), risk level (low/med/high), classification (`scam`/`legitimate`), per-stage breakdown | Primary detector for textual and infrastructural attack vectors; provides threat evidence for policy rules | **ACTIVE & VERIFIED** (FastAPI `:8001`, 37 unit tests pass) |
| **Component 02 (C2)** | Multi-modal evidence synthesis, proportionality, reversibility, and user-comprehension gap | Declarative 18-rule JSON Policy Engine (`c2-defense-policy` v1.5.0) + Severity layer + C3 direct-path arbitration + Deterministic awareness template selector | Canonical `SecurityAssessmentEnvelope` (strict Pydantic schema) with findings from C1 and C3 | Graded defense posture (5 levels), recommended action (advisory), grounded user awareness guidance, audit logs | **Final Decision Authority**; sole component that issues user actions and explanations | **ACTIVE & VERIFIED** (FastAPI `:8002`, 796 tests pass, 167 phase checks pass) |
| **Component 03 (C3)** | Concealed binary payloads hidden inside benign-looking email image attachments | Deep Learning Transfer Learning: EfficientNet-B2 (binary classification `clean` vs `stego`) + Explainable Grad-CAM heatmaps | Image file stream (multipart/form-data: PNG, JPEG, BMP) | Prediction (`Clean`/`Stego`), class probabilities, confidence, visual Grad-CAM heatmap (Base64 PNG) | Primary detector for image steganography; can escalate posture independently | **ACTIVE & VERIFIED** (Flask `:8003`, checkpoint verified, thread-safety caveat noted) |
| **Integration Gateway (Orchestrator)** | System fragmentation, port conflicts, incompatible dependencies, and fail-safe multi-modal aggregation | Asynchronous Parallel Dispatch (`asyncio.gather`), canonical Pydantic envelope transformation, fail-safe degradation handler | Inbound mail from Thunderbird MailExtension (`POST /api/analyze-email`) or direct EML file | Aggregated `UnifiedAnalysisResponse` sent to mail client; feeds live SOC demonstration dashboard | System Coordinator; assigns `request_id`, normalizes evidence, prevents fail-open | **ACTIVE & VERIFIED** (FastAPI `:8000`, 21 tests pass, 8 live E2E scenarios pass) |

---

## 3. Disambiguation of Active vs. Obsolete Project Copies

To ensure absolute accuracy on the academic website, active runtime paths are distinguished from obsolete artifacts:

1. **Component 02 Active Runtime:**
   - **Active:** `Draft-Component02/Draft-C-2-Test/` — Started by `scripts/start-all.ps1` via `-m uvicorn api.main:app --port 8002`.
   - **Inactive Duplicate:** `Draft-C-2-Test/` at root — Functional clone left from an earlier replacement phase; not referenced by any launcher.
2. **Thunderbird Extension:**
   - **Active:** `unified-thunderbird/` (packaged as `dist/MailSentra-unified-thunderbird.xpi`) — Single MailExtension communicating exclusively with Orchestrator on port 8000.
   - **Obsolete:** `Draft-Component01/extension/` (marked with `LEGACY.md`) and `Draft-Component03/.../thunderbird_extension/` (pointed to obsolete port 5000).
3. **Component 03 Virtual Environment:**
   - **Active:** `.venv-c3` (Python 3.11.9 with locked PyTorch 2.13.0 and OpenCV).
   - **Obsolete:** `Draft-Component03/.../venv/` — Historical broken virtual environment containing hardcoded paths from developer machine.
4. **Machine Learning Model Weights:**
   - **Active Checkpoints (Protected by SHA-256):**
     1. C1 DistilBERT: `Draft-Component01/artifacts/models/text/model/model.safetensors`
     2. C1 Calibrator: `Draft-Component01/artifacts/models/text/calibrator.joblib`
     3. C1 AI-text Detector: `Draft-Component01/artifacts/models/aigen/model.joblib`
     4. C3 EfficientNet-B2: `Draft-Component03/RP final (stego)/saved_models/best_efficientnet_b2.pth`
     5. C2 Awareness Selector (v1 legacy baseline): `Draft-Component02/Draft-C-2-Test/models/awareness_selector_v1.joblib`
   - *Note on C2 v2.0.0:* The active runtime employs deterministic template matching while v2.0.0 ML selector models (`awareness_category_v2.joblib`, `awareness_triggers_v2.joblib`) remain disabled (`ml_enabled: false`) pending human review.

---

## 4. Empirical Validation & Key Research Findings

All test suites and integration scenarios were independently verified on 2026-10-10:

- **Orchestrator Unit & Integration:** 21 / 21 pytest passed.
- **Component 01 Unit & Detection Tests:** 37 passed, 1 skipped.
- **Component 02 Comprehensive Test Suite:** 796 / 796 pytest passed (52.03s), 167 / 167 phase validation checks passed, 15 / 15 security audit probes passed.
- **End-to-End Orchestrator Scenarios:** 8 / 8 live scenarios passed with verified response times (560 ms – 1808 ms).
- **Live SOC Dashboard Tests:** 11 / 11 automated verification tests passed.
- **Fail-Safe Integrity:** Confirmed that a corrupted or unreadable attachment produces status `partial` and error flags, and **never fails open** to report "safe" or "clean".
- **Significant Research Finding (Negative Result in ML Awareness):** C2's research study revealed that an ML classifier for scam categorization achieved macro F1 0.9457, whereas a deterministic keyword baseline achieved macro F1 0.9704. In accordance with rigorous scientific practices, the ML selector was disabled in favor of deterministic templates, proving that lack of human-annotated awareness data favors explainable rule-based approaches.
- **Disclosed Technical Concurrency Limitation (Finding D-01):** Component 03's shared module-level PyTorch model and Grad-CAM backward hooks are not re-entrant. Rapid parallel multi-image calls can cause race conditions under high concurrency; the Orchestrator safely catches worker dropouts to preserve overall system stability.
