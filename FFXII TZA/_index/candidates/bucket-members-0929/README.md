# The member formats of the `.bin` and `.dat` buckets (SWE2-DATA, 2026-09-29)

**Request.** `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS` (P1, user-mandated). FABLE's MP-1 meaning review (C4,
[`mp1-meanings-review`](../mp1-meanings-review/README.md)) ruled that a bucketed extension is not an accepted
disposition: its **member formats** are the requirements. This record declares every member of both buckets and binds
each one to a consumer-bound sheet.

**Canonical output: [`_index/bucket-members.tsv`](../../bucket-members.tsv)** (tracked; the path My Progress MP-3
reads). `Database/Tools/work/formats/bucket-members.tsv` is a byte-identical convenience copy for the MP-2 reader that
predates MP-3; it is gitignored and is **not** canonical.

## Files

| file | what |
|---|---|
| [`gen_bucket_members.py`](gen_bucket_members.py) | the generator and its checks C1-C6 (`--check` writes nothing) |
| [`bucket-member-units.tsv`](bucket-member-units.tsv) | every logical unit of both extensions (locale segment folded) -> its member, with the entries (locale copies) per signature |
| [`../../bucket-members.tsv`](../../bucket-members.tsv) | one row per member: `ext, family, signatures, entries, units, sheet` |

Inputs: the per-entry signature censuses `census_bin_signatures.py` writes over `FFXII_TZA.vbf` (`--ext .bin` /
`--ext .dat`; default `Database/Tools/work/formats/{bin,dat}-signature-census.tsv`, regenerable) and the tracked
full-archive census [`bucket-members-input-0929/format-magic-census-full.tsv`](../bucket-members-input-0929/README.md).

## Method: the unit of assignment is the layout, not the leading dword

The census signature is the first four bytes. It is **not** a format identity, in either direction:

* **One format, several signatures.** The eighteen headerless `bin_menu` images (`face_guest07`-`16`, `map_efe00`-`06`,
  `mini_guest_face`) start with pixel bytes, so they carry seven different leading patterns (`'CCdd'`,
  `D1 D1 F4 F4`, `C9 C9 E3 E3`, `E5 E5 E5 E5`, `BA BA A3 A3`, `'//22'`, `00 00 00 00`). OPUS's observation that
  `'//22'` (`face_guest15`) is the guest-face format and not a new family is **confirmed**: it is one of these units,
  and the [bin_menu sheet](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md)
  §2 layout (the file is the pixel buffer) covers all eighteen.
* **One signature, several formats.** `00 00 00 00` is 72 `bin_menu` image entries **and** `behindcamera.bin`;
  `80 00 00 00` is 10 `mrppack_ys` pack directories, 2 `musicinfo.bin` and 2 `growth_rate_growth_rate_name.bin`;
  `01 00 00 00` is `skeletonmapping.bin` and `test_map_ref.bin`; `'FLAG'` is `mapjumpgroupinit.bin` (`FLAGDEF1`) and
  `mapjumpgroupflagrom.bin` (`FLAGROM1`).

So each rule in the generator names **units** (a path pattern, locale folded) and the signatures it expects to take;
C5 fails if a rule takes a signature it did not expect, so a new or moved signature cannot be absorbed silently. The
signature column is derived from what a member actually took, written `SIG=N` where a signature is split between
members. Whether MP-3's coverage check accepts `SIG=N` is `DATA-REQ-OPUS-BUCKET-MEMBERS-SHARED-SIGNATURES` (OPUS).

## Checks (the run that produced the published TSV)

```
$ python gen_bucket_members.py --check
C1 PASS  4387 entries; unmatched 0, matched by two rules 0, signature absent from the full census 0 []
C2 PASS  per-signature entries reproduce the full census: 59 bin + 21 dat rows
C3 PASS  .bin members sum to 1439 entries, census 1439
C3 PASS  .dat members sum to 2948 entries, census 2948
C4 PASS  every named sheet exists; 0 member(s) with no sheet yet: none
C5 PASS  each rule took exactly its expected signatures
C6 PASS  control: an invented unit matches no rule (0 matched)
C7 PASS  each member's sheet carries a signature-scoped explained/standard/external row naming it
  .bin: 53 members, 1439 entries, 236 units
  .dat: 5 members, 2948 entries, 350 units
FAILS 0
```

C7 is the consistency the measurement needs: every member's sheet carries a signature-scoped
`archive_formats:` row (`explained`) naming the member token, which `check_assets.py` now resolves
through this declaration (`member_families`; its self-test refuses an undeclared token).

