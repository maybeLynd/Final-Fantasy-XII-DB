---
system: Native command / action seam
category: 07-Combat-Action
status: DOCUMENTED
owner_layer: PrimaryOwner:CombatAction
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 2
---

# Native command / action seam

> Where a command actually enters the engine - and three nearby mechanisms that look like
> that entry point but are not. One of them was wrong in this project's own notes and had to
> be withdrawn.

## 1. What the player sees

Choosing Attack from the Battle Menu, a Gambit firing, an enemy deciding to act. All of them
have to become "this unit is doing this thing to that target" somewhere in native code.

## 2. Native mechanism

### The real command seam

`00311CF0` `BattleUnit_IssueCommand` (283 B), with two wrappers:

| Address | Working name | Body |
|---|---|---:|
| `00311CD0` | `BattleUnit_IssueCommandByFocusHandles` | 26 B |
| `00311B20` | `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout` | 426 B |

These take **receiver-local focus / BattleStats identities**. Downstream, native target-set
selection, availability, reservation, action commit, timeline and presentation all proceed
naturally.

### What is NOT the seam

**`00313DB0`** (360 B) - takes **no BattleUnit argument**. It drains a 64-entry ring of packed
BattleUnit IDs:

```
022BEDA0  u8   read index
022BEDA1  u8   write index
022BEDA4  ...  64-entry data bank
```

It consumes the next queued ID, advances read index mod 64, resolves the unit, applies state
changes, publishes `02089350`, runs downstream services, and calls `00313A00`. Its clear path
clears `02089350` and tail-jumps to `00313A00`.

The ring's only producer is at `00304E5C`, inside `00304850`
`BattleUnit_AdvanceStandardActionState` (2,034 B) - a **13-phase post-commit** pipeline. The
enqueue happens only when `0030CA80` reports the presentation slot ready.

So the ring is a **presentation-ready / action-lifecycle notification ring**, not command
intent. Calling `00313DB0` manually would just consume whatever local queue state happens to
exist.

**`00313CD0`** `BattleUnit_ProcessPendingActionSelectionQueue` (220 B) - a *different*
pending action-selection ring at `022BE980`, drained **up to 8 entries per call**. It is a
**64-entry** ring, not an 8-entry one - see the correction in section 7. Structurally it is a
**twin** of the presentation ring: same paired byte indices, same 8-byte stride, same mod-64
advance~~, same resolve-then-act loop~~ *(corrected 2026-10-02, OPUS: the drains differ - `00313CD0` pops eight entries whatever they resolve to (`00313CF7 mov edi, 8`, `00313D31 je 00313D8E`), `00313DB0` stops at the first entry that does not resolve (`00313E11 je 00313EAC`); CONTRACT-native-command-seam.md CS-3)*. That is exactly why the two are easy to confuse, and why
they must not be merged: identical shape, different transaction.

**`0030F760`** `BattleUnit_CommitAction` - a genuine lower commit owner (installs order/action
context at `+0x708`, target focus `+0x710`, action ID `+0x714`, phase reset `+0x6B4`), but
current evidence does **not** establish it as a universal human/Gambit/AI/guest/script funnel.

