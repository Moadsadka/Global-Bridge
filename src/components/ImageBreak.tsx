"use client";

import Image from "next/image";
import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { imageBreak } from "@/content/site";

/**
 * Full-bleed visual divider between content sections.
 *
 * Awaiting a photograph, the panel is a deep brand surface carrying the
 * monogram, which drifts slowly as the section passes — the one piece of
 * scroll-linked motion on the page. Swapping in a photograph means replacing
 * the mark; the parallax rig stays as it is.
 */
export function ImageBreak() {
  const sectionRef = useRef<HTMLElement>(null);
  const layerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const section = sectionRef.current;
    const layer = layerRef.current;
    if (!section || !layer) return;

    gsap.registerPlugin(ScrollTrigger);

    const ctx = gsap.context(() => {
      gsap.fromTo(
        layer,
        { yPercent: -6 },
        {
          yPercent: 6,
          ease: "none",
          scrollTrigger: {
            trigger: section,
            start: "top bottom",
            end: "bottom top",
            scrub: true,
          },
        },
      );
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="px-6 py-10">
      <div className="mx-auto max-w-[1200px]">
        <div className="relative h-[420px] overflow-hidden rounded-[var(--radius-break)] bg-espresso sm:h-[520px]">
          <div
            ref={layerRef}
            className="absolute inset-0 grid place-items-center will-change-transform"
          >
            <Image
              src="/logo-mark.svg"
              alt=""
              width={520}
              height={549}
              className="h-[80%] w-auto opacity-[0.08]"
            />
          </div>
          <p className="absolute bottom-8 left-8 text-caption uppercase tracking-[0.18em] text-cream/70">
            {imageBreak.caption}
          </p>
        </div>
      </div>
    </section>
  );
}
