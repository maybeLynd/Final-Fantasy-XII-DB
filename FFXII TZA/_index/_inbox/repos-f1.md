# repos-f1 — block 3: the 41 path-dependent verbs

*(Block 2 merged by repos-55 on 2026-09-02. Everything below is new.)*

Same program state: `GN158`, snapshot `46f02e26…bbbb2`, EXE `73461d08…721f8`, project
`Tools\work\proj_hf1` / `GFZ_HF1`. No mutation. No `_index/*.md` edited. `check_links` green
(168 files, 794 links). `verify_doc_addresses` green — 96 cited addresses in the verb document, 0
unresolved.

**The answer to the question you set: a real design feature, and there are two of them, unrelated.
Neither is a measurement artefact.**

---

## COVERAGE

`Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md` — `DOCUMENTED`, **3 falsification
passes**. New §12. `scriptvm-verb-table.tsv` regenerated with two new columns (`guard`,
`net_or_sums`) and a new status value (`GUARDED`).

| | block 1 (§10) | block 2 (§11) | block 3 (§12) |
|---|---:|---:|---:|
| rows with a measured arity | 76 | 1,691 | **1,870** of 1,960 |
| named + declared, measured | 76 | 1,091 | **1,210** |
| agreement with the authored count | 75 (98.7 %) | 1,090 (99.91 %) | **1,209 (99.92 %)** |
| delta histogram | `0`, `−2` | `0`, `−2` | **`0`, `−2`** |
| rows with no arity evidence | 646 | 117 | **90** |

**Three passes, three samples — 76, 1,091, 1,210 — and the delta histogram has contained exactly two
values every time:** `0`, and the `−2` of `unkCall_5c7` whose handler is the shared `ret 0`. A
sixteen-fold growth in sample has produced no new disagreement.

Status distribution in the table: `CONFIRMED` 1,184 · `DERIVED` 632 · `GUARDED` 34 ·
`DERIVED-UNNAMED` 19 · `LOWER-BOUND` 33 · `UNPROVEN` 57 · `CONFLICT` 1.

---

## OPEN-QUESTIONS

| ID | Disposition |
|---|---|
| **BQ-7** | **CLOSED.** 1,870 of 1,960 rows measured; 1,209/1,210 agree. The 41 path-dependent rows resolved into two mechanisms (below), not a measurement limit. |
| **BQ-4** | **ANSWERED — genuinely zero-argument.** All seven `*sync` verbs measure net 0 and are `CONFIRMED` against a declared 0. The push-then-pop round trip is no longer purposeless: §12 proves handlers hand arguments to one another *through the value stack*, and the round trip is that same hand-off with producer and consumer inlined into one function and the argument a compile-time constant. |
| **BQ-9** *(new)* | The **90 rows still without a measured arity**: 33 command slots with no callback at all, 31 whose operand reads sit inside a loop or whose CFG exceeded the path budget, 26 whose handler calls a function whose own stack effect is not exactly known. Each needs a body read; **none is blocked on the instrument.** |
| **BQ-10** *(new)* | Whether a script can issue a family-7 `fsmenu_*` verb while the menu object `*(*(void**)0x0209AC30 + 0xC0)` is null. If it can, the verb's operands are **left on the value stack** (§12). Killer observation: find a shipped `.ebp` calling a family-7 verb outside a fullscreen-menu sequence, or find the code that guarantees it cannot. |
| **BQ-1..BQ-3, BQ-5, BQ-6** | Unchanged, still OPEN. Document §7 now uses the merged `BQ-n` ids rather than `PROPOSED-repos-f1-n`. |

### The ledger half of my edits — I cannot make these, `_index` is yours

I ticked `BQ-4` and `BQ-7` in §7 of the verb document, so `check_questions.py` now reports them as
**EARLY** until the ledger rows change. The rows should read:

- **`BQ-4`** → **ANSWERED 2026-09-02.** Genuinely zero-argument. All seven `*sync` verbs measure net
  0 and are `CONFIRMED` against a declared 0. The push-then-pop round trip is the *inlined* form of
  the verb-to-verb stack hand-off proved in §12, with the argument a compile-time constant.
- **`BQ-7`** → **CLOSED 2026-09-02.** 1,870 of 1,960 rows carry a measured arity; 1,209 of the 1,210
  the catalog also declares agree — 99.92 %, delta histogram `{0: 1209, −2: 1}`. The 41
  path-dependent rows resolved into two mechanisms, not a measurement limit. Residue moved to BQ-9.
- **`BQ-9`** and **`BQ-10`** are new rows (text in the table above).

Also: **`BH-6` no longer resolves.** The prefix rename to `BQ` reached the verb document but not the
interpreter document, which still cited `BH-6`; I have corrected it to `BQ-6` there and `BH-5` →
`BQ-5` in the lifecycle document, so `ids cited by a document with NO row in the table` should drop
from 2 to 1 (`BQ-9`, until you file it).

**Not mine:** the two `STALE` findings are `input-stack-device-channel-and-bindings.md` (AP-1, AP-3).
None of my four documents appears in the drift report other than the two ticks above.

---

## AUDIT-LOG

### 2026-09-02 — repos-f1 block 3: the path-dependent verbs are two mechanisms, both real

**Attack chosen.** §11 left 41 rows whose net value-stack effect differs between execution paths.
Either an optional-argument convention the authored catalog cannot express, or a defect not yet
found. **Neither guess was right.**

**Mechanism 1 — handlers hand arguments to each other over the value stack (7 rows).**
`setentrypos` (`0x0405`, `00354FB0`) pops one index, looks the entry up, **pushes four floats** and
calls `00350510` — which is the `result` callback of **`0x0019 setpos_19`, declared with four
arguments**. The verb is literally *"look up that entry's position, then do `setpos_19` with it"*,
and the four values travel over the same operand stack a script would have used. `ucsetpos`
(`0x0168`, `0034F800`) does it by tail jump into **`0034EBC0`, `0x0001 setpos`'s handler (three
arguments)**, or drains three floats when its target does not resolve. Folding callees whose net is
itself exactly known — a fixpoint over 1,912 candidates, 1,816 resolving — took exactly-measured rows
from 1,691 to 1,836 and cut the "callee net unknown" category **from 164 to 26**. (You said to leave
the 164; this is the narrow version needed to answer the assigned question, and it collapsed most of
them as a side effect.)

**This closes BQ-4.** The seven `*sync` push-then-pop round trips are the same hand-off inlined, with
a constant argument. All seven measure 0 against a declared 0.

