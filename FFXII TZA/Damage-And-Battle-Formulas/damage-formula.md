---
title: "Damage formula: how an attack or a magick is resolved, from the hit, evade, block and parry rolls to the final number"
kind: "system"
category: "Damage and battle formulas"
addresses: "0x00385F60, 0x00385680, 0x003847C0, 0x003849B0, 0x003848E0, 0x003896B0, 0x0038B950, 0x0038B010, 0x0038D280, 0x0038F890"
---

## What the player sees

An attack first has to land: the target may evade, block with a shield or parry with a weapon. Then its
damage is the attacker's attack minus the target's defence, times a scale built from level and stats,
with a little randomness.

- **Weapon attacks** scale with Strength and a second stat that depends on the weapon type
  ([Weapon formulas](weapon-formulas.md)); Berserk and Bravery raise them, Protect lowers them, and a
  sleeping target takes 50 % more.
- **Magicks** scale with Magick Power against Magick Resist; Faith raises them, Shell lowers them, and a
  sleeping target takes 50 % more.
- **Augments** such as Adrenaline's (augment 10) add their own multipliers after the status
  multipliers, Oil's ×3 and Float's miss among them, and the element stages apply last
  ([Elements](elements.md)).

## How it works

### The resolver

`0x00385F60(action, source, target, result)` resolves one target (`0x00385F60`-`0x0038685D`). It first finds the
user's memo record (below) and stores the action id in `0x02AEDFD4`; for Shades of Black (`0x9F`) the id
is replaced by the record's word `+0x10` (`0x00385FE4`-`0x00385FF7`). Then:

1. It resets the scratch block with `0x003849B0` (`0x00386001`) and the result record with `0x003848E0`
   (`0x0038600F`).
2. An action outside `0xF5`-`0x105` needs both a source and a target record (`0x00386014`-`0x00386027`). When
   the caller left bit 5 in result byte `+0`, an action without flag bit 11 resolves nothing
   (`0x00386029`-`0x00386087`).
3. An enemy-table target with KO, Stone or X-Zone gets result kind 6 at once (`0x00386091`-`0x003860A7`).
4. It builds the context with `0x003847C0` (`0x003860D5`).
5. It copies bits 1-3 of the memo record's byte `+0x12` into result `+0x18` (`0x003860DF`-`0x00386108`), and
   goes on only when the result kind is 0 or 9, setting it to 0 (`0x0038610B`-`0x0038612D`).
6. It takes the recipe from the action row, or from the weapon for recipe 0 (`0x0038617E`-`0x00386210`).
7. Against a target with KO, Stone or X-Zone, no slot runs (`0x02AEDFB8` = 1) unless the recipe is 1, 2, 3,
   6, 34, 36 or 54, the mask `0x4000140000004E` (`0x00386249`-`0x00386278`). An Esper target at 0 HP is a miss
   (`0x0038627E`-`0x003862A9`).
8. A bit for the target in the memo record's `+0x08` makes result kind 10, a bit in `+0x04` kind 6, before
   any slot (`0x003862B6`-`0x0038634B`).
9. It calls each slot of the recipe's committed list (`0x00386350`-`0x003863E6`), stopping when `0x02AEDFB8` is 1,
   and then `0x00390F20(source, target, &context)` (`0x003863F8`).
10. It clears bit 0 of the memo record's `+0x12` (`0x00386402`) and turns the scratch block into the result
   (below).

### The scratch block

The slots pass their numbers to the resolver through one static block of `0xA8` bytes at `0x02AEDFB8`, laid out
under Layouts. `0x003849B0` resets it before each resolve and each first-list run (`0x00386001`, `0x0038585E`)
(`0x003849B2`-`0x00384B03`):

- -1 ("none") goes into the Mist-charge words `0x02AEDFF8` and `0x02AEDFFC` and the HP, MP, stat, level and poach
  words `0x02AEE004`-`0x02AEE050`, except the steal bytes `0x02AEE04C`-`0x02AEE04E`;
