---
system: Applying a result to a target
category: 07-Combat-Action
status: DOCUMENTED
owner_layer: PrimaryOwner:CombatFormula — the result is applied by the formula owner; the page sits under 07 by subject, not by owner
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-22
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: true
  reopened_count: 0
production_review: "SECTION-01 corrections; prior audit metadata is historical, current T2 peer review pending."
---

# Applying a result to a target

`BattleFormula_ApplyTargetResult` at **`003112F0`**, 2,040 bytes. Three documents leaned on it and
none had opened it — **and one of them had already established that poison damage and a sword swing
arrive here through the same door.**

> **Current correction (SECTION-01, 2026-09-22):** this page's original instruction-order
> table is retained, but the universal-sentinel, confirmed-change, and absence-of-refresh
> interpretations below have been corrected. The [contract](CONTRACT-apply-result-to-target.md)
> and [review](../_experiments/evidence/continuation-section01-result-install/REVIEW.md)
> distinguish direct copies, caller-tail recompute, and nested callee effects.

## What the player sees

**This is where an action stops being a decision and becomes changes to the world.** Everything that
"happens to" a target happens here: the number that appears over its head, the statuses it gains and
loses, the stat changes, how long each status lasts, and — separately — whatever the *attacker* gains
in the same instant.

**One result record selects the effects.** Quantities mainly come from upstream, but this
routine also multiplies the secondary resource, computes relative stat adjustments, and
subtracts gil. Dispatch additionally depends on current stats, owners, globals and callees.

## The record is a to-do list of independent effects

**Absence is field-specific.** Masks/presence bits use zero; layer and level bytes use
`0xFF`; the item dword uses `-1`; parameter and timer copies skip negatives; multiplier,
steal/effect selectors and gil use zero. **All-`FF` is not neutral**: it selects both
32-bit status masks. Even an effect-neutral fixture can run metadata and owner-bit cleanup.

| in the record | effect on the target |
|---|---|
| `+0x54` | **32-bit mask of statuses to apply**, with per-status parameters at `+0x5C` (dword each) and `+0xDC` (`s16` each) |
| `+0x58` | **32-bit remove mask over the same status IDs**, parameters zeroed, mode 0 |
| `+0x3C` (2 bytes) · `+0x3E` (4 bytes) | mutable-layer **set** (mode 2) and **clear** (mode 0) respectively |
| `+0x42 … +0x50` (8 × `s16`) | **written straight into the target's `+0x17C` array** — ~~the status duration timers~~ the eight effect-slot timers (stage 3's countdown, keyed by the effect table; not the 32 statuses' durations, which are `+0xBC`) *(renamed 2026-09-29, FABLE; `_index/candidates/pkg-gp-status-poison/timers.md`)* |
| `+0x24` / `+0x2A` | the target's two applied numbers |
| `+0x20` / `+0x28` | **the source's two numbers, in the same call** |
| `+0x1D` (`s8`) | a **multiplier** — applied as `target[+0x28] × value` |
| `+0x11E · +0x120 · +0x122 · +0x124` | foe-only stat deltas, each **relative to a base byte on the target** |
| `+0x128 … +0x12F` | foe-only: **four bytes OR-ed in, four bytes AND-NOT-ed out** |

**The two masks apply and remove the same 32 status IDs.** The apply parameters are
indexed by bit position:

```asm
00311510  mov   eax, dword ptr [rbx + 0x54]
00311513  bt    eax, ebp                      ; bit per status
00311516  jnc   0x00311545
00311518  movsx eax, word ptr [r12]           ; parameter B, +0xDC array
00311521  mov   r9d, dword ptr [r15]          ; parameter A, +0x5C array
0031153A  call  0x0030E360                    ; apply
0031153F  mov   r14d, 0x1                     ; <- "something happened"
00311547  add   r12, 0x2                      ; s16 stride
0031154B  add   r15, 0x4                      ; dword stride
0031154F  cmp   ebp, 0x20
```

## The flag that selects the outer stats recomputation

**`r14d` is a branch-selected outer-recompute flag, not a callee-success result.**
At `0031153F/003115A4/003117D0/0031180C`, it is set after a selected status/layer call
without checking whether that call changed anything. At the very end:

