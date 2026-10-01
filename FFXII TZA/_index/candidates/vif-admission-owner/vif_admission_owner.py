"""OPUS owner check on ASTRA-RETURN-OPUS-VIF-ADMISSION-PROGRESS (2026-09-27).

Re-reads the shipping bytes of the UNPACK helper 0022BFF0 and the decoder 0022C970 and checks the facts the
OPUS-owned rows (Vif1Registers02088E30 +0x0C wl / +0x10 cycle, the UQ-215 size-formula paragraph) now carry:

  V1  0022BFF0 loads WL from 02088E3C (+0x0C) into r11 and CL from 02088E40 (+0x10) into edi, before any payload access.
  V2  the only admission test is 0022C00A cmp r11d, edi / jg 0022C8C2 (signed WL > CL), and 0022C8C2 returns 0
      (xor eax, eax) without reaching the nominal-count return 0022C89E.
  V3  the decoder advances its cursor by 4 before the header load (0022C9D3 / 0022C9D6), adds UNPACK's return
      (0022CACC) and loops back to the header load (0022CB55 / 0022CB58) - so on the WL > CL exit the next
      header is read from the first payload dword.
  V4  UNPACK's arguments (0022CA7C..0022CAC7) never use r12, the decoder's byte budget (0022C986 mov r12d, r8d).
  V5  in the V4-32 arm the element counter moves only by WL (0022C67E add ebx, r11d); CL feeds only the
      destination step (0022C611 shl edi, 4 -> rbp -> 0022C678 add r10, rbp). So NUM > 0 with WL = 0 has no
      progress for every CL the signed test admits (0..0x7FFFFFFF), not only CL = 0.
  V6  NUM is the header's byte 2 (0022CA86 sar eax, 0x10 / 0022CA8C movzx ecx, al) -> r13d; NUM = 0 leaves by
      0022C60B jle 0022C89E with a nominal count of 0 (the size formula multiplies by NUM), not 256.

Each check is also run on a mutated instruction list; the run fails unless every mutant is rejected.
Static derivation from original bytes, not execution. Usage: python vif_admission_owner.py <path to FFXII_TZA.exe>
"""
import copy, hashlib, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
BODIES = {0x22BFF0: 2268, 0x22C970: 533}


def load(path):
    d = open(path, "rb").read()
    assert hashlib.sha256(d).hexdigest() == SHA, "not the shipping exe"
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    n = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]

    def off(v):
        for vs, va, rs, ro in secs:
            if BASE + va <= v < BASE + va + rs:
                return v - BASE - va + ro
    cs = Cs(CS_ARCH_X86, CS_MODE_64)
    ins = {}
    for a, size in BODIES.items():
        for x in cs.disasm(d[off(a):off(a) + size], a):
            ins[x.address] = [x.mnemonic, x.op_str, x.address + x.size]
    return ins


def rip_target(ins, pc):
    op = ins[pc][1]
    disp = int(op.split("rip + ")[1].split("]")[0], 16)
    return ins[pc][2] + disp


