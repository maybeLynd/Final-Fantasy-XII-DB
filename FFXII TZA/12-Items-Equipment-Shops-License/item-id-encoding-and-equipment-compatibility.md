---
system: Item ID encoding and equipment compatibility
category: 12-Items-Equipment-Shops-License
status: AUDITED — the encoding, the compatibility test and every sibling read: the derived-index trio on the encoded-id-space page (2026-09-11), the three bundle appliers (classes 9, 0xA, 0xD), the four-slot Optimise builder and the starting inventory 2026-09-18
owner_layer: PrimaryOwner:Items_Equipment_Shops_License
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
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
registry_slots:
  - "0x02EBF0F8"
---

# Item ID encoding and equipment compatibility

> Every item in FFXII is a 16-bit number whose top four bits say what *kind* of thing it is —
> and whether two pieces of equipment can be worn together comes down to one byte matching
> another.

~~**PARTIAL.**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`)*. The ID encoding and the compatibility test are read at tier 1. ~~The full category~~
~~enumeration and the comparison/optimise logic are not.~~ The full category enumeration and the comparison / Optimise logic are read too (§7, P-1 and P-4; §3, the `002F9F20` row).

## 1. What the player sees

Some combinations simply refuse. A shield will not go with certain weapons; an off-hand slot
greys out depending on what is in the main hand. The menu does not explain the rule — it just
will not let you.

That rule is not a special case list. It is **one byte on the main-hand item compared against
one byte on the off-hand item**, and if they differ the combination is rejected. Every
weapon/shield restriction in the game is that single comparison.

## 2. Native mechanism

### Item IDs are encoded

```c
ItemDefinition_ClassifyEncodedItemCategory(ushort id)
{
    if (id == 0xFFFF) ...                 // no item
    if (id >> 0xC == 1) ...               // top 4 bits = category
    ...
}
```

A 16-bit item id splits as:

```
bits 15..12   category (top nibble)
bits 11.. 0   index within that category
```

`0xFFFF` is the **"no item" sentinel**, checked before anything else — and it is used
consistently across the equipment functions, not just here.

### Compatibility is one byte against another

```c
bool Equipment_CheckPrimarySecondaryDefinitionCompatibility(ushort primary, ushort secondary)
{
    if (primary == 0xFFFF || secondary == 0xFFFF) ... 

    table  = DAT_02ebf0f8;
    stride = *(ushort *)(table + 8);
    base   = ImageAddress_ResolveRuntimePointer(*(dword *)(table + 0xC));

    secRec = base + (secondary - 0x1000) * stride;
    priRec = base + (primary   - 0x1000) * stride;

    return *(char *)(secRec + 0x11) == *(char *)(priRec + 9);
}
```

Three things this establishes:

**The record index is `id - 0x1000`**, which independently confirms the nibble encoding —
`0x1000` is exactly category 1's base, so these are category-1 definitions indexed by their
low 12 bits.

**The definition table is resolved through image-address indirection**, not a raw pointer:
`table+0xC` holds an RVA and `table+8` the record stride, so the layout is data-driven rather
than compiled in.

**Compatibility is a single byte equality** — the secondary's field at `+0x11` must equal the
primary's field at `+9`. Different offsets on each side, so these are two *different* fields
that happen to be compared: something like "what this item requires of its partner" against
"what this item provides".

That asymmetry is the interesting part. It is not a symmetric "same class" test; each item
carries both a *provides* byte and a *requires* byte, and only one direction is checked here.

## 3. Key addresses

| Address | Name | Verified |
|---|---|---|
| `002FABD0` | `ItemDefinition_ClassifyEncodedItemCategory` | ✅ read whole (2026-09-12, P-1) |
| `002F7EC0` | `Equipment_CheckPrimarySecondaryDefinitionCompatibility` | ✅ read |
| `002F7A10` | `Equipment_SelectPreferredCandidateByAuthoredStats` | ✅ read (P-4, 2026-09-12) |
| `002F7C80` | `Equipment_ComputeComparisonMetricWithCompatiblePartner` | ✅ read (P-4, 2026-09-12) |
| `002F9F20` | `Equipment_BuildRecommendedLoadoutForMappedStats` | **read 2026-09-18 (FABLE).** `(slotIndex, out[5])`: takes the stats block of mapped slot `slotIndex` (`BattleStats_GetByMappedBattleSlot`, kind 3), copies its five equipment words `+0x50`..`+0x58` into `out`, then for each of four slots walks an authored id range from the constant pairs at `00D0F9C0` — slot 0 `0x1000`..`0x10C7`, slot 1 `0x10C8`..**`0x11A3`**, slot 2 `0x10DC`..`0x1117`, slot 3 `0x1118`..`0x1153` — **CORRECTED 2026-09-22 (FABLE): slot 1 was written here as ending at `0x10DB`, the value that makes the four ranges contiguous. It does not. The two 16-byte constants are a `lo[4]` at `00D0F9C0` and a `hi[4]` at `00D0F9D0`, and `hi[1]` is `0x11A4`, so slot 1 spans 220 ids and CONTAINS slots 2 and 3 entirely.** The contiguity was assumed, not read; this sentence's own later clause about ids `0x1184`..`0x11A3` being walked is only possible under the measured bound, so the paragraph contradicted itself. The ranges are coarse search bounds, not slot definitions — the slot filter is the definition record's byte `+0x07` bits 7..5 (`00317A18`), see [the compatibility contract](CONTRACT-equipment-compatibility.md) EQ-3 and EQ-4 — keeping an id only when `Equipment_CheckItemEligibleForSlotByStatsIndex(class byte +4, out, id, slot)` passes and, for slot 1, `Equipment_CheckPrimarySecondaryDefinitionCompatibility(id, out[0])` too, and letting `Equipment_SelectPreferredCandidateByAuthoredStats(out[slot], id, mode, stats)` pick the better of the incumbent and the candidate (`mode` = the slot, or 0 for ids `0x1184`..`0x11A3`, `002FA021`..`002FA033`); after slot 0 an empty hand becomes `0x1000` (Unarmed) and a slot-1 item incompatible with it is dropped to `0xFFFF` (`002FA05A`..`002FA077`). Returns 1 with the loadout in `out`. |
| `0023AF50` | `Inventory_InitializePrimaryStateFromAuthoredTable` | **read 2026-09-18 (FABLE).** After `002370C0()`, it walks the table at registry slot `02EBF048` (count at `+4`, stride word `+8`, rows through `ImageAddress_ResolveRuntimePointer` of `+0xC`) and, for every row, calls `Inventory_MutateEncodedItemPrimaryChannelMode1(word +0, word +2, 0)`: the row is `{u16 item id, u16 count}` and the walk is the starting inventory, applied by `BattleSystem_ResetRuntimeState`. Returns 1. |
| `00252E60` / `002535D0` / `002534C0` | `InventoryDerivedIndex_*` | **read on [the encoded-id-space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.9 (2026-09-11), carried here 2026-09-18 (FABLE):** twelve per-category `u16` present-item lists in the state block `*(020927C0)`, counts at `+0x47B8 + 4 × list`, capacity and base in the twelve-entry table `02092760`; add appends when absent and within capacity (an inconsistent list or a category above 11 hits the `0x200` fast-fail), remove blanks with `0xFFFF` and compacts, compact pulls later entries over every blank and rewrites the count. |
| `002FD530` | `InventoryBundleClass09_ApplyGilAndNestedItems` | **read 2026-09-18 (FABLE).** `(id, count, r8, r9, flags)`: acts only for `r8 == 0` and `r9 == 1` (`002FD53F`..`002FD54C`); the row is registry slot `02EBF070`'s base plus `(id - 0x9000) × stride` (`+8`). It adds `count × row +0` gil (`GameState_GetGil` / `SetGil`, clamped at 0, `002FD5A9`..`002FD5C0`) and, when `flags` bit 0 is set, reports the difference through `00469E80`; then for each of the two nested entries `{u16 id +4, u16 qty +6}` and `{+8, +0xA}` whose id is not `0xFFFF` it calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState(id, qty × count, 0, 1, flags)`. Returns 0. |
| `002FD640` | `InventoryBundleClass0A_ApplyNestedItems` | **read 2026-09-18 (FABLE).** Same guard and row rule over slot `02EBF068` with base `0xA000`; the row is six `u16` ids in two triples, `+0`..`+4` and `+6`..`+0xA`, and `flags` bit 1 selects the second triple (`002FD6BA`); every id of the chosen triple that is not `0xFFFF` is added with quantity `count` (not multiplied) through the same modify call (`002FD6C0`..`002FD757`). Returns 0. |
| `002FD780` | `InventoryBundleClass0D_ApplyNestedItems` | **read 2026-09-18 (FABLE).** Same guard and row rule over slot `02EBF058` (the bazaar goods) with base `0xD000`; the row holds three `{u16 id, u8 qty}` pairs at `+4`/`+6`, `+8`/`+0xA` and `+0xC`/`+0xE`, and each pair with a non-zero quantity is added as `qty × count` through the same modify call (`002FD7F2`..`002FD85D`). Returns 0. |
| `002FD880` | `InventoryEncodedGilClass0E_ApplyGilDelta` | ~~not read~~ read: adds `(id & 0xFFF) × delta` gil, the id is the amount *(answered: see §7, P-5; checked at `002FD880`–`002FD8C5`; 2026-10-02, OPUS)* |
| `02EBF0F8` | equipment definition table header | — |

