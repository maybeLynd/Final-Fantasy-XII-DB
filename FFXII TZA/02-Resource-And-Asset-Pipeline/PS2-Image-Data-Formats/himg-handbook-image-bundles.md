---
system: The `himg` handbook image bundle — `handbook/menuhandbook_<family><NNN>.dat`
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 25 addresses cited - 1 data, 12 entry, 12 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all 2,721 shipped himg entries extracted from FFXII_TZA.vbf, 2026-09-16; every offset-table entry lands on TIM2 and every page closes to the next offset/EOF on the full population; native page binder read at 00575B80"
archive_formats:
  - "himg | explained | Handbook TIM2 page bundle — {u16 baseOrdinal, u16 count} + u32 offset table; pages are family-globally numbered so the handbook widget bounds-checks a page id against [base, base+count) before indexing."
last_reviewed: 2026-09-16
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# The `himg` handbook image bundle — `menuhandbook_<family><NNN>.dat`

> **A bundle of one to four TIM2 pages behind a `{base, count}` window.** `himg` is 90% of the
> `.dat` extension by logical unit (309 of 343) — the page images of the in-game **Handbook**
> (story, world, person, knowledge, tutorial, monster sections). Each file declares which slice of
> its family's global page numbering it carries; the widget bounds-checks the requested page
> against that window and indexes a `u32` offset table at `+0x0C` by `page − base`.

**Corpus validation, before anything else.**

|| |
|---|---|
| files examined | **2,721 of 2,721** shipped `himg` entries in `FFXII_TZA.vbf`, extracted and SHA-1'd — **309 distinct logical units** (one unit ≈ same filename across locales) |
| directories | `ps2data/image/ff12/myoshiok/<lang>/handbook/` — 294 units ship all 9 languages; a few are locale-subset |
| families | `menuhandbook_{story,world,person,knowledge,tutorial,monster}<NNN>.dat` — the numbered `.dat` files only; the unnumbered `<fam>.dat` are `hchk`, and low-numbered index files are `hdat` (§5) |
| magic + tag | 2,721 of 2,721 begin `68 69 6D 67` and carry dword `0x64` (100) at `+0x04` |
| structural failures | **0 of 2,721** — every table offset points at `TIM2`, every page closes to the next offset or EOF |

Decoder: `Tools/work/DATA/himg_decode/decode_himg.py` → `decode_himg.out.txt`.

## 1. What the player sees

The Handbook menu's illustrated pages — bestiary plates, lore illustrations, tutorial figures.
Each handbook entry refers to pages by a **family-global page number**; those pages are physically
shipped packed 1–4 per file, and the file header says which window of the numbering it covers.

## 2. The layout

```struct HimgHeader base=file
+0x00  char[4]  magic        'himg' - 68 69 6D 67, in 2,721 of 2,721
+0x04  u32      formatTag    always 100 (0x64); distinguishes himg from the hdat/hchk siblings (103)
+0x08  u16      baseOrdinal  family-global page number of page[0] — the window base
+0x0A  u16      count        TIM2 pages in this file: 1 (72 files), 2 (1,983), 3 (9), 4 (657)
+0x0C  u32      pageOff[count]  file-relative offset of each TIM2, strictly ascending
…     …         pad to the next 16-byte boundary (0 / 4 / 8 / 12 bytes, by count mod 4)
…     TIM2[count]             pages, contiguous; each page spans `0x10 + u32[TIM2+0x10]` bytes
```

- **Count-closed:** `pageOff` ends at `0x0C + 4·count`; the TIM2 area starts at the next
  16-byte boundary (measured pads: count 1 → 0, count 2 → 12, count 3 → 8, count 4 → 4).
- **Page-closed:** for page `i`, `pageOff[i+1] − pageOff[i] = 0x10 + totalSize` and the last page
  ends exactly at EOF — **6,693 of 6,693 pages** across the corpus satisfy this.
- `baseOrdinal`/`count` define the half-open window `[base, base+count)`; within a
  (locale, family) the shipped files' windows never overlap. `us` monster tiles `[0,384)`
  exactly (192 files); other families have gaps at page numbers the handbook never ships —
  the **same** gaps in all 9 locales, so they are authored holes, not corruption.

