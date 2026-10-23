# 11 — Master Academic Website Content (`11_WEBSITE_MASTER_CONTENT.md`)

This consolidated master document integrates the complete, verified content for all seven mandatory academic website sections in their proper logical presentation order.

---

# SECTION 1: HOME

## 1.1 Project Identity & Header
- **Official Research Title:** Multi-Modal Email Threat Detection & Defense Platform (Codename: *MailSentra* / *MailSentra-RP*)
- **Platform Subtitle:** A Lightweight Multi-Modal Detection, Visual Steganalysis, and Policy-Driven Defense Platform for Email Security
- **Version:** Version 1.0 (Research Prototype)
- **Deployment Mode:** Multi-Service Local Cluster (`127.0.0.1:8000–8003`), Operating in Shadow/Advisory Mode
- **Institution:** `NOT AVAILABLE` (Placeholder: Faculty of Computing & Information Technology)
- **Academic Year:** 2026

## 1.2 Introduction & Research Motivation
Email remains the primary attack vector for advanced persistent threats, business email compromise (BEC), and automated cyber manipulation. Modern adversaries no longer rely solely on simple typos or malicious executable attachments. Attacks have evolved into multi-modal campaigns that distribute threat cues across linguistic manipulation, domain impersonation, and covert payloads concealed inside innocent-looking images (digital steganography).

Existing defensive tools examine these vectors in technical silos:
1. Conventional filters inspect headers and body text but ignore pixel-level steganography.
2. Endpoint security tools inspect attachments with binary signatures, failing to uncover steganographic data hidden in valid PNG or JPEG structures.
3. Most gateways deliver opaque, binary verdicts ("Safe" or "Quarantined") with zero contextual reasoning, leaving users untrained and vulnerable to repeat attacks.

**MailSentra** bridges this gap by unifying deep linguistic analysis, convolutional visual steganalysis, and policy-driven security reasoning into a single client-integrated pipeline operating natively inside Mozilla Thunderbird.

## 1.3 Project Abstract
> Modern email-borne cyber attacks increasingly exploit distributed, multi-modal attack surfaces—combining social engineering text, domain impersonation, and concealed image steganography. Conventional defense solutions analyze these modalities in technical silos, offering binary safe/unsafe verdicts with minimal explanatory guidance for the recipient. This project presents **MailSentra**, an integrated, multi-modal email security platform that unites three independent detection and defense engines into a cohesive client-integrated pipeline.  
> The system orchestrates: (1) a four-stage email threat engine utilizing fine-tuned transformer models (DistilBERT), real-time DNS/reputation filtering, and stylometric AI text profiling; (2) a convolutional deep learning engine (EfficientNet-B2) performing image steganalysis with explainable Grad-CAM heatmaps; and (3) a declarative, policy-driven defense and awareness engine mapping heterogeneous evidence into five graded operational postures. Evaluated across eight live end-to-end scenarios, the platform demonstrates sub-2-second end-to-end multi-modal triage, zero fail-open occurrences under worker faults, and transparent, evidence-grounded awareness guidance rendered natively inside Mozilla Thunderbird and an integrated SOC dashboard.

## 1.4 Core Highlights
- **Atomic Multi-Modal Triage:** Simultaneously analyzes email text, authentication headers, and image attachments in a single request.
- **Cross-Modal Posture Escalation:** Autonomously escalates defense postures to `THREAT_DETECTED` when an email with benign text contains a covert steganographic payload.
- **Zero-ML Gateway Coordination:** Coordinates microservices via asynchronous dispatch without modifying trained models or inventing unvalidated fusion formulas.
- **Strict "Never Fail Open" Resiliency:** Enforces explicit `partial` and `analysis_incomplete` states when worker services encounter corrupted data.
- **Evidence-Grounded Awareness:** Translates raw detection signals into educational explanations and tracks longitudinal user security evolution across seven progression states.
- **Empirically Validated:** Verified across 854 unit tests, 167 phase checks, 15 security audit probes, and 8 live multi-modal test scenarios.

---

# SECTION 2: DOMAIN

## 2.1 Research Background & Problem Statement
Cyber threats exploit human cognitive vulnerabilities and structural blind spots in enterprise communication systems. Modern email deception combines sophisticated social engineering phrasing, lookalike domain spoofing, and steganographic payload delivery.

### Overall Problem Statement
> *Modern email-borne cyber attacks increasingly exploit distributed, multi-modal attack surfaces—combining social engineering text, domain impersonation, and concealed image steganography. Defenses in common practice evaluate these vectors in isolation and deliver opaque, binary verdicts without contextual explanations. Consequently, multi-channel attacks bypass perimeter filters, and recipient end users—lacking actionable reasoning—remain vulnerable to persistent manipulation.*

