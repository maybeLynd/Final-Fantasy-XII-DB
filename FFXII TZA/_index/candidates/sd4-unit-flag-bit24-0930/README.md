# SD-4: battle-unit flag bit 24 marks a transition in progress (OPUS, 2026-09-30)

Register row SD-4 was registered by SWE2-DATA (`f7a3292bd`, capability-inhibition-policy.md §7). It asks what battle-unit
flag bit 24 (the `+0` qword, `0x1000000`) means. The capability recompute `0023B040` sets inhibit-mask bit 1 whenever it
is set (`0023B131`–`0023B14F`). The battle-unit field map lists writers but gives no name. This record is static. The
checker is `sd4_bit24.py` (output `sd4_bit24.out`, `FAILS 0`). It scans every catalogued function for sets and clears of
the bit, **including wide AND masks and `movabs` masks**: the shape SWE2-AUDIT-SEM's BIT46 review
(`auditsem-review-bit46-0930`) showed a single-bit search misses.

## The answer (OPUS)

**Bit 24 is set when a unit starts one of five transitions, and cleared when that transition ends or is cancelled.
While it is set, the unit's capabilities are inhibited.** The companion bits that travel with it name the transition.

| event | writer | bits set with 24 |
|---|---|---|
| enter the party combat stance | `BattleUnit_EnterPartyCombatStance` `00313400` (`00313469`) | 50 (T1) |
| leave the party combat stance | `BattleUnit_ExitPartyCombatStance` `00313480` (`003134EB`) | 51 (T2) |
| a combat navigation step | `00313500` (from `BattleUnit_UpdateCombatNavigationStep` `00325BB0`), at `00313537` | 25 and 8 at `00313531` (T3) |
| being processed as an action's target | `Battle_ProcessActionTarget` `00307300` (`00307A97`) | none (T4) |
| revival from a terminal status | `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` (`003012A1`) | none (T4) |

| end | writer | bits cleared with 24 |
|---|---|---|
| the reaction-animation event | `BattleUnit_HandleReactionAnimationEvent` `003250F0`: `0032517C` directly, or `003083A0` via `00325175` | 25, through `003083A0` (T5) |
| stance transitions | `00307C70` (`00307CA2` / `00307CD7`) | 50 or 51 (T6) |
| action cancel | `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031066F`) | 50 and 51 (T6) |
| slot release / allocation | the battle-unit memsets named in the BIT46 review (`002342CE` / `002344D2`) | the whole word |

- **Reader (R1):** the capability recompute tests the bit and inhibits (mask bit 1) while it is set.
- **Reading (an interpretation, not claimed as the bit's name):** "transition animation in progress". The unit cannot
  take new actions until the transition's reaction-animation event arrives or the action is cancelled.

**Correction for the field map (`the-battle-unit-field-map.md`, flag table row 24):** its writer lists are
incomplete. It names two setters and two clearers. The scan finds the five setters and the clear sites above, plus
`00227680` below.

## Limits (OPUS)

- **`00227680`** sets and clears bit 24 on several objects (`002276D1` / `002276D8` / `0022777C` / `00227ABD`; clears at
  `00227775` / `00227C28` / `00227CA7`). The objects are not identified here: they look like a transfer between two
  units, but that is not shown. `00760700` (`00761499`) and `002D8050` (`002D80DF`, a 6-bit field mask) are not shown to
  address a battle unit.
- **Scope of the scan.** It covers the `or` / `and` / `bts` / `btr` shapes on `[reg]`. A clear by whole-word store
  (`mov [unit], reg`) or a memset other than the named ones is not listed.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The row and the field map belong to their
owners.
