# RC-21: the script-verb reach census regenerated, with its tie-break stated (ORACLE, 2026-09-30)

## The question

RC-21 (registered 2026-09-30 by SWE2-CONTRACT from section 8 of
`01-Script-VM-Native-Bridge/Verb-Dispatch/what-each-script-verb-touches.md`) asks for three things:
- the depth-1, depth-2 and depth-3 per-subsystem counts at the current certified snapshot;
- the counting rule and tie-break stated;
- the GN160 table kept beside them as history.

Its premise: five of the fourteen depth-1 rows drift at the current snapshot (ActorEntity, Party, WorldAreaField,
Resource, Rewards).

## Method

- [`rc21_reach.py`](rc21_reach.py), output [`rc21_reach.out`](rc21_reach.out), per-verb labels
  [`rc21_reach.tsv`](rc21_reach.tsv). The script re-implements the page's own generator,
  `Database/Tools/analysis-kit/gfz-scripts/census_verb_reach.py`, rule for rule:
  - the owner is the `GFZ.V120.PrimaryOwner` tag, else the first `FFXII.` tag;
  - edges are the non-external rows of `edges.tsv`;
  - the seeds are the `begin`/`poll`/`result` columns of `scriptvm-verb-table.tsv`;
  - the walk is breadth-first; each newly seen callee counts once for its non-bridge owner, and bridge callees are
    walked through;
  - the label is the owner with the most hits.
- The generator's one nondeterminism is removed and measured separately (below).
- [`rc21_draws.py`](rc21_draws.py), output [`rc21_draws.out`](rc21_draws.out), runs the generator's logic verbatim
  under `PYTHONHASHSEED` 0 to 99.
- Snapshots:
  - `cur` is the current census on the certified GN162 parent: `Tools/work/graph/functions.tsv`, sha256
    `c0e1de8f650f2e8d...`, and `edges.tsv` `de21ba1bc62d9224...`.
  - `old` is the 2026-09-03 export `functions_live.tsv` (`cfe9c6b03900e5c7...`) with `edges_live.tsv`, which is
    byte-identical to `edges.tsv`.

Controls, all PASS:

| control | what it checks |
|---|---|
| C1 | 1,960 verb rows |
| C2 | the old snapshot reproduces the page's depth totals 616, 851 and 944 exactly |
| C3 | each of the page's fourteen GN160 depth-1 rows lies inside the old snapshot's range (strict wins to strict wins plus ties) |
| C4, C4b | section 2's owner-tag figure (1,857 of 1,888) and pass 1's (1,890 of 1,922) both reproduce, identically, at the old and the current snapshot |
| C5, C5b | one assignment of the tied verbs reproduces all fourteen GN160 rows and the omitted 11 at once (bipartite matching), on both snapshots |
| C6 | negative control for the matcher: an out-of-range target (Movement 179) is rejected |

## Result

**ANSWERED, and the row's premise is corrected.**

**1. The counting rule and the tie-break.**
- **The rule:** one verb, one subsystem, the owner its handlers' callees hit most. This is the rule pass 1 recovered.
- **The generator's tie-break is not a rule, it is hash order.** It takes `Counter.most_common(1)` over callees
  iterated from Python `set`s of address strings. Among tied owners, that returns whichever one the set iteration met
  first, which depends on the per-process string-hash seed.
- Across 100 seeds on the current census, the depth-1 partition always totals 616. Nine rows move between draws:
  - Movement 181 to 190;
  - ActorEntity 135 to 154;
  - Party 37 to 52;
  - WorldAreaField 26 to 32;
  - Resource 4 to 9;
  - Rewards 3 to 4;
  - Audio 36 to 37;
  - Spawn 31 to 32;
  - CoreRuntimeScheduling 10 to 12.
- Five rows never move: Presentation, Input, Story, UI and CombatFormula.
- This record breaks ties **alphabetically by owner name**, and publishes each subsystem's full range beside the count.

**2. The five rows do not drift with the snapshot.**
- The old and the current snapshots give **identical** labels for every verb at depths 1, 2 and 3: 0 label changes,
  the same 36 / 89 / 61 tied verbs, and the same ranges.
