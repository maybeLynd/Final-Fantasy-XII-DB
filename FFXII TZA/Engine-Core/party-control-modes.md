---
title: "Party control modes: the summon, chocobo, town and event-party levels and who may set them"
kind: "system"
category: "Engine core"
addresses: "0030D9A0, 00377C20, 00377C70, 003148F0, 003135C0, 00303EC0, 003072C0, 00307280, 003135E0, 00313550, 0035C620, 00303EE0, 00303D90, 003072E0, 00307240, 003072A0, 00307200, 0034E1F0, 0034FE80, 0050FFB0, 00355C40, 00356A30, 00347230, 00347820, 003514D0, 00355910, 00356630, 00351B40, 00355FE0, 00356DF0, 00351E50, 00356370, 003573A0, 0037C8F0, 0037C860, 003CA2E0, 0037C870, 0037C900, 0037C890, 0037C8B0, 0037CFF0, 0037CFC0, 0037D100, 0037D110, 0037D120, 00306760, 00328BD0, 00313840, 00584210, 00304680, 0035CA70, 0030D8B0, 002EA8E0, 002EA8B0, 003E7CC0, 003E7C70, 00313600, 00313730, 00313650, 00304180, 00304400, 00304060, 00304140, 0016D6A0, 00233AA0, 00233CF0, 0025D9E0, 0037C730, 0026CE60, 0037C980, 0037CA00, 0037CA80, 00326500, 003266C0, 00327850, 00327200, 003594B0, 00234590, 00300FC0, 0023B040, 00253C70, 00309A90, 00303CC0, 00303F00, 00304440, 00313590, 002EF3C0, 002EF410, 003139D0, 00304790, 003047C0, 0030DA10, 00237DF0, 003EBC50, 003EBD00, 002E73C0, 002EB030, 00314D40, 003139C0, 003138D0"
---

## What the player sees

An Esper on the field, a chocobo under the party, a town, and a cutscene that has taken the party
over are four states the game keeps apart with one number. While an Esper is out, the summoner is
the character the game follows and the Esper holds the fourth place in the party selection. On a
chocobo the rider steers the mount and the other members leave the field. In a town the party is
never out of play from KO, Stone or X-Zone, and the town's own leader row is followed. During an
event the script owns the party: the gambits, the battle menu and the controls stop answering.

The four states rank. A script's event claim beats the town, the town beats a chocobo ride, and a
ride beats a summon, so riding into a town keeps the chocobo under the party while every rule that
asks "is the party riding?" answers no, and a summon that is still running when an event starts
waits in the background until the event's claim is withdrawn.

## How it works

### The level

`0030D9A0()` reads the dword at `[02EBF190] + 0x5B04` and returns the first match: bit 3 gives 5,
bit 2 gives 4, the town flag `00377C20()` gives 3, bit 1 gives 2, and otherwise bit 0 gives 1 or 0;
the word is reloaded after the town call. Only bits 0 to 3 are consulted. The town flag is
authored data ([area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)): `00377C20` takes
the area index `003148F0()`, checks it against the count at `[02ADD100] + 4` and returns bit 15 of
the 16-bit word at `+8 + 3 × index`.

| Level | Condition | Meaning | Set by |
|---|---|---|---|
| 5 | bit 3 | the second event-party claim | `seteventparty2mode` |
| 4 | bit 2 | the event-party claim | `seteventpartymode` |
| 3 | the area's town flag | a town | authored data |
| 2 | bit 1 | a chocobo ride | `ridechocobo`, `setchocobomode`, the mount stage of a special sequence |
| 1 | bit 0 | a summon | `summonread`, `btlAtelSetSummonMode`, the summon stage |
| 0 | none | | |

Four predicates compare the level: `003135C0` (= 1, thunk `0037C8F0`), `00303EC0` (= 2, thunks
`0037C860` and `003CA2E0`), `003072C0` (= 4) and `00307280` (= 5).

### The four bits and their setters