**Mechanism 2 — the fullscreen menu bails out without reading its operands (34 rows).**
All 34 have `sums = [0, N]`. Thirty-two share one 20-byte predicate:

```c
FUN_00280120:  return *(u64 *)(*(void **)0x0209AC30 + 0xC0) == 0;   /* menu object absent */
```

and open `call 0x280120 ; test eax,eax ; jne <return>` — **bail without reading anything.** It is
family 7's standard prologue, on **65 of its 131 callbacks**; it only produces a path-dependent arity
on the 33 records that have operands to read. Family 7's records come in exactly four shapes:
`(—,—,guarded)` ×20, `(guarded,guarded,—)` ×22, `(—,—,plain)` ×54, `(plain,plain,—)` ×5 — so a
guarded **durative** verb guards both `begin` and `poll` and has **no `result` at all**.

**The decisive check: `min(sums) == 0` on all 34, and `max(sums)` equals the declared count on all 25
that declare one — 25/25, zero mismatches.** So the arity is not path-dependent: the verb takes N
arguments and there is a path on which it takes none of them. **A guard, not an optional-argument
convention.** The 34th row, `unkCall_3092` in family 3, has the identical shape with its own
predicate (`FUN_002E9A30`), so the pattern is not unique to the menu.

**The consequence, stated as an implication and not as a fact.** On the bail path the operands are
not consumed, nothing later in the sequence takes them (a guarded durative verb has no `result`), and
the executor's own action after `result` is to **push** — the return value, or integer `0` when there
is no `result` callback (`00262360`). Against a 63-slot stack whose pushes silently drop when full,
that is an operand leak. **Whether it is reachable is not claimed** — it needs a script to call an
`fsmenu_*` verb while the menu object is null. Killer observation named and filed as **BQ-10**.

**What did not break.** Base, stride, extent, the family tables, the three-callback layout, the
parameter encoding, both anchors and the delta histogram all re-derived and unchanged. This pass
added no correction to a previous claim — the first block in this run that did not.

**Method note.** Three passes at three sample sizes, each time asking whether the *disagreements*
were the table's fault or the instrument's. Passes 1 and 2 found the instrument at fault four times.
Pass 3 found the instrument sound and the *binary* interesting — which is what the earlier fixes were
for. The rule held throughout: **an aggregate cannot report its own bias; only the rows that disagree
with an independent source can.**

### Structural changes

None. `scriptvm-verb-table.tsv` regenerated in place: new `guard` column (`fsmenu` / `other` /
blank), `net_or_sums` (a single net, or `0|N` for a guarded verb), and the `GUARDED` status value.

---

## CALL-CHAINS / ADDRESS-INDEX

### CALL-CHAINS — a new cross-verb transition class

```
script issues setentrypos(entryIndex)        id 0x0405
  -> result 00354FB0
     -> pop the index
     -> FUN_003DFD00(0, idx, &out)           entry-table lookup -> 4 floats
     -> PUSH out[0..3] onto the VM value stack
        -> FUN_00350510  =  the result callback of 0x0019 setpos_19   *** VERB-TO-VERB ***
           -> pops the four values it was just handed

script issues ucsetpos(x, y, z)              id 0x0168
  -> result 0034F800
     -> resolve the target; if it resolves, TAIL JUMP into
        0034EBC0  =  the result callback of 0x0001 setpos
     -> otherwise drain three floats and do nothing
```

**This is a call-chain class the database did not have: one script verb reaching another verb's
native handler, with the operand stack as the calling convention.** Not a wrapper and not a shared
helper — the callee is a fully-fledged verb in the same table.

### ADDRESS-INDEX — new entries

| Address | Name | Body | Document |
|---|---|---:|---|
| `00280120` | fullscreen-menu absent predicate — family 7's standard guard, 65 of 131 callbacks | 20 B | Verb-Dispatch §12 |
| `0x0209AC30` | pointer to the context whose `+0xC0` holds the fullscreen-menu object | — | Verb-Dispatch §12 |
| `00354FB0` | `setentrypos` handler — pushes four floats and calls `setpos_19`'s handler | 167 B | Verb-Dispatch §12 |
| `0034F800` | `ucsetpos` handler — tail jumps into `setpos`'s handler, or drains three floats | 112 B | Verb-Dispatch §12 |
| `00350510` | `0x0019 setpos_19` result callback — arity 4 | — | Verb-Dispatch §12 |
| `0034EBC0` | `0x0001 setpos` result callback — arity 3 | — | Verb-Dispatch §12 |
| `00511510` | `fsmenu_setslot` result callback — the shortest guarded handler | 44 B | Verb-Dispatch §12 |
| `0050F6E0` | `unkCall_3092` begin — the one non-`fsmenu` guarded verb (`FUN_002E9A30`) | 302 B | Verb-Dispatch §12 |

---
---

# repos-f1 — block 4: B-4, the 585 intentionally ownerless functions

*(Appended, not overwritten — `repos-f1.md` was being edited concurrently while this was written.
Block 3 above is merged and can be deleted.)*

Same program state: `GN158`, snapshot `46f02e26…bbbb2`, EXE `73461d08…721f8`, project
`Tools\work\proj_hf1` / `GFZ_HF1`. No mutation. No `_index/*.md` edited. `check_links` green
(171 files, 821 links). `verify_doc_addresses` green on the new document — 39 cited, 0 unresolved.

**B-4 answered: EARNED, not inherited.** Three independent measurements, each against controls, and
three named exceptions in the sub-labels — none in the ownership decision itself.

New document:
[`../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md)
— `DOCUMENTED`, tier 1, one falsification pass.

**Placement, and why it is not in 24.** **Zero of the 585 carry a `CompilerGenerated` / `Microsoft` /
`Thunk` CodeDomain tag** — they cannot, because the three ledger layers are disjoint by construction
(9,409 + 585 + 28,009 = 38,003, overlap 0). B-4's population has no members in any CodeDomain-defined
category, so it has no home in 24. Filed under `00-Engine-Core-Runtime/Ownership-Boundary/`, beside
the cross-subsystem accessor hubs, which is the same question from the other side. Flagging rather
than silently relocating.

## COVERAGE — block 4

`00-Engine-Core-Runtime` — **8 documents** (was 7). New: *The 585 intentionally ownerless functions,
and the shared scratch buffers they write.*

| measurement | result |
|---|---|
| ownerless functions writing module state | **10.1 %** (59 of 585) |
| control: `PrimaryOwner` functions | **21.5 %** (2,019 of 9,409) |
| control: `CodeDomain` only | 17.1 % (4,798 of 28,009) |
| control: unresolved residual | 24.7 % (39 of 158) |
| `READ_QUERY_RESOLUTION_SUPPORT` writing module state | **0 of 107** |
| mislabelled sub-classes found | **3 of 585** (0.5 %) |
| shared geometry scratch at `022D9198`–`022D9428` | 660 B, **215 distinct writers**, 4 owner categories |

Also newly documented: the `022D8F00`–`022D9500` page is **13 distinct objects**, not one region;
two are the engine's shared geometry scratch (660 B / 215 writers and 130 B / 76 writers), and one is
the RNG enable/mode word already documented in
[`rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md).

