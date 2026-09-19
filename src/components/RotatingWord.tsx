"use client";

import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";

/**
 * A single word in the headline that cycles through alternatives.
 *
 * The live word sits in normal flow so the box is sized by its content — that
 * way the word is visible before any JavaScript runs, and stays visible under
 * reduced motion where this component never animates at all. Each change
 * overlays the incoming word absolutely, rises one out as the other rises in,
 * and eases the box width so the rest of the headline settles instead of
 * jumping.
 */
export function RotatingWord({
  words,
  interval = 2400,
  className = "",
}: {
  words: string[];
  interval?: number;
  className?: string;
}) {
  const boxRef = useRef<HTMLSpanElement>(null);
  const wordRef = useRef<HTMLSpanElement>(null);
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (words.length < 2) return;

    const box = boxRef.current;
    const word = wordRef.current;
    if (!box || !word) return;

    let i = 0;
    let timeline: gsap.core.Timeline | null = null;

    // Measure a word by rendering it off-screen in the same typography.
    const widthOf = (text: string) => {
      const probe = word.cloneNode(false) as HTMLElement;
      probe.textContent = text;
      probe.style.position = "absolute";
      probe.style.visibility = "hidden";
      probe.style.whiteSpace = "nowrap";
      box.appendChild(probe);
      const w = probe.getBoundingClientRect().width;
      probe.remove();
      return w;
    };

    const tick = () => {
      const next = (i + 1) % words.length;

      const incoming = document.createElement("span");
      incoming.textContent = words[next];
      incoming.className = word.className;
      incoming.style.position = "absolute";
      incoming.style.left = "0";
      incoming.style.top = "0";
      incoming.style.whiteSpace = "nowrap";
      box.appendChild(incoming);

      timeline = gsap.timeline({
        onComplete: () => {
          // Hand the incoming word's text back to the in-flow span, then drop
          // the overlay. React's own render agrees with this via setIndex, so
          // the two never disagree about what is on screen.
          word.textContent = words[next];
          gsap.set(word, { yPercent: 0, opacity: 1 });
          gsap.set(box, { clearProps: "width" });
          incoming.remove();
          i = next;
          setIndex(next);
        },
      });

      // The two words overlap just enough to hand over. Too much overlap reads
      // as two words fighting for the line; too little leaves the headline with
      // a visible hole where the word should be.
      timeline
        .to(box, { width: widthOf(words[next]), duration: 0.5, ease: "power3.inOut" }, 0)
        .to(word, { yPercent: -105, opacity: 0, duration: 0.34, ease: "power2.in" }, 0)
        .fromTo(
          incoming,
          { yPercent: 105, opacity: 0 },
          { yPercent: 0, opacity: 1, duration: 0.5, ease: "power3.out" },
          0.17,
        );
    };

    const id = window.setInterval(tick, interval);
    return () => {
      window.clearInterval(id);
      timeline?.kill();
      gsap.killTweensOf([box, word]);
    };
  }, [words, interval]);

  // The box is taller than the line box so descenders are not clipped by the
  // mask; the negative margin keeps the baseline where the headline wants it.
  return (
    <span
      ref={boxRef}
      className="relative inline-flex overflow-hidden align-bottom -mb-[0.14em]"
      style={{ height: "1.2em" }}
    >
      <span
        ref={wordRef}
        className={`inline-block whitespace-nowrap ${className}`}
      >
        {words[0]}
      </span>
      {/* Announce the live word without the animation spamming assistive tech. */}
      <span className="sr-only" aria-live="polite">
        {words[index]}
      </span>
    </span>
  );
}
