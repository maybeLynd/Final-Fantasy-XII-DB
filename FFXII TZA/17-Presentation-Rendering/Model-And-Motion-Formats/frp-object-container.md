---
system: The @FRP object container (.ca and .cm)
category: 17-Presentation-Rendering
status: AUDITED — no register row is open (owner re-status 2026-09-30, OPUS): the entry payloads are decoded on their own sheets (fcp, ftr, fdm/for, fte/fct, fef and motion entries; their residue stays there); the name compare is 32 bytes and no caller passes a name (§7, 2026-09-30); the seven '@FRP' argument sites read 2026-09-18 (a section-lookup key, the fallback after @FMN / @FMC at five of them) (status line current 2026-09-30, SWE2-DATA)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 5 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "4,230 / 4,230 — every .ca and .cm in the archive, header read from FFXII_TZA.vbf 2026-09-04"
last_reviewed: 2026-09-30
archive_formats:
  - "ca"
  - "cm"
audit:
  passes: 1
  last_pass: 2026-09-05
  last_pass_state: GN160-corpus-and-code-reparse-repos-1e — 4,230 files re-parsed from the VBF and every cited instruction re-decoded; corpus and loader contract confirmed, 10 non-boundary anchors corrected
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record GN160-corpus-and-code-reparse-repos-1e — 4,230 files re-parsed from the VBF and every cited instruction re-decoded; corpus and loader contract confirmed, 10 non-boundary anchors corrected; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# The `@FRP` object container — `.ca` and `.cm`

> One container under two extensions: **3,164 `.ca` and 1,066 `.cm`, all `@FRP`.** A short header,
> a name, and a table of tagged entries the engine looks up by four-byte id.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **4,230 of 4,230** — every `.ca` and `.cm` in the archive |
| magic `@FRP` | **3,164 / 3,164 `.ca`** and **1,066 / 1,066 `.cm`** |
| where they live | `ps2data/obj_finish` — both, exclusively |
| `.ca` size | 1,408 B – 2,752,512 B, median 15,552 B |
| `.cm` size | 7,168 B – 1,310,720 B, median 131,072 B |
| name field matches the filename stem | **4,230 / 4,230** |

---

## 1. What the player sees

**Objects.** These files sit in `obj_finish` and are named for the things in the world — `b0001`
(a boss), `c1004_10_3000` (a character variant), `w0001` (a weapon), `s0031_00` (a summon),
`hn1018_11` and `n1059_00` (map objects and NPCs). Every one of them is a bundle of tagged pieces
that the engine pulls out **by a four-byte id**, not by position.

The player-facing summary is that this is the wrapper around a rendered object's parts. ~~**What the
parts are is not established here** — §7 is explicit about that, and the tags are not evidence for
it.~~ *(Corrected 2026-09-30, SWE2-DATA: each entry type is now read from its readers on its own sheet —
[`@FCP`](fcp-character-parameter-block.md), [`@FTR`](ftr-node-table.md), [`@FDM` / `@FOR`](fdm-and-for-entries.md),
[`@FTE` / `@FCT`](fte-fct-texture-colour-tables.md), [`@FEF` and the motion entries](fef-and-motion-entries.md).
This sheet stays the container.)*

## 2. The layout

```struct FrpHeader base=file size=0x30
+0x00  char[4]   magic          '@FRP' -- 4,230 / 4,230
+0x04  u32       variant        0 or 1 -- the loader rejects anything else
+0x08  u32       contentLength  bytes of real content; <= file size in 4,230 / 4,230
+0x0C  u32       entryCount     number of entries; bounds-checks the lookup index
+0x10  char[16]  name           NUL-terminated; matches the filename stem 4,230 / 4,230   <- corrected 2026-10-02, OPUS - char[32]: 00408F30+0x0..+0x3C compares eight dwords, so +0x20..+0x2F below are the name's NUL tail (section 7)
+0x20  u32       _zero0         0 in 4,230 / 4,230
+0x24  u32       _zero1         0 in 4,230 / 4,230
+0x28  u32       _zero2         0 in 4,230 / 4,230
+0x2C  u32       _zero3         0 in 4,230 / 4,230
```

