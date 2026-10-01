"""CharacterRenderRecord DISCOVERED spans the access census missed (OPUS, 2026-09-27, BT-2).

The census character-render-record-accesses.tsv tracks registers linearly, without control flow, so it loses a base
that is re-defined on another path and carries one into a branch where it no longer holds (002EDF90: the four literal
+0x6C8 stores missing, a false +0x6E7 'addr' row). A whole-image scan of the 40 DISCOVERED spans, keeping only bases
proved to be this record, finds three spans with real accesses:

  M1 +0x4B8..+0x4BB, four selector-choice bytes: 00417110 (command class 0x0B) takes the record from the entry
     (00417125 mov rbx, [r8 + 0x2e0]) and the parent record from the pool (0041716C imul rcx, rax, 0x740 / 00417173
     add rcx, [022C6F28]); it reads the parent's byte for selector kinds 0 / 2 / 0x0A / 0x10 (0041718A, 004171AD,
     004171BC, 004171CB) and writes the record's (00417235, 00417242, 0041724F, 0041725C).
  M2 +0x6D8 / +0x6DC: the same body stores entry bit 13 (004171FC..00417204 -> 00417217) and the selector's result
     (004171FA call -> 00417207); rbx is not re-defined before 004172A6.
  M3 +0x110: 00429140, on a record (it addresses +0x284, +0x290, +0x2AE and +0x108), zeroes +0x108 (qword) and +0x110
     (dword) together (00429176 xor eax, eax; 0042917F; 00429186).
Rejected receivers, kept so the wrong reading fails:
  X1 00417110's +0x60 / +0x8C qword stores (0041731F, 00417332) follow 004172A6 lea rbx, [rdi + 0x30]: a 0xA0-stride
     entry array, not the record.
  X2 002E6BD0's +0xEC store (002E6C33): rdi is the actor (002E6BFB mov rdi, rcx; it reads [rdi + 0xc0]).
  X3 002EE1D0's +0x60 read (002EE251): rbx is formed as rax*9 (002EE1EB lea rbx, [rax + rax*8]), not a record.
  S  the store (_types/fields.tsv) no longer declares +0x4B8, +0x6D8 / +0x6DC or +0x110 as unobserved: FAILS on the
     store before this correction.
Usage: python crr_census_misses.py [exe] [fields.tsv]
"""
import copy, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FIELDS = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("FIELDS_PATH") or "FFXII TZA/_types/fields.tsv"
BASE = 0x120000
FUNCS = {0x417110: 703, 0x429140: 358, 0x2E6BD0: 399, 0x2EE1D0: 189}


def load():
    d = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
    off = lambda v: next(v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs)
    cs = Cs(CS_ARCH_X86, CS_MODE_64); ins = {}
    for a, sz in FUNCS.items():
        for x in cs.disasm(d[off(a):off(a) + sz], a):
            ins[x.address] = [x.mnemonic, x.op_str]
    rows = {}
    for l in open(FIELDS, encoding="utf-8"):
        c = l.rstrip("\r\n").split("\t")
        if c[0] == "CharacterRenderRecord":
            rows[int(c[1], 16)] = c
    return ins, rows