> **E-5 settled 2026-09-12 (FABLE) — both halves are true, and they are different claims.** As the
> *commit* of a unit's action state it **is** universal: a whole-image writer census of unit
> `+0x700`–`+0x717` finds the order context `+0x708`, target focus `+0x710` and action id `+0x714`
> written only by `BattleUnit_CommitAction` (`0030F7F9`–`0030F806`), the cancel
> `BattleUnit_CancelAndResetCurrentAction` and the reuse reset `BattleUnit_ResetStateForReuse`; the
> only other touches are `Battle_ProcessActionTargetEntry` raising `+0x700` bit 1 and `00328640`
> (the `talktreasure` verb's chain, `0x02BF` → `00355E20` → `00355830` → `00269090`) writing a target
> focus **without** an action. Its four callers carry every source: `BattleUnit_SelectAndCommitNextAction`
> (from `BattleUnit_UpdateCombatFrame` and the pending-selection queue) commits the **issued command**
> — `+0xBA0` id and `+0xBB8` handle, the words `BattleUnit_IssueCommand` writes for human, guest and
> script commands (`00305AE4`–`00305B2F`) — and otherwise the **gambit / AI order sets** `+0x6F8` and
> `+0x6F0` through `BattleUnit_TrySelectAndCommitAiOrderFromSet` (`00305BA5`–`00305C9B`);
> `BattleAction_TryContinueComboSequence` commits the combo continuation; and
> `BattleUnit_TryCommitEngageAutoAttack` (from the reaction-animation event) the engage auto-attack.
> As the *intent seam* it is **not** universal — that is `BattleUnit_IssueCommand`, whose two callers
> are the by-focus-handles fan-out and the defeat-cleanup step `003138D0` — and it takes resolved
> inputs, exactly as the paragraph above and §"Confirmed" say. So: one commit funnel, one intent seam.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00311CF0` | `BattleUnit_IssueCommand` | 283 B | **the seam** |
| `00311CD0` | by-focus-handles wrapper | 26 B | |
| `00311B20` | by-focus-handles + party fanout | 426 B | |
| `0030F760` | `BattleUnit_CommitAction` | - | lower commit owner |
| `00304850` | `BattleUnit_AdvanceStandardActionState` | 2,034 B | 13-phase post-commit |
| `00313DB0` | presentation-ready ring consumer | 360 B | **not** a command API |
| `00313CD0` | pending action-selection queue drain | 220 B | separate 64-entry ring at `022BE980`; drains <=8 per call |
| `0030CA80` | `BattleAction_CheckPresentationSlotReady` | - | gates the enqueue |
| `0030C970` / `0030CF40` / `0030CFB0` / `0030D070` | presentation slot release / reset / acquire / allocate | - | slot pool |

## 4. Data structures

Two rings of identical shape, different purpose:

```
PRESENTATION-READY RING            PENDING ACTION-SELECTION RING
022BEDA0  u8   read index          022BE980  u8   read index
022BEDA1  u8   write index         022BE981  u8   write index
022BEDA4  64 x 8B packed IDs       022BE984  64 x 8B packed IDs
  consumer 00313DB0                  consumer 00313CD0
  ~~drains until empty~~              drains <= 8 per call
  stops at the first unresolved      unresolved entries still count
  entry (00313E11 -> exit)           toward the 8 (00313D31 -> 00313D8E)
                                     (corrected 2026-09-26, CONTRACT CS-3)
  advance: (read + 1) & 0x3F         advance: (read + 1) & 0x3F
  empty test: read == write          empty test: read == write

02089350  ptr   CombatAction current-selected BattleUnit

BattleUnit
  +0x6B4  action phase
  +0x708  order/action context
  +0x710  target focus
  +0x714  action ID
```

## 5. Call chain

```
COMMAND AUTHORITY
  stable command intent
    -> resolve to receiver-local focus / BattleStats identity
       -> 00311CF0 BattleUnit_IssueCommand  (or a wrapper)
          -> native target selection / availability / reservation
             -> 0030F760 BattleUnit_CommitAction  (where flow reaches it)   # <- corrected 2026-10-02, OPUS - the seam does not reach the commit; 00311CF0 records +0xBA0 / +0xBB8 only (00311D7A, 00311DB0), and BattleUnit_SelectAndCommitNextAction commits the issued command later (00305AE4-00305B2F); CONTRACT-native-command-seam.md CS-1
                -> 00304850 BattleUnit_AdvanceStandardActionState

PRESENTATION / CURRENT-UNIT SIDE TRANSACTION  (separate!)
  00304850
    -> acquire / wait presentation slot
       -> 0030CA80 ready?
          -> enqueue packed ID into 64-entry ring @ 022BEDA4
             -> 00313DB0 consumes ring
                -> publishes 02089350
                   -> 00313A00 rebuilds capability/UI policy
```

These are **related but not interchangeable authority seams.**

## 6. Modding notes

- **Best intervention point:** the `BattleUnit_IssueCommand` family.
- **Do not:** write `02089350` directly; insert IDs into the ring; call `00313DB0` as a
  command substitute; write `+0x708`/`+0x710`/`+0x714` by hand; or call `00313A00` to repair
  the consequences of a lower-level write.
- **`00313DB0` is useful for observation** - it tells you when the current unit changed and
  why UI eligibility moved. It is a good telemetry point and a bad API.
- **XIIOnline stable identity rule:** process-local pointers, BattleUnit handles, focus
  handles, BattleStats slots and UI actor handles are **not** wire identities. Carry stable
  logical/network identity, translate to the receiver's local native identity, *then* enter
  the seam.

## 7. What is not known

- [x] ~~Whether `BattleUnit_CommitAction` is a universal command funnel (open question **E-5**).~~
      **Settled 2026-09-12:** universal as the *commit* of the action state (the only writer of
      `+0x708` / `+0x710` / `+0x714` besides cancel and reset; four callers carry the issued
      command, the order sets, the combo and the engage auto-attack), not as the *intent seam*,
      which is `BattleUnit_IssueCommand` (§2).
- [x] ~~**UQ-108.** The full 13-phase breakdown of `00304850`.~~ **Answered 2026-09-14 (FABLE).**
      The phase is the unit's byte `+0x6B4`. The function loads `rsi = unit + 0x6B0` at entry (`0030487F`) and
      dispatches on `byte [rsi + 4]` through a 13-entry jump table (`0030493C`–`0030495A`, table at image
      `0x305044`); any value above 12 returns `-1`. Each arm ends in `inc byte [rsi + 4]` and **falls through into the
      next arm on the same call**, unless it has to wait. So one call can run several phases, and a waiting phase
      returns `0` and is re-entered on the next call. There are 16 `inc` sites.

      | phase | table target | what the arm does | leaves when |
      |---:|---|---|---|
      | 0 | `0030495C` | `BattleAction_PrepareExecutionResources`; clears unit flag bits; stores a limit into `+0x764` (`[rsi+0xB4]`); resolves and caches the effective action id | at once → 1 |
      | 1 | `003049FA` | dispatches the phase's presentation event; adds a step to `+0x760` while it is below `+0x764` | limit reached → **3** (two `inc`, `00304A46`/`00304A49`) |
      | 2 | `00304A49` | only the second of those two `inc`, an entry point for callers that store `2` | at once → 3 |
      | 3 | `00304A4C` | action setup: a status change, `BattleAction_ComputeEffectiveRangeBands`, `BattleAction_ComputeChargeLimitTicks`, a locomotion reset, and the release of the unit's three presentation slots (`+0x694`–`+0x696` set to `0xFF`) | at once → 4 |
      | 4 | `00304BA5` | approach: event, approach geometry around the target, `BattleLocomotion_SetApproachAndReferenceTargets`, `BattleAction_ComputeChargeProgressStep`, `BattleUnit_UpdateCombatNavigationStep` | arrived (`00304D70`) → 5; otherwise returns |
      | 5 | `00304D73` | arrival: event, locomotion reset | at once → 6 |
      | 6 | `00304DA5` | event; clears flag bits; acquires the presentation slot (`BattleAction_AcquirePresentationSlot`) | at once → 7 |
      | 7 | `00304E2C` | `BattleAction_CheckPresentationSlotReady` (UQ-109, UQ-110); queues the unit into the shown-unit ring on *should play* | ready **and** unit bit 12 (queued) clear → 8 |
      | 8 | `00304EB3` | one call on the `+0x6B0` block | at once → 9 |
      | 9 | `00304EBE` | execution: `Battle_BuildActionTargetSet`, sets unit bit 46, `BattleAction_EvaluateTargetPreviews`; then, for an action whose definition `+0x0C` has bit 30, `BattleAction_ConsumeExecutionResources` and `BattleAction_UpdateSpecialPresentationSequence`, otherwise `BattleAction_DispatchResolvedPresentationEvent` | at once → 10 |
      | 10 | `00304F62` | bit-30 actions wait while the special-sequence mode `022C2160` is 5 or 6; the others clear bit 46 (only once `animationEventFlags` `+0x690` holds bits 1 and 3, `00304F91`–`00304FA9`; the bit-30 arm leaves it set - *narrowed 2026-09-30, FABLE, [the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) bit 46*), may post event `0x2001` for the party-focus unit, and wait on the 109-byte presentation-finished test | done → 11 |
      | 11 | `00304FE9` | clears unit bit 13 (*shown*) | at once → 12 |
      | 12 | `00304FF3` | returns `1`, the action is finished | — |

      - **The `>= 9` reader at entry** (`003048BD`). Below phase 9 the unit's focus target `+0x710` must still
        resolve, or the call returns `-1`. From 9 on, the targets are built and the focus is no longer needed.
      - **Why a displacement census misses the advance.** Every `inc` addresses `[rsi + 4]`, not `[reg + 0x6B4]`.
        The battle-unit field map's row is corrected accordingly.
      - **Not read:** the called bodies beyond their names. `+0x760` / `+0x764` are `rsi`-relative `+0xB0` / `+0xB4`,
        and what they count was not named. Nothing was executed.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `00313DB0` is zero-argument and ring-driven | complete body (360 B, one contiguous range, `deab0e53...2461`) | 1 |
| Ring is 64 entries with those indices | complete body; read/write index arithmetic mod 64 | 1 |
| Sole producer is the standard-action pipeline | producer at `00304E5C` inside `00304850` (2,034 B, `48ca39ef...d680`), gated by `0030CA80` | 1 |
| `00313CD0` is a different ~~8-entry queue~~ 64-entry ring drained up to 8 entries per call *(corrected 2026-10-02, OPUS: `00313D18 and cl, 0x3f`, trip count `00313CF7 mov edi, 8`; section 7)* | complete body (220 B, `adf43795...e331`) | 1 |
| Command seam bodies | `00311CF0` (283 B, `774d9502...0bc81`), `00311CD0` (26 B, `0ee477c3...e22b`), `00311B20` (426 B, `8ef0373e...2ad67`) | 1 |

**Superseded readings:**
- *Old:* `00313DB0` is a preferred arbitrary selected-BattleUnit replay API, body 356 B,
  SHA `62e92b...`.
- *New:* **withdrawn.** The 356-byte extent came from a truncated executable-boundary pass;
  the real Ghidra body is 360 B. It has no BattleUnit parameter and is not a command entry
  point. The old body extent must not be used as function identity.

## 9. Related

- [`../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)
- [`../../08-Combat-Formula/`](../../08-Combat-Formula/)

