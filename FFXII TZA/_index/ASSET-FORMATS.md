# Shipped file formats — the census, the owners, and the order to do them in

**Written 2026-09-03.** The population is generated, not typed: `census_archive_formats.py` reads
the archive index and writes `Tools/work/formats/archive-extension-census.tsv`. **Re-run it; never
edit it by hand.** Scored by `check_assets.py` into `progress.py`'s `formats_explained`.

---

## 1. Why this dimension exists

**The database reads engines well and the files they eat barely at all.**

Audio has eleven documents and 2,064 owned functions. `.sab` — 4,609 sound banks, 838 MB — had one
passing mention in the whole database, and `.snd` (2,304 files) had one more. Nothing was wrong
with the audio documents; the gap was invisible to every metric in place.

> **`engine_explained` is structurally blind to this.** It counts functions cited, and a format
> nobody documents costs no functions. A database could reach 100 % of the binary and still not
> tell you what a single shipped file contains.

That is the whole argument for a separate dimension, and it is the same argument that produced
`registry_explained` and `ebp_explained`: **a thing that is not counted does not get done.**

## 2. Why it is allowed to be scored

`container_format:` was deliberately **counted and not scored**, for a reason written into the
template: *"no censused universe of container formats exists, so a percentage would be invented."*

**That reason is now gone for archive formats.** `FFXII_TZA.vbf` indexes every file the game
ships, so the population is a `GROUP BY` over **89,414 entries → 48 extensions**. Not a plan, not a
wish list, and not something an author can shrink to flatter the ratio.

**The boring rows stay in.** `.ico` (2 files), `.tga` (2), `.h` (6) are in the denominator with
`.phyre` (35,984). Trimming a census down to the interesting rows is an author choosing what they
will be graded against — the exact defect `check_ebp.py` exists to prevent. They are cleared by
**disposition**, not by exclusion.

**`container_format:` is unchanged and still not scored**, and that is not an inconsistency: the
save image, the VBF container itself and `GameSetting.ini` are not archive entries, so they still
have no census. The reason was removed for archive formats only. See §6.

## 3. The three dispositions

Deliberately the same shape as the A/B/C policy [COMPLETION-PLAN.md](COMPLETION-PLAN.md) §3 sets for
`engine_explained`, because it answers the same objection: **volume of citation is not explanation.**

| disposition | what it means | bar |
|---|---|---|
| **`explained`** | a format sheet with the loader contract | `_templates/FORMAT.md`, §3 filled in |
| **`standard`** | an open public format the game did not author | **name the standard** |
| **`external`** | documented outside this database, cross-linked rather than re-derived | **name the reference** |

Declared in frontmatter, never scraped:

```yaml
archive_formats:
  - "sab"
  - "webm | standard | WebM/Matroska container, VP8 video"
  - "phyre | external | ffxii-tza-tools docs/formats/phyre.md"
```

> **`standard` and `external` are refused without a note, and a refused entry does not count.**
> That is the entire anti-gaming mechanism. The cheap disposition is the one that forces you to
> write down a falsifiable claim somebody else can check — and *"the game uses WebM"* invites the
> immediate question of which codecs it actually accepts and what it does with one it does not.

**`standard` is not a free pass.** A game that ships a public format still decides what it rejects,
what it clamps and what it ignores, and **that half is what this database is for**. A `standard`
row with nothing else is honest bookkeeping; a `standard` row that also states where the loader
departs from the spec is the deliverable.

## 4. The population, with proposed owners

**Counts and directories are evidence** — straight from the archive index. **Owners are proposals**
and are marked as such, because a file's location is a strong signal of its subsystem and not a
proof of one. Nothing in this column may be cited as established until a sheet establishes it.

The archive has four trees, and the split is itself informative: **`ps2data/` is the original game
data carried forward, `gamedata/d3d11/` is what this remaster added.**

### `ps2data/sound` → 18-Audio

| ext | files | size | note |
|---|---:|---:|---|
| `sab` | 4,609 | 838 MB | the largest undocumented format by file count |
| `seb` | 248 | 0.5 MB | |
| `mab` | 116 | 1,312 MB | **11 MB per file** — streams, not banks |
| `spp` | 1 | 3 KB | |
| `config` | 1 | 1 KB | |

### `ps2data/plan_master` → mixed; the biggest tree after `d3d11`

| ext | files | size | proposed owner |
|---|---:|---:|---|
| `ebp` | 10,045 | 549 MB | **25-EBP-Script-Container** — already scoped, 14 units |
| `mot` | 4,392 | 2,552 MB | motion / animation |
| `snd` | 2,304 | 146 MB | 18-Audio |
| `vpc` | 1,809 | 1,240 MB | 18-Audio — voice, paired with `vpcjp` |
| `vpcjp` | 1,809 | 1,298 MB | 18-Audio — the Japanese half of the same pair |
| `mpk` | 550 | 1,660 MB | **unknown** — 3 MB average, third-largest format on disk |
| `ard` | 332 | 3 MB | **unknown** |
| `nmb` | 332 | 18 KB | **unknown** — 56 bytes per file; an index or a name list |

> **`vpc`/`vpcjp` at exactly 1,809 files each is a strict pair**, the same shape as EBP's
> `008`/`009`. A pair that never appears alone is a finding before anyone opens one.

### `ps2data/obj_finish` → models

| ext | files | size |
|---|---:|---:|
| `ca` | 3,164 | 632 MB |
| `cm` | 1,066 | 147 MB |

### `ps2data/effect_finish`, `ps2data/efb` → 17-Presentation

