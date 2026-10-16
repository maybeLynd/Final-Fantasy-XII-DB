---
title: "Action commit: locking in an action and target, the leader's target, the attacker mask and the idle-unit queue"
kind: "system"
category: "Battle actions"
addresses: "0030F760, 00310780, 00313B30, 00308610, 00313CD0"
---

## What the player sees

The moment a character or an enemy locks in an action - from the menu, a gambit, its AI, an
automatic attack or the next hit of a combo - the game records what it is doing and to whom.
Nothing about damage, cost or timing is decided at that moment.

- **The action and its target** are stored on the unit, and the target becomes the first entry of
  the action's target list.
- **The leader's target.** When the leader of a group commits to a hostile target, every living
  member of that group records it as the leader's target.
- **Who is targeting whom.** The target keeps a mask of the units that have committed an action
  against it, and a count of them; a unit is added once and removed when its action is cancelled or
  reset. Each such change is posted as a combat-relation event to the acting side's living party
  members (or to the enemy itself).
- **Idle units.** A unit with no action goes into a queue; once per simulation tick, up to 8 queued
  units that are still able to act are sent back to choose their next action.

## How it works

### The commit

`0030F760(unit, actionData, actionId, targetHandle, reset)` (570 bytes) has five
callers: action selection `00305AB0` (`00305B2F`, `00305C9B`), the AI order step `00305CC0`
(`00305DF4`), the combo continuation `0030FA00` (`0030FA5C`) and the automatic engage attack `00312FA0`
(`003130DC`).

1. With `reset` non-zero it first calls `003105D0`, the action cancel and reset (`0030F788`).
2. The target handle is resolved with `0031B7E0`; a handle that does not resolve leaves the target
   null and the commit still goes ahead (`0030F78F`-`0030F79E`).
3. **Action ids.** An id up to `21E`<sub>h</sub> clears the target list at unit `+778`<sub>h</sub> (`00316CF0`) and
   appends the target's `+10`<sub>h</sub> object, or 0 (`00316CD0`) (`0030F7A1`-`0030F7D7`). An id above it is
   accepted only when `(u16)(id - 4000h) <= 166h`, that is `4000`<sub>h</sub>-`4166`<sub>h</sub>, and then the list is
   left alone; any other id returns 0 (`0030F7D9`-`0030F7EC`).
4. **The commit block.** It clears bits 0 and 1 of `+700`<sub>h</sub>, stores `actionData` at `+708`<sub>h</sub>, the
   handle at `+710`<sub>h</sub> and the id at `+714`<sub>h</sub>, zeroes the phase byte `+6B4`<sub>h</sub>, and copies `+700`<sub>h</sub>-`+717`<sub>h</sub>
   to `+718`<sub>h</sub>-`+72F`<sub>h</sub> (`0030F7F2`-`0030F82A`).
5. `+770`<sub>h</sub> is kept when the unit is on the enemy side (stats `+05`<sub>h</sub> = 1), or on the party side with an
   id equal to `+744`<sub>h</sub> and a handle equal to `+740`<sub>h</sub>; otherwise it is zeroed (`0030F832`-`0030F85F`).
6. When bit 1 of the action-context word `+6B0`<sub>h</sub> is set it is cleared, and the stats-record list gets
   one entry: `+6B9`<sub>h</sub> = the byte at `022C1DB8 + 12 * [unit+EA9h]`, `+6B6`<sub>h</sub> = 1 (`0030F865`-`0030F894`).
7. `+24`<sub>h</sub> holds the handle of the unit's group leader (see
   [the battle unit field map](../Characters-And-Objects/battle-unit-fields.md)); a unit
   is its group's leader when its own id `+08`<sub>h</sub> equals it, and a group is the units sharing that
   handle. When the unit is not its group's leader, `+750`<sub>h</sub> is zeroed (`0030F89B`-`0030F8A3`).
8. For a resolved target and an id up to `21E`<sub>h</sub> (`0030F8A9`-`0030F8B6`):
   - **Hostile target** (`0030AB40(unit, target, 0)` above 1, see [Area of effect](area-of-effect.md)):
     `+754`<sub>h</sub> = the handle. If the unit is its group's leader, every slot unit that has a stats record,
     is not KO, Stone or X-Zone (unless `00377C20()` is non-zero) and has the same group-leader handle `+24`<sub>h</sub> gets
     `+754`<sub>h</sub> = the handle, and the leader's `+750`<sub>h</sub> = the handle (`0030F8BC`-`0030F931`).
   - **Any target**, unless unit bit 22 is set: with `bit = 1 << [unit+EA9h]`, if the target's mask
     `+EA4`<sub>h</sub> does not have it, the target's count `+EA8`<sub>h</sub> goes up by 1, the bit is set, and
     `00313B30(unit, target, 1)` reports it (`0030F937`-`0030F975`).
9. It returns 1 (`0030F97A`).

### Release