## Mechanical re-check 2026-09-02 (AH-6) - stamp NOT advanced

**Addresses:** 14 cited - 13 function entries, 1 interior - **0 unresolved** against the current
parent (`verify_doc_addresses.py`).

Independent corroboration exists for the surrounding mechanism: separate work on
`BattleUnit_SelectAndCommitNextAction` (`00305AB0`) established that `qwUnitFlags` bit `0x4000`
marks a player-issued command, is consumed on read, and short-circuits gambit evaluation when the
command commits. That is consistent with this document's account of where a command enters.

**But this document's central claim is a negative** - that three nearby mechanisms *look* like the
entry point and are not, one of which was previously wrong here and withdrawn. Confirming a negative
requires re-reading all three candidates, which has not been done.

**The provenance stamp is therefore left at `381d2aea...`.** Addresses verified; claim not
re-derived. **AH-6 stays open**, which is the correct state - a stamp records verification, and
verifying the addresses is not verifying the argument.

## 7. Re-verification 2026-09-02 (AH-6) - one claim corrected

Stamped against parent `381d2aea...`; re-verified against the current `2ed8affb...`.

This document's central assertion is a **negative** - that three nearby mechanisms look like
the command entry point and are not. A negative cannot be confirmed by verifying addresses, so
the stamp was deliberately held back in an earlier pass. **All three candidates have now been
re-read, plus the seam itself.** One stated fact did not survive.

### CORRECTED: the pending action-selection queue is 64 entries, not 8

The document said `00313CD0` was "a *different*, **8-entry** pending action-selection queue."
The body says otherwise:

```c
lVar4 = 8;                                        // <- a LOOP TRIP COUNT
do {
  if (DAT_022be980 == DAT_022be981) { handle = 0; }
  else {
    uVar3 = DAT_022be980;
    DAT_022be980 = DAT_022be980 + 1 & 0x3f;       // <- capacity is 0x3F + 1 = 64
    handle = (&DAT_022be984)[uVar3 * 2];
  }
  ...
  lVar4 = lVar4 + -1;
} while (lVar4 != 0);
```

