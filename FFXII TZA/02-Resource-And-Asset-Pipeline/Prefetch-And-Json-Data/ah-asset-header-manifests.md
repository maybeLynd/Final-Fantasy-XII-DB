---
system: .ah — the D3D11 asset-header manifests
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: PrimaryOwner:Resource
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
corpus_validated: "2,564 .ah in the archive index; leading signature '/Gam' in 12 of 12 sampled; no file opened — see section 5"
last_reviewed: 2026-09-05
archive_formats:
  - "ah"
audit:
  passes: 2
  last_pass: 2026-09-13
  last_pass_state: opus-ah-manifests-pass-2 - all 2,564 files opened; two leading signatures not one; 142,481 tokens; 62 non-path tokens in five fontlist.ah; the _srm list is parallel, not a subset; the npc shadow gap is two out and one in
  crossref_clean: true
  reopened_count: 0
---

# `.ah` — the D3D11 asset-header manifests

> One `.ah` beside every model, map and font in the remaster's art tree: **an ordered, whitespace-
> delimited list of the `.phyre` files that make up that asset.** 2,564 files and 11.7 MB — the
> smallest large family in the archive, and the index the renderer actually goes through.

**Corpus validation.**

| | |
|---|---|
| files | **2,564**, 11.7 MB — all under `gamedata/d3d11/artdata` |
| leading signature | ~~**`/Gam` in 12 of 12 sampled** — a single signature~~ **two signatures over all 2,564 (§7): `/Gam` in 2,559 and `font` in 5** |
| largest groups | `chr/weapon` 308 · `chr/monster` 254 · `chr_shadow/monster` 249 · `chr/npc` 172 · `chr_shadow/npc` 171 · `chr/gadget` 103 |
| naming | `<asset>_d3d11.ah` and a `_d3d11_srm.ah` variant beside it |
| **files opened** | ~~none~~ **all 2,564, 2026-09-13 (§7)** — **142,481** tokens, **12.2 MB** |

---

## 1. What the player sees

Nothing, directly — and everything, indirectly. **Every character, weapon, monster and map in the
remastered art path is assembled from a list held in one of these files.** A modder replacing a
model's `.phyre` meshes is editing files that a `.ah` names; **if the name is not in the list, the
renderer never asks for it.**

The `chr_shadow` tree is the tell that these are render-side rather than gameplay-side: the same
asset appears twice, once for itself and once for the geometry that casts its shadow.

## 2. The layout

**There is no binary structure.** A `.ah` is plain text, and the parser reads it as
**whitespace-delimited tokens** — the same idiom the prefetch manifests use, with the same format
string at `0x008F4438` (`"%s"`), and one difference that matters (§3).