## OPEN-QUESTIONS — block 4

| ID | Disposition |
|---|---|
| **B-4** | **ANSWERED — earned, not inherited.** Population re-derived from the image (all 38,161 real bodies disassembled), never re-selected from the tag. Three results: the ownerless population writes module state at **less than half** the rate of the owned population; **all 107** `READ_QUERY_RESOLUTION_SUPPORT` functions write none; and the **six CLASS labels produce six distinct, correctly-ordered profiles** — `CALLER_OWNED_OR_TRANSIENT_MATERIALIZATION` at 0 median callees / 279 B / 56 % write rate against `ROUTER_ADAPTER_OR_THUNK` at 2 callees / 56 B / 2.8 %. A bulk sweep has no mechanism for producing that separation. **Scope correction:** 583 of the 585 carry Presentation prior evidence — this is one category's ownerless residue, not a whole-image population, and B-4's wording implies otherwise. |
| **BL-1** | **BOUNDED — exactly 7 rows, not systemic.** `SUPERSEDES` and `RECLASSIFY` mark **the same seven functions** (`00182E80`, `001DC3D0`, `00225570`, `00225580`, `00225680`, `00225690`, `002256A0`), all `PrimaryOwner:Audio`, all still tagged, **none in the 585**. And **`REJECT` is not a retraction marker** — it appears as `SOURCE_REJECTION_REASON=REJECT_<CATEGORY>_…`, which declines ownership *for* a category. Machine test: **zero** owned functions carry a `REJECT` naming their own owner. Tags and prose contradict each other nowhere except those seven. BL-1's "every tag-based census over-counts" is too strong; the correct statement is "seven functions carry an unhonoured retraction." |
| **BQ-11** *(new)* | Three `ROUTER_ADAPTER_OR_THUNK` labels are wrong. `003B8670` (4,578 B, 63 distinct callees, 15 written objects over 11 pages) is a coordinator; `00521BB0` (1,757 B, 1 callee, 14 objects all in shared scratch) is a materializer; `005004C0` (497 B, 39 callees) is a switchboard. Class median is 56 B / 2 callees. **The ownerless decision on all three stands** — only the sub-label is wrong. |
| **BQ-12** *(new)* | What `003B8670` is. 930 instructions, 97 calls to 63 distinct functions, 2 indirect, and **8 exclusive globals nothing else in the image writes** (`0209218C+20`, `020925A0+12`, …). A function of that shape with private state is a system, and it has no document. |
| **BQ-13** *(new)* | Field-by-field layout of the 660-byte object at `022D9198` and the 130-byte object at `022D8F90`. Their role is established; their layout is not. |
| **BQ-14** *(new)* | Whether the eight `Gi*` backend factories (`00862E50`, `00862FD0`, `00863060`, `00863B40`, `00864E00`, `00865130`, `008652B0`, `00865320`), each caching its constructed object in one exclusive global, count as lifecycle authority. Arguable either way; currently ownerless. |
| **BQ-15** *(new)* | Whether the other categories' shared helpers were held to the same rule. This population is 583/585 Presentation, so B-4 has only been answered for one category. |

## AUDIT-LOG — block 4

### 2026-09-02 — repos-f1 block 4: B-4 answered, and a fifth instrument defect

**Method.** B-4's failure mode is the one this database keeps hitting — a tag population mistaken for
a census. So the population was **re-derived from the image**: all 38,161 real function bodies
disassembled (stopping at `int3` padding, so the block-2 extent defect could not contaminate the
count), measured for the property the GFZ's own policy names — *"primary ownership requires
independent subsystem state/lifecycle authority"* — and compared against **three control groups**.
A rate with no control is not evidence.

**SURVIVED, three ways.** 10.1 % against 21.5 %. 107 of 107 read-side functions writing nothing. Six
labels producing six distinct profiles in the correct order. The last matters most:
`CALLER_OWNED_OR_TRANSIENT_MATERIALIZATION` and `ROUTER_ADAPTER_OR_THUNK` have *opposite* measured
profiles under labels that promise opposite behaviour, which a bulk application cannot produce.

**The apparent counterexamples are the proof.** The ownerless functions that write the most module
state write it into buffers that **215** and **76** other functions also write, spanning Presentation,
Audio, Movement and ActorEntity. A helper borrowing a workbench four subsystems share is the
definition of what the policy calls ownerless.

**DEFECT 5, caught before publication — the census counted addresses, not objects.** The first pass
reported `00433830` writing **84 distinct globals**, which would have been the clearest
counterexample in the set. The addresses were `022D8F90, 022D8F91, 022D8F92 …` — **84 consecutive
bytes of one buffer**, written byte-wise. Recounted with adjacent targets coalesced (gap ≤ 8), the
same function writes **12 objects**, largest a 52-byte run, and the population maximum drops from 84
to **15**.

It also killed a second claim already drafted: that `022D8F00`–`022D9500` is one 1,436-byte
scratchpad. **It is thirteen objects**, and one of them (`022D9138`) is RNG control state documented
elsewhere. What forced the look was checking my region against a document that already cited an
address inside it — `rng-streams.md`. **Cross-checking against an existing document is what broke the
over-claim**, which is an argument for doing it before publishing rather than after.

Fifth defect in four blocks, fifth to produce a plausible number rather than an obvious failure:
pops-without-pushes · branch-insensitive summing · an over-running body extent · a sweep reading past
a table's end · a census counting addresses as objects.

**A measure that returned an impossible answer, and was therefore not published.** A pointer-write
detector (writes through a register loaded from a global) returned **zero hits across all 38,161
functions**. Zero is not a finding, it is a broken instrument, so it appears nowhere in the document.

**Recorded limits.** The call graph does **not** corroborate "shared across subsystems": only **1 of
the 585** has callers in three or more owner categories. Stated in the document as a limit rather
than dropped, and it is why the ownership decision is argued from behaviour rather than from callers
— which the evidence standard requires anyway, since caller ownership may never be inherited.

### Structural changes — block 4

