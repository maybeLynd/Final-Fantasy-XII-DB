# The team's operating protocol

> ## Adopted completion workflow — FF12-WORKFLOW-MIGRATION-20260928-01 (SWE2-FRONTIER, 2026-09-28)
>
> The user-approved operating brief is `_index/workflow/COMPLETION-WORKFLOW.md`
> (`Database/FFXII TZA/_index/workflow/`), with `ACCEPTANCE-MATRIX.md`,
> `WORKER-ASSIGNMENTS.md`, `ALL-TOP-LEVEL-GOALS.md` and `worker_prompts/` beside
> it. It governs execution roles (OPUS technical delivery, SOL/ASTRA independent
> engineering verification, FABLE mechanism/semantic ownership, FRONTIER
> operations/deployment), the migration milestones M0–M5, capacity-aware
> scheduling and the read-only dashboard/export contract. It does **not** lower
> the L1+L2 requirements, independent review, safety or the terminal protocol
> below; report a real policy conflict through the board rather than silently
> overriding it.

> ## TEAM ROLLBACK RECOVERED — new durability rules (SWE2-FRONTIER, 2026-09-26 02:30Z)
>
> The 2026-09-25 ~21:53Z rollback (an ~11-hour-stale in-memory board dumped over ~1,050
> live ops by a hand `checkpoints` edit) is **resolved**: the recovered board is installed
> at `recovery_epoch` 1, revision 31132 — the uploaded rev-30730 witness plus all 193
> validated tail ops plus all 209 receipted post-reset fork ops. Reconciliation,
> adjudication of every unresolved op, and the evidence package live in
> `Database/Tools/work/_incident-team-rollback-20260926/` (start at `RECONCILIATION.md`).
> Both branches and the preimage are retained; independent review is routed to
> `SWE2-AUDIT-SEM` (`FRONTIER-REQ-AUDITSEM-REVIEW-TEAM-RECOVERY-20260926`).
>
> **HOLD IS LIFTED.** New rules, now enforced mechanically:
>
> - **`team.py` is the only board write path.** It now journals every write (intent +
>   commit with content hashes) to `work/_team-journal/` and checks the on-disk board
>   against the journaled high-water under the lock. A stale/rolled-back/divergent or
>   wrong-epoch file raises `BoardIncident` — the op fails closed and nothing is written.
> - **A `BoardIncident` stops the fleet**: the watchdog reports `board-incident` (never
>   an empty frontier) and `publish_paths.sh` refuses to stage `TEAM.json`.
> - **Board-level notes** (`checkpoints` array — the field whose hand-edit caused this
>   incident) now have a sanctioned action: `{"action": "note", "note": "..."}` via
>   `team.py apply`. Hand-editing `TEAM.json` is what broke; never do it.
> - Writers holding pre-recovery copies: your next write fails closed — re-read the
>   board, rebase, re-apply. Your work is not lost: every op you receipted was merged.
>
> **Operative headers are generated, not hand-maintained (2026-09-26):** each lane inbox
> now carries a `<!-- TEAM-CURRENT:begin ... -->` block generated from live board state —
> board revision, `recovery_epoch`, and a `queue_sha` fingerprint of the agent's
> selection-relevant state (active + blocked tasks, addressed READY, unassigned pool,
> held resources). At session start/resume and before selecting work, run
> `team.py current --check --file <your inbox>`: `CURRENT`/`MOVED` is usable (`MOVED` =
> board advanced but your queue is unchanged); `STALE-QUEUE`/`STALE-LABELLED` means the
> block is **non-authoritative — do not select work from it**; refresh with
> `team.py current --agent <YOU> --write --file <your inbox>` and re-read. Never
> hand-maintain completion counts or a NEXT section; never replay a block's task list
> after a stale verdict — completed work re-checks against the board, not the header.
> `publish_paths.sh` refreshes the block on any published inbox automatically.
>
> **Session exhaustion is a pause, not a verdict (2026-09-27):** a lane that is out of
> context after checkpointing *pauses* — `goal_gate_hook.py` allows the stop once an
> already-triggered continuation (`stop_hook_active`) produced no new tool work, or
> after two consecutive unchanged-signature blocks on hosts without the flag. The
> pause, the gate verdict and the block count are recorded in
> `work/goal-gate/hook-state.json`; `DB_GOAL=NOT_MET` is unaffected. A paused lane's
> successor resumes from its inbox resume block + the board — exactly one live owner,
> claims unchanged. Before pausing, a lane must checkpoint: resume block current,
> board claims released or recorded, dirty work committed or disclosed. Never mark a
> solvable obligation BLOCKED or waive it to exit; the pause exists precisely so no
> one has to.



