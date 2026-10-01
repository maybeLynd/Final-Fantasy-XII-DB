"""Append-only extension of text-gap-citations-250.tsv (OPUS, 2026-09-30).
Runs scratch copies of the kit's seeder and classifier, each pointed at a scratch file, so the
registry's hand-written verdicts are never re-seeded or re-classified; then appends the classified
rows for addresses the registry does not yet hold.
"""
import io, os, re, subprocess, sys
REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
KIT = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
SC = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(REPO, "Database", "FFXII TZA", "_index", "candidates", "text-gap-citations-250.tsv")
SEED_OUT = os.path.join(SC, "textgap_seed.tsv").replace("\\", "/")

seed = io.open(os.path.join(KIT, "gen_text_gap_citations.py"), encoding="utf-8").read()
seed = seed.replace('OUT = os.path.join(DB, "_index", "candidates", "text-gap-citations-250.tsv")', 'OUT = r"%s"' % SEED_OUT)
assert SEED_OUT in seed
seed = seed.replace("_os.path.dirname(_os.path.abspath(__file__))", "r'%s'" % KIT)
io.open(os.path.join(SC, "_seed_copy.py"), "w", encoding="utf-8").write(seed)
r = subprocess.run([sys.executable, "-B", os.path.join(SC, "_seed_copy.py")], cwd=REPO, capture_output=True, text=True)
print("seed rc", r.returncode, r.stdout[-300:], r.stderr[-500:])

reg = io.open(REG, encoding="utf-8").read()
nl = "\r\n" if "\r\n" in reg else "\n"
have = set(l.split("\t")[0] for l in reg.splitlines() if l and not l.startswith("#"))
seedrows = io.open(SEED_OUT, encoding="utf-8").read().splitlines()
new = [l for l in seedrows if l and not l.startswith("#") and l.split("\t")[0] not in have]
print("seeded", sum(1 for l in seedrows if l and not l.startswith('#')), "new", len(new))

# classify only the new rows: a scratch registry with the real header comments + new rows
hdr = [l for l in reg.splitlines() if l.startswith("#")]
CL_IN = os.path.join(SC, "textgap_new.tsv")
io.open(CL_IN, "w", encoding="utf-8", newline="").write(nl.join(hdr + new) + nl)
cl = io.open(os.path.join(KIT, "gen_text_gap_classification.py"), encoding="utf-8").read()
cl = cl.replace('F = "Database/FFXII TZA/_index/candidates/text-gap-citations-250.tsv"', 'F = r"%s"' % CL_IN.replace("\\", "/"))
assert CL_IN.replace("\\", "/") in cl
cl = cl.replace("_os.path.dirname(_os.path.abspath(__file__))", "r'%s'" % KIT)
io.open(os.path.join(SC, "_class_copy.py"), "w", encoding="utf-8").write(cl)
r = subprocess.run([sys.executable, "-B", os.path.join(SC, "_class_copy.py"), "--write"], cwd=REPO, capture_output=True, text=True)
print("classify rc", r.returncode, r.stdout[:900], r.stderr[-500:])

classified = [l for l in io.open(CL_IN, encoding="utf-8").read().splitlines() if l and not l.startswith("#")]
if "--append" in sys.argv and classified:
    note = ("# APPENDED 2026-09-30 (OPUS), terminal-audit dry run: %d addresses cited since GN160 were seeded and classified "
            "by scratch copies of gen_text_gap_citations.py / gen_text_gap_classification.py pointed at scratch files, so no "
            "existing row was re-seeded or re-classified. UNCONFIRMED rows below still need a hand verdict." % len(classified))
    body = reg.rstrip("\r\n") + nl + note + nl + nl.join(classified) + nl
    io.open(REG, "w", encoding="utf-8", newline="").write(body)
    print("appended", len(classified))
from collections import Counter
print(Counter(l.split("\t")[8] for l in classified))
