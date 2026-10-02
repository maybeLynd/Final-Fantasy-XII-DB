"""item4_malloc_forwarder.py - does any caller of 00210EC0 pass, or rely on, a second argument? (FABLE, 2026-10-02)
Static, read-only.

Question (memory page, "Interior citations - three allocation hubs"): "00210EC0's caller-visible contract beyond
malloc(n) - whether a caller relies on the dead-arg form is not established."

Method
  F1  the body: 00210EC0 must be `or r8d, -1 / xor edx, edx / jmp 0085E730` and 0085E730 must reach the `malloc`
      import (PE import directory). The body overwrites edx and r8d before the tail jump, so a value a caller leaves
      there cannot reach malloc; F2-F4 ask whether callers nevertheless SET those registers for the call.
  F2  every raw E8/E9/jcc site whose target is 00210EC0 (byte scan of .text, decode-aligned in the owner), plus
      rip-relative operands, absolute qwords and RVA dwords equal to it (a pointer route).
  F3  at each aligned site: the last instruction in the same basic block (stop at a jump target, a call, a jmp, a
      ret) that writes rdx/edx/dx/dl or r8/r8d/r8w/r8b, using capstone's register write lists. A write there is an
      argument the caller prepares for the call; none means the register is whatever the block left in it.
  F4  after each `call` site: whether rdx/r8 is READ before it is written again in the same block - a caller that
      expected the forwarder's edx = 0 / r8d = -1 to survive would read them; malloc may clobber both (volatile).

Controls
  C1  F2 must find 0017D029 (in 0017D000), a caller listed in the edge table, and the count is compared with the page's
      "81 frontier callers".
  C2  sensitivity of F3: run on the sibling 0017D260 (`allocate(n, align)`: or r9d, -1 / xor r8d, r8d / jmp to the
      _aligned_malloc thunk), whose callers DO pass a second argument in edx. F3 must find edx prepared at most of
      its sites; if it found none there, a zero on 00210EC0 would mean nothing.
"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mp_lib import *
from capstone.x86 import X86_REG_RDX, X86_REG_EDX, X86_REG_DX, X86_REG_DL, X86_REG_DH, X86_REG_R8, X86_REG_R8D, X86_REG_R8W, X86_REG_R8B

FWD, SIB = 0x210EC0, 0x17D260
RDX = {X86_REG_RDX, X86_REG_EDX, X86_REG_DX, X86_REG_DL, X86_REG_DH}
R8 = {X86_REG_R8, X86_REG_R8D, X86_REG_R8W, X86_REG_R8B}
fails = []


def block_targets(ins):
    t = set()
    for x in ins:
        if (x.mnemonic.startswith("j") or x.mnemonic == "call") and x.op_str.startswith("0x"):
            t.add(int(x.op_str, 16))
    return t


def regs_w(x):
    try:
        return set(x.regs_access()[1])
    except Exception:
        return set()


def regs_r(x):
    try:
        return set(x.regs_access()[0])
    except Exception:
        return set()


def census(target, label, p):
    idx = raw_index([target])[target]
    rows = []
    for site, form, o, al in sorted(idx):
        if not al:
            p("  (byte coincidence at %08X, not an instruction)" % site); continue
        ins = decode(o)
        jt = block_targets(ins)
        k = [i for i, x in enumerate(ins) if x.address == site][0]
        prep = {"rdx": None, "r8": None}
        for j in range(k - 1, -1, -1):
            y = ins[j]
            if y.mnemonic == "call" or y.mnemonic == "ret" or (y.mnemonic.startswith("j")):
                break
            w = regs_w(y)
            if prep["rdx"] is None and w & RDX:
                # a one-operand mul/imul/div/idiv or cdq/cqo writes rdx as the high half - not an argument
                side = y.mnemonic in ("mul", "div", "idiv", "cdq", "cqo") or (y.mnemonic == "imul" and "," not in y.op_str)
                prep["rdx"] = ("SIDE-EFFECT " if side else "") + "%08X %s %s" % (y.address, y.mnemonic, y.op_str)
            if prep["r8"] is None and w & R8:
                prep["r8"] = "%08X %s %s" % (y.address, y.mnemonic, y.op_str)
            if y.address in jt:
                break
        after = ""
        if form == "call":
            live = {"rdx": RDX, "r8": R8}
            for j in range(k + 1, len(ins)):
                y = ins[j]
                if y.address in jt or y.mnemonic in ("call", "ret") or y.mnemonic.startswith("j") or not live:
                    break
                r, w = regs_r(y), regs_w(y)
                selfxor = y.mnemonic == "xor" and len(set(y.op_str.replace(" ", "").split(","))) == 1
                if not selfxor and any(r & fam for fam in live.values()):
                    after = "%08X %s %s" % (y.address, y.mnemonic, y.op_str); break
                for nm in [n for n, fam in live.items() if w & fam]:
                    del live[nm]
        rows.append((site, form, o, prep["rdx"], prep["r8"], after))
    return rows


def main():
    out = []
    p = out.append
    p("# item 4 - 00210EC0's callers and the second argument (static). run: item4_malloc_forwarder.py at %s" % head_sha())
    body = decode(FWD)
    p("\n## F1 body of 00210EC0 (%d bytes): %s" % (funcs[FWD], " | ".join(x.mnemonic + " " + x.op_str for x in body)))
    if [x.mnemonic + " " + x.op_str for x in body][:3] != ["or r8d, 0xffffffff", "xor edx, edx", "jmp 0x85e730"]:
        fails.append("F1 body differs")
    th = list(md.disasm(d[off(0x85E730):off(0x85E730) + 7], 0x85E730))[0]
    p("  thunk 0085E730: %s %s -> IAT slot %08X (item1's import walk resolves it to malloc)" % (th.mnemonic, th.op_str, rip_target(th, th.operands[0])))
    # pointer routes
    qh = len(re.findall(re.escape(struct.pack("<Q", FWD)), d)); rh = len(re.findall(re.escape(struct.pack("<I", FWD - BASE)), d))
    rip = 0
    for fn in all_functions():
        for x in decode(fn):
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and rip_target(x, op) == FWD:
                    rip += 1   # includes `lea reg, [rip+X]` (an address taken)
                    p("  rip-relative operand on 00210EC0: %08X in %08X %s: %s %s" % (x.address, fn, names.get(fn, ""), x.mnemonic, x.op_str))
    p("  pointer routes: absolute qwords %d, RVA dwords %d, rip-relative operands %d" % (qh, rh, rip))
    # census
    p("\n## F2-F4 census of 00210EC0")
    rows = census(FWD, "fwd", p)
    calls = sum(1 for r in rows if r[1] == "call"); jmps = sum(1 for r in rows if r[1] != "call")
    owners = {r[2] for r in rows}
    p("  aligned sites: %d (call %d, tail/other jump %d) in %d functions" % (len(rows), calls, jmps, len(owners)))
    if not any(r[0] == 0x17D029 for r in rows):
        fails.append("C1 0017D029 not found")
    nrdx = [r for r in rows if r[3]]; nr8 = [r for r in rows if r[4]]; aft = [r for r in rows if r[5]]
    p("  sites whose block prepares rdx before the transfer: %d; r8: %d; sites that read rdx/r8 after the call before"
      " rewriting: %d" % (len(nrdx), len(nr8), len(aft)))
    for site, form, o, rdx, r8, after in rows:
        p("  %-5s %08X in %08X %-40s rdx<- %s | r8<- %s%s" % (form, site, o, names.get(o, "")[:40], rdx or "-", r8 or "-",
          (" | READ AFTER: " + after) if after else ""))
    # F5 the address-taken route found by F2
    p("\n## F5 the address-taken route: 00210760 hands {00210EC0, free forwarder 00210EB0} to a library init")
    for x in decode(0x210760):
        if 0x21082A <= x.address <= 0x210889:
            p("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
    r = raw_index([0x7A4D50, 0x7AD620])
    for t in (0x7A4D50, 0x7AD620):
        p("  raw sites of %08X: %s" % (t, ", ".join("%s %08X in %08X" % (f, s, o) for s, f, o, al in r[t] if al)))
    for x in decode(0x7A4D50):
        if 0x7A4E20 <= x.address <= 0x7A4E39:
            p("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
    p("  " + " | ".join("%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in decode(0x7AD620)))
    CELL = 0x2EAD0B0
    for fn in all_functions():
        ins = decode(fn)
        for k, x in enumerate(ins):
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and rip_target(x, op) == CELL:
                    kind = "WRITE" if op.access & CS_AC_WRITE else "read"
                    p("  cell 02EAD0B0 %s at %08X in %08X: %s %s" % (kind, x.address, fn, x.mnemonic, x.op_str))
                    if x.mnemonic == "call":
                        win = ins[max(0, k - 4):k + 3]
                        p("      window: " + " | ".join("%s %s" % (y.mnemonic, y.op_str) for y in win))
                        # does anything read rdx/r8 after the indirect call before rewriting them?
                        live = {"rdx": RDX, "r8": R8}; after = "-"
                        for y in ins[k + 1:]:
                            if y.mnemonic in ("call", "ret") or y.mnemonic.startswith("j") or not live:
                                break
                            rr, ww = regs_r(y), regs_w(y)
                            sx = y.mnemonic == "xor" and len(set(y.op_str.replace(" ", "").split(","))) == 1
                            if not sx and any(rr & fam for fam in live.values()):
                                after = "%08X %s %s" % (y.address, y.mnemonic, y.op_str); break
                            for nm in [n for n, fam in live.items() if ww & fam]:
                                del live[nm]
                        p("      rdx/r8 read after the call before rewrite: %s" % after)
    # C2 sensitivity
    p("\n## C2 sensitivity: the same census on the two-argument sibling 0017D260")
    p("  body: %s" % " | ".join(x.mnemonic + " " + x.op_str for x in decode(SIB)))
    srows = census(SIB, "sib", p)
    s_rdx = sum(1 for r in srows if r[3])
    p("  aligned sites: %d; sites whose block prepares rdx: %d" % (len(srows), s_rdx))
    if not srows or s_rdx < len(srows) // 2:
        fails.append("C2 detector insensitive")
    p("\nFAILS %d %s" % (len(fails), fails))
    open(os.path.join(HERE, "item4_malloc_forwarder.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


main()
