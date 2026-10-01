# Reconstruction roadmap — which subsystem is closest, and why

**Tool:** `Database/Tools/analysis-kit/gfz-scripts/readiness_rank.py` ·
**Data:** [`READINESS-RANK.tsv`](READINESS-RANK.tsv)

Charter §38 asks the program to **identify subsystems near reconstruction readiness** and to build a
**prioritized roadmap**. Both were still open, for a reason the database already knew: **the readiness
ladder is stated in the frontmatter of 6 of 221 documents, as measured 2026-09-08** (`DJ-1`; the
corpus is 365 documents at 2026-09-14, so this is a reading of its date). The column that would
answer this directly is empty, so the ranking comes from the preconditions instead.

## 1. What is measured, and what is not

| signal | meaning |
|---|---|
| `contracts` | a behavioural §4 contract exists — **the strongest single signal** |
| `types` / `fields` | entries in `_types/` — *a contract without types is prose* |
| `cited` | distinct functions this category's documents cite, **wherever owned** |
| `owned` / `cov%` | functions the ledger assigns to this category's owner, and **how many of those any document cites** |
| `rt` | documents containing a runtime-evidence marker — **see §4, this one is over-counted** |
| `corr` | recorded corrections, from [the contradiction ledger](CONTRADICTION-LEDGER.md) |

**No composite score is emitted.** A single number would hide *which* signal is missing, and which
one is missing is the whole output.

> ### `cited` and `cov%` are different populations, and the first version conflated them
>
> Dividing *"functions this category's documents cite"* by *"functions this owner owns"* gave
> **313 % for `14-Story-Event-Quest-Hunt`**, because a category's documents freely cite functions
> another category owns. `cov%` is now the **intersection** — functions owned by X that any document
> cites, over functions owned by X — and cannot exceed 100 %.

## 2. The ranking

**Only three categories have a contract, and only one has all four signals non-zero.**

| | contract | types | fields | cov% | verdict |
|---|---:|---:|---:|---:|---|
| **19-Save-Load-Settings** | **1** | **1** | **40** | 34.5 | **closest** — the only category with a contract, a type and coverage |
| 16-UI | 1 | ~~0~~ **1** | ~~0~~ **15** | 7.0 | ~~contract, no types~~ — **`Widget` added 2026-09-08**, acting on this page |
| 18-Audio | 1 | ~~0~~ **1** | ~~0~~ **6** | 25.7 | ~~contract, no types~~ — **`AudioParameterRamp` added 2026-09-08** |

> **This page named those two gaps and the next block closed them.** GAME types in the store moved
> **2 → 4** and fields on a game type **81 → 109**. The table above is left with its original
> figures struck through rather than overwritten, because a roadmap that silently rewrites itself
> cannot be checked against what it recommended.

**Small subsystems that are nearly fully attended**, and would be cheap to finish:

| | owned | cov% | docs | |
|---|---:|---:|---:|---|
| 14-Story-Event-Quest-Hunt | 15 | **100.0** | 2 | — **taken 2026-09-08: all 15 read, disposition A** |
| 10-Status-Periodic-Terminal | 24 | 91.7 | 3 |
| 13-Rewards-Progression-Economy | 38 | 78.9 | 8 |
| 21-RNG-And-Determinism | 18 | 77.8 | 2 |
| 05-Spawn-Encounter-Lifecycle | 52 | 67.3 | 4 |

**Large subsystems that are barely touched**, where a document costs the same and buys less:

| | owned | cov% |
|---|---:|---:|
| 17-Presentation-Rendering | 1,564 | **5.9** |
| 01-Script-VM-Native-Bridge | 1,900 | 6.8 |
| 16-UI | 544 | 7.0 |
| 02-Resource-And-Asset-Pipeline | 572 | 8.9 |
| 15-Input | 1,047 | 15.3 |

> **This page's small-category recommendation was acted on.** `14-Story-Event-Quest-Hunt` cost
> one block to finish, and **three of its fifteen functions were already read** — the work was
> the measurement, not the reading. `cov%` was 100.0 before and after: **the metric could not
> see the difference**, which is §3's caution demonstrated rather than asserted.

