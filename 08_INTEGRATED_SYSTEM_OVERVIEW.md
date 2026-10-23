# 08 — Integrated System Overview & Technical Architecture (`08_INTEGRATED_SYSTEM_OVERVIEW.md`)

This document details the software architecture, microservice topology, data models, interface contracts, and end-to-end operational flows of the MailSentra platform.

---

## 1. System Architecture & Microservice Topology

MailSentra is deployed as a coordinated multi-service cluster running exclusively on loopback (`127.0.0.1`) on a single Windows 64-bit host:

```
                                  +---------------------------------------+
                                  |      Mozilla Thunderbird Client       |
                                  |   (Unified MailExtension WebExtension)|
                                  +-------------------+-------------------+
                                                      |
                                                      | HTTP POST /api/analyze-email
                                                      v
                                  +---------------------------------------+
                                  |         Orchestrator Gateway          |
                                  |         (FastAPI :8000 / No ML)       |
                                  +---------+-------------------+---------+
                                            |                   |
                     HTTP POST /api/v1/     |                   | HTTP POST /api/analyze
                     analyze/email          |                   | (Parallel image fan-out)
                                            v                   v
            +---------------------------------+   +---------------------------------+
            |       Component 01 Engine       |   |       Component 03 Engine       |
            |     (FastAPI :8001 / .venv-c1)  |   |     (Flask :8003 / .venv-c3)    |
            | - Prefilter (SPF, DKIM, DNS)    |   | - 224x224 Tensor Scaling        |
            | - DistilBERT Scam Classifier    |   | - EfficientNet-B2 Stego Model   |
            | - Stylometric AI Text Profiler  |   | - Grad-CAM Visual Heatmap       |
            | - Hybrid Risk Scorer            |   +----------------+----------------+
            +----------------+----------------+                    |
                             | Threat Score &                      | Stego Probability &
                             | Stage Evidence                      | Base64 Heatmap
                             +----------------+   +----------------+
                                              |   |
                                              v   v
                                  +---------------------------------------+
                                  |     Envelope Builder & Normalizer     |
                                  |  (SecurityAssessmentEnvelope Schema)  |
                                  +-------------------+-------------------+
                                                      |
                                                      | HTTP POST /api/v1/evaluate
                                                      | (Bearer Token Authorized)
                                                      v
                                  +---------------------------------------+
                                  |       Component 02 Defense Engine     |
                                  |     (FastAPI :8002 / .venv-c2)        |
                                  | - D3 Trigger Gate (Clean Bypass)      |
                                  | - Four-Factor Evidence Assessment     |
                                  | - C3 Direct Severity Arbitration      |
                                  | - Declarative 18-Rule Policy Match    |
                                  | - Evidence-Grounded Awareness Text    |
                                  | - Longitudinal Vulnerability Profiler |
                                  +-------------------+-------------------+
                                                      |
                                                      | Defense Response & Guidance
                                                      v
                                  +---------------------------------------+
                                  |        Response Assembly Engine       |
                                  |      (UnifiedAnalysisResponse Schema) |
                                  +---------+-------------------+---------+
                                            |                   |
                                            v                   v
            +---------------------------------+   +---------------------------------+
            |  Thunderbird In-Message Banner  |   |  Live SOC Demonstration Web UI  |
            | - Graded Warning & Action Badges|   | - Live Triage Feed & Log Stream |
            | - Why It Matters & Learning Text|   | - Grad-CAM Visual Inspection    |
            | - Grad-CAM Heatmap Inspector    |   | - 6 One-Click Demo Scenarios    |
            +---------------------------------+   +---------------------------------+
```

---

## 2. Microservice Deployment & Virtual Environment Isolation

To overcome mutually exclusive library dependencies across research components, each service runs in an isolated Python 3.11 virtual environment communicating over HTTP:

| Service Unit | Port | Runtime Directory | Python Env | Framework | Critical Pinned Dependencies |
|---|---|---|---|---|---|
| **Orchestrator** | 8000 | `orchestrator/` | `.venv-orchestrator` | FastAPI 0.142.2 | `httpx==0.28.1`, `pydantic==2.13.5` *(Strictly zero ML libraries)* |
| **Component 01** | 8001 | `Draft-Component01/` | `.venv-c1` | FastAPI 0.111.0 | `torch==2.14.1`, `transformers==4.40.2`, `scikit-learn==1.4.2`, `numpy==1.26.4` |
| **Component 02** | 8002 | `Draft-Component02/Draft-C-2-Test/` | `.venv-c2` | FastAPI 0.142.2 | `pydantic==2.13.5`, `cryptography==50.0.2`, `scikit-learn==1.9.0`, `numpy==2.4.6` |
| **Component 03** | 8003 | `Draft-Component03/RP final (stego)/` | `.venv-c3` | Flask 3.1.3 | `torch==2.13.0`, `torchvision==0.28.0`, `opencv-python==5.0.0.93`, `Pillow==12.3.0` |

