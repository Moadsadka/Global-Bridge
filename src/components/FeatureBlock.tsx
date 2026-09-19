import { RevealText } from "./RevealText";
import { friction, testimonials } from "@/content/site";

/**
 * Dark band listing what the service removes. Inverts the page against the
 * light canvas either side of it, per the reference's rhythm.
 */
export function FeatureBlock() {
  return (
    <section id="how" className="px-6 py-20">
      <div
        className="mx-auto grid max-w-[1200px] gap-10 lg:grid-cols-[0.85fr_1.15fr] lg:gap-16"
        data-animate-group
      >
        <div>
          <RevealText
            text={friction.heading}
            className="max-w-[18ch] text-heading-sm font-semibold leading-[1.15] tracking-[-0.01em] text-espresso sm:text-heading"
          />

          {/* Anchors the column so the dark list does not sit beside empty canvas. */}
          <figure
            data-animate
            className="mt-12 rounded-[var(--radius-cards)] border border-linen bg-snow p-card"
          >
            <blockquote className="text-body leading-[1.55] text-ink">
              “{testimonials[0].quote}”
            </blockquote>
            <figcaption className="mt-5 text-[14px] text-stone">
              <span className="font-medium text-espresso">
                {testimonials[0].name}
              </span>
              <span className="text-taupe"> · </span>
              {testimonials[0].role}
            </figcaption>
          </figure>
        </div>

        <ul className="overflow-hidden rounded-[var(--radius-cards)] bg-espresso px-7 py-2">
          {friction.items.map((item) => (
            <li
              key={item.rest}
              data-animate="left"
              className="flex items-center gap-4 border-b border-white/10 py-5 last:border-b-0"
            >
              <span
                aria-hidden
                className="grid size-7 shrink-0 place-items-center rounded-full border border-cream/30 text-cream"
              >
                <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                  <path
                    d="M3 8h9M8.5 4.5 12 8l-3.5 3.5"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </span>
              <p className="text-subheading font-medium leading-[1.4] text-cream">
                <span className="text-taupe">{item.lead}</span> {item.rest}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
