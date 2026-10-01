---
system: The `.mg` world-map mesh container — `worldmap/meshdata.mg`
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation; superseded readings are marked on the page) — no registered residue left: the walker (RC-32: a two-entry sub-mesh directory, three draw paths; §2's slot struct is 4 bytes out of phase), every byte placed (RC-33) and the mainN.psd binding traced (RC-34: w_main0..3.tm2) (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Menu.WorldMap
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 17 addresses cited - 4 data, 7 entry, 6 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "both shipped .mg files extracted from FFXII_TZA.vbf and hashed, 2026-09-14; section offsets + name directory verified on both"
archive_formats:
  - "mg | explained | World-map mesh container — header section offsets + 4-slot mainN.psd name directory + float vertex and u16 index bodies."
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The `.mg` world-map mesh container — `worldmap/meshdata.mg`

> **The world map's mesh + texture-source directory.** A header of section offsets, a four-slot
> `mainN.psd` name table, then float vertex data, u16 index tables and a u16 pair stream — the
> geometry the world-map screen draws and the names of the four `.psd` sources it textures from.

**Corpus validation, before anything else.**

|| |
|---|---|
| files examined | **2 of 2** shipped `.mg` entries — `in/worldmap/meshdata.mg`, `ch/worldmap/meshdata.mg` = **1 distinct content**; the format ships only in these two locale trees |
| size | 13,648 B (0x3550) both — `ch` copy hash-identical to `in` |
| first dword | `0x10` — not a magic, a version/stride field |
| name directory | `main0.psd`..`main3.psd` at `+0x30`, stride `0x20`, count 4 |

## 1. What the player sees

The world map (Select a Region → the Ivalice globe view) and the shared map-data surface the
license board touches. `meshdata.mg` is the geometry for that view; the four `mainN.psd` names
are its texture sources (the `w_main0..3.tm2` family it is drawn against).

## 2. The layout

```struct MgHeader base=file size=0x30
+0x00  u32   version     0x10 in both files
+0x04  u32   offIdxA     0x2C0 — offset to u16 index table A (16 B strip before the big section)
+0x08  u32   offSectionB 0x2D0 — offset to the big trailing section
+0x0C  u32   sizeSectionB 0x3280 — SIZE of that section: 0x2D0 + 0x3280 == 0x3550 == fileSize exactly (FABLE's arithmetic; the u16 pair stream sampled at file offset 0x3280 is interior content, not the target of this field)
+0x10  u32   offVerts    0x2A0 — offset to the 16-byte float block before index table A
+0x14  u32   f14         0x10
+0x18  u32   f18         0xA0 — reads as an offset into the region after the name table
+0x1C  u32   f1C         0x10
+0x20  u32   nameStride  0x20 — name-slot size
+0x24  u32   nameCount   4
+0x28  u32   _zero28     0
+0x2C  u32   _zero2C     0
```

```struct MgNameSlot base=+0x30 stride=0x20 count=nameCount
+0x00  char[16]  name     'mainN.psd' NUL-padded
+0x10  u8[4]     unk10    between the 16-byte name field and base; contents not established
+0x14  u32       base     0, 4, 8, 0x0C — a running base index into a sub-table, +4 per slot
+0x18  u32       count    4 in all four slots — each source owns 4 sub-entries
+0x1C  u16[4]    tail     0x7E,0x7E,0x7E,0x7F in all four slots — per-source constant
```

### The section bodies

| offset | content |
|---|---|
| `0xB0` | **sixteen `0x10`-byte homogeneous points** — 4 corners × 4 images (FABLE's read): `x ∈ {0,1,2}`, `y = 0`, `z ∈ {0,-1,-1.25}`, `w = 1`. Verified: `00 00 80 3F, 0, 00 00 80 3F, 00 00 80 3F` = (1.0, 0, 1.0, 1.0) opens the block |
| `0x1B0..0x2A0` | 240 B not yet decoded this pass |
| `0x2A0` | 16 B float block — `FF FF 7F 3F`(≈1.0), `0`, `FF FF 7F BF`(≈-1.0), `00 00 80 3F`(1.0) — a unit-range quad |
| `0x2B0` | u16 strip indices — `02 80 00 00 01 00 03 00 06 80 04 00 05 00 07 00` — the `0x8000` flag on alternate entries is the PS2 strip-restart convention |
| `0x2C0` (`offIdxA`) | u16 index table A — `0A 80 08 00 09 00 0B 00 0E 80 0C 00 0D 00 0F 00` — 16 B, ends exactly at `offSectionB` |
| `0x2D0` (`offSectionB`, `0x3280` B → EOF) | big section — opens `00 2B 00 00 BC 03 00 00 60 00 00 00 55 01 00 00 20 00 00 00 02 00 00 00` — a dword sub-header (`0x2B00`, `0x3BC`, `0x60`, `0x155`, `0x20`, `2`), then interior u16 content incl. the pair stream at file `0x3280` (`C1 00 FD 00`, `BF 00 FE 00`, `BD 00 FF 00`… — pairs counting down/up) |

## 3. The loader contract

|| |
|---|---|
| requesters | `00562F90` — world-map loader (calls at `00562FB6`..`00562FDA`, buffer stored at `+0x10`), and `00561390` — a widget installed by `00561300` on the license-board side (call at `0056162B`, buffer stored at `+0x110`, alongside `license_chip.bin` `0x7E` and `Lic_Bk`/`lic_8_c*.tm2`) — per FABLE's reader census |
| kind-7 id | `0xA8` — also listed in the manifest's worldmap set: the `2`-tagged list at `008FD0C0` carries `0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD` beside `w_*` ids |
| path resolution | kind-7 path slot `01E0E530[0xA8]` → `…\myoshiok\<lang>\worldmap\meshdata.mg` — 2/2 membership |
| companion requests | `00562F90` then names `w_shade_p` / `w_main0..3` / `w_icon_p` from table `00D231C0` as kind-7 ids `0xAA`.. (the `w_*.tm2` textures the four `mainN.psd` slots correspond to) plus `w_menu.mrp` `0xA6` |
| consumer family | world-map / license-board map data — the `menumap_world`/`menumap_location`/`menumap_common` widget at `02B457E0` ([map page](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md)) |
| magic check | none — `0x10` is a field, not a tag |

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x04..+0x10` offsets | mesh binder (presumed) | — | — | field-level reader not isolated *(superseded: the header is a two-entry `{offset, size}` sub-mesh directory read by `00274780`, RC-32)* |
| `+0x24` nameCount | — | — | — | no reader found *(superseded: file `+0x24` is sub-mesh 0's slot count, read by `005556A0` at `00555808`, RC-32)* |
| name slots | texture-source binder | — | — | the `mainN.psd` → `w_mainN.tm2` mapping is inferred, not traced *(since traced: `00563110` matches the slot names against `00D23270`; `mainN.psd` → `w_mainN`, RC-34)* |

*(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-02-b2-0930/REVIEW.md) correction 4: the three rows above carry their answers.)*

## 4. Key addresses

| Address | Role |
|---|---|
| `00562F90` | world-map loader — `0x7 0xA8` request at `00562FB6`..`00562FDA`, buffer stored at `+0x10` |
| `00561390` | license-board-side widget (installed by `00561300`) — `0x7 0xA8` request at `0056162B`, buffer stored at `+0x110`; interior read 2026-09-17, SWE2-FRONTIER: 1,091 B — `005C5230` first at [`005613D6`](../../_index/ADDRESS-INDEX.md), `002493D0` ×5 + `00249210` ×2 |
| `00D231C0` | the name table `00562F90` then resolves — `w_shade_p`, `w_main0..3`, `w_icon_p`, `w_menu` |
| `02B457E0` | map-data widget — loads the three `menumap_*` resources |

## 5. Corpus survey — 2 files

|| |
|---|---|
| identical `in`/`ch` | byte-for-byte the same — the `ch` copy is a duplicate |
| header offsets | all four section offsets and both counts identical |
| name directory | 4 slots, `main0..3.psd`, base 0/4/8/12, count 4 each |

## 6. Falsification pass — 2026-09-14

| attack | result |
|---|---|
| Is `+0x00` a magic? | **No** — `0x10` is a small version/stride value; the file has no tag. |
| Is `+0x0C` an offset or a size? | **Size** — `offSectionB + +0x0C == fileSize` exactly (0x2D0 + 0x3280 = 0x3550). The u16 pair stream at file `0x3280` is interior content; an earlier draft had this field as `offPairs` — wrong. |
| Are `mainN.psd` dead strings? | They sit in a `{base,count,tail}` slot structure — a live directory, not residual text. `+0x14`/`+0x18` are monotonic base+count pairs. |
| Are the float bytes really vertices? | `0x3F7FFFFF ≈ 1.0`, `0xBF7FFFFF ≈ -1.0`, `0x3F800000 = 1.0` — canonical unit-range floats, consistent with UV/vertex data. |
| Could the `0x8000` u16s be something else? | They alternate with small indices (`0x8002,0,1,3,0x8006,4,5,7`) — the strip-flag pattern is the natural reading, but the draw-path reader is not isolated. |
| Is the `0xB0` block a table of corners? | Verified — sixteen `0x10` vec4s, homogeneous `w=1`, matching FABLE's independent read of 4 corners per image × 4 images. |

## 7. What this document does not claim

- **The exact primitive encoding** — vertex/index/strip semantics are corpus-inferred; the
  renderer that walks them is not isolated.
- **What `+0x08`'s table B is** — its `0x2B00`-headed dwords read as a sub-header; undecoded.
- **The `mainN.psd` → shipped-texture binding** — the `.psd` names are authoring sources; which
  `.tm2`/`.nfs` they resolve to at runtime is not traced.
- **Why `+0x10` (offVerts) sorts before `+0x04` (offIdxA)** — the section order in the file is
  `verts 0x2A0 < idxA 0x2C0 < idxB 0x2D0 < pairs 0x3280`; the header order is a different
  arrangement.

*Searched 2026-09-30 (SWE2-CONTRACT):* [the map screens page](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md)
and [the menu screen atlas](../../16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md) name the two requesters (`00562F90`,
`00561390`) and nothing that reads the mesh bytes.

- [x] **RC-32.** Which code walks a loaded `meshdata.mg` — reads the header offsets, the name slots and the vertex /
  index / strip sections — and so the exact primitive encoding and why the header lists its offsets in a different
  order from the file. Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-32:* **ANSWERED 2026-09-30 (static; SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §6, commit `1261e2044`, `mg_reader_check.py` 125 checks): the file is a two-entry sub-mesh directory walked by three draw paths.** *(The slot struct in §2 is 4 bytes out of phase — see the note under §7.)*
- [x] **RC-33.** The undecoded bytes of `meshdata.mg`: the name slots' `unk10` word, the 240 bytes at
  `0x1B0`–`0x2A0`, and table B's `0x2B00`-headed body at `0x2D0`. Registered 2026-09-30 (SWE2-CONTRACT); static
  (bounded by RC-32's reader).
  *Applied 2026-09-30 (records) RC-33:* **ANSWERED 2026-09-30 (the same record §6): every byte is placed**; a few fields have no reader, and the record names them.
- [x] **RC-34.** Which shipped textures the four `mainN.psd` name slots resolve to at run time (`w_main0..3.tm2` is
  inferred from `00562F90`'s companion requests, not traced). Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-34:* **ANSWERED 2026-09-30 (the same record §6), traced:** `00563110` matches each slot name against `00D23270` (`main0..3.psd` → `w_main0..3`, `upper` → `w_shade_p`, `linetex` → `w_line01`) and binds the named-image entry `00562F90` created for kind 7 ids `0xAA + i`, so `mainN.psd` draws with `Tm2_Menu\w_mainN.tm2` (ids `0xAB`–`0xAE`).

*Superseded readings, 2026-09-30 (SWE2-CONTRACT, from SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §6, commit `1261e2044`): §2's `MgNameSlot` struct is 4 bytes out of phase, and its `unk10` / `base` / `count` / `tail` readings, the "240 B not yet decoded", table B and the "header order" question are replaced by the record's two-entry sub-mesh directory with every byte placed (RC-32, RC-33). The struct is kept as written, marked here.*

## 8. Related

- [`the-map-screens-and-their-shared-map-data.md`](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) — the world-map consumer family.
- [`constant-resource-requests.tsv`](../VBF-Archive-And-Authored-Tables/members/constant-resource-requests.tsv) — rows for `0x7 0xA8`.
- [`README.md`](README.md) — the `ps2data/image` long tail.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**SaveLoad — SERVICE.** `00582790`, owned by that layer, calls this page's `00249210` at **two**
sites — `005827FE` and `00582826`. **The save path consults this page; this page owns nothing in
SaveLoad.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions.*

**UI — SERVICE and CLIENT (15 edges).** The mesh's requesters are UI bodies. `00561300` installs the license-board widget `00561390` (it passes `00561390` to `00244F50`), and `00558FB0` / `00560910` call it. `00561390` calls the list helpers `00291D70` / `00291D80` and the widgets `00558F20`, `0055A810` and `0055C690`. The world-map loader `00562F90` is called by `00550540`, and `00563110` by `00552250`. `003C9950`, `00561390` and `00562F90` claim slots through `00249210`, and `00558FB0`, `00561390` and `00562F90` request through `002493D0`, which calls `00249210` and the label create `0024A4E0`. The UI owns the screens; the mesh is the data they load.
