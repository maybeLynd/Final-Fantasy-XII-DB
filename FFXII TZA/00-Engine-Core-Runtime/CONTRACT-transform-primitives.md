---
contract: put a point through the workbench matrix, or compose two transforms, and leave in the four shared workbench slots exactly what the engine's other readers expect to find there
category: 00-Engine-Core-Runtime
scope: family            # two leaf primitives of ONE workbench, reimplemented together because they share its matrix convention and its deposit slots (sections 4-5); not `operation` (they are two), not `subsystem` (no ordering across them, section 7). The sibling CONTRACT-transform-workbench-save-restore.md carries the same value for the same pair-of-primitives reason. Chosen 2026-09-17 (FABLE) on OPUS-REQ-FABLE-CONTRACT-TRANSFORM-PRIMITIVES-FRONTMATTER; keys renamed to the template's vocabulary (title/subsystem/formalises/status -> contract/category/implements/readiness), content untouched.
level: L1                # L2 needs runtime evidence (RECONSTRUCTION-READINESS-GATE section 1); section 13 records none - the differential test runs the ISOLATED original code under Unicorn
readiness: DIFFERENTIAL TESTED   # reconstruction axis: diff_transform.py re-run 2026-09-13 (FABLE), 123 point + 123 compose cases, 0 mismatches; original axis: NOT runtime validated (section 13) - KNOWLEDGE-SCHEMA 5a rule 1
confidence: PROVEN       # rates the two laws: exact over 123 + 123 differential cases and 350 predictions, 0 mismatches. What the matrix IS and who reads the deposits stay UNRESOLVED (section 14) and are not what this key rates
implements: Shared-Transform-Workbench/the-two-transform-primitives.md
entries: ["00398F90", "00397910"]
evidence_class: isolated original-code
last_reviewed: 2026-09-17
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 22 addresses cited - 12 data,
    6 entry, 4 interior, every one resolving into a known section of the authority image.
    This document had no verified_against block at all; the line records a check performed
    on that date and is not a reconstruction of the original derivation, for which see
    section 13 and `audit.last_pass_state`.
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-transform-primitives-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# CONTRACT — the workbench's two transform primitives

**Formalises** [the two transform primitives](Shared-Transform-Workbench/the-two-transform-primitives.md).
That page did the work; this contract states it in the form a reimplementer and the parity machinery
can both read. Nothing here is new analysis, and where the page refuses a claim this contract refuses
it too.

## 1. Purpose

Two leaf functions that every transform in the game passes through: one puts a point through the
workbench matrix, the other composes two transforms. Between them they have **156 non-EH callers**.
They compute, they deposit into shared scratch, and they call nothing.

## 2. Interface

| | |
|---|---|
| `00398F90` | `TransformPointByWorkbenchMatrix(const float in[4] /*rcx*/, float out[4] /*rdx*/)` (377 B) — no return |
| `00397910` | `ComposeTransforms(const Mat4 *a /*rcx*/, const Mat4 *b /*rdx*/, Mat4 *out /*r8*/)` (567 B) — no return |
| calling convention | Microsoft x64 |
| callees | **none from the point transform** — a true leaf. `00397910` reaches `__security_check_cookie` only |

## 3. Types

`Mat4` is four 16-byte rows, 64 bytes total, **row-major with the translation in row 3**. A point is
four floats; the fourth is read and discarded (§4).

## 4. The two laws, and they are exact

**The point transform** is a row-vector × matrix product:

```text
out[c] = in.x * M[0][c] + in.y * M[1][c] + in.z * M[2][c] + 1.0 * M[3][c]
```

where `M[r]` is the 16-byte block at `022D91B0 + r*0x10`.

**The composer multiplies in the reverse of the obvious order:**

```text
out = b × a          (NOT a × b),    out[i][j] = Σₖ b[i][k] · a[k][j]
```

**Preconditions.** None. Neither validates anything; both address fixed globals for the matrix and
take their buffers from the caller.

**Postconditions.**

- The point transform writes `out` **and four deposits** (§5).
- The composer writes **exactly 64 bytes** to `out` and nothing else.

**Invariants.**

1. **The point's own `w` is ignored and replaced by a LIVE LOAD from `01EF93FC`** — the `w`
   lane of the software `vf00` image at `01EF93F0`, **which is `.data`, not a constant**. Every
   shipped writer sets it to `1.0f`, so the transform's law is `… + 1.0*M[3][c]` in the
   shipped image; the mechanism is a load, and §15b says what that does and does not license.
   `in[3]` is loaded and never used. **So this transforms a POSITION and can never express a direction**, which
   would need `w = 0`.
