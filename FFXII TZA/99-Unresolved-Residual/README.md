# Unresolved residual

**30 functions in `FFXII_TZA.exe` currently carry no classification at all** *(GN161, 2026-09-14 —
160 when this folder opened; the dated sections below record each checkpoint's state at its date).*
This folder tracks them until that number is zero.

| | |
|---|---|
| Count | **30** |
| Residual list SHA-256 | `955da8c990265c87878d7b6c5e30e0fdfdb395825745cadc3813ec3b40a93353` *(GN161; GN158 list was `c5d4b7f7…`)* |
| Address list | [`residual-30-GN161.tsv`](residual-30-GN161.tsv), `address` column. The SHA-256 above is over the uncommitted work list `Tools/work/verify_GFZ_PARENT/residual_addrs.txt`, which holds the same 30 addresses (sorted set diff empty, 2026-09-15) |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Why these are hard

There is no cheap evidence left in this tail. Every easy signal is exhausted:

| Signal | Available |
|---|---:|
| Direct authored strings | **0** *(answered: see the glyph-quads page, "Superseded reading" — the zero was the scanner's; `0020AC30`, one of the 158, loads `"sum_"` at `0020AC30`+0xFA; 2026-10-02, OPUS)* |
| Exact-body clone hits | **0** |
| Qualified Phyre/std/EASTL symbols | **0** |
| Functions with direct PrimaryOwner references | **2** |
| Real code data references | **16** (across 13 functions) |

And of the 382 incoming data references to these functions:

| Count | Type | Usable |
|---:|---|---|
| 199 | `PEx64_UnwindInfo` | banned |
| 160 | `_IMAGE_RUNTIME_FUNCTION_ENTRY` | banned |
| 6 | `IPToStateMapEntry[...]` | banned |
| 16 | real `.text` references | yes |

~~**96 % of the incoming references are exception metadata**~~ — **QUALIFIED 2026-09-02.** The
figure is correct *about the reference dump* and is **not a measurement of the image**. It counts
only references Ghidra holds, and Ghidra holds none from a data slot that was never typed as a
pointer. A base-relocation census of function-pointer slots finds one for `002AAE40` at
`00916518` — the very function this category called *"the purest example of why a call-context
classifier cannot touch these."*

**A relocated function pointer is admissible tier-8 evidence**, so the 96 % is an upper bound on
banned-ness and the denominator is the wrong population.

**The re-census has now been run, and the result overturns this section's premise.**

| incoming evidence | of the 158 |
|---|---:|
| direct caller in the call graph | ~~143~~ **144** |
| verified RIP-relative `LEA` | 12 |
| relocated data slot pointing at the entry | 1 |
| **at least one admissible reference** | ~~156~~ **~~157~~ 158** *(answered: see the-unresolved-158.md, "The count is now 158 of 158" — the nine-patch box renderer is entered by a conditional jump at +0x5 of its 12-byte opacity gate, and that gate has four callers; 2026-10-02, OPUS)* |
| **no admissible reference of any kind** | ~~2~~ **~~1~~ 0** *(answered: see the box-renderer page's REFUTED box; 2026-10-02, OPUS)* |

~~**156 of 158**~~ **~~157 of 158~~ 158 of 158 have admissible incoming evidence.** *(answered: see the-unresolved-158.md, UPDATED 2026-09-16; 2026-10-02, OPUS)*

> **Corrected within the hour, and the correction is the same defect this section is about.**
> `0020AC30` is reached through `thunk_FUN_0020ac30` (`001EC660`, five bytes, one `JMP`) from
> `ActorResource_BeginManagerResourceSetLoad`. The census route that missed it used
> `edges.tsv`, **and a thunk is a sink in the call graph** — a byte-level `E8`/`E9` decode finds
> the jump immediately. `the-thunk-layer-and-why-call-counts-disagree.md` §1 calls this *"the
> single most common way a measurement of this binary comes out wrong"*, and §2 says a graph
> census loses the path at the thunk. **The warning was written down and not consulted** —
> exactly what this document criticised a sibling for two passes earlier.
>
> **Cost measured rather than assumed:** across all 158, 143 have callers in both graph and
> bytes, **1 in bytes only**, 0 in graph only, 14 in neither. **One function — and it was half
> the headline.** The 15 without a direct caller match §10's
caller-less count exactly, and for **13 of those 15 the evidence was available all along and the
instrument did not surface it.**

> **The barrier was never the evidence. It was the census.**

**And the dump is wrong in both directions**, which is why the figure above cannot be repaired by
moving one number. Of the 16 rows it credits as real code references, **two are not references at
all**, decoded from the image and re-verified here:

```
0023F06E   48 89 83 20 01 00 00        mov [rbx+0x120], rax
                                       the STORE of an address the previous instruction loaded --
                                       one address-taking counted twice
002A756C   81 8b e8 03 00 00 00 20 40 00
                                       or dword ptr [rbx+0x3E8], 0x402000
                                       an immediate BITMASK equal to a function entry
```

So *"16 across 13 functions"* is **14 across 12**, and `00402000` is **not address-taken in code at
all** — it keeps admissible status only through a direct caller. The scan both **omits** references
it was never told about and **invents** ones it was told about wrongly: the 96 % is an upper bound on
banned-ness **and a lower bound on admissibility.**

**Blind spots, stated so the number's direction is known:** the scan matches the `LEA` form only (a
`mov reg,imm64` address-taking would be missed — none of the 16 uses that form, which is not proof
none exists), and it is restricted to the file image (91 % of `.data` is not on disk). **So 156 is a
floor and "2 of 158 are evidence-free" is a ceiling.** The number can only move one way.

This tail is complete-body reading, one function at a time.

Body sizes: 289 B to 7,489 B, mean ~1,132 B, 181,146 bytes total.

## Closed — GN checkpoint, 2026-09-02

Both rows passed the exact-current fence and are now persistence-certified:

| Address | Proposed CodeDomain | Body | Documented at |
|---|---|---:|---|
| `00313A00` | `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation` | 289 B | [`../15-Input/Gameplay-Capability-Policy/`](../15-Input/Gameplay-Capability-Policy/) |
| `002F7380` | `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild` | 723 B | [`../17-Presentation-Rendering/Legacy-PS2-GS/`](../17-Presentation-Rendering/Legacy-PS2-GS/) |

Applied GN rows = **2**. Certified state is now **38,003 explicit / 158 unresolved /
99.58596 % / overlap 0**, reproduced from a fresh import of the packed checkpoint.

The evidence tail is unchanged in character: the remaining 158 still have no strings, no
exact-body clones, no qualified symbols, and their incoming data references remain almost
entirely banned EH metadata. Regenerate the residual evidence before working them.

## Method

Work them in small batches. For each candidate:

1. regenerate the residual and its evidence (never reuse a stale list);
2. rank by complete-body mechanism evidence, **not** address neighbourhood;
3. bounded-decompile the batch;
4. challenge each reading against callers, callees, real data refs, RTTI, strings, authored
   script data, and upstream source;
5. survivors become pre-enrichment rows; everything else stays unresolved;
6. run the mutation gate (see [`../../Tools/README.md`](../../Tools/README.md));
7. write the system document **before** claiming the function is understood.

Preserving `unresolved` is always allowed. Forcing a generic classification to move the
percentage is not.

## Systems in this category

- [`Unlisted-Code/referenced-code-the-list-never-had.md`](Unlisted-Code/referenced-code-the-list-never-had.md) -
  **PARTIAL, tier 1.** *(answered: see the page's front matter, now `status: DOCUMENTED`; 2026-10-02, OPUS)* The sharper half of the same defect: **143 of those blocks ARE pointed at**,
  and fourteen are reached by a tail `jmp` from a function the list does contain. **Twelve of the
  fourteen are named nowhere else in this database** - the list took the thunk and never took the
  implementation. Also measures a third defect: 29 listed bodies whose recorded range **contains**
  49 others.
- [`Unlisted-Code/the-code-the-function-list-does-not-contain.md`](Unlisted-Code/the-code-the-function-list-does-not-contain.md) -
  **PARTIAL, tier 1.** *(answered: see the page's front matter, now `status: DOCUMENTED`; 2026-10-02, OPUS)* A **third residual, and the only one outside every denominator**: the
  568,793 bytes `progress.py` reports between listed bodies, classified. **244,619 of them are
  code in ~~at least 1,471 blocks~~ 1,471 blocks** *(corrected 2026-10-02, OPUS: 874 bodies, 162 continuations, 3 ambiguous, 1 covered and 431 jump tables of data, `unlisted-body-admissions.tsv`)* ** the function list does not contain** - not cited, and not in the
  frontier either. Three quarters of it is 66 blocks of hand-written SIMD at the head of `.text`,
  attributed to **libvpx VP8 1.6.0** at tier 2. ~~The linker's own `.pdata` census agrees with the
  list **perfectly** (24,360 of 24,360) and is blind in exactly the same place.~~ *(Withdrawn 2026-09-15, pass 6:
  banned evidence. The page's unreferenced finding rests on relocations and branch targets alone.)*
- [`Largest-Unclassified-Code/the-largest-unclassified-functions.md`](Largest-Unclassified-Code/the-largest-unclassified-functions.md) -
  **PARTIAL, tier 1.** *(answered: see the page's front matter, now `status: DOCUMENTED`; its three largest are identified there; 2026-10-02, OPUS)* A **second, larger residual**: 10,024 functions / **2.41 MB with no
  `CodeDomain`** *(GN161; 10,154 when written)*, of which **9,409 do have an owner**. The three largest are characterised and
  placed in their call chains; **none is identified**.
- [`the-unresolved-158.md`](the-unresolved-158.md) -
  **DOCUMENTED, tier 3.** The 158 functions with no owner, no finalNo and no CodeDomain.
  **Every one is large** (median 828 B, max 7,489 B, 2.25% of `.text`); zero thunks, zero under
  128 bytes. The residual is a difficulty gradient, not a remainder.

## THE SHAPE OF THE FRONTIER, measured 2026-09-13 (OPUS)

19,909 bodies are declared by nothing - 58 % of the census and the largest single population in the
database. Every plan for it so far has been a plan for a NUMBER. `check_frontier_shape.py` measures
what it is made of instead, and proposes nothing; the EC-7 rule this role holds is that a bulk
disposition is earned per population, never applied to a total.

| by size | bodies | | by what the list already knows | bodies |
|---|---:|---|---|---:|
| 0-16 bytes | 1,801 (9.0 %) | | flagged as a **THUNK** | **7 (0.0 %)** |
| 17-64 | 5,622 (28.2 %) | | carrying a name that is not `FUN_*` | 801 (4.0 %) |
| 65-256 | 8,450 (42.4 %) | | **total bytes** | **4,685,043** |
| 257-1024 | 3,344 (16.8 %) | | | |
| 1025+ | 692 (3.5 %) | | | |

**SEVEN THUNKS. The easy wins are gone.** A frontier made of forwarding stubs would be a
bookkeeping problem; this one is 4.7 MB of real bodies, 96 % of them not even named. Nothing here
is going to fall out of a pattern match.

**AND IT IS HEAVILY CLUSTERED, which is the finding that decides what to try next.**

| in an unbroken run of | bodies | |
|---|---:|---|
| >= 2 frontier bodies | 19,143 | 96.2 % |
| >= 8 | 16,071 | 80.7 % |
| >= 32 | 8,806 | **44.2 %** |
| >= 128 | 1,668 | 8.4 % |
| longest run | 331 bodies | |

> **44 % of the frontier sits in runs of thirty-two or more consecutive undeclared bodies.** That is
> what statically-linked library code looks like in an address space, and it means **span
> dispositions are worth ATTEMPTING** here. Had the frontier been evenly scattered through
> documented code, they would not be, and proposing them anyway would have been the unsupported bulk
> disposition this role exists to refuse.

**A RUN IS A CANDIDATE, NOT A FAMILY.** The PPFX row that carries 1,657 members earned it with a
provenance argument, boundary controls at both edges, outbound-call and shared-global controls, and
a generated member list that a checker re-derives. A run length is none of those. What the clustering
establishes is that the *attempt* is justified - not any particular disposition, and not one member.

**The control is the part worth keeping.** Read naively this shape came out over 23,800 bodies
against the headline's 19,909, because the raw function list holds 38,161 rows and the scored census
keeps 34,270. The 3,891 difference was entirely rows the census never counted. The check now refuses
to print percentages unless its population matches `check_dispositions` exactly - **a shape measured
over a wider population than the headline describes something else entirely**, which is the defect
this session found six times and the one time it was caught before publication rather than after.

### THE HEAVIEST RUN IS NOT UNIDENTIFIED CODE — it is an unfinished page (OPUS, 2026-09-13)

The 210-body run at `00478280`–`004FF270` is **551,023 bytes, the densest block of undeclared code
in the database** and 96 % of the clustered mass is runs like it. Before anyone budgets it as
research from nothing, here is what it is.

**Five pieces of evidence, none of them a guess:**

| evidence | what it says |
|---|---|
| **82 distinct outbound targets** from 210 bodies and 551 KB | a largely **self-contained** subsystem |
| `sqrtf` ×107, `sinf` ×4, `cosf` ×4 | heavy **scalar float geometry** |
| `RenderCommand_GetCurrentWriteBuffer` ×9, and the run's one named member is `RenderCommandBuffer_ConfigureBackingRange` | it **emits render commands** |
| **0 of 25,797 RTTI method rows** fall in the range | **not C++ virtual-dispatch code** — no vtable slot points here |
| `the-vif1-vu1-layer.md` cites **29 distinct addresses inside the run**, including `004B1190`, its largest member at 32,136 bytes | **a page already covers it** |

> **THE REGION IS THE PS2 VIF1 / VU1 LAYER, AND IT HAS A PAGE.** Non-virtual, math-heavy,
> render-command-emitting, self-contained: exactly a recompiled vector-unit pipeline. The page names
> its biggest function already.

**So why is every one of those 210 bodies still in the frontier?** Because the page is
`status: PARTIAL`, and `measure_a` counts a citation only from a **DOCUMENTED** page. Twenty-nine
citations into the densest undeclared region in the database are invisible to the disposition
measure for that one reason.

> **AND THE FIX IS NOT TO CHANGE THE STATUS.** `PARTIAL` is the page's own honest assessment and it
> carries `passes: 0` — it has never been attacked. Promoting it to get the citations counted would
> move 551 KB out of the frontier by editing a word, which is precisely the inflation the standing
> rules forbid. The status follows the work; it does not substitute for it.

**HOW MUCH OF IT THE PAGE ACTUALLY REACHES, because "a page covers it" is too generous and was my
own first wording.** Mapping every address the page cites onto the bodies it lands in:

| | bodies | bytes |
|---|---:|---:|
| frontier bodies in the run | 210 | 551,023 |
| the page cites **any** address in | **22** (10.5 %) | 178,017 (32.3 %) |
| the page never mentions at all | **188** | **373,006** |

So the page reaches a third of the mass and a tenth of the bodies. **That is what `PARTIAL` means
here, stated as a number instead of a label** — and it is a far more useful thing to hand an auditor
than the word. The page knows this about itself: its last open item is *"the 45 region functions
that touch VU state but neither template path installs"*, and it names `00499A20`, `0049D540` and
`004A8B00` — three of the bodies in this very run.

The largest body the page never mentions is `004D40E0` at 14,891 bytes, and it is not unknown to the
store either: it sits in `entry-only-large-bodies.tsv` as the second-largest entry-only body, cited
at its entry by the script-VM interpreter page. **Two documented pages touch this region and neither
opens it** — one names a third of its mass without entering most of it, the other names one body at
its front door.

**What this changes is the estimate, not the plan.** The heaviest run is not 551 KB of code nobody
has looked at — it is a subsystem with a page, an identification, and a named largest member,
needing the page finished and attacked. That page is already routed for a falsification pass as one
of the three documents short of `audit_coverage`, and this raises what that pass is worth: it is not
one document of 348, it is the gate on the largest single block of undeclared code in the store.

### `004D40E0` IS A RECOMPILED VU1 MICROPROGRAM — identified in the page's own vocabulary

`004D40E0` is where the two queues meet: the **second-largest body** in
[`entry-only-large-bodies.tsv`](../_index/entry-only-large-bodies.tsv), cited at its entry by the
script-VM interpreter page, and the **largest body the VIF1/VU1 page never mentions**. 14,891 bytes.
So it is the cheapest test of whether "finish the existing pages" is the right fix for that region.

Decoded whole — 2,776 instructions:

| measurement | value | what it means |
|---|---:|---|
| float-class instructions | **1,730 of 2,776 (62.3 %)** | 664 `movss`, 277 `mulss`, 179 `addss`, 56 `subss`, 50 `comiss` |
| distinct call/jump targets | **31** | almost no control flow out of itself |
| `0022CC20` | called **13×** | clears sixteen bytes at `01E02830` — one VU register |
| `0022CC30` / `0022CC40` | **5× each** | **the page's own §2.2: "VU sticky Z / sticky S"**, `\|= 0x80` and `\|= 0x40` on `02064DEC` |

> **A body that is 62 % scalar float arithmetic, calls almost nothing, and drives the VU register
> file and the VU sticky flag word is a VU1 microprogram recompiled to x64** — which is precisely
> what the VIF1 page's own introduction says exists: *"the VU1 microprograms they call exist as
> recompiled x64 functions, working over an emulated 1,024-word VU memory."*

**The page has the vocabulary and not the enumeration.** It documents `02064DEC` as the status word
with `0022CC40` / `0022CC30` as its only two writers, traces `004804A0` calling them on arithmetic
outcomes, and lists the sticky-flag pair in its key addresses. It simply never reaches the 14.9 KB
microprogram that calls them twenty-three times.

**So "finish the existing pages" survives its first test.** This body did not need new research to
identify - it needed the page's existing terms applied to a body the page had not opened. That is a
different and much cheaper kind of work than 373 KB of cold reading, and it is what the 188
unmentioned bodies should be assumed to be until one of them proves otherwise.

### CORRECTED AGAIN — I COUNTED 13,470 PACKED MOVES AS MATHS

The classification below, and the `48 → 47` reconciliation under it, were built on a float ratio
that counted `movaps` and `movups` as float work. **They are block copies.** This kit carries a
module whose first line is *"ONLY ARITHMETIC AND COMPARISON SAY WHAT SOMETHING IS. EVERYTHING THAT
RELOCATES BYTES SAYS WHERE THEY WENT"* — written on 2026-09-13 after the same mistake was made four
times in two other instruments — and I wrote a private `re.compile(r'(ss|ps|pd|sd)$')` anyway, with
`insn_class.py` sitting in the same directory. **Fifth time for this rule, first time with the cure
already on the shelf.**

Measured across the region: **13,470 packed moves** against **18,808 scalar float arithmetic**
instructions. Every ratio below was inflated by that. Re-run through `insn_class`:

| class | bodies | bytes | of region | *was* |
|---|---:|---:|---:|---:|
| **VU MICROPROGRAM** | **24** | 254,763 | **46.2 %** | *48 / 78.7 %* |
| drives VU state, not float-dominated | 35 | 202,418 | 36.7 % | *11* |
| neither signal | 134 | 77,307 | 14.0 % | *127* |
| float-dominated, no VU helper call | 17 | 16,535 | 3.0 % | *24* |

`004B1190`, the region's largest body at 32,136 bytes, falls from 40.4 % float to **29.9 %** — it
drives VU state but is not float-dominated, and 238 `movups` plus 187 `movaps` were what put it over
the line.

> **THE `48 → 47` RECONCILIATION IS SUPERSEDED, NOT REPAIRED.** It was a neat story — my classifier
> over-counted by one, the page was exactly right — and it rested on ratios that were wrong for every
> body. `004804A0` is still the status-flag comparison routine and still not a microprogram; that
> part was read from the page's prose and survives. **But the count was never 48 on a correct
> measure, so "48 was 47" was never the finding.** A reconciliation that lands on a satisfying number
> deserves more suspicion than one that does not, and it got less.

**And the corrected measure has its own known bound, stated rather than left implied.** `insn_class`
counts scalar float arithmetic and not packed arithmetic, and the region contains **829** packed
arithmetic instructions (`mulps` 478, `xorps` 182, `andps` 169) against 18,808 scalar ones. So these
ratios under-count real vector work by **at most about 4 %** — an error in the safe direction, unlike
the one it replaces, and small enough not to move a 40 % threshold.

### AND THE 24 IS A FLOOR — the float test misses the largest microprogram in the region by ten points

Auditing [`the-vif1-vu1-layer.md`](../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md)
turned the instrument on its own author. That page names six bodies as microprograms on
**registration** evidence — they are installed as function pointers through the MPG/template path and
entered by MSCAL. Five of the six my classifier agrees with. **The sixth is `004B1190`, the largest
body in the region at 32,136 bytes, and my classifier files it as `drives VU state, not
float-dominated`.**

| body | bytes | float % | VU helper calls | my class |
|---|---:|---:|---:|---|
| **`004B1190`** | **32,136** | **29.9 %** | **17** | *drives VU state, NOT float-dominated* |
| `004C8320` | 28,422 | 43.0 % | 16 | VU MICROPROGRAM |
| `004F7070` | 24,541 | 43.7 % | 30 | VU MICROPROGRAM |
| `004EF940` | 22,073 | 46.8 % | 30 | VU MICROPROGRAM |
| `004E31E0` | 18,098 | 51.3 % | 22 | VU MICROPROGRAM |
| `004E7D90` | 15,212 | 48.2 % | 20 | VU MICROPROGRAM |

> **THIS IS NOT A THRESHOLD THAT NEEDS TUNING.** `004B1190` misses by **ten points**, not by one, and
> it carries **17** helper calls and 1,591 references to the VU working-register area — the page counts
> those itself. A body cannot be dismissed as "not maths enough" while it is demonstrably installed
> and entered as a microprogram. **The float ratio is not a necessary condition, and my two-signal
> test was never entitled to a point estimate.**

**So the corrected 24 is a FLOOR, and here is the ceiling.** Dropping the float signal and keeping
only "drives VU state" gives **59 bodies / 457,181 bytes / 83.0 %** of the region. The truth is
between:

| | bodies | bytes | of region |
|---|---:|---:|---:|
| floor — both signals | **24** | 254,763 | 46.2 % |
| ceiling — VU-helper signal alone | **59** | 457,181 | 83.0 % |

**The page's independently derived 47 sits inside that interval**, and it got there without my
instrument: 35 distinct programs through the template path plus 12 unshared from the render-command
path. An interval that brackets a number derived another way is worth more than my retracted point
estimate ever was.

> **THE TWO-SIGNAL TEST NOW FAILS IN BOTH DIRECTIONS, AND I HAVE ONE OF EACH.** `004804A0` is a false
> **positive** — it watches the VU machine rather than operating it. `004B1190` is a false
> **negative** — it operates the machine without being float-dominated. Both were found by reading the
> page's prose against the instrument's output, and neither was findable from the output alone.
> **The classifier sorts bodies; it does not decide what they are.** The ceiling row above is
> deliberately not offered as the answer either: `004804A0` is inside those 59.

### SUPERSEDED — THE REGION AS I FIRST CLASSIFIED IT: "48 microprograms, four fifths of its mass"

> **EVERY FIGURE IN THIS SECTION IS RETRACTED.** It is kept, unedited, because the correction above
> is only checkable against what it corrects. **The live numbers are 24 bodies / 254,763 bytes /
> 46.2 %** — see *CORRECTED AGAIN* above. Both reconciliation blockquotes below (`48 WAS 47` and
> `48 AGAINST THE PAGE'S 47`) rest on the retracted count and are superseded with it; FABLE's **47**
> is untouched by any of this, because it is a registration census and never came from my classifier.
> **Nothing below this line should be cited.**

`004D40E0` was identified from the page's own vocabulary rather than new research. `classify_vu_region.py`
applies the same two signals to **every** body in the region, to find out whether that was luck or a
method. A body is called a microprogram only when **both** hold — float-dominated (≥ 40 % of decoded
instructions) **and** calling one of the three VU helpers the page names. Either alone would fire on
any maths or any caller.

| class | bodies | bytes | of region |
|---|---:|---:|---:|
| ~~**VU MICROPROGRAM** — float-dominated **and** drives VU state~~ RETRACTED | ~~48~~ | ~~433,680~~ | ~~78.7 %~~ |
| neither signal | 127 | 55,947 | 10.2 % |
| float-dominated, no VU helper call | 24 | 37,895 | 6.9 % |
| drives VU state, not float-dominated | 11 | 23,501 | 4.3 % |

**All ten of the largest bodies are microprograms**, from `004B1190` at 32,136 bytes down. So the
region's mass is not miscellaneous: four fifths of it is one kind of thing, and the 127 bodies that
show neither signal average 440 bytes — they are the small change.

> **RECONCILED: 48 WAS 47, AND THE EXTRA ONE IS MINE.** Sorting the microprograms by how close they
> sit to the 40 % threshold - where a two-signal test is weakest - puts `004804A0` near the bottom at
> 43.0 % float with 9 helper calls. **The page explains that body already, and it is not a
> microprogram:** *"`004804A0` compares a result with 0 and calls `0022CC40` when it is zero
> (`004805A2`) and `0022CC30` when it is negative (`004805B4`)"*. It is the **status-flag comparison
> routine** — the thing that CALLS the sticky helpers on an arithmetic outcome, which is exactly what
> a float-heavy body calling those helpers looks like from outside. Drop it and the count is **47**,
> the page's own figure.
>
> **This is a false positive of my classifier, not a correction to the page**, and it is worth
> recording as one: the two signals cannot separate a body that OPERATES the VU machine from a body
> that WATCHES it, because both are float-heavy and both call the same three helpers. The page's
> prose could; the instrument could not. **A near-match between a measurement and a document is the
> easiest place to write a sentence that sounds like a result** — the reconciliation went the other
> way from the one I would have guessed, and it cost one sort and one grep.

> **48 AGAINST THE PAGE'S 47, AND I AM NOT CALLING THEM THE SAME SET.** The page's first open item is
> *"what each of the **47** microprograms draws"*. This finds **48** carrying both signals **among the
> undeclared bodies alone**. That near-match is worth reconciling and is not evidence on its own:
> either one of the 48 is a false positive of a two-signal test, or the page's 47 is a floor, or the
> two populations are not the same list — the page may count microprograms it has already placed
> elsewhere. **The reconciliation is a piece of work, not an inference**, and the numbers are handed
> over rather than merged.

**One structural detail the counts gave up for free.** Across the region the helpers are called: VU
register clear **343×**, VU sticky Z **114×**, VU sticky S **114×**. The sticky pair is **exactly
equal**, which matches the page's own trace of `004804A0` calling one when a result is zero and the
other when it is negative — they are emitted together at every comparison site, and a reimplementation
that emits one without the other would diverge on the first non-zero result.

### CORRECTED THE SAME DAY — A LONG RUN IS NOT EVIDENCE OF LIBRARY CODE

The clustering table above says 44 % of the frontier sits in runs of thirty-two or more and
concludes: *"that is what statically-linked library code looks like in an address space."* **That
reading is too strong, and opening the two largest runs disproved it.**

| the longest run | the heaviest run |
|---|---|
| 331 bodies, **10,828 bytes** | 210 bodies, **551,023 bytes** |
| 33 bytes each, one idiom, 331/331 tail-jump to `atexit` | up to **32,136 bytes each**, all unnamed, no strings |
| a family candidate | **research, and no disposition will touch it** |

Two runs of comparable body count, fifty times apart in mass, and opposite kinds of work. So the
split was measured across **every** run of 32 or more rather than argued from two:

| shape | runs | bodies | bytes |
|---|---:|---:|---:|
| **generated** — mean body ≤ 96 B | 29 | 1,731 | 106,849 |
| **research** — mean body > 96 B | 116 | 7,075 | **2,647,425** |

> **THE CORRECTION. Contiguity is evidence of contiguity, and it has at least two causes.** Of the
> clustered frontier, generated-shaped runs are **19.7 % of the bodies and 3.9 % of the bytes**.
> Four fifths of the clustered bodies, and **96 % of the clustered mass**, are runs of substantial
> functions that no span disposition will ever legitimately claim. Span dispositions are worth
> attempting on a fifth of the clustered bodies, not on 44 % of the frontier.

**What survives from the original reading:** the frontier is not scattered, the generated-shaped
runs are real and the first of them is now routed with its controls named. **What does not survive
is the inference from run length to library code** — the 210-body run has a *longer* unbroken span
than the 331-body one and is 32 KB-per-body of unidentified engine work.

**The practical consequence is a change of expectation, not of plan.** The frontier's mass will be
reduced by reading code, not by declaring families: 2.6 MB of it sits in runs that look clustered
for the ordinary reason that a compiler emits a translation unit's functions together.

### THE LONGEST RUN, OPENED — 331 bodies at `0016AB00`–`0016D540` (OPUS, 2026-09-13)

The clustering measurement above says span dispositions are worth attempting. The way to find out
is to open the most concentrated run and see whether it survives the bar, so here is that run.

**331 bodies, 10,828 bytes — an average of 33 bytes each.** And the pattern is not sampled:

> **ALL 331 OF 331 REFERENCE `00808B90`.** Not a spot check, not a majority — every body in the run,
> decoded. `00808B90` is `atexit`, and the shape is the MSVC dynamic-initialiser idiom: `lea` a
> static object, `call` its constructor, `lea` its destructor, and tail-jump to `atexit` to register
> the teardown.

**THE BOUNDARY CONTROL IS THE PART THAT MAKES THIS SERIOUS.** The body immediately BEFORE the run
(`0016AAC0`, 53 bytes) and the body immediately AFTER it (`0016D560`, 53 bytes) are **both already
members of the accepted C family `PClassDescriptorConcrete static initialisers`**, whose own control
is *"all 254 tail-jump to `00808B90` (atexit)"*. So this run is not a region someone hopes is
library code — it is bounded at both edges by declared members of a family of exactly this kind, and
it is made of the same idiom at a different size class (33 bytes against that family's uniform 53).

**They are not that family's missing constructors.** That row records, in its own text, that each of
its 254 members calls its own per-type constructor and *"EVERY ONE STILL IN THE FRONTIER"*. A
constructor does not tail-jump to `atexit`; all 331 of these do. So this is a **third** population in
the same region: more registration wrappers, for statics that are not `PClassDescriptor`s.

> **AND IT IS STILL A CANDIDATE, NOT A FAMILY.** What it has: a provenance idiom, a 331-of-331
> control, and boundary controls at both edges. What it does not have: an outbound-call control, a
> shared-global control, and a generated member list a checker can re-derive — the things the PPFX
> row earned before it was allowed to claim 1,657 bodies. **Declaring 331 members on a strong
> pattern and two good edges would be precisely the unsupported bulk disposition this role exists to
> refuse, and refusing it is worth more when the pattern looks this good than when it looks weak.**

The declaration is routed to the area that owns the sibling family rather than made here.

*(Pass 22 adjacency, 2026-09-14: residual members still carry cross-layer edges — `002F7380` is
called by **movement** `0026E290` and `00313A00` by **combat-action** `00313DB0` (2 edges).
Residual is a classification state, not an isolation claim; the folder's members are called from
classified layers.)*

*(Pass 22 live-graph completion, 2026-09-15: `00313DB0` also calls `Audio` `002DEE70` and
`Party` `0031B7E0` (2 edges) — the same residual-member-adjacency argument as the movement
and combat rows.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `0031B7E0` on this page calls `ActorWork_GetBattleUnitRaw`, owned by that layer. What it reaches is **five bytes** that say where the link is: `return [actor + 0x30]`, the actor's battle-unit pointer, with no test of any kind; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B7E0` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `BattleMenu_BuildCommandEntryList`, owned by that layer, calls `0031B7E0` on this page. That caller is the command-list build, and the ceiling is in the first instruction: the menu kind is bounded at **`0x22`** into a jump table, after which `dword[+0x40]` is zeroed and `dword[+0x44]` set to `-1` before any entry is written; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**WorldAreaField — CLIENT.** `BattleSystem_RunFieldFrameOrchestrator`, owned by that layer, calls `00313A00` on this page. That caller is the field-frame orchestrator: with a zero argument it **clears bit 13 of `[02089340]`** and takes the tick counter, and the `0x40`-aligned stack block it builds is what the rest of the frame works from; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

Every citation on this page is a census entry of unresolved or unowned code, so each layer below arrives with those bodies' ordinary call graphs. None of them is a claim this page makes.

**Audio — MECHANICAL, 2 edges.** `002DEE70` calls `001DBE90`; `00313DB0` calls `002DEE70`.

**Gameplay — MECHANICAL, 5 edges.** `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) is called by `BattleUnit_HasCurrentFocusEngagementEvidence` (`0030BB30`), `00312B40`, `0031ADB0`, `BattleAction_FindApproachGeometryAroundTarget` (`00339630`); `00313DB0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`).

**Input — MECHANICAL, 2 edges.** `0016D540` calls `00879570`; `00313DB0` calls `00226BE0`.

**InputGameplay — MECHANICAL, 1 edge.** `00313DB0` calls `00313A00`.

**Party — MECHANICAL, 1 edge.** `00313DB0` calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`).

**Presentation — MECHANICAL, 29 edges.** `0022CC20` is called by `004753B0`, `004825F0`, `0048D240`, `004B0CF0` and 1 more; `0022CC30` is called by `004753B0`, `004825F0`, `0048D240`, `004B0CF0` and 1 more; `0022CC40` is called by `004753B0`, `004825F0`, `0048D240`, `004B0CF0` and 1 more; `004FF270` calls `00537C80`, `00537FA0`, `00538350`, `005387B0`; `002F7380` calls `00467AA0`, `00467B00`, `00467B10`; `004FF270` is called by `003A7DC0`, `003A7E80`; `0020AC30` calls `001C5750`; `0026E290` calls `002F7380`; `004B1190` calls `004B0CF0`; `004EF940` calls `004EDB50`; `004F7070` calls `004F5360`.

**Script_VM_Native_Bridge — MECHANICAL, 1 edge.** `002DEE70` is called by `00354EF0`.

**StoryEvent — MECHANICAL, 1 edge.** `0020AC30` calls `0020A800`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
