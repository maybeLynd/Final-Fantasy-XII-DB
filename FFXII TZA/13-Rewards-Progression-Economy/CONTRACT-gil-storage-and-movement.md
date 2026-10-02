---
contract: Move gil — one setter that clamps, meters and stores, and thirteen paths that inherit all three
category: 13-Rewards-Progression-Economy
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md
entries: ["00254EE0", "00253690", "00309BF0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the setter disassembled in full with **every one of its three delta branches
    traced to the store it reaches**, both clamp constants read at their instructions, and the
    callers of the setter and of BOTH getter entry points censused image-wide **with the thunk
    identified inside the body's own caller list**. **This records checks performed on that date,
    not the method of the original derivation**, which is on the gil page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-gil-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — gil storage and movement

> **Authored 2026-09-22 by FABLE.** S-32's binding gap is *"EXP/LP division only, of 5 pages"*. The
> loot rolls and the chain were taken at `8cfdf3851`; **this takes the gil paths.** The death
> sequence and the level-up ~~remain uncontracted~~ have since been contracted *(answered: see CONTRACT-defeat-rewards-sequence.md and CONTRACT-level-advance-and-growth.md; 2026-10-02, OPUS)*, and this document does not claim them.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants, and **GL-1, GL-2 and GL-3 are properties the thirteen callers inherit without
> expressing** — none of them is visible from a call site.

## 1. Purpose

Change how much money the party has, from anywhere, without any caller having to know the rules.

## 2. Interface

| | body | note |
|---|---|---|
| **the setter** | `GameState_SetGil` (`00254EE0`), **72 B** | **13 callers, no thunk** — the whole census |
| the getter | `GameState_GetGil` (`00253690`) | 19 real callers **plus a second entry point** |
| the getter's thunk | `GameState_GetGil` (`00309BF0`) | 5 B, 3 further callers, **zero overlap** |

## 3. Types

```
game state   *(void**)0x02092758
  +0x08  i32  gil -- SIGNED, and clamped to [0, 0x05F5E0FF] on every write (GL-1)
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**GL-1 — The clamp lives in the SETTER, so all thirteen paths inherit it and none expresses it.**
`00254F07`–`00254F15`: `xor ecx, ecx` / `cmovns ecx, ebx` floors at zero, then `mov eax, 0x5f5e0ff`
/ `cmp` / `cmovg` caps at **99,999,999**. *So a caller that computes a negative balance silently
gets zero rather than failing, and no caller can exceed the ceiling however it arrives.*

**GL-2 — Every change is METERED as a side effect of the write, and the debug path is not
exempt.** Before storing, the setter calls `00316A50` — owned by `PlatformOnlineAchievements` — with
kind **6 for a gain** and **7 for a spend**, by *absolute* delta (`00254EF8`, `00254F00`). **The
developer console's `Debug_SetGilToMaximum` is one of the thirteen ordinary callers**, so it moves
the same counters a player's gil would. *There is no unmetered way to change gil.*

**GL-3 — The delta is measured BEFORE the clamp, so the meter and the balance can disagree by
construction.** `00254EF1 sub edx, dword ptr [rax + 8]` runs on the raw argument; the clamp happens
fourteen instructions later. *A write of 200,000,000 records a "gained" delta far larger than the
gil actually stored, and nothing reconciles them afterwards.*

**GL-4 — A delta of ZERO is not metered at all.** The branch pair is `00254EF6 jle` then
`00254EFC jns`: a positive delta falls through to `cl = 6`, a negative one takes `jle` and fails
`jns` to reach `neg` / `cl = 7`, and **a zero delta takes `jle` and then takes `jns`, jumping past
the call to `00254F07`.** *So "every change is metered" is exact and not loose — setting gil to the
value it already holds records nothing, and still performs the store.*
**One edge: the metered delta is 32-bit and uses the UNCLAMPED request** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 347](../_index/candidates/s32-opus-replay-gil-storage/README.md), which executed it 8/8; `00254EE0` re-read whole.)*. `00254EF1 sub edx, [rax + 8]`
subtracts the balance from the requested value before the store clamps the request to `[0, 99,999,999]`
(`00254F07`–`00254F15`). So:
- a request that wraps is metered with the wrong sign. For −2,147,483,648 over a balance of 100, the difference is
  `+0x7FFFFF9C`: a **gain** of 2,147,483,548 (kind 6) is metered while 0 is stored;
- a request above the cap is metered in full, although only the cap is stored.

The meter's two counters are saturating dwords at `[020927C0] + 0x3848 + kind × 4` (`+0x3860` gains, `+0x3864`
losses), and they stop at `0x7FFFFFFF`. The branch reading above holds for every delta that does not wrap.

**GL-5 — Thirteen writers, twenty-two readers, and the reader count is only right if you notice the
second entry point.** The setter has **13 call sites in 13 functions and no thunk**. The getter has
**two entry points**: the body `00253690` and a 5-byte thunk `00309BF0` with **3 callers of its
own**, disjoint from the body's.

> **And the body's own census is a trap.** A caller sweep of `00253690` returns **20** — because
> **the thunk itself appears in that list**, reaching the body by `jmp`. The real figure is
> **19 + 3 = 22**, which is what the page records. *A census that counts the thunk as a consumer
> reports 23; one that misses the thunk's own callers reports 19. Both are wrong and both look
> well-formed.*

**GL-6 — Gil is an EXECUTION RESOURCE, spent in three phases.** Three of the thirteen writers are
`BattleAction_PrepareExecutionResources`, `BattleAction_ConsumeExecutionResources` and
`BattleAction_RefundReservedExecutionResources` — reserve, commit, give back. *So an action can take
gil and hand it back, and each of the three movements is separately clamped (GL-1) and separately
metered (GL-2) — a reserve-then-refund pair is invisible in the balance and visible twice in the
counters.*

## 5. State

**Owned:** the `i32` at game state `+0x08`. **Written elsewhere:** the statistics counters `00316A50`
maintains, which this subsystem updates but does not own.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-experience-and-licence-award.md`](CONTRACT-experience-and-licence-award.md) — S-32's first |
| **Sibling** | [`CONTRACT-loot-rolls-and-the-chain.md`](CONTRACT-loot-rolls-and-the-chain.md) — S-32's second |
| **Meters into** | `PlatformOnlineAchievements`' counters (GL-2) |
| ~~**Uncontracted**~~ **Contracted separately** | the death sequence and the level-up — S-32's other two pages, not claimed here *(answered: CONTRACT-defeat-rewards-sequence.md, CONTRACT-level-advance-and-growth.md; 2026-10-02, OPUS)* |

