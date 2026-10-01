"""f1_thread_reach.py - F-1: on which thread, and from where, is the weather apply 0026D910 called? (FABLE, Claude Opus 5.5,
2026-09-26)

  R1 upward: every direct call, tail jump or conditional jump into 0026D910 or its ancestors, walked to their roots
     through a function-list-independent rel32 index. The roots are exactly three application entries:
     - 0017CCD0, GameApplication's update slot (MainLoop_UpdateAndRenderFrame 0022B8C0 is on the paths);
     - the thunk 0017D150 of GameApplication's setup 0017D000;
     - 003565C0, the setweatherslot script verb (verb table row 0x21A).
  R2 downward: a forward walk from every thread procedure the image starts reaches none of those roots, nor 0026D910.
     The procedures are the eight distinct procedures of the 5 CreateThread and 4 _beginthreadex sites that
     the graphics-handshake page enumerated, and the Tk thread API's own workers.
  R3 control: the same forward walk does reach deep code from the two big workers, so the zero is not an empty walk.
Blind spot, stated as on the handshake page (CG-3): thread procedures dispatched through the guarded trampoline's
ctx+8 and the Tk workers' per-thread callback tables are indirect and not followed.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, collections, csv, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
secs = {struct.unpack_from("<8s", d, pe + 24 + optsz + i * 40)[0].rstrip(b"\0").decode():
        struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8) for i in range(n)}
F = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2])
    except (ValueError, IndexError): pass
ST = sorted(F)
def owner(a):
    i = bisect.bisect_right(ST, a) - 1
    return ST[i] if i >= 0 and a < ST[i] + F[ST[i]] else None
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
vs, va, rs, ro = secs[".text"]; T0 = BASE + va; text = d[ro:ro + rs]
callers = collections.defaultdict(set); callees = collections.defaultdict(set)
for i in range(len(text) - 6):
    b0 = text[i]
    L = 1 if b0 in (0xE8, 0xE9) else 2 if (b0 == 0x0F and 0x80 <= text[i + 1] <= 0x8F) else 0
    if not L: continue
    t = T0 + i + L + 4 + int.from_bytes(text[i + L:i + L + 4], "little", signed=True)
    o = owner(T0 + i)
    if t in F and o is not None and t != o:
        callers[t].add(o); callees[o].add(t)
APPLY = 0x26D910
seen = {APPLY}; fr = [APPLY]; roots = set()
while fr:
    nx = []
    for f in fr:
        cs = callers.get(f, set())
        if not cs: roots.add(f)
        for c in cs:
            if c not in seen: seen.add(c); nx.append(c)
    fr = nx
check("R1 the roots above 0026D910 are the three application entries",
      roots == {0x17CCD0, 0x17D150, 0x3565C0} and 0x22B8C0 in seen, "roots %s; ancestors %d" % (["%08X" % r for r in sorted(roots)], len(seen)))
THREADS = [0x171370, 0x5CCAB0, 0x5CCBA0, 0x7DEC40, 0x7DD950, 0x863500, 0x7A5550, 0x35EA40, 0x368C10, 0x369100, 0x368AE0]
reach = {}
for e in THREADS:
    s = {e}; fr = [e]
    while fr:
        nx = []
        for f in fr:
            for c in callees.get(f, ()):
                if c not in s: s.add(c); nx.append(c)
        fr = nx
    reach[e] = s
hits = {"%08X" % e: sorted("%08X" % h for h in reach[e] & (seen | roots)) for e in THREADS if reach[e] & (seen | roots)}
check("R2 no thread procedure the image starts reaches 0026D910 or any of its ancestors", hits == {}, str(hits))
check("R3 control: the two big workers' walks are deep (hundreds of functions)",
      len(reach[0x35EA40]) > 500 and len(reach[0x369100]) > 500, "%d / %d" % (len(reach[0x35EA40]), len(reach[0x369100])))
print("FAILS", fails)
sys.exit(1 if fails else 0)
