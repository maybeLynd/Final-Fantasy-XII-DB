"""sd107o_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SWE2-ORACLE's SD-107 record
(sd107-register-stores-0930, dedfaf0d7). Written without the package's checker, retool.py or regval.py: the lane
loader ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha256 asserted), capstone, pefile.

  A  pinned text of the setters 002475D0 / 00247680 / wrapper 00247590 and the stub 005C5230
  B  reference census of the setters, the six widget procedures, and the five kind readers: E8/E9 rel32, jcc 0F 8x,
     abs64 / rva32 in any section, rip-relative lea/mov into the entry (function address taken)
  C  per setter site: the instructions before the call that set edx/dl/rdx and rcx (read by eye, printed)
  D  the widget layout: 002465F0 body (+0 / +0x48 stores), 00244F50 size default, the text-element builder 002B3C30
  E  S5 embedded-element sizes: allocation sizes of the 00241D40 / 0057C480 widgets vs element offset + 0xD0
  F  S6: the 002AF960 call inside 002D8550 - is its element the incoming r9?
  G  C1 independent: every `mov [base+disp], gpr` (no index; base not rsp/rbp/rip) whose byte range covers +0xA3,
     over every .pdata function; control: the 93 sites the package lists must all be found
  H  S7 samples: straight-line check of same-field copies; RTTI of the vtable holding each 'polymorphic this' function
"""
import bisect, collections, json, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_REG, CS_OP_IMM
from capstone.x86 import X86_REG_RIP

IB = T.IB
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def pdata_entry(va):
    j = bisect.bisect_right(ST, va - IB) - 1
    return PD[j] if j >= 0 and PD[j][0] <= va - IB < PD[j][1] else None


def show(a, b, mark=()):
    for i in T.dis(a, b):
        s = "    %08X  %-8s %s" % (i.address, i.mnemonic, i.op_str)
        for m, sz in T.mem_ops(i):
            if m.base == X86_REG_RIP:
                s += "   ; -> %08X" % (i.address + i.size + m.disp)
        if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == CS_OP_IMM:
            pass
        print(s + ("   <==" if i.address in mark else ""))


def refs(tgt):
    r = T.rel32_callers(tgt) + T.jcc_callers(tgt)
    d = T.data_refs(tgt)
    rr = T.rip_refs(tgt, tgt + 1)
    return r, d["abs64"], d["rva32"], ["%08X %s %s" % (h[0], h[1], h[2]) for h in rr]


part = sys.argv[1] if len(sys.argv) > 1 else "ABCDEFGH"

if "A" in part:
    print("== A. setters")
    show(0x00247590, 0x002475A8)
    print("  --")
    show(0x002475D0, 0x00247620)
    print("  --")
    show(0x00247680, 0x00247698)
    print("  --")
    show(0x005C5230, 0x005C5233)
    print("  bytes before 002475D0:", T.rd(0x002475C8, 8).hex(), " before 00247680:", T.rd(0x00247678, 8).hex(),
          " before 00247590:", T.rd(0x00247588, 8).hex())

if "B" in part:
    print("== B. reference census")
    for name, t in [("setter 002475D0", 0x002475D0), ("setter 00247680", 0x00247680), ("wrapper 00247590", 0x00247590),
                    ("proc 00227EE0", 0x00227EE0), ("proc 00241D40", 0x00241D40), ("proc 003F4330", 0x003F4330),
                    ("proc 0057C480", 0x0057C480), ("proc 005599D0", 0x005599D0), ("proc 0056B4D0", 0x0056B4D0),
                    ("reader 002B3930", 0x002B3930), ("reader 002ABF20", 0x002ABF20), ("reader 002ABEC0", 0x002ABEC0),
                    ("dispatcher 002AF960", 0x002AF960), ("emit 002D8550", 0x002D8550)]:
        r, a64, r32, rr = refs(t)
        print("  %-20s rel32/jcc %d %s | abs64 %s | rva32 %s | rip %s" % (name, len(r), " ".join(x.split()[0] for x in r),
              a64, r32, rr))

if "C" in part:
    print("== C. setter sites (preceding instructions)")
    SITES = ["228070", "242060", "24759D", "296994", "298521", "29C7C8", "29CA28", "2A7164", "2A73F5", "2D682A",
             "3F4649", "57C802", "2A71A6", "559B64", "55A2E3", "56B79B", "56B9BE", "572823", "279C60", "27A5B1"]
    for s in SITES:
        a = int(s, 16)
        print("  site %08X" % a)
        # linear decode from 0x30 back, keeping the decode that lands exactly on the site
        for back in range(0x40, 0x10, -1):
            ins = T.dis(a - back, a + 5)
            if any(i.address == a for i in ins):
                for i in ins[-9:]:
                    print("    %08X  %-8s %s" % (i.address, i.mnemonic, i.op_str))
                break

if "D" in part:
    print("== D. widget constructor 002465F0 / allocator 00244F50 / text-element builder 002B3C30")
    show(0x002465F0, 0x00246760)
    print("  -- 00244F50")
    show(0x00244F50, 0x00244FE0)
    print("  -- 002B3C30 (first 0x120 bytes)")
    show(0x002B3C30, 0x002B3D50)