**The offset table follows the header, and where it begins depends on `variant`:**

    variant 0:  u32 offset[entryCount] at +0x30, each offset relative to +0x30
    variant 1:  u32 offset[entryCount] at +0x40, each offset relative to +0x40

*Not a `struct` fence: the array length is `entryCount` and its base is variant-dependent, neither
of which the fence grammar can express. Both facts are read off the loader in §3, not inferred.*

**Each entry begins with a four-byte id**, which is what the lookup compares against.

> **"Relative to the table base" is the trap this format sets.** The offsets are not file-relative
> and not entry-relative — they are relative to `+0x30` or `+0x40`, the same address the offset
> array itself starts at. A reader that treats them as file offsets is wrong by exactly the header
> size, which is small enough to look like a plausible parse for a while.

## 3. The loader contract

**`FRP_FindEntry` — `0x00408FA0`.** One function carries the whole contract.

```
FRP_FindEntry(void* blob, u32 wantId, const char* wantName, int startIndex) -> int
  if (blob == NULL)                       -> -1        0x00408FC4
  if (*(u32*)blob != '@FRP')              -> -1        0x00408FC9   <- MAGIC VALIDATED
  v = blob[+0x04]                                      0x00408FD1
  if (v != 0 && v != 1)                   -> -1        0x00408FD8   <- ONLY 0 AND 1 ACCEPTED
  n = blob[+0x0C]                                      0x00408FDD / 0x00409037
  if ((unsigned)startIndex >= n)          -> -1        0x00408FE1 / 0x0040903B
  base = (v == 1) ? blob+0x40 : blob+0x30
  tbl  = base + startIndex*4                           0x00408FE6 / 0x00409040
  for (i = startIndex; i < n; i++, tbl += 4)           0x00409016 / 0x00409070
      e = base + *(u32*)tbl                            0x00408FF3 / 0x00409053
      if (*(u32*)e != wantId) continue                 0x00408FF5 / 0x00409055
      if (wantName == NULL)  -> hit                    0x00408FFA / 0x0040905A
      if (NameEquals(blob+0x10, wantName)) -> hit       0x00409006 / 0x00409066   <- corrected 2026-10-02, OPUS - the helper returns 0 when the 32 bytes match (00408F30+0x3E) and 1 otherwise (+0x41), and the finder takes non-zero as the hit (00408FA0+0x6E jne), so a supplied name selects files whose name differs (section 7)
  return -1                                            0x0040901B
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | `0x00408FC9` | **mismatch → −1**; NULL blob → −1 | — | — |
| `+0x04` variant | `0x00408FD1` | **any value other than 0 or 1 → −1** | — | — |
| `+0x08` contentLength | — | — | — | **yes — no reader in this function; see §5, where it is nonetheless exactly the content length in 4,230 / 4,230** |
| `+0x0C` entryCount | `0x00408FDD`, `0x00409037` | — | — | — |
| `+0x10` name | `0x00409006` via `NameEquals` | — | — | — |
| `+0x20`–`+0x2C` | ~~—~~ the name compare `0x00408F30`, as the tail of its 32 bytes *(2026-09-30, SWE2-DATA)* | — | — | ~~**yes — 16 constant zero bytes, no reader in this function**~~ *(corrected 2026-09-30, SWE2-DATA: 16 constant zero bytes, read only as the NUL tail of the 32-byte name field, §7)* |
| offset table | `0x00408FF3`, `0x00409053` | — | — | — |

**The index is bounds-checked, and correctly.** `cmp ebx, r14d` / `jae` is an **unsigned** compare
against `entryCount`, so a negative `startIndex` fails too — unlike `ResourcePath_Get`
([`area-nmb-index.md` §3](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md#3-the-loader-contract)),
which checks neither of its arguments. **Two path-adjacent loaders in the same binary, opposite
answers** — which is why "the engine validates its indices" is not a statement that can be made
about the engine, only about a function.

**A miss is a supported outcome.** The scan runs to `entryCount` and returns **−1**; nothing throws
and nothing is logged. `startIndex` exists so a caller can resume a scan, so **duplicate ids are
expected by design** — the function finds the *next* match, not *the* match.

**`NameEquals` — `0x00408F30`** compares the blob's own name field at `+0x10` against a
caller-supplied string as a run of dword compares (`0x00408F32`, `0x00408F39`, `0x00408F41`,
`0x00408F49`, `0x00408F51`, …), bailing to a common failure exit on the first mismatch. **The
comparison is against `blob+0x10`, the file's name — not the entry's**, so the name argument filters
whole files, not entries within one.

**Three further sites validate the same magic** — `cmp dword ptr [reg], 0x50524640`:
`0x004090DA` (in `0x004090D0`), `0x0040981A` (in `0x00409780`) and `0x00409ACA` (in `0x00409A60`).
Seven more load `'@FRP'` into a register as an argument — `0x004180BF`, `0x0041C003`, `0x0041D301`,
`0x0041FDA6`, `0x00424691`, `0x0042510E` (`mov edx, 0x50524640`) and `0x00504F58`
(`mov r9d, 0x50524640`) — so the tag is used both as a file magic and as a lookup key passed to
generic code. **Eleven sites in total, and `0x00408FC9` above is the eleventh.**

> **The seven argument sites, read 2026-09-18 (FABLE).** All seven hand the tag to the resource entry's section-lookup family with the object's name — `ResourceEntry_FindSectionOffsetByTagAndName` `00409A30`, `00409FA0` (the index form), `00409660` (block by tag), or the wrapper `00504E70` — so as a key `@FRP` names **the container's own section inside a resource entry**, and at five of the seven it is the *fallback* tried when a more specific tag is absent: after `@FMN` at `004180BF` (`PresentationAuthoredCommand_Class09_ActivateLoadedResourceState`, `004180AA`–`004180C7`, the block then handed to `00408F80`) and at `0041C003` (`0041BEE0`, offset into `+0x54`, followed by `@FMW` into `+0x58`); after `@FMC` at `0041D301` (`PresentationEntry_InitializeFromResourceDefinition`, offset into `+0x320`, followed by `@FRM`), at `00424691` (`00424550`) and at `0042510E` (`00424D80`) — those two fall through to `@FMN` next. It is the *first* key at `0041FDA6` (`0041FCF0`, the character render record's bind: the index goes to the record's `+0x408`, see [the render record array](../Character-Render-Records/the-character-render-record-array.md), UQ-196) and at `00504F58` (`00504F00`, through `00504E70` into the context's `+0x1F0`, then `@FEF` into `+0x228` and `@FOR` by offset). So the seven sites are one idiom — *find this object's section by name, preferring the motion or model-parameter section when the entry has one* — and none reads the container's parts~~; what the parts are stays open~~. *(answered: see the 2026-09-30 corrections - each entry type is read on its own sheet; 2026-10-02, OPUS)*

> **These ten addresses were corrected on 2026-09-05 (§6b) and the correction is instructive.** They
> previously read `0x004090DD`, `0x0040981D`, `0x00409ACC`, `0x004180C0`, `0x0041C004`, `0x0041D302`,
> `0x0041FDA7`, `0x00424692`, `0x0042510F`, `0x00504F5A` — **each 1–3 bytes higher, and none of them
> an instruction boundary.** They were the addresses of the `40 46 52 50` *bytes*, not of the
> instruction consuming them: in `mov edx, 0x50524640` (`BA 40 46 52 50`) the immediate begins one
> byte into the instruction, and in `cmp dword ptr [r9], imm32` (`41 81 39 …`) three bytes in.
> **The finding was right and every anchor was unusable** — a disassembler jumped to any of them
> lands mid-instruction. `0x00408FC9`, the one address read off a disassembly rather than off a byte
> scan, was correct.

**The write path.** None found.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x00408FA0` | `FRP_FindEntry` — null guard `0x00408FC4`, magic `0x00408FC9`, variant gate `0x00408FD8`, count `0x00408FDD`, bounds check `0x00408FE1`, variant-1 table base `0x00408FE6`, entry rebase `0x00408FF3`, id compare `0x00408FF5`, name call `0x00409006`, loop `0x00409016`, miss `0x0040901B` | ✅ full body |
| `0x00409037` | the variant-0 arm of the same function — count `0x00409037`, bounds `0x0040903B`, table base `+0x30` `0x00409040`, rebase `0x00409053` | ✅ full body |
| `0x00408F30` | `NameEquals` — dword-wise compare from `0x00408F32` | ◐ the compare chain |
| `0x004090D0` · `0x00409780` · `0x00409A60` | three further `@FRP` magic validations | `004090D0` ✅ full body 2026-09-13 — the child selector: version 0 / 1 child offsets from `+0x30` / `+0x40`, returned as zero-extended 32-bit sums; version 1 reads the offset table before its bound test ([addressing §4](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md)); the other two ✗ magic site only |

