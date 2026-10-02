"""gi14_check.py - the instructions behind GI-14's answer and the re-correction of 518a7f2d8 (OPUS, 2026-10-01).
FAILS n; refuses if any cited instruction no longer decodes as recorded.

- 008642A0 allocates the 0x68-byte GiPrim object, stores its vtable at +0, and returns object + 8 (008642F8).
- the line emitter 0039D6C0 and the point emitter 0039D970 keep that pointer and store the blend value at its +0x30
  (object +0x38) and 1 at its +0x44 (object +0x4C).
- GiPrim 00863D80 runs with this = the object (its count at +0x60 is the one the constructor 00864210 stores), tests
  +0x4C, passes +0x38 to 001EE650 (the GS ALPHA translator, BC-1) and calls the device's slot +0x78.
- the dword at object +0x30 goes to the device's slot 8, PrimitiveRendererD3D11 006CAEB0 (vtable 00D86960), which
  stores it at renderer +0x208FC.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x008642C5, "mov", "edx, 0x68"),
    (0x008642DE, "mov", "qword ptr [rax], rcx"),
    (0x008642F8, "lea", "rax, [rbx + 8]"),
    (0x00864291, "mov", "dword ptr [rdi + 0x60], esi"),
    (0x0039D78A, "mov", "rbx, rax"),
    (0x0039D84B, "mov", "dword ptr [rbx + 0x44], 1"),
    (0x0039D875, "mov", "qword ptr [rbx + 0x30], rax"),
    (0x0039DA1A, "mov", "rdi, rax"),
    (0x0039DA82, "mov", "dword ptr [rdi + 0x44], 1"),
    (0x0039DAAC, "mov", "qword ptr [rdi + 0x30], rax"),
    (0x00863DB4, "mov", "r14, rcx"),
    (0x00863DCD, "mov", "edx, dword ptr [r14 + 0x60]"),
    (0x00863ED4, "cmp", "dword ptr [r14 + 0x4c], r12d"),
    (0x00863EE6, "mov", "rcx, qword ptr [r14 + 0x38]"),
    (0x00863EFA, "call", "0x1ee650"),
    (0x00863F24, "call", "qword ptr [r10 + 0x78]"),
    (0x00863FF9, "mov", "eax, dword ptr [r14 + 0x30]"),
    (0x00864029, "call", "qword ptr [rbx + 0x40]"),
    (0x006CAEB0, "mov", "eax, dword ptr [rsp + 0x28]"),
    (0x006CAEB7, "mov", "dword ptr [rcx + 0x208fc], eax"),
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
    slot8 = struct.unpack("<Q", d[off(0x00D86960 + 0x40):off(0x00D86960 + 0x48)])[0]
    ok = slot8 == 0x006CAEB0
    fails += 0 if ok else 1
    print("%s PrimitiveRendererD3D11 vtable 00D86960 slot 8 = %08X" % ("ok  " if ok else "FAIL", slot8))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
