---
contract: One intent seam and one commit funnel, and two identical rings that carry different transactions
category: 07-Combat-Action
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 07-Combat-Action/Command-And-Action-Seam/native-command-seam.md
entries: ["00311CF0", "0030F760"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's writer census **re-run
    image-wide rather than carried**, over the three commit fields, **with the page's own named
    exception used as the control** — it reappears on exactly the field the page says and not on the
    other. **This records checks performed on that date, not the method of the original derivation**,
    which is on the seam page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-command-seam-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the native command seam

> **Authored 2026-09-22 by FABLE.** S-20's binding gap is *"2 contracts over 4 pages"*. **This takes
> the command seam.**
>
> Written against FRONTIER's adequacy test. **`CS-2` and `CS-3` are both cross-operation by
> construction**: one says which of several bodies may write a field, which no single body can
> state, and the other says that two structurally identical rings must not be merged — a statement
> about a pair.

## 1. Purpose

Get a decided action onto a unit, from whichever source decided it.

## 2. Interface

| | body | role |
|---|---|---|
| **the intent seam** | `BattleUnit_IssueCommand` (`00311CF0`), 283 B | takes **resolved** focus / `BattleStats` identities |
| **the commit funnel** | `BattleUnit_CommitAction` (`0030F760`) | installs the action on the unit |

## 3. Types

```
battle unit
  +0x6B4   u8    phase, reset by the commit
  +0x708   ptr   the order / action context   \
  +0x710   u32   the target focus handle       |  the three commit fields (CS-2)
  +0x714   u16   the action id                /   -- and +0x714 is what the dispatcher re-reads
```

*Corrected 2026-09-27 (FABLE, Claude Opus 5.5), on OPUS-NOTICE-FABLE-COMMAND-SEAM-710-IS-A-HANDLE: `+0x710` was listed `ptr`. It is a 4-byte handle (`targetFocusHandle` in the store): the action id at `+0x714` starts 4 bytes later, and the flow census shows 4 dword writes and 17 dword reads; the only 8-byte accesses are two `movsd` copies of `+0x710`/`+0x714` together (`00236B6A`, `0030F81B`).*


## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**CS-1 — ONE intent seam, and it takes RESOLVED identities.** `BattleUnit_IssueCommand` is reached
through two callers only — the by-focus-handles fan-out and the defeat-cleanup step — and its
arguments are receiver-local focus and `BattleStats` identities, **not raw input and not a target
search**. *So target resolution happens above the seam, and everything below it sees an already
decided receiver.*
**The seam records INTENT only; it does not reach the commit funnel** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 351](../_index/candidates/s20-opus-replay-command-seam/README.md), which executed it 4/4; `00311CF0` re-read whole.)*.
- **What it records.** It stores the command at `+0xBA0` (`00311D7A`) and the target at `+0xBB8` (`00311DB0`). It
  marks them pending with `+0xBA4` bit 15 and unit bit 14 (`00311DB6`–`00311DC2`).
- **What it does not write.** It never writes `+0x708` / `+0x710` / `+0x714`. A dispatch after the seam alone reads
  `+0x714` = 0 and returns −1. Intent and commit are therefore separated in time, and what carries `+0xBA0` into
  the funnel is not read here.
- **Its return cannot separate refusal from success.** A status in `0x8800203B` jumps from `00311D72` to
  `00311DED`, which returns **0** with nothing recorded, the same value as the success path. Only a null stats
  record, or the `0x80000003` status gate with the field bit clear, returns −2.

**CS-2 — ONE commit funnel, and the three commit fields have no other writer in the battle-unit
population.** Re-measured image-wide: within the battle-unit bodies, `+0x708`, `+0x710` and `+0x714`
are written **only** by `BattleUnit_CommitAction`, `BattleUnit_CancelAndResetCurrentAction` and
`BattleUnit_ResetStateForReuse`.

> **The control is the page's own named exception, and it reappears exactly where the page puts
> it.** `00328640` — the `talktreasure` verb's chain — writes a **target focus without an action**:
> it shows up on `+0x710` and **not** on `+0x714`. *A census that had drifted would not reproduce an
> asymmetry that specific.*

