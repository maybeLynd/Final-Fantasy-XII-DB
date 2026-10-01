---
system: The prefetch manifests — how FileCachePrefetchManager reads them
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
corpus_validated: "9,351 prefetchdata entries across 9 languages, archive index, 2026-09-05; no file opened — see section 5"
last_reviewed: 2026-09-05
archive_formats:
  - "txt"
audit:
  passes: 1
  last_pass: 2026-09-06
  last_pass_state: GN160-code-and-index-reparse-repos-1e — FUN_001DA0F0 re-decoded, all 7 cited addresses exact; corpus 9,351 entries / 283,340,853 B and Total_data_Size 0 occurrences confirmed
  crossref_clean: true
  reopened_count: 0
---

# The prefetch manifests — how `FileCachePrefetchManager` reads them

> One flat list of asset paths per scene, read at game start and at every map entry, to pull files
> into the file cache before anything asks for them. **This sheet answers the question the folder
> README left open: the engine does *not* read the `##Total_data_Size` budget. It throws that line
> away.**

**Corpus validation.**

| | |
|---|---|
| entries under `prefetchdata/` | **9,351**, 283,340,853 B |
| languages | **9** — `ch` `cn` `de` `es` `fr` `it` `jp` `kr` `us`, 1,036–1,042 files each |
| per language | `common.txt` ×1 · `eventList.csv` ×1 · `events/` ×329 · `maps/` ×709 |
| outside the language trees | 2 — an `add-on/` file and `ff12mapjump_custom_nocrystal.csv` |
| **files opened for this sheet** | **none — see §5** |

---

## 1. What the player sees

Loading that does not happen. When you walk through a zone exit, the assets for the next map have
often already been pulled into memory, so the transition is short. That is what these files buy.

**For a modder the consequence is sharper: a replaced asset that is not named in the manifest for
the scene that uses it may never be prefetched.** It will still load on demand, but the streaming
hint that was hiding the cost is gone.

## 2. The layout

A manifest is **plain text with no structure beyond whitespace**. The engine does not read lines,
columns or sections — it reads **whitespace-delimited tokens**, one at a time, to the end of the
buffer. Each token that survives the filter in §3 is treated as an asset path.

The `##Total_data_Size:_361_MB` header that opens each file is, to the parser, **one token** — and
that is not an accident:

> **The underscores in the header are load-bearing.** Written with spaces, `##Total_data_Size: 361
> MB` would be split by `"%s"` into four tokens; only the first begins `##`, so `361` and `MB` would
> survive the filter and be handed to the file cache as asset paths. **Written with underscores it
> is a single token, discarded whole.** The header's odd punctuation is what makes it inert.

`eventList.csv` is a different shape in the same tree — four comma-separated integers per record —
and is covered in §3 because the same subsystem reads it.

## 3. The loader contract

### The parser — `FUN_001DA0F0(cache, buffer, outList)`

**The whole of the manifest format is this one function.**

```
001da12e  CALL 0x00210EC0                    ; allocate a 0x100 token buffer
001da136  LEA  RDX,[0x008F4438]              ; the format string, "%s"
001da143  CALL 0x0018A330                    ; scan one token
001da148  CMP  EAX,0x1
001da14b  JNZ  001da1ef                      ; not exactly one field -> stop, free, return
001da186  CMP  byte ptr [RBX],0x23           ; token[0] == '#'
001da189  JNZ  001da19b                      ;   no  -> keep
001da18b  CMP  byte ptr [RBX + 0x1],0x23     ; token[1] == '#'
001da18f  JNZ  001da19b                      ;   no  -> keep
001da194  CALL 0x00210EB0                    ; yes -> FREE the token; it never reaches the list
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| any token | `0x001DA143`, `"%s"` at `0x008F4438` | scan returns ≠ 1 → parse stops at `0x001DA14B` | — | — |
| a token beginning `##` | tested at `0x001DA186` / `0x001DA18B` | — | — | **yes — freed at `0x001DA194`, never appended** |
| every other token | appended to the list at `0x001DA19B` | — | — | — |

> ### The row's question, answered
>
> **`##Total_data_Size:_N_MB` is discarded, not parsed.** There is no numeric conversion of it
> anywhere in the subsystem: the byte pair `0x23 0x23` is tested and the token is handed straight to
> `free`. **No allocation is sized from it, no budget is reserved, no comparison is made against it.
> It is a build note that the parser is written to skip.**
>
> **The corroborating negative is stronger than usual because the string is absent too:**
> `Total_data_Size`, `##Total` and `Total_data` occur **0 times in the whole executable**, while the
> controls in the same scan — `effect_finish` (30), `atelload.c`, `SRYK` — are all found. **The
> engine holds no copy of that header's name, and the only code that could see it throws it away.**

