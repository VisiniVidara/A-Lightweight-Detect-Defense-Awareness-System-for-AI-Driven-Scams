# 02 — Domain Research & Technical Core (`02_DOMAIN_CONTENT.md`)

This document details the academic domain, problem definitions, literature context, research gaps, methodology, architectural design, component mappings, and experimental results.

---

## A. Page Title
**Research Domain, Methodology & Integrated Solution Architecture**

## B. Page Introduction
This section presents the comprehensive academic foundation of the MailSentra platform. It details the motivating cyber threat landscape, formalizes the research problem and subproblems, reviews the state-of-the-art and technical gaps, outlines the empirical methodology, and provides a component-by-component mapping of the integrated multi-modal solution.

---

## C. Main Content Sections

### 2.1 Research Background & Literature Survey

#### 1. Domain Background
The proliferation of digital communication has positioned email as the primary attack vector for advanced threat actors. The United Nations Sustainable Development Goals (SDG 9: Industry, Innovation, and Infrastructure, Target 9.5) emphasize scientific research and resilient digital infrastructures. In this context, protecting communication channels against modern cybercrime is a foundational cybersecurity imperative.

Modern attacks have transitioned from generic spam mass-mailings to **multi-channel, context-aware campaigns**:
- **Social Engineering & Linguistic Manipulation:** Attackers employ spear-phishing, authority impersonation, and urgency-driven calls to action. The emergence of large language models (LLMs) allows adversaries to generate grammatically impeccable, synthetically authored scam text at scale.
- **Infrastructure Spoofing:** Attackers weaponize lookalike domain typography (typosquatting, IDN homograph attacks) and exploit misconfigurations in domain authentication records (SPF, DKIM, and DMARC).
- **Steganographic Payload Delivery:** Digital steganography embeds covert payloads inside arbitrary carrier media, altering pixel values imperceptibly while preserving visual aesthetics. Traditional endpoint detection and antivirus engines rely heavily on static hashing and binary file signatures; they cannot detect malicious data encoded inside standard PNG, JPEG, or BMP email attachments.
- **The Explainability Deficit in Security Operations:** Modern email filtering engines are predominantly opaque. They assign a monolithic score or silently redirect emails to junk folders without explaining *why* an email is hazardous or how the recipient should behave.

#### 2. Technological Foundations in Project Workspace
The research builds upon four technological pillars evidenced within the project repository:
1. **Transformer-Based NLP (DistilBERT):** Lightweight bidirectional encoder representations fine-tuned on email corpora for binary scam/legitimate text classification (`Draft-Component01/src/component1/scam_classifier.py`).
2. **Stylometric AI-Authorship Detection:** Perplexity, burstiness, and lexical diversity metrics calibrated to identify automated text synthesis (`Draft-Component01/src/component1/ai_detector.py`).
3. **Deep Convolutional Steganalysis (EfficientNet-B2):** Scaled convolutional neural networks retrained on pixel-domain steganography pairs, augmented by Gradient-weighted Class Activation Mapping (Grad-CAM) to visualize payload regions (`Draft-Component03/RP final (stego)/model.py`).
4. **Declarative Policy-as-Data Architecture:** Formal decoupling of threat scoring from policy decisions, utilizing an 18-rule declarative JSON rulebook evaluated against multi-modal evidence envelopes (`Draft-Component02/Draft-C-2-Test/src/component2/policy.py`).

---

### 2.2 Research Gap Analysis

A rigorous investigation of the project records reveals five critical gaps in existing email security research and industry tooling:

| Gap ID | Identified Research Gap | Limitations of Current Approaches | How MailSentra Addresses the Gap |
|---|---|---|---|
| **GAP-01** | **Multi-Modal Cross-Channel Silos** | Existing email filters evaluate text bodies, reputation headers, and attachments in isolation. A malicious steganographic payload attached to a benign-sounding email will routinely pass through text filters untouched. | MailSentra unifies text, header reputation, and deep image steganalysis into an atomic, parallel client request, allowing visual threats to autonomously escalate defense postures. |
| **GAP-02** | **Score Incommensurability & Fusion Briskness** | Combining disparate model outputs (e.g., an NLP risk score vs. a CNN softmax probability) typically involves training complex fusion models that require massive multi-modal training sets and risk overfitting. | MailSentra introduces a structured evidence normalization gateway (`SecurityAssessmentEnvelope`) and an explicit severity arbitration layer (`select_combined_winner`), preserving individual model calibrations without speculative fusion weights. |
| **GAP-03** | **Black-Box Warnings & Absence of User Agency** | Legacy email gateways provide binary "Safe/Unsafe" tags or opaque banners, offering no actionable learning points or contextual reasoning to the end user. | Component 02 transforms threat evidence into structured, plain-language awareness guidance explaining *why* a message is hazardous and recommending reversible user actions. |
| **GAP-04** | **Fail-Open Vulnerability in Cascaded Architectures** | When an attachment scanner or external API encounters a timeout or malformed payload, conventional tools often swallow the error or mark the item "clean" to avoid user disruption. | MailSentra strictly enforces a "Never-Fail-Open" invariant: unanalyzed or corrupted attachments return explicit `partial` and `analysis_incomplete` states, preventing false reassurance. |
| **GAP-05** | **Lack of Longitudinal User Awareness Tracking** | Security tools treat each email interaction as an isolated event, failing to model user risk evolution over time. | Component 02 implements a stateful **Vulnerability Profiler** tracking user behavior across seven distinct progression phases (from `early_observation` to `consistently_safer`). |

