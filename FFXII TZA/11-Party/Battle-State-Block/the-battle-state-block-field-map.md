---
system: The battle-state block — the 0x7410-byte image-backed record behind 02EBF190, field by field above the forty stats records
category: 11-Party
status: AUDITED
owner_layer: PrimaryOwner:Party (the configuration, slot map and leader) — the mode words are CoreRuntime, the result echoes CombatFormula, the gambit banks CombatAI, the inventory snapshot Items
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: a typed field scan (hop_scan) seeded by the qword at 02EBF190 over the block's 0x7410 bytes (the
    size the reset 002370C0 clears), depth 2, control 00385BA0's write at +0x5B0E found; 1,145 accesses in
    217 functions over 165 offsets (1,236 / 232 / 173 before 91 rebased rows were removed 2026-09-13); the small writers and readers of the region above the records read to
    their rets (00320890, 0030A970, 00233C10, 002370C0, 002FA210, 00313840, 00313600, 00313730, 00317230,
    00320D50, 00322200, 00329E40, 0030D8B0, 0030DA10, 00307200 / 00307240 / 003072A0, 00304140)
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-battle-state-block-field-map-pass-1
  last_pass_kind: authored
  crossref_clean: false
  reopened_count: 0
---

# The battle-state block — what lives above the forty stats records

> The qword at `02EBF190` points into the save image: a block of **0x7410 bytes** that opens with
> the magic `0x05071901`, holds the **forty party `BattleStatsRecord`s** from `+8`, and then, above
> `+0x2D48`, the things this page names — the party configuration's nine selectors, the four-entry
> battle slot map, the party leader, a special-presentation sequence, the mode ladder's words, three
> small echoes the combat formulas leave for each other, ~~the inventory's temporary snapshot~~ the item and equipment count arrays *(answered: §2.3's rows and §2.8; 2026-10-02, OPUS)*, and
> forty members' worth of gambit banks. Everything here is saved in place.

## 1. What the player sees

Who is in the party and in which order, who is the leader, whose gambits say what, which party
mode a scene has put the group in — all of it is a few bytes in one record that the save file
carries byte for byte. Load a save and the block is pointed at inside the image; nothing is
rebuilt from it except the inventory descriptors and the gambit runtime orders.

## 2. Native mechanism

### 2.1 Where the block is, and how big

`00233C10` binds the global: when `02EBF190` is null it is set to the active runtime buffer
`+0x4E68C` — payload `+0x4E48C` — and the inventory descriptors are rebased (`00233C25`–`00233C3A`);
when it is set, the magic `0x05071901` is checked (`00233C4D`). The block's **size is 0x7410**: the
reset `002370C0` clears exactly that many bytes (`002370CD`, `memset` via `00861EC0`), rewrites the
magic, fills the nine selectors at `+0x5A48` with `0xFFFF` (`00237100`–`00237116`) and zeroes the
accumulator at `+0x5AC8` / `+0x5ACC`. So the block runs from payload `+0x4E48C` to `+0x5589B` —
which places [the save map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)'s
~~inventory descriptors~~ the inventory region it calls the descriptors (`+0x53C54` = block `+0x57C8`, class 7's second region, the descriptors themselves being static at `01EEBCC0` *(corrected 2026-10-02, OPUS: descriptor row 2 names `+0x57C8` at its `+0x18`, and `0030B702`–`0030B737` zero `0x200` bytes there; FO-5)*) and the gambit banks **inside** it; that page's
23,312-byte extent was the scan's reach at the time and is corrected with this page.

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: the qword at `02EBF190`; the block's allocator (`002370C0`'s `memset`) is reached through that pointer, code that receives an interior pointer as an argument is not unless propagated.
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 The forty records

