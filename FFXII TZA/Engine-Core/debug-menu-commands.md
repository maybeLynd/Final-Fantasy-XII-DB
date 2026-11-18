[Home](../../README.md) / [Engine core](README.md) / Debug menu commands

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Debug menu commands: every developer-console row id with its label, arm, kind, field, step and bound | reference | Engine core | Debug tools | All 282 command ids of the developer console's dispatcher 0x001D1660, ids 12 to 293: the label the menu prints, the arm the dispatch table at 0x001D4C1C selects, what kind of control the arm is, the field it steps or the function it calls, the step magnitude and the wrap or clamp, in debug-menu-commands.tsv. | 0x001D1660, 0x001D4C1C, 0x001D4BFA, 0x001D0390, 0x01F81428 |

## What it lists

One row per command id the dispatcher `0x001D1660` accepts, 12 to 293 ([debug
menu](debug-menu.md)). The arm column is decoded from the 282-entry table at `0x001D4C1C` in the
image; the label is the string the console object's filler `0x001D0390` stores at `+0x130 + id ×
8`; kind, field, step and bound are read from the arm's instructions. Ids 1 to 11 have labels and
no arm and are not listed. The 56 ids whose arm is the shared do-nothing tail `0x001D4BFA` are
listed with kind `no-action` (a button row whose action is absent) or `readout` (a row that still
prints a live value).

| Kind | Rows | Meaning |
|---|---|---|
| nudge | 110 | a float adjusted in both directions: most add or subtract one constant; id 106 multiplies by 0.99 or 1.01, and ids 190 to 193 scale their step while the field `+0xC58` is above 20 |
| toggle | 55 | a byte or flag flipped between two values |
| int-step | 30 | an integer stepped by 1 (or 10) with a floor, clamp or wrap |
| cycle | 23 | a small mode value cycled over N states |
| call | 8 | a subsystem function called with the direction |
| readout | 16 | prints a value, no action |
| no-action | 40 | button rows without an action arm |

[The command inputs](debug-menu-commands-inputs.tsv) table gives each id's values, who reaches it, when it takes
effect, what its arm changes, what the player sees and when it changes nothing.

- Sixteen ids are the Config screen's settings: `0x0017DB90` maps the screen's row kinds to them, so a change on the
  Config screen runs the id's arm through `0x001CD040` and the dispatcher.
- The other 266 change nothing in the shipped game, because the menu that would reach them never opens and no Config
  screen row maps to them. Two of those bytes are read by input code (`+0xC35`, id 187, and `+0xC3D`, id 293),
  and their only writes outside the console object's constructor are their own arms.

### Columns of debug-menu-commands-inputs.tsv

| Column | Holds |
|---|---|
| `input` | the command id, as `id` in debug-menu-commands.tsv |
| `label` | the row text the console prints, as `label` in debug-menu-commands.tsv |
| `domain` | the values the row can take, built from its kind, step and bound in debug-menu-commands.tsv: `on or off (0/1)` on the 55 toggles; kind, step and bound (for example `nudge, step ±0.01, -` or `cycle, step ±1, wraps 0..2`) on the 163 nudge, int-step and cycle rows; `a button row with no value` on the 40 no-action rows; `a read-out row` on the 16 read-outs; `a button row that runs its arm` on the 8 call rows |
| `precedence` | which writer wins when another one sets the same field: `-` on the 266 ids that only the console reaches; on the 16 Config screen ids, the Config screen row kind that `0x0017DB90` maps to the id, its only caller |
| `takes_effect` | when a change starts to act: `never` on 266 rows; on the 16 Config screen ids, when the player changes that Config row (`0x0023B330` or `0x0023B6F0`, then `0x0017DB90`, `0x001CD040` and the dispatcher `0x001D1660`) |
| `consumers` | the arm the dispatch table selects for the id (the same address as `arm` in debug-menu-commands.tsv on all 282 rows), then the field it changes and the code that reads that field |
| `visible_effect` | what the player sees: `the setting of that Config screen row` on the 16 Config screen ids; the other 266 rows record that nothing on screen changes |
| `inert_when` | when a change does nothing: `always` with the reason on the 266 console-only ids (the menu that would reach the id never opens, and no Config screen row kind maps to it; ids 187 and 293 add the input code that reads their byte); `-` on the 16 Config screen ids |

## Columns

| Column | Meaning |
|---|---|
| `id` | the command id, 12 to 293 |
| `label` | the row text the console prints, from `0x001D0390` |
| `arm` | the arm address: `0x120000` + the RVA at `0x001D4C1C + (id - 12) × 4` |
| `kind` | nudge, int-step, toggle, cycle, call, readout, no-action |
| `field` | the `.data` address the arm reads and writes, or `obj+offset` on the console object at `[0x01F81428]`; `-` when the arm only calls |
| `step` | the magnitude, signed `±` when the direction flag picks the sign |
| `bound` | the wrap, clamp or floor the arm applies |
| `note` | what the arm does in plain words, from its instructions |

## Related

- [Debug menu](debug-menu.md): the dispatcher, the pages and the arms' shape.
- [Graphics settings](graphics-settings.md): the block most nudge rows step, and the shader
  constant each field feeds.
