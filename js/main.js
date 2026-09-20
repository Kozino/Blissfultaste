/* Blissful Tastes Restaurant — interactions */
(function () {
  'use strict';

  // Current year
  document.querySelectorAll('#year').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Sticky header shadow
  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('scrolled', window.scrollY > 8);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Mobile navigation
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('mainNav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      toggle.classList.toggle('open');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('open');
        toggle.classList.remove('open');
      });
    });
  }

  // Order-food dropdowns
  document.querySelectorAll('[data-order-toggle]').forEach(function (btn) {
    var wrap = btn.closest('.order-wrap');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      // close any other open dropdown
      document.querySelectorAll('.order-wrap.open').forEach(function (w) {
        if (w !== wrap) w.classList.remove('open');
      });
      wrap.classList.toggle('open');
    });
  });
  document.addEventListener('click', function () {
    document.querySelectorAll('.order-wrap.open').forEach(function (w) {
      w.classList.remove('open');
    });
  });

  // Reveal-on-scroll
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('vis');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('vis'); });
  }
})();
