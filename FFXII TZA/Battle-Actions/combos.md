---
title: "Combos: combo chance, the hit-count roll, low-HP bonus and how each extra hit is re-committed"
kind: "system"
category: "Battle actions"
addresses: "00388550, 00388660, 0030FA00, 0030C010, 00308610, 00307300, 00385680, 003105D0"
---

## What the player sees

A weapon attack can turn into a **combo**: the same attack lands again and again on the same target.
Whether a combo happens, and how many hits it has, is decided once, on the first hit.

- **The chance** comes from the weapon: a combo byte on the weapon's equipment row, times 0.7 as a
  percentage (a byte of 20 gives a 14 % chance). With the Genji Gloves equipped (augment 13) the byte is
  multiplied by 1.8 instead, so a byte of 56 or more
  makes every attack a combo.
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

## How it works

### Where the decision is made

Before a weapon attack resolves, the preview pass `00385680` runs the first slot segment of the
action's formula recipe (the recipe table at `01EF96C0`, slot functions at `01EFA5C0`;
`003859BD`-`00385A16`). For every recipe that contains slot 10 (20-24, 28, 29, 64, 103 and 104) that
segment is slots 5, 6, 7, 8, 9, 10, 22, 33, 34 and 41. Recipe 103 is chosen by 10 monster action rows
such as Ram, Gnaw and Rake, the others by weapons. Slot 9 is the combo chance and slot 10 the combo
roll.

Before running the slots, when the target being previewed is the unit's current target (`+710`<sub>h</sub>
through `00320A70`, or on the stats-record path the first `+6B9`<sub>h</sub> entry through `00320A40`),
`00385680` clears the first `14`<sub>h</sub> bytes of the unit's 64-byte record, keeping the `u16` at `+10`<sub>h</sub>. It
puts back the high nibble of `+12`<sub>h</sub> (read at `0038579C`) while the unit's combo counter `+6B7`<sub>h</sub> is
non-zero, and sets bit 0 of `+12`<sub>h</sub> (`003857A1`-`003857DD`).

### The chance, slot 9

`00388550(stats, target, context)` reads the attacker's weapon id at stats
`+50`<sub>h</sub>; when it is below the equipment table's count plus `1000`<sub>h</sub> (table `02EBF0F8`), the threshold is
`(int)(byte +1Ch of the equipment row * 0.7)` (`008F3104`), or `* 1.8` (`00908E1C`) when bit 5 of the
evaluation context's byte `+1B`<sub>h</sub> (merged augment 13) is set (`0038855F`). It is stored at
`02AEDFE4` (`00388648`). An id outside the table gives 0.

### The roll, slot 10

`00388660(stats, target, context)` (602 bytes):

1. It finds the attacker's battle unit (`0031B860`) and reads its counter `+6B7`<sub>h</sub> (`0038868A`). The
   record is `0208D480 + stats[+04h] * 40h` for a party-side attacker (stats `+05`<sub>h</sub> = 0), otherwise
   `0208DE80 + unit[+EA9h] * 40h` (`003886A7`-`003886E1`). Result flag bit 1 at
   `[context+10h]+18h` is cleared (`003886F1`).
2. **Counter 0 - the first hit.** One draw from the Mersenne Twister (`00379CD0`) modulo 100 must be
   below `02AEDFE4`, else there is no combo (`003886FD`-`0038871D`). The count is then rolled as shown
   below, and when `c >= 1` it is stored in the high nibble of the record's byte `+12`<sub>h</sub> and result flag
   bit 1 is set (`00388850`-`00388876`).
3. **Counter above 0 - a later hit.** No draw: result flag bit 1 is set when the counter is below the
   stored nibble (`0038886B`-`0038887A`).
4. Whenever bit 1 ends up set, the knockback decision `02AEDFC8` and the guard decision `02AEDFC4`
   are zeroed (`00388891`-`003888AB`); see below.

### The extra-hit count

The per-roll chance comes from the attacker's HP (`00388723`-`003887D6`), with `cur` = stats `+48`<sub>h</sub>
and `max` = `max(cur, 1)` when status bit 16 is set, else `+24`<sub>h</sub> (doubled under status bit 28):

| Current HP | Chance per roll |
|---|---:|
| below `max / 16` | 64 % (`40`<sub>h</sub>) |
| below `max / 8` | 32 % (`20`<sub>h</sub>) |
| below `max / 4` | 16 % (`10`<sub>h</sub>) |
| otherwise | 8 % |

The divisions are signed and truncating. The count is then:

```python
n = 1
repeat 11 times: if MT() % 100 < chance: n = n + 1  # 003887DA-00388807
enemy-side attacker: n = min(n, byte [[unit+0xE68]+0x20] - 1)  # 00388827-0038884D
c = min(n, 11)
```

### Guard and knockback on combo hits

Slot 6 (`00388440`) sets the knockback decision `02AEDFC8` on a draw below `02AEDFD8`, made only when
bit 0 of context bytes `+68`<sub>h</sub> and `+78`<sub>h</sub> is clear. Slot 8 (`003884F0`) sets the guard decision
`02AEDFC4` on a draw below `02AEDFDC` for a target whose unit has flag bit 23.

