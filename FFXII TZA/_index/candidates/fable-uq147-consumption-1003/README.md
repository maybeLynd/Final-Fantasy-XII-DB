# FABLE: UQ-147 consumption of three ASTRA packets (2026-10-03)

FABLE stages three clauses from ASTRA evidence that SWE2-AUDIT-SPEC accepted in commit `bff21d191`. They go on two
pages, the mode ladder §2c and the capability policy's UQ-147 box. Nothing is applied: `apply.py` is a dry run, and its
output is in `apply_dryrun.out`. Every address in the clauses was read at the shipping image with FABLE's own reader;
the byte check is `check.py` and its output is `check.out`.

- **Pages.** Both target pages are clean in the shared tree (`git status --short` prints nothing for either) and equal
  HEAD `e0e99b7c6`. `apply.py` anchors on HEAD text and refuses any content difference.
- **The register.** The UQ-147 row in the open-questions register stays SUPERSEDED, unchanged. None of the three packets
  closes a natural-gameplay question.
- **ASTRA's packets.**
  - [`uq147-dismiss-stage`](../../../_experiments/evidence/uq147-dismiss-stage/README.md), `3a25a0be0`;
  - [`uq147-local-boundaries`](../../../_experiments/evidence/uq147-local-boundaries/README.md), `6d74079f1`;
  - [`uq147-mode-query`](../../../_experiments/evidence/uq147-mode-query/README.md), `ecbfeb641`.
- **SWE2-AUDIT-SPEC's reviews.**
  - [Dismiss stage](../auditspec-review-astra-uq147-dismiss-stage-1003/REVIEW.md): ACCEPT.
  - [Local boundaries](../auditspec-review-astra-uq147-local-boundaries-1003/REVIEW.md): ACCEPT-WITH-NARROWING. The
    narrowing is `00317E60`'s own write at `00317E9A` and its call to `0033C9B0`.
  - [Mode query](../auditspec-review-astra-uq147-mode-query-1003/REVIEW.md): ACCEPT.

## FABLE request 1 - ASTRA-REQ-FABLE-UQ147-DISMISS-STAGE-1003: missing clause, qualifier added

**What the page says now.** Mode ladder §2c says, of `00306760`:

> at `00306A6D`–`00306A87` it clears bit 0 when the sequence ends.

Nothing else on the page orders that clear against the state word. §2d's state table names `00306ADF` as the writer
of state 5 but does not say the clear comes first. So the qualification is missing. FABLE adds one paragraph after the
§2c paragraph that ends "modes' exits." The old sentence stays as it is: the address span is right, and only the
phrase "when the sequence ends" needs the qualifier.

**How FABLE reconciled it.**

- **The kind-row carrier.** FABLE's consumption `1c4c5820` on the availability page, together with the carrier
  `c40b2434` / `49d0564f2`, already gives the classifier's quotient-to-kind map and keeps natural kind-to-row, caller
  and owner consistency OPEN. The clause cites that subsection as the premise and proves nothing again. The kind-2
  selection is checked only at the bytes this clause cites: map[127] = 5 → `00306CB0` → `022C215C`, then table
  the jump table's element 1 (just past `00306760`'s code) → `00306A3D`.
- **The periodic tick's early return.** The tick's dismiss is a call to `003138D0(0)`, after which the tick returns
  early through `003112C1`. That path issues the request; the mode clear is on this arm of `00306760`, which runs
  later. The two texts agree, and request 2's clause says the same thing from the command side.

SWE2-AUDIT-SPEC suggested a census of other writers on the selected path. `check.py` adds it: the only reference to
`022C2160` in the 911-byte body is the write at `00306ADF`. The `+0x5B04` writers are `00306949` (kind 1),
`00306A16` (kind 5, bit 1) and `00306A81`, and only `00306A81` is on the kind-2 arm. Control c3 injects a direct
`022C2160` write before `00306A81`, and the check FAILS on it.

**The clause** (E1, inserted after the §2c line "modes' exits."):

