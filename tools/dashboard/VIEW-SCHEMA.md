# Dashboard view contract (OPUS, 2026-09-29)

The migration's M3 read-only dashboard serves **only** the CURRENT dashboard generation, which is written through
`gfz-scripts/generation.py`. Each view is one output file, `view-<name>.json`. A view adapter (DATA, per the M3 split in
`_index/workflow/IMPLEMENTATION-MAP.md`) builds it from declared inputs. The server never scans a live source.

## Required views

These are the brief's section 8. A missing required view is shown as **UNMEASURED**, never as empty or green:
`overview`, `systems`, `vbf`, `executable`, `types`, `evidence`, `fleet`.

## One view file

```json
{
  "view": "vbf",
  "title": "VBF archive (the browser's own folder tree)",
  "status": "OK",
  "source": {"identity": "<archive sha256 or board rev ...>", "as_of": "<UTC>", "instrument": "<script@sha>", "limits": "..."},
  "measures": [
    {"id": "files", "label": "files in the archive", "numerator": 89414, "denominator": null,
     "scope": "the archive's file table", "instrument": "...", "as_of": "...", "limits": "..."}
  ],
  "tree":  [{"id": "gamedata", "label": "gamedata", "counts": {"files": 39653}, "children": [...],
             "links": [{"label": "evidence", "href": "<repo-relative path>"}], "state": "UNKNOWN"}],
  "rows":  {"columns": ["..."], "data": [["..."]]}
}
```

**`status`** is one of `OK`, `STALE`, `UNMEASURED`, `FAILED`, `PARTIAL`. A view whose source failed says `FAILED` and why
(`source.limits`); it must never become zeros.

**Measures:**
- Every measure carries `numerator`, `denominator` (a number, or `null` for a plain count), `scope`, `instrument`,
  `as_of` and `limits`.
- The server marks a view **MALFORMED** when a measure lacks any of these, or when `numerator > denominator`. It then
  shows no number from that view.
- No percentage is drawn without both numbers.

**Axes** are kept apart by measure ids and labels: physical, representation, semantic, review and execution. A single
"understanding %" across axes is not a valid measure.

**Tree and rows** are optional. `links` are repo-relative paths.

**`state` on a node** must be a word from FABLE's vocabulary:
- [`FFXII TZA/_index/workflow/DASHBOARD-MEANINGS.md`](../../FFXII%20TZA/_index/workflow/DASHBOARD-MEANINGS.md) §1 (one axis
  per state) and §2 (obligation outcomes);
- the package stages in `completion-packages/README.md` §2;
- or `FAILED` / `STALE`.

The server marks a view **MALFORMED** when a node state is outside that vocabulary, or when the vocabulary cannot be read
(so an unchecked state is never shown as if checked). A scoped L2 verdict is not a completion state; the systems view
carries it in `counts`. Added 2026-09-29 for FABLE-REQ-OPUS-VIEW-SCHEMA-MEANINGS-LINK.

## Deltas, definitions and the live feeds (OPUS, 2026-09-29)

- **`definition`** (per view): the counting-rule version. It is `MP-2` for My Progress, `v2` for executable and `v1`
  for the others; bump it whenever a view's counting rule changes.
  - evidence `v3` (2026-09-30): the view gains `"page": "evidence"` and an `evidence` block (lessons, findings, checks,
    formats, register) drawn by `pages/evidence.html`. Its six measures keep their ids and counting rules; the version
    moves because the view's content changed, so their first delta after the change reads "N/A - definition changed".
  - executable `v2` (2026-09-29, ASTRA `0d9d9330c`): `bytes-overlap` counts unique bytes covered by two or more
    population bodies. `v1` counted additional covers, so a byte in three bodies counted twice (1,759 against 1,758
    on the same image). No delta is taken across the change (`test_build_views` B8, B9).
    ASTRA's REJECT (`0d9d9330c`) is upheld and the helper re-review (ASTRA `1548d3896`) is ACCEPT, scoped to the
    overlap/helper repair; both ratified `verdict:ACCEPT` by SWE2-AUDIT-SPEC at `a95c664bf` (L342, L347).
