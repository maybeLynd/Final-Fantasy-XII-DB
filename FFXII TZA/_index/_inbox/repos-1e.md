# repos-1e — lane 1

## STATUS — 2026-09-06 (round 5: auditor, and a correction to the board's own critical-path block)

**Row read from the 10:40 rewrite: auditor, unchanged.** No author output has landed yet — the three
author rows were re-issued at 10:40. So I audited **the thing all three of them are told to build
on**: the board's *"What is already established — start from here, do not re-derive it"* block.

**Six of its seven claims verify exactly. One is wrong, and it is the one that says where the rows
come from.**

---

## AUTHOR OUTPUT AUDITED AS IT LANDED — `the-definition-record-flag-pair.md`

`repos-c7`'s sheet landed mid-round and I audited it immediately, per my row. **`passes: 0` → `1`.**

**The three load-bearing figures reproduce exactly** by an independent scan: **229** `OR`-sites,
**162** distinct functions, and the **same ten bit positions** (0, 1, 3, 4, 5, 13, 14, 16, 27, 31).
**Its centrepiece re-derives from the bytes**: the six-entry jump table at `0x0030E88C` resolves to
exactly the six case addresses listed, and `0x0030E531 test dword ptr [rsi+0x38], edi` /
`0x0030E534 jne` is the immunity guard — **a bit set in `+0x038` really does make that bit
unsettable in `+0x064`, and cases 4 and 5 have no equivalent.**

**Two defects, both minor and neither touching a conclusion:**

- *"9 distinct masks"* is correct **scoped to `test`**; widening to `and` finds two more
  (`0x1`, `0x8800003B`). **Neither adds a bit position**, so the headline ten-bit figure is robust
  to the scoping while the mask count is not — the right way round for the claim the sheet rests on.
- *"`.text` scanned: **8,001,280** bytes"* **does not reproduce.** The section table gives
  **7,996,981** virtual / **7,997,440** raw — a 3,840-byte gap, not a rounding. **Left for the
  author**; the census is driven by the function list, not that number, so the result is unaffected.

**The sheet grew between the start of my pass and its end** — it gained `+0x038`, the jump table and
the guard. I re-derived those too rather than let a `passes: 1` stand over material it never saw.
**A pass has to say what it covered, and "the document at the time" is not a description anyone can
check.**

### The defect generalises — a second function, same contamination

`repos-3f` applied my board-block warning to their own reader and found it there too. I reproduced
their scan exactly: `BattleUnit_ApplyUnitDefinition` (`0x0023A570`, 1,808 B, 452 instructions)
references **eight** registry slots, **three of them outside the `.ard` family** —
`0x02EBF170`, `0x02EBF130` (the same growth table) and `0x02EBF190` — with the first non-`.ard`
reference at `0x0023A860`.

> **So it is not local to `0x002FEF30`. Two independent functions mix `.ard` and non-`.ard`
> descriptors using identical lookup code, and nothing in the instruction shape separates them.**

**And `repos-3f` sharpened the diagnosis in a way worth adopting:** the block is wrong *twice over*,
because **`0x02EBF168` IS one of the five `.ard` slots and is NOT an `st2e` table** — its count is a
bare `u16` at `+0x00`, not a descriptor `+0x04`. So *"the four `.ard` `st2e` tables (84/88/56/56)"*
and *"one of the four"* name **different sets of four**, and the block treats them as one. That
explains why the error was invisible: **both readings are individually true of *a* set of four.**
It is corroborated three ways already on disk — my `.ard` sheet has category 1 bound by a different
binder, `repos-d6`'s census has directory slot 1 carrying no `st2e` table (0/166), and `repos-3f`'s
five-differences list.

## VERIFIED FOR THE CRITICAL PATH: `.ard` directory slot 1 is the `.nmb` container

`repos-3f` tested an objection I raised — that their slot-1 join was bounded against a `u16` they
had *assumed* was a count — and the test produced a better result than the objection. **I reproduced
all five of their header tests from the 166 extracted `.ard` files with my own parser:**

| test | result |
|---|---|
| `+0x02 == 100` | **166 / 166** |
| `offsets[0] == 4 + 4*(count+1)` | **166 / 166** |
| offsets ascending | **166 / 166** |
| `offsets[count]` within the block extent | **166 / 166** |
| every offset inside the block | **166 / 166** |

**That is exactly the header and offset table in `area-nmb-index.md`** — `{u16 count, u16
version=100, u32 offsets[count+1]}` — which I audited on 09-06 and confirmed at 11/11. **So the same
container ships as the standalone per-area `.nmb` file and as `.ard` directory slot 1.** One design
used twice, the `CML1`-across-EBP-slots-8-and-10 trick again. And the `u16` **is** a count,
established by the container's own arithmetic rather than assumed.

### The payload has a stride, and that is the part the critical path needs

`repos-3f` characterised the payload as *"56 B in 165 areas then 872/800/632/1256/1136/920/944"*,
which reads as a list of sizes. Measured over **all 1,422 slot-1 entries**:

> **`entry length mod 24 == 8` in 1,422 of 1,422.** Every entry is exactly **`8 + 24k`** bytes,
> `k = 2 … 125`, min 56, max 3,008.

**So a slot-1 entry is an 8-byte header plus `k` records of 24 bytes**, and the size variation is a
record count rather than an arbitrary size. **24 is the record stride** — the thing the *"what a row
means"* work needs next — and it is none of `84 / 88 / 56 / 56`, which is a fifth independent reason
slot 1 is not an `st2e` table. *(Their 165 counts **areas** containing a 56-byte entry; my 1,422
counts **entries**. Different populations, not a conflict.)*

**What I deliberately did not name.** The 8-byte entry header is `(1,0)` ×165, `(2,0)` ×27, `(4,0)`
×15 — which looks like a small count — but also `(1282,1541)` ×18 and `(772,2563)` ×18, which do
not. **The `8 + 24k` arithmetic is solid; the header's fields are not**, and I would not let the
first three rows of that distribution name a field.

### One asymmetry survives the tidy explanation, and it should

Four of `repos-3f`'s five slot-1 asymmetries collapse into *"it is a different container"*. **The
fifth does not: the signed `jg` at `0x0023A724` where the other three joins use `ja`.** A container
difference does not make an index signed. **Once the other four are explained, the signed compare is
the only thing left that the explanation does not cover** — which makes it more diagnostic, not
less, and it should not be pulled along by the tidy account of its neighbours.

## ⚠ FOR THE COORDINATOR — THE "ALREADY ESTABLISHED" BLOCK HAS A DEFECT

The block reads:

```
definition record +0x004        the row index (one byte)
  x  stride       .ard slot descriptor +0x08
  +  baseOffset   .ard slot descriptor +0x0C, resolved vs arena 0x01F83530 (via 0x20E600)
  -> a row in one of the four .ard st2e tables  (84 / 88 / 56 / 56)
```

**`BattleStats_RebuildEffectiveStatsAndAffinityState` performs that lookup TWICE, against TWO
DIFFERENT registry slots, and only one of them is an `.ard` slot.**

| lookup site | `imul` by `[rdi+4]` | slot resolved against | is it `.ard`? |
|---|---|---|---|
| `0x002FF065` | yes | **`0x02EBF130`** | **NO** |
| `0x002FF119` | yes | `0x02EBF120` | yes — `.ard` directory slot 2 |

**`0x02EBF130` is class 2, *character/unit growth definitions*** — 23 references, read by
`BattleUnit_ApplyUnitDefinition` (`0x0023A570`) and
`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0x0030C650`). It is documented in
[`the-encoded-id-class-registry.md`](../../00-Engine-Core-Runtime/the-encoded-id-class-registry.md)
and in the registry sheet. **The `.ard` loader does not fill it** — that loader binds exactly
`02EBF150 / 02EBF168 / 02EBF120 / 02EBF148 / 02EBF140`, and `0x02EBF130` is not among them.

> **So "→ a row in one of the four `.ard` st2e tables" is true of one lookup and false of the other.**
> An author who takes the block at face value will attribute **growth-definition** rows to `.ard`
> tables. That lands directly on `repos-3f` (decoding the four `st2e` row layouts) and on `repos-c7`
> (reading this exact function).

**And the function reads seven registry slots, not four:**

| slot | refs here | what it is |
|---|---:|---|
| `0x02EBF040` | 10 | status auxiliary / timer parameters — **not `.ard`** |
| `0x02EBF0F8` | 3 | equipment definitions — **not `.ard`** |
| `0x02EBF120` | 3 | `.ard` slot 2 |
| `0x02EBF130` | 3 | character/unit growth definitions — **not `.ard`** |
| `0x02EBF140` | 3 | `.ard` slot 6 |
| `0x02EBF148` | 3 | `.ard` slot 5 |
| `0x02EBF150` | 3 | `.ard` slot 0 |

Each appears in the same three-reference shape (slot → `+0x0C` → `0x20E600` → `+0x08` stride).
**`0x02EBF168`, the gambit order-set slot, is NOT read here** — consistent with four `.ard` slots
feeding stats and one feeding AI.

**The registry document is not at fault.** `authored-data-table-registry.md` §5 states the lookup
generically — *"any gameplay lookup → read slot pointer → count at `+0x04` → stride at `+0x08` → RVA
at `+0x0C` → row = base + index × stride"* — and never says `.ard`. **The `.ard` attribution was
introduced by the board's summary.** That is the same shape as the failure the 10:40 rewrite was
written to fix: a summary that reads as settled and is one clause stronger than its source.

### A second, smaller correction: `+0x004` is not only a row index

The block calls `+0x004` *"the row index (one byte)"*. It is that — and it is **also range-tested as
an actor type id**, in the same function, guarded by the `+0x005` gate:

```asm
002FEFFB  movzx ecx, byte ptr [rdi + 5]   ; the gate
002FF003  test  ecx, ecx
002FF005  jne   0x2ff021                  ; non-zero -> skip  (so zero = proceed, as the board says)
002FF007  movzx eax, byte ptr [rdi + 4]
002FF00B  sub   al, 0x1b
002FF00D  cmp   al, 0xc
002FF00F  ja    0x2ff021                  ; in-range iff [rdi+4] in [0x1B, 0x27] -- 13 values
```

**That is the 13-value band already documented** in
[`actor-type-id-partition-and-the-13-value-band.md`](../../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md),
whose §3 records **27 byte-for-byte copies of this same `sub al,0x1b` predicate**. So the byte at
`+0x004` carries a **type id** on one path and a **table row index** on another. **An author naming
`+0x004` as "the row index" and stopping will miss half of what the field does.**

## What DID verify, exactly

| board claim | result |
|---|---|
| `0x002FEF30` is 2,859 B | **2,859**, 735 instructions |
| it touches 20 record offsets | **exactly 20 distinct `rdi` displacements** |
| the 17 named offsets | **all 17 present**, none missing |
| max offset `+0x1C2` fits inside `0x1C8` | **max is `0x1C2`** |
| `+0x005` gates, **zero = proceed** | `test ecx,ecx ; jne` — **non-zero skips**, so zero proceeds |
| stride at descriptor `+0x08` | `movzx ebx, word ptr [rcx+8]` at `0x002FF05D` — a **u16** |
| baseOffset at descriptor `+0x0C` | `mov ecx, [rax+0xc]` at `0x002FF04E`, passed to `0x20E600` |
| arena `0x01F83530` via `0x20E600` | `0x0020E600` is **three instructions**: `mov eax,ecx ; add rax,[0x01F83530] ; ret`. **The arena global is in `.data` but NOT file-backed** — BSS, set at runtime, so it is meaningless in a static dump. |

**The three unread slot blocks are where `repos-c7`'s "the rest of the function is unread" lives** —
`0x02EBF040` (10 refs, the most-referenced slot in the function), `0x02EBF0F8` and `0x02EBF130`.

## COVERAGE

No document was edited this round. **This is a finding about the board, and the board is the
coordinator's file** — I do not edit it beyond my own status cell. The registry document needed no
correction; it was already right.

Gates unchanged and green: links 10,040 / 0 broken, layouts 44 fences / 0 errors, hygiene clean.

**Next:** the three 09-06 format sheets (`tim2`, `chse`, `lmap`) are new, unaudited and in nobody's
partition — `repos-c9` holds the 09-03 backlog. Taking those unless author output lands first.

---
---

# ROUND 4 — the 09-05 sheets (below)

## STATUS — 2026-09-06 (round 4: the 09-05 sheets, an unassigned partition)

**Second auditor row complete. Five more sheets `passes: 0` → `1`.**

`repos-c9` holds the 09-03 backlog and `repos-4b` the EBP sections; **the five sheets written 09-05
by `repos-c7` and `repos-d6` were in nobody's partition.** I took them under the standing
"next unclaimed row" instruction.

**All five survived. No corpus figure and no loader claim in any of them was wrong.** One sheet had
its missing half supplied rather than merely checked.

---

## `efx-and-efb` — the corpus half SUPPLIED, not just audited

**This sheet was written with no file opened**, and said so at the top and in §5: *"the split
between `EFX0008` / `0009` / `0010` across the 3,288 files is unmeasured … the single most useful
number this sheet lacks."* I have the archive mounted, so I measured it.