`+8 + i × 0x1C8`, `i = 0..39`: the party `BattleStatsRecord`s, every offset of
[the stats map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)
applying at `+8 + d` for record 0. The scan attributes ~~835 accesses in 130 functions~~ 683 accesses in 100 functions to that range
(~~111 offsets~~ 105 offsets *(corrected 2026-10-02, OPUS: counted in the published `battle-state-block-accesses.tsv`, displacements `0x8`–`0x4747`)*) — record-0 fields reached through the block base; record `i` accesses are reported at
the base, per the scanner's stated limit. `+4` is the flag dword (`00233C6E` sets bit 12 on the
restart path and `00233CA6` clears it otherwise; the full writer census is §2.10; `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0` ORs the **discovery bits** into it on a first acquisition — bit 0 and one of `2 / 4 / 8 / 0x10 / 0x20` for a magick by school, `0x40` for a technick, `0x80` / `0x100` for a quickening, `003009C1`–`00300B5A`; read by `00318CD0` under `BattleMenu_BuildCommandEntryList` as the Magicks / Technicks / Mist command gates, the school bits by nothing — [the encoded-id space page](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.9; the dword's other bits: 11 set by `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout` (`00311BD7`) and tested by `BattleMenu_BuildCommandEntryList` (`0031EBDA`), 12 / 13 / 14 set and cleared by `00239960` under `InitializeAreaState` (`002399F5`–`00239A77`) and by the script verbs `0050F3C0` → `0023A2C0` (bit 13) and `0050F500` → `0023A390` (bit 12, also from `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`)). They are not repeated here.

### 2.3 Above the records, offset by offset

| offset | width | what | w / r | writers (sites) | readers (sites) |
|---|---:|---|---|---|---|
| `+0x2E5D` | 1 | ~~read by `003202F0` (`00320319`) with four neighbours — one function's private fields, unread~~ *2026-09-26: stats record 26's `+5` (block + 0x2E58 = record 26; `FO-5`)* | 0 / 1 |  | `003202F0` (`00320319`) |
| `+0x2EA8` | 2 | *not named by any page* *2026-09-26: stats record 26's `+0x50` (block + 0x2E58 = record 26; `FO-5`)* | 0 / 1 |  | `003202F0` (`0032034B`) |
| `+0x2EAA` | 2 | *not named by any page* *2026-09-26: stats record 26's `+0x52` (block + 0x2E58 = record 26; `FO-5`)* | 0 / 1 |  | `003202F0` (`0032035E`) |
| `+0x2EC1` | 1 | *not named by any page* *2026-09-26: stats record 26's `+0x69` (block + 0x2E58 = record 26; `FO-5`)* | 0 / 1 |  | `003202F0` (`00320364`) |
| `+0x2ED1` | 1 | *not named by any page* *2026-09-26: stats record 26's `+0x79` (block + 0x2E58 = record 26; `FO-5`)* | 0 / 1 |  | `003202F0` (`0032036A`) |
| `+0x4748` | 2 | ~~inventory temporary-state snapshot, first half~~ **the item owned-count array** (class 5, 64 words, §2.8) — snapshotted by `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` | 0 / 1 |  | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FC67`) |
| `+0x47C8` | 2 | ~~inventory temporary-state snapshot, second half~~ **the equipment owned-count array** (class 6, 420 words, §2.8) | 0 / 1 |  | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FCC7`) |
| `+0x4F84` | 2 | inventory backup A — written by the snapshot (`0030FC6F`), read back by `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0` (`0030FAE7`) | 1 / 1 | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FC6F`) | `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0` (`0030FAE7`) |
| `+0x5004` | 2 | inventory backup B — the same pair (`0030FCCF` / `0030FB37`) | 1 / 1 | `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` (`0030FCCF`) | `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0` (`0030FB37`) |
| `+0x59C8` | 1 | **the bazaar goods' flag bytes, 128 of them** (bit 0 unlocked once, bit 1 available now, bit 2 read by the menu record only; [the bazaar page](../../12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md) §2.2) — masked with `0xF8` by the rebaser on bind and rebind | 2 / 2 | `BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState` `0030B180` (`0030B203`); `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` `0030B270` (`0030B461`) | `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` `0030B270` (`0030B345` +1); `0031C5D0` (`0031DA69` +2) |
| `+0x5A48` | 1 | **the nine party-configuration selectors**, u16 each, `0xFFFF` = empty: `[0..3]` the active party, `[4..8]` the available / reserve indices (`PartyConfiguration_AddSelector00To06ToAvailableIndex4To8` `003172E0`); reset to `0xFFFF` by the block reset `002370C0` (`00237100`–`00237116`); `00320890(sel)` returns the index holding a selector byte, `0030A970` returns a 4-bit mask of the filled active slots | 1 / 18 | `PartyConfiguration_SetDefinitionSelectorForIndex` `00329080` (`00329122` +1) | `0030A970` (`0030A994`); `PartyConfiguration_AddSelector07To25ToAvailablePrimaryIndex` `003170E0` (`00317100`); +16 more |
| `+0x5A4A` | 2 | selector `[1]` | 0 / 1 |  | `0030A970` (`0030A9A7`) |
| `+0x5A4C` | 2 | selector `[2]` | 0 / 1 |  | `0030A970` (`0030A9B8`) |
| `+0x5A4E` | 2 | selector `[3]` | 0 / 1 |  | `0030A970` (`0030A9C7`) |
| `+0x5A58` | 2 | ~~**the battle slot map**: four 18-byte entries at `+0x5A5A` … (word `+0` = the mapped definition selector)~~ **Corrected 2026-09-14 (FABLE, `OPUS-NOTICE-FABLE-SLOTMAP-CLASS0`): selector `[8]`, the last word of the nine party-configuration selectors at `+0x5A48`, not a slot-map field.** Every whole-table copy moves the 16 bytes at `+0x5A48` together with the word at `+0x5A58` (`00329DE3`/`00329DEA`; `00326714` with `003266F8`; and the nine readers in this row). The four battle mapping tables that follow start at `+0x5A5A`, `+0x5A6C`, `+0x5A7E` and `+0x5A90`. Each is a whole nine-u16 selector table in the same format as `+0x5A48`, and they are classes 1–4 of `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (class 0 is `+0x5A48` itself, `0031BAAA`). `BattleSlotMap_InitializeMappingClasses` `00329CC0` fills all four as copies of `+0x5A48`. `BattleGroup_RefreshFourActorDefinitions` `003266C0` rebuilds them through `rdi = block + 0x5A48`: it copies `+0x5A48` into classes 1 and 3, clears class 1's selectors `[4..8]` to `0xFFFF` (`00326728`–`00326730`), copies class 1 into classes 2 and 4, then rewrites selectors `[0..3]` of classes 1, 2 and 4 ~~per mode~~ as CONTRACT-the-five-parallel-slot-maps.md SM-5 tabulates per mode: mode 0 rewrites nothing, mode 5 only classes 1 and 2, and modes 3 and 5 first restore class 4 from a copy taken on entry *(corrected 2026-10-02, OPUS: mode arms `003269D2`, `00326991`, `003268F3`, `0032683F`, `00326783`; restores `003268FD`, `003267F3`)* (`003268BD`–`003268DC`) | 0 / 9 |  | `PartyConfiguration_AddSelector00To06ToAvailableIndex4To8` `003172E0` (`00317352`); `PartyConfiguration_SetEmptyIndexSelector` `00326110` (`00326138`); +7 more |
| `+0x5A5A` | 1 | mapping class 1, selector `[0]` (~~slot-map entry 0: mapped selector~~; a whole nine-u16 table, see `+0x5A58`) | 2 / 8 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326717` +5); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329DF6`) | `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810` (`0031B841`); `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (`0031BA8B`); +6 more |
| `+0x5A5C` | 2 | *not named by any page* | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003268BD`) |  |
| `+0x5A60` | 2 | *not named by any page* | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003269A7` +1) |  |
| `+0x5A62` | 8 | mapping class 1, selectors `[4..7]` set to `0xFFFF` (`00326728`; `[8]` at `+0x5A6A` by `00326730`) | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326728`) |  |
| `+0x5A6A` | 2 | *not named by any page* | 2 / 1 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`0032671B` +1); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329DFD`) | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326739`) |
| `+0x5A6C` | 2 | mapping class 2, selector `[0]` (~~slot-map entry 1: mapped selector~~; a whole nine-u16 table, see `+0x5A58`) | 2 / 2 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`0032673E` +5); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E04`) | `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (`0031BA71`); `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326705`) |
| `+0x5A6E` | 2 | *not named by any page* | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003268CD`) |  |
| `+0x5A72` | 2 | *not named by any page* | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003269AB` +1) |  |
| `+0x5A7C` | 2 | *not named by any page* | 2 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326742`); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E0B`) |  |
| `+0x5A7E` | 1 | mapping class 3, selector `[0]` (~~slot-map entry 2: mapped selector~~; a whole nine-u16 table, see `+0x5A58`) | 2 / 4 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326720`); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E12`) | `BattleStats_SetEquipmentSlotByMappedId` `0031A510` (`0031A554`); `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (`0031BA57`); +2 more |
| `+0x5A8E` | 2 | *not named by any page* | 2 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326724`); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E19`) |  |
| `+0x5A90` | 1 | mapping class 4, selector `[0]` (~~slot-map entry 3: mapped selector~~; a whole nine-u16 table, see `+0x5A58`) | 2 / 7 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326747` +4); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E20`) | `0031B950` (`0031B981`); `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (`0031BA3D`); +5 more |
| `+0x5A92` | 2 | *not named by any page* | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003268DC`) |  |
| `+0x5A96` | 2 | *not named by any page* | 1 / 0 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`003269B0` +1) |  |
| `+0x5AA0` | 2 | *not named by any page* | 2 / 1 | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`0032674B` +2); `BattleSlotMap_InitializeMappingClasses` `00329CC0` (`00329E27`) | `BattleGroup_RefreshFourActorDefinitions` `003266C0` (`00326700`) |
| `+0x5AA4` | 4 | **the preferred definition selector — the party leader** (~~1 byte~~ **a dword whose six writers each store a zero-extended byte or `0xFF`** — `movzx` before every `mov dword` at `00322173`, `003266A3`, `00327836`, `0032785A`, `003278A4`, `00329DC2` — so the upper three bytes are always 0 and the twelve byte readers are exact; corrected 2026-09-11, OPUS-CONTRA-FOCUSBYTE, EXP-049): `PartyFocus_SetPreferredDefinitionSelectorAndRefresh` `00327850` writes it, `PartyFocus_GetPreferredDefinitionSelector` `003271D0` reads it, `PartyFocus_SelectAndRequestDefaultActor` `00326500` and `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0` consult it; the status view's bit 11 tests a member's index against its position in the list | 6 / 10 | `003220E0` (`00322173`); `00326620` (`003266A3`); `00327810` (`00327836` +1); +3 more | `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0` (`0032620A`); `PartyFocus_SelectAndRequestDefaultActor` `00326500` (`00326542` +1); +8 more |
| `+0x5AC8` | 4 | **the focus actor's walked distance** (float part; named 2026-09-11, [the walk recipe](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.3): `PartyFocus_ProcessActorControlPresentationState` `00358F90` measures the kind-3 focus actor's movement-context position against its previous position (`003A1920`, `00358FFF`–`00359010`) and adds a positive length through `00317230` (`0035904F`–`00359052`); an accumulator fed a per-frame delta by `00317230` (carry into `+0x5ACC` when ≥ the constant at `008F8180`; whole capped at 99,999,999 = `0x5F5E0FF`); read as `int(+0x5AC8) + +0x5ACC` by `00320D50`; `00329E40(n)` sets the integer part, `00322200` and the block reset zero both | 4 / 2 | `002370C0` (`0023712E`); `00317230` (`0031726B` +2); `00322200` (`00322216`); +1 more | `00317230` (`00317243` +1); `00320D50` (`00320D57`) |
| `+0x5ACC` | 4 | integer part of that accumulator — saved inside the image (payload `+0x53F58`); `00329E40` re-seats it from the header stash `+0x7C` on the load normaliser's restore path and `00322200` zeroes it on the stash path (FU-2) | 4 / 2 | `002370C0` (`00237121`); `00317230` (`0031727C` +1); `00322200` (`00322209`); +1 more | `00317230` (`0031724F` +1); `00320D50` (`00320D5F`) |
| `+0x5AD0` | 2 | **the special-presentation flag word** (u16): bit 1 = a sequence is active (`00313600` sets it with a timer floor, `00313730` / `00313840` clear it, `003139A0(n)` toggles it), ~~bit 2 cleared by `00313840`~~ bit 0 cleared by `00313840` with bit 1 *(corrected 2026-10-02, OPUS: `0031388B and word ptr [rax + 0x5ad0], cx` with `cx = 0xFFFE`, `0031389E` with `0xFFFD`)*; captured to the transition record by `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` ([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §"It survives area transitions and saves") | 7 / 6 | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF44C`); `BattleUnit_IssueCommand` `00311CF0` (`00311D5E`); `00313600` (`00313638`); +4 more | `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3E5`); `SaveTransitionMetadata_RefreshSubsetToRecord` `002EF510` (`002EF517`); +4 more |
| `+0x5AD4` | 1 | the sequence's mode byte (`003139C0(n)` sets it, `00313840` resets it to `0x1B`; `003137E0` reads it) | 3 / 2 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`0030697F`); `00313840` (`0031387D`); `003139C0` (`003139C7`) | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`003067EC` +1); `003137E0` (`003137E7`) |
| `+0x5AD5` | 1 | **the sequence's acting member** — a definition selector: `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`00306966`) and `00313840` (`0031386A`, clears) write it; `003137F0` reads it; `00313730` hands it to `PartyFocus_SetPreferredDefinitionSelectorAndRefresh` when the sequence ends; the status view's bit 10 tests a member against `00320890(+0x5AD5)` | 2 / 7 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`00306966`); `00313840` (`0031386A`) | `00300FC0` (`0030110B`); `0030A970` (`0030A9D7`); +5 more |
| `+0x5AD8` | 4 | the sequence's timer A (float): `00313600` floors it, `00313760` / `00313840` write it, `00313820` reads it; `AiOrder_EvaluateTargetSelector` `00301AD0` reads it (`00303543`) | 3 / 3 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`003069A8`); `00313760` (`0031378A` +1); `00313840` (`003138AE`) | `AiOrder_EvaluateTargetSelector` `00301AD0` (`00303543`); `00313600` (`00313616`); +1 more |
| `+0x5ADC` | 4 | the sequence's timer B (float): `00313830` reads it | 2 / 2 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`003069B7`); `00313840` (`003138BB`) | `00313760` (`00313784`); `00313830` (`00313837`) |
| `+0x5AE0` | 4 | **the event-party state word** of the mode ladder (`00303D90` sets flag bit 1 with side effects, `00303F00` / `00304440` / `00304680` drive it; captured to the transition record) | 9 / 11 | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF424`); `00303D90` (`00303DC6` +1); `00303F00` (`00303FDD` +2); +6 more | `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3D3`); `00303D90` (`00303E03` +2); +9 more |
| `+0x5AE4` | 4 | **the chocobo ride time** — `180.0f` on mount (`00303DD4`), counted down by channel 1, held by console command 229 ([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2c) | 4 / 2 | `00303D90` (`00303DD4`); `00304440` (`00304468` +1); `00304680` (`00304734`); +1 more | `00304060` (`003040CE`); `00304660` (`00304667`) |
| `+0x5AE8` | 4 | **the chocobo turbo time** — `10.0` per charge (`00303FB6`), counted down by channel 2 (the same page §2c) | 3 / 2 | `00303F00` (`00303FB6`); `00304440` (`0030449E`); `00304680` (`00304741`) | `00304060` (`003040F3`); `00304670` (`00304677`) |
| `+0x5AEC` | 4 | the last `btlAtelSetChocoboTurboMode` argument, written only (`00303E37`, `00303F59`, `00304546`) | 4 / 0 | `00303D90` (`00303E37`); `00303F00` (`00303F59`); `00304440` (`00304546`); +1 more |  |
| `+0x5B00` | 4 | **result echo A = the walked distance modulo 1000 at the walk recipe's last use** (recipe 60, slot 146 `0038EBE0` writes result `+0x13C`; [the walk recipe](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.3) — `BattleFormula_ApplyResultMetadata` `00385BA0` copies result `+0x13C` here when it is not `-1` (`00385BEA`); `0038EBE0` subtracts it inside a per-mille computation (`0038EC70`); zeroed by `00233C10` on the restart path | 2 / 1 | `00233C10` (`00233C9E`); `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385BEA` +1) | `0038EBE0` (`0038EC70`) |
| `+0x5B04` | 4 | **the mode flags** — bit 0 UI, bit 1 combat / audio, bit 2 `seteventpartymode`, bit 3 `seteventparty2mode` ([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)); the status view's bits 10 / 11 require bits 0 / 1; captured and restored with the transition record | 10 / 14 | `SaveTransitionMetadata_RestoreFromRecord` `002EF410` (`002EF435` +2); `00303D90` (`00303DB8` +1); `BattleAction_UpdateSpecialPresentationSequence` `00306760` (`00306949` +2); +7 more | `SaveTransitionMetadata_CaptureToRecord` `002EF3C0` (`002EF3F7`); `00303D90` (`00303D9B`); +12 more |
| `+0x5B08` | 4 | the previous mode, kept by the mode-transition dispatcher `0030D8B0` (`0030D8DB` read, `0030D97C` write; handler table `01EECFC0`); zeroed with `+0x5B04` by `0030DA10` | 2 / 1 | `0030D8B0` (`0030D97C`); `0030DA10` (`0030DA26`) | `0030D8B0` (`0030D8DB`) |
| `+0x5B0C` | 2 | **result echo C = the bank** — a third of every recipe-16 hit, paid out by recipe 17 ([the bank](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.4) (u16): `0038D970` adds a third of its argument and caps at 60,000 (`0038D9DE`–`0038D9F2`); `0038DA00` moves it into the target's 64-byte prefix record `+0` and zeroes it (`0038DA56`–`0038DA61`); zeroed by `00233C10` and `002FA210` | 4 / 2 | `00233C10` (`00233C83`); `002FA210` (`002FA219`); `0038D970` (`0038D9F2`); +1 more | `0038D970` (`0038D9DE`); `0038DA00` (`0038DA56`) |
| `+0x5B0E` | 1 | **result echo B = the streak count** of recipe 56 (0–17; damage `2 ^ count`, [the streak](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.2) (u8) — result `+0x138` when not `-1` (`00385BD1`); `0038EAF0` raises the double at `01CEBC10` to it (`pow` `00861F80`) into the formula scratch `02AEE004`; `00389C60` reads it beside the target's prefix record; zeroed by `00233C10` and `002FA210` | 3 / 2 | `00233C10` (`00233C91`); `002FA210` (`002FA227`); `BattleFormula_ApplyResultMetadata` `00385BA0` (`00385BD1` +1) | `00389C60` (`00389CC4`); `0038EAF0` (`0038EB03`) |
| `+0x5B10` | 2 | **gambit configuration, member 0, bank 0** — three 0x34-byte banks per party stats index from here (`GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` writes banks 0–2 of index 0 at `+0x5B10`, `+0x5B44`, `+0x5B78`; `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0`; `00235AF0` compares and copies a bank) | 3 / 5 | `00235AF0` (`00235BCC` +1); `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0` (`0032832E`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326069`) | `00235AF0` (`00235D17`); `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0` (`00327E2F` +3); +3 more |
| `+0x5B12` | 2 | bank 0 word `+2` | 1 / 4 | `00235AF0` (`00235CEC`) | `00235AF0` (`00235B39`); `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0` (`00327E6E` +1); +2 more |
| `+0x5B20` | 16 | bank 0 `+0x10` | 3 / 0 | `00235AF0` (`00235BDB`); `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0` (`00328336`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326078`) |  |
| `+0x5B30` | 16 | bank 0 `+0x20` | 3 / 0 | `00235AF0` (`00235BEA`); `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0` (`0032833F`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326087`) |  |
| `+0x5B40` | 2 | bank 0 `+0x30` | 3 / 4 | `00235AF0` (`00235BF8` +2); `GambitConfig_CommitBankAndRebuildRuntimeOrders` `003282D0` (`00328347`); `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326095`) | `00235AF0` (`00235CF5` +1); `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0` (`00327E51` +5); +2 more |
| `+0x5B42` | 1 | bank 0 `+0x32`: the available entry count (`GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0`) | 2 / 2 | `00235AF0` (`00235D0F`); `GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0` (`00327A01`) | `00235AF0` (`00235B29`); `GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0` (`003279E7`) |
| `+0x5B44` | 16 | bank 1 of index 0 | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260A3`) |  |
| `+0x5B54` | 16 | bank 1 `+0x10` | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260B2`) |  |
| `+0x5B64` | 16 | bank 1 `+0x20` | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260C1`) |  |
| `+0x5B74` | 4 | bank 1 `+0x30` | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260CF`) |  |
| `+0x5B78` | 16 | bank 2 of index 0 | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260DD`) |  |
| `+0x5B88` | 16 | bank 2 `+0x10` | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260EC`) |  |
| `+0x5B98` | 16 | bank 2 `+0x20` | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`003260FB`) |  |
| `+0x5BA8` | 4 | bank 2 `+0x30` | 1 / 0 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326109`) |  |
| `+0x7370` | 4 | **the selected-bank index per member**, `int[40]` to `+0x740F` — the block's last field: `GambitConfig_CopySelectedBankForStatsIndex` `00327C40` reads `bank = +0x5B10 + (3 × i + sel[i]) × 0x34` (`00327C63`–`00327C7C`), so the banks are `[40][3] × 0x34` from `+0x5B10` to `+0x736F`; written by the initialiser (`00326039`), read by sixteen gambit functions | 1 / 16 | `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030` (`00326039`) | `GambitConfig_CopySelectedBankForStatsIndex` `00327C40` (`00327C63`); `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0` (`00327E27` +1); +14 more |

**What the region is.** Reading the table top down: ~~the inventory's temporary snapshot~~ the item and equipment count arrays *(answered: §2.8; 2026-10-02, OPUS)* and backup
(`+0x4748`–`+0x5005`, Items), a BattleIdClassD flag (`+0x59C8`), then the party's own state — the
nine selectors (`+0x5A48`), the four mapping-class tables derived from them (`+0x5A5A`–`+0x5AA1`), the leader (`+0x5AA4`), a play accumulator
(`+0x5AC8`), the special-presentation sequence (`+0x5AD0`–`+0x5ADF`), the mode ladder's words
(`+0x5AE0`–`+0x5AEF`, `+0x5B04`, `+0x5B08`), three combat-formula echoes (`+0x5B00`, `+0x5B0C`,
`+0x5B0E`) and the gambit banks (`+0x5B10`–~~`+0x7373`~~`+0x736F` *(corrected 2026-10-02, OPUS: `0x5B10 + 120 × 0x34 = 0x7370`, the selection array's start; `00327C63`–`00327C7C`)*).

### 2.4 The two designations the status view keys on (`FJ-2`)

[The status view](../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md) §2.2 sets
bit 10 when `+0x5B04` bit 0 is on and `00320890(+0x5AD5)` equals the member's index, and bit 11
when `+0x5B04` bit 1 is on and the member's index equals the position of `+0x5AA4` in the selector
list. With the names above: **bit 10 = "this member is the one acting in the special-presentation
sequence, in the UI mode"; bit 11 = "this member is the party leader, in the combat / audio mode"**.
`00320890(sel)` is the index of `sel` among the nine selectors (`003208A3`–`003208BC`, `-1` when
absent); `0030A970(out)` returns the 4-bit mask of filled active slots and, through the same lookup,
the sequence actor's index (`0030A994`–`0030A9E4`).

### 2.5 The special-presentation sequence

`BattleAction_UpdateSpecialPresentationSequence` (`00306760`, 911 B) drives `+0x5AD0`–`+0x5ADF`:
`00313600` starts it (`+0x5AD0 |= 2` after flooring timer A and asking `003EBC50` / `003EBD00`),
`00313840` (UI) ends it (`+0x5B04` bit 0 cleared with `0035C620`, `+0x5AD5 = 0`, `+0x5AD4 = 0x1B`,
`+0x5AD0` ~~bits 1–2~~ bits 0 and 1 *(corrected 2026-10-02, OPUS: `0031388B`, `0031389E`)* cleared, both timers zeroed), `00313730` ends it and makes the actor the
preferred selector. The field frame's steps 15 and 20 read `+0x5AD0` bit 1 as a timer-copy gate and `+0x5AD5`
through `003137F0` ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
§2.3). **The sequence is the Esper summon** (FO-1 answered 2026-09-12 on [the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2c): `+0x5AD4` is the Esper's party-table row (`0x1B` = Belias), `+0x5AD5` the summoner's selector, the two timers the Esper row's `+0x32` (250 on all thirteen), and the same function's mode-2 block is the chocobo mount. `003EBC50` / `003EBD00` start a countdown channel.

### 2.6 The three echoes

`BattleFormula_ApplyResultMetadata` (`00385BA0`) copies a resolved result's `+0x138` (byte) and
`+0x13C` (dword) into `+0x5B0E` / `+0x5B00` when they are not `-1`; `0038EAF0` turns `+0x5B0E`
into `pow(constant, value)` in the formula scratch `02AEE004`, `0038EBE0` subtracts `+0x5B00` in a
per-mille step, and `+0x5B0C` is a running sum (thirds, capped at 60,000) that `0038DA00` banks
into the target's 64-byte prefix record and clears. Which results set `+0x138` / `+0x13C`, and what
the sum is, are `FO-2`.

### 2.7 How the focus actor is chosen — `PartyFocus_SelectAndRequestDefaultActor` (`00326500`), read 2026-09-11

`PartyFocus_SetPreferredDefinitionSelectorAndRefresh` (`00327850`) is a dword store of the selector
into `+0x5AA4` and a tail-jump into this 274-byte function (`0032785A`–`00327860`), which every
leader change and every handle re-key ends in. In order:

1. `00311E20()` (a bracket around a global at `022BE974`, unread), `00326620()` (unread), then the
   runtime mode from `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`): **modes 0 and 1
   take `+0x5AA4`**, mode 2 takes the constant `0x1A`, mode 3 the low byte of `00377C70()`, any
   other `0xFF` (`0032651B`–`00326542`).
2. `BattleUnit_FindByCombatantId` (`0031B770`) on that selector; a unit **with a stats record**
   (`+0x698 != 0`, `00326563`) is the focus: its `+0x08` handle is taken (`003265FB`), and in
   mode 1 only `00317400(unit)` runs first (`003265FE`–`0032660B`).
3. Otherwise the **four mapping-class tables** in order — selector `[0]` of each, the words at `+0x5A5A`, `+0x5A6C`, `+0x5A7E`,
   `+0x5A90` (`00326573`–`003265C3`; each first through `BattleEncodedId_IsValidForClass` `00322C50` `(0x17, i)`
   and `BattleUnit_FindByDefinitionSelector` `002367A0`) — the first with a stats record wins.
4. Otherwise `PartyRoster_GetActorBySlot(0)` (`00263750`), encoded (`003589B0`), or **0** when
   there is no actor at all (`003265C5`–`003265D9`).
5. `00311E20()` again and the tail-call `PartyFocus_RequestPackedActorHandle` (`003594B0`): the
   handle into `022C7FE4` and a request byte `022C7FF8 = 1` — consumed by `PartyFocus_CommitPendingPackedActorHandle` `00358BC0` ([the party page](../active-party-reserve-and-the-moment-the-leader-changes.md) §4).

`00327150` is the other half: it turns `+0x5AA4` into the leader's **unit** by walking the pool for
the unit whose stats record is this block's record for that selector (`block + 8 + sel × 0x1C8`,
`0032715D`–`003271A3`; `0` above `0x27` or when none). The installer's re-key delegate
(`003220E0`, [the definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md))
compares that unit's handle with the handle it is about to retire and, on a match, writes the
re-keyed unit's stats byte `+4` into `+0x5AA4` and runs the selection above (`00322129`–`00322179`)
— so the focus follows a leader whose definition is re-installed.

ASTRA's [EXP-049](../../_experiments/EXP-049-handle-renewal-focus.md) and
[EXP-050](../../_experiments/EXP-050-focus-fallback-selection.md) executed the re-key delegate and
this function in isolation over controlled dependencies — the mode table, the with-stats gate, the
four-slot fallback, the actor-slot-0 default and the call order above, eleven and seven cases —
which is isolated execution with the callees controlled, not a live focus change; the static
reading is this section's tier. What `00311E20`, `00326620`, `00317400` and the request's consumer
do is `FO-6`.

### 2.8 The inventory region, laid out by the class descriptors (extension 2026-09-11, FABLE)

The fifteen inventory class descriptors at `01EEBCC0` ([the encoded-id space page](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.2–2.3)
carry, per class, an offset into this block and a length in words, and the rebaser `0030B6A0`
adds the block base to each at load. The regions abut:

| block offset | words | class | content |
|---|---|---|---|
| `+0x4748` | 64 | 5 items | one owned count per item id |
| `+0x47C8` | 420 | 6 equipment | one owned count per equipment id (`0x1000`–`0x11A3`) |
| `+0x4B10` | 512 | 7 loot | one owned count per loot id |
| `+0x4F10` | 6 | 8 magicks | one learned bit per magick (81) |
| `+0x4F1C` | 2 | 9 technicks | one learned bit per technick (24) |
| `+0x4F20` | 16 | 11 gambit conditions | one bit per condition (256) |
| `+0x4F40` | 32 | 13 key items | one owned bit per key item (512) |
| `+0x4F80` | 2 | 17 quickenings | one bit per quickening (32) |

Class 5 also names `+0x57C0` and class 7 `+0x57C8` as second regions, and the rebaser zeroes
`+0x57C8`–`+0x59C7` and masks `+0x59C8`–`+0x5A47` with `0xF8` (`0030B702`–`0030B75B`). The
snapshot / restore pair at `+0x4748` / `+0x47C8` / `+0x4F84` in §2.3 walks these regions by the
descriptors' counts (`0030FC90`, `0030FCE9`, `0030FAAD`–`0030FB4F`), which is why the rows above
had them as "inventory temporary-state snapshot": they are the item and equipment count arrays,
snapshotted and restored.
### 2.9 The compatibility copy — only the stats records travel, so each member's selected bank is folded into them (2026-09-13, FABLE review of ASTRA's `00234ED0`)

The block is saved whole at payload `+0x4E48C`. **A second, partial copy** — the block's first
`0x6000` bytes — is written to buffer `+0x2200` (payload `+0x2000`), the location an older build kept it
at ([save payload map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)).
That window holds the forty stats records (`+8`–`+0x4747`) but **ends inside the gambit banks**:
`0x5B10 + 8 × 0x9C = 0x5FF0`, so members 0–7 have their three banks in it, member 8 only the first 16 bytes of bank 0, and the
selected-bank indices at `+0x7370` are outside it altogether. Each stats record, though, carries its own
`GambitConfig` at `+0x88` (twelve `(condition, action)` word pairs, mask `+0x30`, count `+0x32` — the
same `0x34`-byte layout as one bank; [stats record map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)).
The two functions below move the selected bank through that slot. ASTRA derived both
([spawn placement §28](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)); this is an independent
re-read of the same bytes, with the four points §28 does not state marked **new**.

**Export — `00234ED0`, a 489-byte leaf with no calls.** For `i = 0..39`: `sel = (i32) B[+0x7370 + 4i]`,
then `0x34` bytes from `B + 0x5B10 + (3i + sel) × 0x34` to `B + 0x90 + i × 0x1C8` — the record's
`+0x88`. Eight passes of five unrolled records (`r9` from `0x7374` by `0x14` to `0x7414`, `r10` by 15, the
destination by `0x8E8`), the global reloaded per record. **No clamp on `sel`**: a value outside 0–2
reads another member's bank.

**Writers.** `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40` calls it unconditionally
(`00229B71`), then copies `0xC0 × 0x80` bytes from the active buffer `+0x4E68C` to `+0x2200`.
`SaveTransition_PrepareRuntimeImageForCapture` `005844A0` does the same (`00584510`, copy from
`00584515`) **only when `byte [active + 0x4E68C] != 0` (`0058450B`)** — **new:** that byte is the
block's `+0`, the low byte of the magic `0x05071901`, so the condition means *the block has been
initialised*; an unbound block gets neither the export nor the copy.

**Import — `00235AF0`.** It compares the copy with the live block at `+0`, `+4`, byte `+0x5B42` and
word `+0x5B12` (`00235B19`–`00235B48`) and **does nothing when all four agree**. Otherwise
`002EF4A0` copies the `0x6000` bytes back — between fixed addresses, `02166480` → `021B290C`, which are the static active buffer's `+0x2200` → `+0x4E68C`, so the copy lands on the block `02EBF190` names only while that pointer is bound to the active buffer (the binder `00233C10` sets exactly that) — and then, for each `i` (`r14` to `0x28`):

| step | instructions | effect |
|---|---|---|
| deselect | `00235BAF` | `B[+0x7370 + 4i] = 0` |
| bank 0 | `00235BC4`–`00235BF8` | `0x34` bytes from the record's `+0x88` (`B + 0x90 + i × 0x1C8`) — the exported selection returns as bank 0 |
| banks 1 and 2 | `00235C00`–`00235D44` (`rbp` = 2) | **new: both receive the same preset.** The source row is computed from `i` alone: party-definition row `i` of `02EBF130`, its u16 `+0x14` validated as a class-`0xA` id (`BattleEncodedId_IsValidForClass` `00322C50`), then row `id − 0x5000` of `02EBF0E0`; up to twelve pairs from its `+0` / `+0x20` word arrays, stopping at the first `0xFFFF` in either, each setting its bit in `+0x30`; the rest of the twelve slots become `0xFFFFFFFF` with their bits cleared. ~~**new: if the id is invalid or either table does not resolve, the row pointer is 0, the pair count is 0 (`neg` / `sbb` / `and 0xC`, `00235CB0`–`00235CB9`) and banks 1 and 2 are empty**~~ **Narrowed 2026-09-13 (ASTRA-CONTRA-FABLE-GAMBIT-PARTY-NULL, accepted):** the two tables are not symmetric. **A missing or unresolvable party table `02EBF130`** takes `00235C1B` / `00235C28` to `00235C4C` (`edi = 0`) and `00235C4E` then reads `word [0 + 0x14]` — a null dereference, before any preset validation. Only after a readable party row does an invalid class-`0xA` id, a null preset descriptor `02EBF0E0` or an unresolved preset table reach `00235CA9` (`edx = 0`), where the pair count becomes 0 (`neg` / `sbb` / `and 0xC`, `00235CB0`–`00235CB9`). **"Empty" is not zeroed:** the twelve slots are filled with `0xFFFFFFFF` (`00235D20`) and mask bits 0–11 cleared (`00235D2E`), while mask bits 12–15 and byte `+0x33` are left as they were and `+0x32` is still copied from the exported record. Static only; whether a null party table is reachable in ordinary play is not claimed |
| count byte | `00235D07`–`00235D0F` | **new: every bank's `+0x32` comes from the exported record's `+0xC2`** (`r15 = B + i × 0x1C8`), i.e. the selected bank's count, not the preset's |

`00327CB0` (`GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`) runs the same preset walk into a
stats record's own `+0x88`, so banks 1 and 2 after an import equal what that loader would give a fresh
record, except for the count byte.

**What this settles and what it does not.** Static only. It fixes *which* gambit configuration crosses
the compatibility copy — each member's selected bank, and nothing else of the banks — and what the three
banks look like after a qualifying import. It does not show when the importer's four-field test differs
in real play, whether an ordinary current-format load ever reaches it with differing fields, or what the
player sees; those remain with the live evidence (ASTRA) and `V-12` / `L-13`.

**Observed in a running game (EXP-080, ASTRA; re-derived by FABLE from the raw spans, 2026-09-13).** A fresh process loaded the 2018-size manual save `004` (`0x4E690` bytes) to its Load-complete popup and then the field. At the popup the bound block (`021B290C`, which is the active image `02164280 + 0x4E68C`) already shows the import: its first `0x5B10` bytes equal the image's `+0x2200` copy byte for byte; **bank 0 of all forty members equals the copied record's `+0x88`**, and for members 8–39 that cannot come from the `0x6000` copy itself (their banks lie beyond it), only from `00235AF0`'s loop — 32 of 32; banks 1 and 2 carry the copied record's `+0xC2` in `+0x32`, 80 of 80; the selectors at `+0x7370` are zero; the copied range `+0x5B10`–`+0x5FFF` differs from the save's bytes there, i.e. it was overwritten after the copy. The fresh-title samples of the same process are the control: bank 0 matches 0 of 40 and `+0x32` 22 of 80. **One check does not discriminate and is not counted:** bank 1 equalled bank 2 in all forty members before the load as well. Not shown: which caller ran the import, anything about the two keep banks (all zero before and after), a same-session current-to-old reload, or what the player sees.

### 2.10 The flag dword `+4` — its writers, and the `0x40 → 0x17F` a live load shows (2026-09-13, FABLE; OPUS-REQ-FABLE-BLOCKFLAGS-0X4)

**Writers.** I scanned every listed function that references `02EBF190` rip-relatively (176 functions) for writes to
`[base + 4]`: a register-tracked pass (`blk4_writers.py`) plus an untracked pass over every base register
(`blk4_any.py`). The untracked pass is the control: it finds `00233C6E`, which the tracked pass loses across a branch.
Every untracked site whose base is not the block was checked by its load: unit `+4` in `00300FC0`, a selector context in
`AiOrder_EvaluateTargetSelector`, word writes in `0023AD8E` / `0056854B`–`005687B9`, and a record in
`SaveTransitionMetadata_CaptureToRecord`. Besides the whole-block writers (the reset's `memset` in `002370C0`, and the
import copy `002EF4A0` of §2.9), the block's `+4` has exactly these:

| bits | set | cleared | meaning |
|---|---|---|---|
| 0, and one of 1–5 | `003009F7`; `00300B5A` (`or [rcx+4], eax`, the school bit) | — | a magick acquired, by school |
| 6 (`0x40`) | `003009E7` | — | a technick acquired |
| 7 / 8 (`0x80` / `0x100`) | `003009D4` / `003009C1` | — | a quickening acquired |
| 11 (`0x800`) | `00311BD7` | **`00311C8C`** | `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout`: the same load of the global (`00311BC8`) sets it when `ebx != 0` and clears it otherwise |
| 12 (`0x1000`) | `00233C6E`, `00239A35`, `0023A39B` | **`00233CA6`**, `00239A3E`, `0023A3A3` | in the binder `00233C10`, set when `02089344` bit 0 is set (then that bit and the three echoes are cleared), **cleared otherwise**; `00239960` under `InitializeAreaState`; the script verb path `0023A390` |
| 13 (`0x2000`) | `002399FB`, `00239A56`, `0023A2CB` | `00239A04`, `0023A2D3` | `00239960`; the script verb path `0023A2C0` |
| 14 (`0x4000`) | `00239A18`, `00239A77` | `00239A21` | `00239960` |

Bits 0–8 are only ever set: nothing in the census clears a discovery bit. Bits 9, 10 and 15–31 have no writer. The
discovery-bit writers are all in `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0`, whose meanings are in
the encoded-id page §2.9 ([the encoded-id space](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)).
**Not covered:** a function that receives the block pointer as an argument without naming `02EBF190` itself.

**What EXP-080 shows, bit by bit.** `0x40` in both fresh-title samples is bit 6 alone: *technick acquired* in the
session's own block. The same `0x40` is in the `+0x2200` copy **and** the block of the two current level-1 saves
`FFXII_000` / `FFXII_001` (decoded with `safh_decode.py`). **Which writer sets it before any load is not read.**
`0x17F` in all four post-load samples is bit 0, the five school bits `0x3E`, technick `0x40` and quickening `0x100`.
**The import supplies it.** The decoded `FFXII_004` (SHA-256 `8fb99c6d…`, the EXP-080 input) holds `0x0000017F` at buffer
`+0x2204`, the `+4` of its `+0x2200` copy. The 2018 image (`0x4E690` bytes) ends before a block location exists, and §2.9's
observation already found the live block's first `0x5B10` bytes equal to that copy. The bank rebuild writes only
`+0x5B10` and above, so it does not touch `+4`.
- **Bit 12 clear after the load** is *consistent with* the binder's clear branch `00233CA6` (restart flag `02089344` bit 0
  not set). It could equally be that the imported value simply had it clear. EXP-080 does not separate the two.
- **For comparison**, the other older saves' copies hold `0x7F` (`FFXII_005`, `006`), `0x47` (`007`) and `0x40` (`008`).
  The current `FFXII_002` / `003` hold `0x17F` in both copies.

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `02EBF190` | | the block pointer (payload `+0x4E48C`) |
| `002370C0` | 121 B | the block reset — `memset(0x7410)`, magic, selectors, accumulator |
| `00233C10` | 214 B | the binder / restart path (`+4` bit 12, the three echoes zeroed) |
| `00320890` / `0030A970` | 47 / 131 B | selector index lookup / filled-slot mask |
| `003266C0` | | `BattleGroup_RefreshFourActorDefinitions` — writes the slot map |
| `00327850` / `003271D0` | 21 / 15 B | `PartyFocus_SetPreferredDefinitionSelectorAndRefresh` / `PartyFocus_GetPreferredDefinitionSelector` |
| `00326500` | 274 B | `PartyFocus_SelectAndRequestDefaultActor` — the focus selection (§2.7) |
| `00327150` / `003594B0` | 117 / 14 B | the leader's unit from `+0x5AA4` / `PartyFocus_RequestPackedActorHandle` (§2.7) |
| `00313600` / `00313840` / `00313730` | 69 / 134 / 38 B | sequence start / end (UI) / end-and-prefer |
| `00317230` / `00320D50` | 170 / 22 B | the accumulator's adder / reader |
| `0030D8B0` / `0030DA10` | 237 / 29 B | the mode-transition dispatcher (`+0x5B08`) / the reset |
| `00385BA0` | 250 B | `BattleFormula_ApplyResultMetadata` — the echoes' writer |
| `00326030` | 224 B | `GambitConfig_InitializeThreeBanksFromBasePairs` — the gambit banks' initialiser |

## 4. Data structures and formulas

```
block (0x7410 B, at payload +0x4E48C)
  +0x0000  u32   magic 0x05071901              +0x5AA4  u32   preferred selector (leader; low byte, upper bytes always 0)
  +0x0004  u32   flags (bits 0-8/11-14, §2.10) +0x5AC8  f32 + +0x5ACC i32  accumulator, cap 99,999,999
  +0x0008  BattleStatsRecord[40] (0x1C8)       +0x5AD0  u16   sequence flags; +0x5AD4 u8 mode; +0x5AD5 u8 actor
  +0x4748  inventory temporary snapshot        +0x5AD8  f32 timer A; +0x5ADC f32 timer B   <- corrected 2026-10-02, OPUS - the item (+0x4748) and equipment (+0x47C8) count arrays, section 2.8
  +0x57C8  inventory class descriptors         +0x5AE0..+0x5AEF  mode-ladder words   <- corrected 2026-10-02, OPUS - +0x57C8 is class 7's second region, not the descriptors, which are static at 01EEBCC0; 0030B702-0030B737 zero it
  +0x5A48  u16[9] party selectors (0xFFFF)     +0x5B00  i32 echo A; +0x5B04 u32 mode flags; +0x5B08 i32 previous mode
  +0x5A5A  u16[9] x 4 mapping classes 1-4      +0x5B0C  u16 echo C; +0x5B0E u8 echo B
                                               +0x5B10  gambit banks [40][3] x 0x34 B; +0x7370 i32[40] selected bank
