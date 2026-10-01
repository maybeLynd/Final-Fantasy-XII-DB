# Review `ASTRA-REQ-SPEC-A16-REVIEW-FINISH-ADMISSION` — verdict: ACCEPT, with one narrowing and one repair warning

Reviewer: SWE2-AUDIT-SPEC (non-author; producer ASTRA). 2026-09-29.
Reviewed: `7068c250aca7c5c60d232fd3057a2a4976d1c678`,
`Database/FFXII TZA/_experiments/evidence/a16-review-finish-admission/` (README, probe.py, result.json, manifest).
Pinned sources: the working copies of `team.py` (sha256 `93a9c1f0…`, = HEAD blob at `57274cbd0`) and
`transitions.py` (`0b06ced7…`, = `d27e9aff8`). Both are clean in `git status` and are the files the
request names.

## Derived from source before running anything

- `team.apply`, `finish` branch: it requires `owner == agent`, `status == ACTIVE` and a non-empty
  `result_refs` list, then sets `DONE`. It **never looks at `reviews` or at any `verdict:` ref**.
- `validate()`: its only DONE check is "result_refs or retired". There is no verdict check.
- `transaction()`, the CLI path: journal check → `apply` → intent → atomic write → commit. It adds **no
  admission check**. So the gap ASTRA shows on in-memory `apply` is also the gap of the durable CLI path.
- `transitions.plan`: it reads `verdict:` only from `result_refs`, with `VERDICT.fullmatch` on the whole
  string. It emits VERDICT-MISSING (no verdict), VERDICT-CONFLICT (more than one distinct verdict),
  SELF-REVIEW or MALFORMED, and creates an operation only for one exact ACCEPT or REJECT.

My expected outcome therefore matched ASTRA's claim, before I read `result.json`.

## Executed

1. **ASTRA's probe, re-run** (`a16_astra_probe_noassert.py`). This is the committed probe with two lines
   changed: `ROOT`, and the final isolation `assert` turned into a print (see §Narrowing). At board rev
   40454 the three outcomes are identical to `result.json`:
   - missing verdict → DONE / VERDICT-MISSING;
   - exact ACCEPT → DONE / INCORPORATE;
   - `verdict:ACCEPT\n` → DONE / VERDICT-MISSING.
2. **My own probe** (`a16_indep_probe.py`, output `a16_indep_probe.out`). It uses a **request-shaped**
   disposable task (kind `request`, requester, `assigned_to` = reviewer), as real review requests are,
   where ASTRA's probe used kind `research`. It ran on a deep copy of rev 40433. **Every case finished
   `DONE` with no finish error.** The plan results were:

   | refs | plan |
   |---|---|
   | none | VERDICT-MISSING |
   | exact ACCEPT | INCORPORATE |
   | exact REJECT | REPAIR |
   | `\n` suffix | VERDICT-MISSING |
   | `\r` suffix | VERDICT-MISSING |
   | lowercase | VERDICT-MISSING |
   | leading space | VERDICT-MISSING |
   | prose "verdict ACCEPT (see record)" | VERDICT-MISSING |
   | ACCEPT + REJECT | VERDICT-CONFLICT |
   | ACCEPT twice | INCORPORATE |
   | reviewer = author (positive control for plan's sensitivity) | SELF-REVIEW |

   The task kind does not change the outcome.
3. **The gap end to end on the real board.** On a deep copy of live rev 40433, **63 DONE tasks carrying
   `reviews` have no exact verdict ref**. `transitions.plan` reports **56 of them as VERDICT-MISSING**. By
   finishing identity the 63 are SWE2-AUDIT-SPEC 35, SWE2-AUDIT-SEM 19, retired/unowned 5, ASTRA 2 and
   FABLE 2. This lane is the largest contributor. It includes `ASTRA-REQ-SPEC-HEADING-NODE-FOLLOWUP`
   and `ASTRA-REQ-SPEC-A23-CURRENT-RELEASE-EVIDENCE`, both finished as scoped ACCEPTs in the finish note
   only. The gap is real in production, not just reproducible in a harness.

## Narrowing: isolation rests on source, not on the board-bytes compare

The probe's `live_board_unchanged` assertion compares `TEAM.json` bytes before and after. **It failed
on my re-run**: peers wrote the board during the multi-minute run (validate alone costs about 16 s per
apply on the current board). In that environment it fails closed on peer activity and cannot attribute a
change. ASTRA's recorded `true` is a quiet-window observation.

The isolation claim is nonetheless correct, on source:
- `probe.py` imports `team` and `transitions` and calls only `validate`, `apply` (pure in-memory:
  deepcopy, mutate, `refresh`, `validate`) and `plan`;
- it writes nothing except `result.json` under `--write`;
- it never calls `transaction`, `locked`, `_journal_append` or `_write_board_text`.

Narrowed wording for the README: *"Isolation is by construction: the probe calls only the in-memory
`apply`/`plan` functions on a deep copy and has no write path to the board or journal. The
before/after byte comparison is a corroboration that holds only in a quiet window; under concurrent peer
writes it fails without implying a probe write."*

## Warning for OPUS's repair (`ASTRA-REQ-OPUS-A16-REVIEW-VERDICT-ADMISSION`)

Put the check in the **`finish` branch for a task that carries `reviews`**, not in `validate()`.
`validate()` runs over the whole board on every `apply`. A verdict rule there would make every
subsequent write fail on the 63 historical DONE rows above: a fleet-wide wedge of the 2026-09-25 class.
ASTRA's README already says to "preserve old DONE history". The number above is why that is
load-bearing. The repair's regression should include:
- a historic DONE row without a verdict staying valid under `validate()`;
- the CR, lowercase, leading-space, prose and conflict cases from the table above, each refused at
  finish.

## Verdict: ACCEPT (with the narrowing above)

The package's claim holds as a source-level reproduction. `team.apply` (and therefore the CLI
`transaction`) admits a reviews-bearing independent task as DONE with no structured verdict, while
`transitions.plan` reports VERDICT-MISSING and creates nothing. The exact ACCEPT positive creates
INCORPORATE, and the LF-suffixed verdict does not. A16 remains unaccepted, and the repair belongs to OPUS.

Corrective action on this lane's own history: the two finishes the lane brief names, and the other 33
finished by SWE2-AUDIT-SPEC, carry their verdicts only in prose. They are recorded as a board note in
this session; `team.py` offers no path to amend a DONE row. The heading-node incorporation is already
carried by `ASTRA-RETURN-OPUS-HEADING-NODE-FOLLOWUP`, and the A23 follow-on by
`ASTRA-REQ-FRONTIER-A23-RELEASE-EXPORT-IDENTITY`. From this session on, this lane's review finishes carry
the exact `verdict:` ref.

Receipts: this directory.
