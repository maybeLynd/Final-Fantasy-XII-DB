---
system: The maths the game runs on
category: 24-Compiler-And-CRT-Runtime
status: AUDITED
owner_layer: CodeDomain:Microsoft.MSVCCRT_STL_Runtime + Runtime.SIMD (call sites cross into Movement, Presentation, UI)
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-independent-instruction-census
  crossref_clean: true
  reopened_count: 0
---

# The maths the game runs on

> Every square root, sine and arctangent in FFXII is a call into a Windows DLL the game does not
> ship — 566 square roots' worth of call sites, and only **four** ~~SSE `sqrt` instructions~~ scalar `sqrtss` instructions, beside 14 packed `sqrtps` and 10 `rsqrtps` in the audio cluster, *(corrected 2026-10-02, OPUS: an instruction grep of every body; the corrected count in §3)* in the
> whole 7.5 MB of code. Battle numbers, meanwhile, use no such maths at all: exactly **one**
> function in the entire Combat-Formula category calls the maths library, and what it computes is
> a power of two.

## 1. What the player sees

Two very different things in FFXII are described as "the numbers", and they are computed by
completely different machinery.

**Geometry is continuous.** When Vaan turns to face a Marlboro, he does not snap — he swings round,
and the swing is not at a constant speed. If he is already nearly facing the right way he turns
very gently; the further off he is, the faster he comes about, up to a point. When you are checking
whether you are in range of a Hunt, the game is measuring a distance across the *ground* and
ignoring height, which is why standing on a ledge directly above something can still count as being
next to it. The camera, the flow of the Mist gauge across the screen, a bat circling — all of that
is smooth, curved, floating-point maths.

**Battle numbers are not.** Damage, accuracy, evasion and the rest are integer and rational
arithmetic — multiply, divide, clamp — of the `Strength × (Level + Speed) / 218 + 1` kind. There is
no sine, no square root, and no logarithm anywhere in a damage roll. This is worth knowing because
it settles a recurring argument: FFXII's damage formulas cannot have hidden curve-fitting or
floating-point drift in them, because the code that computes them never calls anything that could
introduce it. Whatever a damage formula does, it does with whole numbers.

There is one exception in the whole of combat, and it is almost a joke: a single function that
raises 2 to the power of a small byte using the full floating-point `pow` routine, when a shift
would have done. It is documented in §4 because a modder tracing floating-point calls in battle
code will find it and reasonably wonder what curve it belongs to. It is not a curve. It is
`1 << n` taking the scenic route.

The other thing worth knowing before touching any of this: **the maths itself is not in the game.**
`sin`, `cos` and `sqrt` live in a Windows system DLL, so a player on a freshly-updated Windows and
a player on an older one are running different implementations of them from the same game files.
The game supplies the *inputs* and the *shaping* around them; Windows supplies the curves.

## 2. Native mechanism

### The maths library is the operating system's

`FFXII_TZA.exe` declares **45 imports from `api-ms-win-crt-math-l1-1-0.dll`** — the API-set stub
that forwards to `ucrtbase.dll`. It ships none of them: there is no `ucrtbase.dll` and no
`api-ms-win-crt-*.dll` in the game's `x64` folder, so they resolve from the system directory.

**The consequence for this database is a boundary, and it is worth stating plainly: the polynomial
coefficients and range-reduction constants of `sinf`, `cosf`, `atan2f` and the rest are not facts
about FFXII.** They live in a Microsoft-supplied binary that is versioned by Windows Update, differs
between machines, and is not the program this database documents. Writing them down here would be a
factual error about the game dressed up as precision — the evidence standard's rule that a
companion binary is *tier 1 about itself and tier 9 about the game* applies with extra force when
the companion is not even shipped. What **is** a fact about FFXII, and what this document records,
is: which of those routines the game calls, how often, from where, in what units, and what
arithmetic the game wraps around them.

**One qualification, added after an independent falsification pass.** This is true of the *scalar*
CRT, not of everything: `0080A270` (`Runtime.Math.VectorPowf4`, 1,191 B — interior read 2026-09-17, SWE2-FRONTIER: single `0080B8A0` helper call at [`0080A710`](../../_index/ADDRESS-INDEX.md), rest is inline SIMD; `0080B8A0` itself is a 2,967-B no-call scalar-SSE body — `mulss` ×53/`addss` ×46 from [`0080B8F7`](../../_index/ADDRESS-INDEX.md), a polynomial/evaluation core) is a **hand-vectorised
4-wide `powf` inside the image**, with its own reciprocal seed and its own exponent extraction. So
the accurate statement is that FFXII imports its scalar transcendentals and ships a small amount of
vectorised maths of its own — that routine, and the Audio SIMD cluster below.

### What the game actually calls

Every one of these is reached by `call` into a jump thunk, never inlined:

| routine | call sites | distinct calling functions |
|---|---:|---:|
| `sqrtf` | 566 | 269 |
| `sinf` | 174 | 119 |
| `powf` | 133 | 53 |
| `cosf` | 109 | 74 |
| `logf` | 86 | 32 |
| `expf` | 65 | 33 |
| `tanf` | 60 | 40 |
| `atan2f` | 51 | 38 |
| `sqrt` (double) | 36 | 19 |
| `pow` (double) | 34 | 13 |
| `ceilf` | 32 | 19 |
| `floor` (double) | 27 | 14 |
| `atanf` | 22 | 18 |
| `floorf` | 14 | 13 |
| `_hypotf` | 12 | 6 |
| `acosf` | 9 | 9 |
| `asinf`, `tan`, `modff` | 2 each | — |
| `sinh`, `cosh`, `tanh`, `fmod`, `fmodf`, `log10`, `log10f`, `acos`, `asin`, `__setusermatherr` | 1 each | — |

The single-call-site tail is the shape of a library that was linked wholesale: ten routines the
game touches exactly once, including all three hyperbolics.

### Only four scalar square roots are instructions

Search the whole `.text` section for SSE square-root and reciprocal instructions and confirm every
candidate by disassembling from its function's entry point:

| instruction | confirmed occurrences | audit 2026-09-07 |
|---|---:|---|
| `sqrtps` (4-wide) | ~~13~~ **14** | corrected — **all fourteen are in `Audio`-owned functions**, not geometry |
| `rsqrtps` (4-wide reciprocal) | 10 | confirmed |
| `sqrtss` (scalar) | **4** | **confirmed**, sites `0016A270` `007D0FB7` `007D119B` `007E9184` |
| `rcpps` | ~~0~~ **2** | **refuted** — both real, in `Runtime.Math.VectorPowf4` (`0080A270`). See section 10 |
| `rcpss`, `sqrtsd`, `rsqrtss` | **0** | confirmed |

Four scalar square-root instructions, against 566 call sites for the library `sqrtf`. That ratio is
a compiler-settings fingerprint: MSVC emits an inline `sqrtss` for `sqrtf` only under `/fp:fast`
(or with an explicit intrinsic), because under the default `/fp:precise` the library call is
required to set `errno` for a negative argument. **FFXII TZA was built `/fp:precise`, with no
fast-math relaxation**, and the price is that every distance check in the game is a cross-DLL call
rather than one instruction.

*(Instrument note — and this table was wrong twice before it was right. A raw byte-pattern search
for the `0F 51/52/53` opcodes over 7.5 MB reported 18 `sqrtps`, 14 `rsqrtps` and 4 `rcpps`.
Disassembling only the functions that search nominated cut those to 13, 10 and zero — a ~28 %
false-positive rate, since a 3–4 byte pattern occurs by chance inside immediates and displacements.
**That second answer was also wrong**, in the opposite direction: the scan's REX handling excluded
any `0F 5x` preceded by a byte in `0x40`–`0x4F`, an exclusion added to stop the prefixed and
unprefixed branches double-counting, which silently discarded every **REX-prefixed NP-form**
instruction — `44 0F 51`, `44 0F 53`, `45 0F 53`. A decoder can only report on what it is given, and
it was being given a filtered list. The counts above come from **disassembling all 38,161 functions
in the image**, with the scanner removed from the loop entirely; it costs seconds and needs no
correction. See §8.)*

### The vector maths that *is* in the game — and it belongs to the sound system

The SIMD routines are the part of the maths Square Enix shipped rather than imported, and they carry
real constants this document can state exactly. They live in a cluster around `007EF000`–`007F8000`.

**Every one of them is `Audio`-owned, and that is the single most useful fact in this section.**
Sorting all 28 SIMD square-root sites in the image by `PrimaryOwner`: **`sqrtps` 14/14 Audio,
`rsqrtps` 10/10 Audio, `sqrtss` 3 of 4 Audio** (the fourth is the boot-time constant at `0016A270`).
The remaining two sites are the `rcpps` pair in `Runtime.Math.VectorPowf4` (§10).

