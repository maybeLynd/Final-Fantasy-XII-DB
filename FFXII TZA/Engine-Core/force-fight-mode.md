---
title: "Force fight mode: the flag behind the fleeing state, who sets it and what fleeing changes"
kind: "system"
category: "Engine core"
addresses: "0x01E0C2B8, 0x00253B90, 0x0030C0D0, 0x00253BA0, 0x00254EA0, 0x003444D0, 0x003BA2E0, 0x003BA300, 0x003BA310, 0x0050C910, 0x00266D10, 0x002628B0, 0x00252C80, 0x00252B60, 0x00253C70, 0x003603B0, 0x003603C0, 0x0035C6F0, 0x0035C880, 0x00366950, 0x003669F0, 0x003667E0, 0x00366870, 0x00276650, 0x00276D30, 0x002FFCF0, 0x00307D10, 0x00308130, 0x00308610, 0x00309A90, 0x0030C010, 0x0030FA00, 0x00313A00, 0x002E1C20, 0x002E1CA0, 0x00234590, 0x00336710, 0x00339BF0, 0x0033A720, 0x0033C310, 0x0033CEF0, 0x0033D3E0, 0x00267E10, 0x00307FF0"
---

## What the player sees

Press R2 in the field; once the arming counter has run, the word FLEEING appears on the HUD: the party
stops answering the enemy, combos stop chaining for anyone who is not Confused or Berserk, and
most battle commands are refused until the party fights again. Press R2 again and the label is
gone and the party fights. The ordinary state is the fighting one. Area scripts put the party
into the fleeing state at map entry and after a teleport, and the game restores the toggle's own
state a moment later.

## How it works

### The flag and its two readers

`0x01E0C2B8` is a dword holding 1 in the image, so the game boots in force fight mode. The predicate `0x00253B90()` (thunk
`0x0030C0D0`) returns `flag == 0`: true means fleeing. Every gameplay reader tests it that way round. The predicate
takes no argument and reads only that dword (`0x00253B90`-`0x00253B9B`): there is one fleeing state, which the readers
below that take a unit apply to each unit they handle.

The second reader `0x00253BA0()` returns the flag only while the enable `0x003BA2E0()` holds and 0 otherwise; its two
callers are the battle menu's opener `0x00276650` (the `0x61F0` widget), which returns without building the menu while
`0x00253BA0()` is 0 (`0x0027668C`-`0x00276693`), so the menu is built only while the party fights and the enable holds, and
the menu's message procedure `0x00276D30`, whose message-2 arm treats a set `+0x2FF0` bit `0x4000` as the mode being on.

`0x003BA2E0()` is true when both bytes `0x02B4053C` and `0x02B4053D` are non-zero. Both are 0 in the
image; the boot `0x00266D10` writes 1 to both (`0x003BA300(1)`, `0x003BA310(1)`), the manager-0 area
unload `0x002628B0` writes 1 to the first again, and the verb `debug_setfightstatusbyevent(v)`
(`0x206B`, `0x0050C910`, one popped argument) writes its argument into the first. No shipped
event script calls that verb, so the enable holds from the first area on.

### The writers

The script verb `setforcefightmode(enable)` (`0x0334`, `0x003444D0`) calls `0x00254EA0(enable)`:
with `enable` non-zero and `0x003BA2E0()` true the flag becomes 1 and the call returns 1; otherwise
the flag becomes 0 and the call returns 0. So a script can always force the party to flee, and
can force it to fight only while the enable holds.

The R2 toggle reaches the flag through `0x00252C80(state, force)`, called only by `0x00252B60`,
called only by the input arbiter `0x00253C70` (the wrapper `0x00253C50` of [frame update
order](frame-update-order.md)) with `force` = 0, on every pass that reaches the arbiter's tail:

- with `force` clear the write is refused while either skip predicate `0x003603B0()` (`0x022CB728`)
  or `0x003603C0()` (`0x022CB726`) holds; `0x022CB728` is never set in this build (its one writer
  `0x00360370` stores 0), and `0x022CB726` is set by the title-return reset `0x003601D0` and cleared at
  the next area start (`0x00360110`), so the refusal lasts from a title return to the next area;
