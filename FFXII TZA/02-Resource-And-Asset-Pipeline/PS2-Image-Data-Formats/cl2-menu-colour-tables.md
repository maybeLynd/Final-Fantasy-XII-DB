---
system: The `CLT2` colour table — `bin_menu/loca_*.cl2`
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation; superseded readings are marked on the page) — the manifest premise refuted (RC-29: 008FCE00 is the developer console's page table); RC-30 answered 2026-09-30: 003C1F00 requests the file (kind 7 id 0xE1 + menumap_common entry byte +1; only loca_gil and loca_bhm are selected, loca_rbl never), 003C26C0 reads it as a TIM2-shaped CLUT, the variant is not read, and the upload 0017F3B0 builds an RGBA8 texture and rescales byte 3 as a PS2 alpha (SWE2-DATA, ORACLE; RC-30 round 3, SWE2-CONTRACT); no register row open on this page (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Menu.LocationMap
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 10 addresses cited - 4 data, 3 entry, 2 interior, 1 literal, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all 20 shipped .cl2 files extracted from FFXII_TZA.vbf and hashed, 2026-09-14; header arithmetic verified on all 20"
archive_formats:
  - "cl2 | explained | CLT2 colour table — 0x40 header, u16 count at +0x1E, count x 4-byte palette at +0x40; location-map pages."
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The `CLT2` colour table — `bin_menu/loca_*.cl2`

> **A palette/colour table for the location-map pages.** `CLT2` — PS2-era "CLUT v2" naming — a
> `0x40`-byte header whose second u16 of `+0x1C` is the entry count, followed by `count × 4` bytes
> of colour data. `Loca_bhm`/`Loca_gil` carry 512 colours; `Loca_rbl` carries 32.
> `dataSize + 0x40 == fileSize` in every shipped file.

**Corpus validation, before anything else.**

|| |
|---|---|
| files examined | **20 of 20** shipped `.cl2` entries — `loca_bhm` ×9, `loca_gil` ×9, `loca_rbl` ×2 — **3 distinct contents**; every same-name copy is byte-identical |
| magic `CLT2` | 20 of 20 (3 distinct) |
| locale duplication | nothing differs by language — each name's copies across locale dirs are hash-identical |
| `+0x14` (dataSize) `+ 0x40 == fileSize` | 20 of 20 |
| palette size `== +0x1C.hi16 × 4` | 20 of 20 — `0x200×4=0x800` for bhm/gil, `0x20×4=0x80` for rbl |

## 1. What the player sees

The Location map (the floor-plan / region inset) — `bhm`, `gil`, `rbl` are the authored map pages
(Bhujerba-class named locations). The `.cl2` carries the colours the page's indexed art resolves
through; the `.mrp` sibling says where the pieces land.

## 2. The layout

```struct Clt2Header base=file size=0x40
+0x00  char[4]  magic     'CLT2' - 43 4C 54 32, 20 of 20
+0x04  u32      tag       0x00010004 in 20 of 20 — a constant, version-or-type shaped
+0x08  u32      _zero08   0 in 20 of 20
+0x0C  u32      _zero0C   0 in 20 of 20
+0x10  u32      endOff    dataSize + 0x30 in 20 of 20 (0x830 for the 0x800 palettes, 0xB0 for 0x80) — reads as a data-end offset parked 0x10 short of EOF
+0x14  u32      dataSize  fileSize - 0x40 in 20 of 20 (0x800 / 0x80) — palette byte size
+0x18  u32      _zero18   0 in 20 of 20
+0x1C  u16      fieldLo   0x30 = 48 in 20 of 20 — constant; possibly a stride/flags slot
+0x1E  u16      count     palette entry count — 512 (bhm/gil) or 32 (rbl)
+0x20  u16      _zero20   0 in 20 of 20
+0x22  u8       kindLo    0x03 in 20 of 20
+0x23  u8       kindHi    5 in the 512-entry files, 4 in the 32-entry — correlates with log2 of entry count (2^5=512-row space? no — 5 vs 4 tracks entry-count, meaning unknown)
+0x24  u32[7]   _zero24   all zero in 20 of 20
```

```struct Clt2Palette base=+0x40 size=count*4
+0x00  u8[4]  entry   4 bytes per colour. The 4th byte is 0..255 ALPHA, not the PS2 0..128 convention: in the 512-entry files max = 0xFF, 0x80 occurs ZERO times, 0xFF occurs 239 of 512 (OPUS measurement, re-verified on us/loca_bhm)
```

*TIM2 reading, 2026-09-30 (SWE2-CONTRACT, RC-30 round 3; SWE2-DATA's `_index/candidates/rc30-census-0930/` §4 and ORACLE's `_index/candidates/rc30-cl2-request-bounds-0930/` §3, static):* the file is a one-picture TIM2-shaped container with no image. In TIM2 picture-header terms `+0x10` is the picture total size, `+0x14` the CLUT size, `+0x18` the image size (0), `+0x1C` the header size (`0x30`), `+0x1E` the colour count, and `+0x22` / `+0x23` the ClutType / ImageType pair (3 with 5 or 4: 32-bit colours with an 8-bit or 4-bit image). The reader uses `+0x18`, `+0x1C` and `+0x1E` only (§3).

*Palette alpha on upload, 2026-09-30 (SWE2-CONTRACT, `_index/candidates/swe2contract-rc-round3-0930/` B4 and B7, static + the 20 shipped files):* the upload `0017F3B0` rescales byte 3 of every entry as a PS2 alpha, `min(255, trunc(a × 255 / 128))` (`0017F517`–`0017F54A`, scale `008C5B34` = 1/128). In all three distinct files every 4th byte is either `0xFF` (239 of 512 in `bhm` / `gil`, none in `rbl`) or at most `0x6F`. So the engine reads the byte on the PS2 `0`–`0x80` scale; `0xFF` saturates to fully opaque, and `0x6F` displays as 221. The measurement above (max `0xFF`, no `0x80`) stands as a description of the file bytes.

The palette bytes are real colour data, not ASCII — the earlier "embedded ASCII `220`" reading was
component bytes `0x30..0x39` coincidentally in the digit range.

> **Correction note (2026-09-15):** an earlier revision of this sheet placed every field one dword
> too low (endOff `+0x0C`, dataSize `+0x10`, count `+0x1A`, kinds `+0x1E`/`+0x1F`) and carried a
> reconciliation note claiming OPUS's +4-higher numbering was the shifted one. Re-verified against
> the raw bytes (`us/loca_bhm.cl2`: `30 08 00 00` at `+0x10`, `00 08 00 00` at `+0x14`,
> `30 00 00 02` at `+0x1C`, `00 00 03 05` at `+0x20`): **OPUS's offsets were correct** — endOff is
> `+0x10`, dataSize `+0x14`, count the u16 at `+0x1E`, kinds `+0x22`/`+0x23`. The earlier pass had
> confirmed `+0x04 = 0x00010004` but did not re-check the higher fields before writing.

## 3. The loader contract

|| |
|---|---|
| request path | ~~**no constant-request site in the census**~~ *(superseded by RC-30: the request is `003C1F00`'s computed site `003C208D`, see the answered contract below)* — the `.cl2` ids ride the **menu resource manifest**: `008FCE00`–`008FD2D0` in `.rdata` is a sequence of 14 `u32-2`-tagged id lists; the third (`008FCEB0`) opens `0xDF, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5…0xF2, 0xD1, 0xD2` — the `Loca`/`bin_menu` set. `0xD1`/`0xD2` recur as list tails. **No rip-relative reference and no pointer-table entry reaches the block** (both scans run) — the walker addresses it by index/base not yet identified |
| kind-7 ids | `0xE2`–`0xE4` per the path arrays (`Loca_bhm`/`Loca_gil`/`Loca_rbl`) |
| path resolution | kind-7 per-language path array: `…\myoshiok\<lang>\bin_menu\loca_*.cl2` — 27/27 membership checks |
| consumer family | location-map rendering — the `Loca` pages; ~~field-level binder not isolated~~ the reader is `003C26C0` (RC-30) |
| magic check | none found — no `CLT2`/`0x32544C43` constant compare located (ORACLE's RC-30 record: `CLT2` is not tested) |

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `CLT2` magic | nothing found | — | — | no compare found |
| `+0x10` endOff (TIM2 total size) | not read on this path (`0024A9E0` steps by it only past picture 0) | — | — | inert here |
| `+0x14` dataSize (TIM2 CLUT size) | not read | — | — | inert |
| `+0x18` (TIM2 image size, 0) | `003C26C0` (`003C27B4`), added to the palette offset | — | — | — |
| `+0x1C` fieldLo (TIM2 header size, `0x30`) | `003C26C0` (`003C27B0`): palette = `+0x10 + 0x30 + 0` = file `+0x40` | — | — | — |
| `+0x1E` count (TIM2 colour count) | `003C26C0` (`003C27B7`), passed to `0024A480` | — | — | — |
| `+0x22` / `+0x23` variant (TIM2 ClutType / ImageType) | not read: the upload takes the image's own pair | — | — | inert |

*Answered 2026-09-30 (SWE2-CONTRACT, RC-30 round 3; SWE2-DATA `rc30-census-0930` `79e70e154`, reviewed ACCEPT by
SWE2-AUDIT-SEM `f29e44c6e`; ORACLE `rc30-cl2-request-bounds-0930` `be7c6fcd6`, independent):* the table above replaces
the earlier rows (`+0x10` / `+0x14` / `+0x22` "no reader found", `+0x1E` "palette binder (presumed)"). The request is the
location-map pane loader `003C1F00`: it reads byte `+1` of `menumap_common` entry `edi` and, when non-zero, requests
kind 7 id `0xE1 + byte` (`003C207A`–`003C208D`), keeping the buffer at world-map widget `+0x118`. Entries 40 (byte 1,
`0xE2` `Loca_gil`) and 46 (byte 2, `0xE3` `Loca_bhm`) are the only non-zero bytes in all nine copies; `Loca_rbl`
(`0xE4`) is never requested. The reader `003C26C0` takes `+0x118` (fallback `+0x110`), calls `0024A9E0(buf, 0)` for the
picture header at `+0x10`, and hands `0024A480` the palette and count as an external CLUT for a location-map image. The
upload `0024A1D0` → `00180E70` / `00181000` → `0017F3B0` builds each palette row as a texture of the format object
`02CF7480`, which `00163D00` constructs with the name `RGBA8` and `0x1C` in its four format slots (`0x1C` is the value
of `DXGI_FORMAT_R8G8B8A8_UNORM`: an inference from the constant, the Direct3D call itself is not traced). **Component
order: R, G, B, A**, byte 3 being the alpha that `0017F3B0` rescales (§2).

## 4. Key addresses

| Address | Role |
|---|---|
| `00404060` | location-map screen loader (requests `Loca.mrp` id `0xBF` at `00404107`) — the `.cl2` consumer family |
| `003C1D70` | dynamic kind-7 loader — `0xE8 + byte[+0xB]` index pattern seen near the location family |
| `003C1F00` | location-map pane loader — requests kind 7 id `0xE1 + byte [entry + 1]` at `003C208D` (RC-30) |
| `003C26C0` | the `.cl2` reader — TIM2 picture header via `0024A9E0`, palette to `0024A480` (RC-30) |
| `0017F3B0` | palette-row upload — texture format `02CF7480` (`RGBA8`), byte-3 alpha rescale ×255/128 |
| `002DF9A0` | path-array install — `.cl2` membership proven there; itself called from the CoreRuntimeScheduling boot path |

## 5. Corpus survey — 20 files

|| |
|---|---|
| `CLT2` | 20 of 20 |
| 512-colour (`count 0x200`, size 2112) | `loca_bhm`, `loca_gil` — 18 of 20 (9 locales each) |
| 32-colour (`count 0x20`, size 192) | `loca_rbl` — 2 of 20 (only `ch` and `in` ship it) |
| `variant 0x0503` | all bhm/gil | 
| `variant 0x0403` | all rbl |
| locale duplication | same-name files are byte-identical across locale dirs — 3 distinct contents total |

## 6. Falsification pass — 2026-09-14

| attack | result |
|---|---|
| Are the `+0x1C` u16s a single u32? | Read as two: `0x30` constant + count. The u32 `0x02000030` / `0x00200030` splits identically in all 20. |
| Is `dataSize` coincidence? | `+0x14 + 0x40 == fileSize` in 20 of 20 — not a coincidence, a size field. |
| Is `count` really entries? | `count × 4 == dataSize` in 20 of 20 (512×4=2048; 32×4=128). |
| Is `.cl2` dead baggage? | **No** — 27/27 path-array membership, interleaved with live `.tm2` entries in the same array. |

## 7. What this document does not claim

- ~~**The component order** (RGBA/BGRA) — not established.~~ R, G, B, A: the upload's texture format is `RGBA8` and byte 3 is rescaled as alpha (RC-30, §3).
- ~~**Which function reads the header fields** — no field-level reader isolated; the request is
  dynamic and its site is not pinned.~~ `003C26C0`, on the request `003C208D` (RC-30, §3).
- ~~**`fieldLo` (`+0x1C` = 48) semantics** — constant across all 20; could be a stride, a header
  version, or a sub-table offset that never fires.~~ The TIM2 header size, read (§2, §3).
- ~~**`endOff` (`+0x10`) semantics** — always `fileSize-16`; a parked end offset or a bound.~~ The TIM2 picture total size (`fileSize − 0x10`), not read on this path (§3).
- ~~**Whether `variant` selects a decode path** — correlates with size (0x0503↔512, 0x0403↔32) but
  no reader found.~~ It does not: `+0x22` / `+0x23` are never read (§3).
- **When the map screen shows entries 40 and 46 in play** — the entry index is the menu's selection; not claimed.
- **What the `+0x110` fallback buffer holds** — not claimed.

*Searched 2026-09-30 (SWE2-CONTRACT):* no page names a reader of the `loca_*.cl2` files. The only `CLT2` readers the
database traces are the `clutpack_ys` binder `00280AD0` (four palettes to `*(0209AC30)+0x390..+0x3A8`) and
`monotone_chr`'s loader, which grafts the `+0x390` palette ([loader-bound bin families](loader-bound-bin-families.md)
§`clutpack_ys`, §`monotone_chr`); neither loads a `loca_*` file. The "27/27 membership" (§3) is the kind-7 path-array
check of [the file-size tables page](../Loose-Files-And-Size-Tables/file-size-tables-fst.md) (`.cl2` 27/27).

- [x] **RC-29.** Which code walks the menu resource manifest (`.rdata` `008FCE00`–`008FD2D0`, fourteen `u32-2`-tagged
  kind-7 id lists) — the batch preload that carries the `.cl2` ids and the `.mrp` ids with no constant request
  ([the MRP sheet](mrp-menu-resource-packages.md) §3 shares this residue). No rip-relative or pointer-table reference
  reaches the block. Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-29:* **ANSWERED 2026-09-30 with the premise refuted (static; SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §3, commit `1261e2044`, `manifest_walker.py`): `008FCE00` is the developer console's page layout table, not a resource manifest** — 14 pages × 22 rows of u32 command ids (stride `0x58`, `0x4D0` bytes), read by the label filler `001D0390`, the page-header refresh `001D5260` and the row renderer `001CD0E0` (three rip-relative references and one image-base-relative read). The page's "no rip-relative … reference reaches the block" was a narrower sweep. Four of the unrequested `.mrp` files come through `.rdata` id lists of `003933F0` / `00393460`.
- [x] **RC-30.** Which function reads a loaded `loca_*.cl2` — its header (`+0x10` endOff, `+0x14` dataSize, `+0x1C`
  fieldLo, `+0x1E` count, `+0x22`/`+0x23` variant) and palette — and so the component order and whether the variant
  selects a decode path. Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-30:* **NARROWED 2026-09-30 (the same record §3, `cl2_requests.py`, `request_lists.py`):** no traced request route reaches ids `0xE2`–`0xE4`; six computed-id sites are bounded away from them, and three are not bounded (`002CEAE0`, `003C9950`, `00575C30`), nor are 18 path-API sites whose kind is computed. **Residue (static):** those sites' index ranges; until one reaches a `loca_*.cl2` id, the component order and the variant's role have no reader to ask.
  *Round 2 (records) RC-30:* **NARROWED again 2026-09-30 (SWE2-DATA's round-2 record `_index/candidates/rc-residue-0930/`, commit `39d08c02f` §2, `rc30_bounds.py`):** the three unbounded sites are bounded away from `0xE2`–`0xE4`: `002CEAE0` ids `0x17`–`0x29`, `003C9950` ids at most `0x1A`, `00575C30` ids at least `0x228`. The computed-kind path-API sweep finds 54 of 124 sites with a computed kind; the only ones not bounded read `(kind, id)` pairs from loaded structures (`003A13F0`, `003DDA70`, `003DF550`, `003E9EF0`, `003EADE0`, `003DC5B0` / `003DC8D0`). **Residue (static, data):** whether any shipped instance of those structures holds kind 7 with id `0xE2`–`0xE4`.
  *Round 3 (records) RC-30:* **ANSWERED 2026-09-30 (SWE2-CONTRACT, RC-30 round 3, `_index/candidates/swe2contract-rc-round3-0930/`):** SWE2-DATA's census (`rc30-census-0930`, `79e70e154`, AUDIT-SEM ACCEPT `f29e44c6e`) and ORACLE's independent bounds (`rc30-cl2-request-bounds-0930`, `be7c6fcd6`) find the route the rounds above missed: `003C1F00` requests kind 7 id `0xE1 + byte [menumap_common entry + 1]` at `003C208D`; `Loca_gil` and `Loca_bhm` are selected, `Loca_rbl` never. The reader is `003C26C0` (§3), the variant is not read, and the component order is R, G, B, A (the `RGBA8` upload `0017F3B0`, with byte 3 rescaled as a PS2 alpha, §2). The round-2 residue is superseded: every data-driven `(kind, id)` structure carries a constant non-7 kind.

*Superseded readings, 2026-09-30 (SWE2-CONTRACT, from SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §3, commit `1261e2044`): §3's "menu resource manifest" at `008FCE00`–`008FD2D0` and "no rip-relative reference and no pointer-table entry reaches the block" are refuted by RC-29 — the block is the developer console's page table, reached by three rip-relative references and one image-base-relative read. The `.cl2` ids have no traced request route (RC-30). §3 is kept as written.*

## 8. Related

- [`the-map-screens-and-their-shared-map-data.md`](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) — the location-map screen family.
- [`constant-resource-requests.tsv`](../VBF-Archive-And-Authored-Tables/members/constant-resource-requests.tsv) — `.cl2` is **absent** here by design (dynamic index).
- [`README.md`](README.md) — the `ps2data/image` long tail.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions or is named as the page reads it.*

**Presentation — SERVICE and CLIENT (18 edges).** The colour tables are read by render-side code. The row renderer `001CD0E0`, the label filler `001D0390` and the page-header refresh `001D5260` read the tables and call each other (`001D0390` and `001D5260` call `001CD0E0`, which calls `001DCD30`). The upload `0017F3B0` allocates, clears and builds the RGBA8 texture; it is called by `00180E70` and `00181000` and calls `0061E200`. The image member callback `0024A1D0` calls five `00180E70`..`00181520` image helpers. `003DDA70` and `003DC8D0` are the bounded `(kind, id)` readers the page names, and `003DD4C0` / `003DCD00` call them. Presentation owns the draw; the page owns the table format.

**Audio, PlatformOnlineAchievements, WorldAreaField — SERVICE (5 edges).** The 11 KB row renderer `001CD0E0` also calls `002DEBA0` (Audio), the game-state reader `003166F0`, `FieldData_GetVariable0` (`00265270`) and `WorldTransition_GetTransitionFieldId` (`00314910`). The `(kind, id)` reader `003EADE0` calls `002DF660` (Audio). These are reads a menu row makes, and none of them touches the colour tables.

**CoreRuntimeScheduling, World, SaveLoad — CLIENT (5 edges).** The boot pass `0022A0B0` calls the path-array install `002DF9A0`, which proves `.cl2` membership. `003C63A0` calls the label helper `0024A480`, which creates a label and calls `0024A1D0`. The world body `00266D10` calls the bounded reader `003A13F0`. `00582790` requests through `003933F0` / `00393460`. All are shared entry points.
