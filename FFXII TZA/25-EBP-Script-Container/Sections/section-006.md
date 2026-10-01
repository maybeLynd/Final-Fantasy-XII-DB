---
system: EBP section_006 — the TIM2 texture block
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: PrimaryOwner:Presentation-Rendering
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "1115 / 1115 us .ebp scripts, 2026-09-03 (1114 containers; section_006 in 67)"
last_reviewed: 2026-09-03
ebp_units:
  - "section_006"
audit:
  passes: 2
  last_pass: 2026-09-04
  last_pass_state: GN160-repos-c9-falsification-2-after-reopen
  crossref_clean: true
  crossref_checked: null
  crossref_report: null
  reopened_count: 1
---

# EBP `section_006` — the `TIM2` texture block

> The rarest section in the container, and the only one that is a **published third-party format**:
> a Sony PlayStation 2 `TIM2` image, embedded whole. 55 of the 67 are the same tiny 24×23 4-bit
> indexed picture.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` scripts (1,114 containers) |
| this unit present in | **67 (6.0 %)** — the rarest of the 13 section types |
| co-occurrence | always with `000` and `002` (67/67 each); `012` 57, `016` 54, `003` 30, `004` 14, `008`/`009` 14 each, `010`/`011` 3 each, `019` 3, **`014` 1** |
| size range | **448 B – 22,400 B, median 448 B**, 11 distinct sizes; 57 of 67 are exactly 448 B |

`section_006` implies `section_002` (the text section) in all 67 files, and the reverse does not
hold — `002` occurs 828 times. One more one-way implication in a container full of them.

---

## 1. What the player sees

**A small picture drawn over the field** — at 24×23 pixels, sixteen colours, this is the size of an
on-screen glyph or marker, not of a scene. The three larger entries (640×23, 640×46, 616×16) are
wide strips, the shape a text banner or a bar takes rather than a sprite.

The honest answer for most of the 67: **nothing directly, on its own.** It is an image the script's
own presentation draws; which draw call consumes it is not established here (section 3).

## 2. The layout

**This is Sony's `TIM2` (`.tm2`) container, unmodified**, and the field names below are that format's
own. Offsets from the start of the section body.

```
+0x00  char[4]  magic          'TIM2'                     -- 67/67
+0x04  u8       version        4                          -- 66/67 (one file: 0xD8)
+0x05  u8       format         0                          -- 67/67  => picture headers start at 0x10
+0x06  u16      pictureCount   1 (57 files) or 2 (10)
+0x08  u8[8]    0                                         -- 67/67
+0x10  the first picture header
```

Picture header, at `+0x10` because `format == 0`:

```
+0x00  u32  totalSize
+0x04  u32  clutSize        0    -- 67/67
+0x08  u32  imageSize
+0x0C  u16  headerSize      0x60 in the single-picture files
+0x0E  u16  clutColors      0    -- 67/67
+0x10  u8   pictFormat      0    -- 67/67
+0x11  u8   mipMapCount     1    -- 67/67
+0x12  u8   clutType        3    -- 67/67
+0x13  u8   imageType       4    -- 67/67  (4 = 4-bit indexed)
+0x14  u16  imageWidth
+0x16  u16  imageHeight
+0x18  u64  GsTex0
+0x20  u64  GsTex1
+0x28  u32  GsRegs
+0x2C  u32  GsTexClut
+0x30  extended header, headerSize - 0x30 bytes
```

Pixel data begins at `0x10 + headerSize`, which is `0x70` in the 57 single-picture 448 B files, and
that is exactly where 4-bit index data is observed to start.

**`imageType == 4` (4-bit indexed) with `clutSize == 0` and `clutColors == 0` in all 67 files.** A
4-bit indexed image carries sixteen palette entries and these files carry none, so **the palette is
not in this section.** That is an invariant, and an unusual one: it means `section_006` is not
self-sufficient as an image and something else supplies its colours.

### The dimensions, all 67

| width × height | files |
|---:|---:|
| **24 × 23** | **55** |
| 640 × 23 | 3 |
| 40 × 23 | 1 |
| 80 × 21 | 1 |
| 576 × 21 | 1 |
| 616 × 16 | 1 |
| 200 × 16 | 1 |
| 640 × 46 | 1 |

Height is 16, 21, 23 or 46 and never anything else — four values over 67 files. Width varies far
more. That is the profile of a **row of glyphs or a banner strip**, not of arbitrary artwork.

## 3. The loader contract

**Complete as of 2026-09-04. The connection to `section_006` is made and it runs through the
container directory, not through a filename.**

```
ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources   003304A0
  0033054F  CMP dword ptr [RDI+4],6      ; slotCount > 6
  00330555  MOV EAX,[RDI+0x28]           ; slot 6's offset; 0 -> absent
  0033055B  ADD RAX,RDI ; OR EAX,EBX     ; base + offset, manager index in the low nibble
  00330565  CALL FUN_00330060
        |
        v
