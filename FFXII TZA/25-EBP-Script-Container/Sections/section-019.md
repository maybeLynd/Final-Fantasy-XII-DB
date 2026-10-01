---
system: EBP section_019 — the FF12AR03 area-data block
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: PrimaryOwner:WorldAreaField
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
corpus_validated: "1115 / 1115 us .ebp scripts, 2026-09-03 (1114 containers; section_019 in 271)"
last_reviewed: 2026-09-12
ebp_units:
  - "section_019"
audit:
  passes: 3
  last_pass: 2026-09-05
  last_pass_state: "GN160 (gzf fa0db293…d2f708, snapshot b57264ba…d18fea34, exe 73461d08…d89721f8) — independent pass by repos-4b: own header parser over all 271 sections, cross-checked against my own parse of the 166 standalone .ard files"
  last_pass_by: repos-4b
  crossref_clean: true
  crossref_checked: null
  crossref_report: null
  reopened_count: 1
---

# EBP `section_019` — the `FF12AR03` area-data block

> A fixed header, a 16-byte record array, and a second table after it. The engine's own name is
> **`MAPARD`** — map area data — and unlike every other section in this lane, **the same format also
> ships as 332 standalone `.ard` files**, which makes it the one section here with an independent
> second copy to check against.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` scripts (1,114 containers) |
| this unit present in | **271 (24.3 %)** |
| co-occurrence | **always with `section_016` — 271 of 271**, and always with `000`. Also `012` 252, `002` 229, `003` 69, `004` 65, `008`/`009` 33 each, `006` 3, `010`/`011` 2 each. **Never with `014`.** |
| size range | **128 B – 768 B, median 256 B**, 9 distinct sizes, every one a multiple of 16 |
| records | **2,116 across the 271 files**, 0 – 41 per file |

**`019` is a strict subset of `016`.** `section_016` occurs 517 times, `section_019` 271, and there
is no file with `019` and not `016`. The two share the `FF12` family prefix in their magics
(`FF12POS3` and `FF12AR03`), and the engine's tags for them (`POSENT`, `MAPARD`) sit adjacent in one
`.rdata` table. They are two members of one authored-file family with a one-way dependency, and the
direction is a fact about both: **area data implies positions; positions do not imply area data.**

---

## 1. What the player sees

**Where one map ends and the next begins.** An `.ard` — area data — is the per-zone table that
answers "the party walked to this edge; what happens?" In the game that is the zone-transition
line, the load boundary, the named region the map screen labels.

The honest limit: the shape below is proven and the naming is strong, but **no field in the record
is decoded to a game-visible meaning.** Section 2 gives the measured value ranges; section 7 says
what that does not amount to.

## 2. The layout

Offsets from the **start of the section body**. All fields little-endian.

```
+0x00  char[8]  magic       'FF12AR03'                    -- 271/271
+0x08  u32      0                                         -- 271/271
+0x0C  u32      offsetB     offset of the second table; 0 = absent
+0x10  u32      0x30                                      -- 271/271
+0x14  u32      0x30                                      -- 271/271
+0x18  u32      0x30                                      -- 271/271
+0x1C  u32      0                                         -- 271/271
+0x20  u32      0                                         -- 271/271
+0x24  u32      0                                         -- 271/271
+0x28  u32      0                                         -- 271/271
+0x2C  u32      0x30                                      -- 271/271
+0x30  u32      countA      number of 16-byte table-A records
+0x34  u32      0                                         -- 271/271
+0x38  u32      0                                         -- 271/271
+0x3C  u32      0                                         -- 271/271
+0x40  <countA * 16 bytes>   table A
[offsetB]  table B
```

**`offsetB == 0x40 + countA * 16` in 266 of 271 files** — table B begins immediately after table A.
In the other **5 files `offsetB` is `0`** while `countA` is non-zero (4, 5, 5, 5 and 11), which on
this reading means *table A is present and table B is absent*. Those five are listed in section 5.

### `+0x10`–`+0x2C` is an eight-slot offset directory — and it is degenerate here

The 2026-09-03 version of this sheet recorded these eight `u32` as constants it could not explain and
raised `BZ-2`. **They are a directory**, indexed by slot number with `0` meaning absent — the same
construction the `EBP2` container itself uses.

```struct Ff12Ar03Header base=section size=0x30
+0x00  char[8]  magic        'FF12AR03' -- 271/271
+0x08  u32      _zero0       0 in 271/271
+0x0C  u32      trailerOff   offsetB: past every present slot in 266/271; 0 in the other 5
+0x10  u32      slot0        0x30 -- 271/271
+0x14  u32      slot1        0x30 -- 271/271
+0x18  u32      slot2        0x30 -- 271/271
+0x1C  u32      slot3        0 -- absent, 271/271
+0x20  u32      slot4        0 -- absent, 271/271
+0x24  u32      slot5        0 -- absent, 271/271
+0x28  u32      slot6        0 -- absent, 271/271
+0x2C  u32      slot7        0x30 -- 271/271; the one slot the handler follows (section 3)
```

The sixteen bytes every present slot points at are **not part of the container header** — they are
the first block's own header, and in a standalone `.ard` the same position holds an `st2e` table
header instead:

```struct Section019TableAHeader base=slot0 size=0x10
+0x00  u32      countA       16-byte table-A records
+0x04  u32      _zero1       0 in 271/271
+0x08  u32      _zero2       0 in 271/271
+0x0C  u32      _zero3       0 in 271/271
```

*(Fence split 2026-09-11: `Ff12Ar03Header` is the 0x30-byte eight-slot directory header, declared
with the same names here, on the `.ard` loader page and in the St2e-Carriers README; the 0x40 this
sheet first declared folded table A's header into the container's. OPUS-REQ-FABLE-FENCEDUP.)*

Measured over all 271 files, **exactly one directory pattern occurs**:

| slot | offset | value | present |
|---:|---|---:|---|
| 0 | `+0x10` | `0x30` | 271/271 |
| 1 | `+0x14` | `0x30` | 271/271 |
| 2 | `+0x18` | `0x30` | 271/271 |
| 3 | `+0x1C` | `0` | **absent, 271/271** |
| 4 | `+0x20` | `0` | **absent, 271/271** |
| 5 | `+0x24` | `0` | **absent, 271/271** |
| 6 | `+0x28` | `0` | **absent, 271/271** |
| 7 | `+0x2C` | `0x30` | 271/271 |

**The directory ends at `0x30` and every present slot points at `0x30`** — the first payload byte.
That is what "degenerate" means here: four live slots all resolving to the same place, which is why
a corpus reading saw four constants rather than four offsets. Every present value is `0x10`-aligned,
and `trailerOff` at `+0x0C` is greater than every present slot in 266 files and `0` in 5.

**Two independent lines of evidence support the directory reading, and neither would be enough
alone:**

1. **The loader treats `+0x2C` as an offset.** `003EAA32` reads it, resolves it and **adds the
   result to the section base** (§3). That is tier 1, it is this sheet's own, and it proves at least
   slot 7 is an offset rather than a constant.
2. **The standalone `.ard` files use the same eight slots non-degenerately.** `repos-d6` measured
   166 areas: present offsets strictly ascending and distinct 166/166, all inside the file, all
   `0x10`-aligned, first present offset `0x30` in 166/166 — and **slots 3 and 4 absent in all 166**.
   In `.ard` the slots carry four `st2e` tables at slots 0, 2, 5, 6 with a per-slot constant record
   size. *(Corpus-side only; `repos-d6` read no `.ard` loader and says so. See
   `_index/_inbox/repos-d6.md`.)*

> **CORRECTED 2026-09-05 by the audit — the two absences are not the same, and the difference
> weakens this argument rather than supporting it.** This paragraph said `.ard`'s missing slots 3
> and 4 were *"the same absence this corpus shows"*. Re-derived over both populations:
>
> | population | present slots | absent |
> |---|---|---|
> | `section_019`, **271/271** | **{0, 1, 2, 7}** | 3, 4, **5, 6** |
> | `.ard`, **166/166** | {0, 1, 2, 5, 6, 7} | 3, 4 |
>
> **`section_019` is missing slots 5 and 6 as well**, so its absence is a strict superset of
> `.ard`'s, not a match. That matters for the argument being made here: **`.ard` carries its four
> `st2e` tables at slots 0, 2, 5, 6, and `section_019` populates only two of those four.** The
> structural agreement is over `{0, 1, 2, 7}` — real, and narrower than "same directory, same absent
> slots" implies. **The §3 conclusion is unaffected**; what changes is how much this second line of
> evidence carries. *(`repos-4b`; `section_019` slot presence re-derived here, `.ard` slot presence
> from my own parse of the 166 extracted files during the `.nmb` work.)*

**`BZ-2` closes**: the eight fields are directory slots, and §3 says which of them this build's
handler actually follows.

> **What this does not establish.** That `section_019` and a standalone `.ard` are the *same format*
> still needs their bytes compared, and they have not been. The agreement is structural — same
> directory, same size, same absent slots — and structural agreement between two populations is
> strong evidence about the shape and no evidence at all about the contents.

### Audit pass — 2026-09-05, `repos-4b` (independent)

**Every header claim in the `Ff12Ar03Header` fence re-derived over all 271 sections, all exact:**
magic `FF12AR03` **271/271**; `+0x08` zero **271/271**; `+0x34`, `+0x38`, `+0x3C` zero **271/271**
each; `+0x0C` **greater than every present slot in 266 and zero in 5, with no third case**; every
present slot equal to `0x30` in **271/271**, so the degenerate reading is exact as written.

**One correction, above:** the claim that `.ard` and `section_019` show *"the same absence"* is
wrong — `section_019` is `{0,1,2,7}` and `.ard` is `{0,1,2,5,6,7}`. Details and consequence in the
blockquote in §2.

**Not attacked:** whether `section_019` and a standalone `.ard` are the same *format* — the sheet
already declares that open and explicitly refuses the byte comparison it would need.

### Table A — the record

16 bytes, fixed. Measured over all **2,116** records:

```
+0x00  u16  0 .. 242          202 distinct values
+0x02  u16  {109, 110, 115}   only three values ever: 109 x1449, 110 x658, 115 x9
+0x04  u16  1 .. 15           8 distinct; 1 in 1,698 of 2,116
+0x06  u16  500 .. 4008       92 distinct
+0x08  u16  60 .. 2306        1,161 distinct -- the widest field, near-unique per record
+0x0A  u16  0                 -- 2116/2116, invariant
+0x0C  u16  0                 -- 2116/2116, invariant
+0x0E  u16  0                 -- 2116/2116, invariant
```

**Six of the sixteen bytes are zero in every record in the corpus.** That is 37.5 % of the record
reserved or unused — a large fraction, and the kind of thing worth knowing before assuming a field
is meaningful.

`+0x02` is the striking one: **three values in 2,116 records.** A field with that distribution is a
kind or a version, not a quantity. `+0x08`, at the other end, is nearly unique per record and reads
like an identifier.

### Table B

**Not decoded.** It is present in 266 files and runs from `offsetB` to the end of the section — 16 B
to 256 B, most commonly 64 B (128 files) or 48 B (54 files). It is non-zero in every file that has
it, so it is real content and not padding.

## 3. The loader contract

**Established 2026-09-04.** `section_019` is slot 19 of the `EBP2` directory.

```
ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources   003304A0
  00330650  CMP dword ptr [RDI+4],0x13   ; slotCount > 19
  00330656  MOV EAX,[RDI+0x5C]           ; slot 19's offset; 0 -> absent
  0033065C  ADD RAX,RDI ; OR EAX,EBX
  00330666  CALL FUN_003320D0
        |
        v