## 5. Corpus survey

**Invariants — measured over all 4,230 files.**

| | |
|---|---|
| magic `@FRP` | **4,230 / 4,230** |
| `+0x04` ∈ {0, 1} | **4,230 / 4,230** — matching exactly what the loader accepts |
| `+0x08` ≤ file size | **4,230 / 4,230** |
| `+0x20`–`+0x2C` all zero | **4,230 / 4,230** |
| name NUL-terminated and equal to the filename stem | **4,230 / 4,230** |

### `+0x08` is the content length, and the rest of the file is zero padding

| group | files | `+0x08` vs size | trailing bytes all zero |
|---|---:|---|---|
| `.ca` variant 0 | 1,969 | **equal in all 1,969** | no padding at all |
| `.ca` variant 1 | 1,195 | always less | **1,195 / 1,195** |
| `.cm` variant 0 | 1,066 | always less | **1,066 / 1,066** |

**Every byte between `+0x08` and EOF is zero, in every padded file.** ~~The padded groups are aligned
to large boundaries — 4 KiB, 16 KiB, 32 KiB and 64 KiB dominate — while the unpadded `.ca`
variant-0 files are merely 16-byte aligned.~~ *(Corrected 2026-09-30, SWE2-DATA, census [`frp_checks.py`](../../_index/candidates/dd-data-4-0930/frp_checks.py) A1: by the
largest power of two dividing the file size, capped at 64 KiB, `.ca` variant 1 lands on 64 KiB in 474 files, 4 KiB in
378, 16 KiB in 188, 8 KiB in 99 and 32 KiB in 56 (never below 4 KiB); `.cm` on 16 KiB in 340, 32 KiB in 200, 8 KiB in
186, 64 KiB in 121, 1 KiB in 95, 2 KiB in 64 and 4 KiB in 60, so 159 `.cm` files are padded only to 1 or 2 KiB. The
unpadded `.ca` variant-0 files are 16-byte aligned at least, and 959 of 1,969 at exactly 16.)* So `.cm`'s much larger median size (131,072 B against
`.ca`'s 15,552 B) is **partly padding, not content**, and any size comparison between the two
extensions that uses the file length is measuring the alignment policy as much as the data.

