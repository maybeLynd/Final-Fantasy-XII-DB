"""uc1_apply_band_1_64.py - OPUS (Claude Opus 5.5), 2026-09-28. OPUS-UC1-POPULATION-CHANGE, authorised by
FRONTIER's GO (OPUS-REQ-FRONTIER-UC1-APPLY-GO-AND-ROW-DISPOSITION, 6ba4b6a91) under FABLE's band ruling section 5,
as amended by sections 6-7 (_index/candidates/uc1-band-ruling-fable-2026-09-25.md).

It writes the CANONICAL APPLIED POPULATION for the 1-64 B band, uc1-applied-population-1-64.tsv, one row per change:
  admit-frontier   a new body joining the EC-7 population AS FRONTIER (unexplained code; not a proven whole function)
  split-part       one of the two bodies the 00125743 block splits into
  extend-listed    a listed entry whose extent grows by its cold tail (no row is added)
  held             a declared uncertainty, reported every run, never dropped
  remove-listed    a listed entry that leaves the population (007EE7F0, adjudicated a false entry)
and checks it. The inputs are the band TSV (a dated 2026-09-25 output, left as written), the frozen function list, and
the certified image. It moves NO reporter: the readers of the population switch to this file separately (DATA).

Checks:
  C1 tallies: 694 admit (007EE7C0 included) + 2 split parts = 696 new bodies; 5 extends; 4 held; 1 removal
  C2 007EE7C0 is admitted at 57 B [007EE7C0, 007EE7F9) (section 7), and 007EE7F0 is a listed non-funclet entry
  C3 the split parts: [00125743, 00125753) and [00125753, 00125764), each ending in its own ret
  C4 every new body lies in .text, overlaps no listed body (after the removal), no extension and no other new body
  C5 each extension's tail starts at or after its listed predecessor's end; 007C2A29 carries two extents (section 6):
     instruction [007C23C0, 007C2A2F), native [007C23C0, 007C2A58)
  C6 the population after application: listed 34,270 - 1 = 34,269, plus 696 = 34,965 (INFO: overlap with the
     established 139-body floor)
Exit 1 on a failed check.
"""
import bisect, hashlib, os, struct, sys
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

