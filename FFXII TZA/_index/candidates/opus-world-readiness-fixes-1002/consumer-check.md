# Consumer check: 03-World contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-03-VALUES-1002. Cloud wave 3 mapped `03-World-Area-Field/` from a text snapshot (session
`session_015MguvEESqUEwUm6JUUqGBu`; report `cloud-reports/re-readiness/03-world.md` in maybeLynd/Final-Fantasy-XII-DB,
68343d98; rated NOT YET). Its 28 value-changing contradictions were page-text only. OPUS decided 23 of them at the
shipping image, and a local read-only pass decided the other five plus the count items. The control is `world_check.py`.

What the bytes show:
- The trigger radius is horizontal and the threshold is the f32 nearest 1.3.
- A missing field table is permissive for `00377700`.
- `00377C70` takes bits 4-6.
- The resolver draws only in the slot-2 arm and falls back to the current slot, so all-zero probabilities pin the
  weather.
- The init latch still runs `003601C0(0xB/0xC)`.
- The MWeather entry index is `3*selector + slot - 1`.
- `00210570` can store into `01F83530` through id `0xFFFB`.
- `0209A6E8` is the weather slot, which selects bits 24-26.

The pass drafted 114 strike edits (`apply_03world.py`). OPUS applies the 31 on its own lines (`apply_by_owner.py
OPUS`). The rest go to their owners as requests:
- 52 to SWE2-EC7;
- 19 to FABLE;
- 10 to SWE2-FRONTIER (the accessor contract and FRONTIER's line on the call-chain page);
- 2 to SWE2-DATA.

The map-pack page's 12 EC7 edits should wait for SWE2-AUDIT-SPEC's ACTIVE OPUS-REQ-AUDITSPEC-MAPCTRL-INTERIOR-1001.

- **Affected:** 03-World-Area-Field/CONTRACT-weather.md, 03-World-Area-Field/README.md, 03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md, 03-World-Area-Field/walking-into-an-authored-trigger-point.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the weather contract, the README, the call-chain page and the walking page (OPUS lines) | revised-here |
  | navimapdata, map-pack, mweather, apply, probability and slot-state pages | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 52 edits; map-pack after SPEC's MAPCTRL review) |
  | the trigger contract, the variant contract and the bit-15 page | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 19 edits) |
  | the accessor contract and FRONTIER's call-chain line | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER`, 10 edits) |
  | the variant-choosing page | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 2 edits) |
  | RE repo `docs/readiness/03-world.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-world-readiness-fixes-1002/world_check.py, verified at aac0489ac: 22 instructions decode as cited, FAILS 0 ([`world_check.out`](world_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (31), FAILS 0.
