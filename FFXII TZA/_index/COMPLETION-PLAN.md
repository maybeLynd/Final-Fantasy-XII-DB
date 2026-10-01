# Completion plan — what "done" is, and how each dimension gets there

**Written 2026-09-03.** Numbers are from `progress.py` on that date; **re-run it, never quote from
here.** This document is the plan, not the score.

---

## 1. What done means

> **REVISED 2026-09-08.** The goal expanded to modding-grade → reconstruction-grade →
> parity-certified. See [`GOAL-REVISION-2026-09-08.md`](GOAL-REVISION-2026-09-08.md). **This plan is
> not superseded** — its three dispositions and its argument against volume-as-progress are carried
> forward intact. Two things change: a fourth disposition **D**, and completion criteria per
> maturity level.

The terminal condition for **L1 (modding-grade)** is already declared by
[the final audit protocol](FINAL-AUDIT-PROTOCOL.md): **thirty consecutive passes from pass 1**,
gated on `unresolved = 0`, every system documented, and `OPEN-QUESTIONS.md` empty.

**L2 (reconstruction-grade)** additionally requires, for major systems: reconstruction-grade types,
relationships, a behavioural contract, runtime evidence, and script/data/resource integration.
**L3 (parity-certified)** requires independent implementation compared against the original within
stated parity dimensions.

> **REVISED 2026-09-12 — the endpoint is L1 + L2, and the readiness gate is not it.** The programme
> previously ran toward assembling [`RECONSTRUCTION-READINESS-GATE.md`](RECONSTRUCTION-READINESS-GATE.md)
> and asking for a decision on it. **That endpoint is replaced.** The gate document stays a valid
> instrument and its measurements stand; **producing it is no longer an ending.**
>
> **DONE is that this plan, [`GOAL-REVISION-2026-09-08.md`](GOAL-REVISION-2026-09-08.md) and
> [`FINAL-AUDIT-PROTOCOL.md`](FINAL-AUDIT-PROTOCOL.md) are satisfied for L1 and L2**, including the
> reviews those documents require — for L1 the thirty consecutive passes from pass 1, gated on
> `unresolved = 0`, every system documented and `OPEN-QUESTIONS.md` empty; for L2 reconstruction-grade
> types, relationships, behavioural contracts, runtime evidence and script/data/resource integration
> **for major systems**, with the claim-level reconciliation §4 requires. L3 parity is later, and a
> **primary reconstruction phase needs a separate user instruction**; bounded probes that test
> database sufficiency are unaffected.
>
> **Not completion:** a report, a pilot count, a green validator, an empty board or an approval
> request. **Not a route to completion:** inventing an exclusion, waiving an architectural gap, or
> erasing a question to reach zero. Evidence-backed **B** and **C** dispositions remain valid exactly
> as §3 defines them, and **D** exists so an unresolvable operation stays visible rather than silent.
> Missing live evidence blocks the **affected claims**, not the database.
>
> **34 executed contracts are not 34 established systems.** A contract's claims are established
> **claim by claim**, at the evidence class each one earns; a validator or a `CONTRACT_MAP` alignment
> establishes only what its implementation actually tests.

### Disposition D — added 2026-09-08

§3 below defines **A individually explained / B class-explained / C dispositioned**. A fourth is
added:

**D — explicit unresolved exception.** Something that genuinely cannot yet be resolved stays
**visible in coverage rather than absent from it**. Without D, an unresolvable operation has nowhere
to live except silence, and silence reads as completion.

**And the disqualifying justification is now named.** *"This function probably isn't interesting to
modders"* is no longer sufficient. The question is **could ignorance of this operation prevent us
from reproducing FFXII correctly?** — if **yes** or **unknown**, it stays on the frontier.

> **`final_audits 0 / 30` is the terminal condition being correctly gated, not thirty passes nobody
> has started.** It cannot move until everything else does, and it should be the last thing touched.

---

## 2. Where it stands

**The table immediately below is the STARTING POSITION and was superseded on 2026-09-14** — it is kept, and restated underneath. The marker is here, above the rows, rather than only after them: a reader scanning the table meets it first, and a checker reading a few lines around any row can see it.

