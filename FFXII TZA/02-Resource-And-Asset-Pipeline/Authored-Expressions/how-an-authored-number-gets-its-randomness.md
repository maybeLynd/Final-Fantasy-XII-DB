---
system: How an authored number gets its randomness — the two-operand expression evaluator
category: 02-Resource-And-Asset-Pipeline
status: AUDITED — the expression record, its operator, the random draw and every operand kind read; kinds >= 2 (00431080: a piecewise curve over (x, y) pairs, linear or quadratic B-spline, with a period) read 2026-09-18
owner_layer: unowned in the ledger — filed here for what it does, not for who calls it
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 60 addresses cited - 11 data, 13 entry, 34 interior, 1 literal, 1 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-authored-randomness-pass-1
  crossref_clean: true
  reopened_count: 0
---

# How an authored number gets its randomness

## 1. What the player sees

Two casts of the same spell do not look identical. Sparks fly at slightly different angles, embers
last slightly different lengths of time, a flame flickers on its own schedule. **Almost nothing
authored about how an effect *looks* is a flat number** — it is a number with a spread, authored
beside it, and rolled fresh every time.

This page is the machinery that turns *"about this much, give or take that much"* into an actual
value. One small record, two operands, and a four-bit code saying how to put them together.

> ### Which randomness this is — read this before using the page
>
> **This is the render-local stream, not the gameplay one.** The draw behind these expressions
> (`003A6E60`) runs on the **shared procedural recurrence** at `01EF93E8`, which
> [RNG streams](../../21-RNG-And-Determinism/rng-streams.md) documents as *"render-local"* and warns
> must **never** be treated as world RNG.
>
> Consistently, **96 of the evaluator's 99 callers are Presentation-owned** in the function ledger
> (3 untagged, 0 in any other owner category).
>
> So this is **not** where damage variance, gil amounts or drop rolls come from. Those are on other
> streams — see [which roll is on which
> generator](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md). For a mod or a
> multiplayer build the practical consequence is that **two clients may legitimately disagree on
> every number on this page** while agreeing exactly on the fight.
>
> *(Corrected 2026-09-08. This section originally opened with damage, gil and chest contents. That
> was wrong — it attributed gameplay rolls to a render-local generator. The error and how it was
> caught are recorded in `PROGRAM-STATE.md` §4bs.)*

## 2. Why this function

A whole-binary ranking of functions **no document cites**, ordered by distinct non-EH callers, puts
`004314E0` at the top with **99**. Three of its neighbours are in the same top twelve — `004309C0`
(89), `00430B90` (78), `004304F0` (64) — so roughly 330 call sites sit in one small address range
with nothing written about any of it.

*(`check_already_answered.py` reported "no existing coverage found" for all four before this block
started.)*

> **That check was run on the four functions and not on the globals they reach, and that was the
> gap.** `01EF93E8` and `022D9138` were **already documented** — by
> [RNG streams](../../21-RNG-And-Determinism/rng-streams.md) and [which roll is on which
> generator](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) — and reading them
> first would have prevented §1's original framing error. **A coverage check on a function is not a
> coverage check on the state it touches.**

## 3. The record, and the two operands

Every call is `eval(record, context)`. The record's first fifteen bytes are all this path reads *(Qualified 2026-09-29, OPUS, falsification pass 1 of [the contract](CONTRACT-authored-expression-evaluation.md): the operator is loaded as a `u16` at `+0x0E`,
so the path reads **sixteen** bytes, `0x00`-`0x0F`. The operator's bits 4-7 lie in the byte at `+0x0E`, so fifteen
of them decide anything.)*:

```text
+0x00  u32   operand A's payload
+0x04  u32   operand B's payload
+0x0C  u8    operand A's KIND
+0x0D  u8    operand B's KIND
+0x0E  u16   flags; bits 4-7 are the OPERATOR
```

**A kind selects how a payload becomes a number**, and there are three cases:

| kind | meaning |
|---:|---|
| `0` | the operand is **absent**. A yields `0`; B absent means the whole expression is just A |
| `1` | the payload is an **authored-data reference** — `ImageAddress_ResolveRuntimePointer` turns it into a live pointer and the value is read from **`+0x04`** of the target |
| ≥ `2` | a general operand evaluator, `00431080` (718 B), called with the operand's **index** — `0` for A, `1` for B. **Read 2026-09-18 (FABLE): a piecewise curve.** The kind byte is the number of `(x, y)` `int32` pairs in the table the payload resolves to (`+0` for A, `+4` for B, through `ImageAddress_ResolveRuntimePointer`); the `u16` at `+8` (A) or `+0xA` (B) is a period, and a value above it is reduced modulo it (`004310D0`..`004310EC`); the operand's two flag bits (`+0xE` bits 0..1 for A, bits 2..3 for B) select the curve: **0 linear** — an exact `x` returns its `y`, a value between two points returns `y0 + (y1 - y0)(v - x0) / (x1 - x0)` in integer arithmetic, a value past the last point returns the last `y` (`004312CF`..`00431315`); **1 quadratic B-spline** — with three points or fewer the linear path, otherwise the three control points around the value's segment are the curve `0.5(1-t)² p0 + ((1-t)t + 0.5) p1 + 0.5t² p2` (`0039B630`), `0039B6E0` solves `x(t) = v` for `t` by the quadratic formula (falling back to `(2v - x0 - x1) / (x2 - x0)` when it degenerates, sentinel `2.0`), and `y(t)` is rounded away from zero by `0.5` (`004312A1`..`004312C8`); **2 and 3 return 0** (`00431113`). |

Kind 1 is the interesting one for a modder: it means an operand can *point at other authored data*
rather than carry a literal, and `ImageAddress_ResolveRuntimePointer` (`0020E600`, 10 B) is the
same image-address fixup the rest of the authored pipeline uses.

```c
int eval(Rec *rec, int ctx)                        /* 004314E0 */
{
    int a = rec->kindA == 0 ? 0
          : rec->kindA == 1 ? ImageAddress_ResolveRuntimePointer(rec->payloadA)[+0x04]
          :                   operand(rec, ctx, 0);
    if (rec->kindB == 0)
        return a;                                  /* the one-operand form */
    int b = rec->kindB == 1 ? ImageAddress_ResolveRuntimePointer(rec->payloadB)[+0x04]
          :                   operand(rec, ctx, 1);
    return combine(rec, a, b);                     /* TAIL call to 00431350 */
}
```

## 4. The six operators, written out

`combine` (`00431350`, 190 B) reads `op = (rec->u16_0E >> 4) & 0xF`, rejects anything above `5`, and
dispatches through a jump table at `00431410` whose six entries are offsets from the image base
`00120000`. **Four of the six arms call `f()`; operators 0 and 5 do not call it directly** —
op 0 returns `a` outright, and op 5 *jumps into op 1's arm* to borrow its call. See §5.

| op | target | result |
|---:|---|---|
| `0` | `00431401` | **`a`** — five instructions, **no call**: the operand's *value* is discarded, not a draw |
| `1` | `00431390` | **`a + f(b)`** |
| `2` | `004313A4` | **`a − f(b)`** |
| `3` | `004313BA` | **`a − b + f(2b)`** |
| `4` | `004313D2` | **`a × (f(b) + 1)`** |
| `5` | `004313FD` | **`b == a ? a : a + f(b − a)`** — two instructions, then `jne` **into op 1's arm** |
| >5 | `00431401` | **`a`**, same as op 0 |

**Op 3 is the one that gives the page its title.** `a − b + f(2b)` is a draw from a window of width
`2b` centred on `a` — *"`a`, give or take `b`"* — which is how an authored value carries a symmetric
spread.