> **The identities are eleven, fixed, as of 2026-09-13** — `FABLE`, `OPUS`, `ASTRA` and the eight
> `SWE2-*` lanes. The roster and what the migration did and did not touch are in
> [**the eleven-identity section**](#the-team-is-eleven-fixed-production-identities--2026-09-13-opus-records-once);
> review tiers and auditors are in [`REVIEW-POLICY.md`](REVIEW-POLICY.md). The paragraph below is
> the 2026-09-10 protocol this file was founded on: **its "exactly three research identities" is
> superseded**, everything else in it stands.

Effective 2026-09-10. ~~Exactly three research identities~~; no standing coordinator or helper slots.
This protocol supersedes old coordination assignments, **not** the mission, evidence standard,
correction history, templates, mutation fences or charter quality gates. Old inboxes remain evidence.
The [historical board](ASSIGNMENTS.md) grants no live claims. Do not infer identity from peer discovery:
start with one explicitly assigned ID and retain it across session restarts.

## Phase and specialties

[TEAM.json](TEAM.json) is the canonical operational board. **All eleven currently prioritize
`DATABASE`.** The three research identities below are the original specialties, unchanged; the eight
`SWE2-*` production and audit lanes are tabulated in the eleven-identity section.

| ID | Primary specialty |
|---|---|
| FABLE | Deep semantic/static/system research: functions, scripts/resources, state machines, architecture |
| OPUS | Types, fields, signatures/ABI, ownership/lifetime, relationships, contracts, readiness closure — and **canonical adjudication**, not first-line review |
| ASTRA | Autonomous original-game runtime evidence, experiments, tooling/process improvements, skeptical review |

These are soft boundaries. Cross them for requested support, a clearly faster unblock, an unavailable
owner, or independent risk review; check and claim the actual scope first. Never self-award an
independent audit. **No production identities beyond the fixed eleven unless the user explicitly
changes the roster** — the old three-agent protocol's *"no additional autonomous researchers"* was a
restatement of *"exactly three"* and is superseded with it. Deterministic tools/tests are unrestricted.

Bounded reconstruction/differential probes may test database sufficiency and must end with evidence
or an explicit database gap. The full L1/L2 endpoint and separate-instruction requirement below
supersede the former readiness-gate transition language. The current phase remains `DATABASE`.

### Staffing — ASTRA restored to three specialties, 2026-09-12

**ASTRA has usage again and resumes all three of its specialties**: autonomous original-game runtime
evidence, experiments and tooling/process improvement, and skeptical review. Recorded once here by
OPUS so peers read it rather than re-deriving it; no further acknowledgement ticket is wanted.

What this does and does not change:

- **Nothing is taken back automatically.** ASTRA's own `ASTRA-FACING-REAPPLY-COMPARISON` and its
  three BLOCKED rows stay ASTRA's; the offline original-code and differential work OPUS carried
  during the absence stays with OPUS until it is handed over **at a safe checkpoint**, with the
  receipts, never abandoned mid-campaign. Reconcile tasks, dirty files, live processes and temporary
  transfers **before** any ownership changes, through `team.py` transactions only.
- **The queued requests targeted at ASTRA are live work again** — `OPUS-REQ-ASTRA-TRIAGED-QUEUE`
  (which names three items needing no running game at all), `OPUS-REQ-ASTRA-CONTRACT-OBSERVATIONS`,
  `FABLE-REQ-ASTRA-HANDLERS`, `FABLE-REQ-ASTRA-EXPKEYS` and the rest of the `to ASTRA` rows.
- **The live-game pause is NOT lifted by usage returning.** Driving, attaching to, instrumenting or
  closing the original-game process needs the user's explicit permission, asked once and then
  honoured; offline captures, isolated original-code execution and static work continue meanwhile.
  `@runtime` is still reserved only for the bounded experiment itself.
  **Historical staffing condition: the explicit authorization below now supersedes that pause.**

### Staffing — ASTRA usage window, unavailable to about 2026-09-19

**ASTRA is about to exhaust its usage and is expected back in roughly six days** (user, 2026-09-13).
Recorded once here by OPUS so peers read it rather than re-deriving it; no acknowledgement ticket is
wanted.

**This is availability, not authorization.** The live-control scope granted in the section below does
**not** lapse because the agent holding it is out of usage, and the *scope lives here, runnability
lives in `ASTRA.md`* rule is unchanged. Nothing about the grant is edited by this note.

**ASTRA being away is not a global blocker, and no one idles waiting for it.** When a package reaches
a question that genuinely needs live-original-runtime evidence:

1. **Preserve the question precisely** — do not soften it into one the static evidence can answer.
2. **Record, in the request:** target/function/state; evidence already known; the competing
   interpretations; the **exact discriminating observation**; why static/original-code evidence is
   insufficient; the affected downstream claims; and any useful save/area/setup information.
3. **Route it into the existing ASTRA/runtime queue.**
4. **Mark only the affected claim or package boundary BLOCKED** — never the whole package.
5. **Continue immediately** with the highest-value non-conflicting work that does not need ASTRA.

**Exhaust the cheaper evidence first**, in this order, before routing anything: existing evidence →
static analysis → call/data relationships → scripts and resources → isolated original-code execution.
A question that any of those can settle does not belong in a six-day queue.

**Do not weaken or guess a runtime-dependent conclusion to avoid waiting.** Leave the exact claim open
and move to another package. A conclusion reached by lowering the bar is worse than an open question,
and this database's whole value is that the difference is visible.

**Absorption while ASTRA is out** — `SWE2-ORACLE` takes bounded original-code experiments that do not
need the running game; `SWE2-DATA` takes authored-data and resource questions; `FABLE` continues
architecture and family work; `OPUS` continues EC-7, types, contracts, canonical integration and
adjudication; the other SWE2 lanes continue their normal bounded queues.

**Triage your own rows now, so ASTRA returns to a prepared, prioritized batch rather than six days of
accumulated waiting.** OPUS has done this for its eight `to ASTRA` rows and the result is worth
reading before you assume yours are live-only:

| OPUS row | needs a running game? |
|---|---|
| `OPUS-REQ-ASTRA-AUDIO-GATE-LIVE` | **yes** — one attach answers three queued observations, one of them a negative |
| `OPUS-REQ-ASTRA-CML1-COLUMN-STABILITY` | **yes** — the column has to survive an actual load |
| `OPUS-REQ-ASTRA-MGRMARK-RELOAD` | **yes** — two reads of `022C6D20[0..4]` across a real area change |
| `OPUS-REQ-ASTRA-EXP-METHOD-LAPSE` | **no** — every one of `EXP-075`..`081` states its own method in its own body, with Unicorn versions or PIDs; recoverable from published evidence, taken off the queue |
| `OPUS-REQ-ASTRA-EXP-STATUS-VOCABULARY` | **no** — a schema question about the `status:` field, decidable without the game |
| `OPUS-NOTICE-GUARD`, `OPUS-NOTICE-SWEEP`, `OPUS-NOTICE-GATEAXIS-CONCEDE` | **not questions** — notices ASTRA reads on return; they block nothing |

**Five of eight did not need ASTRA's runtime at all.** That ratio is the reason for the triage
instruction rather than a courtesy: a queue that mixes live-only questions with documentation and
schema work hides how much live time is actually owed, and it is the live-time estimate that decides
what ASTRA does first when it comes back.

### Test authorization and evidence-method selection — 2026-09-12

**The user explicitly lifts the previous live-game automation pause for FF12 database research.**
Ordinary runs within this scope need no repeated approval. This also supersedes the temporary
saved-capture-only continuation recorded in ASTRA's handoff. Identity, the full L1/L2 completion
rule, evidence standards and separate-instruction requirement for reconstruction remain unchanged.

Under a bounded `@runtime` reservation, ASTRA may control the designated FF12 test instance:
launch/close/restart, focus/input/navigation, load backed-up test saves, establish state, inspect
memory, capture screenshots/telemetry, attach/detach validated instruments, and collect breakpoint,
watchpoint and entry/return evidence. Scoped test hooks/DLLs, reversible writes and native calls are
authorized when justified by ABI, thread and state preconditions, with verified cleanup. Label
interventions explicitly; an injected call does not prove ordinary gameplay reaches that call.

Protect original saves, reference binaries, unrelated processes and peer work. Use disposable
copies/backups and prevent experimental progress from overwriting or syncing over real saves.
Keep runs bounded and stoppable; verify detach, restored state and responsiveness, and safely
restart a contaminated test instance. **A new stop request, emergency-stop input or user takeover
halts automation. Do not override it or automatically restart afterward.** This authorization does
not bypass tool or OS security. Ask only for genuinely unavailable access, new destructive scope
or an unavoidable manual action.

Before expensive setup, briefly record in the existing task: claim/hypotheses, existing evidence,
distinguishing observation, method and limits, controls, and escalation/stop condition. Choose the
cheapest **sufficient** method, not an automatic preference or a required three-stage sequence:

- **A — offline analysis:** original disassembly, captures, scripts/resources, checks and replay,
  when these settle the claim. Agreement of a reconstruction with its own fixture is insufficient.
- **B — isolated original-code execution:** verified shipping instructions in controlled memory/ABI,
  for bounded calculations, layouts, branches, writes, callback boundaries and composition. Disclose
  stubs, injected state and entry boundaries; omitted initialization/scheduling/effects stay open.
- **C — live FF12:** actual initialization, binding, ownership/reuse, scheduling, caller/command flow,
  presentation and cross-system consequences when A/B do not establish them. Verify state and trigger.

Use a small feasibility/control probe before a large capture or harness. If controls fail or cannot
discriminate, revise the method instead of repeating it or broadening the conclusion. Preserve exact
binary/tool identity and raw evidence; negative results require detection controls. Compare effects
and order, not only returns. For live combat consequences, establish **target -> command -> action**
before damage/death. No live-test ratios. Propagate results under ownership, run impacted checks and
mutations, commit validated checkpoints and continue. Recording permission or completing one test
does not complete the database.

**Re-confirmed 2026-09-13 under external review, and nothing about it reopened.** The section above
is the current authorization and needs no revision.

> **Scope lives here; runnability lives in [`ASTRA.md`](ASTRA.md).** The authorization above defines
> *what* ASTRA may do and does not expire. Whether live control is **presently runnable** is read
> from **ASTRA's latest permission checkpoint in `ASTRA.md`** — the newest one, by date and file
> order — and from nowhere else. A stop request, emergency-stop input or user takeover halts
> automation until the user renews it, and both the halt and the renewal are recorded there, not
> here. **Any status line in this file is a snapshot of the moment it was written**, so do not read
> one as current permission and do not treat a halt recorded in `ASTRA.md` as narrowing the scope
> above. Scope survives a stop; runnability does not.

#### Renewed by the user 2026-09-13, and why both sets of lines in `ASTRA.md` are correct

The user **explicitly renewed** ASTRA's live-game automation permission in a fresh turn on
2026-09-13; ASTRA recorded it in its own file under *"User renewed live authorization - 2026-09-13"*.
That is a second authorization act, not a re-reading of the 2026-09-12 one, and this record carries
the date so the two files do not disagree.

**Read `ASTRA.md` as three states in sequence, not as a contradiction:**

1. **2026-09-12** - the pause is lifted (the section above).
2. **Between the two dates** - a user takeover halted automation, and ASTRA's checkpoints from that
   span say *"no automatic live restart after cleanup-only resumption"*. **Those lines are correct
   and remain correct for their span:** the authorization above ends with *"a new stop request,
   emergency-stop input or user takeover halts automation; do not override it or automatically
   restart afterward"*, so a halt recorded there is the rule working, not a stale claim.
3. **2026-09-13** - the user renews it, which is what lifts that halt. Only the user can; ASTRA
   correctly did not restart on its own.

**The residual named here on 2026-09-13 is closed.** The three pre-lift checkpoint lines this
paragraph used to flag - *"the live-game pause remains in force"*, *"once-asked live permission
remains unanswered"*, *"the live-game pause remains unchanged"* - **now each carry a
`Historical checkpoint: superseded by ...` marker in `ASTRA.md` itself** (verified at that file's
three checkpoint lines). The stale-reading-first shape is gone; ASTRA fixed it in the file that owns
it, which is the right repair and the same one applied to `fields.tsv` `+0x698`.

**ASTRA owns that file and OPUS is not editing it.** The authoritative statement is here. Anyone
reading `ASTRA.md`'s early checkpoints should treat every pre-2026-09-12 pause line as historical,
and every between-dates halt line as **true of its span and lifted by the 2026-09-13 renewal**.

### EC-7 lanes, parallel family dispositioning, and a stale assumption retired — 2026-09-13 (OPUS records once)

**The live-game authorization above is in force and has been since 2026-09-12.** Recording this
again because **OPUS carried the retired assumption anyway**: my 2026-09-13 checkpoint listed *"the
live-game authorisation question is unanswered"* as an open blocker after this section had already
superseded the pause. Nothing was corrupted — every package that session was static and labelled
static — but **an operating record only works if it is read**, and a blocker asserted from a stale
summary is a blocker invented. Retired here in the file that owns it.

Three consequences, so nobody re-derives them:

1. **Static cases need no ASTRA approval.** Method selection above is a *cheapest sufficient*
   rule. A claim that A or B settles is settled; routing it to ASTRA for a live confirmation is
   not thoroughness, it is cost.
2. **Live evidence is not mandatory by ratio.** The section above already says *"No live-test
   ratios."* A document is not weaker for being static when static is sufficient, and a live run
   does not upgrade a claim the run did not test.
3. **ASTRA has explicit authorization for bounded live FF12 testing** when method selection says C
   is necessary — under a bounded `@runtime` reservation, with the protections and stop conditions
   stated above.

#### EC-7 ownership and the parallel family lanes

**FABLE is authorized to consume large semantic-family EC-7 lanes in parallel.** To let that run
without collisions, the mechanism and the declarations are deliberately different files:

| surface | owner | what changes there |
|---|---|---|
| `gfz-scripts/check_dispositions.py` | **OPUS** | the A/B/C/D schema, the checker, the refusal rules, the denominator |
| `progress.py`'s disposition line | **OPUS** | the metric input |
| `function_families:` frontmatter on a page | **the page's owner** | declarations |
| the members TSV beside a page | **the page's owner** | the enumerated population |

**A family is dispositioned by editing a page and adding a TSV. It never requires touching the
checker.** That is the whole point of the split: FABLE can run many lanes at once, and OPUS's
mechanism stays a single-writer file.

**OPUS remains the canonical EC-7 owner** and holds four duties that are not FABLE's to take:
maintaining the schema and checker; **protecting denominator consistency** (the population is the
34,270 non-funclet bodies `progress.py` counts, and any change to it is a change to both
dimensions at once); **rejecting unsupported dispositions**; and resolving structural, ABI and type
ambiguity a family declaration runs into. **The checker already refuses a function that two
families claim, and one that is both declared and measured as A**, so a function cannot silently
disappear or hold conflicting dispositions — that guarantee is mechanical, not a convention, and it
is the reason the lanes can run in parallel at all.

**The EC-7 mechanism is not to be expanded for elegance.** It is established; defects get fixed,
features do not get added. Using it to disposition the long tail is the work.

### The endpoint is L1 + L2 completion, not the readiness gate — 2026-09-12

**Recorded once, in the operating protocol rather than as a parallel policy.** The programme's
endpoint has been **replaced**: it is no longer the assembled readiness gate and its request for
approval. `RECONSTRUCTION-READINESS-GATE.md` remains a valid instrument — it measures five L2
requirements and separates local from architectural residue — but **assembling it, reporting it, or
having it approved does not end the work.**

**DONE is:** the database meets the existing requirements of [`COMPLETION-PLAN.md`](../COMPLETION-PLAN.md),
[`GOAL-REVISION-2026-09-08.md`](../GOAL-REVISION-2026-09-08.md) and
[`FINAL-AUDIT-PROTOCOL.md`](../FINAL-AUDIT-PROTOCOL.md) for **L1 and L2**, including the reviews those
documents require. L3 parity is later. Bounded reconstruction probes may test database sufficiency;
a **primary reconstruction phase needs a separate user instruction**.

**And what is explicitly not completion:** a report, a pilot count, a green validator, an empty
board, or an approval request. Required unknowns and contradictions stay **open until resolved** —
evidence-backed family and library dispositions remain valid, but no exclusion is invented, no
architectural gap is waived and no question is erased to reach zero. Missing live evidence blocks
**the affected claims, not the database**.

## Start and choose the next package

Use the existing shared checkout at `C:\Users\Kristian\source\repos\XIIOnline`.
It has one Git worktree, substantial ignored evidence/tool installs, and established absolute-path
consumers. Adding separate worktrees now would create incomplete/stale tool inputs. Claims protect
file ownership; publication is serialized below. A future move needs demonstrated benefit.

Run from that root in PowerShell, substituting the assigned identity:

```powershell
$py = '.\Collaboration\Tools\analysis\venv\Scripts\python.exe'
$team = '.\Database\Tools\analysis-kit\gfz-scripts\team.py'
git status --short
git log -8 --oneline
& $py $team validate
& $py $team show --agent FABLE
```

Read [README](README.md), [mission](../../../GFZ-MISSION-PROMPT.md),
[evidence standard](../EVIDENCE-STANDARD.md), [completion plan](../COMPLETION-PLAN.md),
[program state](../PROGRAM-STATE.md) (including its latest appended checkpoint),
[tool manifest](../../../Tools/README.md), and relevant recent commits. ASTRA also reads
[runtime methodology](../RUNTIME-RESEARCH.md) and the latest experiment records.

Use [OPEN-QUESTIONS](../OPEN-QUESTIONS.md), [READINESS-RANK](../READINESS-RANK.tsv), existing
frontier/readiness/coverage tools and inbox backlog to select work. The board is a small working set
of packages and requests, **not a second knowledge backlog**. Re-check the cited question against
current documents, TSVs, evidence and history before claiming; old register questions may be answered.
When the board runs out, derive and add a bounded package from those sources without user prompting.

Priority: **P0** foundational/blocking correctness; **P1** high downstream leverage or modding/
reconstruction importance; **P2** normal database completion; **P3** low-connectivity long tail.
Respect the mission's breadth rules. Use dependencies, not a scoring service.

## Atomic claims and checkpoints

Run `team.py apply --agent ID --file operation.json`; place operation files in ignored
`Database/Tools/work/ID/`. Never hand-edit live TEAM.json. Exclusion is the named kernel mutex
`Local\XIIOnlineTEAMBoardLock` — the OS releases it if a holder dies mid-write; `TEAM.lock` is still
created and honoured inside the mutex so a peer running an older team.py stays excluded, and serves
as the diagnostic record of who holds the lock. A collision fails
closed: read the board and retry. No claim is effective until the command succeeds.
Board updates are short transactions; the lock is **not** held during research.

To queue a package, provide this operation (resource keys are lowercase, ranges decimal and half-open):

```json
{"action":"add","task":{"id":"TYPE-ACTOR-017","kind":"research","priority":"P1",
 "target":"ActorStorageRecord movement field cluster","scope":"+0x2C0..+0x320",
 "completion":"Writer/consumer evidence and type entries, or an explicit bounded blocker",
 "dependencies":[],"resources":[{"key":"type:actorstoragerecord","start":704,"end":800},
 {"key":"file:database/ffxii tza/_types/fields.tsv"}]}}
```

Claim, checkpoint, finish, block, resume or release with these operation shapes:

```json
{"action":"claim","task":"TYPE-ACTOR-017","note":"Checked current claims and existing coverage"}
```
```json
{"action":"checkpoint","task":"TYPE-ACTOR-017","note":"Read writers A/B; evidence in work/OPUS/...; consumer C next"}
```
```json
{"action":"finish","task":"TYPE-ACTOR-017","note":"Bounded package complete","result_refs":["commit:<actual hash>","<document or handoff path>"]}
```
```json
{"action":"block","task":"TYPE-ACTOR-017","note":"Need runtime distinction H1/H2; request RT-ACTOR-017",
 "resume_when":"RT-ACTOR-017 returns controlled evidence"}
```

`resume` moves an owner's BLOCKED package to READY for a fresh collision/dependency check;
`release` moves an ACTIVE package to READY. Both require a `note`. Blocking releases resources;
bank partial work in a commit or owner inbox first and select other useful work immediately.
Never silently delete a claim or take it over because its timestamp is old. A stopped owner resumes
under the **same identity** after checking process/session state and dirty files, records recovery,
and releases/reclaims explicitly. Never delete a TEAM.lock by hand: since the file is still honoured
under the mutex for backward compatibility, removing one that belongs to a live writer admits a
second holder — exactly how the revision-35478/35479 same-revision double-commits of 2026-09-27
happened (manual reaps racing a rotating lock file). A genuinely wedged holder is resolved by
proving the recorded PID stopped, then re-running `team.py`, which reaps dead records itself. The
board itself must only ever be written through `team.py`'s journaled transaction; never hand-edit
TEAM.json or write it from a stale copy.

Each substantive package names the semantic target **and every file to be edited**. Reuse existing
target keys (resolve aliases against the type/knowledge store); the tool cannot infer that two
different descriptions mean the same work. Whole-target and parent-directory claims conflict with
their ranges/children. Disjoint offsets can run concurrently, but two edits to the same TSV require
serialization or staging rows in separate inboxes. Trivial reads need no claim.
No broad "Actors"/"Combat" claims: name the field cluster, verb family or contract blocker and a
completion condition. For an exceptional swarm, first record high leverage, distinct methods and
expected time saving in the requesting package; split method/scope and output files explicitly.

## Requests, runtime queue and contradictions

A request is a task with `kind: request` or `runtime`; runtime tasks target ASTRA by default.
In addition to the package fields above, require `requester`, `assigned_to`, `question`,
`known_evidence`, `missing_information`, `why_it_matters`, and `what_is_blocked`.
Name the exact missing observation and the downstream decision; "please investigate" is insufficient.
The recipient sees it in `show --agent ID`, claims a separate bounded observation scope, and returns
`result_refs` to durable evidence, controls, limitations, failed methods and a commit/handoff.
The requester integrates it under its own claim. Dependency task IDs can gate claims; external
blockers belong in the checkpoint/resume condition. No dependence on cross-account messaging.

For contrary evidence, add `kind: contradiction` with those same fields plus `original_claim`,
`counter_evidence`, and `affected_documents`. This preserves both positions immediately, including
while the affected document is owned by someone else. The recipient pauses conclusions relying on
the disputed claim, records REOPENED in the affected documents and propagates reopening per the
evidence standard under file claims. Use the existing permanent correction sections, AUDIT-LOG and
[contradiction ledger](../CONTRADICTION-LEDGER.md); TEAM.json routes work, not scientific truth.
An unresolved ticket is not a resolved contradiction. Finishing one requires result references to
the inspected evidence, correction/resolution and propagated affected records. Never latest-writer-wins.

The five views are: ACTIVE tasks; READY tasks with satisfied dependencies and no collision;
targeted requests; runtime-kind requests; unresolved contradiction-kind requests. Historical DONE
records and operation history are retained. Keep new scientific questions in OPEN-QUESTIONS.

### Review transitions — the `reviews` convention (adopted by SWE2-FRONTIER, 2026-09-29, M2/A16)

A review request SHOULD carry a `reviews` field on the task:
`{"author": <lane>, "commit": <sha>, "record": <repo path>,
  "incorporation_owner": <lane, optional>, "package_item": "<PKG-...:ID, optional>"}`.
The reviewer finishing it SHOULD include a `result_refs` entry `verdict:ACCEPT` or
`verdict:REJECT` alongside its receipt refs. `gfz-scripts/transitions.py` then performs the
next step deterministically on the controller timer — `REJECT` files exactly one
`AUTO-REPAIR-<review id>` to the author; `ACCEPT` files `AUTO-INCORP-<review id>` to the
named incorporation owner. No verdict is read out of prose; no relayed message is needed.
Review tasks filed without the field simply don't transition automatically.

**The verification evidence behind these rules** (recorded 2026-09-30 by SWE2-CONTRACT for OPUS, `OPUS-INCORP-RATIFIED-0930`).
Each review was ratified `verdict:ACCEPT` by SWE2-AUDIT-SPEC at `a95c664bf`
(`_index/candidates/auditspec-ratify-legacy-verdicts-0929/`, source line given). Every scope is the package's own:
- Admission R2 (ASTRA `117f85ab6`, `migration-transitions-r2/`): ACCEPT, scoped to read-only admission (L326).
- Line boundary (ASTRA `f112e86b0`, `transition-line-boundary/`): REJECT at the exact-field admission scope, upheld
  (L332). `f21fe8044` admitted a 40-hex commit or a verdict ref followed by one LF. Repaired at `d27e9aff8`
  (`fullmatch`).
- Writer status (ASTRA `821c25f8b`, `transition-writer-status/`): scoped REJECT, upheld (L333). `f21fe8044` reported
  `created` and exit 0 when the required child exited 1 after printing `Saved revision`. Repaired at `d27e9aff8`
  (`writer_status`: success needs exit 0 and a whole `Saved revision N` line).
- R3 on `d27e9aff8` (ASTRA `5eaabddf1`, `migration-transitions-r3/`): ACCEPT, scoped to exact fields and caller
  status, with no real-writer parity (L337). The `--apply` write campaign stays open.
- Actual write and repeated dispatch (ASTRA `c7f2f592f`, `transition-actual-write/`): ACCEPT, scoped (L343). Labelled
  synthetic reviews on a fixture board give two derived requests and a valid boardcheck, and a re-run changes nothing.
  No simultaneous contention, fairness or real review cycle is shown, and there is no A14/A16 award.
- Board writes, expected revision (ASTRA `521f189be`, `board-stale-revision-writer/`): ACCEPT, scoped (L338). A stale
  writer refuses with board and journal unchanged, and of two callers with one token, one commits. Full A13 is
  NOT_ACCEPTED.
- Board writes, pending state (ASTRA `afd0b8233`, `board-pending-state-binding/`): ACCEPT, scoped (L339). A healthy
  prefix is accepted and healed, on one constructed prefix and one changed checkpoint field. The required consumer
  action: FRONTIER's writer-source half is done at `57274cbd0` (intents bind the intended board sha; an altered
  interrupted write refuses to heal; pre-binding intents heal as `received-legacy`, the explicit unverified
  boundary). OPUS's migration-integration half stays open. No crash, fault campaign, fairness or production
  divergence was tested. *(Updated 2026-09-30 by SWE2-CONTRACT on FRONTIER-REQ-SWE2CONTRACT-PENDING-STATE-DONE-0930.)*

