"""RM-1 part 3: the nine math-template `m_elements` registrations bound to their classes and carved (OPUS, 2026-09-27).

Each registrar builds its class descriptor through 00632C90(desc, parent, name, size, 4) and then registers
`m_elements` through the fixed-size member constructor 00632A70 with a7 = the element count and the element type from
006301F0, which returns the descriptor 01F2E690 - the one 97 members of the recovered field schema name `float`.
The name string, the size and the count are read from the registrar's own instructions; the carve refuses a class
whose single declared gap is not exactly count x 4 bytes. Idempotent; EOL-preserving.
  --check   verify only (exit 1 on any mismatch), no write
"""
import pathlib, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG

DB = pathlib.Path(__file__).resolve().parents[3]
EXE = DB.parent / "Tools" / "work" / "exe" / "FFXII_TZA.exe"
F = DB / "_types" / "fields.tsv"
MARK = "REFLECTED MEMBER, RM-1 part 3 2026-09-27 (OPUS)"
REG = {0x006B0760: 0x006B0854, 0x006B08A0: 0x006B0994, 0x006B09E0: 0x006B0AD4, 0x006B0B20: 0x006B0C27,
       0x006B0EC0: 0x006B0FC7, 0x006B1320: 0x006B1427, 0x006B1600: 0x006B1707, 0x006B19A0: 0x006B1AA7,
       0x006B33F0: 0x006B34F3}
d = EXE.read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]


def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True


def cstr(a):
    o = off(a); return d[o:d.index(b"\0", o)].decode("latin1")


def read_registrar(entry, site):
    regs = {}; cls = size = count = elem = None
    for i in cs.disasm(d[off(entry):off(site) + 5], entry):
        ops = i.operands
        if i.mnemonic == "lea" and ops[1].type == X86_OP_MEM and ops[1].value.mem.base != 0:
            if i.reg_name(ops[1].value.mem.base) == "rip":
                regs[i.reg_name(ops[0].reg)] = i.address + i.size + ops[1].value.mem.disp
        elif i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_IMM:
            regs[i.reg_name(ops[0].reg)] = ops[1].imm
        elif i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[1].type == X86_OP_IMM \
                and i.reg_name(ops[0].value.mem.base) == "rsp" and ops[0].value.mem.disp == 0x30:
            count = ops[1].imm
        elif i.mnemonic == "call" and ops[0].type == X86_OP_IMM:
            if ops[0].imm == 0x00632C90:
                cls, size = cstr(regs["r8"]), regs["r9d"]
            elif ops[0].imm == 0x006301F0:
                x = next(cs.disasm(d[off(0x0063021E - 7):off(0x0063021E)], 0x0063021E - 7))
                elem = x.address + x.size + x.operands[1].value.mem.disp
            elif ops[0].imm == 0x00632A70:
                assert i.address == site
    return cls, size, count, elem


def main():
    check_only = "--check" in sys.argv
    found = [read_registrar(e, s) for e, s in REG.items()]
    lines = F.read_bytes().decode("utf-8").splitlines(keepends=True)
    bad = []; n = 0
    for (e, s), (cls, size, count, elem) in zip(REG.items(), found):
        if elem != 0x01F2E690 or count * 4 != size:
            bad.append((cls, size, count, hex(elem or 0))); continue
        idx = [i for i, l in enumerate(lines) if l.startswith(cls + "\t")]
        cur = [lines[i].rstrip("\r\n").split("\t") for i in idx]
        if any(MARK in "\t".join(c) for c in cur):
            continue
        if not (len(cur) == 1 and cur[0][1] in ("0x0000", "0x000") and int(cur[0][2]) == size and cur[0][3].startswith("unobserved")):
            bad.append((cls, "gap does not tile", [c[:4] for c in cur])); continue
        if check_only:
            continue
        c = cur[0]; eol = lines[idx[0]][len(lines[idx[0]].rstrip("\r\n")):]
        c[3], c[4] = "m_elements", "float[%d]" % count
        c[5] = ("engine-registered member name m_elements (Phyre reflection of the math template %s): a fixed-size array of"
                " %d floats. Element meaning is not claimed." % (cls, count))
        c[6], c[7] = "TYPE RESOLVED", "PROVEN"
        c[8] = ("%s: registrar %08X builds the %s descriptor through 00632C90 (name string, size 0x%X) and registers"
                " 'm_elements' through the fixed-size member constructor 00632A70 at %08X with a7=%d and the element descriptor"
                " 01F2E690 from 006301F0 (float in 97 field-schema members). The member tiles the class's former single gap"
                " exactly. Evidence _index/candidates/rm1-array-members/carve_math.py. || previous: %s"
                % (MARK, e, cls, size, s, count, c[8]))
        lines[idx[0]] = "\t".join(c) + eol; n += 1
    if bad:
        print("REFUSED", bad); sys.exit(1)
    if check_only:
        print("CHECK OK", [(f[0], f[2]) for f in found]); return
    if n:
        F.write_bytes("".join(lines).encode("utf-8"))
    print("carved", n, [(f[0], f[2]) for f in found])


if __name__ == "__main__":
    main()