So a modder who reasons "4-wide square roots and cross products must be the geometry code" will
search this cluster and find **the sound engine** — this is 3-D positional audio doing vector
arithmetic on emitter and listener positions, not character or camera geometry.

**The geometry path has no SIMD in it at all.** Movement, Presentation and UI reach their square
roots through 566 scalar `sqrtf` calls into the CRT, exactly as `Vector3_ComputeXZDistance` does.
That is consistent with the `/fp:precise` finding above and it is why the two facts belong together:
this build did not vectorise its geometry, and the only hand-vectorised maths in the image was
written for audio.

The core idiom is a cross product followed by a normalise, and the normalise is a hardware
reciprocal square root refined by one Newton–Raphson step:

```
007EF1EB  movaps xmm5, [00D22600]   ; 0.5, 0.5, 0.5, 0.5
007EF201  movaps xmm6, [00D560A0]   ; 3.0, 3.0, 3.0, 3.0
007EF219  movaps xmm9, [00D11570]   ; 1.0, 1.0, 1.0, 0.0   <- the W mask
...
007EF257  rsqrtps xmm2, xmm0        ; y0 ~= 1/sqrt(x), about 12 bits
007EF25A  mulps   xmm0, xmm2
007EF25D  mulps   xmm0, xmm2        ; x * y0 * y0
007EF260  subps   xmm1, xmm0        ; 3 - x*y0^2
007EF266  mulps   xmm0, xmm2        ; (0.5 * y0)
007EF269  mulps   xmm1, xmm0        ; y0 * (3 - x*y0^2) / 2
```

The formula is in §4. The `[1, 1, 1, 0]` vector at `00D11570` is what turns a 4-wide dot product
into a 3-wide one — it zeroes the W lane before the two `haddps` that sum the components, which is
how a 3-component length is computed with 4-wide instructions. That constant is the reason a
`Vector4` and a `Vector3` can share a code path here.

`007EF3B0` is the same routine again, and "same" here is measured rather than assumed: its two
`rsqrtps` sit at `007EF42F` and `007EF499`, mirroring `007EF1E0`'s at `007EF257` and `007EF2C1`, and
the two bodies agree on every count that distinguishes this idiom — 2 `rsqrtps`, 10 `haddps`, three
`shufps 0xC9` and three `shufps 0xD2` for the cross product, two `shufps 0xFF` broadcasts, and
references to all three refinement constants. The pair are two instantiations of one template.

**The sound system carries two vector-length implementations and they are not interchangeable.**
Every function that uses `rsqrtps` also references all three Newton–Raphson constants
(`0.5`, `3.0`, and the W mask); every function that uses `sqrtps` references **only the W mask**
and none of the refinement constants. So the `sqrtps` group takes an exact hardware square root and
the `rsqrtps` group takes a refined approximation, and a modder reimplementing either must match the
one they are replacing — the two disagree in the low bits by construction, not by accident. Both
groups are `Audio`-owned, so the choice between them is an audio-engine decision about cost versus
precision, not a split between two subsystems.

The cluster is also layered rather than flat: `007EF630` and `007EF790` contain `rsqrtps` of their
own *and* call `007EF1E0` and `007EF3B0`, so they are compositions over the two primitives rather
than further copies of them.

The cross product immediately before it is the standard SSE shuffle pair — `shufps` with `0xC9`
selects lanes (1,2,0) = *yzx* and `0xD2` selects (2,0,1) = *zxy*, so
`a.yzx * b.zxy − a.zxy * b.yzx` is the cross product with no branches.

### Angles are radians in `float`, and there is no other representation

Many PS2-era engines store angles as fixed-point "binary angle" units — 4096 or 65536 to a full
turn. FFXII TZA does not. A census of the constants that such a representation requires finds
**none of them present anywhere in the image**:

| constant | value | addresses in the image | `.text` references |
|---|---:|---:|---:|
| `2π` | 6.28318548 | 4 | 246 |
| `π` | 3.14159274 | 33 | 192 |
| `π/2` | 1.57079633 | 15 | 58 |
| `1/π` | 0.31830989 | 9 | 14 |
| `1/(2π)` | 0.15915494 | 1 | 4 |
| 1° in radians | 0.0174532924 | 1 | 6 |
| **`65536/2π`** | 10430.3783 | **0** | **0** |
| **`2π/65536`** | 9.58738e-05 | **0** | **0** |
| **`4096/2π`** | 651.898987 | **0** | **0** |
| **`2π/4096`** | 0.00153398 | **0** | **0** |
| **`180/π`** (rad→deg) | 57.2957795 | **0** | **0** |

So: **angles are `float` radians throughout, there is no fixed-point angle unit, and there is no
radians-to-degrees conversion in the shipped binary at all.** A modder writing a facing value writes
radians, and a value read out of memory is radians. The census has a positive control built in — the
same scan finds `π`, `2π` and `π/2` in quantity, so it is demonstrably capable of finding a
four-byte float constant that is present.

The single "1° in radians" constant is *not* a conversion factor. All six of its uses are as a
**value** — a floor, in radians, on how slowly something may turn. §4 shows the site.

### The angle primitive, and where its contract fails

`Angle_NormalizeRadiansPi` (`0033CB70`, 128 B) is the wrap-to-±π primitive the movement code calls
before every angular comparison. Its complete body has two paths, and **they do not agree on what
the function returns**:

```c
float Angle_NormalizeRadiansPi(float a)
{
    if (a > 12.566371f || a < -12.566371f)          // |a| > 4pi
        return a - (float)(int)(a / 6.28318548f) * 6.28318548f;   // ONE truncating step

    while (a >  3.14159274f) a -= 6.28318548f;      // subtract 2pi until in range
    while (a < -3.14159274f) a += 6.28318548f;      // add 2pi until in range
    return a;
}
```

The near path is exact: it iterates until the result is in [−π, π]. The far path — taken when the
input exceeds **4π** in magnitude — performs a single truncating `fmod` by 2π and returns
immediately, with no correction afterwards. A truncating `fmod` by 2π lands in **(−2π, 2π)**, not
in [−π, π] — **for inputs whose quotient fits a signed 32-bit integer** (qualified 2026-09-11). The
`cvttss2si` at `0033CBD5` returns the integer indefinite `0x80000000` = `−2³¹` once the quotient
leaves `[−2³¹, 2³¹)` — a **signed** boundary: `a = −T` (with `T` = binary32 `2³¹ × 2π` =
`50490FDB` = 13,493,038,080) converts validly and returns `0`, `a = +T` does not. The product is then
`f32(−2³¹) × 2π = −T`, and the subtraction **returns `f32(a + T)`**: `T` comes back as `2T`,
`−T − 1024` as `−1024`, `±1e11` as `±1e11 + T`. ~~The input comes back unchanged~~ — **corrected
2026-09-12** (ASTRA's [EXP-074](../../_experiments/EXP-074-angle-conversion-boundary.md), ten
paired original-code executions at the two limits and beyond; all ten reproduced here by emulating
the sequence in binary32) — only once `|a| ≥ 2⁵⁸ ≈ 2.9 × 10¹⁷`, where `T` is below half an ulp and
the addition rounds away; that is what the earlier `±1e20` controls had shown, and it was
overgeneralised. `±inf` do return unchanged. A NaN never reaches
the far path: both `COMISS` tests at `0033CB73` and `0033CB84` are unordered, so it takes the near
path, fails both loop tests and is returned as it came. ASTRA's
[EXP-073](../../_experiments/EXP-073-facing-reapply-comparison.md) (isolated original-code
execution of the 128 bytes) produced exactly these outputs for `±1e20`, `+inf` and a quiet NaN.

**So the function does not honour its name for |input| > 4π.** Feed it 13.0 radians and it returns
about 0.43 (correct); feed it 13.0 + 2π ≈ 19.28 and the fast path returns about 0.43 as well — but
feed it 4.5π ≈ 14.14 and it returns ≈ 1.57 correctly, while 6.5π ≈ 20.42 returns ≈ 1.57 too. The
failure is not that it never wraps; it is that the fast path's output range is twice as wide as the
slow path's, so a value that lands between π and 2π comes back un-normalised. The engine never hits
this in normal play because facings arrive already near range — but a mod or a network path that
writes a large accumulated angle will, and the symptom is a character that picks the long way round
a turn.

This is stated as a defect in the *shipped* function, not as a reading to be confirmed: both paths
are in the same 128-byte body and both were read.

### Which subsystems use maths at all

Grouping every caller of every `api-ms-win-crt-math` import by `PrimaryOwner`:

