"use client";

import { useEffect } from "react";
import Lenis from "lenis";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

/**
 * Smooth scroll and scroll-triggered reveals.
 *
 * Everything animated here moves only transform and opacity. Under
 * prefers-reduced-motion nothing initialises at all: Lenis stays off, native
 * scrolling is left alone, and content renders at its resting position.
 */
export function MotionProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (reduced.matches) return;

    gsap.registerPlugin(ScrollTrigger);

    // Marking the root tells CSS it is safe to hide elements that will animate.
    // Doing it here rather than in the markup means a failed hydration leaves
    // the page readable instead of blank.
    document.documentElement.classList.add("js-ready");

    const lenis = new Lenis({
      duration: 1.1,
      easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
      touchMultiplier: 1.6,
    });

    lenis.on("scroll", ScrollTrigger.update);

    const raf = (time: number) => lenis.raf(time * 1000);
    gsap.ticker.add(raf);
    gsap.ticker.lagSmoothing(0);

    // Same-page links jump instantly by default, which reads badly against
    // smooth scrolling everywhere else. Hand them to Lenis instead, offset so
    // the section heading clears the sticky bar.
    const onAnchorClick = (event: MouseEvent) => {
      const link = (event.target as HTMLElement)?.closest?.<HTMLAnchorElement>(
        'a[href^="#"]',
      );
      if (!link) return;

      const id = link.getAttribute("href");
      if (!id || id === "#") return;

      const target = document.querySelector(id);
      if (!target) return;

      event.preventDefault();
      lenis.scrollTo(target as HTMLElement, { offset: -88, duration: 1.2 });
      history.pushState(null, "", id);
    };

    document.addEventListener("click", onAnchorClick);

    // How each reveal variant starts. Every one of them is a transform and an
    // opacity, nothing that triggers layout.
    const from: Record<string, gsap.TweenVars> = {
      rise: { y: 26 },
      fade: {},
      scale: { y: 18, scale: 0.985 },
      left: { x: -22 },
    };
    const restingState = { y: 0, x: 0, scale: 1, opacity: 1 };

    const variantOf = (el: HTMLElement) =>
      from[el.dataset.animate || "rise"] ?? from.rise;

    const ctx = gsap.context(() => {
      // Set every element to its own starting pose before anything animates.
      gsap.utils.toArray<HTMLElement>("[data-animate]").forEach((el) => {
        gsap.set(el, variantOf(el));
      });

      // Grouped reveals: children of a [data-animate-group] stagger together,
      // anything else comes in on its own.
      gsap.utils.toArray<HTMLElement>("[data-animate-group]").forEach((group) => {
        const items = gsap.utils.toArray<HTMLElement>("[data-animate]", group);
        if (!items.length) return;

        gsap.to(items, {
          ...restingState,
          duration: 0.9,
          ease: "power3.out",
          stagger: 0.08,
          scrollTrigger: { trigger: group, start: "top 82%", once: true },
        });
      });

      gsap.utils
        .toArray<HTMLElement>("[data-animate]")
        .filter((el) => !el.closest("[data-animate-group]"))
        .forEach((el) => {
          gsap.to(el, {
            ...restingState,
            duration: 0.9,
            ease: "power3.out",
            scrollTrigger: { trigger: el, start: "top 86%", once: true },
          });
        });

      // Headings that assemble a word at a time.
      gsap.utils
        .toArray<HTMLElement>('[data-reveal="words"]')
        .forEach((heading) => {
          const words = gsap.utils.toArray<HTMLElement>("[data-word]", heading);
          if (!words.length) return;

          // fromTo so the tween owns both ends of yPercent. A set() plus a to()
          // leaves the start value in play if anything else touches y, and the
          // words settle a full line-height below where they belong.
          gsap.fromTo(
            words,
            { yPercent: 108, opacity: 0 },
            {
              yPercent: 0,
              opacity: 1,
              duration: 0.85,
              ease: "power3.out",
              stagger: 0.055,
              scrollTrigger: { trigger: heading, start: "top 88%", once: true },
            },
          );
        });
    });

    ScrollTrigger.refresh();

    return () => {
      document.removeEventListener("click", onAnchorClick);
      ctx.revert();
      gsap.ticker.remove(raf);
      lenis.destroy();
      document.documentElement.classList.remove("js-ready");
    };
  }, []);

  return <>{children}</>;
}