- `state` = 0 (the toggle disengaged) writes 1, then `0x003BA2E0()`, so the flag ends as the enable;
  `state` non-zero (engaged, the party fleeing) writes 0;
- without `force`, a non-zero `state` writes only while the flag is non-zero and `state` 0 only while
  the flag is 0 (`0x00252CBA`-`0x00252CCE`): a flag at 1 is kept by `state` 0 even while the enable is clear,
  and a flag at 0 is rewritten by `state` 0 to 1 and then to the enable. The call returns 1 when it
  writes and 0 when it does not (`0x00252CB6`, `0x00252CEA`-`0x00252CEF`);
- on a pass where `0x00265680()` answers non-zero the arbiter passes the toggle, so the toggle's state is
  re-asserted and a script's write that disagrees with it lasts only until that pass; when `0x00265680()` answers
  0 it passes instead whether the arming word `0x022CBE1A` has bit `0x1` (`0x003669D0`, `0x00254179`-`0x0025418F`), and
  while `0x00253BC0([0x02092730])` answers non-zero it calls nothing (`0x0025416C`-`0x00254173`).

The arbiter keeps the toggle in `0x020927E0`: it flips on each press while `0x0017DE10()` holds and
the edge byte `0x020927E4` was clear, is forced to 1 by the device poll path (`0x00862CF0`, with
`0x01E0C2B4`), and is cleared when `0x01E0C2B4` is 1 or the area is a town (the town flag
`0x00377C20()`, bit `0x8000` of the area's flag word, [area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

`0x00252B60(state, flag)` re-decides the state before the write:

- it returns at once when the input snapshot `0x02F97362` has bit `0x200`;
- `0x002E0FA0()` bit `0x40` forces the state to 0 with `flag` = 1; else bit `0x200` does the same and runs
  `0x00366950`; else bit `0x400` or `0x00237260()` (every active party member down) does the same; then
  `0x020927CC` = 1 does the same;
- the mode register `0x0035C6F0()` (`0x022C83EC`): with bits `0x4` and `0x8` clear and bit `0x1` set the state
  is its bit `0x2`; with bit `0x4` or `0x8` set the state is the snapshot's bit `0x200` (`0x02F97360`, 0 under policy
  bit `0x400`), `0x0035C880(0xC, (register & 4) × 2)` and, for state 0, `0x0035C880(0xC, 0)`, then
  `0x00366950`;
- unless a skip predicate holds, the arming counter runs (`0x003669F0`, then `0x003667E0` for state
  0 or `0x00366870` for state 1), and a non-zero state is replaced by `0x003669F0()`, bit `0x4` of
  `0x022CBE1A`: the flag drops to 0 only once the counter has armed.

The arming counter is audible. Both of its steps return at once while the mode register `0x0035C6F0()` has bit `0x1`
(`0x00366874`-`0x0036687B`, `0x003667E4`-`0x003667EB`). `0x00366870` starts sound `0x52` (`0x003A1180`, then `0x002DF220(handle,
0x40, 0x7F)`) on its first pass, keeping the handle in `0x022CBE1C` and bit `0x10` of `0x022CBE1A`; with bit `0x10`
already set, or when `0x003A1180` returns -1, it starts no sound (`0x0036688D`-`0x003668D7`).

It counts its passes in `0x022CBE18`, from 1 on the first pass, and once the count reaches `0x022CBE08` it holds it there
and sets bit `0x4` (armed), with bit `0x8` on the pass that arms; every pass sets bit `0x1` and clears bits `0x2` and
`0x40` (`0x003668F0`-`0x00366928`). `0x003667E0` stops that sound if it still plays (`0x002DEE80`, `0x002DF0F0`) and, when the
counter had armed (bit `0x4`) and `0x00265680()` holds with bit `0x40` clear, plays sound `0x2A` (`0x00249C60`) ([sound
effects](../Sound-And-Music/sound-effects.md)).

