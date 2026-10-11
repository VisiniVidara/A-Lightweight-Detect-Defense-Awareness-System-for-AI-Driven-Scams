// MailSentra Product Simulator & Interactivity Script

const SCENARIOS = {
  scenario4: {
    name: "Covert Steganography Escalation",
    subject: "Fwd: Updated Q4 Marketing Strategy Asset",
    from: "colleague.design@partner-agency.com",
    body: "Hi team, please find attached the high-resolution logo banner for the upcoming regional product launch. Let me know if you need SVG vectors.",
    hasImage: true,
    imageSrc: "assets/stego_image.png",
    riskScore: 6,
    verdict: "THREAT_DETECTED",
    posture: "warning",
    matchedRule: "RULE-012 (Stego Attachment Confirmed)",
    headline: "Covert Payload Detected in Image Attachment",
    sub: "Steganography Analysis: EfficientNet-B2 flagged high-frequency spatial payload (Probability: 91.91%). Defense posture autonomously escalated.",
    tone: "rose",
    stegoProb: "91.91%",
    stegoClass: "Stego Detected",
    latency: "1006.9 ms"
  },
  scenario2: {
    name: "Credential Harvesting Spear-Phishing",
    subject: "URGENT: Microsoft 365 Password Expiration in 24 Hours",
    from: "security-update@account-microsoft-verify.net",
    body: "Your organizational credentials will expire today. Immediate action required. Visit the secure portal at https://login.microsoftonline.fake-portal.ru/auth to retain mailbox access.",
    hasImage: false,
    riskScore: 85,
    verdict: "THREAT_DETECTED",
    posture: "warning",
    matchedRule: "RULE-009 (High-Confidence Phishing Text & Lookalike Domain)",
    headline: "Dangerous Deception & Credential Theft Attempt",
    sub: "Linguistic Analysis: DistilBERT NLP classified message as phishing (Confidence: 94.2%). Lookalike domain detected. Never click authentication links.",
    tone: "rose",
    stegoProb: "N/A (No Images)",
    stegoClass: "Not Applicable",
    latency: "560.0 ms"
  },
  scenario1: {
    name: "Verified Benign Business Email",
    subject: "Agenda for Tomorrow's Architecture Sync",
    from: "dev-team@internal-corp.org",
    body: "Hi team, here is the tentative agenda for our weekly architecture review meeting at 10:00 AM UTC. Please review the proposal ahead of time.",
    hasImage: false,
    riskScore: 2,
    verdict: "BENIGN",
    posture: "informational",
    matchedRule: "RULE-006 (Standard Clean Mail Ingestion)",
    headline: "Verified Legitimate Sender & Safe Content",
    sub: "SPF, DKIM, and DMARC checks passed. Text classification confirms authentic internal correspondence.",
    tone: "green",
    stegoProb: "Clean",
    stegoClass: "Clean / None",
    latency: "911.8 ms"
  },
  scenario5: {
    name: "Composite Multi-Vector Attack",
    subject: "Final Notice: Wire Transfer Invoice & Banking Voucher",
    from: "billing-finance@exec-wire-transfer.com",
    body: "Attached is the amended wire transfer voucher. Process payment immediately before close of business to prevent contract termination.",
    hasImage: true,
    imageSrc: "assets/stego_image.png",
    riskScore: 89,
    verdict: "THREAT_DETECTED",
    posture: "warning",
    matchedRule: "RULE-015 (Corroborated Dual-Vector Threat)",
    headline: "Severe Multi-Modal Attack: Phishing Text + Concealed Payload",
    sub: "Both text deception and steganography confirmed. Urgency pressure detected; concealed carrier payload identified in attachment.",
    tone: "rose",
    stegoProb: "94.80%",
    stegoClass: "Stego Detected",
    latency: "1808.9 ms"
  },
  scenario7: {
    name: "Corrupted Attachment Resiliency",
    subject: "Project Photos (Archive Attached)",
    from: "external-client@design-studio.io",
    body: "Sharing the raw photographic assets for the layout. Let us know if you encounter compression artifacts.",
    hasImage: true,
    imageSrc: "assets/white.png",
    riskScore: 4,
    verdict: "BENIGN (Partial)",
    posture: "informational",
    matchedRule: "RULE-003 (Never-Fail-Open Error Trapped)",
    headline: "Attachment Inspection Incomplete (Fault Safely Isolated)",
    sub: "Attachment payload unreadable or corrupted. The system flagged status=partial and never failed open to safe. Recheck before downloading.",
    tone: "amber",
    stegoProb: "null (Error trapped)",
    stegoClass: "Analysis Incomplete",
    latency: "1170.0 ms"
  }
};

function renderScenario(key) {
  const s = SCENARIOS[key];
  if (!s) return;

  // Update Email Elements
  document.getElementById('simSubject').textContent = s.subject;
  document.getElementById('simFrom').textContent = s.from;
  document.getElementById('simBody').textContent = s.body;

  // Warning Banner
  const banner = document.getElementById('simBanner');
  banner.className = 'warning-banner-mock ' + s.tone;
  document.getElementById('simHeadline').textContent = s.headline;
  document.getElementById('simSub').textContent = s.sub;

  // Attachment display
  const attachArea = document.getElementById('simAttachmentArea');
  if (s.hasImage) {
    attachArea.style.display = 'block';
    document.getElementById('simImage').src = s.imageSrc;
  } else {
    attachArea.style.display = 'none';
  }

  // Telemetry items
  document.getElementById('simScore').textContent = s.riskScore + " / 100";
  document.getElementById('simVerdict').textContent = s.verdict;
  document.getElementById('simPosture').textContent = s.posture.toUpperCase();
  document.getElementById('simRule').textContent = s.matchedRule;
  document.getElementById('simStego').textContent = s.stegoProb;
  document.getElementById('simLatency').textContent = s.latency;
}

document.addEventListener('DOMContentLoaded', () => {
  const scenarioBtns = document.querySelectorAll('.scenario-btn');
  scenarioBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      scenarioBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderScenario(btn.getAttribute('data-scenario'));
    });
  });

  // Default initial scenario: Scenario 4 (Stego Escalation)
  renderScenario('scenario4');
});
