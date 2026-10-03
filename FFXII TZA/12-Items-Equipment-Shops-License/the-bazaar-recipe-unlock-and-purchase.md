---
system: The bazaar — the 128-row goods table, the loot-sold tally that unlocks a good, the flag byte that shows it, and the purchase that consumes the recipe
category: 12-Items-Equipment-Shops-License
status: AUDITED — the last open box, +0x22 = 120 (UQ-130, the good's icon frame), answered 2026-09-17
owner_layer: both
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0056E140, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "the us battle_pack.bin bazaar table (directory +0xE8, 128 rows x 36 B) decoded in full: every name, granted item, price, flag and required-loot reference resolved through the class tables, 2026-09-11"
last_reviewed: 2026-09-11
registry_slots:
  - "0x02EBF058"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-bazaar-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The bazaar — the 128-row goods table, the loot-sold tally that unlocks a good, the flag byte that shows it, and the purchase that consumes the recipe

> **Selling loot counts it; a bazaar good appears when its three counts are met; buying it takes the
> counts back to zero.** The whole mechanism is one 36-byte row per good, one byte of flags per
> good in the battle state block, one byte of "sold" tally per loot id in the inventory's second
> loot region, and three functions — the sale commit that adds to the tally and refreshes the
> flags, the refresh that compares tallies against the row, and the purchase reset that clears the
> flag and the tallies. *Antidote Set* is 100 gil and two Drab Wool sold; *Morbid Urn* is 250,000
> gil and one each of Horakhty's Flame, Phobos Glaze and Deimos Clay, for a Canopic Jar.

**Corpus validation, before anything else.**

| | |
|---|---|
| file examined | `ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin`, directory entry `+0xE8` → `st2e` section at file offset `0x25370`: **128 rows × 36 bytes** |
| resolved | all 128 names (bank 9 of [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)), every granted item and every required loot through the class tables of [the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.5 |
| positive controls | row 0 *Antidote Set* → Antidote × 3 for 100 gil after Drab Wool × 2; row 2 *Gilt Shield* → Buckler for 250 gil after Molting × 3 and Fire Stone × 3; row 127 *Morbid Urn* → Canopic Jar for 250,000 gil after Horakhty's Flame, Phobos Glaze, Deimos Clay — the recipes the game presents |
| censuses | 81 rows want three loots, 9 two, 31 one, 7 none (the seven *Forgotten Grimoire* rows); prices **70 … 600,000** (~~100 … 250,000~~ — corrected 2026-09-13, §9; 100 distinct values); `+0x14` is 0 on 106 rows, 1 on 15, 2 on the seven Grimoires; `+0x22` is 120 on every row |

---

## 1. What the player sees

The bazaar tab of any shop lists goods that have "appeared". A good appears once the party has
sold enough of the loot it asks for — not owned, *sold* — and it costs gil like any other purchase.
Buying it delivers a package of one to three items and, for most goods, makes it vanish until the
loot has been sold again; a handful of goods (the consumable packs, the Flasks, the Magick
Shards …) come back every time, and the seven Grimoires behave differently again.

## 2. Native mechanism

### 2.1 The row — 36 bytes, class 18 of the encoded-id space (`0xD000` + row)

| offset | size | field | read by |
|---|---|---|---|
| `+0x00` | u16 | name reference, bank 9 (`bank : index` word) | the query record's class-18 arm (`0031DA1B`) |
| `+0x02` | u16 | description string id (`0x55F0` + row, the `22000 + n` pool) | the same arm, `+0x10 ← 002F9860(word)` |
| `+0x04` / `+0x06` | u16 / u8 | granted item 1 and its count | `InventoryBundleClass0D_ApplyNestedItems` (`002FD7F2`–`002FD815`) |
| `+0x08` / `+0x0A` | u16 / u8 | granted item 2 and count | `002FD81A`–`002FD839` |
| `+0x0C` / `+0x0E` | u16 / u8 | granted item 3 and count | `002FD83E`–`002FD85D` |
| `+0x10` | u32 | **price in gil** | the shop driver's purchase (`Shop_CommitPurchaseItemAndGil` receives it as the gil delta) |
| `+0x14` | u16 | **flags**: bit 0 = *repeatable* (the ever-unlocked flag is not consulted, `0030B33F`); bit 1 = **availability is script-settable** — `BattleIdClassD_SetRuntimeFlagBit1IfSupported` (`0030B570`) writes the good's flag bit 1 from a boolean only when this bit is set (`0030B5F6`–`0030B619`), reached through `0032AB50(good, bool)` from `0034C2C0` / `0034C710`; the seven Grimoires, which have no recipe, are the rows that carry it | `BattleIdClassD_RefreshPrerequisiteRuntimeFlags`; `0030B570` |
| `+0x16` / `+0x18` | u16 / u8 | required loot 1 and the **sold count** it needs | the refresh (`0030B375`–`0030B3DA`); the purchase reset (`0030B20C`) |
| `+0x1A` / `+0x1C` | u16 / u8 | required loot 2 and count | `0030B3E0`–`0030B44C`; `0030B225` |
| `+0x1E` / `+0x20` | u16 / u8 | required loot 3 and count | `0030B44E`–`0030B45F`; `0030B240` |
| `+0x22` | u16 | 120 on every shipped row; ~~no reader found~~ the good's icon frame, read by `0057AC10`, `0057B1A0`, `003F41C0` and `0057DC30` *(answered: see §7, UQ-130 ANSWERED 2026-09-17; 2026-10-02, OPUS)* | — |

An unused granted slot has count 0 (the id word is then 0, *Potion*, and is skipped by the count
test at `002FD7FA`); an unused requirement likewise ships as id 0 with count 0 (§2.4 step 4).

### 2.2 The two runtime bytes

**The good's flag byte** — `state + 0x59C8 + row` in the battle state block ([the state map](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md),
save payload `+0x53E54`): bit 0 = **unlocked at least once**, bit 1 = **available now**, bit 2 = **the shop UI's own
marker** — set and cleared by `BattleIdClassD_SetRuntimeFlagBit2` (`0030B630`) from the shop driver
`0056D370` and `0057B6F0`, read by `BattleIdClassD_GetRuntimeFlagBit2` (`0030B4B0`) from `0056E410`,
`0057B6F0` and `0057DC30`; bit 1 is read for the listing by `BattleIdClassD_GetRuntimeFlagBit1`
(`0030B510`) from `002FA920`. A whole-image displacement census of `+0x59C8` finds exactly these,
the refresh, the reset, the rebaser and the query arm (fourteen sites; re-counted 2026-09-22 SWE2-CONTRACT). The query record's class-18 arm copies
bits 0–2 into record `+0x44` (`0031DA69`–`0031DA9D`), which is what the bazaar list draws from.
The rebaser `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` masks all 128 bytes
with `0xF8` (`0030B739`–`0030B75B`), having first zeroed the 512 loot-sold tally bytes at `+0x57C8` (`0030B702`–`0030B737`) *(corrected 2026-10-02, OPUS: checked at `0030B702`–`0030B737`; CONTRACT-bazaar-unlock-and-purchase.md §14 states it)*, when the block is bound (`00233C10`) and after a save image is
rebound (`SaveRuntime_RebindImageBackedGameplayState`, `00238A80`) — see §7.

**The loot's sold tally** — one byte per loot id in the loot class's **region B** at `state +
0x57C8` ([the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.7): channel 3 of the packed-count handlers,
capped at 99. Only two callers in the image use channel 3: the sale commit (adds the quantity
sold) and the purchase reset (writes 0).

### 2.3 Sell — `Shop_CommitSaleItemAndGil` (`00310870`)

`(item, quantity, gilDelta, flags)`: channel 1 `−quantity` through the modify entry (`003108A6`),
gil `+= gilDelta` clamped at 0 with the "You obtain {n} gil" line when `flags & 1` (`003108AB`–`003108CC`),
then **channel 3 `+quantity`** (`003108D1`–`003108E8`) — for a loot id that is the sold tally; for
any other class, channel 3 has no region and the call is a no-op — and finally
**`BattleIdClassD_RefreshPrerequisiteRuntimeFlags`** (`003108ED`), its only caller.

### 2.4 Refresh — `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` (`0030B270`)

For every row `i` of the table (count from the descriptor `+4`, `0030B285`):

1. if the row is not repeatable (`+0x14` bit 0 clear) and flag bit 0 is set — already unlocked
   once — skip (`0030B33F`–`0030B34C`);
2. if flag bit 1 is set — already available — skip (`0030B352`);
3. if all three required counts are 0 — no recipe — skip (`0030B35F`–`0030B36F`);
4. for each of the three requirements the loot's **channel-3 value must be ≥ the row's count**
   (`0030B3CC`–`0030B3DA`, `0030B43E`–`0030B44C`, `0030B454`–`0030B45F`). An id of `0xFFFF` or
   above the `0xE000` class yields −1 and blocks the row (`0030B380`, `0030B393`); an unused slot
   ships as id 0 with count 0, and item 0's channel 3 (no region) is 0, so `0 ≥ 0` passes;
5. all met → `flag |= 3` (`0030B461`): unlocked once, available now.

### 2.5 Buy — `Shop_CommitPurchaseItemAndGil` (`002FEEB0`) and the reset (`0030B180`)

`(item, quantity, price, flags)`: channel 1 `+quantity` (`002FEEDB`) — for a bazaar id this is
`InventoryBundleClass0D_ApplyNestedItems`, which hands out the row's three granted pairs through
the modify entry — gil `−= price` clamped at 0 (`002FEEE0`–`002FEEF3`), the gil line when
`flags & 1`, then **`BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState(item)`**
(`002FEF0A`): it validates the id as class 18 (`0030B194`–`0030B19F`; any other purchase returns
here), clears **flag bit 1** (`0030B203`, bit 0 stays — the good has been unlocked once), and writes
**0 to the sold tally of each of the three required loots** (`003008A0(loot, 0, absolute = 1,
channel = 3, 0)`, `0030B20C`–`0030B256`). A non-repeatable good therefore cannot reappear, and a
repeatable one needs the loot sold again from zero.

Both commits are called only by the shop transaction driver `0056D370` (1,274 B), which the call
graph reaches through no static caller — the shop UI.

### 2.6 What the query record shows the menu

`0031C5D0`'s class-18 arm (`0031D8F1`–`0031DAA0`) fills, for a bazaar id: the name (`+0x18`), the
description (`+0x10`), `+0x28 ← price`, `+0x2C ← +0x22`, the three granted pairs as words at
`+0x38` … `+0x42`, and **the flag byte's bits 0–2 at `+0x44`** — the record mirror of bit 2; the
flag itself is read through `0030B4B0` by `0056E410`, `0057B6F0` and `0057DC30` (§2.2).

## 3. Key addresses

| Address | Role |
|---|---|
| `02EBF058` | the bazaar table descriptor (class 18) |
| `00310870` | `Shop_CommitSaleItemAndGil` — adds to the sold tally, then refreshes |
| `0030B270` | `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` — the recipe check |
| `002FEEB0` | `Shop_CommitPurchaseItemAndGil` — grants, charges, then resets |
| `0030B180` | `BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState` — clears bit 1 and the tallies |
| `002FD780` | `InventoryBundleClass0D_ApplyNestedItems` — the row's granted pairs |
| `003008A0` | `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` — the channel-1 and channel-3 entry |
| `0030B6A0` | the rebaser that masks the flag bytes with `0xF8` |
| `0056D370` | the shop transaction driver, sole caller of both commits |
| `0030B570` | `BattleIdClassD_SetRuntimeFlagBit1IfSupported` — script availability for rows with `+0x14` bit 1 |
| `0030B630` / `0030B4B0` | `BattleIdClassD_SetRuntimeFlagBit2` / `…GetRuntimeFlagBit2` — the shop UI's marker |
| `0030B510` | `BattleIdClassD_GetRuntimeFlagBit1` — the listing's availability read |

## 4. Data structures and formulas

```
BazaarGoodRow (36 B, 02EBF058, id 0xD000 + row)
  +0x00 u16 nameRef      +0x02 u16 descStringId (0x55F0 + row)
  +0x04 u16 giveA  +0x06 u8 giveACount   +0x08 u16 giveB  +0x0A u8 giveBCount   +0x0C u16 giveC  +0x0E u8 giveCCount
  +0x10 u32 priceGil     +0x14 u16 flags (bit 0 repeatable; bit 1 Grimoires)
  +0x16 u16 needA  +0x18 u8 needASold    +0x1A u16 needB  +0x1C u8 needBSold    +0x1E u16 needC  +0x20 u8 needCSold
  +0x22 u16 = 120

state + 0x59C8 + row  u8 flags:  bit 0 unlockedOnce, bit 1 availableNow, bit 2 newEntryMarker (0030B4B0/0030B630, mirrored to menu record +0x44)
state + 0x57C8 + lootIndex  u8 soldTally (0..99)   -- loot class region B, channel 3

sell(loot, n):   tally[loot] += n ; refresh()
refresh():       for each row: if (repeatable or !unlockedOnce) and !availableNow and hasRecipe
                                 and tally[needX] >= needXSold for all X:  flags |= 3
buy(good):       grant the three pairs ; gil -= price ; availableNow = 0 ; tally[needX] = 0
```

## 5. Call chain

```
shop UI (0056D370)
  -> Shop_CommitSaleItemAndGil(item, n, gil, flags)   <- corrected 2026-10-02, OPUS: (id, qty, total, 0) - the fourth argument is a literal 0 (0056D457 xor r9d, r9d), so no gil line
       -> 003008A0(item, -n, 0, 1, flags) ; GameState_SetGil ; 003008A0(item, +n, 0, 3, 0) ; 0030B270
  -> Shop_CommitPurchaseItemAndGil(good, 1, price, flags)   <- corrected 2026-10-02, OPUS: (good, qty, total, 0) - qty is the panel's word +0xDC, total = (price & 0x7FFFFFFF) x qty, the fourth argument 0 (0056D457-0056D49A); section 7, UQ-131
       -> 003008A0(good, 1, 0, 1, flags) -> InventoryBundleClass0D_ApplyNestedItems -> 003008A0(item, count, 0, 1, flags) x3
       -> GameState_SetGil ; 0030B180(good) -> flags[row] &= ~2 ; 003008A0(loot, 0, 1, 3, 0) x3
menu: 0035D3x0 / 0031C5D0(class 18, row) -> record +0x44 = flags[row] & 7
```

## 6. Modding notes

- **A recipe is three `(loot, count)` pairs and a price** — all in the row. Changing what a good
  asks for or costs is a table edit; nothing in code knows a specific good.
- **Sold, not owned.** The tally is written only by the sale commit; granting loot by any other
  path (chests, drops, scripts) never unlocks a good.
- **Repeatability is `+0x14` bit 0.** Clearing it on a repeatable good makes it one-time; setting it
  on a one-time good makes it recur after each purchase and re-sale.
- **The tally caps at 99** (the packed-count channel-3 clamp); a requirement above 99 can never be
  met.
- **The flag bytes are masked on every rebind** (§7): a mod that wants a good to stay consumed must
  make sure the loaded image's bytes are the ones that survive.

## 7. What is not known

- [x] ~~**Whether one-time goods survive a save and reload.** The rebaser clears bits 0–2 of all 128
      flag bytes on the bind path and on `SaveRuntime_RebindImageBackedGameplayState`; if that runs
      after the image's bytes are in place, every good is "never unlocked" again after a load and a
      one-time good returns as soon as its loot is sold again. Static reading cannot order the two.~~
      **FZ-3 ANSWERED 2026-09-11 (OPUS-NOTICE-FZ3-STATIC): they survive, so a one-time good does not
      return.** The mask has two callers and neither reaches a loaded image: `00233C10` masks only in
      its first-bind arm, taken while `02EBF190` is null (`00233C19`–`00233C3A`) — and the pointer
      is bound at boot (`0022B6E0` → `SaveRuntime_ResetActiveImageAndRebindState`, `0022B78B`;
      `0022B6E0`'s 9-member exclusive subtree is bound on
      [the resource-queue page](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md)); the
      rebind `00238A80` is reached only through `002EF650`, which memsets the image to zero first
      (`002EF656`–`002EF663`) and is taken only when the header fails `SaveImage_ValidateRuntimeFormatHeader`
      (`0028037B`, `003941E5`). A loaded image is read whole into the active buffer
      (`005810BC`–`0058111E`) and bound through `00285E60` → `00233C10`'s non-null arm. So bit 0 —
      cleared by nothing but the purchase's `&= ~2`, which keeps it — survives; the refresh's first
      clause rejects the row, and the tallies are zero besides (OPUS,
      [the contract](CONTRACT-bazaar-unlock-and-purchase.md) §7). The flag bytes reach the save
      inside the capture's whole-block copy of the state block ([the save page](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md) §5).

      > **The endpoint is now observed, not only argued — 2026-09-21 (ASTRA,
      > `ASTRA-RETURN-FABLE-CONTRACT-LIVE-REUSE`; consumed by FABLE).** `FZ-3` above was answered from
      > static reachability alone: neither caller of the mask reaches a loaded image, therefore the
      > loaded bytes survive. An older `FFXII_004` has since been loaded in a live process, and **both
      > regions come back full** — **18 nonzero flag bytes and 44 nonzero loot-sold counters**, at
      > old-load-complete and again at settled old field, **every byte matching the documented decoding
      > of that exact file**. Modern-field and returned-title samples read zero in both regions, so the
      > nonzero reading is stage-bounded rather than a constant of the process.
      >
      > **The offsets only mean something with their frame attached.** Getter `002EF640` returns the
      > **image** base, `02164280`; the **payload** base is `0x200` past it, the header's own width, and
      > the capture's caller chain (recorded in the package README) performs that add. So a payload
      > offset handed to the image base names a byte `0x200` away from the one intended. The captured
      > binding was `B = 021B290C` — image `+0x4E68C`, payload `+0x4E48C`:
      >
      > | region | `B`-relative | payload-relative | whole-image-relative | width |
      > |---|---|---|---|---:|
      > | loot-sold counters | `0x57C8` | `0x53C54` | `0x53E54` | 512 |
      > | bazaar flags | `0x59C8` | `0x53E54` | `0x54054` | 128 |
      >
      > *The counters are 512 bytes wide and the header is 512 bytes*, so **the counters'
      > whole-image offset and the flags' payload offset print as the same number, `0x53E54`** — the
      > one place a frame-blind reading would stack two different bytes on top of each other. The
      > flags' `B`-relative offset is also exactly the one the contract already added statically:
      > §3 computes the flag byte's payload offset as `0x4E48C + 0x59C8`, and the live capture binds
      > `B` at payload `+0x4E48C` and finds the flags `0x59C8` past it. The declared sub-object offset
      > and the captured binding are the same two numbers, reached from opposite directions.
      >
      > ***What it does not show is that the mask never ran.*** Nonzero final values establish that
      > the file's bytes are what survived; they cannot exclude a clear or mask *in between*. Nothing
      > here should be written as "these bytes are never cleared" — only as **"whatever ran left the
      > loaded values in place"**, which is the claim `FZ-3` actually needs. Also still unobserved:
      > **saving a new purchase and reloading it**, the refresh order across that roundtrip, the
      > behaviour of a one-time good after it, and any shop menu — no row is tied to a named good here.
      > (The payload extent used above is `0x56490`; [the contract](CONTRACT-bazaar-unlock-and-purchase.md)
      > ~~§3 still prints `0x564D0`, `0x40` bytes long, which is OPUS's to correct~~ **— corrected
      > 2026-09-21 (OPUS), in §3 and in the §13 claim-map row; this page was right and the contract
      > was the one carrying the wrong figure.** It changed no containment result, here or there.)
- [x] ~~**What `+0x14` bit 1 means** on the seven *Forgotten Grimoire* rows, and what flag bit 2
      is.~~ **FZ-4 ANSWERED 2026-09-11 (§2.1, §2.2):** bit 1 marks a good whose availability a
      script sets directly; flag bit 2 is the shop UI's marker.
- [x] ~~**UQ-130.** What `+0x22` = 120 is for; no reader was found.~~
      *Narrowed 2026-09-14 (FABLE): "no reader" is contradicted by §2.6 of this page.* The query record builder's
      class-18 arm copies `+0x22` into query record `+0x2C`, beside the price. What reads a class-18 query's `+0x2C`, and
      so what 120 means on screen, is still open.
      ***ANSWERED 2026-09-17 (FABLE): `+0x22` is the good's icon, a frame index into the menu icon sprite; 120 is the one frame every bazaar good shows.** Query record `+0x2C` is the icon slot for every class the builder `0031C5D0` fills: it takes item row `+4`, equipment row `+4`, loot row `+4`, magick and technick row `+3`, gambit-condition row `+3`, key-item row `+4`, action row `+0x22`, bazaar row `+0x22`, and `-1` for a quickening, which has no icon (the class table on [the query-record page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)). Its readers make it a frame: `0057AC10` (`0057ACE1`..`0057ACF9`), `0057B1A0` (`0057B327`..`0057B336`) and `003F41C0` (`003F4243`..`003F4254`) sign-extend the value, store it as the sprite node's frame index `+0xA` and copy byte 7 of the frame's 8-byte sub-image record (from the node's `+0x20`) into the node's opacity byte `+0x39`, exactly the frame select the sprite-node constructor performs from authored data on [the typed-list page](../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md), and the same idiom appears at 55 sites in the menu code. The bazaar listing's own reader is `0057DC30`, already placed on this page as a reader of the good's runtime flag bit 2: for a class outside 6 and 10..12 it stores `-1` at entry `+2`, the query's `+6` at entry `-2` and the query's `+0x2C` as the entry's icon byte at `+0` (`0057DCB9`..`0057DCCC`), and its three siblings `0057DAD0`, `0057DD60` and `0057DED0` copy the same byte for their lists. A byte that every shipped row sets to 120 is one shared frame: the bazaar package icon rather than the granted item's, which is why the table carries it at all. Which picture frame 120 holds is in the atlas, not the code. Static, builder arms and reader bodies read; the reading also names item, equipment and loot row `+4` and magick row `+3` as their icon bytes.*
- [x] ~~**UQ-131.** Where `0056D370` is reached from, and how it turns a bazaar selection into
      `Shop_CommitPurchaseItemAndGil(good, 1, price, flags)`.~~ **Answered 2026-09-14 (FABLE).**
      - **Reached from.** `0056D370` is a widget procedure, the trade panel of
        [the shop screens](../16-UI/Shop-Screens/the-shop-screens.md).
        - A 268-byte installer constructs it through the widget factory with a `0xE8`-byte object and this procedure
          (`0056C9B7`–`0056C9C3`).
        - The panel's mode byte sits at `+0xE4` bits 6–13.
        - The installer is called by the shop page's panel rebuild and by its directional-input helper. The outer shop
          menu's `0x8001` sub-command reaches both.
        - That explains the missing static caller: the procedure is dispatched by message.
      - **The commit.** It runs on message 12 with argument `0x8001`, only while the quantity child `+0xC8` exists
        and panel flag `+0xE4` bit 1 is set (`0056D42B`–`0056D44A`).
        - The selected entry `[+0xD0]` supplies the id (word `+0x08`) and the unit price (dword `+0x10` with bit 31
          cleared).
        - The quantity is the panel's word `+0xDC`. The total is price × quantity (`0056D450`–`0056D46C`).
        - Flag bit 0 selects the direction. Set: `Shop_CommitSaleItemAndGil(id, qty, total, 0)`. Clear:
          `Shop_CommitPurchaseItemAndGil(id, qty, total, 0)`. The fourth argument is a literal 0, and the quantity is
          the panel's, not a fixed 1.
      - **Only in bazaar mode.** When the mode byte is `0x0B` (`+0xE4 & 0x3FC0 == 0x2C0`), a purchase also calls
        `BattleIdClassD_SetRuntimeFlagBit2(id, 0)` (`0056D4AC`–`0056D4C0`). ~~Then:~~ That test guards only this call; the rest runs in every mode *(corrected 2026-10-02, OPUS: checked at `0056D4AC`–`0056D4D2` — the `0x2C0` test skips only `call 0030B630`, and `cl = 0x13` / `call 00316A50` runs on every purchase; the PlatformOnlineAchievements crossing below)*:
        - a purchase, bazaar or not, calls the 411-byte achievement routine with id `0x13` and the good;
        - a sale in mode `0x07` (`0x1C0`) calls it with id `0x0E` and the quantity;
        - the gil display is moved by the signed total (`0056D4D9`).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the row layout and the three readers of each field | `002FD7F2`–`002FD85D`; `0030B33F`–`0030B461`; `0030B20C`–`0030B256`; `0031DA1B`–`0031DA9D` | 1 |
| the sale adds channel 3 and refreshes | `003108D1`–`003108ED` | 1 |
| channel 3 is region B, the loot descriptor's `+0x18` = `0x57C8` | the encoded-id space page §2.2, §2.7; `002FD1BF`–`002FD237`, `002FD906` | 1 |
| the refresh's five conditions and the `|= 3` | `0030B2D0`–`0030B477` | 1 |
| the purchase clears bit 1 and zeroes the three tallies | `0030B203`, `0030B20C`–`0030B256` | 1 |
| only the sale and the reset use channel 3 | every call site of `003008A0` (25 callers) read for its `r9d` argument, 2026-09-11 | 1 |
| the rebaser masks the 128 bytes with `0xF8` on bind and rebind | `0030B739`–`0030B75B`; callers `00233C10`, `00238A80` | 1 |
| the menu record carries flag bits 0–2 | `0031DA69`–`0031DA9D` | 1 |
| every name, item, loot, price and flag of the shipped table | the `us` section at `0x25370`, all 128 rows decoded through the class tables | data |
| the shop driver is the sole caller of both commits | `edges.tsv` | 1 (graph) |

## 9. Related

- [`the-encoded-id-space-and-the-query-record.md`](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) — the descriptors, channels, regions and the class-18 handler.
- [`the-battle-state-block-field-map.md`](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) — `+0x59C8` and `+0x57C8`.
- [`the-save-payload-field-map.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) — payload `+0x53E54`, the rebind.
- [`battle-text-banks.md`](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) — bank 9, the goods' names.
- [`the-post-result-events-and-the-battle-message-table.md`](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) — the obtain-item and obtain-gil lines the commits post.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

The section was re-decoded from `battle_pack.bin` without reading the prose. **Every census
reproduces but one.**

| claim | measured |
|---|---|
| directory `+0xE8` → file offset `0x25370` | **`0x25370`** |
| `st2e`, **128 rows × 36 B** | **128** and **36** |
| "81 rows want three loots, 9 two, 31 one, 7 none" | **81 / 9 / 31 / 7** |
| "`+0x14` is 0 on 106 rows, 1 on 15, 2 on the seven Grimoires" | **106 / 15 / 7**, and the seven are rows **99–102** and **124–126** |
| "`+0x22` is 120 on every row" | **120 on all 128**, no other value |
| `+0x02` = `0x55F0 + row` | true on **all 128**, no exception |

> And the name bank agrees from the other side: **bank 9 holds 128 entries**, re-derived in today's
> [battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)
> pass — one entry per bazaar row, the two tables sized to each other.

### ⚠ The price range is wrong at both ends

`corpus_validated` gives **"prices 100 … 250,000"**. The true range is **70 … 600,000**, over **100
distinct values**, and **four rows lie outside the stated bounds**:

| row | price |
|---:|---:|
| 105 | **70** |
| 103 | **99** |
| 95 | **350,000** |
| 96 | **600,000** |

The `250,000` is real — it is *Morbid Urn*, row **127**, the figure §1 quotes — but it is **not the
maximum**, and two goods cost more, one of them more than twice as much. A reader sizing a field or a
UI column from the stated range would be short by a factor of 2.4, and would also assume no good
costs under 100 gil when two do.

**The engine half was read on 2026-09-12.** `OPUS-PASS-BAZAAR`, on
[the contract](CONTRACT-bazaar-unlock-and-purchase.md), took `0030B1AC`–`0030B1FD`, the signed
class bound and the `+0x59C8` masks instruction by instruction. **This pass is the other half** —
the shipped rows against the censuses — and neither repeats the other.

**Not claimed:** the three functions (`0030B33F`, `0030B375`–`0030B45F`, `0030B225`/`0030B240`), the
state-block flag byte at `+0x59C8`, the sold tally at `+0x57C8` and the name resolution through bank
9 were **not** re-read — this pass checked the shipped rows against the censuses, not the engine
against the rows. Nothing was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Rewards_Progression_Economy — SERVICE.** The purchase and sale commits `Shop_CommitPurchaseItemAndGil` (`002FEEB0`)
  and `Shop_CommitSaleItemAndGil` (`00310870`) both read and write gil through `GameState_GetGil` / `GameState_SetGil`.
  So [the achievement catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md)'s
  gil counters 6 and 7 fire on shop trades. The 1,274-byte `0056D370` reads gil.
- **PlatformOnlineAchievements — SERVICE.** `0056D370` fires achievement counter **19** (mode 1, threshold 53375)
  through the counter updater, with a word from its record's `+8` (AB-7). *(2026-09-30, OPUS, on SWE2-STRUCT's DD batch 11, [`swe2struct-ddres-b11-0930`](../_index/candidates/swe2struct-ddres-b11-0930/README.md) S1-S2: it also fires counter **14** (`ACH_COUNT_SELL_EVITEM`, *Privateer*) on a sale, with the quantity sold (`+0xDC`), when `+0xE4 & 0x3FC0 == 0x1C0` (`0056D483`-`0056D498`); counter 19 fires on every purchase - the bazaar-mode test `0x2C0` guards only the `0030B630` unlock call (`0056D4AC`-`0056D4C0`).)*
- **Input and Presentation — CLIENT of boot mode 0.** `0022B6E0`, the boot frame mode cited here, calls
  `InputControl_SetOneShotFrameCallback` and a 39-byte Input-filed helper. It also calls the graphics-sync pair
  `GraphicsSync_ClearSharedCommandState…` / `GraphicsSync_WaitBackendState100Clea…` and three Presentation bodies of
  71–979 bytes. See [between two frames](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)
  for the mode table. None of this is bazaar logic.
- **ActorEntity - SERVICE (42 edges).** `00234DA0`, `002350C0` reach bodies filed to ActorEntity: `00265020`, `0031B810`, `00300E40` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (12 edges).** `002367A0` is also called by bodies filed to movement: `00312730`, `00326BB0`; `0023A410` reaches bodies filed to movement: `00300310`, `003208C0` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (24 edges).** `002367A0` is also called by bodies filed to party: `00326500`; `00234DA0`, `002350C0` reach bodies filed to party: `003273B0`, `003272A0` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `0022B6E0` reaches bodies filed to random selection: `00379CD0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (5 edges).** `0023A3B0`, `0032AB50` are also called by bodies filed to script VM / native bridge: `00510160`, `0034C2C0`, `0034C710`; `0034C2C0` reaches bodies filed to script VM / native bridge: `00267E10` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT and SERVICE (8 edges).** `00234DA0` is also called by bodies filed to spawn/encounter lifecycle: `00234AF0`; `002350C0`, `0023A3B0`, `0023A570` reach bodies filed to spawn/encounter lifecycle: `00306E60`, `002355A0`, `00236100` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT and SERVICE (16 edges).** `0030E130` is also called by bodies filed to status/periodic terminal: `0030E970`; `0023A410`, `0030E130` reach bodies filed to status/periodic terminal: `0030FED0`, `0030EA40` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (15 edges).** `0022B6E0`, `00234DA0`, `002350C0` reach bodies filed to WorldAreaField (world area): `003318C0`, `00313F60`, `00320940` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatAction — CLIENT.** `BattleAction_PrepareExecutionResources` and `BattleAction_RefundReservedExecutionResources` call a cited function.
- **CoreRuntimeScheduling — CLIENT and SERVICE.** Cited functions are called by a 255-byte boot-mode body and a 465-byte core body, and one reads a 7-byte core getter.
- **Resource — SERVICE.** A cited function calls a 107-byte Resource helper.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — SERVICE.** `00233C10` on this page calls `GambitRuntime_RebuildAllOrderSets`, owned by that layer. What it reaches is the 437-byte gambit re-form, and it is where the gambit numbers live: it walks the same **40 records of `0x1C8` bytes** the battle stats table holds, takes each record's `byte[+0xC]` as the owner index, and fills that owner's `0x170`-byte slot from **twelve** enable-mask bits, copying ten fields per row out of the definition table indexed by **`id - 0x6000`** and skipping the `0xFFFF` sentinel pairs; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleFormula_ApplyTargetResult`, owned by that layer, calls `003008A0` on this page. That caller is the target-result application: it resolves the owning unit for both the source and the target stats records, keeps bit 9 of its flags argument as a switch, and **unless bit 0 is set** runs an eligibility test between the two units that abandons the whole call when it fails; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — SERVICE.** `0030B270` on this page calls `FUN_0030adc0`, owned by that layer. What it reaches is one of a pair of 105-byte id dispatchers built exactly like the encoded-id query: `0xFFFF` answers `-1`, the top nibble must be `0xE000` or below, and `id >> 12` picks the arm; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (SWE2-EC7-167, 180 edges).** The message-path helpers this page's purchase bodies
name — `002DD7E0` (the `002CC780` pair's message issuer), `0029FB50`, `0029FF60` and the pointer
codec `0020E620` — are called throughout the UI layer (`002A86A0`, `00555330`, `00559E30`,
`0057CF20`, +176 more). Shared message-path fan-in: the shop screens reach these helpers the
same way the recipe purchase does, and no UI responsibility moves here.

**Save_Load_Settings — shared helpers.** `0057AA00`'s dispatcher names the shared `00254A10` gate (called by `005832B0`), the `002F9860` scratch allocator (called by `00582860`), `00861EC0` block clear and the `0020E600` offset resolver (called by `00253240`) - all utility code the save/load layer consumes the same way; no save responsibility moves here.

## Interior citation — frontier hub `0031C4C0` (2026-09-18, SWE2-EC7)

`0031C4C0` — 59 B, 15 callers; the encoded-ID-gated table byte the unlock paths share.
Interior verified: `BattleEncodedId_IsValidForClass` (`00322C50`) with `(0x17, ecx, 0)`
gates the read ([`0031C4D2`](../_index/ADDRESS-INDEX.md)) — invalid ids return `0xFF`;
valid ones read `byte [02EBF190 + ecx*2 + 0x5A7E]` at
[`0031C4ED`](../_index/ADDRESS-INDEX.md), the word-pair table's flag byte for the class.

### Crossings — ActorEntity / Movement / Status_Periodic_Terminal (batch-9 hub exposure)

Naming `00322C50` (`BattleEncodedId_IsValidForClass`) and `0031C4C0` exposes their
non-Items caller sets on this page. The predicate is shared *policy*, not Items machinery —
the bazaar path borrows the same validity check the wider game does:

- **ActorEntity** (6 edges): `0031C4C0` is called by `00265A20`; `00322C50` is called by
  `002367A0`, `0023A570`, `0031B810`, `003266C0`, `00329CC0` — actor/unit code validating
  encoded ids against their class before use.
- **Movement** (2 edges): `00322C50` callers `0031BAC0`, `00326BB0` — movement-side records
  running the same check.
- **Status_Periodic_Terminal** (3 edges): `00322C50` callers `0030E130`, `0030FED0`,
  `00310DB0` — status/periodic handlers validating ids the same way.

- **Spawn_Encounter_Lifecycle** (5 edges): the named ActorEntity/Status callers themselves
  live in the spawn path -- `0023A570` calls `00236100` and is called by `0023A3B0`,
  `0031B810` calls `00234DA0` and `002350C0`, and `0030FED0` is called by `0023A410`.
  Spawn/encounter construction runs the same class-validity check on encoded ids.


### Interior citation — frontier hub `0035D380` (2026-09-18, SWE2-EC7)

`0035D380` — 73 B, 14 callers (`003F41C0`, `0056E410` and peers above). Stores
`ecx`/`dx` into the `022CA480` record, runs `0031C5D0` on the
`022CA480` record, and on a negative result calls `0016D6A0(0x800)` then
`00861EC0` zeroes the 0x98-byte block at
[`0035D3BB`](../_index/ADDRESS-INDEX.md) — returning the block pointer either
way. A lookup-or-clear on a named record.

Cross-subsystem note: `0057AC10` among the callers above also reaches into
Audio (one edge) — the sound priming the purchase flow plays.

## SWE2-EC7-40 update (2026-09-19) - `0057DD60`

`0057DD60` (363 B) is a bazaar body - `0035D380` pair plus `002B58B0`. Interior anchor `0057DDCE` (a `0035D380` call).

## SWE2-EC7-41 update (2026-09-19) - `0057DED0`

`0057DED0` (345 B) is a shop/bazaar body - `0035D380`/`002B58B0` pair. Interior anchor `0057DF35` (a `0035D380` call).

## SWE2-EC7-41 update (2026-09-19) - `0057DAD0`

`0057DAD0` (343 B) is a shop/bazaar sibling - `0035D380`/`002B58B0` pair. Interior anchor `0057DB50` (a `0035D380` call).

## SWE2-EC7-100 update (2026-09-20) - `002CC4F0` measured

`002CC4F0` (251 B) is the nine-slot refresh `0056D370` and
`0057B1A0` call on the `0209AC30` `+0x2E0` object: one
`002CB1F0` against `[rbx+0xC8]` with `(word[+0x16A] & 0xF,
si)`, then a nine-iteration `0x8`-stride loop running
`002CA7C0` per `+0xD0` slot; afterwards, when
`dword[+0x168]` carries either `0x300000` bit and
`si != 0xFFFF`, `0035D330(1, si << 16)` resolves a record
whose `[+0]` value in `{8, 9, 0xB, 0xC}` arms `+0x168`
bit 22 (bit 23 cleared), anything else clearing both -
the per-entry sweep plus flag-arm the bazaar list runs.
Interior anchor `002CC550` (the `002CA7C0` loop head).

## SWE2-EC7-103 update (2026-09-20) - `0027F360` + `0027ED10` measured

`0027F360` (204 B) and `0027ED10` (141 B) are the
mod-9 ring step pair `002C2240`, `00568280`,
`002C2200`, `00567990` and `0057AC10` call on the
`0209AC30` shop record: `0027F360` advances
`(word[+0xDE0] + 1) mod 9` (`0x38E38E39` magic
divide) and `0027ED10` retreats
`(word[+0xDE0] - 1) mod 9` (`cmovs` to 8), each
walking the nine `+0xAC8` slots until it returns
to `+0xDE0`; when `+0xD3C` bit 4 is set a slot is
eligible only while `word[+0x60]` is nonnegative,
`byte[+0]` bit 1 is clear and the word is `<= 5`,
and unconditionally while `word[+0x60] >= 0` on the
plain path; a hit stores `byte[+0xDE9] = 1`/`2`,
publishes `word[+0xDE0]` and runs `0027F210`,
returning 1 (0 on full wrap) - the next/prev
eligible-entry steps the bazaar arms drive.
Interior anchors `0027F388` (the `x*9`
remainder) and `0027ED33` (the `cmovs`
wrap).

`0057B680` (32 B) is the `02CA9790` indexed getter `0056D370`'s shop driver uses: null global or `ecx >= 1` returns 0; otherwise `movsxd`s `ecx` and returns `[[02CA9790] + ecx*8 + 0x158]` — the shared object's `+0x158` pointer table, valid only for index 0.

Interior anchor `0057B697` (function `0057B680`).

`0057A980` (117 B) is the `02CA9790`-gated submit `0056D370` runs: when the global is live it builds `{ptr=[g+0x158], w0=dx, w1=r8w}` context and calls `00244F50(0x2D8, 0057A620, &ctx)` — a `0x2D8`-kind create dispatched to the `0057A620` handler; a dead global skips the submit entirely.

Interior anchor `0057A9DE` (function `0057A980`).

`0057A480` (90 B) is the ungated `00244F50` submit `0056D370` shares: context `{w0=dx, ptr=rcx}` with callback `0057A4E0`, size `0xF0` — the small sibling of `0057A980`'s `0x2D8` create.

Interior anchor `0057A4C3` (function `0057A480`).

`0030B630` (104 B) is the `0xDxxx` unlock-bit setter `0056D370` and the precheck `0057B6F0` share: only ids with `(cx & 0xF000) == 0xD000` that `00322C50(1, id, 1)` confirms as live reach the write — `u8[02EBF190 + 0x59C8 + (id & 0xFFF)]` has its bit-2 field cleared then set to `(dl & 1) << 2`. Everything else is a silent no-op.

Interior anchor `0030B67E` (function `0030B630`).

`0030B4B0` (94 B) is the read half of `0030B630`'s flag: the same `0xD000` high-nibble gate and `00322C50(1, id, 1)` existence check, then returns `u8[02EBF190 + 0x59C8 + (id & 0xFFF)] >> 2 & 1` — 1 when the recipe/purchase bit is set, 0 on any failed gate or a clear bit.

Interior anchor `0030B4FA` (function `0030B4B0`).

`0056E700` (307 B) is the packed flag-word evaluator `0056C490`/`0056D370`/`0056CA60`/`0056D9D0` consult on entry records: entry `[rdx]` bit 0 takes the direct arm — base 8 when `[rcx+0x10]`'s sign bit is set, `|2` when the `movsx [rcx+0xC]` index is 0 (with `[+0xE]` substituting on -1), and entry bit 2 adds `|1` unless the index exceeds `word[rdi+4]`. The clear-bit-0 arm instead ranges `word[rdx+6]` against `0xFF` and `[r11+0xE]`, folds `[r11+0x10]`'s magnitude (sign bit stripped) against `[rdi+8]` for bit 2, and under entry bit 2 runs the `r9d`-stride loop whose clamped count lands in `[r8]` — bits {1, 2, 4, 8} mark in-range / more-entries / extent / base.

Interior anchor `0056E7F0` (function `0056E700`).

`0056E580` (68 B) is the `+0x194` bit-1 setter `0057AC10`/`0057C010` run: `edx == 0` sets the bit (else clears), the object registers through `00246AD0(0208EA28, this)`, and the tail `0056C850([this+0xC0])` resyncs the record — the marker-and-refresh pair.

Interior anchor `0056E5B2` (function `0056E580`).

`0056C850` (249 B) is the record resync `0056D370`/`0056E580` run on a pane object: `[+0xC0]`'s `+0xE0` gains 0x200000 then `002D45C0(rec, 1)`, then 0x8000000 with `002445C0`; `0056E410([+0x10])` decides the branch; `0056C490(this, 0)` pushes state; when `[+0xC8]` is live and `[+0x10]`'s `+0x7C` low nibble is 1 the child registers through `00246AD0(0208EA28, child)`; a set `r14` runs `0056E5D0(child, 0)`, a null `[+0xC8]` instead `00293110(0, 0)`s, sets `[child+0x194]` bit 2 and `00244F00`s it; `[+0xE4]` bit 5 is cleared on exit.

Interior anchor `0056C8D1` (function `0056C850`).

`0056C490` (959 B) is the record-state push `0056C850`/`0056D370`/`0056CA60` run on the pane object: `[+0xE4]` bits 0x3FC000 suppress the `00D23580` presence-table walk — row `(e4 & 1)·0x24` (`+0x12` when `dl` set) lists `[row]` stride-2 `{index, style}` pairs whose `[+0x60]`-indexed objects get `+8` bit 0 set with `0029FB50`/`0029FA40` on style 1/2, then `[row+1]` more indices cleared. `dl == 0` masks `[+0xC0]+0xE0` to the plain set (0x20000000 on; 0x20000/0xC0000000/0x1C0000 off) and clears `[+0xD8]` bit 1; `dl != 0` sets it, ORs 0x20000 | 0xC0000000, picks `[rdx+0x106]` from the `{3,2,2,2}` array by `e4 >> 0xE`, and copies the parent's `+0xEC·(+0xF2 + +0xF4) + +0xEE + +0xED` geometry into the child's `+0xF2`/`+0xF4`; the suppressed case instead ORs 0x1C0000 and centers `[+0xFA]` on `02CA9710`. `0056E700([+0xD0], rdi, 1, 0)` then folds the evaluator into `+0xE4` bit 2, mirrored onto `[+0xC0]+0xE0` bits 19/20; `00567690([r15+0xC8], rdi, 0)` syncs the child's table, `002F9860(0xC6B|0xC6C + (e4 & 1)·2)` -> `00291D80(text, 0)` posts the message, and `+0xE4` bit 1 is XOR-mirrored from `[rdi]` bit 1.

Interior anchor `0056C7AF` (function `0056C490`).

`0056E5D0` (303 B) is the record-activation arm `0056C850`/`0056DD50`/`0056DED0`/`0056E140` run on the pane object: `0056E880(byte[+0x190], byte[+0x191], ~(+0x194) & 1)` returning 0 skips to the tail; nonzero posts `002F9860(0xC6B + (+0x194 & 1)·2)` through `00291D80(text, 0)`, resolves `di` = the `(+0xF2 + +0xF4)·+0xEC + +0xEE + +0xED` extent's `+8` word over `[+0xD8]`'s `0x20`-stride table (sentinel 0xFFFF when the table is null), and unless `+0x180` bit 0x4000000 is set runs `00293100(00D235D8[+0x191] or 0, di << 16 or 0, arg)` — the selected-record activate. The tail: `+0x191 != 0xB` runs `002CC4F0(di)` then `002CC2A0()`.

Interior anchor `0056E693` (function `0056E5D0`).

`0056E410` (357 B) is the member-count arm `0056C850`/`0056DD50`/`0056DED0` run on the pane object: `r14 = this + ((+0x180) << 6 >> 0x1B)·8` selects the slot; a live `[rsi+0xC8]` resolves `rbx = [+0xC8] + extent·0x20`, then `003933B0(byte[+0x191])` -> `0035D380(eax, word[rbx+8])` — a nonzero `[resolved+0x24]`, or `+0x191 == 0xB` with `0030B4B0(word[rbx+8])` zero, clamps `ebp` into the `[+0xD8]+0xE8 - 1` bound (re-basing `rbx` on the clamped row), writes `+0xF2`/`+0xF4` = 0xFFFF and returns `clamped + 2`; the plain arm only writes `+0xF0` = `word[rbx+8]` and returns 0. `005655F0(this, r14+0xF0, byte[+0x190])` runs, `003697F0([rsi+0xC8])` frees the old child, and `[rsi+0xC8]` = `[rdi+0xE0]` with `[rdi+0xE0]` = 0 hands off the pending object.

Interior anchor `0056E4AD` (function `0056E410`).

`00565A00` (454 B) is the find-and-commit slot command `005655F0` runs — the call `0056E410` makes: `di` = `word[r8]`; a `0xFFFF` or a null `[+0xE0]` commits `002D47C0([+0xD8], 0, 0, 1, 1)`, and both `r8+2`/`r8+4` non-0xFFFF commit `002D47C0` on them directly; otherwise `002D1820([+0xD8], &out, 0)` yields `r11d`, `ebx` = `(+0xF2·+0xEC) + +0xEE + +0xED`, and the `[+0xE0]+8+i·0x20` table is scanned for `word == di` over `edx` entries — a hit at `r8d` runs the `[+0xE8]`-bound scroll-window clamp against `r14d = r11d - 1 + ebx` before `002D47C0(rec, ebx, r8d, 1, 1)`; a miss keeps `r8d` = 0.

Interior anchor `00565ADE` (function `00565A00`).

`002CA7C0` (1065 B) is the per-slot worker `002CC4F0`'s nine-slot refresh runs: `00282DF0([rdx+0xD4])` resolves four times, `r9w` supplies the slot index, and `002CA3B0`, `002DD7E0`, `0035D330`, `002CB360` x2, `00282EE0`, `0031C4C0`, `00317B70`, `002CA5D0`, `0030A4E0` x2, `002CC780` x2 rebuild the slot state before the cookie check - the refresh's per-entry body.

Interior anchor `002CA7F2` (function `002CA7C0`).

`002CB360` (325 B) is the compare-and-flag `002CA7C0` calls: `00282DF0` resolves `[rdi+0xD4]` and `0209AC30`'s `word[+0xDE0]` records, compares their `word[+0x60]` type ids, and sets bit0 of `+0x8` on the `+0x48` node (and `+0x50` when `dword[rdi+0xE0]` is zero) on match; mismatch arms emit `0xF4`/`0xF5` via `002DD7E0` and the `esi`-zero arm stages `0x64`/`0x15`/`0x20` messages through `002CA3B0` - the stock-state refresh behind a recipe purchase.

Interior anchor `002CB39C` (function `002CB360`).

`002CA3B0` (128 B) is the record stager `002CA7C0`/`002CB360` call: resolves `rax = [rcx+0x60][edx*8]` (0 when rcx null), clears `dword[+0xC0] &= 0xFFFFFF41` then sets `(r9d&0xF)<<2 | 0x41`, writes `word[+0xC4] = byte[rax+0x3B]`, `word[+0xC6] = dx`, `word[+0xC8] = r8w - ax`, `dword[+0xCC]` = the `[rsp+0x28]` arg x 0x3C magic-divided (`0x10624DD3`/`sar 6`), and `dword[+0xD0]` = the `0208F570` tick - the field staging behind a staged `0x64`/`0x15`/`0x20` message set.

Interior anchor `002CA3C7` (function `002CA3B0`).

`002CC780` (324 B) is the purchase loop `002CA7C0` calls: `002DD7E0` issues message 0 (and a `setle`-selected 4/5 when `edx` nonzero) into `r14d`; `or dword[rdi+8],1` marks the node, `abs(ebx)` (cdq/xor/sub) becomes `r9d`, `0029FF60`/`0029FB50` run on `rdi`, `dword[rdi+0x24] = r14d`, then a `/10` loop (`imul 0x66666667`) iterates `ebx` times over `0029CCD0`/`0029CCF0`/`0020E620` - the per-item stage-commit behind the recipe purchase.

Interior anchor `002CC7EC` (function `002CC780`).

`0029FB50` (126 B) is the record field commit `002CC780` (the purchase loop) runs: `(rec+8 <<0x10)>>0x16` sign-extends a 10-bit field, `0020E600` resolves `+0x20`, `002D8B00` writes the pair; the returned `sx word` times `float[+0x28]` subtracts from `word[+0x10]` and adds `word[+0xC]` into `word[+0xA]`; `byte[+0x2D] = (b & 0xD7) | 0x10` - the stock-slot's post-purchase refresh.

Interior anchor `0029FB8F` (function `0029FB50`).

`0027F210` (199 B) is the five-slot stock-block rebuild the `+0xDE0`-cursor publish runs: five iterations (`rsi 0x98 -> 0xAC` step 4, `r14 0xD40` step `0x20`) zero each `0x20` record, copy `word[slot+rsi+2]` into `+8`, and for non-`0xFFFF` entries `0035D330(1, id<<0x10)` then `002B58B0([+0x18])` resolve the pointer while `byte[rdi+0x2C]`/`+0x38` land at `+0xA`/`+0xB` - the `0209AC30` context's slot-array refresh.

Interior anchor `0027F290` (function `0027F210`).

`00317B70` (76 B) is the registry-slot class dispatch the purchase paths share: `cl > 0x27` fails to 0, else `[02EBF190] + 8 + cl*0x1C8` selects the class record inside the same 0x1C8-stride bank the unlock flags live beside, `+0x50` heads its sub-object, and `00317930(row+0x50, dx, ~r9&1, [rsp+0x20])` runs - the class-indexed service entry behind the bazaar writers.

Interior anchor `00317BAB` (function `00317B70`).

`0057AA00` (515 B) is the item-kind dispatcher `0057AC10` calls per purchase request: `bl` kind 0 zero-builds a `0x50`-byte block (`00861EC0`, `|0x10` flag) and emits `003948B0(rbp, 0x21071, buf)`; kinds 1/2 fetch the `0035D380(6, r8w)` record and resolve `[rax+0x18]` through `002B58B0`, then fork on `00254A10` - true issues `002B4090` over a `002F9860(0x854)` (kind 1) or `0xCF8` (kind 2) scratch buffer, false walks `02EBF018` through two `0020E600` hops and the `edi`-selected `0x190`/`0x194` slot index before `002B40C0` issues it - and every armed path finishes through `003949B0` with the `{type 3, flags 0x0A|bts7}` request block on the stack.

Interior anchor `0057AB12` (function `0057AA00`).

`002CB1F0` (361 B) is the row refresh `002CC4F0` runs per bazaar entry: it clears bit 0 of the `+8` flag dword on both `[rdx+0x60]` records, and unless arg3 is `0xFFFF` it looks up the `0035D330` row keyed `(1, arg3 << 16)` - required type 6 - then dispatches on the row's `+0x50` value and `+0x38` bands (`0x15`/`0x16` vs `0x17..0x1A` vs the fallback) to pick one of the message ids `0x4A90`-`0x4A94`; each arm sets the dirty bit on both records, stores the `002F9860` string for the picked id through `0020E620` into the record's `+0x18`/`+0x20` fields, and finishes with `0029FB50` re-layout on both.

Interior anchor `002CB2AA` (function `002CB1F0`).

`002B5A20` (142 B) is the code-write `0029CCF0` calls: `ebx >= 3` required on `0039C4A0`'s record, `esi` selects `dword[+0x18]`/`+0x14` through `0020E600`, `ebp` selects `word[+0x16]`/`+0x1A`, then `cl` is emitted - `cl - 0x20 <= 0xDF` writes one byte, wider writes `cl >> 8` then `cl` - NUL-terminated with the length+1 returned - the one/two-byte glyph emit for the recipe text.

Interior anchor `002B5A6E` (function `002B5A20`).

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-the-bazaar-recipe-unlock-and-purchase-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `002ABAA0` | 126 B | `0029CCD0` + 0xE | calls `002ABAA0` + 0x8 and, only when that returns 0, `002ABAA0` + 0x11; when the second call returns 7 and `ecx` is zero it returns 26 (`00916484`, truncated) with no further call; on every other path it makes one call (`002ABAA0` + 0x1F, `002ABAA0` + 0x48 or `002ABAA0` + 0x63) and returns the truncated (`cvttss2si`) product of its `xmm0` result with 15 (`00916314`) when `ecx` is non-zero or with 10 (`008F8180`) when `ecx` is zero | Interior anchor `002ABAB6`; Interior anchor `002ABAD6`; Interior anchor `002ABAC4`; Interior anchor `002ABB0C`; Interior anchor `002ABACC` |
