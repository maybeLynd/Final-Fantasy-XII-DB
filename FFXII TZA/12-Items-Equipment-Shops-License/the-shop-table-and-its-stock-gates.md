---
system: The shop table — 57 shops, each a ladder of stock lists gated on story progress or clan rank, bound to registry slot 02EBF158
category: 12-Items-Equipment-Shops-License
status: DOCUMENTED — every register row the page names is answered and its prose residue is closed (owner re-status 2026-10-01, OPUS, batch 22): the three list-interface questions are answered 2026-09-30 (OPUS 9c71391a8: GR-13 a shop row has one layout and its price is read at entry +0x10, GR-14 a shop list never receives message 26, so +0x10 is not rewritten, GR-15 the list kinds per widget family) and the body is corrected to them (FABLE 2026-09-30, shop-page-corrections-fable-0930); the shop table, the gate and the listing are read whole. Answered: the 57 name ids through npcdic.bin 2026-09-17 (UQ-132); row 24's runs 2026-09-27 (UQ-133: the vendor is first usable at story progress 3,100, so only entry 0 is ever gated); the rank counters' predicates are FG-1's, and no purchase path re-checks a gate (2026-09-30)
owner_layer: both
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 4 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "the us battle_pack.bin shop table (directory +0xA0: 57 rows, 267 stock entries, 2,512 item references) decoded in full through the class tables; every gate kind, threshold and item id tabulated, 2026-09-11"
last_reviewed: 2026-09-30
registry_slots:
  - "0x02EBF158"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-shop-table-pass-1
  crossref_clean: false
  reopened_count: 0
---

# The shop table — 57 shops, each a ladder of stock lists gated on story progress or clan rank, bound to registry slot 02EBF158

> **A shop's stock is a ladder.** Each of the 57 shops in `battle_pack.bin` is a name id and a list
> of stock entries ordered from the most demanding gate to the least; the menu finds the first entry
> whose gate the player meets and offers everything from that entry to the end of the ladder. A
> gate is one of three things: nothing, *story progress at least N*, or *clan rank at least N*. The
> twelve-tier shop that unlocks a line per clan rank, the five shops that each sell all 241 gambits,
> and the eight two-item stalls that share one name are all the same 8-byte entry shape.

**Corpus validation, before anything else.**

| | |
|---|---|
| file examined | `ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin`, directory entry `+0xA0` → the shop section at file offset `0x22418`: header `{u32 0x64, u16 stride 8, u16 count 57, u32 data 0xC}`, 57 rows |
| resolved | every stock list's item ids through the class tables of [the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.5; 267 entries, 2,512 ids |
| positive controls | row 3's first entry: gate *story ≥ 200*, six weapons starting Longsword (`0x1002`), Cypress Pole (`0x1037`); its base entry: four weapons starting Mace (`0x108B`); row 0's base entry: Eye Drops (`0x000A`), Potion (`0x0000`), Onion Bolts (`0x118C`) |
| censuses | gate kinds: 0 on 45 entries, 2 on 210, 3 on 12, kind 1 on none, `operandIndex` 0 everywhere; kind-2 thresholds 0, 145, 200, 500, 680, 960, 1090, 1240, 1330, 1380, 1580, 1740, 1982, 2100, 3050, 3100, 3210, 3250, 4150, 5100, 5300, 5350; kind-3 thresholds 1 … 12 on one row; ids by class: 267 items, 694 equipment, 4 loot (`0x2000` Teleport Stone, `0x20D8`), 214 magicks, 83 technicks, 1,250 gambits; five rows sell the 241 gambits in one ungated entry; eight rows carry name id `0x22D` |

## 1. What the player sees

Shops open more of their stock as the story advances — a weapon smith sells better blades after
the next chapter — and one shop unlocks a new line for every clan rank the player earns. Gambit
shops sell every gambit at once. Nothing a shop sells depends on what the player has bought before;
the stock is a function of two numbers.

## 2. Native mechanism

### 2.1 The binding — registry slot `02EBF158`, directory `+0xA0`

The `battle_pack.bin` binder `00236C30` handles this entry unlike its `st2e` siblings: it passes the
directory dword to `00238660` (`00236F28`–`00236F2E`), which **adds it to the slot** (`00238678`–
`00238686`; the slot is the only writer's target, so a zero slot becomes the section pointer) and
then walks the table converting every nested offset into an encoded runtime pointer through
`ImageAddress_ResolveRuntimePointer` (`0020E600`) and `RuntimePointer_EncodeImageAddress`
(`0020E620`): the header's data offset (`0023868D`–`002386B9`), each row's section (`00238713`–
`00238726`) and that section's data (`0023872E`–`0023875E`), each entry's list (`002387D2`–
`002387E5`) and each list's data (`002387E8`–`0023881D`). Three levels, all rebased once at load.
This is why the registry census saw one write and no `LEA` on the slot.

### 2.2 The three levels

```
shop table (at 02EBF158)          header {u32 tag 0x64, u16 stride 8, u16 count 57, u32 data}
  row[i]      (8 B)               {u32 nameId, u32 section}
    section                       header {u32 tag 0x164, u16 stride 8, u16 count n, u32 data}
      entry[j] (8 B)              {u8 gateKind, u8 operandIndex, u16 threshold, u32 list}
        list                      header {u32 tag 0x264, u16 stride 2, u16 count m, u32 data}
          id[k]  (2 B)            an encoded item id: 0x0000 items, 0x1000 equipment, 0x3000 magicks,
                                  0x4000 technicks, 0x6000 gambits, 0x2000 the class-7 rows
```

Every header is the same four fields the binder rebases; the tags `0x64` / `0x164` / `0x264` are
the only difference between the levels.

### 2.3 The name — `002FAE40(shopIndex)` and `setshopname`

`002FAE40(i)` returns row *i*'s first word (`002FAE4A`–`002FAEA4`: bounds test against the count,
row = data + stride × i). Its callers are the script verb **`setshopname`** (`0x4A9`, `0034C170`,
at `0034C18A`), which stores the word through `Actor_SetNameId` into the actor's `+0x102` — the
same id space `setnpcname` uses, resolved at display time by `Actor_GetDisplayName` →
`0032A930` → `003EAC10` ([the NPC-name dictionary](../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md)
§2.3) — and two readers that reach it through **one branch of a five-way name-source dispatch**
(`002B9C70` at `002B9CE7`, `002BA530` at `002BA5C8`, both then `0032A930`; the word `+0xE` is a
shop-row index **only** when that record's byte `+0xD` is 3 — §7's answered entry), and the shop menu
(`0057B890` at `0057B98F`, `0057C010` at `0057C022`). So **the row's first word is a dictionary
name id, not a text-bank reference** — the eight rows sharing `0x22D` share one displayed name (Assistant Storekeeper; every row's name is resolved in §7, UQ-132).

### 2.4 The gate — `002FAD40(row)` picks the first entry the player meets

`002FAD40` takes a row, reads its section (`002FAD56`) and walks the entries in order (`002FAD73`–`002FAE23`), returning the first that passes:

| `gateKind` | test | passes when |
|---|---|---|
| 0 | none (`002FADC8`–`002FADCA`) | always |
| 1 | `AiTargetSelector_ResolveOperandValue(3, 0, operandIndex, &v)` (`002FADD0`–`002FADDF`) | `v ≥ threshold` (`002FADE4`–`002FADEC`) |
| 2 | the same query with element **0** (`002FADF3`–`002FAE00`) | `v ≥ threshold` (`002FAE05`–`002FAE0D`) |
| 3 | `002536F0()` = the low byte of `00315390()` (`002FAE14`) | `rank ≥ threshold` (`002FAE19`–`002FAE1F`) |
| other | — | never (the entry is skipped) |

Kinds 1 and 2 read **the kind-3 authored-operand bank** — the `i16[256]` at save payload `+0x000`
([the payload map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)
§2.2) — through the selector's operand resolver. The shipped table uses only element 0 (kind 2),
and its thresholds rise monotonically from 145 to 5,350 across the game: **element 0 is the story
progress value**, which the shop data is the first consumer to name.

*The resolver, tied by instruction (2026-09-30, FABLE, Claude Opus 5.5).* The operand resolver is
`AiTargetSelector_ResolveOperandValue` (`00321190`). `002FAD40` calls it at `002FADDF` (kind 1) and `002FAE00` (kind 2),
with `ecx = 3` (`002FADDC` / `002FADFD`: `lea ecx, [rdx + 3]` after `xor edx, edx`), the entry's `operandIndex` or 0 in
`r8d`, and the answer slot `[rsp + 0x30]` in `r9`. The resolver subtracts one (`00321196`) and dispatches through its
ten-slot jump table, so operand kind 3 takes the third slot, the arm at `003211E4`. That arm passes `operandIndex` to
the bank's indexed getter, which returns 0 for an index of `0x100` or more. It then sign-extends the word it gets
(`003211EC` `movsx ecx, ax`) and stores it through `r9` (`003211F1`). The getter and its 256-entry bank are the actor
storage page's ([the record behind every actor](../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md)
§24, operand kind 3). So the story gate compares a **signed** 16-bit progress value against the entry's unsigned
`threshold` (`002FAE05`–`002FAE0D`).

Kind 3 is **the clan rank**: `00315390` walks a twelve-row table from rank 12 down (`003153B5`–
`003153DF`; rows of `{u32 points, u8 countA, u8 countB, u16}` at `00D105D0`, rank *r* at `+8(r−1)`)
and returns the first rank whose three thresholds the player meets — the dword `+0x3868` of the
block `002536A0()` returns (`0031539A`–`003153A4`) against the points, `00316480()` against
`countA` and `00316670()` against `countB` — else 1 (`003153E1`). The same function stamps the rank
into the save header (`SaveImage_FinalizeHeaderAndChecksum`, `00583F2A`). The shipped table:

| rank | points | countA | countB |
|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 |
| 2 | 700 | 2 | 0 |
| 3 | 8,000 | 4 | 0 |
| 4 | 20,000 | 8 | 0 |
| 5 | 30,000 | 10 | 0 |
| 6 | 40,000 | 12 | 0 |
| 7 | 100,000 | 14 | 0 |
| 8 | 200,000 | 16 | 0 |
| 9 | 250,000 | 24 | 0 |
| 10 | 300,000 | 28 | 0 |
| 11 | 500,000 | 32 | 0 |
| 12 | 1,000,000 | 44 | 30 |

The one twelve-entry ladder in the shop table (row 2) gates its lines at ranks 12, 11 … 1: one new
line per rank, the rank-12 line being twenty ids.

### 2.5 The listing — `002FA920(shopIndex, mode, …, out, category)`