| dimension | now | remaining |
|---|---|---|
| `engine_explained` | 6,811 / 34,270 | **27,459 functions** |
| `ledger_resolved` | 34,116 / 34,270 | **154 residuals** |
| `audit_coverage` | 139 / 166 | **27 documents** |
| `registry_explained` | 5 / 63 | **58 slots** |
| `ebp_explained` | 0 / 14 | **14 units** |
| `formats_explained` | 0 / 48 | **48 shipped file formats** |
| `questions_closed` | 326 / 1,538 | **403 OPEN + 38 PARTIAL + 6 BLOCKED** in the register, plus document checklists |
| `final_audits` | 0 / 30 | gated |

> **THIS TABLE IS TITLED "WHERE IT STANDS" AND HAD NOT BEEN RESTATED SINCE IT WAS WRITTEN.**
> Seven of its eight rows are superseded — one of them completely, since `ebp_explained` reads
> `0 / 14` and is **finished**. The table above is kept because a plan's starting position is worth
> preserving; **it is not the current state.** Re-measured with `progress.py`, 2026-09-14:
>
> | dimension | **now** | **remaining** | movement |
> |---|---|---|---|
> | `engine_explained` | **13,117 / 34,270** | 21,153 functions | 6,811 → 13,117 |
> | `ledger_resolved` | **34,240 / 34,270** | **30 residuals** | 154 → 30 |
> | `audit_coverage` | **363 / 365** | 2 documents | denominator 166 → **365** |
> | `registry_explained` | **62 / 63** | 1 slot | 5 → 62 |
> | `ebp_explained` | **14 / 14** | **none — complete** | 0 → 14 |
> | `formats_explained` | **40 / 48** | 8 formats | 0 → 40 |
> | `questions_closed` | **1,026 / 2,294** | 1,268 open | denominator 1,538 → **2,294** |
> | `final_audits` | **0 / 30** | gated, and correctly so | unchanged |
>
> **TWO DENOMINATORS GREW AND THAT IS NOT A SETBACK.** `audit_coverage`'s denominator was 166
> documents and is now **365**, and the ratio still climbed to 99.45 %; `questions_closed`'s was
> 1,538 and is now **2,294**,
> because questions are FOUND, not invented, and the ratio still climbed from 21 % to 44.7 %.
> **A row that reported only the ratio would have hidden both.** `engine_explained`'s denominator
> is unchanged at 34,270 — and is itself under review, because `UC-1` voted 3-0 to admit the
> unlisted code blocks and that change is unimplemented pending independent review of its floor.
>
> **`final_audits` is the one row that has not moved, and it is the one that should not have.** Its
> gate needs `unresolved = 0`, every system documented and `OPEN-QUESTIONS.md` empty. The first is
> now within one task; the third is 1,268 away.


---

## 3. The 27,459, and the trap in counting them

**`engine_explained` counts functions *cited* by a document.** Nothing stops a single table of
11,848 rows from moving it thirty-four points overnight without explaining anything — the same
defect `check_named_not_cited.py` already warns about for names: *"an address supplied from a name
lookup is a transcription, not a citation."*

**So the plan needs a disposition policy before it needs volume.** What the 27,459 actually
are — **every `share` below is of the 34,270 non-funclet functions**, not of the 27,459, so
the column does not sum to 100 %:

| population | count | share |
|---|---:|---:|
| **no CodeDomain** (owner or final-no instead) | 10,024 | 29.3 % |
| **Phyre middleware** | 6,769 | 19.8 % |
| **generic shape classes** — `NativeRoutine` 5,088, `NativeAdapter` 2,168, `NativeInline` 1,883, `NativeLeaf` 1,637, `NativeDispatch` 1,072 | **11,848** | **34.6 %** |
| `Runtime` | 1,553 | 4.5 % |
| `Boundary` | 831 | 2.4 % |
| `ThirdParty` | 691 | 2.0 % |
| `Thunk` | 689 | 2.0 % |
| `CompilerGeneratedCpp` | 417 | 1.2 % |

**Ownership is thinner than classification**: 24,861 functions carry **no `PrimaryOwner` at all**.
The owned 9,409 concentrate in Audio (2,064), ScriptVM (1,900), Presentation (1,564), Input (1,047).

