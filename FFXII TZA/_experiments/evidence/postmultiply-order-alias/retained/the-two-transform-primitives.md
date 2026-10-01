---
system: The workbench's two primitives — transforming a point, and composing two matrices
category: 00-Engine-Core-Runtime
owner_layer: unowned in the ledger — filed here for what these compute, not for who calls them
evidence_tier: 1
level: L2
status: AUDITED
readiness: BEHAVIORALLY UNDERSTOOD   # §5a adds live observation of the STATE, not of the functions running
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 160 addresses cited - 31 data, 108 entry, 21 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-transform-primitives-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The workbench's two primitives

> *2026-09-14 (FABLE):* the "workbench" is the register bank of the PS2 assembly emulation. See
> [the EE and VU0 register bank](the-ee-and-vu0-register-bank.md). The matrix these primitives use is VU0 vector rows 1–4.
> `00398F90` also uses ACC and the vf00 constant, so it is a translated VU0 routine. The laws below were measured by
> execution and stand.

## 1. What the player sees

Everything that is anywhere. A character's sword is at the end of their arm; the camera swings and
the whole world swings with it; a spell effect appears at the caster's hand and not at the origin of
the map. All of that is one operation repeated: **take a position, and express it relative to
something else.**

This page is the two pieces of arithmetic that does. One moves a single point. The other combines two
transforms into one, so a hand attached to an arm attached to a body needs only one multiplication at
the end instead of three.

## 2. Why these two

A whole-binary ranking of functions **no document cited when this page was written** (2026-09-08 — see §9; three documents cite them now), ordered by distinct **non-EH** callers,
puts them near the top — and unlike most of that ranking they are not eight-byte accessors:

| entry | body | distinct non-EH callers | callees |
|---|---:|---:|---|
| `00397910` | 567 B | **82** | only `__security_check_cookie` |
| `00398F90` | 377 B | **74** | **none — a true leaf** |

**156 distinct callers between them** (~~156 call sites~~ — 156 is the *caller* sum; the **sites**
are **231**, 129 and 102; corrected 2026-09-13), **and nothing written about either at the time.** Both are leaves, which is what
makes this page unusual: **every claim below was produced by executing the shipped bytes**, not by
reading them. `check_already_answered.py` reported no existing coverage for either function.

*(The subsystem around them is documented — [the shared transform workbench](the-shared-transform-workbench.md)
and [its save-and-restore](the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md). These
two functions are not.)*

## 3. `00398F90` — one point through the workbench matrix

```c
void TransformPointByWorkbenchMatrix(const float in[4] /*rcx*/, float out[4] /*rdx*/);
```

**The law, and it is exact:**

```text
out[c] = in.x * M[0][c]  +  in.y * M[1][c]  +  in.z * M[2][c]  +  1.0 * M[3][c]
```

where `M[r]` is the 16-byte block at `022D91B0 + r*0x10`. That is a **row-vector × matrix** product
with the **translation in row 3**.

> **How this was established, and how it could have failed.** The matrix and the point were set to
> distinguishable values, the function was run, and the law above was then used to *predict* the
> output for **200 random matrix/point pairs**. Any single mismatch would have killed it.
> **200 of 200 matched.**

**Two things a reimplementation would get wrong:**

1. **The point's own 4th component is ignored.** `in[3]` is loaded and never used: `w` is forced to
   **1.0** by a live load from `01EF93FC` — the `w` lane of the software `vf00` image at `01EF93F0`, in `.data`, which all three of its writers (`0036D9A8`, `0036D9E8`, `0036DD87`) set to the architectural `[0,0,0,1]`. Not an immediate; see [the contract's §15b](../CONTRACT-transform-primitives.md). Feeding `w = 7` and `w = -123` gives byte-identical
   output. **So this transforms a POSITION, never a direction** — a direction would need `w = 0`, and
   this function cannot express one.
2. **There is no perspective divide.** It emits all four components and divides by nothing.

**It also deposits, and that is not a side effect to drop:**

| address | what lands there |
|---|---|
| `022D9300` | the **input** point, copied verbatim |
| `022D91A0`–`022D91AC` | the running accumulator, mid-computation |
| `022D9310`–`022D931C` | the result |
| `022D8F90` | the result again |
| `[rdx]` | the result, for the caller |

**The result is written to three places and the input to one.** A reconstruction that only filled
`out` would compile, pass any test of its return value, and silently starve every consumer that reads
the workbench instead of the caller's buffer.

## 4. `00397910` — composing two transforms

```c
void ComposeTransforms(const Mat4 *a /*rcx*/, const Mat4 *b /*rdx*/, Mat4 *out /*r8*/);
```

**The argument order is the reverse of the obvious reading:**

```text
out = b × a          (NOT a × b)
```

with `out[i][j] = Σₖ b[i][k] · a[k][j]`. Verified the same way — **150 of 150** random pairs
predicted exactly, and the designed case distinguishes the two orders outright:

| | first four floats |
|---|---|
| observed | 6610, 7020, 7430, 7840 |
| `b × a` | 6610, 7020, 7430, 7840 |
| `a × b` | 1210, 1220, 1230, 1240 |

**Writing it the natural way round gives a completely different matrix**, and every transform built
from it would be wrong in a way that still looks like a transform.

**Aliasing is safe, and deliberately so.** The function copies **both** inputs to its stack frame
before it multiplies (`[rsp+0x40]` and `[rsp+0x80]`), so `out == a` and `out == b` both produce the
same answer as three distinct buffers. Tested, not assumed. A reconstruction that multiplied in place
without staging would corrupt its own input halfway through and pass every test that used separate
buffers.

**It writes exactly 64 bytes.** The 16 bytes following the destination were sentinel-filled and were
untouched in every run.

## 5. What this settles about the workbench matrix

`BQ-16` records that the getter `003970A0` loads four `movups` from `022D91B0`, `+0x10`, `+0x20`,
`+0x30` as one 64-byte block. **This page reaches the same four blocks from the other end** — as the
multipliers of `x`, `y`, `z` and `1` respectively — which fixes the convention:

> **The matrix at `022D91B0` is row-major with the translation in its last row, and the engine's own
> consumer applies it to points with `w = 1`.**

`BI-9` asks what that matrix *is* — world, view, projection, or a current transform. **This does not
answer that**, and the distinction matters: a projection matrix multiplies exactly the same way. What
it does establish is that **the workbench's own point primitive treats it as a positional transform
and never divides by `w`**, so if it is a projection the divide happens somewhere else, in code this
page has not read.

## 5a. Observed in the running game — 2026-09-08

§3–§5 are emulation: the shipped bytes executed in isolation. **This section is the retail game,
launched and read.** The reference install is the clean Steam copy whose build hash matches the
authority, `runtime_probe.py`'s base control passed (the module loads at its PE `ImageBase`, so a
database VA is a runtime address unmodified), and the process was verified to be **ticking** —
4,251 bytes moved across seven 1 MB slabs in three seconds — before anything below was believed.

**At the title screen, the workbench's deposit slots do not move at all.** Forty samples over four
seconds, against a control that the surrounding region *did* move 91 bytes in the same window:

| address | what it holds (§3) | result |
|---|---|---|
| `022D8F90` | the last result | **0 of 16 bytes moved** |
| `022D91A0` | the accumulator | **0 of 16 bytes moved** |
| `022D9300` | the last input point | **0 of 16 bytes moved** |
| `022D91B0` | the matrix | 2 of 64 bytes, transiently |

**This table samples three of the four deposits §3 names.** `022D9310`, where the result also lands,
was not read at all — so even the observed half of this section is a subset of the writes the
primitive makes. *(Noted 2026-09-21, FABLE, while consuming the return that withdrew the line below.)*

And the matrix's first row read `[0, 0, 0, 0]`, stable across thirty further samples. A matrix whose
first row is all zeros is **degenerate** — it collapses the `x` axis and no transform in a working
renderer looks like that.

> ~~**So `00398F90` is not running at the title screen**~~ — **WITHDRAWN 2026-09-21 (ASTRA,
> `OPUS-REQ-ASTRA-TWO-PARITY-CLAIMS-ARE-LIVE-ONLY`; consumed by FABLE).** *Unchanged scratch does not
> mean the leaf did not run.* ASTRA re-ran the verified shipping body twice on identical input and
> recorded **instruction execution and deposit writes separately from endpoint changes**: it executes,
> it writes, and the endpoints do not move — with a third call on changed input as the change-detection
> control. **Repeated execution on identical inputs is indistinguishable from no execution by sampling
> alone**, which is exactly what this line did. *What I inferred from stable bytes was never available
> from them.*
>
> **What survives is the half that was doing the work anyway:** the 64-byte block is not being maintained
> as a live transform there — that rests on the **degenerate first row**, not on the absence of writes,
> and a degenerate matrix rules out a continuously maintained one whether or not anything is running.
>
> That is evidence about `BI-9`, and it is bounded evidence. **What it rules out** is the reading in
> which this block is a **continuously maintained** world, view or projection matrix owned by the
> engine — such a matrix would hold a sane value while the renderer runs, and this one holds a
> degenerate one. **What it cannot rule out**, now that the execution half is withdrawn, is that the
> primitive runs here and deposits the same bytes each time; and a title screen need not render a 3D
> scene at all, so nothing here reaches "idle always" either.

**Two blocks immediately past the matrix are live, and that speaks to `BQ-16`:**

| address | size | behaviour |
|---|---:|---|
| `022D91F0` | 16 B | **a new value in all 30 samples**, floats oscillating in about `[-0.08, +0.20]` |
| `022D9210` | 32 B | **a new value in all 30 samples**, and internally structured — see below |

`022D9210`'s eight floats are not eight independent quantities. The second group of four repeats the
first with **its first two entries exchanged**:

```text
[-0.05229, -0.04414, -0.05736, -0.07307,  -0.04414, -0.05229, -0.05736, -0.07307]
             ^^^^^^^^ swapped ^^^^^^^^                        ^^^^ identical ^^^^
```

and values appearing in `022D91F0` reappear in `022D9210` on later samples, so the two are stages of
one pipeline carrying the same oscillating quantity.

**`BQ-16` asks how the region divides past `022D91B0`.** Measured live, the first two divisions after
the 64-byte matrix are a **16-byte** unit at `022D91F0` and a **32-byte** unit at `022D9210`, both
updating continuously while the matrix does not. **What they are is not established** — the numbers
are small and oscillating, which is the shape of an animated parameter, and nothing here identifies
it.

> **Answered 2026-09-14 (FABLE, `BQ-16`): the region does not divide into matrices.** `022D91A0` is the VU0
> `ACC` register, and `022D91B0`–`022D939F` are its 31 vector registers, one per 16 bytes
> ([the EE and VU0 register bank](the-ee-and-vu0-register-bank.md)). The 64-byte "matrix" is rows 1–4 as
> `003970A0` / `00398F90` load them. The two live units are **vector register 5** (`022D91F0` = `022D91A0` +
> 16 × 5) and **vector registers 7–8** (`022D9210`–`022D922F`). Their contents belong to whichever translated
> routine used them last, so the division is per routine. *Which* routine keeps the oscillating quantity there
> was not identified; the sentence above stays true of that quantity and no longer of the layout.

## 5b. Reconstructed and differential-tested — 2026-09-08

Both primitives are now implemented in
[`Reconstruction/Game/Math/transform.c`](../../../../Reconstruction/Game/Math/transform.c) and
compared against the shipped bytes by
[`diff_transform.py`](../../../../Reconstruction/Tests/Differential/diff_transform.py).

| | |
|---|---|
| point cases | **123** — 3 designed, 120 randomised |
| compared per point case | **five buffers**: the caller's `out` **and all four deposits** |
| compose cases | **123**, across **3 aliasing modes** (`out` distinct, `out == a`, `out == b`) |
| mismatches | **0** |
| mutation score | **19 of 20 (95 %)** |

**The deposits are compared, not just the output**, which is the whole point: on the path in
[how a position becomes a single number](../../17-Presentation-Rendering/Position-To-Scalar/how-a-position-becomes-a-single-number.md)
the installed matrix is the **identity**, so the arithmetic is a no-op and the call exists *only*
for what it deposits.

### One detail the test settled rather than assumed

**The accumulator at `022D91A0` holds the sum WITHOUT the translation row.** `00398F90` writes the
packed `x·M[0]` there, reads lanes back out of it, folds in the `y` and `z` terms and stores each
lane again — all **before** the row-3 term is added on the way to the result. So

```text
022D91A0[c] = x*M[0][c] + y*M[1][c] + z*M[2][c]          (no translation)
022D9310[c] = 022D91A0[c] + M[3][c]                       (the result)
```

A reconstruction that deposited the finished value there — the obvious reading — fails **all 123**
point cases on that buffer and no other. It is the kind of difference only a byte comparison of the
side effects can see.

### The tests were changed by their own mutation score, and the source was not

Mutation testing first scored **17 of 20**, with three survivors of one shape: a loop bound `< 4`
changed to `< 5`. Each writes one element past a `Vec4` or `Mat4` — **undefined behaviour the
comparison could not see**, because the harness reads back only `sizeof` bytes and the extra store
lands in padding.

**Canaries after every output buffer in the driver** made the overrun observable and killed two of
the three, taking the score to 19 of 20.

**The last survivor is left alive on purpose.** Line 24's bound writes past `accum` and `result`,
which are **locals inside the reconstruction**, and `*out = result` copies only `sizeof(Vec4)` — so
the extra lane never reaches the interface. It is benign *in this build's stack layout* rather than
truly equivalent; had the compiler placed `result` immediately after `accum`, the mutant would have
corrupted the output and died. **Killing it would mean putting canaries in production code to
satisfy a test**, which is contorting the source to flatter the instrument. Recorded instead.

### What this does not do

- **It does not model the globals.** The reconstruction takes the workbench as parameters and names
  the physical addresses in its header; it does not write `022D91B0` and friends. **The mapping from
  parameters to those addresses is the caller's, and no caller is reconstructed.**
- **`RECONSTRUCTION READY` is not claimed for the subsystem.** Two leaf primitives are implemented;
  the 156 call sites around them are not.

