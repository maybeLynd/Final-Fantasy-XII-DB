# Context refresh: the lifecycle after the database, written once, and the current-state drift it exposed (FABLE, 2026-10-03)

*FABLE's part of the user's `FFXII_DB_RECONSTRUCTION_CONTEXT_REFRESH_PACKAGE_2026-10-02_v3` and
`FFXII_PROJECT_IMPROVEMENT_ADDENDUM_2026-10-03` (a copy of the package is in `Database/Tools/work/FABLE/`). Board task
`FABLE-CONTEXT-REFRESH-1003`. This publish does not start the primary reconstruction phase. The current phase stays
DATABASE, and only the user changes it.*

## What changed

- **One lifecycle authority.**
  - `RECONSTRUCTION-CHARTER.md` gains §0, *Project lifecycle (user directive, 2026-10-02)*:
    - the phase;
    - L1+L2 as the goal, with L3 later;
    - bounded probes as evidence only;
    - the explicit user-authorized transition;
    - independent maintainable source, with the original game as evidence and oracle, never the backend;
    - the validation chain and the first-divergence rule;
    - the maturity ladder;
    - the whole-game target, and modding as a first-class output.
  - Its machine-readable twin is `_index/workflow/PROJECT-LIFECYCLE.json`.
  - §16 ("advance in parallel") gets a read-with-§0 note. The user's 09-08 text is otherwise unchanged.
- **Database README.**
  - A lifecycle summary after the L1/L2/L3 table, and a *Project lifecycle after database completion* section.
  - "Source of truth" is split into the reference executable / provenance authority and the canonical technical
    knowledge.
  - The hardcoded team count is replaced by the live TEAM authority and the Resume state rule.
  - A *Where each current answer lives* table labels each source CURRENT AUTHORITY, CURRENT DERIVED or HISTORICAL.
  - The two format folders the category tables omitted (`25-EBP`, `26-PKFL`) are listed.
  - The Status table points at `goal_gate.py` and the generated `PROGRESS.md`, and copies no numbers.
- **TEAM.md.**
  - A new *Starting or resuming* section: current authority first, plus the startup guard for old handoffs.
  - The endpoint paragraph links §0.
  - The September *Exact starting instructions* are labelled HISTORICAL CHECKPOINT in place, not rewritten.
- **DASHBOARD-MEANINGS.md §6** (FABLE-owned vocabulary):
  - the phase axis, and the rule that no view moves to RECONSTRUCTION AUTHORIZED;
  - the DB_GOAL blocking chain, taken from `goal_gate.py`;
  - scoped L2 versus the whole database;
  - the Depth diagnostic;
  - knowledge events versus workflow activity;
  - reconstruction maturity labels and the first-divergence report;
  - current/historical identity labels.
- **`_index/workflow/CONTEXT-MAINTENANCE.md`:** the five material classes, the working-day sweep, the supersession
  index and ownership. It names the existing mechanisms; only one new check is added.
- **`check_lifecycle_consumers.py`** (gfz-scripts) compares the contract with the charter and the entry points, and
  flags known superseded phrases. It has a five-mutation self-test.

## Stale current-state claims corrected

1. **README, the `99-Unresolved-Residual` row.** It said "the gate is not sealed". The README's own Status row records
   the seal of 2026-09-16 (independent re-certification by SWE2-AUDIT-SEM), so the row is struck and corrected to
   SEALED.
2. **README "Concurrent researchers".** It said "eleven fixed identities since 2026-09-13". That is true today
   (`team.py` lists 11), but it is a volatile fact, so it is replaced by the pointer to TEAM.md and TEAM.json.
3. **PROGRAM-STATE.md coordination header.** It said "the main transition awaits the existing charter
   quality/readiness gate". That endpoint was replaced on 2026-09-12 (TEAM.md), so the phrase is struck and corrected
   to L1+L2 completion plus the user's explicit authorization.
4. **TEAM.md *Exact starting instructions*.** They named first-week packages (EE-2, EH-3, ASTRA-RT1). They are
   labelled historical and superseded by *Starting or resuming*.

## Verified, no edit needed

- `goal_gate.py` already decides L1+L2 with no L3 prerequisite.
- `requirements.py` already holds `DATABASE READY - awaiting user authorization` and the cumulative-L2 gate.
- TEAM.md's 2026-09-12 endpoint paragraph already says a primary reconstruction phase needs a separate user
  instruction.
- `PROGRESS.md` is generated, so it is left to its generator. It is dirty in the tree with SWE2-DATA's work.

## Left historical on purpose

- `_index/workflow/START-HERE.md` and `ALL-TOP-LEVEL-GOALS.md` are the 2026-09-28 migration ZIP's start files.
- GM/GN-era handoffs.
- Dated audits, sealed evidence and proposals.
- The supplied 2026-09-26 `knowledge.sqlite` snapshot.

All of these are labelled in CONTEXT-MAINTENANCE §4, not edited.

## Routed (not FABLE's code)

- **SWE2-FRONTIER:** dashboard rendering of the phase axis and the transition states, the DB_GOAL blocking chain,
  recent knowledge changes, the provenance drawer, and `PROJECT-LIFECYCLE.json` as a declared generation input, with
  focused tests.
- **SWE2-DATA:** `knowledge_db.py check` and the refresh, knowledge-versus-activity reporting in `progress_report.py`,
  and PROGRAM-STATE's data sections.
- **Deferred:** the P2 items (dependency graph, first-divergence views). The addendum ranks them for the
  reconstruction approach.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/README.md`

affected: `Database/FFXII TZA/_index/PROGRAM-STATE.md`

- consumer: the database README's residual row, team line and status pointers: revised-here.
- consumer: PROGRAM-STATE's coordination header: revised-here.
- consumer: TEAM.md's startup path: revised-here.
- consumer: the dashboard's phase rendering: routed to SWE2-FRONTIER. The meanings are in DASHBOARD-MEANINGS §6.

run: check_lifecycle_consumers.py at 6b7ff727e: FAILS 9 before the apply (all nine are the drift listed above, which
shows the check is sensitive to it); FAILS 0 and SELF-TEST PASS after the apply in a clean worktree
