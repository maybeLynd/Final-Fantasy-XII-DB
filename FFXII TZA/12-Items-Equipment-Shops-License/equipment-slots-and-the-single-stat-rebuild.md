---
system: Equipment slots and the single stat rebuild
category: 12-Items-Equipment-Shops-License
status: DOCUMENTED — the equipment contribution formula inside 002FEF30 is read whole (§6, 2026-09-30); battle actions 0x9C / 0x9D, which the battle menu issues against the stashed loadout, do nothing (GR-12, answered 2026-09-30, SWE2-CONTRACT for OPUS; reviewed by SWE2-AUDIT-SEM, C4 applied) (owner re-status 2026-10-01, OPUS; documented_rule READY)
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
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: fable-plus-five-2026-09-20 - section 11 answers the structural lane's "five or six" question:
    FIVE, and +0x5A is the first word of a five-word BACKUP (+0x5A..+0x63) written by takeaway_item_and_equip
    (0030FBE0) and read back five-at-a-time by giveback_item_and_equip (0030FAA0 -> 0031A710, cmp edi,5/jl).
    The display record's "sixth equipment word" and the AI selectors 0x1A/0x1B index one past the array into
    saved[0]. 0x1000 is Unarmed, from the sibling id-encoding page. PRIOR: opus-equipment-slots-pass-1 - both caller censuses reproduce (14 over 25 sites, and exactly 2 with no thunk) and the equip path matches instruction for instruction; ANSWERED: there are five slots 0-4, bounded by an unsigned cmp esi, 4 in 00317930, whose short-circuit table 1000 FFFF FFFF FFFF FFFF accepts only (slot 0, 0x1000); CORRECTED: the preview diffs five slots at +0x50..+0x58, not three, and section 3's parenthesis about re-reading 'old' reverses the order; and 00328BD0 is gameplay, answered by FZ-6 one register row away
  crossref_clean: false
  reopened_count: 0
---

# Equipment slots and the single stat rebuild

> **Equipping something does not add anything to your stats.** It writes a 16-bit id into a slot and,
> if that changed the slot, throws the character's entire effective-stat state away and rebuilds it
> from scratch. There is no "apply a bonus" path in this engine, because there is nothing to undo.

**PARTIAL.** The slot model, the equip path and the complete set of rebuild triggers are read at
tier 1. ~~**The contribution formula inside the rebuild is not read** (§7).~~ *Corrected 2026-09-30 (FABLE):
the rebuild's whole body is read and its formula is written out in §6; the one item still open is what the
battle menu's two equip-branch actions `0x9C` / `0x9D` do (§11.3, `GR-12`).*

## 1. What the player sees

Swap a weapon and every number that depends on it is correct immediately — including numbers the
weapon does not obviously touch. Swap it back and you are exactly where you were, with no drift after
a hundred swaps. Look at the equip menu's projected stats and they match what you get, exactly.

All three are consequences of one design decision (§4).

## 2. The slot array

Equipment lives in the stats record as **`uint16` slots at `stats + 0x50 + slot*2`**, and there
are **five of them, `0`–`4`** (§10) — `+0x50` through `+0x58`:

```c
uint16 slot[5];        // at stats + 0x50 .. +0x59
0xFFFF                 // = empty
uint16 saved[5];       // at stats + 0x5A .. +0x63 - NOT a sixth slot; section 11
```

**What is immediately after the array is a copy of it.** `+0x5A` is not slot 5: it is the first word
of a five-word **backup** the takeaway/giveback verb pair writes and reads (section 11). Two pieces of
code index one word past the array and land in that backup; both are read there.

`0xFFFF` as the empty marker is the same convention the comparison path initialises with
(`mov word ptr [rdi + 0x28], 0xFFFF`), and it agrees with the empty-slot handling in
[`item-id-encoding-and-equipment-compatibility.md`](item-id-encoding-and-equipment-compatibility.md).

## 3. Equipping, in full

`BattleStats_SetEquipmentSlotDirect(stats, slot, itemId, updateInventory)` (`0031A630`) is the base
of the three setters, and it is short enough to give whole:

```c
if (stats == NULL) return -1;
if (itemId != 0xFFFF                                        // clearing a slot skips the check
    && !Equipment_CheckItemEligibleForSlot(&stats[0x50], slot, itemId, updateInventory))
    return -1;

old = slot16[slot];
if (updateInventory) {
    EquipmentInventory_DecrementSecondaryCountChannel(old);      // 0030F9A0
    EquipmentInventory_IncrementSecondaryCountChannel(itemId);   // 0030C410
}
slot16[slot] = itemId;
Equipment_ReconcilePrimarySecondarySlotCompatibility(&stats[0x50], slot, updateInventory); // 00318B40

if (slot16[slot] != old) {                                  // <-- the whole point
    BattleStats_RecomputeDerivedStateAndAutoStatuses(stats, 0x97);
    if (updateInventory) {
        unit = BattleStats_FindOwningBattleUnit(stats);
        if (unit) FUN_00324470(unit);
    }
}
return 0;
```

Three details that are easy to miss and change the meaning:

- **Clearing a slot bypasses eligibility.** `itemId == 0xFFFF` skips `Equipment_CheckItemEligibleForSlot`
  entirely — you can always take something off, whatever state you are in.
- **Reconciliation runs *before* the change test**, and it can itself rewrite the slot — so an off-hand
  dropped for being incompatible with a new main hand is included in "did anything change".
- **The rebuild is conditional on the slot actually differing.** Re-equipping what you already wear
  costs nothing. Note the comparison is against `old`, re-read *after* reconciliation, so the test is
  "is the array different now", not "did the caller ask for a different id".

## 4. There is exactly one place effective stats exist

`BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`) is reached from **14 direct callers
across 7 owner subsystems**, and it is the only route to
`BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`) that gameplay takes:

| Trigger | Function | Owner |
|---|---|---|
| equip / unequip | `0031A410`, `0031A510`, `0031A630` `BattleStats_SetEquipmentSlot*` | Items/Shops |
| **buying a License square** | `00323910` `BattleStats_SetLicenseNodeStateAndApplySideEffects` | Items/Shops |
| status gained or lost | `0030E130`, `0030E360`, `0030E8F0`, `0030F690` | Status |
| level change | `0030C650` `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`, `0030C470` | Rewards |
| an action's result on a target | `003112F0` `BattleFormula_ApplyTargetResult` | CombatFormula |
| unit spawn | `0023A410` `SpawnUnit_FinalizeSpawnEntryActivation` | Spawn |
| a direct state command | `002FDDA0` `BattleUnit_ExecuteDirectStateCommandOrder` | CombatAction |
| — | `00328BD0` | — |

> **Nothing in this list adjusts a stat. Every one of them invalidates and rebuilds.** That is why
> equipment needs no un-apply step, why a hundred swaps cannot drift, and why buying a License square
> — which is not an equipment operation at all — goes through the same door.

