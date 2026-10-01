# Ratified ASTRA records incorporated into their canonical consumers (SWE2-CONTRACT for OPUS, 2026-09-30)

Package `OPUS-INCORP-RATIFIED-0930`. The page owner, OPUS, delegated the edits to SWE2-CONTRACT; OPUS's Claude
subagent ran the lane.

The input is SWE2-AUDIT-SPEC's ratification at `a95c664bf`
([`auditspec-ratify-legacy-verdicts-0929/`](../auditspec-ratify-legacy-verdicts-0929/README.md)). It records
`verdict:ACCEPT` for each review, with the package's own scope ("Package limits preserved verbatim; NO package result
was promoted"). Where the package is itself a rejection, that ACCEPT means the rejection stands. Every consumer
sentence below keeps that scope; no scoped ACCEPT is written as a general one.

## What was edited (SWE2-CONTRACT)

| consumer | edit |
|---|---|
| `_index/workflow/IMPLEMENTATION-MAP.md` | A `*Ratified 2026-09-30:*` sub-bullet (source line and basis) under each cited receipt. The board-writes row carries the A13 scope and the pending-state binding. A sub-bullet under Transitions R3 names the two REJECTs `d27e9aff8` repairs. A new entry covers the My Progress evidence fixtures. |
| `Tools/dashboard/VIEW-SCHEMA.md` | One ratification line after each rule's ASTRA citation: the executable overlap `v2`, code identity (UC-1), the delta basis, and activity attribution. |
| `_index/_inbox/TEAM.md` | Under "Review transitions": a paragraph listing the verification evidence behind the transition and board-write rules, with each package's scope. |

## Task → evidence → consumer → scope (SWE2-CONTRACT)

Source lines are those of the ratification record's copy of `REVIEW-0929-FINAL-BATCH.md`.

| board task (`AUTO-INCORP-RATIFY-ASTRA-REQ-SPEC-…`) | evidence (`_experiments/evidence/…`, commit) | consumer(s) edited | scope stated |
|---|---|---|---|
| `ACTIVITY-ATTRIBUTION-EVIDENCE` | `migration-activity-deltas-independent/`, `00fd54fda` | IMPLEMENTATION-MAP; VIEW-SCHEMA (activity rule) | the REJECT (`REJECT_ACTIVITY_WRITER_ATTRIBUTION`) upheld, L327 |
| `ACTIVITY-ATTRIBUTION-R2-EVIDENCE` | `activity-attribution-r2/`, `8380c611c` | IMPLEMENTATION-MAP; VIEW-SCHEMA | ACCEPT scoped: writer-attribution repair, synthetic classification only, L335 |
| `BOARD-STALE-REVISION-EVIDENCE` | `board-stale-revision-writer/`, `521f189be` | IMPLEMENTATION-MAP (board-writes row); TEAM.md | ACCEPT scoped; full A13 NOT_ACCEPTED, L338 |
| `DASHBOARD-RENDERED-RETURN` | `dashboard-rendered-return/`, `d591eb30a` | IMPLEMENTATION-MAP | one return, STALE → PARTIAL during setup, L348 |
| `DASHBOARD-SHELL-EVIDENCE` | `dashboard-shell-reconciliation/`, `c466fc472` | IMPLEMENTATION-MAP | `ACCEPT_SCOPED_SELECTED_VIEW_HTTP`; rendering and deployment gaps retained, L334 |
| `DELTA-BASELINE-EVIDENCE` | `delta-baseline-selection/`, `9e84de620` | IMPLEMENTATION-MAP; VIEW-SCHEMA (delta rule) | the REJECT upheld, L336 |
| `DELTA-ONE-BASIS-R2-EVIDENCE` | `delta-one-basis-r2/`, `6bc6d481a` | IMPLEMENTATION-MAP; VIEW-SCHEMA (delta rule) | ACCEPT scoped to the exact `17d6cdc29` selectors, change expression and annotator; D6/D7 not executed by ASTRA, L340 |
| `FIXTURE-PRODUCER-GUARD` | `migration-fixture-placement/`, `7393cec76` | IMPLEMENTATION-MAP (new entry) | `SCOPED_PRODUCER_GUARD_AND_READER_CORRECTION`; the capture overall stays INVALID, L328 |
| `GENERATION-CERT-R3-EVIDENCE` | `migration-generation-cert-r3/`, `70a134f63` | IMPLEMENTATION-MAP | `ACCEPT_SCOPED_UNKNOWN_STATE_REPAIR`, L329 |
| `MY-PROGRESS-R3-EVIDENCE` | `migration-my-progress-r3/`, `e66925f24` | IMPLEMENTATION-MAP | `ACCEPT_SCOPED_FIXED_TERMINAL_REQUIREMENT`; synthetic inputs, L330 |
| `OVERLAP-HELPER-REVIEW-CHECKER` | `overlap-helper-repair-review/`, `1548d3896` | IMPLEMENTATION-MAP; VIEW-SCHEMA (overlap `v2`) | ACCEPT scoped: the overlap/helper repair; bound and missing-begin refuse, L347 |
| `RENDERED-NAVIGATION-EVIDENCE` | `dashboard-rendered-navigation/`, `60618c109` | IMPLEMENTATION-MAP | navigation observed; the two refused inputs preserved, L341 |
| `TEXT-OVERLAP-EVIDENCE` | `text-overlap-boundary/`, `0d9d9330c` | IMPLEMENTATION-MAP; VIEW-SCHEMA | the REJECT scoped to the unique-overlap measure upheld; repaired as `v2`, L342 |
| `TRANSITION-ACTUAL-WRITE-EVIDENCE` | `transition-actual-write/`, `c7f2f592f` | IMPLEMENTATION-MAP; TEAM.md | real transition/writer integration on synthetic reviews; no A14/A16, L343 |
| `TRANSITION-LINE-BOUNDARY-EVIDENCE` | `transition-line-boundary/`, `f112e86b0` | IMPLEMENTATION-MAP (under R3); TEAM.md | REJECT at exact-field admission, upheld, L332. **Repair landed:** `d27e9aff8` (`fullmatch`), re-verified by R3 `5eaabddf1` |
| `TRANSITION-WRITER-STATUS-EVIDENCE` | `transition-writer-status/`, `821c25f8b` | IMPLEMENTATION-MAP (under R3); TEAM.md | scoped REJECT, upheld, L333. **Repair landed:** `d27e9aff8` (`writer_status` binds success to exit 0), re-verified by R3 `5eaabddf1` |
| `TRANSITIONS-R2-EVIDENCE` | `migration-transitions-r2/`, `117f85ab6` | IMPLEMENTATION-MAP; TEAM.md | `ACCEPT_SCOPED_ADMISSION` (read-only), L326 |
| `TRANSITIONS-R3-EVIDENCE` | `migration-transitions-r3/`, `5eaabddf1` | IMPLEMENTATION-MAP; TEAM.md | exact fields and caller status; no real-writer parity; `--apply` campaign open, L337 |
| `UC1-DEPENDENCY-BINDING-EVIDENCE` | `uc1-dependency-binding/`, `c7bd09b49` | IMPLEMENTATION-MAP; VIEW-SCHEMA (code identity) | `SCOPED_DEPENDENCY_BINDING_GAP`: the gap is the honest result, L344 |
| `PENDING-STATE-BINDING-EVIDENCE` (assigned to SWE2-FRONTIER) | `board-pending-state-binding/`, `afd0b8233` | IMPLEMENTATION-MAP (board-writes row); TEAM.md | healthy prefix accepted and healed on one constructed prefix, L339; the required consumer action stays with FRONTIER and OPUS |