New folder `00-Engine-Core-Runtime/Ownership-Boundary/`. Rationale in the placement note above: the
population has zero members in any CodeDomain-defined category, so it cannot live in 24, and it sits
naturally beside `Shared-State-Accessors/`, which asks the same question from the hub side.

## CALL-CHAINS / ADDRESS-INDEX — block 4

### A shared-state seam rather than a call chain

```
215 functions  (Presentation 128 · Audio 4 · Movement 2 · ActorEntity 1 · 30 ownerless · 50 CodeDomain)
   -> WRITE ->  022D9198..022D9428   660 B   shared geometry scratch      *** NO OWNER ***
 76 functions
   -> WRITE ->  022D8F90..022D900E   130 B   secondary shared scratch     *** NO OWNER ***
  2 functions  (00259180, 0044BAC0)
   -> WRITE ->  022D9138             4 B     RNG enable/mode  -- NOT scratch; see rng-streams.md
```

**This is a seam no call-graph reading can find**, because the functions never call each other — they
meet only at the buffer. Worth placing next to the accessor hubs: hubs are shared *code*, these are
shared *memory*, and the database had the first but not the second.

### ADDRESS-INDEX — new entries

| Address | Name | Size | Document |
|---|---|---:|---|
| `022D9198`–`022D9428` | primary shared geometry scratch — 215 writers, 4 owner categories | 660 B | Ownership-Boundary |
| `022D8F90`–`022D900E` | secondary shared scratch — 76 writers | 130 B | Ownership-Boundary |
| `022D8F30`–`022D8F50` | small shared scratch — 29 writers | 36 B | Ownership-Boundary |
| `003B8670` | authored-event / bootstrap coordinator — mislabelled a router | 4,578 B | Ownership-Boundary (BQ-11, BQ-12) |
| `00521BB0` | scratch materializer — mislabelled a router | 1,757 B | Ownership-Boundary (BQ-11) |
| `005004C0` | effect-subtype switchboard — 39 callees | 497 B | Ownership-Boundary (BQ-11) |
| `00433830` | shared tessellation helper — writes a 52-byte scratch run byte-wise | 3,202 B | Ownership-Boundary |
| `00259180` | RNG stream seeding — one of two writers of `022D9138` | — | Ownership-Boundary / rng-streams |

---
---

# repos-f1 — block 5: BQ-13, the shared transform workbench

*(Appended. Block 4 above is merged and can be deleted.)*

Same program state: `GN158`, snapshot `46f02e26…bbbb2`, EXE `73461d08…721f8`. No mutation. No
`_index/*.md` edited. `check_links` green (174 files, 853 links). `verify_doc_addresses` green on the
new document — 52 cited, 0 unresolved.

New document:
[`../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md`](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md)
— `DOCUMENTED`, tier 1, one falsification pass.

**Both questions you set are answered, and the second answer required correcting my own block-4
method.**

## COVERAGE — block 5

`00-Engine-Core-Runtime` — **9 documents** (was 8).

| | |
|---|---|
| region | `022D8F00`–`022D9500`, 1,536 B, **BSS** — `.data` raw ends at VA `01F7E400`, so no file image |
| addresses touched | 315 — 134 write-only, 8 read-only, 173 both |
| distinct writers / readers | **249** / 251 |
| objects, by writer-set similarity | **62** (adjacency-only coalescing gave 13 — corrected) |
| SSE-width accesses | 46, **all 46 16-byte aligned**, histogram `{0: 46}` |
| proven matrix | `022D91B0`, 4×4, by `003970A0`'s four-row 64-byte copy |
| row-touchers that write before reading | **215 of 216** |
| owner categories that only read | **none** |

## OPEN-QUESTIONS — block 5

| ID | Disposition |
|---|---|
| **BQ-13** | **ANSWERED, both halves.** *Structure:* the area is BSS with no static layout; every 16-byte access is 16-byte aligned (46/46); `003970A0` (44 B) copies four consecutive rows at `022D91B0` into one 64-byte destination, which fixes a 4×4 matrix **from the engine's own code** rather than from adjacency; `0036D9E0` (918 B) clears 80 slots and reads none. *Ownership:* **no owner, and "shared scratch" undersells it — it is an argument-passing area.** 215 of 216 row-touchers write before reading; only **one** function in the image reads a row it did not write; no non-Presentation owner keeps a private sub-area (ActorEntity 0 slots Presentation does not write, UI 0, Movement 0, Audio 4); and the only whole-area initializer is **unowned**. A parameter area cannot be owned because nothing is held in it. |
| **BQ-14** | **ANSWERED and CORRECTED.** The page holds **62 objects, not 13**. My block-4 count coalesced write targets by **address adjacency** — the inference this database bans — which over-merged by nearly 5×. Re-derived from writer-set overlap. |
| **BQ-16** *(new)* | How the row array divides into matrices beyond `022D91B0`. Rows are accessed in runs of 4, 6 and 8, so a sliding window makes every 16-byte offset look like a base; the structural probe cannot separate them. Left open rather than guessed. |
| **BQ-17** *(new)* | What `022D94B0` and `022D94B4` point to. Read 8 bytes wide by 16 functions in one tight family (`0036DDC0`–`0036E9B0`), never as floats, and **never written through a RIP-relative store** — set through a register. |
| **BQ-18** *(new)* | What the four Audio users (`00361DE0`, `00362230`, `003623C0`, `00363FD0`) compute. They write 11–28 slots each and read fewer, so they are using the workbench as arguments; which transform they ask for is unread. |
| **BQ-19** *(new)* | Whether any of the 62 behavioural objects is genuinely persistent state rather than parameter space. The test applied is population-wide; individual slots were not traced. |
| **BQ-20** *(new)* | What `0036D9E0`'s header writes (`01EF93F0`, `01EF93F4`, `01EF93FC`) configure. |

**Numbering note:** you filed BQ-13 as the scratch and BQ-14 as the thirteen objects; my block-4 text
had BQ-13 as the layout and BQ-14 as the `Gi*` factories. I have used your numbering. The `Gi*`
factory question is unanswered and needs an id.

## AUDIT-LOG — block 5

### 2026-09-02 — repos-f1 block 5: BQ-13, and my block-4 object boundaries were derived the banned way

**Attack chosen: my own clustering rule.** This area entered the database in the B-4 audit as *"13
objects, the largest a 660-byte buffer with 215 writers"*. Both figures came from coalescing write
targets whose addresses lie within 8 bytes of each other — **address adjacency, which the evidence
standard bans as proof.** Having just been burned in the other direction (84 consecutive bytes read
as 84 globals), the rule itself was the first thing to attack.

