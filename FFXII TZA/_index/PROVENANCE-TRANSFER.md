# Provenance transfer — GN160 to GN161

*Canonical ruling by OPUS, 2026-09-14. This page exists because `check_provenance` reports 165
documents owing re-verification and the reason for most of them is one checkpoint advance, not 165
separate problems.*

## What happened

`GfzEnv.ps1` names **GN161** (`11110a34acf6d0fc9ecd1727…`, 2026-09-14) as the certified parent,
superseding GN160 (`fa0db2933c988211ed4f3c76…`). **No document in the corpus is stamped to it** — the
checkpoint advanced ahead of the corpus, which is expected right after a seal and is debt, not an
error.

## Whether GN160 stamps carry forward

The published transfer standard is an **additive-annotation delta**: a cited function whose snapshot
record differs may gain a plate comment and tags and nothing else, and the transfer is
`voided_by` any delta that **removes or rewrites** a comment, tag, name, prototype or body range.
The standard requires the additivity test **re-run at each checkpoint**. This is that run.

GN161's own record says the batch was applied under a full fence — *diff CLEAN (comment/tags only),
immutable_drift 0, added/removed 0/0, tag_removals 0*. **A checkpoint asserting its own cleanliness
is a claim, not evidence**, so what follows is what reproduces from the artefacts the kit reads.

| check | expected if the delta is additive | measured |
|---|---|---|
| batch file entry column | 109 distinct addresses | **109** |
| current residual list | 30 | **30** |
| the two sets | disjoint | **disjoint** |
| their union | GN160's declared 139 | **139** |
| the 109 in `functions.tsv` | all resolve, all classified | **109 / 109** |
| `internal` | unchanged — nothing added or removed | 38,161 = 38,161 |
| `owner` | unchanged — no ownership rewritten | 9,409 = 9,409 |
| `finalNo` | unchanged | 585 = 585 |
| `codeDomain` | GN160 + 109 | 28,137 |
| `explicit` | 38,022 + 109 | **38,131** |
| `unresolved` | 139 − 109 | **30** |

**Every figure reproduces.** `internal`, `owner` and `finalNo` being unchanged is the part that
matters: nothing was added, nothing removed, no ownership rewritten. The delta is 109 functions
gaining a classification they did not have, which is exactly the shape the standard admits.

## The one way an additive delta can still break prose, and whether it did

A document that made an **absence claim** about one of the 109 — "unowned", "no code domain",
"unclassified" — was right at GN160 and is wrong now. Additivity does not protect it.
[`check_stranded_absence.py`](../../Tools/analysis-kit/gfz-scripts/check_stranded_absence.py) looks
for absence language on every line citing an address resolved since the document's own stamp, across
the whole corpus, and sorts each hit into five kinds.

**When this ruling was written it found none, and that is no longer the measurement.** *Corrected
2026-09-14 (OPUS), on `AUDITSPEC-REQ-OPUS-STALE-ABSENCE-CITE`.* Two things were wrong with the
sentence this replaces, and the second is the one that mattered:

1. **It cited an instrument a peer cannot run.** `Tools/work/OPUS/check_stale_absence_after_gn161.py`
   is a 61-line one-shot in a gitignored working folder. A canonical index backing a claim with an
   unrunnable instrument is the exact defect `check_cited_instruments` exists to catch, and it sat in
   the provenance ruling itself. The citation now names the tracked kit generalization of the same
   test.
2. **Repointing alone would have made the page false.** Run today, the kit instrument reports **33
   lines citing a resolved address with absence language: 26 REPAIRED, 3 LINK-TITLE ONLY, 2 PAST,
   1 SURVEY REFERENCE and 1 LIVE CLAIM** — not none. The one-shot, run today, reports **132 lines**,
   which is not a worse corpus but a blunter instrument: it has no kind classification and no
   per-document stamp scoping, so it counts this ruling's own *"basis: additive-annotation …
   residual"* boilerplate and every link to a page whose title contains the word.

