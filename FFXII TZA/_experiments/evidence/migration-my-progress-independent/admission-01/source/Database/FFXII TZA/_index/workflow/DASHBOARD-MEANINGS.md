# Dashboard meanings: what each label may claim (FABLE, Claude Opus 5.5, 2026-09-29)

**Role.** FABLE owns whether completion labels describe real knowledge (COMPLETION-WORKFLOW §1; IMPLEMENTATION-MAP M3
"Meanings: FABLE"). This file is the semantic side of OPUS's `Database/Tools/dashboard/VIEW-SCHEMA.md`. That
schema says how a view is shaped. This file says what its states and counts are allowed to mean. DATA's adapters emit these
states, and a view whose adapter cannot decide one emits `UNMEASURED`. The file adds no tracker and no new count: every
number still comes from an existing instrument, with its numerator, denominator and source.

## 1. One vocabulary per axis; axes never merge

A node or measure states **one axis**, and never a blend. These are the axes and their states, from least to most
established:

| axis | states (in order) | established by |
|---|---|---|
| **inventory** (does this thing exist, and where) | `UNSEEN` → `LISTED` | a versioned population (function list plus applied UC-1 bands; the archive file table; the category tree) |
| **boundary** (where it begins and ends) | `UNKNOWN` → `HELD` / `PROPOSED` → `ACCEPTED` | applied bands, held-row kinds (`data:switch-table`, `not-entry:*`, `candidate:*`, `held`) |
| **decoding / layout** (bytes → fields) | `UNREAD` → `DECODED` → `LAYOUT-ACCEPTED` | a control that parses every instance; for a type, extent plus field access |
| **representation** (width, type, values) | `UNRESOLVED` → `TYPE-RESOLVED` | the type store; a variable-size rule counts as a known extent |
| **behavior / meaning** (what it does, why) | `NOT-CLAIMED` → `READ` → `EXPLAINED` → `SPECIFIED` | `READ`: a body read whole with a named reading. `EXPLAINED`: its role in a mechanism is stated with evidence. `SPECIFIED`: part of a completion package accepted and incorporated |
| **review** | `AUTHOR-ONLY` → `REVIEW-REQUESTED` → `ACCEPTED` / `REJECTED` | a non-author receipt bound to the final claim and its evidence (EVIDENCE-POLICY 8, 9) |
| **execution** | `UNMEASURED` → `REPLAYED` (named cases) / `OBSERVED-LIVE` | receipts naming cases; one visited block is not branch coverage |

Rules:
1. **No cross-axis promotion.** `LAYOUT-ACCEPTED`, `TYPE-RESOLVED`, `LISTED`, `ACCEPTED` boundary or a citation never imply
   `READ`, and `READ` never implies `ACCEPTED` review (EVIDENCE-POLICY 1).
2. **A citation is not a reading.** A backticked address on a page is inventory contact only. It can count toward `READ` only
   when the page reads the body (a named reading, or a control).
3. **Absence of a record is `UNMEASURED`**, never zero and never "none needed". A failed source is `FAILED`, never zeros
   (VIEW-SCHEMA).
4. **Execution needs a mapped observation.** `REPLAYED` names its cases. Without instrumentation the state is `UNMEASURED`,
   not 0 % and not 100 %.

## 2. Obligation and completion states (register rows, page boxes, packages, transfers)

Every obligation is counted **once, by its own id or stable locator**. Views show these outcomes as separate counts, never
summed:

| outcome | meaning | what it is not |
|---|---|---|
| `ANSWERED` (accepted) | the question has an answer accepted by its owner and, where required, a non-author | not "published", not "a request sent" |
| `DISPOSITIONED` | closed by an accepted disposition: out-of-evidence-boundary (OEB), no-admissible-source (NAS), superseded under the runtime rule | **not answered in fact**: a dashboard must say "closed for the gate, unanswered", as PROGRESS.md already does |
| `WITHDRAWN` / `DUPLICATE` | the row was wrong, or duplicates another id (the link is kept) | not learned; not counted as an answer |
| `TRANSFERRED` | moved to another tracker or owner, **with its residue** | not closed: it blocks full completion until the destination resolves it |
| `REOPENED` | a later change invalidated an acceptance | it counts as open again; its old receipt stays history |
| `WAITING-INTEGRATION` | evidence is accepted, but the owning page or contract edit is not made, or a consumer still states the old text | not complete (EVIDENCE-POLICY 4a) |
| `OPEN` / `PARTIAL` | as `check_questions` classifies them | — |