**CS-3 — TWO 64-entry rings that are structural twins and MUST NOT be merged.** `022BEDA0` and
`022BE980` share the same paired byte indices, the same 8-byte stride and the same mod-64 advance
~~and the same resolve-then-act drain loop~~. **They carry different transactions**: the first is
presentation-ready notification, the second is pending action selection, drained up to eight entries
per call.
*Restated 2026-09-26 (FABLE, Claude Opus 5.5), on `OPUS-NOTE-FABLE-S20-CS3-DRAINS-DIFFER`; bytes re-read:* **the drains
differ.** The instruction sites are on [the seam page](Command-And-Action-Seam/native-command-seam.md) §2's ring diagram.
- **The action drain pops up to eight entries per call, whatever they resolve to.** An entry that does not resolve
  still uses one of the eight.
- **The presentation drain stops at the first entry that does not resolve.** It loops on only past units that resolve
  but do not qualify.
- So ten unresolvable entries leave the action ring in two calls (eight, then two), and the presentation ring one per
  call. Executed with no stub: `candidates/s20-opus-replay-rings/` (OPUS; re-run by FABLE 2026-09-26, all pass).
- The shape above, the indices, stride and advance, is unchanged, and so is the rule that the rings must not be
  merged. *They are easy to confuse precisely because nothing in their shape distinguishes them —
which is why the distinction has to be a contract rather than a comment.*

**CS-4 — The presentation ring is NOT command intent, because of who fills it.** Its only producer
sits inside `BattleUnit_AdvanceStandardActionState`'s post-commit pipeline, and only when the
presentation slot reports ready. *So draining it does not issue anything; it consumes a lifecycle
notification that a commit already produced. Calling the drain by hand would consume whatever local
queue state happened to exist.*

**CS-5 — `+0x714` is the field the ACTION DISPATCH re-reads, so the commit funnel feeds the handler
table.** [The handler-table contract](CONTRACT-battle-action-handler-table.md)'s `HT-3` establishes
that the dispatcher tail-calls with only `this` set and the handler recovers the id from
`unit + 0x714`. **`CS-2` says which bodies may put it there.** *Together they close the loop: one
funnel writes the id, and the dispatch trusts the field rather than an argument — so a port that
passes the id as a parameter must also decide who is allowed to write `+0x714`, a question it would
otherwise never be asked.*

**CS-6 — The census that establishes `CS-2` cannot be stated as a bare displacement count, and the
figure is the reason.** A whole-image sweep for writes at `+0x714` returns **eight bodies**, of which
only three are battle-unit bodies; the other five sit in the `005…`/`007…` bands and are unrelated
structures that happen to carry a field at that offset. *So "three writers" is a claim about a
population, not about a displacement, and quoting the raw eight would contradict the page while
measuring the same thing.*

## 5. State

**Owned:** nothing. **Written:** the three commit fields and the phase byte, by the funnel.
**Consumed:** the two rings, by their own drains.

## 6. Relationships

| | |
|---|---|
| **Feeds** | [`CONTRACT-battle-action-handler-table.md`](CONTRACT-battle-action-handler-table.md) — `CS-5` |
| **Sibling** | [`CONTRACT-combo-continuation.md`](CONTRACT-combo-continuation.md) — one of the funnel's four callers commits a combo continuation |
| **Sources that reach the funnel** | the issued command (human, guest, script), the gambit / AI order sets, the combo continuation, and the engage auto-attack |

## 7. State transitions

*resolve a receiver → intent seam → selection → commit funnel writes `+0x708`/`+0x710`/`+0x714` and
resets the phase → post-commit pipeline → presentation ring, when the slot is ready.*

## 8. Script · resource · event interactions

Script commands reach the funnel as issued commands, through the same seam as human and guest input
(`CS-1`). The engage auto-attack arrives from a reaction-animation event.

## 9. Determinism

Deterministic at this level. What the committed action then computes is the formula side's.

## 10. Failure paths and edge conditions

- A target focus can be written **without** an action, by the `talktreasure` chain (`CS-2`).
- Draining the presentation ring by hand consumes lifecycle state and issues nothing (`CS-4`).
- The two rings are indistinguishable by shape (`CS-3`).

## 11. Observable behaviour

None directly. This is the join between deciding to do something and the unit doing it; the visible
consequence of merging the two rings (`CS-3`) is actions that fire when an animation finishes.

## 12. Reproduction formula

Census writers of `+0x708`, `+0x710` and `+0x714` and assert **three battle-unit bodies** on each,
plus `00328640` on `+0x710` **only** (`CS-2`). Assert the `+0x714` sweep returns eight bodies
image-wide and that five are outside the battle-unit population (`CS-6`). Assert the two ring heads
have identical index/stride/advance structure and different producers (`CS-3`, `CS-4`).

