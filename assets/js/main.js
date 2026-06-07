document.addEventListener('DOMContentLoaded', () => {
  navbarScroll();
  mobileMenu();
  smoothScroll();
  typeWriter();
  animateOnView();
  setActiveNav();
});

function navbarScroll() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  });
}

function mobileMenu() {
  const toggle = document.querySelector('.mobile-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (!toggle || !navLinks) return;
  toggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

function smoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

function typeWriter() {
  const el = document.querySelector('.typewriter');
  if (!el) return;
  const text = el.getAttribute('data-text') || el.textContent;
  el.textContent = '';
  let i = 0;
  function type() {
    if (i < text.length) {
      el.textContent += text.charAt(i);
      i++;
      setTimeout(type, 30 + Math.random() * 40);
    }
  }
  setTimeout(type, 1000);
}

function animateOnView() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-up');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.animate-on-view').forEach(el => observer.observe(el));
}

function setActiveNav() {
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    a.classList.toggle('active', href === current || (current === '' && href === 'index.html'));
  });
}

function switchTab(group, tab) {
  document.querySelectorAll(`.${group}-tab`).forEach(t => t.classList.remove('active'));
  document.querySelectorAll(`.${group}-content`).forEach(c => c.classList.remove('active'));
  document.getElementById(`${group}-${tab}`)?.classList.add('active');
  document.querySelector(`[data-tab="${group}-${tab}"]`)?.classList.add('active');
}
