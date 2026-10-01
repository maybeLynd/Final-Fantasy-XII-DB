"""motion_pop_pairing.py - the party standard-motion verbs' push/pop pairing and where the -1.0f goes
(SWE2-CONTRACT, 2026-09-30, batch 2 of the DD residue closure; kept in the batch-1 folder beside the shared helpers).
Static. Reads only. Each check asserts the instruction the page cites; exit 1 on any mismatch.

 P1 003580C0 pops int (00267E10) -> r12d, float (00267DB0) -> xmm6, int (00267E10) -> r15d, in that order;
 P2 00267DB0 returns a float in xmm0 (movss / cvtdq2ps) - a pop, not a discard;
 P3 003580C0 passes xmm6 as xmm3 and r15d as r8d, and r12d chooses 003DDB40 (non-zero) or 003DDBB0 (zero);
 P4 003DDB40 / 003DDBB0 move xmm3 to xmm2 and tail-jump 002EB3E0 / 002EB4F0;
 P5 002EB0D0: with its fourth argument zero the blend is compared (comiss) and a blend below the compared value takes
    the 004272E0 call, otherwise 004270A0; with it non-zero 00427860 is called instead.
"""
import sys
import capstone
import block_writer_disjoint as b


def body(at, ext, f, n=None):
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    return ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in md.disasm(at(f, n or ext[f]), f)]


def main():
    at, ext = b.load(), b.extents()
    t = "\n".join(body(at, ext, 0x003580C0))
    d = "\n".join(body(at, ext, 0x00267DB0))
    x = "\n".join(body(at, ext, 0x003DDB40) + body(at, ext, 0x003DDBB0))
    e = "\n".join(body(at, ext, 0x002EB220, 0xB0))
    checks = [
        ("P1", all(s in t for s in ("003580F2 call 0x267e10", "003580FA mov r12d, eax", "003580FD call 0x267db0",
                                     "00358105 movaps xmm6, xmm0", "00358108 call 0x267e10", "0035810D mov r15d, eax"))),
        ("P2", "cvtdq2ps xmm0, xmm0" in d and "movss xmm0" in d),
        ("P3", all(s in t for s in ("0035817A movaps xmm3, xmm6", "0035817D mov r8d, r15d", "00358183 test r12d, r12d",
                                     "00358188 call 0x3ddb40", "0035818F call 0x3ddbb0"))),
        ("P4", "003DDB92 movaps xmm2, xmm6" in x and "003DDBA7 jmp 0x2eb3e0" in x and "003DDC17 jmp 0x2eb4f0" in x),
        ("P5", all(s in e for s in ("002EB23F test esi, esi", "002EB26A call 0x427860", "002EB277 comiss xmm1, xmm6",
                                     "002EB27A jb 0x2eb2a6", "002EB29F call 0x4270a0", "002EB2C9 call 0x4272e0"))),
    ]
    fails = 0
    for n, ok in checks:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
        fails += not ok
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
