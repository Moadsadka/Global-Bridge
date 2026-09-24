#!/usr/bin/env python3
"""Apply the same copy rewrite to the template's page modules.

The exported HTML is only the server render. Framer ships the same pages again
as JavaScript modules under assets/animate, and React re-renders from those on
hydration, so any string left untouched here comes back a moment after load.

Text in those modules is a backtick template literal, which makes a whole
string easy to match exactly. A heading with one coloured word is built as an
array of runs instead, so those are matched across the span that separates
them. Run this after rewrite-content.py, which owns the replacement maps.
"""
import html as H
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def load_maps():
    ns = {"__name__": "rewrite_content"}
    exec(compile((HERE / "rewrite-content.py").read_text(),
                 "rewrite-content.py", "exec"), ns)
    return ns


NS = load_maps()
NODE, TEXT, SLUGS = NS["NODE"], NS["TEXT"], NS["SLUGS"]
WHOLE = {**NS["WORD_SPLIT"], **NODE}
ACCENT = NS["accent_parts"]()

# Headings the exported HTML animates word by word are plain accent headings in
# the page modules, so they need the runs spelled out here. Each one rebuilds
# the same sentence as its WORD_SPLIT entry.
JS_ACCENT = [
    (["The signs that something ", "needs", " to change."],
     ["The friction that slows a ", "principal", " down."]),
    (["It started and ended with ", "burnout."],
     ["It began with one missed ", "connection."]),
    (["Let's have a ", "conversation."],
     ["Tell us where you are ", "going."]),
    (["Writing from the ", "other side", " of burnout."],
     ["Notes from the ", "travel desk", "."]),
    (["You ", "wandered", " off the path."],
     ["This page has ", "moved", " on."]),
]

# Strings the modules carry in a longer form than the rendered page does.
JS_TEXT = {
    "I used to lie awake replaying work conversations. Now I actually sleep "
    "through the night. Maya helped me find calm in the chaos that was my life.":
        "Four cities in six days and not one arrangement needed my attention.",
    "} - Holistic`": "} - Global Bridge`",
}



# a run of text, then the coloured <span> element, then the next run
GAP = r"(.{0,400}?children:)"
TAIL = r"(.{0,40}?)"


def accent_regexes():
    for old, new in ACCENT + JS_ACCENT:
        pat = re.escape(f"`{old[0]}`") + GAP + re.escape(f"`{old[1]}`")
        if len(old) > 2:
            pat += TAIL + re.escape(f"`{old[2]}`")

        def repl(m, new=new):
            out = f"`{new[0]}`" + m.group(1) + f"`{new[1]}`"
            if len(new) > 2:
                out += m.group(2) + f"`{new[2]}`"
            return out

        yield re.compile(pat, re.S), repl


REGEXES = list(accent_regexes())


def forms(old: str, new: str):
    """The pair as written, and again with its HTML entities resolved."""
    pairs = [(old, new)]
    plain = (H.unescape(old), H.unescape(new))
    if plain[0] != old:
        pairs.append(plain)
    return pairs


def main() -> None:
    root = HERE.parent
    files = sorted(p for p in root.rglob("*.mjs")) + \
        sorted(p for p in root.rglob("*.js"))
    files = [p for p in files if ".git" not in p.parts and "tools" not in p.parts]
    counts = {"accent": 0, "whole": 0, "text": 0, "slug": 0}

    for path in files:
        src = before = path.read_text(encoding="utf-8")

        for rx, rep in REGEXES:
            src, n = rx.subn(rep, src)
            counts["accent"] += n

        for old, new in WHOLE.items():
            for o, n in forms(old, new):
                if f"`{o}`" in src:
                    counts["whole"] += src.count(f"`{o}`")
                    src = src.replace(f"`{o}`", f"`{n}`")

        for old, new in {**TEXT, **JS_TEXT}.items():
            for o, n in forms(old, new):
                if o in src:
                    counts["text"] += src.count(o)
                    src = src.replace(o, n)

        for old, new in SLUGS.items():
            if old in src:
                counts["slug"] += src.count(old)
                src = src.replace(old, new)

        if src != before:
            path.write_text(src, encoding="utf-8")
            print(f"  {path.relative_to(root)}")

    print("rewrote {accent} accent headings, {whole} labels, {text} strings "
          "and {slug} links in the page modules".format(**counts))


if __name__ == "__main__":
    main()
