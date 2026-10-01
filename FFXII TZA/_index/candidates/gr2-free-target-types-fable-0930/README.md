# GR-2 answered: what each free-target type value denotes, by the scripts that set it (FABLE, Claude Opus 5.5, 2026-09-30)

GR-2 asks what each value of the actor's free-target type nibble (`actor[+0x0E] & 0xF`, AL-3) denotes as authored. Its
readers were already mapped on [the kind page](../../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)
section 7:
- the relationship classifier treats 5 as neither friendly nor hostile;
- the cursor helpers accept 1-2, 1-3, 3 and 5;
- the kind classifier maps 3 to 4, and 1, 2 and 7 to 8;
- the time-stop sweep groups {1, 2, 7}, {3} and the rest.

SWE2-AUDIT-SEM's review C3 pointed at SD-160's census. That census decoded every call of the two verbs, but it joined
only value 3 to scripts. This record joins every value.

## Method (FABLE)

[`gr2_join.py`](gr2_join.py) copies the decode loop of OPUS's
[`sd160_census.py`](../sd160-free-target-type3-0930/sd160_census.py) verbatim. It groups every call by the **type value
it produces**:
- `setfreetargettype` stores its argument as is;
- `btlAtelSetUnitType(v)` stores `{1, 5, 3, 4}[v]`, the table at `01E09EE8`. SD-160's record reads it through
  `00510340` -> `002396B0`, and the image's initialised `.data` holds `1, 5, 3, 4` there.

**Control:** the eight (verb, argument) counts must equal `sd160_census.out`'s, or the run refuses. They do: 59,814 /
234 / 297 / 369 and 18 / 315 / 2,340 / 45, over 16,666,842 decoded CALL-family sites. Output:
[`gr2_join.out`](gr2_join.out), and [`gr2-type-scripts.tsv`](gr2-type-scripts.tsv) with every (type, verb, argument,
script, sites) row.

## Result (FABLE)

| type | sites | set by (verb(arg)) | the scripts | reading |
|---:|---:|---|---|---|
| 1 | 59,832 | `btlAtelSetUnitType(0)`; `setfreetargettype(1)` (18, all `BOSS_Dウォール`) | `monster_*` (45,666), `trial*`, `unique_monster_*`, `lot*`, `ex*`, `boss*`, `nm*`, `fh*` | a hostile combatant |
| 3 | 612 | `btlAtelSetUnitType(2)` (297), `setfreetargettype(3)` (315) | `THIRD_*` guests, `DAL_SOLDIER_*`, `npc_battle_*`, `BASH`, `event*` (22 zones); `disp_tama01`-`05` (7 `rbl` zones) | an allied or event combatant |
| 4 | 2,709 | `setfreetargettype(4)` (2,340, 82 zones), `btlAtelSetUnitType(3)` (369, 18 zones) | `system_crystal_actor` (2,187), `system_anchor_actor` (117), treasure and quest objects (たからば, 伝説の剣, 沈黙の壺, 置き手紙, ダルマス); ordinary `monster_*` scripts in 18 zones | an object the player interacts with, or a monster parked as one |
| 5 | 234 | `btlAtelSetUnitType(1)` (5 zones) | `TWN_*`, `SND_*`, `PRISON_*`, `COCKATRICE_A`-`E`, and `BASH` / `DAL_SOLDIER_A` in one scene | a non-combatant in a battle scene |
| 6 | 45 | `setfreetargettype(6)` (3 zones) | `BOSS_Dウォール` (which also sets 1), `STAY_ボス武器`, `STAY_ダイダロス` | a stationary boss part |
| 0, 2, 7 | 0 | none | - | never authored: they come only from the unit refresh, AL-3's other writer |

The "reading" column comes from the script names. It is a naming reading of shipped data, not a code reading. It agrees
with every reader above:
- 5 is the classifier's neutral value;
- 3 is the value the kind classifier and the time-stop sweep single out;
- the kind classifier's enemy group {1, 2, 7} holds the one hostile value scripts set.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`

- consumer: GR-2 - revised-here (ANSWERED).
- consumer: the kind page's status line and the GR-2 box - revised-here (box ticked with the answer).
- consumer: SD-160's record - agrees (its counts are this run's control; not edited).
- consumer: [the record behind every actor](../../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md)
  (the time-stop grouping) - agrees; not edited.

## Controls (FABLE)

run: gr2_join.py at 3cae47364 (control counts equal; output [`gr2_join.out`](gr2_join.out))
