"""Record the verification method of the 11 Phyre module member records of 2026-10-03 in their rows.json (OPUS)."""
import glob
import io
import json
import os

C = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates"
METHOD = ("The page declares the family `{fam}` (a classification family: ordinary functions grouped by module, not "
          "template copies). No page explained these members. A local drafting agent (local-ee-drafter) drafted one "
          "sentence and 1-5 interior anchors per body from OPUS's pack (`mem_pack.py`); OPUS checked every row mechanically "
          "with `interior_ingest.py` (member mode: the body is an unexplained member of a family this page declares). A "
          "second local agent, not the drafter, then read every one of the 272 rows of this batch against the "
          "disassembly (repetitive destructors, initialisers and clone bodies compared instruction by instruction "
          "against a fixed template): 262 stood, 10 clauses in 8 functions were corrected (signed compares written as "
          "above/below, one missing dereference, two operand groupings, one pair of per-pair callees). OPUS confirmed "
          "each correction at the bytes and re-read a random sample of the rows that stood; the corrections are listed "
          "below. Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.")
n = 0
for p in glob.glob(os.path.join(C, "opus-member-*module-[0-9]*", "rows.json")):
    d = json.load(io.open(p, encoding="utf-8"))
    if d.get("session") != "local-ee-drafter" or d.get("mode") != "member":
        continue
    d["method"] = METHOD.format(fam=d.get("family", ""))
    json.dump(d, io.open(p, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    n += 1
print("method set on", n, "records")