**Op 5 is a *half-open* range — it includes `a` and excludes `b`**, and that holds in both
directions, because `f` never returns its own bound:

| `a` | `b` | ten results | range seen |
|---:|---:|---|---|
| 10 | 100 | 49, 88, 95, 16, 75, 40, 19, 20, 25, 51 | `[10, 100)` |
| 100 | 10 | 61, 22, 15, 94, 35, 70, 91, 90, 85, 59 | `(10, 100]` |
| 7 | 7 | 7, 7, 7, 7, 7, 7, 7, 7, 7, 7 | exactly `a` |

**When `b < a` the bound handed to `f` is negative**, which is why §5's sign rule is load-bearing
rather than a curiosity.

**When `b` is zero** the function branches at `00431362` to a separate path at `004313E9` that
re-reads the operator and does `sub ecx, 4`:

```text
004313E9  movzx ecx,[rcx+0xE] / shr ecx,4 / and ecx,0xF
004313F3  sub   ecx, 4
004313F6  je    00431401        ; op 4  -> return a
004313F8  cmp   ecx, 1
004313FB  jne   00431401        ; anything but op 5 -> return a
004313FD                        ; op 5 falls through
```

**Only operator 5 survives it.** Op 4 is tested by name and then returns `a` like everything else —
so of the six operators, exactly one behaves differently when the spread is zero.

And it is **not** a degenerate case. Op 5 computes `a + f(b − a)`, so with `b == 0` it computes
**`a + f(−a)`** — a genuine roll that lands in **`[1, a]`**:

```text
a = 50  ->  29, 7, 3, 47, 14, 34, 45, 45, 42, 28
a = 1   ->  1, 1, 1, 1, 1, 1, 1, 1, 1, 1
```

A reimplementation that treated "zero spread" as "no randomness" would be right for five operators
and wrong for the sixth.

## 5. `f()` — the recurrence and exact scaling

`003A6E60` (345 B) takes the bound in `ecx` and returns in `eax`. It is a **leaf — it calls
nothing** — so it can be run in isolation from the shipped bytes with no stubs at all. That is what
the rest of this section is: **the function's own bytes, executed**, not a reading of its shape.

### The scaling law — exact only in single precision, in this order

~~Every call draws one fraction `u` in `[0, 1)` and scales the bound by it, truncating toward zero:
`return (int)(u * bound);`~~ **Corrected 2026-09-11 (ASTRA-CONTRA-FABLE-RNG-ROUNDING).** That
algebra is right and its arithmetic is not: the bytes never form `u`. They advance the shared
recurrence ([the RNG page](../../21-RNG-And-Determinism/rng-streams.md) §2 has it) **five** steps,
reinterpret the new state as a binary32 `v` in `[1, 2)`, and compute, each step rounded to
binary32:

```c
int f(int bound)                       /* 003A6E60 */
{
    advance(5);  float v = as_float(state);           /* 003A6E7B-003A6F12 */
    float B = (float)bound;                            /* cvtdq2ps, 003A6F2A */
    float P = v * B;                                   /* mulss, 003A6F2D  -> 022D91A0 */
    float D = P - B * 1.0f;                            /* mulss / subss, 003A6F31-003A6F41 -> 022D92E0 */
    advance(2);                                        /* 003A6F4D-003A6F8C: the state the next caller sees */
    return (int)D;  /* cvttps2dq over the 16-byte lane block at 022D92E0, 003A6FA9 */
}
```

So `f` is `trunc(v × B − B)`, not `trunc((v − 1) × B)`: the two differ when the products round
differently. ASTRA's [EXP-070](../../_experiments/EXP-070-procedural-rng-controls.md) executed the
345 bytes with no stubs: from seed `458DC800` the fifth-step `v` is `3FB90003` and bound
1,000,000,000 returns **445,312,896**, where `trunc((v − 1) × B)` in binary32 gives 445,312,864
(the negative bound mirrors it); a bound of 0 returns 0 but **still consumes all seven steps**;
with the mode word `022D9138` zero no step is taken, `v` is 1.0 and the scratch is still written.
The six writes, in order: fifth-step state → `01EF93E8` (`003A6F0C`), `P` → `022D91A0`
(`003A6F39`), `D` → `022D92E0` (`003A6F45`), seventh-step state → `01EF93E8` (`003A6F8C`), the
seventh-step sample → `022D92F0` (`003A6FA1`), and the converted four-lane vector back over
`022D92E0`–`022D92EF` (`003A6FAD`) — the other three lanes are whatever the scratch held.

**How the simpler law was established, and why it held.** `u` was recovered to ~31 bits from the
widest bound (`0x7FFFFFFF`), then used to *predict* the output for thirteen other bounds from the
same seed. Any single mismatch would have killed it — and none did, because none of those bounds
sat on a rounding boundary of the two products:

| bounds predicted | draws each | exact |
|---|---:|---:|
| `2, 3, 7, 8, 10, 100, 1000, 65536, 0x40000000, −2, −10, −50, −1000` | 60 | **780 / 780** |

### The sign rule, which op 5 depends on

**`f` is signed.** The result carries the *bound's* sign and stays strictly inside it:

| bound | six results |
|---:|---|
| `100` | 43, 86, 94, 7, 72, 33 |
| `−50` | −21, −43, −47, −3, −36, −16 |
| `−1000` | −436, −866, −945, −76, −729, −336 |
| `0` | 0, 0, 0, 0, 0, 0 — no fault |

So `f(bound)` is in `[0, bound)` for a positive bound and `(bound, 0]` for a negative one. **`f` never
returns its own bound**, which is exactly why op 5's range excludes `b` at both ends.

### Roughly even, with its denominator

6,000 draws at bound 8: `{0: 762, 1: 761, 2: 750, 3: 707, 4: 792, 5: 769, 6: 721, 7: 738}` — against
an even split of 750, the worst deviation is **5.7 %**. Over 60 draws the recovered `u` has mean
**0.497**, min 0.024, max 0.9999. That is evidence of *roughly* even; it is **not** a distribution
test, and none was run.

### Which stream this is — the globals were already identified

[RNG streams](../../21-RNG-And-Determinism/rng-streams.md) names both globals, and **its values
reproduce against the binary**, which is the strongest cross-check this page carries:

| global | that page's identification | shipped | seeded by |
|---|---|---|---|
| `01EF93E8` | shared procedural recurrence **state**, seed `0x458DC800` | `3F800000` | `00259180` |
| `022D9138` | the stream's **enable/mode** word, set to `1` | BSS (zero) | `00259180`, `0044BAC0` |

Emulated with exactly those documented values — `022D9138 = 1`, `01EF93E8 = 0x458DC800` — the
generator comes alive: bound 100 gives `44, 0, 0, 85, 16, 64, 63, 76, 22, 29`, and over 2,000 draws
`u` has mean **0.4935**, min 0.00005, max 0.9998. **Neither value alone is enough**: with the enable
word at 1 but the state shipped, and with the state seeded but the enable word zero, every bound
returns 0.

That is two independently written documents and the shipped bytes agreeing.

### The rest of the state, recorded rather than guessed

A memory-write hook over the whole run — so nothing depends on my choosing which address to watch —
says each call writes **five** locations:

| address | writes per call | shipped value |
|---|---:|---|
| `01EF93E8` | 2 | `3F800000` (= `1.0f`) — **written, so it is state, not a constant** |
| `022D91A0` | 1 | BSS — but **shared scratch**, written by **67** functions |
| `022D92E0` | 2 | BSS — **shared scratch**, written by **106** functions |
| `022D92E8` | 1 | BSS — inside the same shared region |
| `022D92F0` | 1 | BSS — inside the same shared region |

