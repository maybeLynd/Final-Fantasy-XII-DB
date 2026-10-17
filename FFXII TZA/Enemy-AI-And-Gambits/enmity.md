---
title: "Enmity: the hidden threat table that decides who an enemy attacks, what raises it, how it spreads and how it decays"
kind: "system"
category: "Enemy AI and gambits"
addresses: "003216E0, 00321850, 003219D0, 00321B00, 00321530, 00321D30, 003215C0, 00321630, 00321770"
---

## What the player sees

Every enemy remembers how much each party member has bothered it.

- **Actions raise it.** An attack, a heal or a spell used by a party member raises the targeted enemy's
  enmity toward that member, can raise it in enemies that already hold a grudge and are watching the same
  target, and lowers the target's enmity toward the rest of the party.
- **The first grudge is strong.** The first time an enemy holds a real grudge it gets 10 extra, and it
  starts holding a small grudge against every other party member too.
- **It decays.** While the enemy is not engaged, every grudge drops by 10 at a fixed interval, but never
  below 1: an enemy never fully forgets someone it was angry at.
- **Enemies act on it.** Enemy AI orders can pick the party member the enemy hates most.

## How it works

### The table

The table lives in the enemy's spawn record at unit `+0x6A0`, from `+0x19` (`00321553`-`0032156D`):

| Byte | Meaning |
|---|---|
| `+0x19` | the decay timer |
| `+0x1A` + *id* | the enemy's enmity toward party table row *id*, 0-255, for *id* 0-39 |

The row id is a party member's type byte (stats `+0x04`). An id counts only when
`00322C50(2, id, 1)` accepts it, that is when it is below the 40 rows of the party table `02EBF130`
(`00322C9A`, `0032302A`-`0032303B`). The readers return -1 for an invalid id or a missing table
(`003215C0`-`0032161D`).

### Writing an entry

`00321850(enemy, id, value, mode)` changes one entry (`00321850`-`003219CC`):

1. It does nothing unless the enemy is an enemy-table unit (stats `+0x05` = 1, `003218D0`) that is not KO,
   Stone or X-Zone, unless bit 15 of the active field record waives that (`003218A6`-`003218BA`).
2. The new value is `old + value` for mode 0 or `value` for mode 1 (`00321914`-`0032191A`).
3. A new value of 0 or less becomes 1 when the old value was above 0 (`0032191D`-`00321923`).
4. When the value rises and no entry of the enemy is above 1 (`00321770`), it gets 10 more
   (`00321927`-`0032193A`).
5. The value is stored, limited to 0-255 (`00321E40`).
6. When the entry went from 0 to above 0, every other zero entry with a valid id becomes 1
   (`0032194B`-`003219A5`).

So no write takes a held grudge back to 0, and the first grudge seeds a grudge of 1 against everyone else.

### What an action does

`003216E0(caster, target, actionRow)` runs for a party record caster only (stats `+0x05` = 0,
`0032170D`-`00321714`). With `id` the caster's type byte, it makes three calls with the action row's three
enmity bytes ([Action definition row](../Battle-Actions/action-definition-row.md)):

| Call | Row byte | Effect | Site |
|---|---|---|---|
| `00321850(target, id, +0x1D, 0)` | `+0x1D` | the target's enmity toward the caster rises | `0032172E` |
| `003219D0(id, +0x1F, target, 0)` | `+0x1F` | spread to other enemies, below | `0032173F` |
| `00321B00(target, -[+0x20], caster, 0)` | `+0x20` | the target's enmity toward every other active party member falls | `00321753` |

It is called from `Battle_ProcessActionTarget` (`0030760A`) and from the special-sequence target loop
(`0030ECF2`).

### Spreading

`003219D0(id, value, target, mode)` walks every unit slot (`003219F4`-`00321AD5`) and writes `value` into
an enemy's entry for `id` when all of these hold:

- the unit is an enemy-table unit other than the target (`00321A33`-`00321A40`);
- its entry for `id` is already above 0 (`00321A73`-`00321A7B`);
- with a target, the target's actor (`+0x10`) is in the enemy's AI candidate list, the 16-byte entries
  from unit `+0xBC8` counted by `+0xBC4` (`00321A82`-`00321AB8`).

### Drawing threat off the rest of the party

`00321B00(enemy, value, except, mode)` builds the active party list (`0030A880(buffer, 1)`, `00321B5E`)
and, for every member other than `except`, changes the enemy's entry for that member's type byte by the
same rules as `00321850` (`00321B90`-`00321CF7`).

### Decay

The periodic maintenance step `00310DB0` calls `00321530(enemy)` for each unit (`003112A4`). For an
enemy-table unit with a table (`0032154D`-`00321574`):

1. If the enemy is engaged, the timer is reset to 0 and nothing decays (`00321576`-`0032157D`).
   `00307CE0` answers "engaged" when `0030C210` or `0030BB30` does.
2. Otherwise the timer counts up; when it reaches `30 * [01DFE0B8]` steps, `00321D30(enemy, -10, 0)`
   lowers every entry by 10 and the timer restarts (`0032157F`-`003215AC`).

`01DFE0B8` is the frame base, 1.0 as shipped ([Action phases](../Battle-Actions/action-phases.md)).
`00321D30` writes all 40 ids through `00321850` (`00321D90`-`00321DA6`), so the floor of 1 holds.

### Resets and orders

Two more callers change the table:

- **A unit leaving the fight.** `00300FC0(unit, flag)` calls `003219D0(id, 0, null, 1)` for the unit's
  type byte (`00301048`-`0030105E`): every enemy holding a grudge against it is set to 1. Teardown calls
  it with flag 1 (`00300E54`-`00300E59`).
- **KO, Stone and X-Zone.** The status write calls `00300FC0` with flag 0 when one of them is set: its
  side-effect switch (`0030E737`-`0030E759`, byte table `0030E8C4`) sends statuses 0, 1 and 31 to
  `0030E80A`, `0030E850` and `0030E85E`, which reach `0030E877` when the status is being set.
- **Espers keep the table.** With flag 0, an Esper record (party type `0x1B`-`0x27`) leaves `00300FC0`
  early through `003105D0` and `003138D0` (`00300FCF`-`00301005`), before the reset. The status write's
  own Esper call at `0030E497` takes that exit too.
- **Battle orders `0x4163` and `0x4164`.** The direct state orders call `00321B00` on the committing
  enemy: `0x4163` sets every active party member's entry to 1 and `0x4164` adds the order's parameter
  (`002FE4F1`-`002FE507`, [Battle orders](../Battle-Actions/battle-orders.md)).

### How the AI reads it

The enemy AI's target selector `AiOrder_EvaluateTargetSelector` reads the enmity of a candidate party
member (`003215C0`, at `00302153`) and compares the candidate with the highest enmity toward any active
party member (`00321630`, at `00302573`-`0030258C`). `00321630` walks the same active party list and
returns -1 when the enemy has no table. The relation test `0030BD00` asks `00321840` whether an enemy
holds any grudge above 0 (`0030BDA0`).

## Modding notes

- An action's enmity is the three bytes `+0x1D`, `+0x1F` and `+0x20` of its row; an action with all three
  at 0 leaves the table alone.
- The decay step and interval are `-10` (`0032159F`) and the 30.0 at `008F8D80`, shared with other code.
- Only party records generate enmity, and only enemy-table units hold it.

## Related

- [Action definition row](../Battle-Actions/action-definition-row.md) - the three enmity bytes.
- [Battle orders](../Battle-Actions/battle-orders.md) - orders `0x4163` and `0x4164`.
- [Action phases](../Battle-Actions/action-phases.md) - the frame base.
- [Area of effect](../Battle-Actions/area-of-effect.md) - the 16-byte list layout the AI candidate list shares.
