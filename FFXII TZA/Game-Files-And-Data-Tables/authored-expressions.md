[Home](../../README.md) / [Game files and data tables](README.md) / Authored expressions

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Authored expressions: the 16-byte value records in effect data, their operand kinds, curves and six operators, the random spread, and the colour forms | system | Game files and data tables | Data tables and configs | How a number authored in effect data becomes a value: the 16-byte expression record with two operands, the constant, reference and curve operand kinds, the linear and B-spline curves over (x, y) pairs with an optional period, the six operators that add a random spread from the presentation generator, the integer and float evaluators, the four-record colour evaluator and the float RGB evaluator, and the edge cases authored data has to respect. | 0x004314E0, 0x00431350, 0x00431080, 0x003A6E60, 0x004309C0, 0x00430540, 0x004307C0, 0x003D8E50, 0x0039B630, 0x0039B6E0, 0x0042FDB0, 0x00431430, 0x00430370, 0x00430B90, 0x004308D0, 0x0020E600, 0x01EF93E8, 0x022D9138, 0x01EF93FC, 0x022D8F40 |

## What the player sees

Two casts of the same spell never look quite the same: sparks leave at slightly different angles,
embers live slightly different times, a glow pulses on its own schedule. Most numbers authored in
effect data are not flat values but "this much, give or take that much", or a curve over time, and
they are rolled or sampled each time they are used. The roll comes from the presentation generator,
so it never touches damage, drops or anything else in play.

## How it works

### The expression record

An expression is a 16-byte record with two operands, A and B, and an operator. `0x004314E0(record, x)`
evaluates it as an integer and `0x004309C0(record, x)` as a float; `x` is the input a curve is
sampled at, usually a time or frame.