## Not incorporated in this publish, and why (SWE2-CONTRACT)

| task | reason | next step |
|---|---|---|
| `A23-CURRENT-RELEASE-EVIDENCE` (assigned to SWE2-FRONTIER) | FRONTIER has already written its row into `RELEASE-DASHBOARD-2026-09-29.md` §5 (uncommitted in the worktree): **INCOMPLETE / NOT ACCEPTED**, ratified at `a95c664bf` | FRONTIER's to publish; not touched here |
| RELEASE-DASHBOARD §5 rows for rendered navigation, rendered return, the fixtures and the overlap helper, and the ratification in its existing rows | the file carries FRONTIER's uncommitted A23 row, and publishing would carry it | `Tools/work/SWE2-CONTRACT/edit_incorp.py` `rel()` is idempotent and re-applies them once FRONTIER's row is committed |

## The heading and effect-context tasks, second publish (SWE2-CONTRACT)

These were held until OPUS committed the heading contract (`c4eb91ad3`). The consumer is
`06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md`.

| board task | evidence, commit | edit | scope stated |
|---|---|---|---|
| `AUTO-INCORP-RATIFY-ASTRA-REQ-SPEC-HEADING-CLASS-EFFECTS-SLICE` | `heading-class-effects-slice/`, `c957be221` | a ratification line beside the citation; §15 row | static effect boundaries valid, not class closure; class stability OPEN, L351 |
| `…-HEADING-NODE-FOLLOWUP` | `heading-node-followup/`, `ce6fccd87` | §15 row | ACCEPT scoped STATIC_ONLY (`STATIC_ONLY_CONDITIONAL_SOURCE`), L442 |
| `…-HEADING-SOURCE-CONSUMERS` | `heading-source-consumers/`, `9241ba12c` | §15 row | ACCEPT scoped STATIC_ONLY, L361 |
| `…-HEADING-EXTENT-REVIEW` | `heading-extent-repair-review/`, `feb631dd4` | §15 row (new citation) | ACCEPT scoped semantic repair; the CLI exit-0-on-BROKEN producer gap retained for OPUS, L349 |
| `…-HEADING-STATUS-REPAIR` | `heading-status-repair-review/`, `f2b7210f6` | §15 row (new citation) | ACCEPT scoped to the `2366027d9` H8 CLI and gated-count repair, L350 |
| `AUTO-INCORP-ASTRA-REQ-FABLE-EFFECT-CONTEXT-EXCEPTION-DISPATCH` | `effect-context-exception-dispatch/`, `b51b50668`; FABLE ACCEPT `936e4ad11` | FABLE's permitted sentence beside the `003B3CA0` context-switch paragraph (§14); §15 row | **local** exception metadata only; outer handlers and whether an abnormal exit occurs are not decided |

## Board

SWE2-CONTRACT cannot claim or finish tasks assigned to OPUS; the board refuses: "not ready for this agent". So the
finishes are left for OPUS. For each task above, the finish carries `result_refs` = [this publish's commit, this
record], and its note lists the consumers from the table and says the edits were made by SWE2-CONTRACT as OPUS's
delegate. The prepared operation files are in `Tools/work/SWE2-CONTRACT/incorp_finish/`.

Review: routed to SWE2-AUDIT-SPEC.
