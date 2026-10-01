"""sd192_census.py - SWE2-AUDIT-SPEC independent census for the SD-192 review (2026-09-30).

Not the author's sweep: a raw byte search of every executable section for a disp32 in 0x140..0x14F (disp8 cannot
hold 0x14F), each candidate decoded backwards and kept only when the decoded memory operand has a non-rip base and
that displacement. Loader: ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha256 asserted).

For every access whose byte range covers +0x14F it prints the instruction and, for a register load, the first later
instruction (linear, <= 16 instructions, stopping at a branch) that uses the loaded register - so bit-0 tests done
through movzx+test, and/test, shr, bt, or a wider read are classified too.
Output groups: B0 (tests bit 0 of +0x14F), OTHER-BIT (a read whose first use tests other bits), WRITE, UNCLASSIFIED.
Blind spot: +0x14F reached through a pre-offset pointer (lea r,[x+0x1xx] then a disp8), not searched.
"""
import os, struct, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID
from capstone import CS_OP_REG, CS_OP_IMM, CS_OP_MEM

FIELD = 0x14F
md = T.md
FAM = {}
for fam in (("rax", "eax", "ax", "al"), ("rbx", "ebx", "bx", "bl"), ("rcx", "ecx", "cx", "cl"), ("rdx", "edx", "dx", "dl"),
            ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"), ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")) + \
        tuple(("r%d" % n, "r%dd" % n, "r%dw" % n, "r%db" % n) for n in range(8, 16)):
    for r in fam:
        FAM[r] = fam[0]


def fam(name):
    return FAM.get(name, name)


def candidates():
    seen = set()
    for n, v, vs, p, rs in T.TEXT:
        blob = T.raw[p:p + min(vs, rs)]
        for disp in range(0x140, 0x150):
            pat = struct.pack("<I", disp)
            k = blob.find(pat)
            while k >= 0:
                for back in range(1, 12):
                    if k - back < 0:
                        continue
                    ins = list(md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                    if not ins:
                        continue
                    i = ins[0]
                    if not (i.address < v + k < i.address + i.size):
                        continue
                    for op in i.operands:
                        if op.type == CS_OP_MEM and op.mem.base not in (X86_REG_RIP, X86_REG_INVALID) and op.mem.disp == disp:
                            if disp <= FIELD < disp + op.size and i.address not in seen:
                                seen.add(i.address)
                                yield i, op
                k = blob.find(pat, k + 1)


def follow(i, reg):
    """first later instruction (linear) that reads fam(reg); stops at branches / ret / overwrite."""
    rf = fam(reg)
    o = T.off(i.address + i.size)
    for j in md.disasm(T.raw[o:o + 16 * 15], i.address + i.size):
        regs_r, regs_w = j.regs_access()
        rd = set(fam(j.reg_name(r)) for r in regs_r)
        wr = set(fam(j.reg_name(r)) for r in regs_w)
        if rf in rd:
            return j
        if rf in wr or j.group(1) or j.group(3) or j.mnemonic in ("ret", "call"):
            return None
    return None


def main():
    groups = collections.defaultdict(list)
    for i, op in sorted(candidates(), key=lambda x: x[0].address):
        bit = 8 * (FIELD - op.mem.disp)          # bit index of +0x14F bit 0 inside the operand
        txt = "%08X  %s %s  (size %d, +0x14F bit0 = operand bit %d)" % (i.address, i.mnemonic, i.op_str, op.size, bit)
        ops = i.operands
        is_write = ops[0].type == CS_OP_MEM and i.mnemonic not in ("test", "cmp", "bt")
        if i.mnemonic == "test" and ops[1].type == CS_OP_IMM:
            g = "B0" if (ops[1].imm >> bit) & 1 else "OTHER-BIT"
            groups[g].append(txt)
            continue
        if i.mnemonic == "bt" and ops[1].type == CS_OP_IMM:
            groups["B0" if ops[1].imm == bit else "OTHER-BIT"].append(txt)
            continue
        if i.mnemonic == "cmp":
            groups["UNCLASSIFIED"].append(txt + "   [cmp]")
            continue
        if is_write:
            groups["WRITE"].append(txt)
            continue
        if ops[0].type == CS_OP_REG:
            dst = i.reg_name(ops[0].reg)
            j = follow(i, dst)
            use = ("%08X %s %s" % (j.address, j.mnemonic, j.op_str)) if j else "(no use before branch/overwrite)"
            g = "UNCLASSIFIED"
            if j is not None and len(j.operands) == 2 and j.operands[1].type == CS_OP_IMM and j.mnemonic in ("test", "and"):
                g = "B0" if (j.operands[1].imm >> bit) & 1 else "OTHER-BIT"
            elif j is not None and j.mnemonic == "bt" and j.operands[1].type == CS_OP_IMM:
                g = "B0" if j.operands[1].imm == bit else "OTHER-BIT"
            elif j is not None and j.mnemonic in ("shr", "sar") and j.operands[1].type == CS_OP_IMM:
                g = "SHIFT(bit0->%d)" % (bit - j.operands[1].imm) if j.operands[1].imm <= bit else "OTHER-BIT"
            groups[g].append(txt + "   -> " + use)
            continue
        groups["UNCLASSIFIED"].append(txt)
    for g in sorted(groups):
        print("== %s: %d" % (g, len(groups[g])))
        for s in groups[g]:
            print("  " + s)


if __name__ == "__main__":
    main()