### 2.1 The TIM2 pages

Standard PS2 TIM2: 16-byte file header (`'TIM2'`, u16 version = `0x0004`, u16 pictureCount = 1),
then one 0x30-byte picture header at `+0x10` — `u32 totalSize` (everything after the file header),
`u32 clutSize` = 0x400, `u32 imageSize`, `u16 headerSize` = 0x30, `u8 imageType` = 5 (8bpp
palettized, 256-colour CLUT), `u16 width`, `u16 height`, GS register block. Image bytes
(`width × height`, 8bpp) at `+0x40`, 0x400-byte CLUT after it.

| dims (w×h) | pages | families |
|---|---|---|
| 512×896 | 3,480 | the large illustration pages |
| 512×224 | 2,754 | the common half-height pages |
| 512×448 | 450 | |
| 1024×448 | 9 | `tutorial001` in every locale — also the only files with TIM2 version `0x00D8` instead of `0x0004` |

`imageSize` values are exactly `width × height` (8bpp): `0x70000`, `0x1C000`, `0x38000`.

## 3. The native consumer — the handbook page widget

The consumer is a small (~0x100-byte) child widget in the Handbook menu, functions in the
`00575xxx` range. Its fields:

```
+0xC0  parent / request context       +0xC8  u8 state (1 = single-page bind, 2 = paged view)
+0xC9  u8 load phase (0 idle, 2 loading, 3 releasing)   <- corrected 2026-10-02, OPUS: 1 = loaded: 00575870+0x63 stores 1 when the load completes, and the readers require 1
+0xCA  u16 resource-index delta       +0xCC  u16 record field copy
+0xCE  u16 requested global page      +0xD0  u16 currently bound page (0xFFFF = none)
+0xD2  u8 page mode                   +0xF0  resource buffer (the raw himg file)   <- corrected 2026-10-02, OPUS: +0xD2 is the record's byte +0 (00575C30+0xA2), the family index into 0xD23740
+0xF8  TIM2 handle returned by the texture registry
```

### 3.1 Request — resource id = `familyBase[type] + fileIndex`

`00575C30` computes the kind-7 resource id. The record handed in is
`{u8 type @+0, u16 fileDelta @+2, u16 page @+4}`:

```
00575C60   edi = word[0xD23740 + type*2]     ; family base id
00575C64   edi += word[rbp+0xCA]            ; widget's file-index delta
           if byte[rbp+0xC8] == 1: edi += word[rec+2]
00575CAD   request(kind=7, id=edi)          ; via 00249210, committed by 00249410
           buffer -> widget +0xF0           ; byte[+0xD2]=type, word[+0xCC]=rec.f2, word[+0xCE]=rec.page
```

The `.rdata` family-base table at **`0xD23740`** holds six u16s, verified against the kind-7
path array (`0x01EC73A0`):

| type | base | registry path |
|---|---|---|
| 0 | 0x228 | `…\us\Handbook\menuhandbook_story.bin` |
| 1 | 0x294 | `…\us\Handbook\menuhandbook_world.bin` |
| 2 | 0x2CC | `…\us\Handbook\menuhandbook_person.bin` |
| 3 | 0x2F4 | `…\us\Handbook\menuhandbook_knowledge.bin` |
| 4 | 0x31C | `…\us\Handbook\menuhandbook_tutorial.bin` |
| 5 | 0x354 | `…\us\Handbook\menuhandbook_monster.bin` |

