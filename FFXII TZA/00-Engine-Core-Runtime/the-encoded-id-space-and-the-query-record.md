---
system: The encoded-id space — the fifteen inventory class descriptors behind id >> 12, and the class-normalised query record
category: 00-Engine-Core-Runtime
status: "REOPENED — SECTION-05 corrects producer semantics; historical audit retained, independent acceptance pending (the open row is OV-5)"
owner_layer: both
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `00273BA0`, `00292B70`, `003FD360`, `003FDFE0`, `00564430`, `0056C490`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "the us battle_pack.bin only: every loader-bound st2e section's row count and stride read from its header, and the name field of nineteen class tables resolved through the text banks at rows 0, 1, 2, the middle and the last, 2026-09-11"
last_reviewed: 2026-09-22
production_review: "SECTION-05 original-code controls; historical corpus/caller work not newly certified"
registry_slots:
  - "0x02EBF100"
  - "0x02EBF098"
  - "0x02EBF0F0"
  - "0x02EBF0E8"
  - "0x02EBF0C8"
  - "0x02EBF128"
  - "0x02EBF110"
  - "0x02EBF050"
  - "0x02EBF0B0"
  - "0x02EBF040"
  - "0x02EBF090"
  - "0x02EBF088"
  - "0x02EBF080"
  - "0x02EBF130"
  - "0x02EBF118"
  - "0x02EBF038"
  - "0x02EBF0D8"
  - "0x02EBF070"
  - "0x02EBF068"
  - "0x02EBF060"
  - "0x02EBF0A0"
  - "0x02EBF048"
  - "0x02EBF010"
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-encoded-id-space-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The encoded-id space — the fifteen inventory class descriptors behind `id >> 12`, and the class-normalised query record

> **An item, loot, magick, technick, gambit, key item, quickening or bazaar id is one 16-bit number
> whose top nibble is a row of a fifteen-record table at `01EEBCC0`, and that row says everything the
> engine needs about the class: which table it is (class `5 + nibble` of
> [the class registry](the-encoded-id-class-registry.md)), how many ids it has, where in the battle
> state block its owned counts or owned bits live, and which two handlers mutate and query them.**
> On top of that sits one function, `0031C5D0`, that partially fills a compatible tagged request in a 0x98-byte
> **query record** — name, description, owned count, and a per-class copy of the row — and it is
> reached by fourteen direct callers plus ninety more through two static records. Reading its
> twenty-one name-field sites, and then the tables themselves, names every class the registry could
> not: **items, equipment, loot, magicks, technicks, gambit conditions, key items, quickenings, bazaar
> goods, commands, magick schools, elements, weapon categories, augments.**

**Corpus validation, before anything else.**

| | |
|---|---|
| file examined | `ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin` — the `us` copy; the other eight language copies carry byte-identical authored tables ([the text-banks page](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) §5.2, 2026-09-11) |
| sections walked | every directory entry the loader `00236C30` binds (34 `st2e` sections, §2.5) — row count at header `+4`, stride at `+8`, rows at `+0x20` |
| names resolved | the name field of nineteen class tables, rows 0 / 1 / 2 / middle / last, through [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) (§2.5) |
| positive controls | the action table (class 20, `+0x34`) resolves to *Cure, Blindna, Vox*, the names that page validated 543 / 543; the party table (class 2, `+0x30`) to *Vaan, Ashe, Fran … Zodiark*, the rows [PUB100](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) decoded; the status table (class 26, `+0`) to *KO, Stone, Petrify … X-Zone* in the id order the status page uses |
| descriptor table | the fifteen `0x58`-byte records at `01EEBCC0` read from the shipping image (`.data`, file offset `0x1DCA2C0`); their runtime fields are zero on disk and are filled by `0030B6A0` (§2.2) |

---

## 1. What the player sees

Every list the menus draw — the Items tab with its quantities, the Loot tab, the Magicks and
Technicks lists, the gambit condition picker, the Key Items tab, the bazaar's goods, the licence
board's node names — is built by asking the same question of the same function: *"here is an id;
tell me its name, its description, and how many the party has."* The answer arrives as one record
whose assigned fields and preserved prior bytes depend on the class; it is not a uniformly refreshed value object.

## 2. Native mechanism

### 2.1 The id space: the top nibble is a descriptor row, and the class is `5 + nibble`

`FUN_00309440` (30 B) is the whole derivation: `movzx eax, cx ; shr eax, 0xC ; cmp eax, 0xE ; ja
→ −1 ; imul rcx, rax, 0x58 ; mov eax, [01EEBCF8 + rcx]`. The word at `01EEBCF8` is the `+0x38`
field of the first `0x58`-byte record of a table that begins at **`01EEBCC0`** (the base the
rebaser and the two query dispatchers use, §2.2), so the function returns **record[nibble].class**.
The fifteen records carry classes **5 through 19 in order** (§4), which is why the class registry's
class-1 arm, which calls this function and re-enters its switch, is "work out what this id is": it
maps the nibble the item-id page calls the *category* onto the registry's class number by adding
five. That closes the registry's open item on what `FUN_00309440` uses, and turns the
"correspondence, not identity" between the encoded-id class and the item-category nibble of
[the item-id page](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)
into an identity: **class = nibble + 5**, read from the same table on both sides. Nibbles `0xF`
and above derive to −1; class 19 (~~`0xE000`–`0xEFFF`~~ **`0xE000`–`0xEFFE`** — the registry's shared tail rejects `id > ecx - 1` and its arm sets `ecx = 0xEFFF`, so the last accepted id is `0xEFFE`, which is exactly the `0xFFF` this record's `+0x3C` holds; corrected 2026-09-13) is the range arm the registry describes, and
its descriptor says why — it has no table, a count of `0xFFF`, and only a mutate handler
(`InventoryEncodedGilClass0E_ApplyGilDelta`): **those ids are gil amounts**.

### 2.2 The inventory class descriptor — `0x58` bytes, fifteen of them

`InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (`0030B6A0`) walks `01EEBCC0` to
`01EEC1E8` in steps of `0x58` (`0030B6A8`, `0030B6B2`, `0030B6F9`–`0030B700`) and is the one site
that states the layout:

| offset | on disk | at runtime | from |
|---|---|---|---|
| `+0x00` | u32 offset of the class's **region A** in the battle state block | | `0030B6C5` |
| `+0x08` | 0 | `state + [+0x00]` when `+0x00` is non-zero | `0030B6C8`–`0030B6CB` |
| `+0x10` | u32 **length of region A in 16-bit words** | | the regions abut (§2.3) |
| `+0x18` | u32 offset of **region B**, or 0 | | `0030B6D5` |
| `+0x20` | 0 | `state + [+0x18]` | `0030B6DC` |
| `+0x28` | u32 offset of **region C**, or 0 | | `0030B6E6` |
| `+0x30` | 0 | `state + [+0x28]` | `0030B6ED` |
| `+0x38` | u32 **class** (5 … 19) | | `00309456` |
| `+0x3C` | u32 **id count** of the class | | `0030B6F5`; the query dispatchers' bound (`00309F08`, `0030AE78`) |
| `+0x40` | 0 | **cumulative id base**: the running sum of the counts of the records before it | `0030B6F1`–`0030B6F5` |
| `+0x48` | pointer to the class's **mutate handler**, or 0 | | the registry's named `Inventory*` functions (§4) |
| `+0x50` | pointer to the class's **query handler**, or 0 | | `00309F11`, `0030AE81` |

After the walk the function zeroes `0x200` bytes at state `+0x57C8` (eight `0x40`-byte strides,
`0030B702`–`0030B737`) and masks `0x80` bytes at `+0x59C8` with `0xF8` (`0030B739`–`0030B75B`) —
the "derived state" of its name; the save page records both.

The two dispatchers the query record uses are the same eleven instructions:
`BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`) and `…Mode1` (`0030AE30`) return −1 for
`0xFFFF`, −1 for a nibble above `0xE`, index the record by the nibble, bound `id & 0xFFF` by
`+0x3C`, and tail-call `+0x50` with `(id, mode)`, mode 0 or 1; **a class without a query handler
answers 0**. So `+0x20` and `+0x24` of the query record are the class's two query channels — for
the packed-count classes `InventoryPackedCountClass_QueryChannel`, for the bitset classes
`InventoryBitsetClass_QueryState`. Per class (FY-1, answered): packed-count mode 0 =
free = total − reserved (signed, can be negative), mode 1 = total; bitset modes 0 and 1 =
the owned bit; no handler = 0. Controls: continuation-section05 `native_controls.c`
`packed_query_mode0/1`, `packed_available_can_be_negative`, `bitset_mode0/1`. See
`_index/candidates/query-abi-meaning-check.md`.

### 2.3 The state block's inventory region, laid out by the descriptors

Region A offsets and lengths are contiguous — each region ends where the next begins — which is
the check that `+0x10` is a length in words:

| class | region A | words | what the handler pair makes it |
|---|---|---|---|
| 5 items | `+0x4748` | 64 | one count per id (`InventoryPackedCountClass_*`) |
| 6 equipment | `+0x47C8` | 420 | one count per id |
| 7 loot | `+0x4B10` | 512 | one count per id |
| 8 magicks | `+0x4F10` | 6 (96 bits) | one bit per id (`InventoryBitsetClass_*`); 81 ids |
| 9 technicks | `+0x4F1C` | 2 (32 bits) | one bit per id; 24 ids |
| 11 gambit conditions | `+0x4F20` | 16 (256 bits) | one bit per id; 256 ids |
| 13 key items | `+0x4F40` | 32 (512 bits) | one bit per id; 512 ids |
| 17 quickenings | `+0x4F80` | 2 (32 bits) | one bit per id; 32 ids |

Class 5 also carries region C `+0x57C0` and class 7 region B `+0x57C8`; classes 10, 12, 14, 15,
16, 18 and 19 have no region at all (their descriptors hold a count and, for 14 / 15 / 18 / 19,
only a mutate handler — the bundle and gil classes act on *other* classes' regions). This is the
region the state-block page had as "inventory temporary-state snapshot" at `+0x4748` / `+0x47C8`:
`InventoryEquipment_SnapshotAndClearTemporaryState` (`0030FBE0`) walks it by the descriptors'
counts (`01EEBCFC` = class 5's `+0x3C`, `01EEBD28` = class 6's `+0x10`, `0030FC90`, `0030FCE9`),
which is consistent with, and now explained by, the layout above.

### 2.4 The query record — tagged input and partial outputs (SECTION-05)

The full current specification is [from initialization to reuse](the-query-record-from-initialization-to-reuse.md)
and the [contract](CONTRACT-encoded-id-space-and-class-registry.md). Original `0031C5D0` clears
QWORD+18 (`0031C5F0`), then dispatches through `0031E598` (`0031C5F7`–`0031C61D`). WORD+6 is read by classes1,5..11,13..18,30,31;
DWORD+4 by2..4,19..29,32. Class12 immediately returns-2 without reading either lane (`0031C650`). Class1
rewrites its tag and redispatches without converting the input representation (`0031C61F`–`0031C639`). The old sixteen-versus-
sixteen fallthrough reading was false.

`0035D330` writes the DWORD form to022CA520 (`0035D346`); `0035D380` writes the WORD form to022CA480 (`0035D396`). Both
zero all0x98 bytes after negative returns (`0035D355`–`0035D36A`, `0035D3A6`–`0035D3BB`), and both return the static address either way. Success
keeps unassigned old fields; direct-fill failure clears only name+18 and may preserve a rewritten tag.
Classes4/22/23 can return0 with no further output (`0031DD9E`–`0031DDB5`). Correct DWORD class19 E000..EFFE returns-1 (jump-table slot 19 is `0031C63B`; after the validator passes, `0031C64A jne` reaches the `or eax, -1` exit).

*Retained from the pre-SECTION-05 page (FABLE, Claude Opus 5.5, 2026-09-25; re-read against the image today).* A third producer writes the static record directly: `0035E070` stores `id << 16` into `022CA524` and class 1 into `022CA520` (`0035E2A8`–`0035E2BC`), calls the filler, and formats `+0x18` (`022CA538`) with text id `0x833` (`0035E2F6`–`0035E31F`). Among the own-record callers, the battle-message slot formatter `00536410` fills a stack record (class 1, the id at `+6`), and it reads that record's `+0x18` back only on a non-negative return (`005367AF`, `cmovns`).

### Equipment +0x54 has a masked writer; class10 writes the formerly excluded tail

**The former no-writer conclusion is withdrawn.** `0031CA42` reads query+54 and `0031CA47`
XOR-writes it after masking with1: bit0 becomes equipment row+7 bit1; upper bits are preserved.
The historical consumer is the shop/licence row filler `0057DED0`. It clears bit 31 of the price dword (`0057DFB4 btr ecx, 0x1f`), then ORs in the byte shifted left by 31 (`0057DFBF movzx`, `0057DFC3 shl edx, 0x1f`, `0057DFC6 or`), so only the byte's bit 0 reaches the price. That consumer is compatible with this producer. *(FABLE, Claude Opus 5.5, 2026-09-25: this withdraws FABLE's own earlier paragraphs on this page, which said no store covers `+0x54` and that the price's bit 31 'is not a property of that row'. Their census counted `mov`-form stores and missed this read-modify-write.)* A census ignoring RMW stores
cannot establish absence.

Class10 writes empty-string pointers+08/+10, QWORD zeros+20/+28, and twelve DWORD sentinels at
+38+8*k (`0031CF5A add rbx, 0x3a`, then `0031CF60 mov dword ptr [rbx-2], -1` at stride 8), ending+90..93. Its four-byte gaps include+54..57, but its writes extend beyond+64.
Action/command/school classes also write+08. The old 'no +08 writer' and 'unwritten tail' claims are
false. Sentinel-filled full-buffer comparisons and deliberately incorrect private-image variants
are in [Section05](../_experiments/evidence/continuation-section05-encoded-query/REVIEW.md).

**The following FY-3 consumer census is retained as historical bounded evidence, not a new exhaustive
consumer proof.** Its own handoff/spill exclusions remain material; it does not establish absence of
producer writes or unmodeled downstream usage.

**Which caller reads which offset — the census (`FY-3`, 2026-09-12, FABLE).** A register-tracked
read census over every caller in the graph (the returned record pointer and its register copies
followed until overwritten; for the twelve own-record callers, the stack buffer handed in `rcx`):

| route | callers | functions reading each offset |
|---|---|---|
| row form `0035D330` | 75 | `+0x18` name **37**, `+0x38` 21, `+0x10` description 16, `+0x2C` 11, `+0x00` class 10, `+0x24` q1 10, `+0x30` 8, `+0x58` / `+0x5C` / `+0x60` 7 each, `+0x20` q0 5, `+0x21` / `+0x23` 5, `+0x3C` 4, `+0x50` 4, `+0x22` / `+0x3D` / `+0x3E` / `+0x3F` / `+0x44` / `+0x48` 3, `+0x25` / `+0x4C` 2, `+0x40` 1 |
| id form `0035D380` | 14 | `+0x18` 10, `+0x2C` 7, `+0x24` 5, `+0x20` / `+0x28` 4, `+0x38` 3, `+0x3C` / `+0x4C` 2, `+0x00` / `+0x3A` / `+0x3E` / `+0x40` / `+0x42` / `+0x54` 1 |
| own record → `0031C5D0` | 12 | `+0x18` 5, `+0x38` 4, `+0x00` 3, `+0x3C` / `+0x4C` 2, `+0x04` / `+0x20` / `+0x28` / `+0x36` / `+0x3A` / `+0x3E` / `+0x40` / `+0x42` 1 |

Three things the census settles. **The name is the record's purpose** — half of all callers read
`+0x18` and nothing else. **The equipment block is read as a block**: `+0x3C`–`+0x48` and
`+0x58`–`+0x60` (the class-6 stores) are read by the same seven menu functions — `00293310`,
`00293FE0`, `00294B50`, `00295390`, `00295900`, `002CFEE0`, `002D0100` — with `+0x4C` (the slot
group) at `00292B70`, `002CA7C0`, `0057A620`, `0057AC10` and `+0x50` (the item-row class) at
`002CA7C0`, `002CB1F0`, `002CFEE0`. **The licence bytes `+0x21`–`+0x25`** (class 25 / 32) are read
by `00275E40`, `002D02C0`, `0055BFF0`, `00559E30`, `0055F830`, `00295FE0`, `002960B0` and `00506700`.
The historical bounded census recorded no direct scalar read of `+0x08`, `+0x0C`, `+0x14`, `+0x1C`, `+0x31`–`+0x35`, `+0x37`, `+0x39`, `+0x3B`,
`+0x41`, `+0x43`, `+0x45`–`+0x47`, `+0x49`–`+0x4B`, `+0x4D`–`+0x4F`, `+0x51`–`+0x53`, `+0x55`–`+0x57`,
`+0x59`–`+0x5B`, `+0x5D`–`+0x5F` or offsets from `+0x61` on in its limited tracked routes — except `00273BA0`, which copies the whole
`0x98` bytes (reads at `+0x00`, `+0x10` … `+0x90`) and is the one reader the census cannot resolve
further. **Limits:** a record pointer handed to another function is not followed (`0027B880`, four
calls, and `0027CE70` pass it on and show no offsets), and the tracking is by register, so a read
through a saved stack copy would be missed; the tally is in `Tools/work/FABLE/bf3-scratch/qrcensus-2026-09-12.txt`
(`pub140-scratch/tools/qrcensus.py`).

### 2.5 Naming the classes from their tables

The loader `00236C30` binds each descriptor from a directory entry of the loaded blob
(`movsxd rdx, [rax + off] ; lea rcx, [desc] ; call 003845F0`, one triple per slot — the
offsets in the table are those triples, `00236C86`–`0023701E`); four are bound by helpers that
take the same directory word (`00238160` for equipment `+0x38`, `00237FC0` for actions `+0x3C`,
`003847B0` for statuses `+0x40`, `GambitTargetDefinition_BindAndBuildMenuLookup` for gambits
`+0x20`). Each section is `st2e` — `+4` row count, `+8` stride, rows at `+0x20` — and the query
filler's arm says which row word is the name. Reading that word at five rows per table through the
banks:

| class | descriptor | directory | rows × stride | name at | bank | rows 0, 1, 2 … last | **what the class is** |
|---:|---|---|---|---|---|---|---|
| 2 | `02EBF130` | `+0x44` | 40 × 128 | `+0x30` | 8 | Vaan, Ashe, Fran … Zodiark | the party definition table (PUB100) |
| 5 | `02EBF100` | `+0x4C` | 64 × 12 | `+0x08` | 0 | Potion, Hi-Potion, X-Potion … Knot of Rust | **items** (the Items tab; 64 ids, one count each) |
| 6 | `02EBF0F8` | `+0x38` | 557 × 52 | `+0x02` | 1 | Unarmed, Broadsword, Longsword … Magepower Shishak | **equipment**; the descriptor counts 420 ids (`0x1000`–`0x11A3`, the `0x11A4` the arm tests at `0031C988`), the table has 557 rows |
| 7 | `02EBF098` | `+0x84` | 512 × 10 | `+0x06` | 11 | Teleport Stone, (reserve), … Empty Bottle … | **loot** — a packed-count class, so bank 11 is the loot names, not "key items" |
| 8 | `02EBF0F0` | `+0x78` | 81 × 8 | `+0x04` | 0 | Cure, Blindna, Vox … Immobilize … Graviga | **magicks** (81; one learned bit each) |
| 9 | `02EBF0E8` | `+0x7C` | 24 × 8 | `+0x04` | 0 | First Aid, Shades of Black, Horology … Telekinesis … Gil Toss | **technicks** (24) |
| 11 | `02EBF0D8` | `+0x20` | 256 × 32 | `+0x14` | 6 | Foe: party leader's target, Foe: nearest visible, Foe: any … | **gambit target conditions** |
| 13 | `02EBF090` | `+0x88` | 64 × 10 | `+0x08` | 12 | Rabanastre, Nalbina Fortress, Bhujerba … Stilshrine of Miriam | **key items, sub-table 1** — ids `0x8000`–`0x803F`, the 64 area maps |
| 13 | `02EBF088` | `+0x8C` | 32 × 10 | `+0x08` | 12 | Rabanastre, (reserve), Nalbina Fortress … Giruvegan | **key items, sub-table 2** — ids `0x8040`–`0x805F`, 32 area names |
| 13 | `02EBF080` | `+0x90` | 416 × 10 | `+0x08` | 12 | Blue Bottle, Green Bottle, Red Bottle … | **key items, sub-table 3** — ids `0x8060`–`0x81FF`, the objects; so bank 12 is the Key Items tab, not "locations" |
| 17 | `02EBF0C8` | `+0x6C` | 32 × 8 | `+0x00` | 0 | Red Spiral, White Whorl, Pyroclasm … Evanescence … SecondJob | **quickenings** (bank 0 from `0xD0`, the range the action page found; 32 ids, one bit each) |
| 18 | `02EBF058` | `+0xE8` | 128 × 36 | `+0x00` | 9 | Antidote Set, Unassuming Surcoat, Gilt Shield … Morbid Urn | **bazaar goods** (the registry's "item class `0xD`") |
| 20 | `02EBF138` | `+0x3C` | 543 × 60 | `+0x34` | 0 | Cure, Blindna, Vox … Zeromus … | the action table |
| 21 | `02EBF128` | `+0x48` | 21 × 4 | `+0x02` | 4 | Attack, Magicks, Technicks, Items, (unused), Summon, Quickening, Foecraft, (unused), 0, 0, Dismiss, 0, Gambits, (unused ×4), Magicks & Technicks, Mist, (unused) | **the battle command list** (all 21 rows read) |
| 24 | `02EBF110` | `+0x30` | 5 × 4 | `+0x02` | 4 | White Magicks, Black Magicks, Time Magicks, Green Magicks, Arcane Magicks | **magick schools** (all 5 rows read) |
| 25 | `02EBF038` | `+0x34` | 361 × 24 | `+0x00` | 3 | Quickening ×3 … Accessories … Second Board | the licence-board nodes |
| 26 | `02EBF118` | `+0x40` | 32 × 40 | `+0x00` | 5 | KO, Stone, Petrify … Disease … X-Zone | the status table, in status-id order |
| 27 | `02EBF050` | `+0xA8` | 8 × 2 | `+0x00` | 4 | Fire, Lightning, Ice, Earth, Water, Wind, Holy, Dark | **elements** (all 8 rows read) |
| 28 | `02EBF0B0` | `+0x18` | 32 × 4 | `+0x02` | 4 | Unarmed, Sword (1H), Sword (2H), Katana, Ninja Sword, Spear, Pole, Bow, Crossbow, Gun, Axe, Hammer, Dagger, Rod, Staff, Mace, Measure, Hand-bomb, Shield, Helm, Chest, Accessory, (unused), Arrows, Bolts, Shot, Incendiaries, (reserve ×3), (unused ×2) | **equipment categories** (all 32 rows read) |
| 29 | `02EBF040` | `+0xEC` | 129 × 8 | `+0x02` | 10 | NOT USED … "Increases physical attack damage." … "Additional License Board unlocked." | **the augment table** — bank 10 holds its texts, mostly NOT USED |

Tables the filler resolves no name for, read for their headers only: class 10 `02EBF0E0` `+0x24`
40 × 64 (the gambit presets — twelve condition ids and twelve action ids per row, decoded on
[the gambit page](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) §4), class 14 `02EBF070` `+0x98` 512 × 12 and class
15 `02EBF068` `+0x9C` 256 × 12 (the bundle classes `0x9000` / `0xA000` — the reward packages and their
selectors, decoded in §2.8), class 16 `02EBF060` `+0x74` 128 × 4 (`0xB000`, no handler); and eleven slots outside the class registry: `02EBF018` `+0x0C`
102 × 8 (the battle message table), `02EBF0B8` `+0x10` 25 × 8, `02EBF0A8` `+0x14` 0 × 4, `02EBF0C0`
`+0x1C` 4 × 37, `02EBF108` `+0x28` 99 × 2, `02EBF020` `+0x70` 6 × 20, `02EBF0A0` `+0x80` 16 × 13,
`02EBF078` `+0x94` 0 × 10, `02EBF048` `+0xAC` 32 × 4, `02EBF030` `+0xF4` 50 × 208, `02EBF028` `+0xF0`
226 × 44, `02EBF010` `+0x114` 120 × 8, `02EBF008` `+0x118` 49 × 8.

**What this does and does not establish.** The *identity* column is what the names say, at five
rows each, in the `us` copy; the counts (81 magicks, 24 technicks, 8 elements, 5 schools, 32
quickenings, 129 augments) match what the game presents and are the corroboration. The reading
"key items" for class 13 rests on two facts — bank 12's first 96 entries are area names, its
remaining 416 are objects, and the class is a *bitset* class (owned or not, never a count) — and on
nothing else; a player-facing check that the Key Items tab lists maps first is not made here.

### 2.6 The modify and query API — one dispatcher each, through the descriptor's handler pointers

`Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`, 25 callers) is the one entry
that changes what the party owns: `(id, delta, absolute, channel, flags)`. It refuses `0xFFFF`,
**`0x1000`** (the *Unarmed* row — the empty weapon can never be granted), nibbles above `0xE`, and
an index at or past the class's `+0x3C` (`003008AF`–`00300929`); reads the channel's value before
through `Inventory_QueryEncodedItemStateByClass` (`00309F30`); calls the descriptor's **`+0x48`
mutate handler** with the same five arguments (`00300943`–`00300960`); and returns the value after.
Then, **only for channel 1 and only on a transition from nothing to something** (`00300968`–`0030097C`),
it sets the block's flag dword `[02EBF190] + 4` — the *discovery* of its name (§2.9).

`Inventory_QueryEncodedItemStateByClass(id, mode)` bounds the index and tail-calls the **`+0x50`
query handler** (`00309F96`–`00309FA6`); mode 4 always goes to the bitset query regardless of class
(`00309F84`–`00309F91`). The two dispatchers of §2.2 are its fixed-mode twins, and
`BattleEncodedId_DispatchQueryMode3` (`0030ADC0`) is the third. A whole-image census of the table
base `01EEBCC0` finds fifteen functions: the four handlers, these dispatchers, the rebaser, and the
readers `Equipment_CheckMatchingSecondaryPartnerSelectedOrOwned` (`003096F0`),
`Inventory_QueryEncodedItemDiscoveryBit` (`00309B60`),
`Inventory_QueryOwnedCountIncludingReservedActionItems` (`00309FB0`) and
`BattleIdClassD_RefreshPrerequisiteRuntimeFlags` (`0030B270`) — the only code that touches the
descriptors at all.

### 2.7 The packed-count word and the bitset bit — what the two handler pairs store

**Packed-count classes** (items, equipment, loot — regions A of §2.3) keep **one 16-bit word per
id**: bits 0–9 the **owned total** (capped at 99, `0x63`), bits 10–15 the **reserved count** — the
copies that are equipped or committed. `InventoryPackedCountClass_QueryChannel(id, mode)`
(`002FD8D0`): mode 0 → `total − reserved` (the free copies, `002FD942`–`002FD95F`), mode 1 → total
(`002FD92B`), mode 2 → reserved (`002FD917`), mode 3 → the byte at region B `+ index` (`002FD906`),
else 0. `InventoryPackedCountClass_MutateChannels(id, delta, absolute, channel, flags)`
(`002FD150`) writes the same fields — channel 1 sets or adds the total, clamped to `[reserved, 99]`
(`002FD2AD`–`002FD31A`); channel 0 and 2 move the reserved count (0 taking it from the free copies,
2 setting it, both clamped to the total, `002FD383`–`002FD3F1`, `002FD23C`–`002FD298`); channel 3
sets or adds the region-B byte, clamped to `[0, 99]` (`002FD1BF`–`002FD237`). When channel 1 raises
the total past its old value and the class has a **region C**, the id's bit is set there
(`002FD31E`–`002FD34B`): for items that is `+0x57C0`, the *ever-owned* bitset. Every channel-1
change calls `InventoryDerivedIndex_UpdateOnPresenceTransition(id, oldTotal, newTotal)` (§2.9), and
a relative change with `flags & 1` posts the "You obtain …" line through `0046A630(id, delta)`
(`002FD355`–`002FD369`; events `0x24` / `0x25` on [the message-table page](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)).

**Bitset classes** (magicks, technicks, gambit conditions, key items, quickenings) keep **one bit
per id** in region A, word `index >> 4`, bit `index & 0xF`. `InventoryBitsetClass_QueryState`
(`002FD970`): modes 0 and 1 → that bit (`002FDA2F`–`002FDA57`); mode 3 → bit `index` of region B,
mode 4 → of region C, byte-addressed (`002FD9F2`–`002FDA2B`, `002FD9B4`–`002FD9F1`); mode 2 → 0.
`InventoryBitsetClass_MutateState(id, delta, absolute, channel, flags)` (`002FD420`) ignores the
channel: the new value is `delta` (absolute) or `bit + delta`, a negative clears, anything above 1
saturates to 1 (`002FD4A6`–`002FD4E9`); the presence hook and the obtain line follow as above
(`002FD4ED`–`002FD509`); the return is the new bit.

So **loot's region B `+0x57C8`** is a second per-loot byte counter capped at 99 that channel 3
reads and writes and nothing else in these handlers touches; the rebaser zeroes it on load. It is
**the loot-sold tally of the bazaar**: the only two channel-3 callers in the image are
`Shop_CommitSaleItemAndGil`, which adds the quantity sold, and the bazaar purchase reset, which
writes 0 ([the bazaar page](../12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md) §2.2–2.5; FY-4 answered on the tally side).

### 2.8 The bundle classes and gil — what the mutate-only handlers do with a row

Classes 14, 15, 18 and 19 have no region: their handlers act on *other* classes through the
modify dispatcher, and only for `absolute = 0, channel = 1` (every other call returns 0):

| class | handler | row it reads | effect (`mult` = the delta argument) |
|---|---|---|---|
| **14** `0x9000` | `InventoryBundleClass09_ApplyGilAndNestedItems` (`002FD530`) | `02EBF070` row = `{u32 gil, u16 itemA, u16 countA, u16 itemB, u16 countB}` | `GameState_SetGil(gil + row.gil × mult)` clamped at 0, the "You obtain {n} gil" line when `flags & 1` (`00469E80`); then each item that is not `0xFFFF` → `003008A0(item, count × mult, 0, 1, flags)` |
| **15** `0xA000` | `InventoryBundleClass0A_ApplyNestedItems` (`002FD640`) | `02EBF068` row = six `u16` ids, two triples | `flags & 2` selects the second triple; each id that is not `0xFFFF` → `003008A0(id, mult, 0, 1, flags)` |
| **18** `0xD000` bazaar | `InventoryBundleClass0D_ApplyNestedItems` (`002FD780`) | `02EBF058` row `+4 / +6`, `+8 / +0xA`, `+0xC / +0xE` = three `(u16 item, u8 count)` pairs | each pair with a non-zero count → `003008A0(item, count × mult, 0, 1, flags)` |
| **19** `0xE000` | `InventoryEncodedGilClass0E_ApplyGilDelta` (`002FD880`) | none | `GameState_SetGil(gil + (id & 0xFFF) × mult)` clamped at 0 — **the id is the amount** |

Read against the `us` tables: **class 14 is the reward-package table** — row 3 is *300 gil,
Potion × 2, Teleport Stone × 1*; row 4 *500 gil, Headguard, Teleport Stone*; row 7 *600 gil, Rose
Corsage, Balaclava* — the shape of a treasure. **Class 15's** 256 rows are empty except rows
128–172, whose first slot holds a class-14 id (`0x9003`, `0x9004`, … in order): a package
selector wrapping the reward table, with the second triple unused in the shipped data. **Class
18's** rows carry, after the three granted pairs, a `u32` price at `+0x10` (100, 105, 250 gil for
the first three goods) and three `(u16 loot id, u16 count)` pairs from `+0x16` — *Antidote Set*
costs 100 gil and wants loot `0x205C` × 2; *Gilt Shield* 250 gil and `0x2051` × 3 plus `0x2023` × 3
— the bazaar recipe: [the bazaar page](../12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md) reads the refresh that compares each
loot's *sold* tally (channel 3) against those counts and the purchase that zeroes them (FY-5 answered). **Class 16** (`02EBF060`, `0xB000`,
128 × 4) has no handler and no name; its rows are one `u32` each — 45 rows hold 1, the rest values
from 30 to 11,160 — and **nothing consumes it**: a whole-image rip-relative census of `02EBF060`
finds only the validator (`00322EBB`), the loader (`00236E13`) and the query filler's arm
(`0031D7B0`), where the same census of `02EBF068` (class 15) also finds its consumer
`InventoryBundleClass0A_ApplyNestedItems` (`002FD662`) — the positive control. The table is bound
and validated but read by no gameplay code in the image (FY-2 answered as a negative).

### 2.9 Discovery flags and the derived index — what a first acquisition also does

**The block's flag dword.** On a channel-1 transition from 0, `003008A0` ORs into
`[02EBF190] + 4`: for a **magick** (`0x3000`) bit 0, and then the bit the magick's action row
selects — the action row's `+0x2C & 7` (0–4, the school) indexes `01EECF98` = `{2, 4, 8, 0x10, 0x20}`
(`003009F0`–`00300B5A`); for a **technick** (`0x4000`) `0x40`; for a **quickening** `0xC000`–`0xC011`
`0x80`, `0xC012`–`0xC01E` `0x100` (`0030099A`–`003009DB`). **Their one reader is `00318CD0`**, called only by
`BattleMenu_BuildCommandEntryList`: it tests `0x41` (a magick or a technick known, `00318DA5`),
bit 0 (`00318DD4`), `0x40` (`00318E46`), `0x180` (either quickening range, `00318EEE`), `0x100`
(`00318F01`) and `0x80` (`00318F74`) to decide which command entries exist — so these bits are the
Magicks, Technicks and Mist command gates. **The five school bits are set and never read**: every
function that loads the block pointer was scanned for a test of `+4` through the pointer or a
register copy (176 functions, 2026-09-11) and none tests `2` … `0x20` (FY-6 answered).

**The derived index.** `InventoryDerivedIndex_UpdateOnPresenceTransition(id, old, new)`
(`00325F40`) fires on 0 → non-zero (`InventoryDerivedIndex_AddPresentItem`, `00252E60`) and
non-zero → 0 (`…RemoveAbsentItem`, `002535D0`); it maps the id to one of **twelve category lists**
through `01EED1B0` (a `{pointer, count}` pair per nibble 0 … `0xA`, each pointing at a signed-byte
map; equipment's map is 27 bytes indexed by the row's `+9` category: weapons → list 1, shield /
helm / chest → 2, accessory → 3, ammunition → 4; items → 0, loot → 11, magicks → 9, technicks → 8,
`0x5000` → 5, `0x6000` → 6, `0x7000` → 7, key items → 10). The lists are `u16` id arrays in the
**image-backed state block** `*(020927C0)` ([the save map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)),
counts at `+0x47B8 + 4 × list`, capacities and bases in a twelve-entry table at `02092760` (zero on
disk); add appends and re-sorts through `002CD650`, remove blanks the slot with `0xFFFF` and
compacts through `InventoryDerivedIndex_CompactCategoryList` (`002534C0`). The list contents are
what the menus page through.
**The lists, read (2026-09-11).** Each list is a `u16` id array with its count at block `+0x47B8 +
4 × list` and its capacity and offset in the twelve-entry table `02092760` (`{u16, s16 capacity,
u32 offset}` per list; the offset resolves through `0020E600`). `InventoryDerivedIndex_AddPresentItem`
(`00252E60`) walks the list for the id, stops at the first `0xFFFF`, appends at the count when the
capacity allows and bumps the count (`00252EBE`–`00252F18`); `…RemoveAbsentItem` (`002535D0`) blanks
the slot with `0xFFFF` and calls `…CompactCategoryList` (`002534C0`), which pulls later entries over
every blank and rewrites the count (`00253544`–`0025359F`). `00252FA0(list)` returns a count;
`00252FF0(list)` the same, except for list 10 (key items) where it excludes ids `0x8000`–`0x803F`
(the area maps) and `0x8040`–`0x805F` (the area names) — only the objects count (`002530A0`–`002530CF`).
After every append, `002CD650` refreshes the **inventory category flags** — bits of the image block's
`+0x3244` (save payload `+0xB244`), tested by `00252D10(bit)` and set by `00252D40(bit, 1)`: a bit is
set when its source list is non-empty — **1 ← list 1 (weapons), 2 ← list 2 (shield / helm / chest),
3 ← list 4 (ammunition), 4 ← list 0 (items), 5 ← lists 8 or 9 (technicks or magicks), 6 ← list 11
(loot), 7 ← the filtered list 10 (key items other than maps and area names), 8 ← list 3
(accessories)** (`002CD654`–`002CD79F`) — and never cleared by this path: once a category has been
seen it stays unlocked. The flags are read by the menu code (`002CDE20`, `003FD360`, `00557DB0`,
`0055BFF0`, `0055E9E0`, …) and, by name, are the inventory tabs that appear when the party first
holds something of that kind. ~~**What is not found**: the code that fills the capacity table
`02092760` — no rip-relative write reaches it; `00253970`, which binds `020927C0` to the runtime
buffer `+0x8200`, does not touch it.~~
**The capacity table's writer, found 2026-09-15 (FABLE, `FY-4`).** It is `SaveRuntime_InitializeImageBackedPointerDescriptor`
(`00253240`, `list`, `reset`), and it reaches the table through the image base, not `[rip + disp]`:
`lea r12, [rip → 00120000]` then `lea rbx, [r12 + 0x1F72760]` (`0025327E`–`0025328D`), entry = `02092760 + list × 8`.
That form is why the rip-relative census found nothing; a displacement sweep for `0x1F72760` finds this site alone.
- A twelve-arm jump table (RVA table `0x0013344C`, dispatched at `002532CA`) gives each list its base inside the block, from
  `*(020927C0) + 0x38CC`. It stores the encoded pointer at entry `+4` (`RuntimePointer_EncodeImageAddress` `0020E620`)
  and the capacity at `+2`. The arrays are contiguous `u16` runs, each base the previous one plus 2 × capacity:

  | list | 0 items | 1 weapons | 2 shield / helm / chest | 3 accessories | 4 ammunition | 5 | 6 | 7 | 8 technicks | 9 magicks | 10 key items | 11 loot |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|
  | base `+0x38CC +` | `0` | `0x80` | `0x210` | `0x328` | `0x388` | `0x3C8` | `0x418` | `0x618` | `0x618` | `0x648` | `0x6EA` | `0xAEA` |
  | capacity | 64 | 200 | 140 | 48 | 32 | 40 | 256 | **0** | 24 | 81 | 512 | 512 |

  - Four capacities equal the authored table sizes: 64 items, 24 technicks, 81 magicks and 512 loot. Key items'
    512 is the sum of its three sub-tables (64 + 32 + 416).
  - List 7 (the `0x7000` class) is given capacity 0 and shares list 8's base, so it can never hold an entry.
- With `reset` non-zero it also zeroes the list's count at `+0x47B8 + 4 × list` and fills the array with `0xFFFF`
  (`002533EA`–`0025341F`).
- Its two callers each loop lists 0–11 with `reset = 1`, then clear category bits 1–8 of the `+0x3244` word and keep
  bit 0 (`and byte [+0x3244], 1`; `and byte [+0x3245], 0xFE`):
  - `SaveRuntime_InitializeHeaderAndImageBackedState` (`00253B02`–`00253B23`), called from
    `SaveRuntime_ResetActiveImageAndRebindState` (`002EF66F`);
  - `00253480`, called from `0035C584` and tail-jumped from `0030483D`.
  So the table is rebuilt at run time whenever the active image is reset, which is why it is zero on disk.
### 2.10 The consumer sweep of the unclaimed slots, and three more tables named (2026-09-11)

Every authored-data slot no page had declared was censused for its rip-relative referrers (whole
image, 2026-09-11). Besides the loader `00236C30` and the validator, the referrers are:

| slot | rows × stride (`us`) | referrers | what the readers make it |
|---|---|---|---|
| `02EBF0A0` | 16 × 13 | `BattleSpecialSequence_SelectActionByAuthoredThreshold` (`002F8D60`) | **the concurrence selection table**: row `{u8 action, u8 need1, u8 need2, u8 need3, 0xFF × 9}`; the selector walks the rows from the last to the first and returns the first whose three needs are all ≤ the caller's three counts (`002F8DB0`–`002F8E36`), or a debug override from `022BE930` when the global at `01EEBAF0` is non-negative. The rows, by bank 0: **Inferno** 3 · 0 · 0, **Cataclysm** 6 · 0 · 0, **Torrent** 2 · 2 · 0, **Windburst** 0 · 4 · 0, **Whiteout** 0 · 0 · 4, **Ark Blast** 2 · 2 · 2, **Luminescence** 3 · 3 · 3, **Black Hole** 4 · 4 · 4, then eight *Black Hole* 4 · 4 · 4 rows — the three counts are the quickening levels 1 / 2 / 3 of a Mist chain, by the shape and the names |
| `02EBF048` | 32 × 4 | `Inventory_InitializePrimaryStateFromAuthoredTable` (`0023AF50`) | **the starting inventory grant table**: after resetting the state block (`002370C0`) every row `{u16 item, u16 count}` goes through `Inventory_MutateEncodedItemPrimaryChannelMode1` (`0023AFF5`–`0023AFFF`); the `test_battle` pack ships it empty (32 × `FFFF 0000`) because the scenario rows of `02EBF030` carry their own inventories |
| `02EBF108` | 99 × 2 | `002F9A60`, `002F9B20` (← `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`) | **the per-level HP / MP growth table**, `{u8 hpGrowth, u8 mpGrowth}` by level — [the level-up page](../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md) carries the formula |
| `02EBF020` | 6 × 20 | `0032A230` (← `BattleMenu_BuildCommandEntryList`, `0031F1AD`) | **the scripted command-list presets** (FY-7 answered 2026-09-12): the header's `+0x1C` is a range table `{5; 0, 2, 4, 5, 6}` cutting the six rows into five groups; the builder passes the command entry's `+4` as the group and the kind-0 unit's type byte `+4` as the key (`0031F199`–`0031F1AD`), and the scanner returns the first row of the group whose word `+0` equals the type (`0032A2C0`–`0032A30E`). A row is `{u16 type, u16 ids[7] (0xFFFF-terminated), u32 skipMask}` — **corrected 2026-09-12 (FABLE):** the dword is a per-id bit mask the builder tests with `bt` (`0031F1DF`–`0031F1E6`), bit *i* exempting id *i* from the compare, not an "is item list" flag: group 0 — type 5 (Penelo) → action 82 *Potion*, type 0 → nothing; group 1 — type 0 → `0x5000`, type 5 → `0x5005` (mask 1) — **nibble-5 ids: the item classifier's category 8, registry class 10 (`02EBF0E0`), not items. The earlier *Potion* / *Elixir* reading assumed an item encoding the builder does not establish (it compares the ids against its running entry index, `0031EF48`–`0031EF59`, `0031F1D0`–`0031F1EC`); what the two ids select is open (retracted 2026-09-12, FABLE);** group 2 — type 0 → actions 57 *Blind*, 18 *Fire*; group 3 — type 0 → 183 *Hellfire*, 210 *Pyroclasm*; group 4 empty. Which script situations select each group is not read. |
| `02EBF030` / `02EBF028` | 50 × 208 / 226 × 44 | `00239960` (← `InitializeAreaState`) | **the SetSaveData presets** — fifty scenario rows (formation, gil, 64 items) and 226 party presets (level, gear, gambit preset, LP, MP %) applied once when the script verb `btlAtelSetNextSetSaveData` has stored a set number ([the presets page](../11-Party/the-setsavedata-presets-test-battle-scenarios.md)) |
| `02EBF010` | 120 × 8 | `0033A720` (← `BattleLocomotion_ResolveTargetSpacingAndAvoidance`, `…ResolveDefaultHeadingConstraint`) | **per-field locomotion spacing rows**: `{u16 fieldId, u8 spacing, u8 flags, 0 × 4}` — the resolver walks the rows for the active field id (`WorldTransition_GetActiveOrPendingFieldId`, [`0033A8F0`](../_index/ADDRESS-INDEX.md)–`0033A940`; interior verified 2026-09-17, SWE2-FRONTIER — the 4,006-B body's call profile is `0033CEF0`/`0033CC80`/`00339DF0`/`00335B60` ×2 + `0020E600` ×2, matching this table's description), takes byte `+2` ÷ a scale as a distance (`0033AA43`–`0033AA4E`, a constant when no row matches, `0033AA54`) and tests byte `+4` against a per-slot bit (`0033AB94`); shipped rows key fields `0x0306`, `0x0307`, `0x017B` … with spacings 15, 20 and 25 |
| `02EBF008` | 49 × 8 | `0037DDD0` (← `MainLoop_UpdateAndRenderFrame` and two peers) | a **clock-driven schedule**: the row is chosen from the application root's time fields (`001B7F20` → `01F81218`; `001B77B0` / `001B77E0` / `001FDF70` scale its `+0x18` / `+0x20` / `+0x00`) by a mode 1–3 (`00184860`), its pointer kept at `02ADED98`, and `0037DEA0` compares the row's bytes `+1` … `+4` (15 / 30 / 60 / 90 in the shipped rows) against a context's elapsed counter before calling `002EFA70` and `002EFE40(5)`; what those two do is unread, so the table stays unnamed (FY-7) |
| `02EBF0A8` / `02EBF078` | 0 × 4 / 0 × 10 | `00320B30`, `003204B0` / none | empty in the `us` pack |
| `02EBF150` | — | `BattleUnit_ApplyUnitDefinition`, `BattleStats_RebuildEffectiveStatsAndAffinityState`, `0031C2F0`, `BattleData_SetAreaArdSectionCategory` | the area unit-definition sibling the unit-definition page reads |
| `02EBF158` | 57 × 8, three levels | `002FAE40` (← `setshopname` `0034C170`), `002FA920` (← the shop menu) | **the shop table** — a name id and a ladder of stock lists gated on story progress or clan rank ([the shop table page](../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md), declared there) |
| `02EBF180` | 23 × 1 (directory `+4`) | `003203B0`, `003202F0`, `00325AD0`, `00325A20` | **the weapon-class map**: an equipment row's category byte `+0x26` → a class 0–15 ([the registry page](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md), *the tail read*, declared there) |

The slots this page explains — the party, status, licence-node and gambit-condition tables of
§2.5, the reward, selector and unreferenced tables of §2.8, and the two named above — are now
declared in its front matter.
## 3. Key addresses

| Address | Role |
|---|---|
| `00309440` | `id >> 12` → descriptor class (§2.1) |
| `01EEBCC0` | the fifteen inventory class descriptors, `0x58` bytes each |
| `0030B6A0` | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` — fills the runtime fields |
| `00309EC0` | `BattleEncodedId_DispatchQueryMode0Value` — channel 0 through descriptor `+0x50` |
| `0030AE30` | `BattleEncodedId_DispatchQueryMode1` — channel 1 |
| `0031C5D0` | the query-record filler |
| `0031E598` | its 32-entry jump table, `class − 1` |
| `0035D330` | the row-form wrapper into `022CA520` |
| `0035D380` | the id-form wrapper into `022CA480` |
| `022CA520` | static query record, row form |
| `022CA480` | static query record, id form |
| `00322C50` | `BattleEncodedId_IsValidForClass`, called first by every arm |
| `002F9860` | the string-pool indexer behind `+0x10` — `id / 1000` by reciprocal `0x10624DD3` + `sar 6` (`002F9866`–`002F9872`), 28-group bound `cmp 0x1C` (`002F9879`), empty-string fallback `002F987E` |
| `00236C30` | the loader that binds the descriptors from the blob directory |
| `00238160` | binds the equipment table from directory `+0x38` and walks its ids from `0x1000` |
| `003008A0` | `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` — the one write entry (§2.6) |
| `00309F30` | `Inventory_QueryEncodedItemStateByClass` — the read entry with a mode |
| `002FD150` | `InventoryPackedCountClass_MutateChannels` |
| `002FD8D0` | `InventoryPackedCountClass_QueryChannel` |
| `002FD420` | `InventoryBitsetClass_MutateState` |
| `002FD970` | `InventoryBitsetClass_QueryState` |
| `002FD530` | `InventoryBundleClass09_ApplyGilAndNestedItems` — reward packages |
| `002FD640` | `InventoryBundleClass0A_ApplyNestedItems` — package selectors |
| `002FD780` | `InventoryBundleClass0D_ApplyNestedItems` — bazaar goods |
| `002FD880` | `InventoryEncodedGilClass0E_ApplyGilDelta` — gil by id |
| `00325F40` | `InventoryDerivedIndex_UpdateOnPresenceTransition` |
| `01EECF98` | the five magick-school discovery bits |
| `01EED1B0` | the nibble → derived-list map |

