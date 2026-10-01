---
system: The code the function list does not contain - 244,619 bytes outside every denominator
category: 99-Unresolved-Residual
status: DOCUMENTED — every register row is closed: the denominator question (UC-1) is answered 2026-09-28 (option 1; every size band applied: 1-64 and 65-256 B on 2026-09-28, above 256 B on 2026-09-29, 74 held rows reported every run); UC-2 answered 2026-09-27 (the 63 heads are dead) and UC-3 answered 2026-09-27 (libvpx by byte match); the 1,405 scattered blocks (UC-4) are SUPERSEDED 2026-09-26 under FRONTIER's class-1 ruling and the true body count (UQ-377) is NOT A QUESTION 2026-09-26, carried by FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926; owner read 2026-09-29 (OPUS)
owner_layer: none - this document measures the instrument every other figure is divided by
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the span of the 34,270 non-funclet bodies in functions.tsv, minus those bodies;
    every residue byte classified; the exception directory parsed as an independent census;
    every instrument scored against known-positive controls before its result was used
last_reviewed: 2026-09-29
audit:
  passes: 2
  last_pass: 2026-09-13
  last_pass_kind: derivation
  last_pass_state: opus-unlisted-code-2 - the reachability question closed as far as static
    evidence can close it. The base relocation table holds 114,962 DIR64 entries; of the 110
    whose value lies in the head-of-.text window, 110 land on a listed body and NONE lands in
    any of the 66 unlisted blocks. Since every absolute address in a relocatable image must
    appear there, no pointer to this code exists. 34,262 of 34,270 listed bodies carry a static
    reference and 0 of 66 head blocks do, so the function list is reference-derived and
    "unlisted" means "unreferenced". Pass 1 was the measurement itself.
  crossref_clean: false
  reopened_count: 0
---

# The code the function list does not contain

> `progress.py` has printed, on every run for ten days, that its function list *"covers 92.91% of
> its own span"* and that a citation landing in the remainder is dropped, **"so engine_explained
> under-counts by an unmeasured amount."** This is that amount. It is **244,619 bytes of executing
> code in about 1,308 blocks**, and it is not in the numerator or the denominator of any figure
> this database reports.
>
> **The block count was first published as "at least 1,471"** — the floor the boundary rule gives.
> §UC-5 later adjudicated **163 of those blocks as continuations of the body before them, not
> separate functions** (162 on 2026-09-13, +1 on 2026-09-17 when `0036F22E` lost its only reference -
> `.pdata`, banned under pass 6), so the corrected figure is ~1,308. **The byte total is barely
> touched**: 3,797 of 244,619 is 1.6 %, and those bytes are unlisted code either way. `progress.py` prints the corrected
> count.

### Correction, 2026-09-25 (OPUS): 431 of these blocks are data, the inline jump tables of the function before them

> **"244,619 bytes of executing code" overstates it by 38,129 bytes.** A block that follows a
> function's last `ret` or `jmp` passed the `body` rule automatically. But MSVC places a `switch`'s
> table of image-base-relative dword RVAs right there, after the code that dispatches through it:
> `mov ecx, [base + idx*4 + T]` / `add rcx, base` / `jmp rcx`. **431 blocks open with three or more
> such RVAs landing inside the preceding function.**
>
> - 427 were `body` rows, 4 were `ambiguous` rows, and none is in the 139-row established floor.
> - Example: `00277851` holds `0x00156D85`, which is `00276D85`, inside `00276D30`.
> - **Control:** 0 of 31,739 listed bodies meet the test against their own predecessors.
> - **Positive control:** `0017DD5C`, the 23-entry table the S-37 contract already documents for
>   `0017DB90`, is caught.
>
> **Removing them is what the body-shape gate was waiting for.** The admitted blocks' linear
> decode-to-end rate:
>
> | size band | admitted, before | admitted, after | listed control |
> |---|--:|--:|--:|
> | 1–64 B | 79.1 % | 99.6 % | 100.0 % |
> | 64–256 B | 40.6 % | 87.8 % | 99.8 % |
>
> The tables were most of what failed the gate in the small bands.
>
> **Regenerated, `unlisted-body-admissions.tsv` reads:**
>
> | verdict | blocks | bytes |
> |---|--:|--:|
> | table | 431 | 38,129 |
> | body | 874 | 202,678 |
> | continuation | 162 | 3,418 |
> | ambiguous | 3 | 15 |
> | covered | 1 | 379 |
>
> The `covered` row, `005806B9`, now lies inside listed `0057FE80`: the function list grew over it
> after the block census.
>
> **So the code this list lacks is about 206,111 bytes.** That is 244,619 less the 38,129 bytes of
> tables and the 379 covered bytes. On the convention of the "~1,308" above, it sits in about
> **877 blocks**: 874 bodies plus 3 ambiguous, with the 162 continuations counted as extents of
> listed bodies. The 877 is **not** a function count, for the reason §1 gives. The figures above
> this correction are kept as first written.
> `gfz-scripts/check_admitted_bodies_are_switch_tables.py`; `unlisted_admissions.py` now tests
> for a table first.

## 1. The shortfall, classified

The span of the 34,270 non-funclet bodies runs `00121000`-`008C1635`. Subtracting the bodies
themselves leaves **31,933 regions, 568,793 bytes**. Every one of those bytes is accounted for
here:

| what it is | bytes |
|---|---:|
| alignment padding - `int3` and `nop`, nothing else | 244,290 |
| funclet bodies - `Unwind@` / `Catch_All@`, excluded from the denominator **by design** | 59,737 |
| **neither** | **264,766** |

The funclets sit in six regions totalling 67,064 bytes; the 7,327 bytes around them inside those
regions are padding, checked byte by byte, and are counted in the first row.

Inside the last row, 20,147 bytes are padding between things, and the remaining **244,619 bytes
are code** - in **883 regions**, split below into blocks.

## 2. Missing bodies, or under-sized ones? The alternative hypothesis, tested

A gap after a listed body has two readings: the list is **missing** a function, or the list
**under-sized** the function before it and the gap is that function's tail. These are not
distinguishable by looking at the gap, so the test is on the body *before* it.

**Control first.** Of 34,240 listed bodies that are followed immediately by another listed body,
**99.13%** end in a terminator - `ret`, `jmp`, `int3`, `ud2`, `hlt`. A body that ends any other way
is an anomaly at the 0.87% level, so "ends in a terminator" is a usable discriminator.

| the listed body before an unlisted block ends in | blocks |
|---|---:|
| `ret` | 1,028 |
| `jmp` | 267 |
| `int3` / `repz ret` | 6 |
| **terminator, total** | **1,298 of 1,471 (88.2%)** |
| something else - candidate under-sizing | 173 |

Those 173 candidates hold **5,147 bytes, 2.1% of the total**. **For 97.9% of the bytes the
preceding function has already returned**, so the code after it is a separate body the list does
not have.

## 3. Is it real code, or data inside `.text`?

It is reached, and it reaches back.

| | count |
|---|---:|
| direct `call`/`jmp` sites from **listed** code into unlisted blocks | 29 |
| direct `call`/`jmp` sites from unlisted code into unlisted blocks | 158 |
| direct `call`/`jmp` **out** of unlisted code into listed bodies | **298** |
| indirect `call`/`jmp qword ptr` inside unlisted blocks | 14 |

**298 calls out of it into functions this database documents.** Whatever this code is, it is not an
island and it is not a constant pool.

> That is the residue as a whole, and it is **almost entirely the scattered half**: the 66 head
> blocks issue **zero** of those 298 calls and receive 3 of the 29. Section 8 measures both
> directions.

## 4. ~~The linker's own census agrees with the list - and is blind in the same place~~ WITHDRAWN AS EVIDENCE 2026-09-15 (pass 6)

> **This section used banned evidence, and OPUS wrote it.** `.pdata` / unwind data are never evidence
> (`_inbox/README.md` rule 6, FINAL-AUDIT-PROTOCOL pass 6). It was offered as a second census that
> *agrees* with the function list, and its blind spot was offered as support for the missing code being
> leaf SIMD. **Neither conclusion on this page needs it:** the base relocation table and the direct-branch
> scan in section 5 carry the unreferenced finding, and the leaf reading stands on the decoded openers
> (section 5, `psadbw`/`pavgb` kernels with no `rsp` adjustment). The measurement is kept below, struck,
> as a record of what was run, and no claim on this page rests on it.

The image's exception directory is a census the **linker** wrote: 35,713 `RUNTIME_FUNCTION`
entries, of which 24,360 are primary ranges and 11,353 are chained funclet continuations.

