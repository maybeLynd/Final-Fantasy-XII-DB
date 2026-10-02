# data-review-my-progress-metrics-1001

**Identity:** SWE2-DATA · **date:** 2026-10-01/02 · **kind:** metric review record
**Tasks:** OPUS-REQ-DATA-MY-PROGRESS-METRICS-R2 (supersedes
OPUS-REQ-DATA-MY-PROGRESS-METRICS, whose `reviews` field was a string)
**Reviewed:** `Database/Tools/dashboard/requirements.py` MP-1/MP-2 readers at
`622c0866d` (record `_index/workflow/MY-PROGRESS-METRICS.md`), against
`_index/progress/progress_report.py` at `605882fdc` and the current reporter.

## Verdict

**result: verdict:ACCEPT** — this record is the single durable verdict
reference for both MY-PROGRESS-METRICS tasks.

MP-1's counting reconciles with the reporter's semantics at the reviewed
commit; MP-2's distinctions (answered vs dispositioned, bucketed extensions as
named gaps, L2 gated by L1, per-family-first display) are the same rules the
reporter publishes. The one divergence found was not a count error but a code
duplication hazard, resolved below.

## (a) Family counts at the reviewed generation (view g20260929T025707Z-bffd92)

| claim | check | result |
|---|---|---|
| register ANSWERED 1435 = 1403 + NAS 17 + OEB 15 | reporter dispositions | reconciles: `accepted_answers` excludes NAS/OEB, ANSWERED re-adds them |
| withdrawn 159 = SUPERSEDED 121 + NAQ-with-carriers 29 + excluded 9 | `withdrawn_by_lead` split | reconciles; the lead column keeps SUPERSEDED / NOT A QUESTION / DISSOLVED / struck apart |
| page-local obligations 49 | `parse_page_boxes` | reconciles; R3 now emits one obligation row per unticked box (T34b/T37) |
| functions 22950/35064 = A 9178 + B 1368 + C 12404 | `fam-*` readers | reconciles; F family kept out of the headline union per MP-2 |
| audited 386/488, provenance 488/488 | `audited()` / DV reader | reconciles at review time (see note below) |
| registry 63/64, formats 46/48, EBP 14/14 | R/X/E readers | reconciles; `.bin`-bucket formats correctly held as a named gap, never counted |
| L2 cells 251/251, terminal 0/30 | L2/T readers | reconciles; T reads the declared receipt counter, not artefact headings |

Live numbers differ now (register ANSWERED 1612 etc.) because the governing
records moved — the reconciliation is a method check, not a frozen figure.

## CH-2: the reporter's single UNKNOWN

Confirmed and since repaired. CH-2's id cell is struck (`~~CH-2~~`); the
check_questions QID pattern never scores a struck id, and its lead text
(`STRUCK ... FILED IN ERROR`) is in nobody's vocabulary. progress_report.py
parser v5+ reclassifies a *struck* row with an unreadable lead as
WITHDRAWN/STRUCK (T35 covers it; live `UNKNOWN` count is 0). MP-1's behaviour —
excluded from scored rows, listed — is the same class of treatment.

## (b) The audited() question — decided: YES, one rule

`requirements.py::audited()` was a hand-copied port of the audit-pass rule in
`progress.py` (stamped `passes` + non-null `last_pass_state`, or
`falsification_passes` + a written falsification-pass section). The rule had
already been corrected twice in the canonical scorer, so the copy was a drift
risk: whichever side was fixed next would silently change one dashboard and
not the other.

Resolution implemented 2026-10-01:

- `Database/Tools/analysis-kit/gfz-scripts/progress.py` now owns the canonical
  predicate `audit_pass_recorded(text)`.
- `Database/Tools/dashboard/requirements.py::audited()` delegates to it.

Receipts:

- Pre/post live-corpus comparison: both implementations classified the same
  491 audited documents, zero per-document differences (491 → 491, diffs []).
- `python Database/Tools/dashboard/test_requirements.py` — FAILS 0 after the
  refactor (MP1–MP17 fixtures green).

## Cluster receipts (the three engineering tasks this review rode on)

- `python Database/FFXII TZA/_index/progress/test_progress_report.py` —
  FAILS 0, 59 checks: T1–T8 live tree, T9–T23 reporter fixtures, T27
  classifier parity, T34b/T37 obligation-row contract, T36 deep-body
  fingerprint move, T38 empty-vs-invalid, T39/T40 coherent-generation
  commit + last-COMPLETE retention, T41a–d export pin / later-commit
  isolation / mixed-ZIP refusal / mid-export failure, T42a–d
  crosswalk-meanings (reviewer join from the assigned review task, chores
  out of the deduplicated route, every transferred obligation a listed row,
  outcomes as separate counts).
- `python Database/Tools/analysis-kit/gfz-scripts/test_generation.py` —
  FAILS 0 (G1–G15, E1–E8, C1, R1–R8).
- Live: `generate` committed `g20261002T081334Z-e24638`
  (fp `b58dc108a7`, board rev 46472); `check` → `CURRENT`; `export` →
  VERIFIED ZIP (25 members); `verify-zip` → VERIFIED.
- FABLE `CROSSWALK-MEANINGS` R1–R6 + DASHBOARD-MEANINGS §4 are implemented
  in the same adapter: per-obligation transfer rows (60 canonical + 12
  extension-ruling rows), reviewer resolution from the assigned review task
  (requester never a reviewer), coordination chores split out of the route,
  duplicate/split rows separated from carrier-bearing supersessions, blank
  owner-doc cells filled from the naming page or UNKNOWN, and PROGRESS.md
  relabelled (`open board tasks (coordination load)`, separate obligation
  outcomes, completion packages by stage, scoped-L2 label).