## Shared files, generators and publication

| Class | Treatment |
|---|---|
| Task-owned system pages, types, contracts, experiments, scripts | Claim the exact files; reader writes the finding; unique owner scratch/Ghidra projects |
| Shared manual files: OPEN-QUESTIONS, COVERAGE prose, PROGRAM-STATE, name equivalents, type TSVs | Claim the file before edits; otherwise stage in the author's inbox |
| Generated: RULES, ADDRESS-INDEX, coverage/readiness reports, knowledge SQLite, graph exports | Edit sources; invoke their existing generator with explicit inputs/output; never hand-edit generated facts. Canonical policy: [`_index/EVIDENCE-POLICY.md`](../EVIDENCE-POLICY.md); freshness mechanics: [`_index/DERIVED-DATA.md`](../DERIVED-DATA.md) — a derived snapshot is dated; check its recorded dependencies (`knowledge_db.py check` / `freshness_report`) before quoting it; STALE names the moved inputs |
| Mixed generated/manual: CONTRADICTIONS.tsv, COVERAGE | Preserve manual columns/prose using the owning tool; never replace with a pure generated approximation |
| History: inbox returns, AUDIT-LOG, evidence/correction trails | Append or annotate consumption with commit/reference; never erase the returned evidence |
| TEAM.json | Only team.py transactions; agent summaries derived from claims |

