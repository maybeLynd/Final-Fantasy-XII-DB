---
title: "Enmity: the hidden threat table that decides who an enemy attacks, what raises it, how it spreads and how it decays"
kind: "system"
category: "Enemy AI and gambits"
addresses: "0x003216E0, 0x00321850, 0x003219D0, 0x00321B00, 0x00321530, 0x00321D30, 0x003215C0, 0x00321630, 0x00321770"
---

## What the player sees

Every enemy remembers how much each party member has bothered it.

- **Actions raise it.** An attack, a heal or a spell used by a party member raises the targeted enemy's
  enmity toward that member, can raise it in enemies that already hold a grudge and are watching the same
  target, and lowers the target's enmity toward the rest of the party.
- **A fresh grudge is strong.** When no grudge an enemy holds is above 1 - before its first grudge,
  or after every grudge has decayed to 1 - the next grudge that rises gets 10 extra. The first time a
  grudge starts from nothing, the enemy also starts holding a small grudge against every other party
  member.
- **It decays.** While the enemy is not engaged, every grudge drops by 10 at a fixed interval, but never
  below 1: an enemy never fully forgets someone it was angry at.
- **Enemies act on it.** Enemy AI orders can pick the party member the enemy hates most.

How much an action changes enmity is set in that action's own definition row: one number for the target, one spread to
other enemies already holding a grudge, and one taken off the target's enmity toward the rest of the party. Only party
members' actions create enmity, and only enemies hold it.

## How it works

### The table

The table lives in the enemy's spawn record at unit `+0x6A0`, from `+0x19` (`0x00321553`-`0x0032156D`):

| Byte | Meaning |
|---|---|
| `+0x19` | the decay timer |
| `+0x1A` + *id* | the enemy's enmity toward party table row *id*, 0-255, for *id* 0-39 |

The row id is a party member's type byte (stats `+0x04`). An id counts only when
`0x00322C50(2, id, 1)` accepts it, that is when it is below the 40 rows of the party table `0x02EBF130`
(`0x00322C9A`, `0x0032302A`-`0x0032303B`). The readers return -1 for an invalid id or a missing table, and
`0x003215C0(unit, id)` for a null unit too; otherwise it returns the entry `+0x1A` + *id* (`0x003215C0`-`0x0032161D`,
`0x0032160D`).

### Writing an entry

`0x00321850(enemy, id, value, mode)` changes one entry (`0x00321850`-`0x003219CC`):

1. It does nothing unless the enemy is an enemy-table unit (stats `+0x05` = 1, `0x003218D0`) that is not KO,
   Stone or X-Zone, unless bit `0x8000` of the active field record waives that (`0x003218A6`-`0x003218BA`).
   A null enemy, one without a table or stats record, or an id `0x00322C50` rejects also changes nothing
   (`0x00321853`, `0x00321890`, `0x003218A0`, `0x003218F9`-`0x00321900`).
2. The new value is `old + value` for mode 0 or `value` for mode 1, as for any mode other than 0
   (`0x00321914`-`0x0032191A`).
3. A new value of 0 or less becomes 1 when the old value was above 0 (`0x0032191D`-`0x00321923`).
4. When the value rises and no entry of the enemy is above 1 (`0x00321770`), it gets 10 more
   (`0x00321927`-`0x0032193A`).
5. The value is stored, limited to 0-255 (`0x00321E40`).
6. When the entry went from 0 to above 0, every other zero entry with a valid id becomes 1
   (`0x0032194B`-`0x003219A5`).

So no write takes a held grudge back to 0, and the first grudge seeds a grudge of 1 against everyone else.

### What an action does

`0x003216E0(caster, target, actionRow)` runs for a party record caster only (stats `+0x05` = 0,
`0x0032170D`-`0x00321714`). With `id` the caster's type byte, it makes three calls with the action row's three
enmity bytes ([Action definition row](../Battle-Actions/action-definition-row.md)):

| Call | Row byte | Effect | Site |
|---|---|---|---|
| `0x00321850(target, id, +0x1D, 0)` | `+0x1D` | the target's enmity toward the caster rises | `0x0032172E` |
| `0x003219D0(id, +0x1F, target, 0)` | `+0x1F` | spread to other enemies, below | `0x0032173F` |
| `0x00321B00(target, -[+0x20], caster, 0)` | `+0x20` | the target's enmity toward every other active party member falls | `0x00321753` |

It is called from `Battle_ProcessActionTarget` (`0x0030760A`) and from the special-sequence target loop
(`0x0030ECF2`).

### Spreading

`0x003219D0(id, value, target, mode)` walks every unit slot (`0x003219F4`-`0x00321AD5`) and changes an enemy's entry
for `id` through `0x00321850(enemy, id, value, mode)`, by that function's rules: mode 0 adds `value` and mode 1
writes it (`0x00321ABA`-`0x00321AC7`). It does so when all of these hold:

- the unit is an enemy-table unit other than the target (`0x00321A33`-`0x00321A40`);
- it has a table and `0x00322C50` accepts `id` (`0x00321A46`-`0x00321A71`);
- its entry for `id` is already above 0 (`0x00321A73`-`0x00321A7B`);
- with a target, the target's actor (`+0x10`) is in the enemy's AI candidate list, the 16-byte entries
  from unit `+0xBC8` counted by `+0xBC4` (`0x00321A82`-`0x00321AB8`).

### Drawing threat off the rest of the party

`0x00321B00(enemy, value, except, mode)` builds the active party list (`0x0030A880(buffer, 1)`, `0x00321B5E`)
and, for every member other than `except`, changes the enemy's entry for that member's type byte by the
same rules as `0x00321850` (`0x00321B90`-`0x00321CF7`). Unlike `0x00321850`, which returns at once for a null enemy
(`0x00321850`-`0x00321853`), it reads the enemy's `+0x698` without a test (`0x00321B11`).

### Decay

The periodic maintenance step `0x00310DB0` calls `0x00321530(enemy)` for each unit (`0x003112A4`). For an
enemy-table unit with a table (`0x0032154D`-`0x00321574`):

1. If the enemy is engaged, the timer is reset to 0 and nothing decays (`0x00321576`-`0x0032157D`).
   `0x00307CE0` answers "engaged" when `0x0030C210` or `0x0030BB30` does.
2. Otherwise the timer counts up; when it reaches `30 * [0x01DFE0B8]` steps, `0x00321D30(enemy, -10, 0)`
   lowers every entry by 10 and the timer restarts (`0x0032157F`-`0x003215AC`).

`0x01DFE0B8` is the frame base, 1.0 as shipped ([Action phases](../Battle-Actions/action-phases.md)).
`0x00321D30` writes all 40 ids through `0x00321850` (`0x00321D90`-`0x00321DA6`), so the floor of 1 holds.
It changes nothing for a null enemy, one without a table or stats record, or one that is KO, Stone or X-Zone
without the field record's waiver (`0x00321D33`-`0x00321D8E`). Each id goes as `0x00321850(enemy, id, value, mode)`
(`0x00321D90`-`0x00321D9C`).

### Resets and orders

Two more callers change the table:

- **A unit leaving the fight.** `0x00300FC0(unit, flag)` calls `0x003219D0(id, 0, null, 1)` for the unit's
  type byte (`0x00301048`-`0x0030105E`): every enemy holding a grudge against it is set to 1. Teardown calls
  it with flag 1 (`0x00300E54`-`0x00300E59`).
- **KO, Stone and X-Zone.** The status write calls `0x00300FC0` with flag 0 when one of them is set: its
  side-effect switch (`0x0030E737`-`0x0030E759`, byte table `0x0030E8C4`) sends statuses 0, 1 and 31 to
  `0x0030E80A`, `0x0030E850` and `0x0030E85E`, which reach `0x0030E877` when the status is being set.
- **Espers keep the table.** With flag 0, an Esper record (party type `0x1B`-`0x27`) leaves `0x00300FC0`
  early through `0x003105D0` and `0x003138D0` (`0x00300FCF`-`0x00301005`), before the reset. The status write's
  own Esper call at `0x0030E497` takes that exit too.
- **Battle orders `0x4163` and `0x4164`.** The direct state orders call `0x00321B00` on the committing enemy: `0x4163`
  writes 1 (mode 1) and `0x4164` adds the order's parameter (mode 0) to every active party member's entry by those
  rules (`0x002FE4F1`-`0x002FE507`, [Battle orders](../Battle-Actions/battle-orders.md)), so under `0x4163` an entry
  that was 0 becomes 11 when no entry of the enemy is above 1 at that moment (`0x00321C55`-`0x00321C67`).

### How the AI reads it

The enemy AI's target selector `AiOrder_EvaluateTargetSelector` reads the enmity of a candidate party
member (`0x003215C0`, at `0x00302153`) and compares the candidate with the highest enmity toward any active
party member (`0x00321630`, at `0x00302573`-`0x0030258C`).

`0x00321630` walks the same active party list (`0x0030A880(buffer, 1)`, `0x0032166A`) and returns the highest entry for
a member's type byte, an id `0x00322C50` rejects counting as -1 (`0x00321680`-`0x003216BE`). It returns -1 when the
enemy is null or has no table (`0x0032163E`, `0x0032165B`), and when the list is empty (`0x00321674`). The relation test
`0x0030BD00` asks `0x00321840` whether an enemy holds any grudge above 0 (`0x0030BDA0`).

## Modding notes

- An action's enmity is the three bytes `+0x1D`, `+0x1F` and `+0x20` of its row; an action with all three
  at 0 leaves the table alone.
- The decay step and interval are `-10` (`0x0032159F`) and the 30.0 at `0x008F8D80`, shared with other code.
- Only party records generate enmity, and only enemy-table units hold it.

## Related

- [Action definition row](../Battle-Actions/action-definition-row.md) - the three enmity bytes.
- [Battle orders](../Battle-Actions/battle-orders.md) - orders `0x4163` and `0x4164`.
- [Action phases](../Battle-Actions/action-phases.md) - the frame base.
- [Area of effect](../Battle-Actions/area-of-effect.md) - the 16-byte list layout the AI candidate list shares.