```

## 5. Call chain

```
save image payload +0x4E48C  <- 00233C10 binds 02EBF190 ; 002370C0 resets (0x7410)
  party verbs / menus -> PartyConfiguration_* -> +0x5A48 selectors, +0x5AA4 leader
  BattleGroup_RefreshFourActorDefinitions 003266C0 -> +0x5A5A..+0x5AA1 mapping classes 1-4 -> BattleSlotMap_ResolveMappedBattleSlot 0031B9F0 -> stats record
  BattleAction_UpdateSpecialPresentationSequence 00306760 -> +0x5AD0..+0x5ADF -> 00329220 status view bit 10 ; world tick sub-steps 15 / 20
  mode ladder 0030D9A0 <- +0x5B04 ; 0030D8B0 -> +0x5B08 ; SaveTransitionMetadata_CaptureToRecord 002EF3C0 <- +0x5AD0 / +0x5AE0 / +0x5B04
  BattleFormula_ApplyResultMetadata 00385BA0 -> +0x5B00 / +0x5B0E -> 0038EBE0 / 0038EAF0 / 00389C60 ; 0038D970 -> +0x5B0C -> 0038DA00
  GambitConfig_InitializeThreeBanksFromBasePairs 00326030 -> +0x5B10.. ; GambitRuntime_* read