FUN_00330060  (170 bytes)
  00330088  AND RBX,0xFFFFFFF0                       ; the section pointer
  0033008D  AND EAX,0xF                              ; the manager index
  00330097  MOV [r15 + rax*8 + 0x21A6CF0],RBX        ; 022C6CF0[mgr] = section
  0033009F  CALL FUN_0026C860(mgr, section)          ; the binder
  003300AF  AND RSI,~0x40                            ; clear pending bit 6
  003300DB  CALL 0032F1B0                          ; finalize, only when the mask drained
  003300E5  CALL FUN_0017F790(packed, section)
  00330105  JMP FUN_0029CAC0(section)                ; tail call -- the texture cache
        |
        v
FUN_0029CAC0  (72 bytes) -- a 6-entry x 16-byte refcounted cache at 0209C320
  0029CAD0  loop 1: if an entry's pointer == this one, INC [entry+8] and RET   (already registered)
  0029CAE2  loop 2: find the first entry whose pointer is 0
  0029CAF4  MOV [rax],RCX ; MOV dword ptr [rax+8],1  ; claim the slot, refcount = 1
  0029CAFE  JMP FUN_0039BEC0                         ; register the texture
        |
        v
FUN_0039BEC0  -- validate and register (below)
```

**So the `TIM2` block is validated, and the path is: directory slot 6 → per-manager store → binder →
a six-entry refcounted cache → the eight-slot texture registry.** If the cache is full,
`0029CAF3 RET` drops the registration silently — a third way to get `0` behaviour that the
registrar's own return value cannot distinguish.

`FUN_0039bec0`, signature `(void *block) -> unsigned slot`:

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `block` pointer | `0039BEC9` `TEST RCX,RCX` | null → returns `0` | — | — |
| `+0x00` magic | `0039BEDC` `LEA RDX,[00D11470]` then `strncmp(block, "TIM2", 4)` | mismatch → returns `0` | — | — |
| `+0x40` | `0039BEED` `MOV EAX,[RDI+0x40]`, `0039BEF2` `CMP AL,0x1` after `& 0xF` | low nibble ≠ 1 → returns `0` | — | — |
| `+0x04` `version` | — | — | — | **not read by this function** — `0xD8` and `4` both pass |
| `+0x06` `pictureCount` | — | — | — | **not read by this function** |
| everything else | — | — | — | **not read by this function** |

On success it takes the **first free slot of the 8-entry pointer table at `02AEE810`, scanning
indices 1 through 7 only** (`uVar2 = 1; … while (uVar2 < 8)`), stores the pointer, calls
`FUN_0039bf50()` and returns the index. **Slot 0 is never used**, and when all seven are occupied it
returns `0` — the same value it returns on validation failure, so a caller cannot distinguish "bad
data" from "table full" from the return alone.

**The magic is compared with `strncmp` against an `.rdata` constant**, not with an immediate. This
is why the `TIM2` search behaves differently from `LGT2`: `LGT2` appears once in `.text` as a
compare immediate, `TIM2` appears once in `.rdata` at `00D11470` and zero times in `.text`. Both
magics *are* validated; only the encoding differs. **A `.text`-only constant scan finds one and
misses the other**, which is worth knowing before concluding a magic is unchecked.

### The gate at `+0x40`, measured

`+0x40` is `0x10 + 0x30` — the first dword of the picture header's **extended** region, immediately
after the standard 0x30-byte picture header. The check is `(*(u32 *)(block + 0x40) & 0xF) == 1`.

**All 67 shipped `section_006` blocks pass it.** That is a real corroboration of the link between
this function and this section — the gate is narrow (one nibble value out of sixteen) and the
corpus satisfies it universally. It is corroboration and not proof; see below.

### How the link was missed, and what closed it

The 2026-09-03 version of this sheet left the link open on this reasoning: `FUN_0039bec0`'s four call
sites — `0037F2B9`, `003BC7C3`, `0057576C` and the tail `JMP` at `0029CAFE` — are **none of
them in the `atelload.c` translation unit** (`0032F520`–`00331E9F`), which is where every other
section in this lane is registered, so the `.ebp` connection could not be asserted.

**That reasoning was sound and its premise was wrong.** `atelload.c` is where the *legacy filename*
registrations live; the container's directory walk at `003304A0` is a different function in a
different unit, and it is the live route. The fourth call site, `0029CAFE`, **is** on the `.ebp`
path — three tail calls downstream of slot 6. A search that asks *"is the caller in `atelload.c`?"*
cannot find it, because the answer is legitimately no.

`FUN_0039bec0` is still also the generic registrar for the **447 standalone `.tm2` files** that ship;
the other three call sites are presumably those. The two facts were never in conflict — the sheet
treated "generic registrar" and "`section_006`'s reader" as alternatives when they are the same
function serving both.

**The write path.** None found. Nothing observed writes a `TIM2` block.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0039BEC0` | `FUN_0039bec0` — the `TIM2` validate-and-register function | ✅ full body |
| `0039BEC9` | `TEST RCX,RCX` — the null guard | ✅ |
| `0039BEDC` | `LEA RDX,[00D11470]` — the `"TIM2"` compare operand | ✅ |
| `0039BEED` | `MOV EAX,[RDI+0x40]` — the extended-header gate | ✅ |
| `0039BEF2` | `CMP AL,0x1` | ✅ |
| `0039BEFB` | `LEA RDX,[02AEE810]` — the 8-slot registry | ✅ |
| `00D11470` | `.rdata` `"TIM2"`, the only occurrence in the image | ✅ |
| `02AEE810` | the 8-entry pointer table, slots 1–7 usable | ✅ at the 10 sites that reference it |
| `0039BF50` | the post-registration refresh | ❌ not read |
| `0037F1F0`, `003BC4E0`, `00575710`, `0029CAC0` | the four callers | ❌ not read |

