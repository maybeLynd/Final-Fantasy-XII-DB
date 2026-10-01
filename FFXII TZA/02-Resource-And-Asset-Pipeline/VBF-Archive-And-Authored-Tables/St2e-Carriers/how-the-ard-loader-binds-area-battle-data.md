---
system: The .ard loader — how an area's FF12AR03 file reaches the battle-data registry
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: CodeDomain — Resource (the reader) crossing into BattleData (the consumers)
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
corpus_validated: "166 / 166 area .ard files, 2026-09-04"
last_reviewed: 2026-09-04
archive_formats:
  - "ard"
# Claimed 2026-09-04 and NOT on the first draft. This sheet held the declaration back for a
# container sheet that turns out not to exist — no other .ard document is in the database, and
# leaving a censused, scored format at [ ] is worse than either owner holding it. If a dedicated
# layout sheet lands later, move this line there; one owner per format.
#
registry_slots:
  - "0x02EBF140"
  - "0x02EBF148"
  - "0x02EBF150"
#
# COORDINATOR CORRECTION, 2026-09-04, kept in full because it was right:
#   This sheet said "all five already have owners". They do not. The five declared slots in the
#   whole database are 0x02EBF0C0, 0x02EBF0F8, 0x02EBF138, 0x02EBF160 and 0x02EBF190 — NOT ONE of
#   the five in §4. registry_explained reads 5/63 and none of those five was mine.
#
# RESOLVED by repos-1e, 2026-09-04. Verified independently before acting: the gambit document
# declares 0x02EBF160, not 0x02EBF168. My error was reading MENTIONS as DECLARATIONS — 0x02EBF120
# and 0x02EBF150 are discussed in three other documents, and I took discussion for ownership. That
# is rule 3c's own warning ("mentioned in ten documents and explained in one") running backwards,
# and it is why the numerator is declared rather than scraped from prose.
#
# Declared: the four whose contents this sheet establishes — each holds a named .ard directory slot
# with a fixed record size, a cited binding site and a named consumer set. See §4.
#
# NOT declared: 0x02EBF168. Deliberate, and NOT the earlier mistake repeated. That slot's CONTENTS
# are explained in more depth elsewhere — 09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-
# a-command-switches-it.md reads the order sets as 32-bit offsets resolved against 0x01F83530 —
# while this sheet establishes only where the bytes come from. It is undeclared today, so it scores
# 0 either way; the declaration belongs on that sheet. **If it is not taken there, it should come
# here rather than stay unclaimed** — the same call I made for archive_formats: "ard".
audit:
  passes: 2
  last_pass: 2026-09-05
  last_pass_state: "GN160 (gzf fa0db293…d2f708, snapshot b57264ba…d18fea34, exe 73461d08…d89721f8) — independent pass by repos-4b: own .ard parser over 166 extracted areas + own capstone read-set of the 267-byte binder from functions.tsv bounds"
  last_pass_by: repos-4b
  crossref_clean: true
  crossref_checked: null
  crossref_report: null
  reopened_count: 0
---

# How the `.ard` loader binds area battle data

> **This is the reader half of `.ard`.** The [carrier README](README.md) establishes what the file
> *is* — `FF12AR03`, one per area, four `st2e` tables. This document establishes **what the engine
> does with it**: which function loads it, which six header fields it reads, which it never touches,
> and where the bytes end up. The answer to the last one is the authored-data registry that
> `BattleUnit_ApplyUnitDefinition` reads.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **166 of 166** area `.ard` files (332 on disk; every area ships twice, byte-identical) |
| magic `FF12AR03` | 166 / 166 |
| size range | 224 – 35,632 B |
| header fields the loader reads | **6** — `+0x10 +0x14 +0x18 +0x24 +0x28 +0x2C`, non-zero and in-range in **166 / 166** |
| header fields the loader never reads | **5** — `+0x00 +0x08 +0x0C +0x1C +0x20` |

---

## 1. What the player sees

**Which monsters live in this part of the world, how tough they are, and how they fight.**

Walk from the Estersand into the Giza Plains and the wildlife changes: different enemies, different
levels, different behaviour. That switch is this file. When the game crosses into a new **area** —
not a new map, an *area*, the outer folder that several maps share — it throws away the previous
area's battle definitions and loads one `.ard`.

The loader is blunt about it. **Everything is unbound first, then rebound**, and if the area has no
`.ard` the five battle-data slots are simply set to null and the game continues. There is no
fallback and no merge: an area's enemy definitions are all-or-nothing, which is why a third of areas
(85 of 251) that ship no `.ard` at all are areas where nothing needs stats — towns, title screens,
interiors.

One of the five things it binds is the **gambit order-set directory** — the authored AI that decides
which behaviour a monster runs. So `.ard` is not only *what* an enemy is, it is also *how it acts*.

## 2. The layout

The header the loader actually indexes. **Offsets are from the start of the file**, and the values
in the six read fields are *image addresses*, not plain offsets — §3 explains the difference.

```struct Ff12Ar03Header base=file size=0x30
+0x00  char[8]  magic      'FF12AR03' — 166/166, never read by the loader
+0x08  u32      _zero0     0 in 166/166 — never read
+0x0C  u32      trailerOff offset-shaped, 134 distinct values — read by 003EA650, not by the loader (CC-8, 2026-09-12)
+0x10  u32      slot0      always 0x30 in 166/166 — battle category 0
+0x14  u32      slot1      battle category 1, the gambit order-set directory
+0x18  u32      slot2      battle category 2
+0x1C  u32      slot3      0 in 166/166 — absent, and no reader
+0x20  u32      slot4      0 in 166/166 — absent, and no reader
+0x24  u32      slot5      battle category 3
+0x28  u32      slot6      battle category 4
+0x2C  u32      slot7      NOT a battle category — goes to FUN_003DCF00
```

**`+0x10 .. +0x2C` is an eight-slot offset directory indexed by slot number, `0 = absent` — the same
construction as the `EBP2` container.** That is `repos-d6`'s corpus finding, not this document's
(§5), and it supersedes the naming this sheet first used: I had numbered only the six fields the
loader reads as `sect0..sect5`, which **hides that slots 3 and 4 exist and are always empty**. Slot
numbers here are directory positions, and the census's names map as `const30`→`slot0`,
`varB`→`slot1`, `varC`→`slot2`, `varD`→`slot5`, `varE`→`slot6`, `varF`→`slot7`.

The directory ends at `0x30` and the first block begins at `0x30`, which is why `slot0` is always
`0x30`: it is simultaneously the first block's offset and the header's length.

`+0x0C` is a **trailer offset**, not a directory slot — it sits below the directory and, uniquely
among the offset-shaped fields, **nothing reads it** (§3).

## 3. The loader contract

### The path to the file — resource namespace 21

`.ard` is **not** opened by name. It is requested through the engine's generic
`(namespace, index)` resource address, the same mechanism that loads `.ebp`:

```
MapRef_GetAreaArdFieldResourceIndex  0x00264ED0   field id -> u16 area index
  → AreaArd_RefreshForMapRefField    0x003EA6E0   skip if already loaded and not forced
    → AreaArd_LoadOrUnloadFieldResource 0x003EA820  ← THE READER
        size = Resource_GetSize   (21, areaIndex*2)          0x003EA868
        buf  = FUN_0036c660(...)  tagged "..\\..\\katano\\atelareaload.c"
        Resource_BeginRead(21, areaIndex*2, buf, size, ctx)   0x003EA97F
        ctx.completion = AreaArd_BindLoadedRootAndBattleSections
    → AreaArd_BindLoadedRootAndBattleSections 0x003EA710  ← THE BINDER
```

**Namespace 21 is the `.ard` path table.** The engine holds a per-locale array of path tables at
`0x0215F000`, filled by `FUN_002DF9A0` (2,831 B, a `switch` on locale id), and the resolver is

```asm
002DF980  movsxd rax, ecx              ; namespace
002DF983  lea    r8, [rip + 0x1e7f676] ; -> 0x0215F000, the table-of-tables
002DF98A  movsxd rcx, edx              ; index
002DF98D  mov    rax, [r8 + rax*8]     ; table = pathTables[namespace]
002DF991  mov    rax, [rax + rcx*8]    ; return table[index]  (char*)
002DF995  ret
```

Namespace 21 is `0x0215F0A8`, i.e. `(0xA8 / 8) = 21` into that array — written at `002DFA9E` and
`002DFE66`, once per locale branch.

**The index is `areaIndex * 2`, and that is the whole explanation of the 16-byte record.** The path
table is a **flat `char*[]` at 8-byte stride**, and the pair a reader sees as
`{ardPath; fpkPath}` is simply indices `2i` and `2i+1`:

```struct ArdPathTablePair base=record size=0x10
+0x00  u64  ardPath   char* — requested as (namespace 21, index 2*areaIndex)
+0x08  u64  fpkPath   char* — index 2*areaIndex + 1; the .fpk never ships
```

`.ard` is fetched with `field_index * 2` (`003EA868`, `003EA97F`) and the sibling slot with
`field_index * 2 + 1` (`003EA83E`, via `FUN_0032eb40(0, 0x15, field_index*2+1)`). **So the "16-byte
record" and the "flat pointer array" are the same bytes described from two ends** — the file corpus
sees records, the engine sees a doubled index.

**The parity rule was challenged and then proved from the array itself.** A neighbouring session
could neither confirm nor deny it, because **both arrays installable at namespace 21 begin with 24
NULL qwords** — the head of the array holds no `.ard` at all, so any head-only inspection sees
nothing and a walk that stops at the first NULL measures the distance to a hole rather than a
length. Walking the arrays in full instead:

| | `0x01E0CFA0` (written `002DFE66`) | `0x01EDC280` (written `002DFA9E`) |
|---|---:|---:|
| first non-NULL index | **24** | **24** |
| `.ard` at **even** indices | **215** | **215** |
| `.fpk` at **odd** indices | **215** | **215** |
| `.ard` at an odd index | **0** | **0** |
| `.fpk` at an even index | **0** | **0** |

