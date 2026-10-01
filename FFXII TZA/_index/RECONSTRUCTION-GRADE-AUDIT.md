# The database against the charter's own standard

**Tool:** `Database/Tools/analysis-kit/gfz-scripts/charter_grade_audit.py` ·
**Data:** [`RECONSTRUCTION-GRADE-AUDIT.tsv`](RECONSTRUCTION-GRADE-AUDIT.tsv)

> ### ⚠ THIS FILE IS MIXED GENERATED AND MANUAL. Do not regenerate it over itself.
>
> `charter_grade_audit.py --out <this path>` emits **35 lines**; this file is **195**. The
> difference is curated prose — the naming-range analysis, the dimension narratives, the debt
> reading — that the generator does not produce and will silently discard. Running the tool onto
> the canonical path replaces a mixed file with a pure generated approximation, which is exactly
> what [TEAM.md](_inbox/TEAM.md)'s shared-files table forbids.
>
> **Found 2026-09-10 by doing it.** OPUS regenerated over this path while refreshing the stale
> figures, lost 160 lines, and restored them from git because the change had not been committed.
> Nothing was published. **Regenerate to a scratch path and merge the numbers by hand**, or teach
> the tool to preserve the prose first.
>
> ~~Numbers refreshed by hand from a scratch run, 2026-09-10~~ **Refreshed again by hand,
> 2026-09-13 (OPUS), from a scratch run: the table below now carries them, so it no longer
> disagrees with its own instrument.** The 2026-09-10 note said the table “still reads 183 /
> 722 / 4” while the data was 206 / 880 / 27; it now reads **239 / 1,764 / 60**, and every
> superseded figure is struck through rather than deleted. **The Runtime row's verdict is
> unchanged and that is still the point** - 1 document of 305 claims the rung, it was the
> blocker in September and it is the blocker now.

Charter §38 lists *"audit the database against the reconstruction-grade requirements (§3)"* as a
first action. **It has been open since the program began.** Every readiness statement so far has
been by proxy — contracts held, types declared, runtime evidence counted — and nobody had checked
the database against the definition of the quality it is trying to reach.

## 1. The §3 dimensions

§3 names seven. Population for the per-function rows is **the 7,376 distinct function entries any
document cites** — this database's own definition of *important*, being what somebody bothered to
write about. It is a proxy and is stated as one.

| dimension | measurable | value | instrument |
|---|---|---|---|
| **Identity** | yes | ~~5,319–5,812 / 7,376; 677 in the ledger~~ **5,506–6,087 / 10,885 named in prose; 1,083 in the ledger** | `knowledge_db` `doc_names` vs `functions.tsv` |
| Identity (owner) | yes | ~~1,596 / 7,376~~ **3,145 / 10,885 owned** | `functions.tsv` owner, joined to citations |
| **Interface** | yes | ~~3 / 224~~ ~~32 / 305~~ **46 / 348** documents declare signatures | contract §2 is the only parsable signature record |
| **Data** | yes | ~~183 types / 722 fields; 4 GAME types~~ ~~239 / 1,764 / 60~~ **247 types / 1,858 fields; 65 GAME types** | `_types/`, validated by `types_index.py` |
| **Behaviour** | ~~**NO**~~ **yes** | ~~7 / 229 documents; 63 claims, 11 `UNKNOWN`~~ ~~32 / 305; 227 claims~~ **46 / 348 documents; 706 claims, 50 `UNKNOWN`** | `knowledge_db` `contract_sections` §§4/5/7/10/12 + `contract_claims` — **closed 2026-09-08** |
| **Relationships** | yes | ~~9,104~~ **10,885 / 10,885** | `edges.tsv` with `caller_is_eh` filtered — **true by construction** |
| **Runtime** | yes | ~~0 / 224~~ ~~1 / 305~~ **2 / 348 claim the rung; 4 linked to a VALIDATED experiment (11 of 82 validated)** | readiness frontmatter, and EXP citations resolved against `_experiments/` status |
| **Validation** | yes | ~~15 / 224~~ ~~81 / 305~~ **95 / 348** carry a confidence label | frontmatter; `DJ-1` is the labelling backlog |

