---
title: "Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the counter hash and the PPFX xorshift, with their constants, seeds and states"
kind: "system"
category: "Random numbers"
addresses: "00863BF0, 00863C80, 00866B90, 00866D60, 00863D30, 00328370, 00328D80, 0018EE20, 0018D740, 0015BCF0, 003D8E50, 004005E0, 006B05E0, 0074BDE0"
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

The main gameplay generator is a standard MT19937 with its 624-word state at `02EB3870`, its
index at `02EB4230` and a seeded flag at `02EB4234`. Three functions draw or seed it, each reached
through a jump thunk:

| Function | Thunk | What it does |
|---|---|---|
| `00863BF0` | `00379CD0` | next 32-bit value |
| `00863C80` | `00379CE0` | next value as a float in [0, 1] |
| `00863D30` | `00379CF0` | seed with the argument |

Every one of the three first checks the flag `02EB4234`; when it is 0 it seeds with 5489
(`0x1571`, `00863C13`, `00863CA3`, `00863D57`) and sets the flag. A draw then refills the state when
the index is 624 (`00866B90`), takes `state[index]`, advances the index, and tempers it:

```c
y = state[i] ^ (state[i] >> 11);
y ^= (y & 0xFF3A58AD) << 7;       // the standard (y << 7) & 0x9D2C5680, rewritten by the compiler
y ^= (y & 0xFFFFDF8C) << 15;      // the standard (y << 15) & 0xEFC60000
return y ^ (y >> 18);             // 00863BF0; 00863C80 then multiplies by 1 / 4294967295.0 (double) and rounds to float
```

The seed `00866D60(seed)` is the textbook initialisation: `state[0] = seed`,
`state[i] = 0x6C078965 * (state[i-1] ^ (state[i-1] >> 30)) + i` for `i` = 1..623, and the index is
set to 624 so that the first draw refills (`00866D98`). The refill `00866B90` is the standard twist
with `0x9908B0DF` (written as `* -0x66F74F21`), in a four-lane SSE form when `01F44858` is 2 or more
and a scalar form otherwise, and ends with the index at 0 (`00866D31`).

### Seeding the gameplay Mersenne Twister

The seed function has exactly two callers:

1. **Boot.** The application's first frame mode `0022A0B0` seeds with `0x11B9` = 4537 (`0022A40B`-
   `0022A410`), after `00259180` has initialised the presentation generator. So the 5489 lazy seed is
   overwritten before any gameplay draw.
2. **Loading a save.** `00584210` seeds from the clock at `005843A5`-`005843D3`:

```c
t    = _time64(NULL);                                   // IAT 008C3060, called at 0058439F
seed = ((lo32(t) + 0x2B5A5) * 0x21 + hi32(t)) & 0x7FFFFFFF   // 005843A5-005843B2, btr bit 31 at 005843BE
     + 0x258 * frameCounter;                            // 005843B4, 005843C2
```

`frameCounter` is `01FD4A80`, which the application frame dispatcher `0022A580` increments once
per frame (`0022A59F`); nothing else writes it. `hi32(t)` is 0 before the year 2038.

The boot frame modes also draw from the generator and discard the value, once per dispatch:
mode 0 `0022B6E0` at `0022B706` and mode 1 `0022B7E0` at `0022B7EB`. The first gameplay draw
therefore reads the 4537 sequence at an offset equal to the number of those dispatches.

### The shared gameplay LCG

The second gameplay generator is one 32-bit word at `022C256C`. A draw steps the C-library
recurrence three times and assembles 31 bits from the high halves:

```c
a     = state * 0x41C64E6D + 0x3039;
b     = a     * 0x41C64E6D + 0x3039;
state = b     * 0x41C64E6D + 0x3039;                     // one store, after all three steps
draw  = ((a >> 16 & 0x7FF) << 10 ^ (b >> 16 & 0x3FF)) << 10 ^ (state >> 16 & 0x3FF);   // 00328370
```

`00328370` is the out-of-line draw; it has 23 call sites in 15 functions. Seven more functions
carry the same three steps inline, reading and writing `022C256C` directly, so an instruction
census of the multiplier `0x41C64E6D` finds 24 sites in 8 functions: `00328370`, `00317ED0`,
`003183D0`, `00318510`, `003185D0`, `003186F0`, `00318820` and `00319530` (three sites each). All
eight advance the same word, so every draw by any of them moves the others along.

