---
title: "Maths library: the C runtime maths imports, the inline SSE maths and the floating-point setup"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x008C2BB8, 0x00861F14, 0x0016A270, 0x02EADEF0, 0x007D0F60, 0x007D1140, 0x007E9030, 0x007EF1E0, 0x007F25E0, 0x007F1EC0, 0x00809900, 0x00809920, 0x0080A270, 0x0080B8A0, 0x01F44858, 0x0033CB70, 0x0033CEF0, 0x004686D0, 0x003A1960, 0x0031E620, 0x0038EAF0, 0x006E5A20, 0x0077A8C0, 0x008C2D18, 0x00380190"
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
are those of the installed runtime. 34 of them have an import stub in the run at `0x00861E90` (for
example `sqrtf` at `0x00861F14`, slot `0x008C2BB8`); the other 11 are called only through their slot.
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

One double-precision routine is linked into the executable instead: `0x008958C0(x)`, called twice by `0x00895DC0`
(`0x0089622D`, `0x0089624A`). It reduces the argument against the table at `0x0300E7D0`, picks one of 64 entries of 32
bytes at `0x0300E880` (a step of pi / 32, `0.09817477042088285`), and finishes with sine and cosine series; entry 16,
the one `x = 0` selects, holds 0 and 1.0, so it returns 1.0 for 0, and entry 32, the one `x = pi / 2` selects,
holds 0 and 0: a cosine at both points.

The other 25 imports have 7 sites or fewer each; `tanh`, `sinh`, `cosh`, `modf`, `log2f`, `log10f`,
`log10`, `fmodf`, `fmod`, `asin`, `acos` and `__setusermatherr` have one each.

### Only four scalar square roots are instructions

The code section has four `sqrtss` instructions and no `sqrtsd`, `rsqrtss` or `rcpss`:

- `0x0016A270` computes `0.9 / sqrt(16.0)` (constants at `0x008FCC8C` and `0x01CEBC84`) and stores 0.225
  at `0x02EADEF0`. It is a dynamic initialiser, named in the start-up table at `0x008C4AE8`.
- `0x007D0FB7` in `0x007D0F60` and `0x007D119B` in `0x007D1140` take the square root of a gain while
  computing the five coefficients of a shelving filter, each scaled by `0.9999` over the leading
  term. `0x007D1C80`, slot 8 of the `SQEX::Sd::Driver::Filter` vtable (`0x01CB7078`), jumps to both.
  - With `A` the gain (fourth argument), `q` the third, `C = 0x007B8BA0(w)`, `S = 0x007B8C80(w)`,
    `k = S x q x sqrt(A)`, `P = A + 1` and `M = A - 1`, the low shelf `0x007D1140` has `a0 = P + M C + k`,
    `b0 = A (P - M C + k)`, `b1 = 2A (M - P C)`, `b2 = A (P - M C - k)`, `a1 = -2 (M + P C)` and `a2 = P + M C - k`.
  - The high shelf `0x007D0F60` has `a0 = P - M C + k`, `b0 = A (P + M C + k)`, `b1 = -2A (M + P C)`,
    `b2 = A (P + M C - k)`, `a1 = 2 (M - P C)` and `a2 = P - M C - k`. Both store each times `0.9999 / a0`, in
    the order `a1`, `a2`, `b0`, `b1`, `b2`.
- `0x007E9184` in `0x007E9030`, which advances a time value at `+0x3C0` and interpolates between control
  points linearly or as a cubic.
  - With the curve `[+0x3B8]`, `t = min(time x 999.99994 / u32 [+0x24], 1)` (1 for a zero duration). Mode byte
    `+0x28` 0 gives `p = p0 + (p3 - p0) t`, mode 1 the cubic Bezier `(1 - t)^3 p0 + 3(1 - t)^2 t p1 + 3(1 - t) t^2 p2
    + t^3 p3`, with the points `(x, y)` at `+0x04`, `+0x0C`, `+0x14` and `+0x1C`.
  - `r = sqrt(x^2 + y^2)`, with `p` scaled to length 1 when `r > 1`; the ramp at `+0xB8` gets `atan2(x, y) / pi`
    (0 when `p` is zero) and the ramp at `+0xE8` gets `min(r, 1)` (`0x007E9030`).

### The sound engine's vector routines

Fourteen `sqrtps` and ten `rsqrtps` sit in `0x007EF1E0` to `0x007F74E0`, in virtual functions of the
sound engine's source classes: `0x007F25E0` is slot 34 of `SQEX::Sd::Lay::PolygonSound` (`0x01CB9F18`)
and `0x007F1EC0` slot 7 of `SQEX::Sd::Lay::DirectionSound` (`0x01CB9DD0`). `0x007EF1E0` shows the pattern:

1. A cross product from two shuffles, `0xC9` (y, z, x) and `0xD2` (z, x, y) (`0x007EF1F5` to `0x007EF242`).
2. A squared length: the product with itself, times the mask `1, 1, 1, 0` (`0x00D11570`), summed with
   two `haddps` (`0x007EF24F`).
3. A reciprocal square root, `rsqrtps` (`0x007EF257`), refined once:
   `y = (3 - x·y0·y0) · 0.5 · y0`, with `3.0` from `0x00D560A0` and `0.5` from `0x00D22600`.

Routines that use `sqrtps` take the exact root and load only the mask. What the sound engine does
with these values is on [spatial-sound.md](../Sound-And-Music/spatial-sound.md).

### Four-wide power routines

The runtime linked into the image carries four-wide `float` power routines with their tables in
`_RDATA`:

- `0x00809900` tests the CPU level the start-up probe `__isa_available_init` (`0x00809458`) stores at
  `0x01F44858`. At level 2 or above it jumps to `0x0080A000`, otherwise to `0x00809D80`. It is called once,
  from the post-effect library (`0x006EA4CF`).
- `0x00809920` is `jmp 0x0080A270`, called once from `0x00767052`, also in the post-effect library.
  `0x0080A270` widens the four inputs to `double` (`0x0080A298`), seeds a reciprocal with `rcpps`
  (`0x0080A339`, `0x0080A33D`, the only two in the image), and loads tables from `0x03006800`.
- For each lane flagged in a bit mask, `0x0080A270` calls the scalar routine `0x0080B8A0` with pointers to
  that lane's entries in three four-float arrays based at `r13` (`0x0080A710`).

### Angles and distance helpers

Angles are `float` radians. The read-only sections hold `pi` (`40490FDB`) twice and `2pi` four times,
with 192 and 246 code references; no `f32` constant equals 180/pi, 65536/2pi, 4096/2pi or their
inverses.

- `0x0033CB70` wraps an angle. When it is within ±4pi (`0x00D10B0C`, `0x00D10B20`) it adds or subtracts
  2pi until the result is in [-pi, pi]. Beyond that it subtracts 2pi times the truncated quotient
  once (`0x0033CBCD` to `0x0033CBE8`), so the result can lie between pi and 2pi in magnitude.
- `0x0033CEF0` turns a moving unit. Below 60 degrees of error (`0x0091572C`) it eases the turn rate:
  `rate = (1 - cos(3a)) / 2 · (rate - 1°) + 1°`, with one degree at `0x008C5F68`. The rest of the
  routine is on [battle-locomotion.md](../Movement-And-Pathfinding/battle-locomotion.md).
- `0x004686D0` returns `sqrtf((a.z - b.z)² + (a.x - b.x)²)` by tail-jumping to the `sqrtf` stub;
  `0x003A1960` is the same sum without the root, and `0x0031E620` is a forwarder to it. Neither reads
  `y` (`+4`).
- `0x00380190(out, axis, angle)` builds a quaternion from an axis and an angle: x, y and z are the
  axis divided by its length (`sqrtf`) times `sinf(angle / 2)`, w is `cosf(angle / 2)`. Its callers
  are the camera's sphere sweep `0x00230C10` and the scripted camera's matrix rebuild `0x003CBD60`.

### A power in the battle formulas

`0x0038EAF0` is reached through a pointer at `0x01EFAA40`. It computes `pow(2.0, n)` with the `double`
routine, where `n` is the byte at `+0x5B0E` of the object `0x02EBF190` points to, truncates the result
to an integer and stores it at `0x02AEE004`. What that value is in the damage step is on
[formula-slots.md](../Damage-And-Battle-Formulas/formula-slots.md).

### Floating-point control

No instruction in the code section loads or stores `MXCSR`. `_controlfp` (slot `0x008C2D18`) is called
at six sites in two post-effect routines, `0x006E5A20` and `0x0077A8C0`. Each reads the control word with
`_controlfp(0, 0)`, sets `0x10000` under the mask `0x30000` (`0x006E5AF3`), and at the end restores the
saved bits under the same mask (`0x006E97D8`). Two x87 helpers at `0x00125743` (`fldcw`) and `0x00125753`
(`fstcw`) have no references.

## Layouts