**The rebuild has a second half, documented separately.** `0030FED0` also rebuilds the **auto-status
set** from scratch — from actor type, the foe table, **five equipment slots each granting one status,
and up to eight per owned License node** — which is why equipment can grant a permanent status and
why removing it takes the status away with no un-equip logic anywhere. **The same reason stats cannot
drift, one layer up.** That mechanism is read and owned by
[`the-auto-status-rebuild.md`](../08-Combat-Formula/the-auto-status-rebuild.md) and is not
re-derived here.

**`002FEF30` has exactly two callers**, and the second one is the interesting half:

```
0030FED0  BattleStats_RecomputeDerivedStateAndAutoStatuses          the real thing
0030A4E0  Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats    the menu's preview
```

`0030A4E0` builds a *hypothetical* loadout — `uint16` ids read from a candidate block, diffed
against the live slots at **`stats + 0x50`, `+0x52`, `+0x54`, `+0x56` and `+0x58`: all five**
(`0030A565`–`0030A5BA`, corrected §10) — and runs **the same rebuild** to produce its numbers.

> **The equip menu's projected stats are not a model of the formula; they are the formula.** There is
> no second implementation to disagree with the first, which is the strongest possible answer to
> "does the preview lie?"

## 5. Key addresses

| Address | Name | Role |
|---|---|---|
| `0031A630` | `BattleStats_SetEquipmentSlotDirect` | the equip path (§3) |
| `0031A410` | `BattleStats_SetEquipmentSlotByStatsIndex` | by stats index |
| `0031A510` | `BattleStats_SetEquipmentSlotByMappedId` | by mapped id |
| `0031A710` | `BattleStats_SetEquipmentSlotsByMappedId` | whole-loadout variant |
| `0031A260`, `0031A300` | `BattleStats_ClearAllEquipmentSlots*` | clear all |
| `00317930` | `Equipment_CheckItemEligibleForSlot` | eligibility gate |
| `00318B40` | `Equipment_ReconcilePrimarySecondarySlotCompatibility` | pair reconciliation |
| `0030C410` / `0030F9A0` | `EquipmentInventory_Increment/DecrementSecondaryCountChannel` | inventory counts |
| `0030FED0` | `BattleStats_RecomputeDerivedStateAndAutoStatuses` | the invalidation point (§4) |
| `002FEF30` | `BattleStats_RebuildEffectiveStatsAndAffinityState` | the rebuild itself |
| `0030A4E0` | `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` | the preview |
| `0031B860` | `BattleStats_FindOwningBattleUnit` | stats → unit |
| `00324470` | *(unnamed)* | the unit refresh after an inventory-affecting equip or a License purchase (§7) |
| `00324380` | *(unnamed)* | the party-slot snapshot that restarts the party read-in, called by takeaway and giveback (§11) |
| `0034A300` | *(unnamed)* | the poll the takeaway / giveback verbs share: waits for that read-in (§11) |

## 6. What the rebuild does, as far as it is read

`002FEF30` takes the stats record, captures the slot array pointer (`lea rbx, [rdi + 0x50]`), zeroes
a **0x24-byte output block** (by default at `stats + 0x24`), and branches on the **record kind byte at
`+5`** — the same byte that gates the License check. It then indexes a per-character table at
`02EBF130` by the ~~**party slot at `+4`**~~ **type id at `+4`** and reads base-growth fields from that row (`+0x18`, `+0x19`,
`+0x1D`, `+0x2A`, `+0x4C`) against the record's level and related fields.

*Corrected 2026-09-30 (FABLE): `+4` is the record's type id, the party-table row, not a party slot
([the type-id partition](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md) §8);
for the main roster, rows `0`–`6`, the two coincide. The row read also takes `+0x48` (`002FF0D6`). The kind
byte's two readers, cited: the rebuild loads it at `002FEFFB` and branches on it at `002FF026`
(`test ecx, ecx` / `jne`, 0 = the party side); the License check loads it at `00323EF3`
(`movzx eax, byte ptr [rsi + 5]`) and answers "licensed" for any non-zero kind at `00323EF9`, before a
board node is read.*

