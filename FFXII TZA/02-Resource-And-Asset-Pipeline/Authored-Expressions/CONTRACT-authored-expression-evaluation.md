---
contract: evaluate an authored two-operand expression into one integer, drawing from the procedural generator exactly as many times as the operator requires
category: 02-Resource-And-Asset-Pipeline
scope: subsystem
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md
entries: ["004314E0", "00431350", "003A6E60", "00431080", "0020E600"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the record layout, the six operator arms and the operand kinds are the page's reading with
    site citations; the scaling law, the seven-step draw cost and the scratch writes are EXP-070's
    executed results, run with NO CALLEE STUBS. OPUS assembled and scoped this contract on
    2026-09-20 and did not re-derive the bodies. RE-DERIVED 2026-09-29 (OPUS, falsification pass 1,
    falsify_authored_expression.py A0-A7) - see the end of this page.
last_reviewed: 2026-09-29
audit:
  by: OPUS
  date: 2026-09-20
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-authored-expression-falsification-pass-1
---

# Contract — authored expression evaluation

> **Provenance, stated once.** **[page]** marks the page's reading. **[EXP-070]** marks isolated
> original-code execution **with no callee stubs** — the strongest isolated class available, because
> `003A6E60` is a **leaf that calls nothing** and so runs from the shipped bytes with nothing faked.
> **[live]** marks what only a running game settles.

## 1. Purpose

A great deal of the game's authored data does not store a fixed number — it stores a small
**expression**: two operands and an operator, where the operator usually means *"take this much, plus
a random amount up to that much."* Evaluating one turns authored data into the concrete number the
game then uses.

## 2. Interface

| | |
|---|---|
| evaluate | `eval(record, context)` — `004314E0` **[page]** |
| combine | `00431350` (190 B), tail-called; `op = (rec->u16_0E >> 4) & 0xF` **[page]** |
| the draw | `f(bound)` — `003A6E60` (345 B), **a leaf, calls nothing** **[page]** |
| operand ≥ 2 | `00431080` (718 B), a piecewise curve **[page]** |
| reference fixup | `ImageAddress_ResolveRuntimePointer` (`0020E600`, 10 B) **[page]** |

## 3. Types

The record's **first fifteen bytes** are all this path reads: `+0x00` operand A payload (`u32`),
`+0x04` operand B payload (`u32`), `+0x0C` kind A (`u8`), `+0x0D` kind B (`u8`), `+0x0E` flags
(`u16`) whose **bits 4–7 are the operator** **[page]**. *(Qualified 2026-09-29, OPUS, falsification pass 1 of the contract: the operator is loaded as a `u16` at `+0x0E`,
so the path reads **sixteen** bytes, `0x00`-`0x0F`. The operator's bits 4-7 lie in the byte at `+0x0E`, so fifteen
of them decide anything.)*

## 4. Preconditions · postconditions · invariants

**I1 — three operand kinds.** `0` absent (A yields `0`; **B absent means the expression is just A**);
`1` an **authored-data reference** — resolve the payload and read the value from **`+0x04` of the
target**; `≥ 2` the piecewise-curve evaluator, called with the operand's **index** (0 for A, 1 for B)
**[page]**.

**I2 — six operators, and two of them never draw.**

| op | result | draws |
|---:|---|---|
| `0` | `a` | **none** — the operand's value is discarded, not a draw |
| `1` | `a + f(b)` | one |
| `2` | `a − f(b)` | one |
| `3` | `a − b + f(2b)` | one |
| `4` | `a × (f(b) + 1)` | one |
| `5` | `b == a ? a : a + f(b − a)` | **none when `b == a`**, else one — it *jumps into op 1's arm* |
| `> 5` | `a` | none |

**[page]**

> **THE DRAW COLUMN HOLDS ONLY FOR `b ≠ 0`** *(corrected 2026-09-29, OPUS, falsification pass 1, `CON-162`)*. The combiner
> tests `b` first (`0043135F`). With `b == 0`, ops 0-4 return `a` **without drawing**, and op 5 draws `f(−a)` only when
> `a ≠ 0` (`004313E9`-`004313FF`). The page says so; this table had dropped it. A present B whose value is 0 is the case.

**I3 — THE SCALING LAW IS `trunc(v × B − B)`, NOT `trunc((v − 1) × B)`.** The bytes never form a
fraction `u`. They advance the shared recurrence **five** steps, reinterpret the state as a binary32
`v ∈ [1, 2)`, then compute **each step rounded to binary32, in this order**: `B = (float)bound`,
`P = v * B`, `D = P − B * 1.0f`, and return `(int)D`. **The two laws differ when the products round
differently** — from seed `458DC800` the fifth-step `v` is `3FB90003` and bound 1,000,000,000
returns **445,312,896**, where the discarded law gives **445,312,864** **[EXP-070]**. *Corrected
2026-09-11 by `ASTRA-CONTRA-FABLE-RNG-ROUNDING`.*

**I4 — EVERY CALL COSTS SEVEN STEPS, INCLUDING A BOUND OF ZERO.** `f` samples after five steps and
advances **two more**; **a bound of 0 returns 0 but still consumes all seven** **[EXP-070]**.
*(2026-09-29, pass 1: true of `f`. From this evaluator a zero bound reaches `f` only through op 3 with
`b = 0x80000000`, because every other call follows a `b ≠ 0` or `b − a ≠ 0` test.)*

**I5 — THE NUMBER OF DRAWS IS PART OF THE CONTRACT.** Two identically seeded generators, one given a
single extra call, produce the same sequence **shifted by one**. So **§I2's per-operator draw counts
are load-bearing**: an implementation that draws for op 0, or draws when `b == a` under op 5,
desynchronises everything drawn afterwards — not just its own value **[page]**.

**I6 — the mode word gates the stepping, not the writes.** With `022D9138` zero **no step is taken**
and `v` is `1.0`, **but the scratch is still written** **[EXP-070]**.

**I7 — `f` is signed**, carrying the bound's sign and staying strictly inside it; **op 5 depends on
that** **[page]**.

## 5. State

The shared recurrence state at `01EF93E8`, the mode word `022D9138`, and the scratch block. **Six
writes per call, in order** **[EXP-070]**: fifth-step state → `01EF93E8`; `P` → `022D91A0`;
`D` → `022D92E0`; seventh-step state → `01EF93E8`; the seventh-step sample → `022D92F0`; and the
converted four-lane vector back over `022D92E0`–`022D92EF` — **the other three lanes are whatever
the scratch held**. *(2026-09-29, pass 1: the scratch is the VU0 register bank. `022D91A0` is ACC, `022D92E0` is vf20
and `022D92F0` is vf21, and the `1.0f` is vf00.w at `01EF93FC`; see the pass section.)*

## 6. Relationships

`0020E600` is the image-address fixup the rest of the authored pipeline uses — **not** an accessor of
this or any type. `00431080` reaches `0039B630`/`0039B6E0` for the quadratic B-spline. The recurrence
itself is specified on the RNG page **[page]**.

## 7. State transitions

None. The evaluator is a pure function of the record, the context and the generator state — but it
**advances that state**, which is why I4 and I5 exist.

## 8. Script · resource · event interactions

The record is **authored data**, and kind 1 lets an operand **point at other authored data** rather
than carry a literal **[page]**.

## 9. Determinism

**This is the determinism-critical system of the four requirements.** The value is reproducible from
the seed **only if both the arithmetic (I3) and the draw count (I4, I5) match**. Note the asymmetry:
a wrong rounding law corrupts one value; **a wrong draw count corrupts every value after it**.

## 10. Failure paths and edge conditions

* **Operator > 5** behaves as op 0 — returns `a`, no draw (I2).
* **Bound 0** → 0, **seven steps still consumed** (I4).
* **Mode word zero** → no stepping, `v = 1.0`, **scratch still written** (I6).
* **`b == a` under op 5** → `a` with **no draw** (I2, I5).
* **`b == 0`** → ops 0-4 return `a` with **no draw**; op 5 draws `f(−a)` when `a ≠ 0` *(2026-09-29, pass 1, `CON-162`)*.
* **Kinds 2 and 3 of the curve evaluator return 0**; a value past the last point returns the last
  `y`; ~~three points or fewer~~ two points or fewer fall back to linear *(corrected 2026-10-02, OPUS: `00431080+0xA1` `cmp al, 2` / `00431080+0xA3` `jbe` send a point count of two or fewer to the linear path, so three points already take the spline; the kinds 2 and 3 above are the operand's two-bit curve selector, `00431080+0x93`)* **[page]**.

## 11. Observable behaviour

Authored ranges come out as concrete numbers — damage spreads, timings, quantities. A desynchronised
draw count shows up as *everything random after this point differs*, which is why I5 matters more
than it looks.

## 12. Reproduction formula

```c
int f(int bound) {                 /* 003A6E60 - a leaf */
    advance(5);
    float v = as_float(state);     /* binary32, in [1,2) */
    float B = (float)bound;
    float P = v * B;               /* binary32 */
    float D = P - B * 1.0f;        /* binary32, THIS ORDER */
    advance(2);                    /* even when bound == 0 */
    return (int)D;                 /* truncate */
}
```

**Do not simplify `P - B*1.0f` to `(v-1)*B`.** They are algebraically equal and **numerically
different**, and I3 gives a fixture where they differ. **Do not skip the two trailing steps** on the
zero-bound path.

## 13. Runtime validation

**Isolated original-code, NO CALLEE STUBS — the strongest isolated evidence in this set.**
`EXP-070` (COMPLETE, method B, `live_game: false`) executed **two complete original procedural RNG
helpers with synthetic state and a controlled MXCSR**, its own `execution_scope` recording **"no
stubs"** and **"failed fixtures and rounding corrections preserved"**. It establishes I3's fixture,
I4's zero-bound cost, I6's mode-word behaviour and the six scratch writes of §5 **[EXP-070]**.

The earlier simpler law was additionally falsification-tested: `u` recovered to ~31 bits from the
widest bound, then used to **predict** thirteen other bounds from the same seed — **780 of 780** —
which held only because none of those bounds sat on a rounding boundary **[page]**.

**LINKED — ASTRA accepted the match, and the pair now agrees in both directions.** This paragraph
previously read *"UNLINKED, and this one has a clean fix rather than an exemption"* and waited on the
author's decision. The decision came back accepted (`ASTRA-RETURN-OPUS-EXP070-BOUNDED-LINK`,
consumed here 2026-09-20 by OPUS) and **has already landed**: commit `16eda50ed` replaces EXP-070's
`contract: none` with this document and rewrites its `contract_coverage` to bound it —
*"Bounded isolated evidence for the procedural helpers' rounding, seven-step cost, mode behaviour
and scratch writes; **not** the full expression evaluator, initialization, live ordering or scratch
ownership."* `check_contract_runtime_links.py` no longer reports this pair.

**Two things verified rather than taken on report.** ASTRA's return said *"publication is pending the
legitimate shared slot, so do not claim my new commit exists yet"* — **it has since landed**, which is
why this paragraph states it. But **the blob ASTRA named as reviewed, `0347f85c…`, is not an object
in this repository**; what is committed hashes to `e2d47e7d…`. So the *decision* is confirmed from
the tree and the *reviewed artifact* is not the one in it, and the second half is recorded rather
than smoothed over. Separately, ASTRA's note claims this contract *"now cites these exact
procedural-helper results in §13"* — **it does**: the paragraph above attributes I3's fixture, I4's
zero-bound cost, I6's mode-word behaviour and the six scratch writes of §5 to `EXP-070`, which is the
same four things its `contract_coverage` now bounds it to.

**Nothing in this contract's scope moved.** The link records where the evidence belongs; it adds no
execution, no fixture and no observation. EXP-070 remains `live_game: false` with a **controlled
MXCSR**, and §14's *"No observation of the running game"* stands unchanged.

**One thing the link cannot fix, and it is a property of the schema rather than a defect.** EXP-070
is cited by **two** contracts — this one and
[`CONTRACT-which-generator-serves-which-roll.md`](../../21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md)
— and an experiment's `contract:` key is **single-valued**, so it can only ever name one of them.
The checker therefore still reports that second pair as `ONE-WAY` and **always will**. That row is
neither contract's error and must not be "fixed" by inventing a second link or by adding an
exemption to hide it.

## 14. Unresolved

* **The other ~~eleven~~ eight bits of `+0x0E`** — only bits 4–7 are the operator *(answered in part: bits 0–3 are the A and B curve selectors, `00431080+0x47` and `+0x4D`; 2026-10-02, OPUS)* **[page]**.
* **What the record is part of, and who authors it** **[page]**.
* **Whether this stream is used outside Presentation** — 96 of 99 callers are Presentation-owned,
  3 untagged and **not read** **[page]**.
* **Live draw order, the complete consumer census, and shared-scratch ownership** are outside
  EXP-070's evidence, by its own statement **[EXP-070]**.
* **No observation of the running game** **[live]**.

## 15. Evidence

The record layout, the operand kinds, the six arms and the falsification history are the page's
**[page]**; the rounding law, the seven-step cost, the mode-word behaviour and the scratch writes are
EXP-070's, executed with no stubs **[EXP-070]**. This contract's contribution is I1–I7 stated as a
contract, §9's asymmetry between a wrong law and a wrong count, and §12's two explicit "do not"s.

## 16. Parity plan

Seed the recurrence, then for each operator evaluate a record and compare **both the returned value
and the generator state afterwards**. **The state comparison is the test that matters** — a
reimplementation with the right arithmetic and the wrong draw count passes every value check in
isolation and fails the first time two expressions are evaluated in sequence. Include the
**zero-bound** case (I4) and the **`b == a` op-5** case (I2), which are exactly where a plausible
implementation skips steps.

`002FC200` (313 B) is the 48-slot freelist init `00259180` calls: `0036C1D0(8, 0xA)` gate, then 48 records at 0x38 stride from `02EC32E0` are zeroed (6 qwords), tagged `dword[-0x28] = (i & 0x3F) | bit28`, and linked `rax` -> `02EC32E0 + (i+1)*0x38`; `02EC3D70` takes the head, `02EC3D60`/`+0x18`/`+0x1C` clear, `0024C460` runs and `00861EC0` registers `02EC19C0` - the evaluation pool's free-list build.

Interior anchor `002FC25E` (function `002FC200`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7-167, 2026-09-23)

**CoreRuntimeScheduling — CLIENT (SWE2-EC7-167, 1 edge).** `00259180` — the caller of this
page's `002FC200` freelist init — is itself called by `0022A0B0`, owned by that layer: the
evaluation-pool build is reached from the runtime scheduler's side. One client edge; the pool
belongs to the expression evaluator, not the scheduler.

**Presentation — CLIENT and SERVICE (SWE2-EC7-169, 128 edges).** This page's cited
subjects are reached from the presentation layer (`00537FF0`/`005383B0` calling
`0039B630`, `003A69F0`/`00422560`-side callers of `003A6E60` among 128 edges), and the
newly measured `003D8C30` registers each `02B4E3xx` range through `0050C450`, which
itself calls `00500470` of that layer - the pool init both serves and consumes
presentation machinery; the table remains evaluator-owned.

`003D8C30` (298 B) is the pointer-table init `00259180` runs: four image-relative ranges (`+0x1DDE510`, `+0x1DDE3A0`, `+0x1DDE690`, `+0x1DDE810` from `00120000`) store at `02B4E3D0`/`02B4E3D8`/`02B4E3E0`/`02B4E3E8` with `dword[range+8] + range+0x10` fixups, each registered through `0050C450`; then `02B4D7B8` takes `1.0f`, `02B4D7A1`/`02B4D7A0`/`02B4D7A8`/`02B4D7B0`/`02B4D7A4` clear, and 32 records at `02B4E374` walk down 0x60 each with `dword[0]` zeroed - the evaluation pool's table publish `002FC200`'s freelist sits beside.

Interior anchor `003D8CD7` (function `003D8C30`).

`00259250` (271 B) is the `02096xxx` state-block reset `00259180` runs beside `003D8C30`'s table publish: `020968A0` takes the zero xmmword, `020968BC` takes `0.5f`, `020968C8` keeps `(b & 0xF5) | 5`, `02096C60` drops bit 0; `02096884`/`0209688E`/`02096892`/`02096896` fill `0x1011000`/`0`/`0x200`/`0x8040`, `020968B0`/`020968B4` take `0x80808080`/`0x80000080`, `020968B8` takes 1, `02096810`/`+14`/`+18` take `1.0f` x3, and `020969F0`..`02096A08`, `02096B3C`/`02096B40`, `02096BA0`/`02096BA8`, `02096C78`, `02096D21`, `02096844`/`0209688C`/`020968EE`/`020968EC` clear while `02096D28` sets 1 - the evaluation pool's working-state init.

Interior anchor `00259295` (function `00259250`).

## Falsification pass 1 — 2026-09-29 (OPUS): I2's draw column refuted for b == 0; the bodies re-derived

**Attack.** The frontmatter said the bodies were never re-derived. This pass derives them. Every clause of §2-§10 became a
check that fails if the shipping image says otherwise. The checks decode every listed body in `.text`. Script:
`Tools/analysis-kit/gfz-scripts/falsify_authored_expression.py`, output `falsify_authored_expression.out`, image `73461d08…`,
0 BROKEN.

| # | Clause attacked | Killer | Result |
|---|---|---|---|
| A0 | §2 sizes, the tail call, `f` a leaf | another size, a call in `f` | **survives**: 190 / 345 / 718 / 10 B; `004314E0` tail-jumps at `0043156E`; `f` calls nothing |
| A1 | I1 the three operand kinds | another read | **survives**: kind bytes `+0x0C`/`+0x0D`; kind 1 reads `[target + 4]`; curve index 0 / 1; B absent returns A |
| A2 | I2 the six arms for b ≠ 0 | another arm | **survives**: table `00431401`, `00431390`, `004313A4`, `004313BA`, `004313D2`, `004313FD`; op > 5 returns a |
| A3 | I2's draw column (ops 1-4 "one") | an f call on the b == 0 path | **REFUTED** (below) |
| A4 | I4 in context | a zero bound reachable from the combiner | **made exact** (below) |
| A5 | I3 / I4 / I6 inside `f` | another step count, gate or order | **survives**: seven steps, five before the first store; both blocks gated on `022D9138`; `P = v·B`, then `B·[01EF93FC]`, then `P − B·1` |
| A6 | §5 the six writes | another order or cell | **survives**, and the cells have names (below) |
| A7 | §3 "the first fifteen bytes" | a read past `+0x0E` | **made exact**: sixteen are loaded, fifteen matter (§3) |

* **A3: with `b == 0` the combiner draws for op 5 only.** `00431350` tests `b` before it dispatches
  (`test r8d, r8d / je 004313E9`). The zero-`b` path re-reads the operator:
  * op 4, and every op other than 5, returns `a` without calling `f`;
  * op 5 computes `0 − a` and draws `f(−a)` only when that is non-zero.

  I2's table gave ops 1-4 one draw each, unconditionally. I5 says the draw count is load-bearing, so an implementation
  that followed the table would draw once too often for every present B operand whose value is 0, and every draw after
  it would shift. [The page](how-an-authored-number-gets-its-randomness.md) states the zero-`b` path correctly ("only op 5
  survives it"); the contract lost it when it carried the table. `CON-162`.
* **A4: `f(0)` is almost unreachable from here.** The combiner's four calls take `b` (ops 1, 2 and 4), `2b` (op 3) or
  `b − a` (op 5 and the zero-`b` path). Each is made only after `b ≠ 0` or `b − a ≠ 0` was established. So a zero bound
  reaches `f` from this path only through op 3 with `b = 0x80000000`, where `2b` wraps to 0. I4's seven-step cost of a
  zero bound is true of `f`, which has 97 call sites. It is not something this evaluator ordinarily pays.
* **A6: the "scratch block" is the VU0 register bank** of [the shared transform workbench](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md):
  * `P` goes to **ACC.x** (`022D91A0`), `D` to **vf20.x** (`022D92E0`), and the seventh-step sample to **vf21.x**
    (`022D92F0`);
  * the converted vector goes back over **vf20**;
  * the `1.0f` in `P − B · 1.0f` is **vf00.w** (`01EF93FC`). Its two writers, the bank's start-up `0036D990` and its
    clear `0036D9E0`, both store the `.rdata` 1.0 at `01CEBBA8`.

  So `f` is emulated vector-unit code: five random steps, `MUL`, `MUL` by `vf00.w`, `SUB`, two more steps, then `FTOI0`.
  Any other workbench user that holds a value in ACC, vf20 or vf21 across a call to `f` loses it.

Consumer record: [`_index/candidates/authored-expression-falsification-pass-1-0929/`](../../_index/candidates/authored-expression-falsification-pass-1-0929/README.md).
Contradiction: `CON-162`.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-contract-authored-expression-evaluation-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0039B6E0` | 147 B | with `t` = `xmm0` and floats `a` = `[rdx]`, `b` = `[rdx+0x10]`, `c` = `[rdx+0x20]`: forms `A` = `a` - (`b` + `b`) + `c`; when `A` compares equal to 0.0 (ordered, so not NaN) it stores 2.0 (0x40000000) to dword `[r8]`; otherwise (unordered included) it stores (`sqrtf`((`b` - `a`)^2 - (`a` + `b` - 2`t`)*`A`) - (`b` - `a`)) / `A` there, `sqrtf` through the CRT thunk `00861F14`; returns nothing | `0039B715`, `0039B725`, `0039B72C`, `0039B752`, `0039B760` |
