# `ps2data/image` — the long tail

The PS2 disc-image data root. **Seventeen extensions live here**, most of them small, and this is
where the archive gives the least help: a directory called `image` says nothing about what any
individual format is for.

| ext | files | note |
|---|---:|---|
| `dat` | 2,885 | plus 63 in `gamedata/d3d11` — **possibly not the same format** |
| `bin` | ~~1,437~~ 1,439 *(corrected 2026-10-02, OPUS: the archive index; the census below counts the same 1,439)* | 2,366 MiB (2,481 MB) |
| `tm2` | 447 | ~~**likely TIM2**~~ **TIM2**, the PS2 image format, magic `TIM2` in 447 of 447 *(answered: see [the TIM2 sheet](tim2-images-and-the-seven-slot-registry.md) §8, all 456 files opened; 2026-10-02, OPUS)* — candidate `standard` |
| `mrp` | 116 | |
| `cl2` · `as7` · `btm` | 20 · 18 · 12 | |
| `sav` | 16 | likely 19-Save-Load-Settings, not here |
| `lst` · `nfs` · `dbg` · `msb` · `sbn` | 9 · 9 · 8 · 8 · 8 | |
| `h` · `ico` · `mg` · `sys` | 6 · 2 · 2 · 2 | `h` and `ico` candidate `standard` |

## What the magic census settled — 2026-09-03

**`.bin` is the weak row, not `.dat`.** ~~Twelve sampled `.bin` files gave **seven signatures** —
`sloc`, **`st2e`**, `FLAG`, `gmap`, `CCdd`, `hctg` and a bare dword.~~ It is a bag of unrelated
formats sharing a name, and `st2e` (already documented) is one of them. **One census row cannot
cover it**, so this row is under-weighted; stated rather than re-cut.

~~`.dat` was tamer than feared: **`himg` in 10 of 12**, plus `hdat` and one bare dword.~~

**Both sampled lines are superseded by the full census below, and one of the seven was not a
signature at all.**

## The full census — 2026-09-19 (OPUS), replacing the twelve-file sample

**The ceiling stands and the denominator does not move.** `progress.py` tops `formats_explained`
out because `bin` and `dat` are extensions the game reuses for unrelated containers, and
re-cutting the census would be an author choosing their own denominator. What changes here is the
**evidence**: every `.bin` and `.dat` entry in `FFXII_TZA.vbf` was read rather than twelve of
each, through `census_bin_signatures.py`'s five-valued classifier (`MAGIC`,
`MAGIC_TAG_VERSION`, `EBP_SECTION_BODY`, `NOT_A_MAGIC`, `UNDETERMINED`).

| | `.bin` | `.dat` |
|---|---:|---:|
| archive entries | 1,439 | 2,948 |
| **logical units** after removing locale segments | **236** | **343** |
| distinct magics | **26**, over 178 units | **4**, over 326 units |
| largest single magic | `st2e`, 73 units — **30.9%** | `himg`, 309 units — **90.1%** |
| all magics as a share of units | 75.4% | **95.0%** |
| distinct non-magic leading dwords | 33, over 58 units | 17, over 17 units |
| `UNDETERMINED` | 9 units | 0 |
| units whose locale copies disagree about the verdict | **0** | **0** |

**`.bin`'s 26 magics.** `st2e` 73, `sloc` 52, `licd` 13, `CHSE` 8, `hctg` 6, `gmap` 5, `FLAG` 2,
then `NPC0`, `PLMN`, `QST1`, `GRMI`, `MUS0`, `EVME`, `VIB0`, `FOOT`, `ashd`, `sign`, `MENU`,
`bwin`, `CLT2`, `hcom`, `hodr`, `amap`, `cmap`, `lmap` and `wmap` at one unit each.

**`.dat`'s four.** `himg` 309, `hdat` 17, `hchk` 6, `qstd` 1. **Those sum to 333 over 326
units, and the seven-unit excess is not an error — it is the seven split units below, each
counted under both of its magics.** `.bin`'s 26 sum to 178 exactly, because its one split unit
is split between two non-magics.

### `CCdd` was never a magic, and two separate readings repeated it — 2026-09-19 (OPUS)

The sample's seventh signature is **byte-doubled image data that happens to spell ASCII** — the
classifier carries exactly that case in its self-test and returns `NOT_A_MAGIC`. It is absent
from the 26. **A four-printable-character leading dword is not a magic**, and this is the second
name-driven miss on this page, after `.lst` and `.ico`.

### The finding: `bin` and `dat` are not alike, and the ceiling treats them as one case — 2026-09-19 (OPUS)

**`.bin` really is a junk drawer** — 26 unrelated magics with the largest under a third of its
units. **`.dat` is not** — one magic covers nine units in ten, and four cover 95%, the
stragglers being font tables whose first dword is a small index. **A dimension that refuses
`.dat` because `.bin` is heterogeneous is refusing it for the wrong file's reason.**

**This is raised, not taken.** Whether `.dat` can be dispositioned changes a scored denominator
and belongs to whoever owns this README and the formats dimension, not to the measurement.