## 4. Data structures and formulas

```
encoded id (16 bits):   nibble = id >> 12 ; index = id & 0xFFF
descriptor  = 01EEBCC0 + nibble * 0x58      (nibble 0..0xE; else class -1)
class       = descriptor[+0x38]  = 5 + nibble
valid       = index < descriptor[+0x3C]

InventoryClassDescriptor (0x58)
  +0x00 u64-tested/low32-used regionA_offset   +0x08 ptr regionA (runtime)   +0x10 u32 regionA_words
  +0x18 u64-tested/low32-used regionB_offset   +0x20 ptr regionB (runtime)
  +0x28 u64-tested/low32-used regionC_offset   +0x30 ptr regionC (runtime)
  +0x38 u32 class            +0x3C u32 idCount              +0x40 u32 cumulativeBase (runtime)
  +0x48 fn  mutate(id, ...)  +0x50 fn  query(id, mode)

the fifteen, as shipped (class: count, regions, handlers)
   5: 0x40   A +0x4748 (64 w)   C +0x57C0   PackedCount mutate/query
   6: 0x1A4  A +0x47C8 (420 w)              PackedCount
   7: 0x200  A +0x4B10 (512 w)  B +0x57C8   PackedCount
   8: 0x51   A +0x4F10 (6 w)                Bitset
   9: 0x18   A +0x4F1C (2 w)                Bitset
  10: 0      —                              none
  11: 0x100  A +0x4F20 (16 w)               Bitset
  12: 0      —                              none
  13: 0x200  A +0x4F40 (32 w)               Bitset
  14: 0x200  —                              InventoryBundleClass09_ApplyGilAndNestedItems (mutate only)
  15: 0x100  —                              InventoryBundleClass0A_ApplyNestedItems (mutate only)
  16: 0      —                              none
  17: 0x20   A +0x4F80 (2 w)                Bitset
  18: 0x80   —                              InventoryBundleClass0D_ApplyNestedItems (mutate only)
  19: 0xFFF  —                              InventoryEncodedGilClass0E_ApplyGilDelta (mutate only)

EncodedIdQueryRecord (0x98) — request, then the common half
  +0x00 u32 class   +0x04 u32 row   (+0x06 u16 id, the id form)
  +0x08 ptr auxiliary text (selected classes)   +0x10 ptr description   +0x18 ptr name   +0x20 s32 channel0   +0x24 s32 channel1
```

