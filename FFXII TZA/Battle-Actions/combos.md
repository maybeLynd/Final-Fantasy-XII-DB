---
title: "Combos: combo chance, the hit-count roll, low-HP bonus and how each extra hit is re-committed"
kind: "system"
category: "Battle actions"
summary: "How a weapon attack becomes a combo - the chance from the weapon's combo byte (x0.7, or x1.8 with the multiple-hits augment), the extra-hit count rolled once on the first hit with odds that rise as the attacker's HP falls, the caps, how every further hit re-commits the same action, what stops a combo (fleeing, a KO'd target, special sequences) and what a running combo blocks."
addresses: ["00388550", "00388660", "0030FA00", "0030C010", "00308610", "00307300", "00385680", "003105D0"]
---

# Combos: combo chance, the hit-count roll, low-HP bonus and how each extra hit is re-committed

## What the player sees

A weapon attack can turn into a **combo**: the same attack lands again and again on the same target.
Whether a combo happens, and how many hits it has, is decided once, on the first hit.

- **The chance** comes from the weapon: a combo byte on the weapon's equipment row, times 0.7 as a
  percentage (a byte of 20 gives a 14 % chance). With the augment whose help text reads "Improves
  chance of scoring multiple hits" the byte is multiplied by 1.8 instead, so a byte of 56 or more
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

Before running the slots, when the target being previewed is the unit's current target (`+0x710`
through `00320A70`, or on the stats-record path the first `+0x6B9` entry through `00320A40`),
`00385680` clears the first 0x14 bytes of the unit's 64-byte record, keeping the `u16` at `+0x10`. It
puts back the high nibble of `+0x12` (read at `0038579C`) while the unit's combo counter `+0x6B7` is
non-zero, and sets bit 0 of `+0x12` (`003857A1`-`003857DD`).

### The chance, slot 9

`00388550(stats, target, context)` reads the attacker's weapon id at stats
`+0x50`; when it is below the equipment table's count plus `0x1000` (table `02EBF0F8`), the threshold is
`(int)(byte +0x1C of the equipment row * 0.7)` (`008F3104`), or `* 1.8` (`00908E1C`) when bit 5 of the
evaluation context's byte `+0x1B` (merged augment 13) is set (`0038855F`). It is stored at
`02AEDFE4` (`00388648`). An id outside the table gives 0.

### The roll, slot 10

`00388660(stats, target, context)` (602 bytes):

1. It finds the attacker's battle unit (`0031B860`) and reads its counter `+0x6B7` (`0038868A`). The
   record is `0208D480 + stats[+0x04] * 0x40` for a party-side attacker (stats `+0x05` = 0), otherwise
   `0208DE80 + unit[+0xEA9] * 0x40` (`003886A7`-`003886E1`). Result flag bit 1 at
   `[context+0x10]+0x18` is cleared (`003886F1`).
2. **Counter 0 - the first hit.** One draw from the Mersenne Twister (`00379CD0`) modulo 100 must be
   below `02AEDFE4`, else there is no combo (`003886FD`-`0038871D`). The count is then rolled as shown
   below, and when `c >= 1` it is stored in the high nibble of the record's byte `+0x12` and result flag
   bit 1 is set (`00388850`-`00388876`).
3. **Counter above 0 - a later hit.** No draw: result flag bit 1 is set when the counter is below the
   stored nibble (`0038886B`-`0038887A`).
4. Whenever bit 1 ends up set, the knockback decision `02AEDFC8` and the guard decision `02AEDFC4`
   are zeroed (`00388891`-`003888AB`); see below.

### The extra-hit count

The per-roll chance comes from the attacker's HP (`00388723`-`003887D6`), with `cur` = stats `+0x48`
and `max` = `max(cur, 1)` when status bit 16 is set, else `+0x24` (doubled under status bit 28):

| Current HP | Chance per roll |
|---|---:|
| below `max / 16` | 64 % (`0x40`) |
| below `max / 8` | 32 % (`0x20`) |
| below `max / 4` | 16 % (`0x10`) |
| otherwise | 8 % |

The divisions are signed and truncating. The count is then:

```
n = 1
repeat 11 times: if MT() % 100 < chance: n = n + 1          (003887DA-00388807)
enemy-side attacker: n = min(n, byte [[unit+0xE68]+0x20] - 1)   (00388827-0038884D)
c = min(n, 11)
```

