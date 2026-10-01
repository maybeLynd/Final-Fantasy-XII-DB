"""sd5_indep.py - SWE2-AUDIT-SPEC's independent check of SD-5 (2026-09-30), not using the SD-7 value-flow engine.
1. Every reference to the three request setters (slot 12 007A0B10, slot 13 0079F140, slot 18 007A1180) and to the
   start-up setter 0079F150: raw rel32 E8/E9/0F8x over ALL .text, rip-relative lea/mov, DIR64 relocations (vtable slots).
   For each relocation, the qword's owner section and the RTTI-free neighbourhood (the vtable base = first slot whose
   predecessor is not a .text pointer) are printed, so a second vtable that also carries the setter is visible.
2. Indirect calls through slot offsets 0x60 / 0x68 / 0x90 (slots 12 / 13 / 18) anywhere in the framework range
   00790000-007A2000 and in the game-side application methods 0017xxxx (listed functions).
3. Linear dump of the per-frame update's resize block 0079C4A0-0079C5C5, and the window-data sites 0079B6D0-0079B6F0,
   007985F8-00798620, 007A07C0-007A07F2.
Control: the start-up setter 0079F150 must show at least one reference (it is live on the record's own reading).
"""
import sys, struct, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk  # noqa: E402

TG = [0x007A0B10, 0x0079F140, 0x007A1180, 0x0079F150]
text = tk.d[tk.TRO:tk.TRO + tk.TRS]
refs = {t: [] for t in TG}
for p in range(len(text) - 6):
    b = text[p]
    if b in (0xE8, 0xE9):
        L, rel = 5, struct.unpack_from("<i", text, p + 1)[0]
    elif b == 0x0F and 0x80 <= text[p + 1] <= 0x8F:
        L, rel = 6, struct.unpack_from("<i", text, p + 2)[0]
    else:
        continue
    a = tk.TVA + p; t = a + L + rel
    if t in refs:
        x = tk._decode_at(a)
        if x is not None and x.size == L:
            refs[t].append((a, x.mnemonic, tk.fname(a)))


def vt_base(q):
    a = q
    while True:
        v = tk.u64(a - 8)
        if v is None or not (tk.TVA <= v - 0 < tk.TVA + tk.TVS): return a
        a -= 8


for t in TG:
    rip = [(r[0].address, r[0].mnemonic, tk.fname(r[0].address)) for r in tk.rip_refs(t, t + 1)[0]]
    rel = tk.reloc_ptrs(t, t + 1)
    print("%08X: branch refs %d, rip refs %d, relocs %d" % (t, len(refs[t]), len(rip), len(rel)))
    for a, m, f in sorted(refs[t]) + sorted(rip):
        print("    %08X %-5s %s" % (a, m, f))
    for r in rel:
        q = r[0] if isinstance(r, tuple) else r
        vb = vt_base(q)
        print("    reloc at %08X (%s) vtable base %08X slot %d" % (q, tk.sec_of(q), vb, (q - vb) // 8))
ok = len(refs[0x0079F150]) + len(tk.reloc_ptrs(0x0079F150, 0x0079F151)) > 0
print("%s  control: the start-up setter 0079F150 has a reference" % ("PASS" if ok else "FAIL"))

print("-- indirect calls through +0x60 / +0x68 / +0x90 in 00790000-007A2000 and 00170000-00180000 (listed functions)")
pat = re.compile(r"^qword ptr \[(r\w+) \+ (0x60|0x68|0x90)\]$")
for f, n in tk.flist:
    if not (0x00790000 <= f < 0x007A2000 or 0x00170000 <= f < 0x00180000): continue
    for x in tk.dis(f, f + n):
        if x.mnemonic in ("call", "jmp") and pat.match(x.op_str):
            print("  %08X %s %s   in %s" % (x.address, x.mnemonic, x.op_str, tk.fname(x.address)))

for lo, hi in ((0x0079C4A0, 0x0079C5C5), (0x0079B6D0, 0x0079B6F0), (0x007985F8, 0x00798620), (0x007A07C0, 0x007A07F2)):
    print("-- %08X-%08X" % (lo, hi))
    o, how = tk.owner(lo)
    xs = tk.dis(o, o + (tk.fsize(o) or 0x2000))
    for x in xs:
        if lo <= x.address < hi:
            print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
