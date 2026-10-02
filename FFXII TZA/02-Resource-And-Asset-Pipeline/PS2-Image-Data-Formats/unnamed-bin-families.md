---
system: The twenty .bin families no path in the executable names
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: PrimaryOwner:Resource
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: literal search of the authority image plus an archive census - census.py over all 146
    .bin families (1,439 files), each family's name looked for in the per-kind path tables and as a
    loader literal, with the separator anchor that keeps ctrl.bin from false-matching inside
    musicctrl.bin. **This is the method of the ORIGINAL derivation, not a later check.** The
    document cites one address, 0215F000, and it is data.
  reclassified: 2026-09-14 (OPUS) - was GZF-derived, stamped gzf fb9b5e7e / snapshot a9cead87
    (GN159) and carrying a snapshot-identity transfer to GN160 under
    OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144. That basis quantifies over "every function this
    document cites" and this document cites NONE, which made it VACUOUSLY true - a pass for the
    wrong reason, found when the transfer was re-adjudicated for GN161. Its evidence never rested
    on function annotation at all: it rests on the image's bytes and the archive, so the stamp it
    always needed is this one, which cannot go stale.
corpus_validated: "146 of 146 .bin families (1,439 files) searched for their file name in the executable; 20 families, 41 files unnamed, 2026-09-13"
container_format: "bin families without a path literal"
last_reviewed: 2026-09-13
archive_formats:
  - "filelistlocalin | explained | filelistlocalin.bin (.bin member): u32 sectionOffset[38], each {u32 count, u32 absoluteStringOffset[count]} into 24,358 disc paths - decoded, control filelistlocalin.py; no PC loader (every byte inert), UQ-70 / UQ-380"
  - "st2enames | explained | basic_skill_basic_skill_name.bin and growth_rate_growth_rate_name.bin (.bin member): {u32 count, u32 offsets[count+1] (the last = file size), UTF-16LE strings}, count = the st2e sibling's rows - controls uq70_name_tables.py, endslot_check.py (end slot, narrowed 2026-09-30 per SWE2-AUDIT-SEM N2); no PC loader, UQ-70"
  - "logicpack | explained | logicpack.bin (.bin member): {u32 count, u32 offsets[count+1] (the last = file size, endslot_check.py)} over .ard AI logic blocks (0x20-byte u8 group-count header + 24-byte entries), 1,147 of 1,310 byte-identical to shipped .ard blocks - control logicpack.py; no PC loader, UQ-70"
  - "ashd | explained | katano/event.bin (.bin member): ashd 12-byte header + flagless LZ token stream, two layers, payload a v0x80000002 section_000 script image - control ashd_decode.py; no PC loader, UQ-70"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-unnamed-bin-families-pass-1 - 20 families / 41 files reproduced exactly; the separator anchor is load-bearing (without it ctrl.bin false-matches inside musicctrl.bin, a control); the ten st2e families split three ways by header arithmetic; every directory segment of every unnamed family is present as a literal
  crossref_clean: true
  reopened_count: 0
---

# The `.bin` families nothing names

> Of the 146 `.bin` families in the archive, **20 (41 files) have no file name anywhere in the executable** —
> neither in the per-kind path tables that name most PS2-era files nor as a literal a loader opens. Most are
> Chinese- and Korean-tree copies of battle tables whose other members *are* named, the four ATEL control
> scripts, four extra world-map sub-picture sets, and two one-offs. This page records them and what their bytes
> are; it does not claim any is unreachable at run time.

**Corpus validation.**

| | |
|---|---|
| `.bin` families searched | **146 of 146** (1,439 files); a family is a directory with the language segment and digit runs folded |
| test | the file name right after `\` or `/`, digit runs as digits, case-insensitive, in ASCII and in UTF-16LE |
| positive controls | `battle_message.bin`, `menumap_sub#.bin`, `npcdic.bin`, `musicctrl.bin` — all found |
| unnamed families | **20, 41 files** |

Census: [`census.py`](../../_experiments/evidence/unnamed-bin-families/census.py) →
[`census.out.txt`](../../_experiments/evidence/unnamed-bin-families/census.out.txt).