| owner | function-to-routine calls | dominant routines |
|---|---:|---|
| Presentation | 88 | `sqrtf` 45, `sinf` 17, `cosf` 8, `atan2f` 5 |
| Audio | 66 | `floor` 8, `powf` 7, `expf` 7, `atan2f` 4 |
| Movement | 50 | `sqrtf` 28, `cosf` 5, `sinf` 5, `_hypotf` 4, `atan2f` 3, `acosf` 2 |
| UI | 15 | `sinf` 9, `cosf` 4 |
| Script VM bridge | 3 | `cosf`, `sinf`, `atan2f` |
| ActorEntity | 2 | `cosf`, `sinf` |
| Input | 2 | `cosf`, `sqrtf` |
| Party | 2 | `sqrtf`, `atan2f` |
| CombatAction | 2 | `atan2f`, `_hypotf` |
| Spawn | 1 | `sqrtf` |
| **CombatFormula** | **1** | **`pow`** |

And the owners that reach it **zero** times: **CombatAI, Status/Periodic/Terminal,
Items/Equipment/Shops/License, Rewards/Progression/Economy, RNG/Random-Selection, Save/Load/Settings,
Story/Event/Quest/Hunt, World/Area/Field, Resource, Platform/Online/Achievements, Core scheduling.**

That is the evidence behind §1's claim. Gambits, status ticks, the licence board, loot and reward
tables, the RNG and the save system contain **no transcendental maths whatsoever**. The two
CombatAction entries are `BattleAction_ApplyKnockbackImpulse` (`00323350`), which needs a direction
and a magnitude for a knockback — geometry, not damage — and the single CombatFormula entry is the
`pow(2, n)` in §4.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0033CB70` | `Angle_NormalizeRadiansPi` | 128 B | wrap to ±π; **fast path fails above 4π**, §2 |
| `0033CEF0` | movement turn-rate solver | 772 B | the `cosf` easing in §4; ~~the only non-third-party user of the 1°-in-radians constant~~ a user of the 1°-in-radians constant, not the only one *(corrected 2026-10-02, OPUS: `008C5F68` is read by `0028BB50`, `0033CEF0`, `00538B80` and `0085EA40`)* |
| `004686D0` | `Vector3_ComputeXZDistance` | 35 B | ground-plane distance; **tail-jumps to `sqrtf`** |
| `003A1960` | `Vector3_ComputeSquaredXZDistance` | 31 B | the same body without the square root |
| `0031E620` | `Vector3_ComputeSquaredXZDistance` | 5 B | forwarder to `003A1960` |
| `0038EAF0` | the Combat-Formula `pow` | 54 B | `(int)pow(2.0, byte)` — §4 |
| `0016A270` | runtime-computed tunable | 29 B | `0.9 / sqrt(16)`; one of the four `sqrtss` |
| `007EF1E0` | cross-product + approximate normalise | 455 B | 2 `rsqrtps`, 10 `haddps`, all three NR constants, calls nothing — §4 |
| `007EF3B0` | cross-product + approximate normalise | 463 B | structurally identical to `007EF1E0`: same counts, same shuffles, same constants |
| `007EF630` | caller of the two above | 344 B | 2 `rsqrtps`, 4 `haddps`, only broadcast shuffles; **calls** `007EF1E0` and `007EF3B0` |
| `007EF790` | caller of the two above | 349 B | same shape as `007EF630` |
| `007F1EC0` | approximate normalise | 188 B | 1 `rsqrtps`, NR constants present |
| `007F74E0` | approximate normalise | 135 B | 1 `rsqrtps`, NR constants present |
| `007F25E0` | exact-length vector routine (**Audio**) | 2115 B | **7** `sqrtps`, 20 `haddps`; W-mask only, **no** NR constants |
| `007F0320` | exact-length vector routine (**Audio**) | 600 B | 2 `sqrtps`, W-mask only |
| `007F0820` | exact-length vector routine (**Audio**) | 1966 B | 1 `sqrtps` — **missed by the original scan**, see §8 |
| `007F1670` | exact-length vector routine (**Audio**) | 239 B | 2 `sqrtps`, W-mask only |
| `007F1340` | exact-length vector routine (**Audio**) | 742 B | 1 `sqrtps`, W-mask only |
| `007F1A50` | exact-length vector routine (**Audio**) | 497 B | 1 `sqrtps`, W-mask only |
| `0080A270` | `Runtime.Math.VectorPowf4` | 1191 B | hand-vectorised 4-wide `powf`; the image's **only** 2 `rcpps` |
| `00323350` | `BattleAction_ApplyKnockbackImpulse` | 489 B | the only Combat-owned `atan2f` and `_hypotf` |
| `00358CB0` | `PartyControl_ApplyAnalogLocomotionToActor` | 545 B | `atan2f` on stick input |
| `003594E0` | `PartyControl_BuildAnalogMovementVectorFromInputHistory` | 461 B | `sqrtf` on stick input |
| `00861F14` | `sqrtf` import thunk | 6 B | `FF 25` to the IAT |
| `00861F80` | `pow` import thunk | 6 B | `FF 25` to the IAT |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `00D22600` | SIMD half | `f32[4]` | `0.5, 0.5, 0.5, 0.5` |
| `00D560A0` | SIMD three | `f32[4]` | `3.0, 3.0, 3.0, 3.0` |
| `00D11570` | SIMD W-mask | `f32[4]` | `1.0, 1.0, 1.0, 0.0` |
| `01CEBC50` | π | `f32` | `3.14159274` |
| `01CEBC78` | 2π | `f32` | `6.28318548` |
| `00915620` | −π | `f32` | `-3.14159274` |
| `00915624` | −2π | `f32` | `-6.28318548` |
| `00D10B0C` | 4π | `f32` | `12.566371` — the fast-path threshold |
| `00D10B20` | −4π | `f32` | `-12.566371` |
| `008C5F68` | one degree | `f32` | `0.0174532924` — a floor value, not a conversion |
| `0091572C` | π/3 | `f32` | `1.04719758` — the turn-easing knee (60°) |
| `008F311C` | three | `f32` | `3.0` — the easing frequency multiplier |
| `01CEBBA8` | one | `f32` | `1.0` |
| `01CEBB70` | half | `f32` | `0.5` |
| `01CEBD80` | fabs mask | `u64` | `0x7FFFFFFFFFFFFFFF` |
| `01CEBC10` | two | `f64` | `2.0` — the base in the Combat-Formula `pow` |
| `02AEE004` | `pow` result | `s32` global | destination of `(int)pow(2.0, byte)` |
| `02EBF190` | ~~settings object pointer~~ pointer to an object whose byte `+0x5B0E` three code sites write *(corrected 2026-10-02, OPUS: `00385BA0+0x31` copies a record's byte `+0x138` into it, `002FA210+0x17` and `00233C10+0x81` zero it; UQ-320's answer)* | `void*` global | the `pow` input is its byte at `+0x5B0E` |
| `02EADEF0` | runtime-computed tunable | `f32` global | receives `0.225` from `0016A270` |

## 4. Data structures and formulas

### Vector normalise — hardware estimate plus one Newton–Raphson step

`rsqrtps` gives roughly 12 correct bits. One Newton–Raphson iteration for `y = 1/√x` doubles that
to about 22, which is close enough to `float` precision for geometry and far cheaper than a
`sqrtps` and a divide.

```c
// y0 = rsqrtps(x)                             ~12 bits
// y1 = y0 * (3 - x * y0 * y0) * 0.5           ~22 bits
//
// as emitted at 007EF257, with the exact constants:
y0 = rsqrtps(x);
y1 = (3.0f - (x * y0) * y0) * (0.5f * y0);
```

The squared length that feeds it is a masked 3-component dot product:

```c
// v is a 4-lane register holding (x, y, z, w)
t   = v * v;                       // mulps
t   = t * (1.0f, 1.0f, 1.0f, 0.0f) // mulps by the mask at 00D11570 -- kills the W lane
t   = haddps(t, t);                // pairwise add
t   = haddps(t, t);                // now every lane holds x^2 + y^2 + z^2
```

and the cross product ahead of it:

```c
// shufps imm 0xC9 selects lanes (1,2,0) = yzx ; 0xD2 selects (2,0,1) = zxy
cross(a, b) = a.yzx * b.zxy - a.zxy * b.yzx;
```

### Ground-plane distance

The two distance primitives are byte-identical except for their last instruction, which is the
cleanest possible demonstration that the square root is a library call and not an instruction:

```c
// Vector3_ComputeSquaredXZDistance (003A1960) -- 31 bytes, ends in `ret`
dx = a[0] - b[0];                  // X is at +0x00
dz = a[2] - b[2];                  // Z is at +0x08 -- Y at +0x04 is IGNORED
return dz*dz + dx*dx;

