[Home](../../README.md) / [Damage and battle formulas](README.md) / Weapon formulas

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Weapon formulas: each weapon type's damage recipe, bow, crossbow and gun rules, critical hits, and the Numerology, Traveler, Knot of Rust and Gil Toss recipes | system | Damage and battle formulas | Damage and formulas | Which damage recipe each weapon class uses and the formula it runs: the stat scale per weapon type, the 12.5 % Attack Power variance, the random axe and hammer finisher, guns ignoring Defense and the evade bands, bows and crossbows losing accuracy in strong wind (wind class 2) unless the wielder has augment 2, the ranged critical hit, unarmed attacks, and the four action recipes whose damage is not a stat formula: the Numerology streak, the Traveler walk, the Knot of Rust and Dark Matter bank, and Gil Toss. | 0x00385F60, 0x0038AAF0, 0x0038A110, 0x0038A1F0, 0x0038A2D0, 0x0038A3A0, 0x0038A470, 0x0038A680, 0x0038AE50, 0x0038DB50, 0x00389140, 0x00389C60, 0x0038EBE0, 0x0038D970, 0x0038ED40 |

## What the player sees

A weapon's damage depends on its type. Every type adds Attack Power and subtracts the target's Defense,
then multiplies by a scale built from the wielder's level and one or two stats:

| Weapon type | Scale built from | Against |
|---|---|---|
| swords, greatswords, spears, rods, crossbows | Strength and Strength | Defense |
| daggers, ninja swords, bows | Strength and Speed | Defense |
| katanas, staves, and the sword Kumbha | Strength and Magick Power | Defense |
| axes, hammers, hand-bombs | Strength and Vitality, with a random share | Defense |
| poles | Strength and Strength | Magick Resist |
| maces, and the sword Joyeuse | Magick Power and Magick Power | Defense |
| guns, measures, and the Healing Rod, Rod of Faith, Excalipur and Bonebreaker | Attack Power alone | nothing |
| unarmed | Strength and Strength, without the base of 1 | Defense |

- **Guns and measures** ignore Defense, and their hit is not tested against block, parry or evade.
- **Bows and crossbows** lose accuracy in strong wind (wind class 2: the area's MWeather wind preset is 4 or more;
  [Weather](../World-Areas-And-Travel/weather.md)) unless the wielder has augment 2, which the Cameo
  Belt carries, and they can score critical hits that double the damage, as guns can.
- **Axes, hammers and hand-bombs** deal a random share, from nothing up to the full amount.

The formula is chosen by the weapon's own row: an Attack has no formula of its own, so the game uses the recipe number
in the main-hand weapon's equipment row. Ammunition adds its Attack and its element to the bow, crossbow, gun or
hand-bomb that fires it.

## How it works

### Which recipe a weapon uses

An Attack has recipe byte 0, so the resolver takes the recipe from byte `+0x19` of the main-hand
weapon's equipment row (`0x00385F60`, at `0x003861FD`). Each recipe's committed list contains one
preparation slot that sets the attack value `0x02AEE058`, the defence value `0x02AEE05C` and the scale
`0x02AEE054`. The finisher then deals `(attack - defence) * scale` ([Elements](elements.md) has the finisher
`0x0038D280`).

| Recipe | Weapon classes in the shipped rows | Preparation slot |
|---:|---|---|
| 20 | 1 (Broadsword), 2 (Claymore), 5 (Javelin), 13 (Rod); and rows the party cannot hold: 11 Reserve rows the Espers wield (class 0: 181, 183-185, 187-191; class 5: 179, 180) and 39 rows named `NOT USED` from 420 on (classes 1, 2, 5 and 6, row 455 among them), 34 of them enemy weapons, row 484 a weapon of Reddas's scenario presets, and four more (rows 440, 445, 446 and 486) | 65 `0x0038AAF0` |
| 21 | 4 (Ashura), 12 (Dagger) | 66 `0x0038A110` |
| 22 | 3 (Kotetsu), 14 (Oak Staff), 1 (Kumbha) | 67 `0x0038A1F0` |
| 23 | 10 (Handaxe), 11 (Iron Hammer), 17 (Hornito); also one class-0 row named Reserve | 68 `0x0038A2D0` |
| 24 | 6 (Oaken Pole) | 69 `0x0038A3A0` |
| 25 | 7 (Shortbow); also three class-8 (crossbow) rows named Reserve or `NOT USED` (186, 458, 490) | 66 `0x0038A110` |
| 26 | 8 (Bowgun) | 65 `0x0038AAF0` |
| 27 | 9 (Altair), 16 (Gilt Measure), and Healing Rod, Rod of Faith, Excalipur, Bonebreaker | 70 `0x0038A470` |
| 29 | 0 (Unarmed) | 72 `0x0038A680` |
| 104 | 15 (Mace), and Joyeuse | 79 `0x0038AE50` |
| 64 | 58 rows from 420 on, all named `NOT USED`: 57 of class 0 and one of class 9 (gun) | 76 `0x0038AAF0` |

