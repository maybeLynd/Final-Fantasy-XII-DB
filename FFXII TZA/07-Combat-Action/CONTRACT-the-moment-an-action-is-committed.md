---
contract: Commit an action onto a unit through two disjoint id ranges, and shadow the command block as it is written
category: 07-Combat-Action
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 07-Combat-Action/the-moment-an-action-is-committed.md
entries: ["0030F760", "003105D0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants read from the
    shipping bytes — **both range tests taken at their instructions**, the target-buffer path traced
    through its unresolved arm, and the shadow copy's two stores located. **This records checks
    performed on that date, not the method of the original derivation**, which is on the commit page;
    see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-commit-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the moment an action is committed

> **Authored 2026-09-22 by FABLE.** S-20's binding gap is *"2 contracts over 4 pages"*. **This takes
> the fourth, so all four of S-20's named pages now carry a contract that declares them.**
>
> Written against FRONTIER's adequacy test. **`CM-2` and `CM-3` are the reason this is not
> operation-scoped:** the function accepts two disjoint id ranges that do *different work*, and which
> range an id falls in decides whether a second structure is touched at all.

## 1. Purpose

Put a decided action onto a unit, and leave a record of what it was told to do.

## 2. Interface

```c
int BattleUnit_CommitAction(BattleUnit *unit, void *actionData,
                            uint16 actionId, uint32 targetId, int alsoPrepare)
```

`003105D0 BattleUnit_CancelAndResetCurrentAction` is the block's other writer and runs first when
`alsoPrepare` is non-zero.

## 3. Types

```
battle unit
  +0x6B4          u8     phase, zeroed by the commit
  +0x700          u32    flags; the low TWO bits are cleared
  +0x708          ptr    actionData
  +0x710          u32    targetId
  +0x714          u16    actionId
  +0x718 .. +0x72F       a verbatim copy of +0x700 .. +0x717   (CM-5)
  +0x778          BattleTargetBuffer, 0x208 bytes              (CM-3)
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**CM-1 — A target that does not resolve is NOT an error.** `targetId` is decoded through
`BattleUnit_ResolveByFocusHandle` at `0030F791`; a null result skips the broadcast and enmity steps
and **does not refuse the commit**. *So a committed action can carry a target id whose unit no longer
exists, and everything downstream must tolerate it.*

**CM-2 — TWO disjoint accepted id ranges, and the second is EXACTLY the handler table's window.**
`0030F798` loads `0x21E`; `0030F7A1 cmp di, r13w` / `ja` sends anything above it to a second test:
`0030F7D9`–`0030F7EC` computes `ax = actionId − 0x4000` as a **16-bit subtraction** and refuses when
`ax > 0x166`.

> **That is the same index and the same bound the action dispatch uses** —
> [the handler-table contract](CONTRACT-battle-action-handler-table.md)'s `HT-1`, `id − 0x4000`
> bounded at `0x166`, 359 ids. *The commit and the dispatch agree on the order id space instruction
> for instruction, which is what makes the second range an order rather than an action.* **Note the
> form**: it is a `sub` and an unsigned compare, not the equivalent `+0xC000` the page describes —
> the same arithmetic, and worth citing as shipped.

**CM-3 — ONLY the low range touches the target buffer, so the two ranges are not interchangeable.**
Ids `≤ 0x21E` take `0030F7A7`–`0030F7CD`: the `0x208`-byte buffer at `+0x778` is reset **preserving
its flag bit 0**, then an entry is appended. **The high range jumps straight to the command block**
(`0030F7D7`/fallthrough to `0030F7F2`) and never touches `+0x778`. *An order therefore commits
without disturbing the target buffer the previous action left there.*

**CM-4 — On the low path the buffer is appended to EVEN WHEN THE TARGET DID NOT RESOLVE — as a null
entry.** `0030F7B8 test r15, r15` / `je` selects between `[r15 + 0x10]`, the resolved `ActorWork*`,
and `rsi`, which was zeroed at `0030F796`. **Both arms fall into the same
`BattleTargetBuffer_TryAppendActorWork`.** *So "resolve failed" is not "append skipped": the buffer
receives a null first qword and its count advances, which is a different post-state from an
untouched buffer and the one a reimplementation is most likely to get wrong.*

**CM-5 — The command block is SHADOWED as it is written, unconditionally, and this function never
reads the shadow.** After the six fields are stored, `+0x700`–`+0x70F` is copied by `movups` to
`+0x718` and `+0x710`–`+0x717` by `movsd` to `+0x728`. *Nothing here reads it back, so what it is
for is not established by this body — but it is written **before anything can modify the live copy**,
which gives it the shape of "what the unit was told to do" kept beside "what it is doing now".* **The
cancel is what consumes it.**

**CM-6 — The cancel has two gates that make it a NO-OP rather than a reset.** A null unit, and a
unit with no stats record at `+0x698`, both return without touching anything. *So "cancel then
commit" is not a way to guarantee a clean block: on a unit without stats the cancel silently does
nothing and the commit writes over whatever was there.*

## 5. State

**Owned:** the command block and its shadow, and the embedded target buffer. **Read, not owned:** the
focus-handle space the target id is decoded through.

## 6. Relationships

| | |
|---|---|
| **Agrees with** | [`CONTRACT-battle-action-handler-table.md`](CONTRACT-battle-action-handler-table.md) — `CM-2` shares its index and bound |
| **Is the funnel of** | [`CONTRACT-native-command-seam.md`](CONTRACT-native-command-seam.md) — `CS-2` names this body as the only writer of the three fields |
| **Sibling** | [`CONTRACT-battle-target-buffer.md`](CONTRACT-battle-target-buffer.md) — the `+0x778` structure `CM-3` and `CM-4` touch |

## 7. State transitions

*optional cancel → resolve the target (may fail) → low range: reset and append the buffer; high
range: nothing → write six fields → copy them 24 bytes on → broadcast and enmity, only if the target
resolved.*

## 8. Script · resource · event interactions

Script commands arrive here as issued commands through the seam; the high id range carries AI orders.

## 9. Determinism

Deterministic. No generator is drawn in this body.

## 10. Failure paths and edge conditions

- An unresolvable target commits anyway, with the broadcast and enmity steps skipped (`CM-1`).
- An id in neither range is refused at `0030F7EC` (`CM-2`).
- A cancel on a unit with no stats record does nothing at all (`CM-6`).

## 11. Observable behaviour

None directly. This is the instant a decision becomes the unit's current action.

## 12. Reproduction formula

Commit with `actionId = 0x21E` and `0x21F` and assert the first takes the buffer path and the second
the range test (`CM-2`, `CM-3`). Commit an order id and assert `+0x778` is **untouched** (`CM-3`).
Commit a low id with an unresolvable target and assert the buffer's count advanced with a **null**
first qword (`CM-4`). Compare `+0x700`–`+0x717` against `+0x718`–`+0x72F` after any commit and assert
they are equal (`CM-5`). Cancel a unit whose `+0x698` is null and assert nothing changed (`CM-6`).

## 13. Runtime validation

**None by this contract.** [`EXP-043`](../_experiments/EXP-043-target-buffer-boundary.md) and
[`EXP-046`](../_experiments/EXP-046-target-buffer-reset.md) executed the buffer helpers and corrected
this page's earlier reading of them; **they are cited here as the source of `CM-3`'s reset/append
naming**, not as execution of the commit itself~~, which is unexecuted~~ *(answered: the commit is executed as shipped bytes under Unicorn, 1309 commands, 704 compared lines, 0 mismatches, and its nine callees by EXP-091 - CONTRACT-commit-action.md §13 and §13a; 2026-10-02, OPUS)*.

## 14. Unresolved

- ~~**What the shadow at `+0x718` is read by**, beyond the cancel. `CM-5` establishes it is written
  unconditionally and not read here.~~ **Resolved 2026-09-22 (SWE2-CONTRACT): the cancel is the
  ONLY decisional reader.** A per-body census of `+0x718`–`+0x72F` displacements over all 35,713
  `.pdata` bodies, filtered to bases that also touch unit markers (`+0x698` stats, `+0x778`
  buffer), leaves seven true unit bodies: the commit itself (`0030F7D9`, the verbatim copy of
  `CM-5`); three resets that stamp or clear it (`00236A60`, `0041F730`, `00615840`); `00308610`,
  which **writes** shadow flags bit 0 after the fact (`or dword [rbx+0x718], 1` at `00308762`,
  under the `00305AB0`/`00307BE0` predicate pair — a post-commit flag mutation, not a read); the
  unit serializer `00604750`, which copies it out verbatim with the rest of the record; and the
  cancel `003105EF` (`003106B9`/`003106CC`), the only body that reads shadow fields to make a
  decision. The other ~17 hits are non-unit structs sharing the displacement band — pointer
  records (`001CC55D`, `001D0390` handler-table init, `004200A0` destructor), float records
  (`003714A0`, `006FCB53`, the `007C*`/`007D*` families) and two stack slots — all decoded and
  rejected. **New finding:** `00236A60` stamps the live block into `+0x718` *and* `+0x730`
  (`+0x710` into `+0x728` *and* `+0x740`), so a second verbatim shadow exists at
  `+0x730`–`+0x747`; ~~its readers were not in this census's band and stay unenumerated.~~ its reader is the next commit, `0030F84E cmp di, word ptr [rbx + 0x744]` and `0030F857 cmp ebp, dword ptr [rbx + 0x740]` *(corrected 2026-10-02, OPUS: the cancel `003105D0` writes the cancelled record there and `BattleUnit_CommitAction` reads it; the-moment-an-action-is-committed.md, the cancellation section)*.
- ~~Whether any caller relies on the null-append of `CM-4` rather than merely tolerating it.~~
  **Resolved 2026-09-22 (SWE2-CONTRACT): exactly one relies — `002FFB60`'s count gate.** The
  `+0x77C` count / `+0x780` entry consumers on unit-typed bases: `002FFB60` tests `count > 0`
  at `002FFC3E` and only then re-resolves the stored `+0x710` targetId through `0031B7E0` and
  applies it via `002FFA60` — a deferred target retry that is reachable **because** the buffer
  is non-empty, and the `CM-4` null-append is exactly what makes it non-empty on a failed
  resolve. Every other consumer tolerates the null: `0030EC4E` iterates entries and skips each
  whose `0031B760` resolution yields zero (`0030EC68`–`0030EC76`); `00325260` tests each entry
  pointer before use (`003254E8`–`003254F4`); `0030C010` exits on `[+0x780] == 0` and also
  requires entry-0 flag `0x400` (`0030C03B`–`0030C04F`) — a null-only buffer is treated as
  empty; `003067C2`'s jump-table arm copies entries verbatim into a global array; `0030602B`
  evaluates entries through `0031B9A0`; the serializer copies the whole range.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `CM-2` — two ranges, the second `id − 0x4000 ≤ 0x166` | `0030F798`, `0030F7A1` and `0030F7D9`–`0030F7EC` read at the instructions; the bound compared against the dispatch's | 1 |
| `CM-3` — only the low range touches the buffer | `0030F7A7`–`0030F7CD` against the high range's jump to `0030F7F2` | 1 |
| `CM-4` — the null append | `0030F7B8`/`0030F7C3` traced: both arms reach the same append, with `rsi` zeroed at `0030F796` | 1 |
| `CM-5` — the shadow | the `movups`/`movsd` pair located after the six stores at `0030F7F2`–`0030F800` | 1 |
| `CM-1`, `CM-6` and the cancel's order of work | [the commit page](the-moment-an-action-is-committed.md), falsified 2026-09-03 and corrected 2026-09-11 | 1 |
| the `+0x718` shadow has no decisional reader beyond the cancel, and a second verbatim shadow exists at `+0x730`–`+0x747` | `+0x718`–`+0x72F` displacement census over all `.pdata` bodies filtered to unit-typed bases: 7 true unit bodies (commit, resets `00236A60`/`0041F730`/`00615840`, flag-writer `00308610`, serializer `00604750`, cancel `003105EF`); ~17 non-unit hits decoded and rejected; `00236A60` stamps live→`+0x730` at `00236B72`/`00236B95` | 1 (static) |
| exactly one consumer relies on the `CM-4` null-append: `002FFB60`'s `count > 0` gate | `002FFC3E` `cmp dword [rbx+0x77c], 0` gates the `0031B7E0`/`002FFA60` deferred target re-resolve; null-tolerating consumers `0030EC4E` (`0030EC68`–`0030EC76`), `00325260` (`003254E8`–`003254F4`), `0030C010` (`0030C03B`–`0030C04F`) read at the instructions | 1 (static) |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `CM-1` through `CM-6`. **`CM-4` is the one a port
gets wrong while looking more correct**: skipping the append when the target does not resolve is the
obvious guard and leaves the buffer in a different state. **`CM-3` is the one a port unifies** —
resetting the buffer for every commit is tidier and destroys an order's inherited target set.
**`CM-5` is the one a port drops**, because nothing in this function reads it.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CombatAction — internal.** The commit, the cancel, the command block and its shadow are this
  category's own.
- **ActorEntity — SERVICE.** The focus-handle decode that turns `targetId` into a unit belongs to
  that layer; **`CM-1` asserts only that a null result is tolerated**, which is visible at the
  branch, and nothing about how handles decode.
- **Party — SERVICE.** The stats record at `+0x698` that `CM-6`'s second gate tests is that
  category's; this contract asserts **that the gate tests it for null**, not what it contains.
- **Gameplay — SERVICE, and `CM-3`/`CM-4` are the statements.** The two target-buffer helpers
  belong to that layer. **This contract asserts the ORDER they are called in, that the reset
  preserves flag bit 0, and that BOTH arms of the resolve test reach the append** — all read at
  this body's own branches — and nothing about what the helpers do inside, which is
  [the target-buffer contract's](CONTRACT-battle-target-buffer.md) and `EXP-043`/`EXP-046`'s.
- **CombatAI, CombatFormula and Status_Periodic_Terminal — CLIENTS.** Bodies in those layers call
  the commit or the cancel. *They are the sources `CS-2` enumerates on the seam contract; none is
  cited by address here and none is read, because this contract is about what the callee does
  with what it is handed.*
- **Movement and WorldAreaField — MECHANICAL, through the cancel's release steps and one commit
  callee.** *`CM-6` asserts only the cancel's two RETURN gates, which precede every one of them.*
- **Every other layer reached is MECHANICAL**, through these two bodies' own callees — the
  broadcast, enmity and presentation-slot steps among them. *Their addresses are deliberately not
  cited: each is a hub, and `CM-1` already states the only thing this contract needs about them,
  which is that the target-resolve failure skips two of them.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Party" would otherwise be cleared by the word alone.*

## 17. Related

- [The moment an action is committed](the-moment-an-action-is-committed.md) — the mechanism
- [Contract — the battle action handler table](CONTRACT-battle-action-handler-table.md) — `CM-2`'s other half
- [Contract — the native command seam](CONTRACT-native-command-seam.md) — the funnel this body is

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** CM-1 to CM-6 became checks that fail if the shipping image says otherwise. Script:
`Tools/analysis-kit/gfz-scripts/falsify_commit.py`, output `falsify_commit.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| M1 | CM-1 | **survives**: the target resolves through `0031B7E0` at `0030F791`; the result is kept in `r15` and nothing returns on null |
| M2 | CM-2 | **survives**: `≤ 0x21E`, or `sub ax, cx` (`0x4000`) then `cmp ax, cx` (`0x166`) / `ja` - 16-bit, unsigned |
| M3 | CM-3 / CM-4 | **survives**: the low range resets `+0x778` (`00316CF0`) and appends `[r15+0x10]` or the zeroed `rsi` (`00316CD0`); the high range goes straight to `0030F7F2` |
| M4 | CM-5 and §3 | **survives**: `+0x700 &= ~3`, the three fields, `+0x6B4 = 0`, then the `movups` / `movsd` shadow copy to `+0x718` / `+0x728`; the commit never reads the shadow |
| M5 | CM-5 "the cancel consumes it" | **survives**: `003105D0` reads `+0x718` and `+0x728` |
| M6 | CM-6 | **survives**: a null unit and a null `+0x698` both exit before any write |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Several subjects below are cited in section 14 only as census hits; their paragraphs say so.*

**ActorEntity — SERVICE and CLIENT (36 edges).** The commit `0030F760` and the cancel `003105D0` call `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850`; the cancel is called by `BattleUnit_ResetStateForReuse` `00236A60`, `BattleUnit_TeardownAndDespawn` `00300E40`, the defeat-condition check `00300FC0` and `BattleGroup_RefreshFourActorDefinitions` `003266C0`; `00236A60` is called by `BattleUnit_ApplyUnitDefinition` `0023A570`; `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` calls the combat frame `00308610`; `BattleUnit_ResolveByFocusHandle` `0031B7E0` calls `ActorWork_GetBattleUnitRaw` `00263E30` and `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0`; `0031B9A0` calls `ActorRuntime_GetClassNibble` `00263C20`; the timeline handler `00325260` calls `00263E30`, `0026A430` and `ActorHandle_EncodeRegistryEntry` `003589B0`; and the getter `ActorWork_GetBattleUnit` `0031B760` wraps `00263E30` and is called by 19 actor bodies (the ActorEntity ones among its 61 direct callers; FABLE, 2026-10-03), among them `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0`, `ActorWork_HasAppliedUnitDefinition` `00237650` and `BattleUnit_SetRuntimeUnitCategoryMode` `002396B0`. The actor layer owns the unit table, the handle decode that CM-1 tolerates failing, and the unit lifecycle that runs the cancel (reuse, teardown, defeat, group refresh); the 19 callers of `0031B760` use the same actor-work-to-unit getter for their own lifecycle work.

**CombatAI — CLIENT and SERVICE (19 edges).** `BattleUnit_SelectAndCommitNextAction` `00305AB0` and `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0` call the commit `0030F760`; the combat frame `00308610` (filed to the AI layer) calls `00305AB0`, the interrupt check `002FFB60`, `BattleUnit_AdvanceActionState` `00307BE0` and the cancel `003105D0`, and `00305AB0` calls `00305CC0`. The AI target builders `AiOrder_EvaluateAndResolveActionTarget` `003014C0`, `AiOrder_EvaluateTargetSelector` `00301AD0`, `AiOrder_SelectFinalTargetFromCandidates` `003087E0` and `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` `0030F130` call the target-buffer helpers `00316CF0` / `00316CD0` and the getter `0031B760`, as does `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` `00239040`, and `00301AD0` calls `0031B7E0`. The AI layer is the commit's main client (it chooses and commits the action, and its frame writes the shadow's bit 0 after the fact, as section 14 records); the target builders use the same buffer helpers and getters when they build candidate target buffers, which is outside the commit's own invariants.