- **Code identity.** The code a build consumes is a declared input: `build_views.py`, `requirements.py` and
  `uc1_band.py`, the last at the path of the module actually imported (`test_build_views` B10). Generations before
  2026-09-29 do not bind `uc1_band.py`, so their manifests prove the builder's identity but not the helper's
  (ASTRA `c7bd09b49`). Third-party imports (`pefile`) are not bound.
  Ratified: ASTRA `c7bd09b49` is ACCEPT, scoped: the dependency-binding gap is the honest result (SWE2-AUDIT-SPEC
  `a95c664bf`, L344).
- **`delta`** (per measure with a denominator), written by `build_views.annotate_deltas` against the **immediately prior
  coherent generation**: the newest history entry that still verifies. A rejected or tampered one is skipped. The view
  names it in `delta_basis`.
  My Progress's change block (`progress.change`) uses **the same generation**. If that generation has no progress view,
  there is no prior: the block and the measure deltas both say so. It never falls back to an older generation that has
  one, which would compute the change against a generation other than the one `delta_basis` names. This was repaired
  after ASTRA `9e84de620`; `test_live.py` D6 and D7 cover it.
  The rejection `9e84de620` is upheld (L336). The repair's re-verification R2 (ASTRA `6bc6d481a`) is ACCEPT, scoped
  to the exact `17d6cdc29` selectors, change expression and annotator (L340); ASTRA did not execute D6 and D7. Both
  ratified `verdict:ACCEPT` by SWE2-AUDIT-SPEC at `a95c664bf`.
  `MY-PROGRESS-METRICS.md` §4 still states a day-boundary checkpoint. That disagreement stays open with its meaning
  owner under `OPUS-NOTICE-DATA-DASHBOARD-DELTAS`.
  - `{"pp": x, "old", "new"}` when the view definition, the measure id, its scope and its denominator are all unchanged.
    `x` is percentage points (`100·n/d − 100·n′/d′`), never relative growth.
  - `{"na": "scope changed" | "N/A - definition changed" | "no prior", "why", "old", "new"}` otherwise. A grown denominator
    is therefore neither a regression nor progress.
  - The page shows the delta as coloured text only: green for progress, red for regression, muted `0.0%` and muted
    labels.