> **A third of the binary carries a generic shape class**, and the residual document already says
> what that is worth: it **"accounts for a function without explaining it."** Citing those 11,848
> without explaining them would satisfy the metric and betray the mission.

### The three dispositions, and the bar for each

Every function must end in exactly one of these. **All three are declared in frontmatter, never
inferred** — the same rule as `registry_slots` and `ebp_units`, for the same reason.

**A — individually explained.** A document says what *this* function does, with an interior address.
The bar is the existing one: a citation inside the body, not at the entry.
*For: game logic, owned systems, anything a modder would change.*

**B — class-explained.** One document explains a mechanism that N functions implement identically,
and **enumerates them by a stated method**. Legitimate and already proven here: the 1,608 deleting
destructors, the 11 generated slot setters, the 315 class registrars.
**Bar: the document states the shared body shape, the enumeration method, and the count — and the
count is reproducible.** *For: generated families and the generic shape classes.*

**C — dispositioned.** Accounted for by naming what it is, not by explaining it.
**Bar: the upstream is named and the boundary is stated.** Category 23 already does this for
`ThirdParty`; category 22 for Phyre; category 24 for the CRT.
*For: vendor, middleware, compiler output.*

> **B is where the 11,836 go, and B is the only one that scales.** A is impossible at that volume
> and C would be a lie — a `NativeLeaf` getter inside combat is not vendor code.

---

## 4. Per-dimension plan

### `ebp_explained` — 14 units *(smallest, most self-contained, start here)*

Population censused: the container plus 13 section types, from unpacking all 1,115 `us` scripts.
Plan and ordering in [25-EBP-Script-Container](../25-EBP-Script-Container/README.md):
container → the four with a decompiler oracle → the seven unknowns, pairs first.
**Template: `_templates/FORMAT.md`.** No live game needed.

### `formats_explained` — 48 shipped file formats *(added 2026-09-03)*

**The database reads engines well and the files they eat barely at all.** Audio: eleven documents,
2,064 owned functions, and `.sab` (4,609 files, 838 MB) plus `.snd` (2,304) had one passing mention
between them. **`engine_explained` is structurally blind to this** — a format nobody documents costs
no functions, so nothing in the metric set could see the hole.

Population and ordering in [ASSET-FORMATS.md](ASSET-FORMATS.md); denominator generated by
`census_archive_formats.py` from the 89,414-entry archive index. Three dispositions — `explained`,
`standard`, `external` — deliberately the same shape as §3's A/B/C, and for the same reason.

**Order: `sab`+`snd` → `mot`+`adm` → `efx`+`efb` → `ca`+`cm` → the `standard` sweep → `phyre` as
`external` → the seven genuine unknowns.** `sab` first because the audio *engine* is already
documented, which makes it the cheapest sheet in the list. **No live game needed for any of it.**

### `registry_explained` — 58 slots

Denominator re-derived from the registry document's own bounds. Work down by reference count; the
most-referenced unexplained slot is **`0x02EBF130`** (23 refs, `BattleUnit_ApplyUnitDefinition`
`0023A570`). Each slot is: read the principal consumer, establish what the table holds, declare the
slot. **No live game needed.**

### `ledger_resolved` — 154 residuals

**Read clusters, not singletons.** Three clusters were closed this way and all three clusterings
held, having been made before any member was opened. Remaining: cluster 1 at 6 of 13, then the
3-function cluster `00256960` / `00256CA0` / `00258350`, then singletons.
**Ledger rows are staged, not applied** — 15 sit in `Tools/work/pending/` and need
`Apply-GfzBatch.ps1` with the Ghidra project closed. **That is the one operator action outstanding.**

### `engine_explained` — 27,459 functions

**Order by disposition, not by address:**

1. **C first** — it is the largest and cheapest. Phyre 6,768 + ThirdParty 690 + Thunk 689 +
   `CompilerGeneratedCpp` 417 ≈ **8,564 functions** dispositioned by documents that largely exist
   in categories 22, 23 and 24; the work is declaring the boundary, not writing new prose.
2. **B next** — the 11,836 generic-shape functions, taken family by family. Each family needs one
   document with a reproducible enumeration.