| Bit | Getter | Setter | What the setter does when the bit changes |
|---|---|---|---|
| 0 | `003135E0` (thunk `0037C900`) | `00313550(on)` | writes the bit, then `0035C620` (`00273E30` on `022CA408`, the width cache) |
| 1 | `00303EE0` (thunk `0037C870`) | `00303D90(on)` | on: the bit, `+0x5AE0 \|= 0xC` (three turbo charges), `+0x5AE4` = 180.0 (the ride time). Off: the bit cleared, the roster entry-3 actor's render record gets presentation request 3 (`002E73C0`), `+0x5AEC` = 0, and when `+0x5AE0` bit 1 (the turbo) was on, event `0x2001` to that actor (`002EB030`) and that bit cleared (a toggle guarded on the bit being set, so it never sets it) |
| 2 | `003072E0` (thunk `0037C8B0`) | `00307240(on)` | the bit only |
| 3 | `003072A0` (thunk `0037C890`) | `00307200(on)` | the bit only |

Every setter writes nothing when the bit already equals its argument. Who calls them:

- bit 0 on: `summonread` (`0034E1F0`: `00313550(1)`, `00314D40(1)` sets `022C253D`, then the task
  installer `0037CA80`); `btlAtelSetSummonMode` (`0050FFB0`: pops the Esper's row into `+0x5AD4`
  through `003139C0`, then pops the on/off argument; the script's first argument is the one popped
  last); the summon stage of the special sequence
  `00306760` ([quickenings and summons](../Battle-Actions/quickenings-and-summons.md)).
- bit 0 off: `summontopartyread` (`0034FE80`: `00313550(0)`, `00314D40(1)`, `0037CA00`); the
  sequence's end; the party-row clear `00328BD0(row)` when the row is the summoner's `+0x5AD5`
  (after `003138D0(1)`); the reset `00313840`; the save handover `00584210` on both of its sides.
- bit 1: `ridechocobo` (`00347230` → `0037CFF0` → `00303D90(1)`), `getoffchocobo` (`00347820` →
  `0037CFC0` → `00303D90(0)`), `setchocobomode(arg)` (`003514D0` → `0037D100`), the mount stage of
  the special sequence, the dismount `00304680` (which calls `00303D90(0)` first), and state 1 of
  the task `0035CA70` ([chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md)).
- bits 2 and 3: only the verbs `seteventpartymode` (`00351B40` → `0037D120` → `00307240`) and
  `seteventparty2mode` (`00351E50` → `0037D110` → `00307200`); no engine path sets them.
- the restore `002EF410` writes the whole word (below).

### The verbs

| Id | Verb | Handler | Does |
|---|---|---|---|
| `0x0203` | `summonread` | `0034E1F0` | bit 0 on, `022C253D` = 1, installs the summon task |
| `0x0207` | `summontopartyread` | `0034FE80` | bit 0 off, `022C253D` = 1, installs the task with step -1 |
| `0x3044` | `btlAtelSetSummonMode` | `0050FFB0` | bit 0 = the first argument, `+0x5AD4` = the second (the handler pops the last argument first) |
| `0x0408` | `getsummonmode` | `00355C40` → `0037C8F0` | level = 1 |
| `0x0512` | `getsummonmodebit` | `00356A30` → `0037C900` | bit 0 |
| `0x037E` | `ridechocobo` | `00347230` | bit 1 on |
| `0x037F` | `getoffchocobo` | `00347820` | bit 1 off |
| `0x03EC` | `setchocobomode` | `003514D0` | bit 1 = the argument |
| `0x0407` | `getchocobomode` | `00355910` → `0037C860` | level = 2 |
| `0x0511` | `getchocobomodebit` | `00356630` → `0037C870` | bit 1 |
| `0x050F` | `seteventpartymode` | `00351B40` | bit 2 = the argument |
| `0x0510` | `geteventpartymode` | `00355FE0` → `003072C0` | level = 4 |
| `0x0513` | `geteventpartymodebit` | `00356DF0` → `0037C8B0` | bit 2 |
| `0x0514` | `seteventparty2mode` | `00351E50` | bit 3 = the argument |
| `0x0515` | `geteventparty2mode` | `00356370` → `00307280` | level = 5 |
| `0x0516` | `geteventparty2modebit` | `003573A0` → `0037C890` | bit 3 |

The `…mode` getters return the level comparison and the `…bit` getters the raw bit: in a town or
under an event claim `getchocobomode` is 0 while `getchocobomodebit` is still 1.