- **`direction`** (per measure): `up` (a rise is progress), `down` (a rise is regression) or `none` (a population with
  no good direction), declared in `build_views.DIRECTIONS` (FABLE's rule, `FABLE-REQ-OPUS-DELTA-COLOUR-DIRECTION`).
  - A rise is green for `up` and red for `down`, and a fall the reverse.
  - `none` is muted whatever the sign, and a measure with no declared direction is `none`, never `up`. A newly
    registered OPEN row, for example, turns `register-open` red.
  - `test_build_views` B7 fails when any overview, executable or progress measure has no declared direction.
- **`measures-history.jsonl`** (store root, outside every generation): one line per commit, holding
  `[view, definition, id, numerator, denominator]` for later trend charts. Nothing reads it back as data.
- **`/api/live`**: the next FULL reconciliation, from the controller's own state.
  - `next_at = dashboard.last_run + DASH_INTERVAL`. The interval is read from `swe2_watchdog.py` (1800 s) unless the
    state carries `dashboard.interval`.
  - States: OK, REFRESHING (`building.json` present), FAILED (the last build exited non-zero; retry at `next_at`), OVERDUE
    (more than two polls late), or UNKNOWN (heartbeat stale, state unreadable, or no build recorded). The page never counts
    down from a guess.
- **`/api/activity`**: Agent Activity. It reads the live board and the controller feed (the newest `poll` event, and
  `claude_lanes`) and places tasks with the served generation's facts and category map (`activity.py`). It is cached for
  10 s, reads files only, and makes no model call.
  A lane with no feed is `recent` only if **it issued** a board operation within an hour. That is read from the board's
  operation history, whose `agent` is the identity `team.py apply` ran as. A task's `updated_at` is never used: it says
  when a row changed, not who changed it. So a review another lane queues for this one credits the queuing lane, and this
  lane's own `note` counts even though it changes no task timestamp. No history means no recent write, and the lane is
  UNKNOWN. This rule was repaired after ASTRA's REJECT of 8ddc8c7e8 (`00fd54fda`); `test_live.py` A8 and A9 cover it.
  ASTRA's REJECT (`00fd54fda`) is upheld (L327). R2 (ASTRA `8380c611c`) is ACCEPT, scoped to the writer-attribution
  repair on synthetic classification (L335). Both ratified `verdict:ACCEPT` by SWE2-AUDIT-SPEC at `a95c664bf`.

## DB_GOAL chain, Depth diagnostic and Source/Freshness drawer (SWE2-FRONTIER, 2026-10-03)

The user's context-refresh package v3 (`08_DASHBOARD_REQUIRED_UPDATE.md`) and improvement addendum section 1. Test:
`test_dashboard_base.py`.
- **`progress.db_goal` / `glance.db_goal`** (`db_goal_block`): goal_gate.py's own `verdict` / `remaining` / `next` /
  `detail`, verbatim, never inferred from the board. The glance page shows `remaining` as well.
- **Depth**: the title, the OVERALL label and the glance tile say "weighted diagnostic (not DB_GOAL)". The view carries
  `diagnostic` (`is`, `is_not`, `never_combined_with`, `completion_authority`), and the tab is "Depth (diagnostic)".
- **Input `knowledge_check`** = this build's `knowledge_db.py check` text (volatile). **`glance.provenance`**
  (`provenance_block`) carries generated at, source commit, board revision and epoch, the progress reporter's freshness
  state and fingerprint, the knowledge.sqlite check (CURRENT / STALE + the stale tables / UNMEASURED), the goal-gate
  identity, and the lifecycle file hash once that input exists. The page's Source / freshness drawer adds the served
  generation id, `committed_at` and the stale sources from the server's `meta.drift`.

## Lifecycle panel (SWE2-FRONTIER, 2026-10-03)

FABLE-REQ-FRONTIER-DASHBOARD-LIFECYCLE-1003; meanings in `DASHBOARD-MEANINGS.md` section 6. Test: `test_lifecycle.py` (L1-L9).
- **Input `lifecycle`** = `_index/workflow/PROJECT-LIFECYCLE.json`, strict (a change makes the served generation STALE),
  `required: False`. If the file is absent, malformed or names an unknown phase, the panel is FAILED, never a default.
- **`progress.lifecycle` / `glance.lifecycle`** (`lifecycle_block`):
  - `phase` is the file's `current_primary_phase`, read and never computed.
  - The gate verdict and `requirements_ready` are shown beside the phase and never move it; parity pilots and the
    board are not inputs.
  - A file declaring a later phase than DB_GOAL supports is shown with `declared_phase` and a DISAGREEMENT note, never
    as current (meanings 6.1 rule 3). Probes are labelled `PROBE (database phase)`.
  - The block also carries the phase list, the transition chain with user authorization, the original game as oracle
    (never the production backend), the validation chain and the modding statement.

## Recent meaningful changes (SWE2-FRONTIER, 2026-10-03)

Improvement addendum section 2; DASHBOARD-MEANINGS 6.3. Test: `test_recent_changes.py`.
- **Input `recent_changes`** = this build's `recent_changes.py --json` (FABLE, `a065b24fa`), volatile, `required: False`.
  The contract was agreed with FABLE: `events[]` carries `class` (the addendum's nine long names or `UNCLASSIFIED`),
  `axis`, `at`, `title`, `identity`, `commit` and `evidence{kind, ref}`; `windows{24h, 7d}.since`, where 24h is the subset of
  7d with `at >= since`.
- **`glance.recent_changes`** counts knowledge / activity / unclassified per window, separately and never summed, and
  lists knowledge events with their canonical evidence. It never classifies. An unknown class string makes it PARTIAL
  and is named. If the output is absent it is UNMEASURED, never zero.

## Next highest-value work (SWE2-FRONTIER, 2026-10-03)

Improvement addendum section 11. Test: `test_next_work.py`.
- **`glance.next_work`** (`next_work_block`): the gate's `remaining` / `next`, plus board tasks placed in the addendum's
  seven buckets by board fields, first match wins:
  1. BLOCKS DB_GOAL NOW - the task names an open register row;
  2. AWAITING INDEPENDENT REVIEW;
  3. AWAITING INTEGRATION;
  4. RUNTIME / LIVE AUTHORIZATION NEEDED;
  5. TOOLING BLOCKER - P0/P1 with a dashboard or kit file key;
  6. HIGH-VALUE NONBLOCKING KNOWLEDGE - other P0/P1;
  7. POST-DB / DEFERRED.
  Inside a bucket the board's own order applies (priority, ACTIVE first, id). `unowned_blockers` lists open register
  rows that no task names. There is no score, no age term and no second scheduler.

## Evidence lineage on the systems view (SWE2-FRONTIER, 2026-10-03)

Improvement addendum section 6. Test: `test_lineage.py`.
- Each registered system node carries `lineage`: nine steps (system / mechanism, current claim, structured contract,
  static/native, isolated original-code, live, review/acceptance, downstream consumers, reconstruction probe/parity).
  Each step is `present` / `not required` / `not measured` / `unknown` / `not yet available`, with a reason, from
  `important-subsystems.tsv` and `L2-VERDICTS.md`. The steps are mirrored into `counts` as `lineage N. <step>`. The
  node also links its contract and the L2 verdicts file. A step no current structure answers per system says so; none
  is left blank or implied required.

## Production system status residue (SWE2-FRONTIER, 2026-10-03)

The user's FFXII_INDEPENDENT_CORPUS_AUDIT_FOLLOWUP_2026-10-03, section 9. Test: `test_status_residue.py`.
- **View `residue`** (`v_residue`, tab "Status residue"). Input `status_residue` = this build's
  `check_status_residue.py --json` (FABLE). It counts system pages by status word (AUDITED / DOCUMENTED / PARTIAL /
  REOPENED), then splits the PARTIAL / REOPENED pages into LIVE-ROW / PROCESS-ONLY / UNMAPPED, listing UNMAPPED first.
  It is UNMEASURED without a census and has no score.

## System readiness view on the systems view (SWE2-FRONTIER, 2026-10-03)

SWE2-STRUCT's `readiness_view.py` (HOOK.md, `_index/candidates/swe2struct-design-readiness-views-1003/`;
SWE2STRUCT-REQ-FRONTIER-READINESS-VIEW-HOOK-1003). Test: `test_readiness_hook.py`.
- **Input `readiness`** = this build's `readiness_view.py --out` TSV, `required: False`. It is captured with `--board`
  at the live TEAM.json at capture time. That is not byte-bound to the generation's `team` snapshot; `board_open` is
  coordination load only. A missing capture makes every system read UNMEASURED.
- Each registered system node's counts gain:
  - "open obligations under this system" from `register_live` / `register_closed`;
  - `maturity` (SPECIFICATION READY or no label, with the withholding conditions);
  - `parity probes (PROBE, database phase)`;
  - the remaining columns as `readiness: <col>`.
- Maturity stays in counts, not the node `state`: the state vocabulary is DASHBOARD-MEANINGS sections 1-2.
- The phase cap: a label past SPECIFICATION READY reads WITHHELD. Columns are never summed and no percentage is drawn.