### What moved between 2026-09-10 and 2026-09-13, and what did not — (OPUS)

Refreshing the table by hand from a scratch run makes one comparison available that neither date could
make alone. **Every dimension grew, and the verdict did not change.**

| dimension | 2026-09-10 | 2026-09-13 |
|---|---|---|
| Identity (named in prose) | 5,319–5,812 / 7,376 | **5,403–5,931 / 9,104** |
| Identity (owner) | 1,596 / 7,376 | **2,364 / 9,104** |
| Interface | 3 / 224 | **32 / 305** |
| Data | 183 types / 722 fields / 4 GAME | **239 / 1,764 / 60** |
| Behaviour | 7 / 229 docs, 63 claims | **32 / 305 docs, 227 claims** |
| Validation | 15 / 224 | **81 / 305** |
| **Runtime** | **0 / 224** | **1 / 305** |

> **The denominator moved too, from 7,376 functions to 9,104 and from 224 documents to 305**, so the
> ratios are not directly comparable and none of them should be quoted as a percentage change. What is
> comparable is the *shape*: contracts went from 3 declaring signatures to 32, the type store more than
> doubled its fields, and **`RUNTIME VALIDATED` went from 0 to 1.**
>
> **That last row is the finding, exactly as it was in September.** One document of 305 claims the
> rung. Four more cite an experiment the `_experiments` corpus marks `VALIDATED`, and **11 of 82
> experiments are validated at all.** The charter's Runtime dimension is not close, and three days of
> real growth everywhere else did not move it.

**A stale table was disagreeing with its own instrument for three days**, with the disagreement written
in its own banner — *"the table below still reads 183 / 722 / 4"*. It now reads what the tool says, and
every superseded figure is struck through rather than deleted.

### The naming effort is trapped in prose, and every machine query has been understating it

**The database has given a semantic name to between 5,319 and 5,812 of the 7,376 function
entries it cites — 72.1 % to 78.8 %. The ledger it exports to carries a name for 677 —
9.2 %.** 1,316 have no name anywhere; 248 are named in the ledger and in no document.

> **Why a range, corrected 2026-09-08 after this page first said 5,812.** The count comes
> from `check_consistency`'s `NAME_PATTERNS`, which were built for **disagreement
> detection** — two different names for one address — where a loose match is harmless
> because it fires only on a conflict. **Used as a census the looseness shows.** Both
> ``0040FF30` | embedded` and ``0072A320` | TEXSHADERSET_CreateEffect` match, and only one
> is a name. Requiring an identifier shape — an underscore, an internal capital, a `::` or
> a `.` — gives **5,319**; the raw match gives **5,812**. The 493 in between are a genuine
> mix: `PArray`, `IGPUDevice`, `IGPUSurface` are real Phyre type names with no internal
> capital, while `enqueue`, `heaviest` and `registers` are prose. **Neither bound is
> narrowed further, because the narrowing rule would itself be a guess.**
>
> **The conclusion is unchanged by the correction.** Against the ledger's 9.2 %, even the
> lower bound is an eight-fold understatement.

> **This is an eight-to-one understatement in the one dimension the database is strongest at.** Any
> tool asking *"is this function identified?"* against `functions.tsv` — which is every tool here
> that has asked it — gets 9.2 % for something that is **at least 72.1 %** true. §3's **Identity**
> is very nearly satisfied over the cited population and no instrument could see it.
>
> **A name written in a document had never flowed back into the export. Fixed 2026-09-08**,
> in the block after this page was written: `knowledge_db.py` now
> carries a **`doc_names`** table — 6,448 rows — built by **importing** `check_consistency`'s
> patterns rather than restating them, and three queries read it: `identity`,
> `named-in-prose-not-in-ledger` (the export backlog, biggest first) and `unnamed-cited`
> (functions a document cites and nobody has named). **§3's first dimension is now
> answerable from the schema.** `DU-1`.