## 7. State transitions

*compute delta → meter it unless zero → floor → cap → store.* There is no other order and no other
path: the field has one writer.

## 8. Script · resource · event interactions

None directly. Gil-carrying inventory objects and shop commits are among the thirteen callers.

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- A negative result is stored as **zero**, silently (GL-1).
- A value above the ceiling is stored as the ceiling, while the meter records the unclamped delta
  (GL-3).
- Setting gil to its current value stores it and meters nothing (GL-4).

## 11. Observable behaviour

Money never goes negative and never passes 99,999,999, however it is gained — and the statistics
screen's totals are not derivable from the balance, because they count movements the clamp discarded.

## 12. Reproduction formula

Set gil to `-1` and assert the stored value is `0` (GL-1). Set it to `200,000,000` and assert the
stored value is `99,999,999` **while the meter received 200,000,000 minus the old balance** (GL-3).
Set it to the value it already holds and assert **no call to the meter** (GL-4). Census the setter
and assert **13**; census both getter entry points and assert **19 and 3**, having first removed the
thunk from the body's own list (GL-5).

## 13. Runtime validation

~~**None.** No experiment executes these bodies. S-32's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*~~ **Superseded
2026-09-25:** [OPUS block 347](../_index/candidates/s32-opus-replay-gil-storage/README.md) executed the setter, the getter and its thunk, and the console writer with the real meter
`00316A50` (GL-1 to GL-5, 8/8, identical three times). The evidence class is native replay, not live.

## 14. Unresolved

