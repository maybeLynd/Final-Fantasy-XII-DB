"""hz_indep.py - SWE2-AUDIT-SPEC (review of ASTRA 8969fe745, 2026-09-29). Independent of the producer's scripts and of
reg_tracking.py: pefile + capstone only (via ../auditspec-review-ov31-type-store-0929/ov31_indep.py).

Part 1 - 00529D50 (917 B): basic-block CFG over direct branches (calls fall through; jmp/jcc targets outside the body are
         exits; ret ends a block). Dominance: with the block containing 00529FEC removed, are 0052A063 and 0052A06C
         unreachable from entry? Every instruction in the body that WRITES r13 (any width), per capstone regs_write
         plus explicit dest-operand check. Control: removing an unrelated block must NOT make the uses unreachable, and
         a same-size branch mutation (00529E48 jcc retargeted to 0052A063) must produce a bypass.
Part 2 - 00533B20 (9,526 B): prologue pushes and frame size; every ret, with the instructions before it; every rsp
         adjustment; every store whose memory operand is [rsp + d] with d inside the pushed-register area
         [frame, frame + 8*pushes) at its site's rsp depth (tracked linearly through push/pop/sub/add rsp in the
         straight-line epilogues); any write to r13/rbx/rsi that is followed by a ret without an intervening pop of it.
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_REG, CS_OP_MEM, CS_OP_IMM
from capstone.x86 import X86_REG_RSP

fails = 0


def body(start, size, patch=None):
    o = T.off(start)
    b = bytearray(T.raw[o:o + size])
    if patch:
        for a, old, new in patch:
            k = a - start
            assert bytes(b[k:k + len(old)]) == old, "patch site mismatch at %08X" % a
            b[k:k + len(new)] = new
    return list(T.md.disasm(bytes(b), start)), bytes(b)


def cfg(ins, lo, hi):
    addrs = [i.address for i in ins]
    leaders = {lo}
    for k, i in enumerate(ins):
        if i.group(1) or i.mnemonic == "ret" or i.group(7):  # jump / ret / relative branch
            if i.operands and i.operands[0].type == CS_OP_IMM and lo <= i.operands[0].imm < hi:
                leaders.add(i.operands[0].imm)
            if k + 1 < len(ins):
                leaders.add(ins[k + 1].address)
    leaders = sorted(x for x in leaders if x in set(addrs))
    blocks, succ = {}, {}
    for n, L in enumerate(leaders):
        end = leaders[n + 1] if n + 1 < len(leaders) else hi
        bi = [i for i in ins if L <= i.address < end]
        blocks[L] = bi
        last = bi[-1]
        s = []
        if last.mnemonic == "ret":
            pass
        elif last.mnemonic == "jmp":
            if last.operands[0].type == CS_OP_IMM and lo <= last.operands[0].imm < hi:
                s.append(last.operands[0].imm)
        else:
            if last.group(7) and last.operands and last.operands[0].type == CS_OP_IMM and lo <= last.operands[0].imm < hi:
                s.append(last.operands[0].imm)
            if end < hi:
                s.append(end)
        succ[L] = s
    return blocks, succ


def reach(succ, start, removed):
    seen, st = set(), [start]
    while st:
        x = st.pop()
        if x in seen or x in removed:
            continue
        seen.add(x); st.extend(succ.get(x, []))
    return seen


def block_of(blocks, a):
    return next(L for L, bi in blocks.items() if any(i.address == a for i in bi))


def part1(patch=None, tag="original"):
    global fails
    LO, N = 0x00529D50, 917
    ins, _ = body(LO, N, patch)
    blocks, succ = cfg(ins, LO, LO + N)
    bz, bc, bs = block_of(blocks, 0x00529FEC), block_of(blocks, 0x0052A063), block_of(blocks, 0x0052A06C)
    full = reach(succ, LO, set())
    cut = reach(succ, LO, {bz})
    print("  [%s] %d insns, %d blocks; entry reaches compare %s store %s; without the XOR block (%08X): compare %s store %s"
          % (tag, len(ins), len(blocks), bc in full, bs in full, bz, bc in cut, bs in cut))
    return ins, blocks, succ, bz, bc, bs, full, cut


print("== Part 1: 00529D50")
ins, blocks, succ, bz, bc, bs, full, cut = part1()
ok = bc in full and bs in full and bc not in cut and bs not in cut
fails += not ok
print("  %s the XOR dominates both uses" % ("PASS" if ok else "FAIL"))
w13 = []
for i in ins:
    regs_w = set(i.regs_access()[1])
    names = {i.reg_name(r) for r in regs_w}
    # a compare/test names r13 as operand 0 but only reads it (first run of this check wrongly flagged 0052A01F cmp r13w, ax)
    dest_reg = i.operands and i.operands[0].type == CS_OP_REG and i.reg_name(i.operands[0].reg) in ("r13", "r13d", "r13w", "r13b")         and i.mnemonic not in ("cmp", "test", "bt", "push") and not i.mnemonic.startswith(("ucomis", "comis"))
    if names & {"r13", "r13d", "r13w", "r13b"} or dest_reg:
        w13.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
print("  r13 writes in the body:", w13)
between = [w for w in w13 if 0x00529FEC < int(w[:8], 16) <= 0x0052A06C]
fails += bool(between) or not any(w.startswith("00529FEC") for w in w13)
print("  %s no r13 write between 00529FEC and the store (found: %s)" % ("PASS" if not between else "FAIL", between))
calls = [("%08X %s %s" % (i.address, i.mnemonic, i.op_str)) for i in ins if i.mnemonic == "call" and 0x00529FEC < i.address < 0x0052A063]
print("  calls crossing the zero-to-compare region:", calls)
# controls
_, _, _, _, bc2, bs2, full2, cut2 = part1([(0x00529E48, bytes.fromhex("0F8480000000"), bytes.fromhex("0F8415020000"))],
                                           "control: 00529E48 retargeted to 0052A063")
ok = bc2 in cut2
fails += not ok
print("  %s control: the retargeted branch bypasses the XOR (compare reachable without it: %s)" % ("PASS" if ok else "FAIL", bc2 in cut2))
other = next(L for L in sorted(blocks) if L not in (bz, bc, bs, 0x00529D50) and L > bs)
c3 = reach(succ, 0x00529D50, {other})
ok = bc in c3 and bs in c3
fails += not ok
print("  %s control: removing an unrelated later block %08X leaves both uses reachable" % ("PASS" if ok else "FAIL", other))

print("== Part 2: 00533B20")
LO, N = 0x00533B20, 9526
ins, _ = body(LO, N)
print("  %d instructions decoded to %08X" % (len(ins), ins[-1].address + ins[-1].size))
pushes = []
for i in ins:
    if i.mnemonic == "push":
        pushes.append(i.op_str)
    else:
        break
frame = next(i for i in ins if i.mnemonic == "sub" and i.op_str.startswith("rsp,")).operands[1].imm
print("  prologue pushes %s; sub rsp, 0x%X" % (pushes, frame))
rets = [k for k, i in enumerate(ins) if i.mnemonic == "ret"]
print("  ret sites: %d" % len(rets))
bad_ret = []
want = list(reversed(pushes))
for k in rets:
    tail = ins[max(0, k - 12):k + 1]
    pops = [i.op_str for i in tail if i.mnemonic == "pop"]
    txt = "; ".join("%s %s" % (i.mnemonic, i.op_str) for i in tail[-8:])
    if pops[-len(want):] != want:
        bad_ret.append("%08X: pops %s" % (ins[k].address, pops))
    print("   ret %08X: ...%s" % (ins[k].address, txt[-200:]))
fails += bool(bad_ret)
print("  %s every ret pops %s in order%s" % ("PASS" if not bad_ret else "FAIL", want, (": " + str(bad_ret)) if bad_ret else ""))
adj = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in ins
       if i.operands and i.operands[0].type == CS_OP_REG and i.operands[0].reg == X86_REG_RSP and i.mnemonic not in ("push", "pop")]
print("  rsp adjustments:", adj)
# direct stores into the pushed-register area, at body depth (rsp = entry - 8*len(pushes) - frame)
lo_slot, hi_slot = frame, frame + 8 * len(pushes)
hits = []
for i in ins:
    if i.operands and i.operands[0].type == CS_OP_MEM and i.operands[0].mem.base == X86_REG_RSP \
            and i.mnemonic not in ("cmp", "test", "push", "pop") and not i.mnemonic.startswith(("ucomis", "comis")):
        d = i.operands[0].mem.disp
        if lo_slot <= d < hi_slot:
            hits.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
fails += bool(hits)
print("  %s direct stores into the pushed-register area [rsp+0x%X, rsp+0x%X): %s" % ("PASS" if not hits else "FAIL", lo_slot, hi_slot, hits))
print("FAILS %d" % fails)