---

### 2.3 Research Problem & Subproblems

#### Overall Problem Statement
> *Modern email-borne cyber attacks increasingly exploit distributed, multi-modal attack surfaces—combining social engineering text, domain impersonation, and concealed image steganography. Defenses in common practice evaluate these vectors in isolation and deliver opaque, binary verdicts without contextual explanations. Consequently, multi-channel attacks bypass perimeter filters, and recipient end users—lacking actionable reasoning—remain vulnerable to persistent manipulation.*

#### Four Structured Research Subproblems
1. **Subproblem 1 (Textual & Infrastructural Threat Detection):** How to reliably detect deceptive text, sender spoofing, malicious links, and AI-synthesized phrasing in real-time with explainable intermediate stages?  
   *(Addressed by Component 01)*
2. **Subproblem 2 (Visual Payload & Steganography Detection):** How to detect concealed steganographic data hidden inside digital image attachments with verifiable visual localization?  
   *(Addressed by Component 03)*
3. **Subproblem 3 (Proportional Policy-Driven Defense & Adaptive Awareness):** How to translate heterogeneous, multi-modal evidence into calibrated, explainable defense actions and personalized educational guidance without hallucination?  
   *(Addressed by Component 02)*
4. **Subproblem 4 (Unified Asynchronous Orchestration & Fail-Safe Composition):** How to integrate heterogeneous, dependency-incompatible microservices into an atomic, fail-safe client pipeline that operates natively within standard email workflows?  
   *(Addressed by the Orchestration Gateway & Unified MailExtension)*

---

### 2.4 Research Objectives

#### Overall Aim
To design, implement, integrate, and empirically validate an explainable, multi-modal email security platform capable of detecting composite textual and steganographic threats, synthesizing calibrated defense postures, and delivering native, actionable awareness guidance directly inside the email client.

#### Specific Research Objectives
1. **Objective 1:** Implement a multi-stage email threat detection pipeline uniting rule-based prefiltering (SPF/DKIM, DNS, URL reputation), fine-tuned DistilBERT classification, and stylometric AI-authorship profiling with explicit hard-evidence score floors.
2. **Objective 2:** Develop a deep convolutional steganalysis model utilizing transfer learning on EfficientNet-B2 with Grad-CAM visual heatmaps for localized inspection of image attachments.
3. **Objective 3:** Construct a declarative, 18-rule policy engine and evidence normalization envelope that arbitrates multi-modal severity and outputs calibrated, five-level defense postures.
4. **Objective 4:** Design an evidence-grounded awareness generation system and longitudinal vulnerability profiler to deliver contextual guidance without generative hallucinations.
5. **Objective 5:** Architect a lightweight, asynchronous orchestration gateway that handles parallel microservice dispatch, eliminates dependency conflicts via virtual environment isolation, and strictly enforces never-fail-open error handling.
6. **Objective 6:** Deploy and validate a unified Mozilla Thunderbird MailExtension and SOC demonstration dashboard to evaluate end-to-end multi-modal triage across representative attack scenarios.

---

### 2.5 Research Methodology & System Pipeline

