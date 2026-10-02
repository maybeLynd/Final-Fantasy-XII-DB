---
system: The `lmap` sublocation table — menumap_location.bin
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation; §10.5's items are answered in place) — the zone routes (array C) answered: map-jump links, each gated by a map-jump-group flag and drawn once as a connection line; A's x/y and the three StoryEvent-filed readers answered (SWE2-CONTRACT's record swe2contract-ddres-b5-0930 and the map-screens page); the 8-byte block is the record's zoom set read by `003BE680` and the marker `+0xC` label is drawn by `003C25BD` (RC-35/RC-36 answered on FABLE's records); the 60,000-range ids resolved 2026-09-16 (§10.7) (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Map
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `003BDDE0`, `003BDFF0`, `003C1A20`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN160
corpus_validated: "9 of 9 locale copies, all 48 records walked, 2026-09-06"
container_format: lmap
last_reviewed: 2026-09-30
archive_formats:
  - "lmap | explained | menumap_location.bin (.bin member): record arrays A-D - (kind 7, 0xA3) by 003BC2D0 into widget +0xE0, accessors 003C0340 / 003BF430 / 003BFF20 / 003C1070, section 10"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-lmap-audit-pass-1, RESTATED 2026-09-13 against the NATIVE layout - the pass was measured under the 12-byte-header model and its offsets are not comparable to the native one, so they are restated here rather than left to be read as current. ACCEPTED: the native layout is counts 4 | A | B | C | block 8 | D, verified at the image - 003BF4D3 lea rcx, [r10+r10*2] / 003BF4D7 lea rax, [rcx*8+4] / 003BF4DF add rax, r9 is rec + 4 + 24*i exactly, and 003BFF20 and 003C1070 place C at rec+4+24*(A+B) and D at C+20*countC+8. WHAT SURVIVES: container, directory, length equation and the three markers reproduce in 9 of 9 copies; array D is 97 entries in 7 records, not 6, and the file size proves it; D+0 holds at 97 of 97; two byte-picture shapes were drawn from single entries; the 111 = 111 match between C self-pairs and array B is a coincidence (34 of 48 per record). WHAT MOVES: the C/A cross-reference I recorded at +12 and +14 is C +0 and +2 in the native frame, and it strengthens from 501 of 545 to 545 of 545 - the 44 shortfall was records with C>=1 being measured from the wrong base. WITHDRAWN: my B +16/+18 finding, which was the C[0] of the 40 records that have both B and C read as if it belonged to B.
  crossref_clean: false
  reopened_count: 0
---

# The `lmap` sublocation table — `menumap_location.bin`

> **One record per sublocation, and it is the index the map screen is built around.** Forty-eight
> records, each holding four arrays: the map's own points of interest, its links out to other areas,
> and two smaller tables. This is the file that says which places exist and how they connect.

~~**Status is `PARTIAL` and deliberately so.**~~ *(Superseded 2026-09-30: the field meanings are read in §10 and in §3's rebuilt table; the page is DOCUMENTED.)* *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-02-b2-0930/REVIEW.md) correction 5)* The container and the **complete record structure** are
established and walk to the byte across every record. **The field meanings inside the four arrays
are not**, and §7 says exactly which. This sheet exists because the structure is worth having on its
own — it is what any reader of this file needs before it can ask what a field means.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **9 of 9** locale copies of `menumap_location.bin` |
| size | **23,852 bytes — every copy, all nine** |
| records | **48**, walked entry by entry in every one |
| distinct contents | **6** across the 9 copies — `ch`/`cn`/`kr`/`us` share one; `de`, `es`, `fr`, `in`, `it` each differ |
| magic `lmap` | 9 / 9 |

---

## 1. What the player sees

**The world map screen's table of contents.** When the map names the place you are in, offers the
routes leading out of it, and marks the points of interest on the drawn plan, those come from here —
one record per sublocation, forty-eight of them.

The drawn picture itself is not in this file. That is [`sloc`](sloc-menumap-container.md), the
menu-map container, which holds **48 base units** — the same count, one image set per sublocation.

**All nine language copies are the same size and six are different**, so something inside varies by
language while the structure does not. The grouping is unusual and unexplained: `ch`, `cn`, `kr` and
`us` share one copy, while `de`, `es`, `fr`, `in` and `it` each get their own.

## 2. The layout

### 2.1 Header and directory

```struct LmapHeader base=file size=0x0A
+0x00  char[4]  magic        'lmap' - 6C 6D 61 70, in 9 of 9
+0x04  u32      version      202 in 9 of 9
+0x08  u8       _pad08       0 in 9 of 9
+0x09  u8       recordCount  48 in 9 of 9; the bound 003C0340 and 003BF430 test the index against
```

*(Corrected 2026-09-13, FABLE — §10. Published as "`+0x08 u16 _unknown` = `0x3000`; no reader found". The two bytes are
`00 30`, and the native reader tests every record index against **byte `+9`** (`003BF453`, `003C0340`). So it is the
record count, 48, and the `u16` reading was a byte-order artefact.)*

```struct LmapDirEntry base=record size=0x2
+0x00  u16  recordOffset  ABSOLUTE file offset of the record
```

**48 entries at `+0x0A`, ending at `+0x6A`.** The offsets are **absolute file offsets, not relative
to any base** — the directory ends at 106, two zero bytes follow, and the first record begins at
**108**. The last record ends at **exactly the file end** (23,248 + 604 = 23,852).

> **Absolute, and that is worth stating because its sibling is not.** The
> [`sloc`](sloc-menumap-container.md) container in the same folder uses offsets based at a constant
> `+0x20`. **Two files, one directory, two different conventions** — a reader that carries one
> across will be wrong by a small constant, which is the failure mode that produces plausible
> garbage rather than an obvious crash.

### 2.2 The record — four counts, three arrays, an 8-byte block, a fourth array

> **✖ Corrected 2026-09-13 (FABLE, §10): the header is 4 bytes, not 12.** The game's own reader places array A at
> **record `+4`** (`003BF4D3`–`003BF4DF`: `rec + 4 + 24*entry`), B after A, and C after B. It then skips **8 bytes after
> array C** to reach D (`003BFF85`–`003BFFAA`, `003C10E4`–`003C110B`). The published model put those 8 bytes in front of
> A as `_head`. That has the same total length, so the length equation and the ~200,000-combination search could not
> tell the two apart. The three `0xFFFF` markers could not either, because an 8-byte phase shift keeps every stride.
> Every array A, B and C entry below was therefore read **8 bytes late**. The "`_head`" is array A entry 0's first
> 8 bytes, and every record has `countA ≥ 1`, so the shift never broke a walk. The original model is kept struck
> below.

```struct LmapRecord base=record size=0x04
+0x00  u8  countA    entries in array A, 24 bytes each, starting at record +4
+0x01  u8  countB    entries in array B, 24 bytes each, after A
+0x02  u8  countC    entries in array C, 20 bytes each, after B
+0x03  u8  countD    entries in array D,  4 bytes each, after C and an 8-byte block
```

```
record layout = counts(4) | A 24*countA | B 24*countB | C 20*countC | block(8) | D 4*countD
recordLength  = 4 + 24*countA + 24*countB + 20*countC + 8 + 4*countD
```

~~The arrays follow a 12-byte header in order, A then B then C then D: `recordLength = 12 + 24*countA + 24*countB +
20*countC + 4*countD`.~~ The length is the same number, and the placement is what changed.

**This holds for all 48 records exactly**, and it is the only solution: a search over four header
bytes against fifteen candidate strides and four candidate header sizes — roughly 200,000
combinations — returned **exactly one** fit satisfying all 48 records simultaneously.

*(2026-09-13, FABLE: exactly one among header-then-arrays models. The search had no candidate with a block *between* the
arrays, and the native layout is one of those, with the same length for every record. "Only solution" was a statement
about the search space, not about the file.)*

**And the arithmetic is not the only evidence.** Walking the four arrays with this model consumes
every record to its exact final byte, and each array then shows its **own** consistent internal
marker:

| array | stride | entries in the corpus | `0xFFFF` sits at (native offset) | as published (8 bytes late) |
|---|---:|---:|---|---|
| A | 24 | **384** | **`+14`, in 348 of 384** | `+6` |
| B | 24 | **111** | **`+22`, in 101 of 111** | `+14` |
| C | 20 | **545** | **`+16`, in 519 of 545** | `+8` |
| D | 4 | **97** (§9 — published as 6) | — | D was not shifted |

> **Three different marker offsets, each consistent within its own array, is the structural check
> the length equation cannot give.** A wrong grouping that happened to satisfy the arithmetic would
> smear those markers across arbitrary offsets. These do not smear.
>
> *(2026-09-13, FABLE: true of grouping, silent on phase. A model shifted by a whole number of bytes inside every array
> keeps every marker consistent. What decided the phase was the native reader, and then the cross-reference: at the
> native offsets array C's two ids hit **545 of 545**, where the shifted offsets gave 501 (§10.3).)*

### 2.3 What the entries look like

Shapes only, measured over the `us` copy at the **native** offsets (§10). The field meanings §10 establishes are marked; the rest are
shapes.

```
A (24B)  x:u16 y:u16 | u16 u16 | 0000 0000 | fieldId:u16 | FFFF(348) | u16 (0 in 327) | 0000 | u16 u16 (0 in 379)
B (24B)  u16 u16 | u16 u16 | u16 u16 | u16 (60,201-60,244) | 0000 | u16 | u16 | u16 (512-5,130) | FFFF(101)
C (20B)  fieldId:u16 fieldId:u16 | u16 u16 | u16 u16 (0 in 508) | u16 u16 | FFFF(519) | 0000
block 8  f0 00 f0 00 40 01 00 00 in 46 of 48 records; eb 00 eb 00 eb 00 00 00 and d2 00 d2 00 d2 00 00 00 once each
D (4B)   nodeFieldId:u16 | memberFieldId:u16
```

~~`A (24B) 00 00 00 00 | id:u16 | FFFF | …`, `B (24B) u16 | u16 | u32 (60000-range) | …`, `C (20B) 00 00 00 00 | u16 | u16 | FFFF | …`~~
*(the published pictures, read 8 bytes late; each began with the previous entry's last 8 bytes)*

**Array B carries a value in the 60,000 range at `+4`** *(native `+12`, §10)* — `0xEB29` = 60,201 in the first entry. The
same range appears in the sibling `cmap` and `wmap` files in this folder. **What that range is, is
not established here**; it is recorded because the coincidence across three files is a lead worth
someone's time and not a finding.
*(Answered 2026-09-16, §10.7: a `menu_mapname.bin` string id in the "To X" destination-label band. Note added
2026-09-30, SWE2-CONTRACT.)*

**Array C's `+12` repeats a value that also appears as array A's `id`** — `0x0124` = 292 in
record 0's first entries of both arrays. (Published as `+10`; `+10` is the `0000` slot the shape
above already shows, zero in 545 of 545 entries — corrected §9.) A cross-reference between the
two arrays was **not** claimed here; §9 tests it over the corpus and it holds. *(At native offsets the pair is C `+0`
/ `+2`, and it holds for 545 of 545 entries — §10.3.)*

## 3. The loader contract

> **Superseded 2026-09-13 (FABLE): the reader is found — §10.** The world map menu widget loads this file as
> kind-7 id `0xA3` (`003BC333`–`003BC340`) and reads it through `003C0340`, `003BF430`, `003BFF20` and `003C1070`. The
> two searches below failed for the reason §3 itself predicted: the file is reached through the resource path table
> and a widget pointer, never by a constant. The table is kept as the record of those searches.

**Not established, and this sheet does not pretend otherwise.**

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | — | **never** | — | **yes** — `lmap` occurs **0 times in the image**, as ASCII or as the dword `0x70616D6C` |
| everything else | — | — | — | **no reader found — by the searches named below** |

**The searches that failed**, so the negative is a statement about them and not about the binary:

1. **The constant.** `lmap` as ASCII and as `0x70616D6C`: 0 hits. *Blind spot:* a constant built by
   arithmetic or compared in halves would not appear.
2. **The path route**, which worked for `licd` and `battle_pack`: `menumap_location.bin` is reached
   through the per-locale path table populated once at boot by `FUN_002DF9A0`. **That establishes
   how the file is found, not what parses it** — and the consumers of that runtime table are reached
   by argument or accessor, which an address scan structurally cannot follow. The same wall
   documented in [`sloc`](sloc-menumap-container.md) §3.

**No `Inert` row is offered for any field except the magic**, because a field nobody has found a
reader for is not a field known to be unread — the distinction this database keeps paying for.

**The contract rebuilt from the native reader (2026-09-30, SWE2-CONTRACT; [`swe2contract-ddres-b5-0930`](../../_index/candidates/swe2contract-ddres-b5-0930/README.md), [`lmap_readers.py`](../../_index/candidates/swe2contract-ddres-b5-0930/lmap_readers.py),
with the member roles of [the map-screens page](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) §4).** Offsets are the native ones of §10. It supersedes the "everything else" row above.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| header byte `+9` | every accessor, as the record count (§10.2) | record `>=` it → 0 / null | — | no |
| header `+0x0A + 2n` | the accessors, added to the table pointer in 32 bits (§10.2) | — | — | no |
| record `+0`..`+3` counts | `003BF430`, `003C0340`, `003BFF20`, `003C0740` (C1) | point `>=` `countA + countB` → null, kind 3 | — | no |
| point `+0` / `+2` (`x`, `y`) | `003C2320` → draw row `+4` / `+6` (P1) | — | — | no |
| point `+4`..`+7` (four bytes) | `003C2320` → draw row `+8`..`+B`, the directional next-target selectors (P1; `003BE810` chases them) | — | — | no |
| point `+8` / `+0xA` | `003C2320` → draw row `+0x18` / `+0x1A` (P1); zero in 384 of 384 A entries | — | — | no |
| point `+0xC` | kind 0: the zone's field id — `003C2320` (P2), `003C1680` → `003C17E0` (P5), `003BCDE0` (C2). Kind 1: the destination-label id (§10.7) — `003C25BD` (`003C2320` marker arm) draws it through `002F9920`; `003BEB06` (`003BE950`) aims the cursor at it (RC-36, `rc36-lmap-label-fable-0930`) | — | — | no |
| point `+0xE`, `+0x12`, `+0x16` | gate ids — `003C06E0`, `003C2320` (P3), `003C0F70` (map-screens §4) | gate not passed → point disabled | — | no |
| point `+0x10` | kind and flags: `& 3` → draw row `+0x1E` (P2); `>> 2 & 0xF` the kind nibble (map-screens §4) | — | — | no |
| point `+0x11`, `+0x15` (markers) | `003C2320` kind-1 arm: marker kind (`0xD` → `0x2F`), link selector → `003BDDE0` (P3) | — | — | no |
| C `+0` / `+2` | `003BCDE0`: the two endpoint field ids (C2) | the point is neither → no link | — | no |
| C `+4`..`+0xF` | `003BCDE0`: `+4`/`+6` and `+0xC`/`+0xE` tested by `003C1180`; `+4`..`+0xF` copied to the link descriptor (C2) | `003C1180` fails both → no link | — | no |
| C `+0x10` | `003BCDE0`: map-jump-group flag gate, `0xFFFF` = none (C2) | flag clear → no link | — | no |
| C `+0x12` | no read in `003BCDE0` or `003C0740` (C3); zero in 545 of 545 | — | — | not claimed beyond those two |
| the 8-byte block | `003BE680` reads words `+0`/`+2`/`+4` — the record's zoom set (RC-35, `rc35-lmap-gap-fable-0930`) | — | — | no |
| D `+0` / `+2` | `003BFF20`, `003C1070` (§10.2, §10.4) | — | — | no |

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x002DF9A0` | populates the per-locale path table that locates this file | partial — established in [`licd`](../../12-Items-Equipment-Shops-License/license-board-grid-format.md) §3 |
| `0x00379870` | the `NPS2` transform consumer for the *sibling* `sloc` container | ✅ — cited as context, not as this file's reader |
| `003BC2D0` | the widget's loader: kind 7, ids `0xA2` / `0xA3` / `0xA4` into widget `+0xD8` / `+0xE0` / `+0xE8` | ✅ §10.1 |
| `003C0340` | record `n` → `countA + countB`, bounded by header byte `+9` | ✅ §10.2 |
| `003BF430` | (record, point index) → A or B entry pointer and its kind (0 = A, 1 = B) | ✅ §10.2 |
| `003BFF20` | (record, member field) → node field id through array D, or −1 | ✅ §10.2 |
| `003C1070` | (record, field id) → "is this the node the player is at" | ✅ §10.4 |
| `003C0380` | field id → record index (the area the field belongs to), or −1 | ✅ §10.4 |

~~**This sheet cites no address as a reader of its own format, because none was found.**~~ *(Superseded 2026-09-13 by the
rows above.)* ~~The status stays `PARTIAL` because most entry fields are still shapes.~~ *(Superseded 2026-09-30: the field meanings are read in §10 and in §3's rebuilt table; the page is DOCUMENTED.)* *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-02-b2-0930/REVIEW.md) correction 5)*

## 5. Corpus survey

| | |
|---|---|
| size 23,852 in every copy | **9 / 9** |
| `version` = 202 | **9 / 9** |
| `+0x08` = `0x3000` | **9 / 9** |
| 48 directory entries, ascending and distinct | **9 / 9** |
| last record ends exactly at EOF | **9 / 9** |
| every record walks to its exact end under the §2.2 model | **48 / 48, in every copy** |

**Record sizes run 108 to 1,720 bytes** and every length is a multiple of 4. Array populations
across the 48 records: **A 384, B 111, C 545, D 97** (§9 — D was published as 6) — array D is empty
in 41 of 48 records but holds 73 entries in one, and array C is the biggest.

**The locale grouping is the outlier worth recording.** Nine copies, six distinct contents, all
identical in size:

```
ch cn kr us   share one copy
de            its own
es            its own
fr            its own
in            its own
it            its own
```

> **`us` grouping with `ch`, `cn` and `kr` is not what a language split looks like.** It is also a
> *different* partition from the `ch`/`in` vs `cn`/`kr` split this session measured in
> [`licd`](../../12-Items-Equipment-Shops-License/license-board-grid-format.md) and in
> `action_data.bin`. **Two different regional groupings in one archive**, and neither is explained.

## 6. Falsification pass — 2026-09-06

| attack | result |
|---|---|
| Is `+0x0A` a directory at all? | The 48 values ascend, are distinct, all land in the file, the first sits 2 bytes past the directory's own end, and the last record ends exactly at EOF. Four independent constraints. |
| Are the offsets absolute or based? | **Absolute.** Tested by requiring the last record to end at EOF — a based reading misses it by the base. |
| Is the record model fitted or forced? | **Forced.** ~200,000 candidate (header, four strides) combinations, **exactly one** satisfies all 48 records. A model fitted to a few records would have many solutions. |
| Could the arithmetic be right and the grouping wrong? | **Checked, and this is the important one.** The three arrays each show their own consistent `0xFFFF` offset (`+6`, `+14`, `+8`). A wrong grouping satisfying the same arithmetic would scatter those. |
| Is the "48 sublocations" figure inherited or measured? | **Measured here** — 48 directory entries. Prior work states 48 sublocation records; **that agreement is corroboration, not the source**, and 48 is also `sloc`'s base-unit count, which makes it a count match and therefore not deciding on its own. |
| ~~Is the 60,000-range value a text id?~~ | **Answered 2026-09-16 (SWE2-DATA, §10.7).** Yes — a `menu_mapname.bin` string-id-table key. |
| Was a reader found and not reported? | No. §3 and §4 state plainly that none was found, and name both failed searches. |

*(2026-09-13, FABLE: this pass tested grouping and length, and both survive. It could not test phase, and the phase was wrong
by 8 bytes — §10.3.)*

*(Superseded reading, 2026-09-30, SWE2-CONTRACT: the last row's "Was a reader found? No" records the 2026-09-06 pass. The
reader was found on 2026-09-13 (§10), and §3 now carries the contract rebuilt from it.)*

**The killer observation.** The central claim is *"a 12-byte header whose first four bytes count
four arrays of stride 24/24/20/4."* One record whose length disagreed, or one array whose marker
offset scattered, kills it. Tested on all 48 records in all 9 copies.

## 7. What this document does not claim

- **What any array's fields mean.** Shapes are given in §2.3; no field is named beyond `id`-shaped
  and coordinate-shaped observations, and even those are described rather than asserted.
  *Narrowed 2026-09-30 (SWE2-CONTRACT): §3's rebuilt contract names every field a traced reader uses. Left: the 8-byte
  block (RC-35) and array B's `+0xC` (RC-36).*
- ~~**That array C's `+10` cross-references array A's `id`.**~~ **Answered 2026-09-13 (OPUS), and
  the offset was wrong**: it is ~~`+12` **and** `+14`~~ `+0` **and** `+2` at native offsets *(corrected 2026-10-02, OPUS: §10.3: the shipped `us` file gives 545 of 545 for each; `+12` / `+14` was the shifted model)*, each an A id from the same record in ~~**501 of~~ **545 of
  545** entries with wrong-record controls at **0**, and array D's `+0` in **97 of 97**. §9.
- ~~**What the 60,000-range value in array B is.**~~ **Answered 2026-09-16 (SWE2-DATA, §10.7)**: a `menu_mapname.bin` string id — array B is keyed by "To X" destination-label ids 60,201–60,244.
- ~~**What the 8 bytes at record `+0x04` hold.**~~ **Dissolved 2026-09-13 (FABLE, §10)**: they are not a head. They are
  array A entry 0's first 8 bytes (`x`, `y` and two `u16`s), which is why they are distinct per record and never ids.
- ~~**What `+0x08 = 0x3000` is for.**~~ **Answered (FABLE, §10)**: byte `+9` is the record count.
- ~~**Anything about the loader.**~~ **Answered (FABLE, §10)**: widget loader `003BC2D0`, accessors `003C0340` /
  `003BF430` / `003BFF20`.
- ~~**What the 8-byte block between C and D is.** No reader of it was found among the accessors: all of them step over it.~~
  *Answered 2026-09-30 (SWE2-CONTRACT, on FABLE's [`rc35-lmap-gap-fable-0930`](../../_index/candidates/rc35-lmap-gap-fable-0930/README.md), `9aac223bf`): `003BE680` reads it as three
  words — `+0` returned, `+2`/`+4` written out through pointers; `+6`/`+7` unread. In the common pattern they are
  240/240/320, the record's **zoom set**, consumed by the map screens `002B7B80`/`002BAF80` at three call sites
  (`002B7FFA`, `002BB45E`, `002BBA8D`), index `word [obj+0x138]`.*
- **What A's `x` / `y` are drawn on.** They are coordinate-shaped (`+0` 7–1,333, `+2` 27–1,741), but their reader is
  not traced.
  *Answered 2026-09-30 (SWE2-CONTRACT, [`lmap_readers.py`](../../_index/candidates/swe2contract-ddres-b5-0930/lmap_readers.py) P1): `003C2320` copies them into the location map's draw row
  (`+4` / `+6`), and the draw-list builder `003BE3A0` emits the rows relative to the record's origin ([the map-screens page](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) §4).*
- **Prior work's route-graph reading.** `agent_flow/tools/lcmpos_decode_progress.md` states this
  file supplies "the area-to-area route graph" with "standard and special forms". **That is
  consistent with array B carrying two `0xFFFF` markers where A and C carry one**, but consistency
  is not derivation and this sheet does not adopt it.

## 8. Related

- [`sloc-menumap-container.md`](sloc-menumap-container.md) — the map images, routes and world
  origins. **48 base units to this file's 48 records.** Its directory is based at `+0x20`; this
  one's is absolute.
- [`README.md`](README.md) — the `ps2data/image` long tail and the `.bin` census row.
- `agent_flow/tools/lcmpos_decode_progress.md` — prior work naming this file as the source of the
  48 sublocation records and the route graph. **A tool progress note, treated as a prior reading**;
  the structural claims here were derived independently and the route-graph reading is not adopted.
- `Tools/work/formats/bin-signature-census.tsv` — the frozen census this unit came from.

## 9. Audit pass 1 — 2026-09-13 (OPUS)

§6 is the authoring session's own falsification pass. This is the independent one: every published
figure re-measured from the archive, and the two leads §7 declines to claim tested over the corpus
rather than over one record.

*(`check_already_answered.py` run by term; the two register rows it prints for `lmap` are about the
script-global named `lmap`, not this format. Archive read, never written; nothing executed.)*

### What reproduces — all of it, in all nine copies

**9 of 9** copies, **23,852 B** each, magic `lmap`, version **202**, `+0x08` = `0x3000`; the 48
directory entries ascending, distinct and in-file, the first record **2 bytes** past the directory's
end, the records **contiguous**, the last ending **exactly at EOF**, lengths **108–1,720** and every
one a multiple of 4 — under `12 + 24A + 24B + 20C + 4D`, in **48 of 48 records in 9 of 9 copies**.
Array populations **A 384, B 111, C 545** and the three markers exactly: `0xFFFF` at **A+6 in 348 of
384**, **B+14 in 101 of 111**, **C+8 in 519 of 545**. Six distinct contents over nine copies, and the
shared group is **`ch`, `cn`, `kr`, `us`** — by SHA-256, not by size.

### ✖ Corrected: array D holds 97 entries, not 6

The published total is a counting error, and the file size proves the correction rather than my walk:

```
106 (header + directory) + 2 (pad) + 12x48 + 24x384 + 24x111 + 20x545 + 4x97 = 23,852
```

— the file exactly. With D = 6 the same sum is 23,488, which is not this file. D is held by **7 of
48 records**, with counts **73, 12, 4, 3, 3, 1, 1** (records 40, 7, 27, 41, 46, 6, 38). "Nearly
always empty" survives — 41 records have none — but one record carries more D entries than the whole
corpus was said to have.

### ✔ Established: array C is an edge list over array A, at `+12` and `+14`

*(2026-09-13, FABLE, §10.3: the edge list stands and is now complete. At native offsets it is C `+0` / `+2`, in **545 of
545**. The 44 misses are exactly the 44 records whose last C entry's shifted `+12` read the 8-byte block.)*

§7 declines this as *"the values coincide in the one record examined — one record is not a corpus."*
Here is the corpus. For every array C entry, is its value an array A `id` **from the same record**?

| field | in the same record | CONTROL: next record | CONTROL: record +7 |
|---|---:|---:|---:|
| **C+12** | **501 of 545** | **0** | **0** |
| **C+14** | **501 of 545** | **0** | **0** |
| C+4 | 20 of 545 | — | — |
| C+6 | 8 of 545 | — | — |
| C+16 | 10 of 545 | — | — |
| C+18 | 6 of 545 | — | — |

Identical in `us`, `de` and `it`. **The wrong-record controls return zero, three times** — so the
match is not "small numbers collide": these ids are bound to their own record. Each C entry therefore
names **a pair of A entries**, and the pairs read as edges: record 0's first three C entries are
(292, 305), (292, 306), (292, 307), then (289, 290), (289, 291), (290, 291).

**The published offset was `+10`, and `+10` is not it.** `+10` is zero in **545 of 545** entries —
which §2.3's own shape diagram already showed. The value 292 sits at **C+12** in record 0.

### ✔ Established: array D's first `u16` is an array A id — 97 of 97

| field | in the same record | CONTROL: next record | in the global id set |
|---|---:|---:|---:|
| **D+0** | **97 of 97** | **0** | 97 |
| D+2 | 2 of 97 | 0 | 2 |

So array D's 4 bytes are `{A id, something else}`, and the something else is not an id.

### ○ Partial: array B names A ids at `+16` and `+18` — 40 of 111

Same-record 40, next-record control 0, for both fields. Real but not general; recorded as measured,
not read as a meaning.

> **✖ Withdrawn 2026-09-13 (FABLE, §10.3): an artefact of the 8-byte shift.** At the published offsets, the last B
> entry's `+16` / `+18` is array **C** entry 0's `+0` / `+2`, which is a field id. **40** is exactly the number of
> records holding both B and C entries. At native offsets, B carries no same-record ids anywhere.

### ✖ Two shape over-generalisations, each drawn from one entry

§2.3's shapes are written as literal byte pictures. Measured over the corpus (`us`):

| shape says | measured |
|---|---|
| B has `FFFF` at `+10` **and** `+14` | `+14` in **101 of 111**; **`+10` in 6 of 111** — `B[0]`, the entry the picture was drawn from, is one of the six |
| A is `00 00 00 00` at `+8`–`+15` | `+10` zero **384 of 384**, but **`+8` is non-zero in 57** (26 of them `64`), and `+12` / `+14` in 5 each |
| C opens with four zero bytes | zero in **508 of 545** at `+0` and `+2` — 37 entries are not |

The three *markers* §2.2 relies on are unaffected; it is the **byte pictures** in §2.3 that read one
entry as the shape.

### A near-miss: 111 = 111 is a coincidence

Array C has exactly **111** entries whose `+12` equals its `+14` (a self-pair), and array B has
exactly **111** entries. A structural link between them is the obvious reading and it is **wrong**:
per record the two counts agree in only **34 of 48**, and they differ by up to 2 in either direction
(one record has `countB` 3 and one self-pair; two have `countB` 0 and one self-pair). **The totals
match and the structure does not** — recorded because an aggregate-only check would have published it.

### A negative, with its own control

The record head's `+0x04` and `+0x06` are `u16`s in the id range, so: are they A ids? **0 of 48** in
their own record. The chance control says the same — 11 and 19 of 48 fall in the *global* 380-id set,
about what 380 ids spread over 48–1,151 gives for free. Not ids.

*(2026-09-13, FABLE: the negative stands, and §10 explains it. Those bytes are array A entry 0's `x` and `y`.)*

### Housekeeping

§2.3 names *"the sibling `cmap` and `wmap` files in this folder"*. Those are **magics, not file
names**: the folder holds `menumap_common.bin` (`cmap`, 1,760 B), `menumap_world.bin` (`wmap`,
2,040 B), and a third the page does not mention, `menumap_area.bin` (**`amap`**, 396 B). The
60,000-range recurs in all three (87 / 48 / 38 dwords in `60000..61000` at any alignment — a crude
count, stated as such). Array B's own `+4` values: **111 values, 42 distinct, 60,201–60,244**, and
**not** a consecutive run.

**Not claimed.** What the ids mean, what an edge between two A points is for, what `D+2` is, what the
60,000 range is, what the 8 bytes at record `+0x04` hold (48 distinct values over 48 records; `+0x05`
and `+0x07` are 0 in 23 and 26 of them, so `+0x04` and `+0x06` read as small `u16`s), or anything
about a loader — **§3's two failed searches were not re-run and no reader is claimed here either**.

## 10. The native reader — 2026-09-13 (FABLE)

*(Found while placing the then-unresolved functions `003BDDE0`, `003BDFF0` and `003C1A20` — residual at GN160,
**resolved at GN161**, see §10.5 — which read this table
through the accessors below. Disassembly is tier 1. The corpus checks are [`lmap-native/lmap_native.py`](lmap-native/lmap_native.py)
and [`mapref_ctl.py`](lmap-native/mapref_ctl.py), with their outputs beside them. The archive was read, never written.)*

### 10.1 Who loads it

**The world map menu widget.** `003BC450` creates a `0x278`-byte widget through the widget factory `00244F50`
(`003BC4A2`) and stores it in the singleton `02B457E0` (`003BC4A7`). Its message procedure is `003BC4E0` (row 134 of
`widget-message-handlers.tsv`). Its loader `003BC2D0` makes three resource requests `00249210(pool, 7, id, 2)`:

| id | file (kind-7 path array `01E0E530`) | magic | widget field |
|---|---|---|---|
| `0xA2` (`003BC305`) | `menumap_world.bin` | `wmap` | `+0xD8` |
| `0xA3` (`003BC333`) | **`menumap_location.bin`** | `lmap` | **`+0xE0`** |
| `0xA4` (`003BC35D`) | `menumap_common.bin` | `cmap` | `+0xE8` |

The message procedure releases all three through `003697F0` (`003BC5B8`–`003BC610`) and clears `02B457E0` at `003BC57C`.
`menumap_area.bin` (`amap`) is not among them.

### 10.2 The accessors

| routine | reads | evidence |
|---|---|---|
| `003C0340(n)` | `countA + countB` of record `n`, or 0 when `n ≥ byte[+9]` | `003C0353`–`003C036D` |
| `003BF430(n, i, &kind)` | point `i` of record `n`: `i < countA` → **`rec + 4 + 24*i`**, kind 0; otherwise `rec + 4 + 24*countA + 24*(i − countA)`, kind 1; out of range → null, kind 3 | `003BF46F`, `003BF4D3`–`003BF4DF`, `003BF4E8`–`003BF50B` |
| `003BFF20(n, field)` | C starts at `rec + 4 + 24*(countA+countB)` (`003BFF79`–`003BFF88`). D starts `20*countC + 8` later (`003BFF95`–`003BFFAA`). The routine scans D for `+2 == field` and returns that entry's `+0`, else −1 | `003BFFB4`–`003BFFDC` |
| `003C1070(n, field)` | the same C and D arithmetic (`003C10D7`–`003C110B`), then a membership test — §10.4 | |

**Arrays A and B are one point space.** `003BF430` indexes them together and reports which half the point came from.
Their entries share the 24-byte stride and the `+12` slot: A holds a field id there, B a value in 60,201–60,244.

**The record index is bounded by header byte `+9`**, never by the `u16` at `+8`. Every routine above adds the directory
word to the table pointer **in 32 bits** (`add r9d, edx` at `003BF467`, `add ecx, edx` at `003C0362`). So the reader
works only while the loaded file image sits below 4 GiB. That is a constraint on where the resource can be placed, and it
is not a claim about where it is placed.

### 10.3 The layout correction, and the data that confirms it

The native offsets disagree with §2.2 by exactly 8 bytes for A, B and C. D agrees. Under the native layout, over all 9
copies:

- every record walks to its exact end (**48 of 48** in each copy), as the shifted model also did;
- the `0xFFFF` markers sit at A `+14` (348 of 384), B `+22` (101 of 111) and C `+16` (519 of 545);
- **array C `+0` and `+2` are field ids of the same record's array A in 545 of 545 entries each** (`us`; A `+12` is the
  id). The shifted model's 501 comes from the 44 records whose last C entry read into the 8-byte block, and 545 − 44 =
  501. Its B `+16` / `+18` result of 40 is the 40 records holding both B and C entries (§9, withdrawn);
- `A +8` / `+10` are zero in 384 of 384; `C +18` is zero in 545 of 545; `B +14` is zero in 111 of 111.

### 10.4 What the ids are: field ids, grouped by area

`003C1070(n, X)` returns 1 when `X` equals the current field id: `FUN_00264790`'s override when positive, else
`WorldTransition_GetActiveOrPendingFieldId` `003148F0` (`003C1118`–`003C1128`). It also returns 1 when record `n`'s
array D holds `(X, current field)` (`003C1140`–`003C1152`). `003C0380(field)` inverts the table:

```
group = MapRef_GetPersistenceGroupId(field)                 ; 00264F90, the map-reference table 02099D88
for n in 0 .. 49:                                           ; 003C03AA .. 003C0429
    if menumap_common entry n, byte +0 != group: continue   ; [widget+0xE8] + word[+8] -> u32 count, 8-byte entries
    node = 003BFF20(n, field); if node == -1: node = field  ; a member field maps onto its node
    for i in 0 .. countA+countB-1:
        if 003BF430(n, i) is kind 0 and its +12 == node: return n
return -1
```

**So each record is one sub-location** (§10.6 names all 48). `menumap_common` entry `n` names its persistence group. Array A lists the sub-location's
fields as points (field id at `+12`, a coordinate-shaped pair at `+0`). Array D maps further fields onto one of those
points (`+2` member field → `+0` node field). Array C joins two points of the same area.

**The authored data agrees with that join exactly.** The map-reference file is `ps2data/image/ff12/{ch,in}/common/map_ref.bin`
(magic `MRF\x02`, header `+4` = 48, 1,530 × 8-byte rows). It was found by searching the archive for the table whose row
`+6` reproduces the join, and it is the only file that does. Using it:

| check (`us`, `de`, `it`) | same record | CONTROL: next record's group | CONTROL: record +7 |
|---|---:|---:|---:|
| A `+12` field's persistence group = `menumap_common[n]` byte `+0` | **384 of 384** | **0** | **0** |
| D `+2` member field's persistence group = `menumap_common[n]` byte `+0` | **97 of 97** | **0** | — |

`menumap_common`'s 48 entries carry 47 distinct groups. Group 14 appears at entries **13 and 47**: Giza Plains in the dry
season and the rainy season, two sub-locations over one set of fields (§10.6). *(Published as "entries 12 and 47";
corrected the same day.)*

### 10.5 What stays open

- What A's `x` / `y` are drawn on, and who reads them. They are presumably the plan-map positions, **but not traced**.
  *Answered 2026-09-30 (SWE2-CONTRACT): see §7 — `003C2320`, the location map's draw row.*
- ~~Array B's meaning beyond "the second half of the point space, keyed by a 60,201–60,244 value".~~ **The key resolved
  2026-09-16 (§10.7)**: it is a `menu_mapname.bin` string id in the "To X" destination-label band. The `menumap_common`
  entry `+4` values (`0xEAEA` = 60,138 onward) resolve into the same table's sub-location-name band — the text-id
  reading was right. What array B *does* with a marker point keyed by a destination label — what the widget draws for
  it — is still not read.
  *Narrowed 2026-09-30 (SWE2-CONTRACT, [`lmap_readers.py`](../../_index/candidates/swe2contract-ddres-b5-0930/lmap_readers.py) P3–P5): a marker is emitted into the same draw list by `003C2320`'s
  kind-1 arm, with its marker kind `+0x11` (kind `0xD` remapped to `0x2F`), its gate `+0x12` and its link selector
  `+0x15`, which `003BDDE0` resolves to the linked point. Up to that call (`003C253F`, P4) the arm does not read `+0xC`; it reads it afterwards, at `003C25BD` (RC-36). `003C1680` passes `+0xC` to the
  progress test only for zones. What reads the marker's destination-label id stays open.*
  *Answered 2026-09-30 (SWE2-CONTRACT, on FABLE's [`rc36-lmap-label-fable-0930`](../../_index/candidates/rc36-lmap-label-fable-0930/README.md), `9a4cd5784`): **the narrowing's P4
  held only through `003C253F`** — the marker arm continues to `003C25BD`, which loads `dword [marker+0xC]` and resolves
  it through `002F9920` into draw row `+0x10`: **the location map draws each marker's destination name** (locked markers
  show text `0x3EC` via `002F9860`; a `-1` label falls back to the sub-location's name, unused in all nine copies). A
  second reader, `003BEB06` in `003BE950`, aims the directional cursor at the label box. Every other `+0xC` load in the
  reach reads something else.*
- [x] **RC-36.** Which code reads a marker's `+0xC` destination-label id, and so what the location map draws for a
  marker's label. *(Registered 2026-09-30, SWE2-CONTRACT; static. Answered same day on FABLE's record — the marker arm
  itself draws it.)*
- The 8-byte block and array C's `+4`–`+16`.
  *Array C answered 2026-09-30 (SWE2-CONTRACT, [`lmap_readers.py`](../../_index/candidates/swe2contract-ddres-b5-0930/lmap_readers.py) C1–C3): `003C0740` hands each entry to `003BCDE0`, which reads
  `+0`/`+2` as the endpoints and `+0x10` as a map-jump-group flag gate, tests `+4`/`+6` and `+0xC`/`+0xE` through
  `003C1180`, and copies `+4`..`+0xF` into the link descriptor. So a zone route is a map-jump link between two of the
  area's zones. The map-screens page (UQ-156, narrowed 2026-09-26) shows the same entries drawn once each as the
  lines between the areas. ~~The 8-byte block stays open.~~ *(answered same day — `003BE680`, RC-35)*
- [x] **RC-35.** What, if anything, reads the 8-byte block between array C and array D. *(Registered 2026-09-30,
  SWE2-CONTRACT; static. Answered same day on FABLE's [`rc35-lmap-gap-fable-0930`](../../_index/candidates/rc35-lmap-gap-fable-0930/README.md) —
  `003BE680` reads it as the record's zoom set, §10 residue list.)*
- `003BDDE0`, `003BDFF0` and `003C1A20` read the table through these accessors, but what each
  does is not read. ~~They belong to the world map menu widget and are routed to residual
  placement.~~

  > **CORRECTED 2026-09-14 (OPUS): they are no longer residual, and they are not the menu
  > widget's.** All three sat in GN160's residual set and are absent from GN161's; the
  > certified parent classifies them as
  >
  > | address | `GFZ.V121.CodeDomain` |
  > |---|---|
  > | `003BDDE0` | `Boundary.StoryEvent.GraphNodeStep` |
  > | `003BDFF0` | `Boundary.StoryEvent.GraphPredicate` |
  > | `003C1A20` | `Boundary.StoryEvent.LocationGraphWalk` |
  >
  > **StoryEvent, not a menu widget** — and the third is named for walking a *location
  > graph*, which is this page's subject and its filename. "Routed to residual placement"
  > is therefore withdrawn: there is nowhere else for them to be placed, and this page is
  > where they belong.
  >
  > **A TAG IS NOT A BODY READING.** *"What each does is not read"* above is unchanged and
  > still true. Naming the family a function was classified into is not the same as having
  > read it, and swapping an honest *not read* for a tag name would be the silent promotion
  > the confidence vocabulary exists to prevent.

  *Read 2026-09-14 (SWE2-FRONTIER, [the map-screens page](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) §4, every member body read) and cited here 2026-09-30 (SWE2-CONTRACT):*
  - `003BDDE0` walks the record's points whose `+0x11` kind matches the given point's, and reports the first enabled one.
  - `003BDFF0` returns the record's last enabled point of a given kind.
  - `003C1A20` collects the record's enabled points into `{position, entry, selector}` triples for the draw-list
    builder `003BE3A0`; its selector is a point-kind filter (0 = zones, 2 = every point).
  So all three serve the location map's point list. *What each does is not read* above is superseded by that reading.

### 10.6 The names, from the generator's own header — 2026-09-13 (FABLE)

The archive ships the header the file generator wrote beside the data: `us/worldmap/menumap_world.h` ("made by
CnvWorldMap … Converted from ff12worldmapdata.xls"; its comments are UTF-8). **It numbers the 48 sub-locations 0–47 in
exactly the record order.** It also sets the limits per sub-location:

| header constant | value | this file, measured (`us` and `de`) |
|---|---:|---|
| `menumap_zone_route_route_MAX` (zone routes) | 59 | **max `countC` = 59** |
| `menumap_zone_MAX` (zones) | 20 | max `countA` = 18 |
| `menumap_zone_marker_MAX` (markers) | 16 | max `countB` = 7 |
| `menumap_zone_data_MAX` (zones + markers) | 24 | max `countA + countB` = 21 |
| `menumap_sublocation_ALL` | 48 | 48 records |

**So the arrays have authored names.** A is the **zones**; the native reader keys them by field id (§10.4), so a zone is a
field. B is the **markers**, which share the point space and stride with zones (`003BF430`). C is the **zone routes**,
and C's measured maximum equals the header's limit exactly. D is not named by the header; natively it maps member fields
onto zones. The equalities for A, B and A + B are bounds, not proofs; C's is the one exact match.

`menumap_world.h` also defines 38 areas, 8 named regions, 45 normal and 15 special world routes (60 in all), 18 Strahl
destinations and 59 locations with at most 2 sub-locations each. Those belong to `menumap_world.bin` and are not
tested here. `menumap_sub.h` limits a sub-location to 18 images and 17 info entries, with data at most 320 KB in a
"double buffer" or 512 KB in a "single buffer". Those are PS2-era sizes: the TZA `menumap_sub00`–`47.bin` files are *(corrected 2026-10-02, OPUS: 1,049,520 – 11,544,192 B over the 436 shipped copies, the sloc sheet's corpus)*
~~4–11 MB~~ 1.0–11.5 MB, every one above both limits. The two-slot cache the reader keeps at map-data widget `+0x120` (two `0xA8`
slots, keyed by record index, loading kind 7 id `0x142 + index` = `menumap_subNN.bin`; `003C1F00`, `003C1FF6`) is the
double buffer's shape, and the byte limit did not survive the remaster.

| index | header name | authored name (UTF-8, verbatim) | `menumap_common` group | A | B | C | D | `menumap_sub%02d.bin` bytes |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 0 | `rbn01_s01` | ラバナスタ市街地 | 16 | 7 | 5 | 10 | 0 | 4,461,744 |
| 1 | `fon01_s01` | フォーン海沿岸 | 26 | 12 | 2 | 19 | 0 | 11,018,144 |
| 2 | `mic01_s01` | バルハイム地下道 | 3 | 18 | 3 | 23 | 0 | 10,493,504 |
| 3 | `bds01_s01` | ナブディス王宮地表部 | 23 | 8 | 2 | 9 | 0 | 5,507,776 |
| 4 | `bog01_s01` | 死都ナブディス | 10 | 11 | 2 | 13 | 0 | 5,510,224 |
| 5 | `ene01_s01` | 東エンサ大砂海 | 20 | 9 | 5 | 16 | 0 | 8,130,128 |
| 6 | `enw01_s01` | 西エンサ大砂海 | 21 | 8 | 5 | 13 | 1 | 7,867,824 |
| 7 | `grm01_s01` | ガラムサイズ水路 | 17 | 17 | 3 | 59 | 12 | 8,396,400 |
| 8 | `nac01_s01` | ナルビナ街部＞ナルビナ上層 | 37 | 3 | 2 | 4 | 0 | 1,051,056 |
| 9 | `naf01_s01` | ナルビナ城塞上層 | 15 | 5 | 0 | 4 | 0 | 1,574,736 |
| 10 | `nal01_s01` | 雑居房＞ナルビナ上層 | 2 | 4 | 0 | 3 | 0 | 1,311,936 |
| 11 | `ozm01_s01` | オズモーネ平原 | 29 | 8 | 5 | 14 | 0 | 6,035,920 |
| 12 | `rwg01_s01` | レイスウォール王墓 | 22 | 8 | 1 | 8 | 0 | 5,770,720 |
| 13 | `sav01_s01` | ギーザ草原乾季 | 14 | 8 | 4 | 14 | 0 | 6,295,936 |
| 14 | `slm01_s01` | ラバナスタ地下街 | 39 | 2 | 2 | 3 | 0 | 1,575,376 |
| 15 | `wdl01_s01` | 西ダルマスカ砂漠 | 18 | 7 | 5 | 14 | 0 | 6,034,240 |
| 16 | `ztc01_s01` | ゼルテニアン洞窟 | 33 | 10 | 6 | 22 | 0 | 8,396,224 |
| 17 | `glf01_s01` | ガリフコミューン | 48 | 3 | 1 | 3 | 0 | 1,312,208 |
| 18 | `hne01_s01` | ヘネ魔石鉱 | 45 | 15 | 2 | 23 | 0 | 8,660,704 |
| 19 | `mfr01_s01` | 幻妖の森 | 30 | 8 | 4 | 14 | 0 | 6,559,504 |
| 20 | `vic01_s01` | ヴィエラコミューン | 50 | 3 | 1 | 3 | 0 | 1,574,288 |
| 21 | `dst01_s01` | 東ダルマスカ砂漠 | 7 | 11 | 7 | 16 | 0 | 7,609,232 |
| 22 | `rrp01_s01` | ラバナスタ王宮 | 32 | 5 | 1 | 2 | 0 | 2,098,864 |
| 23 | `alc01_s01` | アルケイディス市街地 | 38 | 7 | 1 | 12 | 0 | 3,149,552 |
| 24 | `alc01_s02` | アルケイディスダウンタウン | 49 | 2 | 2 | 4 | 0 | 1,049,520 |
| 25 | `frs01_s01` | サリカ樹林 | 9 | 11 | 4 | 16 | 0 | 9,705,952 |
| 26 | `byu01_s01` | ビュエルバ | 36 | 6 | 1 | 10 | 0 | 2,889,648 |
| 27 | `lus01_s01` | ルース魔石鉱 | 19 | 16 | 1 | 20 | 4 | 11,544,192 |
| 28 | `mnt01_s01` | モスフォーラ山地 | 12 | 10 | 3 | 16 | 0 | 7,871,936 |
| 29 | `mrm01_s01` | ミリアム遺跡 | 34 | 14 | 1 | 13 | 0 | 6,821,072 |
| 30 | `pbc01_s01` | パラミナ大峡谷 | 25 | 9 | 4 | 15 | 0 | 7,345,536 |
| 31 | `pla01_s01` | ツィッタ大草原 | 8 | 13 | 3 | 18 | 0 | 10,494,848 |
| 32 | `rsn01_s01` | リヴァイアサン艦内 | 31 | 8 | 0 | 10 | 0 | 4,460,672 |
| 33 | `rui01_s01` | ソーヘン地下宮殿 | 11 | 11 | 2 | 20 | 0 | 6,036,496 |
| 34 | `rwf01_s01` | リドルアナ大瀑布 | 28 | 5 | 1 | 6 | 0 | 3,671,920 |
| 35 | `srb01_s01` | セロビ台地 | 27 | 8 | 2 | 12 | 0 | 7,607,920 |
| 36 | `var01_s01` | 港町バーフォンハイム | 47 | 6 | 1 | 8 | 0 | 2,363,104 |
| 37 | `gol01_s01` | ゴルモア大森林 | 24 | 8 | 4 | 14 | 0 | 5,774,576 |
| 38 | `bul01_s01` | 神都ブルオミシェイス | 46 | 4 | 1 | 4 | 1 | 1,574,672 |
| 39 | `gil01_s01` | 古代都市ギルヴェガン | 42 | 7 | 1 | 2 | 0 | 5,245,536 |
| 40 | `gil01_s02` | コアクリスタル | 43 | 2 | 0 | 0 | 73 | 2,098,288 |
| 41 | `dor01_s01` | ドラクロア研究所 | 53 | 5 | 0 | 1 | 3 | 3,164,016 |
| 42 | `rbl03_s01` | *(blank)* | 57 | 10 | 3 | 9 | 0 | 8,655,136 |
| 43 | `rbl02_s01` | *(blank)* | 56 | 7 | 2 | 0 | 0 | 6,818,816 |
| 44 | `rbl01_s01` | *(blank)* | 55 | 3 | 1 | 0 | 0 | 3,146,880 |
| 45 | `rbl04_s01` | *(blank)* | 58 | 9 | 1 | 12 | 0 | 3,936,336 |
| 46 | `bhm01_s01` | バハムート | 52 | 4 | 0 | 0 | 3 | 4,197,520 |
| 47 | `sav01_s02` | ギーザ草原雨期 | 14 | 9 | 4 | 14 | 0 | 6,819,664 |

*(Generated from the archive: the header's `menumap_sublocation_*` defines, the record counts, `menumap_common` byte `+0`
per entry, and the `us` sub-image sizes. Indices 42–45 (`rbl01`–`rbl04`) have no authored name in the header.)*

### 10.7 The 60,000-range ids, resolved — 2026-09-16 (SWE2-DATA)

The 60,000 band is the key space of `menu_mapname.bin`
(`ps2data/image/ff12/test_battle/<lang>/binaryfile/menu_mapname.bin`), an `st2e` string-id table of 285 entries. Every
60000-band dword in this file's array B lands in that table — **42 distinct values, 60,201–60,244, all present, zero
misses** — and they decode to the "To X" destination labels (`60201–60243`; `60244` is a further table entry). So
array B's `+12` is the marker's destination-name id, the same way array A's `+12` is the zone's field id. The
`menumap_common` entry `+4` values (`0xEAEA` = 60,138 onward) land in the same table's sub-location-name band
(48/48 join, wrong-offset controls 0/48) — the "text-id reading likely" note in §10.5 was right.

Full join evidence and the decoded id-space map are in
[wmap-menumap-world-map-graph.md](wmap-menumap-world-map-graph.md) ~~§6~~ §5 *(corrected 2026-10-02, OPUS: the join and the id-space map are its §5)* and
[cmap-menumap-common-sublocation-directory.md](cmap-menumap-common-sublocation-directory.md).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**CombatAction and Movement — CLIENT.** The field id `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) that the
location graph keys on is shared. It is also read by:

- `BattleUnit_TryTriggerNearbyAuthoredFieldAction` and its 477-byte sibling;
- a 4,006-byte movement body;
- two `003EDxxx` movement helpers.

See [choosing the field environment variant](../../03-World-Area-Field/choosing-the-field-environment-variant.md), crossings.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT.** `WorldTransition_GetActiveOrPendingFieldId` is called by the two `0xBC08` map-screen pages (4,847 and 4,810 bytes, Presentation-filed), and a small accessor this page cites is called by a 1,587-byte Presentation body. The map screens read the current field id; the location graph itself does not draw.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Citation spellings (R5), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** `ResourcePath_Init` (2,831 bytes), which this page cites, is called from the 978-byte core start-up root.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT.** `ActorManager_RunFieldRuntimePass`, owned by that layer, calls `00261F90` on this page. That caller is the field-runtime pass over one manager record - `02098E10` at the **`0x288` stride** - which returns at once while the write-in-progress flag is set; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — CLIENT.** `FUN_00261f90`, owned by that layer, calls `003148F0` on this page. That caller is a per-object audio state step: it needs `[obj+0x28] == 0` and bit 6 of `byte[obj+0x10]` clear, then sets bit 5 of that same byte and notifies through `0037C910`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — CLIENT.** `FUN_003160c0`, owned by that layer, calls `00264790` on this page. That caller is a 212-byte walk of the table at `[022C2550]` from `+8`, the same table the equipment-slot eligibility test walks; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**SaveLoad — CLIENT.** `FUN_00582790`, owned by that layer, calls `00249210` on this page. That caller is a 197-byte routine that writes two `.rdata`-sourced strings into `+0x100` and `+0x108` of its argument; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — CLIENT.** `SpawnKeep_RotatePersistenceBanksForAreaTransition`, owned by that layer, calls `003148F0` on this page. That caller is the area-transition bank rotation: it takes a **`0x9428`-byte stack frame** through the stack probe, needs both `[0208E690]` and `[0208E698]`, and compares the current area index against the stored `word[02089372]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **Script_VM_Native_Bridge — CLIENT (5 edges).** 5 inbound (Script_VM_Native_Bridge bodies `00357450`, `0050CDE0`, `0033F310` call page-cited `MapRef_GetPersistenceGroupId` (00264F90), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `0037C910`). Substantive edges include `MapRef_GetPersistenceGroupId` (00264F90) is called by `00357450`; `MapRef_GetPersistenceGroupId` (00264F90) is called by `0050CDE0`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (5 edges).** 5 inbound (Script_VM_Native_Bridge bodies `00357450`, `0050CDE0`, `0033F310` call page-cited `MapRef_GetPersistenceGroupId` (00264F90), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `0037C910`). Substantive edges include `MapRef_GetPersistenceGroupId` (00264F90) is called by `00357450`; `MapRef_GetPersistenceGroupId` (00264F90) is called by `0050CDE0`; the remaining edges run through shared helpers the page cites.
- **Gameplay — SERVICE (1 edge).** 1 outbound (page-cited `003C06E0` call Gameplay bodies `BattleEncodedId_DispatchQueryMode0Value` (00309EC0)).
- **Input — SERVICE (2 edges).** 2 outbound (page-cited `002B7B80`, `002BAF80` call Input bodies `InputGameplay_TestCombinedMaskBit1WithTemporalGate` (00250200), `InputGameplay_TestFilteredMask92Bit0WithTemporalGate` (00250130)).
- **Story_Event_Quest_Hunt — MECHANICAL (4 edges).** 4 outbound (page-cited `003BCDE0`, `003C06E0`, `003C0F70` call Story_Event_Quest_Hunt bodies `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0)) - shared-helper call surface, not a Story_Event_Quest_Hunt relationship of this page's subjects.
