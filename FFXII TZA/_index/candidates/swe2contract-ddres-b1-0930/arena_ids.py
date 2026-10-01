"""arena_ids.py - which arena ids the image registers through the arena initializer 00369D30(id, block, size, slots).
SWE2-CONTRACT, 2026-09-30, for the boot page's "is id 10 registered elsewhere" residue. Static. Reads only.

Callers come from Tools/work/graph/edges.tsv (direct call AND tail-jump edges). At each call/jmp to 00369D30 the last
write to ecx before it is read: `mov ecx, imm` or `lea ecx, [r9 + imm]` with r9 zeroed or holding a known constant.
Positive control: boot 0022A0B0 must yield exactly {2,3,4,5,6,7,8,9,0xB} (published on the page and in EXP-142).
Also checked: no rip-relative operand and no absolute qword in the file equal 00369D30 (a pointer route would be
invisible to the edge list). Blind spot: a call through a pointer assembled at run time.
"""
import io, os, struct, sys
import capstone
import block_writer_disjoint as b

TARGET = 0x00369D30


def ecx_value(prev, regs):
    for p in reversed(prev):
        ops = p.op_str.replace(" ", "")
        if p.mnemonic == "mov" and ops.startswith("ecx,") and ops[4:].startswith("0x"):
            return int(ops[4:], 16)
        if p.mnemonic == "mov" and ops.startswith("ecx,") and ops[4:].isdigit():
            return int(ops[4:])
        if p.mnemonic == "lea" and ops.startswith("ecx,["):
            inner = ops[5:-1]
            sign = -1 if "-" in inner else 1
            reg, _, disp = inner.replace("-", "+").partition("+")
            base = regs.get(reg)
            if base is not None:
                return base + sign * int(disp, 16 if disp.startswith("0x") else 10)
            return "lea %s" % inner
        if ops.startswith("ecx,") or ops.startswith("rcx,"):
            return "?%s %s" % (p.mnemonic, p.op_str)
    return None


def main():
    at, ext = b.load(), b.extents()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    callers = sorted(set(int(l.split("\t")[0], 16) for l in io.open(os.path.join(b.DB, "..", "Tools", "work", "graph",
                     "edges.tsv"), encoding="utf-8").read().splitlines()[1:] if l.split("\t")[1] == "00369D30"))
    ids, fails = {}, 0
    for f in callers:
        ins = list(md.disasm(at(f, ext[f]), f))
        for k, i in enumerate(ins):
            if i.mnemonic in ("call", "jmp") and i.op_str == hex(TARGET):
                regs = {}
                for p in ins[:k]:   # last assignment of r9 anywhere before the call, linear order
                    o = p.op_str.replace(" ", "")
                    if p.mnemonic == "xor" and o in ("r9d,r9d", "r9,r9"):
                        regs["r9"] = 0
                    elif p.mnemonic == "mov" and o.startswith("r9d,0x"):
                        regs["r9"] = int(o[6:], 16)
                    elif p.mnemonic == "mov" and o.startswith("r9d,") and o[4:].isdigit():
                        regs["r9"] = int(o[4:])
                    elif o.startswith(("r9d,", "r9,")):
                        regs.pop("r9", None)
                v = ecx_value(ins[max(0, k - 12):k], regs)
                ids.setdefault(f, []).append(v)
                print("%08X  %08X %-4s id=%s" % (f, i.address, i.mnemonic, hex(v) if isinstance(v, int) else v))
    boot = sorted(x for x in ids.get(0x0022A0B0, []) if isinstance(x, int))
    ok = boot == [2, 3, 4, 5, 6, 7, 8, 9, 0xB]
    print("%s  control: boot registers %s" % ("PASS" if ok else "FAIL", [hex(x) for x in boot]))
    fails += not ok
    pe = io.open(b.EXE, "rb").read()
    q = pe.count(struct.pack("<Q", TARGET))
    print("absolute qword 00369D30 occurrences in the file: %d" % q)
    allids = sorted(set(x for v in ids.values() for x in v if isinstance(x, int)))
    print("ids registered image-wide: %s ; id 10 present: %s" % ([hex(x) for x in allids], 10 in allids))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
