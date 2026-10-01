# Consumer-check record: counter 17 (ACH_COUNT_SCORE) is fed natively; AB-8's premise was false (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

## What changed

FABLE's DD helper (batch B, the enemy-death page) found that two bodies feed achievement counter 17. FABLE verified it
([`ab8_counter17.py`](ab8_counter17.py) -> [`.out`](ab8_counter17.out), FAILS 0).

The census behind AB-8 (2026-09-18, and the SUPERSEDED disposition of 2026-09-26) counted only the three DIRECT callers
of the counter updater `00316A50`. It missed the six tail jumps through the 5-byte thunk `00253770` (`jmp 00316A50`).
FABLE read each of the six thunk sites:

| thunk site | counter id | amount |
|---|---|---|
| `00317090` (`003170D3`) | **17** | computed per defeat |
| `002E2380` (`002E2382`) | **17** | the caller's, from the `addclanpoint` verb |
| `0028F0C0` | 18 | the caller's |
| `003112F0` (`00311472`) | 3 | 1 |
| `003171C0` (`003171E4`) | 4 | 1 |
| `00305640` (`00305785`-`003057A0`) | 13, 2, 1 or 0 | 1, or computed for 13 |

- `00317090` is reached once per defeat from `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` (`003125BC`).
- `002E2380` is called only by the handler `003403E0` of script verb `0x4DC` `addclanpoint`.

So the page's "none of them feeds counter 17", "never 17" and "no native body advances counter 17" are struck and
corrected. AB-8's disposition rested on the same premise, so the row gets a dated correction. Its lead word should become
ANSWERED on independent acceptance; FABLE does not self-award that.

## Consumers

- consumer: `20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md` (line ~329, the 2026-09-18
  narrowing): revised-here. Three strikes, and one dated correction that states all six thunk sites.
- consumer: `_index/OPEN-QUESTIONS.md` row AB-8: revised-here, with a dated correction appended.
- consumer: the batch-B enemy-death page (`13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md`): agrees.
  It already reads `00317090` as feeding counter 17, and publishes separately (FABLE-PUB-DD-GAMEPLAY-0930).
- consumer: the live discriminator the page named ("whether a Trial stage clear moves the counter"): withdrawn in the page
  correction, because what moves the counter is static.

## Regression

run: ab8_counter17.py at 4407f8484 (FAILS 0; control: the census's three direct feeders `00254EE0` / `00312280` /
`0056D370` are found, and the thunk is `jmp 00316A50`)