- ~~What `003F4AA0`, the one unnamed writer among the thirteen, does — [the page](gil-storage-clamp-and-every-path-that-moves-it.md)
  records it as not read and this contract does not read it either.~~ **Read 2026-09-22
  (SWE2-CONTRACT): it is a reward-bundle record applier.** `003F4AA0(rcx=record)` —
  `test byte [rcx],1` gates `SetGil(GetGil() + dword[record+4])` (`003F4AB5`–`003F4AC1`);
  then `[record+8]` counted items at `+0x0C`, stride 4, granted by
  `00300B80(id=entry[0], count=entry[2], 0)` (`003F4AE0`–`003F4AFB`); then `[record+0x0A]`
  single items at `+0x1C`, stride 2, granted by `00300B80(id, 1, 0)` (`003F4B02`–`003F4B2B`).
  Its sole feeder is `00290130` — fetch bundle `003F8C60`→`003F4C30` keyed by `(edx, r8d)`
  (`record+0x24` = second key), apply it, then post message `0x100` via `00244F50` with the
  key (`003F4BD0`). ~~**`00290130` is statically orphaned**: zero `call`/`jmp` edges, zero
  `lea`/immediate materialisations, zero qword slots in any data section, and the only
  RVA32 slot in the image is its own `.pdata` record — so the thirteenth writer's gil write
  is real but the bundle-claim entry is never invoked by any enumerated route. Residual: a
  route carried as something other than a code or data pointer is not enumerable and is not
  claimed.~~ **Corrected (2026-09-29, OPUS falsification pass 1, `CON-174`): `00290130` is reached through its 5-byte thunk `002E1A50` (`jmp 0x290130`), which is called at `00344C9A` in `FUN_00344C60`, the begin handler of script verb `037C questresultwindow`.**
  The census counted edges to `00290130` only, not to its thunk. So the thirteenth writer's gil write is reached from
  authored script: the quest-result window. The bundle keys are values the handler computes (`00267E10(r9)` and a
  popped integer, `00473C90`); what they select is not read here.
- ~~Whether any consumer reconciles the meter against the balance (GL-3).~~ **Closed
  2026-09-22 (SWE2-CONTRACT): no consumer does.** The meter `00316A50` writes two sinks: the
  per-kind "seen" bitmap at `gameState+0x3844` and the counter records behind singleton
  `*(01F84450)` via `008632B0` (kinds 6/7 → counter ids 8 / `0xA` at `00D10550`). The
  counter-object getter `0020CE00` has exactly three callers — `00863240`, `00863280`,
  `008632B0` — and the bodies calling that accessor family (`00315FDA`, `003162E0`,
  `00316440`, `00316A63`, `0034C9A0`, `00352250`) are disjoint from all ~~21~~ 22 *(corrected 2026-10-02, OPUS: 19 + 3, GL-5)* bodies calling
  `GameState_GetGil`/`00309BF0`: **no function both touches a counter accessor and reads the
  balance**, so no code path compares metered totals to `+0x08`. Residual: a reconciliation
  split across a queued message or stored intermediate is outside a per-body census; within
  every enumerable route, meter and balance can disagree permanently.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| GL-1, GL-3 — the clamp and its position | `00254EF1` against `00254F07`–`00254F15`, read in order, with both constants taken at their instructions | 1 |
| GL-4 — the zero-delta skip | `00254EF6` and `00254EFC` traced for all three sign cases to the store each reaches — the control is that the positive and negative cases *do* reach `00254F02` | 1 |
| GL-2 — the meter and the debug path | `00254EF8` / `00254F00` / `00254F02`; `Debug_SetGilToMaximum` present in the setter's caller census | 1 |
| GL-5 — 13, and 19 + 3 | all three entry points censused image-wide, **with `00309BF0` identified inside `00253690`'s own caller list** as the reason a naive body census reads 20 | 1 |
| GL-6 — the three-phase spend | the three `BattleAction_*` writers present in the same census | 1 |
| the thirteen callers' identities and `AI-8` | [the gil page](gil-storage-clamp-and-every-path-that-moves-it.md) §§4–5 | 1 |
| `003F4AA0` is a reward-bundle record applier; feeder `00290130` ~~is statically orphaned~~ **is reached from verb `037C questresultwindow` through the thunk `002E1A50` (`CON-174`; `falsify_gil.py` K1)** | `003F4AAA`–`003F4B3B` read whole; `00290130`–`0029016E` and `003F4C30`–`003F4DCA` read; route census over all `.pdata` bodies — zero call/jmp/lea/imm edges, zero data qword slots, sole RVA32 slot is its own `.pdata` record | 1 |
| GL-3 — no consumer reconciles meter against balance | `0020CE00` caller census = `00863240`/`00863280`/`008632B0` only; accessor-family callers `00315FDA`/`003162E0`/`00316440`/`00316A63`/`0034C9A0`/`00352250` disjoint from the ~~21~~ 22 *(corrected 2026-10-02, OPUS: 19 + 3, GL-5)* `GetGil`/thunk bodies | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on GL-1 through GL-6. **GL-3 is the one a port will
"fix"**: clamping before measuring the delta is the tidier order, it agrees with the original on
every ordinary transaction, and it silently changes the statistics totals on every one that hits a
bound.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Rewards_Progression_Economy — internal.** The storage, the setter and both getter entry points
  are this category's own.