~~**Behaviour is the one dimension that cannot be asked at all.**~~ **CLOSED 2026-09-08.**
§3 wants preconditions, postconditions, invariants, state read and written, side effects,
allocations, branches, state transitions, failure paths, edge conditions. This page said the
schema had nowhere to put any of it outside contract prose — **and the answer turned out to be
that contract prose IS the record type, and simply had no index.**

> **The seven contracts share an exact 16-section skeleton** — every numbered heading from 2
> to 16 appears in all seven — so §§4, 5, 7, 10 and 12 are precisely the charter's
> preconditions, state, transitions, failure paths and reproduction formula. `knowledge_db.py`
> now indexes them: **115 sections and 63 claims**, with three queries over them. See
> [the schema page](KNOWLEDGE-SCHEMA.md) §8.
>
> **Askable is not covered, and the number says so**: 7 of 229 documents, measured 2026-09-08
> (365 at 2026-09-14). The dimension went
> from *unanswerable* to *answered small*, which is a different and better kind of gap.

**No keyword proxy was invented for it at any point** — that is exactly how `DR-1` happened,
where a marker list counted documents *denying* runtime evidence. The index reads structure
the documents already have, not words they happen to contain.

## 2. Rung debt — four documents stand above a rung nothing has reached

The ladder is written as one ordered sequence, so a document at rung *N* asserts rungs 1…*N*. Six of
the thirteen rungs have a mechanically checkable criterion; the other seven are reported
`not-evaluable`, never as passing.

**15 of 224 documents carry a readiness label at all, as measured 2026-09-08 (6.7 %, `DJ-1`; 365
documents at 2026-09-14), and 10 of those 15 carry rung
debt — in two entirely different shapes.**

> ### Where this stands on 2026-09-08, with the original table left intact below
>
> **The second shape is empty.** Every document that owed `SIGNATURE RESOLVED` or `TYPE
> RESOLVED` — a rung *below* the one it claimed — has been paid off, by five contracts and
> four types written since this page. The list is now **8 of 20 labelled documents, all of
> them owing `RUNTIME VALIDATED` and nothing else.**
>
> **The table below is not updated, deliberately.** It is what the audit found, and a page
> that silently rewrites its own findings cannot be checked against what it reported. Run
> `charter_grade_audit.py` for the live list; read the table for the one that started the work.

| document | stated rung | unmet rungs **below** it |
|---|---|---|
| `15-Input/…/the-input-name-registry-and-channel-aliases.md` | `DIFFERENTIAL TESTED` | `SIGNATURE RESOLVED`, `TYPE RESOLVED`, `RUNTIME VALIDATED` |
| `18-Audio/CONTRACT-field-music-selection.md` | `DIFFERENTIAL TESTED` | `RUNTIME VALIDATED` |
| `16-UI/…/CONTRACT-widget-object.md` | `CONTRACT READY` | `RUNTIME VALIDATED` |
| `19-Save-Load-Settings/…/CONTRACT-game-setting-config.md` | `CONTRACT READY` | `RUNTIME VALIDATED` |
| six documents at `BEHAVIORALLY UNDERSTOOD` | — | `SIGNATURE RESOLVED`, `TYPE RESOLVED` |

**The two shapes are different failures and need different answers.**

- **Four documents sit at or above `RUNTIME VALIDATED` and owe exactly that rung.** Nothing in the
  database has reached it, so everything above it has stepped over it. This is **one blocked
  experiment** — `EXP-001`, which needs the game at the title screen.
- **Six sit at `BEHAVIORALLY UNDERSTOOD` over a category with no `_types/` entry and no contract**,
  so they owe `SIGNATURE RESOLVED` and `TYPE RESOLVED` — both *below* them. That is **work nobody
  has done**, and it is the cheaper of the two.

