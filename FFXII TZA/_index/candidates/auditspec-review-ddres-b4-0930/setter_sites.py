"""setter_sites.py - SWE2-AUDIT-SPEC (review of 3198ee367, RC-25 row): raw byte sweep of all .text for E8/E9 rel32
and 0F 8x rel32 (jcc) whose target is the silhouette setter 002CEE00, plus DIR64 pointers to it; prints the four
instructions before each call so the passed argument (ecx/edx) is visible. Control: the same sweep must find
the 00282DF0 call the record says feeds 0056A05E."""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
def sweep(target):
    t = tk.d[tk.TRO:tk.TRO + tk.TRS]; out = []
    for i in range(len(t) - 5):
        b = t[i]
        if b in (0xE8, 0xE9):
            if tk.TVA + i + 5 + struct.unpack_from("<i", t, i + 1)[0] == target: out.append((tk.TVA + i, "call" if b == 0xE8 else "jmp"))
        elif b == 0x0F and 0x80 <= t[i + 1] <= 0x8F and i + 6 <= len(t):
            if tk.TVA + i + 6 + struct.unpack_from("<i", t, i + 2)[0] == target: out.append((tk.TVA + i, "jcc"))
    return out
for tgt in (0x002CEE00, 0x00282DF0):
    s = sweep(tgt)
    print("%08X raw sites=%d dir64=%d" % (tgt, len(s), len(tk.reloc_ptrs(tgt, tgt + 1))))
    if tgt != 0x002CEE00:
        print("  control 0056A0xx site present: %s" % any(0x0056A000 <= a < 0x0056A060 for a, k in s)); continue
    for a, k in s:
        e, how = tk.owner(a)
        pre = [x for x in tk.fdis(e) if x.address < a][-4:]
        print("  %08X %s owner %s (%s): %s" % (a, k, "%08X" % e if e else "-", how, " ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in pre)))
