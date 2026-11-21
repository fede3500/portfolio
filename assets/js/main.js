'use strict';

// Pointer-only depth: no continuous JS loop, and no motion on touch or reduced-motion.
const portraitStage = document.querySelector('.portrait-stage');
if (portraitStage) {
  const surface = portraitStage.closest('.portrait');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const reducedPortraitMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;
  let bounds = null;
  let pointerX = 0;
  let pointerY = 0;

  const resetPortrait = () => {
    cancelAnimationFrame(frame);
    frame = 0;
    bounds = null;
    portraitStage.classList.remove('is-active');
    portraitStage.style.removeProperty('transform');
  };
  surface.addEventListener('pointerenter', event => {
    if (event.pointerType === 'touch' || !finePointer.matches || reducedPortraitMotion.matches) return;
    bounds = surface.getBoundingClientRect();
    portraitStage.classList.add('is-active');
  });
  surface.addEventListener('pointermove', event => {
    if (!bounds || event.pointerType === 'touch') return;
    pointerX = event.clientX;
    pointerY = event.clientY;
    if (frame) return;
    frame = requestAnimationFrame(() => {
      frame = 0;
      if (!bounds) return;
      const clamp = value => Math.max(-1, Math.min(1, value));
      const rotateY = clamp((pointerX - bounds.left - bounds.width / 2) / (bounds.width / 2)) * 3.2;
      const rotateX = -clamp((pointerY - bounds.top - bounds.height / 2) / (bounds.height / 2)) * 3.2;
      portraitStage.style.transform = `translateY(-8px) scale(1.02) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg)`;
    });
  });
  surface.addEventListener('pointerleave', resetPortrait);
  finePointer.addEventListener('change', resetPortrait);
  reducedPortraitMotion.addEventListener('change', resetPortrait);
  window.addEventListener('blur', resetPortrait);
  document.addEventListener('visibilitychange', () => { if (document.hidden) resetPortrait(); });
}

// Native navigation also works without JavaScript.
const menu = document.querySelector('.mobile-menu');
if (menu) {
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => { menu.open = false; }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) { menu.open = false; menu.querySelector('summary').focus(); }
  });
  document.addEventListener('click', event => { if (menu.open && !menu.contains(event.target)) menu.open = false; });
  matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches) menu.open = false; });
}
const navLinks = [...document.querySelectorAll('.desktop-nav a[href^="#"]')];
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navLinks.forEach(link => {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });
  }, { rootMargin: '-10% 0px -65% 0px', threshold: 0 });
  navLinks.forEach(link => { const target = document.getElementById(link.hash.slice(1)); if (target) observer.observe(target); });
}
const footer = document.querySelector('.site-footer');
const catToggle = document.querySelector('.cat-toggle');
if (footer && catToggle) {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = false;
  let visible = !('IntersectionObserver' in window);
  const update = () => {
    footer.classList.toggle('motion-paused', paused || reduced.matches || document.hidden || !visible);
    catToggle.disabled = reduced.matches;
    catToggle.setAttribute('aria-pressed', String(!paused && !reduced.matches));
  };
  catToggle.addEventListener('click', () => { paused = !paused; update(); });
  reduced.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => { visible = entries[0].isIntersecting; update(); }, { rootMargin: '120px' }).observe(footer);
  update();
}