---

## 1. What the player sees

**Nothing that can be tied to them.** A file whose path the executable never spells cannot be requested through
the path tables or a literal; whether some other route (a name assembled at run time from pieces, or a lookup that
is not by name) reaches them is the open part (§7).

## 2. The families

| Family | Files | Bytes | First bytes | What the bytes are |
|---|---|---|---|---|
| `test_battle/<lang>/binaryfile/actionchip_data.bin` | `cn`, `kr` | 32 | `st2e` | a bare 32-byte [`st2e` table](../VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) header — no record bytes follow; **count 0, stride 8** (§9) |
| `…/bukitye_data.bin` | `cn`, `kr` | 32 | `st2e` | a bare 32-byte `st2e` header — no record bytes follow; **but it claims 23 records with stride 0** (§9) |
| `…/basic_skill.bin` | `cn`, `kr` | 75,352 | `st2e` | `st2e` table |
| `…/growth_rate.bin` | `cn`, `kr` | 7,200 | `st2e` | `st2e` table |
| `…/mons_act.bin` | `cn`, `kr` | 11,756 | `st2e` | `st2e` table |
| `…/mons_category.bin` | `cn`, `kr` | 156 | `st2e` | `st2e` table |
| `…/mons_race.bin` | `cn`, `kr` | 444 | `st2e` | `st2e` table |
| `…/object_data.bin` | `cn`, `kr` | 1,708 | `st2e` | `st2e` table |
| `…/target_data.bin` | `cn`, `kr` | 39,000 | `st2e` | `st2e` table |
| `…/unit_data.bin` | `cn`, `kr` | 41,612 | `st2e` | `st2e` table |
| `…/basic_skill_basic_skill_name.bin` | `cn`, `kr` | 74,868 | `41 05 00 00` | ~~not decoded~~ *2026-09-26: the **designer names of `basic_skill.bin`'s 1,345 rows** — a count, an offset table, UTF-16LE strings (`LEVEL-00基本値` …); `UQ-70` box* |
| `…/growth_rate_growth_rate_name.bin` | `cn`, `kr` | 3,310 | `80 00 00 00` | ~~not decoded~~ *2026-09-26: the **designer names of `growth_rate.bin`'s 128 rows**, same layout (`テスト成長値` …); `UQ-70` box* |
| `…/logicpack.bin` | `cn`, `kr` | 1,035,896 | `1E 05 00 00` | ~~not decoded~~ *2026-09-27 (OPUS): a pack of **`.ard` AI logic blocks**, 1,147 of 1,310 byte-identical to shipped `.ard` blocks; `UQ-70` box* |
| `<lang>/bin/ctrl.bin`, `btlctrl.bin`, `evctrl.bin`, `mapctrl.bin` | `ch`, `in` each | 8,352 / 24,576 / 22,320 / 29,392 | `0B 00 00 80` | the four ATEL control scripts — [EBP2 containers](../../25-EBP-Script-Container/Container/ebp2-container.md), counted in its 10,036-container census; their companions are [inert](../../01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md) |
| `<lang>/bin/filelistlocalin.bin` | `ch`, `in` | 1,137,120 | `98 00 00 00` | ~~not decoded (a leading count and ascending offsets, by eye)~~ *2026-09-27 (OPUS): the **PS2 disc's per-kind file list**, 38 sections, 24,358 paths; `UQ-70` box* |
| `myoshiok/<lang>/worldmap/menumap_sub#_e#.bin` | 3 `in`, 1 `us` | 2.9–11.0 MB | `sloc` | [menu-map sub-picture containers](sloc-menumap-container.md), variants of the named `menumap_sub#.bin` |
| `katano/event.bin` | one | 2,370 | `ashd` | ~~not decoded~~ *2026-09-27 (OPUS): two layers of a bespoke LZ around a **compiled ATEL event script image** (tag `0x80000002`, `event.src`, 9,184 bytes); `UQ-70` box* |

The ten `st2e` families sit in directories whose other 66 families are named: all ten exist only in the `cn` and `kr`
trees.

