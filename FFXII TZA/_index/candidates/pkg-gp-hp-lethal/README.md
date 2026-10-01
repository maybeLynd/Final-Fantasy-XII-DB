# PKG-GP-HP-LETHAL: first corrections (FABLE, Claude Opus 5.5, 2026-09-28)

affected: `08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md` (l.186, l.199–201, §8 key-address row `00469BB0`),
`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` (the `00312280` loot step, "`00317090` closes the record").

The package is [`PKG-GP-HP-LETHAL`](../../completion-packages/PKG-GP-HP-LETHAL.md). This record carries its items G1, G2, G3,
G7 and G8. [`hp_lethal_checks.py`](hp_lethal_checks.py) ([output](hp_lethal_checks.out)) runs S E R K, FAILS 0, static.

- **G1 (S): two HP stores on the lethal path.** The page's "only write of current HP on this path" predates OPUS's 2026-09-25
  contract correction. The status transition `0030E360` calls the stat recompute `0030FED0` (`0030E828`), which stores
  `[unit+0x48]` again at `00310508` against a cap it recomputes. EXP-148 executed that store, and EXP-093 reached it. The page
  now says "the only store in `00300530`'s own instructions" and adds the second store.
- **G2 (E):** the key-address row "What `00469BB0` is – not established – UNKNOWN" now carries EY-3's 2026-09-13 answer: it
  posts event `0x10` ("… has fallen.") through `0046AB10`.
- **G3:** "all but two shipped callers" and "for the other two" now read "23 calls in 14 shipped scripts", which is the page's
  own 2026-09-13 census in §2.3. This is a consistency fix inside the page, and the census record is the evidence.
- **G7 (K), dispositioned.** No status in the 32-status word revives on KO (`the-thirty-two-statuses.md`), so revival is
  only by action (Raise, Arise, Phoenix Down, Renew). The variant is absent by the table, not by an empty grep.
- **G8 (R): nothing in `00312280` retires the unit.** After the drop spawn (`003125B4`) its only calls are `00317090`
  (`003125BC`) and the stack-cookie check. `00317090` adds the reward rows' word `+0`, times the level span, to
  **achievement counter `0x11`** through `00253770` → `00316A50` (`AchievementCounter_UpdateAndMaybeFire`).
  - The field map's "closes the record" is corrected.
  - The rewards prose page's step 6, "Retire the unit", is an overlay carrier, so it is routed to FRONTIER rather than
    edited here.
  - What achievement `0x11` counts is not established.
  - Body removal is spawn-lifecycle work and stays an adjacent obligation.

| consumer | action | agreement |
|---|---|---|
| HP page l.186 | struck and qualified (G1) | revised-here |
| HP page l.199–201 | struck and corrected (G3) | revised-here |
| HP page §8 row `00469BB0` | struck and answered (G2) | revised-here |
| battle-unit field map, loot step | struck and corrected (G8) | revised-here |
| `how-a-battle-unit-is-built-from-its-definition.md` ("word `+0` into game counter `0x11`") | already right | agrees |
| `13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md` step 6 "Retire the unit" (overlay carrier) | not edited | routed-to-FABLE-REQ-FRONTIER-HP-LETHAL-REWARDS-STEP6 |
| `CONTRACT-hp-write-and-lethal-transition.md` §4 (the second store) | already right | agrees |
| the same contract l.380 "Monster-band" (G4), the `00312280` label pair (G5), `crossref_clean: false` (G6) | OPUS-owned | routed-to-FABLE-REQ-OPUS-HP-LETHAL-CONTRACT-ITEMS |

Regression: hp_lethal_checks.py S E R K. S fails if `0030E828` stops calling `0030FED0` or `00310508` stops storing `+0x48`. R fails
if anything but `00317090` and the cookie check follows the drop spawn. run: hp_lethal_checks.py at adf88cdb9, FAILS 0.
