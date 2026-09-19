/**
 * Headline whose words each sit in their own clipping box, so they can rise
 * into place one after another. This renders the markup only — MotionProvider
 * owns every animation on the page and drives these through
 * `[data-reveal="words"]`, which keeps one component responsible for motion
 * instead of each section starting a GSAP context of its own.
 *
 * With JavaScript off, or under reduced motion, this is an ordinary heading.
 */
export function RevealText({
  text,
  as: Tag = "h2",
  className = "",
}: {
  text: string;
  as?: "h1" | "h2" | "h3" | "p";
  className?: string;
}) {
  const words = text.split(" ");

  return (
    <Tag data-reveal="words" className={className}>
      {words.map((word, i) => (
        <span key={`${word}-${i}`}>
          {/* The box clips; the inner span moves. Padding keeps descenders. */}
          <span className="inline-block overflow-hidden pb-[0.12em] align-bottom">
            <span data-word className="inline-block will-change-transform">
              {word}
            </span>
          </span>
          {i < words.length - 1 ? " " : ""}
        </span>
      ))}
    </Tag>
  );
}