The `8` bounds **how many entries one call drains**, not how many the ring holds. The mod-`0x3F`
advance makes the capacity **64** - the same as the presentation ring.

**Why the error happened:** a single small constant near the top of a queue-draining function
was read as the queue's size. It is the one number in the body that is *not* about capacity.
The correction makes the two rings **structural twins**, which strengthens rather than weakens
this document's warning not to merge them: they are confusable precisely because they are
built identically.

**This is a real defect found by audit, not a rewording.** It is corrected in sections 2, 3
and 4.

### Confirmed: `00313DB0` is not a command API

`void FUN_00313db0(void)` - **no arguments at all**, so it cannot receive a command. It drains
the `022BEDA0` ring exactly as described, `(read + 1) & 0x3F`, empty when `read == write`,
publishes the resolved unit to `02089350`.

### Confirmed mechanically: the ring has exactly one producer

The claim "the ring's only producer is at `00304E5C`, inside `00304850`" was checked with a
writer census rather than by reading callers:

| Global | Writers |
|---|---|
| `022BEDA1` write index | **exactly one** - `00304E6E`, in `BattleUnit_AdvanceStandardActionState` (`00304850`) |
| `022BEDA0` read index | two - `00313DB0` (the consumer advancing it) and `BattleAction_ResetPendingQueueBanks` (a reset, storing a **word** and so clearing both index bytes at once) |
| `022BEDA4` data bank | the enqueue at `00304E5C`, `MOV dword ptr [RDX + RCX*0x8 + 0x219eda4], EAX` - an indexed store, plus the same reset |
| `02089350` | three - area-state init, and `00313DB0`'s publish and clear paths |

The cited producer address `00304E5C` is **exactly right**, and the paired-byte index layout is
confirmed by the reset writing both bytes in one 16-bit store.

### Confirmed: `0030F760` is a lower commit owner, not the intent seam

```c
longlong BattleUnit_CommitAction(unit, order_context, action_id, target_focus, mode)
    unit->pAction_context = order_context;   // 0x708 - field after aPad_704_707
    unit->dwTarget_focus  = target_focus;    // 0x710
    unit->wAction_id      = action_id;       // 0x714 - ushort, next field aPad_716_75B at 0x716
    unit->bAction_phase   = 0;               // phase reset
```

All four documented offsets hold, the first three provable by padding-field adjacency alone. It
takes an **already-resolved** `order_context` and target focus, so it sits downstream of intent
resolution - consistent with "genuine lower commit owner, not a universal funnel."

### New corroboration: the seam is where flag `0x4000` is born

`BattleUnit_IssueCommand(unit, target_focus, target_battle_stats_slot, command_id, flags)` sets:

```c
unit->nIssued_command_id     = command_id;
unit->nIssued_target_focus   = uVar3;
unit->wIssued_command_flags |= 0x8000;
unit->qwUnitFlags           |= 0x4000;     // <- the player-issued-command marker
```

Separate work on `BattleUnit_SelectAndCommitNextAction` (`00305AB0`) established that
`qwUnitFlags` bit `0x4000` marks a player-issued command, is consumed on read, and
short-circuits gambit evaluation. That was previously recorded here as merely *consistent* with
this document. It is now stronger than consistent: **this function is where that bit is set.**
The producer and the consumer of the marker have been read independently and they meet.

### Stamp advanced

Three candidates re-read, one producer census, one corrected fact, one upgraded corroboration.
**AH-6 is closed** - and it closed by finding an error, which is the outcome the provenance
register exists to make possible.

## `0030CA80` opened — the gate between a committed action and anything on screen

`BattleAction_CheckPresentationSlotReady` (`0030CA80`, 352 B) was the last unread link in the combat
chain: `BattleUnit_CommitAction` writes the state, `BattleFormula_ApplyTargetResult` applies the
result, and **nothing between them had been read.** Three documents cited it by name only.

**Extent checked**: 104 instructions, ends `ret` at `0030CBDF`, no `jmp` leaves the extent, **no loops**.

### Thirty-two presentation slots of 48 bytes

```asm
0030CA96  cmp   cl, 0x1f            ; slot index 0..31
0030CA9B  movsx rax, cl
0030CA9F  lea   rbx, [rax + rax*2]
0030CAA3  shl   rbx, 4              ; x 48
0030CAA7  lea   rax, [rip + …]      ; -> 022C17B0
```

**`022C17B0` is an array of 32 slots, `0x30` = 48 bytes each**, and **an out-of-range index yields a
null slot rather than a fault** (`xor ebx, ebx`), so the function proceeds with a null base — a
tolerant boundary that a caller cannot distinguish from a legitimately empty slot.

**The slot names an action:** `word [slot + 0x1C]` indexes the authored table at **`02EBF138`**, which
the [registry class map](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) assigns
to classes 19 and 20 and identifies as **action-id-indexed**. **Third independent confirmation of that
slot's identity**, from a consumer that neither of the first two touched.

### It answers two questions on two channels

**The return value is "is this slot ready":**

```asm
0030CB25  cmp dword ptr [rbx + 0x10], 3
0030CB3A  cmp dword ptr [rbx + 0x14], 3
0030CB40  cmp dword ptr [rbx + 0x18], 3
```

**Three separate dwords must all equal 3.** Not a bitmask and not a counter — **three independent
sub-states that each have to reach the same value**, which is the shape of three parallel resources
(model, animation, effect are the obvious candidates and are **not** claimed here).

**The out-parameter is "should it actually play":**

