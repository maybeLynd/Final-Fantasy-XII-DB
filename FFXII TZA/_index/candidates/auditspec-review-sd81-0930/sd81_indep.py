"""sd81_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SD-81 (2026-09-30). Read-only on the image.
Does not use retool.scan (the author's census instrument). Sweeps every .text byte for E8/E9 rel32 and 0F 8x rel32
(and EB/7x rel8) whose target is one of the six EASTL rbtree bodies, verifies each by decoding at the site, groups by
owner (listed function, else .pdata range), and compares with the published 99-row TSV and with rawcalls.json.
Then spot-checks K1/K2, the allocator tags and two instantiations' node size / reject path by instruction text.
"""
import sys, os, struct, json, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk

SIX = {0x16D6D0: "inc", 0x16D720: "dec", 0x16D780: "rotL", 0x16D7E0: "rotR", 0x16D840: "ins", 0x16DA60: "era"}
HERE = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(HERE, "..", "sd81-eastl-callers-0930", "sd81-callers.tsv")
RAW = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"

d, TRO, TRS, TVA = tk.d, tk.TRO, tk.TRS, tk.TVA
sites = []  # (site, kind, target)
for p in range(TRO, TRO + TRS - 5):
    b = d[p]
    if b in (0xE8, 0xE9):
        t = (TVA + (p - TRO) + 5 + struct.unpack_from("<i", d, p + 1)[0]) & 0xFFFFFFFF
        if t in SIX: sites.append((TVA + p - TRO, "call" if b == 0xE8 else "jmp", t))
    elif b == 0x0F and 0x80 <= d[p + 1] <= 0x8F and p + 6 <= TRO + TRS:
        t = (TVA + (p - TRO) + 6 + struct.unpack_from("<i", d, p + 2)[0]) & 0xFFFFFFFF
        if t in SIX: sites.append((TVA + p - TRO, "jcc32", t))
    elif b == 0xEB or 0x70 <= b <= 0x7F:
        t = (TVA + (p - TRO) + 2 + struct.unpack_from("<b", d, p + 1)[0]) & 0xFFFFFFFF
        if t in SIX: sites.append((TVA + p - TRO, "rel8", t))
verified = []
unverified = collections.Counter()
for s, k, t in sites:
    x = tk._decode_at(s)
    ok = x is not None and x.address == s and x.op_str == hex(t)
    o, how = tk.owner(s)
    onb = o is not None and s in tk.boundaries(s)
    if ok and onb:
        verified.append((s, k, t, o, how))
    else:
        unverified[(k, "decoded" if ok else "nodecode", "boundary" if onb else "offboundary")] += 1
print("raw rel sites to the six: %d; verified on an owner instruction boundary: %d" % (len(sites), len(verified)))
print("unverified raw hits by kind:", dict(unverified))
kinds = collections.Counter(k for _, k, _, _, _ in verified)
print("verified by kind:", dict(kinds))
own = collections.defaultdict(list)
for s, k, t, o, how in verified:
    own[o].append((s, SIX[t], k, how))
print("owners: %d; owners via .pdata only: %d; sites: %d" % (
    len(own), sum(1 for o in own if own[o][0][3] == "pdata"), sum(len(v) for v in own.values())))
pairs = sum(len({m for _, m, _, _ in v}) for v in own.values())
print("(owner, body) pairs: %d" % pairs)
tsv = set()
for line in open(TSV, encoding="utf-8"):
    c = line.rstrip("\n").split("\t")
    if c and len(c[0]) == 8:
        try: tsv.add(int(c[0], 16))
        except ValueError: pass
print("TSV rows: %d; owners not in TSV: %s; TSV rows not an owner: %s" % (
    len(tsv), ["%08X" % o for o in sorted(set(own) - tsv)], ["%08X" % o for o in sorted(tsv - set(own))]))
jmpish = [(s, SIX[t], k) for s, k, t, o, how in verified if k != "call"]
print("non-call control transfers into the six:", ["%08X %s %s" % j for j in jmpish])
small = sorted((tk.fsize(o) or 0, o) for o in own)[:3]
print("smallest owners (listed size):", ["%08X=%s" % (o, sz) for sz, o in small])
raw = json.load(open(RAW))
rc = set()
for m in SIX:
    for s in raw.get("%X" % m, []):
        rc.add(int(s, 16))
vs = {s for s, k, *_ in verified if k == "call"}
print("rawcalls.json sites to the six: %d; = verified call sites: %s; only in rawcalls: %d; only here: %d" % (
    len(rc), rc == vs, len(rc - vs), len(vs - rc)))
for m, n in SIX.items():
    rr, rawonly = tk.rip_refs(m, m + 1)
    rp = tk.reloc_ptrs(m, m + 1)
    print("refs to %08X %s: rip %d (raw-only %d), DIR64 relocs %d" % (m, n, len(rr), len(rawonly), len(rp)))

def show(a, n=1):
    for x in tk.dis(a, a + 16 * n)[:n]:
        print("   %08X  %s %s" % (x.address, x.mnemonic, x.op_str))

def cstr(a):
    o = tk.off(a); e = d.index(b"\0", o); return d[o:e].decode("latin1")
print("tags: 008F4120=%r 008F3CB0=%r" % (cstr(0x8F4120), cstr(0x8F3CB0)))
print("K1: 001FDC10 head and the call to 001FC420")
f = tk.fdis(0x1FDC10)
for i, x in enumerate(f):
    if x.address <= 0x1FDC1A or "0x1fc420" in x.op_str or "0x1fc9f0" in x.op_str or "rsp + 0x18" in x.op_str or "rsp + 0x10]" in x.op_str:
        print("   %08X  %s %s" % (x.address, x.mnemonic, x.op_str))
print("K1/K2: 001FC420 sites")
for a in (0x1FC487, 0x1FC4E8, 0x1FC55C): show(a)
x = tk._decode_at(0x1FC487)
if x and "rip" in x.op_str:
    tgt = x.address + x.size + x.operands[1].mem.disp
    print("   001FC487 lea target %08X = %r" % (tgt, cstr(tgt)))
print("B5 spot-check: node-size immediates and [reg+8] byte stores in insert-unique bodies I01 00199DB0 / I20 001FCB40")
for fn in (0x199DB0, 0x1FCB40):
    imms, bst = [], []
    for x in tk.fdis(fn):
        if x.mnemonic == "mov" and x.op_str.startswith(("ecx, 0x", "edx, 0x")):
            imms.append("%08X %s" % (x.address, x.op_str))
        if x.mnemonic == "mov" and x.op_str.startswith("byte ptr [") and "+ 8]" in x.op_str:
            bst.append("%08X %s" % (x.address, x.op_str))
    print("  %08X size %s: imm=%s" % (fn, tk.fsize(fn), imms[:6]))
    print("     byte [+8] stores=%s" % bst)
