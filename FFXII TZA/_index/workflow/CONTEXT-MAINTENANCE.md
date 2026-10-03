# Keeping current-state material current (FABLE, 2026-10-03)

*From the user's `FFXII_DB_RECONSTRUCTION_CONTEXT_REFRESH_PACKAGE_2026-10-02_v3` (the daily freshness policy) and
`FFXII_PROJECT_IMPROVEMENT_ADDENDUM_2026-10-03`. This adds no board, scheduler, dashboard or completion gate. It
says which existing mechanism keeps which surface current, and closes the one gap they leave: hand-maintained
entry points.*

## 1. Five kinds of material, five rules

| kind | examples | rule | mechanism that already enforces it |
|---|---|---|---|
| **A. Live current-state authority** | `TEAM.json`, Resume state blocks, `PROGRAM-STATE.md`, `OPEN-QUESTIONS.md`, `PARITY-STATUS.md` | must not stay materially stale across a working day | the board (`team.py`), the register gates (`check_questions`), publication |
| **B. Current entry points** | `Database/FFXII TZA/README.md`, TEAM.md *Starting or resuming*, `CLAUDE.md`, `RECONSTRUCTION-CHARTER.md` §0 | checked each working day when what they point to changed; volatile numbers are linked, never copied | `check_lifecycle_consumers.py` (§3) |
| **C. Policy and charter** | `RECONSTRUCTION-CHARTER.md`, `EVIDENCE-STANDARD.md`, `EVIDENCE-POLICY.md`, `COMPLETION-WORKFLOW.md` | edited only when policy changes, or when a contradiction is found | review and publication |
| **D. Generated current state** | `PROGRESS.md`, dashboard generations, `_index/knowledge.sqlite`, generated indexes | regenerated through their generator; never hand-edited to look fresh | `progress_report.py` fingerprints; `generation.py` (atomic generations, last-good, STALE on input drift, board-triggered rebuild debounced to 5 min, 30-min reconciliation); `knowledge_db.py check` (CURRENT/STALE, refuses stale reads unless `--snapshot`) |
| **E. Historical / sealed** | dated handoffs (the GM/GN-era continuation notes), dated audits, sealed evidence, earlier GFZ/GZF parents, proposals, session logs | immutable except through correction and supersession records; their age is expected | the correction gate; supersession links (§4) |

**Age alone is not a defect.** A file is stale when it states a superseded fact in the present tense. It is also
stale when its authority moved and it still repeats the old value, or when following it would send an agent to
obsolete work. A September file whose durable content is still right is current. The certified GN162 parent is still
the certified parent. Daily freshness never means bumping dates.

## 2. The working-day sweep

On each day with substantive work, one identity runs the sweep before that day's last durable checkpoint. FABLE runs
it by default, as owner of the meanings; any identity may. The sweep runs:

```text
python Database/Tools/analysis-kit/gfz-scripts/check_lifecycle_consumers.py      # lifecycle + entry points (§3)
python Database/Tools/analysis-kit/gfz-scripts/goal_gate.py                      # whole-database state
python Database/Tools/analysis-kit/gfz-scripts/knowledge_db.py check             # derived mirror CURRENT/STALE
```

It also confirms one more thing: the dashboard controller is healthy and the served generation is not STALE.

Then it asks the package's questions:
- Did the phase, the team, the frontier, L1/L2 status, the audit count or the parity status change?
- Was a canonical claim corrected?
- Did any current document go on saying the old thing?

It fixes the current authority, regenerates any derived output whose inputs moved, and leaves historical files
alone. When the sweep changes something, the checkpoint commit says so in one line: what was refreshed, what was
regenerated, and what was left historical on purpose. The dashboard's own 5-minute and 30-minute refresh is
stronger than daily and stays as it is.

## 3. `check_lifecycle_consumers.py`

This is the one new check. It covers the gap no existing mechanism did: hand-maintained entry points drifting away
from the lifecycle. It is deterministic. It compares sources with their consumers and does no free-text judging.
1. **The contract holds.** `PROJECT-LIFECYCLE.json` parses and keeps its invariants:
   - the goal is L1+L2;
   - L3 is not required;
   - user authorization is required;
   - there is no automatic transition;
   - the original game is not the production backend.
2. **The charter agrees.** `RECONSTRUCTION-CHARTER.md` §0 states the same phase and the same rules, and lists every
   maturity label.
3. **The entry points point at it.** The database README, TEAM.md and DASHBOARD-MEANINGS link §0 or the JSON. The
   README's stated phase equals the JSON's.
4. **Known superseded phrases are absent** from those current surfaces unless struck through. Examples are the
   "not sealed" residual wording and the readiness-gate endpoint.

5. **No current entry point offers a historical artifact as a resume point** *(added 2026-10-03)*. The supersession
   index [`SUPERSESSION.json`](SUPERSESSION.json) lists artifacts by path, with a label. The README or TEAM.md may
   link one only on a line that also carries the label's key word: HISTORICAL, SUPERSEDED, SEALED, AS-OF or
   PROPOSAL.