| ext | files | size |
|---|---:|---:|
| `efx` | 3,288 | 4,368 MB |
| `efb` | 410 | 216 MB |

### `ps2data/image` → 02-Resource-And-Asset-Pipeline

The PS2 disc-image data root, and the long tail lives here.

| ext | files | size | note |
|---|---:|---:|---|
| `dat` | 2,885 | — | plus 63 in `gamedata/d3d11` |
| `bin` | 1,437 | 2,366 MB | |
| `tm2` | 447 | 304 MB | **likely TIM2**, the PS2 image format — candidate `standard` |
| `mrp` | 116 | 209 KB | |
| `cl2` · `as7` · `btm` | 20 · 18 · 12 | | |
| `sav` | 16 | | likely 19-Save-Load-Settings |
| `lst` · `nfs` · `dbg` · `msb` · `sbn` | 9 · 9 · 8 · 8 · 8 | | |
| `h` · `ico` · `mg` · `sys` | 6 · 2 · 2 · 2 | | `h`/`ico` candidate `standard` |

### `gamedata/d3d11` → the remaster's own assets

| ext | files | size | proposed owner |
|---|---:|---:|---|
| `phyre` | 35,984 | 25,896 MB | 22-Middleware — **`external`**, see §5 |
| `ah` | 2,564 | 11.7 MB | **unknown** — 4.7 KB average, so a header or table, not an asset |
| `webm` | 40 | 10,377 MB | movies — candidate `standard` |
| `ta` | 45 | 46 KB | **unknown** |
| `ker` | 34 | 470 KB | **unknown** |
| `fex` | 14 | 692 KB | **unknown** |

### Elsewhere

| ext | files | tree | proposed owner |
|---|---:|---|---|
| `txt` | 10,253 | `prefetchdata/<lang>` | 02 — prefetch lists, ~1,040 per language |
| `json` | 830 | `jsondata/{maps,cutscenes,fontcluts}` | 03-World / 14-Story / 16-UI |
| `mh` | 43 | `ps2data/movie_finish` | movies |
| `adm` | 39 | `ps2data/add_motion` | motion |
| `csv` | 17 | `ps2data/soft_particle`, `jsondata`, `prefetchdata` | candidate `standard` |
| `tga` | 2 | `gamedata/titleimage` | candidate `standard` |
| `cnf` | 1 | `ps2data/cdi` | PS2 `SYSTEM.CNF` |
| `(none)` | 2 | `ps2data/` | extensionless entries |

## 4b. What the bytes say — the magic census

**Added 2026-09-03, and it changed several rows above.** §4's owners came from file location. Two
stronger instruments now exist, both offline:

- **`census_format_magics.py`** samples real archive entries — decompressing only the first block —
  and groups each extension by its leading signature. `Tools/work/formats/format-magic-census.tsv`.
- **`ext_string_probe.py`** asks whether `FFXII_TZA.exe` names the extension, and prints the
  surrounding string. **42 of 47 extensions are named**, many as full path templates.

### One extension is not one format, and the error runs both ways

**32 of 48 extensions show exactly one signature.** Those census rows are sound, and we now know
what they are:

| sig | ext | | sig | ext |
|---|---|---|---|---|
| `RYHP` | `phyre` | | `EBP2` | `ebp` |
| `sabf` | `sab` | | `mabf` | `mab` |
| `EFX0` | `efx` | | `EFB0` | `efb` |
| `SeBl` | `seb` | | `SPP1` | `spp` |
| `FF12` | `ard` | | `CLT2` | `cl2` |
| `qstl` | `lst` | | `MRP\0` | `mrp` |
| `.mhe` | `mh` | | `scnf` | `config` |
| `BOOT` | `cnf` | | `1A 45 DF A3` | `webm` — **EBML confirmed** |

**Four groups are one format wearing several extensions**, and `check_assets.py` now enforces the
consequence: a sheet explaining the layout must declare every row in its group.

| signature | extensions | files |
|---|---|---:|
| **`PKFL`** | `mot` · `snd` · `vpc` · `vpcjp` | **10,314** |
| `@FRP` | `ca` · `cm` | 4,230 |
| `TIM2` | `tm2` · `nfs` | 456 |
| `/Gam` | `ah` · `ta` | 2,609 — **plain text**, beginning with a path |

> **`PKFL` is the finding of the sweep.** 10,314 files across what §4 filed as *motion* and *audio*
> are a **single container format**, so `.mot` is almost certainly not a motion format at all — it
> is a package that happens to hold motion. Splitting them across two owning categories, as §4 does,
> is now the thing to justify rather than assume.

**And `.bin` runs the other way: seven signatures in twelve samples** — `sloc`, **`st2e`**, `FLAG`,
`gmap`, `CCdd`, `hctg` and a bare dword. It is a bag of unrelated formats sharing a name, and
`st2e` — already documented — is one of them. **One census row cannot be "explained"**; that row is
under-weighted and it is recorded here rather than quietly re-cut.