The cue comes first (`0x003667ED`-`0x0036680D`), then the stop, and it ends by clearing bits `0x1`, `0x4`, `0x8`, `0x10`,
`0x20` and `0x40` of `0x022CBE1A` and setting bit `0x2` (`0x00366812`-`0x0036685B`).

### What fleeing changes

The raw predicate has 7 call sites in 7 functions, and its thunk `0x0030C0D0` (a jump to it) 8 sites in 6
functions:

| Reader | What it does while fleeing |
|---|---|
| `0x002FFCF0` | refuses every command with reason `0x24` for a party-side unit without Confuse or Berserk (status `0x08000020`), except Dismiss (`0x113`) and Dismount (`0x95`) ([command availability](../Battle-Actions/command-availability.md)) |
| `0x00308610`, `0x0030C010` | the combat frame skips the combo continuation `0x0030FA00` for a unit without Confuse or Berserk, and `0x0030C010` answers "no" to the same question ([combos](../Battle-Actions/combos.md)) |
| `0x00307D10` | the engagement update, below the table: `0x022C1F48`, `0x022C1F40`, `0x00307CE0`, `0x0030BF20`, `0x0030B050` |
| `0x00307D10` | runs on a status change (`0x0030E360`, at `0x0030E7AC`) and a stats recompute (`0x002FEF30`) |
| `0x00307FF0` | does not read the predicate itself: it makes the fleeing arm's two global writes alone (`0x022C1F48 &= 0xF9`, `0x022C1F40` = 0), run by the area initialisation `0x002342F0` and by `0x002348E0`, which first tears down every enemy unit (`0x00300E40`) |
| `0x00308130` | "may the unit engage", after running `0x00307D10`, answers false for a unit with the two statuses clear; otherwise true for unit `+4` bit `0x10000`, and false when `0x022C1F48` bit `0x1` is clear. With bit `0x1` set it first arms the clock through `0x003081E0` (`0x00308192`): when unit `+0` bit `0x800000` is clear and `+0xDCC` is 0, `+0xDCC = trunc(0x0032A150() + trunc([0x01DFE0B8] * 30) * ((0x00328370() & 3) * 0.25 + 0.5))`, the sum stored as an integer. It then answers true when unit `+0x698` is null or that block's byte `+5` is non-zero (`0x003081A1`, `0x003081A9`), and otherwise when the clock `0x0032A150()` is at or past `+0xDCC` (`0x003081B2`) |
| `0x00309A90` | the approach distance is 3.8 at party-control level 1 or 2.2 otherwise, instead of the fighting value 24.0 ([party control modes](party-control-modes.md)) |
| `0x00313A00` | the action availability row writes: the second of its fourteen bits is set (`0x002E1C20`) instead of cleared (`0x002E1CA0`) while a unit's action is being shown (`0x02089350`, [Action phases](../Battle-Actions/action-phases.md)) or the party is fleeing |
| `0x00234590` | the orchestrator's reset loop runs once each time the predicate changes against the battle-state word's bit `0x8` ([frame update order](frame-update-order.md)) |
| `0x00336710`, `0x00339BF0`, `0x0033A720`, `0x0033C310`, `0x0033CEF0` | battle locomotion, in full below the table |

`0x002FFCF0` reaches reason `0x24` only after its refusals with codes 2 and 4, which keep their own codes
(`0x002FFD0F`-`0x002FFD94`), and before the checks for code `0x2C` and the rest (`0x002FFDAE`-`0x002FFDED`).

The engagement update `0x00307D10`: for a unit that is not the chocobo (`0x1A`) and not in a town, with the two statuses
clear, it clears `0x022C1F48` bits `0x2` and `0x4`, zeroes `0x022C1F40` and the unit's `+0xDCC`, and clears unit `+4` bits
`0x200`, `0x400` and `0x10000` (bit `0x10000` = engaged) (`0x00307D63`-`0x00307D82`, `0x00307DD1`-`0x00307DD8`).

