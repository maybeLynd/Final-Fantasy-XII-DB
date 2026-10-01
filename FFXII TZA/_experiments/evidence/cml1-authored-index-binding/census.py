"""Is the CML1 name resolver live in the shipped build, and what does the authored index column select?

Two tiers, both read-only:
  1. EXE: the gate FUN_0032F3D0 and the routine it ends in, read as bytes from the shipping image
     (set FF12_EXE; SHA-256 73461D08...21F8). The six call sites' kind argument is read from the
     instruction before each call.
  2. DATA: over every us .ebp container (set FF12_EBP_DIR), compare each section_008 / section_010
     entry's authored index with the first-match name lookup the resolver would compute
     (strncmp n = 23 over CAM7 names), and compare duplicate-name CAM7 records byte for byte.
Positive control for tier 2: the same walk must reproduce the published counts - 423 camera files /
3,933 entries, 113 shake files / 300 entries.
FABLE, 2026-09-12.
"""
import os, struct, sys, hashlib

EXE = os.environ["FF12_EXE"]
EBP = os.environ["FF12_EBP_DIR"]
BASE = 0x120000

d = open(EXE, "rb").read()
print("exe sha256", hashlib.sha256(d).hexdigest())
pe = struct.unpack_from("<I", d, 0x3C)[0]
ns = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, o + 8))


def rd(addr, n):
    r = addr - BASE
    for nm, vs, va, rs, ra in secs:
        if va <= r < va + vs:
            return d[ra + r - va: ra + r - va + n], nm
    return None, "?"


print("\n== tier 1: the gate")
for a, n, what in ((0x005C5230, 3, "routine the gate ends in"), (0x0032F3D0, 0x57, "FUN_0032F3D0 whole body")):
    b, s = rd(a, n)
    print("%08X %-6s %s: %s" % (a, s, what, b.hex(" ")))
body, _ = rd(0x0032F3D0, 0x57)
assert rd(0x005C5230, 3)[0] == b"\x33\xc0\xc3", "005C5230 is not xor eax,eax; ret"
# kind 0 -> mov ecx,4 ; kind 1 -> mov ecx,5 ; kind 2 -> lea ecx,[rbx+0xd] ; all then call 005C5230 and test eax
assert b"\xb9\x04\x00\x00\x00" in body and b"\xb9\x05\x00\x00\x00" in body and b"\x8d\x4b\x0d" in body
call_rel = struct.unpack_from("<i", body, 0x3C)[0]
print("call at 0032F40B targets %08X" % (0x0032F40B + 5 + call_rel))
assert 0x0032F40B + 5 + call_rel == 0x005C5230
print("kind argument at each call site of 0032F3D0:")
for site in (0x002E4D46, 0x00378AAB, 0x00378AEA, 0x00378B01, 0x003DA27B, 0x003DD1AB):
    pre, _ = rd(site - 8, 13)
    rel = struct.unpack_from("<i", pre, 9)[0]
    assert pre[8] == 0xE8 and site + 5 + rel == 0x0032F3D0, "%08X is not a call to 0032F3D0" % site
    if b"\xb9" in pre[:8]:
        k = pre.index(b"\xb9"); kind = struct.unpack_from("<I", pre, k + 1)[0]
    elif pre[6:8] == b"\x33\xc9":
        kind = 0
    else:
        kind = None
    print("  %08X  bytes %s  kind %s" % (site, pre.hex(" "), kind))

print("\n== tier 2: authored index vs first-match lookup")
U = lambda b, o: struct.unpack_from("<I", b, o)[0]
I = lambda b, o: struct.unpack_from("<i", b, o)[0]


def sections(b):
    if b[:4] != b"EBP2":
        return None
    n = U(b, 4); offs = list(struct.unpack_from("<%dI" % n, b, 0x10))
    pres = sorted((o, i) for i, o in enumerate(offs) if o); out = {}
    for k, (o, i) in enumerate(pres):
        out[i] = (o, (pres[k + 1][0] if k + 1 < len(pres) else len(b)) - o)
    return out


def cstr(b, o):
    return b[o:b.index(b"\0", o)]


paths = sorted(os.path.join(dp, f) for dp, _d, fs in os.walk(EBP) for f in fs if f.lower().endswith(".ebp"))
cam_files = cam_entries = shk_files = shk_entries = 0
diffs = []
for p in paths:
    b = open(p, "rb").read(); s = sections(b)
    if not s:
        continue
    if 8 in s and 9 in s:
        o8 = s[8][0]; o9 = s[9][0]; cam_files += 1
        recs = []; cur = o9 + U(b, o9 + 0x1C)
        for i in range(U(b, o9 + 4)):
            ln = U(b, cur + 4); recs.append((b[cur + 8:cur + 0x20].split(b"\0")[0], b[cur + 8:cur + ln])); cur += ln
        for i in range(U(b, o8 + 4)):
            e = o8 + 0x10 + 0x10 * i; nm = cstr(b, o8 + I(b, e)); idx = I(b, e + 4); cam_entries += 1
            same = [k for k, (x, _) in enumerate(recs) if x[:23] == nm[:23]]
            first = same[0] if same else -1
            if first != idx:
                a, c = first, idx
                ident = recs[a][1] == recs[c][1]
                nd = sum(1 for x, y in zip(recs[a][1], recs[c][1]) if x != y)
                diffs.append((os.path.basename(p), i, nm.decode("cp932", "replace"), idx, first, same, ident, nd))
    if 10 in s and 11 in s:
        shk_files += 1; o10 = s[10][0]; o11 = s[11][0]
        shk_entries += U(b, o10 + 4)
print("control: camera files %d entries %d (published 423 / 3,933); shake files %d entries %d (published 113 / 300)"
      % (cam_files, cam_entries, shk_files, shk_entries))
print("camera entries whose authored index != first-match lookup: %d" % len(diffs))
for f, i, nm, idx, first, same, ident, nd in diffs:
    print("  %-14s entry %2d %-24s authored %2d  first-match %2d  all matches %s  %s"
          % (f, i, nm, idx, first, same, "records identical" if ident else "records differ in %d bytes" % nd))
print("authored index is the LAST of the duplicates in %d of %d" % (sum(1 for x in diffs if x[3] == x[5][-1]), len(diffs)))