`02EBF130` is **the same table the Quickening rule indexes**
([`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md)
§5) — one per-character row serving both base stats and Quickening ids.

~~**The function is 2,859 bytes and resolves runtime tables dozens of times.** What is stated above is
the prologue and the base-stat entry; **the equipment contribution proper is not read** (§7).~~
*Corrected 2026-09-30 (FABLE): the whole body, `002FEF30` to the `ret` at `002FFA5A`, is now read, and
the formula below is taken from it instruction by instruction. The stages and caps agree with
[where a stat number comes from](../08-Combat-Formula/where-a-stat-number-comes-from.md) and
[the stat-derivation contract](../08-Combat-Formula/CONTRACT-stat-derivation.md), which read the same body
first; this section adds the per-slot equipment terms, the party-side base, and which output each status
list raises. Output names are the
[battle-stats field map](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)'s;
`o` is the output block, `stats + 0x24` by default.*

### 6.1 The formula (FABLE, 2026-09-30)

```c
// stage 1 - base. kind = stats[+5] (002FEFFB). Party side (kind 0), row = 02EBF130[type]:
hp  = (row.b18 + 1) * stats.u32_08 * row.b19 / 100;   // 002FF06F-002FF07B, helper 002F8E50 (30 B)
mp  = stats.s16_0C * row.b1D / 100;                   // 002FF080-002FF090, helper 002F9180 (21 B)
str = (int)stats.f32_10;  mag = (int)stats.f32_14;    // cvttss2si 002FF0C2, 002FF0CD
vit = (int)stats.f32_18;  spd = (int)stats.f32_1C;    // cvttss2si 002FF099, 002FF0B7
innateEvade = row.b2A;    mpBars = stats.b20;         // 002FF095, 002FF0AA
o.u32_14 |= row.u32_4C;   o.u32_18 |= row.u32_48;     // 002FF0D3, 002FF0D9
atk = def = mRes = wEvade = sEvade = mEvade = 0;      // zeroed at 002FEFB1-002FEFF1
// Foe side (kind != 0): every term is growth * (stats[+0x1C2] - stats[+0x88]) + base + own
// (002FF0E1-002FF3C8), read on the stat page, "The foe side"; there mpBars = 0.

// stage 2 - equipment, five slots (002FF3F0-002FF57B; cmp rbp, 5 at 002FF577)
for (s = 0; s < 5; s++) {
    id = slot[s];
    if (!BattleEncodedId_IsValidForClass(6, id)) continue;   // 002FF3FB / 002FF402: an invalid id adds nothing
    item = row of 02EBF0F8 at (id - 0x1000) * stride;        // 002FF430-002FF448
    switch (item category) {                                  // 0031E9A0 at 002FF451
    case 1: if (weaponTerms) { atk += item.b1A; wEvade += item.b1D; }  break;  // 002FF48E-002FF4A4
    case 2: if (shieldTerms) { sEvade += item.b18; mEvade += item.b19; } break; // 002FF477-002FF48A
    case 3: def += item.b18; mRes += item.b19;                  break;  // 002FF465-002FF471
    }                                                        // any other category: no pair
    sub = resolve(item.u32_28);                              // EVERY valid item, 002FF4A7-002FF571
    hp  += sub.u16_00;  mp  += sub.u16_02;
    str += sub.b04;  mag += sub.b05;  vit += sub.b06;  spd += sub.b07;
    o.u32_14 |= sub.u32_0C;  o.u32_18 |= sub.u32_08;
    o.b1C |= sub.b13;  o.b1D |= sub.b10;  o.b1E |= sub.b12;  o.b1F |= sub.b11;  o.b20 |= sub.b14;
}
// weaponTerms and shieldTerms start at 1 (002FEF56, 002FF0B2 / 002FF37C) and are cleared only on the
// foe side, by the authored definition's +0x15 bit 0 (002FF351) and bit 1 (002FF3AD).

// stage 3 - statuses: a status in either layer (stats +0x68 / +0x78 bit arrays) adds the u16 at +4
// of its row in the 02EBF040 table.
for (i < 16) if (has(listA[i])) str += statusRow(listA[i]).u16_04;  // list at image + 0xBF0290, 002FF5B2-002FF63C
for (i < 16) if (has(listB[i])) mag += statusRow(listB[i]).u16_04;  // list at image + 0xBF02A0, 002FF650-002FF6DA
for (i < 12) if (has(listC[i])) hp  += statusRow(listC[i]).u16_04;  // list at image + 0xBF02B0, 002FF6F0-002FF77A

// stage 4 - clamp and store (002FF7B1-002FF96D)
o.u32_00 = clamp(hp, 1, kind == 0 ? 9999 : 1000000000);   // max HP, stats +0x24; floor 1, not 0
if (kind == 0 && (uint8)(type - 0x1B) <= 0x0C)            // the Espers, 002FF007-002FF011
    o.u32_00 = clamp(hp, 1, 32767);                        // second store, 002FF7E5-002FF805
o.u16_04 = clamp(mp, 0, 999);                              // MP capacity, stats +0x28
o.b06..o.b09 = clamp(str / mag / vit / spd, 0, 99);        // stats +0x2A..+0x2D
o.b0A = clamp(atk, 0, 255);  o.b0B = clamp(def, 0, 255);  o.b0C = clamp(mRes, 0, 255);  // +0x2E..+0x30
o.b0D = clamp(innateEvade, 0, 100);  o.b0E = clamp(wEvade, 0, 100);                     // +0x31, +0x32
o.b0F = clamp(sEvade, 0, 100);       o.b10 = clamp(mEvade, 0, 100);                     // +0x33, +0x34
o.b11 = clamp(totalEvadeMod + sEvade + wEvade + innateEvade, 0, 100);  // +0x35, sum at 002FF79A-002FF7A5
o.b12 = clamp(magickEvadeMod + mEvade, 0, 100);                        // +0x36, sum at 002FF7A7-002FF7AE
o.b13 = min((unsigned)mpBars, 3);                                       // +0x37, 002FF889-002FF89F
// totalEvadeMod / magickEvadeMod are the foe record's own i16 +0x1E / +0x20 (002FF2D6, 002FF2F1); 0 on the party side.
```

**What this answers.** Base, then equipment, then statuses, then one clamp per output — and **nothing in
the equipment or status stages multiplies**: every term is an `add`, and the flag words are `or`-ed. The
only products are in stage 1 (the party side's two `/ 100` level helpers, the foe side's growth × level
span). So an item's contribution does not depend on the character's level or on any other item, and it
is the same for every character who can wear it. **An item contributes twice**: once through its
category's stat pair, and once, whatever its category, through the sub-record its row `+0x28` names —
which is how a weapon can raise HP or Strength. The two evasions of a weapon and a shield are counted
twice as well, once in their own byte and once in the evade total `+0x35`.

## 6a. Call chain (FABLE, 2026-09-30)

```
an equip request: the equip menu, a script verb, the loadout builder; giveback and clear-all through ...ByMappedId
  -> BattleStats_SetEquipmentSlotByStatsIndex / ...ByMappedId / ...Direct   (0031A410 / 0031A510 / 0031A630)
     -> Equipment_CheckItemEligibleForSlot (00317930)          gate; skipped for 0xFFFF (§3)
     -> Equipment_ReconcilePrimarySecondarySlotCompatibility (00318B40)
     -> [the slot array changed]
        BattleStats_RecomputeDerivedStateAndAutoStatuses (0030FED0, flags 0x97)   <- OWNER transition
           -> BattleStats_RebuildEffectiveStatsAndAffinityState (002FEF30)        <- THIS SYSTEM (§6)
              -> [+0x3C bits 5 / 27 changed] the in-flight action is cancelled (the stat page, "The tail")
           -> the auto-status rebuild, the same call's second half (§4)
        -> [inventory-affecting] 00324470 on the owning unit (0031B860)            (§7)
the equip menu's preview
  -> Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats (0030A4E0) -> 002FEF30   (§4)
```

**Upstream (who causes this).** Fourteen caller functions of `0030FED0` over 25 call sites (§4, §10); the
setters are three of them. `0031A630` itself has three callers (§10). `00324470` has four raw call sites:
the three setters (`0031A4DF`, `0031A602`, `0031A6ED`) and the License purchase
`BattleStats_SetLicenseNodeStateAndApplySideEffects` (`00323A48`). **The owner transition is `0030FED0`**;
equipping is one trigger of it, not the owner.

**Downstream (what this causes).** Stats `+0x24`–`+0x37` are recomputed from nothing, and bits are OR-ed into
the words at `+0x38` / `+0x3C` and the bytes `+0x40`–`+0x44` (§6.1). What reads each output is tabulated in
[the battle-stats field map](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md), and
the evasions' spender is [the formula scratch block](../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md)
§2.3.

**Do not confuse with:** the level-up growth, which changes the base terms `+0x08`–`+0x1C` that stage 1 reads
([what happens when a character levels up](../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md));
the auto-status rebuild, which runs in the same call and owns the status set
([the auto-status rebuild](../08-Combat-Formula/the-auto-status-rebuild.md)); and the takeaway / giveback backup
(§11), which moves slot words and never computes a stat itself.

## 6b. Modding notes (FABLE, 2026-09-30)

- **Best intervention point:** the item row. An item's stat pair (`+0x18` / `+0x19`, or `+0x1A` / `+0x1D` for a
  weapon) and its sub-record (`+0x28`) are read on every rebuild, so an edit to them takes effect at the next
  trigger with no code change. In code, `002FEF30` is the one place to hook: it serves the live stats and the
  menu preview alike, so a hook there cannot make the preview disagree.
- **Regenerates itself:** stats `+0x24` through `+0x47` are zeroed and rebuilt on every trigger (§4). A direct
  write to one of them lasts only until the next equip, status change, level change, License purchase or action
  result.
- **Breaks if:** an id fails the class-6 validity check — it is skipped silently, so a bad id in a slot looks
  like an empty slot rather than an error. A clear-slot call with an index above 4 writes into the takeaway
  backup (§11.6). An item whose category is not 1, 2 or 3 adds no stat pair, but its sub-record still counts.
- **Multiplayer / XIIOnline:** the slot words `+0x50`–`+0x58` (and the backup `+0x5A`–`+0x63`) are the state
  to replicate; `+0x24`–`+0x37` are derived and should be recomputed on each client by the same function. A
  client that replicated the derived bytes would lose them at its own next trigger.
- **Mod compatibility:** the item rows are authored data other mods may change; the three status-id lists live
  in the executable image, not in an authored file, so regrouping which status raises which stat is a code patch.

## 7. What is not known

- ~~**The equipment contribution formula.** How a slot's item row turns into a stat delta inside
  `002FEF30` — the ordering of base, equipment, License and status contributions, and whether any of
  them multiply rather than add. **This is the substance of the rebuild and it is not read here.**~~
  **ANSWERED 2026-09-30 (FABLE), §6.1, from the whole body:** base, then five equipment slots (a category
  stat pair plus a sub-record for every valid item), then three status lists, then one clamp per output; the
  equipment and status stages only add and OR. License nodes add no stat term inside `002FEF30`: they reach
  it only as a trigger (`00323910`, §4) and through the auto-status half of `0030FED0`.
- ~~**What `0x97` means** as the second argument to `BattleStats_RecomputeDerivedStateAndAutoStatuses`.~~
  ~~Every caller passes some constant; only the equip path's was read.~~ **ANSWERED 2026-09-10 by reference:**
  inside the recompute only bits 1 (forced on at entry), `0x10` and `0x400` are tested — `0x10` suppresses
  the `+0x4E` charge notification — and `0x97 = 0x80 | 0x10 | 4 | 2 | 1` otherwise rides through to
  `0030E130` and `0030E360`; all 25 call sites' constants are tabulated in
  [the auto-status rebuild](../08-Combat-Formula/the-auto-status-rebuild.md), "What the flags do here".
- ~~**What `FUN_00324470(unit)` does** after an inventory-affecting equip — *narrowed §10*: it
  re-applies bit 23 of `[unit]` through `002ECF10(unit->[0x10], bit, 0)`, calls `003105D0(unit)`,
  and then tests the battle record `[unit+0x698]`'s `+0x64 | +0x3C` against `0x80000003` before
  `00313F60`. **Its callees are not read**, so what it refreshes is still open.~~
  **ANSWERED 2026-09-30 (FABLE), body read whole (122 B) with its callees:** it is the unit refresh the
  retire helper `003243F0` performs, bracketed by two extra steps.
  (1) The engaged flag, bit 23 of the unit's flag word (`00324482`–`00324485`), is re-sent to the unit's
  render-side record (`00324488`; the setter it reaches is one of the render record's `+0x294` flag setters,
  [the character render record array](../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md)).
  (2) `BattleUnit_CancelAndResetCurrentAction` (`00324490`).
  (3) A unit that is down — `+0x64 | +0x3C` carrying a bit of `0x80000003` (`003244A1`–`003244AC`) — without
  the field's bit-15 waiver (`003244AE`) and not already torn down (flag bit 1, `003244B7`) goes through
  `BattleUnit_TeardownAndDespawn(unit, 0)` (`003244C1`).
  (4) The three actor-work resets the retire helper also runs (`003244CA`, `003244D3`, `003244DC`; described on
  [how a battle unit is built](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)).
  (5) **Unit flag bit 6 is set** (`003244E1 or dword ptr [rbx], 0x40`). Its only consumer, `00324450`, is
  called once, from `BattleUnit_ActivateAppliedDefinitionRuntime` (`00233B46`): when bit 6 is set it runs
  `003243F0` again and clears the bit (`00324456`–`00324463`). So an equip or a License purchase refreshes the
  unit at once and **marks it for one more refresh at its next definition activation**. What the render record
  does with its flag bits is that page's subject and is not re-derived here.
- ~~**The slot count.**~~ **Answered §10: five, `0`–`4`.** `Equipment_CheckItemEligibleForSlot`
  opens `movsxd rsi, r8d / cmp esi, 4 / ja` (`0031793D`–`0031794D`), so the bound is unsigned and
  a negative index fails with the rest. The preview diffs five slots, and §4's "five equipment
  slots" agrees.
- ~~**What the `[rdi+4] - 0x1B <= 0xC` range in the rebuild's prologue selects** — a 13-wide band of
  slot indices taking a different path.~~ **ANSWERED by reference, 2026-09-30 (FABLE):** `+4` is the type id,
  not a slot index, and `0x1B`–`0x27` is **the thirteen Espers**
  ([the type-id partition](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md)
  §8–§9). The band sets a flag at `002FF011` only for kind 0, and its one effect in the rebuild is the second
  store of max HP with the cap **32,767** (`002FF7E5`–`002FF805`, §6.1) —
  [the stat-derivation contract](../08-Combat-Formula/CONTRACT-stat-derivation.md) §14 reads the same condition and
  OPUS's replay executed it.
- ~~**What `0x1000` is as an item id**~~ (§10 "Not claimed"). **Answered on the sibling page, 2026-09-20:**
  it is **Unarmed** — [`item-id-encoding-and-equipment-compatibility.md`](item-id-encoding-and-equipment-compatibility.md)
  records that `Equipment_BuildRecommendedLoadoutForMappedStats` turns an empty hand into `0x1000` after
  slot 0, and `0x1000` is category 1's own base, so the id is that category's row 0. This is why the
  eligibility short-circuit table's only real entry is `(slot 0, 0x1000)` and why the AI condition in
  §11 counts `0x1000` as *not* equipped: bare hands are a weapon record, not an occupied slot.
- ~~Whether `00328BD0`, the unnamed trigger, is gameplay or tooling.~~ **Gameplay — already
  answered in the register.** `FZ-6` (2026-09-11) names it: it is
  `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`, reached by the script verb
  **`resetJobs` (`05D6`)** through `00342230` and the family-0 handler table, as well as by the
  definition initialiser and the SetSaveData apply. §10.
- **What battle actions `0x9C` and `0x9D` do** — the two the battle menu issues when the selected entry is, or is
  not, the stashed slot-0 item (§11.3). Their action rows name no action: both point at a *Reserve* placeholder in
  the battle text (2026-09-30, §11.3). Registered as **`GR-12`**.
- **Whether any shipped AI order authors the one-past-the-array slot `N = 5` (§11.4)** — **ANSWERED 2026-09-30
  (FABLE), static, from the authored data: none does** — no shipped order uses the equipment-slot selectors at
  all (§11.4).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Slots are `uint16` at `stats + 0x50 + slot*2` | `lea r14,[rbx+rbp*2]` / `[r14+0x50]` in `0031A630`; `[rbp+0x50/0x52/0x54]` in `0030A4E0` | 1 |
| `0xFFFF` is the empty marker | `mov eax,0xFFFF ; cmp si,ax ; je` skipping the eligibility call | 1 |
| Clearing bypasses eligibility | the same branch target skips `call 0x317930` | 1 |
| Reconciliation precedes the change test | instruction order: `call 0x318B40` then `cmp word [r14+0x50], r15w` | 1 |
| The rebuild fires only on a real change | `cmp` / `je` around `call 0x30FED0` | 1 |
| 14 triggers over 7 owners | direct-and-thunk caller census of `0030FED0` | 1 |
| `002FEF30` has exactly 2 callers | same census; 0 thunks | 1 |
| The preview uses the same rebuild | `0030A4E0` calls `002FEF30` directly | 1 |
| The rebuild indexes `02EBF130` by the ~~slot~~ type id at `+4` | `movzx ecx, byte [rdi+4]` / `imul ebx, ecx` (`002FF061`–`002FF065`) | 1 |
| The rebuild's stages and every term of §6.1 | `002FEF30` read whole, `002FEF30`–`002FFA5A`; each term cites its instructions in §6.1 | 1 |
| The party-side base helpers | `002F8E50` (30 B) and `002F9180` (21 B) read whole: `(r8 + 1) * ecx * edx / 100` and `ecx * edx / 100`, both by `0x51EB851F` / `sar 5` | 1 |
| Status list A raises Strength, B Magick Power, C max HP | the accumulator each loop adds to: `r12d` (`002FF632`), `r13d` (`002FF6D0`), `r14` (`002FF770`), stored at `002FF840`, `002FF85A`, `002FF7E2` | 1 |
| The kind byte gates the License check | `00323EF3 movzx eax, byte ptr [rsi + 5]` / `00323EF9 jne` to the "licensed" return | 1 |
| `00324470`'s steps and its four callers | body read whole; raw call index (`rawcalls.py 00324470`): `0031A4DF`, `0031A602`, `0031A6ED`, `00323A48` | 1 |
| Bit 6's consumer reruns the retire helper once | `00324450` read whole; its one caller site `00233B46` (raw call index) | 1 |
| No shipped order authors selector `0x1A` / `0x1B` | `eq_slot5_census.py` over the 166 `in` `.ard` files (controls: 1,422 sets, 50,050 records, 18,206 first operands of 1 and 8,999 empty, as §7a of the loader page and Z-15B give); `eq_slot5_party.py` over the 256 gambit target-condition rows (control: `+0x10` only 1 / 2 / 4, as Z-15 gives); scripts in `_index/candidates/dd-content-fable-0930/` | 9 |
| Actions `0x9C` / `0x9D` carry placeholder names | `eq_action_names.py`: action row `+0x34` into battle-text bank 0 (controls `0x95` Dismount, `0x113` Dismiss, as AT-9 gives) | 2 |

**Controls.** The claim *"there is no apply-a-bonus path"* is bounded by a caller census, and it means
precisely: **no function in the corpus reaches `002FEF30` except those two, and every gameplay route
to it invalidates rather than adjusts.** It is **not** a claim that no code anywhere writes a stat
field directly — `BattleStats_SetCurrentHP` and its neighbours plainly do. The distinction matters
and §4's wording depends on it.

One decode in §6 was discarded: a first read of the rebuild's middle began mid-instruction and
produced `mov bl,0 / add byte [rax],al`, which is not code. **A disassembly that starts at an
arbitrary offset is a guess about instruction boundaries**, and the region was re-read from a known
boundary before anything here was written.

`check_already_answered.py` was run for these addresses and terms before this document was started.

## 9. Related

- [`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md) — the eligibility check equipping must pass, and the other user of `02EBF130`.
- [`item-id-encoding-and-equipment-compatibility.md`](item-id-encoding-and-equipment-compatibility.md) — item id encoding and the primary/secondary compatibility rule the reconciler enforces.
- [`experience-and-license-point-award.md`](../13-Rewards-Progression-Economy/experience-and-license-point-award.md) — level change, one of the 14 triggers.
- [`where-a-stat-number-comes-from.md`](../08-Combat-Formula/where-a-stat-number-comes-from.md) and [`CONTRACT-stat-derivation.md`](../08-Combat-Formula/CONTRACT-stat-derivation.md) — the same rebuild, read first: the foe side, the caps, the stat-change tail.
- [`the-battle-stats-record-field-map.md`](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) — what each rebuilt output is and who reads it.
- [`actor-type-id-partition-and-the-13-value-band.md`](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md) — the type id at `+4` and the Esper band.
- [`the-party-read-in-state-machine.md`](../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md) — the read-in task takeaway and giveback start and wait for (§11).

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` re-run on the addresses this pass introduced; it returned `FZ-6`, which
answers one of §7's items — see below. Static only. Nothing executed.)*

### The censuses reproduce, and two of them gain a number

| claim | measured |
|---|---|
| `0030FED0` — **14 direct callers**, 7 owners | **14 distinct caller functions**, and **25 call sites** — the same 25 the auto-status page tabulates |
| `002FEF30` — **exactly 2 callers, 0 thunks** | **2**, `0030A4E0` and `0030FED0`, **0 `E9`** |
| `0031A630`'s own body against §3 | matches instruction for instruction — `cmp si, ax` → skip `00317930`; `old` captured at `0031A68E`; `0030F9A0` / `0030C410`; the store; `00318B40`; the re-read compare at `0031A6BB`; `0030FED0`; `0031B860`; `00324470` |

Two censuses the page does not have: **`00317930` has 5 callers** — the three setters plus two
wrappers §5 does not list, `Equipment_CheckItemEligibleForSlotByStatsIndex` (`00317B20`) and
`Equipment_CheckItemEligibleAgainstCurrentLoadoutByStatsIndex` (`00317B70`) — and **`0031A630` itself
has 3 callers over 16 sites**: `00239960`, `BattleStats_InitializeDefinitionRecord` (`0023AC80`) and
`Equipment_UnequipEncodedItemFromActiveRoster` (`0030FD10`).

**One wording sharpened.** §3 says the comparison is against *"`old`, re-read after reconciliation"*.
The order is the other way round: `old` is captured **before** the store (`0031A68E`), and it is the
**slot** that is re-read after reconciliation (`0031A6BB`). §3's own next clause — *"is the array
different now"* — is the correct reading; the parenthesis contradicts it.

### ✔ Answered: there are five slots, `0`–`4`

§7 says the bound lives in `Equipment_CheckItemEligibleForSlot` and is unread. It is the fourth
instruction:

```asm
0031793D  movsxd rsi, r8d          ; the slot argument, sign-extended
00317940  movzx  ebx, r9w          ; the item id
0031794A  cmp    esi, 4
0031794D  ja     0x317B0D          ; reject
00317953  lea    rcx, [00D107E8]   ; a five-entry u16 table
0031795A  cmp    bx, word [rcx + rsi*2]
0031795E  jne    ...               ; equal -> accept with no further checks
```

**Five slots**, and because the compare is **unsigned after a sign-extend**, a negative index fails
with everything above 4. This is also what §4 already assumes when it says *"five equipment slots each
granting one status"*, and what the preview does — see the correction below.

**The short-circuit table is `1000 FFFF FFFF FFFF FFFF`.** So the only slot whose entry is a real id
is **slot 0, against `0x1000`**; the other four entries are the empty marker, which the very next
branch handles anyway. The table accepts one (slot, id) pair without eligibility, and that pair is
`(0, 0x1000)`.

### ✖ Corrected: the preview diffs five slots, not three

§4 says `0030A4E0` diffs the candidate against *"`stats + 0x50`, `+0x52`, `+0x54`"* and reads *"four
`uint16` ids"*. It compares **five**: `0030A565`, `0030A585`, `0030A59A`, `0030A5A8` and `0030A5BA`
test `+0x50`, `+0x52`, `+0x54`, `+0x56` and `+0x58`. With the bound above that is the whole slot
array, which is what "the preview *is* the formula" requires — a preview that diffed three of five
would be a preview that could disagree.

### ✔ Answered from the register: `00328BD0` is gameplay

§7's last item asks whether the unnamed fourteenth trigger is gameplay or tooling. **`FZ-6` answered
it on 2026-09-11**: `00328BD0` is `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`, and the
script verb **`resetJobs` (`05D6`)** reaches it through `00342230` and the family-0 handler table at
`01EF91E0` — alongside the definition initialiser and the SetSaveData apply. **Gameplay**, and the
answer was one register row away from the question. Credited, not re-derived.

### ○ Narrowed: `FUN_00324470`

`00324470` reads `[unit]`, takes **bit 23** (`shr edx, 0x17 / and edx, 1`), passes it with
`[unit + 0x10]` to `002ECF10`, calls `003105D0(unit)`, then tests the battle record `[unit + 0x698]`'s
`+0x64 | +0x3C` against **`0x80000003`** and calls `00313F60` when it passes. A unit refresh, then —
**its callees were not read**, so §7's item stays open with a shape rather than a meaning.

**Not claimed.** The equipment contribution formula — **`002FEF30`'s 2,859 bytes were not re-read
here**, and §6 stands as written. What `0x1000` is as an item id. What `002ECF10`, `003105D0`,
`00313F60` do. The `[rdi+4] - 0x1B <= 0xC` band. Nothing was executed.
*(Since answered, 2026-09-30 (FABLE): the formula in §6.1; `00324470` and its callees, and the band, in §7.)*

## 11. `+0x5A` is the takeaway backup, not a sixth slot — 2026-09-20 (FABLE, Claude Opus 5)

**The question, from the structural lane.** An indexed accessor admits six equipment slots where this
page names five: `00302416` is `cmp edi, 5` / `ja`, and `00302428` then reads
`word [rax + rcx*2 + 0x50]`, so indices `0`–`5` pass and the read can reach `+0x5A`. Is the array five
or six? `+0x5A` is separately declared in the type store, with its own direct reader.

**Five. The sixth index reads the first word of a backup copy of the same array.**

### 11.1 What writes `+0x5A` (FABLE)

`InventoryEquipment_SnapshotAndClearTemporaryState` (`0030FBE0`) walks mapped battle slots `0`–`8` and,
for each stats record it gets from `BattleStats_GetByMappedBattleSlot` (kind 3), does exactly this:

```
0030FC16  movzx ecx, word ptr [rax + 0x58]     ; slot 4
0030FC1F  movsd xmm0, qword ptr [rax + 0x50]   ; slots 0-3, eight bytes
0030FC24  movsd qword ptr [rax + 0x5a], xmm0   ; -> +0x5A +0x5C +0x5E +0x60
0030FC29  mov   word ptr [rax + 0x62], cx      ; -> +0x62
0030FC2F  call  0x31a300                       ; BattleStats_ClearAllEquipmentSlotsByMappedId
```

Five live words copied to `+0x5A`..`+0x63` **in slot order**, and then the live five are cleared. It is
a save-and-strip, and it is the **only** write to `+0x5A` anywhere in the image: a displacement sweep of
`0x5A` over the whole `.text` finds one wide access (this one) and, in the battle band, one further
word-sized access — the display-record copier of §11.3. There is no second writer and no other array
that starts there.

### 11.2 What reads it back, and what it is for (FABLE)

`InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` (`0030FAA0`) restores the inventory from its
own backup tables and then, per mapped slot, forms `rdx = stats + 0x5A` (`0030FB94 add rdx, 0x5a`) and
calls `BattleStats_SetEquipmentSlotsByMappedId` (`0031A710`), whose loop is
`movzx r8d, word ptr [rsi]` … `lea rsi, [rsi + 2]` … `inc edi` … `cmp edi, 5` / `jl` — **five words, read
from the backup, written back into slots 0–4**. The backup is the argument; the array is the destination.

Both routines are script verbs, and the verb table names them:

| verb | call id | shape | native |
|---|---|---|---|
| `takeaway_item_and_equip` | `0x388` | durative (begin `00349F90`, poll `0034A300`) | `0030FBE0` |
| `giveback_item_and_equip` | `0x387` | durative (begin `0034A790`, poll `0034A300`) | `0030FAA0` |

So the mechanism is an authored story event: **`takeaway` stashes the party's five equipment words and
its inventory and strips them; `giveback` puts both back.** The stats-side backup is not cleared by the
restore — `0030FBB1`–`0030FBC7` memsets the *inventory* backup at `[02EBF190] + 0x4F84` for `0x83C`
bytes and leaves `+0x5A`..`+0x63` holding the last stashed loadout.

### 11.3 The "sixth equipment word" a consumer reads is `saved[0]` (FABLE)

`00329220`, which builds the unit display record, copies **six** words in an unrolled run —
`+0x50`, `+0x52`, `+0x54`, `+0x56`, `+0x58` and, at `00329738`, `+0x5A` — each `<< 16`, into the record's
`+0x98`…`+0xAC`. The sixth of those is `saved[0]`, not a sixth slot; the uniform shape of the copy is
what made it look like one. `FUN_00273270` presets its stack record's `+0xAC` to `0x0000FFFF`, fills it
through `0031FF70` → `00329220` (mode `full`), and returns `+0xAC >> 16`: **the actor's stashed slot-0
item**. Its five callers are all battle-menu bodies (`0027AD70`, `0027C3D0`, `0027CE70` ×2, `0027D740`);
in `BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands` the selected entry's id
(`0027C61C movzx edi, word ptr [rdx + 0x50]`, the 8-byte entry at container `+0x50 + index*8`) is
compared against that return and chooses command `0x9D` over `0x9C`
(`BattleUnit_IssueCommandByFocusHandles`). ~~*What the two command ids are is not read here*, and the
failure preset makes the "nothing to compare" answer `0`, not `0xFFFF` — that asymmetry is not explained
either.~~ *Narrowed 2026-09-30 (FABLE).* The branch is `0x9D` when the entry equals the stashed item **or is
`0xFFFF`** (`0027C625`–`0027C632`, issued at `0027C65A`), and `0x9C` otherwise (`0027C637`). The ids are action
ids in the same numbering as `0x113` and `0x95`, the command ids AT-9 named from their action rows, so
they were looked up the same way: action row `+0x34` into bank 0 of the battle text. **Both rows point at a *Reserve*
placeholder** (bank 0 entries 156 and 157, category byte `+0x1E` = 13; `eq_action_names.py`, whose controls
read Dismount and Dismiss), so the shipped text gives them no name. What the two actions do stays open as **`GR-12`**. *(Narrowed 2026-09-30, FABLE, [record](../_index/candidates/gr12-actions-9c9d-fable-0930/README.md), `gr12_facts.py` FAILS 0: the menu side is read: in `0027C3D0`'s container-kind switch (table `0027C6B8`) only kind 11 issues an entry whose own id is `0x9C` / `0x9D` at once as that action (`00311CD0(unit, unit, id, 0)`, `0027C5FE`), and only kind 24 runs the stashed-item compare; ~~the list body `0027CF2A` offers them only while the actor has a takeaway backup (`00273270` not `0xFFFF`, `0027D14D`);~~ *(corrected 2026-10-01, OPUS, on SWE2-AUDIT-SEM's C4, [review](../_index/candidates/auditsem-review-gr19-gr11-0930/REVIEW.md):)* the list body `0027CE70` draws a `0x9C` / `0x9D` entry either way; while the actor has a takeaway backup (`00273270` not `0xFFFF`, `0027D14D`) it sets the entry's state word `+0x5A` the other way round from the default (`0x40` when flag bit 0 is clear, else `0x80`) and, with flag bit 0 set, `+0x15EF` = 6; what the two states show is not read; kind 11 needs entry `+0x54` bit 0 clear, and kind 24 needs `+0x52` bit 0 clear; rows `0x9B`-`0x9D` are the only category-13 rows and are near-empty (`+0x22` = `0xFFFF`); a sweep finds no other test of the ids and no category-13 compare. ~~Open: what an issued `0x9C` / `0x9D` changes when it executes, and which screens kinds 11 and 24 are.~~)* **GR-12 ANSWERED 2026-09-30 (SWE2-CONTRACT for OPUS `59ec09a95`, [record](../_index/candidates/gr12-actions-9c-9d-0930/README.md); register restated 2026-10-01; reviewed ACCEPT-WITH-NARROWING by SWE2-AUDIT-SEM, [review](../_index/candidates/auditsem-review-gr19-gr11-0930/REVIEW.md)):** neither does anything. `0x9B`-`0x9D` are the effect-free category-13 rows of a cut battle-menu Gambits sub-list, named only in the de and fr text. An issued `0x9C` or `0x9D` is refused before commit for a party unit (`003060E0` returns 5, `00306480` gives reason `0x0F`), the kind-24 list that would issue them is always built empty, and no order set names them. `00273270`'s `0x0000FFFF` preset never survives `00329220`'s memset. The "no category-13 compare" zero holds under the review's wider census, which covers the direct-compare form (F6). ~~and why an empty
failure answer is `0` where the entry's empty marker is `0xFFFF`~~ *(Corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../_index/candidates/auditsem-review-dd-gameplay-0930/REVIEW.md) C1; record [`dd-gameplay-corrections-fable-0930`](../_index/candidates/dd-gameplay-corrections-fable-0930/README.md))*: `00273270` answers **`0xFFFF`** on both early exits (id 0 at `0027328F`, no actor at `00273299`, both to `002732C1` `mov eax, 0xffff`). It answers 0 only when the filler `0031FF70` leaves the preset: the dword `[rsp+0xCC]` is preset to `0x0000FFFF` (`002732A7`) and returned `>> 16` (`002732BC`), because the filler stores the item as `word << 16`, so the preset's sentinel sits in the low half the shift discards. That is mechanics, not residue.

### 11.4 The AI condition that indexes one past the array (FABLE)

`00302416` sits in `AiOrder_EvaluateTargetSelector`. Its jump table resolves: the byte table at
`00303680` and the dword table at `00303604` route **selector ids `0x1A` and `0x1B`** to this block, and
nothing else does. The operand is the order entry's own byte — entries are six bytes from `record + 6`,
`{u16 @+0, u8 operand @+2, u8 selector @+3, i16 @+4}` (`00301B0F`–`00301B34`) — and the answer is
`value != 0xFFFF && value != 0x1000`, compared against the selector's low bit
(`00301B44 not r12d / and r12d, 1`). So **`0x1A` = "equipment slot N is occupied", `0x1B` = "slot N is
empty"**, with bare hands (`0x1000`) counting as empty.

`cmp edi, 5` admits `N = 5`, which reads `saved[0]` — the loadout stashed by the last `takeaway`, or
zero if there has never been one, since the record's `memset` at `0023ACBD` is the only thing that ever
initialises those bytes (`0023AC80` seeds `0xFFFF` into exactly five words, `+0x50` through `+0x58`, and
stops). ~~**Whether any shipped AI order authors `N = 5` is not settled here.** The instrument that would
settle it is a census of the authored order entries for selector byte `0x1A`/`0x1B` and operand byte 5;
the order records reach `AiOrder_EvaluateAndResolveActionTarget` as an argument from
`BattleUnit_TrySelectAndCommitAiOrderFromSet` (`00305CC0`, from the unit's `+0x714`), and that table was
not located. Until it is, `N = 5` is a **reachable-in-principle overread of one slot**, not a documented
condition.~~ **ANSWERED 2026-09-30 (FABLE), static, from the authored data: no shipped order authors it —
nor either equipment-slot selector at all.** The two authored sources of order records are located on other
pages: the enemy order sets in `.ard` directory slot 1
([the area-file loader](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)
§7a, `Z-2`), and the party's gambit target-condition rows, which `GambitRuntime_RebuildOrderSetFromConfig`
copies into the entries (row word `+8` into entry `+2` at `00328226`, row byte `+0x10` into entry `+0` at
`0032822E`). The switch byte is entry `+3` (`00301B14`, dispatched at `00301EA3`) and the slot is entry `+2`
(`00301B1A`). Over **1,422 sets / 50,050 records** the non-empty entries use 37 distinct switch values and
none is `0x1A` or `0x1B`; over the **256** condition rows the switch byte takes 22 values, none of them
`0x1A` or `0x1B` (`eq_slot5_census.py`, `eq_slot5_party.py`; controls in §8). So **`N = 5` stays a
reachable-in-principle overread with no shipped author**: only a modded order could reach it.

### 11.5 Why the five is not just a compiler idiom (FABLE)

The bound that decides the array is not `cmp edi, 5`. Five independent bodies agree, and none of them
derives from another:

| witness | instruction | says |
|---|---|---|
| `Equipment_CheckItemEligibleForSlot` `00317930` | `0031793D movsxd rsi, r8d` / `cmp esi, 4` / `ja` | slots `0`–`4`, negatives excluded |
| its short-circuit table `00D107E8` | `1000 FFFF FFFF FFFF FFFF` | **five** entries |
| `BattleStats_InitializeDefinitionRecord` `0023AC80` | `qword [rdi+0x50] = -1` then `word [rdi+0x58] = 0xFFFF` | **five** empty markers seeded, `+0x5A` left to the memset |
| `BattleStats_SetEquipmentSlotsByMappedId` `0031A710` | `cmp edi, 5` / `jl` | **five** written per record |
| `Equipment_UnequipEncodedItemFromActiveRoster` `0030FD10` | `mov edi, 0x50` … `add rdi, 2` / `cmp ebx, 5` / `jl` | **five** scanned per record |
| `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` | five compares, `+0x50` `+0x52` `+0x54` `+0x56` `+0x58` | **five** diffed (§10) |

### 11.6 What a reconstruction must emit (FABLE)

```c
uint16 equipmentSlots[5];   // +0x50 .. +0x59, 0xFFFF = empty, 0x1000 = Unarmed in slot 0
uint16 equipmentSaved[5];   // +0x5A .. +0x63, written by takeaway, read by giveback, never cleared
```

`uint16[6]` at `+0x50` would be wrong in the other direction from `uint16[5]`: it would swallow the
backup's first word and make `giveback` overwrite a live slot. **A caution for either shape:** the three
setters — `BattleStats_SetEquipmentSlotByStatsIndex` (`0031A410`), `…ByMappedId` (`0031A510`) and
`…Direct` (`0031A630`) — do **not** bound the index themselves; they take it `movsxd`-widened straight
into `lea r14, [rbx + rbp*2]`. The only bound is inside `Equipment_CheckItemEligibleForSlot`, and
`itemId == 0xFFFF` **skips that call** (`0031A65E`–`0031A666`). A clear-slot call with an index above 4
therefore writes into the backup. Every in-image caller passes `0`–`4`; a reimplementation that exposes
these setters to anything less disciplined needs its own bound.

~~**Not read here:** the two battle-menu command ids `0x9C` / `0x9D`; the poll body `0034A300` the two
verbs share; the authored order table behind §11.4; what `FUN_00324380` (called by both the snapshot and
the restore) refreshes.~~
*Read 2026-09-30 (FABLE).* **`00324380`** walks battle slots `0`–`3`: for each unit it resets the actor's
`+0x23` byte, then records the record's type id (`003243C1`) — or `0xFF` when the slot is empty or unit
flag bit 2 is clear — into four consecutive bytes, and then tail-jumps (`003243E7`) into the installer of the
party read-in task, one of the four reconcile callers
[the party read-in state machine](../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md)
lists. **`0034A300`**, the poll both verbs share, is a member of the generated
`NativeAdapter.PredicateGuardConstCall` family: it returns 1 and sets the VM wait byte (`0034A312`, the
shared setter's argument 1) while its predicate holds, and 0 otherwise. The predicate is a chain of three
boolean wrappers ending at the read-in task's end test — true while the task has not yet rebuilt all four
roster slots ([how a script changes the battle party](../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md)
§4). So **takeaway and giveback each restart the party read-in after moving the loadout, and the verb waits
until the roster is rebuilt.** The authored order table is answered in §11.4. The command ids remain `GR-12`
(§11.3).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Movement — CLIENT and SERVICE.**
  - The spawn activation `0023A410` publishes the unit's locomotion position
    (`BattleUnit_PublishLocomotionPosition…`) and calls a 119-byte movement helper.
  - `BattleUnit_CancelAndResetCurrentAction` resets the path (`BattleLocomotion_ResetPathAndSetTargets`) and calls a
    75-byte helper.
  - The action-permission thunk `00313F60` is read by four movement bodies of 114–1,005 bytes.
  - The owner lookup `0031B860` is used by two locomotion bodies.
  - `002ECF10` is called by a 233-byte Movement-filed body.
- **Input — CLIENT.** `InputGameplay_ArbitrateDigitalInputA…` reads the action-permission thunk `00313F60`, so digital
  input arbitration consults the same field permission.
- **Audio — SERVICE through MECHANICAL wrappers.** The level-up path `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`
  (`0030C650`) and `BattleFormula_ApplyTargetResult` both play a sound directly through the resolver and player.
  For the level-up path this is the fanfare that
  [what happens when a character levels up](../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md) §6 stops.
- **CoreRuntimeScheduling — MECHANICAL.** Twelve cited functions reach tables through `ImageAddress_ResolveRuntimePointer`.
- **Presentation — CLIENT (added 2026-09-20 with §11).** §11.3 names `0031FF70`, the wrapper that fills a unit
  display record, because it is the route by which `FUN_00273270` reads the stats record's `+0x5A`. `0031FF70` has a
  Presentation caller, `003C3340`, which builds the record at `[rsp+0x30]` and reads none of it in its own body
  ([the display-record page](../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md), consumer table).
  That is a **client of a shared builder** — fan-in to an accessor this page only passes through, not shared ownership
  of anything on this page.
- **ActorEntity - CLIENT and SERVICE (34 edges).** `0023AC80` is also called by bodies filed to ActorEntity: `0023A570`; `0023A410`, `00273270` reach bodies filed to ActorEntity: `00238BF0`, `0031B760`, `003588B0` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - SERVICE (82 edges).** `00239960`, `0023A410` reach bodies filed to combat formula: `0023AC80`, `00320A40`, `00300520` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (18 edges).** `0023AC80` is also called by bodies filed to Gameplay: `00237DF0` (Combat); `00239960`, `002FEF30` reach bodies filed to Gameplay: `00237DF0` (Combat), `00307D10` (Combat), `00322C50` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (10 edges).** `002ECF10`, `0030FED0` are also called by bodies filed to party: `00313400`, `00313480`, `00328BD0` (BattleStats); `00239960` reaches bodies filed to party: `00329080` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - SERVICE (21 edges).** `00239960`, `0023AC80`, `0030C470` reach bodies filed to rewards/progression: `00300500`, `0030C470`, `002F8F20` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (13 edges).** `002ECF10` is also called by bodies filed to script VM / native bridge: `00343290`, `00344CC0`, `00345CD0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT and SERVICE (56 edges).** `002ECF10` is also called by bodies filed to status/periodic terminal: `00301140`; `0023A410`, `002FDDA0` reach bodies filed to status/periodic terminal: `0030FED0`, `0030E130`, `0030E360` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (17 edges).** `00273270` is also called by bodies filed to UI: `0027AD70`, `0027C3D0`, `0027D740`; `0027AD70` reaches bodies filed to UI: `003EE420` (BattleWindow) - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleUnit_UpdateCombatFrame`, owned by that layer, calls `003105D0` on this page. That caller is the per-unit combat frame step, behind `byte[02089340] & 0x20`: it tests the unit's stats record for bit 4 of the OR-ed `+0x3C`/`+0x64` pair - the **sixth** entry point on that pair - and on the retire path appends `dword[unit+8]` to a **64-entry ring** at `022BE984` whose index at `byte[022BE981]` wraps with `& 0x3F`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