// Vector3_ComputeXZDistance (004686D0) -- 35 bytes, ends in `jmp sqrtf`
return sqrtf(dz*dz + dx*dx);
```

Height is not part of either. Every range test built on these is a **cylinder**, not a sphere.
Prefer the squared form when comparing against a threshold — the engine already does in the places
that matter, and it is the difference between a DLL call and none.

### The turn-rate easing — `(1 − cos 3a) / 2`

From the complete body of `0033CEF0`. `turnRate` arrives from the unit's configuration
(`+0xE4` when a speed gate is met, `+0xE8` otherwise); `desired` is the requested facing:

```c
delta = Angle_NormalizeRadiansPi(current - desired);
a     = fabsf(delta);                              // via the 0x7FFF... mask at 01CEBD80

if (a < 1.04719758f) {                             // pi/3 == 60 degrees
    float c = cosf(a * 3.0f);                      // 3a maps [0, pi/3) onto [0, pi)
    turnRate = (1.0f - c) * 0.5f * (turnRate - 0.0174532924f) + 0.0174532924f;
}
// a >= pi/3: turnRate is used unmodified
```

`(1 − cos 3a) / 2` is a cosine ease that rises smoothly from **0** at `a = 0` to **1** at
`a = π/3`. So the effective turn rate is interpolated between a hard floor of exactly **one degree**
(`0.0174532924` radians) and the unit's full configured rate, reaching full rate at a 60° error and
staying there beyond it.

That is the maths behind what §1 describes: a character almost facing the right way creeps round at
1°, and one facing 60° or more off turns at full speed. The floor is why a character never quite
stops turning, and the `π/3` knee is why the acceleration is over by the time you notice it.

### The one Combat-Formula transcendental

Complete body of `0038EAF0`, 54 bytes:

```c
// 02EBF190 holds a pointer to the settings/registry object
u8  n      = *(u8*)(*(void**)0x02EBF190 + 0x5B0E);
*(s32*)0x02AEE004 = (s32)pow(2.0, (double)n);        // ... i.e. 1 << n
```

`pow` here is the **double** routine, not `powf`, and both arguments are converted to double for
it. The result is truncated back to a 32-bit int by `cvttsd2si`. For `n ≤ 30` this is exactly
`1 << n`; at `n = 31` the double `2147483648.0` does not fit a signed 32-bit int and `cvttsd2si`
yields the integer indefinite value `0x80000000`. Whether `n` can reach 31 depends on the ~~settings~~
byte at `+0x5B0E`, which ~~is not established here~~ never exceeds 17 *(answered: see UQ-320, answered 2026-09-14 - it is not a setting; 2026-10-02, OPUS)*.

### The angle wrap, with its exact constants

```c
float Angle_NormalizeRadiansPi(float a)      // 0033CB70
{
    if (a >  12.566371f) goto fast;          // +4pi, constant at 00D10B0C
    if (a < -12.566371f) goto fast;          // -4pi, constant at 00D10B20

    while (a >  3.14159274f) a -= 6.28318548f;   //  pi at 01CEBC50, 2pi at 00915624 (negated add)
    while (a < -3.14159274f) a += 6.28318548f;   // -pi at 00915620, 2pi at 01CEBC78
    return a;                                    // guaranteed in [-pi, pi]

fast:
    return a - (float)(int)(a / 6.28318548f) * 6.28318548f;   // in (-2pi, 2pi) while -2^31 <= a/2pi < 2^31;
                                                                // else the int is 0x80000000 and this is a + T
                                                                // (T = 2^31 * 2pi), == a only for |a| >= 2^58 -- see §2
}
```

### The runtime-computed tunable

`0016A270`, 29 bytes, one of the four scalar `sqrtss` in the image, and it computes a constant:

```c
*(float*)0x02EADEF0 = 0.9f / sqrtf(16.0f);    // == 0.225f
```

Both operands are literals. The compiler did not fold it because `/fp:precise` forbids folding a
square root that could set `errno`. It is a static initialiser, so it runs once at boot, and the
value at `02EADEF0` is `0.225` from then on.

## 5. Call chain

```
Movement / Presentation / UI / Audio / Party / CombatAction
  -> 004686D0 Vector3_ComputeXZDistance
  -> 0033CEF0 turn-rate solver -> Angle_NormalizeRadiansPi (0033CB70)
  -> 00323350 BattleAction_ApplyKnockbackImpulse
  -> the 007EFxxx / 007Fxxxx SIMD cluster        (no library call -- rsqrtps in registers)
       |
       +-> 00861F14 sqrtf  (FF 25)  -+
       +-> 00861F80 pow    (FF 25)   +-> IAT -> api-ms-win-crt-math-l1-1-0 -> ucrtbase.dll
       +-> sinf / cosf / atan2f ...  -+