### Structured Research Subproblems
1. **Subproblem 1 (Linguistic & Infrastructure Deception):** Detecting deceptive text, sender spoofing, and malicious URLs with explainable intermediate stages *(Component 01)*.
2. **Subproblem 2 (Visual Payload Concealment):** Detecting steganographic data hidden inside digital image attachments with visual feature localization *(Component 03)*.
3. **Subproblem 3 (Proportional Action & User Awareness):** Synthesizing multi-modal evidence into calibrated defense postures and grounded educational guidance *(Component 02)*.
4. **Subproblem 4 (Unified Asynchronous Orchestration):** Composing heterogeneous, dependency-incompatible microservices into an atomic, fail-safe client pipeline *(Orchestrator Gateway)*.

## 2.2 Research Objectives
- **Objective 1:** Implement a 4-stage threat detection engine combining SPF/DKIM verification, DistilBERT classification, and stylometric AI profiling with hard-evidence score floors.
- **Objective 2:** Train an EfficientNet-B2 deep convolutional network for binary clean/stego classification with explainable Grad-CAM heatmaps.
- **Objective 3:** Construct a declarative 18-rule policy engine and severity arbitration layer that outputs calibrated five-level defense postures.
- **Objective 4:** Develop an evidence-grounded awareness system and longitudinal vulnerability profiler tracking user security evolution.
- **Objective 5:** Architect an asynchronous FastAPI gateway that coordinates parallel worker calls and guarantees never-fail-open error handling.
- **Objective 6:** Deploy a native Mozilla Thunderbird MailExtension and SOC demonstration dashboard to validate end-to-end multi-modal email triaging.

## 2.3 Integrated System Architecture & Pipeline
```
[Mozilla Thunderbird MailExtension]
         │ (HTTP POST /api/analyze-email)
         ▼
[Orchestrator Gateway (:8000)]
   ├── Parallel Dispatch (asyncio.gather)
   │     ├──► [Component 01 (:8001)] ──► DistilBERT & DNS Intel ──► Risk Score (0-100)
   │     └──► [Component 03 (:8003)] ──► EfficientNet-B2 CNN   ──► Stego Prob & Grad-CAM
   │
   ├── Canonical Envelope Normalization (SecurityAssessmentEnvelope)
   │
   └──► [Component 02 (:8002)] ──► 18-Rule Policy Engine ──► Graded Posture & Awareness
         │
         ▼
[Unified Client Delivery] ──► Thunderbird In-Message Banner & SOC Dashboard Feed
```

## 2.4 Empirical Research Findings
1. **Multi-Modal Latency:** End-to-end processing across all three microservices completes in **560 ms to 1809 ms** (under CPU-only execution on Windows 11 x64).
2. **Component 01 Performance:** Achieves **0.972 F1 score**, 0.9566 recall, and 0.0054 false-positive rate on held-out SpamAssassin corpora (N = 5,932).
3. **Component 02 Significant Negative Result:** Demonstrated that an ML classifier for scam categorization achieved macro F1 0.9457, while deterministic keyword templates achieved **macro F1 0.9704**. In accordance with scientific rigor, the ML selector was disabled in favor of explainable, zero-hallucination templates.
4. **Component 03 Checkpoint Validation:** EfficientNet-B2 model achieves **0.7179 validation F1** and 0.7800 validation accuracy at epoch 8, generating Base64 Grad-CAM visual heatmaps.
5. **Fail-Safe Integrity:** Corrupted attachments trigger explicit `partial` and `analysis_incomplete` states with `is_stego: null`, verifying the platform **never fails open**.

---

# SECTION 3: MILESTONES

## 3.1 Academic Assessment Milestones
- **Project Proposal (ACAD-M01):** Conceptual defense of the multi-modal email security framework and component scope division. *(Completed)*
- **Progress Presentation 1 (ACAD-M02):** Evaluation of baseline neural network architectures (DistilBERT and EfficientNet-B2) and initial policy contracts. *(Completed)*
- **Progress Presentation 2 (ACAD-M03):** Standalone prototype demonstrations, initial client add-ons, and integration planning. *(Completed)*
- **Final Assessment & Demonstration (ACAD-M04):** Comprehensive live demonstration of the integrated multi-modal platform operating end-to-end within Thunderbird and SOC dashboard. *(Completed / Verified 2026-10-10)*
- **Viva Voce / Oral Defense (ACAD-M05):** Technical defense of architectural decisions, failure invariants, and empirical findings. *(Prepared / Pending)*

