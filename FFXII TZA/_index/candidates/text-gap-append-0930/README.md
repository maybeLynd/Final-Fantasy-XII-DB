# Text-gap registry extended for the terminal-audit dry run (OPUS, 2026-09-30)

FINAL-AUDIT pass 1 / 17 (`verify_doc_addresses.py --all`) listed **50 documents** with cited `.text` addresses
that are neither a function entry nor inside a listed body. `text-gap-citations-250.tsv` is the registry that
settles them, but it held only the 250 addresses cited up to GN160.

**What was done (the seeder is never re-run on the registry):**

- `textgap_append.py` runs **scratch copies** of the kit's `gen_text_gap_citations.py` (seeder) and
  `gen_text_gap_classification.py` (classifier). Both are pointed at scratch files, so no existing row is re-seeded
  or re-classified.
- It appends only the **273 addresses the registry did not hold**: 115 TABLE, 29 PAD, 11 UNLISTED, and
  118 UNCONFIRMED from the classifier's own rules.
- The registry marks the appended rows with a dated header line.
- `textgap_rule13.py` gives hand verdicts to the 13 appended rows the verifier still listed. Each was checked
  against the image's 35,713 `.pdata` ranges and decoded:
  - **`00129640` is UNLISTED.** It is a body start: the previous body ends `pop rbp; ret`, and this one opens with
    a full frame prologue.
  - **Six addresses are interior points of the unlisted run `0012B980..00133B40`.** That run has no `.pdata` at
    all, so they are deferred on UC-1.
  - ~~**Four addresses are interior to real `.pdata` extents of bodies the list cuts short:** `00808ED9`,
    `00121E11`, `0015AE4A`, and `0036F22E` (a chained fragment).~~ **Four addresses decode as code inside bodies
    the list cuts short:** `00121E11` is the second byte of `jmp $` at `00121E10` after the `ret` at `00121E0E`,
    `0036F22E` is `mov eax, edi` in the epilogue ending `ret` at `0036F23A`, `00808ED9` and `0015AE4A` are epilogue
    instructions. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-pass6-opus-rows-0930/REVIEW.md) text-gap row; the reword lapses disposition row 76, which SWE2-AUDIT-SPEC re-signs)*
  - **Two addresses are the recorded cut points of cut-short bodies:** `00148F41` and `001491CE`.

  None is data cited as code.

**Result:** `verify_doc_addresses.py --all --db "FFXII TZA"` reports **0 documents** with `.text` non-function
citations to confirm.

**Limits:**

- The 105 appended UNCONFIRMED rows the verifier does not list are cited only outside its document population
  (for example under `_experiments/`); they wait for a hand verdict.
- The 14 `unwind-BANNED` citations are pass 6's, not this registry's.