### The `.ca` / `.cm` question, answered — and the answer is not the extension

The folder README asks what distinguishes `.ca` from `.cm`, noting the 3:1 file ratio is the only
hint and that **"it may distinguish nothing."** That is nearly right, and the real split is more
interesting:

| | variant 0 | variant 1 |
|---|---:|---:|
| `.ca` | 1,969 | 1,195 |
| `.cm` | 1,066 | **0** |

**There is a real binary split in the container, and it does not fall on the extension boundary.**
`variant` is a genuine structural discriminator — the loader branches on it and it moves the offset
table by 16 bytes — and **variant 0 spans both extensions** (3,035 files) while variant 1 is `.ca`
only. So the extension does not select a layout; `+0x04` does, and it cross-cuts the extensions.

**No header field separates `.ca` from `.cm`.** Every dword in the first `0x40` bytes was compared
across the two populations: the only disjoint one is `+0x14`, which is **the middle of the name
string** and separates them only because the two naming conventions differ. That is not a format
distinction.

**What varies.** `entryCount` takes 47 distinct values in `.ca` and 11 in `.cm`, the commonest being
4 (`.ca` variant 0) and 6 (`.cm`). Name lengths cluster tightly: 13 characters in every `.ca`
variant-0 file, 8 in every `.ca` variant-1 file, and 5 or 9 in `.cm`.