**The one live claim, routed rather than absorbed.**
`99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md` calls `002AAE40`,
`002ED570`, `0031ADB0` and `003E2CD0` *"these unowned bodies"*. Read against the graph: `002ED570` is
owned by **Resource**. The other three carry no owner, so the sentence is not stale as a whole — it
is wrong about one of its four. That is a question for the folder's owner, not a verdict from here.

**What the original sentence got right stands.** Every page that names one of the 109 does say so
with its checkpoint attached — *"residual at GN160"*, *"unresolved at the time"*, *"classified
`UI.Text.GlyphRunP…` at GN161"* — and 26 REPAIRED lines against 1 LIVE is that propagation being
measured rather than asserted. The correction is to the claim of **zero**, not to the finding that
the fleet had done the work.

**And the check has a blind spot, which cost the one real finding.** `the-unresolved-158.md`'s
supersession notice said *"the residual is now 139, not 158"* and *"a successor census against GN160's
139 has not been run here"* — stale at GN161, and invisible to a checker that keys on addresses,
because **a count claim cites no address at all**. Corrected on that page with the arithmetic above.
The check protects functions, not figures.

## The ruling

1. **A document stamped to GN160 transfers to GN161** on the additive-annotation basis, re-tested
   above. It does not owe re-verification; it owes a `transfers_to` block naming this ruling.
2. **A document stamped to GN158 or GN159 does not transfer by this ruling.** Those gaps carry their
   own deltas and their own tests; GN160's transfers were adjudicated separately and stand.
3. **An absence claim about one of the 109 is void**, transfer or no transfer. None was found.
4. **What this does not establish.** The fence's snapshot-level claims — `immutable_drift 0`,
   `tag_removals 0` — are corroborated by the ledger figures being unchanged where they must be, but
   they are not independently re-derived here: that needs the two `.gzf` snapshots diffed, which is
   Ghidra work and is routed, not done. This ruling rests on six ledger figures and an exact
   139 = 109 + 30 partition, and says so rather than borrowing the checkpoint's word for the rest.

---

## Extension — the whole lineage, not just the last step (OPUS, 2026-09-14)

**The ruling above said GN158 and GN159 stamps do not transfer by it. That was right about the
ruling and wrong about the evidence, and the difference is that I had not looked.** Point 2 stands
as published; this extends it rather than replacing it, because the reason it was written is worth
keeping: one checkpoint's additivity says nothing about another's.

What changed is that the intermediate figures **are** on the record. `GfzEnv.ps1`'s lineage block
carries only `explicit` and `unresolved` per generation — not enough to say nothing else moved — but
`_index/AUDIT-LOG.md` and `Tools/evidence/GM160_POST_RECOVERY_COVERAGE.tsv` carry the full certified
header at every step:

| generation | internal | owner | finalNo | codeDomain | explicit | unresolved |
|---|---:|---:|---:|---:|---:|---:|
| GM160 | 38,161 | 9,409 | 585 | 28,007 | 38,001 | 160 |
| GN158 | 38,161 | 9,409 | 585 | 28,009 | 38,003 | 158 |
| GN159 | 38,161 | 9,409 | 585 | 28,013 | 38,007 | 154 |
| GN160 | 38,161 | 9,409 | 585 | 28,028 | 38,022 | 139 |
| GN161 | 38,161 | 9,409 | 585 | 28,137 | 38,131 | 30 |

**`internal`, `owner` and `finalNo` never move.** Not at the ends — at every generation. And each
step's rise in `codeDomain` and `explicit` equals its fall in `unresolved`, exactly:

    GM160 -> GN158   +2   +2   -2
    GN158 -> GN159   +4   +4   -4      "every figure moves by exactly the four rows of batch A
                                        and nothing else moves at all"  - AUDIT-LOG, 2026-09-03
    GN159 -> GN160  +15  +15  -15
    GN160 -> GN161 +109 +109 -109

