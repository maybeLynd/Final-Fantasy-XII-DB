# Consumer check: 06-Movement contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-06-VALUES-1002. Cloud wave 2 mapped `06-Movement-And-Navigation/` from a text snapshot
(session `session_01MKBAiNUqEAFXnUNyPRoqu9`; report `cloud-reports/re-readiness/06-movement.md` in
maybeLynd/Final-Fantasy-XII-DB, 899678f8; rated NOT YET). Its 43 value-changing contradictions were page-text only.
OPUS decided 33 of them at the shipping image, and a local read-only pass decided the other 10 plus the count items.
The control is `movement_check.py`. Several outcomes overturn a dated correction or a "favoured" side:
- `003A1C50` returns a closed `[-pi, pi]`.
- `0033CB70` does not loop past `4pi`: its result can leave `[-pi, pi]`.
- EC7-22's sign of `0026B5A0`'s bias is reversed.
- The `02AC7Cxx` cell and list addresses have no references; the real ones are `02B57Cxx`.
- The time base does leave 1: it is set to 2 at `001EDDF2`.
- The arrival curve keeps speed A as a floor (`00339DBB`).
- `+0x5C` (pi) is a dead store, so there is no half-turn ceiling.
- Every map-id override verb reaches the navigation caches.

The pass drafted 123 strike edits (`apply_06movement.py`). OPUS applies the 37 on its own lines (`apply_by_owner.py
OPUS`). The rest go to their owners as requests:
- 64 to SWE2-EC7;
- 20 to FABLE, 5 of them lines FABLE wrote on OPUS-led pages;
- 2 to SWE2-DATA.

- **Affected:** 06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md, 06-Movement-And-Navigation/CONTRACT-corridor-query-family.md, 06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md, 06-Movement-And-Navigation/CONTRACT-movement-body-pool.md, 06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md, 06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the six OPUS-led and shared 06 pages (OPUS lines) | revised-here |
  | the facing contract and the heading, pool, turning and mode pages | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 64 edits) |
  | the nav page, nav contract, separation contract, README, and FABLE's lines on the turn-limiter contract and the animation page | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 20 edits) |
  | the clamp page and the shape page's D5A0 code line | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 2 edits) |
  | RE repo `docs/readiness/06-movement.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-movement-readiness-fixes-1002/movement_check.py, verified at 3e0fc5be9: 38 instructions decode as cited, FAILS 0 ([`movement_check.out`](movement_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (37), FAILS 0.
