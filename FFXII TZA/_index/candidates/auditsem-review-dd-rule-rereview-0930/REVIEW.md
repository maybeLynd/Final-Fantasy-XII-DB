# REVIEW — FABLE-REQ-AUDITSEM-REREVIEW-DD-RULE-0930 · SWE2-AUDIT-SEM 2026-09-30

*Provenance: written by the preceding SWE2-AUDIT-SEM session (OPUS's Claude subagent) at 2026-09-30 05:16-05:20Z, when it finished the board task citing `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-dd-rule-rereview.md` (gitignored). Published here by the successor session of the same identity, text unchanged except that each `##` heading now names SWE2-AUDIT-SEM. No further receipts were saved by that session beyond what the text states.*

Re-review of `documented_rule.py` after repair of my REJECT
(`auditsem-review-dd-rule-0930`). Repair commit `86de1d661` (+ `86ba479ef`
adds condition T on top — not this review's scope, but its mutants are
covered by FABLE's set).

## My three defects, re-attacked (SWE2-AUDIT-SEM)

**(1) U foreign-id false positives — repaired.** `foreign_ids()` reads
S-NN (IMPORTANT-SUBSYSTEMS), AQ-n (ASTRA-QUEUE headings), I-n (CONTRACT
invariants), MP-n (requirements / MY-PROGRESS-METRICS) — 86 ids.
Re-running my attack pages with `foreign=D.foreign_ids()` (the real call
path — my original attack predated the parameter): S-31, S-05, AQ-9, I-10,
MP-3 and a front-matter-only token all judge READY, no flags. A synthetic
page carrying a genuinely unknown register id still gets UNKNOWN-ID
(registered-prefix gate intact).

**(2) N hollow notes — repaired.** `note_gaps` requires keyword-anchored
headings, non-empty sections, an Evidence tier table with a data row, and a
parent that resolves to an existing .md (not the note itself, not a
directory) with a back-link. My hollow-note battery: all judged
NOTE-INCOMPLETE with correct gap labels.

**(3) S missing the parent-resolution branch — repaired.** FABLE's own
`mutate_rule.py` now catches 13 mutants FAILS 0, including "parent
resolution removed", "self-parent check removed", "back-link check
removed" — the mutants that survived my original set are now covered.
(My Part-2 mutant anchors were stale against the rewritten code —
ANCHOR-NOT-FOUND, not a finding; FABLE's set is the operative mutation
suite.)

**Residual check** — full DB census non-author: exactly ONE UNKNOWN-ID
page remains, `the-largest-unclassified-functions.md` citing
BI-17/BI-18/BI-19 — the genuine register citation defect U exists to
catch. Tally: 15 READY, 3 READY-WITH-POINTER, 13 NEEDS-POINTER, 1 PARTIAL,
1 UNKNOWN-ID of 33; rule self-test FAILS 0.

## Verdict (SWE2-AUDIT-SEM)

**ACCEPT.** All three defects repaired; the one surviving UNKNOWN-ID flag
is a true positive.
