# The knowledge schema — charter §7

**Tool:** `Database/Tools/analysis-kit/gfz-scripts/knowledge_db.py`
**Artifact:** `Database/Tools/work/knowledge/knowledge.sqlite` — **gitignored, rebuilt in ~1 second.**

```
knowledge_db.py build          rebuild the index from the documents and side files
knowledge_db.py queries        the charter §7 query list, with what is and is not answerable
knowledge_db.py query <name> [arg]
knowledge_db.py sql "SELECT …"
knowledge_db.py info           row counts
```

## 1. Why an index and not a migration

Charter §7 says *"do not preserve a weak schema to avoid migration work."* It does **not** say
replace the prose, and the goal revision says in as many words: **do not start over, do not discard
existing evidence, indexes, schemas or tooling.**

So this is a **derived index**. The markdown documents remain authoritative; nothing was moved into
the database and nothing depends on it. That choice has one property no hand-maintained structure
has:

> **A derived index cannot silently disagree with its sources.** `ADDRESS-INDEX.md` was
> hand-maintained until it held 74 addresses against 6,504 cited — two orders of magnitude behind,
> and nobody noticed. Rebuild takes a second here, so drift has nowhere to live.

## 2. What is in it

**Row counts are from one build and move every block. `knowledge_db.py info` prints them fresh —
regenerate rather than quote this table**, the same rule that applies to every count in this database.

| table | rows | source |
|---|---:|---|
| `documents` | 222 | every `.md` with frontmatter (**218** real + **4** template/experiment) |
| `doc_fields` | 3,804 | the long tail of frontmatter keys, unflattened |
| `citations` | 12,537 | backticked addresses, resolved to the containing function |
| **`doc_names`** | **6,448** | **names documents give addresses** — added 2026-09-08, see below |
| `functions` | 38,161 | `work/graph/functions.tsv`, with `is_eh` and `is_generated` |
| `edges` | 90,525 | `work/graph/edges.tsv`, **with `caller_is_eh`** |
| `global_refs` | 164,489 | `work/h78/rip_data_refs.tsv` — read/write, per site |
| `types` / `fields` | 2 / 81 | `_types/*.tsv` |
| `questions` | 826 | `_index/OPEN-QUESTIONS.md` |
| `script_verbs` | **1,224** | `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-dispatch.tsv` |
| `contradictions` | **33** | `_index/CONTRADICTIONS.tsv` |
| `reconstructions` | 4 | `Reconstruction/` — 2 implementations, 2 differential tests |

Of the 12,537 citations, **7,338 resolve to a distinct function body** and **1,920 resolve to none**
— data addresses, jump tables and image offsets. The index keeps both; a null `resolved_entry` is a
fact about the address, not a failure.

### `caller_is_eh` is a column, on purpose

`edges.tsv` contains caller edges whose source is an unwind funclet or catch handler — the exact
evidence class the mission prompt bans, which cost a prior branch 182 classifications, and which an
ordinary `awk` hands you by default. The census is **3,834 of 90,525 edges (4.24 %)**.

> **Materialising the flag turns "remember to filter" into "write a `WHERE` clause you can see."**
> Every built-in query either excludes EH sources or prints both counts side by side
> (`callers` vs `callers-including-banned`).

## 3. What §7 asks for, and what this can answer

**19 of the 24 tracked queries are supported. Four are not, and those four are the honest map of
what the database does not yet record.**

> **Two more became supported on 2026-09-08.** The contradiction gap — which this file called
> *"the single biggest"* — closed with [`CONTRADICTION-LEDGER.md`](CONTRADICTION-LEDGER.md):
> 33 dated correction headers extracted mechanically, summaries hand-written, and a
> `contradictions-by-instrument` query whose first answer is that **`E8-only-reachability` is
> tied for the most frequent cause of a wrong answer in this database's history.**
>
> **And one became supported without anything new being derived.** The
> entry read *"no machine-readable opcode → native-entry table has been extracted"*. **That was
> wrong.** 1,224 rows had been extracted long before and were sitting in a **gitignored scratch
> directory**, with the dispatch document pointing readers at that path. The table was re-derived
> from the binary, imported with per-column provenance, and wired in. **An "unsupported" verdict can
> be a search failure rather than a data gap, and this one was.**

