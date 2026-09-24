"""Minimal reader for Framer's .framercms record format.

Layout, all integers big-endian:
  chunk  : u32 record-count, then the records back to back
  record : u16 field-count, then fields
  field  : u32 key-length, key, u8 type, payload
  payload: 0x05/0x0a/0x0c  u32 length then that many bytes (text / JSON / ref)
           0x04            8 bytes (timestamp)
           0x0b            u8 flag, u32 length, then that many bytes (richtext)
           0x01            u16 count, then that many u8-type-tagged values
The index file maps each record id to its (offset, length) in the chunk, so
changing a string means rewriting both files.
"""
import struct

U32 = ">I"
STR_TYPES = {0x05, 0x0a, 0x0c}

def read_value(b, i, t):
    if t in STR_TYPES:
        n = struct.unpack_from(U32, b, i)[0]
        return ("s", t, b[i+4:i+4+n]), i + 4 + n
    if t == 0x0b:
        n = struct.unpack_from(U32, b, i + 1)[0]
        return ("r", t, (b[i], b[i+5:i+5+n])), i + 5 + n
    if t == 0x04:
        return ("n", t, b[i:i+8]), i + 8
    if t == 0x01:
        n = struct.unpack_from(">H", b, i)[0]; i += 2
        items = []
        for _ in range(n):
            et = b[i]; i += 1
            v, i = read_value(b, i, et)
            items.append(v)
        return ("l", t, items), i
    raise ValueError(f"unknown type {t:#x} at {i}")

def write_value(v):
    kind, t, payload = v
    if kind == "s":
        return bytes([t]) + struct.pack(U32, len(payload)) + payload
    if kind == "r":
        flag, text = payload
        return bytes([t, flag]) + struct.pack(U32, len(text)) + text
    if kind == "n":
        return bytes([t]) + payload
    out = bytes([t]) + struct.pack(">H", len(payload))
    return out + b"".join(write_value(x) for x in payload)

def read_record(b, off):
    n = struct.unpack_from(">H", b, off)[0]
    i = off + 2
    fields = []
    for _ in range(n):
        kl = struct.unpack_from(U32, b, i)[0]; i += 4
        key = b[i:i+kl]; i += kl
        t = b[i]; i += 1
        v, i = read_value(b, i, t)
        fields.append((key, v))
    return fields, i

def write_record(fields):
    out = struct.pack(">H", len(fields))
    for key, v in fields:
        out += struct.pack(U32, len(key)) + key + write_value(v)
    return out

def map_strings(v, fn):
    kind, t, payload = v
    if kind == "s":
        return (kind, t, fn(payload))
    if kind == "r":
        return (kind, t, (payload[0], fn(payload[1])))
    if kind == "l":
        return (kind, t, [map_strings(x, fn) for x in payload])
    return v


# --- the sibling index file --------------------------------------------------
# section: u32 length + JSON descriptor, u8 key-count, that many u32-length
#          keys, u32 entry-count, then entries
# entry  : one value per key (0x00 = null, otherwise a value as above),
#          u16 padding, u32 record offset, u32 record length

def read_index(b):
    i, sections = 0, []
    while i < len(b):
        n = struct.unpack_from(U32, b, i)[0]; i += 4
        desc = b[i:i+n]; i += n
        nkeys = b[i]; i += 1
        keys = []
        for _ in range(nkeys):
            kl = struct.unpack_from(U32, b, i)[0]; i += 4
            keys.append(b[i:i+kl]); i += kl
        count = struct.unpack_from(U32, b, i)[0]; i += 4
        entries = []
        for _ in range(count):
            values = []
            for _ in range(nkeys):
                t = b[i]; i += 1
                if t == 0x00:
                    values.append(None)
                else:
                    v, i = read_value(b, i, t)
                    values.append(v)
            pad = b[i:i+2]; i += 2
            off, ln = struct.unpack_from(">II", b, i); i += 8
            entries.append([values, pad, off, ln])
        sections.append([desc, keys, entries])
    return sections

def write_index(sections):
    out = b""
    for desc, keys, entries in sections:
        out += struct.pack(U32, len(desc)) + desc + bytes([len(keys)])
        for k in keys:
            out += struct.pack(U32, len(k)) + k
        out += struct.pack(U32, len(entries))
        for values, pad, off, ln in entries:
            for v in values:
                out += b"\x00" if v is None else write_value(v)
            out += pad + struct.pack(">II", off, ln)
    return out