```asm
0030CB55  mov  eax, dword ptr [r14]
0030CB58  test rax, 0x3000
0030CB5E  jne  not_playing         ; caller's flags veto it
...
0030CB71  test word ptr [rcx + 0x2c], 0x100     ; the action record permits it outright
0030CB7B  cmp  ax, 0xffff                       ; ...or a sub-id is present
0030CB85  test dword ptr [rcx + 0xc], 0x40000000
0030CB96  call 0x2fcb40                         ; ...and passes a predicate
0030CB9F  test byte ptr [rbx + 0x2c], sil       ; ...or the slot's own bit
```

> **A slot can be *ready* and still not play**, and the two answers travel on different channels — the
> return value and an out-parameter. **A caller that checks only the return value gets a true that does
> not mean what it looks like.**

### It splits a bit-pair that another document reads as one

```asm
0030CB06  test dword ptr [02089340], 0x400     ; with a slot flag -> suppress entirely, return 0
0030CBAD  test dword ptr [02089340], 0x200     ; -> clear the out-parameter, return 0
```

**`0x200` and `0x400` of `02089340` are tested separately here and do different things.**
[`PartyControl_RecomputeSuppressionFromLeaderBattleState`](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)
tests them **together as `0x600`**.

> **Two consumers, one global, and the pairing is the caller's choice rather than the field's
> structure.** `02089340` now has four separately-observed policy bits — `0x40`, `0x200`, `0x400` and
> the `0x600` pair — and **whether `0x200` and `0x400` are one policy or two depends entirely on which
> function you read.**

### What is not established

- [x] ~~**UQ-109.** What the three dwords at `slot + 0x10`, `+0x14`, `+0x18` are, and why `3` is ready.~~
      **Answered 2026-09-14 (FABLE): they are three independent progress states.** Each follows
      **1 = requested → 2 = waiting → 3 = settled**, where settled means *done* or *nothing to do*. `3` is ready
      because it is each track's terminal value.
      - **Who writes them.** The allocator sets all three to `1` (`0030D136`–`0030D144`). The release zeroes them
        (`0030CA3B`, `0030CA3F`).
      - **The other writes all sit in one 556-byte walker.** Its only caller is
        `BattleSystem_RunFieldFrameOrchestrator`. It walks the slot list headed at `022BE978`, following `+0x00`. A raw sweep of every `mov dword [reg + 0x10/0x14/0x18], 2|3` in the combat range finds no other.
      - **`+0x10`, the presentation-parameter resource.** Handle at `+0x24`.
        - From `1`, the walker requests the resource for `BattleAction_GetPresentationParameter`'s value.
          - A `-1` parameter means none, and the state goes straight to `3` (`0030CCE4`).
          - A zero handle leaves it at `1`, so the request is retried next frame.
          - Any other handle moves it to `2` (`0030CCDB`).
        - From `2`, it moves to `3` once the handle's loader reports state `2` (`0030CCFC`–`0030CD05`).
      - **`+0x14`, the sequence-event request.** Handle at `+0x28`.
        - From `1`, it asks for `BattleAction_SelectGlobalSequencePresentationEvent`'s event through the unit's
          `+0x10` object.
          - `0` stays at `1`.
          - `0x80000000` goes to `3`.
          - `0x80000001` sets bit 31 of the unit's flags and goes to `3`.
          - Anything else goes to `2`.
        - From `2`, it moves to `3` when the request's entry in the 16-slot table at `02B57F70` reports state byte `3`.
          A negative handle reads as `3` at once (`0030CD53`–`0030CD74`).
      - **`+0x18`, the global special sequence.**
        - From `1`, `BattleAction_TryEnterGlobalSpecialSequence` decides.
          - `-1` means no sequence: `3`.
          - `1` means entered: `2`.
          - Other values stay at `1`.
        - From `2`, it moves to `3` once bit 29 of the unit's flags is clear, or the special-sequence step reports `1`.
          It then also sets the slot's `+0x2C` bit 0 (`0030CDBE`–`0030CDD8`). That is the "slot's own bit" the ready
          check above falls back on.
      - **Not named:** which asset kind the `+0x10` loader and the `+0x14` event table hold. The candidates in the
        paragraph above stay unclaimed. Nothing was executed.
- [x] ~~**UQ-110.** What `0x1000` and `0x2000` in the caller's flag word veto.~~ **Answered 2026-09-14 (FABLE):**
      the flag word is the battle unit's own `+0x00` flags. The two bits veto a unit whose action presentation is
      already in the shown-unit queue.
      - **Whose word it is.** The only caller is `BattleUnit_AdvanceStandardActionState`. It passes the unit record as
        `rdx` (`00304E37`), and the check reads `dword [rdx]` (`0030CB55`).
      - **What the bits are.** Both are recorded as rows 12 and 13 of
        [the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md), with
        [the ladder page](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)'s
        cursor section.
        - **`0x1000`**: the unit is queued in the presentation cursor ring `022BEDA4`.
        - **`0x2000`**: the cursor has popped the unit, and its presentation is the one on screen.
      - **The loop it closes.** When this check reports *should play*, the same caller pushes the unit's handle onto
        the ring and sets `0x1000` (`00304E45`–`00304E74`). So the veto stops a unit from being queued a second time
        while its first presentation is still waiting or showing.
      - That bit 13 is cleared when the presentation finishes is the field map's row. It was not re-read here.
