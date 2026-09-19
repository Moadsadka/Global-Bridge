"use client";

import { useEffect, useState } from "react";
import { Logo } from "./Logo";
import { nav, company } from "@/content/site";

/**
 * Sticky top bar. It floats borderless over the canvas and only grows a
 * hairline rule and a frosted backing once the page has scrolled, so the hero
 * reads as one uninterrupted surface at rest.
 */
export function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-50 transition-colors duration-300 ${
        scrolled
          ? "border-b border-linen bg-paper/85 backdrop-blur-md"
          : "border-b border-transparent bg-transparent"
      }`}
    >
      <div className="mx-auto flex h-[72px] max-w-[1200px] items-center justify-between px-6">
        <a href="#top" aria-label="Global Bridge — home">
          <Logo />
        </a>

        <nav className="hidden items-center gap-8 md:flex" aria-label="Main">
          {nav.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="text-[14px] text-ink transition-colors duration-200 hover:text-copper"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-5">
          <a
            href={`mailto:${company.email}`}
            className="hidden text-[14px] text-stone transition-colors duration-200 hover:text-copper sm:inline"
          >
            {company.email}
          </a>
          <a
            href="#contact"
            className="rounded-[var(--radius-pills)] bg-espresso px-5 py-3 text-[14px] text-cream shadow-(--shadow-action) transition-transform duration-200 will-change-transform hover:-translate-y-px"
          >
            Request arrangements
          </a>
        </div>
      </div>
    </header>
  );
}
