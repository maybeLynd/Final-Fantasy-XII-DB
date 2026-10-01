---
system: FileSizeTables/*.fst — the per-language file-size table, 41 resource kinds by 5,000 ids, read at boot and consulted by every resource request
category: 02-Resource-And-Asset-Pipeline
status: AUDITED — the eight path-array formats §7b left unexplained are dispositioned since (six sheets, two buckets; re-derived 2026-09-18)
owner_layer: PrimaryOwner:Resource
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 17 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "12 of 12 FileSizeTables/*.fst in the install parsed as 41 x 5,000 dwords; every kind's population censused against the path arrays ResourcePath_Init installs; kind 0 id 0 = 57 = the size of system.cnf as the positive control, 2026-09-11"
last_reviewed: 2026-09-11
container_format: fst
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-file-size-tables-pass-1
  crossref_clean: true
  reopened_count: 0
---

# FileSizeTables/*.fst — the per-language file-size table, 41 resource kinds by 5,000 ids, read at boot and consulted by every resource request

> **The size of every file the engine can ask for, before it asks.** One `.fst` per language,
> 820,000 bytes each: a flat `u32[41][5000]` of byte sizes indexed by `(kind, id)` — the same two
> numbers that select a path from the resource-kind path tables — with `0xFFFFFFFF` where no file
> exists. `ResourcePath_Init` reads the whole table into `02EC3EE0` at boot, the request builder
> reads it to size every load, and the read issuer refuses any `(kind, id)` whose entry is `-1`.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **12 of 12** `FileSizeTables/FileSizeTable_{ASIA,CH,CN,DE,ES,FR,IN,IT,JP,KR,UK,US}.fst` in the install |
| size | 820,000 B each = 205,000 dwords = **41 × 5,000** |
| positive control | dword 0 (kind 0, id 0) = `0x39` = 57 = the size of `PS2Data\cdi\in\system.cnf`, which is kind 0's only path ([the standard-formats sheet](../Standard-Formats/shipped-standard-formats.md) measured SYSTEM.CNF at 57 bytes) |
| populated kinds (US) | 31 of 41; 10,521 entries; ten kinds (3, 6, 17, 18, 27, 29, 31, 35, 36, 40) hold no entry at all — and those are the kinds whose path array is empty or points at the pool itself |
| language variation | **seven** kinds differ between ASIA and US by value — **1, 2, 5, 7, 8, 9, 12** (~~1, 7, 9 and 12~~; corrected 2026-09-13, §9). By **population** only 1 (2 against 24), 7 (541 against 536) and 12 differ; kind 9 has 26 entries in both and differs in **one** value. The most divergent kind is **5**, with **533** entries changed, and it was not on the list |

## 1. What the player sees

Nothing directly. Every load the game performs — a map, a model, a script, an effect, a licence
board — is sized from this table before the archive is opened, so a wrong or missing entry is a
load that never starts. The loose-file override loaders the mod scene ships (`dinput8.dll.modbak`)
sit on the same path, which is why an override of a file the table does not size is not seen.

## 2. The layout

```struct FileSizeTable base=file size=0xC8320
+0x00000  u32[205000]  size   size[kind * 5000 + id] in bytes; 0xFFFFFFFF = no file for (kind, id)
```

No header, no count, no terminator: the kind count (41) and the id stride (5,000) live in the
reader (`imul rax, rbx, 0x1388`, `002DF963`–`002DF977`) and the file length is what the boot read
demands (`0xC8320`, `002E0439`). The 41 kinds are the 41 slots of the resource-kind path table at
`0215F000` ([the `.nmb` sheet](../VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md)
§3, *the table of tables*), and an id is the position in that kind's path array — so
`size[kind][id]` is the size of the file `ResourcePath_Get(kind, id)` names.

## 3. The loader contract

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| the file | `ResourcePath_Init` `002DF9A0`, once at boot from `CoreRuntimeScheduling` `0022A0B0` (`0022A159`) | `fread` does not return 1 — the error arm prints through the CRT and then writes to address 0 (`002E044F`–`002E0462`), a deliberate crash | — | — |
| `size[kind][id]` | `002DF960(kind, id)` — the whole function is the index arithmetic and one load (`002DF960`–`002DF97B`) | — | — | — |
| `size[kind][id]` | `0032E400(kind, id)` — the request builder's size: a per-kind runtime override array at `022C51F0[kind]` (up to `0x400` ids) is consulted first (`0032E40C`–`0032E428`), else `002DF960` through `0046DE70` (`0032E431`); a positive size is rounded up to a multiple of 64 (`0032E43B`–`0032E448`); kind `0xFF` yields `-1` (`0032E438`) | — | ↑ 64 | — |
| `size[kind][id]` | `0032EB40` — the same lookup and rounding for the staged (2 KB-chunk) request path (`0032EB60`–`0032EBA3`) | — | ↑ 64 | — |
| `size[kind][id]` | `002DF780` — the read issuer: **a `(kind, id)` whose entry is `-1` is refused before any path is resolved** (`002DF7B0`–`002DF7B9`); otherwise the path comes from the kind array (`002DF7BF`–`002DF7CC`) and the read goes through the loose-file check (`0017D930`, `001D6EF0`, `001D6B40`, `001D6F20`) or the archive (`001D6D90`) | entry `== -1` | — | — |

**How the file is found.** The path is `sprintf("%sFileSizeTables/FileSizeTable_%s.fst", "../", name)`
with `name` the language's entry in the twelve-string table at `01E88B00` — `JP US FR DE IT ES UK
KR CH ASIA IN CN`, indexed by the language id `ResourcePath_Init` receives (`002E03F5`–`002E0410`;
the format string at `00B56AC8`); then `fopen(path, "rb")` (`002E0415`–`002E0421`), one
`fread(02EC3EE0, 0xC8320, 1, f)` (`002E0432`–`002E0444`) and `fclose` (`002E0470`). The working
directory is the executable's `x64\`, so `../` reaches the install root. **The retail engine reads
the table on every boot**; it is not an override-loader artefact.

**Where the size goes.** `0032E620(kind, index, dest, id, …)` records the selector and index
(`022C51D8` / `022C51DC`), copies the caller's `0x28`-byte descriptor, and hands the request to
`0032E870`, which takes one of the **64 request slots** at `022C31C0` (`0x80` B each; the pool is
initialised by `0032E450`) and links it onto the pending list; the size from this table becomes the
slot's ~~`+0x2C` rounded up to `0x800` (`0032E8FB`–`0032E918`)~~ **`+0x28`** — `0032E88A` copies the
byte count into `esi` and `0032E92C` stores it there — which is the byte budget the pump `0032E070`
issues reads against (`0032E0CA`–`0032E0F1`). ***`+0x2C` is a different field and a different
value:*** the caller's descriptor `+0`, its **file offset**, and it is **truncated toward zero** to a
multiple of `0x800` rather than rounded up — the bias at `0032E8FC` is the sign mask, so `0x801`
becomes `0x800`. *Corrected 2026-09-21 (FABLE, `ASTRA-CONTRA-FABLE-RESOURCE-OFFSET-AND-COUNT`); the
one-instruction difference between this and the genuine round-up in `0032E400` is on*
[the queue page](../the-resource-request-queue.md). The queue itself — its six states, the chunked mode,
the completion callback at slot `+0x48` — is read only far enough to place the size, and is
**FZ-12**.

## 4. Key addresses

| Address | Name | Size | Role |
|---|---|---|---|
| `02EC3EE0` | — | 820,000 B | the table in memory, `u32[41][5000]` |
| `002DF9A0` | `ResourcePath_Init` | 2,831 B | installs the 41 path arrays per language and reads the table at its tail |
| `002DF960` | — | 28 B | `size[kind][id]` |
| `0032E400` | — | 80 B | the request builder's size, override array first, rounded up to 64 |
| `0032EB40` | — | 222 B | the staged request path's size |
| `002DF780` | — | 243 B | the read issuer; refuses `-1` |
| `01E88B00` | — | 12 × 8 | the language-name strings the file name is built from |
| `022C51F0` | — | 256 × 8 | per-kind runtime size-override pointers — zeroed by `0032EA90`, never filled (DG-6, §7) |

## 5. Corpus survey

Per-kind population of the US table, with the kind's path family from the path arrays:

| kind | entries | max id | size range (B) | what the path array holds |
|---:|---:|---:|---|---|
| 0 | 1 | 0 | 57 | `cdi\in\system.cnf` |
| 1 | 24 | 132 | 2,370 – 57,864 | the per-language `test_battle` text files (`listhelp_*.bin` …) |
| 2 | 81 | 82 | 27 – 281,128 | the `test_battle` binaries: `WepJob_Matrix`, `license_data` (12), `license_board` (70), `board_1` … `board_12` (71–82) |
| 4 | 550 | 775 | 192 – 8,054,336 | `map_ctrl\*.mpk` |
| 5 | 896 | 3,933 | 1,216 – 985,088 | `plan_map\*\global\*.ebp` (stride-3 interleave) |
| 7 | 536 | 1,178 | 16 – 11,544,192 | `myoshiok\in\Bin_Menu`, `Handbook` |
| 8 | 1,080 | 2,963 | 896 – 5,238,784 | `event\*.ebp` / `.mot` (per language) |
| 9 | 26 | 42 | 26 – 37,545 | `ff12\common\*_ref.bin` |
| 10 | 2 | 1 | 106,672 – 1,017,904 | `effect_finish\*\c_all.efx`, `menu\m_all.efx` |
| 11 | 366 | 396 | 21,632 – 969,536 | `effect_finish\*\magic\*.efx` |
| 12 | 532 | 883 | 3,520 – 25,310,800 | `effect_finish\*\event\*.efx` |
| 13 | 103 | 206 | 8,192 – 425,984 | `obj_finish\in\gadget\*.cm` |
| 14 | 143 | 550 | 139,264 – 1,064,960 | `obj_finish\in\chara\*.cm` / `.ca` |
| 15 | 47 | 47 | 32,768 – 229,376 | `obj_finish\in\high\c*` |
| 16 | 326 | 326 | 7,168 – 131,072 | `obj_finish\in\weapon\*.cm` |
| 19 | 691 | 4,350 | 4,096 – 1,900,544 | `obj_finish\in\npc\*` |
| 20 | 80 | 86 | 24,576 – 327,680 | `obj_finish\in\high\n*` |
| 21 | 166 | 640 | 224 – 35,632 | `plan_map\*\area\*.ard` (stride 2 with `.fpk`) |
| 22 | 17 | 34 | 24,576 – 716,800 | `obj_finish\in\bg_obj\*` |
| 23 | 78 | 627 | 81,920 – 1,753,088 | `obj_finish\in\summon\*` |
| 24 | 5 | 4 | 180,224 – 393,216 | `obj_finish\in\high\s*` |
| 25 | 17 | 16 | 34,816 – 57,344 | `obj_finish\in\treasure\*.cm` |
| 26 | 166 | 320 | 8 – 162 | `plan_map\*\area\*.nmb` |
| 28 | 43 | 95 | 228 – 94,356 | `movie_finish\*\*.mh` |
| 30 | 1,969 | 2,315 | 1,408 – 130,208 | `obj_finish\in\chara`, `npc` `.ca` motions |
| 32 | 248 | 317 | 708 – 24,968 | `sound\se\block\*.seb` |
| 33 | 64 | 63 | 59,456 – 100,336 | `sound\shout\us\*.sab` |
| 34 | 754 | 2,785 | 4,096 – 2,752,512 | `obj_finish\in\monster\*` |
| 37 | 1,080 | 2,963 | 896 – 5,238,784 | `event\*.ebp` / `.mot` (`in`) |
| 38 | 366 | 396 | 21,632 – 1,001,792 | `effect_finish\jp\magic\*.efx` |
| 39 | 64 | 63 | 56,384 – 85,312 | `sound\shout\jp\*.sab` |

Kinds 3, 17, 18, 29, 36 and 40 point at the pool's own slots (no array); 6, 27, 31 and 35 have
arrays (`isowaki`, `sound\wave`, `sound\music`, the debug overlays) but no sized entry — files the
engine names and never loads through this path. **The 166 `.nmb` entries of kind 26 are the 166
areas that ship both an `.ard` and an `.nmb`** — the same 166 the `.nmb` sheet counts, at the
array positions that sheet lists — and their sizes, 8 to 162 bytes, are the archive's sizes of
those files to the byte (§6).

## 6. Falsification pass — 2026-09-11

- *Is the table really indexed by `kind × 5000 + id`, with `id` the position in the kind's path
  array?* The two readers compute `kind × 0x1388 + id` (`002DF963`, `002DF79D`) and the boot
  read's length is exactly `41 × 5000 × 4`. Then, for four kinds, every sized id was resolved to
  the path at that position of the kind's `in` / `us` array and the archive's size of that file
  compared with the entry: **kind 26 `.nmb` 166 of 166, kind 21 `.ard` 166 of 166, kind 2
  `test_battle` 81 of 81, kind 16 weapons 326 of 326 exact**, with no offset or stride (an affine
  search over strides 1–4 and offsets −8 … 8 peaks only at `id × 1 + 0`); kind 0 id 0 sizes
  `system.cnf` at 57 and kind 2 ids 71–82 (the twelve boards) all read 1,160, the board files'
  size. **Held — and for kind 26 this also fixes the index a requester passes: the array
  position, which the `.nmb` sheet had left open.**
- *Does `0xFFFFFFFF` mean absent or unbounded?* The read issuer compares the entry with `-1` and
  refuses the request (`002DF7B0`–`002DF7B9`); the builder treats a non-positive size as unrounded
  (`0032E43B`). **Absent.**
- *Does the retail engine read it at all?* The `fread` is in `ResourcePath_Init`'s tail, reached
  once from boot, and a short read is fatal. **Yes, and unconditionally.**
- *Could the override array at `022C51F0` be the loose-file loader's hook?* It is cleared at init
  (`0032EA90`) and no writer of its entries was found by a rip-relative scan; the loose-file check
  is instead the first step of `002DF780`. *Answered 2026-09-13 (DG-6):* nothing fills it — the 256-pointer array at `022C51F0` is **never filled in this build**. Its only references are the resource initialiser `0032EA90`, which zeroes all 256 qwords (`0x20` iterations of 8 stores, `0032EAB1`–`0032EAD8`), and the two size readers `0032E400` and `0032EB40`, which fall back to the `.fst` table (`002DF960`) whenever the pointer is null. Controls: the RIP scan that finds those three sites finds no other; no absolute displacement and no data qword addresses the array. So every request size comes from the `.fst`, and the pointer path — which skips the round-up to 64 — is dormant.

## 7. What this document does not claim

- ~~**What fills the per-kind override arrays at `022C51F0`**, if anything does in a stock install.~~ **Nothing
  found (DG-6, 2026-09-13):** the 256-pointer array at `022C51F0` is **never filled in this build**. Its only references are the resource initialiser `0032EA90`, which zeroes all 256 qwords (`0x20` iterations of 8 stores, `0032EAB1`–`0032EAD8`), and the two size readers `0032E400` and `0032EB40`, which fall back to the `.fst` table (`002DF960`) whenever the pointer is null. Controls: the RIP scan that finds those three sites finds no other; no absolute displacement and no data qword addresses the array. So every request size comes from the `.fst`, and the pointer path — which skips the round-up to 64 — is dormant. A write through a pointer computed from an unrelated base would
  escape these instruments.
- **The request queue** beyond the placement of the size — the 64 slots' state machine, the chunked
  mode, and the completion callback are unread (**FZ-12**).
- **Why ten kinds are unsized** although four of them have path arrays — whether those paths are
  loaded by another mechanism or are dead.
- **The two byte-identical pairs among the twelve files** are not identified here.

## 7b. What else is in the 41 path arrays - and the eight formats that are not explained (2026-09-13, `OPUS-FORMAT-REACHABILITY`)

`ResourcePath_Init` (`002DF9A0`) installs the per-language path arrays. **Reading what is in them
settles a question the format census could not:** whether the eight archive extensions with no
disposition are reachable by this build.

They are. A sample of one array:

```
01E8B1F0 -> ...\in\ExFont\font_stf_a_normal.btm      <- undispositioned
01E8B208 -> ...\in\ExFont\font_stf_b_shadow.btm      <- undispositioned
01E8B230 -> ...\in\Bin_Menu\Loca_gil.cl2             <- undispositioned
01E8B240 -> ...\in\Bin_Menu\Loca_rbl.cl2             <- undispositioned
01E8B260 -> ...\in\worldmap\bin\AreaTim2\loca_00.tm2  <- DOCUMENTED (tim2 sheet)
```

**The undispositioned formats are interleaved with documented ones in the same array**, and every
one of their path strings is a member of such an array: `.cl2` 27/27, `.btm` 24/24, `.lst` 10/10,
`.as7` 18/18, `.mg` 2/2, `.mrp` 84/94. The control is `.ebp` at **10,380 / 10,380**.

**Exactly one function references the whole manifest region** - `002DF9A0`, 24 rip-relative
references, and nothing else in the image touches it.

> ### This does NOT disposition them, and `formats_explained` does not move
>
> Being **reachable** is not being **explained**. `check_assets.py`'s bar for `explained` is a sheet
> with the loader contract - what the engine reads, rejects, clamps and ignores - and none of these
> eight has one. The dimension stays at **40 / 48**.
>
> What this section removes is a *wrong* disposition: **they are not dead PS2-era baggage, and they
> may not be cleared as such.** The magic-based censuses that suggested otherwise were blind, and
> the controls that prove it are in
> [`EVIDENCE-STANDARD`](../../_index/EVIDENCE-STANDARD.md) amendment 2026-09-13e.

**The eight, with their leading signatures**, so the next person starts from the bytes:

| ext | files | signature | note |
|---|---:|---|---|
| `dat` | 2,948 | `'himg'`, `'hdat'`, `01 00 00 00` | several layouts under one extension |
| `bin` | 1,439 | `'sloc'`, `'st2e'`, `'gmap'`, `'hctg'`, `'FLAG'`, `'CCdd'` | several layouts; `st2e` is documented |
| `mrp` | 116 | `4D 52 50 00` = `MRP\0` | uniform across the sample |
| `cl2` | 20 | `'CLT2'` | uniform; sits beside `.tm2` in the arrays |
| `as7` | 18 | `41 37 00 40` / `41 37 0C 18` | two variants |
| `btm` | 12 | `00 00 00 00` | no magic; the `ExFont` bitmap fonts |
| `lst` | 9 | `'qstl'` | uniform; the quest list beside `menuquest*.bin` |
| `mg` | 2 | `10 00 00 00` | `WorldMap\meshdata.mg` |

**Open:** none of the eight has a loader sheet, and `dat` and `bin` cannot get one row each - the
census already refuses to disposition an extension with several signatures, and both have several.

> *Re-derived 2026-09-18 (FABLE):* the reservation above is closed by the sheets written since. `check_assets.py` now lists **six of the eight as explained**, each with a loader sheet in [PS2-Image-Data-Formats](../PS2-Image-Data-Formats/README.md): [`mrp`](../PS2-Image-Data-Formats/mrp-menu-resource-packages.md), [`cl2`](../PS2-Image-Data-Formats/cl2-menu-colour-tables.md), [`as7`](../PS2-Image-Data-Formats/as7-menu-graphics-containers.md), [`btm`](../PS2-Image-Data-Formats/btm-exfont-bitmaps.md), [`lst`](../PS2-Image-Data-Formats/lst-menuquest-list.md) and [`mg`](../PS2-Image-Data-Formats/mg-worldmap-mesh.md); and **`dat` and `bin` as buckets** ([the dat and bin extension buckets](../VBF-Archive-And-Authored-Tables/the-dat-and-bin-extension-buckets.md), [the bin_menu image families](../PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md)), which is the only disposition the sentence above said a multi-signature extension could take. The status line follows. The eight sheets carry their own open questions; none of them is this page's.

## 8. Related

- [`README.md`](README.md) — the loose-file family this sheet belongs to; its three questions are answered above.
- [`area-nmb-index.md`](../VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md) — the 41 path arrays the table is indexed against.
- [`how-the-bigfile-index-loads-and-is-verified.md`](../VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md) — the archive read the issuer falls through to.
- [`license-board-grid-format.md`](../../12-Items-Equipment-Shops-License/license-board-grid-format.md) — kind 2 ids 70–82.
- [`authored-data-table-registry.md`](../authored-data-table-registry.md) — the twelve registry slots the boards are loaded into.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

The twelve tables were read from the install.

| claim | measured |
|---|---|
| 12 of 12 `.fst` present | **12** — ASIA, CH, CN, DE, ES, FR, IN, IT, JP, KR, UK, US |
| 820,000 B each = 41 × 5,000 dwords | **820,000** for every one, and `41 × 5000 × 4 = 820,000` |
| dword 0 = `0x39` = 57 | **`0x39`** |
| US: 31 of 41 kinds populated, 10,521 entries | **31** and **10,521** |
| the ten empty kinds | **`3, 6, 17, 18, 27, 29, 31, 35, 36, 40`** — exactly those ten, in that order |
| kind 1 ASIA 2 against US 24; kind 7 ASIA 541 against US 536 | **2 / 24** and **541 / 536** |

> **The positive control closes across two files and two routes.** Dword 0 is **57**, and
> `PS2Data\cdi\in\system.cnf` — extracted from `FFXII_TZA.vbf` in the same session for
> [the standard-formats sheet](../Standard-Formats/shipped-standard-formats.md) — is **57 bytes**.
> The table's first entry and the file it describes were measured independently and agree.

### ⚠ Seven kinds differ between ASIA and US, not four

Comparing the two tables **byte for byte per kind**:

| kind | entries that differ |
|---:|---:|
| **5** | **533** |
| **8** | **181** |
| 12 | 130 |
| 7 | 34 |
| **2** | 27 |
| 1 | 23 |
| 9 | **1** |

**Kinds 2, 5 and 8 are missing from the row**, and **kind 5 is the most divergent of all** — 533
entries, four times kind 12's. Meanwhile **kind 9, which the row does name, differs in exactly one
entry** out of 5,000.

The row is also true under only one reading. By **population** the differing kinds are **1, 7 and
12**; kind 9 holds **26 entries in both**. So "ASIA differs from US in kinds 1, 7, 9 and 12" is a
*by-value* statement — and read that way it is **incomplete by three kinds**, including the largest.

> Which makes the gloss *"the text-bearing kinds"* unsafe as well: whatever kind 5 is, it changes
> more between these two languages than any kind on the list, and nothing here identifies it. The
> characterisation is left struck rather than replaced — naming the kinds needs the path arrays, not
> this table.

**Not claimed:** `ResourcePath_Init`, the `02EC3EE0` load, the request builder's sizing and the read
issuer's `-1` refusal were **not** re-derived; the per-kind path-array census the row's gloss rests
on was not re-run. The other ten languages were read only for their sizes. Nothing was executed or
observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**ActorEntity, Presentation and Script_VM_Native_Bridge — CLIENT.** The path family `0032E400` (size) / `0032E620` (request) is also issued by `ActorResource_BeginPrimaryPayloadLoad`, `ActorResource_BeginManagerResourceSetLoad` and a 3,882-byte actor loader, by two Presentation bodies (119 B and 337 B) and by script-verb bodies (75 B and 115 B). The 177-byte Input-filed item-graphics loader is another client.

- **Presentation and Audio — CLIENT.** The ~~loose-file~~ open `001D6F20` *(corrected 2026-09-27, FABLE, Claude Opus 5.5: a stream open that the resolver serves from the RAM file cache or the `FFXII_TZA.vbf` archive, never a loose file - [record](../../_index/candidates/pc1-config-route/README.md))* is shared with `AddMotion_LoadResources`,
  `AddMotion_LoadHighModelReplace`, `AddMotion_LoadSkeletonMapping` and a 451-byte Audio body. `001D6B40` is read by a
  715-byte Audio-filed body. `0032E070` calls a 297-byte Presentation body.
- **ActorEntity — SERVICE.** `ActorResource_BeginPrimaryPayloadLoad` calls `0032EB40`. The boot
  initialiser runs `BattleStorage_InitializeWorkArrays`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**RNG_Random_Selection — SERVICE.** `0022A0B0` on this page calls `RNG_MT19937_Seed`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863D30` - onto the CRT's Mersenne Twister seed; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — CLIENT (SWE2-EC7 batch-148).** The `0046DD50` entry's `0053DD10` quiet-check is a shared gate also called by that layer's `0022B6E0` - the fst state stepper borrows the shared quiet-check; no scheduler state lives here.

**UI — CLIENT (SWE2-EC7 batch-148).** The same `0053DD10` is called by `003C80C0` of that layer - a mechanical user of the shared gate, nothing more.

**WorldAreaField — CLIENT (SWE2-EC7 batch-148).** `0053DD10` is likewise called by `003789A0` of that layer, and the `0032E400`-family submit helpers this page already names carry the rest of the field-layer traffic - shared-callee fan-in, not a resource-table relationship.

**Save_Load_Settings — CLIENT (SWE2-EC7 batch-150).** The `001D6FB0` read-item constructor's alloc/enqueue triple `001A1220`/`001A0A90`/`001A0BB0` is shared with that layer's `001C1810` - the same queue machinery the save-image code drives, not a save-format relationship of the fst.


**Platform — CLIENT (SWE2-EC7, batch 169).** The batch-169 `0019AFE0` record-commit's `0019AA20` field-write arm hands to `0019A510` of that layer - a mechanical shared-callee the commit path rides, not a platform relationship of the fst machinery.

## The `0032EA90` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0032EA90` (~126 B) — `0032E450()` then `003EB050()`, clears
`022C51E0`/`022C51F0` (`0032EA94`/`0032EAA7`).

| member | role | interior |
| --- | --- | --- |
| `0032E450` | sets `01EED498 = 1`, walks `022C31D8` (`0032E453`/`0032E460`) | [`0032E453`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003EB050`.

## SWE2-EC7-80 update (2026-09-20) - `00597930` context-record init measured

`00597930` (59 B) is the 0x30-byte context ctor the `001D6F20` caller
uses: `qword[+8] = -1`, `dword[+0] = 0`, `qword[+0x10] = 0`,
`qword[+0x20] = -1`, `dword[+0x28] = 0`, `byte[+0x18] = r9b`; a
non-NULL `rdx` then runs `0059EE90` (the payload fill) and `rcx`
returns - the -1-sentinel record the FST callers populate.
Interior anchor `00597945` (the `+0x10` zero).

`0059D900` (27 B) is the three-field `is-set` predicate `001A0E50` and `001D6F20` consult: returns `0` iff `+8` is `-1`, `+0x10` is `0`, and `+0x20` is `-1` — the union-source record's `unset` shape (no handle, no object, no size); any single field differing makes the source live.

Interior anchor `0059D90E` (function `0059D900`).

`0059A9B0` (293 B) is the union-source commit-and-release `0059EE90`'s payload fill ends in: resolves `001D6BB0([rcx], [rcx+0x18] != 1)` into a base, then reads the position via the `+0x10` object (`002150E0`), the `+8` handle (`008C2140` import into a stack out-param), or the `+0x20` size (`001D6CA0`); a position mismatch against `[rcx]` logs the `00D279A0` `ready byt...` string via `005CDAA0`. It then releases the source — `002150D0` on the object, two IAT calls plus a `-1` store on the handle — writes `001D6A20`'s result into `+0x20`, and frees the base via `001D6B00` when that result is non-positive.

Interior anchor `0059AA27` (function `0059A9B0`).

`00599250` (307 B) is the UTF-8-to-UTF-16 converter `0059EE90` runs on name strings: a byte cursor feeds `0059A600` (the UTF-8 decode) until NUL; decoded values `<= 0xFFFF` outside `0xD800..0xDFFF` write one word, values `<= 0x10FFFF` above that emit a surrogate pair via `-0x10000`, `& 0x3FF`, `0xD800`/`0xDC00` biasing (constant-folded as `-0x2400`/`-0x2800`); a terminating NUL is written and the word count returned, negated on bounds failure against the `rsi` end pointer.

Interior anchor `005992C5` (function `00599250`).

`002150E0` (38 B) is the object-source advance `0059A9B0`'s `+0x10` arm calls: runs `00215110` on the object and, when it returns nonzero, adds the result into `[rcx+0x20]` (the union-source position field `0059D900`'s predicate reads) and returns it; a zero result returns 0 untouched — a bounded tell/step, not a transfer.

Interior anchor `002150F4` (function `002150E0`).

`002150D0` (12 B) is the object-source release `0059A9B0` runs after the commit: tail-jumps to `001F4840` with `rcx = [rcx+0x10]` (the object) and `rdx` = the union record — the callee owns the teardown, this stub only rearranges the two pointers.

Interior anchor `002150D3` (function `002150D0`).

`001D6CA0` (61 B) is the size-source path `0059A9B0`'s `+0x20` arm takes: calls `0020C700` on the size value, then tail-jumps to `0020C150` forwarding `(result, rdx, r8, r9d)` unchanged — a two-stage resolver, so the semantic content lives in the two callees.

Interior anchor `001D6CB8` (function `001D6CA0`).

`00215110` (267 B) is the ring-buffer dequeue `002150E0` wraps: `edi = min(r8d, dword[[rcx+0x18]+8] - [rcx+0x20])` clamps the request (empty window returns 0), the cursor `rbx = [rcx+0x20]` is ranged against the `[[rbp+0x28]+0x10]..[+0x8]` window over base `[r9]`; a contiguous span takes one `00861EBA`, a wraparound takes two with `rsi` bytes carried to `r14+rsi` and `rbx` advanced, and a shortfall beyond the window pulls the head segment instead; the remainder runs `0019B1F0` then `0019AFE0(rbp, rbx, r14, edi, [rbp+0x10])` with `esi` added back - the bounded two-segment read the size-table stream exposes.

Interior anchor `00215182` (function `00215110`).

`0046DD50` (251 B) is the `02CA6068` state stepper the pump `0032E070` runs: after the `0016D6A0` fill, state 4 gates on `0053DD10` and clears, state 3 needs `0053DD10` + `00368F30` quiet then arms `00369050` on `00536F30` and steps to 4, state 2 does `0053DD10` + `00368F30` then zeroes the state, and state 1 sizes the next stage from `02EBB52C`/`02EBB528`/`02EBB520` (each `(x + (x>>31 & 0x7FF))` rounded down by `>> 0xB`) into `02EBA520` via `0016D6A0` before stepping to 3 - the four-state load pipeline the pump advances

Interior anchor `0046DD97` (function `0046DD50`).

`001D6FB0` (236 B) is the queued read-item constructor the read issuer `002DF780` uses: under two `001A1220` checks it stamps `01F82CC0` with the caller's out pointer (first dword `-1`), allocates the record via `001A0A90`, fills `+0` = `3`, `+8` = callback `001D6D70`, `+0x10` = `0`, `+0x18` = `1`, copies the NUL-terminated path into `+0x20`, stores the argument quad at `+0x120`/`+0x128`/`+0x130`/`+0x138`, and enqueues through `001A0BB0` - the asynchronous half of the `(kind, id)` read

Interior anchor `001D7040` (function `001D6FB0`).

`001D6D90` (225 B) is the kind-`2` sibling of the `001D6FB0` queued-read constructor `002DF780` issues: same two `001A1220` gates, out pointer into `01F82CC0` (first dword `-1`), `001A0A90` record with callback `001D6D70` at `+8`, `+0x10 = 0`, `byte +0x18 = 1`, kind `2` at `+0`, the NUL-terminated path copied into `+0x20`, the argument quad at `+0x120`/`+0x128`/`+0x130`, enqueued via `001A0BB0` - the second asynchronous `(kind, id)` read shape

Interior anchor `001D6E2F` (function `001D6D90`).

`002DF6C0` (192 B) is the gated submit-or-decline wrapper `0032E070` runs per request: three admissions must pass in order (`0017D930`, `001D6EF0`, `001D6B40` on `rcx`) before `001D6F20(rcx, 1)` builds the request object and `001D6FB0` configures it with the `0215EFF4` status cell, the `ebp`/`r9d` parameter pair and the `r14` source; a live object is then `001D6E80`-fired, while any gate failure falls to `001D6D90` reporting through the same `0215EFF4` cell - decline is still reported, just on the other lane

Interior anchor `002DF719` (function `002DF6C0`).

`001D6EF0` (41 B) is the two-flag readiness test `002DF6C0` (and sibling submitter `002DF780`) consults before building a request: `001A1220` resolves the shared status record and the predicate returns `1` only when both `[rax+0x69]` and `[rax+0x68]` are nonzero - the pipeline's open-for-work byte pair behind the request queue

Interior anchor `001D6EF9` (function `001D6EF0`).

`0019AFE0` (144 B) is the record-commit `00215110`'s dequeue runs after the bounded read: `0019A770` find-or-makes the record, `0019A860` zero-arms it and `0019AA20` writes the fields, then `dword[rbx+0x88]` decides - 5 means `0019A9B0(rdi, rbx)` finalises it and the function returns `r8d`, anything else falls to the 0 arm - the head-of-line commit the stream pairs against its dequeue.

Interior anchor `0019B02E` (function `0019AFE0`).

`0019A860` (326 B) is the chunked stream-read `0019AFE0`'s record-commit pairs against `0019A770`: on the record it zero-arms it walks the u16 block table in `0x10000` granules, issues bounded reads through the `008C2EF0` import thunk for each occupied span, and advances the `+0x88` phase field as bytes land - the data-fill half of the FST stream pair.

Interior anchor `0019A900` (function `0019A860`).

`0019A770` (234 B) is the find-or-make `0019AFE0` calls before `0019A860` fills: the u16 block table and `0x10000` granule math locate or mint the stream record for the requested range, `+0x88` carries the phase the commit reads afterward, and import-thunk `008C2EF0` does the underlying reads - the record-side of the FST stream pair.

Interior anchor `0019A7EB` (function `0019A770`).