```

## 6. Modding notes

- **The party is nine u16 selectors at `+0x5A48`**: four active, five available; editing a save's
  party is editing those words (and the slot map the next refresh rebuilds).
- **The leader is the low byte of the dword at `+0x5AA4`** — write all four bytes (the engine's six writers do; a byte store leaves stale high bytes that the engine never produces).
- **The block is 0x7410 bytes, saved whole** at payload `+0x4E48C` (its first `0x6000` bytes are also copied to payload `+0x2000`, where the selected bank rides in each stats record — §2.9): the mode flags, the sequence state and the echoes
  persist across a save / load exactly as left — `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`
  (`00584210`) touches `+0x5B04`; the rest is not normalised.
- **Gambits live here too**: 40 × 3 banks of 0x34 bytes from `+0x5B10`, and the bank each member
  has selected at `+0x7370 + 4i`.

## 7. What is not known

- [x] ~~**What the special-presentation sequence is on screen** — the state `00306760` drives with
  `+0x5AD4` / `+0x5AD5` and the two timers (a summon, a quickening, a scene?), and what `003EBC50` /
  `003EBD00` do at its start. **FO-1.**~~ **ANSWERED 2026-09-12 (FABLE): the Esper summon**, as §2.3 above already says;
  `003EBC50` / `003EBD00` arm a countdown channel (`02B5EBC8`, 20 bytes each). *(Ticked 2026-09-14, FABLE: the register's `FO-1` verdict answers this box; the page box had been left open.)*
- [x] ~~**Which results carry `+0x138` / `+0x13C`**, what `0038EBE0`'s per-mille step and `0038EAF0`'s
  power compute, and what the `+0x5B0C` sum banked into the prefix record is.~~ **FO-2 ANSWERED
  2026-09-11** — [the count, walk and bank recipes](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md): recipe 56's
  streak (`+0x138` = the count, `2 ^ count` damage), recipe 60's walk (`+0x13C` = walked distance
  mod 1000; the difference since last use × 10 / 3 / 2 / 1), recipes 16 / 17's bank (`+0x5B0C`).
- [x] ~~**What the accumulator at `+0x5AC8` / `+0x5ACC` counts**~~ **FO-3 ANSWERED 2026-09-11** — the
  focus actor's walked distance, fed every presentation frame by `00358F90` (row above); what
  `00329E40` sets it from is `FU-2`.
- [x] **The gambit bank layout** (0x34 B: `+2` word, `+0x32` count) beyond what the gambit page names. **FO-4.**
  **ANSWERED 2026-09-15 (FABLE), static.**
  - **A bank is byte-for-byte the party stats record's gambit block `+0x88`–`+0xBB`**
    ([the gambit page](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) §4):
    - `+0x00`–`+0x2F`: twelve `{u16 condition, u16 action}` pairs (`0xFFFF` = empty), so the `+2` word is slot 0's
      action;
    - `+0x30`: the `u16` enabled mask (record `+0xB8`);
    - `+0x32`: the **`u8`** count (record `+0xBA`, written `mov byte` at `00327D84` / `00328CF5`); `+0x33` is not
      touched by these paths.
  - **The "base pairs" are that block.** `GambitConfig_InitializeThreeBanksFromBasePairs(block, member)` (`00326030`):
    - zeroes the member's selected-bank index `+0x7370 + 4 × member`;
    - takes the record at `block + 8 + member × 0x1C8` (bounded `member ≤ 0x27`);
    - copies its `+0x88` / `+0x98` / `+0xA8` blocks (16 B each) and its `+0xB8` dword into bank 0, 1 and 2 at
      `+0x5B10 + member × 0x9C` (`00326057`–`00326109`).
  - **When it runs, it seeds all three banks from whatever preset is loaded.**
    - `BattleStats_InitializeDefinitionRecord` calls it at `0023AF03`, right after loading the character's default
      preset (`0023AEEE`–`0023AEF5`).
    - `00328BD0` calls it at `00328D04`; that is the path the script verb `resetJobs` reaches.
- [x] ~~**The three unread calls around the focus selection** — what `00311E20` brackets, what
  `00326620` and mode 1's `00317400(unit)` do, and what `00377C70` returns in mode 3 (§2.7).~~
  **FO-6 ANSWERED 2026-09-12 (FABLE) — all four read.**
  - `00311E20()` (93 B): when the global `022BE974` is **zero**, it takes the focus actor's roster slot
    (`003272F0`: the current packed focus handle resolved through the registry, then its slot),
    the actor (`PartyRoster_GetActorBySlot`), and — if `00265970(actor)` yields its transform —
    tail-jumps to **`0033CA00`**, which stores the actor at `022C7D18` and copies the 64-byte
    transform to `022C7D20` (`0033CA3E`–`0033CA71`): a **focus-actor transform snapshot**, taken
    before and after the selection. The `Actor_GetWorldPosition` into locals at `00311E65` is
    dead — the frame is popped before the jump. When `022BE974` is non-zero the bracket does nothing.
  - `00326620()` (148 B): if the focus selector `+0x5AA4` is not one of the four slot-map words
    `+0x5A5A`… (`00326640`–`00326652`) **and** the runtime mode is 0, it builds the filtered
    four-slot unit buffer (`BattleUnit_BuildFilteredFourSlotUnitBuffer(buf, 3)`), takes the first
    unit's stats byte `+4` (`0xFF` when none) into `+0x5AA4` and re-runs
    `PartyFocus_SelectAndRequestDefaultActor` — **the focus is re-seated when its combatant has
    left the party's four slots.**
  - `00317400(unit)` (119 B, mode 1 only): finds the two units named by `003137E0()` / `003137F0()`,
    picks the one that is **not** `unit`, reads that unit's definition word **`+0x7A`** and, when
    positive, divides it by 10; then `0026DAC0(unit's actor, value)` — which stores the float at
    the render record's `+0x148` and mirrors it to the `+0x138` link's `+8`. An authored tenths
    value of the *other* unit applied to this unit's render record; what `+0x7A` is authored as is
    the residue.
  - `00377C70()` (68 B): the current-or-pending field id (`WorldTransition_GetActiveOrPendingFieldId`)
    indexed into the 3-byte field-record table `[02ADD100]` (count at `+4`, records from `+8`),
    returning **bits 4–6 of the record's third byte** (`00377C91`–`00377C9C`; 0 when the table is
    absent or the id out of range) — so in mode 3 the focus selector is a 3-bit field property,
    the same third byte `C-11` decomposes.
  Narrowed 2026-09-11: the request's consumer is `PartyFocus_CommitPendingPackedActorHandle`
  (`00358BC0`; `022C7FE0` current, `022C7FE4` requested, `022C7FF8` kind) —
  [the party page](../active-party-reserve-and-the-moment-the-leader-changes.md) §4.