```

**Upstream (who causes this):** Presentation is the heaviest user, then Audio and Movement. Every
frame in which anything moves, turns or is drawn crosses this boundary hundreds of times.

**Downstream (what this causes):** `ucrtbase.dll`. Nothing in `FFXII_TZA.exe` is downstream — the
maths routines are leaves.

**Do not confuse with:** the SIMD cluster at `007EF000`–`007F8000` is *not* downstream of the CRT.
It computes its square roots in registers with `rsqrtps`/`sqrtps` and calls nothing. The two
mechanisms coexist: scalar maths goes to the DLL, 4-wide vector maths does not. A modder hooking
`sqrtf` to instrument distance work will see the scalar half of the engine and none of the vector
half.

Also do not confuse `Vector3_ComputeSquaredXZDistance` at `0031E620` (5 bytes) with the real body at
`003A1960` (31 bytes) — the first is a forwarder, and both carry the same name.

## 6. Modding notes

- **Angles are `float` radians. Always.** There is no fixed-point angle and no degree form in the
  binary. If a tool shows you degrees, the tool converted them.
- **Wrap your own angles, or keep them small.** `Angle_NormalizeRadiansPi` is only correct for
  inputs within ±4π, lands in (−2π, 2π) up to `|a| ≈ 1.35 × 10¹⁰`, returns **`a + 1.35 × 10¹⁰`** for
  anything larger up to `≈ 2.9 × 10¹⁷` (a large wrong angle — corrected 2026-09-12, it is not a
  pass-through), and returns only inputs above that, infinities and NaN unchanged. If you write an
  accumulated facing — and a network path that adds deltas will
  accumulate — normalise it yourself before handing it to the engine.
- **Best intervention point for turn feel:** the unit configuration fields at `+0xE4` / `+0xE8`
  (full turn rate) rather than the easing itself. The floor of 1°, the `π/3` knee and the `3.0`
  frequency are shared constants in `.rdata` — `008C5F68`, `0091572C` and `008F311C` — and each is
  referenced from more than one place, so editing them is not a local change.
- **Range checks are cylinders, not spheres.** Height is dropped by both distance primitives. If
  you are reimplementing a range test, drop Y or you will not match the engine.
- **Hooking `sqrtf` is viable and cheap.** It is a single IAT slot and 566 call sites route through
  it, so it is a genuine instrumentation point for distance and geometry work — but see §5: it
  catches none of the SIMD path.
- **Do not expect fast-math behaviour.** The build is `/fp:precise`. Replacement code compiled
  `/fp:fast` will not reproduce the engine's results bit-for-bit, and near a range boundary that can
  flip a comparison.
- **Multiplayer / XIIOnline:** this is the one place where "the same game files" does not mean "the
  same arithmetic". `sinf` and `sqrtf` come from the player's `ucrtbase.dll`. Two clients on
  different Windows builds can produce different low bits from the same inputs, so **no lockstep
  scheme may assume float determinism across machines for anything that passes through the CRT
  maths library.** Send results, or send inputs and accept divergence — do not send neither and
  assume they agree. The SIMD path is safe by comparison: `rsqrtps` is an IEEE-specified
  approximation with a defined result on any x86-64 CPU, and the Newton–Raphson step is plain
  multiplies and subtracts, so that half *is* reproducible.
- **Mod compatibility:** `02EADEF0` is written once at boot by a static initialiser. A mod that
  writes it before that initialiser runs will have its value overwritten; after, it will stick.

## 7. What is not known

- [x] ~~**UQ-320.** What the settings byte at `+0x5B0E` of the object at `02EBF190` controls, what range it takes,
      and therefore whether the `pow(2, n)` at `0038EAF0` can overflow its `cvttsd2si`.~~ **Answered 2026-09-14 (FABLE):** it is not a setting. It is **echo B, the action streak count** of [the count-clock recipes](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.2, and it **never exceeds 17**, so the power of two cannot overflow.
      - **Writers of the byte** (displacement scan):
        - `BattleFormula_ApplyResultMetadata` copies result `+0x138` into it when that field is not −1 (`00385BAF`–`00385BD1`);
        - two resets store 0 (`00233C91`, where `ebx` was zeroed at `00233C63`, and `002FA227`).
      - **Writers of result `+0x138`** (the [result record](../../07-Combat-Action/Result-Record/the-result-record-field-map.md) census): the initialiser stores −1; slot 49 stores `count + 1` only while `count < 17` (`00389D2A`, `00389D58`) and 0 otherwise (`00389D72`).
      - **Consequence.** The byte ranges over 0–17, so `pow(2.0, n)` is at most `2^17 = 131,072` against the `2^31` limit of `cvttsd2si`. When the count is 17, slot 49 has already reset the streak and marked the action a miss, so the largest loss actually dealt is `2^16 = 65,536`, as §2.2 of that page says.
- [x] ~~**UQ-321.** What `02AEE004`, the destination of that power of two, is read by.~~ **Answered 2026-09-14 (FABLE):** `02AEE004` is **result slot A, the HP-loss magnitude** of the battle formula scratch block. That identification is AJ-9 on [attack and defence preparation](../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md): the applied change is `gain (02AEE008) − loss (02AEE004)`.
      - **The power of two.** The 54-byte formula body that stores it (`0038EB1B`) is one of nine formula-family bodies that store it in `0038E480`–`0038EE24` alone. So `pow(2, n)` is one formula's HP loss, not a dedicated control value.
      - **Readers** (RIP census, twelve reads in nine functions):
        - `BattleFormula_ComputeKnockbackImpulseScale` (`00385F13`);
        - `BattleFormula_ResolveTargetResult` (`0038646D`);
        - `BattleFormula_ApplyTargetHpPostMultipliers` (`0038F895`);
        - `BattleFormula_ApplyTargetStatusActionPostModifiers` (`00390F36`);
        - five unnamed formula-family bodies, at `0038CBDC`, `0038D164`, `0038D4F2` / `0038D513`, `0038DECB`, and `0038F8E4` / `0038F91E` / `0038F933`.
      So an overflowing `cvttsd2si` would have reached the HP result, the knockback scale and the post-multipliers. UQ-320 above shows that `n` never exceeds 17, so it cannot overflow.
- [x] **UQ-322.** What the `007EF000`–`007F8000` SIMD cluster's functions each compute. Every function cited
      here was disassembled in full and classified by instruction mix, constant references and
      call targets — that is what separates the exact-length group from the approximate one and
      identifies `007EF630`/`007EF790` as compositions. What was **not** established is what any of
      them means to the game: ~~their callers were not traced and~~ no geometric identity is claimed *(answered: see the UQ-322 answer just below, 2026-09-27 - every body is placed; 2026-10-02, OPUS)*
      beyond "cross product", "length" and "normalise". They are a Phyre-adjacent population and the
      survey belongs to another category.
      *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: every residue body is placed - 13 in the sound driver and 1 in
      the integer Vorbis decoder, none in a third library - see the register row and
      [the families control](../../_index/candidates/uq322-residue-families/uq322_families.py). The last two are the sound
      driver's own MS-ADPCM helpers (samples per block, and the adaptation tables), called only from its voice setup.*
- [x] **UQ-323.** Whether the `Angle_NormalizeRadiansPi` fast path is ever reached in retail play. The defect is *(closed — the register row is WITHDRAWN.)*
      proven from the body; its reachability is not, and settling it needs runtime evidence.
      **NARROWED 2026-09-16 (FABLE): *settling it needs runtime evidence* is too broad. The question decomposes into 53 call sites, and most of them are bounded by static structure.** **The population, which the row never states:** `0033CB70` has **53 call sites across 25 functions, every one of them Movement.** Classified by what last writes `xmm0` before the call, body-bounded within each caller: **21 `movaps`** (a register copy, one hop short), **19 `subss`**, **5 `addss`**, **5 `movss`**, **2 `divss`**, and one where the producer is past a call. **Three sites provably cannot reach the fast path**, because the argument is a literal: `0033A446` loads **π/4**, `0033A4C9` loads **−π/4**, `0033DC00` loads **−0.0091**. All are far below the 4π threshold. **The accumulator behind three more sites is self-normalising, and that is the useful finding.** `022C7CE0` is **zeroed at `0033A386`** (`xor eax, eax` then `mov qword ptr [022C7CE0], rax`) and has **11 accesses, all Movement**. Every terminal write of it is **the output of `Angle_NormalizeRadiansPi` itself** - `00337C10` runs load (`00337CBA`) → `addss` (`00337CC2`) → **normalise** (`00337CCA`) → store (`00337CD6`), and `00337D90` runs the same shape at `003380F1`–`00338106`. **So the accumulator is in [−π, π] whenever it is read**, and for those sites the fast path requires a **single-step angular delta above 3π - about 540° in one step.** That is a concrete, falsifiable condition where the row had none. ~~**`divss` is the only shape that can grow without bound**, and there is **one** of it against a register: `00339880` in `BattleAction_FindApproachGeometryAroundTarget`, `divss xmm0, xmm9`.~~ *(corrected 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's approach-divisor-domain: `xmm9` there is the constant 180.0, loaded once at `00339723` from `008F3138` (`43340000`) and otherwise only restored in the epilogue, so `00339880` is `float(int32(ebx * 90)) * pi / 180` - a degrees-to-radians step, not a variable divisor. Its magnitude is bounded by the signed 32-bit product, which does not exclude values above 4 pi, so this site still does not rule out the fast path)* The other divide, `0033DC99`, is **by 180.0** and shrinks. **WHAT IS NOT DONE, and it is most of the sites.** The **21 `movaps` and 19 `subss` sites are unresolved** - each needs one more hop back to the operands, and a `subss` of two angles is bounded by 2π **only if both operands are themselves normalised**, which I did not establish for any of them. **So this does not say the fast path is unreachable.** It says the residue that genuinely needs a run is small and nameable, and that the cheap static work - one hop per site - has not been spent yet. **The row stays OPEN.**
      **SECOND HOP, same day (FABLE) - the 40 unresolved sites are now traced, and the question is not really about call sites at all.** Each argument was traced back recursively inside its own caller's body, depth-limited, no cross-function reasoning. All 53 classify: **40 MIXED** (arithmetic over fields and literals), **6 OPEN**, **3 LIT**, **2 FIELD**, **2 NORM**. **The operands are dominated by a handful of object fields.** Counted across every traced operand: **`+0xE0` sixteen times**, `+0xBC` six, `+0xEC` four, `+0x40` three, `+0xB4` two, `+0x118` two, `+0xF8` one, `+0x150` one. **So UQ-323 is not a 53-site question - it is a three-field question**, and bounding `+0xE0`, `+0xBC` and `+0xEC` settles most of it. That is the shape the row should have had. **Two sites are provably near-path**, because the argument is the return of `Angle_NormalizeRadiansPi` itself: `0033D9FA` and `0033E0A7`. The second is worth naming - `FUN_0033DFD0` normalises at `0033E045`, parks the result in `xmm6`, and then **normalises the same value a second time** at `0033E0A7` via `movaps xmm0, xmm6`. **A redundant call whose input is already in [−π, π]**, so it can only ever take the near path. **And the dominant field has almost no writers.** Over every `Movement`-owned body there are **four** 4-byte stores to `[reg + 0xE0]`: `00266335` stores the literal `0.1f`, `003DB130` stores a non-register source, and the remaining two - `00336DC5` in `BattleLocomotion_SolveAndPublishNextStep` and `0033A35E` in `FUN_0033A240` - both load from a **stack slot written as an out-parameter by `FUN_0033DFD0`**, which is itself one of the normalisers. **WHAT THIS DELIBERATELY DOES NOT CLAIM.** I have **not** verified that `FUN_0033DFD0` writes its normalised result into that out-parameter - the write is inside its callee `00202F00`, which I did not read. **And nothing here shows the base register at the sixteen `+0xE0` READ sites points at the same kind of object as at the four STORE sites.** A displacement census carries no type information, and **naming that field from the coincidence of one offset is exactly the adjacency reasoning this database forbids.** Establishing it is reader/writer/ lifetime work and belongs to **SWE2-STRUCT**, not to a semantic ruling from me. **The row stays OPEN**, and the honest next step is a typed census of `+0xE0`, `+0xBC` and `+0xEC` on the locomotion object - not a run.
- [x] **UQ-324 ANSWERED 2026-09-15 (OPUS) — none of them. All four `sqrtss` sites are
      FFXII's own code.**
      - **Tested against the catalogue rather than by inspection.**
        [third-party-middleware-inventory.md](../../23-Third-Party-Libraries/third-party-middleware-inventory.md)
        carries a per-library member list with explicit address ranges, and **none of `0016A270`,
        `007D0F60`, `007D1140` or `007E9030` appears in any of them** — `bullet`,
        `cri-hca-decoder`, `libogg-bitwise`, `libogg-framing`, `libvorbis`, `libvpx-vp8-decoder`,
        `libvpx-vp8-dsp-kernels`, `libwebm-mkvparser`, `lua`, `msvc-runtime-tail`,
        `tremor-vorbisfile`, `zlib`.
      - **Positive control, so the absence means something.** The member files are bare uppercase
        hex, one address per line; taking a real member address from `libvorbis.tsv`
        (**`008800C0`**) and searching the same way finds it. A lookup that cannot find a present
        address would have proved nothing.
      - **The ranges are nowhere near, which is the sanity check on the lookup.** libvorbis runs
        `008800C0`–`008958B0` and the CRI HCA decoder `00121000`–`0012573F`; the three audio
        sites sit between them and inside neither.
      - **And the positive attribution already exists on this page:** all three are `Audio`-owned by
        `GFZ.V120.PrimaryOwner.*`, and §6 records that the audio stack's own namespace is
        `SQEX::Sd::*` — Square's sound engine, which *drives* CRI's HCA decoder rather than being
        it. So the arithmetic the page reads as cross-product-and-normalise is FFXII's own
        positional-audio maths, not a vendor's.
      - ⚠ **The bound, stated rather than left implicit:** this is *not in any **catalogued**
        third-party range*. It is exactly as strong as the inventory is complete. If a library is
        ever added to that inventory whose range covers one of these addresses, this answer changes
        — and the check is one lookup with a stated control. **UQ-324.**

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 45 maths imports, none shipped with the game | PE import directory of the authorized EXE; directory listing of the shipping `x64` folder | 1 |
| Per-routine call-site and caller counts | transitive walk of `E9` / `FF 25` / `48 FF 25` forwarder chains, then every `E8` and `FF 15` site in `.text` | 1 |
| 14 `sqrtps`, 10 `rsqrtps`, 4 `sqrtss`, 2 `rcpps` | linear disassembly of **all 38,161 functions** in the image, no byte-scan pre-filter. Supersedes a scan-nominated count that was wrong in both directions; see §8 | 1 |
| Every SIMD square-root site is `Audio`-owned | the same exhaustive pass, grouped by `GFZ.V120.PrimaryOwner.*`: `sqrtps` 14/14, `rsqrtps` 10/10, `sqrtss` 3/4 (the fourth is `0016A270`, the boot-time constant) | 1 + 11 |
| The build is `/fp:precise` | inference from the 4-instruction / 566-call-site ratio plus `0016A270` failing to constant-fold `0.9/sqrt(16)` | 1 + 6 |
| Newton–Raphson normalise and its constants | complete body of `007EF1E0`; constants read from `00D22600`, `00D560A0`, `00D11570` | 1 |
| The `rsqrtps` and `sqrtps` groups are distinct implementations | ~~all eleven cluster functions~~ eleven of the twelve cluster functions disassembled in full, `007F1670` missed *(corrected 2026-10-02, OPUS: a `sqrtps` / `rsqrtps` grep of every body finds twelve functions; §3 adds `007F1670`)*; per-function census of `rsqrtps`/`sqrtps`/`haddps`/`shufps` counts, RIP-referenced constants and direct call targets. The refinement constants appear in every `rsqrtps` function and in none of the `sqrtps` ones — a clean split with no overlap | 1 |
| Angles are radians, no fixed-point unit | float-constant census over `.rdata`/`.data` with a positive control (π, 2π, π/2 all found in quantity; all four fixed-point constants and rad→deg absent) | 1 |
| `Angle_NormalizeRadiansPi` fast path returns outside ±π; its (−2π, 2π) bound needs `−2³¹ ≤ a / 2π < 2³¹`; past that it returns `f32(a + T)`, unchanged only for `|a| ≥ 2⁵⁸`, `±inf` and NaN | complete 128-byte body, both paths read and disassembled; the `cvttss2si` / `COMISS` semantics; ASTRA's EXP-073 (`±1e20`, inf, NaN) and EXP-074 (ten inputs at the signed limits), isolated original-code execution; the ten reproduced by emulated binary32 arithmetic (FABLE 2026-09-12). ~~"larger inputs return unchanged"~~ corrected 2026-09-12 | 1 |
| Turn-rate easing formula and constants | complete body of `0033CEF0`; every `DAT_` operand dereferenced and printed as f32 | 1 |
| Distance primitives ignore Y and one tail-calls `sqrtf` | complete bodies of `003A1960` (31 B) and `004686D0` (35 B) — byte-identical but for the final instruction | 1 |
| The single Combat-Formula maths call is `pow(2, n)` | complete 54-byte body of `0038EAF0`; the `2.0` double read from `01CEBC10` | 1 |
| Owner distribution, and the eleven owners with zero maths calls | caller sets from a freshly regenerated call graph, grouped by `GFZ.V120.PrimaryOwner.*` tag | 11 |

**Superseded readings:**

- *During this session*, an import census counting only `call qword ptr [rip+slot]` reported **zero
  call sites for `sinf`, `cosf`, `sqrtf`, `powf` and every other transcendental**, and this document
  was very nearly written around the conclusion that FFXII carries its own maths library with its
  own coefficients. That was wrong, and it was wrong in the most inviting possible direction — it
  would have produced a longer, more impressive document full of constants that are not in the game.
  What exposed it was `memset` and `memcpy` scoring zero on the same instrument. MSVC reaches these
  imports through `E9` / `FF 25` forwarder chains up to three hops deep. The corrected figures are
  in §2. Recorded in `COVERAGE.md`.
- *Also during this session*, the single "1° in radians" constant at `008C5F68` was first read as a
  degrees-to-radians **conversion factor**, which would have implied a degree representation
  somewhere in the engine. Reading its use site (`0033CEF0`) shows it is used as a **value** — an
  additive floor in a lerp — and the absent-constant census then confirmed there is no degree
  representation at all. A constant's identity is not its numeric value; it is what the code does
  with it.
- *Corrected 2026-09-07 after `xiionline-61`'s independent falsification pass (§10).* The SIMD
  instruction table said `sqrtps` 13 and `rcpps` 0; the true counts are **14** and **2**. The cause
  was mine and it is a specific, repeatable defect: the byte scan excluded any `0F 5x` whose
  preceding byte lay in `0x40`–`0x4F`, an exclusion added earlier **to fix a REX-related undercount**
  in the prefixed forms, which then discarded the REX-prefixed *unprefixed* forms `44 0F 51`,
  `44 0F 53` and `45 0F 53`. The verification step was not at fault — it disassembled correctly, but
  only the functions the broken scanner nominated. **The fix moved the count toward the number I
  expected, and I stopped there instead of re-measuring.** The table now comes from disassembling
  all 38,161 functions with no scanner in the path.
- *Corrected in the same pass, and it is the larger of the two.* This document framed the
  `007EF000`–`007F8000` SIMD cluster as the game's vector **geometry**. It is not: **all 14
  `sqrtps` sites, all 10 `rsqrtps` sites and 3 of the 4 `sqrtss` sites in the entire image are in
  `Audio`-owned functions.** The cross-product-and-normalise reading of the bodies was correct — 3-D
  positional audio needs exactly that arithmetic — but the attribution was wrong, and a reader
  hunting for geometry code would have been sent to the sound engine. The corrected claim is
  stronger than the original: the geometry path contains **no SIMD at all** and reaches its square
  roots through the 566 scalar `sqrtf` calls.
- **No claim in this document rests on `.pdata`, `.xdata`, unwind records, EH maps or
  `_IMAGE_RUNTIME_FUNCTION_ENTRY`.** Every body cited was read.

## 9. Related

- [`../Memory-And-Allocation/where-the-games-memory-comes-from.md`](../Memory-And-Allocation/where-the-games-memory-comes-from.md)
  — the same import-forwarder mechanism, the same "the C runtime is the operating system's"
  boundary, and the census correction both documents rest on.
- [`../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`](../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
  — forwarders counted for internal calls; this document is the import-side case.
- [`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md)
  — where the turn-rate easing and `Angle_NormalizeRadiansPi` belong as *movement* behaviour;
  this document owns them only as maths call sites.