| accepted by the loader | files using it |
|---|---:|
| `EFX0010` | **3,284** |
| `EFX0008` | **4** |
| `EFX0009` | **0** |
| `EFB0002` | **410** |
| `EFB0001` | **0** |

> **Two of the five accepted versions ship in no file at all.** The loader's version space is
> capacity the shipped game does not exercise — the same shape as `section_017` and the 49 dead
> `.ard` paths. **And the four `EFX0008` files are one logical file**: `l0000.efx` under `ch`, `cn`,
> `jp`, `kr`, 180,448 B each, absent from every other locale. *One surviving `EFX0008` asset*, not
> four.

Also confirmed: all five `.rdata` tag constants hold the strings claimed; the reject path is four
instructions and **returns without parsing**, so §6's correction of the decompiler ("reject
silently", not "default to 10 and carry on") is right; and `EFX0`/`EFB0` occur **0 times in `.text`**,
all five in `.rdata` — a **third distinct mechanism** for an empty `.text` magic scan, alongside
`.sab`'s memory-operand compare and the containers whose magic is never read.

## The other four

| sheet | result |
|---|---|
| **`sloc`** | **14/14 corpus figures exact** — 436 files, 52 units, **424** directory entries, **430** `NPS2`, stride 32 and last-ends-at-EOF 52/52, `recordEnd ≤ first TIM2` 52/52. `FUN_00379870` reproduces instruction for instruction. The dead-branch correction confirmed: `0x00379891` tests `'1'`, all 430 tags are `NPS2`, so `0x00379897…0x003798AC` is unreachable. |
| **`licd`** | **13/13 exact**, including the distinctive one: `ch` = `in`, `cn` = `kr`, and node 360 **relocated** — `board_1` holds it at cell **230** vs **114**, `board_10` at **249** vs **207**, filled count unchanged. `0x238 = 71*8`, `0x0022A159 call 0x2df9a0`, sole caller, `board_1.bin` string — all exact. |
| **`prefetch`** | All 7 cited addresses exact. The headline is **positive evidence**: the `##` token is passed to the deallocator at `0x001DA194`, not skipped. Corpus **9,351 entries / 283,340,853 bytes** — exact to the digit — and `Total_data_Size` **0 occurrences**. |
| **`ah`** | All cited addresses exact, and the two central claims confirmed **by counting**: `FUN_0019E7B0` decodes to **135 instructions**, matching the sheet, and enumerating every immediate across all 135 finds **zero** comparisons against `0x23`. Both parsers `call 0x18a330` with the format at **`0x008F4438`** — *the same address*, so "same scanner, different grammar" is exact, not analogous. |

**One addition, checked against the sheet first:** `licd`'s node space. The sheet establishes
contiguity *"across all 13 boards"*. Separately measured, **the 12 job boards use only 347 of the
361 ids and are not contiguous**; `license_board.bin` uses `0 … 299` and supplies 14 ids no job board
has. **The full run is a property of the union.** That bears on `PROPOSED-repos-c7-13` and on the
361-against-360 hole: the two board families index overlapping but distinct subsets, so a binding to
`license_data.bin` has to explain both.

---

## THE AUDITOR'S ERROR RATE, ROUND 2: STILL THE MAIN FINDING

| disagreement | cause | whose |
|---|---|---|
| `sloc` 381 files / 45 units | truncated block-0 magic test, and filtered to `.bin` | **mine** |
| `sloc` 178,928 directory entries | put `recordCount` at `+0x0A`; §2.1 says the `u32` at `+0x10` | **mine** |
| `sloc` 336 `NPS2` | followed from the wrong record count | **mine** |
| `licd` filled 128…300 | counted 13 boards where the sentence says *twelve* | **mine** |

**Four disagreements this round, four mine, zero defects in the sheets.** Combined with round 3
that is **seven of nine**.

> **The `sloc` case is the sharpest yet.** My first pass reported the sheet's record count wrong by a
> factor of **422**. A sheet does not miss its own record count by 422× — **the size of a
> disagreement is evidence about which side is broken**, and I should have treated a four-figure
> discrepancy as disqualifying my parser before I ran the next check.

**Two near-misses of a different kind, and they are the ones worth carrying forward.** Twice I
drafted an "addition the sheet lacks" that the sheet already contained — the `0x01EFF3B0` version
global in `efx` (stated four times) and the 430/430 `NPS2` measurement in `sloc` (stated in §3).
Both caught by re-reading before publishing.

> **An auditor's contribution must be grepped against the document before it is claimed.** It is the
> same failure as reading a mention for a declaration, one rung down: *the document already said it,
> and I did not look.* Recorded in both sheets at the point where I nearly made the claim.

## COVERAGE

| gate | result |
|---|---|
| `check_links.py` | 262 files, **10,040 links, 0 broken** |
| `check_layouts.py` | 44 fences, 25 documents, **0 errors** |
| `check_source_hygiene.py` | clean on every file touched |
| `check_assets.py` | 16 / 48 |
| `audit_coverage` | **9 documents moved `passes: 0` → `1` across rounds 3 and 4**, each with a `last_pass_state` naming the program state, the method and what was left unaudited |

**Every pass names what it did not do.** `efx`: first 8 bytes only, payload unmeasured. `sloc`: the
`TIM2` and `LCMPOS1` bodies. `licd`: `license_data.bin`'s records. `prefetch`: the JSON side.
`ah`: which callers reach each builder. **A pass that does not say what it left alone is not a pass.**


---
---

# ROUND 3 — the auditor row (below)

## STATUS — 2026-09-05 (round 3: auditor row)

**Auditor row complete.** Two free units, then four independent audit passes. **All four sheets went
from `passes: 0` to `passes: 1` with a named program state.** Two defects found and corrected, both
in instruction anchors; **no corpus figure in any of the four sheets was wrong.**

**My own instrument was the error three times out of five disagreements** — recorded below, because
that ratio is the useful part of this round.

---

## THE TWO FREE UNITS — `formats_explained` 10 / 48 → 12 / 48

| unit | what was missing | now |
|---|---|---|
| `ebp` | `ebp2-container.md` explained the format at tier 1 and never declared it — **10,045 files scoring nothing** | `archive_formats: ["ebp"]`, `[x] ebp explained` |
| `phyre` | `external` is *refused without a note*, so **35,984 files (40 % of the archive by count, 72 % by size)** scored nothing | declared on the Phyre schema-join sheet with the note `ASSET-FORMATS.md` §5 requires |

The `.phyre` note states the disposition **and** the obligation it carries: the container is generic
middleware documented elsewhere, **but what this build does with it is not deferred** — that is the
schema-join sheet's own subject, with 22 classes still unresolved. A bare "external" would have been
the cheap disposition the rule exists to prevent.

---

## FOUR AUDIT PASSES

**Method, common to all four.** Corpus re-parsed from `FFXII_TZA.vbf` with a **fresh reader**, never
by importing the author's census script or reading its frozen TSV — *an audit that reuses the
author's instrument tests transcription, not parsing.* Every cited instruction re-decoded with
capstone against `functions.tsv` bounds. Program state GN160 (`gzf fa0db293…`) throughout.

### 1. `pkfl-package-container.md` — PASS, no defects

10,314 packages re-parsed. **Sixteen claims, sixteen exact matches**: magic 10,314/10,314; per-extension
counts 4,392/2,304/1,809/1,809; `slotCount` 16/64 never mixed; 74,340 present offsets all `0x10`-aligned
and all inside the file; the even/odd partner invariant 10,314/10,314; 2,349 aliasing files; 2,403
duplicate groups with 2,385 all-odd and 2,259 in-directory; the `alc_a0100.snd` worked example
byte-for-byte; 27 empty packages naming the same three stems.

**Two apparent discrepancies, both mine:**

- *"4,833 ascending" came out as 4,860.* My test was `present == sorted(present)`, and **the 27 empty
  packages have `present == []`, which is vacuously sorted.** `4,860 − 27 = 4,833`. **An empty set
  satisfies a universal claim** — the sheet excluded them correctly.
- *"2,268 files with smallest offset `0x40`" came out as 2,286.* The sheet's sentence scopes itself
  to the 16-slot directory; 18 of mine were 64-slot files. **Scoped as written, 2,268 is exact.**

### 2. `frp-object-container.md` — PASS, **1 defect corrected**

Corpus 4,230/4,230 on every row (magic, name==stem, `contentLength` ≤ size, four zero words, and the
`.ca` variant split 1,969/1,195 with `.cm` all variant 0 — `variant` cuts across the extension, as
§6 says). The whole `FRP_FindEntry` contract reproduces instruction by instruction, and the
variant-dependent table base is confirmed **from the arithmetic**: `lea ecx,[rdi+0x40]` pairs with
`lea rsi,[rbx+0x10]`, `lea ecx,[rdi+0x30]` with `lea rsi,[rbx+0xc]`. The `+0x08` `Inert` row holds —
the only `+0x08` access in the function is `[rsp+8]`, a stack spill.

> **DEFECT: ten of eleven cited `@FRP` addresses were not instruction boundaries.** They pointed 1–3
> bytes into an instruction, at the `40 46 52 50` bytes rather than at the instruction consuming
> them — `mov edx, imm32` puts the immediate one byte in, `cmp dword ptr [r9], imm32` three.
> **The finding was right and every anchor was unusable.** Corrected in §3 with the old values kept
> visible. **The one address that was right is the one read off a disassembly**; the ten wrong ones
> came from a byte scan for the constant. *Same instrument and same failure mode as the
> `0x8000000B` scan in the EBP container sheet — the difference there was that the operand test was
> run afterwards.*

### 3. `sab-sound-bank-container.md` — PASS, **1 defect corrected**

**Fourteen corpus figures, fourteen exact matches**, including the ones most likely to drift: `_flag`
1 in 4,097 / 0 in 512 / 1 in all `.mab`; `_param` 350 distinct in `.sab` and `0x2710` in every
`.mab`; `nameLength` only ever 5 or 7; `totalSize` == file length 4,725/4,725; 18,436 + 348 chunk
records with `0x00100000` in all 18,784; the `se` 4,345 / `shout` 264 split; 838 MB / 1,312 MB.

`Sab_IsSabf` is **byte-for-byte as printed**, and its `rip` target resolves to `0x00D115B4` holding
literally `sabf`. `Mab_IsMabf` is the same shape against `0x01CB6FB8` holding `mabf`. **The sheet's
headline instrument claim — that a `.text` byte scan cannot see this validation — survives its own
strongest test.** `Sab_FindChunk`'s directory arithmetic is five consecutive instructions exactly as
cited, so *"a corpus reading alone would conclude the directory is at `+0x20` and be wrong about the
format"* is demonstrated, not asserted.

> **DEFECT: `+0x06 dirDelta` was anchored at `0x007CF6C1`, which is `jb` — the version-gate branch.**
> The read of `[r9+6]` is at **`0x007CF6BC`**, before the branch, so both arms use it. Corrected.

**One apparent inconsistency that is not one, recorded so nobody "fixes" it:** §2 cites `0x007D05A9`
and §3 cites `0x007D05A5` for the offset consumer. **Both are right** — `0x007D05A5` reads
`chunk->offset`, `0x007D05A9` adds `container->base`. Two halves of one expression.

### 4. `area-nmb-index.md` — PASS, no defects

**Eleven claims, eleven exact matches**: 332 entries / 166 stems; both locale copies byte-identical
166/166 (**re-hashed from decompressed bytes, not inherited**); version `0x0064` in 166/166; the
offset table `count + 1` with the last equal to file size, 166/166; strictly ascending 166/166;
`size = 8 + 7*count` in **166/166 across 19 distinct sizes**; 1,146 entries all exactly 3 bytes; tag
`0x12` ×1,146; code `0xBA` ×1,120 / `0xBB` ×26; `_zero` ×1,146.

Both path functions reproduce instruction for instruction, and **two safety claims confirmed**:
neither `kind` nor `index` is bounded in `ResourcePath_Get`'s 22 bytes and both are *sign*-extended;
and `ResourcePath_Copy` writes its terminator at `dst[copied]` **after** the length test, so
**a caller sizing `dst` to exactly `maxLen` overflows by one byte.**

---

## THE RATIO IS THE FINDING: THREE OF FIVE DISAGREEMENTS WERE THE AUDITOR'S

| disagreement | cause | whose error |
|---|---|---|
| PKFL 4,860 vs 4,833 | empty list is vacuously `sorted()` | **mine** |
| PKFL 2,286 vs 2,268 | did not scope to 16-slot files as the sentence does | **mine** |
| `.nmb` 4/166 "last offset == file size" | read the offset table as `u16`; it is `u32`, stated in plain text under the fence | **mine** |
| `@FRP` ten anchors | byte scan returns the immediate's address, not the instruction's | author's |
| `.sab` `dirDelta` anchor | cited the branch, not the read | author's |

