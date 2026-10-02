---
system: kind-0x54 effect mesh records
category: 17-Presentation-Rendering
status: PARTIAL — record layout and census complete; the consumers read 2026-09-30 renormalise the +0x24 vectors (normals); SD-140 answered 2026-10-01 (SWE2-ORACLE, execution-proven: +0x28 is a per-corner RGBA8 vertex colour on the GS 0x80=1.0 scale, +0x2C a per-corner float texture coordinate, the 00432300 kernel the PS2 colour modulate); open residue: the uncharacterised pass operators and the clipper 00521450 (status line current 2026-10-01, SWE2-DATA)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "loader 00436D00 disassembled from the authority image (NATIVE/STATIC);
    census over all 3,698 shipped .efx/.efb files (AUTHORED-DATA) — two evidence
    classes kept separate throughout"
corpus_validated: "3,698 / 3,698 effect files (3,288 .efx + 410 .efb) walked; every
  0xB00 record decoded, 2026-09-16"
last_reviewed: 2026-09-16
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# Kind-`0x54` effect mesh records — authored census

Package: `FABLE-REQ-SWE2-DATA-EFFECT-MESH-0X54`. Answers register questions **BI-3a**
(the `+0x24` / `+0x28` / `+0x2C` array contents) and **BI-3d** (whether authored
records exceed the inline-record capacity). Native layout source: loader
`00436D00` ([§22.2 of the unclassified page](../../99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md));
dispatcher `003A9EF0` hands it the record payload. Evidence classes:
**NATIVE/STATIC** for the layout, **AUTHORED-DATA** for every count and
distribution below. ~~Semantic labels (normals / colours / UVs) remain
distributional hypotheses — no consumer body was read for them here.~~ *(Corrected 2026-09-30, SWE2-DATA: the two
vertex-prep consumers are now read (§8). They renormalise blended `+0x24` vectors to unit length, so the normals label
is consumer-backed; the colour and UV labels for `+0x28` / `+0x2C` stay distributional (`SD-140`).)*

| | |
|---|---|
| files examined | 3,698 / 3,698 `.efx` + `.efb` |
| files containing kind-`0x54` records | 1,087 (29.4 %) |
| kind-`0x54` records | 2,252 |
| `0xB00` chunks total | 30,033 (record-store stream; kinds `0x50`–`0x59`) |
| `0xA00` chunks (element definitions) | 31,635 |
| `0x800` chunks (sub-records, subtype 0–8) | 32,639 |

*Caveat 2026-09-29 (FABLE, GI-8): this walk reads each file as one chunk stream from `+0x10`, so it stops at the first
blob header of every `.efb` (whose EFX streams are embedded blobs) and never sees the 531 EFX streams embedded in `.cm`
/ `.mpk` files. Over every stream there are 48,868 `0xA00` and 53,351 `0x800` chunks ([the dispatch page](effect-element-type-dispatch.md)
§2.8, [`type_census.py`](members/type_census.py)); the kind-`0x54` figures of this page were not re-walked and are a
lower bound.*

## 1. Where the records live

`0xB00` chunks carry the record-store stream. Each chunk holds **one** record:

```text
0xB00 chunk +0x00: u32 chunk length (16-byte aligned)
          +0x04: u16 flag = 0x100
          +0x06: u16 type = 0xB00
          +0x08: u32 stream length (= length - 0x10)
          +0x0C: u16 key        (all 2,252 kind-0x54 records: key = 0)
          +0x0E: u8  kind = 0x54
          +0x0F: u8  sub        (the selector id elements reference)
          +0x10: payload, padded with slack so the record stays 16-aligned
```

Stream-entry kind histogram over all `0xB00` chunks: `0x50` 4,520 · `0x51` 4,622 ·
`0x52` 13,161 · `0x53` 374 · **`0x54` 2,252** · `0x56` 2,238 · `0x57` 1,836 ·
`0x58` 746 · `0x59` 284.

## 2. The payload layout (loader `00436D00`)

