import Image from "next/image";

/**
 * The brand lockup, taken straight from the print collateral's logo sheet —
 * monogram between the two words, set in the brand's own wordmark type rather
 * than approximated in the site face. The cream variant is the same artwork
 * recoloured for dark surfaces.
 */
export function Logo({
  variant = "oxblood",
  className = "",
}: {
  variant?: "oxblood" | "cream";
  className?: string;
}) {
  return (
    <Image
      src={variant === "cream" ? "/logo-lockup-cream.svg" : "/logo-lockup.svg"}
      alt="Global Bridge"
      width={190}
      height={55}
      priority
      className={`h-[42px] w-auto ${className}`}
    />
  );
}
