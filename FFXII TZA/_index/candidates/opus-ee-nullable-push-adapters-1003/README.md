# Per-member rows: the script-VM nullable object push adapters, one row per member (OPUS, 2026-10-03)

Host page: [`phyre-script-object-accessors.md`](../../../22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md). It declares the family in its frontmatter (members file `nullable-object-push-adapters.tsv`).

This record adds one row for each of **287** members, under the explained-once family sentence OPUS adopted for engine_explained ([`opus-ee-rulings-1003`](../opus-ee-rulings-1003/README.md)). Each row anchors the member's distinguishing instruction and states the member-specific value, both derived from the certified image. The shared form is stated once in the section's lead, and the lead is the authority for what each column means.

**No rows: 8 members**, each listed with its reason in [`excluded.tsv`](excluded.tsv):
- 8: descriptor not named by exactly one class.

The other 8 are refused by the image for this family's per-member form, and `check` fails if any of them starts deriving.

## Verified (OPUS)

- [`fam_rows.py`](fam_rows.py) `check` re-derives every row from the image and compares it with [`rows.tsv`](rows.tsv) ([`fam_rows_check.out`](fam_rows_check.out)):
  - members 295, committed rows 287, declared exclusions 8
  - control swapped-value: refused (2 failure(s) from the comparison)
  - control moved-anchor: refused (1 failure(s) from the comparison)
  - known answer 005A2BA0: anchor 005A2BB8 references 02CAF0E0 in its raw bytes = committed value
  - FAILS 0
- The controls pass mutated copies of the committed rows (swapped value, moved anchor and, where groups exist, swapped group) through the same comparison and require it to fail; the known-answer line recomputes the first row's value from the anchor's raw instruction bytes without capstone.
- `check` needs an interpreter with capstone and pefile (the analysis venv).
- `fam_rows.py apply` is idempotent: a second run prints ALREADY.
- Page gates are run per batch before publishing: `nb_page`, `check_links`, `verify_doc_addresses`, `check_consistency` and `check_self_contradiction --db`.
