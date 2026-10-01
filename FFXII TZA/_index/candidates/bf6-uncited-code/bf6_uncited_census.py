"""bf6_uncited_census.py - the citation census BF-6 states, regenerated as a worklist (FABLE, Claude Opus 5.5, 2026-09-26).

BF-6 was closed SUPERSEDED onto "the citation census the row states" without naming a file, so the transfer audit
could not find its destination. This regenerates that census and writes the population it transfers to:

  population  every function in Database/Tools/work/graph/functions.tsv, excluding Unwind@ / Catch_All@ funclets
              (the row's own exclusion);
  cited       a function whose entry or any interior address appears as an 8-hex token in a SYSTEM document: any
              database .md outside _index/ and _experiments/ (so the address index, the audit log, candidate lists and
              receipts, which cite without describing, do not count). The same token rule the neighbour and crossings
              gates use. The wider count (every .md outside _index/_inbox/) is printed beside it for comparison;
  output      uncited_functions.tsv beside this file: every uncited function, largest first, with its domain tag,
              and a summary line with the byte share.
Control: a function the database is known to cite at its entry (00521050, fdm-and-for-entries.md) must count as
cited, and one cited only by an interior address (0031E1D4 inside 0031C5D0) must too.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
funcs = []
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs.append((int(p[0], 16), p[1], int(p[2]), p[3] if len(p) > 3 else ""))
    except (ValueError, IndexError): pass
funcs.sort()
funcs = [f for f in funcs if not (f[1].startswith("Unwind@") or f[1].startswith("Catch_All@"))]
starts = [f[0] for f in funcs]
cited = set()
TOK = re.compile(r"(?<![0-9A-Za-z_])([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")
ndocs = 0
wide = set()
for md in DB.rglob("*.md"):
    if "_inbox" in md.parts: continue
    system = "_index" not in md.parts and "_experiments" not in md.parts
    ndocs += system
    for t in TOK.findall(md.read_text(encoding="utf-8", errors="replace")):
        v = int(t, 16)
        i = bisect.bisect_right(starts, v) - 1
        if i >= 0 and v < funcs[i][0] + max(funcs[i][2], 1):
            wide.add(i)
            if system: cited.add(i)
tot = sum(f[2] for f in funcs)
unc = [f for i, f in enumerate(funcs) if i not in cited]
ub = sum(f[2] for f in unc)
big = [f for f in unc if f[2] >= 2000]
out = Path(__file__).with_name("uncited_functions.tsv")
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("# BF-6 population: functions no database document cites (regenerate with bf6_uncited_census.py)\n")
    fh.write("# %d of %d listed functions uncited by the %d system documents; %d of %d code bytes (%.1f %%); %d uncited functions >= 2,000 B\n"
             % (len(unc), len(funcs), ndocs, ub, tot, 100.0 * ub / tot, len(big)))
    fh.write("# wider count, any .md outside _index/_inbox/: %d functions uncited\n" % (len(funcs) - len(wide)))
    fh.write("entry\tname\tbytes\ttags\n")
    for f in sorted(unc, key=lambda f: -f[2]):
        fh.write("%08X\t%s\t%d\t%s\n" % (f[0], f[1], f[2], f[3][:80]))
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
idx = {f[0]: i for i, f in enumerate(funcs)}
check("C1 an entry-cited function counts as cited (00521050)", idx.get(0x521050) in cited)
check("C2 an interior-cited function counts as cited (0031C5D0 via 0031E1D4)", idx.get(0x31C5D0) in cited)
check("C3 the census wrote its worklist", out.exists() and len(unc) > 0,
      "%d uncited of %d; %.1f %% of %d code bytes; %d >= 2,000 B" % (len(unc), len(funcs), 100.0 * ub / tot, tot, len(big)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