- **PlatformOnlineAchievements — SERVICE, and GL-2 is the statement.** The meter belongs to that
  layer; this contract asserts **that the setter calls it on every non-zero delta and with which two
  kinds**, and nothing about what it then counts.
- **CombatAction — CLIENT, and GL-6 is the statement.** Three of the thirteen writers belong to that
  layer and form the reserve/commit/refund triple. *They are cited as callers, by name and not by
  address: their own behaviour is that layer's.*
- **Items_Equipment_Shops_License — CLIENT.** Four further writers — the two shop commits and the
  two gil-carrying inventory objects — belong to that layer, on the same terms.
- **CombatFormula — CLIENT, and it is the one caller that both reads and writes.**
  `BattleFormula_ApplyTargetResult` is among the thirteen writers *and* among the getter's readers,
  so an action's result on a target can consult the balance and then change it. **This contract
  asserts only that it appears in both censuses**; what it computes between the two is that layer's,
  and is not read here.
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by any stray noun.

## 17. Related

- [Gil storage, the clamp and every path that moves it](gil-storage-clamp-and-every-path-that-moves-it.md) — the mechanism
- [Contract — experience and licence award](CONTRACT-experience-and-licence-award.md) — S-32's first
- [Contract — loot rolls and the chain](CONTRACT-loot-rolls-and-the-chain.md) — S-32's second

## Falsification pass 1 — 2026-09-29 (OPUS): the setter survives; the thirteenth writer is not orphaned

**Attack.** GL-1 to GL-6, §2's sizes and §14's two closures became checks. Every census ran twice, bounded by the
function list and as a raw E8/E9 sweep of `.text`, and the two agree. Script:
`Tools/analysis-kit/gfz-scripts/falsify_gil.py`, output `falsify_gil.out`, image `73461d08…`, 0 BROKEN. The behaviour is
OPUS block 347's execution and is not repeated.

| # | Clause attacked | Result |
|---|---|---|
| N0 | §2 | **survives**: 72 / 11 / 5 B; the thunk is `jmp 0x253690` |
| N1 | GL-1 | **survives**: floor with `cmovns`, cap `0x5F5E0FF` with `cmovg`, then the store |
| N2 | GL-2, GL-4 | **survives**: gain `cl = 6`, spend `neg` / `cl = 7`; zero takes `jle` then `jns` past the call |
| N3 | GL-3 | **survives**: `sub edx, [rax+8]` on the raw argument, before the clamp |
| N4 | GL-5, GL-6, §16a | **survives**: 13 setter callers (12 calls plus `Debug_SetGilToMaximum`'s tail-jump); 19 + 3 getter callers (the thunk's 3 are 2 calls plus a tail-jump), disjoint; the three `BattleAction_*` writers; `BattleFormula_ApplyTargetResult` in both |
| N5 | §14: `003F4AA0` | **survives**: gated on `[rcx]` bit 0, reads and sets gil |
| K1 | §14: "`00290130` is statically orphaned" | **refuted** (`CON-174`): the thunk `002E1A50` jumps to it, and the thunk is called at `00344C9A` in `FUN_00344C60`, the begin handler of verb `037C questresultwindow` |

