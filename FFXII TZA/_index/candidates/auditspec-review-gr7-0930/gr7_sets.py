"""gr7_sets.py - SWE2-AUDIT-SPEC review of GR-7: where the selector evaluator's records come from (2026-09-30).

00301AD0 has one raw caller, 003016A8 in AiOrder_EvaluateAndResolveActionTarget 003014C0 (rdx = the order record r14).
003014C0 has one raw caller, 00305DD2 in BattleUnit_SelectAndCommitNextAction 00305AB0, which walks a set's
24-byte records at set + 0x20 (count = sum of the set's first 12 bytes). The set pointer comes from BattleUnit
+0x6E0 / +0x6E8 / +0x6F0 or a built-in set in the image.
This script:
  S1  decodes every built-in set 00305AB0 can pick (rip-relative lea into .data/.rdata passed as rdx to 00305CC0)
      and lists every record's selector entries (operand, mode, opcode, param), flagging opcode 0x36 / 0x37;
  S2  lists every 8-byte store to BattleUnit +0x6E0 / +0x6E8 / +0x6F0 / +0x6F8 (raw displacement decode over .text), so the
      set sources can be read.
"""
import struct, bisect
from img import raw, SECS, IB, md, rd, dis, pdata
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP

P = sorted(pdata())
PB = [b for b, e in P]


def owner(a):
    k = bisect.bisect_right(PB, a) - 1
    return P[k][0] if k >= 0 and P[k][0] <= a < P[k][1] else None


def decode_set(b):
    head = rd(b, 12)
    n = sum(head)
    out = []
    for rr in range(n):
        r = b + 0x20 + 24 * rr
        d = rd(r, 24)
        act = struct.unpack_from("<H", d, 0)[0]
        ents = []
        for e in range(3):
            o = 6 + 6 * e
            opd, mode, opc, prm = struct.unpack_from("<HBBh", d, o)
            ents.append((opd, mode, opc, prm))
        out.append((r, act, ents))
    return n, out


def main():
    # the four direct calls to the record walker 00305CC0 (all inside 00305AB0) and the last rdx write before each,
    # following an unconditional jmp back to its source (the two built-in-set leas jump to the call)
    ins = dis(0x00305AB0, 0x00305CC0 - 0x00305AB0)
    by = {x.address: k for k, x in enumerate(ins)}
    sets = []
    for k, x in enumerate(ins):
        if x.mnemonic == "call" and x.operands[0].type == X86_OP_IMM and x.operands[0].imm == 0x00305CC0:
            j = k - 1
            while j >= 0 and not (ins[j].operands and ins[j].operands[0].type == X86_OP_REG
                                  and ins[j].reg_name(ins[j].operands[0].reg) == "rdx"):
                j -= 1
            src = "%s %s" % (ins[j].mnemonic, ins[j].op_str)
            jumpers = [y for y in ins if y.mnemonic == "jmp" and y.operands[0].type == X86_OP_IMM
                       and ins[j].address <= y.operands[0].imm <= x.address and y.address < ins[j].address]
            extra = []
            for y in jumpers:
                q = by[y.address] - 1
                z = ins[q]
                if z.mnemonic == "lea" and z.reg_name(z.operands[0].reg) == "rdx" and z.operands[1].mem.base == X86_REG_RIP:
                    t = z.address + z.size + z.operands[1].mem.disp
                    extra.append("%08X lea rdx -> %08X, jmp %08X" % (z.address, t, y.operands[0].imm))
                    sets.append(t)
            print("S1 call 00305CC0 at %08X: rdx from %08X %s; jumped-in sources %s" % (x.address, ins[j].address, src, extra or "none"))
    for t in sorted(set(sets)):
        n, recs = decode_set(t)
        print("   built-in set %08X: %d records" % (t, n))
        for r, act, ents in recs:
            flag = any(opc in (0x36, 0x37) for opd, mode, opc, prm in ents)
            print("      %08X action %04X entries %s%s" % (r, act, [(hex(o), m, hex(c), p) for o, m, c, p in ents],
                                                         "  <-- 0x36/0x37" if flag else ""))
    text = [s for s in SECS if s[5]][0]
    n_, v, vs, p, rs, x_ = text
    blob = raw[p:p + min(vs, rs)]
    hits = []
    for disp in (0x6E0, 0x6E8, 0x6F0, 0x6F8):
        pat = struct.pack("<I", disp)
        k = blob.find(pat)
        while k >= 0:
            for back in range(2, 8):
                s = k - back
                try:
                    i = next(md.disasm(blob[s:s + 16], v + s, 1))
                except StopIteration:
                    continue
                if i.disp_size == 4 and i.disp_offset == back and i.mnemonic == "mov" and len(i.operands) == 2 \
                        and i.operands[0].type == X86_OP_MEM and i.operands[0].size == 8 and i.operands[0].mem.disp == disp:
                    hits.append((i.address, disp, "%s %s" % (i.mnemonic, i.op_str)))
                    break
            k = blob.find(pat, k + 1)
    print("S2 qword stores to [reg + 0x6E0/0x6E8/0x6F0/0x6F8]: %d" % len(hits))
    for a, d, t in sorted(hits):
        f = owner(a)
        print("   %08X in %s  +0x%X  %s" % (a, ("%08X" % f) if f else "no-pdata", d, t))


if __name__ == "__main__":
    main()