**CombatFormula — CLIENT (1 edge).** `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` calls the cancel `003105D0`. A stats rebuild can cancel the unit's current action; CM-6 still applies, so on a unit without a stats record that call does nothing.

**Gameplay — SERVICE and CLIENT (13 edges).** The commit `0030F760` calls `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0` and `BattleTargetBuffer_TryAppendActorWork` `00316CD0` (the CM-3 / CM-4 pair) and the cancel calls `00316CF0`; the combat frame `00308610` calls `BattleUnit_DispatchActorPresentationEvent` `003299B0`; the timeline handler `00325260` calls the reaction timeline applicator `003257D0`. In the other direction the target-focus geometry runtime `0031ADB0` calls `0030C010`; `0031ADB0`, `BattleUnit_HasCurrentFocusEngagementEvidence` `0030BB30`, `00312B40` and `BattleAction_FindApproachGeometryAroundTarget` `00339630` call `0031B7E0`; `BattleUnit_HasRelationshipClass2PlusInTrackedActorList` `0030B050`, `WorldActor_HasActiveBattleActionOrUnitFlag14` `0030BA30` and `WorldActor_QueryCombatStanceState` `0030BFB0` call `0031B760`. Gameplay is the census's label for ownerless combat helpers: the commit relies on the two buffer helpers exactly as CM-3 / CM-4 state, and the other callers use the same resolvers for targeting geometry and stance queries.