- 0 goes into the flags, chances and bands `0x02AEDFB8`-`0x02AEDFD0` and `0x02AEDFD8`-`0x02AEDFF4`, the word `0x02AEE000`,
  the steal bytes and the scale, attack and defence `0x02AEE054`-`0x02AEE05C`;
- the action id `0x02AEDFD4` and the byte `0x02AEE04F` are left as they are.

### Turning the scratch block into the result

After the slots, the resolver fills the result record from the block (`0x00386406`-`0x00386819`;
[Action results](../Battle-Actions/action-results.md)):

1. A user with KO, Stone or X-Zone keeps none of its own changes: its HP, MP and level words count as -1
   (`0x0038640B`-`0x0038643D`).
2. The presence bits of result `+0x2C` are set from the words that are not -1 (`0x00386474`-`0x00386595`).
3. Each loss and gain word that is -1 is then written back as 0 (`0x0038659C`-`0x0038662A`), so after this step an
   absent value and a 0 look the same.
4. Each change is the gain minus the loss: target HP into `+0x24`, user HP into `+0x20`, target MP into `+0x2A`
   and user MP into `+0x28` (16 bits), Mist charges into `+0x1D` (8 bits) (`0x00386635`-`0x00386664`).
5. A set-outright word that is not -1 replaces its change and sets its bit of `+0x2C`: target HP bit 3, user HP
   bit 1, target MP bit 4, user MP bit 2 (`0x00386669`-`0x003866BE`).
6. `0x02AEDFBC` gives result kind 6 and `0x02AEDFC0` kind 10 (`0x003866C1`-`0x003866D7`); the stat, level, steal and
   poach words are copied (`0x0038679F`-`0x00386819`).

### The memo record

Each user has a 64-byte record that carries the first list's outcome to the committed resolve: for a party
record `0x0208D480 + type * 0x40`, otherwise `0x0208DE80 + unit[+0xEA9] * 0x40` (`0x00385FA0`-`0x00385FDE`). The
target's index is its unit's `+0xEA9`, or its type byte without a unit. A first-list run that ends failed
or immune sets the target's bit in the record's `+0x04` or `+0x08` (`0x00385A7F`, `0x00385AC0`), so the committed resolve gives that
target kind 6 or 10 without running a slot; the combo count lives in the high nibble of `+0x12` (slot 10).

Bit 0 of `+0x12` is the stored-preview flag. When the first list resolves the user's current target (its
`+0x710` target, or the `+0x6B9` slot when `+0x6B6` is set), it clears the record's first `0x14` bytes, keeping
the word `+0x10` and, with unit `+0x6B7` set, the high nibble of `+0x12`, and sets bit 0
(`0x00385733`-`0x003857E1`). The committed resolve clears it (`0x00386402`); Numerology, Traveler, Dark Matter and
Gil Toss read it ([Weapon formulas](weapon-formulas.md)).

### The context

`0x003847C0` fills the context the slots read (`0x003847D4`-`0x003848BC`):

| Context offset | Holds |
|---|---|
| `+0x00` | the action id |
| `+0x02-0x03` | nothing: written only by the builder's qword clear (`0x003847D8`) and read by no instruction; nothing fixes their width |
| `+0x04` | the source's statuses (`+0x64 \| +0x3C`) |
| `+0x08` | the target's statuses |
| `+0x0C-0x0F` | nothing: written only by the builder's qword clear (`0x003847DE`) and read by no instruction; nothing fixes their width |
| `+0x10` | the result record |
| `+0x18` | the target unit's byte `+0x55`, or -1 without a unit |
| `+0x1A-0x29` | the source's 128 augment bits, from both layers `+0x68` and `+0x78` |

Without a target unit, Reverse (status 12) is removed from `+0x08` and augment 15 (Medicine Reverse) from the merged bits
(`0x00384896`-`0x0038489D`). When the result's bit 5 is set it also removes Reverse, Disease (16) and Reflect
(23) from `+0x08`, sets a `+0x18` of `0x0D` to 0, and removes augment 15 (Medicine Reverse) (`0x003848A1`-`0x003848B8`).

### The first list: landing the hit