if "E" in part:
    print("== E. widget allocations around the procedure registrations")
    for a, b in [(0x00227E70, 0x00227EC8), (0x00241C40, 0x00241CF0), (0x003F4740, 0x003F47B0), (0x0057C380, 0x0057C3C0),
                 (0x00559880, 0x005598E8), (0x0056B3A0, 0x0056B3D0), (0x002A2C00, 0x002A2C40)]:
        print("  -- %08X" % a)
        show(a, b)
    print("  -- 00241D40 element build / 0057C480 element build")
    show(0x00241DC0, 0x00241DF0)
    show(0x0057C500, 0x0057C525)

if "F" in part:
    print("== F. 002D8550 (r9 to 002AF960 at 002D8620)")
    show(0x002D8550, 0x002D8630, mark=(0x002D8620,))
    print("== F2. 002A4830 second path (002A4899 / 002A4919 / 002A4B3E)")
    show(0x002A4890, 0x002A48A0)
    show(0x002A4905, 0x002A4925)
    show(0x002A4B30, 0x002A4B43)

if "G" in part or "H" in part:
    # Raw disp32 scan over executable sections: any displacement that can put +0xA3 inside an <=8-byte store is
    # 0x9C..0xA3, always encoded as disp32 (> 0x7F). Back-decode 1..10 bytes; keep decodes that contain the disp.
    # (A first draft walked .pdata bodies and missed 16 of the 93: leaf functions have no .pdata entry.)
    stores, seen, excl = [], set(), set()
    for n_, v, vs, p, rs in T.TEXT:
        blob = T.raw[p:p + min(vs, rs)]
        for dsp in range(0x9C, 0xA4):
            pat = struct.pack("<i", dsp)
            k = blob.find(pat)
            while k >= 0:
                for back in range(10, 0, -1):   # longest decode first (a short one drops a prefix / REX byte)
                    if k - back < 0:
                        continue
                    ins = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                    if not ins:
                        continue
                    i = ins[0]
                    # a `mov [base+disp32], reg` ends exactly at the end of its displacement
                    if i.address + i.size != v + k + 4 or i.mnemonic != "mov" or len(i.operands) != 2:
                        continue
                    d, s = i.operands
                    if d.type != CS_OP_MEM or s.type != CS_OP_REG or d.mem.disp != dsp:
                        continue
                    m = d.mem
                    bn = i.reg_name(m.base) if m.base else None
                    if bn in (None, "rip", "rsp"):
                        continue
                    if bn == "rbp" or m.index:
                        if m.disp <= 0xA3 < m.disp + d.size:
                            excl.add((i.address, bn, "index" if m.index else "", d.size, i.op_str))
                        break
                    if m.disp <= 0xA3 < m.disp + d.size:
                        # the longest decode fixes the operands (REX); a redundant prefix byte in front would also
                        # decode to the same text, so take the SHORTEST decode with that same text as the address
                        for b2 in range(1, back + 1):
                            j = list(T.md.disasm(blob[k - b2:k - b2 + 15], v + k - b2, 1))
                            if j and j[0].address + j[0].size == v + k + 4 and (j[0].mnemonic, j[0].op_str) == (i.mnemonic, i.op_str):
                                i = j[0]
                                break
                        if i.address not in seen:
                            seen.add(i.address)
                            e = pdata_entry(i.address)
                            stores.append((IB + e[0] if e else 0, i.address, d.size, bn, m.disp, i.reg_name(s.reg)))
                    break
                k = blob.find(pat, k + 1)
    stores.sort(key=lambda x: x[1])
    pkg93 = set()
    for L in open(os.path.join(HERE, "..", "sd107-register-stores-0930", "sd107_register_stores.out"), encoding="utf-8"):
        mm = re.match(r"\s+S7 (open|copy|this)\s+([0-9A-F]{8}) ([0-9A-F]{8})", L)
        if mm:
            pkg93.add(int(mm.group(3), 16))
    pkg93.add(0x0024768D)
    mine = {x[1] for x in stores}
    print("== G. register-sourced mov stores covering +0xA3 (no index, base not rsp/rbp/rip), raw image-wide scan: %d" % len(stores))
    print("  by width:", dict(collections.Counter(x[2] for x in stores)))
    print("  package's 93 (S7 lines + 0024768D): %d; found by this sweep: %d; missing: %s" % (
        len(pkg93), len(pkg93 & mine), ["%08X" % x for x in sorted(pkg93 - mine)]))
    print("  outside the package's shape (rbp base or an index register), same coverage test: %d" % len(excl))
    fr = collections.Counter()
    for x in sorted(excl):
        e = pdata_entry(x[0])
        kind = "index" if x[2] else "no .pdata"
        if e and not x[2]:
            # chain to the root, then look for an rbp frame setup in its first 24 instructions
            r = e
            while True:
                uo = T.off(IB + r[2])
                if not (T.raw[uo] >> 3) & 4:
                    break
                cnt = T.raw[uo + 2]
                r = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)
            pro = T.dis(IB + r[0], IB + r[0] + 0x80)[:24]
            fp = any(i.mnemonic in ("lea", "mov") and i.op_str.startswith("rbp, ") and "rsp" in i.op_str for i in pro)
            kind = "rbp = frame (rsp-derived in prologue of %08X)" % (IB + r[0]) if fp else "rbp not rsp-derived in prologue of %08X" % (IB + r[0])
        fr[kind.split(" (")[0].split(" in ")[0]] += 1
        print("    %08X  %-32s %s" % (x[0], x[4], kind))
    print("  by kind:", dict(fr))
    json.dump([["%08X" % x for x in s[:2]] + list(s[2:]) for s in stores], open(os.path.join(HERE, "sd107o_stores.json"), "w"))

