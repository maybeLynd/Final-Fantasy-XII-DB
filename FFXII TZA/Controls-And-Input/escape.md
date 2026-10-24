---
title: "Escape Mode: the R2 toggle that makes the party run from battle, what it switches off, and why it takes a second to engage"
kind: "system"
category: "Controls and input"
addresses: "0x0017DE10, 0x00253C70, 0x00252B60, 0x00252C80, 0x00366870, 0x01E0C2B8"
---

## What the player sees

- Pressing R2 switches Escape Mode on, and pressing it again switches it off; the button does not have to be held.
- Escape Mode takes about a second to engage after the press, with a sound while it arms.
- In towns it switches itself off as soon as R2 is released.
- While it is on, the party runs instead of fighting: the commands offered, combos, engagement and battle movement all
  change.

## How it works

### The button

`0x0017DE10` answers whether the R2 binding is held. It reads the stored word directly: `0x00197710(manager, 0, 0, 9)`
returns slot 9 of the first profile, `[Keyboard1]`, from `0x01F80F90` (`0x0017DE2A`-`0x0017DE32`, `0x0019775A`-`0x0019776F`),
not from the published copy, which has L2 and R2 cleared ([keymap.ini](keymap-file.md)). The code is tested on the current input device (`0x0079E6A0`). It is a
level, not a press; the press is made by the latch below.

### The latch

The input arbiter `0x00253C70` keeps the toggle `0x020927E0`, a press latch `0x020927E4` and an override `0x01E0C2B4`, and
nothing else touches them (`0x002541D4`-`0x00254258`):

1. While R2 is held, the override is cleared, and on the first frame of the press the toggle flips
   (`0x002541D4`-`0x002541FD`); the latch then stays set.
2. When R2 is released, input snapshot bit 9 (`0x02F97360`) is set and `0x00862CF0` does not answer 1, the toggle and the
   override are set to 1 (`0x0025420A`-`0x00254228`), and the latch is left set.
3. Otherwise, when the override is set or the area's town bit is set (`0x00313F60`), the toggle is set to 0
   (`0x0025422A`-`0x0025423B`).
4. The latch is cleared on release only while the override is 0 (`0x00254241`-`0x00254249`).
5. The toggle is passed to the applier `0x00252B60` (`0x00254250`-`0x00254258`).

So one press flips the toggle once. After step 2 the latch is still set, so the next press clears the override but
does not flip the toggle.

### The applier

`0x00252B60(toggle, force)` decides what reaches the flag (`0x00252B60`-`0x00252C7F`):

1. With input snapshot bit 25 set it does nothing (`0x00252B7A`-`0x00252B86`).
2. When the aggregate action policy `0x002E0FA0` has bit 6, bit 9 or bit 10 set, or `0x00237260` answers non-zero, the
   toggle becomes 0 with `force` 1 (`0x00252B8C`-`0x00252BB3`). Bit 9 also sets the quiet bit through `0x00366950`.
3. A `0x020927CC` of 1 does the same (`0x00252BB6`-`0x00252BC1`).
4. The battle mode register `0x0035C6F0` can replace the toggle, in the next two steps.
5. With bit 2 or 3 of the register set, the toggle becomes input snapshot bit 9, or 0 when policy bit 10 is set
   (`0x00252BCD`-`0x00252BEC`). It writes `0x0035C880(0xC, (register & 4) * 2)`, then `0x0035C880(0xC, 0)` when the toggle
   is 0, and sets the quiet bit (`0x00252BEF`-`0x00252C0C`).
6. Otherwise, with bit 0 of the register set, the toggle becomes the register's bit 1 (`0x00252C13`-`0x00252C25`).
7. Only when `0x003603B0` and `0x003603C0` both answer 0 does it arm (`0x00252C28`-`0x00252C5D`). While the toggle is 1 it
   runs the arming step `0x00366870` and passes on the armed bit from `0x003669F0` instead of the toggle. While the
   toggle is 0 it runs the disarm step `0x003667E0`. Otherwise the toggle is passed on unarmed.
8. It calls `0x00252C80(value, force)` (`0x00252C5F`-`0x00252C63`).

### The flag

`0x00252C80(value, force)` writes the force-fight flag `0x01E0C2B8` (`0x00252C80`-`0x00252D05`). A value of 1 clears the
flag, which is Escape Mode on. A value of 0 sets it back to 1, or to 0 when the area's force-fight feature is off
(`0x003BA2E0`). Without `force` it writes only when the flag would change, and not at all while `0x003603B0` or
`0x003603C0` answers non-zero.

The flag has one other writer. `0x00254EA0(v)` is the body of the script verb `0x334` `setforcefightmode` (handler
`0x003444D0`, call `0x003444E2`): it writes 1 when `v` is non-zero and `0x003BA2E0` answers non-zero (`0x00254EB1`), and 0
otherwise (`0x00254EC5`).

### Arming

