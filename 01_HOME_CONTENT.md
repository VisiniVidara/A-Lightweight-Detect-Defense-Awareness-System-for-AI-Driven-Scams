# 01 — Home Page Content (`01_HOME_CONTENT.md`)

This document specifies the verified, website-ready content for the **Landing Page (Home)** of the MailSentra Academic Research Website.

---

## A. Page Title
**MailSentra: Multi-Modal Email Threat Detection, Steganography Analysis & Defense Platform**

## B. Page Introduction
Welcome to the official academic research portal for the **MailSentra Integrated Email Security Platform**. MailSentra is an advanced research prototype designed to protect enterprise and individual email users against sophisticated, multi-vector cyber attacks. By synthesizing natural language processing, deep visual steganalysis, and policy-driven security reasoning, MailSentra bridges the critical gap between raw algorithmic threat detection and actionable, human-centered defense.

---

## C. Main Content Sections

### 1.1 Project Identity
- **Official Research Project Title:** Multi-Modal Email Threat Detection & Defense Platform (Platform Codename: *MailSentra* / *MailSentra-RP*)
- **Project Abbreviation:** MailSentra-RP
- **Research Domain:** Cybersecurity, Natural Language Processing, Applied Deep Learning, Steganography & Human-Centered Security Awareness
- **Academic Context:** Final Year Research Project / Common Research Thesis
- **System Version:** Version 1.0 — Research Prototype
- **Release Date:** October 2026 (Audit Baseline: October 10, 2026)
- **Deployment Mode:** Multi-Service Local Cluster (`127.0.0.1:8000–8003`), Operating in Shadow/Advisory Mode (`execution_state: "shadow_only"`)
- **Institution / Department:** `NOT AVAILABLE` (Placeholder: Faculty of Computing & Information Technology)
- **Academic Year:** `NOT AVAILABLE` (Documented Runtime: 2026)
- **Group Identification:** `NOT AVAILABLE` (Referenced as Integrated Research Group 2026)

---

### 1.2 Executive Introduction & Research Motivation

#### The Modern Threat Landscape
Email remains the primary initial access vector for advanced persistent threats, business email compromise (BEC), and automated cybercrime. Modern threat actors no longer rely solely on simple typographical errors or suspicious attachments. Instead, attacks have evolved into **multi-modal social engineering campaigns**:
1. **Deceptive Message Semantics & Sender Spoofing:** Spear-phishing emails leverage sophisticated social engineering cues, urgency triggers, and domain lookalike spoofing that bypass conventional reputation filters.
2. **Concealed Visual Payloads (Steganography):** Attackers increasingly embed covert data, command-and-control scripts, or malware download triggers inside legitimate-looking images (such as logos, banners, and photographic attachments), entirely undetectable to signature scanners and optical inspection.
3. **The User Awareness & Decision Deficit:** Conventional security tools act as black boxes—they either silently quarantine messages or present generic warning banners without explaining the nature of the risk, leaving users unprepared and prone to repeated error.

#### The MailSentra Solution
MailSentra introduces an end-to-end, multi-modal security pipeline operating directly within the user's workflow:
- **Comprehensive Email Threat Detection (C1):** Evaluates message headers, DNS reputation (SPF, DKIM, DMARC), URL threat intelligence (over 226,000 blacklisted entries), fine-tuned DistilBERT linguistic classification, and stylometric AI-authorship profiling.
- **Deep Image Steganography Detection (C3):** Employs an ImageNet-pretrained EfficientNet-B2 deep neural network to inspect image attachments for hidden payloads, accompanied by visual Grad-CAM activation heatmaps.
- **Policy-Driven Defense & Adaptive Awareness (C2):** Acts as the platform's central decision authority, evaluating an 18-rule declarative policy matrix to derive calibrated defense postures, advisory actions, and evidence-grounded educational guidance.
- **Unified Orchestration & Native Mail Client Integration:** Seamlessly coordinates asynchronous inspection through Mozilla Thunderbird without introducing brittle fusion models, guaranteeing that the platform **never fails open**.

---

### 1.3 Project Abstract