if "H" in part:
    print("== H1. same-field copies: load..store straight line")
    for ld, stv in [(0x0018A5BE, 0x0018A5C4), (0x001C24A7, 0x001C24AD), (0x005DED6E, 0x005DED74), (0x006928B0 + 0xFB, 0x006929B2),
                    (0x00747E9D, 0x00748155), (0x007222CC, 0x00722409)]:
        print("  load %08X -> store %08X" % (ld, stv))
        ins = T.dis(ld, stv + 8)
        L = ins[0]
        reg = L.operands[0].reg
        big = T.md.reg_name(reg)
        fam = {"esi": ("esi", "rsi", "si", "sil"), "r15d": ("r15d", "r15", "r15w", "r15b"),
               "eax": ("eax", "rax", "ax", "al", "ah"), "rax": ("eax", "rax", "ax", "al", "ah")}.get(big, (big,))
        wr = []
        for i in ins[1:]:
            if i.address >= stv:
                break
            try:
                _, w = i.regs_access()
            except Exception:
                w = []
            if any(T.md.reg_name(r) in fam for r in w):
                wr.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
        st = [i for i in ins if i.address == stv]
        print("    %08X %s %s | store decoded on this linear walk: %s | writes of %s between: %s" % (
            L.address, L.mnemonic, L.op_str, ("%s %s" % (st[0].mnemonic, st[0].op_str)) if st else "NOT ALIGNED", big, wr or "none"))
    print("== H2. polymorphic this: vtable slots holding the function, RTTI class")

    def col_name(vt_slot0):
        colp = struct.unpack("<Q", T.rd(vt_slot0 - 8, 8))[0]
        c = T.rd(colp, 24)
        if c is None or len(c) < 24:
            return None
        sig, ofs, cdo, tdr = struct.unpack_from("<IIII", c, 0)
        td = IB + tdr
        nm = T.rd(td + 16, 96).split(b"\0")[0]
        return nm.decode("latin1"), sig, ofs

    def vtables_of(fn):
        out = []
        for slot in T.data_refs(fn)["abs64"]:
            s = int(slot[:8], 16)
            # walk back to the vtable start: previous qword whose predecessor is a COL pointer (rdata)
            k = s
            for _ in range(200):
                prev = struct.unpack("<Q", T.rd(k - 8, 8))[0]
                cn = None
                try:
                    cn = col_name(k)
                except Exception:
                    cn = None
                if cn and cn[0].startswith(".?A"):
                    out.append((slot, k, (s - k) // 8, cn[0]))
                    break
                k -= 8
        return out

    def fstart(a):
        e = pdata_entry(a)
        while e:
            uo = T.off(IB + e[2])
            if not (T.raw[uo] >> 3) & 4:
                return IB + e[0]
            cnt = T.raw[uo + 2]
            e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)
        return None

    SEVEN = [(0x001A0960, 0x001A099A), (0x006566D0, 0x00656757), (0x00656F20, 0x00656FF3), (0x00657330, 0x0065738C),
             (0x006BAB40, 0x006BAC9E), (0x00864750, 0x00864786), (0x0087B850, 0x0087B940)]
    for fn, site in SEVEN:
        print("  %08X (store %08X):" % (fn, site))
        vt = vtables_of(fn)
        for v in vt[:2]:
            print("    in vtable: slot %s  vtable %08X  index %d  class %s" % v)
        if not vt:
            cs = T.rel32_callers(fn) + T.jcc_callers(fn)
            for c in cs:
                ca = int(c[:8], 16)
                cf = fstart(ca)
                print("    no vtable slot; caller %s in %08X:" % (c, cf))
                for v in vtables_of(cf)[:2]:
                    print("      caller in vtable: slot %s  vtable %08X  index %d  class %s" % v)
                pre = [i for i in T.dis(cf, ca + 5)]
                print("      caller entry: " + "; ".join("%s %s" % (i.mnemonic, i.op_str) for i in pre[:10]))
                print("      at call:      " + "; ".join("%s %s" % (i.mnemonic, i.op_str) for i in pre[-4:]))
        ins = T.dis(fn, fn + 0x40)
        print("    entry:", "; ".join("%s %s" % (i.mnemonic, i.op_str) for i in ins[:8]))
        for back in range(0x30, 0x8, -1):
            ii = T.dis(site - back, site + 8)
            if any(i.address == site for i in ii):
                for i in ii[-5:]:
                    print("      %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
                break