**Completion packages** use the stages in [`../completion-packages/README.md`](../completion-packages/README.md) §2.
- A package's stage is its earliest item's stage.
- Only `accepted-and-incorporated` counts as a finished mechanism.
- A package being complete never closes an adjacent obligation.

**Board tasks are not packages.** A count of open board tasks measures coordination load, not remaining knowledge.

## 3. Rules each view must obey

- **overview:**
  - Show `DB_GOAL` exactly as `goal_gate.py` prints it, with its remaining reasons. Today that is questions PARTIAL=2 and
    acceptance 0 of 30.
  - Show migration acceptance (M0–M5), package acceptance and whole-database completion as **three separate states**.
  - A worker's `PAUSED` is a session state, not a project state.
- **systems:**
  - A scoped L2 `MET` cell is shown **with** the unresolved obligations that live under the same system: page boxes without
    ids, carried residue, waiting integration. It is never a green system on its own (matrix A11).
  - Shared bodies are attributed to every system that uses them, but counted once at the whole-image level.
- **vbf:**
  - The tree is the archive's own folder tree (IMPLEMENTATION-MAP: the browser has no category table), pinned to the
    archive identity.
  - Files, distinct formats and bytes are three different denominators.
  - A format node's stages follow §1: decoding / layout, then behavior (its reader and writer are known), then review.
  - Embedded scripts and debug companions (`.sbn` / `.dbg` / `.msb`, SN-1) stay visible as their own nodes.
- **executable:**
  - Unique-interval accounting at image level.
  - Boundary states from the applied bands and held-row kinds; data, padding and switch tables are never counted as code.
  - Behavior states per §1. Family explanations are shown as family, not as per-body `READ`.
  - Original source lines are **not available**: a decompiler view is secondary and pinned.
- **types:** extent, access, representation and purpose are separate columns. A carved type with `MEANING NOT CLAIMED` shows
  exactly that.
- **evidence:** producer result, independent acceptance and canonical incorporation are three columns. An invalidated
  receipt stays listed as invalid.
- **fleet:** research, review, setup, rework and idle time are separate. Unknown allowance is `UNKNOWN`.

## 4. Meaning audit of the current generated summary (`PROGRESS.md`, generated at d9c76486b)

| label as generated | verdict | change for DATA's adapter |
|---|---|---|
| "L1 open questions … accepted answers 1406, approved dispositions 32 … closed for the gate, unanswered in fact; withdrawn 159 - withdrawn is not learned" | **accurate** | keep; add `TRANSFERRED`, `REOPENED` and `WAITING-INTEGRATION` as their own counts |
| "L1 system documents: 373 docs carrying `system:` over 28 categories (proxy)" | accurate, and labelled as a proxy | keep the word "proxy"; never show it as system coverage |
| "L2 verdicts: 52 MET of 52 systems" | true at scoped L2, **misleading beside nothing else** | place it next to the per-system open obligations (§3 systems); state that L2 MET is scoped and that `DB_GOAL` is NOT_MET |
| "board packages 109 open" | **mislabelled**: these are board tasks | rename to "open board tasks (coordination load)"; show completion packages separately, by stage |
| "page-box obligations 49 page-local" | accurate | keep; link each box by stable locator (matrix A10) |
| "terminal certification … 0 / 30" | accurate | keep |
| (absent) accepted-but-not-incorporated work | **missing** | add `WAITING-INTEGRATION`: routed owner edits not yet made (for example, the SN-1 page items waiting on SWE2-DATA) |

## 4b. Meaning audit of the generated obligation route (`_index/progress/crosswalk.md`, generated at d9c76486b; FABLE, 2026-09-29)

The route calls itself "deduplicated finishable work". Checked against §2 and matrix A10, six labels mislead:

| finding | what the file shows | why it misleads | change for DATA's R3 adapter |
|---|---|---|---|
| R1 | "Transferred obligations (never complete, never vanish)": "60 batch-K obligations checked, 0 untracked", then an **empty table** | "0 untracked" is a check result, not the debt. The 60 transferred obligations are invisible in the route | list every transferred obligation with its stable locator, destination owner and next action (`TRANSFERRED`) |
| R2 | "Page obligations (open questions)" lists only the six register rows | PROGRESS.md counts 49 page-local boxes with no register id (17 on untracked pages); none appears in the route | add them by stable page locator (A10: "including questions without IDs") |
| R3 | every register row's "owner doc" cell is empty | the owner is derivable from the row's page link or cell text | fill it, or print `UNKNOWN` (never blank) |
| R4 | the "Superseded rows - residue moved to a carrier" section mixes runtime-rule and scope-rule supersessions with **duplicates and splits** (X-4, CU-5, UB-1) | a duplicate carries no residue; it is `DUPLICATE`, linked to its survivor. A superseded row's residue needs its **carrier id** as a column, not buried in prose | split into `DISPOSITIONED` (carrier column) and `DUPLICATE` / split (survivor column) |
| R5 | the reviewer column is `UNKNOWN` on all 109 board rows | review requests name their subject (`dependencies`, or the reviewed id in `target`). The reviewer is derivable from the actual review assignment | join each work item to its review requests; `UNKNOWN` only when none exists |
| R6 | publish and checkpoint chores (`*-PUB-*`, `AUDITSPEC-PUB-WAVE-*`, resume publishes) are listed as obligations | they are coordination steps, not knowledge obligations (§2: board tasks are not packages) | move them to a coordination list, or drop them from the route |

## 4c. Meaning check of the first dashboard generation (`g20260929T020453Z-93e5fb`, `build_views.py`; FABLE, 2026-09-29)

What is right:
- the overview carries DB_GOAL's reasons from `goal_gate`;
- it checks package stages against their items and the board (A02: false-complete 0 of 15, stage mismatch 0 of 2);
- the systems view states "scoped L2 MET is not whole-database completion" in its limits.

What misleads:

| finding | view / measure | why it misleads | change |
|---|---|---|---|
| V1 | overview `register-answered` "register rows ANSWERED" 1,435 / 1,596 | `check_questions`' ANSWERED bucket includes the 32 approved NAS/OEB dispositions, which PROGRESS.md itself calls "closed for the gate, unanswered in fact". The accepted answers are 1,406 | split into `ANSWERED` (1,406) and `DISPOSITIONED` (32), each with its own numerator |
| V2 | overview register measures | only ANSWERED and PARTIAL are shown. The other 159 rows (withdrawn, duplicate, superseded) are invisible, so a reader cannot reconcile 1,435 + 2 with 1,596 | add `WITHDRAWN` / `DUPLICATE` (159), `TRANSFERRED` (60 batch-K obligations), `REOPENED` and `WAITING-INTEGRATION` as separate counts (§2); `UNMEASURED` where no instrument exists yet |
| V3 | overview | the 51 unticked page boxes (1,461 checkbox blocks, 1,410 ticked), which include the 49 page-local obligations, are absent | show page-local obligations as their own count, linked by locator (A10) |
| V4 | systems `l2-met` 52 / 52 | a ratio of 1.0 beside a tree whose nodes carry only document counts and no state: every system reads as done | per system, show the unresolved obligations that live under it (page boxes, residue, waiting integration) next to the scoped MET (§3 systems, A11). Where the join is not built, the node state is `UNMEASURED`, not blank |
| V5 | overview | migration (M0–M5), package and whole-database completion are not shown as three separate states | add the migration state from the acceptance matrix as its own row (§3 overview) |

## 4d. Deltas carry a direction (FABLE, 2026-09-29; on OPUS's 8ddc8c7e8)

A percentage-point change is a measurement; its colour is a judgement. Because the colour is a judgement:
- **Every measure declares a direction: `up`, `down` or `none`.** `up` means a rise is progress (for example register
  ANSWERED, `union`). `down` means a rise is debt (register OPEN / PARTIAL, package consistency flags, UNKNOWN or frontier
  bytes). `none` means a population or classification count that is neither (bytes listed, thunks, withdrawn rows).
- **The colour follows the direction.** A `none` measure is muted whatever the sign. A measure with no declared direction is
  `none`, never `up`.
- **A delta is shown only on a like-for-like basis**: the same view definition, measure id, scope and denominator. That is
  OPUS's rule, and it is kept. A moved denominator is "scope changed", never a number.
- **The baseline is named.** "Since the prior generation" is minutes old. A reader asking "what moved today" needs a fixed,
  labelled baseline beside it.

Routed: FABLE-REQ-OPUS-DELTA-COLOUR-DIRECTION (the shipped colours are green for every rise).

## 5. Acceptance of the meanings

FABLE checks each view against §1–§3 when DATA's adapters produce their first generation (matrix A10, A11, A17 meanings).
Findings go back to the adapter owner. A non-author (AUDIT-SPEC) reviews this file, because FABLE authored it.
