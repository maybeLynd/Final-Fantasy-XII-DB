---
system: Arm catalogue — the cross-slice census (formerly the work division)
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: CodeDomain:Presentation.Rendering.NativeSupport + InputBoundary
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 27 addresses cited - 7 data, 6 entry, 11 interior, 1 literal, 2 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
converted_from: "WORK ORDER, owner repos-55 (coordinator), completed 282 of 282; converted by FABLE on OPUS-REQ-FABLE-ARMCATALOGUE-DISPOSITION"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: cross-slice-figures-rederived-from-image-two-corrections
  crossref_clean: true
  reopened_count: 0
---
# Arm catalogue — the cross-slice census

> **What this page is now.** It began as the work order that divided the console's 282 action ids into
> nine slices. The slices are delivered — [A](arm-catalogue-slice-A-ids-12-43.md) to
> [I](arm-catalogue-slice-I-ids-268-293.md) — and they are the authority for each row. What only this page
> holds is **the census across them**: the counts no single slice could make. Those counts are re-derived
> below from the image, by instruments that share nothing with the extractors that first produced them,
> and two of the published statements do not survive. The work order itself is kept unchanged under
> *History* for the record of how the catalogue was built.

## 1. The census, re-derived 2026-09-13

Console `001D1660` (13,753 B), dispatch table `001D4C1C` (dword RVAs), action ids 12–293. Every figure is
reproduced by `Tools/work/FABLE/ec7/arm_census.py`, `arm_floats.py` and `label_census.py`.

