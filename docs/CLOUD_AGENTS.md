# Cloud agents for the FF12 database: how we use them, and what to expect (OPUS, 2026-10-01)

Read this before starting or briefing a cloud agent for FF12. It records how cloud sessions are used here, so a future
session can carry on without relearning it.

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

<!-- LAUNCH-METHOD: filled in once confirmed -->
See "Launch method" below. If it is unknown, the user can start one at https://claude.ai/code on this repo with the
brief above.

## Task log

| date | branch | task | status | applied locally |
|---|---|---|---|---|
