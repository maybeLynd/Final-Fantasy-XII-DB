"""sd182_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for the SD-182 review (2026-09-30).

Not the package's img.py / census: the lane's ov31_indep loader (sha256 asserted), my own .pdata root walk, capstone.

  A  image-wide sweep for every way of forming a x*144 offset: (a) `lea r,[x+x*8]` with `shl r,4` within the next 4
     instructions on the same register (any order of the following add), (b) `shl r,4` followed within 4 by
     `lea r,[r+r*8]`, (c) `imul r,*,0x90`. Each hit is printed with its .pdata root and the next instruction that adds a
     memory qword to the register (the base it indexes), so a non-adjacent / differently-ordered index is not missed.
  B  a forward taint per function (linear, per root, all fragments): a register becomes tainted when it is the result of
     an x*144 index plus a memory qword at displacement 0x18, or a load `mov r,[t+0x18]` where t holds a nav-table
     pointer (loaded from 02EC1370 / 02EC1378 / 0209A678 / 0209A680); taint propagates through mov/lea/add/sub of a
     tainted register; any instruction whose FIRST operand is memory based on a tainted register and whose mnemonic is a
     write form is reported. Writes are found by mnemonic + first operand (capstone 5 marks movups/movq/... memory
     destinations as READ). Run over: the five walks, every function referencing the four table cells, and FA0/EB0.
     Positive controls: two synthetic byte sequences (a direct `movss [r10+0x14],xmm0` and a derived
     `lea rcx,[r10+0x50]; movups [rcx],xmm0` after the D4B0 index idiom) must be flagged.
  C  references to the table cells 02EC1370 / 02EC1378 / 0209A678 / 0209A680: rip-relative, image-base-relative, abs64.
  D  callers (E8/E9 + jcc + stored pointers) of the two shape consumers 00380FA0 / 00381EB0.
"""
import bisect, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_REG, CS_OP_IMM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(e for e in (struct.unpack_from("<III", T.raw, o + 12 * k) for k in range(dd.Size // 12)) if e[0])
ST = [e[0] for e in PD]


def root_of_entry(e):
    while True:
        uo = T.off(T.IB + e[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
        if not (fl & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)


FR = {}
for e in PD:
    FR.setdefault(root_of_entry(e), []).append((T.IB + e[0], T.IB + e[1]))


def root(va):
    rva = va - T.IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    return root_of_entry(PD[j])


def fn(r):
    out = []
    for a, b in sorted(FR.get(r, [])):
        out += T.dis(a, b)
    return out


WRITE = ("mov", "movss", "movsd", "movups", "movaps", "movdqa", "movdqu", "movq", "movd", "movlps", "movhps", "movlpd",
         "movhpd", "movntps", "movnti", "stos", "add", "sub", "and", "or", "xor", "inc", "dec", "neg", "not", "xchg",
         "cmpxchg", "bts", "btr", "btc", "shl", "shr", "sar", "rol", "ror", "adc", "sbb", "setb", "seta", "sete", "setne",
         "vmovss", "vmovups", "vmovaps", "pextrd", "extractps", "movsxd", "cvtps2ph", "pop")
WRITE_PREFIX = ("set", "cmov")


def is_write(x):
    ops = x.operands
    if not ops or ops[0].type != CS_OP_MEM:
        return False
    m = x.mnemonic
    if m.startswith(("cmp", "test", "prefetch", "push", "lea", "nop", "bt ")) or m in ("bt", "ucomiss", "comiss"):
        return False
    return m in WRITE or m.startswith(WRITE_PREFIX) or m.startswith("v") or m.startswith("rep")


REG64 = {}
def r64(x, reg):
    n = x.reg_name(reg)
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "esp": "rsp"}
    if n in m:
        return m[n]
    if n.startswith("r") and n[-1] in "dwb" and n[1:-1].isdigit():
        return n[:-1]
    return n


TABLE_CELLS = (0x02EC1370, 0x02EC1378, 0x0209A678, 0x0209A680)


def taint_scan(ins, seed_tab_regs=()):
    """returns (writes through subrecord-tainted regs, writes through table-tainted regs)."""
    sub, tab = set(), set(seed_tab_regs)
    idx144 = set()
    hits_sub, hits_tab = [], []
    for k, x in enumerate(ins):
        ops = x.operands
        # writes first (uses the taint before this instruction redefines it)
        if is_write(x):
            b = ops[0].mem.base
            bi = ops[0].mem.index
            names = {r64(x, b) if b else None, r64(x, bi) if bi else None}
            if names & sub:
                hits_sub.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
            if names & tab:
                hits_tab.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
        if not ops or ops[0].type != CS_OP_REG:
            continue
        d = r64(x, ops[0].reg)
        src_regs = set()
        for op in ops[1:]:
            if op.type == CS_OP_REG:
                src_regs.add(r64(x, op.reg))
            elif op.type == CS_OP_MEM:
                if op.mem.base:
                    src_regs.add(r64(x, op.mem.base))
                if op.mem.index:
                    src_regs.add(r64(x, op.mem.index))
        m = x.mnemonic
        new_sub = new_tab = new_idx = False
        if m == "lea" and len(ops) == 2 and ops[1].type == CS_OP_MEM and ops[1].mem.scale == 8 and ops[1].mem.base \
                and ops[1].mem.base == ops[1].mem.index:
            new_idx = True
        if m == "shl" and d in idx144:
            new_idx = True
        if m == "mov" and len(ops) == 2 and ops[1].type == CS_OP_MEM and ops[1].mem.base == X86_REG_RIP:
            t = x.address + x.size + ops[1].mem.disp
            if t in TABLE_CELLS:
                new_tab = True
        if m == "mov" and len(ops) == 2 and ops[1].type == CS_OP_MEM and ops[1].mem.base and \
                ops[1].mem.disp in tuple(c - T.IB for c in TABLE_CELLS):
            new_tab = True
        if m == "add" and d in idx144 and len(ops) == 2 and ops[1].type == CS_OP_MEM and ops[1].mem.disp == 0x18:
            new_sub = True
        if m == "mov" and len(ops) == 2 and ops[1].type == CS_OP_MEM and ops[1].mem.disp == 0x18 and \
                ops[1].mem.base and r64(x, ops[1].mem.base) in tab and ops[0].size == 8:
            new_sub = True
        if m in ("mov", "lea", "add", "sub") and (src_regs & sub) and not (m == "mov" and ops[1].type == CS_OP_MEM):
            new_sub = True
        if m in ("mov", "lea", "add", "sub") and (src_regs & tab) and not (m == "mov" and ops[1].type == CS_OP_MEM):
            new_tab = True
        if m in ("add", "sub") and d in sub:
            new_sub = True
        for s, flag in ((sub, new_sub), (tab, new_tab), (idx144, new_idx)):
            if flag:
                s.add(d)
            elif m not in ("cmp", "test", "push") and not m.startswith(("cmp", "test")):
                s.discard(d)
    return hits_sub, hits_tab


print("== B0. positive controls for the taint scan (synthetic bytes, decoded at a dummy address)")
syn1 = bytes.fromhex("4C8D14C0" "49C1E204" "4D035718" "F3410F114214")
syn2 = bytes.fromhex("4C8D14C0" "49C1E204" "4D035718" "498D4A50" "0F1101")
# syn3: the load itself must seed via the rip->TABLE_CELLS rule, not a manual seed that the
# same instruction immediately discards (the old control's rip+0 resolved to a non-table cell).
import struct as _st
DUMMY = 0x10000000
disp = TABLE_CELLS[0] - (DUMMY + 7)
syn3 = bytes.fromhex("488B05") + _st.pack("<i", disp) + bytes.fromhex("4C8B4018" "F3410F114010")
for name, b in (("direct movss", syn1), ("derived lea+movups", syn2)):
    ins = list(T.md.disasm(b, DUMMY))
    hs, ht = taint_scan(ins)
    print("  %-22s -> flagged %d: %s" % (name, len(hs), "; ".join(hs)))
ins = list(T.md.disasm(syn3, DUMMY))
hs, ht = taint_scan(ins)
print("  %-22s -> flagged %d: %s" % ("tab+0x18 load", len(hs), "; ".join(hs)))

print("== A. image-wide x*144 index forms (all .pdata roots)")
A = []
for r in sorted(FR):
    if not any(n == ".text" and v <= r < v + vs for n, v, vs, p, rs in T.TEXT):
        continue
    ins = fn(r)
    for k, x in enumerate(ins):
        ops = x.operands
        kind = None
        if x.mnemonic == "lea" and len(ops) == 2 and ops[1].type == CS_OP_MEM and ops[1].mem.scale == 8 and ops[1].mem.base \
                and ops[1].mem.base == ops[1].mem.index and ops[1].mem.disp == 0:
            d = r64(x, ops[0].reg)
            for y in ins[k + 1:k + 5]:
                if y.mnemonic == "shl" and y.operands[0].type == CS_OP_REG and r64(y, y.operands[0].reg) == d and \
                        y.operands[1].type == CS_OP_IMM and y.operands[1].imm == 4:
                    kind = "lea9+shl4"; break
        if x.mnemonic == "imul" and len(ops) == 3 and ops[2].type == CS_OP_IMM and ops[2].imm == 0x90:
            d = r64(x, ops[0].reg); kind = "imul 0x90"
        if x.mnemonic == "shl" and len(ops) == 2 and ops[1].type == CS_OP_IMM and ops[1].imm == 4 and ops[0].type == CS_OP_REG:
            d = r64(x, ops[0].reg)
            for y in ins[k + 1:k + 5]:
                if y.mnemonic == "lea" and y.operands[1].type == CS_OP_MEM and y.operands[1].mem.scale == 8 and \
                        y.operands[1].mem.base and r64(y, y.operands[1].mem.base) == d and r64(y, y.operands[1].mem.index) == d:
                    kind = "shl4+lea9"; break
        if kind:
            nxt = ""
            for y in ins[k + 1:k + 8]:
                if y.mnemonic == "add" and y.operands[0].type == CS_OP_REG and r64(y, y.operands[0].reg) == d:
                    nxt = "%08X %s %s" % (y.address, y.mnemonic, y.op_str); break
            A.append((r, x.address, kind, d, nxt))
for r, a, kind, d, nxt in A:
    print("  root %08X  %08X %-10s %-4s next-add: %s" % (r, a, kind, d, nxt))
plus18 = [h for h in A if h[4].endswith("+ 0x18]")]
print("  total x*144 forms %d in %d roots; followed by `add r, qword [..+0x18]`: %d in roots %s"
      % (len(A), len(set(h[0] for h in A)), len(plus18), ", ".join("%08X" % r for r in sorted(set(h[0] for h in plus18)))))

print("== C. references to the nav-table cells")
users = set()
for c in TABLE_CELLS:
    rr = T.rip_refs(c, c + 8)
    ib = T.imagebase_refs(c, c + 1)
    dr = T.data_refs(c)
    print("  %08X: rip %d, image-base %d, abs64 %d, rva32 %d" % (c, len(rr), len(ib), len(dr["abs64"]), len(dr["rva32"])))
    for h in rr + ib:
        print("     %08X %s %s (%dB)  root %s" % (h[0], h[1], h[2], h[3], "%08X" % root(h[0]) if root(h[0]) else "?"))
        if root(h[0]):
            users.add(root(h[0]))

print("== B. taint scan: writes through a subrecord pointer (and through a table pointer)")
targets = sorted(set(h[0] for h in A) | users | {0x00380FA0, 0x00381EB0})
for r in targets:
    ins = fn(r)
    seed = ("rcx",) if r in (0x00232380,) else ()
    hs, ht = taint_scan(ins, seed)
    print("  %08X  %4d ins  sub-writes %d %s | tab-writes %d %s" % (r, len(ins), len(hs), hs[:6], len(ht), ht[:6]))

print("== D. callers of the shape consumers")
for t in (0x00380FA0, 0x00381EB0):
    rc = T.rel32_callers(t); jc = T.jcc_callers(t); dr = T.data_refs(t)
    print("  %08X: rel32 %s ; jcc %s ; abs64 %s ; rva32 %d" % (t, ["%s (root %08X)" % (s, root(int(s[:8], 16)) or 0) for s in rc], jc,
                                                              dr["abs64"], len(dr["rva32"])))