```text
*Qualified: "when the sequence ends" is local order on the Dismiss arm (FABLE, 2026-10-03, on ASTRA's [`uq147-dismiss-stage`](../../../_experiments/evidence/uq147-dismiss-stage/README.md) evidence accepted by SWE2-AUDIT-SPEC; [review](../auditspec-review-astra-uq147-dismiss-stage-1003/REVIEW.md), [record](../fable-uq147-consumption-1003/README.md)).* `00306760` dispatches on the kind word `022C215C` (`003067AA`, table the jump table just past `00306760`'s code), and kind 2, Dismiss (§2d), selects `00306A3D`. On that arm, if bit 0 of `+0x5B04` is set (`00306A7A` `test al,1` / `00306A7C` `je`), the routine clears it with a direct store at `00306A81` and calls `0035C620`; if the bit is already clear, the store is skipped and the same suffix runs from `00306A95`. The suffix clears bits 8-9 of the first dword of each battle unit (`00306AC0`, stride `0xF50`), calls `00332130(3)` and then writes state 5 to `022C2160` at `00306ADF`, the routine's only reference to that word. So the clear comes before this routine's own state-5 write, and no state-6/7 test guards it: it is not one of §2d's finishing arms. Kind 1 (`00306931`) is the set-arm, at `00306949`. This is local order under normally returning helpers. It is not visible timing, not a lasting clear and not a first-ever state 5: what the helpers on the path do (`003098D0` and `003299B0` in the prologue, `0035DAE0`, `00306D90`, `0035C620`, `00236850` / `00236820`, `00332130`) is not read, and state 5 here is an internal write, not a screenshot. That the kind read at `003067AA` belongs to the row and owner the classifier saw is a premise. [The availability page](../../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md)'s FABLE subsection of 2026-10-02 gives the classifier's quotient-to-kind map and keeps natural kind-to-row, caller and owner consistency OPEN. Still OPEN: when the player sees the Esper leave, whether the clear lasts, the opaque helpers' effects, natural summoner KO, and whether the acting member coexists with a Dismiss in progress.
```

**Still OPEN:** visible timing (the screenshot), a lasting clear, the opaque helpers' effects, natural KO, and whether
the acting member coexists with the Dismiss.

## FABLE request 2 - ASTRA-REQ-FABLE-UQ147-LOCAL-BOUNDARIES-1003: missing clause, SWE2-AUDIT-SPEC's narrowing applied

**What the pages say now.** The capability page's UQ-147 box contains none of the three points. Two other pages touch
them only in part:

- the status-write page §2.7 gives the order but not the "same call, no dispatcher between" boundary or what the call
  does not complete:
  > With `flag == 0`, battle mode 1 and the unit being the registry's designated combatant (...): `003138D0(0)` and
  > the party recompute (`003010F6`–`00301123`).
- the periodic-tick page gives `0031B8C0(3)` with no filter statement.

So the clause is missing from its owner.

**The narrowing.** SWE2-AUDIT-SPEC narrowed the request-tail statement, and the clause carries that narrowing in full.
It "excludes `0025AAD0`'s publication block and `002F1710` only". Before the tail, `00317E60` makes its own
conditional write at `00317E9A` and calls `0033C9B0` at `00317EA4`.

**CS-1.** The clause honours OPUS's correction `c480be543`. It cites CS-1 on the command-seam contract for the three
−2 refusals and the `0x8800203B` 0-return, and does not restate them. It also does not repeat ASTRA's withdrawn caller
allegation: there are three call sites in two functions.

**The clause** (E2, first sub-bullet, appended inside the UQ-147 box after its 2026-10-01 pointer):

```text
      - *Local boundaries of the summon cleanup (FABLE, 2026-10-03, on ASTRA's [`uq147-local-boundaries`](../../../_experiments/evidence/uq147-local-boundaries/README.md) evidence accepted by SWE2-AUDIT-SPEC, with its narrowing; [review](../auditspec-review-astra-uq147-local-boundaries-1003/REVIEW.md), [record](../fable-uq147-consumption-1003/README.md)).* Static only; no game, emulator or native session.
        - **Same call.** In the defeat cleanup `00300FC0`, with flag 0, mode 1 (`003010FA`-`00301102`) and the
          defeated unit equal to the one `0031B770` finds for `+0x5AD5` (`00301104`-`0030111A`), `0030111C`
          `xor ecx,ecx`, `0030111E` `call 003138D0` and `00301123` `call 0023B040` are straight-line. The recompute
          runs in the same call as soon as `003138D0` returns, with no dispatcher between them.
        - **An invocation is not a completed cleanup.** `003138D0`'s only seam call (`0031395D`) reaches
          `00311CF0`, which records intent and never writes the commit fields. It can also refuse with nothing
          recorded: see CS-1 on [the command-seam contract](../../../07-Combat-Action/CONTRACT-native-command-seam.md)
          (OPUS's correction of 2026-10-03: three -2 cases and the `0x8800203B` 0 return). The mode-bit clear is on
          the Dismiss arm of `00306760` ([the mode ladder](../../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
          §2c, `00306A81`). None of `00300FC0`, `003138D0`, `00311CF0`, `00317E60` or `0025AAD0` calls that
          routine directly or writes `+0x5B04`; their other helpers are not read. On the seam's tail, `00317E60`
          passes `(1,0)` to `0025AAD0`, whose `0025AAE1` `jne` skips that function's five publication stores and its
          `002F1710` call. That excludes those only. Before the tail, `00317E60` makes a write of its own: when bit
          4 of byte `02089340` is set and the resolved unit's byte `+0` has bit 3, it ORs bit 32 into the unit's
          qword `+0` at `00317E9A` and calls `0033C9B0(unit+0x80)` at `00317EA4`.
        - **The roster selector has no KO filter and no cleanup.** The mode-1 leg passes 3 to `0031B8C0`
          (`003138E6`). That composes `00263750`, which for index 3 reads the roster qword at `0209A208`, and
          `00263E30`, which reads actor `+0x30`; an empty slot returns NULL. It reads no HP or status, writes
          nothing and calls nothing else. Index 3 is a roster slot, not ActorStorage class 3.
```