FUN_003320D0  (13 bytes)
  003320D5  AND RCX,0xFFFFFFF0           ; recover the pointer; manager index DISCARDED
  003320D8  JMP FUN_003EAA00
        |
        v
FUN_003EAA00  (105 bytes)
  003EAA06  CMP qword ptr [02B5E0C8],0 ; is a previous section_019 still bound?
  003EAA15  CALL FUN_003DCF10(0)         ;   yes: unbind
  003EAA21  CALL FUN_00331880(oldPtr)    ;   yes: release the old buffer
  003EAA26  MOV qword ptr [02B5E0C8],RBX   ; latch the new pointer
  003EAA30  TEST RBX,RBX ; JE            ; null -> done
  003EAA32  MOV ECX,dword ptr [RBX+0x2C] ; *** reads +0x2C ***
  003EAA35  CALL FUN_0020E600            ; resolve it
  003EAA3D  TEST RAX,RAX ; JE  -> FUN_003DCF10(0)
  003EAA47  MOVSXD RCX,EAX ; ADD RCX,RBX ; section + resolved offset
  003EAA52  JMP FUN_003DCF10(ptr)
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic `FF12AR03` | — | — | — | **YES — never read.** `FUN_003320D0` + `FUN_003EAA00` are 118 bytes and neither touches `[rbx+0x00]` |
| `+0x08` | — | — | — | **YES — never read** |
| `+0x0C` `offsetB` | `003EA650(1)` — via the base table `02B5E0C0 + 8`, where `003EAA26` latches this section | — | — | **NO — read (BZ-2, 2026-09-12)**: the trailer reader resolves it and the flag-mask appliers `0035A3A0` / `0035AC60` walk both bases, `.ard` and this section |
| `+0x10`, `+0x14`, `+0x18` — slots 0, 1, 2 | — | — | — | **never read on this path.** Present and pointing at `0x30`; in a standalone `.ard` the same slots carry separate tables, so this is build-inert, not format-inert |
| `+0x1C` – `+0x28` — slots 3, 4, 5, 6 | — | — | — | **YES — never read, and absent (`0`) in 271/271** |
| **`+0x2C`** — directory slot 7 | **`003EAA32` `MOV ECX,[RBX+0x2C]`, twice** | — | — | — |
| `+0x30` `countA` | — | — | — | **not read by this handler** — but see below |
| `+0x34` – `+0x3C` | — | — | — | **YES — never read** |

