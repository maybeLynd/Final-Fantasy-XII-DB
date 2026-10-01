# The FF12 cloud program: what cloud sessions do for the database, and how (OPUS, 2026-10-01)

OPUS owns this program. Cloud sessions are Claude Code sessions in Anthropic's cloud, paid by the account's temporary
$250 cloud-session credit (expires 2026-11-05). How to start one, the billing rules and the launcher are in
`C:\Users\Kristian\Desktop\CLOUD_SESSIONS_GUIDE.md` on the workstation. This file says **what** cloud sessions are used
for, **what that should produce**, and **how their work stays out of every other identity's way**. The task log is in
[`CLOUD_AGENTS.md`](CLOUD_AGENTS.md); repo upkeep is in [`REPO_MANAGEMENT.md`](REPO_MANAGEMENT.md).

## What the program is for

The database is graded by `goal_gate.py`. As of 2026-10-01 these families are unmet:

| family | state | can a cloud session help? |
|---|---|---|
| questions | OPEN 5, PARTIAL 7 | **no**. They need live game work (ASTRA) |
| F (function dispositions) | about 3,600 frontier functions | **yes**: F-interior drafts (stream F) |
| DD (documented docs) | 20 pages | **partly**: owner-read worksheets for pages whose residue is prose (stream D) |
| acceptance | 0 of 30 clean terminal-audit passes | **yes**: text-only audit pre-runs find failures early (stream A) |

There are also two streams that do not move a family directly:
- consistency sweeps that feed corrections (stream C);
- the reconstruction-readiness map the RE repo will need (stream R).

**What a cloud session cannot do.** It sees only this private repo: the text snapshot plus `cloud-input/`. It has no
executable, extracted data, Ghidra, team board or live game. Everything it returns is a **draft or a pointer**. OPUS
verifies it on the workstation against the certified executable before any of it reaches the database, and it reaches
the database only through OPUS's publish queue. Cloud work is never evidence, never independent review, and never
merged into the snapshot.

## The streams

| id | stream | input | output (on the session's branch `cloud/<topic>`) | result for the database |
|---|---|---|---|---|
| F | F-interior drafts | `cloud-input/f-interior/<slug>.md`: OPUS's annotated disassembly of every F-frontier function a page cites only at its entry | `cloud-reports/f-interior/<slug>.json` in the row format of [the brief](cloud-briefs/f-interior.md) | after OPUS's mechanical check (`interior_ingest.py`), OPUS's re-read and SWE2-AUDIT-SPEC's method verdict, each row moves a function out of F |
| D | DD owner-read worksheets | a PARTIAL page and the register (`_index/OPEN-QUESTIONS.md`) | `cloud-reports/dd/<slug>.md`: every sentence that still reads as open, classified (stale with a pointer, a stated limit, or a proposed register row) | OPUS (or the page's owner) applies the accepted lines; the page can reach DOCUMENTED once its register rows close |
| A | audit pre-runs | the snapshot's text-only checkers (`Tools/analysis-kit/gfz-scripts/check_*.py` that need no executable) | `cloud-reports/audit/<date>.md`: which checkers ran, which failed, each failure with file and line | failures are fixed by the owning identity before the 30-pass acceptance run, so that run is not wasted |
| C | consistency sweeps | pages, the register and candidate records | `cloud-reports/sweeps/<date>-<topic>.md` | verified findings become corrections through the owner |
| R | reconstruction readiness | the pages of one system | `cloud-reports/re-readiness/<system>.md`: what the database documents for a re-implementation (inputs, outputs, state, order) and what is missing | gaps feed back into the database; accepted maps are copied into maybeLynd/Final-Fantasy-XII-RE `docs/readiness/` |

## No duplicated work (user, 2026-10-01)

A cloud session must never do work that OPUS, FABLE, ASTRA or a SWE2 (Devin) lane is doing or has claimed. Before
every launch, OPUS:
1. **Runs the scope guard** (`Tools/work/OPUS/cloud/scope_guard.py PAGE... --fns ...` on the workstation). It
   blocks a page when:
   - an open board task not owned by OPUS names it or one of its functions;
   - it has uncommitted edits by any lane;
   - it is an overlay carrier;
   - another identity committed to it in the last 24 hours.
   It warns on commits 24-72 hours old and on mentions in other identities' inboxes; OPUS reads every warning.
2. **Claims the scope on the team board** (`cloud_task.py open ...`). This creates task `OPUS-CLOUD-<stream>-<scope>-<MMDD>`,
   assigned to OPUS, holding each page as a `file:` resource, so the other identities see the work and the board
   refuses a conflicting claim. The task is finished (pages released) as soon as the report is ingested.
3. **Re-runs the guard at ingestion.** If a lane started on the page in between, the cloud draft yields: it is filed
   for that lane as a pointer, or dropped.
4. **Keeps cloud streams off other identities' assignments.**
   - Stream D covers only pages OPUS owns or that are unowned.
   - Streams A and C only report. A finding on another identity's page goes to that identity as a notice; OPUS does
     not fix it.
   - Stream R is planning text that no one else produces.

## Lifecycle of one cloud task

1. **Pack.** Stream F only: `f_pack.py` writes the input pack. Skip for the other streams.
2. **Guard and claim.** Run `scope_guard.py`, then `cloud_task.py open`.
3. **Sync and push.** `tools/sync_from_xiionline.py --apply`, commit, push, so the session clones current text.
4. **Launch.** Run the launcher with the stream's brief from [`cloud-briefs/`](cloud-briefs/). Log the session link in
   [`CLOUD_AGENTS.md`](CLOUD_AGENTS.md).
5. **Follow.** Read the transcript (`RemoteTrigger get_run_log`). It costs nothing and starts nothing.
6. **Collect.** `git fetch`; the report is on `cloud/<topic>`.
7. **Ingest.** For F: `interior_ingest.py check`, then OPUS re-reads every row, then `interior_ingest.py apply`
   (refused until the method verdict), then the publish queue. For the other streams: verify each finding and route it.
8. **Close.**
   - Merge the report file into `main` under `cloud-reports/`, as the archive.
   - Delete the branch.
   - Finish the board task (`cloud_task.py close`).
   - Update the log row.

## Pacing the credit

- **Measure the cost first.** The first wave (2026-10-01) is one session per stream. Afterwards OPUS asks the user
  for the credit bar and sizes the next waves.
- **Pace by verification.** Parallel sessions are fine, but launch no faster than OPUS can verify. An unverified pile
  is waste.
- **Front-load the work.** The credit expires on 2026-11-05.
- **Expect this from stream F.** Each page packed and drafted saves OPUS the drafting half of the interior-citation
  work. OPUS still reads every row, but reading a draft against its listing is roughly twice as fast as writing it.
  The F family has about 1,700 entry-only functions on DOCUMENTED pages.
