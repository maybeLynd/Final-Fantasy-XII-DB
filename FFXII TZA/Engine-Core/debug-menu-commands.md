---
title: "Debug menu commands: every developer-console row id with its label, arm, kind, field, step and bound"
kind: "reference"
category: "Engine core"
addresses: "001D1660, 001D4C1C, 001D4BFA, 001D0390, 01F81428"
---

## What it lists

One row per command id the dispatcher `001D1660` accepts, 12 to 293 ([debug
menu](debug-menu.md)). The arm column is decoded from the 282-entry table at `001D4C1C` in the
image; the label is the string the console object's filler `001D0390` stores at `+130h + id ×
8`; kind, field, step and bound are read from the arm's instructions. Ids 1 to 11 have labels and
no arm and are not listed. The 56 ids whose arm is the shared do-nothing tail `001D4BFA` are
listed with kind `none` (a button row whose action is absent) or `readout` (a row that still
prints a live value).

| Kind | Rows | Meaning |
|---|---|---|
| nudge | 110 | a float stepped by one constant in both directions |
| toggle | 55 | a byte or flag flipped between two values |
| int-step | 30 | an integer stepped by 1 (or 10) with a floor, clamp or wrap |
| cycle | 23 | a small mode value cycled over N states |
| call | 8 | a subsystem function called with the direction |
| readout | 16 | prints a value, no action |
| none | 40 | button rows without an action arm |

## Columns

| Column | Meaning |
|---|---|
| `id` | the command id, 12 to 293 |
| `label` | the row text the console prints, from `001D0390` |
| `arm` | the arm address: `120000`<sub>h</sub> + the RVA at `001D4C1C + (id - 12) × 4` |
| `kind` | nudge, int-step, toggle, cycle, call, readout, none |
| `field` | the `.data` address the arm reads and writes, or `obj+offset` on the console object at `[01F81428]`; `-` when the arm only calls |
| `step` | the magnitude, signed `±` when the direction flag picks the sign |
| `bound` | the wrap, clamp or floor the arm applies |
| `note` | what the arm does in plain words, from its instructions |
| `slice` | the letter of the id range the row falls in (A = 12 to 43 and so on in steps of 32) |

## Related

- [Debug menu](debug-menu.md): the dispatcher, the pages and the arms' shape.
- [Graphics settings](graphics-settings.md): the block most nudge rows step, and the shader
  constant each field feeds.
