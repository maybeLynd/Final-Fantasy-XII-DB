# Consumer check: 05-Spawn contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-05-VALUES-1002. Cloud wave 2 mapped `05-Spawn-Encounter-Lifecycle/` from a text snapshot
(session `session_01NcTcvS8gdiEyacPvQXf8eR`; report `cloud-reports/re-readiness/05-spawn.md` in
maybeLynd/Final-Fantasy-XII-DB, 899678f8; rated NOT YET). The session could not see the executable, so all 18 of its
value-changing contradictions were page-text only.

OPUS decided A1, A2, A3 and A6 at the shipping image. A local read-only pass decided the rest, A4 to A18 and the B
counts that change a number. The bytes overturn several of the sides the map's dated corrections favoured:
- `0208E6A0` is the battle-unit count (32, `002368FE`), not a bank flag.
- `0208D45C` is a frame counter (`0032A135`), not a 30 Hz tick.
- The selector compares the cooldown natively (`002358D1`-`002358D7`), with `>=`.
- The deferred completion has a static route (slot 0xC, `0041DC9E`, `003251A4`).
- The ledger has 64 entries (`00307090`).
- The eligibility flag is `00234DA0`'s fifth argument (`00234DC3`).
- The handler-0xC call sites are `0041DC9E` / `0041DD1D` / `0041CEE3`. The cited addresses were the slot loads.

OPUS re-checked the deciding instructions (`spawn_check.py`).

The pass drafted 65 strike edits (`apply_05spawn.py`). OPUS applies the 16 on its own lines (`apply_by_owner.py OPUS`).
The rest go to their owners as requests:
- 24 to FABLE;
- 18 to SWE2-FRONTIER, on the keep-entry field map, placement-and-retirement, and FRONTIER's `00307140` line;
- 7 to SWE2-EC7, on the height page.

- **Affected:** 05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md, 05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md, 05-Spawn-Encounter-Lifecycle/README.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the group-completion and spawn-placement contracts (OPUS lines) and the README | revised-here |
  | `Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` and `why-the-enemies-you-killed-come-back.md` (FABLE-led) | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 24 edits) |
  | `Spawn-Record/the-spawn-keep-entry-field-map.md`, `spawn-placement-and-retirement.md`, and FRONTIER's `00307140` line on the group contract | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER`, 18 edits) |
  | `spawn-placement-height-and-authored-tunables.md` | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 7 edits) |
  | the member table behind B3 (six functions on the page, fewer in the TSV) | routed-to-SWE2-DATA (regenerate, no strike) |
  | RE repo `docs/readiness/05-spawn.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-spawn-readiness-fixes-1002/spawn_check.py, verified at 3c1948afc: 32 instructions decode as cited, FAILS 0 ([`spawn_check.out`](spawn_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (16), FAILS 0.