```c
if (target && (flags & 0x200) == 0 && branchSelectedRefresh) FUN_0030FED0(target, 0);
```

> **Absence of every dirty-flag-setting branch skips the outer recompute.** Selected-but-idempotent or refused status calls still set this flag. Bit 9 of the caller's
> fifth argument suppresses this outer call, not arbitrary nested recomputes.

## Both sides, in one call

The source is not a bystander. `+0x2C` bit 7 drives a call against the **source** with `+0x20`, and
bit 13 another with `+0x28` — **structurally identical to the target's `+0x24`/`+0x2A` pair.**

> **That is why a draining attack needs no special path: the record simply has numbers in the source
> fields as well as the target fields**, and the same applier writes both.

**And the choice of function is a bit, not a branch on meaning:** `+0x2C` bit 3 selects between
`00300530` and `00300520`, bit 4 between `00300CE0` and `00300C90`. Two implementations per quantity,
picked from the record.

## The copy-through, and its sentinel

After the apply masks, **32 dwords from `+0x5C` and 32 `s16` from `+0xDC` are copied into the target at
`+0x60` past the same positions** — but only where the value is **not negative**. **The same arrays
that parameterised the apply are copied to stats `+0xBC/+0x13C` even when both masks
are zero.** Negative values preserve the destination; zero is copied. This copy-through
does not set `r14d`. EXP-149's contrary prose is withdrawn by SECTION-01.

## Foe-only paths

Three effects run **only when the target's record byte `+0x05` is `1`** — the byte that separates the
two sides everywhere in this engine:

1. **Three slots at `+0x32`**, each resolving through `targetActor[+0xE60]` to an id; on a hit the
   engine clears the matching bit in `targetActor[+0x6A0][+0x14]`. **Three slots, one bit each,
   consumed on use.**
2. The four stat deltas at `+0x11E …`, each computed as **`value − base_byte`** and *added* to the
   live stat.