## 5. Corpus survey

> **Cross-tree census 2026-09-12 (FABLE) — the pictures are pre-rendered text strips, and the
> localisations say so.** The 67 files are the `us` tree's; across the nine trees of
> `FFXII_TZA.vbf` the section is present in **67 (`us`, `fr`, `it`), 68 (`de`, `es`), 556 (`kr`),
> 584 (`cn`), 603 (`ch`) and 633 (`in`)** containers, every one `TIM2`, every one `imageType 4`.
> In every Latin-script tree the population is the same: 55–57 files carry one **24 × 23** picture
> (448 B), three carry a two-picture **640 × 23**, one a 64 × 23, one an 8 × 22, one a 40 × 14 and
> one two-picture 640 × 46 (`evt_t0505`, 22,400 B). In `kr`, `cn`, `ch` and `in` the same 23-pixel
> height dominates but the **width varies per file in multiples of 8 from 24 to 640** (`kr`: 64 × 23
> ×73, 24 × 23 ×64, 40 × 23 ×52, two-picture 640 × 23 ×85, 640 × 46 ×48, and widths 80, 104, 120,
> 144, 160, 184, 200, 224, 240, 264, 280, 288, 304, 320, 344, 360, 400, 424, 440, 464, 480, 504,
> 520, 528, 544, 560, 584, 600, 624, 640 once or twice each; `in` leads with 80 × 23 ×76 and
> 144 × 23 ×42). A paletteless 4-bit strip of fixed 23-pixel height whose width tracks the script
> and whose count multiplies eightfold exactly in the trees that cannot draw their text from the
> Latin font is **a line of text rendered to a texture** — place or event captions the CJK and
> `in` (International, presumably Japanese) builds ship as pictures. The 24 × 23 picture the Latin
> trees carry in 55 files each is one glyph cell wide. What the strips *say* needs the pixel
> data decoded against the palette-carrier BZ-1 chases; the `us` invariants below hold for the
> `us` tree only (the section's content differs per tree — the container page §5).

> **Correction/refinement 2026-09-24 (SWE2-DATA) — the `in` strips are per-event expansion-glyph
> sheets, not captions.** With `decode_msb.py` the `in` message banks decode through
> `fontex_subtitle.fex`/`fontex_expand.fex` per-event codepoint tables (keyed by the
> `00674A00`-family path hash of `event\<dir>\<name>` — see `16-UI/Text-And-Number-Rendering/
> font-data-kerning-and-expansion.md`), and the slot-6 TIM2 is the **bitmap half of that system**:
> measured over the 61 `in` event files that carry a `.fex` chunk, TIM2 pixel capacity at ~10 px
> per glyph cell meets or exceeds the chunk's record count in every case (`alc_a0100`: 66 chunk
> codepoints ↔ 640×23 + 24×23 = ~66 cells; `byu_b0101`: 30 ↔ 304×23 = ~30; `bhm_d0101`: 257 ↔
> 640×115 = 320), while the same files at a 20 px cell assumption fall *short* of the count for
> `dor_a0100` (64 < 65) and `alc_z0104` (128 < 193). Events bound to `fontex_expand` instead fit a
> ~20 px cell exactly (`alc_a0280` 14 ↔ 280 px, `enw_a0580` 6 ↔ 120 px). The strips therefore hold
> **one bitmap per `.fex` entry** — the event's `18`-plane glyph atlas — not one readable line of
> caption text.
>
> **Order and pitch confirmed 2026-09-25 (SWE2-DATA).** The glyph bitmaps are packed at roughly
> **10 px each in `.fex` record order**, not on a 20 px grid — what reads as one inked 20 px cell
> is two adjacent ~10 px glyphs. `alc_a0100` (66 records, 640×23 + 24×23 = 664 px ≈ 66 glyphs)
> head cells render slot 0 = `元`, slot 3 = `一`, and the 24 px tail picture carries the last two
> records `事`,`実` in order; `byu_b0101` is exact at 30 records ↔ 304 px; `bhm_d0101` carries
> 257 records in 640×115 (~320 slots, slack-filled — pic width rounds up). `fontex_expand` sheets
> keep the wider ~20 px pitch (`alc_a0280` 14 ↔ 280 px, `enw_a0580` 6 ↔ 120 px) — the dialog font
> is wider than the subtitle font. Per-glyph advance metrics are not inside the TIM2 (the
> registrar reads nothing past `+0x40`); the renderer's width source — a fixed ~10 px subtitle
> pitch or a companion table — is still open.
>
> The earlier "a line of text rendered to a texture" reading is superseded for the
> `in`/`ch`/`cn`/`kr` populations (it remains possible that Latin-tree strips are captions). The
> external-palette invariant (§2) now has its explanation: the text renderer supplies colours, as
> it does for every other glyph source.