- [`../../08-Combat-Formula/README.md`](../../08-Combat-Formula/README.md)
  — the integer damage formulas, and the negative result that they use no maths library.

## 10. Falsification pass 2026-09-07 — `xiionline-61`, independent

**First independent pass on this document.** The auditor had not read it before this pass and did not
read `xiionline-8d`'s inbox notes on it. Program state GN160
`fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`; every figure below re-derived by
decoding function bodies from the authorized EXE, not by scanning bytes and not from the ledger.

### Method

Every function in the ledger's function list was decoded linearly from its entry point across its
exact body extent, and SSE square-root and reciprocal mnemonics were counted from the **decoder's**
output. Byte-count sanity was checked per function (`decoded bytes == body bytes`) so a desynced
stream could not contribute phantom instructions.

### SURVIVED — the headline claim, exactly

| claim | this pass |
|---|---|
| **`sqrtss` (scalar) = 4** | **4 — confirmed**, and the four sites match: `0016A270`, `007D0FB7`, `007D119B`, `007E9184` |
| `rsqrtps` = 10 | **10 — confirmed** |
| `rcpss`, `sqrtsd`, `rsqrtss` = 0 | **0 — confirmed** (also `sqrtpd` = 0) |

**Four scalar square roots against 566 `sqrtf` call sites stands**, and with it the `/fp:precise`
conclusion, which is the document's most consequential claim.

