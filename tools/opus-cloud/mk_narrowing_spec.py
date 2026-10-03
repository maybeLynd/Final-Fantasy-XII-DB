"""Build the consolidated publish spec for SWE2-AUDIT-SPEC's narrowings of batch 95d495604 (OPUS, 2026-10-03)."""
import glob
import json
import os
import subprocess

REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
DB = os.path.join(REPO, "Database", "FFXII TZA")
CAND = os.path.join(DB, "_index", "candidates")
SKIP = ("opus-ee-verb-adapters-1003", "opus-ee-rulings-1003")
INTERIOR = ("opus-animation-channel-binding-and-transform--ee-1003", "opus-sound-variant-selection-ee-1003",
            "opus-referenced-code-the-list-never-had-uc1-1002")


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, encoding="utf-8").stdout


fam = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(CAND, "opus-ee-*", "spec.json"))
             if os.path.basename(os.path.dirname(p)) not in SKIP
             and not json.load(open(p, encoding="utf-8")).get("retired"))
recs = fam + list(INTERIOR)
paths, pages = [], set()
for r in recs:
    st = git("status", "--porcelain", "--untracked-files=all", "--", "Database/FFXII TZA/_index/candidates/%s" % r)
    for l in st.splitlines():
        paths.append(l[3:].strip().strip('"'))
    sp = os.path.join(CAND, r, "spec.json") if r in fam else os.path.join(CAND, r, "rows.json")
    pages.add(json.load(open(sp, encoding="utf-8"))["page"])
for pg in sorted(pages):
    rel = "Database/FFXII TZA/" + pg
    num = git("diff", "--numstat", "--", rel).strip()
    if num:
        paths.append(rel)
    print("PAGE %-110s %s" % (pg[:110], num.split("\t")[:2] if num else "unchanged"))
gate = " && ".join(
    ["(cd 'FFXII TZA/_index/candidates/%s' && python -B fam_rows.py check | tail -1 | grep -qx 'FAILS 0' && "
     "python -B fam_rows.py apply | head -1 | grep -q ALREADY)" % r for r in fam]
    + ["(cd 'FFXII TZA/_index/candidates/%s' && python -B interior_applier.py | tail -1 | grep -qx 'FAILS 0')" % r
       for r in INTERIOR]
    + ["(cd 'FFXII TZA/_index/candidates/opus-referenced-code-the-list-never-had-uc1-1002' && "
       "python -B uc1_entry_check.py | tail -1 | grep -qx 'FAILS 0')"]) + " && echo NARROW-OK || echo GATE-FAIL narrow"
spec = {"id": "OPUS-PUB-SPEC-NARROWINGS-1003",
        "title": "SWE2-AUDIT-SPEC's narrowings of batch 95d495604 incorporated: family leads, columns and exclusion "
                 "reasons, controls that run mutated rows through the comparison plus a raw-byte known answer, skips "
                 "re-verified, +4 return-value adapters (census-extent decode), 005C6D90 16-bit stores, three address "
                 "wordings, 19 UC-1 census phrases",
        "gate": gate, "paths": sorted(set(paths)),
        "requests": [{"id": "OPUS-REQ-AUDITSPEC-NARROWINGS-REREVIEW-1003", "to": "SWE2-AUDIT-SPEC",
                      "target": "_index/candidates/opus-ee-traversal-adapters-1003/", "scope": "re-review",
                      "priority": "P2",
                      "question": "At {commit}: your ACCEPT-WITH-NARROWING items of 95d495604 are incorporated - "
                                  "the six lead replacements verbatim; name-only skips now re-verified against "
                                  "00875E10 (spec skip_caller) and marked 'skip:' in excluded.tsv; return-value "
                                  "adapters decode the census extent (398 rows, 4 exclusions); guarded-registration "
                                  "columns per your wording and refusal reasons split 35/19; fam_rows.py controls now "
                                  "pass mutated copies of rows.tsv through compare() and require FAILS > 0, plus a "
                                  "raw-byte known answer; 005C6D90, the three address wordings and the 19 UC-1 "
                                  "phrases verbatim. Please confirm the narrowings are closed.",
                      "blocked": "closing the narrowings", "why": "producer incorporation of a non-author review",
                      "completion": "a review record with a verdict"}]}
out = os.path.join(REPO, "Database", "Tools", "work", "OPUS", "queue", "hold", "0n_spec_narrowings_1003.json")
json.dump(spec, open(out, "w", encoding="utf-8"), indent=1)
print("records", len(recs), "paths", len(spec["paths"]), "->", out)