---

## 3. Inter-Service Communication & Data Flow Sequence

Every email analysis follows a strictly choreographed 10-step lifecycle:

1. **Email Capture:** The user opens an email in Mozilla Thunderbird. The MailExtension extracts subject, sender, recipient, headers, body text, HTML, URLs, and image attachments.
2. **Gateway Ingestion:** The client sends an asynchronous HTTP POST request to `http://127.0.0.1:8000/api/analyze-email`.
3. **Correlation Assignment:** The Orchestrator assigns a unique `request_id` (e.g., `req-a1b2c3d4`) and initializes an execution timer.
4. **Parallel Worker Dispatch:** The Orchestrator fans out two simultaneous calls via `asyncio.gather`:
   - Text, headers, and metadata are dispatched to Component 01 (`POST :8001/api/v1/analyze/email`).
   - Every image attachment is dispatched concurrently to Component 03 (`POST :8003/api/analyze`).
5. **Worker Inference:**
   - C1 executes its 4-stage pipeline, returning a hybrid threat score (0–100), risk band, and stage breakdown.
   - C3 scales each image to 224×224, executes EfficientNet-B2 inference, generates a Grad-CAM activation map, and encodes it as Base64 PNG.
6. **Canonical Envelope Construction:** The Orchestrator normalizes worker responses into a strictly validated `SecurityAssessmentEnvelope` (`schemas.py`), mapping threat indicators to typed evidence items and appending the SHA-256 hash of any flagged steganographic image.
7. **D3 Trigger & Evaluation Gate:**
   - If the envelope is completely clean, Component 02 returns `422 no_positive_finding`. The Orchestrator catches this, submits a lightweight `POST :8002/api/v1/scan-tick`, and synthesizes a baseline benign response (`RULE-006`).
   - If findings exist, the envelope is submitted to `POST :8002/api/v1/evaluate` accompanied by a secret Bearer authorization token.
8. **Policy Decision & Severity Arbitration:**
   - Component 02 computes four assessment factors: score band, evidence strength, reliability, and consequence.
   - Evaluates the C3 direct severity path (`stego_path.py`) and executes `select_combined_winner` arbitration, ensuring that higher-severity steganographic findings elevate overall posture.
   - Evaluates the 18-rule declarative policy matrix (`defense_policy_v1.json`) to select posture and advisory action.
   - Matches evidence to deterministic awareness templates to formulate plain-language explanations.
   - Updates the user's longitudinal vulnerability profile and records the event in SQLite.
9. **Unified Response Assembly:** The Orchestrator compiles findings into a canonical `UnifiedAnalysisResponse` containing verdict, posture, score, C1 details, C3 heatmaps, defense action, and awareness text.
10. **Client & Dashboard Rendering:**
    - The Thunderbird MailExtension renders an in-message colored warning banner with actionable advice and collapsible Grad-CAM heatmaps.
    - The SOC Dashboard (`:8000/dashboard`) updates its real-time incident triage table and metrics counters.

---

## 4. Resilience, Degradation & Fail-Safe Invariants

The platform enforces rigorous architectural fail-safes documented in `docs/FAILURE_HANDLING.md`:

- **Never Fail Open:** If Component 01 or Component 03 times out, crashes, or receives corrupted input, the platform **never** defaults to a "Clean" or "Safe" verdict.
- **Explicit Status Transparency:** The overall response status is marked `partial`, and the affected worker status is explicitly reported as `error` or `unavailable`.
- **Degraded Fallback Posture:** If Component 02 becomes unreachable, the Orchestrator activates a hardcoded conservative fallback rule (`DEGRADED_FALLBACK`), assigning a cautious posture to safeguard the user until policy services recover.
- **Non-Fatal Audit Failures:** In both C1 and C2, database logging errors are trapped and handled gracefully, guaranteeing that audit storage issues never impede real-time threat detection.

---

## 5. Supporting Evidence References
- `docs/SYSTEM_ARCHITECTURE.md`: Complete microservice specification
- `docs/REQUEST_FLOW.md`: Step-by-step lifecycle trace
- `docs/FAILURE_HANDLING.md`: Resilience and error handling contracts
- `orchestrator/app/main.py`: Lines 143–250 (Parallel dispatch and envelope orchestration)
- `orchestrator/app/services/evidence_mapper.py`: Lines 74–235 (Multi-modal evidence normalization)
- `Draft-Component02/Draft-C-2-Test/src/component2/stego_path.py`: Lines 300–361 (Severity arbitration)