The ammunition classes 23-26 have recipe 0: the main hand's bow, crossbow, gun or hand-bomb supplies the recipe.
Equipped ammunition adds to the swing in two ways. Its Attack, byte `+0x1A` of its row, goes into Attack Power
through equipment group 1 in the stats rebuild (`0x002FF495`-`0x002FF499`; [Equipment row](../Items-Equipment-Shops-And-Licenses/equipment-row.md)),
and its element is the attack's ([Elements](elements.md)).

### The stat scale

With `Lv` the wielder's level `+0x1C2` and the stats from the stats record ([Stats](stats.md)):

```python
slot 65, 76   scale = 1 + Str * (Lv + Str) / 256        0x0038AAF6-0x0038AB3F
slot 66       scale = 1 + Str * (Lv + Spd) / 218        0x0038A116-0x0038A163
slot 67       scale = 1 + Str * (Lv + Mag) / 256        0x0038A1F6-0x0038A243
slot 68       scale = 2 * Str * (Lv + Vit) / 256        0x0038A2D6-0x0038A31F
slot 69       scale = 1 + Str * (Lv + Str) / 256        0x0038A3A6-0x0038A3EF
slot 79       scale = 1 + Mag * (Lv + Mag) / 256        0x0038AE56-0x0038AE9F
slot 72       scale = Str * (Lv + Str) / 256            0x0038A68F-0x0038A6C5
```

The divisions are float multiplications by 1/256 (`0x009088D8`), or a division by 218.0 (`0x00D112D0`).

### Attack, variance and defence

