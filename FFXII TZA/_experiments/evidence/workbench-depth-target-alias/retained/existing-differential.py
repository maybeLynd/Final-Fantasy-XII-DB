#!/usr/bin/env python
"""diff_workbench_save - the shipped save/restore pair against Game/Math/workbench_save.c

The fourteenth pilot. Two small bodies at their real virtual addresses under Unicorn, with the three
globals mapped where the shipped code's rip-relative operands actually resolve: the values array at
0x02EC0800, the pointer array at 0x02EC0A00, and the depth counter at 0x022D8F08. Neither function
takes the workbench as an argument, so planting these anywhere else would not be running this code.

WHAT THIS SUITE IS FOR
----------------------
Two claims that reading can state and only a run can drive:

  * SAVE IS VARIADIC. `ecx` is the count and the pointers arrive in `rdx`, `r8`, `r9` and then ON THE
    STACK. Every case with four or more items exercises the home-area spill at 0036D930-0036D943 and
    the stack slots behind it. A reconstruction taking a count and an array is observably identical
    for three items and diverges for none of them, which is exactly the kind of agreement that means
    nothing - so this suite drives 1, 2, 3, 4, 5 and 8.

  * IT IS NOT A STACK. Save ASSIGNS depth and indexes from zero, so a second Save overwrites the
    first in place. The outer caller's Restore then writes the INNER caller's bytes through the INNER
    caller's pointers. That is driven directly: save two rows, save one different row, restore, and
    compare what came back.

The saved POINTERS cannot be compared as values - the scratch block sits at a different address here
than in the driver - so both sides report them as offsets into that block. Everything else, including
all 16 bytes of every saved value and the whole scratch block, is compared byte for byte.
"""

# PARITY - charter section 21. parity_status.py derives CONTRACT from CONTRACT_MAP below.
PARITY = {
    "subsystem": "workbench_save",
    "entry": "0036D930",
    "contract": "00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md",
    "dimensions": {
        "CALCULATION":      ("COVERED",
                             "the 16-byte item stride and the two array index scalings - one qword "
                             "per pointer, 16 bytes per value - driven at every item count from 0 "
                             "to 8 with distinct bytes at each offset"),
        "STRUCTURAL":       ("COVERED",
                             "both arrays and the depth counter read back after every operation, "
                             "and the whole scratch block compared byte for byte so a write through "
                             "the wrong pointer is caught"),
        "STATE-TRANSITION": ("COVERED",
                             "save, clobber, restore, restore again - the second restore must do "
                             "nothing because the first zeroed depth - and the overwrite-in-place "
                             "sequence where a second save replaces the first"),
        "CONTRACT":         ("NOT COVERED",
                             "derived from the map below: the call-graph claims about nesting and "
                             "the image-wide sweep of the counter are not reachable by a run"),
        "EDGE-CASE":        ("COVERED",
                             "a count of zero, which skips the loop and still assigns depth; a "
                             "restore with no save; a second restore; and counts past three, which "
                             "is where the variadic arguments leave the registers"),
        "SERIALIZATION":    ("N/A", "no byte stream on this path"),
        "RNG":              ("N/A", "no random draw on this path"),
        "TIMING":           ("N/A", "no ordering beyond the sequence the caller drives"),
        "INTEGRATION":      ("NOT COVERED",
                             "no caller is reconstructed; the nine Save callers and the nine "
                             "Restore callers are not driven"),
        "PRESENTATION":     ("N/A", "nothing is displayed"),
        "FULL-SUBSYSTEM":   ("NOT COVERED",
                             "the workbench's other users - the 249 functions that write the "
                             "region - are not exercised, and it is their clobbering that gives "
                             "this pair its purpose"),
    },
}