- The page's five "drifting" values (ActorEntity 142, Party 51, WorldAreaField 29, Resource 6, Rewards 4) are each
  inside their tie range (C3). One tie assignment reproduces all fourteen published rows at once (C5), and every
  published value occurs among the 100 draws.
- So the GN160 table is **one hash-seed draw of the same census**. The drift pass 1 measured is the tie-break, not the
  snapshot.
- The owner-tag "drift" (1,857 of 1,888 then, 1,890 of 1,922 now) is not a snapshot change either. They are two
  definitions:
  - section 2 counts verb rows by `arg_handler`;
  - pass 1 counts rows whose tagged `begin`/`poll`/`result` handlers are all bridge-owned.
- Each definition gives the same value on both snapshots (C4b).

**3. The regenerated census at the current snapshot.** Each cell is the count under the alphabetical tie-break, then
`[strict, strict+ties]`. Labelled verbs: 616 at depth 1, 851 at depth 2, 944 at depth 3. Tied verbs: 36, 89 and 61.

| subsystem | GN160 page, d1 | d1 | d2 | d3 |
|---|---:|---|---|---|
| Movement | 182 | 182 [180,192] | 232 [232,243] | 236 [236,245] |
| ActorEntity | 142 | 162 [130,162] | 262 [209,262] | 284 [253,284] |
| Presentation | 42 | 42 [42,42] | 70 [69,72] | 88 [86,96] |
| Party | 51 | 37 [37,53] | 31 [31,49] | 23 [23,36] |
| Audio | 36 | 36 [36,37] | 50 [50,51] | 57 [56,57] |
| Input | 35 | 35 [35,35] | 41 [39,41] | 43 [43,45] |
| Spawn_Encounter_Lifecycle | 31 | 31 [31,32] | 7 [7,29] | 6 [6,7] |
| WorldAreaField | 29 | 26 [26,32] | 25 [25,41] | 20 [20,35] |
| Story_Event_Quest_Hunt | 21 | 21 [21,21] | 6 [6,25] | 4 [4,12] |
| CoreRuntimeScheduling | 11 | 11 [10,12] | 21 [18,26] | 49 [35,53] |
| UI | 8 | 8 [8,8] | 8 [8,8] | 16 [12,16] |
| CombatFormula | 7 | 7 [7,7] | 8 [7,8] | 9 [8,9] |
| Resource | 6 | 4 [4,11] | 6 [6,10] | 15 [15,20] |
| Rewards_Progression_Economy | 4 | 3 [3,4] | 4 [4,5] | 4 [4,5] |
| CombatAction | (omitted) | 3 [3,3] | 6 [6,6] | 6 [4,6] |
| CombatAI | (omitted) | 2 [2,2] | 2 [2,3] | 2 [2,2] |
| Items_Equipment_Shops_License | (omitted) | 2 [1,2] | 11 [11,11] | 9 [8,12] |
| RNG_Random_Selection | (omitted) | 2 [2,2] | 3 [2,4] | 3 [2,4] |
| PlatformOnlineAchievements | (omitted) | 1 [1,2] | 2 [2,2] | 3 [3,3] |
| Save_Load_Settings | (omitted) | 1 [1,2] | 56 [28,57] | 65 [61,70] |
| Status_Periodic_Terminal | - | 0 | 0 [0,0] | 2 [2,2] |
| total | 605 shown | 616 | 851 | 944 |

The any-subsystem count (a verb counted under every owner it reaches) is in `rc21_reach.out`, column `cur-any`.

**For the page.** The fourteen GN160 numbers are a valid draw and can stay as history. Any claim resting on the gap
between two rows inside a tie range is not supported:
- **ActorEntity against Party.** 15 depth-1 verbs tie between the two: 13 two-way, and 2 three-way with Movement.
  The 36 tie sets are listed by the `d1_cur_ties` column.
- **The depth-2 `Save_Load_Settings` 28.** That figure is its strict-win floor; the alphabetical count is 56.

A stable census has to publish the tie-break it used, or the ranges.

## Not claimed

- That `functions_live.tsv` is byte-identical to the GN160 project's export. It is the 2026-09-03 export, and it
  reproduces the page's totals and its fourteen rows jointly.
- Any verb's semantics. This is a call-graph census, as the page states.
- The in-degree-filtered table of section 2 was not regenerated.
