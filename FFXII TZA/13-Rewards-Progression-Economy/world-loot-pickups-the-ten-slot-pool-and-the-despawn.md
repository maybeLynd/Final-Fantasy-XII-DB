---
system: World loot pickups — the ten-slot pool, the blink and the despawn
category: 13-Rewards-Progression-Economy
status: AUDITED
owner_layer: PrimaryOwner:Rewards_Progression_Economy
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `002C7660`, `003FBE90`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-07
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-world-loot-pickups-pass-1
  crossref_clean: false
  reopened_count: 0
---

# World loot pickups — the ten-slot pool, the blink and the despawn

> The shiny thing a dead Marlboro leaves on the ground. **Only ten can exist at once**, an eleventh
> drop destroys the oldest, and every one of them blinks five times and vanishes on a fixed timer.

## 1. What the player sees

Kill something and it may leave loot on the ground — a small glinting object you walk over to pick
up. Three things about it are engine behaviour rather than chance, and all three are visible in
ordinary play:

**It does not wait for you.** A pickup has a fixed lifetime from the moment it appears. Near the end
it starts **blinking**, five times, and then it is gone. Walk back for it after a long fight and it
will not be there.

**Some glint differently.** The engine sorts every pickup into one of **three presentation tiers**
before it is created, by looking at what is actually inside it — so the shine is not decoration, it
is a readable signal about whether the drop is worth the walk.

**And the ground can be full.** The game keeps **exactly ten** loot pickups in the world. If a
fight produces an eleventh while ten are still lying there, the engine does not queue it or drop
it — **it destroys the oldest pickup still on the ground and reuses its slot.** In a long chain
fight in a crowded room, loot you have not collected is being deleted behind you, oldest first.

Everything a single pickup holds — up to **seven** separate item stacks — is granted at once when
you touch it.

## 2. Native mechanism

### The pool

`g_aWorldLootPickupNodes` is a **fixed array of ten nodes, stride `0x60` bytes**. Both bounds are
literal in `Loot_CreateWorldPickup` (`00319CA0`): the scan increments a counter and tests
`iVar4 < 10`, and the node pointer advances by `0x18` dwords per step.

Nodes are threaded onto a **doubly-linked active list** with `g_pWorldLootPickupListHead` and
`g_pWorldLootPickupListTail`; `+0x10` is the previous pointer and `+0x18` the next. A node is free
when its state word at `+0x04` is `0`.

| node offset | meaning |
|---|---|
| `+0x00` | pool slot index (0–9), used as the key into the presence table |
| `+0x04` | lifecycle state, `0` = free |
| `+0x08` | the clock stamp taken when the pickup materialised |
| `+0x10` | previous node |
| `+0x18` | next node |
| `+0x20 … +0x57` | **seven** drop entries, `{u16 item_id, u32 quantity}` |
| `+0x58` | the world object handle |

### Creation, and the eviction that a player can actually notice

`Loot_CreateWorldPickup(drop_buffer, position_xyz)` scans for a node with state `0`. **If all ten
are in use it takes the list head** — the oldest — and retires it in place:

```
unlink head from the active list
FUN_0028f000(handle, 5, …)      /* presentation op 5 — destroyed to make room */
LootPresence_ClearSlot(node[+0x00])
zero state, stamp, both links, handle
```

then reuses that node for the new drop. **No drop is ever refused; an existing pickup is always
sacrificed instead.**

### The lifecycle, with its exact arithmetic

`Loot_UpdateWorldPickupLifetimeAndDespawn` (`00319600`) runs once per field frame and walks the
active list. Two constants drive all of it:

```
DAT_01CEBCAC = -30.0f      (.rdata, immutable)
DAT_01DFE0B8 =   1.0f      (.data,  a runtime scalar — default 1.0)
step = (int)(DAT_01DFE0B8 * DAT_01CEBCAC) = -30
now  = DAT_0208D45C        (the field clock; BSS, so zero at image load)
```

**State 1 — waiting to materialise.** When the world object reports ready
(`FUN_0028efe0(handle) == 2`), the node stamps `now`, moves to **state 2**, reads the object's
position and publishes it with `LootPresence_PublishSlotPosition(slot, pos)`.

**States 2–6 — the blink.** Each step fires when

```
stamp − step × (0x3C − (7 − state)) ≤ now
   i.e.  stamp + 30 × (60 − (7 − state)) ≤ now
```

giving five thresholds, thirty clock units apart:

| state | fires at | presentation call |
|---:|---|---|
| 2 → 3 | `stamp + 1650` | `FUN_0028f000(handle, 2, {5})` |
| 3 → 4 | `stamp + 1680` | `… {4}` |
| 4 → 5 | `stamp + 1710` | `… {3}` |
| 5 → 6 | `stamp + 1740` | `… {2}` |
| 6 → 7 | `stamp + 1770` | `… {1}` |

The argument passed to the presentation layer is `7 − state`, so it counts **5, 4, 3, 2, 1** —
a countdown the renderer turns into the blink.

**State 7 — expiry.** Fires when

```
stamp + step × (−0x3C) ≤ now    i.e.  stamp + 30 × 60 = stamp + 1800 ≤ now
```

and then unlinks the node, calls `FUN_0028f000(handle, 4, …)`, clears the presence slot and zeroes
the node.

> **Total lifetime is `1800` clock units, and the blink occupies the last `150` of them** — five
> equal steps of 30. The whole ladder is `60 × 30` with the last five thirties spent blinking.

**The clock counts frames, and the lifetime is sixty seconds — settled 2026-09-07, one block after
this document was written.** `DAT_01DFE0B8` is one of a **triple of frame-rate scalars**
(`01DFE0B4` int, `01DFE0B8`, `01DFE0BC` float) written by exactly one function, `FUN_001EDDC0`, which
gates on its own parameter:

```asm
001EDDC4  test  ecx, ecx
001EDDC6  je    0x1EDE1F              ; zero -> skip, .data defaults (1, 1.0, 1.0) stand
001EDDC8  movss xmm0, 2.0
001EDDD0  movss xmm1, 0.5
001EDDD8  movss [01DFE0B8], xmm0      ; 2.0
001EDDE0  movss [01DFE0BC], xmm1      ; 0.5
001EDDF2  mov   dword [01DFE0B4], 2
```

**And the caller is now read, 2026-09-07** — found by an independent audit after this document had
recorded *"non-zero `ecx`"* as an inference from the constants:

```c
0022BDF0 (146 B, CoreRuntimeScheduling):    /* the command-line parser */
    iVar1 = FUN_0017D8F0();                 /* 11 B: *(u32 *)(*(void **)0x01F82D20 + 0x48) */
    FUN_001EDDC0(iVar1 == 1);
```

