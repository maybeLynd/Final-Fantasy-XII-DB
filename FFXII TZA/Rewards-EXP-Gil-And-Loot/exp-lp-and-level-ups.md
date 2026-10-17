---
title: "EXP, LP and level-ups from kills: who receives them, the formulas, the split, the doublers and the EXP table"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "00312280, 002F8BB0, 002F90C0, 002F8F20, 0023A570, 0028FB80"
---

## What the player sees

When an enemy dies, the party members fighting on the field share its EXP; party members not on the
field get none. Every party member, on the field or not, receives the enemy's full LP.

Equipment effects change this per member:

- "Doubles EXP earned." (Embroidered Tippet);
- "Doubles license points earned." (Golden Amulet);
- "Reduces EXP earned to 0." (Firefly);
- "Convert all license points earned to gil." (Cat-ear Hood).

A game started as New Game Minus earns no EXP at all, though LP and gil are still paid. EXP stops at
99,999,999 and LP at 99,999. A member levels up as soon as their EXP reaches the next level's total;
the last level is 99. While the script's summon mode is on, the whole EXP goes to one unit.

## How it works

### When rewards are paid

`00312280(killer, enemy)`, whose only caller is the status write `0030E360` when it adds KO, Stone or X-Zone
([Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md)), pays EXP and LP only when the defeated unit is an
enemy (stats byte `+05`<sub>h</sub> = 1) whose byte `+E9A`<sub>h</sub> has bit 3 clear, and when at least one of these
holds: `+E9A`<sub>h</sub> has bits 0 and 2 set, or the enemy's status words `+64h | +3Ch` have bit 1 set
while `+E9A`<sub>h</sub> bit 1 is set, or the killer is a party member (killer stats byte `+05`<sub>h</sub> = 0).

### Recipients

It walks the nine entries of party map 3 (`00320AB0(i, 3)`, `i` = 0-8: the selector
bytes at `[02EBF190] + 5A7Eh + i*2` resolved by `0031B9F0` to stat records), and keeps a
record when `(+64h | +3Ch) & 80000003h` is 0 (not out of play), or in any area where `00377C20`
reports the town flag. The list is built at `022C1740`. For each kept record it computes EXP with
`002F8BB0` and LP with `002F90C0`, caps EXP at 999,999 and LP at 999, and applies them (below).

### The enemy's level term

Both formulas use `d = stats.b[+1C2h] - stats.b[+88h]` of the defeated
enemy: its level minus the stats byte `+88`<sub>h</sub> that `0030C470` writes from its third argument for an
enemy record (`0030C4B1`). The enemy carries two reward rows, installed by `0023A570`:
`[+E70h]` is the base row, row `+22`<sub>h</sub> of the table in registry slot `02EBF148` (`0023A9A5`), and
`[+E78h]` is the per-level row, row `+24`<sub>h</sub> of the table in slot `02EBF140` (`0023A9F4`), the row
indices coming from the enemy's definition row.

### EXP

`002F8BB0(recipient, enemy)` computes one recipient's EXP:

```c
amount = d * [E78].i32[+0x34] + [E70].i32[+0x34];
if (battle mode != 1) {                               // 003135C0: 0030D9A0() == 1
    n = members among battle slots 0-3 (0031B810) that are not out of play and are not
        party records with type id 0x1A or 0x1B-0x27;
    exp = n ? amount / n : 0;                         // integer division
} else {
    exp = (recipient == 00320AB0(00313800(), 1)) ? amount : 0;
}
if (recipient.b[+0x6B] & 8 || recipient.b[+0x7B] & 8)     exp *= 2;
if (recipient.b[+0x6B] & 0x20 || recipient.b[+0x7B] & 0x20) exp = 0;
```

A recipient gets 0 unless all of these hold:

- it is a party record (`+05`<sub>h</sub> = 0);
- it has a unit on the field (`0031B860` finds the battle unit whose stats pointer is the record);
- its type id `+04`<sub>h</sub> is outside `1B`<sub>h</sub>-`27`<sub>h</sub>;
- it is not out of play.

The type id is the record's `chr_data` row: 0-6 the main characters, 7-25 guests and story
variants, `1A`<sub>h</sub> the Chocobo and `1B`<sub>h</sub>-`27`<sub>h</sub> the thirteen Espers (see the stat growth page).

Battle mode 1 is bit 0 of `[02EBF190] + 5B04h` with bits 1-3 clear outside town areas
(`0030D9A0`). The script verb `btlAtelSetSummonMode` sets and clears that bit through `00313550`. In
that mode the receiving unit is the one whose id equals byte `[02EBF190] + 5AD5h`, looked up in the
slot table at `+5A48`<sub>h</sub> by `00320890`; it must still pass the recipient gate above, or nobody
receives EXP.

### LP

`002F90C0(recipient, enemy)` computes one recipient's LP:

```c
if (byte 0209A2A9 != 0) return 0;                     // 00264150
lp = d * [E78].u8[+0x2F] + [E70].u8[+0x2F];
if (recipient.b[+0x6B] & 0x10 || recipient.b[+0x7B] & 0x10) lp *= 2;
```

