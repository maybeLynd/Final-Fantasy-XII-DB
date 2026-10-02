# `st2e` carriers — the wrappers the authored tables ship inside

**`st2e` is the authored-table format and the database already documents it.** What was missing is
that it does not ship loose: it arrives wrapped, and the wrappers were filed as unknown.

| carrier | files | magic | verified 2026-09-03 |
|---|---:|---|---|
| **`.ard`** | 332 | `FF12AR03` | **40 of 40 sampled contain `st2e` tables** |
| **`battle_pack.bin`** | 1 per language | 71-slot offset table | **37 `st2e` tables in one file** |

## Why this folder exists

> **Authored side and runtime side are the same data at two ends.** These carriers are where the
> tables live *on disk*; the [63-slot authored-data registry](../../authored-data-table-registry.md)
> is where they live *at run time*. That is why the format work and `registry_explained` converge,
> and why neither is finished without the other.

## `.ard`

`ps2data/plan_master/<locale>/plan_map/<area>/area/<area>.ard`. Magic `FF12AR03`, then `st2e`
tables from roughly `+0x30`.

**The unit is the AREA — not the map, and not the enemy.** The `plan_map` tree is two levels deep
and the two levels hold different things:

```
plan_map/
  ztc_d/                       <- AREA        251 distinct names
    ztc_d01/
      global/ztc_d01.ebp       <- MAP         935 distinct maps, one .ebp each
    area/
      ztc_d.ard                <- AREA data   the st2e carrier
      ztc_d.nmb                <- AREA data   its strict pair
```

**332 files, but only 166 logical areas.** Every `.ard` ships **twice** — once under the `ch`
locale tree and once under `in`, 166 each, and no other locale carries one at all. So the corpus
for a sheet is 166 areas, and the file count double-counts.

> **`.ard` and `.nmb` are a strict pair.** Identical stem sets, 166 each, always in the same
> `area/` folder — **never one without the other**, the same shape as EBP's `008`/`009`. `.nmb`
> averages 56 bytes per file, so the natural reading is an index or name list *for* the `.ard`, and
> a sheet should treat the two together rather than separately.

**Two open questions the counts raise.** Only **166 of 251 areas** have an `.ard` at all — so
whatever it holds, a third of areas do without it. And a per-area data file shipping under exactly
two locale trees, neither of them `us` or `jp`, is not what a localisation split looks like.
**Neither is explained; both are recorded rather than smoothed over.**

## Census — 166 of 166 areas, 2026-09-03

`census_ard_container.py` → `Tools\work\formats\ard-container-census.tsv`. **Keyed by area stem, not
by file**, so the locale duplication is reported rather than inherited.

| | |
|---|---|
| area stems | **166** — 332 `.ard`, 332 `.nmb`, **zero areas missing either half** |
| copies per area | **exactly 2, in all 166** (`ch` and `in`) |
| **duplicate copies byte-identical** | **166 of 166** |
| magic `FF12AR03` | **166 of 166** |
| **`st2e` tables per `.ard`** | **exactly 4, in all 166** |
| `.ard` size | 224 – 35,632 B |
| `.nmb` size | 8 – 162 B |

> **The two locale copies are byte-identical in every area.** The `ch`/`in` duplication is redundant
> packaging, **not localisation** — which kills any reading in which `.ard` content varies by
> language. *Why* only those two trees remains unexplained; that it carries no per-language
> difference is now settled.

> **Every `.ard` holds exactly four `st2e` tables — 166 of 166, no exceptions.** A fixed arity
> across the whole corpus is a far stronger structural fact than a range, and it is the shape a
> sheet must explain: four tables of *what*, in the same order, for every area in the game.

### Header, measured across all 166