### The transition dispatcher

`0030D8B0(commit)` reads the level, the previous level at `+0x5B08` and the town flag. It writes
the flag as bit 2 of the two source bytes `0215FD44` and `0215FD45` (`002EA8E0(2, town)` and
`002EA8B0(2, town)`): any set bit in a byte sets `02B59D70` or `02B59D71`, and the second byte's
value also runs `003ACA80`, `003AC8F0(0)` and `003E0B40(1)` when non-zero, else `003ACA90(0x20)`,
`003AC8F0(1)` and `003E0B40(0)`.

Then it indexes the table `01EECFC0`, five rows of four pointers: column 0
enters or stays without commit, column 1 leaves without commit, column 2 enters or stays with
commit, column 3 leaves with commit. Same level: that level's enter column. Changed: the old
level's leave column, then the new level's enter column, and with commit `+0x5B08` = the new
level. Level 5 has no row: nothing runs for it, though the level it replaces still gets its leave.

| Row | enter, no commit | leave, no commit | enter, commit | leave, commit |
|---|---|---|---|---|
| 0 | | | | |
| 1 summon | `0016D6A0` (return stub) | `00313730` | `00313600` | `00313650` |
| 2 chocobo | `00304180` | `00304400` | `00304060` | `00304140` |
| 3 town | `0016D6A0` | `0016D6A0` | `0016D6A0` | `0016D6A0` |
| 4 | | | | |

The handlers:

- `00313600`: countdown channel 2 = max(2.0, `+0x5AD8`) (`003EBC50(2, t)`, `003EBD00(2)`) and
  `+0x5AD0` bit 1 set: the summon timer runs.
- `00313730`: `+0x5AD0` bit 1 cleared, then the focus row = the summoner's `+0x5AD5` through
  `00327850`, which rebuilds the focus with `00326500`.
- `00313650`: with bit 0 already clear, the reset `00313840` (`+0x5AD5` = 0, `+0x5AD4` = `0x1B`,
  `+0x5AD0` bits 0 and 1 cleared, `+0x5AD8` and `+0x5ADC` = 0); with bit 0 set, nothing.
- `00304180`: collects up to nine main members (row type below 7, byte `+5` zero, status words
  clear of `0x80000003` or a town) into `022C1740` and makes the first the focus row; then, once
  per ride (unit flag bit 26), snaps the mount's position and heading to the rider's (`00265020`,
  `0026B0C0`, `00392170`, `0026A0D0`, `0026B620`); `0035C900(1)` sets `022C83E8` bit 3.
- `00304060`: attaches the rider (the selector entry of `+0x5AA4`, `00327200`) to the slot-3 unit
  (`002E28C0`, `002ECF10(rider, 1)`), `0025A160` of `0031B950(3)`, channel 1 = max(2.0,
  `+0x5AE4`), channel 2 = `+0x5AE8`, `00303F00(turbo bit)`, `+0x5AE0` bit 0 set.
- `00304400`: `+0x5AE0` bit 0 cleared, `022C1F48 &= 0xF9`, `022C1F40` = 0, the rider detached
  (`002E6B10`).
- `00304140`: `0025A160` of the rider's selector entry; when bit 1 is already clear, the dismount
  `00304680` and `0035C770(0)`.

Two wrappers call the dispatcher. `00233AA0` (`0030D8B0(1)`, `00326500`, `00311E10(0)`,
`00311E20`) runs from the actor drive pass `0025D9E0` ([frame update
order](frame-update-order.md)) when the slot's byte `+0x200` has bit 1, all four roster entries are
empty or have finished their pass (byte `+0x10` clear) and the manager's `+0x28` is 0, and from
state 3 of the summon task `0037C730` once `0037CB50()` succeeds.

`00233CF0` (`0030D8B0(0)`,
`003266C0`, `00311E10(1)`) runs from the manager runtime init `0026CE60` and from the task
installers `0037C980`, `0037CA00` and `0037CA80`, which place the task `0037C730` at `02EBF400`
with its entry `02EBF3FE` = 0 or 3 and its step `02EBF3FD` = 1 or -1.

