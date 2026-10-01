"""bt4_event_slots.py [CA_ROOT] - BT-4: a render event's low 12 bits are the slot of the character's motion
container (.ca, @FRP version 1) that holds the @FMC block the event plays (FABLE, Claude Opus 5.5, 2026-09-27).

Image (static, the authorised exe):
  I1 00424D80 stores its event argument (esi = r9d) into the presentation entry's word +0x31C and the render
     record's +0xCC in the same arm (00424FA4 / 00424FAB).
  I2 PresentationEntry_RebuildDerivedResourcePointers 0041CA70 passes word +0x31A (movsx) and word +0x31C & 0xFFF
     to 004090D0 and stores the result at entry +0x368 (0041CABD..0041CAD2).
  I3 004090D0, version 1: index = a*[+0x30] + b when a < [+0x34], else b; child offset = [frp + index*4 + 0x40].
  P1 the posters of the four speed-rule indices: 0x200D after terminal-status recovery (00301140, 0030127A) and
     after the Spawn placement (00307300, 00307A68, action id 0x1C7 at 00307912); 0x2010 in place of 0x2001 for
     the type-0x1A mount while turbo is on (00305080 at 003050B5, 00303F00 at 0030400A/0030400F); 0x4035 / 0x4036
     from 00426130 (00426164 / 00426171), reached with mode 1 from BattleUnit_EnterPartyCombatStance (flag 1,
     00313415) and BattleUnit_ExitPartyCombatStance (flag 0, 00313493).
  P2 BattleAction_SelectPhasePresentationEvent 0030A370's table 01EEC1F0 (three events per action category):
     category 0 -> 0x203D, 1 -> 0x2009/0x200A, 2 -> 0x200B, 3 -> 0x2031/0x2032, 5 -> 0x2033, 7 -> 0x2048,
     8 -> 0x3009, 9 -> 0x2030; and it returns the row's dword +0x30 as the event (0030A457, 0030A46A).
Corpus (with CA_ROOT, e.g. D:/FFXII_TZA_extract/ps2data/obj_finish/in):
  C1 every version-1 .ca has [+0x30] = 0x50 slots per bank; every non-empty slot 0x00..0x4F holds an @FMC block
     (offsets relative to +0x40), and each slot carries ONE name across all files (rlx_ prefix folded).
  C2 slot 0x0D = revive, 0x10 = c_turbo, 0x35 = active, 0x36 = deact; and the posters' other indices name what
     posts them: 0x08 dead, 0x0B item, 0x0C stn, 0x0E poach, 0x33 steal, 0x3D attack.
  C3 sensitivity: the same census keyed one slot off (index + 1) gives the wrong name at every checked index.
Exit 1 on any FAIL.
"""
import glob, os, re, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[4]
d = (ROOT / "Tools/work/exe/FFXII_TZA.exe").read_bytes()
_pe = struct.unpack_from("<I", d, 0x3C)[0]; _n = struct.unpack_from("<H", d, _pe + 6)[0]; _opt = struct.unpack_from("<H", d, _pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, _pe + 24 + _opt + i * 40 + 8) for i in range(_n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, n=1):
    return ["%s %s" % (x.mnemonic, x.op_str) for x in list(cs.disasm(d[off(a):off(a) + 16 * n], a))[:n]]
def at(a): return ins(a)[0]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

check("I1 00424D80 writes the event to entry +0x31C and render +0xCC",
      at(0x00424DA4) == "mov esi, r9d" and at(0x00424FA4) == "mov word ptr [rdi + 0x31c], si" and at(0x00424FAB) == "mov word ptr [rbx + 0xcc], si")
seq = ins(0x0041CAB2, 7)
check("I2 0041CA70 resolves child(+0x31A, +0x31C & 0xFFF) into entry +0x368",
      seq[:4] == ["movzx r8d, word ptr [rdi + 0x31c]", "mov rcx, rax", "movsx edx, word ptr [rdi + 0x31a]", "and r8d, 0xfff"]
      and seq[4] == "call 0x4090d0" and at(0x0041CAD2) == "mov qword ptr [rdi + 0x368], rax", str(seq[:5]))
