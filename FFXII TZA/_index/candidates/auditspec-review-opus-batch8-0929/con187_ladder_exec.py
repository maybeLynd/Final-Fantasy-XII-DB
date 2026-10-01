"""con187_ladder_exec.py - SWE2-AUDIT-SPEC (batch-8 review, 2026-09-29).

Executes the SHIPPED bytes 002FECA2..002FECB8 (xorps / ucomiss / jp / je ladder of the band builder 002FEB80) under
Unicorn for a truth table over a = xmm7 (00320D70 r9=0) and b = xmm6 (00320D70 r9=1), with ebx pre-cleared as at
002FEB9F. The authored flag is ebx at 002FECB8. CON-187 says: 1 only when a != 0 AND b != 0.
Control: the same harness with the je at 002FECAA patched to a 2-byte nop must turn (a=0, b!=0) into 1 - i.e. the
harness can see the "either component" reading if the bytes said so.
"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RBX, UC_X86_REG_XMM6, UC_X86_REG_XMM7

START, END = 0x002FECA2, 0x002FECB8
code = T.rd(START, END - START)
PAGE = START & ~0xFFF


def run(a, b, patch_je=False):
    c = bytearray(code)
    if patch_je:
        k = 0x002FECAA - START
        assert c[k] == 0x74, "002FECAA is not a short je"
        c[k:k + 2] = b"\x66\x90"
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(PAGE, 0x2000)
    mu.mem_write(START, bytes(c))
    mu.reg_write(UC_X86_REG_RBX, 0)
    f = lambda x: struct.unpack("<I", struct.pack("<f", x))[0]
    mu.reg_write(UC_X86_REG_XMM7, f(a))
    mu.reg_write(UC_X86_REG_XMM6, f(b))
    mu.emu_start(START, END)
    return mu.reg_read(UC_X86_REG_RBX)


nan = float("nan")
cases = [(0.0, 0.0), (0.0, 1.5), (1.5, 0.0), (1.5, 2.5), (-0.0, 2.5), (2.5, -0.0), (nan, 0.0), (0.0, nan), (nan, 2.0)]
bad = 0
print("a      b      ebx   CON-187 (both non-zero)")
for a, b in cases:
    got = run(a, b)
    want = int((a != 0 or a != a) and (b != 0 or b != b))  # NaN compares unordered -> jp path -> treated as non-zero
    bad += got != want
    print("%-6s %-6s %d     %d %s" % (a, b, got, want, "" if got == want else "MISMATCH"))
ctl = run(0.0, 1.5, patch_je=True)
print("control (je 002FECAA -> nop), a=0 b=1.5: ebx=%d (must be 1)" % ctl)
bad += ctl != 1
print("FAILS %d" % bad)
sys.exit(1 if bad else 0)
