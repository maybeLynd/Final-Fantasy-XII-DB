---
title: "Authored expressions: the 16-byte value records in effect data, their operand kinds, curves and six operators, the random spread, and the colour forms"
kind: "system"
category: "Game files and data tables"
addresses: "004314E0, 00431350, 00431080, 003A6E60, 004309C0, 00430540, 004307C0, 003D8E50, 0039B630, 0039B6E0, 0042FDB0, 00431430, 00430370, 00430B90, 004308D0, 0020E600, 01EF93E8, 022D9138, 01EF93FC, 022D8F40"
---

## What the player sees

Two casts of the same spell never look quite the same: sparks leave at slightly different angles,
embers live slightly different times, a glow pulses on its own schedule. Most numbers authored in
effect data are not flat values but "this much, give or take that much", or a curve over time, and
they are rolled or sampled each time they are used. The roll comes from the presentation generator,
so it never touches damage, drops or anything else in play.

## How it works

### The expression record

An expression is a 16-byte record with two operands, A and B, and an operator. `004314E0(record, x)`
evaluates it as an integer and `004309C0(record, x)` as a float; `x` is the input a curve is
sampled at, usually a time or frame.

The evaluators' callers are presentation code: the effect
element runtime and types (`002F2530`, `00441B30`, `00442600`), the character rig (`003A4290`,
`003A56F0`), the character render records (`00422870`) and the model oscillators (`0040AA20`)
([effect element runtime](../Graphics/effect-element-runtime.md),
[character render records](../Graphics/character-render-records.md)).

Each operand is one of three kinds:

| Kind byte (`+0x0C` A, `+0x0D` B) | Value |
|---|---|
| 0 | absent: A is 0, and an absent B makes the result A |
| 1 | a reference: the dword at `+4` of the address the payload decodes to (`0020E600`) |
| 2 or more | a curve of that many `(x, y)` pairs, sampled at `x` (`00431080`, or `00430540` for floats) |

With B present the result is the operator applied to A and B: `00431350` for integers, `004307C0` for
floats.

### The operators

The operator is bits 4–7 of the word `+0x0E`. `f(n)` is a random value in `[0, n)` for positive `n`,
and in `(n, 0]` for negative `n` (below).

| Operator | Result | Meaning |
|---|---|---|
| 0, 6–15 | `a` | B is ignored |
| 1 | `a + f(b)` | `a` plus up to `b` |
| 2 | `a − f(b)` | `a` minus up to `b` |
| 3 | `a − b + f(2b)` | `a`, give or take `b` |
| 4 | `a × (f(b) + 1)` | `a` scaled by a random factor; in floats `a + a × f(b)` |
| 5 | `b == a ? a : a + f(b − a)` | a value from `a` towards `b` |

When `b` is 0 every operator returns `a`, except operator 5, which then returns `a + f(−a)`: a value
in `[1, a]` for positive `a`.

### The random draw

`003A6E60(n)` is `f` for integers. It steps the presentation generator `01EF93E8` (enabled by
`022D9138`) for a sample in `[1.0, 2.0)`, multiplies it by `n`, subtracts `n × [01EF93FC]` (1.0) and
truncates toward zero, then steps the generator once more. With the generator disabled the sample is
1.0 and every draw is 0. The float operators use `003D8E50`, the float draw on the same generator. The
generator and its other users are on the [RNG page](../Random-Numbers/random-number-generators.md).

### Curves

`00431080(record, x, operand)` reads the operand's pairs from the address its payload decodes to.
The count is the operand's kind byte, the period the `u16` at `+0x08` (A) or `+0x0A` (B), and the curve
mode bits 0–1 (A) or 2–3 (B) of `+0x0E`:

1. When the period is non-zero and smaller than `x`, `x` becomes `x % period`.
2. Mode 2 or 3 gives 0.
3. Mode 1 with three or more pairs is a quadratic B-spline. At or before the first pair it gives
   the first `y`, past the last pair the last `y`. From the first pair to the midpoint of the first
   two, and from the midpoint of the last two to the last pair, it interpolates linearly as in mode 0.
