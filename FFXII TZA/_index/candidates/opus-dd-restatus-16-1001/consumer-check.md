# Consumer check: corrections in owner re-status batch 16 (OPUS, 2026-10-01)

Batch 16 incorporates SWE2-AUDIT-SEM's corrections on three pages and strikes the old text.

- **Corrects:** in equipment-slots-and-the-single-stat-rebuild.md §11.3, "the list body `0027CF2A` offers them only while the actor has a takeaway backup" (C4) and the struck "Open: what an issued 0x9C / 0x9D changes" (GR-12 answered); in the-selection-the-menu-publishes.md, "`00279E20` rewrites the whole dword at construction" (N1) and the in-play sentence without its two gates (C1); in the-battle-hud-layout-readers.md, SD-128's "fade level, anchor offset" as readings (N3).
- **Affected:** 12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md, 16-UI/the-selection-the-menu-publishes.md, 16-UI/Battle-Hud/the-battle-hud-layout-readers.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the three pages' own sections and status lines | revised-here |
  | _index/OPEN-QUESTIONS.md row GR-12 (the stash wording survives only in the kept-as-history part; the ANSWERED lead does not carry it) | agrees |
  | _index/OPEN-QUESTIONS.md row SD-125 ("closes itself unless the top list is showing", without the two gates) | routed-to-FABLE (OPUS-REQ-FABLE-SD125-C1-1001) |
  | _index/OPEN-QUESTIONS.md row SD-128 ("fade level") | routed-to-FABLE (OPUS-REQ-FABLE-SD125-C1-1001, N3) |
  | _index/candidates/sd125-sd128-fable-0930/README.md and gr12-actions-9c9d-fable-0930/README.md (FABLE's records) | routed-to-FABLE (the same requests) |

- **Regression:** Database/FFXII TZA/_index/candidates/auditsem-review-sd125-128-0930/sd125_128_sem.py (28 checks) and
  Database/FFXII TZA/_index/candidates/auditsem-review-gr19-gr11-0930/gr19_11_12_sem.py (17 checks),
  run: sd125_128_sem.py and gr19_11_12_sem.py at fdc46b6eb (FAILS 0).
