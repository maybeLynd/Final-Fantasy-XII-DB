# Per-member rows: the PClassDescriptorForType destructor thunks, one row per member (OPUS, 2026-10-03)

Host page: [`class-descriptor-and-metadata-system.md`](../../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md). It declares the family in its frontmatter (members file `pclassdescriptor-destructor-thunks.tsv`).

This record adds one row for each of **384** members, under the explained-once family sentence OPUS adopted for engine_explained ([`opus-ee-rulings-1003`](../opus-ee-rulings-1003/README.md)). Each row anchors the member's distinguishing instruction and states the member-specific value, both derived from the certified image. The shared form is stated once in the section's lead, and the lead is the authority for what each column means.

## Verified

- [`fam_rows.py`](fam_rows.py) `check` re-derives every row from the image and compares it with [`rows.tsv`](rows.tsv) ([`fam_rows_check.out`](fam_rows_check.out)):
  - members 384, committed rows 384, declared exclusions 0
  - control swapped-value refused, control moved-anchor refused
  - FAILS 0
- `fam_rows.py apply` is idempotent: a second run prints ALREADY.
- Page gates are run per batch before publishing: `nb_page`, `check_links`, `verify_doc_addresses`, `check_consistency` and `check_self_contradiction --db`.