**`0x01F82D20` is the `GameSetting.ini` singleton and `+0x48` is `FrameLimit`**, settings index 18,
already documented at
[`../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md).
**The scalar is selected by a named user setting read out of the ini**, not by an unknown.

> ⚠ **The gate is `FrameLimit == 1`, not "non-zero".** This document said non-zero. **Any other value
> takes the other branch and leaves the defaults** — so if `FrameLimit` is a three-state enum, the
> original phrasing was wrong for every state above 1.

The other branch is **not** inert: it raises the Windows multimedia timer resolution via
`timeBeginPeriod`, which the `== 1` branch releases with `timeEndPeriod`. **A lower-rate mode needing
finer OS timer granularity is independent corroboration that these are two frame-pacing modes.**

So the step is `(int)(scalar × −30.0)` = **−30** on the default path and **−60** when
`FrameLimit == 1`, and the lifetime is **1800 frames or 3600 frames** — **the same wall-clock
duration either way, because the scalar exists precisely to hold it constant.**

> **What is still not established: that `FrameLimit == 1` means 60 rather than 30.** The scalars are
> unambiguously **twice the base rate** against `.data` defaults of `(1, 1.0, 1.0)`, but **the base
> rate itself is not read here.** The sixty-second figure therefore rests on the base being 30 —
> which is consistent with a PS2-derived engine and with ordinary play, and is **not proven**.
> `CM-7`.
>
> **CM-7 answered 2026-09-12 (FABLE), by reconciliation with the settings pages written after this
> note.** `FrameLimit` is stored as an **index into the value table `30, 60`** — `FrameLimit=60`
> stores as `1`, `FrameLimit=30` as `0` — and the runtime reduces it to the boolean "exactly 1"
> ([the settings contract](../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md)
> §10–11 and its "stores as `1`" note). The `1` arm is the only writer of the time base: `001EDDC0`
> stores `2` at `01DFE0B4` and the `2.0 / 0.5` pair at `01DFE0B8` / `01DFE0BC` (`001EDDD8`–`001EDDF2`),
> sets the 60 Hz gate `01F82E38` and releases the multimedia timer; on `0` nothing is written and
> the linker's `{1, 1.0, 1.0}` stands while `timeBeginPeriod` is raised
> ([the ini page](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
> "at 30 fps the engine writes nothing at all"). So **`FrameLimit == 1` is the 60 fps choice and the
> base is the 30 fps rate the PS2 timings were authored in**: the −30 step is the 30 fps path, the
> −60 step the 60 fps path, and the sixty-second lifetime holds in both. That the tick at index 0
> is 30 Hz rests on the option's own value table and the doubling scalars, not on a read of the
> limiter's period — which is the settings contract's ground, not this page's.

### Collection

`Loot_CollectWorldPickupAndGrantInventory(node, collector_field_id)` grants **all seven** entries,
skipping any whose item id is `0xFFFF`:

```c
for (i = 0; i < 7; i++)
    if (entry[i].item_id != 0xFFFF)
        Inventory_GrantEncodedLootItem(entry[i].item_id, entry[i].quantity, 1);
```

It then bumps a counter at `DAT_022C3174`, unlinks the node, calls
`FUN_0028f000(handle, 3, {collector_field_id})` and ~~zeroes the node~~ resets four fields of it.
**`0xFFFF` is the empty-entry sentinel**, consistent with the all-ones convention this database
records elsewhere.

**The exact order and extent, read 2026-09-11 (ASTRA-REQ-FABLE-LOOT-COLLECTION):**
`Loot_CollectWorldPickupAndGrantInventory` (`00319920`) walks the seven entries at `+0x20` (stride
8, `00319950`–`00319972`) and **skips only an id of `0xFFFF` — an interior sentinel does not stop
the walk**; every other id, including `0`, goes to `Inventory_GrantEncodedLootItem(id, quantity, 1)`
(`00300B80`) with the raw dword quantity. Only after the seventh entry: the counter `022C3174`
increments (`00319974`, even when all seven were empty), the node is unlinked (previous `+0x18`
or the list head `02EC1360` takes `next`; next `+0x10` or the tail `02EC1368` takes `previous`,
`0031997A`–`003199A7`), presentation opcode `3` is posted on the node's handle `+0x58`
(`003199AE`–`003199BF`), the presence byte is cleared (`LootPresence_ClearSlot` `002FB2A0`, slots
0–9 only, `003199C4`), and then **exactly four fields are zeroed: the qword at `+0x04` (state and
timestamp), `+0x18`, `+0x10` and the dword `+0x58`** (`003199DC`–`003199E8`). The slot `+0x00`,
the seven entries at `+0x20`–`+0x57` and the padding survive — stale bytes, not live loot.
`Loot_RemoveWorldPickupWithoutInventoryGrant` (`003197B0`) is the same retirement without the
grants and without the counter (`003197B9`–`00319818`). **Neither routine guards against a
repeat**: a retired node passed in again unlinks nothing new but repeats the grants and the
counter increment — the caller's checks are the only gate. ASTRA's
[EXP-055](../_experiments/EXP-055-loot-collection-effects.md) executed the three bodies in
isolation over synthetic lists with the inventory and presentation callees stubbed (eight cases;
omitting the seventh entry detected); the reading above is the static tier, and what the grant
and the presentation do natively is not claimed by either.

### Finding the nearest pickup — `Loot_FindNearestActivePickupPosition` (`00319850`), read 2026-09-11

`Loot_FindNearestActivePickupPosition(actor, out16)` walks the pickup list from its root at
`02EC1360` through each node's `+0x18` link (`00319870`, `003198E8`) — **list order, not pool
index**. For every node it hands the node's slot dword to `LootPresence_GetSlotPosition`
(`002FB310`): `022BE7F0 + slot × 0x20`, byte `+0` non-zero means present, and the 16 bytes at
`+0x10` are copied out (`002FB31E`–`002FB331`; no bounds check on the slot). A present slot's XYZ
goes through `Vector3_ComputeSquaredXZDistance` (`003A1960`) against the actor's position at
`+0xE0` — **Y does not take part** — and a candidate replaces the best only when its squared
distance is **strictly below** the running ceiling (`comiss` / `jbe` at `003198D5`–`003198D8`):
equal distances keep the earlier node, an unordered compare skips. The ceiling starts from the
float at `02F973B8` (`0031987A`), which is written once, by `BattleStorage_InitializeWorkArrays`
(`002368F0`) from the constant at `00914700` — **`+inf`** — so the walk has no radius: it returns
the nearest present pickup of any distance, the slot in `eax`, `-1` when none is present. The
16-byte store into `out` (`003198E2`) is the `movaps` of a stack vector whose first three floats
were built from the presence entry (`003198B8`–`003198CA`); **its fourth word is whatever the
stack held**. A caller must give it 16 bytes and must not read the fourth lane. The same `+inf`
word is the AI target selector's initial ceiling (`00301BDB`, `0030276D`, `00308882`).

ASTRA's [EXP-052](../_experiments/EXP-052-loot-pickup-selection.md) executed the three bodies in
isolation over synthetic lists (eleven cases, the tie branch mutated and detected) with only the
security-cookie callee controlled; the reading above is the static tier. The radius test the
player experiences belongs to the overlap collector `Loot_FindOverlappingPickupIndex` (`002FB150`),
still unread (`CM-5`).

### Finding the pickup under foot — `Loot_FindOverlappingPickupIndex` (`002FB150`), read 2026-09-11

`Loot_FindOverlappingPickupIndex(unit, extra)` is the radius test the nearest selector lacks. A null
unit returns `-1` (`002FB170`–`002FB178`). Otherwise it takes the unit's actor (`[unit+0x10]`),
reads its position through `Actor_GetWorldPosition` (`00265020`, `002FB1A0`; the vector's fourth
lane is set to the constant `1.0` at `01CEBBA8`, `002FB1A5`–`002FB1BB`) and its two radii through
`ActorRuntime_GetClass3FloatPair` (`00265090`, `002FB1C1`) — **a getter that writes its pair only
for a kind-3 actor** (`00265090`–`00265098`: `packed_03 & 0xE0 == 0x60`, then the movement
context's `+0x50` / `+0x54` copied by `003DA710`); for any other kind the two stack floats are
whatever the stack held. Then the **ten presence slots in index order** (`022BE7F0 + i × 0x20`,
byte `+0` present, position at `+0x10`; `002FB1CD`–`002FB217`): the first present slot whose XZ
distance from the actor (`Vector3_ComputeXZDistance` `004686D0`, a `sqrtf`) is **strictly less
than `max(r1, r2) + extra`** (`maxss` `002FB1F0`, `addss` `002FB205`, `comiss` / `ja`
`002FB209`–`002FB20C`) is returned; none → `-1`. So collection is *first-in-slot-order within the
actor's own radius plus the caller's margin*, not nearest — the two selectors answer different
questions, and neither has a caller in the function graph (`CM-5`'s residue).

ASTRA's [EXP-053](../_experiments/EXP-053-loot-overlap-controls.md) executed the six bodies in
isolation with `sqrtf` and the cookie check controlled — eleven cases, the equality mutant detected,
kind-1 fixtures changing the result with the stack residue — which is the isolated tier beside
this reading; nothing live is claimed.

### Who runs the collector — `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`), read 2026-09-11

The overlap collector has exactly one direct caller in the image, inside the periodic maintenance
at `003110DC`–`00311141` (ASTRA's EXP-054 found it by a raw `E8` scan; the function graph has no
edge for it). The unit qualifies when its cached handle `+0x08` **is the current focus**
(`PartyFocus_IsCurrentPackedActorHandle` `003273B0`, `003110DC`–`003110E6`) **or its committed
action `+0x714` is `0x4165`** (`003110E8`–`003110F4`). Then `Loot_FindOverlappingPickupIndex(unit,
1.0)` — the extra radius is the constant at `01CEBBA8` (`003110FA`–`00311105`) — and a negative
result skips everything (`0031110E`). A found slot is kept in `ebx`; `00469E30` runs on the unit's
stats record (`00311114`–`0031111B`); then the stats pointer is **re-read** (`00311120`): a null
record, or a record whose kind byte `+0x05` is not 0 (not a party record), goes to
`Loot_RemoveWorldPickupByIndexWithoutGrant` (`00319830`, `0031127F`) — the pickup vanishes without
an inventory grant; a party record goes to `Loot_CollectWorldPickupByIndex` (`00319A00`,
`00311141`). Both get `ecx` = the slot and `edx` = the unit's handle. So **a non-party unit that
walks over loot destroys it**, and the party collects it — the same test, two dispatches.

EXP-054 executed the segment with a synthetic unit and stopped before either dispatch (nine
cases, the kind branch mutated and detected); isolated execution, no live claim. Whether every
unit that reaches the collector has a kind-3 actor — the precondition the radius getter needs
(above) — is **not established** by this caller: the focus test and the action test say nothing
about the actor's kind (`CM-6`).

### The presentation opcode set

All six ops of the dispatcher `0028F000` are fixed — four by their call sites on this page, the
other two by the dispatcher's six-entry table at `0028F09C` (read 2026-09-12, FABLE). The
dispatcher resolves the world-object manager `[0209BE80] + 0x57E0` and jumps on `op − 1`; **there
is no op 0** — anything outside 1–6 returns 0 untouched (`0028F017`–`0028F01D`, `0028F094`).

| op | meaning | behind the table |
|---:|---|---|
| 1 | **create** — posted by `Loot_CreateWorldPickup` itself at `00319DF9`–`00319E00` with a `0x18`-byte block `{x, y, z of the drop position, 1.0f, tier from 00319A20, `01EED3A8[022C3158]` — the **chain rank remapped through a four-entry table**, not the rank itself: `00319DD4` loads the selector, `00319DDB` bounds it with `cmp eax, 3` / `ja` to `0` (`ebp`), and `00319DE0`–`00319DE7` `lea`s `01EED3A8` and reads `[rcx + rax*4]`. **The table ships identity** — `{0, 1, 2, 3}`, with the `cmp eax, 3` agreeing that four entries is its whole width — so every shipped byte gives the same answer as the passthrough this row previously recorded, and the indirection is invisible unless the body is read. Corrected 2026-09-21 (OPUS) against ASTRA's EXP-141 return, which had it right. The selector is the enemy chain rank of [loot-drops-and-enemy-chain](loot-drops-and-enemy-chain.md)}`; the result is the node's `+0x58` | `003FA160(manager, block, tier, word)`: the first of **13** records of stride `0x2A0` from `manager + 0x270` whose `+0x272` bit 0 is clear (none → 0) is zeroed, flagged 1, given `+0x260 = 1`, `+0x264 = −0.25f`, `+0x268` the tier, `+0x26C` the word, placed (`0026E350`, `00202C90` ×2, `003FBE90`), appended to the manager's list at `+0x2490` (`+0x278` next, `+0x280` prev), audio cue `0x50` (`00249C60`) is played and the record's address is returned; on first use (`manager + 0x2690` null) it loads the resources `partytop_4_c` and `partytop_8_c` (`0024A5A0`) |
| 2 | blink step, argument `7 − state` counting 5 → 1 | `003FAA10(record, step)` |
| 3 | collected, argument the collecting character's field id | `003FA820(record, fieldId)` |
| 4 | expired on the timer | `003FA820(record, 0)` |
| 5 | destroyed to free a slot for a newer drop | `003FA820(record, 0)` — **the same call as op 4**: at the world object, expiry and eviction are one thing |
| 6 | end every live record in the manager's list | `003FA900(manager)` — the op-4 body over the `+0x2490` list; called only by the dispatcher's own op-6 arm (`0028F088`–`0028F08F`), and **none of the dispatcher's six call sites passes op 6** (`Loot_CreateWorldPickup` 1 / 5, `Loot_UpdateWorldPickupLifetimeAndDespawn` 2 / 4, the two collect / remove paths 3 — raw `E8` index, 2026-09-12) — so the op, not the function, is unreached |

`003FA820` (`003FA820`–`003FA8E6`) on a record with bit 0 set and bit 1 clear: sets bit 1; when
the record's bit 3 is set or a collector is given, sets bits 6 and 8 and writes a phase word at
`+0x28C` from `sinf` of the global counter `0208F570`; a collector additionally swaps bit 6 for
bit 7, plays audio cue `0x46`, and is stored at `+0x290` (`+0x294 = 0`). **The handle is the
record's address truncated to 32 bits** — `00319E05` keeps `eax` in the dword `+0x58`, and every
op site (`003196BC`, `0031971A`, `003197ED`, `003199AE`) and the dispatcher (`0028F009`,
`0028F053`) zero-extend it back — so the manager must live below 4 GB, the same property [the field-record table page](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
records for the resource arena (`PROPOSED-repos2d-4`).

### The three presentation tiers

`Loot_DeriveWorldPickupPresentationTier(drop_buffer)` (`00319A20`) runs over the **same seven
entries** before the pickup exists and returns `0`, `1` or `2` — **lower is better**:

```c
tier = 2;
for (i = 0; i < 7; i++) {
    id = entry[i].item_id;
    if (id == 0xFFFF)            continue;
    if ((id & 0xF000) != 0x1000) continue;        /* only item class 1 is considered */
    row = table(0x02EBF0F8).base + table.stride * (id - 0x1000);
    cat = BattleDefinition_MapByte9ToRuntimeCategory(row);
    if (cat > 0 && cat < 6) return 0;             /* best tier, decided immediately */
    if (cat == 6)            tier = 1;
}
return tier;
```

**The encoded item id carries its own table row**: the top nibble `0x1000` selects the class and the
low twelve bits are the row index into the definition table at registry slot **`0x02EBF0F8`**. Only
class-1 ids are inspected at all — an entry of any other class cannot raise the tier.

**Tier 0 short-circuits.** The moment one class-1 entry maps to runtime category 1–5 the loop
returns, so a pickup shows its best contents, not an average.

## 3. Key addresses

| address | name | size |
|---|---|---:|
| `00319B10` | `Loot_InitializeWorldPickupPool` | 387 B |
| `00319CA0` | `Loot_CreateWorldPickup` | 394 B |
| `00319600` | `Loot_UpdateWorldPickupLifetimeAndDespawn` | 423 B |
| `00319920` | `Loot_CollectWorldPickupAndGrantInventory` | 215 B |
| `00319A00` | `Loot_CollectWorldPickupByIndex` | 26 B |
| `00319A20` | `Loot_DeriveWorldPickupPresentationTier` | 227 B |
| `00319850` | `Loot_FindNearestActivePickupPosition` | 197 B — read (§2) |
| `002FB150` | `Loot_FindOverlappingPickupIndex` | 253 B — read (§2); one caller, `00310DB0` at `00311105` |
| `00265090` | `ActorRuntime_GetClass3FloatPair` | 27 B — the radius pair, kind 3 only |
| `004686D0` | `Vector3_ComputeXZDistance` | 35 B — the overlap distance |
| `002FB310` | `LootPresence_GetSlotPosition` | 38 B — its presence leaf |
| `003A1960` | `Vector3_ComputeSquaredXZDistance` | 31 B — its distance leaf |
| `003197B0` | `Loot_RemoveWorldPickupWithoutInventoryGrant` | 113 B |
| `00319830` | `Loot_RemoveWorldPickupByIndexWithoutGrant` | 26 B |
| `002FB150` | `Loot_FindOverlappingPickupIndex` | 253 B |

| data | meaning |
|---|---|
| `01CEBCAC` | `-30.0f`, the lifetime step |
| `01DFE0B8` | `1.0f`, runtime scalar multiplying it |
| `0208D45C` | the field clock (BSS) |
| `022C3174` | pickups-collected counter |
| `02EBF0F8` | item/equipment definition table (registry slot 30) |

## 4. Modding notes

- **Ten is a hard cap and it is a literal.** Raising it needs both the `iVar4 < 10` bound in
  `Loot_CreateWorldPickup` and the pool allocation in `Loot_InitializeWorldPickupPool`. Raising one
  without the other walks off the end of a `0x60`-stride array.
- ⚠ **`01DFE0B8` is NOT a loot knob, and this note said it was.** It is the **60 fps frame-rate
  scalar**, one of a triple read **438 times** across the image (`01DFE0B4` 211, `01DFE0B8` 45,
  `01DFE0BC` 182) and written once at startup. Changing it to lengthen loot **rescales every timed
  system in the game at once.** The original wording — *"the single cheapest lever on this system,
  one float, no code change"* — was true about the arithmetic and badly wrong about the consequence.
  **To change loot lifetime alone, edit the `0x3C` and the `-30.0f` in the ladder, not the scalar.**
- **A pickup holds seven stacks, not one.** Any tool that writes a drop buffer must fill or
  `0xFFFF`-terminate all seven; a stale eighth entry is not read, and an unset middle entry that is
  not `0xFFFF` **will be granted**.
- **The tier is computed before creation and never revisited.** Changing an item's runtime category
  changes the shine of future drops only.
- **Eviction is silent.** Nothing signals that an uncollected pickup was destroyed to make room; it
  simply receives presentation op 5 instead of op 4.

## 5. What is not known

- [x] ~~The unit of the field clock `0208D45C`.~~ **ANSWERED 2026-09-07 — frames.** 1800 at 30 fps,
  3600 at 60 fps, sixty seconds either way. `CM-1`.
- [x] ~~What `01DFE0B8` actually is.~~ **ANSWERED 2026-09-07 — the 60 fps frame-rate scalar**, not the
  `Speed1/2/3` game-speed toggle. **That lead was wrong**, and it was published as a lead rather than
  a finding, which is the only reason it cost nothing. `CM-2`.
- [x] ~~**`BattleDefinition_MapByte9ToRuntimeCategory`'s categories 1–6** in player terms.~~
  **CM-3 ANSWERED 2026-09-12 (FABLE):** the equipment row's `+0x09` is its **equipment class**
  (27 values), and the mapper folds them into nine runtime categories through a 27-byte index
  table at `0031EA74` and a nine-arm jump table at `0031EA50` (`0031E9F0`–`0031EA4C`):
  **1** unarmed and the reserve rows, **2** the one-handed weapons that take a shield (swords,
  axes, hammers, daggers, maces, measures), **3** the two-handed and mage weapons (greatswords,
  katana, ninja swords, spears, poles, rods, staves), **4** the ammunition weapons (bows,
  crossbows, guns, hand-bombs), **5** the ammunition itself (arrows, bolts, shot, bombs),
  **6** shields, **7** helmets, **8** armor, **9** accessories and the special six. So the loot
  shine's best tier is *any weapon or ammunition*, the middle tier *a shield*, and head, body and
  accessory drops show the default. The class-by-class table with the bank-1 names is on
  [the id-encoding page](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md) §11 (P-2).
- [x] ~~The remaining presentation op — op `1` or `0` — is not exercised by any path read here.~~
  **ANSWERED 2026-09-12 (FABLE)** — "The presentation opcode set": there is no op 0, op 1 is the
  creation this page's own `Loot_CreateWorldPickup` posts at `00319E00`, ops 4 and 5 are one call,
  and op 6 (end every record) has no static caller.
- [x] **UQ-137.** **Live:** the 32-bit handle at node `+0x58` requires the world-object manager *(closed — the register row is WITHDRAWN.)*
  `[0209BE80]` to sit below 4 GB; the image cannot show where it is allocated (queued, live
  automation paused).
- [x] ~~`Loot_FindOverlappingPickupIndex` (`002FB150`) and `Loot_FindNearestActivePickupPosition`
  (`00319850`) are named and not read~~ — **`CM-5` ANSWERED 2026-09-11** (§2, the two "Finding"
  sections): the overlap test is first-in-slot-order within `max(r1, r2) + extra` by XZ distance,
  the radii from a kind-3 actor's movement context; the nearest selector is list order, strictly
  nearest, no radius. The overlap collector's one caller is the periodic maintenance (§2, "Who runs
  the collector"); the nearest selector still has none in the function graph. *(Corrected 2026-09-23, SWE2-CONTRACT:
  the graph missed an edge — `BattleLocomotion_DecodeOrderGoal` (`00312730`) calls it at
  `003129AF` on order-goal opcode `0x4165`, passing the unit and a position out-pointer; that is the
  selector's one static caller.)*
- [x] ~~**Is every unit that reaches the collector backed by a kind-3 actor?**~~ **CM-6 ANSWERED
  2026-09-12 (FABLE): yes, by construction — and it matters, because the collector never
  initialises the pair.** `Loot_FindOverlappingPickupIndex` writes nothing to its two radius slots
  before `ActorRuntime_GetClass3FloatPair` (`002FB17D`–`002FB1C1`: the position triple goes to
  `+0x30`–`+0x38`, the extra radius to `+0x3C`), and the getter returns without writing for any actor
  whose byte `+3` is not `0x60`-class (`00265090`–`002650AA`) — so a non-kind-3 actor would compare
  stack garbage. It cannot happen: every battle unit's `actorWork` ([the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) `+0x010`) is
  stored once, by `BattleUnit_AllocateSlotAndBindActor` (`002344EF`), whose one caller
  `ActorSystem_BindBattleUnitsForEligibleRecords` binds only records whose `flags14` carries bit 7
  (`00265A83`–`00265A89`, [the slot-pool page](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md)), and that bit is set in exactly two arms of the
  record initialiser's sequence switch — sequence 5 (`00266C19`–`00266C1F`) and sequence 7
  (`00266C24`) — which the kind table at `01E0C328` pairs with kind 3 ([the actor storage record map](../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md) `+0x014`).
  Both gates therefore see kind-3 actors: the current focus is a bound unit, and a unit carrying
  action `0x4165` is a bound unit. The literal `0x4165` occurs once in `.text` (a byte scan for
  every `mov r32` / `cmp` form: only `003110E8`); it lies in the extended commit block
  `0x4000`–`0x4166` whose contents [the commit page](../07-Combat-Action/the-moment-an-action-is-committed.md) leaves open, so *which* units commit it is
  data-driven and not enumerable here.

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| Ten-node pool, `0x60` stride | literal `iVar4 < 10` and `+0x18` dword step in `00319CA0` | 1 |
| Eleventh drop evicts the list head | complete eviction block in `00319CA0`, op 5 | 1 |
| Blink thresholds 1650/1680/1710/1740/1770, expiry 1800 | the state ladder in `00319600` with `-30.0f` at `01CEBCAC` and `1.0f` at `01DFE0B8`, both read from the image | 1 |
| Blink argument counts 5 → 1 | `7 − state` passed to op 2 | 1 |
| Seven drop entries | loop bounds in both `00319920` and `00319A20` | 1 |
| `0xFFFF` is the empty sentinel | skip tests in both loops | 1 |
| Tier 0 short-circuits on category 1–5 | early `return 0` in `00319A20` | 1 |
| The nine runtime categories and the 27 equipment classes behind them | `0031E9F0` read whole; the index bytes at `0031EA74` and the jump table at `0031EA50` dumped; `+0x09` histogrammed over all 557 rows of the equipment table (`battle_pack.bin` directory entry `+0x38`, `st2e`, stride 52) and every class's names resolved through text bank 1 (2026-09-12) | 1 |
| Low 12 bits of the item id are the table row | `stride × (id − 0x1000) + base` in `00319A20` | 1 |
| The clock counts frames; 1800 @30 fps = 3600 @60 fps = 60 s | complete disassembly of `FUN_001EDDC0`: `test ecx,ecx` gating a write of `2.0`/`0.5` over `.data` defaults of `1.0`/`1.0`; the scalar multiplies the `-30.0f` step | 1 |

## 7. Related

- [`loot-drops-and-enemy-chain.md`](loot-drops-and-enemy-chain.md) — **what** a kill drops. This
  document covers what happens to it once it is on the ground; the two meet at the drop buffer.
- [`../12-Items-Equipment-Shops-License/`](../12-Items-Equipment-Shops-License/) — the definition
  table at `02EBF0F8` the tier test reads.
- [`../00-Engine-Core-Runtime/the-all-ones-empty-convention.md`](../00-Engine-Core-Runtime/the-all-ones-empty-convention.md)
  — the `0xFFFF` sentinel.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

I came to this page expecting to correct it, because I had spent the morning publishing — and then
retracting — the claim that `01DFE0B8`'s neighbour `01DFE0B4` was "a tuning slot currently set to
unity". **This page had the whole thing right, and in more detail than my retraction did.** The
frame-rate triple, its single writer, the `.data` defaults, the `FrameLimit` gate and `CM-7`'s answer
are all here. Nothing in it needed correcting.

| claim | measured |
|---|---|
| the fourteen stated body sizes in §3 | **14 of 14 exact** |
| ten nodes, bound literal in `00319CA0` | **`cmp eax, 0xa` — and it appears twice**, once per scan arm |
| stride `0x60` | `00319CCC add rbx, 0x60` — a **byte** add of 0x60, which is §2's "`0x18` dwords" as the decompiler renders it |
| the seven drop entries fill `+0x20`–`+0x57` | 7 × 8 = 0x38, and `0x20 + 0x38 = 0x58` — the handle's offset, so the span closes exactly |
| `01CEBCAC` = `−30.0f`, `01CEBC08` = `2.0f`, `01CEBB70` = `0.5f` | exact, all three in `.rdata` |
| `.data` defaults `(1, 1.0f, 1.0f)` | exact, and **initialised in the file** — the RVAs lie inside `.data`'s `SizeOfRawData`, so these are linker values, not zeroed BSS |
| the five blink thresholds and the expiry | **re-derived from the instructions**: `r8d = 7 − state`, `eax = 0x3C − r8d`, `imul ecx, eax` → `stamp + 30 × (53 + state)` = **1650, 1680, 1710, 1740, 1770**, and `00319674 imul ecx, eax, 0x3c` → **1800** |

### What the page did not have: how widely the triple is read

§ says the three scalars are "written by exactly one function". Measured across every body in
`functions.tsv`, that is right — **one writer instruction each** — and the readership is the part
worth adding:

| slot | `.data` | on the `FrameLimit == 1` arm | references | writers |
|---|---|---|---:|---:|
| `01DFE0B4` | `1` (int) | `2` | **212** | **1** (`001EDDF2`) |
| `01DFE0B8` | `1.0f` | `2.0f` | **46** | **1** (`001EDDD8`) |
| `01DFE0BC` | `1.0f` | `0.5f` | **183** | **1** (`001EDDE0`) |

**441 references, three writer instructions.** That is the number a modder needs: these are not three
local constants but a time base the whole image reads, and `01DFE0BC` — the *reciprocal* arm, 0.5 at
60 fps — has 183 readers of its own, four times `01DFE0B8`'s.

### The same triple reaches at least four subsystems

This page proves the loot lifetime. Three more consumers were read elsewhere today, all on
`01DFE0B4`:

- the **status beat timer** — `003876D0`, definition `+9` × base × 30
  ([the status write](../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2.4a);
- the **periodic drain beat** — `00385CA0`, `base × 30 / 3` = base × 10 ticks
  ([the periodic tick](../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md) §5);
- the **battle-message dedup window** — `0046ABE6 imul ecx, [01DFE0B4], 0x1c2`
  ([the post-result events](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2.3).

So §'s sentence *"the scalar exists precisely to hold [the wall-clock duration] constant"* is not a
loot-local observation: **it is the engine's general answer to frame rate**, and the loot despawn is
one of at least four authored durations riding it.

**Not claimed:** nothing here was executed or observed live. The presentation opcodes, the collection
path and the three tiers were not re-read; `CM-7`'s residue — that index 0 is 30 Hz rests on the
option's value table rather than on a read of the limiter's period — stands exactly as § states it.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Platform — CLIENT, not read.** An 11-byte function this page cites is called by a 1,170-byte Platform-labelled body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleTarget_ComputeSurfaceDistanceBetweenUnits`, owned by that layer, calls `004686D0` on this page. That caller is the two-unit form of the same measurement, with **both** radii taken off the centre-to-centre distance and the result floored at zero; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleFormula_AppendStatusAddOperation`, owned by that layer, calls `003876D0` on this page. That caller is the status-add append: it takes both a `4`-byte and a `2`-byte view of the same index into the caller's `[+0x10]` buffer, and gates on the `0x80000003` bits of `dword[+8]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (61 edges through 4 of this page's functions).** The UI layer reaches this page at `00249C60`, `00202C90`, `0024A5A0`, `00265020`. `FUN_002c7660` is the worked example, read in full - it is a 1,190-byte routine in a `0xD8`-byte frame with a stack cookie and one preserved SSE register; **2 of the 55 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Most of these edges come from shared accessors and math leaves this page cites for the pickup code (the position and radius getters, the focus-handle pair, the XZ distance leaves, the matrix helpers of the visual constructor) and from bodies cited only as callers in the appended interior notes; their other callers are counted here, not read.*

**ActorEntity — SERVICE and CLIENT (36 edges).** The overlap collector `Loot_FindOverlappingPickupIndex` (`002FB150`) calls `Actor_GetWorldPosition` (`00265020`) and `ActorRuntime_GetClass3FloatPair` (`00265090`) for the unit's position and two radii; the maintenance runner `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) calls `BattleUnit_FindByCombatantId` (`0031B770`) and is itself called by `BattleUnit_UpdateLifecycleAndCombatFrame` (`00233F70`); `BattleLocomotion_DecodeOrderGoal` (`00312730`) calls `BattleUnit_FindByDefinitionSelector` (`002367A0`) and `00265090`. The rest are actor-layer callers of the same shared helpers — `BattleUnit_SnapshotWorldActorRuntimeState` (`00236300`), `ActorManager_RunFieldRuntimePass` (`0025D9E0`) and nine more readers of the focus handle `003590D0`, the position readers `0037B4D0` and `003B73B0`, the matrix and fill leaves' callers `003F1E90` and `00400AC0` — plus the actor lookups of the two bodies cited only as callers (`00226BE0` reaching `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` and `ActorManager_GetRecordByOrdinal` `00358940`; `002C6F70` and `002C7660` reaching `0025B4C0` and `ActorRuntime_GetClassNibble` `00263C20`). The collector depends on the actor layer only for position, radii and unit lookup, and the lifecycle frame is what schedules it; every other edge is that layer using the same accessors for its own work.

**Audio — CLIENT, OUT-OF-SCOPE (2 edges).** `00362850`, a 1,036-byte Audio body, calls `00265020` and `003590D0`: it reads an actor position and the focused actor's handle through the same shared accessors the pickup code uses (the body is not read here), and no pickup state reaches it.

**CombatAction — SERVICE and CLIENT (16 edges).** `00310DB0` calls `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`), `BattleTarget_ComputeGlobalEligibilityMask` (`0030B770`) and `BattleTarget_ComputeUnitEligibilityMask` (`0030B7F0`) in the same periodic pass that runs the collector; `BattleAction_PrepareExecutionResources` (`0030EF20`) and `BattleAction_RefundReservedExecutionResources` (`00300280`) call the inventory primitive `003008A0`; `00312730` is called by `002FDA60` (a 464-byte switch arm the census names caseD_4000); and `Battle_ProcessActionTarget` (`00307300`), `BattleAction_ComputeEffectiveRangeBands` (`002FEB80`), `BattleUnit_AdvanceStandardActionState` (`00304850`), `00320E10` and four others read positions, radii, the focus test or the XZ distance through the shared helpers, while `00313DB0` calls `00226BE0`. The maintenance runner is shared with that layer's per-unit checks and action costs spend items through the same primitive the pickup grant uses; nothing in that layer reads the pickup pool.

**Core — CLIENT (1 edge).** `002341C0`, a 62-byte battle-storage reset batch, calls `Loot_InitializeWorldPickupPool` (`00319B10`) after clearing the pending action queues, the navigation dataset and the perception cache: the pool is emptied as one step of that reset.

**CoreRuntimeScheduling — DEPENDENCY (6 edges).** The command-line and settings parser `0022BDF0` (called by the boot root `0022A0B0`) reads `FrameLimit` through `0017D8F0` and calls the time-base writer `001EDDC0`; `00310DB0` and the drain beat `BattleFormula_ApplyGlobalPeriodicDrainModes` (`00385CA0`) call `GameClock_GetRawTickCounter` (`0032A150`). The pickup lifetime and blink arithmetic depend on the frame-rate scalar that path writes and on that clock; nothing else is shared.

**Gameplay — SERVICE and CLIENT (11 edges).** `Loot_DeriveWorldPickupPresentationTier` (`00319A20`) calls `BattleDefinition_MapByte9ToRuntimeCategory` (`0031E9F0`), which `BattleDefinition_GetRuntimeCategoryBySelector` (`0031EA90`) also calls; `00310DB0` calls `BattleEncodedId_IsValidForClass` (`00322C50`); `00312730` calls `BattleRuntime_GetModeDependentDistanceThreshold` (`00309A90`); `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` (`00316DF0`) and `DefinitionRuntime_DeactivateAndRemoveConfiguredItems` (`00323540`) call the grant arm `00300B80`; and `BattleAction_FindApproachGeometryAroundTarget` (`00339630`) and `0031ADB0` use the matrix helpers, the position getter or the focus handle. The tier depends on that layer's item-category mapping, and definition activation grants items through the same arm as a pickup; the rest is shared helpers.

**Input — CLIENT, OUT-OF-SCOPE (1 edge).** `00226BE0`, the Input-domain actor mask propagation body, calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`): input reads the same focused-actor identity the loot test compares against, and the pickup pool does not reach input state.

**Items_Equipment_Shops_License — SERVICE and CLIENT (16 edges).** `Loot_CollectWorldPickupAndGrantInventory` (`00319920`) calls `Inventory_GrantEncodedLootItem` (`00300B80`), which tail-calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`); `003008A0` calls `Inventory_QueryEncodedItemStateByClass` (`00309F30`) and is called by twelve inventory bodies, among them `InventoryBundleClass09_ApplyGilAndNestedItems` (`002FD530`), `InventoryBundleClass0A_ApplyNestedItems` (`002FD640`), `Shop_CommitPurchaseItemAndGil` (`002FEEB0`) and `EquipmentInventory_IncrementSecondaryCountChannel` (`0030C410`); and `BattleStats_SetLicenseNodeStateAndApplySideEffects` (`00323910`) calls `00300B80`. A collected pickup is granted through that layer's modify primitive, the same one bundles, shops and licence side effects use; the pickup code owns only which slot and which seven entries are granted.

**Movement — SERVICE and CLIENT (165 edges).** `BattleLocomotion_DecodeOrderGoal` (`00312730`) calls `Loot_FindNearestActivePickupPosition` (`00319850`) and that layer's `00309B10`, `BattleUnit_GetNavigationClearanceRadius` (`0030A130`), `00312DF0` and `0031ABE0`; the visual create `003FA160` calls the placement resolve `0026E350`, which calls the scored id selector `00231900` and the record read `00231820`, and the selector's helpers cited in the appended note (`00231890`, `002324F0`, `00233050`) and their other callers, among them `0026E3C0`, `002FB560`, `003808A0` and `0022F430`, are movement bodies; `0026A1D0` calls `00226BE0`; the time-base writer `001EDDC0` calls `00337A00`, which re-derives two movement timing constants from the new frame-rate scalar. The remaining edges are locomotion bodies — `Movement_UpdateSteeringTowardTarget` (`002E45E0`), `BattleLocomotion_TestForwardStepClearance` (`00335B60`), `PartyFollow_SolveFormation` (`00338490`), `BattleLocomotion_ComputeRemainingPathDistance` (`00334950`) and others — calling the matrix helpers, the position and radius getters, the float-pair copy `003DA710`, the focus handle and the XZ distance leaf. The loot code asks movement for a placement record and movement asks the loot code for the nearest pickup as an order goal; everything else is the two layers sharing geometry helpers.

**Party — SERVICE and CLIENT (18 edges).** `PartyFocus_IsCurrentPackedActorHandle` (`003273B0`), which the maintenance runner `00310DB0` calls to qualify the collecting unit, calls `003590D0`; `00312730` calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) and `BattleUnit_GetPartyLeader` (`003272A0`); and `003590D0` is called by `PartyRoster_GetActorBySlotOrCurrentFocus` (`00263770`), `PartyRoster_AssignActorToSlot` (`00269C70`), `003272A0` and three more, `003273B0` among them, while `PartyFocus_TryGetCurrentActorWorldPosition` (`00359150`), `00303CC0` and `00304180` read positions through `00265020`, and `00226BE0`, `002C6F70` and `002C7660` reach `003590D0` or `PartyRoster_GetActorBySlot` (`00263750`). The "is this the focused actor" test that decides who collects loot is that layer's; the other edges are party bodies reading the same identity and position accessors.

**Presentation — SERVICE and CLIENT (100 edges).** `Loot_CreateWorldPickup` (`00319CA0`) calls `Loot_DeriveWorldPickupPresentationTier` (`00319A20`), filed to that layer, which calls `0031E9F0`; the other edges are render bodies calling the leaves this page cites — the 16-byte copy `00202C90` (24 callers, among them `RenderBounds_ClassifyViewFrustumIntersection` `003B3F10`), the identity-matrix set `00203170` (30, among them `Skeleton_ComposeFinalPose` `00373860`), the three matrix-rotate helpers `00202E90`, `00202F00`, `00202F70`, the dword fill `00275550`, the texcoord decoder `002711E0`, the 16-byte fetch `003E5700`, the named-image lookup `0024A5A0`, the placement resolve `0026E350` and the selector helpers `00231890` and `002324F0` — or reading positions and the focus handle (`BattleUnit_TestActorViewFrustumAtCurrentPosition` `00322360`, `WorldActor_TestBoundsAgainstViewFrustumAtPosition` `003223C0`, `RenderSystem_UpdateCharacterRecords` `00426090`). The pickup's tier is computed by a Presentation-filed body; everything else is rendering using the same generic vector and matrix machinery.

**Resource — SERVICE (2 edges).** The visual create `003FA160` and the UI body `00279E20` call `0024A5A0`, the lookup that finds an entry by name in the 64-slot named-image table: the pickup's two visual objects are fetched by name from that table, and the UI body is cited here only as a caller of the flag-scan fetch.

**Script_VM_Native_Bridge — CLIENT, MECHANICAL (44 edges).** Twenty-three script-VM bodies — `0033FD60`, `00344AF0`, `00345180`, `00345830` and nineteen more — call `00265020`; fourteen, among them `00341CB0`, `0034F800` and `00350DD0`, call `003590D0`; `00344390`, `003448F0` and `00345630` call `004686D0`; `00356160` calls the matrix helpers `00202E90`, `00202F00` and `00203170`; and `0050FAF0` calls the grant arm `00300B80`. Script natives read positions, the focus handle and XZ distances through the same accessors, and one native grants an item through the loot grant arm; none of them touches the pickup pool.

**Spawn_Encounter_Lifecycle — CLIENT, MECHANICAL (5 edges).** `Spawn_TrySelectCandidatePosition` (`00234AF0`), `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`) and `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`) call `00265020`, and the last two also call `003273B0`: spawn placement and range retirement use the same position and focus accessors, and share no state with the pickup pool.