def check(ins):
    def at(pc, m, o):
        assert ins.get(pc, [None, None])[:2] == [m, o], (hex(pc), ins.get(pc))
    # V1
    at(0x22BFF8, "movsxd", "r11, dword ptr [rip + 0x1e5ce3d]")
    at(0x22C001, "mov", "edi, dword ptr [rip + 0x1e5ce39]")
    assert rip_target(ins, 0x22BFF8) == 0x02088E3C and rip_target(ins, 0x22C001) == 0x02088E40
    pre = [v for a, v in ins.items() if 0x22BFF0 <= a < 0x22C00A]
    assert not any("ptr [r" in v[1] and "rip" not in v[1] and "rsp" not in v[1] for v in pre), "payload access before test"
    # V2
    at(0x22C00A, "cmp", "r11d, edi"); at(0x22C00D, "jg", "0x22c8c2")
    at(0x22C8C2, "xor", "eax, eax")
    tail = [ins[a] for a in sorted(ins) if 0x22C8C4 <= a <= 0x22C8CB]
    assert [t[0] for t in tail] == ["add", "pop", "pop", "pop", "ret"], tail
    # V3
    at(0x22C986, "mov", "r12d, r8d")
    at(0x22C9D0, "movsxd", "rax, edi"); at(0x22C9D3, "add", "edi, 4")
    at(0x22C9D6, "mov", "ebx, dword ptr [rax + rbp]")
    at(0x22CAC7, "call", "0x22bff0"); at(0x22CACC, "add", "edi, eax"); at(0x22CACE, "jmp", "0x22cb41")
    between = [ins[a] for a in sorted(ins) if 0x22CB41 <= a < 0x22CB55]
    assert not any(v[0].startswith("j") or v[0] == "call" or "edi" in v[1] for v in between), between
    at(0x22CB55, "cmp", "edi, r12d"); at(0x22CB58, "jl", "0x22c9d0")
    # V4
    args = [ins[a] for a in sorted(ins) if 0x22CA7C <= a < 0x22CAC7]
    assert len(args) > 10 and not any("r12" in v[1] for v in args), "budget passed to UNPACK"
    # V5
    at(0x22C5F6, "cmp", "esi, 3"); at(0x22C5FF, "test", "r8d, r8d"); at(0x22C602, "jne", "0x22c68d")
    at(0x22C611, "shl", "edi, 4"); at(0x22C61D, "movsxd", "rbp, edi"); at(0x22C678, "add", "r10, rbp")
    at(0x22C614, "mov", "ecx, r11d"); at(0x22C617, "shl", "ecx, 4"); at(0x22C622, "movsxd", "r14, ecx")
    at(0x22C61A, "mov", "esi, r11d"); at(0x22C620, "neg", "esi"); at(0x22C625, "mov", "edi, r13d")
    at(0x22C630, "cmp", "edi, r11d"); at(0x22C635, "cmovg", "ecx, r11d"); at(0x22C63E, "jle", "0x22c678")
    at(0x22C67E, "add", "ebx, r11d"); at(0x22C681, "add", "edi, esi")
    at(0x22C683, "cmp", "ebx, r13d"); at(0x22C686, "jl", "0x22c630")
    loop = [ins[a] for a in sorted(ins) if 0x22C630 <= a <= 0x22C686]
    assert not any(v[1].startswith(("ebx", "r13")) and v[0] not in ("cmp",) and v[1] != "ebx, r11d" for v in loop)
    # V6
    at(0x22CA86, "sar", "eax, 0x10"); at(0x22CA8C, "movzx", "ecx, al"); at(0x22CAAE, "mov", "dword ptr [rsp + 0x28], ecx")
    at(0x22C023, "mov", "r13d, dword ptr [rsp + 0x68]"); at(0x22C039, "imul", "eax, r13d")
    at(0x22C05F, "mov", "dword ptr [rsp], r10d")
    at(0x22C608, "test", "r13d, r13d"); at(0x22C60B, "jle", "0x22c89e"); at(0x22C89E, "mov", "eax, dword ptr [rsp]")
    return True


MUTANTS = {
    "V1 WL read from +0x10": (0x22BFF8, "movsxd", "r11, dword ptr [rip + 0x1e5ce41]"),
    "V2 reject returns the count": (0x22C8C2, "mov", "eax, dword ptr [rsp]"),
    "V2 test is unsigned": (0x22C00D, "ja", "0x22c8c2"),
    "V3 cursor skips a payload on reject": (0x22CACC, "add", "edi, 0x10"),
    "V4 budget passed": (0x22CAC4, "mov", "r9d, r12d"),
    "V5 counter moves by CL": (0x22C67E, "add", "ebx, 1"),
    "V6 NUM 0 means 256": (0x22C60B, "jle", "0x22c611"),
}


def main():
    ins = load(sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe")
    check(ins)
    print("PASS V1-V6 on the shipping bytes")
    bad = 0
    for name, (pc, m, o) in MUTANTS.items():
        mut = copy.deepcopy(ins)
        mut[pc][:2] = [m, o]
        try:
            check(mut)
            print("MUTANT SURVIVED:", name); bad += 1
        except AssertionError:
            print("rejected:", name)
    print("FAILS", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