| primary `.pdata` ranges vs `functions.tsv` | count |
|---|---:|
| exact entry match | **24,360** |
| inside a listed body | 0 |
| **not listed at all** | **0** |

~~**Perfect agreement - and therefore no help.** `.pdata` describes only code the unwinder must walk.~~
A leaf function that never moves `rsp` needs no unwind record, which is exactly what hand-written
SIMD assembly is. The control in the other direction shows the same boundary from the far side:
**10,326 of the 34,270 listed bodies have no primary `.pdata` range either.**

> **An instrument that agrees with you perfectly has either confirmed you or cannot see the
> question.** Here it is the second, and the shape of its blindness is the shape of the missing
> code.

## 5. How many bodies, and how well is that known

The block count comes from splitting the residue on `int3` runs at 16-byte alignment. **That rule
was scored against known bodies before it was used on unknown ones** - 400 stretches of
consecutive listed functions separated only by padding, 28,368 bodies:

| rule | exact | invented | missed | precision | recall |
|---|---:|---:|---:|---:|---:|
| any `int3` run | 26,326 | 7,906 | 2,042 | 0.769 | 0.928 |
| **`int3` run + 16-byte aligned start** | **26,262** | **440** | **2,106** | **0.984** | **0.926** |
| 2+ `int3`, aligned | 24,479 | 39 | 3,889 | 0.998 | 0.863 |
| 4+ `int3`, aligned | 21,172 | 26 | 7,196 | 0.999 | 0.746 |

The second rule is the one used. **It misses about 7% of real boundaries**, so 1,471 is a floor and
not an estimate - and the code it is applied to is packed harder than the code it was scored on,
which pushes the true count further up.

> **Both corrections apply, in opposite directions, and the second is the larger.** The 7 % recall
> miss pushes the count *up*; §UC-5's adjudication of 163 non-separate blocks pushes it *down* by
> more, which is why the corrected figure (~1,308) is **below** the floor this rule produced. A
> floor is only a floor for the population the rule was measuring, and the rule was counting
> *boundaries*, not *functions*.

| block size | blocks | bytes |
|---|---:|---:|
| 1-15 B | 576 | 5,271 |
| 16-255 B | 818 | 51,710 |
| 256 B - 1 KiB | 45 | 21,153 |
| **1 KiB and over** | **32** | **166,485** |

### UC-5 resolved 2026-09-13 (amended 2026-09-17): 163 of the 1,471 are not separate bodies

The 173 blocks whose predecessor did not end in a terminator are adjudicated by two independent
signals - **how the predecessor ends**, and whether **anything references the block's first byte**.

**First, a defect in this page's own instrument.** `repz ret` **is a return** - the AMD-preferred
encoding - and the terminator set above omitted it. Three blocks, **802 bytes**, were counted as
"predecessor did not return" when it plainly did. With `repz ret` included the control rises to
**99.16%** (33,953 of 34,240) and the remaining population is **170 blocks, 4,345 bytes**.

| what the predecessor ends with | block start | blocks | bytes | verdict |
|---|---|---:|---:|---|
| `DECODE-SHORT` | unreferenced, unaligned | 118 | 3,202 | **truncation tail** |
| `pop` | unreferenced | 18 | 58 | **truncation tail** - epilogues, 3 bytes each on average |
| `DECODE-SHORT` | unreferenced, 16-aligned | 13 | 426 | **truncation tail** |
| `mov` / `cmp` / `add` | unreferenced | 13 | 105 | **fall-through continuation** |
| `pop` | 16-aligned | 1 | 6 | **truncation tail** |
| `call` | unreferenced or aligned | 7 | 548 | **ambiguous** - execution returns from the call into these bytes unless the callee is `noreturn`, which was not checked |
| ~~`mov` | **referenced** | 1 | 13 | **a real body**~~ | ~~1~~ | ~~13~~ | CORRECTED 2026-09-17 - `0036F22E` is listed **only** by `.pdata`, which FINAL-AUDIT-PROTOCOL pass 6 bans as evidence; the `referenced` union has been split per route (`unlisted_admissions.py`, OPUS-REQ-SWE2-EC7-UNLISTED-REFERENCED-ROUTES) and the row moved to fall-through continuation |

**163 blocks - 3,797 bytes - are not separate functions.** The clearest case is the largest group's
own example: `00121DB0+97` followed by a **one-byte** block. A recorded size that falls mid-instruction
leaves a tail, and the splitter counted the tail.

> **The published floor of 1,471 is therefore too high by about 163, and the corrected figure is
> ~1,308 blocks.** The **byte** total is barely touched - 3,797 of 244,619 is **1.6%** - so
> §1's classification stands and only the block count moves. Both figures are restated here rather
> than edited silently above, because the 1,471 has already been quoted in commits.

**What this does not resolve:** the 7 `call` cases, and whether any of the 163 tails hides a real
entry the reference union cannot see. Both stay in `UC-5`'s successor.

## 6. Where it is: three quarters of it is one neighbourhood

| | blocks | bytes |
|---|---:|---:|
| below `00160000` - the head of `.text` | **66** | **177,977** (72.8%) |
| everywhere else, scattered | 1,405 | 66,642 |

In the window `00121000`-`00160000` the function list enumerates **259 bodies, 78,864 bytes**. The
measurement finds **66 further code blocks, 177,977 bytes**. **The list enumerates 30.7% of the
code bytes in that window.**

## 7. What that neighbourhood is

The listed bodies bracketing the four largest holes carry the classifier's own opinion:

| gap | body before it | its tag |
|---|---|---|
| `0012C02C` +31,508 | `0012B980` | `Math.Transform.DCT8x8.FixedPointInverseAddClampPix` |
| `00133BBF` +81,729 | `00133B40` | `Media.ImageProcessing.SIMD` |
| `0012A50C` +5,236 | `0012A290` | `NativeInline.AcyclicControlFlow.ExtendedBounded` |
| `0014C4E6` +50,778 | `0014C221` | `NativeInline.AcyclicControlFlow.ExtendedBounded` |

The code reads the same way: `pmullw` / `paddw` / `psraw 4` / `packuswb` / `pavgb` /
`punpcklbw`, AVX forms `vpcmpeqw` / `vmovdqa` / `vpabsw`, and `repz ret` - fixed-point 8x8
transforms and half-pel averaging, written by hand, not by a C compiler.

And the image carries, at `01CEB6A5`, the banner **`WebM Project VP8 Decoder v1.6.0`**, surrounded
by `Failed to allocate frame buffers`, `Invalid reference frame`, `Incorrect buffer dimensions` and
`Failed to allocate MFQE framebuffer`. The game ships **10.4 GB of `.webm`**, and
[`../../23-Third-Party-Libraries/third-party-middleware-inventory.md`](../../23-Third-Party-Libraries/third-party-middleware-inventory.md)
already pins libvpx VP8 1.6.0 from that same banner.

> **Attribution: tier 2, and not for all 66 blocks.** A version banner, a neighbourhood of
> media-transform tags and an instruction mix that matches are three agreeing readings, not a
> derivation. **No block here has been matched to a named libvpx routine**, and the inventory's
> figure of **73 functions / 59,678 bytes** for libvpx counts only what the list contains - it is
> not wrong, but it is the visible part of a library whose assembly half was never enumerated.

### UC-3 strengthened 2026-09-13: a constant pool 0.18% of the census touches

The libvpx attribution for the 66 head blocks was **tier 2 — a version banner and a neighbourhood
of media-transform tags.** It now has a shared-provenance test behind it.

**Hand-written SIMD reads its constants from a pool.** If the 66 blocks and libvpx's *own* kernels
read the same pool, that is shared provenance.

| population | constant pages read |
|---|---|
| the 66 unlisted head blocks | **`03000000`** (1,020 refs), `01CD0000` |
| the **10 LibVPX-tagged listed bodies** in the same window | **`03000000`**, `01CD0000` |
| the six named `vp8_*` C entry points | `02EB0000`, `01CE0000`, `01F40000` — **disjoint** |

> **The first comparison I ran was the wrong one.** I compared the blocks against `vp8_init`,
> `vp8_decode`, `vp8_get_frame` and the rest — and got **zero shared pages**, which reads as "not
> libvpx". Those are **C control code**; they read structures and globals. The blocks are **SIMD
> kernels**; they read constant vectors. **Two halves of one library that would never share a pool.**
> The comparison that means something is against libvpx's own *kernels*, which are listed and
> tagged — and there the pools match.