### SURVIVED — every cited constant, read at its cited address

| address | claimed | actual `float` |
|---|---|---|
| `00D10B0C` | `+4pi 12.566371` | `12.566370964050293` ✅ |
| `00D10B20` | `-4pi -12.566371` | `-12.566370964050293` ✅ |
| `01CEBC50` | `pi 3.14159274` | `3.1415927410125732` ✅ |
| `00915620` | `-pi` | `-3.1415927410125732` ✅ |
| `00915624` | `2pi`, used as a negated add | `-6.2831854820251465` ✅ |
| `01CEBC78` | `2pi 6.28318548` | `6.2831854820251465` ✅ |

`02EADEF0` could not be read as a float **because it lies past `.data`'s raw backing** — which is
itself confirmation of the document's claim that the value is *computed at boot by a static
initialiser* rather than stored. And `0.9 / sqrtf(16.0f) = 0.225` exactly in `float`.

### REFUTED — `rcpps` is **2**, not 0

The document states `rcpps` = **0** and adds an instrument note saying *"all four `rcpps` hits were
noise."* **Two of them are real.**

```asm
FUN_0080A270  (1,191 bytes, decoded 1191/1191 — no desync)
  0080A32F  movlhps   xmm9, xmm9
  0080A333  psrlq     xmm11, 0x14
  0080A339  rcpps     xmm8, xmm5        <-- real
  0080A33D  rcpps     xmm10, xmm9       <-- real
  0080A341  cvtps2pd  xmm4, xmm8
  0080A345  cvtps2pd  xmm5, xmm10
```

The context is coherent and diagnostic: `psrlq xmm, 0x14` is exponent extraction by a 20-bit shift,
and `rcpps` → `cvtps2pd` is a reciprocal seed being widened to double. **The function is tagged
`GFZ.V121.CodeDomain.Runtime.Math.VectorPowf4` — a 4-wide vectorised `powf`**, which is precisely
where a reciprocal seed belongs.

> **This does not overturn the `/fp:precise` finding.** Two reciprocals inside a hand-vectorised
> `powf` are not compiler fast-math relaxation; they are a library routine choosing its own
> approximation. **But the document's table says zero, and the correct number is two.**

### CORRECTED — `sqrtps` is **14**, not 13, and they are all Audio

Fourteen confirmed occurrences, every one inside an **`Audio`-owned** function: `007F03A2`,
`007F04CD`, `007F0A17`, `007F15D9`, `007F16FF`, `007F1709`, `007F1C11`, `007F2685`, `007F26B7`,
`007F2752`, `007F2935`, `007F2AE1`, `007F2CB2`, `007F2DCF` — in `FUN_007F0320` (600 B),
`FUN_007F25E0` (2,115 B) and neighbours, all `GFZ.V120.PrimaryOwner.Audio`.

**That is a fact the document does not state and which changes how its §2 reads.** The 4-wide square
roots in this image are **not** geometry. The geometry path is the `rsqrtps` + Newton–Raphson
normalise the document documents at `007EF257`; the `sqrtps` are **audio DSP**.

### The instrument lesson: the correction over-corrected