- [x] ~~**UQ-111.** What `002FCB40` tests about the action's sub-id.~~ **Answered 2026-09-14 (FABLE):**
      bit 5 of the sub-id's entry in a per-id load-cost table. No instruction that addresses the table sets that
      bit, so the predicate reads `0`, and the sub-id arm of the ready check never admits a slot by itself.
      - **The test.** The 21-byte body is `movzx eax, byte [02EC19C4 + id*8]`, `shr eax, 5`, `and eax, 1`. Its
        argument is the action record's `+0x24` word. The call is made only when that word is not `0xFFFF` and not
        negative, and the record's `+0x0C` bit 30 is clear (`0030CB77`–`0030CB96`).
      - **The table** is 512 entries of 8 bytes at `02EC19C0`, 0x1000 bytes long.
        - `+0x00` holds a byte size rounded up to 64. A 103-byte initialiser fills it for every id from a
          resource-size lookup of kind `0x26` or `0x0B`.
        - The low five bits of the `+0x04` word are a load cost. A 313-byte initialiser memsets the whole table and
          then ORs in `byte[01EEBB10 + id] & 0x1F` for ids 0–400. The shipped bytes take only the values
          0, 1, 2, 4, 8 and 24.
        - The loaders add these costs over the list at `02EC3D60` and refuse a load that would exceed 24
          (`cmp eax, 0x18` in the 898-byte loader and the 115-byte can-load test).
      - **Nothing sets bit 5.** Across the whole image, eight functions address the table `rip`-relative, each through
        a `lea` of its base or of `+0x04`, or a direct read of entry 0: the two initialisers, the loaders and cost summers, this predicate, and a
        size reader. The only write to the `+0x04` word is the initialiser's `and 0xFFE0` / `or cost`. The cost byte
        is masked to five bits, and no shipped cost byte has bit 5 set in any case.
        - Two spawn-group functions `lea` `02EC19D0`, but only as the end pointer of loops over the group ledger
          below it.
      - **Consequence for the ready check.** After the veto on the caller's flags, a slot can play only through the
        action record's `+0x2C` bit `0x100`, or the slot's own `+0x2C` bit.
      - **Not excluded:** a write through a copy of the table pointer. None of the eight functions passes the base to
        a callee other than `memset`. Nothing was executed.
- [x] ~~What distinguishes `0x200` from `0x400` in `02089340`~~ **Answered 2026-09-12 (by propagation):** bit 9
      (`0x200`) = every active party member is incapacitated, bit 10 (`0x400`) = the whole roster is
      ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5).
      So this function suppresses entirely when the whole roster is down (with a slot flag) and only clears
      the out-parameter when the active party is down; the leader-state mask treats either as all-suppressed.
- [x] **UQ-112.** The remaining 44 bytes of a slot. Only `+0x10`, `+0x14`, `+0x18`, `+0x1C` and `+0x2C` are read
      **Narrowed 2026-09-14 (FABLE): every byte but `+0x1E`–`+0x1F` is placed.** The slot array is 32 × `0x30` at `022C17B0`.
      Offsets come from the seven functions that address the array `rip`-relative (the pool reset, the allocator, the
      release, the ready check, a second 185-byte readiness test and two handle readers), plus the frame walker and the `+0x2C` step:
      ***ANSWERED 2026-09-18 (FABLE): `+0x1E`..`+0x1F` is alignment padding after the `u16` action id, accessed by nothing.** The eight functions that reference the slot array `022C17B0` or its list heads `022BE978` / `022BEB88` rip-relatively (`0030A250`, `0030BC40`, `0030C970`, `0030CA50`, `0030CA80`, `0030CBE0`, `0030CF40`, `0030D070`) and every function they call to a depth of two, 44 in all, contain no instruction that reads or writes a `+0x1E` or `+0x1F` displacement off a non-stack register; the allocator's only touch of the neighbouring bytes is the word compare `cmp word ptr [r9+0x1C], cx` (`0030D0AA`) and the word store `mov word ptr [rcx+0x1C], r10w` (`0030D14F`), and the pool reset `0030A250` is a single call (`0031B7E0`) with no clear of the array. The array is zero-initialised `.data`, so the two bytes stay zero for the life of the process: the slot is 0x30 bytes because `+0x20` needs 4-byte alignment after a 2-byte id. Static, the closure scanned instruction by instruction.*

      | offset | size | what | evidence |
      |---|---:|---|---|
      | `+0x00` | 8 | next live slot; the list head is `022BE978` | allocator `0030D106`–`0030D112`, walker `0030CDE6` |
      | `+0x08` | 8 | previous live slot; the list tail is `022BEB88` | allocator `0030D119`–`0030D126`, release `0030C9B7`–`0030C9EB` |
      | `+0x10` / `+0x14` / `+0x18` | 4 each | the three track states (UQ-109) | allocator sets 1, release clears |
      | `+0x1C` | 2 | the action id; `0xFFFF` = free, which is the allocator's search key | allocator `0030D0AA`, `0030D14F` |
      | `+0x1E` | 2 | **no access found** in any of the nine functions *(answered: alignment padding after the `u16` action id, accessed by nothing - the 2026-09-18 answer above; 2026-10-02, OPUS)* | — |
      | `+0x20` | 4 | the owning unit's focus handle | allocator `0030D14B`; walker and release resolve it |
      | `+0x24` | 4 | the presentation-parameter resource handle; `-1` = none | reset, release; the two handle readers return it |
      | `+0x28` | 4 | the sequence-event request handle; `0x80000000` = none | reset, release (released through its own call first) |
      | `+0x2C` | 4 | flags; the release and reset clear the low five bits | see below |

      - **`+0x2C` bit 0**: the special-sequence track settled with a sequence (UQ-109).
        - The ready check returns 0 for such a slot when `02089340` has `0x400` set (`0030CB00`–`0030CB10`).
        - Otherwise the bit is the check's last admission (`0030CB9F`).
      - **Bits 1–2 and 3–4** are two 2-bit codes, written by the 212-byte step the walker calls first
        (`0030C8E2`–`0030C907`).
        - Bits 1–2 come from a 104-byte query on the sequence event.
        - Bits 3–4 come from a query on the presentation parameter. That query reaches the load-budget test of UQ-111.
        - The step returns `2` when both codes are `2`, `1` when both are non-zero, and `0` otherwise.
        - What codes `1` and `3` mean was not read.
      - **Which unit byte names a slot.** The ready check takes the unit's `+0x694`. The two handle readers take
        `+0x695`.
      - **Still open:** ~~`+0x1E`–`+0x1F`,~~ *(answered: padding, 2026-09-18 above; 2026-10-02, OPUS)* the `+0x2C` bits above bit 4, and the meanings of the 2-bit codes.
      here.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **Movement — SERVICE and CLIENT.**
  - `BattleUnit_AdvanceStandardActionState` (`00304850`) steers through `BattleLocomotion_SetApproachAndReference…`,
    `BattleUnit_UpdateCombatNavigationStep`, `BattleLocomotion_ResetPathAndSetTargets` and a 94-byte helper.
  - `00313CD0` and `00313DB0` are both called by a 109-byte Movement-filed body. That body also runs
    `PartyControl_RecomputeSuppressionFromLeaderBattleState` and `Navigation_HasDataset`.
  - The script-side `00355830` stops the actor through `Actor_StopRequestedMovement`.