The member evidence scripts written for this package are in [`checks/`](checks/) (each prints its
checks and `FAILS`; all FAILS 0 on the certified image `73461d08…` and the full extract):
`check_amap.py` 128, `check_gmap.py` 198, `check_menuquest.py` 228, `b1_flagrom.py` 31,
`b2_fhmusicdata.py` 14, `b3_test_refs.py` 30, `b4_license_chip.py` 41, `b5_item_clut.py` 43,
`b6_battle_copies.py` 34, `b7_summoneffect.py` 39, `b8_menu_version.py` 18.

## The members

**58 members: 53 in `.bin` over 1,439 entries / 236 units, 5 in `.dat` over 2,948 entries / 343 units**
(`.dat` lists 350 unit rows because seven handbook units are `hdat` in some locales and `himg` in
others; each entry is assigned by its own signature). Every member is bound to a sheet that
carries its layout and, where one exists, its native requester and reader.

| ext | member | entries | units | leading signatures | sheet |
|---|---|---:|---:|---|---|
| `.dat` | `himg` | 2,721 | 309 | `'himg'` | [himg-handbook-image-bundles](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/himg-handbook-image-bundles.md) |
| `.dat` | `hdat` | 101 | 17 | `'hdat'` | [hchk-hctg-hdat-handbook-indexes](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md) |
| `.dat` | `hchk` | 54 | 6 | `'hchk'` | [hchk-hctg-hdat-handbook-indexes](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md) |
| `.dat` | `qstd` | 9 | 1 | `'qstd'` | [five-small-bin-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) |
| `.dat` | `fontdat` | 63 | 17 | 17 signatures (`01 00 00 00` ... `16 00 00 00`) | [font-data-kerning-and-expansion](../../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md) |
| `.bin` | `sloc` | 436 | 52 | `'sloc'` | [sloc-menumap-container](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/sloc-menumap-container.md) |
| `.bin` | `st2e` | 407 | 73 | `'st2e'` | [vbf-archive-and-st2e-tables](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) |
| `.bin` | `hctg` | 54 | 6 | `'hctg'` | [hchk-hctg-hdat-handbook-indexes](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md) |
| `.bin` | `licd` | 52 | 13 | `'licd'` | [license-board-grid-format](../../../12-Items-Equipment-Shops-License/license-board-grid-format.md) |
| `.bin` | `gmap` | 35 | 5 | `'gmap'` | [gmap-menumap-guide-texts](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/gmap-menumap-guide-texts.md) |
| `.bin` | `flagdef` | 9 | 1 | `'FLAG'=9` | [persistent-flag-banks](../../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md) |
| `.bin` | `flagrom` | 9 | 1 | `'FLAG'=9` | [persistent-flag-banks](../../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md) |
| `.bin` | `binmenuimage` | 162 | 18 | 7 signatures (`00 00 00 00=72` ... `BA BA A3 A3`) | [binmenu-guest-face-and-map-effect-images](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md) |
| `.bin` | `CHSE` | 16 | 8 | `'CHSE'` | [chse-character-se-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/chse-character-se-tables.md) |
| `.bin` | `NPC0` | 9 | 1 | `'NPC0'` | [the-npc-name-dictionary](../../../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md) |
| `.bin` | `PLMN` | 9 | 1 | `'PLMN'` | [field-record-table-navimapdata](../../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) |
| `.bin` | `QST1` | 9 | 1 | `'QST1'` | [five-small-bin-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) |
| `.bin` | `sign` | 9 | 1 | `'sign'` | [five-small-bin-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) |
| `.bin` | `bwin` | 9 | 1 | `'bwin'` | [five-small-bin-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) |
| `.bin` | `MENU` | 2 | 1 | `'MENU'` | [five-small-bin-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) |
| `.bin` | `hcom` | 9 | 1 | `'hcom'` | [the-handbook-screen](../../../16-UI/Handbook/the-handbook-screen.md) |
| `.bin` | `hodr` | 9 | 1 | `'hodr'` | [the-handbook-screen](../../../16-UI/Handbook/the-handbook-screen.md) |
| `.bin` | `menuquest` | 27 | 3 | `38 00 38 00`, `94 03 94 03`, `8C 01 70 02`, `8C 01 74 07` | [menuquest-bin-quest-detail-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/menuquest-bin-quest-detail-tables.md) |
| `.bin` | `amap` | 9 | 1 | `'amap'` | [amap-menumap-area-table](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/amap-menumap-area-table.md) |
| `.bin` | `cmap` | 9 | 1 | `'cmap'` | [cmap-menumap-common-sublocation-directory](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cmap-menumap-common-sublocation-directory.md) |
| `.bin` | `lmap` | 9 | 1 | `'lmap'` | [lmap-menumap-location-graph](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md) |
| `.bin` | `wmap` | 9 | 1 | `'wmap'` | [wmap-menumap-world-map-graph](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/wmap-menumap-world-map-graph.md) |
| `.bin` | `battlepack` | 9 | 1 | `47 00 00 00` | [vbf-archive-and-st2e-tables](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) |
| `.bin` | `wordbanks` | 9 | 1 | `0F 00 00 00` | [battle-text-banks](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) |
| `.bin` | `commandpack` | 4 | 1 | `3A 03 00 00` | [vbf-archive-and-st2e-tables](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) |
| `.bin` | `shopdata` | 4 | 1 | `64 00 00 00` | [vbf-archive-and-st2e-tables](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) |
| `.bin` | `wepjobmatrix` | 4 | 1 | `01 00 17 00` | [vbf-archive-and-st2e-tables](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) |
| `.bin` | `scriptimage` | 8 | 4 | `0B 00 00 80` | [section-000-bytecode](../../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md) |
| `.bin` | `NAV` | 3 | 1 | `4E 41 56 02` | [field-record-table-navimapdata](../../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) |
| `.bin` | `skeletonmapping` | 1 | 1 | `01 00 00 00=1` | [add-motion-skeleton-and-high-model-tables](../../../17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md) |
| `.bin` | `highmodelreplace` | 1 | 1 | `00 00 63 00` | [add-motion-skeleton-and-high-model-tables](../../../17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md) |
| `.bin` | `testmapref` | 1 | 1 | `01 00 00 00=1` | [choosing-the-field-environment-variant](../../../03-World-Area-Field/choosing-the-field-environment-variant.md) |
| `.bin` | `testarearef` | 2 | 1 | `00 00 01 00` | [choosing-the-field-environment-variant](../../../03-World-Area-Field/choosing-the-field-environment-variant.md) |
| `.bin` | `MRF` | 2 | 1 | `4D 52 46 02` | [choosing-the-field-environment-variant](../../../03-World-Area-Field/choosing-the-field-environment-variant.md) |
| `.bin` | `filelistlocalin` | 2 | 1 | `98 00 00 00` | [unnamed-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md) |
| `.bin` | `GRMI` | 2 | 1 | `'GRMI'` | [mweather-resource-format](../../../03-World-Area-Field/Weather/mweather-resource-format.md) |
| `.bin` | `MUS0` | 2 | 1 | `'MUS0'` | [the-music-control-file-and-the-bgm-stream](../../../18-Audio/the-music-control-file-and-the-bgm-stream.md) |
| `.bin` | `musicinfo` | 2 | 1 | `80 00 00 00=2` | [how-the-music-changes-when-you-change-area](../../../18-Audio/how-the-music-changes-when-you-change-area.md) |
| `.bin` | `pcskillmotion` | 2 | 1 | `21 00 00 00` | [loader-bound-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md) |
| `.bin` | `fontcolor` | 2 | 1 | `07 01 00 00` | [loader-bound-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md) |
| `.bin` | `itemclut` | 2 | 1 | `00 00 00 80` | [binmenu-guest-face-and-map-effect-images](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md) |
| `.bin` | `licensechip` | 2 | 1 | `01 00 02 00` | [license-board-grid-format](../../../12-Items-Equipment-Shops-License/license-board-grid-format.md) |
| `.bin` | `monotonechr` | 2 | 1 | `'CLT2'` | [loader-bound-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md) |
| `.bin` | `st2enames` | 4 | 2 | `41 05 00 00`, `80 00 00 00=2` | [unnamed-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md) |
| `.bin` | `logicpack` | 2 | 1 | `1E 05 00 00` | [unnamed-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md) |
| `.bin` | `ashd` | 1 | 1 | `'ashd'` | [unnamed-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md) |
| `.bin` | `EVME` | 1 | 1 | `'EVME'` | [event-memory-at-actor-bind](../../../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md) |
| `.bin` | `VIB0` | 1 | 1 | `'VIB0'` | [five-small-bin-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) |
| `.bin` | `fhmusicdata` | 1 | 1 | `1B 00 00 00` | [the-music-control-file-and-the-bgm-stream](../../../18-Audio/the-music-control-file-and-the-bgm-stream.md) |
| `.bin` | `FOOT` | 1 | 1 | `'FOOT'` | [five-small-bin-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) |
| `.bin` | `summoneffectdata` | 1 | 1 | `'dP<d'` | [five-small-bin-tables](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) |
| `.bin` | `behindcamera` | 1 | 1 | `00 00 00 00=1` | [loader-bound-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md) |
| `.bin` | `packdirectory` | 52 | 10 | `40 00 00 00`, `80 00 00 00=10` | [loader-bound-bin-families](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md) |

