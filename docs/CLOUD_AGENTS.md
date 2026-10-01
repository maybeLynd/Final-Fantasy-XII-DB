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