The document's own instrument note is admirably explicit — a byte-pattern scan reported
18/14/4 for `sqrtps`/`rsqrtps`/`rcpps`, and a disassembly pass cut those to 13/10/**0**, a claimed
28 % false-positive rate.

**The disassembly pass removed two true positives along with the false ones.** Fixing a
false-positive problem introduced false negatives, and the second error is harder to see because the
number moved in the direction the author already expected.

> **A correction needs its own control.** The scan was checked against a decoder; the decoder was
> checked against nothing. **When a fix moves a count toward the answer you predicted, that is the
> moment to re-measure, not the moment to stop.**

### Verdict

`status` unchanged at **DOCUMENTED** *(answered: see the front matter - since promoted to `status: AUDITED`; 2026-10-02, OPUS)* — the central claims survive and the corrections are to two
counts in one table, not to the document's argument. `audit.passes: 0 -> 1`. Two figures corrected in
§2 above the fold, and the Audio attribution of the `sqrtps` cluster added, because it was absent and
is load-bearing for a reader who assumes 4-wide square roots mean geometry.

## 11. Correction 2026-09-12 — the far path adds `T`, it does not pass the input through

**CORRECTED 2026-09-12 (ASTRA-CONTRA-FABLE-ANGLE-OVERFLOW, EXP-074).** §2's 2026-09-11 qualification
said that once `|a| / 2π ≥ 2³¹` *"the input comes back unchanged"*. That was read off two facts that
are both true — the conversion returns the integer indefinite, and at `±1e20` the result equals the
input — joined by an inference that is false: the product `−2³¹ × 2π` is not "absorbed by the
subtraction's rounding" in general, it is **subtracted**, and the far path returns `f32(a + T)`.

```
s      = f32(a + bias)                        bias = (a >= 0) ? +π : −π      (the facing writer 002E5E10 only; this helper has no bias)
q      = f32(s / 2π)
k      = trunc(q)   if −2^31 <= q < 2^31,  else −2^31    (cvttss2si: the integer indefinite 80000000)
p      = f32(f32(k) × 2π)                     = −T when the conversion is invalid, T = 50490FDB = 13,493,038,080
stored = f32(f32(s − p) − bias)               invalid conversion ⇒ f32(f32(s + T) − bias)
```

ASTRA executed the shipped bytes at ten inputs the earlier controls had not touched — the two
adjacent floats on each side of `±T`, `±1.4e10`, `±1e11` — and none came back unchanged; `+T` gives
`2T`, `−T` (a *valid* conversion) gives `0`, `−T − 1024` gives `−1024`. I reproduced all ten by
emulating the instruction sequence in binary32 with the indefinite rule, and the same emulation
gives the threshold the experiment did not claim: **`f32(a + T) == a` exactly when `|a| ≥ 2⁵⁸`**
(`T` = 0.785 ulp at `2⁵⁷`, 0.393 ulp at `2⁵⁸`). So the corrected statement is three regimes, not
two: in range for `|a| / 2π < 2³¹`; `a + T` up to `2⁵⁸ ≈ 2.9 × 10¹⁷`; the input itself above that
and for `±inf` / NaN.

**Why the earlier reading was reachable:** the only executed inputs (`±1e20`) lay in the third
regime, and the static reading treated "the indefinite makes the product `−T`" and "`−T` is absorbed"
as one step. A negative claim about a boundary needs a control **at** the boundary. Propagated to
[the facing page](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) (K-6 box,
the wrap paragraph, the consequences table and its correction), the `K-6` ledger row, the modding
note and evidence row above, and the listing comment in §4. The reconstruction
`Reconstruction/Game/Math/angle_wrap.c` truncates through `(int)` and so matches on MSVC x64 by
construction; its comment calls the result "garbage rather than large" — the exact value is
`f32(a + T)` and is routed to OPUS with the ten EXP-074 inputs as named cases for
`diff_angle_wrap.py`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Gameplay — CLIENT.** `Angle_NormalizeRadiansPi` (`0033CB70`) is also used by
`BattleAction_FindApproachGeometryAroundTarget`. The §2 fast-path limit above 4π therefore applies to approach
geometry as well as to movement.

## Interior citation — frontier hub `00202F00` (2026-09-17, SWE2-EC7)

`00202F00` — 100 B, 11 A-measured callers at census. Interior verified: copies the caller's
64-byte block `rdx` -> `rcx` verbatim (four `movups` at
[`00202F06`](../../_index/ADDRESS-INDEX.md)–`00202F30`), then calls the `00861F08`/`00861F0E`
import pair on `xmm2` (the trig pair — sin/cos thunks), and tail-jumps `00217880` with the
results in `xmm1`/`xmm2`. A stage-and-rotate helper: preserve the matrix, evaluate the angle,
hand off.

## Interior citation — frontier hub `00334120` (2026-09-18, SWE2-EC7)

`00334120` — 116 B, 8 callers; `Angle_ApproachWrappedRadians` confirmed. `0033CB70`
normalises `target - current` into the wrapped delta, `andps` with the ~~`0x7FFFFFFF`~~ `0x7FFFFFFFFFFFFFFF` double mask *(corrected 2026-10-02, OPUS: `00334120+0x21` widens the delta with `cvtss2sd`, `00334120+0x25` masks it and `00334120+0x2C` narrows it with `cvtpd2ps`; `01CEBD80` holds two copies of `0x7FFFFFFFFFFFFFFF`)* at
`01CEBD80` takes its absolute value, and `|delta| <= step` returns `target` unchanged
(`00334187`). Otherwise it adds or subtracts `step` on the delta's sign and re-wraps through
`0033CB70` before returning ([`0033415D`](../../_index/ADDRESS-INDEX.md)). The steering
cap that keeps a turning actor from snapping across the ±π seam in one frame.

## Interior citation — frontier hub `003A1960` (2026-09-18, SWE2-EC7)

`003A1960` — 31 B, 8 callers; `Vector3_ComputeSquaredXZDistance` confirmed: `(a.x−b.x)² +
(a.z−b.z)²` ([`003A1972`](../../_index/ADDRESS-INDEX.md)), the squared XZ-plane distance the
proximity and facing tests compare against a radius² — no `sqrt` anywhere, by design.


### Interior citation — frontier hub `00202E10` (2026-09-18, SWE2-EC7)

`00202E10` — 115 B, 26 callers: the vec3 cross product leaf. `out[0] =
a1*b2 - a2*b1`, `out[1] = a2*b0 - a0*b2`, `out[2] = a0*b1 - a1*b0` — the
`subss` at [`00202E36`](../../_index/ADDRESS-INDEX.md) closes the first lane —
and `out[3] = 0`. Six `mulss`, three `subss`, no calls.
## SWE2-EC7-46 update (2026-09-19) - `00217880`

`00217880` (234 B) is a call-free per-component vector lerp - `t`*v + `(1-t)`*w over the `+0x00`/`+0x08`/`+0x10`/`+0x18`/`+0x20`/`+0x28`/`+0x30` float fields, `mulss`/`addss`/`subss` throughout. Interior anchor `002178AD` (the first `mulss`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page inventories where the image does maths, so it cites maths routines inside other layers. Their neighbours
are those layers' own call graphs.

**Audio — CLIENT, 82 edges, all inside the audio engine's vector cluster.**
- The exact-length and approximate-normalise routines `007F0320`, `007F0820`, `007F1340`, `007F1A50`, `007F25E0`,
  `007F1EC0`, `007F74E0`, `007EF630` / `007EF790` and their helpers `007EF1E0` / `007EF3B0` are called by the audio
  engine's `007A4xxx`-`007BBxxx` bodies, and call one another.
- The unattributed maths sites `007D0F60`, `007D1140` and `007E9030` sit between libvorbis (`008800C0`-`008958B0`) and
  the CRI HCA decoder (`00121000`-`0012573F`). Both of those libraries' entries also appear with their own callers.

Which precision the audio engine chooses is its cost decision (§ the cluster). The sound pages own what it computes.

**ActorEntity, Party, Input, CombatAI, CombatAction and WorldAreaField — CLIENT, 26 edges, through the movement and
combat geometry this page names.**
- The facing and turn solvers `00337C10` / `00337D90` read battle-unit slots and actor world positions.
- The turn-rate solver `0033CEF0` resolves a unit.
- `0033A240` is called by the combat and lifecycle frames.
- The analog-stick path `PartyControl_ApplyAnalogLocomotionToActor` → `PartyControl_BuildAnalogMovementVectorFromInputHistory`
  reads the input history (`InputControl_GetHistoryAnalogByteByIndex`).
- `Vector3_ComputeXZDistance` serves the target-distance tests (`BattleTarget_ComputeSurfaceDistance*`) and `00320E10`.
- `BattleAction_ApplyKnockbackImpulse` is called by `Battle_ProcessActionTarget` and reads the field flag.

The maths is shared; each caller's purpose is its own layer's.

**Presentation, UI, Script_VM_Native_Bridge and Rewards_Progression_Economy — SERVICE, 18 edges, through the vector
leaves.**
- The cross product `00202E10` (26 callers) and `00202F00` are called by render bodies (`0040B430`, `0051C3C0`,
  `00523380`, `00542740`, `003F3710`, `00466550`), widget bodies (`003F26F0`, `003F2A70`, `005512B0`) and `00356160`.
- `Vector3_ComputeXZDistance` is also called by three script handlers.
- The loot searches (`Loot_FindNearestActivePickupPosition`, `Loot_FindOverlappingPickupIndex`) measure XZ distances.
- The facing writer `002E5E10` calls `003EC260`, and `00337D90` calls `BattleUnit_ComputePresentationSuppressionMask`.


**CombatFormula, SaveLoad, Save_Load_Settings, Items_Equipment_Shops_License and
CoreRuntimeScheduling — CLIENT, 7 edges: the cited writers' own paths.** (2026-10-02,
SWE2-CONTRACT, graph-churn residue)
- `00385BA0` (`BattleFormula_ApplyResultMetadata`, cited at `+0x31` as a `02EBF190`-byte write
  site) is called by `BattleFormula_ApplyTargetResult` (`003112F0`) and calls
  `BattleStats_FindOwningBattleUnit` (`0031B860`) and `BattleFormula_DispatchPostResultEvents`
  (`00469EC0`) — the combat layer's own result pipeline.
- `00233C10` (cited at `+0x81` as the third `+0x5B0E` zero site) is the save path's reset
  helper: called by the save/load lifecycle `00280140`, it reads the active save buffer through
  `SaveImage_GetActiveRuntimeBuffer` (`002EF640`), rebase-clears derived inventory state through
  the Items layer's `0030B6A0`, and hops the 7-byte thunk `00229ED0`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-maths-the-game-runs-on-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0085EA40` | 883 B | with `p` = `r8`, `x` = `r9` and F(q) = `0085E740(rcx, edx, q, x)`: `i` = F(p) (sign-extended); with `t` = qword [x+0x10] returns `i` when dword [t+4i] is 3; calls `00861D30(&v, p)` for a stack vec3 `v` and takes `w` = (v.y p.z - v.z p.y, v.z p.x - v.x p.z, v.x p.y - v.y p.x); with Q(a) = p + 0.025 (`00D22C30`) times (v sinf(r) + w cosf(r)), r = a times pi/180 (`008C5F68`), sinf and cosf by `00861F0E` and `00861F08`, passed as a stack vec4 with 0 last, and `e` = -1: for `a` = 0, 45, ..., 360 (steps `00902EF0`, limit `00902438`): `j` = F(Q(a)); goes to D when `e` and `j` are both `i`; unless `e` is -1 or equals `j`, for `b` = `a` - 40 (`00D11670`) up to `a` in steps of 5 (`009146E4`): `k` = F(Q(b)), going to D when `e` and `k` are both `i`, then `e` = `k`; after each `a` sets `e` = `j`; when every angle passes, stores 0 at dword [t+4i] and repeats everything from the first F(p); D: stores 3 at dword [qword [x+0x10] + 4i] and returns `i` | `0085EACC`, `0085EAEF`, `0085EB70`, `0085EC0D`, `0085ED45` |
| `008800C0` | 348 B | with `v` = `rcx`, `c` = `rdx` and `p` = `r8`: returns 0xFFFFFF7B when `p` is null; otherwise builds the stack reader `b` (qword +0 = 0, qwords +8 and +0x10 = qword [p], dword +0x18 = dword [p+8], dword +0x1C = 0), takes `t` = `0017CB40(&b, 8)` and calls `00880C10(&b, &s, 6)` on a zeroed 6-byte stack buffer `s`; returns 0xFFFFFF7C unless the first dword and the next word of `s` equal dword `01CEBB50` ("vorbis") and word `01CEBB54`; then for `t` 1: returns 0xFFFFFF7B when dword [p+0xC] is 0 or dword [v+8] is non-zero, 0xFFFFFF86 when qword [v+0x20] is null, else `00880720(v, &b, qword [v+0x20])` + 7; for `t` 3: returns 0xFFFFFF7B when dword [v+8] is 0 or qword [c+0x18] is non-null, else `00880540(c, &b)`; for `t` 5: returns 0xFFFFFF7B when dword [v+8] is 0 or qword [c+0x18] is 0, 0xFFFFFF7F when qword [v+0x20] is null, 0xFFFFFF7B when dword [qword [v+0x20] + 0x18] is greater than 0 (signed), else `00880230(v, &b)`; any other `t` returns 0xFFFFFF7B | `0088010B`, `0088012B`, `00880134`, `008801A0`, `008801F2` |