**Termination is by token, not by size.** The loop stops when the scan returns anything other than 1
(`0x001DA14B`), so a malformed tail truncates the list silently rather than failing the file.

### Where the manifests are read from

| when | function | builds |
|---|---|---|
| game init | `FUN_001DA610` — logs `[FileCache] Prefetch On Init Game Begin` at `0x001DA647` | `<lang>/PrefetchData/common.txt`, then calls the parser at `0x001DA7F6` |
| map entry | `FUN_001DA290` — logs `[FileCache] Prefetch On Enter Map(%d %s) Begin` at `0x001DA4CC` | `…/Maps/` + name + `.txt` (`0x001DA53F`) |
| event list | `FUN_001D9A40` — logs `[FileCache] Init Event Prefetch List` at `0x001D9A78` | `<lang>/PrefetchData/eventList.csv` |

**CORRECTED 2026-09-21 (SWE2-DATA; `FABLE-CONTRA-PREFETCH-SELECTOR-IS-ZERO-NOT-FIVE` +
`FABLE-AMEND-PREFETCH-SELECTOR-NARROWS-THE-CORRECTION`, verified against the shipped image):**
the two sites this paragraph originally cited are the opens of the **manifest files**, not of the
tokens — `0x001DA758` opens `common.txt` and `0x001D9B75` opens `eventList.csv`, and both pass
selector **0** (`xor r8d,r8d` at `0x001DA74C` and `0x001D9B6A`). The per-token request is the
loop at `0x001DA810`–`0x001DA83F` inside `FUN_001DA610`: it walks the parsed token list and calls
`FUN_00597970(token, 5)` per node (`mov r8b, 5` at `0x001DA810`; `call` at `0x001DA81B`), then
`0x0059BD40` (frees the stream's `+0x30`, releases the `+0x40` handle) and `0x00598100` (the
stream destructor) — construct, tear down, destroy, **never read**: a prefetch token is a
resolve-and-mark, not a fetch of bytes. `eventList.csv` records are `%d,%d,%d,%d` quads and get
no per-record request at all. An independent census of every `0x00597970` (18) and `0x00597930`
(2) call site — raw `E8` scan of `.text`, selector read from the `r8` setup — gives selector 0
five times (`0x001D8DC2`, `0x001D9B75`, `0x001DA758`, `0x001DAA05`, `0x00677076`), 1 eleven times
plus two flag-derived sites (`setne r8b` at `0x001D6F4D`, `movzx r8d, r9b` with `r9b=1` at
`0x006CCB53`), 5 once (`0x001DA81B` — the token loop), and `lea r8d, [r14+3]` once (`0x001DAFD8`,
where `r14b` ∈ {0,1} is the function's own flag — i.e. 3 or 4; **not** 24 as the filing's figure
had it). **The manager object itself is
named `FileCachePrefetchManager` (`0x009005E8`), referenced once, from `FUN_001DAAC0`.**

**`eventList.csv` uses the same `##` convention and a different body.** `FUN_001D9A40` scans each
record with `"%d,%d,%d,%d"` (`0x001D9C13`) and **accepts it only if all four fields convert**;
a record beginning `##` is skipped by the same byte-pair test. **Two file kinds, one comment
convention, two payload grammars** — which is why this sheet declares `txt` and not `csv`: the
`soft_particle` and `jsondata` CSVs were not read and share nothing but an extension.

**Path case does not match the archive.** The engine builds `/PrefetchData/` (`0x00900648`),
`/Maps/` (`0x009006B0`) and `/common.txt` (`0x00900638`) with capitals; the archive stores
`prefetchdata/us/maps/…` in lower case. **Lookup is therefore case-insensitive somewhere below this
layer** — not established here, and named in §7.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x001DA0F0` | `FUN_001da0f0` — **the manifest parser**; `##` test at `0x001DA186`, discard at `0x001DA194` | ✅ |
| `0x008F4438` | `.rdata` — the `"%s"` token format | ✅ |
| `0x0018A330` | the scan routine the parser calls | ❌ entry only |
| `0x001DA610` | `FUN_001da610` — `common.txt` at game init; parser call at `0x001DA7F6` | ✅ |
| `0x001DA290` | `FUN_001da290` — per-map manifest on map entry | ✅ |
| `0x001D9A40` | `FUN_001d9a40` — `eventList.csv`; `"%d,%d,%d,%d"` at `0x001D9C13` | ✅ |
| `0x001DAAC0` | `FUN_001daac0` — the only reference to `FileCachePrefetchManager` | partial |
| `0x00597970` | the file-cache request — opens the two manifest files (selector 0) and resolves each `common.txt` token (selector 5, per-node in the `0x001DA81B` loop) | ❌ entry only |
| `0x009005E8` … `0x009006E8` | `.rdata` — the ten-string `[FileCache]` cluster | ✅ |

