---
experiment: EXP-103
title: Auto-status Notify (002FEF30) under isolated original execution
contract: ../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md
method: B
live_game: false
tool: evidence/autostatus-notify-exec/check.py
---
# EXP-103 — autostatus-notify-exec

**Status:** complete · **31/31 cases, 15/15 mutants, stable across three
processes**
**Evidence:** `evidence/autostatus-notify-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `run2.log`, `run3.log`,
`gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`002FEF30` ("Notify") is the auto-status event constructor — the body that
builds the 0x24-byte stat-event output for a unit: kind discriminator,
definition-row resolution, five-slot equipment accumulation, three status
bitmask walks over real rdata tables, and a clamped writeback followed by a
unit-side tail (reset masks, bit clears, flag OR). Its closure is almost
entirely already-proven code: `RESOLVE`, `FIND` (EXP-101), `EQGATE`/`EQCLASS`
and `VALID` (EXP-100). This experiment executes the subject **and every
closure body from shipped bytes**; only the two tail-effect sinks are
scripted boundaries with argument capture.

| VA | role | execution |
|---|---|---|
| `002FEF30` | subject — stat-event constructor | **real** (2859 B) |
| `002F8E50` | `((r8+1)*ecx*edx)/100` signed magic-mul | **real** (30 B) |
| `002F9180` | `(ecx*edx)/100` signed magic-mul | **real** (21 B) |
| `0031B860` | owning-unit FIND (EXP-101) | **real** (83 B) |
| `00236850` | pool count getter | **real** (7 B) |
| `00236820` | bounds-checked element getter | **real** (37 B) |
| `00322C50` | validity dispatcher, arm 6 path | **real** (1025 B) |
| `0031E9A0` | equipment gate dispatch | **real** (68 B) |
| `0031E9F0` | equipment class (t9 -> selector -> arm) | **real** (93 B) |
| `00309440` | class lookup from handle bits | **real** (30 B) |
| `0020E600` | resolver base accessor | **real** (10 B) |
| `003105D0` | unit-side reset helper | scripted (`X` token + arg capture) |
| `00307D10` | tail-effect sink | scripted (`A` token + arg capture) |

## Measured semantics (native execution, not static reading)

```
002FEF30(record rdi, rdx, r8):
  unit = rdx ? rdx : FIND(record)          ; flag64 = (unit != 0 path)
  zero 0x24-byte out struct at record+0x24
  kind = byte[record+5]                    ; 0xFF if record == 0
  flag5c = (kind==0 && record[4]-0x1B <= 0xC)   ; live, enables 0x7FFF cap
  flag4c = 1                               ; prologue init
  kind==0:  defrow via [0x2EBF130] -> RESOLVE -> row
            ae8 += MM3(row[...]) ; MM2 calls ; out[0x18] |= row[0x48]
            out[0x14] |= row[0x4C]
  kind!=0:  rowA = row(G_DT1, record[4])   ; rowB = row(G_DT2, rowA[0x22])
            rowC = row(G_DT3, rowA[0x24]) ; rowD = row(G_DT4, rowA[0])
            rowD writes out[0x1C..0x20] (5 bytes)
            rowA[0x15] bit0 clears flag4c + adds to ae8/a24
            rowA[0x15] bit1 clears flag70 + adds to a20/ad8
            level-delta-weighted stat accumulation (sub, not add)
  equipment loop i=0..4:
    id = word[record + 0x10 + i*2] - 0x1000
    VALID(6, id) + EQGATE/EQCLASS -> gate 1..3
    gate1 (flag4c): ae8 += row[0x1A]; r14 += row[0x1D]
    gate2 (flag70): r15/a20 += row[0x18]; edi/ad8 += row[0x19]
    gate3:          a34 += row[0x18];  a38 += row[0x19]
    12-13 RESOLVE reads per slot into out fields
  bitmask walks i=0..15 / 0..15 / 0..11 over rdata T1/T2/T3:
    ebp = 0 (start index 0); r15d = 1 reloaded before walks
    test bit (1 << i) of [unit+0x68]/[unit+0x78] mask dwords
    set bits resolve [0x2EBF040] rows -> out accumulation
  clamp/writeback:
    out[0]  = clamp(r14q, 1, kind?1e9:9999); flag5c -> 2nd write cap 0x7FFF
    out[4:6]= clamp s32 [0,999];  out[6..9] = clamp s32 [0,0x63]
    out[0x0F]= a20 ; out[0x10] = ad8 (UNCONDITIONAL)
    out[0x11]= clamp(a54 + a20 + a24 + a50, 0, 0x64)
    out[0x12]= clamp(a58 + ad8, 0, 0x64)
    out[0x0A..0x0C]= clamp s32 [0,0xFF]; out[0x0D..0x10]= [0,0x64]
    out[0x13]= umin(..., 3)
  unit tail (kind==0 && flag64 && ((out[0x18] ^ record[0x3C]) & 0x8000020)):
    RESET(unit) scripted X ; APPLY scripted A
    bit24 handling ; word[0] bit14 clear unless ba0 in {0x113, 0x95}
    mask writes at unit+0x788 / unit+0x6B0
    ZERO writes (ebp=0) at unit+0x6F8 / 0x748 / 0x770 / 0x750 / 0x74C
```

## Findings measured by the suite

