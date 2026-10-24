---
title: "Action commit: locking in an action and target, the leader's target, the attacker mask and the idle-unit queue"
kind: "system"
category: "Battle actions"
addresses: "0x0030F760, 0x00310780, 0x00313B30, 0x00308610, 0x00313CD0"
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

`0x0030F760(unit, actionData, actionId, targetHandle, reset)` (570 bytes) has five
callers: action selection `0x00305AB0` (`0x00305B2F`, `0x00305C9B`), the AI order step `0x00305CC0`
(`0x00305DF4`), the combo continuation `0x0030FA00` (`0x0030FA5C`) and the automatic engage attack `0x00312FA0`
(`0x003130DC`).

1. With `reset` non-zero it first calls `0x003105D0`, the action cancel and reset (`0x0030F788`).
2. The target handle is resolved with `0x0031B7E0`; a handle that does not resolve leaves the target
   null and the commit still goes ahead (`0x0030F78F`-`0x0030F79E`).
3. **Action ids.** An id up to `0x21E` clears the target list at unit `+0x778` (`0x00316CF0`) and
   appends the target's `+0x10` object, or 0 (`0x00316CD0`) (`0x0030F7A1`-`0x0030F7D7`). An id above it is
   accepted only when `(u16)(id - 0x4000) <= 0x166`, that is `0x4000`-`0x4166`, and then the list is
   left alone; any other id returns 0 (`0x0030F7D9`-`0x0030F7EC`).
4. **The commit block.** It clears bits `0x1` and `0x2` of `+0x700`, stores `actionData` at `+0x708`, the
   handle at `+0x710` and the id at `+0x714`, zeroes the phase byte `+0x6B4`, and copies `+0x700`-`+0x717`
   to `+0x718`-`+0x72F` (`0x0030F7F2`-`0x0030F82A`).
5. `+0x770` is kept when the unit is on the enemy side (stats `+0x05` = 1), or on the party side with an
   id equal to `+0x744` and a handle equal to `+0x740`; otherwise it is zeroed (`0x0030F832`-`0x0030F85F`).
6. When bit `0x2` of the action-context word `+0x6B0` is set it is cleared, and the stats-record list gets
   one entry: `+0x6B9` = the byte at `0x022C1DB8 + 12 * [unit+0xEA9]`, `+0x6B6` = 1 (`0x0030F865`-`0x0030F894`).
7. `+0x24` holds the handle of the unit's group leader (see
   [the battle unit field map](../Characters-And-Objects/battle-unit-fields.md)); a unit
   is its group's leader when its own id `+0x08` equals it, and a group is the units sharing that
   handle. When the unit is not its group's leader, `+0x750` is zeroed (`0x0030F89B`-`0x0030F8A3`).
8. For a resolved target and an id up to `0x21E` (`0x0030F8A9`-`0x0030F8B6`):
   - **Hostile target** (`0x0030AB40(unit, target, 0)` above 1, see [Area of effect](area-of-effect.md)):
     `+0x754` = the handle. If the unit is its group's leader, every slot unit that has a stats record,
     is not KO, Stone or X-Zone (unless `0x00377C20()` is non-zero) and has the same group-leader handle `+0x24` gets
     `+0x754` = the handle, and the leader's `+0x750` = the handle (`0x0030F8BC`-`0x0030F931`).
   - **Any target**, unless unit bit `0x400000` is set: with `bit = 1 << [unit+0xEA9]`, if the target's mask
     `+0xEA4` does not have it, the target's count `+0xEA8` goes up by 1, the bit is set, and
     `0x00313B30(unit, target, 1)` reports it (`0x0030F937`-`0x0030F975`).
9. It returns 1 (`0x0030F97A`).

### Release

The action reset `0x003105D0` calls `0x00310780` first (`0x00310605`). For a unit with a stats
record whose target `+0x710` resolves and whose bit `0x400000` is clear, `0x00310780` removes the unit's bit from
the target's `+0xEA4`, decrements `+0xEA8`, reports it with `0x00313B30(unit, target, 0)` and calls
`0x002FEAD0(target)` (`0x0031079F`-`0x003107FE`). `0x00310780` is also called from `0x00300FC0` (`0x0030100D`). Both
fields are zeroed when a unit is reset for reuse (`0x00236AD8`-`0x00236ADF`) and by `0x00322050` and `0x00322080`.

For any unit with a stats record, `0x00310780` then releases the presentation slot `+0x694`
([Action phases](action-phases.md); `0x00310812`-`0x00310825`). For the order id `0x414E` it calls
`0x00317E50`, which is `0x0025AAD0(1, 0)`: with handle 0 `0x003588B0` resolves nothing and the non-zero
first argument skips the rest, so the call changes nothing (`0x0031084D`-`0x00310856`, `0x003588B4`,
`0x0025AAE1`).

### The report

