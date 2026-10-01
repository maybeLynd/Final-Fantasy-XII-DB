# Three-agent bootstrap — implementation and validation

## Old assumptions, preserved rules and obsolete instructions

Inspected the nested XIIOnline repository at `910f05d` on `master`, its one-worktree layout,
README/rules/mission/charter/completion plan, current appended frontier, coordination inboxes,
GZF wrappers, runtime methodology and recent workflow history. The outer `repos` Git repository
is a separate server checkout and is not the database publication target.

The old board had six helper identities plus a coordinator, later two more category sessions,
hard category lanes and enemy-record priority, coordinator-only indexes/GZF mutation, and a
cross-account messaging failure. It records real question-ID, mistaken-identity, duplicate-research,
mid-write-gate and output-directory collisions. Its September 6/7 rows are historical, not live
ownership. All old returns and corrections remain available for inbox-backlog reconciliation.

Preserved: binary/provenance authority, evidence tiers and bans, falsification/reopening propagation,
permanent corrections, reader-authored documents, private Ghidra projects, exact mutation/pack/reopen
fences, question-prefix validation, existing knowledge backlog/readiness machinery, generator
ownership and Git discipline. Retired: helper slots, coordinator identity, discovery-derived names,
hard silos, stale lane priorities, deleting consumed evidence, and deferring every runtime task to
the end. No scientific completion bar was lowered.

## Implementation and changed files

- `Database/FFXII TZA/_index/_inbox/TEAM.md`: sole current operating protocol and exact startup steps.
- `Database/FFXII TZA/_index/_inbox/TEAM.json`: three identities, bounded claims, requests and history.
- `Database/Tools/analysis-kit/gfz-scripts/team.py`: atomic claim/handoff transactions and validation.
- `Database/Tools/analysis-kit/gfz-scripts/test_team.py`: A–F plus failure/concurrency tests.
- `_inbox/.gitignore`: temporary board locks/writes excluded from Git.
- `_inbox/README.md`: retain evidence lessons; replace obsolete coordination authority.
- `_inbox/ASSIGNMENTS.md`: explicit historical-only notice, original record preserved beneath it.
- database `README.md` and `_index/PROGRAM-STATE.md`: point startup to the current protocol.
- `_index/COMPLETION-PLAN.md`: revise runtime ordering while retaining completion criteria.
- `gen_rules_index.py` and `_index/RULES.md`: index the current protocol and regenerate normally.
  Regeneration also catches up accumulated headings/checkers in the previously stale generated index;
  generated output was not manually trimmed to disguise that drift.
- `_inbox/ASTRA.md`: actual first runtime/environment triage checkpoint and next experiment.
- this report.

IDs/specialties: **FABLE** semantic/static/system research; **OPUS** types/signatures/contracts/
dependencies/readiness; **ASTRA** runtime experiments/evidence/tooling/process improvement/skeptical
validation. All three currently work toward `DATABASE`; phase can later change without new identities.

Claims use task IDs, owners, targets, bounded scopes, resources, status, dependencies, completion
conditions and timestamped checkpoints. Exclusive lock creation plus atomic replacement prevents
two claim updates winning together. Whole-object/range and parent-file/child-file overlap is checked.
This remains a cooperative protocol: agents must identify equivalent semantic targets and declare
the files they edit; it cannot prevent an editor deliberately bypassing the board.

Requests use existing durable inboxes plus recipient-addressed tasks containing question, known
evidence, exact missing information, importance and blocked work. Results reference durable evidence.
Contradictions preserve both positions and route reopening/resolution through existing scientific
records. READY/ACTIVE, cross-agent/runtime requests and contradictions are board views; the existing
open-question/frontier machinery remains the main backlog. Blocking banks work and frees its scope.

Shared checkout retained because current ignored tool/evidence dependencies and absolute-path
consumers already work there. Any of the three can claim temporary `@publication` responsibility;
shared output files need claims too. Generated indexes come from their owning generators. GZF
mutation remains serialized under its original gates. Unique project names **and** explicit private
OutDir prevent the verifier's project-name-keyed default output collision. `@runtime` serializes
driving/instrumenting the reference process. No extra workers, worktrees or scheduler were created.

The external roughly 60-second watchdog checks state and recovers idle/stopped/blocked agents;
it leaves productive sessions alone. No periodic continue injection or duplicate task creation.

## Simulation and validation results

`test_team.py`: **8 tests passed**, including actual subprocess contention:

| Scenario | Result |
|---|---|
| A | FABLE's semantic claim hides overlapping OPUS work; OPUS claims a different target |
| B | OPUS request is visible/claimable by ASTRA; durable result unlocks the dependent package |
| C | Contrary evidence and original claim both survive; disputed file waits for owner release |
| D | Completion exposes the next unblocked task in priority order |
| E | Publication and generated-directory/file overlap reject simultaneous owners |
| F | Blocker/resume condition retained; ASTRA takes another package and later resumes |
| Additional | Invalid identity/range/foreign release rejected; adjacent ranges allowed; two real processes yield exactly one winner; failed write leaves bytes unchanged; live lock cannot be stolen |

Also passed: live board validation; rule-generator self-test/reproducibility; database link check;
question/checklist consistency (891 register rows); source hygiene; cross-document consistency
(245 system documents, zero size/name/caller disagreements or frontmatter defects); Git diff checks.
The first source-hygiene invocation used an unsupported `--db` option and failed argument parsing;
the corrected documented `--paths` invocation passed. No semantic/GZF/type changes were made, so
native certification and unrelated DLL/reconstruction suites were not run for this bootstrap.

ASTRA then ran the existing runtime environment control self-test (four cases passed), found a
clean authority-matching Steam reference, rejected both mod clients, and observed no running FFXII
process. RT-1 triage and the next state-matched no-arm experiment are in [ASTRA.md](ASTRA.md).
No runtime observation of game behaviour or cure for RT-1 is claimed.

## Commit and starting instructions

The bootstrap is committed as one scoped milestone; obtain its exact hash with:

```powershell
git log -1 --format=%H -- 'Database/FFXII TZA/_index/_inbox/BOOTSTRAP-2026-09-10.md'
```

Pre-existing unrelated state was preserved: `Collaboration/tools/los_view/los_live.js`,
`Reconstruction/Game/Input/name_registry.c`, `.claude/settings.local.json`,
`Collaboration/models_browser.html`, `Collaboration/script_events/`,
`Collaboration/tools/native_lab/`, `Reconstruction/Tests/Differential/_fmb.bat`, and
`XIIOnlineNet/.claude/`. The milestone's files are committed; the whole checkout was already dirty
and was not reset/cleaned to create an artificial clean status.

Use the [exact startup commands and reading list](TEAM.md#start-and-choose-the-next-package):

1. **FABLE:** ID FABLE; inspect claims/current EE-2 evidence, claim FABLE-EE2 or a fresher semantic
   package; work, validate, publish, then immediately select the next unblocked package.
2. **OPUS:** ID OPUS; inspect current EH-3/type rows, claim OPUS-EH3 or a fresher type/contract
   package; use specialized requests when evidence is missing.
3. **ASTRA:** ID ASTRA; initial ASTRA-RT1 triage has finished. Continue with ASTRA-RT1-CONTROL
   from the board, the [triage handoff](ASTRA.md), and current runtime controls; take `@runtime`
   before operating the game. Stop infrastructure work and follow the database loop.

The bootstrap configures exactly three identities and proves the coordination scenarios. FABLE
and OPUS external sessions were not launched by this task; their startup instructions are ready.
