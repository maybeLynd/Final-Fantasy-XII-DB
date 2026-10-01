# The contradiction ledger — what this database got wrong, and what found it

**Data:** [`CONTRADICTIONS.tsv`](CONTRADICTIONS.tsv) · **Tool:**
`Database/Tools/analysis-kit/gfz-scripts/contradiction_index.py`

```bash
python contradiction_index.py extract          # reserve @publication; ambiguous anchors abort
python contradiction_index.py status
python contradiction_index.py by-instrument    # the query this exists for
python knowledge_db.py query contradictions-by-instrument
```

## 1. Why this exists

Charter §7 requires the knowledge to answer **"all contradictions involving a subsystem."**
`knowledge_db.py queries` listed that as unsupported from the day the schema was built, with the
note *"there is no contradiction record type — this is the single biggest gap."*

It was never a hypothetical corpus. Across 219 documents, measured 2026-09-08 (365 at
2026-09-14): **117 contain a correction marker**, there
are **251 strikethrough spans**, and **33 dated correction headers** of the five kinds this ledger
tracks. **A project that overturns its own claims this often is generating evidence about its own
methods, and that evidence was greppable only.**

## 2. What is extracted mechanically, and what is not

A dated header — `CORRECTED 2026-09-02`, `RETRACTED …`, `SUPERSEDED …`, `WITHDRAWN …`,
`OVERTURNED …` — yields four fields with no judgement at all: **document, line, kind, date**, plus
any 8-hex addresses on the line. Those are filled by the tool and refilled on every re-run.

**`claim`, `correction` and `instrument` are not extractable from prose.** They are hand-written, the
tool never overwrites them, and until one is written the cell reads `UNSUMMARISED`.

> **A summary produced by a regex would be a fabrication with a citation attached.** The ledger
> reports how many cells are still empty on every run, the same way the type store reports its
> unresolved sizes.

**The audit log is excluded.** It is the narrative; the documents hold the claims, and a correction
that changed a document is the durable record. Corrections that live only in `AUDIT-LOG.md` are
therefore **not** in this ledger — a known and deliberate gap.

**33, not 165.** An early grep counted 165 by including `ANSWERED 20…`. **Answering a question is
not overturning a claim**, and the ledger tracks only the five kinds above.

## 3. The state of it

| | |
|---|---:|
| records | ~~**40**~~ **113** — *re-extracted 2026-09-13 (OPUS) after the extractor had been aborting since 2026-09-05; 54 corrections recovered, 0 identities lost* |
| with a written correction | **37** — ~~100 %~~ **32.7 %** of rows |
| with a named instrument | **37** — ~~100 %~~ **32.7 %** of rows |
| **UNSUMMARISED** | **76** — document, line, date and kind only; **no cause assigned** |
| `CORRECTED` / `WITHDRAWN` / `RETRACTED` / `SUPERSEDED` / `OVERTURNED` | ~~28 / 5 / 2 / 2~~ **97 / 8 / 4 / 3 / 1** |


### The cause table describes a third of the history — 2026-09-13 (OPUS)

**§4 below counts 37 records. The ledger now holds 113.** The other **76** were recovered on
2026-09-13 and carry document, line, date and kind but **no cause**, because a cause is read, not
extracted.

**That matters more here than anywhere else in this file**, because §4's ranking is what instruments
get built from: the absence-claim gate exists precisely because `no-reader-found` and
`E8-only-reachability` were **tied for most frequent in a 33-record sample**. With 113 records the
ranking may not survive, and **no instrument should be commissioned off the old one without
re-counting.**

**Nothing in §4 is withdrawn** — every row there was read and is correct about the record it names.
The claim that is now unsupported is the *implicit* one: that the table describes this database's
mistakes. It describes **32.7 %** of them. The 76 are routed for cause-assignment as
`OPUS-REQ-FABLE-LEDGER-CAUSES`; until they are read, quote §4 with its denominator.

## 4. What produced the wrong answers

**This is the column the ledger exists for.** Counting the instrument rather than the subject:

| instrument | times | categories |
|---|---:|---|
| `recount` | 3 | 99-Unresolved-Residual, 11-Party |
| `no-reader-found` | 3 | 25-EBP-Script-Container |
| `assumed-single-instance` | 3 | 11-Party, 02-Resource, 17-Presentation |
| **`E8-only-reachability`** | **3** | 99-Unresolved-Residual, 13-Rewards, `_index` |
| `wrong-name-table` | 2 | 01-Script-VM-Native-Bridge |
| `premise-wrong` | 2 | `_index`, 99-Unresolved-Residual |
| `misread-field` | 2 | 08-Combat-Formula, 99-Unresolved-Residual |
| `unread-branch-asserted` | 3 | 01-Script-VM-Native-Bridge — **added by hand**, §7 |
| `bias-recorded-not-applied` | 1 | 05-Spawn-Encounter-Lifecycle — **added by hand**, §7 |
| `stale-status-row` | 1 | 14-Story-Event-Quest-Hunt — **added by hand**, §6 |
| `duplicate-question-id` | 1 | 14-Story-Event-Quest-Hunt — **added by hand**, §6 |
| `mutable-evidence-citation` | 1 | 99-Unresolved-Residual — **added by hand**, §6 |
| **`check-cannot-fail`** | **2** | 22-Middleware-PhyreEngine, `_types` — **added by hand** 2026-09-19 (FABLE, ruling on OPUS's request), last section |
| *17 more, one each* | 17 | `address-adjacency`, `out-of-bounds-read`, `wrong-record-frame`, `conflated-id-spaces`, `edges-counted-as-functions`, `assumed-lea-is-a-table-base`, `scope-too-narrow`, `stopped-at-first-null`, `measured-from-a-listing`, `signedness`, `false-symmetry`, `over-generalised`, `single-caller-unread`, `endpoint-arithmetic`, `ledger-tag-as-mechanism` |

> ### The database's own history validates its own rules
>
> **`E8-only-reachability` is tied for the most frequent cause of a wrong answer** — three separate
> corrections, in three different categories, all from asking "who calls this" with one instrument:
> a function with *no caller* but a base-relocation-certified pointer; a gil counter that missed
> three callers reaching it through a five-byte thunk; a census where **a thunk is a sink in the call
> graph**.
>
> The mission prompt's four-instrument rule was written from experience. **It is now measured**, and
> the measurement says the rule is load-bearing rather than cautious.
>
> Two more of the top four are the same family of mistake in a different dress:
> `assumed-single-instance` (one map where a class argument selects five; one thread where nine
> procedures exist) and `no-reader-found` (three rows of "nothing reads this", all wrong).
> **"I could not find one" is not "there is not one" — and it accounts for 6 of 33 corrections.**

## 5. What this does not claim

- **That 33 is the number of times this database has been wrong.** It is the number of *dated
  correction headers in documents*. Corrections written without a date, corrections that live only
  in the audit log, and claims that were quietly rewritten are all invisible to the extractor.
- **That the instrument names are a taxonomy.** They are a small vocabulary chosen so the query
  aggregates. Two entries sharing a name are not proof they share a cause.
- **That a category with more corrections is less reliable.** `99-Unresolved-Residual` leads partly
  because it is where the hardest questions are sent.

## 6. Added by hand — 2026-09-08

The extractor reads **dated correction headers in documents**. These two were found by
enumerating a category's owned functions and checking each row of its address table against the
prose — a check no existing gate performs — and neither wrote a correction header of the shape
the extractor matches. **They are recorded here rather than left invisible**, and marked so the
33 mechanical records stay separable from the 2 manual ones.

### `stale-status-row` — a table said `partial` about work that was finished

**Claim:** [`persistent-flag-banks.md`](../14-Story-Event-Quest-Hunt/persistent-flag-banks.md)
§3 marked `00377970`, `00377440` and `00379160` as `⚠ partial`.

**Correction:** two of the three had been read in full — `00377970` by that same document's
falsification pass on 2026-09-02 (§10), `00377440` by its sibling
[`event-memory-at-actor-bind.md`](../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md)
§2. **A pass that answers a question and does not update the table that asked it leaves the
database understating itself**, and understatement is as wrong as overstatement here: it sends
the next block to re-read work already done.

> **`cov%` for the category read 100.0 both before and after.** The citation metric cannot see
> this class of error at all, in either direction.

### `duplicate-question-id` — one id, two different unknowns

**Claim:** the same document's §7 used **`AA-6`** for *the payload field at `+0x1534`* while
[`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) held `AA-6` for *`EventMemory_QueryDefinitionIdAbsent`
and `DAT_02ADD0A8`*. A staging row, `PROPOSED-repos46-15`, still proposed `AA-6` for the first.

**Correction:** the payload field is now **`AA-8`**, in the document, in the ledger table and in
the staging row. `check_questions` passed green throughout — it cross-checks ticked boxes
against table state and **does not check that an id means one thing**.

### `mutable-evidence-citation` — a document cited a file that changed under it

**Claim:** [`the-unresolved-158.md`](../99-Unresolved-Residual/the-unresolved-158.md) §3:
*“The complete list is `Database/Tools/work/verify/residual_addrs.txt` (158 entries, one per
line).”*

**Correction:** that file now holds **139**. `work/` is gitignored, so the list is mutable and
unversioned; it was regenerated twice after the document quoted it. The citation now names
`Tools/evidence/GM160_CURRENT160_ADDRS.txt` — 160 entries, **tracked**, so the next reader can
check it.

> **The document was not wrong when it was written. It had no way to stay right**, and no gate
> could have caught it: `check_links` resolves relative links between markdown files, and this
> was a path in prose to a file git had never seen. **The fix is not a gate, it is that
> evidence a document cites must be tracked.**

**What it cost:** nothing, as it happens — the three snapshots are strictly nested and the
undocumented remainder is identical across all of them, so no conclusion in the document
depended on which one it quoted. **That is luck, and it is recorded as luck.**

## 7. Added by hand into the TSV — 2026-09-10 (FABLE)

Four corrections with dated headers of exactly the shape the extractor matches — three in the
script-bridge contract, one in the group-completion contract — were **appended to the TSV by hand
as `CON-034`–`CON-037`**, not extracted, because running `contradiction_index.py extract` on
2026-09-10 did three things a mixed generated/manual file must not survive:

1. **It renumbered every id.** New headers found in earlier documents (and one false positive,
   below) shifted `CON-010` onward, so any query or note that names a `CON-` id is unstable across
   runs.
2. **It dropped hand-written cells whose header line had drifted.** `CON-021` (`COVERAGE.md`, line
   716, summarised on 2026-09-03) came back as `CON-022` at line 718 with `UNSUMMARISED` in all
   three cells; `RUNTIME-RESEARCH.md`'s two 2026-09-08 rows likewise. Preservation is evidently keyed
   on the line number, which is the one field guaranteed to move.
3. **It matched its own documentation.** The ledger's §2 sentence *"A dated header — `CORRECTED
   2026-09-02`, …"* became a record.

The regenerated file was discarded (`git checkout` of the untouched HEAD copy) and the four rows
appended in the extractor's column order with their cells filled, so a future extractor that keys
on `(document, header text)` can adopt them. **Routed to ASTRA as a tooling defect** on the board
(`FABLE-REQ-ASTRA-TOOLING`). At that checkpoint, re-running `extract` would lose cells again.
The repair and preservation controls are recorded below; do not reinterpret the old extraction
as a safe operation.

### `unread-branch-asserted` ×3 — the bridge contract stated a failure path it had not read

`EF-6` said, on 2026-09-08, that the int pop's body *"was read as far as the depth check and the
tag dispatch"* — and the same day the contract's §4, §10 and §12 asserted what the unread empty-stack
edge does, by symmetry with the float pop. The bytes disagree: `00267E18 jle` → `00267E3B xor
eax, eax / ret`, no `008620C0`, no decrement. **A branch that has not been read to its `ret` is
not a claim, however symmetric the sibling looks**; and the verb-dispatch page had read it
correctly, so the database held both readings for two days with no checker able to see a
contradiction that is not expressed through an address.

### `bias-recorded-not-applied` ×1 — the reset's own arithmetic, misread once

The group-completion contract's §7 said the reset *"does not clear `memberMask`"*, immediately
after listing eight qword stores per four entries against a `+0x10` bias it had itself recorded.
Two stores per entry, two `u64`s per entry: both masks. **Recording an offset bias and then reading
`rax-0x10` as if `rax` were the entry base** is the whole error; re-tabulating each store against
the bias (system page §4) is the whole correction.

## CORRECTED 2026-09-10 — input capture promoted to producer and scheduling proof

ASTRA-ORACLE-SCOPE records the original claims and counter-evidence in TEAM.json. EXP-008's
captured MUS0 contents were promoted to producer closure; EXP-009's untimestamped two-condition
traces were promoted to scheduling and integration sufficiency. Those conclusions are withdrawn
in the experiments, contract and affected status sources; DG-1 is reopened. The observed input/
return tuples remain intact. Instrument: raw within-thread trace recensus and observation-scope
review. TSV extraction was deferred under FABLE-REQ-ASTRA-TOOLING's stable-ID preservation
blocker; EXP-020 now repairs that tool and preserves this correction in the stable ledger.

## CORRECTED 2026-09-10 — unchecked pre-attach debugger-exit policy

hwbp and an AUDIT-LOG entry claimed that calling DebugSetProcessKillOnExit(False)
before attachment prevented debugger loss from killing the game. Both EXP-016 API
receipts instead show 0/error 6. [EXP-017](../_experiments/EXP-017-debugger-exit-policy.md)
tests the actual Windows policy: a disposable target dies after loss of an old-order
debugger; a second target remains detached and advances its heartbeat after loss of
a debugger using checked post-attach setup. Shared hwbp now uses that supported
order, aborts before event/context work on setup failure and reports detach failure.

Propagation: source protection text, historical AUDIT assertions, RT-1 register,
EXP-016 follow-up and ASTRA inbox. Captured tool snapshots remain original evidence.
No conclusion about armed-game liveness, the attach-to-policy interval or the cause
of a historical game death is inferred. ASTRA-CONTRA-KILLONEXIT routes this bounded
correction. TSV extraction was deferred under FABLE-REQ-ASTRA-TOOLING; EXP-020 now
repairs stable-ID/manual-cell preservation and includes this permanent record.

## CORRECTED 2026-09-10 — contradiction extraction could erase curated evidence

The old extractor assigned IDs from a newly sorted census and matched manual cells by
`(document, line)`. Earlier insertions changed IDs; line drift lost summaries/instruments.
Its self-documentation example also became a false correction record. The failed old
behavior and revised controls are retained in
[EXP-020](../_experiments/EXP-020-contradiction-preservation.md).

Extraction now matches `(document, source_header)`, where source_header stores the
normalized full source line separately from the curated claim. IDs are never renumbered;
new records take numbers above the existing maximum. Existing claim, correction,
instrument and addresses cells are preserved. A removed source retains its record and
ID with source_status `missing`; a legacy row without an adoptable marker is retained as
`legacy-unmatched`. Its line remains historical, not a verified current location.

Legacy rows adopt only a unique exact original snippet. Hand-written claims are not
anchors. Duplicate anchors, renamed markers overlapping unmatched history, malformed
rows or unsupported extra columns abort before replacement. Review and explicitly update
source_header when a marker is renamed or a legacy manual claim cannot be adopted; do not
fall back to line proximity. CON-034 through CON-037 required such reviewed initial anchors.
CON-033's prior marker is absent and its history remains retained rather than deleted.

The tool uses a same-directory temporary file and atomic replacement, checks that the
ledger's prior bytes still match, and removes the temporary file on failure. Continue to
use file claims and @publication; this check does not replace the repository's ownership
protocol. The correction-ledger page contributes actual Markdown correction headings,
not example sentences in its prose. Other documents retain their existing inline/table/
code correction-marker coverage. This remains marker extraction, not semantic discovery.

## CORRECTED 2026-09-12 — large-angle pass-through overgeneralised from two absorbed inputs

**Claim (2026-09-11, `2f419ae` / `e307fa1`):** inputs of magnitude `≥ 2^31 × 2π` pass through both
angle wraps (`002E5E10`, `0033CB70`) unchanged, because the invalid conversion's product is absorbed.
**Correction:** the invalid conversion yields the integer indefinite `−2^31`, the product is `−T`, and
the result is `f32(a + T)`; it equals the input only for `|a| ≥ 2^58`. The boundary is signed —
`−2^31` converts validly. **Instrument:** isolated original-code execution at the boundary
([EXP-074](../_experiments/EXP-074-angle-conversion-boundary.md), ASTRA, ten paired inputs, mutant
detected) and an independent binary32 emulation of the sequence (FABLE). **Why reachable:** the only
executed inputs (`±1e20`) were in the absorbed regime, and the static reading fused "product is `−T`"
with "`−T` is absorbed". **Kind:** `unread-boundary-generalised`. Affected: the facing page, the maths
page, ledger row `K-6`; the reconstruction's comment routed to OPUS.

## CORRECTED 2026-09-12 — an import slot misnamed as free, and an absence claimed past its instruments

**Claim (2026-09-12, FABLE, `BW-2` / `CD-2` / `J-C`):** `0036C660` releases a container through import
`008C2F70`, the game has no arena, the sub-4 GiB placement is OS policy, and nothing can write the
resolver base `01F83530`, so it is zero for the process's life. **Correction:** `008C2F70` is
`strncpy`; `0036C660` tags an arena block header; `0036BC60` is a fifteen-heap arena whose links are
32-bit references through the same base; the writer search is narrowed to five named instruments
and a computed-address store remains unexcluded. **Resolution (2026-09-26, FABLE):** `01F83530` is
zero at image load (past `.data`'s file-backed end `01F7E400`), and exactly one in-image store
route reaches it — texture-id writer `00210570` (`GiSetTexture` execute `00863040` → `00210570`)
bounds ids only from above, so `0xFFFB` stores a pointer into `01F83530` (replayed on unmodified
bytes; `members/image_address_base_writer_bounds.py` R6). Id producers keep ids `< 0x4000` at the
shipped width `0x200`: the route is **undriven, not absent** — *"no writer in the image"* false as
an image fact, *"zero for the process life"* supported not proven as a runtime claim (canonical:
`CONTRACT-authored-table-row-lookup.md` §7, `de52023ee`). **Instrument:** PE import-directory parse and the
bodies (ASTRA, re-derived by FABLE); image-base-register displacement sweep with a positive control.
**Why reachable:** the import was named from its position next to allocator slots rather than parsed,
and "no `lea`" was read as "no writer" although stores through computed addresses exist in the same
subsystem (`003303C5`). **Kind:** `import-named-by-neighbourhood`, `absence-past-instrument`. Affected:
the EBP container sheet, section 019, the memory page, ledger rows `BW-2`, `CD-2`, `J-C`; OPUS's
authored-table contract already corrected.

## CORRECTED 2026-09-19 — a check that cannot fail, twice published (FABLE, ruling for OPUS)

**The class.** `check-cannot-fail`: a sweep, filter or comparison whose predicate was never shown able to come out the
other way. Its silence is then not a finding, and nothing about the result says so. Two sub-cases: a positive control
that once existed and died (OPUS's original proposal), and a control that never existed.

**Claim 1 (2026-09-19, OPUS):** `classdesc +0xF4` is zero - from a sweep restricted to `mov`-family writes. Written into
section 12 of
[the member-registration page](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md),
into `_types/README.md` and into 201 field-row evidence strings. **Correction:** `0063E410` writes the field with `add` -
it is a running sum down the parent chain (that page's section 16, the same day).

**Claim 2 (2026-09-19, OPUS):** every "weak non-span" figure of a session, from the filter `^(unobservedSpan|unread)`.
**Correction:** the store also spells a span `unobservedTail`; 37 spans were being counted as named fields. True figures:
2,658 named fields, 120 weak, 611 span-like rows (`_types/README.md`, "a defect in my own metric").

**Instrument that found them:** by OPUS's own account in `_types/README.md`, "something other than the sweep that made
them" in every case; for claim 1 it was the body of `0063E410`, read.

**Why reachable, and the rule that follows.** OPUS's own split of that session: every sweep that carried a positive
control **chosen to fail if the predicate were wrong** came out sound; every sweep that did not is on this list. *A
control that can only pass is not a control.* **Kind:** `check-cannot-fail`.

**Counted and not counted.** Section 4 counts corrections actually made, so **these two enter the denominator**. Not
counted, because nothing was written before they were caught: the staleness sweep filtered on `assigned_to == "OPUS"`
(22 READY OPUS tasks are unassigned); capstone's operand size for a `lea` taken as a field width; a merge script that
counted five enrichments and wrote none; the two instances of OPUS's original proposal; and one of the ledger owner's
own the same day - a wait loop that asked the process list whether a script was still running, matched its own query,
and could never answer no. `CONTRADICTIONS.tsv` is left to the extractor: the member-registration page's section 16
carries a dated correction header of the shape it matches.
