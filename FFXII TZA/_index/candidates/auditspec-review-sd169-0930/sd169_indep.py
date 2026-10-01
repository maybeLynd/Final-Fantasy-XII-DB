"""sd169_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SD-169 (draw-surface cells 022D8EAC / 022D8EB0).
Uses ../auditspec-review-sd141-0930/sdx.py (pefile + capstone + numpy, certified image; not retool.py).

  A  every .text operand starting in [022D8EB0 - 0x40, 022D8EB4) in every form, with coverage of +0xA0 (022D8EB0).
  B  every rip lea with target in [022D8E10 - 0x100, 022D8EB4) (a base that could reach +0xA0), tracked with
     sdx.track(): accesses through it, hand-ons (followed one level with track_entry) - any access landing on 022D8EB0.
  C  relocations / raw values into [022D8E10 - 0x100, 022D8EB4).
  D  0036D2F0 after the call to 0016D6A0: is r8 (the +0xA0 value) read before it is written? 0016D6A0's bytes and
     its caller count (E8/E9 + jcc).
  E  00244200's packet: every qword store into the packet with its value source, decoded from the bytes; the GIF tag.
  Controls: K1 the +0x9C cell 022D8EAC must show 00244200's read (00244224) and 0036D2F0's (0036D31B); K2 the
  image-base-relative 0036E414 (SD-121) is found by the same window call.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd141-0930"))
import sdx  # noqa: E402

CELL = 0x022D8EB0
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


print("== A. operands starting in [%08X, %08X)" % (CELL - 0x40, CELL + 4))
A = sdx.window(CELL, CELL + 4, 0x40)
for h in A:
    print("  " + sdx.fmt(h), " root %08X" % (sdx.root(h["addr"]) or 0))
cov = [h for h in A if h["covers"]]
print("  covering 022D8EB0: %s" % ["%08X %s %s w%d" % (h["addr"], h["form"], h["mn"], h["width"]) for h in cov])

print("== B. leas of addresses in [%08X, %08X)" % (0x022D8E10 - 0x100, CELL + 4))
B = sdx.rip_leas(0x022D8E10 - 0x100, CELL + 4)
bhits = []
for s, r, t in sorted(B):
    tgt, acc, calls, st = sdx.track(s)
    on = [x for x in acc if not x[5] and x[2] <= CELL < x[2] + max(x[3], 1)]
    print("  %08X lea %s -> %08X (cell - 0x%X) root %08X: accesses %d, hand-ons %d, stores %d%s" % (
        s, r, t, CELL - t, sdx.root(s) or 0, len(acc), len(calls), len(st), "  ON-CELL" if on else ""))
    bhits += on
    for c in calls:
        print("      hand-on %08X %s %s" % c)
        if c[1].startswith("0x"):
            for reg, base in c[2].items():
                t2, acc2, calls2, st2 = sdx.track_entry(int(c[1], 16), reg, int(base, 16))
                on2 = [x for x in acc2 if not x[5] and x[2] <= CELL < x[2] + max(x[3], 1)]
                mx = max([x[2] + max(x[3], 1) - int(base, 16) for x in acc2 if not x[5]] or [0])
                print("        callee %s %s=%s: accesses %d, max extent +0x%X, further hand-ons %d%s" % (
                    c[1], reg, base, len(acc2), mx, len(calls2), "  ON-CELL" if on2 else ""))
                bhits += on2
print("  %d leas" % len(B))

print("== C. stored pointers")
C1 = sdx.relocs_into(0x022D8E10 - 0x100, CELL + 4)
C2 = [r for r in sdx.data_refs(0x022D8E10 - 0x100, CELL + 4) if r[3] != ".text"]
print("  relocations %d %s; raw values outside .text %d %s" % (len(C1), ["%08X->%08X" % x for x in C1], len(C2),
                                                              ["%s@%08X=%08X" % r[:3] for r in C2[:10]]))

print("== D. 0036D2F0 after the stub call; the stub")
o = sdx.off(0x0036D34E)
r8use = None
for i in sdx.md.disasm(sdx.raw[o:o + 0x200], 0x0036D34E):
    if i.address == 0x0036D34E:
        continue
    rd_, wr_ = i.regs_access()
    names_r = {sdx._full(i, r) for r in rd_}
    names_w = {sdx._full(i, r) for r in wr_}
    if "r8" in names_r:
        r8use = ("read", i.address, "%s %s" % (i.mnemonic, i.op_str))
        break
    if "r8" in names_w or i.mnemonic in ("call", "ret"):
        r8use = ("written/call", i.address, "%s %s" % (i.mnemonic, i.op_str))
        break
print("  first r8 event after 0036D34E: %s" % (r8use,))
stub = sdx.rd(0x0016D6A0, 4)
nstub = len(sdx.rel32(0x0016D6A0)) + len(sdx.jcc(0x0016D6A0))
print("  0016D6A0 bytes %s = `%s`; raw callers (E8/E9 + jcc) %d" % (stub.hex(), sdx.txt(0x0016D6A0), nstub))

print("== E. 00244200 packet stores")
e = sdx.pdata_of(0x00244200)
o = sdx.off(0x00244200)
for i in sdx.md.disasm(sdx.raw[o:o + (e[1] - e[0])], 0x00244200):
    s = "%s %s" % (i.mnemonic, i.op_str)
    keep = i.mnemonic in ("movabs", "sar", "shl", "or", "imul", "shr", "and") or "0x2094" in i.op_str or \
        (i.mnemonic == "mov" and "qword ptr [r" in i.op_str and i.op_str.split(",")[0].startswith("qword ptr [r")) or \
        (i.mnemonic == "call")
    if keep:
        extra = ""
        for m, sz in sdx.mem_ops(i):
            if m.base == sdx.X86_REG_RIP:
                extra = "   ; -> %08X" % (i.address + i.size + m.disp)
        print("  %08X %s%s" % (i.address, s, extra))
tag = 0x1000000000008007
print("  GIF tag 0x%016X: NLOOP %d EOP %d PRE %d FLG %d NREG %d REGS 0x%X" % (
    tag, tag & 0x7FFF, (tag >> 15) & 1, (tag >> 46) & 1, (tag >> 58) & 3, (tag >> 60) & 0xF, 0))

print("== controls")
k1 = sdx.window(0x022D8EAC, 0x022D8EB0, 0)
check("K1", {0x00244224, 0x0036D31B} <= {h["addr"] for h in k1}, "+0x9C readers 00244224 / 0036D31B found: %s" % (
    ["%08X %s" % (h["addr"], h["mn"]) for h in k1]))
check("K2", any(h["addr"] == 0x0036E414 for h in sdx.window(0x022D97B0, 0x022D97B4, 0)), "image-base-relative control")
check("V1", sorted((h["addr"], h["mn"], h["width"]) for h in cov) == [
    (0x00244224, "mov", 8), (0x002443E7, "mov", 8), (0x0036D2A3, "mov", 4), (0x0036D342, "movzx", 2), (0x004FDDC7, "mov", 8)],
      "022D8EB0 is covered by the boot store 0036D2A3, the word read 0036D342 AND three qword loads of +0x9C "
      "(00244224, 002443E7, 004FDDC7) that carry +0xA0 in their high half - see sd169_qword.out")
check("V2", not bhits and not C1, "no lea'd base or stored pointer reaches 022D8EB0")
check("V3", stub[:3] == b"\xc2\x00\x00" and r8use and r8use[0] != "read", "0016D6A0 is `ret 0`; r8 is not read after the call")
print("FAILS %d" % fails)
