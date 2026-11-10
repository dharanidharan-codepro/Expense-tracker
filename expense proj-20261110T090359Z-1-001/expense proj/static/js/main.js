/**
 * main.js — Interactive UX & Micro-Animations for Smart Expense Tracker
 * Features:
 *  - Animated number counter for metrics & totals
 *  - Dynamic button ripple effect
 *  - Navbar scroll blur & elevation
 *  - Alert auto-dismiss with fade out
 *  - Active link state management
 */

document.addEventListener('DOMContentLoaded', function () {

  // ── 1. Animated Number Counter ──
  function animateValue(element, start, end, duration, isCurrency, prefix) {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      // Smooth easeOutExpo curve
      const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      const current = start + (end - start) * easeProgress;

      if (isCurrency) {
        element.textContent = (prefix || '₹') + current.toLocaleString('en-IN', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      } else {
        element.textContent = Math.round(current).toLocaleString('en-IN');
      }

      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  }

  // Animate summary values on dashboard and report pages
  const valueElements = document.querySelectorAll('.summary-value, .report-stat-value');
  valueElements.forEach((el) => {
    const rawText = el.textContent.trim();
    // Check if it's a currency value like ₹1,234.56 or 1234.56
    const isCurrency = rawText.includes('₹') || rawText.includes('$');
    const numericMatch = rawText.replace(/[^0-9.]/g, '');
    const num = parseFloat(numericMatch);

    if (!isNaN(num) && num > 0) {
      el.textContent = isCurrency ? '₹0.00' : '0';
      // Trigger counter with small stagger
      setTimeout(() => {
        animateValue(el, 0, num, 1200, isCurrency, '₹');
      }, 100);
    }
  });

  // ── 2. Button Ripple Micro-Interaction ──
  document.querySelectorAll('.btn, .quick-action-btn').forEach((btn) => {
    btn.addEventListener('click', function (e) {
      const circle = document.createElement('span');
      const diameter = Math.max(btn.clientWidth, btn.clientHeight);
      const radius = diameter / 2;
      const rect = btn.getBoundingClientRect();

      circle.style.width = circle.style.height = `${diameter}px`;
      circle.style.left = `${e.clientX - rect.left - radius}px`;
      circle.style.top = `${e.clientY - rect.top - radius}px`;
      circle.classList.add('btn-ripple');

      const ripple = btn.querySelector('.btn-ripple');
      if (ripple) ripple.remove();

      btn.appendChild(circle);
    });
  });

  // ── 3. Auto-dismiss flash messages ──
  const alerts = document.querySelectorAll('.alert.fade.show');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ── 4. Navbar Scroll Glass Effect ──
  const navbar = document.getElementById('mainNavbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 30) {
        navbar.style.padding = '0.55rem 0';
        navbar.style.background = 'rgba(15, 23, 42, 0.96)';
        navbar.style.boxShadow = '0 12px 35px rgba(0, 0, 0, 0.3)';
      } else {
        navbar.style.padding = '0.85rem 0';
        navbar.style.background = 'rgba(15, 23, 42, 0.88)';
        navbar.style.boxShadow = '0 8px 30px rgba(0, 0, 0, 0.2)';
      }
    });
  }

  // ── 5. Highlight active nav link ──
  const currentPath = window.location.pathname;
  document.querySelectorAll('#mainNavbar .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

});