The arming state is the word `0x022CBE1A`. Both steps return at once when the battle mode register has bit 0 set
(`0x00366874`-`0x0036687B`, `0x003667E4`-`0x003667EB`).

1. `0x00366870` counts frames in `0x022CBE18`. On the first frame, bit 0 clear, it restarts the count and starts a
   repeating sound, block slot `0x52`, and sets bit 4 (`0x0036688D`-`0x003668E0`).
2. When the count reaches `0x022CBE08` it pins the count there and sets the armed bit, bit 2, and on that frame only
   also bit 3 (`0x00366902`-`0x00366918`).
3. Every frame it clears bits 1 and 6 and sets bit 0 (`0x0036691C`-`0x00366928`).
4. `0x003667E0` plays the disarm cue, block slot `0x2A` through `0x00249C60`, when the armed bit is set, `0x00265680`
   answers non-zero and the quiet bit, bit 6, is clear (`0x003667ED`-`0x0036680D`).
5. It then stops the repeating sound if it plays, clears bits 0, 2, 3, 4, 5 and 6, and sets bit 1
   (`0x00366812`-`0x0036685B`).

`0x022CBE08` is 30 times the frame-time base `0x01DFE0B4`, set once by `0x00366B80` (`0x003670A6`-`0x003670B7`): one second
of frames. Until it is reached `0x003669F0` answers 0, the applier passes 0, and the flag does not change.

Two setters skip the count. `0x00366960(on)`, run by `0x0028E580`, writes the count word `0x022CBE18` with the full
delay and the arming word `0x022CBE1A` with `0x25` (bits 0, 2 and 5: armed at once), or clears both for 0.
`0x003667B0(on)`, run by `0x00280140`, sets or clears bit 7 of the arming word.

The escape widget `0x00366B80`, built by `0x00366740` from `0x00253A30`, draws its parts with two helpers: `0x00367110(points,
node, x)` writes five points through `0x00862980`: (0, 0), (x - w, top / 2), (left - w / 2, top + h / 2),
(left + w / 4, top) and (left, top), with left, top, w and h the node's `+0x0C`, `+0x0E`, `+0x10` and `+0x12`;
and `0x00366A30(sprite, node, x, y, scale, cx, cy)` draws
a node's picture cell at (x, y) through `0x002D8D10`, scaling it and its offset from (cx, cy) by `scale / 256`
when `scale` is not 0.

### What reads the flag

`0x00253B90` answers true when the flag is 0, Escape Mode on. Its readers are command availability `0x002FFCF0`, the
engagement flag `0x00307D10`, the party's stance `0x00308130`, the combat frame `0x00308610` (the combo roll), the AI
distance threshold `0x00309A90`, `0x0030C010`, `0x00313A00`, and through its thunk `0x0030C0D0` the field frame `0x00234590`
and the battle movement step `0x00336710`, `0x00339BF0`, `0x0033A720`, `0x0033C310` and `0x0033CEF0`. What each does with it
is on [Force fight mode](../Engine-Core/force-fight-mode.md).

`0x00253BA0` returns the flag itself when `0x003BA2E0` answers non-zero, and 0 otherwise (`0x00253BAD`). It is called from
the battle menu's builder `0x00276650` (`0x0027668C`) and its panel procedure `0x00276D30` (`0x00276FD3`)
([Battle menu](../Menus-And-HUD/battle-menu.md)). Those two readers and the writers above are the only accesses
to `0x01E0C2B8`.

## Layouts

### The escape widget's fields

The escape widget is the `0xE0`-byte widget at `0x022CBE20` with procedure `0x00366B80` (State below).

