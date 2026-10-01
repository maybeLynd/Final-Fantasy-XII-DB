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