4. Elsewhere in mode 1 it takes the three pairs `(x0, y0)`, `(x1, y1)`, `(x2, y2)` around `x`, solves
   the curve's `x(t) = x` for `t` (`0039B6E0`) and evaluates `y(t)` (`0039B630`) as in the block
   below; the integer form rounds the result half away from zero, the float form `00430540` returns
   it as it is.
5. Mode 0, or mode 1 with fewer than three pairs, is linear. An `x` equal to a pair's `x` gives its
   `y`; between two pairs it gives `y0 + (y1 − y0)(x − x0) / (x1 − x0)` in integer arithmetic; past the
   last pair the last `y`; with no pairs 0.

```python
a = x0 - 2*x1 + x2,  b = x1 - x0                                 0039B6E6-0039B720
t = (sqrt(b*b - (x0 + x1 - 2*x) * a) - b) / a;  t = 2.0 if a == 0  0039B725-0039B769
y(t) = (1-t)^2/2 * y0 + ((1-t)*t + 0.5) * y1 + t^2/2 * y2         0039B64B-0039B6C7
```

In linear mode an `x` below the first pair's `x` interpolates from stack values no pair has set,
so the result is garbage.

### Colours

`0042FDB0(record, x)` evaluates a colour from four consecutive expression records (r, g, b, a) and
the mode byte `+0x40`:

- bits 0–1 = 0: each component is its own expression (`004314E0`);
- = 3: one value, the first record's, for r, g and b;
- = 1: each component combines the first record's channel-0 value with its own channel-1 operand;
- = 2: each component combines its own channel-0 value with the first record's channel-1 operand `b`
  and one shared draw `d = f(b)`, under the first record's operator (`00431430`): operator 1 adds
  `d`, 2 subtracts it, 4 gives `a × (d + 1)`, 3 gives `a − b + 2d`, and 5 draws afresh per
  component;
- alpha is always the fourth record's own expression.

With bit 2 of `+0x40` clear, the four values are clamped to 255 each (against `022D8F40`) and
packed as `r | g << 8 | b << 16 | a << 24`; there is no lower clamp, so a negative value keeps its low
byte. With bit 2 set they are converted by `00430370` instead.

`00430B90(out, record, x)` is the float RGB form, alpha always 1.0, with the mode byte `+0x30`:
bits 2–3 of 0 give black and of 1 white; otherwise bits 0–1 and the bytes `+0x31` and `+0x32` choose
which components have their own curves and which share one, and whether the spread is applied
per component (`004307C0`) or as one shared factor (`004308D0`).

## Layouts

```
expression record (0x10)
+0x00  u32  operand A payload (reference or curve address, encoded)
+0x04  u32  operand B payload
+0x08  u16  operand A curve period (0 = none)
+0x0A  u16  operand B curve period
+0x0C  u8   operand A kind (0 absent, 1 reference, 2+ curve pair count)
+0x0D  u8   operand B kind
+0x0E  u16  bits 0-1 A curve mode, bits 2-3 B curve mode, bits 4-7 operator
curve pair   s32 x, s32 y
```

The fields are listed access by access in
[`authored-expressions-record-accesses.tsv`](authored-expressions-record-accesses.tsv) and
[`authored-expressions-block-accesses.tsv`](authored-expressions-block-accesses.tsv).

## Operations

Per evaluation: up to two operand reads or curve walks (linear in the pair count), and one or two
generator steps per random draw.

## State

None of its own; each draw advances the presentation generator `01EF93E8`.

## Modding notes

- Start every linear curve at an `x` no larger than the smallest input it will see.
- A curve's period only wraps inputs above it; an input equal to the period is not wrapped.
- Operator 3 with spread `b` gives `a − b` up to just under `a + b`.
- Operator 5 with `b` = 0 is not a constant: it rolls in `[1, a]`.
- Colour components are packed from their low bytes after a cap at 255; keep them non-negative.

## Related

- [Random number generators](../Random-Numbers/random-number-generators.md): the presentation generator behind every draw.
- [Authored data tables](authored-data-tables.md): the address encoding that reference and curve payloads use.
