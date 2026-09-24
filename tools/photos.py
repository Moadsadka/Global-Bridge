#!/usr/bin/env python3
"""Swap the template's stock photography for Global Bridge's own.

Every photo slot in the template is listed below with the shape it needs and
what belongs in it. A slot is filled from one of two places, in this order:

  1. a file at assets/photos/<slot>, which always wins; or
  2. the Unsplash photograph named in STOCK, served from Unsplash's own CDN
     at the slot's shape.

The stock photographs are a stand-in until Global Bridge's own photography
arrives. They are hotlinked rather than copied into the repository, which is
what Unsplash's API terms ask for; assets/photos/CREDITS.md names each
photographer. Drop a real file in beside it and the stand-in goes away with no
other change.

Whichever it is, this stage points every reference at it: the exported HTML,
the page modules React hydrates from, and the responsive srcset variants.

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

# slot file -> Unsplash photograph, as (photo path, id, photographer, handle).
# The same reasoning as the testimonials keeps faces out of these: the two
# about-page slots take the Valencia office's city and a skyline rather than a
# stranger standing in for Al Waleed Jalloud. about-hero.png is not here at
# all, because the template's is a cut-out on transparency and no photograph
# can supply the alpha channel.
STOCK = {
    "friction-lead.jpg": ("photo-1774471114722-264b64993219", "hNQ0RH_a5Jo",
                          "jack berry", "jackseeberry"),
    "friction-terminal.jpg": ("photo-1765971394562-403ebd8d1b7c", "Tdaf0LvYfeY",
                              "Rudityas W Anggoro", "rudityas"),
    "friction-suppliers.jpg": ("photo-1712231169791-3f4de102505c", "P8vvpipXLu4",
                               "Bill Zannoni", "billznn"),
    "friction-driver.jpg": ("photo-1605606290699-da4b6b4614d0", "pA4lVRcShrQ",
                            "Adam Borkowski", "borkography"),
    "friction-hotel.jpg": ("photo-1660557989695-14fac79c086d", "8BYahZcwYgI",
                           "Dylan Calluy", "dylancalluy"),
    "friction-privacy.jpg": ("photo-1655722725332-9925c96dd627", "LPdaW746WAw",
                             "Global Residence Index", "globalresidenceindex"),
    "friction-transfer.jpg": ("photo-1759432311506-03c9f66e8065", "mU08S5tpEb4",
                              "Hodder", "hodderphotos"),

    "services-lead.jpg": ("photo-1772354815085-0cb07ca438fe", "dzTNbKfW8Fc",
                          "Nitish Suri", "nitishsuri13"),
    "service-aviation.jpg": ("photo-1570125910130-67cb59733d1d", "EwoyDPlT_H0",
                             "Jonathan Borba", "jonathanborba"),
    "service-transfers.jpg": ("photo-1485291571150-772bcfc10da5", "FMbWFDiVRPs",
                              "Samuele Errico Piccarini", "samuele_piccarini"),
    "service-airport.jpg": ("photo-1775644605455-49b8a8f27eaa", "cSL1cZQuEWE",
                            "Maria Beres", "mberes"),
    "service-concierge.jpg": ("photo-1629140727571-9b5c6f6267b4", "p3UWyaujtQo",
                              "Linus Mimietz", "linusmimietz"),

    "about-portrait.jpg": ("photo-1637516465638-cc596d698506", "O8mS-Y7Uy7E",
                           "Hasmik Ghazaryan Olson",
                           "find_something_pretty_everyday"),
    "about-working.jpg": ("photo-1641834090472-952828a18a22", "zhD0ndWYd9o",
                          "Jules Marvin Eguilos", "jmeguilos"),

    "not-found.jpg": ("photo-1517999349371-c43520457b23", "5bwgW8_9OPs",
                      "Sacha Verheij", "sachaverheij"),
}

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "assets" / "photos"
CDN = "https://images.unsplash.com"


def stock_url(photo: str, shape: str, cap: int = 0) -> str:
    """The photograph at the slot's shape, as Unsplash's CDN serves it.

    `cap` is the width Framer asked for in this particular reference, taken
    from its own `scale-down-to`. Honouring it keeps the srcset doing its job:
    a phone fetches the small variant rather than the full-size one.
    """
    w, h = (int(n) for n in shape.split("x"))
    if cap and cap < w:
        w, h = cap, round(h * cap / w)
    return (f"{CDN}/{photo}?ixlib=rb-4.1.0&fm=jpg&q=80"
            f"&fit=crop&crop=entropy&w={w}&h={h}")


def credits() -> str:
    lines = [
        "# Photography credits",
        "",
        "The photographs standing in until Global Bridge's own arrive. They are",
        "served from Unsplash's CDN rather than stored here, which is what the",
        "Unsplash API terms ask for. Each is free to use under the Unsplash",
        "licence; the credit below is the attribution that licence asks for.",
        "",
        "Replacing one is a matter of dropping a file at `assets/photos/<slot>`:",
        "a real file always wins over the stand-in, and `tools/photos.py` needs",
        "no edit.",
        "",
        "| Slot | Photographer | Photograph |",
        "| --- | --- | --- |",
    ]
    for _, (name, _, _) in SLOTS.items():
        if name not in STOCK:
            continue
        _, pid, who, handle = STOCK[name]
        lines.append(
            f"| `{name}` | [{who}](https://unsplash.com/@{handle}) | "
            f"[unsplash.com/photos/{pid}](https://unsplash.com/photos/{pid}) |")
    lines += [
        "",
        "`about-hero.png` has no stand-in: the template's is a cut-out on a",
        "transparent background, and a photograph cannot supply the alpha",
        "channel. It stays on the template's image until real photography of",
        "the founder arrives.",
        "",
        "The six squares under the testimonials have no stand-in either, on",
        "purpose. They sit beside named roles, so a stock face there would read",
        "as a client who does not exist.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    files = [p for p in ROOT.rglob("*")
             if p.suffix in {".html", ".mjs", ".js"}
             and ".git" not in p.parts and p.parent.name != "tools"]

    ours, stock, missing, touched = [], [], [], 0
    for old, (name, shape, what) in SLOTS.items():
        if (PHOTOS / name).exists():
            replace, bucket = lambda _m, n=name: f"/assets/photos/{n}", ours
        elif name in STOCK:
            def replace(m, photo=STOCK[name][0], shape=shape):
                cap = re.search(r"scale-down-to=(\d+)", m.group(0))
                return stock_url(photo, shape, int(cap.group(1)) if cap else 0)
            bucket = stock
        else:
            missing.append((name, shape, what))
            continue
        bucket.append(name)
        for path in files:
            text = path.read_text(encoding="utf-8")
            # every reference, with or without Framer's sizing query string
            swapped = re.sub(
                r"(?:/assets/images/)?" + re.escape(old) + r"[^\"'`\s,]*",
                replace, text)
            if swapped != text:
                path.write_text(swapped, encoding="utf-8")
                touched += 1

    (PHOTOS / "CREDITS.md").write_text(credits(), encoding="utf-8")

    print(f"placed {len(ours)} of our photos and {len(stock)} stand-ins "
          f"across {touched} files")
    if missing:
        print(f"{len(missing)} slots still on the template's image:")
        for name, shape, what in missing:
            print(f"  assets/photos/{name:24} {shape:>10}  {what}")


if __name__ == "__main__":
    main()
