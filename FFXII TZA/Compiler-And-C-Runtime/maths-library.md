---
title: "Maths library: the C runtime maths imports, the inline SSE maths and the floating-point setup"
kind: "system"
category: "Compiler and C runtime"
addresses: "008C2BB8, 00861F14, 0016A270, 02EADEF0, 007D0F60, 007D1140, 007E9030, 007EF1E0, 007F25E0, 007F1EC0, 00809900, 00809920, 0080A270, 0080B8A0, 01F44858, 0033CB70, 0033CEF0, 004686D0, 003A1960, 0031E620, 0038EAF0, 006E5A20, 0077A8C0, 008C2D18, 00380190"
---

## What the player sees

Smooth movement and sound. A character turning to face a target eases in: the turn is slow when it
is nearly facing the right way and full speed from 60 degrees off. Range tests measure across the
ground and ignore height. Positional sound works out the direction and distance of each source with
four-wide vector code. Almost every sine, cosine, square root and power in the game is a call into
the C runtime that Windows provides, not code inside the executable.

## How it works

### Scalar maths comes from the system C runtime

The executable imports 45 functions from `api-ms-win-crt-math-l1-1-0.dll`, the API-set name the
Windows loader resolves to the system's universal C runtime, so their algorithms and coefficients
are those of the installed runtime. 34 of them have an import stub in the run at `00861E90` (for
example `sqrtf` at `00861F14`, slot `008C2BB8`); the other 11 are called only through their slot.
Together they are reached from 1,563 call or jump sites:

| Routine | Sites | Routine | Sites |
|---|---:|---|---:|
| `sqrtf` | 570 | `pow` | 34 |
| `sinf` | 175 | `floor` | 27 |
| `powf` | 136 | `log` | 24 |
| `cosf` | 109 | `atanf` | 22 |
| `logf` | 86 | `floorf` | 14 |
| `expf` | 65 | `_hypotf` | 12 |
| `tanf` | 60 | `exp`, `atan` | 11 each |
| `atan2f` | 53 | `cos` | 10 |
| `ceilf` | 37 | `acosf` | 9 |
| `sqrt` | 36 | `sin` | 8 |

One double-precision routine is linked into the executable instead: `008958C0(x)`, called twice by `00895DC0`
(`0089622D`, `0089624A`). It reduces the argument against the table at `0300E7D0`, picks one of 64 entries of 32
bytes at `0300E880` (a step of pi / 32, `0.09817477042088285`), and finishes with sine and cosine series; entry 16,
the one `x = 0` selects, holds 0 and 1.0, so it returns 1.0 for 0, and entry 32, the one `x = pi / 2` selects,
holds 0 and 0: a cosine at both points.

The other 25 imports have 7 sites or fewer each; `tanh`, `sinh`, `cosh`, `modf`, `log2f`, `log10f`,
`log10`, `fmodf`, `fmod`, `asin`, `acos` and `__setusermatherr` have one each.

### Only four scalar square roots are instructions

The code section has four `sqrtss` instructions and no `sqrtsd`, `rsqrtss` or `rcpss`:

- `0016A270` computes `0.9 / sqrt(16.0)` (constants at `008FCC8C` and `01CEBC84`) and stores 0.225
  at `02EADEF0`. It is a dynamic initialiser, named in the start-up table at `008C4AE8`.
- `007D0FB7` in `007D0F60` and `007D119B` in `007D1140` take the square root of a gain while
  computing the five coefficients of a shelving filter, each scaled by `0.9999` over the leading
  term. `007D1C80`, slot 8 of the `SQEX::Sd::Driver::Filter` vtable (`01CB7078`), jumps to both.
  - With `A` the gain (fourth argument), `q` the third, `C = 007B8BA0(w)`, `S = 007B8C80(w)`,
    `k = S x q x sqrt(A)`, `P = A + 1` and `M = A - 1`, the low shelf `007D1140` has `a0 = P + M C + k`,
    `b0 = A (P - M C + k)`, `b1 = 2A (M - P C)`, `b2 = A (P - M C - k)`, `a1 = -2 (M + P C)` and `a2 = P + M C - k`.
  - The high shelf `007D0F60` has `a0 = P - M C + k`, `b0 = A (P + M C + k)`, `b1 = -2A (M + P C)`,
    `b2 = A (P + M C - k)`, `a1 = 2 (M - P C)` and `a2 = P - M C - k`. Both store each times `0.9999 / a0`, in
    the order `a1`, `a2`, `b0`, `b1`, `b2`.