### Seeding the shared gameplay LCG

`00328D80(seed)` stores the word and has one caller: the area initialisation `002342F0`
(`00234320`). The seed is the counter at `0208E6B0`, which `002342F0` reads and then increments
(`00234301`-`00234315`); those two instructions are the counter's only references in the image, so
it starts at 0 with the process and the generator is seeded 0, 1, 2, ... on successive area
initialisations. Loading a save does not touch the word or the counter.

### The graphics-noise Mersenne Twister

A second MT19937 instance lives in a caller-supplied block at `01F7F600`: 624 words, then a cursor
pointer at `+0x9C0` (`01F7FFC0`) and a remaining count at `+0x9C8` (`01F7FFC8`). Its seed
`0018D740(block, seed)` runs the same initialisation recurrence as `00866D60` (SSE form when
`01F44858` is 2 or more), and its refill `0018EE20(block)` is the same twist, ending with the
count at 624 and the cursor at the array start.

It is seeded once, by the static initialiser `0015BCF0` (entry in the initialiser table at
`008C3200`): seed = `0018D680(_time64(NULL), clock())`, a byte-fold of the two values plus a call
counter at `01F7FFD0`, then `0018D740` and `0018EE20`. Its one consumer is the noise texture builder
`001946E0`, which draws two values per texel for 4,096 texels: an angle
`u × 2^-32 × 2π / 16` stored as cos and sin, and a scalar `u × 2^-32`, with the standard tempering
inline and the refill call before each draw (`0019483B`-`001948C9`). The state `01F7F600` has no other reference in the image.

### The C runtime rand

The C runtime `rand` (import at `008C3098`) has 48 direct call sites in 30 functions, plus the
stub `00861F38` called once from `00149610` (`0014963E`): 49 sites in 31 functions. It is the
CRT's own generator with per-thread state. `srand` (import `008C30A0`) has two callers: the Lua
binding `LuaMath_RandomSeed` (`008193E0`, `008193F0`), which seeds with its argument and discards
one `rand`, and the worker thread procedure `007A5400` (`007A540B`), which seeds its own thread's
state once at thread start. The callers are on the roll map page.

### The presentation bit-feedback generator

Presentation effects use a 32-bit shift register at `01EF93E8`, enabled by the word `022D9138`
(1 = run):

```c
feedback = (((state >> 18) ^ state) >> 4) & 1;
state    = (((state & 0x003FFFFF) | 0x1FC00000) << 1) | feedback;   // the bits form a float in [1.0, 2.0)
```

| Function | Steps per call | Result |
|---|---|---|
| `003D8E50(A)` | 7 when enabled: 5 before the sample, 2 after (`003D8E95`-`003D8FBE`); 0 when `A` is 0 or the enable word is 0 | `f32(sample × A) − f32(A × vf00.w)`, with `vf00.w` at `01EF93FC` |
| `004005E0()` | 1 when enabled | `sample − 1.0`, in [0, 1); the sample is kept at `022D92E0` and copied to `022D8F90` |

`00259180` seeds it: `01EF93E8` = `022D92E0` = `0x458DC800` and `022D9138` = 1 (`00259216`);
it runs from the boot frame mode `0022A0B0` (`0022A406`). Ten functions touch the state directly:
the two above, the seed, and seven that step the recurrence inline (`003CCC20`, `003A6E60`,
`00515DA0`, `004010A0`, `0044B960`, `0044BAC0`, `00515FE0`). `003D8E50` has 220 call sites in 49
functions.

### The counter hash

The routine at `006B05E0` (code the analysis did not carve as a function) is not a recurrence: it increments the counter `02E50260` and hashes it:

```c
c = ++counter;                                   // 006B05E0-006B05EB
x = (c ^ 0x00BC602F) * 0x9E3779B9;               // 006B05F1-006B05F6
y = ((x << 6) ^ (x >> 26) ^ x) * 0x9E3779B9;     // 006B0600-006B060A
r = ((y << 5) ^ (y >> 12)) + y;                  // 006B0614-006B061C
return (float)(u64)r * 2^-32;                    // 006B061E-006B0623, 008F30E0 = 0x2F800000; r >= 0xFFFFFF80 rounds to 1.0
```

