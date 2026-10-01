"""sd3_indep.py - SWE2-AUDIT-SPEC's independent check of SD-3 (2026-09-30).
1. Raw rel32 (E8 / E9 / 0F 8x) references over ALL .text bytes to 00228380, 00229AF0, 0017D4B0, 002282F0 and 00229590,
   plus rip-relative lea/mov references to 00229590 and 00229AF0 (a handler address can escape as data), plus DIR64
   relocations pointing at them (vtable / table slots).
2. Linear dump of 00229AF0 and 00228380 with every bt/test on bit 21 (0x15 / 0x200000) marked, read by hand.
3. Names of the callees the record relies on (functions.tsv).
Control: 00253C70 must appear as a caller of 00228380 (the record's one caller); a sweep that misses it is blind.
"""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk  # noqa: E402

TG = [0x00228380, 0x00229AF0, 0x0017D4B0, 0x002282F0, 0x00229590]
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
for t in TG:
    rr = tk.rip_refs(t, t + 1)
    rip = [(r[0].address, r[0].mnemonic, tk.fname(r[0].address)) for r in rr[0]]
    rel = tk.reloc_ptrs(t, t + 1)
    print("%08X %s: branch refs %d, rip refs %d, relocs %d" % (t, tk.names.get(t, "?"), len(refs[t]), len(rip), len(rel)))
    for a, m, f in sorted(refs[t]) + sorted(rip):
        print("    %08X %-5s %s" % (a, m, f))
    for r in rel:
        print("    reloc %s" % (r,))
ok = any("00253C70" in f for _, _, f in refs[0x00228380])
print("%s  control: 00253C70 found as a caller of 00228380" % ("PASS" if ok else "FAIL"))
for f in (0x00229AF0, 0x00228380):
    print("-- %s" % tk.fname(f))
    for x in tk.fdis(f):
        mark = "   <== bit 21" if (x.mnemonic in ("bt", "test") and ("0x15" in x.op_str or "0x200000" in x.op_str)) else ""
        print("  %08X %s %s%s" % (x.address, x.mnemonic, x.op_str, mark))
for c in (0x002E0FA0, 0x002E1020, 0x00226BD0, 0x002DF370, 0x00228480, 0x00244F50, 0x00253C70, 0x007A3B20):
    print("name %08X %s" % (c, tk.names.get(c, "(not listed)")))