- `007E9184` in `007E9030`, which advances a time value at `+0x3C0` and interpolates between control
  points linearly or as a cubic.
  - With the curve `[+0x3B8]`, `t = min(time x 999.99994 / u32 [+0x24], 1)` (1 for a zero duration). Mode byte
    `+0x28` 0 gives `p = p0 + (p3 - p0) t`, mode 1 the cubic Bezier `(1 - t)^3 p0 + 3(1 - t)^2 t p1 + 3(1 - t) t^2 p2
    + t^3 p3`, with the points `(x, y)` at `+0x04`, `+0x0C`, `+0x14` and `+0x1C`.
  - `r = sqrt(x^2 + y^2)`, with `p` scaled to length 1 when `r > 1`; the ramp at `+0xB8` gets `atan2(x, y) / pi`
    (0 when `p` is zero) and the ramp at `+0xE8` gets `min(r, 1)` (`007E9030`).

### The sound engine's vector routines

Fourteen `sqrtps` and ten `rsqrtps` sit in `007EF1E0` to `007F74E0`, in virtual functions of the
sound engine's source classes: `007F25E0` is slot 34 of `SQEX::Sd::Lay::PolygonSound` (`01CB9F18`)
and `007F1EC0` slot 7 of `SQEX::Sd::Lay::DirectionSound` (`01CB9DD0`). `007EF1E0` shows the pattern:

1. A cross product from two shuffles, `0xC9` (y, z, x) and `0xD2` (z, x, y) (`007EF1F5` to `007EF242`).
2. A squared length: the product with itself, times the mask `1, 1, 1, 0` (`00D11570`), summed with
   two `haddps` (`007EF24F`).
3. A reciprocal square root, `rsqrtps` (`007EF257`), refined once:
   `y = (3 - x·y0·y0) · 0.5 · y0`, with `3.0` from `00D560A0` and `0.5` from `00D22600`.

Routines that use `sqrtps` take the exact root and load only the mask. What the sound engine does
with these values is on [spatial-sound.md](../Sound-And-Music/spatial-sound.md).

### Four-wide power routines

The runtime linked into the image carries four-wide `float` power routines with their tables in
`_RDATA`:

- `00809900` tests the CPU level the start-up probe `__isa_available_init` (`00809458`) stores at
  `01F44858`. At level 2 or above it jumps to `0080A000`, otherwise to `00809D80`. It is called once,
  from the post-effect library (`006EA4CF`).
- `00809920` is `jmp 0080A270`, called once from `00767052`, also in the post-effect library.
  `0080A270` widens the four inputs to `double` (`0080A298`), seeds a reciprocal with `rcpps`
  (`0080A339`, `0080A33D`, the only two in the image), and loads tables from `03006800`.
- For each lane flagged in a bit mask, `0080A270` calls the scalar routine `0080B8A0` with pointers to
  that lane's entries in three four-float arrays based at `r13` (`0080A710`).

### Angles and distance helpers

Angles are `float` radians. The read-only sections hold `pi` (`40490FDB`) twice and `2pi` four times,
with 192 and 246 code references; no `f32` constant equals 180/pi, 65536/2pi, 4096/2pi or their
inverses.

- `0033CB70` wraps an angle. When it is within ±4pi (`00D10B0C`, `00D10B20`) it adds or subtracts
  2pi until the result is in [-pi, pi]. Beyond that it subtracts 2pi times the truncated quotient
  once (`0033CBCD` to `0033CBE8`), so the result can lie between pi and 2pi in magnitude.