## 5. Corpus survey

**No manifest file was opened.** `prefetchdata` is not in the local extraction and no `.vbf` exists
on this machine, so the corpus column here is the archive index and the header form already recorded
in this folder's README. **Every claim in §2 and §3 is read from the parser**, which is the stronger
of the two sources for a grammar — it is what the engine actually does — but it cannot tell you what
the shipped files contain.

**What that costs, specifically:** the distribution of token counts per manifest is unmeasured, and
so is whether any shipped manifest contains a second `##` line, a blank file, or a token that fails
the `%s` scan and truncates the list. **The parser tolerates all three silently**, so a corpus pass
is the only way to know if any file exercises them.

Per-language counts are near-identical (1,036–1,042), and the three smallest — `ch`, `cn`, `kr` at
1,036 — are the same three trees that differ elsewhere in the archive. Not investigated.

## 6. Falsification pass — 2026-09-05

| attack | result |
|---|---|
| Does anything read the budget? | **No.** The only code that sees the token frees it (`0x001DA194`). No `atoi`/`strtol`/scan of it exists in the subsystem, and the literal `Total_data_Size` is absent from the whole image while the controls in the same scan are found. |
| Is the `##` test on lines or tokens? | **Tokens.** The scan at `0x001DA143` uses `"%s"`, which is whitespace-delimited; nothing in the function looks for `\n`. This is why the header's underscores matter. |
| Could the decompiler have invented the discard? | **No — checked against the listing.** `0x001DA186`/`0x001DA18B` are two literal `CMP byte ptr …, 0x23` and `0x001DA194` is a `CALL` to the allocator's free entry, on the taken path. |
| Is `FUN_001DA0F0` really used for the manifests, or only somewhere else? | `FUN_001DA610`, the `common.txt` loader, calls it at `0x001DA7F6` with the file buffer it just read. |
| Is absence of the string being used as evidence? | **No, and this is the trap `ASSET-FORMATS.md` §5 names.** The absence corroborates; **the finding rests on the `free`**, which is positive evidence of discard rather than absence of a reader. |

**The killer observation** for *"the budget is never read"* would be a numeric conversion of the
token anywhere in the subsystem, or a second parser that consumes manifests without the `##` filter.
The first does not exist in `FUN_001DA0F0`; the second was not searched for beyond the eight
functions in the `[FileCache]` string cluster.

## 6b. Independent audit pass — 2026-09-06, `repos-1e`

**Method.** `FUN_001DA0F0` re-decoded with capstone from `functions.tsv` bounds; every cited address
checked for boundary *and* content; the archive index re-read. Program state: GN160
(`gzf fa0db293…`).

**Every cited address is an instruction boundary and does what the sheet says.**

| cited | claim | decoded |
|---|---|---|
| `0x001DA12E` | allocate a `0x100` token buffer | `call 0x210ec0` |
| `0x001DA136` | the `"%s"` format | `lea rdx, [rip + 0x71a2fb]` → **`0x008F4438` = `'%s'`** |
| `0x001DA143` | scan one token | `call 0x18a330` |
| `0x001DA14B` | scan ≠ 1 → stop | `jne 0x1da1ef` |
| `0x001DA186` | `token[0] == '#'` | `cmp byte ptr [rbx], 0x23` |
| `0x001DA18B` | `token[1] == '#'` | `cmp byte ptr [rbx + 1], 0x23` |
| `0x001DA194` | free the token | `call 0x210eb0` |

**The headline result holds, and it is positive evidence.** The `##` token is not merely skipped —
it is passed to `0x210eb0`, the deallocator, at `0x001DA194`, so it is destroyed rather than parsed.
**The budget line cannot be read because the only thing done with it is to free it.**

**Corpus, re-measured from the archive index:** entries under `prefetchdata/` = **9,351**, total
**283,340,853 bytes** — both exact to the digit. And **`Total_data_Size` occurs 0 times in the
image**, so no code anywhere names the field, which is the complementary negative the sheet pairs
with the `free`.

