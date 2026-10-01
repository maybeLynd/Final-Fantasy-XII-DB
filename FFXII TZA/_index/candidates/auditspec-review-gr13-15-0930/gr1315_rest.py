"""gr1315_rest.py - GR-13/14/15 review, remaining items (2026-09-30).

  R2  classify every rva32 occurrence of the reach targets: is it a .pdata BeginAddress, an unwind chain entry, or other.
  T2  tables re-read at the checker's widths: 00D23920 as u32 x4 (shop tab ids), 00D0F990 as i32 x8 (nibble -> category).
  C2  0057BEA0 loop bound and 0057C0F7-0057C0FE (the tab index into 00D23920).
  C3  003FE30B-003FE324 (create +8 tested against 1); all references to 003FDA20 and 003FF040 (E8/E9, jcc, rip, abs64,
      rva32 classified), and 003FDA20's call site context.
"""
import os, sys, struct, bisect, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

IB, raw = T.IB, T.raw
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
PDVA = IB + dd.VirtualAddress
PDEND = PDVA + dd.Size
RCJ = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))


def secname(va):
    for n, v, vs, p, rs, x in T.SECS:
        if v <= va < v + vs:
            return n
    return "?"


def classify_rva32(t):
    out = []
    for s in T.data_refs(t)["rva32"]:
        va = int(s[:8], 16)
        if PDVA <= va < PDEND:
            k = (va - PDVA) % 12
            out.append("%08X .pdata %s" % (va, {0: "Begin", 4: "End", 8: "Unwind"}[k]))
        else:
            # unwind chained entry: RUNTIME_FUNCTION inside .xdata/.rdata after an UNWIND_INFO with UNW_FLAG_CHAININFO
            out.append("%08X %s other" % (va, secname(va)))
    return out


def ins(a, n=1):
    return list(T.md.disasm(T.rd(a, 16 * n), a, n))


def s(i):
    return "%08X %s %s" % (i.address, i.mnemonic, i.op_str)


print("== R2. rva32 occurrences of the reach targets, classified")
for t in (0x005651E0, 0x005636F0, 0x00563930, 0x00563B10, 0x00563D20, 0x0056E140, 0x0056D370, 0x002D2600, 0x002D28E0,
          0x002D2DB0, 0x002D1420):
    print("  %08X %s" % (t, classify_rva32(t)))

print("== T2. tables at the checker's widths")
print("  00D23920 u32 x4: %s" % [hex(x) for x in struct.unpack("<4I", T.rd(0x00D23920, 16))])
print("  00D0F990 i32 x8: %s" % list(struct.unpack("<8i", T.rd(0x00D0F990, 32))))
kinds = {}
for k in range(40):
    idn, kd = struct.unpack("<HH", T.rd(0x00D233A0 + 4 * k, 4))
    kinds[idn] = kd
print("  00D233A0 slots: 0x5AF->%s 0x5A2->%s 0x5AE->%s ; 0x405..0x40F -> %s"
      % (kinds.get(0x5AF), kinds.get(0x5A2), kinds.get(0x5AE), [kinds.get(x) for x in range(0x405, 0x410)]))

print("== C2. tab loop and tab index")
for a in (0x0057BE80,):
    for i in T.dis(0x0057BE80, 0x0057BEC0):
        print("  " + s(i))
print("  --")
for i in T.dis(0x0057C0E0, 0x0057C110):
    print("  " + s(i))

print("== C3. 003FE30B..003FE324; references to 003FDA20 / 003FF040")
for i in T.dis(0x003FE300, 0x003FE330):
    print("  " + s(i))
for t in (0x003FDA20, 0x003FF040):
    rc = RCJ.get("%X" % t, [])
    jc = T.jcc_callers(t)
    rr = ["%08X %s %s" % h[:3] for h in T.rip_refs(t, t + 1)]
    ab = T.data_refs(t)["abs64"]
    print("  %08X rel32 %s | jcc %s | rip %s | abs64 %s | rva32 %s" % (t, rc, jc, rr, ab, classify_rva32(t)))
print("  003FF040's call of 003FDA20, and the equip menu's call of 003FF040:")
for c in RCJ.get("3FDA20", []) + RCJ.get("3FF040", []):
    a = int(c, 16)
    for i in T.dis(a - 0x28, a + 5):
        if i.address >= a - 0x28:
            print("    " + s(i))
    print("    --")

print("== R2b. the '.rdata other' rva32 hits read as RUNTIME_FUNCTION triples (chained unwind entries?)")
for va in (0x01D900B4, 0x01D900C4, 0x01D71D24, 0x01D71D34, 0x01D71D68, 0x01D71D78, 0x01D71D8C, 0x01D71DD8, 0x01D71DE8):
    b, e, u = struct.unpack("<III", T.rd(va, 12))
    hdr = T.rd(IB + u, 4) if T.off(IB + u) is not None else b""
    ok = e > b and e - b < 0x10000 and hdr and (hdr[0] & 7) == 1
    print("  %08X begin %08X end %08X unwind %08X -> %s" % (va, IB + b, IB + e, IB + u, "RUNTIME_FUNCTION (unwind v1)" if ok else "NOT a triple"))
print("== C3b. function-aligned decode: 003FDFE0 create arm, and 003FF360's call of 003FF040")
for lo, hi, f in ((0x003FE300, 0x003FE330, 0x003FDFE0), (0x003FF740, 0x003FF76A, 0x003FF360)):
    for i in T.md.disasm(T.rd(f, hi - f), f):
        if lo <= i.address < hi:
            print("  " + s(i))
    print("  --")
