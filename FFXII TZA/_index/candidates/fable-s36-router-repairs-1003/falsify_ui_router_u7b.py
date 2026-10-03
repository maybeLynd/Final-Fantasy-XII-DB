"""falsify_ui_router_u7b.py - FABLE, 2026-10-03: U7 re-done against BOTH clauses of R-5, at the bytes.

The pass-1 falsifier (Tools/analysis-kit/gfz-scripts/falsify_ui_router.py, U7) tested R-5's single drain call site only,
so it reported "survives" while R-5's guard text said bit 7 and "deferred" (SWE2-AUDIT-SEM S-36 point 7). This file does
not replace it; it adds the two clauses that U7 never read.

  T0  the drain 002E09A0 has exactly one caller, 0031427D, by a raw .text index (E8/E9 rel32, 0F 8x rel32, EB/7x rel8).
  T1  CLAUSE 1, the guard bit. In the drain's record loop (r15 = lea 0215F200, index*0x68, 8 records) the guard byte is
      `movzx eax, byte [rdx+r15+0x3E]`, then `shl al, N`, `sar al, M`, `or al, byte [rdx+r15+0x38]`, `jne`. The set of
      +0x3E bits the shift pair keeps is COMPUTED from N and M by evaluating all 256 byte values, and compared with the
      contract's reading: bit 0.
  T2  the guard DEFERS: the jne target sets ecx = esi (1) and jumps back to the word test, whose `or eax, ecx; jne`
      skips the dispatch to the tail store of the blocked byte; no store to the pending byte 0215F1A0 lies on that path.
  T3  CLAUSE 2, the not-ready discard. After `xor ecx, ecx; call 00267360` the non-zero arm (fall-through of `je`) runs
      `xor r8b, r8b`, three zero stores of ebp to 0215F1A4 (u32), 0215F1A8 (u32) and 0215F1A1 (u8), then an
      unconditional jmp whose target stores r8b to the pending byte 0215F1A0. ebp is 0: set by `xor ebp, ebp` in the
      prologue and written by nothing else in the body. Then the dispatch test `test r8b, r8b; je` skips the router
      call 00254B50, with no write to r8 and no call between the pending store and that test.
      Outcome computed: "discarded" when the pending byte stored is 0 and the id/parameter are zeroed; "deferred"
      when the pending byte is left set.

Sensitivity (each must FAIL, or this file counts a FAIL):
  S1  the mutated reading "bit 7" against T1's computed set;
  S2  the mutated reading "deferred" against T3's computed outcome;
  S3  a mutated IMAGE: `shl al, 7` patched to `shl al, 6` - T1's claim "bit 0" must then fail;
  S4  a mutated IMAGE: the `xor r8b, r8b` of the discard arm patched to three NOPs - T3's claim "discarded" must then
      fail (the stored pending value is no longer provably 0).

Prints FAILS N last; exit 1 when N > 0.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP  # noqa: E402

DRAIN, DRAIN_END = 0x002E09A0, 0x002E0D8A          # .pdata 002E09A0..002E0D8A (1,002 B)
READY, ROUTER = 0x00267360, 0x00254B50
PENDING, BLOCKED, ID, PARAM, RECS = 0x0215F1A0, 0x0215F1A1, 0x0215F1A4, 0x0215F1A8, 0x0215F200
fails = 0


def report(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))


def body(img):
    img.cs.detail = True
    return list(img.cs.disasm(img.read(DRAIN, DRAIN_END - DRAIN), DRAIN))


def rip(x):
    return [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]


def imm(x, k=0):
    o = x.operands[k] if len(x.operands) > k else None
    return o.imm if o is not None and o.type == X86_OP_IMM else None


def S(x):
    return ("%s %s" % (x.mnemonic, x.op_str)).strip()


def writes(x, names):
    try:
        _r, w = x.regs_access()
    except Exception:
        return False
    return any(x.reg_name(r) in names for r in w)


R8 = ("r8", "r8d", "r8w", "r8b")
RBP = ("rbp", "ebp", "bp", "bpl")


def kept_bits(n, m):
    """+0x3E bits b for which ((b << n) as i8 >> m) != 0, over all 256 byte values, per bit."""
    out = set()
    for bit in range(8):
        v = (1 << bit) & 0xFF
        s = (v << n) & 0xFF
        s = s - 256 if s & 0x80 else s
        if (s >> m) & 0xFF:
            out.add(bit)
    return out


def t1_guard(ins):
    """Return (kept_bit_set, info, jne_target) or (None, why, None)."""
    lea_r15 = any(x.mnemonic == "lea" and x.op_str.startswith("r15,") and rip(x) == [RECS] for x in ins)
    for i, x in enumerate(ins):
        if x.mnemonic == "movzx" and "byte ptr [rdx + r15 + 0x3e]" in x.op_str and i + 4 < len(ins):
            a, b, c, d = ins[i + 1:i + 5]
            if a.mnemonic == "shl" and b.mnemonic == "sar" and c.mnemonic == "or" and "[rdx + r15 + 0x38]" in c.op_str \
                    and d.mnemonic == "jne" and lea_r15:
                n, m = imm(a, 1), imm(b, 1)
                return kept_bits(n, m), "%08X %s / %s / %s / %s / %s" % (x.address, S(x), S(a), S(b), S(c), S(d)), imm(d)
            return None, "guard shape not found after %08X" % x.address, None
    return None, "no movzx of +0x3E in the drain", None


def t2_defers(ins, tgt):
    by = {x.address: x for x in ins}
    x = by.get(tgt)
    if not x or S(x) != "mov ecx, esi":
        return False, "jne target %s is not `mov ecx, esi`" % (tgt and "%08X" % tgt)
    j = ins[ins.index(x) + 1]
    if j.mnemonic != "jmp":
        return False, "no jmp after the guard arm"
    back = imm(j)
    # from back: mov eax,[02092730]; test; je; cmp 5; mov eax, esi; jne; mov eax, ebp; or eax, ecx; jne SKIP
    seq = [y for y in ins if back <= y.address]
    k = next((y for y in seq if S(y) == "or eax, ecx"), None)
    if not k:
        return False, "no `or eax, ecx` after %08X" % back
    jn = ins[ins.index(k) + 1]
    skip = imm(jn) if jn.mnemonic == "jne" else None
    router_call = next((y.address for y in ins if y.mnemonic == "call" and imm(y) == ROUTER), None)
    pend_st = [y.address for y in ins if back <= y.address < (skip or 0) and PENDING in rip(y)
               and y.operands[0].type == X86_OP_MEM]
    tail = by.get(skip)
    ok = bool(skip and router_call and skip > router_call and tail and BLOCKED in rip(tail) and not
              [a for a in pend_st if a < k.address])
    return ok, "guard arm %08X `mov ecx, esi` -> jmp %08X -> %08X `or eax, ecx` / %s -> %s; router call %s; pending " \
               "stores between: %s" % (tgt, back, k.address, S(jn), tail and "%08X %s" % (skip, S(tail)),
                                        router_call and "%08X" % router_call,
                                        ["%08X" % a for a in pend_st if a < k.address] or "none")


def t3_discard(ins):
    """Return (outcome, info) where outcome is 'discarded', 'deferred' or None (not provable)."""
    by = {x.address: x for x in ins}
    # ebp == 0: one `xor ebp, ebp` and no other writer of rbp before the epilogue restore
    xb = [x for x in ins if S(x) == "xor ebp, ebp"]
    other = [x.address for x in ins if writes(x, RBP) and S(x) != "xor ebp, ebp"
             and not S(x).startswith("mov rbp, qword ptr [rsp")]
    ebp0 = len(xb) == 1 and not other
    c = next((x for x in ins if x.mnemonic == "call" and imm(x) == READY), None)
    if not c:
        return None, "no call to 00267360"
    i = ins.index(c)
    pre, t, je = ins[i - 1], ins[i + 1], ins[i + 2]
    if S(pre) != "xor ecx, ecx" or S(t) != "test eax, eax" or je.mnemonic != "je":
        return None, "slot-0 test shape differs at %08X" % c.address
    # the non-zero arm: fall-through of je, up to an unconditional jmp
    arm, r8val, stores = [], "unknown", {}
    for y in ins[i + 3:]:
        arm.append(y)
        if S(y) == "xor r8b, r8b":
            r8val = 0
        elif writes(y, R8):
            r8val = "unknown"
        if y.operands and y.operands[0].type == X86_OP_MEM and rip(y):
            src = y.operands[1]
            val = 0 if (src.type == X86_OP_REG and y.reg_name(src.reg) in RBP and ebp0) else (
                imm(y, 1) if src.type == X86_OP_IMM else "reg")
            stores[rip(y)[0]] = (y.operands[0].size, val, y.address)
        if y.mnemonic == "jmp":
            break
    jt = imm(arm[-1])
    st = by.get(jt)
    if not st or rip(st) != [PENDING] or not (st.operands[1].type == X86_OP_REG and st.reg_name(st.operands[1].reg) == "r8b"):
        return None, "jmp target %s is not the pending-byte store of r8b" % (jt and "%08X" % jt)
    pend_val = r8val
    # from the store to the dispatch test: no r8 write, no call
    j = ins.index(st)
    test = next((y for y in ins[j + 1:] if S(y) == "test r8b, r8b"), None)
    between = ins[j + 1:ins.index(test)] if test else []
    clob = [y.address for y in between if writes(y, R8) or y.mnemonic == "call"]
    nxt = ins[ins.index(test) + 1] if test else None
    router_call = next((y.address for y in ins if y.mnemonic == "call" and imm(y) == ROUTER), None)
    skips = bool(test and nxt.mnemonic == "je" and router_call and imm(nxt) > router_call and not clob)
    zeroed = stores.get(ID) == (4, 0, stores.get(ID, (0, 0, 0))[2]) and stores.get(PARAM) == (4, 0, stores.get(PARAM, (0, 0, 0))[2]) \
        and stores.get(BLOCKED) == (1, 0, stores.get(BLOCKED, (0, 0, 0))[2])
    info = "slot-0 call %08X, arm %s; ebp==0 %s; stores %s; jmp %08X -> %08X %s with r8b=%s; dispatch test %s %s skips " \
           "router %s: %s; clobbers between %s" % (
               c.address, "%08X..%08X" % (arm[0].address, arm[-1].address), ebp0,
               {("%08X" % k): ("w%d=%s @%08X" % v) for k, v in sorted(stores.items())}, arm[-1].address, jt, S(st),
               pend_val, test and "%08X" % test.address, nxt and S(nxt), router_call and "%08X" % router_call, skips,
               ["%08X" % a for a in clob] or "none")
    if pend_val == 0 and zeroed and skips:
        return "discarded", info
    if pend_val == "unknown":
        return None, info
    return "deferred", info


def raw_callers(img, target):
    ts = next(s for s in img.secs if s[0] == ".text")
    tlo = img.base + ts[1]
    a = np.frombuffer(img.d[ts[3]:ts[3] + ts[4]], dtype=np.uint8).astype(np.int64)
    n = len(a)
    pos = np.arange(n, dtype=np.int64) + tlo
    d = np.zeros(n, dtype=np.int64)
    m = n - 4
    d[:m] = a[1:m + 1] | (a[2:m + 2] << 8) | (a[3:m + 3] << 16) | (a[4:m + 4] << 24)
    d = np.where(d >= 2 ** 31, d - 2 ** 32, d)
    out = []
    for p in np.nonzero(((a == 0xE8) | (a == 0xE9)) & (pos + 5 + d == target))[0]:
        out.append(("%08X" % int(pos[p]), "E8" if a[p] == 0xE8 else "E9"))
    d1 = np.roll(d, -1)
    a1 = np.roll(a, -1)
    for p in np.nonzero((a == 0x0F) & (a1 >= 0x80) & (a1 <= 0x8F) & (pos + 6 + d1 == target))[0]:
        out.append(("%08X" % int(pos[p]), "0F8x"))
    s8 = np.where(a1 >= 128, a1 - 256, a1)
    for p in np.nonzero(((a == 0xEB) | ((a >= 0x70) & (a <= 0x7F))) & (pos + 2 + s8 == target))[0]:
        out.append(("%08X" % int(pos[p]), "rel8"))
    return sorted(out)


img = Img.load()
ins = body(img)

rc = raw_callers(img, DRAIN)
report("T0", rc == [("0031427D", "E8")], "raw callers of 002E09A0: %s" % rc)

kept, info, jtgt = t1_guard(ins)
report("T1", kept == {0}, "guard keeps +0x3E bits %s (claim: bit 0); %s" % (kept and sorted(kept), info))

ok, info2 = t2_defers(ins, jtgt)
report("T2", ok, "the guard defers: %s" % info2)

outcome, info3 = t3_discard(ins)
report("T3", outcome == "discarded", "slot-0 not ready -> %s (claim: discarded); %s" % (outcome, info3))

# ---- sensitivity ----
report("S1", kept != {7}, "mutated reading 'bit 7' %s against the computed set %s" % (
    "FAILS as required" if kept != {7} else "PASSES - the test is blind", kept and sorted(kept)))
report("S2", outcome != "deferred", "mutated reading 'deferred' %s against the computed outcome '%s'" % (
    "FAILS as required" if outcome != "deferred" else "PASSES - the test is blind", outcome))

shl = next(x for x in ins if S(x) == "shl al, 7")
im3 = img.patched(shl.address, bytes(shl.bytes[:-1]) + b"\x06")
k3, i3, _ = t1_guard(body(im3))
report("S3", k3 != {0}, "image with %08X patched to `shl al, 6`: kept bits %s, claim 'bit 0' %s" % (
    shl.address, k3 and sorted(k3), "FAILS as required" if k3 != {0} else "still passes - the test is blind"))

x8 = next(x for x in ins if S(x) == "xor r8b, r8b")
im4 = img.patched(x8.address, b"\x90" * x8.size)
o4, i4 = t3_discard(body(im4))
report("S4", o4 != "discarded", "image with %08X `xor r8b, r8b` patched to NOPs: outcome %s, claim 'discarded' %s" % (
    x8.address, o4, "FAILS as required" if o4 != "discarded" else "still passes - the test is blind"))

print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
