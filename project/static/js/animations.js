/**
 * GSAP scroll animations + premium smooth scroll (GSAP ScrollToPlugin)
 */
(function() {
  'use strict';

  function initGSAP() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);
    if (typeof ScrollToPlugin !== 'undefined') gsap.registerPlugin(ScrollToPlugin);

    var mainHome = document.querySelector('main.page-home');

    /* Premium smooth scroll: anchor links (same page) + hash on load */
    if (typeof ScrollToPlugin !== 'undefined') {
      var scrollToTarget = function(el) {
        if (!el) return;
        gsap.to(window, {
          duration: 1.2,
          scrollTo: { y: el, offsetY: 80 },
          ease: 'power3.inOut'
        });
      };
      document.querySelectorAll('a[href^="#"]').forEach(function(link) {
        var href = link.getAttribute('href');
        if (href === '#') return;
        var target = document.querySelector(href);
        if (!target) return;
        link.addEventListener('click', function(e) {
          e.preventDefault();
          scrollToTarget(target);
        });
      });
      if (window.location.hash) {
        var onLoad = document.querySelector(window.location.hash);
        if (onLoad) setTimeout(function() { scrollToTarget(onLoad); }, 100);
      }
    }

    /* Home page only: starting page animation */
    if (mainHome) {
      gsap.set(mainHome, { opacity: 0, y: 24 });
      gsap.to(mainHome, { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out', delay: 0.08 });
      /* Hero title/lead reveal (home clone classes) */
      gsap.utils.toArray('.home-hero-title, .home-hero-lead').forEach(function(el, i) {
        gsap.fromTo(el, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, delay: 0.25 + i * 0.08, ease: 'power2.out' });
      });
    }

    /* Sections: trigger early, animate quickly and smoothly */
    gsap.utils.toArray('.reveal-section').forEach(function(el) {
      gsap.fromTo(el, { opacity: 0, y: 32 }, {
        opacity: 1,
        y: 0,
        duration: 0.4,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 97%',
          toggleActions: 'play none none none'
        }
      });
    });

    /* Cards: trigger as they approach, fast stagger */
    gsap.utils.toArray('.reveal-card').forEach(function(el, i) {
      gsap.fromTo(el, { opacity: 0, y: 24 }, {
        opacity: 1,
        y: 0,
        duration: 0.35,
        delay: i * 0.04,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 97%',
          toggleActions: 'play none none none'
        }
      });
    });

    /* Hero text (legacy hero-title/hero-lead on other pages) */
    gsap.utils.toArray('.hero-title, .hero-lead').forEach(function(el, i) {
      gsap.fromTo(el, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, delay: i * 0.08, ease: 'power2.out' });
    });

    /* Section titles: trigger early, short duration */
    gsap.utils.toArray('.section-title').forEach(function(el) {
      gsap.fromTo(el, { opacity: 0, y: 16 }, {
        opacity: 1,
        y: 0,
        duration: 0.35,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 97%',
          toggleActions: 'play none none none'
        }
      });
    });

    /* Card hover scale (card-premium + home clone cards) */
    document.querySelectorAll('.card-premium, .home-content-card, .home-media-card, .home-theme-card, .home-brand-card').forEach(function(card) {
      card.addEventListener('mouseenter', function() {
        gsap.to(this, { scale: 1.02, boxShadow: '0 12px 40px rgba(61,54,53,0.12)', duration: 0.3, ease: 'power2.out' });
      });
      card.addEventListener('mouseleave', function() {
        gsap.to(this, { scale: 1, boxShadow: '0 4px 20px rgba(61,54,53,0.06)', duration: 0.3, ease: 'power2.out' });
      });
    });

    document.querySelectorAll('.btn-premium-primary, .btn-premium-dark').forEach(function(btn) {
      btn.addEventListener('mouseenter', function() {
        gsap.to(this, { y: -2, duration: 0.2, ease: 'power2.out' });
      });
      btn.addEventListener('mouseleave', function() {
        gsap.to(this, { y: 0, duration: 0.2, ease: 'power2.out' });
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGSAP);
  } else {
    initGSAP();
  }
})();
