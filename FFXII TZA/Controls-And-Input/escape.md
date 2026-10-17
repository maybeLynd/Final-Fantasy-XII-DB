---
title: "Escape Mode: the R2 toggle that makes the party run from battle, what it switches off, and why it takes a second to engage"
kind: "system"
category: "Controls and input"
addresses: "0017DE10, 00253C70, 00252B60, 00252C80, 00366870, 01E0C2B8"
---

## What the player sees

- Pressing R2 switches Escape Mode on, and pressing it again switches it off; the button does not have to be held.
- Escape Mode takes about a second to engage after the press, with a sound while it arms.
- In towns it switches itself off as soon as R2 is released.
- While it is on, the party runs instead of fighting: the commands offered, combos, engagement and battle movement all
  change.

## How it works

### The button

`0017DE10` answers whether the R2 binding is held. It reads the stored word directly: `00197710(manager, 0, 0, 9)`
returns slot 9 of the first profile, `[Keyboard1]`, from `01F80F90` (`0017DE2A`-`0017DE32`, `0019775A`-`0019776F`),
not from the published copy, which has L2 and R2 cleared ([keymap.ini](keymap-file.md)). The code is tested on the current input device (`0079E6A0`). It is a
level, not a press; the press is made by the latch below.

### The latch

The input arbiter `00253C70` keeps the toggle `020927E0`, a press latch `020927E4` and an override `01E0C2B4`, and
nothing else touches them (`002541D4`-`00254258`):

1. While R2 is held, the override is cleared, and on the first frame of the press the toggle flips
   (`002541D4`-`002541FD`); the latch then stays set.
2. When R2 is released, input snapshot bit 9 (`02F97360`) is set and `00862CF0` does not answer 1, the toggle and the
   override are set to 1 (`0025420A`-`00254228`), and the latch is left set.
3. Otherwise, when the override is set or the area's town bit is set (`00313F60`), the toggle is set to 0
   (`0025422A`-`0025423B`).
4. The latch is cleared on release only while the override is 0 (`00254241`-`00254249`).
5. The toggle is passed to the applier `00252B60` (`00254250`-`00254258`).

So one press flips the toggle once. After step 2 the latch is still set, so the next press clears the override but
does not flip the toggle.

### The applier

`00252B60(toggle, force)` decides what reaches the flag (`00252B60`-`00252C7F`):

1. With input snapshot bit 25 set it does nothing (`00252B7A`-`00252B86`).
2. When the aggregate action policy `002E0FA0` has bit 6, bit 9 or bit 10 set, or `00237260` answers non-zero, the
   toggle becomes 0 with `force` 1 (`00252B8C`-`00252BB3`). Bit 9 also sets the quiet bit through `00366950`.
3. A `020927CC` of 1 does the same (`00252BB6`-`00252BC1`).
4. The battle mode register `0035C6F0` can replace the toggle, in the next two steps.
5. With bit 2 or 3 of the register set, the toggle becomes input snapshot bit 9, or 0 when policy bit 10 is set
   (`00252BCD`-`00252BEC`). It writes `0035C880(Ch, (register & 4) * 2)`, then `0035C880(Ch, 0)` when the toggle
   is 0, and sets the quiet bit (`00252BEF`-`00252C0C`).
6. Otherwise, with bit 0 of the register set, the toggle becomes the register's bit 1 (`00252C13`-`00252C25`).
7. Only when `003603B0` and `003603C0` both answer 0 does it arm (`00252C28`-`00252C5D`). While the toggle is 1 it
   runs the arming step `00366870` and passes on the armed bit from `003669F0` instead of the toggle. While the
   toggle is 0 it runs the disarm step `003667E0`. Otherwise the toggle is passed on unarmed.
8. It calls `00252C80(value, force)` (`00252C5F`-`00252C63`).

### The flag

`00252C80(value, force)` writes the force-fight flag `01E0C2B8` (`00252C80`-`00252D05`). A value of 1 clears the
flag, which is Escape Mode on. A value of 0 sets it back to 1, or to 0 when the area's force-fight feature is off
(`003BA2E0`). Without `force` it writes only when the flag would change, and not at all while `003603B0` or
`003603C0` answers non-zero.