Within a family the ids run `.bin` = +0, `hchk` `.dat` = +1, numbered `.dat` = `+2 + NNN`
(verified: `knowledge000.dat` at `0x2F6`, `monster195.dat` at `0x419`). `+0xCA` is seeded `2`
for state-1 objects (`005759E2`) — the first numbered file — and for state-2 objects is set from
`word[hctg+0x14] + 2` (`005773D2`): **`hctg +0x14` is the family's `hdat` file count** (1 for
story/world/person/tutorial, 2 for knowledge, ~~4 for monster~~ 4, 5 or 11 for monster by locale *(corrected 2026-10-02, OPUS: the shipped monster catalogs hold `+0x14` = 4 in `de`, `it`, `kr`, `us`, 5 in `ch`, `cn`, `es`, `fr` and 11 in `in`, and each equals that locale's leading `hdat` file count)* — matching the shipped file names),
so the first `himg` delta is `2 + hdatCount` ([the sibling page](hchk-hctg-hdat-handbook-indexes.md)).

### 3.2 Bind — the two paths that read `+0x0C`

**State 1** (`00575710`, entered when `byte[+0xC8] == 1`): reads `dword[buf+0x0C]` — the first
offset-table entry — and registers `buf + off` as a TIM2 via `0039BEC0`. A `0xFFFFFFFF` value is
the none sentinel (`cmp ecx,-1; je`) — the same `+0x0C` slot is a single TIM2 pointer in the
`hdat` sibling (§5), which is what this path is shaped for.

**State 2** (`00575B80`, the page switcher): proves the window arithmetic:

```
00575B96   rax = [widget+0xF0]                       ; himg buffer
00575BAD   r8w = word[rax+0x08]                      ; baseOrdinal
           if (word[widget+0xCE] < r8w) return        ; page < base: not this file's window
00575BB8   ecx = word[rax+0x0A] + r8w                ; base + count
           if (word[widget+0xCE] >= ecx) return       ; page outside window
           if (dx == word[widget+0xD0]) return        ; already bound
00575BF7   local = word[widget+0xCE] - word[buf+0x08]
00575C00   ecx  = dword[buf + local*4 + 0x0C]        ; pageOff[local]
           tim2 = buf + ecx
00575C0D   register(tim2, "hb_tex")  -> widget+0xF8  ; 0024A440, name string @0xD23768
           word[widget+0xD0] = requested page
```

`hb_tex` ("handbook texture") is the registration name passed to the TIM2 registry.
Teardown `00575640` unregisters `+0xF8` via `0039BB60` and releases `+0xF0` via `003697F0`.
Requests are re-issued through the message handler `00575A50`, whose command record carries the
new global page in `word[rec+4]` → `+0xCE`.

`0024A440` and `00249410` are shared APIs, not handbook internals: `0024A440` is the generic
named-TIM2 registration entry (its other callers live in Input), and `00249410` is the generic
resource-request commit (its other callers live in Presentation). Those callers are fellow API
consumers, not `himg` readers; the same applies to the kind-7 request helper `00249210` and the
TIM2 unregister `0039BB60` / buffer release `003697F0` already named above.

## 4. The gap map is authored, not corrupt

Per-locale page windows (decoder §4 output):

| family | files (us) | window coverage |
|---|---|---|
| monster | 192 | `[0,384)` — exact tile, the positive control |
| story | 26 | gaps at 65–67, 77–79, 81–83, 93–95 |
| knowledge | 27 | gap at 45–51 |
| person | 26 | gap at 41 |
| world | 22 | gap at 46 |
| tutorial | 8 | gap at 1–3 |

Every gap repeats identically in all 9 locales — unshipped page numbers in the global numbering,
not missing files. Page-space sizes differ per family (story 96+, monster 384).

## 5. Siblings sharing the envelope

The same `{+0x04 tag, +0x08 u16, +0x0A u16, +0x0C pointer(s)}` envelope covers all three magics
below. The first is this page's own subject; the siblings are fully documented in
[the hctg/hchk/hdat page](hchk-hctg-hdat-handbook-indexes.md):

| magic | tag | files | role |
|---|---|---|---|
| `himg` | 100 | 2,721 | this page — TIM2 page bundles |
| `hdat` | 103 | 101 | numbered record headers: `u16 baseOrdinal` at `+0x08`, `u16 count` at `+0x0A`, `u32 tim2Off` at `+0x0C` (or `0xFFFFFFFF`), `u16 stringsOff` at `+0x10`, `u16 recOff[count]` at `+0x12`, then `12+4k`-byte records, an encoded-string blob, and at most one TIM2 |
| `hchk` | 103 | 54 | the six unnumbered `menuhandbook_<fam>.dat` unlock-predicate tables: `u16 entryCount` at `+0x08`, then count × **8-byte** records (five families) or **16-byte** `u16[8]` records (monster) at `+0x0C`; counts equal the `hctg` record count per family (story 69 … monster 384) |

The state-1 bind path's `buf + dword[+0x0C]` works for both `himg` (first offset-table entry) and
`hdat` (single TIM2 offset), which is why one widget serves both.

## 6. Evidence status and falsification

- **Established (native):** the bounds-check + index arithmetic at `00575B80` proves
  `+0x08 = baseOrdinal`, `+0x0A = count`, `+0x0C = u32 page-offset array`, and that payloads are
  registered as TIM2 under the name `hb_tex`. The family-base table `0xD23740` joins the kind-7
  path registry exactly.
- **Established (corpus):** 0 structural failures over 2,721 files; every offset lands on `TIM2`;
  every page span equals `0x10 + u32[+0x10]`; last page ends at EOF.
- **Measured:** TIM2 dims/type distribution, the `0x00D8` version anomaly confined to
  `tutorial001`, per-locale page-window gaps.
- **Unbound:** the two request-flag arguments (`r9d` 2-vs-3, stack flag 0-vs-1)
  passed to `00249210`; the record field `+2` added in state 1 (a file-index delta, but which *(answered: see [the index sheet](hchk-hctg-hdat-handbook-indexes.md) - `00575D10` fills it from the record's `+0x06` `hdatFile`; 2026-10-02, OPUS)*
  index table authors it is not yet traced).
- **Negative control:** no `himg` file's offset table entry falls outside the file or off a
  `TIM2` magic; `menuhandbook_order.bin`/`menuhandbook.bin` (ids `0xC9`/`0xC8`) are loaded by the
  parent widget (`00572D80`) and are not `himg`.

## Interior citation — frontier hub `00249410` (2026-09-17, SWE2-EC7)

`00249410` — 133 B, 27 frontier callers at census; the generic batch-commit this page already
names ("committed by `00249410`"). Interior verified: `or [rcx],2` marks the batch; if bit 1 was
**already** set and `word [+0x18] == word [+0x1A]` (count met at
[`00249430`](../../_index/ADDRESS-INDEX.md)) it dispatches — `dword [+4] != 0` calls
`[rcx+0x10]` directly, else it vcalls `*[rcx+8]` with a `{0x10,0,0,0}` arg block. The exit clears
bit 0 (`and [rbx],~1`). So "commit" is conditional on the batch's own count words, matching the
spawn page's "sets bit1, compares two words, dispatches when equal".

NOT claimed: what the two completion callbacks (`+0x10` direct vs `[+8]` virtual) deliver.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions.*

**UI — CLIENT (14 edges).** `00249210` claims a slot in the shared loader pool and starts a request. `00249410` closes a request batch (the `00249580` record): it marks the batch issued (bit 1) and, if every request has already finished (`+0x18` == `+0x1A`), fires it — the callback at `+0x10` when `+4` is set, otherwise message 16 (resource batch complete, DL-1) to the owner at `+8`; otherwise the last request's completion `002495C0` fires it. The menu screens load through the same pool: `003C9950`, `00561390` and `00562F90` claim slots through `00249210`, and eleven UI bodies (`00253780` to `00561390`) close their batches through `00249410`. The pool is shared; the handbook bundles are one of its clients.

**Presentation — CLIENT (2 edges).** The input-consumer state machines `002B7B80` and `002BAF80` close request batches through `00249410`, the same close step.

**SaveLoad — CLIENT (2 edges).** `00582790` claims a slot through `00249210` and closes the batch through `00249410`. The load menu reuses the pool.

**Input — CLIENT (1 edge).** `00291D90` calls `0024A440`, which creates a text label through `0024A4E0` and calls the image member callback `0024A1D0`. It is the helper the bundle's `hb_tex` registration uses.