- **Audio — SERVICE, not read.** `00313DB0` calls a 13-byte Audio-filed forwarder, which is unread.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT and SERVICE.** A cited function is called by `BattleUnit_RunPeriodicCombatMaintenance`, and another calls `BattleStats_ChangeStatusAndProcessSideEffects`.

**Party — CLIENT (SWE2-EC7-158, 25 edges).** Batch-123's `0026B4A0` names `00351F40`/`00355540`/`00355A00`/`00238BF0`, and the seam's own `0026D6D0` is called by the party layer's `00358B40`/`00359200`/`00359250`/`003592C0` — the party side consults the seam's helpers, fan-in only.

- **CombatFormula — SERVICE (3 edges).** `BattleUnit_AdvanceStandardActionState` (`00304850`) reaches the combat formula helpers `00387090`/`00387A50`, and `003202F0` calls `0031B860` — formula-side leaves the seam's bodies consume.
- **Presentation — SERVICE and CLIENT (14 edges).** `0030F760` calls `00313B30`, and `003590D0` is called by presentation-side bodies `003A4290`/`003A56F0`/`003F1Axx` — the seam's lower-commit and helper lanes cross that layer both ways.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAI — CLIENT and SERVICE (6 edges).** `BattleUnit_SelectAndCommitNextAction` `00305AB0` is called by `BattleUnit_UpdateCombatFrame` `00308610` and by the action-ring drain `BattleUnit_ProcessPendingActionSelectionQueue` `00313CD0`, and calls `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0`; both of those call the lower commit `BattleUnit_CommitAction` `0030F760`; and `AiOrder_EvaluateTargetSelector` `00301AD0` calls `BattleUnit_ResolveByFocusHandle` `0031B7E0`. The AI side is where an action is chosen, and it commits through the lower commit this page places below the seam; the gambit target selector resolves focus handles with the same resolver the seam uses.

**Gameplay — SERVICE and CLIENT (12 edges).** `BattleUnit_AdvanceStandardActionState` `00304850` calls `BattleUnit_DispatchActorPresentationEvent` `003299B0` and `BattleAction_FindApproachGeometryAroundTarget` `00339630`; `0030CBE0` calls `BattleEncodedId_IsValidForClass` `00322C50`; `0030F760` calls `BattleTargetBuffer_TryAppendActorWork` `00316CD0` and `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0`; the cleanup step `003138D0` and the presentation drain `00313DB0` call `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0`; `0031B7E0` is also called by `BattleUnit_HasCurrentFocusEngagementEvidence` `0030BB30`, `00312B40`, `0031ADB0` and `00339630`, and `0031ADB0` calls `PartyFocus_GetCurrentPackedActorHandle` `003590D0`. These ownerless combat helpers are what the non-seam bodies use: the lower commit refills the target buffer, the drains read the battle runtime mode, the standard action state raises presentation events and solves approach geometry, and the domain's focus-geometry code shares the focus resolver.

**Input and InputGameplay — SERVICE and CLIENT (3 edges).** The presentation drain `00313DB0` calls the per-channel actor mask helper `00226BE0` and the capability / UI-request inhibit reconciliation `00313A00`; `00226BE0` in turn calls `003590D0`. Draining a presentation entry re-derives which input channels and UI requests are allowed for that unit, and the input helper reads the current focus handle to do it; the seam itself reads no raw input.

**Spawn_Encounter_Lifecycle — CLIENT (1 edge).** `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0`. Spawn activation refreshes the new unit's actor runtime from its definition through the same body the party crossing already names; it issues no command through the seam.

**UI — CLIENT (6 edges).** `BattleMenu_UpdateCommandSelectionAndDispatch` `002778C0` calls `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout` `00311B20` and `BattleUnit_IssueCommandByFocusHandles` `00311CD0`, and `BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands` `0027C3D0` calls `00311CD0`; `BattleMenu_BuildCommandEntryList` `0031EB20` calls `0031B7E0`; `00299BD0` and `002C7660` call `003590D0`. A command picked in the battle menu enters the real command seam through these entries, and other menu bodies read the focus handle and resolve it; the menu is the player's route into the seam.