- [x] **UQ-127.** **The 0x2D48–0x4747 and 0x5006–0x59C7 ranges** the scan reaches only at five and one
  offsets — indexed or pointer-passed regions the scanner cannot see. **FO-5.**
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): every byte of both ranges is placed.** Control: [`fo5_block_ranges.py`](../../_index/candidates/fo5-block-ranges/fo5_block_ranges.py) (5 checks, FAILS 0). First
  placed by a delegated read-only pass; re-checked.
  - **`+0x2D48`–`+0x4747` is stats records 25 (from its `+0xB8`) to 39** (§2.2: forty `0x1C8`-byte records from
    `+8`). The five §2.3 rows inside it are record 26's `+5`, `+0x50`, `+0x52`, `+0x69` and `+0x79`: `00320230` forms
    block `+ 0x2E58` = record 26 and tail-jumps into `003202F0`, whose reads are record-relative.
  - **`+0x5004`–`+0x534B` is inventory backup B**, one word per equipment id (`0x1A4`), written by the snapshot and
    read by the restore.
  - **`+0x534C`–`+0x57BF` is the unused remainder of the backup mirror.** The restore clears `0x83C` bytes from
    `+0x4F84`. That is region A's whole size, and both used backups sit at their source `+ 0x83C`. Only items and
    equipment are ever snapshotted, so the other classes' mirror slots are only cleared.
  - **`+0x57C0`** is the items' ever-owned bitset and **`+0x57C8`–`+0x59C7`** the loot sold tally, per the class
    descriptors (§2.8; [the encoded-id page](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)).

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The block is 0x7410 bytes at payload `+0x4E48C` | `002370CD` (`memset` size), `00233C2A`–`00233C33` (bind), `00233C4D` (magic) | 1 | PROVEN |
| The nine selectors and the lookups | `00237100`–`00237116` (fill), `003208A3`–`003208BC`, `0030A994`–`0030A9E4` | 1 | PROVEN |
| The four mapping-class tables (classes 1–4) | `00326714`–`0032674B`, `003268BD`–`003268EC`; `0031BA3D`–`0031BA8B` | 1 | PROVEN |
| The leader byte | `00327850` / `003271D0` bodies (21 / 15 B) | 1 | PROVEN |
| The sequence fields | `00313600`, `00313840`, `00313730`, `003139A0`, `003139C0`, `003137E0`–`00313830` bodies | 1 | PROVEN |
| The echoes' writer and readers | `00385BAF`–`00385BEA`; `0038EB03`, `0038EC70`, `0038D9DE`–`0038D9F2`, `0038DA56`–`0038DA61`, `00389CC4` | 1 | PROVEN |
| The gambit banks' extent and the selection table | `00327C63`–`00327C7C` (`bank = +0x5B10 + (3i + sel[i]) × 0x34`, `i ≤ 39`); `00326039`–`00326109` (index 0's three banks) | 1 | PROVEN |
| Every row of the table | [`battle-state-block-accesses.tsv`](battle-state-block-accesses.tsv) (~~1,145 rows~~ 1,135 rows, 215 functions, 166 offsets *(corrected 2026-10-02, OPUS: counted in the file)*; 91 removed 2026-09-13, listed in [`route-contamination-removed.tsv`](route-contamination-removed.tsv)); scan control found | 1 | PROVEN, with the scanner's stated limits — **except the 31 rows at block offset `0x6A0`** (below) |

