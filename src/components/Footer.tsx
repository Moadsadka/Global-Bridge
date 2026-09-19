import { Logo } from "./Logo";
import { company, nav } from "@/content/site";

export function Footer() {
  return (
    <footer id="coverage" className="border-t border-linen px-6 py-16">
      <div className="mx-auto max-w-[1200px]">
        <div className="grid gap-12 lg:grid-cols-[1fr_1.4fr]">
          <div>
            <Logo />
            <p className="mt-5 max-w-[30ch] text-[14px] leading-[1.5] text-stone">
              {company.tagline}
            </p>
          </div>

          <div className="grid gap-10 sm:grid-cols-3">
            {company.offices.map((office) => (
              <address key={office.city} className="not-italic">
                <p className="text-caption uppercase tracking-[0.16em] text-copper">
                  {office.city}
                </p>
                <div className="mt-3 space-y-0.5 text-[14px] leading-[1.5] text-stone">
                  {office.lines.map((line) => (
                    <p key={line}>{line}</p>
                  ))}
                  <p className="pt-2">
                    <a
                      href={`tel:${office.tel.replace(/\s/g, "")}`}
                      className="transition-colors duration-200 hover:text-copper"
                    >
                      {office.tel}
                    </a>
                  </p>
                </div>
              </address>
            ))}

            <nav aria-label="Footer">
              <p className="text-caption uppercase tracking-[0.16em] text-copper">
                Site
              </p>
              <ul className="mt-3 space-y-1.5 text-[14px] text-stone">
                {nav.map((item) => (
                  <li key={item.href}>
                    <a
                      href={item.href}
                      className="transition-colors duration-200 hover:text-copper"
                    >
                      {item.label}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </div>

        <div className="mt-14 flex flex-col gap-3 border-t border-linen pt-8 text-caption text-taupe sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {new Date().getFullYear()} {company.name}. All rights reserved.
          </p>
          <a
            href={`mailto:${company.email}`}
            className="text-stone transition-colors duration-200 hover:text-copper"
          >
            {company.email}
          </a>
        </div>
      </div>
    </footer>
  );
}