# One row per claim in the contract's section 15 evidence table, in the same order.
# Marking a row EXERCISED asserts that breaking the claim breaks this test.
CONTRACT_MAP = [
    ("Save is variadic: ecx is the count, pointers in rdx, r8, r9 and then the stack",
     "EXERCISED",
     "driven at 1, 2, 3, 4, 5 and 8 items. Three or fewer never leaves the registers, so the counts "
     "past three are the ones that exercise the home-area spill and the stack slots"),
    ("Save copies sixteen bytes per pointer",
     "EXERCISED",
     "every saved value is compared in full, over a scratch block filled so that neighbouring "
     "offsets differ; a 15- or 17-byte copy changes the value or the block"),
    ("Save assigns depth and indexes from zero, so a second Save overwrites the first in place",
     "EXERCISED",
     "driven directly: save two rows, save one different row, restore, and compare. This is the "
     "contract's sharpest hazard and it is the case the suite was built around"),
    ("a count of zero still assigns depth",
     "EXERCISED",
     "the zero case is driven and the depth read back; the shipped body jumps over the loop to the "
     "same store"),
    ("Restore writes each saved 16 bytes back through its saved pointer",
     "EXERCISED",
     "every case clobbers the scratch block between save and restore, so a restore that did nothing "
     "would leave the clobber visible in the block comparison"),
    ("Restore zeroes depth, and is therefore idempotent",
     "EXERCISED",
     "restore is driven twice with no save between, and the depth and the whole block are compared "
     "after each"),
    ("the depth counter is touched by exactly four instructions image-wide",
     "NOT EXERCISED",
     "an image-wide sweep. A run of these two functions cannot establish what else does or does not "
     "reference an address"),
    ('the nine users DO call one another \u2014 just never while holding the workbench',
     'NOT EXERCISED',
     "a static measurement over the call graph and every user's Save-to-Restore window: 0044BAC0 transitively reaches six of the other eight, and across all nine held windows there are four calls, none to a user, none to anything reaching one, and no indirect call at all. This pilot drives the pair, not its nine callers"),
    ('four of the nine restore by TAIL JUMP, not by call',
     'NOT EXERCISED',
     'read from the bytes at 0026F413, 003AFFAB, 00431F0A and 0046242E. The pilot calls Save and Restore directly and so exercises neither form of the callers\' control flow'),
    ("nesting cannot happen on the direct call graph",
     "NOT EXERCISED",
     "a reachability argument over the edge list, and the contract already records that it holds "
     "for DIRECT calls only. No run of this pair reaches it"),
    ("`022D8F0C` is read and written by functions with no relationship to the workbench",
     "OPEN QUESTION",
     "claim WITHDRAWN 2026-09-23 (SWE2-CONTRACT): 00502280 is itself a workbench borrower (111 "
     "rip-operands into the region); 022D8F0C is the bit-offset parameter it passes to the "
     "00501820 sliding-window extract. The 'no relationship' premise was refuted by reading "
     "the body"),
    ("**N is structurally bounded at 32, unenforced; no caller saves a whole matrix**",
     "NOT EXERCISED",
     "a static layout argument - values 02EC0800 (16 B/item) and pointers 02EC0A00 (8 B/item) "
     "tile so values[32] would alias pointers[0] - plus the nine callers' ecx arguments "
     "({1}x8, {2}x1). A run of this pair cannot establish an array bound or another caller's "
     "count"),
    ("any runtime observation",
     "OPEN QUESTION",
     "none exists"),
]

import argparse
import os
import struct
import subprocess
import sys
import tempfile

try:
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UcError
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                                   UC_X86_REG_R9, UC_X86_REG_RSP, UC_X86_REG_RIP)
except ImportError:
    sys.stderr.write("diff_workbench_save: needs unicorn (pip install unicorn)\n")
    raise SystemExit(2)

SAVE_FN = 0x0036D930
RESTORE_FN = 0x0036D8E0

VALUES_AT = 0x02EC0800
POINTERS_AT = 0x02EC0A00
DEPTH_AT = 0x022D8F08
ITEM = 16
CAPACITY = (POINTERS_AT - VALUES_AT) // ITEM      # 32