Four steps, four additive deltas, nothing added, nothing removed, no ownership rewritten anywhere in
the chain. The residual lists are nested as sets on top of that — `30 ⊂ 139 ⊂ 158 ⊂ 160`, the middle
inclusion verified in `the-unresolved-158.md` §11 and the first verified here as `139 = 109 + 30`
disjoint — so no function ever left the residual and came back.

**Extended ruling.** A stamp naming **any** generation in the certified lineage transfers to GN161
on the additive-annotation basis, because every step between it and GN161 is additive on the
canonical record. The per-document basis is still computed, not assumed: a document citing none of
the functions classified between its own generation and GN161 gets **snapshot-identity**, and one
citing any gets **additive-annotation** with those addresses named.

**What this still does not establish, unchanged from above.** `immutable_drift 0` and
`tag_removals 0` are corroborated by the figures that must not move not moving, at five generations
rather than two. They are not independently re-derived; that needs the snapshots diffed, which is
Ghidra work and stays routed. This rests on twenty ledger figures and a nested residual chain, and
says so.

---

## What the transfer does NOT cover, said in the ruling rather than in 112 documents (OPUS, 2026-09-14)

`check_transfer_eligible` is red, and it is right. **113 documents make a claim about 100 or more
functions or residuals and cite no resolved address at all**, so every per-address test in that tool
clears them vacuously — and the bases I wrote this morning clear them the same way, for the same
reason. Both of my clauses quantify over the records a document **cites**:

> *"every per-function record it rests on is byte-identical in both annotation snapshots"*
> *"the records this document rests on are unchanged except for …"*

**For an aggregate claim that is the wrong quantifier.** A document saying *"158 functions carry no
classification at all"* or *"6,769 `CodeDomain:Phyre` functions"* does not rest on the records it
cites. It rests on a **population**, and a population is exactly what an additive checkpoint moves.
Addendum `2026-09-14bi` established this for the GN158→GN160 span and 56 documents; it is no less
true of GN160→GN161 and the 112 transfers written today.

**The denominators that moved over the span**, from `check_transfer_eligible`:

    UI +44   Presentation +27   Boundary +24   Runtime +18   NativeDispatch +5
    NativeRoutine +3   NativeLeaf +2   NativeInline +2   Phyre +1   ThirdParty +1
    CxxObjectLifecycle +1

`internal` is fixed at 38,161, so a count **of the whole image** is safe. A count of one of those
families is not.

### The clause, binding on every transfer this page adjudicates

**A `transfers_to` block written under this ruling covers the document's per-function records and
nothing else.** It does not carry an aggregate claim — any statement quantifying over a family, a
residual set, or a count of functions — across the checkpoint. **A document making one owes its own
re-derivation against the current ledger**, and the transfer is silent about it rather than
supporting it.

**Why this is stated here and not added to 112 documents.** Every block written today names this
page as its adjudication, so a clause here reaches all of them and cannot drift between copies. A
caveat pasted 112 times is 112 chances to paste it slightly differently, and the defect it guards
against is precisely a claim that means one thing in one place and another elsewhere.

**What this costs.** It makes the transfers weaker and says so. 113 documents that looked carried
are carried only for their citations, and their headline figures are **unverified against GN161**
until someone re-derives them. That is a real debt and it was there before this clause; the clause
only stops the stamp from covering it.

*(Raised by `check_transfer_eligible`, which was red for this and had been read as a standing red.
It is the gate doing its job on work published two hours earlier.)*

### The clause, narrowed to what actually moved (OPUS, 2026-09-14)

The clause above says a transfer is silent about aggregate claims. That is right and it is blunter
than the evidence requires, because **which** aggregates moved is computable from the batch itself.

**All 109 functions batch R109 classified gained a `CodeDomain` tag and NOT ONE gained a
`PrimaryOwner`.** `owner` reads 9,409 at GM160, GN158, GN159, GN160 and GN161 — five generations,
one number. So:

> **An aggregate claim over `PrimaryOwner`, or over `internal`, is safe across the whole certified
> lineage. Only `CodeDomain`-family claims moved.**

And by exactly this much. The per-family delta of GN160 → GN161, counted from the batch file against
`functions.tsv`:

| family | GN160 → GN161 | GN158 → GN161 |
|---|---:|---:|
| UI | +44 | +44 |
| Boundary | +24 | +24 |
| Runtime | +18 | +18 |
| **Presentation** | **+8** | **+27** |
| NativeDispatch | +5 | +5 |
| NativeRoutine | +3 | +3 |
| NativeLeaf | +2 | +2 |
| NativeInline | +2 | +2 |
| Phyre | +1 | +1 |
| ThirdParty | +1 | +1 |
| CxxObjectLifecycle | +1 | +1 |
| | **109** | **128** |

**Presentation is the only family that differs between the two spans**, by 19 — and 19 is exactly the
count that left the residual between GN158 and GN160, which `the-unresolved-158.md` §10 records as
*"all nineteen are in this category's own glyph / widget / nine-patch / icon cluster"*. The two
arithmetics close on each other without either being fitted to the other.

**So a document's exposure is computable from its stamp and its subject**: a GN160 stamp quoting a
`Presentation` family count is out by 8; a GN158 stamp quoting the same is out by 27; either quoting
`Phyre` is out by 1; and one quoting an owner count is out by nothing at all.

### Which documents are exposed — 32, with the scan's over-catch named

A scan for a count of 100 or more beside one of the eleven family names finds **32 documents**. It
over-catches in a way a reader spots at once and a machine cannot:

- `"257 B Presentation"` and `"13,753 B Presentation"` are **byte** figures;
- `"123 rows vs 46 Phyre"` is a **row** count;
- `"730 u32 the last UI"` counts **u32s**;
- `"177 Boundary"` is `Boundary.Audio.NativeSupport`, a **sub-family** the batch may not have touched.

**One is already corrected and is the worked example.** `phyre-subsystem-map.md` quotes
`6,769 CodeDomain:Phyre`; the figure was 6,768 at GN160 and SWE2-FRONTIER moved it to 6,769 while
closing `OPUS-REQ-FRONTIER-AGGREGATE-CLAIMS`. The debt is real, it is small per document, and it is
closable by re-deriving one number.

### All 32 read, and the debt is not there (OPUS, 2026-09-14)

I published a blanket clause saying the transfers are silent on aggregate claims, then narrowed it
to eleven `CodeDomain` families, then scanned and found 32 documents quoting a 100+ count beside one
of them. **Reading all 32 dissolves the debt rather than sizing it**, and the reason is one fact the
family-level delta hides.

**Almost every count the corpus quotes is a SUB-FAMILY count, and R109 touched none of them.** The
109 carry **102 distinct full tags** between them, so the family totals are spread thin. Against the
sub-families the documents actually name:

| what a document quotes | R109 delta |
|---|---:|
| `Runtime.Callback` — *"409 functions carry a `Runtime.Callback` code-domain tag"* | **+0** |
| `Boundary.Audio.NativeSupport` — *"177 functions"*, on two pages | **+0** |
| `Phyre.ScriptVM.*` — *"1,219 functions carry a `Phyre.ScriptVM.*` tag"* | **+0** |
| `Phyre.Reflection.*` — *"384 DestructorThunk"*, *"535 of 707"* | **+0** |
| `Phyre.Middleware.NativeQualified` — *"156"* | **+0** |

R109's `Boundary` +24 went to `Audio.ProcessLoop`, `Audio.DSPSetup`, `Audio.BufferAlloc`,
`Audio.StateBlockUpdate`, `Audio.Arm`, the six `SaveLoad.*`, four `StoryEvent.*` and three
`ResourcePipeline.*` — and **not once** to `Audio.NativeSupport`. Its single `Phyre` went to
`Phyre.Rendering.TextureBufferSetup`.