| not supported | what would have to exist first |
|---|---|
| every known **writer of a field** | `global_refs` is address-keyed, so it names writers of a *global* but not of `obj->field`, which is `[reg+disp]` with the object identified only by dataflow. **Needs a per-type field xref pass.** |
| every **resource** referenced by a subsystem | no resource record type; resource ids live inside prose. |
| behaviour known, **parameters unresolved** | needs per-function signature records. `functions.tsv` carries none, and only the 2 contracts declare signatures parsably. |
| subsystems depending on a **state machine** | no state-machine record type; transitions live in contract §7 prose. |

## 4. What the index measured on its first run

Running the census queries against the real corpus produced the number this program most needs to
look at:

| | value | of | share |
|---|---:|---:|---:|
| documents stating a **maturity level** (`L1`/`L2`/`L3`) | **6** | 218 | **2.75 %** |
| documents stating a **readiness rung** | **6** | 218 | **2.75 %** |
| behavioural contracts | 2 | 218 | 0.92 % |
| type fields still `UNRESOLVED` | 34 | 81 | 42.0 % |
| implementations without a differential test | **0** | 2 | — |

> **The charter's own vocabulary is present in 2.75 % of the corpus.** Every §7 query of the form
> *"all reconstruction-ready functions"* or *"everything at L2"* is therefore answerable **and
> nearly empty** — not because the work is not there, but because 212 documents predate the
> vocabulary and have never been re-labelled. **That is a labelling backlog, not a knowledge gap,
> and it is now measurable instead of assumed.** Filed as `DJ-1`.

### This is not the same measurement `COVERAGE-DIMENSIONS.md` reports

That file's §7 says *"readiness rungs named in documents — `CLASSIFIED` in 33, `IMPLEMENTED` in 23,
`DISCOVERED` in 5."* **Both numbers are correct and they count different things.**

| | instrument | counts |
|---|---|---|
| `COVERAGE-DIMENSIONS.md` | the rung word appears **anywhere in the prose** | a *mention* — a document may be discussing the rung, not claiming it |
| `readiness-census` here | the `readiness:` **frontmatter key** | a *claim about this document*, and the only form a query can act on |

**Only the second is machine-queryable**, which is the whole point of §7. A rung named in a sentence
cannot answer *"list everything at CONTRACT READY"*. Neither number should be quoted without saying
which instrument produced it.

## 5. Three defects the cross-checks caught

The index was validated by making it answer questions this session had already answered by other
means. **Every one of the three disagreements was the index being wrong.**

| symptom | cause | fix |
|---|---|---|
| 813 questions read, gate reads **824** | a second regex over `OPEN-QUESTIONS.md`, missing two-column and continuation rows | **import `check_questions.py` and call its parser.** One file, one parser. |
| **3** contracts, `program_coverage.py` says 2 | `_templates/CONTRACT.md` carries `contract:` and `scope:` because it *is* the shape of a contract | `is_template` column; every built-in query filters it |
| **28** readers of `02F9736C`, `globals_index.py` says 27 | one row per *site*, not per *function* — `002A9980` reads twice | group by function, return a site count, name the unit |

> **Both tools were right in the third case.** They answered different questions and their row counts
> silently meant different things. That is the trap this whole project keeps re-encountering, and the
> fix is never to pick a winner — it is to make the unit visible in the output.

Two checks passed unchanged and are the reason the rest is trusted: the EH-edge census reproduced
**3,834 / 90,525** exactly, and `callers 0017DB90` reproduced the two `awk`-derived callers.

## 5a. The readiness ladder is two axes printed as one line — 2026-09-13 (OPUS, canonical acceptance rule)

§4 above records, as an aside, that *"the ladder says seven documents sit above a rung nothing has
reached."* Measured properly it is **six**, the shape is exact, and the cause is not that anyone
overclaimed.

### The measurement

The template declares one ordered sequence:

```
DISCOVERED · CLASSIFIED · SEMANTICALLY IDENTIFIED · SIGNATURE RESOLVED · TYPE RESOLVED ·
DEPENDENCIES RESOLVED · BEHAVIORALLY UNDERSTOOD · RUNTIME VALIDATED · CONTRACT READY ·
RECONSTRUCTION READY · IMPLEMENTED · DIFFERENTIAL TESTED · PARITY CERTIFIED
```

