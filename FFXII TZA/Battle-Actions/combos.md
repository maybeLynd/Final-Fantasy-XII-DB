[Home](../../README.md) / [Battle actions](README.md) / Combos

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Combos: combo chance, the hit-count roll, low-HP bonus and how each extra hit is re-committed | system | Battle actions | How an action runs | How a weapon attack becomes a combo - the chance from the weapon's combo byte (x0.7, or x1.8 with the multiple-hits augment), the extra-hit count rolled once on the first hit with odds that rise as the attacker's HP falls, the caps, how every further hit re-commits the same action, what stops a combo (fleeing, a KO'd target, special sequences) and what a running combo blocks. | 0x00388550, 0x00388660, 0x0030FA00, 0x0030C010, 0x00308610, 0x00307300, 0x00385680, 0x003105D0 |

## What the player sees

A weapon attack can turn into a **combo**: the same attack lands again and again on the same target.
Whether a combo happens, and how many hits it has, is decided once, on the first hit.

- **The chance** comes from the weapon: a combo byte on the weapon's equipment row, times 0.7 as a
  percentage (a byte of 20 gives a 14 % chance). With the Genji Gloves equipped (augment 13) the byte is
  multiplied by 1.8 instead, so a byte of 56 or more
  makes every attack a combo.
- **Weapons that never combo**: a weapon whose damage recipe has no combo roll never combos, whatever
  its byte: every bow, crossbow, gun and measure, and the Healing Rod, Rod of Faith,
  Bonebreaker and Excalipur.
- **The length** is rolled at the same moment: the combo starts with 1 extra hit, and eleven more
  rolls can each add one. Each of those rolls succeeds 8 % of the time at more than a quarter of
  maximum HP, 16 % below a quarter, 32 % below an eighth and 64 % below a sixteenth, so a wounded
  attacker lands far longer combos. A combo has at most 11 extra hits; an enemy's combos are also
  limited by a value in its own class data.
- **Every extra hit is a new commit of the same action** on the same target, so each one is
  resolved like an attack of its own. The combo ends when the stored number of extra hits has
  been dealt, or earlier if the target is KO'd, stoned or X-Zoned, if a special sequence such as a
  Quickening or a summon is running, or if the FLEEING mode is switched on - which stops the combos
  of every unit that is not Confused or Berserk, enemies included.
- While a character is in the middle of a combo it does not take navigation steps, and for the
  party leader the party-control suppression state is forced fully on until the combo ends.

The game also counts the hits of an Attack across the whole combo, and from the second hit on it hands the unit and
that count to the on-screen display (the HUD).

## How it works

### Where the decision is made

Before a weapon attack resolves, the preview pass `0x00385680` runs the first slot segment of the
action's formula recipe (the recipe table at `0x01EF96C0`, slot functions at `0x01EFA5C0`;
`0x003859BD`-`0x00385A16`). For every recipe that contains slot 10 (20-24, 28, 29, 64, 103 and 104) that
segment is slots 5, 6, 7, 8, 9, 10, 22, 33, 34 and 41. Recipe 103 is chosen by 10 Foecraft action rows
such as Ram, Gnaw and Rake, recipes 20-24, 29, 64 and 104 by weapons; no shipped action row and no weapon row names
recipe 28. Slot 9 is the combo chance and slot 10 the combo
roll.

Before running the slots, when the target being previewed is the unit's current target (`+0x710`
through `0x00320A70`, or on the stats-record path the first `+0x6B9` entry through `0x00320A40`),
`0x00385680` clears the first 0x14 bytes of the unit's 64-byte record, keeping the `u16` at `+0x10`. It
puts back the high nibble of `+0x12` (read at `0x0038579C`) while the unit's combo counter `+0x6B7` is
non-zero, and sets bit `0x1` of `+0x12`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003857A1`-`0x003857DD` |

</details>

### The chance, slot 9

`0x00388550(stats, target, context)` reads the attacker's weapon id at stats
`+0x50`; when it is below the equipment table's count plus `0x1000` (table `0x02EBF0F8`), the threshold is
`(int)(byte +0x1C of the equipment row * 0.7)`¹, or `* 1.8`² when bit `0x20` of the
evaluation context's byte `+0x1B` (merged augment 13) is set³. It is stored at
`0x02AEDFE4`⁴. An id outside the table gives 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008F3104` |
| ² | `0x00908E1C` |
| ³ | `0x0038855F` |
| ⁴ | `0x00388648` |

