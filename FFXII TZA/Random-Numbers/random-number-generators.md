---
title: "Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the counter hash and the PPFX xorshift, with their constants, seeds and states"
kind: "system"
category: "Random numbers"
addresses: "0x00863BF0, 0x00863C80, 0x00866B90, 0x00866D60, 0x00863D30, 0x00328370, 0x00328D80, 0x0018EE20, 0x0018D740, 0x0015BCF0, 0x003D8E50, 0x004005E0, 0x006B05E0, 0x0074BDE0"
---

## What the player sees

Nothing in the game is random in the everyday sense; every roll comes from one of a handful of
generators that start from a known number and step through a fixed sequence.

- Hits, misses, damage spread, status chances and chest contents come from one generator that is
  reseeded from the clock every time a save is loaded, so reloading a save rerolls them.
- Loot drops, the chain coin, where enemies appear and which action an AI picks come from a second
  generator that restarts from a counter every time an area is entered, counting from the moment
  the game was started. A save load leaves it alone.
- Everything else, from noise textures to shaking effects, uses generators of its own that never
  touch those two.

Which roll uses which generator is on the [roll map page](which-roll-uses-which-generator.md).

## How it works

### The gameplay Mersenne Twister

The main gameplay generator is a standard MT19937 with its 624-word state at `0x02EB3870`, its
index at `0x02EB4230` and a seeded flag at `0x02EB4234`. Three functions draw or seed it, each reached
through a jump thunk:

| Function | Thunk | What it does |
|---|---|---|
| `0x00863BF0` | `0x00379CD0` | next 32-bit value |
| `0x00863C80` | `0x00379CE0` | next value as a float in [0, 1] |
| `0x00863D30` | `0x00379CF0` | seed with the argument |

Every one of the three first checks the flag `0x02EB4234`; when it is 0 it seeds with 5489
(`0x1571`, `0x00863C13`, `0x00863CA3`, `0x00863D57`) and sets the flag. A draw then refills the state when
the index is 624 (`0x00866B90`), takes `state[index]`, advances the index, and tempers it:

```c
y = state[i] ^ (state[i] >> 11);
y ^= (y & 0xFF3A58AD) << 7;       // the standard (y << 7) & 0x9D2C5680, rewritten by the compiler
y ^= (y & 0xFFFFDF8C) << 15;      // the standard (y << 15) & 0xEFC60000
return y ^ (y >> 18);             // 0x00863BF0; 0x00863C80 then multiplies by 1 / 4294967295.0 (double) and rounds to float
```

The seed `0x00866D60(seed)` is the textbook initialisation: `state[0] = seed`,
`state[i] = 0x6C078965 * (state[i-1] ^ (state[i-1] >> 30)) + i` for `i` = 1..623, and the index is
set to 624 so that the first draw refills (`0x00866D98`). The refill `0x00866B90` is the standard twist
with `0x9908B0DF` (written as `* -0x66F74F21`), in a four-lane SSE form when `0x01F44858` is 2 or more
and a scalar form otherwise, and ends with the index at 0 (`0x00866D31`).

The SSE form covers words 0-223, eight per iteration (`0x00866BF0`-`0x00866C7A`); the scalar loops then do
words 224-226 (`0x00866CB0`), 227-622 (`0x00866CF0`) and the last word (`0x00866D1D`-`0x00866D54`), the same
loops that do every word when `0x01F44858` is below 2.

### Seeding the gameplay Mersenne Twister

The seed function has exactly two callers:

1. **Boot.** The application's first frame mode `0x0022A0B0` seeds with `0x11B9` = 4537 (`0x0022A40B`-
   `0x0022A410`), after `0x00259180` has initialised the presentation generator. So the 5489 lazy seed is
   overwritten before any gameplay draw.
2. **Loading a save.** `0x00584210` seeds from the clock at `0x005843A5`-`0x005843D3`:

```python
t = _time64(NULL);                                        # IAT 0x008C3060, called at 0x0058439F
seed = (((lo32(t) + 0x2B5A5) * 0x21 + hi32(t)) & 0x7FFFFFFF) + 0x258 * frameCounter;  # 0x005843A5-0x005843B2, btr bit 0x80000000 at 0x005843BE; 0x005843B4, 0x005843C2; all 32-bit, wrapping
```

`frameCounter` is `0x01FD4A80`, which the application frame dispatcher `0x0022A580` increments once
per frame (`0x0022A59F`); nothing else writes it. `hi32(t)` is 0 before the year 2038.

The boot frame modes also draw from the generator and discard the value, once per dispatch:
mode 0 `0x0022B6E0` at `0x0022B706` and mode 1 `0x0022B7E0` at `0x0022B7EB`. The first gameplay draw
therefore reads the 4537 sequence at an offset equal to the number of those dispatches.

### The shared gameplay LCG

The second gameplay generator is one 32-bit word at `0x022C256C`. A draw steps the C-library
recurrence three times and assembles 31 bits from the high halves:

```python
a = state * 0x41C64E6D + 0x3039;
b = a     * 0x41C64E6D + 0x3039;
state = b     * 0x41C64E6D + 0x3039;                      # one store, after all three steps
draw = ((a >> 16 & 0x7FF) << 10 ^ (b >> 16 & 0x3FF)) << 10 ^ (state >> 16 & 0x3FF);  # 0x00328370
```

`0x00328370` is the out-of-line draw; it has 23 call sites in 15 functions. Seven more functions
carry the same three steps inline, reading and writing `0x022C256C` directly, so the multiplier
`0x41C64E6D` appears at 24 sites in 8 functions: `0x00328370`, `0x00317ED0`,
`0x003183D0`, `0x00318510`, `0x003185D0`, `0x003186F0`, `0x00318820` and `0x00319530` (three sites each). All
eight advance the same word, so every draw by any of them moves the others along.

### Seeding the shared gameplay LCG

`0x00328D80(seed)` stores the word and has one caller: the area initialisation `0x002342F0`
(`0x00234320`). The seed is the counter at `0x0208E6B0`, which `0x002342F0` reads and then increments
(`0x00234301`-`0x00234315`); those two instructions are the counter's only references in the image, so
it starts at 0 with the process and the generator is seeded 0, 1, 2, ... on successive area
initialisations. Loading a save does not touch the word or the counter.

### The graphics-noise Mersenne Twister

A second MT19937 instance lives in a caller-supplied block at `0x01F7F600`: 624 words, then a cursor
pointer at `+0x9C0` (`0x01F7FFC0`) and a remaining count at `+0x9C8` (`0x01F7FFC8`). Its seed
`0x0018D740(block, seed)` runs the same initialisation recurrence as `0x00866D60` and writes only the
624 words, and its refill `0x0018EE20(block)` is the same twist, scalar only, ending with the
count at 624 and the cursor at the array start (`0x0018EECD`-`0x0018EED8`).

`0x0018D740` holds a four-lane SSE copy of its loop behind `0x01F44858` being 2 or more (`0x0018D746`), but
the overlap test in front of it (`0x0018D773`-`0x0018D77B`) always picks the scalar loop
(`0x0018D820`-`0x0018D844`): each word is stored one word after the word it is computed from, so the SSE
body (`0x0018D7A0`-`0x0018D819`) never runs and the block is seeded by the scalar loop at every level.

It is seeded once, by the static initialiser `0x0015BCF0` (entry in the initialiser table at
`0x008C3200`): seed = `0x0018D680(_time64(NULL), clock())`, a byte-fold of the two values plus a call
counter at `0x01F7FFD0`, then `0x0018D740` and `0x0018EE20`. Its one consumer is the noise texture builder
`0x001946E0`, which draws two values per texel for 4,096 texels: an angle
`u × 2^-32 × 2π / 16` stored as cos and sin, and a scalar `u × 2^-32`, with the standard tempering
inline and the refill call before each draw (`0x0019483B`-`0x001948C9`). The state `0x01F7F600` has no other reference in the image.

