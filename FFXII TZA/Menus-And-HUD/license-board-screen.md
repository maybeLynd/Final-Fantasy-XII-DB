---
title: "License Board screen: the board chooser, the square grid and its states, the change sweep, preview, and obtaining a license"
kind: "system"
category: "Menus and HUD"
addresses: "0x0055B3F0, 0x0055BFF0, 0x0055B310, 0x0055DD70, 0x0055CD40, 0x00557DB0, 0x0055D978, 0x0055F3E0"
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

The member-pick widget `0x00560910` opens one of two screens (`0x00560910` messages 2, 12 and 20):

| The member has | Screen | Built by |
|---|---|---|
| a board | the board screen `0x00561390` with the view `0x0055CD40` | `0x00561300(self, 0, 0xFF)` (`0x00560C98`) |
| no board | the chooser window `0x00558FB0` with the chooser `0x00557DB0` | `0x00558F20` (`0x00560C89`) |

The board screen loads `lic_bk`, `cm2_win_c`, `lic_8_c`, `lic_8_c2` and `lic_8_c3`, and the per-node art table into
`[0x02CA9670]` (`0x005615C4`-`0x00561765`).

### The board chooser

The chooser steps through the twelve boards with left and right (`0x00557B90`), showing each board's name
(`menu_command.bin` `0x3ED` + board) and description (`menu_message.bin` `0x838` + board) in the description box
([Dialogs](dialogs.md)). Its stage byte `+0x37D` runs the opening (`0x00557DF0`):

1. The first visit to the chooser shows "You must choose a license board in order to obtain licenses. ..." (`0x836`)
   once per save, and sets the save-wide flag `0xBB` (`0x00252D10`).
2. Confirm asks "Choose this license board?" (`0x835`, `0x00558607`).
3. Yes plays three cues and stores the board: `0x00323740(row, board)` for a first board, or `0x003236F0(row, board)` for
   the second (`0x00558630`-`0x00558668`). [License Board](../Items-Equipment-Shops-And-Licenses/license-board.md) has the
   two board slots.

### Building the grid

`0x0055B3F0` picks the board shown, the member's stats byte `+0x1C5` (`0x003236B0`, `0x0055B446`), and sizes the view from
the board file: width + 1 by height + 1 (`0x0055B484`-`0x0055B4A2`). The extra column and row are always empty. It fills a
tile byte per square with `table[(rand() & 3) + 4 x ((col + row) & 1)]` (`0x0055B4E0`-`0x0055B517`), the table being
`00 02 04 06 01 03 05 07`, so even and odd squares draw from different sets of variants.

`0x0055B560` allocates the squares, 0x38 bytes each (`0x0055B63C`), and runs the fill `0x0055BFF0`. For each square inside
the board it reads the board cell, then the license node's record (`0x0035D330(0x19, node)`, `0x0055C0FA`-`0x0055C15C`) and
the member's answer for the node (`0x00323600`, which calls `0x00323D10`; [Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md)). The script verb
`fsmenu_getneedlp` (`0x005112E0`) returns a node's LP cost through `0x00282E60`, the record byte the square's `lpCost`
is copied from (`0x0055C117`).

- A Quickening square shows the member's own Quickening in the order bought, from `0x00D230B0` and bank-8 words
  `row x 3 + 0x53` (`0x0055C16F`-`0x0055C247`).
