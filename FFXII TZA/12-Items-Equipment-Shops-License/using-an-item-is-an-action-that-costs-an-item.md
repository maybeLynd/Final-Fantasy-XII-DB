---
system: Using an item — an action that costs an item
category: 12-Items-Equipment-Shops-License
status: AUDITED
owner_layer: PrimaryOwner:Items_Equipment_Shops_License
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-item-use-pass-1
  crossref_clean: true
  reopened_count: 0
---

# Using an item — an action that costs an item

> **There is no item-effect system.** A Potion is an ordinary action row whose category byte says
> "item", and whose effect resolves through exactly the same pipeline as a spell. The only
> item-specific behaviour in the engine is that *preparing* the action takes one out of your bag —
> and remembers which one, so it can put it back.

## 1. What the player sees

Use a Potion and it leaves the inventory the moment the character commits, not when the healing
lands. Interrupt the action — the character is killed, the target dies first, the order is cancelled
— and the Potion comes back. An enemy that uses an item takes nothing from your bag, and nothing from
its own.

All three fall out of §3 and §5.

## 2. An item is an action row

Actions live in the table at `02EBF138` — the same table the License check consults for its
"needs no License" flag. Two fields carry the item behaviour:

```
action row (table 02EBF138)
    +0x1E  uint8   category;  == 3 means THIS ACTION IS AN ITEM
    +0x22  uint16  the item id consumed when it is used
```

Everything else about a Potion — what it heals, its animation, its targeting — is the ordinary
content of an action row, resolved by the ordinary action pipeline. **Nothing downstream of the
resource step distinguishes an item from a spell.**

> The engine does not ask "what does this item do?" It asks "what does this action do?", and *item*
> is a property of how the action is paid for, not of what it does.

**The row is passed by pointer and the id recovered by division:**

```asm
base   = ResolveRuntimePointer([02EBF138].handle)
stride = word [02EBF138 + 8]
id     = (rowPointer - base) / stride
```

Both `Prepare` and `Consume` do this, so callers hold a row pointer and the id is derived where
needed rather than carried alongside.

## 3. Prepare takes the item