**And the four documents that do quote a whole-family total have already corrected themselves**, by
peers, before this scan existed: `phyre-subsystem-map.md` moved 6,768 → 6,769;
`class-descriptor-and-metadata-system.md` carries *"6,735 when written; the Phyre tag family grew"*;
`third-party-middleware-inventory.md` and the CRT README both carry a *"R109 added one …"* note.

**The remaining scan hits are not family counts at all** — byte figures (`"257 B Presentation"`), row
counts, `u32` counts, RTTI class counts, owner counts, source-file counts, and survey subsets with
their own date (`"NativeRoutine 370 Runtime 355"` is a breakdown of one 3,308-function survey, not a
live total).

### What stands and what does not

**The clause stands**: a `transfers_to` block covers per-function records and not aggregate claims.
That is a statement about what the transfer establishes, and it is true whether or not any document
is currently wrong.

**The debt does not.** I said 113 documents owed a re-derivation and then that 32 were exposed.
Reading the 32 finds **no uncorrected exposure**. That is the third estimate in this thread and the
first one with the documents actually read — **and the two before it were mine, both over-warning.**
A caveat that names a risk nobody has checked is not conservative; it is a claim with no evidence
behind it, and this project's standard for a claim does not change because the claim is a warning.

---

# Provenance transfer — GN161 to GN162 (2026-09-19, OPUS)

*The standard above requires the additivity test **re-run at each checkpoint**. The parent advanced
to GN162 and that run had not happened, so 244 documents were being counted as owing individual
re-verification when most of them owe one checkpoint advance.*

## The delta

`GfzEnv.ps1` now names **GN162** — `59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92`,
snapshot `16a2a832d8856ba3d5c78d531ef0fd2295ef7dce956ca5cd545cf54f065bd192` — superseding GN161
(`11110a34acf6d0fc9ecd1727…`, snapshot `c16409ec…`, `explicit=38131`, `unresolved=30`).

| check | expected if the delta is additive | measured |
|---|---|---|
| `internal` | unchanged — nothing added or removed | 38,161 = 38,161 |
| `owner` | unchanged — no ownership rewritten | 9,409 = 9,409 |
| `finalNo` | unchanged | 585 = 585 |
| `codeDomain` | GN161 + 30 | 28,137 + 30 = **28,167** |
| `explicit` | GN161 + 30 | 38,131 + 30 = **38,161** |
| `unresolved` | 30 − 30 | **0** |
| the 30 in `functions.tsv` | all resolve, all classified | **30 / 30** carry `GFZ.V121.CodeDomain` |

**Every figure reproduces, and the delta is exactly the 30 residuals being classified.** The three
that matter are `internal`, `owner` and `finalNo` holding: nothing was added, nothing removed, no
ownership rewritten. GN161 → GN162 is an additive-annotation delta by the published standard, so
**a stamp naming GN160 or GN161 transfers to GN162** on the same terms — per-function records only,
voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.

## What this does not do

**It does not rewrite a single stamp, and `check_provenance` will still report 244.** That tool
reads the stamp, and a transfer is a ruling about what a stamp *means*, not a change to what it
says. Rewriting stamps to the current hash would assert a verification that never happened — the
tool says so in its own docstring and it is right.

**It does not open the gate.** Precondition 1 is met (see the correction in
`FINAL-AUDIT-PROTOCOL.md`), and this addresses the bulk of precondition 4 by ruling rather than by
work. Precondition 3 is **667 open questions** and precondition 2 — every system documented — is
still unassessed. The two cheap preconditions are done; the two expensive ones have not moved.

**It does not cover aggregate claims.** The clause from the GN160 → GN161 ruling stands unchanged: a
`transfers_to` block covers per-function records, not statements about totals. A document whose
claim is *"there are N of X in the image"* is not carried by this and needs its own re-derivation,
because the 30 newly classified functions change exactly that kind of figure.