**Current class-specific producer table:** [query initialization and reuse, section4](the-query-record-from-initialization-to-reuse.md#4-query-class-producer-behavior).
It replaces the former table's incorrect class10 tail, row+3 gambit lookup index, zero key-item price,
class15/31 triple conflation, dropped action pointer+08, action two-bit source, licence WORD+2A source,
and name-only classification of class28. The original source bytes and exact old/new diff remain in
[Section05 evidence](../_experiments/evidence/continuation-section05-encoded-query/REVIEW.md).
This replacement deliberately distinguishes physical stores from still-unproved output meanings.

*Store-site anchors retained from the former table (FABLE, Claude Opus 5.5, 2026-09-25). These are sites only, re-read today; the linked table gives the meanings.*

- Class 6 copies the `row+0x28` sub-record's `+0xC` / `+8` into `+0x44` / `+0x48` (`0031CA25`–`0031CA36`).
  It stores `0031E9A0(row)` at `+0x50` (`0031CA59`), and one arm stores a byte triple at `+0x5C` / `+0x60` /
  `+0x58` (`0031CA73`–`0031CA81`).
- Class 8 stores `word[action row + 0x2C] & 7` at `+0x3C` (`0031CD82`–`0031CDC5`). The action row comes from
  `02EBF138`, selected by `row+2`.
- Class 18 merges three bits of the state byte at `+0x59C8` into `+0x44` (`0031DA69`–`0031DA9D`).
- Class 20 returns when `byte[row+0x0A]` is 0 (`0031DBD8`). Otherwise it stores that byte at `+0x28` when
  `row+0x1E` is 5 or 6 (`0031DBE9` → `0031D7F4`), and at `+0x24` otherwise.
- Classes 25 and 32 store `00323890(row+5)` at `+0x23` (`0031DFF6`): the result of `003241D0` minus `0x15`,
  mapped to a small code.
- Class 26 merges `row+6` bit 13 and `row+0x24` shifted left one into `+0x25` (`0031E295`–`0031E2E2`).

### 4.1 The inventory word, the bit, and the API

```
packed-count word (items / equipment / loot, region A, u16 per id)
  bits 0..9   ownedTotal   (0..99)
  bits 10..15 reserved     (equipped / committed copies)
  free = ownedTotal - reserved            query mode 0
  loot region B: u8 per id, 0..99          query / mutate channel 3
  items region C: 1 bit per id, set when the total first rises   query mode 4 (any class)

bitset classes (magicks / technicks / gambit conditions / key items / quickenings, region A)
  word index >> 4, bit index & 0xF ; 1 = owned / learned

Inventory_ModifyEncodedItemAndUpdateDiscoveryState(u16 id, s32 delta, s32 absolute, s32 channel, u32 flags) -> s32 after | -1
  flags bit 0: post the "You obtain" line ; bit 1: bundle class 15 takes its second triple
Inventory_QueryEncodedItemStateByClass(u16 id, s32 mode) -> s32
mutate handler (id, delta, absolute, channel, flags) -> value after ; query handler (id, mode) -> value

reward package (class 14 row, 12 B):  u32 gil ; u16 itemA ; u16 countA ; u16 itemB ; u16 countB   (0xFFFF = none)
package selector (class 15 row, 12 B): u16 idA[3] ; u16 idB[3]
bazaar good (class 18 row, 36 B): u16 nameRef ; u16 descId ; (u16 item, u8 count, u8 pad) x3 ; u32 price ; u16 ; (u16 loot, u16 count) x3 ; u16
```
## 5. Call chain

```
menu / message / licence / gambit code (76 + 14 callers)
  -> 0035D330(class, row) | 0035D380(class, id)    static records 022CA520 / 022CA480
       -> 0031C5D0(record)                          validator 00322C50, then the class arm
            -> 0020E600 (row), 02EBF170 banks (+0x18), 002F9860 (+0x10),
               00309EC0 / 0030AE30 -> descriptor[+0x50](id, 0 | 1)   (+0x20 / +0x24)
  <- record pointer (zeroed after a failure)

area load: 00236C30 binds the descriptors from the blob directory (34 sections)
save load / reset: 0030B6A0 rebases the fifteen inventory class descriptors onto the state block
inventory change: caller -> 003008A0(id, delta, absolute, channel, flags)
  -> 00309F30(id, channel) (before) -> descriptor[+0x48](id, delta, absolute, channel, flags)
       packed-count / bitset: write region A (B, C) -> 00325F40 (derived lists) -> 0046A630 (obtain line)
       bundle 14 / 15 / 18: GameState_SetGil, then 003008A0 per nested item ; gil 19: GameState_SetGil
  -> on a first acquisition through channel 1: [02EBF190]+4 |= discovery bit
```

## 6. Modding notes

- **Adding ids to a class is bounded twice**: by the `st2e` row count the loader binds *and* by the
  descriptor's `+0x3C` in the image (`01EEBCC0 + nibble × 0x58 + 0x3C`), which the query
  dispatchers and the derive path check. Equipment already ships 557 rows behind a 420-id count.
- **The state block's inventory region is a fixed layout** (§2.3) — a class's region A cannot grow
  without moving every region after it and the descriptor offsets that name them.
- **A class with no query handler answers 0 owned** through the query record; that is the
  behaviour a menu will show for a new class until a handler is installed at `+0x50`.
- **Counts cap at 99 in the word itself** (bits 0–9 masked, the clamp at `002FD2F5`); a larger
  stack needs a wider field and every reader of the word.
- **Granting `0x1000` is refused** by the modify entry; a mod that wants a real "unarmed" item must
  use another id.
- **A reward package is data**: class-14 rows are `{gil, item, count, item, count}`, and any code that
  calls the modify entry with a `0x9xxx` id and delta 1 hands out the row — the treasure path does
  not need touching to change what a chest holds.
- **Bank labels to use when authoring names**: loot in bank 11, key items in bank 12 (maps first),
  augment texts in bank 10, items / magicks / technicks / quickenings in bank 0, equipment in bank 1.

## 7. What is not known

- [x] ~~SECTION-05: remaining class-specific output meanings, caller compatibility/reentrancy and
  resource-owned string lifetime; see the current mechanism's precise boundaries.~~ *SUPERSEDED 2026-09-29 (SWE2-FRONTIER): duplicate of OV-1 - the same ask in substance; OV-1 carries it. Register OV-4.*
- [ ] **OV-5.** SECTION-05: shipped-state reachability of unusual count/high-pointer/fourth-key-range cases,
  and formal independent acceptance. These are not closed by synthetic assertions.

The checked historical entries below retain their original scope, not acceptance of the new corrections.


- [x] ~~What region B (`+0x57C8`, loot) and region C (`+0x57C0`, items) hold, and what the two
      query channels return per class.~~ **FY-1 ANSWERED 2026-09-11 (§2.7):** region B is a second
      per-loot byte counter (channel 3), region C the items' ever-owned bitset (set on a first rise,
      read by mode 4); the channels are free / total / reserved / region-B byte for the packed word
      and the bit for the bitset classes.