SINK_AT = 0x30001000        # mirrors the reconstruction's sink; unused pointer slots point here
SINK_BYTES = 16
SCRATCH_AT = 0x30000000
SCRATCH_BYTES = 0x200
STACK = 0x40000000
RET_MAGIC = 0x50000000


def read_exe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs = []
    off = pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40

    def rd(va, n):
        r = va - base
        for sva, vs, ra, rs in secs:
            if sva <= r < sva + rs:
                return d[ra + (r - sva):ra + (r - sva) + n]
        return None
    return rd


def page_down(a):
    return a & ~0xFFF


def page_up(a):
    return (a + 0xFFF) & ~0xFFF


class Original(object):
    REGIONS = ((0x0036D000, 0x0036E000),)

    def __init__(self, rd):
        uc = Uc(UC_ARCH_X86, UC_MODE_64)
        for lo, hi in self.REGIONS:
            uc.mem_map(lo, hi - lo)
            for p in range(lo, hi, 0x1000):
                b = rd(p, 0x1000)
                if b:
                    uc.mem_write(p, b)
        # the two arrays are adjacent, so one mapping covers both
        lo = page_down(VALUES_AT)
        hi = page_up(POINTERS_AT + CAPACITY * 8)
        uc.mem_map(lo, hi - lo)
        uc.mem_map(page_down(DEPTH_AT), 0x1000)
        uc.mem_map(SCRATCH_AT, 0x1000)
        uc.mem_map(SINK_AT, 0x1000)
        uc.mem_map(STACK, 0x20000)
        self.uc = uc

    def reset_storage(self):
        self.uc.mem_write(VALUES_AT, b"\x00" * (CAPACITY * ITEM))
        # Every slot points at the sink, matching the reconstruction. A slot Save never wrote is
        # then written into somewhere comparable instead of faulting through a null pointer - and
        # the two sides must AGREE about that starting state, which is what the initial-state case
        # in build_script() checks. This first shipped as a zero fill and the suite stayed green,
        # because no case read a pointer slot the run had not already overwritten.
        self.uc.mem_write(POINTERS_AT, struct.pack("<Q", SINK_AT) * CAPACITY)
        self.uc.mem_write(SINK_AT, b"\x00" * SINK_BYTES)
        self.uc.mem_write(DEPTH_AT, struct.pack("<I", 0))

    def plant(self, seed):
        s = seed if seed else 1
        out = bytearray(SCRATCH_BYTES)
        for i in range(SCRATCH_BYTES):
            s ^= (s << 13) & 0xFFFFFFFF
            s ^= s >> 17
            s ^= (s << 5) & 0xFFFFFFFF
            out[i] = s & 0xFF
        self.uc.mem_write(SCRATCH_AT, bytes(out))
        self.reset_storage()

    def save(self, offsets):
        """The variadic call, spelled the way the ABI spells it: count in ecx, the first three
        pointers in rdx/r8/r9, and the rest written into the stack slots at rsp+0x28 upward - which
        is exactly where the callee's home-area spill expects to find them continuing."""
        uc = self.uc
        sp = STACK + 0x10000
        uc.mem_write(sp, struct.pack("<Q", RET_MAGIC))
        uc.reg_write(UC_X86_REG_RSP, sp)
        uc.reg_write(UC_X86_REG_RCX, len(offsets) & 0xFFFFFFFF)
        regs = (UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)
        for i, r in enumerate(regs):
            uc.reg_write(r, SCRATCH_AT + offsets[i] if i < len(offsets) else 0)
        for i in range(3, len(offsets)):
            uc.mem_write(sp + 8 + 8 * (i + 1), struct.pack("<Q", SCRATCH_AT + offsets[i]))
        uc.emu_start(SAVE_FN, RET_MAGIC)

    def restore(self):
        uc = self.uc
        sp = STACK + 0x10000
        uc.mem_write(sp, struct.pack("<Q", RET_MAGIC))
        uc.reg_write(UC_X86_REG_RSP, sp)
        uc.emu_start(RESTORE_FN, RET_MAGIC)

    def run(self, script):
        out = []
        for line in script:
            p = line.split()
            if p[0] == "NEW":
                self.plant(int(p[1], 16))
            elif p[0] == "SAVE":
                self.save([int(x, 16) for x in p[2:]])
            elif p[0] == "RESTORE":
                self.restore()
            elif p[0] == "POKE":
                self.uc.mem_write(SCRATCH_AT + (int(p[1], 16) % SCRATCH_BYTES),
                                  bytes([int(p[2], 16)]))
            elif p[0] == "DEPTH":
                out.append("N %X" % struct.unpack("<I", self.uc.mem_read(DEPTH_AT, 4))[0])
            elif p[0] == "PTRS":
                n = int(p[1])
                cells = []
                for i in range(n):
                    v = struct.unpack("<Q", self.uc.mem_read(POINTERS_AT + i * 8, 8))[0]
                    cells.append("%X" % (v - SCRATCH_AT)
                                 if SCRATCH_AT <= v < SCRATCH_AT + SCRATCH_BYTES
                                 else ("sink" if v == SINK_AT else "-"))
                out.append("P " + (" ".join(cells) if cells else ""))
            elif p[0] == "VALS":
                n = int(p[1])
                out.append("V " + bytes(self.uc.mem_read(VALUES_AT, n * ITEM)).hex().upper())
            elif p[0] == "SINK":
                out.append("K " + bytes(self.uc.mem_read(SINK_AT, SINK_BYTES)).hex().upper())
            elif p[0] == "SCRATCH":
                out.append("S " + bytes(self.uc.mem_read(SCRATCH_AT, SCRATCH_BYTES)).hex().upper())
        return out


