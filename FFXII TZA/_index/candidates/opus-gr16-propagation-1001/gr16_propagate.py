"""gr16_propagate.py - carry SWE2-AUDIT-SEM's SECTION-03 verdict (GR-16, ACCEPT-WITH-NARROWING, f41194772) and two
other closed rows (GR-17, RC-37) into the pages that still call them pending (OPUS, 2026-10-01).

Found by the cloud register-consistency sweep (Final-Fantasy-XII-DB PR #1, sections a and d), re-checked here against
the live tree. Byte-preserving, idempotent: each edit's old text must occur exactly once, or the new text already be
there. Prints PATCHED / ALREADY per edit and FAILS n.
"""
import os, sys

DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))  # FFXII TZA
R13 = "13-Rewards-Progression-Economy/"
REV = "../_index/candidates/auditsem-review-section03-1001/REVIEW.md"
ACC = ("independently accepted with a narrowing 2026-10-01 (SWE2-AUDIT-SEM, [review](%s), GR-16; N1: "
       "`run_review.py` reproduces against the pinned pre-image of the reward-binding checker, and the sealed checker "
       "agrees with the preserved observation)" % REV)
FM = "independently accepted with a narrowing 2026-10-01 (SWE2-AUDIT-SEM, auditsem-review-section03-1001, GR-16, N1)"
QUOTE_OLD = "> **SECTION-03 production review, 2026-09-22; independent peer acceptance pending** (registered as GR-16, 2026-09-30)."
QUOTE_NEW = ("> **SECTION-03 production review, 2026-09-22; ~~independent peer acceptance pending~~** (registered as GR-16, "
             "2026-09-30). *(OPUS, 2026-10-01: " + ACC + ".)*")
FM_OLD = "  status: locally validated; peer acceptance pending"
FM_NEW = "  status: locally validated; " + FM

EDITS = [
    (R13 + "experience-and-license-point-award.md",
     "status: PARTIAL — SECTION-03 independent peer acceptance pending (GR-16); reward-row binding lifetime (GR-17) and "
     "edge-state reachability (GR-18) open;",
     "status: PARTIAL — edge-state reachability (GR-18) partial; SECTION-03 " + FM + "; reward-row binding lifetime "
     "(GR-17) answered 2026-09-30;"),
    (R13 + "experience-and-license-point-award.md", FM_OLD, FM_NEW),
    (R13 + "experience-and-license-point-award.md", QUOTE_OLD, QUOTE_NEW),
    (R13 + "how-experience-is-computed-and-divided.md",
     "status: REOPENED — SECTION-03 independent peer acceptance pending (GR-16);",
     "status: REOPENED — SECTION-03 " + FM + "; the page's re-status is left to its owner (FABLE);"),
    (R13 + "how-experience-is-computed-and-divided.md", FM_OLD, FM_NEW),
    (R13 + "how-experience-is-computed-and-divided.md", QUOTE_OLD, QUOTE_NEW),
    (R13 + "what-happens-when-an-enemy-dies.md", QUOTE_OLD, QUOTE_NEW),
    (R13 + "CONTRACT-defeat-rewards-sequence.md", FM_OLD, FM_NEW),
    (R13 + "CONTRACT-defeat-rewards-sequence.md",
     "> **SECTION-03 production review, 2026-09-22; independent peer acceptance pending.**",
     "> **SECTION-03 production review, 2026-09-22; ~~independent peer acceptance pending.~~** *(OPUS, 2026-10-01: "
     + ACC + ".)*"),
    (R13 + "CONTRACT-experience-and-licence-award.md",
     '  status: "PRODUCTION COMPLETE; formal peer acceptance pending"',
     '  status: "PRODUCTION COMPLETE; ' + FM + '"'),
    (R13 + "CONTRACT-experience-and-licence-award.md",
     "production corrections and leaves formal peer acceptance pending.",
     "production corrections and leaves ~~formal peer acceptance pending~~ formal peer acceptance to the auditor. "
     "*(OPUS, 2026-10-01: " + ACC + ".)*"),
    ("02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md",
     "static; pending SWE2-AUDIT-SPEC review). |",
     "static; ~~pending SWE2-AUDIT-SPEC review~~ reviewed ACCEPT by SWE2-AUDIT-SPEC 2026-09-30, "
     "[`auditspec-review-rc37-0930`](../_index/candidates/auditspec-review-rc37-0930/REVIEW.md)). |"),
]

# CONTRACT-* files in _index/candidates/overlay-drop-census-2026-09-25.tsv are overlay carriers: FRONTIER applies those.
# Default: the ordinary pages only. --carriers: the carrier edits only. --dry-run: report without writing.
CARRIERS = "--carriers" in sys.argv
DRY = "--dry-run" in sys.argv
fails = 0
for rel, old, new in EDITS:
    if ("/CONTRACT-" in "/" + rel) != CARRIERS:
        continue
    p = os.path.join(DB, rel)
    b = open(p, "rb").read()
    o, n = old.encode("utf-8"), new.encode("utf-8")
    if "|" in new.replace(" |", "", 1) and rel.endswith("request-queue.md"):
        print("REFUSING pipe inside a table cell", rel); fails += 1; continue
    if n in b:
        print("ALREADY", rel.split("/")[-1]); continue
    k = b.count(o)
    if k != 1:
        print("REFUSING %s: old text found %d times" % (rel.split("/")[-1], k)); fails += 1; continue
    if not DRY:
        open(p, "wb").write(b.replace(o, n))
    print("WOULD PATCH" if DRY else "PATCHED", rel.split("/")[-1])
print("FAILS", fails)
sys.exit(1 if fails else 0)