A recipient gets 0 unless it is a party record whose type id is 0-6 (the main characters), `1A`<sub>h</sub> (the
Chocobo) or 40 and above, and that
is not out of play. LP is not divided. Byte `0209A2A9` is set by the script verb
`debug_set_e3demo_status` (`0050CB60` through `0026A580`) and cleared on every area initialisation
(`00266D77` in `00266D10`).

### The effect bits

The four tests read the two 16-byte effect layers at stats `+68`<sub>h</sub> and `+78`<sub>h</sub>, where effect `n` is
bit `n % 8` of byte `+68h + n / 8`. The help texts are the descriptions of the augment table rows in
`battle_pack.bin` (description ids in `listhelp_ability.bin`), and the equipment is the shipped row
whose augment byte `+1A`<sub>h</sub> carries the effect:

| Bit | Effect | Description id | Equipment (augment byte `+1A`<sub>h</sub>) |
|---|---|---|---|
| `+6B`<sub>h</sub> bit 3 | 27 | 13027 | Embroidered Tippet (`1168`<sub>h</sub>) |
| `+6B`<sub>h</sub> bit 4 | 28 | 13028 | Golden Amulet (`116F`<sub>h</sub>) |
| `+6B`<sub>h</sub> bit 5 | 29 | 13029 | Firefly (`1171`<sub>h</sub>) |
| `+69`<sub>h</sub> bit 4 | 12 | 13012 | Cat-ear Hood (`117F`<sub>h</sub>) |

### Applying them

`00312280` then applies both amounts to each recipient:

1. When the recipient's stats byte `+69`<sub>h</sub> or `+79`<sub>h</sub> has bit `10`<sub>h</sub> set, `level × LP × 5` is added to
   the kill's gil and the recipient's LP becomes 0 (see the gil page).
2. Unless bit 14 of `[02EBF190] + 4` is set (`00236780`), EXP is added to `+18C`<sub>h</sub>, capped at
   99,999,999. Bit 14 is New Game Minus: the script verb `btlAtelResetNgMinus` (`308B`<sub>h</sub>, `0050F490`
   jumping to `00238A50`) sets bit 2 of `02089344`, and `00239960` copies it into bit 14 when it applies
   the starting preset (`00239A6C`-`00239A7E`), keeping bits 12-14 across the battle-state reset
   (`002399D7`-`00239A45`).
3. The new level: starting from `+1C2`<sub>h</sub>, the level rises while `002F8F20(level)` is positive and not
   above the EXP total.
4. LP is added to `+190`<sub>h</sub>, capped at 99,999, and metered as counter kind 11 (`00316A50(Bh, LP)`).
5. `0030C650(record, newLevel, 0)` applies the level change.

After the loop, `0028FB80(enemy id, exp, lp)` posts the amounts, clamped to 999,999 and 999, to the HUD's reward display
(`00289D00` on `[0209BE80] + 5380h`, once for EXP and once for LP). It uses EXP and LP computed with no
recipient (`002F8BB0(0, enemy)`, `002F90C0(0, enemy)`): divided as above but never doubled, and EXP
shows as 0 while bit 14 of `[02EBF190] + 4` is set.

### The level table

`002F8F20(L)` returns the EXP total needed to reach level `L + 1`:

```c
if (L == 0) return 0;
if (L > 98) return -1;                                // so level 99 is the last
total = 0;
for (i = 2; i <= L + 1; i++)
    total += (int)(0.4f * i*i*i + 12 * i*i);          // single precision, truncated
```

Values: level 2 at 51, level 3 at 169, level 4 at 386, level 6 at 1,254, level 11 at 7,798,
level 21 at 61,056, level 31 at 223,374, level 51 at 1,249,590, level 71 at 4,075,246, level 91 at
10,073,142, level 99 at 13,741,148.

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| party record `+18C`<sub>h</sub> | `u32` | EXP, cap 99,999,999 | `00312280` |
| party record `+190`<sub>h</sub> | `u32` | LP, cap 99,999 | `00312280` |
| party record `+1C2`<sub>h</sub> | `u8` | level | set to 0 by `0030C470` (`0030C496`); the new level is passed to `0030C650` |
| enemy `+E70`<sub>h</sub> | `void*` | base reward row: `+2F`<sub>h</sub> LP, `+30`<sub>h</sub> gil, `+34`<sub>h</sub> EXP | `0023A9A5` |
| enemy `+E78`<sub>h</sub> | `void*` | per-level reward row, same offsets | `0023A9F4` |
| `0209A2A9` | `u8` | no-LP flag | `0026A580`, `00266D77` |

## Modding notes

- An enemy's EXP, LP and gil come from its two reward rows (`+34`<sub>h</sub>, `+2F`<sub>h</sub>, `+30`<sub>h</sub>), base plus
  per-level times `level - stats.b[+88h]`. Edit the rows in the tables behind registry slots
  `02EBF148` and `02EBF140`, or point the enemy definition's `+22`<sub>h</sub> / `+24`<sub>h</sub> at other rows.
- The level curve is code, not data: `0.4` at `009153EC` and the `12` step built from `18`<sub>h</sub> and `+C`<sub>h</sub>
  in `002F8F20`; the level cap is the `cmp eax, 62h` there.
- The EXP and LP caps per kill (999,999 and 999) and the totals' caps (99,999,999 and 99,999) are
  immediates in `00312280`.

## Related

- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
- [Kill chain: chain count, chain level, the chain coin and resets](kill-chain.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](loot-drops.md)
