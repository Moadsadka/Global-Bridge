import Image from "next/image";
import { services } from "@/content/site";

/**
 * Horizontal band of service categories.
 *
 * Each card reserves its top half for photography. Until the client supplies
 * images, that area is a brand-toned panel carrying the monogram as a
 * watermark — the same treatment the letterhead uses — so the band reads as
 * finished rather than as a row of empty boxes. Dropping a photograph in means
 * replacing the panel, nothing else.
 */

const tones = {
  espresso: { panel: "bg-espresso", mark: "opacity-[0.07]", text: "text-cream" },
  copper: { panel: "bg-copper", mark: "opacity-[0.09]", text: "text-cream" },
  cream: { panel: "bg-cream", mark: "opacity-[0.13]", text: "text-espresso" },
  gold: { panel: "bg-gold", mark: "opacity-[0.11]", text: "text-espresso" },
} as const;

type Tone = keyof typeof tones;

export function ServiceCards() {
  return (
    <section id="services" className="py-20">
      <div className="mx-auto mb-12 max-w-[1200px] px-6" data-animate-group>
        <h2
          data-animate
          className="max-w-[20ch] text-heading-sm font-semibold leading-[1.15] tracking-[-0.01em] text-espresso sm:text-heading"
        >
          Four services, arranged as one itinerary
        </h2>
      </div>

      {/*
        The band bleeds past the page container so cards run to the edge of the
        viewport, and scrolls horizontally with snap points on every screen.
      */}
      <div
        data-animate-group
        className="flex snap-x snap-mandatory gap-4 overflow-x-auto pb-4 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
        style={{
          // scroll-padding has to match, or snapping aligns the first card to
          // the scrollport edge and scrolls the leading gutter away.
          paddingInline: "max(24px, calc((100vw - 1200px) / 2))",
          scrollPaddingInline: "max(24px, calc((100vw - 1200px) / 2))",
        }}
      >
        {services.map((service) => {
          const tone = tones[service.tone as Tone] ?? tones.espresso;

          return (
            <article
              key={service.title}
              data-animate
              className="group w-[300px] shrink-0 snap-start overflow-hidden rounded-[var(--radius-cards)] border border-linen bg-snow transition-transform duration-500 ease-out will-change-transform hover:-translate-y-1.5 sm:w-[340px]"
            >
              <div
                className={`relative flex h-[220px] items-center justify-center overflow-hidden ${tone.panel}`}
              >
                <Image
                  src="/logo-mark.svg"
                  alt=""
                  width={220}
                  height={232}
                  className={`absolute -right-10 -top-6 h-[150%] w-auto transition-transform duration-700 ease-out will-change-transform group-hover:scale-[1.04] ${tone.mark}`}
                />
                <h3
                  className={`absolute bottom-6 left-7 right-7 text-subheading font-semibold ${tone.text}`}
                >
                  {service.title}
                </h3>
              </div>

              <div className="p-card">
                <p className="text-body text-stone">{service.body}</p>
                <ul className="mt-5 flex flex-wrap gap-2">
                  {service.tags.map((tag) => (
                    <li
                      key={tag}
                      className="rounded-[var(--radius-badges)] border border-linen px-2 py-1 text-caption text-ink"
                    >
                      {tag}
                    </li>
                  ))}
                </ul>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