Single-row edits to `OPEN-QUESTIONS.md` go through
`analysis-kit/gfz-scripts/register_row.py` — row-scoped read-modify-write with a
stale-read refusal and a duplicate-id refusal, no lock. Batch imports and multi-row
edits stay whole-file under the file claim above. (OPUS-NOTICE-FLEET-REGISTER-ROW-TOOL,
routed 2026-09-15.)

Reserve the `@publication` resource in a short separate task before shared generation, GZF mutation,
Git staging/commit/merge/rebase, or canonical index integration. Any of the three can do this;
publication is a temporary responsibility, not a fourth identity or permanent coordinator.
The publication claim **does not grant ownership of another task's files**: also claim each output
file; if occupied, leave a handoff or wait while researching a different package. Keep independent
source edits outside the publisher's read set or checkpoint them until its gates finish.
Publishers compare relevant inputs before/after validation; rerun changed-input checks. Existing
non-atomic-gate rule remains: one transient red is not grounds for a semantic correction.

**Before publishing a correction** (EVIDENCE-POLICY rule 4a): (a) list the claim's current
consumers — owning contract, mechanism page, register row, summaries; (b) each is updated in this
publish or routed to its authorized editor with the exact text; (c) the commit message names the
propagation state; (d) the regression that rejects the old reading ships with it.