**CORRECTED: 62 objects, not 13.** Re-derived behaviourally — two slots belong to one object when
the same functions touch them — the page holds **62** groups. The "660-byte buffer" is three separate
64-byte row blocks plus a 20-byte hot spot with 138 writers, a 148-byte area with **one** writer, and
several isolated slots.

**Both of my clustering errors were the same error.** Adjacency splits one object into many when
access is byte-wise, and merges many into one when they are packed. Wrong in both directions within
two blocks of each other, and **neither failure announced itself in the number.**

**SURVIVED: everything that came from the code rather than from a rule.** All 46 SSE accesses
16-byte aligned. `003970A0` fixing a matrix at `022D91B0`. `0036D9E0` clearing 80 slots with zero
reads. 215 of 216 row-touchers writing before reading.

**SURVIVED: the ownership verdict, tested three ways.** The suspicion worth killing was that
Presentation owns the area and the rest borrow — 144 of the 152 owned writers are Presentation.
All three tests fail: no other owner keeps a private sub-area; the whole-area initializer is unowned;
and only one function reads a row it did not write. **The head count is deliberately not the
argument** — this database may not infer ownership from a population of users, which is the same
inheritance error it bans for callers.

**What stopped the over-claim, again.** Checking the page against every document that already cites
an address inside it. `rng-streams.md` claims `022D9138`; its writer set is two and it is never
touched by a float instruction, so it is not workbench data — and finding that is what forced the
look at the page's internals that broke "one 660-byte buffer".

### Structural changes

New folder `00-Engine-Core-Runtime/Shared-Transform-Workbench/`. The block-4 document has been
corrected in place (banner over the wrong figures, `[x]` on BQ-13, pointer to the new document); its
**writer counts were correct and are what carried the B-4 argument** — only the object boundaries
were wrong, and the correction says so rather than rewriting the earlier reading away.

## CALL-CHAINS / ADDRESS-INDEX — block 5

```
144 Presentation ─┐
  4 Audio         ├─ WRITE ─> 022D8F00..022D9500 ─ READ ─> the same functions
  1 ActorEntity   │            the transform workbench
  1 UI            │            (1,536 B, BSS, 62 objects)
  2 Movement      ┘
 97 unowned / CodeDomain

   0036D9E0 ── clears the whole area, reads nothing, UNOWNED
   003970A0 ── the only function that reads a row it did not write (matrix 0)
```

**These 249 functions overwhelmingly do not call one another.** They are related only by touching the
same memory, so no call-graph reading can find the relationship — the same seam your accessor-hubs
document has for shared *code*.

### ADDRESS-INDEX — new entries

| Address | Name | Size | Document |
|---|---|---:|---|
| `022D91B0` | **matrix 0** — proven 4×4 by `003970A0` | 64 B | Shared-Transform-Workbench |
| `022D91A0`–`022D939F` | the row array — 32 aligned 16-byte rows | 512 B | Shared-Transform-Workbench |
| `022D8F90`–`022D900F` | second row block, 8 rows | 128 B | Shared-Transform-Workbench |
| `022D8F30`–`022D8F6F` | third row block, 4 rows | 64 B | Shared-Transform-Workbench |
| `022D94B0`, `022D94B4` | two pointers, 16 readers, never RIP-written | 8 B each | Shared-Transform-Workbench (BQ-17) |
| `0036D9E0` | workbench clear — 80 slots, no reads, **unowned** | 918 B | Shared-Transform-Workbench |
| `003970A0` | matrix 0 getter — four `movups` into one 64-byte block | 44 B | Shared-Transform-Workbench |
| `00361DE0`, `00362230`, `003623C0`, `00363FD0` | the four Audio users | — | Shared-Transform-Workbench (BQ-18) |
| `0025C830` | the ActorEntity user — 29 slots written, 24 read | — | Shared-Transform-Workbench |
| `0035DCC0` | the UI user | — | Shared-Transform-Workbench |

---
---

# repos-f1 — block 6: category 24's four C++ runtime families

*(Appended. Block 5 above is merged and can be deleted.)*

Same program state: `GN158`, snapshot `46f02e26…bbbb2`, EXE `73461d08…721f8`. No mutation. No
`_index/*.md` edited. `check_links` green (177 files, 877 links). `verify_doc_addresses` green — 29
cited, 0 unresolved.

New document:
[`../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`](../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md)
— `DOCUMENTED`, tier 1, one falsification pass.

**The labels are EARNED. Seven mechanisms re-derived from the image, every one scoring 100 %.** One
label's *name* is unsupported and is called out.

## COVERAGE — block 6

`24-Compiler-And-CRT-Runtime` — **5 documents** (was 4). 915 functions that had no mechanism
document between them now have one.

| label | n | own instrument | score |
|---|---:|---|---:|
| all deleting-destructor labels (6 sub-labels, 4 families) | 226 | the `flags & 1` test + a deallocator call | **226 / 226** |
| `CompilerGeneratedCpp.StaticObjectInitializer` | 90 | the CRT registration table | **90 / 90** |
| `CompilerGeneratedCpp.StaticZeroInitObjectInitializer` | 11 | same | **11 / 11** |
| `CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` | 117 | `call _Init_thread_header` | **117 / 117** |
| `CompilerGeneratedCpp.ThreadSafeStaticObjectInitializer` | 23 | same | **23 / 23** |
| `CxxObjectLifecycle.VtableInstall*` | 60 | RIP-`lea` → store into the object | **60 / 60** |
| `CxxObjectLifecycle.DerivedConstructorVtableInstall` | 25 | same | **25 / 25** |
| teardown labels | 88 | neither instrument | **0 / 88**, correctly |

**Perfect separation in both directions**: eager initializers are 100 % registered and 0 % guarded;
lazy accessors are 100 % guarded and 0 % registered.

New mechanism facts worth having: **a deleting destructor's `mov edx, imm` before the free call is
its class's exact size**, so 226 functions each hand you a `sizeof`. And all 63
`AlignedOrGuardedFree` destructors route through `0016D6A0`, the disabled CFG stub — which is what
"guarded" names, and it is inert in the shipped game.

## OPEN-QUESTIONS — block 6