and **all 430 `.ard` path strings in the executable are reachable at even indices from those two
bases, with none unreachable.**

**Re-verified within a derived extent, after the same measurement went wrong on another namespace.**
The counts above were first taken with an arbitrary scan window, which is the *span-is-not-a-
structure* error in miniature — **where an array ends is not observable from the array.** Taking the
extent as the distance to the next base in address order, over all **83** path-table bases recovered
from `FUN_002DF9A0`'s stores, each namespace-21 array is **642 slots**, and inside that bound the
figures are unchanged: **215 `.ard` + 215 `.fpk` = 430 entries, first at index 24.** The window had
overrun here too; it simply happened that the neighbouring array carries no `.ard` or `.fpk`, so
nothing was miscounted. **The same window inflated a namespace-37 count by 65 % and invented a
"mixed table" that did not exist** — the numbers being right here was luck, and the extent rule is
what makes them checkable. Those are the only two writes to `0x0215F0A8` in the whole image —
established by decoding every RIP-relative operand in all 38,161 functions, not by pattern-matching
a `lea`/`mov` pair.

**One honest limit on that.** The arrays are **not** `{ard, fpk}` pairs end to end: they also carry
`bin`, `tm2`, `mrp`, `as7`, `ico`, `efx`, `cm`, `sys` and `mg` paths, and those appear at **both**
parities. The proven claim is the narrow one — *within these arrays every `.ard` is at an even index
and every `.fpk` at the odd index after it, 215/215 with zero crossover* — not that the whole array
is a table of pairs.

### The field table

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | — | — | — | **YES — never read** |
| `+0x08` `_zero0` | — | — | — | **YES — never read** |
| `+0x0C` `trailerOff` | `003EA650` | `0035A3A0` / `0035AC60` / `0037C3F0` | actor flag masks | **corrected 2026-09-12 (CC-8): read through the base table `02B5E0C0`, which the §7 searches did not follow** |
| `+0x10` `slot0` | `003EA73B` | — | — | — |
| `+0x14` `slot1` | `003EA743` | — | — | — |
| `+0x18` `slot2` | `003EA751` | — | — | — |
| `+0x1C` `slot3` | — | — | — | **never read — and never authored, see below** |
| `+0x20` `slot4` | — | — | — | **never read — and never authored, see below** |
| `+0x24` `slot5` | `003EA7AD`, `003EA7BA` | — | — | null → category 3 bound to 0 |
| `+0x28` `slot6` | `003EA7D6`, `003EA7E3` | — | — | null → category 4 bound to 0 |
| `+0x2C` `slot7` | `003EA789`, `003EA796` | — | — | null → `FUN_003dcf00(0)` |