**What the enumeration found that was not on any page before (2026-09-29):**
- **New sheets** for the three members with none: [`amap`](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/amap-menumap-area-table.md)
  (loader `00253780`, four accessors), [`gmap`](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/gmap-menumap-guide-texts.md)
  (only `guide00` is ever requested; a latent four-byte over-read on the Latin-alphabet copies) and
  [`menuquest00-02`](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/menuquest-bin-quest-detail-tables.md)
  (one table per quest group, not image data).
- **New sections**: `mapjumpgroupflagrom.bin` is the threshold-schedule table read by
  `00377970` (persistent-flag-banks §2) and a different layout from `FLAGDEF1`; `license_chip.bin`
  (license-board page §6b); `Item_Clut.bin` (bin_menu page §5b, correcting "RGBA5551" to 32-bit
  RGBA); `fhmusicdata.bin` (music-control page, no requester); `test_area_ref.bin` (loaded, never
  read) and `test_map_ref.bin` (no requester) on the field-environment page; `shop_data.bin` and
  `wepjob_matrix.bin` are byte copies of `battle_pack.bin` entries 39 and 0 (vbf page, AY-12 paragraph).
- **A correction**: `summoneffectdata.bin` is 64 ten-byte `{scaleA[3], scaleB[3], colour[4]}`
  records and a 32-byte tail, read straight into `.data` `02AD9B60`; `dP<d` is record 0's data. The
  five-small page's "packed parameter stream, no consumer" and the loader-bound page's "17 float
  records" and "named object" are struck; `b7_summoneffect.py` rejects both old readings.
