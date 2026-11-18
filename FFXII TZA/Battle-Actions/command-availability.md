[Home](../../README.md) / [Battle actions](README.md) / Command availability

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Command availability: why a battle command is greyed out or refused, and the refusal codes | system | Battle actions | How an action runs | The one check the battle menu, gambits, AI and the action itself all use to decide whether a unit may use an action - the order of its tests (unable to act, FLEEING, summoning while an Esper is out, Stop, Sleep, Silence, Disable, commands disabled by the battle, abilities not owned, missing items, licenses, MP, Mist charges, gil) and the refusal code each test returns. | 0x002FFCF0, 0x0030E9C0, 0x0031A7B0, 0x00306480, 0x003060E0, 0x00323EC0, 0x00303BD0 |

## What the player sees

Whether an action can be used is decided by one check, asked by the battle menu, by gambits and enemy
AI before they pick an action, and again while the action runs. A command the menu greys out is
refused by gambits for the same reason. The check goes through its tests in order and stops at the
first that refuses:

1. **The character cannot act at all** - KO, Stone or X-Zone (except in towns, the areas whose town flag is
   set; [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)), or not active in battle.
2. **FLEEING.** While the FLEEING mode is on, a party member who is not Confused or Berserk can use
   nothing except Dismiss and Dismount.
3. **Summoning while an Esper is out.** The summon actions are refused while a summoned Esper is in
   the battle (in the plain battle state; in a town or while riding a chocobo this test does not apply).
4. **Statuses.** Stop, Sleep and Disable refuse every action; Silence refuses Magicks and the 16 enemy
   Foecraft actions that the game data also flags for Silence, such as Fear, Fog, Aquaga, Curse and
   Necromancy; KO, Stone and X-Zone refuse everything - even where the town flag lets such a unit pass
   the first test.
5. **Commands disabled by the battle.** A battle can switch off the Attack, Magicks, Technicks or
   Items command for the party.
6. **Not owned.** A party member must own the magick, technick, summon or Quickening; guests and
   Espers must have it in their own list; Esper attacks are for Espers only.
7. **No item left** for an item action.
8. **No license.** Main party members need the license for the action; guests, Espers and enemies
   do not.
9. **Cost.** Not enough MP; not enough Mist charges for summons and Quickenings; not enough gil when
   magicks are paid with gil.

The switches in step 5 are bits of the battle flags. Internal battle orders set and clear them, and AI order lists and
scripts are what issue those orders.

## How it works

### The check

`0x002FFCF0(actionId, unit)` returns 0 when the action is available and a refusal code
otherwise. It has seven callers: the battle menu `0x0031EB20` (`0x0031F28A`), the menu entry check
`0x00317BC0` (`0x00317C45`), the AI order step `0x003014C0` (`0x003015FF`), action selection `0x00305AB0`
(`0x00305B09`), the effect applier `0x00307300` (`0x00307398`), `0x0030DB70` (`0x0030DBBE`) and the running-action
check `0x002FFB60` (`0x002FFC7C`, its reason 6). In order:

1. Code 2 when the unit lacks bit `0x10` of its first byte or a stats record, when it has status bit `0x1`, `0x2` or
   `0x80000000` and `0x00377C20()` is 0, or when it is on the enemy side and the byte at `[unit+0x6A0]` has any of
   bits `0x8`, `0x10`, `0x20` or `0x40` (`0x30` or `0x48`).
2. Code 4 when `0x00322C50(0x14, id, 1)` rejects the id (returns 0, `0x002FFD75`-`0x002FFD94`).
3. Code `0x24` for a party-side unit without Confuse or Berserk (status `0x08000020`) while
   `0x00253B90()` is 1 (FLEEING, `0x01E0C2B8` = 0), unless the id is `0x113` (Dismiss) or `0x95` (Dismount).
4. Code `0x2C` for ids `0x106`-`0x112` (the summons) while `0x0030D9A0()` is 1 - bit `0x1` of
   `[0x02EBF190]+0x5B04`, which the summon scene sets ([Quickenings and summons](quickenings-and-summons.md)).
   `0x0030D9A0` returns 5, 4, 3 (town flag `0x00377C20`), 2 or 1 from bits `0x8`, `0x4`, the town flag, `0x2` and `0x1` of
   that dword, in that priority.
