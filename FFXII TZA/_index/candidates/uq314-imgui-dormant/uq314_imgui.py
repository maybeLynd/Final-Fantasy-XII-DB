"""uq314_imgui.py - UQ-314: can the Dear ImGui debug menu be re-enabled at runtime? (FABLE, Claude Opus 5.5, 2026-09-27).
Static.

  I1 the image carries ImGui's IO-constructor filenames (imgui.ini, imgui_log.txt - the positive control) and none of the
     string literals ImGui's frame, window and widget code creates: Debug##Default (NewFrame's implicit window),
     ##Tooltip_, ##Menu_, ##Popup_, ##Combo_, #SCROLLX, #MOVE, #COLLAPSE, #RESIZE. So NewFrame / Begin / Render are not
     linked - only the dormant context object SWE2-EC7 declared (10 members, members/imgui.tsv).
  I2 nothing but start-up and exit reaches those 10 members: over the rel32 index their only callers outside the
     member set are the static-object constructor 00791E70 and the teardown stub 008B7D40, and 00791E70's only caller
     is 00169620, slot 743 of the 1,172-slot CRT initializer table, which constructs the object and registers atexit.
  I3 the script verbs that set the draw-mode-1 gate bits - debug_setdraweffectstatus / debug_setdrawsystemeffectstatus /
     debug_setdrawmenustatus (20A0 / 20A1 / 20A2) - are called by no shipped script (7,564 distinct .ebp files), while
     the same 0x20xx band shows 56 called ids (controls). Skipped, not failed, without the local extract.
  I4 the context object the initializer constructs (02EA58C0) is referenced only by that initializer and its atexit stub,
     and the constructors store no global pointer to it, so no frame code - linked or not - can reach it.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, csv, hashlib, re, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
present = [b"imgui.ini", b"imgui_log.txt"]
absent = [b"Debug##Default", b"##Tooltip_", b"##Menu_", b"##Popup_", b"##Combo_", b"#SCROLLX", b"#MOVE", b"#COLLAPSE", b"#RESIZE"]
check("I1 the IO filenames are present and none of ImGui's frame/window/widget literals is",
      all(d.count(p) == 1 for p in present) and all(d.count(a) == 0 for a in absent),
      "present %s absent-hits %s" % ([d.count(p) for p in present], [d.count(a) for a in absent]))

F1 = DB / "_index/candidates/f1-weather-apply-thread/f1_thread_reach.py"
g = {"__file__": str(F1)}; exec(compile(open(F1, encoding="utf-8").read().split("APPLY = 0x26D910")[0], str(F1), "exec"), g)
members = [int(l.strip(), 16) for l in open(DB / "23-Third-Party-Libraries/members/imgui.tsv", encoding="utf-8") if re.fullmatch(r"[0-9A-Fa-f]{8}\s*", l)]
outside = sorted({c for m in members for c in g["callers"].get(m, ()) if c not in members})
ctor_callers = sorted(g["callers"].get(0x791E70, ()))
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
table = [struct.unpack_from("<Q", d, o)[0] for o in range(off(0x8C31D8), off(0x8C5678), 8)]
init = d[off(0x169620):off(0x169640)]
check("I2 the members are reached from outside only through the static-object constructor 00791E70 and the teardown stub 008B7D40; the constructor's only caller is CRT initializer slot 743 (00169620), which constructs and registers atexit",
      len(members) == 10 and outside == [0x791E70, 0x8B7D40] and ctor_callers == [0x169620] and len(table) == 1172
      and table.index(0x169620) == 743 and not g["callers"].get(0x169620) and 0xE8 in init[:0x10],
      "outside callers %s; 00791E70 callers %s" % (["%08X" % c for c in outside], ["%08X" % c for c in ctor_callers]))

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
cs = Cs(CS_ARCH_X86, CS_MODE_64)
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
RIP = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+)\]")
refs = set(); gstores = []
for f, sz in SIZES.items():
    o = off(f)
    if o is None or sz <= 0 or not (0x121000 <= f < 0x8C0000): continue
    for x in cs.disasm(d[o:o + sz], f):
        m = RIP.search(x.op_str)
        if not m: continue
        t = x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16))
        if 0x2EA58C0 <= t < 0x2EA6500: refs.add(f)
        if f in (0x791E70, 0x791D80, 0x792090) and x.mnemonic.startswith("mov") and x.op_str.startswith(("qword ptr [rip", "dword ptr [rip")): gstores.append(x.address)
check("I4 the context object 02EA58C0 is referenced only by its initializer 00169620 and its atexit stub 008B7DA0, and its constructors store no global pointer to it - no frame code can reach it",
      refs == {0x169620, 0x8B7DA0} and gstores == [] and 0x16962B + 0x2D3C295 == 0x2EA58C0, "refs %s" % sorted("%08X" % r for r in refs))
EX = Path("D:/FFXII_TZA_extract")
if EX.exists():
    U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
    band = collections.Counter(); seen = set()
    for p in sorted(EX.rglob("*.ebp")):
        b = p.read_bytes(); h = hashlib.md5(b).digest()
        if h in seen or len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
        seen.add(h)
        sec = b[0x80:0x80 + U32(b, 0x84)]; diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
        if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
        st = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)); bounds = sorted(set(st) | {diroff, len(sec)})
        for s0 in st:
            code = sec[s0:min((x for x in bounds if x > s0), default=len(sec))]; i = 0
            while i < len(code):
                op = code[i]
                if op > 0x63: break
                if op >= 0x48:
                    if op in (0x58, 0x59, 0x5D, 0x5E) and i + 2 < len(code):
                        v = code[i + 1] | (code[i + 2] << 8)
                        if 0x2000 <= v < 0x3000: band[v] += 1
                    i += 3
                else: i += 1
    check("I3 no shipped script calls 20A0 / 20A1 / 20A2, while 56 ids of the 0x20xx band are called",
          all(band[v] == 0 for v in (0x20A0, 0x20A1, 0x20A2)) and len(band) == 56 and band[0x20A4] >= 1 and band[0x2086] > 1000,
          "distinct ebp %d; band ids %d, calls %d" % (len(seen), len(band), sum(band.values())))
else:
    print("SKIP  I3 D:/FFXII_TZA_extract not present")
print("FAILS", fails)
sys.exit(1 if fails else 0)
