import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';
import { initHero } from './hero';

gsap.registerPlugin(ScrollTrigger);

const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!calm) {
  const touch = matchMedia('(hover: none)').matches;

  if (!touch) {
    const lenis = new Lenis({ duration: 1.2 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
    window.addEventListener('menu:toggle', (e) =>
      (e as CustomEvent<boolean>).detail ? lenis.stop() : lenis.start(),
    );
  }

  // Le hero épinglé doit être créé d'abord : il décale tout ce qui le suit.
  initHero();

  const mobile = innerWidth < 900;

  // IntersectionObserver plutôt que ScrollTrigger : aucune lecture de mise en page par élément.
  const reveals = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        reveals.unobserve(entry.target);
        gsap.to(entry.target, { autoAlpha: 1, y: 0, duration: 1.2, ease: 'power3.out' });
      });
    },
    { rootMargin: '0px 0px -12% 0px' },
  );
  gsap.utils.toArray<HTMLElement>('[data-reveal]').forEach((el) => {
    gsap.set(el, { autoAlpha: 0, y: 44 });
    reveals.observe(el);
  });

  // Sur mobile, les objets gardent leur flottaison mais pas de parallaxe au scroll.
  const parallax = mobile ? [] : gsap.utils.toArray<HTMLElement>('section:not([data-hero]) [data-speed]');
  parallax.forEach((el) => {
    const range = Number(el.dataset.speed) * 170;
    gsap.fromTo(
      el,
      { y: range },
      {
        y: -range,
        ease: 'none',
        scrollTrigger: {
          trigger: el.closest('section'),
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        },
      },
    );
  });

  // Filet de la frise : il se trace au scroll, à l'horizontale sur desktop, à la verticale sur mobile.
  gsap.utils.toArray<HTMLElement>('[data-draw]').forEach((el) => {
    gsap.from(el, {
      [innerWidth < 1100 ? 'scaleY' : 'scaleX']: 0, // même seuil que la frise (services.astro)
      ease: 'none',
      scrollTrigger: { trigger: el.parentElement, start: 'top 80%', end: 'bottom 55%', scrub: true },
    });
  });

  document.fonts.ready.then(() => ScrollTrigger.refresh());
}