`022D9138` is **read and never written by this function**, and it *gates* the update: with it zero,
the two state stores at `003A6F0C` and `003A6F8C` are skipped and `01EF93E8` keeps its value
(the scratch writes still happen, §5). Across the binary it has only **two** writers, `00259180`
and `0044BAC0`.

**The last four are not this generator's private state.** They sit in `022D9198`–`022D9428`, the
660-byte shared scratch region mapped by [intentionally ownerless functions and shared
scratch](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md),
which warns explicitly: *"the shared scratch is not yours"*. `003A6E60` is one of 67 and 106 writers
respectively — so **nothing here claims it owns them**, and a reimplementation must not assume it may
keep private state there.

> **The image ships this generator inert.** `022D9138` is past `SizeOfRawData` — BSS, so zero at
> load — and with the shipped values **every bound returns 0**. Both globals must be non-zero before
> a single call varies. So the sequence a player gets is decided entirely by **whatever seeds these
> at runtime, which is not established**, and a reimplementation that seeded them differently would
> produce a different game.

### One extra draw shifts everything after it

Two identically seeded generators, one given a single extra call:

```text
without: 21, 43, 47, 3, 36, 16, 5, 5
with   : 43, 47, 3, 36, 16, 5, 5, 8
```

The second is the first shifted by one. **The *number* of draws matters as much as the formula** — so
the count of `f` calls per authored value is part of the contract, and §4's per-operator call counts
are load-bearing.

> **Correction closure, 2026-09-11 (ASTRA).** The earlier version of this summary still called
> the recurrence unknown after the correction above and RN-1's resolution. The bit recurrence
> is specified on the RNG page and tested in [EXP-070](../../_experiments/EXP-070-procedural-rng-controls.md):
> the bounded helper samples after five steps and advances two more, even for bound zero.
> Its binary32 multiply/subtract order is required; the older `u * bound` shorthand is not exact.
> The one-step sibling is also executed and its scratch copy is known. Seven sibling calls match
> one bounded call's final recurrence state, but not its scratch effects. Live draw order, the
> complete consumer census and shared-scratch ownership remain outside that evidence.

## 5a. Four of these records side by side are a colour — 2026-09-21 (FABLE, answering `OPUS-REQ-FABLE-WHAT-THE-FOUR-AUTHORED-EXPRESSIONS-PRODUCE`)

`0042FDB0` evaluates **four** of the records above, at block `+0x00`, `+0x10`, `+0x20`, `+0x30`, into
four consecutive stack dwords, and when **bit 2 of the block's mode byte `+0x40`** is set it hands
those four to `00430370` (`004300BE`–`004300CF`). OPUS closed the shape and asked what it means.
**It is a colour, and the conversion names every component itself** — no consumer is needed to read
it, because only one arithmetic does this.

**`00430370` is `0x180` bytes and the part past its first `0x60` is a textbook HSV→RGB.** After the
two normalisations it:

| | |
|---|---|
| `004303E6` | `comiss` the first component against **`360.0`**, and `jb` past the next instruction — so a value **at or above 360 is replaced by zero** |
| `004303F4` | divides it by **`60.0`** |
| `00430401` | `floorf` → the **sector**, `cvttss2si` into `ecx` at `0043041F` |
| `00430414` | `subss` gives the **fraction** `f` of the way through that sector |
| `00430431`, `0043043F` | `p = (1 - S) · V` |
| `0043042C`, `0043043B`, `00430447` | `q = (1 - f·S) · V` |
| `00430423`, `00430436`, `00430443`, `0043044B` | `t = (1 - (1-f)·S) · V` |

and then dispatches six ways (`0043044F`–`00430499`). **All six arms were enumerated**, and they are
the standard table exactly — the triple below is `(xmm1, xmm0, xmm6)`, which is what the stores then
emit as `(R, G, B)`:

| sector | arm | result |
|---:|---|---|
| 0 | fallthrough → `00430499` | `(V, t, p)` |
| 1 | `00430493` | `(q, V, p)` |
| 2 | `00430488` | `(p, V, t)` |
| 3 | `00430480` | `(p, q, V)` |
| 4 | `00430478` | `(t, p, V)` |
| 5 | `00430470` | `(V, p, q)` |

**The achromatic case settles it beyond the table.** `004303CB` compares the *second* component with
zero and, on equality, skips the whole sector machine and sets all three outputs to the *third*
(`004303DB`–`004303E1`). **Zero saturation gives grey at the value's brightness**, which is what an
HSV converter does and what nothing else does.

### The four components, and three of them are not what the shape suggests (2026-09-21, FABLE)

| offset | component | range, as the code treats it |
|---|---|---|
| `+0x00` | **hue** | **degrees.** Compared with `360.0`, divided by `60.0`; **never touched by 255** |
| `+0x04` | **saturation** | `minss` against `255.0` then `divss` — `0..255` → `0..1` |
| `+0x08` | **value** | the same, `0..255` → `0..1` |
| `+0x0C` | **alpha** | clamped **above** at 255 and stored **raw** (`004304DA`–`004304E7`); never normalised |

***So "four integers clamped to 255 and normalised" is true of two of them.*** A type row that calls
all four `0..255` channels is wrong about the hue and the alpha both.

**The output is four bytes** at the second argument (`004304BE`–`004304E7`): `R`, `G`, `B` — each
multiplied back by `255.0` and truncated — then the alpha byte. `0042FDB0` returns that packed dword
(`004300D4`), and one caller of record is the **effect element loop** `00441B30`, which stores it at
element `+0xF0` (`00441E52`) — the same body [the element dispatch](../../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md)
already names. **So an authored effect can drive hue, saturation, value and alpha each by its own
expression**, with all the randomness and recurrence §5 describes, and the engine resolves the four
to a packed RGBA byte quad per evaluation.

**Edge behaviour, all defined and none of it meaningful.** Hue `360` and hue `400` both render as
`0°`, because the guard is a **clamp to zero, not a modulo**. A **negative** hue passes the `jb`,
divides to a negative sector, and falls through every arm to the sector-0 fallthrough with a negative
fraction. A negative saturation or value is **not** clamped below, because `minss` only takes the
smaller of the two. A negative alpha stores its low byte.

**What this does not establish.** No live observation and no rendered pixel: the claim is that the
routine computes HSV→RGBA, not that any effect looks like any particular colour on screen. The
**bit-2-clear** branch of `0042FDB0` is not characterised here — one correction of fact only, that the
two operands it loads at `004300E0`/`004300EC` are `.bss` scratch buffers at `022D8F30` and
`022D8F40`, **not string literals**, so "a diagnostic" is a shape and not yet a reading. Mode-byte
values 1 and 2, which reach `0042FE85`, are unread.

