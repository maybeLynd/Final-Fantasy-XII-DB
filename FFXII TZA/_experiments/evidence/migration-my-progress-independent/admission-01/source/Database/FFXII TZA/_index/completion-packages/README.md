# Completion packages: record shape and stages (FABLE, Claude Opus 5.5, 2026-09-28)

**For:** FRONTIER-REQ-FABLE-WORKFLOW-PILOTS-SEMANTICS, under
[`COMPLETION-WORKFLOW.md`](../workflow/COMPLETION-WORKFLOW.md) §3 (revision FF12-WORKFLOW-MIGRATION-20260928-01).

**What a package is.** A completion package groups existing work around one recognizable behavior until that behavior is a
usable, independently accepted specification. It is **not a tracker**. Its work items point at board task ids, register rows,
page anchors and receipts that already exist, and it adds a board task only for a missing link. FABLE defines what the
fields and stages mean. FRONTIER schedules the work and deploys the workflow. DATA's adapters may read these files. The
records themselves are prose plus one table.

## 1. The record

Every package file carries these fields in this order. A field with no value says `none` and gives the reason; it is never
omitted.

| field | meaning |
|---|---|
| **id** | `PKG-<area>-<short-name>`; never reused |
| **behavior** | the recognizable behavior in one or two plain sentences, and why a developer needs it |
| **reproduction target** | what a developer can build or predict from the accepted package alone, with no L3 engine |
| **scope: included** | inputs, variants and exceptional paths the package must explain |
| **scope: adjacent obligations** | required work outside the package, each with its current owner and locator. It stays open elsewhere and is never silently dropped |
| **dependencies** | other packages, contracts or verdict cells relied on, with the scope at which they are accepted |
| **owner** | the one accountable completion owner |
| **contributors** | lanes that authored evidence or own canonical files, with the files they own |
| **reviewers** | the named independent reviewer(s). They cannot be an author of the claim reviewed; they come from actual assignment or receipt, never from the requester field |
| **requirement ids** | register rows, L2 verdict cells, contract ids and page questions the package answers or depends on |
| **evidence** | canonical pages and contracts with the controls/receipts behind each stage. Each is labelled static, replay, live or inference |
| **canonical destination** | where the accepted specification lives. Normally the existing pages and contracts, plus one end-to-end reading path in the package file; the package never becomes a second canonical copy |
| **work items** | a table: item, kind (see §3), locator, owner, reviewer, stage, board task id |
| **stage** | the package stage (§2), derived from the work items |
| **blocker / next action** | the single current blocker, or the next action and who takes it |
| **acceptance checks** | the tests a reviewer runs on the final text; they must bind to the final claims and evidence |

## 2. Stages

A work item has one stage. The package stage is the **earliest** stage among its non-adjacent items.

| stage | meaning | leaves when |
|---|---|---|
| `research` | a claim is not yet established | evidence exists with a control, or the item is dispositioned |
| `evidence-ready` | the author has evidence and a self-check | a named non-author review is requested with the claim and evidence bound |
| `review` | an independent reviewer holds it | the reviewer ACCEPTs (→ `incorporation`), or returns a defect (→ `repair`) |
| `repair` | a review defect is being fixed at its cause, including current consumers and a regression | re-submitted (→ `review`) |
| `incorporation` | accepted evidence waits for the canonical owner's edit or acceptance | every affected current consumer carries it |
| `accepted-and-incorporated` | final claims accepted, canonical files updated, consumers agree | never automatically. It goes back to `repair` only when a dependency it rests on changes (claim-level, not package-wide) |
| `dispositioned` | closed by an accepted disposition: out-of-boundary, superseded, transferred with its residue | never. The residue stays listed under adjacent obligations |

**What does not move a stage:** a sent request, a board DONE on a producer task, a green producer check, a published candidate
record, or a peer comment. The one exception: a request can move `evidence-ready` to `review` when the reviewer has claimed it.

**Package complete** means every non-adjacent item is `accepted-and-incorporated` or `dispositioned`, and the acceptance checks
pass on the final text. A package being complete says nothing about the whole database. Adjacent obligations remain debt
wherever they live.

## 3. Work-item kinds

Each kind is counted once, by its own id:
- `claim`: a new or corrected statement;
- `stale-text`: a current consumer contradicting accepted evidence;
- `gap`: required and unread;
- `review`: an acceptance still owed;
- `incorporation`: an owner edit still owed;
- `disposition`.

A dashboard should show them separately, together with accepted answers, transfers, reopened debt and waiting integration. A
stale-text item is a propagation debt, not new research. A gap inside the included scope blocks completion; a gap listed
under adjacent obligations blocks only the full-database goal.

## 4. The pilots

| package | kind | why chosen |
|---|---|---|
| [`PKG-GP-HP-LETHAL`](PKG-GP-HP-LETHAL.md) | recognizable gameplay specification | every stage from damage to KO, rewards and game over is already documented and largely replayed (S-21, S-23 MET). What remains is finishable: stale text, named gaps and reviews, not open research |
| [`PKG-TECH-SCRIPTVM-VALUE`](PKG-TECH-SCRIPTVM-VALUE.md) | evidence-rich technical chain | the ScriptVM's value path from operand to typed store has static reads, ASTRA replays and OPUS records, and FABLE's consumer edits land in canonical pages. It exercises review → repair → incorporation on real items already in flight |

## 5. Further packages (FABLE)

| package | kind | opened |
|---|---|---|
| [`PKG-GP-SPAWN-RESPAWN`](PKG-GP-SPAWN-RESPAWN.md) | gameplay specification: death, group wipe, teardown and respawn; it carries `PKG-GP-HP-LETHAL`'s adjacent body-removal obligation | 2026-09-29 |
| [`PKG-GP-STATUS-POISON`](PKG-GP-STATUS-POISON.md) | gameplay specification: a damaging timed status (Poison; Sap and Regen share the path) from infliction through ticks to expiry, cure or KO | 2026-09-29 |
