[Home](../../README.md) / [Enemy AI and gambits](README.md) / Enmity

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Enmity: the hidden threat table that decides who an enemy attacks, what raises it, how it spreads and how it decays | system | Enemy AI and gambits | Enemy decisions | How each enemy keeps one threat byte per party member: the three enmity numbers every action carries (to the target, spread to other enemies, drawn from the rest of the party), the +10 first-grudge boost and the seeding of every other member, the floor of 1, the decay of 10 every 30 steps while the enemy is not engaged, what KO, Stone, X-Zone and leaving the fight reset, the two orders that change it, and how the enemy AI reads it to pick a target. | 0x003216E0, 0x00321850, 0x003219D0, 0x00321B00, 0x00321530, 0x00321D30, 0x003215C0, 0x00321630, 0x00321770 |

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
other enemies already holding a grudge, and one taken off the target's enmity toward the rest of the party. Among actions, only party members' create enmity; an enemy's own orders `0x4163` and `0x4164` raise its enmity toward
the active party too. Only enemies hold it.

## How it works

### The table

The table lives in the enemy's spawn record at unit `+0x6A0`, from `+0x19`¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00321553`-`0x0032156D` |

</details>

| Byte | Meaning |
|---|---|
| `+0x19` | the decay timer |
| `+0x1A` + *id* | the enemy's enmity toward party table row *id*, 0-255, for *id* 0-39 |

The row id is a party member's type byte (stats `+0x04`). An id counts only when
`0x00322C50(2, id, 1)` accepts it, that is when it is below the 40 rows of the party table `0x02EBF130`¹. The readers return -1 for an invalid id or a missing table, and
`0x003215C0(unit, id)` for a null unit too; otherwise it returns the entry `+0x1A` + *id*².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00322C9A`, `0x0032302A`-`0x0032303B` |
| ² | `0x003215C0`-`0x0032161D`, `0x0032160D` |

</details>

### Writing an entry

`0x00321850(enemy, id, value, mode)` changes one entry¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00321850`-`0x003219CC` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It does nothing unless the enemy is an enemy-table unit (stats `+0x05` = 1, `0x003218D0`) that is not KO, Stone or X-Zone, unless bit `0x8000` of the active field record waives that. A null enemy, one without a table or stats record, or an id `0x00322C50` rejects also changes nothing. | `0x003218A6`-`0x003218BA`<br>`0x00321853`, `0x00321890`, `0x003218A0`, `0x003218F9`-`0x00321900` |
| 2 | The new value is `old + value` for mode 0 or `value` for mode 1, as for any mode other than 0. | `0x00321914`-`0x0032191A` |
| 3 | A new value of 0 or less becomes 1 when the old value was above 0. | `0x0032191D`-`0x00321923` |
| 4 | When the value rises and no entry of the enemy is above 1, it gets 10 more. | `0x00321770`<br>`0x00321927`-`0x0032193A` |
| 5 | The value is stored, limited to 0-255. | `0x00321E40` |
| 6 | When the entry went from 0 to above 0, every other zero entry with a valid id becomes 1. | `0x0032194B`-`0x003219A5` |

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

It is called from `Battle_ProcessActionTarget`¹ and from the special-sequence target loop².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030760A` |
| ² | `0x0030ECF2` |

</details>

### Spreading

`0x003219D0(id, value, target, mode)` walks every unit slot¹ and changes an enemy's entry
for `id` through `0x00321850(enemy, id, value, mode)`, by that function's rules: mode 0 adds `value` and mode 1
writes it². It does so when all of these hold:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003219F4`-`0x00321AD5` |
| ² | `0x00321ABA`-`0x00321AC7` |

</details>

- the unit is an enemy-table unit other than the target¹;
- it has a table and `0x00322C50` accepts `id`²;
- its entry for `id` is already above 0³;
- with a target, the target's actor (`+0x10`) is in the enemy's AI candidate list, the 16-byte entries
  from unit `+0xBC8` counted by `+0xBC4`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00321A33`-`0x00321A40` |
| ² | `0x00321A46`-`0x00321A71` |
| ³ | `0x00321A73`-`0x00321A7B` |
| ⁴ | `0x00321A82`-`0x00321AB8` |

</details>

### Drawing threat off the rest of the party

`0x00321B00(enemy, value, except, mode)` builds the active party list (`0x0030A880(buffer, 1)`, `0x00321B5E`)
and, for every member other than `except`, changes the enemy's entry for that member's type byte by the
same rules as `0x00321850`¹. Unlike `0x00321850`, which returns at once for a null enemy², it reads the enemy's `+0x698` without a test³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00321B90`-`0x00321CF7` |
| ² | `0x00321850`-`0x00321853` |
| ³ | `0x00321B11` |