## 8. The `00319600` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`Loot_UpdateWorldPickupLifetimeAndDespawn` owns three exclusive members — the two
`[0209BE80]+0x57E0` forwards that arm a slot and the position publisher that fills it.
The root's body confirms §3's ladder exactly: the walk is over the intrusive list rooted
at `02EC1360`/`02EC1368` (`00319615`), each node carrying state `+0x4`, the arming tick
`+0x8`, the world-object id `+0x58`, the pool slot `+0x0` and the `+0x10`/`+0x18` links.

- **State 1** (`00319739`–`00319775`): `0028EFE0(id)` polls the object; on return 2 the
  node stamps `+0x8 = dword[0208D45C]` (the field clock), moves to state 2, fetches the
  16-byte position through `0028EFC0(id, &vec)` and publishes it with `002FB2D0(slot, &vec)`.
- **States 2–6** (`003196E9`–`00319732`): the blink ladder — when
  `dword[0208D45C] ≥ stamp + 30×(state+53)` ticks (1650/1680/1710/1740/1770, since
  `step = int(1.0f × −30.0f) = −30`), the state increments and `0028F000(id, 2, &phase)`
  fires with `phase = 7 − old state`.
- **State 7** (`00319664`–`003196E4`): at `stamp + 1800` ticks the node is unlinked from
  the `02EC1360`/`02EC1368` list, `0028F000(id, 4, &out)` fires the despawn verb,
  `002FB2A0(slot)` frees the pool slot, and `+0x4`/`+0x10`/`+0x18`/`+0x58` are cleared.