A recipe's first list runs when the action executes, through `0x00385680` (slot call `0x003859FF`), which
`0x00303830` calls at `0x00303910` and `0x00303A00` at `0x00303AD7`. A weapon recipe's first list is
`5 6 7 8 9 10 22 33 34 41`:

| Slot | Function | Does |
|---:|---|---|
| `5` | `0x00388350` | knockback chance = weapon byte `+0x1B`, adjusted by a random share of both levels |
| `6` | `0x00388440` | rolls knockback against it, unless the target has augment 0 (Stability) |
| `7`, `8` | `0x00388490`, `0x003884F0` | the counter flag `0x02AEDFC4`: rolled against the target's Speed / 2, or Speed × 2 with augment 7 (Counter Boost), when it has augment 6 (Counter) and no Stop, Sleep or Disable |
| `9`, `10` | `0x00388550`, `0x00388660` | the combo chance and count ([Combos](../Battle-Actions/combos.md)) |
| `22` | `0x00388FB0` | loads the target's shield, weapon and innate evade (`+0x33`, `+0x32`, `+0x31`) and sets the hit chance to 100 |
| `33` | `0x00389310` | halves the hit for a Blind source, `0x02AEDFE0 = 0x02AEDFE0 / 2` signed (`0x00389318`-`0x00389323`); clears the bands for an Invisible source or a target under Stop, Sleep or Disable, and the innate band under Immobilize |
| `34` | `0x00389370` | adds 25 to the innate band (30 for a party-side target) under target augment 4 (Evasion Boost), adds augment 3 and the three Shield Block licenses' augments 88-90 to the block band, clears all three bands when the user has augment 2 (Accuracy Boost, the Cameo Belt's augment), and clears bands the target's equipment does not allow |
| `41` | `0x003896B0` | the outcome roll below |

The bands slot 34 keeps come from `0x00384E50(target)`, which reads the integers `0x2902032B` and
`0x6003082D` of the target's model `@FCP` block through `0x004FE2F0` (`0x00384EBC`-`0x00384F12`). It gets
the block from `0x002E7FD0(actor)`: 0 for a null actor, a null `[actor+0xC0]` or an id of -1 there,
otherwise `0x002EDBD0(id)` for the character record that id names (`0x002E7FD0`-`0x002E7FF0`).

A magick recipe such as 7 has only slot 2 (`0x00387FD0`): an action with flag bit 17 can be blocked by a
shield, against the target's magick evade `+0x34` plus the Shield Block augments 88-90 (`0x00387FD0`-`0x0038823B`).

### The outcome roll

Slot 41 rolls the outcome (`0x003896B0`-`0x00389805`). When the target unit has bit 23 of its first dword:

```
r = MT19937 % hit
r < shield band  -> blocked with the shield, result kind 3 (or 4 with 0x02AEDFC4)
fresh r < weapon band -> parried with the weapon, kind 1 (or 2 with 0x02AEDFC4)
fresh r < innate band -> evaded, kind 5
```

Each failed band draws again, and when all three fail `MT19937 % 100` at or above the hit chance is a miss
(`0x02AEDFBC`). Without that bit only the hit chance is rolled. With knockback (`0x02AEDFC8`), a landed hit, a
shield block of kind 3 and a parry of kind 1 set result `+0x18` bit 3; kinds 2, 4 and 5 do not
(`0x00389734`-`0x00389741`, `0x003897F8`-`0x00389805`).

### The knockback value

When the committed resolve ends with result `+0x18` bit 3 set, the resolver stores
`0x00385E50(source, target, &context)` as an `f32` in result `+0x134` (`0x0038680F`-`0x0038682E`). The
value starts from a property of the target's model:

```python
k = 2.0                                  the target has no battle unit (0x01CEBC08, 0x00385E79)
k = p / s / 100.0                        p: @FCP float 0x09001E1F of the target's model s: the float at [actor+0xB8]+0x28
k = k * 0.5   when the outcome (result +0x04) is 1, 3, 7 or 11      mask 0x88A (0x00385EA9-0x00385EBC)
ref = min(7000, maxHp +0x24, doubled under Bubble)
ref = min(7000, max(hp +0x48, 1))        under Disease instead
k = k * 1.5   when the HP loss 0x02AEE004 > ref * 0.6                 (0x00385EC4-0x00385F32)
```

