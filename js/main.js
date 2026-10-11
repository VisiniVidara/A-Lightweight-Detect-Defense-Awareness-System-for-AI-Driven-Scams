// MailSentra Academic Research Portal — Interactive Navigation & Content Script

document.addEventListener('DOMContentLoaded', () => {
  // Navigation Section Switching (Tabs)
  const navLinks = document.querySelectorAll('.nav-link');
  const sectionPanels = document.querySelectorAll('.section-panel');

  function switchSection(targetId) {
    // Update nav links
    navLinks.forEach(link => {
      if (link.getAttribute('data-target') === targetId) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    // Update visible section panel
    sectionPanels.forEach(panel => {
      if (panel.id === targetId) {
        panel.classList.add('active');
      } else {
        panel.classList.remove('active');
      }
    });

    // Update URL hash without jump
    history.pushState(null, null, '#' + targetId);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('data-target');
      switchSection(targetId);
    });
  });

  // Handle direct hash navigation
  if (window.location.hash) {
    const hash = window.location.hash.substring(1);
    const validSections = ['home', 'domain', 'milestones', 'documents', 'presentations', 'about', 'contact'];
    if (validSections.includes(hash)) {
      switchSection(hash);
    }
  }

  // Handle in-page buttons that point to sections
  document.querySelectorAll('[data-switch-to]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = btn.getAttribute('data-switch-to');
      switchSection(targetId);
    });
  });

  // Secondary Tab Switching inside Domain & Milestones
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parentTabNav = btn.closest('.tab-nav');
      const targetContentId = btn.getAttribute('data-tab');
      const tabContainer = parentTabNav.parentElement;

      // Deactivate siblings in this nav
      parentTabNav.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Deactivate tab contents in this container
      tabContainer.querySelectorAll('.tab-content').forEach(content => {
        if (content.id === targetContentId) {
          content.classList.add('active');
        } else {
          content.classList.remove('active');
        }
      });
    });
  });

  // Contact Form Mock Submission
  const contactForm = document.getElementById('academicInquiryForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const feedbackBox = document.getElementById('formFeedback');
      if (feedbackBox) {
        feedbackBox.innerHTML = `
          <div class="callout callout-teal" style="margin-top: 1.5rem;">
            <div class="callout-title">✓ Inquiry Submitted Successfully</div>
            <p style="font-size: 0.9rem; color: #0d9488;">
              Thank you for reaching out. Your academic inquiry has been registered in the demonstration log. In a live deployment, this message is routed to the faculty project coordinator.
            </p>
          </div>
        `;
        contactForm.reset();
      }
    });
  }

  // Interactive System Working Flow Sample (Variations)
  const FLOW_DATA = {
    'var-stego': {
      step1Text: "Parses email stream: subject, sender, SPF/DKIM headers, body text, and PNG image attachment.",
      step1Meta: "Attachment: marketing_banner.png (77 KB)",
      c1Output: "Score 6/100 (Benign Text & Clean SPF)",
      c1Color: "#166534",
      c3Output: "Stego 91.91% + Grad-CAM Heatmap",
      c3Color: "#9f1239",
      latency: "1006.9 ms (CPU execution)",
      step3Text: "Normalizes evidence into canonical envelope. Attaches image SHA-256 (7a9e14c...).",
      envelope: "Envelope: SecurityAssessmentEnvelope (extra='forbid')",
      rule: "RULE-012 (Stego Confirmed Escalation)",
      posture: "WARNING (Escalated)",
      postureClass: "badge-status badge-amber",
      action: "show_prominent_warning (Advisory Only)",
      verdictBadge: "VERDICT: THREAT_DETECTED",
      verdictClass: "badge-status badge-amber",
      bannerBorder: "#f43f5e",
      bannerBg: "#fff1f2",
      headline: "🛡 Covert Payload Detected in Image Attachment",
      headlineColor: "#9f1239",
      bannerText: "Steganography Analysis: EfficientNet-B2 identified high-frequency spatial payload perturbations (Probability: 91.91%). The system autonomously escalated posture from benign text to active threat. Do not extract or execute attachment payloads.",
      bannerTextColor: "#4c0519",
      hasImage: true,
      imageSrc: "assets/stego_image.png",
      learningPoint: "Attackers use legitimate-looking logos and banners to slip payloads past gateway filters. Always inspect attachments flagged with spatial anomalies."
    },
    'var-phish': {
      step1Text: "Parses incoming phishing email: urgent credential warning, lookalike domain, and login hyperlink.",
      step1Meta: "Zero attachments • Suspicious URLs: 1",
      c1Output: "Score 85/100 (High Risk Phishing)",
      c1Color: "#9f1239",
      c3Output: "Not Triggered (No Image Attachments)",
      c3Color: "#64748b",
      latency: "560.0 ms (Fast Text Evaluation)",
      step3Text: "Maps DistilBERT prediction (94.2% conf) and lookalike domain flag to threat envelope.",
      envelope: "Envelope: Assessment ID assess-req-941",
      rule: "RULE-009 (Phishing Text & Lookalike Domain)",
      posture: "WARNING (Action Gated)",
      postureClass: "badge-status badge-amber",
      action: "show_prominent_warning (Block Quarantined)",
      verdictBadge: "VERDICT: THREAT_DETECTED",
      verdictClass: "badge-status badge-amber",
      bannerBorder: "#f43f5e",
      bannerBg: "#fff1f2",
      headline: "⚠️ Phishing Attack & Lookalike Domain Detected",
      headlineColor: "#9f1239",
      bannerText: "Linguistic Analysis: DistilBERT NLP classified this message as deceptive credential harvesting. Domain reputation failed. Never enter credentials or follow embedded links.",
      bannerTextColor: "#4c0519",
      hasImage: false,
      learningPoint: "Look closely at the sender domain. Spear-phishing emails frequently create false urgency to pressure recipients into hasty action."
    },
    'var-clean': {
      step1Text: "Parses internal team message: meeting agenda, authentic company domain, and valid DKIM signature.",
      step1Meta: "Zero attachments • Internal Correspondence",
      c1Output: "Score 2/100 (Verified Benign)",
      c1Color: "#166534",
      c3Output: "Not Triggered (No Attachments)",
      c3Color: "#64748b",
      latency: "911.8 ms (Complete Pipeline)",
      step3Text: "Trigger Gate (D3): Clean analysis routed via lightweight scan-tick endpoint (:8002/api/v1/scan-tick).",
      envelope: "Lightweight ScanTickRequest Recorded",
      rule: "RULE-006 (Standard Clean Mail Ingestion)",
      posture: "INFORMATIONAL",
      postureClass: "badge-status badge-green",
      action: "show_notice (Safe Verification)",
      verdictBadge: "VERDICT: BENIGN",
      verdictClass: "badge-status badge-green",
      bannerBorder: "#10b981",
      bannerBg: "#ecfdf5",
      headline: "✓ Authentic Sender & Legitimate Content",
      headlineColor: "#065f46",
      bannerText: "Email authentication passed (SPF, DKIM, DMARC valid). Linguistic classifier confirms authentic routine business communication.",
      bannerTextColor: "#064e3b",
      hasImage: false,
      learningPoint: "Verified internal messages with valid cryptographic signatures protect the organization against impersonation spoofing."
    },
    'var-corrupt': {
      step1Text: "Parses email containing an unreadable, truncated image file attachment.",
      step1Meta: "Attachment: corrupted_photo.png (Malformed Stream)",
      c1Output: "Score 4/100 (Benign Text Body)",
      c1Color: "#166534",
      c3Output: "Status: ERROR (Malformed Tensor)",
      c3Color: "#d97706",
      latency: "1170.0 ms (Fault Trapped Safely)",
      step3Text: "Traps C3 exception. Populates status=partial and is_stego=null to enforce Never-Fail-Open invariant.",
      envelope: "Envelope: Warnings[1] • Errors[1] Recorded",
      rule: "RULE-003 (Never-Fail-Open Error Trapped)",
      posture: "ANALYSIS_INCOMPLETE",
      postureClass: "badge-status badge-amber",
      action: "request_reanalysis (Caution Advisory)",
      verdictBadge: "STATUS: PARTIAL (FAIL-SAFE)",
      verdictClass: "badge-status badge-amber",
      bannerBorder: "#f59e0b",
      bannerBg: "#fffbeb",
      headline: "⚠️ Attachment Inspection Incomplete (Fault Safely Isolated)",
      headlineColor: "#92400e",
      bannerText: "The image attachment could not be parsed or inspected by the steganalysis engine. In compliance with platform safety guarantees, this message was NOT marked clean. Treat unverified attachments with caution.",
      bannerTextColor: "#78350f",
      hasImage: true,
      imageSrc: "assets/white.png",
      learningPoint: "Security tools must never fail open. A crashed or malformed detector must always notify the user that analysis could not be completed."
    }
  };

  const flowBtns = document.querySelectorAll('.flow-scenario-btn');
  flowBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      flowBtns.forEach(b => {
        b.classList.remove('active');
        b.style.background = '#fff';
        b.style.borderColor = 'var(--border-light)';
        b.style.color = 'var(--secondary)';
      });
      btn.classList.add('active');
      btn.style.background = 'var(--primary-subtle)';
      btn.style.borderColor = 'var(--primary-light)';
      btn.style.color = 'var(--primary)';

      const flowKey = btn.getAttribute('data-flow');
      const d = FLOW_DATA[flowKey];
      if (!d) return;

      document.getElementById('flowStep1Text').textContent = d.step1Text;
      document.getElementById('flowStep1Meta').textContent = d.step1Meta;
      
      const c1Elem = document.getElementById('flowC1Output');
      c1Elem.textContent = d.c1Output;
      c1Elem.style.color = d.c1Color;

      const c3Elem = document.getElementById('flowC3Output');
      c3Elem.textContent = d.c3Output;
      c3Elem.style.color = d.c3Color;

      document.getElementById('flowLatency').textContent = d.latency;
      document.getElementById('flowStep3Text').textContent = d.step3Text;
      document.getElementById('flowStep3Envelope').textContent = d.envelope;
      document.getElementById('flowRule').textContent = d.rule;

      const postureElem = document.getElementById('flowPosture');
      postureElem.textContent = d.posture;
      postureElem.className = d.postureClass;

      document.getElementById('flowAction').textContent = d.action;

      const verdictElem = document.getElementById('flowVerdictBadge');
      verdictElem.textContent = d.verdictBadge;
      verdictElem.className = d.verdictClass;

      const bannerBox = document.getElementById('flowBannerBox');
      bannerBox.style.borderLeftColor = d.bannerBorder;
      bannerBox.style.backgroundColor = d.bannerBg;

      const headlineElem = document.getElementById('flowBannerHeadline');
      headlineElem.textContent = d.headline;
      headlineElem.style.color = d.headlineColor;

      const textElem = document.getElementById('flowBannerText');
      textElem.textContent = d.bannerText;
      textElem.style.color = d.bannerTextColor;

      const imgContainer = document.getElementById('flowImageContainer');
      if (d.hasImage) {
        imgContainer.style.display = 'flex';
        document.getElementById('flowBannerImg').src = d.imageSrc;
      } else {
        imgContainer.style.display = 'none';
      }

      document.getElementById('flowLearningPoint').textContent = d.learningPoint;
    });
  });
});