> **This page does not demote anybody.** Rung debt is a fact about a label and the evidence beneath
> it. Whether the fix is to relabel four documents or to say in the charter that the ladder is not
> ordinal is a **decision**, and a decision is not a measurement. What can be said plainly: **the
> ladder as written cannot express "everything except runtime"**, which is precisely the state the
> four best documents in this database are in, and each of them says so in its own words. The
> `GameSetting.ini` contract's §13 reads, in full, *"None. Empty deliberately, and this is the gate
> the subsystem fails."*

## 3. The §27 completion gate, scored by hand on one subsystem

§27 is a list of questions a researcher must be able to answer **directly from the database**. No
mechanical proxy for *"can you answer what its invariants are"* is honest, so this was scored by
reading — on the subsystem [the roadmap](RECONSTRUCTION-ROADMAP.md) names as closest: **the
`GameSetting.ini` configuration object**, `19-Save-Load-Settings`.

The charter writes some clauses compound — *"how is it initialized, updated, destroyed"*, *"what
state does it read and write"*. Split, that is **21 questions**, which is why a casual count of the
sentence gives fewer.

| # | §27 question | answered? | where |
|---:|---|---|---|
| 1 | what is this system | ✅ | contract §1 |
| 2 | what does it do | ✅ | §1, §11 |
| 3 | what owns it | ✅ | frontmatter `category`, §6 chain |
| 4 | what does it own | ✅ | §3 the type, §5 state written |
| 5 | how is it initialized | ✅ | §4 preconditions, §7 `RAW → DEFAULTED` |
| 6 | how is it updated | ✅ | §7 transitions |
| 7 | **how is it destroyed** | ❌ | **§5: "the singleton is never freed; no destructor identified"** |
| 8 | what types does it use | ✅ | §3, `_types/GameSettingConfig`, 40 fields |
| 9 | what state does it read | ✅ | §5 |
| 10 | what state does it write | ✅ | §5 — including *1 writer, 61 readers* on the singleton |
| 11 | what calls it | ✅ | §4, §6 — CRT static init, before `main` |
| 12 | what does it call | ✅ | §6 |
| 13 | what state machines and events exist | ✅ | §7 — five named states |
| 14 | what scripts, resources and RNG affect it | ✅ | §8 *(none)*, §9 *(no RNG)* |
| 15 | what are its invariants | ✅ | §4 — four, each with its derivation |
| 16 | what side effects occur | ✅ | §5 allocations, §11 |
| 17 | what can fail | ✅ | §10 — five paths incl. the startup mismatch |
| 18 | how does it interact with other systems | ✅ | §6 — Config screen, renderer, frame limiter |
| 19 | how can we observe and test it | ✅ | §13, §16 parity plan |
| 20 | what is still unknown | ✅ | §14 — six items |
| 21 | what evidence supports what we believe | ✅ | §15 — nine claims, each tiered |

**20 of 21.** The miss is **destruction**, and the contract states it rather than omitting it.

**§26's readiness gate then fails on one question and one only:** *"Have major assumptions been
runtime validated?"* — **no.** §13 is empty by the author's decision, and the contract says so.

> ### The verdict, stated once
>
> **One subsystem in this database answers 20 of the charter's 21 completion questions and fails
> the readiness gate on a single item: runtime validation.** That is the closest anything has come
> to L2, and it is a far better position than any aggregate metric on this page suggests.
>
> **The category around it does not follow.** `19-Save-Load-Settings` also holds the save image
> layout, version stamps, language and locale, and where the files live — **none of which has a
> contract**. One contracted subsystem is not a contracted category, and the scoring above is of
> the subsystem, named.

## 4. What this audit does not claim

- **That the seven §3 dimensions are equally weighted.** They are seven headings in one paragraph
  of the charter. Reporting them as a row each is a presentation choice, not a scoring model, and
  **no composite is emitted** — a single number would hide that Behaviour cannot be asked at all.
