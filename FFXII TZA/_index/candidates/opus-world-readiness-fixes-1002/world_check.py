"""world_check.py - the instructions behind the 03-World readiness corrections (OPUS, 2026-10-02). FAILS n.
The trigger's horizontal radius and threshold; the field record accessors' permissive default, bits 4-6 and the
bits 12-13 read; the weather resolver's single draw and slot fallback; the init latch's partial skip; the +0x1061 flag;
the MWeather slot bias; the 0x4000-bound table writer that reaches 01F83530; the 0209A6E8 slot writer and bit base;
the type filter; the pass-1 increment.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x002F8150, "mov", "dword ptr [rsp + 0x54], edi"),
    (0x002F81C1, "mov", "dword ptr [rsp + 0x44], 0"),
    (0x00377728, "xor", "dl, dl"),
    (0x0037772D, "not", "eax"),
    (0x0037773C, "mov", "eax, 1"),
    (0x00377C99, "shr", "eax, 4"),
    (0x00377C9C, "and", "eax, 7"),
    (0x00377BE7, "shr", "edx, 0xc"),
    (0x00377BEA, "and", "edx, 3"),
    (0x0025ABB8, "call", "0x379cd0"),
    (0x002620F7, "jne", "0x2621a8"),
    (0x002621BC, "jmp", "0x3601c0"),
    (0x0026D951, "cmp", "byte ptr [rax + 0x1061], bl"),
    (0x0026DA92, "mov", "byte ptr [rax + 0x1061], 0"),
    (0x003777F9, "lea", "r10d, [r9 - 9]"),
    (0x00210575, "cmp", "cx, ax"),
    (0x00210588, "mov", "qword ptr [rcx + rax*8], rdx"),
    (0x0026E8E1, "mov", "dword ptr [rip + 0x1e2be01], ecx"),
    (0x002F7394, "add", "ecx, 0x17"),
    (0x00466228, "test", "cl, 0xe7"),
    (0x002F7416, "lea", "ebp, [rcx + 1]"),
    (0x0026DA1E, "mov", "edx, dword ptr [rcx + rax*4 + 4]"),
]


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
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