Every preparation slot except 70 takes Attack Power `+0x2E` plus a variance, and so does slot 72 except with
Brawler and an empty off hand, where the attack is built from level and Strength instead ([Unarmed](#unarmed)):

```python
variance = (MT19937 % (int)(AP * 0.125 * 100)) / 100      0 when AP * 0.125 < 0.01
attack = AP + variance                                   so AP <= attack < 1.125 * AP
```

The defence is the target's Defense `+0x2F`, except slot 69 (poles), which takes Magick Resist `+0x30`
(`0x0038A446`).

### Guns and measures

Slot 70 (`0x0038A470`) puts Attack Power plus a variance in both the scale and the attack, each with its own
draw, and stores a defence of 0 (`0x0038A4C1`-`0x0038A57D`):

```python
damage = (AP + variance1) * (AP + variance2)
```

Recipe 27's outcome step is slot 44 (`0x00389A50`). It rolls only the hit chance against `MT19937 % 100`
(`0x00389A59`-`0x00389A72`). The melee step 41 (`0x003896B0`) and the bow step 42 (`0x00389820`) also test the
target's shield, weapon and innate evade bands (`0x02AEDFF0`, `0x02AEDFF4`, `0x02AEDFEC`), and the crossbow step
43 (`0x00389950`) the shield and weapon bands, but only when the target's battle unit has bit `0x800000` of its first
dword (`0x003896C0`-`0x003896DD`, the same test at `0x00389847` and `0x00389977`); otherwise they make the same
plain hit roll as slot 44.

### Axes, hammers and hand-bombs

Recipe 23 uses slot 126 (`0x0038DB50`) in place of 125; slots 165, 171, 176 and 182 still follow. It works like
`0x0038D280` but replaces the scale with a random share of it (`0x0038DBF7`-`0x0038DC48`):

```python
share = (MT19937 % (int)(scale * 100)) / 100        0 when scale < 0.01
damage = (attack - defence) * share
```

### Unarmed

Slot 72 checks Brawler (augment 9; context `+0x1B` bit `0x2`, `0x0038A6B1`).
With that augment and nothing in the off hand (word `+0x52` is `0x1000` or not an item), the attack is
half of `Lv + Str` plus a 12.5 % variance (`0x0038A6B1`-`0x0038A77B`). Otherwise it is Attack Power plus the
variance (`0x0038A785`-`0x0038A7EE`).

The Brawler variance is drawn on `Lv + Str` as the other one is on Attack Power, and the half is taken of the sum,
`(Lv + Str + variance) * 0.5` (`0x0038A70D`-`0x0038A773`). An off-hand word that is not an item is one at or above
`0x1000` plus the equipment table's row count `+0x04` (`0x0038A6D3`-`0x0038A6ED`).

### Bows and crossbows in strong wind

The first list of recipe 25 runs slot 35 (`0x003895D0`) and that of recipe 26 slot 36 (`0x00389610`). When
the wielder lacks augment 2 (Accuracy Boost) (context `+0x1A` bit `0x4`) and the wind class `0x02099DAC` is 2, they scale the hit
chance `0x02AEDFE0`. The Cameo Belt (equipment row 372, class 21) has augment byte `+0x1A` = 2:

| Slot | Weapons | Hit chance factor | Sites |
|---:|---|---:|---|
| `35` | bows | 0.8 (`0x008F3108`) | `0x003895D4`-`0x003895FC` |
| `36` | crossbows | 0.5 (`0x01CEBB70`) | `0x00389614`-`0x00389630` |

### Critical hits

Recipes 25, 26 and 27 start their committed list with slot 29 (`0x00389140`); the other weapon recipes
have slot 28, the empty `0x0016D6A0`. Slot 29 sets result `+0x18` bit `0x1` when byte `+0x1C` of the main-hand
row is above `MT19937 % 100` (`0x003891B3`-`0x003891D9`). Slot 98 (`0x0038BE00`) then doubles the scale when that
bit is set (`0x0038BE04`-`0x0038BE1A`).

A main-hand word at or above `0x1000` plus the equipment table's row count `+0x04` gives slot 29 a chance of 0, so
no critical, though the roll is still drawn (`0x0038916A`-`0x00389176`, `0x003891B7`).

### Numerology

Recipe 56 (action `0xB0`, Numerology) runs slot 49 (`0x00389C60`) and slot 144 (`0x0038EAF0`). The count is byte
`+0x5B0E` of the party block `[0x02EBF190]`:

1. The hit chance becomes `row[+0x12] - count * count / 4` (`0x00389D0B`-`0x00389D19`).
2. With a stored preview (bit `0x1` of the user's 64-byte record `+0x12`) and a count below 17, a roll under
   that chance writes `count + 1` into result `+0x138`; a miss or a count of 17 or more writes 0 and fails
   the action (`0x00389D24`-`0x00389DAE`). Without a stored preview it fails at count 0, and at a higher count
   rolls the hit chance, writes no new count and fails the action on a miss (`0x00389D7E`-`0x00389DAE`).
3. Both rolls compare the chance with the roll as unsigned 32-bit numbers (`0x00389D48`-`0x00389D4F`,
   `0x00389D9B`-`0x00389DA2`), so a chance below 0, from a row byte below `count * count / 4`, reads as a number
   above 99 and the roll hits.
4. Slot 144 deals `2 ^ count`, the count before this use (`pow(2.0, count)`, `0x0038EAF4`-`0x0038EB1B`).

`0x00385BA0` copies result `+0x138` into `+0x5B0E` afterwards (`0x00385BAF`-`0x00385BD1`), so the damage runs 1,
2, 4 and so on up to 65,536.

### Traveler

Recipe 60 (action `0xB4`, Traveler) runs slot 146 (`0x0038EBE0`). `0x00320D50` returns the walked distance in
the party block (`+0x5AC8` and `+0x5ACC`):

```python
d = ((total % 1000) - [+0x5B00] + 1000) % 1000            0x0038EC49-0x0038EC93
damage = 10*d if d >= 990, 3*d if d >= 500, 2*d if d >= 100, else d      0x0038ECC3-0x0038ED01
```

It stores `total % 1000` in result `+0x13C` (`0x0038ECBC`), which `0x00385BA0` moves into `+0x5B00`
(`0x00385BD7`-`0x00385BEA`). Without a stored preview it deals the record's last value again (`0x0038ED17`).
The damage goes to the HP loss `0x02AEE004` and into the dword `+0x00` of the user's 64-byte record
(`0x0038ECD5`-`0x0038ECD7`, `0x0038ECFF`-`0x0038ED01`), the value a later use without a stored preview deals again.

### Knot of Rust and Dark Matter

Recipe 16 (Knot of Rust `0x91`, Devour Soul `0xC4`) runs slot 121 (`0x0038D970`), recipe 17 (Dark Matter
`0x90`, Soul Purge `0xC5`) slot 122 (`0x0038DA00`):

- **Deposit:** the user's max HP (doubled under Bubble; under Disease its current HP, at least 1) divided
  by `MT19937 % 10 + 1` is the damage, and a third of it is added to the bank, at most 60,000
  (`0x0038D976`-`0x0038D9F2`). The bank is the word `rustBank` at `+0x5B0C` of the party block `[0x02EBF190]`
  (`0x0038D9C1`, `0x0038D9DE`; [Party data](../Party/party-data.md)), one bank for every user.
- **Withdrawal:** with a stored preview, the bank moves into the user's record and is emptied; the damage
  is the record's value (`0x0038DA49`-`0x0038DA6A`).
- **Which row:** `0x0038DA00` takes its argument as the user's record when it is not null and its byte
  `+0x05` is 0; the row is then `0x0208D480 + 64 × byte +0x04` (`0x0038DA04`-`0x0038DA1C`, `0x0038DA3D`).
  Otherwise it calls `0x0031B860`, stores the answer in `0x02EBF188` and takes the row
  `0x0208DE80 + 64 × byte +0xEA9` of the answer (`0x0038DA1E`-`0x0038DA41`).

  A null answer is not passed over: its dword at address 0 is read for `0x02AEE004`
  (`0x0038DA2A`-`0x0038DA2D`, `0x0038DA75`). Without bit `0x1` of the row's byte `+0x12` the bank is left
  as it is and the row's first dword alone goes to `0x02AEE004` (`0x0038DA49`-`0x0038DA4D`,
  `0x0038DA68`-`0x0038DA6A`). With the bit, the row's first dword takes the bank word zero-extended
  before the bank is set to 0 (`0x0038DA4F`-`0x0038DA61`).

### Gil Toss

Recipe 61 (action `0xB5`, Gil Toss) has slot 18 (`0x00388D50`) in its first list and slot 147 (`0x0038ED40`) in
its committed list:

1. For the user's current target (`+0x710`), slot 18 sums the current HP of the four party slots that are
   not KO, Stone or X-Zone, up to 10,000 (`0x00388DEE`-`0x00388E21`).
2. When that is more than the party's gil, the action fails and sets result `+0x140` bit `0x800`
   (`0x00388E24`-`0x00388E45`); otherwise the sum goes into the user's record and result `+0x08`, the gil cost
   (`0x00388E51`-`0x00388E57`). For every other target slot 18 copies the stored sum into result `+0x08`
   (`0x00388E5C`-`0x00388E62`).
3. Slot 147 deals the record's value divided by the user's target count `+0x77C`, and fails when there
   are no targets or the share is 0 (`0x0038EDB4`-`0x0038EDFF`). A user without a battle unit fails too (`0x0038EDB2`);
   failing sets `0x02AEDFBC` (`0x0038EDFF`) and writes no HP loss, and the share goes to the HP loss `0x02AEE004`
   (`0x0038EDDF`).
   - Every call, failing or not, stores the user's battle unit from `0x0031B860`, or 0, at `0x02EBF188`
     (`0x0038EDA8`, before the failure tests; also `0x0038ED7A` and `0x0038EDC4`).

## Modding notes

- A weapon's recipe is byte `+0x19` of its equipment row; giving a sword recipe 27 makes it ignore
  Defense and evasion.
- The 12.5 % variance and the 1/256 and 1/218 factors are constants in `.rdata` (`0x00915508`, `0x009088D8`,
  `0x00D112D0`) that other slots share.
- A weapon's critical chance is byte `+0x1C` of its row; only recipes 25-27 read it.
- The strong-wind factors are the floats at `0x008F3108` and `0x01CEBB70`, both shared.

## Related

- [Elements](elements.md) - the finisher and the weapon element stage.
- [Stats](stats.md) - where Strength, Speed, Attack Power and the evades come from.
- [Steal](steal.md) - another recipe end to end.
- [Action definition row](../Battle-Actions/action-definition-row.md) - the recipe byte of an action.
- [Combos](../Battle-Actions/combos.md) - the combo hits of melee weapons.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Items equipment shops license: `0x0031B860` is called by `0x0031A410`, `0x0031A510`, `0x0031A630`, `0x00323910`; those
  functions are documented on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Movement: `0x0031B860` is called by `0x0033CB10`, `0x0033D890`; those functions are documented on
  [status timers](../Status-Effects-And-KO/status-timers.md),
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md).
- Rewards progression economy: `0x0031B860` is called by `0x002F8BB0`, `0x0030C650`; those functions are documented on
  [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).

---

[← Elements](elements.md) | [HP and KO →](hp-and-ko.md)
