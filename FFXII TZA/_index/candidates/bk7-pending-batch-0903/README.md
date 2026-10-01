> **Tracked copy (FABLE, 2026-09-30).** This is a verbatim copy of `Database/Tools/work/pending_batch/README.md`, the pending-batch staging note (2026-09-03), which register row BK-7 cites. The original lives in gitignored `Tools/work`, so the documented-status rule's condition T could not read it (AUDITSEM-REQ-FABLE-DDRULE-T-TOOLSWORK-0930). Nothing below this header is edited.

# Staged pre-enrichment rows

**batchA is APPLIED (2026-09-03, batch id `M55A`) and NOT YET PACKED.** `APPLY EXIT: 0`,
`changed=4  immutable_drift=0  added/removed=0/0`, diff clean, pre-snapshot identical to the
certified `$GfzParentSnapshot`. Artifacts in `work/batch_M55A/`. **Close the project, then run
`Pack-GfzCheckpoint.ps1` in a SEPARATE invocation** — the wrapper says so and it is not optional.

`batchB1` and `batchB2` remain staged and unapplied.

---


Held by `repos-55`, which holds mutation authority. Ten rows, verified, **split into three batches by
fence requirement rather than by source.**

Nothing here has been through `EnrichCurrentBodyManifest`. Do not hand-author the hashes — the
enricher computes the address-salted hash the apply gate wants, and the hashes quoted in prose are
the *other* convention and will abort the gate.

## Why three batches and not one

`Apply-GfzBatch.ps1 -AllowExistingTag` is a **batch-level** flag. A batch that mixes rows which need
it with rows which do not **applies the weakened fence to rows that never asked for it**, and it
succeeds either way — so nothing in the result would say it had happened.

> **A flag applied to the whole batch is applied to the rows that did not need it, and a gate that
> passes in both cases cannot tell you which you got.**

This was nearly committed on 2026-09-03: the ten rows were first staged as one ledger-moving batch
plus one "re-classification" batch, on the assumption that everything not from the residual already
carried a `CodeDomain`. **Two of the six did not.** Checked rather than assumed, per the standing
rule that a control must be able to fail.

## batchA_ledger_moving.tsv — 4 rows, PLAIN apply

| entry | size | state |
|---|---:|---|
| `003649A0` | 3,020 B | residual, tags empty |
| `00366110` | 1,318 B | residual, tags empty |
| `00364530` | 684 B | residual, tags empty |
| `0053E0B0` | 718 B | residual, tags empty |

**All four are in the residual 158 with completely empty tag fields**, verified against
`verify/residual_addrs.txt` and `graph/functions.tsv`.

**Applying this batch takes unresolved 158 → 154 and explicit 38,003 → 38,007 — the first movement in
the residual count of the entire campaign.**

Evidence is the strongest in the staging area: complete-body reads with the glyph LRU cache, a
22-entry jump table decoded from the EXE independently of the decompiler with exact agreement on
eleven real cases, 12.4 fixed-point texture coordinates built from named `.rdata` constants, and a
**tier-2 corroboration** — the authored string `'display : draw Font'` whose sole `.text` reference
sits inside the scope-close the function calls. Every row ends *"No PrimaryOwner inferred"*, which is
correct: a `CodeDomain` classification is not an ownership claim.

## batchB1_new_classification.tsv — 2 rows, PLAIN apply

`00313A00` and `002F7380` carry tags but **no `CodeDomain`**, so they take the strict fence too. They
are not residual, so they move `explicit` without moving `unresolved`.

## batchB2_allow_existing.tsv — 4 rows, `-AllowExistingTag`

The `008A5Bxx` rows **already carry a `CodeDomain`** (a generic shape class), so these are
re-classifications: they move the ledger by **zero** and their value is replacing an honest shape
label with a mechanism identity.

**Gate decision, 2026-09-02, unchanged:** the proposing session's evidence was *"declared SEH filters
in `__C_specific_handler` scope tables"*. **A scope table is `.xdata` — an EH map — and the mission
bans it as semantic evidence absolutely.** A prior branch used that class of evidence and lost 182
classifications. Each of the original six was judged on its **complete body alone**, with the scope
table disregarded; two were refused and two relabelled.

## Why they have not been applied yet

Not size, and no longer doubt about the rows. **A `mutate → pack → fresh-import → re-certify` cycle
changes the parent checkpoint every session imports from**, and four sessions have been continuously
mid-block reading bodies. The cycle runs when the current blocks land.

Parent: `work/gn158_certify/GFZ_GN158.gpr`, no lock held. Order: **A, then B1, then B2** — the strict
fences first, so an unexpected failure lands before any weakened flag has been used.

---

## batchB1 is RETIRED — both rows were already classified

**2026-09-03.** `Apply-GfzBatch` refused both rows at enrichment, mutating nothing:

```
RuntimeException: already classified 00313A00
RuntimeException: already classified 002F7380
```

**The fence worked.** It aborted at step 2 of 5, before any write, both times.

**The cause is that these rows' eligibility was checked against `graph/functions.tsv` — the 01:09
dump — which shows neither function carrying a `CodeDomain`.** The live project disagrees. **Tags are
exactly what that dump is stale about**, and tags are exactly what eligibility depends on.

> **The same stale dump that made a document's census wrong by two functions this morning made a
> mutation's eligibility check wrong by 100 %.** The scorer was audited and found clean because it
> reads only addresses and sizes. **The eligibility check was never audited, because it is not a
> number — it is a decision.**

**Both files are retired rather than deleted**, so the proposed domains survive. If either proposed
domain is better than what the project now carries, that is a **re-classification** requiring
`-AllowExistingTag` and a fresh comparison against the live tag — **not the strict-fence batch they
were staged as.**

**Standing consequence for this directory: no row here may be staged or applied on the strength of
`graph/functions.tsv`.** Eligibility is a property of the live project and only the gate knows it.
Re-dump before re-staging.

`batchA` is applied (`M55A`, clean). `batchB2` is unaffected — its four rows were **known** to carry
an existing `CodeDomain`, which is why they were separated in the first place.
