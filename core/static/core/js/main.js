'use strict';

/* ══════════════════════════════════════════
   UTILITY HELPERS
══════════════════════════════════════════ */

function generateSessionId() {
  return 'sess_' + Math.random().toString(36).slice(2, 11);
}

function getSessionId() {
  let id = sessionStorage.getItem('ais_chat_session');
  if (!id) {
    id = generateSessionId();
    sessionStorage.setItem('ais_chat_session', id);
  }
  return id;
}

function getCsrfToken() {
  // Method 1: from cookie
  const name = 'csrftoken';
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) return decodeURIComponent(match[2]);

  // Method 2: from hidden input in the page
  const input = document.querySelector('[name=csrfmiddlewaretoken]');
  if (input) return input.value;

  // Method 3: from meta tag
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.getAttribute('content');

  return '';
}


/* ══════════════════════════════════════════
   NAVBAR BEHAVIOUR
══════════════════════════════════════════ */

(function initNavbar() {
  const navbar    = document.querySelector('.navbar');
  const hamburger = document.querySelector('.navbar__hamburger');
  const nav       = document.querySelector('.navbar__nav');
  const navLinks  = document.querySelectorAll('.navbar__nav a');

  if (!navbar) return;

  const onScroll = () => {
    navbar.classList.toggle('navbar--scrolled', window.scrollY > 10);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
      const open = nav.classList.toggle('navbar__nav--mobile-open');
      hamburger.setAttribute('aria-expanded', open);
    });
  }

  const currentPath = window.location.pathname;
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
})();


/* ══════════════════════════════════════════
   SCROLL REVEAL ANIMATION
══════════════════════════════════════════ */

(function initScrollReveal() {
  const targets = document.querySelectorAll('.reveal');
  if (!targets.length || !window.IntersectionObserver) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  targets.forEach(el => observer.observe(el));
})();


/* ══════════════════════════════════════════
   AI CHATBOT WIDGET
══════════════════════════════════════════ */

(function initChatbot() {
  const fab        = document.getElementById('chatbot-fab');
  const windowEl   = document.getElementById('chatbot-window');
  const closeBtn   = document.getElementById('chatbot-close');
  const messagesEl = document.getElementById('chatbot-messages');
  const inputEl    = document.getElementById('chatbot-input');
  const sendBtn    = document.getElementById('chatbot-send');
  const quickReplies = document.querySelectorAll('.quick-reply');

  if (!fab || !windowEl) return;

  let isOpen   = false;
  let isTyping = false;
  const sessionId = getSessionId();

  /* ── Open / close ── */
  function toggleChat(open) {
    isOpen = (typeof open === 'boolean') ? open : !isOpen;
    windowEl.classList.toggle('chatbot-window--open', isOpen);
    fab.setAttribute('aria-expanded', isOpen);
    if (isOpen && inputEl) inputEl.focus();
    const badge = fab.querySelector('.chatbot-fab__badge');
    if (badge && isOpen) badge.remove();
  }

  fab.addEventListener('click', () => toggleChat());
  if (closeBtn) closeBtn.addEventListener('click', () => toggleChat(false));

  /* ── Append message bubble ── */
  function appendMessage(text, role) {
    const msg = document.createElement('div');
    msg.classList.add('chatbot-msg', 'chatbot-msg--' + role);
    msg.textContent = text;
    messagesEl.appendChild(msg);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return msg;
  }

  /* ── Typing indicator ── */
  function showTyping() {
    if (isTyping) return;
    isTyping = true;
    const indicator = document.createElement('div');
    indicator.classList.add('chatbot-typing');
    indicator.id = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    messagesEl.appendChild(indicator);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function hideTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
    isTyping = false;
  }

  /* ── Send message to Django API ── */
  async function sendMessage(text) {
    const userText = text.trim();
    if (!userText) return;

    appendMessage(userText, 'user');
    if (inputEl) inputEl.value = '';
    showTyping();

    const csrfToken = getCsrfToken();

    try {
      const response = await fetch('/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          message: userText,
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error('Server returned ' + response.status);
      }

      const data = await response.json();
      hideTyping();

      if (data.reply) {
        appendMessage(data.reply, 'bot');
      } else {
        appendMessage("Sorry, I could not process that. Please try again.", 'bot');
      }

    } catch (err) {
      hideTyping();
      console.error('[Help desk] Error:', err);
      // Show a helpful message instead of a connection error
      appendMessage(
        "I'm having trouble connecting right now. Please try the Contact Us form to reach our team directly.",
        'bot'
      );
    }
  }

  /* ── Event listeners ── */
  if (sendBtn) sendBtn.addEventListener('click', () => sendMessage(inputEl.value));

  if (inputEl) {
    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(inputEl.value);
      }
    });
  }

  quickReplies.forEach(btn => {
    btn.addEventListener('click', () => sendMessage(btn.dataset.msg || btn.textContent));
  });

})();


