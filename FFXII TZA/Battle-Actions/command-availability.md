---
title: "Command availability: why a battle command is greyed out or refused, and the refusal codes"
kind: "system"
category: "Battle actions"
addresses: "002FFCF0, 0030E9C0, 0031A7B0, 00306480, 003060E0, 00323EC0, 00303BD0"
---

## What the player sees

Whether an action can be used is decided by one check, asked by the battle menu, by gambits and enemy
AI before they pick an action, and again while the action runs. A command the menu greys out is
refused by gambits for the same reason. The check goes through its tests in order and stops at the
first that refuses:

1. **The character cannot act at all** - KO, Stone or X-Zone (except in areas whose map flag waives
   this), or not active in battle.
2. **FLEEING.** While the FLEEING mode is on, a party member who is not Confused or Berserk can use
   nothing except Dismiss and Dismount.
3. **Summoning while an Esper is out.** The summon actions are refused while a summoned Esper is in
   the battle (in the plain battle state; in a town or while riding a chocobo this test does not apply).
4. **Statuses.** Stop, Sleep and Disable refuse every action; Silence refuses Magicks (and any other action with
   one particular flag); KO, Stone and X-Zone refuse everything - even where the map flag lets such a
   unit pass the first test.
5. **Commands disabled by the battle.** A battle can switch off the Attack, Magicks, Technicks or
   Items command for the party.
6. **Not owned.** A party member must own the magick, technick, summon or Quickening; guests and
   Espers must have it in their own list; Esper attacks are for Espers only.
7. **No item left** for an item action.
8. **No license.** Main party members need the license for the action; guests, Espers and enemies
   do not.
9. **Cost.** Not enough MP; not enough Mist charges for summons and Quickenings; not enough gil when
   magicks are paid with gil.

## How it works

### The check

`002FFCF0(actionId, unit)` returns 0 when the action is available and a refusal code
otherwise. It has seven callers: the battle menu `0031EB20` (`0031F28A`), the menu entry check
`00317BC0` (`00317C45`), the AI order step `003014C0` (`003015FF`), action selection `00305AB0`
(`00305B09`), the effect applier `00307300` (`00307398`), `0030DB70` (`0030DBBE`) and the running-action
check `002FFB60` (`002FFC7C`, its reason 6). In order:

1. Code 2 when the unit lacks bit 4 of its first byte or a stats record, when it has status bit 0, 1 or
   31 and `00377C20()` is 0, or when it is on the enemy side and the byte at `[unit+6A0h]` has any of
   bits 3, 4, 5 or 6 (`30`<sub>h</sub> or `48`<sub>h</sub>).
2. Code 4 when `00322C50(14h, id)` rejects the id.
3. Code `24`<sub>h</sub> for a party-side unit without Confuse or Berserk (status `08000020`<sub>h</sub>) while
   `00253B90()` is 1 (FLEEING, `01E0C2B8` = 0), unless the id is `113`<sub>h</sub> (Dismiss) or `95`<sub>h</sub> (Dismount).
4. Code `2C`<sub>h</sub> for ids `106`<sub>h</sub>-`112`<sub>h</sub> (the summons) while `0030D9A0()` is 1 - bit 0 of
   `[02EBF190]+5B04h`, which the summon scene sets ([Quickenings and summons](quickenings-and-summons.md)).
   `0030D9A0` returns 5, 4, 3 (town flag `00377C20`), 2 or 1 from bits 3, 2, the town flag, 1 and 0 of
   that word, in that priority.
5. **Statuses:** `0030E9C0(stats, mask)` with mask `8000201B`<sub>h</sub> (status bits 0, 1, 3, 4, 13, 31), or
   `8000221B`<sub>h</sub> (adding bit 9) when the row has bit 19 of `+0C`<sub>h</sub> or kind byte `+1E`<sub>h</sub> = 1 (Magicks).
   With a status in the mask it returns 10 for Silence (bit 9), 7 for Stop (3), 8 for Sleep (4), 11 for
   Disable (13), 9 for Confuse (5), 12 for Berserk (27), else 6 - in that priority; bits 5 and 27 are
   never in the mask here.
6. **Disabled commands:** `0031A7B0(stats, id)` - for a party-side unit only - returns `16`<sub>h</sub>, `17`<sub>h</sub>,
   `18`<sub>h</sub> or `19`<sub>h</sub> when the row's kind `+1E`<sub>h</sub> is 0, 1, 2 or 3 and bit 2, 3, 4 or 5 of the battle flags
   `022C314C` is set. Those bits are set and cleared by the battle orders `413B`<sub>h</sub>-`413E`<sub>h</sub> /
   `4143`<sub>h</sub>-`4146`<sub>h</sub> ([Battle orders](battle-orders.md)).
7. **Ownership and license:** `00306480(id, stats)` returns `0F`<sub>h</sub> when `003060E0` returns non-zero,
   `10`<sub>h</sub> when the license check `00323EC0` returns 0, else 0.
8. **Cost:** `00303BD0(unit, id)`.

### Action kinds