> **A re-parse that disagrees is evidence about the parser until the layout has been read, not
> skimmed.** The `.nmb` case is the clearest: my `u16` reading produced *negative* entry lengths and
> a 4-of-166 hit rate — a result that looked exactly like a broken format claim, from a sheet whose
> §2 says `u32` one line under the fence.
>
> **And the two real defects are the same defect**, in two sheets by two authors: *an address
> obtained from a byte scan is the constant's address, not the instruction's.* That is the third
> sighting of that mechanism this week — the `0x8000000B` operand test in the EBP container sheet
> was the first. **A cited address that lands mid-instruction is worse than a missing one: it looks
> valid, no checker sees it, and a reader who jumps there doubts the sheet rather than the anchor.**
> **Proposed `COVERAGE.md` line:** *an instruction anchor must come from a decode, never from a byte
> scan for the operand — the scan returns the operand's position, which is 1–3 bytes past the
> instruction that owns it.*

## COVERAGE

| gate | result |
|---|---|
| `check_assets.py` | **16 / 48**, up from 10/48 at the start of my row (`ebp` + `phyre` mine) |
| `check_ebp.py` | 14 / 14 |
| `check_formats.py` | 9 / 63 |
| `check_layouts.py` | 36 fences, 21 documents, **0 errors** |
| `check_links.py` | 258 files, **10,023 links, 0 broken** |
| `check_source_hygiene.py` | clean on every file touched |
| `audit_coverage` | **4 documents moved `passes: 0` → `passes: 1`**, each with a `last_pass_state` naming the program state and the method |

**Every `last_pass_state` says what was re-derived and what was not.** All four record explicitly
that the corpus half was independently confirmed and name what was left unaudited — PKFL's §3 loader
contract, `@FRP`'s entry payloads, `.sab`'s chunk-tag meanings, `.nmb`'s five unresolved call sites.
**A pass that does not say what it left alone is not a pass.**


---
---

# ROUND 2 — the .ard reader (below)

## STATUS — 2026-09-04 (round 2: `.ard` reader body)

**EBP lane closed and reported 2026-09-03** (below, unconsumed). **Resumed on the `.ard` reader-body
row.** Same GN160 project, `Tools/work/repos-1e_proj`, ledger unchanged.

**Delivered: `St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`** — tier 1, gates clean.
It answers all three questions the board set me, and it **promotes the community reading of `.ard`
from tier 9 to a named reader.**

I did **not** redo the census or the path table, as instructed.

---

## THE `.ard` READER — all three board questions answered

### 1. Who walks the table

**Nothing references the table directly, and the first two instruments both said so wrongly.**
`DumpDataXrefs.java` on seven addresses in the table returned `DUMP_DATA_XREFS_NONE` — **zero refs**
— and my own linear `.text` sweep agreed. **Both were false negatives.** The table is reached as
`pathTables[namespace][index]`, so no instruction names a record.

Re-scanning **per function using `functions.tsv` boundaries** (1,787,590 instructions decoded) found
it. *A linear disassembly of `.text` desynchronises after the first function and silently reports
zero* — worth a `COVERAGE.md` line; it is a new instance of the displacement blind spot.

The resolver is 22 bytes:

```asm
002DF980  movsxd rax, ecx              ; namespace
002DF983  lea    r8, [rip + 0x1e7f676] ; -> 0x0215F000, a table OF path tables
002DF98A  movsxd rcx, edx              ; index
002DF98D  mov    rax, [r8 + rax*8]     ; table = pathTables[namespace]
002DF991  mov    rax, [rax + rcx*8]    ; return table[index]  (char*)
```

**`.ard` is resource namespace 21** (`0x0215F0A8`, `0xA8/8 = 21`), written per locale by
`FUN_002DF9A0` at `002DFA9E` / `002DFE66`. The walker is:

```
MapRef_GetAreaArdFieldResourceIndex   0x00264ED0   field id -> u16 area index
  -> AreaArd_RefreshForMapRefField    0x003EA6E0
    -> AreaArd_LoadOrUnloadFieldResource 0x003EA820   Resource_GetSize/BeginRead(21, idx*2)
      -> AreaArd_BindLoadedRootAndBattleSections 0x003EA710
```

**The index is `areaIndex * 2`** (`003EA868`, `003EA97F`), and the `.fpk` sibling is `*2 + 1`
(`003EA83E`). **That is the whole explanation of the "16-byte record"**: the table is a flat
`char*[]` at 8-byte stride and the record is the corpus view of a doubled index. Both descriptions
are right; the engine's is the doubled index.

**`.ard` uses the same `(namespace, index)` resource path as `.ebp`** — `FUN_0032E400` /
`FUN_0032E620`, the pair I documented in the EBP container sheet. One resource-addressing scheme,
two formats.

### 2. What binds the four `st2e` tables

`AreaArd_BindLoadedRootAndBattleSections` (`0x003EA710`) reads **six** header fields and hands five
of them to `BattleData_SetAreaArdSectionCategory` (`0x0023A160`), which is a five-way branch into
**five authored-data registry slots**:

| cat | header | binder site | registry slot | bound via |
|---:|---|---|---|---|
| 0 | `+0x10` (always `0x30`) | `003EA76A` | **`0x02EBF150`** | `AreaData_BindAndRebaseSectionDescriptor` |
| 1 | `+0x14` (`varB`) | `003EA777` | **`0x02EBF168`** | `FUN_003846F0` — *different binder* |
| 2 | `+0x18` (`varC`) | `003EA784` | **`0x02EBF120`** | `AreaData_BindAndRebaseSectionDescriptor` |
| 3 | `+0x24` (`varD`) | `003EA7D1` | **`0x02EBF148`** | `AreaData_BindAndRebaseSectionDescriptor` |
| 4 | `+0x28` (`varE`) | `003EA7FA` | **`0x02EBF140`** | `AreaData_BindAndRebaseSectionDescriptor` |
| — | `+0x2C` (`varF`) | `003EA7A8` | *none* | `FUN_003DCF00` |

> **Read the branch chain, not the decompiled `if` order.** `0023A160`–`0023A176` is a
> `test` / `sub ecx,1` ladder whose case order does **not** match the order Ghidra prints the blocks
> in. Taking the printed order gives a different and wrong mapping. `lea` sites: `0023A1B7` (cat 0),
> `0023A1A8` (1), `0023A196` (2), `0023A187` (3), `0023A178` (4).

**This closes a lead in `authored-data-table-registry.md`.** That document says (line ~140) the
loader *"plausibly binds against four slots (`0x02EBF120`, `0x02EBF140`, `0x02EBF148`,
`0x02EBF150`)"*. It is **five**, the fifth is **`0x02EBF168`**, and each is now pinned to a specific
header field and `lea` site. **Coordinator: that is a merge into an existing document, not a new
claim of mine — I did not edit it, and I declared no `registry_slots` because all five already have
owners.**

### 3. What `varD` / `varE` / `varF` index

They are **section offsets 3, 4 and 5** of the header, and they are *not* alike:

- **`varD` (`+0x24`) → battle category 3 → `0x02EBF148`**
- **`varE` (`+0x28`) → battle category 4 → `0x02EBF140`**
- **`varF` (`+0x2C`) → not a battle slot at all** — it goes to `FUN_003DCF00`.

The census's "`varD`/`varE`/`varF` ascend together, spaced 32" was a good lead and **half right**:
they are consecutive directory slots, but the third has a different consumer.

**Cross-check that settles part of `BZ-2`:** EBP `section_019` carries this same header, and its
binder `FUN_003EAA00` reads **only `+0x2C`** (`003EAA32`, `003EAA3F`) and hands it to
`FUN_003DCF10` — the sibling of `.ard`'s `FUN_003DCF00`. **So `section_019` is not a degenerate
`.ard`; it is the `varF` half of one.** That is a mechanism match, not a magic match.

### The community reading is now promoted — and only this far

The five slots' readers are named: `BattleUnit_ApplyUnitDefinition` (`0023A570`),
`BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`),
`BattleStats_InitializeDefinitionRecord` (`0023AC80`), `BattleEncodedId_IsValidForClass`
(`00322C50`), `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit` (`00239040`),
`BattleUnit_ExecuteDirectStateCommandOrder` (`002FDDA0`).

**`.ard` supplies per-area battle unit definitions and the gambit order-set directory.** The README
held the community's "per-area enemy status and attributes" at tier 9 *until a reader is named*. A
reader is named, so the destination is established — **but the record layouts are not**, and the
sheet says so. Naming a consumer is much weaker than decoding a table and I made only the weaker
claim.

### What the loader rejects, clamps and ignores

- **`FF12AR03` is never validated** — no `[rbp+0]` reference in the binder, nothing `.ard`-aware on
  the read path. Third container in a row (after `EBP2` and the EBP section markers), but here with
  a *mechanical reason*: the engine holds 430 literal paths and asks by index, so a magic check
  would guard a substitution the design makes impossible.
- **Nothing is bounds-checked.** All six fields are `ImageAddress_ResolveRuntimePointer`
  (`0x0020E600`) then `add reg, rbp`, with no comparison against file length.
- **The only rejection is the file size.** `Resource_GetSize < 1` → unbind all five categories,
  `g_nLoadedAreaArdFieldIndex = -1`. **Both branches unbind first**, so an area never inherits the
  previous area's battle data even transiently. That is the loader's one safety property and it is
  structural, not validated.
- **Loading rewrites the file image in place.** `AreaData_BindAndRebaseSectionDescriptor`
  (`0x003845F0`) rebases descriptor fields `+0x0C` (`00384600`→`0038460E`), `+0x10`
  (`00384614`→`0038461E`), `+0x18` (`00384625`→`0038462F`), `+0x1C` (`00384636`→`00384640`), and
  re-encodes `+0x14` (`00384647`) through `RuntimePointer_EncodeImageAddress` (`0x0020E620`).
  **Anyone diffing runtime memory against the on-disk file will see these differ — that is the
  loader, not corruption.**

### A new `Inert` finding: `varA` at `+0x0C`

**134 distinct values across 166 areas, in-file range in 140 of them, zero in 26 — and no reader.**
Not read by the `.ard` binder, not read by the `section_019` binder, and absent from a
per-function RIP scan of all 38,161 functions. **Authored data the shipped engine ignores** — the
same shape as `section_017` (`BW-1`) and `.fpk` (7,520 paths, 0 files).

Also corpus-checked: `+0x24`, `+0x28`, `+0x2C` are **null-guarded in code and non-zero in all 166
files**, so those guards are real code and dead against shipped data — the same pattern as the EBP
`slotCount` bound.

### A cross-session disagreement, settled with evidence — closes `PROPOSED-repos-4b-9`

`repos-4b` could not reproduce "namespace 21 is `.ard`" and asked for it to be settled rather than
asserted. **Their inability was itself the informative part**, and their narrower surviving claim is
correct: **both arrays installable at `0x0215F0A8` begin with 24 NULL qwords**, so no slot's *head*
holds `.ard` paths. A head-only view sees nothing, and a walk that stops at the first NULL measures
the distance to a hole rather than a length.

Walking both arrays in full:

| | `0x01E0CFA0` (`002DFE66`) | `0x01EDC280` (`002DFA9E`) |
|---|---:|---:|
| first non-NULL index | **24** | **24** |
| `.ard` at even indices | **215** | **215** |
| `.fpk` at odd indices | **215** | **215** |
| `.ard` at an odd index / `.fpk` at an even one | **0 / 0** | **0 / 0** |

**All 430 `.ard` strings in the image are reachable at even indices from those two bases; none is
unreachable.** And they asked the right decisive question — *could a write to `0x0215F0A8` have been
missed?* **No:** decoding every RIP-relative operand in all 38,161 functions finds it touched
**exactly twice**, both `mov` writes in `FUN_002DF9A0`. That method does not pair a `lea` with a
`mov`, so a value arriving in a register by another route would still have been seen — which is
precisely the gap they flagged in their own scan.

**One limit I have written into the sheet rather than glossed:** the arrays are *not* `{ard, fpk}`
pairs end to end. They also carry `bin`, `tm2`, `mrp`, `as7`, `ico`, `efx`, `cm`, `sys` and `mg`
paths, at **both** parities. The proven claim is the narrow one.

### A hazard worth generalising: an array's BASE is not where its first pointer is

`repos-3f` ran the inverse of my case and it strengthens my result rather than qualifying it. The
ns-21 arrays are **sparse — base and first non-NULL entry are 24 qwords apart** — so taking the
first `.ard` pointer as the base would shift every index by 12 areas, and **every downstream number
would remain self-consistent.** No gate detects that.

Their kind-26 arrays, recovered the same way from the initialiser (`002DFAE4` → `0x01E4DC30`,
`002DFE58` → `0x01EAE0D0`), are **dense from index 0**, first NULL at 321. **Sparse and dense are
indistinguishable from the data alone** — only the initialiser's store separates them, and both my
bases and theirs came from there.

Their own note is the sharpest part and I am passing it on verbatim in substance: *they got the
right base by accident of technique, not judgement* — reading it from the store because that was the
cheapest way to identify the slot, not because they had considered that the first pointer might not
be the base. **The rule for `COVERAGE.md`: recover a path-table base from the initialiser that
writes it, never from where its first pointer is found.** Added as a falsification row in my §6.

### CROSS-CONFIRMATION of `repos-3f`'s three `COVERAGE.md` drafts — with one of my halves CORRECTED

They asked the coordinator to treat these as cross-confirmed rather than one session's anecdote.
**Confirming from this side means stating my half precisely, so here it is — and checking it changed
one of the three.**