### The C runtime rand

The C runtime `rand` (import at `0x008C3098`) has 48 direct call sites in 30 functions, plus the
stub `0x00861F38` called once from `0x00149610` (`0x0014963E`): 49 sites in 31 functions. It is the
CRT's own generator with per-thread state. `srand` (import `0x008C30A0`) has two callers: the Lua
binding `LuaMath_RandomSeed` (`0x008193E0`, `0x008193F0`), which seeds with its argument and discards
one `rand`, and the worker thread procedure `0x007A5400` (`0x007A540B`), which seeds its own thread's
state once at thread start. The callers are on the [roll map page](which-roll-uses-which-generator.md).

### The presentation bit-feedback generator

Presentation effects use a 32-bit shift register at `0x01EF93E8`, enabled by the word `0x022D9138`
(1 = run):

```python
feedback = (((state >> 18) ^ state) >> 4) & 1;
state = (((state & 0x003FFFFF) | 0x1FC00000) << 1) | feedback;  # the bits form a float in [1.0, 2.0)
```

| Function | Steps per call | Result |
|---|---|---|
| `0x003D8E50(A)` | 7 when enabled: 5 before the sample, 2 after (`0x003D8E95`-`0x003D8FBE`); 0 when `A` is 0 or the enable word is 0 | `f32(sample × A) − f32(A × vf00.w)`, with `vf00.w` at `0x01EF93FC` |
| `0x004005E0()` | 1 when enabled | `sample − 1.0`, in [0, 1); the sample is kept at `0x022D92E0` and copied to `0x022D8F90` |

`0x003D8E50` returns 0.0 at once for an `A` of 0 (`0x003D8E5D`-`0x003D8E6B`); a NaN `A` takes the drawing path. Otherwise
it saves the 16 bytes at `0x022D8F30` with `0x0036D930(1, 0x022D8F30)` (`0x003D8E78`) and puts them back with `0x0036D8E0`
before it returns (`0x003D8FE2`), which also sets the count `0x022D8F08` to 0 (`0x0036D91A`).

In between it writes `0x022D8F30` = `A` and `0x022D8F34` = 0, or `0xFFFFFFFF` for an `A` with the sign bit set
(`0x003D8F3F`-`0x003D8F44`), copies `0x022D8F30`-`0x022D8F3F` to `0x022D92E0` (`0x003D8F56`), and stores `0x022D91A0` = sample ×
`A` (`0x003D8F65`), `0x022D92E0` = the result (`0x003D8F71`) and `0x022D92F0` = the generator's new state read as a float,
or 1.0 when disabled (`0x003D8FCD`). It copies `0x022D92E0`-`0x022D92EF` back to `0x022D8F30` (`0x003D8FD5`) before the
restore.

`0x00259180` seeds it: `0x01EF93E8` = `0x022D92E0` = `0x458DC800` and `0x022D9138` = 1 (`0x00259216`);
it runs from the boot frame mode `0x0022A0B0` (`0x0022A406`). Ten functions touch the state directly:
the two above, the seed, and seven that step the recurrence inline (`0x003CCC20`, `0x003A6E60`,
`0x00515DA0`, `0x004010A0`, `0x0044B960`, `0x0044BAC0`, `0x00515FE0`). `0x003D8E50` has 220 call sites in 49
functions.

`0x004005E0` steps the register only while `0x022D9138` is non-zero (`0x004005E0`-`0x004005EF`). With the word
at 0 it leaves `0x01EF93E8` as it is and takes 1.0 from `0x01CEBBA8` as the sample (`0x004005F1`), so it
returns 0.0. On both paths it stores the sample at `0x022D92E0` (`0x00400625`), copies the 16 bytes
`0x022D92E0`-`0x022D92EF` to `0x022D8F90` (`0x0040062D`-`0x00400634`) and returns `sample − 1.0` (`0x00400647`).