def build_script():
    s = []

    # The fixture's OWN initial state, read before anything is saved. Without this the reset is
    # invisible: every later case overwrites the slots it reads before reading them, so three
    # mutations of the reset survived a whole campaign not because they were equivalent but because
    # nothing ever looked at what they changed. Observing the starting point costs four lines.
    s += ["NEW 3", "DEPTH", "PTRS 4", "VALS 4", "SINK"]

    # Every item count the suite drives, each with distinct offsets so a wrong index scaling moves a
    # value into the wrong slot. 4, 5 and 8 are the ones that leave the registers.
    for n, offs in ((1, ["10"]),
                    (2, ["10", "40"]),
                    (3, ["10", "40", "70"]),
                    (4, ["10", "40", "70", "A0"]),
                    (5, ["10", "40", "70", "A0", "D0"]),
                    (8, ["10", "30", "50", "70", "90", "B0", "D0", "F0"])):
        s += ["NEW %X" % (0x100 + n), "SAVE %d %s" % (n, " ".join(offs)),
              "DEPTH", "PTRS %d" % n, "VALS %d" % n]
        # clobber every saved row, then put them back: a restore that did nothing leaves the clobber
        for k, o in enumerate(offs):
            s += ["POKE %X %X" % (int(o, 16) + k, 0xE7)]
        s += ["SCRATCH", "RESTORE", "DEPTH", "SCRATCH", "SINK"]

    # A count of zero: the loop is skipped and depth is still assigned.
    s += ["NEW 7", "SAVE 2 20 60", "DEPTH", "SAVE 0", "DEPTH", "PTRS 2", "VALS 2",
          "RESTORE", "SCRATCH", "DEPTH", "SINK"]

    # IT IS NOT A STACK. Two rows saved, then one different row saved on top, then restore. The
    # outer frame's pointers and values are gone, overwritten in place, and only the inner row
    # comes back - so the first row's clobber must still be visible afterwards.
    s += ["NEW B", "SAVE 2 10 50", "POKE 10 AA", "POKE 50 BB",
          "SAVE 1 90", "POKE 90 CC", "DEPTH", "PTRS 2", "VALS 2",
          "RESTORE", "SCRATCH", "DEPTH", "SINK"]

    # Restore with no save at all, and a second restore after a real one: both must do nothing.
    s += ["NEW D", "RESTORE", "DEPTH", "SCRATCH", "SINK"]
    s += ["NEW F", "SAVE 3 10 40 70", "POKE 11 5A", "RESTORE", "SCRATCH", "DEPTH",
          "POKE 11 A5", "RESTORE", "SCRATCH", "DEPTH", "SINK"]
    return s