The flag has one other writer. `00254EA0(v)` is the body of the script verb `334`<sub>h</sub> `setforcefightmode` (handler
`003444D0`, call `003444E2`): it writes 1 when `v` is non-zero and `003BA2E0` answers non-zero (`00254EB1`), and 0
otherwise (`00254EC5`).

### Arming

The arming state is the word `022CBE1A`. Both steps return at once when the battle mode register has bit 0 set
(`00366874`-`0036687B`, `003667E4`-`003667EB`).

1. `00366870` counts frames in `022CBE18`. On the first frame, bit 0 clear, it restarts the count and starts a
   repeating sound, block slot `52`<sub>h</sub>, and sets bit 4 (`0036688D`-`003668E0`).
2. When the count reaches `022CBE08` it pins the count there and sets the armed bit, bit 2, and on that frame only
   also bit 3 (`00366902`-`00366918`).
3. Every frame it clears bits 1 and 6 and sets bit 0 (`0036691C`-`00366928`).
4. `003667E0` plays the disarm cue, block slot `2A`<sub>h</sub> through `00249C60`, when the armed bit is set, `00265680`
   answers non-zero and the quiet bit, bit 6, is clear (`003667ED`-`0036680D`).
5. It then stops the repeating sound if it plays, clears bits 0, 2, 3, 4, 5 and 6, and sets bit 1
   (`00366812`-`0036685B`).

`022CBE08` is 30 times the frame-time base `01DFE0B4`, set once by `00366B80` (`003670A6`-`003670B7`): one second
of frames. Until it is reached `003669F0` answers 0, the applier passes 0, and the flag does not change.

Two setters skip the count. `00366960(on)`, run by `0028E580`, writes the count word `022CBE18` with the full
delay and the arming word `022CBE1A` with `25`<sub>h</sub> (bits 0, 2 and 5: armed at once), or clears both for 0.
`003667B0(on)`, run by `00280140`, sets or clears bit 7 of the arming word.

The escape widget `00366B80`, built by `00366740` from `00253A30`, draws its parts with two helpers: `00367110(points,
node, x)` writes five points through `00862980`: (0, 0), (x - w, top / 2), (left - w / 2, top + h / 2),
(left + w / 4, top) and (left, top), with left, top, w and h the node's `+0C`<sub>h</sub>, `+0E`<sub>h</sub>, `+10`<sub>h</sub> and `+12`<sub>h</sub>;
and `00366A30(sprite, node, x, y, scale, cx, cy)` draws
a node's picture cell at (x, y) through `002D8D10`, scaling it and its offset from (cx, cy) by `scale / 256`
when `scale` is not 0.

### What reads the flag

`00253B90` answers true when the flag is 0, Escape Mode on. Its readers are command availability `002FFCF0`, the
engagement flag `00307D10`, the party's stance `00308130`, the combat frame `00308610` (the combo roll), the AI
distance threshold `00309A90`, `0030C010`, `00313A00`, and through its thunk `0030C0D0` the field frame `00234590`
and the battle movement step `00336710`, `00339BF0`, `0033A720`, `0033C310` and `0033CEF0`. What each does with it
is on [Force fight mode](../Engine-Core/force-fight-mode.md).

`00253BA0` returns the flag itself when `003BA2E0` answers non-zero, and 0 otherwise (`00253BAD`). It is called from
the battle menu's builder `00276650` (`0027668C`) and its panel procedure `00276D30` (`00276FD3`)
([Battle menu](../Menus-And-HUD/battle-menu.md)). Those two readers and the writers above are the only accesses
to `01E0C2B8`.

## Modding notes

- The flag is the opposite of the toggle: Escape Mode on is the force-fight flag at 0.
- A script that forces a fight sets the flag through `setforcefightmode` (`00254EA0`); the next frame's applier
  writes it again only when the toggle changes, or when a policy bit forces it.
- The one-second delay is `022CBE08`, set from the frame-time base when the sound object is built.

## Related

- [keymap.ini](keymap-file.md) - the R2 binding.
- [Force fight mode](../Engine-Core/force-fight-mode.md) - the flag's readers.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the town bit.
