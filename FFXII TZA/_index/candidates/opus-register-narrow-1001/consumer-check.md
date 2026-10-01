# Consumer check: register cell narrowings (OPUS for SWE2-DATA, 2026-10-01)

- **Corrects:** in _index/OPEN-QUESTIONS.md, GR-19's "when x is NaN" and "in another colliding body's reach, inside static geometry, off the map grid or off walkable ground"; SD-125's in-play sentence without its two gates; SD-128's "fade level" as a reading; AL-8's untracked evidence path.
- **Affected:** _index/OPEN-QUESTIONS.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the five register cells | revised-here |
  | 13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md (GR-19) | agrees (narrowed in batch 17) |
  | 16-UI/the-selection-the-menu-publishes.md (SD-125) and 16-UI/Battle-Hud/the-battle-hud-layout-readers.md (SD-128) | agrees (narrowed in batch 16, e042d3ab8) |
  | 04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md (GR-2 section 7, AL-8) | routed-to-OPUS (owner re-status next, with the C1-C5 page text) |
  | FABLE's records gr19-gr11-placement-fable-0930, sd125-sd128-fable-0930, gr2-free-target-types-fable-0930 | routed-to-FABLE (the open requests) |

- **Regression:** Database/FFXII TZA/_index/candidates/auditsem-review-gr19-gr11-0930/gr19_11_12_sem.py,
  Database/FFXII TZA/_index/candidates/auditsem-review-sd125-128-0930/sd125_128_sem.py and
  Database/FFXII TZA/_index/candidates/auditsem-review-gr2-0930/gr2_sem.py,
  run: gr19_11_12_sem.py, sd125_128_sem.py and gr2_sem.py at e042d3ab8 (FAILS 0).
