"""set_member_method2.py PREFIX DRAFTER TOTAL STOOD ROWS_FIXED CLAUSES NOTE - record the verification method of a batch
of member records (rows.json 'method') whose rows a non-drafting local agent read at the bytes (OPUS, 2026-10-03).
PREFIX selects the record folders; NOTE names the commonest corrections. Re-run after any interior_ingest check."""
import glob
import io
import json
import os
import sys

C = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "FFXII TZA",
                                  "_index", "candidates"))
prefix, drafter, total, stood, fixed, clauses, note = sys.argv[1:8]
import subprocess
n = 0
for p in sorted(glob.glob(os.path.join(C, prefix + "*", "rows.json"))):
    # a PUBLISHED record's method is history: never rewrite it (2026-10-03: a broad prefix overwrote 28 published
    # records' method text with another batch's counts; restored from HEAD)
    if subprocess.run(["git", "-C", C, "ls-files", "--error-unmatch", p], capture_output=True).returncode == 0:
        continue
    d = json.load(io.open(p, encoding="utf-8"))
    if d.get("mode") != "member":
        continue
    d["method"] = (
        "The page declares the family `%s` (a classification family: ordinary functions grouped by module, not template "
        "copies). engine_explained did not credit these members. %s drafted one sentence and 1-5 interior anchors per "
        "body from OPUS's pack (`mem_pack.py`, filtered against engine_explained's own set); OPUS checked every row "
        "mechanically with `interior_ingest.py` (member mode). A second local agent, not the drafter, then read every one "
        "of the %s rows of this batch against the disassembly: %s stood, %s rows were corrected in %s clauses (%s). OPUS "
        "confirmed corrections at the bytes on a sample; they are listed below. Neither agent is an independent "
        "reviewer: the non-author check is SWE2-AUDIT-SPEC's." % (d.get("family", ""), drafter, total, stood, fixed,
                                                                   clauses, note))
    json.dump(d, io.open(p, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    n += 1
print("method set on", n, "records")
