---
system: ".dat and .bin are extension buckets, not formats — the two rows `formats_explained` can never count"
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED
owner_layer: PrimaryOwner:Resource — the archive assigns the extension; the families inside belong to their own loaders
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 7 addresses cited - 6 entry, 1 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "dat: 2,948 archive entries, 21 signature rows; bin: 1,439 entries, 59 signature rows (dat-bin-signature-map.tsv)"
last_reviewed: 2026-09-16
archive_formats:
  - "dat | bucket | 21 signature rows over 2,948 entries: himg 2,721, hdat 101, hchk 54, qstd 9, plus 17 numeric-header rows — _index/candidates/dat-bin-signature-map.tsv. CLOSED 2026-09-20: every unit resolves to a documented consumer-bound family (OPUS-REQ-SWE2-DATA-DAT-SEPARABLE-FROM-BIN). Its five member formats are declared in _index/bucket-members.tsv, 2026-09-29"
  - "bin | bucket | 59 signature rows over 1,439 entries: sloc 436, st2e 407, hctg 54, licd 52, gmap 35, FLAG/CCdd/CHSE and a long tail — _index/candidates/dat-bin-signature-map.tsv. MEMBERS DECLARED 2026-09-29: 53 member formats, every entry assigned, each claimed on its consumer-bound sheet — _index/bucket-members.tsv (OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS)"
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# `.dat` and `.bin` are buckets, and the metric now says so

> **`.dat` and `.bin` are not file formats. They are the absence of one** — the extension an
> author reaches for when the file has no other name. `formats_explained` counts an extension as
> covered when a sheet declares its layout, and no sheet can declare "the layout of `.bin`" —
> 1,439 files, 59 distinct leading signatures, 2.4 GB do not have one layout. These two rows are
> **dispositioned, not explained**, and the scorer now records that explicitly.

This sheet carries the two `bucket` declarations. The unit of `formats_explained` stays the
extension — the denominator is a census of what ships, and a denominator an author can type is not
a denominator. The disposition for these two rows is `bucket`: adjudicated non-format, **counted in
nothing's numerator**, carrying the note that names the families known to live under the extension.
That is the falsifiable part: if the family list is wrong, the claim is wrong.

## The decision chain

1. **OPUS ruling 2026-09-14** (`_index/FORMATS-DECLARATION.md`): the eight undeclared extensions
   were split — six got sheets, `.dat`/`.bin` got "a disposition the metric does not yet have".
2. **SWE2-AUDIT-SPEC ruling** (`OPUS-REQ-AUDITSPEC-FORMATS-BUCKET-DISPOSITION`, commit `ea764c1d`):
   add the fourth disposition **and** publish the ceiling. `bucket` records the adjudication,
   must not count in `formats_explained`, and a later `explained` claim collides into the upgrade
   path. `progress.py` prints the composition.
3. **OPUS contra** (`OPUS-CONTRA-FORMATS-METRIC-UNIT`, P1): decided here — the unit stays the
   extension; the rows carry `bucket`. The alternative (splitting the census into
   extension-signature rows) would let an author re-cut the denominator, which the metric exists
   to forbid.
4. **Implementation** (this package): `check_assets.py` knows `bucket` (NEEDS_NOTE — the contents
   list is the falsifiable part), `evaluate` returns it separately, `progress.py` prints
   `X/48 dispositioned = N explained + M bucketed`, `check_format_row_purity.py` treats bucketed
   rows as dispositioned.

## What is inside the buckets

From `_index/candidates/dat-bin-signature-map.tsv` (the full census, not the 12-file magic
sample; `mentioned_in` is an upper bound — a mention is not an explanation):

### `.dat` — 2,948 entries, 21 signature rows

| signature | entries | share | status |
|---|---:|---:|---|
| `himg` | 2,721 | 92.30% | `himg-handbook-image-bundles.md` — layout landed 2026-09-16 (`OPUS-REQ-SWE2-DATA-HIMG-LAYOUT`) |
| `hdat` | 101 | 3.43% | `himg-handbook-image-bundles.md` §5 — sibling index layout, same widget path |
| `hchk` | 54 | 1.83% | `five-small-bin-tables.md` §12 + `himg-handbook-image-bundles.md` §5 |
| `qstd` | 9 | 0.31% | `five-small-bin-tables.md` §12 — `menuquest.dat` decoded |
| 17 numeric-header rows (`01 00 00 00` … `16 00 00 00`) | 63 | ~2.1% | `font-data-kerning-and-expansion.md` — the `gamedata/d3d11/artdata/font/*.dat` glyph tables |

