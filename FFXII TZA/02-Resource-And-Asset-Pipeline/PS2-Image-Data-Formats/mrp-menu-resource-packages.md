---
system: The `MRP` menu rect/element package — `mrp_menu/*.mrp`
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation) — the tail table, the descriptors' draw side and table B are answered from the typed-list and map-pack pages (2026-09-30); the manifest premise refuted (RC-29: 008FCE00 is the developer console's page table; four unrequested .mrp files come through .rdata id lists of 003933F0 / 00393460) (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 40 addresses cited - 7 data, 24 entry, 9 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all shipped .mrp files extracted from FFXII_TZA.vbf and hashed, 2026-09-14; directory arithmetic verified on the full population; native relocator read at 002A00F0"
archive_formats:
  - "mrp | explained | Menu rect/element package — relocated-pointer table container; relocator 002A00F0 rewrites offsets in place and flips magic byte +3 as the flag."
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The `MRP` menu rect/element package — `mrp_menu/*.mrp`

> **A relocated-pointer table container for menu layout data.** Every menu screen ships a `.tm2`
> image (the pixels) and a `.mrp` of a few hundred bytes — a directory of record tables whose file
> offsets the loader rewrites into live pointers **in place**, flipping the magic's fourth byte as
> the "already relocated" flag. That is why `MRP\0` occurs **zero times in `.text`**: `+3` is not a
> terminator, it is a flag, and after load the buffer reads `4D 52 50 01`.

**Corpus validation, before anything else.**

|| |
|---|---|
| files examined | **116 of 116** shipped `.mrp` entries in `FFXII_TZA.vbf`, extracted and SHA-256'd — **52 distinct contents**; most rows are locale-duplicated copies |
| directories | `ps2data/image/ff12/myoshiok/<lang>/mrp_menu/` — all 9 languages **plus `in_sdver`** |
| size range | 128 B (`nowload.mrp`) – 7,696 B (`party_book.mrp`) |
| magic `MRP`+flag | 116 of 116 begin `4D 52 50 00`; the `00` is the un-relocated flag, not a terminator |
| `title_fore3.mrp` | ships only in `de` `es` `fr` `in` `it` — **absent in `us` `ch` `cn` `kr` `in_sdver`** |

All sizes, paths and hashes are frozen at
`Tools/work/DATA/extract/manifest.tsv` (177 rows covering this and the five sibling formats).

## 1. What the player sees

Every fixed menu backdrop — the title screen, game-over card, save/load chrome, shop frame, quest
board, party book, the "NOW LOADING" strip — is a `.tm2` sheet plus one of these files saying
**which rectangles of that sheet land where**. A `.mrp` is therefore small even when its `.tm2` is
huge: `quest.mrp` is 3,072 B next to `quest_c.tm2` at hundreds of KB.

## 2. The layout

### 2.1 The directory — a run of `{count, offset}` table slots, `+0x04` .. `+0x2F`

The relocator `002A00F0` (§3) rewrites three of the offsets in place, which fixes what the header
*is*: not a fixed layout but **a run of table slots**, each `{u32 count, u32 fileOffset}`:

```struct MrpHeader base=file size=0x30
+0x00  char[3]  magic       'MRP' - 4D 52 50, in 116 of 116 files
+0x03  u8       relocated   0 on disk ('\0' of the shipped magic); set to 1 by 002A00F0 after the relocation pass — a second pass is skipped
+0x04  u32      tailCount   records in the tail table (0x10 bytes each); nonzero in shipped files
+0x08  u32      tailOff     file offset of the tail table — REWRITTEN in place to a buffer-absolute pointer
+0x0C  u32      spareCount0 0 in 116 of 116 files
+0x10  u32      spareOff0   file offset; equals file size in 116 of 116 (an empty table parked at EOF)
+0x14  u32      spareCount1 0 in 116 of 116 files
+0x18  u32      spareOff1   file offset; equals file size in 116 of 116
+0x1C  u32      descCount   records in table A (0x14 bytes each) — the descriptor array; nonzero
+0x20  u32      descOff     file offset of table A — REWRITTEN in place; 0x30 in 116 of 116 (immediately after this directory)
+0x24  u32      tableBCount records in table B (0x0C bytes each); 0 in 116 of 116 files
+0x28  u32      tableBOff   file offset of table B — REWRITTEN in place; equals file size in 116 of 116 (empty table at EOF)
+0x2C  u32      unk2C       header tail; the {count,offset} run ends at +0x2C — whether this lone u32 is a fifth count, a spare, or unused is not established *(2026-09-30, OPUS: the header relocator `002A00F0` reads `+0x24` and `+0x28` and never `+0x2C`; no reader on the header path, a declared limit)*
```

> **The "three size fields" are not sizes — they are parked offsets.** Earlier reading of this
> directory called `+0x10`/`+0x18`/`+0x28` "file size, three times". They *equal* the file size in
> every shipped file **because their counts are zero and an empty table sits at EOF** — a
> coincidence of emptiness, not a type. The relocator treats `+0x20` and `+0x28` as offsets; the
> whole `+0x0C`..`+0x2F` run reads as `{count, offset}` pairs.

### 2.2 Table A — descriptor records, `0x14` bytes, 1,458 records across the corpus

```struct MrpDescriptor base=record size=0x14
+0x00  u8   index    small ascending values 0..9 (427 records carry 1, 217 carry 2 …)
+0x01  u8   sub      0,4,8,12,16,20,24,28… — steps of 4 within a file
+0x02  u8   _zero2   0 in every observed record
+0x03  u8   tag      0x10 in 1,403 of 1,458 records; 0x00 in the remaining 55 — a class/variant byte, not a constant
+0x04  u16  u        source-space coordinate (values like 0x1C0, 0x1DA)
+0x06  u16  v        source-space coordinate
+0x08  u16  w        extent — most common values (1024,896) and (1920,1080): the second is a full-screen rect, so the space is a design/output canvas, not pure texture texels
+0x0A  u16  h        extent, same space
+0x0C  u32  aux      0 in 1,392 of 1,458; small nonzero values (38 ×20, 92 ×10, 22 ×10, 400 ×9, 296 ×7, 8 ×9, 4 ×1) in the rest
+0x10  u32  ref      ROW-RELATIVE offset — the relocator adds the row's own address, so ref points from this record into the payload that follows the descriptor array; in-bounds in 1,458 of 1,458
```

**`ref` is row-relative, proven by the relocator, not guessed**: `002A1AD0 ADD ECX,EBX` adds the
row's address. In `e3_logo.mrp` (one descriptor, `ref` = `0x14`) the target lands at `0x30 + 0x14
= 0x44` — exactly the payload byte after the descriptor array, where the `80 80…` fill begins.

### 2.3 The tail table — `0x10`-byte records, `tailOff` .. EOF

`tailOff + 0x10 * tailCount == fileSize` holds on **all 116 files with zero slack**. Field
structure not decoded this pass. *Decoded since (pointer 2026-09-30, SWE2-CONTRACT):* the table is the file's
**atlas-name array** — 16-byte name records read by `002A0060`, which resolves each against the atlas registry; the
census over all 344 shipped typed lists (116 files and 228 `mrppack_ys` units) finds bounds consistent in every blob
([a typed list, measured once](../a-typed-list-measured-once-and-built-in-one-allocation.md) §5c–§5d,
`members/atlas-name-census.tsv`). Tier 1 + authored data.

### 2.4 Table B — `0x0C`-byte records, empty in every shipped file

Count slot `+0x24` is 0 in 116 of 116; the format has a second 12-byte-record table that ships
empty across the whole corpus. *Refined since (pointer 2026-09-30, SWE2-CONTRACT):* "the whole corpus" holds for the
116 standalone files and for `mrppack_ys` units 13–16. It is the file-row atlas registration table — rows with tag 1
register an atlas through `0024A440`, name at row `+8` (the typed-list page §5d) — and the only populated table B ships
in the map-pack `MRP` section of `rwg0201` / `rwg0202`: two rows naming the map-gauge's `TIM2` images
([the map ctrl pack](../../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md) §2.5).

## 3. The loader contract — **established at instruction level**

`002A00F0(buffer)` is the completion path for `00249320`-wrapped requests. Read against the
shipping bytes ([spawn page §23.2](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)):

| step | what it does |
|---|---|
| guard | `byte[buffer+3] == 1` → skip everything; else run the pass and set it to 1 |
| `+0x08` | rewrite dword buffer-relative → pointer to the tail table |
| `+0x20` | inside `002A1A80`: decode buffer-relative → table A; then walk `descCount` rows of `0x14` B, rewriting **each row's `+0x10`** relative to *that row's address* |
| `+0x28` | decode buffer-relative → table B; walk `tableBCount` rows of `0x0C` B, rewriting each row's `+8` relative to the **table-B base** (`002A0147 ADD ECX,EBP`) |

Encoding: `0020E600`/`0020E620` — `full-64 base + zero-extended-32 encoded value`, minus the
reference window global `01F83530` ([reference contract](../CONTRACT-authored-table-row-lookup.md)).
Counts are compared unsigned; the table-A index is sign-extended first, and **there is no
file-size validation of the offset/count pairs** — a corrupt file is relocated the same way.

The request chain for every constant `.mrp` request in the census
([`members/constant-resource-requests.tsv`](../VBF-Archive-And-Authored-Tables/members/constant-resource-requests.tsv)):

`screen → 00249320 (or 00249350 for w_menu) → 00249210 → 0032E400 size + 0032E620 request`.
`0032E400`/`0032E620` are the generic resource-pool entry points — the same pair is called by
ActorEntity (`0032FCA0`, `00330310`, `003306E0`), Presentation (`003B2310`, `003B53C0`) and Input
(`00291C80`) clients for their own resources; those are fellow API consumers, not `.mrp` readers.
→ on completion the member callback `00249660` (`mov rcx,[member+8]; jmp 002A00F0`) hands the
buffer to the relocator.

| screen / loader | `.mrp` | kind-7 id | site |
|---|---|---:|---|
| title `00393FF0` | `title.mrp` | `0x3A` | `00394048` via `00249320`; also manifest list `008FD010` |
| shop `003F4840` | `shop_new.mrp` | `0x96` | `003F492D` via `00249320` |
| location map `00404060` | `Loca.mrp` | `0xBF` | `00404107` via `00249320`; also manifest list `008FCF60` |
| world map `00562F90` | `w_menu.mrp` | `0xA6` | `00563048` via `00249350`; also manifest lists `008FD170` **and** `008FD278` |
| load menu (reused `00582790`) | `dataface_c` (idx 127) + id 111 | — | `00393460`/`003933F0` — §23.1 |

**The manifest is a second path.** `.rdata` `008FCE00`–`008FD2D0` holds a sequence of 14
`u32-2`-tagged kind-7 id lists (each a screen's resource set; `0xD1`/`0xD2` recur as list tails).
`title`/`Loca`/`w_menu` appear there **and** as constant requests — the manifest is the batch
preload, the constant sites are the direct fetches. The other `.mrp` ids (`gameover`, `quest`,
`save_load`…) are presumably manifest-carried too; the manifest's walker is not isolated (no
rip-relative or pointer-table reference to the block — see `cl2` sheet §3 for the same finding).

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00..+0x02` `MRP` | nothing — the tag is never compared | never | — | **yes — 0 hits in `.text`** |
| `+0x03` relocated | `002A00F0` | second pass skipped if `==1` | written `1` | — |
| `+0x04`/`+0x08` tail | `002A00F0` (rewrite `+8` only) | — | — | row fields: no reader found yet *(since read: the 16-byte atlas-name records, by `002A0060`, §2.3; pointer 2026-09-30, OPUS)* |
| `+0x0C`..`+0x18` spares | nothing found | — | — | **0 in 116 of 116** |
| `+0x1C`/`+0x20` table A | `002A00F0`→`002A1A80` | — | unsigned compare | — |
| `+0x24`/`+0x28` table B | `002A00F0` | — | unsigned compare | — |
| desc `+0x10` ref | `002A1A80` (row-relative rewrite) | — | — | — |
| desc `u,v,w,h` | — | — | — | no reader found — draw side not isolated *(since read: the typed-list decoder `002432B0` and the list drawers `002435C0` / `00243C00`, §7; pointer 2026-09-30, OPUS)* |

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `002A00F0` | the `.mrp` relocator — the parser that makes the buffer live | ✅ §23.2 |
| `002A1A80` | the table-A pass (desc array + row `ref`s) | ✅ §23.2 |
| `00249660` | completion thunk → `002A00F0(buffer)` | ✅ 9-byte body read |
| `00249320` / `00249350` | `.mrp` request wrappers installing the callback | ✅ census + §23.1 |
| `00249210` | pool core — `0032E400` at `00249296`, `0032E620` at `002492F3` | ✅ census |
| `002DF9A0` / `002DFBAF` | kind-7 per-language path-array install | ✅ |

## 5. Corpus survey — 116 files

|| |
|---|---|
| `MRP` + `00` flag | 116 of 116 |
| `descOff` = `0x30` | 116 of 116 |
| `tailOff + 0x10*tailCount == fileSize` | 116 of 116 |
| three spare/B slots = `{0, fileSize}` | 116 of 116 — empty tables parked at EOF |
| descriptor `ref` in-payload bounds | 1,458 of 1,458 records |
| desc tag `+3` = `0x10` | 1,403 of 1,458 (rest are `0x00`) |
| `nowload.mrp` = 128 B | smallest shipped (1 desc, 1 tail rec, 3 parked slots) |
| `party_book.mrp` = 7,696 B | largest; `descCount` = 60 |
| `title_fore3.mrp` | only `de`/`es`/`fr`/`in`/`it` |
| `in_sdver/save_load.mrp` = 2,736 B vs 2,848 B elsewhere | the SD variant differs |

## 6. Falsification pass — 2026-09-14

| attack | result |
|---|---|
| Is `+0x20` a header size or an offset? | **Offset.** The relocator decodes it buffer-relative to reach table A. Its value `0x30` is where descriptors begin. |
| Are `+0x10`/`+0x18`/`+0x28` size fields? | **No — parked offsets.** They equal file size only because their counts are 0; `+0x28` is decoded to table B by `002A00F0`. The "three equal sizes" reading was an emptiness coincidence. |
| Is `ref` section-relative or row-relative? | **Row-relative** — `002A1AD0 ADD ECX,EBX` adds the row address. `e3_logo`'s `ref 0x14` lands exactly past the descriptor array. |
| Does the engine verify `MRP\0`? | **No** — and it cannot: `+3` is consumed as the relocation flag. The format tag is effectively `MRP` + flag byte. |
| Could the relocation run twice on one buffer? | Guarded — byte `+3` is set to 1 at the end and `==1` skips the whole pass. |
| Is `descCount` the descriptor count? | **Yes at relocation level** — `002A1A80` walks `buffer+0x1C` rows of `0x14` B. |
| Is the tag byte always `0x10`? | **No** — 55 of 1,458 records carry `0x00`. It is a class/variant byte. |

## 7. What this document does not claim

- **What the descriptors mean to the draw side** — `u,v,w,h` is rect-shaped (1920×1080 values say
  output canvas); the consumer that walks the relocated table is not isolated. *(Answered since: the 20-byte outer
  records are walked by the typed-list decoder `002432B0`, which builds each record's self-sized items into nodes and
  hands them to the list drawers `002435C0` / `00243C00` — the typed-list page §3 and UQ-76. Pointer 2026-09-30,
  SWE2-CONTRACT.)*
- **The tail table's row fields** and **what requests it for** — `+0x08` becomes a pointer; no
  reader of the records found yet. *(Answered since: 16-byte atlas names read by `002A0060`, §2.3 above.)*
- **Which requester covers** `gameover`/`title_menu`/`save_load`/`E3_Logo`/`quest`/`Party_Book`/
  `nowload`/`title_fore3` — no constant-request site in the census; manifest/dynamic path expected.
  *(`save_load` is resource 111, requested by the save/load controller's setup `00582790` through `003933F0` — the
  typed-list page §5d. The rest is RC-29.)*
- [x] **RC-29.** Which code walks the menu resource manifest (`.rdata` `008FCE00`–`008FD2D0`) that preloads the `.mrp`
  ids with no constant request. Shared with [the CLT2 sheet](cl2-menu-colour-tables.md) §7. Registered 2026-09-30
  (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-29:* **ANSWERED 2026-09-30 with the premise refuted (static; SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §3, commit `1261e2044`, `manifest_walker.py`): `008FCE00` is the developer console's page layout table, not a resource manifest** — 14 pages × 22 rows of u32 command ids (stride `0x58`, `0x4D0` bytes), read by the label filler `001D0390`, the page-header refresh `001D5260` and the row renderer `001CD0E0` (three rip-relative references and one image-base-relative read). The page's "no rip-relative … reference reaches the block" was a narrower sweep. Four of the unrequested `.mrp` files come through `.rdata` id lists of `003933F0` / `00393460`.
- **The spare `{count,offset}` pairs' table strides** — empty in all 116 files; nothing walks them.

*Superseded reading, 2026-09-30 (SWE2-CONTRACT): §3's "manifest is a second path" is refuted by RC-29 — `008FCE00` is the developer console's page table; four of the unrequested `.mrp` files come through `.rdata` id lists of `003933F0` / `00393460` (SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §3, commit `1261e2044`).*

## 8. Related

- [`README.md`](README.md) — the `ps2data/image` long tail and the kind-7 mechanism.
- [`constant-resource-requests.tsv`](../VBF-Archive-And-Authored-Tables/members/constant-resource-requests.tsv) — the request census.
- [`spawn-placement-and-retirement.md` §23](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) —
  the relocator reading this sheet's loader contract rests on.
- [`tim2-images-and-the-seven-slot-registry.md`](tim2-images-and-the-seven-slot-registry.md) — the `.tm2` pixels.
- `Tools/work/DATA/extract/manifest.tsv` — frozen path/size/hash rows for the whole population.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions or is named as the page reads it.*

**ActorEntity, WorldAreaField, World, Presentation, Input, Save_Load_Settings, Script_VM_Native_Bridge — CLIENT (request path).** These layers use the generic pool entry points this page names: the per-kind size lookup `0032E400` (`[022C51F0][kind][id]`, `id < 0x400`) and the request queue `0032E620`. The actor loaders `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`, reached from `0032FC30`), `ActorResource_BeginPrimaryPayloadLoad` (`00330310`) and `003306E0` call them, along with their own calls (`002628B0`, `0032ED80`, `00263FF0`, `003304A0`, and `003306E0`'s calls to `002561C0`, `002566E0` and `0037DC30`). The field loaders `MapRef_BeginLoadResources` (`00268750`), `003319D0`, `00378030`, `00379A10` and `AreaArd_LoadOrUnloadFieldResource` (`003EA820`) call them, as do `00378540` and the render bodies `003B2310` / `003B53C0` (reached from `003B25D0` and `CharacterRenderSystem_Initialize` `004269A0`). So do `00291C80`, the save-slot loader `002EF300` and the script adapters `0050DF70` / `0050DFE0`, which pop their arguments through `00267E10`; `0050DF70` writes the result through `0026B4E0`, while `0050DFE0` queues through `0032E620`. These are fellow API consumers for unrelated resources, not readers of this format.

**Presentation, Audio, PlatformOnlineAchievements, WorldAreaField, CoreRuntimeScheduling, SaveLoad — SERVICE and CLIENT (menu drawers).** The row renderer `001CD0E0`, the label filler `001D0390` and the page-header refresh `001D5260` read the packages and call each other. `001CD0E0` also calls `001DCD30`, `002DEBA0` (Audio), `003166F0`, `FieldData_GetVariable0` (`00265270`) and `WorldTransition_GetTransitionFieldId` (`00314910`), and it is reached from `001D0190` / `001CCB20`. The list drawers `002435C0` / `00243C00` call `0029ED50`, and `00245E60` calls `002435C0`. The atlas-name resolver `002A0060` resolves each record through the image-address codec and is called by `0029F130`. The boot pass `0022A0B0` calls the path-array install `002DF9A0`, and `00582790` loads through `00249210`, `003933F0` and `00393460`, called by `SaveLoad_ControllerLifecycleHandler` (`00582860`). `00291D90` calls the label helper `0024A440`. These are shared drawers and loaders; the package format stays this page's.
