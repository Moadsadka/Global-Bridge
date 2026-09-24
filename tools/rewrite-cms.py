#!/usr/bin/env python3
"""Apply the same copy rewrite to Framer's CMS data files.

The journal is a Framer CMS collection. Its first four articles are rendered
into journal/index.html, but "Load More" and any client-side query read
assets/animate/*.framercms instead, so the articles have to be rewritten there
too or the template's copy comes back on the second page.

The chunk file holds the records; the index file holds each record's byte
offset and length, so changing any string means rewriting both. Run this after
rewrite-content.py, which owns the replacement maps.
"""
import pathlib
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import framercms as fc


def load_maps():
    """rewrite-content.py is not importable by name, so exec it instead."""
    ns = {"__name__": "rewrite_content"}
    exec(compile((HERE / "rewrite-content.py").read_text(),
                 "rewrite-content.py", "exec"), ns)
    return ns["NODE"], ns["TEXT"], ns["SLUGS"], ns["json_forms"]


NODE, TEXT, SLUGS, json_forms = load_maps()
changed = 0


def convert(raw: bytes) -> bytes:
    """Rewrite one stored value: a whole field, or richtext holding many."""
    global changed
    s = before = raw.decode("utf-8")
    if s in NODE:
        s = NODE[s]
    else:
        for old, new in TEXT.items():
            # richtext is stored as JSON, where quotes inside a sentence are
            # backslash-escaped.
            for o, n in zip(json_forms(old), json_forms(new)):
                if o in s:
                    s = s.replace(o, n)
        for old, new in NODE.items():
            # a whole text node, quoted inside the richtext JSON
            for q, o, n in zip(('"', r'\"'), json_forms(old), json_forms(new)):
                if f"{q}{o}{q}" in s:
                    s = s.replace(f"{q}{o}{q}", f"{q}{n}{q}")
        for old, new in SLUGS.items():
            if old in s:
                s = s.replace(old, new)
    if s != before:
        changed += 1
    return s.encode("utf-8")


def main() -> None:
    root = HERE.parent
    for chunk in sorted(root.glob("assets/animate/*-chunk-default-*.framercms")):
        index = chunk.with_name(chunk.name.replace("-chunk-", "-indexes-"))
        if not index.exists():
            continue

        blob = chunk.read_bytes()
        count = struct.unpack_from(">I", blob, 0)[0]
        records, off = [], 4
        for _ in range(count):
            fields, end = fc.read_record(blob, off)
            records.append((off, end - off, fields))
            off = end
        if off != len(blob):
            sys.exit(f"{chunk.name}: {len(blob) - off} bytes left over")

        out, remap = struct.pack(">I", count), {}
        for old_off, old_len, fields in records:
            body = fc.write_record(
                [(k, fc.map_strings(v, convert)) for k, v in fields])
            remap[old_off] = (len(out), len(body))
            out += body

        sections = fc.read_index(index.read_bytes())
        for _, _, entries in sections:
            for entry in entries:
                entry[0] = [None if v is None else fc.map_strings(v, convert)
                            for v in entry[0]]
                if entry[2] not in remap:
                    sys.exit(f"{index.name}: offset {entry[2]} is not a record")
                entry[2], entry[3] = remap[entry[2]]

        chunk.write_bytes(out)
        index.write_bytes(fc.write_index(sections))
        print(f"  {chunk.relative_to(root)}\n  {index.relative_to(root)}")

    print(f"rewrote {changed} CMS values")


if __name__ == "__main__":
    main()