## 13. Runtime validation

~~**None.** No experiment executes this seam. S-20's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*~~ **Superseded
2026-09-25:** [OPUS block 351](../_index/candidates/s20-opus-replay-command-seam/README.md) executed the seam, the commit funnel and the dispatch after them (4/4). CS-5 closes as an
execution: the committed `0x4005` reaches `table[5]`, and the pending one does not. The evidence class is native
replay, not live.

## 14. Unresolved

- Whether the pending-selection ring can hold an entry that the commit funnel then rejects, and what
  happens to it if so.
- Why the two rings were built as twins rather than one parameterised structure.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `CS-2`, `CS-6` — the writer sets | an image-wide displacement census of `+0x708`/`+0x710`/`+0x714`, re-run rather than carried; **the control is `00328640` reappearing on `+0x710` and not `+0x714`** | 1 |
| `CS-5` — the field the dispatch reads | [the handler-table contract](CONTRACT-battle-action-handler-table.md) `HT-3`, measured the same day — cited by contract, not re-derived here | 1 |
| `CS-1`, `CS-3`, `CS-4` and the four funnel callers | [the seam page](Command-And-Action-Seam/native-command-seam.md) §2 and its settled `E-5`, 2026-09-12 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `CS-1` through `CS-6`. **`CS-3` is the one a port
merges**: two rings with identical layout invite one generic queue, and that makes a presentation
notification able to select an action. **`CS-2` is the one a port loosens** — letting any subsystem
write `+0x714` costs nothing until `CS-5`'s dispatch reads it.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CombatAction — internal.** The seam, the funnel, the two rings and the commit fields are this
  category's own.
- **CombatFormula — SERVICE.** The `BattleStats` identities the seam takes belong to that layer;
  **`CS-1` asserts only that the seam receives them already resolved**, which is a property of its
  signature and its two callers.
- **Presentation — SERVICE, through `CS-4`.** The presentation-slot readiness test that gates the
  only producer is that layer's; this contract asserts **that the enqueue is gated on it**, not what
  readiness means.
- **ActorEntity, Gameplay and Party — MECHANICAL, through the FUNNEL's own callees.** `0030F760`
  is cited because it is this contract's subject and `CS-2` is a statement about what it writes;
  **`CS-2` is a WRITER census over three fields, settled before any of those callees runs**, and
  none of their bodies is read here.
- **Every other layer reached is MECHANICAL**, through these two bodies' own callees. *Only the seam
  and the funnel are cited by address; the ring drains and the producer are named, because this
  contract reads their relationship and not their bodies.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun.

## 17. Related

- [The native command seam](Command-And-Action-Seam/native-command-seam.md) — the mechanism
- [Contract — the battle action handler table](CONTRACT-battle-action-handler-table.md) — `CS-5`
- [Contract — combo continuation](CONTRACT-combo-continuation.md) — one of the funnel's callers

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** CS-1 to CS-3 became checks that fail if the shipping image says otherwise. CS-2's writer census covers every listed
body. Script: `Tools/analysis-kit/gfz-scripts/falsify_command_seam.py`, output `falsify_command_seam.out`, image
`73461d08…`, 0 BROKEN. The ring-drain behaviour is the executed `s20-opus-replay-rings` result, and is not re-run.

| # | Clause attacked | Result |
|---|---|---|
| N0 | CS-1 one seam, two callers | **survives**: `00311CF0` is 283 B, called from `00311B20` and `003138D0` |
| N1 | CS-1 intent only; an ambiguous 0 | **survives**: it stores `+0xBA0` (word) and `+0xBB8` (dword), never `+0x708`/`+0x710`/`+0x714`; `test ecx, 0x8800203b` at `00311D72` is followed by `jne 00311DED`, the 0-returning exit |
| N2 | CS-2 | **survives**: among the `BattleUnit_*` bodies, the writers of `+0x714` are exactly `CommitAction`, `CancelAndResetCurrentAction` and `ResetStateForReuse`; the control `00328640` writes `+0x710` and not `+0x714` |
| N3 | CS-3 two rings | **survives**: `022BEDA0` is referenced by `0030FE60` and `00313DB0`, and `022BE980` by `0030FE60` and `00313CD0` |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE and CLIENT (6 edges).** The commit funnel `0030F760` calls `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850`; the by-focus-handles fan-out `00311B20` calls `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810`; the `talktreasure` chain `00328640` calls `ActorWork_GetBattleUnitRaw` `00263E30` and `ActorHandle_EncodeRegistryEntry` `003589B0`; and the defeat-condition check `00300FC0` calls the defeat-cleanup step `003138D0`. The seam's bodies use the actor layer's unit table, unit lookup and handle encoder (that encoder is what puts a target focus into `+0x710` for `00328640`, the CS-2 exception), and the one actor caller is the defeat check that runs the cleanup step, which issues command `0x113` through the seam `00311CF0`.