### What the level changes

`0030D9A0` has 21 direct callers; the level-2 predicate has 6 direct callers and 16 through its
thunks; the level-1 predicate has 7 direct and 9 through its thunk. The ones read for this page:

- the focus row `00326500` (the commit wrapper and `00327850`): at levels 0 and 1 the saved leader
  `+0x5AA4`, at level 2 row `0x1A` (the chocobo), at level 3 the town's row `00377C70()` (bits 4
  to 6 of the area record's third byte), and at levels 4 and 5 the row `0xFF`, which no unit has.
  - When that row has no unit with a record it falls back to the first selection entry with one,
    then to `003589B0` of roster entry 0, so under an event claim the focus is the first selected
    unit; at level 1 it also runs `00317400(unit)`; the result goes out through `003594B0`
    (`022C7FE4`, `022C7FF8` = 1).
- the selection maps `003266C0` (the no-commit wrapper): the selector `+0x5A48` (nine 2-byte
  entries) is copied whole to `+0x5A5A` and `+0x5A7E`; entries 4 to 8 of the first copy are then
  set to -1 and it is copied again to `+0x5A6C` and `+0x5A90`. The per-level loops touch entries
  0 to 3 only, and `+0x5A7E` keeps the full selector.
  - level 1: only the summoner's entry (`00313800`) and entry 3 (the Esper's row `+0x5AD4`)
    survive in the three maps;
  - level 2: entry 3 becomes row `0x1A` in the first and third maps and -1 in the second; the
    other entries are -1 except the rider's in the second map and entries 0 to 2 of the third;
  - level 3: the third map is first restored to its contents from before the rebuild, the town's
    row is looked up in it (entry 3 when the row is `0xFF` or absent), and only that entry survives
    in the first two maps;
  - level 4: only the leader's entry survives, with the town's row standing in under the flag;
    level 5 does the same after restoring the third map and rewrites only the first two;
  - each changed entry goes through `0023A570`, then `00326500` runs and the active count
    `022C2670` is recounted.
- the field frame orchestrator `00234590` sets battle-state bit 11 at level 1 unless the summoner's
  unit is in play; the unit teardown `00300FC0` at level 1 runs `003138D0(0)` and the lock
  evaluator when the torn-down unit is the summoner's ([frame update order](frame-update-order.md)).
- the lock evaluator `0023B040` tests level 2, and at level 1 tests the summoner's unit
  (`0031B770(003137F0())`: no record, or status words holding `0x80000003` without the town flag,
  raises every lock bit); the input arbiter `00253C70` tests level 2.
- `00309A90`: 24.0 while the party is fighting (`00253B90()` = 0, [force fight
  mode](force-fight-mode.md)), else 3.8 at level 1 and 2.2 at any other level while fleeing.
- `00303CC0`: at level 2 only, the distance test `00336390` between the mount and the rider.
- `00303F00` grants a turbo at level 2 only, spending one of the two charge bits, or refilling them
  to 3 while `0017D3A0()` holds.
- the ride's frame step `00304440` refreshes `+0x5AE4` from channel 1 (`003EBA90(1)`, or 180.0
  while `0017D380()` holds) and `+0x5AE8` from channel 2, then ends the ride (`00311E20`,
  `0035CFA0(1)`) only when `00303CC0()` passes, channel 1 has expired (`003EBB70(1)`), `0017D380()`
  is 0, the level is 2 and `0031B8C0(3)` is non-null.
- `00313590`: at level 1, `0031E860(3)`.

### Carried across an area change, restored and reset

`002EF3C0(rec)` captures `021B28E4` at `rec+4`, the ride block `+0x5AE0..+0x5AEF` at `rec+8`, the
summon block `+0x5AD0..+0x5ADF` at `rec+0x18` and the mode word at `rec+0x28`. `002EF410(rec)`
restores the ride block and the word unconditionally; the summon block only when `rec+0x18` has
bit 1 (the summon timer was running), restarting channel 2 from `rec+0x20` (`003139D0`); and when
`rec+8` has bit 0 (the ride timers were armed) it restarts channel 1 from `rec+0xC` (`00304790`)
and channel 2 from `rec+0x10` (`003047C0`), then sets bit 1 and clears bit 0 of the word.
`+0x5B08` is not captured.

