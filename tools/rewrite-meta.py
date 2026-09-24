#!/usr/bin/env python3
"""Apply the same copy rewrite to Framer's site search index.

assets/meta/*.json holds every page's title, description and visible text for
the site search. It is ordinary JSON, so each string is rewritten in place and
the /journal/... page keys follow the renamed articles.
"""
import html
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent


def load_maps():
    ns = {"__name__": "rewrite_content"}
    exec(compile((HERE / "rewrite-content.py").read_text(),
                 "rewrite-content.py", "exec"), ns)
    return ns["NODE"], ns["TEXT"], ns["SLUGS"], ns["plain_forms"]()


NODE, TEXT, SLUGS, PLAIN = load_maps()
changed = 0


def convert(s: str) -> str:
    global changed
    before = s
    unescaped = {html.unescape(k): html.unescape(v) for k, v in NODE.items()}
    if s in NODE:
        s = NODE[s]
    elif s in unescaped:
        s = unescaped[s]
    else:
        for mapping in (PLAIN, TEXT):
            for old, new in mapping.items():
                # the index stores text unescaped, so "&amp;" is a bare "&"
                for o, n in ((old, new),
                             (html.unescape(old), html.unescape(new))):
                    if o in s:
                        s = s.replace(o, n)
                        break
        for old, new in SLUGS.items():
            if old in s:
                s = s.replace(old, new)
    if s != before:
        changed += 1
    return s


def walk(node):
    if isinstance(node, str):
        return convert(node)
    if isinstance(node, list):
        return [walk(x) for x in node]
    if isinstance(node, dict):
        return {convert(k): walk(v) for k, v in node.items()}
    return node


def main() -> None:
    root = HERE.parent
    files = sorted(root.glob("assets/meta/*.json"))
    if not files:
        sys.exit("no search index found")
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps(walk(data), ensure_ascii=False),
                        encoding="utf-8")
        print(f"  {path.relative_to(root)}")
    print(f"rewrote {changed} search index strings")


if __name__ == "__main__":
    main()
