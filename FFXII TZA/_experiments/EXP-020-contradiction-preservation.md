---
experiment: EXP-020
title: Preserve contradiction IDs and curated cells across extraction
status: VALIDATED — stable identity and curated-cell preservation
contract: none - contradiction-ledger preservation across an extractor change; a Method A tooling record that executes no shipping game code. Checked BOTH directions 2026-09-13: it names no contract and no contract names it
date_designed: 2026-09-10
method: A - offline instrument preparation
live_game: false
---

# EXP-020 — repair the mixed generated/manual ledger's identity boundary

FABLE-REQ-ASTRA-TOOLING reports that the extractor renumbers CON IDs, loses curated
cells when lines move, and matches examples in the correction ledger's own prose.
These are tool behavior questions, not original-game runtime claims. No reference
game is involved. EXP-019's reference was closed and restored before this package.

Compare the original extractor at commit 9f3c3f5 with the revised implementation on
isolated fixtures containing a curated CON-021, a shifted source line, an earlier
new marker and the documentation example. Preserve commands, both outputs and
source hashes. The original should demonstrate the reported loss; the revision
must preserve the ID and all curated cells while rejecting the example.

Exercise removed/reappearing markers, duplicate anchors/IDs, edited headers,
ambiguous legacy claims, malformed TSV rows, unknown columns, failed replacement
and stale ledger input. A failure must leave original ledger bytes intact. The
--db option must select that database's ledger unless --ledger explicitly overrides
it. This prevents isolated commands from defaulting to the canonical output path.

Before canonical extraction, produce a proposal from the existing 37-row ledger.
Adopt unique original source snippets automatically, and explicitly anchor only
the four reviewed manual rows CON-034 through CON-037. Retain CON-033, whose marker
is absent, with its historical cells and unmatched status. Assert every old ID and
every nonempty curated claim/correction/instrument/addresses cell survives. Repeat
extraction to prove idempotence, check source-file stability, then publish under
the existing file claim and @publication reservation. Never use a line-number
fallback to guess a legacy record's identity.

## Results and limits

The isolated [comparison](evidence/EXP-020-contradictions/comparison.json) reproduces
the old failure: three extracted rows include the documentation example, the actor
record loses CON-021, and its curated correction/instrument cells become
UNSUMMARISED. The revision emits two rows, retains CON-021 and all four curated
cells, and updates the actor's source location from line 1 to line 3.

The 14 regression tests pass. The first real-corpus migration attempt correctly
aborted before writing: normalizing whitespace before comparing a legacy snippet
prevented adoption of a historically spaced line. Matching against the original
extracted snippet fixes that migration boundary; a new spacing regression covers
it. Full source_header normalization remains separate from the preserved claim.
An initial fixture-driver invocation also failed before running either extractor
because its repository-parent calculation was wrong; the corrected path is used
in the retained comparison. Neither failed setup was counted as a semantic pass.

The [proposal validation](evidence/EXP-020-contradictions/proposal-validation.json)
starts with 37 old IDs and retains all of them, including every nonempty curated
claim/correction/instrument/addresses cell. CON-021 survives actual line drift;
CON-034 through CON-037 receive the four explicit reviewed anchors. CON-033 is
retained as legacy-unmatched because its prior dated marker is absent. The proposal
contains 59 records from 58 current markers plus that unmatched historical record.
New IDs extend the old maximum instead of shifting earlier IDs. A fresh CLI
[re-extraction](evidence/EXP-020-contradictions/idempotence.json) is byte-idempotent.
The [published migration](evidence/EXP-020-contradictions/published-migration.json)
retains all 120 nonempty curated cells, including the unmatched record's cells.

This is correction-marker extraction. It does not find unmarked semantic conflicts,
summarize new corrections, prove every marker meaningful, or restore a marker
removed by an earlier author. Historical unmatched line numbers are explicitly not
verified current locations. Changing a source header can require a reviewed anchor
update. Atomic replacement and stale-byte checks still rely on the existing
publication/file ownership protocol for concurrent writers.

The existing knowledge_db reader projects its ten named semantic columns, so the
two new source-tracking columns do not change that projection. No canonical SQL
database or unrelated generated index is regenerated in this package. Remaining
FABLE-REQ-ASTRA-TOOLING items are the control-byte regex defects, RULES docstring
leak and three answered/not-established reports; this package does not claim them
fixed.
