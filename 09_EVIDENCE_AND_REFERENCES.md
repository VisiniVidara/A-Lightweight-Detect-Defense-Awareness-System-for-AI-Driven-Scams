# 09 — Evidence Register & Verification Status (`09_EVIDENCE_AND_REFERENCES.md`)

This document provides a consolidated register of primary evidence files, empirical test results, machine learning checkpoints, and verification statuses supporting all academic website claims.

---

## 1. Verified Machine Learning Model Checkpoints

All five machine learning model weights used by the platform are protected by immutable SHA-256 integrity baselines recorded in `installation/model_hashes.sha256`:

| Model / Artifact | Engine Component | Framework / Architecture | Workspace File Path | Verified SHA-256 Hash | Verification Status |
|---|---|---|---|---|---|
| **Text Classifier** | Component 01 | DistilBERT (`model.safetensors`) | `Draft-Component01/artifacts/models/text/model/model.safetensors` | `10265fb20b2207908b87c7aa3a8e97a3cf134c442eef01476d0cb7440498b301` | **VERIFIED (Bit-for-bit Match)** |
| **Score Calibrator** | Component 01 | Scikit-Learn Calibrator (`.joblib`) | `Draft-Component01/artifacts/models/text/calibrator.joblib` | `f34351aeec95804e389e875150821d3f9f9b5c3d25862343da3febe3ff0eb95b` | **VERIFIED (Bit-for-bit Match)** |
| **AI Text Detector** | Component 01 | Stylometric Estimator (`.joblib`) | `Draft-Component01/artifacts/models/aigen/model.joblib` | `dca4b123897eb33630f576e828469d4c7b2756df626c8b9356eb50e3ce7e4fbc` | **VERIFIED (Bit-for-bit Match)** |
| **Stego CNN Backbone** | Component 03 | PyTorch EfficientNet-B2 (`.pth`) | `Draft-Component03/RP final (stego)/saved_models/best_efficientnet_b2.pth` | `2fc3582ee0a90562e15bc99ec6a4db11623910c25dbcb4cfd5867ea32958742b` | **VERIFIED (Bit-for-bit Match)** |
| **Awareness Selector (v1)** | Component 02 | Scikit-Learn Selector (`.joblib`) | `Draft-Component02/Draft-C-2-Test/models/awareness_selector_v1.joblib` | `f4e15647eef090d8a6df64ea9bc59c6b65376db149a4253dd708b5f36e4f16b2` | **VERIFIED (Bit-for-bit Match)** |

*Integrity Confirmation:* Re-running `powershell -File scripts\verify-install.ps1` confirms Stage 4 passes with 5/5 hashes matching. Original trained models were 100% preserved during integration.

---

## 2. Empirical Test Execution Log (Conducted 2026-10-10)

| Suite Identifier | Executed Command | Test Scope | Output / Result Observed | Status |
|---|---|---|---|---|
| **TEST-01** | `pytest orchestrator/tests -q` | Orchestrator unit & gateway integration | **21 passed** in 2.56s | **PASS** |
| **TEST-02** | `pytest Draft-Component01/tests -q` | Component 01 threat detection & prefilter | **37 passed, 1 skipped** (exit code 0) | **PASS** |
| **TEST-03** | `pytest tests -q` (in `.venv-c2`) | Component 02 policy, defense, & profiler | **796 passed** in 52.03s | **PASS** |
| **TEST-04** | `python scripts/validate_all_phases.py` | Component 02 25-phase regression checks | **167 / 167 PASS** (incl. DB preservation) | **PASS** |
| **TEST-05** | `python scripts/audit_probe.py` | Component 02 security audit findings probe | **15 / 15 PASS** | **PASS** |
| **TEST-06** | `powershell scripts\verify-install.ps1` | 6-stage platform integrity diagnostic | **All 6 Stages PASS** (Ports, envs, hashes) | **PASS** |
| **TEST-07** | `python orchestrator/tests/run_live_scenarios.py` | 8 live end-to-end multi-modal scenarios | **8 / 8 Scenarios PASS** (Latency recorded) | **PASS** |
| **TEST-08** | `python demo/test_dashboard_live.py` | Live SOC Dashboard integration tests | **11 / 11 PASS** (Grad-CAM Base64 checked) | **PASS** |
| **TEST-09** | `node unified-thunderbird/tests/test_extension.js` | Thunderbird extension unit logic | **6 / 6 PASS** (Deduplication verified) | **PASS** |

---

## 3. Disclosed Technical Anomalies & Contradictions (Academic Rigor)

To ensure the academic website maintains scientific credibility, known discrepancies and edge cases are openly disclosed:

1. **Finding D-01 (Component 03 Concurrency Race Condition):**  
   - *Observation:* Rapid concurrent image submissions during high-speed parallel fan-out tests can trigger native PyTorch hook contention in Component 03's shared model object.
   - *Mitigation & Handling:* The Orchestrator safely traps worker unavailability, prevents process lockup, and enforces fail-safe degradation without corrupting client decisions.
2. **Finding D-02 (Component 03 Validation Metrics):**  
   - *Observation:* Metadata embedded within `best_efficientnet_b2.pth` records best validation F1 = 0.7179 and accuracy = 0.7800 at epoch 8. While no written test report existed in the original repository, these empirical figures are now documented transparently.
3. **Contradiction C-04 (C2 Model Baseline Hash):**  
   - *Observation:* `installation/model_hashes.sha256` preserves C2's v1 awareness selector model, whereas the updated runtime incorporates v2.0.0 artifacts while defaulting to deterministic template matching.
4. **Contradiction C-01 (System Name Divergence):**  
   - *Observation:* Four names exist across launchers, extensions, and documents. The academic website presents "Multi-Modal Email Threat Detection & Defense Platform" as the formal descriptive title and "MailSentra" as the project codename.

---

## 4. Primary Source Document Citations

- `INTEGRATION_PLAN.md`: "Three-Component Integration Plan", October 2026.
- `INTEGRATION_ANALYSIS.md`: "Three Component Integration Analysis & Technical Audit", October 2026.
- `FINAL_PROJECT_VALIDATION.md`: "Platform Validation & Regression Sign-off", October 2026.
- `FINAL_TECHNICAL_SUMMARY.md`: "Integrated Engineering Specifications", October 2026.
- `COMPONENT02_REPLACEMENT_REPORT.md`: "Component 02 Replacement & Policy Alignment Report", October 2026.
- `common_thesis_evidence/`: 12-document Common Thesis Evidence Base, compiled October 10, 2026.
