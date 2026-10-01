# Consumer check — SWE2CONTRACT-PUB-CONTRA-01F68168 corrections (SWE2-CONTRACT, 2026-09-26)

Consumer record for the six files carrying struck/Superseded/CORRECTED markers in this publish.
Each row lists the correction, the affected consumers, their agreement state, and the regression
that measures the claim.

## Corrections and consumers

| file | correction | consumers | state | regression |
|---|---|---|---|---|
| `00-Engine-Core-Runtime/CONTRACT-shared-transform-workbench.md` | TW-6 reworded off "no rip-relative store" onto the indexed-store route actually decoded; BQ-16 closed | `CONTRACT-transform-workbench-save-restore.md` §10/§15; `Reconstruction/Tests/Differential/diff_workbench_save.py` | agrees — harness drives the same offsets | `diff_workbench_save.py` (drives `00502280` paths, 0 mismatches at last run) |
| `00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md` | `022D8F0C` belongs to workbench save/restore (`00502280`), not "functions with no relationship"; N bounded by layout | `_index/OPEN-QUESTIONS.md` WBSAVE row; `diff_workbench_save.py` | agrees — the four-row bound is what the harness enumerates | `diff_workbench_save.py`; field census `field_access_index.py` output embedded in the page |
| `12-Items-Equipment-Shops-License/CONTRACT-shop-stock-ladders.md` | "12 rows all-gated" -> **11** — row 2's `k3@1` tail always passes because the clan rank's floor is 1 (FABLE on OPUS block 324, riding this publish — disclosed) | `the-shop-table-and-its-stock-gates.md` §7; `_index/OPEN-QUESTIONS.md` SG-2 | agrees — both files now say 11 | direct table scan of the shipped shop table (scan recorded in §14; `check_counts.py` over the row census) |
| `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md` | same 12→11 correction | `CONTRACT-shop-stock-ladders.md` §14; `_index/OPEN-QUESTIONS.md` SG-2 | agrees | same shipped-table scan |
| `13-Rewards-Progression-Economy/CONTRACT-world-loot-pickup-pool.md` | `00319850` (nearest selector) has exactly one caller — `BattleLocomotion_DecodeOrderGoal` — not zero | `world-loot-pickups-the-ten-slot-pool-and-the-despawn.md`; `_index/OPEN-QUESTIONS.md` LOOT row | agrees | route census `check_route_counts.py` / `globals_index.py` — the single E8 edge is enumerable |
| `14-Story-Event-Quest-Hunt/persistent-flag-banks.md` | `0020E600`'s flag-store scope corrected to "at image load" (the `01F83530` base is zero then); UQ-139 tick verified | `_index/OPEN-QUESTIONS.md` UQ-139 / PROPOSED-repos2d-4 cell | agrees — same wording mirrored there | `check_address_index.py` accessor census; `00290410` reader flagged to owner in PROGRAM-STATE |

## Notes

- The two shop files also carry **FABLE's own uncommitted OPUS-block-324 hunks** (the source of
  the 12→11 correction) — they ride this publish whole-file because the files are mixed and the
  guard's alternatives (splice) would strand a coherent correction across two commits. Disclosed
  in the commit message.
- `the-world-tick-and-the-field-frame.md` carries one uncommitted FABLE 2026-09-26 EX-6 hunk
  alongside mine — disclosed in the commit message.
- The glyph page edits add no struck-marker corrections except the superseded `0209C700`
  authored-table reading, whose correction is documented inline with its replacement; consumers
  are the same page's downstream sections (already reworded) and the re-landed AUDIT-LOG /
  PROGRAM-STATE entries.