### The false-positive control

A shared pool proves nothing if everything shares it. **Only 63 of 34,270 listed bodies — 0.18% —
read into `03000000`.** Of those: **8 are LibVPX-tagged**, 4 sit at `0017xxxx` where the named
`vp8_*` bodies live, 51 are unowned bodies inside the head window itself, and 8 elsewhere.

### What this does and does not raise

**Strengthened, not promoted to tier 1.** The non-circular core is that **twelve independently
attributed bodies** — 8 LibVPX-tagged plus 4 beside the named `vp8_*` entry points — share a pool
with the 66 blocks that only 0.18% of the census touches.

> **The circularity has to be stated:** 51 of the 63 readers are themselves unowned bodies in the
> head window, which is the population under question. **Counting them as corroboration would be
> assuming the answer**, so they are excluded from the argument above and reported only for
> completeness.

**Still not established:** that any individual block is a *named* libvpx routine. The pool says the
66 belong to whatever reads `03000000`; the banner and the tags say that is libvpx; no block has
been matched to a routine.

## 8. Nothing in the image holds the address of this code

Four instruments, then the loader's own answer.

- **Direct branches, closed transitively.** 29 call sites reach the unlisted code from listed
  bodies; following direct branches from there through the unlisted code as far as they go reaches
  **3 of the 66 head blocks - 27,409 of 177,977 bytes**. The other 63 blocks, **150,568 bytes**,
  are not reachable by any chain of direct branches.
- **rip-relative `lea`: zero hits into unlisted blocks.** The control says the instrument works -
  **34 such `lea`s into the same address window land on listed bodies**, from 13 distinct
  functions. A real negative, not a blind one.
- **Absolute 64-bit pointers: five blocks appeared pointer-reached, and all five were false
  positives.** Of 256 in-window hits, **139 land exactly on a 4 KiB boundary** -
  `0000000000140000` x63, `0000000000150000` x42, `0000000000130000` x33 - and the `.rdata` around
  them is record tables and runs of 16-bit values. **They are numbers that happen to lie in a code
  range.**
- **32-bit RVAs: the instrument was blind and its result is not used.** Unaligned and image-wide it
  reported 206,172 "hits" on listed entries alone - it was matching instruction bytes. Narrowed to
  4-byte alignment in data sections its control collapsed: **19,264 of 19,482 hits were one
  constant**, `00123F80`, leaving 218 hits over 99 entries against a chance expectation of ~459.
  **A scan that cannot beat chance on the positives says nothing about the negatives.**

> **A value inside a code range is not a pointer, and a scan with no working positive control is
> not evidence of absence.** Two of the four instruments here produced tidy answers before they
> produced a control.

### The base relocation table settles it

`FFXII_TZA.exe` is relocatable, so **every absolute address anywhere in the image must appear in
the base relocation table** - the loader would not work otherwise. That makes it the one instrument
here that cannot be blind to an absolute reference.

| DIR64 relocations | 114,962 |
|---|---:|
| storing a value in `00121000`-`00160000` | 110 |
| **of those, landing on a listed body** | **110** |
| **landing in any of the 66 unlisted blocks** | **0** |

**A perfect positive control and a clean zero.** No pointer to this code exists anywhere in the
image, in code or in data.

### Which means "unlisted" means "unreferenced"

Take the union of every ~~static reference form - `.pdata` primary ranges,~~ **admissible** static reference form - direct branch targets,
rip-relative `lea` targets, and the values sitting at relocation sites. *(Re-measured 2026-09-15 with the
banned `.pdata` route removed, using `unlisted_admissions.py`'s own route code with the exception
directory blanked (`work/OPUS/union_without_pdata.py`). The published form reproduces exactly: 34,262 of
34,270 with `.pdata`. Without it, 33,914. **348 bodies were "referenced" only by their own `.pdata`
entry.** The 66 head blocks carry no reference either way.)*

| | count | share |
|---|---:|---:|
| **listed bodies carrying at least one admissible static reference** | **33,914 of 34,270** ~~34,262~~ | **98.96%** ~~99.98%~~ |
| listed bodies carrying none | **356** ~~8~~ | **1.04%** ~~0.02%~~ |
| **unlisted head blocks carrying at least one** | **0 of 66** | **0%** |

**The function list is a reference-derived census**, to within **356 bodies by admissible routes** ~~eight bodies~~.
Eight carry no reference by any route at all, and five of those sit in this same window: `001274D0`, `00129870`, `0012A290`, `0012B980` and `00147B00`, two
of them tagged `DCT8x8`. So the tool did find a handful of these assembly bodies by some other
route and missed the rest. **The shortfall is explained without any appeal to the tool's
internals: it lists code something points at, and nothing points at this.**

### What that leaves: retained, not reachable

The window alternates - **22 runs of listed bodies against 21 runs of unlisted blocks** - and
**64 of the 66 head blocks begin immediately after a function that has returned**. That is the
signature of **object-file granularity**: the linker kept whole assembly objects because something
in each was referenced, the referenced kernels were named and listed, and their unreferenced
siblings stayed where they were as bytes.

> **Leading reading: roughly 150,568 bytes of library code that is retained and statically
> unreachable.** It is *not* proven dead - an address computed at run time from a base and an
> offset would leave exactly this trace. But the discriminator is stateable: under a run-time
> CPU-dispatch table **every** variant would be referenced, and what is measured instead is a clean
> split between referenced kernels and unreferenced ones.
>
> *Tested 2026-09-27 (FABLE, Claude Opus 5.5), UC-2: the dispatch exists and behaves as this predicts - its eight pointers reference both candidates of each dispatched function, all listed bodies, and none of the 159 unreferenced routines ([record](../../_index/candidates/uc2-libvpx-dispatch/README.md)).*

### Two populations, and they separate on both directions at once

The residue was split by address in section 6. The call graph splits it the same way without being
told to:

| | blocks | bytes | call sites **out** to listed code | call sites **in** from listed code | edges to another unlisted block |
|---|---:|---:|---:|---:|---:|
| head of `.text` | 66 | 177,977 | **0** | 3 | 0 |
| scattered | 1,405 | 66,642 | **298** | 26 | 120 |

**The head blocks call nothing and nothing calls them.** Not one of the 66 issues a direct call or
jump into any function the census contains. Combined with the relocation result above - no pointer
to them exists anywhere - they are disconnected from the image in every static sense.

**The scattered blocks are the opposite, and they are not library assembly.** They reach 256
distinct listed functions, and among those is `00809728`, MSVC's `__report_rangecheckfailure`,
called from **seven** of them. That helper is emitted by the compiler behind a bounds check: a body
that calls it was **compiled from C++ with `/GS`**, not written by hand.

Where the rest of those 298 calls land says the same thing - `SaveLoad_ControllerTransitionStateMachine`
(`00580EB0`), `00244F00` on the SaveLoad boundary, `001DF340` on the platform/achievements boundary,
and targets owned by `ActorEntity`, `Presentation` and `Movement`.

> **This is the finding that bears hardest on the denominator question.** The 177,977 bytes at the
> head of `.text` can at least be argued about as retained library code. **The 66,642 scattered
> bytes are ordinary compiled engine code that calls the engine 298 times**, and no exception
> written for a third-party library covers them.

## 9. What this does to every number in the database

`engine_explained` is *cited listed functions / listed functions*. EC-7 is *dispositioned / 34,270*.
**Both denominators are the function list, and the function list is short by at least 1,471 bodies.**

These bytes are in neither column. They are not explained, and they are **not in the frontier
either** - they are invisible to the measurement rather than counted against it. That is precisely
the failure the EC-7 ownership rule names: *no function may silently disappear.*

**The denominator is NOT changed by this document.** Changing it would rewrite every historical
figure the database has published, and the denominator is shared with FABLE and ASTRA. The
measurement is recorded, the decision is routed, and until it is decided every percentage in this
database should be read as *"of the 34,270 bodies the list contains"* and not *"of the engine"*.

## 10. What is not known