2. **There is no perspective divide.** All four components are emitted and nothing is divided.
3. **Aliasing is safe on the composer.** Both inputs are staged to the stack frame (`[rsp+0x40]` and
   `[rsp+0x80]`) before any multiply, so `out == a` and `out == b` give the same answer as three
   distinct buffers.

## 5. State — the deposits are not a side effect to drop

| address | what lands there | width |
|---|---|---:|
| `022D9300` | the **input** point, copied verbatim | 16 B |
| `022D91A0` | the running accumulator — **without the translation row** | 16 B |
| `022D9310` | the result | 16 B |
| `022D8F90` | the result again | 16 B |
| `[rdx]` | the result, for the caller | 16 B |

**The result goes to three places and the input to one.** A reconstruction that filled only `out`
would compile, satisfy any test of its output, and silently starve every consumer that reads the
workbench rather than the caller's buffer.

**The accumulator holds the sum WITHOUT the translation row**, which is the opposite of the obvious
reading:

```text
022D91A0[c] = x*M[0][c] + y*M[1][c] + z*M[2][c]      (no translation)
022D9310[c] = 022D91A0[c] + M[3][c]                   (the result)
```

**All four deposit slots are SHARED, not owned here.** `022D91A0` has 67 writers image-wide,
`022D9300` has 41 writers and 63 readers, `022D8F90` has 47 and 59. That these two functions write
them is proven; **who consumes them is not**.

## 6. Relationships

The getter `003970A0` (`BQ-16`) loads the same four 16-byte blocks at `022D91B0` as one 64-byte
block. This contract reaches those blocks **from the other end** — as the multipliers of `x`, `y`, `z`
and `1` — which fixes the convention without settling what the matrix *is*.

## 7. State transitions

**None.** Neither function has a state machine: each is called, computes, writes, and returns. The
only ordering that exists is the caller's.

## 8. Script · resource · event interactions

**None.** No script opcode reaches either directly, neither touches a resource, and neither raises
an event. They are arithmetic the rest of the engine calls.

## 9. Determinism

Fully deterministic. No RNG, no timing, no synchronisation, no allocation. Both are pure arithmetic
over their inputs plus the global matrix.

## 10. Failure paths and edge conditions

**There are none inside either function.** Neither validates, refuses, or returns an error. The edges
that matter belong to a reimplementer:

1. Writing the composer the natural way round (`a × b`) produces a completely different matrix, and
   every transform built from it is wrong **in a way that still looks like a transform**.
2. Multiplying in place without staging corrupts the input halfway through and passes every test
   using separate buffers.
3. Depositing the *finished* value at `022D91A0` instead of the pre-translation sum.

## 11. Observable behaviour

In memory: after a point transform, the input at `022D9300`, the pre-translation sum at `022D91A0`,
and the result at `022D9310`, `022D8F90` and the caller's buffer. After a compose, 64 bytes at the
destination and the 16 bytes behind it untouched.

## 12. Reproduction formula

```
M[r]   = 022D91B0 + r*0x10
point(in, out):
    accum[c] = in.x*M[0][c] + in.y*M[1][c] + in.z*M[2][c]
    store accum -> 022D91A0
    store in    -> 022D9300
    res[c]      = accum[c] + M[3][c]
    store res   -> 022D9310, 022D8F90, out
compose(a, b, out):
    stage a and b to locals FIRST
    out[i][j] = Σₖ b[i][k] * a[k][j]        /* b × a */
```

## 13. Runtime validation

**Evidence class: isolated original-code. The two laws have NOT been observed in the running game.**

**What was executed.** Both bodies run at their real virtual addresses under Unicorn against
[`Reconstruction/Game/Math/transform.c`](../../../Reconstruction/Game/Math/transform.c), driven by
[`diff_transform.py`](../../../Reconstruction/Tests/Differential/diff_transform.py).

| | |
|---|---|
| point cases | **123** — 3 designed, 120 randomised |
| compared per point case | **five buffers** — the caller's `out` and all four deposits |
| compose cases | **123**, across **3 aliasing modes** (`out` distinct, `out == a`, `out == b`) |
| mismatches | **0** |
| mutation score | **19 of 20** |

The laws were additionally established by *prediction*: 200 random matrix/point pairs for the point
transform and 150 for the composer, every one exact. A single mismatch would have killed either.

### What the live session did and did not see — 2026-09-08

A live read was taken at the **title screen** of the reference install, with the process verified
ticking first. It observed **the state of the globals, not these functions executing**:

| address | result |
|---|---|
| `022D8F90`, `022D91A0`, `022D9300` | **0 of 16 bytes moved** in 40 samples over four seconds |
| `022D91B0` (the matrix) | 2 of 64 bytes, transiently; **first row `[0,0,0,0]`** across 30 samples |

**So `00398F90` is not running at the title screen**, and the block is not being maintained there as
a live transform — a first row of zeros is degenerate and no working renderer holds one. That rules
out the reading in which this block is a *continuously maintained* world, view or projection matrix.
It is **bounded evidence**: a title screen need not render a 3D scene, so *idle here* is not *idle
always*. **The decisive in-world observation needs a loaded save and was not taken.**

Two blocks past the matrix *are* live — 16 bytes at `022D91F0` and 32 at `022D9210`, both new in all
30 samples, the second internally structured (its last four floats repeat the first four with the
first two exchanged). Their sizes and update rate are measured; **their meaning is not**.

**This section does not make the contract runtime-validated.** Nothing here observed either function
run.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**26 generated points: 14 KILLED · 2 SURVIVED · 5 EQUIVALENT · 0 NO_BUILD · 0 TIMEOUT · 5 INVALID. Verdict `FAIL_INCOMPLETE`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/transform` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

Both survivors are **kind C, undefined behaviour**: `c < 4` → `c < 5` writes a fifth lane of a `Vec4`, and `k < 4` → `k < 5` reads past a 4×4. The five `INVALID` cases are the same mutation elsewhere, and they are the driver's OWN guard firing — *“compose case 0 wrote past a buffer”* — so the suite noticed every one of them and the instrument still refuses to call that a kill, because no comparison happened.

## 14. Unresolved

1. ~~**What the matrix IS** — world, view, projection, or a current transform (`BI-9`).~~ **Answered
   2026-09-21 (SWE2-CONTRACT) at the static limit: a caller-installed current transform, and the
   sources are now enumerated.** §6 constrains
   the convention, not the meaning, and a projection matrix multiplies exactly the same way.
   A per-site producer census over all **116 unique call sites** (`af70_sources` receipts,
   `Tools/work/SWE2-CONTRACT/af70_sources.json`) resolves where `rcx` comes from at every one —
   see item 2 for the breakdown. The dominant shape settles the meaning: **the installed matrix is
   the caller's own object transform** — an element's matrix field installed verbatim
   (`[obj+0x10]`, a matrix *pointer* field, null-guarded, 48 sites; an embedded matrix at
   `obj+0x40`, 12 sites) or a stack local composed on the spot from it (38 sites). "World, view or
   projection" was indeed the wrong trichotomy — the slot is the workbench's current-matrix
   register, and in the dominant case it holds *this element's* transform for the duration of its
   point run.
   > *BI-9 answered 2026-09-12 (FABLE), CORRECTED 2026-09-13 (FABLE) and revised here by OPUS.*
   > **The slot is fed by ONE fixed matrix and ONE that varies, and the earlier note had them the
   > same.** `0039B550` installs `02AEECB0` (the projection×viewport) **at all 82 of its unique
   > sites** — that half stands. `0039AF70` installs **whatever `rcx` points at**, over 116 unique
   > sites: **11 globals** (`02AEEA20` ×9, `02AEEBF0` ×2), **38 stack locals** (at least 19 of them
   > composed on the spot by `00397910`), and **67 register- or object-derived**. `0024C060` writes
   > the two globals. See the two-primitives page §7 and the 2026-09-13 correction block.
   >
   > **Why the revision matters more than the numbers:** the old note specified a FIXED-SOURCE
   > installer, and a reimplementation reading this contract would have hard-wired `02AEEA20` into
   > `0039AF70`. It would then be correct at 9 sites out of 116 and silently wrong at the rest.
   >
   > **Verified before accepting, at a single site.** `004357EF lea rcx, [rbp + 0x10]` then
   > `004357F3 call 0039AF70` installs a STACK LOCAL — one composed four instructions earlier by
   > `004357BC lea rcx, [02AEEBF0]` / `004357C3 call 00397910`, so it is neither `02AEEA20` nor even
   > a global. One counter-example is all an **always** claim needs, and this contract carried one.
2. ~~**Who writes the matrix**, beyond the setter `0039AF70` that `BQ-16` names — now a larger question than it was, since `0039AF70`'s source is a caller's pointer rather than a known global, so "who writes the matrix" is partly "who builds the 105 non-global sources".~~ **Answered
   2026-09-21 (SWE2-CONTRACT) — the 105 non-global sources enumerated by producer.** Tracing the
   last `rcx` writer before each of the 116 sites, then who wrote that:

   | source shape | sites | producer |
   |---|---|---|
   | `mov rcx, [obj+0x10]` | **48** | the caller's object — a **matrix-pointer field** (null-guarded `test rcx,rcx; je`), e.g. `003D951B`, `00462204` |
   | embedded matrix at `obj+0x40` | **12** | `lea rcx,[rdi+0x40]` ×8 on the object itself; `mov rcx,[obj+0x10]` then `+0x40` ×4 — the **second** 4×4 inside the pointed block (`00462219`) |
   | stack local, composed | **19** | `ComposeTransforms 00397910` wrote the local through `r8` earlier in the window (e.g. `004355D0`: `02AEEBF0` × element matrix) |
   | stack local, inline | **13** | `movups`/`movaps` row copies of an input matrix — `0039D480` copies `*rcx` rows 0–2 into `[rsp+0x40]` and forces row 3 to `[0,0,0,1]` from `008C5FD0` |
   | stack local, out-param | **6** | written through an output pointer (`rdx`) by a workbench matrix op — `00397ED0` (the vec4-by-4×4 transform loop; `00442AD5`/`00442AE2` feed it `rcx+0x40` and `02AEEA20` into `[rbp-0x19]`), `00398480` (`0044A7EE`, `0044A95E`, `0044AADE`, `004647CA` — the three `0044A620` sites then run `00397ED0` on it before install), `00398A90` (`0050368A`) |
   | regcopy / misc | **~7** | mostly more object fields — `[rcx+0x100]` ×2 (`0052F5D2`, `0052F62A`), `[rbx+0x10]` via `rax` ×1, one frame arg `[rbp+8]` at `002F2EF4` (a matrix pointer handed in by *its* caller), one `[rsp+0x30]` local; two mis-traces (`xor rax,rsp` cookie, a `rdi`/`rcx` swap) left unclassified |
   | globals | **11** | `02AEEA20` ×9, `02AEEBF0` ×2 — written by `0024C060` per the 2026-09-13 block |

   So "who builds the sources" is: **the caller's own element/object** (its `+0x10` matrix pointer,
   its `+0x40` embedded matrix, or a matrix-pointer at `+0x100`), or a **fresh composition** — the
   composer's `b×a` or `00397ED0`'s row-transform — staged into a stack frame. Nothing in the 105
   is built by a shared builder; each call site produces or points at its own.
3. ~~**Whether the deposits are read by anyone**, given that all four slots are shared.~~ **Answered
   2026-09-21 (SWE2-CONTRACT): yes — pervasively, but by the workbench family, not by the callers.**
   The four slots are named registers under
   [the EE and VU0 register bank](Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md):
   `022D91A0` = VU0 **ACC**, `022D9300` = **vf22**, `022D9310` = **vf23**, `022D8F90` = EE **$t0**.
   A per-instruction census over all 35,754 `.pdata` bodies — rip-relative operands, 16-byte span,
   read/write split by operand position — counts ACC **356 reads / 47 reader fns** (535 writes / 84),
   vf22 **160 / 47** (244 / 63), vf23 **88 / 31** (223 / 48), `$t0` **446 / 44** (863 / 60). The
   readers are the translated-VU0 routine family consuming the register convention: e.g. `00394E50`
   reads vf22's components as broadcast scalars (`movss xmm2,[022D9304]`; `mulss`) while
   accumulating rows into ACC. **The deposits are not a side channel — they are the VU0 calling
   convention**: the primitive leaves its result where subsequent VU0 code expects it.
4. ~~**What the other callers do with the result.** 156 call sites counted, **none read**.~~
   **Verified 2026-09-21 (SWE2-CONTRACT).** An E8/E9 rel32 census finds 102 sites / 81 caller fns
   for `00398F90` and 129 / 86 for `00397910` (137-fn union; the "156" figure does not reproduce
   and is marked accordingly). **Zero caller fns read the deposits as values.** Only two even touch
   vf22/vf23: `00434A70`'s reads follow its own writes (register staging, `movss` stores then
   `movups` reloads) and `00531094`'s reads precede its call entirely. The callers consume `out`;
   the deposits belong to the workbench's register convention, not to the call interface.
5. ~~**What the live blocks at `022D91F0` and `022D9210` are.**~~ **Answered in the corpus — layout
   since 2026-09-14, contents since the oscillator page.** They are not objects: `022D91F0` is
   **VU0 vector register 5** (`022D91A0` = ACC, one register per 16 bytes) and `022D9210`–
   `022D922F` are **vector registers 7–8** — [the EE and VU0 register
   bank](Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md), BQ-16's answer. The
   oscillating contents belong to whichever translated routine ran last; the routine family is
   identified: the per-model oscillator's walkers `0040DBB0` / `0040B780` write a second 4×4 from
   ~~`[sub-obj + 0x150]`–`+0x180`~~ the bone's `0x290` row `+0x150`–`+0x180` *(corrected 2026-10-01, OPUS - the oscillator page's GI-19 section)* straight into rows 5–8 (`022D91F0`–`022D9220`, `0040DE9E`–
   `0040DEEF`), node matrices through the VU0 bank — [the oscillator
   subsystem](../17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md)
   §5b. Residual: which routine holds them *at the title screen specifically* is not
   runtime-confirmed — a live-only check, not a static gap.
6. ~~**Whether `00397910` is only a matrix multiply.** Its 567 bytes were not read line by line; the
   law comes from prediction over 150 random pairs, which is evidence about behaviour on those
   inputs rather than a proof that no other path exists inside it.~~ **Answered 2026-09-20 by a
   full line-by-line read: yes.** The body's only control-flow edge is the four-iteration row
   loop's `jne 00397A10`; the only call is `__security_check_cookie` at `00397AFD`; the only
   global touched is the cookie at `01F44830`. Both inputs are staged on the stack before the
   first multiply — that staging is why `out == a` / `out == b` cannot corrupt a source. §15
   gains a row.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the point transform's law | `out[c] = x*M[0][c] + y*M[1][c] + z*M[2][c] + 1.0*M[3][c]`, used to PREDICT 200 random matrix/point pairs; all 200 exact, any one mismatch fatal | 1 (isolated original-code) | PROVEN |
| the point's `w` is ignored and replaced by `[01EF93FC]` | `in[3]` is loaded and never used; the `1.0f` is **loaded from the `.data` cell `01EF93FC` on every call**, not an immediate. `w = 7` and `w = -123` give byte-identical output | 1 (isolated original-code) | PROVEN |
| every shipped writer of that cell stores `1.0f` | three stores cover it — `0036D9A8`, `0036D9E8` (`movss` from the `.rdata` `1.0f` at `01CEBBA8`) and `0036DD87` (`movups` of `[0,0,0,1]` from `008C5FD0`); a range-aware sweep over `.text` finds no other | 1 (static, range-aware) | PROVEN |
| there is no perspective divide | all four components emitted, nothing divided — `00398F90` is `mulss`/`mulps`/`addss` throughout, zero divides in 377 B | 1 (isolated original-code) | PROVEN |
| the composer computes `b × a` | 150 random pairs predicted exactly, and the designed case separates the orders outright — observed `6610, 7020, 7430, 7840`, which is `b × a`; `a × b` gives `1210, 1220, 1230, 1240` | 1 (isolated original-code) | PROVEN |
| the composer is ONLY a matrix multiply — no other path exists in its 567 bytes | whole body read line by line 2026-09-20: the single control-flow edge is the row loop's `jne 00397A10` (4 iterations × 4 dot products), the single call is `__security_check_cookie` at `00397AFD`, and no global is touched except the cookie at `01F44830` | 1 (isolated original-code) | PROVEN |
| aliasing is safe on the composer | both inputs staged before any multiply — `a` at `00397977`–`0039799E` and `b` at `003979A7`–`003979DE`, first multiply at `00397A1F` — and `out == a` / `out == b` both match the distinct-buffer result. **§15a: the staged offsets are `[rsp+0x40]`–`+0x70` and `[rsp]`–`+0x30` in the current body; the row's `+0x80` does not appear** | 1 (isolated original-code) | PROVEN |
| the composer writes exactly 64 bytes | the 16 bytes after the destination were sentinel-filled and untouched in every run | 1 (isolated original-code) | PROVEN |
| the point transform makes four deposits | `022D9300`, `022D91A0`, `022D9310`, `022D8F90`, each compared byte for byte over 123 cases | 1 (isolated original-code) | PROVEN |
| the accumulator holds the sum WITHOUT the translation row | a reconstruction depositing the finished value there fails all 123 point cases on that buffer and no other | 1 (isolated original-code) | PROVEN |
| the four deposit slots are SHARED, not owned here | 67 writers at `022D91A0`; 41 writers / 63 readers at `022D9300`; 47 / 59 at `022D8F90`, counted across both reference instruments | 1 (static) | PROVEN  **§15a: the SUBSTANCE is confirmed and stronger; the NUMBERS do not reproduce.** Two independent instruments agree on functions referencing each slot's base — `022D91A0` **70**, `022D9300` **68**, `022D9310` **47**, `022D8F90` **64** — and none of `67 / 41 / 47` matches. Note `47` is exactly `022D9310`'s count, so the `022D8F90` figure looks mis-attributed. **Neither the unit (references or functions) nor the span (the base or the 16-byte slot) was recorded**, which is why the figures cannot be checked as written |
| the matrix at `022D91B0` is row-major with translation in row 3 | this contract reaches the four blocks as the multipliers of x, y, z and 1; `BQ-16`'s getter reaches the same four from the other end | 1 (isolated original-code) | PROVEN |
| the workbench deposit slots are idle at the TITLE SCREEN | 40 samples over four seconds, 0 of 16 bytes moved at each of three slots, against a control showing the surrounding region moved 91 bytes in the same window | 10 (live) | PROVEN, and bounded to that state |
| the deposits are read — by the workbench family, not the callers | per-instruction census over all 35,754 `.pdata` bodies (rip-relative operands, 16-byte span, operand-position split): ACC 356 reads/47 fns, vf22 160/47, vf23 88/31, `$t0` 446/44; reader example `00394E50` consumes vf22 components as broadcast scalars while accumulating into ACC — the deposits ARE the VU0 calling convention | 1 (static) | PROVEN |
| zero caller fns read the deposits as values | E8/E9 rel32 census: 102 sites/81 fns (`00398F90`) + 129/86 (`00397910`); of 137-union, only `00434A70`/`00531094` touch vf22/vf23 and only for their own staging, not the deposited values | 1 (static) | PROVEN |
| what the matrix is: the caller's current transform; and who builds the 105 non-global sources: the caller's own object or a fresh composition | per-site producer census over all 116 `0039AF70` call sites — 48 `[obj+0x10]` matrix-pointer loads (null-guarded), 12 embedded/`+0x40` matrices, 38 stack locals (19 composer-built, 13 inline `movups`, 6 out-param via `00397ED0`/`00398480`/`00398A90`), 11 globals, ~7 regcopies (more object fields); receipts `Tools/work/SWE2-CONTRACT/af70_sources.json` | 1 (static) | PROVEN |
| any runtime observation of either function EXECUTING | — | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### The sharing claim is right, and its numbers cannot be reproduced

Two instruments, run independently: the database's own `data_xref_scan.py`, and a per-function
capstone sweep of all 38,161 bodies that separates reads from writes **by operand position** and
counts the whole **16-byte** slot as well as the exact base — because a reference to `022D91A4` is a
reference to the `022D91A0` slot, and these are `movaps`/`movss` accesses that a detector keyed on
`mov` would miss.

| slot | `data_xref_scan.py` | my sweep, exact base | my sweep, 16-byte span | **the contract says** |
|---|---|---:|---:|---|
| `022D91A0` | 237 refs in **70** fn | **70** | 83 | 67 writers |
| `022D9300` | 236 refs in **68** fn | **68** | 69 | 41 writers / 63 readers |
| `022D9310` | 147 refs in **47** fn | **47** | 51 | — |
| `022D8F90` | 668 refs in **64** fn | **64** | 64 | 47 writers / 59 readers |

**The two instruments agree exactly on all four**, which is what makes the disagreement with the
document meaningful rather than a third opinion. The stated figures match none of them — and **`47`
is precisely `022D9310`'s count**, so the `022D8F90` row looks like a slot mix-up rather than a
counting error.

> **The claim itself is not in doubt, and the true numbers make it stronger.** Between 47 and 70
> distinct functions touch each of these slots, and `022D8F90` alone carries **668** references.
> *"Shared, not owned here"* is if anything understated.

**What cannot be checked is what was counted.** The row says "writers" and "readers" without
recording the **unit** — references or functions — or the **span** — the exact base or the 16-byte
slot. Those two choices move `022D91A0` between 70 and 83 and `022D9310` between 47 and 51. The
figures are marked as unreproduced rather than replaced, because a reader cannot tell which quantity
the original measured.

> **Replaced 2026-09-21 (SWE2-CONTRACT) with a defined instrument** — rip-relative memory operands
> inside `.pdata`-bounded bodies, 16-byte slot span, writes = the memory operand in destination
> position, `lea` counted apart; receipts `Database/Tools/work/SWE2-CONTRACT/workbench_slot_rw.json`.
> Per slot, reads/writes as instructions (functions): `022D91A0` 356/535 (47r/84w), `022D9300`
> 160/244 (47r/63w), `022D9310` 88/223 (31r/48w), `022D8F90` 446/863 (44r/60w). The register names
> come from the bank page: ACC, vf22, vf23, `$t0`.

### Confirmed

`01EF93FC` holds `00 00 80 3F` = **`1.0f`** in the file image — but it is `.data` and it is written at
runtime; see §15b, which corrects this pass's word *"constant"*.

**Untouched by this pass:** the live row — *"the workbench deposit slots are idle at the title
screen"*, 40 samples with a moving control — is **one of the three live claims in the entire
database**, and nothing here bears on it. §14's 156 call sites and the four `UNKNOWN` rows stay open.


## 15b. `w` is a load, not an immediate — [`EXP-115`](../_experiments/EXP-115-transform-primitives-exec.md), folded in 2026-09-19 (OPUS)

`EXP-115` executed the two primitives and reports that the forced `w` *"is a live global read, not
a constant"*. **It is right about the mechanism, and its consequence is overstated. Both halves
matter, so both are recorded.**

### What the cell is

`01EF93FC` is not a standalone constant. It is the **`w` lane of the 16-byte cell at `01EF93F0`,
the software image of VU0's `vf00`** — the register the VU0 architecture hardwires to `[0,0,0,1]`.
[The EE and VU0 register bank](Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md) already
identifies it as `vf00`; this contract called it *"the constant at `01EF93FC`"* and the two
descriptions had not met.

### Every writer, and they all store 1.0

A sweep for stores **whose destination range covers** `01EF93FC` — not merely stores addressed to
it, which is the distinction that matters when a 16-byte store writes a 4-byte lane — finds three:

| writer | store | source |
|---|---|---|
| `0036D990` | `0036D9A8` `movss [01EF93FC], xmm0` | `1.0f` at `01CEBBA8` (`.rdata`) |
| `0036D9E0` | `0036D9E8` `movss [01EF93FC], xmm0` | the same `1.0f` |
| `0036DD80` | `0036DD87` `movups [01EF93F0], xmm0` | `[0, 0, 0, 1]` at `008C5FD0` (`.rdata`), verified byte-for-byte |

> **So the divergence `EXP-115` warns of has no writer in this image.** Its wording — *"a
> reimplementation baking `1.0` would diverge under any writer that changes it"* — describes a
> writer that does not exist: all three restore the architectural `vf00`. **A reimplementation that
> bakes `1.0` produces identical output for every input the shipped binary can present.**

**The reason to correct the contract is therefore not divergence, it is description.** Saying *"the
constant at `01EF93FC`"* states the wrong mechanism: a reader implementing from that sentence
writes an immediate, and then cannot explain why the address appears in 176 sites across the image,
why it sits in `.data`, or why three functions initialise it. The invariant now says **load**, and
says separately that every shipped writer makes that load yield `1.0`.

*(A note on my own instrument. The first sweep asked which stores are **addressed to** `01EF93FC`
and found two, missing `0036DD80` entirely — the `movups` writes the lane without naming it. The
second sweep then over-reported, because it sized `mov` by mnemonic and counted a `mov dword ptr
[01EF93F8], 0` as eight bytes. The figure above comes from the third, which uses the decoded
operand size. **Two of the three sweeps were wrong in opposite directions, and only comparing them
showed it.**)*

### The other four findings

- **`in[3]` reaches the input deposit and nothing else.** `in[3] = 99` and `in[3] = 0` give
  byte-identical output *and* byte-identical deposits apart from the verbatim copy at `022D9300`.
  This **strengthens** invariant 1: the fourth lane is not merely unused in the arithmetic, it is
  preserved into the deposit, so a reconstruction must copy it rather than drop it.
- **Triple aliasing is safe**, extending the contract's two alias modes: `a == b == out` on one
  buffer computes `mat²` correctly, because the stack staging precedes every store.
- **The stack cookie check is real**, comparing against the shipped `q[01F44830]` and executed in
  full — `cmp`, the top-16-zero `rol` test, and a `bnd jne` to `00809654`.
- **The composer touches no global but the cookie**: the whole `022D8F80`–`022D9330` window is
  unchanged across all ten compose cases, so **the deposits belong to the point transform alone.**

*(OPUS 2026-09-19, on `REQ-OPUS-TRANSFORM-PRIMITIVES-FINDINGS` from SWE2-ORACLE.)*

## 16. Parity plan

`CALCULATION` — both laws, over random pairs and designed cases that separate the argument orders.
`STRUCTURAL` — the four deposits and the composer's 64-byte extent, against sentinels.
`EDGE-CASE` — `w` ignored, and all three aliasing modes.

**All three are done offline** — §13. `CALCULATION`, `STRUCTURAL` and `EDGE-CASE` are covered;
`INTEGRATION` is not, because no caller is reconstructed; `FULL-SUBSYSTEM` is not, because the
reconstruction takes the workbench as parameters and **does not write the globals at all** — the
mapping from parameters to those addresses belongs to callers, and none exists.

**One mutant is left alive on purpose**, and the reason is a rule rather than an exception: a loop
bound `< 4 → < 5` writes one element past `accum` and `result`, which are locals, and `*out = result`
copies only `sizeof(Vec4)`, so the extra lane never reaches the interface. It is benign *in this
build's stack layout* rather than truly equivalent — a different placement would have corrupted the
output and killed it. **Killing it would mean putting canaries in production code to satisfy a test**,
which is contorting the source to flatter the instrument. Two sibling mutants of the same shape WERE
killed, by putting the canaries in the *driver* where they belong.

**Four things a reimplementer must take from this contract:**

1. **`out = b × a`.** The natural order is wrong and still looks like a transform.
2. **Write the deposits.** Three of the five destinations are not the caller's buffer.
3. **The accumulator is the pre-translation sum**, not the result.
4. **Stage both inputs before multiplying**, or aliasing corrupts the answer silently.

## 17. Related

- [the two transform primitives](Shared-Transform-Workbench/the-two-transform-primitives.md) — the
  page this formalises, with the falsification checklist.
- [how a position becomes a single number](../17-Presentation-Rendering/Position-To-Scalar/how-a-position-becomes-a-single-number.md)
  — a path where the installed matrix is the **identity**, so the arithmetic is a no-op and the call
  exists *only* for what it deposits.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT, fan-in of 299 edges.** The render layer is the primitives' main consumer. By Presentation neighbours: `00397910` 76, `0039AF70` 72, `00398F90` 64, `0039B550` 57, `003970A0` 29. Each edge is a Presentation body calling a primitive the contract documents.
- **ActorEntity — MECHANICAL (1 edge).** 1 ActorEntity-side calls into shared helper(s) the page cites (`0036DD80`) - the helpers' general call surface, not a ActorEntity relationship of this page's subjects.
- **Audio — MECHANICAL (3 edges).** 3 Audio-side calls into shared helper(s) the page cites (`0036DD80`) - the helpers' general call surface, not a Audio relationship of this page's subjects.
- **UI — CLIENT (3 edges).** 3 inbound (UI bodies `0024B9B0`, `0035DCC0`, `00368010` call page-cited `0024C060`, `0036DD80`, `00397910`). Substantive edges include `0024C060` is called by `0024B9B0`; `00397910` is called by `00368010`; the remaining edges run through shared helpers the page cites.
## SWE2-EC7-91 update (2026-09-20) - `0039EC30` + `00396A30` + `003954E0` measured

`0039EC30` (693 B) is the `02F8F2xx` sibling of `0039F9F0`: the
`02F8F2C6` word indexes a `02F8F2F8` slot (x5) whose record
takes a `0020E680` allocation, the minimum of the
`+4`/`+0x14`/`+0x24`/`+0x34` fields, the `02AEE910` flag nibble
and the `0024E460`/`003A3D20`/`003A2C70` OR; `008642A0` +
`0039CDC0` produce the output record, 16 byte->float lanes fill
its `+0x10` block, `+0x40` = 4 and `+0x44` = 1, the
`02AEE900 == 6` arm selects `02AEE908` into `+0x30`, and
`0020E670` publishes before tailing `00182F50`.
Interior anchor `0039EC68` (the `0020E680` call).

`00396A30` (1,262 B) is the canonical staged transform pass the
primitives call: [rcx]'s vec4 seeds the `022D9xxx` workbench,
each iteration advances the source 0x10 bytes, dot-product
chains accumulate, `00861F14` renormalizes with a
zero-fallback, and `movups [rax-0x10]` emits each staged vec4
until the watermark matches.
Interior anchor `00396D8D` (the `00861F14` call).

`003954E0` (662 B) is the offset-cursor variant: the source
walk starts at `[rdx-4]` stepping 0x10, the same dot-product
and `cvtps2pd`/`andps` magnitude chain runs, `minss` clamps the
published lanes, and the staged vec4 lands at `[r9]` on the
watermark turn.
Interior anchor `00395651` (the `cvtps2pd` magnitude arm).

`00503180` (336 B) is the arg vector `00501750`/`005032D0` call: `byte[rbx + 0x3A]` times, `word[rbx + 0xC]` plus `byte[[rbx + 0x18] + i]` feed `003AA280(0x52)` and each result lands at `[rbx + 0x28] + i*8` - the expression's argument fill.

Interior anchor `005031B5` (function `00503180`).
