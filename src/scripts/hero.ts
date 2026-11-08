import gsap from 'gsap';

const DESKTOP = '(min-width: 900px) and (prefers-reduced-motion: no-preference)';
const MOBILE = '(max-width: 899px) and (prefers-reduced-motion: no-preference)';

export function initHero() {
  const hero = document.querySelector<HTMLElement>('[data-hero]');
  if (!hero) return;

  const q = gsap.utils.selector(hero);
  const mm = gsap.matchMedia();

  mm.add(DESKTOP, () => {
    const root = document.documentElement;
    root.classList.add('motion-hero');

    const stage = hero.querySelector<HTMLElement>('[data-hero-stage]')!;
    const word = hero.querySelector<HTMLElement>('[data-hero-word]')!;
    const cubes = q('[data-cube]') as HTMLElement[];
    const mouseOf = (c: HTMLElement) => c.querySelector<HTMLElement>('[data-mouse]')!;

    // À chaque chargement, les lettres se répartissent au hasard entre les emplacements
    // définis dans Hero.astro : ceux-ci, et non les lettres, garantissent un titre dégagé.
    const slots = gsap.utils.shuffle(
      cubes.map((c) => ({ sx: +c.dataset.sx!, sy: +c.dataset.sy!, s: c.dataset.s!, m: mouseOf(c).dataset.mouse! })),
    );
    cubes.forEach((c, i) => {
      const slot = slots[i];
      c.dataset.sx = String(slot.sx + gsap.utils.random(-1.5, 1.5));
      c.dataset.sy = String(slot.sy + gsap.utils.random(-1.5, 1.5));
      c.dataset.s = slot.s;
      c.dataset.r = String(gsap.utils.random([-1, 1]) * gsap.utils.random(10, 26));
      mouseOf(c).dataset.mouse = slot.m;
    });

    // Décalage entre la place finale d'un cube et le centre de l'écran.
    const toX = (c: HTMLElement) =>
      (innerWidth * Number(c.dataset.sx)) / 100 - (c.offsetLeft + c.offsetWidth / 2 - word.offsetWidth / 2);
    const toY = (c: HTMLElement) =>
      (innerHeight * Number(c.dataset.sy)) / 100 - (c.offsetTop + c.offsetHeight / 2 - word.offsetHeight / 2);

    let progress = 0;

    const tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: stage,
        pin: true,
        start: 'top top',
        end: '+=150%',
        scrub: 1,
        invalidateOnRefresh: true,
        onUpdate(self) {
          progress = self.progress;
          hero.style.setProperty('--float', (1 - progress).toFixed(2));
        },
      },
    });

    tl.to('[data-hero-copy]', { autoAlpha: 0, y: -70, duration: 0.26, ease: 'power1.in' }, 0.04);

    cubes.forEach((cube, i) => {
      tl.fromTo(
        cube,
        {
          x: () => toX(cube),
          y: () => toY(cube),
          rotation: Number(cube.dataset.r),
          scale: Number(cube.dataset.s),
        },
        { x: 0, y: 0, rotation: 0, scale: 1, duration: 0.6, ease: 'power2.inOut' },
        i * 0.011,
      );
    });

    tl.fromTo(
      '[data-hero-star]',
      { y: () => -innerHeight * 0.65, rotation: -70, scale: 0.4, autoAlpha: 0 },
      { y: 0, rotation: 0, scale: 1, autoAlpha: 1, duration: 0.22, ease: 'back.out(1.5)' },
      0.7,
    );
    tl.fromTo('[data-hero-after]', { autoAlpha: 0, y: 26 }, { autoAlpha: 1, y: 0, duration: 0.12 }, 0.86);

    (q('[data-speed]') as HTMLElement[]).forEach((el) => {
      tl.to(el, { y: -Number(el.dataset.speed) * innerHeight * 0.6, duration: 1 }, 0);
    });

    tl.to({}, { duration: 0.08 });

    gsap.set(cubes, { willChange: 'transform' });
    word.classList.add('is-ready');

    gsap.from('[data-hero-intro]', {
      y: 28,
      autoAlpha: 0,
      duration: 1.2,
      stagger: 0.12,
      ease: 'power3.out',
    });
    gsap.from(word, { autoAlpha: 0, duration: 1.4, ease: 'power2.out' });

    // Suivi de souris : atténué à mesure que le mot se forme.
    if (!matchMedia('(hover: hover)').matches) {
      return () => root.classList.remove('motion-hero');
    }
    const movers = (q('[data-mouse]') as HTMLElement[]).map((el) => ({
      depth: Number(el.dataset.mouse),
      x: gsap.quickTo(el, 'x', { duration: 1.4, ease: 'power3.out' }),
      y: gsap.quickTo(el, 'y', { duration: 1.4, ease: 'power3.out' }),
    }));
    const onMove = (e: PointerEvent) => {
      const nx = e.clientX / innerWidth - 0.5;
      const ny = e.clientY / innerHeight - 0.5;
      const k = 1 - progress;
      movers.forEach((m) => {
        m.x(nx * m.depth * 46 * k);
        m.y(ny * m.depth * 30 * k);
      });
    };
    hero.addEventListener('pointermove', onMove);

    return () => {
      hero.removeEventListener('pointermove', onMove);
      root.classList.remove('motion-hero');
    };
  });

  mm.add(MOBILE, () => {
    gsap.from(q('[data-cube]'), {
      y: 26,
      autoAlpha: 0,
      duration: 1,
      stagger: 0.09,
      ease: 'power3.out',
    });
    gsap.from('[data-hero-star]', {
      y: -34,
      autoAlpha: 0,
      rotation: -30,
      duration: 1.1,
      delay: 1.3,
      ease: 'back.out(1.5)',
    });
  });
}