## 6. Falsification pass — 2026-09-04

| attack | result |
|---|---|
| Is the magic actually compared, or are the `.text` hits coincidence? | **Compared — and this was tested, not eyeballed.** `'@FRP'` occurs 12 times image-wide, 11 in `.text`. Decoding every containing function and reading each instruction's operands: **11 of 11 are real operands** — four `cmp dword ptr [reg], 0x50524640` and seven `mov reg, 0x50524640`. Contrast the EBP `section_000` marker, where 8 `.text` byte hits yielded **0** real operands. The same test, opposite answers; the byte count alone would have been consistent with either. |
| Is the offset table file-relative? | **No — relative to the table base**, `+0x30` or `+0x40`. Read off `lea ecx, [rdi + 0x30]` / `add ecx, [rsi]` at `0x00409050`–`0x00409053` and the variant-1 twin at `0x00408FF0`–`0x00408FF3`. **The corpus cannot distinguish this from a file-relative table** — the difference is one header size — so it is decided by the instruction. |
| Is `variant` really constrained to {0, 1}? | **From both sides.** The loader rejects anything else (`0x00408FD8`), and the corpus contains nothing else in 4,230 files. Independent agreement between what the code accepts and what the data contains. |
| Is `+0x08` a content length or a coincidence? | **It is ≤ the file size in 4,230 / 4,230, equal in 1,969, and every byte beyond it is zero in all 2,261 padded files.** No offset-to-a-member would satisfy all three. It is still listed **`Inert`** in §3 because *this function does not read it* — a field can be perfectly meaningful and unread by the code you have read. |
| Does the extension select the layout? | **No.** Variant 0 spans both extensions; variant 1 is `.ca`-only. And no header dword separates the extensions except one inside the name text. |
| Did an external tool supply any of this? | **No.** No oracle reads `@FRP`. |

**What was tried and failed to break it.** The natural reading of two extensions sharing a magic is
that one is a subset or a version of the other. That predicts a header field separating them. **A
dword-by-dword comparison of the whole first `0x40` bytes across both populations found exactly one
disjoint offset, and it is the middle of the name string** — an artefact of naming convention, not a
discriminator. The real split is `variant`, and it does not respect the extension boundary.

## 6b. Independent audit pass — 2026-09-05, `repos-1e`

**Method.** The corpus was re-parsed from `FFXII_TZA.vbf` with a fresh reader (block-0 decompress,
header only), and every cited instruction address was checked against a capstone decode of the
containing function taken from `functions.tsv` bounds. Program state: GN160 (`gzf fa0db293…`).

**The corpus half reproduces exactly — every row.**

| claim | sheet | re-parse |
|---|---|---|
| files | 3,164 `.ca` + 1,066 `.cm` = 4,230 | **identical** |
| magic `@FRP` | 4,230 / 4,230 | **4,230 / 4,230** |
| name field matches the filename stem | 4,230 / 4,230 | **4,230 / 4,230** |
| `contentLength` ≤ file size | 4,230 / 4,230 | **4,230 / 4,230** |
| `+0x20`–`+0x2C` all zero | 4,230 / 4,230 | **4,230 / 4,230** |
| `.ca` variant 0 | 1,969 | **1,969** (and `.ca` v1 1,195, `.cm` v0 1,066 — `variant` cuts across the extension, as §6 says) |

