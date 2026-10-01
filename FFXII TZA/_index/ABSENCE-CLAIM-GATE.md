# The absence-claim gate

**Tool:** `Database/Tools/analysis-kit/gfz-scripts/check_absence_claims.py` ·
**Output:** [`ABSENCE-CLAIM-AUDIT.tsv`](ABSENCE-CLAIM-AUDIT.tsv)

## 1. Why this gate, and not another hygiene check

The existing gates — `check_links`, `check_consistency`, `check_questions`,
`verify_doc_addresses` — check **document hygiene**. None of them checks a **claim**.

[The contradiction ledger](CONTRADICTION-LEDGER.md) measured which mistakes this database actually
makes. Two of the four most frequent are the same mistake:

```
no-reader-found          3 corrections    "nothing reads this"  - all three wrong
E8-only-reachability     3 corrections    "who calls this", asked with one instrument
```

**"I could not find one" is not "there is not one", and it accounts for 6 of 33 recorded
corrections.** This gate tests that class of claim, and only that class, because that is the one the
database has been provably worst at.

## 2. A phrase names the instrument that can refute it

**This was the tool's own first mistake, and its own output exposed it.**

The first version ran all four instruments against every absence phrasing and returned **55**
candidates. Reading them showed the majority were the documents agreeing with themselves: a line
saying *"`0081D790` has zero callers"* was flagged because a `lea` materialises the address — and the
very next clause of that line reads *"it is address-taken once, at `0081DF7C`"*.

> **A function with no caller can perfectly well be address-taken.** *"Zero callers"* is a claim
> about `E8`/`E9`; an operand hit does not contradict it. Binding each phrase to the instruments that
> can actually refute it took the candidate set from **55 to 28**.

| phrase | refutable only by |
|---|---|
| `no caller`, `zero caller`, `never called`, `uncalled` | `E8`, `E9` |
| `no reader`, `nothing reads`, `not referenced`, `no writer`, `no consumer`, `unreferenced`, `no xref` | `operand`, `qword` |

## 2a. A claim the gate could not bind — V-6, 2026-09-12

*Added 2026-09-12 (FABLE).* The save-image page's line *"its writer no caller (V-6)"* named only the
**buffer** (`022676C0`) on that line, so the gate bound the phrase to the buffer's operand hit — the
writer's own `lea`, self-consistent — and never tested the writer `002EF570` at all. A raw `E8`/`E9`
index run by hand found the writer's caller: the 5-byte thunk `00584490` (`jmp 002EF570`, an `E9`
this gate's instrument would have caught had the address been on the line) called at `0027F974`. Two
rules follow. **A "no caller" phrase must carry the function's address on the same line**, or the
gate cannot test it. **An `E9` hit on a 5-byte function is a thunk and must be followed one hop** —
the same shape hid the settings mask's bit setter behind `0017D9C0` the same day (AX-5), and hid the
event-slot feeder behind `001EC660`/`001EC6A0` the same way (EC-2, 2026-09-25: `0020AC30`/`0020AF10`
read "0 callers" while `call 001EC660` sites ran them four times over). Since then the hop is
**automated in the shared substrate**: `call_graph.call_maps` detects a listed body whose only
direct-immediate edge is `jmp <target>` and folds the thunk's callers and sites into the target's
maps, so every consumer (the census generators, `field_access_index`, the descriptor writers)
answers "who calls X" through the stub; `check_caller_claims` had carried its own
through-thunk accounting since d25c08dfb. The hop is one level, matching this rule. A caller
census built from the function list's disassembly misses both, and also misses the 134 listed
functions whose only call sites lie in code the list does not cover.

## 3. The instruments, and the one that is weak here

All four are built in a single pass and answered in O(1), each with a control that must be positive
**for that instrument** or the run refuses to report:

| instrument | control | built from |
|---|---|---|
| `E8` | `001DE4F0` | every `E8 rel32` in `.text` |
| `E9` | `001D1660` | every `E9 rel32` in `.text` |
| `operand` | `0023B6F0` | every RIP-relative memory operand, disassembled from each function entry |
| `qword` | `005C5230` | every 8-aligned qword in `.rdata`/`.data`/`_RDATA`/`.rodata` that looks like a VA |

> ### The `qword` instrument is a poor absence-refuter, and this run measured it
>
> A first version scanned **every** section including `.text`, at 4-byte stride, and collected
> **98,285** candidate addresses — any eight consecutive bytes that happen to form a plausible VA.
> Narrowed to 8-aligned data it still holds **92,162**. Against a corpus that large a coincidental
> match is likely for any given address, and it produced 19 of the original 55 hits.
>
> **It is excellent for confirming a pointer is in a vtable — the use it was introduced for — and
> weak as a general "is this referenced" test.** After the phrase mapping it accounts for 3 of 28.

## 4. First run

| | |
|---|---:|
| absence phrasings found | **372** |
| with no address on the line — unverifiable by this tool | **298** |
| address-anchored and tested | **74** |
| …of those, `call` claims | 35 |
| …of those, `reference` claims | 39 |
| the naming instrument is negative — claim stands | **46** |
| the naming instrument is positive — flagged | **28** |
| …of the 28, the **same line already states the refutation** | **7** |

**Reading the remaining 21 line by line: no unhedged false absence claim.** They are overwhelmingly
hedged in the corpus's own words —

- *"no consumer of `0x01E0C2A0` … **was read** in this pass"*
- *"no consumer walking `01F7F5E8` … **was found**"*
- *"Is the section really never parsed? **Not established, and deliberately not claimed.**"*
- and several that are narrative *about* a past correction, quoting the trap rather than falling into it

> **The gate's first run found the corpus already disciplined about this.** That is a result, not a
> null: it is measured over 74 claims with the denominator stated, where before there was no
> instrument at all. **Its value is ongoing** — it will catch the next unhedged one on the run after
> it is written.

**The classification above is line-level.** 28 lines were read; the surrounding sections were not.

## 5. A heuristic that was removed rather than shipped

A filter was written to skip lines that *negate* the phrase — *"**not** unreferenced"* — and it
**never fired once across the corpus**, while the same regex matched the same line correctly in
isolation. The cause was not found.

> **A filter that reports zero while possibly being broken is worse than no filter**, because every
> later run inherits a silent exemption. It was deleted. The false positives it was meant to catch
> are now handled by §2's phrase mapping, which is a rule rather than a guess.

## 6. What this gate does not do

- **It does not adjudicate.** An address is matched to a phrase by **proximity on the line**, which
  is a heuristic; the nearest address may not be the subject. Every hit is a candidate for a human.
- **It cannot see 298 of 372 phrasings** — those name no address on their line. That is 80 % of the
  population, and no instrument can test a claim whose subject is not stated.
- **It says nothing about whether a reference is meaningful.** A `lea` that materialises an address
  is a reference; whether anything reads through it is a different question.

## 7. The sibling gate, dispositioned — 2026-09-08

`check_self_contradiction.py` asks a narrower question than this page's gate: **does a document
assert that an address is never written and then, elsewhere in itself, write it?** Its first
full run reported **7 hits in 5 documents**. All seven were read.

| hits | verdict |
|---:|---|
| **1** | **warranted an edit** — and even that one was not a false claim |
| 2 | `_index/_inbox/` — peer handoff notes, which `COVERAGE.md` does not count as documents |
| 1 | `AUDIT-LOG.md` — an **append-only log** where the refuting line came *later* and supersedes |
| 3 | `OPEN-QUESTIONS.md` — rows that **quote** an absence claim in order to ask about it |

### The one that mattered, and it was a scope ambiguity rather than an error