Each surviving token is a path. **Order is significant and the engine records it**: every entry
stores its own position in the list as a `u16` (`0x0019E88C` `SAR RAX,0x3`, `0x0019E890`
`MOV word ptr [R9],AX` — the byte distance from the list base divided by 8, i.e. the entry's index).

```struct AhListEntry base=record size=0x03
+0x00  u16     index    the entry's ordinal in the file, computed not stored in the text
+0x02  byte    _pad     the name begins at +0x03, so the string is not aligned
```

**The token itself follows at `+0x03`, NUL-terminated and variable-length**, so it is stated here
rather than fenced: `FORMAT.md` §2's grammar admits only a literal `[N]`, and inventing a length the
data does not have to satisfy `check_layouts.py` would be the token-satisfaction failure. *(I hit
this gap myself after flagging it for another session two rounds ago — the remedy is the one
`repos-c7` proposed: fence the fixed part, put the repetition in prose.)*

The remaining fields of the entry are the manager's, not the file's: `+0x108` in the request holds
the list cursor and `+0x110` its end, and the entry's `+0x88` is a back-pointer to the request that
produced it. **Nothing in the text encodes a count, a size or a type** — the file is exactly a list.

## 3. The loader contract

### The parser — `FUN_0019E7B0`

Reached as the completion callback of an async load: `FUN_0019EB60(mgr, path)` builds a request
record, stamps it kind **4**, plants `FUN_0019EF20` as the callback and submits it via
`FUN_001A0BB0`. `FUN_0019EF20` is a five-instruction thunk that tail-jumps to `0x0019E7B0`
(`0x0019EF2D`), which is where the file is actually consumed.

```
0019e808  LEA  RDX,[0x008F4438]     ; "%s" — the same format the prefetch parser uses
0019e80f  CALL 0x0018A330           ; scan one whitespace-delimited token
0019e814  CMP  EAX,0x1              ; exactly one field, or stop
0019e88c  SAR  RAX,0x3              ; (cursor - base) / 8
0019e890  MOV  word ptr [R9],AX     ; store the entry's ordinal
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| any token | `0x0019E80F`, `"%s"` | scan returns ≠ 1 → the walk stops at `0x0019E814` | — | — |
| the request's buffer pointer | `+0x120` of the request | null → the list is closed empty and a flag set at `+0x128` | — | — |
| a token beginning `##` | — | — | — | **not filtered — see below** |

> ### The one difference from the prefetch manifests, and it is the interesting half
>
> **The prefetch parser discards any token beginning `##`** (`0x001DA186` / `0x001DA18B`, freed at
> `0x001DA194`). **The `.ah` parser has no such test.** Checked across all **135** instructions of
> `FUN_0019E7B0`: **zero occurrences of a `0x23` comparison.**
>
> **So the two manifest families share a scanner and not a grammar.** A `.ah` has no comment
> convention: a `#`-prefixed line would be taken as an asset path, requested, and missed. **A modder
> cannot annotate a `.ah` the way they can a prefetch list**, and that is a loader fact no amount of
> reading the shipped files would reveal — every shipped `.ah` simply happens not to contain one.

**Termination is by scan failure, not by length.** A malformed tail truncates the list silently.

**What loading normalises:** nothing. The token is copied verbatim to `entry+0x03`.

### Where `.ah` paths are built — five sites, five asset classes

| what | function | format string |
|---|---|---|
| map | `FUN_001A7A50` | `.\GameData\%s\ArtData\map\%s\%s_%s.ah` and `…_srm.ah` (`0x008F65B0`, `0x008F6580`) |
| font | `FUN_001B44A0` | five literal `./GameData/D3D11/ArtData/font/<lang>/fontlist.ah` — `jp` `us` `ch` `cn` `kr` only |
| character | `FUN_001BB2B0`, format loaded at `0x001BB7B7`; also `FUN_001BB920` | `./GameData/%s/ArtData/chr/%s_%s.ah` (`0x008F9158`) |
| character shadow | same two, at `0x001BB82D` and `0x001BB87E` | `./GameData/%s/ArtData/chr_shadow/%s_%s.ah` (`0x008F9180`) **and** a nested `…/%s%s/%s_%s.ah` (`0x008F91B0`) |
| procedural texture | `FUN_001BE730` | `./GameData/%s/ArtData/map/proceduralTexture/proceduralTexture_%s.ah` (`0x008F99D0`) |

**The `%s` that varies is always `"D3D11"`**, passed as a literal at every character-path site — so
the remaster's art root is a formatted parameter that only ever takes one value. **The two
`chr_shadow` forms are the flat and nested directory layouts** — `chr_shadow/<name>` versus
`chr_shadow/<group>/<name>` — matching the `n12/n1248` grouping the archive uses.

**Only five languages have a `fontlist.ah`** (`jp`, `us`, `ch`, `cn`, `kr`) against nine locale trees
elsewhere. Recorded, not explained. *Narrowed 2026-09-13:* the font builder `001B44A0` does not need more —
it maps language values `1`–`6` to the `us` list, `7` to `kr`, `8` to `ch`, `11` to `cn` and every other value to
`jp` ([font kerning and expansion](../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md) §3);
which in-game language each value is remains `KE-1`.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x0019E7B0` | `FUN_0019e7b0` — **the `.ah` parser**; token scan `0x0019E80F`, ordinal store `0x0019E890` | ✅ |
| `0x0019EF20` | the 5-instruction completion thunk; tail-jump at `0x0019EF2D` | ✅ |
| `0x0019EB60` | `FUN_0019eb60` — builds the request, kind `4`, plants the callback | ✅ |
| `0x008F4438` | `.rdata` — the `"%s"` token format, **shared with the prefetch parser** | ✅ |
| `0x001BB2B0` | `FUN_001bb2b0` — the character asset-header path builder; format loaded at `0x001BB7B7` | ✅ |
| `0x001A7A50` · `0x001B44A0` · `0x001BE730` | map, font and procedural-texture path builders | partial |
| `0x008F9158` · `0x008F9180` · `0x008F91B0` · `0x008F65B0` · `0x008F99D0` | `.rdata` — the five path formats | ✅ |
| `0x0018A330` | the token scanner both manifest families call | ❌ entry only |

## 5. Corpus survey

**No `.ah` file was opened.** `gamedata/d3d11` is not in the local extraction and no `.vbf` exists on
this machine. The corpus column is the archive index plus the frozen leading-signature census, which
gives **one signature, `/Gam`, in 12 of 12 sampled** — consistent with a file whose first token is a
`/GameData/…` path, and the strongest single corpus fact available here.

~~**What that costs:** the token count per file is unmeasured, and so is whether any shipped `.ah`
contains a token that is *not* a path — the parser would accept it and request it as one. The
`_srm` variant's relationship to its base file is likewise unestablished~~ — **all three measured
2026-09-13 (§7): 142,481 tokens over 234 distinct counts (1 to 407); **62 non-path tokens**, all
in the five `fontlist.ah`; and the `_srm` list is a **parallel** list, not a copy or a subset.**
**It is a separate file with its own path format (`0x008F6580`), not a section of the other.**

**A distribution fact worth keeping:** `chr_shadow` mirrors `chr` closely but not exactly — 249
shadow files against 254 monster files, 171 against 172 npc. **Five monsters and ~~one npc~~ *two*
npcs have no shadow asset header — and one shadow has no npc** (corrected 2026-09-13, §7: the
counts differ by one, the *sets* differ by two out and one in). Not investigated further, and it is
the kind of near-miss that is either an authoring gap or a deliberate exclusion.

## 6. Falsification pass — 2026-09-05

| attack | result |
|---|---|
| Is `FUN_0019E7B0` really the `.ah` parser, or a generic text reader? | It is reached only through the callback planted by `FUN_0019EB60`, and `FUN_0019EB60` is what every `.ah` path builder calls after formatting its path. **It is generic in shape and `.ah`-specific in reachability**, and this sheet claims only the latter. |
| Is the missing `##` filter a real difference or an artefact of where I looked? | **Checked over all 135 instructions of the function, not a sample: zero `0x23` comparisons.** The positive control is the prefetch parser, where the same search finds two, at `0x001DA186` and `0x001DA18B`. |
| Could the decompiler have invented the ordinal store? | **No — and the decompiler hid something else.** It inlined `FUN_0019EF20`, so the parser appeared to be part of the callback; the listing shows a 5-instruction thunk tail-jumping to `0x0019E7B0`. The `SAR`/`MOV word` pair is read from the listing. |
| Does the claim rest on a file? | **No file was opened.** §2 and §3 are the parser's own behaviour; §5 says what that leaves unmeasured. |
| Is `"D3D11"` really always the format argument? | Observed as a literal at the character sites. **The map and font builders were not read in full**, so "always" is scoped to what §3 cites. |

**The killer observation** for *"a `.ah` is exactly a token list"* would be a second consumer that
reads the same buffer with a different grammar, or a field in the entry populated from the text
rather than computed. Neither appears in `FUN_0019E7B0`; no wider search was run.

## 6b. Independent audit pass — 2026-09-06, `repos-1e`

**Method.** `FUN_0019E7B0` and the thunk `FUN_0019EF20` re-decoded with capstone; every cited string
address resolved from the image; the archive index re-read. Program state: GN160 (`gzf fa0db293…`).

**Every cited address and every string reproduces.**

| cited | claim | decoded |
|---|---|---|
| `0x0019E808` | the `"%s"` format | `lea rdx, [rip + 0x755c29]` → **`0x008F4438` = `'%s'`** |
| `0x0019E80F` | scan one token | `call 0x18a330` |
| `0x0019E814` | scan ≠ 1 → stop | `cmp eax, 1` |
| `0x0019E88C` | `SAR RAX,3` | `sar rax, 3` |
| `0x0019E890` | store the ordinal as `u16` | `mov word ptr [r9], ax` |
| `0x0019EF2D` | the thunk tail-jumps to the real parser | `jne 0x19e7b0`, in a **5-instruction** function |

**The two central claims are confirmed by counting, not by reading.**

- **`FUN_0019E7B0` is 135 instructions** — decoded count **135**, matching exactly.
- **Zero comparisons against `0x23` in it** — I enumerated every immediate operand across all 135
  instructions and found **none**. So the `.ah` parser genuinely has no `##` filter.

**And the "same scanner, different grammar" result is exact at the address level:** both parsers
`call 0x18a330` with the format string at **`0x008F4438`** — *the same address*, not merely the same
literal. The whole difference between the two grammars is the pair of byte compares the prefetch
parser has at `0x001DA186`/`0x001DA18B` and this one does not.

**All five path builders' format strings resolve as cited**, including the nested shadow variant:
`0x008F9158` `./GameData/%s/ArtData/chr/%s_%s.ah`, `0x008F9180` `…/chr_shadow/%s_%s.ah`,
`0x008F91B0` `…/chr_shadow/%s%s/%s_%s.ah`, `0x008F65B0` `.\GameData\%s\ArtData\map\%s\%s_%s.ah`,
`0x008F6580` the `_srm` variant. **Note the separator split — the `chr` builders use `/` and the
`map` builders use `\`** in the same binary, which the sheet's table shows but does not remark on.

**Corpus:** **2,564** `.ah` entries, **11.7 MB**, **all** under `gamedata/d3d11/artdata` — exact.

**What was attacked and held.** (a) That the thunk might do work the sheet attributes to the parser —
it is five instructions, a null test and a tail jump, nothing else. (b) That the ordinal store might
be wider than `u16` — `mov word ptr` settles it. (c) That "no `##` filter" might be a scan of the
wrong function — the instruction count matches the sheet's own 135, so both readings are of the same
body.

**Not audited:** which callers actually reach each of the five builders, and the `fontlist.ah`
locale-coverage claim.

## 7. What this document does not claim

- **What the requested paths are used for.** The entries are handed on by the manager; the consumer
  of the assembled list was not read.
- **The `_srm` variant's meaning.** A separate file with its own path format, nothing more.
- **Request kind `4`.** The constant is stamped at `FUN_0019EB60`; the dispatch that interprets it
  was not read.
- **Why only five languages have a `fontlist.ah`** — narrowed in §3: five lists serve every language value.
- **The five monster and one npc assets missing a `chr_shadow` header** — counted, not explained.
- **Anything measured from a `.ah` file**, for the reason in §5.

## 8. Related

- [`how-the-prefetch-manifests-are-read.md`](how-the-prefetch-manifests-are-read.md) — the other
  token-scanned manifest family; **same scanner, same format string at `0x008F4438`, different
  grammar** — that one filters `##`, this one does not
- [`README.md`](README.md) — the folder census
- [`../../25-EBP-Script-Container/Sections/section-012.md`](../../25-EBP-Script-Container/Sections/section-012.md)
  — the per-map actor manifest whose class letters (`c` `n` `m` `g` `b` `s` `t` `w`) name the very
  `artdata/chr/<class>` directories a `.ah` sits in
- [`../../_index/ASSET-FORMATS.md`](../../_index/ASSET-FORMATS.md) §8 item 7 — where `ah` sits in the build order

## 7. Falsification pass 2 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one address at a time and read in full.)*

§5 was written with no archive on the machine and listed three things that cost. **There is an
archive now, and all 2,564 files were opened.**

### ⚠ There are two leading signatures, not one

| | §5 | measured over all 2,564 |
|---|---|---|
| files | 2,564 | **2,564**, all under `gamedata/d3d11/artdata` |
| bytes | 11.7 MB | **12.2 MB** |
| leading signature | **`/Gam` in 12 of 12 sampled — "a single signature"** | **`/Gam` in 2,559 and `font` in 5** |

The five are the `font/<lang>/fontlist.ah` files. **A twelve-file sample found one signature because
the other one is 0.2 % of the corpus** — which is what a sample of twelve can be expected to miss,
and is worth recording as the cost rather than as a failure of the census.

### ✔ The three unmeasured things, measured

**Token counts.** **142,481** tokens over the corpus, in **234** distinct per-file counts, from **1**
to **407**. The commonest are 4 (635 files), 6 (544), 9 (127), 12 (86), 15 (46).

**Non-path tokens — yes, 62 of them.** Every token in 2,559 files starts with `/` and ends `.phyre`
(**142,419** of them). The remaining **62** are in the five `fontlist.ah` and are **font names**, not
paths: `fontex_expand`, `fontex_subtitle`, `font00`, `font_bookman`, `font_iwa_g12` and the rest.
§5's worry — *"the parser would accept it and request it as one"* — has five concrete files behind
it now.

**The `_srm` relationship.** **457** `_srm.ah` against 2,107 base files, and **every one of the 457
has a base file of the same stem**. Their token lists are **identical in 6**, a **subset in 0**, and
**no pair shares zero tokens**. Median base **127** tokens, median `_srm` **127**, **median shared 21**.
So `_srm` is **a parallel list of the same size that overlaps its base by about a sixth** — neither a
copy, nor a subset, nor an unrelated file.

### ⚠ The shadow near-miss is itself a near-miss

§5 reads the difference off the counts. Compared as **sets**:

| | base | shadow | in base, no shadow | in shadow, no base |
|---|--:|--:|---|---|
| `chr/monster` ↔ `chr_shadow/monster` | 254 | 249 | **5** — `m1003`, `m1055`, `m1136`, `m1137`, `m1188` | **0** |
| `chr/npc` ↔ `chr_shadow/npc` | 172 | 171 | **2** — `n1021`, `n1189` | **1** — `n1174` |

**The five monsters are exact.** The npc line is not: 172 − 171 = 1 is a subtraction, and the sets
say **two npcs have no shadow header and one shadow header has no npc**. A difference of counts is
not a difference of sets, and here they disagree.

**Not claimed.** Why those assets lack a shadow header — still not investigated, only enumerated.
What the 62 font tokens resolve to, or whether the parser really requests them as paths: §3's reader
was not re-run against them. What the ~21 shared tokens in an `_srm`/base pair have in common. The
archive was **read, never written**, and nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE.** Cited manifest functions are called by Presentation bodies of 1,220, 1,248 and 1,636 bytes, and one calls a 485-byte Presentation body.
- **Save_Load_Settings — CLIENT (3 edges).** 3 inbound (Save_Load_Settings bodies `SaveloadManager_RequestDisableAutosaveList` (001C1810) call page-cited `001A0A90`, `001A0BB0`, `001A1220`). Substantive edges include `001A0BB0` is called by `SaveloadManager_RequestDisableAutosaveList` (001C1810); the remaining edges run through shared helpers the page cites.
## Interior citation — frontier hub `0018A330` (2026-09-18, SWE2-EC7)

`0018A330` — 79 B, 8 A-measured callers; the token scanner both manifest families call
(entry-only above, now read). Interior verified: `0018A320()` returns the shared globals
pointer, `rsi` points at the caller's `0x60`-byte stack token record, and the scan itself is
the indirect call at [`0018A371`](../../_index/ADDRESS-INDEX.md) — `rcx = [rax]` (the scanner object), `rdx = rdi`
(the source cursor), `r8 = -1`, `r9 = rbx` (the terminator set), invoked through the
`008C2ED8` IAT slot. The manifest loop's whitespace-token step is a
single table-slot call, not inlined scanning.
## SWE2-EC7-32 update (2026-09-18) — `0019EB60` kind-4 node factory

`0019EB60` (210 B) is the enlist the manifest code runs:
`001BA860(obj+8)` resolves the arena, the caller's string copies
into it, then a `001A1220`/`001A0A90`-allocated node is stamped
— `+0` = 4 (the kind), `+8` = `0019EF20` (the handler), `+0x10` =
the arena base, `+0x18` = 1, `+0x20` = a second string copy —
`+0x120` self-links, and `001A0BB0(alloc, node, 0)` enlists it.
Interior anchor `0019EC14` (the `call 001A0BB0` insert).

## SWE2-EC7-39 update (2026-09-19) - `001BE730`

`001BE730` (403 B) is the procedural-texture path builder the page names - `01F44830`, `"./GameData/%s/ArtData/map/proceduralTexture/proceduralTexture_%s.ah"`, `001EDF00` quintuple plus `0017D2E0`/`0019EF80`/`0019EB60`/`0019C5D0`/`00808C40`. Interior anchor `001BE78B` (an `001EDF00` call).