- **That "cited" is "important".** The population is what documents cite. A function nobody has
  written about is invisible to every row here, and there are 34,266 authored functions against
  7,376 cited.
- **That prose names are correct.** The range counts *that a name was written*, by
  `check_consistency`'s patterns. It does not check the name against the binary — that is
  `verify_doc_addresses` and `audit_crossrefs`, and they check different things. It also
  does not check that the name is a **function** name: 6 of the entries are named only at an
  interior address, and those are excluded rather than credited.
- **That the six `BEHAVIORALLY UNDERSTOOD` documents are wrong.** Their debt is `SIGNATURE
  RESOLVED` and `TYPE RESOLVED` *as this tool evaluates those rungs* — a contract in the category
  and a `_types/` entry for it. A document may well have resolved the signatures of the functions
  it reads without either artifact existing. **The rung is unmet as a database record, which is
  what an ordered ladder asserts.**
- **That §27 was scored on more than one subsystem.** It was scored on exactly one, by hand, and
  the subsystem is named in every row.


## 5. The claim ledger — 634 claims, and what each one actually rests on

**Tool:** `claim_census.py` · counted 2026-09-12, **recounted and corrected the same day** (OPUS) ·
**write it to a scratch path, never over this file.**

[`COMPLETION-PLAN.md`](COMPLETION-PLAN.md) §1 is explicit: *"34 executed contracts are not 34
established systems. A contract's claims are established **claim by claim**, at the evidence class
each one earns."* **Nothing had counted the claims.** This does.

| evidence class | claims | share |
|---|---:|---:|
| **live** | **3** | **0.5 %** |
| executed — isolated original-code | 282 | 44.5 % |
| corpus / census over shipped data | 5 | 0.8 % |
| **static — the instructions, read** | **227** | **35.8 %** |
| none / explicitly unknown | 51 | 8.0 % |
| unclassified by this tool | 66 | 10.4 % |
| **total** | **634** | over 42 contracts |

**Three claims in the entire database rest on watching the game run.** That is the number the
per-contract view hides: "5 of 42 contracts are runtime-validated" (measured 2026-09-12; 47
contracts at 2026-09-14, still 5 validated) counts documents, and a document
counts once whether it carries one live claim or thirty static ones.

**A claim that is executed is not a claim that is live**, and the 282 are exactly what this session's
pilots keep demonstrating: an isolated original-code run settles what the instructions *do* with
planted memory, and says nothing about what reaches them in play.

### The first count of this ledger was wrong, and it was wrong about its population

The figures above replace **644 claims / 4 live / 251 executed / 248 static / 85 unclassified**,
published earlier the same day. Both defects were in *which rows were counted*, never in the
arithmetic — the fourth time this sweep that a miscount has had that shape:

| defect | effect |
|---|---|
| the row pattern was matched against the **whole of §15**, not against the claim table | **41 rows that are not claims** were counted — per-slot function maps, and the `§15a` falsification-pass records this sweep has been adding, which are themselves `\| claim \| …` tables |
| the row pattern hard-coded **four columns** | **9 real claims were invisible**, in the one contract (`CONTRACT-widget-object.md`) whose claim table has three |
| cells were split on every `\|` | a markdown-**escaped** pipe inside a claim — ``presence is `+0x3C \| +0x64` `` — shifted every column to its right |

625 correctly-counted rows + 9 invisible ones = **634**. Every body row of every claim table is now
accounted for, checked row-for-row against the tables themselves rather than inferred from a total.

### There are not three §15 schemas. There is one, and its third column carries two vocabularies

**This section previously reported three schemas and named eight contracts to normalise. That was an
artefact of the broken count** — the "schemas" were rows lifted out of other tables in §15. All 42
claim tables carry **one** header:

```
| claim | evidence | tier | confidence |
```

The defect is *inside* that schema, and it is worse than a formatting split:

| what the `tier` column actually holds | rows | share |
|---|---:|---:|
| a **class word** — `static`, `executed`, `isolated original code` | 330 | 52.1 % |
| a **number** — a source tier | 272 | 42.9 % |
| `—`, on rows whose confidence is `UNKNOWN` | 31 | 4.9 % |
| empty | 1 | 0.2 % |

**These are different axes.** [`EVIDENCE-STANDARD.md`](EVIDENCE-STANDARD.md)'s tiers 1–11 grade the
**kind of source** — disassembly, authored strings, RTTI, runtime capture. The evidence class grades
**how the claim was established** — read, executed in isolation, observed live. A row states one and
leaves the other unrecorded, and **8 contracts use both vocabularies inside a single table**.

> **The consequence is the reason this ledger had to exist at all.** Of the 272 rows that give a
> number, **266 are tier 1** — and **48 of those cite an executed pilot while 218 do not**. *A claim
> proved by running the original code and a claim read off the instructions are the same tier.* So
> the tier column cannot answer COMPLETION-PLAN §1 even in principle, and for those rows the class
> has to be inferred from prose — which is where **every one of the 66 unclassified claims lives**.

**What this needs is not normalisation but an added column.** Reshaping the eight would destroy the
richer statement 330 rows are making; dropping the class words would destroy it outright. The claim
tables need `tier` **and** `class`, which is a change to 42 peer-owned contracts and is registered as
an open question rather than made unilaterally — see `SC-1` in
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).

> **What this does not say.** It does not judge whether any claim *earns* the class it states —
> that is final-audit pass 8, and [the protocol](FINAL-AUDIT-PROTOCOL.md) is gated and must not be
> started. It counts what the tables say about themselves. The 66 unclassified rows are a limit of
> the instrument, not a finding about the database, and they are printed rather than distributed
> across the other classes.

## The 16 "rung debts" are 16 non-debts, in three different ways — 2026-09-13 (OPUS)

`charter_grade_audit.py` leaves a question open in its own docstring: *"whether the fix is to relabel
documents or to say in the charter that the ladder is not ordinal"*. **Today's ruling answers it**
([`KNOWLEDGE-SCHEMA` §5a](KNOWLEDGE-SCHEMA.md)) — the ladder is **not one ordinal axis** — and applying
that answer to this section's 16 rows leaves **none of them a debt**:

| rows | shape | why it is not debt |
|---:|---|---|
| **13** | `DIFFERENTIAL TESTED` or `CONTRACT READY` → **`RUNTIME VALIDATED`** unmet | **two axes.** `RUNTIME VALIDATED` is a fact about the *original*; `DIFFERENTIAL TESTED` is about a *reconstruction* and `CONTRACT READY` about a *document*. Neither implies it |
| **2** | `_index/CITATION-FORMS.md`, `_index/RUNTIME-RESEARCH.md` → `SIGNATURE RESOLVED` / `TYPE RESOLVED` unmet | **population.** Both declare `owner_layer: none — … not a game subsystem`. A rung about signatures and types is meaningless for an instrument rule or a methodology note |
| **1** | `CONTRACT-lua-chunk-loader.md` → `TYPE RESOLVED` unmet | **category proxy.** The rung is decided by *"does any type exist in this document's category"*, and `23-Third-Party-Libraries` deliberately declares none — third-party internals are EC-7 family C, *not this game's code* |

> **A section headed "rung debt" reporting sixteen items, none of which is debt**, is not a fault in the
> tool — it says plainly that it *"does not demote anybody"* and that the decision was open. It is what
> an open decision costs while it stays open: every reader re-derives it, or believes it.

**Two limits worth stating in the tool rather than rediscovering**: `TYPE RESOLVED` and
`SIGNATURE RESOLVED` are tested **per category**, not per document — *"does this category have any
types / any contract"* — so a document in a category that deliberately declares neither inherits an
unmet rung it cannot fix, and a document in a rich category inherits a met rung it did nothing to earn.

**Nothing is regenerated over this file**, per its own warning at the top; the run was to a scratch
path and these numbers were merged by hand.

