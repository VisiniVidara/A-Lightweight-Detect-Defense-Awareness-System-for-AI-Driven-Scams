[README.md](https://github.com/user-attachments/files/33895961/README.md)
# A Lightweight Detect, Defense & Awareness System For AI - Scams

**Version 1.0 – Research Prototype** · Windows 10/11 x64 · Python 3.11 · Local multi-service deployment · Shadow / advisory mode

## Overview

This integrates three independently developed research components into one email-security pipeline, delivered to the user through Mozilla Thunderbird and to an examiner through a live dashboard.

| Part | Role |
|---|---|
| **Component 01 (C1)** | Email threat detection: scam/phishing classification, URL/domain, authentication, impersonation and AI-generated-text indicators |
| **Component 02 (C2)** | Defense and awareness decision layer: policy-driven posture, action and user-awareness guidance, audit trail |
| **Component 03 (C3)** | Image steganography detection (EfficientNet-B2, Clean vs Stego) with Grad-CAM |
| **Orchestrator** | Lightweight FastAPI gateway that coordinates the workers (no ML) |
| **Unified Thunderbird MailExtension** | Single client; talks only to the Orchestrator |
| **Dashboard** | Integrated SOC / demonstration dashboard served at `/dashboard` |

## Architecture

```
            Thunderbird (Unified MailExtension)
                         |
                         v
               Orchestrator  :8000
                  /            \
                 v              v
          C1 :8001 (email)   C3 :8003 (images)
                  \            /
                   v          v
                SecurityAssessmentEnvelope
                         |
                         v
                    C2 :8002
          (defense policy + awareness)
                         |
                         v
              UnifiedAnalysisResponse
                         |
                         v
          Thunderbird warning  +  Dashboard
```

- **C1 owns** email-threat scoring.
- **C3 owns** steganography inference.
- **C2 owns** defense policy and awareness; it is the final decision layer.
- **The Orchestrator coordinates only**: it assigns `request_id`, routes inputs, normalises evidence, calls C2 and assembles the response.
- **No new fusion/ML model was introduced**, and no new risk score is computed by the Orchestrator.

Each service runs in its own Python 3.11 virtual environment because their pinned dependencies (PyTorch, scikit-learn, NumPy versions) are mutually incompatible.

| Service | Address |
|---|---|
| Orchestrator + Dashboard | http://127.0.0.1:8000 (`/dashboard`) |
| Component 01 | http://127.0.0.1:8001 |
| Component 02 | http://127.0.0.1:8002 |
| Component 03 | http://127.0.0.1:8003 |

All services bind to loopback only.

## Quick start (Windows)

1. Install Python 3.11 (64-bit, "Add to PATH").
2. First time only: run `SETUP_SYSTEM.bat`
3. Install `dist\vishini-unified-thunderbird.xpi` in Thunderbird (Tools → Add-ons → Install Add-on From File).
4. Run `START_SYSTEM.bat` and open http://127.0.0.1:8000/dashboard
5. `VERIFY_SYSTEM.bat` checks the installation; `STOP_SYSTEM.bat` stops everything.

## Protected model artifacts

Five trained checkpoints are never modified; their SHA256 values are in `installation/model_hashes.sha256` and are checked by setup and verify.