/* ══════════════════════════════════════════
   GALLERY LIGHTBOX
══════════════════════════════════════════ */

(function initLightbox() {
  const galleryItems = document.querySelectorAll('.gallery-item');
  if (!galleryItems.length) return;

  const overlay = document.createElement('div');
  overlay.style.cssText = [
    'display:none',
    'position:fixed',
    'inset:0',
    'z-index:10000',
    'background:rgba(0,0,0,0.92)',
    'cursor:pointer',
    'align-items:center',
    'justify-content:center'
  ].join(';');

  overlay.innerHTML =
    '<button style="position:absolute;top:20px;right:28px;background:none;border:1px solid rgba(255,255,255,.6);color:white;font-size:.9rem;padding:8px 12px;cursor:pointer" aria-label="Close">Close</button>' +
    '<img id="lightbox-img" alt="" style="max-width:90vw;max-height:88vh;object-fit:contain;box-shadow:0 24px 80px rgba(0,0,0,0.6)">' +
    '<p id="lightbox-caption" style="position:absolute;bottom:24px;left:0;right:0;text-align:center;color:rgba(255,255,255,0.75);font-size:0.92rem"></p>';

  document.body.appendChild(overlay);

  const lightboxImg = overlay.querySelector('#lightbox-img');
  const lightboxCap = overlay.querySelector('#lightbox-caption');
  const closeBtn    = overlay.querySelector('button');

  function openLightbox(src, caption) {
    lightboxImg.src = src;
    lightboxCap.textContent = caption || '';
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    overlay.style.display = 'none';
    document.body.style.overflow = '';
  }

  galleryItems.forEach(item => {
    item.addEventListener('click', () => {
      const img   = item.querySelector('img');
      const title = item.querySelector('.gallery-item__overlay h3');
      if (img) openLightbox(img.src, title ? title.textContent : '');
    });
  });

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay || e.target === closeBtn) closeLightbox();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });
})();


/* ══════════════════════════════════════════
   DASHBOARD CHART (Chart.js)
══════════════════════════════════════════ */

(function initDashboardChart() {
  const canvas = document.getElementById('inquiry-chart');
  if (!canvas || typeof Chart === 'undefined') return;

  const labels = JSON.parse(canvas.dataset.labels || '[]');
  const data   = JSON.parse(canvas.dataset.values || '[]');

  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Queries',
        data: data,
        backgroundColor: 'rgba(47,70,57,0.14)',
        borderColor: '#2f4639',
        borderWidth: 2,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0, color: '#65685f', font: { size: 11 } },
          grid: { color: 'rgba(0,0,0,0.05)' }
        },
        x: {
          ticks: { color: '#65685f', font: { size: 11 } },
          grid: { display: false }
        }
      }
    }
  });
})();


/* ══════════════════════════════════════════
   SMOOTH ANCHOR SCROLL
══════════════════════════════════════════ */

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top: top, behavior: 'smooth' });
    }
  });
});