`p / s` is number 33 of `0x003204E0`, reached through `0x003204D0`, which passes the unit's actor
`[unit+0x10]` (`0x00385E7F`-`0x00385E8C`): `0x002ECE50` reads property `0x09001E1F` through `0x003E6150`
([Model files](../Graphics/model-files-cm-ca.md)), and number 33 then divides by the
float `0x00265240` returns from `[actor+0xB8]+0x28` (`0x0032055C`-`0x0032056A`). Outcome 1 is a weapon parry
and 3 a shield block (above). The constants are 100.0 (`0x008F3134`), 0.5 (`0x01CEBB70`), 0.6
(`0x008F3100`) and 1.5 (`0x00901B3C`).

### The committed list: the number

A weapon recipe's committed list is `28 or 29, prep, 96 97 98 99, 125, 165 171 176 182`, and the magick
recipe 7's is `62 92 93 94 95 113 170 175 182`:

| Slot | Function | Does |
|---:|---|---|
| `29` | `0x00389140` | ranged critical roll (recipes 25-27) |
| `65`-`79` | various | attack, defence and scale for the weapon type ([Weapon formulas](weapon-formulas.md)) |
| `62` | `0x00389DD0` | magick: scale `2 + Mag * (Lv + Mag) / 256`, attack = power + 12.5 % variance, defence = Magick Resist |
| `96` | `0x0038B950` | weapon status multipliers, table below |
| `92` | `0x0038B010` | magick status multipliers, table below |
| `97`, `93` | `0x0038BC00`, `0x0038B150` | the HP Critical and full-HP augments, below |
| `98` | `0x0038BE00` | doubles the scale on a critical |
| `99`, `94`, `95` | `0x0038BE30`, `0x0038B220`, `0x0038B6A0` | elements and weather ([Elements](elements.md)) |
| `125`, `113` | `0x0038D280` | the finisher: `(attack - defence) * scale` into HP loss or gain |
| `165` | `0x0038F890` | ×1.2 for augment 49 (Attack Boost), ×2 for augment 50 (Double-Edged) (`0x0038F89B`-`0x0038F8D0`) |
| `170`, `171` | `0x0038F970`, `0x0038F9D0` | the status chance: the action's `+0x14`, or the weapon's `+0x1F` |
| `175`, `176` | `0x0038FB80`, `0x0038FBC0` | roll it; a miss stops the list |
| `182` | `0x0038FCD0` | add the action's or weapon's statuses |

### Multipliers from statuses

The two status slots multiply the scale `0x02AEE054` (`0x0038B965`-`0x0038BBE6`, `0x0038B01A`-`0x0038B131`):

| Status | Weapon (slot 96) | Magick (slot 92) |
|---|---:|---:|
| source Berserk | ×1.5 | - |
| source Bravery | ×1.3 | - |
| source Faith | - | ×1.3 |
| target Sleep | ×1.5 | ×1.5 |
| target Protect | ×0.75 | - |
| target Shell | - | ×0.75 |
| source or target Stone or Petrify | × (its `+0xC4` - 1) / 10 | - |

### Augment multipliers

Slots 97 and 93 test the user's merged augment bits and the target's layers (`0x0038BC0F`-`0x0038BDDE`,
`0x0038B15A`-`0x0038B1FC`). "Party" here means a party or Esper record or an allied unit, those for which
`0x002F8E90() & 7` is non-zero:

| Effect | License | Condition | Factor |
|---:|---|---|---|
| 10 | Adrenaline | user HP Critical | ×2 party, ×1.7 others |
| 11 | Focus | user at full HP | ×1.5 party, ×1.4 others |
| 8 | Spellbreaker | user HP Critical | ×2 party, ×1.7 others |
| 103 | Serenity | user at full HP | ×1.5 party, ×1.4 others |
| 5 (target) | Last Stand | target HP Critical | ×0.5 party, ÷3 others |
| 40 (target) | none (Resist Piercing) | the user's main hand is a gun or a measure (class 9 or 16) | ×0.125 |

## Layouts

