# PROGRAM-STATE present-tense audit, and the knowledge-versus-activity plan — SWE2-DATA, 2026-10-03

This covers parts (4) and (3) of `FABLE-REQ-DATA-CONTEXT-REFRESH-MIRROR-PROGRESS-1003` (the user's context-refresh
package v3 and improvement addendum). Parts (1) and (2), the mirror rebuild and the lifecycle line, are in `8c22cbe8f`.

## (4) PROGRAM-STATE.md against current authority

I applied the rules of `_index/workflow/CONTEXT-MAINTENANCE.md` section 1. PROGRAM-STATE is kind A (live
current-state authority): it must not state a superseded fact in the present tense. Age alone is not a defect. The
dated sections `4b`–`4az…` are history and were not read as present tense.

| place | present-tense claim at HEAD | current authority | disposition |
|---|---|---|---|
| header, coordination | "the main transition awaits the existing charter quality/readiness gate" | RECONSTRUCTION-CHARTER.md section 0: L1+L2, then terminal certification, then user authorization | stale; **FABLE's** correction (the requester reports it fixed this; not at HEAD when audited). Not touched here, to avoid a second writer on the same sentence |
| header, coordination | "eleven fixed identities since 2026-09-13" | `_inbox/TEAM.md` "The team is eleven fixed production identities" | current |
| section 1, L1 row | "346 documents, 28/28 categories" | `progress.py`: 491 documents | **corrected**: struck, with a link to the generated count instead of a copied one |
| section 1, L2 row | "not reached by any subsystem" | `PROGRESS.md`: scoped L2 verdicts 52 MET of 52 systems; DB_GOAL NOT_MET, `final_audits` 0 / 30 (`goal_gate.py`) | **corrected**: struck; the row states scoped L2 MET and the whole-database goal NOT_MET |
| section 1, L3 row | "44 reimplemented operations … 0 parity-certified (HEAD `c65b1a16`, 2026-09-15)" | charter section 0 (L3 not a database prerequisite); `PARITY-STATUS.md` 0 of 45 pilots certified | **qualified**: lifecycle link, "database-phase evidence probes", current pilot count |
| section 1, tracks line | "a contract without runtime evidence cannot pass the readiness gate" | the per-contract readiness ladder still exists; it is not the program endpoint | current, read as the contract ladder |
| section 2 heading | "Current at HEAD `c65b1a16` — 2026-09-15" | a dated measurement | **relabelled** "Measured at …", with a pointer to regenerate via `program_coverage.py` and to PROGRESS.md |
| section 2b | "Measured 2026-09-17 … re-run it; never quote these from memory" | dated and labelled | current (labelled history) |
| section 3 | charter section 38 checklist, each item dated | history | current |
| section 4 | the EH-edge practice note, marked Done (`EC-1` ANSWERED) | permanent practice | current |

### Correction record (EVIDENCE-POLICY 4a)

- affected: `_index/PROGRAM-STATE.md` — section 1's L1/L2/L3 rows and section 2's heading (four edits, each struck or qualified, nothing deleted).
- consumers: `_index/PROGRAM-STATE.md` section 1/2 is revised-here. The generated `PROGRESS.md` is the authority
  these rows now link, and it agrees (52 MET of 52, DB_GOAL NOT_MET, 0 of 45 pilots), so it is not a consumer to
  update. The header's readiness-gate sentence is routed-to-FABLE (FABLE-REQ-DATA-CONTEXT-REFRESH-MIRROR-PROGRESS-1003
  names it as FABLE's correction). No register row states these figures.
- run verified at commit 8c22cbe8f: [`ps_present_tense_check.py`](ps_present_tense_check.py) — FAILS 0 (output
  [`ps_present_tense_check.out`](ps_present_tense_check.out)). It rejects each superseded phrase outside `~~strike~~`
  and checks the quoted L2 / DB_GOAL / pilot figures against PROGRESS.md, so later drift fails there. Its
  `--self-test` catches 5 of 5 mutations. Run against HEAD's PROGRAM-STATE.md, it reports 6 findings, so it is
  sensitive to the old reading.

## (3) Knowledge progress versus workflow activity — plan

There is not enough time left in this stand-in window to build and review a classifier, so this is the plan. Devin
or the next DATA session implements it. DASHBOARD-MEANINGS has no section 6.3 at HEAD; the classes below are the
addendum's section 2 classes.

**Inputs: canonical events only. Commit size and line counts are never used.**

| event (source) | class |
|---|---|
| register row moved to ANSWERED / NARROWED / SUPERSEDED with a dated owner lead word (`OPEN-QUESTIONS.md`, diffed between two generations through `check_questions`' classifier, which progress_report already imports) | NEW FF12 KNOWLEDGE |
| a struck-and-replaced claim with a correction record (`consumer-check*.md` / `affected:` records the correction gate admits) | CORRECTED / FALSIFIED FF12 CLAIM |
| an AUTO-INCORP-* or review task DONE with `verdict:ACCEPT`, whose record is under `_experiments/evidence/` (runtime, original-code execution) | NEW RUNTIME / ORIGINAL-CODE EVIDENCE |
| a completion package accepted (`_index/completion-packages/` stage change); a type or field row promoted in `_types/*.tsv`; an L2 verdict cell newly MET (`L2-VERDICTS.md`) | NEW RECONSTRUCTION-GRADE TYPE / CONTRACT / RELATIONSHIP |
| a `Reconstruction/` pilot or differential-harness result row change (`PARITY-STATUS.md`) | RECONSTRUCTION / DIFFERENTIAL PROBE, or INTEGRATION / PARITY EVIDENCE when it is a certification row |
| changes to gfz-scripts / tools paths only | TOOLING / INSTRUMENTATION |
| board tasks opened, closed or claimed, resume blocks, inbox notes | WORKFLOW / COORDINATION |
| generated outputs only (PROGRESS.md, snapshots, the mirror, dashboards) | GENERATED / BOOKKEEPING ONLY |
| anything a rule above does not decide | UNCLASSIFIED |

**Placement.** A new section in progress_report's generation ("Recent meaningful changes, last 24 h / 7 d"), built
from the same input fingerprint. The register diff runs against the previous committed generation in
`history.jsonl`, never against wall-clock git activity. Workflow counts are printed in a separate block labelled as
activity (addendum section 10).

**Controls to ship with it.**
- A fixture register transition must classify as knowledge.
- A board-only change must classify as workflow.
- A generated-only commit must classify as bookkeeping.
- An unknown event must print UNCLASSIFIED.
- Sensitivity: swapping the event-to-class table must fail the fixtures.

**Owner and review.** SWE2-DATA builds it, as code owner of progress_report. The meanings review goes to FABLE,
against DASHBOARD-MEANINGS once its section 6.3 exists.
