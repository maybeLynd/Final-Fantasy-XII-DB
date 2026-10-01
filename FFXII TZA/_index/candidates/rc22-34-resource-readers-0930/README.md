# RC-22 to RC-34: the PS2-image resource readers — `.as7`, `.btm`, the "menu manifest", `loca_*.cl2`, `menuquest.lst`, `meshdata.mg` (SWE2-DATA, 2026-09-30)

**Question.** SWE2-CONTRACT registered thirteen static format questions as DD residue of the
`02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats` pages (RC-22 to RC-34). This record answers them from the
certified image (`73461d08…`) and the full extract (`D:/FFXII_TZA_extract`). No runtime evidence is used, and none is
needed for any residue named below. Nothing is routed to ASTRA.

The register rows and the owning pages are SWE2-CONTRACT's to incorporate. This record edits neither.

| RC | question | verdict |
|---|---|---|
| RC-22 | `.as7` payload subformat | **ANSWERED** — a static-dictionary LZ stream (§1) |
| RC-23 | the block at `tailOff` | **ANSWERED** — the codec head plus the shared dictionary, read for every page (§1) |
| RC-24 | the `offsets[]` walker | **ANSWERED** — `0024AA00`, two callers (§1) |
| RC-25 | which `char_silhouette` pages are indexed | **NARROWED** — whole 516-page groups, group = `{0,1,3,2,4,5}[c]`, `c` ≤ 5 (§2) |
| RC-26 | `.btm` texel packing | **ANSWERED** — 4 bpp, low nibble first (§5) |
| RC-27 | the file supplying the `font_stf` glyph table | **ANSWERED** — `fontpack_fs.bin`; ids 130–135 are never requested (§5) |
| RC-28 | glyphs per face against the 1,237 kerning pairs | **ANSWERED** (counts), three static leftovers (§5) |
| RC-29 | the walker of `.rdata` `008FCE00`–`008FD2D0` | **ANSWERED, premise refuted** — it is the developer console's page table, not a resource manifest (§3) |
| RC-30 | the reader of a loaded `loca_*.cl2` | ~~**NARROWED** — no static request route to ids `0xE2`–`0xE4` exists outside three index-computed sites (§3)~~ **ANSWERED by `../rc30-census-0930/`** (corrected 2026-09-30) |
| RC-31 | the `menuquest.lst` parser | **ANSWERED** — `0037EFC0` and `0037E5B0`; order-independent (§4) |
| RC-32 | the `meshdata.mg` reader | **ANSWERED** — a two-entry sub-mesh directory, three draw paths (§6) |
| RC-33 | its undecoded bytes | **ANSWERED** — every byte placed; a few fields have no reader (§6) |
| RC-34 | the `mainN.psd` textures | **ANSWERED, traced** — `Tm2_Menu\w_mainN.tm2` (§6) |

Each script below prints its checks with a positive control and ends `FAILS 0` at `73204a188`; `pe.py` (section-aware,
SHA-checked image reads) and `kind7.py` (the kind-7 path arrays as `002DF9A0` installs them) are shared helpers.

| script | pins |
|---|---|
| [`as7_decode.py`](as7_decode.py) ([out](as7_decode.out)) | RC-22/23/24: walker and codec pins; every page of all 18 shipped `.as7` decoded |
| [`silhouette_pages.py`](silhouette_pages.py) ([out](silhouette_pages.out)) | RC-25: the page arithmetic, group table, setter and its callers |
| [`manifest_walker.py`](manifest_walker.py) ([out](manifest_walker.out)) | RC-29: every reference to the block (rip, image-base-relative, pointer) and its geometry |
| [`manifest_item_labels.py`](manifest_item_labels.py) ([out](manifest_item_labels.out)) | RC-29: every entry's console label |
| [`request_lists.py`](request_lists.py) ([out](request_lists.out)) | RC-29/30: the three list-request helpers, their `.rdata` id lists, the `.mrp` and `.cl2` coverage |
| [`cl2_requests.py`](cl2_requests.py) ([out](cl2_requests.out)) | RC-30: argument-shaped immediates of `0xE2`–`0xE4`, the computed-id request sites |
| [`lst_reader.py`](lst_reader.py) ([out](lst_reader.out)) | RC-31: the readers of the `.lst` buffer, the lookup, the `+0x04` consumer, all 9 files |
| [`btm_font_census.py`](btm_font_census.py) ([out](btm_font_census.out)) | RC-26/27/28 (21 checks) |
| [`mg_reader_check.py`](mg_reader_check.py) ([out](mg_reader_check.out)) | RC-32/33/34 (125 checks) |
| [`mg_slotwalk_scan.py`](mg_slotwalk_scan.py) ([out](mg_slotwalk_scan.out)) | RC-32: no other 0x20-stride slot walk off `s32[+0x10]` |