**Movement — SERVICE and CLIENT (11 edges).** The cancel `003105D0` calls `BattleLocomotion_ResetPathAndSetTargets` `003291B0` and `0033C9B0`; `00236A60` calls `003839C0` and `Navigation_ResetPathPredecessors` `003839F0`; the combat frame `00308610` calls the locomotion-step publisher `0033A240`; the timeline handler `00325260` calls `0033CB10`; `00239210` calls `0031B760`; `BattleLocomotion_DecodeOrderGoal` `00312730`, `BattleLocomotion_BuildSolverContext` `00336710`, `00337A50` and `BattleLocomotion_ResolveTargetSpacingAndAvoidance` `00338140` call `0031B7E0`. Cancelling or reusing a unit releases its locomotion path, which is why the cancel and the reset reach the movement layer; the locomotion solvers resolve the committed `+0x710` target through the same focus-handle resolver.

**Party — SERVICE and CLIENT (5 edges).** `0031B7E0`, the focus-handle resolver the commit decodes `targetId` with, is filed to the party layer; the interrupt check `002FFB60`, `0030C010` and the commit `0030F760` call it. The combat frame `00308610` calls `BattleUnit_UpdatePartyCombatStanceState` `00307DF0`, and `0030BEB0` calls the getter `0031B760`. The party layer supplies the resolver whose null result CM-1 tolerates, and it updates stance from the same frame; `0030BEB0` is a party body using the shared getter.