**Invariants over all 67 files:**

| | |
|---|---|
| `+0x00` magic `TIM2` | 67 / 67 |
| `+0x05` `format == 0` | 67 / 67 |
| `+0x08`–`+0x0F` all zero | 67 / 67 |
| picture `clutSize == 0` and `clutColors == 0` | 67 / 67 |
| `pictFormat == 0`, `mipMapCount == 1`, `clutType == 3`, `imageType == 4` | 67 / 67 |
| `(*(u32 *)(section + 0x40) & 0xF) == 1` — the loader's gate | **67 / 67** |
| section length a multiple of 16 | 67 / 67 |

**Outliers, each on its own line:**

- **One file has `version == 0xD8` (216)** where the other 66 have `4`. `FUN_0039bec0` does not read
  the version byte, so if that is the consumer, the anomaly is invisible to the engine. If some other
  consumer *does* read it, this file is a live edge case. Either way it is one file in 67 carrying a
  value nothing else in the corpus carries, and it should be looked at before anyone writes a
  `section_006` tool.
- **10 files carry `pictureCount == 2`**, with `headerSize` 304, 512, 560 or 640 rather than 96.
  Multi-picture `TIM2` is part of the format; this sheet does not walk the second picture header.
- **The 22,400 B outlier** is 26 times the median. With 57 of 67 at exactly 448 B, `section_006` is
  a near-constant-size section with a handful of exceptions.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is this really `TIM2`, or a game format that reuses the fourcc? | It parses as `TIM2` **as a format, not as a guess**: `format == 0` predicts picture headers at `0x10`, `headerSize == 0x60` predicts pixel data at `0x70`, and 4-bit index data is observed to begin exactly there. Three independent predictions from the published layout, all confirmed, in 57 files. |
