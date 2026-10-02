---
system: EBP section_016 — the POSENT position-entry table
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
corpus_validated: "1115 / 1115 us .ebp scripts, 2026-09-03; 1114 containers; 25,687 records"
last_reviewed: 2026-09-03
ebp_units:
  - "section_016"
audit:
  passes: 2
  last_pass: 2026-09-04
  last_pass_state: GN160_99P636
  last_pass_by: repos-c9
  last_pass_independent: true
  crossref_clean: true
  reopened_count: 0
  corrections: 1
---

# EBP `section_016` — the POSENT position-entry table

> A flat list of authored **places on a map**: a point on the ground, the direction something
> standing there should face, and — for some entries — a rectangle around it. The engine's own
> name for this section is **`POSENT`**.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` scripts (1,114 containers) |
| this unit present in | **517 (46.4 %)** |
| co-occurrence | always with `section_000` (517/517); with `012` 396 (77 %), `019` 271 (52 %). With `010`/`011` only 4 times. Not a member of either strict pair |
| **subtree split** | **`plan_map` 517 of 769 — `event` 0 of 345.** A position table never appears in an event script |
| size range | 256 B – 9,280 B, median 2,176 B |
| record population | **25,687 records** across the 517 files; per file 3 – 191, median 42 |

The subtree split is the strongest single fact in this table and it is not a tendency — it is
absolute. **`section_016` is a property of a map, not of a cutscene.**

---

## 1. What the player sees

Nothing draws this section. What it *causes* is that a map has **specific, authored spots** rather
than arbitrary ones.

When you walk through a zone exit in the Estersand and arrive in the next area, you arrive **facing
a particular way**, standing in a particular place — not at the geometric edge of the map, and not
facing whatever direction you happened to be walking. When a Save Crystal, a Gate Crystal or a
merchant stands somewhere, something had to say *where* and *which way round*. This section is the
list those come out of: for each entry, a spot on the ground and a heading.

The heading is the tell that these are authored by hand rather than computed. Of the 2,069 entries
that specify a non-zero heading, **97.5 % are a whole number of degrees** — 60°, 30°, 45°, 90°,
135°, 180°. Somebody typed those numbers.

Some entries also carry a **rectangle** rather than being a bare point, which is what an area you
can be *inside* looks like, as opposed to a spot you stand *on*.

## 2. The layout

Offsets are **from the start of the section**, which is where the container directory's slot 16
points. The section carries its own length and does **not** depend on the container's
"distance to the next present offset" rule.

```struct Ff12Pos3Header base=section size=0x10
+0x00  char[8]  magic   FF12POS3 in 517 of 517
+0x08  u32      size    = 0x10 + 0x30 * count, exact in 517 of 517
+0x0C  u32      count   records that follow; 3 .. 191, median 42
```

The `count` records begin at `+0x10`, stride `0x30`. A single terminator dword `0x0000000A` sits at
`+size` in 517 of 517 files; it is outside the header struct and has no reader (§7).

**One record, 0x30 bytes.**

```struct Ff12Pos3Record base=record size=0x30
+0x00  u32   type      0, 1 or 2 only, in all 25,687 records
+0x04  f32   extentA   1.0 for type 0; varies for type 1
+0x08  f32   extentB   1.0 for type 0; varies for type 1
+0x0C  f32   extentC   1.0 in 25,685 of 25,687
+0x10  f32   posX
+0x14  f32   posY
+0x18  f32   posZ
+0x1C  f32   dir       heading in RADIANS, authored in whole degrees
+0x20  f32   _zero0    0 in 25,687 of 25,687
+0x24  f32   _zero1    0 in 25,687 of 25,687
+0x28  f32   _zero2    0 in 25,687 of 25,687
+0x2C  f32   _zero3    0 in 25,687 of 25,687
```

> **This fence reports zero `UNACCOUNTED` bytes, and that does not mean the record is fully
> explained.** Nine of the twelve fields are measured facts; `extentA`/`extentB`/`extentC` are named
> by **inference** — they are sizes because `type == 1` records vary them while `type == 0` records
> hold `1.0`, not because any reader was found that treats them as sizes. Which axes they measure is
> open (§7). **An accounted byte is not an explained one, and a complete fence can launder an
> unknown into a clean check** — flagged here rather than left for a reader to discover.

**`dir` is stored in radians and was authored in degrees.** Convert with `degrees = dir * 180 / π`.
Of the 2,069 records with a non-zero `dir`, **2,017 (97.5 %) land on a whole degree** — corrected
from 2,018, see §6. The observed
range is −2.861 to +5.760 rad (−164° to +330°), so it is **not** normalised to ±π and a reader must
not assume it is.

`type` partitions the corpus:

| `type` | records | `+0x04` / `+0x08` | reading |
|---|---:|---|---|
| `0` | 20,867 | both `1.0` in 20,008 | a bare point — the extent triple is inert filler |
| `1` | 4,801 | vary: 12.0, 10.0, 8.0, 6.0, 4.0 | a rectangle around the point |
| `2` | 19 | near-equal pairs (32/31, 25/25, 4/4, 15/15) | a third shape~~, too rare to characterise~~: an ellipse *(answered: `CC-3`, §5 — `00236513`–`00236586`; 2026-10-02, OPUS)* |

For `type == 1` the smaller of `+0x04`/`+0x08` clusters at 6.0 (1,266), 12.0 (1,263), 4.0 (530) and
8.0 (486) — **both numbers are substantial**, so these are rectangles with real width in both axes,
not thin walls. 1,633 of the 4,801 are exactly square.

## 3. The loader contract

**The section is bound whole, by pointer. Nothing is parsed, copied, clamped or normalised when it
loads.** Every field below is read later, on demand, by the record accessor.

### How it is bound

The engine's own name for the section is the string **`POSENT`** at `.rdata` `0x00D10978`,
referenced **exactly once** in the image, from `0x00331DB3` inside `FUN_003319d0`. The surrounding
assertions cite `..\..\katano\atelload.c` (`0x00D10958`) at line `0x564` (**1380**) — the
translation unit that loads the EBP container.

The completion handler is `FUN_003320e0`, five instructions:

```
003320e0  MOV  EDX, ECX          ; the loaded section pointer, tag bits in the low nibble
003320e7  AND  RDX, RAX          ; RAX = 0xFFFFFFF0 -- clear the low 4 bits
003320ea  XOR  ECX, ECX          ; format class 0
003320ec  JMP  FUN_003dfe60      ; tail call
```

and `FUN_003dfe60` is the whole of the "load":

```
003dfe60  MOVSXD RAX, ECX
003dfe63  LEA    RCX, [0x02B59D48]        ; g_fieldRoots
003dfe6a  MOV    [RCX + RAX*8], RDX       ; g_fieldRoots[0] = section pointer
003dfe6e  RET
```

**`POSENT` is format class 0** (`0x003320EA`) and lands in `g_fieldRoots[0]` at `0x02B59D48`.
The array has three slots (`0x02B59D48`, `+0x08`, `+0x10`); `FUN_003dfa50` tears down all three,
walking the first two from `0x003DFA5F`.

### What actually reads the bytes

`FieldData_CopyIndexedRecordByFormatClass` (`0x003DFD00`, 44 instructions) is the accessor. It
takes `(formatClass, index, out)` and fills a 0x30-byte output.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic bytes 0–6 (`FF12POS`) | — | — | — | **yes — no reader found; see the search below** |
| `+0x07` magic byte 7 (the version digit `'3'`) | `FieldData_CopyIndexedRecordByFormatClass` `0x003DFD2C` | — | — | — |
| `+0x08` `size` | — | — | — | **yes — not read by the accessor at `0x003DFD00`** |
| `+0x0C` `count` | `0x003DFD33` (current path), `0x003DFD69` (legacy path) | `index >= count` → returns 0, reads nothing | — | — |
| record `+0x00 .. +0x2F` | copied verbatim, `0x003DFD48`–`0x003DFD63` | — | — | — |

**The magic *is* checked — but only its last byte, and as a version number.**

```
003dfd2c  CMP  byte ptr [R9 + 0x7], 0x33     ; the '3' of 'FF12POS3'
003dfd31  JC   003dfd69                      ; below '3' -> the legacy record layout
```

This is why searching `.text` for the literal `FF12POS3`, for `FF12`, or for the dword `POS3`
returns nothing: **the comparison is one byte wide.** The check is a *format-version* test, not an
identity test — any file whose byte 7 is `'3'` or greater takes the 48-byte-record path, whatever
its first seven bytes say. A modder can corrupt `FF12POS` freely and nothing happens; changing the
`3` switches the engine to a different record layout and misparses the file.

**The two record layouts.** Under `byte[+7] >= '3'` the accessor copies the 48-byte record verbatim
in three SSE moves — `[R9 + RCX*8 + 0x10]`, `+0x20`, `+0x30` with `RCX = index * 6`, that is
**base + 0x10 + index * 0x30**, exactly the layout §2 derives from the corpus (`0x003DFD3C`
computes `index*3`, `0x003DFD45` doubles it, the `*8` addressing scale completes `*0x30`).

Under `byte[+7] < '3'` (`0x003DFD69`–`0x003DFD9A`) records are **0x10 bytes** at
`base + (index + 1) * 0x10` (`0x003DFD75` `INC RCX`, `0x003DFD78` `SHL RCX,4`), and the four dwords
it reads are stored to output **`+0x10`, `+0x14`, `+0x18`, `+0x1C`** (`0x003DFD81`, `0x003DFD88`,
`0x003DFD8F`, `0x003DFD96`), with the output's type byte forced to 0 at `0x003DFD6F`.

> **That back-compatibility path is independent proof of the field assignment.** The engine maps a
> legacy 4-float record onto output offsets `0x10/0x14/0x18/0x1C` — so those four slots are the
> position triple and the heading, established from the binary and not from any external tool.

**What loading normalises:** nothing. The output buffer is zeroed first (`0x003DFD10`–`0x003DFD23`,
six 8-byte stores covering all 0x30 bytes), so a rejected index yields an all-zero record rather
than stale data. That is the only normalisation anywhere in the path.

**The write path is not documented here.** The game ships these files; no writer was found, and §7
names the search that failed.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x00D10978` | `.rdata` — the string `POSENT` | ✅ |
| `0x00D10958` | `.rdata` — `..\..\katano\atelload.c`, 20 assertion sites | ✅ |
| `0x00331DB3` | the single reference to `POSENT`, inside `FUN_003319d0` | ✅ |
| `0x003320E0` | `FUN_003320e0` — completion handler; class 0 selected at `0x003320EA` | ✅ |
| `0x003DFE60` | `FUN_003dfe60` — `g_fieldRoots[class] = ptr`; the store is `0x003DFE6A` | ✅ |
| `0x02B59D48` | `g_fieldRoots[0]` — where the section pointer lives | ✅ |
| `0x003DFD00` | `FieldData_CopyIndexedRecordByFormatClass` — version gate `0x003DFD2C`, bound `0x003DFD33`, copy `0x003DFD48` | ✅ |
| `0x003DFA50` | `FUN_003dfa50` — teardown; slot walk at `0x003DFA5F` | ✅ |
| `0x003DFAC0` | `FUN_003dfac0` — also reads slot 0, incompatibly; see §7 — **unreachable** (CC-4, 2026-09-12) | dead |

