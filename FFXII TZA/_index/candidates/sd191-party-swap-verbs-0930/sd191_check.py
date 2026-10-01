"""sd191_check.py - SD-191: which scripts call the party-swap verbs that drop / raise the flat-movement flag B
(02B40534, BV-5), and in what order (OPUS, 2026-09-30).
Runs Database/Tools/analysis-kit/gfz-scripts/script_verb_census.py over every shipped .ebp (writes sd191-census.out),
then checks the us-copy table sd191-calls-us.tsv it keeps beside this file.
"""
import collections, csv, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


DROP = {"0x202", "0x2A3", "0x232", "0x191"}   # BV-5: store 0 into 02B40534
RAISE = {"0x195", "0x205", "0x2A4"}           # BV-5: store 1
out = subprocess.run([sys.executable, "-B", os.path.join(KIT, "script_verb_census.py"),
                      "--verbs", ",".join(sorted(DROP | RAISE)), "--out", os.path.join(HERE, "sd191-census-all.tmp")],
                     capture_output=True, text=True).stdout
open(os.path.join(HERE, "sd191-census.out"), "w", encoding="utf-8", newline="\n").write(out)
allrows = list(csv.DictReader(open(os.path.join(HERE, "sd191-census-all.tmp"), encoding="utf-8"), delimiter="\t"))
os.remove(os.path.join(HERE, "sd191-census-all.tmp"))
# C1 - the whole corpus: 738 calls, 82 per language across nine copies that agree in all 27 zone files
check("C1", "matching calls: 738" in out and "zone files: 27 (language copies agree on (script, verb) in 27)" in out
      and len(allrows) == 738, "738 calls; 27 zone files; all language copies agree")
us = [r for r in allrows if "/us/" in r["file"]]
kept = list(csv.DictReader(open(os.path.join(HERE, "sd191-calls-us.tsv"), encoding="utf-8"), delimiter="\t"))
check("C2", len(us) == 82 == len(kept) and sorted((r["file"], r["pc"]) for r in us) == sorted((r["file"], r["pc"]) for r in kept),
      "the kept us table (82 calls) matches this run")
# C3 - only the 26 summon files sum_a..sum_m x 0000/0001 and one special-attack file spc_z0000 call them
files = sorted(set(r["file"].split("/")[-1] for r in us))
want = sorted(["sum_%s%s.ebp" % (ch, n) for ch in "abcdefghijklm" for n in ("0000", "0001")] + ["spc_z0000.ebp"])
check("C3", files == want, "the 26 summon files and spc_z0000, nothing else")
by = collections.defaultdict(list)
for r in us:
    by[(r["file"].split("/")[-1], r["script"])].append((int(r["pc"], 16), r["verb"]))
seq = {k: [v for _, v in sorted(c)] for k, c in by.items()}
# C4 - each summon's 0000 director script: capture > dispose > setpossummonspace (all drop B) > changetosummonparty (raise)
ok4 = all(seq[k] == ["0x232", "0x202", "0x191", "0x205"] for k in seq if k[0].endswith("0000.ebp") and k[0].startswith("sum_"))
check("C4", ok4 and sum(1 for k in seq if k[0].startswith("sum_") and k[0].endswith("0000.ebp")) == 13,
      "13 summon entries: capturepartyforsummon > disposepartywithoutcontrol > setpossummonspace > changetosummonparty")
# C5 - each summon's 0001 file holds one setpossummonspace (drop) and one resumeposbattletarget (raise), in one script
#      or split across two (終了 'end' + ＡＤ in b, g, i)
ok5 = True
for ch in "abcdefghijklm":
    vs = sorted(v for k, s in seq.items() if k[0] == "sum_%s0001.ebp" % ch for v in s)
    ok5 &= vs == ["0x191", "0x195"]
check("C5", ok5, "13 summon exits: one setpossummonspace and one resumeposbattletarget each")
# C6 - the special attack: duplicatepartyinfo_spattack > setpossummonspace > resumeposbattletarget > resumepartyinfo_spattack
check("C6", seq.get(("spc_z0000.ebp", "監督")) == ["0x2A3", "0x191", "0x195", "0x2A4"],
      "spc_z0000: duplicate > setpossummonspace > resumeposbattletarget > resumepartyinfo_spattack")
print("FAILS %d" % fails)