3. **A last and forever** — owned game systems, which is the ordinary work of this database and the
   part that never really ends.

**The honest expectation: A will not reach 100 %, and the plan should not pretend otherwise.** The
mission is that nothing is *unexplainable*, not that every leaf getter has a paragraph.

### `audit_coverage` — 27 documents

Every document needs one named falsification pass. **This lags by construction**: a document lands,
the denominator rises, the ratio falls. It caught up all night and will keep doing so. No plan
needed beyond doing it — but **it should be swept before the final-audit gate**, not during.

### `questions_closed` — 447 outstanding

Two shapes, and they need different treatment:
- **Malformed questions must be withdrawn, not answered.** The `WITHDRAWN` status exists for this.
  *"What `002AC5F0` draws"* could never be answered — it draws nothing.
- **The rest close as the work above closes them.** Many are downstream of a residual or a slot.

### `final_audits` — 0 / 30

**Do not start.** Gated, and nine of the thirty are already mechanised. Pass 5 — fresh-import
reproducibility — **should run first in practice despite being numbered fifth**, because it
re-validates the parent every other pass is measured against.

---

## 5. The live-game tail — historical ordering

**Ordering revised 2026-09-10:** ASTRA now performs high-leverage runtime research concurrently
with FABLE and OPUS database work, following [RUNTIME-RESEARCH](RUNTIME-RESEARCH.md) and the
[three-agent protocol](_inbox/TEAM.md). The old end-only batching and operator-only language below
is historical. Preserve its useful state-vs-behaviour distinction; choose targeted captures by
current dependencies. Existing completion bars and mutation gates are unchanged.

**Almost nothing here needs the running game**, which is what makes deferring it cheap:

| item | why runtime |
|---|---|
| **BQ-27** | 1,606 deleting destructors whose bit-2 path calls a 3-byte `ret`. One breakpoint on `0016D6A0` with `rcx` non-null settles leak-vs-never-taken. **Static reading cannot.** |
| **BL-7** | as recorded in the register |
| **the 22 Phyre classes** | [the file/runtime schema join](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md) §3b falsified three static routes. Descriptors are zero-filled until run time; enumerating them after init settles all 22 in one pass. |
| **6 BLOCKED rows** | `AB-3`, `AP-5`, `AY-6`, `AY-10`, `BL-8`, `F-1` |

**Two open register rows out of 447 name runtime evidence as their route.** Everything else is
static. Batch the live work into one session at the end, per standing preference — and note the
debugger freezes this game, so it is Cheat Engine and breakpoints, not stepping.

### The tail is two different jobs, and only one of them needs the game running

**This distinction was not in the plan and it changes the ordering.** *State* questions and
*behaviour-over-time* questions look alike in the table above and are not alike at all:

| shape | question | what settles it |
|---|---|---|
| **state** | the 22 Phyre classes — *are these descriptors registered?* | **a full-memory snapshot.** Descriptors are static after init, so any moment past initialisation answers it. |
| **behaviour** | **BQ-27** — *does anything ever call `0016D6A0` with bit 2 set?* | **a breakpoint.** No snapshot can show a call that did or did not happen. |

> **A full-memory dump is a capture, not a debugging session.** Launch, reach an initialised scene,
> dump, close. Everything after that is offline analysis against a file — which suits a game the
> debugger freezes far better than live stepping does.

**So the live batch runs capture-first:** take one full-memory dump, close the game, then do the
state work offline; return to the game only for the breakpoint-shaped rows.

**Recorded because it was nearly lost:** 59 such dumps (203 GB, 2026-08-30) were found in the
install with `Memory64List` streams present, which would have made the 22 answerable with no capture
at all. **They were deleted on 2026-09-03 to reclaim the disk**, so the capture step is required
again. Not a mistake — 203 GB is a real cost and the capture is cheap — but the fact that the
evidence existed and was discarded belongs in the record rather than in nobody's memory.

---

## 6. Ordering

1. **Apply the 15 staged ledger rows** *(operator: project closed)*
2. `ebp_explained` — 14 units, smallest closed set
3. `registry_explained` — 58 slots, by reference count. **The highest value per unit of work in
   the plan**: these are the game's own content tables — unit definitions, items, actions, loot —
   and they are the difference between a database that explains the engine and one that lets
   somebody change the game.