## 5. Corpus survey

**Invariants, each checked over all 517 files, never over the file that was opened first:**

| | |
|---|---|
| magic `FF12POS3` | **517 / 517** |
| `+0x08 == 0x10 + 0x30 * count` | **517 / 517, exact** |
| terminator dword `0x0000000A` at `+size` | **517 / 517** |
| bytes after the terminator all zero | **516 / 517** |
| record `+0x20`, `+0x24`, `+0x28`, `+0x2C` | **`0` in all 25,687 records** |
| record `+0x0C` | `1.0` in **25,685 of 25,687** |
| `type` | only `0`, `1`, `2` — no other value in 25,687 records |
| fully-zero records | **none** — 0 in every one of the 517 files |

Those four always-zero dwords are 16 bytes of every record, **a third of each record and 8 % of the
whole section**, and the accessor copies them anyway. They are a finding, not an absence: a field
that is `0` in 25,687 of 25,687 records is a different fact from a field nobody looked at.

**Outliers, which deserve their own lines:**

- **`us/plan_map/slm_a/slm_a01/global/slm_a01.ebp` is the only file with non-zero bytes after the
  terminator.** At section `+0x700` it carries `{0, 0x730, 1}` and at `+0x730` four floats
  (`135.01`, `−0.204`, `138.70`, `0.551`) — self-consistent, since `0x730` is exactly where those
  floats sit, and shaped like a position plus a 31.6° heading. **One occurrence cannot tell an
  optional sub-table from stale authoring residue**, and nothing in the loader reads past `count`.
  Recorded as `CC-2`.
  **CC-2 answered 2026-09-12 (FABLE): residue.** The same test over every `section_016` in every
  language tree of `FFXII_TZA.vbf` — 4,653 containers, all with the `FF12POS3` magic and the
  `0x0000000A` terminator exactly at `0x10 + 0x30·count` — finds non-zero bytes after the terminator
  in **nine** files, and they are the nine localised copies of `slm_a01.ebp` (`us`, `kr`, `it`, `in`,
  `fr`, `es`, `de`, `cn`, `ch`), byte-identical: `size` 1744, `count` 36, first non-zero at section
  `+0x704` = `{0x730, 1, 0…}`. One master, not a second occurrence; by this bullet's own criterion
  the sub-table reading has no support and the bytes are authoring residue the loader never reads.
