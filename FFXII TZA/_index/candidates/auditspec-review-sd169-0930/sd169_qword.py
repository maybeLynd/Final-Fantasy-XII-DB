"""sd169_qword.py - SWE2-AUDIT-SPEC (SD-169 review, 2026-09-30). The three QWORD loads of 022D8EAC that also load
+0xA0 (022D8EB0) in their high half (found by sd169_indep.py A, confirmed by linear decode from the function start):
00244224 (rcx, 00244200), 002443E7 (r10, 002443D0), 004FDDC7 (rsi, 004FDDA0). For each, a linear walk from the load
prints every instruction that touches the loaded register (any width) until a full 64-bit overwrite or a ret, marking
64-bit uses (the only ones that can carry the high half) - shifts, 64-bit stores/moves, argument registers at a call.
Linear, not flow-aware: a candidate list read by hand in the record.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd141-0930"))
import sdx  # noqa: E402

ALIAS = {"rcx": ("rcx", "ecx", "cx", "cl"), "r10": ("r10", "r10d", "r10w", "r10b"), "rsi": ("rsi", "esi", "si", "sil"),
         "rbp": ("rbp", "ebp", "bp", "bpl")}


def walk(site, reg, n=400):
    o = sdx.off(site)
    e = sdx.pdata_of(site)
    end = sdx.IB + e[1]
    names = ALIAS[reg]
    live = {reg}
    first = True
    for i in sdx.md.disasm(sdx.raw[o:o + (end - site)], site):
        if first:
            print("  %08X %s %s   <- load" % (i.address, i.mnemonic, i.op_str))
            first = False
            continue
        rd_, wr_ = i.regs_access()
        rdn = {i.reg_name(r) for r in rd_}
        wrn = {i.reg_name(r) for r in wr_}
        t = "%s %s" % (i.mnemonic, i.op_str)
        touches = any(x in rdn or x in wrn for x in names)
        if i.mnemonic == "call":
            print("  %08X %s   (call: %s in an argument register? %s)" % (i.address, t, reg, reg in ("rcx", "rdx", "r8", "r9")))
            if reg in ("rcx", "rdx", "r8", "r9", "rax", "r10", "r11"):
                print("     volatile %s dies at the call" % reg)
                return
            continue
        if touches:
            full_r = reg in rdn
            full_w = reg in wrn
            # a 32-bit write zero-extends: it also kills the high half
            k32 = names[1] in wrn
            tag = "64-bit READ" if full_r else ""
            print("  %08X %-50s %s%s" % (i.address, t, tag, "  (overwritten)" if (full_w and not full_r) or k32 else ""))
            if (full_w and not full_r and i.mnemonic in ("mov", "lea", "movsxd", "movzx", "pop", "xor")) or \
                    (k32 and not full_r):
                return
            if i.mnemonic == "mov" and (full_w or k32) and not full_r:
                return
        if i.mnemonic == "ret":
            print("  %08X ret" % i.address)
            return
        n -= 1
        if n <= 0:
            print("  (walk limit)")
            return


for site, reg in ((0x00244224, "rcx"), (0x002443E7, "r10"), (0x004FDDC7, "rsi"), (0x004FDDCE, "rbp")):
    print("== %08X %s (root %08X)" % (site, reg, sdx.root(site) or 0))
    walk(site, reg)