The evaluators' callers are presentation code: the effect
element runtime and types¹ and the character rig (`0x003A4290`,
`0x003A56F0`, through the float RGB form `0x00430B90` at `0x003A4303` and `0x003A575E`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F2530`, `0x00441B30`, `0x00442600` |

</details>

The draws below also have direct callers in presentation code: the character render records¹ call
`0x003A6E60`² and the model oscillators³ call `0x003D8E50`⁴
([effect element runtime](../Graphics/effect-element-runtime.md),
[character render records](../Graphics/character-render-records.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00422870` |
| ² | `0x00422919` |
| ³ | `0x0040AA20` |
| ⁴ | `0x0040AA78`, `0x0040AA92` |

</details>

Each operand is one of three kinds:

| Kind byte (`+0x0C` A, `+0x0D` B) | Value |
|---|---|
| 0 | absent: A is 0, and an absent B makes the result A |
| 1 | a reference: the dword at `+4` of the address the payload decodes to (`0x0020E600`) |
| 2 or more | a curve of that many `(x, y)` pairs, sampled at `x` (`0x00431080`, or `0x00430540` for floats) |

With B present the result is the operator applied to A and B: `0x00431350` for integers, `0x004307C0` for
floats.

Every expression the shipped effect streams hold, with its operands, curve points and owner, is listed under
[What each effect stream holds](../Graphics/effect-files-efx-efb.md#what-each-effect-stream-holds).

### The operators

The operator is bits `0xF0` of the word `+0x0E`. `f(n)` is a random value in `[0, n)` for positive `n`,
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
in `[1, a]` for a positive integer `a` and in `(0, a]` for a positive float.

### The random draw

`0x003A6E60(n)` is `f` for integers. It steps the presentation generator `0x01EF93E8` (enabled by
`0x022D9138`) five times for a sample `s` in `[1.0, 2.0)`¹, multiplies it by `n`, `s × n`,
subtracts `n × [0x01EF93FC]` (1.0) and truncates toward zero, `(int)(s × n - n × 1.0)`², then steps the generator twice more³. It does not test `n`, so
`0x003A6E60(0)` steps the generator seven times as well. With the generator disabled the sample is 1.0 and every
draw is 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A6E7B`-`0x003A6F12` |
| ² | `0x003A6F2D`-`0x003A6F41`, `0x003A6FA9` |
| ³ | `0x003A6F52`-`0x003A6F8C` |

</details>

Each call also writes the scratch dwords `0x022D91A0`, `0x022D92E0`-`0x022D92EF` and `0x022D92F0`: `0x022D91A0` =
sample × `n`¹, `0x022D92E0` = sample × `n` − `n` × 1.0², then the four dwords
`0x022D92E0`-`0x022D92EF` truncated to integers in place, `cvttps2dq xmm1, xmm0`³ stored back by
`movups`⁴, and `0x022D92F0` = the generator's new state read as a float, or 1.0 with the generator
disabled⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A6F39` |
| ² | `0x003A6F45` |
| ³ | `0x003A6FA9` |
| ⁴ | `0x003A6FAD` |
| ⁵ | `0x003A6FA1` |

</details>

The float operators use `0x003D8E50`, the float draw on the same generator. The generator and its other users are
on the [RNG page](../Random-Numbers/random-number-generators.md).

### Curves

`0x00431080(record, x, operand)` reads the operand's pairs from the address its payload decodes to.
The count is the operand's kind byte, the period the `u16` at `+0x08` (A) or `+0x0A` (B), and the curve
mode bits `0x3` (A) or `0xC` (B) of `+0x0E`:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | When the period is non-zero and smaller than `x`, `x` becomes `x % period`. |   |
| 2 | Mode 2 or 3 gives 0. |   |
| 3 | Mode 1 with three or more pairs is a quadratic B-spline. At or before the first pair it gives the first `y`, past the last pair the last `y`. From the first pair to the midpoint of the first two, and from the midpoint of the last two to the last pair, it interpolates linearly as in mode 0. |   |
| 4 | Elsewhere in mode 1 it takes the three pairs `(x0, y0)`, `(x1, y1)`, `(x2, y2)` around `x`, solves the curve's `x(t) = x` for `t` and evaluates `y(t)` as in the block below; the integer form rounds the result half away from zero, the float form `0x00430540` returns it as it is. | `0x0039B6E0`<br>`0x0039B630` |
| 5 | Mode 0, or mode 1 with fewer than three pairs, is linear. An `x` equal to a pair's `x` gives its `y`; between two pairs it gives `y0 + (y1 − y0)(x − x0) / (x1 − x0)` in integer arithmetic; past the last pair the last `y`; with no pairs 0. |   |

```python
a = x0 - 2*x1 + x2,  b = x1 - x0                                 0x0039B6E6-0x0039B720
t = (sqrt(b*b - (x0 + x1 - 2*x) * a) - b) / a;  t = 2.0 if a == 0  0x0039B725-0x0039B769
t = (2*x - x0 - x1) / (x2 - x0)  if t == 2.0                       0x00431260-0x0043128C, 0x004306F0-0x0043071C
y(t) = (1-t)^2/2 * y0 + ((1-t)*t + 0.5) * y1 + t^2/2 * y2         0x0039B64B-0x0039B6C7
```

`0x0039B6E0(x, points, out)` stores 2.0 when `a` is 0¹, and both curve readers replace a returned 2.0
with the straight-line solution of the third line²; the square root
is the C runtime `sqrtf`³. `0x0039B630(t, points, out)` applies the `y(t)` weights to the first three
floats of each of the three points, 16 bytes apart, and writes three floats⁴.
The readers put `x` and `y` first in each point and keep the second result, `y`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0039B72C` |
| ² | `0x00431260`-`0x0043128C`, `0x004306F0`-`0x0043071C` |
| ³ | `0x0039B752` |
| ⁴ | `0x0039B692`, `0x0039B6AE`, `0x0039B6CF` |
| ⁵ | `0x0043072C`, `0x0043129C` |

</details>

The float form `0x00430540` reads each pair's `y` as an `f32`¹. In linear mode it computes
`y0 + (y1 − y0) × (x − x0) / (x1 − x0)` in floats, taking the two `x` differences as integers first².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00430603`, `0x004306C6` |
| ² | `0x00430773`-`0x00430793` |

</details>

In linear mode an `x` below the first pair's `x` interpolates from stack values no pair has set,
so the result is garbage.

### Colours

`0x0042FDB0(record, x)` evaluates a colour from four consecutive expression records (r, g, b, a) and
the mode byte `+0x40`:

- mask `0x3` = 0: each component is its own expression¹;
- = 3: one value, the first record's, for r, g and b;
- = 1: each component combines the first record's channel-0 value with its own channel-1 operand;
- = 2: each component combines its own channel-0 value with the first record's channel-1 operand `b`
  and one shared draw `d = f(b)`, under the first record's operator²: operator 1 adds
  `d`, 2 subtracts it, 4 gives `a × (d + 1)`, 3 gives `a − b + 2d`, and 5 draws afresh per
  component, `a + f(b − a)`, or `a` when `b` equals `a`³;
- in mode 2 operators 0 and 6-15 give `a`, and with `b` = 0 every operator gives `a` except 5
 ⁴;
- alpha is always the fourth record's own expression.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004314E0` |
| ² | `0x00431430` |
| ³ | `0x004314A6`-`0x004314B3` |
| ⁴ | `0x00431438`-`0x0043146E`, `0x00431492`-`0x004314A4` |

</details>

With bit `0x4` of `+0x40` clear, the four values are clamped to 255 each, `v > 255 ? 255 : v` (against
`0x022D8F40`), and packed as `r | g << 8 | b << 16 | a << 24`; there is no lower clamp, so a negative value keeps
its low byte. With bit `0x4` set they are converted by `0x00430370` instead¹, which reads them as
hue, saturation, value and alpha and packs the same four bytes:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004300BE`-`0x004300D4` |

</details>

- saturation and value are capped at 255 and divided by 255.0, `s = min(S, 255) / 255.0` and
  `v = min(V, 255) / 255.0`¹; a saturation of 0 gives grey, the value in each of r, g
  and b²;
- otherwise a hue of 360 or more becomes 0, `h >= 360.0 ? 0.0 : h`³, and the hue divided
  by 60.0, `h / 60.0`⁴, is split by `floorf` into a sector `i` and a fraction `f`
 ⁵;
- with `p = v(1 − s)`, `q = v(1 − s·f)` and `t = v(1 − s(1 − f))`, sectors 1 to 5 give (r, g, b) =
  (q, v, p), (p, v, t), (p, q, v), (t, p, v) and (v, p, q); any other sector, 0 or a negative one, gives
  (v, t, p)⁶;
- r, g and b are multiplied by 255.0 and truncated, and their low bytes are stored, `(int)(c * 255.0) & 0xFF`
  for each `c`⁷;
- alpha is the fourth value capped at 255 with no lower clamp, `a > 255 ? 255 : a`⁸.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0043037A`-`0x004303D3` |
| ² | `0x004303CB`-`0x004303E1` |
| ³ | `0x004303E6`-`0x004303F0` |
| ⁴ | `0x004303F4` |
| ⁵ | `0x004303F4`-`0x00430423` |
| ⁶ | `0x00430406`-`0x00430499` |
| ⁷ | `0x004304AD`-`0x004304D7` |
| ⁸ | `0x004304A2`, `0x004304DA`-`0x004304E7` |

</details>

`0x00430B90(out, record, x)` is the float RGB form over three consecutive expression records (r, g, b), alpha
always 1.0¹, with the mode byte `+0x30`: bits `0xC` of 0 give black and of 1 white². Otherwise bits `0x3` and the bytes `+0x31` and `+0x32` choose:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00431032` |
| ² | `0x00430BAC`-`0x00430BDA` |

</details>

- bits `0x3` = 0: each component is its own expression¹;
- bits `0x3` = 3 with `+0x31` and `+0x32` both 0: one value for r, g and b, the first record's two operands
 ² combined once by `0x004307C0`³;
- in every other case operand A is taken first (`0x00430540(record, x, 0)`): with bit `0x1` clear each component
  takes its own record's⁴;
- with bit `0x1` set, `+0x31` = 0 gives the first record's A to r, g and b, 1 the first record's to r and g
  and the third's to b, 2 the first record's to r and b and the second's to g, and 3 the second record's to g
  and b and the first's to r⁵. Any other `+0x31` stores nothing, and the next step
  works on what `out` held⁶;
- the spread follows (`b` = `0x00430540(record, x, 1)`): with bit `0x2` clear each component is combined with
  its own record's `b` by `0x004307C0`⁷;
- with bit `0x2` set `+0x32` groups the components as `+0x31` does, and a group shares one `b` and one draw
  `d = 0x003D8E50(b)`, 0 when `b` is 0, through `0x004308D0`: the first record's for r, g and b (0), for r and g
  (1), for r and b (2), the second record's for g and b (3)⁸;
- the component left over then goes to `0x004307C0` under its own record, the third, second or first, with
  `0x003D8E50(b)` in place of that record's `b` when `b` is not 0, a value `0x004307C0` draws on again under
  operators 1 to 5
 ⁹. Any other
  `+0x32` applies no spread¹⁰.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004309C0`, `0x00430BF6`-`0x00430C1A` |
| ² | `0x00430540` |
| ³ | `0x00430C29`-`0x00430C71` |
| ⁴ | `0x00430D22`-`0x00430D54` |
| ⁵ | `0x00430C83`-`0x00430D54` |
| ⁶ | `0x00430C95`-`0x00430C98` |
| ⁷ | `0x00430F9F`-`0x0043100B` |
| ⁸ | `0x00430D68`-`0x00430F98` |
| ⁹ | `0x00430F1D`-`0x00430F2D` and `0x00430FFA`-`0x0043100B`, `0x00430E89`-`0x00430EAB`, `0x00430DF8`-`0x00430E18` |
| ¹⁰ | `0x00430D86`-`0x00430D89` |

</details>

`0x004308D0(record, a, b, d)` combines `a` with a draw `d` that its caller made once (`0x00430DA3`-`0x00430DB5`,
`0x00430E37`-`0x00430E49`, `0x00430ECB`-`0x00430EDD` and `0x00430F4D`-`0x00430F59` in `0x00430B90`), under the record's
operator, as `0x00431430` does in integers: operator 1 gives `a + d`, 2 `a − d`,
3 `a − b + 2d`, 4 `a + a × d`, and 5 draws afresh, `a + f(b − a)` with `0x003D8E50`, or `a` when `b` equals `a`¹. Operators 0 and 6-15 give `a`, and with `b` = 0 every operator gives `a` except 5².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0043090B`-`0x004309A3` |
| ² | `0x004308D4`-`0x004308FE` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

Expression record (`0x10`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | operand A payload (reference or curve address, encoded) |
| `+0x04` | `u32` |  | operand B payload |
| `+0x08` | `u16` |  | operand A curve period (0 = no wrap; the curve is still evaluated) |
| `+0x0A` | `u16` |  | operand B curve period |
| `+0x0C` | `u8` |  | operand A kind (0 absent, 1 reference, 2+ curve pair count) |
| `+0x0D` | `u8` |  | operand B kind |
| `+0x0E` | `u16` |  | mask `0x3` A curve mode, mask `0xC` B curve mode, bits `0xF0` operator |

```
curve pair   s32 x, s32 y (f32 y when the float form 0x00430540 reads it)
```

The fields are listed access by access in
[`authored-expressions-record-accesses.tsv`](authored-expressions-record-accesses.tsv) and
[`authored-expressions-block-accesses.tsv`](authored-expressions-block-accesses.tsv).

</details>

## Operations

Per evaluation: up to two operand reads or curve walks (linear in the pair count), and seven
generator steps per random draw while the generator is enabled, five before the sample and two after:
`0x003A6E60` on every call, `0x003D8E50` unless its amplitude is 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003D8E5D`-`0x003D8E6B` |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

None of its own; each draw advances the presentation generator `0x01EF93E8`.

</details>

## Modding notes

- Start every linear curve at an `x` no larger than the smallest input it will see.
- A curve's period only wraps inputs above it; an input equal to the period is not wrapped.
- Operator 3 with spread `b` gives `a − b` up to just under `a + b`.
- Operator 5 with `b` = 0 is not a constant: it rolls in `[1, a]` for integers and `(0, a]` for floats.
- Colour components are packed from their low bytes after a cap at 255; keep them non-negative.

## Related

- [Random number generators](../Random-Numbers/random-number-generators.md): the presentation generator behind every draw.
- [Authored data tables](authored-data-tables.md): the address encoding that reference and curve payloads use.
