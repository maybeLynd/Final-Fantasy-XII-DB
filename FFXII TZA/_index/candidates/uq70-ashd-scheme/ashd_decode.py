"""ashd_decode.py - OPUS (Claude Opus 5.5), 2026-09-27, for UQ-70's ashd residue (OPUS-STRUCT-UQ70-ASHD-SCHEME).

DATA: decodes ps2data/image/ff12/katano/event.bin, the only file in the extract that opens with the magic 'ashd',
with a scheme recovered from the data alone, and checks the result against the file's own declared sizes.

The scheme (every part is tested below):
  header   'ashd', u32 field04 (role open, see README), u32 decodedSize; the token stream starts at +0x0C.
  token t  even -> a literal run: copy the next t>>1 bytes (0..127).
           odd  -> a back-reference: w = t | next<<8 (little-endian u16);
                   length   = (w >> 12) + 3            (3..18)
                   distance = ((w >> 1) & 0x7FF) + 1    (1..2048), counted back from the current output end.
  The file is two layers deep: layer 1's output is itself an 'ashd' file, and its output is the payload.

Checks:
  D1  layer 1 decodes to exactly its declared size, consumes the stream exactly to EOF, no reference before the start.
  D2  the same for layer 2 (the layer-1 output).
  D3  the payload has the section-000 script-image frame documented in
      25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md: tag with bit 31 set, +0x04 = its own size,
      +0x10 -> the build stamp followed by author and source name, +0x48 -> zeroed local storage up to +0x4C,
      +0x4C -> the name pool.
  C1  control: the same frame holds for a shipped image (ch/bin/ctrl.ebp's section 000 at +0x80, tag 0x8000000B).
  K1-K4  kill controls: each one-part change to the grammar, applied to both layers, must break the pipeline D1-D3.
      Lengths and literal counts already break D1 (the size and the stream end depend on them). The distance does not
      change any size, so D1 alone cannot pin it: a wrong distance is caught by layer 2 and the frame, which read the
      bytes the references produced (measured 2026-09-27: 'field' and 'field + 2' both pass D1).
Skips without the local extract; exits 1 on any failed check.
"""
import hashlib
import os
import struct
import sys

ROOT = r"D:/FFXII_TZA_extract/ps2data/image/ff12"
P = ROOT + "/katano/event.bin"
CTRL = ROOT + "/ch/bin/ctrl.ebp"
if not os.path.exists(P):
    print("SKIP no extract")
    sys.exit(0)


def layer(d, lit=lambda t: t >> 1, dist_of=lambda f: f + 1, len_of=lambda n: n + 3):
    """One ashd layer -> (field04, declared, output, invalid references, stream end).
    A reference is invalid when it starts before the output or has distance 0 (it would read the byte being written)."""
    field04, declared = struct.unpack_from("<II", d, 4)
    p, out, before = 0x0C, bytearray(), 0
    while p < len(d):
        t = d[p]
        if t & 1 == 0:
            n = lit(t)
            out += d[p + 1:p + 1 + n]
            p += 1 + n
        else:
            if p + 1 >= len(d):
                return field04, declared, bytes(out), before, p + 2
            w = t | d[p + 1] << 8
            dist = dist_of((w >> 1) & 0x7FF)
            n, s = len_of(w >> 12), len(out) - dist
            if s < 0 or dist < 1:
                before += 1
            for k in range(n):
                out.append(out[s + k] if 0 <= s + k < len(out) else 0)
            p += 2
    return field04, declared, bytes(out), before, p


def clean(d, **kw):
    f, decl, out, before, end = layer(d, **kw)
    return len(out) == decl and end == len(d) and before == 0, (f, decl, out, before, end)


fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


raw = open(P, "rb").read()
check("D0", raw[:4] == b"ashd" and len(raw) == 2370, "katano/event.bin is 2,370 bytes and opens with 'ashd'")
ok1, (f1, decl1, mid, bef1, end1) = clean(raw)
check("D1", ok1, "layer 1: declared 0x%X, decoded 0x%X, stream end 0x%X of 0x%X, %d references before the start"
      % (decl1, len(mid), end1, len(raw), bef1))