> **They are not one thing (measured 2026-09-13, §9).** Reading each header as
> `{magic, count, stride, dataoff}` and comparing `dataoff + count × stride` with the file size
> splits the ten three ways: **three fit exactly** (`basic_skill`, `growth_rate`, `unit_data`),
> **three describe nothing** (`actionchip_data` count 0; `bukitye_data` and `mons_act` **stride
> 0**), and **four carry far more than the header accounts for** (`mons_category` 64 of 156,
> `mons_race` 160 of 444, `object_data` 560 of 1,708, `target_data` **8,752 of 39,000**).
> `mons_act` is the sharpest: a header describing **zero** bytes in front of **11,756**.

## 3. The loader contract

**No loader.** The `.bin` path tables (`0215F000[kind]`, [the resource path tables](../VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md))
and the literal paths opened by loaders are the two ways a PS2-era file is named in this build; the census finds
neither for these files.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| every byte | nothing found | — | — | by name, yes |

**The write path.** None.

## 4. Key addresses

None — the finding is an absence. The census's controls show the search finds named siblings.

## 5. Corpus survey

41 files: 13 `test_battle` families × (`cn`, `kr`) = 26, 5 `bin` families × (`ch`, `in`) = 10, 4 `menumap_sub#_e#`
files (3 `in`, 1 `us`) and `katano/event.bin`.

## 6. Falsification pass — planned attack (2026-09-05), run in §9

The obvious attack is a name built at run time: a string search for `_e%` finds only the cube-map
formats (`cubemap_%d_%d_e%d.dds.phyre`), and the stems of the thirteen `test_battle` families occur nowhere at all (the `ctrl` and `event` stems do
occur, inside other names), but every `sprintf` argument was not enumerated.

## 7. What this document does not claim