### The counter hash

`0x006B05E0` is the script method `GenerateRandomFloat01` of `PRandomGenerator`: `0x006B04B0` registers the name (`0x00632FB0` at `0x006B052B`) and stores the address in its float caller record (`0x006B059F`-`0x006B05A6`), its only reference. It is not a recurrence: it increments the counter `0x02E50260` and hashes it:

```python
c = ++counter;                                            # 0x006B05E0-0x006B05EB
x = (c ^ 0x00BC602F) * 0x9E3779B9;                        # 0x006B05F1-0x006B05F6
y = ((x << 6) ^ (x >> 26) ^ x) * 0x9E3779B9;              # 0x006B0600-0x006B060A
r = ((y << 5) ^ (y >> 12)) + y;                           # 0x006B0614-0x006B061C
return (float)(u64)r * 2^-32;                    // 0x006B061E-0x006B0623, 0x008F30E0 = 0x2F800000; r >= 0xFFFFFF80 rounds to 1.0
```

The counter is zero in the image and has no other reference, so the k-th call returns the same
value in every run.

### The PPFX xorshift

The post-processing routine `0x0074BDE0` builds stratified unit-disk sample kernels with Marsaglia's
xorshift128, seeded from a counter: `c = ++[0x01F3CD6C]` (`0x0074BFE0`-`0x0074BFF5`; 1 in the image), then
`x, y, z, w` from four rounds of `0x6C078965 * (v ^ v >> 30) + i`. Each draw is

```python
t = x ^ (x << 11);  x = y; y = z; z = w;
w = w ^ (w >> 19) ^ t ^ (t >> 8);         # 0x0074C0A7-0x0074C0C4; the t >> 8 is an arithmetic shift (sar, 0x0074C0BD)
u = (w & 0x7FFFFFFF) * 2^-31;             # 0x0074C0C8-0x0074C0D1
```

The arithmetic shift makes this differ from the reference xorshift128 whenever `t` has its top bit
set. The counter and the kernels (`0x02EA24A0`) are referenced only from this routine.

The kernels are six sets of `0x400` bytes, one for each grid side from 3 to 8 (`0x02EA24A0 + 0x400 x (side - 3)`,
`0x0074BF8B`-`0x0074BF8F`), the side being the square root of the sample count. The first run builds all six and then
sets a byte (`0x0074BF10`-`0x0074BF20`, `0x0074C286`). Later runs rebuild only the set for the current side, and only while
the effect's byte `+0x1F8` is set (`0x0074BEFC`-`0x0074BF0E`). So each later rebuild draws again from the counter.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA3CA4` | `u8` | 0 (zero-filled tail of `.data`) | 1 once all six kernel sets have been built | `0x0074BDE0`, 1 (`0x0074C286`) | `0x0074BDE0` (`0x0074BEE0`) |

## Layouts