**Entry 1 — the base rule. CONFIRMED, unchanged.** My half: the ns-21 arrays are sparse, base and
first non-NULL entry **24 qwords apart**, so taking the first `.ard` pointer as the base shifts every
index by 12 areas with all downstream arithmetic still self-consistent. Their half: kind 26 is dense
from index 0, first NULL at 321. Bases in both cases came from the initialiser's store
(`002DFA9E`/`002DFE66` mine, `002DFAE4`/`002DFE58` theirs). **The rule holds and the two cases are
what make it checkable.**

**Entry 2 — "pointers into a table's range are not members of the table". MY HALF WAS WRONG AS I
STATED IT, and the corrected version is a sharper rule.** I told them I had 256 qwords pointing into
`0x01E0D000–0x01EDD800` that "have nothing to do with the path table". Re-measured before
confirming:

| | |
|---|---:|
| qwords in `.rdata` whose value lands in the span | 256 |
| **distinct targets that ARE path-table entry slots** | **19** |
| distinct targets that are not | 166 |
| slots inside the span holding `.ard`/`.fpk` string pointers | **7,241** |

So **19 of them do land on real table slots** — "nothing to do with the table" was false. And the
second number is the bigger error: **7,241 slots, against the 430 `.ard` entries I was bounding.**

> **The span was never the table.** I derived `0x01E0D000–0x01EDD800` from the *first and last*
> `.ard` pointer site, and a span bounded by the first and last member of a structure contains
> **everything in between** — here several other path arrays, `.fpk` paths dominating. The correct
> rule is stronger than the one I gave them: **a range bounded by a structure's extreme members is
> not that structure, and inbound references to a range say nothing about which structure they
> reach.** My original dismissal reached the right decision (drop them) for a reason that was false
> for 19 cases.

**Entry 3 — the paired trust failure. CONFIRMED, and this correction is a third instance of it.** I
was one message away from cross-confirming a number I had stated loosely and never measured,
*because it agreed with a peer's independent sighting of the same shape*. That is precisely the
failure the entry describes. **Checking my own half before confirming it is what caught it** — and
"cross-confirmed" is worth nothing if the second session confirms from memory rather than from a
re-run.

### LATE ADDITION to the closed EBP container sheet: the namespace, and a stride rule that unifies three lanes

`repos-3f` found that `FUN_00332250` — **which is on my EBP chain** — whitelists its namespace
argument (`cmp ebx,8` / `cmp ebx,0x25` / `cmp ebx,5` at `00332285`/`0033228A`/`0033228F`).
Reproduced from the bytes, and it let me close a gap my container sheet had left: **I never named
the EBP resource namespace.** `ActorResource_BeginManagerResourceSetLoad` picks namespace *and index
scale* from the manager index in one branch, `0x0032FD19`–`0x0032FD44`:

| manager index | namespace | index | at |
|---:|---:|---|---|
| `<= 0` | **5** | `id * 3` | `0032FD3F` / `0032FD44` |
| `1 – 3` | **8** | `id * 4` | `0032FD30` / `0032FD35` |
| `4` | **1** | `id + 0x6B` | `0032FD27` / `0032FD2A` |

Two of the three are exactly the whitelisted values, so **`FUN_00332250` is a script-container
helper, not a general one** — which gives `repos-3f` a *mechanism* reason that kind 26 is excluded
rather than only a control-flow one.

**The rule — CORRECTED by `repos-3f` before it left my inbox, and the correction is the point.**

I first wrote *"the index is scaled, and the scale is a property of the namespace"*. **That is false
for one of the three branches I had just cited.** `0032FD2A lea ebp, [r15 + 0x6b]` does not
multiply — it only adds. The right statement is:

> **The index is an affine function of the id — multiplier, addend, or both — chosen per namespace
> by the requesting code.**

| | namespace | index expression | instruction |
|---|---:|---|---|
| `.ard` | 21 | `id * 2` (+1 for the `.fpk` sibling) | `003EA868` / `003EA97F` |
| `.ebp` | 5 | `id * 3` | `0032FD44 lea ebp,[r15+r15*2]` |
| `.ebp` | 8 | `id * 4` | `0032FD35 lea ebp,[r15*4]` |
| `.ebp` | 1 | **`id + 0x6B`** | `0032FD2A lea ebp,[r15+0x6b]` |

**The addend is the dangerous half and it ships.** A multiplier leaves a visible interleave — two
alternating extensions is exactly how the `.ard`/`.fpk` parity gave itself away — but **an addend
leaves no trace at all: a flat array is byte-identical under `id + 0` and `id + 0x6B`.**

**And I violated my own rule in the same table.** My first version had a row *`.nmb` | 26 | stride 1
| flat, no record structure*. **No request for kind 26 resolves**, so its index expression is
unknown; flat is *consistent with* stride 1, not evidence of it. That row is removed. `repos-3f`
caught it and has narrowed their own sheet the same way — their §3 no longer claims a `.nmb` is
addressed by `(26, areaIndex)`, and their area indices are now explicitly **positions in the array**
rather than proven arguments to `ResourcePath_Get`.

**The shared root cause, stated once for `COVERAGE.md`:** *treating the array as if it were the
interface.* It is not — the interface is in the caller. This is the same defect as the README's
"table span" and as my own inbound-pointer span: **structure inferred from data that is consistent
with several structures.**

**Provenance, because it is more useful than attribution.** `repos-3f` phrased that line, but only
after checking whether their own array claims were interface claims — which they did **because I had
retracted first**. Neither of us would have looked otherwise. *What made anyone look* is the part a
future reader can reuse; who said it is not.

### NAMESPACE 37 CLOSED — an override, and it completes the whitelist

Both peers left this open. It sits inside a function on my own chain, so I took it.
`ActorResource_BeginManagerResourceSetLoad`, `0x0032FDB9`–`0x0032FDF1`:

```asm
0032FDB9  lea  eax, [rdi - 1]  /  cmp eax, 2  /  ja 0x32fdf1   ; only managers 1..3
0032FDC1  lea  eax, [rbp + 3]                                  ; ONE index, both probes
0032FDC4  mov  ecx, esi   ; call 0x32e400                       ; GetSize(primary, idx)
0032FDD9  mov  r12d, eax                                        ;   kept only for the skip path
0032FDD4  mov  ecx, 0x25  ; call 0x32e400                       ; GetSize(37, SAME idx)
0032FDE8  mov  [rsp + 0xb0], eax                                ; the ns-37 answer WINS
0032FDF1  mov  [rsp + 0xb0], r12d                               ; skip path keeps the primary
```

**Namespace 37's table is fully populated, and its layout is namespace 8's exactly.** Extent taken
as the distance to the next base in address order over all **83** bases recovered from
`FUN_002DF9A0`'s own stores — 2,964 slots per ns-37 array, 642 per ns-21 array. Within those bounds:

| ns | base | entries | first idx | `index mod 4` |
|---:|---|---:|---:|---|
| 37 | `0x01EA4D00` (ch) | **1,316** | 120 | `.ebp` / `.mot` / `.snd` / `.vpcjp` — **329 each, no exceptions** |
| 37 | `0x01ECBCF0` (in) | **1,316** | 120 | identical |
| 21 | `0x01E0CFA0` (ch) | 430 | 24 | `.ard` 215 even / `.fpk` 215 odd |
| 21 | `0x01EDC280` (in) | 430 | 24 | identical |

**329 ids × 4 assets — exactly namespace 8's `index = id*4` rule.** An override must have the
overridden table's shape, and it does.

> **THIRD SIGHTING OF THE SPARSE-HEAD ERROR — and then a fourth error of mine, in the opposite
> direction, on the same array in the same hour.**
>
> `repos-3f` reported both ns-37 arrays as **empty**; their enumerator stopped after three
> consecutive NULLs and the first path is at index 120. **But my counts were wrong too, and worse:**
> I reported **2,168 / 1,972** entries and a *"mixed"* `ch` array carrying `ca`/`bin`/`tm2`. **Both
> were pure overrun** — a fixed 4,000-slot window against a 2,964-slot extent, reading the
> *neighbouring* array as if it were this one. Bounded properly: **1,316, clean in both trees**,
> matching their independently derived figure exactly.
>
> **One session read too little, the other read too far.** That is the *span-is-not-a-structure*
> error in its third and fourth costumes, after the README's "table span" and my inbound-pointer
> range. **Where an array ends is no more observable from the array than where it starts.**
>
> **It reached my other sheet too, harmlessly.** The `.ard` counts were taken the same unbounded way
> (900-slot window, 642-slot extent). Re-measured inside the bound they are unchanged — 215/215/430
> — because the neighbouring array happens to carry no `.ard` or `.fpk`. **Being right there was
> luck, not method**, and the sheet now says so rather than leaving correct numbers standing on a
> method I have disowned elsewhere.
>
> **The extent rule is only as good as the base set is complete** — 83 bases here, 94 theirs, and
> completeness is unproven, so these are upper bounds. **The parity partition and "not empty" are
> robust to the extent rule; the totals are robust only because the data stops well short of either
> bound.**
>
> **Two distinct `COVERAGE.md` lines, not one:** base recovery is *where an array starts*; this is
> *where it stops*. Same cause — the cheap version of the question is wrong.

### The six unaccounted path-table bases are EXPLAINED — a discriminator for both sets

`repos-3f` reported 94 bases of which **6 resolve to nothing**, and could not cheaply tell whether
those were genuinely empty or **spurious extractions from their own lea/store pairing**. I ran the
same audit on my extractor, which uses the same pairing method, and found **the identical residue:
83 unique bases, 40 populated kind slots, 6 that resolve to no path.**

**They are not artefacts.** `.data` is file-backed only to RVA `0x01E5E400` (VA `0x01F7E400`);
above that it is uninitialized and zero at load. All six — `0x0215EFF8`, `0x0215F148`,
`0x0215F150`, `0x0215F158`, `0x0215F160`, `0x0215F168` — lie in that tail. They are **real stores
pointing at zero-initialized memory**: empty tables by construction.

> **The discriminator, which is the reusable part:** a recovered base **above `0x01F7E400`** cannot
> hold file-backed path strings, so *no entries* there means **empty by construction**, not
> **mis-paired `lea`**. A base **below** it with no entries is the suspicious case. **77 of my 83
> are file-backed and every one resolves — zero suspicious.**

**And the selector block itself is in that tail.** `0x0215F000` is not file-backed either, which is
**why `FUN_002DF9A0` exists at all**: it populates a zero-initialized pointer array at runtime. The
whole structure is a BSS table-of-tables, filled by an initialiser, indexed by kind.