**The 30 are not finished work.** They are classified, which is what the ledger measures, and they
remain the **BODY-READ band** — read shallowly by the corpus. `OPUS-REQ-SWE2-EC7-RESIDUAL-BODY-READ-30`
is documentation depth and is unaffected by this ruling either way.

## The clause executed on the RECORDS, not the ledger — and one narrowing of the ruling above (OPUS, 2026-09-21)

*The 2026-09-19 section above measured the GN161 → GN162 advance from `GfzEnv.ps1`'s ledger figures
and `functions.tsv`. **The `voided_by` clause is not about ledger figures.** It is about per-function
annotation records — "any delta that removes or rewrites a comment, tag, name, prototype or body
range" — and that is measured in the FAS2 snapshots. This is that run, and it changes the ruling's
scope in one respect.*

### Why it had not been run, and it was not missing data (OPUS)

`check_delta_additivity.py --from GN161 --to PARENT` answered **"snapshot not in the tree"**, and
`check_transfer_eligible.py` reported every one of the 245 GN161-targeted transfers as
**UNMEASURED** — which reads like a failed basis and was really **an unnamed file**. Both tools
carry a `SNAP_BY_TAG` map with `GN158`, `GN160` and `PARENT` and no `GN161`. The GN161 snapshot was
sitting beside the current one the whole time, retained under `snapshot_GN161_0914_STALE.fas2` when
GN162 was certified. **Adding the tag is the whole fix**, and it is in both tools with a note.

### The span measured is the certified span, by hash (OPUS)

| file | sha256 | is |
|---|---|---|
| `work/verify_GFZ_PARENT/snapshot_GN161_0914_STALE.fas2` | `c16409ec…` | **GN161**'s certified `$GfzLineage` snapshot |
| `work/verify_GFZ_PARENT/snapshot.fas2` | `16a2a832…` | **GN162**'s certified `$GfzParentSnapshot` |
| `work/batch_R30/pre.fas2` | `c16409ec…` | byte-identical to GN161's |
| `work/batch_R30/post.fas2` | `16a2a832…` | byte-identical to GN162's |
| `work/batch_R109/post.fas2` | `c16409ec…` | byte-identical to GN161's |

**The lineage is continuous across the batches that produced it** — R109's post *is* R30's pre — so
the span measured below is the certified advance and not a lookalike.

### The measurement (OPUS)

```
check_delta_additivity.py --from GN161 --to PARENT
  changed records    30   fields touched: {'comment': 30, 'tags': 30}
  functions ADDED            0        IMMUTABLE field changes    0
  functions REMOVED          0        tag REMOVALS               0
  old tag set NOT a subset   0        comments REWRITTEN         0
  ADDITIVE: True
  CONTROL (one record renamed, its comment rewritten, its tag dropped)
    caught as NOT additive: True; immutable / tag-removal / comment-rewrite all fired.
```

All four spans in the tree now measure additive: GN158 → PARENT (158 records), GN160 → PARENT
(139), **GN161 → PARENT (30)**, GN158 → GN160 (19). **The `voided_by` clause does not fire**, at
record level, for any of them.

**And the 30 sit inside a set that was already swept.** The changed records are exactly the 30
addresses batch R30 classified, and they are a **strict subset of GN160's 139 residual addresses**
(verified by set containment, and none of them is still residual at PARENT, whose residual file is
empty). So `check_stranded_absence.py`'s existing sweep over the GN160-resolved set already covers
every one of them: **51 lines carry both a resolved address and absence language, of which 3 are
LIVE.**

### THE NARROWING (OPUS): "a stamp naming GN160 or GN161 transfers to GN162" is too broad

The section above ends with that sentence. It holds for an **additive-annotation** basis and it is
**false for a `snapshot-identity` one**, because snapshot identity is the strictly stronger claim —
*every record this document cites is byte-identical in both snapshots* — and 30 records stopped
being identical.