- [x] ~~What the tables of classes 14, 15 and 16 are.~~ **FY-2 ANSWERED 2026-09-11 (§2.8):** 14 is
      the reward-package table `{gil, item, count, item, count}`, 15 a package selector (two triples,
      rows 128–172 shipped); 16 (`02EBF060`, one `u32` per row) is bound, validated and consumed by
      nothing — a census negative with class 15's consumer as the control.
- [x] ~~Which caller drives loot's channel-3 byte~~ **answered 2026-09-11: the sale commit adds and
      the bazaar purchase reset zeroes it (the bazaar page).** ~~What the twelve derived-index lists
      look like~~ **read (§2.9): `u16` id arrays, counts at `+0x47B8`, add / remove / compact, the
      category flags at `+0x3244`.** ~~Still open: **the code that fills the capacity table `02092760`**
      (no rip-relative writer).~~ **Answered 2026-09-15: `SaveRuntime_InitializeImageBackedPointerDescriptor`
      (`00253240`), through the image base (§2.9).** **FY-4.**
- [x] ~~Who reads the bazaar row's price at `+0x10` and its three `(loot, count)` pairs from `+0x16`.~~
      **FY-5 ANSWERED 2026-09-11:** the refresh `0030B270` compares each loot's sold tally against
      the count, the purchase reset `0030B180` zeroes the tallies, and the shop driver charges the
      price ([the bazaar page](../12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md)).
- [x] ~~Who reads the discovery bits of `[02EBF190] + 4`.~~ **FY-6 ANSWERED 2026-09-11 (§2.9):**
      `00318CD0` under `BattleMenu_BuildCommandEntryList` — the Magicks / Technicks / Mist command
      gates; the five school bits have no reader.
- [x] ~~What the class-specific stores of §4 mean — the raw sources are listed; which caller reads
      which offset of the record is not censused (76 + 14 + 14 callers).~~ **FY-3 ANSWERED
      2026-09-12 (FABLE)** — the census in §2.4: 37 / 10 / 5 functions read the name, the
      equipment block `+0x3C`–`+0x48` / `+0x58`–`+0x60` is read by one group of seven menu
      functions and the licence bytes by eight in the bounded historical routes. Absence of other
      hits does not establish absence of producer writes or all downstream use (SECTION-05). What
      each equipment field *means* to those seven is on [the Optimise page](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)
      (P-4) for the `+0x58`–`+0x60` trio; the rest is per-reader and not pursued here.
- [x] ~~The tables the consumer sweep reaches but does not name (§2.10)~~ **ANSWERED 2026-09-12 (FABLE):** `02EBF020` (six rows the
      command-list builder scans) is the scripted command-list presets, keyed by the member's type byte in five groups (the §2.10 row); ~~and `02EBF008` (the clock-driven schedule whose consumers `002EFA70`
      / `002EFE40` are unread)~~. **Slot 0 named 2026-09-12 (FABLE):** the **movie fade schedule** —
      49 rows of `{id, fadeInStart, fadeInLength, fadeOutLength, fadeOutLead, …, flags}` that
      `0037DEA0` turns into `002EFA70` fade-ins and fade-outs on layer 0 ([the screen-fade layers](../17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md)
      §2.4); the "clock" was the movie player's elapsed frame count. ~~`02EBF030` / `02EBF028`~~ are the SetSaveData presets, ~~`02EBF010`~~
      the per-field locomotion spacing rows (2026-09-11). **FY-7 (narrowed).**
- [x] ~~Why the equipment table ships 557 rows against a 420-id descriptor, and what rows 420–556
      are (rows 555–556 resolve to *(reserve)*).~~ **ANSWERED 2026-09-12 (FABLE), from the shipped
      table:** rows 420–543 are 124 `NOT USED` rows, spread over thirteen equipment classes (57 in
      class 0, 22 swords, 13 greatswords, 13 shields, 4 guns, 4 maces, 3 spears, 2 crossbows, 2 bolts,
      one each of poles / daggers / staves / shot — [the id-encoding page](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)
      §11), none of them zeroed beyond the name; rows 544–556 carry bank-1 references `0x800 + row`
      that exceed the bank's 544 blocks. The descriptor's 420 ids are the named rows plus the
      `Reserve` block at 181–191; the padding is authored slack, not a second table.
- [x] ~~Whether the other language copies of `battle_pack.bin` bind the same directory offsets.~~ They
      carry byte-identical tables at the same offsets (the text-banks page §5.2, 2026-09-11).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `00309440` returns `[01EEBCF8 + (id >> 12) × 0x58]` for nibbles 0–0xE, else −1 | `00309443`–`0030945D` | 1 |