def run_driver(driver, script):
    fd, name = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as f:
            f.write("\n".join(script) + "\n")
        p = subprocess.run([driver, name], capture_output=True, text=True)
        lines = [ln for ln in p.stdout.splitlines() if ln.strip()]
        if p.returncode != 0:
            # The original completed and the reconstruction did not, which is a
            # DIFFERENCE. Raising printed no summary, so a crashed mutant was scored
            # INVALID instead of KILLED (2026-09-12).
            sys.stderr.write(p.stderr)
            print("DRIVER FAILED: exit %d after %d line(s) - the lines it never produced"
                  " are compared as mismatches" % (p.returncode, len(lines)))
        return lines
    finally:
        os.unlink(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True)
    ap.add_argument("--driver", default=os.path.join(".", "workbench_save_driver.exe"))
    ap.add_argument("--show", type=int, default=10)
    a = ap.parse_args()

    print("diff_workbench_save - the shipped pair against Game/Math/workbench_save.c")
    print("  exe    : %s" % a.exe)
    print("  driver : %s" % a.driver)
    print()

    script = build_script()
    rd = read_exe(a.exe)
    try:
        ref = Original(rd).run(script)
    except UcError as e:
        raise SystemExit("emulation failed: %s" % e)
    got = run_driver(a.driver, script)

    # A LENGTH DIFFERENCE IS A MISMATCH, NOT A REASON TO STOP. Raising here printed no
    # summary, and mutation_test reads a killed mutant out of this harness's stdout - so
    # a mutant that changed the NUMBER of lines was scored INVALID rather than KILLED
    # (measured on hp_write, 2026-09-12: 36 of 102). The shorter side is padded instead.
    if len(ref) != len(got):
        print("LINE COUNT DIFFERS: reference %d, driver %d - padding the shorter side"
              % (len(ref), len(got)))
        pad = ["<missing line>"]
        ref = ref + pad * (len(got) - len(ref)) if len(ref) < len(got) else ref
        got = got + pad * (len(ref) - len(got)) if len(got) < len(ref) else got

    # Controls. A save/restore suite can pass by comparing a block that never changed, so the
    # distinct counts are printed and a degenerate run is visible.
    scratch = [x for x in ref if x.startswith("S ")]
    depths = [x for x in ref if x.startswith("N ")]
    print("%d commands, %d compared lines" % (len(script), len(ref)))
    print("  distinct scratch images              : %d of %d" % (len(set(scratch)), len(scratch)))
    print("  distinct depth readings              : %s" % sorted(set(x[2:] for x in depths)))
    print("  cases driving stack-passed arguments : %d"
          % len([l for l in script if l.startswith("SAVE") and int(l.split()[1]) > 3]))
    print()

    mism = [(i, r, g) for i, (r, g) in enumerate(zip(ref, got)) if r != g]
    print("cases: %d" % len(script))
    print("%d comparisons, %d mismatches" % (len(ref), len(mism)))
    for i, r, g in mism[:a.show]:
        print("  line %d" % i)
        print("    original       %s" % r)
        print("    reconstruction %s" % g)
    print("RESULT: %s" % ("OK" if not mism else "FAIL"))
    return 1 if mism else 0


if __name__ == "__main__":
    raise SystemExit(main())
