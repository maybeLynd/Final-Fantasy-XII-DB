"""systemstop08_check.py - SystemStopRecord +0x08 is stored directly by the builder 00227680 in both records (SWE2-STRUCT,
2026-10-03, OPUS-REQ-STRUCT-SYSTEMSTOP-08-1003). Decodes every cited instruction from the shipping image, checks that rbx
is written only once (rbx = r8) before the epilogue pops, and checks the single caller's two record bases.
Refuses (FAILS n) if anything no longer decodes as recorded."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CHECKS = [
    (0x00227686, "xor", "eax, eax"),
    (0x00227698, "mov", "qword ptr [rdx + 8], rax"),
    (0x0022769C, "mov", "rbx, r8"),
    (0x002276A2, "mov", "qword ptr [r8 + 8], rax"),
    (0x002276B0, "mov", "byte ptr [r8 + 0x14], r9b"),
] + [(a, "mov", "qword ptr [rdx + 8], 0xffffffffffffffff") for a in (0x002277A1, 0x0022793E, 0x00227C0E, 0x00227C46, 0x00227C82)] \
  + [(a, "mov", "qword ptr [rbx + 8], 0xffffffffffffffff") for a in (0x002277B0, 0x0022794D, 0x00227C1D, 0x00227C55, 0x00227C91)] + [
    (0x00226C20, "lea", "rax, [rip + 0x1dad539]"),     # 01FD4160, the registry
    (0x00226C27, "lea", "r12, [rax + 0x2a0]"),         # bank B = +0x2A0 (28 records of 0x18)
    (0x00226C37, "lea", "r15, [rax + r10*8]"),         # bank A
    (0x00226C50, "mov", "r8, r12"),
    (0x00226C5A, "mov", "rdx, r15"),
    (0x00226C72, "call", "0x227680"),
]


def main():
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    fails = 0
    for va, mn, ops in CHECKS:
        i = next(md.disasm(d[off(va):off(va) + 16], va), None)
        ok = i is not None and i.mnemonic == mn and i.op_str == ops
        fails += 0 if ok else 1
        print("%s %08X %s %s" % ("ok  " if ok else "FAIL", va, i.mnemonic if i else "?", i.op_str if i else ""))
    writes = [i for i in md.disasm(d[off(0x00227680):off(0x00227CD3)], 0x00227680)
              if i.op_str.startswith("rbx,") and i.mnemonic not in ("cmp", "test")]
    ok = len(writes) == 1 and writes[0].address == 0x0022769C
    fails += 0 if ok else 1
    print("%s rbx written once before the epilogue pops (%s)" % ("ok  " if ok else "FAIL", [hex(w.address) for w in writes]))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