> ~~**The 31 rows filed at block offset `0x6A0` are not block accesses**~~ **Superseded 2026-09-13 (FABLE, answering
> OPUS-REQ-FABLE-STATEBLOCK-ROUTE-CONTAMINATION): the 31 were part of 91, and all 91 are removed from the TSV.**
> `Battle_ProcessActionTarget` `00307300` sets `rbx` to a stats record only inside the loop `003073F0`–`00307452`,
> which leaves by `00307452 jmp 00307B91`. The label `00307457` is reached only from `003073E0 je`, where `rbx` is
> still the target **unit** (`0030733A mov rbx, r8`). `hop_scan.py` walks in address order, so it carried the stats
> record across that label. Everything the unit path touches was then filed at `block + 8 + disp`: the function's
> own 33 reads and writes, and every callee reached from its calls at `0030760A`, `00307685`, `00307695`, `003076A8`,
> `00307727`, `00307890`, `00307A70`, `00307A82`, `00307B04`, `00307B26` and `00307B78`, one hop further through
> `003216E0`, `00312170`, `0030B9B0`, `00311F70` and `002F91A0`.
>
> **How the set was measured, not guessed.** `hop_scan.py` now takes `--cut FN:ADDR`, which drops tracked registers at
> a label that has been read. The same seeds were re-run with and without `--cut 00307300:00307457`. The cut run
> removes 96 rows of the current scanner generation (5 of those rows were never in this older TSV) and **adds none**. Every propagation key it removes had all of
> its routes inside the cut path (`--routes`). **91 of the 96 are rows of this TSV.** They sit in 15 functions:
> `00307300` 33, `00311F70` 13, `00323350` 9, `0030AB40` 7, `00321B00` 5, `0030B7F0` 4, `00321850` 4,
> `003299B0` 4, `003125E0` 2, `00328480` 2, `002F91A0` 2, `002F9240` 2, `002FB6C0` 2, `003219D0` 1, `00329F70` 1. OPUS's census-overlap
> check found 42 of them, the ones `battle-unit-accesses.tsv` also records at `arg+0x0`. The other 49 have no unit-census
> twin, but they lose their route in the same cut. The removed rows are kept with their original columns in
> [`route-contamination-removed.tsv`](route-contamination-removed.tsv).
>
> **What was ever intended.** The route `arg+0x8` is real for the loop's two calls `00307419` / `00307436`
> (`BattleFormula_ResolveTargetResult` / `BattleFormula_ApplyTargetResult`, stats record in `r8`), which the cut leaves
> in place. It was never intended past the label. **Blast radius:** every removed displacement lies inside the
> declared `statsRecords` array (`+0x008`–`+0x4748`), and no row on this page cites a removed site except `00307568`,
> which is cited here as the example of the defect. No field row changes.