ok2 = False
if mid[:4] == b"ashd":
    ok2, (f2, decl2, pay, bef2, end2) = clean(mid)
    check("D2", ok2, "layer 2: declared 0x%X, decoded 0x%X, stream end 0x%X of 0x%X, %d references before the start"
          % (decl2, len(pay), end2, len(mid), bef2))
else:
    check("D2", False, "layer 1 output does not open with 'ashd'")


def frame(img):
    """The section-000 frame facts D3 / C1 test, or a reason string."""
    tag, size = struct.unpack_from("<II", img, 0)
    stamp, locals48, pool = struct.unpack_from("<I", img, 0x10)[0], *struct.unpack_from("<II", img, 0x48)
    strs = img[stamp:stamp + 64].split(b"\0")
    return {"tag": tag, "size_ok": size == len(img), "stamp": strs[0], "author": strs[1], "src": strs[2],
            "locals_zero": pool > locals48 and not any(img[locals48:pool]), "pool": img[pool:pool + 10]}


if ok2:
    fr = frame(pay)
    good = (fr["tag"] & 0x80000000 and fr["size_ok"] and fr["stamp"][2:3] == b"/" and fr["src"].endswith(b".src")
            and fr["locals_zero"])
    check("D3", bool(good), "payload: tag 0x%08X, +0x04 = own size %s, stamp %r, author %r, source %r, "
          "+0x48..+0x4C zero %s, name pool %r" % (fr["tag"], fr["size_ok"], fr["stamp"], fr["author"], fr["src"],
                                                   fr["locals_zero"], fr["pool"]))
    print("INFO payload %d bytes, sha256 %s" % (len(pay), hashlib.sha256(pay).hexdigest()))
    print("INFO field04: layer 1 0x%X, layer 2 0x%X (role open; the decoder does not use it)" % (f1, f2))
if os.path.exists(CTRL):
    c = open(CTRL, "rb").read()
    img = c[0x80:0x80 + struct.unpack_from("<I", c, 0x84)[0]]
    fr = frame(img)
    check("C1", fr["tag"] == 0x8000000B and fr["size_ok"] and fr["stamp"][2:3] == b"/" and fr["src"] == b"ctrl.src",
          "control ch/bin/ctrl.ebp section 000: tag 0x%08X, own size %s, stamp %r, author %r, source %r"
          % (fr["tag"], fr["size_ok"], fr["stamp"], fr["author"], fr["src"]))
else:
    check("C1", False, "control file missing")

KILLS = (("K1", "literal run = (t>>1)+1", dict(lit=lambda t: (t >> 1) + 1)),
         ("K2", "distance = field (no +1)", dict(dist_of=lambda f: f)),
         ("K3", "length = nibble + 2", dict(len_of=lambda n: n + 2)),
         ("K4", "distance = field + 2", dict(dist_of=lambda f: f + 2)))


def pipeline(**kw):
    """D1-D3 under a grammar variant -> (clean, where it broke)."""
    ok, (_, decl, out, before, end) = clean(raw, **kw)
    if not ok:
        return False, "layer 1: decoded 0x%X of 0x%X, end 0x%X of 0x%X, %d before the start" % (
            len(out), decl, end, len(raw), before)
    if out[:4] != b"ashd":
        return False, "layer 1 output does not open with 'ashd'"
    ok, (_, decl, pay2, before, end) = clean(out, **kw)
    if not ok:
        return False, "layer 2: decoded 0x%X of 0x%X, end 0x%X of 0x%X, %d before the start" % (
            len(pay2), decl, end, len(out), before)
    try:
        fr = frame(pay2)
    except (struct.error, IndexError):
        return False, "payload has no readable frame"
    if not (fr["tag"] & 0x80000000 and fr["size_ok"] and fr["src"].endswith(b".src") and fr["locals_zero"]):
        return False, "payload frame fails (tag 0x%08X, source %r)" % (fr["tag"], fr["src"])
    return True, "clean"


for tag, what, kw in KILLS:
    ok, where = pipeline(**kw)
    check(tag, not ok, "%s breaks the pipeline: %s" % (what, where))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