```struct Ff12Ar03Header base=file size=0x30
+0x00  char[8]  magic       FF12AR03 in 166 of 166
+0x08  u32      _zero0      0 in 166 of 166
+0x0C  u32      trailerOff  134 distinct values - offset-shaped (census name varA)
+0x10  u32      slot0       0x30 in 166 of 166 (census name const30)
+0x14  u32      slot1       16 distinct values (varB)
+0x18  u32      slot2       149 distinct values - offset-shaped (varC)
+0x1C  u32      slot3       0 in 166 of 166 - absent
+0x20  u32      slot4       0 in 166 of 166 - absent
+0x24  u32      slot5       150 distinct values - offset-shaped (varD)
+0x28  u32      slot6       150 distinct values - offset-shaped (varE)
+0x2C  u32      slot7       151 distinct values - offset-shaped (varF)
```

*(Field names harmonised 2026-09-11 with the loader page's fence — one `Ff12Ar03Header`, the
0x30-byte eight-slot directory header, is declared with one set of names wherever it appears;
the census names this sheet coined are kept in the comments. OPUS-REQ-FABLE-FENCEDUP.)*

**`varD`/`varE`/`varF` ascend together** — in the smallest area they are 128 / 160 / 192, spaced 32.
That is the shape of a directory, and it is a **lead, not a reading**: no loader has been consulted.

### How `.ard` is reached — hardcoded paths, not a pattern — 2026-09-04

**The engine does not build `.ard` filenames. It holds every one of them as a literal string.**

| | |
|---|---|
| `.ard` path strings in the EXE | **430**, full paths, both `in` and `ch` trees |
| pointers to them | **430 — every string referenced exactly once** |
| table span | `0x01E0D060` – `0x01EDD680`, in `.data` |
| stride | **16 bytes in 406 of 429 gaps** |

```struct ArdTableEntry base=record size=0x10
+0x00  u64  ardPath   char* to a full PS2Data\...\<area>.ard path
+0x08  u64  fpkPath   char* to the matching .fpk path - USUALLY NULL
```

**`FF12AR03` appears nowhere in the binary** — zero occurrences as text, zero as the dword `AR03`.
**So the magic is not validated by a literal comparison**, exactly as `repos-1e` established for the
`EBP2` container magic. Two containers, same result; and per `CA-4`, section magics *are* checked,
so this is a property of container headers rather than a blanket no-validation policy.

> **The absence is not proof of no check** — a comparison can be built by arithmetic or folded into
> a hash. But a 430-entry table of literal paths says the loader was never looking for `.ard` files
> generically in the first place, which makes a magic check redundant by design.

### `.fpk` — 7,520 paths in the binary and not one file in the archive

The second field of every table entry is a **`.fpk`** path beside the `.ard`
(`…\ttl_a\area\ttl_a.fpk`). It is null in 33 of the first 40 records.

| | in the EXE | in `FFXII_TZA.vbf` |
|---|---:|---:|
| **`.fpk`** | **7,520 strings** | **0 files** |
| `.nmb` (control) | 642 strings | 332 files |

> **A format the engine carries seven and a half thousand hardcoded paths for, and which does not
> ship at all.**

**The control was originally stated too strongly, and `repos-4b` corrected it.** This README said
*"the `.nmb` control shows the instrument works: a format that does ship appears in both columns"* —
which implies a path in the table predicts a shipped file. **It does not.** Only **166 of the 321
kind-26 entries ship a file — 52 %** — the rest being development areas (`tst_*`, `ttl_*`, `e00_*`).

> **A path in a table is not evidence that the file ships.** So `.nmb` is a weak control, not a
> clean one.

**The finding survives anyway, because it never rested on the contrast.** A format that ships for
52 % of its table entries and a format that ships for **0 of 7,520** are categorically different,
and the zero is what carries the claim. Corrected rather than quietly softened, because the
*reason* a conclusion holds is part of the conclusion.

`.fpk` is absent from the 48-extension archive census entirely, so **no existing dimension counts
it** — it cannot be found by censusing what ships. This is the same shape as `BW-1` (`section_017`
has a live handler and occurs in 0 of 1,115 files): **authored capacity the shipped game never
uses.** Cut content, a dev-only path, or a format folded into another before release — **none of
those is established**, and the count is what is being reported here, not a story about it.

### `.ard` and EBP `section_019` are the same container

