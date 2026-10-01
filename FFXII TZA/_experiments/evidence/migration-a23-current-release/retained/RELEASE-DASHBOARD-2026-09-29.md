# Dashboard release record, 2026-09-29 (OPUS; matrix A23, with FRONTIER)

**Status: DELIVERED, NOT ACCEPTED.**
- A23 needs independent receipts from SOL/ASTRA and the relevant auditors. Until one names these commits, A23 is NOT_RUN.
- This record states what is deployed and how to roll it back. It does not certify anything.

## 1. Deployed versions

| component | source | commit |
|---|---|---|
| dashboard server (read-only, 127.0.0.1:8765) | `Database/Tools/dashboard/server.py` | 763d466d6 (current; served-content verification since e8999f966, ASTRA's same-stat repair) |
| view builder | `Database/Tools/dashboard/build_views.py` | 763d466d6 (current; My Progress adapter since 605882fdc) |
| requirement catalog (My Progress, MP-2) | `Database/Tools/dashboard/requirements.py` | 7aaa2f8bd (MP-1 at 605882fdc) |
| generation library (manifest `ff12-generation-2`) | `Database/Tools/analysis-kit/gfz-scripts/generation.py` | 225465c2e |
| launchers | `START-DASHBOARD.cmd` / `STOP-DASHBOARD.cmd` (FRONTIER) | 6be90c7ee |
| metric definitions and category map | `_index/workflow/MY-PROGRESS-METRICS.md`, `my-progress/category-map.tsv` | 605882fdc |

- **Running process:** the dashboard server, pid 71184, restarted 2026-09-29 about 07:33Z (earlier pid 46136, then 39660 and 67816) with
  `python server.py --root Database/Tools/work/dashboard --port 8765`.
- **Self-check:** `/api/status` reports `reader_stale: false`, meaning the running code equals the files on disk.
- **Controller builds:** these are FRONTIER's (`maybe_dashboard_build`). They do not run until the controller process is
  restarted (OPUS-REQ-FRONTIER-CONTROLLER-RESTART-0929); until then generations are built by hand.

## 2. Launch

- Double-click `Database/Tools/dashboard/START-DASHBOARD.cmd`. It builds once and serves CURRENT.
- Or run `python build_views.py` and then `python server.py --root ..\work\dashboard`, both from `Database/Tools/dashboard`.
- The page opens on **My Progress**, and every existing view stays behind its tab.

## 3. Matching portable snapshot

| generation | export | sha256 | verification |
|---|---|---|---|
| g20260929T031017Z-483ba2 (serving at the time of this record) | `Database/Tools/work/dashboard-exports/g20260929T031017Z-483ba2.zip` (32 members) | `ff0fcbd7b381535077c7ce15f22ec962e1651c1c99a2a3b19b111a5baca320ca` | `generation.py verify-zip` → VERIFIED |
| g20260929T075521Z-fbf2f8 (serving after 763d466d6; exported with the repaired verifier f145d442f) | `Database/Tools/work/dashboard-exports/g20260929T075521Z-fbf2f8.zip` (33 members) | `595f86d6e856333a648d4707af66450b3cd695abe7f4acefc20cb1a0d17049b3` | `generation.py verify-zip` at f145d442f → VERIFIED; the earlier export also still VERIFIES under it |

- **External dependency:** the certified EXE is an external input. It is hashed in the manifest, never copied, so the
  export is portable except for it.
- **Location:** the export lives in the work area, not in Git.

## 4. Tests (author runs at these commits)

| suite | cases | result |
|---|---|---|
| `dashboard/test_server.py` | S1-S17 | FAILS 0 at 763d466d6 (S17 fails on 605882fdc's server: FAILS 1) |
| `dashboard/test_requirements.py` | MP1-MP12 | FAILS 0 at 763d466d6 |
| `dashboard/test_build_views.py` | B1-B7 | FAILS 0 at 763d466d6 |
| `dashboard/test_live.py` | A1-A7, D1-D5, T1-T5, J1-J4 | FAILS 0 at 763d466d6 |
| `gfz-scripts/test_generation.py` | G1-G15 | FAILS 0 at 225465c2e |

## 5. Independent receipts

| receipt | verdict | follow-up |
|---|---|---|
| SOL/ASTRA, incident verification (cccd7c04c) | **REJECT**: a same-stat edit escaped the stat-only cache key | repaired at e8999f966; re-verified below |
| SOL/ASTRA, the cache repair (dcc53dc22, `migration-dashboard-cache-r2/`) | **ACCEPT, scoped**: the same-stat edit is refused on the next request, and the fallback and stale controls work, on published 622c0866d (cache code equal to e8999f966) | limits: request-time re-verification within the 60 s bound, not idle checking; loaded module, PID and current deployment unaccepted; 8ddc8c7e8 and later not covered |
| My Progress, non-author | R3 **ACCEPT, scoped** to the terminal-count admission (ASTRA e66925f24); synthetic inputs, no builder or deployment acceptance | OPUS-REQ-ASTRA-VERIFY-MY-PROGRESS-R3 |
| My Progress meanings (FABLE) | **delivered: ACCEPT with C1-C4** at 62c566676 ([`mp1-meanings-review`](../candidates/mp1-meanings-review/README.md)); C1-C4 applied at 622c0866d (MP-2). A meaning receipt, not a non-author verification of the counts | - |
| My Progress counts | pending | OPUS-REQ-DATA-MY-PROGRESS-METRICS |
| prerequisites (A03) | **ACCEPT, scoped** at 1f11830e9 (ASTRA fe4bc030b) | the first legacy pair remains an invalid API call, not semantic evidence |
| transitions (A14/A16) | **REJECT** (ASTRA 888afe2e4), then R2 **ACCEPT, scoped** to read-only admission (ASTRA 117f85ab6) | repaired f21fe8044; the write campaign under --apply stays NOT_EXECUTED |
| dashboard shell, generation library | shell: **ACCEPT, scoped** to selected-view admission over real HTTP at 69bbf8c81 (ASTRA c466fc472: valid OK, hash-declared non-JSON MALFORMED, missing UNMEASURED, FAILED retained; rendering, navigation, taxonomy, the loaded module and PID, scheduler, restart and export stay open). A09 certification R3 **ACCEPT, scoped** to the unknown-input-state repair (ASTRA 70a134f63) | OPUS-REQ-ASTRA-VERIFY-DASHBOARD-SHELL, -A05-A09-GENERATION |
| Agent Activity, deltas, countdown (8ddc8c7e8) | **REJECT, scoped to activity-writer attribution** (ASTRA 00fd54fda, `migration-activity-deltas-independent/`): a review another lane queued credited the recipient with a board write, and a lane's own note was missed. Deltas, rendered UI and the loaded module stay untested by that package | repaired: writes now come from the board history's issuer (test_live A8, A9). **R2 ACCEPT, scoped** (ASTRA 8380c611c) on 0bec2215d. Deltas: ASTRA 9e84de620 found the progress change block using a different prior generation than delta_basis; repaired at 17d6cdc29 (one basis, D6/D7), re-verification OPUS-REQ-ASTRA-VERIFY-DELTA-ONE-BASIS |

## 5b. Later deployments the same day (OPUS, 2026-09-29)

| commit | what | deployed | verification |
|---|---|---|---|
| e8999f966 | served content hashed each request (ASTRA's same-stat REJECT repaired) | server only, pid 46136 | OPUS-REQ-ASTRA-REVERIFY-DASH-INCIDENT-CACHE-R2 |
| 622c0866d | My Progress MP-2 (FABLE C1-C4; bin/dat as a named gap) | builder, server | OPUS-REQ-ASTRA-VERIFY-MY-PROGRESS-R2, OPUS-REQ-DATA-MY-PROGRESS-METRICS-R2 |
| 8ddc8c7e8 | Agent Activity tab, percentage-point deltas, the full-refresh countdown (user request) | server only, pid 39660; generation g20260929T061717Z-4720b8 | OPUS-REQ-ASTRA-VERIFY-AGENT-ACTIVITY-DELTAS-TIMER |
| 7aaa2f8bd | DD split: documented with all residue answered vs with a dispositioned residue (FABLE's status ruling) | builder, server | covered by the MP-2 verification |
| 763d466d6 | each measure declares a direction; a delta's colour follows it, so a rise in open rows is red (FABLE-REQ-OPUS-DELTA-COLOUR-DIRECTION) | builder (the controller's build g20260929T072902Z-b80641 started after the patch) and server (pid 71184) | not yet requested; test_build_views B7, test_live J4 |

Rollback for these follows section 6 unchanged. Each is a code change; no generation is rewritten.

## 6. Rollback

**Scope.** Rollback changes feature code and configuration only. It never reverts, deletes or rewrites database
content, accepted research history, the board, or a committed generation. The generation store is derived data, and its
generations stay as they are.

**Steps:**
1. **Stop only the dashboard server:** `STOP-DASHBOARD.cmd`, or stop the `python server.py` process listening on
   127.0.0.1:8765. Workers and the controller are not touched.
2. **Materialise the earlier release's code outside the working tree:**
   `git worktree add --detach <scratch dir> <earlier commit>`. This leaves the shared tree and index alone; never run
   `git checkout` on shared files.
3. **Start that server against the same store:**
   `python <scratch dir>/Database/Tools/dashboard/server.py --root Database/Tools/work/dashboard`.
4. **Reader older than 225465c2e:** it reads only `ff12-generation-1` and shows `ff12-generation-2` generations as
   UNSUPPORTED. That is by design: an older reader must refuse, not guess. So the oldest usable rollback target for
   the current store is 225465c2e.
5. **Rolling back My Progress alone:** run the builder from 605882fdc's parent (`build_views.py` without `v_progress`) and
   restart the server from a commit whose REQUIRED list lacks `progress`. The progress generations stay in the store
   and remain verifiable.
6. **Verify:** `/api/status` shows the expected generation, `problems: []`, and `reader_stale: false` for the code it
   was started from. Record the rollback here with the time and the pid.
