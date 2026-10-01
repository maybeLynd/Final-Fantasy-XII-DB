---
system: The @FTE and @FCT entries of .cm files - per-model textures and colour palettes
category: 17-Presentation-Rendering
status: DOCUMENTED — the residue is answered (DD batch 10); what a co-drawn model that shares a texture key shows is runtime-only (owner re-status 2026-10-01, OPUS, on SWE2-CONTRACT's proposed line; documented_rule READY)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the entry binder 00504F00, the @FCT accessor 00504D30 and the combined draw builder
    0053B270-family disassembled from the authority image; the authored layouts then re-parsed
    out of all 1,066 .cm files in the archive (members/for_fdm_entry_census.py family +
    inline census), 2026-09-26
last_reviewed: 2026-09-29
archive_formats:
  - "cm"
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-fte-fct-falsification-pass-1
  note: written by SWE2-DATA as the UQ-218 @FTE/@FCT slice; corrected 2026-09-28
    on FABLE's uq218-cm-entry-residues record - record layouts, counts, the
    four-page palette payloads and the +0xBA page selection are code- and
    census-verified. ~~Not read - the FTE +0x1C cache-key semantics, the FCT +0x08
    id word's use, and how @FCT sub-indices are chosen.~~ All three read
    2026-09-30 (SWE2-CONTRACT, DD batch 10, swe2contract-ddres-b10-0930) - a key
    already live shares its cache slot and the last binder's descriptor stays
    (T4-T5), no pointer-forming body reads FCT +0x08 (T2), and the sub-indices
    come from command 0x16, whose shipped value 0xFFFF binds every sub (T8).
    Front matter brought current by DD batch 14.
---

# `@FTE` and `@FCT` — per-model textures and palettes (SWE2-DATA)

**Package:** `SWE2-DATA-UQ218-FTE-FCT` (UQ-218 residue). **Population:** both present
in `1,044/1,066` `.cm` files (the texture/colour-carrying subset; weapons and most
`gadget`/`treasure`/`bg_obj` files lack them). Same binder pattern as `@FDM`/`@FOR`:
`00504F00` stores the entry offsets at render-record `+0x218` (`@FTE`) and `+0x21C`
(`@FCT`); entry ptr = `rec+0x1F8` blob base + offset, `-1` = absent.

## `@FTE` — texture entry (SWE2-DATA)

```
+0x00  '@FTE', u32 kind = 0, u32 entryLen, u32 0
+0x10  char[0x20] name (file basename)
+0x30  u8 count + u8[] list — textures uploaded unconditionally, seeded into the
       builder's frame list before the @FOR table-B picks (0053B45A..0053B48A);
       values < record count in 1,044/1,044
+0x40  texture records, 0x20-byte stride, count of them
…      pixel payloads follow the whole record array in record order
       (dataOff chain contiguous 2,127/2,127, ending exactly at entryLen)
```

Record layout (0x20 bytes, record-relative — `rec = FTE + 0x40 + idx*0x20`,
reader `0053AB50` computes `((idx+2)<<5) + FTE`):

```
+0x00  u32  VRAM bytes reserved        (multiple of 0x2000 in 2,127/2,127;
                                          bottom-up allocator 00537AA0)
+0x04  u16  w    pixel width
+0x06  u16  h    pixel height
+0x08  u16  GS PSM format               (0x13 PSMT8 in 2,081, 0x14 PSMT4 in 46,
                                          nothing else; passed through to TEX0
                                          bits 20-25 at 0053BFD7 — no switch)
+0x0A  u16  RRW  upload-rectangle width (TRXREG)
+0x0C  u16  RRH  upload-rectangle height
+0x0E  u16  DPSM = 0                    (PSMCT32, 2,127/2,127)
+0x10  u32  0    (no read found in the three readers)
+0x14  u32  upload bytes  == RRW * RRH * 4 (2,127/2,127)
+0x18  u32  payload offset (entry-relative)
+0x1C  u32  texture-cache key           (256-slot cache 00521290/005210F0;
                                          form: prefix letter<<24 | set<<4 |
                                          record index)
```

Census over `1,044` files:

- `count` is `u32 @ +0x0C` (1:615, 2:170, 3:126, 4:57, 5:27, 6:13, up to 17).
- Pixel dimensions (`+0x04/+0x06`) — dominant sizes `256×256` (274),
  `128×128` (213), `128×64`, `128×256`, `256×128`, `512×256`, `8×8` (48 icon
  blocks), up to `512×512`.
- **Corrected 2026-09-28 (FABLE evidence record
  `_index/candidates/uq218-cm-entry-residues/`, controls.py 16 checks FAILS 0):**
  the earlier "record 0 only, pixelBytes then `u16 +0x4A` palette count" reading
  is replaced — `+0x4A` is the **upload width (RRW)**, not a palette count
  (`+0x14 == RRW*RRH*4` in every record; the upload is PSMCT32 regardless of the
  stored pixel format). The multi-texture cadence is resolved: `count` records
  then all payloads in order.

## `@FCT` — colour/palette entry (SWE2-DATA)

```
+0x00  '@FCT', u32 kind = 0, u32 entryLen, u32 0
+0x10  char[0x20] name
+0x0C  u32 count (1..8 typical)
+0x30  16-byte header records (rec = FCT + 0x30 + idx*0x10):
         +0x00 u16 vramBytes = 0x2000   VRAM reserved per CLUT, top-down
                                       allocator 00537AA0 (invariant, 1,951/1,951)
         +0x02 u16 clutBytes           colours = clutBytes>>2
         +0x04 u8  clutRRW             upload width / DBW source
         +0x05 u8  pageCount = 4       palette pages per payload (1,972/1,972)
         +0x06 u16 clutRRH             rrw*rrh*4 == clutBytes (1,972/1,972)
         +0x08 u32 id                  equals the same-index @FTE id in
                                       1,911/1,972; no read found in the
                                       three readers
         +0x0C u32 payloadOff          entry-relative
…      payloads: pageCount × clutBytes each — **four palette pages**, the
       page chosen at draw time by `s8[renderRecord+0xBA]` (below)
```

Census over `1,044` files / `1,951` header records:

- `u16 +0x02` values are `0x400` (1618), `0x200` (318), `0x40` (35) →
  **256, 128 or 16 RGBA colours** per palette — the PS2 CLUT sizes.
- **Corrected 2026-09-28 (FABLE evidence record
  `_index/candidates/uq218-cm-entry-residues/`):** the `+0x00` word is a VRAM
  reservation, not flags, and `+0x04..+0x0F` is `{RRW, pages, RRH, id,
  payloadOff}`, not an opaque parameter block.

### `@FCT` consumer — `00504D30(record, idx, sub, out)`

- Bounds: `idx < dword[entry+0x0C]`, `idx < 0x10`, `sub < 0x10`.
- `u16[entry + idx*16 + 0x32] >> 2` (the colour count) → `003CCB60` → resource
  id stored into `record+0x140 + idx*4` (the render record's 16-slot resource
  array; `-1` = unbound). `003CD7C0(1, id)` retains it.
- On first bind the pair `(idx<<4) | (sub&0xF)` is dedup'd into the 20-slot
  byte map at `record+0x180` (scan for a matching byte, else a `0xFF` free
  slot) and `dword[record + slot*4 + 0x194]` gets `003CCC20(out)`'s handle.
- Mirror: `00504C40`-family teardown walks `record+0x140` (16 slots) and
  `record+0x100` (0x20 u16 slots) releasing `003CD590`/`003CD5D0`/`00521250`.

So `@FCT` records are **palette descriptors**: VRAM reservation + CLUT byte
size + upload geometry; the runtime allocates a palette resource per index and
dedups `(idx,sub)` pairs in the record's `+0x180` byte map.

### `@FCT` page selection — `005044D0` / `renderRecord+0xBA` (SWE2-DATA)

Each payload holds **four palette pages** (`pageCount × clutBytes` bytes).
`005044D0` resolves the live page as `entry + payloadOff + s8[rec+0xBA] *
clutBytes` (`005044F8`..`0050450D`), and `+0xBA` is written only by the setter
`00504D20` (7 bytes; called from the status-look code at `00428D3C`, plus
`00428CD0` twice and `0042E520`) — the status-look page names `+0xBA` the
"record mode", with mode 3 = Stone. Corroborating data: **page 3 is grey in
1,914/1,970 palettes** (mean chroma 1.6 vs 30.6 on page 0 — the Stone palette),
pages 1/2 are brighter variants (luminance 98.7/98.3 vs 78.9; page 2
desaturated, chroma 21.4) — the status-look flashes. With mode 3, `0053BD30`
skips the palette-resource copy and uploads the page directly. Known shape
anomaly: 10 PSMT4 records with 0x400 CLUTs have a 0x100 stride to the next
record, so their 4-page windows overlap the following palettes (2 records'
windows run past the entry end; `fct_pages` measured 1,970 of 1,972).

## The combined draw bind (`0053B270`-family) (SWE2-DATA)

One ~0x1E00-byte builder **`0053AB50`** (called twice from `0053D780` — the
earlier "two inlined copies at `00532Cxx`/`005339xx` were frame-local qword
loads of `[rbp+0x218]` in `005325D0`/`00533250`, not builder copies; the frame
buffers `+0x83B0`/`+0x8430`/`+0x8530` occur only inside `0053AB50`) joins four
entries at once, resolving indices from **two** render
records — the source model `r14` and the LOD'd target `r13`:

- `r13`: `@FDM` (+0x20C), `@FTE` (+0x218), `@FCT` (+0x21C), `@FOR` (+0x208)
- `r14`: its own `@FOR` (+0x208), magic-checked, then **key-selected**: the
  0xE0 record whose `u8[rec+0]` equals `s8[r14+0xB8]` (the variant selector
  written by `00504F00` at `+0xB8`) is chosen (`0053B3F6`..`0053B40B`) — this
  is the consumer of the `@FOR` record keys.
- `@FOR` `u16@0x34` (table A) and `u16@0x36` (table B) resolve as
  entry-relative pointers (`0053B33A`..`0053B34D`): table A is a **u8-triplet
  table** (byte-indexed, `rec byte × 3` addressing at `0053B4C9`..`0053B4E2`),
  table B a **u8-pair table** indexed by ~~`(tableA byte + byte[FOR+0x32]·count)`~~
  **`(tableA byte + byte[FOR+0x32] · s8[r13+0xB9])`** (`0053B4B6`..`0053B4EC`). *(corrected 2026-09-29, OPUS falsification pass 1, `CON-182`: the multiplier is
  the target record's `+0xB9` byte, loaded at `0053AB9F`. `00504F00` sets it from its argument when that is at least 0
  and below `@FOR` byte `+0x33`, and to 0 otherwise (`005050CF`..`00505116`). The row width `byte[+0x32]` is read
  from `r14`'s `@FOR`, while tables A and B come from `r13`'s.)*
- `byte[FTE+0x30]` is itself a count field — `0053B45A` walks `byte[FTE+0x31..]
  ` per element, building a dedup list at the builder's `+0x83B0`.

That last point refines the `@FTE` header: `+0x30`..`+0x3F` is not padding but
`{u8 count@0x30, u8 bytes[]}` — a small index/flag list walked per texture
record.

## Residue

- ~~`@FTE` `+0x10` (unread) and the cache-key's per-file collision semantics
  (87 ids occur in more than one file, 80 with identical payloads).~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD
  batch 10): both are answered in the section below. `+0x10` is 0 in all 2,127 records, and no body that forms the
  entry pointer reads it. A shared key shares one cache slot, whose descriptor is the last binder's record.*
