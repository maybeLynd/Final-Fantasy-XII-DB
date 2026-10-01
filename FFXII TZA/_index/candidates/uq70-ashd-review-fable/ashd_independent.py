"""ashd_independent.py - FABLE's independent re-implementation of OPUS's ashd scheme, written from the record's text,
not from ashd_decode.py (FABLE, Claude Opus 5.5, 2026-09-27). DATA check: needs the local extract.

  R1  two layers decode to the declared sizes with each stream ending exactly at EOF
  R2  the payload's SHA-256 equals the record's (cc7c625a...), so two implementations agree byte for byte
  R3  the payload frame: tag, own size at +0x04, stamp / author / source at +0x10, and the name pool's 32 names with
      the counts the record gives (7 function names, 1 control name, 24 actor names)
  C   control: the same decoder applied with the literal count off by one fails R1 (it is sensitive to the spec)
"""
import hashlib, os, struct, sys
EXTRACT = os.environ.get("EXTRACT", r"D:/FFXII_TZA_extract")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def find(name):
    for r, _, fs in os.walk(EXTRACT):
        if name in fs and r.replace("\\", "/").endswith("katano"): return os.path.join(r, name)
def decode(buf, lit_bias=0):
    assert buf[:4] == b"ashd"
    field04, size = struct.unpack_from("<II", buf, 4)
    out = bytearray(); i = 12
    while i < len(buf) and len(out) < size:
        t = buf[i]
        if t % 2 == 0:
            n = (t >> 1) + lit_bias; out += buf[i + 1:i + 1 + n]; i += 1 + n
        else:
            w = t | (buf[i + 1] << 8); i += 2
            ln = (w >> 12) + 3; dist = ((w >> 1) & 0x7FF) + 1
            if dist > len(out): return field04, size, out, i, False
            for _ in range(ln): out.append(out[-dist])
    return field04, size, bytes(out), i, True
p = find("event.bin")
if not p: print("SKIP: katano/event.bin not in the extract"); sys.exit(0)
raw = open(p, "rb").read()
f1, s1, l1, e1, v1 = decode(raw)
f2, s2, l2, e2, v2 = decode(bytes(l1)) if v1 and l1[:4] == b"ashd" else (0, 0, b"", 0, False)
ok("R1", v1 and v2 and len(l1) == s1 == 0xB10 and e1 == len(raw) and len(l2) == s2 == 0x23E0 and e2 == len(l1),
   "layer 1 %#x of %#x ending %#x/%#x; layer 2 %#x of %#x ending %#x/%#x" % (len(l1), s1, e1, len(raw), len(l2), s2, e2, len(l1)))
h = hashlib.sha256(l2).hexdigest()
ok("R2", h == "cc7c625a8afc1a295e587b928e2a664b4b123542a9ba9bda77aad7a3b56faf6d", "payload sha256 %s" % h)
tag, own = struct.unpack_from("<II", l2, 0)
pool = struct.unpack_from("<I", l2, 0x4C)[0]
names = [n for n in l2[pool:].split(b"\0") if n][:32]
dec = [n.decode("cp932", "replace") for n in names]
funcs = [n for n in dec if n in ("init", "main", "setpc", "appear", "disappear", "clearpc", "control")]
actors = [n for n in dec if n.startswith("バッシュ")]
ok("R3", tag == 0x80000002 and own == len(l2) and b"09/18 20:20:10" in l2[0x54:0x80] and b"event.src" in l2[0x54:0xA0]
   and len(funcs) == 7 and len(actors) == 24 and "コントロール" in dec,
   "tag %#x, own size %s, functions %d, actors %d, control name %s" % (tag, own == len(l2), len(funcs), len(actors), "コントロール" in dec))
_, sc, lc, ec, vc = decode(raw, lit_bias=1)
ok("C", not (vc and len(lc) == sc and ec == len(raw)), "control: literal count +1 fails layer 1 (valid=%s, %#x of %#x)" % (vc, len(lc), sc))
print("FAILS", fails); sys.exit(1 if fails else 0)
