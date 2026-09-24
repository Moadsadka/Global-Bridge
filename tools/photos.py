#!/usr/bin/env python3
"""Swap the template's stock photography for Global Bridge's own.

Every photo slot in the template is listed below with the shape it needs and
what belongs in it. Drop a file at the slot's path under assets/photos/ and
this stage points every reference at it: the exported HTML, the page modules
React hydrates from, and the responsive srcset variants.

Slots with no file yet are left on the template's image and reported, so this
can be run repeatedly as photography arrives rather than all at once.

Run it as part of tools/build.sh, after the copy rewrite.
"""
import pathlib
import re
import sys

# template image -> (slot file, shape, what the slot is)
SLOTS = {
    # Home: the section that lists what slows a principal down
    "image-94878099.png": ("friction-lead.jpg", "1200x1200",
                           "the lead image beside the friction list"),
    "image-be010e13.png": ("friction-terminal.jpg", "1200x1200",
                           "a commercial terminal queue"),
    "image-46f06097.png": ("friction-suppliers.jpg", "1200x1200",
                           "a desk of scattered paperwork or screens"),
    "image-f1a7fcad.png": ("friction-driver.jpg", "1200x1200",
                           "a car waiting kerbside in an unfamiliar city"),
    "image-7caa8ea2.png": ("friction-hotel.jpg", "1200x1200",
                           "a hotel reception or suite door"),
    "image-6daf8a03.png": ("friction-privacy.jpg", "1200x1200",
                           "a document or screen, shot discreetly"),
    "image-3921faed.jpg": ("friction-transfer.jpg", "1856x2304",
                           "a car moving, or an aircraft waiting, at dusk"),

    # Home and services: the service section
    "image-093f385d.png": ("services-lead.jpg", "1200x800",
                           "a private jet on stand, wide"),
    "image-3f433653.png": ("service-aviation.jpg", "840x1200",
                           "private aviation: cabin interior or boarding steps"),
    "image-a7da01df.png": ("service-transfers.jpg", "1200x673",
                           "a chauffeured saloon, exterior or interior"),
    "image-f2eb1935.png": ("service-airport.jpg", "992x1200",
                           "a private terminal or fast-track channel"),
    "image-c3c10fde.jpg": ("service-concierge.jpg", "1856x2304",
                           "a hotel suite, meeting room or executive lounge"),

    # About
    "image-c55d70ab.png": ("about-hero.png", "3712x4608",
                           "the about hero; the template's is a cut-out on "
                           "transparency, so this one needs an alpha channel"),
    "image-bdbd9dfb.jpg": ("about-portrait.jpg", "2048x2048",
                           "the about page's square portrait"),
    "image-50f2d61c.jpg": ("about-working.jpg", "1856x2304",
                           "a coordinator at work, or a city at night"),

    # 404
    "image-e310e3f9.jpg": ("not-found.jpg", "3712x4608",
                           "the 404 page's full-bleed image"),
}

# Deliberately not listed: the six 1200x1200 images under the testimonials.
# They sit beside named roles ("Managing Director", "Chief of Staff"), so a
# stock face there reads as a real client who does not exist. Those slots want
# real people, with permission, or nothing at all.

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "assets" / "photos"


def main() -> None:
    files = [p for p in ROOT.rglob("*")
             if p.suffix in {".html", ".mjs", ".js"}
             and ".git" not in p.parts and p.parent.name != "tools"]

    filled, missing, touched = [], [], 0
    for old, (name, shape, what) in SLOTS.items():
        if not (PHOTOS / name).exists():
            missing.append((name, shape, what))
            continue
        filled.append(name)
        new = f"/assets/photos/{name}"
        for path in files:
            text = path.read_text(encoding="utf-8")
            # every reference, with or without Framer's sizing query string
            swapped = re.sub(
                r"(?:/assets/images/)?" + re.escape(old) + r"[^\"'`\s,]*",
                new, text)
            if swapped != text:
                path.write_text(swapped, encoding="utf-8")
                touched += 1

    print(f"placed {len(filled)} photos across {touched} files")
    if missing:
        print(f"{len(missing)} slots still on the template's image:")
        for name, shape, what in missing:
            print(f"  assets/photos/{name:24} {shape:>10}  {what}")


if __name__ == "__main__":
    main()
