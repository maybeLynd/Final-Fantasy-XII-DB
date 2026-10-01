# Migration implementation map (M0), OPUS technical delivery

**Brief:** FF12-WORKFLOW-MIGRATION-20260928-01 (`COMPLETION-WORKFLOW.md`, adopted at 2af29d4c7).

**Parent task:** FRONTIER-REQ-OPUS-WORKFLOW-M0M1-DELIVERY (OPUS, ACTIVE).

**Baseline taken 2026-09-29 ~00:10Z:** board rev 38407 epoch 3, Git HEAD f62195be2.

This file maps each requirement to the code that exists, the gap, the owner of the exclusive paths, the board task, the
acceptance-matrix items and the independent verifier. **It is not a task tracker.** Status lives on the board. A row
changes here only when ownership or a path changes. Nothing here is an acceptance result: the matrix items stay NOT_RUN
until a non-author executes them.

## What exists (verified by reading the code, 2026-09-29)

| capability | code | state |
|---|---|---|
| progress report | `_index/progress/progress_report.py` (`generate` / `auto` / `check` / `status`; fingerprint before and after build; `snapshot.json` carries each output's sha256 and a `commit_id` stamped into every .md) | Works; `check` says STALE between regenerations. Known R3 defects: the doc fingerprint reads only the first 4000 bytes of each page; outputs are replaced file by file, not as one generation; `progress.config.json` says parser 3, the code says 4. |
| derived SQL view | `gfz-scripts/knowledge_db.py` (`provenance` table, `freshness_report`) | Staged build and re-fingerprint. Two copies: `Tools/work/knowledge/` is the default; `_index/knowledge.sqlite` is a tracked older copy that no script targets. |
| portable export | none | Uploads are made by hand, so a mixed-generation ZIP is possible and has been seen (rev 38074 against 38081 members). |
| dashboard | none | (Only radare2's bundled web UI exists.) |
| controller | `gfz-scripts/swe2_watchdog.py` | Devin lanes only; runs `progress_report.py auto` every 30 min or when `.dirty` is set. |
| Claude sessions | `goal_gate_hook.py` (Stop hook) and `goal_resume.py` (`claude -p --resume`) | Exist; A15 is not exercised. |
| top gate | `gfz-scripts/goal_gate.py` | Fails closed. Read 2026-09-29: provenance and transfers check return codes; questions requires counts plus "questions consistent" (the tool's last line, so a crash cannot leave it); any exception is UNMET. |
| gate runner | `gfz-scripts/run_gates.py` | Compares each gate's return code and output digest against `gate-baseline.tsv`, so a changed failure is reported. |
| board writes | `gfz-scripts/team.py` (mutex + lock + journal + epoch) | The direct-writer incident is repaired (FRONTIER-REQ-STRUCT-BOARD-WRITE-PATH-REPAIR DONE, a70307d37). ~~A13 still needs an independent run.~~ A13, expected revision only: ASTRA `521f189be` on source `bf000cdc9` - a fresh write commits, a stale one refuses with board and journal unchanged, and of two callers with the same token one commits and one refuses. Not a proof of simultaneous contention or fairness; fault prefix, removed lock, epoch, idempotence and the rest of A13 stay open. Ratified `verdict:ACCEPT`, scoped (full A13 NOT_ACCEPTED; the healthy-prefix and changed-checkpoint controls accepted), by SWE2-AUDIT-SPEC at `a95c664bf` (L338). Pending-state binding, ASTRA `afd0b8233` (`board-pending-state-binding/`): healthy prefix accepted and healed on one constructed prefix and one changed checkpoint field, ratified the same way (L339); its required consumer action (bind the intended pending full state before writing, or keep the unverified boundary) is done on the writer side at `57274cbd0` (FRONTIER; `test_team_rollback.py` PendingStateBinding) and stays with OPUS for migration integration. |
| evidence sealing | none | ORACLE's P0 task. |
| VBF taxonomy | `XIIOnlineNet/Additional resources/Tools/VBF Browser/` (Browser.exe is a .NET GUI; ff12-vbf.exe is a MinGW extractor) | **Settled 2026-09-29: the browser has no category table of its own.** Its code builds `VFolder` nodes with `GetChildFolders` from the archive's file-name table, so its taxonomy **is** the archive's folder tree. From the file table (`Tools/work/repos-2d/vbf_list.txt`, 89,414 entries = the extract's file count): 4 roots (`gamedata` 39,653, `ps2data` 39,578, `prefetchdata` 9,351, `jsondata` 832), 37 second-level nodes, 27,543 folders, depth up to 9, 58.9 GB, 48 extensions. The adapter must read the table from the archive itself and pin its identity; `vbf_list.txt` dates from 2026-09-02. |
| coverage | `program_coverage.py`, `check_coverage_dimensions.py`, `coverage_balance.py` (a hard-coded category table), `uc1_band.py` (the versioned population 34,269 + 795 = 35,064) | These give measured pieces, but no unique-interval whole-image view. |

## M1 - trustworthy foundation

| # | requirement | owner and exclusive paths | board task | matrix | independent verifier |
|---|---|---|---|---|---|
| 1a | Checked prerequisite results | OPUS: `gfz-scripts/prereq.py` (new, promoted from `sn1-layouts/sn1_prereq.py`), and OPUS's own composers. Composers in other lanes are routed to their owners, below. | this parent | A03 | ASTRA/SOL (FRONTIER-REQ-ASTRA-WORKFLOW-INDEPENDENT-VERIFY) |
| 1b | Immutable evidence receipts | OPUS: the generic mechanism `gfz-scripts/seal.py` (written 2026-09-29 while the P0 task sat unclaimed for three days; no experiment file touched). ORACLE: applies it to EXP-201 and its experiments. OPUS: applies it to its own controls (the S-13/S-15 case). | FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING (P0) | A04 | AUDIT-SEM (FRONTIER-REQ-AUDITSEM-REVIEW-EXP201-RECEIPT-SEALING; OPUS-REQ-AUDITSEM-REVIEW-SEAL) |
| 1c | Board writer | STRUCT (done) | FRONTIER-REQ-STRUCT-BOARD-WRITE-PATH-REPAIR | A13 | ASTRA/SOL runs A13 on isolated fixtures |
| 1d | Obligation accounting | DATA: `progress_report.py` R3 (page-only questions, empty vs invalid register, receipt-derived terminal). FABLE: package record and stage vocabulary. | FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10R3; FRONTIER-REQ-FABLE-WORKFLOW-PILOTS-SEMANTICS | A02 A10 A11 A12 | AUDIT-SPEC (FRONTIER-REQ-AUDITSPEC-EXECUTED-REVIEW-PROGRESS-CKPT10R3) |
| 1e | Coherent generation and export | OPUS: `gfz-scripts/generation.py` (new) - generation directory, manifest, guarded CURRENT pointer, verified export. DATA: adopts it in `progress_report.py` under R3. | FRONTIER-REQ-SWE2-DATA-EXPORT-COHERENT-GENERATION (DATA owns the integration; OPUS supplies the library) | A05 A06 A07 A08 A09 | ASTRA/SOL |

**1a - the composers found (a targeted search for swallowed prerequisite exits, 2026-09-29).**
- `candidates/s15-opus-replay-field-pass-stub-free/check.py` (OPUS): runs S-13's `check.py`, ignores its exit, and
  asserts `res["ok"]`. S-13 exits 0 exactly when `res["ok"]` is true, so the contract is equivalent to a checked exit.
  **No change;** editing an accepted driver for no behavioural difference would be churn. **Found on the way:** the
  run rewrites S-13's own `result.json` as a side effect. That is a mutable-output-over-a-cited-receipt case for 1b
  (routed to ORACLE's sealing task).
- `gfz-scripts/check_gap_debt.py`: runs `check_census_widths.py`, ignores its verdict, and uses `CENSUS`. That is a
  narrower data-only dependency, but it is implicit. It needs an explicit contract and a rejected case.
- `gfz-scripts/check_route_collisions_control.py`: runs `check_route_span_overlaps.py`, ignores its exit, and uses its
  functions. The same fix is needed.
- The `except SystemExit` sites around `R.decode` in five other tools are the decoder's own bad-extent signal, not
  prerequisite results. No change.

## M2 - completion loop (after M1 1a / 1e land)

- **Package records and stages:** FABLE.
- **Review-to-incorporation transitions and routing:** FRONTIER's controller.
- **Claude session adapter:** `goal_resume.py` / hook, owned by FRONTIER with OPUS integration.

Shadow-check first, then run one pilot (FABLE's). Matrix A14 A15 A16 A22.

## M3 - dashboard (after 1e, which it reads)

- **Data:** DATA, from generation outputs only. It never scans live on a refresh.
- **Integration and launch:** OPUS.
- **Meanings:** FABLE.
- **Deployment and loopback launch:** FRONTIER.
- **VBF taxonomy:** the archive's folder tree (above).

**Split CONFIRMED by SWE2-FRONTIER 2026-09-29** (`OPUS-REQ-FRONTIER-CONFIRM-M3-SPLIT`; paths stay
exclusive — DATA adapters emit view JSONs through `generation.py` only, OPUS's server never writes
`progress_report.py`, FRONTIER never touches view code):
- DATA writes the view adapters. They are generators that emit one JSON per view into a dashboard generation through
  `generation.py`: categories from the DB tree, the VBF tree from the archive table, coverage from the existing
  instruments, evidence and review health from the board and receipts, and the fleet from the watchdog state.
- OPUS writes the read-only loopback server and the pages that render those JSONs, under a new
  `Database/Tools/dashboard/`. It serves only the CURRENT generation and shows each view's source generation, time and
  stale reason.
- FRONTIER owns the launch, stop, shortcut and controller refresh.

Matrix A17 A18 A19.

## M4 / M5

- **Independent exercise:** ASTRA/SOL with the auditors (A01-A23).
- **Pilots:** FABLE (A21).
- **Release and rollback:** OPUS + FRONTIER (A23).

M5 is one accepted migration receipt. It is not this file.

## First bounded change (M0)

`gfz-scripts/prereq.py` (tagged and explicit data contracts) with `test_prereq.py`: T1-T9, D1-D5, and C1-C2 through
a composer run as a subprocess, FAILS 0. Two mutants of `prereq.py` each fail it: ignoring the exit code, and hiding
FAIL lines. The two shared composers are routed with the exact defect. See the commit that carries this file.

## Delivery links per matrix item (OPUS, updated 2026-09-29)

These are implementations and the requests that verify them. **Statuses are not kept here:** the board holds them, and
each item stays NOT_RUN until a non-author's receipt names the commit it ran at.

| item | implementation (commit) | verification request |
|---|---|---|
| A02 | package consistency flags in the overview (338b41712) | FABLE's pilots (FRONTIER-REQ-FABLE-WORKFLOW-PILOTS-SEMANTICS) |
| A03 | `prereq.py` (de83673fd; configured-FAIL repair 1f11830e9); SN-1 chain (0b26f50c4); composers (cd8bb2fab) | OPUS-REQ-ASTRA-VERIFY-A03-PREREQ (REJECT) → -R2 (ACCEPT, below); SN-1 executed ACCEPT (AUDIT-SEM) |
| A05-A09 | `generation.py` (3165f963e, volatile 9175ebf03, external a5e9a1a0d) | OPUS-REQ-ASTRA-VERIFY-A05-A09-GENERATION; reporter adoption OPUS-REQ-DATA-ADOPT-GENERATION-LIB |
| A04 | `seal.py` (this publication) | OPUS-REQ-AUDITSEM-REVIEW-SEAL; EXP-201 application: ORACLE |
| A14 / A16 | `transitions.py` (0d50ee5f3; admission repair f21fe8044); convention + controller hook (FRONTIER 89e78f275); synthetic pilot run by FRONTIER | OPUS-REQ-ASTRA-VERIFY-TRANSITIONS (REJECT, below) → -R2; the pilot's independence: OPUS-NOTICE-FRONTIER-A16-PILOT-SELF-REVIEW |
| A15 | `goal_resume.py` (existing) | OPUS-REQ-FRONTIER-CLAUDE-LANE-ADAPTER |
| A17 / A19 | dashboard server + views (7705335e2, 9175ebf03, f77c08954, 9f4571eb4, 7a5546fc6; served-content verification e8999f966; My Progress 622c0866d; activity, deltas, countdown 8ddc8c7e8; delta direction 763d466d6); controller builds (FRONTIER) | OPUS-REQ-ASTRA-VERIFY-DASHBOARD-SHELL; the cache repair -R2 (scoped ACCEPT, below); OPUS-REQ-ASTRA-VERIFY-AGENT-ACTIVITY-DELTAS-TIMER; OPUS-REQ-FRONTIER-DASHBOARD-DEPLOY |
| A18 | `.text` byte accounting (a5e9a1a0d) | none yet (to be filed with the M3 verification) |

### Independent receipts incorporated (OPUS, 2026-09-29, on ASTRA-RETURN-OPUS-R2-REPAIR-CONSUMPTION)

Each receipt covers only the scope it states. None of them awards an M-milestone, the migration, or L1+L2 completion.

- **A03, prerequisites: ACCEPT, scoped** (`OPUS-REQ-ASTRA-REVERIFY-A03-PREREQ-R2`, ASTRA `fe4bc030b`,
  `_experiments/evidence/migration-prerequisite-contract-r2/`). At exactly `1f11830e9`:
  - a configured FAIL is recognised and refuses composition;
  - the 16 generic controls are retained;
  - the corrected legacy supported-API pair works.

  Limit: the first legacy pair remains an invalid API call and is not semantic evidence.
- **A17 / A19, the dashboard cache repair: ACCEPT, scoped** (`OPUS-REQ-ASTRA-REVERIFY-DASH-INCIDENT-CACHE-R2`, ASTRA
  `dcc53dc22`, `_experiments/evidence/migration-dashboard-cache-r2/`). What held, on published `622c0866d`, whose cache
  code equals `e8999f966`:
  - the same 97-byte, same-mtime edit is refused on the next request;
  - the historical fallback, ordinary snapshot, no-invalid-data and code-stale controls work.

  Limits, kept verbatim in meaning:
  - The verification is **request-time**: a request begun after the 60 s bound does not report CURRENT (detected at
    60.75 s). It is **not** idle or background checking, and not an exact wall-clock deadline.
  - Only production HTTP responsiveness was observed. Loaded-module identity, the PID and the current deployment
    remain **unaccepted**.
  - Later dashboard commits (`8ddc8c7e8`, `763d466d6`) are not covered by this receipt.
- **A14 / A16, transitions: REJECT** (`OPUS-REQ-ASTRA-VERIFY-TRANSITIONS`, ASTRA `888afe2e4`). The defects were
  malformed-link admission and self-review incorporation. Both are repaired at `f21fe8044`, and re-review is
  `OPUS-REQ-ASTRA-VERIFY-TRANSITIONS-R2`.

  ASTRA's write campaign (race, idempotence, failed-writer prefix) is NOT_EXECUTED and stays open. The repaired code
  reports FRONTIER's two A16 pilot reviews as SELF-REVIEW, so A16 still needs a non-author pilot.

  **R2: ACCEPT, scoped to read-only admission** (ASTRA `117f85ab6`, `migration-transitions-r2/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L326) records `verdict:ACCEPT` for this review: ACCEPT scoped (`ACCEPT_SCOPED_ADMISSION`). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - The 12 exact `888afe2e4` inputs, plus a minimal self-REJECT, were run as 13 original CLI and plan cases: exit 0,
    no stderr, and the board bytes unchanged.
  - Malformed typed links are refused, and a self-review reads SELF-REVIEW for both verdicts.
  - Still NOT_EXECUTED: the write campaign under `--apply`, descendant cleanup, and the writer return code.
- **A09, generation certification: ACCEPT, scoped to the unknown-input-state repair** (`OPUS-REQ-ASTRA-VERIFY-GENERATION-CERT-R3`,
  ASTRA `70a134f63`, `migration-generation-cert-r3/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L329) records `verdict:ACCEPT` for this review: ACCEPT scoped (`ACCEPT_SCOPED_UNKNOWN_STATE_REPAIR`). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - On `b6e6de3f0`, over three byte-identical archives, library and CLI give: unknown state or removed snapshot
    UNVERIFIED (exit 1), valid VERIFIED (exit 0), duplicate UNVERIFIED (exit 1).
  - Not accepted: the normal builder, the deployed reader and M1 as a whole. A consistent whole-manifest rewrite still
    needs sidecar or origin evidence.
- **Dashboard shell, A17/A19 server scope: ACCEPT, scoped to selected-view admission** (`OPUS-REQ-ASTRA-VERIFY-DASHBOARD-SHELL`,
  ASTRA `c466fc472`, `dashboard-shell-reconciliation/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L334) records `verdict:ACCEPT` for this review: ACCEPT scoped (`ACCEPT_SCOPED_SELECTED_VIEW_HTTP`; the rendering and deployment gaps retained). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - Over real HTTP on `69bbf8c81`, one owned loopback server with four labelled generations gives:
    - a valid view: OK;
    - honestly hash-declared non-JSON: MALFORMED, data withheld;
    - a missing view: UNMEASURED, data withheld while other output is served;
    - a declared FAILED view: FAILED, retained.
  - The accepted source is `69bbf8c81`, not the request's historical `7705335e2`.
  - Still unaccepted:
    - page rendering and navigation;
    - the category taxonomy and adapter meanings;
    - the loaded module and PID in production;
    - the scheduler, restart and offline export;
    - A17, A19 and M3 as a whole.
  - ASTRA also found server.py's opening docstring stale: it said verification is cached once per CURRENT pointer.
    It is corrected to the per-request behaviour the code has had since `e8999f966`.
- **My Progress terminal admission: ACCEPT, scoped** (`OPUS-REQ-ASTRA-VERIFY-MY-PROGRESS-R3`, ASTRA `e66925f24`,
  `migration-my-progress-r3/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L330) records `verdict:ACCEPT` for this review: ACCEPT scoped (`ACCEPT_SCOPED_FIXED_TERMINAL_REQUIREMENT`). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - On `69bbf8c81`, a requirement of 0 fails T and is unmeasured and NOT READY, and a Ready-with-0 view is refused.
  - The complete-30 positives are retained.
  - The inputs are synthetic, not thirty real audits.
- **My Progress evidence fixtures: ACCEPT, scoped** (`ASTRA-REQ-SPEC-FIXTURE-PRODUCER-GUARD`, ASTRA `7393cec76`,
  `migration-fixture-placement/`), to `SCOPED_PRODUCER_GUARD_AND_READER_CORRECTION`.
  - The freezer `migration-my-progress-independent/freeze.py` now refuses a preparation tree holding
    `_index/OPEN-QUESTIONS.md` before copying. A clean inert source is accepted read-only, and a missing source is refused.
  - The ten fixture members sealed in `037557884` keep their bytes; nothing is relabelled or deleted.
  - The capture overall stays INVALID: its reader check expected the wrong API. Only that reader observation was
    re-run (`reader-02`). Active fixtures stay under private `work/`, and a future publication must capsule them as
    inert byte records.
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L328) records `verdict:ACCEPT` for this review. *(Added by SWE2-CONTRACT for OPUS.)*
- **Agent Activity writer attribution R2: ACCEPT, scoped** (`OPUS-REQ-ASTRA-VERIFY-ACTIVITY-ATTRIBUTION-R2`, ASTRA `8380c611c`,
  `activity-attribution-r2/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L335) records `verdict:ACCEPT` for this review: ACCEPT scoped (`ACCEPT_SCOPED_WRITER_ATTRIBUTION_REPAIR`; synthetic classification only). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - On `0bec2215d`, ASTRA's six original inputs pass through the actual compute and CLI:
    - a review FABLE queued for OPUS does not credit OPUS;
    - a real OPUS note is credited under the one-hour rule;
    - the busy and free controls are unchanged.
  - Still open: deltas, rendered UI, and loaded-module identity.
- **Transitions R3: ACCEPT, scoped** (`OPUS-REQ-ASTRA-VERIFY-TRANSITIONS-R3`, ASTRA `5eaabddf1`, `migration-transitions-r3/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L337) records `verdict:ACCEPT` for this review: ACCEPT scoped (exact fields and caller status R3; no real-writer parity). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - On `d27e9aff8`: exact 40-hex fields with no LF forwarding; the caller's status follows the required child status;
    the derived-id re-read exception holds; the original thirteen fixtures are preserved.
    - This repairs two scoped REJECTs of `f21fe8044`, both upheld at ratification (`a95c664bf`): ASTRA `f112e86b0` (`transition-line-boundary/`, L332: a 40-hex commit or a verdict ref plus one LF was admitted, the dollar anchor allowing a terminal newline) and ASTRA `821c25f8b` (`transition-writer-status/`, L333: a required child that exited 1 after printing `Saved revision` was reported `created`). *(Added by SWE2-CONTRACT for OPUS.)*
  - The `--apply` write campaign (race, idempotence, fault, cleanup) stays open.
- **Dashboard deltas, one prior basis R2: ACCEPT, scoped** (`ASTRA-RETURN-OPUS-DELTA-ONE-BASIS-R2-CONSUMPTION`, ASTRA
  `6bc6d481a`, `delta-one-basis-r2/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L340) records `verdict:ACCEPT` for this review: ACCEPT scoped to the exact `17d6cdc29` selectors, change expression and annotator. The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - On `17d6cdc29`, over copies of the original `9e84de620` histories:
    - a newest verified generation without a progress view gives no prior, no change, and `delta_basis` naming it;
    - an aligned 30 -> 40 gives +10 on the same basis;
    - an empty history gives none.
  - The actual build passes one prior to both consumers (checked statically).
  - Not credited:
    - `test_live.py` D6 and D7 were not executed by ASTRA;
    - the full measure set, the adapters, `_build`, the deployed browser and the counts;
    - the terminal audit.
  - The `9e84de620` counterexample stays immutable. DATA's day-boundary wording debt is a separate item.
- **Rendered navigation: bounded observations, scoped** (`ASTRA-RETURN-OPUS-RENDERED-NAVIGATION-CONSUMPTION`, ASTRA
  `60618c109`, `dashboard-rendered-navigation/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L341) records `verdict:ACCEPT` for this review: ACCEPT scoped (navigation observed; the two refused inputs preserved). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - In the host browser, the deployed page went Progress -> Overview (heading and source table) -> Activity (DOM, a
    screenshot, and a named ASTRA task).
  - The return to My Progress was refused twice, and that is preserved:
    - the first input used a stale accessibility id (12, against 356 in the newer tree);
    - the second targeted a STALE label that had become PARTIAL, so it matched nothing.
    - A return is therefore unobserved.
  - Also preserved:
    - the generations are ordered but not atomic (DOM 130427, screenshot 131122);
    - the screenshots are JPEG despite their suffix;
    - the first reducer failed, and the correction is additive.
  - The later served page matches the copied `7c14` source bytes. That is not proof of the loaded module or its PID.
  - Not awarded: totals, the taxonomy, real worker scheduling, all views, source links, the adapters, A17, M3, the
    migration and the database.
  - Targeting controls by their stable labels is proposed for future captures and was not executed.
  - SPEC reviews ASTRA's own evidence separately.
- **Rendered return to My Progress: one observation, scoped** (`ASTRA-RETURN-OPUS-DASHBOARD-RENDERED-RETURN`, ASTRA
  `d591eb30a`, `dashboard-rendered-return/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L348) records `verdict:ACCEPT` for this review: ACCEPT scoped (one return; STALE -> PARTIAL during setup; limits as stated). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - In the host browser, a stable role/name locator matched one visible control, with the mutable status text excluded.
    The click was followed by an immediate accessibility tree and a later DOM and JPEG of the My Progress destination.
  - The setup status changed STALE -> PARTIAL. That change is not proven at the exact dispatch: there are two inputs in
    all, and no event trace or registration timing.
  - `60618c109`'s two refused returns stay as they were and are not retroactively credited.
  - Source-page equality and HTTP generation identity do not establish the loaded server module, PID or browser build,
    or an atomic snapshot.
  - Still unproved: totals, the taxonomy, all views, full A17, M3, the migration and the database.
  - SPEC reviews ASTRA's own checker and gate.
- **Transition actual write and repeated dispatch: scoped** (`ASTRA-RETURN-OPUS-TRANSITION-ACTUAL-WRITE-CONSUMPTION`, ASTRA
  `c7f2f592f`, `transition-actual-write/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L343) records `verdict:ACCEPT` for this review: ACCEPT scoped (real transition/writer integration; no A14/A16 award). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - The setup is synthetic: an immutable empty seed `521f` plus six original apply operations, on a native fixture board.
  - On the original caller at `d27e9aff8` with the path-keyed writer, `--apply` over labelled synthetic DONE reviews
    gives:
    - two derived requests, INCORP (DATA) and REPAIR (OPUS);
    - board revision 6 -> 8, genesis/intent commits 7 and 8;
    - a valid original boardcheck.
  - Running the identical parent again gives DONE-ALREADY with the board and journal byte-unchanged.
  - Not substituted: no child substitution, no mutex replacement, no replay of the old seven operations.
  - The FABLE review in the fixture is fictional, not a real acceptance.
  - The child's return 0 / Saved is inferred from the original caller's created status; the child's raw stdout was not
    captured separately.
  - Unproved:
    - the real controller and native host;
    - the package cycle, races and fairness;
    - cancellation, quota and budget timeout;
    - recovery, and full A14/A16.
  - FRONTIER takes the controller implications from this entry. The capture is not duplicated.
  - ASTRA co-authored its own gate (the receipt controls, and the premature 24-member freeze retained as failed), so
    that gate needs SPEC review. OPUS does not award it.
- **`.text` overlap: REJECT, repaired** (`ASTRA-REQ-OPUS-TEXT-OVERLAP-UNIQUE-REPAIR`, ASTRA `0d9d9330c`,
  `text-overlap-boundary/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L342) records `verdict:ACCEPT` for this review: the REJECT is upheld (scoped to the unique-overlap measure at the exact original source). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - The defect: `bytes-overlap` summed the seen flags, so it counted additional covers, not unique bytes.
    - `0032E040..0032E041` lies in three listed extents and counted twice: 1,759 reported against 1,758 unique.
    - The class-sum check cannot see it, because the classes tile correctly either way.
  - Repaired at `cdbf25a5d`:
    - `build_views.population_cover` counts unique bytes at cover depth two or more, and reports the additional covers
      beside them in the measure's limits.
    - The executable view's definition is `v2`, so no delta is taken across the change.
  - Controls:
    - `test_build_views` B8: disjoint 0, double 8, triple 12, and ASTRA's real extents 33 unique / 34 covers, each
      equal to an independent sweep. The pre-repair formula over-counts both triples and gives 1,759 on the real
      population, against 1,758.
    - B9: a `v1` prior gives `N/A - definition changed` with both sides shown.
  - The 1,759 is an instrument artifact. A falling overlap here is not new database understanding.
  - The UC-1 extents, dispositions and native semantics are unchanged, and no index regression is claimed.
  - Re-review is `OPUS-REQ-ASTRA-VERIFY-OVERLAP-AND-HELPER-BINDING`.
  - **Re-review: ACCEPT, scoped** (ASTRA `1548d3896`, `overlap-helper-repair-review/`; consumed by
    `ASTRA-RETURN-OPUS-OVERLAP-HELPER-REVIEW-CONSUMPTION`).
    - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L347) records `verdict:ACCEPT` for this review: ACCEPT scoped (the overlap/helper repair; bound and missing-begin refuse). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
    - Through the actual `population_cover` and `text_intervals`/`v_executable` on the real image: the four fixtures,
      triple 8 unique / 12 extra, and the three retained real extents 33 unique / 34 extra.
    - An actual `_build`/Store with only the executable adapter commits `v2`. A labelled `v1` prior (12) then `v2` (8)
      gives `N/A - definition changed` with both sides; an unchanged `v2` gives 0 pp.
    - The full 35,064-body census (1,758) was not repeated.
    - ASTRA's first preflight was invalid: it compared raw helper bytes, CRLF on disk against LF in Git. It is retained,
      and the correction compares Python-level content only.
    - Not certified:
      - the full build, the deployed module and all views;
      - a source edited before import, third-party binding, and historical helper identity;
      - A05, A23, M3, the migration, and L1/L2.
    - The earlier counterexamples stay immutable.
    - ASTRA owns its checker and gate, and SPEC reviews them separately.
- **UC-1 helper binding: REJECT, repaired** (`ASTRA-REQ-OPUS-UC1-HELPER-BINDING-REPAIR`, ASTRA `c7bd09b49`,
  `uc1-dependency-binding/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L344) records `verdict:ACCEPT` for this review: ACCEPT scoped (`SCOPED_DEPENDENCY_BINDING_GAP`: the gap is the honest result). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - The defect: at `17d6cdc29`, `declare_inputs` bound 25 inputs, including the builder, but not `uc1_band.py`, which
    `text_intervals` imports and calls (load, apply, describe).
  - Repaired at `cdbf25a5d`: `uc1_band.py` is a declared input, bound at the path of the module actually imported.
  - Control, B10: the manifest names it with that file's sha256, and the helper edited mid-build refuses the commit,
    naming `uc1_band.py`.
  - Older generations stay immutable. Their manifests prove the builder's identity only; the helper's identity then is
    unrecorded, and the current `746b6fab` is not assumed for them.
  - Still not bound:
    - third-party imports (`pefile`);
    - a file edited after it was imported but before the build begins (as for `build_views.py`).
  - Not claimed: full generation certification, and A05/A23 adoption by DATA or FRONTIER.
  - Re-review is the same request as the overlap repair.
- **Dashboard deltas, prior basis: REJECT, scoped** (ASTRA `9e84de620`, `ASTRA-REQ-OPUS-DELTA-BASELINE-SELECTION`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L336) records `verdict:ACCEPT` for this review: the REJECT is upheld (`REJECT_SAME_PRIOR_AT_VERIFIED_MISSING_VIEW_BOUNDARY`). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - The defect: My Progress's change block fell back to an older generation than the one `delta_basis` named.
  - Repaired at `17d6cdc29` with one basis (`test_live.py` D6, D7). Re-verification is
    `OPUS-REQ-ASTRA-VERIFY-DELTA-ONE-BASIS`.
- **Agent Activity: REJECT, scoped to writer attribution** (`OPUS-REQ-ASTRA-VERIFY-AGENT-ACTIVITY-DELTAS-TIMER`, ASTRA
  `00fd54fda`, `migration-activity-deltas-independent/`).
  - *Ratified 2026-09-30:* SWE2-AUDIT-SPEC's ratification at `a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929/`](../candidates/auditspec-ratify-legacy-verdicts-0929/README.md), source L327) records `verdict:ACCEPT` for this review: the REJECT is upheld (`REJECT_ACTIVITY_WRITER_ATTRIBUTION`). The scope above is unchanged. *(Added by SWE2-CONTRACT for OPUS.)*
  - The defect: a task's timestamp credited the lane it named, not the lane that wrote it.
  - Repaired at `0bec2215d`: writes come from the board history's issuer (`test_live.py` A8, A9). The server was
    restarted alone as pid 63884.
  - Re-review is `OPUS-REQ-ASTRA-VERIFY-ACTIVITY-ATTRIBUTION-R2`.
  - Deltas, the rendered UI and loaded-module identity were outside that package, and stay open.

### M4 exhibit: a real rejection drove repair and re-review without a relayed message (OPUS, 2026-09-29)

1. ASTRA finished `OPUS-REQ-ASTRA-VERIFY-TRANSITIONS` with `verdict:REJECT` (`888afe2e4`).
2. FRONTIER's controller, running `transitions.py`, filed `AUTO-REPAIR-OPUS-REQ-ASTRA-VERIFY-TRANSITIONS` to OPUS by
   itself (07:09Z). Nobody passed a message.
3. OPUS repaired at `f21fe8044` and filed `OPUS-REQ-ASTRA-VERIFY-TRANSITIONS-R2`, whose `reviews` field names the repair.

This is the M4 sentence "a real reviewer rejection must drive repair and re-review", executed on the production board.
It is an exhibit for the independent M4 review, not an acceptance. ~~The re-review has not returned~~ The re-review
returned a scoped **ACCEPT** (`117f85ab6`), which closes the loop once. The incorporation half (a non-author owner) is
still unexercised: FRONTIER's two pilots are self-reviews.

4. The loop ran a second time on a different producer. ASTRA rejected the Agent Activity writer attribution (`00fd54fda`).
   The controller filed `AUTO-REPAIR-OPUS-REQ-ASTRA-VERIFY-AGENT-ACTIVITY-DELTAS-TIMER`. OPUS repaired at `0bec2215d`
   and filed `-ACTIVITY-ATTRIBUTION-R2`, whose `reviews.repairs` names the repair task.
