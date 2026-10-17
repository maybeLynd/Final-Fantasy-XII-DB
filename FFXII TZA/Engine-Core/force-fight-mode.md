---
title: "Force fight mode: the flag behind the fleeing state, who sets it and what fleeing changes"
kind: "system"
category: "Engine core"
addresses: "01E0C2B8, 00253B90, 0030C0D0, 00253BA0, 00254EA0, 003444D0, 003BA2E0, 003BA300, 003BA310, 0050C910, 00266D10, 002628B0, 00252C80, 00252B60, 00253C70, 003603B0, 003603C0, 0035C6F0, 0035C880, 00366950, 003669F0, 003667E0, 00366870, 00276650, 00276D30, 002FFCF0, 00307D10, 00308130, 00308610, 00309A90, 0030C010, 0030FA00, 00313A00, 002E1C20, 002E1CA0, 00234590, 00336710, 00339BF0, 0033A720, 0033C310, 0033CEF0, 0033D3E0, 00267E10, 00307FF0"
---

## What the player sees

Hold R2 in the field until the hold arms and the word FLEEING appears on the HUD: the party
stops answering the enemy, combos stop chaining for anyone who is not Confused or Berserk, and
most battle commands are refused until the party fights again. Hold R2 again and the label is
gone and the party fights. The ordinary state is the fighting one. Area scripts put the party
into the fleeing state at map entry and after a teleport, and the game restores the toggle's own
state a moment later.

## How it works

### The flag and its two readers

`01E0C2B8` is a dword holding 1 in the image, so the game boots in force fight mode. The
predicate `00253B90()` (thunk `0030C0D0`) returns `flag == 0`: true means fleeing. Every gameplay
reader tests it that way round. The second reader `00253BA0()` returns the flag only while the
enable `003BA2E0()` holds and 0 otherwise; its two callers are the battle menu's opener
`00276650` (the `0x61F0` widget) and the menu's message procedure `00276D30`, whose message-2 arm
treats a set `+0x2FF0` bit 14 as the mode being on.

`003BA2E0()` is true when both bytes `02B4053C` and `02B4053D` are non-zero. Both are 0 in the
image; the boot `00266D10` writes 1 to both (`003BA300(1)`, `003BA310(1)`), the manager-0 area
unload `002628B0` writes 1 to the first again, and the verb `debug_setfightstatusbyevent(v)`
(`0x206B`, `0050C910`, one popped argument) writes its argument into the first. No shipped
event script calls that verb, so the enable holds from the first area on.

### The writers

The script verb `setforcefightmode(enable)` (`0x0334`, `003444D0`) calls `00254EA0(enable)`:
with `enable` non-zero and `003BA2E0()` true the flag becomes 1 and the call returns 1; otherwise
the flag becomes 0 and the call returns 0. So a script can always force the party to flee, and
can force it to fight only while the enable holds.

The R2 toggle reaches the flag through `00252C80(state, force)`, called only by `00252B60`,
called only by the input arbiter `00253C70` (the wrapper `00253C50` of [frame update
order](frame-update-order.md)) with `force` = 0, on every pass that reaches the arbiter's tail:

- with `force` clear the write is refused while either skip predicate `003603B0()` (`022CB728`)
  or `003603C0()` (`022CB726`) holds; `022CB728` is never set in this build (its one writer
  `00360370` stores 0), and `022CB726` is set by the title-return reset `003601D0` and cleared at
  the next area start (`00360110`), so the refusal lasts from a title return to the next area;
- `state` = 0 (the toggle disengaged) writes 1, then `003BA2E0()`, so the flag ends as the enable;
  `state` non-zero (engaged, the party fleeing) writes 0;
- a value equal to the one already stored is not rewritten unless `force` is set. So every pass
  re-asserts the toggle's state, and a script's write that disagrees with it lasts only until the
  arbiter's next pass.