It prints one line per finding and `FAILS N`. `--self-test` runs six mutations, each of which must fail.

## 4. Supersession index (labels where linked; the files themselves are not edited)

The machine-readable form is [`SUPERSESSION.json`](SUPERSESSION.json), which §3 check 5 reads. The table summarises it.

| artifact | status | superseded by | why |
|---|---|---|---|
| GM160 / GN-era continuation handoffs and dated session handoffs | HISTORICAL CHECKPOINT | each identity's Resume state block; `PROGRAM-STATE.md` | the frontier advanced through GN162 and the database phase that followed |
| `_inbox/EXTERNAL-CONTINUATION.md` (titled "current handoff", SECTION-12, 2026-09-24/25) | SUPERSEDED CURRENT-STATE VIEW | each identity's Resume state block; TEAM.json | SECTION-12 was accepted on 2026-09-29. The file is labelled here, not edited, because the user's external-update overlay writes it |
| `_index/workflow/START-HERE.md` | HISTORICAL CHECKPOINT (the 2026-09-28 migration ZIP's own start file) | `COMPLETION-WORKFLOW.md` (adopted) and TEAM.md *Starting or resuming* | it tells the user and FRONTIER how to install the migration, which is done. *(Corrected 2026-10-03: `ALL-TOP-LEVEL-GOALS.md` was listed here too, but it is NOT superseded. It holds the agents' goal texts, which TEAM.md names as governing.)* |
| TEAM.md *Exact starting instructions* (FABLE EE-2, OPUS EH-3, ASTRA-RT1) | HISTORICAL CHECKPOINT, labelled in place | TEAM.md *Starting or resuming* | first claims of the week of 2026-09-13 |
| `RECONSTRUCTION-READINESS-GATE.md` as an endpoint | SUPERSEDED CURRENT-STATE VIEW (still a valid instrument) | L1+L2 via `goal_gate.py`, then user authorization (charter §0) | endpoint replaced 2026-09-12 (TEAM.md) |
| the supplied `knowledge.sqlite` of 2026-09-26 (pinned `43f63e7ac`) | AS-OF SNAPSHOT | the active mirror when `knowledge_db.py check` reports CURRENT | a newer ZIP name is not freshness |
| dated audits, sealed evidence, proposals, earlier GFZ/GZF parents | HISTORICAL / SEALED EVIDENCE / PROPOSAL | — | provenance; never redated |

## 4b. Which existing check covers each consumer pair (FABLE, 2026-10-03; the improvement addendum's §7)

The addendum asks that the most damaging "two current files say different things" cases be detectable mechanically.
Each pair it lists has an owner check:

| consumer pair | check | owner |
|---|---|---|
| README current facts vs generated state | the README copies no volatile numbers; it links them (`check_lifecycle_consumers.py` §3 checks 3-4) | FABLE |
| dashboard labels vs `DASHBOARD-MEANINGS.md` | `Database/Tools/dashboard/test_lifecycle.py` L9, run against §6 | SWE2-FRONTIER |
| current progress summaries vs source registers | `progress_report.py check` (fingerprints); `ps_present_tense_check.py` (PROGRAM-STATE present tense) | SWE2-DATA |
| current parity summary vs parity records | `check_parity_current.py` | kit tool with no single owner; PARITY-STATUS.md was last edited by SWE2-CONTRACT (2026-09-22) |
| current parent/GFZ identity vs environment | `goal_gate.py` *scope* and *provenance* (certified parent, 0 residual) | OPUS |
| active handoff blocker vs current resolved/unresolved status | `check_status_residue.py` (status lines vs register rows); SUPERSESSION.json + §3 check 5 (no stale handoff as a resume point) | FABLE |
| current reconstruction count/status vs indexed records | `knowledge_db.py check` (mirror freshness); `readiness_view.py` (phase cap) | SWE2-DATA, SWE2-STRUCT |
| lifecycle/phase wording vs canonical lifecycle | `check_lifecycle_consumers.py` | FABLE |

**A gap no current check covers:** a batch publish that re-commits stale copies of pages, reverting newer text. One
reverted FABLE's S-36 correction (`95b1f3a4c`, found by the audit follow-up's L2 sample). `survive.py` in
`auditsem-l2-sample-1003` finds candidates. Turning it into a pre-publish gate is proposed in
`FABLE-REQ-OPUS-L2-SAMPLE-EXPANSION-1003`.

## 5. Who owns which part

| part | owner |
|---|---|
| lifecycle text (charter §0, the JSON), the meanings, this file, the checker | FABLE (semantics); the user changes the phase |
| dashboard views that render the phase, the blocking chain, recent knowledge changes and the provenance drawer | SWE2-FRONTIER (deployment), with OPUS's `VIEW-SCHEMA.md` and FABLE's meanings §6 |
| `PROGRESS.md`, `knowledge.sqlite` refresh, `PROGRAM-STATE.md` data sections, knowledge-versus-activity reporting | SWE2-DATA |