> **BZ-2 answered 2026-09-12 (FABLE) — per field, by every static route.** "Needs the loader" is
> satisfied by this table plus one route it could not see: the handler latches the section at
> `02B5E0C8`, the second entry of the `.ard` base table `02B5E0C0`, and `003EA650(idx)` reads
> `[table + idx·8]` then `[base + 0x0C]` (`003EA671`), so **`+0x0C` is read** — by the actor
> flag-mask appliers `0035A3A0` / `0035AC60`, whose loop runs `idx` over 0 and 1 (see the `.ard`
> sheet, CC-8). Every other reference to `02B5E0C8` in the image is the handler's own (`003EAA06`,
> `003EAA1A`, `003EAA26`; none in the code outside the function list), so **`+0x2C` (the handler) and
> `+0x0C` (the trailer reader) are the only header fields any code reads**. The constants are then
> split: `+0x2C = 0x30` is a **read constant** the handler follows to `countA`; `+0x10` / `+0x14` /
> `+0x18 = 0x30`, `+0x08 = 0`, `+0x1C`–`+0x28 = 0` and `+0x34`–`+0x3C = 0` are **unread** in this
> build by any static route — the exporter fills them because the format is the `.ard` header, in
> which the same slots are live.

### The handler follows exactly one directory slot — slot 7