| ID | Disposition |
|---|---|
| **BQ-22** *(new)* | **`CxxStandardLibrary.NativeQualified` (52) is not supported by its own name.** "Qualified" asserts a recovered qualified symbol; **all 52 have `name_source: DEFAULT`** — the snapshot holds no symbol for any of them. The functions may well be std code; the label's justification is not visible. |
| **BQ-23** *(new)* | The other `CxxStandardLibrary` sub-labels — `ContainerAllocatorSupport` 40, `StdRegex.Runtime` 21, `OrderedContainerRuntime.*` 19, `StringHeapAlgorithms` 6 — untested. Each names a specific std mechanism and each is checkable against upstream MSVC STL source (tier 6). |
| **BQ-24** *(new)* | The 57 `Microsoft` functions with no recovered symbol. The other 49 carry real ones (`sprintf`, `underflow`, `_Reset_back`, `_Set_back`, and eight copies of `scheduler_resource_allocation_error` — the Concurrency Runtime ships whether or not the game uses it). |
| **BQ-25** *(new)* | `ConditionalTeardownReturnTrue` (28) and `StaticContainerTeardown.IndirectAllocator` (60) — 88 teardown functions confirmed only negatively. |
| **BQ-26** *(new)* | The **vector** deleting destructor form (`flags & 4`) has no label in any of the four families. `00185800` is one; the population is unmeasured. |

## AUDIT-LOG — block 6

### 2026-09-02 — repos-f1 block 6: the C++ runtime families are earned; two more defects, both in the test

**Method.** Both instruments were **validated against published figures before use**: the CRT
initializer table read returns **1,172** and the guard census returns **707**, exactly the numbers the
static-initialization and lazy-statics documents already publish, derived here independently. An
instrument that cannot reproduce a known number is not trusted for an unknown one. **The call graph
was avoided entirely** — your 689 thunk sinks would truncate any path-based measure silently, so every
census here is over instruction bytes or a data table.

**DEFECT 6 — the detector was built from one instance of the idiom.** The first census looked for
`test dl, 1` and scored `CxxObjectLifecycle.ScalarDeletingDestructor` at **0 of 135**, which reads as
"this label is wrong for every member it has". It is wrong for none of them. Those destructors call an
inner destructor first, that call clobbers `rdx`, so the compiler moves the flag to a callee-saved
register and tests it there (`mov ebx, edx` … `test bl, 1`). **The detector could not see the more
common spelling of the thing it was detecting.** Following the flag through a register copy, and using
the deallocator call as the primary diagnostic, turned 0/135 into **135/135**. Found by reading four
bodies instead of trusting a rate — a 0 % score on a 135-member label is not a finding, it is an
instrument report.

**DEFECT 7 — one instrument applied to two different mechanisms.** The same census lumped eager
initializers together with lazy accessors and tested the lot against `_Init_thread_header`, scoring
**58.1 %**. That number measures nothing: eager initializers are registered in a table and are
*supposed* to score zero on the guard test; lazy accessors are guarded and *supposed* to score zero on
the table test. Tested separately against the mechanism each label actually names, every group is
perfect. **A blended rate over two mechanisms is not weak evidence — it is not evidence.**

**SURVIVED: the other direction.** 178 functions perform the deleting-destructor idiom without one of
these labels, which looked like under-inclusion until they were classified properly: **99
`PrimaryOwner:Audio`, 42 Phyre, 17 `NativeRoutine`, 8 Input**. They are *owner*-tagged, and the layers
are disjoint by design — a destructor for an Audio object is Audio's, and its compiler-generated shape
does not transfer it to a CodeDomain family. Same for the 1,071 registered initializers and 566 guard
callers outside the families. **The layer separation is doing exactly what it exists to do**, and this
is the second block in which an apparent gap turned out to be it working.

**Defect count for the run: seven, all in instruments, none in the binary.** pops-without-pushes ·
branch-insensitive summing · an over-running body extent · a sweep past a table's end · a census
counting addresses as objects · a detector blind to the commoner spelling · one instrument for two
mechanisms.

### Structural changes — block 6

New folder `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/`.

## CALL-CHAINS / ADDRESS-INDEX — block 6

```
CRT startup
  -> walk 008C31D8..008C5678            1,172 registered initializers
     -> StaticObjectInitializer (90) / StaticZeroInit (11)
        -> the object's constructor
           -> VtableInstall* (85)       writes the vtable pointer into the object

first use of a lazy static
  -> ThreadSafeStaticRecordAccessor (117)   median body 115 B
     -> _Init_thread_header 008092FC        take the guard
        -> ThreadSafeStaticObjectInitializer (23)
     -> _Init_thread_footer 0080929C        publish

object death, from any subsystem
  -> vtable slot 0 = the deleting destructor (226)
     -> inner destructor (spelling B)
     -> free 00809950   or the aligned/guarded path via 0016D6A0
```

### ADDRESS-INDEX — new entries

| Address | Name | Document |
|---|---|---|
| `0x008C31D8`–`0x008C5678` | CRT dynamic-initializer table — 1,172 entries, all real function entries | Cxx-Runtime-Families |
| `00809950` | `free` — 5-byte thunk to `00210EB0`; the sized deallocator every spelling-A destructor calls | Cxx-Runtime-Families |
| `001D70A0` | spelling-A deleting destructor, 43 B — the whole idiom on one screen | Cxx-Runtime-Families |
| `00195530` | spelling-B deleting destructor, 52 B — flag saved in `ebx` across the inner call | Cxx-Runtime-Families |
| `00185800` | **vector** deleting destructor, 66 B — tests `dl,1` and `dl,4`; unlabelled | Cxx-Runtime-Families (BQ-26) |
| `0016D6A0` | on the "guarded free" path of all 63 `AlignedOrGuardedFree` destructors | Cxx-Runtime-Families |

---
---

# repos-f1 — block 7: BQ-26, and the question's own name was the hypothesis

*(Appended. Block 6 above is merged and can be deleted.)*

Same program state: `GN158`, snapshot `46f02e26…bbbb2`, EXE `73461d08…721f8`. No mutation. No
`_index/*.md` edited. `check_links` green (177 files, 878 links). `verify_doc_addresses` green — 42
cited, 0 unresolved.

Extended in place rather than forked into a new document:
[`../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`](../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md)
— new §2.1a and §11, `audit.passes` 1 → 2. Same subject; splitting it would have fragmented the
destructor material across two files.

**BQ-26 answered, and its framing was wrong.** It is not the vector deleting destructor. The
population is real and large — **1,608 functions** — and the GFZ label that covers 63 of them names
the mechanism correctly.

## COVERAGE — block 7

