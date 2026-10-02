---
system: EBP section_004 — the NAVIICN2 map-icon block
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
corpus_validated: "1115 / 1115 us .ebp scripts, 2026-09-03 (1114 containers; section_004 in 209)"
last_reviewed: 2026-09-03
ebp_units:
  - "section_004"
audit:
  passes: 2
  last_pass: 2026-09-04
  last_pass_state: GN160-repos-c9-falsification-2-after-reopen
  crossref_clean: true
  crossref_checked: null
  crossref_report: null
  reopened_count: 1
---

# EBP `section_004` — the `NAVIICN2` map-icon block

> A second indexed directory, nested inside the container's indexed directory: ten category slots,
> each a run of 16-byte records carrying signed 2-D coordinates and a type. The engine's own name
> for it is **`NV_ICON`** — navigation icons.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` scripts (1,114 containers) |
| this unit present in | **209 (18.7 %)** |
| co-occurrence | always with `000` (209/209); `002` 202, `012` 194, `016` 117, `003` 116, `008`/`009` 79 each, `019` 65, `006` 14, `010`/`011` 1 each. **No strict pairing in either direction.** |
| size range | **128 B – 704 B, median 128 B**, only **7 distinct sizes** (128, 192, 256, 384, 576, 640, 704), every one a multiple of 16 |
| records | **650 in total across the 209 files**, 1 – 38 per file |

Two things the numbers already say. First, **this is a small format** — seven distinct sizes over
209 files, and 186 of those files are the minimum 128 B. Second, `section_004` sits in the *map*
half of the corpus: every one of the 209 is under `plan_map/…/global/`, and its strongest partners
are the other map-side sections.

---

## 1. What the player sees

**The markers on the area map.** When the player opens the map for a zone, the map is a picture and
the things drawn *on* it — the shop marker, the save-crystal marker, the exit arrows, the little
labels — are placed from data like this. `section_004` supplies, per icon, a position and a
category.

The honest limit: this sheet proves the **shape** of that data and the engine's **name** for it
(`NV_ICON`), and it does **not** prove which visual belongs to which type code. The type field takes
26 distinct values across the corpus and nothing read here maps a value to an image.

## 2. The layout

Offsets from the **start of the section body**. All fields little-endian.

```
+0x00  char[8]  magic       'NAVIICN2'                     -- 209/209
+0x08  u16      slotCount   10                             -- 209/209, never any other value
+0x0A  <slotCount * 4 bytes>  the slot directory:
         +0x00  u16  offset   from section start; 0 = slot absent
         +0x02  u16  count    number of 16-byte records in this slot
+0x32  first record run begins here
```

The header is therefore `0x0A + 10 * 4 = 0x32` bytes, and **the first non-empty slot's offset is
`0x32` in every file that has one** — the runs begin immediately after the directory.

**The directory is indexed, not packed** — exactly the design the container itself uses. A slot is a
*category*, and an absent category is a zero entry rather than a missing list. That is why the used
slot indices are sparse:

| slot | files using it | records |
|---:|---:|---:|
| 0, 1, 2 | **0** | 0 |
| **3** | 79 | 93 |
| 4 | **0** | 0 |
| **5** | 132 | 455 |
| **6** | 1 | 1 |
| 7 | **0** | 0 |
| **8** | 13 | 13 |
| **9** | 73 | 88 |

**Five of the ten slots never occur in 1,115 files**, and slot 6 occurs exactly once. Slot 5 carries
70 % of all records. As with the container, the empty indices are *observable* only because the
directory is indexed — a packed list would have hidden them.

### The record

16 bytes, fixed:

```
+0x00  s16  x1
+0x02  s16  y1
+0x04  s16  x2
+0x06  s16  y2
+0x08  s16  type      1 .. 28, and -1 in 3 records
+0x0A  u8   ?         194 distinct values
+0x0B  u8   ?         {0, 1, 64} only
+0x0C  u8   0         -- 650/650, invariant
+0x0D  u8   ?         {0, 1, 2, 3, 4} only
+0x0E  u8   ?         114 distinct values
+0x0F  u8   ?         {0, 1, 2, 3, 4, 89, 90} only
```

**The coordinates are signed.** 48 of the 650 records carry a negative `s16` in `+0x00`–`+0x06`;
read as unsigned they would be values above 65,500 next to neighbours in the 0–240 range, which is
how the sign was found. Positive values run 0 – 242.

**`+0x00..+0x03` and `+0x04..+0x07` are two points, and often the same point.** In slot 9,
`x1 == x2` and `y1 == y2` in 84 of 88 records — a degenerate box, i.e. a point marker. In slots 3
and 5 the two pairs commonly differ, so the same record shape carries both point icons and extents.

**The type field is per-slot, not global.** Slot 8 is `15` in all 13 of its records; slot 9 is `17`
in 84 of 88; slot 3 is `1` in 53 of 93 and `2` in 24; slot 5 spreads over 23 distinct values with
`12` and `14` dominant. So the slot is a coarse category and `+0x08` a finer one *within* it, rather
than two independent classifications.

## 3. The loader contract

**Established 2026-09-04.** `section_004` is slot 4 of the `EBP2` directory, and its handler is
thirteen bytes long.

```
ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources   003304A0
  00330635  CMP dword ptr [RDI+4],4      ; slotCount > 4
  0033063B  MOV EAX,[RDI+0x20]           ; slot 4's offset; 0 -> absent
  00330641  ADD RAX,RDI                  ; file base + offset
  00330646  OR EAX,EBX                   ; pack the manager index into the low nibble
  0033064B  CALL FUN_00332100
        |
        v