**What was attacked and held.** (a) That the `##` test might be a *prefix* test that also matches a
single `#` — it is two separate byte compares, `[rbx]` and `[rbx+1]`, so a lone `#` token is
appended like any other. (b) That the "underscores are load-bearing" argument might be inference —
it follows from the scanner being `"%s"`, which is whitespace-delimited by definition, and the format
string address resolves to a literal `%s`. (c) That the sheet might have mistaken a *skip* for a
*free* — `0x210eb0` is reached by `call`, not by a branch around the append.

**Not audited:** the JSON-side material in §5 and the `FileCachePrefetchManager` call graph beyond
the parser itself.

## 7. What this document does not claim

- **What the selector byte means.** It is *not* `5` at every site — CORRECTED 2026-09-21
  (SWE2-DATA): selector 0 opens the two manifest files and three other resources, 5 is passed
  exactly once — `0x001DA81B`, the per-token prefetch request — 1 marks the common open path
  (11 literal sites + two flag-derived), and `0x001DAFD8` computes `r14+3` (3 or 4) for its
  request. FABLE's sweep finds
  `0x0059EE90` branching on the byte at `0x0059EF38` — selector 0 takes the MD5 package route,
  non-zero the djb2 index route; what `5` stamps on the resolved entry is still unestablished.
  This sheet stops at "handed to the file cache".
- **Where case-insensitive path lookup happens.** The engine's literals are capitalised and the
  archive's are not; the resolution layer was not read.
- **Whether the manifests are complete or advisory** — i.e. what happens to an asset a scene uses
  that its manifest omits. That is the question a modder actually has, and it needs the file-cache
  miss path, not this parser.
- **`events/` (329 files per language).** Named by the census; the loader for that subdirectory was
  not distinguished from the `maps/` path in this block.
- **`csv` as a format.** Only `eventList.csv`'s grammar was read. The `soft_particle` and `jsondata`
  CSVs share an extension and nothing else, and `csv` is deliberately **not** declared.
- Anything measured from a manifest file, for the reason in §5.

## 8. Related

- [`README.md`](README.md) — the folder census, and the `##Total_data_Size` header this sheet resolves
- [`../../_index/ASSET-FORMATS.md`](../../_index/ASSET-FORMATS.md) §5 — dispositions and the
  presence-is-evidence-absence-is-not rule this sheet obeys in §6
- [`../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md`](../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md)
  — the other format read this round; there the magic is a version selector, here the `##` is a
  discard filter, and both are loader facts a file corpus alone cannot produce

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Input — CLIENT.** A 162-byte function this page cites is called by a 1,396-byte Input body.
- **Audio — CLIENT.** `0059F4A0` (the release body this page measures) is
  also called by `00225BA0`, an Audio-layer body - the same
  handle-or-buffer release pair serves the audio close path.

**Platform — SERVICE (SWE2-EC7-158, 1 edge).** `001DADC0` — one of this page's manifest-family callers of `001D6B20`/`001D6B90` — calls the platform layer's `005CC930`; a single consult, not a shared responsibility.

**WorldAreaField — SERVICE (SWE2-EC7-158, 2 edges).** `001DA220` and `001DA970`, both callers of this page's `001D6B20`/`001D6B90` thunks, reach the world layer's `00265270` — the manifest readers consult it, nothing more.

**CoreRuntimeScheduling — CLIENT (SWE2-EC7-169, 1 edge).** `00214C30` — the caller of
this page's `001C61F0` JsonData path builder — is itself called by `0022A580`, owned
by that layer: the per-map filename resolve is reached from the scheduler's side.

**Presentation — CLIENT (SWE2-EC7-169, 19 edges).** The copy/compare primitives
`001C61F0` names — `001A5760`, `00861ED2`, `001C53F0` — are called from the
presentation layer (`001A74A0`, `001BF8B0`, `001C0670`, `001A6FF0` among 19 edges):
shared string-helper fan-in, not a presentation relationship of the prefetch
manifests.

**Save_Load_Settings — CLIENT (SWE2-EC7-174, 1 edge).** `001A5500` — the string
assign the batch-139 `00675580` section names — is also called by `001DE5D0`, a
save/settings-layer body: shared string-helper fan-in, not a save relationship
of the prefetch manifests.

## SWE2-EC7-72 update (2026-09-19) - `0059F4A0` release measured