## 6. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00398F90` | the point transform | 377 B | **74** non-EH callers; true leaf; §3 |
| `00397910` | the transform composer | 567 B | **82** non-EH callers; `out = b × a`; §4 |
| `022D91B0`–`022D91EF` | the workbench matrix | 64 B | four 16-byte rows; row 3 is translation |
| `022D91A0`–`022D91AC` | the accumulator | 16 B | shared scratch — ~~**67 writers image-wide**~~ **70 functions reference it** (*recounted 2026-09-12, §15a of the contract; two instruments agree*) |
| `022D9300` | the last input point | 16 B | ~~**41 writers**~~ **68 functions** — shared, not owned here (*recounted 2026-09-12*) |
| `022D8F90` | the last result | 16 B | secondary shared scratch, ~~**47 writers**~~ **64 functions and 668 references** at this address (*recounted 2026-09-12; `47` is `022D9310`'s count, apparently mis-attributed*) |
| `01EF93FC` | `1.0f` | 4 B | the `w` the point transform forces |
| `003970A0` | the matrix getter | 44 B | `BQ-16`; loads the same four blocks |

## 7. What this document does not establish

- ~~**What the matrix *is*.** `BI-9` stays open; §5 constrains the convention, not the meaning.~~
  **`BI-9` ANSWERED 2026-09-12 (FABLE): a current-transform slot with exactly two sources.** The
  slot `022D91B0` has two installers and each installs one fixed matrix: ~~`0039AF70` (232 raw call
  sites) always copies **`02AEEA20`**~~ *(wrong on both counts; see the 2026-09-13 correction below)* `0039AF70` — the workbench's own matrix, the identity at the title screen —
  and `0039B550` (82 raw call sites, function-list-independent index; `Workbench_InstallMatrix4x4`
  on the position-to-scalar page) is called with **`02AEECB0` at all 82** — the projection with the
  viewport folded in, the matrix `PS-2` describes. No other code writes the slot. So the matrix
  *is* whichever of the two a caller last installed: the 232 sites (the draw-side families
  `00435xxx`–`00444xxx`, `00530xxx`–`00531xxx`) run points through the workbench matrix, and the 82
  sites (the fade node `002F1F40` and the `0039C4C0`–`0039CCB0` and `00434CD0`–`00455DB0` families; `00455DB0` interior read 2026-09-17, SWE2-FRONTIER: `00434A70` first at [`00455E38`](../../_index/ADDRESS-INDEX.md), `00434900` next)
  project them; the getter `003970A0`'s seven callers are among the latter, taking the slot back
  after installing. "World, view or projection" was the wrong trichotomy — it is a register.
  > **Corrected 2026-09-13 (FABLE, self-correction; the rest of this answer stands).** `0039AF70` does **not** always copy
  > `02AEEA20`. Its body copies whatever `rcx` points at (`0039AF70`–`0039AF94`), and it has **116 unique call sites**; the
  > "232" counted each site twice (running `rawcalls.py A A` prints every result twice; the index itself holds 116). By the last `rcx` load before each call (`tools/setter_args.py`):
  > - **11** pass a global: `02AEEA20` at 9 and `02AEEBF0` at 2;
  > - **38** pass a stack local, and at least **19** of those locals were just written by `ComposeTransforms` `00397910`.
  >   For example, `004355D0` composes `02AEEBF0` with the element's matrix into `[rbp+0x10]`, runs `0039B960` on three
  >   rows, and installs the result (`004357B5`–`004357F3`);
  > - the remaining **67** pass register- or object-derived pointers.
  >
  > `0039B550`'s "`02AEECB0` at all 82" re-verifies exactly (82 unique sites, all that global).
  >
  > **So the slot is a register with a projection installer and a general installer.** The general installer's users are
  > overwhelmingly effect element code: of `0039AF70`'s 82 calling functions, 58 are one or two calls below the effect
  > type dispatchers `002F4020` / `002F3BC0` / `002F3910` / `0043EBF0`, and 65 are within four
  > ([effect element type dispatch](../../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md)).
  > Each element composes and installs its own transform before running points through `00398F90`. This fits the
  > runtime observation that the slot is not maintained at the title screen and holds different leftovers between launches.
- ~~**Who writes the matrix**, beyond the setter `0039AF70` that `BQ-16` already names.~~ **Answered
  with `BI-9`:** the two installers above write the slot; the two matrices they copy are written by
  **`0024C060`** (called from `0024B9B0` ×4 and the VFX group draw `0024D370` — once per effect
  container, see §11), which composes
  `02AEECB0` with four `ComposeTransforms` (`00397910`) calls after `00250010` queries (`0024C2E3`–
  `0024C3A0`) and stores `02AEEA20`'s translation row `02AEEA50` (`0024C2AA`); `00434CD0` and
  `00435050` rewrite `02AEECB0` (two rows each) on their own paths. `02AEEA20`'s upper three rows
  have **no RIP-relative writer** in the image — the identity the title screen shows is written by
  a route the operand scan cannot see, or it is the zero-initialised BSS plus a row the code sets.
- **Whether the deposits are read by anyone.** Counted across **both** reference instruments,
  `022D9300` has **41 writers / 63 readers** and `022D8F90` has **47 / 59**, so they are **shared
  slots**; that these two functions write them is proven and **who consumes them is not**.

  *(Corrected before publication: this first said `022D8F90` had 76 writers, which is the count for
  the whole `022D8F90`–`022D900E` region in the shared-scratch page, not for this address.
  `check_global_claims.py` — written two blocks ago for exactly this class of error — caught it.)*
- **What the other callers do with the result.** 156 call sites were counted, **none was read**.
- **That the workbench is idle in play.** §5a observed the **title screen only**. A title screen
  need not render a 3D scene, so the idle deposit slots bound the claim to that state. **The
  decisive observation is in-world and was not taken** — it needs a loaded save, which is a physical
  in-game action.
- **What the live blocks at `022D91F0` and `022D9210` are.** Their sizes, their update rate and one
  internal symmetry are measured; their meaning is not.
- **That the two laws in §3 and §4 were observed in the game.** They were **emulated**. §5a observed
  the *state of the globals*, not the functions running.
- **That `00397910` is only a matrix multiply.** Its 567 bytes were not read line by line; the law
  was established by prediction over 150 random pairs, which is evidence about its *behaviour on
  those inputs*, not a proof that no other path exists inside it.

## 8. Falsification checklist

- [x] **The point transform's law.** *Killer:* one mismatched prediction. 200 random matrix/point
      pairs, all exact.
- [x] **The point's `w` is ignored and forced to 1.** *Killer:* output changing with `in[3]`.
      `w = 7` and `w = -123` give identical output; the `1.0f` comes from `01EF93FC`.
- [x] **The composer computes `b × a`.** *Killer:* a case matching `a × b`. The designed case
      separates them completely, and 150 random pairs match `b × a` exactly.
- [x] **Aliasing is safe.** *Killer:* `out == a` differing from the distinct-buffer result. Both
      aliases match, because both inputs are staged on the stack first.
- [x] **The composer writes 64 bytes and no more.** *Killer:* a disturbed sentinel. The 16 bytes
      after the destination were untouched in every run.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

§2's measurements reproduce exactly, and so does the shape of §3's law — by a different route from
the one that produced it.

| claim | measured |
|---|---|
| `00397910` is **567 B**, `00398F90` **377 B** | **567** and **377** |
| `00397910` **82** distinct callers, `00398F90` **74** | **82** and **74** |
| `00397910` calls only `__security_check_cookie` | its **only** direct call target is `00808C40` |
| `00398F90` is "a true leaf" | **no direct call target at all** |
| the matrix lives at `022D91B0` | `00398F94 movups xmm0, [rip + 0x1f40215]` resolves to **`022D91B0`** |

### The law's shape, derived statically

§2 says every claim on this page "was produced by **executing** the shipped bytes, not by reading
them". Reading them gives the same shape:

```asm
00398FA8  movups xmm6, xmmword ptr [rcx]   ; the input point
00398FAF  movaps xmm7, xmm6
00398FBD  shufps xmm7, xmm7, 0             ; broadcast in.x
00398FC1  mulps  xmm7, xmm0                ; x the 16-byte block at 022D91B0  = M[0]
00398FB5  shufps xmm2, xmm6, 0x55          ; broadcast in.y
```

A component broadcast across all four lanes and multiplied by a **16-byte row** is a
**row-vector × matrix** product — `in.x * M[0][*]` as the first term, exactly as §3 states.
**Execution and disassembly agree**, which is worth having on an L2 page whose evidence class is
isolated original-code execution: the two routes are independent.

### ⚠ "156 call sites" is the caller sum

82 and 74 are **distinct calling functions**, and their sum is 156. The **call sites** are more:
**129** into `00397910` and **102** into `00398F90`, **231** together. The sentence gives the caller
figure the site unit — the failure
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s own amendment names, *a count without
its unit cannot be checked*, in the form where the unit is present and wrong.

### ⚠ "no document cites them" was true, and is no longer

`check_novelty_claims.py` flagged this section on its first run. Reading it settles the question in
the page's favour **and** dates it:

| document | first commit | cites |
|---|---|---|
| **this page** | `a5f89e4` — **z268**, 2026-09-08 | — |
| `how-a-position-becomes-a-single-number.md` | `28a3c3f` — **z270**, 2026-09-08 | `00398F90` |
| `CONTRACT-transform-primitives.md` | `24219b7`, 2026-09-12 | both |
| `_index/PARITY-STATUS.md` | — | `00398F90` |

**This page is z268 and the others are z270 and later**, so "no document cites" was **correct when
written**. It is now stale: three documents cite these functions today, one of them a contract
derived from this page. Tensed in §2 rather than struck — the claim was true, and what changed is
the database, not the finding.

> That is the gate behaving as designed: it raises a *candidate*, and a human check decides. Here the
> answer was "true when made, stale now", which no checker could have settled on its own.

**Not claimed:** §3's exact coefficient law and §4's matrix composition were **not** re-derived term
by term — only the first term's shape and the matrix address. §5a's live observation of the state is
untouched. Nothing was executed in this pass; the static reading is the whole of it.

## 10. Residual consumers placed here — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

These functions were uncited residuals whose documented neighbours are this page's primitives or
the workbench vocabulary around them (`00202B10` vec4-add, `00202C90` vec4-copy, `00203170`
identity-store `008C5F80`–`008C5FD0`, `00397910` compose, `00398F90` run-point). Each row is a
call-signature-level read: the listed calls and fields were verified in the body, deeper helper
semantics marked where not walked.

| function | size | role (evidence level) |
|---|---:|---|
| `00275570` | 1835 | cubic easing ramp: divides a constant by count `0209A76C` (`002755BD`–`002755C5`), then iterates steps evaluating `t²`/`t³` terms with constants `009159F4`/`008F311C`/`01CEBC74`/`01CEBC70` (`00275620`–`0027564D`), depositing via `00202B10`/`00202C90`. Curve target record not identified |
| `0028AAA0` | 1692 | quantized-track channel builder: fixed-point decode `00271140` (`1 << ((v>>0x1A)&0xF)` divisor), slot allocation `003F0040` (0x100-stride ring), list append `003F1290` (`+0xD0`/`+0xD8` links); reads `[rcx+0x10]`/`[+0xC]` |
| `0028B140` | 1462 | sibling of `0028AAA0` over `[rdx+0x14]`/`[+0x10]`/`[rsi+0x20]`: same `003F0040`/`003F1290` slot+list pair, `002DD7E0` ×2. Track variant, not read deeper |
| `002A0440` | 5301 | large record translator: `00181xxx` accessor prologue (`00181560`/`001816B0`/`00181870`/`00181910`/`001819A0`), `[rbx+0x47]` flag byte, then `002A1900` ×6 — per-slot record init (copies `[rbx+0x94..96]` bytes into `[out+0x10..18]`). The six `002A1900` sites' differing args not walked; `00181560` first at [`002A04BD`](../../_index/ADDRESS-INDEX.md) |
| `002C3D70` | 1151 | round-robin channel picker: collects `[entry+0x40]&1` from the 4-entry ring `rcx+0xC0` starting at index word `[rcx+0x7A4]`, then scans the ring mod-4 (`& 0x80000003` at `002C3E06`/`002C3E2B`) for the first flagged entry, with a second mod-4 scan in the +3 direction (`002C3E43`/`002C3E6B`) when the first misses; context `rcx+0x780` (`002C3DF4`) |
| `002C84E0` | 829 | tail of a channel-evaluation chain (called from `002C7B10`), gated on byte `[rcx+0x29]`: `002708B0`, `002E9CA0`, `003F0040`, `002C6DC0`, workbench `00202C90`/`00202B10`, then `0035D460` ×4 (`[0209AC30]+0x338` context fetch) + `00271140` decode + `003F1290` append |
| `002D2600` | 721 | transform-block init on `r8` record: `00203170` identity store, `00202C70`/`00202D70` vec ops across `[r8+0xEA]`/`+0xE4`/`+0x128`/`+0x120`/`+0x100`, `00249EE0`, counter/gate `002D8BB0` (`[+0x5C]`/`[+0x5D]` repeat bitmask) |
| `002D4330` | 575 | `[rcx+0xE0]`-keyed small compose: indexed 3-word record fetch `00243260` (`[rcx]` bound `>>2`, `[+0x10]` table → `+0xC`/`+0xE`/`+0x10` words), then state update `00368360` (gated on `022CBE30`, writes `022CBE34`; interior read 2026-09-17, SWE2-FRONTIER: `00368010` first at [`00368500`](../../_index/ADDRESS-INDEX.md), `00367820` at `0036859E`) |
| `002D8D40` | 1595 | vec math on `[rsi+0x5C]`/`[rdi+0x30]`: `00181890`, `00202B70` ×2, `001813F0`. Interior read 2026-09-17 (SWE2-FRONTIER): `00181890` first at [`002D9140`](../../_index/ADDRESS-INDEX.md) — the call profile matches the table's description |
| `00367AA0` | 1042 | nine-field record pass over `rcx+0x10..0x90` + `rdi+0x100`: alternating `00246450`/`00246480`/`00249EE0` calls then `002426F0` (interior read 2026-09-17, SWE2-FRONTIER: `00246480` first at [`00367B99`](../../_index/ADDRESS-INDEX.md), `00246450` at `00367BA6` — the page's alternating profile confirmed); globals `022CBE90`/`022CBE98`, constant `008C5FD0` |
| `00368010` | 559 | transform-chain builder: `00203170` identity ×2, composer `00397910`, plus `003985B0`/`00398910`/`00398C50`/`00202B70`/`00246480`/`00246450`; constants `008C5FD0`, `01CEBB70`, `022CBE32` ×3 |
| `003BE3A0` | 734 | `02B457E0`-block evaluator: `003C1A20` ×2, `003C2320`, `003BD9F0`, `00473CC0`; six rip refs into `02B457E0`. Script/UI-side, interior not walked |
| `003BE950` | 759 | sibling evaluator on `[rcx+0x20..24]`/`[rbx+0x10..1A]`: `0037EB70` ×2, `0029CD00` ×2, `003BCBA0`, `003C0380`, `003BF5E0`, `002F9920`, `003BD6F0` |
| `003F3E40` | 511 | `[+0xE1]` byte-keyed dispatcher (jump table present): `002C9060`/`002C9490` pair ×2, `00253BC0`, `002CCCA0`, `002A5B90`, `002CCB10`; table not decoded in this pass |
| `004027D0` | 623 | small-record transform apply on `[rdx+0xC]`/`[+0xE]` → `[rbx+0x90]`: `00203080`, `00270550`, `00270260` |
| `005680E0` | 326 | gambit-editor icon transform: called by `005691E0`/`00567D80`; reads `[rbx+0x330]`/`+0x340`/`+0x341`, `002CB9C0` + `00368A60`/`00368830` (transform helpers) |
| `005709E0` | 515 | handbook-pane transform: `[rcx+0xD0]`/`+0xF0`, `[r8+0xEC..0xF4]` rect; `005760A0` ×4 |
| `00571F60` | 895 | handbook content-page setup (`00571A50` caller): `[rcx+0xEA]`/`+0xEE`, `00576xxx` widget helpers, `002D48C0`/`002D46F0`, inventory call `002526F0` |

**What is not claimed:** the record types are not named — offsets are stated, not the structs they
belong to. `002A0440`'s six `002A1900` sites, `003F3E40`'s jump table, and `002C7660`'s middle
helpers (`00263C20`/`002ED0B0`/`0037C8F0`/`0035BAD0`) are not opened. Rows marked "interior not
walked" are head+signature reads only.

**The helpers' caller population is not only the draw side.** The workbench vocabulary cited here —
`00202B10`, `00202C70`, `00203080`, `00203170`, `00263C20` — is also called by the **Movement**
layer's `0033xxxx` locomotion family (`00338490`, `00337470`, `00335B60`, `0033D890`, `0033C310`,
`0033DFD0`, `00336E40`, `0033CC80`, `00334220`, `00339F00`, `0033DB60`, `003347C0`, `00335E50`,
`00334E00`, `0033A3D0`, `0033BAA0` and siblings, 64 edges on the pre-§10 graph): the same vector
add/copy/identity helpers serve steering and placement code, so a reconstructed caller cannot assume
a render context. The helpers' remaining edges tell the same story in smaller volume —
**actor** `003F1E90`/`00273750`/`00273A00`/`0046BAC0` call `00202C70`/`00203170`/`00263C20` (7),
**audio** `00362850` calls `00202C70`/`00203080` and `005691E0`/`00571A50` call `00249C60` (4); `00571A50` interior read 2026-09-17 (SWE2-FRONTIER): `00577A00` first at [`00571AB8`](../../_index/ADDRESS-INDEX.md), `003946B0` at `00571ADD`,
**gameplay** `00339630` calls three of the helpers (3), and single edges reach **party**
(`002C7660` → `003590D0`), **platform** (`005760A0` → `00315420`) and **resource**
(`005691E0` → `00249580`) — the workbench vocabulary is image-wide infrastructure.


## 11. The `0024D370` exclusive subtree — all 8 members bound (SWE2-FRONTIER, followup queue)

~~`0024D370` is the per-frame transform workbench update~~ — **corrected 2026-09-19 (FABLE
read it whole, `67f5f6f45`; byte-verified by FRONTIER):** `0024D370` is the **VFX group draw**,
called with (layer, group). It takes the group's container list head from table `020910F0`,
asks the group gate `0024D4E0`, stamps `02092700` with the group number for the duration, and
walks the containers by their `+0x348` link — drawing each only when its `+0x3A8` word matches
the mode and the top nibble of `+0x378` equals the layer, making it current through `0024ED80`
before composing its transform with `0024C060` **once per container**. The call rate is not
once a frame: `00259030` holds eight sequential call sites (verified: `00259067`–`002590BB`),
once per group for the layer, and `002590F0` adds a ninth — up to ~40 draws a frame across the
five layers. The commit side stands as first read: `003AA2E0` runs under the `0039D410` scoped
guard with bit 0 of `02F8F310` raised, beside `003A72F0`/`0024E4B0`, and `02092700` closes at
`-1`. The exclusive census assigns it **8 frontier functions** —
the commit chain below the primitives this page documents. Every member was disassembled from
the shipping image; interior cites are one instruction inside each extent.

| member | role | interior |
| --- | --- | --- |
| `003AA2E0` (231 B) | the commit-publish dispatcher: `00501610`/`005011B0` arms over the `02EBEF70` object, `0020E600` image fixup, `003697F0` | [`003AA34A`](../../_index/ADDRESS-INDEX.md) |
| `00501610` (319 B) | the submit arm — `02EBEFC0`/`02EBEFF0` state, `002D81D0`, `003A22A0` ×2, `003A1DB0` (render-submit family) | [`00501688`](../../_index/ADDRESS-INDEX.md) |
| `005011B0` (610 B) | the sweep driver — `002D81D0`, `002D83B0` ×2, `002D8150` ×3 across the transform records | [`00501285`](../../_index/ADDRESS-INDEX.md) |
| `002D83B0` (381 B) | the per-record transform sweep: walks `02F8F1Ex`/`02F8F2xx`/`02F8DAxx` banks with a `0215E6B0` change-detect, `002D7E30`, `002D8050` | [`002D84C5`](../../_index/ADDRESS-INDEX.md) |
| `002D8050` (242 B) | the twin-arm dispatch — two `002D8150` calls over the record's sub-state | [`002D80F5`](../../_index/ADDRESS-INDEX.md) |
| `0039D410` (30 B) | the scoped guard wrapper — `00864E00()` acquire, tail `00864E60` release | [`0039D418`](../../_index/ADDRESS-INDEX.md) |
| `00864E00` (83 B) | the guard acquire: `0016D6A0(1)` marker, `001A1470([01F7F4C0],0x10)` allocs a 0x10 object, installs vtable `01CCFB38` (RTTI `01D49410`), publishes it at `02EB3828` | [`00864E2B`](../../_index/ADDRESS-INDEX.md) |
| `00864E60` (39 B) | the guard release: `001FB840(&02EB3820)` then `0020E630(&02EB3820, arg)` — the critical-section pair | [`00864E6F`](../../_index/ADDRESS-INDEX.md) |

`002D8150`/`002D81D0`/`002D7E30` and the `003Axxxx`/`0024Cxxx` helpers are shared callees with
other callers — deliberately not census members.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT, fan-in of 837 edges across 59 cited functions.** By Presentation neighbours: `00397910` 76, `002F1F40` 74, `0039AF70` 72, `00398F90` 64, `0039B550` 57. Each edge is a Presentation body calling one of the primitives or their wrappers.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT (4 edges through 3 of this page's functions).** The CombatAction layer reaches this page at `003590D0`, `00263C20`, `00339630`. `FUN_0030ab40` is the worked example, read in full - it is a 266-byte relation query that keeps only **bit 0** of its third argument and answers nothing at all when the first operand is null; **3 of the 4 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE.** `0033D890` on this page calls `BattleStats_FindOwningBattleUnit`, owned by that layer. What it reaches is an 83-byte reverse lookup that walks every battle unit for the one whose `[unit + 0x698]` equals the pointer it is given - which is what identifies that block as the unit's **stats record**; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `00317ED0`, owned by that layer, calls `00229E40` — the
7-B accessor stub this page names among its callee context (`00532xxx` list); the rewards layer
consults the same primitive. Mechanical fan-in, not shared ownership. Read from `edges.tsv`
2026-09-17 (SWE2-FRONTIER).

**Spawn_Encounter_Lifecycle — MECHANICAL (SWE2-EC7-36, 1 edge).** `003208C0` — the shared callee this page cites inside `00337470` — is called by a body on the Spawn_Encounter_Lifecycle layer. Shared-helper fan-in; no spawn relationship to the transform primitives.

**Items_Equipment_Shops_License — MECHANICAL (SWE2-EC7-94, 1 edge).** `00236820` — the `00236850`-counted slot fetch this page cites inside `0033CEF0` — is called by `0031A300` on the Items_Equipment_Shops_License layer. Shared-resolver fan-in; no items relationship to the transform primitives. Edge from `edges.tsv` 2026-09-20.


**CombatAI — MECHANICAL (SWE2-EC7-161, 13 edges).** `00336210` — the guarded transform apply
this page measured — is called by `00336E40`; the same helper family is reached from CombatAI-layer
bodies (`0032A4D0` calls `002315E0`; `00301AD0`/`00308C20`/`003219D0` call `00236820`).
Shared-primitive fan-in; no combat-AI relationship to the workbench. Edge list from `edges.tsv`.

**UI — CLIENT (SWE2-EC7-168, 508 edges).** `00270590` — the settings-table arm that calls this
page's `002708E0` vector compose — sits on the UI layer; the rest of the pair is the workbench's
shared helpers (`0017FFD0`, `001813F0`, `00181560`, `00203080`) called by UI bodies
`002C7B10`/`002D8D40`/`002D9380`/`002A0440` (+504 more). Shared-primitive fan-in; no UI
relationship to the workbench. Edge list from `edges.tsv`.

## The `00434CD0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`00434CD0` (896 B) is the interpolating vertex-channel publisher over the
`02AEECB0` workbench. It reads the three word indices `[rcx+0x14]`/`+0x16`/
`+0x18`, takes the blend weight `xmm6 = [rdx+0x1EC]` and `xmm7 = 1 − w`
(`00434D08`–`00434D21`), saves the four `02AEECB0`–`02AEECE0` matrix rows
(`00434D25`–`00434D4F`), and computes the destination pointers
`dst1 = [02AEED50] + idx16*0x20` (→ `02AEED58`), `dst2 = dst1 + idx14*0x10`,
`dst3 = (dst2 + idx18*8) + idx18*8` (→ `02AEED90`). `00434C50` picks the mode
from `byte[rdx+0x1F1] & 7`, `003977B0` composes the workbench matrix, and the
`+0x20` sections feed member `00431F10` (`00434DE0`). `byte[+0x1F1]` then
gates the remaining channels: bit 3 stamps packed u16 constants
(`0x7233`/`0x8DCC` default, `0x80FF`/`0x7813`/`0x7FCC` for `00229E40` in
1..6, `0x7ED0`/`0x75E3`/`0x7D9C` otherwise, `00434E1B`–`00434ED7`) gated by
`0039A150`/`0024E410`, or — bit 3 clear — `00399B80` may return 0 early after
restoring the matrix rows (`00434ED9`–`00434F04`). Bit 4 sends the `+0x28`
sections through `00433830` and always calls `00432300` (`00434F40`). Bit 5
sends `+0x2C` through `004344C0` into `dst3`; clear → a plain `00861EBA` copy
of `idx18*8` (`00434F56`–`00434FA7`). Bit 6 sends `+0x24` through `00432030`
into `dst1`; clear → `00861EBA` of `idx16*4` (`00434FB9`–`0043500D`). The
matrix rows are restored before return — the save/restore contract.

| member | role | interior |
| --- | --- | --- |
| `00431F10` (284 B) | the position lerp — per-`0x10` element, `src_a * w1` + `src_b * w2` on `float4` lanes with `022D92E0`/`92F0`/`9300`/`9310` staging (`00431F50`–`00431FBE`) | [`00431F6C`](../../_index/ADDRESS-INDEX.md) |
| `00432030` (710 B) | the dst1 channel blend — two-tap weighted combine staging `022D8F90`/`8FA0`/`8FB0` before the `022D92E0` block (`0043209C`–`004321FE`) | [`0043213D`](../../_index/ADDRESS-INDEX.md) |
| `00433830` (3,202 B) | the dst2 channel kernel — no calls; a pure-SIMD weighted blend over the `022D8Fxx` staging cells with a 16-lane output loop comparing `dword[022D8FC0 + rax]` (`00434277`–`004342C1`) | [`004338B4`](../../_index/ADDRESS-INDEX.md) |
| `004344C0` (360 B) | the dst3 channel blend — stages the source descriptors at `022D8F90`/`8FA0`/`8FB0` then blends per element (`004344CB`–`004344F2`) | [`004344CB`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `00434C50`, `003977B0`,
`0039B550`, `0039A150`, `0024E410`, `00229E40`, `00399B80`, `00432300`,
`0020E600`, `00861EBA`. Two of the shared pair are now interior-read
2026-09-17 (SWE2-FRONTIER): `0039A150` (1,558 B) and `00399B80` (1,482 B)
are both call-free SIMD leaves — `mulss` ×18 apiece over `movups`/`movaps`
lane traffic (19 and 23 wide loads), the scalar-blend members of this
family ([`0039A163`](../../_index/ADDRESS-INDEX.md) / [`00399B94`](../../_index/ADDRESS-INDEX.md) prologues).

`00432300` (2,486 B) read to interior anchors 2026-09-17 (SWE2-FRONTIER): the bit-4 `+0x28`
channel's operand unpacker. It `movsxd`s the source descriptors' head dwords (`[rcx]` at
`00432309`, `[rdx]` at `00432321`) into the `022D8F90`/`022D8FA0` staging cells
(`00432313`/`00432324`), loads the `022D8F10` staging row into `xmm4` (`0043230C`), then
`psrldq`-extracts byte lanes (`psrldq xmm0,1` / `psrldq xmm1,7` at `00432335`/`0043233A`,
low lane out to `byte[022D8F91]` at `0043233F`) — the MMI-style lane unpack the register-bank
page describes for this family. No external calls; pure staging into the shared `022D8Fxx`
cells the channel kernels blend from.

## Interior citations — four frontier workbench hubs (2026-09-17, SWE2-EC7)

- **`00398F90`** — the point-through-matrix routine this page's §3 covers (377 B leaf). Interior
  verified: [`00398F94`](../../_index/ADDRESS-INDEX.md) is `movups xmm0, [rip+...]` loading the ACC
  row, then `movaps xmm6, [rcx]` splats the input point's lanes (`shufps 0x55`/`0`/`0xAA`), scales
  each by the workbench coefficient banks, accumulates into the `022D9xxx` global cells, and
  stores the vector result at `[rdx]`. 64 frontier callers — the Presentation fan-in this page's
  pass-22 table counts.
- **`0039B550`** — `Workbench_InstallMatrix4x4` (195 B). Interior verified:
  [`0039B557`](../../_index/ADDRESS-INDEX.md) is `mov dword ptr [rip+...], eax` publishing the low32
  of a `.data` address (`02AEE7F0` — the same arena-offset style as §4's encoding); the body then
  stores the 64-byte source matrix (`movups` ×4 from `[rcx]`) into the `022D9xxx`/`02AEECB0`
  banks, plus a `cvtdq2ps` conversion of an int4 row accumulated into a global float — the
  install step callers invoke before the transform runs.
- **`002DD7E0`** — the bounded dword-table getter (36 B). Interior verified:
  [`002DD7E4`](../../_index/ADDRESS-INDEX.md) is `cmp ecx, dword [rip+...]` — the bounds check against
  the table's count cell at ~~`021586B8`~~ **`0215E6B8`**; on `0 <= ecx < count` and non-null table
  ~~`021586C8`~~ **`0215E6C8`** it returns ~~`table[ecx]` (a dword)~~ **the first dword of the 8-byte entry
  `ecx`** (`002DD7FA`, `mov eax, [rdx + rax*8]`), else `0x80808080` — the opaque default the colour callers
  depend on. 64 frontier callers. *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), re-read from the bytes: the two
  cells were transposed (`rip`-relative targets `002DD7EA + 0x1E80ECE` and `002DD7F3 + 0x1E80ED5`), and the stride is
  8. The entries are `fontcolor.bin`'s colour pairs (face, then shadow/outline); the function returns the face
  colour. See [the loader-bound families](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md)
  and [the blinking icon](../../99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md).*
- **`00202C90`** — `vec4 copy` (7 B). Interior verified: [`00202C93`](../../_index/ADDRESS-INDEX.md)
  is `movups [rcx], xmm0` — the store half of `movups xmm0,[rdx]; movups [rcx],xmm0; ret`. 56
  frontier callers.

NOT claimed: `0039B550`'s published mode dword's semantics. ~~and `002DD7E0`'s table identity
(which colour/attribute table `021586C8` points at) — reads cover mechanics, not the table's
domain.~~ *`002DD7E0`'s table is identified (corrected 2026-09-26, above): `fontcolor.bin`'s face colours at
`0215E6C8`, established on the blinking-icon page on 2026-09-18.*

## Interior citations — frontier workbench hubs, batch 2 (2026-09-17, SWE2-EC7)

Seven more frontier callees in the workbench band, all read against the shipping image:

- `00398030` — 861 B, 47 frontier callers. Interior verified: [`00398073`](../../_index/ADDRESS-INDEX.md)
  is the first `movups` store into the `023393xx` bank — the body loads the three `rcx` rows plus
  three `rdx` rows, splat-multiplies each lane by the coefficient bank and writes the results back
  through `rdx` while publishing intermediates to the globals; the full three-source matrix
  product, not a leaf.
- `00399600` — 1,296 B, 43 frontier callers. Interior verified: [`00399654`](../../_index/ADDRESS-INDEX.md)
  is `shufps xmm7, xmm7, 0` splatting `rcx`'s row 0 — the sibling long-form compose that also
  serialises a packed tail record to `[r9]` and ORs an accumulator into a global qword.
- `0039ADE0` — 238 B, 42 frontier callers. Interior verified: [`0039ADE7`](../../_index/ADDRESS-INDEX.md)
  is the first `mulss` — a strict in-place row-scale: `[rcx]` row 0 × `[rdx]`, row 1 × `[rdx+4]`,
  row 2 × `[rdx+8]`, row 3 × `[rdx+0xC]`; 16 multiplies, no other ops.
- `00398480` — 273 B, 39 frontier callers. Interior verified: [`003984AF`](../../_index/ADDRESS-INDEX.md)
  is `jmp r8` — a six-way `r8d ∈ {0..5}` computed dispatch; every arm calls `00250010` then two or
  three of `003985B0`/`00398730`/`00398910`/`00398A90`/`00398C50` in a fixed per-mode order on
  `rdi`'s vec4 fields — a per-mode transform pipeline selector.
- `00434A70` — 466 B, 37 frontier callers. Interior verified: [`00434AAB`](../../_index/ADDRESS-INDEX.md)
  is `call 00398F90` — composes `0039AF70` → `00398F90` on `rbx`'s `+0x30` vec4, diffs the result
  against the `01EA47xx` bank, runs `atan2f` (`00861F02`) on the delta vector, then
  `00398910` → `00398030` to republish the corrected transform.
- `00434900` — 360 B, 37 frontier callers. Interior verified: [`0043494D`](../../_index/ADDRESS-INDEX.md)
  is `call 00398F90` — the same compose skeleton (bank diff → `003A2690` → `00398030`) with a
  different constant row; the two bodies are sibling entry points into the same correction pass.
- `0039B620` — 13 B, 47 frontier callers. Interior verified: [`0039B626`](../../_index/ADDRESS-INDEX.md)
  is `mov [rip+0x27531c4], ecx` — the two-instruction accumulator: `ecx += dword[03B0E7F4]`,
  `dword[03B0E7F0] = ecx`. The element-types pages call it from the "workbench compose" chain;
  it is the bank's running-sum write-back, not a slot resolver.

NOT claimed: the physical meaning of the `023393xx`/`03B0E7Fx`/`01EA47xx` banks as EE vs VU0
residence (that split is UQ-38/39's open question on the register-bank page) — only the data-flow
shapes above are measured.

## Interior citation — frontier hub `003970A0` (2026-09-17, SWE2-EC7)

`003970A0` — 44 B, 28 frontier callers at census; the matrix getter `BQ-16` already names.
Interior verified: four `movups`/`movups` pairs copy the four 16-byte blocks at `022D91B0`,
`+0x10`, `+0x20`, `+0x30` into `[rcx]`..`[rcx+0x30]` verbatim
([`003970AA`](../../_index/ADDRESS-INDEX.md) is the first store) — a 64-byte snapshot of the
vector-unit-5 quadrant into caller storage, exactly the "slot back" read the page describes.
No arithmetic, no tag handling.

## Interior citation — frontier hubs `00202B10` / `002C9490` (2026-09-17, SWE2-EC7)

- `00202B10` (81 B, 12 A-callers) — the vec4 add this page already names. Interior verified:
  scalar `movss`/`addss` per lane at [`00202B14`](../../_index/ADDRESS-INDEX.md)–`00202B49`,
  staged to the stack then stored as one `movups` — component-wise `dst = a + b`, no fused SIMD.
- `002C9490` (211 B, 10 A-callers) — the band-build writer paired with `002C9060` in the `003F3E40`
  dispatcher. Interior verified: the target is `[0209AC30]+0x2C8` — a band record whose `+0xD0`
  dirty bits are cleared then re-set per field change (`+0xCE`/`+0xC6` word compares at
  [`002C94BA`/`002C94CE`](../../_index/ADDRESS-INDEX.md)); on any change it snapshots
  `+0xCA`->`+0xD6`, writes deltas `+0xD4`/`+0xD8`, stamps `+0xDA` from `01E0C0E8` minus
  position-minus-arg, `+0xE0` from `0208F4D0`, and `+0xDC` = `(arg3 * 60) / 1000` via the
  `0x10624DD3` magic divide — a milliseconds->frames-style rate conversion on the band period.

NOT claimed: the `0209AC30`+0x2C8 record's owner beyond "the band the apply arms animate".

## Interior citation — frontier hub `002D46F0` (2026-09-18, SWE2-EC7)

`002D46F0` — 206 B, 9 A-measured callers; a widget mirror-update in the same `+0xC0`/
`+0xC8` record family as `002D45C0`. Interior verified: gated on `002D4B70(rcx) == 1`
(`002D46FE`); it computes `-(word[+0xEA] * sbyte[+0xED])` and `-(word[+0x100] *
word[+0xF2])` and, when either differs from the linked object's `+0x98`/`+0x9A`, clears
that object's `+0x80` bit 0 and writes the new pair at [`002D4758`](../../_index/ADDRESS-INDEX.md)–`002D4767`.
When `[+0xC8]` is non-null it tail-calls `00247510(obj, (word[+0xF4]+word[+0xF2])*byte[+0xEC]
+ sbyte[+0xEE] + sbyte[+0xED], 0x8000)` at `002D47B3` — the change-notify down the chain.


## Interior citation — frontier hub `00398C50` (2026-09-18, SWE2-EC7)

`00398C50` — 379 B, 6 A-measured callers; the trig-table field init that fills a `022D92xx`
workbench-adjacent float block. Interior verified: `divss` by a constant (`00398C6B`), two
`cvttss2si … & 0x7FFF` indices into the sine table `r8 = 01F404E0` (`00398C76` lea;
[`00398CD0`/`00398CF8`](../../_index/ADDRESS-INDEX.md) fetch `table[idx]` and
`table[0x2000 - idx]` — the sin/cos pair), then a 16-instruction `movss`/`shufps` run scatters
the prior block (`01F405xx`/`01F406xx`) and the two fresh samples into the destination rows,
and `00397ED0` consumes the packed frame at [`00398DAC`](../../_index/ADDRESS-INDEX.md). GS-cookie
checked. This is the scale/rotation preset publish the primitives then install from.


## Interior citation — frontier hub `002D48C0` (2026-09-18, SWE2-EC7)

`002D48C0` — 101 B, 23 callers (5 A-measured); the ring-position publish the transform rows'
consumers share. Interior verified: `[+0xE8]` takes the new index `dx` (`002D48C6`), then
`(dx - 1 + [+0xEC]) mod [+0xEC]` — a `idiv` remainder at [`002D48D9`](../../_index/ADDRESS-INDEX.md)
— wraps back one slot and lands on `[+0xF0]`; the `rem == quot` arm bumps by one
(`002D48EA`). When the `[+0xC0]` sub-record exists it receives the scaled pair
`[+0x9E] = [+0x100] * slot` and `[+0x9C] = [+0xEA] * [+0xEC]` (`002D48F2`–`002D491C`). The
previous-slot math is the "where the ring just was" half of the publish.


## Interior citation — frontier hubs `003F1290`, `001819A0`, `003F0040` (2026-09-18, SWE2-EC7)

`003F1290` — 56 B, 15 callers; the intrusive-list append the channel builders use.
Interior verified: node's `+0xD0`/`+0xD8` links cleared (`003F1292`/`003F1299`); empty list
(`[rcx] == 0`) installs `rdx` as both head `[rcx]` and tail `[rcx+0x10]` (`003F12A5`);
otherwise the old tail's `+0xD0` takes `rdx` and `rdx`'s `+0xD8` back-links it
([`003F12B1`–`003F12C3`](../../_index/ADDRESS-INDEX.md)). Textbook push_back on an embedded
doubly-linked list.

`001819A0` — 109 B, 15 callers; the accessor prologue `002A0440` runs per slot.
Interior verified: `001B1C00()` supplies the shared object ([`001819BE`](../../_index/ADDRESS-INDEX.md)),
then `001B2410(ecx=ebp, edx, r8=esi, r9=rdi)` runs with six staged stack args including
`1` at `[rsp+0x38]` and the caller's `arg4` at `[rsp+0x30]` ([`001819F3`](../../_index/ADDRESS-INDEX.md)).
An argument-marshalling adapter, not a transform.

`003F0040` — 162 B, 14 callers; the `0x100`-stride ring's slot allocator the builders use.
Interior verified: cursor `[rcx+0xC]` bounds-checked against `[rcx+8]` (`003F0044`–`003F004B`),
`rbx = [rcx] + idx*0x100` (`003F005C`–`003F0068`), the row's `+0x60`/`+0x6C` get
`cosf`/`sinf` of the supplied angle ([`003F0070`/`003F007B`](../../_index/ADDRESS-INDEX.md)),
`+0x64` zeroed, `+0x68` sign-flipped via `01CEBDA0` (`0x80000000` mask), `+0xC` = `1.0f`,
`+0x80` a flag dword — the unit-circle velocity row a track channel starts from.

## Interior citation — frontier hub `002C9060` (2026-09-18, SWE2-EC7)

`002C9060` — 191 B, 10 callers; the dirty-field transition recorder on the `0209AC30`
record's `[+0x2B8]` sub-record. It clears flag bits 0–1 of `[+0xD0]`, sets bit 0 when the new
`ecx` differs from `word [+0xCE]` and bit 1 when `edx` differs from `word [+0xC6]`
(`002C9087`–`002C90B1`); when either changed it latches bit 2, saves the old pair to
`+0xD4`/`+0xD6`, the deltas to `+0xD8`/`+0xDA`, stamps `+0xE0` from `0208F570`, and converts
the `r8d` argument from milliseconds to frames — `imul ecx, ebx, 0x3C` then the
`0x10624DD3`/`sar 6` magic divide (`r8d·60/1000`) — into `[+0xDC]`
([`002C90FE`](../../_index/ADDRESS-INDEX.md)). The same `0209AC30` record whose `+0xCE`/`+0xD0`
fields `002C9430` (batch 10) reads; this is the write side.

## Interior citation — frontier hub `00249EE0` (2026-09-18, SWE2-EC7)

`00249EE0` — 211 B, 9 callers; the three-word clock-field adder. Given two `{w0, w2, w6}`
records it orders them by `w0` (`cmovge` at `00249F03`), then performs carry-aware
addition: `w6' = w6_small + w2_small`, wrapped by subtracting the larger `w2` when the sum
exceeds it ([`00249F74`](../../_index/ADDRESS-INDEX.md)–`00249F8D`), `w2'` taking the larger
`w2` operand, `w0'` the larger `w0`. Result lands at `[r11]`/`+2`/`+6`, returns 1. This is
wraparound time arithmetic — `w6`/`w2` are sub-unit/unit fields with the larger operand's
unit as modulus — the primitive the transform-workbench's frame-clock merges run on.


### Interior citation — frontier hub `003946B0` (2026-09-18, SWE2-EC7)

`003946B0` — 78 B, 20 callers: the four-word record copy `00571A50` runs mid-
body. `002432B0(rcx + 0x50, r9 = rbx)` resolves a record; when `rbx` is non-null
its words `+0xA`, `+8`, `+6`, `+4` are copied to `[rbx+0x98]`, `[+0x9A]`,
`[+0x9C]`, `[+0x9E]` ([`003946C5`](../../_index/ADDRESS-INDEX.md)) — the
signed/unsigned mix of `+6` (`movsx`) vs `+4`/`+8`/`+A` (`movzx`) marks the
format's one signed field.
### Interior citation — frontier hub 00202DE0 (2026-09-18, SWE2-EC7)

**00202DE0** (33 B, 4 A-measured callers) — the support-record copy §5a's STATE observer walks past. `movups [rdx] → [rcx]` (16-byte copy), `00216660(rcx)` (the record-init sibling), `[+0xC] = 0` — the node init when a STATE entry is re-parented. In-scope: `movups` store [`00202DEC`](../../_index/ADDRESS-INDEX.md); `00216660` call [`00202DF3`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-19 update (2026-05-15) — `003977B0` in-place 4×4 matrix post-multiply

`003977B0` (349 B) is the in-place 4×4 matrix post-multiply this page names: it snapshots `rcx`'s 0x40-byte matrix onto the stack (`movaps` ×4 at `003977CD`..`00397805`), then runs a 4-iteration column loop (`r11d=4`, `0039780A`..`003978E8`) — each pass computes `out[r][i] = Σ_k stack[r][k]·rdx[k][i]` for the four rows (`mulss`/`addss` chains at `00397821`..`003978D7`) and stores the column into `[rcx+i*4]`, `[rcx+0x10+i*4]`, `[rcx+0x20+i*4]`, `[rcx+0x30+i*4]` — i.e. `M[rcx] = M[rcx] · M[rdx]` evaluated against a snapshot so the write-back can't alias the operand. This is the compose-step the workbench runs per accumulated transform.

## SWE2-EC7-23 update (2026-09-18) — `003985B0` LUT-index composer

`003985B0` (379 B) is the trig-LUT index composer: `xmm1 / [01CEBC78]` scale,
`r8 = [01F004E0]` LUT base, `ecx = 0x2000` quarter-phase, `cvttss2si; and eax,
0x7FFF` wrapped index, `xmm4` lanes stored to `[022D92FC]`/`[022D92F0]`/
`[022D92F8]` globals — the same `0x8000`-entry table family `003977B0`
composes, publishing its output through the shared vector globals the
transform primitives read. Interior anchor `003985CB` (the divisor).

## SWE2-EC7-27 update (2026-09-18) — `002D8150` threshold classifier

`002D8150` (114 B) is the per-record helper the `005011B0` sweep driver
calls three times: cookie-checked, it lays out a stack threshold table
(`00917230`/`00917240` constants plus `0x100`/`0x200`/`0x400`) and
returns the index of the first entry `>= ecx` — the size-class lookup
feeding the transform-record dispatch. Interior anchor `002D81A0` (the
table scan).

## SWE2-EC7-28 update (2026-09-18) — `002CCCA0` fixed-shape request thunk

`002CCCA0` (77 B) is cookie-checked: builds the `{1, rcx, edx, 0}`
record on the stack and calls `002CCD40` on it — the constant-kind
request wrapper over the same-object callee. Interior anchor `002CCCC4`
(the kind-1 store).

## SWE2-EC7-29 update (2026-09-18) — `002CCD40` kind-keyed `+0x290` ensure

`002CCD40` (272 B) is the lazy ensure `002CCCA0` runs for the
constant-kind record: `[rdi]` selects a `*(0209AC30) + kind*8 + 0x290`
slot; an occupied slot returns null (already ensured); empty allocates
`00244F50(0xF0, 002CCE70)` — the `002CCE70` init arms set `+0xE8 = 1`
(kind `0x13`), clear the kind slot (kind `0x12`), or fall to `005C5230`.
The publish bank is picked by kind: `[rdi+0x18] != 0` -> `0208EA20`,
kind 2 -> `0208EA38`, 3 -> `0208EA48`, 4 -> `0208EA50`, else
`0208EA28`; `00246AD0(bank, slot)` submits and `slot[+0xE0] = bank`
back-links it. Interior anchor `002CCE07` (the `call 00246AD0`
publish).

## SWE2-EC7-30 update (2026-09-18) — `002708B0` uniform vec3 scale

`002708B0` (41 B) is the scale helper the `002C84E0`/`002C7B10`
channel-evaluation chain calls: `out[0..2] = xmm2 * in[0..2]` — a
uniform scalar multiply over the first three floats — with
`out[3] = in[3]` copied through untouched. Interior anchor `002708B6`
(the first `mulss`).

## SWE2-EC7-34 update (2026-09-19) - `00571F60`

`00571F60` (895 B) is a transform primitive init - zeroes `[rcx+0xEA]`/`[+0xEE]`, `00576030`/`00577550`/`00576740`/`00576CA0`/`005760A0`. Interior anchor `00571F94` (an `00576030` call).

## SWE2-EC7-35 update (2026-09-19) - `002CCE70`

`002CCE70` (733 B) is a transform-primitive record body - `0209AC30`/`01E0C1D8`/`01E0C1DC` state, four `00247930` plus `002D8BB0`/`002DC290`/`002D8C80`/`00247570`/`0017FFD0`. Interior anchor `002CCF89` (a `00247930` call).

## SWE2-EC7-35 update (2026-09-19) - `002D2600`

`002D2600` (721 B) is a transform sibling - `002D8BB0`/`00249EE0`/`00203170`/`00202D70`/`00202C70` plus `00808C40`. Interior anchor `002D2729` (a `002D8BB0` call).

## SWE2-EC7-36 update (2026-09-19) - `00337470`

`00337470` (647 B) is a transform-primitive body - `008C5F6C`/`01CEBBA8`, `003208C0` triple plus `004692F0`/`0032A6A0`/`00203080`/`00202B10`/`00202C70`/`00202C90`. Interior anchor `00337547` (a `003208C0` call).

## SWE2-EC7-36 update (2026-09-19) - `004027D0`

`004027D0` (623 B) is a transform sibling - `00915508`/`01CEBBA8`/`01CEBC08`/`01EF93F0`, `00270550`/`00270260`/`00203080`/`00808C40`. Interior anchor `0040286F` (an `00808C40` call).

## SWE2-EC7-37 update (2026-09-19) - `002D4330`

`002D4330` (575 B) is a transform-adjacent body - `01F44830`, `00243260`/`00368360`/`00808C40`. Interior anchor `002D4475` (a `00243260` call).

## SWE2-EC7-37 update (2026-09-19) - `005709E0`

`005709E0` (515 B) is the handbook-pane transform the page names - `[rcx+0xD0]`/`+0xF0`, `[r8+0xEC..0xF4]` rect, `005760A0` quadruple plus `00808C40`. Interior anchor `00570A7C` (a `005760A0` call).

## SWE2-EC7-38 update (2026-09-19) - `00398730`

`00398730` (467 B) is a call-free scalar transform - `divss` by the `01CEBC78` constant, `mulss` by `00D10820`, `cvttss2si`, `and 0x7fff` - a normalize-and-quantize pass. Interior anchor `0039875E` (the `divss` step).

## SWE2-EC7-38 update (2026-09-19) - `0033BAA0`

`0033BAA0` (465 B) is a transform-adjacent body - `01F44830`/`008F3108`/`01CEBBA8`, `00334AB0`/`00335B60`/`0033D660`/`00203170`/`0033CB70`/`00202F00`. Interior anchor `0033BAD3` (a `00334AB0` call).

## SWE2-EC7-39 update (2026-09-19) - `00398A90`

`00398A90` (446 B) is a call-free normalize-and-quantize sibling of `00398730` - `divss` by the `01CEBC78` constant, `mulss` by `00D10820`, `cvttss2si` + `and 0x7fff`, indexing the `01F004E0` table. Interior anchor `00398ABE` (the `divss` step).

## SWE2-EC7-39 update (2026-09-19) - `002C6DC0`

`002C6DC0` (432 B) is a transform-primitive body - `01F44830`, `00861F0E` pair plus `002752E0`/`00808C40`. Interior anchor `002C6E8A` (an `00861F0E` call).

## SWE2-EC7-39 update (2026-09-19) - `00334220`

`00334220` (431 B) is a transform-matrix compute - `01CEBB70`/`01CEBC50`/`01CEBC78`/`01F004C0`/`01F44830`, `0033CB70`/`00203170`/`00202F00`/`00202B70`/`00202FE0`/`00202B10`/`003A1920` pairs. Interior anchor `003342A5` (a `0033CB70` call).

## SWE2-EC7-40 update (2026-09-19) - `002426F0`

`002426F0` (370 B) is a transform-primitive body - `01CEBBA8`/`01E0C150`/`0208EA90`, `002D8BB0` pair plus `002D8D10`. Interior anchor `0024280C` (a `002D8BB0` call).

## SWE2-EC7-40 update (2026-09-19) - `002A1900`

`002A1900` (369 B) is a transform sibling - `01CEBBA8`/`01F44830`, `00202B70`/`00202CA0`/`00181350`/`00808C40`. Interior anchor `002A1A02` (a `00202B70` call).

## SWE2-EC7-40 update (2026-09-19) - `00398910`

`00398910` (376 B) is a transform-matrix body - `01CEBC78`/`01CEBDA0`/`01EF93F0`/`01F004E0`/`01F44830` plus the `022D92F0`..`022D9300` field block, `00397ED0`/`00808C40`. Interior anchor `00398A69` (a `00397ED0` call).

## SWE2-EC7-40 update (2026-09-19) - `003BD6F0`

`003BD6F0` (358 B) is a transform sibling - `01CEBB70`/`01CEBBA8`/`01CEBD80`/`01EF93F0`/`01F44830` plus `022D9198`/`022D91E0`/`022D91F0`, `0036DDA0`/`0036DD90`/`0036DD80`/`00861F14`/`00203080`/`00202DE0`. Interior anchor `003BD76D` (a `0036DDA0` call).

## SWE2-EC7-41 update (2026-09-19) - `0033CC80`

`0033CC80` (351 B) is a transform helper - `01CEBDA0`/`01F004C0`/`01F44830`, `00202FE0`/`00203170` pair/`00202E90`/`00202B70` pair/`0033CB70`/`00202F00`. Interior anchor `0033CCEB` (a `00202FE0` call).

## SWE2-EC7-42 update (2026-09-19) - `0024E4B0`

`0024E4B0` (308 B) is a transform body - `02F97340`, `00862C40` single call. Interior anchor `0024E4BE` (the `00862C40` call).

## SWE2-EC7-42 update (2026-09-19) - `00335E50`

`00335E50` (305 B) is a transform helper - `01F004B0`/`01F44830`, `00203080` triple/`00202DE0`/`00202E10`/`00202FE0`/`00202B10` pair/`0033D3E0`. Interior anchor `00335E86` (a `00203080` call).

## SWE2-EC7-43 update (2026-09-19) - `003A2690`

`003A2690` (294 B) is a transform-primitive body - `01F44830`, `00250010`/`00398470`/`00808C40`. Interior anchor `003A26CA` (a `00250010` call).

## SWE2-EC7-50 update (2026-09-19) - `00216660`

`00216660` (186 B) is a body - `00861F14` plus `008C2C68`/`008C2C70` import calls. Interior anchor `0021669B` (the `00861F14` call).

## SWE2-EC7-53 update (2026-09-19) - `00334AB0`

`00334AB0` (370 B) is a transform-adjacent body - `00202B70`/`00202F00`/`00203080`/`00203170`/`0033CB70`/`004686D0`/`004687F0`/`004692F0`/`00808C40` plus `01CEBC08`-`01CEBC9C` rdata. Interior anchor `00334AED` (a `004686D0` call).

## SWE2-EC7-58 update (2026-09-19) - `002D7E30`

`002D7E30` (168 B) is a transform-primitive body - `00182CA0`/`00183720`/`005C3A30`/`00863060` plus `0209E6B0`. Interior anchor `002D7E74` (a `00182CA0` call).

## SWE2-EC7-61 update (2026-09-19) - `0039CCB0`

`0039CCB0` (152 B) is a transform-primitive body - `00399B10`/`0039B550`/`003A0870`/`003A0AA0`/`00808C40` plus `01F44830`/`02AEE900`/`02AEECB0`. Interior anchor `0039CCE5` (a `0039B550` call).

## SWE2-EC7-62 update (2026-09-19) - `003A0870`

`003A0870` (555 B) is a transform-primitive body - `0020E630`/`0020E670`/`0020E680`/`0039CDC0`/`008642A0`. Interior anchor `003A0890` (a `0020E680` call).


## SWE2-EC7-62 update (2026-09-19) - `003A0AA0`

`003A0AA0` (488 B) is a transform-primitive body - `0020E680`/`0024E460`/`0039CDC0`/`003A2C70`/`003A3D20`/`008647C0` plus `01EFAC20`/`02AEE900`/`02AEE908`/`02AEE910`. Interior anchor `003A0AE0` (a `0020E680` call).


## SWE2-EC7-62 update (2026-09-19) - `00271140`

`00271140` (150 B) is the fixed-point decode the transform-primitives page names - call-free `1<<cl` / `1<<((v>>0x1A)&0xF)` divisors, `word[rdx]` -> `cvtdq2ps`/`divss` -> `movss [r10+8]` (verifies the page). Interior anchor `0027117D` (the `divss` normalize store).



## SWE2-EC7-63 update (2026-09-19) - `0039CDC0`

`0039CDC0` (330 B) is a transform-primitive body - `0017FFD0`/`00202B70`/`0024E640` plus `00915248`/`01CEBBA8`/`02AEEB20`/`02AEEBA0`. Interior anchor `0039CDE5` (a `0024E640` call).



## SWE2-EC7-66 update (2026-09-19) - `0024E640`

`0024E640` (132 B) is a transform-primitive body - `0024E4B0`/`00862C40` plus `02F97340`. Interior anchor `0024E646` (a `0024E4B0` call).


## SWE2-EC7-68 update (2026-09-19) - `00202E90` / `00183720`

`00202E90` (100 B) is the copy-and-rotate primitive the
`0033xxxx`/`003EDxxx` transform callers run: four `movups` pairs
copy the caller's `0x40`-byte source block into `rcx`, `xmm2` is
saved to `xmm7`, the two trig import stubs `00861F08` and
`00861F0E` are applied to it in turn (results landing `xmm6` ->
`xmm2` and `xmm1`), and the tail `00217790(rcx, xmm1, xmm2)`
applies the pair. Interior anchor `00202EC7` (the `00861F08` call).

`00183720` (52 B) is the register-on-resolve helper the transform
and loader bodies share: a null `rcx` returns at once; otherwise
`00189120(rcx)` resolves the object twice and `00185A90(result,
&0017ECC0, rcx)` registers the `0017ECC0` leaf on it with the
original argument as the callback's data. Interior anchor `00183749`
(the `00185A90` call).

## SWE2-EC7-70 update (2026-09-19) - `003F1230` axis-fill measured

`003F1230` (84 B) is the `(a, b, -a, a)` write the transform workbench
shares: `00861F08(xmm1)` is held in `xmm7`, `00861F0E(xmm1)` lands at
`[+0x64]`; then `+0x60 = xmm7`, `+0x68 = -xmm7` (xor `0x80000000`), and
`+0x6C = xmm7` - a quaternion-shaped axis fill off the two scalar helpers
the application page names.
Interior anchor `003F1263` (the `xorps` sign flip).

## SWE2-EC7-71 update (2026-09-19) - `00862C40` paired getter measured

`00862C40` (46 B) is the `+0x90`/`+0x94` pair read on the `01F7F4D8`
singleton the transform bodies share: NULL `rcx`, NULL `rdx`, or a NULL
global all short-circuit; otherwise `[rax+0x90]` -> `[rcx]` and
`[rax+0x94]` -> `[rdx]`.
Interior anchor `00862C56` (the first store).

## SWE2-EC7-73 update (2026-09-19) - `003E5700` + `003A1F20` transform helpers measured

`003E5700` (12 B) is the `+0x670` movaps row copy: 16 bytes from
`[rcx+0x670]` to `[rdx]` - the transform row fetch.
Interior anchor `003E5707` (the `movdqa` store).

`003A1F20` (109 B) is the divider the transform workbench callers
share: `r9d = ecx * edx`, then `(r8d - 1)` indexes a `0x39`-bound jump
table at `00281F90` selecting /3, /2, /4 or /8 rounding divisions
(`cdq`/`sar` and `&3`/`&7` bias forms); out-of-range returns `r9d`
unscaled.
Interior anchor `003A1F4C` (the `jmp rcx` table dispatch).

## SWE2-EC7-74 update (2026-09-19) - `00318CA0` gated service call measured

`00318CA0` (44 B) is the gated forwarder: when the `02EC1378`
singleton exists it runs `002315E0(rcx, rax, r8)` and sign-extends
the word result; absent returns -1 - the singleton-gated call the
transform bodies share.
Interior anchor `00318CB9` (the `002315E0` call).

## SWE2-EC7-77 update (2026-09-20) - `00202CA0` vec4 reciprocal scale measured

`00202CA0` (79 B) is the vec4 scale-by-reciprocal: `xmm3 =
1.0f/xmm2`, then `[rcx]` gets the `movups` of `{[rdx], [rdx+4],
[rdx+8], [rdx+0xC]} * xmm3` - a uniform divide folded into a
multiply.
Interior anchor `00202CCC` (the `+0xC` component multiply).

## SWE2-EC7-80 update (2026-09-20) - `00577A00` + `00577550` + `00576860` measured

`00577A00` (20 B) is the `+0xC0` setter on `[02CA9738]`: a live
global stores `rcx` to `[rax+0xC0]`, a NULL one does nothing.
Interior anchor `00577A0C` (the store).

`00577550` (383 B) is the `ecx`-armed dispatcher on `[02CA9738]`:
negative `ecx` or `byte[+0x100] & 2` returns 0; arms 0-4 loop the
`[r11 + ecx*8 + 0xC8]` record's `word[+8]` elements calling
`00575E80` then `00315910` under the `00D23750` identity-permutation
byte table; arm 5 iterates the `[r11+0xF0]` list `word[+8]` times
calling `005768E0`/`00576860` per (row, col) with `00315AD0` on the
hit conditions; arm 6 returns 1; arm 7 runs `00316930` and returns 1.
Interior anchor `005775B2` (the arm-7 call).

`00576860` (127 B) is the `edx == 5` lookup arm-5 uses: the record's
`[rcx+0xF0]` list supplies `word[rdx+0xC + r10*8 + 0xE]` flags - bit1
yields `0xFFFF`, else bit0 picks `0xFF` vs `0xFFFF`; `r9d >= 7`
returns that value, else `word[rdx+0xC + (r9 + r10*8)*2]` returns the
table entry.
Interior anchor `00576899` (the flag-word fetch).

## SWE2-EC7-83 update (2026-09-20) - `0043E7B0` + `00434760` + `00434630` measured

`0043E7B0` (140 B) is the `r9d`-count qword push the workbench callers
run: each iteration stores `[rcx+i*8]` to `02EB8738`, rotates the
`02EB8790`/`02EB8798`/`02EB87A0` triplet, and writes `eax`/`edx` into
`[rdx+i*8-4]`/`[-8]` - a counted copy driving the global ring.
Interior anchor `0043E7F4` (the `[r8-4]` store).

`00434760` (404 B) is the larger bank-transform: `[r8]`'s xmm seeds
`02EB9010`/`02EB9350`, `[rcx]` qwords feed `02EB8E80`-family rotates,
and each of `r9d` iterations spins `xmm3` through the `02EB8F90` bank
- `mulss` by `xmm4`/`xmm5`, scaled adds at `rip+0x1ac4bda`, stores to
`02EB91A8`/`02EB91A4`/`02EB92D8`/`02EB92E0` - before the output xmm
lands at `[rdx-4]`/`[-8]` and `02EB9498` counts down.
Interior anchor `00434840` (the `mulss xmm2, xmm4` bank step).

`00434630` (289 B) is the reduced sibling: same `[r8]` seed into
`02EB8FA0`/`02EB92D0`, same `r9d` bank loop at half the steps, single
output `[rax-8]` and the `02EB9490` countdown - the two-step variant
of `00434760`'s three-step pass.
Interior anchor `004346BA` (the `mulss` bank step).

## SWE2-EC7-84 update (2026-09-20) - `008642A0` object factory measured

`008642A0` (133 B) is the 0x68-byte object factory the transform
callers reach: `0016D6A0(1)` gates, `001A1470(global, 0x68)`
allocates, `01CCFAF0` lands as the first-field pointer, `00864210
(obj, edi)` initializes, `[obj+0x58]` goes 1, and `obj+8` returns
through `[rsi+8]` - 0 on allocation failure.
Interior anchor `008642CA` (the `001A1470` allocation call).

## SWE2-EC7-88 update (2026-09-20) - `003C0340` + `003BF5E0` measured

`003C0340` (51 B) is the byte-pair sum over
`[02B457E0+0xE0]`: `byte[+9]` bounds `ecx`, the
`word[+rcx*2+0xA]`-relative entry supplies `byte[+0]` and
`byte[+1]`, and their sum is returned - a two-byte field
probe, call-free.
Interior anchor `003C0366` (the byte-sum read).

`003BF5E0` (217 B) is the four-arg query `003BEC50` wraps: the
`[rcx+0x120]` slots (0xA8 stride, `byte[+0x10]` category gate)
each hold a `word[+0xA]`-relative word table scanned for a
`(word, byte[+2])` pair matching `(esi, edi)`; a hit returns
`qword[r10 + idx*8 + 0x18]` and optionally stores the
`dword`-relative continuation pointer into the caller's
out-slot.
Interior anchor `003BF697` (the hit arm).

## SWE2-EC7-90 update (2026-09-20) - `0039F9F0` display-record builder measured

`0039F9F0` (814 B) is the record builder the primitive callers
run: the `02F8F2C6` word indexes a `02F8F2F8` slot (x5) whose
record takes a `0020E680` allocation, the minimum of the
`+0x4`/`+0x14`/`+0x24`/`+0x34` fields, an `02AEE910`-derived
flag nibble, and the `0024E460`/`003A3D20`/`003A2C70` result OR;
`00864D10` + `0039CDC0` produce the output record, which then
receives eight `divss` component ratios (`+0x40`..`+0x74`), 16
byte->float lanes (`+0x80`..`+0xBC`), the `+0xE0`/`+0xE8`/
`+0xD8` pointer triple (the `02AEE900 == 6` arm selecting
`02AEE908`), and a `0020E670` publish before tailing
`00182F50`.
Interior anchor `0039FA30` (the `0020E680` call).

## The primitives executed — [`EXP-130`](../../_experiments/EXP-130-transform-predicate-exec.md), adopted 2026-09-20 (OPUS)

This page names `00202B10`, `00203080`, `00202FE0`, `00202DE0` and `00216660` as workbench
vocabulary. EXP-130 ran them — 35/35 functional cases, 36/36 mutants, stable across three
processes — and three of the results are **contract facts a caller can be wrong about**,
not restatements.

### `00216660` is normalize-**or-zero**, and it returns something nobody declared (OPUS)

The primitive is `NORM(rcx = vec*)`, normalize in place. It has **three separate gates to
the zero path**, and they are different kinds of test:

| gate | reached how | identity |
|---|---|---|
| `_isnan(len²)` nonzero | `call q[0x8C2C68]` | **proven by the PE import directory** |
| `_finite(len²)` zero | `call q[0x8C2C70]` | **proven by the PE import directory** |
| `comiss len², FLT_MIN` + `jbe` | `d[0x907698]` ships `0x00800000` | the constant is in the image |

`jbe` **includes equality**, so `len² == FLT_MIN` takes the zero path — measured, not read
off the mnemonic. The zero path at `0x216701` writes `q[v] = q[v+8] = 0`: **all sixteen
bytes, `w` included.** The scale path leaves **`w` untouched**. So *"the vector is
normalized"* is not one postcondition — **`w` survives on one path and is destroyed on the
other**, and a caller that relies on `w` has to know which path ran.

**And it does have a way to know, which is the part worth flagging: `NORM` leaves a live
value in `rax`.** `_finite`'s return `1` survives the epilogue on the scale path; the zero
path's `xor eax, eax` leaves `0`. Nothing declares this as a return value — but it is
observable, it is bit-exact in both directions, and the `m-pred-r8d` mutant demonstrates it
is **live** rather than incidental. `NCOPY` (`00202DE0`) propagates it: its own exit `rax`
*is* NORM's residual. Treat it as an undeclared out-parameter that a reimplementation must
reproduce, not as junk.

*The identities were nearly wrong, and how they were fixed matters.* The predicate cells
were first scoped as `q[0x86AC68]`/`q[0x86AC70]` — `int3` padding and code bytes, nonsense
targets, the same rip+displacement arithmetic slip EXP-129 made. The corrected cells
`q[0x8C2C68]`/`q[0x8C2C70]` resolve **through the import table**, so `_isnan` and `_finite`
are named by the PE rather than inferred from behaviour.

### `dst == src` is safe on the binary primitives, by construction (OPUS)

`VSUB` `00203080`, `VADD` `00202B10` and `VSCALE` `00202FE0` compute all four components
into `rsp` temporaries and commit with **one `movups`**, so aliasing the destination onto a
source is safe — verified directly by the `vsub-alias` and `vadd-alias` cases rather than
assumed from the shape. The read order is fixed (`a0, b0, a4, b4, a8, b8, aC, bC` for the
binary ops; `+0, +4, +8, +0xC` for `VSCALE`), which is what makes the single-store commit
sound. **A reimplementation that writes components as it computes them is not equivalent**,
and this is the kind of difference a functional test over non-aliased inputs never sees.

**The cross product belongs in that list and was missing from it.** `XPROD` `00202E10` has the
same construction — all four components into `rsp` temporaries, one `movups` to commit — and its
alias case is verified in the same way, by EXP-129's `xprod-alias` rather than by the shape
(adopted 2026-09-20, OPUS). It matters more here than for the binary ops, because a real caller
uses it: `0040B430`, the MWeather basis publish, crosses its own local with the direction it has
just published **straight back into that same local**, which is only sound because the commit is
a single store. `dst = d × a`, `dst.w = 0` unconditionally — so the `w` lane of either input is
discarded rather than carried, which is half of why that caller's `w` is dead end to end. See
[`mweather-resource-format.md`](../../03-World-Area-Field/Weather/mweather-resource-format.md).

### The corridor predicate is XZ-only, and its third probe is not the one you would guess (OPUS)

`PRED` (`00335E50`, `rcx=p1, rdx=p2, xmm2=scale, r9d=flag`) builds a perpendicular offset
and probes three segments. Two facts are easy to get wrong from a static read:

- **`tmp.y` is flattened to zero before the normalize** (`xorps xmm0` / `movss [rsp+0x24]`),
  so the offset is strictly in the XZ plane. A pure-Y delta degenerates: `pred-degen-y`
  feeds `p1 − p2 = (0, 8, 0)`, which normalizes to zero, so the offset is zero and all
  three probes see the **unshifted** points.
- **The third probe is `Q(p2 + off, p2 − off)`** — a self-difference *at the destination*,
  measuring the corridor's width at `p2`. It is not `p1`-based like the first two.

Only an exact `1` counts as a pass: the result comes back through `sete`, and the
`pred-ret2` case proves a returned `2` becomes `0`.

**What is not claimed here.** The nav-grid query `Q` was a scripted boundary in this
package; its own tree was executed separately in EXP-131 and is that package's to report.
Nothing on this page asserts what the predicate is *for* — only what it computes.

## SWE2-EC7-91 update (2026-09-20) - `0039B780` + `003962F0` + `003952D0` measured

`0039B780` (191 B) is the tight staged-copy loop the primitives
call: `r9d` iterations each copy `[rcx]` into `022D8FA0`, pull
`[r8]`'s index into `022D8FB0`, multiply staged `022D90xx`
lanes, `movq`-emit through `[rdx+8]`, and stop when the index
reaches the `022D9xxx` watermark.
Interior anchor `0039B7A0` (the loop head load).

`003962F0` (612 B) is the clamp-calling member: [rcx]'s vec4
seeds the `022D9xxx` workbench, `0036DD80` runs mid-pass, the
dot-product chains accumulate per 0x10-advanced iteration, and
`movups [rax-0x10]` writes each staged vec4 until the watermark
matches.
Interior anchor `00396399` (the `0036DD80` call).

`003952D0` (522 B) is the `003954E0` sibling over a second
staging block: the `[rdx-4]` source walk steps 0x10, the
dot-product and `cvtps2pd`/`andps` magnitude chain runs, and
the staged vec4 lands at `[r9]` when the watermark turns.
Interior anchor `003953EB` (the `cvtps2pd` magnitude arm).

## SWE2-EC7-92 update (2026-09-20) - `00394E50` transform-workbench staging pass measured

`00394E50` (501 B) is the larger member of the `004355D0`/`00444340`
staging family: `[rcx]`'s vec4 seeds `022D92xx` scratch, a `r8d`-counted
loop walks `[r10]`'s vector stream 0x10 at a time, the broadcast
`mulss`/`addss` chains stage `022D93xx`/`022D94xx` lanes, and the
`cvtps2pd` + `andps` abs-mask + `cvtpd2ps` normalization runs before
each staged vec4 commits at `[r9]` until the watermark matches.
Interior anchor `00394E9F` (the `dec r8d` loop count).

## SWE2-EC7-94 update (2026-09-20) - `0033CEF0` + `0033BC80` measured

`0033CEF0` (772 B) is the bounded turn-and-approach pass
`003394A0`, `00339F00` and `0033A720` call: `004686D0` and
`00236820` resolve the pose record and its `+0x698` link, the
`+0xE4`/`+0xE8` bound pair is picked by a `[rbx+0xB0]` vs
`[+0x104]` `comiss`, and each angle is walked toward its target
through `0033CB70` wraps - `cvtss2sd`+`andps` absolute value,
`divss`-scaled step `+0xF8`, `maxss`-style clamp at `+0x118`, the
result landing in `[rbx+0xBC]`/`[rbx+0xB4]`. The epilogue rewrites
`[rsi]`'s flag word: when `0x7FE0` bits are clear and the
`0030C0D0`/`+0x698`/`+0x714==0x4022` gates pass, it ANDs off
`~0x7FE0` and ORs `0xA0` (or `0xC0` on gate failure).
Interior anchor `0033CFA7` (the first `0033CB70` angle-wrap call).

`0033BC80` (225 B) is the conditional facing write `00338140` and
`0033BAA0` run: `+0x174` on the `+0x108` record must equal 3 and
`+0x1F4` on the `+0xF8` record must differ from 3, then `003208C0`
projects the argument vec4's z-lane (`shufps 0xAA`), `comiss`
against `[rbx+0x44]` falls back to the `[rbx+0x40]` vec, and the
`+0xC0 - [rbx+4]` delta - `cvtps2pd`/`andps` absolute - must clear
the `05D9521`-constant threshold before `[rbx+0xB8]` gets
`+1.5708` or `-1.5708` (the `0x3FC90FDB`/`0xBFC90FDB` pi/2 pair)
and `[rbx+0xB0]` copies `[+0xE8]`.
Interior anchor `0033BCD4` (the `003208C0` call).

## SWE2-EC7-96 update (2026-09-20) - `00309AE0` measured

`00309AE0` (40 B) is the mode-picked constant read `00336E40`
and `00338490` call: `0030D9A0` returning 1 selects the
`068F6824` float, anything else the `05DA7E00` float - the
two-constant branch the transform pass reads per query.
Interior anchor `00309AEE` (the mode-1 `movss`).

## EXP-132 shared-math helpers placed here — 2026-09-20 (SWE2-ORACLE, ownership decision)

Placement decision answering `OPUS-REQ-ORACLE-NAV-ADOPTIONS-HAVE-NO-OWNING-PAGES`:
the six shared-math bodies executed real under EXP-132 are **owned by this page** —
they are the workbench vocabulary itself, filed here for what they compute, not for
who calls them. Grep presence in crossing tables was never ownership; this note is.

| address | role (executed real, EXP-132) | size |
|---|---|---:|
| `0033CB70` | AWRAP — angle wrap to `[−π, π]` | 128 B |
| `00203170` | MLOAD — shipped const 4×4 matrix copy | 44 B |
| `00202F00` | RBUILD — rotation-matrix builder (`cosf`/`sinf`) | 100 B |
| `00217880` | ROTCOL — in-place column rotation `(x,z)→(z·sin+x·cos, z·cos−x·sin)` | 234 B |
| `00217060` | MXV — `out[j] = X·m[j] + Y·m[4+j] + Z·m[8+j] + W·m[12+j]` (flat f32 `m`; SSE products, summed Y+X, then Z, then W) - a ROW vector times a row-major matrix, equivalently a column-major matrix times a column vector; NOT row-major storage left-multiplying a column vector, which transposes: input (1,2,3,1) with diag(2,3,4,·) and last four (10,20,30,2) gives the original (12,26,42,2), against (2,6,12,142) *(vector side qualified 2026-09-27 (OPUS, ASTRA-RETURN-OPUS-MATRIX-APPLICATION-CONVENTION))* | 235 B |
| `00202B70` | MXVW — frame-temp MXV wrapper | 31 B |

The executed semantics land via OPUS's EXP-132 findings adoption
(`REQ-OPUS-NAV-CONSUMER-FINDINGS`); the evidence is
[`_experiments/EXP-132-nav-consumer-exec.md`](../../_experiments/EXP-132-nav-consumer-exec.md).
The two nav predicates from the same experiment (`0033A3D0` PATHW, `00335F90` BLKCHK)
are owned by the nav-mesh page, not here — they query the grid, they do not compute
transforms.

## SWE2-EC7-104 update (2026-09-20) - `00270260` measured

`00270260` (396 B) is the segment-counted float
interpolator `00366B80`, `00271960` and
`004027D0` call: for `r8d <= 2` it is a plain
lerp - `dst[i] = a[i] + (b[i] - a[i]) * t` for
`x / y / z` with `w` fixed at `1.0f`. For
`r8d > 2` it splits `t` into integer and
fraction, and depending on where the integer
part sits inside the `r9 - 1` span either calls
`00202C90` directly on the `(r9 - 1) << 4`
element, or builds the `t, t^2, t^3` scratch
row and runs the `00202C90` / `00276220` /
`002762A0` basis evaluation, then two
`00202B70` combines and a `00202D80` half-scale
into `dst` - the cubic path the longer ramps
take. The `01F44830` cookie xor is the
standard stack guard.
Interior anchor `0027028B` (the first lerp
component).

## SWE2-EC7-107 update (2026-09-20) - `00246480` + `00246450` measured

`00246480` (306 B) is the
`0x24`-byte record composer
`00245E60`, `00272310`, `00367AA0`,
`00368010` and `00553F40` call: the
`[rcx + 0x98]` qword is copied to
`[rdx]`, and when `byte[+0x40]` bit
7 arms the `movsx byte[+0xAC]` /
`+0xAD` pair adds into `word[rdx]` /
`[rdx + 2]`; the destination record's own
`word[+4]`/`[+6]` are re-staged at
`+0xC`/`+0xE`, the
`+0xA4..+0xA7` signed bytes write/
add `+8`..`+0xE` under the same
flag, `dword[+0x40]` bit `0x8000000`
adds `+0xAE`/`+0xAF` to `+0xC`/`+0xE`,
`float[+0x1C]`/`[+0x20]` default to
`1.0`, `dword[+0x24] = byte[+0xA0]`,
then `00244A20(rcx)` runs - the
call answers 0 only when the
composed record is entirely default
(`+0x10..+0x18` zero, `+0x1C`/`+0x20`
`1.0`).
Interior anchor `002464B5` (the
`+0xAC` add).

`00246450` (43 B) is the head half
`00367AA0`, `00368010` and
`003EE420` call standalone: the
same `[+0x98]` qword copy plus the
`byte[+0x40]`-gated `+0xAC`/`+0xAD`
signed adds - the base-copy arm the
composer reuses.
Interior anchor `0024646C` (the
`+0xAC` add).

## SWE2-EC7-112 update (2026-09-20) - `001813F0` measured

`001813F0` (107 B) is the
seven-argument forwarder
`002D8D40`, `002D9380` and
`003F0610` run: `001B1C00()`
fetches the target object,
then `001B0CE0` is called
with the register arguments
rotated - `rcx` becomes
`rdx`, `edx` becomes `r8d`,
`r8d` becomes `r9d`, `r9d`
drops to the first stack slot,
and the caller's three stack
arguments shift up one slot
each. Pure repack, no logic.
Interior anchor `00181441`
(the `001B0CE0` call).

`0057A1F0` (221 B) is the three-way fork `0024C060` invokes mid-compose: reads `[[0209AC30]+0x158]` and its `+0x187` byte — flag clear runs `00561BE0`, flag set runs `00559540`; when the `+0x158` record itself is absent it falls back to `002465D0()` -> `00202C70(02CA9750, result)`, then `00183280` scales a `0.5f` triple by the result and `0039ADE0(02CA9750, &vec)` stores it — an absent-record default-write path.

Interior anchor `0057A21F` (function `0057A1F0`).

`00183280` (109 B) is the unit-scale ratio `00559540`/`00561BE0`/`0057A1F0` fold into their composed transforms: `00189120()` supplies the shared state object twice — `00186AA0(obj)` gives the divisor and `00186A90(obj)` the dividend; the scale factor comes from `001DD110(001DDAB0())` when the record exists, else the `1.7778f` constant at `008C5B38`. Returns `(float)dividend * factor / (float)divisor`.

Interior anchor `001832CC` (function `00183280`).

`005713C0` (536 B) is the kind-gated row fetch `00571A50` runs on the `+0xD0` record: `[rcx+0xE8]` kind 4 masks `r9d` with `0xC50`, kind 5 with `0xCF0`; a masked `0x400` arm requires `r8d` bit 0xA (and zeroes `esi`), a masked `0x800` arm requires `r8d & mask` nonzero, every other value returns 0. Survivors take `005709E0(rcx, esi)`'s extent (`-1` bails to 0) and `002D1820([rdi+0xD0], &out30, &out60)`'s mode — mode 2 with an odd `(+0xF2 + +0xF4)·+0xEC + +0xEE + +0xED` extent answers with one `002D3BA0` 0x80-pitch call; otherwise `002D3BA0` steps at pitch `esi == 0 ? 0x10 : 0x40` until the recomputed extent equals `005709E0`'s answer, returning the last step's result.

Interior anchor `0057143E` (function `005713C0`).

`00570CE0` (1758 B) is the repeat-scroll engine `00571A50` drives on the `+0xD0` record: recomputes both `(+0xF2 + +0xF4)·+0xEC + +0xEE + +0xED` extents, snapshots context via `00367EC0`, and advances the `0209E65C` rate counter against `01E0CF88` with `001E0A10` resampling on wrap. A zero rate is one `002D3BA0(rbx, esi, r14d, r12d, 0)` pass; a nonzero rate is clamped to +/-1 when `|ecx|` reaches `01E0CF84` and `[rbx+0xE8]` <= 0xC, the sign folds into `esi`/`r14d` bits 0x10/0x40, and `002D3BA0` iterates `|ecx|` times with a `+0xF4 == +0xF0 - 1` clamp. The second phase clears bit 0xC off the flag words, steps `005715E0` inside a `[+0xE4]` 0x800000 bracket until the `[r13 + extent*2 + 0xF0]` low-nibble == 1 marker or the cap, commits through `002D47C0`, clears `[+0xC0]+0x80` bit 0 and `+0xE0` bit 0x1000000, closes the context with `00368820`, and on a residual delta finishes `002D49F0` with mode 8/9/0xA under `[+0xE4]` |= 0x8000000.

Interior anchor `00570F9D` (function `00570CE0`).

`0056A3D0` (904 B) is the pane-transition state machine `005691E0` steps: `[+0x331]` selects arms 0-6 — arm 0 resets `+0x330`/`+0x33B`; arm 1 `002497B0(0x5A8)`-creates the child bound to `this+0x160 + [+0x337]·0x20` with `+0x584`/`+0x588`/`+0xC8` back-refs, then dispatches on `+0x336` (0 parks, 1/2 gate on `0056B100`/`0056AE80` into `+0x332` = 0x1005, 3 validates `+0x337`/`+0x33C` against `[+0xD8]+0xE8` into `+0x338` = 1) — every live arm tail-`003697F0`s the child; arm 2 counts `+0x333` down into a `+0x332`-low-byte re-dispatch; arm 3 recomputes the `[+0xD8]` extent into `002D66A0` direction codes {0x10, 0x20, 0x40, 0x80} and reloads `+0x333` = `+0x33A`; arm 4 `002D66A0`s the `01E0C2A0` constant then promotes `+0x33C` -> `+0x337` when `+0x338` else parks at 7; arm 5 `005685B0`s a rect into `002D78B0`/`002D7CB0` and sets `+0x33B`; arm 6 `002D7CB0`s and parks via `+0x332` = 0x1000. State 7 falls off the table — the halt.

Interior anchor `0056A427` (function `0056A3D0`).

`0056A1D0` (502 B) is the 0x20-stride record writer `005691E0`/`0056AC50` run: `r8d` >= 0 selects `this+0x160 + r8·0x20`. `edx` mode 2 stores the arg word at `[+0x12]` — `0xFFFF` puts the `002F9860(0x3EB)` empty marker at `[+8]`, otherwise `0035D330(0x14, w)` -> `002B58B0([obj+0x18], 0)` resolves it, and a live `[+0x10]` adds `0035D330(0xB, w << 16)` with `[+0x15]` = (`[+0x38]` != 3). Mode 1 mirrors the same pair on `[+0x10]`/`[+0]`, forcing `[+0x15]` = 2 on the `0xFFFF` arms. Mode 0 toggles `[+0x14]` — set when absent with both words live — folds record `r8-1` into `[+0x124]` and returns 0x29 (set) / 0x5E (clear). Mode -1 resets the record to the empty marker (`-1` when `r8d` <= 0, else 0x19). All write paths `00569F90(this)`-repack and stamp `0208F570` into `[+0x344]`; the default return is 0x18.

Interior anchor `0056A397` (function `0056A1D0`).

`0056A010` (299 B) is the pane reset `005691E0`/`00567990`/`00568280` run: `002CC2A0()` gates; a live `rcx` resolves `00282DF0([0209AC30]+0xDE0)` whose `[+0x60]` seeds `[+0xF0]`; `+0x33E` = 0, `+0x341` = 0xFF; `002CEE00(7)` and `00567B60(this)` follow; `+0x354` = 0x80808080; `[+0x174]` selects `+0x352` bit 0 plus `+0x350` = 0x80 (else both clear); `+0x357` takes the `+0x350` byte; `0208F570` stamps `[+0x344]`; a `+0x33E` mode other than 3 picks `00D234F8[mode]` for `[+0xD8]+0x106`, mode 3 instead `00254A10()`s into 8|9; `[+0xD8]+0xF8` = 1 and `002D1AC0(rec, 1, 0x8000)` commits; the tail `002527B0(6, [0209AC30]+0xDE0, 4)` notifies.

Interior anchor `0056A110` (function `0056A010`).

`00569F90` (119 B) is the record repack `005691E0`/`0056A1D0`/`00567D80` run after field writes: for `i < byte[+0x126]` it copies the word pair `[+0x190 + i·0x20]`/`[+0x192 + i·0x20]` to `[+0xF4 + i·4]` and folds `byte[+0x194 + i·0x20] != 0` into `[+0x124]` bit i; the tail `003282C0(this+0xF4, byte[+0xF0])` commits the packed array.

Interior anchor `00569FB0` (function `00569F90`).

`00568280` (54 B) is the `0027F360()`-gated reinit `005691E0`/`00567D80` run: only a 1 return opens `00249C60(0x51)` then `0056A010(this)` — the shared gate plus pane reset; the gate's own result is returned either way.

Interior anchor `005682A4` (function `00568280`).

`005680E0` (326 B) is the pane reset `005691E0`/`00567D80` run (the gambit-editor icon transform this page's table lists): zeroes the `[+0x198]` array up to `[+0xD8]+0xE8` entries at stride 0x20; `[+0xD8]` gets `+0xE0` |= 0x200000 with low word 0xFFFF, `+0xF6` = 0, `+0x114` = 0, `+0xE4` bits 0x40000/0x20000/0x180000 cleared, `+0xF8` = 1; `002CB9C0(1)`, `+0x340` bit 0 clear, `+0x341` = 0xFF, `00368A60(0)`, `00368830(1)`; a nonzero `+0x330` byte invokes `[this]`'s vfn with a `{0x121, 0, 0, 0}` record.

Interior anchor `0056820A` (function `005680E0`).

`00368830` (38 B) is the `022CBE32` flag-word bit-4 setter `005680E0`/`005687F0`/`005641F0`/`00564650` run: a nonzero `ecx` ORs `0x10` into the shared transform flags; zero clears it.

Interior anchor `0036884A` (function `00368830`).

`002D78B0` (68 B) is the `0209AC30` `+0xF0` record writer `0056A3D0`/`005691E0`/`0056BE40`/`005109B0` run: a null table or `ecx > 7` returns; else the `(ecx + 8)·24`-indexed entry gets `+0x14` &= ~0x10 and the word quadruple `{dx, r8w, r9w, stack arg}` lands at `+0`/`+2`/`+4`/`+6` — the rect/arm notification the pane-transition state machine posts.

Interior anchor `002D78D3` (function `002D78B0`).

`002D66A0` (30 B) is the shared direction-word writer `0056A3D0`/`0027F5D0`/`005116E0`/`0055AA00`/`0056A140`/`0056BE40` run: a nonzero `cx` is stored to all three of `02F973AC`/`02F973AE`/`02F973B0` — the direction cell `0056A3D0` feeds its {0x10, 0x20, 0x40, 0x80} codes into.

Interior anchor `002D66A8` (function `002D66A0`).

`005715E0` (303 B) is the bounded `002D3BA0` step `00570CE0` iterates on the `+0xD0` record: `[rdi+0xE4]` gains bit 2, `002D45C0(rdi, 0)` opens, `+0xE4` bit 0x400000 is XOR-mirrored from `+0xE0` >> 2, then `002D3BA0(rdi, r15d, r14d, ebp, {arg, 0})` runs — a result of 3 stores 1 through the out pointer. The `(+0xF2 + +0xF4)·+0xEC + +0xEE + +0xED` extent picks `[rsi + extent·2 + 0xF0]`; a low nibble of 1 with a zero `ebx` folds `r9d` into the return. `+0xE4` bit 0x400000 clears, `002D45C0(rdi, 1)` closes, bit 2 clears, and `ebx`-or-`r9d` returns.

Interior anchor `00571665` (function `005715E0`).

`00567D80` (514 B) is the record-toggle `005691E0` steps per index: `00368240(this+0x160 + edx·0x20)` answering 1 writes `[+0xD8]+0xFC` = 0xFF and exits; `edx == 0` clears `+0x353`, toggles `[rec+0x14]` bit 0, runs `00311AF0(byte[+0xF0], new)`, and writes `+0xFC` = 0x12 or 0x13 by the post-toggle state; `edx > 0` zeroes `+0xFC` then dispatches on `byte[+0x33E]` — modes 1/2 store the mode into `02CA9700`'s `+0x360` and, when `00264150()` returns 0, run `0056B350(this, rec, 1|2)`; mode 0 walks `02CA96E0[[+0x35C]]`'s `+0x340` bit-0 gate — a `+0x341` byte equal to `esi` re-toggles `[rec+0x14]` (set only when both `+0x10`/`+0x12` are non-0xFFFF), folds `esi - 1` into `+0x124` as set/clear, `00569F90`-repacks, stamps `0208F570` into `+0x344`, writes `+0xFC` = 0x29 / 0x5E (0x5 on the both-0xFFFF arm, 0x37 on mismatch), then `00567F90` and `005680E0` run; the un-gated case tail-calls `005687F0(this, esi)`.

Interior anchor `00567F03` (function `00567D80`).

`00567B60` (540 B) is the record-array builder `0056A010` runs: `00861EC0(this+0x160, 0, 0x1A0)` zeroes the thirteen 0x20-stride records; `00327C40(this+0xF4, byte[+0xF0])` resolves the packed source whose `+0x32` byte is the count `r13d`; `0035D330(2, [+0xF0])` -> `002B58B0([obj+0x18], 0)` seeds `[+0x160]`; `00309B40(+0xF0)` lands in `+0x174`; `+0x340` = 0. Per record `i < r13d`: the `+0xF4` word pair at `i·4` land in `rec+0`/`rec+2` — `0xFFFF` stores the `002F9860(0x3EB)` empty marker at `[rbx-0x10]`/`[rbx-8]`, else `0035D330(0xB, w<<16)` / `0035D330(0x14, w)` -> `002B58B0` resolve the text; `rec+5` = (`resolved[+0x38]` != 3), forced 2 when both words are `0xFFFF`; `rec+4` takes the `[r14+0x30]` bitmask bit (rotating `esi`). Then `02CA96E0[[+0x35C]]`'s `+0x302` byte at channel `[0209AC30]+0xDE0`·4 seeds `+0x33E`/`+0x33F`, `002D48C0` runs on `[+0xD8]` and `[+0xE0]` with `r13d + 1`, and the tail `002D4840([+0xD8], 0, word[+0x300 + ch·4], 1)` commits.

Interior anchor `00567C6D` (function `00567B60`).

`005679D0` (263 B) is the pane rebuild `005691E0` runs: a set `02CA96E0[[+0x35C]]` `+0x340` bit 0 clears `[+0xD8]` `+0xE0` bit 0x200000, clears `+0xE4` bit 0x80000, ORs 0x100000, runs `002D4840(rec, 0, byte[+0x341], 0)` and returns 0; a clear bit instead `002CEE00(-1, 7)`, `00569F90`-repacks, `00244F00` releases each of the three `02CA96E0` entries (to `02CA96F8`), then `002CA110`, `002CB8B0`, `002C9400(0x6E)`, `002C9060(01E0C3CC, 01E0C3BC, 01E0C3E8)`, `002C9890(0x6E)`, `002C9490(01E0C3D0, 01E0C3BC, 01E0C3E8)` and `002CF3C0` — the full teardown/rebind.

Interior anchor `00567A77` (function `005679D0`).

`00567990` (54 B) is the `0027ED10()`-gated reinit `005691E0` runs — the twin of `00568280` on a different gate: a 1 return opens `00249C60(0x51)` then `0056A010(this)` — the shared gate plus pane reset; the gate's own result is returned either way.

Interior anchor `005679A9` (function `00567990`).

`005678F0` (153 B) is the fade-byte compute `005691E0` runs: with `[+0xC0]` bits 0-1 set, `00248F40((+0xC0 >> 2) & 0xF, +0xCC, 0208F570 - +0xD0)` interpolates into xmm0 and `+0x343` = `cvttss2si(+0xC4 + +0xC8·xmm0)`; when xmm0 reaches 1.0f the byte is instead written as `+0xC4 + +0xC8` and `+0xC0` bits 0-1 clear — the interp's terminal state. The tail `005682C0(this, 0)` runs either way.

Interior anchor `00567927` (function `005678F0`).

`002CEE00` (138 B) is the pane-mode commit `005679D0`/`0056A010` run on `0209AC30`'s `+0x308` record: `[+0x308]+0x10C` = `dl` and `+0x10D` = `cl`; `cl <= 5` sets the `+0x310` record's `+0xC4` to 1, `cl > 5` instead clears `+0x10C` bit 1 and zeroes `+0xC4`; then `+0x104` takes the `0208F570` frame stamp and `+0x100` = 6 — the mode field the pane arms leave behind.

Interior anchor `002CEE71` (function `002CEE00`).

`0056B350` (376 B) is the mode-1/2 record arm `00567D80` dispatches into: a null `[+0xE8]` is `00244F50(0x5A8, 0056B4D0, &ctx)`-created with context `{this, +0x35C, rdx, r8d, 0}`, registered through `00246AD0(0208EA28, obj)`, and `002470D0`'d; then `00368250(&stack)`'s word pair minus `[+0x98]`/`[+0x9A]` lands in `+0x348`/`+0x34A`, `002D4570([+0xD8])` and `002CBA30()` run with `[rsi+0x17]` = `r8b`, and `+0x353` = 1; a nonzero `+0x343` byte masks `+0xC0` to `(& ~0x3A) | 5`, mirrors the byte into `+0xC4` and negated into `+0xC8`, stamps `0208F570` into `+0xD0` with `+0xCC` = 0xC; finally `r8d` == 1 picks `-dword[01F2CB10]` else `-dword[01F2CB14]` for `002468A0(this, that, movsx +0x9A, 1, 0xC8)`.

Interior anchor `0056B4AB` (function `0056B350`).

`005687F0` (172 B) is the un-gated arm `00567D80` tail-calls: `00368240(rec)` answering 2 returns 1 early; else `[+0xD8]` takes `+0xE0` = `di` (the index), `+0xF6` = 1, `+0xE4` |= 0x40000 | 0x20000, `+0xF8` = 0; `002CB9C0(1)`, `00368A60(4)` and `00368830(0)` run, then `+0x340` |= 1 and `+0x341` = `dil` — it sets the very `+0x340`-gate/`+0x341`-index pair `00567D80`'s mode-0 dispatch reads.

Interior anchor `00568881` (function `005687F0`).

`005682C0` (293 B) is the `+0x350`/`+0x352`/`+0x354` fade driver `005678F0` tails into: `+0x354` = 0x80808080 first; a clear `[+0x174]` zeroes `+0x352` bits 0-1 with `+0x350`/`+0x357` (`edx` set) or steps `+0x350` by -0x10 floored at 0 (`edx` clear); a set `[+0x174]` with `edx` forces `+0x352` bit 0 and `+0x350`/`+0x357` = 0x80, while `edx` clear ramps `+0x350` by -0x20 (floor 0x80) or +0x20 (cap 0xFF, clearing `+0x352` bit 1 at the cap) and a `+0x350` byte over 0x80 fills `+0x354`-`+0x356` before `+0x357` takes it under `+0x352` |= 1.

Interior anchor `00568362` (function `005682C0`).

`00567F90` (332 B) is the move-and-repack `00567D80`/`0056A1D0` run on the `this+0x160` record array: `rsi` = `byte[+0x341]`, `edi` = the `(+0xF2 + +0xF4)·+0xEC + +0xEE + +0xED` extent; the `rsi·0x20` record is held in xmm2/xmm3 while the array shifts — `rsi` inside the extent `rep movsq`s records `rsi+1..extent` down over the gap, `rsi` past it reverse-copies up — and the saved record lands at `this+0x160 + extent·0x20`. The tail is `00569F90`'s pack loop inline: `+0x190+i·0x20`/`+0x192+i·0x20` word pairs to `+0xF4+i·4`, `byte[+0x194+i·0x20]` folding into `+0x124` bit i, ending `003282C0(this+0xF4, byte[+0xF0])`.

Interior anchor `00568049` (function `00567F90`).

`00561BE0` (180 B) is the `[0209AC30]+0x320` brightness apply `0057A1F0` runs: `002465D0()` resolves the target; a live record takes xmm6 = `[rbx+0x8C]` when `[rbx+0x40]` bit 0x15 is set (else 1.0f), `00202C70(rbx+0xE0)` opens the transform, `00183280` on the `{xmm6, xmm6, xmm6, 1.0f}` vector scales it by the returned xmm0, and `0039ADE0(rbx+0xE0, &stack)` commits.

Interior anchor `00561C4E` (function `00561BE0`).

`002CB9C0` (103 B) is the `+0x2E0`-record flag arm `005687F0`/`005680E0` run: on `0209AC30`'s `+0x2E0` child, `[+0xC0]+0xF0` is rewritten to `(arg ? 2 : 0) | (old & ~2)` and `002CAFE0([+0xC0], byte[+0x168], 0, 1)` re-drives it; a null `+0x2E0` returns without touching anything.

Interior anchor `002CBA1D` (function `002CB9C0`).

`002465D0` (24 B) is the context-record picker `00561BE0`/`00559540`/`0057A1F0` call: `01E0280C` nonzero returns `0208EC50`, zero returns `0208EC10` — the two global transform/context records the selection-side arms choose between.

Interior anchor `002465E0` (function `002465D0`).

`00559540` (155 B) is the `+0x100` sibling of `00561BE0` that `0057A1F0` also runs: on `0209AC30`'s `+0x320` record, `00202C70(rbx+0x100)` opens the transform, `00183280` scales a `{0.8f, 0.8f, 0.8f}` vector (`01CEBB70` family constant `0x3FCCCCCD`) by the returned factor with a 1.0f alpha, and `0039ADE0(rbx+0x100, &stack)` commits — the same shape as `00561BE0` on the sibling transform.

Interior anchor `00559594` (function `00559540`).

`002030E0` (142 B) is the copy-and-offset record helper `00555F80`'s map draw runs beside `00202E90`/`00202D70` (`0027B200`, `003F1E90`, `003F74F0`, `003F7610` and `00555A70` share it): `rdx`'s 0x40-byte record is copied verbatim into `rcx`, then `{+0x30, +0x34, +0x38}` are overwritten with `rdx`'s floats plus `r8`'s `{0, 4, 8}` floats — a position-offset rebase for the packet record.

Interior anchor `0020313E` (function `002030E0`).

`00438860` (20603 B) is the larger `004355D0` composition path: `[rdx+0x48]` and the `1.0f - [rdx+0x1EC]` fade load first, the four `02AEECB0`/`ECC0`/`ECD0`/`ECE0` matrix rows land in xmm9-xmm12, then a 239-call `0020E600`-driven record walk through `00431D30` x54, `00521450`/`003AFDD0`/`0039A150` x18, `0039B960`/`0039B880` x12 and the `0039xxxx`/`0043xxxx` helpers - the composer's full element emit, the path the unclassified ledger paired against `00437130`.

Interior anchor `0043AE84` (function `00438860`).

`00437130` (5930 B) is the second `004355D0` path: `word[rsi+0x14]`/`+0x16` index the `02AEED50` table at `0x10` stride, then a 77-call `0020E600` walk with `0039B960` x12, `00397910`/`0039AF70`/`00432300`/`0043E840`/`0039B840`/`0039B860` and the `0043xxxx` local arms - the index-table composer where `00438860` carries the fade and matrix rows inline.

Interior anchor `00437CC9` (function `00437130`).

`002D0A20` (2553 B) is the call-free extent compute `002D3BA0` runs on the `+0xD0` record: `word[+0x100]`/`+0xF0`, `byte[+0xED]`, `word[+0x9C]`/`+0xF2` fields folded through `idiv` extents and `cmovl` clamps - the field arithmetic the `005713C0`/`00570CE0` extent formulas quote before the `002D3BA0` pitch passes.

Interior anchor `002D0F24` (function `002D0A20`).

`0043E840` (370 B) is the `022D8F90` state-block snapshot the composer paths run: `[r8]` stages to `022D8FA0`, `0xFFFFFFFFBF000000` writes into `022D8FB0` and half-unpacks to `022D8FB4`/`B8`/`BC`, `rcx`'s pair shifts into `022D8FBC`, and vector copies land at `022D92F0`/`022D9308` - a call-free publish of the workbench header.

Interior anchor `0043E8FF` (function `0043E840`).

`00432CC0` (1519 B) is the keyed byte expander `004355D0`/`00437130`/`00438860` share: `word[r9]` keys the `022D8F10` table, `x16 + r8d` stages the record into `022D8FB0`, `[rcx]`'s index and `022D8F10`'s block combine at `022D8FD0`/`022D8FE0`, then the `022D8F10` quadword is `psrldq`-unpacked byte-by-byte into `022D8F91`-`022D8F9B` - the composer-side form of `004332B0`'s expansion.

Interior anchor `00432FAF` (function `00432CC0`).

`0039F4B0` (720 B) is the slot-array element build the three composition paths share: `word[02F8F2C6]` x `0x28` selects the `02F8F2F8` slot, the slot is zeroed, `0020E680` allocates into `[slot+0x18]`, `+4`/`+0x14`/`+0x24` params feed the `0024E460`/`003A3D20`/`003A2C70`/`008642A0`/`0039CDC0` ladder, and `0020E670` tails out - the heavier of the two slot builds.

Interior anchor `0039F571` (function `0039F4B0`).

`0039F2B0` (506 B) is the shared-divisor vector build: `0020E680` allocates, `008642A0(3)` shapes, `0039CDC0` binds, then each `[rdi]` component divides by the common `[rsi]` scalar into the `+8`-chained output before `0020E630` frees - the normalize-by-extent helper.

Interior anchor `0039F2F8` (function `0039F2B0`).

`0039E820` (587 B) is the sibling slot-array build: the same `02F8F2C6` x `0x28` / `02F8F2F8` slot shape as `0039F4B0` with the same `0020E680` alloc and param block, but a different fill path through `0039E8E3`/`0039EA47` local arms and a `+4` vs `+0x14` ordering compare; `0020E670` tails out identically.

Interior anchor `0039E8E3` (function `0039E820`).

`0039E6B0` (360 B) is the byte-channel vector converter: `0020E680` allocates, `008642A0(3)` shapes, `0039CDC0` binds, then `movzx byte[rsi]` lanes `cvtdq2ps` into the `[rdi+0x10]` vector before `0020E630` frees - the colour/UV byte-quad unpack.

Interior anchor `0039E6EE` (function `0039E6B0`).

`0039B840` (25 B) is the 3-count specialization entry: forces `r9d = 3` and tail-calls `0039B880`, which the composers also reach through `0039B860`.

Interior anchor `0039B84F` (function `0039B840`).

`0039B880` (223 B) is the transform kernel behind `0039B840`/`0039B860`: `[r8]`-indexed `022D8F10` fetches stage into `022D8F90`/`A0`/`B0`, `022D9300`-`022D9320` publish, and the `(sum) x scale` pairs write into `[rdx]` at +8 stride - a call-free scaled-pair scatter.

Interior anchor `0039B8E8` (function `0039B880`).

`00396F20` (161 B) is the index scatter the composers run: `word[rdx]` keys `x16 + r11` records staged into `022D8F90`/`A0`/`B0`/`94A0`, `r9d` counts down while `[rdx]` qwords write into `[rax-8]` slots - a call-free indexed copy.

Interior anchor `00396F70` (function `00396F20`).

`00394B70` (550 B) is the unrolled index-list accumulate: `r9d` groups of four read `word[rdi]` indices into `+rcx*8` record pairs, `cvtdq2ps` against the `008F30EC`/`008C5B30` scale constants, `subss` the `00D113E0`/`00D113E4` minimums, and `addss` into the out vector - the weight scatter under the composers' vertex lists.

Interior anchor `00394C8D` (function `00394B70`).

`0043DB90` (999 B) is the four-call helper `00438860` runs inside its record walk: `r10 = 4` bounds the pair loop (`rcx < r10` twice), `0020E680`, `008642A0`, `0039CDC0` and `0020E670` do the field math - the composer's bounded inner step.

Interior anchor `0043DBD7` (function `0043DB90`).

`0043E440` (874 B) is the record-walk helper `00438860` calls beside `0043DB90`: `0020E680` and `0024E460` prepare, `003A3D20`, `003A2C70`, `008642A0` and `0039CDC0` run the field math under the cookie check - the composer's second bounded inner step.

Interior anchor `0043E4F8` (function `0043E440`).

`002C84E0` (829 B) is the tail of the channel-evaluation chain `002C7B10` calls, gated on `byte[rcx+0x29]` exactly as the table records: `002708B0`, `002E9CA0`, `003F0040`, `002C6DC0`, workbench `00202C90` x2/`00202B10`, then `0035D460` x4 for the `[0209AC30]+0x338` context fetch, `00271140` decode and `003F1290` append - the chain's gated closing stage.

Interior anchor `002C8598` (function `002C84E0`).

`001B0CE0` (685 B) is the pair registrar `001813F0` calls: absent `+0x2108`/`+0x2110` -> `001B1440` lookup, ordered-map scan on the `+0x2208` tree (`+0x20` keys, `+0x28` values), `006B5C60` and `001FB720` resolve, then `+0x3928`-indexed 0x58-stride slot match at `+0x2328`/`+0x2330` with `+0x2350==1` occupancy - the workbench's 64-slot pair table.

Interior anchor `001B0D32` (function `001B0CE0`).

`0043D8F0` (661 B) is the channel converter `00438860` calls (the authored-number family's `0039DAD0` is its twin): `0020E680` resolves the table, `008642A0`/`0039CDC0` build the output object, then the loop `cvtdq2ps`-converts packed bytes at `rdx - 2` onward into the `[rsi + 0x10]`-indexed float lanes - the family's byte-channel-to-float expander.

Interior anchor `0043D913` (function `0043D8F0`).

`00435050` (610 B) is the index-table arm `004355D0` runs: `word[+0x14]`/`+0x16`/`+0x18` compute the `02AEED50 + (edi<<5) + (r14<<4) + rbp*24` record, `00434C50` takes `rdx & 7`, the `02AEECB0`/`ECC0`/`ECD0`/`ECE0` identity rows stage on-stack, `003977B0`/`0039B550` compose, `byte[r15+0x1F1] & 8` picks the tail arm - the composer's tabled emit.

Interior anchor `004350EB` (function `00435050`).

`00434C50` (125 B) is the four-arm row select `00435050` (the tabled emit) and `00434CD0`/`0044F4C0`/`00454480` call: `edx` decrements 1/2/3 pick `00434A70`, `00434900`, or the `02AEEC70`/`02AEEC30` globals, and every arm tail-jumps `00398030(table, rbx)` - the composer's matrix-row chooser.

Interior anchor `00434C6D` (function `00434C50`).

`00368010` (559 B) is the slot pass `00368360` calls: `rdx == 0` outs, else per iteration `00246480(rbx)` fills `[rsp+0x28]`, `022CBE32 & 0x20` + `esi == 0` gate a `00203170` pair that negates `word[+0x2C]`/`+0x2E` into 0.5-scaled floats, and `00202B70`/`00246450`/`00397910`/`003985B0`/`00398910`/`00398C50`/`00808C40` compose - the workbench's flag-gated transform step.

Interior anchor `00368078` (function `00368010`).

`00398DD0` (442 B) is the call-free triple-angle evaluator `00398480` calls: `[rcx]`/`+4`/`+8` divide by `01CEBC78`, each `* 00D10820` `cvttss2si` `& 0x7FFF` indexes the `01F004E0` LUT (with the `00D10828` twin for the phase terms), and the products combine - the primitive's three-component table evaluation.

Interior anchor `00398E21` (function `00398DD0`).

`00336210` (370 B) is the apply `00336E40` calls: `r8` null or `[r8 + 0x10]` null returns 1; otherwise `00265090` resolves the record, `003357B0` x3 steps the transform, `0033D3E0`/`00391410`/`00384130` commit and `00336390` finishes - the workbench's guarded transform apply.

Interior anchor `00336261` (function `00336210`).

`002708E0` (304 B) is the vector arm `00270590` calls: `00203080`/`00202DE0` build the `rsp+0x30` basis block, the `rbx`.`rdi` dot product (three mulss/addss pairs) feeds `00202D20`, and the result scales back through `rbx` and `rbx+0xC` into xmm2-xmm5 - the workbench's per-record orientation compose the settings-table arm shares.

Interior anchor `00270961` (function `002708E0`).

`00272590` (295 B) is the tagged-block emit `00404230` runs on `02EBEFC0`'s slot state: `dword[02EBEFF0]` selects the `*24` slot and `[r14+rbp*8+8]`'s record gets `00276430` applied at `+0x10`; the stream takes `0x10000000` tags, a `(len-0x10)&~7 | 0x6C008 << 0xC` count field, `02EBB7AC`'s `0xA0000007` tag at `>>3`, and `0x11000000`/`0x13000000` markers before `0016D6A0` + `003A1DB0` submit - the submit family's second emitter beside `00501610`.

Interior anchor `00272683` (function `00272590`).

`00276430` (514 B) is the `0209AB90` quad-workbench fill `00272590` runs: `byte[+0x90..0x93] x sword[+0x5A]` and `byte[+0x93] x sword[+0x58]` (each `>> 7`) build the modulated RGBA stored at `dword[+0x94]`; `00203170` initialises the workbench, then the rect publishes - `0209AB90`/`0209ABA4` take `xmm4`, `0209ABC0`/`0209ABC4` take `45000000 - 0x200/0x1C0 halved + edi/ebx`, `0209A760`/`0209A764` take the stack pair; `[rsi]` and `[rsi+0x14] x 3DB851EC` write `0209ABF4`/`0209ABF8`, `byte[+0x94..0x97] x 3FE38E39` write `0209ABE0..0209ABEC`, `[rax+0..0xC]` copies into `0209ABD0..0209ABDC`, and `xmm4 x 41800000/41000000` lands at `0209ABF0` - the centred 512x448 quad state the record's draw consumes.

Interior anchor `002764A5` (function `00276430`).

`003F74F0` (281 B) is the apply leg `003F7610` drives per pose element: `00203170` initialises the stack transform, `00270720(rdi, rbx+0x2A0)` composes it, `dword[rbx+0x2E4]` sign-flips when the flag arg is set, and `00202F70` scales the xmm6/xmm7 pair into the block; `003588B0([rbx+0x2D0])` resolves the factor record for `002645D0` (1.0f on a miss), multiplied by `3FA66666` or `3F99999A` per the flag; `00202D70(rdi, rdi, &stack)` applies and `002030E0(rdi, rdi, rbx+0x280)` commits - the scaled-orientation write under the composer.

Interior anchor `003F7573` (function `003F74F0`).

`00276430` (514 B) is the `0209AB90` quad-workbench fill `00272590` runs: `byte[+0x90..0x93] x sword[+0x5A]` and `byte[+0x93] x sword[+0x58]` (each `>> 7`) build the modulated RGBA stored at `dword[+0x94]`; `00203170` initialises the workbench, then the rect publishes - `0209AB90`/`0209ABA4` take `xmm4`, `0209ABC0`/`0209ABC4` take `45000000 - 0x200/0x1C0 halved + edi/ebx`, `0209A760`/`0209A764` take the stack pair; `[rsi]` and `[rsi+0x14] x 3DB851EC` write `0209ABF4`/`0209ABF8`, `byte[+0x94..0x97] x 3FE38E39` write `0209ABE0..0209ABEC`, `[rax+0..0xC]` copies into `0209ABD0..0209ABDC`, and `xmm4 x 41800000/41000000` lands at `0209ABF0` - the centred 512x448 quad state the record's draw consumes.

Interior anchor `002764A5` (function `00276430`).

`003F74F0` (281 B) is the apply leg `003F7610` drives per pose element: `00203170` initialises the stack transform, `00270720(rdi, rbx+0x2A0)` composes it, `dword[rbx+0x2E4]` sign-flips when the flag arg is set, and `00202F70` scales the xmm6/xmm7 pair into the block; `003588B0([rbx+0x2D0])` resolves the factor record for `002645D0` (1.0f on a miss), multiplied by `3FA66666` or `3F99999A` per the flag; `00202D70(rdi, rdi, &stack)` applies and `002030E0(rdi, rdi, rbx+0x280)` commits - the scaled-orientation write under the composer.

Interior anchor `003F7573` (function `003F74F0`).

`002645D0` (55 B) is the scale source-select the pose legs `003F74F0`/`003F7610`/`003F7BC0`/`00272F30` consult: `byte[rcx+3] >> 5` minus one picks the float - selector 1 returns `[qword[+0xB8] + 0x70]`, selector 3 returns `[qword[+0xB8] + 0xFC]`, anything else returns `1.0f` (`01CEBBA8`) - the per-class factor fetch `003F74F0` runs on the record `003588B0` resolves.

Interior anchor `002645EA` (function `002645D0`).

`0039C800` (1197 B) is the quad/vertex emitter the operand stager `00502160` feeds through `[rdi+0x50]`: after `0039B550` opens the `02AEECB0` scratch it loops `dword[rbx+0x58]` entries in three materializations - indexed mode (`[rbx+0x28]` live) runs two `00399B80` 2-word decodes off the `rdi`/`rsi` `0x10`-stride arrays plus two `0039B780` packs off the `r14`/`r15` `8`-stride index rows, then `0039FD20` or `003A0370` (picked by `dword[02AEE900]`) on `[rbx+0x18]`/`[rbx+0x50]`; vertex mode (`[rbx+0x20]` live) refreshes the stack float4 from `+0x38..+0x44` whenever `r15d == dword[+0x5C]`, runs the same two decodes plus one `0039B780` into the staged vec, picks `003A0040`/`003A05F0` by `02AEE900`, then adds `[rbx+0x48]` into the first two lanes and `[rbx+0x4C]` into the second two when each is nonzero; the bare mode repeats the indexed decode pair with `0039FD20`/`003A0370` - the painter that turns the staged stream into emitted primitives.

Interior anchor `0039C83C` (function `0039C800`).

`00276320` (265 B) is the GS packet emitter `00274CB0` runs per `02EBEFF0`-indexed `x3` slot of `02EBEFC0`: into `[slot->+8]` it writes the tag ladder `+0x30 = 0x5C`, `+0x40 = 0x44`, `+0x48 = 0x42`, then at `+0x10` the sub-record `+0x50 = 1`, `+0x58 = 0x1A`, `+0x18 = 0xE`, the running pointer advanced `0x50` and back-computed into `+0x10 = 0x1000000000008000 | ((end-start-0x10) >> 4)`, `+0` = 0, `+4 = 0x13000000`, `+8 = 0x10000000`, `+0xC = 0x50000000 | ((end-base-0x10) >> 4)`, `+8 = 0x11000000`, `+0xC = 0x10000000` before `0016D6A0` registers the span; a nonempty tail (`ebx != edi`) adds the `& ~0xF` remainder into `dword[slot+8]` and calls `003A1DB0` - the DMA-tag-shaped block writer the workbench's packet channel drives.

Interior anchor `002763FC` (function `00276320`).

`003A0040` (814 B) is the slot-record emit `0039C800` runs when `02AEE900` selects it: `word[02F8F2C6]` `x 5` `x 8` indexes a `0x28` slot of `02F8F2F8` written `{+0 = 0, +8 = min(+4, +0x14, +0x24, +0x34) of rsi, +0xB |= byte[02AEE910] << 4, +0xC = 1, +0x10 = 0, +0x18 = 0020E680()}`; `0024E460`/`003A3D20` gates force code 2 and `003A2C70` finishes - the indexed-record arm of the emit pair.

Interior anchor `003A0080` (function `003A0040`).

`003A0370` (637 B) is the divide-normalize emit `0039C800` picks via `02AEE900`: `0020E680` + `008642A0(4)` stage the output record and `0039CDC0` opens it, then a `divss` ladder writes `dst = src / scale` lanes (`+0`/`+4`, `+0x10`/`+0x14`, `+0x20`/`+0x24`, ...) into `[r14+8]`'s buffer - the coordinate-normalizing arm of the pair.

Interior anchor `003A0394` (function `003A0370`).

`003A05F0` (626 B) is the twin of `003A0370` - the same `0020E680`/`008642A0(4)`/`0039CDC0` stage and `src / scale` `divss` ladder into `[r14+8]`, differing in which lanes take the divide - the second normalizing arm `02AEE900` selects.

Interior anchor `003A0614` (function `003A05F0`).

`00217790` (236 B) is the in-place three-column rotate `00202E90` runs: `(xmm1, xmm2)` = `(cos, sin)` applies `x' = y*s - x*c`-style pairing per column pair - `+4`/`+8`, `+0x14`/`+0x18`, `+0x24`/`+0x28` and `+0x34`/`+0x38` each take `mulss`/`subss`/`addss` against the two angles and store back - a call-free planar rotate over the transform's basis pairs.

Interior anchor `002177B6` (function `00217790`).

`00335B60` (748 B) is the clamped interpolation submit the locomotion callers share: `ucomiss` rejects a zero `xmm3` divisor, `[rbp+0x40]` clamps through `minss`/`maxss` into `xmm8`, `00861F08` divides `xmm7` by `xmm6` when nonzero, and a battery of `00202xxx`/`00203xxx` matrix builders composes the working transform across `rsp+0x30`..`+0x70`, scaled by the `[rbx+0x108]+0x110` members and submitted through `003357B0` with the `+0xE0`/`+0xF0` context - returns 0/1/2 by which validation arm `00318CA0`/`0033D3E0`/`00391410`/`0032A6A0` answered.

Interior anchor `00335D37` (function `00335B60`).

`00244A20` (943 B) is the gated component scale/snap arm of the transform pair: when `[rsi+0x7C]` carries bits 0x30 it takes a component selector (`([+0x7C]>>7)&7` if bit 0x40 is set, else the child record's `[rdi]` byte) and on selector 1 converts the i16 extent quad at `[rbx+8..0xE]` through the `(x - x*scale*0.5)` half-pixel formula into integer pairs fed by `xmm6 = [rsi+0x78]` and the 0.5 constant `01CEBB70`, writing the scaled floats to `[rbx+0x10/0x14/0x18]` or folding into `[rbx+0x20]`; a nonzero `[rdi+0x10]` float then nudges `[rbx+0x18]` by `(1.0 - scale)` scaled by the `01CEBC50` constant, and the `+0x80` flag byte's bit-3/nibble lane copies `[rsi+0x84]` into exactly one of `+0x10`/`+0x14`/`+0x18`.

Interior anchor `00244B0A` (function `00244A20`).

`0039D480` (230 B) is the matrix-publish `0024C060` runs on the `02AEEAA0` work block: it copies the caller's four `0x10` rows into `02AEEAA0`..`02AEEAD0`, rebuilds a stack copy with a zero `+0x30` row, runs `0039AF70` then `00398F90` for a float pair that `00861F02` reduces to a scalar, and finishes with `00250010` + `00398910` on `02AEEAE0` - the decomposed-rotation publish sibling of the transform primitives

Interior anchor `0039D50D` (function `0039D480`).

`00367820` (200 B) is the tracked-pair handshake `00368360` calls: a live foreign `022CBE68` (non-null, != rcx) clears `022CBE32` bit 7 and returns 1; phase byte `022CBE87` in {2,3} also returns 1; otherwise it compares `[rdx+8]/[+0xA]` against the saved `022CBE4C`/`022CBE4E` words and `[rdx]/[+2]` against `022CBE50`/`022CBE52`, and when `[rdx+0xC] & 0x100` is set it either snapshots `4C/4E` back (when `022CBE30 == 2`) or `00368940`s and stores `50/52` from `[rbx]`

Interior anchor `00367869` (function `00367820`).

`00519880` (408 B) is the 3x3 row-major matrix multiply the `0x290`-record fan-in (`0051A280`) calls on each element's `+0x230`/`+0x240`/`+0x250` rows: `out[r][c] = A[r][0]*B[0][c] + A[r][1]*B[1][c] + A[r][2]*B[2][c]` for `r,c` in 0..2, all `mulss`/`addss`, rows at `+0x00`/`+0x10`/`+0x20` - the same row-major layout `022D91B0` uses, applied per-element to the oscillator's transform records.

Interior anchor `005198A7` (function `00519880`).

`001E5080` (460 B) is a transform-list sweep `001A7A10` runs: it validates the `[[rcx+0x18]]` header (`dword[+0x70]` must be <= 0x7FFFFFFF, `+0x5C` bit 6 clear) and every element of the `[rsi+0x18]`..`[+0x20]` list (`+0x5C` bit 1 clear), sign-flips all eight floats of `r9`'s pair record with the `01CEBDA0` sign mask into a stack copy, then per element applies `00189120`/`001854C0` and tests `001E4B80` - the negate-then-apply walk the transform primitives share.

Interior anchor `001E51E3` (function `001E5080`).