Per-document, from `check_transfer_eligible.py --transfers`:

| basis family | HOLDS | VOID |
|---|---:|---:|
| `additive-annotation` (both spans) | 93 | 0 |
| `snapshot-identity` (both spans) | 137 | **15** |

**The 15 each cite at least one of the 30.** They are listed with the records they cite in the
commit that carries this ruling; `game-application.md` cites three (`001D72F0`, `001D7A20`,
`0024B580`) and `the-shared-dialog-widgets.md` three (`002AC5F0`, `00566680`, `0056F810`); the rest
cite one each, with `0020AC30` and `0026F470` each appearing in three documents.

**Their basis is REPLACED, not re-targeted** — the same disposition, and for the same reason, that
`the-text-control-code-language.md` already carries from the GN158 → GN159 step: *"replaced rather
than re-targeted because that basis is FALSE for this document, which cites a record that changed."*
The weaker basis is measured and holds for all 15.

### Why moving the TARGET is not rewriting a stamp (OPUS)

The section above says *"It does not rewrite a single stamp, and `check_provenance` will still
report 244."* **That is right about the stamp and wrong about the tool**, and the distinction is
worth stating because it is the difference between a ruling nobody can act on and one that closes.

- `gzf_sha256` and `snapshot_sha256` record **which parent a document was actually verified
  against**. That is a historical fact, it has not changed, and rewriting it would assert a
  verification that never happened. **Untouched here, in all 236 documents.**
- `transfers_to.parent` records **which parent a measured basis carries that verification to**. It
  named GN161. GN161 is superseded. Leaving it there is not caution — it is a stale pointer, and
  `check_transfer_eligible.py` flags it in those words: *"245 name a SUPERSEDED parent, so their
  TARGET is stale."*

`check_provenance.py` already distinguishes the two and counts them separately — `transferred = [d
for d in gzf_derived if d["gzf"] != parent and d["transfers"] == parent]`, described in its own
source as *"records that a verification HOLDS against a later parent without rewriting the
`gzf_sha256` it actually ran against."* **That category existed and was empty.** Carrying the target
is what fills it, and it is the mechanism the tool was built around.

### What was carried, and what was held back (OPUS)

**236 carried**: 222 re-pointed with their basis intact and extended, 14 re-based from
snapshot-identity to additive-annotation. **9 held back, none of them silently:**

- **6 were peer-dirty in the worktree** at the moment of the carry. A stamp is frontmatter and a
  peer's uncommitted prose is in the same file; publishing one would commit the other.
- **3 carry the only LIVE absence claims in the corpus** — `the-shop-table-and-its-stock-gates.md`
  (`0057D620`), `ui-request-router.md` (`002ABF70`) and
  `numeric-formatting-and-character-mapping.md` (`002AC5F0`). **Two of those three addresses are
  among the 30 R30 just classified**, so the claims were written while the record was residual and
  may now be false. The transfer clause has two halves and this is the other one; the additivity
  half holds for all three. Routed as
  `OPUS-REQ-FABLE-THREE-LIVE-ABSENCE-CLAIMS-BLOCK-THE-GN162-CARRY`, and the carry applies to them
  the moment each line is settled either way.

### What this still does not do (OPUS)

**It does not make any of the 245 documents *verified against GN162*.** It records that a measured
basis carries an older verification forward, which is what a transfer is. A document whose claims
rest on a record R30 touched still owes a reading if its prose depends on what changed — the 15
re-based blocks say exactly which records that is.

**It does not touch the aggregate-claim exclusion**, which stands unchanged from the GN160 → GN161
ruling: a transfer covers per-function records, never statements about totals, and the 30 newly
classified functions move exactly that kind of figure. `check_transfer_eligible.py` counts 146
documents making a 100+ claim, 106 of them cleared vacuously by every per-address test.

**It does not open the gate.** `final_audits` is still 0 / 30 and cannot move until everything else
does.