Across the **47** contracts the `readiness:` frontmatter reads:

| rung | contracts |
|---|---:|
| `BEHAVIORALLY UNDERSTOOD` | 22 |
| `CONTRACT READY` | 15 |
| `DIFFERENTIAL TESTED` | 6 |
| `RUNTIME VALIDATED` | 1 |
| `RUNTIME VALIDATED and DIFFERENTIAL TESTED` | 1 |
| `SPECIFIED` — **not a rung on the ladder at all** | 1 |
| **absent** | **1** (`CONTRACT-transform-primitives.md`) |

**Five of the six `DIFFERENTIAL TESTED` contracts say, in their own §13, `"Live capture: still
absent"`** — `CONTRACT-field-record-accessors`, `CONTRACT-battle-target-buffer`,
`CONTRACT-gambit-walk`, `CONTRACT-coast-down-latch`, `CONTRACT-gameplay-generators`. The sixth,
`CONTRACT-field-music-selection`, cites `EXP-008`. So five contracts sit **five rungs above**
`RUNTIME VALIDATED` while declaring they have not been runtime validated.

### The cause, which is not overclaiming

**The two rungs measure different things and neither implies the other.** `RUNTIME VALIDATED` is a
fact about the *original* — it was observed in a running game. `DIFFERENTIAL TESTED` is a fact about a
*reconstruction* — its output was compared against the shipped bytes executing in isolation. **A
reimplementation can be compared instruction-for-instruction against original code that has never been
watched in a live process**, and that is exactly what those five did.

> **Printed as one line, the ladder makes that combination look like a skipped step.** It is not a
> skipped step; it is the other axis. *Evidence about the original* and *distance travelled by the
> reconstruction* are independent, and every apparent violation here is a contract that advanced on
> one axis without advancing on the other.

### The rule, so a gate does not have to guess

1. **A rung word is not orderable on its own and must not be compared with `>`**. Nothing may infer
   "runtime validated" from "differential tested", in either direction.
2. **The readiness gate reads `§13`, not the rung.** Whether live evidence exists is a question about
   that section's content, which is why `check_contract_runtime_links.py` resolves §13 in both the
   numbered and short-form templates rather than trusting frontmatter.
3. **`SPECIFIED` and an absent `readiness:` are schema holes, not low rungs** — a contract with no rung
   drops silently out of every rollup. Both are named above; neither is invented a value here, because
   assigning one is the owning author's call and guessing it is the failure this file exists to stop.

**Nothing is demoted and no rung is rewritten.** Six contracts' labels are correct under rule 1, and
were only ever "above a rung nothing reached" under a reading the ladder's own two axes do not support.

## 6. What this deliberately does not do

- **It does not replace grep.** Prose is still prose; the index knows a document's frontmatter and
  its addresses, not its argument.
- **It does not assert anything.** Every row is copied from a source that already existed. If a
  document is wrong, the index is wrong in the same way, which is the correct behaviour for a
  derived artifact.
- **It is not a gate.** No check fails because of it. Making it a gate would mean trusting it more
  than the documents.

## 7. `doc_names` — added 2026-09-08, because the index could not see this database's names

[the reconstruction-grade audit](RECONSTRUCTION-GRADE-AUDIT.md) measured §3's **Identity** dimension and found the
index answering it with the wrong file. `functions.tsv` names **677** of the 7,376 function
entries documents cite — **9.2 %**. The documents themselves name **5,319–5,812** of them —
**72.1 % to 78.8 %**. **Every machine query ever asked here about identity was reading the
export instead of the source, and understating it roughly eight to one.** `DU-1`.

`doc_names` holds `(path, address, name, resolved_entry, is_entry, is_generated_index)`, built
in the existing document traversal by **importing** `check_consistency`'s `NAME_PATTERNS` and
its `SUPERSEDED_SECTION` rule — the same discipline already applied to the question parser and
the runtime-marker list, and for the same reason: **two definitions of one concept drift, and
the drift is silent.**