| the descriptor table starts at `01EEBCC0`, stride `0x58`, fifteen records | `0030B6A8`, `0030B6B2`, `0030B6F9`–`0030B700` (`01EEBCC0` → `01EEC1E8` = 15 × 0x58); `01EEBCF8` = record 0 `+0x38` | 1 |
| the rebaser fills `+8`, `+0x20`, `+0x30` from `+0`, `+0x18`, `+0x28` plus the state base, and `+0x40` as the running sum of `+0x3C` | `0030B6C0`–`0030B6F5` | 1 |
| the dispatchers bound by `+0x3C` and tail-call `+0x50` with mode 0 / 1 | `00309F08`–`00309F20`, `0030AE78`–`0030AE93` | 1 |
| the fifteen records carry classes 5–19, the counts, offsets and handlers of §4 | the shipping image, `.data` file offset `0x1DCA2C0` – `0x1DCA7E8`, read 2026-09-11 | data |
| region A offsets and word lengths abut for the eight classes that have one | arithmetic on the same bytes (`0x4748 + 64×2 = 0x47C8` … `0x4F40 + 32×2 = 0x4F80`) | data |
| `0031C5D0` dispatches on `class − 1` through `0031E598`, validates first, returns 0 / −1 / −2 as §2.4 | `0031C5EA`–`0031C61D`, `0031C643`–`0031C655`, `0031DDA6`–`0031DDB5`, `0031E57A` | 1 |
| every class arm's name store comes from the row word at the offset in §2.5 and goes to record `+0x18` | the 21 `02EBF170` sites `0031C6B5`, `0031C7BB`, `0031C915`, `0031CB7D`, `0031CCE7`, `0031CE8D`, `0031D038`, `0031D176`, `0031D324`, `0031D4E7`, `0031D86E`, `0031D9C2`, `0031DB48`, `0031DC58`, `0031DD5E`, `0031DE19`, `0031DF59`, `0031E1D7`, `0031E352`, `0031E3F0`, `0031E4DE`, each preceded by the row load and followed by the `+0x18` store | 1 |
| the two static records and their wrappers | `0035D336`–`0035D36A`, `0035D386`–`0035D3BB`; a whole-image rip-relative census of `022CA480`–`022CA5B8` finds only the wrappers and `0035E070` | 1 |
| 76 / 14 / 14 callers | `edges.tsv` for `0035D330`, `0035D380`, `0031C5D0` | 1 (graph) |
| which caller reads which offset | `qrcensus.py` over the graph's callers (75 / 14 / 12 today), register-tracked; the equipment arm's upper stores `0031CA1D`–`0031CAB6` | 1 (static heuristic) |
| the loader's descriptor ↔ directory-offset pairs | `00236C86`–`0023701E`: each `call 003845F0` / `003846F0` with its preceding `lea rcx, [desc]` and `movsxd rdx, [rax + off]` | 1 |
| row counts, strides and names per class | the `us` `battle_pack.bin` sections listed in §2.5, five rows each, decoded through the bank walk the text-banks page validated | data |
| the identity readings of §2.5 | the names plus the counts (81, 24, 8, 5, 32, 129) — and, for class 13, the bitset handler; no player-facing check was made | data + inference |
| the modify entry's refusals, before / handler / after sequence, and the channel-1 first-acquisition gate | `003008AF`–`003008F5`, `00300919`–`00300929`, `0030093C`–`00300962`, `00300968`–`0030097C` | 1 |
| the packed word's two fields and the four channels, the cap of 99, the region-C bit on a first rise | `002FD8D0`–`002FD95F`; `002FD253`–`002FD34B`, `002FD383`–`002FD405` | 1 |
| the bitset bit's addressing and saturation | `002FD472`–`002FD4E9`; `002FDA2F`–`002FDA57` | 1 |
| the bundle handlers' row fields and nested calls | `002FD552`–`002FD626`; `002FD662`–`002FD757`; `002FD7A2`–`002FD85D`; `002FD89A`–`002FD8B4` | 1 |
| the discovery bits and the school table | `00300982`–`00300B5A`; `01EECF98` read from the image | 1 + data |
| the derived-index map and list mechanics | `00325F79`–`0032601D`; `01EED1B0` and its byte maps read from the image; `00252E7A`–`00252F18`; `002535F0`–`0025366D` | 1 + data |
| the fifteen functions that reference `01EEBCC0` | a whole-image rip-relative census of the table base, 2026-09-11 | 1 |
| class 14 / 15 / 18 row readings | the `us` tables at directory `+0x98`, `+0x9C`, `+0xE8`, rows decoded through the class tables of §2.5 | data |

## 9. Related

- [`the-encoded-id-class-registry.md`](the-encoded-id-class-registry.md) — the validator's 32 classes; this page names the eleven it could not, and closes its `00309440` item.
- [`battle-text-banks.md`](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) — the banks the name field resolves through; bank 10 / 11 / 12 relabelled from this page.
- [`item-id-encoding-and-equipment-compatibility.md`](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md) — the category nibble; identical to `class − 5`.
- [`the-battle-state-block-field-map.md`](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) — the block the regions live in.
- [`the-save-payload-field-map.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) — the rebase on load.
- [`authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) — the slots by weight of use.
- [`the-post-result-events-and-the-battle-message-table.md`](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) — `00536410`, a direct caller.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every §8 claim that can be recomputed was recomputed. **All of them hold**, and two of them hold only
in the unit the page chose — which is now the most reliable thing this sweep knows about the
database's counts.

### The arithmetic

| claim | recomputed |
|---|---|
| the table starts at `01EEBCC0`, stride `0x58`, **fifteen** records → `01EEC1E8` | `01EEBCC0 + 15 × 0x58 = ` **`01EEC1E8`** |
| `00309440` returns `[01EEBCF8 + …]` | `01EEBCC0 + 0x38 = ` **`01EEBCF8`** — the field is `+0x38` of each record |
| region A offsets abut: `0x4748 + 64×2 = 0x47C8` | **`0x47C8`** |

### `00309440`, instruction for instruction

```asm
00309440  movzx eax, cx
00309443  shr   eax, 0xc          ; id >> 12
00309446  cmp   eax, 0xe
00309449  ja    0030945A          ; nibble > 0xE ...
0030944B  imul  rcx, rax, 0x58
0030944F  lea   rax, [rip → 01EEBCF8]
00309456  mov   eax, dword ptr [rcx + rax]
00309459  ret
0030945A  or    eax, 0xffffffff   ; ... returns -1
```

**"nibbles 0–0xE, else −1" is exact**, and the `ja` is safe because `eax` arrives through `movzx`
then `shr 12` and cannot be negative.

### Two counts that are right in their own unit — and wrong in every other

| claim | the unit that gives it | what other units give |
|---|---|---|
| **"the fifteen functions that reference `01EEBCC0`"** | **15 functions** ✔ | **19** referencing instructions |
| **"the 21 `02EBF170` sites"** | **21 name-lookup sites** in `0031C5D0` ✔ — the sequence *row word → slot → `shr 0xb` → `[rax+rcx*4+4]` → `call 0020E600`* | **42** raw references to the slot in that function; **58** across the image; **9** functions |

> **Both numbers are exactly right, and a reader who counts instructions instead of functions, or
> references instead of sites, will conclude both are wrong.** `0031C5D0` is 8,136 bytes and touches
> `02EBF170` forty-two times to perform twenty-one lookups — a factor of two that looks like an error
> and is a unit.

`02EBF170`'s 58 image-wide references match what [the authored-table row
lookup](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) §15a measured
independently while establishing that this slot is **not** one of the forty that feed both halves of
the registry shape — it is read here through `[rax + rcx*4 + 4]`, a different addressing entirely.

**Not claimed:** the page's own note that the caller census reads 76/14/14 in `edges.tsv` and
75/14/12 under `qrcensus.py` *"today"* is untouched — it is a drift the page already records, not a
contradiction this pass resolves. Nothing here was executed or observed live.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `003FDFE0` | 947 | query-record consumer on `[rbx+0xE0]`/`+0x180`: `005C5230`, `003697F0`, `002527B0` x2, `0035D330`, `002CCA10`/`002CCA00`, `003FD2C0`/`003FCA70`/`003FFA20` pair repeated |
| `00564430` | 497 | item/shop helper chain: `00252FA0`, `00252F40`, `0020E600`, `00292B70`, `002B3050`; caller `00565E00` |
| `0056C490` | 959 | shop-screen quantity-entry body (also a member of the shop screen, [the shop screens](../16-UI/Shop-Screens/the-shop-screens.md)): `[rcx+0xE4]`, `[rsi+0x12]`, `[rbx+0x60]`, `0029FB50`/`0029FA40`, `00243260`, `0056E700`, `00567690`, `002F9860`, `00291D80` |

