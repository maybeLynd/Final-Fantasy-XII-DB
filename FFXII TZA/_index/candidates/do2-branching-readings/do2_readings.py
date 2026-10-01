"""do2_readings.py - DO-2: every branching verb-handler body is read (FABLE, Claude Opus 5.5, 2026-09-27). Static.

The readings in do2-branching-readings.tsv are prose; this control checks everything in them that the bytes decide.
  D1 the work list: the rows are exactly the distinct BRANCHING bodies of scriptvm-verb-shapes.tsv (primary handlers)
     and members/dispatch-secondary-handler-shapes.tsv (secondary slots) - 293 bodies, each once.
  D2 per body, the branch count equals the conditional jumps in the body, and the condition column cites exactly the
     sites of those jumps, in address order.
  D3 per body, the callee column (addresses outside parentheses) equals the body's direct call/jmp targets outside it,
     with the two VM pop helpers counted separately.
  D4 per body, the pop column equals the PopI (00267E10) / PopF (00267DB0) call sites in address order.
  D5 every row carries a reading and the confidence 'read'.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

V = DB / "01-Script-VM-Native-Bridge/Verb-Dispatch"
work = set()
for l in open(V / "scriptvm-verb-shapes.tsv", encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if len(p) > 5 and p[5] == "BRANCHING": work.add(int(p[3], 16))
for l in open(V / "members/dispatch-secondary-handler-shapes.tsv", encoding="utf-8"):
    if l.startswith("#"): continue
    p = l.rstrip("\n").split("\t")
    if len(p) > 3 and p[3] == "BRANCHING": work.add(int(p[2], 16))
rows = list(csv.DictReader(open(HERE / "do2-branching-readings.tsv", encoding="utf-8"), delimiter="\t"))
hs = [int(r["handler"], 16) for r in rows]
check("D1 the rows are exactly the 293 distinct branching bodies", len(hs) == len(set(hs)) == 293 and set(hs) == work,
      "rows %d, work list %d" % (len(hs), len(work)))

JCC = re.compile(r"^j(?!mp)")
bad = {"D2": [], "D3": [], "D4": [], "D5": []}
for r in rows:
    f = int(r["handler"], 16); sz = SIZES.get(f, 0x100)
    ins = list(cs.disasm(d[off(f):off(f) + sz], f))
    jsites = [x.address & 0xFFFFFF for x in ins if JCC.match(x.mnemonic)]
    cited = [int(m, 16) for m in re.findall(r"\b([0-9A-Fa-f]{6}):", r["conditions"])]
    if str(len(jsites)) != r["branches"].strip() or cited != jsites: bad["D2"].append(r["handler"])
    tg = set(); pops = []
    for x in ins:
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if f <= t < f + sz: continue
            if t == 0x267E10: pops.append("I")
            elif t == 0x267DB0: pops.append("F")
            else: tg.add(t)
    listed = {int(m, 16) for m in re.findall(r"\b([0-9A-Fa-f]{8})\b", re.sub(r"\([^)]*\)", "", r["callees"]))} - {0x267E10, 0x267DB0}
    if listed != tg: bad["D3"].append(r["handler"])
    ap = [a[0].upper() for a in r["args_popped"].replace(",", " ").split() if a != "-"]
    if ap != pops: bad["D4"].append(r["handler"])
    if not r["reading"].strip() or not r["confidence"].startswith("read"): bad["D5"].append(r["handler"])
check("D2 branch counts and cited condition sites match every body", not bad["D2"], str(bad["D2"][:5]))
check("D3 callee sets match every body", not bad["D3"], str(bad["D3"][:5]))
check("D4 pop sequences match every body", not bad["D4"], str(bad["D4"][:5]))
check("D5 every row is read", not bad["D5"], str(bad["D5"][:5]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