5. **Statuses:** `0x0030E9C0(stats, mask)` with mask `0x8000201B` (status bits `0x1`, `0x2`, `0x8`, `0x10`, `0x2000`, `0x80000000`), or
   `0x8000221B` (adding bit `0x200`) when the row has bit `0x80000` of `+0x0C` or kind byte `+0x1E` = 1 (Magicks).

   With a status in the mask it returns 10 for Silence (bit `0x200`), 7 for Stop (bit `0x8`), 8 for Sleep (bit `0x10`), 11 for
   Disable (bit `0x2000`), 9 for Confuse (bit `0x20`), 12 for Berserk (bit `0x8000000`), else 6 - in that priority; bits `0x20` and `0x8000000` are
   never in the mask here.
6. **Disabled commands:** `0x0031A7B0(stats, id)` - for a party-side unit only - returns `0x16`, `0x17`,
   `0x18` or `0x19` when the row's kind `+0x1E` is 0, 1, 2 or 3 and bit `0x4`, `0x8`, `0x10` or `0x20` of the battle flags
   `0x022C314C` is set. Those bits are set and cleared by the battle orders `0x413B`-`0x413E` /
   `0x4143`-`0x4146` ([Battle orders](battle-orders.md)).
7. **Ownership and license:** `0x00306480(id, stats, flag)` returns `0x2C` for a null stats record
   (`0x00306490`-`0x00306495`), `0x0F` when `0x003060E0(id, stats, flag)` returns non-zero,
   `0x10` when the license check `0x00323EC0` returns 0, else 0. It hands its own third argument on unchanged
   (`0x003064A6`): 0 from the calls at `0x002FFE9D`, `0x00317BEC`, `0x00317D1D` and `0x0031F941`, 1 from `0x0031FA2B`.
8. **Cost:** `0x00303BD0(unit, id)`.

In step 6, `0x0031A7B0` itself first returns 4 when `0x00322C50(0x14, id, 1)` rejects the id (`0x0031A7D5`), and 0 for a
stats record whose kind byte `+0x05` is 1 (`0x0031A7EA`) or a row kind above 3; a null stats record goes on to the
kind test. The row is 0 when the action table slot `0x02EBF138` is 0 or `0x0020E600` resolves its `+0x0C` to null
(`0x0031A837`), and the kind read at `0x0031A839` then faults.

### Action kinds

Byte `+0x1E` of an action row is its kind; the names come from the members of each kind in
`battle_pack.bin`: 0 Attack, 1 Magicks,
2 Technicks, 3 Items, 5 summons, 6 Quickenings, 7 Foecraft, 8 traps, 9 Esper attacks, 10 Concurrences,
and 255 for 56 rows: 47 placeholders named `NOT USED` or Reserve, and nine named rows, Do nothing. (`0x92`),
Mount (`0x94`), Dismount (`0x95`), `sousachange` (`0x98`), three Mist Charge rows (`0xF2`-`0xF4`), Chain Bonus
(`0xF5`) and Dismiss (`0x113`) ([Action list](action-list.md)).

### Ownership

`0x003060E0(id, stats, flag)` returns 4 when `0x00322C50(0x14, id, 1)` rejects the id (`0x0030610D`-`0x00306116`). It
checks ownership for the party side only; enemies and a null stats record pass (`0x00306120`-`0x0030612F`). Kind 0 and 255
pass. Kinds 1,
2, 5 and 6: a guest (type id `0x07`-`0x19`) or Esper (`0x1B`-`0x27`) passes when the row's ability id
`+0x22` is one of the ten `i16` at `+0x58` of its record in the table at `0x02EBF130`; anyone else when
`0x0030B0E0(+0x22)` (the owned count for that id class, through the handler table at `0x01EEBD10`) is above
0.

Kind 3 with `flag` 0: `0x003037A0` (below), for the unit `0x0031B860` finds for the stats record (`0x003061EE`-`0x003061FC`).
Kind 3 with `flag` non-zero: a row `+0x22` of `0xFFFF` passes, and any other passes when `0x00309B60(+0x22, 0)` is
above 0, else `0x0F` (`0x003061B1`-`0x003061CF`). Kind 9: only an Esper passes. Kind 4 and every kind from 7 to 254
other than 9 return 5, among them the shipped kinds 7, 8 and 10 (`0x003061A3`, `0x003062F4`-`0x00306300`).

