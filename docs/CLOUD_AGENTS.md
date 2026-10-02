# Cloud agents for the FF12 database: how we use them, and what to expect (OPUS, 2026-10-01)

Read this before starting or briefing a cloud agent for FF12. It records how cloud sessions are used here, so a future
session can carry on without relearning it.

**Since 2026-10-01 the work itself is organised as a program.** See [`CLOUD_PROGRAM.md`](CLOUD_PROGRAM.md) for the
streams, the results they should produce, the no-duplication protocol and the task lifecycle. The per-stream briefs
are in [`cloud-briefs/`](cloud-briefs/), and repo upkeep is in [`REPO_MANAGEMENT.md`](REPO_MANAGEMENT.md). This file
keeps the background and the **task log** at the end.

## The credit is temporary

- The account has **$250 of Claude Code cloud-session credit, expiring 2026-11-05** (1:59 AM CST).
- **While it lasts, use it to the best of its capability**, with as many bounded tasks as are useful running in
  parallel.
- **Once it is used up or expired, stop.** Cloud agents are then no longer used or relied on. No milestone, workflow,
  gate or plan may depend on them, and nothing in the database's process may require one.
- The user authorized autonomous use on 2026-10-01: OPUS chooses the tasks and briefs and runs the agents without
  asking each time.

## What a cloud agent can and cannot see

| it sees | it does not see |
|---|---|
| this repo: the text-only snapshot of `XIIOnline/Database` (`FFXII TZA/`, `Tools/analysis-kit`, `Tools/dashboard`, docs) | the shipping exe, the extracted archive (`D:/FFXII_TZA_extract`), `Tools/work/` |
| everything committed on `main` at the snapshot commit | the live team board (`TEAM.json`), the queue, local dashboards, Ghidra, Devin, ASTRA |
| | uncommitted work in `XIIOnline` |

So **most checkers cannot run in the cloud**, because they read the exe or the extracted data. Give cloud agents
self-contained work only:
- **Consistency sweeps:** pages against the register (`_index/OPEN-QUESTIONS.md`), stale "open" or "pending" wording,
  status lines that contradict their rows, broken links, struck-but-still-cited claims.
- **Cross-reading:** one system's pages against another's (producer and consumer both documented the same way?),
  candidate records against the pages that cite them.
- **Tooling:** pure-Python tools and tests that need no game data (parsers for the TSV/JSON records, report
  generators).
- **Drafting:** prose clean-up, summaries and indexes. These are proposals only; the canonical edit is made locally.

## The output contract

1. **Report-only by default.** The agent writes `cloud-reports/<YYYY-MM-DD>-<topic>.md` on its own branch
   `cloud/<topic>` and opens a PR. It does not edit the database snapshot itself. The snapshot is regenerated from
   `XIIOnline`, so edits made here would be overwritten.
2. **Every finding names file and line**, quotes the text, says what it contradicts, and proposes replacement wording.
3. **OPUS verifies each finding locally** against the real database (and the exe where needed). It applies accepted
   ones in `XIIOnline/Database` through the normal publish queue, with OPUS attribution and, for corrections, a
   consumer-check. Then it closes the PR with a note listing what was applied and what was rejected and why.
4. A cloud report is **never evidence on its own**. It is a pointer for a local verification. A cloud agent's
   agreement with OPUS is not independent review.

## Brief template

```
Repository: maybeLynd/Final-Fantasy-XII-DB (text-only snapshot; do not edit FFXII TZA/ or Tools/).
Read docs/CLOUD_AGENTS.md and FFXII TZA/_index/EVIDENCE-POLICY.md first.
Task: <one bounded sweep or tool>, scope <folders/files>.
Output: cloud-reports/<date>-<topic>.md on branch cloud/<topic>, then open a PR to main.
For each finding: file:line, quoted text, what it contradicts (with file:line), proposed wording.
Do not guess about the game. If a claim needs the executable or game data, list it under "needs local check".
Stop when the scope is covered; summarise counts at the top of the report.
```

## How a session starts one

