"""uc1_apply_band_257_up.py - OPUS (Claude Opus 5.5), 2026-09-28. OPUS-UC1-POPULATION-CHANGE, third band (bodies above 256 B).
PREPARED, NOT APPLIED: writes uc1-applied-population-257-up.tsv only with --write --go <FRONTIER GO commit>. Conditions (FABLE ruling
812143f1b section 3): ASTRA's extent check (FABLE-REQ-ASTRA-UC1-257-EXTENT, DONE), AUDIT-SPEC's corroboration, FRONTIER's GO.

Rows, from OPUS's band rows (_index/candidates/uc1-band-257-up/uc1-band-257-up-rows.tsv, 458b41480) and FABLE's ruling:
  admit-frontier  00712180 (353 B, clean, L passes). Owner YEBIS (FABLE 10308fd02). Reachability recorded as a BOUND: no literal
                  reference of the searched forms (rel32 call / jmp, jcc rel32 / rel8 at nearest-.pdata linear-decode instruction
                  starts, RIP lea, u64 / u32 VA and RVA) other than the thunk 006DAA30, which itself has none; a computed, encoded or
                  out-of-image entry is not excluded (FABLE-NOTICE-OPUS-00712180-SCOPE, ASTRA-REQ-OPUS-PRESET-REACHABILITY-LIMIT)
  held            00131B50 (clean, but L fails: xmm10 read before write - a continuation candidate, FABLE H1) and the other 48 by
                  their band outcome (28 gate, 16 multi, 3 unaligned-unreferenced, 1 non-leaf without unwind)
Checks:
  C1 tallies: 1 admit, 49 held (28 gate + 16 multi + 3 unaligned-unreferenced + 1 nonleaf-no-unwind + 1 L)
  C3 the admitted body decodes exactly to its end, ending on ret
  C4 it lies in .text and overlaps no listed body, no 1-64 B new body and no 65-256 B admitted body
  C5 it has no jump leaving it and no call (a leaf with no tail transfer)
  C6 the population: 35,064 (after the 65-256 B band) + 1 = 35,065
Exit 1 on a failed check.
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
TEXT = [s for s in SECS if s[0] == b".text"][0]; TLO, THI = B + TEXT[2], B + TEXT[2] + TEXT[1]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
listed = {}
for line in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    if len(q) < 3: continue
    try: a, name, sz = int(q[0], 16), q[1], int(q[2])
    except ValueError: continue
    if name.startswith(("Unwind@", "Catch_All@")): continue
    listed[a] = sz
def applied(fn):
    return [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, fn), encoding="utf-8") if l.strip() and not l.startswith("#") and not l.startswith("kind\t")]
p1, p2 = applied("uc1-applied-population-1-64.tsv"), applied("uc1-applied-population-65-256.tsv")
removed = {int(r[1], 16) for r in p1 if r[0] == "remove-listed"}
extend = {int(r[1], 16): int(r[3], 16) for r in p1 if r[0] == "extend-listed"}
new64 = [(int(r[2], 16), int(r[3], 16)) for r in p1 if r[0] in ("admit-frontier", "split-part")]
new256 = [(int(r[2], 16), int(r[3], 16)) for r in p2 if r[0] == "admit-frontier"]
band = [l.rstrip("\n").split("\t") for l in open(os.path.join(DB, "_index", "candidates", "uc1-band-257-up", "uc1-band-257-up-rows.tsv"), encoding="utf-8") if l.strip()]
hdr, band = band[0], band[1:]; col = {h: i for i, h in enumerate(hdr)}
BOUND = ("frontier; owner YEBIS (FABLE 10308fd02); no literal reference of the searched forms (rel32 call/jmp, jcc rel32/rel8 at "
         "nearest-pdata linear-decode instruction starts, RIP lea, u64/u32 VA and RVA) except the thunk 006DAA30, which has none itself; "
         "a computed, encoded or out-of-image entry is not excluded")
rows = []
for r in band:
    a, nb, oc = int(r[col["start_va"]], 16), int(r[col["bytes"]]), r[col["outcome"]]
    if oc == "clean" and a == 0x712180: rows.append(["admit-frontier", a, a, a + nb, BOUND, "band rows; FABLE ruling 812143f1b s2-s3; ASTRA extent"])
    elif oc == "clean" and a == 0x131B50: rows.append(["held", a, a, a + nb, "L: xmm10 read before written - a continuation candidate", "FABLE ruling 812143f1b H1, s4"])
    else: rows.append(["held", a, a, a + nb, "declared uncertainty (%s)" % oc, "band rows; FABLE ruling 812143f1b s2"])
kinds = {}
for r in rows: kinds[r[0]] = kinds.get(r[0], 0) + 1
hw = [r[4] for r in rows if r[0] == "held"]
check("C1", kinds == {"admit-frontier": 1, "held": 49} and sum("gate" in w for w in hw) == 28 and sum("(multi)" in w for w in hw) == 16
      and sum("unaligned" in w for w in hw) == 3 and sum("nonleaf" in w for w in hw) == 1 and sum(w.startswith("L:") for w in hw) == 1, "tallies %s" % kinds)
adm = [r for r in rows if r[0] == "admit-frontier"]
L = list(cs.disasm(d[off(0x712180):off(0x712180 + 353)], 0x712180))
check("C3", L and L[-1].address + L[-1].size == 0x712180 + 353 and L[-1].mnemonic == "ret", "00712180 decodes exactly to 00712180 + 353, ending on ret")
lst = {a: s for a, s in listed.items() if a not in removed}
spans = sorted([(a, max(a + s, extend.get(a, 0)), "listed") for a, s in lst.items()] + [(lo, hi, "new") for lo, hi in new64 + new256] + [(r[2], r[3], "adm") for r in adm])
bad = [("%08X" % x[0], "%08X" % y[0]) for x, y in zip(spans, spans[1:]) if y[0] < x[1] and "adm" in (x[2], y[2])]
check("C4", all(TLO <= r[2] and r[3] <= THI for r in adm) and not bad, "in .text; overlaps involving the admitted body: %s" % bad)
out_edges = [x for x in L if (x.mnemonic.startswith("j") and x.op_str.startswith("0x") and not 0x712180 <= int(x.op_str, 16) < 0x712180 + 353) or x.mnemonic == "call"]
check("C5", not out_edges, "no jump leaves 00712180 and it makes no call")
before = len(lst) + len(new64) + len(new256); after = before + len(adm)
check("C6", before == 35064 and after == 35065, "population %d -> %d" % (before, after))
if "--write" in sys.argv:
    go = sys.argv[sys.argv.index("--go") + 1] if "--go" in sys.argv else None
    if not go or fails: print("REFUSED  --write needs --go <FRONTIER GO commit> and FAILS 0"); sys.exit(1)
    with open(os.path.join(HERE, "uc1-applied-population-257-up.tsv"), "w", encoding="utf-8", newline="\n") as w:
        w.write("# UC-1 band above 256 B APPLIED 2026-09-29 (OPUS, OPUS-UC1-POPULATION-CHANGE; FRONTIER GO %s). Series break:\n"
                "# figures before this band count 35,064; after it, 35,064 + 1 = 35,065.\n"
                "# Generated by uc1_apply_band_257_up.py. The 49 held rows are declared uncertainty and must be reported every run.\n" % go)
        w.write("kind\tsource_start\tstart\tend\tnote\tauthority\n")
        for r in rows: w.write("%s\t%08X\t%08X\t%08X\t%s\t%s\n" % tuple(r))
    print("written")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
