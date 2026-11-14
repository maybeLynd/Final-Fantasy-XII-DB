---
title: "Statuses: every status with its name, help text, duration, the statuses it cancels and blocks, and what it does when it lands"
kind: "reference"
category: "Status effects and KO"
addresses: "0x02EBF118, 0x00236D94, 0x00387730, 0x003876D0, 0x0030E68A, 0x00387E5D, 0x0030E8C4"
---

## What it lists

A unit's statuses are 32 bits, status *s* being bit `1 << s`, held in its stats record's words `+0x64` and
`+0x3C`, with immunities in `+0x38` ([Gaining and losing statuses](status-changes.md)). Each status has a
40-byte row in `battle_pack.bin` section 15, bound to `0x02EBF118` (`0x00236D94`). The name is entry *s* of text bank
5 (row word `+0x00` = `0x2800` + *s*), and the help line is entry *s* of `listhelp_status.bin` (row word `+0x0A`,
text id 12,000 + *s*, `0x0031E288`).

Each status is one row of a table in `battle_pack.bin`. The row gives the number of the status's name in a text bank
and of its help line in `listhelp_status.bin`, and holds its length, its beat, and the statuses it removes or is
blocked by.

Row bytes `+0x11`-`+0x12` and `+0x14`-`+0x1F` are read and written by no function; nothing fixes their width. In the
shipped rows 42 of these 448 bytes are not `0xFF`, all of them 25 to 31.

### Duration and beat

The default duration comes from row byte `+0x08` through `0x00387730` (`0x00387740`-`0x00387992`):

```python
b = row +0x08            (0xFF: no duration)
vit = target Vitality (+0x2C), 0 with a null stats pointer
harmful:     v = trunc(2b - b * vit / 100)
beneficial:  v = trunc(b + b * vit / 100); with Spellbound (augment 30) in either layer, v = trunc(v * 1.5)
duration timer = v * 300 * frame base
```

With a null stats pointer the Vitality is 0 and the Spellbound test is not made (`0x003877B5`-`0x003877C1`,
`0x0038795B`). The test is bit `0x40` of the stats byte `+0x6B` or `+0x7B`, and `v * 1.5` goes through
`cvttss2si` before the integer `v * 300 * frame base`, the frame base being the dword `0x01DFE0B4`
(`0x00387960`-`0x00387992`). A row whose `+0x08` is `0xFF` returns 0 (`0x003877A6`-`0x003877AA`,
`0x003879A3`-`0x003879A8`).

The beat timer is row byte `+0x09` times 30 times the frame base (`0x003876D0`). The periodic step takes 10 off both
every frame ([Status timers](status-timers.md)), so `+0x08` is in seconds and `+0x09` in tenths of a second at 30
and at 60 frames per second. Petrify and Doom have no duration in their rows (`+0x08` is `0xFF`); instead
`0x00387730` returns a count of 11 for them before it reads the row (`0x00387740`), and the count steps down on each
beat; the player sees 10. Augment 30's text is "Increases duration of status effects."

### Cancelling and blocking

Two masks over status ids sit in each row:

- **cancels**, row `+0x0C`: when the status lands, each status in the mask is removed from the timed word
  (`0x0030E63D`-`0x0030E6D7`);
- **blocked by**, row `+0x20`: the status is not applied while the target already has any status in the mask
  (`0x00387E5D`-`0x00387E63`, `0x0038FE0D`, `0x003909DC`).

### The flag word

Row word `+0x06` holds these bits:

| Bit | Meaning | Sites |
|---|---|---|
| `0x2000` | harmful: Vitality shortens it, a removal posts "is cured of" rather than "fades from", and augment 57 blocks it | `0x00387806`, `0x0046A34D`, `0x00387D25`-`0x00387D76` |
| `0x400` | Remedy always cures it | `0x003873FE`, `0x0038540C` |
| `0x4000`, `0x1000`, `0x800` | Remedy cures it with Remedy Lore 3, 2 or 1 (augment 116, 117 or 118) | `0x0038746E`, `0x003874DE`, `0x0038754D` |
| `0x20` | it can be applied again while present in the timed word, restarting its timers; one held in `+0x3C` is still refused | `0x00387DA1`-`0x00387DC6`, `0x00390953` |
| `0x100` | it is refused on a target that is not a party record | `0x00387E17`, `0x0038FDC6`, `0x003909A5` |

