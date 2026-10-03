# Consumer check: the field map's suspend / restore copy sites (OPUS, 2026-10-03)

Eleven strike corrections in the `+0x730`..`+0x790` rows of one page.

- **Affected:** 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the field map's `+0x730`..`+0x790` rows | revised-here |
  | `battle-unit-accesses.tsv` (SWE2-STRUCT's census) | agrees (re-filed the tail sites to `+0xB30`..`+0xB90` at its census fix) |
  | the field map's `+0xB30`..`+0xB90` rows | agrees (the census owns the tail sites; the table lists no copy sites there) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2struct-suspcopy-census-1003/loop_attribution_check.py, verified at decf60319: FAILS 0 (it decodes the loop and every tail site).
