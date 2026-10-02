"""lbg_check.py - the facts behind the licence node-360 re-correction and the 00323D10 / 00309060 sections (OPUS,
2026-10-02). FAILS n. The image checks, then a shipped-data check: battle_pack.bin directory +0x34 holds 361 records
in every language copy (VBF path argument optional).
"""


import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00236D5C, "lea", "rcx, [rip + 0x2c882d5]"),
    (0x00236D63, "movsxd", "rdx, dword ptr [rax + 0x34]"),
    (0x00322FCB, "mov", "rcx, qword ptr [rip + 0x2b9c066]"),
    (0x00322FD9, "mov", "ecx, dword ptr [rcx + 4]"),
    (0x00323D85, "movzx", "r8d, byte ptr [rcx + rbp + 0x194]"),
    (0x00323DF0, "movzx", "ecx, byte ptr [rdx + 6]"),
    (0x00323E88, "cmp", "byte ptr [rdx + 5], 0x1e"),
    (0x00323E8E, "mov", "cx, 0xc01f"),
    (0x0055D9B1, "mov", "eax, 0x168"),
    (0x0055D9B6, "cmp", "word ptr [rcx + 8], ax"),
    (0x0055DA6A, "movzx", "edx, word ptr [rax + 8]"),
    (0x0055DA6E, "call", "0x3235c0"),
    (0x002F97EB, "mulss", "xmm0, dword ptr [rip + 0x61cb25]"),
    (0x002F97F3, "divss", "xmm0, dword ptr [rip + 0x5f9935]"),
    (0x002F97FB, "cvttss2si", "eax, xmm0"),
    (0x002F97FF, "lea", "eax, [rax + rax*4]"),
    (0x002F9802, "add", "eax, eax"),
]


def extra():
    import struct
    sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "dashboard")))
    from ff12_content import vbf_load_index, vbf_read_entry
    vbf = sys.argv[1] if len(sys.argv) > 1 else r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
    fails = 0
    with open(vbf, "rb") as f:
        names, blocks = vbf_load_index(f)
        packs = sorted(n for n in names if n.endswith("/battle_pack.bin"))
        for n in packs:
            b = vbf_read_entry(f, names, blocks, n)
            o = struct.unpack_from("<I", b, 0x34)[0]
            cnt = struct.unpack_from("<I", b, o + 4)[0]
            ok = b[o:o + 4] == b"st2e" and cnt == 361
            fails += 0 if ok else 1
            print("%s %s licence table count %d" % ("ok  " if ok else "FAIL", n.split("/")[-3], cnt))
    if len(packs) != 9:
        print("FAIL battle_pack copies %d" % len(packs)); fails += 1
    d, off = fp.load_image()
    for va, want in ((0x00916318, 64.0), (0x008F3130, 50.0)):
        got = struct.unpack("<f", d[off(va):off(va) + 4])[0]
        fails += 0 if got == want else 1
        print("%s %08X = %r" % ("ok  " if got == want else "FAIL", va, got))
    return fails


def main():
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fails = 0
    for va, mn, ops in CHECKS:
        ins = next(md.disasm(d[off(va):off(va) + 16], va), None)
        ok = ins is not None and ins.mnemonic == mn and ins.op_str == ops
        fails += 0 if ok else 1
        got = "%s %s" % (ins.mnemonic, ins.op_str) if ins else "<no decode>"
        print("%s %08X %s" % ("ok  " if ok else "FAIL", va, got))
    fails += extra()
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