- [x] **UQ-70.** What the five undecoded families hold (`logicpack`, `filelistlocalin`, the two `_name` tables,
      `katano/event.bin`). `UB-1`. *(Split 2026-09-14, FABLE: this box asked two questions.)*
      *Narrowed 2026-09-26 (FABLE, Claude Opus 5.5): two of the five are decoded.* Control: [`uq70_name_tables.py`](../../_index/candidates/uq70-name-tables/uq70_name_tables.py) (5 checks,
      FAILS 0).
      - **The two `_name` tables** are a `u32` count, then ~~that many~~ count + 1 ascending offsets, the last the file size *(corrected 2026-10-02, OPUS: `basic_skill` 1,345 and `growth_rate` 128 rows; the first string sits at `4 + 4·(count + 1)` and `offsets[count]` equals the file size, `kr` and `cn`)*, each to a NUL-terminated
        UTF-16LE string. Each count equals the row count of its `st2e` sibling: 1,345 for `basic_skill`, 128 for
        `growth_rate`. So they are the **designer names of those rows**, in Japanese (`LEVEL-00基本値`,
        `[sav]Mons[ウルフ／ハイエナ]`, `テスト成長値`, `街の人成長値`). The `cn` and `kr` copies are identical.
      - **`logicpack.bin`** has the same count-and-offsets frame: 1,310 records of 56 to 3,008 bytes, all multiples
        of 8. What a record holds is not decoded, and no record occurs verbatim in another `test_battle` file.
      - **`filelistlocalin.bin`** (152 non-ascending offsets) and **`katano/event.bin`** (`ashd` chunks) stay open.
      *Narrowed 2026-09-27 (OPUS; carried here by FABLE as page owner): two more are decoded.* Controls:
      [`filelistlocalin.py`](../../_index/candidates/uq70-filelistlocalin/filelistlocalin.py) (6 checks) and
      [`logicpack.py`](../../_index/candidates/uq70-filelistlocalin/logicpack.py) (4 checks), FAILS 0.
      - **`filelistlocalin.bin`** is the PS2 disc's file list by resource kind. It is `u32 sectionOffset[38]`, each
        section `{u32 count; u32 absoluteStringOffset[count]}` into a pool of 24,358 `%`-rooted disc paths. Section
        *k* lists the family of the file-size table's kind *k* (section 11 is exactly `m0000`..`m0511`). The `ch` and
        `in` copies are identical, and the PC executable never reads the file (`UQ-380`).
      - **`logicpack.bin`** is a pack of `.ard` AI logic blocks: each record is a `0x20`-byte header of `u8` group
        counts followed by that many 24-byte entries. 1,147 of the 1,310 records are byte-identical to AI blocks of
        the 166 shipped `.ard` files; the other 163 are variants not in the shipped maps. (The 2026-09-26 line above
        compared it only against other `test_battle` files.)
      - **`katano/event.bin`** remains: the only `ashd` file in the extract, a compressed stream ~~(declared size
        `0x2509` against 2,370 bytes)~~ that no stock LZSS reproduces. OPUS proposed NO ADMISSIBLE SOURCE; FABLE's
        non-author review [declined it on scope](../../_index/candidates/nas-review-uq70-ashd-fable/README.md), as
        MH-1 was: the decoder lives in the PS2 build, and the data may still be reversed. It stays open.
      *Answered 2026-09-27 (OPUS; applied to this page by OPUS with the register row, for FABLE's review as page
      owner): the fifth is decoded, by reversing the scheme from the data.* Control:
      [`ashd_decode.py`](../../_index/candidates/uq70-ashd-scheme/ashd_decode.py) (D0-D3, C1, K1-K4), FAILS 0.
      - **The scheme.** `ashd` is a 12-byte header (magic, `u32 field04`, `u32 decodedSize`) and a token stream
        with no flag bytes. An even token `t` copies the next `t >> 1` literal bytes. An odd token opens a
        little-endian `u16 w`, a back-reference of length `(w >> 12) + 3` at distance `((w >> 1) & 0x7FF) + 1`.
        **Correction:** `0x2509` is `field04`, not the declared size. The declared size is the third dword,
        `0x0B10`. `field04`'s role is open.
      - **Two layers.** Layer 1 decodes to exactly `0x0B10` bytes, which are another `ashd` file. That file
        decodes to exactly its declared `0x23E0`. Each stream ends at its EOF with no reference before the start.
      - **The payload** is a section-000 script image with version tag `0x80000002`, an older compiler than the
        shipped `0x8000000B`, in the same frame:
        - the stamp `09/18 20:20:10`, author `Unknown`, source `event.src`;
        - a 32-name pool: `init`, `main`, `setpc`, `appear`, `disappear`, `clearpc`, `control`, `コントロール`, and
          `バッシュ00`..`バッシュ23`.
        Its bytecode is not disassembled. Record: [the ashd scheme](../../_index/candidates/uq70-ashd-scheme/README.md).
- [x] **UQ-380.** That these files are never read at run time. A name assembled from pieces, or a request that *(closed — the register row is WITHDRAWN.)*
      is not by name, would escape a literal search; the runtime kind/index trace requested from ASTRA
      (`FABLE-REQ-ASTRA-KIND-INDEX-TRACE`) would close it.

## 8. Related

- [The VBF archive and `st2e` tables](../VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md).
- [PS2 image data formats](README.md).

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full. Published the same
day; the pass is peer review of fresh work.)*

### The negative claim reproduces exactly

Re-run from the archive with independent code: **1,439** `.bin` files, folded to **146** families,
and **20 families / 41 files** with no name in the executable — the page's figures to the file. The
controls `battle_message.bin`, `npcdic.bin` and `musicctrl.bin` are all found.

> **The separator anchor is load-bearing, and that is worth stating on a page whose whole result is
> an absence.** §*Corpus validation* specifies *"the file name **right after `\` or `/`**"*. Drop
> that anchor and the answer becomes **19 families / 39 files**: `ctrl.bin` false-matches **inside
> `musicctrl.bin`** — which is one of this page's own controls. **The control and the false positive
> are the same string.** A substring search would have quietly dropped the four ATEL scripts' parent
> family from the result.

### ⚠ The ten `st2e` families are three different things

§2 calls all ten *"`st2e` table"* and two of them *"a bare 32-byte header"*. Reading each header as
`{magic, count, stride, dataoff}` and comparing `dataoff + count × stride` against the file size:

| family | count | stride | dataoff | header describes | file is | |
|---|--:|--:|--:|--:|--:|---|
| `basic_skill` | 1,345 | 56 | 32 | 75,352 | 75,352 | **exact** |
| `growth_rate` | 128 | 56 | 32 | 7,200 | 7,200 | **exact** |
| `unit_data` | 495 | 84 | 32 | 41,612 | 41,612 | **exact** |
| `actionchip_data` | 0 | 8 | 0 | 0 | 32 | header only |
| `bukitye_data` | **23** | **0** | 0 | 0 | 32 | header only — **but it claims 23 records** |
| `mons_act` | **359** | **0** | 0 | **0** | **11,756** | header describes nothing |
| `mons_category` | 16 | 2 | 32 | 64 | 156 | +92 |
| `mons_race` | 64 | 2 | 32 | 160 | 444 | +284 |
| `object_data` | 66 | 8 | 32 | 560 | 1,708 | +1,148 |
| `target_data` | 1,090 | 8 | 32 | 8,752 | **39,000** | +30,248 |

**Only three of the ten are tables their own header accounts for.** Two claim records with a
**stride of 0**, and `mons_act` puts a header describing **zero** bytes in front of **11,756**. The
"bare 32-byte header" reading is right for both 32-byte files, and `bukitye_data` is not empty *by
count* — it is empty because its stride is zero.

### ⚠ §6's run-time-name attack is live, not closed

§6 reasons that the leaf stems occur nowhere. True — and **every directory segment of every unnamed
family is present in the image as a literal**: `ps2data`, `image`, `ff12`, `bin`, `binaryfile`,
`test_battle`, `katano`, `myoshiok`, `worldmap`. **Only the leaves are missing.** So a path assembled
from a directory literal and a name from a table has all of its prefixes available, and the literal
search cannot narrow `UB-1` further on its own. That is not a defect in the page — §1 and §7 both say
the assembled route is open — but it is the measurement that says *how* open.

**Not claimed.** That any of these files is or is not read at run time — `UB-1` stands untouched, and
`FABLE-REQ-ASTRA-KIND-INDEX-TRACE` is still the thing that would settle its first half. What the five
undecoded families hold. What the surplus bytes in the four over-long `st2e` files are — the arithmetic
is measured, the content is not read. Whether a `stride` of 0 means anything to a reader: **no reader
was found for any of these**, so the header's self-description is all there is. The archive was
**read, never written**, and nothing was executed.


## UQ-380's escape routes, measured (FABLE, 2026-09-16)

**THE BLIND SPOT IS MEASURED, AND IT UPHOLDS THE ROW - 2026-09-16 (FABLE).** This row names its own escape routes, so I tested them rather than the claim. **Two of three results strengthen it and the third confirms the caveat was right to be there.** **(1) The literal half holds.** Across every mapped section: **`logicpack` 0, `filelistlocalin` 0, `event.bin` 0** occurrences. Nothing names them. **(2) `katano` DOES occur - three times - and every one is a false lead worth recording.** They are `__FILE__` strings from assertion macros in the original source tree: `..\..\katano\ateldecode.c` at `009156E8`, `..\..\katano\atelload.c` at `00D10958`, and `..\..\katano\atelareaload.c` at `00D117F8`. **`katano` is a source DIRECTORY, not a data path**, and the referrers are the loader family - `atelload.c` from `ActorResource_BeginPrimaryPayloadLoad` and one further actor-loading body, `atelareaload.c` from `AreaArd_BindLoadedRootAndBattleSections` and `AreaArd_LoadOrUnloadFieldResource`. *(The second actor-loading body is named on the `UQ-380` register row rather than here: naming it on this page would pull in five ActorEntity and Presentation edges this document has no crossing section for, and I am not classifying a crossing I have not read.)* **Anyone re-running the literal search will hit these three and should not chase them.** *(The `atel*` filenames themselves are already carried on four pages, so this is not a new attribution - only a warning about the hit.)* **(3) The composed-name route is narrowed but NOT closed, and that is the honest result.** **No single string in the image carries both a `%` conversion and `.bin`** - so no one-shot `sprintf` can produce a `.bin` name. **But 95 strings have the shape of two-part path assembly**, including bare `%s%s%s` at `008F80C8` and `%s%s` at `008F80F0`, beside worked examples like `./GameData/%s/ArtData/chr/%s_%s.ah`. **A name built as `%s%s` from a stem and a separate `".bin"` literal would leave no trace my test could see.** **So the row's caveat was correct and remains the live half.** What changes: the *literal* search is now confirmed clean over the whole image rather than over a page's sample, the `katano` hit is disarmed, and the composed route is bounded to **two-part assembly specifically** - which is a much more targeted thing for the runtime trace to look for than *a name assembled from pieces*. *What I did not do.* Enumerate which of the 95 assembly sites could reach a `.bin` stem; that needs the callers of each format string, and it is the cheap static step remaining before `FABLE-REQ-ASTRA-KIND-INDEX-TRACE` is worth booking.