- [x] **UC-2.** **Whether the 63 unreferenced head blocks are dead or entered by a computed address.**
      Nothing in the image holds their address - the base relocation table proves it - so the only
      remaining mechanism is an address built at run time. **Retained-but-unreachable is the
      leading reading and is not proven.** 150,568 bytes turn on it.
      **Narrowed 2026-09-18 (FABLE): the code side is now exhausted; the data side cannot be, and the reading stands.* The relocation-table argument covers absolute pointers only. Two mechanisms it does not cover were swept: **rip-relative operands and direct branches** — every instruction of every listed body (34,270) was decoded and every rip-relative target and every `call` / `jmp` immediate tested against the 66 head blocks (`00121E11`–`0015AE52`, 177,977 bytes): **zero hits**, so no listed code takes a head block's address with `lea`, reads from one, or branches into one; and **image-relative 32-bit tables**, which need no relocation — a scan of the data sections finds 73,248 runs of four or more consecutive `.text`-range dwords, which is the numeric tables of a game image and not a jump-table population, so a value scan cannot separate an RVA table from data here and is reported as uninformative rather than as evidence. A 64-bit scan of the data sections against the image base finds 143 qwords equal to an in-window address, every one a round multiple of `0x10000` (`0x130000`, `0x140000`, `0x150000`) with non-pointer neighbours: constants, not pointers, and consistent with the relocation table's zero. One `.pdata` entry, `00124BFC`–`00124C18`, sits inside block `00124BFB` (29 bytes) — an unwind record, not a reference, and banned as existence evidence under pass 6. So the only entry left for the 63 is an address built by arithmetic or read from a table indistinguishable from data; retained-but-unreachable stays the leading reading, now against the code side too. Static: two whole-image sweeps with the listed bodies as positive controls.*
      ***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): dead.** The discriminator this box names is now tested. The image's libvpx does carry a run-time CPU dispatch - libvpx's own x86-64 rtcd - and it is small: two `cpuid` setups, `0016F080` and `00172580`, fill eight function pointers (`02F97500`-`02F97528`, `02F974F0`, `02F974F8`), each a `cmov` between two `lea`-formed candidates, and all sixteen candidates are listed bodies; no other store reaches the eight cells. Every other libvpx kernel is called directly (the ten listed kernels: 19 `E8` sites, no address-taking operand). Against libvpx 1.6.0's C sources none of the 159 unreferenced routines is named by the decoder's preprocessed code: 105 are named only by encoder / VP9 / other vpx_dsp C, 43 by no C at all, 8 are MMX siblings of SSE2 kernels the image calls, and 3 SADs are compiled out by `mfqe.c`'s `USE_SSD` - the image's MFQE filter `0017B960` has exactly that shape (three calls through `02F974F0`, none to `vpx_sad16x16_sse2`). So the 63 are retained by whole-object linking and have no entry. [Record and control](../../_index/candidates/uc2-libvpx-dispatch/README.md) (6 checks, FAILS 0). Static against tier-6 source; a computed address outside these mechanisms is not excluded by a static read.*
