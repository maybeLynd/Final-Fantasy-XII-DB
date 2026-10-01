---
experiment: EXP-098
title: Battle runtime mode composition under isolated original execution
contract: ../00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md
method: B
live_game: false
tool: evidence/battle-mode-composition-exec/check.py
---
# EXP-098 — battle-mode-composition-exec

**Status:** complete · **19/19 cases, 10/10 mutants, stable across two processes**
**Evidence:** `evidence/battle-mode-composition-exec/` (`check.py`,
`result.json`, `bodies.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-battle-runtime-mode.md`'s pilot (`diff_battle_mode.py`, 55
comparisons / 0 mismatches) ran the ladder `0030D9A0` and the predicate
`00377C20` **separately** — each with the other scripted — and the index
getter `003148F0` was "answered, not read". The contract says it plainly:
*"a scripted callee is not a proved one — what is established is each
function, not their composition."* This experiment executes the entire
composition: five bodies, ~238 bytes, **zero scripted boundaries**.

| VA | role | execution |
|---|---|---|
| `0030D9A0` | mode ladder — 5 decision points, 6 modes | **real** |
| `00377C20` | field-record bit-15 predicate | **real** |
| `003148F0` | active field index getter (`cmovs` clamp) | **real** — the pilot's scripted callee |
| `002EF2B0` | context getter (`base + 0x200`) | **real** |
| `002EF640` | context base (`0x2164280`, constant) | **real** |

Nothing is stubbed: the state pointer `[0x2EBF190]`, table pointer
`[0x2ADD100]`, and the index cell `[0x21654C4]` (a real `.data`/BSS
global — `0x2164280 + 0x200 + 0x1044`) are data, planted per case and read
by real instructions. Trace: `d` ladder entry, `P` predicate, `I` index,
`C` ctx, `G` base — the `P I C G` tail must appear iff the ladder reaches
the predicate arm.

## Executed bodies

5 bodies, spans + sha256 in `bodies.json`; `stubbed` is empty.

| VA | span | role |
|---|---|---|
| `0030D9A0` | 105 B | flags `[state+0x5B04]`: `&8`→5, `&4`→4, predicate→3, `&2`→2, else `&1` |
| `00377C20` | 78 B | `idx` vs `[tab+4]` bound, row `tab+3·idx+8` u16, `>>15` |
| `003148F0` | 27 B | `eax=[ctx+0x1044]`, `cmovs` clamps negative→0 |
| `002EF2B0` | 20 B | returns `002EF640()+0x200` |
| `002EF640` | 8 B | returns `0x2164280` |

## Fixture surface

- `STATE` at `0x40000000`; `[0x2EBF190]` → `STATE`; flags dword at
  `STATE+0x5B04` per case.
- `TAB` at `0x40100000`; `[0x2ADD100]` → `TAB` (or 0 for `tab-null`);
  count dword `TAB+4`; rows at `TAB+8`, stride 3, the tested u16 at
  `row+0` (`tab[3i+8]` lo, `tab[3i+9]` hi per the body).
- `[0x21654C4]` = the active field index (real BSS cell inside the mapped
  image). Decoy cell `[0x21653C4]` = 7 for the `m-add200` mutant.
- No TLS, no IAT involvement — the chain is call-free below the predicate.

## Findings (native-verified, composition level)

1. **The six modes compose exactly as contracted.** `flags&8`→5,
   `flags&4`→4, predicate nonzero→3, `flags&2`→2, else `flags&1`
   (0 or 1). All six observed; `m-mode5`, `m-test4`, `m-test8`,
   `m-and1` pin each arm.
2. **Priority order verified at composition level.** `m5-priority`
   (`flags=0xF`) → 5; `m4-over-low` (`0x6`) → 4; `m3-over-low`
   (`flags=0x3`, predicate true) → 3 — the predicate outranks bits 1–2.
3. **Early returns really skip the predicate chain.** `flags&8` and
   `flags&4` produce trace `d` with no `P I C G` — the callee trace is
   the proof, not a model assumption. The `m-predcall` mutant (NOP'd
   call) flips 14 cases to mode 3 — a real divergence, since stale `eax`
   holds the state pointer's low 32 bits (nonzero).
4. **The index chain is real.** `003148F0` → `002EF2B0` → `002EF640`
   resolve the index cell to `0x21654C4`: `idx-neg-clamp` drives
   `idx=-1`, `cmovs` clamps to 0, row 0 is read (mode 3); `m-cmovs`
   leaves `0xFFFFFFFF` unclamped → unsigned `jae` refuses → mode 0.
   `m-add200` (`+0x200`→`+0x100`) reads the decoy cell — divergent in 5
   cases.
5. **Bounds and table checks verified.** `idx==count` and `idx>count`
   refuse (`jae`); `idx=count-1` is the last valid row; a null table
   pointer refuses before any row read (`tab-null`); `m-jae` inverts the
   bound (in-range refuses); `m-tabnull` forces the null arm.
6. **The row test is bit 15, not "any high bit".** `row-bit14` plants
   `0x4000`: real `>>15` → 0 → mode 0; `m-shr` (`>>15`→`>>14`) answers 1.
   Row select is per-index: `idx-select` reads row 2, not row 0.
7. **Flags are re-read after the predicate call** (`0x30D9E2` reloads the
   state pointer and the flags dword) — `obs.flags_after` confirms the
   predicate does not write the state block under this fixture.
8. **High flag bits are ignored**: `flags=0x100` → mode 0; `0x108` → 5.

## Mutants (10/10 killed)

| mutant | site | semantic |
|---|---|---|
| `m-mode5` | `0x30D9B7` imm 5→6 | wrong mode constant |
| `m-test4` | `0x30D9C2` imm 4→2 | bit-4 test reads bit 2 |
| `m-predcall` | `0x30D9CF` `call` NOP×5 | predicate skipped; stale eax→mode 3 |
| `m-tabnull` | `0x377C30` `test`→`xor r8d,r8d` | table always null |
| `m-jae` | `0x377C39` `jae`→`jb` | bound inverted |
| `m-shr` | `0x377C57` imm 15→14 | bit-14 answers instead of bit-15 |
| `m-cmovs` | `0x314903` `cmovs` NOP×3 | negative index unclamped |
| `m-add200` | `0x2EF2BB` imm `0x200`→`0x100` | index read from wrong cell |
| `m-and1` | `0x30DA03` imm 1→2 | mode 0/1 answered from bit 1 |
| `m-test8` | `0x30D9B3` imm 8→4 | bit-8 flag falls to the bit-4 arm |

## Not exercised (disclosed, not claimed)

- The four mode setters (`0030DA10` writes the flags dword — visible in
  the tail bytes but not driven), the save round trip, and the 21
  consumers listed in the contract.
- The contract's queued live half (`state+0x5B04` while mounted / in a
  cutscene, `state+0x5AE4` = 180.0f on mount) — still live-only.
- No live process; this is isolated original-code execution.

## Harness notes

- All patch sites verified against shipped bytes before the first run;
  two initial sites (`m-shr`, `m-and1`) were off by one — the imm8 sits
  at insn+2 for `c1`/`83` encodings.
- The `m-shr` mutant requires a bit-14-only row to diverge — `rows`
  carries the raw u16, not a boolean, so `row-bit14` can plant `0x4000`.
- The contract's equivalent-mutant adjudication is honored: mutating the
  row's byte offsets is provably equivalent for bit-15 (the low byte
  cannot carry into it), so no such mutant is listed.