> **⚠ "Seven" was a floor from a 12-file sample. The full census, 2026-09-04 by `repos-c7`, found
> 28 signatures over 236 logical units** — all 1,439 entries read, with the file count over-counting
> roughly **6:1 by locale duplication**. Frozen at `Tools/work/formats/bin-signature-census.tsv`.
> **So `.bin` is not a bag of seven formats; it is a bag of twenty-eight**, and the single census
> row is under-weighted by far more than this paragraph assumed.
>
> **How the 28 is composed, recounted from the frozen file 2026-09-13 (OPUS), because "28
> signatures" does not reproduce on its own:** the census holds **26 distinct `MAGIC`
> signatures** over the 236 units — `st2e` 73, `sloc` 52, `licd` 13, `CHSE` 8, `hctg` 6, `gmap` 5,
> `FLAG` 2, and nineteen that appear in exactly one unit each — **plus two further verdict
> classes**, `EBP_SECTION_BODY` and `MAGIC_TAG_VERSION`. 26 + 2 = 28. Stated because a bare
> "28 signatures" invites a reader to look for 28 magics and find 26.
>
> **And 258 of the 1,439 entries have NO magic at all** (`NOT_A_MAGIC`), with 39 `UNDETERMINED`.
> So `.bin` is not merely a bag of formats, it is a bag of formats *and* headerless data, and an
> extension-keyed row could not be "explained" even in principle without naming what those are. Four of the units are bare EBP
> `section_000` bodies shipped under a `.bin` name. `.ker` (6), `.fex` (3), `.nmb` (5) and
`.csv` (5) split too, though a split is equally the shape of a **version field in the first
four bytes**, and neither script will call that either way.

> **`.dat` (3) CORRECTED TO 4 — 2026-09-13 (OPUS), and the correction was overdue in this very
> paragraph.** Its full census gives **four** magics over 343 logical units, and §*`dat` is
> nearly one format* below has carried that table for some time: `himg` 309, `hdat` 17,
> `hchk` 6, `qstd` 1, plus 17 non-magic. The `(3)` was a floor from the same 12-file sample
> that produced the `.bin` "seven".
>
> **I corrected the `.bin` figure in this paragraph earlier today and left the `.dat` one two
> lines below it.** Going in to fix a known stale number is exactly when the neighbouring stale
> numbers are least likely to be read, because the eye is hunting for one thing.

### Corrections this forced

**Four guesses in the first draft of this index and its folder READMEs were wrong.** Recorded rather
than silently fixed:

| claim | verdict |
|---|---|
| *"`dbg` and `lst` are build artefacts by name"* | **False.** `.lst` is `qstl` and the binary calls it `quest\menuquest.lst` — **quest menu data**, not debris. |
| *"`.ico` — candidate `standard`, but probably a PS2 icon"* | **It is a real Windows ICO** — `00 00 01 00`. The second guess was the wrong one. |
| *"`ah`, `ta`, `ker`, `fex` are Phyre neighbours"* | **No.** `ah`/`ta` are plain text asset lists; the binary shows `fontlist.ah` and `map/%s_srm.ah`. `.ker` and `.fex` sit consecutively at `008F81F4`/`008F81FC`/`008F8204`, immediately after `fontlist.ah` and `_shadow.dds.phyre` — **font-system files**, so they belong with 16-UI text rendering. |
| *"`nfs` unknown"* | It is **`TIM2`** — the same image format as `.tm2`. |
| *"It is a real Windows ICO"* (the row above, 2026-09-03) | **Overturned 2026-09-11.** The four bytes match, the next sixteen do not: read as an ICO the entry is 1 × 256 px, 6 planes, 0 bpp, **1,065,353,216 bytes at offset 36 of a 33,688-byte file**. Read as a **PS2 memory-card icon** (`u32 0x00010000`, 1 shape, texture type 6, `1.0f`, 36 vertices) the parts sum to the file exactly. The first guess was right after all; [`shipped-standard-formats.md`](../02-Resource-And-Asset-Pipeline/Standard-Formats/shipped-standard-formats.md) §2.6 dispositions it with `icon.sys` — and `tga`, `csv`, `json`, `h`, `cnf`, `webm`. |

### Two findings the string probe handed over free

**The PC build loads `.win.`-infixed variants**: `.win.sab` (`00908998`), `.win.mab` (`00908930`),
`.win.config` (`00906A38`), with real paths like
`PS2Data\sound\shout\us\shout00\shout00.win.sab`. **The remaster substitutes Windows audio assets by
filename convention** — a loader-contract fact, and the sort of thing a file corpus alone never
reveals.

**`/Tools/AutoTest/MapIndex.json` and `JsonData/0.json` ship in the retail binary.** An automated
test harness's index survives in the shipping executable.

> **Presence is evidence; absence is not.** `.efb`, `.sav`, `.dbg`, `.msb` and `.sbn` produce no
> string, and that means nothing — `PClusterHeaderBase` has eighteen recovered fields and zero name
> strings. A miss is never *"the engine does not load this"*. `.h`'s 36 "hits" are 17 `.text` code
> bytes like `D$.H`; the probe flags that column so a noisy extension cannot pass as well-attested.

## 4bb. `st2e` has carriers, and two of them were filed as unknown — corrected 2026-09-03

**Prompted by community modding knowledge, then verified against the archive.** Two rows this index
called unknown or unhelpful turn out to carry the authored-table format the database **already
documents**.

| carrier | files | magic | verified |
|---|---:|---|---|
| **`.ard`** | 332 | **`FF12AR03`** | **40 of 40 sampled contain `st2e` tables** |
| **`battle_pack.bin`** | 1 per language | 71-slot offset table | **37 `st2e` tables inside one file** |

**`.ard` sits at `ps2data/plan_master/in/plan_map/<area>/area/<area>.ard`** — one per *area*
(`ztc_d`, `wdl_b`, …), and the modding community reads it as per-area **enemy status and
attributes**. §4 filed it as *unknown*; it is a `FF12AR03` container of `st2e` tables.

**`battle_pack.bin` sits at `ps2data/image/ff12/test_battle/<lang>/binaryfile/`** and is a
**71-entry offset table, ascending, payload from `0x128`** — structurally the same shape as the EBP2
container. The community reads its section 13 as **all weapon statistics**. It was invisible here
because it lives inside `.bin`, the seven-signature bag of §4b.