## 4. Data structures and formulas

```
Item ID                        u16
  bits 15..12   category
  bits 11.. 0   index
  0xFFFF        no item / empty slot sentinel

Equipment definition table     header at DAT_02EBF0F8
  +0x08   u16   record stride
  +0x0C   u32   RVA -> record array   (via ImageAddress_ResolveRuntimePointer)

Equipment definition record
  +0x09   i8    the item's EQUIPMENT CLASS, 0..26 (section 11)
  +0x11   i8    the class the OFF-HAND item must carry: 18 = a shield, 23..26 = the matching ammunition, -1 = nothing (section 11)
```

**Category extraction:**

```
category = id >> 12
index    = id & 0x0FFF
```

**Record address:**

```
record(id) = resolve(table[+0x0C]) + (id - 0x1000) * table[+0x08]
```

**Compatibility:**

```
compatible(primary, secondary)  iff  record(secondary)[0x11] == record(primary)[0x09]
```

Note the offsets differ by side — the test is **asymmetric**, comparing two different fields.

## 5. Call chain

```
equip attempt / loadout build
  -> Equipment_BuildRecommendedLoadoutForMappedStats     (not read)   <- corrected 2026-10-02, OPUS: read 2026-09-18 (section 3)
     -> Equipment_SelectPreferredCandidateByAuthoredStats (not read)   <- corrected 2026-10-02, OPUS: read, P-4, 2026-09-12 (section 3)
        -> Equipment_ComputeComparisonMetricWithCompatiblePartner (not read)   <- corrected 2026-10-02, OPUS: read, P-4, 2026-09-12 (section 3)
           -> Equipment_CheckPrimarySecondaryDefinitionCompatibility   <- THIS
              -> resolve definition records, compare one byte
```

**Upstream:** the equip menu and the auto-optimise path.
**Downstream:** accept or reject the pairing.

**Do not confuse with:** the augment byte on equipment definitions, which feeds the derived
effect layer and is a different field entirely — see the two-layer effect model.

**The same byte, used as a verdict (added 2026-09-19, FABLE; one body read whole).** `003231F0` (345 B) answers "can
this unit attack with what it holds?" for a stats slot, optionally for a weapon / off-hand pair other than the
record's own (`+0x50` / `+0x52`). **No weapon → `0x25`.** A weapon whose runtime category is not 4 → **0, usable**.
Category 4 is the ammunition weapons of section 11: **no off-hand item → `0x26`**; otherwise both equipment rows are
resolved and the answer is 0 only when the weapon's `+0x11` equals the off-hand item's `+0x09`, else `0x26`. A slot
above `0x27` answers 1. *Its three call sites are in two HUD bodies, which were not read; the battle availability
check does not call it, so whether `0x25` / `0x26` continue that check's reason numbering was not established.*
Interior: `003231F9`, `0032322A`, `0032323B`, `0032324B`, `00323250`, `0032325F`, `00323310`, `00323319`, `0032333E`.