The scratch block, `0xA8` bytes at `0x02AEDFB8` in the zero-filled tail of `.data`. "Slot n" is calculator slot n
([Formula slots](formula-slots.md)); "result" is the action result record. The words read as -1 = none are set
to -1 by the reset (above).

`BattleFormulaScratch` (`0xA8` bytes, offsets from the start of the block):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | stop | 1 ends the slot list: the first list (`0x00385A07`) and the committed list (`0x003863D7`) run no later slot, and slots that call others return (`0x00388250`, `0x003889F0`, `0x00390190`, `0x00390240`); set by each slot that decides the outcome, e.g. the outcome roll (`0x0038971B`, `0x00389745`, `0x003897E3`) and the status-chance roll (`0x0038FBB2`), and by the resolver before any slot (`0x00386278`, `0x003862A2`) |
| `+0x04` | `u32` | failed | 1 when the action fails on this target: result kind 6 (`0x003866C1`-`0x003866CA`) and, after a first-list run, the target's bit in the memo record's `+0x04` (`0x00385A3A`); set by the outcome roll's miss (`0x003897D9`), the stat-lowering slots on a stat of 0 (`0x0038E878`), Steal with nothing to take (`0x0039049A`) and the other refusing slots |
| `+0x08` | `u32` | immune | 1 when the target is immune: result kind 10 (`0x003866CE`-`0x003866D7`) and, after a first-list run, the target's bit in the memo record's `+0x08` (`0x00385A82`); set by slot 0 for a target with augment 1 (Safety) (`0x00387F4C`), by the status step `0x00387CB0` (`0x00387F03`) and by the finishers when the element is nullified (`0x0038D2B0`, `0x0038D6C5`, `0x0038DBAE`, `0x0038E495`) |
| `+0x0C` | `u32` | counter | 1 when the target counters: slot 8 sets it when MT19937 % 100 is below `+0x24` for a target whose unit has bit 23 (`0x00388512`-`0x00388537`); the outcome roll then gives kind 4 for a block and 2 for a parry (`0x0038970A`, `0x00389779`), and the first list copies it into result `+0x18` bit 2 (`0x00385A21`-`0x00385A2D`); slot 10 clears it when a combo goes on (`0x003888A1`) |
| `+0x10` | `u32` | knockback | 1 when the hit knocks the target back: slot 6 sets it when MT19937 % 100 is below `+0x20`, unless the target has augment 0 (Stability) (`0x00388440`-`0x0038847E`); the outcome rolls of slots 41-44 turn it into result `+0x18` bit 3 (`0x00389734`, `0x003897F8`, `0x00389882`, `0x00389927`, `0x003899AE`, `0x00389A27`, `0x00389A95`); slot 10 clears it when a combo goes on (`0x003888AB`) |
| `+0x14` | `u32` | elementImmune | 1 when the target is immune to the action's element: set by the element stages, slot 95 for a magick (`0x0038B717`) and slot 99 for a weapon (`0x0038C016`); the finishers then store no HP number and set `+0x08` (`0x0038D2A3`, `0x0038D6B0`, `0x0038DBA1`, `0x0038E480`) |
| `+0x18` | `u32` | elementAbsorb | 1 when the target absorbs the action's element: set by slots 95 (`0x0038B8D1`) and 99 (`0x0038C75F`), which read it back (`0x0038B8C8`, `0x0038C756`); the finishers then store an HP gain instead of a loss (`0x0038D2CC`, `0x0038D6DC`, `0x0038DBD9`, `0x0038E4B8`) |
| `+0x1C` | `u32` | actionId | the action being resolved, by which every slot reads its action row; stored by the first list (`0x003857EC`) and the resolver (`0x00385FE4`), which put the memo record's word `+0x10` in place of Shades of Black, `0x9F` (`0x00385806`, `0x00385FFB`); the reset leaves it |
| `+0x20` | `u32` | knockbackChance | knockback chance in percent: slot 5 from the weapon's byte `+0x1B` (`0x00388430`), slot 16 from the action row's byte `+0x04` (`0x00388BFB`), each plus MT19937 % the user's level minus MT19937 % the target's level, not below 0; rolled by slot 6 (`0x00388474`) |
| `+0x24` | `u32` | counterChance | counter chance in percent: slot 7 sets the target's Speed / 2 under augment 6 (Counter), Speed × 2 under augments 6 and 7 (Counter Boost), and 0 without Counter or under Stop, Sleep or Disable (`0x00388490`-`0x003884DF`); rolled by slot 8 (`0x0038852D`) |
| `+0x28` | `u32` | hitChance | hit chance in percent: 100 from slot 22 (`0x00388FCE`), the action row's byte `+0x12` from slots 25 and 26 (`0x0038908D`, `0x00389108`), or a recipe's own value; halved for a Blind user by slot 33 (`0x00389323`); the outcome rolls count MT19937 % 100 at or above it as a miss (`0x003897D0`) and draw the evade bands modulo it (`0x003896E3`) |
| `+0x2C` | `u32` | comboChance | chance in percent that a combo starts: slot 9 (`0x00388648`), rolled by slot 10 (`0x00388716`) |
| `+0x30` | `u32` | statusChance | chance in percent that the action's statuses land: slot 170 from the action row's byte `+0x14` (`0x0038F9B4`), slot 171 from the weapon's byte `+0x1F` (`0x0038FB48`, `0x0038FB63`); slots 175 and 176 stop the list when MT19937 % 100 is at or above it (`0x0038FBA8`, `0x0038FBE2`) |
| `+0x34` | `u32` | innateBand | the target's innate evade: its stats byte `+0x31` from slots 22 and 25 (`0x00388FC8`, `0x003890AB`), 0 from slot 26 (`0x00389122`); raised for Evasion Boost by slot 34 (`0x003893BF`) and cleared by slots 33 and 34 (`0x00389368`, `0x003895AD`); a band draw below it is an evade, kind 5 (`0x003897A5`) |
| `+0x38` | `u32` | shieldBand | the target's shield evade: its stats byte `+0x33` from slots 22 and 25 (`0x00388FB4`, `0x00389097`); in slot 2 the magick block chance (`0x00388080`-`0x003881FC`); raised for Shield Boost and the Shield Block augments by slots 2 and 34; a band draw below it is a block, kind 3 or 4 (`0x00389702`) |
| `+0x3C` | `u32` | weaponBand | the target's weapon evade: its stats byte `+0x32` from slots 22 and 25 (`0x00388FBE`, `0x003890A1`); cleared by slots 33 and 34 (`0x00389339`, `0x00389597`); a band draw below it is a parry, kind 1 or 2 (`0x00389771`) |
| `+0x40` | `i32` | chargesLost | Mist charges the target loses: slot 129 sets 0, or all the target's charges (stats `+0x4E`) under Reverse or the user's Medicine Reverse (`0x0038E11C`, `0x0038E149`, `0x0038E1CF`, `0x0038E1F7`, `0x0038E29B`); the resolver subtracts it from `+0x44` into result `+0x1D` (`0x00386621`-`0x00386655`) |
| `+0x44` | `i32` | chargesGained | Mist charges the target regains: slot 129 sets its MP bars (stats `+0x37`) minus its charges, or 0 under Reverse (`0x0038E127`, `0x0038E161`, `0x0038E1DA`, `0x0038E20F`, `0x0038E2A6`); result `+0x1D` is this minus `+0x40`, low byte (`0x0038660E`-`0x00386655`) |
| `+0x48` | `u32` | mpFlag | read only by the resolver, which sets result `+0x2C` bit 12 from it when the target's MP words `+0x54` and `+0x58` are -1 (`0x00386537`-`0x0038654B`); its one writer is the reset's 0 (`0x00384A16`), so it never sets the bit |
| `+0x4C` | `i32` | targetHpLoss | HP the target loses, the damage: written by the finishers and the damage slots (`0x0038D280` and others); the HP loss in the knockback value (`0x00385F13`); result `+0x24` is `+0x50` minus this (`0x00386635`, `0x00386658`); not -1, it sets result `+0x2C` bits 6, 8 and 18 |
| `+0x50` | `i32` | targetHpGain | HP the target regains, from a cure or an absorbed element (`0x0038D2E9` and others); not -1, it sets result `+0x2C` bits 6, 8 and 10 |
| `+0x54` | `i32` | targetMpLoss | MP the target loses: slots 107, 117, 128 and 153 (`0x0038CF0F`, `0x0038D658`, `0x0038E04D`, `0x0038F108`); result `+0x2A` is `+0x58` minus this in 16 bits (`0x00386638`, `0x0038665F`); not -1, it sets result `+0x2C` bits 12 and 14 |
| `+0x58` | `i32` | targetMpGain | MP the target regains: slots 109, 128, 134 and 201 (`0x0038D0CF`, `0x0038E034`, `0x0038E789`, `0x00390A46`); not -1, it sets result `+0x2C` bits 12, 14 and 16 |
| `+0x5C` | `i32` | userHpLoss | HP the user loses: Double-Edged's cost (`0x0038F8D0`), Damage Spikes on the target (`0x00390F85`), slots 103, 116, 135 and 140 (`0x0038CB5E`, `0x0038D4B3`, `0x0038E830`, `0x0038E97F`); result `+0x20` is `+0x60` minus this (`0x00386642`, `0x0038665B`); not -1, it sets result `+0x2C` bits 5 and 7 |
| `+0x60` | `i32` | userHpGain | HP the user regains: the drain slots 116, 148 and 151 (`0x0038D46B`, `0x0038EE2A`, `0x0038EF84`) and slot 162, the target's HP (`0x0038F6CA`); not -1, it sets result `+0x2C` bits 5, 7 and 9 |
| `+0x64` | `i32` | userMpLoss | MP the user loses; no slot writes it: its writers are the reset's -1 (`0x00384A81`) and the resolver's write-back of 0 (`0x00386617`), and its one reader is the resolver (`0x00386453`), so it adds nothing to result `+0x28` and never sets result `+0x2C` bit 11 or 13 |
| `+0x68` | `i32` | userMpGain | MP the user regains: the MP drain of slot 117 (`0x0038D65E`); result `+0x28` is this minus `+0x64` in 16 bits (`0x00386651`, `0x00386664`); not -1, it sets result `+0x2C` bits 11, 13 and 15 |
| `+0x6C` | `i32` | userHpSet | the user's HP set outright; no slot writes it: its writers are the reset's -1 (`0x00384A95`) and the resolver's -1 for a user with KO, Stone or X-Zone (`0x00386424`), and its one reader is the resolver (`0x0038645A`), which would put it in result `+0x20` with result `+0x2C` bit 1 (`0x0038667D`-`0x0038668E`); it is always -1 there |
| `+0x70` | `i32` | userMpSet | the user's MP set outright: 0 from slot 164 (`0x0038F85B`, `0x0038F869`), -1 for a user with KO, Stone or X-Zone (`0x0038641D`); result `+0x28` with result `+0x2C` bit 2 (`0x003866A9`-`0x003866BE`) |
| `+0x74` | `i32` | targetHpSet | the target's HP set outright: full HP from slots 1 and 129 (`0x00387FA5`, `0x0038E0ED`), 0 from slot 3 (`0x003882FC`), a swap from slot 152 (`0x0038F00C`), among others; result `+0x24` with result `+0x2C` bit 3 (`0x0038664B`-`0x0038667A`); not -1, it sets bit 8 (`0x0038647E`) |
| `+0x78` | `i32` | targetMpSet | the target's MP set outright: 0 from slot 48 (`0x00389C29`), max MP from slot 129 (`0x0038E103`), slots 152, 154, 155 and 159 (`0x0038EFBD`, `0x0038F199`, `0x0038F23A`, `0x0038F54E`); result `+0x2A` with result `+0x2C` bit 4 (`0x00386691`-`0x003866A6`); not -1, it sets bit 14 (`0x003864E1`) |
| `+0x7C` | `i32` | newStrength | an enemy's new Strength: 70 % from slot 136 (`0x0038E89A`), raised by the action's power from slot 149 (`0x0038EEBC`); the resolver copies its low 16 bits to result `+0x11E` (`0x0038679F`), and not -1 it sets result `+0x2C` bit 18 (`0x00386571`) |
| `+0x80` | `i32` | newMagickPower | an enemy's new Magick Power: 70 % from slot 137 (`0x0038E8DA`), raised from slot 150 (`0x0038EF4C`); result `+0x120` (`0x003867AD`); bit 18 (`0x0038657A`) |
| `+0x84` | `i32` | newDefense | an enemy's new Defense: 90 % from slot 138 (`0x0038E919`); result `+0x122` (`0x003867BB`); bit 18 (`0x00386583`) |
| `+0x88` | `i32` | newMagickResist | an enemy's new Magick Resist: 90 % from slot 139 (`0x0038E949`); result `+0x124` (`0x003867C9`); bit 18 (`0x0038658C`) |
| `+0x8C` | `i32` | targetLevel | the target's new level: slot 161 adds level × the action row's byte `+0x10` / 100, at most 99 (`0x0038F620`); the resolver copies the low byte to result `+0x11C` (`0x003867D7`) |
| `+0x90` | `i32` | userLevel | the user's new level: slot 162 (`0x0038F6D4`); -1 for a user with KO, Stone or X-Zone (`0x00386430`); the resolver copies the low byte to result `+0x11D` (`0x003867E4`) |
| `+0x94` | `u8` | stealCommon | 1 when Steal takes the target's first item, `+0x32` (`0x0039055B`, `0x00390635`); result `+0x32` (`0x003867F1`) |
| `+0x95` | `u8` | stealUncommon | 1 when Steal takes the second item, `+0x34` (`0x00390527`, `0x00390650`); result `+0x33` (`0x003867FB`) |
| `+0x96` | `u8` | stealRare | 1 when Steal takes the third item, `+0x36` (`0x003904EB`, `0x0039066A`); result `+0x34` (`0x00386805`) |
| `+0x97` | `u8[1]` | unused97 | read and written by no function; nothing fixes its width |
| `+0x98` | `i32` | poachItem | the item Poach takes, from slot 196 (`0x003906D9`-`0x003907AB`); result `+0x38` (`0x00386813`) |
| `+0x9C` | `f32` | scale | the damage scale: set by the preparation slots, multiplied by the status and augment slots, and applied by the finishers, (attack - defense) × scale (`0x0038D2D3`) |
| `+0xA0` | `f32` | attack | attack, with its variance (`0x0038D280`) |
| `+0xA4` | `f32` | defense | the defence subtracted from attack (`0x0038D28B`) |