- `0033CEF0` turns a moving unit. Below 60 degrees of error (`0091572C`) it eases the turn rate:
  `rate = (1 - cos(3a)) / 2 · (rate - 1°) + 1°`, with one degree at `008C5F68`. The rest of the
  routine is on [battle-locomotion.md](../Movement-And-Pathfinding/battle-locomotion.md).
- `004686D0` returns `sqrtf((a.z - b.z)² + (a.x - b.x)²)` by tail-jumping to the `sqrtf` stub;
  `003A1960` is the same sum without the root, and `0031E620` is a forwarder to it. Neither reads
  `y` (`+4`).
- `00380190(out, axis, angle)` builds a quaternion from an axis and an angle: x, y and z are the
  axis divided by its length (`sqrtf`) times `sinf(angle / 2)`, w is `cosf(angle / 2)`. Its callers
  are the camera's sphere sweep `00230C10` and the scripted camera's matrix rebuild `003CBD60`.

### A power in the battle formulas

`0038EAF0` is reached through a pointer at `01EFAA40`. It computes `pow(2.0, n)` with the `double`
routine, where `n` is the byte at `+0x5B0E` of the object `02EBF190` points to, truncates the result
to an integer and stores it at `02AEE004`. What that value is in the damage step is on
[formula-slots.md](../Damage-And-Battle-Formulas/formula-slots.md).

### Floating-point control

No instruction in the code section loads or stores `MXCSR`. `_controlfp` (slot `008C2D18`) is called
at six sites in two post-effect routines, `006E5A20` and `0077A8C0`. Each reads the control word with
`_controlfp(0, 0)`, sets `0x10000` under the mask `0x30000` (`006E5AF3`), and at the end restores the
saved bits under the same mask (`006E97D8`). Two x87 helpers at `00125743` (`fldcw`) and `00125753`
(`fstcw`) have no references.

## Layouts

`Vec3Xz` (`0xC` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | x | read by the distance helpers |
| `+0x04` | `f32` | y | not read by `004686D0` or `003A1960` |
| `+0x08` | `f32` | z | read by the distance helpers |

## Shipped data

| Fact | Value |
|---|---|
| maths imports | 45 from `api-ms-win-crt-math-l1-1-0.dll`, 34 with a stub |
| maths call and jump sites | 1,563, of which `sqrtf` 570 |
| `sqrtss` sites | 4: `0016A270`, `007D0FB7`, `007D119B`, `007E9184` |
| `sqrtps` / `rsqrtps` / `rcpps` sites | 14 / 10 / 2 |
| `sqrtsd`, `rsqrtss`, `rcpss`, `ldmxcsr`, `stmxcsr` | 0 |
| `_controlfp` sites | 6 |
| `pi` / `2pi` as `f32` in read-only data | 2 / 4 copies |

## Modding notes

- Hooking the `sqrtf` slot `008C2BB8` sees every scalar square root the game computes except the four
  `sqrtss` sites; it does not see the sound engine's four-wide routines.
- The scalar results come from the installed C runtime, so a replacement routine has to match that
  runtime's results, not a textbook formula, to keep identical low bits.
- Write facing values in radians and keep them within ±4pi, or wrap them yourself: above that
  `0033CB70` can return an angle outside [-pi, pi].
- Range tests built on `004686D0` and `003A1960` are cylinders; a replacement that includes height
  changes which targets are in range.
- `02EADEF0` is written once by its initialiser at start-up; a value written before that is
  overwritten.

## Related

- [Thunks and import stubs](thunks-and-import-stubs.md): the stub run and the import table.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md): the turn and wrap routines
  in context.
- [Facing and steering](../Movement-And-Pathfinding/facing-and-steering.md): the angles a unit
  carries.
- [Spatial sound](../Sound-And-Music/spatial-sound.md): the sound classes that own the vector routines.
- [YEBIS and PPFX](../Third-Party-Libraries/yebis-ppfx-post-effects.md): the library that calls the
  power routines and `_controlfp`.
- [Formula slots](../Damage-And-Battle-Formulas/formula-slots.md): where the power of two is used.
- [Static initialisation and teardown](static-initialisation-and-teardown.md): the start-up table
  that runs `0016A270`.
- [Runtime services](runtime-services.md): the other C runtime imports.