**Presentation — OUT-OF-SCOPE and SERVICE (17 edges).** `001D0390` (the debug-menu handler-table init; it calls the menu renderer `001CD0E0` and is called by the menu singleton builder `001CCB20`), `AddMotion_ApplyBonePose` `003714A0` (it calls `Matrix4x4f_BuildEulerRotation` `0046D380` and `004776D0` and is called by `Skeleton_ComposeFinalPose` `00373860`), `CharacterRenderRecord_ResetDefaults` `0041F730` (calls `003E5D00`; called by `004200A0`, `CharacterRenderSystem_Initialize` `004269A0`, `004279B0` and `00429140`) and `CharacterRenderRecord_TeardownAndReset` `004200A0` (calls `003AEF30`, `003E69A0`, `0041E860`, `0041F730` and `00512C80`; called by `00427C90`) are cited only in section 14's `+0x718` displacement census: `001D0390`, `003714A0` and `004200A0` as hits decoded and rejected because they are other structures at that offset, `0041F730` as one of the three resets that stamp or clear the shadow. Their render, skeleton and debug-menu neighbours are outside this contract. The one live crossing is the commit `0030F760` calling `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30`, one of the broadcast steps CM-1 says a failed resolve skips.

**Resource — OUT-OF-SCOPE (1 edge).** `AddMotion_ApplyBonePose` `003714A0` calls `ResourceTable_ResolveEntryBySignedIndex16` `004780B0`. `003714A0` is on this page only as a rejected float-record hit of the section-14 census; its resource lookup has nothing to do with the command block.

**Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (1 edge).** `005102D0`, the native end of the `btlAtelCanselInitialSpawnFlag` verb, calls the getter `0031B760` to reach the unit whose flag bit 45 it sets. It is a script consumer of the shared getter, not a writer or reader of the command block.

**Spawn_Encounter_Lifecycle — CLIENT, OUT-OF-SCOPE (24 edges).** The getter `ActorWork_GetBattleUnit` `0031B760` is called by 24 spawn bodies, among them `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0`, `Spawn_SelectAndPrepareAutomaticEntry` `00235720`, `SpawnEntry_GetDeathCount` `00235F50`, `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` and `Spawn_ApplyScriptSelectedUnit` `0023A3B0`. The page cites `0031B760` only as the resolution a null-tolerating buffer consumer uses; the spawn layer uses the same getter to reach each spawned unit's battle record for its own entry and lifecycle bookkeeping.

**Status_Periodic_Terminal — CLIENT and SERVICE (3 edges).** `BattleUnit_ResetActionControlForStatusTransition` `00300140` and `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` call the cancel `003105D0`, and `00236A60` calls `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450`. A status transition that takes away action, or recovery from a terminal set, cancels the current action through the same two-gated cancel; the reset clears the status layer's resource accumulator when a unit is reused.

**UI — CLIENT (1 edge).** `BattleMenu_BuildCommandEntryList` `0031EB20` calls `BattleUnit_ResolveByFocusHandle` `0031B7E0`. The battle menu resolves focus handles with the same resolver when it builds its command list; it does not touch the command block.

**WorldAreaField — SERVICE (6 edges).** The eligibility test `002FFA60`, `00305AB0`, `0030C010`, the commit `0030F760` and `003714A0` call `FieldData_GetActiveFieldRecordBit15` `00377C20`, and the timeline handler `00325260` calls its five-byte thunk `00313F60`. Each asks the current area's record whether its action-permission override is set; the commit's own call belongs to the steps after the command block is written, not to CM-1 … CM-6.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-the-moment-an-action-is-committ-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003AEF30` | 29 B | stores dword 0 at `[rcx]`, then follows the chain from qword `+0x18` through each node's qword `+0x48` until null, storing byte 0 at the first byte of every node | `003AEF34`, `003AEF3D`, `003AEF40`, `003AEF43`, `003AEF4A` |
| `003E69A0` | 50 B | when dword `+0x448` of `rcx` is non-zero calls the callee at `003E69A0` + 0x13 with it in `ecx`; then, when dword `+0x44C` is non-zero, tail-jumps the same callee (`003E69A0` + 0x27) with it in `ecx`, else returns | `003E69A9`, `003E69B3`, `003E69B8`, `003E69C7` |