### The Runtime floor is a floor by one record, not by many — 2026-09-13 (OPUS)

`charter_grade_audit.py` qualifies its Runtime figure honestly: only `VALIDATED` counts, *"so the
linked figure is a FLOOR"*, because *"some RUN and COMPLETE experiments carry real validation in their
status line"*. **Measured, that is one record.**

The corpus uses **ten status words over 82 records** — `COMPLETE` 48, `VALIDATED` 11, `RUN` 7,
`PREPARED` 6, `PARTIAL` 4, `REPRODUCED` 2, and one each of `CHECKPOINT`, `INCOMPLETE`, `OVERTURNED`,
`RESOLVED`. Scanning every non-`VALIDATED` status **line** for validation language:

| | records |
|---|---:|
| `COMPLETE` with validation language in the line | **0 of 48** |
| every other non-`VALIDATED` word with such a line | **6** |
| of those 6, actually asserting a validated game claim | **1** — `EXP-008`, *"400 cases over the game's own data, 0 mismatches"* |

The other five say something weaker and say it correctly: `EXP-032` and `EXP-035` are `PREPARED` with
*"controls pass; no runtime observation"* — **controls passing is not the claim validated**; `EXP-031`
is `PARTIAL` with *"original matched campaign incomplete"*; `EXP-036` and `EXP-044` are `REPRODUCED`
about a **checker defect**, not a game claim.

> **So `4 linked` is a floor whose ceiling is 5.** The undercount the tool warns about is real and it is
> one record wide. **The Runtime dimension is not a labelling artefact** — `COMPLETE`, the word on 59 %
> of the corpus, contributes nothing to it, and that is because `COMPLETE` says the experiment finished,
> not that its evidence stands.

**The fix the tool names is still right and now has its size.** A status vocabulary would move one
record today and prevent the ambiguity from growing; a looser match here would guess at five that
should not move. Routed as `OPUS-REQ-ASTRA-EXP-STATUS-VOCABULARY`, with `EXP-008`'s word as the one
concrete question.

### CORRECTED the same day — the refresh above was read from a two-day-old index (OPUS)

**I refreshed this table an hour earlier and said it "now reads what its own instrument says". It read
what a *stale copy* of its instrument said.** `charter_grade_audit.py` queries a cached
`knowledge.sqlite`; that cache had been built **2026-09-12 01:06**, and nothing in the tool's output
said so.

| dimension | published from the stale index | rebuilt |
|---|---|---|
| Identity (prose) | 5,403–5,931 / 9,104 | **5,506–6,087 / 10,885** |
| Identity (owner) | 2,364 / 9,104 | **3,145 / 10,885** |
| Interface | 32 / 305 | **46 / 348** |
| Data | 239 / 1,764 / 60 | **247 / 1,858 / 65** |
| Behaviour | 32 / 305 docs; **227** claims | **46 / 348; 706** claims |
| Relationships | 9,104 | **10,885** |
| **Runtime** | **1 / 305** | **2 / 348** |
| Validation | 81 / 305 | **95 / 348** |

**`Behaviour` was out by a factor of three** — 227 claims against 706 — because the index predated two
days of contract work. Every superseded figure above is struck through; none is deleted.

**The tool now prints its index's build time and tells the reader to rebuild before quoting anything.**
That is the fix, not vigilance: a cache with no age on it will be quoted stale by whoever reads it next,
and this time that was me, in the same entry where I criticised a stale table for disagreeing with its
instrument.

> **The `Interface` row still is not what its label says.** Its numerator counts documents whose
> frontmatter carries `contract:` and `scope:` — *"is this a contract"* — not documents that declare a
> signature, and its denominator is all 348 documents as of 2026-09-13 (365 at 2026-09-14), most
> of which are prose pages with no interface
> to declare. **46 / 348 is "how many documents are contracts", wearing an interface-coverage label.**
> Recorded here rather than changed, because choosing the right denominator is a charter question.
