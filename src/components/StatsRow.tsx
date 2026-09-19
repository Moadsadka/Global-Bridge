import { stats } from "@/content/site";

/** Three headline metrics on one baseline. */
export function StatsRow() {
  return (
    <section className="px-6 py-20">
      <div
        className="mx-auto grid max-w-[1200px] gap-10 sm:grid-cols-3"
        data-animate-group
      >
        {stats.map((stat) => (
          <div key={stat.label} data-animate className="flex items-baseline gap-4">
            <span className="text-heading font-semibold tracking-[-0.02em] text-espresso sm:text-heading-lg">
              {stat.value}
            </span>
            <span className="max-w-[18ch] text-[14px] leading-[1.4] text-stone">
              {stat.label}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