| Does `imageSize` agree with `width × height` at 4 bpp? | For the 24×23 case: 12 bytes per row × 23 rows = 276, against `imageSize` 288 — consistent with row padding, not with a different bit depth. A 8-bit reading would need 552 and an 16-bit one 1,104; neither fits. |
| Is `clutColors == 0` real, or did I read the wrong offset? | Read at picture-header `+0x0E` = section `+0x1E`, and `headerSize` at `+0x0C` = `+0x1C` gives `0x60`, which correctly predicts the pixel-data offset. If the offsets were wrong, that prediction would have failed. |
| Is the `+0x40` gate evidence that `FUN_0039bec0` reads this section? | **Corroboration, not proof.** 67/67 pass a 1-in-16 nibble test, which is strong, but every shipped `.tm2` in the game may pass it equally — and 447 of those ship. The test that would settle it is whether any `.ebp`-side code path reaches `0039BEC0`, and **none of its four callers is in the `atelload.c` unit**. Left open rather than asserted. |
| Was the external specification consulted before or after the reading? | **The bytes were read first.** The magic and the field layout were recovered from the corpus census — an 8-byte header, a picture header at `0x10`, pixel data at `0x70` — and the published `TIM2` layout was matched to that afterwards. It is used as an oracle for field *names*. Nothing in section 3 rests on it: every entry there is an instruction address. |
| Could the `.rdata` `"TIM2"` be a string constant rather than a compare operand? | It is passed as `RDX` to a call preceded by `MOV R8D,0x4`, and the result is tested and branched on — the shape of `strncmp(a, b, 4)`, not of a printed string. It sits in a run of float constants with no surrounding string table, which also argues against it being message text. |

**What I tried that failed to break it.** I tried to connect `FUN_0039bec0` to the `.ebp` path by
looking for any of its callers inside `atelload.c`'s address range. All four are outside it. The
attempt failed to confirm the link, and reporting the failure is the point — the alternative was to
let a 67/67 gate match stand in for a call chain.

## 7. What this document does not claim

- **The consumer of `section_006` is identified (2026-09-28, SWE2-CONTRACT).** The section lands at
  the actor-manager slot's `+0xB0` (binder `0026C860`) and is consumed as a *resource reference*, not
  decoded by the slot code itself: the `meswin`-family verb tail reads `[slot+0xB0]` as `r9` into the
  window opener `002E16B0` (`00348EF8`, siblings `0034AE91`/`0050EB57`), where it becomes the
  `window+0x1A8` resref lazily resolved by `0039C480`; and `002C8BC0` reads it as `r8` into the
  kind-2 text-element constructor `002B3400` (`002C8D26`), which classifies it via `0039BAD0` into
  `element+0xA6` and — when the kind byte is 7 — binds a texture handle at `element+0x60` through
  `0039C4A0`. Whether the registered form (`0039BEC0`) is what `0039BAD0`/`0039C4A0` resolve remains
  the open edge — the `.ebp`-side delivery chain is proven, the register-side link is not.
- **`Inert` in section 3 is scoped to one function.** The version byte and `pictureCount` are marked
  *not read by `FUN_0039bec0`*, which is the only function read. They are **not** claimed inert in
  the engine.
