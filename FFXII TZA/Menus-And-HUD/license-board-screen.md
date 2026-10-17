---
title: "License Board screen: the board chooser, the square grid and its states, the change sweep, preview, and obtaining a license"
kind: "system"
category: "Menus and HUD"
addresses: "0055B3F0, 0055BFF0, 0055B310, 0055DD70, 0055CD40, 00557DB0, 0055D978, 0055F3E0"
---

## What the player sees

- Licenses asks for a character, then shows that character's license board; a character without a board first picks
  one of the twelve boards ("Choose this license board?").
- Owned squares are lit, the squares next to them can be obtained, and the rest of the board stays dark.
- Obtaining a square asks for confirmation, plays an effect, lights the neighbours one after another, and may
  announce a new Esper, a new Mist ability or the Second Board.
- From the board chooser, a board can be previewed without choosing it.

## How it works

### Opening

The member-pick widget `00560910` opens one of two screens (`00560910` messages 2, 12 and 20):

| The member has | Screen | Built by |
|---|---|---|
| a board | the board screen `00561390` with the view `0055CD40` | `00561300(self, 0, FFh)` (`00560C98`) |
| no board | the chooser window `00558FB0` with the chooser `00557DB0` | `00558F20` (`00560C89`) |

The board screen loads `lic_bk`, `cm2_win_c`, `lic_8_c`, `lic_8_c2` and `lic_8_c3`, and the per-node art table into
`[02CA9670]` (`005615C4`-`00561765`).

### The board chooser

The chooser steps through the twelve boards with left and right (`00557B90`), showing each board's name
(`menu_command.bin` `3ED`<sub>h</sub> + board) and description (`menu_message.bin` `838`<sub>h</sub> + board) in the description box
([Dialogs](dialogs.md)). Its stage byte `+37D`<sub>h</sub> runs the opening (`00557DF0`):

1. The first visit to the chooser shows "You must choose a license board in order to obtain licenses. ..." (`836`<sub>h</sub>)
   once per save, and sets the save-wide flag `BB`<sub>h</sub> (`00252D10`).
2. Confirm asks "Choose this license board?" (`835`<sub>h</sub>, `00558607`).
3. Yes plays three cues and stores the board: `00323740(row, board)` for a first board, or `003236F0(row, board)` for
   the second (`00558630`-`00558668`). [License Board](../Items-Equipment-Shops-And-Licenses/license-board.md) has the
   two board slots.

### Building the grid

`0055B3F0` picks the board shown, the member's stats byte `+1C5`<sub>h</sub> (`003236B0`, `0055B446`), and sizes the view from
the board file: width + 1 by height + 1 (`0055B484`-`0055B4A2`). The extra column and row are always empty. It fills a
tile byte per square with `table[(rand() & 3) + 4 x ((col + row) & 1)]` (`0055B4E0`-`0055B517`), the table being
`00 02 04 06 01 03 05 07`, so even and odd squares draw from different sets of variants.

`0055B560` allocates the squares, `38`<sub>h</sub> bytes each (`0055B63C`), and runs the fill `0055BFF0`. For each square inside
the board it reads the board cell, then the license node's record (`0035D330(19h, node)`, `0055C0FA`-`0055C15C`) and
the member's answer for the node (`00323600`, which calls `00323D10`; [Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md)). The script verb
`fsmenu_getneedlp` (`005112E0`) returns a node's LP cost through `00282E60`, the record byte the square's `lpCost`
is copied from (`0055C117`).

- A Quickening square shows the member's own Quickening in the order bought, from `00D230B0` and bank-8 words
  `row x 3 + 53h` (`0055C16F`-`0055C247`).