`EscapeWidget` (`0xE0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00366B80` |
| `+0xC0` | `void*` | atlas | the image label battle_4_c (the name at `0x009152B0` through `0x01E0C1E8`), looked up with `0x0024A5A0` on construction (`0x003670DC`-`0x003670E1`); no function reads it back |
| `+0xC8` | `void*` | latch | the address of the latch words `0x022CBE18` that `0x00366740` passes as the construct message's second argument (`0x00367096`-`0x0036709A`). The draw fills the gauge from the count word `+0x00` against the delay `0x022CBE08` (`0x00366C5B`-`0x00366C6A`, `0x00366CE6`-`0x00366D0D`); the update reads the arming word `+0x02`: bit 7 runs the disarm `0x003667E0` (`0x00366F0E`-`0x00366F1B`), bit 3 or 5 starts the pulse and is cleared (`0x00366F40`-`0x00366F8C`), bit 2 keeps the pulse running (`0x00366F9C`-`0x00366FAC`), bits 0 and 1 fade the picture in and out (`0x00366FE6`-`0x0036701D`) |
| `+0xD0` | `i16` | alpha | the picture's alpha, 0 to 128: set to 128 when a pulse starts with bit 5 (`0x00366F5B`); rises by 128 / [`0x022CBE0C`] per update while arming bit 0 is set and falls to 0 while bit 1 is set, when no pulse runs (`0x00366FE6`-`0x00367037`); while a pulse runs the draw sets it to 96 + 32 sin(pi x frames since `+0xD4` / 30) (`0x00366BEC`-`0x00366C29`). The draw draws nothing while it is 0 (`0x00366BD0`) and scales each node's alpha `+0x58` by it (`0x00366DDC`-`0x00366E10`) |
| `+0xD2` | `i16` | brightness | the picture's brightness scale: 255 when a pulse starts with bit 3 and without bit 5 (`0x00366F71`-`0x00366F80`), 128 with bit 5 (`0x00366F5B`); each update takes 128 / [`0x022CBE14`] from it down to 128 (`0x00366FB4`-`0x00366FD0`). The draw multiplies the draw record's brightness `+0x5A` by it over 128 (`0x00366D6F`-`0x00366D86`) |
| `+0xD4` | `u32` | pulseStart | the frame counter `0x0208F570` when the pulse started (`0x00366F90`-`0x00366F96`); the draw's pulse takes the frames since then (`0x00366BEC`-`0x00366BF5`) |
| `+0xD8` | `u16` | pulsing | 1 while the armed pulse runs: set with `+0xDA` by one dword store when arming bit 3 or 5 is seen (`0x00366F65`, `0x00366F76`); the update clears it while arming bit 2 is clear (`0x00366FA6`-`0x00366FAC`). While it is set the update leaves the alpha alone (`0x00366FD8`), the draw pulses the alpha (`0x00366BDE`) and draws the ring copy (`0x00366E2B`) |
| `+0xDA` | `u16` | ringScale | the scale of the expanding copy, in 256ths: `0x100` when the pulse starts with bit 3 (`0x00366F76`), `0x200` with bit 5 (`0x00366F65`); each update adds `0x20` up to `0x200` (`0x00366F20`-`0x00366F38`). While it is below `0x200` the draw draws each node a second time at this scale with its alpha times (`0x200` - scale) / 256 (`0x00366E35`-`0x00366E8B`) |
| `+0xDC` | `u8[4]` | tail0DC | read and written by no function; nothing fixes its width |

## State

The escape widget `0x00366B80` sets these when it is built (message 1, `0x003670A6`-`0x003670D6`), from the frame-time
base `0x01DFE0B4`, 1 as shipped, beside the delay `0x022CBE08`. Its update (message 2, `0x00366EFB`-`0x003670E8`) moves the
picture's alpha `+0xD0` and brightness `+0xD2` by 128 divided by them; its draw reads both (`0x00366D6F`, `0x00366DDC`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CBE0C` | `i32` | 0 | the frames the picture takes to fade, 30 times the base over 6, so 5: while the arming word `0x022CBE1A` has bit 0 the alpha rises by `128 / 5` a frame to 128, and while it has bit 1 it falls to 0 (`0x00366FE6`-`0x00367037`); the pulse of an armed escape replaces both | `0x00366B80` (`0x003670D0`) | `0x00366B80` (`0x00366FF3`, `0x00367024`) |
| `0x022CBE10` | `i32` | 0 | 30 times the base, the same value as `0x022CBE08`; nothing reads it | `0x00366B80` (`0x003670C0`) | no instruction |
| `0x022CBE14` | `i32` | 0 | the frames the picture's brightness takes to settle, 20 times the base: when the escape is armed with bit 3 and without bit 5 the brightness jumps to 255 (`0x00366F71`-`0x00366F80`), and each update takes `128 / 20` from it down to 128 (`0x00366FB4`-`0x00366FD0`) | `0x00366B80` (`0x003670D6`) | `0x00366B80` (`0x00366FB9`) |
| `0x022CBE20` | `void*` | 0 | the escape widget: the `0xE0`-byte widget with procedure `0x00366B80` that `0x00366740` creates through `0x00244F50` and opens (`0x00246AC0`), passing it the address `0x022CBE18` | `0x00366740` (`0x0036678D`), run by the field set-up `0x00253A30` (`0x00253A57`); `0x00366A00`, 0 after it destroys the widget with `0x00245020` (`0x00366A15`), run by `0x00252DE0` (`0x00252E15`) | `0x00366740`, which builds it only while it is 0 (`0x00366753`); `0x00366A00` (`0x00366A04`) |

No other instruction reaches these four.

## Modding notes

- The flag is the opposite of the toggle: Escape Mode on is the force-fight flag at 0.
- A script that forces a fight sets the flag through `setforcefightmode` (`0x00254EA0`); the next frame's applier
  writes it again only when the toggle changes, or when a policy bit forces it.
- The one-second delay is `0x022CBE08`, set from the frame-time base when the sound object is built.

## Related

- [keymap.ini](keymap-file.md) - the R2 binding.
- [Force fight mode](../Engine-Core/force-fight-mode.md) - the flag's readers.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the town bit.