- ~~`@FCT` `+0x08` id word (unread by the three readers; equals the same-index
  `@FTE` id in 1,911/1,972) and the page-1/2 status-mode bindings (mode 3 =
  Stone is established; page 1's setter value is not tied).~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10):
  answered below. The three readers are the only bodies that form the `@FCT` pointer, and none of them reads `+0x08`.
  Mode 2 (page 2) is the HP Critical and Doom flash and two effect definitions. **Nothing selects page 1**: no status
  look passes 1, and no shipped `0xD0` effect authors it.*
- ~~The `w2/w4/w6` record source feeding the `@FDM` composite-key bridge and
  the `@FEF` (`144` files), `@FMC`/`@FMN`/`@FMW`/`@FRM` motion entries —
  UQ-218 stays PARTIAL.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10): each is on its own page now. The
  `w2/w4/w6` source is the authored command `0x14` ([`fdm-and-for-entries.md`](fdm-and-for-entries.md)), and the
  `@FEF` and motion entries are in [`fef-and-motion-entries.md`](fef-and-motion-entries.md). UQ-218 is ANSWERED.*
- *Added 2026-09-30 (SWE2-CONTRACT, DD batch 10): how `@FCT` sub-indices are chosen, which the front matter lists as
  not read, is answered below.*

## DD batch 10: cache keys, the unread words, page 1 and the sub-indices (SWE2-CONTRACT for OPUS)