FUN_00332100  (13 bytes)
  00332100  MOV EAX,0xFFFFFFF0
  00332105  AND RCX,RAX                  ; recover the pointer; the manager index is DISCARDED
  00332108  JMP FUN_003DFDC0
        |
        v
FUN_003DFDC0  (8 bytes)
  003DFDC0  MOV qword ptr [rip + 0x2779F91],RCX    ; 02B59D58 = section
  003DFDC7  RET
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic `NAVIICN2` | — | — | — | **YES — never read.** `FUN_00332100` and `FUN_003DFDC0` are 21 bytes between them and neither touches the buffer |
| `+0x08` `slotCount` | — | — | — | **YES — never read on this path** |
| the slot directory | — | — | — | **YES — never read on this path** |
| record fields | — | — | — | **YES — never read on this path** |
| the section pointer | `003DFDC0` | — | — | — |

**The whole contract is: store the pointer in a global.** Nothing is validated, nothing is clamped,
nothing is normalised, and the buffer is not touched at all. `section_004` is bound, not parsed.

Three consequences a modder can use directly:

- **The `NAVIICN2` magic is inert in the strongest sense** — not "no reader found", but *the handler
  provably reads no byte of the section*. This is the same result the container sheet establishes for
  `EBP2`, reached the same way: read the whole handler and enumerate what it touches.
- **The manager index is discarded.** Slot 14 and slot 6 both index their state by manager;
  slot 4 does not — `00332105` masks the nibble off and never recovers it. **`section_004` is a
  single global binding**, so the last map to load wins, and two managers cannot hold different icon
  sets at once.
- **Rebinding does not release the previous pointer.** `FUN_003DFDC0` overwrites the global with no
  null check and no teardown call, unlike `section_019`'s handler, which explicitly tears the old
  binding down first (`Sections/section-019.md` §3). The difference is real and is visible in eight
  bytes of code.

**The global is `g_fieldRoots[2]`, and that ties this section to `section_016`.** `section-016.md`
identifies a three-slot array `g_fieldRoots` at `02B59D48`, written by `FUN_003DFE60(class, ptr)`
as `g_fieldRoots[class]`. `02B59D48 + 2*8 = 02B59D58` — **this section's global is slot 2 of that
same array**:

| slot | address | section | written by |
|---:|---|---|---|
| 0 | `02B59D48` | `section_016` (`FF12POS3`) | `FUN_003DFE60(0, ptr)` via `FUN_003320E0` |
| 1 | `02B59D50` | `section_017` — **handler exists, 0 shipped users** | `FUN_003DFE60(1, ptr)` via `FUN_00332110` |
| **2** | **`02B59D58`** | **`section_004` (`NAVIICN2`)** | **`FUN_003DFDC0`, a dedicated 8-byte store** |

**Slot 2 is written by its own function rather than through the indexed setter.** `FUN_003DFE60`
would have reached it with `class = 2` and nothing does; `section_004` gets an 8-byte writer of its
own. That asymmetry is the reason this section's binding has no teardown while `section_019`'s does.

**The consumer module.** `02B59D58` has **six** references, all RIP-relative, all inside one
module: `003DFA8A`, `003DFA9B`, `003DFC14`, `003DFCC0`, `003DFDA3` and the store at
`003DFDC0`. `FUN_003DFA50` (98 bytes) is the teardown, and its shape confirms the array reading —
it loops **twice** (`003DFA66 MOV EDI,2`) over `g_fieldRoots[0]` and `[1]` from
`003DFA5F LEA RBX,[02B59D48]`, calling `FUN_00331880` on each non-null pointer and nulling it,
then handles `02B59D58` **separately** at `003DFA8A`. Slot 2 is outside the loop in the teardown
for the same reason it is outside the indexed setter in the bind.