```text
+0x00  u8  flags        all 2,252 records: 0x07 (bits 0-2 -> runtime +0x18C;
                        bit 3 borrow-vs-copy is never set in authored data)
+0x02  u16 tri          triangle count   -> +0x10
+0x04  u16 quad         quad count       -> +0x12
+0x06  u16 c14          position count   -> +0x14, array +0x20 (16 B each, w forced 1.0)
+0x08  u16 c16          vector count     -> +0x16, array +0x24 (16 B each)
+0x0A  u16 c18          4-byte count     -> +0x18, array +0x28
+0x0C  u16 c1A          8-byte count     -> +0x1A, array +0x2C
+0x0E  u16 c1C          id-byte count    -> +0x1C, ids +0x180, handles +0x184 (8 B each)
+0x10  u16 c1E          inline 20-byte record count -> +0x1E, array +0x30 (cap 16)
+0x12  arrays begin:    pos, vec, 4B, 8B, 20B,
                        then (flags&1) index list A, index list B
                        [2 * (6*tri + 8*quad) bytes each -> +0x170 / +0x174],
                        (tri+quad) per-primitive bytes -> +0x188,
                        c1C id bytes -> +0x180
```

### Size control (the census control)

`size = 0x12 + 16·c14 + 16·c16 + 4·c18 + 8·c1A + 20·c1E + (flags&1 ? 2·(6·tri+8·quad) : 0) + (tri+quad) + c1C`,
then 16-byte alignment padding (`0–15` slack bytes).

**Result: 2,252 / 2,252 records reproduce their stride exactly, 0 failures.**
The layout is complete — there is no undecoded tail.

## 3. Count relationships