## 6. Modding notes

- **`0xFFFF` means empty.** Any item field holding `0xFFFF` is "nothing equipped", not item
  65535.
- **Item IDs carry their category in the top nibble.** A raw ID is not a flat index; the
  definition lookup subtracts the category base (`0x1000` for category 1). *Extension 2026-09-11:*
  the nibble is the row of the fifteen inventory class descriptors at `01EEBCC0`, and the
  encoded-id **class is `nibble + 5`** — read from that table by `FUN_00309440`, so the class
  registry's "correspondence" with this nibble is an identity
  ([the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.1).
- **The equipment table is data-driven** — stride at `+8`, record RVA at `+0xC`. Adding or
  resizing records is a data change, not a code change.
- **One byte governs every weapon/off-hand restriction.** To change what pairs with what, edit
  `+0x09` ~~(primary side)~~ on the off-hand item and `+0x11` ~~(secondary side)~~ on the main-hand weapon *(corrected 2026-10-02, OPUS: the main hand's `+0x11` must equal the off-hand's `+0x09`, checked at `002F7ECF` / `002F7F76` and both call sites `002FA00D`–`002FA013`, `002FA062`–`002FA069`; CONTRACT-equipment-compatibility.md EQ-1)* on the definitions — no code patch needed.
- **The test is asymmetric.** Swapping which item is primary changes which fields are compared,
  so a pairing may validate in one order and not the other. Do not assume symmetry.
- **XIIOnline:** equipment state is authoritative character data. Compatibility is computed
  locally from definition tables, so clients running different item data will disagree about
  legal loadouts — version-fence equipment definitions if that matters.

## 7. What is not known

- [x] ~~The full category enumeration — only category 1 is confirmed via the `0x1000` base.~~
      **P-1 ANSWERED 2026-09-12 (FABLE) — `002FABD0` read whole.** After the `0xFFFF` sentinel the
      function keys on the id's top nibble through a constant table of eight dwords at `00D0F990`
      (`002FAD20`): nibble 0 → **4**, 2 → **7**, 3 → **6**, 4 → **5**, 5 → **8**, 6 → **9**, 7 → **10**
      (the nibble-1 entry, −1, is never read; nibbles 8–15 index past the table into the frame —
      the function is not defined for key items, quickenings or bazaar ids). Nibble 1 (equipment)
      resolves the row (`base + (id − 0x1000) × stride`, `002FAC4A`–`002FAC8F`) and keys on the row's
      **byte `+7` top three bits** through a second table at `00D0F980` (`002FAD1A`): group 0 →
      **0**, groups 2 and 3 → **1**, group 4 → **2**, and group 1 re-reads the row and returns **3**
      when the equipment class `+9` is 23–26 (ammunition) and **1** otherwise (`002FACE1`–`002FAD18`).
      Over all 557 shipped rows the byte-7 group is the **slot group**: 0 = the eighteen weapon
      classes, 1 = shields (18) and ammunition (23–26), 2 = helmets (19), 3 = armor (20), 4 =
      accessories (21) and the special six (22). So the categories are **0 weapons, 1 shields /
      helmets / armor, 2 accessories, 3 ammunition, 4 items, 5 technicks, 6 magicks, 7 loot, 8 / 9 /
      10 the nibble-5 / 6 / 7 classes** (registry classes 10 / 11 / 12, [the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)). The
      consumers agree: `003933D0` returns `category ≤ 3` (is equipment), `002FA920` collects every id
      of a wanted category, and `003933B0` maps a category back to its registry class through the
      12-byte table at `00D113B8` — `6, 6, 6, 6, 5, 9, 8, 7, 10, 11, 12, 18` — which also admits a
      category 11 (bazaar goods, class 18) the classifier never produces.
- [x] ~~What the `+0x09` and `+0x11` bytes *mean* (equip-slot class? handedness?).~~ **P-2
      ANSWERED 2026-09-12 (FABLE):** `+0x09` is the item's equipment class (27 values, §11) and
      `+0x11` the class the item in the other slot must carry — 18 (a shield) on every
      one-handed melee class, the matching ammunition class (23–26) on bows, crossbows, guns and
      hand-bombs, −1 on everything that admits nothing. With §9's orientation, slot 0's weapon
      advertises what slot 1 may hold.
- [x] ~~Whether any caller also checks the reverse direction, given the test's asymmetry.~~
      **P-3 ANSWERED** — the "no caller checks the reverse direction" section below: one caller,
      two sites, slot 0 always the secondary (re-read 2026-09-12, FABLE: `002FA00D`–`002FA013`
      candidate vs slot 0, `002FA062`–`002FA069` slot 1 vs slot 0, the latter after an empty slot 0
      is defaulted to `0x1000` Unarmed and before an incompatible slot 1 is blanked to `0xFFFF`,
      `002FA04C`–`002FA077`). Pairings are order-dependent by construction: the weapon dictates.
- [x] ~~The comparison metric and recommended-loadout logic (`002F7C80`, `002F7A10`,
      `002F9F20`) — the actual "Optimise" behaviour.~~ **P-4 ANSWERED 2026-09-12 (FABLE) — all three
      read whole.**
      **The builder** `Equipment_BuildRecommendedLoadoutForMappedStats(index, out[5])` (callers
      `003FE720` / `003FF360`, the equip menu) takes the mapped stats record (`00320AB0(index, 3)`),
      copies its five equipment words `+0x50`–`+0x58` into `out`, and for **slots 0–3 only** walks
      every id of a per-slot range from the tables at `00D0F9C0` / `00D0F9D0` — slot 0 `0x1000`–`0x10C7`
      (the weapon rows), slot 1 `0x10C8`–`0x11A3` (every non-weapon row), slot 2 `0x10DC`–`0x1117`
      (helmets), slot 3 `0x1118`–`0x1153` (armor) — keeping a candidate that
      `Equipment_CheckItemEligibleForSlotByStatsIndex(type, out, id, slot)` accepts, that for slot 1
      also passes the compatibility test against `out[0]` (`002FA00D`), and that
      `Equipment_SelectPreferredCandidateByAuthoredStats(out[slot], id, slot, stats)` prefers — the
      slot argument being 0 for an ammunition id (`0x1184`–`0x11A3`, `002FA021`–`002FA033`). Afterwards
      an empty slot 0 becomes `0x1000` Unarmed and a slot 1 incompatible with it is blanked
      (`002FA04C`–`002FA077`). **Slot 4 — accessories — is never visited.**
      **The preference** (`002F7A10`): a candidate whose slot group (byte `+7 >> 5`) is 4 keeps the
      current item (`002F7A87`–`002F7A92`, the accessory guard); an empty current takes the candidate.
      Otherwise, **weapons (slot 0)** compare the metric below and keep the current on a strict win;
      on a tie the currently *equipped* weapon `stats +0x50` decides — a candidate that is it wins,
      one of its class `+9` beats one that is not (`002F7BF0`–`002F7C37`) — then row byte `+6`
      equality and finally **the higher id** (`002F7C4D`–`002F7C5A`). **Slots 1–3** compare two row
      bytes lexicographically, larger wins: `+0x18` then `+0x19` for slots 1 and 3, `+0x19` then
      `+0x18` for slot 2 (`002F7B15`–`002F7B76`; ~~what the two bytes are on non-weapon rows this page~~
      ~~has not named~~ *(answered: see equipment-slots-and-the-single-stat-rebuild.md §6.1 — a shield's evade and magick evade; a helmet's, armour's or accessory's defence and magick resist, grouped by `0031E9A0`, checked at `0031E9A0`–`0031E9DF`; 2026-10-02, OPUS)* — on weapon rows `+0x19` is the recipe, §10), ties again by `+6` then the higher id.
      **The metric** (`002F7C80(id, stats)`): 0 for Unarmed or `0xFFFF`; the row's byte **`+0x1A`**
      for an ordinary weapon; for a weapon whose partner class `+0x11` is 23–26 (bow, crossbow, gun,
      hand-bomb) it finds the best eligible ammunition of that class among `0x1184`–`0x11A3` — the
      equipped off-hand `stats +0x52` when it matches, else the preferred candidate — and returns
      **weapon `+0x1A` + ammunition `+0x1A`**, or **−1 when no ammunition is available** (`002F7D1E`–
      `002F7EAB`): a ranged weapon without ammo never wins.
- [x] ~~The inventory bundle classes `09`, `0A`, `0D`, `0E` and what distinguishes them.~~
      **P-5 ANSWERED** — [the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.8 reads all four handlers against the shipped tables
      (closed 2026-09-12, FABLE): `0x9000` **reward packages** (`{gil, itemA, countA, itemB,
      countB}`, gil plus two nested grants), `0xA000` **package selectors** (six ids, two triples,
      the first slot a `0x9000` id in the shipped rows), `0xD000` **bazaar goods** (three granted
      pairs, a price, three loot requirements), `0xE000` **gil as the id** (`id & 0xFFF` × the
      delta). What distinguishes them is what a grant of one id expands into.
- [x] ~~The rest of `ItemDefinition_ClassifyEncodedItemCategory` beyond the category-1 branch.~~ Read 2026-09-12 (P-1 above).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `0xFFFF` is the no-item sentinel | explicit guards in both `002FABD0` and `002F7EC0` | 1 |
| Top nibble is a category | `id >> 0xC` tested as a discriminator in `002FABD0` | 1 |
| Record index is `id - 0x1000` | index arithmetic in `002F7EC0` | 1 |
| Table is data-driven via image-address indirection | stride at `+8`, RVA at `+0xC`, resolved through `ImageAddress_ResolveRuntimePointer` | 1 |
| Compatibility is one byte equality | `*(char *)(secRec + 0x11) == *(char *)(priRec + 9)` — the function's return expression | 1 |
| The test is asymmetric | the two sides read different offsets, `+0x11` vs `+0x09` | 1 |

**Scope honesty.** ~~Only two of this category's functions were read. The "Optimise" behaviour —~~
~~which most players would consider the interesting part — sits in three unread functions and is~~
~~recorded as **P-4** rather than guessed at from their names.~~ *(answered: see §3 and §7 — the three Optimise functions `002F9F20`, `002F7A10` and `002F7C80` are read, P-4 answered 2026-09-12 and the builder 2026-09-18; 2026-10-02, OPUS)*

## 9. Related

- [`../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md) — the equipment augment byte, a different field
- [`../02-Resource-And-Asset-Pipeline/resource-section-addressing.md`](../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) — the same image-address indirection pattern
- [`../13-Rewards-Progression-Economy/experience-and-license-point-award.md`](../13-Rewards-Progression-Economy/experience-and-license-point-award.md) — licence progression, adjacent owner

## 9. Falsification pass 2026-09-02

**Attack chosen.** The striking claim here is the **asymmetry**: compatibility compares
`record(secondary)[0x11]` against `record(primary)[0x09]` — two *different* fields. An asymmetric
equality test is either a real design or a misread of which operand is which, so the killer looked
for was an operand mix-up. §7 also asks whether any caller checks the reverse direction, which makes
the asymmetry testable rather than merely stated.

### SURVIVED: the expression, exactly

`Equipment_CheckPrimarySecondaryDefinitionCompatibility` (`002F7EC0`) re-read in full:

```c
uVar3 = (param_2 - 0x1000) * stride + base;      // record of the SECONDARY
uVar2 = (param_1 - 0x1000) * stride + base;      // record of the PRIMARY
return *(char *)(uVar3 + 0x11) == *(char *)(uVar2 + 9);
```

The operands are as documented: `+0x11` is read from `param_2`'s record, `+0x09` from `param_1`'s.
The `- 0x1000` index and the `+0x08` stride / `+0x0C` RVA table access are also confirmed.

### ANSWERED — §7's open question: no caller checks the reverse direction

`002F7EC0` has exactly **one caller**, `Equipment_BuildRecommendedLoadoutForMappedStats`
(`002F9F20`), which calls it at **two sites**:

```c
Equipment_CheckPrimarySecondaryDefinitionCompatibility(uVar9 & 0xffff, *param_2);   // candidate vs slot 0
Equipment_CheckPrimarySecondaryDefinitionCompatibility(param_2[1],     *param_2);   // slot 1   vs slot 0
```

**Both put `*param_2` — slot 0 — in the `secondary` position.** So across the whole executable,
`+0x11` is *always* read from slot 0's record and `+0x09` *always* from the other item's. The
asymmetry is never exercised in both directions; it is **consistently oriented**.

That makes the two fields readable as a pair of roles rather than an oddity: slot 0 advertises a
value at `+0x11`, and the item being fitted against it must carry the matching value at `+0x09`.
Which of the two is "requirement" and which is "capability" ~~is still not established — **P-2 stays~~
~~open**~~ *(answered: see §7, P-2 ANSWERED 2026-09-12 — `+0x09` is the item's own equipment class and `+0x11` the class the other slot's item must carry; 2026-10-02, OPUS)* — but the direction is now fixed, and a modder editing these bytes needs to know which slot
they are editing for.

### NEW: an empty slot is compatible with everything

The `0xFFFF` guard's *result* was not recorded:

```c
if ((param_1 != 0xffff) && (param_2 != 0xffff)) { ... return false; }
return true;                                   // <- either side empty => COMPATIBLE
```

If either side is the no-item sentinel the function returns **true**. An empty slot never blocks an
equip, which is the behaviour a player expects and the opposite of what a "fail closed" reading of
the sentinel would predict.

### NEW: an empty primary slot is substituted with item `0x1000`

Immediately before the second call site the caller does:

```c
if (*param_2 == 0xffff) { *param_2 = 0x1000; }
iVar5 = Equipment_CheckPrimarySecondaryDefinitionCompatibility(param_2[1], *param_2);
if (iVar5 == 0) { param_2[1] = 0xffff; }
```

So for the slot-1 check, an **empty slot 0 is replaced by item id `0x1000`** — the first id in the
table — rather than being left as `0xFFFF`. "Nothing equipped" is therefore evaluated as a **real
item** here, and if slot 1 is then incompatible it is cleared to `0xFFFF`. A modder changing the
`0x1000` record's `+0x11` byte changes what may be worn in slot 1 **while slot 0 is empty**.

### A tooling correction that reaches beyond this document

The call-graph edge count for `002F9F20 -> 002F7EC0` is **1**, but the body contains **two calls**.
`edges.tsv` stores one row per caller-callee pair — 90,525 rows across 90,525 distinct pairs, no
duplicates — so **an edge count is a count of distinct callers and never of call sites**. This is
now rule 6 in [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md), and it forced the
retraction of a vacuous inference published one pass earlier in
[`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) §9.
## 10. The weapon row's `+0x19` is its damage recipe — 2026-09-11

When an action's own recipe byte is 0 — the plain Attack — `BattleFormula_ResolveTargetResult`
resolves the attacker's weapon word (`stats +0x50`) to its equipment row and takes **byte `+0x19`
as the recipe id** (`003861A7`–`00386201`; a word outside `0x1000` … `0x1000 + count` returns −2).
Across the 308 weapon and shield rows (kind byte `+7` below `0x20`) the byte takes ten values, and
they follow the weapon category `+0x26` almost exactly: 20 for swords, greatswords, spears and rods
(categories 3, 4, 15, 13), 21 daggers and ninja swords (2, 6), 22 katana and staves (5, 7), 23 axes,
hammers and hand-bombs (11, 12, 21), 24 poles (14), 25 bows (17, plus three crossbow-category
rows), 26 crossbows (18), 27 guns and measures (20, 10, plus a few special rods, maces and swords),
29 the Unarmed row alone, 104 maces (8), and 64 on the 58 `NOT USED` rows. What each recipe
computes is [the attack-defence page](../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md)
§5.1. **To move a weapon to another formula, change this byte**; the category byte `+0x26` is what
the weapon-class map and the motion cache read, not the formula.

## 11. The equipment class byte, named row by row — 2026-09-12, FABLE (P-2, CM-3)

`+0x09` is not a handedness flag but the **equipment class** (distinct from the weapon row's `+0x26`, the category §10 says the weapon-class map and the motion cache read), and every row of the shipped table
falls into one of 27 values. The table was histogrammed over all 557 rows of `battle_pack.bin`'s
directory entry `+0x38` (`st2e`, stride 52, rows from `+0x20`) and each class's rows named through
text bank 1 (`+0x02` is `0x800 + row`, [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) §4). `+0x11` takes only four kinds of value,
and they line up with the classes exactly as the compatibility test (§2) needs them to: the
one-handed melee classes say **18** (the shield class), the four ammunition weapons say the class
of their ammunition, and everything else says **−1**. Read with §9's orientation — slot 0's `+0x11`
against the fitted item's `+0x09` — a sword in slot 0 admits a shield, a bow admits arrows, a
greatsword admits nothing; the shields, helmets, armor, accessories and ammunition, which are
never slot 0 of a weapon pair, all carry −1.

| `+0x09` | rows (named) | what they are (bank 1 names) | `+0x11` | runtime category (`0031E9F0`) |
|---:|---:|---|---:|---:|
| 0 | 68 (1) | Unarmed, then the `Reserve` / `NOT USED` rows | 18 / −1 | 1 |
| 1 | 49 | swords — Broadsword, Longsword, Iron Sword … | 18 | 2 |
| 2 | 26 | greatswords — Claymore, Defender, Save the Queen … | −1 | 3 |
| 3 | 10 | katana — Kotetsu, Osafune … Masamune | −1 | 3 |
| 4 | 8 | ninja swords — Ashura, Sakura-saezuri, Kagenui, Koga Blade, Iga Blade, Orochi, Yagyu Darkblade, Mesa | −1 | 3 |
| 5 | 18 | spears — Javelin, Spear, Partisan … | −1 | 3 |
| 6 | 14 | poles — Oaken Pole, Cypress Pole, Battle Bamboo … | −1 | 3 |
| 7 | 16 | bows — Shortbow, Silver Bow, Aevis Killer … Dhanusha | 23 | 4 |
| 8 | 11 | crossbows — Bowgun, Crossbow, Paramina Crossbow … | 24 | 4 |
| 9 | 16 | guns — Altair, Capella, Vega … | 25 | 4 |
| 10 | 7 | axes — Handaxe, Broadaxe, Slasher … Golden Axe | 18 | 2 |
| 11 | 6 | hammers — Iron Hammer, War Hammer, Sledgehammer … Vrscika | 18 | 2 |
| 12 | 13 | daggers — Dagger, Mage Masher, Assassin's Dagger … | 18 | 2 |
| 13 | 8 | rods — Rod, Serpent Rod, Healing Rod … Rod of Faith | −1 | 3 |
| 14 | 11 | staves — Oak Staff, Cherry Staff, Wizard's Staff … | −1 | 3 |
| 15 | 15 | maces — Mace, Bronze Mace, Bhuj … | 18 | 2 |
| 16 | 6 | measures — Gilt Measure, Arc Scale, Multiscale … Euclid's Sextant | 18 | 2 |
| 17 | 6 | hand-bombs — Hornito, Fumarole, Tumulus … Makara | 26 | 4 |
| 18 | 33 | shields — Gendarme, Leather Shield, Buckler … | −1 | 6 |
| 19 | 60 | helmets — Leather Cap, Headgear, Headguard … Grand Helm | −1 | 7 |
| 20 | 73 (60) | armor — Leather Clothing, Chromed Leathers, Leather Breastplate … Grand Armor | −1 | 8 |
| 21 | 42 | accessories — Opal Ring, Ruby Ring, Tourmaline Ring … Quasimodo Boots | −1 | 9 |
| 22 | 6 | the special six — Manufacted Nethicite, Cat-ear Hood, Fuzzy Miter, Ribbon, Goddess's Magicite, Dawn Shard | −1 | 9 |
| 23 | 8 | arrows — Onion Arrows, Parallel Arrows, Fiery Arrows … Artemis Arrows | −1 | 5 |
| 24 | 10 (8) | bolts — Onion Bolts, Long Bolts, Stone Bolts … Grand Bolts | −1 | 5 |
| 25 | 9 (8) | shot — Onion Shot, Silent Shot, Aqua Shot … Stone Shot | −1 | 5 |
| 26 | 8 | bombs — Onion Bombs, Poison Bombs, Stun Bombs … Castellanos | −1 | 5 |

The last column is `BattleDefinition_MapByte9ToRuntimeCategory` (`0031E9F0`), which folds the
27 classes into nine runtime categories through a 27-byte index table at `0031EA74` and a
nine-arm jump table at `0031EA50` — the categories [the world-loot page](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) §"The three presentation
tiers" grades the loot shine by and [the auto-status rebuild](../08-Combat-Formula/the-auto-status-rebuild.md) tests for the equipment auto-statuses:
**1** unarmed / reserve, **2** shield-taking melee, **3** two-handed and mage weapons, **4**
ammunition weapons, **5** ammunition, **6** shields, **7** helmets, **8** armor, **9** accessories
and the special six (Manufacted Nethicite, Cat-ear Hood, Fuzzy Miter, Ribbon, Goddess's Magicite,
Dawn Shard, class 22). The reserve rows of class 0 mostly carry 18 like Unarmed does; two guns'
`NOT USED` rows carry −1.

| claim | evidence | tier |
|---|---|---|
| 27 classes, their names and their `+0x11` values | every row's `+0x09` / `+0x11` / `+0x02` read from the `us` `battle_pack.bin`; bank 1 decoded with the battle charset; the row 0 / 1 / 18 / 200 / 220 / 280 / 340 / 388 boundaries are where the names change kind | 1 |
| The nine runtime categories | `0031E9F0`–`0031EA4C`, the index bytes at `0031EA74` (`0,1,2,2,2,2,2,3,3,3,1,1,1,2,2,1,1,3,4,5,6,7,7,8,8,8,8`) and the nine jump-table arms | 1 |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Gameplay — CLIENT.**
  - `Inventory_InitializePrimaryStateFromAuthoredTable` (`0023AF50`) is called by `BattleSystem_ResetRuntimeState`.
  - `BattleDefinition_MapByte9ToRuntimeCategory` (`0031E9F0`) is also used by `BattleDefinition_GetRuntimeCategoryB…`.
  - `BattleStats_GetByMappedBattleSlot` (`00320AB0`) resolves through `BattleSlotMap_ResolveMappedBattleSlot`.
- **Party — CLIENT.** A 639-byte Party-filed body uses `BattleStats_GetByMappedBattleSlot`.
- **Audio — MECHANICAL.** The 1,458-byte UI body `003FF360` plays a cue through the gated request wrapper.
- **Rewards_Progression_Economy - SERVICE (8 edges).** `002FD530`, `002FD880` reach bodies filed to rewards/progression: `00253690`, `00254EE0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (9 edges).** `00320AB0` is also called by bodies filed to script VM / native bridge: `0050FD00`, `0050FD50`, `0050FDD0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (1 edge).** `00320AB0` is also called by bodies filed to status/periodic terminal: `00310DB0` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE.** A cited function calls `BattleStats_GetByMappedBattleSlot`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `Battle_BuildActionTargetSet`, owned by that layer, calls `00320AB0` on this page. That caller is the target-set assembly: it resolves the acting unit through the focus handle and then works from the table at `[02EBF138]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — MECHANICAL.** The item-lookup helper `0032A8A0`, cited by this page's `00400CF0`, is also called by the Input-layer body `00253C70` — a shared leaf, not an Input service this page invokes. The page owns the item-record encoding; what Input asks of the same leaf is not claimed.

**UI — CLIENT.** `003231F0`, the usability verdict of section 5, is called from the UI layer's action-list pass (two sites) to decide how an attack entry is shown. The crossing is that call; this page owns the rule, the HUD owns what it draws.

**Presentation — CLIENT (SWE2-EC7 batch-149, 1 edge).** `002B3050`, the produce step the `003FCEE0` stock scan cites, is also called by the Presentation-filed `00506700` - a shared leaf consulted by the render side, not a presentation responsibility of this page.

**CoreRuntimeScheduling and Save/Load — CLIENT (shared-callee edges, SWE2-EC7 batch-161).** The `003FDA20` bracketed-reload entry names `00244DD0`/`002470D0`; `00244DD0` fans into core-runtime helpers `00229DF0`/`00229E70`/`00229EA0` and is also invoked from the save/load layer (`00583040`), while `0032A8A0` sits between `00583D60` and `002EF2B0`. Shared-helper exchange along the ticket lifecycle; the item page owns no scheduling or save state. Edge list from `edges.tsv`.

## The `002F9F20` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002F9F20` (`Equipment_BuildRecommendedLoadoutForMappedStats`~~, ~212 B~~, 435 B *(corrected 2026-10-02, OPUS: its `ret` is at `002FA0D2`; 212 B is `002F7EC0`'s size; CONTRACT-equipment-compatibility.md §2)*) —
stack-cookie frame (`01F44830`), seeds `xmm0` with the `00D0F9C0`
`0x1000`/`0x10C8` constant pair (`002F9F28`/`002F9F37`).

| member | role | interior |
| --- | --- | --- |
| `002F7EC0` | `0xFFFF` keyed compare — `movzx` `cx`/`dx`, `cx == 0xFFFF` guard (`002F7ECA`/`002F7ED5`) | [`002F7ECA`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-33 update (2026-09-19) - `003FF360`

`003FF360` (**1,458 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,487 B, a wrong literal in the batch-33 append — the body is 1,458 B per the function list*) is the item-record lookup the HUD shares - `002CD3C0`/`00400CF0`/`002D45C0`/`002445C0`/`003C8060`/`0039BA00`/`00282EA0`. Interior anchor `003FF687` (a `002CD3C0` call).

## SWE2-EC7-34 update (2026-09-19) - `003FE720`

`003FE720` (934 B) is an item-id command handler - `ecx-0x401` switch `{0x401, 0x402, 0x404}` with a `edx==-1` veto, `003FEAD0`/`003FEAB1`/`0030A4E0`/`00282EA0`/`002F9F20`. Interior anchor `003FE7E8` (an `003FEAD0` call).

## SWE2-EC7-53 update (2026-09-19) - `00400CF0`

`00400CF0` (396 B) is an item-record lookup helper the HUD's `003FF360` shares - `0032A8A0`/`003C8060`/`003DFBE0`/`003DFCC0`. Interior anchor `00400D1D` (a `003DFCC0` call).


## SWE2-EC7-70 update (2026-09-19) - `003FEAD0` nine-row config copy measured

`003FEAD0` (741 B) is the config-block copy `003FE720`'s command handler
runs: under a stack cookie it resolves `[0209AC30]+0x138` (absent -> return
0), reads `[+0xDE0]` through `00282EA0`, fills the `rsp+0x30` source block
via `0030A4E0` (a second call writes into `rbx` when given), then loops the
nine `0x2C`-strided source rows into the child's `+0xC8`..`+0xE8` dword
window plus `+0xDE2`/`+0xDE4`, and writes four difference-clamped words
into `[+0x130]->+0xC0`'s `+0xF0`..`+0xF6` when that chain exists. Returns
`dword[rsp+0x80] != 0`.
Interior anchor `003FEBAB` (the first `[rcx+r9+0xC8]` store).

## SWE2-EC7-95 update (2026-09-20) - `00317B20` measured

`00317B20` (70 B) is the `0x1C8`-stride sibling of `00317B70`
that `002F7C80` and `002F9F20` call: `cl <= 0x27` indexes the
same ~~`02EBF183`-rooted~~ table, rooted at `[02EBF190] + 8` with stride `0x1C8` *(corrected 2026-10-02, OPUS: checked at `00317B36`–`00317B41` `mov rax, [02EBF190]` / `add rax, 8`; `02EBF183` is not even pointer-aligned)*, but the stack out-slot is fixed at
1 and `00317930` gets `r9d = r8w`, `r8d = r10d` - the flag-set
variant of the record fetch.
Interior anchor `00317B55` (the `00317930` call).

## SWE2-EC7-100 update (2026-09-20) - `002C2CD0` measured

`002C2CD0` (168 B) is the cursor-indexed resolve
`002C2C50` and `003FF360` call on the `0209AC30` `+0x140`
object: `dword[+0x168]` bit 0 clear tails `003FEAD0` with
`ecx = 0`; otherwise `(word[+0xF2] + word[+0xF4]) *
byte[+0xEC] + byte[+0xEE] + byte[+0xED]` indexes the
`+0xC8` table's `0x20`-stride entries (`r8d` forced to
`-1` when bit 2 is set) and `003FE720` runs on the entry's
first dword; a bit-2 `+0x168` afterwards tails
`002C9EB0(rbx, 0x8000, 0)` - the scroll-cursor row fetch
with the two conditional tails.
Interior anchor `002C2D4C` (the `0x20`-stride indexed
load).

`003FF040` (281 B) is the slot dispatch the equip menu `003FF360` runs: `word[rcx+0x18A]` saves and zeroes, `00252610` runs twice (`8, 0x48, 5` then `8, 0x20, 0x20`); `dword[+0x178] == 0x400` fast-paths - `byte[[+0x170] + 0xFC] = 2` and `003FDA20(idx, saved)` - else `word[0209AC30 + idx x 0x20 + 0xD48]` is read, `0xFFFF`/`0x1000` return 1, other values run `003FFA20(idx, 0xFFFF)` then `003FF920(idx, (sword[+0xF2] + sword[+0xF4]) x byte[+0xEC] + sbyte[+0xEE] + sbyte[+0xED])` before `byte[[+0x170] + 0xFC] = 0x19` - the confirm path that weights the roster slot and marks the widget.

Interior anchor `003FF0FC` (function `003FF040`).

`003FF040` (281 B) is the slot dispatch the equip menu `003FF360` runs: `word[rcx+0x18A]` saves and zeroes, `00252610` runs twice (`8, 0x48, 5` then `8, 0x20, 0x20`); `dword[+0x178] == 0x400` fast-paths - `byte[[+0x170] + 0xFC] = 2` and `003FDA20(idx, saved)` - else `word[0209AC30 + idx x 0x20 + 0xD48]` is read, `0xFFFF`/`0x1000` return 1, other values run `003FFA20(idx, 0xFFFF)` then `003FF920(idx, (sword[+0xF2] + sword[+0xF4]) x byte[+0xEC] + sbyte[+0xEE] + sbyte[+0xED])` before `byte[[+0x170] + 0xFC] = 0x19` - the confirm path that weights the roster slot and marks the widget.

Interior anchor `003FF0FC` (function `003FF040`).

`003FF920` (116 B) is the roster-slot weight `003FF040`'s confirm path calls: `word[0209AC30 + idx x 0x20 + 0xD48]` supplies the slot tag and a `0xFFFF` there runs `00292F60(idx)` for the fallback value first; `00293110` consumes `(slot << 16) | weight`, and a live `[0209AC30 + 0x108]` object gets its `[+0x180]` refreshed through `002CA490` - the equip-confirm helper that prices the slot and keeps the paired object current.

Interior anchor `003FF95A` (function `003FF920`).

`00252F40` (40 B) is the `02092760` category-table accessor the derived-index family calls: `ecx > 0xB` resets through `0016D6A0(0x200)` and falls back to slot 0, else returns `02092760 + ecx*8` - the `{base, capacity}` pair of the twelve per-category present-item lists.

Interior anchor `00252F58` (function `00252F40`).

`002CA490` (226 B) is the board-mode to license-id map: `byte[0209AC30 + 0xDE2]` selects 0..0x10 through the `002CA4CB` jump table - mode 0 runs `00291D70(arg)`, modes 1..0x10 yield fixed license ids `0xC9D/0xCB0/0xC9F/0xCA0/0xCB7/0xCB2/0xCB3/0xCB4/0xCB5/0xCF9/0xCFA` (a few cases share ids); when the mode changed since `+0xDE3` and the id is nonzero `002F9860(id)` resolves its string record, `00291D70(1)` and `00291D80(rbx)` finish either way, and `+0xDE3` latches the mode - the license-grid cell resolver.

Interior anchor `002CA4CB` (function `002CA490`).

`003FCEE0` (251 B) is the multi-kind stock scan `003FF360` runs: over the packed kind table `{1,1,3,2}` (`00D120C0`/`00D120D0`) it counts `00252FA0(kind)`, resolves the `00252F40(kind)` record's `+4` through `0020E600`, then walks that u16 list calling `00292B70` per entry and `002B3050` on each match, returning the largest produced value

Interior anchor `003FCF7B` (function `003FCEE0`).

`003FDA20` (174 B) is the bracketed reload `003FF040` runs around the item-table update: `00244F50(0x188, sub-003FDFE0, args)` registers an op ticket stored at `[0209AC30+0x150]` and fed to `00246AD0` on `0208EA28`, an optional `00244DD0` fires on `[rax+0x108]`, the payload runs `003FEDC0(ecx)` then `002CBA30`/`002C1D30`, and `002470D0` releases the ticket before the stack-cookie check

Interior anchor `003FDA99` (function `003FDA20`).

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-item-id-encoding-and-equipment-compatib-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `003DFDD0` | 104 B | `003DFBE0` + 0x2F | zeroes the two qwords at `r8`; when `ecx - 1` is above 7 (unsigned) it goes straight to the return, otherwise it dispatches on `ecx` through an indexed table: 1 and 2 reach a call (`003DFDD0` + 0x35) whose result is stored to qword `r8` and, when non-null, plus 0x10 to qword `r8+8`; 3, 5, 6 and 8 reach a call (`003DFDD0` + 0x4C) whose result is stored to qword `r8`; 4 and 7 go straight to the return; every path returns 1 when qword `r8` (the incoming `r8`, kept in `rbx`) is non-null and 0 otherwise | Interior anchor `003DFDDF`; Interior anchor `003DFDEC`; Interior anchor `003DFE05`; Interior anchor `003DFE1C`; Interior anchor `003DFE2C` |
| `003FE3A0` | 69 B | `003FF360` + 0x4F2 | makes the calls at `003FE3A0` + 0x6 (`ecx` = 0), `003FE3A0` + 0xB and `003FE3A0` + 0x12 (`ecx` = 0); when qword `+0x130` of qword `0209AC30` is non-null it calls `003FE3A0` + 0x33 with that object's qword `+0xC0` and `edx` = 0; it then tail-jumps (`003FE3A0` + 0x40) with `ecx` = `edx` = 0 | Interior anchor `003FE3A6`; Interior anchor `003FE3B2`; Interior anchor `003FE3C8`; Interior anchor `003FE3D3`; Interior anchor `003FE3E0` |
| `003FE6E0` | 53 B | `003FF360` + 0x3A6 | makes the call at `003FE6E0` + 0x6 with `ecx` = 0; then, when qword `+0x130` of qword `0209AC30` is non-null, tail-jumps (`003FE6E0` + 0x2B) with that object's qword `+0xC0` and `edx` = 0, otherwise returns | Interior anchor `003FE6E6`; Interior anchor `003FE6F2`; Interior anchor `003FE6FC`; Interior anchor `003FE70B` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-item-id-encoding-and-equipment-compatib-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `00264CA0` | 56 B | `003DFDD0` + 0x4C | when `ecx` is 6 or 9, tail-jumps to `00264CA0` + 0x33 with `ecx` and `edx` unchanged; otherwise calls `00264CA0` + 0x11 with `ecx` and `edx`, returns 0 when its result is negative (signed), and else tail-jumps to `00264CA0` + 0x23 with (that result, the incoming `edx`) | Interior anchor `00264CA7`; Interior anchor `00264CAC`; Interior anchor `00264CB8`; Interior anchor `00264CC3`; Interior anchor `00264CD3` |