[The game settings config](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
has a two-column table — `FrameLimit=30` against `FrameLimit=60` — whose 30 fps cells carried
an **unscoped absence phrase**. Elsewhere the same document records **`01F82E38`: 1 write,
13 reads**.

**The first repair was not a repair.** Rewriting the cells to *“not written on this path”*
swapped one absence phrasing for another and the gate flagged the same line again. The cells
now **state the fact positively** — *“BSS zero stands; `001EDDE8` is its one writer, on the
60 fps arm”* — which is both unambiguous and more informative than the absence it replaced.
**A scoped absence is still an absence; the way out was to stop making one.**

> **This page tripped its own gate while being written.** The first draft quoted the offending
> phrase verbatim two lines above the write it describes, and the next run flagged
> `ABSENCE-CLAIM-GATE.md` itself. **That is the instrument working, not failing** — a
> document quoting an absence claim next to its refutation is precisely the shape it looks
> for, and it cannot tell narration from assertion. The phrase is paraphrased above; the
> incident is recorded here because it is the cheapest possible demonstration of why the
> three `OPEN-QUESTIONS.md` hits are not exempted by a rule.

**Both statements are true.** Re-derived here from the binary: `01F82E38` has **exactly 1 write
and 13 reads**, and the write is `mov dword [01F82E38], 1` at **`001EDDE8`**, inside
`001EDDC0` — the *apply frame limit* function, i.e. **the 60 fps path**. The table's cell was
scoped to its own column and did not say so.

> **The gate's preamble had it exactly right**: *“the two statements may be differently scoped —
> but if they are, neither of them says so, and a reader has no way to tell which one to
> believe.”* The fix was three words in two cells, not a changed fact.

### The population was wrong, and that is now fixed and stated

`_inbox/` is excluded outright — **18 files** — and an append-only log now counts a hit only
when the **absence claim is the later line**. With the one real edit made as well: **7 → 3**,
in one document.

> **`OPEN-QUESTIONS.md` was deliberately NOT exempted**, though a blanket rule would have taken
> the count to 1. Its three hits are rows already naming the instrument they are scoped to —
> *“no writer … has been located across 24 write-form references. **Either they are set through
> a path the RIP-relative scan cannot see**”* — and they are recorded here rather than hidden.
> **A blanket exemption on the question ledger would silently swallow a real contradiction filed
> as a question**, and this database has already deleted one heuristic that reported zero while
> possibly being broken (§5). A hit that has to be read beats a rule that cannot be checked.

## A blind spot: the gate reads prose, and claims now live in the type store too

**Found 2026-09-10 by OPUS, auditing my own session's claims with this gate and finding none of
them — because it cannot see where I put them.**

`check_absence_claims.py` walks `*.md`. Since the type store started carrying evidence prose,
`_types/fields.tsv` has accumulated **14 absence claims** in its `meaning` and `evidence`
columns, and no gate reads one of them:

| type | offsets |
|---|---|
| `ActorManagerSlot` | `+0x48`, `+0x50`, `+0x60`, `+0x68`, `+0x70`, `+0x78`, `+0x80` |
| `SteeringRecord` | `+0x04`, `+0x24` |
| `VmValueStack` | `+0x44`, `+0x84` |
| `AudioParameterRamp` | `+0x18` |
| `BattleUnit` | `+0x6A0` |
| `PersistentFlagPayload` | `+0x1063` |

Seven of those are mine, written this session.

### Why the obvious fix was started and abandoned

Widening the file filter is two lines and was tried. It is not enough: `ADDR_RE` requires the
address to be **backquoted**, which is a markdown convention a TSV cell does not follow, so every
store claim lands in the *unverifiable* bucket instead of being tested. A TSV-specific address
pattern was then tried and did not work first time, and the debugging was consuming more effort
than the finding was worth. **The tool was reverted to its committed state rather than left
half-changed**, and its four controls still pass.

### What a fix has to get right

- A bare 8-hex run in **prose** is as likely to be a hash or a constant as an address, so the
  looser pattern must apply to the store only, never to `.md`.
- The store's claims are mostly *well* instrumented — several name two anchors and their positive
  controls inline — so the gate should expect to mark them clean, not flag them. **A fix that
  produced 14 new candidates would be suspect.**
- The point is regression, not discovery: these claims were sound when written, and the gate's
  value is re-testing them as the binary knowledge moves.

## The 63 have never been read — 2026-09-13 (OPUS)

**The gate works and its output has not been consumed.** All four instruments return a positive
control; **184 address-anchored absence claims are tested, 121 come back NEGATIVE** — the claim
survives its own refuting instrument — and **63 come back POSITIVE**, which the tool correctly labels
*"candidates for a human to read."* **Nobody has read them.**

That is the register built for exactly the failure class this database is worst at, holding sixty-three
unexamined candidates, in the same week its own contradiction ledger silently stopped updating. **Two
instruments whose output nobody consumes fail the same way: quietly.**

### Two matcher shapes were the document agreeing with the gate

Triaging the original 67 found four that were never absence claims:

| shape | example |
|---|---|
| **negated** — the line asserts the presence the gate looks for | *"`0x02EBF178` — **2 references, both writes** — **not** unreferenced"* (`authored-data-table-registry.md:301`) |
| **bounded** — the claim already names its own exception, so the instrument's positive **is** that exception | *"a debug-status flag with four consumers and **no writer but the reset**"* (`ff12config-and-debglobal.md:77`) |

Both are now skipped, **67 → 63**, with the negative count unchanged at 121 — nothing that was being
checked stopped being checked. **Neither skip is a relaxation:** an unqualified claim still fails, and a
bounded claim is not adjudicated here, only recognised as one this gate cannot settle mechanically,
because whether the exception is the *right* one needs a reader.

> The bounded example is **my own**, published this morning. The gate flagged a line I wrote, I read it,
> and the line was already correct — which is what a triage is for, and why 63 candidates are candidates
> rather than defects.

**The 63 are routed to be read, not bulk-dispositioned.** Each is a claim that *"nothing does X"* where
the instrument that could refute it says something does. Some will be correct claims with an unstated
exception, some will be the instrument seeing a neighbour, and some will be wrong — and the whole point
of this gate is that those three are only separable by reading.

## What the 583 unanchored phrasings actually are — 2026-09-13 (OPUS)

The gate skips a phrase whose own line carries no address: it has nothing to test. That is **583 of
767**, and the previous note implied a backlog four times the size of the tested set. **Measured, most
of it is not a backlog.** Decomposed with the gate's **own** matchers:

| bucket | rows | what it means |
|---|---:|---|
| **NEARBY** — an address within 3 lines | **235** (40 %) | anchorable by editing; the address is already on the page |
| **SECTION** — the enclosing `##` section names one | **211** (36 %) | anchorable after a read, to pick which address the claim is about |
| **PROSE** — no address in the whole section | **137** (24 %) | **correctly unanchored** — the phrase is about a concept, not an address |

**And the corpus is concentrated in narrative, not in claims.** The eight documents holding the most
are `AUDIT-LOG.md` (91), `_inbox/FABLE.md` (32), `COVERAGE.md` (19), the two 99-Unresolved censuses,
`OPEN-QUESTIONS.md`, `PARITY-STATUS.md` and `EVIDENCE-STANDARD.md` — files that *discuss* absence
findings rather than assert them about an address. A sentence like *"`INTEGRATION` is not covered,
because no caller is reconstructed"* has no address to cite and should not acquire one.

> **The 235 are the subset worth spending on**, because an anchor is available on the page and adding
> it moves the claim from unverifiable to tested. The 137 should be left alone, and saying so is part
> of the measurement: *a gate's "cannot test" bucket is not automatically a queue.*

*Method note: a first decomposition re-declared the phrase list and the address regex and produced
**621** against the gate's 583 — a breakdown of a corpus that was not quite the one it claimed to
explain. Re-run importing the gate's own `PHRASE_RE`, `ADDR_RE`, `NEGATED_RE` and `BOUNDED_RE`, it
reproduces 583 and 184 exactly. **Import, do not restate** — the same rule that fixed
`check_cited_site_widths`' stale census list earlier today.*

## The eight ways a register-tracking census manufactures an absence (OPUS)

*Recorded 2026-09-20 (OPUS), closing
`OPUS-AMEND-THE-CENSUS-TOOL-ALMOST-ASSERTED-A-FOREIGN-OBJECTS-FIELDS`, which was filed for the
fifth of these before the sixth, seventh and eighth were found in the same family.*

Most absence claims in this store come from an **access census**: track the register holding an
object, record every `[reg + disp]`, and report the offsets nothing touches. Section 1 says *"I
could not find one is not there is not one"*. This is the catalogue of **why** that census fails,
with what each one actually cost. Every entry was found by a result looking wrong to a reader, not
by a test.

| # | the rule that was missing | what it did |
|---|---|---|
| 1 | decode the **whole extent**, not to the first `ret` | all 22 arms of a table dispatch were invisible; two rows wrongly recorded as unobserved |
| 2 | `add base, index` **keeps** the base | lost every child selected by `imul idx, STRIDE` + `add`; half the offsets on `002778C0` |
| 3 | a load **from memory** is a different object | `ActiveLogEntry0198 +0x188` nearly became a field of the widget that owns it |
| 4 | a frame restore at an arm epilogue is not a reload | 10 offsets collapsed to 3 on a proc where a hand scan found 20 |
| 5 | a stack load is **ambiguous** - flag SUSPECT, do not guess | nearly attributed a world object's `+0x698` and `+0xE68` to a 64-byte block |
| 6 | a **call clobbers the volatile registers** | the receiver survived a call and the callee's *return value* inherited it - 9 foreign offsets |
| 7 | a **sub-register write clears the 64-bit name** | `xor eax, eax` never cleared `rax`; reported a zero-fill as 8 escaping pointers |
| 8 | `add index, base` makes the **destination** a base | the most expensive: `ActorManagerSlot` censused 26 accesses in 8 bodies instead of 155 in 39 |

**The direction matters more than the count.** Six of the eight *hide* accesses, producing a
too-strong negative - which this gate exists to catch, and which the store's "NOT CLAIMED"
discipline partly guards. Two of them - **6 and 7** - *invent* accesses, and that is worse: an
invented access becomes **a field row for a foreign object**, and nothing downstream would ever
question it. Blind spot 7 was found only because the invented offsets landed *inside declared
8-byte pointers*, which is a lucky tell and not a general one.

**A kill rule must model the ABI and the register file, not the operand list.** That is the
common cause of 6, 7 and 8: each was a write the rule could not see, because capstone's operand
list does not report what a `call` destroys, what a 32-bit write zero-extends, or which operand of
an `add` becomes the pointer.

**The tools now carry failing fixtures, not just passing ones.**
`census_selftest.py` disables each rule in turn at the host that motivated it and asserts the
answer **changes**, and in the stated direction - a rule that removes offsets is excluding foreign
fields, one that adds them is recovering real accesses. A known-right case proves a tool can
agree; it cannot prove a rule is doing anything, and all three of the late defects survived the
known-right check. Two rules remain **declared uncovered** rather than quietly assumed: `canon`,
whose motivating case is a store into another object that neither census records, and the
whole-extent traversal, which is structural and has no toggle.

**What this means for reading any absence row in this store.** A negative written before
2026-09-20 rests on an instrument with at least one of these defects. That does not make it wrong -
`ActorManagerSlot`'s five spans and `BattleUnit`'s two survived a six-fold widening of the census
that produced them - but the re-test is what makes it worth trusting, and the rows that got one
say so.

### Before claiming a system lacks something, read the system's own primary page (OPUS)

Recorded 2026-09-20 (OPUS) after breaking it three times in one session, on one system.

While declaring types for the navigation mesh I wrote, in type evidence and in a verdict, that the
portal costs were "untouched", that `A*` and the step-follower were "untouched", and that the
authored dataset had "no declared type at all - a name search finds only Phyre rendering and physics
meshes". The first two were false. `06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-
navigation-mesh.md` - the primary page of the very category the types were being filed into - already
carried the region Dijkstra, the portal cost function, the mover classes, the script verb that opens
and closes doors, and counts from the shipped data. **It also corrects the premise of the third
claim**: the search is Dijkstra, not `A*`, so the system registration's own wording was wrong.

What I had searched was `_types/*.tsv`, `_index/`, and prose matching the ADDRESSES I was holding.
That finds pages that happen to cite an address. It does not find the page that explains the system,
because a page can describe a mechanism thoroughly while naming few of its addresses in the form you
are grepping for.

**The same rule one level down: read the TYPE ROW before analysing the type (OPUS).**

Added 2026-09-20 (OPUS) after the third instance in one session.

Evidence cells on `_types/types.tsv` run to thousands of characters and are appended to over time,
so the answer to the question being asked is often already in the row - past the point where a
reader stops. Three times today:

1. `ArenaBlockHeader` and `ArenaHeapDescriptor` were declared as duplicates of
   `ImageAddressArenaBlockHeader` and `ImageAddressArenaRecord`; a grep of `_types` for the base
   address would have prevented 32 rows of work.
2. `_8FA0 +0xAC0`'s collapse was recorded as "blocked on Widget's extent"; the `Widget` row says
   outright that its size is an argument with 26 distinct values and there is no `sizeof`.
3. `ManagerSub0209BE80_8FA0` was "established" to be a Widget by matching thirteen offsets against
   Widget's map - and its own type row already said so, from the same day, **with more**: that
   `002465F0`, Widget's declared constructor, constructs it at base 0.

The third is the cleanest case because the re-derivation agreed with the record in every particular.
That is not reassuring. **Two passes reaching the same answer is one measurement and one waste** when
the first was already written down, and the effort spent re-deriving it was effort not spent on the
part the row leaves open.

**The rule.** Before analysing a declared type, read its `evidence` cell to the end - not the first
paragraph, which is usually the original declaration and the least current part of it. The
open questions are normally at the bottom, because that is where amendments land.

**The rule.** An absence claim about a SYSTEM - "X is untouched", "there is no type for Y", "nobody
has looked at Z" - requires reading the primary page of that system's category, not a grep. Category
folders are small; the cost is one read. A claim about a single ADDRESS may still rest on a grep.

The reason this matters beyond bookkeeping: the types I declared were genuinely missing and the work
stands, but every sentence I wrote about what the database did not contain had to be retracted, and a
reader who trusted those sentences would have concluded the navigation system was unexplored when it
was one of the better-explained systems in the store.

### Nine: a kill on a branch the base's own path never reaches (OPUS)

Found 2026-09-20 (OPUS), while censusing the arena heap descriptor table at `022D7FD0`.

These scans decode a function's whole extent **linearly**. That is deliberate and section 1 of this
catalogue defends it - it is how every arm of a table dispatch gets seen. But it also means the scan
applies the effect of every instruction it walks past, **including instructions the path that
established the base can never reach**.

`0036BC60` is the worked case:

```
0036BCBE  add rbx, rax        ; rbx becomes the heap descriptor (blind spot 8's rule)
0036BCC1  jmp 0x36bcc5        ; leave
0036BCC3  xor ebx, ebx        ; the ERROR arm - taken only when the heap id is out of range
0036BCC5  mov byte [rbx+2], 1 ; the join, reached from BOTH
```

Linearly, `xor ebx, ebx` sits between the base and its uses, so it killed `rbx`. The census reported
**zero** accesses for a body that plainly reads `+0x02`, `+0x90` and `+0x98` - and it was reporting
zero for a function I had just read myself, which is the only reason it was noticed.

**Direction: it HIDES accesses**, like six of the other eight. It cannot invent one.

**Measured cost, on the two censuses available.** The alternative reading - keep the base across the
boundary - is available as `rules=["postjmp"]` so the question can be answered rather than argued:

| census | default | keep-across-boundary | offsets gained |
|---|---|---|---|
| `ActorManagerSlot` (`02098E10`, stride `0x288`) | 155 acc / 34 offsets | 155 / 34 | **0** |
| arena heap descriptor (`022D7FD0`, stride `0xA8`) | 41 acc / 26 offsets | 57 / 26 | **0** |

So in both cases the choice changes **reference counts and nothing else** - no field appeared or
disappeared. That matters for what has already been published: the five `ActorManagerSlot` spans
re-tested with this instrument are **unaffected**, and that is now measured rather than assumed.
`0036BC60` is the case where it mattered, and it mattered totally: zero accesses instead of some.

**Why the instrument counts this instead of correcting it.** The sound incoming state at a block
boundary is the union over predecessors, which a linear scan cannot compute. Keeping the pre-`jmp`
state is one predecessor's state - often the right one, sometimes a base belonging to another path.
Section 1 holds that an invented access is the worse failure, because it becomes a field row on a
foreign object. So `static_array_census.py` now **records** every kill of a held base at such a
boundary in `LAST_POSTJMP_KILLS`; a non-zero count is a signal to read the body, not a correction.

**The rule for a reader.** A zero from a fixed-address census is only as good as its boundary count.
Check `LAST_POSTJMP_KILLS` before writing "nothing touches this span".

**Not yet done:** `receiver_census.py`, `pool_census.py`, `escape_sweep.py` and `trackscan.py` share
the same linear decode and have the same exposure. Only `static_array_census.py` carries the
detector so far.

### Ten: a bias-less base does not hide an access, it MISPLACES one (OPUS)

Found 2026-09-20 (OPUS), while re-testing two `BattleUnit` spans.

`receiver_census.py` holds its tracked bases in a **set**. `static_array_census.py` holds them in a
**map from register to bias**, and says why: *"`lea rbx, [ARRAY + 0x17]` then `[rbx+0x10]` is field
+0x27, not +0x10. Without the bias every non-zero-offset base silently reports the wrong field."*
The receiver census never had it.

**A third direction.** The other nine either hide an access or invent one. This one does both at
once, to two different offsets: the access is **removed** from the field it belongs to and
**added** to wherever `disp` alone lands - which is very often an unobserved span, because spans are
where nothing has been attributed yet.

**The worked case, proven in both directions.** `003105D0`
`BattleUnit_CancelAndResetCurrentAction` does `lea rsi, [rcx + 0x80]` and later
`mov dword ptr [rsi + 0x120], ebp` and `mov qword ptr [rsi + 0x124], rbp`. The bias-less census
reports `+0x120` and `+0x124`, **inside `unobservedSpan0120`**. With the bias applied they are
`+0x1A0` and `+0x1A4` - and those are declared fields `orderRangeBand0` and `orderRangeBand1`, a
`u32` pair, matching the `dword` and the `qword` writes exactly. The correction lands on existing
declarations; the error landed in an empty span.

**What it did NOT overturn.** I ran this re-test expecting to break the S-14 verdict's claim that
`BattleUnit`'s two spans "survive three widening passes". It does not. Of the twelve offsets the
re-test produced inside `unobservedSpan0120`:

- two came from `003105D0` and are the misplacement above - really `+0x1A0`/`+0x1A4`;
- eleven came from `003112F0` `BattleFormula_ApplyTargetResult` through `rbx`, and **`rbx` is not a
  `BattleUnit`**. `00311311` sets `rbx = rcx` (arg0), while the object this function treats as the
  unit is `rsi`, loaded at `00311339` from the **return value** of `0031B860`. The existing artifact
  censuses `rsi` and is right to; I seeded `rcx` on every function in its seed list without checking
  which register each one actually receives the unit in.

**`unobservedSpan0120` and `unobservedTail0EB4` are still clear, and the store was right.** Two
instruments disagreed and the older one won. That is worth recording as loudly as the cases where the
instrument won.

**The fix is not the obvious one, and was reverted.** Converting `hold` to a bias map fixes
`003105D0` (verified) but breaks the blind-spot-2 fixture: on `002778C0`, which walks
`BattleMenuChildWidget1620` children, accumulated `lea` constants produced a maximum offset of
`0x43D6` - larger than the child (`0x1620`) **and** the parent (`0x2DC0`), so neither object's field
map. A single bias is only meaningful while the chain is `base + constant`; the moment a body walks
between ELEMENTS the offset must be re-based on the element, which needs a stride this tool has no
notion of. Resetting the bias at the `add` of a computed base was tried and is not sufficient,
because the walk here is by `lea` constant, not by `add`.

So the instrument is unchanged and this is a **known limitation with a proven example**, not a fixed
defect. Until it is fixed:

**SCOPE, measured after the fact and much narrower than the entry above implies.** The
access artifacts in the store are **bias-aware**, and this was checked rather than assumed. In
`04-Actor-Entity/Battle-Unit/battle-unit-accesses.tsv`, the two writes through
`lea rsi, [rcx + 0x80]` are recorded with `disp` = `0x1A0` and `0x1A4` while their `instruction`
text still reads `[rsi + 0x120]` and `[rsi + 0x124]` - the column carries the CORRECTED offset and
the disassembly carries the raw one. `0x124 + 0x80 = 0x1A4`. A second body, `00304850`, records the
same pair the same way. Across every `*accesses*.tsv` in the store the `route` column holds non-zero
biases (`0x8`, `0x80`, `0x180`, `0x550`, `0x580`, `0xE240`, `0x4E494` and more), so the generator has
always tracked them.

**So the defect is confined to `receiver_census.py`**, which is an interactive instrument, and does
NOT reach the published field maps derived from the artifacts. I first read the artifact's opening
rows, saw the `lea` recorded and no `rsi` rows among them, and concluded it dropped the derived base;
the `rsi` rows are simply further down the file. **Checking the scope of a defect deserves the same
care as finding it** - the first reading would have condemned every census artifact in the store on
fourteen lines of evidence.

One genuine oddity remains and is NOT a claim of error: 108 of the artifact's 2,198 rows are `lea`
instructions, which compute an address without accessing memory. Whether a census should record
those as accesses is a judgement for whoever owns the generator.

**FIXED 2026-09-20, after the paragraph above was published saying it was not.** The entry
went out in `64bc2f487` recording a reverted attempt; the design that works arrived shortly after
and `receiver_census.py` now carries it. The paragraph above is kept because the failed attempt is
the reason the working one is shaped as it is.

`hold` maps a register to **(bias, pure)**, not to a bias alone. That second term is the whole
difference:

- `lea r, [base + const]` with no index register keeps the chain **pure** and accumulates the
  constant. This is the `003105D0` case, and it now reports `+0x1A0`/`+0x1A4` - the declared
  `orderRangeBand` pair - instead of `+0x120`/`+0x124` inside an empty span.
- `lea r, [base + idx*scale]`, and **`add` of a scaled index onto a base that is already held**,
  make the register an ELEMENT base: the bias restarts at zero and the chain is marked **impure**.
  Everything reached through an impure base keeps its RAW displacement and is reported SUSPECT.

The second rule is the one the first attempt missed. `002778C0` does `lea rdx, [rsi + 0x2d30]` and
then `add rdx, rax` with a scaled index; because `rdx` was *already* held, blind spot 2's rule left
it alone and it kept a `0x2D30` bias it had no right to. That produced a maximum offset of `0x43D6`
against a `0x1620` child and a `0x2DC0` parent. With the element rule the maximum is `0x2DB6` -
inside the parent, where it belongs.

**Measured effect.** The blind-spot-2 fixture moved from 51/23 to 53/25, both modes by the same two
accesses, and the relation it exists to prove is untouched. Re-running the `BattleUnit` span test
that found this, the two misplaced offsets from `003105D0` are **gone from the span by themselves** -
the instrument no longer needs a reader to know about the `lea`. The eleven remaining offsets are
still there, because they are a SEED error rather than a bias error: `003112F0`'s `arg0` is not a
`BattleUnit`. No instrument change can fix choosing the wrong receiver, which is why the second half
of the rule below still stands.

**WHICH TOOLS COULD HAVE BEEN AFFECTED - surveyed rather than asserted.** Bias
misplacement needs two things at once: a tool must PROPAGATE a base to another register, and it must
record the raw displacement. Fourteen scripts in `Tools/analysis-kit/gfz-scripts` both track a base
register and record `mem.disp`. They fall into three groups:

- **`receiver_census.py`** propagated through `mov`, `lea` and `add` and recorded the raw
  displacement. It is the one tool with both properties, and it is now fixed.
- **The artifact generators are bias-aware.** `battle-unit-accesses.tsv` records `disp = 0x1A4` for
  an instruction whose text reads `[rsi + 0x124]`, and biases appear in the `route` column across
  every `*accesses*.tsv` in the store.
- **`gen_ptr_census.py` cannot misplace because it does not propagate at all.** It seeds only on
  `mov reg, [rip -> slot]` and on the store that publishes a lazy singleton, and never follows
  `mov reg, reg` or `lea`. It also drops any offset outside the declared type
  (`if size is not None and not (0 <= d < size): continue`), which would discard a misplacement that
  escaped the type rather than recording it. The cost is the opposite error - it UNDER-reports
  through derived registers - and that is a limitation of that tool, not a correctness problem in
  what it emits.

**CORRECTION, same day: it was TWO tools, and the second is mine.** `trackscan.py`
propagates through `lea` into a bare set and records `op.mem.disp`, which is the same pair of
properties. It was written four hours before the survey and the survey's sweep keyed on the shape of
the older tools, so it matched nothing and was silently excluded. **A tool is not out of scope
because it is new.**

It surfaced the way these things do: a query for accesses at singleton `+0x9A60` - the parent's
`+0x8FA0` plus the sub-object's `+0xAC0` - returned zero, and the reason was that the tool would have
reported any such access at `+0xAC0`, in the sub-object's own coordinates, not the singleton's.
`trackscan.py` now carries the same `(bias, pure)` pair as `receiver_census.py`, and its self-test
still passes unchanged, which is what a fixture is for.

So the answer is one tool, for a structural reason rather than because the others were checked
individually and happened to be clean. **A defect's blast radius is a claim like any other**, and the
first version of this entry asserted a store-wide one on fourteen lines of a single file.

**The rule for a reader.** Before trusting a receiver-census offset, check how the base was formed.
If any `lea reg, [base + const]` sits between the seed and the access, the offset is short by the
sum of those constants. And before trusting a receiver census at all, check that the seed register
is the one that function actually receives the object in - the `route` column of an access artifact
records this per function, and ignoring it is how eleven foreign offsets entered a span above.

### A layout match refutes far more strongly than it identifies (OPUS)

Recorded 2026-09-20 (OPUS) from `check_base_type_match.py`, written the same day.

Scoring a declared type's field offsets against a candidate base type, and checking the CTYPE at
each hit, gives two results that look symmetrical and are not:

- **A float where the base declares a pointer is a contradiction no spelling explains.** `REFUTED`
  is a real negative, and the sweep produced **40** of them.
- **A pointer where the base declares a pointer is unremarkable.** `Widget`'s first `0x30` is six
  pointers, so any pointer-headed struct agrees with it by alignment alone. The sweep produced
  **28** `compatible`, which is far too many to be an identification - `ItemClassDescriptor` is in
  the list.

**The first version of this test scored offsets only**, and called
`ManagerSub0209BE80_00A0` a "partial" match at 4 of 6. It is not a widget: three of the four hits
are floats in pointer slots. That version's output was published in S-02's relationships cell and
had to be corrected the same day.

**The rule.** A layout comparison can rule a base OUT. It cannot rule one IN. An identification
needs a signal the layout cannot give - the base's own constructor (`002465F0` for `Widget`), a proc
or vtable value, or a call site that passes the object as `this`. Every widget identification in
this store that is worth anything rests on one of those; the layout score is how you decide which
candidates are worth that work.


## A falsified instrument does not falsify its results (OPUS, 2026-09-21)

ASTRA proved my AQ18 scanner misplaced addresses - it kept a stale `lea` value through
`xor al,al` because its kill map had no 8/16-bit aliases, and reported that stale address as
an exact target. Five of ten fixtures failed. The tempting response, and the one that looks
most rigorous, is to withdraw everything the instrument produced.

THAT WOULD HAVE BEEN WRONG HERE. The defect never fires in this executable. Running both
versions over the same image and comparing every resolved site: AGREE 121,843, MISPLACED 0,
V1-ONLY 0, V2-ONLY 6,643. The conclusion survived and got stronger, on a denominator 5.5%
larger than the one it was first claimed on.

SO THE RULE IS: a proven defect and a moved result are two separate findings, and the second
does not follow from the first. When an instrument is falsified, REPAIR IT AND RE-RUN, then
compare old against new site by site. Three outcomes, all real:
  * the result moves - retract and propagate;
  * the result survives on the same coverage - the claim stands, the wording may still not;
  * the result survives on MORE coverage - the claim is stronger than when it was filed.
Retracting without measuring throws away true findings and calls it caution.

AND THE CONVERSE, WHICH IS WHY THE MEASUREMENT NEEDS ITS OWN CONTROL: a comparison that
cannot detect a difference reports zero differences. Before trusting MISPLACED 0 over the
image, the same detector was pointed at ASTRA's fixtures, where three misplacements are
proven by emulation, and it found exactly those three and named them. A null from an
uncontrolled detector is not evidence.

SEPARATELY, THE WORDING STILL LOST SOMETHING. The scanner claimed "A HIT is decisive". No
hit in this image was misplaced, but the rule as stated was unsafe, and an unsafe rule that
happens not to have fired is still withdrawn - it would have been believed the next time.

## Blind spot 11: an absence of ADDRESS-TAKERS is not an absence of ACCESSES (OPUS, 2026-09-21)

Found by `ASTRA-CONTRA-OPUS-MGRMARK-HAS-CLEAR`, and this one is worth reading closely
because nothing about the method looked careless.

FRP-4 claimed `022C6D20[m]` has no clear anywhere in the image. **Five independent routes to
a clear were tested and each was given its own positive control**: a direct RIP-relative
store, a neighbouring store spilling in, a pointer held in initialised data, a block fill
spanning it, and a caller writing through the base the getter leaks in `rcx`. Every route
came back empty. Every control passed. The claim was still false, and there are in fact
**two** clears - `0032F14B` and `0032F4A2`.

THE FAILURE IS SHARED, WHICH IS WHY THE CONTROLS COULD NOT CATCH IT. All five routes assume
that reaching a global requires MATERIALISING ITS ADDRESS - in a `lea`, in a RIP-relative
operand, in a relocation, in a fill's destination. The clear never materialises it. It holds
the IMAGE BASE in a register (`lea r14,[rip-0x20edc2]` = `0x120000`) and reaches the table by
its IMAGE OFFSET as an instruction displacement: `mov byte [rdi + r14 + 0x21a6d20], bpl`. The
value `022C6D20` appears nowhere - not in the instruction, not in a relocation, not in any
`lea` in the image. Five searches for the address, and the address is never formed.

A positive control proves a route WORKS. It says nothing about routes not taken. Five
controls on five routes that share an assumption test that assumption zero times.

THE EXPOSURE IS MEASURED, NOT ASSUMED. This idiom is ordinary in this executable:
**921 `lea` sites in 641 distinct function bodies materialise the image base `0x120000`, and
1,901 memory accesses go through such a register with an image-offset displacement.** A
census restricted to address-takers is blind to all 1,901.

THE RULE. Before an absence claim over a GLOBAL, ask what the census resolves, not what it
searched for. An address-taker census supports "no code forms this address"; it does NOT
support "nothing accesses this object". To support the second, resolve effective addresses
with a register tracker that follows an image-base `lea` - which is what
`mgrmark_table_census.py` does and what the repaired AQ18 tracker does.

AND A STANDING DEBT THIS OPENS: any absence claim in this store argued from RIP-relative
address-takers, relocation searches or fill-span decoding is exposed to those 1,901 accesses
and has not been re-tested. That is not a claim that any particular one is wrong. It is a
named, measured debt, recorded here rather than discovered a second time.

## "No registered member" is not "no registered evidence" (OPUS, 2026-09-21)

`PApplication` carried 4,400 bytes in ONE span, and the row's reason was correct as far as it
went: *the Phyre reflection schema recovered no member for this class.* True - its registrar
registers no DATA MEMBER. It registers eleven SCRIPT-CALLABLE ACCESSORS, and nine of them are a
single instruction reading `this` at a fixed offset. The field-schema pass could not see them
because it was looking for members, and nothing else looked at all.

THE RULE: when a reflective class reports no members, read its REGISTRAR before concluding there
is no evidence. A registrar that binds names to adapters is a field map written in a different
alphabet - the adapter's one instruction gives the offset, the width AND the type, which a member
record gives no more precisely. `movsd` said double; `lea` rather than `mov` said the world object
is embedded and not a pointer; `btr eax, 0x1f` said the viewport count shares its dword with a
flag. None of those three would have come from a member list.

THE SCOPE, measured rather than promised: 315 classes have a descriptor vtable with a registrar
slot in `phyre-class-descriptor-vtable.tsv`, and the field schema covers 246. The gap is not all
accessor-bearing, and this note does not claim it is - it says the question has not been asked of
them, which is a different and cheaper thing to find out.

## Blind spot 12: a census keyed on where an access STARTS is blind to what it COVERS (OPUS, 2026-09-21)

Found twice in one day, in two different instruments, and the second time it had been hiding
behind four widening passes.

FIRST, IN A POOL CENSUS. WorldLootPickupNode's control asked whether the three declared fields
came back. `materialiseStamp` at +0x08 returned ZERO accesses although it is declared - which
would have voided the result - and the cause was not reach. The pool initialiser zeroes `state`
(+0x04) and `materialiseStamp` (+0x08) with ONE QWORD STORE at +0x04, and the census filed each
access under its STARTING offset. A declared field read as absent because a wider neighbour writes
it.

SECOND, IN THE STORE'S PRIMARY RECEIVER CENSUS, where it mattered more. `receiver_census.py`
files each access as `acc[d]` with d the displacement where the access STARTS, and
`battle-unit-accesses.tsv` carries a `disp` column and NO WIDTH column. Re-reading that artifact
width-aware: **5 of BattleUnit's 30 declared spans are covered by a wider access** - 16-byte
`movups` and 8-byte `movsd` block moves that begin at an aligned offset before the span and reach
into it. Those five rows said "no censused access" and it was false.

**S-14's types cell has read PARTIAL through FOUR widening passes on the strength of that
sentence.** Each pass added seed functions. Widening the SEEDS cannot fix a BUCKETING rule, and
three of those passes were spent proving the seeds were not the problem.

THE RULE. An absence over a byte range must be asked as *does any access COVER this range*, never
*is there an access AT this offset*. An instrument that records a width and then keys on the start
has the information and throws it away, which is the easiest version of this to miss - the width
is right there in the tuple.

AND THE COROLLARY, because the fix is not "call it a field". What covers these five spans is a
BLOCK COPY spanning several declared fields. That proves the bytes are carried along, not that
anything reads them for their own sake. The correct repair is to change the REASON under the row -
from "nothing touches these bytes" to "nothing touches them individually" - and leave the span
wording alone. A defect in an absence instrument does not convert its subject into a finding.

THE STANDING EXPOSURE, named rather than measured: any "no censused access" in this store that
came from an artifact with a displacement column and no width column is open to this. BattleUnit
is the measured case at 5 of 30; the others have not been re-read.

**MEASURED THE SAME DAY (OPUS), because "named rather than measured" is a debt and not a finding.**
`check_width_blind_spans.py` asks the question of every type in the store that has an access
artifact, using the artifacts that already exist - the width is recoverable from the `instruction`
column even though no artifact stores it.

**80 access artifacts, 46 mapped to a declared type, 185 unobserved spans on those types, and 20
COVERED by a wider access.** It is a FLOOR: 593 instructions carry no readable operand keyword and
are counted as one byte, which can only under-report.

| type | covered | of |
|---|---:|---:|
| `BattleUnit` | 5 | 30 |
| `SpawnRecord` | **5** | **6** |
| `CharacterRenderRecord` | 4 | 42 |
| `EvaluationContext` | **3** | **3** |
| `BattleStatsRecord` | 2 | 4 |
| `MovementContext` | 1 | 4 |

`SpawnRecord` at 5 of 6 and `EvaluationContext` at 3 of 3 are the ones to read twice. SpawnRecord
is S-16's type, a named frontier system, and its verdict cites *79 bytes* of span.

**AND THE TWENTY ARE NOT ONE THING.** Seventeen are what the BattleUnit case was - a 16-byte
`movups` or an 8-byte init store spanning several declared fields, which proves the bytes are
carried and nothing more. **Three are sharper, and they are not about the span at all - they are a
width disagreement about the DECLARED FIELD BESIDE IT:**

* `CharacterRenderRecord +0x10` is declared `encodedContextPtr`, `uint32`, 4 bytes - and
  `mov rcx, qword ptr [rcx + 0x10]` reads EIGHT. The span at +0x14 would be its upper half.
  *Re-adjudicated 2026-09-27 (OPUS): **widened to 8, `void*`.** The 2026-09-21 ruling kept `uint32`
  as "a lone outlier", weighing one qword read against the dword reads without looking at the
  writer. The only receiver-proven store is itself a qword (`0042055B`) of `0020E600`'s 64-bit
  return, and all 145 dword reads feed `0020E600` directly, so they re-resolve the low half. The
  `+0x14` / `+0x16` rows were misattributed and are removed: their seven sites are on other
  objects. Control: `_index/candidates/crr-context-ptr-width/crr_context_ptr.py`.*
* `BattleStatsRecord +0x20` is declared `packedByte20`, 1 byte - and `movsx eax, word ptr
  [rdi + 0x20]` reads TWO.
* `MovementContext +0x5C` is declared as two bytes, `moveStateByte5C` and `moveFlagBits5D` - and a
  4-byte float read covers +0x5C..+0x60.

Those three are candidate CONTRADICTIONS rather than span corrections, and one of them - the
MovementContext float - is on an access the census resolves through a biased base, so it must be
checked against blind spot 10 before it is believed. **None of the three is adjudicated here.**
Filed as `OPUS-ADJUDICATE-THREE-WIDTH-DISAGREEMENTS-FOUND-BY-BLINDSPOT-12`.


## Unearned names are not a population in this store, and that was measured (OPUS, 2026-09-21)

S-21's types paragraph flagged `BattleResultRecord.recordSlot144` as *"a row with a name and the
lowest rung, which is a claim someone made and nobody checked"*. It was right, and the row turned
out to have a second fault: its evidence cited the very memset that writes those bytes and then
concluded nothing writes them. Renamed, and the bulk clear recorded.

**The obvious next thought was that this is a population.** A name is a claim, the goal warns
against confusing named fields with understood fields, and a store this size will have more than
one. So it was measured instead of assumed.

**52 rows carry a name at DISCOVERED readiness with UNKNOWN confidence.** Reading them rather than
counting them, almost all are names EARNED BY THE OBSERVATION THAT PRODUCED THEM and asserting
nothing beyond it: `minusOneDword04` records the value seen, `zeroedDword0C` and `untouchedDword1C`
record what the initialiser did and did not do, `subAddr24B0` and `addrTaken26AE` record that an
address is taken, `clearedSpan000C` records a clear. Those are descriptions, not claims to check.

**The two that looked like genuine role assertions survive reading.** `Widget +0x058
elementDescriptor` and `Widget +0x060 elementBlock` are named for what the acquire and the release
do with them, which is the standard this store holds names to.

> **CORRECTED 2026-09-21 (OPUS), a few hours after publishing the paragraph above in
> `a789eb580`.** It said their low rung "reflects **no writer found**". **Both writers had been
> found on 2026-09-19 and were recorded in the same cells I was quoting** - `00243305` for `+0x58`,
> `002433AA` for `+0x60`, with the allocator, the freer, the nuller, the element width and the
> count encoding beside them. I read the HEAD of each evidence cell, which still opens *"NO WRITER
> IN THIS CENSUS"*, and the two columns, which still read `DISCOVERED`/`UNKNOWN`, and took those
> for the row's state. The rung has now been moved to `SEMANTICALLY IDENTIFIED`/`PROVEN`. The
> paragraph's actual finding - that the names are earned and a rename sweep would have been wrong -
> is unaffected; only my explanation of the rung was, and it was wrong in the direction of
> flattering the store's bookkeeping.

**So the finding is a negative and it is worth keeping:** the one unearned name was the one already
flagged, the store's naming discipline holds elsewhere, and a future sweep can skip re-deriving
this. **A low readiness rung is not evidence that a name is wrong** - it usually means a writer is
missing, not that a reader invented a role.


## An amendment supersedes the clause above it, and nothing in the cell says so (OPUS, 2026-09-21)

**I re-derived an answer the store already had, and the cost was an hour.** Looking for the writer
of `Widget +0x58`, I read the row's opening clause - *"3 qword LOADS and no store ... NO WRITER IN
THIS CENSUS"* - checked the two columns, `DISCOVERED` and `UNKNOWN`, and treated the question as
open. It was closed on 2026-09-19, in the same cell, after a ` || `. Before finding that I had
already built and rejected two instruments for it: an offset fingerprint that returned 159 bodies
(`+0x10/+0x18/+0x20/+0x28` are the commonest pointer offsets in any struct, and many hits stored
float constants at `+0x58`), and a proc-population sweep described below.

**This store appends; it does not revise.** Evidence cells grow by ` || ` because an amendment that
overwrites the clause it corrects destroys the record of what was believed and why - which is the
right choice, and the corrected `recordSlot144` and I6 entries depend on it. But the consequence is
that **the head of a cell is the OLDEST statement in it**, and the head is what a reader sees first.

**Measured, so the shape is known rather than guessed.** Of 4,523 field rows, **322 carry at least
one ` || ` amendment**; of those, **93 are still at `DISCOVERED` readiness or `UNKNOWN`
confidence**. Reading all 93 rather than counting them: **62 are `unobservedSpan`/`clearedSpan`
rows, where the low rung is CORRECT** and the amendment records why the span stays unobserved. Of
the 37 named rows, most amendments are **demotions or bookkeeping** - `WIDTH RESTS ON NO
INFORMATION`, `NAME IS IN THE PARENT'S COORDINATES`, `CONFIDENCE NORMALISED` from a `MEDIUM` that
was never on the vocabulary list - and one, `Widget +0x038`, says `STILL NO WRITER` and means it.
**The rung was genuinely behind the evidence on a handful**, of which the two Widget rows are the
clearest.

**So this is NOT a sweep and NOT a new gate.** A keyword check over amendment text would flag all
322, or all 93, and be wrong about most of them; the distinction between an amendment that promotes
and one that demotes is a reading, not a pattern. What is durable is the reading rule:

- **When a row looks unresolved, read the WHOLE cell before spending anything on it.** The columns
  and the first sentence are the two places the old state survives.
- **A rung that disagrees with its own evidence is a defect in the rung**, not a reason to re-derive
  the evidence.
- The reverse of `recordSlot144`. That row's name **outran** its evidence; these rows' evidence
  outran their **columns**. Both are the same failure to keep one row's parts in agreement, and
  nothing in the gate set asks whether they agree - `types_index` checks a type against itself,
  `check_storage_class` and the route checks compare a row to the binary, and
  `check_duplicate_declarations` compares rows to each other.

## A return-zero stub is not a family marker: 005C5230 (OPUS, 2026-09-21)

While looking for widget field writers I tried to build an exact population instead of a
fingerprint: the widget constructor `002465F0` substitutes **`005C5230` for a null handler
argument**, and `005C5230` is `xor eax, eax ; ret` - so "every function that falls through to the
default handler" looked like a definition of the widget handler family rather than a guess.

**It is not, and the number says so: 352 functions reach `005C5230` across 439 sites, totalling
256,050 bytes.** The tags on them are input boundaries, shader material, frame orchestration,
container allocators and resource loading. `005C5230` is not the widget default handler that other
code happens to share - **it is the image's shared "return 0", and the widget constructor merely
uses it as a null-safe default.** A two-instruction stub is the most foldable body a compiler has;
reaching it says nothing about what a function is.

**Recorded because the instrument was plausible and would have been believed.** A population built
this way would have carried 352 functions and a quarter-megabyte of unrelated code into a widget
claim, and every member would have had a real, checkable edge to the default handler to point at.
**A shared callee identifies a family only when the callee is itself distinctive**, and a stub that
returns a constant never is.


## A pre-biased base makes an interior offset look like offset zero (OPUS, 2026-09-21)

Reading `00309440`, the encoded-id class decoder, I recorded that **the class is at `+0x00` of a
`0x58`-stride row based at `01EEBCF8`**. The instructions say exactly that:
`imul rcx, rax, 0x58` / `lea rax, [01EEBCF8]` / `mov eax, [rcx + rax]`.

**It was one step from being filed as a contradiction against
`CONTRACT-encoded-id-space-and-class-registry.md`**, which puts the fifteen rows at `01EEBCC0` and
the class at `+0x38`. `01EEBCC0 + 0x38 = 01EEBCF8`. **The two readings are the same field.** The
compiler folded the member offset into the base pointer, so a reader who takes the `lea` as the
array base sees a row that starts `0x38` bytes late, and **every offset in it is short by `0x38`**.

**This is blind spot 10 from the other direction.** Blind spot 10 says a bias-less base MISPLACES an
access. This says a **pre-biased** base misplaces the whole *structure*, and it is worse, because
the resulting field map is internally consistent: a row read from `01EEBCF8` has a plausible class
at `+0x00`, a plausible count at `+0x04` and plausible handlers at `+0x10`/`+0x18`, and nothing
about it looks wrong until it is compared with a declaration derived from a different site.

**The rule.** A `lea` feeding an indexed load gives the address of *some member*, not necessarily of
the row. **Before declaring a structure from one access site, check whether another site reaches the
same bytes through a different base** — a stride that divides evenly and an offset that does not
start at zero are the signal. Here the stride `0x58` was identical in both readings while the base
differed by exactly one member offset, which is the shape to look for.

**What it cost and what it did not.** It cost nothing this time because the contract was read before
the finding was filed. **It would have cost a retraction and a false contradiction against a correct
document**, and the same reading also produced two corrections that ARE real - `+0x40` zero in every
authored row, and the `+0x48`/`+0x50` handlers not always being a pair. **A near-miss on one claim is
not a reason to distrust the other two**, and it is not a reason to hedge them either; each was
checked on its own.

## Blind spot 13: a getter's return register is an alias the cell-seeded census cannot see (SWE2-STRUCT, 2026-09-28)

Found by `ASTRA-REQ-STRUCT-NAV-TRAILER-GETTER-ALIAS` (evidence package
`nav-population-id-domains`). `NavTrailerRecord28`'s type evidence carried **"No code reads
this table"** on a whole-image census of every body that loads the block pointer `02AEDFB0`.
Two readers exist and were verified against the image:

```
003928E7  call 00383840      ; getter: mov rax, [02AEDFB0]; ret
003928F4  mov r15, rax       ; the base arrives as a CALL RETURN, not a load
00392909  cmp  [rax+0x24],edx   ; trailerRecordCount, min-bound at 0039290C
00392920  mov  ecx,[r15+0x28]; call 0020E600   ; decode the trailer table
```

The consumer `00392740` (and the `00391597` reader) **never loads the cell**. The only load
site in the image is the getter's own `mov rax, [02AEDFB0]` inside `00383840`. A census
seeded on loads of the cell attributes that one site to the getter body and stops - the
callee's `rax` is not propagated into callers, so no body in the consumer set is seeded, and
every downstream `[r15+d]` access is invisible. Trackscan's declared limits already named
the shape ("does not follow a pointer into a callee"), but the *return-register alias* is
the shape that actually fired here: the base does pass through a register the consumer holds,
just not one a load scan ever formed.

THE RULE. Before a "no code reads" verdict on a cell-reachable object, check whether the
cell has a ONE-INSTRUCTION GETTER. `mov rax, [cell]; ret` is the marker - its existence means
consumers can hold the base as an alias formed by `call; mov reg, rax`, and a load-seeded
census reports their absence whether or not they exist. The bounded result stays valid as
**scoped** history ("zero under the cell-seeded procedure"), never as the universal claim.

AND A STANDING DEBT THIS OPENS, of the same kind blind spot 11 opened: other "no consumer"
verdicts in this store argued from cell-seeded or receiver-bounded census are exposed to
getter-alias paths and have not been re-tested. The getter family is enumerable - any body
whose whole shape is `mov rax, [rip]; ret`. **The enumeration is now run** (SWE2-STRUCT,
same day): `.text` holds **69 such sites over 68 distinct cells, 11 of which anchor `PTR`
routes** - `01F7F598` (BootSingleton01F7F598), `01F7F5E8` (RenderCommandOwnerList),
`01F81248` (PendingCompletionQueue01F81248), `01FD4948` (WidgetSingleton01FD4948),
`020927C0` (ImageBackedStateBlock + AchievementState, one getter), `0209C498`,
`02AEDFB0` (NavRunStateBlock, the motivating case), `02B62D78`, `02EA0B70` (CPostEffect +
PpfxInitDescriptor, two getters), `02EA5368` (PApplication), `01F7FFE0` (InputManager).
Read back, the affected rows' negatives already name their instrument ("no access in the
flow census", "FIXPOINT RECEIVER CENSUS", "no access by the census union") - scoped, not
universal, so no cell was amended on this pass. What remains open is the *re-test* itself:
a transitive consumer census that propagates callee returns into callers, which is a
different instrument and deliberately not approximated here. Also not enumerated: getters
with any instruction between the load and `ret` - this family is bounded, not exhaustive.

**Second bound, measured 2026-09-29 (SWE2-STRUCT)** - the same scan widened to bodies of at
most three instructions between the `mov rax, [rip]` head and `ret`, then every candidate
body disassembled and classified by what `rax` holds at `ret`:

- **Object-returning, clean** (rax is still the cell object): 69 `mov;ret` + **11
  frame-bearing** `mov rax,[cell]; add rsp,imm[;pop]; ret` (0018B4F5, 001B5FC5, 001D6A05,
  001D8225, 001D8A75, 001DC582, 00210B45, 002B9C63, 003C4AED, 00550669, 0071435E - cells
  01F7F5E0/OrderedCommandList, 0209E5F8, 02CA8F38 and eight undeclared cells 01F81200,
  01F82CB8, 01F82CD0, 01F82CD8, 01F82D10, 01FD36A0, 02B45A50, 02EA1590) + **17
  conditional mutator hybrids** (`test rax,rax; j* ; mov/or/and [rax+N],cx` - return the
  object after mutating it, e.g. 0028F260/0028F280/0029E0C0 on 0209BE80 and 0209C498) +
  `0039C4A4` (object or fallback cell 02AEE800). **Total object-alias surface: 98 sites.**
- **Member-pointer getters** (~20 sites): `mov rax,[cell]; mov rax,[rax+N]; ret` and the
  guarded arm variants (`0028F570`->[+0x9FE8], `0028F6F0`->[+0x10F50], `0037EB70`->[+0xD8])
  or interior (`0028F590` returns obj+0x80). These alias the *member*, not the cell's type:
  a member-object census seeded at its own cell misses the consumer's accesses the same
  way, and a parent-cell census sees the member load inside the getter but not its callers.
- **Scalar-field accessors** (~100 sites): `mov eax/movsx/movzx [rax+N]` - return a field
  value, never the object; the member read sits in the getter body so a cell seed sees it.
  Not alias exposure.
- **Address-of-cell getters**: 0 (`lea rax,[rip];ret` does not occur).
- Still outside the envelope: bodies with >3 mid-instructions or prologue work before the
  load - bounded, not exhaustive.

**Re-test of the widened surface, same day** (`census_receiver_fixpoint.py SEED=call` on
all 42 typed sites, debt spans as targets): only two seeds produced tracked caller pairs
(`0028F570` 1 pair / 4 accesses, `0028F590` 2 pairs / 4 accesses) and **every hit lands on
already-named regions** - the +0x9FE8 member object and the +0x80 interior - none in a debt
span. The other 40 seeds report zero pairs, which is an instrument bound, not a "no
callers" claim: `0037EB70` has four direct E8 callers whose member pointer leaves through
`rdx` (arg2 at 003BE9BB) - outside the tracked rcx set - so caller-side aliases through
non-rcx argument registers remain the named, unenumerated residue of this blind spot.

**The residue measured and the instrument widened, 2026-09-30.** A third enumeration,
arm-following to a `ret` within 8 instructions (not bounded to 3 linear mids, so it
also catches prologue-bearing and branch-arm getters) counts **202 object-returning
and 18 member-pointer sites** among 420 `mov rax,[rip]` sites that reach a return.
Across their **1,740 direct call sites** the caller's first copy of `rax` lands in
`rcx` at 734 sites, a non-argument register at 103, and a non-`rcx` argument register
at **22 sites** (`rdx` 20, `r9` 2 - measured first-copy destination; `r10` counts with
the non-argument group, and the one apparent `r8` transfer at `00225553` is a false
positive: `mov rdx, rbx` there moves the enclosing `this`, not the getter's return,
while the return itself goes `rcx` -> tail-call `002211B0`). ~1.3% of the getter-call
surface, small but real - and it is
no longer a miss: `census_receiver_fixpoint.py` now takes **`ARGREGS=1`**, which
enqueues a callee for any argument register holding the tracked base and seeds the
callee's scan on THAT register (pair identity is `(function, base, arg)`). Verified
on `0037EB70`: the run goes from 0 pairs to 4, reaching `0029CD00` - the callee that
the `mov rdx, rax` at `003BE9BB` hands the member to. Default off: the fixpoint's
published numbers were all measured without it and re-running with it changes pair
counts where these sites exist. Yield over all 24 member-pointer getters with
`SEED=call ARGREGS=1` (extent 0x800): `00282DF0` reaches 9 pairs/25 displacements,
`0028F800` 25 pairs/24 displacements, `0035D460` 19 pairs, `0035D480` 14 pairs -
member-consumer sets that the rcx-only fixpoint could not see; several others
(`0035D520`, `00683AF0`, `007AAA2C`, `007BB69C` a.o.) still report zero pairs, the
same instrument bound as before.

The 22 non-`rcx` argument transfers, enumerated (getter | caller site | arg | callee):
`00282DF0`->0055BAE0 r9->0055BB1C, 00583DC4 rdx->00583E35; `0028F6F0`->003F788C
rdx->00271650; `0029CB70`->002A745F, 002A759B both rdx->0020E620; `0035D3F0`->
00299F58 rdx->00299FC0, 003FAE83/003FC47C rdx->0028F810; `0035D460`->0028BA38,
0028BA98 rdx->0028B700, 00299665/00299838 rdx->002998D0, 002BDA50 rdx->002D8CB0,
002C896C rdx->003F12E0, 003FAE19 rdx->002D8C80; `0035D470`->002C7C94 rdx->003F12E0;
`0035D480`->0028D36B, 0028D6D5 rdx->003F1430; `0035E810`->0050CE44, 0050CEC4
rdx->0017D280; `00377B90`->0034DC80 rdx->003E9020; `0037EB70`->003BE9AE
rdx->0029CD00.

2026-09-28 (SWE2-STRUCT), cohort re-test under the widened option: every fixpoint
seed in the SWE2-DATA census-rerun registry (33 types, 53 seed runs,
`Database/Tools/work/SWE2-STRUCT/census-argregs/`) was replayed with `ARGREGS=1`
and diffed per span against the recorded run. **No unread-named or measured-ZERO
row gained an access** - the rcx-only limit hid no debt-span consumers in this
cohort. The yield it did produce is real and belongs to the named residue:
call-seeded runs that found ZERO pairs reach closures now (`0081ED30` 0->78
pairs on all four Lua types; `002EF640`, the save-buffer getter, 9->33
functions; `001BDAB0` 23->30; `00189120` 69->81), so member-result and
factory-result consumers are where the residue lives, exactly as the
enumeration predicted. Two caveats carried rather than smoothed: five
hub-closure seeds (`0209BE80`/`022C6F28`) TRUNCATED at the default 400 pair cap
under the widened mode where they converged rcx-only - the (function,base,arg)
space is larger (a function entered through two argument registers is scanned
once per register); re-run at CAP=8000 both closures converge (`0209BE80`: 1463
pairs over 149 functions; `022C6F28`: 717 pairs over 369, forty-two more than
rcx-only found) and the re-test is then complete - still no debt row gained an
access. The second caveat stands: several converged runs show small LOSSES
versus the recorded run (`LuaProto` +0x00/+0x08, `MapScreenPage` fn counts),
which reproduce under `ARGREGS=0` - they are the intervening
`reg_tracking.written` kill-set fix (6b6a423db) shrinking stale attributions,
not the option removing coverage.