</details>

`0x0030A880(out, mode)` builds no list itself. It stores the address of the staging list `0x022C1788` at
`out` only when `out` is not null, and then jumps to the builder `0x0030A8A0(0x022C1788, 4, mode)`¹. Every caller is therefore handed the same list, which the next call fills
again.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030A880`-`0x0030A89A` |

</details>

The builder takes its members from the fighting seats alone: for seat 0 to 3 it asks `0x0031B810(seat)`
([Party slots](../Party/party-slots.md)) and passes over a seat with no unit (`0x0030A8D2`-`0x0030A8DF`, back
branch `0x0030A94B`). The mode narrows the list:

- with mode bit `0x4` only a unit whose flag bit `0x10` is set¹;
- with mode bit `0x1` only a unit with a stats record whose dwords `+0x64` and `+0x3C` have none of the bits
  `0x80000003`, or has them while `0x00377C20()` answers non-zero²;
- with mode bit `0x2` only a unit whose stats record is of kind 0 with a type byte `+0x04` of 6 or less
 ³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030A8E1`-`0x0030A8EA` |
| ² | `0x0030A8EC`-`0x0030A911` |
| ³ | `0x0030A913`-`0x0030A931` |

</details>

A unit that passes is counted, and stored in the list when the list pointer is not null and fewer than
`capacity` are stored¹; the count is the answer².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030A933`-`0x0030A943` |
| ² | `0x0030A952` |

</details>

The direct call and jump instructions that have `0x0030A880` as their target are at
`0x00234651`, `0x00234937`, `0x00237EF8`, `0x00237F9B`, `0x0032166A`, `0x00321B5E`, `0x003246E3`, `0x0032666C` and
`0x00326D9A`.

### Decay

The periodic maintenance step `0x00310DB0` calls `0x00321530(enemy)` for each unit¹. For an
enemy-table unit with a table²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003112A4` |
| ² | `0x0032154D`-`0x00321574` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | If the enemy is engaged, the timer is reset to 0 and nothing decays. `0x00307CE0` answers "engaged" when `0x0030C210` or `0x0030BB30` does. | `0x00321576`-`0x0032157D` |
| 2 | Otherwise the timer counts up; when it reaches `30 * [0x01DFE0B8]` steps, `0x00321D30(enemy, -10, 0)` lowers every entry by 10 and the timer restarts. | `0x0032157F`-`0x003215AC` |

`0x01DFE0B8` is the frame base, 1.0 as shipped ([Action phases](../Battle-Actions/action-phases.md)).
`0x00321D30` writes all 40 ids through `0x00321850`¹, so the floor of 1 holds.
It changes nothing for a null enemy, one without a table or stats record, or one that is KO, Stone or X-Zone
without the field record's waiver². Each id goes as `0x00321850(enemy, id, value, mode)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00321D90`-`0x00321DA6` |
| ² | `0x00321D33`-`0x00321D8E` |
| ³ | `0x00321D90`-`0x00321D9C` |

</details>

### Resets and orders

Two more callers change the table:

- **A unit leaving the fight.** `0x00300FC0(unit, flag)` calls `0x003219D0(id, 0, null, 1)` for the unit's
  type byte¹: every enemy holding a grudge against it is set to 1. Teardown calls
  it with flag 1².
- **KO, Stone and X-Zone.** The status write calls `0x00300FC0` with flag 0 when one of them is set: its
  side-effect switch (`0x0030E737`-`0x0030E759`, byte table `0x0030E8C4`) sends statuses 0, 1 and 31 to
  `0x0030E80A`, `0x0030E850` and `0x0030E85E`, which reach `0x0030E877` when the status is being set.