> **The actionable reading.** `19-Save-Load-Settings` is the only subsystem where the next
> reconstruction step is obvious and small. `16-UI` and `18-Audio` each need **a type in `_types/`**
> before their contract is more than prose. And the five small categories above are the cheapest
> places to take a subsystem from *mostly attended* to *complete*.

## 3. The gate nothing passes

The charter gates reconstruction readiness on **runtime validation**. Correcting for §4 below,
**no category has a document that positively asserts live-process observation of the system it
documents.** The ranking above is therefore advisory: it says which subsystem is closest to the gate,
not that any subsystem has reached it.

`EXP-001` remains the shortest path — it is written, and it needs the game at the title screen.

## 4. A metric defect found while building this

`program_coverage.py` has long reported **"documents citing any runtime/live-process evidence"** by
searching the body for markers: *cheat engine, breakpoint, livelab, live process, runtime trace,
observed in game, debugger, attached to the process, tier 10, runtime-confirmed*.

**Those markers match negations.** Of 17 documents containing one, **at least 3 have every
occurrence inside an explicit denial** — including two contracts written this session whose sentence
is, verbatim:

> *"Nothing in this contract has been observed in a live process."*

**A document is being counted as runtime-evidenced for saying it has no runtime evidence.**

> **The over-count is a floor, not a total.** A 110-character negation window catches *"Nothing …
> has been observed in a live process"* but not a marker sitting under a **"What this document does
> not claim"** heading, which is how several others are phrased. So the true figure is somewhere
> below 14 and at most 14, and this page does not guess where. `DR-1`.

The marker list is now **imported** by `knowledge_db.py` rather than copied — an earlier copy dropped
four markers and reported 11 where the owning tool reported 14, which is the same drift the question
ledger produced before its parser was shared.

## 5. What this roadmap does not do

- **It does not rank by readiness.** It ranks by preconditions, because readiness is unstated in
  215 of 221 documents, as measured 2026-09-08 (365 at 2026-09-14). Closing `DJ-1` would replace
  this page with a direct query — which is the durable fix, since a ratio typed into prose is
  correct for a week and a generated one is correct always.
- **It cannot rank `00-Engine-Core-Runtime`, `22`, `23`, `24`, `25`, `26` or `99`** — no ledger owner
  maps to them, so `cov%` is blank rather than divided by a guess. They are cross-cutting, and an
  ownership ratio for them would be meaningless rather than merely missing.
- **`cov%` counts citation, not understanding.** A function named once in a table is "covered" by
  this measure. It is an attention proxy and nothing more.

## The data file is current again; the tables below are the snapshots they were written from — 2026-09-13 (OPUS)

[`READINESS-RANK.tsv`](READINESS-RANK.tsv) had been **committed 2026-09-10 and every one of its 28
category rows was stale** — `04-Actor-Entity` read 93 cited functions against 698, `19-Save-Load-Settings`
1 contract against 4, `17-Presentation-Rendering` 0 against 4. Regenerated (it is a pure generated file,
so regenerating it destroys no prose) after rebuilding the knowledge index, which was itself two days
old.

**This page's own tables are older still, and are left as written.** They are dated recommendations and
the page says so — *"cannot be checked against what it recommended"* — so rewriting them would erase the
record of what was advised. But the recommendation *"small subsystems that are nearly fully attended,
and would be cheap to finish"* has largely come true, and the current figures say so:

| | this page says | now |
|---|---:|---:|
| `14-Story-Event-Quest-Hunt` | 100.0 % | **100.0 %** |
| `10-Status-Periodic-Terminal` | 91.7 % | **95.8 %** |
| `13-Rewards-Progression-Economy` | 78.9 % | **89.5 %** |
| `21-RNG-And-Determinism` | 77.8 % | **83.3 %** |
| `05-Spawn-Encounter-Lifecycle` | 67.3 % | **98.1 %** |

**Every one moved up, and the largest move is the one the page ranked last.** `05-Spawn` went from
67.3 % to 98.1 %. **Read the TSV for current numbers and this page for what was recommended and when** —
they are different questions and the file no longer pretends otherwise.