- An Esper square shows the Esper's name once obtained (`0x0055C260`-`0x0055C284`).
- The ten Gambit Slot squares (nodes 266-275) are left out unless the Gambits command is available
  (`0x00283730(0x4B9)`, `0x0032A8A0(0x4009)`, `0x0055C34E`-`0x0055C38B`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32[2]` | name | the square's name string |
| `+0x08` | `u16` | node | license node, `0xFFFF` for an empty or hidden square |
| `+0x0B` | `u8` | rule | node byte `+0x06`: 1, 2 or 3 choose the confirm text |
| `+0x0C` | `u16` | lpCost | node byte `+0x04` |
| `+0x0E` | `u16` | artNode | row of the art table [`0x02CA9670`] |
| `+0x10` | `u32[2]` | kindText | the kind of license, Weapon to Gambit (`0x4280`-`0x4289`) |
| `+0x18` | `u32` | state | bits 0-3 corner shape, 4-7 state, 8-11 state shown, 12-15 purchase flags |
| `+0x20` | `u8` | col | column |
| `+0x21` | `u8` | row | row |
| `+0x22` | `u8` | phase | 0 idle, 1 effect armed, 2 countdown, 3 effect playing (`0x0055F010`) |
| `+0x23` | `u8` | pending | the state the transition will show |
| `+0x24` | `u8` | tile | tile variant 0-7 |
| `+0x25` | `u8` | alpha | `0x80` when built |
| `+0x26` | `u8` | fadeLeft | fade counter |
| `+0x27` | `u8` | fadeLen | fade length |
| `+0x28` | `u8` | fadeOn | fade running |
| `+0x29` | `u8` | fadeIn | fade direction |
| `+0x2A` | `i16` | countdown frames before the pending state shows |  |
| `+0x2C` | `u32` | effect | the playing effect (`0x003B2D80`) |
| `+0x30` | `u32` | category | node byte `+0x05`; `0x1E` is the Second Board |

### Square states

The member's answer for the node sets the purchase flags through the table at `0x0055C504`:

| Answer | Flags |
|---|---|
| 0, can be obtained | bit 14 when the cost is at most the member's LP (`0x0055C492`), and bit 15 |
| 1, owned | bits 12 and 13, state 5 (`0x0055C472`) |
| `2` | bit 15 unless bit 12 |
| `3`, `4`, `5`, `8` | the square is emptied (`0x0055C4CA`) |

`0x0055E090` then turns bit 15 into bit 12 on each square next to an owned one. So bit 13 means owned, bit 12
obtainable now, bit 14 affordable and bit 15 obtainable later. The state nibble, bits 4-7, takes four values:

| State | Meaning | Set by |
|---:|---|---|
| `0` | empty | the fill |
| `1` | a square not yet next to an owned one | `0x0055E230` |
| `4` | next to an owned square | `0x0055E3F0(view, 4, owned)` |
| `5` | owned | answer 1, or the purchase (`0x0055F641`) |

Squares in states 4 and 5, and Esper and Second Board squares in state 1, are drawn with their art (`0x0055BAC0`). A
state-4 square shows its LP cost when zoomed in.

### Corner shapes

`0x0055DEA0` gives each square a corner piece in bits 0-3 from the squares to its left, above and above-left
(`0x0055DF32`-`0x0055DF94`). It looks the three tests up in the 2 x 7 table at `0x00D230F8`, using the second row when the
square itself is empty, and stores the entry plus 1. `0x0055AE80` draws the piece half a cell offset, so the grid of
squares also forms the grid of joins between them.

### The change sweep

The sweep `0x0055B310` walks the squares and finds those whose state differs from the state shown
(`0x0055B361`-`0x0055B36C`):

1. With the view's collect bit set, it lists up to 32 changed squares at `+0x308` (`0x0055B380`-`0x0055B390`).
2. Without it, it copies each state into the state shown at once (`0x0055B398`-`0x0055B3A6`).

After a purchase, `0x0055DD70` sets the collect bit, runs the fill and gives each listed square a transition
(`0x0055DDC6`-`0x0055DE80`): a newly reachable square shows state 4 after 0x2E frames with an effect, and an emptied
square fades out. A square past the 32nd keeps its old look until the next sweep. `0x0055F010` runs the transitions
every frame.

### Preview

The chooser's preview control closes it with the board in hand, and the window opens the board screen with the
preview flag (`0x005590E3`, `0x00557B90`). In the view (`+0x570` bit 10, `0x0055CEB2`):

- the board shown is the previewed one (`0x0055B436`);
- the cursor starts on Essentials, node `0x1F` (`0x0055E600`);
- obtaining squares and changing members are refused with sound 5, and the board switch is ignored (`0x0055C740`).

Leaving the preview reopens the chooser on the same board (`0x005614A1`).

### Scripted cursor moves

Two script verbs move the view's cursor for lessons: `0x00560070` (from `0x00511F50`) walks it to a node, one injected
direction step at a time (`0x002D66A0`), and `0x0055F740` (from `0x00511FE0`) marks the move done after a purchase. The
mover is `0x0055AA00`, on `+0x563`.

### Obtaining a license

1. The confirm button (`0x01E0C2A0`) on a square opens its detail panel (`0x0055A1F0`); the cancel button (`0x01E0C2A4`)
   closes it.
2. Confirm again sends take-square (`0x8001`) to the view (`0x0055D617`):
   - the owned Second Board square, when the member has no second board yet (`0x00323630`), closes the board and
     opens the chooser for the second board (`0x0055D633`-`0x0055D6E5`);
   - any other owned square, or one that cannot be obtained yet, plays sound 5;
   - an obtainable square the member cannot afford shows "Insufficient license points." (`0xCD9`, `0x0055D709`);
   - an obtainable, affordable square asks for confirmation.
3. The question depends on the square (`0x0055D73A`-`0x0055D774`):

   | Square | Question (`menu_message.bin`) |
   |---|---|
   | rule 1 | "Only one character can obtain this license. Obtain {name}?" (`0x861`) |
   | rule 2 (Quickening) | "Each character can obtain up to three quickening licenses from those available on the board. Learn {name}?" (`0x863`) |
   | rule 3 (Esper) | "Only one character can obtain the license for this Esper. Obtain {name}?" (`0x864`) |
   | Second Board | "You will be unable to return to the License menu until you confirm your new board. Proceed anyway?" (`0x88D`) |
   | any other | "Obtain {name}?" (`0x860`) |

4. Yes reaches `0x0055D978`. It records the node taken in bank 8, then obtains it with `0x003235C0(row, node, 1)`
   (`0x0055DA6E`), which calls `0x00323910` and charges the LP. This is the only call of `0x003235C0`.
5. `0x0055F3E0` then runs the purchase stages on `+0x55E`: it pans to the square, lights it (`0x0055F641`), runs the
   sweep (`0x0055DD70`), waits for the transitions, and shows the notices.

| Notice (`listhelp_license.bin`) | When |
|---|---|
| "{name} has learned a new Mist ability!" (`0x426C`) | the member's Mist count grew (`+0x570` bit 5) |
| "The character can now summon Espers under the Mist command in the Battle Menu." (`0x4269`) | the first Esper obtained |
| "The character can now perform quickenings under the Mist command ..." (`0x426A`) | the first Quickening obtained |
| "The license for the Esper {name} has been added to the board!" (`0x426B`) | when the board opens with a new Esper square (`0x0055E9E0`) |
| "The Second Board license has been added to the license board!" (`0x428A`) | the same, for the Second Board square |

Obtaining the Second Board ends with the chooser opening for the member's second board (`0x0055F3E0` stage 4).

### Grid helpers

- `0x0055E3F0(view, state, test)` gives state 4 to squares next to one passing `0x00556580` (bit 13, owned) and state 1
  to those passing `0x00556570` (a node other than `0xFFFF`) (`0x0055C3E5`, `0x0055C3F6`).
- `0x00556590(square)` returns the art row's word `+0x22` of `[0x02CA9670]` for a state-4 square, or the default at
  `+0x5A62` when it has no art row; 0 for other states.
- `0x0055EF10(view)` runs every square's transition (`0x0055F010`) and fade (alpha `+0x25` from `+0x26`/`+0x27`, rising or
  falling by `+0x29`), and plays sound `0x4A` once when a transition returns `0x10`. `0x0055B2B0(view)` returns 1 while
  any square still fades or counts down.
- `0x0055B8C0(view)` starts a 6-frame pan toward the cursor square (`+0x550`/`+0x551` times the cell size `+0x554`) when
  the view is not there; `0x0055F1C0` runs the pan (`0x00248F40`) and the cursor's pulse `+0x191` in five steps.
- `0x0055B960(view, dx, dy, now)` gives the scroll `d` that keeps the cursor inside the view. Unless `now`,
  each axis takes `s = d >> 4` (arithmetic), `s = d / abs(d)` when that is 0, and an odd `s` one further from 0
  (`0x0055BA33`-`0x0055BA5F` for x, `0x0055BA6E`-`0x0055BA91` for y).
- `0x00561F20` clamps a scroll to its limits: `+0x10 = min(max(+0x10, +0x08), +0x0C)` and
  `+0x12 = min(max(+0x12, +0x0A), +0x0E)`, all `s16`.
- `0x0055AB20` tiles the background picture `+0x180` over the screen in batches of 12 (`0x002D9380`); `0x0055B6D0` draws
  the cursor frame `+0x188`, inset by the pulse.

### Detail panel and member switch

- `0x0055A180(view, square)` fills the four detail panes (`+0x140`) through `0x00559E30`, or closes the panel when it is
  open (`0x0055A1F0`). `0x005597C0` closes the panes (`0x00244F00`) and `0x00559800(view, v)` hides or shows them.
- `0x00559E30(pane)` shows the square's name and LP cost (`0x0029FF60`), its kind icon (`0x12` for category `0x1E`) and up
  to eight contents from the node record `0x0035D330(0x19, node)` `+0x26`, by its list type `+0x23`: class 1 records
  for type 0, class `0x14` records for type 1 (with the icon of the class 1 record each names), and class `0x1D`
  names for types 2 and 3.
- `0x0055AE00` and `0x0055B840` step to another member that has a board (`0x0027EDA0` or `0x0027F430` with the test
  `0x005617E0`), play sound `0x51` and rebuild the view (`0x0055DBD0`); `0x00557A40` and `0x00557A90` do the same in the chooser
  (`0x00558760`).

### Chooser helpers

- `0x00556380(slot, board1, board2, current)` builds the line of one or two board names (`menu_command.bin` `0x3ED` +
  board, joined by `0x3F9`) into `0x02CA8FF0` + slot x 256, colouring one name with colour 3 (`0x002AB870`);
  `0x00558E70` shows it for the member, and `0x00556F50` hands the text of a row to its label.
- `0x005587E0(chooser)` lists, for up to six members (`0x00282DF0`, `0x00282FA0`), which board each holds as first
  (`0x00323670`) and second board (`0x00323630`).
- `0x00558A10(chooser, board, curve, frames)` turns the board wheel to `board` (30 degrees a board, crossing 360 between
  boards 0 and 11), and `0x00558AF0` steps it (`0x00248F40`) into the angle `+0x34C`.
- `0x005574C0` draws a chooser picture as four mirrored quarters at 0.8 scale (`0x002DB080`).
- `0x00561020` releases the chooser's five widgets and two buffers.
- `0x002CE280(window)` puts a window, its child `+0xC0` and that child's `+0xD8` into the second draw pass
  (`0x00247730(widget, 1)`); the chooser (`0x005584CE`), the board view (`0x0055D71E`, `0x0055D784`), `0x0055E9E0` and
  `0x0055F3E0` call it.

### The member picker

`0x00560910` lists the members with `0x00561100`: the roster slot of each one `0x00282FA0` accepts and its portrait
(`0x002526F0(8, id + 0x4D, 1)`). `0x00560610` draws a member's board in miniature, one cell per square of the board table
`[0x02EBF1A0 + board]` coloured `0x002DD7E0(0xDB + value)`, and `0x0055FA50` frees the six cell arrays at `+0x150`.

## Shipped data

| | |
|---|---|
| boards | 12, each 24 x 24 squares in the file, 25 x 25 on screen (625 squares, 49 of them the empty border) |
| Gambit Slot squares | 10 on each board, 120 in all |

## Modding notes

- The view is the board file plus one row and column; a larger board needs `+0x559`/`+0x55A` to fit a byte.
- The screen tests LP against the menu record's `+0xB0` (`0x0055C496`), and the purchase charges the member's stats
  record.
- One purchase animates at most 32 changed squares; the rest change without an effect.

## Related

- [License Board](../Items-Equipment-Shops-And-Licenses/license-board.md) - the board file and the two board slots.
- [Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md) - the node records and what obtaining one does.
- [Dialogs](dialogs.md) - the description box and the confirm and notice boxes.
- [Menus](menus.md) - the Licenses entry.
