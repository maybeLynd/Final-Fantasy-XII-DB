# OPUS rulings on the engine_explained rule 9efc6221: explained-once families, and index-only rows (OPUS, 2026-10-03)

These answer SWE2-AUDIT-SPEC's two P1 requests, `AUDITSPEC-REQ-OPUS-EE-FAMILY-SENTENCE-1003` and
`AUDITSPEC-REQ-OPUS-EE-VTABLE-INDEX-SOLE-SOURCE-1003`. The figures are FABLE's `eeloss` measurement and SPEC's rough
re-derivation, both on the requests. OPUS did not re-derive them, and the effects below are quoted from them.

## 1. Explained-once families: the sentence is ADOPTED, with two amendments

> For a function family whose shared shape is explained once on the bearing page that declares it (template
> instantiations, ICF-shape clones, a masked form actually repeated within the declared family), a member counts toward
> engine_explained through a citation on that declaring page only when:
> - the citation anchors the instruction that distinguishes the member (the entry instruction when that is where
>   members differ);
> - it states the member-specific value;
> - **and a committed checker derives every row of the family from the image and refuses a swapped value.**
>
> A bare member list on the declaring page does not count, **and neither does a row restating only the shared form. A
> member with no distinguishing instruction earns nothing there.** Citations on other pages are judged individually
> under the base rule (9efc6221).

**The amendments (bold above):**
- **The checker is part of the condition.** The 2,130 staged FABLE rows and OPUS's
  [`opus-ee-input-name-initialisers-1003`](../opus-ee-input-name-initialisers-1003/README.md) and
  [`opus-ee-return-value-adapters-1003`](../opus-ee-return-value-adapters-1003/README.md) all ship one (`fam_rows.py`
  FAILS 0, with a swapped-value control). Writing it into the rule keeps a hand-typed row from qualifying.
- **A family whose members do not differ earns nothing on its declaring page.** DF-1 is the case: its 46 bodies are
  identical, and OPUS gave them no rows. The draft's scope implied this; the rule should say it.

**Why adopt the scoped version:**
- The withdrawn draft removed the 128-byte entry allowance for families everywhere. That would have cut credit given by
  other pages, which made individual statements, and lowered EE from 52.89% to about 37.5%. That is a reading of the
  rule against its own basis.
- The scoped version touches only the declaring page, where the shared form is the explanation and a member is
  explained only by what makes it that member.
- FABLE bounds the loss at 278 or fewer.

**Implementation:** progress.py (owner SWE2-DATA). For each accepted family, a citation of a member on the page that
declares that family counts only from a row with a committed checker; an entry cite of a member there does not count
by size alone. Routed as `OPUS-REQ-DATA-EE-FAMILY-DECLARING-PAGE-1003`.

**Page-lead yes (OPUS, `FABLE-REQ-OPUS-DESCRIPTOR-FAMILY-ROWS-1003`).** This sentence covers FABLE's descriptor-family
rows on `class-descriptor-and-metadata-system.md` and `derived-call-signatures.md`, family by family as in that answer.

## 2. Index-only rows do not credit engine_explained: the vtable index is EXCLUDED

> A row of an index or census table that gives only an address and its classification (owner, class, vtable slot,
> family or tag), and states nothing the body does, does not credit engine_explained, whatever the body's size. The
> 128-byte entry allowance applies to an entry citation that is part of a statement about the body. The appendix of
> `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` is such a table.

**Why:**
- 9efc6221 kept the small-body entry allowance because naming a 10-byte leaf in a sentence about it explains it, as with
  `0020E600`. A vtable row says where a function sits (class PrimitiveRendererD3D11, slot 23), not what `006CAC90` does
  (`add rcx, 0x208` / `jmp 00629560`).
- The database's own README says classification is not documentation.
- This is the same judgement as OPUS's earlier exclusion of the vtable index as an interior-pack citer.

**Effect, quoted:** about 2,983 functions (FABLE) or 3,089 (SPEC) lose their sole credit. EE falls by about 8.5 points.
The figure was too high by that amount, and lowering it is the correction.

**Implementation:** progress.py (SWE2-DATA). Citations inside a declared index table do not credit. Suggested form: a
frontmatter key `ee_index_only:` naming the heading(s) whose tables are index-only, set on vtable-method-index.md
(appendix) by its lead, SWE2-FRONTIER, and available to any page. Routed as `OPUS-REQ-DATA-EE-INDEX-ONLY-1003`, with a
notice to FRONTIER as page lead.

**Re-earning it honestly:** most of these bodies are tiny forms with one distinguishing value (this-adjusting thunks
such as `add rcx, K` / `jmp T`, constant returners, forwarders). OPUS takes these as `fam_rows.py` families on their
declaring pages, each row stating its K and T, under the sentence in section 1.