Byte `+1E`<sub>h</sub> of an action row is its kind; the names come from the members of each kind in
`battle_pack.bin`: 0 Attack, 1 Magicks,
2 Technicks, 3 Items, 5 summons, 6 Quickenings, 7 Foecraft, 8 traps, 9 Esper attacks, 10 Concurrences,
255 unused.

### Ownership

`003060E0(id, stats, 0)` checks ownership for the party side only; enemies pass. Kind 0 and 255
pass. Kinds 1,
2, 5 and 6: a guest (type id `07`<sub>h</sub>-`19`<sub>h</sub>) or Esper (`1B`<sub>h</sub>-`27`<sub>h</sub>) passes when the row's ability id
`+22`<sub>h</sub> is one of the ten `i16` at `+58`<sub>h</sub> of its record in the table at `02EBF130`; anyone else when
`0030B0E0(+22h)` (the owned count for that id class, through the handler table at `01EEBD10`) is above
0. Kind 3: `003037A0` (below). Kind 9: only an Esper passes. Kind 4 and kinds 7, 8 and 10 return 5.
`00306480` turns any non-zero result into `0F`<sub>h</sub>. `003093B0(row)` returns a kind-3 row's `+22`<sub>h</sub>, and `FFFF`<sub>h</sub>
for any other kind or a null row; the battle menu `0031EB20` asks it (`0031F090`).

### License

`00323EC0(stats, id)` passes (returns non-zero) for anyone other than a main party
member (stats `+05`<sub>h</sub> = 0 and type id below 7), and for rows with bit 13 of `+2C`<sub>h</sub>. For the
Quickenings (`D0`<sub>h</sub>-`E1`<sub>h</sub>) a main party member passes when the Quickening's index in the character's
record (`0030A330`) is below `00324020(stats)`; for any other row the License Board check
`00323BB0(stats, 1, id)` decides.

### Cost

`00303BD0(unit, id)` checks the costs in this order:

| Code | Test |
|---:|---|
| `12`<sub>h</sub> | `003037A0`: for a party-side unit, the item the action uses (`003093D0(id)`, not `FFFF`<sub>h</sub>) has an owned count of 0 (`0030B0E0`) and is not the item already set aside at `+DC8`<sub>h</sub> |
| `13`<sub>h</sub> | MP: the `i16` at stats `+4C`<sub>h</sub> is below `00309110` - for kinds other than 5 and 6, the row's byte `+0A`<sub>h</sub> adjusted by `002F95D0`, or 0 when the unit pays with gil |
| `14`<sub>h</sub> | Mist charges: the byte at stats `+4E`<sub>h</sub> is below `00308FF0` - the row's byte `+0A`<sub>h</sub> for kinds 5 and 6, else 0 |
| `15`<sub>h</sub> | gil: for a party-side unit paying with gil (`002F9820`: effect bit 0 of `+6C`<sub>h</sub> or `+7C`<sub>h</sub>, effect 32, "Enables casting of magicks with gil, rather than MP"), when the cost `00309060` is above both the party's gil (`[02092758]+8`, `00253690`) and the gil already reserved at `+E58`<sub>h</sub> |

### Which cost the battle menu shows

For a row with bit 29 of `+0C`<sub>h</sub> (the entry carries a cost), the battle menu `0031EB20` asks
`002FA140(unit, id)` (90 bytes, called only at `0031F033`) which cost to show, and stores the mapped value
at `+4C`<sub>h</sub> of its list record:

| `002FA140` returns | When | Stored |
|---:|---|---:|
| 0 | the unit's stats record has kind byte `+05`<sub>h</sub> = 1 (an enemy) (`002FA151`) | 1 (MP) |
| 2 | the id is a summon `106`<sub>h</sub>-`112`<sub>h</sub> or a Quickening `D0`<sub>h</sub>-`E1`<sub>h</sub> (`002FA15A`-`002FA179`) | 2 (Mist charges) |
| 1 | bit 0 of stats `+6C`<sub>h</sub> or `+7C`<sub>h</sub> is set, the same pay-with-gil test as `002F9820` (`002FA182`-`002FA18C`) | 4 (gil) |
| 0 | otherwise | 1 (MP) |

A row with bit 31 of `+0C`<sub>h</sub> stores 3 (the item count) instead.

## Modding notes

- An action's kind is byte `+1E`<sub>h</sub> of its row; kinds 1 and 2 decide whether Silence applies (kind 1,
  or flag bit 19) and which of the battle's command switches covers it.
- Bit 13 of `+2C`<sub>h</sub> makes an action need no license.
- The cost byte is `+0A`<sub>h</sub> of the row: MP for most kinds, Mist charges for summons and Quickenings.

## Related

- [Battle orders](battle-orders.md) - the orders that switch commands off and on.
- [Quickenings and summons](quickenings-and-summons.md) - the summon flag behind code `2C`<sub>h</sub>.
- [Target selection](target-selection.md) - the menu builder that asks this check.
- [Action phases](action-phases.md) - the running action that asks it again.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status
  names.
- [License check](../Items-Equipment-Shops-And-Licenses/licenses.md)
  - what the License Board check tests.
