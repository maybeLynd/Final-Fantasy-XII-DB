# Consumer check: FABLE's routed OV-42 type-store text (OPUS, 2026-10-02)

One sentence on the scratch-block page is qualified, with no strike. The rest is additive: reader-list evidence on three
`fields.tsv` rows and two new OPUS sections.

- **Type store:** `_types/fields.tsv` (the evidence cells of three rows).
- **Affected:** 02-Resource-And-Asset-Pipeline/authored-data-table-registry.md, 08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the three fields.tsv rows, the registry page, the scratch-block page | revised-here |
  | FABLE's pages (OV-42 sections) | agrees (consumed at b128c3a2c) |
  | the mode-ladder page's `00306760` extent and `022C215C` row | routed-to-FABLE (FABLE's own later package, per its review) |
  | register row OV-42 | agrees (row-to-kind / caller / owner consistency stays open) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-ov42-typestore-1002/ov42_check.py, verified at eef52f02c: 18 checks,
  FAILS 0 ([`ov42_check.out`](ov42_check.out)).
