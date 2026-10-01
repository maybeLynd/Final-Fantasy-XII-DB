"""fr2_icon_pair.py - FR-2: nothing on PC copies the PS2 icon pair into a save slot (FABLE, Claude Opus 5.5, 2026-09-26;
read by a delegated read-only pass, anchors re-checked here).

  I1 the load: 00582790 requests kind 7 id 0x2C (icon.sys) and id 0x2D (icon1.ico) through 00249210 (r8d = 7 + 0x25 and
     7 + 0x26, 005827FA/00582822). It keeps their data pointers at controller +0x110 and +0x118 (00582814, 0058282F).
  I2 icon.sys is used as a template. SaveSlotMetadata_BuildSubmissionDescriptor 005832B0 loads it from controller
     +0x110 (005832FB), clears a 0x3C4-byte
     image (00583302), stamps "PS2D" (00583307) and writes the three icon names (00583644, 00583675, 005836A5) into
     it: the PS2 icon.sys layout.
  I3 that image goes nowhere. 005832B0's one caller is state 7 of SaveSlotTransaction_StateMachine, which builds it at
     the transaction record's +0xE8 (00581EB7, 00581ED2). State 7's storage call 00581F89 enqueues the data file.
  I4 the icon names are otherwise used only to delete. The slot asset name builder 005837F0 has ten E8 callers. Kind 0
     (icon.sys) is used only at 00581E55, and kinds 2-4 (static.ico) at 00581E87. Each is followed by 005826D0
     (00581E5D, 00581E8F), the storage delete-if-exists (how-a-manual-save-is-committed.md); the other six are the data file and the three descriptor calls.
  I5 no other reference to the name strings or the magic: every rip-relative operand into the icon.sys / static.ico
     literals (00D23EC8..00D23EE4) is in 005837F0 or 00584610, and "PS2D" (00D23F10) has one reference.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
def win(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
L = win(0x582790, 0xC5)
check("I1 00582790 loads kind 7 ids 0x2C and 0x2D into controller +0x110 / +0x118",
      L.get(0x5827FA) == "lea r8d, [rdx + 0x25]" and L.get(0x582803) == "mov edx, 7" and L.get(0x582822) == "lea r8d, [rdx + 0x26]"
      and L.get(0x5827FE) == "call 0x249210" and L.get(0x582826) == "call 0x249210"
      and L.get(0x582814) == "mov qword ptr [rbx + 0x110], rcx" and L.get(0x58282F) == "mov qword ptr [rbx + 0x118], rcx"
      and 7 + 0x25 == 0x2C and 7 + 0x26 == 0x2D)
M = win(0x5832B0, 0x420)
memset_len = [a for a, v in M.items() if a < 0x583302 and v == "mov r8d, 0x3c4"]
check("I2 005832B0 builds a 0x3C4-byte PS2D image and writes the three icon names into it",
      memset_len and M.get(0x583302) == "call 0x861ec0" and M.get(0x5832FB) == "mov r15, qword ptr [rax + 0x110]" and at(0x583307).startswith("mov eax, dword ptr [rip")
      and d[off(0xD23F10):off(0xD23F10) + 4] == b"PS2D" and all(M.get(a) == "call 0x5837f0" for a in (0x583644, 0x583675, 0x5836A5)))
def e8(t):
    out = []; vs, va, rs, ro = secs[0]; k = d.find(b"\xE8", ro)
    while 0 <= k < ro + rs - 5:
        a = BASE + va + k - ro
        if a + 5 + struct.unpack_from("<i", d, k + 1)[0] == t: out.append(a)
        k = d.find(b"\xE8", k + 1)
    return out
check("I3 005832B0's one caller is state 7, which builds it at record +0xE8 and enqueues only the data file",
      e8(0x5832B0) == [0x581ED2] and at(0x581EB7) == "lea rcx, [rbx + 0xe8]" and at(0x581F89) == "call 0x582540")
C = e8(0x5837F0)
check("I4 the slot asset name builder's ten callers: kind 0 only at the delete 00581E55, kinds 2-4 at 00581E87, "
      "three descriptor calls",
      sorted(C) == sorted([0x57F2F5, 0x5810D5, 0x581E1C, 0x581E55, 0x581E87, 0x581EFE, 0x581FC8, 0x583644, 0x583675, 0x5836A5])
      and at(0x581E5D) == "call 0x5826d0" and at(0x581E8F) == "call 0x5826d0",
      str(["%08X" % a for a in C]))
vs, va, rs, ro = secs[0]
cs2 = Cs(CS_ARCH_X86, CS_MODE_64); cs2.skipdata = True
hits = []; magic = []
for x in cs2.disasm(d[ro:ro + rs], BASE + va):
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    if not m: continue
    t = x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
    if 0xD23EC8 <= t < 0xD23EE4: hits.append(x.address)
    if t == 0xD23F10: magic.append(x.address)
ok = all(0x5837F0 <= a < 0x5837F0 + 0x200 or 0x584610 <= a < 0x584610 + 0x200 for a in hits)
check("I5 image-wide, the icon name literals are referenced only from 005837F0 / 00584610, and PS2D once",
      hits and ok and magic == [0x583307], "name refs %s; PS2D refs %s" % (["%08X" % a for a in hits], ["%08X" % a for a in magic]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