**Corrected 2026-10-01 (OPUS).** The first method written here (RemoteTrigger routines) was **wrong**. Routines
bill the plan's weekly usage limit, not the cloud-session credit: the credit stayed at $250 while the routine runs hit
"You've hit your weekly limit". **Do not create or run routines** (RemoteTrigger `create`/`run`, `/schedule`,
`/v1/code/triggers`).

The credit pays for ordinary cloud sessions. An agent starts one with `claude --cloud "<task>"`. That command needs an
interactive terminal, so run it through the launcher on this PC, which provides a pseudo-console:

```
C:\Users\Kristian\Tools\cloud-launch\.venv\Scripts\python.exe C:\Users\Kristian\Tools\cloud-launch\cloud_launch.py ^
    --cwd C:\Users\Kristian\source\repos\Final-Fantasy-XII-DB --task-file brief.txt --wait 120 --log launch.log
```

It prints `SESSION https://claude.ai/code/session_...`. The full method, its limits and how to check the credit are in
**`C:\Users\Kristian\Desktop\CLOUD_SESSIONS_GUIDE.md`** (an identical copy sits next to the launcher in
`C:\Users\Kristian\Tools\cloud-launch\`); read it first. Billing confirmed 2026-10-01: after the probe session the
user's Cloud session credits bar read $249 of $250 left.

1. **Refresh the snapshot** (`tools/sync_from_xiionline.py --apply`), commit and push, so the session clones current
   text.
2. **Launch** with the brief template above; `--cwd` is this checkout.
3. **Follow**: `RemoteTrigger get_run_log` with the `session_...` id reads the transcript and starts nothing.
4. **Collect**: fetch the `cloud/<topic>` branch locally, verify every finding against `XIIOnline/Database`, apply the
   accepted ones through the publish queue, and record them in the task log below.

The `Agent` tool's `isolation: "remote"` silently falls back to a local worktree in this session. It uses no cloud
credit, so do not use it for cloud work.

Before a session launches anything, check that the credit still has a balance (ask the user, who sees Settings ->
Usage) and that today is before 2026-11-05. If either fails, stop using cloud agents.

## Task log

| date | branch | task | status | applied locally |
|---|---|---|---|---|
| 2026-10-01 | cloud/register-consistency | register vs page consistency sweep (ROUTINE: billed plan usage, not the credit; session cse_01U8msvcyJcZBFDBTcM3ZfLL) | done: PR #1, 84 findings | section (d) and the GR-17 status verified and queued (OPUS-PUB-GR16-PROPAGATE-1001); overlay carriers routed to SWE2-FRONTIER |
| 2026-10-01 | cloud/register-vs-records | register cells vs their cited records (ROUTINE: billed plan usage; session cse_01FzYbtkHfwTDWZWmdih3zsL) | stopped by the weekly limit at 08:19 UTC, no output | - |
| 2026-10-01 | - | credit-billing probe via `claude --cloud` (cloud_launch.py; session_01GBKBghCBkGvvHjNQghLtXj, claude-opus-5-5) | method verified; credit confirmed by the user ($249 of $250 left afterwards) | - |
| 2026-10-01 | cloud/f-interior-battle-runtime-mode-ladder | wave 1, stream F: F-interior drafts for battle-runtime-mode-ladder + audio-bank-and-controller-family (46 functions); board OPUS-CLOUD-F-INTERIOR-W1-1001; https://claude.ai/code/session_01MsKSmz4qgiM3h8TPNKv3gp | done: 45 rows + 1 skip, 0 rejected by interior_ingest check; archived in cloud-reports/f-interior/ | OPUS re-read all 45 rows against the listings (1 correction: 00420E70's r8b argument); records opus-*-cloudint-1001 staged; apply waits for SWE2-AUDIT-SPEC's interior-method verdict, so the board task stays open |
| 2026-10-01 | cloud/audit-prerun-1001 | wave 1, stream A: text-only audit pre-run; board OPUS-CLOUD-AUDIT-PRERUN-1001; https://claude.ai/code/session_0193YNrU1oBcBFBoWgpYKQNr | done: 159 checkers (CLEAN 26, FINDINGS 62, NEEDS-EXE 39, NEEDS-PACKAGE 25, CRASH 7); archived in cloud-reports/audit/ | OPUS re-ran 26 defect-class checkers locally: the findings reproduce as the known backlog, except check_links (214 in the snapshot, 2 locally: snapshot-only link targets) and check_rules_index (11 vs 0). Two defects in OPUS's own checkers fixed (OPUS-PUB-CHECKERS-AUDIT-PRERUN-1001: check_interior_offsets wrote into the tree; check_index_figures' control tested the corpus); 21 stale interior-offset leads routed to SWE2-STRUCT |
| 2026-10-01 | cloud/re-readiness-15-input | wave 1, stream R: readiness maps for 15-Input and 18-Audio; board OPUS-CLOUD-RE-READINESS-INPUT-AUDIO-1001; https://claude.ai/code/session_014xapq8GYgyFvvwy2xRFAwk | done: 15-Input MOSTLY, 18-Audio NOT YET; archived in cloud-reports/re-readiness/ | verified (8 citations line-exact; 5 contradictions checked against the image, all real) and copied to the RE repo docs/readiness/ (3b5fe44); the 9 + 36 page contradictions are OPUS DD work (OPUS-DD-UNCLAIMED-15-99-0930) |
| 2026-10-02 | cloud/re-readiness-05-spawn | wave 2, stream R: readiness map for 05-Spawn-Encounter-Lifecycle (snapshot 4da4b9d0); board OPUS-CLOUD-R-READINESS-05-1002; https://claude.ai/code/session_01NcTcvS8gdiEyacPvQXf8eR | done: NOT YET (ledger and keep entry MOSTLY; placement and retirement NOT YET), 18 value-changing contradictions page-text only; archived in cloud-reports/re-readiness/ | verified: all 18 value items decided at the image (several dated corrections overturned: A6, A9, A11, A12, A14, A17), control spawn_check.py; OPUS share applied in XIIOnline 186b1d04f, FABLE 24 / FRONTIER 18 / EC7 7 requested; map + verdicts in the RE repo docs/readiness/05-spawn.md (72e6abc) |
| 2026-10-02 | cloud/re-readiness-06-movement | wave 2, stream R: readiness map for 06-Movement-And-Navigation (snapshot 4da4b9d0); board OPUS-CLOUD-R-READINESS-06-1002; https://claude.ai/code/session_01MKBAiNUqEAFXnUNyPRoqu9 | done: NOT YET (7 of 11 parts MOSTLY; gaps G-01/03/05/06), 43 value-changing contradictions page-text only; archived in cloud-reports/re-readiness/ | verified: all 43 value items decided at the image (several dated corrections overturned), control movement_check.py; OPUS share applied in XIIOnline c8a281ba1, EC7 64 / FABLE 20 / DATA 2 requested; map + verdicts in the RE repo docs/readiness/06-movement.md (564f563) |
| 2026-10-02 | cloud/re-readiness-07-action | wave 2, stream R: readiness map for 07-Combat-Action (snapshot 4da4b9d0); board OPUS-CLOUD-R-READINESS-07-1002; https://claude.ai/code/session_018kFSP47XCyorcYBsfyonGU | done: NOT YET (core MOSTLY), 17 value-changing contradictions page-text only; archived in cloud-reports/re-readiness/ | verified: 17 value + 9 count items decided at the image (pages' dated corrections held on almost all), control action_check.py; OPUS share applied in XIIOnline 3e0fc5be9, FABLE 68 / EC7 3 / CONTRACT 1 / FRONTIER 4 requested; map + verdicts in the RE repo docs/readiness/07-action.md |
| 2026-10-02 | cloud/re-readiness-09-ai | wave 2, stream R: readiness map for 09-Combat-AI-And-Gambits (snapshot 4da4b9d0); board OPUS-CLOUD-R-READINESS-09-1002; https://claude.ai/code/session_01FNGRVb6xYymAE7HhAttG93 | done: NOT YET (walk READY bar one callee; enmity and config MOSTLY), 12 value-changing contradictions page-text only; archived in cloud-reports/re-readiness/ | verified: 11 of 12 value items decided at the image (C-V11 both right; C-V1/2/3/8/12 against the report's lean), control ai_check.py; OPUS share applied in XIIOnline 871706705, FABLE's 30 edits requested; map + verdicts in the RE repo docs/readiness/09-ai.md (03b3315) |
| 2026-10-02 | cloud/re-readiness-03-world | wave 3, stream R: readiness map for 03-World-Area-Field (snapshot df2c9f47); board OPUS-CLOUD-R-READINESS-03-1002; https://claude.ai/code/session_015MguvEESqUEwUm6JUUqGBu | done: NOT YET, 74 contradictions (28 value-changing, page-text only); archived in cloud-reports/re-readiness/ | verified: all 28 value items decided at the image, control world_check.py; OPUS share applied in XIIOnline 185789b98, EC7 52 / FABLE 19 / FRONTIER 10 / DATA 2 requested; map + verdicts in the RE repo docs/readiness/03-world.md (e1a0655) |
| 2026-10-02 | cloud/re-readiness-04-actor | wave 3, stream R: readiness map for 04-Actor-Entity (snapshot df2c9f47); board OPUS-CLOUD-R-READINESS-04-1002; https://claude.ai/code/session_01CyCFGXs9kPwVXaq5BmAkb1 | done: NOT YET (names READY bar one address; BattleUnit pool, field pass, manager slot, kind byte, StatusView MOSTLY); value items page-text only; archived in cloud-reports/re-readiness/ | verified: all 52 value items decided at the image (50 refute a side), control actor_check.py; OPUS share applied in XIIOnline 3159f78f1 (field map held for SPEC's audit), FRONTIER 33 / EC7 23 / FABLE 11 / STRUCT 2 requested; map + verdicts in the RE repo docs/readiness/04-actor.md |
| 2026-10-02 | cloud/re-readiness-11-party | wave 3, stream R: readiness map for 11-Party (snapshot df2c9f47); board OPUS-CLOUD-R-READINESS-11-1002; https://claude.ai/code/session_01FJpNGAfhZw9eGS9RVWrAn5 | done: NOT YET (roster, focus, slot maps, block, SetSaveData MOSTLY), 54 contradictions (27 value-changing, page-text only); archived in cloud-reports/re-readiness/ | verified: all 27 value items decided at the image (C-V17, C-V19 against the report's lean), control party_check.py; OPUS share applied in XIIOnline d814d081d (roster page held for SPEC's audit), FABLE 20 / EC7 13 / FRONTIER 2 / DATA 5 requested; map + verdicts in the RE repo docs/readiness/11-party.md (95b14d4) |
| 2026-10-02 | cloud/re-readiness-14-story | wave 3, stream R: readiness map for 14-Story-Event-Quest-Hunt (snapshot df2c9f47); board OPUS-CLOUD-R-READINESS-14-1002; https://claude.ai/code/session_01A9VNiknt2kLKbpS5joq1do | done: MOSTLY (flag-bank core READY statically; treasure NOT YET), 40 contradictions (18 value-changing, page-text only); archived in cloud-reports/re-readiness/ | verified: 13 of 18 value items decided at the image (5 ledger/corpus counts undecidable), control story_check.py; OPUS's 4 edits applied in XIIOnline 6599f2a4c, FABLE's flag-bank pages got the verdicts as a request; map + verdicts in the RE repo docs/readiness/14-story.md (8ed5fd9) |
| 2026-10-02 | cloud/re-readiness-01-scriptvm | wave 4, stream R: readiness map for 01-Script-VM-Native-Bridge (snapshot 86b70c69); board OPUS-CLOUD-R-READINESS-01-1002; https://claude.ai/code/session_01EHPGLJXLf4LQ9idMivvB2A | done: NOT YET (lifecycle, value stack, variables, request scheduling MOSTLY), 60 value-changing items page-text only; archived in cloud-reports/re-readiness/ | verified: 60 value items decided at the image (6 undecidable), control scriptvm_check.py; OPUS share applied in XIIOnline 1f193fec9 (binding page held), FRONTIER 24 / FABLE 15 / EC7 9 / DATA 7 / CONTRACT 6 requested; map + verdicts in the RE repo docs/readiness/01-scriptvm.md (d0cdf78) |
| 2026-10-02 | cloud/re-readiness-16-ui | wave 4, stream R: readiness map for 16-UI (snapshot 86b70c69); board OPUS-CLOUD-R-READINESS-16-1002; https://claude.ai/code/session_016dMPD3qWpTj3TJxBrhZe2s | done: NOT YET, 112 value-changing items page-text only; archived in cloud-reports/re-readiness/ | verified: 74 of 112 value items decided against a side at the image (17 left for longer reads), control ui_check.py; OPUS share applied in XIIOnline b70c3da07, EC7 44 / FABLE 15 / FRONTIER 9 / DATA 2 requested; map + verdicts in the RE repo docs/readiness/16-ui.md |
| 2026-10-02 | cloud/re-readiness-22-phyre | wave 4, stream R: readiness map for 22-Middleware-PhyreEngine (snapshot 86b70c69); board OPUS-CLOUD-R-READINESS-22-1002; https://claude.ai/code/session_01NqcVVFsta7oaQ6z4swFnL2 | done: NOT YET (application slots, module registry, header, reflection MOSTLY), 101 value-changing items page-text only; archived in cloud-reports/re-readiness/ | verified: 101 value items decided at the image (2 undecidable), control phyre_check.py; OPUS share applied in XIIOnline 0adae56fa, EC7 70 / FABLE 18 / DATA 5 / FRONTIER 1 / CONTRACT 1 requested; map + verdicts in the RE repo docs/readiness/22-phyre.md (8e4ae26) |
| 2026-10-02 | cloud/re-readiness-25-ebp | wave 4, stream R: readiness map for 25-EBP-Script-Container (snapshot 86b70c69); board OPUS-CLOUD-R-READINESS-25-1002; https://claude.ai/code/session_01KboLsRxwSDCcdGdhuXddFR | done: NOT YET (container and dispatch MOSTLY; sections 12, 17 READY), 16 value-changing items page-text only; archived in cloud-reports/re-readiness/ | verified: value and count items decided at the image and the shipped .ebp data, control ebp_check.py; OPUS share applied in XIIOnline 8ccd3aad3, EC7 1 / DATA 1 (+ census regeneration) requested; map + verdicts in the RE repo docs/readiness/25-ebp.md (eb7770d) |
| 2026-10-02 | cloud/re-readiness-00-engine | wave 5, stream R: readiness map for 00-Engine-Core-Runtime (snapshot 34861cfd); board OPUS-CLOUD-R-READINESS-00-1002; https://claude.ai/code/session_01CZqFVU5oUoW88c6NELytjK | done: NOT YET (boot, tick, gate, stop registry, mode ladder core MOSTLY), 269 value-changing items page-text only; archived in cloud-reports/re-readiness/ | local verification at the bytes pending (OPUS); re-run scope_guard before applying |
| 2026-10-02 | cloud/re-readiness-17-render | wave 5, stream R: readiness map for 17-Presentation-Rendering (snapshot 34861cfd); board OPUS-CLOUD-R-READINESS-17-1002; https://claude.ai/code/session_01Bf11Bg4ubT2fxuBZvpWtqD | done: NOT YET, 193 value-changing items page-text only; archived in cloud-reports/re-readiness/ | local verification at the bytes pending (OPUS); re-run scope_guard before applying |
| 2026-10-02 | cloud/re-readiness-20-platform | wave 5, stream R: readiness map for 20-Platform-Online-Achievements (snapshot 34861cfd); board OPUS-CLOUD-R-READINESS-20-1002; https://claude.ai/code/session_012aVGLuf29A9aQWEkT3c5Vr | done: MOSTLY (counter update/store READY statically), 15 value-changing items page-text only; archived in cloud-reports/re-readiness/ | verified: 14 of 15 value items decided at the image, control platform_check.py; OPUS share applied in XIIOnline 16e03537d, FABLE 3 / CONTRACT 4 / DATA 2 requested; map + verdicts in the RE repo docs/readiness/20-platform.md |
| 2026-10-02 | cloud/re-readiness-24-crt | wave 5, stream R: readiness map for 24-Compiler-And-CRT-Runtime (snapshot 34861cfd); board OPUS-CLOUD-R-READINESS-24-1002; https://claude.ai/code/session_0137yPRG7XTM3wFKHbcLxYsK | done: NOT YET (start-up, lazy statics, teardown, containers MOSTLY), 104 value-changing items page-text only; archived in cloud-reports/re-readiness/ | local verification at the bytes pending (OPUS); re-run scope_guard before applying |
| 2026-10-02 | cloud/re-readiness-02-resource | wave 6, stream R: readiness map for 02-Resource-And-Asset-Pipeline (snapshot f26c5667); board OPUS-CLOUD-R-READINESS-02-1002; https://claude.ai/code/session_01B4SaFqE6PKekGoBmNC5uAR | done: NOT YET, 123 value-changing items page-text only; archived in cloud-reports/re-readiness/ | local verification at the bytes pending (OPUS); re-run scope_guard before applying |
| 2026-10-02 | cloud/re-readiness-23-thirdparty | wave 6, stream R: readiness map for 23-Third-Party-Libraries (snapshot f26c5667); board OPUS-CLOUD-R-READINESS-23-1002; https://claude.ai/code/session_01LJvAciEcWWmN4q69YNqjNu | done: NOT YET (zlib, JsonBox, Dear ImGui READY), 35 value-changing items page-text only; archived in cloud-reports/re-readiness/ | local verification at the bytes pending (OPUS); re-run scope_guard before applying |
| 2026-10-02 | cloud/re-readiness-26-pkfl | wave 6, stream R: readiness map for 26-PKFL-Package-Container (snapshot f26c5667); board OPUS-CLOUD-R-READINESS-26-1002; https://claude.ai/code/session_01Jj4UjYygkaGeAfKG9UBegc | done: MOSTLY, 15 value-changing items page-text only; archived in cloud-reports/re-readiness/ | local verification at the bytes pending (OPUS); re-run scope_guard before applying |
| 2026-10-02 | cloud/re-readiness-99-residual | wave 6, stream R: readiness map for 99-Unresolved-Residual (snapshot f26c5667); board OPUS-CLOUD-R-READINESS-99-1002; https://claude.ai/code/session_016siHJQNhxaAAsMTubX3jKu | done: NOT YET, 67 value-changing items page-text only; archived in cloud-reports/re-readiness/ | local verification at the bytes pending (OPUS); re-run scope_guard before applying |
| 2026-10-02 | cloud/f-interior-w2-1 | wave F2, stream F: F-interior drafts for 14 OPUS-led pages (56 entry-only functions; packs 32499a12); board OPUS-CLOUD-F-INTERIOR-W21-1002 (pages held); https://claude.ai/code/session_01XRXP3rS6fx4VxurArNZ8tP | done: drafts archived in cloud-reports/f-interior/ | OPUS ingest (interior_ingest.py check, OPUS re-read, apply) pending |
| 2026-10-02 | cloud/f-interior-w2-2 | wave F2, stream F: F-interior drafts for 14 OPUS-led pages (56 entry-only functions; packs 32499a12); board OPUS-CLOUD-F-INTERIOR-W22-1002 (pages held); https://claude.ai/code/session_01AgDnGDrHFC5Nb2A49asyw5 | done: drafts archived in cloud-reports/f-interior/ | OPUS ingest (interior_ingest.py check, OPUS re-read, apply) pending |
| 2026-10-02 | cloud/f-interior-w2-3 | wave F2, stream F: F-interior drafts for 13 OPUS-led pages (55 entry-only functions; packs 32499a12); board OPUS-CLOUD-F-INTERIOR-W23-1002 (pages held); https://claude.ai/code/session_01TC3EwFqtoYbhukMEoJ3ZVA | done: drafts archived in cloud-reports/f-interior/ | OPUS ingest (interior_ingest.py check, OPUS re-read, apply) pending |
| 2026-10-02 | cloud/f-interior-w2-4 | wave F2, stream F: F-interior drafts for 14 OPUS-led pages (55 entry-only functions; packs 32499a12); board OPUS-CLOUD-F-INTERIOR-W24-1002 (pages held); https://claude.ai/code/session_01EsnYZKbu767dCnSLHP8iar | done: drafts archived in cloud-reports/f-interior/ | OPUS ingest (interior_ingest.py check, OPUS re-read, apply) pending |