</details>

### The roll, slot 10

`0x00388660(stats, target, context)` (602 bytes):

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It finds the attacker's battle unit and reads its counter `+0x6B7`. The record is `0x0208D480 + stats[+0x04] * 0x40` for a party-side attacker (stats `+0x05` = 0), otherwise `0x0208DE80 + unit[+0xEA9] * 0x40`. Result flag bit `0x2` at `[context+0x10]+0x18` is cleared. | `0x0031B860`<br>`0x0038868A`<br>`0x003886A7`-`0x003886E1`<br>`0x003886F1` |
| 2 | **Counter 0 - the first hit.** One draw from the Mersenne Twister modulo 100 must be below `0x02AEDFE4`, else there is no combo. The count is then rolled as shown below, and when `c >= 1` it is stored in the high nibble of the record's byte `+0x12` and result flag bit `0x2` is set. | `0x00379CD0`<br>`0x003886FD`-`0x0038871D`<br>`0x00388850`-`0x00388876` |
| 3 | **Counter above 0 - a later hit.** No draw: result flag bit `0x2` is set when the counter is below the stored nibble. | `0x0038886B`-`0x0038887A` |
| 4 | Whenever bit `0x2` ends up set, the knockback decision `0x02AEDFC8` and the guard decision `0x02AEDFC4` are zeroed; see below. | `0x00388891`-`0x003888AB` |

### The extra-hit count

The per-roll chance comes from the attacker's HP¹, with `cur` = stats `+0x48`
and `max` = `max(cur, 1)` when status bit `0x10000` is set, else `+0x24` (doubled under status bit `0x10000000`):

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00388723`-`0x003887D6` |

</details>

| Current HP | Chance per roll |
|---|---:|
| below `max / 16` | 64 % (`0x40`) |
| below `max / 8` | 32 % (`0x20`) |
| below `max / 4` | 16 % (`0x10`) |
| otherwise | 8 % |

The divisions are signed and truncating. The count is then:

```python
n = 1
repeat 11 times: if MT() % 100 < chance: n = n + 1  # 0x003887DA-0x00388807
enemy-side attacker: n = min(n, byte [[unit+0xE68]+0x20] - 1)  # 0x00388827-0x0038884D
c = min(n, 11)
```

### Guard and knockback on combo hits

Slot 6¹ sets the knockback decision `0x02AEDFC8` on a draw below `0x02AEDFD8`, made only when
the target has no Stability: bit `0x1` (augment 0) is clear in both of the target's augment layers, stats
`+0x68` and `+0x78` (`0x00388444`, `0x0038844A`; [Augments](../Damage-And-Battle-Formulas/augments.md)). Slot 8² sets the guard decision
`0x02AEDFC4` on a draw below `0x02AEDFDC` for a target whose unit has flag bit `0x800000`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00388440` |
| ² | `0x003884F0` |

</details>

Slot 41¹ runs after slot 10 and reads both: `0x02AEDFC4` turns outcome codes 1 and 3 into 2
and 4, and `0x02AEDFC8` sets result flag bit `0x8`. Because slot 10 zeroes both whenever the combo
continues, no hit that is followed by another combo hit takes either effect.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003896B0` |

</details>

### From the result to the target entry

The effect applier `0x00307300` copies result flag bit `0x2` to bit
`0x400` of the target entry's flags, unless bit `0x200000` of the attacker's word `+0x04` is set¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003075D3`-`0x003075E0` |

</details>

### Continuing

The combat frame `0x00308610` calls `0x0030FA00` after the action state step `0x00307BE0` returns non-zero,
when all of these hold¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308768`-`0x0030879F` |

</details>

- the attacker has Confuse or Berserk (status `0x08000020`) or is not fleeing (`0x00253B90()` returns
  0, that is `0x01E0C2B8` is non-zero);
- the first target entry exists (unit `+0x780`) and its flags have bit `0x400`.

`0x0030FA00` (146 bytes) asks the gate `0x0030C010`¹;
when it passes, it commits the same action again - `0x0030F760(unit, [+0x708], [+0x714], [+0x710], 1)` -
and on success increments `+0x6B7`, restores `+0x6B8` and sets the action phase `+0x6B4` to 5².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030FA20` |
| ² | `0x0030FA3B`-`0x0030FA80` |

