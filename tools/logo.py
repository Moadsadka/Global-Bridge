#!/usr/bin/env python3
"""Put the Global Bridge marks in place of the template's.

Three swaps:

  nav mark        The template flips its mark white over the hero with a CSS
                  invert filter driven by a scroll variant, so the asset there
                  has to be monochrome or the inverted state comes out cyan.
                  It gets the ink monogram and the filter is left alone.
  standing mark   Everywhere the filter is a constant invert(0), the mark is
                  never flipped, so it gets the full-colour oxblood monogram.
  signature       The template signs its about section with a handwritten
                  "Maya". That is another brand's name, so it is replaced with
                  the Global Bridge lockup.

The page modules carry the same references as the HTML and React re-renders
from them, so both have to be rewritten.
"""
import pathlib
import re

MARK = "image-354aa990.png"
SIGNATURE = "image-a753d099.png"

INK = "/assets/brand/gb-mark-ink.svg"      # nav: inverted to white over the hero
OXBLOOD = "/assets/brand/gb-mark.svg"      # everywhere else
LOCKUP = "/assets/brand/gb-lockup.svg"

# the template's own invert filter, written out in the exported HTML
HTML_INVERT = "filter:invert(1);-webkit-filter:invert(1)"
# ...and as the variant-driven expression in the page modules
JS_INVERT = "parseFloat(m)/100"


def swap(region: str, asset: str, old: str = MARK) -> str:
    """Point src and srcSet at an asset, and stop the square crop.

    The template's mark is square and set to cover. The monogram is not, so
    cover would shave its ring.
    """
    region = re.sub(r"/assets/images/" + re.escape(old) + r"[^\"'`\s]*", asset, region)
    region = re.sub(re.escape(old) + r"[^\"'`\s]*", asset.lstrip("/"), region)
    return region.replace("object-fit:cover", "object-fit:contain")


def rewrite_html(html: str) -> str:
    # Header placements: the ones the template wraps in its invert filter.
    out, cursor = [], 0
    for m in re.finditer(re.escape(HTML_INVERT), html):
        end = min(len(html), m.end() + 1600)
        region = html[m.end():end]
        if MARK not in region:
            continue
        out.append(html[cursor:m.start()])
        out.append(HTML_INVERT)
        out.append(swap(region, INK))
        cursor = end
    out.append(html[cursor:])
    return swap("".join(out), OXBLOOD)


def rewrite_js(src: str) -> str:
    """Same split, but the nav is identified by the invert expression near it."""
    out, cursor = [], 0
    for m in re.finditer(re.escape(MARK), src):
        if JS_INVERT not in src[max(0, m.start() - 900):m.start()]:
            continue
        out.append(src[cursor:m.start()])
        out.append(INK.lstrip("/"))
        cursor = m.end()
    out.append(src[cursor:])
    src = "".join(out)
    # the nav swap above leaves the path prefix, so tidy both forms
    src = src.replace("/assets/images/" + INK.lstrip("/"), INK)
    src = src.replace('"/assets/images/" + ' + INK, '"' + INK + '"')
    return swap(src, OXBLOOD)


def contain(src: str) -> str:
    """Framer's `fill` fit crops to the box; the marks must fit inside it.

    Each brand asset sits in a background object that opens with its fit, so
    the nearest one before the asset is the one to change.
    """
    out, cursor = [], 0
    for m in re.finditer(r"/assets/brand/[a-z-]+\.svg", src):
        head = src.rfind("fit:`fill`", cursor, m.start())
        if head == -1:
            continue
        out.append(src[cursor:head])
        out.append("fit:`fit`")
        cursor = head + len("fit:`fill`")
    out.append(src[cursor:])
    return "".join(out)


def main() -> None:
    root = pathlib.Path(__file__).resolve().parent.parent
    total = 0
    for path in sorted(root.rglob("*")):
        if path.suffix not in {".html", ".mjs", ".js"} or ".git" in path.parts:
            continue
        if path.parent.name == "tools":
            continue
        text = before = path.read_text(encoding="utf-8")
        if MARK in text:
            text = rewrite_html(text) if path.suffix == ".html" else rewrite_js(text)
        if SIGNATURE in text:
            text = swap(text, LOCKUP, SIGNATURE)
        if path.suffix != ".html":
            text = contain(text)
        if text != before:
            path.write_text(text, encoding="utf-8")
            total += 1
            print(f"  {path.relative_to(root)}")
    print("updated", total, "files")


if __name__ == "__main__":
    main()