## 1. `.as7` — the walker, the page codec and the tail block (RC-22, RC-23, RC-24)

**The walker is `0024AA00(as7, out, first, n)`.**
- It reads `count` as the big-endian u16 from bytes `+2`, `+3` (`0024AA0A`, `0024AA26`) and fails when `first ≥ count`.
- `n = 0` or `n > count` means all pages; `n` is then clamped to `count − first`.
- `tail = as7 + be32[+4]` (`0024AA62`–`0024AA97`).
- It zeroes the output cursor `02091090` and stores the output base at `02090788`.
- For each page `i` it calls `00248500(as7 + be32 offsets[i], tail)` (`0024AAC3`–`0024AAF4`); a 0 return fails the walk.
- A raw E8/E9 sweep finds three call sites:
  - `00292768` in `00292390`, for `item_gra`: sheet slot `(id >> 6) + 2` through `00292050`, page `id & 63`, one page;
  - `002CF2B4` and `002CF2CE` in `002CEFD0`, for `char_silhouette` (§2).

**The page codec is `00248500(payload, tail)`, a static-dictionary LZ.** It reads `mode = tail[0]` and `k = tail[1]`.
- When `mode ≤ 2`, the page's output length is `be16 tail[2..3]` and the dictionary is `tail + 4`.
- When `mode = 3`, the length is the page's own first two bytes and the dictionary is `tail + 2`.
- Modes 1 and 2 return 0: only 0 and 3 decode.

Tokens are read until the output length is reached:
- **`1nnnnnnn`**: a literal run. `n + 1` bytes are copied from the payload.
- **`0c` then `c2`**: a copy of `((2c) >> (8 − k)) + 3` bytes from `dictionary[(c << 8 | c2) & (0xFFFF >> (k + 1))]`.
  The source is the dictionary in the tail, never the output.
- Producing more than the output length fails (`0024866A`).

With the shipped `k = 5` a copy token is `0LLLLLOO OOOOOOOO`: a 5-bit length (+3) and a 10-bit dictionary offset.

**Corpus (all 18 shipped files, 7,216 pages).** Every page decodes to exactly the output length, and its tokens consume
exactly its `offsets[]` span, so the page boundaries are the codec's. Every copy stays inside the tail block. Controls:
- with `k − 1` only 6 of the 7,216 pages still decode;
- raw page spans come in 991 different sizes, so the pages are not fixed-size texel blocks.

| file | pages | tail | output per page | output bytes |
|---|---|---|---|---|
| `item_gra00`–`06` | 64 each | mode 0, `k` 5, 900–1,028 B | 6,144 B | 255 distinct values |
| `item_gra07` | 64 | mode 0, `k` 5, **38 B** | 1,536 B | **all zero** — an empty sheet |
| `char_silhouette` | 3,096 | mode 0, `k` 5, 1,028 B | 1,024 B | 256 distinct values |

The `in` and `ch` copies are byte-identical. The `7C 05` units the page noticed are copy tokens: 0x7C = a length of 31 + 3,
from dictionary offset 0x005.

**RC-23 answered:** `tailOff` points at `{u8 mode, u8 k, be16 outLen, dictionary}`, read by every page decode.

**Not claimed:**
- the pixel geometry of a decoded page (6,144 or 1,024 bytes);
- whether the output is drawn as 8-bit indices against the `Item_Clut` palette. The binmenu page §5b's `id >> 6`
  palette pick fits it, but that is not traced here.