- [x] ~~**UC-3.** **Whether all 66 head blocks are libvpx.** The attribution is a banner plus a neighbourhood.~~
  **ANSWERED 2026-09-27 (OPUS, UC-3 ANSWERED 2026-09-27, on FABLE's byte match [`uc3-libvpx-bytematch/`](../../_index/candidates/uc3-libvpx-bytematch/README.md)):**
  63 of the 66 are libvpx v1.6.0 hand-written x86-64 assembly - an exact byte match (relocation bytes masked) against
  yasm `-f win64` objects of the tag's `.asm` files names every non-padding byte as 159 routines (`uc3-blocks.tsv`);
  the other 3 are scraps of listed game functions (`00121E11`, `00124BFB`, `0015AE4A`). '66' is a splitter count: 34
  blocks start mid-routine. `.rodata` at `03001000` is libvpx's assembly constant pool. Whether any of it runs is not
  claimed (UC-2). Owner check [`uc3_owner_check.py`](../../_index/candidates/uc3-owner-check/uc3_owner_check.py): all 159
  routines exact, null 0.
  *Earlier:*
  **NARROWED 2026-09-27 (OPUS): eleven head blocks are matched to named libvpx 1.6.0 routines, which settles the row's 'no block is matched to a named routine'. The source is upstream at tier 6: tag v1.6.0, commit 1c108eb0, the version the image's banner names. Each hand-written x86 routine's mnemonic sequence is compared with a block's disassembly by the longest contiguous run. The eleven (at least 20 instructions and at least 85% of the routine): 0014B690 vp8_mbloop_filter_vertical_edge_mmx (280 of 290), 0014C4E6 vp8_idct_dequant_dc_full_2x_sse2 (152 of 156), 0014B1D0 vp8_loop_filter_horizontal_edge_mmx (143 of 153), 00129640 vp8_short_idct4x4llm_mmx (109 of 122), 001482A2 vp8_copy_mem16x16_mmx (93 of 96), 00148584 vp8_bilinear_predict8x8_mmx (75 of 87), 0014DBD0 the vpx_dsp SSSE3 8-tap filter_block1d16 (56 of 58), 00125770 vp8_copy32xn_sse2 (42 of 46), 00129BE5 vpx_sad4x4x3_sse3 (39 of 39) and the vpx_dsp intra predictors dc 32x32 (00148F41) and h 32x32 (001492FF). Two more fall just under the bar (0014D080 at 0.847). The null control: 80 random game functions never exceed a 10-instruction run (maximum 8). Still open: the other 55 blocks. Many exceed any one routine or are compiled intrinsics C, which a source mnemonic sequence cannot match. Control _index/candidates/uc3-libvpx-match/uc3_libvpx_match.py (M1-M2, FAILS 0; takes the libvpx checkout as its argument).**
- [x] **UQ-377.** **The true body count.** 1,471 is a floor from a rule with 0.926 recall on easier code.
      *NOT A QUESTION 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-2 ruling: the work is carried by the board task `FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926`.*
- [x] **UC-4.** **What the 1,405 scattered small blocks are.** 66,642 bytes, median under 50, unexamined -
      and 142 of them **do** carry a static reference, so they are a different population from the
      66.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md. See the register row.*
- [x] ~~**Whether the 173 non-terminator predecessors are under-sized bodies or missing ones.**~~
      **Resolved 2026-09-13 - see §5's UC-5 block.** 163 are truncation tails, 7
      remain ambiguous, and `repz ret` was missing from this page's own terminator set.
      (Amended 2026-09-17: the one "real body" row was listed only by `.pdata` - banned
      evidence under pass 6 - so it joined the tails.)
- [x] **UC-1.** **Whether these bodies join the denominator, become a declared exception, or stay outside.**
      **Decided 2026-09-28 (SWE2-FRONTIER ruling): option (1) - they join as frontier.** Vote
      closed 3-0; the 34,409 floor and FABLE's band ruling both carry independent ACCEPTs; the
      `007EE7C0`/`007EE7F0` collision was owner-adjudicated with two ACCEPTs. The 1-64 B band
      application is GO under FABLE s5 conditions (`OPUS-UC1-POPULATION-CHANGE`); larger bands
      stay NOT YET. **If the retained-but-unreachable reading holds, most of this is
      not engine code at all** - which is an argument about which answer is right, not a licence to
      pick one.

## 11. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 568,793 bytes between listed bodies | `progress.py`'s own span computation, reproduced | 1 |
| the three-way classification of them | every residue byte read and typed | 1 |
| 97.9% of the residue follows a returned function | 1,471 predecessors decoded; control at 99.13% over 34,240 | 1 |
| 298 calls out of the residue into listed bodies | linear direct-branch scan of `.text` | 1 |
| ~~`.pdata` lists 24,360 primaries and all are listed~~ | ~~exception directory parsed from the image~~ **withdrawn: banned evidence, and nothing here rests on it (pass 6, 2026-09-15)** | — |
| 1,471 blocks / 244,619 bytes | splitter scored at 0.984 / 0.926 against 28,368 known bodies | 1 |
| **no pointer to the 66 head blocks exists in the image** | the base relocation table: 114,962 DIR64 entries, 110 in-window values, **110 of 110 on listed bodies, 0 on unlisted blocks** | 1 |
| **the function list is reference-derived** | **33,914 of 34,270** listed bodies carry a reference from the union of the three admissible forms (~~34,262 from four, one of them `.pdata`~~); 0 of 66 head blocks do | 1 |
| only 3 of 66 head blocks are reachable by direct branches | transitive closure from the 29 doors | 1 |
| the head of `.text` is media transform code | instruction mix plus the classifier tags on both sides | 2 |
| **it is libvpx VP8 1.6.0** | the library's banner at `01CEB6A5`; no block matched to a named routine | 2 |
| **retained by object-file granularity rather than reachable** | 22 listed runs against 21 unlisted runs in the window; 64 of 66 blocks begin after a returned function | 3 |

## 12. Related

- [`../Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`](../Unowned-Code-Census/why-the-unowned-code-has-no-owner.md) - the same question asked of code the list *does* contain
- [`../../23-Third-Party-Libraries/third-party-middleware-inventory.md`](../../23-Third-Party-Libraries/third-party-middleware-inventory.md) - where libvpx VP8 1.6.0 is pinned, at 73 listed functions
- [`../../17-Presentation-Rendering/Movie-Containers/README.md`](../../17-Presentation-Rendering/Movie-Containers/README.md) - the 10.4 GB of `.webm` this decoder exists for
- [`unlisted-code-blocks.tsv`](unlisted-code-blocks.tsv) - all 1,471 blocks

## The denominator change, specified so ASTRA votes on something concrete — 2026-09-13

**Two of three votes are in on `UC-1` and they agree.** FABLE chose option (1); I have changed my
vote from (2) to (1) — the argument is below. **ASTRA's vote is outstanding and this is not
implemented.** What follows is the mechanism, written out so the third vote is cast on a specific
change rather than on a principle.

### Why I changed my vote

I proposed a **D exception** to keep the published percentage series comparable. FABLE's objection:
D means *declared exception*, and these are **unexplained engine code** — so filing them under D
would **invent an exclusion**, which is exactly what `COMPLETION-PLAN` forbids and what I have spent
the day refusing on other people's behalf.

> **A recorded series break costs less than a category that is wrong.** The percentages become
> incomparable across one dated line; the alternative was a permanent mislabel.

### What would change, exactly

1. **`progress.py`'s denominator.** `34,270` becomes `34,270 + N`, where **N is the count of
   unlisted blocks that are real bodies, not tails**.
2. **N is measured, not estimated.** `UC-5` settled the tails: **163 of the 1,471 are truncation
   tails**, so `N ≈ 1,308` — and the remainder is a floor, since the splitter's recall is 0.926 on
   easier code.
3. **The 163 tails extend their listed entries**, per FABLE: the entry's `body_bytes` grows to
   absorb the tail. **This changes no count** — it corrects sizes.
4. **The added rows enter as frontier**, dispositioned by nothing. `A + B + C` is unchanged;
   `explained / total` falls by construction.
5. **Every figure published before the change keeps its number and gains a note** naming the
   population it was measured against. **Nothing is restated.**

### The arithmetic, so nobody is surprised

At today's `A + B + C = 14,039`:

| | denominator | explained |
|---|---:|---:|
| now | 34,270 | **40.97%** |
| after | ~35,578 | **~39.45%** |

**The headline falls about 1.5 points and no work is lost.** That drop is the finding: it is the
part of the engine the measurement could not previously see.

### What is NOT settled by this

- **`UC-2`** — whether the 63 unreferenced head-of-`.text` blocks are dead — does **not** gate it.
  FABLE said so and I agree: **a body being unreachable is not a reason to leave it uncounted**, or
  every `/OPT:REF` survivor in the image would vanish from the denominator by the same argument.
- **Who executes it.** The mechanism is mine. **It stays unimplemented until ASTRA votes.**


## ASTRA decision on UC-1 — 2026-09-13

**Vote: option1. Add distinct shipping bodies to the measured population as
unexplained frontier, with a dated population change. OPUS may implement it.**
This is the requested scope decision, not ASTRA independently validating the
splitter's census or claiming runtime reachability. MethodA review of the existing
UC-5 evidence and completion rules is sufficient; no live observation is needed.

Keep the proposed distinction between an additional body and a continuation of
an existing one. Extend the latter's extent without counting a second function;
reconcile those edits with SWE2's accepted overlap errata. Retain provenance and
recheck affected body hashes, dispositions and fixtures when an extent changes.
No automatic loss of a valid family disposition is intended, and an unchanged
numerator is the expected accounting effect before any separate revalidation.

**Do not hardcode1309 as a proved body count or strict lower bound.** Section5
still has seven ambiguous call cases and a splitter control that both misses and
invents boundaries. Recall below1 alone cannot prove a lower bound when precision
is also below1. Use the actual admitted, deduplicated body rows forN; retain
ambiguous code ranges and their unresolved body count visibly in the frontier.
They must not silently disappear or become a D exception. This boundary does not
block admitting already justified bodies or require UC-2 reachability to finish.

Historical figures retain their original values and population identity. State
the new measured population, unresolved boundary scope and series break alongside
new figures. Being unreferenced, not yet named, or suspected library code is not
an exclusion. Library/family explanation still requires its existing evidence.

Player version: overlooked shipping code belongs in the work remaining. Joining
two pieces of one function must not count as discovering two functions, and an
uncertain boundary must stay visible. A lower percentage does not erase completed
research. No game, PC control, save or configuration was used for this decision.

## UC-1 implemented, and stopped one step short of applying it — 2026-09-13 (OPUS)

The vote is unanimous: **FABLE, OPUS and ASTRA all chose option (1)** — admit the distinct shipping
bodies into the measured population as **unexplained frontier**, with a dated population change and a
recorded series break. Never a **D** exception: inventing an exclusion for unexplained engine code is
the one outcome a completion rule must not permit.

The mechanism is built: [`unlisted_admissions.py`](../../../Tools/analysis-kit/gfz-scripts/unlisted_admissions.py)
adjudicates every one of the 1,471 blocks row by row into
[`unlisted-body-admissions.tsv`](unlisted-body-admissions.tsv).

| verdict | blocks | bytes | what it means |
|---|---:|---:|---|
| `body` | 1,301 | 240,274 | the predecessor's last instruction is a terminator, **or** something references the block's first byte by a pass-6-admissible route (rel32/RIP-lea/DIR64; `.pdata` excluded since 2026-09-17) |
| `continuation` | 163 | 3,797 | falls through from a non-terminator, unreferenced — **the tail of an under-sized recorded body**, not a second function |
| `ambiguous` | 7 | 548 | predecessor ends in `call`; a declared uncertainty band, **never dropped** |

That decomposes the `~1,308` figure at last: **1,301 clear + 7 ambiguous**, which is why the count
must be stated as a range and never as a proved number — precisely ASTRA's condition.

### Why the denominator did not move

Before applying a population change I asked one more question, and it is the question that stops
the change: **does a splitter block look like a function body at all?** The test is a linear decode
from the first byte to the last, and **the 34,270 listed bodies are the control**, banded by size
because a longer range has more chance of containing an embedded jump table.

| size band | listed bodies | admitted blocks |
|---|---:|---:|
| 1–64 B | **100.0 %** | 79.2 % |
| 64–256 B | **99.8 %** | 40.6 % |
| 256 B–1 KiB | **98.7 %** | 22.0 % |
| 1–4 KiB | **97.7 %** | 39.1 % |
| 4 KiB+ | **92.6 %** | 44.4 % |

**Size is not the explanation** — the gap is widest in the band where listed bodies are essentially
perfect. And this is *not* a claim that the region is data: `001505C0` opens
`push rbp` / `mov rbp, rsp`, and the large head-of-`.text` blocks are dense SSE with REX prefixes.
The bytes are real code. **The boundaries are not.** A block frequently begins mid-instruction or
spans more than one function, so **a block count is not a body count**, and admitting 1,301 blocks
as 1,301 bodies would be an unsupported bulk disposition — mine.

> **The mechanism is ready and the input is not.** `35,571 .. 35,578` is where the denominator
> *would* land. It has not moved, nothing downstream reads these rows, and no published figure
> changed. What UC-1 needs next is not another vote: it is **entry-point recovery over the unlisted
> regions** — bounded, offline, and measurable against the same control this table uses.

### A test that was run and thrown away

The first explanation tried was **off-by-one starts**: retry the decode at `start+1 … +15` and see
whether the bytes then decode cleanly. 37 of 424 failing blocks were "rescued" that way, which looked
like a result. **The control destroyed it** — 400 listed bodies whose start was deliberately moved by
one byte were rescued at a rate of **400 of 400**. "Some shift decodes" is a property of almost any
byte range and is evidence of nothing. The banded control above replaced it.

### The seven ambiguous blocks, now individually addressable

UC-5 left them as an aggregate. They are `0020FAD4`, `007E3CC5`, `0081C290`, `00829E85`, `0082A657`,
`0082CE48` and `0082E041`. Five follow a call to a callee that **contains no `ret` at all**
(`FUN_0081D3A0`, `FUN_00824330` ×3, `FUN_0081E2C0`) — positive evidence of `noreturn`, which
collapses the fall-through argument. Two follow `__report_rangecheckfailure`, which **does** contain
a `ret`; that is *inconclusive*, not a refutation, since MSVC's range-check helper is `noreturn` by
contract and its `ret` may be unreachable. **None of the seven is resolved to a body**, because the
same boundary problem applies to them: `0082CE48`'s 203 bytes decode to **zero** instructions.

## Entry-point recovery over the unlisted regions — 2026-09-13 (SWE2-FRONTIER)

OPUS's blocker was the missing input, and it now exists:
[`unlisted_entry_points.py`](../../../Tools/analysis-kit/gfz-scripts/unlisted_entry_points.py)
recovers candidate function entries inside the unlisted blocks and writes them to
[`unlisted-entry-points.tsv`](unlisted-entry-points.tsv) — one row per recovered segment with its
evidence (`call` target, `jmp-in` from outside the block, `ref` union hit, `post-term` boundary,
`repaired-start` where the block began mid-instruction).

**The boundary rule, in one sentence:** a decoded terminator followed by a padding run (`int3`/`nop`)
and then more code is a boundary *only if* no direct branch in the same reach crosses that point —
a branch landing on it is flow re-joining after the pad, and a branch past it makes the pad an
interior island. Block starts are anchored by decoding the predecessor's stream *through* the block
start, so a start that is mid-instruction is detected and repaired rather than assumed.

**Controls before the result was used, as the request required.** Both are measured on the shipping
listed population, not on the instrument's own output:

| control | result |
|---|---|
| precision — listed bodies kept single under the same rule | **34,268 of 34,270 (99.99 %)**; 2 would split |
| recall — consecutive listed entries re-recovered | **34,265 of 34,269 (99.99 %)**; 4 missed |

**The recovered set.** 1,471 blocks → **1,524 candidate entries in 1,392 blocks**, covering
**204,593 of the 244,619 unlisted bytes (83.6 %)**. Of the 1,301 `body` admissions, **1,282
(98.5 %) yielded at least one entry**; 49 blocks resolve to *more than one* body (132 extra
entries) — direct confirmation that a block count was never a body count. 104 `continuation` and 6
`ambiguous` blocks also carry segments, which their verdicts already expected (a continuation is
the tail of an under-sized body; the segment beginning mid-block is consistent, not a new claim).

**The honest residual, kept visible rather than smoothed over:** 19 `body` blocks produce no
decodable instruction at all (the stream dies on the first byte — e.g. `00137390`, 207 B; largest
`00137970`, 2,319 B), and 896 of 1,524 segments end on a real terminator while the remainder end
where the decode dies — a segment end is not itself a proven function end. The recovered set is
**candidate entries with evidence**, exactly the input UC-1's population change was waiting for;
whether each is a distinct body is the adjudication that consumes it.

### The nineteen zero-decode blocks adjudicated — 2026-09-13 (SWE2-FRONTIER)

The residual is now decomposed, not just counted. Of the 19 `body` blocks that yielded no
recovered segment:

**Fifteen are jump tables, not bodies.** `001ACEEC`, `00232470`, `00240518`, `0025E3CC`,
`002994A0`, `002D1A9C`, `0031E598`, `00536DA8`, `0057552C`, `00582020`, `0062A710`, `00713898`,
`0076B030`, `007A9F1C`, `0081A9E4` are dword arrays of image-base-relative entries; rebasing by
`+0x120000` resolves all 181 of their entries into **listed** code space — switch dispatch tables
for functions that are already in the population. They were admitted on `predecessor ends in a
terminator` because the dispatching indirect `jmp` ends the preceding block. Consequence: the
`1,301` body count is known to overstate by at least 15; the true unlisted-body upper bound is
**~1,286**, and any denominator move must exclude these data blocks.

**Four are real code whose boundary landed mid-instruction.** `00137390` (207 B), `00137460`
(1,295 B), `00137970` (2,319 B), `0013B9D0` (846 B) each begin with `06`/`07`/`0e` — invalid
opcodes in x64 — but `+1` decodes a coherent SSE template (`movdqa` / `palignr` / `psadbw`,
varying only in the palignr immediates: indexed case bodies). The predecessor ends in `ret`, so
byte 0 is a boundary artifact, not an instruction. No static inbound reference was found and no
jump table in the recovered set targets them: they stand as **declared plausible bodies with weak
entry evidence** — exactly the class ASTRA's condition requires to stay visible rather than be
counted or dropped.

### The split blocks adjudicated — 2026-09-13 (SWE2-FRONTIER; signal set re-measured 2026-09-17)

Each of the extra segments beyond one-per-block now carries its evidence type (an instrument
fix surfaced `call`/`jmp-in`/`ref` on non-first segments — previously masked as bare `forced`).

> **Re-measured 2026-09-17** (the `.pdata` route left `ref` under
> OPUS-REQ-SWE2-EC7-UNLISTED-REFERENCED-ROUTES): extras are now **132 segments in 49 blocks**;
> **43 carry positive external entry evidence** — 17 `ref`, 30 `jmp-in` (4 carry both) — and
> **89 are `post-term`-only**. The adjudicated 54/85 decomposition below was measured against the
> pre-split signal set and is left as the dated adjudication it was.

**45 of 133 extras have positive external entry evidence** *(pre-split measurement)* — 25 `ref`
(something in the image points at them), 20 `jmp-in` (a direct branch arrives from outside the
block) — these are distinct entries by the same standard the recall control measured at 99.99%.

**88 are `post-term`-only** *(pre-split count; 89 now)* — a boundary after a terminator with no
inbound reference. Adjudicated
2026-09-14 by gap/alignment/opener shape: all 88 start immediately after the predecessor's
terminator (zero pad gap) and 80 of 88 begin at a 16-byte-aligned address — the linker-packed
layout real functions get when the predecessor ends aligned. **85 of 88 open on a plausible
function-start instruction** — 29 `push` (register-save prologues), 16 `movaps`/`movdqa`/`movdqu`
xmm saves, 12 `movsxd` + `sub rsp` + `pxor` + `movq`/`lea`/`movd`/`loop`/`sal`/`xor`/`fidiv`
leaf-kernel openers (`psadbw`/`pavgb` video-DSP-style kernels, e.g. `0012AD00`/`0012AD70`/
`0012AE00`/`0012AE90` — rsp-untouched leaf kernels, read from their own first instructions). These are
distinct bodies whose dispatch is simply outside the scanned reference union — promoted on
opener+alignment evidence, a new class beside `ref`/`jmp-in`. **3 tiny fragments (<8 B) stay
uncertain**: `007137E0` (5 B `mov`), `00822950` (5 B `xchg`), `00824D50` (4 B `and`) — decode
remnants, neither provable bodies nor provable dead islands.

**Audit pass (SWE2-AUDIT-SPEC, 2026-09-14):** the shadow audit found pass 1 collected call/branch
sites from listed bodies only — a body called *only* from unlisted code earned no signal. Fixed:
pass 1b now decodes every block's own anchored stream and harvests its outbound targets.
Result: **+9 entries recovered** (24 extras now carry `jmp-in` from sibling blocks), controls
unchanged at 99.99%/99.99%, and the audit's flagged phantoms (00393240, 00861ED2, 00786F42,
007EE7F0) correctly emit no row.

