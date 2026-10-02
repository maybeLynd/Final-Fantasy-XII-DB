# RC-5 item 1: does any counter increment run twice between its resets? (FABLE, 2026-10-02)

Static; shipped bytecode only. Run at HEAD `871706705`. This record edits no page and no register row.

## The question

ORACLE's record [`rc5b-event-slot-residue-0930`](../rc5b-event-slot-residue-0930/README.md) ("Item 1") bounds the
variable operands of three event-slot verbs as counters:
- 3,429 `startscene` operands;
- 45 `startscene_4b3` operands;
- 4 counter-kind `eventread_e8` operands.

A counter is a file variable that is only set to constants or advanced by `x = x + k`. ORACLE puts its values in
[smallest constant, largest constant + the file's total increments]. The record's "Not claimed" names the premise this
needs: each increment runs once per pass through its code, and no loop check was run.

This record asks, for every counter variable that feeds one of those operands, whether an increment can execute more
than once between the stores that bound it:
- **(a) a loop.** Is the increment on a cycle of the control-flow graph, through the actor's jump table?
- **(b) re-entry.** Is the increment dominated, within its own function, by a constant store (a reset) of the same
  variable? If it is not, the variable carries over between invocations.

It then asks whether the bound still holds, and corrects it where it does not.

## Method

[`rc5c_loops.py`](rc5c_loops.py) produces [`rc5c_loops.out`](rc5c_loops.out) and two tables:
- [`rc5c_increments.tsv`](rc5c_increments.tsv): one row per counter increment site, in all copies;
- [`rc5c_sites.tsv`](rc5c_sites.tsv): one row per operand site, with ORACLE's interval and the corrected one.

The script reports `FAILS 0`. Run it from the repo root; it takes about four minutes.

**The walk is ORACLE's.** The per-file loop, descriptor decode, increment idiom, store table, `domain()` and
`classify()` are copied unchanged from [`rc5b_operands.py`](../rc5b-event-slot-residue-0930/rc5b_operands.py). They are
copied, not imported, because importing that script runs it and rewrites its `.tsv`. The walk uses the kit decoder
`gen_req_channel_census.py`. Only each actor's function table and jump table were added: directory entry `+0x10` and
`+0x14`, BW-5, [section-000 §4](../../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md).

**Control flow.** Opcode semantics are from the handler table in
[`consumer-before.md`](../../../_experiments/evidence/script-division-unordered-guard/retained/consumer-before.md) and
[the interpreter page](../../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md).
- A JMP-family immediate indexes the actor's jump table, which holds an offset within the actor's code.
- Unconditional jumps: `0x51 JMP`, `0x60 JMPINTERNAL`, `0x5A POPXJMP`.
- Conditional jumps: `0x52`–`0x57`, `0x5B POPXCJMP`, `0x5C POPXNCJMP`.
- No successor: `RET`, `RETN`, `RETT`, `RETTN`.
- `DRET` is inert and falls through. A `CALL` that yields repeats only itself.

The graph spans the whole actor, not a body cut at the next function offset. So the two defects that
[the OV-16 review](../auditsem-review-ov16m-0930/REVIEW.md) F1 found, out-of-body jumps and fall-through, are followed
rather than lost. They are still counted for the functions that hold an increment (C5 and the containment lines).

**Per increment** (the `POPV` of `x = x + k`), with R = the constant stores of the same variable in the same actor:
- **any cycle:** the increment lies on a cycle.
- **literal span:** the brief's test. Inside the cut body, a jump source after the increment targets a point at or
  before it.
- **reset-free cycle:** the increment lies on a cycle that avoids R. Only this lets it run twice between resets; a loop
  that re-runs the reset re-bounds the variable on every lap.
- **undominated:** the increment can be reached from its own function's entry without passing R. The script also tests
  reach from any function entry of the actor.

**Per operand site:** the script recomputes ORACLE's interval, then corrects it.
- The declared value of a class-1 variable joins the interval when an increment, or the read itself, can run before any
  store. The declared value is in the image's file-variable area, header `+0x38`.
- An increment on a reset-free cycle makes the upper end fail. Only the store's width clamp then bounds the value
  ([storage classes §2.2](../../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)).

## Controls

All controls pass.

| id | what | result |
|---|---|---|
| C0 | ORACLE's populations reproduce | 3,429 `startscene` variable operands = 3,141 constant+increment + 288 increment-only; 45 `startscene_4b3`; 4 counter `eventread_e8` |
| C1, C2 | ORACLE's own controls | 34,125 `startscene` sites; 0 illegal descriptors |
| C3 | synthetic bytecode, same functions | straight reset-then-increment: no loop, dominated. Increment under a backward `JMP`: reset-free loop, undominated. A loop that re-runs its reset: a loop, but not reset-free. Increment-then-reset: undominated |
| C4 | the detector fires on shipped code | 1,510,427 backward JMP-family edges in 87,464 of 223,532 actors. An I-register `for` loop is located: `bhm_a0200` `Camera`/`cut004`, a backward jump at `+12C` to `+D0` over `PUSHI0 PUSHII OPLSE POPXNCJMP …`. Over every `x = x + k` in the us copy, 8,540 of 31,600 increments lie on a reset-free cycle, for example the `sav_a01` gauge functions. A zero on the counters is therefore not a blind detector |
| C5 | containment | every JMP-family index resolves to an instruction boundary of its actor: 0 unresolved |

## Result

**(a) holds for every counter except one.** No increment that feeds the 45 `startscene_4b3` operands, or the 3,141
constant+increment `startscene` operands, lies on a loop. One increment-only `startscene` variable does: `str_z0000`,
9 sites, one per copy. Its upper bound fails.

**(b) holds for most.** Every `startscene_4b3` increment is dominated by a reset. For `startscene`:
- 252 of 270 constant+increment variables (all but 2 distinct) are dominated;
- the 2 that are not make ORACLE's lower end wrong for 603 sites;
- the 6 increment-only variables have no reset at all.

**The 4 counter `eventread_e8` operands are not counters (F1).**

The counts are over all language copies; each variable appears in 9 copies.

| class | operand sites | variables (distinct) | increments | reset-free loop | undominated increments | bound |
|---|---:|---:|---:|---:|---:|---|
| `startscene` constant+increment | 3,141 | 270 (30) | 2,880 | **0** | 72, in 18 (2) variables | holds for 2,538 sites. For 603 sites the lower end fails: see below |
| `startscene` increment-only | 288 | 54 (6) | 279 | **9** (1 variable) | 279 (no reset exists) | holds for 279 sites if each function runs once per image load. **Fails for 9 sites**: see below |
| `startscene_4b3` | 45 | 36 (4) | 882 | 0 | 0 | **holds** |
| `eventread_e8` "counter" | 4 | 2 (1) array + 2 (1) index | 2 | 2, on the index | 0 | **not a counter** (F1) |

No cut body that holds a counter increment jumps out or falls through. Every increment is reachable from its own
function's entry.

### (a) The one loop: `str_z0000` `監督`/`main`, class-1 `+0x2a` (s8, declared 0)

- **The loop.** The increment at `+2B1` is followed by `startscene(x)` at `+2B7`.
  - If the first menu's answer was 3, the script asks a second menu at `+2D3`.
  - Answer 0 there takes the jump at `+2E0` back to `+25`, the top of the event.
  - Each lap plays the next scene.
- **The trip count is the player's.** It is set by menu choices, not by a static guard.
- **Corrected bound:** [0, 127]. The site always reads after an increment, so in practice the value is at least 1.
  The upper end is set only by the s8 store's saturation at 127. ORACLE's "initial value plus up to 1" fails for
  these 9 sites.
- **Effect on ORACLE's summary.** ORACLE's overall `startscene` counter range of 0 to 102 widens to 0 to 127 for this
  one variable.

The other increment-only hits are not loops:
- the literal test flags 18, against 9 real cycles;
- the extra 9 are `rwg_a0181` `+27C`;
- there, the backward jumps are a switch dispatch (`+31D`–`+326` → `+317` → `+1C6`), whose case body exits forward to
  `+32C`.

So the literal span test over-reports. The reset-free-cycle test is the one this record uses.

### (b) Undominated increments: the lower end ignored the declared value

| file | variable | where | ORACLE | corrected | sites |
|---|---|---|---|---|---:|
| `gil_a0200` | class-1 `+0x13`, s8, declared 0 | `監督`/`main`: five increments (`+2B6`, `+333`, `+374`, `+3E6`, `+4E8`) run before the only constant store (5, at `+90D`); eight follow it (`+9C2` … `+C56`). On the straight-line pass the 14 reads see 1 to 5, then 5, then 6 to 13 | [5, 18] | **[0, 18]** | 126 |
| `dgl_g0100` | class-1 `+0x18`, s16, declared 0 | `カメラ`/`開始c58`: increments at `+418`, `+492` and `+4C1`, in an actor with no reset. The resets (7 … 49) are all in `監督`/`main` | [7, 102] | **[0, 102]** | 477 |

- **`gil_a0200` is a certain failure.** The values 1 to 4 lie below ORACLE's lower end on the straight-line first pass.
- **`dgl_g0100` is a sound static bound, not a demonstrated failure.** The tight bound [7, 102] holds only if
  `開始c58` runs after the director's first reset. That is a run-time order.
- **The upper ends stand only under one condition.** Each function that holds an undominated increment must run at most
  once between resets, or, with no reset at all, at most once per image load. This record does not settle that; it is
  the one run-time premise left.
  - For the 6 increment-only variables, those functions are `main` of `監督` or `読込監督`.
  - For the 2 variables above, they are `main` and `開始c58`.
  - Class-1 storage lives in the loaded image, so the variable returns to its declared value when the image reloads.

Only 9 operand reads can be reached before any store of their variable: `rwg_a0181` `監督`/`main` `+226`, one per
copy. It comes before that function's only increment, at `+27C`, and reads the declared value 0. That is already
ORACLE's lower end there.

### F1 (finding): the 4 `eventread_e8` "counters" are array indices

- **The image.** `POPV`'s store helper `00267E60` calls the resolver `00262440` first, at `00267E7F`; the resolver pops
  one index per array dimension. Only then does the helper pop the value: count load, decrement and store at
  `00267E9C`, `00267EA2` and `00267EA7`. So for an array `POPV` the stack top is the **index**.
- **ORACLE's resolver.** It takes the stack top as the value stored.
- **The bytecode.** The four operands read elements 0 and 1 of `evctrl.ebp`'s array class-7 `+0x1c50`. There are 4
  stores to that array:
  - `メニュー`/`callmenu` `+15CF` and `+15D8` store the constant 0;
  - `シナリオイベント`/`メニュー表示` `+4EB` and `ボスイベント`/`メニュー表示` `+233` store class-1 `+0x8dc` **at
    index** class-1 `+0x904`.
- **So [0, 3] is the range of the index `+0x904`, not of the operand.** That index is the variable on the loop: the
  menu-page loop in `callmenu` (`+1527` … `+167D`, increment at `+15F7`). That loop is guarded: it leaves when the
  index is at least 2, and the reset at `+1518` re-arms it.
- **The operand's value.** It is 0, or the value of `+0x8dc`. `+0x8dc` has no scalar `POPV` anywhere in the file, and
  its declared value is 0. ORACLE's own rows classify its direct `eventread_e8` uses as "initial value only".

## Not claimed (limits)

- **Re-entry.** This record does not show that a function holding an undominated increment runs once per reset, or
  once per image load. Request (`REQ`-family) targets were not resolved. That is the run-time premise named above.
- **Concurrency.** The graph models one execution context. Two contexts running the same increment site between two
  resets are outside it. That needs the same function active on two actors at once.
- **Element aliasing.** Class-7 element stores whose flattened address overlaps a counter or `+0x8dc` are not checked.
  ORACLE keys array stores by their header offset.
- **ORACLE's other class-7 domains.** F1's mis-read applies to any domain ORACLE drew from an array `POPV`. Examples are
  the "initialiser elements" of `file_var_s1_5`, `s1_7` and `s7_1` in its Item 1. Those were not re-run here; this is
  a lead for ORACLE.
- **Retail reachability.** It is not claimed for `str_z0000`'s repeat menu, nor for `evctrl`, which RC-5 already
  caveats as a debug controller.

## FABLE's own re-read of the stack order (FABLE, 2026-10-02)

F1 turns on the order of pops in an array `POPV`, so FABLE re-read it in the shipping image before publishing. The store
helper `00267E60` calls the resolver `00262440` at `00267E7F` with the stack object still in `r8`. The resolver keeps it
in `r14` (`00262467`), loads its count `[r14]` (`002624D2`), decrements it (`002624DC`) and stores it back
(`002624E1`): that is the index pop. Only after the call does `00267E60` load, decrement and store the same count
(`00267E9C`, `00267EA2`, `00267EA7`) for the value. **So for an array `POPV` the top of the stack is the index.**

## Consumer check and routing (FABLE)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

- consumer: register row RC-5: revised-here (a dated narrowing appended to the OPEN cell; the round-3 text is kept as
  history; the row stays OPEN).
- consumer: ORACLE's [`rc5b-event-slot-residue-0930`](../rc5b-event-slot-residue-0930/README.md) operand resolver:
  routed-to-SWE2-ORACLE. Its array `POPV` reading takes the stack top as the value; every array domain it reports
  (the round-3 "array reads clamp to initialiser elements" for `eventread_e8`) needs a re-run with the index popped
  first. FABLE does not edit ORACLE's record.
- consumer: SWE2-CONTRACT's round-3 narrowing and its proposed ANSWERED disposition: routed-to-SWE2-CONTRACT. The
  proposal rested on the counter bounds and the array domains; both need the corrections here first.
- review: FABLE authored this record; it goes to SWE2-AUDIT-SEM for a non-author verdict.
- regression: run: [`rc5c_loops.py`](rc5c_loops.py) at 871706705 (controls PASS, FAILS 0).
