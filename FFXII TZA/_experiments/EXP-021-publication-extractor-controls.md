---
experiment: EXP-021
title: Control-byte address guards and rules docstring extraction
status: VALIDATED — bounded source defects repaired
contract: none - publication-extractor controls; a Method A tooling record that executes no shipping game code. Checked BOTH directions 2026-09-13: it names no contract and no contract names it
date_designed: 2026-09-10
method: A - offline instrument preparation
live_game: false
---

# EXP-021 — make the publication extractors implement their stated operations

FABLE-REQ-ASTRA-TOOLING asks whether four hygiene reports indicate real behavior
defects and whether RULES.md's leaked triple quotes come from its generator. No
reference game or canonical semantic type/contract is changed by this package.

The [original sources](evidence/EXP-021-publication/baseline-sources.json) contain
three literal backspace bytes: gen_address_index.py's ADDR_LONGHEX,
knowledge_db.py's ADDR_LONGHEX, and program_coverage.py's LONGHEX. Each is used by
an active extraction path. The patterns require a real backspace character, so
ordinary long hexadecimal text is not removed. Restoring the intended escaped
word-boundary matches such text and retains an isolated eight-digit address.
This repairs an active guard; it does not establish that published citation counts
were wrong.

The [old/new comparison](evidence/EXP-021-publication/comparison.json) runs both
knowledge_db.citation_forms and program_coverage.cited_addresses over the same
captured Markdown texts, and the actual old/new gen_address_index CLI over identical
frozen numbered-category Markdown/TSV files and function-table bytes. **No current
citation differences occur, and the two complete address-index outputs are byte
identical.** Other address patterns already reject ordinary long tokens. No citation
or readiness total is corrected on the basis of a hypothetical error. These controls
do not claim to solve every possible malformed symbol spelling.

The two literal byte-2 characters in census_bin_signatures.py are inside the
self-test's NAV version byte strings. Writing them as escaped hex preserves the
entire module's parsed AST, including those byte constants. The classifier behavior
is unchanged; this is a source-hygiene correction, distinct from the regex repair.

The rules generator used a regex over the first 400 characters of each script.
One-line docstrings leaked their closing triple quotes, and docstrings whose opening
quotes occupied a line alone were omitted. Parsing the module AST and reading its
module docstring fixes both without executing source. On the compared script set,
99 old entries become 105: six existing module docstrings are recovered, and five
one-line entries lose delimiters. The exact changed names and titles are retained
in the comparison. This is an index of source descriptions, not a claim that every
listed script is a build gate.

Five regression controls cover the ordinary long-token boundary, valid neighboring
citations, NAV classification, one-line/single-quoted/multiline/late module
docstrings, rejection of nested function docstrings as module descriptions,
non-execution of top-level code, and invalid-source rejection. The existing NAV
and rules-generator self-tests are also retained in validation output.

Original source snapshots use .bin suffixes to preserve their literal control
bytes as historical evidence. The clean-source hygiene gate covers the repaired
current kit, not a rewritten version of those old receipts. Only RULES.md requires
regeneration: the compared citation/index outputs are unchanged, so this package
does not rebuild canonical ADDRESS-INDEX, the knowledge database or coverage totals.

The remaining answered-question reports are advisory candidates, not automatic
semantic failures. A current run reports nine lines. Initial inspection separates
stale I-6/AY-10/DD-1 prose from adjacency to unrelated open questions, struck-through
history and the reopened DG-1 row. They require their own bounded checker/disposition
package; this experiment does not mark them corrected.