- Two records of 25,687 break the `+0x0C == 1.0` invariant: one `0.0` and one `−1.0`.
- The section length the container implies always exceeds the declared `size` by 96–176 bytes —
  one or two whole `0x40` blocks beyond the minimum alignment padding. The packer reserves slack;
  **the declared `size` is authoritative and the container-derived length is not.**

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the offset relative to the file or the section? | **Section.** Settled from the binary, not by assumption: `0x003DFD48` addresses `[R9 + RCX*8 + 0x10]` where `R9` is the very pointer stored at `0x003DFE6A`. |
| Does this hold on the whole corpus or on the file that was opened? | Every invariant in §5 carries its own count over all 517 files and all 25,687 records. The two-record and one-file exceptions are named rather than rounded away. |
| Could the decompiler have invented a value the instruction stream does not have? | **Yes, and it did.** The decompiled `FieldData_CopyIndexedRecordByFormatClass` renders the copy as five `u64` assignments that skip record `+0x00..+0x07`. The instruction listing shows three `MOVUPS` pairs copying the **whole** 0x30 record. §3 follows the listing. That function's evidence record also states `ABI CC=unknown`, so no argument mapping in this document rests on the decompiler's signature. |
| If an external tool agrees, was it consulted **after** the reading or **before**? | **After.** §2 was derived from the corpus and §3 from the binary before `ff12-pos.exe` was run. |
| Does the tool actually agree? | **Yes, and this document claims more than it prints.** `ff12-pos.exe -u` over an 80-file random sample (seed 7) gives **4,172 records, 4,172 agreements, 0 disagreements** on `type`, `posx`, `posy`, `posz`, `dir`. The tool emits no name for `+0x04`/`+0x08`/`+0x0C` (it prints them as `unknown1[]`) and never prints `+0x20..+0x2C` at all. |
| Is the magic really unchecked, or is the search blind? | **The search was blind, and the check exists.** `FF12POS3`, `FF12POS` and `POS3` occur 0 times in the image; `FF12` occurs 8,385 times and **every one is `.rdata` path text, 0 in `.text`**. The positive control works — the same scan finds `cmp dword ptr [rcx], 'CAM7'` at `0x002561C8`, `'SHK1'` at `0x0037DA96`, `'LGT2'` at `0x0037AABF`, and `SRYK` where the VBF sheet says it is. The check for this section is one byte wide (`0x003DFD2C`) and no whole-magic search could have found it. |
| Could `dir` be something other than an angle? | It would have to be a quantity whose non-zero values land on a whole number of degrees 97.5 % of the time by coincidence, and whose commonest values are 60, −60, 30, 45, 90, 135 and 180. |