*For the player:* a character's palette has four pages. Stone and Petrify use page 3. The HP Critical and Doom
flashes, and two effect definitions, use page 2. Page 1 ships in every palette but nothing in the game shows it.
Models that share a texture key share one slot in the texture cache.
The checks are in [`b10_checks.py`](../../_index/candidates/swe2contract-ddres-b10-0930/b10_checks.py) (T1–T8):
static, on the shipping image and all 1,066 `.cm` files of the extract (control X1 re-decodes `m1132.cm` from the
archive).

**Who forms the entry pointers (T1).** In the render-record code (`00500000`–`0053FFFF`), only three bodies read
the `@FTE` / `@FCT` offset (`+0x218` / `+0x21C`) next to the blob base `+0x1F8`: `005044D0`, `00504D30` and
`0053AB50`. The binder `00504F00` writes both offsets.

**`@FCT` `+0x08` has no reader (T2).**
- `00504D30` reads a record's `+0x02` (`00504DA7`).
- `005044D0` reads `+0x02` and `+0x0C` (`005044F8`, `00504508`).
- `0053AB50` reads `+0x00` through `FCT + (idx + 3) × 16` (`0053B62F`). At `0053BB59` it forms the record once more
  and reads `+0x00`, `+0x02`, `+0x04`, `+0x05` and `+0x06` until the register is reused (`0053BDF7`), without
  handing it to a callee.