`FUN_003DFA50` is called at the top of `FUN_003319d0`, which is where the legacy filename path and
the container path meet.

**What loading normalises: nothing.** **The write path: none found** — no code in the image
constructs a `NAVIICN2` block, and the magic occurs zero times (below).

### The search that failed, named — and why it was the wrong search

Per the standing rule, *"no reader found"* is only worth writing down with the method attached.
Three searches, all over the certified embedded EXE (`73461d08…721f8`, 32,864,752 bytes):

1. **Literal byte search of the entire image** for `NAVIICN2`, `NAVI` and `ICN2`.
   **0 occurrences each** — not in `.text`, not in `.rdata`, nowhere. So the magic is neither a
   compare immediate nor an `.rdata` constant for a `strncmp`, which are the two forms that *did*
   find the loaders for `section_014` (`LGT2`, one `.text` immediate) and `section_006` (`TIM2`, one
   `.rdata` constant).
2. **Displacement search, both encodings**, for the data addresses this section would be bound
   into — RIP-relative `disp32` and image-base-relative raw dword. This finds candidates only once a
   destination table is known, and no destination table is known for `section_004`, so it produced
   nothing. Recorded because it is the search a reader will think to try next.
3. **The named-constant route.** The engine's name for this unit **is** in the binary —
   `"NV_ICON"` at `00D10980` — and it has **exactly one** code reference, `00331E3E`, inside
   `FUN_003319d0`. That function is read below, and it does not reach a `NAVIICN2` parser.

**All three searches started from the section and looked outward, and that is why all three failed.**
The route that worked starts from the *container* and looks in: the `EBP2` directory walk at
`003304A0` dispatches slot 4 unconditionally by offset, never by name or magic, so no search keyed
on either could have found it. Recorded because it is a general property of this container, not a
fact about `section_004`.

**The negative result was correct and the inference drawn from it was too weak.** The 2026-09-03
version of this sheet said only that the magic's absence *"is consistent with"* a container that
identifies sections by directory index. That is now **established rather than suspected**: the
handler is 21 bytes and reads no byte of the section, so the magic is not merely unfound, it is
unread. The lesson is that a failed byte search can never settle an `Inert` row — **only reading the
handler can** — and the handler was reachable all along, through the container's directory rather
than through the section's own name.

### What `NV_ICON` is attached to, and why it does not close the contract

`FUN_003319d0` is a per-map resource driver in the `atelload.c` translation unit. It builds four
sibling paths from one base and issues a streamed read for each. For the icon one:

```
00331C13  FUN_00331f50(buf, "global" @00D1092C, "icon" @00D1094C)  ; swap the directory
00331C79  ... replace the extension with "icn" @00D10954
00331CA3  FUN_0032e400(0xFF, buf)                                       ; probe the size
            ... allocate, tag with "..\..\katano\atelload.c", name it "NV_ICON" @00D10980
00331E3E  LEA RDX,[00D10980]
```

So the engine's model is: **`NV_ICON` is a `<map>/icon/<map>.icn` file.** And in this build that
file does not exist:

| probe | result over the 89,414-entry archive index |
|---|---|
| `.icn` as an extension | **0 entries** |
| `/icon/` as a directory component | **0 entries** |
| `.eps` (the sibling paths this function also builds) | **0 entries** |
| `/entry/` | **0 entries** |
| `/global/` (what the paths are rewritten *from*) | 8,635 entries |

**Every path `FUN_003319d0` constructs names a directory that does not ship.** The size probe
returns nothing, the guarded branch is skipped, and no allocation is made. `FUN_003319d0` is
PS2-era: it is the code that loaded these payloads when they were four separate files, and in the
shipped build the same payloads travel as sections inside the `.ebp` container instead.

That is why the `NV_ICON` reference does not give a loader contract. It names the data and proves
what the data *is*; it does not read it.

### What is therefore still open