| | |
|---|---|
| functions testing bit 0 **and** a second flag bit, returning `this`, body ≤ 400 B | **1,608** |
| of those in the recovered vtable index (an instrument that never saw a flag test) | **1,607** |
| containing any backward branch — i.e. iterating, as a *vector* destructor must | **14** |
| bit-2-**set** side: first call is `0016D6A0` | **1,606 / 1,606** |
| bit-2-**clear** side | `00584730` → `_aligned_free` 1,494 · `007AD450` 93 · `0085E710` 19 |
| body size | min 62, median 92, **max 317** |
| carrying `DeletingDestructor.AlignedOrGuardedFree` | 63 |
| labelled elsewhere | **1,410 Phyre**, 94 Audio, 33 Input, 8 others |

`00584730` is `if (this) _aligned_free(this)`, a null check in front of the imported `_aligned_free`
at `0019C570`. **Bit 2 selects the sized `operator delete` over `_aligned_free`** — exactly what
`AlignedOrGuardedFree` says. The label is right and applied to 4 % of its population.

## OPEN-QUESTIONS — block 7

| ID | Disposition |
|---|---|
| **BQ-26** | **ANSWERED, framing refuted.** Not the vector form: only **14 of 1,608** members iterate, and a vector deleting destructor must iterate over the array. Bit 2 selects the deallocator. The name came from what MSVC's second flag bit is called in some references, not from this binary — worth recording, because the question's own wording was the hypothesis and it survived three blocks unexamined. |
| **BQ-27** *(new)* | **On the bit-2 path these destructors free nothing.** `0016D6A0` is the three-byte `ret 0` that `/OPT:ICF` folded ~273 `ret`-bodied functions onto — the same address the disabled CFG stub occupies. 1,606 functions have a sized-delete branch that returns immediately. Either the engine never passes bit 2, or it leaks those objects by design. **Checkable at runtime against the unmodified test client**, which repos-55 established hashes to the authorised EXE. |
| **BQ-28** *(new)* | What `007AD450` (93 members) and `0085E710` (19) are — the two minority deallocators on the bit-2-clear side. |

## AUDIT-LOG — block 7

### 2026-09-02 — repos-f1 block 7: BQ-26 refuted, and defect 8 caught by the shape rule

**DEFECT 8 — the tool ran, and the number was about the tool.** The first sweep promoted any register
receiving `edx` to "the flag register" anywhere in the body; in a 3 KB function that happens by
accident. It returned **1,616 functions with a median body of 92 bytes and a maximum of 3,175**, 1,412
of them Phyre. Nothing in the tool complained. **The shape of the answer did** — a 3,175-byte
compiler-generated destructor does not exist, so the population could not be what it claimed.

This is exactly the rule from repos-94's block that you logged this tick: *check that the answer has
the shape the question implies, not only that the tool ran.* It arrived before I ran the census and I
used it as the check. Tightened three ways — the flag copy must precede the first call, the function
must return `this`, body ≤ 400 B — the population became **1,608**, median 92 B, **max 317 B**.

**Cross-checked against an instrument that has never seen a flag test:** the recovered vtable index.
**1,607 of 1,608 are recovered virtual methods.** A loose detector does not produce that, and it is
what promotes this from "a plausible list" to a population.

**REFUTED: the vector framing.** Only **14 of 1,608** contain a backward branch. No iteration means no
array. BQ-26's name was inherited from a reference rather than measured here — and it had sat in the
document for three blocks as though it were a finding.

**The GFZ was right again.** `00584730` reads as `if (this) _aligned_free(this)`. Bit 2 chooses the
sized `operator delete` over `_aligned_free`, which is precisely what `AlignedOrGuardedFree` names.
**Third block running in which an apparent classification gap is the layer separation working** — the
other 1,545 members are Phyre- and owner-tagged, not mislabelled.

**A limit placed on one of my own earlier claims.** §4 says the `mov edx, imm` before the free gives
the class's exact size. That is verified at the sized-delete call sites read in §2.1 (`0x90`, `0x98`,
`0xD8`). It is **not** a bulk census: sweeping the first `mov edx, imm` in each of the 1,608 returns
`0x100` for 1,186 of them, which is not 1,186 classes of 256 bytes — it catches a different
instruction. **The claim holds per call site, not as a population statistic**, and the document now
says so rather than leaving a reader to trip over it.

**Defect count for the run: eight, all in instruments, none in the binary.**

### Structural changes — block 7

None. Existing document extended.

## CALL-CHAINS / ADDRESS-INDEX — block 7

```
object death, bit-2 form (1,608 functions, 1,410 of them Phyre)
  -> vtable deleting destructor
     if (flags & 1) {
        if (flags & 4)  operator delete(this, size) -> 0016D6A0   *** ret 0: frees nothing ***
        else            00584730 -> if (this) _aligned_free(this) -> 0019C570 (import)
     }
     return this
```

### ADDRESS-INDEX — new entries

| Address | Name | Size | Document |
|---|---|---:|---|
| `00584730` | `if (this) _aligned_free(this)` — the bit-2-clear deallocator for 1,494 destructors | 10 B | Cxx-Runtime-Families |
| `0019C570` | `_aligned_free` — imported thunk | 7 B | Cxx-Runtime-Families |
| `00185800` | `Phyre.SceneCamera` two-deallocator deleting destructor | 66 B | Cxx-Runtime-Families |
| `007AD450`, `0085E710` | the two minority deallocators (93 and 19 members) | — | Cxx-Runtime-Families (BQ-28) |

---
---

# repos-f1 — block 8: BK-3, the Yebis/PPFX source map

*(Appended. Block 7 above is merged and can be deleted.)*

Same program state: `GN158`, snapshot `46f02e26…bbbb2`, EXE `73461d08…721f8`. No mutation. No
`_index/*.md` edited. `check_links` green (181 files, 911 links). `verify_doc_addresses` green.
`check_consistency` **9 → 8** disagreements: one was mine and is fixed (below).

New document:
[`../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md`](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md)
— `DOCUMENTED`, tier 2, one falsification pass.

**BK-3 answered: yes, and there are 26 paths rather than 18.** They reconstruct a four-directory
source tree and attribute **193 compiled functions to the source file they were written in** — 188 of
them beyond RTTI's reach.

## COVERAGE — block 8

| | |
|---|---|
| source-path strings in the image | **300** (many duplicate copies) |
| distinct paths | **26**, all referenced from code |
| reference sites | **1,857** across **940** functions |
| PPFX/Yebis functions attributed | **193**, of which **192 to exactly one file** |
| of those, reachable by RTTI class recovery | **5** — the other 188 are not virtual methods |
| `PhyreScripting.inl` | 1,494 sites, 747 functions, **disjoint** from the PPFX set |