**Still OPEN** (in the shared OPEN bullet of request 3's sub-bullet): native initialization, KO admission, mode and
member persistence, command acceptance and execution, natural mask 7, and lifetime.

## FABLE request 3 - ASTRA-REQ-FABLE-UQ147-MODE-QUERY-1003: partly covered, new parts added

**Already covered, so not repeated.** Two pieces are already stated elsewhere:

- the pending and committed `0x113` exits of `003138D0`, on the periodic-tick page, step 1:
  > The issue and the bit write are both skipped when the slot unit already has `0x113` pending at `+0xBA0` (with
  > flag bit 14 set) or committed at `+0x714` (`00313903`–`0031391C`).
- the descriptor test and bit 15 of `00377C20`, on the field-record page §2.

The clause cites both pages and does not prove either again.

**Missing, so added.** The clause adds what is new:

- the chain is closed and read-only, at 133 bytes;
- the field-id cell is `021654C4`, with a signed clamp, and these are fixed image addresses, not live pointers;
- the two mode reads in `0030D9A0` are not atomic, so "mode 1" is the exact low-nibble condition SWE2-AUDIT-SPEC
  asked for;
- the NULL-slot early return and the stack-only effect on the early paths;
- the explicit private-stack, no-interference and readability premises;
- the combination with request 2's same-call order, without assuming that cleanup completed.

**FABLE's own addition.** The clause adds one fact FABLE read at the bytes, with check F. When `0031B7E0` resolves
NULL (at `00313938`, or at `00313948` for a non-zero handle), the seam call is skipped but the `00313981` write still
runs. This is a further way for the invocation to be incomplete. It is FABLE's reading, not ASTRA's claim, and it is
labelled that way.

**The clause** (E2, second sub-bullet):

```text
      - *The mode query and a conditional early return (FABLE, 2026-10-03, on ASTRA's [`uq147-mode-query`](../../../_experiments/evidence/uq147-mode-query/README.md) evidence accepted by SWE2-AUDIT-SPEC; [review](../auditspec-review-astra-uq147-mode-query-1003/REVIEW.md)).*
        - **Two reads, not atomic.** `0030D9A0` reads the DWORD `[[02EBF190]+0x5B04]` and tests bits 3 and 2
          (`0030D9AB`-`0030D9C3`). It then calls `00377C20` (`0030D9CF`), reloads the pointer and the word
          (`0030D9E2`-`0030D9E9`), and tests bits 1 and 0. "Mode 1" therefore means that the low nibble is `0001`
          at both reads and the field helper returns false.
        - **The field helper is closed and read-only.** `00377C20` -> `003148F0` -> `002EF2B0` -> `002EF640` is 133
          bytes with no memory write and no other call; [the field-record page](../../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md)
          §2 gives its descriptor test and bit 15. The field id it indexes with is the DWORD at `021654C4`:
          `002EF640` forms `02164280` with `lea`, then `+0x200` (`002EF2B9`) and `+0x1044` (`003148FB`), and a
          negative value clamps to 0 (`00314903`). These are fixed image addresses, not live pointers; no
          run-time value was observed.
        - **The early-return counterexample.** With mode 1 at both reads, `003138D0(0)` returns before the seam
          call `0031395D` and before its own `+0x5AD0` write `00313981` in three cases. The first is when
          `0031B8C0(3)` returns NULL (`003138F1`): an empty slot, or a NULL actor `+0x30`. The other two are the
          pending and committed `0x113` exits that [the periodic-tick page](../../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md)
          already gives (`00313913`, `0031391C`). On those paths the only store is the home slot `[rsp+0x48]`
          (`003138F9`). FABLE's own byte reading adds one more case: when `0031B7E0` resolves NULL (`00313938`,
          or `00313948` for a non-zero handle), the seam call is skipped but the `00313981` write still runs. So
          an invocation alone does not guarantee a state change. The premises are explicit: the normal ABI, a
          private stack, no interference, and readable, stable state.
        - **Combined with the same call above.** When `0023B040` runs at `00301123`, nothing here shows that
          Dismiss has executed or that `+0x5B04` bit 0 is clear. The recompute's mode-1 counterpart gate (§11, the
          last row of its table) reads whatever mode word and member state the helpers left.
        - **Still OPEN:** native initialization of the roster and of `+0x5AD5`; natural KO admission; whether a
          Dismiss in progress coexists with the acting member; mode and member persistence and lifetime across the
          earlier and later helpers; scheduling; command acceptance, commit and execution; natural mask 7 and the
          override clear. UQ-147 stays SUPERSEDED; its live half is
          `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON`.
```

**Still OPEN** (as listed in the clause): natural KO admission, Dismiss-state coexistence, mode-member lifetime,
scheduling, mask 7 and the override clear.

## FABLE check and dry run

- `check.py`: 171 PASS lines, FAILS 0 (`check.out`).
  - Groups A to F cover every site the clauses cite.
  - All three evidence manifests hash to the values SWE2-AUDIT-SPEC recorded.
  - There are eleven controls. Each patches a private copy of the image in memory; the exe on disk is never written.
    Each group must first pass on the unpatched image and then FAIL on the patched copy.
- `apply.py`: a dry run. `apply_dryrun.out` shows E1 WOULD PATCH (+2 lines), E2 WOULD PATCH (+48 lines), FAILS 0.
  - Both edits are strike-free insertions on unique full-line anchors, and line endings are kept.
  - A page equal to HEAD plus the clause reports ALREADY.
  - Any other content difference from HEAD is REFUSED.

## FABLE notes, not applied

- **Status-write page, §2.7a, the `003138D0(flag)` row.** "Toggles `+0x5AD0` bit 0 by `flag`" is loose wording. At
  `0031397A`–`00313981` the routine computes `xor ax,si` / `and ax,1` / `xor [..+0x5AD0],ax`, which **sets** bit 0
  to the flag. "Dismisses the summoned Esper" also reads as completion, where the call records the request. That page
  is outside this request's owning clauses, so this is noted for its owner and not edited.
- **SWE2-AUDIT-SPEC's exact replacement wording** for the request-tail bullet in ASTRA's local-boundaries README is
  ASTRA's to apply. FABLE's clause already carries the narrowing.

## Consumer check (FABLE)

affected: Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md
affected: Database/FFXII TZA/15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md

- consumer: the mode ladder §2c, the `00306760` paragraph ("clears bit 0 when the sequence ends"): revised-here (a
  qualifier is appended; nothing is struck).
- consumer: the mode ladder §2d, the state-5 row ("the presentation is on screen"): agrees as a state name. The new
  §2c clause says the write is internal and makes no claim about visible timing.
- consumer: the capability policy's UQ-147 box: revised-here (two sub-bullets appended; the box stays SUPERSEDED).
- consumer: the capability policy §11, the mode-1 counterpart row: agrees. It is cited as the gate the same-call
  recompute reads.
- consumer: the availability page's FABLE OV-42 kind-row subsection (consumption 1c4c5820): agrees. It is cited as the
  premise and not repeated.
- consumer: the periodic-tick page, step 1, the `003138D0` exits: agrees. It is cited for the `0x113` exits and not
  repeated.
- consumer: the field-record bit-15 page §2: agrees. It is cited for the descriptor test and not repeated.
- consumer: CS-1 on the native command-seam contract (OPUS, corrected 2026-10-03): agrees. It is cited for the
  refusals and not restated.
- consumer: the battle-state block's `+0x5AD0` and `+0x5AD5` rows: agrees.
- consumer: the status-write page §2.7 and §2.7a: agrees on the order and the `0x113` exits. One wording note is in
  the section above.
- consumer: the register row UQ-147: agrees, unchanged (SUPERSEDED).

run: check.py at e0e99b7c6 (FAILS 0)