The augment texts (bank 10, entries 116-118) are "Remedies remove Stop, Doom, and Disease.", "Remedies remove
Petrify, Confuse, and Oil." and "Remedies remove Sleep, Sap, Immobilize, and Disable."

### Statuses the game checks together

Code tests the two status words together: it loads `+0x64`, ORs `+0x3C` into it and tests a mask. Over every function of the image this happens at 251 sites in 168 functions (`0x003868F1`-`0x003868F7` is one); the three
in `0x00390F20` load both words into registers first (`0x00391118`-`0x0039111E`). The masks group the
statuses by what they stop:

| Mask | Statuses | Sites | What it stops |
|---|---|---:|---|
| `0x80000003` | KO, Stone, X-Zone | 127 | taking HP damage (`0x00300530`), and the defeat and slot-release steps, which run their full work only for a unit without them (`0x00233AD0`, `0x00234200`) |
| `0x00010000` | Disease | 44 | HP recovery and the HP checks of gambits and targeting (`0x0030F340`, `0x00385B10`, `0x00301AD0`, `0x003083B0`) |
| `0x08000020` | Confuse, Berserk | 7 | following orders: stance, engagement and moving under the player's control (`0x00307D10`, `0x00308130`, `0x00325D90`) |
| `0x8800203B` | KO, Stone, Stop, Sleep, Confuse, Disable, Berserk, X-Zone | 3 | issuing a command (`0x00311CF0`, `0x00307E70`) |
| `0x8000001B` | KO, Stone, Stop, Sleep, X-Zone | 2 | continuing or queueing an action (`0x002FFB60`, `0x00313CD0`) |
| `0x8000201B`, `0x8000401B` | the same with Disable, or with Immobilize | 3 | stance and movement queries (`0x00307DF0`, `0x0030BFB0`, `0x00325D90`) |
| `0x00010010` | Sleep, Disease | 1 | the periodic HP credit (`0x00386860`) |

Nine more masks are each used at one to four sites, and 50 sites test the combined word some other way.

## Columns

[`statuses.tsv`](statuses.tsv), one row per status:

| Column | Meaning |
|---|---|
| `id` | the status id, 0-31 |
| `name` | the name the game shows, from text bank 5 |
| `help_text` | the help line, from `listhelp_status.bin` |
| `duration` | the default duration before Vitality, from row `+0x08`; `-` when the status has no duration; `count 11` for Petrify and Doom, from the code, not the row |
| `beat` | the interval of the status's periodic step, from row `+0x09`; `-` when the status has no periodic step |
| `cancels` | the statuses it removes when it lands, from row `+0x0C` |
| `blocked_by` | the statuses that keep it from landing, from row `+0x20` |
| `class` | harmful or beneficial, from flag bit `0x2000` |
| `remedy` | whether Remedy cures it: always, or with Remedy Lore 3, 2 or 1 (augment 116, 117 or 118) |
| `refresh` | `yes` when it can be applied again while present (flag bit `0x20`) |
| `party_only` | `yes` when it is refused on a target that is not a party record (flag bit `0x100`) |
| `arm` | what its arrival or removal does beyond the status bit ([Gaining and losing statuses](status-changes.md)) |
| `sites` | the row's file offset in `battle_pack.bin` |

## Related

- [Gaining and losing statuses](status-changes.md) - the status write, the cancel cascade and each status's arm.
- [Status timers](status-timers.md) - how the duration and beat run down, and what Poison, Sap, Regen, Petrify and
  Doom do on their beat.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - the augment ids named here and the immunity word.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) - the conditions that test statuses.