During publication: inspect status and recent history; never `git add .`/`-A` or commit someone else's
dirty files. Stage explicit reviewed paths; inspect the **entire staged diff**, run affected checks,
commit promptly, and release publication. No reset/clean/stash/force-overwrite of peer work.

> **Make the scoped commit with `Database/Tools/analysis-kit/gfz-scripts/publish_paths.sh
> <message-file> <path>…`, not with `git add` and `git commit`.** It seeds a **private index** from
> `HEAD` through `GIT_INDEX_FILE`, adds only the paths you name, commits from that, and leaves the
> repository index exactly as it was — so a peer's staged work **cannot** be swept in even if the
> script is run carelessly, and their staging survives your commit.
>
> **This is written here because describing the technique was not enough.** The rule used to end
> *"if pre-existing staged work exists, use a separate temporary Git index"*, the script that does
> precisely that has been committed since the second incident, and the sweep happened **a third
> time anyway** — `53fb13d` (OPUS, 2026-09-12) carried ASTRA's entire staged `EXP-076` evidence set
> and 36 lines of `ASTRA.md` into a commit about a mode ladder, while ASTRA held `@publication`.
> The publisher had checked the dirty column earlier in the session, correctly left `ASTRA.md`
> unstaged once, and then typed `git add` again an hour later. **A guard you have to remember is
> not a guard, and a tool the protocol does not name is not reached for.** Prior incidents:
> `OPUS-NOTICE-SWEEP` (commit `2897620`, EXP-030) and `OPUS-NOTICE-GUARD` (EXP-024, nearly).
>
> **And NAME THE FILES — the script now refuses a directory, because the private index does not
> prevent the other half of this mistake.** `git add -- <dir>` adds every changed file under that
> directory, which is exactly what was asked for, so a peer's work goes in even though the index was
> private. **One hour after the rule above was written, commit `3912914` did precisely that** — it
> named twenty-three category directories to reach thirty-four contracts and took three files inside
> two peers' **ACTIVE claims** with them: FABLE mid-answer to two of OPUS's own contradiction
> tickets, and ASTRA's new 191-line evidence document. `OPUS-NOTICE-SWEEP-DIRS` and
> `OPUS-NOTICE-SWEEP-DIRS-ASTRA`.
>
> **Two mistakes are possible and they need two different guards**: the work is already *staged*
> (the private index), or the path list *contains* it (the directory refusal). If a commit needs
> thirty files, list thirty — or generate the list, which is what anyone making a thirty-file commit
> should be doing anyway.
Resolve merges by evidence and provenance, then regenerate artifacts; never blindly choose a side.
Commit board snapshots and attributable handoffs with coherent checkpoints. After a finish/release,
TEAM.json alone may be pending until the next publication; that is explained coordination state.

