import { RevealText } from "./RevealText";
import { finalCta, company } from "@/content/site";

/** Closing call to action on a dark surface. */
export function FinalCta() {
  return (
    <section id="contact" className="px-6 py-20">
      <div
        className="mx-auto max-w-[1200px] rounded-[var(--radius-cards)] bg-espresso px-8 py-20 text-center sm:px-16"
        data-animate-group
      >
        <RevealText
          text={finalCta.heading}
          className="mx-auto max-w-[18ch] text-heading-sm font-semibold leading-[1.15] tracking-[-0.01em] text-cream sm:text-heading-lg"
        />
        <p
          data-animate
          className="mx-auto mt-6 max-w-[52ch] text-body-lg text-taupe"
        >
          {finalCta.body}
        </p>
        <div
          data-animate
          className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row"
        >
          <a
            href={`mailto:${company.email}`}
            className="rounded-[var(--radius-pills)] bg-cream px-6 py-3.5 text-[14px] font-medium text-espresso transition-transform duration-200 will-change-transform hover:-translate-y-px"
          >
            {finalCta.cta}
          </a>
          <a
            href={`tel:${company.offices[0].tel.replace(/\s/g, "")}`}
            className="rounded-[var(--radius-pills)] border border-cream/35 px-6 py-3.5 text-[14px] text-cream transition-colors duration-200 hover:border-cream/70"
          >
            {company.offices[0].tel}
          </a>
        </div>
      </div>
    </section>
  );
}
