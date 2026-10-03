# Consumer check: FABLE's routed OV-42 batch-6 texts (OPUS, 2026-10-02)

The registry page's AG-12 row and the paragraph after it are corrected with strikes (FABLE's OLD -> NEW, FABLE
concurring). The MP page's EXP-061 sentence is qualified, with no strike. The rest is additive.

- **Type store:** `_types/fields.tsv` (the evidence cells of `AuthoredTableHeader` `+0x08` and `+0x0C`).
- **Affected:** 02-Resource-And-Asset-Pipeline/authored-data-table-registry.md, 10-Status-Periodic-Terminal/where-mp-comes-from.md, 01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the registry page (AG-12 block, new section), the MP page, the calling-convention page, the two fields.tsv rows | revised-here |
  | FABLE's availability page and console slice A (OV-42 subsections) | agrees (consumed at 28534fcdb) |
  | FABLE's review drafts for the six packets | agrees (FABLE wrote the AG-12 OLD -> NEW and concurred in advance) |
  | register row OV-42 | agrees (natural kind-to-row, caller, owner and binding consistency stays open) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-ov42-batch6-routes-1002/batch6_check.py, verified at ace5507ec: 63 checks,
  FAILS 0 ([`batch6_check.out`](batch6_check.out)).
