"""G-5: how Magi::Music is driven, and what the exploration<->battle change actually is (OPUS, 2026-09-27). Control. Static.

  M1 THE GAME'S FADE: 002DEE50 (the track-level setter the area-music code calls with 0x78 / 0x7F) -> 001DBCA0 ->
     00210A50 (MusicAudioController, slot +0x00) -> 00218E50 (the instance whose +0x50 is the track) -> 00222B70, which
     calls 007A81F0(handle, level / 127.0, duration / 60.0) - so 0x78 is 2.0 seconds and 0x7F is volume 1.0
  M2 007A81F0 posts driver command 0xE (handle types 2 / 8 / 9) - Sound::SetVolume with a fade in seconds - or the Lay
     queue's 0xD (type 7)
  M3 MAGI MODES ARE THE SOUNDTRACK VERSION: the Config "Music" setter 002DE110 (Original / Reorchestrated / OST) stores
     options +0x0E (mode 2 only when 0017E490 allows it) and calls Audio_SetMode 002DF530 (clamps 0..2) -> 001DBAC0 ->
     ... -> 00222AD0 -> 007A9650, which posts command 0x26 {handle, mode, 4.0}; the driver arm for 0x26 calls 007CAB80,
     the function whose diagnostics say "Music::SyncTo" - a mode change timed to the music (CalcSampleDelay)
  M4 the other Magi::Music transition commands - 0x21 (SetMode), 0x27 (Start), 0x28 (End) - are posted only by
     007EEA00, SEAD's record-driven re-issue wrapper; no game function reaches their posters within four calls
Not claimed: what 007EEA00's records are, i.e. whether authored data ever drives a Magi mode change of its own; what the
4.0 argument measures.
"""
import re, struct, sys, bisect, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64)
_c = {}
def D(f):
    if f not in _c: _c[f] = list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
    return _c[f]
def I(f): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(f)}
def rip_t(f, a):
    x = next(x for x in D(f) if x.address == a); m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
def flt(v): return struct.unpack_from("<f", d, off(v))[0]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

A, B, C, E, F = I(0x2DEE50), I(0x1DBCA0), I(0x210A50), I(0x218E50), I(0x222B70)
check("M1 the game's fade: 002DEE50 -> 001DBCA0 -> 00210A50 -> 00218E50 (track match) -> 00222B70 -> 007A81F0(level/127, dur/60)",
      A.get(0x2DEE65) == "jmp 0x1dbca0" and B.get(0x1DBCD5) == "jmp 0x210a50" and C.get(0x210A53) == "jmp 0x218e50"
      and E.get(0x218E69) == "cmp dword ptr [rcx + 0x50], edx" and E.get(0x218E77) == "jmp 0x222b70"
      and F.get(0x222BBA) == "call 0x7a81f0" and flt(rip_t(0x222B70, 0x222BAA)) == 60.0 and flt(rip_t(0x222B70, 0x222BB2)) == 127.0)
G = I(0x7A81F0)
check("M2 007A81F0 posts driver command 0xE (types 2 / 8 / 9) or the Lay queue's 0xD (type 7)",
      G.get(0x7A82A2) == "mov dword ptr [rax], 0xe" and G.get(0x7A8258) == "mov dword ptr [rax], 0xd"
      and G.get(0x7A8294) == "call 0x7ab460" and G.get(0x7A8246) == "call 0x7bad60")
S, M_, P, R = I(0x2DE110), I(0x2DF530), I(0x222AD0), I(0x7A9650)
arm = BASE + struct.unpack_from("<i", d, off(BASE + 0x68C080) + 0x26 * 4)[0]
armI = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x7AB5C0)}
syncstr = next(p for p in [d.find(b"Music::SyncTo failed to CalcSampleDelay")] if p > 0)
check("M3 Config 'Music' (002DE110, options +0x0E) -> Audio_SetMode -> 007A9650 posts 0x26 {mode, 4.0} -> 007CAB80 (Music::SyncTo)",
      S.get(0x2DE122) == "mov word ptr [rax + 0xe], cx" and S.get(0x2DE12C) == "call 0x17e490" and S.get(0x2DE14B) == "jmp 0x2df530"
      and P.get(0x222B01) == "call 0x7a9650" and flt(rip_t(0x222AD0, 0x222AF4)) == 4.0
      and R.get(0x7A9697) == "mov dword ptr [rax], 0x26" and armI.get(arm + 0x25) == "call 0x7cab80" and syncstr > 0)
calls = collections.defaultdict(set)
for ch, vs, va, rs, ro in SECS:
    if ch & 0x20000000:
        for p in range(ro, ro + rs - 5):
            if d[p] in (0xE8, 0xE9):
                v = BASE + va + p - ro; t = v + 5 + struct.unpack_from("<i", d, p + 1)[0]; f = owner(v)
                if f: calls[t].add(f)
posters = collections.defaultdict(set)
for f in calls.get(0x7AB460, ()):
    for x in D(f):
        m = re.fullmatch(r"dword ptr \[\w+\], 0x([0-9a-f]+)", x.op_str)
        if x.mnemonic == "mov" and m and int(m.group(1), 16) in (0x21, 0x26, 0x27, 0x28): posters[int(m.group(1), 16)].add(f)
def up(f, k, seen):
    out = set()
    for g in calls.get(f, ()):
        if g not in seen:
            seen.add(g); out.add(g)
            if k: out |= up(g, k - 1, seen)
    return out
game = {c: sorted(a for f in posters[c] for a in up(f, 3, set()) if a < 0x5E0000) for c in (0x21, 0x27, 0x28)}
check("M4 SetMode / Start / End are posted only by 007EEA00; no game function reaches them within four calls",
      all({g for f in posters[c] for g in calls.get(f, ())} == {0x7EEA00} for c in (0x21, 0x27, 0x28)) and not any(game.values())
      and posters[0x26] == {0x7A9650}, str({hex(c): sorted("%08X" % f for f in posters[c]) for c in posters}))
print("FAILS", fails)
sys.exit(1 if fails else 0)