`.dat` has **zero** signature families no document mentions. Its tail is small; its head —
`himg`, 92.3% of the extension — was the single largest unexplained family in the archive until
2026-09-16, when `himg-handbook-image-bundles.md` laid out the container, the page-window
semantics and the native consumer chain.

#### `.dat` is now a closed bucket — 2026-09-20 (SWE2-DATA, `OPUS-REQ-SWE2-DATA-DAT-SEPARABLE-FROM-BIN`)

**Ruling: `.dat` is separable from `.bin`, and it stays `bucket` for its own reason, not
`.bin`'s.** `.bin` is refused because it is genuinely heterogeneous — 26 magics over 236 logical
units, six token families no document names, an open tail. `.dat` is refused for a different,
narrower reason: **the extension names no single format**, while every shipped unit underneath it
resolves to a documented, consumer-bound family. In the full-census units (`census_bin_signatures.py`,
locale segments removed, 343 logical units, 0 `UNDETERMINED`, 0 locale-verdict disagreements):

| family | units | consumer-bound sheet |
|---|---:|---|
| `himg` | 302–309 (88.0%–90.1% — seven units split `hdat`/`himg` across locales) | `himg-handbook-image-bundles.md` (bound through widget `00575B80`) |
| `hdat` | 17 | same sheet §5 — index layout through the same path |
| `hchk` | 6 | `five-small-bin-tables.md` §12 |
| `qstd` | 1 | `five-small-bin-tables.md` §12 — `menuquest.dat` |
| numeric-header font tables | 17 | `font-data-kerning-and-expansion.md` — **the 63 `gamedata/d3d11` `.dat` entries are exactly these units, inside the 343, not a separate population** (`+0x04` glyph count header, completed by `001B4D70`) |

Every unit is covered; nothing under `.dat` awaits a sheet. What remains untrue is the
*extension-level* claim — five layouts share the extension, so no sheet can declare "the layout
of `.dat`". Whether an exhaustive decomposition like this earns `explained` (a magic-dispatched
union claim rather than a single-layout claim) is a metric-vocabulary change to `check_assets` —
routed to `SWE2-AUDIT-SPEC`, not taken here, for the same reason the bucket disposition itself
was routed: this sheet's owner is the agent the figure scores.

### `.bin` — 1,439 entries, 59 signature rows

| signature | entries | share | status |
|---|---:|---:|---|
| `sloc` | 436 | 30.30% | named in `file-size-tables-fst.md` |
| `st2e` | 407 | 28.28% | `the-encoded-id-class-registry.md` + `St2e-Carriers/` |
| numeric `00 00 00 00` | 73 | 5.07% | NOT-A-TOKEN |
| `hctg` | 54 | 3.75% | `file-size-tables-fst.md` |
| `licd` | 52 | 3.61% | `chse-character-se-tables.md` |
| `gmap`, `FLAG`, `CCdd`, `CHSE`, `NPC0`, `PLMN`, `sign`, `bwin`, `amap`, `cmap`, `lmap`, `wmap`, `GRMI`, `MUS0`, `MENU`, `CLT2`, `VIB0`, `FOOT`, `ashd` | 2–35 each | | all carry a `mentioned_in` row |
| `QST1`, `//22`, `hcom`, `hodr` (9 each), `EVME`, `dP<d` (1 each) | 38 | 2.6% | ~~**no document mentions them at all**~~ (`OPUS-REQ-SWE2-DATA-SIX-UNNAMED-BIN-FAMILIES`) — *all six bound 2026-09-29; `//22` is not a family but a guest-face image's first pixels, and `dP<d` is `summoneffectdata`'s first record — see below* |
| ~25 more numeric/UNDETERMINED rows | ~170 | | NOT-A-TOKEN |

## The member formats, declared — 2026-09-29 (SWE2-DATA, `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS`)

FABLE's MP-1 meaning review (C4) ruled that a bucket is not a requirement — its **member formats**
are. They are now declared, in the tracked **[`_index/bucket-members.tsv`](../../_index/bucket-members.tsv)**,
generated with its checks by
[`gen_bucket_members.py`](../../_index/candidates/bucket-members-0929/gen_bucket_members.py); the
record, the full member table and every member's evidence script are in
[`bucket-members-0929/`](../../_index/candidates/bucket-members-0929/README.md).

