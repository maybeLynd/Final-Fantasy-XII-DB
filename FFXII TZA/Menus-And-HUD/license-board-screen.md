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

The square record, `LicenseSquare`, is under [Layouts](#layouts).

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
- `0x005599D0` is the callback of the four detail panes at view `+0x140`: `0x00559860` installs it (`0x005598A8`) for each
  of the four slots (`0x005598E4`) as a `0x208`-byte task (`0x005598B9`) through `0x00244F50`, and passes no menu id.
- The Licenses command id `0x4B5` of `menu_command.bin` is an immediate at eight sites in `.text`. The chooser
  window (`0x00558FF0`) and the board screen (`0x00561446`) pass it to `0x00280CA0`, which looks the id up in the entry
  list of `[0x0209AC30] + 0xD8`; the member-pick widget passes it to the return to the Party Menu, `0x002814E0`
  (`0x005609AC`); the others are `0x00281BE5`, `0x0028237F`, `0x002C1236`, `0x002C1278` and `0x002D739D`.
- Each detail pane's row callback `0x00559910`
  (`0x00559ABF`, kept at the list's `+0x120`) fills row `n` from the pane's `0x20`-byte rows at `+0xE8`:
  - the text element (`[[pane + 0x10] + 8]`) gets the row's string `+0x00`, the colour `0x0020E620(0)` at `+0x20` and,
    at `+0x24`, `0x002DD7E0(2)` when the row's word `+0x0C` is 0, else `0x002DD7E0(0)`;
  - the icon element (`[[pane + 0x10]]`) is shown (bit `0x1` of `+0x08`) when the row's word `+0x08` is not `0xFFFF`
    and its byte `+0x0A` is not `0xFF`, with that byte as the cell `+0x0A` and `+0x39` from the picture's palette
    table (`[+0x20] + 8 x cell + 7`).
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

## Layouts

The squares are one array at view `+0x120`, row by row, the row width the view's `+0x559` (`0x0055C140`-`0x0055C14E`).
`0x0055B560` allocates `0x38` bytes a square (`0x0055B586`) and zeroes the whole array with `0x00861EC0` (`0x0055B643`).

`LicenseSquare` (`0x38` bytes, offsets from the start of the [view+0x120]+i*0x38):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | name | the square's name string, from `0x002B58B0` (`0x0055C114`) |
| `+0x08` | `u16` | node | license node (`0x0055C0DD`), `0xFFFF` for an empty or hidden square (`0x0055C38B`, `0x0055C4F8`) |
| `+0x0A` | `u8[1]` | pad0A | zeroed with the array (`0x0055B643`) and by the qword stores of +`0x08` for an empty or hidden square (`0x0055C37F`, `0x0055C4E2`); the fill writes +`0x08` and +`0x0B` around it |
| `+0x0B` | `u8` | rule | record byte +`0x22`, node byte +`0x06` (`0x0055C11F`, `0x0055C123`): 1, 2 or 3 choose the confirm text |
| `+0x0C` | `u16` | lpCost | record byte +`0x20`, node byte +`0x04` (`0x0055C117`); the record holds the node at +`0x1C` |
| `+0x0E` | `u16` | artNode | row of the art table [`0x02CA9670`] (`0x0055C126`) |
| `+0x10` | `u32[2]` | kindText | the kind of license, Weapon to Gambit (`0x4280`-`0x4289`), (`0x0055C12E`) |
| `+0x18` | `u32` | state | bits 0-3 corner shape, 4-7 state, 8-11 state shown, 12-15 purchase flags |
| `+0x1C` | `u8[4]` | pad1C | zeroed with the array (`0x0055B643`) and by the qword stores of +`0x18` for an empty or hidden square (`0x0055C387`, `0x0055C4EA`); the fill writes +`0x18` as a dword (`0x0055C47F`, `0x0055C4C2`) |
| `+0x20` | `u8` | col | column (`0x0055C0E1`) |
| `+0x21` | `u8` | row | row (`0x0055C0E5`) |
| `+0x22` | `u8` | phase | 0 idle, 1 effect armed, 2 countdown, 3 effect playing (`0x0055F010`) |
| `+0x23` | `u8` | pending | the state the transition will show |
| `+0x24` | `u8` | tile | tile variant 0-7 (`0x0055C15C`) |
| `+0x25` | `u8` | alpha | `0x80` when built (`0x0055B690`) |
| `+0x26` | `u8` | fadeLeft | fade counter |
| `+0x27` | `u8` | fadeLen | fade length |
| `+0x28` | `u8` | fadeOn | fade running |
| `+0x29` | `u8` | fadeIn | fade direction |
| `+0x2A` | `i16` | countdown | frames before the pending state shows |
| `+0x2C` | `u32` | effect | the playing effect (`0x003B2D80`); `0x0055B560` passes a non-zero one to `0x003B2AA0` (`0x0055B5DA`) and clears it (`0x0055B5DF`) |
| `+0x30` | `u32` | category | node byte +`0x05` (`0x0055C13D`); `0x1E` is the Second Board |
| `+0x34` | `u8[4]` | pad34 | zeroed with the array (`0x0055B643`); the fill writes +`0x30` as a dword and stops there |

### The board screen's fields

The board screen is the `0x110`-byte widget with procedure `0x00561390` that `0x00561300` builds and its owner keeps at `+0xC8` (Opening above).

```struct BoardScreen base=record size=0x110
+0x00    u8[192]         header                 the widget header, written by the constructor 0x002465F0 (Widgets, The
                                                header); procedure 0x00561390
+0xC0    ptr             owner                  the member picker 0x00560910 that built the screen through 0x00561300 and
                                                keeps it at its +0xC8: the creation record's first qword (0x00561580).
                                                When its pictures have loaded (message 16) the screen loads lic_bk,
                                                cm2_win_c, lic_8_c, lic_8_c2, lic_8_c3 and the art table into the
                                                owner's +0xD8-+0x118 (0x00561601-0x0056177B); on destroy (message 18) it
                                                clears the owner's +0xC8 and hands back to it (0x00561403-0x005614A1)
+0xC8    ptr             view                   the 0x580-byte board view with procedure 0x0055CD40 that 0x0055C690 builds
                                                when the pictures have loaded (0x0055C6EF), also kept at [0x0209AC30] +
                                                0x320 and opened under the main root (0x0055C6FD-0x0055C71E); 0x0055C690
                                                builds it only while this is 0 (0x0055C6A5). The screen passes message
                                                20 to the view's procedure (0x005613E0-0x005613FC)
+0xD0    u32             member                 the member's roster slot, copied from the owner's +0xD0 on
                                                construction (0x00561587-0x0056158D); written back to the owner when the
                                                screen hands over to the board chooser (0x0056147A-0x00561480)
+0xD4    u8[12]          gap0D4                 read and written by no function; nothing fixes its width
+0xE0    ptr             closeChild             on closing (message 15) the screen asks the widget here to close with
                                                0x00244F00 when it is not 0 (0x00561522-0x00561532); no access writes it, so
                                                it keeps the constructor's 0
+0xE8    u8[32]          gap0E8                 read and written by no function; nothing fixes its width
+0x108   u8              chooserByte            the creation record's byte +0x18 (0x005615C6-0x005615CA): 0xFF from the
                                                member picker (0x00560C81-0x00560C98), the board chooser's own +0xDC when
                                                it hands over (0x005590D4-0x005590E3); passed back as the third argument
                                                of 0x00558F20 when the screen hands over to the chooser
                                                (0x0056148C-0x005614A1)
+0x109   u8[3]           gap109                 read and written by no function; nothing fixes its width
+0x10C   u32             flags                  bit 0: on destroy, sends the owner the command 0x8003 (0x00247510)
                                                instead of handing back (0x00561424-0x0056143C); no access sets it. Bit 1:
                                                the owner's byte +0x185 (0x00561593-0x005615A5); no access reads it. Bit
                                                2: the creation record's +0x08 bit 0 (0x005615AB-0x005615BE), 1 from the
                                                board chooser when the board changed (0x005590A5-0x005590E3), 0 from the
                                                member picker; on destroy, set: the member goes back to the owner and
                                                0x00558F20(owner, 1, +0x108) builds the chooser (0x0056147A-0x005614A1);
                                                clear: the owner is opened again (0x00561460-0x00561470)
```

### The members on each board

The board chooser keeps one `0x28`-byte record per board at its `+0x16C`, twelve in all.

```struct BoardHolders base=[chooser+0x16C]+board*0x28 size=0x28
+0x00    i32[9]          members                the word +0x60 of each member holding the board as first or second
                                                board, in roster order (0x0055883C-0x0055885A, 0x00558871-0x00558891)
+0x24    u32             count                  how many members are listed, raised with each (0x00558861, 0x00558898);
                                                0x0055A340 reads it first (0x0055A4D6)
```

### The board chooser's fields

The board chooser is the `0x390`-byte widget with procedure `0x00557DB0` that the chooser window `0x00558FB0` builds (The board chooser above).

```struct BoardChooser base=record size=0x390
+0x00    u8[192]         header                 the widget header, written by the constructor 0x002465F0 (Widgets, The
                                                header); procedure 0x00557DB0
+0xC0    ptr             window                 the chooser window 0x00558FB0 that built the chooser: the creation
                                                record's first qword (0x00557FE1). On destroy the chooser clears the
                                                window's +0xC8 and [0x0209AC30] + 0x320 (0x005582C5-0x005582DC); command
                                                0x8002 sets the window's +0xE0 bit 1 and +0xDC to the board the
                                                command carries, or clears the bit and stores 0xFF for 0xFF, and
                                                closes the window (0x005583BE-0x0055841D)
+0xC8    ptr             memberPanel            the 0xD0-byte panel with procedure 0x00558CE0 that 0x00558C40 builds while
                                                this is 0 and opens under the main root, copying +0xE8 into the
                                                keyboard cell 0x02CA8FE0 (0x00558C55-0x00558CC7); built at stage 2
                                                (0x00557EDD) and again on a member switch, which closes the old one
                                                first (0x0055878F-0x005587AE); stage 4 shows the member's boards in it
                                                through 0x00558E70 (0x00557E7B); command 0x8002 closes it
                                                (0x0055838C-0x0055839F)
+0xD0    ptr             descriptionBox         the 0x3D8-byte description box with procedure 0x00556F90 that 0x00556EC0
                                                builds for the shown board while this is 0 (0x00556ED5-0x00556F26);
                                                turning the wheel writes the board to its +0x3D1 and the board less 1
                                                to +0x3D2 (0x00558536-0x00558551); command 0x8002 and the confirm close it
                                                (0x005583A6-0x005583B7, 0x0055866F-0x00558682)
+0xD8    ptr             picturesPart           the 0xE0-byte part with procedure 0x00557760, which draws the chooser's
                                                pictures through 0x005574C0: built by 0x00557370 at the wheel centre less
                                                0x28 in y on construction (0x005581AC, 0x005573CB), closed by 0x00557340 on
                                                command 0x8002 (0x00557349-0x0055735A)
+0xE0    ptr             wheelPart              the 0xF0-byte part with procedure 0x005565E0, which draws the wheel's
                                                board pictures at the angle +0x34C and marks the boards set in +0x364:
                                                built by 0x005572B0 on construction (0x005581BC, 0x0055730B), closed by
                                                0x00557280 on command 0x8002 (0x00557289-0x0055729A)
+0xE8    ptr             namePart               the 0xF0-byte part with procedure 0x005569F0, which draws the board
                                                names (menu_command.bin 0x3ED + board) around the wheel at the
                                                angle +0x34C: built by 0x005571F0 on construction (0x005581D7, 0x0055724B), closed
                                                by 0x005571C0 on command 0x8002 (0x005571C9-0x005571DA); faded in by
                                                0x002D04F0 at stage 4 (0x00557E87) and out on the confirm (0x00558689);
                                                0x00558C40 copies it to 0x02CA8FE0 (0x00558CAB)
+0xF0    ptr             wheelPart2             the 0xF0-byte part with procedure 0x0055A340, which draws at the
                                                angle +0x34C: built by 0x00557430 on construction (0x005581CA, 0x0055748B), closed
                                                by 0x00557400 on command 0x8002 (0x00557409-0x0055741A); faded in at stage 4
                                                (0x00557EA6) and out on the confirm (0x005586A8)
+0xF8    u8[72]          gap0F8                 read and written by no function; nothing fixes its width
+0x140   ptr             atlasC2                the member picker's +0xF0, the lic_8_c2 label the board screen stores
                                                there (0x005616FE-0x00561738), copied through the window's +0xC0 on
                                                construction (0x00557FF7-0x00558005); the pictures part copies it to
                                                its +0xC8 when built (0x005579D2)
+0x148   ptr             atlasC3                the member picker's +0xF8, the lic_8_c3 label (0x0056175E-0x00561765),
                                                copied on construction (0x0055800C-0x0055801A); the pictures part copies
                                                it to its +0xD0 (0x005579E0)
+0x150   ptr             backAtlas              the member picker's +0x100, the lic_bk label (0x0056169E-0x005616A8),
                                                copied on construction (0x00558021-0x0055802F); the name part copies it to
                                                its +0xE0 (0x00556986)
+0x158   u32             turnBits               the wheel's turn: bit 0 a turn is running and bits 2-5 its curve, set
                                                to curve 1 by 0x00558A10 (0x00558A84-0x00558A8B); 0x00558AF0 steps while bits
                                                0-1 are set, passing bits 2-5 to 0x00248F40, and clears bits 0-1 when
                                                the turn is done (0x00558AF9-0x00558B3E)
+0x15C   i16             turnFrom               the angle in degrees when the turn started, the low word of +0x350
                                                (0x00558A98, 0x00558AB8); 0x00558AF0 adds the turned part of +0x160 to it
                                                (0x00558B35, 0x00558B58)
+0x15E   i16             turnTo                 the board the wheel turns to: the shown board on construction
                                                (0x00558135) and each turn (0x00558AB1); 0x00558A10 does nothing when asked
                                                for the same board (0x00558A30) and turns the short way, through 360,
                                                when the boards are 0 and 11 (0x00558A4F-0x00558A7E)
+0x160   i16             turnBy                 the degrees to turn, the board x 30 less +0x15C (0x00558AA5-0x00558AC4);
                                                0x00558AF0 adds it times the curve's 0 to 1 to +0x15C (0x00558B2E,
                                                0x00558B4D)
+0x162   i16             turn162                set to 0 by 0x00558A10 (0x00558ACB); no function reads it
+0x164   u32             turnFrames             the turn's length in frames, 0x00558A10's fourth argument (0x00558AAB): 12
                                                from the turn command (0x00558521); passed to 0x00248F40 (0x00558B12)
+0x168   u32             turnStart              the frame counter 0x0208F570 when the turn started (0x00558A92-0x00558A9F);
                                                0x00558AF0 passes the frames since then to 0x00248F40 (0x00558B04-0x00558B0B)
+0x16C   u8[480]         holders                twelve BoardHolders records, one per board (above): 0x005587E0 clears
                                                all 0x1E0 bytes and lists in them, for the first six of the nine
                                                roster slots 0x00282FA0 accepts that hold a first board, the member
                                                under its first and its second board (0x00558800-0x00558898); called on
                                                construction and at stage 4 (0x005580DB, 0x00557E6E). The part 0x0055A340
                                                reads the records through its +0xD8 to place the members' marks around
                                                the wheel (0x0055A3E0, 0x0055A4D6-0x0055A4E9)
+0x34C   f32             angle                  the wheel's angle in radians, (360 - +0x350) / 180 x pi, written by
                                                0x00558AF0 every tick (0x00558B7B-0x00558B9D); the parts 0x005565E0, 0x005569F0
                                                and 0x0055A340 draw by it (0x00556629, 0x00556712, 0x00556B58, 0x0055A392,
                                                0x0055A48F)
+0x350   i32             degrees                the wheel's angle in degrees, 30 a board: the shown board x 30 on
                                                construction, moved by 360 when the boards are 0 and 11
                                                (0x00558132-0x00558169, 0x00558A67-0x00558A7E); stepped to +0x15C + +0x160 x t
                                                during a turn and to the end when it finishes (0x00558B45, 0x00558B75)
+0x354   u32             member                 the member's roster slot: the window's +0xD8 on construction
                                                (0x00557FEB-0x00557FF1), [0x0209AC30] + 0xDE0 on a member switch
                                                (0x00558775-0x00558783); 0x00282DF0 resolves it for the member's boards
                                                (0x005580E9, 0x00558434, 0x005585D9, 0x005588E1)
+0x358   i8              board                  the board shown, 0-11: the member's active board 0x003236B0, or the
                                                window's +0xDC when +0x388 bit 1 is set, 0 for none
                                                (0x005580E0-0x00558122); 0x00557B90 steps it by one with the two directions,
                                                wrapping between 11 and 0, and posts the turn command 0x8000
                                                (0x00557C49-0x00557CB1); 0x00556EC0 builds the description box for it
                                                (0x00556EE2); stage 4 sets its bit in +0x364 (0x00557E2D); the confirm
                                                stores it (0x00558637-0x00558652)
+0x359   u8[3]           gap359                 read and written by no function; nothing fixes its width
+0x35C   i32             centreX                the wheel centre's x, half the screen width 0x01E0C1D8
                                                (0x0055816F-0x00558186); the parts are placed and the effects started at
                                                it (0x005581AC-0x005581F1, 0x0055898F, 0x005585F0, 0x0055890B)
+0x360   i32             centreY                the wheel centre's y, half the screen height 0x01E0C1DC less 0x17
                                                (0x0055817F-0x005581A6); the parts sit 0x28, 0x2A and 0x2B above it
                                                (0x005581A2-0x005581C1)
+0x364   u32             boardsHeld             one bit per board: on construction the first and second boards of the
                                                nine roster slots 0x00282FA0 accepts (0x00558081-0x005580D6), and at stage 4
                                                the board just chosen (0x00557E2D-0x00557E41); the wheel part tests each
                                                board's bit to pick the board's picture (0x00556763)
+0x368   u32             hintEffect             the effect 0x005588C0 starts below the wheel, 0x1C while the member has
                                                no first board and 0x1F once it has one, after stopping the old one
                                                (0x005588D2-0x00558940); stopped on closing (0x0055830C-0x0055831B) and after
                                                the confirm (0x005586C7-0x005586D8)
+0x36C   u32             confirmEffect          the effect 0x1B the confirm starts at the wheel centre
                                                (0x005585E4-0x00558601); stage 4 waits while 0x003B2CE0 reports it running,
                                                then stops it and clears this (0x00557E1A-0x00557E57)
+0x370   u32             boardEffect            the effect 2 + board at the wheel centre, one above it: started on
                                                construction (0x00558217-0x00558244) and replaced on every turn by
                                                0x00558960 (0x0055897A-0x005589AD)
+0x374   u32             turnEffect             the effect 0x00558960 starts on every turn, 0x1D or 0x1A by the turn
                                                command's direction (0x005589B7-0x005589EB); stopped on closing
                                                (0x005582F5-0x00558306)
+0x378   u32             centreEffect           the effect 0x1E at the wheel centre, started on construction
                                                (0x005581DC-0x00558208)
+0x37C   u8              cuesRunning            1 while the confirm's three cues play, set with stage 4 by one word
                                                store (0x00558607); the tick waits each cue's delay +0x380 and plays its
                                                cue +0x383 (0x00557F5E-0x00557FA2), and clears this after the third
                                                (0x00557FAD-0x00557FBA)
+0x37D   u8              stage                  the opening stage (0x00557DF0): 0 first tick: 1 with a delay of 0x10
                                                frames when the save-wide flag 0xBB is clear (0x00557F3E-0x00557F4C), else
                                                2; 1 waits the delay, sets flag 0xBB and opens message 0x18
                                                (0x00557EFA-0x00557F30), then 3; 2 builds the member panel and description
                                                box (0x00557ED2-0x00557EF1), then 3; 3 idle; 4 after the confirm: waits
                                                for the confirm effect, then marks the board and fades the parts in
                                                (0x00557E1A-0x00557EC8), then 3. Command 0x11D with 0x18 sets 2 (0x00558707)
+0x37E   u8              stageDelay             frames left at stage 1, 0x10 from the word store (0x00557F4C); counted
                                                down by the tick (0x00557EFA-0x00557F07)
+0x37F   u8              cueIndex               the cue playing, 0-2: 0 on the confirm (0x0055863E), raised after each
                                                cue (0x00557FA7-0x00557FAD)
+0x380   u8              cueDelay0              frames before the first cue, 0x40 (0x00558620 with +0x381); counted down
                                                by the tick (0x00557F73-0x00557F81)
+0x381   u8              cueDelay1              frames before the second cue, 0x18 (0x00558620)
+0x382   u8              cueDelay2              frames before the third cue, 0x38 (0x00558629)
+0x383   u8              cue0                   the first cue, sound 0x45 (0x00558610 with +0x384), played through
                                                0x00249C60 (0x00557F9A-0x00557FA2)
+0x384   u8              cue1                   the second cue, sound 0x4A (0x00558610)
+0x385   u8              cue2                   the third cue, sound 0x6B (0x00558619)
+0x386   u8[2]           gap386                 read and written by no function; nothing fixes its width
+0x388   u32             flags                  bit 0: input is held: set on construction (0x00558235), by a step
                                                (0x00557CDD) and when the confirm question opens (0x00558475, 0x005584E1),
                                                cleared at stages 2 and 4 (0x00557E4C, 0x00557EEA) and by the answer No
                                                (0x005586EE); the input turn does nothing while it is set (0x00558261).
                                                Bit 1: start at the window's board: the window's +0xE0 bit 1
                                                (0x00558036-0x0055804C), tested at 0x005580E0. Bit 2: the member has no
                                                first board, so the confirm stores a first board through 0x00323740
                                                rather than a second through 0x003236F0 (0x00558475, 0x005584DE,
                                                0x00558630-0x00558652)
+0x38C   u8[4]           tail38C                read and written by no function; nothing fixes its width
```

## Shipped data

| | |
|---|---|
| boards | 12, each 24 x 24 squares in the file, 25 x 25 on screen (625 squares, 49 of them the empty border) |
| Gambit Slot squares | 10 on each board, 120 in all |

## State

These start with the file's values and are replaced when the board view `0x0055CD40` is built: it builds its widgets
from layout 5 of the menu layout block (`[0x0209AC30] + 0x58`, `0x002432B0`, `0x0055CDE6`-`0x0055CE02`) and takes them
from the layout's nodes (`0x0055CE07`-`0x0055CE61`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F2CACC` | `i32` | 48 | the size of a board square in pixels: the word `+0x10` of the third entry of the view's node array `+0x60`, when there is one; `0x01F2CAF0` becomes 48.0 over it (`0x0055CE1B`-`0x0055CE38`). Half of it is the view's `+0x554` (`0x0055C598`-`0x0055C5AC`) | `0x0055CD40` (`0x0055CE27`) | `0x0055AB20` (`0x0055AB81`); `0x0055AE80` (`0x0055AEF9`, `0x0055B0C6`); `0x0055B8C0` (`0x0055B8D7`); `0x0055B960` (`0x0055B9B0`); `0x0055BAC0` (`0x0055BB73`, `0x0055BEE3`); `0x0055C530` (`0x0055C598`, `0x0055C5A6`, `0x0055C5DE`, `0x0055C605`); `0x0055CD40` (`0x0055D270`, `0x0055D295`, `0x0055D2BB`, `0x0055D2DB`, `0x0055D33D`, `0x0055D364`, `0x0055D378`, `0x0055D3C5`, `0x0055D427`, `0x0055D46B`); `0x0055E9E0` (`0x0055EA60`, `0x0055EA7C`, `0x0055EBA3`, `0x0055EBBF`, `0x0055ED4E`, `0x0055ED62`); `0x00561CA0` (`0x00561CD2`); `0x00561D30` (`0x00561D62`) |
| `0x01F2CAD0` | `i32` | -1 | the x offset, from the square, of the text `0x0055BAC0` writes on a square (formatted by `0x00365B30` into the view's `+0x4F2` and drawn by `0x002D8910`): the signed word `+0x0C` of the second entry of that array | `0x0055CD40` (`0x0055CE51`) | `0x0055BAC0` (`0x0055BEFB`) |
| `0x01F2CAD4` | `i32` | -12 | that text's y offset, added to half the square size (`0x0055BF01`-`0x0055BF09`): the signed word `+0x0E` of the second entry | `0x0055CD40` (`0x0055CE61`) | `0x0055BAC0` (`0x0055BF03`) |

No other instruction reaches these three.

The member picker draws its miniature boards with the menu picture `lic_4_c` (`Tm2_Menu\lic_4_c.tm2`, kind 7, id
`0x79`), which the game requests once at start-up: the start-up step `0x0022A4B0` calls `0x00556500` (`0x0022A4DC`), which
takes one of the twelve request batches (`0x002486B0`) with the callback `0x00556560`, which sets `0x02CA8F94` to 1, and
files the picture in it through `0x002493D0` (`0x00556541`).

On opening, `0x00560910` waits until `0x02CA8F94` is non-zero (`0x00560A55`-`0x00560A62`), then copies the picture to its own
`+0xE0` (`0x00560A78`), where `0x00560610` reads it for each miniature (`0x0056065D`); closing clears that copy
(`0x0056099E`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA8FD8` | `void*` | 0 | the texture entry of `lic_4_c`, the one `0x002493D0` returns from the 64-entry table `0x0208F580` | `0x00556500` (`0x00556549`) | `0x00560910` (`0x00560A6C`) |

No other instruction reaches `0x02CA8FD8`.

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