| figure | published here | re-derived | verdict |
|---|---|---|---|
| action ids / distinct targets / ids on the do-nothing arm `001D4BFA` | 282 / 227 / 56, all targets in the body | **282 / 227 / 56**, all in `001D1660`–`001D4C19` | **reproduced** |
| real arms that end with a `jmp 001D4BFA` (the common tail) | 212 of 226 | **212 of 226** | **reproduced** |
| references to `01F82D20` inside the arms | 24, all `mov reg, qword ptr [01F82D20]`, in 18 arms | **24 in 18 arms**, all 8-byte loads (19 into `rcx`, 4 `rax`, 1 `rbx`) | **reproduced** — a pointer slot, never nudged |
| labels at `ctx + 0x130 + id × 8` | 293 labels, ids 1–294, no collisions | the filler `001D0390` stores through `rdi` for **every id 1–294** (id 2's string is empty, so **293 non-empty**), no collisions, all displacements conforming — **and one more: id 298, `Super wide Mask Debug Enable :`** (`001D160D`) | **reproduced, plus one label outside the 294-row table** |
| stepping arms with one magnitude, and their magnitudes | "**102 of 102** stepping arms have this shape" (a direction-flag `test`, then `subss` / `addss` on the same constant); magnitudes 0.01 × 58, 0.02 × 11, 0.05 × 10, 0.1 × 9, 0.001 × 7, 0.03 × 3, 1.0 × 2, 0.005556 × 1, 0.5 × 1 | **102 arms and exactly those magnitudes — but only 55 have that shape.** The other **47 are signed pairs**: two `addss` on stored `+K` / `−K` constants, the direction chosen by which constant loads (D 25, E 21, G 1 — the "third mechanism" section below) | **population and magnitudes reproduced; the shape statement is wrong for 47 of the 102** |
| float-stepping ids, by mechanism | `FLOAT / CALL 104 / 69` and `SUB/ADD / ADD/ADD 55 / 47`, both **withdrawn** by this page pending re-derivation (History) | 110 ids use `addss` / `subss`. **109 step a float:** `SUB/ADD` one magnitude **58** (55 on a stored constant + ids 190–192 whose value travels through a getter / setter call), `SUB/ADD` mixed constants **1** (193), signed `ADD/ADD` **50** (47 on stored constant pairs + id 26, which loads `±1.0` into a register first, + ids 173 / 174, `movss` into `xmm7` and `addss xmm6, xmm7`). **Id 28 is not a stepper:** it multiplies three values by `0.2126` / `0.7152` / `0.0722` — the Rec.709 luma weights — inside the save / zero / restore toggle [slice A](arm-catalogue-slice-A-ids-12-43.md) describes | **the withdrawn totals are replaced by 109 steppers (58 + 1 + 50) and one non-stepper** |
| float-stepping ids per slice F / G | F 7, G 3 (slice documents) | **F 7** (173, 174, 189–193), **G 3** | **reproduced** |
| action ids by render-table outcome | 226 live · 38 read-outs · 12 labelled buttons without an action · 6 `(EMPTY)` | **not re-derived in this pass** — carried by [the command names](console-command-names.md), which cross the two tables | carried, not re-checked |

**`CALL 69` is not re-derived** either; the population definition behind it is not recoverable from the
published text and a count with an unstated selector is the thing this page's history warns about.

## 2. Falsification pass 2026-09-13 (FABLE)

**Attack chosen.** Every cross-slice figure was re-derived with new instruments: the dispatch table read
directly from `001D4C1C`; arm extents cut at the next distinct target, the do-nothing arm or the table;
float constants taken from every rip-relative `*ss` operand in an arm, not only from the operand of the
arithmetic; labels from the filler's own `lea` + `mov qword ptr [rdi + disp]` pairs.

**What survived:** the table figures, the tail count, the `01F82D20` correction, the label count, the 102
population and its nine magnitudes, and the per-slice float counts the slices themselves report.

**What did not:** (1) the banner's *shape* claim — 47 of the 102 one-magnitude steppers use signed
constant pairs, not a flag-tested `subss` / `addss`; the page's own later section had found the mechanism
without retracting the banner. (2) The float totals the page had withdrawn are now replaced, with the
selector stated: 109 steppers and one luma computation. **New:** a label for id 298 exists outside the
294-row table; which row, if any, renders it is not established.

**Controls.** The float classifier was run against the slice documents where they are authoritative — F's
seven arms and G's three are recovered exactly, including the register-only arithmetic of 173 / 174 that
defeated the first census twice — so the instrument is not blind to the encodings that broke the earlier
counts.

## History — the work order as it ran (2026-09-03, completed 282 of 282)

*Kept as written. The census above supersedes its counts where they differ; its rules, claims and
corrections are the record of how the catalogue was built.*

### The work order's original title: *Arm catalogue — work division*

> ## SLICES B-I ARE OPEN - hold cleared 2026-09-03
>
> **Two independent instruments, sharing no code and no method, measured the same three cells
> exactly: `addss +0.01` x58, `subss +0.01` x30, `addss -0.01` x28.** One counted constant references
> over the function body; the other walked the 282-entry dispatch table into its 227 arms. **The
> console is symmetric and the asymmetry was an extractor artefact.**
>
> **And the table walk supplied what a constant census cannot: 58/58 is FIFTY-EIGHT ARMS, not 58
> raise-commands and 58 lower-commands.**
>
> ```
> 001D1FB0  movss xmm0, [02CB8140]   ; the parameter
> 001D1FB8  test  bl, bl             ; the direction flag
> 001D1FBA  je    0x1d1fd1
> 001D1FBC  subss xmm0, [008F30E8]   ; 0.05 -> decrement
> 001D1FD1  addss xmm0, [008F30E8]   ; the SAME 0.05 -> increment
> ```
>
> **102 of 102 stepping arms have this shape.** So **the command id names the PARAMETER, not the
> direction** - which is why the row shape below records a magnitude and a mechanism.
>
> **Step magnitudes, per arm:** `0.01` x58, `0.02` x11, `0.05` x10, `0.1` x9, `0.001` x7, `0.03` x3,
> `1.0` x2, `0.005556` x1, `0.5` x1 - **102 arms.**
>
> **The two extractors have complementary blind spots and neither alone is complete.** The table walk
> finds 102 and the reference census 110; the walk's set is a strict subset. The 8 extras are real and
> differently shaped - one loads `+1.0`/`-1.0` **into the register** and does a single `addss` against
> the parameter (the reverse operand roles), another **computes** its step by dividing an integer by 5
> and scaling. **Together they account for all 110.**
>
> **Also reproduced exactly:** 282 entries, 227 distinct targets, 56 ids at the no-op, all targets
> inside the body.
>
> **One correction that changes how a slice reads its own data:** `001D4BFA` is not only the target of
> 56 unimplemented ids - **212 of the 226 real arms jump to it when they finish.** It is the
> function's common tail. **A reader told only that it is the no-op target will misread 212 jumps as
> 212 commands doing nothing.**


The console at `001D1660` dispatches **282 command ids (12–293)** through a table of image-base-relative
offsets at `001D4C1C`, to **227 distinct targets — 226 real arms plus one do-nothing arm at
`001D4BFA` shared by 56 ids.** The frame is established in
[the-282-command-parameter-console.md](the-282-command-parameter-console.md): the dispatch, the table
extent, the distribution of arm kinds, and the step constants.

**What is not established is what each arm tunes.** That is the remaining value, and it is the single
most parallelisable block in the database.

> **The distribution is measured; the individual targets are not.** 226 independent arms, each a few
> instructions, in a function whose frame is already read — so the expensive part is done and the rest
> divides cleanly.

## Why this is worth doing

It is **the richest catalogue in the binary of which addresses the developers thought were worth
tuning by hand.** An arm that walks a float by `0.01` is pointing at a value somebody sat and adjusted
while watching the screen — which makes each one a named, human-selected tuning parameter, and makes
the set of them a map of what the engine's authors considered adjustable.

## The division

**Nine slices: eight of 32 ids and one of 26.** Each is independent: an id range, its table entries, and the arm bodies
they reach. **Take a slice by claiming its letter.**

| slice | command ids | ids | table byte extent at `001D4C1C` |
|---|---|---:|---|
| A | 12–43 | 32 | `+0x000` … `+0x07F` |
| B | 44–75 | 32 | `+0x080` … `+0x0FF` |
| C | 76–107 | 32 | `+0x100` … `+0x17F` |
| D | 108–139 | 32 | `+0x180` … `+0x1FF` |
| E | 140–171 | 32 | `+0x200` … `+0x27F` |
| F | 172–203 | 32 | `+0x280` … `+0x2FF` |
| G | 204–235 | 32 | `+0x300` … `+0x37F` |
| H | 236–267 | 32 | `+0x380` … `+0x3FF` |
| I | 268–293 | 26 | `+0x400` … `+0x467` |

**Checked: 32×8 + 26 = 282 ids, and the last byte is `+0x467` = 282×4 − 1.** The extents are byte
ranges throughout — the first draft of this table mixed *entry starts* for A–H with a *byte extent*
for I, which is the units inconsistency this session has logged seven times in other people's work
and which is no more acceptable in a work order than in a document.

Table entry for id *n* is the dword at `001D4C1C + (n − 12) × 4`, holding an **RVA**: add the image
base `0x00120000` to get the arm address.

## The extraction exists — start from it, and distrust one column

All 282 rows are extracted to `Tools/work/repos-d2/console_arms.tsv` as
`id / arm / kind / step / data_touched / calls`. **Start there rather than from the table.**

**`kind` is sound and reproduces the published distribution**: nudge 110, call 63, unimplemented 56,
other 32, flag 21. It rests only on whether `addss`/`subss` appears in the arm.

**`step` is INDICATIVE AND NOT VERIFIED PER ROW — re-derive it for every arm you touch.** It records
the first float operand of an `addss`/`subss`/`movss`/`mulss` and signs it by the mnemonic, so an arm
that loads one constant and steps by another is mis-valued. **The tell is in the data itself: 58 rows
read `-0.01` and none reads `+0.01`**, which is not plausible for a console with up/down pairs, and
only 3 of 88 nudged addresses show both directions.

> **That is a limitation of the extractor, not a fact about the data.** The up/down pairing is almost
> certainly there and the column is not showing it. **The author labelled it unreliable rather than
> handing over a clean-looking number — a handoff artifact that overstates itself is worse than none.**

## What the extraction found that no single arm could

**The arms touch 97 distinct `.data` addresses, and 86 fall in one span** — `02CB7FD0`–`02CB8438`,
1,132 bytes, **81 of the 85 gaps exactly 4 bytes.** A densely packed array of 4-byte values in the
zero-filled tail of `.data`, built at run time.

**And it is not the console's scratch space: twenty-eight functions reference that span** — the console
and twenty-seven others.

> **So the commands adjust values the engine is already reading elsewhere. That is what makes this a
> tuning console rather than a debug display**, and it is a fact no per-arm reading could have
> produced.

The hottest single address is `01F82D20`, nudged by **18** different commands.

## The arms mostly do NOT touch globals — read slice A before starting

**Slice A found the shape, and it changes what a row should contain.** The arms tune **fields of a
settings object through `rdi`**, not globals: `add dword ptr [rdi + 0xDA0], ebp` with the direction
taken from `test bl,bl ; cmovne`. **Slice A touches 26 distinct fields and only four or five ids touch
a global at all.**

**Measured across the whole extraction, which qualifies the span finding above:**

```
rows                              282
with a data_touched value         112   (40 %)
without one                       170   (60 %)
of slice A's 32 ids, with one       5
rows touching 02CBxxxx              86
```

> **So the 86-in-one-span figure is 86 of the 97 distinct addresses and 86 of the 112 rows that touch
> data at all — not 86 of 282 arms.** Sixty per cent of the arms touch no global whatever, because
> they are writing through the context pointer. **The span finding stands; its population needed
> stating.** A count is only as wide as its selector, and this one had two plausible denominators.

**What a row is actually worth is therefore `field · width · step · bound`** — and **the bound is
where the authored intent survives not knowing what the field is**:

```
id 14   d+0xC20   increments and WRAPS AT 3      a three-state mode cycle
id 19   d+0xDA0   +/-1, CAPPED AT 0x12           nineteen positions
id 21   d+0xC44   +/-1, FLOORED AT 0
id 43   d+0xC04   +/-1, bounds 2 and 0x13
id 29   b+0xC71   cmp/sete/mov                   a boolean toggle
```

**The settings object is not identified**, and slice A says so rather than working around it. `rdi` is
the console's own context pointer and nothing in that slice names it or its type. **Twenty-six offsets
with their bounds is still the catalogue, because the bound is the part somebody chose.**

**`verify_doc_addresses` returns REVIEW on `001D4C1C` and on every arm address.** Both are legitimate
and dispositioned in slice A's §8: the first is the dispatch table in `.text` after the function, and
**switch arms are interior addresses of the function, not functions.** Do not re-derive it per slice.

## What a slice delivers

For each id in the slice, a row:

> **`id · arm address · field · width · step MAGNITUDE · direction mechanism · bound`**

**The magnitude is the invariant; the sign is not a property of the arm.** Every stepping arm
holds both directions - `addss`/`subss` on one constant in the float arms, `test bl,bl ; cmovne`
selecting `+1`/`-1` in the integer arms - so **a row that records "a step" has already lost the
thing that makes it a console.** Record the mechanism that chooses, not one branch of it. Rows for ids landing on `001D4BFA` say **do-nothing** and stop there — 56 of the
282 do, and they are gaps in a tool edited over years, not work.

## Rules for this block, all earned this session

- **Name the target, not the arm.** An arm that adds `0.01` to a float at some address is only
  interesting because of what that address *is*. If the address cannot be identified, say so — **an
  honest unknown is a complete row.**
- **Do not characterise the console from your slice.** Thirty-two arms is not 226. The whole document
  exists because one inviting command out of ~250 nearly named the system, and **a slice is exactly
  the position from which that mistake is easiest to make.** State what your slice contains; the
  distribution is already measured elsewhere.
- **Cite by address only what you have accounted for.** A shared singleton — `001A9930` is used by 45
  arms, `00193D50` by 33 — is a hub, and citing it by address commits your rows to its whole
  neighbourhood. **Name it; do not cite it.**
- **Any absence claim needs a known-positive control chosen before the scan.** If a slice reports "no
  arm in this range touches X", the scan must first find something you already know is there.

## Claimed

| slice | ids | session | state | verified against |
|---|---|---|---|---|
| A | 12–43 | repos-78 | **delivered**, re-run under the corrected row shape | GN158 |
| B | 44–75 | repos-78 | **delivered** | GN158 |
| C | 76–107 | repos-78 | **delivered** | GN159 |
| D | 108–139 | repos-78 | **delivered** | GN159 |
| E | 140–171 | repos-2d | **delivered** | GN159 |
| F | 172–203 | repos-78 | **delivered** | GN159 |
| G | 204–235 | repos-78 | **delivered** | GN159 |
| H | 236–267 | offered to repos-d2 | **offered, awaiting reply** | — |
| I | 268–293 | repos-78 | claimed | — |


> **CLAIM PROTOCOL — read this table before answering a claim, and write to it when you approve one.**
>
> On 2026-09-03 two sessions were approved for slice C within minutes of each other, because the
> coordinator answered a claim without consulting this table and did not update it on approval.
> **Fourth routing collision of the run.**
>
> **A claims table is only a coordination device if it is consulted before the answer and written on
> the answer.** Otherwise it is documentation of collisions after the fact — which is what it had been
> until this line was added.

**96 of 282 ids catalogued; 186 remain.**

### A slice is stamped with the parent it was checked against, not the current one

Slices A and B read `GN158` and **stay that way.** Their evidence is tier-1 off the EXE, whose sha is
unchanged by the batch, so nothing in them depends on it — **but re-stamping to GN159 would assert a
check that was not run.**

> **A stamp records the state a check ran against. Bumping it because the parent moved is the status
> field asserting a check that never happened**, which is the defect this project has now corrected
> three times in three different fields. **The session flagged it rather than quietly bumping it, and
> that was right.**

### Every slice so far has contained something the previous slice's extractor would have mis-typed

> **A was counters. B was floats. C was floats plus a multiplicative arm, a re-seeder and two
> clamps.**

**Three slices, three shapes.** *"Does the arm shape hold here at all"* is now evidence-backed as the
correct first question for every remaining slice, and **inheriting the previous slice's extractor is
the specific thing not to do.**


## Corrections to this work order, 2026-09-03

**`01F82D20` is a pointer slot and is never nudged.** This document called it *"the hottest single
address, nudged by 18 different commands."* Re-derived over all 227 arms:

```
24 references inside the arms - ALL `mov <reg>, qword ptr [01F82D20]`, in 18 distinct arms
 0 references that read or write it as a 4-byte float
```

**The count of 18 is right and the operation is not.** It is an **8-byte pointer** that 18 arms
dereference to reach fields of the object behind it — id 134 steps the dword at its `+0x40`.

> **A `data_touched` column cannot separate an 8-byte pointer load from a 4-byte float nudge**, which
> is how a pointer became the most-nudged address in the binary. *Control:* the same scan does find
> float-shaped references — `01F82ED0`, sixteen bytes further into the same region, is read and
> written as a float.

**Both corrections are to figures this work order published**, and both came from a slice re-deriving
the frame rather than consuming it.


## THE PARAMETERS ARE NAMED — read this before writing another row

**The console names its own parameters.** The row renderer prints `"%s%s%f"` with the label from
`[ctx + id*8 + 0x130]`, filled one `lea`+`mov` at a time, so **`id = (disp - 0x130) / 8`.**

> **293 labels, ids 1-294, zero collisions, zero non-conforming stores. All 282 action ids have one.**

**Every slice's targets can be named.** `Tools/work/repos-2d/console_labels.tsv` carries all 294 rows.

> **"Name the target, not the arm" was right; what it needed was a second table, not a better reading
> of the first.** Slices A-D reported bare addresses because an arm never names its field — **and the
> arm was never the only place to look.**

**Id 14** — slice A's wrap-at-3 counter — is **`Invincible:`**. **Id 103** is
**`Camera Over Write (O to capture)`** and 104/105/106 are **FOV / Aspect Ratio / Camera scale**, so
**the ratio-stepping arm is the one called "scale"** — the label explaining a mechanism the
disassembly had already given.

**Alignment is proven four ways, not assumed:** the dispatcher's own `add r9d,-0xC` / `cmp r9d,0x119`;
id 103's label against slice C's capture behaviour; the clamped Ambient pairs in C and E; and
`lea eax,[r13-0xF7]` drawing a stride-12 stat array. **Cross-source control: 20 arm-bearing pairs
against the config keys, 0 contradictions.**

**Propagation to the delivered slices A-D is a separate pass**, so the label source is one decision
recorded once rather than four sessions each deciding what a label licenses.

## "56 unimplemented" retired — it is three different outcomes

**There are two tables**: action (282 ids, base 12) and render (294 ids, base 1). Crossed over all
294:

```
226  live
 38  no action, but still SHOW a live value   (read-outs: Current LP, twelve character stats)
 12  labelled buttons with the action removed
  6  draw "  (EMPTY)  "                        (ids 211-216)
```

> **Unreachable in one table says nothing about how the other table draws you. Only six rows of 282
> are actually blank in the menu.**

## A third direction mechanism, and it is concentrated

**21-25 float arms use `addss`/`addss` with a stored NEGATIVE constant** — direction is *which
constant loads*, not which mnemonic runs.

```
per slice:  A 0 · B 0 · C 0 · D 25 · E 21 · F 0 · G 1 · I 0
```

**A `subss`-keyed classifier finds no decrement in them; a mnemonic-signed one reads two increments.**

**~~Slice D needs this correction.~~ RETRACTED — D had it first, and had it as the headline.** D's §2
table, written at delivery, reads `signed pair, addss (−K) down / addss (+K) up : 25`, with 25
catalogue rows carrying it, and D's own summary says *"the dominant encoding here is not the one B and
C are made of."* **The census rediscovered a slice's headline finding and I relayed it back to its
author as a correction.** Merging it as written would have republished a confirmation as a discovery.

**Corrected within the hour, by its own author.** The first count said `F 0 · G 0` and that the
mechanism was confined to D and E. Id 217 in G uses it, so it is **rarer outside D and E than stated,
not absent** — and the same pass found **id 189, "Navi Map Scale", is a float stepper that slice F had
already typed correctly** as *"float step via a getter/setter pair"*. The classifier required a `movss`
load; 189 and 217 take their value as a **function return**, step it in `xmm6`, and push it back
through a setter.

```asm
001D4006  call 0x2deba0            ; getter -> xmm0     (id 217)
001D400F  addss xmm0, [00900308]   ; -0.1
001D4017  call 0x2df2a0            ; setter
```

| | first reported | correct |
|---|---:|---:|
| FLOAT / CALL, ids 12–293 | 102 / 71 | **104 / 69** |
| `SUB/ADD` / `ADD/ADD` | 54 / 46 | **55 / 47** |
| slice F floats | 0 | **7** — *see below; the "1" was also wrong* |
| slice G floats | 2 | **3** (id 217) |

**And the corrected number was wrong too, by the defect it was correcting.** F documents **seven**
float-stepping arms — 173, 174, 189, 190, 191, 192, 193. **Ids 190–193 are the exact shape the repair
was aimed at** (value in by `call`, stepped in a register, out by `call`), and the repair caught one of
the five. **173 and 174 need a further case: the constant is `movss`-ed into `xmm7` and applied as
`addss xmm6, xmm7`, so there is no memory operand on the arithmetic at all.**

> **The census still requires either a `movss` or a memory operand on the `addss`. That is the same
> defect a third time, inside its own repair** — the fix was aimed at one *encoding of the exception*
> instead of at the *requirement that produced it*. It does not dent the four-instruments finding; it
> is the strongest instance of it, because it happened to someone who had just written the rule down.

**`FLOAT/CALL 104/69` and `SUB/ADD vs ADD/ADD 55/47` are therefore withdrawn, not corrected.** They
rest on the same requirement and are wrong by an unknown amount in a known direction — **too few
floats.** They must be re-derived by the census owner against the seven slice documents, which are the
authority here; **a coordinator patching a census he cannot re-derive is how a wrong total survives a
correction.**

**Attribution:** the name *"Navi Map Scale"* for id 189 comes from the label table, not from F's read.
It goes in with that attribution or not at all.

> **Requiring a `movss` to recognise a float step is the same species of mistake as requiring a
> `subss` to recognise a decrement: an extractor keyed on the common encoding of a thing, reporting
> the absence of the thing.** Three instances now, and the rule is stable enough to state:
> **check what your classifier requires, not just what it matches.**

**And the thing that stopped it becoming a false accusation against a delivered slice: its author read
F's text before reporting.** F was right and the instrument was wrong. **When your instrument disagrees
with a delivered document, read the document first.**

## `02CB7FD0` is a `this` pointer, not a global

Passed by `lea rcx` to a constructor, **so every `02CBxxxx` field is `this + offset` and the
constructors hold a shipped default for each** — `SSS enable` = 1, `SSS Width` = 7.0.

**Two decoding traps, both of which bit their finder first:**

- **Width must come from the store.** Merging three constructors produced *"Fresnel Enabled = 3.9"*
  for a one-byte boolean — **a boolean that cannot be 3.9 is what caught it.** Same species as the RGB
  triple: a fact about the subject matter the instrument had no access to.
- **`mov qword ptr [x], imm32` is two adjacent 4-byte fields**, not one.

## H delivered — 282 of 282, and the prediction failed

**The table is closed.** Nine slices, five sessions, every action id catalogued.

### The prediction failed, and its author reported it failing

Slice I recorded properties **11, 14, 16, 19, 20, 21** as *unreached, not absent*, and predicted H
would hold them. **H holds none of the six.** Its only two arms touching `01F82D20` — ids 263 "Game
Window Mode" and 264 "Game Display Resolution" — read `+0x08` and **never call the property setter**,
going through `00182DE0`/`00182E10` instead.

**The answer came from scanning all 282 ids rather than only the slice:**

| | |
|---|---|
| arms referencing `01F82D20` | **18** — D 1 · E 1 · H 2 · I 14 |
| rule `offset/4 == property` | **14 agreements, 0 disagreements** |
| **14** | id 166 "Use soft particle" — **slice E** |
| **16** | id 134 "Water Quality" — **slice D** |
| **11, 19, 20, 21** | reached by **no arm anywhere**: `+0x2C`, `+0x4C`, `+0x50`, `+0x54` |

Id 166 passes `edx = 0xE` for field `+0x38`, and `0x38/4 = 14` — **extracted in slice E before slice
I's rule existed.** So the two-slice corroboration arrived, from the two slices nobody named.

> **The failure is worth more than the success would have been.** Finding 14 and 16 elsewhere while
> finding 11/19/20/21 in *nothing* separates **"H has not been read yet"** from **"no arm anywhere
> touches these."** The object has **at least 23 dword properties and the menu reaches 17** — four
> fields the console does not expose, which a confirmed prediction would have left invisible.

### Two counts disagreed and both were right

The cross-arm check reproduced exactly: **21 jump sites, 14 distinct arms.** Ids 177 and 180 contain
three such jumps each; 190, 192 and 279 two each.

> **A disagreement between two careful counts is usually a disagreement about the population.**

**And the "second shared tail" was wrong.** `001D4B49` is not a tail — it is **one arm, id 281
"Glare", entered at three different offsets**: `4B59` compute the flag and call, `4B60` call only,
`4B65` do the property-3 call and exit. **Nine ids across D, E and I enter it.** H itself has **zero
crossers**; all 16 of its arms exit to `001D4BFA`.

**The short-arm heuristic paid on contact:** ids 276 and 280 set their property numbers with
`lea edx,[rsi+0xF]` and `lea edx,[rsi+0xC]` — properties **15 and 12**, both `offset/4` — then jump
in. **Invisible unless the jump is followed.**

### What H adds that no earlier slice contained

- **Step magnitude is not constant.** Ids 238–242 step by **1 or 10**, chosen by a per-counter
  modifier flag (`mov ebp,1` / `lea edx,[rbp+9]` / `cmovne`), over five stride-8 value/flag pairs.
  **"Magnitude 1" and "magnitude 10" are both wrong cells; the honest one is `1 or 10` and where the
  choice comes from** — the row shape's first genuine widening since it was fixed.
- **The "Enable 100 % successful" rows are not toggles.** Steal cycles `−1,0,1,2`; poach `−1,0,1`;
  drop `−1,0,1,2,3`. **Three different state counts for three adjacent rows with near-identical
  labels.** A label saying *"Enable X"* and an arm cycling five states disagree, **and the arm wins.**
- **Id 266 "System Adapter" is a two-level cursor** — steps a monitor index, carries into an adapter
  index, re-queries the count after each carry.
- **Id 265 "Game Monitor" tests neither direction** and writes the current value back — a **fourth**
  independent retirement of "the direction flag".
- **Id 264 refuses to act unless id 263's window mode is ≤ 1** — a dependency between two rows that
  **neither label mentions**, and the first cross-row dependency in the table.

**H's 18 do-nothing arms: 15 still draw a live value, 3 are label-only, 0 draw `(EMPTY)`.** The
strongest case yet for the two-table correction — a slice-local reading reports a page of dead rows;
what is actually there is **a working character inspector with its editing removed.**

### Fourth and fifth instance, volunteered

The property scan keyed on `mov edx, imm` and missed `lea edx,[rsi+imm]`; **the fix still missed it**,
because `xor esi,esi` registers as `esi` while the `lea` base reads `rsi`. After `subss` and `movss`,

> **it is no longer coincidence** — and it was reported by its author as *"I would rather it be counted
> against my instruments than quietly fixed."*

### G amendment — recorded here, not folded into G

- **Ids 225/226 are 8-digit decimal editors, not steppers.** A cursor at `rdi+0xDD8` selects a digit
  in an 8-dword array at `+0xDB8`; left/right step that digit, `add 0xA` and a mod-10 wrap it 0–9, and
  the composite is recomposed into `+0xDB4` by **Horner's method**. Id 226 is the same shape at
  `+0xDE4`/`+0xE04`/`+0xDE0`.
- **Id 227 "Set play time" is an h:mm:ss editor** — `+0xE14` picks the field; minutes and seconds wrap
  mod 60, **hours wrap mod a runtime value at `+0xE18`**; the down path adds 59 before the mod so
  −1 becomes 59.
- **Ids 205–207 respond identically to both directions**, then push to channels **1, 3, 2** — not menu
  order. H's id 260 pushes one value to channels **1, 2, 3**, so the channel set is consistent and
  **only 205–207's ordering is odd.**

*(Pass 22 adjacency, 2026-09-14: the dispatcher `001D1660` the division table routes around calls
**audio** `002DEBA0`/`001DBB00` and **resource** `002EEEE0`, and the accessor `00193D50` is called
by resource `001A7A50` — 4 edges, all belonging to the shared machinery every slice cites.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE, 32 edges.** Most come from two small shared helpers the work division cites (8 bytes with 11 Presentation neighbours, 66 bytes with 9). The console body itself has 3, and a 4,812-byte arm body 2.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Input — CLIENT (1 edges, one fan-in).** All 1 edges are Input bodies reaching `00182DE0` on this page. `FUN_0079c140` is the worked example - it is a 1,404-byte routine that does nothing at all unless `byte[+0x20]` of its argument is set, in a `0x40`-byte frame with an unwind marker. The crossing is **one shared subject with 1 callers on that layer**, not 1 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Application — MECHANICAL (SWE2-EC7-35, 1 edge).** `00584740` — the shared CRT helper this page cites inside `001EA3C0` — is called by a body on the Application layer. Shared-helper fan-in; no application relationship to the work division.

**Platform — MECHANICAL (SWE2-EC7-35, 1 edge).** `00584740` is also called by a body on the Platform layer. Same shared-helper fan-in.

**PlatformOnlineAchievements — MECHANICAL (SWE2-EC7-35, 1 edge).** `00796E20` — the other shared callee `001EA3C0` names — is called by a body on the PlatformOnlineAchievements layer. Same shared-helper fan-in.
- **WorldAreaField — CLIENT (1 edge).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `002DEBA0`). Substantive edges include `002DEBA0` is called by `World_UpdateSimulationTick` (00314020).
## The `001D0390` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`001D0390` is the label filler this page counts 293 non-empty labels
through: `001EA3C0`/`001EAC30`/member `002F79E0` (`001D03CA`–
`001D03DC`), `dword[rdi+0xAE4] = "OFF\0"` (`001D03E1`), then the
`movsd`/`movzx` string stores — `"Black Hole"` → `+0xB0C`/`+0xB0E`
(`001D03EB`–`001D0410`), `"Luminescence"`/`"ence"` → `+0xB2C`/
`+0xB30` (`001D0416`–`001D0439`), `"Ark Blast"` → `+0xB4C`
(`001D043F`), `"Whiteout"` → `+0xB6C` (`001D045D`), …

| member | role | interior |
| --- | --- | --- |
| `002F79E0` (17 B) | 16-byte constant copy — `movdqa` `00D0F9E0` → `movdqu` `022BE930` (`002F79E0`/`002F79E8`) | [`002F79E8`](../../_index/ADDRESS-INDEX.md) |
| `001EAC50` (7 B) | dword setter — `dword[rcx+0xEC] = edx; ret` | [`001EAC50`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001EA3C0`, `001EAC30`. The sibling
`002F7A00` body (`dword[01EEBAF0] = ecx`) is adjacent, not a member.

## SWE2-EC7-35 update (2026-09-19) - `001EA3C0`

`001EA3C0` (763 B) is a work-division body - `01DFDE00`/`02E3FA60`/`00901B18`/`00901B28`, `00796E20`/`00796350`/`00584740` pairs plus the `0067C5A0`/`0067C310`/`0067BD50` family. Interior anchor `001EA3F1` (a `00796E20` call).

## SWE2-EC7-54 update (2026-09-19) - `0067C310`

`0067C310` (289 B) is a work-division body - `005CDAA0`/`00671B10`/`00671B20`/`00672B80`/`00672C70` plus `00D6CFD0`/`00D6D020` rdata. Interior anchor `0067C35E` (a `00671B10` call).

## SWE2-EC7-56 update (2026-09-19) - `00672B80`

`00672B80` (226 B) is a work-division body - `00584730`/`0066F7F0`/`00673780`/`00674230`. Interior anchor `00672BA2` (a `00674230` call).


## SWE2-EC7-56 update (2026-09-19) - `00672C70`

`00672C70` (226 B) is a work-division body - `00584730`/`0066F8B0`/`006737F0`/`00674420`. Interior anchor `00672C92` (a `00674420` call).


## SWE2-EC7-56 update (2026-09-19) - `0067BD50`

`0067BD50` (191 B) is a call-free intrusive-list predicate scan - `r9` chain against `02CB6B80`, `[rax+0x78]` next links, `[r9+0x74]` count check. Interior anchor `0067BD95` (the `+0x78` next load).

## SWE2-EC7-57 update (2026-09-19) - `00674420`

`00674420` (494 B) is the index-data-block unbind the work-division page names - `00584730`/`005CDAA0`/`0062EC70`/`006737F0` plus three vcalls, `"Trying to unbind an index data block"` literal. Interior anchor `0067443B` (a `005CDAA0` call).


## SWE2-EC7-57 update (2026-09-19) - `0066F7F0`

`0066F7F0` (181 B) is a work-division body - `0017D260`/`00661720` plus `00D68DD0`. Interior anchor `0066F82A` (a `0017D260` call).


## SWE2-EC7-57 update (2026-09-19) - `0066F8B0`

`0066F8B0` (181 B) is a work-division body - `0017D260`/`006618A0` plus `00D68DE0`. Interior anchor `0066F8EA` (a `0017D260` call).