`0030DA10` zeroes the word and `+0x5B08`; its only caller is the battle-storage reset `00237DF0`,
which also runs `00313840`, the dismount `00304680`, and resets the speed index (`00229ED0(0)`,
[frame update order](frame-update-order.md)). The save handover `00584210` clears bit 0
on both of its sides ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).

## Layouts

```python
[02EBF190] + 0x5B04  u32  the mode word: bit 0 summon, bit 1 chocobo, bit 2 event party, bit 3 event party 2
[02EBF190] + 0x5B08  u32  the previous level (written by the dispatcher with commit)
[02EBF190] + 0x5AD0  u16  summon flags (bit 1 the timer runs)   +0x5AD4 u8 the Esper's row (0x1B after reset)   +0x5AD5 u8 the summoner's row
[02EBF190] + 0x5AD8 / +0x5ADC  f32  the summon timers
[02EBF190] + 0x5AE0  u32  ride flags (bit 0 timers armed, bit 1 turbo on, bits 2-3 charges)   +0x5AE4 f32 ride time   +0x5AE8 f32 turbo time   +0x5AEC u32 last turbo argument
[02EBF190] + 0x5A48  nine 2-byte selector entries   +0x5AA4 u8 the saved leader
[02EBF190] + 0x5A5A / +0x5A6C / +0x5A90  nine 2-byte entries each, the selection maps (entries 0-3 rebuilt by level)   +0x5A7E  the selector's full copy
01EECFC0  ptr[5][4]  the transition table: rows = levels 0-4; columns = enter, leave, enter with commit, leave with commit
[02ADD100]  the area record table: +4 count, +8 rows of 3 bytes; word bit 15 = town, byte +2 bits 4-6 = the town's row
0215FD44 / 0215FD45  u8  source bytes; bit 2 = the town flag (the dispatcher), bit 0 the world-lock apply
02B59D70 / 02B59D71  u8  "any bit set" of the two source bytes
transition record: +4 021B28E4, +8 the ride block (16 bytes), +0x18 the summon block (16 bytes), +0x28 the mode word
```

## Shipped data

| Fact | Value |
|---|---|
| the transition table | row 1 `0016D6A0`, `00313730`, `00313600`, `00313650`; row 2 `00304180`, `00304400`, `00304060`, `00304140`; row 3 `0016D6A0` four times; rows 0 and 4 null |
| the ride time | 180.0 (`0x43340000`) |
| the Esper row after reset | `0x1B` |
| the chocobo's row | `0x1A` |
| timer restart floor | 2.0 on channels 1 and 2 |
| `00309A90` | 24.0, 3.8, 2.2 |

## Operations

Per simulation step: the drive pass's commit run when the roster is settled; the orchestrator's
level-1 test; the ride's frame step. Per verb: one bit written and, for the summon verbs, the
no-commit run through the task installer. Per area change: the capture, the restore, and the
first dispatcher run after it.

## State

The mode word and the previous level; the summon block; the ride block; the selector, the saved
leader and the three selection maps; the two source bytes.

## Modding notes

- An area's town flag outranks a chocobo ride and a summon without any code change: every
  level-2 and level-1 reader stops matching, while the two event claims still win.
- The two event claims come only from scripts; a script that sets one and never clears it leaves
  the party in an event configuration across area changes, because the word is in the transition
  record.
- Level 5 has no row in the table: the level it replaces still runs its leave handler, but entering
  or leaving 5 itself runs nothing.
- The `…bit` verbs read the word and the `…mode` verbs the level; a script that needs to know
  whether the party is physically mounted inside a town must use the bit.
- A saved ride forces the chocobo bit on and the summon bit off when restored; a saved summon
  survives only through the word itself and loses its bit at the save handover.

## Related

- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md): the town flag and the town's row.
- [Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md): the ride timers, the
  turbo and the dismount task.
- [Quickenings and summons](../Battle-Actions/quickenings-and-summons.md): the special sequence
  that sets the summon and mount bits.
- [Frame update order](frame-update-order.md): the drive pass and the orchestrator that run the
  dispatcher and test the level.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the transition record.