The live reader of `section_004` — whatever consumes the block once the container hands it over —
is **not identified**. `PROPOSED-c9-4` in the inbox carries it.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `00D10980` | `.rdata` `"NV_ICON"` — the engine's name for this unit | ✅ |
| `00D10954` | `.rdata` `"icn"` — the extension the legacy path builds | ✅ |
| `00D1094C` | `.rdata` `"icon"` — the directory the legacy path builds | ✅ |
| `00D10958` | `.rdata` `"..\..\katano\atelload.c"` — the loader's own source filename | ✅ |
| `003319D0` | `FUN_003319d0` — the per-map driver that names `NV_ICON` | ✅ body read |
| `00331C13` | `FUN_00331f50(buf, "global", "icon")` — the directory swap | ✅ |
| `00331C79` | the extension swap to `icn` | ✅ |
| `00331CA3` | `FUN_0032e400(0xFF, buf)` — the size probe that fails | ✅ |
| `00331E3E` | `LEA RDX,[00D10980]` — the sole reference to `"NV_ICON"` | ✅ |
| `00331A91` / `00331B69` / `00331D2B` / `00331DB3` / `00331EC9` | the sibling `entry`/`ard`/`MAPARD`/`POSENT`/`TREENT` arms of the same function | ✅ |
| `0032E3F0` | builds the base path (`FUN_0032e3f0(5, mapIndex * 3, buf, 0x103)`) | ❌ not read |
| `00331F50` | the substring replace | ❌ not read |
| `0032E400` | the size probe | ❌ not read |

## 5. Corpus survey

**Invariants over all 209 files:**

| | |
|---|---|
| `+0x00` magic `NAVIICN2` | 209 / 209 |
| `+0x08` `slotCount == 10` | 209 / 209 |
| first non-empty run starts at `0x32` | 209 / 209 |
| runs contiguous — each run ends exactly where the next begins | **209 / 209, 0 violations** |
| every run inside the section length | 209 / 209 |
| record `+0x0C == 0` | **650 / 650 records** |
| section length a multiple of 16 | 209 / 209 |

The contiguity check is the strong one: it means the directory is **not** a free-form offset table
but a partition of one packed record array, and any editor that grows a slot must move every slot
after it.

**Outliers:**

- **Slot 6 is used by exactly one file**, with exactly one record.
- **3 records carry `type == -1`** (`+0x08 = 0xFFFF`) where every other record is `1 .. 28`.
- **`+0x0B` takes the value `64` in 40 records** and `1` in 42, and is `0` in the other 568 — a flag
  byte with two rare settings rather than a range.
- 186 of 209 files are the minimum 128 B — a header plus at most four records.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the directory really 10 slots of `(u16,u16)`, or was that fitted to one file? | Tested on all 209 by *prediction*: from `slotCount` alone, compute the header end, then require every non-zero slot to start at the header end or at the end of the previous run, to be ascending, and to fit. **0 violations in 209 files.** A wrong stride or a wrong pair order would have failed on the first multi-slot file, and 130 files have two or more slots. |
| Are the offsets relative to the section or to the file? | **Section.** The first run is at `0x32`, which is the header size, and the container's slot-4 offset is a different number in every file. Read as file offsets they would land inside other sections. |
| Are the coordinates signed or unsigned? | **Signed.** 48 records would otherwise carry values above 65,500 adjacent to values under 250 in the same field. Signed is the reading that makes the population continuous. |
| Is `+0x0C == 0` a real invariant or an artefact of a small sample? | 650 of 650 records, across all 209 files and all five used slots. It is the only byte in the record that never varies. |
| Could `NV_ICON` name something else, and the `NAVIICN2` match be coincidence? | The tag table at `00D10970`–`00D10988` is `MAPARD`, `POSENT`, `NV_ICON`, `TREENT`, and three of the four line up with section magics — `POSENT` with `section_016`'s `FF12POS3` and `MAPARD` with `section_019`'s `FF12AR03`. A single coincidence is possible; three in a four-entry table adjacent in `.rdata` is not the shape of coincidence. **It is still an inference from naming, and this sheet marks it as one.** |
| Was an external tool consulted? | **No.** `ff12-script` does not read `section_004`; no tool in the kit does. Nothing here is tier 6, and nothing here is corroborated by one either — which is why section 3 is thin rather than confidently wrong. |
| Did the "no reader found" search actually cover the binary? | It covered the certified embedded EXE in full — a literal search of all 32,864,752 bytes, not of `.text` only. What it cannot cover is a magic **constructed** rather than stored, which is the documented arithmetic-constant blind spot. So the correct statement is *"no stored occurrence of the magic anywhere in the image"*, and that is what is written. |

**What I tried that failed to break it.** I tried to make `FUN_003319d0` the live reader — that
would have closed section 3 neatly. It does not survive: the four directories it builds
(`entry`, `icon`, `treasure`, and the `.ard` sibling) occur **0, 0, 0** times respectively in the
shipped index while `/global/` occurs 8,635 times. The tidy answer was the wrong one, and the
measurement that killed it is in section 3.

## 7. What this document does not claim