- **Espers keep the table.** With flag 0, an Esper record (party type `0x1B`-`0x27`) leaves `0x00300FC0`
  early through `0x003105D0` and `0x003138D0`³, before the reset. The status write's
  own Esper call at `0x0030E497` takes that exit too.
- **Battle orders `0x4163` and `0x4164`.** The direct state orders call `0x00321B00` on the committing enemy: `0x4163`
  writes 1 (mode 1) and `0x4164` adds the order's parameter (mode 0) to every active party member's entry by those
  rules (`0x002FE4F1`-`0x002FE507`, [Battle orders](../Battle-Actions/battle-orders.md)), so under `0x4163` an entry
  that was 0 becomes 11 when no entry of the enemy is above 1 at that moment⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301048`-`0x0030105E` |
| ² | `0x00300E54`-`0x00300E59` |
| ³ | `0x00300FCF`-`0x00301005` |
| ⁴ | `0x00321C55`-`0x00321C67` |

</details>

### How the AI reads it

The enemy AI's target selector `AiOrder_EvaluateTargetSelector` reads the enmity of a candidate party
member (`0x003215C0`, at `0x00302153`) and compares the candidate with the highest enmity toward any active
party member (`0x00321630`, at `0x00302573`-`0x0030258C`).

`0x00321630` walks the same active party list (`0x0030A880(buffer, 1)`, `0x0032166A`) and returns the highest entry for
a member's type byte, an id `0x00322C50` rejects counting as -1¹. It returns -1 when the
enemy is null or has no table², and when the list is empty³. The relation test
`0x0030BD00` asks `0x00321840` whether an enemy holds any grudge above 0⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00321680`-`0x003216BE` |
| ² | `0x0032163E`, `0x0032165B` |
| ³ | `0x00321674` |
| ⁴ | `0x0030BDA0` |

</details>

## Modding notes

- An action's enmity is the three bytes `+0x1D`, `+0x1F` and `+0x20` of its row; an action with all three
  at 0 leaves the table alone.
- The decay step and interval are `-10`¹ and the 30.0 at `0x008F8D80`, shared with other code.
- Of actions, only a party record's generate enmity; an enemy's orders `0x4163` and `0x4164` raise its own table, and
  only enemy-table units hold one.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032159F` |

</details>

## Related

- [Action definition row](../Battle-Actions/action-definition-row.md) - the three enmity bytes.
- [Battle orders](../Battle-Actions/battle-orders.md) - orders `0x4163` and `0x4164`.
- [Action phases](../Battle-Actions/action-phases.md) - the frame base.
- [Area of effect](../Battle-Actions/area-of-effect.md) - the 16-byte list layout the AI candidate list shares.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 14 calls with 6 other topics</summary>

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00313A00`](../Battle-Actions/action-phases.md) (on action phases) |

**Graphics** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [battle units](../Characters-And-Objects/battle-units.md), [add motion tables](../Graphics/add-motion-tables.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B810`](enmity.md) Battle unit: find mapped definition selector by index | is called by | [`0x00307E70`](../Party/party-slots.md) Party combat: update stance state (on party slots)<br>[`0x00313B30`](../Party/party-slots.md) Battle unit: broadcast party combat target relation (on party slots) |
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00307E70`](../Party/party-slots.md) Party combat: update stance state (on party slots)<br>[`0x003125E0`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: compute presentation suppression mask (on ko and game over)<br>[`0x00313B30`](../Party/party-slots.md) Battle unit: broadcast party combat target relation (on party slots)<br>[`0x003714A0`](../Graphics/add-motion-tables.md) Add motion: apply bone pose (on add motion tables) |

**Scripts and script commands** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [script censuses](../Story-Events-And-Hunts/script-censuses.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00344740`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00352FA0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003537D0`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list)<br>[`0x00355680`](../Story-Events-And-Hunts/script-censuses.md) (on script censuses) |

**Enemy spawning** (explained on [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B810`](enmity.md) Battle unit: find mapped definition selector by index | is called by | [`0x00234DA0`](../Party/party-slots.md) Spawn: validate candidate distance to players (on party slots)<br>[`0x002350C0`](../Enemy-Spawning/enemy-spawning.md) Spawn lifecycle: check and retire by native range (on enemy spawning) |

</details>