The other arms, in the order the body tests them: a party-side unit whose record byte `+4` is `0x1A` (the chocobo)
gets bit `0x10000` set outright, in a town too (`0x00307D29`-`0x00307D3C`); otherwise a town clears bits `0x200`, `0x400`
and `0x10000` (`0x00307D41`-`0x00307D48`); otherwise a unit with a status set gets bit `0x10000` set (`0x00307D61`); only a
fighting unit runs the bit `0x200` path through `0x00307CE0`, `0x0030BF20` and `0x0030B050`.

With bit `0x200` set, `0x0030B050(unit)` non-zero clears bit `0x400` and sets bit `0x10000`, and a zero result keeps bit
`0x10000` set while bit `0x400` is set and otherwise clears bits `0x200`, `0x400` and `0x10000`
(`0x00307D84`-`0x00307DB0`); with bit `0x200` clear, bit `0x10000` is set when `0x00307CE0(unit)` is non-zero and
`0x0030BF20([unit +0x708])` is 0, and bits `0x200`, `0x400` and `0x10000` are cleared otherwise (`0x00307DB2`-`0x00307DE2`).

It runs when a status is added or removed (`0x0030E360`, at `0x0030E7AC`, [status
changes](../Status-Effects-And-KO/status-changes.md)) and when the stats block is recomputed (`0x002FEF30`,
[stats](../Damage-And-Battle-Formulas/stats.md)).

`0x00311F50(actor)` sets bits `0x200` and `0x400` of the actor's unit `+4` (`or [+4], 0x600`, `0x00311F5E`), and does
nothing for an actor without a unit (`0x0031B760`, `0x00311F5C`); the verbs `setemergency_one` (`0x0546`, `0x003460C0`) and
`0x05CC` (`0x00346620`) run it on the actor they resolve ([battle
verbs](../Scripts-And-Script-Commands/battle-verbs.md)). While the party flees, the next engagement update clears both
bits again for a unit other than the party's chocobo that has neither status (above).

Battle locomotion (`0x00336710`, `0x00339BF0`, `0x0033A720`, `0x0033C310`, `0x0033CEF0`): order `0x4022` counts as the engaged
order `0x4124` while fleeing; the arrival curve of `0x00339BF0` divides the remaining distance, `d / 1.5` while
fleeing against `d / 3` while fighting (`0x00339D8E`, `0x00339D98`), and, when it measures from the leader (context
`+0xD0` bit `0x1`), multiplies it by 0.25 while fleeing, `d * 0.25`, against dividing it by 5 while fighting,
`d / 5` (`0x00339D6A`, `0x00339D74`; `0x00339D52`-`0x00339D98`);

