#!/usr/bin/env python3
"""check.py - the control behind re-landing FABLE's fa2f75e21 / 30b2fd926 (SWE2-CONTRACT, 2026-10-03).

Reads the shipping image only; it never reads a database page, so it cannot pass or fail because of the edit it
supports. Five checks, each ends PASS or FAIL, and the run ends FAILS <n>:
  G1  the drain's guard 002E0C8D..002E0C9E is movzx [..+0x3e] / shl al,7 / sar al,7 / or al,[..+0x38] / jne;
  G2  the probe 002E0540 carries the same shl 7 / sar 7 pair over +0x3e at 002E056F..002E0580;
  G3  the device term 0053DD10 is `mov eax, 1; ret`, so `cmove esi, ebp` at 002E0CD6 cannot fire after it;
  G4  the not-ready arm: 002E0B8B calls 00267360 with ecx = 0; on non-zero it zeroes r8b, stores ebp (0, from
      002E09B6) into 0215F1A4 / 0215F1A8 / 0215F1A1 and jumps to 002E0C65, which stores r8b into 0215F1A0;
  S1  sensitivity: the shift pair simulated on a byte with only bit 0 set and on one with only bit 7 set. The
      bit-0 reading predicts (block, dispatch); the reverted bit-7 reading predicts (dispatch, block). The control
      fails if the bytes produce the bit-7 outcome, so it can tell the two readings apart.
"""
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import kit_paths as KP  # noqa: E402

DATA = open(KP.EXE, "rb").read()
PE = struct.unpack_from("<I", DATA, 0x3C)[0]
NSEC = struct.unpack_from("<H", DATA, PE + 6)[0]
OPT = struct.unpack_from("<H", DATA, PE + 20)[0]
BASE = struct.unpack_from("<Q", DATA, PE + 24 + 24)[0]
SECT = PE + 24 + OPT
MD = Cs(CS_ARCH_X86, CS_MODE_64)


def off(va):
    rva = va - BASE
    for i in range(NSEC):
        s = SECT + 40 * i
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", DATA, s + 8)
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return rptr + rva - vaddr
    raise ValueError("unmapped %08X" % va)


def insns(va, n):
    o = off(va)
    return [("%s %s" % (i.mnemonic, i.op_str)).strip() for i in list(MD.disasm(DATA[o:o + 16 * n], va))[:n]]


def at(va):
    return insns(va, 1)[0]


fails = 0


def check(name, ok, detail):
    global fails
    print("%s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    fails += 0 if ok else 1


g1 = insns(0x002E0C8D, 5)
check("G1 drain guard", g1[0].endswith("+ 0x3e]") and g1[1] == "shl al, 7" and g1[2] == "sar al, 7"
      and g1[3].startswith("or al, byte ptr") and g1[3].endswith("+ 0x38]") and g1[4].startswith("jne"), g1)
g2 = insns(0x002E056F, 5)
check("G2 probe 002E0540", g2[0].endswith("+ 0x3e]") and g2[1] == "shl cl, 7" and g2[2] == "sar cl, 7"
      and g2[3].endswith("+ 0x38]") and g2[4].startswith("jne"), g2)
g3 = insns(0x0053DD10, 2)
check("G3 device term", g3 == ["mov eax, 1", "ret"] and at(0x002E0CC9) == "call 0x53dd10"
      and at(0x002E0CCE) == "test eax, eax" and at(0x002E0CD6) == "cmove esi, ebp", g3)
g4 = [at(0x002E09B6), at(0x002E0B89), at(0x002E0B8B), at(0x002E0B92), at(0x002E0B94)] + insns(0x002E0B97, 4) \
    + [at(0x002E0C65)]
ok4 = (g4[0] == "xor ebp, ebp" and g4[1] == "xor ecx, ecx" and g4[2] == "call 0x267360" and g4[3].startswith("je")
       and g4[4] == "xor r8b, r8b" and g4[5].startswith("mov dword ptr [rip") and g4[6].startswith("mov dword ptr [rip")
       and g4[7].startswith("mov byte ptr [rip") and g4[8] == "jmp 0x2e0c65" and g4[9].startswith("mov byte ptr [rip")
       and g4[9].endswith("r8b"))


def rip_target(va):
    o = off(va)
    i = next(MD.disasm(DATA[o:o + 16], va))
    disp = struct.unpack_from("<i", i.bytes, len(i.bytes) - 4)[0]
    return va + i.size + disp


targets = ["%08X" % rip_target(v) for v in (0x002E0B97, 0x002E0B9D, 0x002E0BA3, 0x002E0C65)]
ok4 = ok4 and targets == ["0215F1A4", "0215F1A8", "0215F1A1", "0215F1A0"]
check("G4 not-ready arm discards", ok4, g4 + targets)


def guard(byte3e):
    al = (byte3e << 7) & 0xFF                       # shl al, 7
    al = (al - 0x100 if al & 0x80 else al) >> 7     # sar al, 7 (arithmetic)
    return "block" if (al & 0xFF) else "dispatch"   # | +0x38 (taken as 0) ; jne


outcome = (guard(0x01), guard(0x80))
check("S1 sensitivity", outcome == ("block", "dispatch") and outcome != ("dispatch", "block"),
      "bit0-only -> %s, bit7-only -> %s (the bit-7 reading would predict dispatch, block)" % outcome)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