- **The palette source is unknown.** All 67 blocks are 4-bit indexed with zero CLUT entries, so
  sixteen colours come from somewhere else, and this sheet does not say where.
- **The second picture header is not walked** in the 10 multi-picture files.
- **The pixel data is not decoded** beyond confirming its offset and bit depth. No image is rendered
  here and none of the 67 is identified as a particular in-game graphic.
- **`section_006` is not compared with the 447 shipped `.tm2` files.** They share a format; whether
  any is the same image is untested.

## 8. Related

- [`25 — the EBP script container`](../README.md) — the directory that supplies this section's offset
- `Sections/section-004.md`, `Sections/section-014.md`, `Sections/section-019.md` — the other three
  sections in this lane
- [`17 — Presentation / Rendering`](../../17-Presentation-Rendering/README.md) — where the eventual
  consumer of a registered `TIM2` belongs
- [`02 — Resource & Asset Pipeline`](../../02-Resource-And-Asset-Pipeline/README.md) — `tm2` is one
  of the 48 censused shipped extensions, 447 entries; this sheet does **not** claim that unit

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Actor — SERVICE.** `0032F1B0` on this page calls `FUN_0037aa90`, owned by that layer. What it reaches is a 491-byte reader bounded at **five** slots of `0x50` bytes from `02EBF420`, which refuses anything whose first dword is not the magic `0x3254474C` - `"LGT2"` in file order; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**SaveLoad / Save_Load_Settings — CLIENT (5 edges).** `00582790` calls `00249210`, `00249410` and
`00249580` — the section-006 helpers (`003BC3D1` context); `00280140` and `0057E4D0` call `00245020`,
the arm this page names beside `003BD8F0`. The save layer consults the same script-container helpers
when serialising its state; fan-in, not shared ownership. Read from `edges.tsv` 2026-09-17
(SWE2-FRONTIER).

- **Input — CLIENT (SWE2-EC7-164, 1 edge).** The free leaf `0024A680` this page's `003C2210` cites is also called by input-filed `00291D90` — the allocator is shared.
- **UI — CLIENT (62 edges, one fan-in).** `00245020` and the section's other helpers are called across the UI layer (`00253780`, `002778C0`, `00279E20`…) — the same fan the save row above already describes.
- **World — CLIENT (1 edge).** `0024A680` is also called by world-filed `003C63A0` — the same shared free.
- **Presentation — CLIENT and SERVICE (8 edges).** 7 inbound (Presentation bodies `002B7B80`, `002BAF80`, `0035C160` call page-cited `00249410`, `00249580`, `0039C4A0`); 1 outbound (page-cited `0017F790` call Presentation bodies `001B47A0`). Substantive edges include `0017F790` calls `001B47A0`; `002B3400` is called by `0035C160`; `0039C4A0` is called by `002B0280`; `0039C4A0` is called by `002AAE40`; the remaining edges run through shared helpers the page cites.
- **Resource — CLIENT and SERVICE (16 edges).** 11 inbound (Resource bodies `002493D0`, `00249350`, `00249380` call page-cited `00674A00`, `00249210`); 5 outbound (page-cited `00249210`, `003BC2D0`, `003C2210` call Resource bodies `0032E620`, `0032E400`, `00249210`). Substantive edges include `00674A00` is called by `001B1C10`; `00674A00` is called by `001B1440`; `00674A00` is called by `0020BE50`; `00674A00` is called by `0020C1B0`; the remaining edges run through shared helpers the page cites.
- **Story_Event_Quest_Hunt — SERVICE (1 edge).** 1 outbound (page-cited `002E16B0` call Story_Event_Quest_Hunt bodies `PersistentFlag_SetBank2048` (0032ABF0)). Substantive edges include `002E16B0` calls `PersistentFlag_SetBank2048` (0032ABF0).
## The `003BC4E0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`003BC4E0` (1,163 B) — one of `0039BEC0`'s four callers, previously unread — is
an **event dispatcher on a TIM2-registry client record**: `[rdx]` selects among
arms `1` (`003BC8A3`), `0x10` (`003BC593`), `0x12` (`003BC522`), default →
`005C5230` (`003BC51D`). The record carries flag bits at `+0xD0`, u16 ids at
`+0xCC`/`+0xCE`, and pointer fields `+0xF8`/`+0x110`/`+0x118`.