`section_019` also carries the magic `FF12AR03`, in 271 of 271 files. **The same format in two
places** — a standalone per-area file and an embedded EBP section — which is the trick `st2e` plays,
and the trick `CML1` plays across EBP slots 8 and 10.

**They are not identically constrained.** `repos-c9` found `section_019` has `+0x10`, `+0x14`,
`+0x18` and `+0x2C` all `0x30` in 271 of 271; in `.ard` **only `+0x10` is `0x30`**, while the other
three vary across 16, 149 and 151 values. **So `section_019` looks like a degenerate case of this
header** — every directory offset collapsed to one constant. Whoever writes either sheet should
write both; question `BZ-2` is where this lands.

**The modding community reads `.ard` as per-area enemy status and attributes.** That reading is
**tier 9 — authored intent, never ownership — until a reader is named in the binary.** What is
verified here is only that the file is `FF12AR03` and contains `st2e`; what the tables *mean* is
not. **Do not promote the community reading by repeating it.**

*Correction to the common description:* `.ard` is one per **area**, not one per map — `plan_map`
holds 769 map directories against 332 `.ard` files.

## `battle_pack.bin`

`ps2data/image/ff12/test_battle/<lang>/binaryfile/battle_pack.bin`, ~281 KB for `us`.

**A 71-entry offset table**, ascending, table ending ~~`0x120`~~ `0x124` (the count and 72 four-byte offsets) and first payload at `0x128` *(corrected 2026-10-02, OPUS: the binder's `+0x56` `lea rbx, [r9 + 4]` and `+0x97` `add rbx, 4`, over count + 1 entries to its `+0x9B` `cmp rdi, rax` and the `jle` at its `+0x9E`)*.

> **⚠ Corrected 2026-09-04 by `repos-c7`'s `.bin` census.** This README originally said the table
> was *"structurally the same shape as the EBP2 and PKFL directories"* and that the engine reuses
> one container idea in three places. **It does not.** `battle_pack`'s directory is **packed, with
> ~~8-byte entries~~ 4-byte entries, and 29 of its 71 slots aliased** *(corrected 2026-10-02, OPUS: the binder steps 4 bytes, its `+0x97` `add rbx, 4`)* — none of which is true of the EBP2 or `FF12AR03`
> directories, which are index-addressed with 4-byte entries and `0 = absent`.
>
> **A leading count followed by ascending offsets is a shape, not an identity.** The same section
> below already flagged this as the thing a sheet must settle — *"similar shapes are a lead, and
> this database has been wrong on exactly that before"* — and then the prose above asserted the
> similarity anyway. **The hedge and the claim were in the same document, and the claim is what a
> reader would have carried away.**

The community reads **section 13 as all weapon statistics** (stats, attributes). Same standing as
above: **a lead, not a finding.**

*Correction:* the path is `ff12/test_battle/<lang>/`, not `ff12/us/test_battle/us/`.

## Why these were invisible

`.ard` sat in `_index/ASSET-FORMATS.md` §4 as **unknown** — the archive gave a directory and nothing
else. `battle_pack.bin` was worse: it is inside `.bin`, which the magic census found carries **seven
different signatures in twelve samples**, so it is one census row standing for a bag of unrelated
formats.

**Both were found by checking outside knowledge against the archive, not by any instrument here
reporting anything.** Recorded because the next gap of this shape will be found the same way.

## What a sheet here must establish

- the carrier header, in a `struct` fence, with `base=` stated
- **where the `st2e` tables begin and how many there are** — from the corpus, not one file
- **the loader contract**: which reader consumes the carrier, what it rejects, and which fields
  nothing reads
- whether the 71-slot `battle_pack` directory is the same layout as EBP2's and PKFL's, or merely
  similar — *similar shapes are a lead, and this database has been wrong on exactly that before*

## Related

- [`../vbf-archive-and-st2e-tables.md`](../vbf-archive-and-st2e-tables.md) — the `st2e` format itself
- [`../../authored-data-table-registry.md`](../../authored-data-table-registry.md) — the runtime end, 63 slots
- [`_index/ASSET-FORMATS.md`](../../../_index/ASSET-FORMATS.md) §4bb — the verification behind this folder