## 9. Related

- [`../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) — where the block sits in the image.
- [`../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) — the forty records.
- [`../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) — `+0x5B04`, `+0x5AE0`.
- [`../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`](../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md) — the two designations.
- [`../party-roster-and-control-suppression.md`](../party-roster-and-control-suppression.md) — the four-pointer roster beside this record's selectors.
- [`../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) — the gambit functions named here.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every cited access site in this map was disassembled and its displacement compared with the offset of
the row citing it, by
[`check_field_citations.py`](../../../Tools/analysis-kit/gfz-scripts/check_field_citations.py):
**179 sites across 62 rows**.

| outcome | sites |
|---|---:|
| displacement **is** the row's offset | 144 |
| resolved through an embedded sub-object base | 33 |
| indexed form, indeterminate by displacement alone | 2 |
| cites the source object of a cross-object copy | 0 |
| cites a datum rather than an instruction | 0 |

**Nothing failed to decode, and no site contradicts its row.**

**The sub-object bases, counted for the first time** (6 distinct): `+0x5A48` x11, `+0x5B10` x8, `+0x2E58` x6, `+0x5A5A` x3, `+0x5A6E` x3, `+0x5A6C` x2.

**Four of the six bases fall inside `+0x5A48`-`+0x5B10`**, a 200-byte window that accounts for 27 of the 33 base-relative citations.