```
                                      [ INCOMING EMAIL ]
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │ Mozilla Thunderbird MailExtension│
                             │ (Header, Body, URLs, Images)     │
                             └────────────────┬────────────────┘
                                              │ POST /api/analyze-email
                                              ▼
                             ┌─────────────────────────────────┐
                             │   Orchestrator Gateway (:8000)   │
                             │   - Assigns unique request_id   │
                             │   - Parallel Dispatch (asyncio) │
                             └────────┬───────────────┬────────┘
                                      │               │
                     Text & Metadata  │               │ Image Attachments
                                      ▼               ▼
                 ┌───────────────────────────┐  ┌───────────────────────────┐
                 │ Component 01 Engine (:8001)│  │ Component 03 Engine (:8003)│
                 │ 1. Prefilter & DNS Intel  │  │ 1. 224x224 Normalization  │
                 │ 2. DistilBERT Classifier  │  │ 2. EfficientNet-B2 CNN    │
                 │ 3. AI Text Profiler       │  │ 3. Grad-CAM Activation    │
                 │ 4. Hybrid Risk Scorer     │  │                           │
                 └─────────────┬─────────────┘  └─────────────┬─────────────┘
                               │ Risk Score (0-100)           │ Stego Probability &
                               │ & Stage Evidence             │ Grad-CAM Heatmap
                               └──────────────┬───────────────┘
                                              ▼
                             ┌─────────────────────────────────┐
                             │ Orchestrator Evidence Mapper    │
                             │ - Canonical Envelope Builder    │
                             │ - Strict Pydantic Validation    │
                             └────────────────┬────────────────┘
                                              │ POST /api/v1/evaluate
                                              ▼
                             ┌─────────────────────────────────┐
                             │ Component 02 Defense & Awareness│
                             │ 1. D3 Trigger Gate (Clean Check)│
                             │ 2. Four-Factor Assessment       │
                             │ 3. C3 Direct Severity Path      │
                             │ 4. 18-Rule Policy Matching      │
                             │ 5. Awareness Template Selector  │
                             │ 6. Longitudinal Profiler & Audit│
                             └────────────────┬────────────────┘
                                              │ Unified Defense Response
                                              ▼
                             ┌─────────────────────────────────┐
                             │     Unified Client Rendering    │
                             │ - Thunderbird Warning Banner    │
                             │ - SOC Dashboard Feed (:8000)    │
                             └─────────────────────────────────┘
```

#### Systematic Research Phases:
1. **Data Acquisition & Curation:** Assembling empirical corpora spanning historical phishing datasets (CEAS_08, Enron, Nazario, Nigerian Fraud, SpamAssassin), AI text benchmarks (HC3), and steganographic image pairs.
2. **Model Training & Hyperparameter Calibration:** Fine-tuning DistilBERT with threshold calibration on external validation sets; transfer learning with EfficientNet-B2 for steganographic feature extraction.
3. **Formal Policy Formalization:** Constructing an unambiguous, declarative policy matrix mapping score bands, evidence strength, reliability, and consequence into graded operational postures.
4. **Interface Contract Engineering:** Formulating strict Pydantic schemas (`SecurityAssessmentEnvelope`, `UnifiedAnalysisResponse`) with `extra="forbid"` to eliminate inter-service contract drift.
5. **Empirical System Validation:** Stress-testing the multi-service cluster via live RFC 822 EML scenarios, automated regression suites, and fault-injection diagnostics.

---

### 2.6 Technologies Used Across the Platform

The MailSentra platform strategically leverages distinct, isolated software stacks to resolve irreconcilable library dependencies:

| Category | Technology | Version | Architectural Role |
|---|---|---|---|
| **Languages** | Python | 3.11.9 (x64) | Primary backend runtime across all four microservices |
| | JavaScript / Node.js | ES6+ / Node v22.18.0 | Thunderbird MailExtension implementation & live client test harness |
| **Web Frameworks** | FastAPI | 0.111.0 (C1), 0.142.2 (C2, Orchestrator) | High-performance asynchronous REST microservice APIs |
| | Flask | 3.1.3 | Lightweight WSGI server for Component 03 image inference |
| | Uvicorn | 0.54.0 | Asynchronous ASGI server for FastAPI services |
| **Deep Learning & ML** | PyTorch | 2.14.1 (C1), 2.13.0 (C3) | Deep learning model execution (DistilBERT & EfficientNet-B2) |
| | Hugging Face Transformers | 4.40.2 (C1) | Transformer model pipeline for text threat classification |
| | Torchvision | 0.28.0 (C3) | Image transforms and pretrained convolutional backbones |
| | Scikit-Learn | 1.4.2 (C1), 1.9.0 (C2) | Isotonic calibrator (C1) and ML awareness selector evaluation (C2) |
| | OpenCV (`cv2`) & Pillow | 5.0.0.93 / 12.3.0 | Visual preprocessing and Grad-CAM colormap rendering |
| **Data & Cryptography** | Pydantic | 2.13.5 | Strict schema validation and data contract enforcement |
| | SQLite | 3.x | Independent per-service persistence (`detection.db`, `component2.db`) |
| | Cryptography (Fernet) | 50.0.2 | Optional field-level encryption for C2 security audit logs |
| **Client & UI** | Mozilla Thunderbird | ≥ 115 (Supernova) | Native host client for the MailExtension user interface |
| | HTML5 / CSS3 / Vanilla JS | — | Responsive SOC Dashboard served natively from Orchestrator `:8000` |

---

### 2.7 Key Research Findings & Experimental Outcomes

