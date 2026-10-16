---
title: "Statuses: every status with its name, help text, duration, the statuses it cancels and blocks, and what it does when it lands"
kind: "reference"
category: "Status effects and KO"
summary: "All 32 battle statuses of battle_pack.bin section 15 by id: the name and help line the game shows, the default duration and the Poison, Sap, Regen, Petrify and Doom beat, the statuses each one removes when it lands and the ones that keep it from landing, whether it counts as harmful, which Remedy cures it, whether it can be cast again while present, whether only party members can have it, and what its arrival or removal does."
addresses: ["02EBF118", "00236D94", "00387730", "003876D0", "0030E68A", "00387E5D", "0030E8C4"]
---

# Statuses: every status with its name, help text, duration, the statuses it cancels and blocks, and what it does when it lands

## What it lists

A unit's statuses are 32 bits, status *s* being bit `1 << s`, held in its stats record's words `+0x64` and
`+0x3C`, with immunities in `+0x38` ([Gaining and losing statuses](status-changes.md)). Each status has a
40-byte row in `battle_pack.bin` section 15, bound to `02EBF118` (`00236D94`). The name is entry *s* of text bank
5 (row word `+0x00` = `0x2800` + *s*), and the help line is entry *s* of `listhelp_status.bin` (row word `+0x0A`,
text id 12,000 + *s*, `0031E288`).

### Duration and beat

The default duration comes from row byte `+0x08` through `00387730` (`00387740`-`00387992`):

```
b   = row +0x08            (0xFF: no duration)
vit = target Vitality (+0x2C)
harmful:     v = trunc(2b - b * vit / 100)
beneficial:  v = trunc(b + b * vit / 100), times 1.5 with augment 30 in either layer
duration timer = v * 300 * frame base
```

The beat timer is row byte `+0x09` times 30 times the frame base (`003876D0`). The periodic step takes 10 off both
every frame ([Status timers](status-timers.md)), so `+0x08` is in seconds and `+0x09` in tenths of a second at 30
and at 60 frames per second. Petrify and Doom have no duration in their rows (`+0x08` is `0xFF`); instead
`00387730` returns a count of 11 for them before it reads the row (`00387740`), and the count steps down on each
beat; the player sees 10. Augment 30's text is "Increases duration of status effects."

### Cancelling and blocking

Two masks over status ids sit in each row:

- **cancels**, row `+0x0C`: when the status lands, each status in the mask is removed from the timed word
  (`0030E63D`-`0030E6D7`);
- **blocked by**, row `+0x20`: the status is not applied while the target already has any status in the mask
  (`00387E5D`-`00387E63`, `0038FE0D`, `003909DC`).

### The flag word

Row word `+0x06` holds these bits:

| Bit | Meaning | Sites |
|---|---|---|
| 13 | harmful: Vitality shortens it, a removal posts "is cured of" rather than "fades from", and augment 57 blocks it | `00387806`, `0046A34D`, `00387D25`-`00387D76` |
| 10 | Remedy always cures it | `003873FE`, `0038540C` |
| 14, 12, 11 | Remedy cures it with augment 116, 117 or 118 | `0038746E`, `003874DE`, `0038754D` |
| 5 | it can be applied again while present in the timed word, restarting its timers; one held in `+0x3C` is still refused | `00387DA2`-`00387DC6`, `00390953` |
| 8 | it is refused on a target that is not a party record | `00387E17`, `0038FDC6`, `003909A5` |

The augment texts (bank 10, entries 116-118) are "Remedies remove Stop, Doom, and Disease.", "Remedies remove
Petrify, Confuse, and Oil." and "Remedies remove Sleep, Sap, Immobilize, and Disable."

### Statuses the game checks together

Code tests the two status words together: it loads `+0x64`, ORs `+0x3C` into it and tests a mask. Over every
function of the image this happens at 248 sites in 167 functions (`003868F1`-`003868F7` is one). The masks group the
statuses by what they stop:

| Mask | Statuses | Sites | What it stops |
|---|---|---:|---|
| `0x80000003` | KO, Stone, X-Zone | 127 | taking HP damage (`00300530`), and the defeat and slot-release steps, which run their full work only for a unit without them (`00233AD0`, `00234200`) |
| `0x00010000` | Disease | 44 | HP recovery and the HP checks of gambits and targeting (`0030F340`, `00385B10`, `00301AD0`, `003083B0`) |
| `0x08000020` | Confuse, Berserk | 7 | following orders: stance, engagement and moving under the player's control (`00307D10`, `00308130`, `00325D90`) |
| `0x8800203B` | KO, Stone, Stop, Sleep, Confuse, Disable, Berserk, X-Zone | 3 | issuing a command (`00311CF0`, `00307E70`) |
| `0x8000001B` | KO, Stone, Stop, Sleep, X-Zone | 2 | continuing or queueing an action (`002FFB60`, `00313CD0`) |
| `0x8000201B`, `0x8000401B` | the same with Disable, or with Immobilize | 3 | stance and movement queries (`00307DF0`, `0030BFB0`, `00325D90`) |
| `0x00010010` | Sleep, Disease | 1 | the periodic HP credit (`00386860`) |

Nine more masks are each used at one to three sites, and 48 sites test the combined word some other way.

## Columns

`statuses.tsv`, one row per status:

| Column | Meaning |
|---|---|
| `id` | the status id, 0-31 |
| `name` | the name the game shows, from text bank 5 |
| `help_text` | the help line, from `listhelp_status.bin` |
| `duration` | the default duration before Vitality, from row `+0x08`; `-` for none; `count 11` for Petrify and Doom, from the code, not the row |
| `beat` | the interval of the status's periodic step, from row `+0x09`; `-` for none |
| `cancels` | the statuses it removes when it lands, from row `+0x0C` |
| `blocked_by` | the statuses that keep it from landing, from row `+0x20` |
| `class` | harmful or beneficial, from flag bit 13 |
| `remedy` | whether Remedy cures it: always, or with augment 116, 117 or 118 |
| `refresh` | `yes` when it can be applied again while present (flag bit 5) |
| `party_only` | `yes` when it is refused on a target that is not a party record (flag bit 8) |
| `arm` | what its arrival or removal does beyond the status bit ([Gaining and losing statuses](status-changes.md)) |
| `sites` | the row's file offset in `battle_pack.bin` |

## Related

- [Gaining and losing statuses](status-changes.md) - the status write, the cancel cascade and each status's arm.
- [Status timers](status-timers.md) - how the duration and beat run down, and what Poison, Sap, Regen, Petrify and
  Doom do on their beat.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - the augment ids named here and the immunity word.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) - the conditions that test statuses.