No instruction reads or writes `+0x97`. No instruction takes the address of any part of the block, so every access
is one of these direct ones.

## State

The two words of the block that no slot writes:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AEE01C` | `i32` | 0 (zero-filled tail); -1 after each reset | the user's MP loss, `+0x64` | `0x003849B0`, -1 (`0x00384A81`); `0x00385F60`, 0 in place of -1 (`0x00386617`) | `0x00385F60` (`0x00386453`) |
| `0x02AEE024` | `i32` | 0 (zero-filled tail); -1 after each reset | the user's HP set outright, `+0x6C` | `0x003849B0`, -1 (`0x00384A95`); `0x00385F60`, -1 for a user with KO, Stone or X-Zone (`0x00386424`) | `0x00385F60` (`0x0038645A`) |

## Modding notes

- A multiplier lives in its slot; changing Berserk's ×1.5 means editing the constant that slot `0x0038B950`
  loads (`0x00901B3C`, shared with other code).
- Moving a slot between a recipe's lists moves it from the landing rolls to the damage step or back.
- The scratch block is global: a slot added to a recipe sees every value the earlier slots of that recipe
  left.

## Related

- [Formula slots](formula-slots.md) - every slot.
- [Formula recipes](formula-recipes.md) - every recipe's lists.
- [Weapon formulas](weapon-formulas.md) - the weapon preparation slots and criticals.
- [Elements](elements.md) - the element stages and the finisher.
- [Action results](../Battle-Actions/action-results.md) - the record the resolver fills.
- [Combos](../Battle-Actions/combos.md) - slots 9 and 10.