## 2. `char_silhouette` — which pages are indexed (RC-25)

`002CEFD0` decodes two runs of `0x102` pages: `[g·0x204, g·0x204 + 0x102)` into its `+0xE0` buffer and the next `0x102`
into `+0xE8` (`002CF249`, `002CF2A0`–`002CF2CE`).
- `g = T[s]`, where `T = {0,1,3,2,4,5}` is the 16-byte `.rdata` copy from `00917160` plus two immediates (`002CEFEF`–`002CF007`).
- `s` is the signed byte at `+0x10D`.
- So a page is decoded only as part of its whole 516-page group, and the six groups tile the 3,096 pages exactly.

Writers of `+0x10D`:
- The image-wide byte-write sweep over displacement `0x10D` (`tools/dispscan.py 10D 10E`) finds two:
  - the reset `002CEDC8` (`0xFF`);
  - the setter `002CEE00`, which clears the "silhouette on" bit (`+0x10C` bit 1) when its argument exceeds 5 (unsigned).
- The setter has two call sites:
  - `00567A52` passes −1;
  - `0056A05E` passes the word at `+0x60` of the record `00282DF0` returns for index `word [0209AC30] + 0xDE0`.

**Every page is reachable exactly when that word takes each value 0–5; values above 5 draw no silhouette.**

**Stays open (static):** which values the record word `+0x60` holds for the records the menu selects. That is a
data-flow question over the `0209AC30 + 0xAC8` record table, not a runtime-only fact.

## 3. The block at `008FCE00` and the `loca_*.cl2` request (RC-29, RC-30)

**RC-29: the premise is refuted.** The block is the **developer console's page layout table**, not a menu resource
manifest:
- It is 14 pages × 22 rows of u32 console command ids, stride `0x58`, exactly `0x4D0` bytes.
- Three rip-relative references reach it (`001D150F`, `001D537D`, `001D542A`), as does one image-base-relative read,
  `001CD186` (`[rsi + rcx·4 + 0x7DCE00]` with `rsi` = image base). The owning pages' "no rip-relative or pointer-table
  reference reaches the block" was a narrower sweep.
- The readers:
  - the console label filler `001D0390`;
  - the page-header refresh `001D5260`, which formats `<Information Page>` / `<Page %d/%d>` with 14 pages hard-coded:
    `mov dword [rbx+0xA88], 0xE`;
  - the row renderer `001CD0E0`, which switches on `id − 1 ≤ 0x125`.
- Row = `[obj+0xA88]`, column 0–21, matching the console pages' "`page·22 + row` → command id" (arm-catalogue slice E §8).
- `manifest_item_labels.py` gives every one of the 266 used ids its label from `001D0390`'s stores (`+0x130 + 8·id`).
  Page 3 — the run `0xDF, 0xE1…0xF2` the pages read as the `Loca` / `bin_menu` ids — is `Unlock All license`,
  `Set clan point`, … `Set count of killed monsters`, then `Load` / `Save Debug Menu Settings`. Ids `0xD1` / `0xD2`
  (209 / 210) are those two rows, which close most pages; id 2 is the blank first row.
- The coincidence with kind-7 ids is numeric only.

