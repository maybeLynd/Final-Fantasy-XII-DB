"""rip_refs.py - list every rip-relative instruction operand, over every listed function body, whose target lies in
[lo, hi). SWE2-CONTRACT, 2026-09-30. Static. Reads only.

Usage: python rip_refs.py <lo_hex> [hi_hex]      (hi defaults to lo + 8)

Blind spots, stated: bodies are linear-swept from functions.tsv entries over body_bytes, so code outside the function
list and references formed through a base register (lea once, then [reg + disp]) are not seen. Positive control, always
run: the boot writer 0022A1A7 must be found as a store to 02064ACC (published on what-the-engine-fixes-at-boot.md).
"""
import sys
import capstone
import block_writer_disjoint as b


def scan(lo, hi):
    at, ext = b.load(), b.extents()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    hits = []
    for entry, size in sorted(ext.items()):
        code = at(entry, size)
        if not code:
            continue
        for ins in md.disasm(code, entry):
            for i, op in enumerate(ins.operands):
                if op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
                    t = ins.address + ins.size + op.mem.disp
                    if lo <= t < hi:
                        kind = "w" if i == 0 and len(ins.operands) > 1 and not ins.mnemonic.startswith(("cmp", "test")) else "r"
                        if ins.mnemonic == "lea":
                            kind = "lea"
                        hits.append((entry, ins.address, kind, ins.mnemonic, ins.op_str, t))
    return hits


def main():
    lo = int(sys.argv[1], 16)
    hi = int(sys.argv[2], 16) if len(sys.argv) > 2 else lo + 8
    hits = scan(min(lo, 0x02064ACC), max(hi, 0x02064ACC + 4))
    ctl = any(a == 0x0022A1A7 and k == "w" for _, a, k, _, _, t in hits if t == 0x02064ACC)
    print("%s  control: store to 02064ACC at 0022A1A7 found" % ("PASS" if ctl else "FAIL"))
    for fn, a, k, m, ops, t in hits:
        if lo <= t < hi:
            print("%08X  %08X  %-3s  %-6s %-40s -> %08X" % (fn, a, k, m, ops, t))
    return 0 if ctl else 1


if __name__ == "__main__":
    sys.exit(main())