`0059F4A0` (92 B) is the release the manifest bodies call: a non-NULL
`[+0x10]` goes to `002150E0` and the body returns; otherwise when `r8d`
is set it either closes the `[+8]` handle through `[008C2140]` (unless
`-1`) or, when the handle is `-1`, frees `[+0x20]` through `001D6CA0` -
the handle-or-buffer release pair the close path shares.
Interior anchor `0059F4DA` (the `[008C2140]` handle close).

`001D6B20` (17 B) is the byte-result thunk `001D9A40`/`001DA220`/`001DA290`/`001DA610`/`001DA970`/`001DADC0`/`0059EE90` call: one call to `0020C710`, `movzx eax, al`, return - the manifest flag byte's widened accessor.

Interior anchor `001D6B24` (function `001D6B20`).

`001D6B90` (17 B) is the sibling thunk to `001D6B20` (`001DA220`/`001DA290`/`001DADC0`/`0059EE90` call): `0020C720`, `movzx eax, al`, return - the adjacent manifest flag byte.

Interior anchor `001D6B94` (function `001D6B90`).

`001D9200` (499 B) is the recursive list splice `001D9A40` enters: `[rcx] != rcx` and `[rcx] != [rcx+8]` head/tail checks, two `001EDF00` copies build local node records at `[rbp-0x28]`/`[rbp-0x10]` from `rcx+0x10`, then self-calls and `001D9150` recurse the halves - the manifest list's split-merge.

Interior anchor `001D924C` (function `001D9200`).

`001C61F0` (294 B) is the JsonData path builder `00214C30` calls: `01DF6E48`/`01F81282` gates exit; `001C53F0` returns the name span and a 5-byte `.json` + `n` tail (`008FB2B4`/`008FB2B8`) or an `00861ED2` match against the `01F81388` region short-circuit; `001A5760` copies the name, `001C3420` prepends `"JsonData/Maps/"` (`008F9E60`) into `rsp+0x48`, and `001C7940`/`00200BF0` finish before the `rsp+0x40` object's vtable `+0x18` call consumes it - the per-map JSON filename resolve.

Interior anchor `001C6291` (function `001C61F0`).

`001C53F0` (319 B) is the `.json` canonicaliser `001C61F0` runs before constructing the path: the `01F81288`/`01F81290` SSO buffer truncates to empty, `001A9930`'s base `+0x241` string appends through `001A5760`, the buffer is scanned for the first `.json` occurrence (`008FB2B1`), and `001A9E50` substrs through it into `rsp+0x30` which `001A5760` re-appends when it differs; a `[rsp+0x48]` object's `+0x18` thunk consumes the trimmed length when non-trivial, and `001B31E0(rbx, rdi, 008FB2B4)` appends the literal `.json` into the out-string - the strip-to-extension pass that keeps the manifest name canonical.

Interior anchor `001C54C6` (function `001C53F0`).

`001C53F0` (319 B) is the `.json` canonicaliser `001C61F0` runs before constructing the path: the `01F81288`/`01F81290` SSO buffer truncates to empty, `001A9930`'s base `+0x241` string appends through `001A5760`, the buffer is scanned for the first `.json` occurrence (`008FB2B1`), and `001A9E50` substrs through it into `rsp+0x30` which `001A5760` re-appends when it differs; a `[rsp+0x48]` object's `+0x18` thunk consumes the trimmed length when non-trivial, and `001B31E0(rbx, rdi, 008FB2B4)` appends the literal `.json` into the out-string - the strip-to-extension pass that keeps the manifest name canonical.

Interior anchor `001C54C6` (function `001C53F0`).

`00675580` (378 B) is the string-table publish `00677030` runs: `00677AD0` resolves `rsi` into a `[rbp-0x41]` record, and when it is not `rsi+8` the `001A1990` compare on `rbx+0x20` gates a two-string build - both locals staged at capacity `0xF`, `001A5500` assigns `rdi` into the first, `006761F0`/`00195200` x2 and four `01CCED90` import calls carry the rest, `00210EB0` frees - the keyed-entry leg of the manifest read.

Interior anchor `006755BB` (function `00675580`).

`0019AEE0` (251 B) is the five-slot resolver `0059EE90` runs when `01F81110` is set: `01CCCC2E` opens with `edx = 0x8003`, `rbx + [rdi+0x70]` is strlen'd for `01CCCC40`, `01CCCC1A` runs with `edx = 2`, then each of the five pointers at `[rdi+0x20 .. +0x48]` is tried through `001F47D0` until one answers - `01CCCC50` unwinds the first call's handle and the hit (or `0`) returns.