The arbiter keeps the toggle in `020927E0`: it flips on each press while `0017DE10()` holds and
the edge byte `020927E4` was clear, is forced to 1 by the device poll path (`00862CF0`, with
`01E0C2B4`), and is cleared when `01E0C2B4` is 1 or the area is a town (the town flag
`00377C20()`, bit 15 of the area's flag word, [area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

`00252B60(state, flag)` re-decides the state before the write:

- it returns at once when the input snapshot `02F97362` has bit 9;
- `002E0FA0()` bit 6 forces the state to 0 with `flag` = 1; else bit 9 does the same and runs
  `00366950`; else bit 10 or `00237260()` (every active party member down) does the same; then
  `020927CC` = 1 does the same;
- the mode register `0035C6F0()` (`022C83EC`): with bits 2 and 3 clear and bit 0 set the state
  is its bit 1; with bit 2 or 3 set the state is the snapshot's bit 9 (`02F97360`, 0 under policy
  bit 10), `0035C880(0xC, (register & 4) × 2)` and, for state 0, `0035C880(0xC, 0)`, then
  `00366950`;
- unless a skip predicate holds, the arming counter runs (`003669F0`, then `003667E0` for state
  0 or `00366870` for state 1), and a non-zero state is replaced by `003669F0()`, bit 2 of
  `022CBE1A`: the flag drops to 0 only once the hold has armed.

The arming counter makes the hold audible. `00366870` starts sound `0x52` (`003A1180`, then
`002DF220`) on its first pass, keeping the handle in `022CBE1C` and bit 4 of `022CBE1A`;
`003667E0` stops that sound if it still plays (`002DEE80`, `002DF0F0`) and, when the hold had
armed (bit 2) and `00265680()` holds with bit 6 clear, plays sound `0x2A` (`00249C60`)
([sound effects](../Sound-And-Music/sound-effects.md)).

### What fleeing changes

The raw predicate has 8 call sites in 7 functions and the thunk 8 sites in 6 functions:

| Reader | What it does while fleeing |
|---|---|
| `002FFCF0` | refuses every command with reason `0x24` for a party-side unit without Confuse or Berserk (status `0x08000020`), except Dismiss (`0x113`) and Dismount (`0x95`) ([command availability](../Battle-Actions/command-availability.md)) |
| `00308610`, `0030C010` | the combat frame skips the combo continuation `0030FA00` for a unit without Confuse or Berserk, and `0030C010` answers "no" to the same question ([combos](../Battle-Actions/combos.md)) |
| `00307D10` | the engagement update: for a unit that is not the chocobo (`0x1A`) and not in a town, with the two statuses clear, it clears `022C1F48` bits 1 and 2, zeroes `022C1F40` and the unit's `+0xDCC`, and clears unit `+4` bits 9, 10 and 16 (bit 16 = engaged); the other arm (fighting, or the chocobo, a town or a status set) runs the bit-9 path through `00307CE0`, `0030BF20` and `0030B050`; it runs when a status is added or removed (`0030E360`, at `0030E7AC`, [status changes](../Status-Effects-And-KO/status-changes.md)) and when the stats block is recomputed (`002FEF30`, [stats](../Damage-And-Battle-Formulas/stats.md)) |
| `00307FF0` | the two global writes alone (`022C1F48 &= 0xF9`, `022C1F40` = 0), run by the area initialisation `002342F0` and by `002348E0`, which first tears down every enemy unit (`00300E40`) |
| `00308130` | "may the unit engage", after running `00307D10`, answers false for a unit with the two statuses clear; otherwise true for unit `+4` bit 16, and false when `022C1F48` bit 0 is clear. With bit 0 set it first arms the clock through `003081E0` (`00308192`): when unit `+0` bit 23 is clear and `+0xDCC` is 0, `+0xDCC = trunc(0032A150() + trunc([01DFE0B8] * 30) * ((00328370() & 3) * 0.25 + 0.5))`, the sum stored as an integer. It then answers true when unit `+0x698` is null or that block's byte `+5` is non-zero (`003081A1`, `003081A9`), and otherwise when the clock `0032A150()` is at or past `+0xDCC` (`003081B2`) |
| `00309A90` | the approach distance is 3.8 at party-control level 1 or 2.2 otherwise, instead of the fighting value 24.0 ([party control modes](party-control-modes.md)) |
| `00313A00` | the capability row writes: the second of its fourteen bits is set (`002E1C20`) instead of cleared (`002E1CA0`) while a unit's action is being shown (`02089350`, [Action phases](../Battle-Actions/action-phases.md)) or the party is fleeing |
| `00234590` | the orchestrator's reset loop runs once each time the predicate changes against the battle-state word's bit 3 ([frame update order](frame-update-order.md)) |
| `00336710`, `00339BF0`, `0033A720`, `0033C310`, `0033CEF0` | battle locomotion: order `0x4022` counts as the engaged order `0x4124` while fleeing; the arrival divisors are 1.5 and 0.25 while fleeing against 3 and 5 while fighting; for a party unit on order `0x4022` the turn class is `0xA0` instead of `0xC0` and the search flag 4 instead of 2, while a fighting party unit on `0x4022` gets speed `+0xFC` outright in `00339BF0` ([battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)) |

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `01E0C2B8` | `u32` | force fight mode: 1 fighting (image value), 0 fleeing |  |
| `02B4053C` | `u8` | enable byte 1: 0 in the image; 1 from the boot, the manager-0 unload and debug_setfightstatusbyevent |  |
| `02B4053D` | `u8` | enable byte 2: 0 in the image; 1 from the boot |  |
| `020927E0` | `u32` | the R2 toggle state (1 = fleeing requested) | `020927E4`  u8  its press edge   `01E0C2B4`  u32  the device-poll override |
| `020927CC` | `u32` | forces the state to 0 when 1 | `022C83EC`  u32  the mode register (`0035C6F0` / `0035C880`) |
| `022CB726` | `/ 022CB728` | the two skip predicates that refuse an unforced write |  |

## Shipped data

| Fact | Value |
|---|---|
| image value of the flag | 1 (fighting) |
| image value of the enable bytes | 0 and 0 |
| verbs | `setforcefightmode` `0x0334`, `debug_setfightstatusbyevent` `0x206B` |
| readers | raw: 8 direct sites, 8 through the thunk; effective: 2 |
| distances and divisors | fighting: 24.0, 3 and 5; fleeing: 3.8 or 2.2, 1.5 and 0.25 |

## Operations

Per frame: the input arbiter reads the pad, re-decides the toggle state and calls the writer. Per
script: `setforcefightmode` writes the flag outright. Per reader: a test of the dword, nothing
cached.

## State

The flag, the two enable bytes, the toggle state and its edge byte, the override cells and the
mode register.

## Modding notes

- The predicate's sense is inverted from its name: a true `00253B90()` means fleeing. A hook that
  fires "during forced fights" on a true result is backwards.
- Scripts and the toggle share one dword, and the arbiter re-asserts the toggle's state on every
  pass: a script's write holds only until then. Every shipped call is `setforcefightmode(0)`, at
  map entry and after a teleport in the area scripts; none passes 1.
- Clearing either enable byte makes `setforcefightmode(1)` and the toggle's disengage both write
  0, so the party can never leave the fleeing state; only the debug verb could clear one, and no
  shipped script calls it.
- The effective reader is UI-only: gameplay never consults the enable, so a flag forced to 1 with
  the enable clear fights on screen while the menu reports fleeing.

## Related

- [Command availability](../Battle-Actions/command-availability.md): reason `0x24`.
- [Combos](../Battle-Actions/combos.md): the continuation gate.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md): the order gate and the
  arrival divisors.
- [Party control modes](party-control-modes.md): the approach distance by level.
- [Frame update order](frame-update-order.md): the input arbiter and the orchestrator's reset loop.