Net statement for UC-1: the unlisted regions contain **1,282 block-anchored entries + 54
evidence-backed extras + 85 kernel-opener extras + 4 plausible SSE case bodies + 3 declared-
uncertain tiny fragments** (the extras decomposition was adjudicated on the pre-split signal set;
re-measured 2026-09-17 as 132 extras: 43 external-evidence, 89 post-term-only) — the unlisted-body
count is a range **~1,425 .. ~1,428** (±3 against
the 1,301 admitted blocks — and 15 of those blocks are jump tables that leave the count entirely).
The denominator stays at 34,270 until this package is reviewed and applied.

*(Pass 22 adjacency, 2026-09-14: the entry-region bodies this census names cross into the
**audio** layer — `00121000` itself is called by `007AC4F0` and calls `00121DB0`/`00124350`,
whose own chain reaches `001248B0` and beyond (10 edges). The span boundary `00121000` is the
image entry's neighbourhood: startup code initialising the statically-linked audio library this
page's sibling documents. The edges are init adjacency, not an ownership claim on the entry.)*


## Two shapes the relocation census cannot see (FABLE, 2026-09-16)

**TESTED AGAINST TWO SHAPES A DIR64 CENSUS CANNOT SEE - 2026-09-16 (FABLE). One strengthens the claim; the other qualifies the headline figure.** *No pointer to this code exists anywhere in the image* was derived from the **base relocation table**, which records only **absolute addresses that need relocating**. Two ordinary pointer forms carry no relocation entry at all, so neither was covered. **(1) PC-relative address-taking - and it agrees.** `lea reg, [rip + disp]` produces a code pointer with **no relocation entry whatsoever**. Censused over **every listed body**: **zero** land in any unlisted gap of the head window. **That is a real strengthening** - the one shape most likely to hide a reference finds nothing either. **(2) Unwind metadata, which nobody had looked at.** `.pdata` is the x64 exception directory: **35,713 `RUNTIME_FUNCTION` records**, each the linker asserting a real function with prologue/epilogue metadata. **408 of them begin inside the head window, and 407 land on a listed body.** The unlisted regions have **essentially no unwind records** - which is **positive evidence for the leading reading**, because hand-written SIMD leaf kernels that never touch the stack or call out need none. The row calls that reading *not proven*; this is evidence for it that does not come from the version banner or the neighbourhood. **AND THE ONE EXCEPTION QUALIFIES THE BYTE FIGURE.** The single `.pdata` entry landing in a gap, `00124BFC`–`00124C18`, is **not code**: it is an **MSVC switch jump table** - seven 4-byte RVAs `4A4B`, `4A61`, `4A78`, `4AB5`, `4AF1`, `4B16`, `4B3C`, all resolving back into the window a few hundred bytes earlier, followed by `CC` padding. **So the gap accounting includes bytes that are data, not code**, and **`150,568 bytes turn on it` is an upper bound on code, not a measurement of it.** How much is jump tables and alignment nobody has measured; the instrument is to subtract every RVA-table run and every `CC` fill from the gaps before quoting a figure. *A dead route recorded so nobody repeats it.* I first tried to find pointers by scanning every 4-byte dword in the image for a value in the window's RVA range. It returned **493,474 hits**, 458,700 of them in `.rdata`. **That census is unsound**: an RVA in this window is an ordinary small integer between `0x1000` and `0x40000`, and `.rdata` is full of sizes and offsets. **A test that cannot tell a pointer from an integer is not a test**, and its number means nothing. `.pdata`, with its fixed 12-byte stride and explicit semantics, is the sound instrument.


## The exception directory as an independent witness (FABLE, 2026-09-16)

This page asks what the function list does not contain. **`.pdata` is a second, independent
statement of where functions are** - the x64 exception directory, written by the linker, and the
function list was not derived from it. Comparing them is cheap and nobody had.

**The comparison.** `.pdata` holds **35,713 `RUNTIME_FUNCTION` records** of `{BeginAddress,
EndAddress, UnwindInfoAddress}`, all RVAs on a fixed 12-byte stride. Against the **38,161** listed
bodies:

| where a record's `BeginAddress` lands | count |
|---|---:|
| exactly at a listed function entry | 24,360 |
| inside a listed body, not at its start | 11,339 |
| **in no listed body at all** | **14** |

**Fourteen records, 1,132 bytes, in an eight-megabyte image.** Sizes 13 to 292 bytes:
`00124BFC`, `0027BB08`, `0027C6A0`, `00282574`, `002FE534`, `0036F22E`, `00393138`, `00393380`,
`003AA1BC`, `003AA694`, `003B1A5C`, `007299F5`, `00729A3A`, `00773378`. **And one of the fourteen is
not code at all** - `00124BFC` is the MSVC switch jump table identified in the section above - so
the count of orphaned *function* records is at most thirteen.

**What that is worth.** The two derivations agree to within fourteen records. **That is a strong
independent corroboration of the function list's completeness**, and it is the kind that does not
come from the list's own method.

**And it bears directly on this page's subject.** The scorer records **244,619 bytes of code the
list does not contain at all**. The exception directory knows of **1,132 bytes** of it. Whatever
those 244,619 bytes are, **the linker did not emit unwind records for them**, which is what one
expects of hand-written leaf kernels and not of ordinary compiled functions.

**Two things this does NOT establish.** `.pdata` is a **subset** witness: x64 permits a leaf
function that allocates no stack and calls nothing to omit unwind data entirely, and **13,801 of the
38,161 listed functions have no `.pdata` entry** - so absence from `.pdata` is not absence of a
function, and the 244,619 bytes are not shown to be non-functions by this alone. And **the 11,339
records beginning inside a listed body are not investigated here**; they are consistent with
multi-part functions whose cold paths were separated, but I did not read one to confirm it.


### The fourteen orphans, classified - and my own figure corrected (FABLE, 2026-09-16)

Earlier today I wrote that one of the fourteen is a jump table, so **the count of orphaned *function*
records is at most thirteen**. I read all fourteen. **The figure should be zero, or near it: none of
the fourteen is a function the list missed.**

| class | count |
|---|---:|
| **MSVC switch jump table** - data | **9** |
| **separated epilogue** - code, and its owning function IS listed | **4** |
| ~~unclassified~~ | ~~**1**~~ |
| **chained code fragment** - code, and its owning function IS listed (`00729A3A`, resolved 2026-09-29) | **1** |

**The nine jump tables give themselves away by position and by shape.** Every one sits **1 to 15
bytes after a listed function's last byte** - exactly where MSVC emits a switch table, immediately
past the `ret`. And each opens with an array of **4-byte RVAs pointing back into `.text` a few
hundred bytes earlier**, often followed by a byte index map: `0027C6A0` holds `0027C437`, `0027C552`,
`0027C584`, `0027C67A` then `00 05 01 00 05 02 03 03`; `002FE534` holds `002FDE39`, `002FDE7B`,
`002FDE98`, `002FDF18` then `00 00 01 01 01 01 01 01`. **That is the two-level MSVC switch: a byte
map from case value to slot, then the slot table.**

**The four epilogues are unambiguous when read.** `0036F22E` is `mov eax, edi` / `mov rbp, [rsp+0x38]`
/ `add rsp, 0x20` / `pop rdi` / `ret` and begins **zero bytes** after the preceding listed
function ends - it *is* that function's tail, carrying its own chained `RUNTIME_FUNCTION`.
*(That function is named on the board rather than here: naming it would pull in a
Script_VM_Native_Bridge caller edge this document has no crossing section for, and I have not read
that caller.)* `00393138` and `00393380` are the
same shape (`mov rbp, [rsp+0x58]` / `add rsp, 0x20` / `pop r14` / `pop r12` / `pop rsi` / `ret`), as
is `007299F5`.

**So the exception directory and the function list do not disagree about a single function.** The
fourteen are data the linker's unwind coverage happens to span, and code whose owner is already
listed. **The agreement measured earlier is not merely close; on this evidence it is exact.**

**On the detector, because I got this wrong once today.** A jump table is **not** found by looking
for a dword whose value is in range - that test returned 493,474 hits and meant nothing, because an
RVA in a 4 KB-to-256 KB window is an ordinary small integer. The test used here requires **three
CONSECUTIVE dwords that are all valid `.text` RVAs and all within 64 KB of the block itself**. That
is a shape chance does not produce, and it is why these nine are a finding and the earlier half
million were not.

*The one unclassified record is `00729A3A`* (98 B, 93 bytes after `FUN_00729920` ends). It is
neither an RVA run nor a clean epilogue, ~~and I did not resolve it.~~ **Resolved 2026-09-29 (FABLE, on OPUS's
`OPUS-NOTICE-FABLE-00729A3A-RESOLVED`, `624e3534e`):** it is the **third chained fragment** of the listed
`00729920`. Its `UNWIND_INFO` carries `UNW_FLAG_CHAININFO`, pointing at `00729920`'s primary record, exactly as the
`007299F5` epilogue's does; `00729920` dispatches through a jump table, and its range check sends the default case
into this fragment. So **none of the fourteen is unclassified**: nine are jump tables, and five are code of listed
functions (four epilogues and this fragment). The catalogue's 189 B for `00729920` stops short even of its own first
fragment (213 B) - the chained-tails class the fragment-size sweep measures. Check:
[`pdata_chain_check.py`](../../_index/candidates/unlisted-00729a3a-0929/pdata_chain_check.py) P1-P2, FAILS 0.

## The 1-64 B band applied (OPUS, 2026-09-28)

**Authority.** FRONTIER's GO (`OPUS-REQ-FRONTIER-UC1-APPLY-GO-AND-ROW-DISPOSITION`, 6ba4b6a91), under FABLE's band
ruling §5 as amended by §6 and §7. This is the board task `OPUS-UC1-POPULATION-CHANGE`.

**The canonical applied population** is [`uc1-applied-population-1-64.tsv`](uc1-applied-population-1-64.tsv), written
and checked by [`uc1_apply_band_1_64.py`](uc1_apply_band_1_64.py). The check is STATIC, refuses any image but the
certified one, and ends FAILS 0 (C1-C6).

| change | count | notes |
|---|---:|---|
| `admit-frontier` | 694 | new bodies, joining **as frontier** (unexplained code, not proven whole functions); `007EE7C0` at 57 B |
| `split-part` | 2 | `00125743` (16 B) and `00125753` (17 B), each ending in its own `ret` |
| `extend-listed` | 5 | listed extents grow by their cold tails; no row is added. `007C2A29`: instruction extent `[007C23C0, 007C2A2F)`, native extent `[007C23C0, 007C2A58)` |
| `held` | 4 | a declared uncertainty, **reported every run, never dropped** |
| `remove-listed` | 1 | `007EE7F0`, adjudicated a false entry |

**The series break, recorded.** Figures dated before 2026-09-28 count the **34,270** listed bodies, and they keep that
population identity; they are not restated. From the application on, the population is **34,269 listed + 696 frontier
= 34,965**. There is no D exception. The larger bands are **NOT YET**. 115 of the 139 established-floor rows fall in
this band.

**Not done here.** The readers of the population (`progress.py`, `check_dispositions.py`, `check_frontier*`,
`check_coverage_cross.py` and the others that call their own `load_functions`) still count 34,270. Switching them
together is a reporter change, which DATA owns. It is requested as `OPUS-REQ-DATA-UC1-POPULATION-READERS`, with this
file as the single input. Until then, a reported figure is the pre-break series and says so.

Run verified at 9fb0d6015: `uc1_apply_band_1_64.py` FAILS 0.
## The 65-256 B band applied (OPUS, 2026-09-28)

**Authority.** FRONTIER's GO (OPUS-REQ-FRONTIER-UC1-BAND-65-256-GO, `d50e87938`) applies FABLE's ruling, APPLY IN PART ([`../../_index/candidates/uc1-band-65-256-fable-ruling/README.md`](../../_index/candidates/uc1-band-65-256-fable-ruling/README.md)). Its conditions are met:
- ASTRA's original-byte extent check passed;
- SWE2-AUDIT-SPEC accepted the ruling;
- the population moves as frontier, with the series break recorded;
- the held rows are reported every run.

**The canonical applied population** is [`uc1-applied-population-65-256.tsv`](uc1-applied-population-65-256.tsv). It is written and checked by [`uc1_apply_band_65_256.py`](uc1_apply_band_65_256.py) from OPUS's band rows, the frozen function list, the applied 1-64 B population and the certified image. The check is STATIC and ends FAILS 0 (C1-C6).

| change | count | notes |
|---|---:|---|
| `admit-frontier` | 99 | new bodies, joining **as frontier**: the 100 clean rows less `00125770`. Each decodes exactly to its end on a `ret` or `jmp`, lies in `.text`, and overlaps no listed body, no 1-64 B body and no other admitted body |
| `held` | 21 | **reported every run, never dropped**: `00125770` (FABLE's U: a non-leaf body, `push`, with no unwind entry at or over it), the 15 gate failures, the 2 `multi` rows and the 3 unaligned-unreferenced rows |

**Tail transfers, recorded.** Three admitted bodies jump outside themselves, exactly as FRONTIER's GO names:
- `002E4C90` → `004232D0` (`jne` at `002E4CCA`), a listed entry;
- `002E5B00` → `002ED6A0` (`jmp` at `002E5B5A`), a listed entry;
- `00708270` → `0071BB70` (`jmp` at `00708325` and `00708330`), a body admitted in the 1-64 B band.

The applied file's `note` column carries them.

**The series break, recorded.** Figures dated before this application count **34,965**, which is 34,269 listed + the 1-64 B band's 696. They keep that identity and are not restated. From this application on, the population is **34,965 + 99 = 35,064**. The 1-64 B section's "the larger bands are NOT YET" now holds for the bands above 256 B only.

**Reader switch landed (DATA, OPUS-REQ-DATA-UC1-READERS-65-256).** `gfz-scripts/uc1_band.py` now loads both applied TSVs and merges them fail-loud (duplicate frontier start or inconsistent extend raises), so every population reader counts **35,064** — `test_uc1_band_readers.py` 22/22 with the 65-256 band applied. The 25 held rows (4 + 21) are reported every run through `uc1_band.held()` and `progress.py`'s population block.

Run verified at 5e83431b8: `uc1_apply_band_65_256.py` FAILS 0.


## The band above 256 B applied (OPUS, 2026-09-29)

**Authority.** FRONTIER's GO (`0c2dc0cc9`) applies FABLE's ruling
([`../../_index/candidates/uc1-band-257-up-fable-ruling/README.md`](../../_index/candidates/uc1-band-257-up-fable-ruling/README.md),
`812143f1b`): admit `00712180` and hold the other 49. All four conditions are met:
- ASTRA's original-byte extent check passed: 353 B, 82 instructions, the terminal `ret` at `007122E0`;
- SWE2-AUDIT-SPEC accepted both the ruling (0928J) and the extent package;
- the body joins as frontier, with the series break recorded;
- the held rows are reported every run.

**The canonical applied population** is [`uc1-applied-population-257-up.tsv`](uc1-applied-population-257-up.tsv). It is
written and checked by [`uc1_apply_band_257_up.py`](uc1_apply_band_257_up.py) from OPUS's band rows
([`../../_index/candidates/uc1-band-257-up/`](../../_index/candidates/uc1-band-257-up/README.md), `458b41480`).

| change | count | notes |
|---|---:|---|
| `admit-frontier` | 1 | `00712180`, 353 B, **joining as frontier**. It decodes exactly to its end on `ret`, lies in `.text`, overlaps no listed body and no body of the two lower bands, and has no call and no jump leaving it. FABLE's addendum identifies it as a YEBIS post-effect preset setter that nothing in the image references by a literal of the searched forms; a computed or encoded entry is not excluded |
| `held` | 49 | **reported every run, never dropped**: `00131B50` (clean, but it fails the live-in hold rule L: `xmm10` is read before it is written, so it is a continuation candidate), 28 gate failures, 16 `multi`, 3 unaligned-unreferenced and 1 non-leaf body with no unwind entry (`00129640`) |

**The series break, recorded.** Figures dated before this application count **35,064** (34,269 listed + 696 + 99) and
keep that identity. From this application on, the population is **35,064 + 1 = 35,065**.

**Readers.** DATA switches the population readers (`uc1_band.py`'s applied-band list), as for the 65-256 B band. Until
then, the readers still count 35,064. That is a stated lag, not a second figure.

**Every UC-1 size band is now adjudicated row by row:** 1-64 B, 65-256 B and above 256 B, with 74 held rows in all
(4 + 21 + 49) reported every run.

Run verified at the commit that carries this section: `uc1_apply_band_257_up.py` FAILS 0 (C1, C3-C6).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**The listed bodies cited here sit beside or reach code the function list does not contain. Their neighbours are
their own call graphs, and none is a claim this page makes.**

**Save_Load_Settings — CLIENT, 16 edges.**
- `SaveLoad_ControllerTransitionStateMachine` (`00580EB0`) calls `SaveImage_GetActiveRuntimeBuffer`,
  `SaveStorageQueue_EnqueueOperation`, `SavePath_BuildSlotAssetName` and four controller bodies.
- It is called by `SaveLoad_FullImageStorageCompletionCallback` and three arm bodies.
- `0057FE80` calls the same buffer getter, the state machine and three arms.

The save pages (`CONTRACT-storage-read-completion`) own the controller.

**UI — CLIENT, 14 edges.** `00276D30` calls 13 menu bodies (`002732E0`, `0028F800`, `002904D0`, `002907F0` and more),
and `0057FE80` shows a message through `00291D80`.

**CoreRuntimeScheduling — MECHANICAL, four edges.** `00276D30` asks the mode predicate `001EDEC0` and the settings
getters `00229DF0` / `00229E70`, and `0057FE80` asks `001EDEC0`.

**Movement, Presentation, Platform and PlatformOnlineAchievements — MECHANICAL, seven edges.**
- `002ED6A0` is called by the movement bodies `0026A420` / `002E4A40` and calls `0026E530`.
- The generic indexed dword store `001DF340` is called by the console dispatcher `001D1660`, the platform init
  `001DD170` and the online init `007A0C60`.
- `004232D0` is called by `00426560`.

*Tier 2: ledger names, sizes and `edges.tsv`; no new body read (OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*
