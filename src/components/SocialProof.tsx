import { socialProof, testimonials } from "@/content/site";

/**
 * Client logos and testimonials.
 *
 * The logo strip is rendered as empty slots on purpose: fabricating marks for
 * a real company would imply endorsements it has not given. They are sized and
 * spaced for real logos to drop straight in.
 */
export function SocialProof() {
  return (
    <section className="px-6 py-20">
      <div className="mx-auto max-w-[1200px]" data-animate-group>
        <h2
          data-animate
          className="max-w-[22ch] text-heading-sm font-semibold leading-[1.15] tracking-[-0.01em] text-espresso sm:text-heading"
        >
          {socialProof.heading}
        </h2>

        <div
          data-animate
          className="mt-12 flex flex-wrap items-center justify-between gap-8"
        >
          {Array.from({ length: socialProof.logoSlots }).map((_, i) => (
            <div
              key={i}
              aria-hidden
              className="h-9 w-[120px] rounded-[var(--radius-badges)] bg-sand/45"
            />
          ))}
        </div>

        <div className="mt-16 grid gap-4 md:grid-cols-2">
          {/* The first quote already carries the dark feature block. */}
          {testimonials.slice(1).map((t) => (
            <figure
              key={t.quote}
              data-animate
              className="rounded-[var(--radius-cards)] border border-linen bg-snow p-card"
            >
              <blockquote className="text-body-lg leading-[1.5] text-ink">
                “{t.quote}”
              </blockquote>
              <figcaption className="mt-6 text-[14px] text-stone">
                <span className="font-medium text-espresso">{t.name}</span>
                <span className="text-taupe"> · </span>
                {t.role}
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