**Not claimed:** this checks what the map *says* — that each citation touches the offset it is filed
under. It says nothing about fields the census never reached, and the document's own coverage limits
stand unchanged.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Rewards_Progression_Economy — SERVICE and CLIENT.**
  - The preset apply `00239960` sets gil (`GameState_SetGilClampedNonnegative`) and calls the level-rank function.
    `00306760` calls the level-rank function too.
  - `Reward_ComputeExperienceForRecipient` reads `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`).
  - The unit display builder `00329220` calls a 122-byte rewards helper.
- **PlatformOnlineAchievements — SERVICE.** The save-load normaliser `00584210` runs the 281-byte post-load pass over
  the achievement counters ([the generator contract](../../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) §6
  note), before it reseeds the MT.

- **ActorEntity — MECHANICAL (SWE2-EC7-169, 85 edges).** `00237140`, `00283270` and
  the `00263750`/`00233C10`/`00239960`/`002367A0` accessors the `00280B70` roster pump
  names reach the actor layer (`0031B810`, `003266C0`, `00301AD0` among 85 edges) —
  shared-accessor fan-in, not an actor relationship of the state block.
- **CombatAI — MECHANICAL (SWE2-EC7-169, 52 edges).** `00283270`, `00233C10`,
  `002367A0`, `00239960` and the focus pair are called from the AI layer (`00327F80`,
  `00301AD0`, `00327CB0`, `00327BE0` among 52 edges) — the same accessors, fanned in.
- **Input — MECHANICAL (SWE2-EC7-169, 2 edges).** `0035C750`/`00244F00` are called by
  `00253C70`/`00291D90` of that layer — shared-helper fan-in.
- **UI — MECHANICAL (SWE2-EC7-169, 28 edges).** `00244F00`, `00273E30` and the
  `00281ED0`/`00280B70` pump pair reach the UI layer (`00252030`, `00276D30`,
  `002778C0`, `00279E20` among 28 edges) — the screens call the same publish and
  accessor helpers.
- **Audio - CLIENT and SERVICE (8 edges).** `002E9B80` is also called by bodies filed to audio: `00332C40`; `0046CC70` reaches bodies filed to audio: `002DEE80`, `00361BF0`, `003A0E20` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT and SERVICE (34 edges).** `003008A0` is also called by bodies filed to combat formula: `003112F0`; `00239960`, `00306760` reach bodies filed to combat formula: `0023AC80`, `00320A40` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (2 edges).** `003EBD00` is also called by bodies filed to core runtime: `0032A100`; `00233C10` reaches bodies filed to core runtime: `00229ED0` - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT and SERVICE (47 edges).** `002370C0` is also called by bodies filed to items/equipment: `0023AF50`; `00233C10`, `00239960` reach bodies filed to items/equipment: `0030B6A0`, `00300BA0`, `0031A630` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (52 edges).** `002367A0`, `00263750` are also called by bodies filed to movement: `00312730`, `00326BB0`, `0034A940` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (31 edges).** `002E9B80` is also called by bodies filed to presentation: `0024E2F0` (RuntimeEligibilityAndInstanceResolution), `003A40F0`, `003A4290` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (3 edges).** `00389C60`, `0038D970`, `00584210` reach bodies filed to random selection: `00379CD0`, `00379CF0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (54 edges).** `0023A2C0`, `0023A390`, `0025A160` are also called by bodies filed to script VM / native bridge: `0050F3C0`, `0050F500`, `00356CB0` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT and SERVICE (4 edges).** `0031B810`, `003299B0` are also called by bodies filed to spawn/encounter lifecycle: `00234DA0`, `002350C0`, `00306F00`; `00229B40` reaches bodies filed to spawn/encounter lifecycle: `00233440` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (14 edges).** `00300FC0`, `0030B7F0`, `0030B9B0` are also called by bodies filed to status/periodic terminal: `0030E360`, `00310DB0`, `00301140` - shared machinery across the layer boundary, no shared ownership.

## The `003282D0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`003282D0` (`GambitConfig_CommitBankAndRebuildRuntimeOrders`, ~369 B) —
`r9 = [02EBF190]`, `movzx r8d, cl`, `cl` bound vs `0x27`
(`003282D4`/`003282E4`).

| member | role | interior |
| --- | --- | --- |
| `00328140` | rebuild body under a five-register save (`00328140`/`00328149`) | [`00328140`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


### Interior citation — frontier hub `003EBD00` (2026-09-18, SWE2-EC7)

`003EBD00` — 35 B, 9 callers: the dirty-flag setter on the `02B5EBC0` block.
`ecx` selects a 0x14-stride row; when `dword[row+4]` differs from
`dword[row+0]` it stamps `byte[row+0x10] = 1`, otherwise `byte[row+0x11] = 1`
([`003EBD17`](../../_index/ADDRESS-INDEX.md)) — changed and unchanged are
different flags, both latched.

### Interior citation — frontier hub `00265970` (2026-09-18, SWE2-EC7)

`00265970` — 37 B, 6 callers: the transform getter the block's readers guard
behind — `[rcx+0xC0]` then `[+0x138]` then `+0x30`, three null gates, at
[`0026598D`](../../_index/ADDRESS-INDEX.md). Null at any step yields 0.

## SWE2-EC7-24 update (2026-09-18) — `0035C620` singleton forward

`0035C620` (12 B) loads `rcx = 022CA408` and tail-jumps `00273E30` — the
state-block singleton handed to the shared setter *(qualified 2026-10-02, OPUS: `022CA408` is a fixed static object, the battle-menu text-width words of [five-small-bin-tables.md](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) (FABLE), not the block behind `02EBF190`; and the jump is not a bare forward - given a normal stack-probe return, a valid private frame, a writable receiver and no interference, `00273E30`'s prefix zeroes `[022CA408, 022CA428)` with four QWORD stores (`00273E30`+0x6E..+0x85) before the uncaptured rest of its 2,382 B; a stub at either address shows only the interception; ASTRA's SPEC-accepted [`mode-summon-tail`](../../_experiments/evidence/mode-summon-tail/README.md), method A)*. Interior anchor
`0035C627` (the jump).

## SWE2-EC7-25 update (2026-09-18) — `003271D0` state byte getter

`003271D0` (15 B) returns `byte[[02EBF190] + 0x5AA4]` — the deep state
byte the block's readers sample directly. Interior anchor `003271D7`
(the `movzx`).

## SWE2-EC7-38 update (2026-09-19) - `00234ED0`

`00234ED0` (489 B) is a call-free `0x34`-stride record materializer - `imul rdx, rcx, 0x34` indexed by the `02EBF190` table, `movups` 16-byte field moves into the state block. Interior anchor `00234F52` (inside the copy run).

## SWE2-EC7-83 update (2026-09-20) - `0046CBB0` gated record dispatch measured

`0046CBB0` (97 B) is the `022C6F28`-family dispatch the block callers
run: `002E9B80()` yields the index (`-1` early-out twice), `ax*0x740`
selects the record, the `+0x284` non-zero gate clears it to 0, and a
live record runs `0046CC70(rec+0x5F0, edx, r8d, 0)`.
Interior anchor `0046CC01` (the `0046CC70` call).

## SWE2-EC7-105 update (2026-09-20) - `0025A160` measured

`0025A160` (29 B) is the bounded slot
publish `00304060`, `00304140` and
`00356CB0` call: when `02098DF0` is live
and `ecx < dword[ptr + 4]` it writes
`02098DF8 = ecx` and tails `00259FE0` -
the bounds-checked current-slot store the
state-block arms share.
Interior anchor `0025A171` (the `02098DF8`
write).

`00280B70` (298 B) is the nine-record pump `00281ED0` calls on `0209AC30`: `[+0xD8]` null exits; `00283270(1)` opens the pass, then `+0xAC8`'s eight-qword list iterates - each record skips on `word[+0x60] < 0`, `byte[0] & 2`, or `byte[owner+0xFC] & 0x10`, else `00327850(byte[+0x60])` writes the preferred selector and `0035C760` tests it: `00237140`/`0035C940` run on the pass arm, `0035C750`/`003271D0` on the fail arm, and `0035C920` closes before `00244F00` runs on `[+0xD8]` and `0209C318` - the roster sweep that re-publishes the party's preferred definition per member.

Interior anchor `00280BF7` (function `00280B70`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-battle-state-block-field-map-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0035C920` | 29 B | replaces bit 4 (mask 0x10) of dword `022C83E8` with bit 0 of `ecx` (shift left by 4, XOR-AND-XOR merge), stores the dword back, then tail-jumps through the jump at `0035C920`+0x18 with `ecx` unchanged | `0035C928`, `0035C92D`, `0035C932`, `0035C938` |
| `0035C940` | 26 B | replaces bit 0 of dword `022C83E8` with bit 0 of `ecx` (XOR-AND-XOR merge), stores the dword back, then tail-jumps through the jump at `0035C940`+0x15 with `ecx` unchanged | `0035C948`, `0035C94A`, `0035C94F`, `0035C955` |