- ~~**No loader contract.** Section 3 has no `Read by` entry that is a real instruction address. That~~
  ~~is the main gap in this sheet and the reason its status is `PARTIAL`, not `DOCUMENTED`.~~ *(answered: §3, established 2026-09-04, is the loader contract — `FUN_00332100` → `FUN_003DFDC0` stores the pointer and reads nothing; the front matter says `status: AUDITED`; 2026-10-02, OPUS)* Until the
  live reader is found, nothing here can say what is rejected, clamped or ignored~~ — and **no field~~
  ~~below is marked `Inert`**, because "no reader found" is not "inert" when the reader itself has not~~
  ~~been located.~~ *(answered: §3 marks four fields `YES — never read` on the handler path; 2026-10-02, OPUS)*.
- **No type-to-icon mapping.** `+0x08` takes 26 values and this sheet maps none of them to a visual.
- **`+0x0A`, `+0x0B`, `+0x0D`, `+0x0E`, `+0x0F` are undecoded.** Their value distributions are in
  section 2 because a distribution is a fact even when the meaning is not.
- **The 2-D coordinate space is not identified.** Values run roughly −8 to 242 and the section is
  map-side, so map-image pixels is the obvious guess; nothing here tests it, and it stays a guess.
- **The `.icn` file format is not claimed to equal `section_004`.** The PS2 build's `icon/*.icn`
  files do not ship and cannot be compared byte-for-byte with anything in hand.

## 8. Related

- [`25 — the EBP script container`](../README.md) — the directory that supplies this section's offset
- `Sections/section-019.md` — `MAPARD`, the sibling tag in the same four-entry `.rdata` table, and
  the sibling arm of the same `FUN_003319d0`
- `Sections/section-016.md` — `POSENT`, the third tag in that table
- `Sections/section-006.md`, `Sections/section-014.md` — the other two sections in this lane
- [`03 — World / Area / Field`](../../03-World-Area-Field/README.md) — `FUN_003319d0` carries the
  World/Area/Field mechanism context
- [`16 — UI`](../../16-UI/README.md) — the eventual consumer, once the live reader is found

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Presentation — CLIENT.** The size probe `0032E400` is also called by two Presentation bodies, of 119 and 337 bytes.
It is a shared file-size query, not specific to this section.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (28 edges through 9 of this page's functions).** The ActorEntity layer reaches this page at `003304A0`, `0032E400`, `003DFE60`, `0032E3F0` and 5 more. `FUN_002628b0` is the worked example, read in full - it is a 1,689-byte manager routine that indexes `02098E10` at the **`0x288` stride** - the same records the manager indexer walks - in a `0x50`-byte frame with a stack cookie; **5 of the 21 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
- **Resource — CLIENT and SERVICE (9 edges).** 8 inbound (Resource bodies `00384420`, `0039C3F0`, `0024AC30` call page-cited `0032E400`); 1 outbound (page-cited `003319D0` call Resource bodies `0032E400`). Substantive edges include `0032E400` is called by `00384420`; `0032E400` is called by `0039C3F0`; `0032E400` is called by `0024AC30`; `0032E400` is called by `00249210`; the remaining edges run through shared helpers the page cites.
- **World — CLIENT (1 edge).** 1 inbound (World bodies `00378540` call page-cited `0032E400`). Substantive edges include `0032E400` is called by `00378540`.
- **WorldAreaField — CLIENT and SERVICE (16 edges).** 11 inbound (WorldAreaField bodies `003319D0`, `MapRef_BeginLoadResources` (00268750), `00378030` call page-cited `0032E400`, `00331880`, `0032E3F0`); 5 outbound (page-cited `003319D0`, `003320E0`, `00332100` call WorldAreaField bodies `003DFE60`, `003DFA50`, `003EAA00`). Substantive edges include `0032E3F0` is called by `003319D0`; `0032E400` is called by `MapRef_BeginLoadResources` (00268750); `0032E400` is called by `00378030`; `0032E400` is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820).
## The `003319D0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`003319D0` (~375 B) — seven-register section-004 body
(`003319D0`/`003319E2`).

| member | role | interior |
| --- | --- | --- |
| `00331F50` | `r11 = rsp` `0x190` stack-cookie frame (`00331F50`/`00331F65`) | [`00331F50`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-section-004-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003DFCC0` | 50 B | loads qword `02B59D58` and returns 0 when it is null, when its byte `+0x7` is below 0x32 (unsigned), when `ecx` is not below its word `+0x8` (signed compare), when `ecx` is 0 or when `ecx - 1` is above 8 (unsigned); otherwise returns the word at `+0xC + ecx*4` | `003DFCC7`, `003DFCCC`, `003DFCD6`, `003DFCE1`, `003DFCE9` |
