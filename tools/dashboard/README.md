# FF12 database dashboard (migration M3)

This is a read-only, loopback-only view of the database. It is built by code from declared inputs and makes no model
call. The contract is in [VIEW-SCHEMA.md](VIEW-SCHEMA.md), and the plan is `FFXII TZA/_index/workflow/IMPLEMENTATION-MAP.md`
(M3).

## Use

For the user: **double-click `START-DASHBOARD.cmd`** in this folder — it builds once if needed,
starts the loopback server under `supervise.py` and opens the page. `STOP-DASHBOARD.cmd` stops both. No shell commands
are needed for routine use. **No restart is needed after a code change** (2026-09-30): the supervisor restarts the server
within a few seconds when any dashboard module or `generation.py` changes, keeps the running server when a change does
not compile, and an open page reloads itself when it sees the new server code.

```
START-DASHBOARD.cmd                        # user entry: build + serve + open http://127.0.0.1:8765/
STOP-DASHBOARD.cmd                         # stop the supervisor and the server
python build_views.py                      # one generation into Database/Tools/work/dashboard (gitignored); ~25 s
python server.py --root ../work/dashboard  # http://127.0.0.1:8765/  (loopback only; GET only)
python supervise.py --root ../work/dashboard  # the same, restarted automatically on code changes
python ../analysis-kit/gfz-scripts/generation.py status ../work/dashboard
python ../analysis-kit/gfz-scripts/generation.py export ../work/dashboard <out.zip>   # verified portable snapshot
```

**Controller refresh (deployed 2026-09-29, SWE2-FRONTIER).** `swe2_watchdog.py
maybe_dashboard_build` runs `build_views.py` from the controller loop: on a TEAM.json
transition debounced to one build per 5 min, plus an unconditional 30-min reconciliation.
Trigger/tick receipts are `dashboard_build` events in the controller log; the generation
store's `history.jsonl` / `FAILURE.json` record each build's outcome.

**Refresh.** Run `build_views.py` again; the open page picks up the new generation within 5 s.
- A build whose strict input moved mid-build is refused and retried, up to three attempts. The previous generation stays
  current, and the failure is shown separately.
- The board and the watchdog state are declared volatile: they are read only from their snapshots.

**Scheduling (FRONTIER).** Run the build from the existing controller timer and after board transitions. Suggested:
debounced after a transition, and every 30 minutes for the full rebuild. The page itself only reads a status file every
5 s.

## What each view measures today (first-pass adapters, OPUS; DATA extends them)

| view | source (snapshotted) | status | not yet measured |
|---|---|---|---|
| journey | *Player progression* (`pages/journey.html`, modelled on the DWNO atlas and the Wizardry player tab): the game's content as a player meets it, in its own names (`ff12_content.py` over the installed archive's battle pack and world-map files, and the hub's enemy catalog). `build_views.journey_tree` nests it by in-game category (The world, Characters, License Board, Battle, Items & equipment, Bestiary, Story & quests), then by groups taken only from the game's own data: world-map region/area records, table category fields (`group` + `group_basis`), party row kind, catalog boss/hunt flags. Duplicate names collapse into one entry; unused slots get their own group. The page is a breadcrumb browser with a list/detail pane, search, filters, paging and cross-links between entries. Each entry shows its player-facing `sections`; the sources, keys and raw rows are under "for modders". Each category shows its My Progress understanding and co-op support from `_index/workflow/coop-support.tsv` | OK | understanding is a category measure, not per item; co-op is unmeasured (a dash) until the ledger has rows; 107 maps have no world-map placement in the files; story scenes and side quests are not yet catalogued; values appear only where a database page documents the field |
| glance | *At a glance*, laid out like the DWNO database dashboard (`pages/glance.html`): headline tiles, progress over generations (from `measures-history.jsonl`), the priority ladder and lanes (board records, commit subjects), the register by section, the audit exchange (board review verdicts) and recent commits (`git log` captured every build) | OK | lanes count records and commits, not effort; review verdicts are read from each task's note |
| depth | `progress.py --json`, run every build: its weighted OVERALL and eight dimensions (engine_explained 0.55 counts a function only when an evidence page explains it) | OK | none of its own; it is a second metric beside My Progress, never summed with it |
| overview | goal gate + register counts (captured instrument outputs), package stages | OK | package stages as FABLE records them, not derived from work items |
| systems | category folders, the 52 registered systems and their L2 verdict cells | OK | per-system register rows and requirements drill-down |
| vbf | the archive file table (the browser's own folder tree) to depth 3, extensions | PARTIAL | the archive is not yet pinned by hash; formats, parse, schema and field meaning |
| executable | every `.text` byte once: listed / frontier (uc1_band population) / EH funclet / held / int3-nop fill / UNKNOWN, overlaps counted once (bytes-overlap = unique bytes in two or more bodies, definition v2), largest UNKNOWN gaps; plus `COVERAGE-DIMENSIONS.md` | PARTIAL | behavior (READ / EXPLAINED) and observed execution; data inside `.text` beyond held rows is UNKNOWN until ruled; multi-byte NOP fill counts as UNKNOWN |
| types | `types.tsv` / `fields.tsv` readiness counts | OK | byte-level extent coverage; meaning is a separate axis |
| evidence | *Evidence & lessons* (`pages/evidence.html`, definition v3, modelled on the Radiata dashboard's Evidence tab): review health (board review/sign/verify tasks, structured verdicts, seal receipts, pending propagation); the lessons ledger (`_index/CONTRADICTIONS.tsv`, states as `goal_gate.py` reads them) and RULES.md's instrument findings; verification checks (goal gate, check_questions and progress_report as captured every build, plus the read-only checkers in `run_checks.CHECKS`, run in parallel, each with status PASS/FAIL/UNMEASURED, exit, seconds, key numbers and full output; the slow or file-writing ones are listed in `run_checks.EXCLUDED`); the format registry (the archive census TSV joined with check_assets' verdicts); the question register (check_questions' own classify, status filter and search) | OK | a checker's key numbers are read from its printed output; document links copy a repo-relative path (the server serves no database files) |
| fleet | board ACTIVE claims, watchdog in-flight | PARTIAL | model, effort, account limits and utilisation (UNKNOWN) |

A view whose adapter fails is shown FAILED, with the reason. A missing required view is shown UNMEASURED.

## Tests

| test | cases |
|---|---|
| `test_server.py` | S1-S9 |
| `test_build_views.py` | B1-B15, against the real database into a scratch store |
| `../analysis-kit/gfz-scripts/test_generation.py` | G1-G12, E1-E3, C1 |
