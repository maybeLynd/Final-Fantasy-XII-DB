"""HM-1 (OPUS, 2026-09-27): the +0x304 bit 6 that the k = 4 body bind sets on the unit's own record is the LIP FLAP
(rig controller 9), made permanent - not a flag that hides the base model.

  L1 002E3110's k = 4 path: or [rec + 0x304], 0x40 / mov [rec + 0x640], 0 / or [rec + 0x290], 0x2000 (002E31DB..002E31E9);
     its k = 2 path clears the bit (002E3246 and 0xFFFFFFBF)
  L2 the same bit is setkutipakustatus's: its service 002E8570 clears then sets 0x40 (002E85BA, 002E85CC), and the timed
     form 002EDF30 does the same (002EDF57, 002EDF6F)
  L3 the dirty pass's bit-13 step 00429C40 mirrors +0x304 bit 6 into +0x40B bit 5 (00429CFE..00429D13), clears dirty bit
     0x2000 (00429D19) and runs 0042DD90 over the record and its +8 / +0xA links (00429C92, 00429CBB, 00429CD6, 00429CF1)
  L4 0042DD90 tests the source record's +0x304 bit 6 (0042DDFE) and switches rig controller 9 on (0042DE0F mov edx, 9 ->
     jmp 003E1610) or off (0042DE30 mov edx, 9 -> call 003E1350)
  L5 the countdown 0042EE90 only counts a non-zero +0x640 (0042EEB7..0042EEC4), so the timer 0 that k = 4 stores makes the
     state permanent until k = 2 or another writer clears it
Usage: python hm1_lipflap.py [exe] [functions.tsv]
"""
import struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUN = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/graph/functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next((v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs), None)
sizes = {}
for l in open(FUN, encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
I = {}
for f in (0x2E3110, 0x2E8570, 0x2EDF30, 0x429C40, 0x42DD90, 0x42EE90):
    for x in cs.disasm(d[off(f):off(f) + sizes[f]], f): I[x.address] = (x.mnemonic, x.op_str)
fails = 0


def check(name, ok):
    global fails
    print("%s  %s" % ("PASS" if ok else "FAIL", name)); fails += not ok


def at(pc, m, o): return I.get(pc) == (m, o)


check("L1 k = 4 sets +0x304 bit 6 with timer 0 and dirty bit 13; k = 2 clears it",
      at(0x2E31DB, "or", "dword ptr [rcx + 0x304], 0x40") and at(0x2E31E2, "mov", "dword ptr [rcx + 0x640], r12d")
      and at(0x2E31E9, "or", "dword ptr [rcx + 0x290], 0x2000") and at(0x2E3246, "and", "dword ptr [rcx + 0x304], 0xffffffbf"))
check("L2 setkutipakustatus's service and timed form write the same bit",
      at(0x2E85BA, "and", "dword ptr [rcx + 0x304], 0xffffffbf") and at(0x2E85CC, "or", "dword ptr [rcx + 0x304], 0x40")
      and at(0x2EDF57, "and", "dword ptr [rcx + 0x304], 0xffffffbf") and at(0x2EDF6F, "or", "dword ptr [rcx + 0x304], 0x40"))
check("L3 00429C40 mirrors bit 6 into +0x40B bit 5, clears 0x2000 and walks 0042DD90",
      at(0x429CFE, "mov", "eax, dword ptr [rdi + 0x304]") and at(0x429D0B, "shr", "eax, 6") and at(0x429D10, "shl", "al, 5")
      and at(0x429D13, "or", "byte ptr [rdi + 0x40b], al") and at(0x429D19, "and", "dword ptr [rdi + 0x290], 0xffffdfff")
      and at(0x429C92, "call", "0x42dd90") and at(0x429CBB, "call", "0x42dd90"))
check("L4 0042DD90 switches rig controller 9 on or off by that bit",
      at(0x42DDFE, "test", "byte ptr [rax + 0x304], 0x40") and at(0x42DE0F, "mov", "edx, 9") and at(0x42DE23, "jmp", "0x3e1610")
      and at(0x42DE30, "mov", "edx, 9") and at(0x42DE35, "call", "0x3e1350"))
check("L5 the countdown skips a zero timer",
      at(0x42EEA6, "test", "byte ptr [rcx + 0x40b], 0x20") and at(0x42EEB7, "movss", "xmm0, dword ptr [rcx + 0x640]")
      and at(0x42EEBF, "ucomiss", "xmm0, xmm6") and at(0x42EEC4, "je", "0x42eef1"))
print("FAILS", fails); sys.exit(1 if fails else 0)
