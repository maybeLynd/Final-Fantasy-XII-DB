"""ns1_w7_flags.py - NS-1: what the packed-namespace class word w7 (record +0x1C) is (FABLE, Claude Opus 5.5, 2026-09-26;
first read by a delegated read-only pass, re-derived here from the bytes, the extract and the carried descriptor table).

  W1 the loader tests two bits of w7, walking the class records at stride 0x24 (0059B7D3 add rsi, 0x24):
     - bit 0 (0x01), "dynamic class": 0059B75A/0059B75E and 0059AC95 test it. When the runtime has no class of that
       name, a set bit builds a descriptor from the file instead of warning "File refers to compiled class ...".
     - bit 2 (0x04), "header": 0059D836 tests it in the instance-list walk. With no runtime descriptor, a set bit
       refuses the file with 6 (0059D840, with ecx zeroed at 0059D827). A clear bit stores null for the list
       instead (0059D8C2). 0059C0E3 tests the bit again in the packed-offset resolver.
  W2 the shipped corpus: every .phyre in the extract. w7 is constant per class name, takes the values
     {0, 2, 8, 12, 20, 32, 34, 40}, and bit 0 is set in no class.
  W3 w7 is the file copy of the runtime class descriptor's +0xFC flag byte. For every class that also has a carried
     runtime descriptor row (members/phyre-class-descriptor-vtable.tsv), w7 & 0x0E equals the +0xFC & 0x0E the
     descriptor's final template leaves: Concrete 0, Abstract 0x2, Header 0x4, WithoutDefaultConstructor 0x8,
     HeaderWithoutDefaultConstructor 0xC. So bit 1 = abstract, bit 2 = header, bit 3 = no default constructor,
     the reflection page's names for the same bits.
  W4 bit 4 (0x10) is set in w7 exactly on the classes whose runtime template is Header. The reflection page has the
     three Header classes' member registrars setting it.
  W5 image-wide, no instruction tests bit 4 or 5 of a +0xFC word in the reflection or loader code. The sweep covers
     `test`/`bt`/isolating `and` directly on [reg + 0xFC], and a load of it tested within eight instructions. The only
     such tests anywhere are in the actor-record code at 0028xxxx, which is a different structure. Control: the same
     sweep finds PCluster::create's bit-3 test at 0063A99A. Blind spot: the word read through a getter and tested in a
     caller.
So bits 0-3 are named and two of them drive the loader. Bits 4 and 5 are set, copied into the file, and tested by
nothing that was found; no use names them.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
check("W1 the loader tests w7 bit 0 (dynamic class) and bit 2 (header, refuse with 6), records at stride 0x24",
      at(0x59B7D3) == "add rsi, 0x24" and at(0x59B75A) == "movzx eax, byte ptr [rsi + 0x1c]" and at(0x59B75E) == "and al, 1"
      and at(0x59AC95) == "test byte ptr [rax + 0x1c], 1" and at(0x59D836) == "test byte ptr [rax + 0x1c], 4"
      and at(0x59D827) == "xor ecx, ecx" and at(0x59D83A) == "je 0x59d8c2" and at(0x59D840) == "lea eax, [rcx + 6]"
      and at(0x59D8C2) == "mov qword ptr [rdi], rcx" and at(0x59C0E3) == "test byte ptr [rdi + 0x1c], 4",
      "%s | %s" % (at(0x59B75E), at(0x59D840)))
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
w7 = collections.defaultdict(collections.Counter); nfiles = 0; pools = set()
for p in EX.rglob("*.phyre"):
    nfiles += 1
    with open(p, "rb") as f:
        h = f.read(12)
        if len(h) < 12: continue
        hs, ns = struct.unpack_from("<II", h, 4); f.seek(hs); b = f.read(ns)
    if len(b) < 0x20: continue
    A_, nC, nM, sp = struct.unpack_from("<IIII", b, 8)
    base = 0x20 + 4 * A_; pool = b[base + 36 * nC + 24 * nM:base + 36 * nC + 24 * nM + sp]
    key = (pool, b[base:base + 36 * nC])
    if key in pools: continue
    pools.add(key)
    for k in range(nC):
        rec = struct.unpack_from("<9I", b, base + 36 * k)
        w7[pool[rec[2]:pool.find(b"\0", rec[2])].decode("latin-1")][rec[7]] += 1
values = sorted({v for c in w7.values() for v in c})
conflicts = [c for c, v in w7.items() if len(v) > 1]
print("   .phyre %d, distinct namespaces %d, classes %d, w7 values %s" % (nfiles, len(pools), len(w7), values))
check("W2 w7 is constant per class, values {0,2,8,12,20,32,34,40}, bit 0 in no class",
      values == [0, 2, 8, 12, 20, 32, 34, 40] and not conflicts and not any(v & 1 for c in w7.values() for v in c),
      "conflicts %s" % conflicts[:3])
rows = [l.rstrip("\n").split("\t") for l in open(DB / "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/phyre-class-descriptor-vtable.tsv", encoding="utf-8") if not l.startswith("#")]
h = rows[0]; ci, di, ti = h.index("class"), h.index("descriptor_template"), h.index("final_template_rtti")
LOW = {"PClassDescriptorConcrete": 0x0, "PClassDescriptorAbstract": 0x2, "PClassDescriptorHeader": 0x4,
       "PClassDescriptorWithoutDefaultConstructor": 0x8, "PClassDescriptorHeaderWithoutDefaultConstructor": 0xC}
tmpl = {r[ci]: (r[ti] or r[di]) for r in rows[1:] if len(r) > ti}
joined = {c: (next(iter(v)), tmpl[c]) for c, v in w7.items() if c in tmpl}
bad = {c: (hex(w), t) for c, (w, t) in joined.items() if (w & 0x0E) != LOW.get(t, -1)}
check("W3 w7 & 0x0E equals the runtime template's +0xFC & 0x0E for every class with a carried descriptor row",
      len(joined) >= 100 and not bad, "joined %d, disagreeing %s" % (len(joined), bad))
b4 = {c for c, (w, t) in joined.items() if w & 0x10}; hdr = {c for c, (w, t) in joined.items() if t == "PClassDescriptorHeader"}
check("W4 bit 4 is set exactly on the Header-template classes", b4 == hdr and b4, "bit4 %s; Header %s" % (sorted(b4), sorted(hdr)))
vs, va, rs, ro = secs[0]
cs2 = Cs(CS_ARCH_X86, CS_MODE_64); cs2.skipdata = True
L = list(cs2.disasm(d[ro:ro + rs], BASE + va))
def imm(s):
    m = re.search(r", (0x[0-9a-f]+|\d+)$", s); return int(m.group(1), 0) if m else None
def isolates(mn, v, bits):
    if v is None: return False
    if mn == "bt": return v in bits
    mask = sum(1 << b for b in bits)
    return mn in ("test", "and") and bool(v & mask) and v < 0x100
def sweep(bits):
    hits = []
    for i, x in enumerate(L):
        if "+ 0xfc]" not in x.op_str: continue
        if x.mnemonic in ("test", "and", "bt") and isolates(x.mnemonic, imm(x.op_str), bits): hits.append(x.address)
        if x.mnemonic in ("mov", "movzx"):
            r = x.op_str.split(",")[0]; low = {"eax": "al", "ecx": "cl", "edx": "dl", "ebx": "bl"}.get(r, r)
            for y in L[i + 1:i + 9]:
                if y.mnemonic in ("test", "and", "bt") and y.op_str.split(",")[0] in (r, low) and isolates(y.mnemonic, imm(y.op_str), bits):
                    hits.append(y.address)
    return sorted(set(hits))
H45 = sweep((4, 5)); H3 = sweep((3,))
outside = [a for a in H45 if not (0x280000 <= a < 0x290000)]
check("W5 no test of bit 4 or 5 on a +0xFC word outside the actor-record code; control: the bit-3 test 0063A99A is found",
      outside == [] and 0x63A99A in H3,
      "bit4/5 tests %s; bit-3 tests %d" % (["%08X" % a for a in H45], len(H3)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
