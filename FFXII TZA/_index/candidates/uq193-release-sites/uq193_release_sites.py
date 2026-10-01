"""uq193_release_sites.py - UQ-193: who discharges the caller's responsibility after a presentation-entry release
(FABLE, Claude Opus 5.5, 2026-09-27). Static.

  R1 PresentationEntryReferenceContainer_ReleaseEntryById (0051BA40) has exactly seven direct call sites.
  R2 six of them reset the render record field they released to -1 before any further use:
       00422AD5 (+0xC4, 00422AE4 r14d = -1), 00422BB8 (+0xC8, 00422BBD), 00422C50 (+0xC4, 00422C55 esi = -1),
       00422C7E (+0xC8, 00422C83), 004239A9 (+0xC4, 004239B1), 004245CC (+0xC8, 004245D1).
  R3 the seventh, 0042464E in 00424550, is dominated by the sixth: 00424550 opens by releasing a live +0xC8 and setting
     it to -1 (004245CC / 004245D1), and its later test at 004245FD only reaches 0042464E when +0xC8 != -1. The two calls
     in between (00372280, 00409090) are handed the resource entry and the payload base, never the record, and no
     instruction of 00424550 writes +0xC8 there. So 0042464E cannot see a live id, and the rebuild at 00424798 passes -1.
  R4 why it matters - planted consequence: 0051BA80 admits a new slot only for id -1 (0051BAB3 / 0051BAE4); a
     non -1 id would resolve through 0051F240, which does not test the occupied bit, onto a node whose cached pointer the
     release zeroes (0051F20D). The reset at 004245D1 is what keeps the rebuild on the admission path.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
W = ROOT / "Database/Tools/work"
d = (W / "exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
text = [x for x in secs if x[1] == 0x1000][0]
hits = []
for i in range(text[3], text[3] + text[2] - 5):
    if d[i] == 0xE8:
        va = i - text[3] + text[1] + BASE
        if va + 5 + struct.unpack_from("<i", d, i + 1)[0] == 0x51BA40 and dis(va, va + 5).get(va) == "call 0x51ba40": hits.append(va)
check("R1 seven call sites", hits == [0x422AD5, 0x422BB8, 0x422C50, 0x422C7E, 0x4239A9, 0x4245CC, 0x42464E], str(["%08X" % h for h in hits]))
a = dis(0x422A30, 0x422C20); b = dis(0x422C20, 0x422C90); c = dis(0x423980, 0x4239C0); e = dis(0x424550, 0x424870)
ok2 = (a.get(0x422A81) == "or r14d, 0xffffffff" and a.get(0x422AE4) == "mov dword ptr [rbx + 0xc4], r14d"
       and a.get(0x422BBD) == "mov dword ptr [rbx + 0xc8], r14d"
       and b.get(0x422C35) == "or esi, 0xffffffff" and b.get(0x422C55) == "mov dword ptr [rbx + 0xc4], esi"
       and b.get(0x422C83) == "mov dword ptr [rbx + 0xc8], esi"
       and c.get(0x4239B1) == "mov dword ptr [rbx + 0xc4], 0xffffffff"
       and e.get(0x4245D1) == "mov dword ptr [rdi + 0xc8], 0xffffffff")
check("R2 six sites reset the released field to -1", ok2)
head = dis(0x424583, 0x4245FE)
between = [t for k, t in head.items() if 0x4245D1 < k < 0x4245FD]
calls_rcx = [t for t in between if t.startswith("mov rcx")]
writes = sorted(k for k, t in e.items() if 0x4245D1 < k < 0x424798 and t.startswith("mov dword ptr [rdi + 0xc8]"))
check("R3 the seventh release is dominated by the reset at 004245D1 and cannot see a live id",
      head.get(0x424583) == "cmp dword ptr [rdi + 0xc8], -1" and head.get(0x4245CC) == "call 0x51ba40"
      and head.get(0x4245D1) == "mov dword ptr [rdi + 0xc8], 0xffffffff" and e.get(0x4245FD) == "cmp dword ptr [rdi + 0xc8], -1"
      and e.get(0x424618) == "je 0x424653" and writes == [] and calls_rcx == ["mov rcx, rsi", "mov rcx, rbp"]
      and e.get(0x424798) == "mov edx, dword ptr [rdi + 0xc8]", str(calls_rcx))
f = dis(0x51BA80, 0x51BB10); g = dis(0x51F1F8, 0x51F215); h = dis(0x51F240, 0x51F2CA)
check("R4 the consequence the reset avoids: no re-admission for a non -1 id, zeroed cache, no occupied-bit test",
      f.get(0x51BAB3) == "cmp edx, -1" and f.get(0x51BAE4) == "cmp ebx, -1" and f.get(0x51BAE7) == "jne 0x51bb04"
      and f.get(0x51BB09) == "call 0x51f240" and g.get(0x51F20D) == "mov qword ptr [rbx + 0x18], rbp"
      and h.get(0x51F2A3) == "test byte ptr [rbx], 2" and h.get(0x51F2BB) == "mov rax, qword ptr [rbx + 0x18]"
      and not any(t.startswith("test byte ptr [rbx], 1") for t in h.values()))
print("FAILS", fails)
sys.exit(1 if fails else 0)