**Audio — SERVICE (1 edge).** The presentation-ring drain `00313DB0` ends by calling `002DEE70`, a 13-byte trampoline that jumps into the audio layer's sound-command dispatcher with the fixed arguments 0, 0 and -4. The drain makes that call once each time it takes a qualifying unit; what that selector does in the sound system is not read here, and CS-4 does not depend on it.

**CombatAI — CLIENT and SERVICE (3 edges).** `BattleUnit_SelectAndCommitNextAction` `00305AB0` and `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0` call the commit funnel `0030F760`, and the action-ring drain `00313CD0` calls `00305AB0`. The AI layer is where an action gets chosen: its selectors commit through the one funnel CS-2 names, and the pending-action ring hands each popped unit to that selector.

**Core — CLIENT (1 edge).** `002341C0`, the census's cross-subsystem reset orchestration, calls `BattleAction_ResetPendingQueueBanks` `0030FE60` first, then clears the navigation dataset, the perception cache and the world-pickup pool. The two CS-3 rings are emptied as one step of that battle-state reset.

**Gameplay — SERVICE (4 edges).** The funnel `0030F760` calls `BattleTargetBuffer_TryAppendActorWork` `00316CD0` and `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0`; the cleanup step `003138D0` and the presentation drain `00313DB0` call `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0`. These are ownerless combat helpers: the funnel resets and refills the target buffer with the resolved target when it installs an action, and both drains read the battle runtime mode (the cleanup step acts only in mode 1; the drain takes an extra lookup in mode 2).

**Input and InputGameplay — SERVICE (2 edges).** After it takes a unit, the presentation drain `00313DB0` calls the input layer's per-channel actor mask helper `00226BE0` (channel `0xA`, the unit's id) and then the capability / UI-request inhibit reconciliation `00313A00`. Draining a presentation-ready entry therefore re-derives which input channels and UI requests are allowed for that unit; the seam itself never reads raw input (CS-1).

**Movement — CLIENT (2 edges).** `00234520` calls the presentation drain `00313DB0` every call and, when the navigation dataset is present, the action drain `00313CD0`. It is the per-frame driver of both CS-3 rings (it also runs the party suppression recompute first), so the rings are drained on the movement side's schedule, the presentation ring unconditionally and the action ring only with navigation data.

**Party — SERVICE and CLIENT (6 edges).** `0030F760`, `00311B20`, `003138D0`, `00313CD0` and `00313DB0` all call `BattleUnit_ResolveByFocusHandle` `0031B7E0`, and the party stats reset support `00328BD0` calls the cleanup step `003138D0`. Every ring entry and every intent is a focus handle, and the party layer's resolver turns it into the battle unit the seam and the drains act on; the reset support is a second caller of the cleanup step.

**Presentation — SERVICE (1 edge).** The funnel `0030F760` calls `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30`, after the target-slot scan (named in the census as a party target-relation broadcast; its body is not read here). It runs at the end of commit and does not write `+0x708` / `+0x710` / `+0x714`, so it does not bear on CS-2.

**Status_Periodic_Terminal — CLIENT (1 edge).** `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls the cleanup step `003138D0`. The periodic maintenance tick is the third caller of that step, alongside the defeat check and the party reset support.

**UI — CLIENT (1 edge).** `BattleMenu_UpdateCommandSelectionAndDispatch` `002778C0` calls the fan-out `00311B20`. A command picked in the battle menu enters the seam through that fan-out, which is one of CS-1's two callers of `00311CF0`.

**WorldAreaField — SERVICE and CLIENT (6 edges).** `0030F760`, `00311B20`, `00311CF0`, `00313CD0` and `00313DB0` call `FieldData_GetActiveFieldRecordBit15` `00377C20`, and `BattleSystem_InitializeAreaState` `002342F0` calls `BattleAction_ResetPendingQueueBanks` `0030FE60`. The seam and the drains re-check a unit carrying one of the statuses the seam's status gate tests against the current area's action-permission bit (the seam's −2 exit is that gate), and area setup empties both rings.