Interior anchor `0019AF92` (function `0019AEE0`).

`006761F0` (429 B) is the keyed string-pool intern `00675580` runs: `[r8]` is compared against the `[rcx+8]` list head (and `rcx+8` itself), `0016D6D0` resolves the node, then `001A1990` string-compares `rbp` against `+0x20` on both the resolved and the head path; a miss with `[r15]` live runs `call [rax+0x10]` on `[rdi+0x30]` for a `0x60` node, `00675300` copies into `+0x20`, `0016D840` list-links it (`inc dword[rdi+0x28]`, `[rsi] = r15`), while the empty-`[r15]` leg runs `006763A0` and the tail re-compare falls to `00676000` - the interned-key insert behind the manifest read.

Interior anchor `00676237` (function `006761F0`).

`00676000` (486 B) is the `std::map`-style emplace the manifest reader inserts names through: it descends the `[r13+0x18]`-rooted tree comparing the `rsi` key against each node's `+0x20` string (`00861ED2` byte compare bounded by the shorter of the `r8`/`node` lengths with the usual short-string inline rules), and on a miss allocates a `0x60`-byte node through the `[r13+0x30]` allocator's `+0x10` vcall, constructs the key copy via `00675300`, links it with `0016D840` (`rbp` parent, `r14d` side), bumps the `[r13+0x28]` size, and returns `{node, 1}` through `r15` - an equal key returns `{node, 0}` instead.

Interior anchor `00676104` (function `00676000`).

`00675300` (150 B) is the two-string member copy the manifest tree-map mutators `00676000` and `006761F0` run on their records: each of the destination's `+0` and `+0x20` fields is first reset to an empty short string (`+0x18` capacity = 0xF, `+0x10` length = 0, first byte NUL via the inline-buffer branch) and then assigned from the matching source member through `001A5500` with `r8` = 0 and `r9` = -1 - the copy-whole-string arm of the MSVC `basic_string` assign.

Interior anchor `00675350` (function `00675300`).

`00677AD0` (204 B) is the string-keyed BST descent `00675580` runs on the manifest map: from `[rcx+0x18]` it `memcmp`-compares the caller's `std::string` key against each node's `+0x20` (SSO at `+0x10`/len `+0x18`), descending `[rbx]`/tail-continuing via `[rbx+8]` on order, and writes the landing node to `*[r15]` (or `*[rdx]` on the empty-tree path) - the ordered-by-name probe behind manifest lookup

Interior anchor `00677B10` (function `00677AD0`).

`001D9150` (175 B) is the sorted doubly-linked-list merge `001D9200` runs: `r8` and `rax` walk the two ranges, each node's `word[[node+0x10]]` key is compared, and the lower-keyed node is spliced ahead through the `+0x0`/`+0x8` link pairs until either range ends - the in-place ordered merge the manifest ordering uses

Interior anchor `001D9179` (function `001D9150`).

`006763A0` (174 B) is the ordered-container insert `006761F0` uses when registering a manifest row: the `[rsp+0x80]` flag plus `001A1990`'s compare of `r8` against `rcx+8` (key at `r8+0x20` vs `r9`) decides uniqueness, the virtual `[rbx+0x30]->+0x10` call allocates the `0x60` node, `00675300` builds the payload at `node+0x20` from `r14`, `0016D840` links it under `rbx+8` with side flag `esi`, `[rbx+0x28]` bumps, and the node returns through `[r15]`

Interior anchor `0067642F` (function `006763A0`).

`001C3420` (162 B) is the name-table append `001C61F0` runs: a manual strlen over `rdx` feeds `001B38B0` with the `r8` record's `+8`/`+0x18` fields and the computed tail offset, then two `001A52A0` calls splice `rsi` onto `rdi + len` and the `r14` range end - the bounded string copy pair that extends the manifest name buffer

Interior anchor `001C347C` (function `001C3420`).

`0018BC90` (145 B) is the deferred-list append `00214C30`'s JsonData path uses: `0085E730` carves a 0x20 node, `001F1940` seeds it with `dl`, then it pushes into `rdi`'s `{begin,end,cap}` span - the fast arm writes at `+8` and bumps `begin`, the full arm goes through `001AB570` - before tail-jumping `0018B4E0` -> `0018AFF0` with the node - the push-back half of the prefetch queue.

Interior anchor `0018BCCD` (function `0018BC90`).