## 6. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `004314E0` | the expression evaluator | 147 B | **99** non-EH callers; resolves both operands; interior verified 2026-09-17 (SWE2-EC7): kind-byte reads `[rcx+0xC]`/`[+0xD]` at [`004314EF`](../../_index/ADDRESS-INDEX.md) |
| `00431350` | the operator combiner | 190 B | the six formulas |
| `00431410` | the jump table | — | **data, not a function**: a 24-byte region, six dwords, offsets from `00120000` |
| `00431080` | the general operand evaluator | 718 B | kinds ≥ 2; takes the operand index; **read 2026-09-18** (the piecewise curve, §2's table) |
| `0020E600` | `ImageAddress_ResolveRuntimePointer` | 10 B | kind 1's authored-data fixup |
| `003A6E60` | the bounded draw | 345 B | leaf; 5 steps, `trunc(f32(v × B) − f32(B))`, 2 more steps; signed; §5 |
| `022D9138` | procedural stream **enable/mode** | — | read here, never written here; **2 writers binary-wide**; BSS |
| `01EF93E8` | shared procedural recurrence **state** | — | **written twice per call**; documented seed `0x458DC800` |
| `00259180` | the stream's seeder | 179 B | read 2026-09-11: called once at boot by `0022A0B0` ([what the engine fixes at boot](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)), runs twenty presentation initialisers, then stores `0x458DC800` to `01EF93E8` and to the scratch lane `022D92E0` and `1` to `022D9138` (`0025920C`–`00259220`) |
| `004005E0` | 1-step sibling returning `[0,1)` | 108 B | same globals; `as_float(state) − 1.0`, sample → `022D92E0` and a 16-byte copy → `022D8F90` even when disabled (EXP-070) |
| `022D91A0`, `022D92E0`, `022D92E8`, `022D92F0` | **shared scratch, not owned here** | — | 67 / 106 writers; see the shared-scratch page |
| `01CEBBA8` | `1.0f` | 4 B | `.rdata` |
| `004309C0` | the **float** twin of `004314E0` | 155 B | 89 callers; interior verified 2026-09-17 (SWE2-EC7): same tag-pair dispatch at [`004309CA`](../../_index/ADDRESS-INDEX.md), operands resolved as `movss` floats, combiner tail `00430540` |
| `00430B90` | uncited neighbour | 1,199 B | 78 callers; **not read** |
| `004304F0` | two-field image-pointer rebase (not an evaluator) | 68 B | 64 callers; interior verified 2026-09-17 (SWE2-EC7): resolve `[rdi]`/`[+0x04]` via `0020E600`, add delta, re-encode via `0020E620`, store back — first resolve at [`00430501`](../../_index/ADDRESS-INDEX.md); returns `rdi+0x10` |

## 7. What this document does not establish

- ~~**What kinds ≥ 2 do.** `00431080` is 718 bytes and was not read;~~ **Read 2026-09-18 (FABLE): kinds ≥ 2 are piecewise curves, the kind byte counting the table's points, linear or quadratic-B-spline by the operand's flag bits, with a period (§2's table).** ~~it is where the operand space
  actually lives, and it takes a *context* argument this page passes through without inspecting.
- **What the other eleven bits of `+0x0E` mean.** Only bits 4–7 are the operator.
- **What the record is part of**, or who authors it. The four uncited neighbours are the obvious next
  place to look.
- ~~**The algorithm that produces `u`.** The *scaling* is proven; the generator is not named.~~
  Resolved by the explicit recurrence and EXP-070; see §5. This does not establish a live draw sequence.
- ~~**The body of `00259180`.** It is named as the seeder by two other documents and its seed values
  reproduce, but **its 179 bytes were not read here**, and when it runs is not established.~~ Read
  2026-09-11: it runs once, at boot — its only caller is the boot fixer `0022A0B0` (itself called
  from `0017D4C0`) — after twenty presentation-subsystem initialisers (`00259191`–`002591F2`), and
  its three stores are the ones `rng-streams.md` lists (§6 key addresses).
- ~~**The body of `004005E0`.** The likely unscaled `u`; not read.~~ Read by EXP-070 (one step, `state − 1.0`, the 16-byte scratch copy).
- **Whether this stream is used anywhere outside Presentation.** 96 of 99 callers are
  Presentation-owned and 3 are untagged; **the 3 were not read**, and ownership is not inferred from
  callers in either direction.
- **Any observation of the running game.** §5 is the shipped bytes emulated in isolation, which is
  stronger than static reading and weaker than the game. No in-game measurement was taken.

## 8. Falsification checklist

- [x] **The operator is four bits at `+0x0E`.** *Killer:* a different extraction. `movzx eax, word
      [rcx+0xE] / shr eax,4 / and eax,0xF` at `00431368`. **SURVIVED 2026-09-12 (FABLE):** re-read
      from `00431350`; the same extraction is repeated on the zero-bound path at `004313E9`–`004313F0`.
- [x] **There are exactly six operators.** *Killer:* a larger bound. `cmp eax,5 / ja` at `00431372`,
      and the table at `00431410` holds six entries, each resolved with a tool. **SURVIVED
      2026-09-12:** the six dwords at `00431410` resolve to `00431401` (op 0, no draw), `00431390`
      (op 1, `a + rand(b)`), `004313A4` (op 2, `a − rand(b)`), `004313BA` (op 3), `004313D2` (op 4,
      `a × (rand(b) + 1)`) and `004313FD` (op 5, which re-enters op 1's arm through `sub edi, ebx`);
      the zero-bound path keeps only ops 4 and 5 (`004313F3`–`004313FB`).
- [x] **Op 3 is a symmetric spread.** *Killer:* different arithmetic. `lea ecx,[r8+r8]` doubles the
      bound, `sub ebx,edi` is `a − b`, and `add eax,ebx` sums them. **SURVIVED 2026-09-12:**
      `004313BA`–`004313C5`, exactly as written.
- [x] **Op 0 does not draw.** *Killer:* a call in its arm. `00431401` is `mov eax,ebx / mov
      rbx,[rsp+0x30] / add rsp,0x20 / pop rdi / ret` — **no call**. The operand's *value* is still
      computed by the caller at `004314E0` and discarded; whether computing it draws depends on
      `00431080`, which is unread.
- [x] ~~**`f(bound) = trunc-toward-zero(u × bound)`.**~~ *Killer:* one mismatched prediction. `u` was
      recovered from bound `0x7FFFFFFF` and predicted 13 other bounds exactly, **780 / 780** — and
      the killer arrived 2026-09-11 from a bound none of the thirteen covered: 1,000,000,000
      (EXP-070). The exact law is the single-precision sequence in §5.
- [x] **`f` is signed and never returns its bound.** *Killer:* a negative bound giving a positive
      result, or any `|result| >= |bound|`. `f(−50)` gives −21, −43, −47, −3, −36, −16.
- [x] **Only op 5 does anything when `b == 0`.** *Killer:* op 4 differing from `a`. `sub ecx,4 / je
      00431401` sends op 4 to the same return as op 0.
- [x] **The shipped image is inert.** *Killer:* a non-zero result from the shipped state. `022D9138`
      is past `SizeOfRawData`; with the shipped values every bound returns 0.
- [x] **`f` calls nothing.** *Killer:* any `call` in its body. There are none.

## Falsification pass 1 — 2026-09-13 (OPUS)

§5's correction turns on one arithmetic distinction — `trunc(v × B − B)` against
`trunc((v − 1) × B)` — and that distinction is checkable without the binary, because it is entirely a
statement about binary32 rounding. Recomputed independently in float32:

| | |
|---|---|
| `v` from bits `3FB90003` | **1.445312858**, and in `[1, 2)` as § requires |
| `B = (float)1,000,000,000` | exactly representable |
| `P = fl(v·B)`, `D = fl(P − B)`, `trunc(D)` | **445,312,896** — §'s figure |
| `trunc(fl(fl(v − 1)·B))` | **445,312,864** — §'s figure |
| the negative bound | **−445,312,896**, mirroring exactly as § says |

Both numbers reproduce, the three stated sizes are exact (`003A6E60` **345 B**, `00431080` **718 B**,
`0020E600` **10 B**), and the six tabulated result rows all lie strictly inside their bound and never
equal it.

### The two laws do not merely round differently — they land on different lattices

§ says the two "differ when the products round differently", which is true and understates it. `P`
is rounded at the magnitude of `v·B` ∈ `[B, 2B)`, and `B` is a multiple of that magnitude's ulp, so
**`D = P − B` can only ever be a multiple of it.** Measured over 3,000 draws at each of 22 bounds
from `2²⁰` to `1.6 × 10⁹`, the byte law's outputs share a gcd of exactly

```
step = 2 ^ (floor(log2(bound)) − 23)
```

**at every one of the 22** — while the algebraic law's gcd is **1** at all of them.

| bound | byte-law step | algebraic step |
|---:|---:|---:|
| `2²³` = 8,388,608 and below | **1** | 1 |
| `2²⁴` = 16,777,216 | **2** | 1 |
| 100,000,000 | **8** | 1 |
| 1,000,000,000 | **64** | 1 |

So the divergence is **systematic above `bound ≥ 2²⁴`**, not an occasional tie-break: at a bound of a
billion `f` returns only multiples of 64, and the algebraic value **445,312,864 is a multiple of 32
but not 64 — off-lattice, and unreachable**. Confirmed: it never appeared in 4,000 draws.

> That is the sharper form of §'s own correction. A reconstruction using the algebraic law would not
> just disagree occasionally at large bounds — **it would produce values the game can never return**,
> and the smaller the step it claims, the more of them.

Below `2²⁴` the two laws agree on the lattice and can still differ on individual ties, which is why
§'s thirteen predicted bounds — all ≤ `0x40000000` but mostly small — came back **780 / 780**: none
of them sat on a boundary, exactly as § says.

**Not claimed:** nothing here was executed — this is arithmetic over the same binary32 constants, not
the 345 bytes running. `EXP-070`'s isolated execution remains the only evidence that the *bytes*
compute this; the pass confirms that the formula § derived from them has the properties § attributes
to it. §§2–4, the stream identification and the scratch writes were not re-derived, and §'s statement
that the distribution evidence is "not a distribution test" stands.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**Input — SERVICE.** The init burst `0017D4C0` creates the input manager (`InputManager_CreateSingleton`), and the boot
initialiser calls the 119-byte Input initialiser. Both are start-up siblings, and neither is a randomness source.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** The seed initialiser this page cites is called only by the core start-up subtree's root. The root is reached from the 387-byte start-up body this page cites (itself called by a 129-byte core body) and calls a 146-byte start-up helper. The cited start-up body also calls two small core helpers (28 and 69 bytes).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `0022A0B0` on this page calls `BattleStorage_InitializeWorkArrays`, owned by that layer. What it reaches is an initialiser: it writes +inf to `[02F973B8]`, zeroes `[02089300]`, sets `[0208E6A0]` to `0x20` and calls `003844F0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — MECHANICAL (SWE2-EC7-160, 1075 edges).** Batch-125's `003B3160` names `00259180`/`0036C1D0`/`0024C550`; the page's expression helpers `001DB840`/`0020E680` are called by Presentation bodies (`003A33B0`, `003A34D0`, `0039D5A0`, +1072 more). Shared presentation fan-in to the expression helpers, not a randomness responsibility.

**Script VM and World Area Field — CLIENT (shared-callee edges, SWE2-EC7-189).** The `0036C1D0`/`0036A100` arena allocator pair my `003CD6E0` entry names is also consulted by the script-VM layer (`0050D8F0`) and by world-area field callers (`00267930`/`003319D0`/`003EA820`/`0036A190`-adjacent). The crossing is those layers sharing the allocator this page names, not shared responsibility. Edge list from `edges.tsv`.
- **RNG_Random_Selection — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_Seed` (00379CF0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **Save_Load_Settings — SERVICE (3 edges).** 3 outbound (page-cited `0017D4C0` call Save_Load_Settings bodies `SaveloadManager_RefreshDisableAutosaveList` (001C1710), `SaveloadManager_GetSingleton` (001C18E0), `SaveloadManager_EnsureSingleton` (001C18A0)). Substantive edges include `0017D4C0` calls `SaveloadManager_RefreshDisableAutosaveList` (001C1710); `0017D4C0` calls `SaveloadManager_GetSingleton` (001C18E0); `0017D4C0` calls `SaveloadManager_EnsureSingleton` (001C18A0).
## Interior citation — frontier hub `00431830` (2026-09-17, SWE2-EC7)

`00431830` — 728 B, 37 frontier callers at census; the five-mode sibling of this page's
tagged-pair evaluators. Interior verified: [`0043184B`](../../_index/ADDRESS-INDEX.md) is
`movzx ecx, byte [rcx+0xA0]` — the body dispatches on the record's `+0xA0` mode byte over
`{0,1,2,3,4}`; each arm resolves image pointers through `0020E600` (5–8 resolves per arm) and
calls the `00502xxx`/`00503xxx` materialisation helpers, with `+0xA8` indexing a qword pair table
at `lea rcx,[rip+0x26bd06d]` on the mode-4 arm. Same authored-record family as
`004314E0`/`004309C0`, one level up: where those evaluate one tagged pair, this materialises the
whole record variant.

NOT claimed: the five mode layouts' field meanings or the `00502xxx` helpers' roles — only the
mode dispatch and the resolve-then-materialise shape are measured.

## SWE2-EC7-21 update (2026-09-18) — `00431B10` SSE-lane scatter fragment

`00431B10` (513 B) is the `02CA4EE0`-record kind dispatch the expression
evaluators share: `003CD840` loads the record context and `004314E0` reads the
`+0x10` sub-record, `byte[rdi+3]` bit-3 folds `si-1` into the staged record, then
`byte[rdi]-1` indexes a six-case jump table at `0x311D14` — each arm packs a
different `{word, byte}` field set into the `[rbp-0x60]` work record and calls
its ~~`0050xxxx` formatter~~ `0050xxxx` palette operation (**Corrected 2026-09-30 (SWE2-EC7, SD-120):** operations 1, 2, 3, 5, 6 and 7 of the palette (CLUT) animation machine, run on the `02CA4EE0` palette `00431B10` decodes - not a formatter; [sd120-binding-ops-0930](../../_index/candidates/sd120-binding-ops-0930/README.md)) (`0050AC20`/`00506B40`/`005080A0`/`00509BB0`/`00507490`/
`00508C90`) — before `003A9C10` republishes the result. Interior anchor `00431B99`
(the jump-table base `lea`). Callers `00431830`/`004490D0`/`0044BAC0`/`0044EDD0`/
`0044F970`/`004518D0`/`00452540`/`00453150`/`00453CF0`/`00454930`/`00461270` —
the expression/effect evaluators including this page's `00431830` authored-number
arm.

## SWE2-EC7-33 update (2026-09-19) - `003CD840`

`003CD840` (21,276 B) is ~~the element-kind megadispatch the `0050xxxx` formatter family feeds~~ the palette (CLUT) unpacker the `0050xxxx` operations work on (**Corrected 2026-09-30 (SWE2-EC7, SD-120):** `r8d` is the entry count - 1, 16 or 256 RGBA8 entries, each unpacked to four 8.8 lanes; K1, [sd120-binding-ops-0930](../../_index/candidates/sd120-binding-ops-0930/README.md)): a call-free `r8d` switch over the `022D8F90`-`022D94A0` global block - `r8d == 1`, `0x10` and `0x100` arms each unpack `022D8F10` into the `022D8F90`+0x10 byte record and clamp the running index at `022D8F94` against the `022D8FB4` bound (`cmovge`/`cmovle`). Interior anchor `003D01A2` (a `022D8FAA` byte store).

## SWE2-EC7-33 update (2026-09-19) - `0050AC20`

`0050AC20` (6,192 B) is the math-heavy member of the `0050xxxx` family: the same `[rdx+0xE]`/`[+0x36]` element record against the `022D8Fxx` block, six `00861EBA` libfn calls over the computed fields. Interior anchor `0050AD36` (an `00861EBA` call).

## SWE2-EC7-33 update (2026-09-19) - `00508C90`

`00508C90` (3,861 B) is a call-free element compute sibling - `[rdx+0xE]`/`[+0x36]`/`[+0x24]` record fields into the `022D8Fxx` block, an `0x7fffffff` bound at `005093E3`. Interior anchor `005093E3` (the bound).

## SWE2-EC7-33 update (2026-09-19) - `00507490`

`00507490` (3,074 B) is a call-free compute sibling - cookie prologue, `022D8F10`/`022D8FA0`/`022D912C` global stores. Interior anchor `00507A5B` (the `022D912C` store).

## SWE2-EC7-33 update (2026-09-19) - `005080A0`

`005080A0` (3,048 B) is a call-free compute sibling - `0x7fffffff` sentinel fills into `[r8+rax+0x21B8FD0]` record slots. Interior anchor `0050866C` (a sentinel store).

## SWE2-EC7-33 update (2026-09-19) - `00509BB0`

`00509BB0` (**1,345 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,113 B, a wrong literal in the batch-33 append — the body is 1,345 B per the function list*) is a call-free compute sibling - `movq`/`xmm` pack-unpack over the `022D8Fxx` block. Interior anchor `00509E2B` (the `movq rdx, xmm0` unpack).

## SWE2-EC7-33 update (2026-09-19) - `00506B40`

`00506B40` (**1,501 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,600 B, a wrong literal in the batch-33 append — the body is 1,501 B per the function list*) is a call-free compute sibling - `[r9+0x36]`/`[+0x28]` field compares. Interior anchor `00506E19` (a pre-shift `mov rax, rdx`).

## SWE2-EC7-33 update (2026-09-19) - `00461270`

`00461270` (3,820 B) is an element-record walker in the `0044xxxx` skeleton - 17 `0020E600` id-record calls plus `0026EE00`/`00430B90`/`00431830`/`00462260`/`0042FDB0`. Interior anchor `004612BA` (the first `0020E600` call).

## SWE2-EC7-33 update (2026-09-19) - `00453CF0`

`00453CF0` (1,935 B) is the same walker skeleton - 8 `0020E600` calls plus `00430B90`/`004314E0`/`004309C0`/`003A6E60`/`003A34D0`/`00397910`. Interior anchor `00453D37` (an `0020E600` call).

## SWE2-EC7-33 update (2026-09-19) - `0044F970`

`0044F970` (1,869 B) is the same skeleton - `0026EE00` plus `004314E0`/`00430B90`/`004309C0`/`003A34D0`. Interior anchor `0044FBB9` (an `0026EE00` call).

## SWE2-EC7-33 update (2026-09-19) - `004518D0`

`004518D0` (1,858 B) is the same skeleton - 7 `004309C0` calls plus `0020E600`/`0026EE00`/`004314E0`/`00430B90`. Interior anchor `004519A4` (a `004309C0` call).

## SWE2-EC7-33 update (2026-09-19) - `00452540`

`00452540` (1,831 B) is the same skeleton - 8 `004309C0` calls plus `0026EE00`/`004314E0`/`00430B90`/`0020E600`. Interior anchor `00452602` (a `004309C0` call).

## SWE2-EC7-33 update (2026-09-19) - `0044EDD0`

`0044EDD0` (1,772 B) is the same skeleton - 7 `0020E600` calls plus `00430B90`/`004314E0`/`0026EE00`/`003A34D0`. Interior anchor `0044EE12` (an `0020E600` call).

## SWE2-EC7-33 update (2026-09-19) - `00453150`

`00453150` (1,725 B) is the same skeleton - `004309C0` plus `0020E600`/`004314E0`/`00430B90`/`0026EE00`/`00397910`. Interior anchor `00453205` (a `004309C0` call).

## SWE2-EC7-33 update (2026-09-19) - `004490D0`

`004490D0` (**1,157 B** — *corrected 2026-09-19 (OPUS); this line said 1,016 B, which disagreed with [the element-types page](../../17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md). The function list gives 1,157, and that page cites an interior anchor at `0044951B`, 1,099 bytes in — past the end of a 1,016-byte body, so 1,016 cannot be right*) is the same skeleton - 6 `0020E600` calls plus `004314E0`/`00430B90`/`004309C0`/`0026EE00`. Interior anchor `0044937E` (an `0020E600` call).

## `005030F0`, the selector every element handler on this page calls (2026-09-19, OPUS)

*Surfaced by the `U-6` census (`12abaf9a9`) as one of three layout-bearing bodies no page in the
database cites. **All nine of its callers are on this page** — `00431830`, `0044EDD0`, `0044F970`,
`004518D0`, `00452540`, `00453150`, `00453CF0`, `00454930`, `00461270` — so the shared routine they
all reach is documented here, where its callers already are.*

`005030F0(ctx, ref, out)` (133 B) resolves a three-byte selector into a 16-byte value.

### The selector is three bytes, and one of them is both a flag and an index

`ref` is read at **`+0x71`, `+0x72` and `+0x73` only**; `+0x70` is never touched by this body and is
not claimed here.

| byte | role | evidence |
|---|---|---|
| `+0x71` | index into table **A** | [`005030F7`](../../_index/ADDRESS-INDEX.md) `movzx r9d, byte [rdx+0x71]`, then `[rax + r9*8]` |
| `+0x72` | **bit 7 selects the table; bits 0–6 are the index into B** | `test al, al / jns` ([`0050313B`](../../_index/ADDRESS-INDEX.md)), and `and edx, 0x7f` before `[rax + rdx*8]` |
| `+0x73` | index into the chosen entry's stride-8 sub-array | `[rdx + rax*8 + 0x24]` / `[rax + rcx*8 + 0x2c]` |

`ctx` carries **two parallel pointer tables**, `+0x28` (A) and `+0x30` (B), both arrays of 8-byte
pointers. The same byte serving as a table flag *and* a 7-bit index is the part a reimplementation is
most likely to get wrong: `+0x72` is not a plain index, and masking it is not optional.

### What it produces

1. `entryA = [ctx+0x28][ref+0x71]`, and **16 bytes are copied from `entryA+0x10` to `out+0x00`**
   ([`00503103`](../../_index/ADDRESS-INDEX.md)). That copy is the whole result in the common case.
2. `kind = byte[entryA+0xA0] & 0x7F`. **`kind >= 3` returns immediately**
   ([`00503114`](../../_index/ADDRESS-INDEX.md)) — so only kinds 0, 1 and 2 go further. The `& 0x7F`
   means **bit 7 of `+0xA0` carries something this function deliberately ignores**; unread here.
3. A selector that points at itself returns too: `ref+0x71 == ref+0x72` **and** `ref+0x73 == 0`
   ([`0050311D`](../../_index/ADDRESS-INDEX.md)–`00503128`).
4. Otherwise `out+4` is rewritten as a **packed 5 + 27 dword**: its low 5 bits are kept from the
   record just copied (`out+4` is `entryA+0x14`), and the upper 27 come from a sub-record —
   `dword[entryA + ref[0x73]*8 + 0x24]` when `+0x72` has bit 7 clear, or
   `dword[entryB + ref[0x73]*8 + 0x2C]` when it is set, in both cases `& 0xFFFFFFE0` before the merge
   ([`00503156`](../../_index/ADDRESS-INDEX.md), [`0050316A`](../../_index/ADDRESS-INDEX.md)).

So an entry owns a **stride-8 sub-array**, and the dword the merge reads sits at **`+0x24` in a
table-A entry and `+0x2C` in a table-B entry** — the same stride at two different displacements,
which is a layout difference between the two entry types and not a typo in either read.

### Two things this does *not* establish

- **The 16-byte copy is one move, not a `vec4`.** `00503103`/`00503107` are a single `movups` pair.
  By this corpus's rule (`check_copy_displacements.py`, `4b91d0dc1`) a block copy's displacement is
  not a field, so `entryA+0x10` must not be declared a four-float vector on this evidence. Note also
  that these are `movups`, **not** the `movaps` the `0x30`-byte record append uses — so **no alignment
  contract is implied here**, and the two idioms should not be read as the same one.
- **NOT CLAIMED:** what the 16 bytes mean; what kinds 0/1/2 are as against `>= 3`; what the 5-bit
  field counts; what bit 7 of `entryA+0xA0` is; and what lives at `ref+0x70`. Every one of those is a
  named location with an unread meaning, and naming is not understanding.

## SWE2-EC7-36 update (2026-09-19) - `00430540`

`00430540` (634 B) is an authored-number body - `01CEBC08`, `0020E600` pair plus `0039B6E0`/`0039B630`/`00808C40`. Interior anchor `0043056E` (a `0020E600` call).

## SWE2-EC7-51 update (2026-09-19) - `003A9C10`

`003A9C10` (175 B) is the authored-number republish - `00183310`/`002D81D0`/`0036A190`/`003D2B60`. Interior anchor `003A9C32` (an `00183310` call).

## SWE2-EC7-52 update (2026-09-19) - `003D2B60`

`003D2B60` (20710 B) is the authored-number kind publish - `r8d` dispatches kinds 1/0x10/0x100; the 0x10 arm walks ~15 sub-cases each bound-checked against `022D8FB4` writing `022D8F10`/`022D8FB0` tables, `003CCA70` tail. Interior anchor `003D7386` (a `003CCA70` call).

## SWE2-EC7-55 update (2026-09-19) - `003A34D0`

`003A34D0` (270 B) is an authored-number operand body - `001DB840`/`0020E680`/`0024E460` plus `01EFAC20`/`02AEE900`/`02AEE910`/`02AEF418`. Interior anchor `003A353B` (a `0024E460` call).

## SWE2-EC7-56 update (2026-09-19) - `003CCA70`

`003CCA70` (236 B) is a call-free SIMD byte unpacker - `movd`/`psrldq` chains extracting xmm1/xmm2 lanes into `[rcx]`-`[rcx+0xF]`. Interior anchor `003CCA93` (the first byte store).

## SWE2-EC7-58 update (2026-09-19) - `0039B630`

`0039B630` (170 B) is a call-free 3x3 matrix-vector transform - `mulss`/`addss` row triples into `[r8]`/`[r8+4]`. Interior anchor `0039B684` (the `addss` row accumulate).


## SWE2-EC7-68 update (2026-09-19) - `00503000` expression-channel row locator

`00503000` (231 B) is the three-out channel-row locator the
authored-number readers (`004490D0`/`0044EDD0`/`0044F970`/
`004518D0`/`00452540`/`00453150`/`00453CF0`/`00454930`/`00461270`)
share. `rcx` is the expression context, `[rcx+0x10]` the record
(null -> return 0); `byte[record+0x71]` indexes the `[rcx+0x28]`
pointer table into `elem1`, which must pass
`byte[elem1+0xA0] & 0x7F < 3` or the body returns 0. Then
`byte[record+0x72]` steers the row source: its sign bit selects
`[rcx+0x30]`-indexed `elem2` rows (`elem1` itself when clear), and
the element stride is `0x100` when `byte[elem2+0x10] & 0x7F` (or
`byte[elem1+0xA0]` on the clear arm) is non-zero, `0x10` otherwise.
`byte[record+0x73] * stride` scales the row index: `*rdx` out gets
`[elem+0x20]`/`[elem1+0xB0] + idx*4`, `*r9` gets `[elem2+0xB8]` /
`qword[elem1 + idx*8 + 0x148]`, and `*r8` gets the stride itself;
return is 1 on success. Interior anchor `00503076` (the
`byte[+0x73] * stride` multiply).

## SWE2-EC7-72 update (2026-09-19) - `005039A0` budget selector measured

`005039A0` (213 B) is the interval selector the expression bodies call:
outer loop `r12` over `word[+0x10]` records resolved through
`0020E600([+0x18])` at `rbx << 4`; each record's `byte[+8]` is its kind -
kind 0 accumulates `byte[+9]` into `edi` against budget `ebp` keeping
the last fit in `r15`, kind 1 reads `word[+0xC]` as a redirect, kind 2
consumes `r8d`; the tightest record under budget returns (else `r15` or
0 through the `r8d` arms).
Interior anchor `005039E4` (the `0020E600` record resolve).

## SWE2-EC7-82 update (2026-09-20) - `00502EA0` + `00502280` + `00501A50` measured

`00502EA0` (130 B) is the indexed active-element fetch the authored
passes open with: `r8d` selects the index-check arm - 0 clamps
against `dword[+0x3C]`, 1 takes `edx mod [+0x3C]`, 2 compares
against `word[+0x38]` - then the `[+0x10]` table walks at 0x90
stride returning the `edx`-th element whose `byte[+0x70]` bit0 is
set (0 when fewer are live).
Interior anchor `00502EF3` (the `+0x70` flag test in the walk).

`00502280` (2,596 B, stack-cookie + `__chkstk` 0x1080 frame) is the
larger authored build: `word[rdx+0x44]` feeds `00502EA0` for the
element, then the SSE pipeline runs `00431D30` x6, `00501820` x6,
`003AFDD0`/`0039A150`/`0039B780`/`0043DF80`/`00521450` pairs and the
`00397910`/`00397ED0`/`00398C50`/`0039ADE0`/`0039C5D0`/`0039CCB0`/
`00250010`/`0026EE00` helpers across the record.
Interior anchor `005022C4` (the `00502EA0` call).

`00501A50` (1,793 B, stack-cookie + `__chkstk` 0x1088 frame) is the
smaller sibling: same `00502EA0` open on `word[+0x44]`, the same
`0039`-family helper set minus `00431D30`/`00501820`/`003AFDD0`, and
`00521450`/`0043DF80` pairs - the reduced build for the same record
kind.
Interior anchor `00501A87` (the `00502EA0` call).

## SWE2-EC7-83 update (2026-09-20) - `00521450` + `0043DF80` measured

`00521450` (1,886 B, call-free) is the matrix-bank multiply the
authored builds run between fetches: `[rdx]`/`[rdx+0x40]`/`[rdx+0x80]`
rows stage into the `022F9xxx` scratch bank alongside `[rcx]`'s four
rows, the shufps/mulss/addss dot-product web writes the `022F9xxx`
result rows, and an `r8d = 3` loop over `[r14+0x400]`-offset records
repeats the accumulate - a pure-SSE 4x4 transform fold with no calls.
Interior anchor `00521513` (the first `mulps` of the dot web).

`0043DF80` (1,204 B) is the record builder the same callers run on
the `02F9F2C0`-indexed 0x28-stride table: `0020E680` resolves the
entry, the min of `[r15+4]`/`[+0x14]`/`[+0x24]` lands at `+8`, `+0xB`
takes `byte[02A5E8B0] << 4`, `+0xC` goes 1; then `0024E460` gates the
`003A3D20` mode (0/1/2 into `r12d`) before `003A2C70`, `008642A0`,
`0039CDC0`, `0020E670` and `0043E40C` run the multi-arm scan.
Interior anchor `0043DFC2` (the `0020E680` fetch).

## SWE2-EC7-84 update (2026-09-20) - `003A2C70` counted-index accessor measured

`003A2C70` (14 B) is the element-offset accessor the authored callers
run: the global count dword reads, `eax*4` returns - count to
4-stride index, call-free.
Interior anchor `003A2C76` (the `lea eax, [rax*4]`).

## SWE2-EC7-91 update (2026-09-20) - `0039C5D0` gated query-build measured

`0039C5D0` (213 B) is the staged query the expression callers
run: `0024D330` gates the fast path (straight into `0039C6B0`);
otherwise `0039B550` primes a table, `00399B80(rcx, &buf60,
&buf30, 4)` queries, `0039B780(rsi, &buf40, &buf30, 4)` builds
on a zero result, and a `02B409C8`-style flag chooses between
`0039DD60` and `0039DAD0` as the finisher - the whole body
under an `00808C40` cookie verify.
Interior anchor `0039C612` (the `0039C6B0` call).

`0039DD60` (861 B) is the expression body `0039C5D0` calls: `0020E680` and `0024E460` prepare, `003A3D20`, `003A2C70`, `008642A0`, `0039CDC0` and `0020E670` run the vector field math - the authored-expression evaluator's workbench step, same call family as the transform composers.

Interior anchor `0039DDA6` (function `0039DD60`).

`003992B0` (848 B) is the call-free SSE worker `004490D0` runs: `movups`/`mulps`/`shufps` on the `[rcx]` vector against the `022D91B0`/`022D91C8`/`022D91E0` constants, results stored to the `022D8F90`/`022D8FB0`/`022D8F9E` globals and `[r8]` - a vectorized evaluate-and-publish pass with no calls.

Interior anchor `00399452` (function `003992B0`).

`0039DAD0` (644 B) is the vector-pair builder `0039C5D0` calls (`0043D8F0` is its byte-channel twin): `0020E680` resolves the table, `008642A0(4)` allocs and `0039CDC0` inits the object, then eight `divss` pairs normalize `rdi[i]` by `rsi[i]` into the `+8` lane while `cvtdq2ps` bytes land in the `+0x10` lane - the family's normalized-float-pair emitter.

Interior anchor `0039DB04` (function `0039DAD0`).

`003B3160` (401 B) is the pool initializer `00259180` calls: `0036C1D0(8)` sizes it, then a loop clears each `0x38`-byte slot at `02EBCDA0` (seven qwords) and stamps `dword[rdx - 0x20] = 0x30000000 | (index & 0x3F)`; iteration 0 also stores `r9` at `+8` before `0024C550` runs - the `02EBCD80` record pool's reset.

Interior anchor `003B316C` (function `003B3160`).

`00375120` (338 B) is the table init `00259180` calls: 0x20 dwords zeroed at `02EBFA48` stride `0x70`, `02EC07E0` = 0x01010101 with `+4`/`+8` word/dword seeds, then `02ADB6E1` packs `eax += 0x11` per 4-byte entry to `0x110` - the randomness table's static fill.

Interior anchor `00375133` (function `00375120`).

`00506A40` (245 B) is the eight-lane s16 product `00506B40` runs: two `movups` load the `rdx`/`r8` 8xs16 vectors, each lane is `movsx`-widened and `imul`-paired against its counterpart, and the four dword products land in `[rcx]`/`+4`/`+8`/`+0xC` while mirroring into `022D9110`/`022D9114`/`022D9120`/`022D9124`/`022D9128` - the element-wise operand multiply the randomness consumer shares.

Interior anchor `00506A76` (function `00506A40`).

`003CD6E0` (210 B) is the lazy pool init `00259180` runs: `02B47790` gets a `0036C1D0(6)`-scoped `0036A100(0x800)` buffer and `02B47798` a `0x2800` one, cursors `02B47774`/`02B47778`/`02B47780`/byte `02B47770` reset, then 32 dwords stride `0x40` and 128 dwords stride `0x50` are zeroed - the two scratch pools behind authored-expression evaluation

Interior anchor `003CD6F5` (function `003CD6E0`).

`00502F30` (196 B) is the index-of-nth-flagged-row helper `00461270` calls: it scans the `+0x38`-counted `0x90`-stride table at `[rcx+0x10]+0x70` for the `edx`-th entry with flag bit 1 set, writes its index to `[r8]`, then counts the remaining flagged entries after it into `[r9]` and returns 1 - 0 with both outputs zeroed when the count is not reached

Interior anchor `00502FA6` (function `00502F30`).

`0039C6B0` (185 B) is the split-eval driver `0039C5D0` calls per authored expression: `0039B550` primes the `02AEECB0` shared record, `0039A770` splits `rdi` into the out-quads at `rsp+0x30` and `rsp+0x60`, `0039B780` runs the `rbp` lane with `r9 = 4`, then the `02AEE900` byte picks the commit - `0039E0C0` when set, `0039E420` when clear - both handed the split record plus the `ebx`/`rsi` argument pair

Interior anchor `0039C6FC` (function `0039C6B0`).

`0039E0C0` (861 B) is the `02AEE900`-set commit arm `0039C6B0` selects: the next `02F8F2F8` record (`word[02F8F2C6]` `*0x28`) takes a `0020E680`-resolved node at `+0x18`, four `rsi` fields fold by `cmova` into the `+0x8` minimum, `byte[02AEE910]<<4` ORs into `+0xB`, `+0xC` arms to 1, `0024E460`/`003A3D20`/`003A2C70` compose the `+0x20` flags, the count word bumps, and `008642A0`/`0039CF10` finish the record

Interior anchor `0039E106` (function `0039E0C0`).

`0039E420` (644 B) is the `02AEE900`-clear commit arm `0039C6B0` selects: `0020E680` resolves the record, `008642A0` and `0039CF10` initialise it (`+0x50` zeroed), then a `divss` sweep divides each `rdi` lane by the `rsi` divisor column (`+0/+4/+8/+0xC` against `rsi+0/+4`, `+0x10/+0x14` against `rsi+8`, and on) into the `[r14+8]` coefficient lanes - the normalised payload the split record stores

Interior anchor `0039E46F` (function `0039E420`).

`0039A770` (561 B) is the row-fold loop `0039C6B0` runs before the commit pick: `r9d` iterations take each `rcx` 16-byte row, `shufps` broadcasts the `+4`/`+8` lanes, and `mulss`/`addss` terms against the `022D91A0`..`022D91E8` constant bank accumulate into the `022D9300` mirror and the `022D91A0` result rows - the per-element matrix fold the expression split consumes

Interior anchor `0039A7F0` (function `0039A770`).

`0039CF10` (210 B) is the per-element normalise both commit arms (`0039E0C0`/`0039E420`) apply to their record: `0024E640` decides whether `0017FFD0` supplies the scalar `xmm6` or `1.0f` stands in, then `r8d` iterations of `0x10`-stride lanes run `00202B70` (the `02AEEB20` record) from `rsi` into `rdi` and perspective-divide - `+0/+4/+8` each divided by `+0xC`, `+0xC` self-divided to `1.0f`, and the x-lane finally multiplied by `xmm6`

Interior anchor `0039CF6E` (function `0039CF10`).

`003B4790` (168 B) is the lazy pool init `00259180` runs for the `02B404E0` record set - the same `0036C1D0`/`0036A100` arena pair as `003CD6E0`: first call `0036C1D0(6)`-scopes a `0036A100(0x1800)` buffer (then `0036C140`), seeds `02B404E8 = 3` and `02B404F8 = 5` with the `00D11520`/`00D11538` float-pair rows, zeroes 64 dwords on `0x60` stride under `+0x17A0`, and clears `02B404C0`..`02B404D0`

Interior anchor `003B47B1` (function `003B4790`).

`00431430` (165 B) is the mode-keyed combiner `0042FDB0` calls on the authored pair: `word[rcx+0xE] >> 4 & 0xF` selects one of six arms through the `004314BC` table - `rbx + r9`, `rbx - r9`, `2*r9 - r8 + rbx`, `(r9+1) * rbx`, or (modes 4/5 with `r8 != rbx`) `003A6E60(r8 - rbx)` + `rbx` - the authored random-range and offset arms the number evaluator lands on.

Interior anchor `0043144A` (function `00431430`).
