# Judgement — the untagged entry-only population (OPUS-REQ-SWE2-EC7-ENTRY-ONLY-1433)

**Question asked:** the largest row of the undeclared entry-only mentions is the
functions carrying no `GFZ.V121.CodeDomain` tag — 1,433 at snapshot
(`entry-only-undeclared-families.tsv`, commit `df1efae7`), **1,504 re-measured
2026-09-16** (the pool grows as documentation grows; the figure is a moving
residual, not a fixed set). A documented page names each entry; the ledger
classifies none. Does the entry-mention overlap make them a cheaper
classification target than the untouched frontier — or are they entry-mentioned
precisely because nobody read them, making the overlap meaningless?

**Judgement: usable — as a stratified work index, not as declaration substrate.**
The overlap is not meaningless (the mentions carry real per-function context),
but the mention itself is never a membership predicate, so it cannot seed a
class declaration directly. Measured structure of the 1,504:

## What the overlap actually contains

| slice | count | what the mention carries | disposition route |
|---|---:|---|---|
| index-mirror | **181** | vtable slot + named class (99 distinct: `SebAudioBank`, `SepAudioBank`, `PFramework::PInputDevice*`, `PSerialization::PStream*`, `PInputs::PInputSource*`, audio controllers/readers…) | **directly declarable** — `vtable-method-index.md` is a COL-validated mirror of `.rdata`; "slot N of class X's vtable" is a falsifiable, image-derivable membership rule, exactly the verb-adapter pattern |
| hypothesis-bearing | ~1,300 | the citing page names the entry while describing behaviour (world-tick step tables, battle-unit field map, audio boundary walkthroughs); 1,495 of 1,504 carry a GFZ comment and 240 carry a semantic name (`BattleUnit_*`, `PartyFocus_*`, `Navigation_*`, `RenderCommand_*`…) | a per-function A-read that starts with a falsifiable hypothesis instead of a blank body — cheaper per member, but one at a time |
| bare mention | residue | entry cited in passing | equivalent to untouched frontier with a subsystem pointer |

Mention-context census of the 1,504 (entry × citing page): 1,208 have at least
one markdown **table-row** mention, 158 are prose-only, 138 list/code-block
only. But table-row ≠ index: the vtable index is an image mirror, while the
world-tick tables (178 untagged entries) are narrative step descriptions —
context for a reader, not a membership rule.

## Why "cheaper" — and why not free

- **Cheaper is real.** 99.4% of the set carries a GFZ comment and the citing
  pages concentrate: the top 25 pages hold ~40% of the mentions. Each function
  is *load-bearing for an existing document* — the page asserts behaviour that
  routes through that body. Reading one validates a live claim and removes a
  frontier member in the same pass: the overlap is where documentation debt and
  classification debt intersect, so each unit of work pays down both.
- **Not free.** A mention is a pointer, not evidence. "Functions cited on page
  P" is a citation set, not a falsifiable class — a B row built on it would be
  exactly the label `check_dispositions` refuses. Every declaration still needs
  its own image-derived selector and controls.
- **Not privileged by size.** Median 96 B vs 105 B for the whole frontier;
  51 bodies >1 KB vs 577 frontier-wide — the bodies are ordinary.

## Consequence

1. The **181 vtable members** are a standing family candidate: per-class-cluster
   B rows with a COL-walk selector reproducing the index's own derivation. The
   audio clusters (`Sep*`/`Seb*`/`Shout*`/`Music*`/`Stream*` banks and
   controllers) and the `PInputs`/`PFramework` device classes are the dense
   first targets.
2. The remaining ~1,320 go to the A-attribution queue **ordered by citing page** —
   a page-local read answers "what was this doing there" with the hypothesis
   already printed.
3. No class declaration may rest on the overlap itself.

*Analysis: `check_dispositions.evaluate` frontier ∩ `measure_a` entry-only ∩
functions.tsv CodeDomain-less, citation contexts re-scanned over DOCUMENTED
pages, 2026-09-16. Figures: 9,150 entry-only total, 5,148 undeclared, 1,504
untagged.*