The counter is zero in the image and has no other reference, so the k-th call returns the same
value in every run.

### The PPFX xorshift

The post-processing routine `0074BDE0` builds stratified unit-disk sample kernels with Marsaglia's
xorshift128, seeded from a counter: `c = ++[01F3CD6C]` (`0074BFE0`-`0074BFF5`; 1 in the image), then
`x, y, z, w` from four rounds of `0x6C078965 * (v ^ v >> 30) + i`. Each draw is

```c
t = x ^ (x << 11);  x = y; y = z; z = w;
w = w ^ (w >> 19) ^ t ^ (t >> 8);      // 0074C0A7-0074C0C4; the t >> 8 is an arithmetic shift (sar, 0074C0BD)
u = (w & 0x7FFFFFFF) * 2^-31;          // 0074C0C8-0074C0D1
```

The arithmetic shift makes this differ from the reference xorshift128 whenever `t` has its top bit
set. The counter and the kernels (`02EA24A0`) are referenced only from this routine.

## Layouts

`Mt19937State` (`0x9C8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u32[624] state` | the MT19937 state vector; 00866D60 (seed), 00866B90 (twist) |  |
| `9C0` | `i32` | index | next word to draw, 624 = refill needed; `00866D60`, `00866B90`, `00863BF0`, `00863C80` |
| `9C4` | `u8` | seeded | 0 until the first seed; `00863BF0`, `00863C80`, `00863D30` |
| `9C5` | `u8[3]` | pad | not written by the five functions |

`GraphicsNoiseMtState` (`0x9D0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u32[624] state` | the MT19937 state vector; 0018D740 (seed), 0018EE20 (twist) |  |
| `9C0` | `u64` | cursor | pointer to the next word; `0018EE20`, `001946E0` |
| `9C8` | `u32` | count | words left before a refill; `0018EE20`, `001946E0` |
| `9CC` | `u32` | pad | not written by the three functions |

## Operations

| Function | Role |
|---|---|
| `00863BF0` / `00379CD0` | gameplay MT: next u32 |
| `00863C80` / `00379CE0` | gameplay MT: next float in [0, 1] |
| `00863D30` / `00379CF0` | gameplay MT: seed |
| `00866D60`, `00866B90` | gameplay MT: initialise state, twist |
| `00328370` | shared LCG: three-step draw |
| `00328D80` | shared LCG: set state |
| `0018D740`, `0018EE20` | graphics-noise MT: initialise state, twist |
| `0015BCF0`, `0018D680` | graphics-noise MT: seed at process start, seed mixer |
| `003D8E50`, `004005E0` | presentation generator: scaled draw, unit draw |
| `00259180` | presentation generator: seed |
| routine at `006B05E0` | counter hash |
| `0074BDE0` | PPFX xorshift kernel builder |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `02EB3870` | 624 × u32 | gameplay MT state | `00866D60`, `00866B90` |
| `02EB4230` | i32 | gameplay MT index | `00866D60`, `00866B90`, `00863BF0`, `00863C80` |
| `02EB4234` | u8 | gameplay MT seeded flag | `00863BF0`, `00863C80`, `00863D30` |
| `022C256C` | u32 | shared LCG state | `00328370`, the seven inline sites, `00328D80` |
| `0208E6B0` | u32 | shared LCG seed counter | `002342F0` |
| `01FD4A80` | u32 | application frame counter, mixed into the save-load seed | `0022A580` |
| `01F7F600` | `0x9D0` | graphics-noise MT block | `0018D740`, `0018EE20`, `001946E0` |
| `01F7FFD0` | u32 | graphics seed call counter | `0018D680` |
| `01EF93E8` | u32 | presentation generator state | `00259180`, the ten functions above |
| `022D9138` | u32 | presentation generator enable | `00259180` |
| `02E50260` | u32 | counter hash counter | `006B05E0` |
| `01F3CD6C` | u32 | PPFX kernel counter | `0074BDE0` |

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