- An Esper square shows the Esper's name once obtained (`0055C260`-`0055C284`).
- The ten Gambit Slot squares (nodes 266-275) are left out unless the Gambits command is available
  (`00283730(4B9h)`, `0032A8A0(4009h)`, `0055C34E`-`0055C38B`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32[2]` | name | the square's name string |
| `08`<sub>h</sub> | `u16` | node | license node, `FFFF`<sub>h</sub> for an empty or hidden square |
| `0B`<sub>h</sub> | `u8` | rule | node byte `+06`<sub>h</sub>: 1, 2 or 3 choose the confirm text |
| `0C`<sub>h</sub> | `u16` | lpCost | node byte `+04`<sub>h</sub> |
| `0E`<sub>h</sub> | `u16` | artNode | row of the art table [`02CA9670`] |
| `10`<sub>h</sub> | `u32[2]` | kindText | the kind of license, Weapon to Gambit (`4280`<sub>h</sub>-`4289`<sub>h</sub>) |
| `18`<sub>h</sub> | `u32` | state | bits 0-3 corner shape, 4-7 state, 8-11 state shown, 12-15 purchase flags |
| `20`<sub>h</sub> | `u8` | col | column |
| `21`<sub>h</sub> | `u8` | row | row |
| `22`<sub>h</sub> | `u8` | phase | 0 idle, 1 effect armed, 2 countdown, 3 effect playing (`0055F010`) |
| `23`<sub>h</sub> | `u8` | pending | the state the transition will show |
| `24`<sub>h</sub> | `u8` | tile | tile variant 0-7 |
| `25`<sub>h</sub> | `u8` | alpha | `80`<sub>h</sub> when built |
| `26`<sub>h</sub> | `u8` | fadeLeft | fade counter |
| `27`<sub>h</sub> | `u8` | fadeLen | fade length |
| `28`<sub>h</sub> | `u8` | fadeOn | fade running |
| `29`<sub>h</sub> | `u8` | fadeIn | fade direction |
| `2A`<sub>h</sub> | `i16` | countdown frames before the pending state shows |  |
| `2C`<sub>h</sub> | `u32` | effect | the playing effect (`003B2D80`) |
| `30`<sub>h</sub> | `u32` | category | node byte `+05`<sub>h</sub>; `1E`<sub>h</sub> is the Second Board |

### Square states

The member's answer for the node sets the purchase flags through the table at `0055C504`:

| Answer | Flags |
|---|---|
| 0, can be obtained | bit 14 when the cost is at most the member's LP (`0055C492`), and bit 15 |
| 1, owned | bits 12 and 13, state 5 (`0055C472`) |
| `2` | bit 15 unless bit 12 |
| `3`, `4`, `5`, `8` | the square is emptied (`0055C4CA`) |

`0055E090` then turns bit 15 into bit 12 on each square next to an owned one. So bit 13 means owned, bit 12
obtainable now, bit 14 affordable and bit 15 obtainable later. The state nibble, bits 4-7, takes four values:

| State | Meaning | Set by |
|---:|---|---|
| `0` | empty | the fill |
| `1` | a square not yet next to an owned one | `0055E230` |
| `4` | next to an owned square | `0055E3F0(view, 4, owned)` |
| `5` | owned | answer 1, or the purchase (`0055F641`) |

Squares in states 4 and 5, and Esper and Second Board squares in state 1, are drawn with their art (`0055BAC0`). A
state-4 square shows its LP cost when zoomed in.

### Corner shapes

`0055DEA0` gives each square a corner piece in bits 0-3 from the squares to its left, above and above-left
(`0055DF32`-`0055DF94`). It looks the three tests up in the 2 x 7 table at `00D230F8`, using the second row when the
square itself is empty, and stores the entry plus 1. `0055AE80` draws the piece half a cell offset, so the grid of
squares also forms the grid of joins between them.

### The change sweep

The sweep `0055B310` walks the squares and finds those whose state differs from the state shown
(`0055B361`-`0055B36C`):

1. With the view's collect bit set, it lists up to 32 changed squares at `+308`<sub>h</sub> (`0055B380`-`0055B390`).
2. Without it, it copies each state into the state shown at once (`0055B398`-`0055B3A6`).

After a purchase, `0055DD70` sets the collect bit, runs the fill and gives each listed square a transition
(`0055DDC6`-`0055DE80`): a newly reachable square shows state 4 after `2E`<sub>h</sub> frames with an effect, and an emptied
square fades out. A square past the 32nd keeps its old look until the next sweep. `0055F010` runs the transitions
every frame.

### Preview

The chooser's preview control closes it with the board in hand, and the window opens the board screen with the
preview flag (`005590E3`, `00557B90`). In the view (`+570`<sub>h</sub> bit 10, `0055CEB2`):

- the board shown is the previewed one (`0055B436`);
- the cursor starts on Essentials, node `1F`<sub>h</sub> (`0055E600`);
- obtaining squares and changing members are refused with sound 5, and the board switch is ignored (`0055C740`).

Leaving the preview reopens the chooser on the same board (`005614A1`).

### Scripted cursor moves

Two script verbs move the view's cursor for lessons: `00560070` (from `00511F50`) walks it to a node, one injected
direction step at a time (`002D66A0`), and `0055F740` (from `00511FE0`) marks the move done after a purchase. The
mover is `0055AA00`, on `+563`<sub>h</sub>.

### Obtaining a license

1. The confirm button (`01E0C2A0`) on a square opens its detail panel (`0055A1F0`); the cancel button (`01E0C2A4`)
   closes it.
2. Confirm again sends take-square (`8001`<sub>h</sub>) to the view (`0055D617`):
   - the owned Second Board square, when the member has no second board yet (`00323630`), closes the board and
     opens the chooser for the second board (`0055D633`-`0055D6E5`);
   - any other owned square, or one that cannot be obtained yet, plays sound 5;
   - an obtainable square the member cannot afford shows "Insufficient license points." (`CD9`<sub>h</sub>, `0055D709`);
   - an obtainable, affordable square asks for confirmation.
3. The question depends on the square (`0055D73A`-`0055D774`):

   | Square | Question (`menu_message.bin`) |
   |---|---|
   | rule 1 | "Only one character can obtain this license. Obtain {name}?" (`861`<sub>h</sub>) |
   | rule 2 (Quickening) | "Each character can obtain up to three quickening licenses from those available on the board. Learn {name}?" (`863`<sub>h</sub>) |
   | rule 3 (Esper) | "Only one character can obtain the license for this Esper. Obtain {name}?" (`864`<sub>h</sub>) |
   | Second Board | "You will be unable to return to the License menu until you confirm your new board. Proceed anyway?" (`88D`<sub>h</sub>) |
   | any other | "Obtain {name}?" (`860`<sub>h</sub>) |

4. Yes reaches `0055D978`. It records the node taken in bank 8, then obtains it with `003235C0(row, node, 1)`
   (`0055DA6E`), which calls `00323910` and charges the LP. This is the only call of `003235C0`.
5. `0055F3E0` then runs the purchase stages on `+55E`<sub>h</sub>: it pans to the square, lights it (`0055F641`), runs the
   sweep (`0055DD70`), waits for the transitions, and shows the notices.

| Notice (`listhelp_license.bin`) | When |
|---|---|
| "{name} has learned a new Mist ability!" (`426C`<sub>h</sub>) | the member's Mist count grew (`+570`<sub>h</sub> bit 5) |
| "The character can now summon Espers under the Mist command in the Battle Menu." (`4269`<sub>h</sub>) | the first Esper obtained |
| "The character can now perform quickenings under the Mist command ..." (`426A`<sub>h</sub>) | the first Quickening obtained |
| "The license for the Esper {name} has been added to the board!" (`426B`<sub>h</sub>) | when the board opens with a new Esper square (`0055E9E0`) |
| "The Second Board license has been added to the license board!" (`428A`<sub>h</sub>) | the same, for the Second Board square |

Obtaining the Second Board ends with the chooser opening for the member's second board (`0055F3E0` stage 4).

### Grid helpers

- `0055E3F0(view, state, test)` gives state 4 to squares next to one passing `00556580` (bit 13, owned) and state 1
  to those passing `00556570` (a node other than `FFFF`<sub>h</sub>) (`0055C3E5`, `0055C3F6`).
- `00556590(square)` returns the art row's word `+22`<sub>h</sub> of `[02CA9670]` for a state-4 square, or the default at
  `+5A62`<sub>h</sub> when it has no art row; 0 for other states.
- `0055EF10(view)` runs every square's transition (`0055F010`) and fade (alpha `+25`<sub>h</sub> from `+26`<sub>h</sub>/`+27`<sub>h</sub>, rising or
  falling by `+29`<sub>h</sub>), and plays sound `4A`<sub>h</sub> once when a transition returns `10`<sub>h</sub>. `0055B2B0(view)` returns 1 while
  any square still fades or counts down.
- `0055B8C0(view)` starts a 6-frame pan toward the cursor square (`+550`<sub>h</sub>/`+551`<sub>h</sub> times the cell size `+554`<sub>h</sub>) when
  the view is not there; `0055F1C0` runs the pan (`00248F40`) and the cursor's pulse `+191`<sub>h</sub> in five steps.
- `0055B960(view, dx, dy, now)` gives the scroll `d` that keeps the cursor inside the view. Unless `now`,
  each axis takes `s = d >> 4` (arithmetic), `s = d / abs(d)` when that is 0, and an odd `s` one further from 0
  (`0055BA33`-`0055BA5F` for x, `0055BA6E`-`0055BA91` for y).
- `00561F20` clamps a scroll to its limits: `+10h = min(max(+10h, +08h), +0Ch)` and
  `+12h = min(max(+12h, +0Ah), +0Eh)`, all `s16`.
- `0055AB20` tiles the background picture `+180`<sub>h</sub> over the screen in batches of 12 (`002D9380`); `0055B6D0` draws
  the cursor frame `+188`<sub>h</sub>, inset by the pulse.

### Detail panel and member switch

- `0055A180(view, square)` fills the four detail panes (`+140`<sub>h</sub>) through `00559E30`, or closes the panel when it is
  open (`0055A1F0`). `005597C0` closes the panes (`00244F00`) and `00559800(view, v)` hides or shows them.
- `00559E30(pane)` shows the square's name and LP cost (`0029FF60`), its kind icon (`12`<sub>h</sub> for category `1E`<sub>h</sub>) and up
  to eight contents from the node record `0035D330(19h, node)` `+26`<sub>h</sub>, by its list type `+23`<sub>h</sub>: class 1 records
  for type 0, class `14`<sub>h</sub> records for type 1 (with the icon of the class 1 record each names), and class `1D`<sub>h</sub>
  names for types 2 and 3.
- `0055AE00` and `0055B840` step to another member that has a board (`0027EDA0` or `0027F430` with the test
  `005617E0`), play sound `51`<sub>h</sub> and rebuild the view (`0055DBD0`); `00557A40` and `00557A90` do the same in the chooser
  (`00558760`).

### Chooser helpers

- `00556380(slot, board1, board2, current)` builds the line of one or two board names (`menu_command.bin` `3ED`<sub>h</sub> +
  board, joined by `3F9`<sub>h</sub>) into `02CA8FF0` + slot x 256, colouring one name with colour 3 (`002AB870`);
  `00558E70` shows it for the member, and `00556F50` hands the text of a row to its label.
- `005587E0(chooser)` lists, for up to six members (`00282DF0`, `00282FA0`), which board each holds as first
  (`00323670`) and second board (`00323630`).
- `00558A10(chooser, board, curve, frames)` turns the board wheel to `board` (30 degrees a board, crossing 360 between
  boards 0 and 11), and `00558AF0` steps it (`00248F40`) into the angle `+34C`<sub>h</sub>.
- `005574C0` draws a chooser picture as four mirrored quarters at 0.8 scale (`002DB080`).
- `00561020` releases the chooser's five widgets and two buffers.
- `002CE280(window)` puts a window, its child `+C0`<sub>h</sub> and that child's `+D8`<sub>h</sub> into the second draw pass
  (`00247730(widget, 1)`); the chooser (`005584CE`), the board view (`0055D71E`, `0055D784`), `0055E9E0` and
  `0055F3E0` call it.

### The member picker

`00560910` lists the members with `00561100`: the roster slot of each one `00282FA0` accepts and its portrait
(`002526F0(8, id + 4Dh, 1)`). `00560610` draws a member's board in miniature, one cell per square of the board table
`[02EBF1A0 + board]` coloured `002DD7E0(DBh + value)`, and `0055FA50` frees the six cell arrays at `+150`<sub>h</sub>.

## Shipped data

| | |
|---|---|
| boards | 12, each 24 x 24 squares in the file, 25 x 25 on screen (625 squares, 49 of them the empty border) |
| Gambit Slot squares | 10 on each board, 120 in all |

## Modding notes

- The view is the board file plus one row and column; a larger board needs `+559`<sub>h</sub>/`+55A`<sub>h</sub> to fit a byte.
- The screen tests LP against the menu record's `+B0`<sub>h</sub> (`0055C496`), and the purchase charges the member's stats
  record.
- One purchase animates at most 32 changed squares; the rest change without an effect.

## Related

- [License Board](../Items-Equipment-Shops-And-Licenses/license-board.md) - the board file and the two board slots.
- [Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md) - the node records and what obtaining one does.
- [Dialogs](dialogs.md) - the description box and the confirm and notice boxes.
- [Menus](menus.md) - the Licenses entry.