#### 1. End-to-End Latency Benchmarks (CPU-Only, Windows 11 x64)
Empirical latency measurements recorded during live system verification on 2026-10-10:
- **Scenario 1 (Benign Text Email):** 911.8 ms (Verdict: `BENIGN`, Posture: `informational`)
- **Scenario 2 (Phishing Text Email):** 560.0 ms (Verdict: `THREAT_DETECTED`, Posture: `warning`, Score: 85.0)
- **Scenario 3 (Benign Text + Clean Image):** 1018.4 ms (Verdict: `BENIGN`, `is_stego: False`)
- **Scenario 4 (Benign Text + Stego Image):** 1006.9 ms (Verdict: `THREAT_DETECTED`, Posture: `warning`, `is_stego: True`, Prob: 0.9191)
- **Scenario 5 (Phishing Text + Stego Image):** 1808.9 ms (Verdict: `THREAT_DETECTED`, Posture: `warning`, Score: 89.0, `is_stego: True`)
- **Scenario 7 (Corrupted Image Fault-Injection):** 1170.0 ms (Verdict: `BENIGN`, Status: `partial`, C3 Status: `error`, Fail-Safe: Enforced)
- **Scenario 8 (Raw RFC 822 EML Upload):** 1065.8 ms (Verdict: `THREAT_DETECTED`, `is_stego: True`)

*Outcome:* The full multi-modal pipeline operates well within normal email reading latency thresholds (under 2.0 seconds end-to-end), even without hardware GPU acceleration.

#### 2. Component 01 Detection Metrics
- External held-out test evaluation on SpamAssassin corpus (N = 5,932):
  - **F1 Score:** 0.972 (Phishing class)
  - **Recall (Detection Rate):** 0.9566
  - **False Positive Rate:** 0.0054 (0.54%)
  - **Local Threat Intel Database:** 226,112 verified malicious URLs and 47,084 malicious domains.

#### 3. Component 02 Significant Methodological Negative Result
- Evaluated an ML classifier for scam category and trigger selection against a deterministic keyword baseline on held-out samples (N = 235):
  - **ML Model Macro F1:** 0.9457
  - **Deterministic Rule Baseline Macro F1:** **0.9704**
- *Research Conclusion:* In the absence of massive human-annotated awareness datasets, rule-based declarative templates outperform statistical models while providing 100% explainability and zero hallucination risk. Consequently, the ML selector was disabled in production (`ml_enabled: false`).

#### 4. Component 03 Model Checkpoint Verification
- Analysis of `best_efficientnet_b2.pth` embedded metadata:
  - **Validation F1 Score:** 0.7179 (selected at epoch 8)
  - **Validation Accuracy:** 0.7800 (78.0%)
  - **Explainability:** Validated Grad-CAM visual heatmaps highlighting high-frequency spatial perturbations.

---

## D. Suggested Content Blocks
- **Domain Overview Card Grid:** Social engineering, steganography, and policy defense pillars.
- **Interactive Methodology Timeline:** Data preparation → model training → contract design → integration testing.
- **Component Architecture Diagram:** Mermaid/SVG diagram illustrating the parallel inspection flow.
- **Technology Stack Badges:** Grouped by Backend, ML, Frontend, and Storage.
- **Empirical Results Data Table:** Comparing scenario latencies, verdicts, and postures.

---

## E. Supporting Files & Assets
- Architecture specification: `docs/SYSTEM_ARCHITECTURE.md`
- Request lifecycle: `docs/REQUEST_FLOW.md`
- Failure handling: `docs/FAILURE_HANDLING.md`
- Live scenarios runner: `orchestrator/tests/run_live_scenarios.py`
- Test fixtures: `orchestrator/tests/fixtures/` (`stego_image.png`, `white.png`)

---

## F. Missing Information (Requires Manual Input)
- Formal academic citations and bibliography entries (`M-08`).
- Component 03 original training scripts and source dataset descriptions (`M-04`).
- Formal human participant usability testing metrics (`M-03`).

---

## G. Supporting Evidence References
- `common_thesis_evidence/01_BACKGROUND_STAKEHOLDERS_SDG.md`: Sections 1.1–1.3
- `common_thesis_evidence/02_PROBLEM_AND_OBJECTIVES.md`: Sections 2.1–2.5
- `common_thesis_evidence/03_SOLUTION_AND_ARCHITECTURE.md`: Sections 3.1–3.7
- `common_thesis_evidence/06_TESTING_AND_EVALUATION.md`: Sections 6.1–6.3
- `Draft-Component01/src/component1/pipeline.py`: Lines 44–86
- `Draft-Component02/Draft-C-2-Test/src/component2/defense.py`: Lines 44–73, 200–222
- `Draft-Component03/RP final (stego)/model.py`: Lines 10–29