3. The eight status bytes at `+0x128 …`, four setting and four clearing, **each followed by
   `flags |= 0x80` on the target's `+0x6A0` block** — a dirty bit raised once per change.

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Are `+0x54` and `+0x58` two halves of one 64-bit mask? | **No** — different loops, different call arguments (`+0x58`'s pass parameters `0, 0` and a different mode), and each is tested against `0` separately before its loop. |
| Is `-1` universally a sentinel? | **No (SECTION-01 correction).** Copy loops skip all negative values; selected scalar fields skip `-1`; masks and presence fields use zero. The old all-ones neutral conclusion was false. |
| Does the `+0x42 …` block really write the status timers? | It writes `target + 0x17C … +0x18A` — **the array a separate document established as ~~the status duration timers~~ the eight effect-slot timers** *(renamed 2026-09-29, FABLE; `_index/candidates/pkg-gp-status-poison/timers.md`)*, decremented one step per tick. Two independent reads, same array. |
| Is `r14d` a return value? | **No** — the function returns `void`; it is consumed only by the final `0030FED0` guard. |
| Could the source-side calls be the target's, misread? | They are in a `param_2 != 0` block using `+0x20`/`+0x28` and pass **`0` where the target block passes the source** — a distinct argument shape, not a repeat. |

**What this document does not claim:** what any individual status bit is, what `0030E360`,
`0030E130`, `00300530`, `00300BC0` or `0030FED0` do internally, what the three consumable slots are,
what `+0x08`'s timer arithmetic feeds, or which caller fills the record. **This is a survey of the
applier's shape, not a decode of its callees** — and the shape is the part three documents were
leaning on without it.

> **Decoded since:** `00300530` and `00300520` are read in
> [the HP write and the lethal transition](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)
> (2026-09-10), including how this applier's `+0x2C` bits 3, 6, 8, 10, 18 and 19 become the writer's
> flag word at `00311608`–`00311668`. **And the applier itself is now decoded in execution order
> below** — the section this survey said it was not.

## The decode, in execution order — 2026-09-10 (FABLE)

`BattleFormula_ApplyTargetResult(record /*rcx*/, sourceStats /*rdx*/, targetStats /*r8*/, id /*r9w*/,
flags /*[rsp+0xA0]*/)`. Both stats records are mapped to their battle units first
(`BattleStats_FindOwningBattleUnit` `0031B860` at `00311321` and `0031132C`; either may be null and
every block below that needs a unit checks). `r14d` starts at `0` (`00311347`); `[rsp+0x44]` holds
caller flag bit 9 (`0031134A`–`00311350`). Every step is cited; the record offsets are the record's,
the stats offsets the BKBI record's (unit `+0x698`), unit offsets the battle unit's.

| # | site | gate | what |
|---|---|---|---|
| 0 | `00311354`–`00311367` | caller flag bit 0 clear | `BattleTarget_HasLow16EligibilitySuppression` (`0030B9B0`) `(targetUnit, sourceUnit)` non-zero → **return, nothing applied** |
| 1 | `0031136D`–`0031137A` | — | `BattleFormula_ApplyResultMetadata(id, sourceStats, targetStats, record)` (`00385BA0`, 250 B, **read 2026-09-12**): record `+0x138` (the streak count, `≠ −1`) → battle-state block `+0x5B0E` byte (`00385BAF`–`00385BD1`); `+0x13C` (the walk echo, `≠ −1`) → block `+0x5B00` (`00385BD7`–`00385BEA`); for each non-zero steal slot `+0x34` / `+0x33` / `+0x32` the target unit's `+0x6A0` block byte `+0x14` loses bit 2 / 1 / 0 (`00385BF0`–`00385C6B`); then, when the record's resolved mark `+0x1C == 1`, `BattleFormula_DispatchPostResultEvents(actionId = word [02AEDFD4], source, target, record)` (`00385C6F`–`00385C85`). **The `id` in `cx` is never read** — the event dispatch takes the current action id from the formula scratch word instead |
| 2 | `0031137F`–`003113BF` | target unit | record `+0x2C` bit 19 → unit `+0xE9A \|= 8`; record `+0x140` bit 14 → sound `0x34` through `003A1180` / `002DF220(id, 0x40, 0x7F)` (skipped when `003A1180` returns `−1`) **and, inside the same bit-14 block, unit `+0xE9A \|= 4`** (`00311394`–`003113BF`; corrected 2026-09-12 — the bit is not set on every apply). Flag C bit 14 has one writer image-wide, the Poison beat in `BattleFormula_AdvanceStatusTimersAndBuildResult` (`00386DF5`, `00386E1D`, `00386E2F`), so **bit 2 means "this apply is a Poison tick"** and bit 3 "taken, not struck". Both are cleared again at `00311AA8`; their one reader is `BattleUnit_ProcessDefeatRewardsAndLoot` (`003122F4`), which the status write reaches on a defeat (`0030E884`) during this call — rewards without a party killer for a Poison-tick death of a party-poisoned foe, none at all for a taken one (the status-write page's `FA-4`) |
| 3 | `003113C6`–`003113FD` | stats present | record `+0x11C` (s8, `-1` = none) → `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth(targetStats, value, 0)`; `+0x11D` likewise on the **source** |
| 4 | `00311402`–`0031148B` | target unit spawn-backed (`+0x698` byte `+5 == 1`) | **three slots at record `+0x32`, `+0x33`, `+0x34`**: for a non-zero slot *i*, the `u16` at `targetUnit->p_E60 + 0x32 + 2i` is an item id (`0xFFFF` = none) → `Inventory_ModifyEncodedItemAndUpdateDiscoveryState(id, 1, 0, 1, 0)` (`00311457`) — **one of that item into the inventory** — then **bit *i* of the spawn record's `+0x14` is cleared** (`0031145C`–`0031146F`) and `00316A50(3)` (PlatformOnlineAchievements, via the thunk `00253770`) is poked. Three per-unit slots, each consumed once, each adding an item: the shape of *Steal*; the imported field name for spawn-record `+0x14`, `bStealAvailabilityFlags`, agrees (tier 9 lead, [spawn placement](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) §4) |
| 5 | `0031148D`–`003114A8` | — | record `+0x38` (`u16`, `-1` = none) → the same inventory add with the id directly |
| 6 | `003114D2`–`003114EE` | target stats | two flag words for the status loops: `esi = 0x200 \| (record +0x140 bit 4 ? 2 : 0)`, `[rsp+0x40] = 0x200 \| (bit 5 ? 2 : 0)` |
| 7 | `003114F2`–`00311552` | `+0x54 != 0` | **add mask**: for each set bit *i*, `BattleStats_ChangeStatusAndProcessSideEffects(targetStats, sourceStats, i, +0x5C[i] /*r9d*/, +0xDC[i] /*[0x20]*/, esi, mode 3)` — **mode 3 = set the bit in `+0x64`**; `r14d = 1` |
| 8 | `0031156A`–`003115AF` | `+0x58 != 0` | ~~a second apply mask with parameters zeroed~~ **the remove mask**: the same call with `0, 0` and **mode 0 = clear the bit in `+0x64`** (`0031158A`, `0031159A`); `r14d = 1` |
| 9 | `003115B6`–`00311606` | — | copy-through: `+0x5C[32]` dwords and `+0xDC[32]` `s16` into the target at `+0x60` past the same positions, non-negative values only |
| 10 | `00311608`–`00311668` | `+0x2C` bit 8 | **HP**: value `+0x24`, source passed, flags from `+0x2C` (b19→8, b10→5, `!`b18→6, `!`b6→4); `BattleStats_SetCurrentHP` when bit 3, else `ModifyHP` — `call rax` |
| 11 | `0031166A`–`003116A4` | `+0x2C` bit 14 | **MP**: value `+0x2A` (`s16`), flags (~~b11→5, `!`b8→4~~ **b16→5, `!`b12→4** — corrected 2026-09-11, `00311679`–`0031168D`); `BattleStats_SetPrimaryResourceAbsolute` when bit 4, else `ModifyPrimaryResource` |
| 12 | `003116A6`–`003116E0` | `+0x1D != 0` | `BattleStats_ModifySecondaryResource(targetStats, targetStats->w_28 × (s8)+0x1D, flags)` — **the secondary pool `+0x06` changed by `+0x1D` whole max-MP units** (`+0x28` is max MP; the pool is the charge store kind-5 / 6 actions spend, `CS-3`), so `+0x1D` is a signed charge count; flags (~~`!`b8→4, b11→5~~ **`!`b12→4, b16→5** — the same two as step 11, `003116B8`–`003116C9`; and `0x400` when the multiplier is negative) |
| 13 | `003116F3`–`00311778` | source stats | **the source's own two numbers**: `+0x2C` bit 7 → HP on the source with value `+0x20`, no source, flags (~~`!`b1→4, `!`b11→6, b4→5~~ **`!`b5→4, `!`b17→6, b9→5**, `0031170A`–`00311729`), absolute when bit 1 (`00311739 call r12`); bit 13 → MP on the source with `+0x28`, flags (~~`!`b7→4, b10→5~~ **`!`b11→4, b15→5**, `00311753`–`0031176A`), absolute when bit 2 (`00311775 call r15`) — corrected 2026-09-11 |
| 14 | `00311781`–`00311819` | target stats | ~~statuses to remove~~ **status-layer bytes**: `+0x3C`, `+0x3D` (`0xFF` = none) → `BattleStats_ModifyStatusLayerStateAndProcessSideEffects(targetStats, byte, -1, 0x200 \| (+0x140 bit 6 ? 2 : 0), mode 2)`; `+0x3E`–`+0x41` → the same with `0`, `0x200 \| (bit 7 ? 2 : 0)`, mode `0`. `r14d = 1` each. **Mode 2 sets and mode 0 clears the mutable layer `+0x68`** ([the status write](../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2.8), so these are **two layer effects to add and four to remove** |
| 15 | `0031181B`–`0031189B` | — | eight `s16` at `+0x42`–`+0x50` → target `+0x17C`–`+0x18A` when non-negative — ~~the status timers~~ the effect-slot timers *(renamed 2026-09-29, FABLE; `_index/candidates/pkg-gp-status-poison/timers.md`)* |
| 16 | `0031189B`–`00311915` | target stats byte `+5 == 1` | four foe stat deltas: `+0x11E` → `w_08 += v − b_2A`, `+0x120` → `w_0A += v − b_2B`, `+0x122` → `w_12 += v − b_2F`, `+0x124` → `w_14 += v − b_30`; `r14d = 1` each |
| 17 | `00311919`–`00311A7E` | target unit spawn-backed | record `+0x128`–`+0x12B` OR into spawn-record bytes `+0x7B`, `+0x79`, `+0x78`, `+0x7A`; `+0x12C`–`+0x12F` AND-NOT the same four; each also `spawnRecord->d_00 \|= 0x80`; `r14d = 1` each |
| 18 | `00311A84`–`00311A9E` | `+0x08 != 0` | **gil**: `GameState_SetGil` (`00254EE0`) of `max(GameState_GetGil() (`00253690`) − value, 0)` — a deduction, floored at zero. **Only one recipe reaches it** (2026-09-12): step slot 163 (`0038F6F0`) is the whole committed list of recipe 99, action `0x103` "gil bug" — the trap whose line is "… Your pockets feel lighter" — and writes `(1 + mt19937 % actionRow[+0x10]) × (1 + mt19937 % target level +0x1C2)`, `0` when the party holds no gil; the other writer, slot 18, fills a *preview* record that never reaches this applier (the gil throw is charged by Consume from unit `+0xE54`) |
| 19 | `00311AA3`–`00311AA8` | target unit | `+0xE9A &= ~0x0C` — the two "being applied" bits from step 2 |
| 20 | `00311AAF`–`00311AC5` | target stats, `!`flag bit 9, `r14d` | `BattleStats_RecomputeDerivedStateAndAutoStatuses(targetStats, 0)` |

### Corrections to the historical survey

- **`+0x58` is not a second apply mask; it is the remove mask.** Both loops call `0030E360`, but the
  seventh argument — the operation mode the field-record page decoded — is `3` (set the bit in
  `+0x64`) for `+0x54` and `0` (clear it) for `+0x58`. *"Parameters zeroed"* was true and beside the
  point.
- **`+0x3C`–`+0x41` do not go to `0030E360` at all.** They go to
  `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (`0030E130`), two bytes in mode 2 with
  `-1`, four in mode 0 with `0`. What that function's modes do is not read here; *"statuses to
  remove"* is withdrawn as a description and replaced by the calls.
- **Step 2's `+0xE9A` bits are not "being applied" markers set on every call** (corrected 2026-09-12):
  bit 3 follows flag A bit 19 and bit 2 sits inside the flag C bit 14 block, which only a Poison beat
  sets. Both are cleared at the end because their one reader, the defeat processor, runs inside the
  apply.
- **`r14d` is not set by every branch that changes the target.** The HP, MP and secondary-resource
  writes, the steal and item adds, the timers and the gil deduction leave it alone; only the status
  loops, the status-layer bytes, the foe stat deltas and the spawn-record flag bytes set it. So **a
  pure numeric result never selects the outer-tail recompute**. Numeric callees may still
  recompute internally (EXP-149's lethal case does); selected-but-unchanged status calls
  still set the outer flag. Neither fact is a claim about visible stat-panel refresh.

- **Steps 11–13 named the shift counts, not the bits (corrected 2026-09-11, ASTRA-CONTRA-FABLE-RESULT-DISPATCH).**
  Each outgoing flag is `(A >> n) & mask`, and the input bit is `n + log2(mask)`, not `n`: target
  MP `shr 11, and 0x20` reads **bit 16**, `shr 8, not, and 0x10` reads **bit 12**; the source's
  HP reads **bits 5, 17, 9**; the source's MP **bits 11, 15**. Step 10 was already right. ASTRA's
  [EXP-060](../_experiments/EXP-060-result-numeric-dispatch.md) executed `00311608`–`00311777`
  in isolation over 22 fixtures with the five setters stubbed and rejects the shift-11-as-bit-11
  mutant. With [the copy-out's meanings](../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md)
  (§2.7) the mapping is uniform across the four calls: **the gain word present → setter bit 5
  (the direction of a zero delta), neither difference word present → setter bit 4 (the reaction
  suppressed)** — bits 10 / 6 for the target's HP, 16 / 12 for its MP, 9 / 5 for the source's HP,
  15 / 11 for its MP — and the target's HP alone adds `!`18 → 6 and 19 → 8; the source's HP adds
  `!`17 → 6, a bit the copy-out does not set. The setters' bit meanings are on
  [the HP write page](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)
  §2.1. Numeric `−1` is forwarded as a value when the presence bit is set; these fields have no
  absence guard of their own here. [EXP-062](../_experiments/EXP-062-mp-composition.md) re-runs
  this dispatch on a copy-out's real output and the native MP writers in one state (nine cases:
  a target gain of 30 takes MP 40 / secondary 80 → 70 / 110 / tier 1; the private `±1` multiplier
  adds or removes one maximum of the secondary word; a null source suppresses the source calls):
  boundary agreement under injected roles, not whole-action parity.

### What this page now claims, and does not

The applier's direct stores and control flow are described above. The five previously
undecoded callees now have bounded original-code evidence in
[EXP-148](../_experiments/EXP-148-apply-result-callees-exec.md), and
[EXP-149](../_experiments/EXP-149-apply-result-whole-exec.md) retains whole-applier
fixtures with real selected callees. SECTION-01 replayed their stored assertions and
added discriminating native controls; it did not rerun their full Unicorn suites.
The current contract keeps scripted callbacks, unexercised nested re-entry, and live
reachability open. Steal IDs/availability must still be tied to authored source where
that mapping has not already been established elsewhere.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **Items_Equipment_Shops_License — CLIENT, and one SERVICE.**
  - `GameState_GetGil` / `GameState_SetGil` are called by the gil-class inventory appliers
    (`InventoryEncodedGilClass0E_ApplyGilDelta`, `InventoryBundleClass09_ApplyGilAndNestedItems`) and by both shop commits.
  - `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`) is the one item write behind all of these:
    - the equipment counters;
    - the class-D purchase reset;
    - the bundle appliers `09`, `0A` and `0D`;
    - the temporary-equipment snapshot and restore;
    - `Inventory_GrantEncodedLootItem`;
    - the shop commits;
    - this page's steal, as a SERVICE edge from `003112F0`.

    The write itself asks `Inventory_QueryEncodedItemStateByClass`.
  - The recompute and the owner lookup are driven by the equipment-slot and licence-node setters.
- **Gameplay — SERVICE.**
  - The HP write finds the target in the battle target buffer (`BattleTargetBuffer_FindActorWorkIndex`) and dispatches a
    presentation event.
  - The status changer dispatches and updates the engagement flag.
  - The status modifier and the recompute ask the shared id-validity query, which is MECHANICAL
    ([shared neighbours](../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)).
- **Movement — CLIENT.** Two locomotion bodies look up stats owners through `BattleStats_FindOwningBattleUnit`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE and CLIENT, 86 edges.** The applier and the formula layer are one path:
  - `BattleFormula_ApplyTargetResult` calls 17 of the cited functions;
  - cited functions call `BattleStats_FindOwningBattleUnit` (8), `BattleStats_ModifySecondaryResource` (3), and `BattleStats_ModifyHPAndProcessLethalState` and `BattleStats_ModifyPrimaryResource` (2 each);
  - the reconcile and absolute-set bodies (`BattleStats_ReconcileResourcesToEffectiveCapacity`, `BattleStats_SetPrimaryResourceAbsolute`, `BattleStats_ReconcileCurrentHpToEffectiveMaximum`) call back into cited functions.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `0030E360` on this page calls `FUN_00300fc0`, owned by that layer. What it reaches is a 371-byte step whose whole first branch is skipped unless its second argument is zero and the stats record's `byte[+5]` is zero too; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — SERVICE.** `0030E130` on this page calls `GambitConfig_AdjustAvailableEntryCountByStatsDelta`, owned by that layer. What it reaches is the availability adjustment, and it fixes the ceiling: for each of **three** rows at a `0x34` stride it adds the delta to `byte[+0x5B42]` and **clamps the result to `0..0xC`** - the same twelve the enable mask carries; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CoreRuntimeScheduling — MECHANICAL (1 edge).** `BattleStats_ModifyHPAndProcessLethalState` `00300530` calls `GameClock_GetRawTickCounter` `0032A150`, a 7-byte getter of the raw game clock. On a lethal change the HP write divides that tick count by 30 times the frame multiplier and stores it at `+0xC` of the record the unit holds at `+0x6A0` (`00300805`–`00300829`) — a death timestamp — before it reports the death to the spawn group; the clock is read, not driven.

**Party — CLIENT (1 edge).** `00328BD0` calls `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`. `00328BD0` is a Party-filed stats-record initialiser (it writes the same `0xFFFF` / `0xFF` licence-board selector sentinels as `BattleStats_InitializeDefinitionRecord`) and finishes with the same recompute the apply's final guard runs; the crossing is that shared recompute, not a party route into result application.

**PlatformOnlineAchievements — SERVICE (6 edges).** `GameState_SetGil` `00254EE0` calls `AchievementCounter_UpdateAndMaybeFire` `00316A50`, which calls the counter updater `00315E90`, `003165C0`, `003166F0`, `00316BF0` and the 44-byte `008632B0`. The gil slot of the result record writes gil through the setter, and the setter feeds the gil-spent / gil-earned achievement counters (ids 6 or 7 by the sign of the delta); that is an achievement side effect of the write, not part of the decode.

**RNG_Random_Selection — SERVICE (1 edge).** Step slot 163 `0038F6F0` (recipe 99, the "gil bug" trap) calls `RNG_MT19937_NextU32_Thunk` `00379CD0`. The trap draws one value from the shared MT19937 stream (taken modulo the unit byte `+0x1C2`) before it writes the amount that the gil slot this page decodes deducts; the stream itself is the RNG layer's.

**Rewards_Progression_Economy — SERVICE and CLIENT (19 edges).** `BattleFormula_ApplyTargetResult` `003112F0` calls `GameState_GetGil` `00253690`, `GameState_SetGil` `00254EE0` and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650`; the getter and setter are also called by `GameState_AddGilClampedAndNotify` `003004B0`, `GameState_SetGilClampedNonnegative` `00300500` (setter only), `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` and the record applier `003F4AA0`, and `00312280`, like `00254EE0`, calls `AchievementCounter_UpdateAndMaybeFire` `00316A50`; `00312280` calls `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`; `0030C650` calls `BattleStats_FindOwningBattleUnit` `0031B860`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` and the sound pair `003A1180` / `002DF220`, and `0030FED0` is also called by the level setter `0030C470`; `Reward_ComputeExperienceForRecipient` `002F8BB0` calls `0031B860`. The apply shares the gil accessors and the level-advance routine with the rewards layer: slot 18's deduction is one of several gil writers, and a level result goes through the same advance-and-recompute the experience award uses.

**Script_VM_Native_Bridge — CLIENT (2 edges).** The verb body `00357040` calls `003A1180` and `002DF220`. That verb pops four arguments from the script value stack and plays a sound through the same resolve-then-play pair the apply's bit-14 block uses for sound `0x34`; the pair is shared, not a script route into the apply.

**Spawn_Encounter_Lifecycle — CLIENT (4 edges).** `Spawn_SetAllSpawnBackedUnitsCurrentHPZero` `002352E0` and `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` call `BattleStats_SetCurrentHP` `00300520`; `0023A410` also calls `0030FED0`; `00300530` calls `SpawnGroup_RecordMemberDeathAndHandleCompletion` `00306F00`. Spawn activation and the zero-all path set HP through the same writer the apply uses, and a lethal HP change reports the member's death to its spawn group — the group-completion bookkeeping is the spawn layer's.

**WorldAreaField — DEPENDENCY (2 edges).** `00300530` and `0030E360` call `FieldData_GetActiveFieldRecordBit15` `00377C20`. Both the HP write and the status change ask the current field record's bit 15 (the per-area bit that keeps terminal-status units), so what a lethal or terminal result does depends on the field.