`002FA920` is the menu's list builder (callers `0057B500`, `0057B6F0`, `0057CF20`; wrapper
`002FAD30`). **Mode 1** — a shop: it calls `002FAD40` on the shop's section (`002FA99E`–`002FA9AE`),
then walks the entries and, from the chosen one onward (`002FAABB`–`002FAACA`, the *reached* flag
reloaded at `002FAB89`), copies every id whose `ItemDefinition_ClassifyEncodedItemCategory` equals
the requested category into `out` (`002FAB4C`–`002FAB73`), returning the count. **No gate after
the chosen entry is tested again**: a ladder is cumulative downward, so the authored order is
most-demanding first and ungated last — which 56 of the 57 rows respect (row 24 is the exception,
§7). *"Ungated last" bears a footnote (2026-09-23, SWE2-CONTRACT, direct rescan): only **43** rows
end in a literal kind-0 entry; rows 17 and 18 end in a `k2@0` entry, which always passes; and
~~**12 rows are all-gated** — 2 (clan rank 1 minimum),~~ **11 rows are all-gated** (row 2's `k3@1` tail always passes, because the clan rank's floor is 1; corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 324) — 21, 22, 26, 27, 43, 44, 48, 49, 51, 54, 55
(story gates, minimums 500–3,250) — whose last line is still always offered because `002FAD40`'s
all-fail path returns the last entry rather than nothing (the CONTRACT's SG-2). So the last line
is effectively ungated everywhere; only 43 rows carry the gate-kind-0 marker for it.* **Mode 2** —
the bazaar: it lists every `0xD000`-class good whose runtime flag bit 1
is set (`002FA9C9`–`002FAA1C`; [the bazaar page](the-bazaar-recipe-unlock-and-purchase.md) §2.2).

### 2.6 What the shipped ladders look like

| shape | rows | reading |
|---|---|---|
| one ungated entry of 241 `0x6000` ids | 7, 28, 42, 47, 53 | the gambit shops — every gambit, always |
| twelve kind-3 entries, thresholds 12 → 1 | 2 | the clan shop: one line per rank; its rank-12 line is the 20-id list starting `003E`, `002B`, `002C` |
| one gated item over one or two base items, name `0x22D` | 29–36 | eight stalls with one displayed name, Assistant Storekeeper; row 36 sells Teleport Stone (`0x2000`) and, from 1,982, `0x20D8` |
| the identical seven-entry technick ladder `4007` @1982, `4016` @1380, `4014` @1240, `4002` @1090, `4005` @500, `4000` @145, `4013` base | 8, 41, 46, 52, 56 | five technick counters with one authored stock |
| one gated entry over one base entry | 3, 4, 10, 12, 23 … | weapon and armour smiths: better goods after a chapter (row 12's base entry is 99 ids, row 23's 3,050 line 71) |
| the same restorative ladder (`0002` @3250, `0014` @3100, `0010` @3050, `0001` @1330, `000E` @1240, `000D`+`0007` @680, `000B`+`000C` @500, `0006` @200, `0008`+`0009` @145) cut at different heights | 5, 9, 13, 25, 39, 50 | item shops that differ only in how far up the ladder they reach |

## 3. Key addresses

| Address | Name | Size | Role |
|---|---|---|---|
| `02EBF158` | — | 8 | the slot: the shop table's section pointer after `00238660` |
| `00238660` | — | 488 B | binds the slot and rebases the three levels of offsets |
| `002FAE40` | — | 114 B | `shopIndex → nameId` |
| `002FAD40` | — | 251 B | `section → first entry whose gate passes` |
| `002FA920` | — | 676 B | the list builder: mode 1 a shop's stock by category, mode 2 the bazaar |
| `002FAD30` | — | 8 B | wrapper into `002FA920` |
| `002536F0` | — | 17 B | `00315390` low byte — the clan rank |
| `00315390` | — | 94 B | the rank from clan points and two counts against the twelve-row table at `00D105D0` |
| `0034C170` | — | 88 B | the script verb `setshopname` |
| `00321190` | `AiTargetSelector_ResolveOperandValue` | 281 B | the operand resolver the kind-1 and kind-2 gates call with operand kind 3 (§2.4) |
| `00316480` | — | 289 B | the rank's quest count `countA` (§7, FG-1) |
| `00316670` | — | 126 B | the rank's award count `countB`, a 30-bit sweep of block `+0x3844` (§7) |
| `0046B1A0` | — | 73 B | quest-clear bit `n` of payload `+0x1020`; `countA`'s first test |
| `002FEEB0` | `Shop_CommitPurchaseItemAndGil` | 121 B | the purchase commit: adds the item, pays the gil; no gate test (§5) |
| `0056D370` | — | 1,274 B | the shop transaction driver: reads a list row's id and price and commits a purchase or a sale (§5) |
| `00236C30` | — | the `battle_pack.bin` binder | passes directory `+0xA0` to `00238660` |

## 4. Data structures and formulas

```c
struct ShopTableHeader { u32 tag; u16 stride; u16 count; u32 data; };   /* tag 0x64, 0x164, 0x264 */
struct ShopRow         { u32 nameId; u32 section; };                    /* 57 of them */
struct ShopStockEntry  { u8 gateKind; u8 operandIndex; u16 threshold; u32 list; };
/* list: ShopTableHeader (stride 2) followed by u16 encodedItemId[count] */

ShopStockEntry *shop_first_open_entry(ShopRow *row)  /* 002FAD40: returns an ENTRY POINTER (rbx), not an index */
{
    ShopSection *s = row->section;
    ShopStockEntry *e = NULL;                          /* 002FAD4F xor ebx, ebx */
    for (int j = 0; j < s->count; j++) {               /* count = word [section + 6], 002FAD6B; test 002FAD73 */
        e = entry(s, j);                               /* data + stride * j, 002FADB8-002FADBF */
        switch (e->gateKind) {
        case 0:  return e;
        case 1:  if (operand(3, 0, e->operandIndex) >= e->threshold) return e; break;
        case 2:  if (operand(3, 0, 0)               >= e->threshold) return e; break;   /* story progress */
        case 3:  if (clan_rank()                    >= e->threshold) return e; break;
        }
    }
    return e;           /* every gate failed: the LAST entry (SG-2); an empty section: NULL */
}
/* the listing then matches that pointer and copies ids from it through the last entry, filtered by category */
```

*Corrected 2026-09-30 (FABLE, Claude Opus 5.5).* This block used to return the index `j` and end with
`return s->count; /* nothing offered */`. Both were wrong, and §2.5 already said so: "`002FAD40`'s all-fail path returns
the last entry rather than nothing (the CONTRACT's SG-2)". Read against `002FAD40`: `rbx` is zeroed once (`002FAD4F`),
set to each entry as the loop reaches it (`002FADB0`, `002FADBF`), and returned by the only exit (`002FAE2D`
`mov rax, rbx`). The loop test `002FAD75 jge 002FAE28` leaves with the last entry still in `rbx`, and a section with no
entries returns null. The listing then matches the pointer, not an index
([CONTRACT-shop-stock-ladders.md](CONTRACT-shop-stock-ladders.md): its first invariant, one evaluation carried by pointer, and SG-2).

## 5. Call chain

```
battle_pack.bin bind: 00236C30 -> 00238660(dir+0xA0) -> 02EBF158 (+ nested offsets rebased)
name:   script setshopname (0x4A9) -> 0034C170 -> 002FAE40(i) -> Actor_SetNameId -> +0x102
        menu 0057B890 / 0057C010 -> 002FAE40(i) -> 0032A930
stock:  menu 0057B500 / 0057B6F0 / 0057CF20 -> 002FA920(i, 1, .., out, category)
                                             -> 002FAD40(section) -> 00321190 / 002536F0
bazaar: the same builder, mode 2 -> BattleIdClassD_GetRuntimeFlagBit1
buy:    transaction driver 0056D370 -> row = list[+0xC8] + index * 0x20       (0056D55D-0056D56F)
          -> price = dword[row + 0x10] & 0x7FFFFFFF, times the quantity (0056D461-0056D46C)
          -> sale: Shop_CommitSaleItemAndGil (0056D478) | purchase: Shop_CommitPurchaseItemAndGil 002FEEB0 (0056D49A)
```

*Call chain filled in 2026-09-30 (FABLE, Claude Opus 5.5).*

**Upstream (who causes this).** The owner transition is the bind: `00236C30` hands directory `+0xA0` to `00238660`, once
per `battle_pack.bin` load (§2.1). After that, three things trigger reads, and none of them changes the table:
- a field script's `setshopname`, which names an actor (§2.3);
- a map marker whose byte `+0xD` is 3, which names a marker row (§7);
- the shop menu's list builders (`0057B500`, `0057B6F0`, `0057CF20`, and `0057D620` through the wrapper `002FAD30`).

**The gate queries, tied.** `002FAD40` has one call site in the image, `002FA9AE` inside the listing (the stock-ladder contract's first invariant). For kinds
1 and 2 it calls `00321190` (`002FADDF`, `002FAE00`), whose operand-kind-3 arm reads the story bank (§2.4). For kind 3
it calls `002536F0` (`002FAE14`), the low byte of the rank walk `00315390`.

**Downstream (what this causes).** A listing is a `0x20`-byte-per-row list (§ "The list-kind selector" below). The shop
transaction driver `0056D370` (the bazaar contract's name for it) points `+0xD0` at the chosen row of the list it holds at
`+0xC8` (`0056D55D`–`0056D56F`). On confirm it takes the row's price, `dword[row + 0x10]`, clears bit 31
(`0056D468 btr ebx, 0x1f`) and multiplies by the quantity word `+0xDC` (`0056D46C`). The product goes to the sale
commit when bit 0 of its mode word is set (`0056D46F`, `0056D478`), and otherwise to the purchase commit with the row's
id `word[row + 8]` (`0056D464`, `0056D49A`).

**No purchase path re-checks a gate** (read 2026-09-30, answering the question the crossing section below left). The
purchase commit `Shop_CommitPurchaseItemAndGil` (`002FEEB0`) makes five direct calls: the inventory writer, the gil getter,
the gil setter, the gil notifier and the bazaar entry reset (`002FEEDB`–`002FEF0A`). None of them is the gate walker or
one of its queries, and a forward closure over the image's direct `E8`/`E9` calls from `002FEEB0` (637 functions) reaches
neither `002FAD40`, `00321190`, `002536F0` nor `00315390`. The driver itself reaches the gate only by rebuilding a list
(`0056D660` into a list refresh that ends in `0057CF20` → `002FA920` → `002FAD40`). That rebuild re-lists; it does not
test the id being bought. **So a purchase trusts the list: the gate is applied once, when the list is built.** *Bound:*
direct calls only. An indirect call would not be seen, and none of the five commit callees was read for one.

## 6. Modding notes

- **Adding stock** is adding ids to a list; the counts are in the list header and the offsets are
  file-relative until `00238660` rebases them, so a rebuilt section must keep every offset
  consistent at all three levels.
- **Gating on a new counter** is possible with kind 1: `operandIndex` selects any element of the
  kind-3 bank, not just element 0 — the shipped table never uses it.
- The ladder must stay ordered most-demanding first: the selector stops at the first pass and lists
  everything after it.

## 7. What is not known

- [x] ~~**UQ-132.** The 57 name ids are dictionary ids (`0x25B`, `0x270`, `0x79`, `0x22D` × 8 …); they are not~~
      ~~resolved here, so which shop is which is known only by shape.~~
      ***ANSWERED 2026-09-17 (FABLE): the 57 name ids resolve through `npcdic.bin`, and the names say what each row is.** Reading the `us` dictionary (`NPC0`, 2,282 entries: entry 2 × id is a pair's first name and 2 × id + 1 its second, per [the NPC-name dictionary page](../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md) §2.2) at each row's first word gives, row by row: 0 and 1 Traveling Merchant (`0x25B`, `0x270`); 2 Clan Provisioner (`0x79`); 3 Weapons of War; 4 Antiqued Armors; 5 Portentous Provisions; 6 Mysterious Magicks; 7 Morning Star Gambits; 8 Troublesome Technicks; 9 Unlucky Merchant; 10 Desert Merchant, second name Lohen; 11 Nomad, second name Arjie; 12 Burrogh; 13 Street Vendor; 14 and 20 Tetran (`0x2B9`); 15, 17 and 18 Dyce (`0x2E6`); 16 Baknamy Merchant; 19 Garif Trader; 21 and 22 Traveling Merchant (`0x1D8`, `0x1D9`); 23 Caravaner, second name Luccio; 24 Vendor of Goods (`0x1F9`); 25 Stranded Merchant; 26 The Leapin' Bangaa; 27 Quayside Magickery; 28 Waterfront Gambits; 29 to 36 Assistant Storekeeper (`0x22D`); 37 Amal; 38 Panamis; 39 Shop Clerk; 40 Yugri; 41 Batahn; 42 Yamoora; 43 Targe; 44 Rithil; 45 Mait; 46 Clio; 47 Bashketi; 48 Weapon Seller; 49 Armor Seller; 50 Granch; 51 Magickery Proprietor; 52 Technick Seller; 53 Lebleu's Daughter; 54 Beruny; 55 Emma; 56 Odo. Forty-seven distinct ids; fifty-four rows' pairs repeat the first name, and only rows 10, 11 and 23 carry a reveal (the persistent flag with the pair's number shows Lohen, Arjie and Luccio). The names match the shapes §2.6 reads: the five one-entry gambit rows are Morning Star Gambits, Waterfront Gambits, Yamoora, Bashketi and Lebleu's Daughter; the five identical technick ladders are Troublesome Technicks, Batahn, Clio, Technick Seller and Odo; the six restorative ladders are Portentous Provisions, Unlucky Merchant, Street Vendor, Stranded Merchant, Shop Clerk and Granch; the clan ladder is the Clan Provisioner; the eight `0x22D` stalls are the Assistant Storekeepers; row 24, the UQ-133 exception, is the Vendor of Goods. Which town each row stands in is authored by the field scripts' `setshopname` calls, which this page does not census, so the names, not the places, are what is resolved here. DATA: the `us` pack and dictionary decoded; the reader chain is static.*
- [x] ~~Which counters `00316480` and `00316670` return for the rank test (`countA` reaches 44 at
      rank 12, `countB` is only required there, at 30).~~
      **ANSWERED 2026-09-13 (OPUS): they count different populations, and that is the whole
      asymmetry — `countA` is sized by data, `countB` is fixed at thirty.**

      **`00316670` → `countB`, a fixed 30-entry sweep.** `edi` runs `0`…`0x1E` (`inc edi` at
      `003166CB`, `cmp edi, 0x1E` at `003166D7`), and each iteration reads a byte at
      `[rcx + rax + 0x3844]` and tests it against ~~a mask from `002536A0` — the same block-state
      function §5 already cites for the points test~~ the mask `1 << (i & 7)` (`003166B7`–`003166C1`), where `rcx`
      is the block `002536A0` returns (`0031669D`–`003166AF`). *Corrected 2026-09-30 (FABLE, Claude Opus 5.5):
      `002536A0` supplies the block pointer (`qword [020927C0]`, 8 bytes), not a mask, and it is §2.4 that cites it
      for the points test, not §5.* **`countB` cannot exceed 30 because the loop
      has thirty iterations**, which is exactly why it "is only required there, at 30": the gate asks
      for every entry it is capable of counting.

      **`00316480` → `countA`, sized by the table's own header.** It loads the static `022C2550`,
      walks to `+8`, and bounds the loop with `cmp ax, word ptr [rcx + 2]` (`0031650C`) — **a `u16`
      count stored in the structure**, not an immediate. Each iteration takes a byte from an array of
      2-byte entries at `+4` (`movzx ecx, byte ptr [rcx + rax*2 + 4]`) and counts the entry when
      `0046B1A0` accepts it. **So 44 at rank 12 is a property of the shipped table, not of the code**,
      and a reconstruction must read the count field rather than hard-code 44.
      `022C2550` is already documented elsewhere as a static walked by a relative-offset chain — see
      [event memory at actor bind](../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md) —
      and the [achievement-counters contract](../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md)
      records that the two counters are *"named and bounded"* but not specified. **This narrows that:
      one bound is the table's count field and the other is the literal 30.**
      ~~**Not established:** what `0046B1A0` accepts, and what the `+0x3844` byte and the `002536A0`
      mask mean. **The populations are read; the predicates are not.**~~
      ***Corrected 2026-09-30 (FABLE, Claude Opus 5.5): the predicates are read, in FG-1 (ANSWERED 2026-09-27, OPUS),
      and this page had not caught up.*** `0046B1A0(n)` returns bit `n` of the persistent payload's quest-clear bank
      at `+0x1020`: byte `n >> 3`, bit `n & 7` (`0046B1AA`–`0046B1E0`). `00316480` counts an entry
      `{questId, minimum}` when that clear bit or the quest-order bit (`0046B240`) is set, **and** the quest's
      scenario flag (`0046B180`) is at least `minimum` (`00316520`–`0031654D`). The walked table is the
      `menuhandbook.bin` node bound at `[022C2550]`: 45 entries, quest ids 128–172, so rank 12's 44 is 44 of those
      45. The `+0x3844` bytes are a 30-bit set, the achievement layer's award bitmap
      ([the achievement-counters contract](../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md)), so
      `countB` is the number of awards earned, and rank 12 asks for all thirty. Source:
      [the save payload field map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)
      §7, FG-1. The mask is the one corrected above.
- [x] **UQ-133.** **Row 24** (name `0x1F9`, 39 entries) is three descending runs, each ending in an ungated
      entry; because the listing never re-tests a gate after the chosen entry, a player who meets
      only the first run's lowest gate is also offered the later runs' gated lines. Whether that
      shop is reachable only after those gates are met, or the authoring relies on it, is not
      established.
      ***NARROWED 2026-09-18 (FABLE), DATA from the row itself: the runs are per-class ladders, and every gate after entry 15 is dead.** Decoding row 24's 39 entries (`battle_pack.bin` shop section, row 24 at section `+0x1338`, entries at `+0x1344`, every gate kind 2 = story progress) gives six descending ladders laid end to end, one per top nibble of the goods: entry 0 an accessory alone (Diamond Armlet at 5,100); entries 1-2 weapons and armour in two bundles (13 at 3,100: Diamond Sword to Crystal Shield; 14 at 3,050: Bastard Sword to Dragon Shield; names from battle text bank 1); entries 3-8 six nibble-3 goods bundles (3,100 down to 1,580); entries 9-15 seven nibble-4 goods (1,982 down to 145, then entry 15 ungated); entries 16-29 fourteen accessories (Power Armlet at 3,100 down to Argyle Armlet at 200, then Bangle ungated); entries 30-38 nine item bundles (3,100 down to 145, then two items ungated). Within each ladder the thresholds descend, which is the rule the other 56 rows follow for their whole row: the authoring wrote row 24 as if each class were scanned on its own. The engine scans once: `002FAD40` returns the first passing entry and entry 15 is ungated, so the chosen entry is never past 15 and the thresholds on entries 16-38 (3,100 on Power Armlet, 3,100 on the item bundle at entry 30, and the rest) are never consulted. What the vendor offers is therefore: below progress 145, entry 15 plus every accessory and every item bundle (entries 16-38, 23 lines); from 145 upward the nibble-4 ladder opens from its lowest gate, and each higher gate adds the entries after it, so a player at 3,050 is offered entries 2-38, which includes entry 3's 3,100 bundle since it sits below entry 2. Still open: where the Vendor of Goods stands (the marker records that carry a shop row are built at runtime from the field's element arrays, `00402000` over `003DFB50`, and were not searched in the archive), so whether the field is reachable before those gates is not established.* *(2026-09-30, SWE2-STRUCT for OPUS: answered - the next two paragraphs: the vendor stands in field `fon_b01` (2026-09-18), and UQ-133 is ANSWERED 2026-09-27: it is first usable at story progress 3,100, after every gate from 145 to 3,100 is met.)*
      **Narrowed 2026-09-18 (FABLE), by a census of the shipped field scripts: the Vendor of Goods stands in field `fon_b01`.* All 769 `us` `plan_map` scripts were extracted from their `EBP2` containers (the header dword at `+0x10` is the script section's offset, the section's own second dword its length, magic `0x8000000B`) and decompiled with `ff12-script -d`; every `setshopname` call was recorded with its argument push. There are **127 calls: 75 with a literal row and 52 whose row is a file variable masked with `0xFFF`** (a per-map data value, not placeable statically). **Row 24 has exactly one literal binding**: `fon_b01`, inside an actor's `BEFORE_SET` — `setpos`, `dir`, `bindp2_d4`, `stdmotionread` / `play`, `reqenable 2`, `setweight -1`, **`setshopname 0x18`**, `setoverheadicontype 1` — with no condition around it, so the vendor exists whenever that field's actor is enabled. Every other literal row from 0 to 47 is bound once to four times, the eight Assistant Storekeeper rows 29–36 four times each. What the database does not hold is the field's first visit in story-progress terms (`fon_b01` appears only in the voice-cue census as an event key), so whether the ladder's gates at 145..3,100 are already met when a player first reaches the vendor is a story-counter fact this census cannot settle; the row's gate mechanics stay as decoded above. DATA: the archive's scripts, decompiled; the binding read in the assembly listing.*
      ***ANSWERED 2026-09-27, FABLE, Claude Opus 5.5, DATA: the vendor is first usable at story progress 3,100.** `fon_b01`'s `main(1)` plays its arrival event whenever the story counter is at most 3,070, and three of its actor functions then set the counter to 3,100; across all 1,114 decompiled scripts nothing writes a value from 3,071 to 3,099, so the counter never stands in that gap. At 3,100 the scan's first passing entry is entry 1 (3,100), so from the first contact the vendor offers entries 1-38; entry 0, the Diamond Armlet at 5,100, joins when normal play reaches 5,100 (field `gil_d01`). Every gate from 145 to 3,100 is therefore met before the vendor can be spoken to, and the per-class ladders are invisible to a player. Debug scripts can set any value; native writes of the counter are not censused. [Record and control](../_index/candidates/uq133-first-visit/README.md) (6 checks, FAILS 0).* *(2026-10-01, SWE2-STRUCT for OPUS, DD batch 21: "native writes of the counter are not censused" is a stated limit of this answer, not an open question. The answer rests on the script census, so it holds for script writes; UQ-133 is ANSWERED with that limit. [Record](../_index/candidates/swe2struct-ddres-b21-1001/README.md).)*
- [x] ~~Which records `002B9C70` and `002BA530` read the shop index from (word `+0xE`).~~
      **ANSWERED 2026-09-13 (OPUS): they are map markers, and the premise is wrong — word `+0xE`
      is not a shop index. It is an id whose *id space is chosen by byte `+0xD`*, and the shop
      table is one of five sources.**

      Both functions carry the **same five-way dispatch** on `movsx ecx, byte [rec+0xD]`
      (`002B9C76`–`002B9C93`; `002BA573`–`002BA589`), and every branch returns a **string pointer**:

      | `+0xD` | the id space word `+0xE` is read in | the chain |
      |---:|---|---|
      | **1** | the **field/map name** table | `00377B60` = `MapName_GetFieldNameById` ([field record table](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md), `MapName_GetFieldNameById`, 45 B) |
      | **2** | the **NPC name dictionary**, the *same* word used as id **and** as flag number | `0032A930(w)` then `0026DEA0(w, flag)` |
      | **3** | **this page's shop rows** | `002FAE40(w)` → row's name id → `0032A930` → `0026DEA0` |
      | **4** | the **string pool** directly | `002F9860(w)` |
      | *other* | word **`+0x8`** (the marker's type) through a 14-entry map | `00916A10` → `002F9860`; **0** if the type is absent |

      The fallback map at `00916A10` is exact and contiguous — types `16, 1…10, 13, 12, 15` (11 and
      14 unused) to string-pool ids **`0x187F`–`0x188C` (6271–6284)**, in that order, so a marker
      with no explicit name shows a per-type caption.

      **Where the records come from.** `00402000(rows, mapDesc)` builds the array both readers walk
      (`00402088`–`004021C6`). It does not create the records: it walks **ten categories** (`ebp`
      `0`…`9`, category 9 skipped, `004020A0`) of an existing container — `003DFBB0(c, cat)` counts,
      `003DFB50(c, cat, i)` fetches, `003FFF40(rec)` validates — and keeps a record only if its
      position passes a **map-visibility test**: `00255150` against the descriptor `00403F90` fills
      (`0040204C`), which [the save payload field map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)
      already names as one of the readers that *"draw the map from the copied entry"*. Marker x/y
      are `word +0x0` / `+0x2` in **1/16 units**, shifted to cells at `0040214E`/`00402157`. Flag
      `0x200` in `[mapDesc+0x28]` skips the test entirely (`00402028`, `r13 = 0`), and types `0x14`,
      `0x17`, `0x18` are exempt from it (`0040210E`–`00402120`).

      **The row is 24 bytes** (`add rsi, 0x18`, `004020D4` + `00402199`): `+0x00` the record pointer,
      `+0x08` its category, `+0x0A` its index, `+0x0C` `0xFFFF`, back-patched with the index of a
      following **type-`0xE`** record, which gets no row of its own and instead annotates the marker
      before it (`00402163`–`00402174`).

      **The two readers are the two halves of one list.** `002BA530(rows, n)` resolves *every* row
      and returns the **widest** measured at scale `1.0f` (`0029CD00`, `002BA61C`–`002BA620`) — a
      column-width pass; `002B9C70` resolves **one** row, and its caller `002BD8C0` stores the
      string at `[dst+0x18]` with its handle at `[dst+0x20]` (`0020E620`, `002BD908`). That caller
      indexes `rcx + (r9d + 8) × 0x18`, and **`8 × 0x18 = 0xC0`** — precisely where `002BA310` put
      the rows inside the `0x3E0`-byte widget it builds through the widget factory `00244F50`
      (`002BA376`, count at `+0x3D8`), so `rcx` is the widget and `r9d` the row index. **33 rows
      fit** between `+0xC0` and `+0x3D8`.

      **What this does not establish:** which screen the widget is, and what the ten categories and
      the type codes at word `+0x8` are. That is map/UI territory, not this page's — **routed, not
      claimed.** What is settled here is the only part this page asserted: the shop table is reached
      from exactly one of five branches, and `002FAE40` is never called with a raw `+0xE` word
      except under `+0xD == 3`. *(2026-10-01, SWE2-STRUCT for OPUS, DD batch 21, static: the screen is now read. `002BA310` has one caller, the location map's page procedure `002BAF80`, at `002BB836` inside its confirm-on-marker arm, and `002BD8C0` and `002BA530` are reached only from `002BA310`. So the widget is the `0x3E0`-byte child page the location map opens on a kind-0 marker ([the map screens](../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md), "Kind 0"). What the ten categories and the `+0x8` type codes are stays with that page: a stated boundary here. [Record](../_index/candidates/swe2struct-ddres-b21-1001/README.md), checks M1-M6.)*
- [x] **What `0046B1A0` accepts, and what the `+0x3844` byte and the `002536A0` mask mean** — **answered in FG-1**
      (2026-09-27, OPUS); reconciled here 2026-09-30. See the corrected countA/countB entry above.
- [x] **Whether any purchase path re-checks the gates** — **no, read 2026-09-30 (FABLE):** see §5, "No purchase path
      re-checks a gate". The bound is direct calls.
- [x] **What consumes price bit 31** — **partly read 2026-09-30 (FABLE).** For a layout-A row (id `+8`, price `+0x10`),
      the transaction driver clears it (`0056D468`) before multiplying, on both the buy and the sell path. ~~The layout-B
      half is GR-13.~~ There is no layout B (GR-13); in sale mode the sale test `0056E700` reads the bit as "cannot be sold" (the list-kind section, the bit-3 note) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 1; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*.
- [x] **GR-13.** Who reads the price of a layout-B row (`0057DAD0`: price at `+8`, bit 31 as the zero-price sentinel),
      and whether a layout-B list ever reaches the transaction driver, which reads layout-A offsets. Selector `0x1B`
      (shop category 7) is on both head arm 1 and tail arm 3, the `0057DAD0` arm, ~~so the question is live for shop stock~~: tail arm 3 sets the zero-price flag `0x20` for selector `0x0F` only (`0057D3F0` `cmovne`), the Sell tab's loot row, so this reason does not hold for the Buy tab *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 5; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*.
      *(Answered 2026-09-30, OPUS `9c71391a8`; register row GR-13, record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md): the premise does not hold - read entry-relative, `0057DAD0`'s rows carry name `+0`, id `+8`, count `+0xC` and price `+0x10` like the other fillers, so the price shown and the price paid come from the same slot. The record lists six statements on this page that follow from the cursor-relative reading, for the page owner.)*
- [x] **GR-14.** Whether the list widget's message-26 layout write (a mode byte at `+0x10`, words at `+0x12` and
      `+0x14`) ever lands on a list before that list reaches the transaction driver's price read. This replaces the
      "not establishable by this method" bound below: a price reader now exists, so the question is one of order.
      *(Answered 2026-09-30, OPUS `9c71391a8`; register row GR-14: no. Message 26 reaches only the inventory menu's lists; the shop's Buy, Sell and Bazaar lists never receive it, so on a shop list `+0x10` is the price from build to purchase.)*
- [x] **GR-15.** Which list kinds each widget family is constructed with. Both `+0x17F` writers take the kind from a
      register (the declared blind spot below). *(Answered 2026-09-30, OPUS `9c71391a8`; register row GR-15: every family takes the kind from a constant table except the equip screen, which passes its slot index - the inventory menu's eight categories, the shop's Buy / Sell / Bazaar tabs (kinds 32, 19, 31) and the equip screen's five slots.)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the slot is bound by adding the directory dword, then rebased at three levels | `00236F28`–`00236F2E`; `00238678`–`00238686`; `0023868D`–`0023881D` | 1 |
| the name reader, `setshopname`, and the two direct name resolvers | `002FAE4A`–`002FAEA4`; `0034C18A`; `002B9CE7`; `002BA5C8` | 1 |
| the two resolvers dispatch five ways on the record's byte `+0xD`, and the shop table is branch 3 | `002B9C76`–`002B9C93` and its five arms `002B9CD5`/`002B9CE3`/`002B9D03`/`002B9D1C`/`002B9C95`; `002BA573`–`002BA589` and `002BA5B9`/`002BA5C4`/`002BA5E1`/`002BA5F7`/`002BA58B` | 1 |
| the fallback maps marker type word `+0x8` to fourteen contiguous string-pool ids | the 14 × 4-byte table at `00916A10` read from the image: keys `16, 1…10, 13, 12, 15` → `0x187F`…`0x188C` | 1 |
| the records are map markers filtered by map visibility, not shop rows | `00402028` (`[desc+0x28] & 0x200` bypass); `0040204C` (`00403F90` fills the descriptor); `0040210E`–`00402161` (type exemptions, then `00255150` on cells from `word +0x0`/`+0x2` at `0040214E`/`00402157`) | 1 |
| the 24-byte row and the widget it lives in | `004020D4` + `00402199` (stride `0x18`); `00402185`–`00402190` (the four written fields); `00402163`–`00402174` (type `0xE` back-patches `+0x0C`); `002BA376` (`00244F50(0x3E0, 002BD680)`), rows at `+0xC0`, count `+0x3D8`; `002BD8D2`–`002BD8E3` indexes `+ (r9d + 8) × 0x18` | 1 |
| the gate kinds and their queries | `002FADC5`–`002FAE23` | 1 |
| the rank walk, its table and its thresholds | `0031539A`–`003153E1` | 1 |
| the listing is cumulative from the chosen entry and filtered by category | `002FA99E`–`002FAB78` | 1 |
| mode 2 lists the bazaar's flag-bit-1 goods | `002FA9C9`–`002FAA1C` | 1 |
| every row, entry and id of the shipped table | the `us` section at `0x22418`, decoded through the class tables | data |
| the gate walk returns an entry pointer, the last entry when every gate fails, null for an empty section (§4 corrected) | `002FAD4F`, `002FADB0`/`002FADBF`, `002FAD75`, `002FAE2D`; SG-2 in the stock-ladder contract | 1 |
| kinds 1 and 2 read operand kind 3 through `00321190`'s third jump-table slot and sign-extend it | `002FADDC`/`002FADDF`, `002FADFD`/`002FAE00`; `00321196`, `003211E4`–`003211F1` | 1 |
| `countB` tests bit `i & 7` of block `+0x3844`; `002536A0` is the block pointer | `0031669D`–`003166C1`; `002536A0` is 8 bytes, a load of `qword [020927C0]` | 1 |
| `0046B1A0(n)` is bit `n` of payload `+0x1020`; `countA`'s predicate | `0046B1AA`–`0046B1E0`; `00316520`–`0031654D`; FG-1 | 1 |
| the transaction driver reads a row's price at `+0x10`, clears bit 31, multiplies by the quantity | `0056D55D`–`0056D56F`, `0056D450`–`0056D46C`, `0056D478`, `0056D49A` | 1 |
| the purchase commit tests no gate | `002FEEB0` read whole (five direct calls); forward closure over direct calls from it, 637 functions, none of the gate family | 1 (direct calls only) |
| after a transaction the driver reports achievement counter 19 (every purchase, the row's id) or counter 14 (a sale, the quantity, when `+0xE4` bits 6-13 are 7) (added 2026-09-30, SWE2-STRUCT for OPUS) | `0056D46F`–`0056D4D2`; `00316A81`–`00316AD3`; descriptors 19 and 14 at `00D10460`; records at `01DFE410`; `b11_struct.py` S1–S5 in [`swe2struct-ddres-b11-0930`](../_index/candidates/swe2struct-ddres-b11-0930/README.md) | 1 |

## 9. Related

- [`authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) — the slot and the binder.
- [`the-encoded-id-space-and-the-query-record.md`](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) — the id classes the lists use.
- [`the-bazaar-recipe-unlock-and-purchase.md`](the-bazaar-recipe-unlock-and-purchase.md) — mode 2 of the same list builder.
- [`the-npc-name-dictionary.md`](../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md) — where the name id resolves.
- [`the-save-payload-field-map.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) — the kind-3 operand bank the story gate reads.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

The section was re-decoded from `battle_pack.bin` without reading the prose, and **every corpus
figure reproduces**.

| claim | measured |
|---|---|
| directory `+0xA0` → file offset `0x22418` | **`0x22418`** |
| the table header | tag **`0x64`**, stride **8**, count **57** |
| the three levels' tags | **`0x64`** once, **`0x164`** on all **57** sections, **`0x264`** on all **267** lists — no other tag anywhere |
| 57 shops / 267 stock entries / 2,512 item references | **57 / 267 / 2,512** |
| gate kinds `0` on 45, `2` on 210, `3` on 12, `1` on none | **45 / 210 / 12 / 0** |
| `operandIndex` 0 everywhere | **0 on all 267** |
| the 22 kind-2 thresholds | `0, 145, 200, 500, 680, 960, 1090, 1240, 1330, 1380, 1580, 1740, 1982, 2100, 3050, 3100, 3210, 3250, 4150, 5100, 5300, 5350` — **all 22, in order** |
| "the eight rows sharing `0x22D`" | **8**, out of 47 distinct name ids over 57 rows |
| "five shops that each sell all 241 gambits" | **five shops carry exactly 241 each**, and 241 is the complete distinct gambit set in the table |

### The file-side offset convention, which a re-decoder needs

§2.1 describes what the *binder* does — three levels rebased through `0020E600` / `0020E620`. On the
file side the rule is simpler and is not stated: **every nested offset is relative to the section
base**, not to the header that carries it. The row's `section`, each section's `data`, each entry's
`list` and each list's `data` are all `sectionStart + offset`. Reading any of them as relative to its
own header walks off the file, which is how this pass first failed.

### Two counts the page gestures at but does not make

**The 2,512 references by class nibble** — §2.2's comment names the six id spaces and never counts
them:

| nibble | `0` items | `1` equipment | `2` class-7 | `3` magicks | `4` technicks | `6` gambits |
|---|--:|--:|--:|--:|--:|--:|
| references | 267 | **694** | 4 | 214 | 83 | **1,250** |

summing to **2,512** exactly — so more than half of every shop reference in the game is a gambit, and
the nibble-`2` space appears just **four** times.

**⚠ Gambits are in six shops, not five.** Five carry all 241; a **sixth carries 45** of them
(`5 × 241 + 45 = 1,250`). The sentence "the five shops that each sell all 241 gambits" is true as
written — five shops do — but it reads as the whole gambit story and is not.

**Not claimed:** §2.3's name-dictionary route and its five readers, §2.4's gate walk, and the mapping
of which shop is which were not re-derived. The `in`/`kr` copies were not decoded. Nothing was
executed or observed live. *(2026-10-01, SWE2-STRUCT for OPUS, DD batch 21, data: the `in` and `kr` copies are now decoded, with the other seven. All nine `battle_pack.bin` packs in the archive (`us`, `de`, `fr`, `es`, `it`, `in`, `kr`, `ch`, `cn`) hold the same shop table: 57 rows, 267 entries and 2,512 references, row for row and id for id, although the files differ and the table sits at a different offset in each. So the counts above hold for every language. [Record](../_index/candidates/swe2struct-ddres-b21-1001/README.md), checks V1-V7.)*

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `00565720` | 656 | license/shop widget worker — called by `005651E0` (license family): `[rcx+0xE0]`, `[rdi+0xE0..0x180]`, `003697F0`, `0057CF20`, `002D1820`, `002D47C0` |
| `0057D620` | 1088 | stock-list worker (caller `0057D610`): `0057CE10`, `00252F40`/`00252F70`/`00252FA0` family, `002FAD30` x2, `0020E600`, `0057DED0` |

## The list-kind selector — what `0057CF20` and `0057D620` actually take — 2026-09-20 (FABLE, Claude Opus 5)

*§5's call chain gives `0057CF20` one line — `menu 0057B500 / 0057B6F0 / 0057CF20 -> 002FA920(i, 1, .., out,
category)`. That line is true and it is **one arm of five**. What follows is the rest of the same function, and it
explains why the shop categories are what they are.*

**The argument is packed, and its low half is a selector in `5 … 0x41`**

```asm
0057CF40  mov r9d, ecx                ; arg0
0057CF7B  movzx esi, r9w              ; selector = LOW 16 bits
0057CF71  shr ebx, 0x10               ; ebx      = HIGH 16 bits  - the index arm 1 passes on as `shopIndex`
0057CF87  lea ecx, [rsi - 5]
0057CF91  cmp ecx, 0x3c / ja default  ; 61 admissible values, 5 … 0x41
0057CF9A  movzx eax, byte  [0x0057D528 + (sel - 5)]   ; byte map, 61 entries
0057CFA2  mov   ecx, dword [0x0057D514 + eax*4]       ; five arm offsets, image-base-relative
0057CFA9  add rcx, 0x00120000 / jmp rcx
```

> **The four table addresses cited here are not function entries, and that is expected.** `0057D514`, `0057D528`,
> `0057D568` and `0057D594` are the head and tail switches' arm tables and byte maps. `0057CF20`'s listed extent is
> `0x5F4`, so the body ends at **`0x0057D514`** — the arm table begins at the **first byte past it**, which is where
> MSVC puts a switch's tables. *Stated because the address gate flags them for confirmation in context, and this is
> the context.*

**The function is two switches on the same selector, not one.** The head picks **where the list comes from and how
long it is**, allocates `count × 0x20`, and falls into a **shared tail** that picks **how each entry is filled**.
*Control: the arm already read by hand at `0057CFB9` must come back as some selector's target — it does.*

| head arm | entry | selectors | source and count |
|---:|---|---|---|
| 1 | `0057CFB9` | `0x14`–`0x1B`, `0x1D` | **shop stock** — `002FAD30(highHalf, mode 1, category = sel − 0x14)` |
| 2 | `0057D036` | `0x1F` | **the bazaar** — the same wrapper, `mode 2`, category `0` |
| 4 | `0057D08B` | `0x06`–`0x13`, `0x1C`, `0x1E`, `0x20`–`0x40`; and, as the default for every selector outside `5 … 0x41` (`0057CF94` `ja 0057D08B`), `0`–`4` (the inventory menu's kinds) and `0x42`–`0x44` (the equip screen's kinds) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 4; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))* | **not the shop path** — three banded tables, below |
| 3 | `0057CFAE` | `0x41` | `r14d = 0x10`, then **straight to the tail — nothing is allocated** |
| 0 | `0057D14B` | `0x05` | **straight to the tail — nothing is allocated** |

> **`0057D14B` is the common tail, not selector `0x05`'s arm — and reading it as an arm is the mistake to avoid.**
> Arms 1, 2 and 4 all converge on `0057D139` (`0057D031`, `0057D086`, and arm 4's `0057D108` path) after
> `0057D124 call 002497E0` / `0057D134 call 00861EC0` have allocated and zeroed `count × 0x20`, and `0057D139`
> falls straight into `0057D14B`. **The head byte map simply routes `0x05` and `0x41` there with no allocation
> step.** *I had this written up as "a second, nested switch" belonging to one selector before tracing the
> fall-through; that is why the jump targets are dumped rather than inferred from the table alone.*

**The tail dispatches on the raw selector** over `0 … 0x44` through its own pair of tables — byte map
`0x0057D594`, arm table `0x0057D568` — into **11 arms**. Over the 61 selectors the head can actually deliver,
`5 … 0x41`, **every one of the 11 is reachable and none of the map's indices goes unused**:

| tail arm | entry | selectors |
|---:|---|---|
| 10 | `0057D4DF` | `0x0D`–`0x0E`, `0x10`–`0x13`, `0x1C`, `0x1E`, `0x20`–`0x3F` — **40 values, the default** |
| 0 | `0057D168` | `0x08`–`0x0B`, `0x40` |
| 5 | `0057D1A1` | `0x14`–`0x17` |
| 3 | `0057D3E3` | `0x06`, `0x0F`, `0x1B` |
| 1 | `0057D330` | `0x0C`, `0x18` |
| 6 | `0057D35C` | `0x19`–`0x1A` |
| 2 | `0057D26A` | `0x05` |
| 4 | `0057D41B` | `0x07` |
| 7 | `0057D494` | `0x1D` |
| 8 | `0057D4BD` | `0x1F` |
| 9 | `0057D1A6` | `0x41` |

**So the nine shop categories do not share one renderer:** `0x14`–`0x17` take tail arm 5, `0x18` arm 1, `0x19`–
`0x1A` arm 6, `0x1B` arm 3 and `0x1D` arm 7. *The category selects the stock; the tail arm selects ~~the row
layout~~ the filler (all four fillers write one row layout), and the two groupings are different.* *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 1; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*

**Where the eleven arms converge.** They are not eleven separate renderers: the whole tail calls `0020E600`
thirteen times for the per-row source and funnels into a small set of fillers, of which `0057DED0` is already
named on `0057D620`'s row above.

> **There are FOUR fillers, not three — corrected 2026-09-21 (FABLE, Claude Opus 5), against my own count.**
> `0057DAD0`, **`0057DC30`**, `0057DD60` and `0057DED0`. *I missed the fourth to a display cutoff:* I built the
> population from a call-target census **printed sorted by frequency and truncated to the top ten**, and
> `0057DC30` has a **single** call site (`0057D4D2`), so it fell below the cut. Re-run with no cutoff over both
> builders it is plainly there. **A census counts what its list reached, and I let a print limit define the
> population.**
>
> **The same re-run also shows the screen I used was too crude in the other direction.** "Advances a cursor by
> `0x20`" also matches `0057CDD0`, `002497E0` and `00252FA0` — whose `add …, 0x20` is **`add rsp, 0x20`**, stack
> cleanup. Checking *what* is advanced, and whether anything is written through it, separates them: `0057DC30`
> steps `rbx` and writes through it **ten times**; those three write through it **never**.
>
> **What survives, checked rather than assumed.** ~~*The two row layouts stand*~~: `0057DC30` sets its cursor
> `0057DC4F lea rbx, [rcx + 0xa]` and writes `+0x08`, `+0x0A`, `+0x0C`, `+0x0E` and `+0x10` — **layout A**, the
> same shape as `0057DED0` and `0057DD60`, with the price at `+0x10`. ~~So it is three fillers on layout A and
> `0057DAD0` alone on layout B, not two against one.~~ All four fillers write layout A: `0057DAD0`'s cursor is `entry + 8` (`0057DAFF lea rbx, [rcx + 8]`), so its price store at cursor `+8` is entry `+0x10` *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 1; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*. *And the flags table stands*: `0057DC30` receives the band
> tag in `r9d` at `0057D4C9` and **tests no bit at all** — its only `test`s are on the count and two pointers — so
> every bit I reported as read by nobody is still read by nobody. **It writes `dword[entry+0x10]` directly
> (`0057DD0A`, `0057DD18`) and reads it back at `0057DCFC`, by a rule the flags word plays no part in.** Arms **0 and 5 literally share a
body**: arm 5 is two instructions, `0057D1A1 cmp esi, 0x17` / `jmp 0057D16B`, landing inside arm 0 just past its
own `cmp esi, 0xB`, so the two differ **only in which selector sets a single flag bit**:

```asm
0057D168  cmp esi, 0xb          (arm 0)     both set bl = (selector == this band's LAST value)
0057D1A1  cmp esi, 0x17         (arm 5)
0057D172  sete bl / or ebx, r14d               then OR'd with the band tag from the head
0057D16B  mov ecx, dword ptr [r13 + 4]         r13 = the query row 00252F40 returned
0057D178  call 0020E600 -> rdx                 the source rows
0057D188  mov r9d, esi                         the SELECTOR is passed through
0057D197  call 0057DED0(buffer, rdx, count, selector, queryRow, flags)
```

*`0xB` is the last of arm 0's `0x08`–`0x0B` and `0x17` the last of arm 5's `0x14`–`0x17`, so the bit marks the
final kind of its band — **and `0057DED0` never reads it.** The bits that body tests are the band tag, below.*

**The band tag is a price rule — 2026-09-21 (FABLE, Claude Opus 5).** *I left "what `0057DED0` does with the
band's last-kind flag" open above. Reading it answers a different question than the one I asked:* the flags word
reaching the filler is `sete bl` (the last-kind bit) **OR'd with `r14d`, the head arm's band tag**, and
`0057DED0` tests **only the tag**:

```asm
0057DFC8  mov dword ptr [rbx], edx         entry+0x10 = the packed dword, bit 31 from byte[rec+0x54]
0057DFCA  test r13b, 2   / je              tag bit 1 ...
0057DFD0  mov eax, dword ptr [rdi + 0x28]  ... take the record's +0x28 WHOLE
0057DFD5  test r13b, 4   / je              else tag bit 2 ...
0057DFDB  mov eax, dword ptr [rdi + 0x28]
0057DFDE  sar eax, 1                       ... take it HALVED
0057DFE0  xor eax, edx / btr eax, 0x1f / xor eax, edx    keep edx's bit 31
0057DFE8  mov dword ptr [rbx], eax
```

and the head arms set the tag: **`2` on the shop-stock exit (`0057D02B`) and the bazaar exit (`0057D080`)**,
**`4` on arm 4's mid band (`0057D0E1`)**, `0x10` on its high band (`0057D0B2`) and on selector `0x41`
(`0057CFAE`), `0` otherwise. So a row's `+0x10` is:

| tag | selectors | `entry + 0x10` |
|---:|---|---|
| `2` | shop stock `0x14`–`0x1B`, `0x1D`; bazaar `0x1F` | `dword[rec + 0x28]` **whole** |
| `4` | arm 4's mid band | `dword[rec + 0x28] >> 1` — **halved** |
| `0x10`, `0` | high band, `0x41`, the rest | left as the packed default |

**`+0x28` is the price, and that identification is the encoded-id page's, not mine.** Its §4 per-class fills give
class 18 bazaar `+0x28 <- row+0x10 (u32)` **"the price"**, and the item-like classes fill the same slot — 5 items
`row+0x0A`, 6 equipment `row+0x12`, 7 loot `row+0`. The shop-screens page independently calls `0057D620`, which
shares these fillers, *"the price/name formatter"*.

***So the tag distinguishes a list you BUY from a list you SELL.*** Arm 1 and arm 2 build from the shop's
authored stock and the bazaar - the things on offer - and pass the price whole. Arm 4 builds from the **shared
query table** through `00252F40`, which is what the player already holds, and passes it **halved**. *The
half-price sell rule is not read here from lore; it falls out of which arm filled the list.* *(2026-09-30, SWE2-STRUCT for OPUS: not open - "not read from lore" names the source; the rule itself is read from the code, arm 4's halving in the "Bounds" paragraph below.)*

**Bounds.** The halving is `sar eax, 1` over bits 0–30 with bit 31 restored from the packed dword, so the top bit
is a flag rather than part of the value. **And that flag comes from a byte the fill never writes** —
`byte[rec+0x54]` is read by `0057DED0` and written by nothing in `0031C5D0`, so on the static-record path it
carries whatever the previous call left; see
[the encoded id space and the query record](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md).
*Bit 31 of a row's price is therefore not a property of that row.*

> **Who reads the last-kind bit: nobody — answered 2026-09-21 (FABLE, Claude Opus 5).** I wrote above that its
> consumer must be one of the other two fillers. It is neither. Sweeping **every** use of the flags value in all
> three, in both register spellings, from the load to the epilogue restore, gives the whole protocol:
>
> | bit | set by | tested by |
> |---:|---|---|
> | 1 (`2`) | the shop-stock exit `0057D02B`, the bazaar exit `0057D080` | all three — price **whole** |
> | 2 (`4`) | arm 4's mid band `0057D0E1`; `0057D620`'s `r14d = 4` | all three — price **halved** |
> | 5 (`0x20`) | ~~tail arm 3 `0057D3EA`~~ tail arm 3 for selector `0x0F` only (`0057D3EA or ebx, 0x20`, then `0057D3ED cmp esi, 0xf` / `0057D3F0 cmovne ebx, r14d` puts the plain tag back for `0x06` and `0x1B`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 5; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*; `0057D620` `0057D98D` | `0057DAD0` only (`0057DBCF`) |
> | **0 (`1`)** | `sete bl`, the band's last kind; `or r14d, 1` at `0057D233` | **nobody** |
> | **4 (`0x10`)** | the high band `0057D0B2`, selector `0x41` `0057CFAE` | **nobody** |
> | **3 (`8`)** | **neither builder** | `0057DAD0` `0057DB67` — a test that can never fire |
>
> **The absences are complete, not sampled.** The three fillers have **exactly two `rel32` callers between them**,
> `0057CF20` and `0057D620`, with no qword-table and no rip-relative `lea` route — so "set by nobody" and "read by
> nobody" range over the entire population that can reach them. And the flags value never leaves a filler by any
> other path: `0057DED0` tests two bits and restores the register (`0057E003`), `0057DD60` tests two and then
> reuses `r8` for an unrelated pointer (`0057DE55`), `0057DAD0` tests four. *It is only ever tested, never stored
> and never passed on.*
>
> **So this is a shared six-bit word with two write-only bits and one read-only one.** That shape is what a
> protocol looks like after one side of it was changed and the other was not; it is **not** evidence that the
> last-kind bit is meaningless, only that nothing downstream of these two builders consumes it.

~~**There are three fillers because there are two row layouts — 2026-09-21 (FABLE, Claude Opus 5).** Reading what
`0057DD60` and `0057DAD0` do with the flags answers the question above and changes its shape: **`0057DAD0` does
not build the same row as the other two.**~~ **There is one row layout, and `0057DAD0` writes it too.** *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 1; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))* The table below reads `0057DAD0`'s stores relative to its cursor, and the cursor is `entry + 8` (`0057DAFF lea rbx, [rcx + 8]`; the entry itself is `rbx - 8`, `0057DB55 lea r14, [rbx - 8]`). Read from the entry, `0057DAD0` writes the name pointer at `+0` (`0057DB98`), the id at `+8` (`0057DB7E`), the class byte at `+0xA` (`0057DB85`), the owned count or `0xFFFF` at `+0xC` (`0057DB76`), channel 1 at `+0xE` (`0057DBA2`) and the price at `+0x10` (`0057DB9F`, `0057DBCC`, `0057DBE0`): the offsets the other fillers write. The flag sentences that follow stand; only the offsets move.

| entry offset | `0057DED0` and `0057DD60` | `0057DAD0` **reads by cursor offset, not by entry offset** (entry = cursor + 8: id `+8`, count `+0xC`, price `+0x10`; name at `+0`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 1; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))* |
|---|---|---|
| `+0x00` | the name string pointer | **the encoded id** — `0057DB7A movzx eax, word ptr [rdi + 6]`, `0057DB7E` |
| `+0x04` | — | the **owned count** `word[rec + 0x20]`, or `0xFFFF` |
| `+0x08` | the encoded id | **the price** — `0057DBCC` / `0057DBE0` |
| `+0x0A`, `+0x0C`, `+0x0E` | class byte, query channels 0 and 1 | — |
| `+0x10` | **the price** — `0057DFC8`, `0057DE1B` / `0057DE8D` | — |

*`0057DD60` writes the same shape as `0057DED0`* — `word[rdi-8]`, `byte[rdi-6]`, `word[rdi-4]`, `word[rdi-2]` and
`dword[rdi]` off a cursor held at `entry + 0x10` and advanced by `0x20`. ~~**`0057DAD0` writes a tighter row with no
name pointer**, which is why the price sits at `+8` there and at `+0x10` in the other two.~~ `0057DAD0` writes the same row: its name pointer goes to `rbx - 8` (`0057DB98`), and its price at cursor `+8` is entry `+0x10` *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 1; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*.

**And both bits I reported as unwired now have a meaning**, which is more than "nothing sets them":

- **Bit 3 (`8`)** selects the **owned count**: `0057DB67 test bpl, 8` takes `word[rec + 0x20]` into ~~`+4`~~ cursor `+4`, entry `+0xC` (`0057DB76`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 1; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*, and the
  `je` arm takes `0xFFFF` instead. Since neither builder sets the bit, **that slot is always the `0xFFFF`
  sentinel on these paths** — the row has a place for the owned count and never carries one.
- **Bit 5 (`0x20`)** is a **zero-price marker**: `0057DBCF test bpl, 0x20`, then `0057DBD5 test eax, 0x7fffffff` /
  `jne`, then `0057DBDC bts eax, 0x1f`. *If the price's low 31 bits are zero, set the top bit.*

> **Which means bit 31 of a price has two writers with different meanings.** In `0057DED0` it is
> `byte[rec + 0x54]`, a byte the fill never writes — see
> [the encoded id space and the query record](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md).
> In `0057DAD0` it is this deliberate "price is zero" sentinel. **A reimplementation cannot treat that bit as one
> flag**, and the two paths are told apart by which filler built the row, not by anything in the row itself.
>
> ~~*Still not read:* what consumes either form of the bit, and what `0057DAD0`'s `+4` would carry if anything ever
> set bit 3.~~ *Corrected 2026-09-30 (FABLE, Claude Opus 5.5).* The `+4` half was already answered by the bit-3
> bullet above: `word[rec + 0x20]`, the owned count. On the consumer: the shop transaction driver `0056D370` reads a
> layout-A row's `+0x10` and discards bit 31 (`0056D468 btr ebx, 0x1f`) before multiplying by the quantity, on the buy
> and the sell path alike (§5). So neither form of the bit reaches a commit from a layout-A row. ~~Who reads a layout-B
> row's price, and its zero-price bit, is GR-13.~~ There is no layout B (GR-13): the driver reads `0057DAD0`'s price at the same `+0x10`. The zero-price bit is read by the sale test: when bit 0 of the mode word it is handed is set (`0056E715`), `0056E700` scores 8 for a row whose `+0x10` dword has bit 31 set (`0056E71A`–`0056E72B`), and the driver declines a non-zero score (`0056D576`–`0056D57D`); so in sale mode bit 31 means "cannot be sold", whichever filler set it *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 1; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*. Arm 9 (`0x41`) is the odd one: it sums **two** query lists,
`00252FA0(2) + 00252FA0(4)`, and returns 0 when the total is zero.

**What the query row is for, and what a `0x20`-byte entry holds**

`0057DED0` walks the source as **16-bit ids terminated by `0xFFFF`**, resolves each through
`0035D380(6, id)` — the class-6 id wrapper that
[`CONTRACT-encoded-id-space-and-class-registry.md`](../00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md)
contracts as "the static record at `022CA480`" — and **filters on the query row**:

```asm
0057DF42  movsxd rax, dword ptr [r12]      r12 = the query row; its first dword is a COUNT
0057DF50  mov r9d, dword ptr [rdi + 0x38]  a class-specific field of the resolved record
0057DF60  movsx ecx, word ptr [rax]        each word of the row, at +4 upward
0057DF63  cmp r9d, ecx / je accept
```

**So the query row is a whitelist**, and an id survives only if `dword[rec+0x38]` appears in it. That answers what
arm 4's banded tables are *for*: their word 0 selects which whitelist applies. *`+0x38` falls in the region the
query-record field map calls "the class's own copies" (`+0x28` onward), so the filter is on a **class-specific**
field, not on the class itself.*

Each surviving id becomes one `0x20`-byte entry — and because the query record's field map is already published,
most of the entry can be named rather than merely located:

| entry | written from | what that record field is |
|---|---|---|
| `+0x00` qword | `002B58B0(qword[rec + 0x18])` | **the name string pointer** |
| `+0x08` word | `word[rec + 6]` | **the encoded id itself** — *the word message `286` carries* |
| `+0x0A` byte | `byte[rec + 0x2C]` | a class copy |
| `+0x0B` byte | `byte[rec + 0x38]` | the field the whitelist matched on |
| `+0x0C` word | `word[rec + 0x20]` | **query channel 0** — the owned count, or the owned bit for a bitset class |
| `+0x0E` word | `word[rec + 0x24]` | **query channel 1** |
| `+0x10` dword | **at build time** the price, or the price **halved**, with `byte[rec + 0x54]` in bit 31 | the band tag decides which — below; ~~**the layout pass overwrites these bytes**~~ on an inventory-menu (family A) list the layout pass overwrites these bytes; a shop list never receives message 26 (GR-14) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 2; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*, see the note after it |

*So a row carries exactly what a list needs to draw it — name, owned count, the mode-1 answer and three
class-specific bytes — and none of that had to be re-derived: it is [the query record's own field
map](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) read against the stores.*
**`word[rec+6]` IS named, and I should have cited it rather than re-derived it — amended 2026-09-21
(FABLE, Claude Opus 5).** I published this as "not in that map and left unnamed", which is true of the field-map
*table* and misleading about the store:
[`the-encoded-id-space-and-the-query-record.md`](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)
§2.4 names it three lines above that table — *"`+0` the class (dword), `+4` the row index (dword), **`+6` the id**
(the high word of `+4` — the word-form wrapper stores `dx` there, `0035D396`)"*. **So `word[rec+6]` is the encoded
id passed to `0035D380`,** and the id form writes only a word where the row form writes a dword row at `+4`, which
is why one eight-byte header serves both.

*What follows from it, which is this page's to say:* **every `0x20`-byte list entry carries the encoded id it was
built from**, at `+8`. That is what makes a pointer to one entry a sensible message payload — the receiver wants
one id, not the row — and it is why `00565720` can stamp that word into every `+0xF0` record while rebuilding the
list. *The identity of the field is the encoded-id page's; only the consequence is new here.*

**The upper `0x10` bytes are view state, not record data.** `005651E0`'s message-26 arm writes `0xFC00` into
`word[entry+0x10]` while accumulating a layout coordinate, and `0057DED0` itself only sets bit 31 of that dword
and preserves the rest — `0057DFA8 and dword ptr [rbx], 0x7fffffff` before `0057DFC8 mov dword ptr [rbx], edx`.

> **`+0x10` IS WRITTEN TWICE, FOR TWO DIFFERENT THINGS, AND I PUBLISHED BOTH CLAIMS WITHOUT RECONCILING THEM —
> 2026-09-21 (FABLE, Claude Opus 5).** The table above calls `+0x10` the price; the paragraph above calls the same
> bytes view state. **Both readings are from the image and they overlap**, which the page should say rather than
> leaving a reader to notice. `0057DED0` writes a **dword** there at build time. `005651E0`'s message-26 arm then
> writes, into the very same bytes of the very same entry — `rbx = [self+0xE0] + index*0x20`, the list
> `00565720` fills — a **mode byte** at `+0x10` (`005654E1` `1`, `00565508` `2`, `00565537` `3`, `00565532` a
> computed value) and **two coordinate words** at `+0x12` and `+0x14`.
>
> ~~***So `+0x10` is not a stable price field.*** It carries the price when the list is built and is overwritten
> when the row is laid out.~~ ***On an inventory-menu list `+0x10` is reused; on a shop list it is not.*** `005651E0`, the message-26 arm, is reached only from the four list procedures `00564B90` installs for the inventory menu's widget ids `0x405`–`0x40F` (GR-14). The shop widget's procedure `0056E140` and the driver `0056D370` hand message 26 to a shared empty stub, `xor eax, eax` / `ret` (the tail jump at `0056E3B3`, the call at `0056D3B8`). So on a shop list `+0x10` is the price from build to purchase *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 2; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*. *Two confident sentences about one field, written a commit apart, is how a page ends
> up contradicting itself; the honest version is that the field is reused.*
>
> **Is the price read before the layout pass overwrites it? Not through the indexed form.** An image-wide sweep
> for bodies that form an entry address the way `005653BE` does — `index` shifted left 5 and added to
> `qword[reg + 0xE0]` — returns **exactly two**: `005651E0`, whose accesses off that register are `R`/`W` at
> `+0x10`, `R` at `+0x11`, `R`/`W` at `+0x12` and `R`/`W` at `+0x14` — *byte and word accesses, the layout
> triple* — and `005665B0`, which forms the address only to hand it on as a constructor argument and never
> dereferences it. **Nothing reads `dword[entry+0x10]` as a price through that addressing.**
>
> **The bound, which is the part that keeps this from being an absence claim.** The sweep catches the `index*0x20`
> form only. The filler itself walks its output with `add rbx, 0x20`, and **a drawing loop that walked the list the
> same way would not appear** — so "nothing reads the price" is *not* established, only that no indexed reader
> exists. What also remains unread is whether the selector reaching this object's list routes to `0057DED0` at
> all, since the selector is a construction parameter this page could not pin down. *(2026-09-30, SWE2-STRUCT for OPUS: answered - the price reader is the transaction driver `0056D370` (the 2026-09-30 paragraph below); the selector is GR-15's: the list `005651E0` lays out belongs to the inventory menu's list widgets (family A, kinds 0-7 passed as selectors 0-7 with no remap), whose equipment kind is filled by `0057DED0`; [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md).)*
>
> **And that gap is not closable by a static sweep — 2026-09-21 (FABLE, Claude Opus 5), after two attempts that
> both failed the same way.** Filtering "bodies of this family" by whether they touch `+0x17F`/`+0x180`/`+0xE8`/
> `+0xF0` returned **283 functions**; filtering by "reads `qword[reg + 0xE0]` **and** advances a register by
> `0x20`" returned **110**. Both numbers are the answer to a different question: those offsets and that stride are
> ordinary across unrelated objects, so any filter wide enough to catch a walking reader is too wide to be
> evidence of one. *Narrowing it needs the object's identity, which is exactly what is not established here* —
> `005651E0`'s `self` is reached through a forward and its type is not named. *(2026-09-30, SWE2-STRUCT for OPUS: answered - GR-14's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md): `005651E0` is entered only by tail jumps from the four list procedures `005636F0`, `00563930`, `00563B10` and `00563D20`, which `00564B90` installs only on the inventory menu's widgets `0x405`-`0x40F`; the shop list is found by the other method below.)* **So this is recorded as not
> establishable by this method, rather than left open-ended**, to stop the next reader re-running the same sweep
> and reading 110 as a finding.
>
> ***A price reader, found by another method — 2026-09-30 (FABLE, Claude Opus 5.5).*** Following the purchase instead
> of sweeping for walkers finds one. The transaction driver `0056D370` forms a row address as `index << 5` plus its own
> list pointer `+0xC8` (`0056D564`–`0056D56F`), not `+0xE0`. That is why the indexed sweep above could not see it.
> It reads `dword[row + 0x10]` as the unit price (`0056D461`, bit 31 cleared at `0056D468`). The list it holds is
> refreshed by the widget's rebuild: `005655F0` builds it through `0057CF20` into the widget's `+0xE0` (`005656A2`,
> `005656AE`), and `0056E410` transfers it to `+0xC8` of the object at the widget's `+0xC0` (`0056E422`, `0056E55A`)
> and zeroes the widget's `+0xE0` (`0056E561`). The driver runs that refresh with its own `+0x10` as the widget
> (`0056C876`, `0056C8B7`) and reads its `+0xC8` straight after (`0056C8C8`); ~~that the object at the widget's `+0xC0`
> is the driver is read from this pairing, not proven separately.~~ the object at the widget's `+0xC0` is the driver: `0056DD50` creates the shop widget with procedure `0056E140` (`0056DD66`) and passes it to `0056C950` (`0056DE78`), which creates a widget with procedure `0056D370` and stores it at the shop widget's `+0xC0` (`0056C9BC`–`0056C9CB`) *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 6; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*. *(2026-09-30, SWE2-STRUCT for OPUS: answered - [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md), consumer item 6: `0056C9BC`-`0056C9CB` creates the widget with procedure `0056D370` and stores it at the shop widget's `+0xC0`.)* So "nothing reads
> the price" is false for this interface. What stays open is whether message 26's layout write can land on a list before
> the transfer hands it to the driver. That is GR-14, and it is now a question of order, not of finding a reader. *(2026-10-01, SWE2-STRUCT for OPUS, DD batch 21: GR-14 is ANSWERED, no. A shop list never receives message 26; see the GR-14 box in section 7 and the corrected paragraph above.)*

> **One caution the contract forces.** `0035D380(class, id)` does not return a fresh record: the contract records
> it as returning **the static `EncodedIdQueryRecord` at `022CA480`**, `0x98` bytes, refilled on each call. So the
> filler resolves and copies out **one id at a time through a single shared scratch record**, and any reading of
> this loop that assumes the `rdi` records of two iterations coexist is wrong.

So **§2.5's nine categories are nine contiguous selector values** and the bazaar is a tenth, which is why
`category = selector − 0x14` works at all.

**Arm 4 carries 49 of the 61 values, and it is not the shop path**

It splits the selector into **three bands, each with its own authored table of 4-byte records**:

| band | test | table | index | `r14d` |
|---|---|---|---|---:|
| high | `sel >= 0x40` | `0x00D23988` | `sel − 0x40` | `0x10` |
| mid | `8 <= sel < 0x40` | `0x00D23D00` | `sel − 8` | `4` |
| low | `sel < 8` | `0x00D23960` | `sel` | unset on this path |

and each band does the same two lookups off the record's **first word**, then sizes the result the same way:

```asm
0057D09A  movzx ecx, word ptr [rbx + rax*4]   0F B7 0C 83   the record's word 0
0057D09E  lea rbx, [rbx + rax*4]                            rbx = the record
0057D0A2  call 00252F40                                     -> r13
0057D0A7  movzx ecx, word ptr [rbx]           0F B7 0B      the SAME word 0, read again
0057D0AD  call 00252F70                                     -> rax
0057D108  mov edi, dword ptr [rax]                          a COUNT; zero returns 0
0057D11F  shl ebx, 5                                        count x 0x20 - the same entry stride
```

*Read byte-exactly, because a body passing one word to two different lookups looks like a misread and is not one:*
`0F B7 0C 83` is `[rbx + rax*4]` and `0F B7 0B` is `[rbx]` after the `lea`, so both calls receive **word 0**.

**And word 0 is a query-row id, which a peer had already measured.**
[`the-encoded-id-space-and-the-query-record.md`](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)
records under *SWE2-EC7-106, 2026-09-20* that `00252F40` is "the bounded query-row fetch … `ecx > 0xB` reports
`0016D6A0(0x200)` and clamps the index to 0, then answers `02092760 + movsxd(ecx) * 8`". So **arm 4 builds its
list out of the shared query table**, not out of shop stock — and the bound corroborates the tables: ~~the four
high-band words at `0x00D23988` are `1`, `1`, `2`, `3`, every one inside `0 … 0xB`.~~ the high band holds five records, `{1, 1}` `{2, 3}` `{2, 4}` `{2, 4}` `{3, 5}`, one per selector `0x40`–`0x44`, and every word 0 (`1`, `2`, `2`, `2`, `3`) is inside `0 … 0xB` *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 4; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*. *I read those tables before
finding that measurement; the agreement is a check on both, not a derivation from either.* `00252F70` then
returns an object whose **first dword is the count**, in the shape of `00252FA0(list)` on the same page.

`r14d` is carried onward as a band tag — `0x10` for the high band, `4` for the mid, and head arm 3 sets `0x10`
for selector `0x41`.

> **The record's second word is read by neither builder — 2026-09-21 (FABLE, Claude Opus 5).** I first wrote this
> as "not consumed at this point", which was true and weak. The scope is exact: ~~**the three tables have nine
> reference sites in the entire image, and all nine are inside these two builders**~~ **the builders reach the three tables through nine image-base-relative sites** *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 3; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))* — `0057D0E9`, `0057D093`,
> `0057D0C2`, `0057D377` in `0057CF20`, and `0057D719`, `0057D672`, `0057D70F`, `0057D92C`, `0057D93D` in
> `0057D620`. Every read of a record takes **word 0**, twice: once for `00252F40` and once for `00252F70`
> (`0057D09A`/`0057D0A7`, `0057D0C9`/`0057D0D6`, `0057D0F0`/`0057D0FD`, `0057D38C`, and `0057D67A`/`0057D684`,
> `0057D728`/`0057D732` in the sibling). The stride is `4`, so ~~`+2` is skipped every time~~ these two builders skip `+2` every time. **The image has five more, rip-relative, sites.** `00565C25` and `00565D06` read the low band's word 0. `00563E37` and `00563F5B` (low band) and `003FE2C5` (high band) point at word 1, and `00563E3E`, `00563F62` and `003FE2CC` read that second word as the first argument of `00293110` (`00563E42`, `00563F7D`, `003FE2D5`). So the second word is unread by these two builders and read elsewhere *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 3; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*.
>
> **And it is not padding.** The high table at `0x00D23988` reads `01 00 01 00 | 02 00 03 00` — ~~records
> `{1, 1}` and `{2, 3}`~~ the first two of five records, `{1, 1}` `{2, 3}` `{2, 4}` `{2, 4}` `{3, 5}` *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 4; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))* — so the second word is authored, non-zero, and differs from the first where it can.
>
> ***This is the third piece of authored data on this mechanism with no reader in the bodies that own it***, after
> the flags word's last-kind bit and its `0x10` bit. Together they read like one side of an interface that was
> reduced while its tables and flag words kept their original width. *Stated as **unread by these two builders**,
> not as unused:* the tables are static data, and a reader elsewhere handed a record pointer would never have to
> reference the base address that this sweep looks for. *(2026-09-30, SWE2-STRUCT for OPUS: answered - [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md), consumer item 3 (its step D1): the second word is read elsewhere. Five more rip-relative sites reference the tables, and three of them read the second word, `00563E3E` and `00563F62` on the low band and `003FE2CC` on the high band, each passing it to `00293110`. So "nine reference sites in the entire image" above undercounts, and "unread by these two builders" stands as worded.)*

**`0057D620` is the same interface, not a coincidence**

The residual-placement row above calls `0057D620` a "stock-list worker" on its callees. *(Provenance note, 2026-09-21 (FABLE), answering `OPUS-REQ-FABLE-THREE-LIVE-ABSENCE-CLAIMS-BLOCK-THE-GN162-CARRY`: the word **residual** here names **this page's own placement row**, not the record's present state. `0057D620` is in the residual set at GN158 and GN160 and **out of it at the current parent GN162**, where it carries `UI.Shop.ScreenRefresh` — which agrees with the reading below rather than disturbing it, a shop-screen refresh worker being exactly what this interface serves. Nothing on this line needs retracting.)* It takes **the same packed
argument**: `0057D64E movzx edi, r9w` for the low half, `0057D65A sar ecx, 0x10` for the high, the same
`call 0057CE10` on arg1, and the same `0057D660 cmp edi, 0x40` / `0057D665 lea eax, [rdi - 0x40]` reaching **the
same table at `0x00D23988`**. *(It uses an arithmetic shift for the high half where `0057CF20` uses a logical one;
nothing here depends on which.)*

**The selector is a construction parameter, and two widget families share the space**

`00565720` reads it as `movsx ecx, byte ptr [rdi + 0x17f]`. **Nothing in the image writes that byte as an
immediate.** An instruction-boundary sweep of every function in the graph for `mov byte ptr [reg + 0x17f], …`
returns **0 immediate writes and exactly 2 register writes** — the control being that `00565720` must come back as
a reader of the same offset, and it does. The two writers are what settle the field:

```asm
00564780:  movsxd r15, edx                            ; arg1 = this widget's own kind
005647AD   mov byte ptr [rcx + 0x17e], r15b
005647B4   mov byte ptr [rcx + 0x17f], r15b           ; selector = kind
005647BB   lea rcx, [rip + 0x19c83ce]                 ; then a per-kind pointer table, indexed kind*8

003FD360:  mov byte ptr [rcx + 0x17e], dl             ; arg1 = this widget's own kind
003FD36E   lea eax, [rdx + 0x40]
003FD371   mov byte ptr [rcx + 0x17f], al             ; selector = kind + 0x40
```

**`003FD360`'s half of that is already published and is not mine.**
[`the-encoded-id-space-and-the-query-record.md`](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)
records under *SWE2-EC7-34, 2026-09-19* that `003FD360` is a query-record setter, "`dl`->`[rcx+0x17E]`,
**`dl+0x40`->`[rcx+0x17F]`**". **What is added here is the other writer and what the bias is for.**

**`+0x17E` is the family's own kind; `+0x17F` is the selector it maps to** — the same value for `00564780`'s
family, **biased by `0x40`** for `003FD360`'s. *That bias is exactly what the `cmp …, 0x40` / `lea …, [… - 0x40]`
band test in both builders is for:* ~~the second family's kinds `0` and `1` arrive as selectors `0x40` and `0x41`~~ the second family's kinds `0`–`4` (the equip screen's five slots, GR-15) arrive as selectors `0x40`–`0x44` *(Corrected 2026-09-30, FABLE, on OPUS's record [`gr13-15-shop-list-widget-0930`](../_index/candidates/gr13-15-shop-list-widget-0930/README.md) statement 4; record [`shop-page-corrections-fable-0930`](../_index/candidates/shop-page-corrections-fable-0930/README.md))*,
and the high-band table at `0x00D23988` is indexed by `selector − 0x40`. **One builder, two families, one selector
space** — which is the part neither page could see alone, because one end records the write and the other the
read.

> **Bound, and it is the interesting one.** Both writers take the value from a **register**, so *which* kinds each
> family actually uses is **not** established here — only that the list kind is chosen by whoever constructs the
> widget rather than authored in these bodies. A reimplementation that hard-codes a kind in either constructor
> would be inventing a constraint the original does not have. **This is a declared blind spot, not an absence.**
> *Registered 2026-09-30 (FABLE) as GR-15.* Each writer's callers pass the kind on from a register again: a
> create-message field in one family, and the caller's own register in the other. So one more hop does not settle it. *(2026-10-01, SWE2-STRUCT for OPUS, DD batch 21: GR-15 is ANSWERED. The kinds each family uses are in the GR-15 box in section 7: the inventory menu's eight categories, the shop's Buy, Sell and Bazaar tabs (kinds 32, 19 and 31), and the equip screen's five slots.)*

**`00565720` is "rebuild the list, reset the selections"**

```asm
00565730  mov rcx, [self + 0xE0] / test / je          release the old list
0056573C  call 003697F0
00565741  mov qword ptr [self + 0xE0], 0
0056574C  mov eax, [self + 0x180] / shl 6 / sar 0x1b  idx  = bits 21..25 of +0x180
0056576B  movsx rdx, byte ptr [self + idx*8 + 0xf6]        = byte +6 of record idx in +0xF0
00565760  mov rax, [self + 0xE8]
0056577B  movzx edx, word ptr [rax + rdx*8 + 6]            a word from row rdx of +0xE8
00565774  movsx ecx, byte ptr [self + 0x17f]               the selector
00565780  call 0057CF20(selector, thatWord, &out, 0)
00565785  mov qword ptr [self + 0xE0], rax                 the new list
```

and then, over `count = (([self+0x180] << 0xB) >>s 0x1B)` — **bits 16–20** of the same packed field — every
8-byte record at `+0xF0` is reset:

```asm
005657B0  mov word ptr [rcx],     bx        the caller's word
005657B5  mov word ptr [rcx + 4], 0xffff
005657BA  mov word ptr [rcx + 2], 0xffff
005657BF  lea rcx, [rcx + 8]
```

**So the object reads:** `+0xE0` the built list, `0x20`-byte entries — the `005653BE shl rbx, 5` in the id-26 arm
is the same stride; `+0xE8` a row table of 8-byte rows carrying a word at `+6`; `+0xF0` an array of 8-byte records
`{ word value, word sel1, word sel2, byte rowIndex }` with both selections cleared to `-1`; `+0x180` a packed
field holding **count at bits 16–20** and **current index at bits 21–25**; `+0x17E` kind and `+0x17F` selector.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

**Presentation — CLIENT.** The shop's stock gates are read by the screens that draw the shop:

- `003DFB50` and `003FFF40` ask `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate`, and `003DFBB0` is a 43-byte
  accessor. All three are read by Presentation bodies of 830, 1,118 and 4,847 bytes.
- The 82-byte `00255150` is read by bodies of 1,118 and 1,864 bytes.
- The 45-byte `00377B60` is read by the two bodies of about 4.8 KB.
- `002BA310` is read by the 4,810-byte body.
- `0046B1A0` reads `SaveImage_GetPersistentPayloadBase`. It and the 128-byte `002D47C0` are read by a 1,038-byte body.

**The gate queries are called from the screens that draw the shop.** ~~Whether any purchase path re-checks them is not
read here.~~ *Answered 2026-09-30 (FABLE, Claude Opus 5.5): none does. The purchase commit tests no gate, and the
transaction driver reaches the gate only by rebuilding a list (§5, "No purchase path re-checks a gate").*

**Rewards_Progression_Economy — SERVICE, added 2026-09-30 (FABLE).** The purchase commit `002FEEB0` pays through
the gil store: it reads the balance with `GameState_GetGil`, floors `old - cost` at zero and writes it with
`GameState_SetGil` (`002FEEE0`–`002FEEF3`). The driver also reads the balance on its other arm (`0056D54B`).
The shop spends gil and the gil store owns it ([the gil store and every path that changes it](../13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md)).
Nothing in the gil store reads the shop table.

**Gameplay — SERVICE, added 2026-09-20 (FABLE, Claude Opus 5).** The list-kind section above names `0035D380`,
the encoded-id id-form wrapper, because the entry filler `0057DED0` resolves every id through it. That carries one
edge out of this page's layer: **`0035D380` calls `0031C5D0`**, the 8,136-byte fill that
[`CONTRACT-encoded-id-space-and-class-registry.md`](../00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md)
records as reading `{class, row}` from the record's first eight bytes, and which the ledger files under
`Gameplay.BattleEncodedId`. **SERVICE, and one-way:** this page's subject asks the encoded-id space to resolve an
id and copies fields out of the answer; nothing in the encoded-id space reads the shop table. *The relationship is
the same one `0057CF20`'s arm 4 already has through `00252F40`, which the same contract owns — naming the wrapper
does not add a new dependency, only a new citation of an existing one.*
- **ActorEntity - CLIENT (1 edge).** `002B58B0` is also called by bodies filed to ActorEntity: `0023A570` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT and SERVICE (4 edges).** `00321190`, `0046B1A0` are also called by bodies filed to combat AI: `00301AD0`, `00321190`; `00236C30`, `002FAD40` reach bodies filed to combat AI: `00238880`, `00321190` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (5 edges).** `002FAE40`, `0032A930` are also called by bodies filed to script VM / native bridge: `0034C170`, `0034E980`; `0034C170` reaches bodies filed to script VM / native bridge: `00267E10`, `00267F90` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (4 edges).** `002B9C70`, `002BA530`, `003DFB50` reach bodies filed to story/event: `0032A930`, `0032A8A0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (80 edges).** `002497E0`, `00252F40` are also called by bodies filed to UI: `0055B560`, `0057CF20` (Shop), `0057D620` (Shop) - shared machinery across the layer boundary, no shared ownership.
- **World - SERVICE (1 edge).** `00236C30` reaches bodies filed to World: `003847B0` (Area) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (5 edges).** `00236C30`, `00238660` are also called by bodies filed to WorldAreaField (world area): `00238850`, `00236C30`; `00236C30` reaches bodies filed to WorldAreaField (world area): `003845F0`, `003846F0` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers, tightened word test — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Heading disambiguated 2026-09-20 (FABLE, Claude Opus 5): this page carried **two** sections under the identical
title `Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)`, over different content — the one
above is the pass-22 accounting, this one is the tightened word test. Both are mine from 2026-09-14 and neither
is changed; only this title is, and I noticed because the duplication made it unusable as an edit anchor.*

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **PlatformOnlineAchievements — CLIENT and SERVICE, ~~not read,~~ 21 edges.** Cited shop functions are called by Platform-filed bodies (80 to 519 bytes) and call others (94 to 289 bytes). ~~Which platform or achievement service these are is not read here.~~ *Read 2026-09-30 (FABLE, Claude Opus 5.5).* They are the achievement-counter family, and they reach this page through the clan rank:
  - The kind-3 gate's `002536F0` calls the rank walk `00315390`, which is filed there.
  - So are its two counters. `00316480` asks the quest-clear getter `0046B1A0`, and `00316670` sweeps the award bitmap at block `+0x3844` (§7).
  - The block getter `002536A0` is shared: fourteen Platform-filed bodies call it, the rank walk and `countB`'s sweep among them.
  - `SaveImage_FinalizeHeaderAndChecksum` calls the rank walk when it stamps a save header (§2.4).
  - The transaction driver calls the family's counter updater after a transaction (`0056D4D2`); this page does not read what it counts. *(Answered 2026-09-30, SWE2-STRUCT for OPUS, DD batch 11, static; record [`swe2struct-ddres-b11-0930`](../_index/candidates/swe2struct-ddres-b11-0930/README.md), `b11_struct.py` S1-S5, FAILS 0: it counts toward two achievements. **A purchase** (`Shop_CommitPurchaseItemAndGil` `002FEEB0`, driver `+0xE4` bit 0 clear) always reports counter 19 with the bought row's id word `+8` (`0056D4C5`-`0056D4D2`; the `0x2C0` test before it guards only the `0030B630` call). Descriptor 19 is kind 0, mode 1, threshold 53375 = `0xD07F`, so `AchievementCounter_UpdateAndMaybeFire` `00316A50` sets the award bit only when that id is `0xD07F` (`00316A81`-`00316AD3`). Counter 19 is `ACH_SPECIAL_HORIDASHI`, titled *Collector*, and `0xD07F` is the top id of class 18, the bazaar goods (`D000`-`D07F`). **A sale** (`Shop_CommitSaleItemAndGil` `00310870`, bit 0 set) adds the quantity sold, the word `+0xDC`, to counter 14 (`ACH_COUNT_SELL_EVITEM`, titled *Privateer*; descriptor kind 2, a 2-byte counter), but only when bits 6-13 of the driver's `+0xE4` equal 7 (`0056D47D`-`0056D498`). The mechanics are [the achievement-counters contract](../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md)'s. In player terms: buying bazaar good `0xD07F` unlocks *Collector*, and qualifying sales add to *Privateer*'s count.)*
  - SERVICE for the rank: the shop asks and the achievement layer's bodies answer. Nothing in that family reads the shop table.
- **Resource — SERVICE.** A cited function calls a 36-byte Resource helper.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — SERVICE.** `00236C30` on this page calls `FUN_00237fc0`, owned by that layer. What it reaches is a 404-byte scan that walks the `[02EBF138]` table from a starting row the lookup helper returns, carrying `-1` as its not-found answer; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## The `00315390` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00315390` (~289 B) — `002536A0()` then `+0x3868` dword deref
(`0031539A`/`003153A4`).

| member | role | interior |
| --- | --- | --- |
| `00316480` | `qword[022C2550]` non-null walk (`00316490`/`00316497`) | [`00316490`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002536A0`.
