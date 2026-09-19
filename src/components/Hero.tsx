import { RotatingWord } from "./RotatingWord";
import { hero, heroStats } from "@/content/site";

/**
 * Split hero: the display headline carries the left column, a compact
 * supporting paragraph and enquiry form sit right, and the stats sit on the
 * baseline beneath both.
 */
export function Hero() {
  return (
    <section id="top" className="px-6 pb-20 pt-16 md:pt-24">
      <div className="mx-auto max-w-[1200px]" data-animate-group>
        <div className="grid gap-12 lg:grid-cols-[1.15fr_0.85fr] lg:gap-16">
          <div>
            <p
              data-animate
              className="mb-8 inline-flex items-center gap-2 rounded-[var(--radius-badges)] border border-linen bg-snow px-3 py-1.5 text-caption tracking-[0.12em] text-copper uppercase"
            >
              {hero.eyebrow}
            </p>

            <h1
              data-animate
              className="text-[40px] font-semibold leading-[1.12] tracking-[-0.015em] text-espresso sm:text-[56px] lg:text-display"
            >
              {hero.headlineBefore}{" "}
              <RotatingWord
                words={hero.rotating}
                className="font-semibold text-taupe"
              />{" "}
              {hero.headlineAfter}
            </h1>
          </div>

          <div className="flex flex-col justify-end">
            <p data-animate className="max-w-[46ch] text-body-lg text-stone">
              {hero.supporting}
            </p>

            <form
              data-animate
              className="mt-8 flex flex-col gap-2 rounded-[var(--radius-cards)] border border-linen bg-snow p-2 shadow-(--shadow-pill) sm:flex-row sm:items-center sm:rounded-[var(--radius-pills)]"
            >
              <label htmlFor="hero-email" className="sr-only">
                Email address
              </label>
              <input
                id="hero-email"
                type="email"
                required
                placeholder={hero.placeholder}
                className="min-w-0 flex-1 bg-transparent px-4 py-2.5 text-body text-ink outline-none placeholder:text-taupe"
              />
              <button
                type="submit"
                className="shrink-0 rounded-[var(--radius-pills)] bg-espresso px-5 py-3 text-[14px] text-cream shadow-(--shadow-action) transition-transform duration-200 will-change-transform hover:-translate-y-px max-sm:w-full"
              >
                {hero.cta}
              </button>
            </form>
          </div>
        </div>

        <div className="mt-20 flex flex-wrap items-baseline gap-x-16 gap-y-8">
          {heroStats.map((stat) => (
            <div key={stat.label} data-animate className="flex items-baseline gap-3">
              <span className="text-heading font-semibold text-espresso">
                {stat.value}
              </span>
              <span className="max-w-[16ch] text-[14px] leading-[1.35] text-stone">
                {stat.label}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
