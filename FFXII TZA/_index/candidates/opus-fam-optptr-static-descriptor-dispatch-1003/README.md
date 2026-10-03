# Rebuild checker: optional-pointer context dispatch adapters, static-descriptor spelling (OPUS, 2026-10-03)

For SWE2-AUDIT-SPEC request `AUDITSPEC-REQ-OPUS-R9-FAMILY-REBUILD-CHECKERS-1003`. Supplement: [`auditspec-r9-family-checker-exposure-1003`](../auditspec-r9-family-checker-exposure-1003/README.md).

- **Host page:** [`phyre-script-object-accessors.md`](../../../22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md), which declares the family. Members file: `22-Middleware-PhyreEngine/Script-Object-Accessors/members/optptr-static-descriptor-dispatch-adapters.tsv`.
- **Rows already on the page:** package [`opus-member-ontext-dispatch-adapters-static-descriptor-spelling-1-r9`](../opus-member-ontext-dispatch-adapters-static-descriptor-spelling-1-r9/README.md). This record adds no page text, and `apply` is never run.

## Key (OPUS)

Each member is identified by the `lea` at entry+0x14 (its rip-relative target). The value column of [`rows.tsv`](rows.tsv) is that value. The anchor column is the first key instruction, and every published row already cites it (`check` re-reads the page to confirm).

The other per-member positions, +0x20 `jmp` (target), are derived too. They are compared through the name column (`+0xOFF=value`), and each has its own swapped-field control.

## What the checker does (OPUS)

[`fam_rows.py`](fam_rows.py) (kind `operand_at`, the same file in every `opus-fam-*-1003` record), run with `check`, does the following:
- It decodes each member over its census extent (60 bytes). It requires the body to equal the committed normalised form in [`spec.json`](spec.json) instruction by instruction, with only the key and field positions masked. Any other difference refuses the member.
- It derives every row and compares the result with the committed `rows.tsv`, column by column.
- It runs controls through the same comparison, each of which must be refused: a swapped value, a moved anchor and a swapped field. A known-answer line recomputes the first row's key from the anchor's raw bytes without capstone.
- It requires the key to be unique across the family.
- It requires each anchor to be cited in its member's row on the page.
- It requires every excluded member to keep its stated status: a member refused by the form fails the check if it starts matching, and a declared skip must still derive.

## Members without a row (OPUS)

Listed in [`excluded.tsv`](excluded.tsv):
- `00584C70`: skip: not in the r9 member pack, which held only frontier members; cited on 22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md, so no row on this page (it still derives: check re-verifies)

## Result (OPUS)

15 rows, from [`fam_rows_check.out`](fam_rows_check.out):

```
members 16, committed rows 15, declared exclusions 1
control swapped-value: refused (2 failure(s) from the comparison)
control moved-anchor: refused (1 failure(s) from the comparison)
control swapped-field +0x20: refused (1 failure(s) from the comparison)
known answer 005847A0: anchor 005847B4 references 02CA9FA0 in its raw bytes = committed value
skips: 1 re-verified (still derive)
key unique: 16 member value(s), 0 shared
page citations: 15 of 15 anchors cited in their member's row
FAILS 0
```

## engine_explained (OPUS)

This is the committed checker that ruling `opus-ee-rulings-1003` section 1 requires for this family. Each member's published row anchors the distinguishing instruction (the `lea` at entry+0x14 (its rip-relative target)) and states its value. `fam_rows.py` derives every row from the certified image and refuses a swapped value, so the provisional-credit narrowing in the family's review lifts once this record is committed. `progress.py` reads `page` from spec.json and `entry` / `anchor` from rows.tsv, and a member credits only through a citation of its anchor on that page.

Limits: static evidence only. These rows state what each body does, not what it means. `check` needs an interpreter with capstone and pefile (the analysis venv).