| relation | result |
|---|---|
| `c1A == c18` | **all 2,252** — the 4-byte and 8-byte arrays are always the same length |
| `c16 != c14` | 1,670 / 2,252 (74 %) — vector count usually differs from position count |
| `key` | `0` in every record (matches the resolver call's `ecx = 0`) |
| `flags` | `0x07` in every record |
| `sub` | `{1:962, 2:626, 3:525, 4:47, 5:22, 6:19, 7:15, 8:9, 9:10, 10:3, 11:6, 12:3, 13:1, 15:1, 20:3}` |

### BI-3d — inline-record capacity

**`c1E` is `0` in every one of the 2,252 records.** The 20-byte inline-record
array is never populated in authored data; the loader's 16-entry (`0x140` B)
window is never even touched, let alone exceeded. The capacity question is
answered vacuously: no authored record approaches it.

## 4. The three arrays — value distributions (BI-3a)

| array | element | entries | distribution |
|---|---|---:|---|
| `+0x24` vectors | 16 B × c16 | 52,808 | **100 % unit-length** (\|v\|² = 1 ± 1e-3); w field `0x00000000` in all — direction vectors, not points. Normals hypothesis. |
| `+0x28` 4-byte | 4 B × c18 | 147,220 | 1,358 distinct u32s; `0x80808080` alone is 47 %; byte-3 dominated by `0x80`/`0x81`/`0x00`/`0x40` — consistent with packed RGBA where `0x80` is the GS full-opacity alpha. Colour hypothesis. |
| `+0x2C` 8-byte | 8 B × c1A | 155,916 pairs | float pairs: 74 % both components in `[0,1]`, 15 % in `[-1,2]`, 11 % larger floats, **0 NaN** — consistent with texture UVs. UV hypothesis. |

`+0x20` positions: file-side w is `0x3F800000` (1.0 f) for all 50,707 entries —
the loader's forced `w = 1.0` is a no-op over shipped data; positions are
homogeneous points. The `w = 1` vs `w = 0` split between `+0x20` and `+0x24` is
the point/direction distinction, which is what the normals hypothesis rests on.

Because `c1A == c18` always, the `+0x28` and `+0x2C` arrays are paired
per-control-point attributes (colour + UV under one index), while `+0x24`
normals are counted independently of `+0x20` positions in three quarters of the
records — consistent with normals indexed separately from positions.

### Secondary lists (BI-3b-adjacent, collected cheaply)

- Index lists `+0x170` / `+0x174` are **not copies**: they differ in 2,249 / 2,252
  records. Two distinct index arrays of identical byte size.
- Per-primitive byte `+0x188`: values `{0: 40,922, 1: 264, 2: 612}` — a small
  selector, mostly 0.
- `+0x1C` id bytes: `c1C` is 0 in 1,813 records, 1 in 425, 2 in 14. Every nonzero
  id resolves to a same-file kind-`0x52` record (key 0, sub = id) — **439 / 439
  all-match, 0 partial**.

## 5. Element type `0x05` — the mesh consumers

Element definitions arrive through `0xA00` chunks: `{u16 id, u8 type, u8 pad}` at
`chunk+0x0C`, record published at `chunk+0x10` by `003A9A70` (table `02EBEF78`,
768 slots; `0x800` chunks are a separate 320-slot sub-record class whose `+0xE`
byte is a subtype bounded ≤ 8 — never an element type). Setup `00538DB0` reads
32 id bytes at record `+0x570`, resolving each nonzero byte through
`003AA280(key = 0, kind = 0x54, sub = id)` into the handle array `+0x5A0`; walk
`00449AB0` reads the `+0x570` ids, the `+0x5A0` handles and the `+0x590` mode
byte.

| | |
|---|---|
| type-`0x05` elements | 5,164 (all `0xA00` records, all ≥ `0x640` B — every one carries the full `+0x570`/`+0x590`/`+0x5A0` region) |
| files using type `0x05` | 1,088 |
| slots filled (of 32) | `0:1, 1:4,268, 2:894, 3:1` — **max 3** |
| id → same-file kind-`0x54` sub linkage | **5,163 all-match**, 1 all-zeros, 0 partial |
| id value set | `{1..13, 15, 20}` — exactly the kind-`0x54` sub value set |

`+0x590` mode byte (bitfield: bit 4 = track vs random mode per §22.3; bit 5 feeds
`+0x1F1.7` → VU0 path `00438860`; bit 0 feeds `+0x1F1.3` → alternative path
`00437130`): dominant values `0x0D` (1,724), `0x0E` (2,831), `0x0F` (52), `0x2E`
(337), `0x2F` (143). Derived path census: VU0 514, alternative 1,791, inline
2,859; random-mode (bit 4) only 2 elements (value `0x1F`).

## 6. Artifacts

- [`members/effect-mesh-54-records.tsv`](members/effect-mesh-54-records.tsv) —
  one row per kind-`0x54` record (file, offset, header, all eight counts,
  computed size, control result).
- [`members/effect-mesh-54-element05.tsv`](members/effect-mesh-54-element05.tsv) —
  one row per type-`0x05` element (file, chunk offset, filled slots, mode byte,
  raw `+0x570` id bytes).
- [`members/census_mesh54.py`](members/census_mesh54.py) — the generator
  (corpus root `Database/Tools/work/DATA/mesh54/fx_all`).

## 7. Limitations

- ~~The `+0x24`/`+0x28`/`+0x2C` roles are **distributional hypotheses**; the
  consumer side (`00435050` / `00434CD0` vertex prep, `00438860` / `00437130` /
  inline emit) resolves the record's pointer fields but their per-vertex packing
  into the emitted vertex was not traced here.~~ *(Corrected 2026-09-30, SWE2-DATA: the vertex prep is read in §8;
  `+0x24` is consumer-backed as unit normals. How the byte kernel and the three emit paths pack `+0x28` / `+0x2C` into
  the emitted vertex is `SD-140`.)*
- The `0x800`-chunk class (32,639 sub-records, subtypes 0–8) is a different
  record family — not covered by this census beyond the subtype histogram.
- `.efb` files share the same chunk grammar; no `.efb`-specific deviation was
  observed in the control.

## 8. The vertex-prep consumers (SWE2-DATA, 2026-09-30)

Both consumers take the record's three attribute arrays by their `+0x24` / `+0x28` / `+0x2C` offsets and counts
([`fx54_consumers.py`](../../_index/candidates/dd-data-4-0930/fx54_consumers.py), V1–V3 and control C1, FAILS 0).
One caller chooses between them.

| consumer | `+0x24` vectors (count `+0x16`) | `+0x28` 4-byte (count `+0x18`) | `+0x2C` 8-byte (count `+0x18`) |
|---|---|---|---|
| `00435050`, one record | `memcpy` of 16 bytes per entry (`004351D3`–`004351EC`) | through a per-byte kernel together with the draw-parameter block's `+0x40` colour — the dword at `[01FD4A78]+0x800+0x40`, written by `0026EE00` from the element instance's `+0x240` (`00435197`–`004351B0`; **narrowed per `SD-140` X4**: the operand is the parameter block, not the element) | `memcpy` of 8 bytes per entry (`004351B5`–`004351CE`) |
| `00434CD0`, two records blended by a factor | a normalised lerp (`0043500D`), or a copy of the second record's entries when element `+0x1F1` bit 6 is set (`00434FAF`) | blended per channel (`00434F33`), then the same byte kernel (`00434F47`) — **only when `+0x1F1` bit 4 is clear; when set, the record's own `+0x28` goes straight to the kernel unblended** (`SD-140`) | a float-pair blend (`00434FAA`), or a copy when element `+0x1F1` bit 5 is set (`00434F4C`) |

The `+0x24` blend (`00432030`) sums the squares of the three blended components, takes `sqrtf`, divides one by the
length (a zero length keeps a constant) and scales the components before storing each 16-byte entry. Renormalising after
interpolation is what a unit normal needs, and it matches the census (every shipped `+0x24` entry is unit length with
`w = 0`). The `+0x28` bytes are not used raw: they pass through the byte kernel with the draw-parameter block's `+0x40`
colour (one dword — `[01FD4A78]+0x800+0x40`, filled by `0026EE00` from the element instance's `+0x240`), which
is consistent with a colour modulated by the element, but ~~the kernel was not decoded~~ *it is now
(`SD-140`, below)*. The `+0x2C` pairs are copied or
blended as floats, which is consistent with UVs. ~~Neither label is consumer-verified, and the emit paths were not traced.~~

- [x] **What the byte kernel does to the `+0x28` entries with the ~~element's~~ draw-parameter block's `+0x40` colour,
  and how the emit paths pack `+0x28` / `+0x2C` into the emitted vertex.** This decides whether they are colours and texture coordinates. **SD-140**
  (SWE2-DATA, 2026-09-30). *(**Answered 2026-09-30, SWE2-ORACLE** — execution-proven against shipped code over seeded
  trials; record [`sd140-vertex-prep-kernel-0930`](../../_index/candidates/sd140-vertex-prep-kernel-0930/README.md),
  `sd140_kernel.py` 23 checks FAILS 0.) `+0x28` is a **per-corner RGBA8 vertex colour** on the GS `0x80` = 1.0 scale
  (`0x80808080` is the exact identity, 47 % of shipped entries) and `+0x2C` a **per-corner float texture coordinate**;
  `c18 = 3·tri + 4·quad` in all 2,252 census records. The kernel `00432300` is the PS2 colour modulate
  `min(255, e·c >> 7)` against the draw-parameter block's `+0x40` colour (only its first dword is read). The two-mesh
  path `00434CD0` rounds a `cur·(1−w) + next·w` blend through `00433830` when `+0x1F1` bit 4 is clear, else calls the
  kernel unblended. Per pass, all three draw paths re-colour — flat broadcast when `param+0x1A8+p` is set, else
  per-corner modulate by `param+0x138+4p`, with `00432CC0` writing `alpha = trunc(alpha·L[n].w) mod 256` from the lit
  per-normal table — and the builders emit the colour as `float(byte)` lanes 0..255 and the UV pair as GS STQ divided
  back by the corner's `Q`. What stays open is the uncharacterised pass operators
  (`0043E7B0`/`00434630`/`00434760`/`00396F20`/`00394B70`/`0043E840`) and the clipper `00521450` itself.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — CLIENT.** Both vertex-prep routines this page cites
(`00434CD0` at `00434E3C`/`00434E46`, `00435050` at `00435130`/`0043513E`) call
`00229E40`, a seven-byte scheduling-domain getter that returns the cached
language id `[01E02814]` (written at startup by `0022A0CB`; see
[language-selection-and-locale-ids](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md)
AV-1). Each caller tests `1 ≤ id ≤ 6` — the Latin-alphabet range — and only
then writes the alternate vertex-attribute constants into the emitted packets;
outside that range the default packing stands. The crossing is that these
routines consult the language cache when packing this record's arrays; nothing
on this page owns or writes the global.
