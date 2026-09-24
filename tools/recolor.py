"""Remap the template's palette onto the Global Bridge brand tokens.

Handles every form the Framer export writes a colour in: 6-digit hex, 8-digit
hex with an alpha suffix, rgb() and rgba() with arbitrary spacing.
"""
import re, pathlib, sys

# template colour -> Global Bridge equivalent (see DESIGN.md)
MAP = {
    "2a2b2f": "432818",  # charcoal      -> espresso   (dark surfaces, headings)
    "f5ede1": "f4ebd7",  # warm sand     -> cream      (recessed surfaces)
    "fef9ef": "f9f8f7",  # off-white     -> paper      (canvas, light text on dark)
    "0099ff": "99582a",  # Framer's default link blue -> copper
    # 99582a (the template's accent) is already the brand's copper: left alone.
}

def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def convert(text):
    n = 0
    for src, dst in MAP.items():
        r, g, b = hex_to_rgb(src)
        nr, ng, nb = hex_to_rgb(dst)

        # #rrggbb and #rrggbbaa — keep any alpha suffix intact
        pat = re.compile(r"#" + src + r"([0-9a-fA-F]{2})?\b", re.I)
        text, k = pat.subn(lambda m: "#" + dst + (m.group(1) or ""), text)
        n += k

        # rgb(r, g, b) / rgba(r, g, b, a) with any spacing
        pat = re.compile(
            r"rgba?\(\s*%d\s*,\s*%d\s*,\s*%d\s*(,\s*([0-9.]+)\s*)?\)" % (r, g, b))
        def rep(m):
            if m.group(2) is not None:
                return "rgba(%d, %d, %d, %s)" % (nr, ng, nb, m.group(2))
            return "rgb(%d, %d, %d)" % (nr, ng, nb)
        text, k = pat.subn(rep, text)
        n += k
    return text, n

total_files = total_subs = 0
for pattern in ("*.html", "*.css", "*.mjs", "*.js"):
    for path in pathlib.Path(".").rglob(pattern):
        if ".git" in path.parts:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated, n = convert(original)
        if n:
            path.write_text(updated, encoding="utf-8")
            total_files += 1
            total_subs += n
print(f"recoloured {total_subs} values across {total_files} files")