GZF writers additionally obey the unchanged fresh-import/body-hash/exact-count/mutation/pack/
reopen gates. Read-only analysis uses agent-specific `-ProjectDir`, **unique `-ProjectName`**, and
explicit per-agent `-OutDir`; the verification default is keyed by project name, so different dirs
with the same default `GFZ_PARENT` name still collide. Never use another agent's project.
Read current parent values from `GfzEnv.ps1`, not old board hashes. Take `@runtime` before driving,
attaching to, instrumenting or closing the original-game reference process; read offline captures
freely. Reserve runtime only for the bounded experiment, never while waiting on static research.

**A stopped `@publication` holder (OPUS, ratified 2026-09-25 from
FRONTIER-REQ-OPUS-PUBLICATION-LEASE-TIMEOUT-RULE, with amendments).** The lease has no expiry, so a
session that stops while holding it blocks every publisher. It may be released without the holder,
but **only when all three of these hold — never on elapsed time alone**, because a live publisher
can legitimately hold the lease for an hour (SWE2-EC7 did, active throughout, on 2026-09-25):

1. no checkpoint on the holding task for **at least 6 hours**;
2. a checkpoint-or-release request addressed to the holder on the board, unanswered for **at least
   2 hours**; and
3. for **at least 2 hours**, no commit by the holder, no process attributable to it, and no write
   inside its claimed paths.

Then an adjudicator — **FRONTIER or OPUS, never the publisher who is waiting for the lease** —
records a board op that releases **the `@publication` key only**, citing the three measurements.
The holding task's **file claims stay with the holder** for a same-identity reclaim; its dirty
files are not staged, committed, reverted or moved by anyone else. A holder that resumes
reclaims `@publication` normally, and **inspects the log before re-running its publish** — its
commit may have happened before the stop. Until `team.py` has that op, the adjudicator uses no
substitute: it files the evidence and waits.

A publication task is finished **only with the hash `publish_paths.sh` prints as
`committed sha:`** — the pinned object it wrote. Never `git log -1`: a peer can commit
between the script's write and your read, and moving HEAD then names their commit. Never a
hash remembered from before the publish, and never from filtered script output. A refused
publish prints its refusal; a stopped one may still have committed — verify by checking
whether the *logged sha* exists (`git cat-file -t <sha>`), not by reading HEAD.

## Watchdog and improvement

The external roughly 60-second mechanism checks session/process state; it is **not a work interval**.
Do nothing while an agent is productively running, even if the claim checkpoint is old. Wake the
same identity/task only if unexpectedly idle/stopped, finished without selecting work, or stuck on a
blocked package; re-read board and session state immediately before waking. Never duplicate tasks or
inject periodic "continue" into active work. This bootstrap does not install another scheduler.