| member | role | interior |
| --- | --- | --- |
| `0028EFE0` (21 B) | **ready query** — arg-shuffles `(id)` onto the manager object `[0209BE80]+0x57E0` and tail-jumps `003FA730`; return 2 means materialised | [`0028EFE9`](../_index/ADDRESS-INDEX.md) |
| `0028EFC0` (24 B) | **position fetch** — same `+0x57E0` object, `(id, &vec16)` tail-jumps `003FA6E0`, producing the vector `00319600` hands to the slot publisher | [`0028EFCC`](../_index/ADDRESS-INDEX.md) |
| `002FB2D0` `LootPresence_PublishSlotPosition` (54 B) | slot guard (`ecx ≤ 9`, else −1) over the ten-entry `0x20`-stride table at `022BE7F0`: a set flag byte returns −2, otherwise the 16-byte vector lands at `slot+0x10`, the flag latches, returns 1 | [`002FB2F2`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0028F000` (the phase verb — also a followup-queue
root with its own members), `002FB2A0` (slot free), `003FA6E0`/`003FA730` (the
`+0x57E0` object's real bodies), and the CRT cookie `00808C40`.

## 9. The `0028F000` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`0028F000` (156 B) is the six-op verb dispatcher every `00319600` phase transition and
every create/destroy path funnels through — the `Loot_…` entry point §3 documents. It
reads the manager at `[0209BE80]` (`0028F00B`), bounds-checks `op − 1 ≤ 5`, and
dispatches through the RVA jump table at `0028F09C` (`0028F01F`–`0028F032`):

| op | arm | call |
| --- | --- | --- |
| 1 | `0028F034` | `003FA160([mgr+0x57E0], args, [args+0x10], [args+0x14])` — create |
| 2 | `0028F050` | `003FAA10(record, [args+0])` — the phase/blink notify `00319600` fires |
| 3 | `0028F063` | `003FA820(record, [args+0])` — remove with a parameter |
| 4 | `0028F076` | `003FA820(record, 0)` — despawn |
| 5 | `0028F076` | **same arm as op 4** — eviction and expiry are literally one call, confirming §3's note |
| 6 | `0028F088` | `003FA900([mgr+0x57E0])` — end every live record; unreached by all six call sites per §3 |

| member | role | interior |
| --- | --- | --- |
| `003FA160` (886 B) | **the create**: lazily builds the manager's two visual objects at `+0x2690`/`+0x2698` via `0024A5A0` (`003FA1BB`/`003FA1CE`), precomputes four `0x10`-stride float triples at `+0x2654` from the `word[+0x44]`-indexed sub-table (`003FA200`–`003FA26D`), walks the signed-offset table at `00D12018` (`003FA2A0`), then per record: `00275550` 0x2A0-byte init, `+0x264 = 0xBE800000` (−0.25), the `+0x4`/`+0x14` position nudges by `float[01D45B70]`/`float[01D45B68]`, `003FBE90` for the visual, and a `+0x278` link into the `+0x2490` list (`003FA46A`–`003FA48F`) | [`003FA465`](../_index/ADDRESS-INDEX.md) |
| `003FAA10` (217 B) | **the phase notify**: builds a six-word table on the stack — `float[01DFE0BC]` scaled by six rodata constants — writes `word[+0x288] = table[phase]`; on first call also sets `word[+0x28A] = 0x4000` and flags `+0x272` (`& 0xFFEF | 8`) (`003FAAA3`–`003FAACF`). The `7 − state` argument `00319600` passes indexes this brightness table | [`003FAACB`](../_index/ADDRESS-INDEX.md) |
| `003FA900` (270 B) | **end-all**: walks the `+0x2490` list with `ebp = 0x100`, running the op-4 teardown on every record — the body §3 already names | [`003FA90F`](../_index/ADDRESS-INDEX.md) |
| `003FBE90` (730 B) | **the visual constructor**: per-entry loop zeroing `+0x70`, a `0xB60B60B7` magic divide computing a `mod 0x168` (360°) yaw scaled by `float[01DFE0B8]`/`float[008C612F]`-family constants (`003FBEFD`–`003FBF29`), the `00203170`/`00202E90`/`00202F00`/`00202F70` name-format sequence twice, then `00270B40` to submit — builds the pickup's render entry with a deterministic rotation | [`003FBF12`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003FA820` (the shared remove — called by ops 3–5 but
with other callers), `0024A5A0`, `002711E0`, `0026E350`, `00275550`, `00202C90`,
`00270B40`, the format helpers, and the CRT cookie `00808C40`.


## Interior citation — frontier hub `00300B80` (2026-09-18, SWE2-EC7)

`00300B80` — 28 B, 6 A-measured callers; `Inventory_GrantEncodedLootItem`, the grant arm of
this page's pickup flow. Interior verified: it is a three-instruction marshal — preserves the
caller's `r8d` on the stack (`00300B84`), forces `r8d = 0`, `r9d = 1` (`00300B89`–`00300B8F`)
and tail-calls `003008A0` = `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` at
[`00300B92`](../_index/ADDRESS-INDEX.md). Grant = the modify primitive with the
discovery-update flag `r9d` forced on.


## Interior citation — frontier hub `003273B0` (2026-09-18, SWE2-EC7)

`003273B0` — 28 B, 6 A-measured callers; `PartyFocus_IsCurrentPackedActorHandle`, the
is-it-me test the loot verbs ask before claiming a pickup. Interior verified: `003590D0()`
supplies the local packed handle ([`003273B8`](../_index/ADDRESS-INDEX.md)) and the whole answer
is `sete (eax == ecx)` (`003273BF`–`003273C4`) — arg equality against the focused actor's
handle, nothing else.

### Crossing — Input (batch-8 hub exposure)

Naming `003590D0` (the packed-handle supplier `003273B0` compares against) exposes one
Input-domain caller edge: `00226BE0` calls `003590D0`. That is Input reading the focused
actor's packed handle — the same identity source the loot verbs consult — not the pickup
pool reaching into input state.

### Interior citation — frontier hub 002FB2A0 (2026-09-18, SWE2-EC7)

**002FB2A0** (`LootPresence_ClearSlot`, 27 B, 4 A-measured callers) — the despawn path's slot clear. Bounds-checks the slot (`edx <= 9`, the ten-slot pool), zeroes `0x20` bytes at `global + edx*0x20` via `rep stosb` (`[rip+0x21A02B]` base + `[rip+0x21A023]` pool), and returns — the per-slot reset the despawn walk and the despawn timer both reach. In-scope: bound test [`002FB2AA`](../_index/ADDRESS-INDEX.md); `rep stosb` clear [`002FB2B8`](../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-30 update (2026-09-18) — `0026E350` gated two-step resolve

`0026E350` (109 B) is the placement call `003FA160` runs when filling
a pickup record: while the `0209A670` manager object and its `+0x8`
list head are both live, `00231900(list, arg, 1)` resolves a word id
(a negative result or either null returns -1), then `00231820(list,
out, id)` reads the record out and the function returns 0 — a
two-stage registry resolve used at record-placement time. Interior
anchor `0026E380` (the `call 00231900` resolve).
## SWE2-EC7-31 update (2026-09-18) — `00231900` scored id selector

`00231900` (393 B) is the resolve the `0026E350` two-step names:
`00233050(list)` returns a signed start index (null list or
negative start returns -1); `word[[list+0x20] + 2*idx]` and its
successor give the scan's (begin, count) over the
`word[[list+0x28] + 2*i]` id array. Each id `< 0x4000` gets a
0x20-stride record at `[list+0x10]`: the candidate must carry
`float[+4] > 0.001` and pass `bt r12d, dword[+0xC] & 7`, then
`002324F0(list, id, &tmp)` must not fault — and `00231890(list,
r15, id)` returns the score kept in `xmm6`, the argmax id in
`si`. The best id comes back in `ax`, -1 on any early out.
Interior anchor `00231A0F` (the `call 00231890` score).

## SWE2-EC7-39 update (2026-09-19) - `00270B40`

`00270B40` (420 B) is a loot-pool body - `01CEBB70`/`01CEBBA8`, `00861F14` pair. Interior anchor `00270B7E` (an `00861F14` call).

## SWE2-EC7-40 update (2026-09-19) - `00319B10`

`00319B10` (387 B) is the `Loot_InitializeWorldPickupPool` body the page names - call-free block initializer zeroing and seeding the `02EC0FA0`..`02EC1xxx` pool record region (`02EC1000` set to 1, the rest to zero). Interior anchor `00319B12` (the `02EC1000` seed store).

## SWE2-EC7-51 update (2026-09-19) - `002711E0`

`002711E0` (174 B) is a call-free packed texcoord decoder - `(word[rdx] + (r9d >> 1)) / (1 << ((r8 >> 0x1A) & 0xF))` -> `[rbx+8]`, `(word[rdx+2] + ...) / (1 << ((r8 >> 0x1E) & 0xF))` -> `[rbx+0xC]`. Interior anchor `002711F4` (the exponent extract).

## SWE2-EC7-97 update (2026-09-20) - `002E9CA0` measured

`002E9CA0` (107 B) is the gated apply `002C6F70` and `002C7660`
call: `rcx`'s `[+0xC0]` word must resolve through the `0x740`
table and `[+0x284] != 0` before `003E5700(rcx)` runs, then
`[rdx+0xC] = 1.0f` either way - the null path additionally
zeroing `[rdx]`/`[rdx+8]` first, so the out record always ends
with a defined scale.
Interior anchor `002E9CE4` (the `003E5700` call).

## SWE2-EC7-103 update (2026-09-20) - `00273460` measured

`00273460` (69 B) is the flag-scan fetch
`00279E20` and `002C7660` call: `0035BB60()`
counts the table, `0035BB20(i)` walks it, and the
first entry with `byte[rax]` bit 2 set answers
`dword[rax + 4]`; no match returns 0 - the
armed-slot read the loot-pool arms share.
Interior anchor `00273478` (the `& 4`
test).