**The loader contract reproduces exactly**, instruction by instruction. `0x00408FC4` `test rcx,rcx`;
`0x00408FC9` `cmp dword ptr [rcx], 0x50524640`; `0x00408FD1` `mov ecx,[rcx+4]`; `0x00408FD8`
`cmp ecx,1`; `0x00408FDD`/`0x00409037` `mov r14d,[rdi+0xc]`; `0x00408FE1`/`0x0040903B`
`cmp ebx,r14d`; `0x00408FE6` `lea rsi,[rbx+0x10]` and `0x00409040` `lea rsi,[rbx+0xc]`;
`0x00408FF3`/`0x00409053` `add ecx,[rsi]`; `0x00408FF5`/`0x00409055` `cmp [rcx],r15d`;
`0x00409006`/`0x00409066` `call 0x408f30`; `0x0040901B` `or eax,0xffffffff`. **All present, all at
instruction boundaries, all doing what the sheet says.**

**The variant-dependent table base is confirmed from the arithmetic, not just the labels.**
`lea ecx,[rdi+0x40]` (`0x00408FF0`) pairs with `lea rsi,[rbx+0x10]`, giving
`entry = blob + 0x40 + startIndex*4`; `lea ecx,[rdi+0x30]` (`0x00409050`) pairs with
`lea rsi,[rbx+0xc]`. **§2's "offsets are relative to `+0x30` or `+0x40`, the same address the table
starts at" is exactly right**, and it is the sheet's most useful sentence for a reader.

**`+0x08` is confirmed `Inert` in this function.** Enumerating every memory operand with a small
displacement, the only `+0x08` access is `mov qword ptr [rsp+8], rbx` — a stack spill, not the blob.
The blob registers are `rcx` (`+0x00`, `+0x04`) and `rdi` (`+0x00`, `+0x0C`, `+0x10`, `+0x30`,
`+0x40`). **I set out to break this row and it held.**

### One defect found: ten unusable instruction anchors

**The three extra validation sites and the seven argument sites are real, and the counts are exact —
4 compares and 7 loads, 11 in total, matching the sheet.** But **ten of the eleven cited addresses
were not instruction boundaries**; they pointed 1–3 bytes into an instruction, at the `40 46 52 50`
bytes rather than at the instruction consuming them. Corrected in §3 with the old values kept.

> **Why it matters more than three bytes.** An anchor that lands mid-instruction is worse than a
> missing one: it looks valid, `check_named_not_cited` cannot see it, and a reader jumping there
> gets a garbage decode and doubts the sheet rather than the address. **The one address that was
> right — `0x00408FC9` — is the one read off a disassembly**; the ten wrong ones came from a byte
> scan for the constant, which returns the immediate's position. *Same instrument, same failure
> mode, as the `0x8000000B` scan in the EBP container sheet — the difference there was that the
> operand test was run afterwards.*

**Not audited:** whether the entry payloads under an id are what §7 says they are not — that is
outside this pass, and §7 already declines to claim it.

## 7. What this document does not claim

- **Nothing about entry contents.** Entries are located, bounded and keyed by a four-byte id; **none
  is parsed and no id is decoded.** What `.ca` and `.cm` actually hold is exactly the question this
  sheet leaves open. → `PROPOSED-repos-4b-14` **Narrowed 2026-09-11** — §9 below censuses the
  entry tags of all 4,230 files and [the `@FCP` page](fcp-character-parameter-block.md) decodes
  the first entry of every `.cm`. *(Closed for this sheet 2026-09-30, OPUS: each entry tag is decoded on its own sheet
  (§9 and the status line: fcp, ftr, fdm/for, fte/fct, fef and motion entries), and any residue stays there. This sheet
  remains the container.)*