4. **the JSON name-oracle join** — 137 map-parameter keys that are literal strings in the binary,
   each one xref from its reader ([ASSET-FORMATS.md](ASSET-FORMATS.md) §4c). **Not a new dimension**
   — it feeds `engine_explained` and 17-Presentation directly, and it is the cheapest route from an
   authored name to a documented struct field anywhere in the plan.
5. `formats_explained` — 48 formats, `sab` first
6. `ledger_resolved` — clusters first
7. **the two cheap outliers** — the managed .NET settings writer and the `.fst` size tables
   ([ASSET-FORMATS.md](ASSET-FORMATS.md) §7). Both are small, both are self-contained, and the
   .NET tool decompiles to near-source, which makes it the best effort-to-answer ratio on the list.
8. `engine_explained` — disposition C, then B, then A continuously
9. `questions_closed` — withdraw the malformed, close the rest as their work closes
10. **audit sweep** — the 27, then hold at zero
11. **live-game batch, capture first** — one full-memory dump, then the state work offline (the 22
    classes and whichever BLOCKED rows are state-shaped), then the game again for BQ-27 and the
    rest of the behaviour-shaped rows
12. `final_audits` — thirty consecutive passes, pass 5 first in practice

---

## 7. Out of scope, stated so it stays out

- **Tooling.** The database is the reference, not a toolbox. **Correction 2026-09-03: an extractor
  is no longer "still needed"** — `agent_flow/tools/vbfextract.py` reads the SRYK index and
  decompresses entries today, and `census_format_magics.py` samples the archive with it. The
  format work is therefore **not blocked on access**, which is what that line had implied.
- **Re-documenting middleware from the file side.** `.phyre`'s container is documented elsewhere and
  PhyreEngine is generic across titles. **Cross-link it** — that is what the `external` disposition
  is for, and it clears 40 % of the archive by count and 72 % by size in one row. The database's
  unique contribution is the loader contract — what the engine reads, rejects, clamps and ignores —
  and an `external` row still owes that half.
- **Bulk citation to move a metric.** See §3. If `engine_explained` ever jumps by thousands in one
  round, that is the defect, not the progress.

---

## The 0.55 dimension reads 8.9 % or 37.2 % depending on a rule nobody has chosen (OPUS, 2026-09-14)

`engine_explained` counts a function as explained when **any** address inside it appears in a
backticked citation on a documented page. `progress.py`'s own output has carried the caveat for
weeks — most of that numerator is **entry-only**, *"a mention, not an explanation"*, with
*"interior citation is a stricter PROXY, not a true count"*.

Both halves of that are right. **Neither was ever a measurement.** This is one.

Every backticked citation on every documented page, attributed to the function whose extent contains
it:

| | functions |
|---|---:|
| cited at all | 14,195 |
| cited **inside** the body | 3,405 |
| cited at the **entry only** | **10,790** |

| rule | explained | of the 38,161 ledger |
|---|---:|---:|
| entry counts — **as shipped** | 14,195 | **37.20 %** |
| interior, or entry and body < 32 B | 5,544 | 14.53 % |
| interior, or entry and body < 64 B | 7,109 | 18.63 % |
| interior, or entry and body < 128 B | 10,399 | 27.25 % |
| interior, or entry and body < 256 B | 12,131 | 31.79 % |
| interior, or entry and body < 512 B | 13,450 | 35.25 % |
| interior required — **the strict proxy** | 3,405 | **8.92 %** |

**A factor of four, on the dimension that is more than half the headline.**

### Why neither extreme is right, which the caveat never sized

The strict proxy is biased against small functions. `0020E600` is `mov eax, ecx / add rax,
[01F83530] / ret` — ten bytes, completely explained by naming it, and **it has no interior to
cite**. The shipped rule is biased the other way: a 3,000-byte body named once in a table is a
mention on any reading.

**The sizes say by how much.** Of the 10,790 entry-only functions:

| body size | count | share |
|---|---:|---:|
| under 32 B — *the entry IS the function* | 2,139 | 19.8 % |
| under 128 B | 6,994 | 64.8 % |
| 512 B or more — *a mention on any reading* | 745 | 6.9 % |
| 1,024 B or more | 317 | 2.9 % |

So the strict proxy would wrongly demote **at least 2,139**, the shipped rule wrongly promotes **at
most 745**, and **3,051** sit between 128 and 512 bytes where it is genuinely arguable.

### Not decided here

**This is OPUS's own headline**, and the rule chosen would be the rule OPUS's completion figure is
measured by. Routed to SWE2-AUDIT-SPEC as `OPUS-REQ-AUDITSPEC-ENGINE-EXPLAINED-RULE`, on the same
ground as the `formats_explained` ceiling. The recommendation is a **size-aware** rule rather than
either extreme, with the threshold chosen from evidence about what a function of a given size needs
before a reader can call it explained — **not from where the headline lands.**

### Two caveats on the figures above

- The denominator here is the **38,161-function ledger**; `progress.py` scores against **34,270**, so
  these percentages are not directly comparable to the headline.
- The entry-only count here is **10,790** against the scorer's **8,606** — a difference in how each
  attributes a citation to a body, and worth reconciling on its own before either number is quoted
  as settled.

*(Measured by `Tools/work/OPUS/measure_entry_only_sizes.py`, which is gitignored, so the figures are
recorded here rather than left in a tool nobody else can run. The method is one paragraph: every
`` `0x…` `` or `` `0…` `` citation, bisected onto the entry whose extent contains it, split on
whether the cited address equals that entry.)*

### Reconciled, and it is two axes rather than one (OPUS, 2026-09-14)

The section above said my entry-only count of 10,790 disagreed with the scorer's 8,606 and was
*"worth reconciling on its own before either number is quoted as settled"*. Reconciled: **the
difference is entirely method, and the scorer's population is the better one.**

`check_dispositions` counts a citation only when the citing page's front matter says
`status: DOCUMENTED`, and it excludes the 3,887 `Unwind@` / `Catch_All@` funclets. Applying both
gives **8,612 entry-only** against its 8,606 — a gap of six, which is the corpus moving under two
runs, not a disagreement. **My 10,790 was the looser population and the figures in the section above
are superseded by the ones here.**

**And the reconciliation turned up a second axis, which is the sharper finding.**

| rule | explained | of 34,270 |
|---|---:|---:|
| **any page**, entry counts — *what `engine_explained` ships* | 14,187 | **41.40 %** |
| DOCUMENTED pages, entry counts | 10,581 | 30.88 % |
| DOCUMENTED, interior or body < 256 B | 9,001 | 26.26 % |
| DOCUMENTED, interior or body < 128 B | 7,683 | 22.42 % |
| DOCUMENTED, interior or body < 32 B | 3,562 | 10.39 % |
| DOCUMENTED, interior required | 1,969 | **5.75 %** |

**`engine_explained` counts a citation on a page that does not claim `DOCUMENTED` status.** 14,187
against 10,581 — **3,606 functions are counted as explained on the strength of a mention in a
document the corpus does not itself claim to have documented.** That is a separate defect from the
entry-versus-interior one, it is larger than the small-function bias in either direction, and no
caveat in the scorer mentions it.

So the dimension that is more than half the headline spans **5.75 % to 41.40 %**, a factor of seven,
across **two** independent choices: *which pages count*, and *which citations count*. The first has
an obvious answer — a page that does not claim to be documented should not be evidence that a
function is explained — and it is still not mine to apply.

**The entry-only size distribution, on the correct population** (8,612 functions): under 32 B
**1,593 (18.5 %)**; under 128 B 5,714 (66.3 %); 512 B or more **481 (5.6 %)**; 1,024 B or more 182
(2.1 %). The shape is the same as the looser measurement reported and the conclusion is unchanged —
neither extreme is right, and a size-aware threshold is the only rule that is wrong in neither
direction.

### The last unsized precondition, and a third axis that cuts the other way (OPUS, 2026-09-14)

Of the terminal gate's four preconditions, `check_provenance` went green today, `unresolved = 0` is
30 rows with an owner, and the empty register was sized at 687. **"Every system documented" had
never had a number.** It does now.