### Guard and knockback on combo hits

Slot 6 (`00388440`) sets the knockback decision `02AEDFC8` on a draw below `02AEDFD8`, made only when
bit 0 of context bytes `+0x68` and `+0x78` is clear. Slot 8 (`003884F0`) sets the guard decision
`02AEDFC4` on a draw below `02AEDFDC` for a target whose unit has flag bit 23.

Slot 41 (`003896B0`) runs after slot 10 and reads both: `02AEDFC4` turns outcome codes 1 and 3 into 2
and 4, and `02AEDFC8` sets result flag bit 3. Because slot 10 zeroes both whenever the combo
continues, no hit that is followed by another combo hit takes either effect.

### From the result to the target entry

The effect applier `00307300` copies result flag bit 1 to bit
10 (`0x400`) of the target entry's flags, unless bit 21 of the attacker's word `+0x04` is set
(`003075D3`-`003075E0`).

### Continuing

The combat frame `00308610` calls `0030FA00` after the action state step `00307BE0` returns non-zero,
when all of these hold (`00308768`-`0030879F`):

- the attacker has Confuse or Berserk (status `0x08000020`) or is not fleeing (`00253B90()` returns
  0, that is `01E0C2B8` is non-zero);
- the first target entry exists (unit `+0x780`) and its flags have bit 10.

`0030FA00` (146 bytes) asks the gate `0030C010`;
when it passes, it commits the same action again - `0030F760(unit, [+0x708], [+0x714], [+0x710], 1)` -
and on success increments `+0x6B7`, restores `+0x6B8` and sets the action phase `+0x6B4` to 5
(`0030FA3B`-`0030FA80`).

### The gate

`0030C010` (179 bytes) returns 1 only when: the fleeing test above passes again; the
first target entry exists with flag bit 10; unit bit 22 is clear; the target `+0x710` resolves to a unit
with a stats record that has none of status bits 0, 1 and 31 (or `00377C20()` is non-zero); when bit 0 of
`02089340` is set, `00237670(unit id)` is non-zero; and the special-sequence state `022C2160` is 0 or 7
(`0030C016`-`0030C0B0`).

### Reset

`003105D0` clears `+0x6B7` and `+0x6B8` with one word store (`003106EB`) when the unit's
action is cancelled or reset.

### What the counter blocks

`00325D90`, the navigation-step test, returns 0 while `+0x6B7` is non-zero
(`00325DDF`). `0023B040` recomputes the party leader's control-suppression bits and, while the leader's
`+0x6B7` is non-zero, replaces its result with all bits set (`0023B124`-`0023B12D`); the bits go to
`003592C0`, `00359200` and `0026BD40` (`0023B1C0`-`0023B1FA`).

## State

| Field | Width | Meaning | Written by |
|---|---|---|---|
| unit `+0x6B7` | u8 | extra hits dealt so far | `0030FA79` (+1); `003106EB` (cleared) |
| unit `+0x6B8` | u8 | kept across a re-commit | `0030FA65`; `003106EB` (cleared) |
| record `+0x12` high nibble | u4 | extra hits rolled for this combo | `00388865` |
| `02AEDFE4` | u32 | combo chance, percent | `00388648` |
| target entry flags bit 10 | bit | continue the combo after this hit | `003075E0` |

## Modding notes

- The combo chance is byte `+0x1C` of each weapon's equipment row in `battle_pack.bin`. Shipped values
  run from 0 to 100; most weapons have 5 to 30.
- The 0.7 and 1.8 factors are floats at `008F3104` (shared with other code) and `00908E1C`.
- The HP bands are the shifts in `00388660` (16, 8, 4) and the chances the immediates `0x40`, `0x20`,
  `0x10` and 8; the eleven rolls are `mov r14d, 0xB` at `003887DA`, which also caps the count.
- An enemy's combo cap is byte `+0x20` of its class row, minus one; a value of 1 disables its combos.

## Related

- [Area of effect](area-of-effect.md) - the target entry flags, including bit 10.
- [Action range](action-range.md) - how the attacker closes in before the first hit.
- The thirty-two statuses - status bits
  5 (Confuse), 16, 27 (Berserk) and 28.
- The R2 modal toggle - the FLEEING mode
  behind `01E0C2B8`.
- The formula step table - the other
  slots of the recipe.