# the listed population, exactly as progress.py / check_dispositions count it: non-funclet entries of the frozen list
listed = {}
for line in open(os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    if len(q) < 3 or not q[0][:1].isdigit() and not q[0][:1] in "ABCDEF": continue
    try: a, name, sz = int(q[0], 16), q[1], int(q[2])
    except ValueError: continue
    if name.startswith(("Unwind@", "Catch_All@")): continue
    listed[a] = sz
band = [l.rstrip("\n").split("\t") for l in open(os.path.join(DB, "_index", "candidates", "uc1-band-1-64-fable-2026-09-25.tsv"),
        encoding="utf-8") if l.strip() and not l.startswith("#")]
hdr, band = band[0], band[1:]
col = {h: i for i, h in enumerate(hdr)}
rows = []
for r in band:
    a, nb, pred, rul = int(r[col["start_va"]], 16), int(r[col["bytes"]]), int(r[col["prev_entry"]], 16), r[col["ruling"]]
    if rul == "admit":
        if a == 0x7EE7C0: nb = 57   # section 7: admitted at 57 B, not the TSV's 48
        rows.append(("admit-frontier", a, a, a + nb, "", "band TSV" + ("; extent per ruling s7" if a == 0x7EE7C0 else "")))
    elif rul == "split":
        rows.append(("split-part", a, 0x125743, 0x125753, "", "ruling s3 / ASTRA uc1-band-ruling"))
        rows.append(("split-part", a, 0x125753, 0x125764, "", "ruling s3 / ASTRA uc1-band-ruling"))
    elif rul == "extend-predecessor":
        if a == 0x7C2A29:
            rows.append(("extend-listed", pred, pred, 0x7C2A2F, "native to 007C2A58", "ruling s6 point 2"))
        else:
            rows.append(("extend-listed", pred, pred, a + nb, "", "band TSV"))
    elif rul == "hold-ambiguous":
        rows.append(("held", a, a, a + nb, "declared uncertainty", "band TSV"))
rows.append(("remove-listed", 0x7EE7F0, 0x7EE7F0, 0x7EE7F0 + listed.get(0x7EE7F0, 0), "false entry", "ruling s7; OPUS f8d908ace, two ACCEPTs"))
kinds = {}
for r in rows: kinds[r[0]] = kinds.get(r[0], 0) + 1
new = [r for r in rows if r[0] in ("admit-frontier", "split-part")]
check("C1", (kinds.get("admit-frontier"), kinds.get("split-part"), len(new), kinds.get("extend-listed"), kinds.get("held"),
             kinds.get("remove-listed")) == (694, 2, 696, 5, 4, 1), "tallies %s" % kinds)
e7 = [r for r in rows if r[1] == 0x7EE7C0][0]
check("C2", e7[2:4] == (0x7EE7C0, 0x7EE7F9) and 0x7EE7F0 in listed, "007EE7C0 [%X, %X); 007EE7F0 listed (%s B)"
      % (e7[2], e7[3], listed.get(0x7EE7F0)))
def ends_ret(lo, hi):
    last = list(cs.disasm(d[off(lo):off(hi)], lo))[-1]
    return last.mnemonic == "ret" and last.address + last.size == hi
check("C3", ends_ret(0x125743, 0x125753) and ends_ret(0x125753, 0x125764), "00125743 (16 B) and 00125753 (17 B) each end in ret")
lst = {a: s for a, s in listed.items() if a != 0x7EE7F0}
ext = {r[1]: r[3] for r in rows if r[0] == "extend-listed"}
spans = sorted([(a, max(a + s, ext.get(a, 0)), "listed") for a, s in lst.items()] + [(r[2], r[3], "new") for r in new])
bad = [(hex(x[0]), hex(y[0])) for x, y in zip(spans, spans[1:]) if y[0] < x[1] and "new" in (x[2], y[2])]
check("C4", all(TLO <= r[2] and r[3] <= THI for r in new) and not bad, "all 696 in .text; overlaps involving a new body: %s" % bad[:5])
okx = all(r[1] in lst and r[2] == r[1] for r in rows if r[0] == "extend-listed")
tails = [(r[1], lst.get(r[1], 0)) for r in rows if r[0] == "extend-listed"]
okx = okx and all(pred + sz <= int(b[col["start_va"]], 16) for (pred, sz), b in
                  zip(tails, [b for b in band if b[col["ruling"]] == "extend-predecessor"]))
check("C5", okx and ext.get(0x7C23C0) == 0x7C2A2F, "5 listed extents grow from their predecessors; 007C2A29 instruction to 007C2A2F")
after = len(lst) + len(new)
floor = [int(l.split("\t")[0], 16) for l in open(os.path.join(DB, "_index", "candidates", "uc1-established-floor-139.tsv"),
         encoding="utf-8") if l[:1].isdigit() or l[:1] in "ABCDEF"]
inband = sum(1 for f in floor if any(r[2] == f for r in new))
check("C6", len(listed) == 34270 and len(lst) == 34269 and after == 34965,
      "listed %d -> %d; after application %d (INFO: %d of the %d established-floor rows are in this band)"
      % (len(listed), len(lst), after, inband, len(floor)))
with open(os.path.join(HERE, "uc1-applied-population-1-64.tsv"), "w", encoding="utf-8", newline="\n") as w:
    w.write("# UC-1 1-64 B band APPLIED 2026-09-28 (OPUS, OPUS-UC1-POPULATION-CHANGE; FRONTIER GO 6ba4b6a91). Series break:\n"
            "# figures before this date count the 34,270 listed bodies; after it, 34,269 listed + 696 frontier = 34,965.\n"
            "# Generated by uc1_apply_band_1_64.py. The held rows are declared uncertainty and must be reported every run.\n")
    w.write("kind\tsource_start\tstart\tend\tnote\tauthority\n")
    for r in rows:
        w.write("%s\t%08X\t%08X\t%08X\t%s\t%s\n" % r)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