> **Academic Abstract:**  
> Modern email-borne attacks increasingly exploit multiple concurrent channels, combining social engineering text, domain impersonation, and concealed image steganography. Conventional defense solutions analyze these modalities in technical silos, offering binary safe/unsafe verdicts with minimal explanatory guidance for the recipient. This project presents **MailSentra**, an integrated, multi-modal email security platform that unites three independent detection and defense engines into a cohesive client-integrated pipeline.  
> The system orchestrates: (1) a four-stage email threat engine utilizing fine-tuned transformer models (DistilBERT), real-time DNS/reputation filtering, and stylometric AI text profiling; (2) a convolutional deep learning engine (EfficientNet-B2) performing image steganalysis with explainable Grad-CAM heatmaps; and (3) a declarative, policy-driven defense and awareness engine mapping heterogeneous evidence into five graded operational postures. Evaluated across eight live end-to-end scenarios, the platform demonstrates sub-2-second end-to-end multi-modal triage, zero fail-open occurrences under worker faults, and transparent, evidence-grounded awareness guidance rendered natively inside Mozilla Thunderbird and an integrated SOC dashboard.

---

### 1.4 Key Project Highlights

1. **Multi-Modal Cross-Channel Triaging:**  
   Simultaneously evaluates email text semantics, sender authentication, URL threat intel, and image attachment steganalysis in a single client request (`POST /api/analyze-email`).
2. **Autonomous Cross-Modal Posture Escalation:**  
   Demonstrated ability to detect attacks where text appears completely benign (threat score 6.0/100) but contains hidden payloads in image attachments, autonomously escalating the defense posture to `THREAT_DETECTED` with prominent user warnings.
3. **Strict Decision Authority & Model Preservation:**  
   Preserves 100% of the integrity of pre-trained machine learning checkpoints across isolated runtime environments without altering original weights or inventing uncalibrated fusion algorithms.
4. **Verifiable "Never Fail Open" Resiliency:**  
   Enforces a strict architectural contract: unanalyzed attachments or worker timeouts yield explicit `partial` and `analysis_incomplete` states, preventing deceptive "clean" ratings when defenses fail.
5. **Grounded, Educational Human-Centered Guidance:**  
   Delivers dynamic, evidence-grounded awareness guidance and tracks longitudinal user security evolution across seven vulnerability states, turning everyday triage into continuous training.
6. **Empirically Validated Architecture:**  
   Backed by 854 automated unit tests, 167 phase validation checks, 15 security audit probes, and 8 live multi-modal operational test cases.

---

## D. Suggested Content Blocks
- **Hero Banner:** System title, research badge ("Version 1.0 Research Prototype"), primary call-to-actions ("Explore Architecture", "Review Domain Research", "View Live Scenarios").
- **Metrics Grid Cards:** 4 key metrics cards (Sub-2s Latency, 226k+ Intel Records, 18 Policy Rules, 0 Fail-Open Guarantee).
- **Three Core Pillars Cards:** Component 01 (Text & Headers), Component 02 (Defense & Awareness), Component 03 (Steganography).
- **Interactive Architecture Flow:** High-level SVG/HTML flow diagram of the Thunderbird ↔ Orchestrator ↔ Worker microservice mesh.
- **Highlights Carousel / Grid:** 6 highlighted innovations with icon badges.

---

## E. Supporting Files & Assets
- High-level system architecture overview: `docs/SYSTEM_ARCHITECTURE.md`
- Core manifest: `unified-thunderbird/manifest.json`
- Extension icons: `unified-thunderbird/icons/icon128.png`, `icon48.png`, `icon32.png`, `icon16.png`
- Live demo scripts: `orchestrator/tests/run_live_scenarios.py`, `demo/test_dashboard_live.py`

---

## F. Missing Information (Requires Manual Input)
- Official institutional affiliation, department, and faculty seal/logo (`M-14`).
- Group member identities, academic supervisor, and co-supervisor names (`M-02`).
- Formal academic course code and degree qualification title (`M-14`).

---

## G. Supporting Evidence References
- `README.md`: Lines 1–45 (Platform overview and microservice table)
- `VERSION.txt`: Lines 1–8 (Release version, mode, platform)
- `orchestrator/app/main.py`: Lines 40–42, 147–165 (App definition, parallel worker dispatch)
- `docs/RESEARCH_CONTRIBUTIONS.md`: Lines 1–45 (Explicit scientific and engineering attributions)
- `common_thesis_evidence/00_PROJECT_OVERVIEW.md`: Sections 1.1–1.3, 3.1–3.3
