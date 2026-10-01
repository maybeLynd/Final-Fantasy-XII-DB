"""s08_incorp.py - incorporate SWE2-ORACLE's S-08 BGM-machine drain record (ACCEPTED by SWE2-AUDIT-SPEC) into the S-08
exposure file (OPUS, 2026-10-01; AUTO-INCORP-ORACLE-REQ-AUDITSPEC-S08-BGM-DRAIN-0930). Byte-preserving, idempotent.
Prints PATCHED / ALREADY per edit and FAILS n."""
import os, sys

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "s08-runtime-per-invariant-exposure.md")
REC = "[`s08-bgm-machine-drain-0930`](s08-bgm-machine-drain-0930/README.md)"
REV = "[review](auditspec-review-s08-bgm-0930/REVIEW.md)"
VERDICT = ("executed 2026-09-30 by SWE2-ORACLE, " + REC + ", ACCEPTED by SWE2-AUDIT-SPEC (" + REV + "): the same-call drain "
           "holds with the stream inactive, which is every shipped run, and with an active stream waiting for play (state 5). "
           "With the stream in a submitting state (1, or 7 with bytes left) and the pool full, the requester re-enters itself "
           "through the machine and nothing drains; that is a modded-script domain, like I5's chunking gate")
EDITS = [
    ("**order not reachable; the drain is exposed at `003EADE0`**, which no record executes |",
     "~~**order not reachable; the drain is exposed at `003EADE0`**, which no record executes~~ **order not reachable; "
     "the drain holds in every shipped run** *(OPUS, 2026-10-01: " + VERDICT + ".)* |"),
    ("- **I3's same-call drain has one named exposure:** the BGM stream machine `003EADE0`, which has not been executed.",
     "- **I3's same-call drain has one named exposure:** the BGM stream machine `003EADE0`~~, which has not been executed~~. "
     "*(OPUS, 2026-10-01: " + VERDICT + ".)*"),
    ("once with `streamActive` 0 and once with it non-zero.",
     "once with `streamActive` 0 and once with it non-zero. *(Done 2026-09-30: " + REC + " ran C0, C1, C3 and C4 with a "
     "negative control, `s08_bgm_drain.py` FAILS 0.)*"),
]
fails = 0
b = open(P, "rb").read()
for old, new in EDITS:
    o, n = old.encode("utf-8"), new.encode("utf-8")
    if n in b:
        print("ALREADY", old[:50]); continue
    k = b.count(o)
    if k != 1:
        print("REFUSING (%d): %s" % (k, old[:60])); fails += 1; continue
    b = b.replace(o, n); print("PATCHED", old[:50])
if not fails:
    open(P, "wb").write(b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