**World and WorldAreaField — SERVICE and CLIENT (11 edges).** `00305AB0`, `0030F760`, `00311B20`, `BattleUnit_IssueCommand` `00311CF0`, `00313A00`, `00313CD0` and `00313DB0` call `FieldData_GetActiveFieldRecordBit15` `00377C20`; `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `0030CBE0` and `00313A00`; and the World-filed `0025E400` and `002623A0` call `003590D0`. The seam and the bodies around it re-check a status-bearing unit against the area's action-permission bit (the seam's status gate), the field frame runs the slot-array body and the inhibit reconciliation, and two world bodies read the current focus handle.

## The `0030CA80` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0030CA80` ~~(`BattleAction_CheckPresentationSlotReady`, ~21 B)~~ (`BattleAction_CheckPresentationSlotReady`, 352 B *(corrected 2026-10-02, OPUS: `0030CA80`–`0030CBDF ret`, 104 instructions, as the section on `0030CA80` above states)*) — arg
shuffle `rdi = r8`, `r14 = rdx` (`0030CA90`/`0030CA93`).

| member | role | interior |
| --- | --- | --- |
| `002FCB40` | `02EC19C4` byte table — `[rcx + rax*8] >> 5 & 1` bit extract (`002FCB43`/`002FCB4E`) | [`002FCB43`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-50 update (2026-09-19) - `0030A250`

`0030A250` (185 B) is the slot-array pool reset - `0020E600`/`0031B7E0`, a single clear pass over `022C17B0`. Interior anchor `0030A254` (a `0020E600` call).

## SWE2-EC7-62 update (2026-09-19) - `00355830`

`00355830` (148 B) is the `setuptreasure` verb handler - `002640C0`/`002650B0`/`00267E10`/`00269090`/`0026D6D0`/`003588B0`/`003590D0`. Interior anchor `00355854` (a `002640C0` call).


## SWE2-EC7-105 update (2026-09-20) - `0025D5E0` measured

`0025D5E0` (88 B) is the flag-clear
dispatch `00238BF0`, `00355830`,
`003558F0` and `00355A00` run: when
`byte[rcx + 0xC]` bit 5 is armed and
`edx - 4 <= 1` it returns early; otherwise
`edx == 0x10` clears `byte[+0xB]` bit 2 and
runs `00262740`, `edx == 0x11` runs
`002626C0`, and every fall-through clears
bit `edx` of `dword[+0x1C]` - the
indexed unlatch the command arms share.
Interior anchor `0025D613` (the `+0xB` bit
clear).

## SWE2-EC7-106 update (2026-09-20) - `00262740` + `002626C0` measured

`00262740` (115 B) is the range-4
unlatch `0025D5E0` and `00268EA0`
run: `byte[rcx + 3] & 0x1F` picks the
record class, `ebx = 4` only when the
class is 7 else `6`, then
`003DBEA0(rcx, ebx, -1, 5)` iterates -
every index it returns below `0xFF` is
handed to `003DB2A0(rcx, idx)` until
the iterator exhausts. Interior anchor
`00262777` (the first `003DBEA0`
call).

`002626C0` (115 B) is the byte-twin
the same two callers reach -
identical shape with `ebx = 3` when
the class is 7 else `5`, and the
`003DBEA0` iterator called with bound
`4` instead of `5` - the narrower
range the pair shares.
Interior anchor `002626F7` (the first
`003DBEA0` call).

## SWE2-EC7-107 update (2026-09-20) - `003DBEA0` measured

`003DBEA0` (181 B) is the entry
iterator `002626C0` and `00262740`
drive: `word[rcx + 6]` bit `edx`
armed short-circuits to `0xFF`; the
walk starts at `byte[rcx + edx +
0x94]` (or `byte[rcx + 0x61]` when
`edx < 0`) and follows `byte[entry]`
links through the `0x14`-stride
`[+0xA0]` table - a hit is an index
whose `word[entry + 4] == r8d` or
`byte[entry + 0x12] >> 1 == r9d`
(each test armed only when its
parameter is non-negative), bounded
by `byte[rcx + 0x89]` hops; `0xFF`
ends the chain. Interior anchor
`003DBEB6` (the `bt` on `word[+6]`).

`0026B4A0` (32 B) is the flag-set + propagate `00238BF0`/`00351F40`/`00355540`/`00355A00` call: `dword[rcx+0x1C] |= 1 << dl` sets the bit, then `byte[rcx+0xB] & 8` decides whether to tail `00268EA0` - the record's flagged-notify.

Interior anchor `0026B4AA` (function `0026B4A0`).

`00325A20` (162 B) is the `003DC410` classifier `0030C890` runs: when `[rcx+0x698]` exists with `byte[+5]` clear it reads `r8d = byte[word[02EBF180] + rdx + 4]`, else `003202F0` fills it; the `003DC410([rbx+0x10], edi, r8d)` result maps to `0`/`1`/`2` - zero stays 0, `0x80000000`..`0x80000001` return 2, everything else 1

Interior anchor `00325A7E` (function `00325A20`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-native-command-seam-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00359250` | 103 B | sets (when `edx` is nonzero, via `bts`) or clears (when `edx` is zero, via `btr`) bit `ecx` of byte `022C8004` and stores the low byte back; then, when bit 0 of that new byte OR bytes `022C8005`, `022C8006` and `022C8007` is set, passes dword `022C7FE0` to the call at `00359250`+0x4C and tail-jumps `0026D6D0` with its result when that result is non-null, otherwise (bit clear or null result) returns | `0035925F`, `00359271`, `00359292`, `0035929C`, `003592AD` |