def check(ins, rows):
    def at(pc, m, o):
        assert ins.get(pc) == [m, o], (hex(pc), ins.get(pc), m, o)
    # M1
    at(0x417125, "mov", "rbx, qword ptr [r8 + 0x2e0]")
    at(0x41716C, "imul", "rcx, rax, 0x740"); at(0x417173, "add", "rcx, qword ptr [rip + 0x1eafdae]")
    for pc, dd in ((0x41718A, 0x4B8), (0x4171AD, 0x4B9), (0x4171BC, 0x4BA), (0x4171CB, 0x4BB)):
        at(pc, "movsx", "eax, byte ptr [rcx + 0x%x]" % dd)
    for pc, dd in ((0x417235, 0x4B8), (0x417242, 0x4B9), (0x41724F, 0x4BA), (0x41725C, 0x4BB)):
        at(pc, "mov", "byte ptr [rbx + 0x%x], al" % dd)
    at(0x4171A7, "cmp", "r8b, 2"); at(0x4171B6, "cmp", "r8b, 0xa"); at(0x4171C5, "cmp", "r8b, 0x10")
    # M2
    at(0x4171FA, "call", "qword ptr [rdx]"); at(0x417207, "mov", "dword ptr [rbx + 0x6dc], eax")
    at(0x4171FC, "mov", "ecx, dword ptr [rdi + 0xc]"); at(0x417201, "shr", "ecx, 0xd"); at(0x417204, "and", "ecx, 1")
    at(0x417217, "mov", "dword ptr [rbx + 0x6d8], ecx")
    between = [ins[a] for a in sorted(ins) if 0x417125 < a < 0x4172A6]
    assert not any(v[1].startswith(("rbx,", "ebx,")) and v[0] not in ("cmp", "test") for v in between), "M2 rbx re-defined"
    # M3
    for pc, o in ((0x42915D, "byte ptr [rcx + 0x284], 4"),): at(pc, "test", o)
    at(0x42916F, "or", "dword ptr [rcx + 0x290], 2"); at(0x429176, "xor", "eax, eax")
    at(0x429178, "or", "byte ptr [rcx + 0x2ae], 1"); at(0x42917F, "mov", "qword ptr [rcx + 0x108], rax")
    at(0x429186, "mov", "dword ptr [rcx + 0x110], eax")
    # X1-X3
    at(0x4172A6, "lea", "rbx, [rdi + 0x30]"); at(0x41731F, "mov", "qword ptr [rbx + 0x60], r12")
    at(0x417332, "mov", "qword ptr [rbx + 0x8c], r12"); at(0x417348, "add", "rbx, 0xa0")
    at(0x2E6BFB, "mov", "rdi, rcx"); at(0x2E6C33, "mov", "dword ptr [rdi + 0xec], 0"); at(0x2E6C3D, "mov", "rax, qword ptr [rdi + 0xc0]")
    at(0x2EE1EB, "lea", "rbx, [rax + rax*8]"); at(0x2EE251, "mov", "ecx, dword ptr [rbx + 0x60]")
    # S
    for o in (0x4B8, 0x6D8, 0x6DC, 0x110):
        r = rows.get(o)
        assert r is not None and r[6] != "DISCOVERED" and "unobserved" not in r[3], ("S", hex(o), r[3] if r else None)
    assert rows[0x6D8][2] == "4" and rows[0x6DC][2] == "4" and rows[0x4B8][2] == "4" and rows[0x110][2] == "4", "S widths"
    return True


def main():
    ins, rows = load()
    try:
        check(ins, rows); print("PASS M1-M3, X1-X3, S")
    except AssertionError as e:
        print("FAIL", e); sys.exit(1)
    muts = {
        "M1 parent not pool-formed": lambda i, r: i.__setitem__(0x41716C, ["imul", "rcx, rax, 0x290"]),
        "M2 rbx re-defined": lambda i, r: i.__setitem__(0x417160, ["mov", "rbx, rcx"]),
        "M3 other object": lambda i, r: i.__setitem__(0x42917F, ["mov", "qword ptr [rcx + 0x100], rax"]),
        "X1 same object": lambda i, r: i.__setitem__(0x4172A6, ["nop", ""]),
        "S stale row": lambda i, r: r.__setitem__(0x110, r[0x110][:3] + ["unobservedSpan0110"] + r[0x110][4:6] + ["DISCOVERED"] + r[0x110][7:]),
    }
    bad = 0
    for name, mut in muts.items():
        i2, r2 = copy.deepcopy(ins), copy.deepcopy(rows); mut(i2, r2)
        try:
            check(i2, r2); print("MUTANT SURVIVED:", name); bad += 1
        except (AssertionError, KeyError):
            print("rejected:", name)
    print("FAILS", bad); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