*(Pass 22 adjacency, 2026-09-14: the query path crosses three layers — `00253970` calls **input**
`00249840`/`0035FF60`, `00557DB0`/`0057AC10` call **audio** `00249C60`, and `00309EC0` is called
by **achievements** `00315E90` (5 edges). The query record is read by input-handling, audio and
achievement code; the crossings are consumers of the id space, not owners of it.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **ActorEntity — CLIENT and SERVICE.** `ActorManager_RunFieldRuntimePass` (twice), `BattleGroup_RefreshFourActorDefinitions`, `BattleUnit_ApplyUnitDefinition` and `BattleSlotMap_InitializeMappingClasses` call cited functions. Cited functions call `BattleUnit_FindMappedDefinitionSelectorByIndex`, `ActorRuntime_GetClass3FloatPair` and `ActorHandle_EncodeRegistryEntry`.
- **CombatFormula — SERVICE and CLIENT.** Cited functions call `BattleStats_GetByBattleSlotIndex` (6), `BattleStats_InitializeDefinitionRecord`, `BattleStats_GetByMappedBattleSlot` and `BattleStats_FindOwningBattleUnit`. They are called by `BattleStats_RebuildEffectiveStatsAndAffinityState` (twice) and `BattleFormula_ApplyTargetResult`.
- **Presentation — CLIENT.** `BattlePresentation_EnqueueReactionWithRandomizedVariant` (twice) and four other Presentation bodies (433 to 636 bytes) call cited functions. One cited function calls a 460-byte Presentation body.
- **Resource — SERVICE and CLIENT.** Cited functions call four small Resource helpers (20 to 75 bytes), and are called by two Resource bodies (298 and 352 bytes).
- **Rewards_Progression_Economy — SERVICE and CLIENT.** The two inventory gil appliers call `GameState_GetGil` and `GameState_SetGil`, and another cited body calls `GameState_SetGilClampedNonnegative` and a 432-byte rewards body. Cited functions are called by `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (twice), `GameState_AddGilClampedAndNotify` and `BattleUnit_ProcessDefeatRewardsAndLoot`.
- **Spawn_Encounter_Lifecycle — MECHANICAL (SWE2-EC7-42, 2 edges).** `0031B810`, called by this page's `00309FB0` section body, is also called by two Spawn-filed bodies; the crossing is shared-helper fan-in, not that this page owns anything in that layer.


**CombatAI — CLIENT (SWE2-EC7-156, 27 edges).** `00301AD0`/`00308C20`/`003219D0`/`003247F0` of that layer call `00236820`, the resolver batch-121's `0033D200` also consults — shared-helper fan-in, not a shared responsibility.
**Gameplay — CLIENT and SERVICE (SWE2-EC7-156, 41 edges).** `00339630` calls `00202B10`/`00203170`, `0030C210` calls `00236820`, and `00239960` calls `00237DF0` of that layer — the two layers exchange helpers, no second owner.
**Items_Equipment_Shops_License — CLIENT (SWE2-EC7-156, 106 edges).** `0031A300` calls `00236820`, `0033AF50`-side bodies call `002370C0`, and `00239960` calls `00300BA0` — shared-helper fan-in across the item/equipment layer, not a shared responsibility.
**Movement — CLIENT (SWE2-EC7-156, 179 edges).** `00334220`/`003347C0`/`00334E00`/`00335B60` call `00202B10`; the movement layer consults this page's shared resolver — fan-in, not a shared responsibility.
**Party — CLIENT and SERVICE (SWE2-EC7-156, 15 edges).** `003261D0`/`003273D0` call `00236820`, `00283270` is reached by `00328BD0`, and `00239960` calls `00329080` of that layer — shared-helper exchange, not a second owner.
**Script_VM_Native_Bridge — CLIENT (SWE2-EC7-156, 26 edges).** `00356160` calls `00203170`, `003559B0`/`00355EB0` call `002EFA70` — the script bridge consults this page's helpers, shared fan-in.
**UI — CLIENT (SWE2-EC7-156, 437 edges).** `002C7B10`/`002C84E0`/`003FC170`/`005512B0` call `00202B10`; the interface layer is this page's largest shared-helper client — fan-in, not a shared responsibility.

**Save_Load_Settings — CLIENT (SWE2-EC7-158, 21 edges).** Batch-123's `003FD860` names `00244960`, whose callers (`0057E4D0`/`005819F0`/`005823B0` among them) sit on the save-load layer — the query record's helpers are consulted there, not owned there.
- **RNG_Random_Selection — MECHANICAL (2 edges).** 2 calls from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_NextU32_Thunk` (00379CD0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **Status_Periodic_Terminal — CLIENT and SERVICE (9 edges).** 8 inbound (Status_Periodic_Terminal bodies `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `FieldData_GetActiveFieldRecordBit15` (00377C20), `0031E9A0`); 1 outbound (page-cited `BattleStats_SetEquipmentSlotByMappedId` (0031A510) call Status_Periodic_Terminal bodies `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0)). Substantive edges include `0031E9A0` is called by `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0); `00323890` is called by `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0); the remaining edges run through shared helpers the page cites.
- **World — CLIENT and SERVICE (3 edges).** 2 inbound (World bodies `003847B0`, `00238640` call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0)); 1 outbound (page-cited `00236C30` call World bodies `003847B0`). Substantive edges include `00236C30` calls `003847B0`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (34 edges).** 24 inbound (WorldAreaField bodies `00236C30`, `00238850`, `BattleSystem_InitializeAreaState` (002342F0) call page-cited `003846F0`, `002EFA70`, `002EFE40`); 10 outbound (page-cited `00236C30`, `00237FC0`, `00238160` call WorldAreaField bodies `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `003846F0`, `WorldTransition_GetActiveOrPendingFieldId` (003148F0)). Substantive edges include `00236C30` is called by `00238850`; `00236C30` calls `003846F0`; `00237FC0` is called by `00236C30`; `00238160` is called by `00236C30`; the remaining edges run through shared helpers the page cites.
## The `0030B270` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0030B270` (`BattleIdClassD_RefreshPrerequisiteRuntimeFlags`, ~105 B) —
`qword[02EBF058]` non-null gate (`0030B279`/`0030B280`).

| member | role | interior |
| --- | --- | --- |
| `0030ADC0` | `cx == 0xFFFF` → `-1`, else `movzx` — sentinel decode (`0030ADC0`/`0030ADCE`) | [`0030ADC0`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `0031C5D0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0031C5D0` (~105 B) — six-register body (`0031C5D0`/`0031C5E6`).

| member | role | interior |
| --- | --- | --- |
| `0030AE30` | `cx == 0xFFFF` -> `-1`, else `movzx` — same sentinel decode as `0030ADC0` (`0030AE30`/`0030AE3E`) | [`0030AE30`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `0037DDD0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0037DDD0` (~239 B) — `00184860()` result dispatch: `<= 0` out, `== 2`
arm (`0037DDD4`/`0037DDE1`).

| member | role | interior |
| --- | --- | --- |
| `0037DEA0` | `rbp = qword[rcx+0xC8]` record deref (`0037DEAA`) | [`0037DEAA`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00184860`.

## SWE2-EC7-27 update (2026-09-18) — `002CDE20` status-to-byte map

`002CDE20` (39 B) calls `002CD920()`: a negative result returns 1,
otherwise the word feeds `00252D10` and the byte comes back — the
status-to-flag read the menu code uses to check whether the unlocked
flag bank reports seen. Interior anchor `002CDE3A` (the `00252D10`
call).

## SWE2-EC7-28 update (2026-09-18) — `0029FB50` scaled-height writeback + `0029CB80` ring publish

`0029FB50` (126 B) is the sibling commit arm: same `+0x08` 10-bit
extract, `0020E600` resolve and `002D8B00` measure, then commits
`word[+0xA] = word[+0x10] - (result * float[+0x28]) + word[+0xC]` and
`byte[+0x2D] = (al & 0xD7) | 0x10` — the field-height writeback with
its flag set. Interior anchor `0029FBB2` (the `+0xA` compose).

`0029CB80` (113 B) — reached through `0027CE70`/`00293310` — resolves
`ecx` (`>= 0x186A0` goes through `002F9920` after subtracting
`0x186A0`, else `002F9860`), then round-robins a `[rip-counter] ++ & 7`
index `* 0x20` into the 8-entry table and `002B4090`s the resolved
pointer plus `ebx`/`0x20` into the slot — the publish ring the menu
reads consume. Interior anchor `0029CBC0` (the `& 7` index).

## SWE2-EC7-29 update (2026-09-18) — `00290CD0`/`002907F0` `0209BE80` bank forwards

`00290CD0` (21 B) and `002907F0` (76 B) — reached through `0027B880` —
are the `0209BE80` bank's two list forwards: `00290CD0` copies `ecx`
into `edx` and tail-jumps `003F35A0([0209BE80+0x10F40])` — the bank's
`+0x10F40` channel object; `002907F0` walks the `+0x10F20` head's
`+0x9B0` links calling `003F3080(node, 1)` on every node whose `+0x980`
doesn't match `ecx` — the notify-all-but-self sweep the selection code
runs when a record changes hands. Interior anchors `00290CD9`/`00290820`
(the `+0x10F40` load / the `003F3080` call).

## SWE2-EC7-34 update (2026-09-19) - `003FD360`

`003FD360` (842 B) is a query-record setter - `dl`->`[rcx+0x17E]`, `dl+0x40`->`[rcx+0x17F]`, `01F2CC98` table, `00252D10`/`0057D610`/`002CCA10`/`002526F0`/`00252D40`. Interior anchor `003FD439` (an `00252D10` call).

## SWE2-EC7-34 update (2026-09-19) - `003FDFE0`

`003FDFE0` (947 B) is an id dispatch - `[rdx]` switch `{1, 9}` arms, `003697F0`/`002527B0`/`003FE377`/`003FD2C0`/`005C5230`. Interior anchor `003FE05F` (an `003697F0` call).

## SWE2-EC7-35 update (2026-09-19) - `00335B60`

`00335B60` (748 B) is a query-record body - `008F3108`/`008F30F8`/`01CEBDA0`/`01F004C0`, `00202FE0`/`00202B10` triples plus `00203170`/`00202B70`/`00391410`. Interior anchor `00335BDF` (a `00202FE0` call).

## SWE2-EC7-36 update (2026-09-19) - `0027B880`

`0027B880` (646 B) is a query-record body - `0035D330`/`00290C80`/`00290C60` quadruples plus `003C93E0`/`0035C150`/`0028C3C0`. Interior anchor `0027B898` (a `0035D330` call).

## SWE2-EC7-36 update (2026-09-19) - `00273BA0`

`00273BA0` (643 B) is a query-record sibling - `002D03B0`/`002D02C0` quadruples plus `0035D330`/`00808C40`. Interior anchor `00273BDA` (a `002D03B0` call).

## SWE2-EC7-38 update (2026-09-19) - `00564430`

`00564430` (497 B) is an encoded-id query body - `01F44830`, `00252FA0`/`00252F40`/`0020E600`/`00292B70`/`002B3050`/`00808C40`. Interior anchor `00564567` (a `00252FA0` call).

## SWE2-EC7-40 update (2026-09-19) - `002CB1F0`

`002CB1F0` (361 B) is an encoded-id query body - `002F9860` quintuple plus `0020E620` triple and `0029FB50`/`0035D330`. Interior anchor `002CB233` (a `0035D330` call).

## SWE2-EC7-40 update (2026-09-19) - `0031C2F0`

`0031C2F0` (380 B) is an encoded-id sibling - `02EBF120`/`02EBF130`/`02EBF150` fields, `0020E600` sextuple plus `00322C50`. Interior anchor `0031C354` (an `0020E600` call).

## SWE2-EC7-42 update (2026-09-19) - `00309FB0`

`00309FB0` (318 B) is `Inventory_QueryOwnedCountIncludingReservedActionItems` - `01EEBCC0`/`022C1788`, `0031B810`/`00377C20`. Interior anchor `0030A039` (a `0031B810` call).

## SWE2-EC7-44 update (2026-09-19) - `002CFEE0`

`002CFEE0` (253 B) is a body - `002D01A0`/`0035D330`. Interior anchor `002CFF10` (a `002D01A0` call).

## SWE2-EC7-46 update (2026-09-19) - `002D02C0`

`002D02C0` (225 B) is a body - `0035D330` single call. Interior anchor `002D030D` (the `0035D330` call).

## SWE2-EC7-48 update (2026-09-19) - `00295FE0`

`00295FE0` (200 B) is an encoded-id/query-record body - `0020E600`/`002B58B0`/`0035D330`. Interior anchor `0029601B` (a `0020E600` call).

## SWE2-EC7-48 update (2026-09-19) - `00275E40`

`00275E40` (200 B) is an encoded-id body - `003178C0`/`0035D330`. Interior anchor `00275E8C` (a `003178C0` call).

## SWE2-EC7-60 update (2026-09-19) - `003FD2C0`

`003FD2C0` (155 B) is a query-record consumer body - `00244F00`/`00246AD0`/`002470C0`/`002CC760` plus `0208EA28`/`0209AC30`. Interior anchor `003FD2D6` (a `002470C0` call).



## SWE2-EC7-63 update (2026-09-19) - `002D0100`

`002D0100` (145 B) is a `+0x4C` query-record body - `002CFDA0`/`0035D330`. Interior anchor `002D0128` (a `0035D330` call).



## SWE2-EC7-64 update (2026-09-19) - `002CFDA0`

`002CFDA0` (146 B) is a `+0x4C` query-record sibling - `0035D330` single call. Interior anchor `002CFDC9` (a `0035D330` call).



## SWE2-EC7-66 update (2026-09-19) - `003FFA20`

`003FFA20` (133 B) is a query-record consumer - `0027F210`/`00282EA0`/`00283270`/`00283E40`/`002858A0`/`0031A510` plus `0209AC30`. Interior anchor `003FFA3C` (a `00282EA0` call).


## SWE2-EC7-69 update (2026-09-19) - `002F9920` bucketed id resolver measured

`002F9920` (314 B) is the high-id resolver the page routes `ecx >= 0x186A0`
into: `edx = ecx / 10000` (signed magic `0x68DB8BAD`, `sar 0xC` + sign fix)
buckets the id into a 28-entry pointer table at `02FDA3D80`
(`edx >= 0x1C` or a null entry returns the `01CEB638` default). Each bucket
entry is a `[+4]`-counted list of `0020E600`-resolved handles; the scan
matches `dword[resolved] == esi`, and a hit chains the leaf resolution -
`[+0x14]` → `0020E600` → `[+4]` → `0020E600` → `[+4 + ebx*4]` → `0020E600` -
returning the fully resolved record, else the default.
Interior anchor `002F992F` (the `sar edx, 0xC` bucket shift).

## SWE2-EC7-70 update (2026-09-19) - `002858A0` nine-slot selector reconcile measured

`002858A0` (355 B) is the reconcile the query-record consumer runs: two
`0020E600` resolves of the `[0209AC30]+0x30` context (one + `0x118`), then
nine iterations over the `[+0xF8]` record's `+0xAC8`-adjacent slot rows
(`[r13+0xC0+i*8]`): writes `+0xC0 = i`, xor-folds flag byte
`[+0xB10 + word[rsi+0x60]]` bit 3 into `+0xFC` (negative word clears it),
calls `00247870`, accumulates `word[+0x9A]` from `+0x10A`/`+0x10E`/`+0x34`/
`[+0x118]+0xC` on later passes, and runs `00283E40` on each slot.
Interior anchor `0028596E` (the `xor`/`and 8` flag fold).

## SWE2-EC7-71 update (2026-09-19) - `0027F210` five-slot selector-table fill measured

`0027F210` (199 B) is the fill sibling of `002858A0` on the same
`0209AC30`/`+0xAC8`/`+0xDE0` record family: loops `rsi` `0x98` -> `0xAC`
step 4 (five slots) with `r14` `0xD40` -> `0xE40` step `0x20`; each
iteration resolves `[0209AC30]`, reads the selector `word[rbx+0xDE0]`
into `[rbx+sel*8+0xAC8]`, zeroes the 0x20 out row, and reads
`word[rec+rsi+2]` - `0xFFFF` leaves the row blank; otherwise
`0035D330(1, key << 16)` resolves the key and `002B58B0(result->[+0x18],
0)` produces the row pointer, with `byte[+0x2C]`/`byte[+0x38]` copied to
row `+0xA`/`+0xB`.
Interior anchor `0027F282` (the `0035D330` key resolve).

## SWE2-EC7-75 update (2026-09-19) - `002CCA10` id-class range check measured

`002CCA10` (22 B) is the small class check the query record callers
run: `ecx - 7 <= 2` unsigned (ids 7..9) or `ecx == 0x11` - returns the
bool.
Interior anchor `002CCA13` (the `cmp eax, 2` bound).

## SWE2-EC7-76 update (2026-09-19) - `0029FF60` + `00283E40` resolver/propagate pair measured

`0029FF60` (247 B) is the `0x186A0`-split resolve-and-dispatch: the
id comes from `[rsp+0x50]` or `[rcx][+0x14] + 0x186A0`; `>= 0x186A0`
resolves through `002F9920(id - 0x186A0)` (the verified high-id
resolver), below through `002F9860`. With `rdi` set, `[rsi+8] &
0xFFFFFFC0 << 0x10` positive picks `00365B30` when `r8d > 0x20` else
`0029CC70`; non-positive picks `002B4090`; `rdi` NULL picks
`0029CC00`/`0029CB80` on the same test. The result lands at
`[rsi+0x18]` and `[rsi+0x20]` gets `0020E620([rsp+0x58])`.
Interior anchor `0029FFB8` (the `002F9920` high-id call).

`00283E40` (1,547 B) is the master flag-propagate over the
`*(0209AC30) + [rbx+0xC0]*8 + 0xAC8` slot record (`r14`): `[rbx+0xC8]`
gets `002845E0`, `[rbx+0x50]` `00243E90`, `00247930(rbx, 0x5D -
2*word[r14+0x60])`; then the `+0x60`-negative arm clears bit 0 across
the `[rbx+0x60]`-listed sub-objects at `+0x140`..`+0x190`/`+0x178`..
`+0x188` and a 0xC0..0x118 loop, sets `[rbx+0x50]` bit 0, and by
`[r14+0x44] & 0x80000003` sets `[rbx+0xFC]` bit 2. `+0xF8` zero runs
`002D0280`/`002D02C0`/`002D03B0` then up to 11 `+0x39`/`+0xA` writes;
`+0xFC` bit 6 runs `0032A8A0(0x4006)`/`003236B0`/`00323670`/
`00323630`/`00556380`/`0029FB50` chains, `0029F6E0` five times with
`r9d = 0x80808080`, `002DD7E0` twice, `002B58B0`, `0035D330`, and a
final `+0x87`-bounded loop writing `+0x39`/`+0xA` on the tail
sub-objects.
Interior anchor `00284133` (the `0029FF60` call - this batch's own
resolver).

## SWE2-EC7-77 update (2026-09-20) - `00243E90` element flag sync measured

`00243E90` (80 B) is the `[rcx+0x50]`-slot call the `00283E40`
propagate makes: `([rcx] >> 2) & 0xFFFF` elements at `[rcx+0x10]`
(stride 8) each get `xor [elem+8], (((*[elem]) >> 28) ^ [elem+8]) &
1` - i.e. bit 0 of `+8` is rewritten to equal bit 28 of the pointed
dword. The whole loop is skipped when `[rcx] & 0x3FFFC` is zero.
Interior anchor `00243EC5` (the `shr ecx, 0x1c`).

## SWE2-EC7-95 update (2026-09-20) - `003203B0` + `00317B70` measured

`003203B0` (160 B) is the id-decode query `002EE430` and
`003202F0` run: `word[rdx]` is primed `-1`, two `0020E600`
resolves on the `02EBF1xx` globals build the row pointer
`word[+8]*(cx-0x1000)+eax`, `cx != 0xFFFF` plus `byte[+7] < 0x20`
admits `byte[+0x26]` as the column (else -1), and
`word[02EBF110]*column +4` indexes the result byte written to
`[rdx]`.
Interior anchor `003203D5` (the first `0020E600` call).

`00317B70` (76 B) is the `0x1C8`-stride record fetch
`002CA7C0`, `0057A620`, `0057AC10`, `0027F030`, `002826F0`,
`00282A40` and `0057B1A0` share: `cl <= 0x27` indexes
`[02EBF190]+8`, `~r9 & 1` is published through the stack slot,
`rdx` points at `record+0x50`, and `00317930` finishes with
`r9d = r10w`.
Interior anchor `00317BAB` (the `00317930` call).

## SWE2-EC7-96 update (2026-09-20) - `00300BA0` measured

`00300BA0` (28 B) is the fixed-flags trampoline `00239960`,
`0023AF50` and `0032A830` call: it repacks `(rcx, rdx, r8d = 1,
r9d = 1)` with the caller's `r8d` forwarded through the stack
slot and falls into `003008A0` - the two-ones-shim into the
shared query.
Interior anchor `00300BB2` (the `003008A0` call).

## SWE2-EC7-98 update (2026-09-20) - `0024DE70` measured

`0024DE70` (60 B) is the top-nibble dispatcher `002EF910`,
`00322310`, `003226D0`, `003228E0`, `0036E1E0`, `0036E540`,
`0036E640`, `0036E680`, `0036E6B0` and `0036E8B0` call:
`sar eax, 0x1C` + `and eax, 0xF` extracts the id's high nibble,
`dec` + `cmp eax, 8` / `ja` bounds the family index, and an
image-relative offset table at `0024DEAC` jumps into four arm
stubs that tail `002FCA00`, `003B0AD0`, `00375AE0` and
`003B2510`; out-of-range nibbles return 0 - the class-select
front end the encoded-id queries share.
Interior anchor `0024DE88` (the offset-table load).

## SWE2-EC7-99 update (2026-09-20) - `002D03B0` measured

`002D03B0` (83 B) is the register thunk `00273BA0` and
`00283E40` call: a stack record built under the stack
guard carries `002D0270` as its entry point and `r8d = 4`
as its arity, then `00249CE0` consumes it - the
four-argument callback registration the query-record
layer issues.
Interior anchor `002D03E6` (the `00249CE0` call).

## SWE2-EC7-100 update (2026-09-20) - `002CD920` + `002CA490` measured

`002CD920` (181 B) is the id-class mapper `002CDE20` and
`002CDE50` call: `ecx - 0x405` bounds a `0xB9`-entry
image-relative offset table at `002CD9D8` (a dead
`002CDA1C` byte-table read rides alongside), and the arms
return constants `0x29` through `0x3A` - out-of-range ids
yield `-1` - the small-class dispatch the encoded-id
forwards resolve through.
Interior anchor `002CD948` (the offset-table load).

`002CA490` (226 B) is the state-change handler `003FDFE0`
and `0057B1A0` call: `byte[*(0209AC30) + 0xDE2]` picks a
17-arm image-relative jump table (`002CA574`) whose arms
either run `00291D70` directly or load a `0xC9D`..`0xCFA`
row id; when the state byte differs from its shadow at
`+0xDE3`, `002F9860` fetches that row and `00291D80`
applies it after the unconditional `00291D70(1)` - then
`+0xDE3` takes `+0xDE2`'s value - the
compare-fetch-apply-change sequence the query-record
state machine runs.
Interior anchor `002CA4C0` (the jump-table load).

## SWE2-EC7-101 update (2026-09-20) - `002AB870` measured

`002AB870` (115 B) is the eight-byte packed writer
`00293310` and the encoded-id arms call: `ecx < 8`
returns 0; otherwise `word[rdx]` takes tag `0x290F`,
byte 2 packs `r8d`'s bits 31/23/15/7 shifted left three
with `0x84`, bytes 3-6 take `r8d` byte-reversed each
`|0x80`, byte 7 terminates at 0, and the function
returns 8 - the tagged variable-length record the
id encoders emit.
Interior anchor `002AB878` (the `0x290F` store).

## SWE2-EC7-102 update (2026-09-20) - `0028E840` measured

`0028E840` (27 B) is the sibling `0209BE80` forward
`0027B880`, `00291D70` and `002BA700` call: a
nonnull root tail-jumps `002BE090` with
`rcx = root + 0x8FA0` and the `edx` argument - the
one-argument trampoline the record paths share.
Interior anchor `0028E84E` (the `+0x8FA0`
add).

## SWE2-EC7-106 update (2026-09-20) - `00252F40` measured

`00252F40` (40 B) is the bounded
query-row fetch `002826F0`,
`00282A40`, `002CCA40`, `003FCEE0`,
`00564430`, `00565CD0`, `0057B500`,
`0057CF20` and `0057D620` call: `ecx
> 0xB` reports `0016D6A0(0x200)` and
clamps the index to 0, then answers
`02092760 + movsxd(ecx) * 8` - the
eight-byte stride into the shared
query table with the over-range
notification in front.
Interior anchor `00252F55` (the
`movsxd`).

`0057CDD0` (57 B) is the zeroed-record-array alloc `0057CF20` uses: `002497E0(2, ecx*32)` reserves `arg` 32-byte records and `00861EC0` memsets them to 0 — returns the buffer, null on failure (the `002497E0` contract).

Interior anchor `0057CDF6` (function `0057CDD0`).

`0057AA00` (515 B) is the two-mode message composer `0057A620`/`0057AC10` call: `cl == 0` sends `003948B0(this, 002F9860(0x803), 0x21071, &rec)` with an optional 0x50-byte memset'd extension; `cl == 1` resolves a `0035D380(6, r8w)` object, `002B58B0`s its `+0x18`, then either `002B4090`s the `002F9860(0x854)` string or — when `00254A10` reports the simple path unavailable — walks `02EBF018`'s `+0x14` chain through `0020E600` twice to reach `[+0x194|+0x190]`-indexed text; `cl == 2` does the same compose via `002F9860(0xCF8)` + `002B40C0`. All paths end in `003949B0(this, text, &flagrec)` — the flag record carries `bts` bits `0xA`/`7`/`8` and tag `3`.

Interior anchor `0057AB91` (function `0057AA00`).

`002CCA00` (12 B) is the four-value kind-window predicate `00292B70` consults on the kind-3 arm (also reached from `0027F030`/`002826F0`/`00282A40`/`003FDFE0`): returns 1 iff `(ecx - 0x17)` unsigned is <= 3 — `ecx` in `0x17..0x1A` — else 0.

Interior anchor `002CCA05` (function `002CCA00`).

`005659B0` (71 B) is the `00D233A0` map's activate arm `00565E00` runs: `ecx` is kind-scanned over the 33-entry `{kind, slot}` word-pair table (a miss yields slot 0), `0209AC30 + slot·8 + 0x170` selects the object, and a non-null object tail-enters `002470D0(obj)`; null returns.

Interior anchor `005659F0` (function `005659B0`).

`00565190` (79 B) is the same `00D233A0` kind-to-slot lookup, forwarding arm: a resolved non-null object tail-enters `00564E10(obj, 1)` — the same function `00564300`/`00563EC0` serve — while a null slot returns 0.

Interior anchor `005651D7` (function `00565190`).

`00564A60` (87 B) is the same `00D233A0` lookup, probe arm: a resolved non-null object returns `[obj+0xE0]` != 0 — the live-child test; a null slot returns 0.

Interior anchor `00564AAE` (function `00564A60`).

`00563FC0` (77 B) is the same `00D233A0` lookup, release arm: a resolved non-null object with `[obj+0x7C]` bit 0x20 clear tail-enters `00244F00(obj)`; a set bit or a null slot returns.

Interior anchor `00564006` (function `00563FC0`).

`002FAE40` (114 B) is the bounded row-index lookup into `02EBF158` — the shop table — that `setshopname`'s `0034C170`, `002B9C70`, `002BA530`, `0057B890` and `0057C010` share: `word[+6]` is the row count (a null table reads as 0), `ecx >= count` returns 0, else `0020E600(dword[+8])` resolves the table base, `word[+4]` strides `ecx` rows in, and `word[row]` — the row's id word — is the return.

Interior anchor `002FAE73` (function `002FAE40`).

`003FDAD0` (769 B) is the query-record consumer `003FDFE0` calls: `002D45C0` x2, `002445C0` x3, `00282DF0`, `002C1A80`, `002D3900`, `00563EC0` x2, `00564300`, `002527B0`, `005655F0`, `005674B0` and `00249C60` run the record's emit - the query walker's wide helper stage.

Interior anchor `003FDB08` (function `003FDAD0`).

`0033D200` (475 B) is the record evaluator `00339F00`/`0033A720` call: `byte[[rcx+0x108]+0x177]` feeds `00236820`, `xmm[rbx+0xB0]` vs `+0x104`/`+0xE4`/`+0xE8` picks the xmm7 operand, `dword[rdi] & 0x7FE0` mode bits select the `00334120`/`00334220`/`0033CB70`/`004686D0` arms - the query record's float-path dispatch.

Interior anchor `0033D235` (function `0033D200`).

`002845E0` (472 B) is the flag rewrite `00283E40` calls: clears bit 0 of `[rax+0x40]+8` and `[rax+0x38]+8`, `byte[rbp+0xFC] & 8` gates, `byte[rcx+0xA1] = 0x80` marks, then `word[rsi+0x60]` sign plus `dword[rsi] & 0x20000`/`& 2` re-set `+8` bit 0 through `00247870`/`00247930`/`002C9BD0`/`002DD7E0` - the record's paired-flag update.

Interior anchor `002846AC` (function `002845E0`).

`003FD860` (435 B) is the three-word record copy `003FDFE0` calls: `002432B0(rcx+0x50, [0209AC30 + 0x40], 3)` resolves an id triple, `word[+4]`/`[+6]`/`[+8]`/`[+A]` land at `[rbx+0x98]`..`[rbx+0x9E]`, then `003FD360`/`00244F50`/`00244960`/`00567190`/`005674B0`/`005655F0` run the follow-up arms - the query record's id-write path.

Interior anchor `003FD89E` (function `003FD860`).

`003FD6B0` (426 B) is the id-record copy `003FDFE0` calls (sibling of `003FD860`, `r8d = 0` variant): `002432B0(rcx+0x50, [0209AC30 + 0x40], 0)` resolves, `word[+4]`/`[+6]`/`[+8]`/`[+A]` land at `[rbx+0x98]`.., `[rbx+0x60]` is read next, and `00254A10`/`0029FB50`/`003FD360`/`00567190`/`00244960`/`005674B0`/`00244F50`/`005655F0` run the follow-up arms - the query record's zero-count id write.

Interior anchor `003FD6E3` (function `003FD6B0`).

`003FCEE0` (251 B) is the four-class max sweep `003FF360` runs: the `{1,2}`/`{3,4}`-shaped `00D120C0`/`00D120D0` id pairs loop four rounds of `00252FA0(id)` count then `00252F40(id, i)` rows, each row's `[+4]` resolved by `0020E600` into a `word`-list whose entries `<< 0x10` pack the out record for `00292B70` validation and `002B3050` decode, `esi` accumulating the largest decoded s16 - the cross-class maximum the query table yields.

Interior anchor `003FCF36` (function `003FCEE0`).
