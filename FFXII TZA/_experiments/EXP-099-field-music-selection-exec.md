---
experiment: EXP-099
title: Field music selection under isolated original execution
contract: ../18-Audio/CONTRACT-field-music-selection.md
method: B
live_game: false
tool: evidence/field-music-selection-exec/check.py
---
# EXP-099 — field-music-selection-exec

**Status:** complete · **22/22 cases, 10/10 mutants, stable across two processes**
**Evidence:** `evidence/field-music-selection-exec/` (`check.py`,
`result.json`, `bodies.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-field-music-selection.md`'s pilot ran `003EAA70` (229 B) with its
only callee — `FieldData_GetVariable0` (`00265270`) — stubbed at its own
address as `mov eax,imm; ret`. This experiment runs the callee from shipped
bytes, so its two refusal gates produce the progress value the ladder
actually sees. Nothing else is scripted: the callee is a leaf.

| VA | role | execution |
|---|---|---|
| `003EAA70` | music-selection ladder | **real** |
| `00265270` | `FieldData_GetVariable0` | **real** |

Trace: `m` subject entry, `V` callee entry — the callee fires on every
path including refusals (it is called *before* the bound check).

## Executed bodies

2 bodies, spans + sha256 in `bodies.json`; `stubbed` is empty.

| VA | span | role |
|---|---|---|
| `003EAA70` | 229 B | bound check → signed page index → run-chain walk → threshold ladder |
| `00265270` | 28 B | liveness gate → varblock pointer gate → `movzx u16` |

## Fixture surface

- Callee gates: liveness byte `[0x2098E20]` bit 0 (the ActorManager slot-0
  byte — same cell EXP-096 measured), varblock pointer `[0x2098E58]`,
  u16 progress at `varblock+0`.
- Table `[0x2B5E0D0]` → `TAB`: bound dword `+4`, page pointers at `+8+4·i`
  as **sign-extended 32-bit absolute addresses** (`movsxd`).
- Page = run chain; header 4 B `{u16 start | len<<11, u8 nEntries,
  u8 default}` then `nEntries` × 3 B `{u16 threshold, u8 value}`.
- Next header at `+4 + 3·nEntries`.

## Findings (native-verified)

1. **The callee's gates compose as progress-0, not refusal.** A dead
   actor (`liveness&1 == 0`) or a null varblock pointer returns 0 from
   `00265270`, and the ladder still runs — progress 0 compares `≤` any
   threshold and answers the run's default byte (`dead-actor`,
   `varblock-null` both return the planted default with `progress=50`
   unread).
2. **Bound check:** `[tab+4] < arg` refuses with −1 before any page read;
   `arg == bound` proceeds (`arg-eq-bound`; `m-bound-jl` `jl`→`jle`
   killed).
3. **Page index is a biased signed `arg/128`** (`cdq; and edx,0x7F;
   add; sar 7`) and the pointer is a sign-extended dword; null page → −1
   (`page-null`; `m-page-sar` killed by `page1`/`start-high`).
4. **Run coverage is inclusive on both ends.** `start > arg` refuses;
   `arg ≤ start+len` enters the ladder — `run-boundary` proves `arg ==
   start+len` still matches the run (the `jae` at `0x3EAAC9`), and
   `start-eq-arg` proves `start == arg` proceeds (`ja` at `0x3EAAC3`).
   `run-gap` refuses on a hole between runs.
5. **The ladder takes the last threshold passed, sign-extended.** The
   u16 result is `movsx`'d to signed at `0x3EAB10` *after* zero-extension
   at entry: `0xFFFF`/`0x8000` progress never passes a threshold
   (`neg-progress`, `neg-prog-8000` → default); equal threshold stops
   (`thr-eq`; `m-thr-jle` killed); `m-movsx` flips negative progress
   positive.
6. **Result 0 maps to −1** via `cmove` at `0x3EAB48` (`zero-result`;
   `m-cmove` killed).
7. **Stride advance verified.** `4 + 3·nEntries` (`run-second`,
   `run-after`; `m-stride` kills the `lea` scale ×2→×1).
8. **The 11-bit start field carries values ≥ 0x400** (`start-high`:
   `start=0x400`, `arg=0x405`, page 8 → 0x55; `m-start-mask` `0x7FF`→
   `0x3FF` killed — patch site corrected from `0x3EABBE` to `0x3EAABE`,
   the imm's second byte).

## Mutants (10/10 killed)

| mutant | site | semantic |
|---|---|---|
| `m-bound-jl` | `0x3EAA8C` `jl`→`jle` | arg==bound refuses |
| `m-page-sar` | `0x3EAA98` `sar 7`→`6` | wrong page granularity |
| `m-start-mask` | `0x3EAABE` `0x7FF`→`0x3FF` | start field mis-reads |
| `m-start-ja` | `0x3EAAC3` `ja`→`jae` | start==arg refuses |
| `m-run-jae` | `0x3EAAC9` `jae`→`jb` | matching arg walks past |
| `m-stride` | `0x3EAAD2` SIB `0x52`→`0x12` | next-header offset wrong |
| `m-thr-jle` | `0x3EAB2F` `jle`→`jl` | equal threshold takes entry |
| `m-movsx` | `0x3EAB12` `movsx`→`movzx` | progress not sign-extended |
| `m-cmove` | `0x3EAB49` `cmove`→`cmovne` | result 0 leaks instead of −1 |
| `m-live-bit` | `0x265276` imm `1`→`2` | liveness reads bit 2 |

## Not exercised (disclosed, not claimed)

- The `musicctrl.bin` loader (`0051ED10(9, 0x20, 003EAB90)` →
  `0x2B5E0D0`) — the table arrives as a fixture, not from a real load.
- The four callers (`0025D9E0`/`00261F90`/`0026DE20`/`0026DEF0`) and the
  selected music's downstream use.
- Negative `arg` (page index sign-extends negative — reads below the
  table) — out of contract scope, undisclosed.
- No live process, no audible result.

## Harness notes

- The contract's prose was right about sign extension *at* `0x3EAB10`
  (not at the call site) — verified by `m-movsx`.
- `run-boundary` caught a model error: the run's upper bound is
  **inclusive** (`jae` into the ladder), not exclusive as first written.
- `len` is a 5-bit field — max run length 31.

## Owner qualification - the 'dead-actor' case is a supplied manager gate (SWE2-ORACLE, 2026-09-30)

Answers `ASTRA-RETURN-ORACLE-FIELD-MUSIC-GATE-SCOPE`.
- **The `dead-actor` case above involves no actor death and no death event.** It plants ActorManager slot 0 with flag 0
  and progress 50. The getter's zero comes from its fixed global gate (slot 0's live bit) or a null variable bank.
- **Read it as "supplied disabled manager gate".** It shows no normal death consequence and no audio consequence.
- **Sources.** ASTRA's scope control is `338deae9d` (`_experiments/evidence/field-music-gate-scope/`), reviewed by
  `ASTRA-REVIEW-FIELD-MUSIC-GATE-SCOPE`. The contract correction is OPUS `4166742bd`.
- **What stands.** The raw 22/20 results, the labels and the 10/10 mutant kills are unchanged.
