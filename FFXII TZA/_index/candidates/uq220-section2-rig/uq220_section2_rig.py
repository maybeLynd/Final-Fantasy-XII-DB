"""uq220_section2_rig.py - UQ-220: FCP section 2 is the character's rig, the table of seventeen controllers
(FABLE, Claude Opus 5.5, 2026-09-26; the join first proposed by a delegated read-only pass, re-checked here).

  R1 the copy. 00372820 stores the @FTR allocation at resource entry +0x84 (00372986) and the 16-aligned core size at
     +0x90 (00372969). It stores +0x94 = resolve(+0x84) + [+0x90] (00372991, 003729A9) and memcpy's the FCP tail into
     resolve(+0x94) (003729B4-003729BD). SWE2-DATA (2026-09-21) proved the source is payload + word[+4], section 2.
  R2 the handoff. 003713C0 (called at 003729CA) recomputes +0x94 the same way (0037144E-00371469) and passes
     resolve(+0x94) to 003E1C50 (00371479-00371487).
  R3 the slot initialiser. 003E1C50 walks the section-2 slot table in place. For each slot it initialises it takes
     the slot dword, calls that slot's own init on rig + slotOffset (`lea edx, [rdi + rax]`), and stores null for an
     empty slot. It initialises slots 0-3 and 5-16. It never addresses +0x10 (slot 4), +0x44 (17) or +0x48 (18).
     Positive control: +0x40 (slot 16) is addressed.
  R4 the rig page's reader is the same field. The lip-flap wrapper 0042DD90 takes the rig from the resource entry's
     +0x94 (0042DDE4) and passes controller index 9 to the switch 003E1610 (0042DE0F/0042DE23). The switch bounds the
     index at 0x10 (003E1610), which is seventeen controllers.
  R5 the shipped data, all 1,066 .cm @FCP blocks in the extract:
     - slots 17 and 18 are zero in every block;
     - slot 4 is non-zero in 52 blocks (chara 17, npc 24, monster 11), although no initialiser addresses it;
     - weapons populate only slots 0 and 11, and `high` models only 0 and 10 (the eyes).
So section 2's slot n is the rig's controller n (n = 0..16), which the rig page names. Slots 17 and 18 exist in the
table format and are empty in every shipped file.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, re, struct, sys
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
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
def txt(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in ins(a, size)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
A = txt(0x372820, 0x200)
check("R1 00372820: +0x84 allocation, +0x90 core size, +0x94 = +0x84 + +0x90, memcpy into +0x94",
      A.get(0x372986) == "mov dword ptr [rsi + 0x84], eax" and A.get(0x372969) == "mov dword ptr [rsi + 0x90], ebx"
      and A.get(0x372991) == "add eax, dword ptr [rsi + 0x90]" and A.get(0x3729A9) == "mov dword ptr [rsi + 0x94], eax"
      and A.get(0x3729B4) == "mov rcx, rax" and A.get(0x3729BD) == "call 0x861eba" and A.get(0x3729CA) == "call 0x3713c0")
H = txt(0x3713C0, 0xD0)
check("R2 003713C0 recomputes +0x94 and hands it to 003E1C50",
      H.get(0x37144E) == "mov ecx, dword ptr [rbx + 0x84]" and H.get(0x371469) == "mov dword ptr [rbx + 0x94], eax"
      and H.get(0x371479) == "mov ecx, dword ptr [rbx + 0x94]" and H.get(0x371487) == "call 0x3e1c50")
L = ins(0x3E1C50, 0xBB0)
cur = None; init = {}; addressed = set()
for k, x in enumerate(L):
    for m in re.finditer(r"\[rdi(?: \+ (0x[0-9a-f]+|\d+))?\]", x.op_str):
        addressed.add(int(m.group(1) or "0", 0))
    m = re.match(r"dword ptr \[rdi(?: \+ (0x[0-9a-f]+|\d+))?\]$", x.op_str.split(", ")[-1]) if x.mnemonic == "mov" and x.op_str.startswith("ecx, ") else None
    if m: cur = int(m.group(1) or "0", 0)
    if x.mnemonic == "lea" and x.op_str == "edx, [rdi + rax]" and cur is not None:
        init[cur // 4] = next(y.op_str for y in L[k:k + 3] if y.mnemonic == "call")
check("R3 003E1C50 initialises slots 0-3 and 5-16 on rig + slotOffset",
      sorted(init) == [0, 1, 2, 3] + list(range(5, 17)), " ".join("%d:%s" % (s, c[2:]) for s, c in sorted(init.items())))
check("R3 003E1C50 never addresses +0x10, +0x44 or +0x48; control: +0x40 is addressed",
      not ({0x10, 0x44, 0x48} & addressed) and 0x40 in addressed)
W = txt(0x42DD90, 0xC0); S = txt(0x3E1610, 0x10)
check("R4 the lip-flap wrapper takes the rig from entry +0x94 and passes controller 9; the switch bounds n at 0x10",
      W.get(0x42DDE4) == "mov ecx, dword ptr [rbx + 0x94]" and W.get(0x42DE0F) == "mov edx, 9"
      and W.get(0x42DE23) == "jmp 0x3e1610" and S.get(0x3E1610) == "cmp edx, 0x10")
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
cms = sorted(EX.rglob("*.cm"))
pres = collections.defaultdict(collections.Counter); tot = collections.Counter()
for p in cms:
    b = p.read_bytes(); i = b.find(b"@FCP")
    pl = b[i + 0x30:i + struct.unpack_from("<I", b, i + 8)[0]]
    cls = p.parts[p.parts.index("in") + 1]; tot[cls] += 1
    o2 = struct.unpack_from("<H", pl, 4)[0]
    for s, v in enumerate(struct.unpack_from("<19I", pl, o2) if o2 else ()):
        if v: pres[cls][s] += 1
every = collections.Counter()
for c in pres: every.update(pres[c])
print("   .cm %d; slots populated (all classes): %s" % (len(cms), " ".join("%d:%d" % (s, every[s]) for s in range(19))))
check("R5 slots 17 and 18 are zero in every one of the 1,066 blocks", len(cms) == 1066 and every[17] == 0 and every[18] == 0)
check("R5 slot 4 is populated in 52 blocks (chara 17, npc 24, monster 11)",
      every[4] == 52 and pres["chara"][4] == 17 and pres["npc"][4] == 24 and pres["monster"][4] == 11)
check("R5 weapons use only slots 0 and 11; high models only 0 and 10",
      set(pres["weapon"]) == {0, 11} and set(pres["high"]) == {0, 10})
print("FAILS", fails)
sys.exit(1 if fails else 0)