**Recovered source tree:** `..\src\` (2 files) · `..\src\GPU\` (**19**) · `..\src\GPU\TinyEffect\` (2)
· `..\src\UT\ppfxLicense.cpp`. Plus two absolute paths naming the **build machines**:
`d:\bamboo\build\yeblic-ppfxlic-bl2015\…` and `e:\jenkins\workspace\c11019p16003\…` —
**two middleware vendors, two CI systems** (Bamboo for Yebis/PPFX, Jenkins for PhyreEngine), and a
workspace name that says *licensed* twice.

Biggest files by attributed functions: `GPUDepthOfField.cpp` **22**, `TFXString.cpp` 20,
`GPUPostEffect.cpp` 19, `GPURenderGlare.cpp` 19, `TinyEffect.cpp` 18. **That is the map to the
remaster's bloom and depth of field.**

## OPEN-QUESTIONS — block 8

| ID | Disposition |
|---|---|
| **BK-3** | **ANSWERED.** 26 paths, not 18; a coherent four-directory tree; 193 functions attributed, 192 uniquely. Also recovers both middleware build systems and confirms the licence module (`..\src\UT\ppfxLicense.cpp`, 4 functions, 9 assertion lines) ships in retail. |
| **BQ-29** *(new)* | What each of the 193 functions *does*. File identity narrows the search enormously and closes nothing. |
| **BQ-30** *(new)* | The `TinyEffect` subsystem — 38 functions across two files, one a string module (`TFXString.cpp`, 20 functions from only 6 distinct assertion lines). An embedded shader-effect language is implied by the name and not established. |
| **BQ-31** *(new)* | Whether the `__LINE__` values reconstruct anything about file size or ordering. |
| **BQ-32** *(new)* | Why `GPUClassUtil.h` alone kept an absolute path while every `.cpp` is relative, and why it has 12 copies but exactly one line number (73). |
| **BQ-33** *(new)* | Whether `PhyreScripting.inl`'s 747 functions are one generated binding family. **Belongs to category 22**, filed against it rather than absorbed here. |

## AUDIT-LOG — block 8

### 2026-09-02 — repos-f1 block 8: BK-3 answered, and defect 9 was the question's own example

**DEFECT 9 — the sweep pattern was written from the question's example.** BK-3 quotes
`d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h`, which begins with a drive letter, so
the regex required one. **Yebis emits its `__FILE__` as a relative path** — `..\src\ppfx.cpp` — so the
sweep missed **287 of 300 strings, 96 % of the evidence**, and returned a tidy, plausible **13**.

Two things caught it and neither was the tool. The printed output showed **six identical copies of
`GPUClassUtil.h` all at line 73** — a display artefact of truncating to the last 72 characters, but a
shape that made no sense and forced a second look. And **BK-3 said 18; I had 13.** A census that
disagrees with the question it is answering has to explain the difference before it reports.

That is the second time in two blocks that **the question's own wording carried an unexamined
assumption into the instrument** — last block the name "vector deleting destructor", this block the
shape of an example path. Both are the same failure as inheriting a name from a neighbour.

**SURVIVED — cross-checked against an instrument that never saw a string.** The RTTI vtable index
overlaps this map on only **5** functions, and on all five the class name and the file name are the
same object: `GPURenderTexture.cpp` ↔ `PPFX::CRenderTexture`, `GPUTextureUtil.cpp` ↔
`PPFX::CTextureUtil`, `GPUInterfaceTexture.cpp` ↔ `PPFX::IGPUTexture`, `GPURenderTextureArray.cpp` ↔
`PPFX::CRenderTextureArray`, `ppfxRenderToTexture.cpp` ↔ `PPFX::IPfxRenderToTexture_Dx11`.
**Five of five.** The other 188 are outside the vtable index entirely — RTTI can only name virtual
methods, and most of a post-effects library is free functions. **The two instruments are
complementary, not redundant.**

**SURVIVED — the Phyre path is a different phenomenon**, not a bigger version of the same one. 1,494
sites but **no recoverable `__LINE__`**, and its 747 functions are **disjoint** from the 193. It is a
header included into generated bindings, so it went to category 22 rather than being absorbed.

**Not claimed:** what any of the 193 functions computes. This establishes *where they came from*.

### A consistency disagreement of mine, found and fixed

`check_consistency.py` flagged `0016D6A0` named `_guard_check_icall` in my new document and
`ICF_FoldedRetStub` in the audio boundary document. **The audio document is right and my own §11
already argued so** — the CFG stub is one of ~273 `ret`-bodied functions `/OPT:ICF` folded onto those
three bytes, and at this call site the arguments are `rcx = this, edx = size`, a deallocator
signature. The label contradicted my own prose. Switched to the neutral name in all three places,
with the reasoning stated. **9 → 8 disagreements.**

### Structural changes — block 8

New folder `23-Third-Party-Libraries/PostEffects-Yebis-PPFX/`.

## CALL-CHAINS / ADDRESS-INDEX — block 8

```
the rendered frame
  -> PPFX / Yebis
     ppfx.cpp                       public entry (8 fns)
       -> GPUInterface*.cpp         device, buffer, texture, surface, query, effect, resource
       -> GPURenderTexture*.cpp     render targets, incl. a pool (18 fns across 3 files)
       -> GPUDepthOfField.cpp (22) · GPURenderGlare.cpp (19) · GPUPostEffect.cpp (19)
          · GPUTextureLuminance.cpp (5) · GPUGlareDef.cpp (3)
       -> TinyEffect/               embedded effect system (38 fns)
       -> ppfxLicense.cpp           licence validation, shipped (4 fns)
```

### ADDRESS-INDEX — new entries

| Address | What | Document |
|---|---|---|
| `00D23FF0` | `…phyreengine\include\Scripting/PhyreScripting.inl` — 1,494 sites, 747 functions | Yebis-PPFX (BQ-33) |
| `00D8E4C0` | `..\src\ppfx.cpp` | Yebis-PPFX |
| `00D8FC48` | `..\src\ppfxRenderToTexture.cpp` | Yebis-PPFX |
| `00D90348` | `..\src\GPU\GPUMath.cpp` — 11 copies, one per assertion line | Yebis-PPFX |
| `00D90E50` | `..\src\GPU\GPUPostEffect.cpp` | Yebis-PPFX |
| `00D94ED0`, `00D94F50` | `d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h` | Yebis-PPFX (BQ-32) |
| `0016D6A0` | the ICF-folded `ret 0` — the assertion reporter these 1,857 sites call; **hooking it yields every failed Yebis assertion with file and line still in registers** | Yebis-PPFX |