v1 = ins(0x004090F2, 6)
check("I3 004090D0 version 1: a*[+0x30] + b if a < [+0x34], child at [+idx*4 + 0x40]",
      v1 == ["mov eax, dword ptr [r9 + 0x30]", "imul eax, edx", "add eax, r8d", "cmp edx, dword ptr [r9 + 0x34]", "cmovb r8d, eax", "movsxd rax, r8d"]
      and at(0x00409107) == "mov edx, dword ptr [r9 + rax*4 + 0x40]")
posts = [(0x0030127A, "mov edx, 0x200d"), (0x00307A68, "mov edx, 0x200d"), (0x00307912, "mov eax, 0x1c7"),
         (0x003050B5, "mov edx, 0x2010"), (0x003050C3, "mov edx, 0x2001"), (0x0030400A, "mov edx, 0x2001"), (0x0030400F, "mov eax, 0x2010"),
         (0x00426164, "mov edx, 0x4035"), (0x00426171, "mov edx, 0x4036"), (0x00313415, "call 0x2ecf10"), (0x00313493, "call 0x2ecf10")]
stance = ins(0x00313400, 12) + ins(0x00313480, 12)
check("P1 the posters of 0x200D, 0x2010, 0x4035 and 0x4036",
      all(at(a) == s for a, s in posts) and "mov edx, 1" in stance and "lea r8d, [rdx + 1]" in stance,
      str([(hex(a), at(a)) for a, s in posts if at(a) != s]))
t = [struct.unpack_from("<III", d, off(0x01EEC1F0) + 12 * i) for i in range(10)]
want = {0: 0x203D, 1: 0x200A, 2: 0x200B, 3: 0x2032, 5: 0x2033, 7: 0x2048, 8: 0x3009, 9: 0x2030}
check("P2 0030A370's table and its +0x30 return",
      all(t[k][2] == v for k, v in want.items()) and t[1][0] == 0x2009 and t[3][0] == 0x2031
      and at(0x0030A457) == "mov eax, dword ptr [rdi + 0x30]" and at(0x0030A46A) == "mov eax, dword ptr [rdi + 0x30]")

if len(sys.argv) > 1:
    names = collections.defaultdict(collections.Counter); nf = 0; nonfmc = 0
    for fn in glob.glob(os.path.join(sys.argv[1], "**", "*.ca"), recursive=True):
        b = open(fn, "rb").read()
        if b[:4] != b"@FRP" or struct.unpack_from("<I", b, 4)[0] != 1: continue
        stride, banks = struct.unpack_from("<II", b, 0x30); n = struct.unpack_from("<I", b, 0xC)[0]
        if stride != 0x50: nonfmc += 1; continue
        nf += 1
        for i in range(min(n, stride)):
            o = struct.unpack_from("<I", b, 0x40 + 4 * i)[0]
            if not o: continue
            p = o + 0x40
            if b[p:p + 4] != b"@FMC": nonfmc += 1; continue
            names[i][re.sub(r"^rlx_", "", b[p + 0x10:p + 0x30].split(b"\0")[0].decode(errors="replace"))] += 1
    one = all(len(c) == 1 for c in names.values())
    check("C1 %d version-1 .ca files: every slot 0x00..0x4F is an @FMC block with one name" % nf, nf > 1000 and nonfmc == 0 and one,
          "multi-named: %s" % {hex(k): dict(v) for k, v in names.items() if len(v) > 1})
    top = {k: v.most_common(1)[0][0] for k, v in names.items()}
    expect = {0x0D: "revive", 0x10: "c_turbo", 0x35: "active", 0x36: "deact", 0x08: "dead", 0x0B: "item",
              0x0C: "stn", 0x0E: "poach", 0x33: "steal", 0x3D: "attack", 0x01: "ready", 0x05: "damage"}
    check("C2 the four speed-rule slots and the posters' other indices", all(top.get(k) == v for k, v in expect.items()),
          str({hex(k): top.get(k) for k in expect}))
    check("C3 sensitivity: keyed one slot off, no expected name survives", not any(top.get(k + 1) == v for k, v in expect.items()))
    with open(Path(__file__).with_name("event-slot-names.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("slot\tkind2_event\tname\tfiles\n")
        for k in sorted(names):
            f.write("0x%02X\t0x%04X\t%s\t%d\n" % (k, 0x2000 | k, top[k], sum(names[k].values())))
print("FAILS", fails)
sys.exit(1 if fails else 0)