### What the file counts would have said, and why unit counts are used instead — 2026-09-19 (OPUS)

`.bin` ships per locale — most units have nine copies — so a **file** count multiplies most
formats by nine: `sloc` is 436 files and **52 units**, `st2e` 407 files and **73**. An earlier
OPUS reading of this census reported *"59 distinct signatures, not seven"*; that counted raw
leading dwords over files, and it is inflated twice over, by the locale duplication and by
counting 33 first-data-words as formats. **The conclusion survives the correction and the
headline number does not.**

### Two caveats on the unit collapse, the second found by not trusting the first — 2026-09-19 (OPUS)

**Collapsing to units is not deduplication.** 90 of `.bin`'s 218 multi-copy units and 220 of
`.dat`'s 342 have locale copies whose bytes **differ**. The census reports **no unit whose
copies disagree about the verdict**, zero for both extensions, and that is what makes a
unit-level count well-defined.

**But verdict agreement is a coarser question than signature agreement, and the finer one has
a different answer.** `hdat` and `himg` are both `MAGIC`, so a unit split between them agrees
on the verdict and disagrees on the format. Recounting by signature: **7 of `.dat`'s 343 units
carry different magics across locales** — `menuhandbook_monster004.dat` through `010`, `hdat`
in some locales and `himg` in others for the same handbook entry — and **1 of `.bin`'s 236**
(`quest/menuquest00.bin`, two different non-ASCII dwords). So the per-magic breakdown is
**ambiguous for those eight units**, and `himg`'s share is a range rather than a point:
**302–309 of 343 units, 88.0%–90.1%**, depending on how the seven are assigned. The
*nine units in ten* reading survives either bound, which is why the asymmetry above is stated
as a conclusion and the count is stated as a range.

| ext | signature | what it is |
|---|---|---|
| `tm2` · `nfs` | `TIM2` | **the same format.** `.nfs` is not a separate thing |
| `lst` | `qstl` | binary calls it `quest\menuquest.lst` — **quest menu data** → [sheet](lst-menuquest-list.md) |
| `mrp` | `MRP\0` | **menu rect/element packages** → [sheet](mrp-menu-resource-packages.md) |
| `cl2` | `CLT2` | binary: `Bin_Menu\Loca_*.cl2` — **location-map colour tables** → [sheet](cl2-menu-colour-tables.md) |
| `as7` | `41 37 ..` (`A7`) | binary: `Bin_Menu\Char_Silhouette.as7` — **big-endian page containers** → [sheet](as7-menu-graphics-containers.md) |
| `btm` | `00 00 00 00` | binary: `ExFont\font_stf_a_normal.btm` — **raw glyph bitmaps, no header** → [sheet](btm-exfont-bitmaps.md) |
| `ico` | `00 00 01 00` | **a real Windows ICO** |
| `sys` | `PS2D` | |
| `mg` | `10 00 00 00` | binary: `WorldMap\meshdata.mg` — **world-map mesh container** → [sheet](mg-worldmap-mesh.md) |

> **Two guesses in this README's first draft were wrong, and are kept here rather than quietly
> fixed.** *"`dbg` and `lst` are build artefacts by name"* — **false**: `.lst` is quest menu data
> the binary names explicitly. *"`.ico` is probably a PS2 icon, not a Windows one"* — **false**: the
> magic is exactly Windows ICO. **A name is a weak instrument and both misses were name-driven.**

`.dbg`, `.msb` and `.sbn` remain genuinely open: no string in the binary, and their sampled leading
dwords look like counts or sizes rather than magics. **Absence of a string proves nothing** — that
was established by `PClusterHeaderBase`, which has eighteen recovered fields and zero name strings.

Write sheets to `_templates/FORMAT.md`. See [_index/ASSET-FORMATS.md](../../_index/ASSET-FORMATS.md).

*2026-09-13:* [the `.bin` families nothing names](unnamed-bin-families.md) — 20 of the 146 `.bin` families (41 files) have no path in the executable; ten are `cn`/`kr` `st2e` battle tables, four are the ATEL control scripts (`UB-1`).

*2026-09-16:* [the `himg` handbook image bundle](himg-handbook-image-bundles.md) — 90% of `.dat` by unit; `{base, count}` window + `u32` TIM2 offset table, natively bound by the Handbook page widget (`00575B80`).

*2026-09-18:* [the loader-bound `.bin` families](loader-bound-bin-families.md) — ~~thirteen~~ fourteen families *(corrected 2026-10-02, OPUS: six pack directories, three kind-9 files and five kind-7 singletons, whose 52 + 4 + 31 files make the 87; fourteen families)* reachable only by kind/subtype request: the six `*pack_ys`/`fontpack_*` sentinel-filled offset directories, the kind-9 ~~named objects~~ files (`behindcamera` and `pc_skillmotion` named objects, `summoneffectdata` read into the fixed `.data` buffer `02AD9B60`, the loader-bound sheet §3), and the `ch`/`in`-only font tables (`fontcolor`, `monotone_chr` — whose loader grafts the `clutpack_ys` palette).