**The `.mrp` files with no constant request** (the MRP sheet's list) mostly come through three `.rdata`-list request
helpers the census could not see (`request_lists.py`):
- `003933F0(pool, out, u32 ids[], n)` → `00249320` per id;
- `00393460` and `003934F0`, which take 0x18-stride records `{u32 id, …, u64 +8, u32 +0x10}` → `002493D0`.

| file | kind-7 id | requested by |
|---|---|---|
| `gameover.mrp` | `0x38` | the list `00D11CA0` in `003EF830` |
| `quest.mrp` | `0x92` | `00D237D8` in `00579AF0` |
| `Party_Book.mrp` | `0xCC` | `00D23680` in `00574E80` |
| `save_load.mrp` | `0x6F` | `00D23D98` in `00582790` (the MRP sheet's own trace; control K1) |
| `shop_new.mrp` | `0x96` | `00D238E0` in `0057B780` (also a list, not a constant) |
| `title_menu.mrp`, `E3_Logo.mrp` | `0x3B`, `0x89` | no list and no argument-shaped constant (K3; the same sweep finds the `w_menu` and `Loca` constants) |

`nowload` and `title_fore3` have no path in the first kind-7 arm. Those four open lines belong to the MRP sheet's own
residue, not to RC-29.

**RC-30: narrowed.** Nothing in the image names ids `0xE2`–`0xE4` (`Loca_gil` / `Loca_bhm` / `Loca_rbl.cl2`) as a request:
- No argument-shaped immediate `0xE2`–`0xE4` precedes a request API call. `cl2_requests.py` S1: the 5 / 1 / 3
  argument-shaped hits are unrelated calls; the controls find the `Loca.mrp` constant `004040FE` and `w_menu.mrp` in `00562F90`.
- No list helper carries them.
- The only data dwords holding them next to other menu ids are the console page table above and an identity sequence
  (`01F420C8`–`01F438B0`, ids 0–0xFF at stride 0x18).
- Of the pool API's computed-id sites, six cannot reach `0xE2`–`0xE4`:
  - `0xE8+byte` (`loca_NN.tm2`), `0x496+byte`, `0x142+byte`;
  - `0x129` / `0x12A+byte` (`menuquest`);
  - the `00D23740` u16 table + 1 (≥ `0x229`);
  - `rdx+0x31` with callers passing 0 / 1 / 2 (`m_all*.efx`).

Three sites are not bounded here:
- `002CEAE0` (`0x10 + byte[obj+0xB2D]`, the `face_guest` family);
- `003C9950` (`0xE + byte[obj+0xC1]`, the `map_efe00..06` family);
- `00575C30` (a `00D23740` table entry plus two words).

The path-API sites whose kind is itself computed (18) are also outside this bound.

~~So **no reader is reachable through any request route this record could trace**. The `CLT2` component order and
whether the `+0x22` variant selects a decode stay unanswerable from code until one of the unbounded sites is shown to
produce `0xE2`–`0xE4`.~~

*Corrected 2026-09-30 (SWE2-DATA, [the RC-30 census](../rc30-census-0930/README.md)) and narrowed verbatim
(SWE2-AUDIT-SEM, `../auditsem-review-rc22-34-0930/REVIEW.md` §6 N1):* "No constant or `.rdata`-list request names
`0xE2`–`0xE4`. Among the computed-id request sites, the location-map loader `003C1F00` requests kind 7 id
`0xE1 + byte [entry + 1]` at `003C208D`, which forms `0xE2`–`0xE4` for bytes 1–3; the route to a `loca_*.cl2`
reader runs through that site and the shipped entries." The site is register-held, so this record's list missed it
(its `0x142 + byte` row is the other request in the same function); `003C26C0` reads the file as an external CLUT.
The census supersedes this paragraph.

**Stays open (static):** the index ranges of `byte[obj+0xB2D]` and `byte[obj+0xC1]`, the `00575C30` sum, and the kind of
the computed-kind path-API sites.

## 4. `menuquest.lst` (RC-31)

The widget `0037F4D0` requests kind 7 `0x128` (`.dat`) and `0x13A` (`.lst`) into its object's `+0xC8` and `+0xD0`
(`0037F750`, `0037F778`). The object is the singleton `02AED490`: `0037F614` stores it and `0037F51E` clears it.

A linear census of every function holding a rip reference to `02AED490` (43 sites, 27 functions) finds **two** readers
of the `.lst` buffer. Of the widget procedure's own callees, only the release `0037F860` touches `+0xD0`.
- **`0037EFC0(questId)`**, the name lookup:
  - it scans `u16 [+0xE]` directory entries at `+0x10`, stride 8, comparing the u16 `questId` at `+0`;
  - on the first match with `dataRel = u16 [entry+2] ≠ 0xFFFF` it returns `lst + u16 [+0x08] + dataRel`;
  - otherwise it returns the empty string at `00D111BA`.
- **`0037E5B0`**, the row builder:
  - it probes the same directory with the `questId` `(u32 [dat record + 0x10] >> 8) & 0x3FF`;
  - it takes the entry's `+0x04` **byte, low nibble only**, into its output record's `+0xE`;
  - it stores the same string at output `+0x10`.

Answers:
- **`+0x04` = 100 is not read** by either reader or by anything else in the census: it bounds nothing in code.
- **`+0x08` is read as a u16**, not a u32.
- **The directory's `+0x04` word** is a threshold. `00577C30`, one of `0037E5B0`'s four callers, sets the row's state to
  `0037EE10(questId) ≥ nibble` when the `.dat` record's low byte is 1 (`00577C9D`–`00577CB3`). Only 0, 3 and 4 ship.
- **The shipped id order does not matter.** The lookup is a linear first-match, the ids are unique in all 9 files, and
  first-match equals the sorted lookup for every id (L3). No entry uses the `0xFFFF` sentinel.

## 5. The `.btm` exfont (RC-26, RC-27, RC-28)

### RC-26 — ANSWERED: 4 bits per texel, low nibble first, cells at power-of-two pitch

- `00364210` fills the glyph cache node but does **not** copy texels:
  - it finds the record by a linear scan of the font's glyph table;
  - it rounds `cellW` / `cellH` up to 8/16/32/64/128 into node `+0x14` / `+0x15`;
  - it stores `bitmap + pixelOffset` at node `+0x18` (`00364346`–`00364359`).
- The copy is the cell upload in `003649A0`: `00474650(dst, [node+0x18], dbp 0x3440, psm 0x14, w, h)` (`00364BE0`,
  `00364BF9`, `00364BFF`), which tail-jumps to the GS transfer builder `003A22A0`.
  - Its transfer length is `003A1F20(w, h, psm) / 4` qwords.
  - `003A1F20`'s jump table sends PSM `0x14` to the `w·h/8`-word case: **4 bits per texel** (PSMT4).
  - Controls from the same table: `0x13` → `w·h/4` (8 bpp), `0` → `w·h` (32 bpp).
- Corpus: in all six `fontpack_fs.bin` copies, the records of glyph tables 6–11 sorted by `pixelOffset` tile back to
  back at `pow2(cellW) × pow2(cellH) / 2` bytes.
  - **3,164 / 3,164** neighbours tile; **0** tile at the 8-bpp size (control).
  - Every table starts at offset 0, and the `in` / `ch` tables end **exactly** at their `.btm` sizes. At 8 bpp they would
    overrun by one cell.
- Nibble order: of the texels outside the authored `cellW × cellH` inside each pow2 cell, **0** are non-zero read
  low-nibble-first, against **1,590** read high-nibble-first (control). The left texel of a byte is its low nibble.

### RC-27 — ANSWERED: the glyph tables come from `fontpack_fs.bin` (kind 7 id `0xD2`); ids 130–135 are never requested

- `00D10C98` = `{130..135, 218..223}`, with one reference, `00365810`'s `lea`.
- `00365810` requests id `table[ecx − 1]`. Its only caller, the loop `0053EC90`–`0053ECA4`, passes `ecx = 7..12`: rows
  6–11, ids **218–223**, the six `.btm`.
  - Raw rel32 (`E8`/`E9`/`0F 8x`), rip-displacement and data-qword sweeps find one site.
  - Control: the same sweep finds `00364210`'s caller `00364BA6`.
- Ids **130–135** are NULL in all ten kind-7 path arrays.
- Glyph table `[022CBE00 + 0x10 + f·8]` and bitmap `[022CBE00 + 0x110 + f·8]` share one index.
- The tables are filled by `00366080` from `003643A0`, the completion of `003658F0`'s request for kind 7 id **`0xD2` =
  `PackFiles\fontpack_fs.bin`**. Every shipped copy holds 12 tables, so tables 6–11 are the `font_stf` faces'.
- **Two corrections for the owning sheet:**
  - its "companion resource … ids 130–135" is wrong;
  - `00364380` is the `.btm` requests' completion callback (sets bit `slot` of `[022CBE00 + 0x240]`), not a glyph measure.

### RC-28 — ANSWERED (counts)

- Glyphs per face (tables 6–11):
  - `in` / `ch` / `cn` / `kr` packs: 78 each;
  - `us` / `it` packs: **78, 78, 127, 127, 127, 127**. The 127-glyph tables are the 78 plus 49 accented Latin glyphs.
- All twelve `stf` `.ker` files carry the same 1,237 pairs. A pair has both code points in a face for **398** pairs of a
  78-glyph face and **663** of a 127-glyph face. The PC `us/font_stf_a.dat` also gives 398 (control).
- The comparison is "both elements are glyphs of the face", not rendered spacing.
- Pairing per language arm:
  - six arms (majority directory `de`, `es`, `fr`, `it`, `uk`, `us`) pair the **`us` `fontpack_fs.bin` with the `in` `.btm`**;
  - in those arms the 49 extra cells of the `b` / `c` tables lie past the end of the loaded `.btm`;
  - the `kr` / `cn` arms name `ExFont` directories the extract does not contain.

**Stays open (static):**
1. Which language index selects which arm. The arms are named by majority directory, an inference.
2. What the file layer does for the absent `kr` / `cn` `.btm` paths.
3. Whether any `font_stf` text drawn with fonts 8–11 in the six `us`-pack arms uses one of the 49 accented glyphs. The
   staff-roll text was not read.

## 6. `worldmap/meshdata.mg` (RC-32, RC-33, RC-34)

### RC-32 — ANSWERED: a two-entry sub-mesh directory, three draw paths

**The file is a two-entry directory of sub-meshes, not a header of section offsets.**
- `00274780(buf, i)` returns `buf + s32[buf + 8·i]` (`00274783`, `00274786`); only the even dwords are read.
- The four header dwords are two `{offset, size}` pairs:
  - sub-mesh 0 at `0x10`, `0x2C0` bytes;
  - sub-mesh 1 at `0x2D0`, `0x3280` bytes;
  - together they fill the file exactly.
- Each sub-mesh opens with `{idxOff, idxCount, vtxOff, vtxCount, slotOff, slotCount}`, relative to the sub-mesh start.
- Slots are 0x20 bytes: `char name[16]`, `s32 indexStart`, `s32 indexCount`, `s16 colour[4]` (RGBA, 0x80 = 1.0).

The three draw paths:
1. **`005556A0`** (via `00562F30`, from the map widget `00552250`) draws sub 0: four textured tiles.
   - Four consecutive vertices per slot, in a fixed order.
   - Vertices are `{f32 s, t, 1, 1}{f32 x, y, z, w}`.
   - It does not read sub 0's index stream.
2. **`00555400` → `00555D10`** draws sub 1:
   - from `005528C0` via `00562F40`, textured with `w_shade_p`;
   - from `0055A8A0`, untextured.
   Index bit 15 starts a new strip and re-emits GS `PRIM` (`00556240`); bits 0–14 are the vertex index. `PRIM` is `0x4C`
   or `0x5C` (triangle strip), or `0x0A` (line strip) when bit 0 of `01F2CAC8` is clear. Vertices are
   `{s32 RGBA}{f32 xyzw}`; texture coordinates are projected, not stored.
3. **`00563110`** binds the textures (RC-34).

A raw E8/E9 sweep gives exact call-site sets for the nine consumers. Rip and data-qword sweeps show none is reached
through a stored pointer (control: `0055A8A0`'s installer `lea` at `0055A84B`). `mg_slotwalk_scan.py` finds no other
0x20-stride slot walk.

**"The header lists its offsets in a different order" dissolves:** the page read the directory and sub 0's header as
one header.

### RC-33 — ANSWERED

- **Name slot `unk10`** is not a field. The page's slot layout is 4 bytes out of phase:
  - `unk10` is name padding;
  - `base` = `indexStart`, `count` = `indexCount`;
  - `tail` = the s16 RGBA colour (126, 126, 126, 127).
- **`0x1B0`–`0x2A0`** is vertices 8–15 of sub 0. The block at `0xB0` is sixteen 0x20-byte vertices.
- **`0x2B0` / `0x2C0`** is one 16-entry index stream, sub 0's.
- **Table B at `0x2D0`** is sub 1's header (`idxOff 0x2B00`, 956 indices, 341 vertices, 2 slots). The "pair stream at
  `0x3280`" is interior to sub 1's index stream (174 strips).
- **Bytes with no reader** in the reader set:
  - the directory's two size dwords;
  - both `idxCount`s;
  - sub 0's index stream;
  - sub 0 vertex `+0x08` / `+0x0C` (1.0 in all sixteen).
  The whole vertex array is also copied into a packet (`00555786`), whose consumer is not traced.

### RC-34 — ANSWERED (traced)

- `00563110` matches each slot name against the table `00D23270`:
  - `main0..3.psd` → `w_main0..3`;
  - `upper` → `w_shade_p`;
  - `linetex` → `w_line01`.
- On a match it stores `0024A5A0(texture name)`, the named-image registry entry at `0208F580`, over the slot's first qword.
- `00562F90` created those entries through `002493D0` for kind 7 ids `0xAA + i`, and `00249670` fills each one on load.
- So **`mainN.psd` draws with `Tm2_Menu\w_mainN.tm2`** (ids `0xAB`–`0xAE`, all four shipped). Control: id `0xA8` =
  `WorldMap\meshdata.mg`.
- Sub 1's slots are unnamed: the world map passes `w_shade_p.tm2` (id `0xAA`) in.

**Not claimed:**
- the consumer of the packet copy;
- the live values of the view matrix and of the projection constants `02CA8F80`–`02CA8F8C`.

## Consumer check (EVIDENCE-POLICY 4a)

This record changes no page. Every consumer below is routed to SWE2-CONTRACT, which holds the RC rows and incorporates
them, or is untouched history.

| consumer | finding against it | state |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` rows RC-22 … RC-34 | verdicts above | routed-to-SWE2-CONTRACT |
| `as7-menu-graphics-containers.md` §2 / §3 / §7 ("payload subformat not decoded", "tailOff content unexamined", "walker not isolated", `+0x04 tailOff` "no reader found") | §1, §2 | routed-to-SWE2-CONTRACT |
| `cl2-menu-colour-tables.md` §3 / §7 (the "menu resource manifest", "no rip-relative … reference reaches the block") and `mrp-menu-resource-packages.md` §7 (RC-29) | §3: the block is the console page table; the `.mrp` list requests | routed-to-SWE2-CONTRACT |
| `lst-menuquest-list.md` §2 / §3 / §7 (`+0x08` "u32 dataOff", `+0x04` "capacity", `kind` / `aux`, "reader not isolated") | §4 | routed-to-SWE2-CONTRACT |
| `btm-exfont-bitmaps.md` §3 / §4 (ids 130–135 as the glyph-table half; `00364380` as a glyph measure) | §5 | routed-to-SWE2-CONTRACT |
| `mg-worldmap-mesh.md` header and slot structs (`unk10`, `base` / `count` / `tail`, the 240 bytes, table B, "header order") | §6 | routed-to-SWE2-CONTRACT |
| `binmenu-guest-face-and-map-effect-images.md` §5b (SWE2-DATA): "`offsets[]` walker not isolated" | §1 | routed-to-SWE2-CONTRACT (the reconciliation line is on CONTRACT's `as7` page) |
| Developer-console pages (`arm-catalogue-slice-E` §8 "a dword table in `.rdata`") | §3 gives its address; nothing contradicts | agrees |

## Crossings into other layers

The functions this record reads sit in the owning pages' layers and in these neighbours. Each crossing is a read of a
neighbour's data or a call into its API; no neighbour body's semantics is claimed beyond what is quoted.
- **UI**: the menu widgets (`0037F4D0`, the map widgets, the gambit / license panes).
- **Developer**: the console table.
- **Resource**: the pool and path request API, the named-image registry, the kind-7 path arrays.
- **Presentation**: the GS transfer builder and PSM size table, the world-map draw paths.