`Vec3Xz` (`0xC` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32` | x | read by the distance helpers |
| `+0x04` | `f32` | y | the height, which both helpers skip: each reads +`0x00` and +`0x08` only, so the distance is horizontal |
| `+0x08` | `f32` | z | read by the distance helpers |

## Shipped data

| Fact | Value |
|---|---|
| maths imports | 45 from `api-ms-win-crt-math-l1-1-0.dll`, 34 with a stub |
| maths call and jump sites | 1,563, of which `sqrtf` 570 |
| `sqrtss` sites | 4: `0x0016A270`, `0x007D0FB7`, `0x007D119B`, `0x007E9184` |
| `sqrtps` / `rsqrtps` / `rcpps` sites | 14 / 10 / 2 |
| `sqrtsd`, `rsqrtss`, `rcpss`, `ldmxcsr`, `stmxcsr` | 0 |
| `_controlfp` sites | 6 |
| `pi` / `2pi` as `f32` in read-only data | 2 / 4 copies |

## State

### The CPU probe's other outputs

The start-up probe `0x00809458`, called once from `0x00808959`, writes three globals besides the CPU level
`0x01F44858`. It reads the `cpuid` leaf 0 vendor string and tests it for `GenuineIntel` (`0x0080948B`-`0x008094D2`) and
`AuthenticAMD`, then reads leaf 1 (`0x008094DA`), and leaf 7 when leaf 0 reports 7 or more (`0x00809575`).

1. It sets `0x01F4485C` to 2 (`0x00809472`) as the level becomes 1 (`0x00809481`).
2. For `GenuineIntel` it sets `0x01F44860` to all ones (`0x008094F3`) and bit 2 of `0x02EAED88` (`0x00809504`), and bit 0
   when the leaf 1 signature masked with `0x0FFF3FF0` is `0x106C0`, `0x20660`, `0x20670`, `0x30650`, `0x30660` or
   `0x30670` (`0x0080953E`).
3. For `AuthenticAMD` it sets bit 2 of `0x02EAED88` when the leaf 1 signature masked with `0x0FF00F00` is at least
   `0x00600F00` (`0x0080955C`).
4. When leaf 7 `ebx` bit 9 is set it sets bit 1 of `0x02EAED88` (`0x00809590`).
5. When leaf 1 `ecx` bit 20 is set the level becomes 2 and `0x01F4485C` 6 (`0x0080959E`, `0x008095A8`). When `ecx` bits
   27 and 28 are also set and `xgetbv` reports both bits of `XCR0 & 6`, the level becomes 3 and `0x01F4485C` gains
   bit 3 (`0x008095E3`, `0x008095F1`). When leaf 7 `ebx` bit 5 is set as well, the level becomes 5 and `0x01F4485C` gains
   bit 5 (`0x008095FC`, `0x00809606`).

So `0x01F4485C` has bit n set for each level n the probe reached. No instruction outside the probe reads any of
the three: the probe's own reads are its loads of `0x02EAED88` (`0x008094B2`) and `0x01F4485C` (`0x008095DA`) and the
`or` on `0x01F44860`. No image-base-relative or disp32 reference and no data qword names them.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F4485C` | `u32` | 2 | one bit per CPU level the probe reached: 2 (level 1), 6 (level 2), `0xE` (level 3), `0x2E` (level 5) | `0x00809458` (`0x00809472`, `0x008095A8`, `0x008095F1`, `0x00809606`) | `0x00809458` (`0x008095DA`) only |
| `0x01F44860` | `u64` | `0x202F` | all ones on a `GenuineIntel` processor, otherwise its start value | `0x00809458` (`0x008094F3`) | `0x00809458` (`0x008094F3`, the read of the `or`) only |
| `0x02EAED88` | `u32` | 0 (zero-filled tail of `.data`) | bit 2: `GenuineIntel`, or `AuthenticAMD` with the leaf 1 signature at least `0x00600F00`; bit 0: `GenuineIntel` with one of the six signatures in step 2; bit 1: leaf 7 `ebx` bit 9 | `0x00809458` (`0x00809504`, `0x0080953E`, `0x0080955C`, `0x00809590`) | `0x00809458` (`0x008094B2`) only |

## Modding notes

- Hooking the `sqrtf` slot `0x008C2BB8` sees every scalar square root the game computes except the four
  `sqrtss` sites; it does not see the sound engine's four-wide routines.
- The scalar results come from the installed C runtime, so a replacement routine has to match that
  runtime's results, not a textbook formula, to keep identical low bits.
- Write facing values in radians and keep them within ±4pi, or wrap them yourself: above that
  `0x0033CB70` can return an angle outside [-pi, pi].
- Range tests built on `0x004686D0` and `0x003A1960` are cylinders; a replacement that includes height
  changes which targets are in range.
- `0x02EADEF0` is written once by its initialiser at start-up; a value written before that is
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
  that runs `0x0016A270`.
- [Runtime services](runtime-services.md): the other C runtime imports.