`0x00313B30(unit, target, adding)` runs when the target has a stats record and is not KO, Stone or
X-Zone (or `0x00377C20()` is non-zero), or when `adding` is 0. For a party-side unit the recipients are
the living party members at positions 0-3 (`0x0031B810`, staged in `0x022C1788`); otherwise the unit
itself.

To each recipient it posts a combat-relation event to its character record through
`0x002ED2A0(recipient id, record)`, which resolves the recipient's actor (`0x003588B0`) and hands the
record to `0x003E6B50`. The record holds:

- 1 when the recipient is the acting unit, 2 otherwise;
- whether this is a removal;
- the ids of the recipient, the acting unit and the target.

### The idle-unit queue

Queueing happens in the combat frame `0x00308610`, for a unit whose `+0x708` is null and whose bit `0x20` is
clear (`0x0030868B`-`0x003086DA`):

1. When unit bit `0x400000` is set, `0x00308270` is called.
2. The unit is cancelled and reset (`0x003105D0`) and its bit `0x20` is set.
3. Its id is written into the 64-entry ring at `0x022BE984` (8-byte entries) at the write index
   `0x022BE981`, which then advances modulo 64.

Draining is done by `0x00313CD0`, called from `0x00234520` (`0x00234582`). The simulation tick `0x00314020`
calls `0x00234520` once per tick in tick mode 0 (`0x0031412B`; it does nothing for any slot but 0) and
never in tick mode 1. Inside it the drain runs only when bits `0x1` and `0x4` of `0x02089340` are not 1 and 0
(otherwise the one-shot callback at `0x0208E6A8` runs) and `0x00383C80` reports a loaded navigation
dataset (`0x00234547`-`0x00234582`).

`0x00313CD0` does nothing while bit `0x20` of `0x02089340` is set; otherwise it makes 8 attempts to take an
entry from the read index `0x022BE980` (an empty ring yields handle 0). For each unit that resolves and
still has bit `0x20`, it clears the bit and calls `0x00305AB0(unit, 0)` when the unit:

- has a stats record and is not KO, Stone or X-Zone (unless `0x00377C20()` is non-zero);
- has none of status bits `0x1`, `0x2`, `0x8`, `0x10` and `0x80000000` (`0x8000001B`);
- gets 0 from `0x0030DA30(unit)`.

`0x0030FE60` resets both indices.

## State

| Field | Width | Meaning | Written by |
|---|---|---|---|
| unit `+0x708` | `void*` | committed action data | `0x0030F7F9` |
| unit `+0x710` | `u32` | committed target handle | `0x0030F800` |
| unit `+0x714` | `u16` | committed action id | `0x0030F806` |
| unit `+0x718`-`+0x72F` | `u8[24]` | copy of `+0x700`-`+0x717` at commit | `0x0030F823`, `0x0030F82A` |
| unit `+0x750` | `u32` | the leader's own hostile target; read by `0x00301AD0` (`0x0030314F`, `0x00303176`) | `0x0030F931`; zeroed at `0x0030F8A3`; `0x00305E70` copies `+0x754` into it |
| unit `+0x754` | `u32` | the group leader's hostile target | `0x0030F8CF`, `0x0030F920` |
| unit `+0xEA4` | `u32` | attacker mask, one bit per `+0xEA9` index | `0x0030F962`; `0x003107EA` |
| unit `+0xEA8` | `u8` | attacker count | `0x0030F959` (+1); `0x003107DD` (-1) |
| `0x022BE980` / `0x022BE981` | `u8` | idle-queue read and write indices | `0x00313D1E` / `0x003086DA`; both zeroed by `0x0030FE60` (`0x0030FE7B`) |

`0x0030FE60` lays out three blocks the same way: a 16-bit word, then 64 entries of 8 bytes. It stores 0 in each word
and in the first dword of each entry. The first block is the idle-unit queue (`0x022BE980`) and the third the show
queue (`0x022BEDA0`, [Action phases](action-phases.md)); the second is used by nothing else.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022BEB90` | `u16` | 0 | the word before the 64 entries `0x022BEB94`-`0x022BED93`; only the reset touches the word and the entries | `0x0030FE60`, 0 (`0x0030FE9B`; the entries at `0x0030FE90`) | no instruction |

No other instruction reaches `0x022BEB90`-`0x022BED93`. The reset's store is `0x0030FE9B`, and its loop starts at
`0x0030FE82` and ends at `0x022BED94` (`0x0030FE89`), the gambit value of
[Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md).

## Related

- [Area of effect](area-of-effect.md) - the target list the commit starts, and the stats-record list.
- [Target selection](target-selection.md) - how the menu's target is chosen before the commit.
- [Combos](combos.md) - the commit repeated for every extra hit.
- [Gambits and enmity](../Enemy-AI-And-Gambits/gambits.md) - the gambit
  target selector that reads `+0x750`.