- **`.bin`: 53 members over all 1,439 entries (236 units); `.dat`: 5 members over all 2,948 entries.**
  Every entry is assigned to exactly one member (C1), the per-signature totals reproduce the full
  census's 59 + 21 rows (C2), and every member's sheet carries a signature-scoped `explained` row
  naming it (C7) — 58 of 58.
- **The unit of assignment is the layout, not the leading dword.** Seven leading patterns
  (`'CCdd'`, `D1 D1 F4 F4`, `C9 C9 E3 E3`, `E5 E5 E5 E5`, `BA BA A3 A3`, `'//22'` and 72 of the
  `00 00 00 00` entries) are one format, the headerless `bin_menu` images; four signatures are
  shared by unrelated formats (`'FLAG'`: `FLAGDEF1` vs `FLAGROM1`; `00 00 00 00`: images vs
  `behindcamera`; `80 00 00 00`: `mrppack_ys` vs `musicinfo` vs a designer-name table;
  `01 00 00 00`: `skeletonmapping` vs `test_map_ref`), and are written `SIG=N` in the declaration.
- **Three new sheets**, for the members no page covered:
  [`amap`](../PS2-Image-Data-Formats/amap-menumap-area-table.md),
  [`gmap`](../PS2-Image-Data-Formats/gmap-menumap-guide-texts.md),
  [`menuquest00–02`](../PS2-Image-Data-Formats/menuquest-bin-quest-detail-tables.md); new sections
  for `mapjumpgroupflagrom`, `fhmusicdata`, `test_area_ref` / `test_map_ref`, `license_chip`,
  `Item_Clut`, `shop_data` / `wepjob_matrix` and `menu_version`; and one correction
  (`summoneffectdata`'s layout and loader).

The extension rows keep `bucket` (the SWE2-AUDIT-SPEC ruling stands); what closes is the member
enumeration beneath them.

## What this does and does not settle

- **Settled:** the metric is honest. `46 explained + 2 bucketed = 48 dispositioned`; the numerator
  ceiling is 46/48 and no declaration can raise it without a real per-family sheet.
- **Not settled:** `.bin`'s families. `sloc`+`st2e` are 58.6% of `.bin`, six `.bin` token families
  are unmentioned anywhere — that is format work, queued as
  `OPUS-REQ-SWE2-DATA-BIN-MENU-IMAGES` and `OPUS-REQ-SWE2-DATA-SIX-UNNAMED-BIN-FAMILIES`, and when
  each family earns a sheet the bucket note shrinks; the row never graduates to `explained` at
  the extension level. **`.dat`'s side is now settled the same way a bucket can be:** every one
  of its 343 logical units resolves to a documented consumer-bound family (the closed-bucket
  table above, `OPUS-REQ-SWE2-DATA-DAT-SEPARABLE-FROM-BIN`, 2026-09-20) — it stays `bucket`
  because five layouts share the extension, and whether an exhaustive decomposition earns
  `explained` is routed to `SWE2-AUDIT-SPEC` as a metric-vocabulary question.

## SWE2-EC7-109 update (2026-09-20) - `0020B5F0` measured

`0020B5F0` (133 B) is the EASTL
map emplace `001B4D70` calls
(`0019CB20` reaches it too):
head `qword[rcx + 0x18]`,
sentinel `rcx + 8`, keys at
`dword[node + 0x20]` walk the
red-black tree lower-bound for
`dword[rdx]`; on a miss
`001AE9B0(rcx, &where, &key,
&slot)` inserts, and the answer
is `node + 0x28` either way -
the keyed value-slot accessor
the table lookups share.
Interior anchor `0020B610` (the
`dword[r8 + 0x20]` compare loop
head).

Mechanical neighbours introduced by
this section's citations: `0019CB20`
(the other `0020B5F0` caller) carries
a Presentation caller (`0018D850`, 1
edge). That is an edge of the shared
emplacement site, not of the bucket
contract - noted so the audit
accounts for it.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions.*

**Presentation — SERVICE (8 edges).** The two renderer-side bodies the bucket census names call into the render layer. `0018D850` calls `0018D160`, `Renderer_CreateRandomNoiseTexture` (`001946E0`), `0061D9C0` and `0019CB20`. The glyph-table completer `001B4D70` calls the four render helpers `001FC060`, `001FDCC0`, `001FE020` and `001FE080`. The bucket files are data those render bodies consume, and nothing here changes how they draw.
