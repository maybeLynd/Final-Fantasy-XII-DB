"""uc1_apply_band_65_256.py - OPUS (Claude Opus 5.5), 2026-09-28. OPUS-UC1-POPULATION-CHANGE, second band, authorised by
FRONTIER's GO (OPUS-REQ-FRONTIER-UC1-BAND-65-256-GO, d50e87938) on FABLE's ruling APPLY IN PART
(_index/candidates/uc1-band-65-256-fable-ruling/README.md, sections 3-4: ASTRA's extent check and AUDIT-SPEC's acceptance met).

It writes the CANONICAL APPLIED POPULATION for the 65-256 B band, uc1-applied-population-65-256.tsv, one row per change:
  admit-frontier   a new body joining the EC-7 population AS FRONTIER (unexplained code; not a proven whole function)
  held             a declared uncertainty, reported every run, never dropped
and records each admitted body's jumps that leave it (the tail transfers FRONTIER's GO names). Inputs: OPUS's band rows
(_index/candidates/uc1-band-65-256/uc1-band-65-256-rows.tsv, as written), the frozen function list, the applied 1-64 B
population, and the certified image. It moves NO reporter: the readers switch to this file separately (DATA).

Checks:
  C1 tallies: 99 admit (the 100 clean rows less 00125770); 21 held = 00125770 (FABLE's U: non-leaf, no unwind entry) + 15 gate
     + 2 multi + 3 unaligned-unreferenced
  C2 00125770 is held for U: its body has a push, and no .pdata entry begins at or covers it
  C3 every admitted body decodes exactly to its end, the last non-padding instruction a ret or an unconditional jmp
  C4 every admitted body lies in .text and overlaps no listed body (after the 1-64 B application's removal and extensions), no
     1-64 B new body and no other admitted body
  C5 the external edges are exactly the three FRONTIER's GO names: 002E4C90 -> 004232D0 (jne at 002E4CCA), 002E5B00 -> 002ED6A0
     (jmp at 002E5B5A), 00708270 -> 0071BB70 (jmps at 00708325 and 00708330; 0071BB70 is a 1-64 B admitted body)
  C6 the population after application: 34,965 (after the 1-64 B band) + 99 = 35,064
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
PD = [s for s in SECS if s[0] == b".pdata"][0]
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
    if len(q) < 3 or not q[0][:1].isdigit() and not q[0][:1] in "ABCDEF": continue
    try: a, name, sz = int(q[0], 16), q[1], int(q[2])
    except ValueError: continue
    if name.startswith(("Unwind@", "Catch_All@")): continue
    listed[a] = sz
prev = [l.rstrip("\n").split("\t") for l in open(os.path.join(HERE, "uc1-applied-population-1-64.tsv"), encoding="utf-8")
        if l.strip() and not l.startswith("#") and not l.startswith("kind\t")]
removed = {int(r[1], 16) for r in prev if r[0] == "remove-listed"}
extend = {int(r[1], 16): int(r[3], 16) for r in prev if r[0] == "extend-listed"}
new64 = [(int(r[2], 16), int(r[3], 16)) for r in prev if r[0] in ("admit-frontier", "split-part")]
band = [l.rstrip("\n").split("\t") for l in open(os.path.join(DB, "_index", "candidates", "uc1-band-65-256", "uc1-band-65-256-rows.tsv"),
        encoding="utf-8") if l.strip()]
hdr, band = band[0], band[1:]
col = {h: i for i, h in enumerate(hdr)}
rows = []
for r in band:
    a, nb, oc = int(r[col["start_va"]], 16), int(r[col["bytes"]]), r[col["outcome"]]
    if oc == "clean" and a == 0x125770:
        rows.append(["held", a, a, a + nb, "U: non-leaf body with no unwind entry", "FABLE ruling s1-s2"])
    elif oc == "clean":
        rows.append(["admit-frontier", a, a, a + nb, "", "band rows; FABLE ruling s3; ASTRA extent check"])
    else:
        rows.append(["held", a, a, a + nb, "declared uncertainty (%s)" % oc, "band rows; FABLE ruling s2"])
kinds = {}
for r in rows: kinds[r[0]] = kinds.get(r[0], 0) + 1
held_why = sorted(r[4] for r in rows if r[0] == "held")
check("C1", kinds == {"admit-frontier": 99, "held": 21} and sum(1 for w in held_why if "gate" in w) == 15
      and sum(1 for w in held_why if "(multi)" in w) == 2 and sum(1 for w in held_why if "unaligned" in w) == 3
      and sum(1 for w in held_why if w.startswith("U:")) == 1, "tallies %s" % kinds)
def pdata_over(v):
    r = v - B
    for i in range(PD[4], PD[4] + PD[3], 12):
        b0, e0, u = struct.unpack_from("<III", d, i)
        if b0 <= r < e0 or b0 == r: return True
    return False
b770 = list(cs.disasm(d[off(0x125770):off(0x125770) + 223], 0x125770))
check("C2", any(x.mnemonic == "push" for x in b770) and not pdata_over(0x125770), "00125770: non-leaf (push) and no .pdata entry at or over it")
def decodes(lo, hi):
    L = list(cs.disasm(d[off(lo):off(hi)], lo))
    if not L or L[-1].address + L[-1].size != hi: return False
    real = [x for x in L if x.mnemonic not in ("int3", "nop")]
    return bool(real) and (real[-1].mnemonic == "ret" or real[-1].mnemonic == "jmp")
adm = [r for r in rows if r[0] == "admit-frontier"]
badd = ["%08X" % r[2] for r in adm if not decodes(r[2], r[3])]
check("C3", not badd, "all 99 decode exactly to their end on ret / jmp; failures %s" % badd)
lst = {a: s for a, s in listed.items() if a not in removed}
spans = sorted([(a, max(a + s, extend.get(a, 0)), "listed") for a, s in lst.items()] + [(lo, hi, "new64") for lo, hi in new64]
               + [(r[2], r[3], "new") for r in adm])
bad = [("%08X" % x[0], "%08X" % y[0]) for x, y in zip(spans, spans[1:]) if y[0] < x[1] and "new" in (x[2], y[2])]
check("C4", all(TLO <= r[2] and r[3] <= THI for r in adm) and not bad, "all 99 in .text; overlaps involving an admitted body: %s" % bad[:5])
edges = []
for r in adm:
    for x in cs.disasm(d[off(r[2]):off(r[3])], r[2]):
        if x.mnemonic.startswith("j") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if not r[2] <= t < r[3]: edges.append((r[2], x.address, x.mnemonic, t))
want = [(0x2E4C90, 0x2E4CCA, "jne", 0x4232D0), (0x2E5B00, 0x2E5B5A, "jmp", 0x2ED6A0), (0x708270, 0x708325, "jmp", 0x71BB70), (0x708270, 0x708330, "jmp", 0x71BB70)]
check("C5", sorted(edges) == sorted(want) and 0x4232D0 in listed and 0x2ED6A0 in listed and any(lo == 0x71BB70 for lo, hi in new64),
      "external edges exactly %s; targets 004232D0 / 002ED6A0 listed, 0071BB70 a 1-64 B admitted body" % ["%08X->%08X" % (e[0], e[3]) for e in edges])
for r in adm:
    tt = sorted({t for s, a, m, t in edges if s == r[2]})
    if tt: r[4] = "tail transfer to " + ", ".join("%08X" % t for t in tt)
before = len(lst) + len(new64); after = before + len(adm)
check("C6", before == 34965 and after == 35064, "population %d -> %d" % (before, after))
with open(os.path.join(HERE, "uc1-applied-population-65-256.tsv"), "w", encoding="utf-8", newline="\n") as w:
    w.write("# UC-1 65-256 B band APPLIED 2026-09-28 (OPUS, OPUS-UC1-POPULATION-CHANGE; FRONTIER GO d50e87938). Series break:\n"
            "# figures before this date count 34,965 (listed 34,269 + the 1-64 B band's 696); after it, 34,965 + 99 = 35,064.\n"
            "# Generated by uc1_apply_band_65_256.py. The 21 held rows are declared uncertainty and must be reported every run.\n")
    w.write("kind\tsource_start\tstart\tend\tnote\tauthority\n")
    for r in rows:
        w.write("%s\t%08X\t%08X\t%08X\t%s\t%s\n" % tuple(r))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