### Independent pass — 2026-09-04, by `repos-c9`, who did not write this sheet

Re-derived from the raw 1,115 containers with a different parser, and from the certified EXE with
capstone instead of Ghidra. **Every corpus figure above reproduced** — the `size` arithmetic 517/517,
the `count` range and median, the `0x0A` terminator 517/517, 25,687 records, the `type` histogram
`0:20867 1:4801 2:19`, `+0x0C == 1.0` in 25,685, `+0x20..+0x2C` zero in all, `dir` non-zero 2,069,
and the `dir` range — plus `g_fieldRoots` at `0x02B59D48` confirmed from `0x003DFA5F`.

**One figure did not reproduce, and the auditor was right.**

> **CORRECTION.** This sheet published **2,018** whole-degree headings. The correct figure is
> **2,017**. What was believed: that rounding a heading to two decimal places and then testing the
> result against the nearest integer measures whether the heading is a whole number of degrees. What
> is now believed: that it over-counts by one. What proved it: `abs(57.99 - 58)` evaluates to
> `0.00999999999999801`, which passes a `< 0.01` test, so the record `dir = 1.01206005` rad
> (57.98677°, a true error of **0.0132°** — not a whole degree by any honest reading) was counted as
> one. Measuring the degrees directly against the nearest integer gives **2,017**, and `repos-c9`
> showed that figure is stable across tolerances from `1e-4` to `1e-2`, a hundredfold range.
>
> **Why the earlier reading was reachable:** the intermediate rounding looked like a tidy-up and was
> actually a second comparison with its own error. **A tolerance applied to an already-rounded value
> is not the tolerance you wrote down** — and a binary floating-point literal near the boundary
> decides which side it falls on. The claim it supports is unchanged: 97.49 % against 97.53 %, and
> *"authored in whole degrees"* survives either way. **The claim was never at risk; the number was
> wrong, and a wrong number in a sheet is a defect whatever it supports.**