`BattleAction_PrepareExecutionResources(unit, actionRow)` (`0030EF20`), complete in the parts that
matter — **including the precondition the first version of this sketch left out** (corrected
2026-09-11, ASTRA-REQ-FABLE-PREPARE-PRECONDITION): the action id is derived from the action
table *before* the null-unit guard, so the table header at registry `02EBF138` must be bound with
a non-zero stride whatever the unit is; a null unit with a valid table returns after the resolver
call, a missing header faults on the read of dword `0xC`, a zero stride raises a divide fault at
`0030EF5B` (ASTRA's [EXP-064](../_experiments/EXP-064-resource-payer-controls.md)). Nothing checks
the row pointer's alignment — the unsigned division truncates:

```c
hdr      = ImageAddress_ResolveRuntimePointer(*(u32*)(REG_02EBF138 + 0xC));   // 0030EF2F-0030EF3F: BEFORE any guard
actionId = (u32)(actionRow - hdr) / *(u16*)(REG_02EBF138 + 8);                // 0030EF44-0030EF5E: unsigned, 32-bit
if (!unit) return;
rec = unit[0x698];
if (!rec || rec[5] != 0) return;              // party members only (§5)

itemId = 0xFFFF;
if (actionRow && actionRow[0x1E] == 3)        // category 3 == item
    itemId = *(uint16*)(actionRow + 0x22);
unit[0xDC8] = itemId;                         // the reservation

if (itemId != 0xFFFF)
    Inventory_ModifyEncodedItemAndUpdateDiscoveryState(itemId, -1, 0, 1, 0);   // take one, now

cost = BattleAction_ComputeGilCost(unit, (u16)actionId);   // 00309060 - the gil cost, a separate resource
unit[0xE58] = cost;                           // stored BEFORE the gil is read
if (cost) SetGil((GetGil() - cost) >= 0 ? GetGil() - cost : 0);   // a sign-bit test of the 32-bit subtraction (0030EFD1-0030EFD3)
```

**The inventory decrement happens at prepare, not at execution.** The item is gone the moment the
action is set up, which is what a player observes; the effect has not resolved and may never resolve.

`unit + 0xDC8` is the **reserved item id**, using `0xFFFF` as "none" — the same empty marker the
equipment slots use
([`equipment-slots-and-the-single-stat-rebuild.md`](equipment-slots-and-the-single-stat-rebuild.md) §2).

## 4. Consume clears the reservation; Refund undoes it

`BattleAction_ConsumeExecutionResources(unit, actionRow, flag)` (`00305640`, 393 B) clears both
reservations and charges the remaining resources — read whole 2026-09-11 (the first sketch
stopped at the MP line and let the kind guard look like an early return; it is not):

```c
actionId = (u32)(actionRow - hdr) / stride;            // 0030565E-00305693, before any guard (as in Prepare)
if (unit && unit[0x698] && unit[0x698][5] == 0) {      // the kind guard scopes ONLY these two stores
    unit[0xE58] = 0;                                    // gil reservation released (003056B3)
    unit[0xDC8] = 0xFFFF;                               // item reservation released -- NOT given back
}
mp    = BattleAction_ComputePrimaryResourceCost(unit, (u16)actionId);        // 00309110
units = BattleAction_ComputeSecondaryResourceMultiplier(unit, (u16)actionId); // 00308FF0: row.b_0A for kinds 5 / 6, else 0
BattleStats_ModifyPrimaryResource(unit[0x698], -mp, 0x10 | (flag != 0));    // 003056F4: reaction suppressed; bit 0 skips the entry gates
stats = unit[0x698];                                                          // re-read after the MP call (003056F9)
BattleStats_ModifySecondaryResource(stats, -(s16)stats[0x28] * units, same flags);   // 0030570D: units x max MP off the pool
SetGil(sign-clear ? GetGil() - unit[0xE54] : 0);                             // 00305712-0030572B: a SECOND gil field, always run
if (unit[0x698][5] == 0)                                                      // kind 0 only: category accounting
    switch (actionRow[0x1E]) { case 0: 00253770(0, 1); case 1: (1, 1); case 2: (2, 1);
                               case 10: 00316440(); 00253770(13, actionId re-derived); }
```

So the kind guard protects only the reservation stores — a kind-1 or kind-3 unit keeps both
fields and still reaches every charge; the MP charge suppresses the reaction publisher and skips
the entry gates when the third argument is non-zero; the secondary pool is charged **max MP × the
action's `+0x0A` byte** for kinds 5 and 6 (the same byte that is the MP cost for other kinds — for
those two kinds `00309110` returns 0), which is exactly what the availability check compares
against `stats + 0x4E` for reason `0x14` ([the availability page](../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md));
`+0xE54` is a gil charge the target-preview evaluators store (`00303954`, `00303B2E`, from
`004698C0`'s output) — distinct from the `+0xE58` reservation, unread beyond that; `00253770`
thunks into the achievements module (`00316A50`). ASTRA's
[EXP-065](../_experiments/EXP-065-resource-consume-controls.md) executed the body in isolation
over 23 fixtures with the eight callees as recording stubs: the guard's extent, the call order,
the stats re-read after the MP call (a mutant reusing the old pointer is rejected), the wrapped
`max × units` product, the always-run extra-gil path and the category tail. [EXP-066](../_experiments/EXP-066-consume-native-composition.md)
then runs the consumer with the cost functions and the native MP / secondary / tier writers as
original code against one memory state (ten bodies, 15 cases; a cost-negation mutant caught): a
base cost of 31 leaves MP 9, category 5 with two charges empties a 150-point pool at max 100, a
kind-1 unit on effect 32 is charged a computed 390 and its 40 MP stops at the floor, 0, and a synthetic negative cost drives a native MP *gain*
that also raises the pool before the consumer's own zero secondary call — composition evidence
for the three contracts, with ownership, eligibility and gil storage as fixtures.

`BattleAction_RefundReservedExecutionResources` (`00300280`) is the mirror of the **reservation half only** — it is gated whole on kind 0 (`0030029D`–`003002A3`), gives the item back and returns the reserved gil, and charges nothing:

```c
itemId = unit[0xDC8];
if (itemId != 0xFFFF) {
    Inventory_ModifyEncodedItemAndUpdateDiscoveryState(itemId, +1, 0, 1, …);  // give it back
    unit[0xDC8] = 0xFFFF;
}
if (unit[0xE58]) SetGil(max(GetGil() + unit[0xE58], 0));
```

Consume clears its kind-zero reservations without returning the item or reserved gil;
Refund returns both. The inventory calls are `-1` at Prepare and `+1` at Refund;
Consume has no inventory call. The reservation fields hold this bookkeeping.

Beyond reservation clearing, Consume calls the MP, secondary-pool and preview-gil
(`+0xE54`) paths for every unit kind, while its category-accounting tail is **kind
zero only**. These are separate operations from Refund. This distinction is
supported by [EXP-065](../_experiments/EXP-065-resource-consume-controls.md) and
[EXP-066](../_experiments/EXP-066-consume-native-composition.md). Corrected
2026-09-11: the earlier “one thing” comparison also omitted reserved-gil return,
and the first residual correction incorrectly included category counters among
charges performed for every kind.

## 5. Enemies do not spend items, and it is the same gate as the License check

All three functions test the same byte — but not with the same reach (corrected 2026-09-11):

```c
rec = unit[0x698];
if (!rec || rec[5] != 0) ...      // Prepare: skip the item and gil reservations (0030EF60-0030EF77)
                                  // Refund : return, nothing to give back (0030029D-003002A3)
                                  // Consume: skip only the two reservation stores (00305695-003056C1); every charge still runs
```

`unit + 0x698` is the battle record, and `rec[5]` is the **record kind byte** documented in
[`battle-record-kind-byte.md`](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) —
**the same byte, at the same offset, that decides whether the License board applies**
([`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md) §3).

So a non-party unit using an item consumes nothing from the bag, reserves nothing and pays no
reserved gil — but Consume still charges it the MP cost, the secondary pool and whatever its
preview parked in `+0xE54` (§4; EXP-065's kind-1 and kind-3 controls execute every resource call).
**The inventory is a property of the party, and the engine expresses that by skipping the
reservation step for everyone else** rather than by giving enemies their own bag.

> Two systems that look unrelated — what you may cast, and what a Potion costs — are gated on one
> byte. **The kind byte is the engine's answer to "is this one of the player's characters?", and it is
> reused wherever that question decides behaviour.**

## 6. Key addresses

| Address | Name | Role |
|---|---|---|
| `0030EF20` | `BattleAction_PrepareExecutionResources` | reserves and takes the item (§3) |
| `00305640` | `BattleAction_ConsumeExecutionResources` | releases the reservation (§4) |
| `00300280` | `BattleAction_RefundReservedExecutionResources` | returns the item and gil (§4) |
| `003008A0` | `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` | the ±1 inventory call |
| `00300CE0` | `BattleStats_ModifyPrimaryResource` | the MP deduction in Consume |
| `00308FF0` | `BattleAction_ComputeSecondaryResourceMultiplier` | kinds 5 / 6: the row's `+0x0A` as a count of max-MP units off the secondary pool |
| `00300BC0` | `BattleStats_ModifySecondaryResource` | the pool deduction in Consume, `−(max × units)` |
| `00253770` | thunk → `00316A50` (achievements) | the category-accounting call at the end of Consume |
| `02EBF138` | — | action row table; `+0x1E` category, `+0x22` consumed item |

`unit + 0xDC8` (reserved item id) and `unit + 0xE58` (reserved gil) are the two reservation fields.

## 7. Data structures and formulas

```
action row (02EBF138)      +0x1E  category (3 = item)
                           +0x22  uint16 consumed item id
                           +0x2C  uint16 flags, bit 0x2000 = no License required

unit + 0x698   battle record; record[5] = kind byte, 0 = party member
unit + 0xDC8   uint16  reserved item id, 0xFFFF = none
unit + 0xE58   int32   reserved gil

prepare :  reserve item, inventory -1, reserve gil, gil -= cost
consume :  reservations cleared, MP deducted, item NOT returned
refund  :  inventory +1, gil += reserved, reservations cleared
```

## 8. Call chain

```
action committed
  -> BattleAction_PrepareExecutionResources (0030EF20)
        -> Inventory_ModifyEncodedItemAndUpdateDiscoveryState(id, -1, …)
        -> GameState_Get/SetGil
  -> ... the ordinary action pipeline resolves the effect ...
  -> BattleAction_ConsumeExecutionResources (00305640)      on execution
     or BattleAction_RefundReservedExecutionResources (00300280)   on cancellation
```

## 9. Modding notes

**To make any action consume an item, set its category byte `+0x1E` to 3 and put the item id at
`+0x22`.** Nothing else is required — the reservation, the decrement and the refund are generic.

**To make an item free, clear `+0x22` to `0xFFFF`** rather than editing the inventory path; prepare
tests exactly that value.

**An item's *effect* is not edited here.** It lives in the action row's ordinary effect fields, which
this document does not cover.

**Do not expect enemies to consume items** by giving them item actions — the reservation step (the
item and the reserved gil) is skipped for any unit whose record kind byte is non-zero (§5); the MP,
pool and preview-gil charges in Consume are not.

## 10. What is not known

- **The other arguments to `Inventory_ModifyEncodedItemAndUpdateDiscoveryState`.** The sign and the
  item id are established; the trailing flags (`0`, `1`, and a fifth argument) are passed as constants
  ~~that were not traced~~ *(answered: the third is the absolute / relative selector, 0 = relative, the fourth the channel, 1 = owned, and the fifth is 0 — CONTRACT-bazaar-unlock-and-purchase.md §13a, "`(loot, 0, 1, 3)` decoded", and §11's evidence table; 2026-10-02, OPUS)*. The "discovery state" in its name is untouched here.
- ~~**What `FUN_00309060` computes** as the gil cost of an action.~~ *(answered: see the section "The action gil cost: 00309060" below - `10 × trunc(row.b[+0x0A] × 64.0 / 50.0)` for a kind-0 record whose status effect 32 is set, an id up to `0x21E` and a row category other than 5 or 6, else 0; 2026-10-02, OPUS)*
- ~~**Whether any category other than 3 exists at `+0x1E`**, and what it means.~~ *(answered: see §9's falsification pass, "`+0x1E` is a category that selects `+0x22`'s id space" — 1 magick, 2 technick, 3 item, 5 / 6 nibble `C`, 255 retired, over all 543 rows; 2026-10-02, OPUS)*
- **Where the effect itself resolves** — this document deliberately stops at the resource boundary.
- ~~**What Consume's `00309110` / `00308FF0` pair compute** before the MP deduction.~~ Answered
  2026-09-11 (§4): the MP cost ([the spend side](../10-Status-Periodic-Terminal/where-mp-comes-from.md))
  and, for kinds 5 / 6, the action's `+0x0A` byte as a count of max-MP units off the secondary pool.
- ~~**What `+0xE54` holds** — the gil charge the preview evaluators store from `004698C0`'s output
  and Consume always deducts.~~ Answered 2026-09-11: the preview record's `+0x08` — the gil amount
  recipe 61's preview slot computes for action `0xB5` (the party's summed current HP) — copied at
  `00303954` / `00303B2E`; zero for every other action ([the recipes page](../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.6).

## 11. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Category byte `+0x1E == 3` selects item behaviour | `cmp byte ptr [rdi+0x1E], 3 ; jne` in `0030EF20` | 1 |
| The action id is derived from the action table before the null-unit guard; a missing header or a zero stride faults even for a null unit; `+0xDC8` is stored before the inventory call and `+0xE58` before the gil read; the fifth inventory argument is 0; the gil subtraction is a sign-bit test | `0030EF2F`–`0030EF5E` read; EXP-064 (17 isolated cases over the 205-byte body with the resolver native and the four callees as recording stubs; the item-gate mutant rejected) | 1 + isolated original code |
| The consumed id is `uint16` at `+0x22` | `movzx eax, word ptr [rdi+0x22]` on that branch | 1 |
| `unit + 0xDC8` is the reservation, `0xFFFF` = none | written in Prepare, cleared in Consume, tested in Refund | 1 |
| The decrement happens at prepare | `call 0x3008A0` with `edx = -1` before the gil step | 1 |
| Refund returns exactly one | the same call with `edx = 1` | 1 |
| Consume does **not** return the item | it writes `0xFFFF` to `+0xDC8` with no inventory call | 1 |
| The party-only gate is the record kind byte | `mov rcx,[rbx+0x698] ; movzx ecx,byte [rcx+5] ; test ; jne` in all three — in Consume it scopes only the two reservation stores, not the charges (`00305695`–`003056C1`; corrected 2026-09-11) | 1 |
| Consume's guard extent, call order, the stats re-read, `max × units` on the pool, the always-run `+0xE54` gil path, the category tail | `00305640` read whole; EXP-065 (23 isolated cases, eight recording stubs, stale-pointer mutant rejected) | 1 + isolated original code |
| The action id is derived from the row pointer | `sub` from the resolved base then `div` by the `+8` stride, in both Prepare and Consume | 1 |

**Controls.** The claim *"Consume does not return the item"* is a negative, and it is a measurement:
the same reading positively identifies the inventory call in Prepare (`edx = -1`) and in Refund
(`edx = 1`), and finds no such call in Consume's body — which was decoded in full, not scanned to the
first `ret`.

**Not re-derived here.** The record kind byte, the gil setter's behaviour, and the action row's
License flag come from the documents linked in §12; each was read before being cited.
`check_already_answered.py` was run for these addresses and terms before this document was started.

## 12. Related

- [`gil-storage-clamp-and-every-path-that-moves-it.md`](../13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md) — gil is the other execution resource; these three functions are three of its thirteen callers.
- [`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md) — the same action table, and the same kind-byte gate.
- [`battle-record-kind-byte.md`](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) — the byte at `record[5]`.
- [`equipment-slots-and-the-single-stat-rebuild.md`](equipment-slots-and-the-single-stat-rebuild.md) — the `0xFFFF` empty-marker convention.

## The action gil cost: 00309060 (OPUS, 2026-10-02)

**What `00309060` is.** `BattleAction_ComputeGilCost(unit, actionId)`, 168 B (`00309060`–`00309107`), read whole from the shipping bytes, with its callees and both callers read. It returns the action's **gil cost** as an `int`. Zero means "costs no gil". The function writes nothing: there is no store in its body, and neither of its callees stores either. Static read only; nothing was executed.

**Arguments.**

- `rcx` is the battle unit (`rbx`, `0030906D`). Its `+0x698` is the stats record (`00309075`).
- `dx` is the action id, zero-extended (`0030906A`).

**Callers.**

| caller | site | what it does with the cost |
|---|---|---|
| `BattleAction_CheckExecutionResourceAvailability` `00303BD0` (← `002FFCF0` at `002FFEB0`) | `00303C7B` | **the check**: reason `0x15` (see below) |
| `BattleAction_PrepareExecutionResources` `0030EF20` (← `00304850` at `00304962`, `00307300` at `003073AB`) | `0030EFBB` | **the debit**: reserve at unit `+0xE58`, then gil −= cost |

**The rule.**

```
stats = unit ? unit[+0x698] : NULL;
if (stats && stats.b[+5] == 1)              return 0;   // kind-1 record: 00309070-00309085 -> 003090FB
if (actionId > 0x21E)                       return 0;   // 00309087-0030908F (543 rows, ids 0..0x21E)
row = res(02EBF138.+0xC) + actionId * 02EBF138.w[+8];   // 00309091-003090CA (NULL -> 0 at 003090CE)
if ((u8)(row.b[+0x1E] - 5) <= 1)            return 0;   // row kinds 5 and 6: 003090D0-003090D8
if (!BattleUnit_UsesGilActionCostChannel(unit)) return 0;  // 002F9820: 003090DA-003090E4
return BattleAction_ComputeModifiedResourceCostAmount(unit, actionId);   // tail jump 002F95D0 at 003090F6
```

**Callee `BattleUnit_UsesGilActionCostChannel` `002F9820` (51 B).**

- It returns 0 if `stats.b[+5] == 1` (`002F9825`–`002F9837`).
- Otherwise it returns 1 if `stats.b[+0x6C]` bit 0 **or** `stats.b[+0x7C]` bit 0 is set (`002F983A`–`002F984D`). That bit is effect id 32 in the mutable status layer `+0x68` or the derived augment layer `+0x78`.
- It has no null guard. For a null `unit` the `je` at `002F9823` falls through to `mov rax, [rcx + 0x698]` at `002F983A`, which faults. A null `stats` faults at `002F9841`. `00309060` itself does not filter a null unit (`00309070`–`00309073` only skip the kind test). Both callers prevent this: `00303BD0` refuses a null unit (`00303BE0`) and only calls when `stats` is non-null and kind 0 (`00303C68`–`00303C73`), and `0030EF20` does the same (`0030EF60`–`0030EF77`).

**Callee `BattleAction_ComputeModifiedResourceCostAmount` `002F95D0` (589 B), on the path `00309060` lets through.**

```
base = row.b[+0x0A];                                    // 002F95E4-002F962B: the authored MP byte
if (stats.kind != 1 && (id in 0xD0..0xE1 || id in 0x106..0x112))  return base;   // 002F962F-002F9667, 002F9806
if (stats.b[+0x6C] & 1 || stats.b[+0x7C] & 1)          // 002F9674-002F9682: tested FIRST
    return 10 * (int)trunc( f32(f32(base) * 64.0f) / 50.0f );   // 002F97E4-002F9802
// (Channeling 91-93, effect 51 zero, effect 36 halve: 002F9688-002F97DE - never reached on the gil path)
```

- The constants were read from the image: `00916318` = `64.0f` (`00 00 80 42`) and `008F3130` = `50.0f` (`00 00 48 42`).
- `cvttss2si` (`002F97FB`) truncates. `lea eax, [rax + rax*4]` / `add eax, eax` multiplies by 10 (`002F97FF`–`002F9802`).
- There is **no cap and no level term**. The cost is a pure function of `row.b[+0x0A]`.
- Because effect 32 is tested first, the gil cost is **not** reduced by Channeling, halved, or zeroed by the other MP effects.
- For every shipped base (1–72), the result equals `10 × floor(32 × base / 25)`. Base 31 gives 390 gil.
- **Shipped table** (`battle_pack.bin` `action_data`, 543 × 60): 115 rows reach the formula with a non-zero `+0x0A`, costing 10 gil (base 1) up to 920 gil (base 72, row 14). Rows whose `+0x0A` is 0 cost nothing, and the availability check skips them (`00303C84`).

**The exemption arm cannot be reached through either wrapper on shipped data.**

- Row byte `+0x1E` is 6 on exactly ids `0xD0`–`0xE1` (18 rows) and 5 on exactly `0x106`–`0x112` (13 rows).
- So `00309060`'s kind-5/6 test (`003090D4`–`003090D8`) and the MP twin's test (`0030916D`–`00309171`) return 0 before `002F95D0` ever sees those ids.
- The id ranges in `002F9646`–`002F9667` only matter for the third caller of `002F95D0`, the menu builder `0031EB20` (`0031F06D`). It calls the formula directly to show the cost word (`0031F072`), and uses `002F9820` to pick the gil marker `8` or the MP marker `2` (`0031F00C`–`0031F029`).

**Where gil is checked: `00303BD0`.**

```
if (stats && stats.b[+5] == 0) {                    // 00303C68-00303C73
    cost = BattleAction_ComputeGilCost(unit, id);   // 00303C75-00303C80
    if (cost && GameState_GetGil() < cost           // 00303C82-00303C8D; GetGil 00253690 = [02092758]+8
             && unit.d[+0xE58] < cost)              // 00303C8F-00303C95 (both compares signed, jge)
        return 0x15;                                 // 00303C97
}
```

This check runs after the reasons `0x12` (`003037A0`), `0x13` (MP: `stats.w[+0x4C]` < `00309110`) and `0x14` (`stats.b[+0x4E]` < `00308FF0`) (`00303BF5`–`00303C53`).

**Where gil is debited: `0030EF20`.**

```
id = (row - res(02EBF138.+0xC)) / 02EBF138.w[+8];   // 0030EF2F-0030EF5E (before any guard)
if (unit && stats && stats.b[+5] == 0) {            // 0030EF60-0030EF77
    ... reserve/consume the item (+0xDC8) ...       // 0030EF79-0030EFB0
    cost = BattleAction_ComputeGilCost(unit, id);   // 0030EFB5-0030EFBB
    unit.d[+0xE58] = cost;                          // 0030EFC0: the reservation, stored even when 0
    if (cost) GameState_SetGil( (GetGil() - cost) >= 0 ? GetGil() - cost : 0 );   // 0030EFC8-0030EFD8 (cmovns)
}
```

`GameState_SetGil` `00254EE0` then clamps to `[0, 99,999,999]` (gil-storage page). The refund `00300280` adds `+0xE58` back to gil and the consume path `00305640` clears it. Neither is re-read here; see `using-an-item-is-an-action-that-costs-an-item.md` §4.

**So `+0xE58` is a reservation, not a second purse.** The check's second compare lets an action through when its own cost is already reserved. That covers an action that was prepared, and so already paid, then re-checked while gil sits below the cost.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py --term "category byte" --addr 02EBF138` run first, per
[`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

§3's sketch reproduces **instruction for instruction at every address it cites**, the corrected
precondition included:

```asm
0030EF2F  mov   rax, qword ptr [02EBF138]      ; the slot
0030EF3C  mov   ecx, dword ptr [rax + 0xc]
0030EF3F  call  0x20e600                       ; the resolver - BEFORE any guard, as corrected
0030EF56  movzx r9d, word ptr [r8 + 8]         ; the stride
0030EF5B  div   r9d                            ; unsigned, 32-bit - the divide fault's address
0030EF60  test  rbx, rbx / je                  ; the null-unit guard, after
0030EF71  movzx ecx, byte ptr [rcx + 5] / jne  ; party members only
0030EF79  mov   ecx, 0xffff
0030EF83  cmp   byte ptr [rdi + 0x1e], 3 / jne ; category 3 == item
0030EF89  movzx eax, word ptr [rdi + 0x22]     ; the item id
0030EF93  mov   word ptr [rbx + 0xdc8], ax     ; the reservation, stored as a WORD
```

### `+0x1E` is a category that selects `+0x22`'s id space — over all 543 rows, without exception

§2 reads `+0x1E` as a category whose value `3` means *item* and `+0x22` as the item id.
[The action definition row](../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)
reads `+0x1E` as the **message kind** and `+0x22` as **the class-3 magick / technick id**. Both are
right about their own rows, and **neither is the rule.** Cross-tabulating the shipped table:

| `+0x1E` | rows | what `+0x22` holds |
|---:|---:|---|
| 1 | **81** | nibble `3` — magick ids — on **100 %** |
| 2 | **24** | nibble `4` — technick ids — on **100 %** |
| **3** | **51** | nibble `0` — **item** ids — on **100 %** |
| 5 | 13 | nibble `C` on 100 % |
| 6 | 18 | nibble `C` on 100 % |
| 0, 7, 8, 9, 10, 13, 14, 16, 17 | 300 | `0xFFFF` on **100 %** |
| 255 | 56 | `0xFFFF` × 43 — **and nibble `0` × 13** |

**Every category but `255` maps to exactly one id space, with no exceptions in 543 rows.** So
`+0x1E` is the field that says *what kind of id `+0x22` is*, and the two pages' readings are each
one row of this table. The 51 category-3 rows carry `+0x22` = `0x0, 0x1, 0x2 …` — sequential item
ids from zero.

> This also settles why the magick count keeps coming out as **81**: `+0x1E == 1` on 81 rows is the
> same 81 as the nibble-`3` block at rows 0–80 and the `4000 + n + 1` help-id run
> ([the count-clock pass](../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §9).
> One block, three fields agreeing.

### ⚠ Thirteen retired rows still carry an item id

Of the **56** rows with `+0x1E == 255` — the `NOT USED` / *Reserve* rows — **43** hold `0xFFFF` at
`+0x22` and **13 hold a live item id**. `0030EF83` tests `== 3`, so those thirteen are inert in the
engine: nothing consumes from them.

> **They are a trap for a reader, not for the game.** `+0x22` is only an item id when `+0x1E` says
> so, and thirteen rows have the id without the category. Anything that walks `+0x22` looking for
> item references — a mod, a randomiser, a census — must gate on `+0x1E` first.

**Not claimed:** §4's consume and refund paths, §5's enemy exception and the gil cost at `00309060`
were not re-read — only `0030EF20`'s prologue and item branch. Nothing was executed or observed
live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatAction — CLIENT and SERVICE, 35 edges.**
  - Cited functions are called by `BattleAction_ConsumeExecutionResources` (5), `Battle_ProcessActionTarget` (3), `BattleAction_CheckExecutionResourceAvailability` (3), `BattleAction_PrepareExecutionResources` (2) and a 722-byte action body (2).
  - They call `BattleTarget_ComputeUnitEligibilityMask` and `BattleTarget_ComputeGlobalEligibilityMask` (2 each), `BattleAction_ComputeModifiedResourceCostAmount` (2), `BattleUnit_UsesGilActionCostChannel` (2) and `BattleAction_ComputePrimaryResourceCost`.
- **CombatFormula — CLIENT and SERVICE, 16 edges.** Cited functions are called by `BattleFormula_ApplyTargetResult` (3), `BattleStats_ReconcileResourcesToEffectiveCapacity` (2), `BattleStats_SetPrimaryResourceAbsolute` (2) and `BattleStats_ModifyPrimaryResource`. They call `BattleStats_FindOwningBattleUnit` (3), `BattleStats_ModifySecondaryResource` (2), `BattleStats_ModifyPrimaryResource`, `BattleStats_GetByBattleSlotIndex` and `BattleStats_ResolveByActorHandle`.
- **Rewards_Progression_Economy — SERVICE and CLIENT.** Cited functions call `GameState_GetGil` and `GameState_SetGil` (3 each), and are called by `BattleUnit_ProcessDefeatRewardsAndLoot` and `GameState_SetGil`.
- **Status_Periodic_Terminal — CLIENT and SERVICE.** A cited function is called by `BattleUnit_RunPeriodicCombatMaintenance` and calls `BattleUnit_ClearPrimaryResourceRecoveryAccumulator`.
- **PlatformOnlineAchievements - SERVICE (8 edges).** `00305640`, `00316440`, `00316A50` reach bodies filed to PlatformOnlineAchievements: `00316440`, `00863280`, `008632B0` - shared machinery across the layer boundary, no shared ownership.

### Interior citation — frontier hub `00308FF0` (2026-09-18, SWE2-EC7)

`00308FF0` — 110 B, 5 callers, `BattleAction_ComputeSecondaryResou…`. An
index-guarded table arithmetic: `dx > 0x21E` returns 0; otherwise two
`ImageAddress_ResolveRuntimePointer` (`0020E600`) resolutions read the row stride
`word[rec+8]`, and `ecx = dx * stride + base`
([`00309041`](../_index/ADDRESS-INDEX.md)) ~~is returned — the flat secondary~~
~~resource offset for a 0x21F-entry table. Null resolutions return 0.~~ is the row address, not the result: the function returns the row's byte `+0x0A` when its category byte `+0x1E` is 5 or 6 (`movzx eax, byte [rcx+0x1e]` / `sub al, 5` / `cmp al, 1` / `ja`, then `movzx eax, byte [rcx+0xa]`), else 0; a failed resolution zeroes `rcx` (`00309048`) and still reads `[0x1E]`, so it faults rather than returning 0 *(corrected 2026-10-02, OPUS: checked at `0030904A`–`0030905D`; §4's `row.b_0A for kinds 5 / 6, else 0`)*.