None of these reads `+0x08`. The word's match with the `@FTE` id (1,911 / 1,972) is authoring, and the shipped
runtime does not read it.

**`@FTE` `+0x10` has no reader (T3).** It is 0 in all 2,127 records. `0053AB50` forms the record at
`FTE + (idx + 2) × 32` (`0053B6CB`), reads it only at `+0x00` and `+0x1C`, and hands it to `00504520` (`0053B71C`).
`00504520` copies every other field into the texture-cache slot: `+0x00`, `+0x04`–`+0x0E`, `+0x14`, `+0x18` and
`+0x1C`.

**A shared key shares a slot (T4–T5).** `005210F0` scans the 256 slots. When a live slot already holds the key, it
returns that slot and raises its count (`00521136`, `00521193`); otherwise it takes a free slot. `00504520` then
writes the binding model's record into the slot: its payload offset goes to slot `+0x10`, its VRAM size to `+0x08`,
and its dimensions and formats beside them. The builder skips the rebind while the model's own slot word already
names a slot holding this key (`0053B70E`). So two models with one key use one slot, and the slot describes whichever
of them bound it last.

In the files, 87 keys occur in more than one `.cm`:
- 80 have identical pixels, and 85 have an identical descriptor (every field but the payload offset).
- Only 15 have the same descriptor **and** the same payload offset.
- The seven with different pixels are variant sets of one character (`hc1024`, `hc1029`, `hc1030`, `hc1042` twice,
  `hc1044`) and the weapons `w0020` / `w2133`.

Runtime-only: whether two such models are ever drawn while both are bound, and what the second one then shows. That
depends on which models a scene loads and on the upload order.

**Page selection (T6–T7).**
- `00504D20`, the `+0xBA` setter named above, has three call sites. All three pass the second argument of `00428CD0`, the
  record-mode body.
- `00428CD0` has 23 call sites. The status looks pass the constants 0, 2 or 3 (see
  [how a status shows on a character](../Character-Render-Records/how-a-status-shows-on-a-character.md)).
- One more site, `00465CD0`, passes the `0xD0` effect instance's byte `+0x235`. That byte is copied from the
  definition's `+0x146` (`004650E5`–`004650ED`) and is used only when definition `+0x144` bit 2 is set. The copy
  goes to instance `+0x232` bit 10, which `00465F11` tests.

