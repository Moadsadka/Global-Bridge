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

    const ctx = gsap.context(() => {
      // Grouped reveals: children of a [data-animate-group] stagger together,
      // anything else rises on its own.
      gsap.utils.toArray<HTMLElement>("[data-animate-group]").forEach((group) => {
        const items = gsap.utils.toArray<HTMLElement>(
          "[data-animate]",
          group,
        );
        if (!items.length) return;

        gsap.to(items, {
          opacity: 1,
          y: 0,
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
            opacity: 1,
            y: 0,
            duration: 0.9,
            ease: "power3.out",
            scrollTrigger: { trigger: el, start: "top 86%", once: true },
          });
        });
    });

    // Elements start offset; the tweens above bring them home.
    gsap.set("[data-animate]", { y: 24 });
    ScrollTrigger.refresh();

    return () => {
      ctx.revert();
      gsap.ticker.remove(raf);
      lenis.destroy();
      document.documentElement.classList.remove("js-ready");
    };
  }, []);

  return <>{children}</>;
}
