import Image from "next/image";

/**
 * The brand lockup: the circular GB monogram beside the stacked wordmark,
 * matching the horizontal lockup on the company's letterhead. The mark is the
 * artwork lifted from the print collateral, so it stays an image rather than
 * being redrawn.
 */
export function Logo({ className = "" }: { className?: string }) {
  return (
    <span className={`flex items-center gap-3 ${className}`}>
      <Image
        src="/logo-mark.svg"
        alt=""
        width={38}
        height={40}
        priority
        className="h-10 w-auto"
      />
      <span className="flex flex-col text-[13px] font-semibold uppercase leading-[1.15] tracking-[0.14em] text-oxblood">
        <span>Global</span>
        <span>Bridge</span>
      </span>
      <span className="sr-only">Global Bridge</span>
    </span>
  );
}
