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
10. It clears bit 0 of the memo record's `+0x12` (`0x00386402`) and turns the scratch block into the result:
   `0x02AEDFBC` → kind 6, `0x02AEDFC0` → kind 10
   (`0x003866C1`-`0x003866D7`), the HP change from `0x02AEE004` / `0x02AEE008`, and the other fields
   ([Action results](../Battle-Actions/action-results.md)).

`0x003849B0` sets the HP, MP and other number words `0x02AEE004`-`0x02AEE050` to -1 ("none"), except the steal
bytes `0x02AEE04C`-`0x02AEE04E`, and the flags, rolls, bands and the scale, attack and defence values
`0x02AEDFB8`-`0x02AEE000` and `0x02AEE054`-`0x02AEE05C` to 0 (`0x003849B2`-`0x00384B03`).

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
| `+0x04` | the source's statuses (`+0x64 \| +0x3C`) |
| `+0x08` | the target's statuses |
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
| `7`, `8` | `0x00388490`, `0x003884F0` | the alternative outcome flag `0x02AEDFC4`: a chance from the target's Speed when it has augment 6 (Counter) |
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
(`0x02AEDFBC`). Without that bit only the hit chance is rolled. A landed hit with knockback sets result
`+0x18` bit 3.

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
| 40 (target) | (no augment text) | the user's main hand is a gun or a measure (class 9 or 16) | ×0.125 |

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