`FUN_0020E600` is ten bytes: `mov eax, ecx` (zero-extend) then `add rax, [01F83530]`. It returns
**`value + a global base`**. `FUN_003EAA00` sign-extends the low 32 bits of that and adds it to the
section pointer, so the handler ends up passing **`section + 0x2C's value`** to `FUN_003DCF10`.

`+0x2C` is `0x30` in **271 of 271** files, so the resolved pointer is `section + 0x30` — exactly
where `countA` sits. **`+0x2C` is directory slot 7**, and the loader reaches `countA` and table A
through it rather than at a hard-coded offset.

**So of the four present slots, this handler follows only slot 7.** Slots 0, 1 and 2 point at the
same byte and are never read on this path — they are inert *in this build*, not inert *in the
format*, and the distinction matters: in a standalone `.ard` those same slots point at four different
tables. A sheet that called them "unused" would be wrong about the format while right about the
build.

> ~~*CD-2 settled statically 2026-09-12 (FABLE):* nothing in the image can write `01F83530` — … the
> base is zero for the life of the process, so the resolution is an identity and the slot-7 offset a
> no-op — only injected code could change it.~~
>
> **CORRECTED 2026-09-12 (ASTRA-CONTRA-FABLE-RESOURCE-ARENA): "cannot be written" overclaimed what the
> instruments can see.** What was searched, each with its reach stated: RIP-relative operands in
> listed functions (the resolver's read `0020E602` and the encoder's `0020E620`, nothing else); the
> gap-code operand index (0); 8-byte and 4-byte absolute constants and the RVA `01E63530` anywhere in
> the file (0); and, added now, **displacements through an image-base register** — the form the step
> interpreter and `ActorResource_BeginPrimaryPayloadLoad` (`003303C5`, `[rax + r13 + 0x21A6C00]`) use —
> at `0x1E63530` (0; the control `0x1DDA5C0` finds the step table's two calls). The object just below,
> constructed at `01F83460` by `0020D2F0`, ends at `+0xC8`; no `+0xD0` write exists in its translation
> unit (control `+0xC8` found). **Not excluded:** a store through an address computed some other way, or
> a block copy spanning the slot. EXP-002's title-screen read of `0` is one live point. So the base is
> **zero at load and unwritten by every form searched**; the identity reading of slot 7 is what the
> image supports, not a proof for the process's life. The arena allocator `0036BC60` decodes its own
> links through the same base, so a non-zero base would move every arena block reference with it — a
> reason it is unlikely to change, not evidence that it does not. `CD-2` stays open for the write
> watchpoint across a load that the authored-table contract §2a queues.
>
> **A caveat stated rather than hidden.** `01F83530` lies past the raw backing of `.data`
> (`.data` RVA `0x01CD0000`, raw size `0x18E400`, so raw-backed through RVA `0x01E5E400`;
> this address is RVA `0x01E63530`). It is therefore **zero at image load**, which makes
> `FUN_0020E600` an identity function at that point. Whether anything writes it later is **not
> established here** — if something does, the resolved offset shifts and the reading above changes.
> That is the killer observation for this claim and it is named rather than assumed away.

**So four of the eight constant header fields are now proven inert and one is proven live.** The
2026-09-03 sheet said a corpus reading could not distinguish "constant field" from "field nothing
reads"; it was right that it could not, and the handler does.

**What loading normalises: nothing** — no write to the section buffer occurs on this path.
**The write path: none found.**

**Rebinding is properly torn down here**, unlike `section_004`, whose handler overwrites its global
with no release (`Sections/section-004.md` §3). Two sections in the same container, two different
lifetime policies, eight and 118 bytes of code respectively.

### The searches that failed, and why they were the wrong searches

Three searches over the certified embedded EXE (`73461d08…721f8`, 32,864,752 bytes):

1. **Literal byte search of the entire image** for `FF12AR03` and for `AR03`: **0 occurrences
   each.** For `FF12` alone: **8,385 occurrences, every one of them `.rdata` path text** of the form
   `PS2Data\image\FF12\…`, and **0 in `.text`**. So a naive scan for the family prefix returns
   thousands of hits and none of them is a magic check — the useful negative here is that the
   *specific* 8-byte magic is not stored anywhere.
2. **The named-constant route.** `"MAPARD"` is at `00D10970` with **exactly one** code reference,
   `00331D2B`, inside `FUN_003319d0`. Read below; it does not reach an `FF12AR03` parser.
3. **Displacement search, both encodings** (RIP-relative `disp32` and image-base-relative raw
   dword), for a destination table — produced nothing, because no destination table for this section
   is known. Recorded because it is the next thing a reader will try.

**All three searched outward from the section — by its magic, by its name, by its destination.** The
route that worked searches *inward* from the container: the directory walk dispatches slot 19 by
offset, never by magic or name, so no search keyed on either could reach it. The same lesson holds
for `section_004` and is recorded on both sheets because a reader will only have one open.

### What `MAPARD` is attached to — the legacy route, now known to be the dead one

`FUN_003319d0`, in the `atelload.c` translation unit, builds four sibling paths per map and streams
each. The `.ard` arm:

```
00331B13  FUN_00331f50(buf, "global" @00D1092C, "entry" @00D10924)
00331B69  ... replace the extension with "ard" @00D10938
00331CA3  FUN_0032e400(0xFF, buf)                          ; probe the size
00331D00  LEA RCX,[00D10958]                             ; "..\..\katano\atelload.c"
00331D2B  LEA RDX,[00D10970]                             ; "MAPARD" names the allocation
            ... thunk_FUN_0032e7c0(buf, alloc, size, ctx)    ; completion callback FUN_003320d0
```

So the engine's model is **`MAPARD` is a `<map>/entry/<map>.ard` file.** Note that the completion
callback it installs, `FUN_003320D0`, is **the same function as the container's slot-19 handler** —
one handler, two entry routes, exactly as `section_014` has for `LGTDAT`/`FUN_00330110`. And:

| probe | result over the 89,414-entry archive index |
|---|---|
| `/entry/` as a directory component | **0 entries** |
| `.ard` as an extension | **332 entries** — but all under `plan_map/<group>/area/<group>.ard` |
| `/area/` as a directory component | 664 entries |
| `/global/` (what the path is rewritten *from*) | 8,635 entries |

**The extension ships; the directory does not.** `FUN_003319d0` looks for `.ard` under `entry/`, and
the shipped `.ard` files are under `area/`. The size probe therefore fails and the branch is skipped,
exactly as it is for `NV_ICON` and the two `.eps` siblings, whose extensions do not ship at all.
`FUN_003319d0` is PS2-era code preserved in the build.

### The one thing this section has that the others do not

**332 standalone `.ard` files ship**, at `ps2data/plan_master/<lang>/plan_map/<group>/area/<group>.ard`,
alongside 332 `.nmb` — the same count, so they are a per-group pair. The `.ebp` `section_019`
population is 271, per map *instance* (`gol_a03`), while `.ard` is per map *group* (`gol_a`). Two
different granularities of the same named thing.

**Whether the standalone `.ard` and `section_019` are byte-compatible is not tested here** — the
`.ard` files were not extracted from the archive for this block, and a claim that two formats are
the same needs the bytes, not the name. It is the cheapest remaining experiment on this sheet and it
is written up as `PROPOSED-c9-5`.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `00D10970` | `.rdata` `"MAPARD"` — the engine's name for this unit | ✅ |
| `00D10938` | `.rdata` `"ard"` — the extension the legacy path builds | ✅ |
| `00D10924` | `.rdata` `"entry"` — the directory the legacy path builds | ✅ |
| `00D10958` | `.rdata` `"..\..\katano\atelload.c"` — the loader's source filename | ✅ |
| `003319D0` | `FUN_003319d0` — the per-map driver that names `MAPARD` | ✅ body read |
| `00331B13` | `FUN_00331f50(buf, "global", "entry")` — the directory swap | ✅ |
| `00331B69` | the extension swap to `ard` | ✅ |
| `00331CA3` | `FUN_0032e400(0xFF, buf)` — the size probe that fails | ✅ |
| `00331D2B` | `LEA RDX,[00D10970]` — the sole reference to `"MAPARD"` | ✅ |
| `003320D0` | the `.ard` stream-completion callback, installed at `00331D89`+ | ❌ not read |
| `0032E7C0` | the streamed-read enqueue | ❌ not read |

## 5. Corpus survey

**Invariants over all 271 files:**

| | |
|---|---|
| `+0x00` magic `FF12AR03` | 271 / 271 |
| `+0x08`, `+0x1C`, `+0x20`, `+0x24`, `+0x28`, `+0x34`, `+0x38`, `+0x3C` all `0` | 271 / 271 |
| `+0x10`, `+0x14`, `+0x18`, `+0x2C` all `0x30` | 271 / 271 |
| `offsetB == 0x40 + countA * 16` | **266 / 271** |
| record `+0x0A`, `+0x0C`, `+0x0E` all `0` | **2,116 / 2,116 records** |
| section length a multiple of 16 | 271 / 271 |

**Outliers, each on its own line:**

- **Five files have `offsetB == 0` with a non-zero `countA`**:
  `bog_b03` (5), `dst_a03` (5), `enw_b02` (11), `grm_e07` (5), `pla_a01` (4). On the reading in
  section 2 they simply have no table B. They are the only files that could distinguish "offset of
  table B" from "end of table A", and they are what makes the former the better reading — an
  end-offset of `0` with 11 records present would be incoherent.
- **Nine files have `countA == 0`** and still carry a table B. So the two tables are independently
  optional, and neither implies the other.
- **`+0x02 == 115` in only 9 of 2,116 records**, against 1,449 and 658 for the other two values.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `+0x0C` the end of table A or the start of table B? | **Start of table B.** The end-of-A reading predicts `offsetB == 0x40 + countA*16` universally; it fails on 5 files where `offsetB` is `0` while `countA` is 4–11. The start-of-B reading explains all 271: those five have no table B. I adopted the end-of-A reading first and this test killed it. |
| Is there really data past `offsetB`, or is that padding? | Non-zero bytes past `offsetB` in **every** file that has one, 16–256 B. Padding to the container's `0x40` alignment would be zeros. |
| Are the records 16 bytes, or was that fitted to one file? | `0x40 + countA*16` lands exactly on `offsetB` in 266 files with `countA` ranging 1–41. A wrong record size fails on the first file with a different count, and 23 distinct counts occur. |
| Are the three zero `u16` at the record tail really invariant? | 2,116 of 2,116 records across all 271 files. |
| Do `019` and `016` share a magic? | **No, and it matters.** They share the four-character prefix `FF12` and then diverge — `FF12AR03` against `FF12POS3`. Reporting them as "the same magic" would be the same conflation the container README caught between the file magic and the `0x8000000B` section marker. |
| Was an external tool consulted? | **No.** `ff12-script` does not read `section_019`. Nothing here is tier 6. |
| Could `MAPARD` name something other than `FF12AR03`? | It is one of four adjacent `.rdata` tags whose siblings match `section_016` (`POSENT`/`FF12POS3`) and `section_004` (`NV_ICON`/`NAVIICN2`), and it is built on the `ard` extension while the magic is `AR03`. Strong, and still an inference from naming — marked as one, not as tier 1. |

**What I tried that failed to break it.** I tried to close section 3 by making `FUN_003319d0` the
live reader, since it is the only function in the image that names `MAPARD`. It does not survive:
the directory it builds, `entry/`, occurs **0** times in the shipped index while the `.ard` files
that *do* ship sit under `area/`. The near-miss is worth recording — the extension matches and the
directory does not, which is a more informative failure than a total mismatch would have been.

## 7. What this document does not claim

- **No loader contract.** No `Read by` cell in section 3 holds a real instruction address, which is
  why the status is `PARTIAL`. **No field is marked `Inert`**, because a field cannot be shown inert
  by a search that never found the reader.
- ~~**No record field is decoded.** Section 2 gives measured ranges and distributions for `+0x00`
  through `+0x08`; it assigns none of them a meaning. `+0x02` with three values and `+0x08` with
  1,161 are described as *shaped like* a kind and an identifier, and that is a description of a
  distribution, not a claim about the engine.~~ **Decoded by the reader 2026-09-12 (FABLE, CC-10):**
  the consumer of `FUN_003DCF10`'s pointer is `003DCA30`, which reads each 16-byte record as
  `{u32 modelKey (a letter — the three values of `+0x02` are `m` / `n` / `s` — over a model number);
  u16 class; u16 groupId; u16 motionIndex}` and resolves a **per-model motion index** for the swing
  motion-file selection (`003DC5B0` / `003DC8D0`, [the authored-data table registry](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)), default `0x1E`; the standalone
  `.ard`'s slot 7 is the same table bound to `02B58178` and searched first, but it is 0 in every
  shipped `in` file ([the .ard loader page](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)).
- **Table B is not decoded at all** — only located, sized, and shown to be non-empty.
- **The eight constant `u32` in the header are not explained**, and `0x30` being the offset of
  `countA` is noted as suggestive and nothing more.
- **`section_019` is not claimed to be the same format as a standalone `.ard`.** The two share a
  name and a granularity mismatch (271 map instances against 332 map groups); their bytes have not
  been compared.
- **Searches that came back empty, with the method:** literal search of the entire 32,864,752-byte
  image for `FF12AR03` and `AR03` — 0 hits each. This cannot rule out a magic built by arithmetic or
  compared as two halves, the documented blind spot; the claim written is *"not stored anywhere in
  the image"*, which is what was actually measured.

## 8. Related

- [`25 — the EBP script container`](../README.md) — the directory that supplies this section's offset
- `Sections/section-016.md` — **`019` never occurs without `016`**, and `POSENT`/`MAPARD` are
  adjacent tags in one `.rdata` table read by one function
- `Sections/section-004.md` — `NV_ICON`, the sibling arm of the same `FUN_003319d0`
- `Sections/section-006.md`, `Sections/section-014.md` — the other two sections in this lane
- [`03 — World / Area / Field`](../../03-World-Area-Field/README.md) — `FUN_003319d0` carries the
  World/Area/Field mechanism context
- [`02 — Resource & Asset Pipeline`](../../02-Resource-And-Asset-Pipeline/README.md) — the archive
  index used for every "does it ship?" test on this page

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Platform — SERVICE.** The constructor of the `01F83460` object, `0020D2F0`, is the AMD ADL probe. It loads
  `atiadlxx.dll` / `atiadlxy.dll` and calls `ADL2_Main_Control_Create`, then the `PCI_VEN` / `SUBSYS` device-id parser.
  **The object whose `+0xC8` end this section notes is built by the GPU vendor probe.**
- **Presentation — CLIENT.** The motion-file selector `003DC8D0` is called by a 504-byte Presentation body.
- **ActorEntity — CLIENT and SERVICE (30 edges).** 12 inbound (ActorEntity bodies `002628B0`, `ActorResource_BeginPrimaryPayloadLoad` (00330310), `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0) call page-cited `0032E400`, `0035A3A0`, `0035AC60`); 18 outbound (page-cited `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `00330110` call ActorEntity bodies `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `00263FF0`, `ActorResource_OnDefinitionPayloadLoaded` (0032F850)). Substantive edges include `0032E400` is called by `003306E0`; `0032E400` is called by `ActorResource_BeginPrimaryPayloadLoad` (00330310); `0032E400` is called by `ActorResource_BeginManagerResourceSetLoad` (0032FCA0); `00330110` is called by `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0); the remaining edges run through shared helpers the page cites.
- **Resource — CLIENT and SERVICE (12 edges).** 8 inbound (Resource bodies `00384420`, `0039C3F0`, `0024AC30` call page-cited `0032E400`); 4 outbound (page-cited `0032E7C0`, `003319D0`, `003DC5B0` call Resource bodies `0032E400`, `0032E870`, `0032E620`). Substantive edges include `0032E400` is called by `00384420`; `0032E400` is called by `0039C3F0`; `0032E400` is called by `0024AC30`; `0032E400` is called by `00249210`; the remaining edges run through shared helpers the page cites.
- **World — CLIENT (1 edge).** 1 inbound (World bodies `00378540` call page-cited `0032E400`). Substantive edges include `0032E400` is called by `00378540`.
- **WorldAreaField — CLIENT and SERVICE (16 edges).** 12 inbound (WorldAreaField bodies `003319D0`, `003EAA00`, `MapRef_BeginLoadResources` (00268750) call page-cited `0032E400`, `00331880`, `003DCF10`); 4 outbound (page-cited `003319D0`, `003320D0`, `003EAA00` call WorldAreaField bodies `003EAA00`, `003DFA50`, `003DCF10`). Substantive edges include `0032E400` is called by `MapRef_BeginLoadResources` (00268750); `0032E400` is called by `00378030`; `0032E400` is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820); `0032E400` is called by `00379A10`.
## SWE2-EC7-33 update (2026-09-19) - `0020D2F0`