</details>

`0x0030FA00` answers 1 after those three stores and 0 when the gate or the commit answers 0, in which
case it stores nothing itself¹. It reads the bytes
`+0x6B7` and `+0x6B8` before the gate call²: the count stored is that earlier
`+0x6B7` value one higher, kept as a byte, and `+0x6B8` gets back the value read then³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030FA25`-`0x0030FA29`, `0x0030FA61`-`0x0030FA74` |
| ² | `0x0030FA0F`-`0x0030FA19` |
| ³ | `0x0030FA65`-`0x0030FA79` |

</details>

### The gate

`0x0030C010` (179 bytes) returns 1 only when: the fleeing test above passes again; the
first target entry exists with flag bit `0x400`; unit bit `0x400000` is clear; the target `+0x710` resolves to a unit
with a stats record that has none of status bits `0x1`, `0x2` and `0x80000000` (or `0x00377C20()` is non-zero); when bit `0x1` of
`0x02089340` is set, `0x00237670(unit id)` is non-zero; and the special-sequence state `0x022C2160` is 0 or 7¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030C016`-`0x0030C0B0` |

</details>

### The hit count

The effect applier `0x00307300` counts the hits of action `0x96` in `+0x6B8`. For a target whose
entry code is 0 it adds 1 and, once the count is above 1, passes the unit id and the count to
`0x0028E920`, which hands them to the HUD object at `[0x0209BE80] + 0x5380` through `0x00289D70`¹. The re-commit in `0x0030FA00` keeps the count, so it runs across
the whole combo.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030761D`-`0x00307676`, `0x0028E920` |

</details>

### Reset

`0x003105D0` clears `+0x6B7` and `+0x6B8` with one word store¹ when the unit's
action is cancelled or reset.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003106EB` |

</details>

### What the counter blocks

`0x00325D90`, the navigation-step test, returns 0 while `+0x6B7` is non-zero¹. `0x0023B040` recomputes the party leader's control-suppression bits and, while the leader's
`+0x6B7` is non-zero, replaces its result with all bits set²; the bits go to
`0x003592C0`, `0x00359200` and `0x0026BD40`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00325DDF` |
| ² | `0x0023B124`-`0x0023B12D` |
| ³ | `0x0023B1C0`-`0x0023B1FA` |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

| Field | Width | Meaning | Written by |
|---|---|---|---|
| unit `+0x6B7` | `u8` | extra hits dealt so far | `0x0030FA79` (+1); `0x003106EB` (cleared) |
| unit `+0x6B8` | `u8` | hits of action `0x96`, kept across a re-commit | `0x00307665` (+1); `0x0030FA65`; `0x003106EB` (cleared) |
| record `+0x12` high nibble | u4 | extra hits rolled for this combo | `0x00388865` |
| `0x02AEDFE4` | `u32` | combo chance, percent | `0x00388648` |
| target entry flags bit `0x400` | bit | continue the combo after this hit | `0x003075E0` |

</details>

## Modding notes

- The combo chance is byte `+0x1C` of each weapon's equipment row in `battle_pack.bin`. Shipped values
  run from 0 to 100; most weapons have 5 to 30.
- The 0.7 and 1.8 factors are floats at `0x008F3104` (shared with other code) and `0x00908E1C`.
- The HP bands are the shifts in `0x00388660` (16, 8, 4) and the chances the immediates `0x40`, `0x20`,
  `0x10` and 8; the eleven rolls are `mov r14d, 0xB` at `0x003887DA`, which also caps the count.
- An enemy's combo cap is byte `+0x20` of its class row, minus one; a value of 1 disables its combos.

## Related

- [Area of effect](area-of-effect.md) - the target entry flags, including bit `0x400`.
- [Action range](action-range.md) - how the attacker closes in before the first hit.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status bits
  `0x20` (Confuse), `0x10000`, `0x8000000` (Berserk) and `0x10000000`.
- [The R2 modal toggle](../Controls-And-Input/escape.md) - the FLEEING mode
  behind `0x01E0C2B8`.
- [The formula step table](../Damage-And-Battle-Formulas/damage-formula.md) - the other
  slots of the recipe.
