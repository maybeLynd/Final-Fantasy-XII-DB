"""RC-25: which char_silhouette pages the code indexes (SWE2-DATA 2026-09-30), static.

002CEFD0 is the only silhouette caller of the .as7 walker 0024AA00 (raw E8/E9 sweep below). It decodes two runs of
0x102 pages each: [g*0x204, g*0x204 + 0x102) into the buffer at +0xE0 and [g*0x204 + 0x102, g*0x204 + 0x204) into
+0xE8, with g = T[s], T = the six dwords built at rsp+0x30 (a 16-byte .rdata copy from 00917160 plus 4, 5) and
s = signed byte [obj + 0x10D]. The only writer of +0x10D with a live value is the setter 002CEE00 (ecx), which also
clears the 'silhouette on' bit (+0x10C bit 1) when ecx > 5; its callers pass -1 (005679D0) and the word +0x60 of the
record 00282DF0 returns for [0209AC30]+0xDE0 (0056A010).
Checks: S1 the page arithmetic; S2 T = {0,1,3,2,4,5}; S3 the walker's silhouette call sites are exactly the two in
002CEFD0; S4 six groups of 0x204 pages partition the shipped 3,096 exactly (every page belongs to one g in 0..5);
S5 the setter bound and its two callers. Control C1: the same raw call sweep finds the item_gra call 00292768.
"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, BASE, secs, owner, dis, u32  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def rawcallers(t):
    out = []
    for name, va, vs, ro, rs in secs:
        if name != ".text":
            continue
        blob = d[ro:ro + rs]
        for p in range(len(blob) - 5):
            if blob[p] in (0xE8, 0xE9) and BASE + va + p + 5 + struct.unpack_from("<i", blob, p + 1)[0] == t:
                out.append(BASE + va + p)
    return out


s = {x.address: x for x in dis(0x002CEFD0)}
for a in (0x002CEFEF, 0x002CEFF7, 0x002CEFFF, 0x002CF235, 0x002CF249, 0x002CF2A0, 0x002CF2B0, 0x002CF2B4, 0x002CF2C0,
          0x002CF2CE):
    print("   %08X %s %s" % (a, s[a].mnemonic, s[a].op_str))
check("S1 first page = T[s] * 0x204; runs of 0x102 at first and first + 0x102",
      s[0x002CF249].op_str == "ebp, dword ptr [rsp + rax*4 + 0x30], 0x204" and s[0x002CF2A0].op_str == "r14d, 0x102"
      and s[0x002CF2C0].op_str == "r8d, [r14 + rbp]" and s[0x002CF235].op_str == "rax, byte ptr [rbx + 0x10d]")
T = [u32(0x00917160 + 4 * i) for i in range(4)] + [4, 5]
check("S2 T = {0,1,3,2,4,5} (00917160 + the two immediates)", T == [0, 1, 3, 2, 4, 5] and
      s[0x002CEFF7].op_str.endswith("4") and s[0x002CEFFF].op_str.endswith("5"), str(T))
calls = sorted(rawcallers(0x0024AA00))
print("   raw callers of 0024AA00: %s" % " ".join("%08X in %08X" % (a, owner(a)) for a in calls))
check("S3 the silhouette call sites of the walker are exactly 002CF2B4 and 002CF2CE",
      [a for a in calls if owner(a) == 0x002CEFD0] == [0x002CF2B4, 0x002CF2CE])
check("C1 control: the sweep also finds the item_gra call 00292768", 0x00292768 in calls)
b = open("D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/in/bin_menu/char_silhouette.as7", "rb").read()
cnt = b[2] << 8 | b[3]
check("S4 six groups of 0x204 pages partition the shipped page count exactly", cnt == 6 * 0x204, "count %d" % cnt)
e = {x.address: x for x in dis(0x002CEE00)}
check("S5 the setter stores ecx to +0x10D and turns the silhouette bit off when ecx > 5 (unsigned: -1 too)",
      e[0x002CEE1A].op_str == "byte ptr [r8 + 0x10d], cl" and e[0x002CEE21].op_str == "ecx, 5"
      and e[0x002CEE24].mnemonic == "ja" and e[0x002CEE45].op_str == "dl, 0xfd")
setc = sorted(rawcallers(0x002CEE00))
print("   raw callers of the setter 002CEE00: %s" % " ".join("%08X in %08X" % (a, owner(a)) for a in setc))
check("S5b the setter's callers are 00567A52 (ecx = -1) and 0056A05E (ecx = word [record + 0x60])",
      setc == [0x00567A52, 0x0056A05E])
print("FAILS %d" % FAILS)