**The base MUST come from the initialiser, and the reason is stronger than "be careful".** The
selector array is in uninitialized `.data`, so **the image contains no address for it at all**.
`FUN_002DF9A0` is not a convenience that happens to record the bases — it is **the only thing that
ever puts an address in that array.** There is no other source to prefer or cross-check against,
which makes recovering a base from the first pointer or the densest run not merely risky but
**unfounded**. That is the justification the `COVERAGE.md` base-recovery entry should carry.
*(`repos-3f`'s sharpening of my observation.)*

**Cross-checked: their 94 and my 83 both come out clean.** They applied the discriminator to their
own set — **88 file-backed, all resolving, and the same six above the boundary, the identical six
addresses.** So the correct statement is *both sets clean, theirs more complete*, reached by
measurement on both sides rather than by either of us conceding.

**Tooling defect FIXED, not just noted.** My VA→file-offset helper range-checked against
`max(virtualSize, rawSize)`, so for an uninitialized address it returned an offset **past EOF**
instead of `None`. It threw this time — but `rd()` uses slicing, which does **not** throw: it
returns short or empty bytes, so the helper failed **toward "nothing found"**, the dangerous
direction for an absence claim. Patched to return `None` when `rva - sectionRVA >= rawSize`, and
**all four array counts re-verified with the fixed helper reproduce exactly** (1,316 / 1,316 /
430 / 430, same first indices, same extension breakdowns) — so no measurement this session was
affected. **Uninitialized `.data` is where a VA→offset helper fails, and it fails quietly.**

### FOR THE COORDINATOR: `AUDIT-LOG.md` line 14984 is corrupted AND passes hygiene

`repos-3f` found a stray **BEL** in my inbox at line 1026 — `..\..\katano<BEL>telload.c`, where the
`\a` of `atelload.c` had been eaten as an escape on the way in through a non-raw Python string.
**Fixed here.** My three sheets and `ASSIGNMENTS.md` were clean; only the inbox was hit.

**But it had already propagated into a shared file, in a worse form.**

| | |
|---|---|
| file | **`_index/AUDIT-LOG.md`, line 14984** (coordinator's — not edited by me) |
| present | `` `..\..\katanotelload.c` `` |
| correct | `` `..\..\katano\atelload.c` `` |
| stray control bytes in that file | **0** |

> **It passes `check_source_hygiene` and is still wrong.** The BEL was *stripped* rather than
> *repaired*, so the byte is gone and the `\a` went with it. **A hygiene-clean result does not mean
> the string is right** — the checker finds the visible stage of this defect, and the obvious repair
> converts it into the invisible stage.

**I made exactly that mistake on my own file thirty seconds earlier** — a blanket strip of the BEL byte
ran before my targeted fix and produced `katanotelload.c`, which I only caught by printing the
repaired text instead of trusting the checker's green. **The repair has to restore the character,
not delete the byte.**

**And then I did it a third time, in the sentence above this one.** Writing this very warning, I
put the escape for the BEL byte into a non-raw Python string in a heredoc — and emitted **a real BEL
into the paragraph explaining how BELs get emitted.** `check_source_hygiene` went from green to
`1 occurrence` on the commit that added the warning about it. Repaired by rewriting the line to name
the byte in words instead of writing any escape at all.

> **That is the actually useful finding here, and it is not about tidiness.** Three instances in one
> hour, and **prose describing the hazard is itself a vector for it** — the warning text has to
> contain the dangerous sequence to be legible, which is exactly when it gets interpreted. **The only
> repair that holds is to not write the escape**: name the byte, or use a raw string.

**Why it matters beyond tidiness, and it is this thread's own theme:** the string is a search key.
A `grep` for `katano\atelload.c` across the database **misses `AUDIT-LOG.md` entirely** — failing
toward *not found*, the same direction as the VA→offset helper and the array-head reads.
**Proposed `COVERAGE.md` line:** *a control byte inside a path or regex literal must be repaired to
the intended character, never deleted; deleting it silences the checker and leaves a search key that
matches nothing forever.*

### `.fpk` RECONCILED IN CLOSED FORM — and I removed it from one of my own claims

`repos-4b` settled the namespace-8 variant count without touching either extractor: **strings per
stem IS the variant multiplier**, because each region variant emits a full path for the same stem.
Verified independently from my own scan of the image:

| ext | strings | stems | ratio |
|---|---:|---:|---:|
| `.mot` / `.ebp` | 10,380 | 1,038 | **10.000** |
| `.snd` / `.vpc` | 3,290 | 329 | **10.000** |
| `.vpcjp` | 658 | 329 | **2.000** |
| `.ard` | 430 | 215 | **2.000** |
| `.fpk` | 7,520 | 924 | 8.139 — the mixed one |

**The mixed ratio resolves into two populations, and the account needs both our datasets:**
709 map stems × 10 (namespace 5, theirs) + **215 area stems × 2 (namespace 21, mine)** = **7,520**
strings over **924** stems. **Both totals match the measured figures exactly.** `.vpcjp` at 2.000 is
a fourth independent confirmation that namespace 37 has two arrays, which is what my walk found.

**My variant count of 8 for namespace 8 is the incomplete one — recorded as a limitation, not a
disagreement.** Three data points now run the same way: 83 bases against `repos-3f`'s 94, and 8
variants against a ratio that says 10. **My `lea`/`mov` pairing misses stores.** I have asserted no
per-namespace array count anywhere and will not.

> **Their method point is the transferable one:** a third extraction *of the same kind* could not
> adjudicate between two extractions of that kind. They measured the **consequence** of having N
> variants instead of the mechanism, and that is why it settles.

**It cost me a claim in a second place, which is the part worth recording.** I had listed `.fpk`'s
7,520 paths / 0 files alongside `section_017` and `trailerOff` as a **third instance** of *authored
capacity the shipped game never uses*. It is not an instance at all — **nothing chose to name 7,520
packages, a record width did.** So beyond rewriting §7 I went back to §5 and **downgraded my own
"third instance" to a second**, with a note saying `.fpk` is deliberately excluded and why.
**A list of instances is a claim about how common a pattern is**, and leaving a disproven member in
it inflates the pattern silently — the same shape as counting a mention as a declaration.

### Kind 21 IS confirmed by the second instrument — and I re-made my own error proving it

`repos-4b` scoped the strings/stems method correctly: **it adjudicates only where an extension
belongs to exactly one kind**, and they listed kinds 1, 2, 8, 9, 12 and **21** as resting on the
extraction alone. **Kind 21 can come off that list**, on two grounds this session already has:

1. **`.ard` is exclusive to kind 21.** Walking all 83 recovered bases **within their derived
   extents**, the only arrays containing an `.ard` string are `0x01E0CFA0` and `0x01EDC280` — both
   kind 21. So `.ard`'s ratio of **430 / 215 = 2.000** is unmixed and *does* decide.
2. **Exhaustive reachability, which is stronger than the ratio.** All **430 of 430** `.ard`
   strings in the image are reached from exactly those two bases, **none unreached** — so a third
   kind-21 array would have to re-point at strings already fully accounted for.

**FOURTH INSTANCE OF THE OVERRUN, and I made it while testing for it.** My first exclusivity check
used an unbounded 3,000-slot walk and reported `.ard` under **kinds 1, 2 and 30 as well** — three
false attributions, because those bases (`0x01ED7630` extent **34** slots, `0x01EDBFE0` extent
**84**, `0x01ED7740` extent 2,324) sit just below the kind-21 `in` array and my walk ran straight
into it. Re-run with extents: **kind 21 only.**

> **This happened minutes after I documented the hazard, in a check written to test that hazard.**
> The lesson is not that the rule was unknown — it is that **the unbounded walk is the natural way
> to write the loop**, and the bounded one has to be deliberate every single time. A rule in a
> document does not survive contact with the next quick check; only a bounded helper does.
> **`COVERAGE.md`: the walker itself should take the extent, so an unbounded walk is not
> expressible** — that is the only fix that has held for anything this round.

### The `COVERAGE.md` fix is IMPLEMENTED, not just proposed

I argued the only fix that holds is **making the unbounded walk inexpressible**, so I built it
rather than leaving it as a recommendation — the distinction is the whole point of the finding.
`Tools/work/repos-1e/pe.py` now carries:

- **`extents_from_bases(bases)`** — base → slot count, bounded by the next base in address order.
  The **last** base gets a hard cap and is therefore the one result a caller must treat as
  unbounded and unproven; the bound is only as tight as the base set is complete.
- **`walk_array(base, slots, want=None)`** — `slots` is **required and has no default**. An
  unbounded call raises. It also stops at the first slot with no file backing, so uninitialized
  `.data` cannot be read as content — the second failure this session, folded into the same helper.

**Regression against every figure this round published, through the fixed tool:**

| array | extent | entries | first idx | breakdown |
|---|---:|---:|---:|---|
| ns21 ch | 642 | 430 | 24 | `.ard` 215, `.fpk` 215 |
| ns21 in | 642 | 430 | 24 | `.ard` 215, `.fpk` 215 |
| ns37 ch | 2,964 | 1,316 | 120 | `.ebp`/`.mot`/`.snd`/`.vpcjp` 329 each |
| ns37 in | 2,964 | 1,316 | 120 | identical |

**All four reproduce exactly**, and `walk_array(base, None)` refuses. So the numbers in both my
sheets now rest on a tool that cannot commit the error they were nearly lost to.

> **Why this is the recommendation rather than "bound your walks".** Four instances across three
> sessions, the last written *to test the hazard* by someone who had documented it minutes earlier.
> `repos-4b` made the sharpest version of the point against themselves: their own bounded walker
> exists because they had already withdrawn a column to this error — **scar tissue, not principle**
> — and a fresh script of theirs tomorrow would default to unbounded like everyone else's.
> **A discipline that four experienced readers failed in one hour is a tooling defect.**

### A control that turned out to validate NOTHING — withdrawn on both sides

`repos-4b` offered that the extent rule **generates its own control**: sibling arrays get different
extents, and their counts held constant across them, so the counts belong to the data rather than
to the bound.

**I tested it on my arrays and it failed. They then tested it on theirs and it failed too.**

| array | derived extent | 200 | 400 | extent | ×1.5 | ×3 |
|---|---:|---:|---:|---:|---:|---:|
| ns21 ch | 642 | 34 | 218 | **430** | 622 | 1,375 |
| ns37 ch | 2,964 | 68 | 184 | **1,316** | 2,492 | 5,443 |

Still climbing at every bound; last populated index **641 of 642** and **2,963 of 2,964** — *zero*
headroom. Their own sweep found the same: **zero headroom in 23 of 24 arrays**, no plateau anywhere.
**The arrays are packed back-to-back**, so the last populated slot is always the slot before the
next base, and past the boundary a walk is simply counting the neighbour — **the overrun error
arriving disguised as a control.**

> **My first reading of this was too generous and is corrected here.** I wrote that the control
> *"validates their figures and cannot validate mine"*, scoping it the way their single-kind caveat
> scopes the ratio. **That was wrong: it validates neither.** What they had compared was not one
> array under two bounds — it was **two different arrays that happen to have different extents**.
> The stability was real; the claim was about what the stability *proved*, and that is the part
> nobody had tested. They withdrew it from both their sheets rather than scoping it, which is the
> right call: *a sheet that supports a right answer with a broken argument invites the next reader
> to reuse the argument.*

> **Their generalisation, which I think is the durable one from this whole exchange:**
> **a control that has only ever been run on the data that suggested it is not a control yet.**
> It held on the arrays it was born on and broke on the first foreign dataset.

**No figure moved on either side** — theirs rest on the same kind of anchor as mine.

**What actually anchors my two counts, independent of any extent — external string exhaustion:**

| | anchor |
|---|---|
| ns21 = 2 arrays × 215 | all **430 of 430** `.ard` strings in the image reached, **0 unreached**; 430 / 215 stems = **2.000**; `.ard` verified single-kind within extents |
| ns37 = 2 arrays × 329 | all **658 of 658** `.vpcjp` strings reached, **0 unreached**; 658 / 329 stems = **2.000**; 329 × 4 fields = **1,316**, matching the walk |

`.vpcjp` is the discriminating extension for namespace 37 the way `.ard` is for 21 — `.ebp`, `.mot`
and `.snd` are shared with namespaces 5 and 8 and isolate nothing. **Neither anchor depends on
where a walk stopped.**

**The bounded walker's real value was not re-deriving the numbers.** It produced no correction. It
made the extent *explicit enough to interrogate*, which is what let me ask whether my figures
depended on it — and find that a check I would otherwise have accepted from a peer does not apply
to my data.

### Cross-lane open item, stated plainly rather than left as a soft edge

**Nobody has read a function that opens a `.nmb` and walks it.** Six of eleven `ResourcePath_Get`
sites now resolve away from kind 26, five do not, and namespace 37 turned out to be an override —
none of that gets closer to a consumer. The two three-byte symbols in `.nmb` remain undecoded.
**That is a fresh block of work — five unresolved sites, each a different indirection — not a loose
end anyone can tidy in passing.** `repos-3f`'s assessment, and I agree with it.

### `COVERAGE.md` DRAFT — my half of entry 2, written here so it merges from two sources

`repos-3f` is deliberately not carrying my numbers. **Entry 2 should merge from two inboxes.**

> **A range bounded by a structure's first and last member is not that structure.**
> Inbound references to such a range say nothing about which structure they reach — some will hit
> real members, most will hit whatever else occupies the span.
>
> **Sighting A (`repos-1e`, `.ard` path table).** The span `0x01E0D000–0x01EDD800` was derived from
> the first and last `.ard` pointer site and then treated as "the table". It is not: it holds
> **7,241** slots carrying `.ard`/`.fpk` pointers against the **430** `.ard` entries being bounded,
> because it contains several other path arrays with `.fpk` dominating. Separately, **256** `.rdata`
> qwords point into the span; of their distinct targets **19 are real table slots** and 166 are not.
> The set was correctly dropped as evidence, but the stated reason — *"nothing to do with the path
> table"* — was false for those 19.
>
> **Sighting B (`repos-3f`, `.nmb`).** 15 stray qwords resolving to `.nmb` paths, initially cleared
> against the two kind-26 arrays only. Re-tested against **all 94 array bases across all 41 kinds**
> (20,107 member slots): 657 total, 642 inside a recovered array, **15 outside all of them**, all 15
> with both neighbours resolving to nothing — and **3 of the 15 point into the interior of a path
> string**, resolving to a bare `.nmb` tail rather than a string start, so they cannot be members
> under any reading.
>
> **What separates the two.** A tested one structure and called the rest strays; B tested a span and
> called it a structure. **Neither tested against *the structures*** — the fix in both cases is to
> materialise every array's members from the initialisers that install them, then test membership.
>
> **Do not read this as "distrust the decision".** Dropping an inbound-reference set as semantic
> evidence is correct under the banned-evidence list's **address-adjacency** rule *regardless of how
> many members it happens to hit*. What was wrong in sighting A was the supporting number, not the
> call. The lesson is about the evidence offered for a decision, not about the decision.

*(That last paragraph is `repos-3f`'s correction of my own framing and I think they are right: I had
called it "a right call for a wrong reason", which is harsher than the evidence and points the
lesson the wrong way.)*

### Entry 4, new: a byte scan cannot settle "is this magic validated" in EITHER direction

> **DUPLICATE — `repos-4b` has drafted this same entry in their inbox and we have each said so.
> Merge ONE copy.** We wrote it independently, then reproduced each other's numbers with separate
> implementations; the duplication is the corroboration, not extra content.

`repos-4b` found the case that closes this. **`.sab`'s magic IS checked on every load** —
`Sab_IsSabf` `0x007CFF90` does `cmp eax, [rip+0x541614]` against a four-byte tag at `0x00D115B4` —
**and a `.text` scan for `sabf` returns zero hits**, because the constant lives in `.rdata` and is
reached through a memory operand. Zero `.text` hits is fully compatible with the magic being checked.

**I re-tested my own two "never validated" results against that, and both survive from a second
direction:**

| | whole-image occurrences | operand test | verdict |
|---|---|---|---|
| `EBP2` | **0** (any section, ASCII, LE and BE dword) | n/a — nothing to compare against | never validated |
| `FF12AR03` | **0**; tail `AR03` **0** | n/a | never validated |
| `0x8000000B` (`section_000` marker) | **19** (8 `.text`, 11 `.rdata`) | **no instruction takes it as an immediate or displacement** — the 8 are byte coincidences inside unrelated instructions | never compared |
| `sabf` *(positive control)* | **1**, `.rdata` | *is* compared, via `cmp eax, [rip+…]` | validated |

**The marker row is the point.** A byte scan there is *not* empty, so the scan alone would have been
consistent with a check; only decoding every containing function and testing instruction operands
settles it. **The rule: a magic-byte scan settles nothing on its own — a positive needs the operand
test, and a negative needs either a complete body read or a whole-image scan showing no constant
exists.** My two negatives were always carried by the body read; this adds the second leg.

**What the 8 `.text` hits actually are, because the mechanism makes the entry reusable.** The
pattern needs only `0B 00 00` followed by any byte ≥ `0x80`:

| site | instruction the bytes fall in | why it matches |
|---|---|---|
| `002A8DB2` | `je 0x2a98dd` (`rel32 = 0xB28`) | **straddles the instruction boundary** — takes the next instruction's first byte as its `0x80` |
| `002971C0` | `and word ptr [rbx + 0xb4a], ax` | straddles |
| `004055AD` | `call 0x4060b0` (`rel32 = 0xB00`) | straddles |
| `0074F79E` | `jmp 0x75035b` (`rel32 = 0xBBA`) | straddles |
| `001884E6` | `mov rcx, [r14 + rax*8 + 0xb08]` | straddles |
| `00313422` | `or dword ptr [rbx], 0x800000` | ModRM `0x0B` + low 3 bytes of the imm32 |
| `002FB5B9` | `mov dword ptr [rbp + 0xb], 0x3f800000` | displacement `0x0B` + low 3 bytes of **`1.0f`** |
| `00404388` | same instruction, second site | same |

**Five of the eight span an instruction boundary**, which rules them out as operands on its own,
before any operand test. And **because `1.0f` is `3F800000`, every marker of the form `0x8000000X`
collides with any `[reg+0x0X]` store of `1.0f`** — so this recurs *by construction* for the whole
`0x8000000n` section-marker family, which is precisely the family the abandoned constant-scan census
was trying to count. **That is the mechanism behind that census's noise floor of 84**, stated as a
cause rather than as a measurement.

*(The 8 sites and the `1.0f` observation are `repos-4b`'s, reproduced here from the bytes; the
straddling analysis is this session's.)*

### FOR THE COORDINATOR: `St2e-Carriers/README.md` line 101 carries the same error, and it is yours to fix

Not edited by me — it is the coordinator's file. But the correction above lands directly on it:

```
| table span | `0x01E0D060` – `0x01EDD680`, in `.data` |
```

**That is a span bounded by the first and last `.ard` pointer, presented as a table.** It is not one.

| README implies | measured |
|---|---|
| one table spanning `0x01E0D060`–`0x01EDD680` (0xD0620 B) | **two arrays**, bases `0x01E0CFA0` and `0x01EDC280`, installed at namespace 21 by `002DFE66` and `002DFA9E` |
| the span is the table | the span holds **7,241** slots carrying `.ard`/`.fpk` pointers, against 430 `.ard` entries — it contains other path arrays too |
| the table starts at `0x01E0D060` | **both real bases are below it**; `0x01E0CFA0` is 24 qwords earlier, and the first 24 entries are NULL |
| "stride 16 bytes in 406 of 429 gaps" | true of **the `.ard` pointer sites**, not of the array — the arrays are flat `char*[]` at 8-byte stride carrying `bin`, `tm2`, `mrp`, `as7`, `ico`, `efx`, `cm`, `sys`, `mg` as well |

**The 16-byte record is still a correct description of the `.ard`/`.fpk` region** (§3 of my sheet
proves the parity), so the README is not wrong about the pairing — it is wrong that the pairing
describes the whole span, and wrong about where the table begins.

**This is the `+0x60..+0x80` situation inverted.** There I was asked to dump 32 bytes before
theorising and the dump was the whole answer; here a bound was inferred from two endpoints and
inherited as a structure. Both are cheap to check and neither was.

### NEW: the binary expects 215 areas and 166 ship

| | |
|---|---:|
| `.ard` paths hardcoded per locale tree (`ch`, `in`) | **215 each, identical stem sets** |
| area stems that ship an `.ard` | **166** |
| **named in the binary, never shipped** | **49** |
| **shipped but not named** | **0** |

**The containment runs one way.** Among the 49 are whole families — `alc_a`…`alc_f`/`alc_z`,
`byu_a`…`byu_z`, `dor_a`/`dor_z`, `glf_a`/`glf_z` — which is what a cut or merged region looks like,
not scattered typos.

**This sharpens the carrier README's open question.** *"Only 166 of 251 areas have an `.ard`"*
compares against the `plan_map` folder count. The sharper comparison is against **what the engine
asks for**, and by that measure the shortfall is **49, not 85**. It is also the third instance of one
shape inside a single format: 49 dead `.ard` paths, 7,520 `.fpk` paths with no files, and
`trailerOff` read by nothing. It does **not** explain the `ch`/`in` duplication — both trees name the
identical 215 stems, so that remains open.

## OPEN-QUESTIONS (round 2)

- **`PROPOSED-repos-1e-6`** — `varA` (`+0x0C`) is authored, varies across 134 areas, and has no
  reader by three independent searches. Cut feature, or read through a computed access the scans
  cannot see? *Killer observation:* a runtime watchpoint on `base+0x0C` of the loaded `.ard`.
- **`PROPOSED-repos-1e-7`** — `FUN_002DF9A0` switches path-table sets on a locale id with **at
  least six cases**; only the two that carry `.ard` (`ch`, `in`) were traced. Does any other case
  select a *different* `.ard` table? This bears directly on the README's unexplained
  "why exactly two locale trees, neither `us` nor `jp`".
- **`PROPOSED-repos-1e-8`** — `FUN_003DCF00` / `FUN_003DCF10` consume `varF` from `.ard` and from
  EBP `section_019` respectively. Not read. Whoever writes `section-019.md` and the `.ard` container
  sheet needs the same answer.

## MANIFEST-ROWS

Offered for the coordinator's gate — all read in full this round, all `Resource`/`BattleData`
boundary work, all cited above:

```
entry     domain                                              unused  evidence
002DF980  Resource.PathTable.NamespaceIndexedLookup           no      22 B; pathTables[ns][idx] at 002DF98D/002DF991; ns 21 = .ard; how-the-ard-loader-binds-area-battle-data.md
002DF880  Resource.PathTable.NamespaceIndexedLookupAndCopy    no      89 B; same lookup + byte copy, -1 on NULL at 002DF8A0; same sheet
003EA820  Resource.AreaArd.LoadOrUnloadFieldResource          no      476 B; Resource_GetSize/BeginRead(21, idx*2) at 003EA868/003EA97F; size<1 unbinds all five categories; same sheet
003EA710  Resource.AreaArd.BindRootAndBattleSections          no      267 B; reads +0x10/+0x14/+0x18/+0x24/+0x28/+0x2C only; same sheet
0023A160  BattleData.AreaArd.SectionCategoryDispatch          no      103 B; five-way sub-ecx ladder 0023A160-0023A176 into 02EBF150/168/120/148/140; same sheet
```

*(I have deliberately not proposed a row for `FUN_002DF9A0` — I read its structure and its two
`.ard` branches, not all six locale cases. `PROPOSED-repos-1e-7`.)*

## COVERAGE (round 2)

**`02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`** — new, `DOCUMENTED`, tier 1, `corpus_validated: 166 / 166`.

**Declarations:**

- **`archive_formats: "ard"` IS declared here — claimed late, and the reasoning is on the record.**
  I first held it back for a container sheet that owns the layout. **That sheet does not exist**: the
  peer I offered it to had the `.nmb` row, not `.ard`, and `St2e-Carriers/` holds only the README,
  `area-nmb-index.md` and mine. Leaving a censused, scored format at `[ ]` is worse than either
  plausible owner holding it, so I took it. `check_assets.py` now reads
  `[x] ard  explained  …/how-the-ard-loader-binds-area-battle-data.md`, **no collision.** If a
  dedicated layout sheet lands later the line should move there — §7 of my sheet says so.
- **`registry_slots`: I said "all five already have owners". That was FALSE, and the coordinator
  caught it.** None of the five was declared anywhere. `registry_explained` stood at **5 / 63** and
  the declared slots are `02EBF0C0`, `02EBF0F8`, `02EBF138`, `02EBF160`, `02EBF190` — the gambit
  document declares `0x02EBF160`, one hex digit from the `0x02EBF168` I assumed it owned.

  **Verified before acting on it** (`check_formats.py`, not a grep), then resolved: **four are now
  declared here** — `02EBF120`, `02EBF140`, `02EBF148`, `02EBF150` — and **`registry_explained` is
  now 9 / 63, no collisions.**

  **`0x02EBF168` deliberately left undeclared, and this is not the same mistake twice.** Its
  *contents* are explained in more depth by
  `09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md` (order sets as
  32-bit offsets resolved against `0x01F83530`); I establish only where the bytes come from.
  Declaring it here would put ownership on the weaker document. **It scores 0 today either way — if
  that sheet does not take it, it should come here rather than stay unclaimed**, which is the same
  call I made for `archive_formats: "ard"`.

  **How the wrong reading was reachable, since that is the reusable part.** A `grep` for those
  addresses hits three other documents and they genuinely *discuss* them — `02EBF120` and `02EBF150`
  at length. **I read discussion as ownership.** That is rule 3c's own warning running backwards:
  the rule exists because `02EBF138` is *mentioned* in ten documents and *explained* in one, which
  is why the numerator counts declarations instead of scraping prose. The same gap that makes a
  mention look like an explanation makes it look like a declaration. **No single session could have
  caught this** — the declaration set lives across every document's frontmatter — and the fix is to
  run `check_formats.py` rather than trust a grep. Recorded in the sheet's new §8.

  **What did not change: the reading.** The mapping, binding sites and consumer sets are unchanged
  and tier 1. Only the declaration decision was wrong.

### The three counts reconciled — and it is genuine corroboration, not agreement by construction

My §5 first recorded "six fields read / five registry slots / four `st2e` tables" as three numbers I
could not map onto each other. **`repos-d6`'s corpus pass supplies the missing column and the two
readings partition the directory identically:**

| slot | offset | `st2e`? *(their corpus)* | `recordSize` | destination *(my instruction read)* |
|---:|---|---|---|---|
| 0 | `+0x10` | yes 166/166 | 84 | cat 0 → `02EBF150` |
| 1 | `+0x14` | **no 0/166** | — | cat 1 → `02EBF168`, **via a different binder `FUN_003846F0`** |
| 2 | `+0x18` | yes 166/166 | 88 | cat 2 → `02EBF120` |
| 3 | `+0x1C` | absent | — | never read |
| 4 | `+0x20` | absent | — | never read |
| 5 | `+0x24` | yes 166/166 | 56 | cat 3 → `02EBF148` |
| 6 | `+0x28` | yes 166/166 | 56 | cat 4 → `02EBF140` |
| 7 | `+0x2C` | **no 0/166** | — | `FUN_003DCF00`, **no registry slot** |

**The two slots that are not `st2e` are exactly the two my loader reading had already singled out as
different**, and neither pass was told the other's answer. Counting `st2e` magic in files and
following call targets in instructions have **no shared failure mode**, so the same 4/2/2 partition
from both is real corroboration. Reconciliation: **8 slots, 6 present, 4 carry `st2e`, 5 reach the
registry** — three different counts, no contradiction, every slot now accounted for.

**I renumbered my sheet's fields to their slot indices** (`sect0..sect5` → `slot0..slot7`). My
numbering covered only the six fields the loader reads and **hid that slots 3 and 4 exist and are
always empty** — which is precisely the fact an *indexed* directory is supposed to make observable,
and the same point the EBP2 sheet makes about `001`/`005`/`007`. Their numbering is better and my
sheet now uses it, credited.

### `.nmb` cross-link — and an index trap I nearly walked into

The `.nmb` sheet reports its entry count equals **"`st2e` table 1"**'s record count, 166/166. **That
is the second `st2e` table, which is slot 2 — not slot 1.** The `st2e` tables are the present slots
`0, 2, 5, 6`, so the two numberings differ, and I had it wrong in my first draft of §8 before
catching it. Slot 2 is category 2 → **`0x02EBF120`**, which is also the slot with the widest reader
set. **Two independent lines now point at slot 2 as the per-area unit list — both still leads**, and
my sheet says so.

### Struct fences

New requirement adopted. `check_layouts.py`: **25 fences, 14 documents, 0 ERRORs.**

- `Ff12Ar03Header`, `ArdPathTablePair` (new sheet) — clean.
- **Retrofitted my two EBP sheets**, which predated the requirement: `EbpContainerHeader` (clean)
  and `EbpSection000Header`. The latter reports **`UNACCOUNTED +0x52..+0x54` (2 bytes)** and **that
  is the correct output** — `flag50` is provably 16-bit from `cmp word ptr` at `0026CD1A`, and what
  follows it is unknown. I left the gap rather than labelling it padding; the sheet says why.

**Gates, re-run AFTER writing:**

| gate | result |
|---|---|
| `check_layouts.py` | 2 fences (`Ff12Ar03Header`, `ArdPathTablePair`), **no findings**; the run's only ERROR is in `area-nmb-index.md` (not mine — see below) |
| `check_links.py` | **0 broken**, 252 files / 9,777 links scanned |
| `check_source_hygiene.py` | `no stray control bytes` |
| `check_named_not_cited.py` | **no rows** — the first run flagged 8, and every one was a function my argument genuinely rests on, so all 8 got addresses rather than a rewrite |
| `check_located_not_read.py` | **no rows** |

> **For repos-4b / the coordinator:** `check_layouts.py` reports one ERROR repo-wide, in
> `St2e-Carriers/area-nmb-index.md:67` — `+0x04  u32[]  offset` — `u32[]` with no size is not a
> valid type in the fence grammar. Needs `u32[N]` or a stated count. **Not touching another
> session's sheet; flagging it.**

## AUDIT-LOG (round 2)

- **An instrument returned a clean false negative and I nearly wrote it down.** `DumpDataXrefs.java`
  reported `DUMP_DATA_XREFS_NONE` for every probed table address, and a linear `.text` disassembly
  independently agreed. **Two instruments, same wrong answer, because they share the assumption that
  a consumer names its target.** The fix was a per-function scan over `functions.tsv` boundaries.
  **Recorded because "zero xrefs" reads exactly like a finding** — and had I reported "the `.ard`
  table is never referenced", it would have been a confident, checkable, wrong claim.
- **A decompiler ordering trap, caught by reading the branch ladder.** Ghidra prints
  `BattleData_SetAreaArdSectionCategory`'s cases in an order that does not match the `sub ecx, 1`
  chain. The category-to-slot mapping taken from the printed order is wrong. **Anyone re-deriving
  this should read `0023A160`–`0023A176`, not the pseudocode.**
- **An interior anchor caught an error in my own draft.** I had written that
  `AreaData_BindAndRebaseSectionDescriptor` rebases descriptor field `+0x00`; disassembling to get
  the anchor showed it is **`+0x0C`** (`00384600`). The claim had come from a decompiler field name.
  **This is the second time this round that a name, rather than an instruction, was the error
  source.**
- **`check_named_not_cited` was right and I did not argue with it.** All 8 flagged functions were
  load-bearing, so I added addresses. None was a passing reference.

---
---

# ROUND 1 — EBP (reported 2026-09-03, unconsumed below)

## STATUS

Lane 1 (`container`, `section_000`). GN160 imported into `Tools/work/repos-1e_proj`, verify
**passed exactly**: `internal=38161 owner=9409 finalNo=585 codeDomain=28028 overlap=0 explicit=38022
unresolved=139 pct=99.63575`. **Not blocked.**

**BOTH LANE-1 SHEETS ARE WRITTEN AND DECLARED (8/14 after mine).** The loader contract was posted
first, before them, because five lanes were waiting on it — it is still below and still current.
The 32-byte hole the board assigned me is **settled**: alignment padding, proven.

**THE LOADER QUESTION IS SETTLED — read `## THE LOADER CONTRACT` below before you write your §3.**
Posted first, before my own sheets, per ASSIGNMENTS.md §4. All three questions the board asked are
answered from the loader body at tier 1, plus a corpus census that hands every lane its section
magic.

> **Import note for everyone:** the `-ProjectDir '..\..\work\<name>_proj'` in ASSIGNMENTS.md §2
> **fails** — `analyzeHeadless` rejects a path element starting with `.`
> (`IllegalArgumentException: Path element starting with '.' is not permitted`). Pass an **absolute**
> `-ProjectDir`. The SHA check passes before that point, so the parent itself is fine.
> For later steps use `Invoke-GfzHeadless.ps1 -Mode Process -ProgramName (Get-GfzProgramName ...)`.

---

## THE LOADER CONTRACT — the shared dependency, settled

### 1. Which function reads the directory

**`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` — `0x003304A0`, 570 B.**

It is the **completion callback of the raw file read**, and the whole path to it is:

```
WorldSimulation_ProcessDeferredModeRequest      0x0032FC30
  -> ActorResource_BeginManagerResourceSetLoad  0x0032FCA0
    -> ActorResource_BeginPrimaryPayloadLoad    0x00330310
       size = FUN_0032e400(ns, idx); buf = FUN_0036c660(...)      alloc whole file
       FUN_0032e620(ns, idx, buf, size, ctx)                      async read, completion =
    -> ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources 0x003304A0
```

Each arrow is the **only** caller of the next (`edges.tsv`, GN160 graph). The buffer is the **whole
`.ebp` file**, read in one shot at its natural size; there is no streaming and no per-section read.

### 2. How a section index reaches its handler

`0x003304D9  and rdi, rax` (with `rax = 0xFFFFFFF0`) recovers the file base into `rdi`. Then the
function is a **flat open-coded sequence of 14 guarded dispatches** — no loop, no table:

```asm
00330504  mov  eax, dword ptr [rdi + 0x10]   ; slot 0 offset
00330507  test eax, eax                      ; 0 = absent
0033050B  add  rax, rdi                      ; base + offset
00330510  or   eax, ebx                      ; pack manager index into the low 4 bits
00330514  call 0x32f850                      ; the slot-0 handler
```

**Extracted mechanically from the instruction stream** (all 15 `cmp dword ptr [rdi+4], N` sites):

| slot | gate | offset read at | handler call site | handler |
|---:|---|---|---|---|
| 0 | `slotCount > 0` | `00330504` | `00330514` | `ActorResource_OnDefinitionPayloadLoaded` `0032F850` |
| 2 | `> 2` | `0033051F` | `0033052F` | `FUN_00330190` |
| 3 | `> 3` | `0033053A` | `0033054A` | `FUN_00330220` |
| 4 | `> 4` | `0033063B` | `0033064B` | `FUN_00332100` -> `FUN_003dfdc0` |
| 6 | `> 6` | `00330555` | `00330565` | `FUN_00330060` |
| 8 | `> 8` | `00330599` | `003305A9` | `FUN_0032fa10` |
| 9 | `> 9` | `0033057E` | `0033058E` | `FUN_0032fac0` |
| 10 | `> 10` | `003305CF` | `003305DF` | `FUN_00331610` |
| 11 | `> 11` | `003305B4` | `003305C4` | `FUN_003316b0` |
| 12 | `> 12` | `003305EA` | `003305FA` | `FUN_0032fb70` |
| 14 | `> 14` **and `manager_index != 0`** | `0033067A` | `0033068A` | `FUN_00330110` |
| 16 | `> 16` | `00330605` | `00330615` | `FUN_003320e0` -> `FUN_003dfe60(0, base)` |
| **17** | `> 17` | `00330620` | `00330630` | `FUN_00332110` -> **`FUN_003dfe60(1, base)`** |
| 19 | `> 19` | `00330656` | `00330666` | `FUN_003320d0` -> `FUN_003eaa00` |

**The gate is uniformly `slotCount > slotIndex`** — checked programmatically across all 15 sites,
`bound == slotIndex` holds for every one. So **`+0x04` is not a version stamp, it is the directory
length and it is genuinely enforced.** A file with `slotCount = 3` would have slots 4+ ignored even
if their offsets were valid. `jbe` — the comparison is **unsigned**.

The three findings a corpus reading cannot produce:

- **Slot 17 has a handler and occurs in 0 of 1,115 files.** `FUN_00332110` at call site `00330630`
  is real, reachable code. It calls the **same binder as slot 16** with the selector flipped:
  `FUN_003dfe60(0, base)` for 16, `FUN_003dfe60(1, base)` for 17. **`section_017` is the same
  format as `section_016`, second instance.** That is why the index space looked sparse at 13.
- **Slots 1, 5, 7, 13, 15, 18 have no handler at all.** Not "absent from the corpus" — *structurally
  unreachable*. Setting a non-zero offset there changes nothing.
- **Slot 14 is skipped entirely for `manager_index == 0`** (`0033066B test ebx,ebx ; je`).

### 3. Is the `EBP2` magic validated? — **NO. It is never read.**

**This is a genuine `Inert` row, and it is proven, not inferred from a failed string search.**

Disassembling the whole 570-byte dispatcher and collecting every `[rdi + N]` reference gives the
complete set of container fields the engine touches:

```
offsets touched = { 0x04, 0x10, 0x18, 0x1C, 0x20, 0x28, 0x30, 0x34,
                    0x38, 0x3C, 0x40, 0x48, 0x50, 0x54, 0x5C }
references to [rdi] (i.e. +0x00, the magic) = 0
```

`+0x00` is exactly `+0x04` minus four and the function reads `+0x04` fourteen times. **Nothing in
the load path compares the magic:** `BeginPrimaryPayloadLoad` allocates by size and hands the buffer
to a generic resource reader that is not `.ebp`-aware; the completion callback goes straight to
`+0x04`. The bytes `E B P 2` are **authoring provenance only**.

So of the README's two readings, **reading 1 is correct** — and the reason the string/dword search
found nothing is simply that there is nothing to find. The blind-spot hypothesis (arithmetic,
16-bit halves, hashed) is **not needed and should not be carried in any sheet**.

**`+0x08` and `+0x0C` are also never read** — the census's "0 in all 1,114" is confirmed as
*inert*, not merely *constant*.

### 4. Two mechanical constraints the corpus alone could not explain

- **Why offsets must be 16-byte aligned.** `0x00330510 or eax, ebx` packs the 4-bit manager index
  into the low bits of the *resolved* pointer, and every handler recovers it with
  `and reg, 0xFFFFFFF0`. Any offset with a low nibble set would corrupt the manager index. The
  corpus is `0x40`-aligned (all 5,419), so the format **over-delivers** — but 16 is the hard
  requirement.
- **The resolved section pointer is carried through 32 bits.** `or eax, ebx` / `mov ecx, eax` are
  32-bit; the handler re-widens with `and rdi, 0xFFFFFFF0` (`0032F860`–`0032F871`). **The `.ebp`
  buffer must live below 4 GiB.** That is an allocator constraint, not a file constraint, but it is
  a real property of this build.

---

## GIFT TO THE OTHER FIVE LANES — every section's magic, corpus-validated

Independent re-census of all 1,115 files (my own script, not `census_ebp_container.py`). It
**reproduces the frozen denominator exactly** — 1,114 containers, `slotCount = 20` in all 1,114, all
5,419 offsets `0x40`-aligned, and `evt_t0020.ebp` the one non-container (`07 00 00 80`).

**Each magic below is 100 % consistent across every file that has the section** — not a sample:

| unit | n | first 4 bytes of the section body | owner |
|---|---:|---|---|
| `section_000` | 1114 | `0B 00 00 80` = **`0x8000000B`** | repos-1e |
| `section_002` | 828 | *no magic* — leading u32 varies (offset-table shape) | repos-3f |
| `section_003` | 359 | *no magic* — same shape as 002 | repos-3f |
| `section_004` | 209 | **`NAVI`** (209/209) | repos-c9 |
| `section_006` | 67 | **`TIM2`** (67/67) | repos-c9 |
| `section_008` | 423 | **`CML1`** (423/423) | repos-4b |
| `section_009` | 423 | **`CAM7`** (423/423) | repos-4b |
| `section_010` | 113 | **`CML1`** (113/113) | repos-c7 |
| `section_011` | 113 | **`SHK1`** (113/113) | repos-c7 |
| `section_012` | 842 | *no magic* — small leading count | repos-d6 |
| `section_014` | 140 | **`LGT2`** (140/140) | repos-c9 |
| `section_016` | 517 | **`FF12`** (517/517) | repos-d6 |
| `section_019` | 271 | **`FF12`** (271/271) | repos-c9 |

**The strict pairs explain themselves.** `008` and `010` carry **the same magic `CML1`**. So `CML1`
is not "section 8" — it is a **shared list/track container that appears twice in the directory**,
paired once with `CAM7` (008+009, 423x) and once with `SHK1` (010+011, 113x). The pair is
`CML1 + <track type>`, and the co-occurrence is the *format*, not a coincidence. **repos-4b and
repos-c7 are documenting two instances of one mechanism** — worth a word between you.

`section_006` is **`TIM2`**, the PS2 texture format — a shipped-format cross-reference for category
02, and a strong hint that `.ebp` carries PS2-era payloads verbatim.

`016` and `019` share the magic `FF12` but go to **different binders** (`FUN_003dfe60` vs
`FUN_003eaa00`), so `FF12` is a generic wrapper tag, not a type. Do not merge them on the magic.

*(Caveat, stated so nobody over-reads it: a 4-byte magic identifies the body's **wrapper**. It does
not tell you the record layout, and `CML1` in two slots is exactly the case where assuming it does
would mislead.)*

---

## OPEN-QUESTIONS
<!-- MERGED 2026-09-03 by repos-55 into _index/OPEN-QUESTIONS.md as BW-1..BW-5. Marked, not deleted: the sessions are live and deleting under a writer risks a lost update. Do not re-merge. -->


- **`PROPOSED-repos-1e-1`** — `section_017` has a live handler (`FUN_00332110`, call site
  `00330630`) sharing `FUN_003dfe60` with `section_016` under selector `1`, yet occurs in **0 of
  1,115** `us` files. Is it populated in another language's archive, or is it authored capacity the
  shipped game never uses? *Killer observation:* census the `jp`/`eu` `.ebp` trees for a non-zero
  slot 17; one occurrence closes it. Same shape as the ten `NOT USED` battle-command markers and the
  six inert VM opcodes.
- **`PROPOSED-repos-1e-2`** — the resolved section pointer is truncated to 32 bits
  (`00330510`, `0032F860`). Does the resource allocator guarantee a sub-4 GiB arena, or is this a
  latent 64-bit defect that survives only because the heap happens to sit low? *Killer observation:*
  read `FUN_0036c660`'s arena for an explicit low-address reservation.
- **`PROPOSED-repos-1e-3`** — `section_014` is dispatched only when `manager_index != 0`
  (`0033066B`). What distinguishes manager 0? If manager 0 is the field/world manager, `LGT2`
  lighting for the base field would be loaded by some other route, or not at all.
- **`PROPOSED-repos-1e-4`** — `weatherProbability` is bound to `section_000` header `+0x64` by two
  independent pointers (fixed arity 3 in 1,114/1,114 files; the glossary's own attribution), but
  **the reading instruction was not found** — `ActorManager_BindLoadedDefinitionPayload` does not
  touch `+0x64`, so the consumer is in the weather subsystem. *Killer observation:* find the load of
  `+0x64` off the manager record and confirm it feeds the transition roll. Until then this binding is
  weaker than the rest of that sheet's §3 and is marked so.
- **`PROPOSED-repos-1e-5`** — the structure behind `ActorScriptResource_GetBytecodeOffsetById`
  (`[rcx+0x48]`, u32 count, 8-byte stride from `+8`) and `FUN_003589E0` (`[rcx+0x50]`, 4-byte stride
  from `+4`) is unidentified. **The actor-manager record is ruled out**: record `+0x50` is set from
  section_000 `+0x48` at `0026CB17`, which is the *name pool*, so `FUN_003589E0` would be reading
  `"init"` as a u32 count. That also means the GFZ comment's claim that `ctx+0x58` is the script
  image base cannot be about the manager record (`+0x58` there is a scratch-bank pointer) — **one of
  the two readings is wrong and neither should be inherited.** *Killer observation:* read the two
  callers of `0x003DBDC0` (`0x0025E4C0`, `0x003DB6E0`) for what they put in `rcx`.

## CALL-CHAINS / ADDRESS-INDEX

| address | role | read? |
|---|---|---|
| `0x0032FC30` | `WorldSimulation_ProcessDeferredModeRequest` — enters the load | partial |
| `0x0032FCA0` | `ActorResource_BeginManagerResourceSetLoad` | partial |
| `0x00330310` | `ActorResource_BeginPrimaryPayloadLoad` — allocates + async-reads the whole file | ✅ |
| **`0x003304A0`** | **`...OnPrimaryPayloadLoadedAndDispatchSubresources` — the EBP2 directory walk** | ✅ full |
| `0x0032F850` | `ActorResource_OnDefinitionPayloadLoaded` — slot 0 handler | ✅ |
| `0x0026C8C0` | `ActorManager_BindLoadedDefinitionPayload` — parses the `section_000` header | ✅ |
| `0x00358A00` | `ActorScriptResource_GetBytecodeOffsetById` — bounds-checked id→offset | ✅ |
| `0x003589E0` | sibling lookup, called by the interpreter `0x0025E4C0` | ✅ |
| `0x003DBDC0` | `ActorResource_StartEntryScriptExecution` — installs the VM PC | ✅ |
| `0x003DFE60` | shared binder for **slot 16 (sel 0) and slot 17 (sel 1)** | not read |
| `0x003EAA00` | slot 19 binder | not read |
| `0x003DFDC0` | slot 4 binder (`NAVI`) | not read |

**New cross-subsystem transition:** `ActorResource` (category 05/ActorEntity) → `ScriptVM`
(category 01) at `0x003DBDC0`, where the loaded `section_000` becomes the interpreter's PC. The
interpreter document `0x0025E4C0` does **not** mention its loader; that is a `NEW SINCE BASELINE`
edge, not a defect in it.

---

## THE 32-BYTE HOLE AT `+0x60 .. +0x80` — SETTLED (assigned to me in §4 of the board)

`check_layouts.py` flagged `+0x60 .. +0x80` as unaccounted in all 1,114 containers. The board offered
three readings — alignment padding, a second header, or authored bytes nothing reads. **Two are
dead and the third is proven.**

| | |
|---|---|
| the 32 bytes are all-zero | **1,114 / 1,114** |
| distinct bit patterns across the whole corpus | **1** |
| offsets in `0x60..0x80` touched by the loader | **0** (the §3 read set is `+0x04` plus the 14 slot offsets, all below `0x60`) |

**It is alignment padding, and the arithmetic says why it is exactly 32 bytes.** Section offsets are
`0x40`-aligned (all 5,419), and **`0x60` is not a multiple of `0x40`**. The next `0x40` boundary at
or after the directory's end is `0x80`:

```
directory ends       0x60
next 0x40 boundary   0x80
padding              0x80 - 0x60 = 0x20 = 32
```

**"A second header" is excluded twice** — nothing reads there, *and* a header identically zero in
1,114 files carries no information. **"Authored bytes" is excluded** for the same content reason.
The board asked for the dump before theorising; the dump is the whole answer.

## `section_000` — what the sheet establishes

- **The header is exactly `0x90` bytes in 1,114 / 1,114.** Taking the minimum in-section value over
  every offset-valued header field, in every container, returns 144 every time.
- **Every script carries its own provenance.** `+0x08` → author username (28 distinct: `t-hirose`
  220, `mtanaka` 184, `naomif` 112 …), `+0x0C` → source filename — which **matches the `.ebp`
  filename stem in 1,114 / 1,114** — and `+0x10` → build timestamp, `"00/00 00:00"` in 1,113 files
  and **`"11/22 12:00"` in exactly one**. The timestamps were scrubbed for the retail build and one
  file escaped it. This is also the evidence that there is no runtime writer.
- **`+0x48` is the name pool**: flat NUL-terminated strings, `"init\0main\0"` then Shift-JIS
  `カット１`…`カット４`. The authoring model's handler names are in the file, and they were never
  localised even in the `us` build — which is why a **language-selected decoder** is installed at
  load (`FUN_00267930` / `FUN_00267bb0` / `FUN_00267c20`, chosen via `FUN_0036b200`).
- **The glossary's `weatherProbability` is located and its encoding refined.** `+0x64` is an
  **offset**, not the value; its target is a **length-prefixed byte array whose count is `3` in
  1,114 / 1,114 files**. In `alc_a0100.ebp`: `03 64 00 00` → `{100, 0, 0}`. Distribution across the
  corpus: `{100,0,0}` 775, `{0,100,0}` 118, `{0,30,70}` 73, `{100,100,100}` 43, `{0,0,100}` 35,
  `{0,60,30}` 24, `{0,50,50}` 10, `{30,50,0}` 9. **They do not have to sum to 100**, so these are
  three independent per-slot chances, not a distribution. `+0x6C` has fixed arity 1 and `+0x70`
  fixed arity 5 — the header carries a run of length-prefixed `option` arrays.
- **The loader clamps and rejects nothing.** The only guard on the entire section-0 path is
  `0032F87E cmp byte ptr [rdi], 0` — the section's **first byte** must be non-zero. The marker
  `0x8000000B` passes on its low byte `0x0B` incidentally; it is **never compared**. All four
  rebases (`0026CB0F/CB40/CB4B/CB56/CB64`) are unchecked against `+0x04` or against EOF.
- **One field is transformed rather than stored:** `+0x14`'s table (u16 count, u16 entries) is
  **summed** into manager-record `+0x20` at load (`0026CB7D`–`0026CBC1`).
- **`+0x50` is 16-bit and signed**, `cmp word ptr` at `0026CD1A`, with `0xFFFF` as a "none" sentinel
  in **493 / 1,114** files. A 32-bit reading puts 452 files out of range — the instruction width is
  doing real work.

## MANIFEST-ROWS

*(Still none. Every claim above is about **data layout**, not about a function's CodeDomain, and the
14 slot handlers are still `FUN_*`. I would rather hand the coordinator rows backed by a written
sheet than rows backed by a reading I have not published. The four handlers I read in full —
`0x0032F850`, `0x00332100`, `0x003320E0`, `0x00332110` — are candidates whenever the coordinator
wants them.)*

## COVERAGE
<!-- MERGED 2026-09-03 by repos-55 into _index/COVERAGE.md (section: 'The EBP round, six sessions in parallel'). Marked, not deleted - sessions are live. -->


**Both lane-1 units are written and declared.**

- `25-EBP-Script-Container/Container/ebp2-container.md` — `ebp_units: ["container"]`
- `25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md` — `ebp_units: ["section_000"]`

`check_ebp.py` after writing: **8 / 14**, my two units listed once each, **no collision**.

**Gates re-run AFTER writing, not only before:**

| gate | result on my two files |
|---|---|
| `check_ebp.py` | both units counted, no collision |
| `check_links.py` | **0 broken links** in either file (the 3 repo-wide breaks are `section-011.md` → `section-010.md` ×2 and an St2e README link — none mine) |
| `check_source_hygiene.py` | `no stray control bytes in 2 file(s)` |
| `check_named_not_cited.py` | **no rows** for either file |
| `check_located_not_read.py` | **no rows** for either file |

Both sheets carry an **interior** anchor per claim, not one per function: the gate constant
(`003304DE`), the slot read (`00330504`), the index packing (`0033052B`), the manager-0 exclusion
(`0033066B`), the payload register (`0026C8F7`), each rebase (`0026CB0F`/`CB40`/`CB4B`/`CB56`/`CB64`),
the sum loop (`0026CB7D`–`0026CBC1`), the 16-bit compare (`0026CD1A`), the first-byte guard
(`0032F87E`) and both lookup strides (`00358A0F`, `003589EF`).

## AUDIT-LOG
<!-- MERGED 2026-09-03 by repos-55 into _index/AUDIT-LOG.md (section: 'EBP container round - falsification passes'). Marked, not deleted - sessions are live. -->


- **Instrument correction.** ASSIGNMENTS.md §2's relative `-ProjectDir` cannot work; absolute
  required. Recorded so the next five sessions do not each rediscover it.
- **Negative result retired.** The board asked me not to repeat the constant scan (noise floor 84)
  and I did not. The dispatch table was read from the branch structure of one function instead, which
  gives all 14 slots with zero false positives — including slot 17, which the scan could never have
  distinguished from noise, and the six no-handler slots, which the scan reported as *present*
  (`001` scored 518).
- **A negative result worth keeping: the VM context is NOT the actor-manager record.** I mapped the
  record from `0x0026C8C0` (base `0x02098E10`, stride `0x288`, confirmed independently by
  `FUN_00263FF0` at `00263FF3`/`00263FFA`) and record `+0x50` is set from `section_000 +0x48`, the
  name pool. So `FUN_003589E0`'s `[rcx+0x50]` would be reading the ASCII `"init"` as a count. The
  identification is therefore open, but this one candidate is **closed by observation** rather than
  left vague. See `PROPOSED-repos-1e-5`.
- **Confirmed by a peer, and one of my phrasings tightened.** `repos-4b` independently re-censused
  the section magics and reproduced my table exactly, and separately established from
  `..\..\katano\atelload.c` (string at `0xd10958`, dispatcher `0x003306E0`) that the four
  camera/shake sections are two **DAT/CTL pairs** — `CAMDAT`/`CAMCTL`, `SHKDAT`/`SHKCTL` — which is
  *why* `CML1` occupies two slots. That is a better explanation than my "shared track container" and
  I am recording it as theirs. They also noted that a handler passes `(slot, blob)` and the binder
  copies the blob into a **second** global inside the same `0x02098E10 + idx*0x288` record — so an
  xref census on the handler's own global under-counts consumers. My container sheet §7 carries that
  caveat; **it is the reason I make no `Inert` claim about any section body.**
- **A GFZ name I am treating as unproven.** `ActorScriptResource_GetBytecodeOffsetById`
  (`0x00358A00`) reads `[rcx+0x48]`, and its sibling `FUN_003589E0` reads `[rcx+0x50]`; I have the
  two tables' shapes from the instruction stream (`00358A0C` / `003589EC`: u32 count at `+0`,
  8-byte entries from `+8`, resp. 4-byte entries from `+4`) but have **not** yet proven which
  structure `rcx` is. The GFZ comment's claim that `+0x58` is the script-image base does not fit the
  manager block I mapped from `0x0026C8C0`, so one of the two is wrong. **Not asserting either until
  I have read the callers of `0x003DBDC0`.** Flagged here so no other lane inherits it.
