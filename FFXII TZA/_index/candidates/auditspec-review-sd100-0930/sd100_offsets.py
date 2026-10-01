"""sd100_offsets.py - SWE2-AUDIT-SPEC: at which offsets K do callers embed a text element, and does any caller body write
the element's mode byte as [base + K + 0xB0]?

  1. Element methods: every E8/E9 target in 002AB000..002B6000 (the element-method block that holds 002ABF70,
     002AC1E0, 002B32D0, 002B3950, 002B3C30, 002B3D50). For every call site of one, the last rcx write before it in
     the caller (decoded from the .pdata root, stopping at a call/branch). Collect `lea rcx, [base + K]` with K != 0.
  2. For each (caller root, base, K), every write in the caller's whole body (all its .pdata ranges) whose operand has
     that base and covers byte K + 0xB0; the low-byte classification of sd100_census.py is applied.
Control: 002A6190 must yield K = 0xD0 with the write 002A6606 (mov byte [rdi+0x180], 1).
"""
import bisect, collections, json, os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_IMM, CS_OP_REG, CS_AC_WRITE
from capstone.x86 import X86_REG_RCX


def is_w(i, op):
    """capstone 5.0.7 marks the memory destination of movups / movq / movlps / movhps as READ; a mov-family
    instruction whose FIRST operand is this memory operand is a store."""
    if op.access & CS_AC_WRITE:
        return True
    o0 = i.operands[0] if len(i.operands) else None
    return (o0 is not None and o0.type == CS_OP_MEM and o0.mem.base == op.mem.base and o0.mem.disp == op.mem.disp
            and o0.mem.index == op.mem.index and i.mnemonic.startswith(("mov", "vmov"))
            and i.mnemonic not in ("movzx", "movsx", "movsxd"))

RC = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
_o = T.off(T.IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", T.raw, _o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def chain_root(e):
    for _ in range(32):
        uo = T.off(T.IB + e[2]); fl = T.raw[uo] >> 3; cnt = T.raw[uo + 2]
        if not (fl & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)
    return None


ROOTS = collections.defaultdict(list)
for e in PD:
    ROOTS[chain_root(e)].append((T.IB + e[0], T.IB + e[1]))


def root(va):
    rva = va - T.IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    return chain_root(PD[j])


BODY = {}


def body(r):
    if r not in BODY:
        out = []
        for a, b in sorted(ROOTS[r]):
            out += T.dis(a, b)
        BODY[r] = out
    return BODY[r]


def lowbyte(i, op, D, tgt):
    sh = (tgt - D) * 8
    imms = [x.imm for x in i.operands if x.type == CS_OP_IMM]
    if i.mnemonic in ("or", "xor", "and") and imms:
        m = (imms[0] & ((1 << (op.size * 8)) - 1)) >> sh & 0xFF
        return m != 0xFF if i.mnemonic == "and" else m != 0
    if i.mnemonic in ("bts", "btr", "btc") and imms:
        return sh <= imms[0] < sh + 8
    if i.mnemonic in ("or", "xor", "and", "bts", "btr", "btc"):
        return "reg"
    return True


targets = sorted(int(k, 16) for k in RC if 0x002AB000 <= int(k, 16) < 0x002B6000)
emb = collections.defaultdict(set)      # (caller root, base reg name, K) -> {(site, callee)}
for t in targets:
    for s in RC["%X" % t]:
        s = int(s, 16)
        r = root(s)
        if r is None:
            continue
        ins = body(r)
        idx = {i.address: n for n, i in enumerate(ins)}
        if s not in idx:
            continue
        for i in reversed(ins[:idx[s]]):
            if i.mnemonic == "call" or i.mnemonic.startswith("j"):
                break
            if len(i.operands) == 2 and i.operands[0].type == CS_OP_REG and i.operands[0].reg == X86_REG_RCX:
                if i.mnemonic == "lea" and i.operands[1].mem.disp not in (0,) and i.operands[1].mem.index == 0:
                    m = i.operands[1].mem
                    emb[(r, i.reg_name(m.base), m.disp)].add((s, t))
                break
print("embedding offsets K found through `lea rcx, [base+K]` before element-method calls: %d (caller, base, K) triples" % len(emb))
ks = collections.Counter(k for (_, _, k) in emb)
print("distinct K: %s" % ", ".join("0x%X x%d" % kv for kv in sorted(ks.items())))
for (r, base, K), calls in sorted(emb.items()):
    tgt = K + 0xB0
    w = []
    for i in body(r):
        for op in i.operands:
            if op.type == CS_OP_MEM and is_w(i, op) and op.mem.base and i.reg_name(op.mem.base) == base \
                    and op.mem.disp <= tgt < op.mem.disp + op.size:
                c = lowbyte(i, op, op.mem.disp, tgt)
                w.append("%08X %s %s%s" % (i.address, i.mnemonic, i.op_str, "" if c is True else ("  [keeps low byte]" if c is False else "  [reg operand]")))
    if w:
        print("%08X  [%s+0x%X] (mode byte +0x%X)  callees %s" % (r, base, K, tgt, sorted({"%08X" % c for _, c in calls})))
        for x in w:
            print("    write %s" % x)
print("(triples with no covering write are omitted)")