Corrected in place: §14 item 1 and its §15 row here, and the writer table, the §10 bullet and §13a on the gil page. The
consumer record is `_index/candidates/gil-falsification-pass-1-0929/`.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity — SERVICE (2 edges).** The script verb `0034C9A0` calls `0032F240`, a 32-byte lookup that returns a dword from an actor-indexed table when that actor's flag byte is set and −1 otherwise; the bundle fetch `003F4C30` calls `PackedActorHandle_IsClass8` `0030BAF0`. The verb turns an actor's table value into a counter id before it writes an achievement counter, and the bundle fetch builds a one-item bundle when its key is a class-8 packed handle; neither touches the balance at `+0x08`.

**CombatAction — CLIENT (8 edges).** `GameState_GetGil` `00253690` is called by `BattleAction_CheckExecutionResourceAvailability` `00303BD0`, `BattleAction_PrepareExecutionResources` `0030EF20`, `BattleAction_ConsumeExecutionResources` `00305640` and `BattleAction_RefundReservedExecutionResources` `00300280`, and `GameState_SetGil` `00254EE0` by the last three; `00305640` also calls `00316440`. This is GL-6's reserve/commit/refund triple plus the availability check reading the balance, and on commit the action layer also runs `00316440`, which fires achievement counter `0x13` once when bit 5 of the game-state byte `+0x3845` is set.

**CombatFormula — CLIENT (2 edges).** `BattleFormula_ApplyTargetResult` `003112F0` calls both `00253690` and `00254EE0`. It is the one writer that is also a getter reader (§16a): result slot 18 deducts `max(balance − value, 0)`.

**Gameplay — CLIENT (2 edges).** `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` `00316DF0` and `DefinitionRuntime_DeactivateAndRemoveConfiguredItems` `00323540` call `Inventory_GrantEncodedLootItem` `00300B80`. The definition runtime grants and removes its configured items through the same grant the reward-bundle applier uses; gil moves only when the encoded item is a gil-carrying object (§16a's two inventory writers).

**Items_Equipment_Shops_License — CLIENT and SERVICE (11 edges).** `00253690` and `00254EE0` are called by `InventoryBundleClass09_ApplyGilAndNestedItems` `002FD530`, `InventoryEncodedGilClass0E_ApplyGilDelta` `002FD880`, `Shop_CommitPurchaseItemAndGil` `002FEEB0` and `Shop_CommitSaleItemAndGil` `00310870`; `00300B80` calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0` and is called by `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` and by the applier `003F4AA0`. Four of the thirteen writers are that layer's shop commits and gil-carrying inventory objects, and the bundle applier grants its items through that layer's inventory write.

**PlatformOnlineAchievements — SERVICE and CLIENT (29 edges).** `00254EE0` calls `AchievementCounter_UpdateAndMaybeFire` `00316A50`, which calls `00315E90`, `003165C0`, `003166F0`, `00316BF0` and `008632B0`; the counter-object getter `0020CE00` is called only by the three accessors `00863240`, `00863280` and `008632B0`, which then call `0020CB50`, `0020CCA0` (a read of byte `+0x190` of the id's `0x198`-byte record) and `0020CE60` respectively; `00863280` and `008632B0` are also called by `003162E0` and `00316440`, and `003162E0` calls `003165C0` and is called by the re-check loop `00316930`; the verbs `0034C9A0` and `00352250` call `00863240` and `008632B0`, and the accessor `008632B0` is also called by `00315E90` and `00316A50`. The setter feeds the meter on every non-zero delta (GL-2), and the accessor family behind the singleton held at `01F84450` is the census GL-3 rests on — none of these bodies reads the balance.

**Script_VM_Native_Bridge — CLIENT and SERVICE (7 edges).** `0034C9A0`, `00352250` and the begin handler of verb `037C questresultwindow` `00344C60` call `VMValueStack_PopInt32CoerceFloat32` `00267E10`; `00344C60` calls `00473C90`; `0034C9A0` calls `00863240` and `00352250` calls `008632B0`; and the verb body `0050FAF0` calls `00300B80` on one arm (its other arm adds gil through `GameState_AddGilClampedAndNotify`). Script verbs pop their arguments from the VM stack and reach this contract's writers — the quest-result window through the thirteenth writer's thunk, `0050FAF0` through the add-and-notify wrapper or the item grant — and two more verbs write achievement counters directly.
