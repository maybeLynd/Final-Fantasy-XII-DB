# PKG-GP-EXP-LEVEL-UP: from a kill's experience to a character's new level (FABLE, Claude Opus 5.5, 2026-09-29)

**behavior.** When an enemy dies, each eligible party member's accumulated experience grows by that member's share of the enemy's experience. The character then climbs as many levels as the new total reaches on the experience curve. Each level gained applies that level's growth to HP, MP and four float stats. After the last level, derived state is rebuilt once and one fanfare plays, if the record has an owner.

This is the progression every player sees after every battle. A reimplementation with the wrong curve, share rule, growth cadence or caps is wrong on the first kill.

**reproduction target.** From the accepted package alone, a developer can predict, for a character with a known level and experience and a kill of known experience:
- the experience added and the cap it respects;
- how many levels are gained, with the threshold for each;
- which fields grow, how many times each grows, and which parts run only once;
- what happens at level 99 and at the experience cap.

**scope: included.**
- the share: `CONTRACT-experience-and-licence-award.md` (recipients, the four-slot division, the designated mode, the doubling);
- the add and its cap: `CONTRACT-defeat-rewards-sequence.md` DR-3 (`+0x18C`, capped at 99,999,999);
- the curve: `002F8F20`, stated on `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` §4, **corrected 2026-09-29** (item E1);
- the threshold walk: DR-3 (a search, not an increment; −1 above level 98 stops it);
- the level advance and growth: `CONTRACT-level-advance-and-growth.md` (LU-1..LU-8: three guards on 99; monotonic; growth every level, rebuild and fanfare once).

**scope: adjacent obligations** (open elsewhere; not closed by this package):

| obligation | owner / locator |
|---|---|
| whether a level-0 unit can be alive at kill time (the negative-share path's reachability) | `CONTRACT-experience-and-licence-award.md` §13; RT, ASTRA |
| the division page's REOPENED status (SECTION-03 production review, peer acceptance pending) | `how-experience-is-computed-and-divided.md`; the section overlay's acceptance carrier |
| what the fanfare looks like on screen (the `0x610` / `0x620` element group) | 17-Presentation-Rendering |
| LP and the licence board | `PKG-GP-HP-LETHAL`'s rewards step; the licence-board pages |

**dependencies.** `CONTRACT-experience-and-licence-award.md`, `CONTRACT-defeat-rewards-sequence.md` and `CONTRACT-level-advance-and-growth.md` (all CONTRACT READY); `PKG-GP-HP-LETHAL` supplies the kill.

**owner.** FABLE (Claude Opus 5.5).
**contributors.** OPUS owns the rewards and level-advance contracts and the unit-construction page, and ran EXP-200. ASTRA ran the reward-gate executions (EXP-090).
**reviewers.** SWE2-AUDIT-SEM for the reading and the corrections. FABLE authored E1, so another lane accepts it.

**evidence** (static unless marked).

| stage | canonical locator | class |
|---|---|---|
| share | the EXP contract §4 | static; EXP-090 native execution (104/104) |
| add, cap | DR-3 (`00312432`–`00312444`) | static; OPUS block 344 replay (6/6) |
| curve | unit-construction page §4; `_index/candidates/exp-curve-fable/` | original bytes executed (`curve.py`, 101 inputs); EXP-200 agrees |
| walk | DR-3 (`0031244A`–`00312473`) | static |
| advance, growth | `CONTRACT-level-advance-and-growth.md` | static |

**canonical destination.** The pages and contracts above. This file keeps only the end-to-end reading order and the items.

**work items.**

| # | item | kind | locator | owner | reviewer | stage |
|---|---|---|---|---|---|---|
| E1 | the curve's linear term: the pages said `k(12k − 2)` and "level 2 is 47"; the bytes give `12k²`, level 2 = 51 | stale-text | unit-construction page §4; unit-display-record page §4 | FABLE | AUDIT-SEM | incorporation: ACCEPT by the page owner OPUS (FABLE-NOTICE-OPUS-EXP-CURVE-CORRECTION, 2026-09-29: independent float32 recomputation gives level 2 = 51, level 99 = 13,741,148). Waiting on FRONTIER's apply of `unitdef-curve.patch` (FABLE-REQ-FRONTIER-APPLY-EXP-CURVE) - earlier stage text kept: evidence-ready (`exp-curve-fable/`, curve.py X B F K): the display page is corrected by FABLE-PUB-EXP-CURVE-FIX-B; the unit-construction page is an overlay carrier, so its hunk is staged as `unitdef-curve.patch` for FRONTIER (FABLE-REQ-FRONTIER-APPLY-EXP-CURVE); owner notice FABLE-NOTICE-OPUS-EXP-CURVE-CORRECTION |
| E2 | the level-up page's "Not claimed: which stats the six fields are": the offsets are answered by the level-advance contract §3 (HP `+0x08`, MP `+0x0C`, four f32 at `+0x10`–`+0x1C`); the names are E4 | stale-text | `what-happens-when-a-character-levels-up.md` l.419–420 | FABLE | AUDIT-SEM | evidence-ready (pointer added 2026-09-29) |
| E4 | name the four f32 base stats: trace `BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`) from its `cvttss2si` reads (`+0x10` `002FF0C2`, `+0x14` `002FF0CD`, `+0x18` `002FF099`, `+0x1C` `002FF0B7`) through the shared accumulator slots to the effective bytes the attack page names (`+0x2A` Strength, `+0x2B` Magick Power, `+0x2C` Vitality, `+0x2D` Speed; the last two named from function names only). The final stores are in callees (`003105D0` / `00307D10`) | gap | the stats field map l.101-107 ("f32 stat 1..4") | FABLE | AUDIT-SEM | evidence-ready (`_index/candidates/exp-level-stats-fable/`, statmap.py R F S K): `+0x10` Strength, `+0x14` Magick Power, `+0x18` Vitality, `+0x1C` Speed - stored in order at `+0x2A`-`+0x2D` by the rebuild, each capped at 99; Vitality and Speed carry the attack page's name-only evidence |
| E3 | fresh-reader sufficiency: predict three cases from the pages (a level-1 character with 0 EXP gaining 200; a four-member split of one kill; a level-98 character crossing into 99 and past the cap) | review | this file | FABLE | AUDIT-SEM | research |

**stage.** `research` (opened 2026-09-29; the earliest item stage, E3). E1 is accepted (OPUS, page owner) and waits on incorporation; E2 and E4 are evidence-ready.

**blocker / next action.** E1's publish lands, then E2's pointer, then ask AUDIT-SEM for E1–E3 in one request.

**acceptance checks.**
1. E1 and E2 are corrected with the old text kept and struck.
2. A non-author predicts the three E3 cases from the pages alone.
3. No adjacent obligation is marked closed.