`Mt19937State` (`0x9C4` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32[624]` | state | the MT19937 state vector; `0x00866D60` (seed), `0x00866B90` (twist) |
| `+0x9C0` | `i32` | index | next word to draw, 624 = refill needed; `0x00866D60`, `0x00866B90`, `0x00863BF0`, `0x00863C80` |

The byte after the index, the seeded flag `0x02EB4234`, is a global of its own: `0x00863BF0`, `0x00863C80` and
`0x00863D30` test it and set it to 1 by its address (`0x00863BF4`-`0x00863C1E`, `0x00863C84`-`0x00863CBA`,
`0x00863D36`-`0x00863D5E`). Every access of the five gameplay functions to the state, the index and the flag is
RIP-relative. `0x02EB4235` to `0x02EB423F` have no RIP-relative reference.

`GraphicsNoiseMtState` (`0x9D0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32[624]` | state | the MT19937 state vector; `0x0018D740` (seed), `0x0018EE20` (twist) |
| `+0x9C0` | `u64` | cursor | pointer to the next word; `0x0018EE20`, `0x001946E0` |
| `+0x9C8` | `u32` | count | words left before a refill; `0x0018EE20`, `0x001946E0` |
| `+0x9CC` | `u8[4]` | pad | read and written by none of the three functions; nothing fixes its width |

## Operations

| Function | Role |
|---|---|
| `0x00863BF0` / `0x00379CD0` | gameplay MT: next u32 |
| `0x00863C80` / `0x00379CE0` | gameplay MT: next float in [0, 1] |
| `0x00863D30` / `0x00379CF0` | gameplay MT: seed |
| `0x00866D60`, `0x00866B90` | gameplay MT: initialise state, twist |
| `0x00328370` | shared LCG: three-step draw |
| `0x00328D80` | shared LCG: set state |
| `0x0018D740`, `0x0018EE20` | graphics-noise MT: initialise state, twist |
| `0x0015BCF0`, `0x0018D680` | graphics-noise MT: seed at process start, seed mixer |
| `0x003D8E50`, `0x004005E0` | presentation generator: scaled draw, unit draw |
| `0x00259180` | presentation generator: seed |
| `0x006B05E0` | counter hash, `PRandomGenerator` method `GenerateRandomFloat01` |
| `0x0074BDE0` | PPFX xorshift kernel builder |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02EB3870` | 624 × `u32` | gameplay MT state | `0x00866D60`, `0x00866B90` |
| `0x02EB422C` | `u32` | the state's last word, `state[623]`: the refill stops its loop before it (`0x00866CE2`) and computes it alone from itself, `state[0]` and `state[396]` at `0x02EB3EA0` (`0x00866D1D`, `0x00866D3B`, `0x00866D4E`) | `0x00866B90` (`0x00866D54`) |
| `0x02EB4230` | `i32` | gameplay MT index | `0x00866D60`, `0x00866B90`, `0x00863BF0`, `0x00863C80` |
| `0x02EB4234` | `u8` | gameplay MT seeded flag | `0x00863BF0`, `0x00863C80`, `0x00863D30` |
| `0x022C256C` | `u32` | shared LCG state | `0x00328370`, the seven inline sites, `0x00328D80` |
| `0x0208E6B0` | `u32` | shared LCG seed counter | `0x002342F0` |
| `0x01FD4A80` | `u32` | application frame counter, mixed into the save-load seed | `0x0022A580` |
| `0x01F7F600` | `0x9D0` | graphics-noise MT block | `0x0018D740`, `0x0018EE20`, `0x001946E0` |
| `0x01F7FFD0` | `u32` | graphics seed call counter | `0x0018D680` |
| `0x01EF93E8` | `u32` | presentation generator state | `0x00259180`, the ten functions above |
| `0x022D9138` | `u32` | presentation generator enable | `0x00259180` |
| `0x02E50260` | `u32` | counter hash counter | `0x006B05E0` |
| `0x01F3CD6C` | `u32` | PPFX kernel counter | `0x0074BDE0` |

## Modding notes

- To reproduce a gameplay MT sequence, seed with 4537 at boot, draw and discard once per boot-mode
  dispatch, and reseed from the clock formula above on every save load; the lazy 5489 seed never
  reaches gameplay. The float draw divides by 4294967295, not 4294967296.
- Every shared LCG draw advances the word three times. Stepping once per draw agrees with the game
  on the first roll at best.
- The LCG seed depends only on how many areas have been initialised since the process started.
- The presentation generator's draw must be computed in the written float order; the factored form
  `A × (sample − 1)` differs in the last bit for some inputs.

## Related

- [Which roll uses which generator: combat, chests, loot, the chain, spawning, AI, movement and presentation, what reseeds each, and what loading a save changes](which-roll-uses-which-generator.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](../Rewards-EXP-Gil-And-Loot/loot-drops.md)
- [Kill chain: chain count, chain level, the chain coin and resets](../Rewards-EXP-Gil-And-Loot/kill-chain.md)