The action reset `003105D0` calls `00310780` first (`00310605`). For a unit with a stats
record whose target `+710`<sub>h</sub> resolves and whose bit 22 is clear, `00310780` removes the unit's bit from
the target's `+EA4`<sub>h</sub>, decrements `+EA8`<sub>h</sub>, reports it with `00313B30(unit, target, 0)` and calls
`002FEAD0(target)` (`0031079F`-`003107FE`). `00310780` is also called from `00300FC0` (`0030100D`). Both
fields are zeroed when a unit is reset for reuse (`00236AD8`-`00236ADF`) and by `00322050` and `00322080`.

For any unit with a stats record, `00310780` then releases the presentation slot `+694`<sub>h</sub>
([Action phases](action-phases.md); `00310812`-`00310825`). For the order id `414E`<sub>h</sub> it calls
`00317E50`, which is `0025AAD0(1, 0)`: with handle 0 `003588B0` resolves nothing and the non-zero
first argument skips the rest, so the call changes nothing (`0031084D`-`00310856`, `003588B4`,
`0025AAE1`).

### The report

`00313B30(unit, target, adding)` runs when the target has a stats record and is not KO, Stone or
X-Zone (or `00377C20()` is non-zero), or when `adding` is 0. For a party-side unit the recipients are
the living party members at positions 0-3 (`0031B810`, staged in `022C1788`); otherwise the unit
itself.

To each recipient it posts a combat-relation event to its character record through
`002ED2A0(recipient id, record)`, which resolves the recipient's actor (`003588B0`) and hands the
record to `003E6B50`. The record holds:

- 1 when the recipient is the acting unit, 2 otherwise;
- whether this is a removal;
- the ids of the recipient, the acting unit and the target.

### The idle-unit queue

Queueing happens in the combat frame `00308610`, for a unit whose `+708`<sub>h</sub> is null and whose bit 5 is
clear (`0030868B`-`003086DA`):

1. When unit bit 22 is set, `00308270` is called.
2. The unit is cancelled and reset (`003105D0`) and its bit 5 is set.
3. Its id is written into the 64-entry ring at `022BE984` (8-byte entries) at the write index
   `022BE981`, which then advances modulo 64.

Draining is done by `00313CD0`, called from `00234520` (`00234582`). The simulation tick `00314020`
calls `00234520` once per tick in tick mode 0 (`0031412B`; it does nothing for any slot but 0) and
never in tick mode 1. Inside it the drain runs only when bits 0 and 2 of `02089340` are not 1 and 0
(otherwise the one-shot callback at `0208E6A8` runs) and `00383C80` reports a loaded navigation
dataset (`00234547`-`00234582`).

`00313CD0` does nothing while bit 5 of `02089340` is set; otherwise it makes 8 attempts to take an
entry from the read index `022BE980` (an empty ring yields handle 0). For each unit that resolves and
still has bit 5, it clears the bit and calls `00305AB0(unit, 0)` when the unit:

- has a stats record and is not KO, Stone or X-Zone (unless `00377C20()` is non-zero);
- has none of status bits 0, 1, 3, 4 and 31 (`8000001B`<sub>h</sub>);
- gets 0 from `0030DA30(unit)`.

`0030FE60` resets both indices.

## State

| Field | Width | Meaning | Written by |
|---|---|---|---|
| unit `+708`<sub>h</sub> | `void*` | committed action data | `0030F7F9` |
| unit `+710`<sub>h</sub> | `u32` | committed target handle | `0030F800` |
| unit `+714`<sub>h</sub> | `u16` | committed action id | `0030F806` |
| unit `+718`<sub>h</sub>-`+72F`<sub>h</sub> | `u8[24]` | copy of `+700`<sub>h</sub>-`+717`<sub>h</sub> at commit | `0030F823`, `0030F82A` |
| unit `+750`<sub>h</sub> | `u32` | the leader's own hostile target; read by `00301AD0` (`0030314F`, `00303176`) | `0030F931`; zeroed at `0030F8A3`; `00305E70` copies `+754`<sub>h</sub> into it |
| unit `+754`<sub>h</sub> | `u32` | the group leader's hostile target | `0030F8CF`, `0030F920` |
| unit `+EA4`<sub>h</sub> | `u32` | attacker mask, one bit per `+EA9`<sub>h</sub> index | `0030F962`; `003107EA` |
| unit `+EA8`<sub>h</sub> | `u8` | attacker count | `0030F959` (+1); `003107DD` (-1) |
| `022BE980` / `022BE981` | `u8` | idle-queue read and write indices | `00313D1E` / `003086DA`; both zeroed by `0030FE60` (`0030FE7B`) |

## Related

- [Area of effect](area-of-effect.md) - the target list the commit starts, and the stats-record list.
- [Target selection](target-selection.md) - how the menu's target is chosen before the commit.
- [Combos](combos.md) - the commit repeated for every extra hit.
- [Gambits and enmity](../Enemy-AI-And-Gambits/gambits.md) - the gambit
  target selector that reads `+750`<sub>h</sub>.