`repos-c9` explicitly did **not** audit `CC-4` or the `+0x04`/`+0x08` axis
assignment, having no independent instrument for either. **Both remain untested by anyone but their
author.**

**The killer observation for the central claim** — *"records are 0x30 bytes starting at +0x10"* —
would be a file where `+0x08 != 0x10 + 0x30 * count`, or an accessor with a different stride. The
first was tested on all 517 files and did not appear; the second is contradicted by
`0x003DFD3C`–`0x003DFD48`.

## 7. What this document does not claim

- ~~**What consumes a position entry.** `FieldData_CopyIndexedRecordByFormatClass` has four direct
  callers; they were not read in this block. Until they are, §1's account of *which* spots these
  are — arrival points, crystals, area volumes — is a plausible reading of the data's shape and
  distribution, **not** a proven mapping.~~ **`CC-1` answered 2026-09-12 (FABLE).** The four direct
  callers, all with format class 0: **`FieldData_GetFormat0RecordVectorByIndex`** (`00320940`, returns
  the record's `+0x10` / `+0x14` / `+0x18` floats), `003209C0` (the whole record, `−1` / `0`), the
  script verb **`setentrypos`** (`0x0405`, `00354FB0`) and **`debug_positioninfo`** (`0x2059`,
  `0050EBA0`, class from its argument; [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)). The vector getter's own callers name the
  entries' uses: **the enemy wander orders** — the locomotion opcode family `0x4000 + k` samples
  within ± its parameter of **entry `k + 1`** (`00312DF0`, [the locomotion page](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md) DE-4) — and a second goal
  helper (`00312B40`); **the AI condition "distance from entry `operand + 1`"** (selector opcodes
  36 / 37, [the gambit page](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) Z-1); **the spawn lifecycle anchor** (`SpawnLifecycle_CheckAndRetireByNativeRange`,
  [spawn placement](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)); two **fixed indices** the engine reserves — `BattleLocomotion_SolveClassMode2Step`
  steers against **entry 8** (`003394DB`) and `0033DB60` reads **entry 32** (`0033DB90`); and the
  script verbs **`btlAtelGetPositionDataX` / `Y` / `Z`** (`0x3032`–`0x3034`), which hand a component
  of any entry to a script. So a `POSENT` entry is the area's authored **reference position**: wander
  centres, AI distance anchors, spawn anchors, script-readable points, with entries 8 and 32 having
  engine-fixed roles — not arrival points or volumes as such, though scripts may use them so.
- ~~**Which axes `+0x04` and `+0x08` measure.** They are a rectangle's two horizontal sizes; whether
  the pair is (X, Z) or (X, Y) is not established, and `+0x0C` being `1.0` almost everywhere leaves
  the third axis unconstrainable from the corpus.~~ **`CC-3` answered 2026-09-12 (FABLE): (X, Z), in
  the record's own frame.** `SpawnPoint_GeneratePositionFromAuthoredRegion` (`00236450`; a consumer of the shared gameplay LCG on [the RNG streams page](../../21-RNG-And-Determinism/rng-streams.md) — *re-pointed 2026-09-14 (FABLE): the link went to spawn placement, which does not name this function*)
  fetches the whole record through `003209C0` and switches on `type`: **0** copies `posX / posY / posZ`
  out unchanged (`00236643`–`00236660`); **1** draws `u` in `(−A/2, A/2)` and `v` in `(−B/2, B/2)` with
  `A = +0x04`, `B = +0x08` (each halved at `0023649D` / `002364B4`, sampled at 1/100 resolution from
  [the shared gameplay LCG](../../21-RNG-And-Determinism/rng-streams.md), sign flipped by a further draw's bit 4, `00236588`–`0023661F`); **2** draws `u` the
  same way and bounds `v` by the ellipse `sqrt(B² − u²·B²/A²)` (`00236513`–`00236586`). Then `00319390`
  rotates the offset `{u, ·, v}` by `dir` (`+0x1C`) through the 32K-entry sine table and adds it to
  `posX / posZ` (`003193A7`–`00319415`) — `u` moves the **x** output, `v` the **z** output, and **y** is
  never touched. So `extentA` is the rectangle's (or ellipse's) full **X** size and `extentB` its **Z**
  size, both in the local frame the heading rotates; `+0x0C` is not read by this sampler.
- **`type == 2`.** Nineteen records in 25,687. ~~Too few to characterise honestly.~~ *(answered: an elliptical region — `CC-3` above, `00236513`–`00236586`; 2026-10-02, OPUS)*
- ~~**`FUN_003dfac0` (`0x003DFAC0`) reads slot 0 incompatibly.** It gates on `byte[+7] > '1'` and
  then treats `+0x08` as an image offset to resolve (`0x003DFACF` onward), indexing a nested table
  with stride `0x20`. For `FF12POS3`, `+0x08` is the total size (`0x670` in the sample file), not a
  resolvable offset. **Either slot 0 holds something other than `POSENT` at some point in the
  frame, or one of these two readings is wrong.** Not resolved in this block —
  `CC-4`. Flagged rather than smoothed over.~~ **`CC-4` resolved 2026-09-12 (FABLE): neither —
  the function is unreachable.** `003DFAC0` has no `call` or `jmp` in any censused function, no
  rip-relative reference, and its address occurs nowhere in the file as a dword or qword (a
  function-pointer table would show it); its body (`003DFAC0`–`003DFB45`, read whole) takes
  `(i, j)`, requires `byte[+7] >= '2'`, resolves `+0x08` as an offset to a table `{u32 count; …;
  {s32 tableOff, s32 count}[i] at +8, 16-byte stride}` and returns `root + tableOff + 32·j`. That is a
  reader for an **earlier `FF12POS` layout** in which `+0x08` pointed at a nested table of 32-byte
  records — the linker kept the body, nothing calls it, and the shipped `FF12POS3` accessor at
  `0x003DFD00` is the only live reader of slot 0. So slot 0 never holds anything but `POSENT`, and
  the "incompatible" reading is dead code, not a second format.
- **The write path.** No writer was found, but the search that failed was a scan for the magic and
  for references to `g_fieldRoots`; that is not the same as establishing there is none.
- **The `0x0000000A` terminator's purpose.** Present in 517 of 517 files, and **no reader was found
  for it** by the same reference scan that located all five readers of `0x02B59D48`. The accessor
  bounds on `count`, never on the terminator.
- Nothing here is claimed for any language other than `us`. The corpus is one of nine.

## 8. Related

- [`../README.md`](../README.md) — the EBP container and the 14 scored units
- [`section-012.md`](section-012.md) — **the per-map actor manifest**, the other section this session read; co-occurs with `016` in 396 files. *(Corrected 2026-09-08: this line labelled it `CHRMDL`, a tag that appears nowhere in `section-012.md` and nowhere else in the database outside `_inbox/`. The target's own `system:` line is used instead — whether `CHRMDL` belongs to some section is unresolved and is not asserted here.)*
- `section_019` (`FF12AR03` / `MAPARD`) and `section_004` (`NAVIICN2` / `NV_ICON`) are loaded by the
  same function, `FUN_003319d0`, and are owned by `repos-c9`
- [`../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md`](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
  — `section_000`, the bytecode this container's other half carries

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Party — SERVICE.** The distance helper `00312B40` resolves units through `BattleUnit_ResolveByFocusHandle` and
`BattleUnit_GetPartyLeader`, so the AI distance condition resolves its units through the party-control lookups.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — SERVICE.** A 1,398-byte function this page cites calls the 80-byte Resource size probe.
- **ActorEntity — CLIENT and SERVICE (5 edges).** 4 inbound (ActorEntity bodies `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `002628B0`, `003320E0` call page-cited `003DFE60`, `003320E0`, `003DFA50`); 1 outbound (page-cited `00312B40` call ActorEntity bodies `BattleUnit_FindByDefinitionSelector` (002367A0)). Substantive edges include `003320E0` is called by `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0); `003DFA50` is called by `002628B0`; `003DFE60` is called by `003320E0`; `003DFE60` is called by `00332110`; the remaining edges run through shared helpers the page cites.
- **CombatAI — CLIENT (1 edge).** 1 inbound (CombatAI bodies `AiOrder_EvaluateTargetSelector` (00301AD0) call page-cited `FieldData_GetFormat0RecordVectorByIndex` (00320940)). Substantive edges include `FieldData_GetFormat0RecordVectorByIndex` (00320940) is called by `AiOrder_EvaluateTargetSelector` (00301AD0).
- **Gameplay — CLIENT (1 edge).** 1 inbound (Gameplay bodies `00312B40` call page-cited `FieldData_GetFormat0RecordVectorByIndex` (00320940)). Substantive edges include `FieldData_GetFormat0RecordVectorByIndex` (00320940) is called by `00312B40`.
- **Movement — CLIENT and SERVICE (8 edges).** 5 inbound (Movement bodies `BattleLocomotion_DecodeOrderGoal` (00312730), `00312DF0`, `BattleLocomotion_SolveClassMode2Step` (003394A0) call page-cited `FieldData_GetFormat0RecordVectorByIndex` (00320940), `00312DF0`, `0033DB60`); 3 outbound (page-cited `00312DF0`, `0033DB60`, `00354FB0` call Movement bodies `00317DE0`, `004687F0`, `00350510`). Substantive edges include `00312DF0` is called by `BattleLocomotion_DecodeOrderGoal` (00312730); `00312DF0` calls `00317DE0`; `FieldData_GetFormat0RecordVectorByIndex` (00320940) is called by `00312DF0`; `FieldData_GetFormat0RecordVectorByIndex` (00320940) is called by `BattleLocomotion_SolveClassMode2Step` (003394A0).
- **RNG_Random_Selection — SERVICE (3 edges).** 3 outbound (page-cited `SpawnPoint_GeneratePositionFromAuthoredRegion` (00236450), `00312B40`, `00312DF0` call RNG_Random_Selection bodies `RNG_SharedGameplayLCG_NextU32` (00328370)). Substantive edges include `SpawnPoint_GeneratePositionFromAuthoredRegion` (00236450) calls `RNG_SharedGameplayLCG_NextU32` (00328370); `00312B40` calls `RNG_SharedGameplayLCG_NextU32` (00328370); `00312DF0` calls `RNG_SharedGameplayLCG_NextU32` (00328370).
- **Spawn_Encounter_Lifecycle — CLIENT (6 edges).** 6 inbound (Spawn_Encounter_Lifecycle bodies `Spawn_TrySelectCandidatePosition` (00234AF0), `SpawnPoint_GeneratePositionFromAuthoredRegion` (00236450), `Spawn_PrepareRandomCandidateForCurrentEntry` (002355A0) call page-cited `00319390`, `003209C0`, `SpawnPoint_GeneratePositionFromAuthoredRegion` (00236450)). Substantive edges include `SpawnPoint_GeneratePositionFromAuthoredRegion` (00236450) is called by `Spawn_PrepareRandomCandidateForCurrentEntry` (002355A0); `00319390` is called by `Spawn_TrySelectCandidatePosition` (00234AF0); `00319390` is called by `SpawnPoint_GeneratePositionFromAuthoredRegion` (00236450); `FieldData_GetFormat0RecordVectorByIndex` (00320940) is called by `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0).
- **WorldAreaField — CLIENT and SERVICE (16 edges).** 5 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020), `WorldSimulation_ProcessDeferredModeRequest` (0032FC30), `003319D0` call page-cited `FieldData_CopyIndexedRecordByFormatClass` (003DFD00), `0017D280`, `003319D0`); 11 outbound (page-cited `003319D0`, `SpawnPoint_GeneratePositionFromAuthoredRegion` (00236450), `00312B40` call WorldAreaField bodies `FieldData_CopyIndexedRecordByFormatClass` (003DFD00), `FieldData_GetFormat0RecordVectorByIndex` (00320940), `003209C0`). Substantive edges include `SpawnPoint_GeneratePositionFromAuthoredRegion` (00236450) calls `003209C0`; `00312B40` calls `FieldData_GetFormat0RecordVectorByIndex` (00320940); `00312DF0` calls `FieldData_GetFormat0RecordVectorByIndex` (00320940); `FieldData_GetFormat0RecordVectorByIndex` (00320940) calls `FieldData_CopyIndexedRecordByFormatClass` (003DFD00); the remaining edges run through shared helpers the page cites.
## SWE2-EC7-42 update (2026-09-19) - `0050EBA0`

`0050EBA0` (297 B) is an EBP-section body - `00D22A30`/`00D22A3C`/`00D22A44`/`00D22A4C`, `00267E10` pair/`003DFD00`/`0017D280` sextuple. Interior anchor `0050EBBF` (a `00267E10` call).