for a party unit on order `0x4022` the turn class is `0xA0` instead of `0xC0` and the search flag 4 instead of 2,
while a fighting party unit on `0x4022` gets speed `+0xFC` outright in `0x00339BF0` ([battle
locomotion](../Movement-And-Pathfinding/battle-locomotion.md)).

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01E0C2B8` | `u32` |  | force fight mode: 1 fighting (image value), 0 fleeing |
| `0x02B4053C` | `u8` |  | enable byte 1: 0 in the image; 1 from the boot and the manager-0 unload; the argument of debug_setfightstatusbyevent |
| `0x02B4053D` | `u8` |  | enable byte 2: 0 in the image; 1 from the boot |
| `0x020927E0` | `u32` |  | the R2 toggle state (1 = fleeing requested) |
| `0x020927E4` | `u8` |  | its press edge |
| `0x01E0C2B4` | `u32` |  | the device-poll override |
| `0x020927CC` | `u32` |  | forces the state to 0 when 1 |
| `0x022C83EC` | `u32` |  | the mode register (`0x0035C6F0` / `0x0035C880`) |
| `0x022CB726` | `...` |  | the two skip predicates that refuse an unforced write; with `0x022CB728` |
| `0x022CB728` | `...` |  | the two skip predicates that refuse an unforced write; with `0x022CB726` |

## Shipped data

| Fact | Value |
|---|---|
| image value of the flag | 1 (fighting) |
| image value of the enable bytes | 0 and 0 |
| verbs | `setforcefightmode` `0x0334`, `debug_setfightstatusbyevent` `0x206B` |
| readers | raw: 7 direct call sites, 8 through the thunk; effective: 2 |
| distances, divisors, factor | fighting: 24.0, divisors 3 and 5; fleeing: 3.8 or 2.2, divisor 1.5, factor 0.25 |

## Operations

Per frame: the input arbiter reads the pad, re-decides the toggle state and calls the writer. Per
script: `setforcefightmode` writes the flag outright. Per reader: a test of the dword, nothing
cached.

## State

The flag, the two enable bytes, the toggle state and its edge byte, the override cells and the
mode register.

The party's battle hold: `0x00307E70`, run once per field frame (`0x00234703`), keeps the party in its battle state for
90 frames after the last member stops fighting. It collects up to four party members (`0x0031B810`) without the
statuses `0x80000003` (or with `0x00377C20`) into `0x022C1788`, moves bit `0x4` of `0x022C1F48` into bit `0x2` and sets bit `0x4` again
when one of them is engaged (`+4` bit `0x10000`) and has none of the statuses `0x8800203B` (`0x00307EE1`-`0x00307F3F`). Then:

1. With bit `0x4` set (fighting this frame) the hold is 0.
2. With bit `0x2` set (fighting the frame before) it notes the frame counter `0x0032A150()` in `0x022C1F40` and starts the
   hold at `3 x trunc([0x01DFE0B8] x 30)`, 90 as shipped (`0x00307F53`-`0x00307F75`).
3. Otherwise a running hold becomes `[0x022C1F40] + 90 - 0x0032A150()` (`0x00307F77`-`0x00307FA5`).

Bit `0x1` of `0x022C1F48` is then set while bit `0x4` is set or the hold is not 0 (`0x00307FB4`-`0x00307FDB`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C1F44` | `i32` | 0 (zero-filled tail) | the frames left of the battle hold | `0x00307E70` (`0x00307FAE`); 0 with `0x022C1F40` in one 8-byte store: `0x00304400` (`0x00304427`), the engagement update `0x00307D10` (`0x00307D75`), `0x00307FF0` (`0x00307FF9`), `0x0030F2D0` (`0x0030F2EB`) | `0x00307E70` (`0x00307F77`) |

No other instruction reaches `0x022C1F44`: no other RIP-relative, image-base-relative or 32-bit offset reference names
it.

## Modding notes

- The predicate's sense is inverted from its name: a true `0x00253B90()` means fleeing. A hook that
  fires "during forced fights" on a true result is backwards.
- Scripts and the toggle share one dword, and the arbiter re-asserts the toggle's state on each pass where
  `0x00265680()` answers non-zero: a script's write holds only until then. Every shipped call is
  `setforcefightmode(0)`, at map entry and after a teleport in the area scripts; no call passes 1.
- Clearing either enable byte makes `setforcefightmode(1)` write 0 and makes the toggle's disengage,
  which rewrites only a flag at 0 (`0x00252CC8`-`0x00252CCE`), write 1 and then 0, so once the party flees
  it can never leave the fleeing state; a flag still at 1 stays 1 under the disengage. Only the debug
  verb could clear one, and no shipped script calls it.
- The effective reader is UI-only: gameplay never consults the enable, so a flag forced to 1 with
  the enable clear fights on screen while the menu reports fleeing.

## Related

- [Command availability](../Battle-Actions/command-availability.md): reason `0x24`.
- [Combos](../Battle-Actions/combos.md): the continuation gate.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md): the order gate and the
  arrival divisors.
- [Party control modes](party-control-modes.md): the approach distance by level.
- [Frame update order](frame-update-order.md): the input arbiter and the orchestrator's reset loop.
- [Escape Mode](../Controls-And-Input/escape.md): the R2 toggle that clears the flag, its latch, overrides and arming.
