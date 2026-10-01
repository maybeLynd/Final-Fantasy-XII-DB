"""bh4_region_callers.py - BH-4: what the external callers of the 0x480000 region call beyond the startup builders
(FABLE, Claude Opus 5.5, 2026-09-26; first measured by a delegated read-only pass, re-derived here).

  Q1 the census: every listed function outside 0x480000..0x500000, decoded whole, and its direct `call rel32` sites
     into the region (and its `jmp rel32` sites, leaving out jumps inside its own body). It reproduces the page: 142 call sites from 45 callers.
  Q2 the builders are the targets of the two startup hubs 0037DF90 and 0037E0F0, including their tail jumps.
  Q3 no call site outside the hubs lands on a builder. Every non-hub target is either in the tail
     004FD4B0..004FF440 or one of three VU helpers (004ECB70, 004825F0, 0048F790). The helpers are called only by the
     two microprograms 00478280 and 0047C360, which sit just below 0x480000.
  Q4 (BH-2) every in-region builder the hubs reach (67, counting their tail jumps) has its object decoded as a row of
     the VIF1 page's vif1-packet-templates.tsv (77 rows), and no row has an unattributed store.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, struct, sys
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
funcs = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
LO, HI = 0x480000, 0x500000
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
calls = []; jmps = []
for f, size in funcs.items():
    if LO <= f < HI or off(f) is None: continue
    for x in cs.disasm(d[off(f):off(f) + size], f):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if x.mnemonic == "jmp" and f <= t < f + size: continue   # a jump inside its own function
            if LO <= t < HI: (calls if x.mnemonic == "call" else jmps).append((f, x.address, t))
callers = {f for f, _, _ in calls}
check("Q1 142 direct call sites into the region from 45 callers", len(calls) == 142 and len(callers) == 45,
      "%d sites, %d callers (+%d jmp sites)" % (len(calls), len(callers), len(jmps)))
HUBS = {0x37DF90, 0x37E0F0}
builders = {t for f, _, t in calls + jmps if f in HUBS}
non = [(f, a, t) for f, a, t in calls + jmps if f not in HUBS]
TAIL = (0x4FD4B0, 0x4FF440 + funcs.get(0x4FF440, 0))
VU = {0x4ECB70, 0x4825F0, 0x48F790}
outside = [(f, a, t) for f, a, t in non if not (TAIL[0] <= t < TAIL[1]) and t not in VU]
vu_callers = {f for f, _, t in non if t in VU}
tail_targets = {t for f, _, t in non if TAIL[0] <= t < TAIL[1]}
check("Q2 the hubs reach the builders", len(builders) >= 65, "%d builders" % len(builders))
check("Q3 no non-hub site reaches a builder; the rest land on the 004FD4B0..004FF440 tail or three VU helpers "
      "called only from 00478280 / 0047C360",
      not ({t for _, _, t in non} & builders) and not outside and vu_callers == {0x478280, 0x47C360},
      "non-hub sites %d, tail targets %d, VU-helper callers %s, other %s" % (len(non), len(tail_targets),
      sorted("%08X" % f for f in vu_callers), ["%08X->%08X" % (a, t) for _, a, t in outside][:5]))
import csv
T = list(csv.DictReader(open(ROOT / "Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/vif1-packet-templates.tsv", encoding="utf-8"), delimiter="\t"))
decoded = {int(r["builder"], 16) for r in T if r.get("builder")}
inreg = {b for b in builders if LO <= b < HI}
unattr = [r["builder"] for r in T if (r.get("unattributed_stores") or "0") not in ("", "0")]
check("Q4 (BH-2) every in-region builder the hubs reach has its object decoded in vif1-packet-templates.tsv, and no row "
      "has an unattributed store",
      inreg <= decoded and not unattr, "in-region builders %d, decoded rows %d, missing %s, unattributed %s"
      % (len(inreg), len(T), sorted("%08X" % b for b in inreg - decoded), unattr[:5]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