## 3.2 Engineering & Integration Roadmap
- **Phases 0–2 (Oct 6, 2026):** Immutable baseline archive, four-virtual-environment dependency isolation, and path normalization.
- **Phases 3–5 (Oct 7, 2026):** Worker port reassignment (8000–8003), contract capture (14 payloads), and asynchronous FastAPI gateway construction.
- **Phases 6–8 (Oct 7, 2026):** Multi-modal parallel fan-out, 8 live E2E demonstration scenarios, and unified Thunderbird MailExtension deployment.
- **Phase 9 (Oct 10, 2026):** Production hardening, Component 02 upgrade (`c2-defense-policy` v1.5.0), and 6-stage regression verification.

---

# SECTION 4: DOCUMENTS

## Verified Research Documents Inventory
1. **Common Thesis Evidence Base:** Master compilation of technical data (`common_thesis_evidence/COMMON_THESIS_EVIDENCE_BASE.docx`).
2. **Project Overview & System Audit:** Complete technical architecture and live runtime verification (`00_PROJECT_OVERVIEW.md`).
3. **Problem Definition & Objectives Specification:** Formal subproblem mappings and objective traceability matrices (`02_PROBLEM_AND_OBJECTIVES.md`).
4. **Integrated Architecture Specification:** Full logical microservice topology and workflow sequences (`docs/SYSTEM_ARCHITECTURE.md`).
5. **Component Integration & Interface Analysis:** Analysis of inter-service contracts and compatibility challenges (`04_INTEGRATION_AND_INTERFACES.md`).
6. **Integrated Testing & Validation Report:** Comprehensive records of 854 unit tests and 8 live scenario benchmarks (`06_TESTING_AND_EVALUATION.md`).
7. **Research Contributions Matrix:** Attribution of scientific and engineering achievements across components (`docs/RESEARCH_CONTRIBUTIONS.md`).
8. **Academic Limitations & Future Work:** Transparent analysis of prototype boundaries and engineering roadmap (`docs/LIMITATIONS.md`, `docs/FUTURE_WORK.md`).

---

# SECTION 5: PRESENTATIONS

## Academic Presentation Catalogue & Demonstrations
- **Milestone Presentations:** Slide decks covering Project Proposal, Progress 1, Progress 2, and Final Defense.
- **Examiner Demonstration Guide:** Step-by-step scripted walkthrough covering the 6 core demonstration fixtures (`DEMO_GUIDE.md`).
- **Live Attack Scenarios:**
  - *Scenario 1:* Benign email baseline triage.
  - *Scenario 2:* Phishing email text detection and warning.
  - *Scenario 3:* Benign email with clean image attachment.
  - *Scenario 4:* Autonomous cross-modal escalation from covert steganography.
  - *Scenario 5:* Simultaneous multi-vector phishing and steganographic attack.
  - *Scenario 6:* Corrupted attachment fault-injection verifying fail-safe resilience.

---

# SECTION 6: ABOUT US

## Research Team Structure & Roles
- **Component 01 Lead (Email Threat Detection):** Lead researcher for NLP text deception classification, SPF/DKIM authentication, and stylometric AI-authorship profiling. *(Draft-Component01/)*
- **Component 02 Lead (Defense Policy & User Awareness):** Lead researcher for the declarative 18-rule policy engine, severity arbitration, deterministic awareness generation, and user vulnerability profiling. *(Draft-Component02/)*
- **Component 03 Lead (Image Steganography Detection):** Lead researcher for EfficientNet-B2 convolutional steganalysis, image preprocessing, and Grad-CAM visual heatmaps. *(Draft-Component03/)*
- **Systems & Integration Architect (Integration Gateway):** Systems architect for dependency-isolated multi-environment orchestration, canonical Pydantic contracts, unified Thunderbird extension, and SOC dashboard. *(orchestrator/, unified-thunderbird/)*
- **Academic Supervision:** Research project guidance and academic oversight provided by project supervisors and departmental evaluators.

*(Note: In accordance with academic privacy standards, student names and supervisor titles are held as cleared placeholders pending public clearance.)*

---

# SECTION 7: CONTACT US

## Academic Inquiries & Communication
- **Primary Channel:** Faculty Research Inquiries / Designated Academic Department
- **Official Research Group Email:** `NOT AVAILABLE` (Placeholder: `research-MailSentra@institution.ac.lk`)
- **Department Address:** `NOT AVAILABLE` (Placeholder: Department of Computing Sciences, University Research Complex)
- **Standard Inquiry Templates:** Structured templates available for examiner inquiries, reproduction requests, and collaborative research.