- **Why variant 1 exists, and why only `.ca` uses it.** The layout difference is 16 bytes of table
  base. Whether that reflects a version, a content class or a build-time choice is not established.
  → `PROPOSED-repos-4b-15` **Narrowed 2026-09-11** — every variant-1 file is a table of 81–311
  entries most of which carry the zero (wildcard) tag: a fixed-slot motion library (§9). *(Declared limit 2026-09-30,
  OPUS: the loader reads both layouts, and the image holds no writer of the container (§3, "The write path"), so why
  the authoring side uses the second layout for motion libraries is the build tooling's, like the alignment policy
  below.)*
- ~~**The seven sites that pass `'@FRP'` as an argument were not read**, so whether the tag doubles as
  an entry id inside some other container is unknown.~~ *(Corrected 2026-09-30, SWE2-DATA: read 2026-09-18, §3 —
  the tag is a section-lookup key naming the container's own section inside a resource entry.)*
- ~~**`NameEquals`'s comparison length was not established** — the dword chain was read, not counted,
  so "16 bytes" is the field width from §2 and not a measured compare length.~~ *(Corrected 2026-09-30, SWE2-DATA,
  [`frp_checks.py`](../../_index/candidates/dd-data-4-0930/frp_checks.py) N1–N3: it compares eight dwords, `+0x00`..`+0x1C` of both strings — 32 bytes, so the header's name
  field is 32 bytes and the four zero dwords `+0x20`–`+0x2C` are its NUL tail. It returns 0 when all 32 bytes match
  and 1 at the first differing dword, and `FRP_FindEntry` takes the non-zero return as the hit (`0x0040900B` /
  `0x0040900E`), so a supplied name would select files whose name *differs* from it; the name `NameEquals` gives it
  is the reverse of what it returns. No caller exercises it: every entry is the zero-start thunk `0x00408F90`, whose
  four callers all pass no name and the tag `@FRM`.)*
- **The alignment policy is described, not explained.** ~~Padded files land on 4 KiB–64 KiB
  boundaries;~~ *(corrected 2026-09-30, SWE2-DATA: `.cm` files land on 1 KiB–64 KiB and `.ca` variant 1 on 4 KiB–64
  KiB boundaries, §4)* nothing here says who pads them or why `.ca` variant 0 is exempt. *(Note 2026-09-30,
  SWE2-DATA: the image holds no writer of the container (§3, "The write path. None found"), and the finder reads neither
  `+0x08` nor the padding (§3), so the policy belongs to the build tooling, which does not ship; it is a declared limit of
  this sheet, not a question the image can answer.)*
- **Ownership is provisional.** The folder README notes these may belong to `04-Actor-Entity`
  rather than `17-Presentation-Rendering`. **This sheet does not settle it** — the loader is generic
  container code and says nothing about who owns the payload.

## 8. Related

- [`Model-And-Motion-Formats/README.md`](README.md) — the folder brief that posed the `.ca` / `.cm`
  question §5 answers.
- [`pkfl-package-container.md`](../../26-PKFL-Package-Container/Container/pkfl-package-container.md)
  — the other multi-extension container, and the contrasting case where the magic is *not* validated.
- [`sab-sound-bank-container.md`](../../18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md)
  — a magic validated through an `.rdata` constant instead of an immediate; the three sheets together
  cover all three ways this binary handles a file tag.
- [`area-nmb-index.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md)
  — `ResourcePath_Get`, the unbounded counterpart to §3's bounds check.
## 9. Extension 2026-09-11 — what the entries are (FABLE)

A second pass over the same 4,230 files read every entry's first `0x30` bytes. **Each entry
begins with the same header shape the container uses**: a four-byte tag, a word at `+0x04`, the
entry's byte length at `+0x08`, a word at `+0x0C`, and a 32-byte NUL-padded name at `+0x10` that
the tag + name finder compares ([the addressing page](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md));
the `+0x04` / `+0x0C` words vary by tag (`@FCP` is always `0, 1`; `@FDM` and `@FOR` `0, 0`; `@FTR`
`2, n`; `@FMN` carries ~~`0x02000211`~~ `0x02001111` or `0x02001011` *(corrected 2026-10-02, OPUS: read through `vbf_read_entry` from `FFXII_TZA.vbf`, a 200-file `.ca` sample: no `@FMN` carries `0x02000211`)* and a count) and no reader of them was found.

| population | entry tags | files |
|---|---|---:|
| `.cm` | `@FCP @FTR @FDM @FOR @FTE @FCT` | 855 |
| `.cm` | the same plus `@FEF` | 144 — 82 monsters, 27 NPCs, 26 summons, 9 gadgets |
| `.cm` | the same plus `@FMC` / `@FMN` / `@FMW` motion entries | 45 — 29 weapons, 16 treasures |
| `.cm` (weapons) | `@FCP @FTR @FOR`, or `@FCP @FTR @FDM @FOR` | 21 + 1 |
| `.ca` variant 0 | `@FMC @FMN @FMW @FRM` | 1,969 |
| `.ca` variant 1 | 81–311 slots: `@FRM` in all 1,195, `@FMC` / `@FMN` / `@FMW` in 817; ~~mostly the zero tag (the finder's wildcard)~~ **corrected 2026-09-12 (FABLE): the remaining slots are *empty* — their offset is 0, so `FRP_FindEntry` reads the id at the table base itself, i.e. the first offset word (`0` in the 574 files whose slot 0 is empty, `0x200` / `0x260` / … otherwise); no shipped entry carries an authored zero tag** | 1,195 |
| `.mot` packs (`PKFL`) | **9,909 `@FRP` containers** embedded at `0x800`-aligned offsets in the 4,392 `.mot` files (1–3 per file), every one `@FRM` + `@FMC` / `@FMN` / `@FMW` — a second motion population the 2026-09-11 census did not cover (2026-09-12) | 4,392 |

*Added 2026-09-20 (FABLE) - three of the motion entries identified from their readers, and what the fixed slots are.*
`@FMC` is the **authored command block** - named `ready`, `attack`, `magic` ..., track count in its word `+0x0C`, format
and a census of all 62,208 on [the authored-command page](../Authored-Commands/the-authored-presentation-command-handlers.md).
`@FMN` is the **bone motion** such a block binds *by name* through command `0x09` (that invoker ~~is only partly read~~ *(answered: see the handler page - `00417F40` read whole; 2026-10-02, OPUS)*),
and `@FMN` / `@FMW` come in equal numbers in every one of the 3,164 `.ca` files. **A version-1 container's slot number
is the motion id**: the presentation entry records the child number of the motion it plays, and the blend-in rule
`0x2C` matches its *from* word against it - in the data all **362,594** such words are below their own container's
slot count and name a slot that is occupied in the same file
([`slots.py`](../../_experiments/evidence/frp-children-and-motion-slots/slots.py),
[output](../../_experiments/evidence/frp-children-and-motion-slots/slots.out.txt)). *(Later the same day: command `0x09` finds the `@FMW` **with the motion's own name** and binds the two together - and all
18,303 bone motions have one; the authored-command page's `0x09` section.)* ~~`@FMW`'s contents, `@FRM` and the model-side
`@FTR` / `@FDM` / `@FOR` / `@FTE` / `@FCT` / `@FEF` remain unread.~~ *(Corrected 2026-09-30, SWE2-DATA: all of them
are now read on their own sheets — [`@FTR`](ftr-node-table.md), [`@FDM` / `@FOR`](fdm-and-for-entries.md),
[`@FTE` / `@FCT`](fte-fct-texture-colour-tables.md), and [`@FEF`, `@FRM` and `@FMW`](fef-and-motion-entries.md);
what each leaves open is stated there.)*

So `.cm` is a model with its parameter block first, `.ca` a motion set, and **variant 1 is the
fixed-slot motion library** — 46 distinct slot counts, `81` in 378 files. The `@FCP` entry is
decoded on [its own page](fcp-character-parameter-block.md); the readers of the others are named
there under "what is not known".

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — CLIENT.** A cited function is called by a 10-byte Resource body.