**(4) THE CHEAP STATIC STEP IS DONE, AND IT DISPROVES COMPOSITION — 2026-09-20 (SWE2-DATA's census, re-derived
here by FABLE, Claude Opus 5).** SWE2-DATA took exactly the step named above and reports **`can_compose = 0`** over
a **broader** population than mine: **142** format strings carrying two or more conversions including `%s` (my 95
are a subset of theirs), **123** `lea` sites, and every rip-load in the 80-byte argument window before each call —
**no `.bin` piece sits in any format call's argument window, and no `.bin`-loading function coincides with a format
function**. Their supply-side census: a `.bin` pointer can reach a register only by `lea` of the string, by a data
pointer-table slot, or by an immediate, and they count **6**, **12** (all inside the path-registry installer
`002DF9A0` and the two AddMotion loaders) and **zero** respectively.

**I re-derived the load-bearing half with my own instrument rather than carrying the figure.** A regex census of
`.rdata` and `.data` finds **2,144** strings containing `.bin`; a sweep of every listed body for a rip-relative
`lea` whose target is one of them finds **exactly six**, and every one is a **complete filename**: the four
`PackFiles\…_ys.bin` full paths in the path-registry installer, and `./PS2Data/add_motion/SkeletonMapping.bin`
and `./PS2Data/add_motion/HighModelReplace.bin` in the two AddMotion loaders. *(The six site addresses and the
three functions holding them are on the `UQ-380` register row rather than here, for the reason point (2) gives:
naming them on this page pulls in a CoreRuntimeScheduling edge — all three are reached from one boot body — and
this document still has no crossing section to classify it in.)*

A separate sweep of **3,449** large-immediate register loads finds **zero** whose value is the address of a
`.bin` string. *Two instruments, built independently, the same two figures — which is what makes this corroboration
rather than agreement.*

**So the composed-name route is closed for every piece the code can supply.** Each one is already a whole path, and
the five stems (`logicpack`, `filelistlocalin`, the two `_name` tables, `event`) occur nowhere, so `%s%s` of a stem
and a `".bin"` literal cannot produce any of the five families. **Point (3)'s live half is therefore narrower than
it was**: not "a name assembled from pieces", but **a name built byte by byte in a buffer at run time**.

**SWE2-DATA's own limit is the right one to keep:** pointer dataflow through memory is unbounded statically, so a
table pointer could reach an argument register without a rip-load — but what it points at is a complete existing
path, so that route cannot manufacture a new name either.

**Which sharpens the runtime ask.** `FABLE-REQ-ASTRA-KIND-INDEX-TRACE` is now worth booking with a different
target: **not "watch for composed names", but "watch the request path by kind and index" — on this evidence a
request for one of the five families would carry no name at all.** *(The census artifact is SWE2-DATA's and sits
beside this page as `members/bin-assembly-census.tsv` with generator `gen_bin_assembly_census.py`; it is theirs to
commit, and this section does not carry it.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **CoreRuntimeScheduling — CLIENT (1 edge).** 1 inbound (CoreRuntimeScheduling bodies `0022A0B0` call page-cited `002DF9A0`). Substantive edges include `002DF9A0` is called by `0022A0B0`.