- **`menu_version.bin`** (16-byte ASCII) has no requester and nothing compares a menu version.

## What is not claimed

- **The measurement is not closed by this record alone.** My Progress MP-3 (`requirements.py`,
  OPUS, `9801f618b`) requires every census signature in exactly one member. Four census signatures
  are shared by separately consumer-bound formats (`'FLAG'`, `00 00 00 00`, `80 00 00 00`,
  `01 00 00 00`), so the committed check reports 22 problems on this file; the exact-coverage
  variant that accepts `SIG=N` passes it (`DATA-REQ-OPUS-BUCKET-MEMBERS-SHARED-SIGNATURES`,
  proposal and its tests in `Database/Tools/work/SWE2-DATA/bucket/mp3_sigN_proposal.py`). DATA does
  not merge unrelated formats to satisfy the one-member rule.
- **"No requester found"** (`fhmusicdata`, `test_map_ref`, `menu_version`, the standalone `shop_data` /
  `wepjob_matrix`) is a whole-image static result with positive controls for constant pairs,
  loop-formed ids and stored pairs; a kind/id computed at run time at one of the 89 register-held
  request sites is outside it.
- Member-level `explained` is the layout plus its consumer, or the layout plus the stated absence of
  one; per-table *record* semantics inside `st2e`, `battle_pack` and the pack directories are the
  authored-data registry's (R family), not this record's.
- The extension rows stay `bucket` (the SWE2-AUDIT-SPEC ruling); nothing here changes `formats_explained`.

## Consumer check for the corrections in this publish (EVIDENCE-POLICY 4a)

affected: 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md, _index/OPEN-QUESTIONS.md

| corrected claim | consumer | state |
|---|---|---|
| `summoneffectdata.bin` is a "packed parameter stream" with "no consumer read" | five-small-bin-tables.md §14 | revised-here (struck; the 64 x 10-byte record grid and its readers added) |
| `summoneffectdata.bin` is "17 float records" in a named object with a bind callback | loader-bound-bin-families.md §3 row and §3 lead sentence | revised-here (struck and corrected) |
| `Item_Clut.bin` is "seven 256-entry RGBA5551 banks" | binmenu-guest-face-and-map-effect-images.md §5 | revised-here (32-bit RGBA; §5b) |
| UQ-206: "the element is released (`002F3890`)" | OPEN-QUESTIONS.md UQ-206 row | revised-here (OPUS CON-179 wording; the dispatch page already carries it) |

No other consumer states either old reading: a corpus grep for "17 float records", "packed parameter stream" and
"RGBA5551" beside `Item_Clut` finds only these pages.

Regressions, each rejecting the old reading:
- `checks/b7_summoneffect.py` requires the ten-byte grid, the 0.01-scaled readers and the null-callback `.data`
  destination: run at 5bb5756ebf, 39 checks, FAILS 0.
- `checks/b5_item_clut.py` requires 7 x 256 x 4 bytes (a 2-byte RGBA5551 entry cannot fill the file): run at 5bb5756ebf,
  43 checks, FAILS 0.
- `falsify_effect_element.py` E11 / E15 (OPUS) for UQ-206: run at 5bb5756ebf, FAILS 0.