`0020D2F0` (**1,066 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,081 B, a wrong literal in the batch-33 append — the body is 1,066 B per the function list*) is the AMD ADL probe that constructs the `01F83460` object - the `ADL2_Main_Control_Create`/`ADL2_Main_Control_Destroy`/`ADL2_Adapter_NumberOfAdapters_Get`/`ADL2_Adapter_AdapterInfo_Get` name strings plus `00861EC0`/`0020E420`/`0020DE30`. Interior anchor `0020D68F` (the `00861EC0` call).

## SWE2-EC7-56 update (2026-09-19) - `0020E420`

`0020E420` (190 B) is a body - `0020D8A0` single call. Interior anchor `0020E46F` (a `0020D8A0` call).

## SWE2-EC7-57 update (2026-09-19) - `0020D8A0`

`0020D8A0` (193 B) is an indirect-only `vector<T>` resize - `imul`/`sar` capacity math with the `0x1555555555555555` magic, `"vector<T> too long"` throw via `008C2618`. Interior anchor `0020D8C7` (the `imul` capacity math).


`0020D7C0` (217 B) is the `0xC`-element vector reassign `0020D8A0` runs on `rcx`'s `{begin, end, cap}` triple: `0020D970` allocates `r14 * 0xC`, `0020D270` elementwise-copies the source range in, the old buffer's `(cap - begin) / 0xC` count is computed through the `0x2AAAAAAAAAAAAAAB` multiply-shift and `001CD050` frees it, then `begin = new`, `end = new + count*0xC`, `cap = new + r14*0xC`

Interior anchor `0020D833` (function `0020D7C0`).