Slot 41 (`003896B0`) runs after slot 10 and reads both: `02AEDFC4` turns outcome codes 1 and 3 into 2
and 4, and `02AEDFC8` sets result flag bit 3. Because slot 10 zeroes both whenever the combo
continues, no hit that is followed by another combo hit takes either effect.

### From the result to the target entry

The effect applier `00307300` copies result flag bit 1 to bit
10 (`400`<sub>h</sub>) of the target entry's flags, unless bit 21 of the attacker's word `+04`<sub>h</sub> is set
(`003075D3`-`003075E0`).

### Continuing

The combat frame `00308610` calls `0030FA00` after the action state step `00307BE0` returns non-zero,
when all of these hold (`00308768`-`0030879F`):

- the attacker has Confuse or Berserk (status `08000020`<sub>h</sub>) or is not fleeing (`00253B90()` returns
  0, that is `01E0C2B8` is non-zero);
- the first target entry exists (unit `+780`<sub>h</sub>) and its flags have bit 10.

`0030FA00` (146 bytes) asks the gate `0030C010`;
when it passes, it commits the same action again - `0030F760(unit, [+708h], [+714h], [+710h], 1)` -
and on success increments `+6B7`<sub>h</sub>, restores `+6B8`<sub>h</sub> and sets the action phase `+6B4`<sub>h</sub> to 5
(`0030FA3B`-`0030FA80`).

### The gate

`0030C010` (179 bytes) returns 1 only when: the fleeing test above passes again; the
first target entry exists with flag bit 10; unit bit 22 is clear; the target `+710`<sub>h</sub> resolves to a unit
with a stats record that has none of status bits 0, 1 and 31 (or `00377C20()` is non-zero); when bit 0 of
`02089340` is set, `00237670(unit id)` is non-zero; and the special-sequence state `022C2160` is 0 or 7
(`0030C016`-`0030C0B0`).

### The hit count

The effect applier `00307300` counts the hits of action `96`<sub>h</sub> in `+6B8`<sub>h</sub>. For a target whose
entry code is 0 it adds 1 and, once the count is above 1, passes the unit id and the count to
`0028E920`, which hands them to the HUD object at `[0209BE80] + 5380h` through `00289D70`
(`0030761D`-`00307676`, `0028E920`). The re-commit in `0030FA00` keeps the count, so it runs across
the whole combo.

### Reset

`003105D0` clears `+6B7`<sub>h</sub> and `+6B8`<sub>h</sub> with one word store (`003106EB`) when the unit's
action is cancelled or reset.

### What the counter blocks

`00325D90`, the navigation-step test, returns 0 while `+6B7`<sub>h</sub> is non-zero
(`00325DDF`). `0023B040` recomputes the party leader's control-suppression bits and, while the leader's
`+6B7`<sub>h</sub> is non-zero, replaces its result with all bits set (`0023B124`-`0023B12D`); the bits go to
`003592C0`, `00359200` and `0026BD40` (`0023B1C0`-`0023B1FA`).

## State

| Field | Width | Meaning | Written by |
|---|---|---|---|
| unit `+6B7`<sub>h</sub> | `u8` | extra hits dealt so far | `0030FA79` (+1); `003106EB` (cleared) |
| unit `+6B8`<sub>h</sub> | `u8` | hits of action `96`<sub>h</sub>, kept across a re-commit | `00307665` (+1); `0030FA65`; `003106EB` (cleared) |
| record `+12`<sub>h</sub> high nibble | u4 | extra hits rolled for this combo | `00388865` |
| `02AEDFE4` | `u32` | combo chance, percent | `00388648` |
| target entry flags bit 10 | bit | continue the combo after this hit | `003075E0` |

## Modding notes

- The combo chance is byte `+1C`<sub>h</sub> of each weapon's equipment row in `battle_pack.bin`. Shipped values
  run from 0 to 100; most weapons have 5 to 30.
- The 0.7 and 1.8 factors are floats at `008F3104` (shared with other code) and `00908E1C`.
- The HP bands are the shifts in `00388660` (16, 8, 4) and the chances the immediates `40`<sub>h</sub>, `20`<sub>h</sub>,
  `10`<sub>h</sub> and 8; the eleven rolls are `mov r14d, Bh` at `003887DA`, which also caps the count.
- An enemy's combo cap is byte `+20`<sub>h</sub> of its class row, minus one; a value of 1 disables its combos.

## Related

- [Area of effect](area-of-effect.md) - the target entry flags, including bit 10.
- [Action range](action-range.md) - how the attacker closes in before the first hit.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status bits
  5 (Confuse), 16, 27 (Berserk) and 28.
- [The R2 modal toggle](../Controls-And-Input/escape.md) - the FLEEING mode
  behind `01E0C2B8`.
- [The formula step table](../Damage-And-Battle-Formulas/damage-formula.md) - the other
  slots of the recipe.