> ### AUDIT 2026-09-05 — the read set and the authored data agree on which slots exist
>
> **The binder reads slots 0, 1, 2, 5, 6, 7 and skips 3 and 4. The corpus populates slots
> {0, 1, 2, 5, 6, 7} and leaves 3 and 4 zero — in 166 of 166 areas.** The same six-of-eight
> partition, from two instruments that share no method: one is the instruction stream, the other is
> the shipped files.
>
> **That is a corroboration the sheet was entitled to and did not state**, and it is stronger than
> either half. It also qualifies the `Inert` verdict on `+0x1C`/`+0x20`: **those two fields are never
> non-zero in any shipped file, so the corpus cannot test whether a reader exists** — the claim rests
> entirely on the instruction stream, and a modder who writes a value there is in territory no
> shipped data covers. *(`repos-4b`, audit pass 1; slot occupancy re-derived from the 166 extracted
> `.ard` files, agreeing with `repos-d6`'s directory census.)*

**The `FF12AR03` magic is never validated.** The binder's read set, taken from the instruction
stream, contains no reference to `[rbp+0]`. This is the *third* container in this database to come
out that way — after `EBP2` and the EBP section markers — and here there is a mechanical reason
rather than an accident: **the engine never searches for `.ard` files.** It holds 430 literal paths
and asks for one by index. A magic check would be guarding against a substitution the design makes
impossible.

**Nothing is clamped and nothing is bounds-checked.** Each of the six fields is resolved and added to
the file base with no comparison against the file's length:

```asm
003EA73B  mov  ecx, dword ptr [rbp + 0x10]   ; rbp = the loaded .ard base
003EA73E  call 0x20e600                      ; ImageAddress_ResolveRuntimePointer
003EA749  add  rsi, rbp                      ; pointer = base + resolved
003EA765  xor  ecx, ecx                      ; category 0
003EA76A  call 0x23a160                      ; BattleData_SetAreaArdSectionCategory
```

`ImageAddress_ResolveRuntimePointer` (`0x0020E600`, 10 B) is **not** a bounds check — it is the shared
image-address decoder the ScriptVM interpreter also uses. An out-of-range `sect` field yields an
out-of-range pointer that is stored and later dereferenced.

> **AUDIT 2026-09-05 — the comment `pointer = base + resolved` hides a second base.** The whole
> resolver is `mov eax, ecx` / `add rax, qword ptr [rip + 0x1d74f27]` / `ret`, and that displacement
> resolves to **`0x01F83530`** — a global, **not** the `.ard` base. So the arithmetic is
> `pointer = ardBase + (sect + [0x01F83530])`: **two bases, not one.**
>
> **`0x01F83530` is above the file-backed end of `.data` (`0x01F7E400`), so it is BSS — zero in the
> image and written at run time.** A reader reconstructing the address arithmetic from the asm
> excerpt alone would treat `sect` as a plain file-relative offset and be wrong. The sheet's actual
> claim — that this is a decoder and not a bounds check — is **correct and survives**; what is added
> here is which bases are involved. *(`repos-4b`, audit pass 1.)*

**The only rejection in the whole path is the file size.** `AreaArd_LoadOrUnloadFieldResource` calls
`Resource_GetSize(21, areaIndex*2)` and branches on `< 1`:

- **size ≥ 1** → unbind everything, allocate, read, bind on completion.
- **size < 1** → unbind everything and stop. `g_pLoadedAreaArdRoot = 0`,
  `g_nLoadedAreaArdFieldIndex = -1`, and all five categories are set to `0`.

**Both branches unbind first.** The five `BattleData_SetAreaArdSectionCategory(n, 0)` calls appear
in the load path *as well as* the unload path, so a new area never inherits the previous area's
battle data even transiently. That is the loader's one real safety property, and it is structural
rather than validated.

### What loading normalises

`AreaData_BindAndRebaseSectionDescriptor` (`0x003845F0`, 252 B) **rewrites the file image in place.**
It stores the section base into the destination global (`003845F4`), then adds that base to four of
the descriptor's internal image addresses, each guarded by its own non-zero test:

| descriptor field | read at | test | written back at |
|---|---|---|---|
| `+0x0C` | `00384600` | `00384608` | `0038460E` |
| `+0x10` | `00384614` | `00384618` | `0038461E` |
| `+0x18` | `00384625` | `00384629` | `0038462F` |
| `+0x1C` | `00384636` | `0038463A` | `00384640` |

and `+0x14` (read `00384647`, tested `0038464A`) is additionally re-encoded through
`RuntimePointer_EncodeImageAddress` (`0x0020E620`, 9 B) rather than simply added.

**So the loaded buffer is not the file.** Anyone diffing runtime memory against the on-disk `.ard`
will find the descriptors' pointer fields changed, and that is the loader's doing, not corruption.

### The write path

**There is none.** No code constructs an `FF12AR03` header. The allocation is tagged with the
original C source filename `"..\\..\\katano\\atelareaload.c"` — the same `katano` source directory
that names the ATEL loader for the EBP camera sections — which is build provenance, not a writer.

## 4. Where the bytes end up — five authored-data registry slots

`BattleData_SetAreaArdSectionCategory` (`0x0023A160`) is a five-way branch that hands each section
to a different registry global. **The mapping below is taken from the branch structure, not from the
decompiler's variable names** — the `sub ecx, 1` chain at `0023A160`–`0023A176` orders the cases
differently from the way Ghidra prints them, and reading the printed order gives the wrong answer.

| category | header field | binder site | registry slot | bound via |
|---:|---|---|---|---|
| 0 | `+0x10` `slot0` | `003EA76A` | **`0x02EBF150`** | `AreaData_BindAndRebaseSectionDescriptor` |
| 1 | `+0x14` `slot1` | `003EA777` | **`0x02EBF168`** | `FUN_003846F0` — *a different binder* |
| 2 | `+0x18` `slot2` | `003EA784` | **`0x02EBF120`** | `AreaData_BindAndRebaseSectionDescriptor` |
| 3 | `+0x24` `slot5` | `003EA7D1` | **`0x02EBF148`** | `AreaData_BindAndRebaseSectionDescriptor` |
| 4 | `+0x28` `slot6` | `003EA7FA` | **`0x02EBF140`** | `AreaData_BindAndRebaseSectionDescriptor` |
| — | `+0x2C` `slot7` | `003EA7A8` | *none* | `FUN_003DCF00` |

The `lea` sites are `0023A1B7` (cat 0), `0023A1A8` (cat 1), `0023A196` (cat 2), `0023A187` (cat 3)
and `0023A178` (cat 4).

**All five are inside the 63-slot authored-data registry `0x02EBF008`–`0x02EBF1F8`**, and their
readers are named:

| slot | read by |
|---|---|
| `0x02EBF120` | `BattleUnit_ApplyUnitDefinition` `0023A570`, `BattleStats_InitializeDefinitionRecord` `0023AC80`, `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`, `BattleEncodedId_IsValidForClass` `00322C50` |
| `0x02EBF140` | `BattleUnit_ApplyUnitDefinition` `0023A570`, `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` |
| `0x02EBF148` | `BattleUnit_ApplyUnitDefinition` `0023A570`, `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` |
| `0x02EBF150` | `BattleUnit_ApplyUnitDefinition` `0023A570`, `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`, `BattleEncodedId_IsValidForClass` `00322C50` |
| `0x02EBF168` | `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` `00239040`, `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0`, `BattleUnit_ApplyUnitDefinition` `0023A570` |

### What this sheet declares, and the one it does not

Four of the five are declared in this document's `registry_slots`. **What each declaration claims is
narrow and checkable:**

> *slot `X` holds the `.ard` section at directory slot `N`, records of a fixed width, bound at a
> cited instruction, read by a named set of functions.*

| registry slot | holds | record width | bound at | declared here |
|---|---|---:|---|---|
| `0x02EBF150` | `.ard` directory slot 0 | 84 | `003EA76A` | **yes** — *observed bound in a loaded field ([EXP-081](../../../_experiments/EXP-081-live-battleunit-bindings.md)): 12 rows at stride `0x54`, the rows three spawned units' `+0xE68` point at; null in the registry before the field initialised* |
| `0x02EBF120` | `.ard` directory slot 2 | 88 | `003EA784` | **yes** |
| `0x02EBF148` | `.ard` directory slot 5 | 56 | `003EA7D1` | **yes** |
| `0x02EBF140` | `.ard` directory slot 6 | 56 | `003EA7FA` | **yes** |
| `0x02EBF168` | `.ard` directory slot 1 — the AI order-set directory | *(not `st2e`)* | `003EA777` | **no — see below** |

It does **not** claim which of the four is "status" and which is "attributes". That distinction is
still undecoded and §7 says so; a declaration of *what the slot holds* is not a claim to have read
its records.

**`0x02EBF168` is deliberately left undeclared.** Its *contents* are explained in more depth by
[the gambit-set document](../../../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md),
which reads the order sets as 32-bit offsets resolved against `0x01F83530`. This sheet establishes
only where those bytes come from, so declaring it here would put the ownership on the weaker
document. **It is undeclared today and therefore scores nothing either way — if that sheet does not
take it, it should come here rather than stay unclaimed.**

### 7a. Slot 1 read whole — the order-set directory's format (CC-5, 2026-09-12, FABLE)

The "count-shaped" opening is a directory, and the binder that takes this slot instead of the
`st2e` one (`FUN_003846F0`, 177 B) is its reader: `slot = resolve(desc)` (`00384704`–`00384709`),
then `count = u16 [desc + 0]` (`00384727`), and for entries `0 … count` (the loop runs `count + 1`
times, `0038478B`–`0038478E`) each `u32` at `desc + 4 + 4i` is **rebased by the section's address**
— the first `count` through a recursive call with the depth argument decremented (`0038475B`–
`0038476B`), the last in place (`00384780`). Over the 166 shipped files (the `in` copies, byte-equal
to `ch`):

```
.ard directory slot 1  (offset +0x14)                      166 / 166 present
  +0x00  u16   count            0 .. 24 order sets per area (four areas have none)
  +0x02  u16   100              the constant 0x64 in every file
  +0x04  u32   offset[count+1]  section-relative; offset[count] bounds the last set
order set  (at slot1 + offset[i])
  +0x00  u8[12]  records per subgroup  (the gambit-set page's count bytes; 1 .. 12 subgroups used)
  +0x0C  u8[20]  zero in all 1,422 sets
  +0x20  record[sum]  24-byte order records, subgroup 0 first
order record (24 B, the gambit-set page §4 layout)
  +0x00 u16 weighted action selector   +0x02 s16   +0x04 u16 flags
  +0x06 / +0x0C / +0x12  three selector entries {u16 operand, u16, u16}; an operand of 0 = empty
```

> **CB-1 answered 2026-09-12 (FABLE): every order set is referenced — a unit row names four of
> them, not one.** Both runtime readers of the slot-1 registry index the authored unit row at
> **`+0x50 + 2·k`, k = 0 … 3**: `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` (`00239073`,
> `movzx ecx, word [rdx + rdi*2 + 0x50]` after `cmp edi, 3`), reached only from the script verb
> **`btlAtelSetDefaultLogic`** (`0x3060` → `VM_BattleUnit_SelectAiOrderSetVariant` `00510580`), and
> `BattleUnit_ExecuteDirectStateCommandOrder` (`002FE05B`, the same word for direct state commands
> `0x4112`–`0x4115`, bounds-checked against the directory's `u16` count at `002FE06C`–`002FE077`);
> the binder's own bind at `0023A92F` takes variant 0. Over the 166 areas / 1,146 unit rows /
> 1,422 sets, coverage by `+0x50` alone reproduces at **0.720** (the inbox note's 0.688 counted the
> same population with a slightly different denominator), coverage by **all four words is 1.000
> with 0 out-of-range values** — no set in any area is unreferenced. Rows carry 2 distinct set
> indices in 927 cases, 3 in 178 and 4 in 41, so the "unreferenced third" is the alternate logic
> variants scripts and direct commands switch a unit to. The five ways slot 1 differs from the
> `st2e` slots stand; this one was never one of them.

**1,422 sets, 50,050 records, none malformed** — every set's records fit inside its offset bounds
and every header tail is zero, which is the corpus proof of the layout the code implies. The
operands and what they say about relation modes are on
[the gambit page](../../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) §8i (Z-15).
~~Slot 7 and the `+0x0C` trailer remain CC-5's residue.~~ *(Corrected (FABLE, Claude Opus 5.5, 2026-09-26, on OPUS-REQ-FABLE-ARD-TRAILER-READ-BY-NOTHING-PROSE): both are answered. Slot 7 is the
area's class-keyed motion index (`CC-10`). The trailer is `{u32 count; {u32 key; u32 mask}[count]}`, read through
the root accessor by the per-name flag-mask walkers (OPUS; the `CC-5` row of [the register](../../../_index/OPEN-QUESTIONS.md)).)*

*(Record widths are `repos-d6`'s corpus measurement, cited not re-derived; the `.ard`→registry
mapping and the binding sites are this document's.)*

### This is what promotes the community reading — and only this far

The modding community describes `.ard` as **per-area enemy status and attributes**. The
[carrier README](README.md) correctly held that at **tier 9 — authored intent, never ownership —
until a reader is named in the binary.**

**A reader is now named.** The path is unbroken and every step is an instruction in this document:
the file loads at `003EA97F`, binds at `003EA710`, reaches the registry at `0023A160`, and
`BattleUnit_ApplyUnitDefinition` (`0x0023A570`) and `BattleStats_RebuildEffectiveStatsAndAffinityState`
(`0x002FEF30`) read those slots. **`.ard` supplies per-area battle unit definitions and the gambit order-set directory.**

**What that does not license.** It says *where the tables go* and *who reads them*. It does **not**
say the tables are laid out the way any community tool claims, and it does **not** identify which of
the five is "status" versus "attributes" — the slot-level meanings belong to the documents that own
those slots, listed in §8. Naming the consumer is a much weaker claim than decoding the records, and
this document makes only the weaker one.

## 5. Corpus survey — 166 of 166 areas

| field | zero | in range | past EOF | distinct |
|---|---:|---:|---:|---:|
| `+0x08` `_zero0` | **166** | 0 | 0 | 1 |
| `+0x0C` `trailerOff` | 26 | 140 | 0 | **134** |
| `+0x10` `slot0` | 0 | 166 | 0 | **1 (always 0x30)** |
| `+0x14` `slot1` | 0 | 166 | 0 | 16 |
| `+0x18` `slot2` | 0 | 166 | 0 | 149 |
| `+0x1C` `slot3` | **166** | 0 | 0 | 1 |
| `+0x20` `slot4` | **166** | 0 | 0 | 1 |
| `+0x24` `slot5` | 0 | 166 | 0 | 150 |
| `+0x28` `slot6` | 0 | 166 | 0 | 150 |
| `+0x2C` `slot7` | 0 | 166 | 0 | 151 |

**Two findings, and the second is the interesting one.**

**The null guards never fire.** `slot5`, `slot6` and `slot7` are null-guarded in the binder and are
**non-zero in all 166 files**. The guards are real code and dead against shipped data — the same
shape as the EBP container's `slotCount` bound, which is enforced and never triggered because every
file declares `0x14`. Both become live the moment someone edits a file, and a modder who zeroes
`slot5` gets category 3 bound to null rather than a crash.

**`trailerOff` at `+0x0C` is authored, varies, ~~and is read by nothing.~~** *(corrected (FABLE, Claude Opus 5.5, 2026-09-26, on OPUS-REQ-FABLE-ARD-TRAILER-READ-BY-NOTHING-PROSE): it is read,
not by the loader but through the root accessor; the `CC-5` row of [the register](../../../_index/OPEN-QUESTIONS.md))* 134 distinct values, in-file range
in 140 of 166, zero in the other 26.

> **CC-6 answered 2026-09-12 (FABLE) — what the offset points at, and why it is zero where it is.**
> In all 140 non-zero files `trailerOff` addresses **the last block of the file**: a `u32 count`
> followed by `count` eight-byte records `{u16 id, u16 kind, u32 param}`, padded to a 16-byte
> multiple (`size − trailerOff` is 32, 48, 64, 80, 96, 112, 128, 144 or 176; counts 2–13; 998 records
> in all). The **26 zero files are exactly the files whose tail after the slot-7 table is 32 zero
> bytes — an empty list**: the four 224-byte stubs (`asp_a`, `dor_f`, `mrm_a`, `slm_a`), `naf_a`,
> `pbc_c` and the twenty `tri_a`–`tri_t` areas. So `0` is "no trailer records", not a different
> layout, and the "why" is authoring: those areas were shipped without the list. **What the records
> are is not established** — `kind` takes only the values `0x63`, `0x6D`, `0x6E`, `0x73`, `0x77`
> (3 / 278 / 140 / 13 / 564 records; every one a lowercase ASCII letter, which *reads as* a
> type tag but is not proved to be one), `param` is `2` for every `0x6D`, `0` for every `0x77` and a
> small bit-set for `0x6E`, and `id` runs 1–326 (247 distinct) and does **not** coincide with the
> area's spawn-row name words (0 of 998) or class words beyond chance (15 of 998). ~~Since nothing in~~
> ~~the shipped engine reads `+0x0C`, nothing depends on the answer; a reconstruction preserves the~~
> ~~block as bytes.~~ *(Corrected (FABLE, Claude Opus 5.5, 2026-09-26, on OPUS-REQ-FABLE-ARD-TRAILER-READ-BY-NOTHING-PROSE): the trailer is read. The same eight bytes are a `u32` key,
> a definition key with a lowercase letter in its high word, and a `u32` mask applied per name while the area's root
> is live; the `CC-5` row of [the register](../../../_index/OPEN-QUESTIONS.md). A reconstruction must implement the walk, not only preserve the bytes.)*
> **Slots 3 and 4** are the other half of the question and were already settled
> above: never read by the loader, zero in 166 of 166 — the same sparse-index fact as the EBP
> container's unused slots, stated here once. A field nobody reads that is nevertheless *different in 134
areas* is not padding — **it is authored data the shipped engine ignores.** That is the same shape as
EBP `section_017`: a live handler with zero users — capacity present in the data or the code that
this build does not exercise.

*(An earlier draft listed `.fpk`'s 7,520 unshipped paths here as a third example. **It is not one** —
§7 shows those names are a consequence of record width, not authored intent. Removed rather than
left standing, because a list of instances is a claim about how common a pattern is.)*

### The binary expects 215 areas and 166 ship

Extracting the area stem from every `.ard` path string in the executable and comparing against the
shipped corpus:

| | |
|---|---:|
| `.ard` paths hardcoded, `ch` tree | **215** |
| `.ard` paths hardcoded, `in` tree | **215** |
| the two trees name the **same** stem set | **yes** |
| area stems that ship an `.ard` file | **166** |
| **named in the binary but never shipped** | **49** |
| **shipped but not named in the binary** | **0** |

**The containment runs one way, and that is the finding.** Every file that ships is reachable; 49
paths reach nothing. Among them are whole families — `alc_a`…`alc_f` and `alc_z`, `byu_a`…`byu_z`,
`dor_a`/`dor_z`, `glf_a`/`glf_z` — which is what a cut or merged region looks like, not scattered
typos.

This is a **second** instance of the same shape in one format: 49 dead `.ard` paths and
~~`trailerOff` read by nothing.~~ *(corrected (FABLE, Claude Opus 5.5, 2026-09-26, on OPUS-REQ-FABLE-ARD-TRAILER-READ-BY-NOTHING-PROSE): the trailer is read, so it is not a second
instance)* **`.fpk` is deliberately not counted as a third** — §7 shows its
7,520 unshipped names fall out of record width, so it is not unused authored capacity at all.
It also sharpens the carrier README's
open question. *"Only 166 of 251 areas have an `.ard`"* compares against the `plan_map` folder
count; the sharper comparison is against **what the engine asks for**, and by that measure the
shortfall is 49, not 85.

**It does not explain the `ch`/`in` duplication.** Both trees name the identical 215 stems and the
shipped copies are byte-identical, so the redundancy is packaging; *why those two trees* remains
open.

### Six fields, five slots, four `st2e` tables — the three counts reconcile

This document's first draft flagged those as three numbers it could not map onto each other.
**`repos-d6`'s independent corpus pass supplies the missing column**, and the two readings — one from
the instruction stream, one from the 166 files — partition the directory the same way:

| slot | offset | holds `st2e`? *(corpus)* | `recordSize` *(corpus)* | destination *(this document)* |
|---:|---|---|---|---|
| 0 | `+0x10` | **yes, 166/166** | **84** | category 0 → `0x02EBF150` |
| 1 | `+0x14` | **no, 0/166** | — | category 1 → `0x02EBF168`, **via a different binder** |
| 2 | `+0x18` | **yes, 166/166** | **88** | category 2 → `0x02EBF120` |
| 3 | `+0x1C` | always absent | — | never read |
| 4 | `+0x20` | always absent | — | never read |
| 5 | `+0x24` | **yes, 166/166** | **56** | category 3 → `0x02EBF148` |
| 6 | `+0x28` | **yes, 166/166** | **56** | category 4 → `0x02EBF140` |
| 7 | `+0x2C` | **no, 0/166** | — | `FUN_003DCF00`, **no registry slot** |

**The two slots that are not `st2e` are exactly the two the loader treats differently**, and neither
reading was told the other's answer. Slot 1 is the one bound by `FUN_003846F0` instead of
`AreaData_BindAndRebaseSectionDescriptor`; slot 7 is the one that reaches no registry slot at all.
A corpus pass counting `st2e` magic and an instruction pass following call targets have **no shared
failure mode**, so their agreeing on the same 4 / 2 / 2 partition is real corroboration rather than
two views of one assumption.

So the reconciliation is: **8 directory slots, 6 present, 4 of those carry `st2e`, 5 reach the
registry.** No number was wrong; they count different things, and now every slot is accounted for.

*`recordSize` and the `st2e` column are `repos-d6`'s measurements, not this document's — cited, not
re-derived.*

## 6. Falsification pass — 2026-09-04, and independent audit — 2026-09-05

> **Independent audit, `repos-4b`, 2026-09-05 — nothing broke.** Both halves of this sheet were
> re-derived with separate implementations: an own `.ard` parser over the 166 extracted areas, and
> an own capstone read-set of the binder taken from `functions.tsv` bounds. **Corpus:** magic
> `FF12AR03` **166/166**, `+0x08` zero **166/166**, `+0x0C` **134 distinct — the sheet's own
> figure**, `slot0` always `0x30`, `slot3` and `slot4` zero in **166/166**. **Binary:** the 267-byte
> binder contains **exactly six** `[rbp + disp]` references — `0x10`, `0x14`, `0x18`, `0x24`,
> `0x28`, `0x2C` — first seen at `0x003EA73B`, `0x003EA743`, `0x003EA751`, `0x003EA7AD`,
> `0x003EA7D6`, `0x003EA789`, **every one matching the address this sheet cites for it**. Of the
> five offsets claimed never read — `+0x00`, `+0x08`, `+0x0C`, `+0x1C`, `+0x20` — **none is
> referenced anywhere in the body.**
>
> **What I attacked and failed to break.** (1) That the read set proves the magic unvalidated: a
> per-function read set says nothing about *other* functions — the `.sab` case is exactly that trap.
> But the sheet does not rest on the read set alone; the whole-image scan for `FF12AR03` and its
> tail `AR03` returning zero was **re-run here and reproduces**, which is the strong form of the
> negative and closes the `.rdata`-constant route. (2) That `+0x0C`'s "134 distinct" might be an
> artefact of a partial corpus — it is 134 over all 166. (3) That slots 3 and 4 might be non-zero in
> the copies this sheet did not open — both are zero in every one of the 166.

| attack | result |
|---|---|
| Is the magic checked somewhere the path-string search could not see? | **The question was answered by reading, not searching.** Every `[rbp+N]` reference in the binder was enumerated from the instruction stream; `[rbp+0]` does not appear. The reader (`003EA820`) never touches the buffer's first bytes either — it only sizes, allocates and reads. |
| **Could `FF12AR03` be compared against a constant held in `.rdata`, so no immediate ever appears in code?** | **No — and the pattern is real, not hypothetical.** Another session found `.sab`'s magic validated on every load as `cmp eax, [rip+0x541614]` against a four-byte tag at `0x00D115B4`, which a `.text` scan for `sabf` cannot see. Applying that method here: **`FF12AR03` occurs 0 times in the whole image, and so does the tail `AR03`** — every section, so there is no constant to compare against and a split two-halves comparison is excluded by the tail alone. (`FF12` alone occurs 8,385 times in `.rdata`, all inside longer strings; the tail is the discriminating half.) **Positive control: the same scan finds `sabf` exactly once, in `.rdata`.** |
| Did Ghidra's xref engine miss the consumer, and did the sheet then claim a false negative? | **This is exactly what happened first, and it is why the method changed.** `DumpDataXrefs` on the table base returned `DUMP_DATA_XREFS_NONE` for all seven probed addresses — **zero references** — and a naive linear disassembly of `.text` agreed. Both were wrong: the table is reached as `pathTables[ns][index]`, so nothing references a record directly. Re-running the scan **per function, using `functions.tsv` boundaries** (1,787,590 instructions decoded) found the reference. **A linear sweep desynchronises after the first function and silently reports zero.** |
| Is the mapping of category → registry slot taken from decompiler names? | **No — from the `sub ecx, 1` branch chain at `0023A160`–`0023A176`.** The printed order of the decompiled `if` blocks does not match the branch order, and following it gives a different and wrong mapping. Each `lea` address is cited in §4. |
| Is `trailerOff` (`+0x0C`) really unread, or does another function read `+0x0C` of this same header? | The EBP `section_019` binder (`FUN_003EAA00`) carries the **same header** and reads **only `+0x2C`** (`003EAA32`, `003EAA3F`) — so it does not read `+0x0C` either. The claim is nonetheless scoped as *"no reader found by"* the named search in §7, not as "unused". |
| Is the doubled index real or an artefact of a struct guess? | **Real, and it is the instruction.** `Resource_GetSize` and `Resource_BeginRead` are both called with `field_index * 2` (`003EA868`, `003EA97F`), and the sibling with `*2 + 1` (`003EA83E`). The 16-byte record is the corpus view of the same bytes. |
| **A second session could not reproduce "namespace 21 is `.ard`" and asked for it to be settled.** | **Settled, and their inability was itself informative.** Both arrays installable at `0x0215F0A8` begin with **24 NULL qwords**, so a head-only view or a walk that stops at the first NULL sees no `.ard` — the array is sparse and its head is empty. Walking both in full gives 215 `.ard` at even indices and 215 `.fpk` at odd, **zero crossover in either array**, and **all 430 `.ard` strings reachable, none unreachable**. Their narrower surviving claim — *no slot's head holds `.ard` paths* — is true and compatible. |
| Could a write to `0x0215F0A8` have been missed, installing some other array? | **No.** Every RIP-relative operand in all 38,161 functions was decoded; `0x0215F0A8` is touched exactly **twice**, both `mov` writes in `FUN_002DF9A0` (`002DFA9E` ← `0x01EDC280`, `002DFE66` ← `0x01E0CFA0`). This does not pair a `lea` with a `mov`, so a value arriving in a register by any other route would still have been seen. |
| **Is the array base right, or is it just where the first pointer happens to be?** | **The base comes from the initialiser's own store, not from the data.** This matters more than it looks: these arrays are sparse, so *the base and the first non-NULL entry are 24 qwords apart*. Taking the first `.ard` pointer as the base would shift every array POSITION by 12 areas — and **every downstream number would stay self-consistent**, so no gate would flag it. **The inverse case exists and was tested by another session:** resource kind 26's arrays, recovered the same way from `002DFAE4` → `0x01E4DC30` and `002DFE58` → `0x01EAE0D0`, are **dense from index 0** with the first entry already a path and the first NULL at 321. Sparse and dense are indistinguishable from the data alone; only the initialiser separates them. |
| Is the slot ordering in §5 stable, or could an area permute its tables? | **Measured, not assumed.** A third session mapped every `st2e` occurrence onto the directory slot whose offset equals it and found the ordinal→slot map **never permutes, 166/166**. Had one area permuted, a claim stated in file order would be wrong there and no gate would catch it. |
| Could the `.ard` and `section_019` header be different formats that merely share a magic? | They share more than the magic: **both are indexed by the same field**, and `section_019`'s binder reads `+0x2C` and hands it to `FUN_003DCF10`, the sibling of the `FUN_003DCF00` that `.ard`'s `+0x2C` goes to. That is a mechanism match, not a name match. |
| Does naming a reader prove the community's "enemy status and attributes"? | **It proves the destination, not the decoding.** §4 states the weaker claim deliberately. |

~~**Not attacked:** whether `FUN_002DF9A0`'s locale branches ever select a table that is *not* the
`ch`/`in` pair — the switch has at least six cases and only two were traced.~~ **CC-9 answered
2026-09-12 (FABLE), the switch mapped mechanically.** The jump table (`002DFBBE`, eleven dwords at
`002E04B0`) sends locale ids 1–8 and 11 to nine bodies, ids 9 and 10 and every out-of-range id to a
tenth (`002DFF32`). The prologue every locale runs installs **35** pointers, among them the `.ard`
slot `0215F0A8 ← 01EDC280` (`002DFA9E`) — the array whose 430 non-null entries of 642 are the
**`in`** tree (`PS2Data\plan_master\in\plan_map\<area>\area\<area>.ard` / `.fpk`, `ttl_a` …
`tri_t`). The bodies re-install between four and nine pointers each — the per-locale text and menu
tables at `0215F008`, `0215F010`, `0215F028`, `0215F040`, `0215F048`, `0215F060` (`0215F038` for the
9 / 10 / default body) — and **exactly one body touches the `.ard` slot: locale 7** (`002DFDF6`),
which replaces it with `01E0CFA0` (`002DFE66`), the same 430-of-642 layout over the **`ch`** tree,
and also re-points `0215F0D0` and `0215F128`. So there are exactly two `.ard` trees because the
loader has exactly two `.ard` arrays: `in` for every locale but one, `ch` for locale 7.

### Audit pass — 2026-09-05, `repos-4b` (independent; not the author)

| attack | result |
|---|---|
| Is the field table's read-set complete, or does the binder touch a field the table omits? | **Complete.** Own capstone read of all 267 bytes of `0x003EA710`, bounds from `functions.tsv`. The `[rbp+disp]` set is **exactly** `{+0x10, +0x14, +0x18, +0x24, +0x28, +0x2C}` — six fields, with `+0x24`/`+0x28`/`+0x2C` each read twice. **No reference to `+0x00`, `+0x08`, `+0x0C`, `+0x1C` or `+0x20`.** The `Inert` rows and the magic claim both survive. |
| Is the five-way branch mapping right, given the sheet's own warning that the decompiler prints it out of order? | **Right, re-derived from the `lea` displacements rather than from the decompiler.** case 0 → `0x02EBF150`, case 1 → `0x02EBF168`, case 2 → `0x02EBF120`, case 3 → `0x02EBF148`, case 4 → `0x02EBF140`. **Case 1 alone tail-jumps to `0x003846F0`, not `0x003845F0`** — which is exactly why this sheet declares four slots and leaves `0x02EBF168` to the gambit document. The declaration boundary is correct. |
| Does the field→category→registry chain hold end to end? | **Yes, traced instruction by instruction.** `+0x10`→cat 0→`0x02EBF150`; `+0x14`→cat 1→`0x02EBF168`; `+0x18`→cat 2→`0x02EBF120`; `+0x24`→cat 3→`0x02EBF148`; `+0x28`→cat 4→`0x02EBF140`; `+0x2C`→`FUN_003DCF00(0)` and no registry. |
| Does the chain agree with the independent `.nmb` join? | **Yes, and this is the useful cross-check.** [`area-nmb-index`](area-nmb-index.md) establishes from the corpus that the `.nmb` entry count equals the record count of the `st2e` table in **directory slot 2**, 166/166. Slot 2 is `+0x18`, which this binder hands to **category 2 → `0x02EBF120`**. **A corpus join and an instruction trace, sharing no method, land on the same table.** |
| Is `ImageAddress_ResolveRuntimePointer` really not a bounds check? | **Confirmed — 10 bytes, `mov eax,ecx` / `add rax,[rip+0x1d74f27]` / `ret`.** No comparison exists. **But it adds a second base**, `0x01F83530`, which is BSS — see §3. |

**Not broken by this pass:** every claim above stood. **What was added** is the read-set as a
complete set rather than a per-row citation, the slot-occupancy corroboration in §3, and the second
base in the resolver.

## 7. What this document does not claim

> **CC-8 answered 2026-09-12 (FABLE): `trailerOff` has a reader, and the trailer is the area's actor
> flag-mask table.** The loader keeps the `.ard` base: `AreaArd_BindLoadedRootAndBattleSections`
> stores it at `003EA809` into a two-entry base table at **`02B5E0C0`** (`AreaArd_LoadOrUnloadField
> Resource` nulls it at `003EA88F` / `003EA999`). `003EA650(idx)` reads `[02B5E0C0 + idx·8]`, then
> **`[base + 0x0C]`** twice (`003EA671`, `003EA67E`), resolves it through `ImageAddress_Resolve
> RuntimePointer` and returns `base + trailerOff` — a double indirection no displacement census on
> the header could see, which is why three searches found nothing. Its callers (raw `E8`/`E9`
> index): **`0035A3A0`** and **`0035AC60`**, a matched pair that walk both bases (`r12` 0..1) over a
> counted list of 8-byte `{selector, mask}` records at the trailer (`+0` count, `+4`…): the selector
> (0–13) is mapped by `002EB7A0` to an encoded actor kind / id (`0x630000`, `0x6E0001`, …), the actor
> is resolved by `002E99C0`, and for every set bit of the 32-bit mask `002ECAB0(selector, bit, on)`
> is applied — `0035A3A0` sets actor `+0x19` bit 0 and passes `on = 1`, `0035AC60` clears the bit and
> passes `on = 0`. Both actor-resource hooks call the setter on their load arm (`0025AFC0`:
> `0035A270` / `0035A490` / `0035A3A0` at `0025AFF6`; `002628B0` at `00262D5E`) and the clearer on
> their unload arm (`0025B021`, `00262D83`), under `ActorResource_OnDefinitionPayloadLoaded` and
> `ActorResource_BeginManagerResour…`. The third caller, `0037C3F0` (a callback with no direct
> caller), reads the trailer ~~for the index in the byte `02ADD955`~~ inside an eleven-state machine.
> *Corrected 2026-09-21 (FABLE): `02ADD955` is the machine's **pass counter**, not a trailer index. It
> calls `003EA650` only on passes 0 and 1 — which is all that accessor accepts — and on pass 2 reads a
> table out of manager slot 0's bound payload instead. Whether pass 2 runs at all is decided by the
> scheduling argument. The eleven states are read out on*
> [the area-music page](../../../18-Audio/how-the-music-changes-when-you-change-area.md) *under `UQ-264`.*
> So `varA` names an authored per-area table of actor flag masks applied on area load and removed
> on unload — not a cut feature; what each mask bit switches in `002ECAB0`'s `0x120`-stride records
> at `02161DA0` is the residue.
>
> *Narrowed 2026-09-18 (SWE2-STRUCT-NBE-SUBTABLE-RECORD): the records are now a store type,
> **`NameBindingSubRecord`** (0x120 × 32 at `02161DA0`). `002ECAB0`'s mask bits land in
> `liveMaskByName` (`+0x38`), gated on the `+0x24|+0x28|+0x34` permitted union; the sibling
> `liveMaskByEntry` (`+0x40`) is written by `002ECA30`. What each *individual* bit switches
> remains open — the record's bit lanes feed `valueIds[32]`/`bitRefcounts[32]` and the
> `CharacterRenderRecord` `+0x42C/+0x430` stores, not a named per-bit semantics.*


- **It carries `archive_formats: "ard"` but it is still not a full container sheet.** The
  declaration was held back for a layout sheet that does not exist; no other `.ard` document is in
  the database, so leaving a censused, scored format unclaimed was the worse of the two errors.
  **What is still missing is the record level:** the four `st2e` tables' fields and what a row
  means. This sheet establishes the header, the directory and the loader, not the records.
- **Four `registry_slots` are declared; the records inside them are not decoded.** The declaration
  claims the slot's *source, width, binding site and consumers* — not the meaning of a row. **The
  first version of this sheet declined to declare all five on a false premise** ("all five already
  have owners"); they had none. See §8.
- **`Inert` means "no reader found by these searches", and here they are.** (a) every `[rbp+N]`
  reference in `AreaArd_BindLoadedRootAndBattleSections`; (b) every RIP-relative operand in all
  38,161 functions, decoded per-function; (c) the `section_019` binder, which carries the same
  header. **It does not mean "nothing anywhere reads it"** — that would need a census of every
  computed access, and the failure at the top of §6 is the reason to say so out loud.
- **Six header fields, five registry slots and four `st2e` tables are three different counts.**
  This document does not claim `slot0..slot7` are all `st2e`, nor which four of them are. Deciding
  that needs the record layouts, which are the container sheet's.
- ~~**`FUN_003DCF00` and `FUN_003DCF10` were not read.** `slot7`'s consumer is named and not explained.~~ **CC-10 answered 2026-09-12 (FABLE).** `FUN_003DCF00` and `FUN_003DCF10` are eight-byte setters (`003DCF00`, `003DCF10`) of two table
  pointers, `02B58178` (slot 7 of the `.ard`) and `02B58180` (`section_019`'s `+0x2C` table); a scan of
  every rip-relative access finds one reader, **`003DCA30`**, plus the binder `003DCBC0` that nulls both
  at start-up. `003DCA30(modelKey, groupId, class, &primary, &secondary)` sets `primary = 0x1E` and
  searches the **`.ard` table first, then `section_019`'s**, over 16-byte entries
  `{u32 modelKey; u16 class; u16 groupId; u16 motionIndex}`: a `(modelKey, groupId)` match yields
  `secondary = motionIndex`, a `(modelKey, groupId, class)` match `primary = motionIndex`
  (`003DCA5F`–`003DCB85`). Its callers are `003DC5B0` (key = the caller record's `+0x0C`, group its
  word `+0x10`, class its byte `+0x12`) and `003DC8D0` — the swing motion-file selection that picks
  `cNNNN_10_XXXX.ca` / `mNNNN_10_XXXX.ca`, [the authored-data table registry](../../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md). So **slot 7 / `section_019` is the per-model
  motion-index override table**, the area's overriding the script's. Corpus (271 `section_019`
  carriers, 2,116 entries, up to 33 per file): keys are a letter in the high word (`m` 109 ×1,449,
  `n` 110 ×658, `s` 115 ×9) over a model number, classes 1 (×1,698), 3, 9, 11–15, groups 500–743,
  904–944 and 4000–4008, motion indices 60–2306 (1,161 distinct). The `.ard` slot is 0 in all 166
  `in` files, so in the shipped game only the script-side table is ever bound.
- **The `.fpk` slot is described from the table, not from a load.** No `.fpk` ships, so the
  `2i + 1` path is never exercised in retail data.

  **The 7,520 `.fpk` strings now reconcile in closed form, and the account needs both this
  document's dataset and a neighbouring session's.** `.fpk` is a **field of a fixed-width record**,
  not an optional extra, and its stems have *mixed* multiplicity — which is why it is the one
  extension whose strings-per-stem is not an integer (7,520 / 924 = 8.139):

  | population | stems | ×variants | strings | from |
  |---|---:|---:|---:|---|
  | namespace 5 maps, `{ebp, mot, fpk}` | 709 | 10 | 7,090 | the other session |
  | namespace 21 areas, `{ard, fpk}` | 215 | 2 | 430 | **this document** |
  | | **924** | | **7,520** | |

  **Both totals were measured independently and both match exactly** — 7,520 strings over 924 stems.
  A prediction that combines two separately derived datasets and lands on the measured figure twice
  is a far stronger test of either than re-counting one array. The variant multipliers check the
  same way: `.mot` and `.ebp` 10,380 / 1,038 = **10.000**, `.snd` and `.vpc` 3,290 / 329 = **10.000**,
  `.vpcjp` 658 / 329 = **2.000**, and this sheet's `.ard` 430 / 215 = **2.000**.

  > **So `.fpk` is not authored capacity at all.** The carrier README reads its 7,520 paths against
  > 0 files as *"capacity the shipped game never uses"*. **Nothing chose to name 7,520 packages — a
  > record width did.** Three fields wide in namespace 5, two here, and an `.fpk` name exists
  > wherever a record exists. That is a different kind of fact from unused authored intent, and it
  > removes the `.fpk` half of §5's "third instance of one shape" — `trailerOff` and the 49 dead
  > `.ard` paths remain; `.fpk` was never an instance of it.
- **`AreaData_BindAndRebaseSectionDescriptor`'s descriptor fields** (`+0x00`, `+0x10`, `+0x14`,
  `+0x18`, `+0x1C`) are recorded as rebased; **what they point at is not established.**

## 8. Corrections and record

**2026-09-04 — "all five slots already have owners" was false, and it cost four declarations.**

The first version of this sheet declined to declare any `registry_slots`, on the stated ground that
`0x02EBF120`, `0x02EBF140`, `0x02EBF148`, `0x02EBF150` and `0x02EBF168` were owned elsewhere. **None
of them was.** The five declared slots in the database are `0x02EBF0C0`, `0x02EBF0F8`, `0x02EBF138`,
`0x02EBF160` and `0x02EBF190`; `registry_explained` stood at 5 / 63 and not one of those five was
this document's. The coordinator caught it; it was verified here before acting on it, and the
gambit document does declare `0x02EBF160` — a different slot one hex digit away from `0x02EBF168`.

**How the wrong reading was reachable, because that is the part worth keeping.** A `grep` for those
addresses returns hits in three other documents, and the addresses are genuinely *discussed* there —
`0x02EBF120` and `0x02EBF150` at length. **Discussion was read as ownership.** That is rule 3c's own
warning running backwards: the rule exists because `0x02EBF138` is *mentioned* in ten documents and
*explained* in one, which is why the numerator counts declarations rather than scraping prose. The
same gap that makes a mention look like an explanation makes it look like a declaration.

**Why no single session could have caught it.** The declaration set lives across all documents'
frontmatter; a session sees its own file and whatever it greps. The check that settles it is
`check_formats.py`, and running that — rather than trusting a `grep` — is the fix.

**What did not change:** the reading. The `.ard`→registry mapping, the binding sites and the consumer
sets are unchanged and tier 1. Only the declaration decision was wrong.

## 9. Related

- [`README.md`](README.md) — the carrier census: 166 areas, 4 `st2e` tables, the path table
- [`area-nmb-index.md`](area-nmb-index.md) — the strict pair. Its entry count matches the **second
  `st2e` table** 166/166, tested on the subsets where the four tables disagree (122/122, 63/63,
  7/7), one 3-byte entry per record.

  > **Mind the two numberings.** The `st2e` tables are the *present* slots `0, 2, 5, 6`, so the
  > "second `st2e` table" is **slot 2** — the one this loader binds as category 2 into
  > **`0x02EBF120`**, which is also the slot with the widest reader set in §4
  > (`BattleUnit_ApplyUnitDefinition`, `BattleEncodedId_IsValidForClass`,
  > `BattleStats_InitializeDefinitionRecord`). Two independent lines of evidence therefore point at
  > slot 2 as the per-area unit list. **Both are still leads** — the `.nmb` entries have no reader,
  > and this document names slot 2's consumers without decoding its records.
- [`../authored-data-table-registry.md`](../../authored-data-table-registry.md) — the 63-slot
  registry; **§4 here supplies the on-disk source for five of its slots** and resolves that
  document's "plausibly binds against four slots" to an exact five-way mapping
- [`../../../00-Engine-Core-Runtime/the-encoded-id-class-registry.md`](../../../00-Engine-Core-Runtime/the-encoded-id-class-registry.md)
  — owns `0x02EBF120` and `0x02EBF150`
- [`../../../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md`](../../../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md)
  — owns `0x02EBF168`, the order-set directory this loader fills from `slot1`
- [`../../../08-Combat-Formula/where-a-stat-number-comes-from.md`](../../../08-Combat-Formula/where-a-stat-number-comes-from.md)
  — reads `0x02EBF150` for the foe base table
- [`../../../25-EBP-Script-Container/Container/ebp2-container.md`](../../../25-EBP-Script-Container/Container/ebp2-container.md)
  — the same `(namespace, index)` resource path, and the same never-validated-magic result
- [`../../../25-EBP-Script-Container/Sections/section-019.md`](../../../25-EBP-Script-Container/Sections/section-019.md)
  — the same `FF12AR03` header embedded in a script container, using only `+0x2C`

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**The area unload `002628B0`, which this page cites, is a multi-layer teardown — SERVICE.** It calls `PartyControl_SetMovementSuppressionBit` and `PartyFocus_ClearCurrentActorIfEligible` (**Party**), six movement helpers (**Movement**), three small Audio-filed bodies (**Audio**), `CharacterRenderSystem_RefreshDistanceCullEna…` and three Presentation bodies (**Presentation**), and a 126-byte Input helper (**Input**).

- **Party — MECHANICAL.** The id-validity query `BattleEncodedId_IsValidForClass` is also asked by the party-roster
  functions: `PartyConfiguration_ReconcileRuntimeRosterFir…`, `PartyConfiguration_CollectRuntimeRosterSelec…`,
  `PartyFocus_SelectAndRequestDefaultActor` and five more.
- **Movement — MECHANICAL.** The same query is asked by two locomotion bodies.
- **Audio and Presentation — CLIENT.** `0035A490` is called by the 335-byte Audio body. The movie table `002DF980` is
  read by a 1,636-byte Presentation body, and the swing motion-file selector `003DC8D0` by a 504-byte one.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Rewards_Progression_Economy — SERVICE.** `0023AC80` on this page calls `FUN_0030c470`, owned by that layer. What it reaches is a per-record step that reads the `byte[+4]` / `byte[+5]` kind-and-state pair and clears `byte[+0x1C2]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
- **ActorEntity — CLIENT and SERVICE (131 edges).** 112 inbound (ActorEntity bodies `002628B0`, `0025AFC0`, `ActorResource_BeginManagerResourceSetLoad` (0032FCA0) call page-cited `00263FF0`, `ActorManager_GetRecordByOrdinal` (00358940), `BattleEncodedId_IsValidForClass` (00322C50)); 19 outbound (page-cited `002628B0`, `ActorSystem_ReleaseManagerRecords` (0025B070), `BattleUnit_ApplyUnitDefinition` (0023A570) call ActorEntity bodies `00263FF0`, `0026A480`, `ActorWork_GetBattleUnit` (0031B760)). Substantive edges include `BattleUnit_ApplyUnitDefinition` (0023A570) is called by `BattleUnit_TeardownAndDespawn` (00300E40); `BattleUnit_ApplyUnitDefinition` (0023A570) is called by `BattleGroup_RefreshFourActorDefinitions` (003266C0); `BattleUnit_ApplyUnitDefinition` (0023A570) calls `BattleUnit_ResetStateForReuse` (00236A60); `BattleUnit_ApplyUnitDefinition` (0023A570) calls `00322050`; the remaining edges run through shared helpers the page cites.
- **CombatAI — CLIENT and SERVICE (17 edges).** 11 inbound (CombatAI bodies `AiOrder_EvaluateTargetSelector` (00301AD0), `BattleEnmity_ReadForCombatantId` (003215C0), `BattleEnmity_ClampAndStore` (00321E40) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `AreaData_BindAndRebaseSectionDescriptor` (003845F0)); 6 outbound (page-cited `BattleStats_InitializeDefinitionRecord` (0023AC80), `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130) call CombatAI bodies `GambitRuntime_RebuildOrderSetForStatsRecord` (00327DE0), `GambitConfig_InitializeThreeBanksFromBasePairs` (00326030), `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` (00327CB0)). Substantive edges include `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `GambitRuntime_RebuildOrderSetForStatsRecord` (00327DE0); `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `GambitConfig_InitializeThreeBanksFromBasePairs` (00326030); `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` (00327CB0); `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0) calls `BattleEnmity_AdjustOtherRelevantCombatants` (00321B00); the remaining edges run through shared helpers the page cites.
- **CombatAction — CLIENT and SERVICE (11 edges).** 10 inbound (CombatAction bodies `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0), `BattleAction_CheckGlobalCategoryDisableReason` (0031A7B0), `BattleAction_CheckActionAvailabilityReason` (002FFCF0) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130), `BattleStats_ClearStatusLayer0AndProcessSideEffects` (0030E970)); 1 outbound (page-cited `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) call CombatAction bodies `BattleUnit_CancelAndResetCurrentAction` (003105D0)). Substantive edges include `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) calls `BattleUnit_CancelAndResetCurrentAction` (003105D0); the remaining edges run through shared helpers the page cites.
- **CombatFormula — CLIENT and SERVICE (9 edges).** 2 inbound (CombatFormula bodies `BattleFormula_ApplyTargetResult` (003112F0), `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) call page-cited `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130), `BattleEncodedId_IsValidForClass` (00322C50)); 7 outbound (page-cited `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130), `BattleUnit_ApplyUnitDefinition` (0023A570) call CombatFormula bodies `BattleStats_InitializeDefinitionRecord` (0023AC80), `002F9180`, `002F8E50`). Substantive edges include `BattleUnit_ApplyUnitDefinition` (0023A570) calls `BattleStats_InitializeDefinitionRecord` (0023AC80); `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) calls `002F9180`; `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) calls `002F8E50`; the remaining edges run through shared helpers the page cites.
- **CoreRuntimeScheduling — CLIENT and SERVICE (2 edges).** 1 inbound (CoreRuntimeScheduling bodies `0022A0B0` call page-cited `002DF9A0`); 1 outbound (page-cited `002628B0` call CoreRuntimeScheduling bodies `00229EE0`). Substantive edges include `002628B0` calls `00229EE0`; `002DF9A0` is called by `0022A0B0`.
- **Items_Equipment_Shops_License — CLIENT and SERVICE (16 edges).** 14 inbound (Items_Equipment_Shops_License bodies `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` (0030A4E0), `BattleIdClassD_GetRuntimeFlagBit1` (0030B510), `InventoryDerivedIndex_UpdateOnPresenceTransition` (00325F40) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30)); 2 outbound (page-cited `BattleStats_InitializeDefinitionRecord` (0023AC80) call Items_Equipment_Shops_License bodies `BattleStats_SetLicenseNodeStateAndApplySideEffects` (00323910), `BattleStats_SetEquipmentSlotDirect` (0031A630)). Substantive edges include `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `BattleStats_SetLicenseNodeStateAndApplySideEffects` (00323910); `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `BattleStats_SetEquipmentSlotDirect` (0031A630); `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) is called by `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` (0030A4E0); the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — MECHANICAL (2 edges).** 1 Save_Load_Settings-side calls into shared helper(s) the page cites (`0032E620`); 1 call from page-cited bodies into shared Save_Load_Settings plumbing (`SaveImage_GetPersistentPayloadBase` (002EF2B0)) - the helpers' general call surface, not a Save_Load_Settings relationship of this page's subjects.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (83 edges).** 82 inbound (Script_VM_Native_Bridge bodies `00340FA0`, `0050DAD0`, `0050D8F0` call page-cited `00263FF0`, `ActorManager_GetRecordByOrdinal` (00358940), `002E9A60`); 1 outbound (page-cited `VM_BattleUnit_SelectAiOrderSetVariant` (00510580) call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10)). Substantive edges include `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` (00239040) is called by `VM_BattleUnit_SelectAiOrderSetVariant` (00510580); `002E99C0` is called by `00340FA0`; `002E99C0` is called by `003414A0`; the remaining edges run through shared helpers the page cites.
- **Spawn_Encounter_Lifecycle — CLIENT and SERVICE (2 edges).** 1 inbound (Spawn_Encounter_Lifecycle bodies `Spawn_ApplyScriptSelectedUnit` (0023A3B0) call page-cited `BattleUnit_ApplyUnitDefinition` (0023A570)); 1 outbound (page-cited `BattleUnit_ApplyUnitDefinition` (0023A570) call Spawn_Encounter_Lifecycle bodies `SpawnKeep_ResolvePrimaryEntry` (00236100)). Substantive edges include `BattleUnit_ApplyUnitDefinition` (0023A570) is called by `Spawn_ApplyScriptSelectedUnit` (0023A3B0); `BattleUnit_ApplyUnitDefinition` (0023A570) calls `SpawnKeep_ResolvePrimaryEntry` (00236100).
- **Status_Periodic_Terminal — CLIENT and SERVICE (14 edges).** 6 inbound (Status_Periodic_Terminal bodies `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleStats_ClearStatusLayer0AndProcessSideEffects` (0030E970), `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130), `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30)); 8 outbound (page-cited `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130), `BattleStats_ClearStatusLayer0AndProcessSideEffects` (0030E970) call Status_Periodic_Terminal bodies `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130), `BattleStats_RemoveAllMode0StatusesAndRecompute` (0030E8F0)). Substantive edges include `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0) calls `BattleStats_RemoveAllMode0StatusesAndRecompute` (0030E8F0); `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0) calls `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0); `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0) calls `BattleStats_ClearStatusLayer0AndProcessSideEffects` (0030E970); `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0) calls `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360); the remaining edges run through shared helpers the page cites.
- **UI — MECHANICAL (2 edges).** 1 UI-side calls into shared helper(s) the page cites (`BattleEncodedId_IsValidForClass` (00322C50)); 1 other inbound edge(s) - the helpers' general call surface, not a UI relationship of this page's subjects.
- **World — CLIENT (11 edges).** 11 inbound (World bodies `00378540`, `00266D10`, `0025E400` call page-cited `ActorManager_GetRecordByOrdinal` (00358940), `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `002EA690`). Substantive edges include `003DCBC0` is called by `00266D10`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (64 edges).** 49 inbound (WorldAreaField bodies `AreaArd_LoadOrUnloadFieldResource` (003EA820), `MapRef_BeginLoadResources` (00268750), `00378030` call page-cited `0036C660`, `0036C110`, `0036C1A0`); 15 outbound (page-cited `002628B0`, `BattleData_SetAreaArdSectionCategory` (0023A160), `AreaArd_RefreshForMapRefField` (003EA6E0) call WorldAreaField bodies `003846F0`, `BattleData_SetAreaArdSectionCategory` (0023A160), `003DCF00`). Substantive edges include `BattleData_SetAreaArdSectionCategory` (0023A160) is called by `AreaArd_BindLoadedRootAndBattleSections` (003EA710); `BattleData_SetAreaArdSectionCategory` (0023A160) is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820); `BattleData_SetAreaArdSectionCategory` (0023A160) calls `003846F0`; `002628B0` calls `003DFA50`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (83 edges).** 82 inbound (Script_VM_Native_Bridge bodies `00340FA0`, `0050DAD0`, `0050D8F0` call page-cited `00263FF0`, `ActorManager_GetRecordByOrdinal` (00358940), `002E9A60`); 1 outbound (page-cited `VM_BattleUnit_SelectAiOrderSetVariant` (00510580) call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10)). Substantive edges include `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` (00239040) is called by `VM_BattleUnit_SelectAiOrderSetVariant` (00510580); `002E99C0` is called by `00340FA0`; `002E99C0` is called by `003414A0`; the remaining edges run through shared helpers the page cites.
## The `0025AFC0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0025AFC0` — the `ActorResource_OnDefinitionPayloadLoaded` load/unload arm —
saves `qword[02099D70]` (the actor-list head, base `02098E10` at
`0025AFD7`), runs the setter triple `0035A270`/`0035A490`/`0035A3A0`
(`0025AFEC`–`0025AFF6`), gates on `byte[02099DA0]` (`0025AFFB`),
`002E4000`/`002E3E20` with `edx=1` (`0025B00B`/`0025B017`), the
clearer pair `0035AD40`/`0035AC60`/`0035AB50` (`0025B01C`–`0025B028`),
zeroes `byte[02099DA0]`/`byte[02099DA6]` (`0025B02F`/`0025B036`),
`002EA870`/`002EA690`, then members `002ECBE0`/`002EBDE0`
(`0025B049`/`0025B050`), and restores `02099D70` (`0025B055`). The
`0025B070` arm compares `word[rcx+0x1DA]` vs `word[rcx+0x1D2]` and
rebinds through `00358940` on mismatch (`0025B0A0`/`0025B0AA`).

| member | role | interior |
| --- | --- | --- |
| `002EBDE0` (58 B) | list remove — `[0215FD58]` head (`002EBDEA`), `dword[rbx+0x10]` → `0036C5D0` (`002EBDF8`/`002EBE01`), `rbx = [rbx+8]` next (`002EBE06`) | [`002EBE01`](../../../_index/ADDRESS-INDEX.md) |
| `002ECBE0` (117 B) | list walk — `[0215FD68]` head (`002ECBEA`), `edi = 0x20` bound (`002ECC14`), `dword[rbx]` reads (`002ECC20`) | [`002ECC20`](../../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0035A270`, `0035A490`, `0035A3A0`,
`002E4000`, `002E3E20`, `0035AD40`, `0035AC60`, `0035AB50`,
`002EA870`, `002EA690`, `00358940`, `0036C5D0`. The `0215FD58`/
`0215FD68` pair are the resource list heads the load arm drains.

## The `002FDDA0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002FDDA0` (`BattleUnit_ExecuteDirectStateCommandOrder`, ~25 B) — reads
`qword[+0x708]`, `word[+0x714]`; `byte[+0x6B4]` gate, `movsx word[rax+2]`
(`002FDDA6`/`002FDDBE`).

| member | role | interior |
| --- | --- | --- |
| `0030E970` | `0030E130(rcx, edx, r8=0, out=[rsp+0x20])` — 4-arg order-issue wrapper (`0030E974`/`0030E97F`) | [`0030E974`](../../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0030E130`.

## SWE2-EC7-24 update (2026-09-18) — `0035AD40`/`0035A490` flag clear/set pair

`0035AD40` (191 B) and `0035A490` (244 B) are the clear/set counterparts over
the same chain: per index `ebx`, `0031C470` fetches the entry, `002EB7A0` +
`002E99C0` resolve the carrier, and `byte[+0x19]` loses/gains bit 0.
`0035AD40` then runs the `00320230` lookup and double `002ECAB0` notify with
`r8d=0`; `0035A490` gates the set on `002E4C20` and notifies with `r8d =
found+1`. Both fall through to the `0031C0E0` second-pass arm. Interior
anchors `0035AD52` / `0035A4A3` (the `0031C470` fetch).

## SWE2-EC7-25 update (2026-09-18) — the `0215FD58` node-list family behind `0035AD40`/`0035A490`

`002EB7A0` (52 B) is a `ecx <= 0xD` jump-table dispatch over `0x1CB7D4` —
each of the 13 arms returns a packed `0x00XX00YY` constant (`0x630000`,
`0x6E0001`, `0x770002`...): the kind-to-paired-id table `0035AD40`/`0035A490`
feed into `002E99C0`. Interior anchor `002EB7AF` (the table fetch).

`002E99C0` (63 B) is the two-list key search this page's flag pair resolves
through: walks `0215FD58`'s `+8`-linked nodes matching `dword[+0x14] == ecx`,
falls through to the `0215FD78` list on miss, returns the node or 0.
Interior anchor `002E99D0` (the key compare).

`002ECAB0` (181 B) is the flag-channel write the notify path drives: same
two-list `+0x14` search, then `movsx word[+0x1E]` indexes `02161DA0` records
at `*0x120` (`lea *9, shl 5`), gated on `[rdx+0x5C] == [rax+0x24]` generation.
Bit `1 << r9d` is tested against `+0x34|+0x28|+0x24`; `r10d` selects OR-set or
AND-clear into `+0x38`, and `r8b & 1` reads the result back. Interior anchor
`002ECAF4` (the `movsx` index fetch).

`002E4C20` (16 B) is the null-safe `byte[+0x18] & 2` test `0035A490` gates
its set arm on. Interior anchor `002E4C25` (the `movsx`).

## SWE2-EC7-27 update (2026-09-18) — `002E4000` / `002E3E20` / `002E9A60` registry-list helpers

`002E4000` (325 B) walks the `0215FD68` list and for each node rotates
a `1 << i` mask through 32 positions (`word[+0xE0]`-indexed count): per
channel it clears `+0x48` (or zeroes it when `edx < 0`), and when the
`+0x4C..0x58`/`+0x38`/`+0x3C` mask lanes are quiet while `+0x24`/`+0x28`/
`+0x34` are live and `+0x2C` is clear, it sets `+0x2C` and unlinks the
node onto the `0215FD90` freelist head. The registry's 32-channel sweep
and free-list return. Interior anchor `002E40BA` (the `+0x2C` set).

`002E3E20` (107 B) walks the `0215FD58` list clearing `1 << cl` out of
each node's `word[+0x20]` (all bits when `edx < 0`); when
`word[+0x1C] <= 0` the bit stays cleared and `byte[+0x19] & 3` is 0,
the node is rearmed through `002EAEB0`. Interior anchor `002E3E62` (the
rearm gate).

`002E9A60` (46 B) — reached through `0035A270`/`0035AB50` — splits on
`ecx < 0x1000000`: small kinds tail-jump `002EB7A0` (this page's
kind-to-packed-ID selector), large ids `002640C0`-resolve then
`00263F80`. The bridging dispatch that hands authored kinds to the
registry selector. Interior anchor `002E9A89` (the `002EB7A0` tail).

## SWE2-EC7-45 update (2026-09-19) - `0037C3F0`

`0037C3F0` (~~248 B~~ **0x308 B**) is the `+0x0C trailerOff` callback - `0020E600`/`00263FF0`/`003601B0`/`003EA650`. Interior anchor `0037C43B` (a `0020E600` call).
*Extent corrected 2026-09-21 (FABLE): `functions.tsv` records 248 bytes, ending at `0037C4E8`, but nine of
the body's eleven jump-table arms lie past that, out to `0037C6C3`, with the table at `0037C6F8` — the
recorded extent stops at the end of state 0's arm, where linear decoding after the indirect `jmp rcx`
stops. The figure above was inherited from the table, not measured.*

## SWE2-EC7-45 update (2026-09-19) - `003DC5B0`

`003DC5B0` (238 B) is the motion-file-selection caller - `0032E620`/`0036A000`/`0036B160`/`0036C110`/`0036C140`/`0036C1A0`/`0036C1D0`. Interior anchor `003DC5EA` (a `0032E620` call).

## SWE2-EC7-46 update (2026-09-19) - `0035A3A0`

`0035A3A0` (233 B) is the flag-mask setter of the `0035A3A0`/`0035AC60` pair - `002E4C20`/`002E99C0`/`002EB7A0`/`002ECAB0`/`003EA650`; sets actor `+0x19` bit 0, passes on = 1. Interior anchor `0035A3C4` (a `002E4C20` call).

## SWE2-EC7-47 update (2026-09-19) - `0035AC60`

`0035AC60` (211 B) is the flag-mask clearer of the `0035A3A0`/`0035AC60` pair - `002E99C0`/`002EB7A0`/`002ECAB0`/`003EA650`; clears actor `+0x19` bit 0, passes on = 0. Interior anchor `0035AC84` (a `002E99C0` call).

## SWE2-EC7-50 update (2026-09-19) - `00320230`

`00320230` (183 B) is the `0035AD40`-driven lookup - `00303EC0`/`00304650`/`00322C50`. Interior anchor `00320240` (a `00303EC0` call).

## SWE2-EC7-94 update (2026-09-20) - `00331880` measured

`00331880` (62 B) is the gated bind tail `003DFA50` and `003EAA00`
call: `00408B30` returning 1 or `00408B10` returning 3 both exit,
and `005C5230(5)` must be nonzero before it tail-calls
`003697F0(rcx)` - the deferred bind step the loader only runs when
the mode pair permits it.
Interior anchor `003318A2` (the `005C5230` call).

## SWE2-EC7-95 update (2026-09-20) - `0031C470` measured

`0031C470` (68 B) is the table-byte fetch `0035A490` and
`0035AD40` call: `00322C50(0x17, ecx, 0)` admits
`byte[02EC01xx + ecx*2 + 0x5A90]` (`0xFF` maps to `0xFFFF`, as
does a failed gate), and it tails `0031C2F0` with the word.
Interior anchor `0031C482` (the `00322C50` call).

## CC-7: slots 5 and 6 are a base row and a growth row (FABLE, Claude Opus 5.5, 2026-09-26)

The two 56-byte slots were already known to be one layout used twice. **They are used as a base and a per-level
increment.**
- **Binding.** `BattleUnit_ApplyUnitDefinition` binds, per unit, a slot-5 row chosen by the definition's word `+0x22`
  and a slot-6 row chosen by its word `+0x24`, and keeps them at unit `+0xE70` and `+0xE78`.
- **Every reader combines them one way:**
  `value = slot6[f] × (level − byte[stats + 0x88]) + slot5[f]`, where `stats` is the unit's stats record and the
  level is its `+0x1C2`.
- **The readers name the fields:**
  - experience at `+0x34` (`Reward_ComputeExperienceForRecipient`);
  - licence points, a byte at `+0x2F` (`Reward_ComputeLicensePointsForRecipient`);
  - gil at `+0x30` (`BattleUnit_ProcessDefeatRewardsAndLoot`);
  - a word at `+0x00`, which one more reader passes on with code `0x11`.

So slot 5 is the value at the reference level `byte[stats + 0x88]`, and slot 6 is what each level above it adds.
That is the growth-versus-base reading, now read rather than proposed.

*Not read here:* what writes `stats + 0x88`, beyond its role as the level the base row describes. Control: [`cc7_base_growth.py`](../../../_index/candidates/cc7-ard-base-growth/cc7_base_growth.py)
(3 checks, FAILS 0).