| `status:` across the 368 system documents | | |
|---|---:|---:|
| `DOCUMENTED` | 185 | 50.3 % |
| `PARTIAL` | 129 | 35.1 % |
| **no `status:` line at all** | **47** | 12.8 % |
| `REOPENED` | 5 | 1.4 % |
| `CONTRACT READY` / `AUDITED` | 2 | 0.6 % |

Whole categories sit at zero: **`09-Combat-AI-And-Gambits` is 3 of 3 not documented**, and
`20-Platform-Online-Achievements` is 2 of 2.

### The 47 are not unstatused, and that is the finding

**Every one of them is a CONTRACT page using `readiness:` instead of `status:`** — and on the
*higher* ladder: `BEHAVIORALLY UNDERSTOOD` 21, `CONTRACT READY` 13, and thirteen more at
`DIFFERENTIAL TESTED` or `RUNTIME VALIDATED`, several naming the diff run and the mutants it killed.

**The corpus writes two status vocabularies and the tooling reads one at a time.** Twelve kit tools
mention `DOCUMENTED`; a different set reads `readiness`. `check_dispositions` gates its entire
measurement on `^status:\s*DOCUMENTED$`, so a contract at `DIFFERENTIAL TESTED` — the strongest
evidence class the project has — contributes exactly as much as a page nobody wrote.

**Measured:**

| | functions |
|---|---:|
| cited by a `DOCUMENTED` page | 10,581 |
| cited by one of the 47 contracts | 1,084 |
| **cited by a contract and by NO documented page** | **386** |
| cited **inside the body** by such a contract | 353 |
| **of those, invisible to the gate** | **88** |

### So the dimension is wrong in both directions, and both magnitudes are now known

- **Over-counting**: 3,606 functions counted on a citation from a page that does not claim
  `DOCUMENTED` status, and 481 entry-only citations of bodies 512 bytes or larger.
- **Under-counting**: **88 functions whose bodies are cited from the inside by a contract at the top
  of the readiness ladder**, which the strict measure scores as nothing at all.

That is a third axis — *which vocabulary counts* — on top of *which pages* and *which citations*.
The first two both shrink the figure; this one grows it. **A correction that only ever moved the
number one way would be the thing to distrust**, and finding one that moves it the other way is the
check on the other two.

**Still not decided here**, for the same reason: it is OPUS's headline. Routed with the rest to
SWE2-AUDIT-SPEC.

### The three axes are adjudicated, and these sections are now history (OPUS, 2026-09-14)

The three sections above measured `engine_explained` three ways in one day — which pages count, which
citations count, which vocabulary counts — and each ended the same way: *"still not decided here,
because it is OPUS's own headline."* **SWE2-AUDIT-SPEC decided it** (`9efc6221`), and OPUS
implemented it (`4d9990d6`).

**They re-derived all three axes independently before choosing.** Their figures against mine:
14,204 / 10,597 / 1,987 against 14,187 / 10,581 / 1,969 — every one inside corpus drift. The
measurements above are confirmed; what changes is their standing.

> **The rule.** A function counts when an **evidence-bearing** page cites it — `status: DOCUMENTED`
> or `AUDITED`, **or** `readiness:` at `BEHAVIORALLY UNDERSTOOD` or above, one ladder rather than two
> vocabularies — and the citation is **strictly interior**, or an **entry cite of a body under 128
> bytes** (the leaf-helper boundary).

| | then | now |
|---|---:|---:|
| `engine_explained` | 41.45 % | **23.55 %** |
| `OVERALL` | 60.19 % | **50.34 %** |

**The tables above are kept unedited.** They are what was measured, and the spread they report — 5.75 %
to 41.40 % — is the reason a rule had to be chosen rather than assumed. `progress.py` now prints that
spread beside the headline for the same reason. **A figure quoted from those tables as CURRENT is
stale; quoted as the measurement that produced the rule, it stands.**

*(This note exists because changing the rule staled every figure that quoted the old one. Swept: 18
unmarked mentions across 5 documents, of which 7 are these sections and 6 are dated resume
checkpoints. The corpus dates its figures well enough that the propagation debt from a
seventeen-point move in the headline dimension is one paragraph.)*
