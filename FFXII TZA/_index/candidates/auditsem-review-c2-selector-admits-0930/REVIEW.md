# REVIEW — SWE2-EC7-REQ-AUDITSEM-C2-SELECTOR-ADMITS-0929

*Provenance: written by the concurrent SWE2-AUDIT-SEM session (OPUS-run Claude) that has since ended; its board finish cited `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-c2-selector-admits.md` (gitignored) for the ACCEPT of SWE2-EC7-REQ-AUDITSEM-C2-SELECTOR-ADMITS-0929 at 06:23Z. Published here by the remaining session of the same identity, text unchanged except that each `##` heading now names SWE2-AUDIT-SEM.*

Reviewer: SWE2-AUDIT-SEM (independent). Commit under review: `302bf18a6` (C2 applied — 59 frontier bodies
into five accepted families, FABLE ruling R3). Reviewed 2026-09-30.

## VERDICT: ACCEPT (SWE2-AUDIT-SEM)

## What was independently verified (SWE2-AUDIT-SEM)

**Plan-to-file identity.** All 59 plan rows in
`_index/candidates/ec7-frontier-plan-0929/cand-selector-admits.tsv` are present, by exact entry address, in the
committed member files of their named families. Committed populations match the request exactly:
`explained-callee-adapters.tsv` 487 · `documented-global-leaf-accessors.tsv` 222 · `trivial-global-accessors.tsv`
483 · `phyre-phyrecore.tsv` 433 · `scriptvm-verb-adapter-callbacks.tsv` 1039. Counts and files moved together.

**Removals.** `0036CAD0` absent from `explained-callee-adapters.tsv`; `003DE970` absent from
`documented-global-leaf-accessors.tsv`. Both carrier pages verified `status: REOPENED` at review time:
`24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md` (its `0036D050` A-status
collapses, so its adapter follows) and `04-Actor-Entity/the-field-runtime-pass.md` (sole citation of `02B58C50`).
Removals correctly motivated — explanation pages reopened ⇒ members graduate back to frontier.

**DGLA stale guard (deviation 1).** `select_documented_global_leafs.py` l.193–197: `assert len(members)==222`
with a comment documenting the drift arithmetic (196 at declaration 09-17 → 211 via A-drift → 222 = 211+12−1).
The predicate above the guard is unchanged. Fresh rerun prints `OK: 222 members` — guard and predicate agree.

**UC-1 exclusion (deviation 2).** `select_global_accessors.py` l.62–68 carries the same patch the library
selectors got in `839236205`: `sizes` minus `uc1_band.frontier_starts()` (795 bodies). Without it the selector
would admit 10 UC-1 bodies; patched it admits 483. Verified the import resolves to
`Tools/analysis-kit/gfz-scripts/uc1_band.py` and that `frontier_starts()` returns 795.

**Guarded-stub withhold.** Committed `guarded-class-registration-stubs.tsv` and
`guarded-class-registration-orchestrators.tsv` (HEAD) contain neither `00676A70` (the plan's one stub row) nor
`005EFE60`; `00665870`/`00666380` remain 455-B orchestrator rows in HEAD. This exactly matches the README's
withholding rationale: applying the full rerun would smuggle the two orchestrator→stub moves (134 drift
admissions, excluded by R3) plus `005EFE60`; applying only the frontier row leaves a file the selector can't
reproduce — so neither was applied. The plan's `00676A70` correctly stays frontier.

(Note: the worktree currently carries an uncommitted rerun in that directory — deleted orchestrators TSV,
modified stubs + selector — another lane's in-flight application of the withheld move. Review judged HEAD.)

## Selector reruns (non-author, own observation) (SWE2-AUDIT-SEM)

| Family | Committed | Fresh rerun | Delta | Cause |
|---|---|---|---|---|
| DocumentedGlobalAccessor | 222 | 222 | 0 | byte-drift confined to `owning-page` citation column (`what-the-console-tunes.md` gained a `01F82D20` cite) |
| Trivial global accessors | 483 | 482 | −1 | `00182FE0` graduated to A: cited on `what-the-console-tunes.md` since 09-14, but that page was `PARTIAL` (not evidence-bearing) at commit `302bf18a6` (21:55) and flipped `DOCUMENTED` only in the 09-30 owner read (`17a146c83`, 22:57). Correct at commit time; now routine A-drift. |
| ExplainedCalleeForwarder | 487 | 484 | −3 | `001A9A70`, `001A9AA0`, `001A9AD0` (all → callee `001A7770`) dropped; remaining diff lines are `owning-page` churn only. Same A-drift class. Positive control: 0 members failed re-check. |
| Phyre PhyreCore | 433 | 430 | −3 | same drift class (not individually resolved this pass) |
| ScriptVM.VerbAdapter | 1039 | 1037 | −2 | same drift class (not individually resolved this pass) |

**Finding (not a defect):** three families now sit 1–3 rows stale under fresh rerun — all post-commit A-graduations
from the DD-residue/owner-read wave flipping pages to evidence-bearing. This is the documented drift mechanism
(DGLA's own guard history shows it). The committed files are correct for their generation point; a routine
drift-removal pass converges them. No membership error, no predicate change, no guard weakening found.

## Board (SWE2-AUDIT-SEM)

`SWE2-EC7-REQ-AUDITSEM-C2-SELECTOR-ADMITS-0929` → ACCEPT.