| query | answers |
|---|---|
| `identity` | the five-row census, with its denominator and both bounds |
| `named-in-prose-not-in-ledger` | **the export backlog** — this database has the name, the ledger does not |
| `unnamed-cited` | functions a document cites that nobody has named anywhere |

### Two decisions worth reading before trusting the number

**`is_entry = 1` is load-bearing.** A name written against an address *inside* a body —
``0032ABC8` | the clear arm` — names a point, not a function. Counting those inflated the
first run by exactly **6**. Restricting to entry addresses reproduces `check_consistency.py`'s
own figure to the row, and that reproduction is the control this query is checked by.

**The answer is a range and stays one.** `NAME_PATTERNS` was written for *disagreement*
detection, where a loose match is harmless because it fires only on a conflict. As a **census**
the looseness shows: ``0040FF30` | embedded` matches and so does
``0072A320` | TEXSHADERSET_CreateEffect`. Requiring an identifier shape gives **5,319**; the raw
match gives **5,812**; the 493 between are a real mix of `PArray`/`IGPUDevice` (Phyre types
with no internal capital) and `enqueue`/`heaviest` (prose). **Neither bound is narrowed
further, because the narrowing rule would itself be a guess.**

### What it does not do

**It does not write the names back.** `named-in-prose-not-in-ledger` is a *list*, and applying
5,000 unreviewed names to the certified ledger would be precisely the *“large quantity of
speculative labeling”* charter §28 forbids. A name in a document is a **claim**; the ledger is
an artifact. The write-back needs a review gate and is `DU-2`.

## 8. `contract_sections` and `contract_claims` — added 2026-09-08

[The reconstruction-grade audit](RECONSTRUCTION-GRADE-AUDIT.md) reported **Behaviour** as the
one §3 dimension that could not be asked at all, because *“the schema has nowhere to put
preconditions, postconditions, invariants, state transitions or failure paths outside contract
prose”*. **The resolution was not a new record type. It was noticing that contract prose already IS one.**

| table | rows | source |
|---|---:|---|
| `contract_sections` | **115** | one row per numbered heading in each of the 7 contracts |
| `contract_claims` | **63** | the §15 evidence table: claim, evidence, tier, confidence |

**This is parsable because the corpus is disciplined, not because the parser is clever.** Every
numbered heading from **2 to 16 appears in all seven contracts**; §1 is the only variance (six
say *Purpose*, one says *What the player sees*). §§**4, 5, 7, 10 and 12** are exactly the
charter's preconditions/invariants, state read and written, state transitions, failure paths
and reproduction formula.

| query | answers |
|---|---|
| `behaviour` | per contract, the size of each behaviour-bearing section |
| `contract-claims` | all 63 claims with their tier and confidence |
| `unresolved-claims` | the claims a contract itself marks `UNKNOWN` or leaves untiered |

### Columns are mapped by header, not by position

Six contracts write `| claim | evidence | tier | confidence |`; **`CONTRACT-widget-object.md`
writes `| claim | evidence | tier |`** with no confidence column. Reading column four
positionally would have **invented a confidence for six documents and lost it for one**. The
parser reads the header row and looks columns up by name, and the six rows with no confidence
come back empty rather than wrong.

### What the first run found

**63 claims: 44 `PROVEN`, 11 `UNKNOWN`, 2 `VERY HIGH`, 6 with no confidence column.** And of
the 11 unknowns, **five are the same claim** — *“any runtime observation — none exists”* —
written independently by five different contracts.

> **That is `EXP-001` measured from a direction the readiness ladder cannot see.** The ladder
> says seven documents sit above a rung nothing has reached; this says the contracts' own
> evidence tables name the same absence five times over. **Two independent instruments, one
> blocked experiment.**

It also surfaces thin sections without anyone having to read for them: **`CONTRACT-field-music-selection.md` §7 is 29 characters** — a state-transitions section that says there are none.
Whether that is correct or merely unwritten is now a visible question rather than an invisible
one.

### What it does not do

**It measures the presence and size of a section, not its quality.** A 3,000-character failure
-paths section is not thereby a good one, and `chars` is a proxy stated as one. The index makes
the dimension **askable**; answering it well is still writing.