`0x00306480` turns any non-zero result into `0x0F`. `0x003093B0(row)` returns a kind-3 row's `+0x22`, and `0xFFFF`
for any other kind or a null row; the battle menu `0x0031EB20` asks it (`0x0031F090`).

### License

`0x00323EC0(stats, id)` returns 0 when `0x00322C50(0x14, id, 0)` rejects the id (`0x00323ED2`-`0x00323EE9`). It passes
(returns non-zero) for a null stats record and for anyone other than a main party
member (stats `+0x05` = 0 and type id below 7), and for rows with bit `0x2000` of `+0x2C`. For the
Quickenings (`0xD0`-`0xE1`) a main party member passes when the Quickening's index in the character's
record (`0x0030A330`) is below `0x00324020(stats)`; for any other row the License Board check
`0x00323BB0(stats, 1, id)` decides.

### Cost

`0x00303BD0(unit, id)` returns 0 for a null unit (`0x00303BE3`); otherwise it checks the costs in this order and
returns the first code that applies, or 0 when no test refuses (`0x00303CAC`):

| Code | Test |
|---:|---|
| `0x12` | `0x003037A0`: for a party-side unit, the item the action uses (`0x003093D0(id)`, not `0xFFFF`) has an owned count of 0 (`0x0030B0E0`) and is not the item already set aside at `+0xDC8` |
| `0x13` | MP: the `i16` at stats `+0x4C` is below `0x00309110` - for kinds other than 5 and 6, the row's byte `+0x0A` adjusted by `0x002F95D0`, or 0 when the unit pays with gil |
| `0x14` | Mist charges: the byte at stats `+0x4E` is below `0x00308FF0` - the row's byte `+0x0A` for kinds 5 and 6, else 0 |
| `0x15` | gil: for a party-side unit paying with gil (`0x002F9820`: bit `0x1` of the augment layer bytes `+0x6C` or `+0x7C`, augment 32 (Offering), "Enables casting of magicks with gil, rather than MP"), when the cost `0x00309060` is above both the party's gil (`[0x02092758]+8`, `0x00253690`) and the gil already reserved at `+0xE58` |

### Which cost the battle menu shows

For a row with bit `0x20000000` of `+0x0C` (the entry carries a cost), the battle menu `0x0031EB20` asks
`0x002FA140(unit, id)` (90 bytes, called only at `0x0031F033`) which cost to show, and stores the mapped value
at `+0x4C` of its list record:

| `0x002FA140` returns | When | Stored |
|---:|---|---:|
| 0 | the unit's stats record has kind byte `+0x05` = 1 (an enemy) (`0x002FA151`) | 1 (MP) |
| 2 | the id is a summon `0x106`-`0x112` or a Quickening `0xD0`-`0xE1` (`0x002FA15A`-`0x002FA179`) | 2 (Mist charges) |
| 1 | bit `0x1` of stats `+0x6C` or `+0x7C` is set, the same pay-with-gil test as `0x002F9820` (`0x002FA182`-`0x002FA18C`) | 4 (gil) |
| 0 | otherwise | 1 (MP) |

A row with bit `0x80000000` of `+0x0C` stores 3 (the item count) instead.

## Modding notes

- An action's kind is byte `+0x1E` of its row; kinds 1 and 2 decide whether Silence applies (kind 1,
  or flag bit `0x80000`) and which of the battle's command switches covers it.
- Bit `0x2000` of `+0x2C` makes an action need no license.
- The cost byte is `+0x0A` of the row: MP for most kinds, Mist charges for summons and Quickenings.

## Related

- [Battle orders](battle-orders.md) - the orders that switch commands off and on.
- [Quickenings and summons](quickenings-and-summons.md) - the summon flag behind code `0x2C`.
- [Target selection](target-selection.md) - the menu builder that asks this check.
- [Action phases](action-phases.md) - the running action that asks it again.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status
  names.
- [License check](../Items-Equipment-Shops-And-Licenses/licenses.md)
  - what the License Board check tests.

---

[Target selection →](target-selection.md)