Over all 1,437 `0xD0` definitions (the published type census's count, and the control), the gate is clear with
value 0 in 1,407. When it is set, the value is 2 (24) or 3 (6). **No shipped path passes 1, so page 1 is authored
and never selected.** Page 2 is the HP Critical and Doom flash, and those effect definitions. Page 3 is Stone and
Petrify, and those effect definitions.

**Sub-index choice (T8).**
- `003E7210` is reached from `RenderRecords_ProcessDirtyState` (`00427FF7`) and from `0042B550` (a conditional tail
  jump, `0042B566`). It takes the palette index from record byte `+0x3D3` and the sub from word `+0x3F8`.
- A sub of `0xFFFF` walks every sub-entry of that index in the list at `[record + 0x400]` and binds each one through
  `00504D30` (`003E722F`–`003E7314`). Any other value binds that one sub (`003E73A9`).
- In the whole image, the only body that stores a word at `+0x3F8` or a byte at `+0x3D3` is command `0x16`'s handler
  `00520BD0`, on any base register. The census's control is the `+0xBA` setter `00504D20`, which it finds.

The [command-handler page](../Authored-Commands/the-authored-presentation-command-handlers.md) has that command's
census: all 373 shipped `0x16` commands carry `0xFFFF`. **So in shipped data every sub of the chosen index is
bound, and no single sub is ever chosen.**

| claim | evidence | tier |
|---|---|---|
| the pointer-forming bodies | T1 | 1 |
| `@FCT` `+0x08` unread; `@FTE` `+0x10` unread and 0 | T2–T3 | 1 |
| cache-slot sharing; the 87 / 80 / 85 / 15 split | T4–T5 | 1 |
| page 1 never selected; 2 and 3's sources | T6–T7 | 1 |
| sub-index choice | T8, the command census on its page | 1 |

## Evidence

- `00504D30` — `@FCT` slot binder, fully disassembled.
- `005044D0` / `00504D20` / `00428D3C` — `@FCT` page selector and its
  `+0xBA` writer (FABLE record, `005044F8`..`0050450D` re-read).
- `0053AB50` — the single combined `@FOR`/`@FTE`/`@FCT`/`@FDM` draw builder,
  key-selection and table-A/B addressing read (called twice from `0053D780`).
- `00504F00` — seven-tag index binder (`+0x208`..`+0x220`).
- `004201F0`, `00504840`, `005048A0`, `00521050` — see
  `fdm-and-for-entries.md`.
- `00537AA0` — VRAM allocator feeding both `@FTE` `+0x00` and `@FCT` `+0x00`.
- FABLE evidence record `_index/candidates/uq218-cm-entry-residues/` (commit
  `f4da22707`): `controls.py` 16 checks FAILS 0, re-run here; per-entry TSVs
  and disassembly extracts.
- Census: `members/for_fdm_entry_census.py` (entry headers) + inline FTE/FCT
  census quoted above, over `1,066` `.cm`, 2026-09-26.

## Falsification pass 1 — 2026-09-29 (OPUS): the bind, the pages, the builder and the cache survive; table B's row multiplier is not a count

**Attack.** The page's claims about the code were turned into checks at their instructions. Caller sets were
re-counted with a raw E8/E9 sweep. The builder's frame offsets were searched for image-wide. Script:
`Tools/analysis-kit/gfz-scripts/falsify_fte_fct.py`, output `falsify_fte_fct.out`, image `73461d08…`, 0 BROKEN, exit 0.
Carried, not re-run: the archive census and FABLE's controls.

| # | Clause attacked | Result |
|---|---|---|
| X5 | "table B … indexed by `(tableA byte + byte[FOR+0x32]·count)`" | **refuted** (`CON-182`). The multiplier is the target record's `s8 +0xB9`, loaded at `0053AB9F` |
| X6 | (supporting X5) | **measured**: `00504F00` sets `+0xB9` from its argument when `0 <= v < byte[@FOR + 0x33]`, and to 0 otherwise |
| X0 | sizes | **survives**: all nine |
| X1 | the `@FCT` consumer `00504D30` | **survives**: the bounds, the colour count into `003CCB60`, the `+0x140` slots, the 20-slot map at `+0x180`, the `+0x194` handles |
| X2 | the page selection | **survives**: entry + payloadOff + `s8 +0xBA` × clutBytes, through a 7-byte setter. Precision: the setter has three call sites (`00428D3C` and `00428D82` in `00428CD0`, and `0042E520`), and the page counts one of them twice |
| X3 | the builder | **survives**: called twice from `0053D780`; its frame offsets occur in no other body |
| X4 | the `+0xB8` key selection | **survives** |
| X7 | the seed list, de-duplication, record reader, PSM | **survives** |
| X8 | the cache and the teardown | **survives** |

Corrected in place: the table-A/B bullet. The consumer record is
`_index/candidates/fte-fct-falsification-pass-1-0929/`.

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **CoreRuntimeScheduling - SERVICE (1 edge).** `0053AB50` reaches bodies filed to CoreRuntimeScheduling: `001EDE70` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (10 edges).** CharacterRenderRecord_SelectLODForViewDepth (`004201F0`), `005048A0`, `00504C40`, `00504F00` (+2 more) reach bodies filed to Resource: ResourceTable_ResolveEntryByIndex (`002ED570`), ResourceEntry_FindSectionOffsetByTagAndName (`00409A30`), `00409CA0`, `00409F50` (+3 more) - shared machinery across the layer boundary, no shared ownership.