**Verified host interface (SWE2-FRONTIER, corrected 2026-09-13 evening):** the fleet's eight stable
session ids are `devin list --format json` titles `SWE2-*`; `devin auth status` now passes
(authenticated 2026-09-13). Two corrections to the earlier record: `devin -r <id> -p "Continue"`
resumes a session **in place** (same id, same chain — verified by a create-then-resume round trip)
and **only while its lock is free**. `%APPDATA%\devin\cli\session_locks\<id>.lock` is held by ANY
process that has the session open — including idle Devin Desktop tabs — so a held lock means *open*,
not *working*, and resume of a held session fails `session_locked` ("already open in another
process"). **For the controller to drive a lane, that lane's session must not be open in the
desktop** — close the tab (or the desktop), verify with `--status` showing `free`. There is no
supported inject-into-open-session path.

`swe2_watchdog.py` in `gfz-scripts/` is now an **event-driven, capacity-limited scheduler**, not
keep-alive: `target_active=3` / `hard_max=3` applies **only to the seven specialist lanes**
(EC7, CONTRACT, STRUCT, DATA, ORACLE, AUDIT-SEM, AUDIT-SPEC); the desired set comes from
`fleet-plan.json` (SWE2-FRONTIER's checkpoint duty) or a board heuristic (ACTIVE claim > targeted
READY request > unblocked lane research; auditors only while review work exists). FRONTIER is
**additive control-plane and holds no specialist slot** — it is manually active, and a pending
replan can wake it as planner outside the cap; its wakes never count toward `hard_max`.
Completed/blocked specialist lanes park and rotate in.

**Replanning is event-driven — workers never wake anyone.** Each worker keeps working
role-appropriate packages while useful work remains: a finished package means commit → update
resume state → claim the next role package → continue, NOT a replan. A worker requests replanning
only on a real condition — `NO_LOCAL_WORK`, `BLOCKED_NEEDS_SPECIALIST`, `REVIEW_QUEUE_READY`,
`HIGH_PRIORITY_REQUEST_RECEIVED`, `ROLE_QUEUE_DRAINED`, `ERROR_OR_COORDINATION_CONFLICT` — by
writing a durable event:

    python Database/Tools/analysis-kit/gfz-scripts/swe2_watchdog.py replan \
        --identity SWE2-XXX --reason ROLE_QUEUE_DRAINED --note "what I saw"

**Worker obligation:** before ending a turn on `NO_LOCAL_WORK`, `BLOCKED_NEEDS_SPECIALIST`,
`ROLE_QUEUE_DRAINED`, or a drained review queue, the worker MUST (a) update its resume block and
checkpoint, then (b) file the replan event — in that order, so the planner always sees a coherent
board. A finished package is not a replan: claim the next role package and continue.

Events are append-only files under `%USERPROFILE%\.swe2-fleet\replan-events\` — concurrent writers
cannot lose each other, and an event landing while the planner clears survives to the next cycle.
After a ~90 s quiet window the watchdog wakes FRONTIER **once** as planner (planner wakes use a
3-minute debounce, not the worker 15-minute one). FRONTIER then inspects board/requests/review
queues/rate-limit state, picks the smallest highest-value `desired` set, writes `fleet-plan.json`,
and clears the replan with `swe2_watchdog.py replan --clear --identity SWE2-FRONTIER` — clearing
is planner-only and refused for any other identity. Auditors wake only for a meaningful batch of
review work and park when drained.

Wakes are staggered (one per poll, ≥120 s apart) behind a fleet-wide circuit breaker: a wake that
dies on a Windsurf overall-message-rate error suspends ALL wakes for the reported reset plus a
~25 s margin, then re-probes ONE worker at a time. `tree-coaster` and `universal-coral` are never
woken; no session id outside the eight mapped identities is ever resumed. Guardrails kept:
debounce, daily cap, consecutive-failure stop, fail-closed on auth/CLI/lock ambiguity. Map, plan,
replan state, queued workers, breaker state and the JSONL telemetry log live under
`%USERPROFILE%\.swe2-fleet\`.

**Temporary fleet policy — ASTRA unavailable (until ~2026-09-19 usage reset, ordered
2026-09-13).** ASTRA is **not an eligible dependency** during this window. Rules for every SWE2
worker:

* Before classifying a question live-only, walk the cheapest-sufficient ladder: existing evidence
  → static/call/data analysis → scripts/resources → isolated verified original-code execution →
  ASTRA only if real runtime state is still required. Prefer SWE2-ORACLE for bounded
  original-code experiments, SWE2-DATA for authored-data/resource questions, SWE2-STRUCT for
  bounded ABI/type/state questions.
* A genuinely live-only question is preserved in [`ASTRA-QUEUE.md`](ASTRA-QUEUE.md) with the full
  item format (question, target/state, known evidence, competing interpretations, why offline is
  insufficient, exact discriminating observation, blocked claims, save/area/setup, priority).
  Deduplicate and batch compatible experiments. **Block only the affected boundary**, then
  continue other role-appropriate work; if none remains, raise `BLOCKED_NEEDS_SPECIALIST` via
  `swe2_watchdog.py replan` so the slot rotates to a more productive identity.
* No SWE2 slot stays occupied merely waiting on ASTRA. Evidence standards do not drop — no
  runtime-dependent conclusion is guessed. When ASTRA returns, FRONTIER re-triages the queue and
  only the highest-value truly live-only items go first.

All three may improve the process only for an observed recurring bottleneck, meaningful failure
class or clear high reuse across remaining work. Make the smallest useful change, validate it, then
return to FFXII. Once the bootstrap scenarios pass, stop building coordination infrastructure.

## Exact starting instructions

1. **FABLE:** use ID FABLE; run the startup commands and required reading; inspect READY candidates
   and current evidence for EE-2 (member-mask writer); claim FABLE-EE2 or a fresher unblocked semantic
   package, then follow the research/checkpoint/publication loop.
2. **OPUS:** use ID OPUS; run startup and reading; inspect EH-3/type-store current state for the
   ActorStorageRecord `+0x60..+0xB8` gap; claim OPUS-EH3 or a fresher type/contract package. Request
   evidence from FABLE/ASTRA with a separate bounded scope when needed.
3. **ASTRA:** use ID ASTRA; run startup, runtime-methodology reading and environment controls;
   the initial ASTRA-RT1 triage is banked in [ASTRA.md](ASTRA.md). Claim the next READY runtime
   package (initially ASTRA-RT1-CONTROL). Reserve `@runtime` only for the actual run. Bank blockers and take another useful
   runtime/evidence/tooling package rather than waiting for user gameplay.

These are identities/startup instructions, not a claim that external sessions have been launched.

### The team is eleven fixed production identities — 2026-09-13 (OPUS records once)

| identity | lane | inbox |
|---|---|---|
| `FABLE` | semantic architecture and families | [`FABLE.md`](FABLE.md) |
| `OPUS` | canonical specification and adjudication; EC-7 owner | [`OPUS.md`](OPUS.md) |
| `ASTRA` | original-runtime and live evidence | [`ASTRA.md`](ASTRA.md) |
| `SWE2-FRONTIER` | bounded offline closure of the unexplained frontier | [`SWE2-FRONTIER.md`](SWE2-FRONTIER.md) |
| `SWE2-EC7` | EC-7 dispositions that yield to measurement | [`SWE2-EC7.md`](SWE2-EC7.md) |
| `SWE2-CONTRACT` | contracts and differential harnesses | [`SWE2-CONTRACT.md`](SWE2-CONTRACT.md) |
| `SWE2-STRUCT` | structure and layout recovery | [`SWE2-STRUCT.md`](SWE2-STRUCT.md) |
| `SWE2-DATA` | authored data and container formats | [`SWE2-DATA.md`](SWE2-DATA.md) |
| `SWE2-ORACLE` | isolated original-code execution | [`SWE2-ORACLE.md`](SWE2-ORACLE.md) |
| `SWE2-AUDIT-SEM` | independent auditor — semantic packages | [`SWE2-AUDIT-SEM.md`](SWE2-AUDIT-SEM.md) |
| `SWE2-AUDIT-SPEC` | independent auditor — specification packages | [`SWE2-AUDIT-SPEC.md`](SWE2-AUDIT-SPEC.md) |

**A claim is not made until the Resume block says so.** The root `CLAUDE.md` continuity rule
already requires every `SWE2-*` identity to keep its inbox **Resume state** block current *at every
checkpoint*; this records that it is a **board-write obligation**, not a tidy-up. Whenever a lane
claims, checkpoints, blocks or finishes a task, the same turn updates *Current package/claim*,
*Exact next action* and *Latest coherent commit/checkpoint* in `<IDENTITY>.md`.

> **Observed drift, 2026-09-13:** the board carried ACTIVE tasks for `SWE2-CONTRACT` and
> `SWE2-STRUCT` while both Resume blocks still read *"Current package/claim: none"*. A restarted
> session rebuilding from that block would have re-claimed over its own live work. **The board is
> authoritative for claims; the Resume block is what a cold start reads** — when they disagree the
> lane has published a claim it cannot resume.

**`SWE2` did not disappear; it became `SWE2-CONTRACT`,** carrying its ACTIVE claim and the request
routed to it (`OPUS-REQ-SWE2-RAMP-DIFFERENTIAL`, verified on the live board before the rename, not
assumed). Its inbox moved with it — `SWE2.md` → `SWE2-CONTRACT.md`, renamed rather than re-created,
so its two checkpoints and the review it passed keep their file history.

**Nothing was redesigned.**

| what changed | what did not |
|---|---|
| `team.py`'s `AGENTS` set names the eleven | the board schema, the claim rules, `conflicts`, `ready`, `refresh`, `overlap`, the lock, the transaction log |
| the `SWE2` identity record and its six task references became `SWE2-CONTRACT` | **2,187 tasks, 6,604 history entries and revision 6,604 — asserted unchanged by the migration itself, which refuses to run otherwise** |
| seven new identity records, **all with no claims** | `@publication` exclusivity and `@runtime` reservation semantics |
| seven new inbox files | every existing checkpoint, request, lock and handoff |

**History keeps the identity that was current when it was written.** An entry recording that `SWE2`
did something on 2026-09-13 is true, and rewriting it to say `SWE2-CONTRACT` would falsify the
record to make a rename look tidy. The rename is stated here instead — which is what an operating
record is for.

`conflicts`, `ready`, `refresh` and `overlap` were already identity-agnostic: they iterate
`board["agents"]` and compare names. **That is why going from four identities to eleven is a data
migration and not a coordination project.**

**Review is no longer OPUS's first-line duty.** [`REVIEW-POLICY.md`](REVIEW-POLICY.md) defines the
tiers and the auditors. OPUS adjudicates disputes, high-blast-radius structured claims, escalated
universal or negative claims, and canonical acceptance — it does not review every package.

---

### ⚠ Superseded by the section above — SWE2 as a *fourth* identity, 2026-09-13 (kept as history)

*The text below was written when the team was four and `SWE2` was one generic worker. Its staffing
statement and its "OPUS is the default reviewer for the first ten packages" duty are **retired**:
the identities are the eleven above, and first-line review belongs to `SWE2-AUDIT-SEM` /
`SWE2-AUDIT-SPEC` under `REVIEW-POLICY.md`. The record of what was done — scenario G, the four-line
edit, the reviewed first package — stands.*

### SWE2 joins as a fourth production identity — 2026-09-13 (OPUS records once)

**The team is four.** `SWE2` is high-throughput bounded offline reverse engineering: original-code
fixtures, differential harnesses and backlog closure. Its inbox is
[`SWE2-CONTRACT.md`](SWE2-CONTRACT.md) *(named `SWE2.md` when this was written)*.

**The extension was deliberately the smallest one that works, and nothing was redesigned.**

| what changed | what did not |
|---|---|
| `team.py`'s `AGENTS` set gained `SWE2` | the board schema, the claim rules, `conflicts`, `ready`, `refresh`, the lock and the transaction log |
| two strings that said "three" now read the set (`validate` prints the count and the names) | every existing task, checkpoint and history entry |
| `TEAM.json` gained an SWE2 record with **no claims** | the revision counter, which `team.py` still owns |
| `test_team.py` gained scenario **G** | scenarios A-F, which pass unchanged |

`conflicts`, `ready`, `refresh` and `overlap` were already identity-agnostic - they iterate
`board["agents"]` and compare names - so **the contention rules needed no change at all.** That is
worth stating because it is the reason this was a four-line edit rather than a coordination project.

**Scenario G asserts the four-way cases rather than SWE2's existence**: one resource with four
claimants and exactly one winner; `@publication` exclusive across all four; `@runtime` unchanged
with a fourth identity present; a request addressed to SWE2 claimable by SWE2 **and by nobody
else**; and owner-only closure still requiring durable result references. **9 of 9 tests pass, and
`team.py validate` reports `4 identities (ASTRA, FABLE, OPUS, SWE2)` against the live board.**

### Review duty for SWE2's first ten FF12 packages

**OPUS is the default reviewer** for SWE2 packages touching bounded native behaviour, ABI or
signatures, exact memory writes and branches, original-code fixtures, differential harnesses,
contracts, types and fields, EC-7 dispositions, or structured propagation.

- Review reads the **shipping instructions, the fixture's behaviour, the tests and the database
  diff** — not the report.
- A defective package is returned with the **exact defect and its evidence**; SWE2 repairs the
  underlying cause and strengthens the tests where appropriate; the reviewer verifies the repair and
  only then closes it. **The reviewer does not silently redo the work.**
- After ten packages, the measured defect and rework rate decides whether review becomes
  risk-based. **Universal or high-blast-radius claims stay reviewed regardless.**

### EC-7 division, restated so nobody re-derives it

FABLE supplies **semantic families**, SWE2 **bounded offline and original-code closure**, ASTRA
**empirical runtime residue**, OPUS **canonical integration and precision**. The mechanism exists
and is not to be expanded for elegance; the priority is consuming the frontier. **Unsupported bulk
dispositions are refused, and that refusal is the mechanism working rather than failing.**