> **The finding neither side had on its own.** The community knows *which file holds what*; this
> database knows *what the format is and who reads it*. Joining them: **`st2e` is the authored-table
> format and these are two of its carriers** — so the engine ships one table format in several
> wrappers, and the [63-slot registry](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
> is where those tables end up at run time. **Authored side and runtime side are the same data at
> two ends**, which is why `registry_explained` and the format work converge.

**Two corrections to the community description**, both minor and both checked: the path is
`ff12/test_battle/<lang>/`, not `ff12/us/test_battle/us/`; and `.ard` is one per **area** (332),
not one per map — `plan_map` holds 769 map directories.

**Not yet established:** that `.ard` *is* enemy data, and that `battle_pack.bin` section 13 *is*
weapon stats. Both are community readings, **tier 9 at best until a reader in the binary is named**.
The `st2e` content is verified; what the tables mean is not.

## 4e. The two rows that cannot be closed by one sheet, split - 2026-09-13 (`OPUS-BIN-DAT-SPLIT`)

`bin` (1,439 files) and `dat` (2,948 files) are **4,387 of the archive's entries in two rows**, and
§4b already established that neither can be closed by one sheet. This section measures the split so
that a worklist exists instead of an objection.

### Both collapse, and by a lot

| extension | files | **logical units** | distinct groups |
|---|---:|---:|---:|
| `bin` | 1,439 | **236** | 31 |
| `dat` | 2,948 | **343** | 4 magics + 17 non-magic |

The collapse is the nine shipped languages: 318 of `dat`'s 343 units ship **nine** copies each.
**A file count over this archive triple-counts at best**, which the `.ard` census found first and
the README already records.

### THE `pack` FAMILY LEADS WITH A CAPACITY, NOT A COUNT — provable from four bytes

The census captures only the first **four bytes** of each unit, which looked like too little to say
anything about a directory format. It is enough to refute one.

| file | size | leading dword |
|---|---:|---:|
| `clutpack_ys.bin` | 6,464 | **64** |
| `fontpack_fs.bin` | 28,288 | **64** |
| `texpack_ys.bin` | 32,224 | **64** |
| `tex2pack_ys.bin` | 313,232 | **64** |
| `fontpack_it.bin` | 556,812 | **64** |
| `texpack_ys.bin` | 1,459,008 | **64** |
| `tex2pack_ys.bin` | 4,885,200 | **64** |
| `mrppack_ys.bin` | 51,056 / 104,384 | **128** |

> **The same leading value across a 755-fold size range is not a count of contents.** A 6 KB file and
> a 4.9 MB file do not hold the same number of things. **64 is a FIXED SLOT COUNT** — the directory
> has a constant capacity and the payloads vary — and `mrppack` uses 128 for the same reason.

That also explains why the fixed-stride test failed for this class: a constant-capacity directory of
variable-length payloads divides evenly only by accident.

**And it separates the family from its neighbours.** `commandpack` leads with 826 and `logicpack`
with 1,310 — values that track content and do not repeat across files. So "count-prefixed" is two
different things: the `*pack_<locale>` files with a fixed capacity, and a handful of genuinely
count-led files that happen to share the census's `small integer` verdict.

> **WHAT FOUR BYTES CANNOT DO.** Whether the 64 slots hold offsets, sizes, or offset/size pairs is
> NOT established, and cannot be from this census — it records four bytes per unit and the table
> begins at the fifth. Reading one requires pulling the file out of the VBF. **The claim here is that
> the leading dword is a capacity and not a count**, which is exactly as much as the evidence
> carries.

### THE COUNT-PREFIXED CLASS — 24, not 14, and they are containers rather than record arrays

Two corrections to the table above, both of them mine and both found by testing the claim instead of
restating it.

**First, the count is 24 and not 14.** The 14 was the three most common leading dwords — 64, 128 and
1 — and the census's `small integer` reason class holds 24 units.

**Second, `{u32 count, entries…}` was a guess and the arithmetic refutes it.** If these were arrays
of fixed-size records, then `(size − header) / count` would be a whole number for some small header.
Tested at headers of 4, 8, 16 and 32 bytes across all 24: **most have no exact fit at any of them**,
and the few that do are `count == 1` files, where every header divides trivially.

What the names say instead: `clutpack_ys`, `fontpack_fs`, `fontpack_it`, `texpack_ys`, `tex2pack_ys`,
`mrppack_ys`, `commandpack`, `logicpack`, `battle_pack`, `filelistlocalin`. **These are indexed
containers** — a count followed by an offset table and variable-length payloads, which is exactly why
a fixed stride never divides.

| | units |
|---|---:|
| already named by some page | **11** |
| named by none | 13 (nine distinct files; the `_ys` pairs are locale duplicates) |

> **"No magic" means no 4CC, not no knowledge.** `battle_pack.bin` is in this class and the store
> decodes its banks and tables in detail. Counting these among 58 "headerless" units and reading that
> as 58 gaps overstates the remainder — for this class it is roughly half.

The nine still unnamed are `clutpack_ys`, `fontcolor`, `fontpack_fs`, `fontpack_it`, `mrppack_ys`,
`pc_skillmotion`, `shop_data`, `tex2pack_ys`, `texpack_ys` — and `mrppack` is plausibly covered by
the MRP work already in flight, so it should be checked against that before anyone starts it.

### THE EIGHTEEN BYTE-DOUBLED UNITS ARE MENU IMAGES — three sizes, one directory

The largest unnamed shape in `.bin` resolves without decoding a byte of it. **All eighteen live in
`bin_menu`**, and they are three families:

| files | each | halved | what that is |
|---|---:|---:|---|
| `face_guest07`–`16` (10) | 12,288 | **6,144** | 64 x 96 at one byte per pixel |
| `map_efe00`–`06` (7) | 16,384 | **8,192** | 64 x 128 |
| `mini_guest_face` (1) | 73,728 | 36,864 | **exactly 6 x 6,144** — an atlas of six faces |

**The `6 x` relation is the load-bearing one.** `mini_guest_face` is not merely large; it is six
times one `face_guest` file to the byte. A size that is an exact multiple of a sibling's is a much
stronger signal than a size that merely factors nicely, because it survives being wrong about the
pixel dimensions.

And the doubling is what the census recorded all along: *"every byte doubled over the first 32"*. The
leading dwords make it visible — `d1d1f4f4`, `c9c9e3e3`, `e5e5e5e5`, `43436464`. **Each source byte
appears twice**, so the payload is half the file and the halved sizes above are the real ones.

> **RESOLVED 2026-09-16** — the family is now decoded:
> [`binmenu-guest-face-and-map-effect-images.md`](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md).
> The doubling is a **2x2 nearest-neighbour upscale**, not channel duplication — and it is real only
> in `face_guestNN` (stored 128x96, logical **64x48**, i.e. the payload is a *quarter* of the file,
> not half). `map_efeNN` (128x128, two stacked field-effect icon cells) and `mini_guest_face`
> (six 128x96 pages of four 64x48 mini portraits — 24 cells, not "six faces") carry no doubling;
> their byte-pair correlation is smooth-icon content. Byte meaning: one single-channel 8-bit value
> per stored pixel, no header and no CLUT; palette ownership is the remaining open point (§5 there).
>
> ~~WHAT THIS IS NOT: a decoded format.~~ *(superseded — the paragraph above)* The original note
> follows for provenance: no page had read a pixel, the palette was not located, and whether the
> doubling was a horizontal upscale or a channel duplication was not established — those two produce
> identical byte patterns and identical sizes. The claim then was the FAMILY and the arithmetic.

### THE MAGIC-LESS HALF IS NOT ONE SHAPE — it is four, and the census already knew

The row above says the headerless units are what makes `.bin` hard. **They are 58 logical units, and
they are not 58 unknowns.** Grouping them by their leading dword and by the census's **own `reason`
column** — which has recorded why each was not called a magic since the day it was generated:

| shape | units | what the census says |
|---|---:|---|
| **byte-doubled** | **18** | *"every byte doubled over the first 32"* — `d1d1f4f4`, `c9c9e3e3`, `e5e5e5e5`. A widening, not a container |
| **count-prefixed** | **24** | *"leading dword is a small integer"* — see below; the `{u32 count, entries…}` reading is WRONG |
| leading zeros | 9 | `00000000` |
| **EBP section bodies** | **4** | *"`0x8000000B` section marker and `+0x04` == whole file"* — §5 already names these |
| everything else | 13 | mixed, including two `CCdd` |

> **Three of the four shapes are recognisable enough to name, and one is already named.** "258
> headerless entries" is true of the ENTRY count and invites the reading that the remainder is
> formless. At the logical-unit level it is 18 of one thing, 14 of another, 4 of a thing this
> document already identifies, and a tail.

**The part worth keeping is where the answer was.** Every one of those groupings came out of the
`reason` column of a file generated on 2026-09-04. Nothing needed to be decoded, disassembled or
re-censused — the instrument recorded WHY it declined each unit, and the summaries built on it
carried the count and dropped the reason. **A generated file's explanatory column is evidence, and
reading only its totals is the same mistake as reading a coverage table instead of the pages.**

Sizes span 27 bytes to 4,885,200, median 12,288 — so a single shape here is not a single size, and
the byte-doubled group is the one most likely to reward a page.

### THE `.bin` WORKLIST, MEASURED — ten magics over nineteen units (OPUS, 2026-09-13)

Having found the `.dat` coverage marks stale in one direction, the same test was owed to `.bin`. The
figure carried elsewhere is *"eleven `bin` signatures have no page"*. **It is three.** Work has
landed since it was written, and counting mentions is in any case the weak test — the `himg` case
above shows a magic can be mentioned everywhere and laid out nowhere.

So both tests, the second a **stated proxy**: a magic counts as laid out when some page puts it
within about 500 characters of three or more `+0xNN` offsets. That is the shape of a byte table and
it is not a guarantee of one.

| | magics | units |
|---|---:|---:|
| **layout-shaped** — near a byte table on some page | **16** | **159** |
| mentioned only — named, never laid out | 7 | 16 |
| no page at all | 3 | 3 |

> **The worklist is the last two rows: ten magics over nineteen units.** `hctg` (6) and `gmap` (5)
> are the only ones above a single unit; `PLMN`, `GRMI`, `ashd`, `CLT2`, `hcom`, `QST1`, `EVME` and
> `hodr` are one unit each. **That is a much smaller job than "a bag of twenty-six" implies**, and it
> revises my own characterisation of `.bin` as a research programme a few hours earlier — at the
> MAGIC level it is nearly finished.

**What stays hard is the half that has no magic at all.** 178 of the 236 logical units carry one of
the 26 signatures; the other **58 units, and 258 of the 1,439 entries, have no magic** for any
instrument to key on. **That, and not the signature list, is why `.bin` cannot be "explained" as one
census row** — a point §5 already makes and this measurement sharpens: the format work is small and
the headerless work is the row.

### THE LAST TWO ROWS ARE NOT THE SAME SIZE OF JOB — measured 2026-09-13 (OPUS)

`formats_explained` reads **40 / 48**, and six of the eight short rows are held by SWE2-DATA. The
other two are `.dat` and `.bin`, and reading "eight to go" as eight comparable pieces of work is
wrong by more than an order of magnitude.

| | `.dat` | `.bin` |
|---|---|---|
| entries / logical units | 2,948 / **343** | 1,439 / **236** |
| distinct `MAGIC` signatures | **4** | **26** (+2 further verdict classes) |
| the most common one covers | `himg`, **309 of 343 — 90 %** | `st2e`, **73 of 236 — 31 %** |
| entries with **no magic at all** | 63 | **258** |
| what is left with no LAYOUT | ~~`himg` — 309 units, 90 %~~ → **`hdat`+numeric rows** (`himg` layout landed 2026-09-16, `himg-handbook-image-bundles.md`) | most of twenty-six |

> **`.dat` IS ONE FORMAT FROM COVERAGE, AND IT IS THE ONE THAT MATTERS.** I wrote "two small
> formats from coverage" here two hours ago, reading the `no page` marks in the table above —
> **which were stale, and the gap is the other way round.** `hchk` (6 units) and `qstd` (1) are
> both documented with byte layouts in `five-small-bin-tables.md` §12. **`himg` is not.** It
> covers **309 of 343 units — 90 % of `.dat`** — and every mention of it in the store is a
> census count or a one-line "image data, mostly menu" table cell. **No page gives it a
> layout.** *(Superseded 2026-09-16: `himg` now has a byte layout, corpus closure and the
> native consumer chain in `himg-handbook-image-bundles.md`.)*
>
> So the small change is done and the bulk is untouched, which is the reverse of the usual
> shape and the reason a coverage table that marks pages rather than LAYOUTS can mislead. I
> read the table instead of the pages, which is the same error this document's own §9 makes
> about citation counts. **`.bin` is a research programme** — a bag of
> twenty-six formats *and* 258 headerless entries, which §5 already says could not be "explained" as
> one census row even in principle.

**So the honest reading of 40 / 48 is not "eight formats to go".** It is six rows already being
worked, one row that is a short piece of work, and one row that is a subsystem. A percentage cannot
carry that and is not being asked to — **the denominator is still not re-cut**, for the reason §9
gives: a generated census an author reshapes after seeing the result is no longer a census. What
changes is only that the cost behind the number is now written down beside it.

### `dat` is nearly one format

| magic | units |
|---|---:|
| `himg` | **309** - **documented** 2026-09-16, `himg-handbook-image-bundles.md` |
| `hdat` | 17 |
| `hchk` | 6 - **documented**, `five-small-bin-tables.md` §12 |
| `qstd` | 1 - **documented**, same section |
| non-magic | 17 |

**`himg` alone is 90% of the units.** `himg` and `hdat` are each mentioned by two pages; `hchk` and
`qstd` are mentioned by **none**.

### `bin` is genuinely many formats

31 groups over 236 units, led by `st2e` (73), `sloc` (52), a `NOT_A_MAGIC` bucket (43), `licd` (13),
`UNDETERMINED` (9), `CHSE` (8), `hctg` (6), `gmap` (5).

**Seventeen of its 28 magic groups have at least one page that quotes the tag, covering 1,079
files. Eleven have none, covering 55 files:**

`QST1` (9), `sign` (9), `bwin` (9), `hcom` (9), `hodr` (9), `NAV.` (3), `MRF.` (2), `MENU` (2),
`EVME` (1), `VIB0` (1), `FOOT` (1).

> **"A page quotes the tag" is not "a sheet explains the format."** That test was chosen because it
> is mechanical, and it is an **upper** bound on coverage - some of the 17 are a passing mention in
> a table.

### ✖ Corrected the same day: the eleven were an over-count

I called the eleven "the safe half - nothing at all mentions them, so they are a worklist no reading
can argue with." **A reading argued with it immediately.** Searching by **filename** instead of by
magic tag finds pages for **six** of the eleven:

| tag | file | already covered by |
|---|---|---|
| `NAV.` | `navimapdata.bin` | [field record table](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) - **fully explained**, magic `NAV\x02`, with the size law `8 + 3 * 1154 == 3470` |
| `MRF.` | `map_ref.bin` | [area nmb index](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md) |
| `QST1` | `questbase.bin` | [the NPC name dictionary](../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md) |
| `EVME` | `eventmemorylist.bin` | the field record table page |
| `hcom`, `hodr` | `menuhandbook*.bin` | [resource section addressing](../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) |

**`NAV.` was not a gap at all** - the page that covers it derives the magic *and* an exact file-size
law, and my tag test missed it only because the magic is written `NAV\x02` rather than as a quoted
four-character token.

> **The lesson is the same one, one level up.** A mechanical test is a lower bound on coverage *or*
> an upper bound, never both, and mine was reported as if it were exact. **Two mechanical tests
> disagreeing is the signal**: quote-the-tag found 17 of 28, filename found 23. The truth is between
> them and neither number is it.

**The five that survive both tests** - nothing mentions the tag, nothing mentions the filename -
are `FOOT`, `MENU`, `VIB0`, `bwin` and `sign`. Those five are now decoded in
[five small `.bin` tables](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md),
each with its layout proved by reproducing the file size exactly. **The real `bin` residue is five
signatures, not eleven.**

> **`dat`'s two are closed as well** (2026-09-13). `hchk` and `qstd` are decoded in §12 of the same
> page and pinned to **kind 7 id 757** and **kind 7 id 296**, each confirmed twice - the size is
> unique in the whole 205,000-entry `.fst`, and reading the kind-7 path array at that index returns
> the file's own path. **So every signature either has a page or is now decoded**, and what remains
> for `formats_explained` is the per-signature disposition key, not the knowledge.

> **The remaining six silent signatures are now decoded too** (2026-09-16, SWE2-DATA): `QST1`
> (`questbase.bin` — `{magic, u32 173, u32[173]}`, kind 9 id `0x21`, consumers `00473B90`/
> `00473C90`), `EVME` (`eventmemorylist.bin` — `{EVME, MLST, u16 8, u16[8]}` in
> [event-memory-at-actor-bind](../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md)),
> `hcom`/`hodr` (`menuhandbook*.bin`, kind 7 ids `0xC8`/`0xC9`, layouts in
> [the handbook screen](../16-UI/Handbook/the-handbook-screen.md)), `dP<d`
> (`summoneffectdata.bin` — dispositioned at container level), and `//22`, which was never a
> magic at all — it is the doubled first texels of `face_guest15.bin`
> ([bin_menu sheet](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md)).
> `QST1` and `dP<d` are §13/§14 of
> [five small `.bin` tables](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md).
> The earlier rows that said "a page mentions the filename" were right but shallow — mention is
> not explanation; now the layouts exist.

### This does not move `formats_explained`, and the reason is structural

`check_assets.py` dispositions **an extension**. `bin` and `dat` need dispositioning **per
signature**, and there is no key for that - the same shape of gap `EC-7` names for functions.

> **Adding one would change a scored dimension's denominator** from 48 extensions to 48 plus some
> number of signatures, which is a program-level decision and is **routed, not taken**
> (`OPUS-REQ-DISPOSITION-PER-SIGNATURE`). Until then `bin` and `dat` stay **undispositioned and
> honest**, and the dimension stays at **40 / 48**.

**Reproduce:** `census_bin_signatures.py --ext .bin` and `--ext .dat`, writing
`Tools/work/formats/bin-signature-census.tsv` and `dat-signature-census.tsv`. The `.dat` census is
new; the script already took `--ext` and needed no change.

> **Both TSVs are untracked.** `Database/Tools/work` is gitignored, so these are regenerable
> work products and not repository content - the same treatment the `.bin` census has always had.
> **Do not look for them in git; run the command.**

## 4d. **48 / 48 would not mean the archive is documented** — measured 2026-09-03

**The denominator counts extensions. Several extensions are indexed containers whose interiors are
a second population nobody has censused.** EBP was recognised as one and given a 14-unit dimension;
the others were not, and a container-detection sweep over the archive shows how much that hides.

| family | files | interior | in the denominator as |
|---|---:|---|---|
| `.ebp` | 10,045 | 20-slot directory → **14 censused units** | its own scored dimension ✔ |
| **`PKFL`** — `.mot` `.snd` `.vpc` `.vpcjp` | **10,314** | **16- and 64-slot directories, 28 distinct slot indices occupied** | **4 extension rows** ✘ |
| `.bin` | 1,439 | **7 signatures**; `battle_pack.bin` alone is a **71-slot** offset table | **1 extension row** ✘ |
| `.ard` | 332 | `FF12AR03` wrapping `st2e` tables | 1 extension row ✘ |

**Method:** for each format, sample entries and test whether a leading count is followed by that
many ascending in-range offsets. `.ebp` returns 20 slots, `.vpc`/`.vpcjp` return 64. A 160-file
PKFL sample was 160/160 `PKFL`, split 108 files at 16 slots and 52 at 64, with **indices 0–27 all
occupied and none skipped** — a densely packed directory, unlike EBP's sparse one.

> **So `formats_explained` could read 100 % while the interiors of the two largest container
> families remain undocumented.** That is the same defect as bulk-citing 11,836 functions to move
> `engine_explained`: **a number that agrees with itself while the mission is unmet.**

**The precedent for the fix already exists and should simply be repeated.** EBP got a censused
denominator *before* anyone wrote a sheet, which is why its 14 units are trustworthy. PKFL needs the
same census — roughly **28 units over 10,314 files** — and `.bin` needs splitting into its seven
signatures before either is written up.

**Do the census first.** Writing PKFL sheets against four extension rows would repeat the
extension-versus-format distortion at more than twice EBP's scale, and it would be discovered
afterwards rather than before.

## 4c. Two of these formats are name oracles, not just formats

**`jsondata` and `prefetchdata` are worth more than their census rows suggest**, because they carry
the engine's own vocabulary in plain text. They are wired in as **evidence sources**, not as a new
scored dimension — the rule is in
[EVIDENCE-STANDARD.md](EVIDENCE-STANDARD.md), *"a name oracle is tier 9 until it is joined to the
binary — then it is tier 2"*.

| corpus | scale | what it gives |
|---|---|---|
| `jsondata/maps` | 459 files, **175 keys, 137 of them literal strings in the EXE** | key → string VA → xref → the reader → the struct field. Corpus: `Tools/work/formats/jsondata-parameter-names.tsv` |
| `jsondata/cutscenes` | 337 files, keyed `Cut 1`…`Cut N` | the same vocabulary per camera cut |
| `prefetchdata` | 9,351 files, ~1,040 per language | a complete **asset → scene map**, each with a declared `##Total_data_Size:_N_MB` budget |

**And the 38 keys with no literal are a finding of their own:** 27 carry authoring-tool markers
(`…CheckBoxCheckState`, `…LockCheckBox`), so **Square Enix's internal lighting-editor UI state ships
inside the retail game data**. No tool-marked key appears in the binary and none of the 137 present
keys is tool-marked — two independent classifications, zero contradictions.

Detail, including the eleven genuinely open keys and the `mMapAmbientColorA` control, lives with the
system it names:
[17-Presentation-Rendering/Visual-Tuning-Parameters](../17-Presentation-Rendering/Visual-Tuning-Parameters/README.md).

## 5. `.phyre` is `external`, and that is a decision not an omission

[COMPLETION-PLAN.md](COMPLETION-PLAN.md) §7 already puts re-documenting middleware from the file
side out of scope: PhyreEngine is generic across titles and its container is documented elsewhere.
**35,984 files — 40 % of the archive by count and 72 % by size — are cleared by cross-link.**

**But the disposition carries an obligation.** The database's stated unique contribution is the
loader contract, and an `external` row should still say what *this* build does: which class
descriptors it registers, what it rejects. That work is already begun in
[the file/runtime schema join](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md),
whose 22 unresolved classes are the open edge of exactly this question.

## 6. The formats that are not archive entries

These ship **loose in the install**, so the archive census cannot see them. Censused separately —
the install holds 12 `.fst`, 2 `.ini`, 1 `.xml`, 1 `.vbf`, 2 `.exe`, 8 `.dll`.

They keep `container_format:` and stay **counted, not scored**: four are documented, the population
is small and known, and inventing a percentage over a handful of files would be worse than the
plain count.

| format | where | state |
|---|---|---|
| VBF bigfile index | `FFXII_TZA.vbf` | **documented** |
| `st2e` authored tables | inside archive entries | **documented** |
| save image | save slots | **documented** |
| `GameSetting.ini` | `ConfigData/` | **documented — reader side only**, see §7 |
| `.fst` file-size tables | `FileSizeTables/` | **not documented** |
| `keymap.ini` | `ConfigData/` | **not documented** |
| `GaussianFilterSetting.ini` | `ConfigData/GaussianFilter/` | **not documented** |
| `SettingsLoc.xml` | install root | **not documented** — plain readable XML, all languages |

## 7. Two finds worth their own sheets

**`FFXII_TZA_GameSetting.exe` is a managed .NET assembly** — verified, CLR directory at RVA
`0x2008`. The database documents the `GameSetting.ini` **reader**: the `0x65C` singleton at
`0x01F82D20`, 31 dword slots, three parallel tables. **The writer is this separate program**, and it
knows the valid value sets, the validation and the keymap format.

> **It decompiles to near-source.** Against the effort of establishing the same facts from native
> code, this is the cheapest high-value item on the whole completion plan — and it is the only place
> in the database where the *authoring* side of a format is recoverable rather than inferred.

**`FileSizeTables/*.fst`** — 12 files, **exactly 820,000 bytes each** (205,000 dwords), first dword
`0x39`, then long runs of `0xFFFFFFFF`. **10 distinct contents across 12 language files.**
Load-bearing for the loose-file mod scene: a file-size table is precisely what a loose-file override
loader must satisfy, and the External File Loader is present in this install.

## 8. The order to do them in

**By size of the hole, not by file count**, with one exception.

1. **`.sab` + `.snd`** — 6,913 files against an audio subsystem that is already well read. The
   engine half is done, which makes these the cheapest sheets in the list.
2. **`.mot` + `.adm`** — 4,431 files, 2.5 GB, and animation is a subsystem modders actually touch.
3. **`.efx` + `.efb`** — 3,698 files, 4.5 GB.
4. **`.ca` + `.cm`** — 4,230 files.
5. **The `standard` sweep** — `webm`, `tga`, `ico`, `csv`, `h`, `tm2`, `cnf`. Cheap, and each still
   owes the note that says where the loader departs from the spec.
6. **`.phyre` as `external`** — one row, one cross-link, 40 % of the archive.
7. **`ah`, `mpk`, `ard`, `nmb`, `ta`, `ker`, `fex`** and the `ps2data/image` tail — the genuine
   unknowns, and the ones where the archive gives the least help.

**The exception is `.ebp`**, which is not in this list because it has its own dimension and its own
14-unit census. Doing it twice would be double-counting.

## 9. What this index does not claim

- **Every owner in §4 is a proposal from file location.** No sheet may cite this table as evidence
  of ownership; the sheet establishes ownership, not the index.
- **`unknown` means unknown.** Seven formats have no proposed owner at all, and a guess dressed as
  a proposal would be worse than the blank.
- **The census counts extensions, not formats — measured in §4b, and wrong in both directions.**
  Four groups are one format under several extensions (`PKFL` alone covers four rows, 10,314 files);
  **`.bin` is TWENTY-EIGHT signature classes under one row** — §5's full census, not the "seven"
  this line carried until 2026-09-13, which was a floor from a 12-file sample that §5 had already
  retracted. **The sampling caveat below does not apply to `.bin`:** its census read all 1,439
  entries. **The denominator was not re-cut to hide this**, because a
  generated census that an author reshapes after seeing the result is no longer a census. The
  mapping is published, `check_assets.py` enforces the group rule, and the distortion is stated.
- **The magic census samples 12 files per extension.** A format present in 1 % of an extension's
  files will usually be missed, so **a single signature is not proof of homogeneity** — only
  evidence for it.
- **Sizes are uncompressed archive sizes** from the index, not on-disk sizes.

## 10. Related

- [COMPLETION-PLAN.md](COMPLETION-PLAN.md) — where this dimension sits in the whole
- [COVERAGE.md](COVERAGE.md) — the reasoning behind the denominator and the re-weighting
- [25-EBP-Script-Container](../25-EBP-Script-Container/README.md) — the one archive format already scoped
- `_templates/FORMAT.md` — the sheet every `explained` row is written to