- **Arm `0x12`** (`003BC522`): `+0xD0` bit 0 → `002F83E0(6)`, bit 1 →
  `002F83E0(0x17)`; clears `+0x110`, destroys `+0x118` via `003697F0`, then
  `003C2210(rbx)` and stores the record into `02B457E0` (`003BC57C`).
- **Arm `0x10`** (`003BC593`): `al == 2` gate, `[rdx+8] == 9` sub-dispatch,
  three `003697F0` node frees, `+0xD0` bit 4 + `+0xF8` →
  `0039BB60`/`0017FA70`/`003697F0` cleanup, then `+0xD8`/`+0xE0`/`+0xE8`/`+0xF8`
  null checks + `+0xD0` bit 7 → `00245020`. This arm calls `003BD8F0`
  (`003BC7A7`) and `003BCAB0` (`003BC7F1`); `0037F140` is the bit-9 predicate
  consulted at `003BC85C`.
- **Arm `1`** (`003BC8A3`) calls `003BC2D0` (`003BC936`) — the release chain.

| member | role | interior |
| --- | --- | --- |
| `0037F140` (26 B) | bit-9 predicate — `([02AED490]+0xE0 >> 9) & 1`, 0 when the object is null (`0037F14D`) | [`0037F14D`](../../_index/ADDRESS-INDEX.md) |
| `003BC2D0` (262 B) | multi-resource release — `00249580`, three `00249210`, two `002F8040`+`002491B0` pairs, tail `00249410` (`003BC3D1`) | [`003BC2EC`](../../_index/ADDRESS-INDEX.md) |
| `003BCAB0` (57 B) | u16 id resolve-and-cache — `0037EDB0([rcx+0xCC])`; `-1` → 0, else `ax` → `[rbx+0xCE]` and tail `0037FD50(rbx, ax)` (`003BCAD8`) | [`003BCAD8`](../../_index/ADDRESS-INDEX.md) |
| `003BD8F0` (87 B) | indexed stream seek — `edx`th 8-stride entry at `[rcx+0x10]` (limit `[rcx+0xE]`), follows the u16 chain at `entry+4` (`0xFFFF` ends), optional `r8` out = `rcx + [rcx+0xA]`, returns `rcx + [rcx+8] + dx` (`003BD930`–`003BD946`) | [`003BD8F8`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003697F0` (node destroy), `002F83E0`,
`003C2210`, `0039BB60`, `0017FA70`, `00245020`, `0037EDB0`, `0037FD50`,
`00249580`/`00249210`/`002491B0`/`00249410`, `002F8040`, `005C5230`.

## SWE2-EC7-89 update (2026-09-20) - `003BC3E0` guarded vtable call measured

`003BC3E0` (82 B) is the guarded callback the section callers
run: under a stack cookie it builds a 0x10-byte descriptor
(`0x10`, the `movsxd` second arg, a null tail) and, when `rcx`
carries a non-null first qword, calls it with the descriptor -
the `00808C40` cookie check seals both paths.
Interior anchor `003BC41E` (the indirect call).

`0037F7C0` (159 B) is the slot erase `0037F1F0` runs on the `+0x18`-stride triple records: `rdi = rcx + (edx + 0xA) * 24`; in-range with `r8d` clear, a `byte[+0]` of 2 downgrades to 3 in place, otherwise `003697F0` frees `[rdi+0x10]` and the byte zeroes; `+0xEE` decrements and the tail `rep movsq` compacts the array - returns 1, or 0 when out of bounds

Interior anchor `0037F81E` (function `0037F7C0`).

`003C2210` (156 B) is the two-row drain `003BC4E0` runs on `[rcx+0x120]` and `[rcx+0x1C8]`: each `0xA8`-stride record frees every pointer in its `[+0x13]`-count `+0x18` array through `0024A680`, clears the count, `003697F0`s the `[+0x0]` head, and clears that too

Interior anchor `003C225A` (function `003C2210`).
