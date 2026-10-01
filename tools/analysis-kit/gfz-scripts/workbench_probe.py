#!/usr/bin/env python3
"""workbench_probe.py - execute 0026EE00 under emulation, with its apparatus kept.

Why this file exists at all
---------------------------
The shared-transform workbench document records a formula *"measured by running it"* -- 168
combinations, zero disagreements -- and the script that ran them **was not kept**. A measurement
whose apparatus is gone cannot be re-run, extended, or checked when a later reading contradicts
it, and `EN-1` is exactly that situation: the byte-wise model fits one argument and fails on 6 of
80 combinations with two.

So the apparatus is a tool now.

What it runs
------------
`0026EE00(out /*rcx*/, a /*rdx*/, b /*r8*/)` with its save/restore pair mapped and executing as
shipped, plus the **fourth argument that arrives through memory** -- the 16 bytes at `022D8F10`,
which the function reads and never writes. A caller that leaves stale bytes there computes
against them, and a probe that forgets to set them is measuring the last run.

What the disassembly says, and why the byte model cannot be right
-----------------------------------------------------------------
The body is 1,560 bytes, but only **8 `imul`** instructions do arithmetic; the rest is byte
scatter through `movd` / `psrldq`. Every one of the eight is fed by **`movsx`** -- sign-extended
**16-bit** operands -- and the four results are stored back as **16-bit words** into the row:

    0026F0A6  movsx eax, dx          0026F17E  mov [022D8F30], bx
    0026F0A9  imul  ebx, eax         0026F193  mov [022D8F34], r11w
                                     0026F1A8  mov [022D8F38], r10w
                                     0026F1B0  mov [022D8F3C], r9w

**So the row is four SIGNED 16-BIT LANES, not sixteen bytes.** That is a structural statement
about the code, and it predicts the anomaly the document could not explain: `row[1]` is the HIGH
byte of lane 0, so `row[1] >= 0x80` makes that lane negative.

`--lanes` tests that prediction against the shipped bytes, on every lane, so the prediction is
confirmed or killed rather than admired.
"""
import argparse
import struct
import sys

try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UcError
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                                   UC_X86_REG_RSP, UC_X86_REG_RIP)
except ImportError:
    sys.stderr.write("workbench_probe: needs unicorn (pip install unicorn)\n")
    raise SystemExit(2)

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from disasm_fn import Image, DEFAULT_EXE

FUNC_VA, FUNC_LEN = 0x0026EE00, 1560
SAVE_VA, SAVE_LEN = 0x0036D8E0, 0x60          # generous; both are short
RESTORE_VA, RESTORE_LEN = 0x0036D930, 0x60
ROW_IN = 0x022D8F10                            # the memory operand, read and never written
WORKBENCH = 0x022D8000                         # the whole workbench page range
SAVE_STORE = 0x02EC0000                        # where the save/restore pair keeps rows
OUT_VA, A_VA, B_VA = 0x40000000, 0x40001000, 0x40002000
STACK = 0x50000000
RET_MAGIC = 0x60000000


def run(img, row16, a_words, b_words):
    """-> the 16 bytes the function stores through `out`, or raises."""
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    page = lambda x: x & ~0xFFF

    for va, ln in ((FUNC_VA, FUNC_LEN), (SAVE_VA, SAVE_LEN), (RESTORE_VA, RESTORE_LEN)):
        base = page(va)
        size = ((va + ln) - base + 0xFFF) & ~0xFFF
        try:
            uc.mem_map(base, size)
        except UcError:
            pass
        code = img.read(va, ln)
        if code is None:
            raise SystemExit("cannot read %08X" % va)
        uc.mem_write(va, code)

    # the workbench itself: BSS, so it starts as zero rather than as file bytes
    uc.mem_map(WORKBENCH, 0x4000)
    # and the pair's OWN storage -- 0036D930 copies saved rows to 02EC0800 / 02EC0A00, which is
    # nowhere near the workbench. Mapping only the workbench faults inside the save, not inside
    # the function under test, which is a good way to misread where the problem is.
    uc.mem_map(SAVE_STORE, 0x4000)
    uc.mem_write(ROW_IN, bytes(row16))

    for va, words in ((OUT_VA, [0, 0, 0, 0]), (A_VA, a_words), (B_VA, b_words)):
        uc.mem_map(va, 0x1000)
        uc.mem_write(va, struct.pack("<4i", *words))

    uc.mem_map(STACK, 0x10000)
    sp = STACK + 0x8000
    uc.mem_write(sp, struct.pack("<Q", RET_MAGIC))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, OUT_VA)
    uc.reg_write(UC_X86_REG_RDX, A_VA)
    uc.reg_write(UC_X86_REG_R8, B_VA)
    uc.mem_map(page(RET_MAGIC), 0x1000)
    uc.mem_write(RET_MAGIC, b"\xF4")
    try:
        uc.emu_start(FUNC_VA, RET_MAGIC, count=2000000)
    except UcError as e:
        raise SystemExit("emulation error at %08X: %s" % (uc.reg_read(UC_X86_REG_RIP), e))
    return bytes(uc.mem_read(OUT_VA, 16))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=DEFAULT_EXE)
    ap.add_argument("--lanes", action="store_true",
                    help="test the prediction that the row is four SIGNED 16-bit lanes")
    a = ap.parse_args()
    img = Image(a.exe)

    zero = [0, 0, 0, 0]
    base_row = [0] * 16
    baseline = run(img, base_row, zero, zero)
    print("baseline: row all zero, both arguments zero -> %s" % baseline.hex())
    print()

    if not a.lanes:
        return 0

    # THE PREDICTION. If the row is four signed 16-bit lanes, then setting the HIGH byte of any
    # lane to >= 0x80 makes that lane negative, and the low byte cannot do it. The document
    # reports byte 1 forcing FFFFFFFF and byte 3 not -- under the lane reading both are high
    # bytes, so either the prediction is wrong or the lane mapping is not what it looks like.
    print("high byte of each lane set to 0x80, everything else zero")
    print("  (lane i's bytes are row[2i] low, row[2i+1] HIGH)")
    print()
    print("  byte | role          | out")
    print("  -----|---------------|--------------------------------")
    for i in range(8):
        row = [0] * 16
        row[i] = 0x80
        out = run(img, row, zero, zero)
        role = "lane %d HIGH" % (i // 2) if i % 2 else "lane %d low " % (i // 2)
        print("   %2d  | %-13s | %s" % (i, role, out.hex()))
    print()
    print("  and the same bytes at 0x7F, which must NOT go negative")
    for i in (1, 3, 5, 7):
        row = [0] * 16
        row[i] = 0x7F
        out = run(img, row, zero, zero)
        print("   %2d  | lane %d HIGH   | %s   (0x7F)" % (i, i // 2, out.hex()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
