"""select_zlib.py - EC-7 member selector for zlib 1.2.11 (FABLE, 2026-09-13).

  zlib.tsv   every census entry in zlib's two link ranges, less A-measured entries and entries declared by another family:
               0080C5A0 up to 0080F2BC   inflate side: uncompress (the 24-byte shim) / uncompress2, inflate, inflateInit2,
                                         adler32, crc32 / crc32_z, inflate_fast, inflate_table
               0087AF40 up to 0087F180   deflate side: compress2, deflate, deflateInit_, the trees (_tr_init, bi_flush ...)

Asserts: both version banners ('inflate 1.2.11 Copyright 1995-2017 Mark Adler', 'deflate 1.2.11 Copyright 1995-2017
Jean-loup Gailly and Mark Adler'); inflate 0080C750 leas 'incorrect header check'; uncompress 0080C5A0 calls
uncompress2 0080C5C0 with &sourceLen; crc32 0080E5F0 and adler32 0080E300 are 'mov r8d,r8d; jmp' widening shims into
their _z bodies; the deflate side calls the inflate side's checksums (they are one library); the neighbours are not
zlib's (0080C51C ATL GetHInstanceAt below, the import thunk 0080F2BC above; 0087AF34 import thunk below, Bullet's
0087F180 above).
Prints the controls: outbound targets outside both ranges, inbound caller zones, shared .data globals.
Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe, graph/functions.tsv; needs capstone.
Usage: python select_zlib.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "zlib 1.2.11"
R = ((0x80C5A0, 0x80F2BC), (0x87AF40, 0x87F180))
inr = lambda a: any(lo <= a < hi for lo, hi in R)
d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(n):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (0x120000 + va, vs, ro, rs)
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs: return ro + (a - va)
sizes = cd.load_functions(); ents = sorted(sizes); eset = set(ents)
names = {}
for line in open(os.path.join(W, "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    p = line.split("\t")
    try: names[int(p[0], 16)] = p[1]
    except ValueError: pass
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and parts[0] != NAME:
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass
def body(e): return d[off(e):off(e) + sizes[e]]
md = Cs(CS_ARCH_X86, CS_MODE_64)
rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")

assert d[off(0x1CC9F51):off(0x1CC9F51) + 46] == b"inflate 1.2.11 Copyright 1995-2017 Mark Adler "
assert d[off(0x1CDA261):off(0x1CDA261) + 80].startswith(b"deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler")
assert d[off(0x1CC7C58):off(0x1CC7C58) + 22] == b"incorrect header check"
leas = {x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        for x in md.disasm(body(0x80C750), 0x80C750) for m in [rx.search(x.op_str)] if m and x.mnemonic == "lea"}
assert 0x1CC7C58 in leas
assert body(0x80C5A0)[14:19] == bytes([0xE8]) + struct.pack("<i", 0x80C5C0 - (0x80C5AE + 5))
for e, tgt in ((0x80E5F0, 0x80E910), (0x80E300, 0x80E310)):
    b = body(e); assert b[:3] == b"\x45\x8b\xc0" and b[3] == 0xE9 and e + 8 + struct.unpack_from("<i", b, 4)[0] == tgt, "%08X" % e
assert names.get(0x80C51C) == "GetHInstanceAt" and sizes.get(0x80F2BC) == 6 and sizes.get(0x87AF34) == 6 and not inr(0x87F180)

text = secs[".text"]; to = text[2]; tn = text[3]
def owner_of(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
callers = collections.defaultdict(set); out = collections.defaultdict(set); cross = 0
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to); t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    f = owner_of(src)
    if f is None or f == t: continue
    callers[t].add(f)
    if inr(src) and not inr(t): out[t].add(f)
    if R[1][0] <= src < R[1][1] and R[0][0] <= t < R[0][1]: cross += 1
assert cross > 0

span = [e for e in ents if inr(e)]
members, excl = [], collections.defaultdict(list)
for e in span:
    if e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    else: members.append(e)
print("zlib ranges: entries %d, members %d; deflate-side calls into the inflate side: %d" % (len(span), len(members), cross))
for k, v in sorted(excl.items()):
    print("  excluded %-50s %4d  %s" % (k, len(v), " ".join("%08X" % x for x in v)))
print("control outbound:", " ".join("%08X %s(%d)" % (t, names.get(t, ""), len(out[t])) for t in sorted(out)))
print("control inbound:", " ".join("%08X<-%s" % (e, ",".join("%08X" % f for f in sorted(callers[e]) if not inr(f))) for e in span if any(not inr(f) for f in callers[e])))
DATA = secs[".data"]; refs = collections.defaultdict(set)
for e in ents:
    if e < 0x121000 or e >= 0x8C2000 or sizes[e] <= 0: continue
    for x in md.disasm(body(e), e):
        m = rx.search(x.op_str)
        if not m: continue
        g = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if DATA[0] <= g < DATA[0] + DATA[1]: refs[g].add(e)
shared = sum(1 for g, fs in refs.items() if g != 0x1F44830 and any(inr(f) for f in fs) and any(not inr(f) for f in fs))
print("control globals: .data locations shared with outside code:", shared)
if "--write" in sys.argv:
    open(os.path.join(HERE, "zlib.tsv"), "w").write(
        "# zlib 1.2.11, 0080C5A0 up to 0080F2BC and 0087AF40 up to 0087F180, less A and other families - select_zlib.py\n"
        + "\n".join("%08X" % e for e in members) + "\n")
    print("wrote", len(members))
