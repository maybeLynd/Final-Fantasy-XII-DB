---
system: Citation forms — the four ways this database writes an address, and which ones count
category: _index
status: DOCUMENTED
owner_layer: none — this is an instrument rule, not a subsystem
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-08
falsification_passes: 0
audit:
  passes: 0
  crossref_clean: false
  reopened_count: 0
---

# Citation forms — the four ways this database writes an address, and which ones count

## 1. Why this page exists

On 2026-09-08 a block asked the schema for *the highest-connectivity callee with a real body that no
document cites*, and was handed **`002F9860`** — 160 callers, 180 bytes, apparently undocumented.

**It had already been read line by line.**
[The VBF / st2e tables document](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)
§9 quotes ten of its instructions, names both group tables, derives the reciprocal divide, and builds
a whole open question (`AY-10`) on the result.

> **The document had spelled it `FUN_002F9860`, and the citation extractor required the address to
> fill a code span by itself.** The address was inside a token, so the index could not see it —
> and `FUN_<addr>` is the GFZ ledger's spelling for every **unnamed** function. **The blind spot was
> aligned with the search space**: the form that goes missing is the form used for exactly the
> functions a *"what is undocumented?"* query hunts for.

**`check_already_answered.py` was the one instrument that was right**, because it does a literal
substring search and never tries to parse. It is the tool the non-negotiables require before filing
a question, and this is the second block in a week where it stopped a rediscovery.

## 2. The four forms

| form | example | counted? |
|---|---|---|
| **backtick** | `002F9860` or `0x002F9860`, alone in a code span | **yes** |
| **symbol** | `FUN_002f9860`, `DAT_0208f570`, `thunk_FUN_00682d20` | **yes — added 2026-09-08** |
| **code** | a bare address inside a fenced block: a disassembly listing | **yes — one gate 2026-09-03, the rest 2026-09-08** |
| **prose** | a bare address in an ordinary sentence | **no — see §4** |

Interior addresses resolve to the function body that contains them, so quoting one instruction
counts as citing its function.

## 3. What the correction moved

| instrument | before | after | delta |
|---|---:|---:|---:|
| `knowledge_db.py` — distinct function entries cited | 7,420 | **7,780** | **+360** |
| `ADDRESS-INDEX.md` — addresses cited by a document | 7,421 | **7,783** | **+362** |
| `program_coverage.py` — authored functions cited | 5,969 | **6,186** | **+217** |
| `script-verbs-undocumented` | 1,158 / 1,224 | **1,153 / 1,224** | −5 |
| `check_located_not_read` | 55 (14 vendor) | 55 (14 vendor) | **0** |
| `check_named_not_cited` | 414 mentions / 96 docs | 414 / 96 | **0** |
| GM160 residual worklist, uncited members (`DT-1`) | 106 / 160 | 106 / 160 | **0** |

> **Two of those zeros are the useful results.** The GM160 residual worklist did **not** shrink:
> none of its 160 members was hidden by the blind spot, so `DT-1` is a real frontier and not a
> reporting artefact. And `check_located_not_read` did not move either, so no function in that cut
> was cited by symbol alone.

**`program_coverage.py`'s movement is decomposed on purpose.** The file on disk read 5,922; a fresh
run of the *unfixed* tool gives 5,969; the fixed tool gives 6,186. **+47 was staleness and +217 was
the defect** — reporting the 264 as one number would have hidden which was which.

## 4. Why a bare address in a sentence is not counted

**It cannot be told apart from a constant of the same width.** Measured over the whole corpus, the
prose form contributes **12 function entries that no other form reaches**, and **two of the twelve
are values, not references**:

| the text | what it really is | what it was read as |
|---|---|---|
| `+0x118 = 0x003C0000` | a field default written into an actor record | a citation of `FUN_003bfff0` |
| `0x00555556` | the compiler's **divide-by-3** reciprocal | a citation of `00555400` |

**Ten of the twelve are genuine** — an entry address written bare in a sentence. So the form is
**kept in the table and excluded from the cited set**. `knowledge_db.py` exposes a view:

```sql
CREATE VIEW cited AS SELECT * FROM citations WHERE form <> 'prose';
```

Ask `cited` *"does any document discuss this function?"*; ask `citations` to see every form,
including the unreliable one, with `form` naming which.

> **Precision was measured, not assumed.** *"Bare prose is noisy"* would have been a guess; **2 of
> 12** is a number, and it is what justifies an exclusion that costs 9 functions while the symbol
> form gains 226.

## 5. Four instruments now agree

| tool | reads | rule |
|---|---|---|
| `knowledge_db.py` | every `.md` with frontmatter | four forms recorded; the `cited` view excludes `prose` |
| `gen_address_index.py` | `.md` under `NN-*`, `.tsv` separately | backtick + symbol + fenced; `.tsv` stays bare |
| `program_coverage.py` | system documents | `cited_addresses()`, the same three forms |
| `check_located_not_read.py` | system documents | backtick + fenced since 2026-09-03, symbol since 2026-09-08 |

**A sha256 opens with eight hex digits and every document states the exe hash**, so all four strip
long hex runs before extracting anything. Without that guard the leading eight digits of a hash read
as a citation in every file in the database.

> **This is the third time this project has found an instrument that could not see evidence in the
> form the evidence is usually written in** — after the `.tsv`-versus-markdown extractor split in
> `gen_address_index.py`, and the fenced-listing miss in `check_located_not_read.py`, whose own
> docstring says it: *"the instrument could not see the evidence in the form the evidence is usually
> written in."* **The pattern is the finding.** When a query returns a suspiciously clean answer
> about what the database does *not* have, suspect the extractor before believing the gap.

## 6. What is not claimed

- [ ] **That the three counted forms are exhaustive.** A document can cite a function by a semantic
      name with no address at all — that is a different gate, `check_named_not_cited`, and it
      reports **414 such mentions across 96 documents**.
- [ ] **That citation means understanding.** It does not, and
      [`COVERAGE-DIMENSIONS.md`](COVERAGE-DIMENSIONS.md) §3 says so: it is the weakest signal in the
      report. This block made the weakest signal *correct*, not stronger.
- [ ] **That the ten genuine prose citations should stay uncounted forever.** They are visible in
      `citations` with `form = 'prose'`; a rule that can separate an address from a constant would
      recover them.
- [ ] **Any runtime observation.** None exists; this is a measurement over the corpus and the
      shipped bytes.

## 7. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the old extractor could not see `FUN_002F9860` | its pattern anchors a backtick on each side of the eight digits, so the span must hold the address and nothing else | 1 | PROVEN |
| the document had read `002F9860` in full | `vbf-archive-and-st2e-tables.md` §9 quotes ten instructions and both group tables | 1 | PROVEN |
| 360 more function entries are cited | `knowledge_db.py` rebuilt: 7,420 with `form='backtick'`, 7,780 through the `cited` view | 1 | PROVEN |
| the prose form is 2/12 wrong on its margin | the twelve prose-only entries listed and read individually | 1 | PROVEN |
| `DT-1` does not move | the 160-address GM160 worklist scored under both rules: 106 uncited either way | 1 | PROVEN |
| the three counted forms are exhaustive | **not established** | — | UNKNOWN |