- **`ebp` is zeroed at `0x2FF58F` and `r15d` reloaded to `1` at
  `0x2FF5A7`.** Three earlier misreads collapse to this one fact: the
  bitmask walks start at index **0** (not 5), the bit test is `1 << bit`
  (not an accumulated gate value), the status-null fault reads `word[4]`,
  the tail writes **0** (not 5), and `flag5c`/`flag64` compare against 0 —
  both flags are **live**, not dead.
- **`out[0]`'s lower bound is 1**, not the gate-2 accumulator — `r15d` is
  reloaded to 1 before the walks; the accumulated `a20` survives in
  `out[0x0F]`.
- **`out[0x10]` is `ad8` unconditionally.** `eax` is loaded from
  `[rsp+0xD8]` at `0x2FF7A7`; the later reload is redundant for this value.
  Earlier "leftover accumulator" and branch-dependent readings are
  disproven by replay (`kind0-out10-quirk`/`kind0-gate2-arm` cases).
- **`out[0x12]` is `a58 + ad8`** — `add r11d, eax` at `0x2FF7AE` adds the
  same `ad8` source into the second clamped sum.
- **The `0x7FFF` cap is a second, conditional write**, not a replacement
  bound: `out[0]` is first clamped to `[1, 9999]` (kind 0) or `[1, 1e9]`
  (kind != 0); when `flag5c` is set a second write caps at `0x7FFF`.
  `kind0-noband-cap` (flag5c=0) and `kind0-cap7fff` (flag5c=1, accumulator
  in `(0x3FFF, 0x7FFF)`) pin both paths.
- **EQCLASS is a two-stage dispatch**: byte table `t9 -> selector` then
  dword-RVA jump table `selector -> arm`. t9 classes: 0->1, 1->2, 2-6->3,
  7-9->4, A-C->2, D-E->3, F-10->2, 11->4, 12->6, 13->7, 14->8, 15-16->9,
  17-1A->5. EQGATE then maps cls 1-5 -> gate1, 6 -> gate2, 7-9 -> gate3 —
  so **gate2 means t9 == 0x12 exactly**.
- **Gate dispatch order**: gate1 -> `ae8/r14` (flag4c-gated, `row[0x1A]`/
  `row[0x1D]`); gate2 -> `a20/ad8` (flag70-gated, `row[0x18]`/`row[0x19]`);
  gate3 -> `a34/a38` (ungated).
- **FIND-miss and explicit-`rdx` skip the entire tail.** `flag64` is live:
  `kind0-find-miss-tailskip` and `kind0-rdx-tailskip` exit clean with no
  unit writes and no `X`/`A` tokens; the earlier "FIND-miss faults through
  the tail" reading is disproven.
- **VALID arm 6 tolerates a null equip table** (returns 0, no fault), while
  a null `[0x2EBF130]` def-table or null resolver base **faults** at the
  first row-field read — the harness asserts exact fault addresses
  (`kind0-tab-null`, `kind0-resb-null`, `kind0-eqtab-null`,
  `kind0-bitmask-tabnull`, `null-record`, `kind0-rcx0-rdx`).
- **`0031B8E0`-style double-RESOLVE pattern repeats**: the kind!=0 arm
  resolves four definition rows in sequence (G_DT1/2/3/4), each `R` token
  appearing twice per lookup.
- **MM3/MM2 are signed `/100` magic-multiplies** with C-style truncation
  (`kind0-neg-mm2` pins the negative-operand path).

## Mutation coverage

15 mutants, all killed (patch site -> case):

| mutant | site | kills via |
|---|---|---|
| m-eqloop-bound | `0x2FF57A` bound 5->3 | kind0-all-gates |
| m-t1-bound | `0x2FF63B` bound 0x10->8 | kind0-bitmask |
| m-t3-bound | `0x2FF779` bound 0x0C->8 | kind0-bitmask |
| m-eq-sub | `0x2FF43D` sub->add | kind0-basic-gate3 |
| m-g1-srcoff | `0x2FF498` row+0x1A->0x1B | kind0-all-gates |
| m-diffmask | `0x2FF98A` 0x8000020->0x8000040 | kind0-reset-runs |
| m-bt-bit | `0x2FF9A0` bt 0x18->0x19 | kind0-skipreset-bit24 |
| m-btr-bit | `0x2FFA10` btr 0x0E->0x0F | kind0-ba0-clear |
| m-or-flag | `0x2FFA3C` or-mask | kind0-reset-runs |
| m-788-mask | `0x2FFA1B` ~0x400->~0x800 | kind0-reset-runs |
| m-6b0-mask | `0x2FFA29` &~2->&~1 | kind0-reset-runs |
| m-cap7fff | `0x2FF7F7` 0x7FFF->0x3FFF | kind0-cap7fff |
| m-clamp63 | `0x2FF82B` 0x63->0x64 | kind0-clamps |
| m-kind-off | `0x2FEFFE` kind off +5->+4 | kind0-basic-gate3 |
| m-lvldelta | `0x2FF200` sub->add | kind1-four-rows |

## Scripted boundaries

Two sinks are scripted with argument capture (same disclosure class as
EXP-100's stubs): `003105D0` emits `X<arg>` and `00307D10` emits `A<arg>`
at their call sites; both are asserted in traces. Every other body in the
closure executes shipped bytes.

## Results

- `cases: 31/31`, `mutants: 15/15 killed` — `run.log`, `run2.log`,
  `run3.log` (three independent processes, identical results).
- `result.json` records per-case trace, out-struct bytes, unit-write fields
  and fault addresses.
- `bodies.json` records measured spans and sha256 for all 11 real bodies
  plus the two scripted boundary entries.
