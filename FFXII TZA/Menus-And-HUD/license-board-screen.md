[Home](../../README.md) / [Menus and HUD](README.md) / License Board screen

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| License Board screen: the board chooser, the square grid and its states, the change sweep, preview, and obtaining a license | system | Menus and HUD | Menu screens | How the Licenses screen opens on a member's board or the board chooser, how the grid is built from the board file plus one row and column with random tile variants, the 0x38-byte square and its state bits, how owned, reachable and affordable squares are worked out, the corner shapes, the change sweep with its 32-square batch, the board preview, the scripted cursor moves, the confirm texts, and the purchase with its animation and notices. | 0x0055B3F0, 0x0055BFF0, 0x0055B310, 0x0055DD70, 0x0055CD40, 0x00557DB0, 0x0055D978, 0x0055F3E0 |

## What the player sees

- Licenses asks for a character, then shows that character's license board; a character without a board first picks
  one of the twelve boards ("Choose this license board?").
- Owned squares are lit, the squares next to them can be obtained, and the rest of the board stays dark.
- Obtaining a square asks for confirmation, plays an effect, lights the neighbours one after another, and may
  announce a new Esper, a new Mist ability or the Second Board.
- From the board chooser, a board can be previewed without choosing it.

The screen draws the member's chosen board file: each square names a license, whose record gives its LP cost, and the
member's license data says whether the square is owned, can be obtained now, or only later. Obtaining a square writes
that license to the member, charges the LP, and the squares are worked out again.

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
   once per save: `0x00252D10` tests the save-wide flag `0xBB` (`0x00557F43`) and `0x00252D40` sets it (`0x00557F16`).
2. Confirm asks "Choose this license board?" (`0x835`, `0x00558607`).
3. Yes plays three cues and stores the board: `0x00323740(row, board)` for a first board, or `0x003236F0(row, board)` for
   the second (`0x00558630`-`0x00558668`). [License Board](../Items-Equipment-Shops-And-Licenses/license-board.md) has the
   two board slots.

### Building the grid

`0x0055B3F0` picks the board shown, the member's stats byte `+0x1C5` (`0x003236B0`, `0x0055B446`), and sizes the view from
the board file: width + 1 by height + 1 (`0x0055B484`-`0x0055B4A2`). The extra column and row are always empty. It fills a
tile byte per square with `table[(rand() & 3) + 4 x ((col + row) & 1)]` (`0x0055B4E0`-`0x0055B517`), the table being
`00 02 04 06 01 03 05 07`, so even and odd squares draw from different sets of variants.

`0x0055B3F0` builds only while the cells pointer `+0x128` is 0 (`0x0055B429`-`0x0055B430`). In the preview view
(`+0x570` bit `0x400`) it keeps the board `+0x558` as it is instead of calling `0x003236B0` (`0x0055B436`-`0x0055B440`).
A board of `0xFF` gets a 16-bit zero over the width and height `+0x559`/`+0x55A` and no tile bytes (`0x0055B45C`).

Any other board is read from its slot `0x02EBF1A0 + 8 × board` with no null test (`0x0055B481`-`0x0055B484`), so an
empty slot reads address 4 and faults. The tile bytes are allocated in arena 3 by `0x002497B0` (`0x0055B4AA`;
`0x0036C1D0(3, 0xC)`, `0x0036A100`), stored at `+0x128` and zeroed (`0x0055B4BE`) with no null test, so a full arena 3
makes the zeroing write at address 0 and fault.

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
| 0, can be obtained | bit `0x4000` when the cost is at most the member's LP (`0x0055C492`), then bit `0x8000` as for answer 2 |
| 1, owned | bits `0x1000` and `0x2000`, state 5 and state shown 5 (`0x0055C472`-`0x0055C47F`) |
| `2` | bit `0x8000` (`0x0055C4A6`-`0x0055C4C2`); the test of bit `0x1000` there always passes, because the fill cleared the four flags at `0x0055C136` |
| `3`, `4`, `5`, `8` | the square is emptied (`0x0055C4CA`) |
| `6`, `7`, `9` | no flag: answers 6 and 7 take the table's empty arm and 9 is past its end (`0x0055C45F`-`0x0055C463`, `0x0055C482`) |

`0x0055E090` then turns bit `0x8000` into bit `0x1000` on each square next to an owned one. So bit `0x2000` means owned, bit `0x1000`
obtainable now, bit `0x4000` affordable and bit `0x8000` obtainable later. The state nibble, mask `0xF0`, takes four values:

| State | Meaning | Set by |
|---:|---|---|
| `0` | empty | the fill |
| `1` | a square not yet next to an owned one | `0x0055E230` |
| `4` | next to an owned square | `0x0055E3F0(view, 4, owned)` |
| `5` | owned | answer 1, or the purchase (`0x0055F641`) |

Squares in states 4 and 5, and Esper and Second Board squares in state 1, are drawn with their art (`0x0055BAC0`). A
state-4 square shows its LP cost when zoomed in.

### Corner shapes

`0x0055DEA0` gives each square a corner piece in bits `0xF` from the squares to its left, above and above-left
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
square fades out. A square past the 32nd keeps its old look until a later fill lists it or, without the collect bit, copies
its state (`0x0055B380`-`0x0055B3A6`). `0x0055F010` runs the transitions
every frame.

Before the transitions, `0x0055DD70` gives the bought square, the cursor's `+0xC8`, state 4 with its new state as
the pending one, phase 2 and a countdown of 0 (`0x0055DD8E`-`0x0055DDBF`). For each listed square it then copies the
state into the state shown (`0x0055DE2C`-`0x0055DE3E`), and a square in state 1 or 5 stops there (`0x0055DE09`).

A square in state 4 has its state set back to the state shown before that copy, with state 4 pending, phase 2 and
a countdown of `0x2E` (`0x0055DE0D`, `0x0055DE46`-`0x0055DE6C`). A square in state 0 is set back the same way, with
phase 2, state 0 pending and a countdown of 0, and its fade starts: `+0x26` 0, `+0x27` 0, `+0x28` 1 and `+0x29` 1
(`0x0055DE15`-`0x0055DE1F`). Any other state value gets state 0, that value pending, phase 2 and a countdown of 0
(`0x0055DE05`-`0x0055DE07`). The sweep returns the fill's result (`0x0055DD97`, `0x0055DE8B`).

### Preview

The chooser's preview control closes it with the board in hand, and the window opens the board screen with the
preview flag (`0x005590E3`, `0x00557B90`). In the view (`+0x570` bit `0x400`, `0x0055CEB2`):

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
| "{name} has learned a new Mist ability!" (`0x426C`) | the member's Mist count grew (`+0x570` bit `0x20`) |
| "The character can now summon Espers under the Mist command in the Battle Menu." (`0x4269`) | the first Esper obtained |
| "The character can now perform quickenings under the Mist command ..." (`0x426A`) | the first Quickening obtained |
| "The license for the Esper {name} has been added to the board!" (`0x426B`) | when the board opens with a new Esper square (`0x0055E9E0`) |
| "The Second Board license has been added to the license board!" (`0x428A`) | the same, for the Second Board square |

Obtaining the Second Board ends with the chooser opening for the member's second board (`0x0055F3E0` stage 4).

### Grid helpers

- `0x0055E3F0(view, state, test)` gives state 4 to squares next to one passing `0x00556580` (bit `0x2000`, owned) and state 1
  to those passing `0x00556570` (a node other than `0xFFFF`) (`0x0055C3E5`, `0x0055C3F6`).
- `0x00556590(square)` returns the art row's word `+0x22` of `[0x02CA9670]` for a state-4 square, or the default at
  `+0x5A62` when it has no art row; 0 for other states.
- `0x0055EF10(view)` runs every square's transition (`0x0055F010`) and fade (alpha `+0x25` from `+0x26`/`+0x27`, rising or
  falling by `+0x29`), and plays sound `0x4A` once when a transition returns `0x10`. `0x0055B2B0(view)` returns 1 while
  any square still fades or counts down.
- `0x0055B8C0(view)` starts a 6-frame pan toward the cursor square (`+0x550` times the cell width `+0x554` and `+0x551`
  times the cell height `+0x555`, each plus half of `0x01F2CACC`) when the view is not there.
- `0x0055F1C0` runs the pan (`0x00248F40`) and, while `+0x570` bit `0x40` is set, the cursor's pulse `+0x191` in the four
  timed steps of `+0x190`: 30 frames at 0, 6 rising to 8, 4 falling to 0 and 30 at 0, starting again with `+0x570`
  bit `0x80` set.
- `0x0055B960(view, dx, dy, now)` gives the scroll `d` that keeps the cursor inside the view. Unless `now`,
  each axis takes `s = d >> 4` (arithmetic), `s = d / abs(d)` when that is 0, and an odd `s` one further from 0
  (`0x0055BA33`-`0x0055BA5F` for x, `0x0055BA6E`-`0x0055BA91` for y).
- `0x00561F20` clamps a scroll to its limits: `+0x10 = min(max(+0x10, +0x08), +0x0C)` and
  `+0x12 = min(max(+0x12, +0x0A), +0x0E)`, all `s16`.
- `0x0055AB20` tiles the background picture `+0x180` over the screen in batches of 12 (`0x002D9380`); `0x0055B6D0` draws
  the cursor frame `+0x188`, inset by the pulse.

### Detail panel and member switch

- `0x0055A180(view, square)` fills the four detail panes (`+0x140`) through `0x00559E30`, or, when the panel is open
  (`+0x570` bit `0x2`), refills only the current pane for the cursor square through `0x0055A1F0(view, 0)`
  (`0x0055A186`-`0x0055A199`). `0x005597C0` closes the panes (`0x00244F00`) and `0x00559800(view, v)` hides or shows them.
- `0x0055A1F0(view, v)` fills pane `+0x55D` for the cursor square, `[+0x120] + 0x38 x (col + row x width)` from
  `+0x550`, `+0x551` and `+0x559`, with the member `+0x160` at the pane's `+0xD8`, through `0x00559E30`, and opens
  it under `0x0208EA28` (`0x00246AD0`); it closes the other three panes (`0x00244DD0`) and skips an absent one
  (`0x0055A230`-`0x0055A30D`). It calls `0x00282DF0(member)` and does not use the result (`0x0055A28A`).
- On that pane `0x0055A1F0` sets `+0x40` bit `0x400000`; for a square with a node, bit `0x800000` when the square's
  `+0x18` bit `0x1000` is clear; and bit `0x8000` as `v & 1`. It gives `0x00247680` the style byte `+0xA3` = 12 + c,
  c being the category word `+0x30` less 1 when above 0 for a square whose `+0x0E` is not `0xFFFF`, else 0
  (`0x0055A297`-`0x0055A2F9`).
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
`[0x02EBF1A0 + 8 x board]` (`0x00560769`-`0x00560782`) coloured `0x002DD7E0(0xDB + value)`, and
`0x0055FA50` frees the six cell arrays at `+0x150`.

## Layouts

The squares are one array at view `+0x120`, row by row, the row width the view's `+0x559` (`0x0055C140`-`0x0055C14E`).
`0x0055B560` allocates `0x38` bytes a square (`0x0055B586`) and zeroes the whole array with `0x00861EC0` (`0x0055B643`).

`LicenseSquare` (`0x38` bytes, offsets from the start of the [view+0x120]+i*0x38):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | name | the square's name string, from `0x002B58B0` (`0x0055C114`) |
| `+0x08` | `u16` | node | license node (`0x0055C0DD`), `0xFFFF` for an empty or hidden square (`0x0055C38B`, `0x0055C4F8`) |
| `+0x0A` | `u8[1]` | pad0A | zeroed with the array (`0x0055B643`) and by the qword stores of `+0x08` for an empty or hidden square (`0x0055C37F`, `0x0055C4E2`); the fill writes `+0x08` and `+0x0B` around it |
| `+0x0B` | `u8` | rule | record byte `+0x22`, node byte `+0x06` (`0x0055C11F`, `0x0055C123`): 1, 2 or 3 choose the confirm text |
| `+0x0C` | `u16` | lpCost | record byte `+0x20`, node byte `+0x04` (`0x0055C117`); the record holds the node at `+0x1C` |
| `+0x0E` | `u16` | artNode | row of the art table [`0x02CA9670`] (`0x0055C126`) |
| `+0x10` | `u32[2]` | kindText | the kind of license, Weapon to Gambit (`0x4280`-`0x4289`), (`0x0055C12E`) |
| `+0x18` | `u32` | state | mask `0xF` corner shape, `0xF0` state, `0xF00` state shown, `0xF000` purchase flags |
| `+0x1C` | `u8[4]` | pad1C | zeroed with the array (`0x0055B643`) and by the qword stores of `+0x18` for an empty or hidden square (`0x0055C387`, `0x0055C4EA`); the fill writes `+0x18` as a dword (`0x0055C47F`, `0x0055C4C2`) |
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
| `+0x30` | `u32` | category | node byte `+0x05` (`0x0055C13D`); `0x1E` is the Second Board |
| `+0x34` | `u8[4]` | pad34 | zeroed with the array (`0x0055B643`); the fill writes `+0x30` as a dword and stops there |

### The board screen's fields

The board screen is the `0x110`-byte widget with procedure `0x00561390` that `0x00561300` builds and its owner keeps at `+0xC8` (Opening above).

`BoardScreen` (`0x110` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00561390` |
| `+0x0C0` | `void*` | owner | the member picker `0x00560910` that built the screen through `0x00561300` and keeps it at its `+0xC8`: the creation record's first qword (`0x00561580`). On construction (message 1), when the owner's `+0x108` is 0, the screen loads lic_bk, cm2_win_c, lic_8_c, lic_8_c2, lic_8_c3 and the art table into the owner's `+0xD8`-`+0x118` (`0x00561601`-`0x0056177B`); otherwise it sends itself message 16 at once (`0x00561789`-`0x005617AA`); on destroy (message 18) it clears the owner's `+0xC8` and hands back to it (`0x00561403`-`0x005614A1`) |
| `+0x0C8` | `void*` | view | the `0x580`-byte board view with procedure `0x0055CD40` that `0x0055C690` builds when the pictures have loaded (`0x0055C6EF`), also kept at [`0x0209AC30`] + `0x320` and opened under the main root (`0x0055C6FD`-`0x0055C71E`); `0x0055C690` builds it only while this is 0 (`0x0055C6A5`). The screen passes message 20 to the view's procedure (`0x005613E0`-`0x005613FC`) |
| `+0x0D0` | `u32` | member | the member's roster slot, copied from the owner's `+0xD0` on construction (`0x00561587`-`0x0056158D`); written back to the owner when the screen hands over to the board chooser (`0x0056147A`-`0x00561480`) |
| `+0x0D4` | `u8[12]` | gap0D4 | read and written by no function. `0x0055A810` addresses 8-byte slots from `+0xD8` by its index argument (`0x0055A825`-`0x0055A82C`), so `+0xD8` is slot 0 of the array whose slot 1 is closeChild, and the call at `0x005614FC` passes index 1 (`0x005614F3`). Nothing fixes the width of `+0xD4` to `+0xD7` |
| `+0x0E0` | `void*` | closeChild | on closing (message 15) the screen asks the widget here to close with `0x00244F00` when it is not 0 (`0x00561522`-`0x00561532`); `0x0055A810`, called with index 1 (`0x005614F3`-`0x005614FC`), builds a `0xD8`-byte widget with procedure `0x0055A8A0` while the slot is 0 and stores it here (`0x0055A82C`-`0x0055A873`); that widget clears the slot again from its own procedure (`0x0055A8E1`-`0x0055A8F1`) |
| `+0x0E8` | `u8[32]` | gap0E8 | read and written by no function; nothing fixes its width |
| `+0x108` | `u8` | chooserByte | the creation record's byte `+0x18` (`0x005615C6`-`0x005615CA`): `0xFF` from the member picker (`0x00560C81`-`0x00560C98`), the board chooser's own `+0xDC` when it hands over (`0x005590D4`-`0x005590E3`); passed back as the third argument of `0x00558F20` when the screen hands over to the chooser (`0x0056148C`-`0x005614A1`) |
| `+0x109` | `u8[3]` | gap109 | read and written by no function; nothing fixes its width |
| `+0x10C` | `u32` | flags | bit `0x1`: on destroy, sends the owner the command `0x8003` (`0x00247510`) instead of handing back (`0x00561424`-`0x0056143C`); the view's commands `0x8002` and `0x8001` copy bit `0x1` of the command's value into it (`0x0055D55C`-`0x0055D56F`, `0x0055D66C`-`0x0055D67F`) and stage 4 of the purchase clears it (`0x0055F4BD`). Bit `0x2`: the owner's byte `+0x185` (`0x00561593`-`0x005615A5`); the view's build copies it to bit `0x2` of its `+0x570` (`0x0055CF52`-`0x0055CF6D`). Bit `0x4`: the creation record's `+0x08` bit `0x1` (`0x005615AB`-`0x005615BE`), 1 from the board chooser when the owner's `+0x18C` was set, or when the owner's word `+0x188` is not the member word [`0x0209AC30`] + `0xDE0` (`0x005590A5`-`0x005590E3`), 0 from the member picker, and set by the view's command `0x8001` (`0x0055D685`-`0x0055D68C`); on destroy, set: the member goes back to the owner and `0x00558F20`(owner, 1, `+0x108`) builds the chooser (`0x0056147A`-`0x005614A1`); clear: the owner is opened again (`0x00561460`-`0x00561470`) |

### The board view's fields

The board view is the `0x580`-byte widget with procedure `0x0055CD40` that `0x0055C690` builds (The board screen's
fields, `+0xC8`). Its fields come from the procedure's build arm (message 1, `0x0055CDE6`-`0x0055D150`), its destroy arm
(message 18, `0x0055CD84`-`0x0055CDD2`) and every access of the view in [`license-board-screen-board-view-accesses.tsv`](license-board-screen-board-view-accesses.tsv)
beside this page. A field reached by no instruction in that table says so.

`BoardView` (`0x580` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header (Widgets, The header): the build arm installs the descriptor `0x00D22FE0` (`0x0055CE86`-`0x0055CE90`), sets `+0x40` bits `0x2000000` and `0x200000` (`0x0055D0D0`, `0x0055D0E6`) and stores a float at `+0x8C` (`0x0055D0FD`); the destroy arm clears bit `0x200000` (`0x0055CDB6`) |
| `+0x0C0` | `u8[8]` | gap0C0 | reached by no instruction in the table |
| `+0x0C8` | `void*` | square | the cursor's square record (LicenseSquare), written by the procedure's take-square arm (`0x0055D73A`; Obtaining a license) and `0x0055E9E0` (`0x0055ECEF`): the purchase passes it to `0x0055A180` and reads its `+0x30` category against `0x1E`, the Second Board (`0x0055F444`, `0x0055F491`), and its `+0x0B` rule byte (`0x0055F586`); `0x0055DD70` reads it (`0x0055DD8E`) |
| `+0x0D0` | `void*` | square0D0 | a square from the `+0x418` entries, stored by `0x0055E9E0` (`0x0055EC64`-`0x0055EC6C`); read by no instruction in the table |
| `+0x0D8` | `void*` | memberStats | the member's record from `0x00282DF0`(`+0x160`), stored when a pending refresh is served (`0x0055F55C`) |
| `+0x0E0` | `u8[32]` | block0E0 | `0x00561BE0` fills it with `0x00202C70` and hands it to `0x0039ADE0` (`0x00561C30`-`0x00561C77`) |
| `+0x100` | `u8[32]` | block100 | `0x00559540` fills it the same way (`0x00559570`-`0x005595C3`) |
| `+0x120` | `void*` | squares | the square array, `0x38` bytes a square, allocated and zeroed by `0x0055B560` (`0x0055B620`-`0x0055B63C`), freed on destroy (`0x0055CDAA`-`0x0055CDAF`; LicenseSquare above) |
| `+0x128` | `void*` | cells | the view's tile-variant bytes, one per square of the `+0x559` x `+0x55A` view (the licd width and height plus one), allocated by `0x0055B3F0` (`0x0055B4AA`-`0x0055B4B7`) and filled from the table 00 02 04 06 01 03 05 07 (`0x0055B4E0`-`0x0055B517`); `0x0055BFF0` copies each into its square's tile `+0x24` (`0x0055C151`, `0x0055C15C`); freed before a rebuild and on destroy (`0x0055DC57`, `0x0055CD97`) |
| `+0x130` | `void*` | owner | the board screen that built the view: the creation record's first qword (`0x0055CE95`-`0x0055CE98`); the rebuild writes the member slot into its `+0xD0` (`0x0055DC15`), the destroy clears its `+0xC8` (`0x0055CDCB`-`0x0055CDD2`), the take-square arm reads it (`0x0055D55C`-`0x0055D6CF`) |
| `+0x138` | `void*` | preview | the widget `0x00561830` builds when it is 0 (`0x00561845`-`0x0056188F`) and `0x00561800` closes and clears (`0x00561809`-`0x0056181A`); the rebuild closes it first (`0x0055DC7B`-`0x0055DC8C`) |
| `+0x140` | `void*[4]` | panes | the four detail panes (Detail panel and member switch): taken by address and walked by `0x005597C0`, `0x00559800`, `0x00559860`, `0x0055A180` and `0x0055A1F0` (`0x005597CA`, `0x00559811`, `0x00559884`, `0x0055A1A3`, `0x0055A214`); `0x0055FB20` reads the pane `+0x55D` names (`0x0055FB59`) |
| `+0x160` | `u32` | member | the member's roster slot: the owner's `+0xD0` at build (`0x0055CEA6`-`0x0055CEAC`), the menu block's word `+0xDE0` at a rebuild (`0x0055DBF0`-`0x0055DC07`); passed to `0x00282DF0` by `0x0055A1F0`, `0x0055B3F0`, `0x0055BFF0`, `0x0055E2C0`, `0x0055E600` and `0x0055F3E0` |
| `+0x164` | `u8[4]` | gap164 | reached by no instruction in the table |
| `+0x168` | `void*[5]` | pictures | the owner's `+0xE8`, `+0xE0`, `+0xF8`, `+0x100` and `+0xF0` copied at build (`0x0055CEDA`-`0x0055CF3B`): the loaded pictures and art table the screen keeps (The board screen's fields); read at `0x0055AEAA`, `0x0055AB51`, `0x0055B6DC` and `0x0055CF86` |
| `+0x190` | `u8` | litOn | 1, as a word with `+0x191` = 0, at a rebuild, a purchase start and the stage changes (`0x0055DAF6`, `0x0055DC2C`, `0x0055EE80`, `0x0055F240`, `0x0055F310`, `0x0055F477`); `0x0055F1C0` steps it (`0x0055F2D5`-`0x0055F2FC`) and clears it (`0x0055F32C`, `0x0055F33C`) |
| `+0x191` | `u8` | pulse | the cursor's pulse step (Grid helpers): `0x0055F1C0` writes it (`0x0055F35F`, `0x0055F39D`, `0x0055F3D3`; 0 as the high byte of the word stores to `+0x190`), `0x0055B6D0` reads it (`0x0055B6E6`) |
| `+0x192` | `u8` | gap192 | reached by no instruction in the table |
| `+0x193` | `u8` | litPhase | 0 at the same sites as `+0x190` and stepped by `0x0055F1C0` (`0x0055F2E0`-`0x0055F36C`) |
| `+0x194` | `u8` | gap194 | reached by no instruction in the table |
| `+0x195` | `u8[4]` | litColour | the bytes 1E 06 04 1E at the same sites (`0x0055DB06`, `0x0055DC3C`, `0x0055EE90`, `0x0055F250`, `0x0055F320`, `0x0055F487`) |
| `+0x199` | `u8[7]` | gap199 | reached by no instruction in the table |
| `+0x1A0` | `u8[192]` | artEntries | 16 twelve-byte entries the build unpacks from the art table: two words copied, two 12-bit fields of its dword +4, and bytes from the table's second part (`0x0055CF8D`-`0x0055D02A`) |
| `+0x260` | `u8[168]` | artEntries2 | 14 more of the same shape from the table's next part (`0x0055D030`-`0x0055D0CA`) |
| `+0x308` | `void*[32]` | changed | the changed squares a fill lists with the collect bit set (`0x0055B388`; The change sweep); `0x0055DD70` takes the list by address (`0x0055DDD8`) |
| `+0x408` | `i8` | changedCount | the number listed: 0 at a fill with the collect bit (`0x0055B31C`), at most 32 (`0x0055B379`), raised with each listing (`0x0055B390`); `0x0055DD70` compares and sign-extends it (`0x0055DDC6`, `0x0055DE6F`) |
| `+0x409` | `u8[7]` | gap409 | reached by no instruction in the table |
| `+0x410` | `u8[208]` | added | 13 entries of 16 bytes, one per square the board read `0x0055BFF0` adds: the column byte at `+0x00`, the row byte at `+0x01` and the square pointer at `+0x08` (`0x0055C2CD`-`0x0055C2F2`); the procedure's announce arm (`0x0055D870`) announces them (`0x0055D884`-`0x0055D8A7`) and `0x0055E9E0` reads them (`0x0055EA44`, `0x0055EC64`) |
| `+0x4E0` | `u8` | secondCol | the Second Board square's entry, the same shape: column, row and square (`0x0055C322`-`0x0055C330`); read at `0x0055EB78`, `0x0055EB69`, `0x0055D8D8`, `0x0055D8F5` and `0x0055EB49`; the square `+0x4E8` is also 0 when a board is read (`0x0055C02F`) and rewritten at `0x0055D911` |
| `+0x4E1` | `u8` | secondRow |  |
| `+0x4E8` | `void*` | secondSquare |  |
| `+0x4F0` | `i8` | addedCount | the entries at `+0x410`: 0 at build (`0x0055CF5B`, as a word with `+0x4F1`), raised by the board read (`0x0055C2FA`), compared with `+0x4F1` by the rebuild before the cursor square's node test (`0x0055DD0F`-`0x0055DD1D`) and by `0x0055E9E0` (`0x0055EA18`, `0x0055EC49`) |
| `+0x4F1` | `i8` | addedNext | the next entry to announce: the announce arm reads and raises it (`0x0055D870`-`0x0055D8B4`), `0x0055E9E0` reads it (`0x0055EA11`, `0x0055EB2D`, `0x0055EC42`) |
| `+0x4F2` | `char[26]` | text | the text `0x0055BAC0` writes on a square (State; formatted by `0x00365B30`) |
| `+0x50C` | `i16` | winX | four words `0x0055B960` reads to place a square on screen with the cursor, the cell size and the scroll `+0x51C`/`+0x51E` (`0x0055B996`-`0x0055B9DA`); written by the build's layout pass (`0x0055D291`-`0x0055D2F2`); the purchase takes `+0x50C` by address (`0x0055F677`) |
| `+0x50E` | `i16` | winY |  |
| `+0x510` | `i16` | winW |  |
| `+0x512` | `i16` | winH |  |
| `+0x514` | `i16` | viewX | the view rect from the layout record (`0x0055D3B6`-`0x0055D4D3`): `0x0055C530` averages `+0x514` with `+0x518` into the scroll centre `+0x51C` and `+0x516` with `+0x51A` into `+0x51E` (`0x0055C63A`-`0x0055C66B`); `0x0055C740` and `0x0055E9E0` read them (`0x0055CCAF`-`0x0055CCF4`, `0x0055EACE`-`0x0055EAFF`) |
| `+0x516` | `i16` | viewY |  |
| `+0x518` | `i16` | viewW |  |
| `+0x51A` | `i16` | viewH |  |
| `+0x51C` | `i16` | scrollX | the scroll centre; the purchase pans it by `0x0055B960`'s result toward the square and ends its stage when both reach their targets (`0x0055F699`-`0x0055F6DF`); `0x0055C740` moves it (`0x0055CC56`-`0x0055CD04`); `0x0055BAC0` reads both (`0x0055BB1C`, `0x0055BB2D`) |
| `+0x51E` | `i16` | scrollY |  |
| `+0x520` | `i16` | x520 | two words the build's layout pass writes (`0x0055D34C`, `0x0055D373`) and `0x0055AB20` reads (`0x0055AB5E`, `0x0055AB65`) |
| `+0x522` | `i16` | y522 |  |
| `+0x524` | `u32` | flags524 | bit `0x1`: set and cleared by `0x0055C740` (`0x0055CA15`, `0x0055CBA5`, `0x0055CC64`) and tested there (`0x0055CC6B`), set by `0x0055E9E0` (`0x0055ED70`), cleared at a rebuild (`0x0055DBFE`) |
| `+0x528` | `f32` | scale528 | from the layout at `0x0055C530` (`0x0055C590`); the build's layout pass writes and reads it (`0x0055D268`-`0x0055D484`) |
| `+0x52C` | `f32` | angle52C | advanced by a constant every purchase tick (`0x0055F706`-`0x0055F716`); `0x0055BAC0` reads it (`0x0055BDDA`) |
| `+0x530` | `u32` | panFlags | `0x0055B8C0` clears bits `0x2`, `0x8`, `0x10` and `0x20` and sets bits `0x1` and `0x4` when it starts a pan (`0x0055B90C`-`0x0055B91E`); `0x0055F1C0` reads and rewrites it (`0x0055F1C9`, `0x0055F213`); `0x0055C740` reads it (`0x0055C7F9`) |
| `+0x534` | `i16` | panFromX | the pan `0x0055B8C0` starts: from the current offsets, by the deltas to the cursor square, 6 frames from the UI tick (`0x0055B929`-`0x0055B953`); `0x0055F1C0` runs it (`0x0055F1DF`-`0x0055F2A4`) |
| `+0x536` | `i16` | panFromY |  |
| `+0x538` | `i16` | panDeltaX |  |
| `+0x53A` | `i16` | panDeltaY |  |
| `+0x53C` | `u32` | panFrames | 6 |
| `+0x540` | `u32` | panStart | the UI tick `0x0208F570` when the pan started |
| `+0x544` | `i16` | offsetX | the current square offsets: set at build from the cursor and cell size (`0x0055C5FD`, `0x0055C620`), compared by the pan before it moves (`0x0055B8F4`-`0x0055B917`), written by the pan (`0x0055F21A`, `0x0055F239`) and `0x0055E9E0` (`0x0055EA6C`-`0x0055ED88`) |
| `+0x546` | `i16` | offsetY |  |
| `+0x548` | `u32` | effectHandle | the handle `0x003B2D80` returns at build (`0x0055D136`), message 20 stops it with `0x003B2AA0` when it is not 0 and zeroes it (`0x0055D1A9`-`0x0055D1BE`) |
| `+0x54C` | `u16` | squareCount | columns x rows (`0x0055E3CE`); read by the grid helpers `0x0055DEA0` (`0x0055DF15`, `0x0055DF4A`, `0x0055DF76`), `0x0055E090` (`0x0055E0EA`, `0x0055E139`, `0x0055E188`, `0x0055E1CE`) and `0x0055E3F0` (`0x0055E475`, `0x0055E4CC`, `0x0055E524`, `0x0055E575`) |
| `+0x54E` | `i8` | defaultCol | the cursor's default square, the centre, written with `+0x550` (`0x0055E7CE`, `0x0055E7E8`; also `0x0055E620`, `0x0055E812`, `0x0055E9A5`); read at `0x0055ED19`, `0x0055ED23` |
| `+0x54F` | `i8` | defaultRow |  |
| `+0x550` | `i8` | cursorCol | the cursor square (Grid helpers) |
| `+0x551` | `i8` | cursorRow |  |
| `+0x552` | `i8` | cols | copies of `+0x559` and `+0x55A` (`0x0055E3B7`-`0x0055E3C0`) |
| `+0x553` | `i8` | rows |  |
| `+0x554` | `i8` | cellW | half the square size `0x01F2CACC`, both (`0x0055C598`-`0x0055C5AE`) |
| `+0x555` | `i8` | cellH |  |
| `+0x556` | `i8` | centreCol | `0xFF` at build (`0x0055CF64`), the centre at `0x0055E600` (`0x0055E7C2`, `0x0055E7DC`); also written at `0x0055CBC3`, `0x0055CBD8`, `0x0055E806`-`0x0055E818` and `0x0055E999`-`0x0055E9AB` |
| `+0x557` | `i8` | centreRow |  |
| `+0x558` | `i8` | board | the member's board from `0x003236B0`, `0xFF` for no board (`0x0055B44B`-`0x0055B45A`); `0xFF` at build (`0x0055CF80`) |
| `+0x559` | `i8` | width | the licd width and height plus one (`0x0055B48A`-`0x0055B4A2`); 0 at `0x0055B45C` |
| `+0x55A` | `i8` | height |  |
| `+0x55B` | `u8` | b55B | 3 at build (`0x0055CF4B`) and the board read (`0x0055C347`); written by the announce arm (`0x0055D87A`, `0x0055D8E1`; as a word with `+0x55C` at `0x0055D908`, `0x0055D925`) and `0x0055E9E0` (`0x0055EB3D`, `0x0055EC1A`, `0x0055ECAF`, `0x0055ED05`, `0x0055ED7D`, `0x0055EEDF`); read at `0x0055E9EF` |
| `+0x55C` | `u8` | b55C | written and read by `0x0055E9E0` (`0x0055EB36`, `0x0055EC28`, `0x0055EC37`) |
| `+0x55D` | `u8` | pane | the current detail pane 0-3, cycled by the rebuild (`0x0055DBF7`-`0x0055DC0F`) and the announce arm (`0x0055D8BA`-`0x0055D8C5`), indexing the panes at `0x0055FB59` |
| `+0x55E` | `u8` | stage | the purchase stage 0-4 (Obtaining a license) |
| `+0x55F` | `u8` | gap55F | reached by no instruction in the table |
| `+0x560` | `u16` | stageFrames | the stage's countdown: `0x10` when the purchase starts (`0x0055DAC9`) and when the pan ends (`0x0055F6ED`), `0x18` with stage 3 at `0x0055D947`, 0 at `0x0055D964`, `0x0055F5E6` and `0x0055F65F`, decremented each tick (`0x0055F5F2`-`0x0055F6ED`) |
| `+0x562` | `u8` | boardByte87 | the board file's byte `+0x87` (`0x0055C029`); read at `0x0055DA99` |
| `+0x563` | `u8` | effectPhase | 0 idle; 1 when `0x00560070` arms the square effect (`0x0056013A`); 4 when `0x0055F740` arms it (`0x0055F75C`); the mover `0x0055AA00` writes 2 and `0x302` as a word with `+0x564` (`0x0055AAA0`, `0x0055AAF8`) and copies `+0x564` into it (`0x0055AAD9`-`0x0055AAE0`); `0x0055FF90` answers 1 while it is 0 (`0x0055FFA5`) |
| `+0x564` | `u8` | phase564 | read by the mover (`0x0055AAD9`) and written with `+0x563` as above |
| `+0x565` | `u8` | effectOn | 1 at both arms (`0x0055F763`, `0x00560141` with `+0x566`); the mover reads and clears it (`0x0055AA06`, `0x0055AB07`) |
| `+0x566` | `u8` | effectB |  |
| `+0x567` | `i8` | effectCol | the effect's square (`0x0056014A`-`0x00560150`); the mover reads them (`0x0055AA40`, `0x0055AA6F`) |
| `+0x568` | `i8` | effectRow |  |
| `+0x569` | `u8` | repeatDelay | the step delay of a scripted move: `0x002D6680`'s result (`0x00560187`); the mover loads it into `+0x56A` after a step (`0x0055AA63`, `0x0055AA92`, `0x0055AAF1`) |
| `+0x56A` | `u16` | repeatCount | the countdown to the next step: `+0x569` (`0x0055AAF1`), `0x18` (`0x0055AA9B`-`0x0055AAA9`) or `0x20` (`0x0055AAEC`-`0x0055AAF1`); decremented while above 0 (`0x0055AABD`-`0x0055AACC`) |
| `+0x56C` | `u32` | effectNode | the node the effect plays for (`0x0055F76A`, `0x0056017C`) |
| `+0x570` | `u32` | flags | bit `0x1` set by the purchase `0x0055DD70` (`0x0055DD7F`) and cleared by the sweep (`0x0055B3D6`); bit `0x2` the panel is open: `0x00561280`(0) fills it with `0x0055A1F0` and sets the bit when it is clear (`0x0056129D`-`0x005612AE`), `0x00561280`(non-zero) runs `0x00559800` and clears it when it is set (`0x005612BB`-`0x005612CC`); bit `0x4` set at build and when a refresh is served (`0x0055CF2E`, `0x0055F573`), cleared at stage start (`0x0055F453`); bit `0x8` makes `0x0055FAE0` answer 2; bit `0x20` a pending refresh, served and cleared at stage 0 (`0x0055F53C`-`0x0055F550`); bits `0xC0` set at a rebuild and a purchase (`0x0055DC22`, `0x0055F46D`); bit `0x200` set when the Second Board square is bought (`0x0055F4A2`); bit `0x400` from the creation record's `+0x10C` bit `0x4` (`0x0055CEB2`-`0x0055CEC6`): a scripted open, which keeps the child `+0x578` and skips the member read (`0x0055B436`, `0x0055DC9B`); bit `0x800` the cursor goes to the centre (`0x0055E7AF`) |
| `+0x574` | `u8[4]` | gap574 | reached by no instruction in the table |
| `+0x578` | `void*` | child578 | the `0xC8`-byte widget `0x00561E90` builds when it is 0 (`0x00561EA5`-`0x00561EEF`); the rebuild closes and clears it unless `+0x570` bit `0x400` (`0x0055DC9B`-`0x0055DCDA`) |

### The members on each board

The board chooser keeps one `0x28`-byte record per board at its `+0x16C`, twelve in all.

`BoardHolders` (`0x28` bytes, offsets from the start of the [chooser+0x16C]+board*0x28):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32[9]` | members | the word `+0x60` of each member holding the board as first or second board, in roster order (`0x0055883C`-`0x0055885A`, `0x00558871`-`0x00558891`) |
| `+0x24` | `u32` | count | how many members are listed, raised with each (`0x00558861`, `0x00558898`); `0x0055A340` reads it first (`0x0055A4D6`) |

### The board chooser's fields

The board chooser is the `0x390`-byte widget with procedure `0x00557DB0` that the chooser window `0x00558FB0` builds (The board chooser above).

`BoardChooser` (`0x390` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00557DB0` |
| `+0x0C0` | `void*` | window | the chooser window `0x00558FB0` that built the chooser: the creation record's first qword (`0x00557FE1`). On destroy the chooser clears the window's `+0xC8` and [`0x0209AC30`] + `0x320` (`0x005582C5`-`0x005582DC`); command `0x8002` sets the window's `+0xE0` bit `0x2` and `+0xDC` to the board the command carries, or clears the bit and stores `0xFF` for `0xFF`, and closes the window (`0x005583BE`-`0x0055841D`) |
| `+0x0C8` | `void*` | memberPanel | the `0xD0`-byte panel with procedure `0x00558CE0` that `0x00558C40` builds while this is 0 and opens under the main root, copying `+0xE8` into the keyboard cell `0x02CA8FE0` (`0x00558C55`-`0x00558CC7`); built at stage 2 (`0x00557EDD`) and again on a member switch, which closes the old one first (`0x0055878F`-`0x005587AE`); stage 4 shows the member's boards in it through `0x00558E70` (`0x00557E7B`); command `0x8002` closes it (`0x0055838C`-`0x0055839F`) |
| `+0x0D0` | `void*` | descriptionBox | the `0x3D8`-byte description box with procedure `0x00556F90` that `0x00556EC0` builds for the shown board while this is 0 (`0x00556ED5`-`0x00556F26`); turning the wheel writes the board to its `+0x3D1` and the board less 1 to `+0x3D2` (`0x00558536`-`0x00558551`); command `0x8002` and the confirm close it (`0x005583A6`-`0x005583B7`, `0x0055866F`-`0x00558682`) |
| `+0x0D8` | `void*` | picturesPart | the `0xE0`-byte part with procedure `0x00557760`, which draws the chooser's pictures through `0x005574C0`: built by `0x00557370` at the wheel centre less `0x28` in y on construction (`0x005581AC`, `0x005573CB`), closed by `0x00557340` on command `0x8002` (`0x00557349`-`0x0055735A`) |
| `+0x0E0` | `void*` | wheelPart | the `0xF0`-byte part with procedure `0x005565E0`, which draws the wheel's board pictures at the angle `+0x34C` and marks the boards set in `+0x364`: built by `0x005572B0` on construction (`0x005581BC`, `0x0055730B`), closed by `0x00557280` on command `0x8002` (`0x00557289`-`0x0055729A`) |
| `+0x0E8` | `void*` | namePart | the `0xF0`-byte part with procedure `0x005569F0`, which draws the board names (menu_command.bin `0x3ED` + board) around the wheel at the angle `+0x34C`: built by `0x005571F0` on construction (`0x005581D7`, `0x0055724B`), closed by `0x005571C0` on command `0x8002` (`0x005571C9`-`0x005571DA`); faded in by `0x002D04F0` at stage 4 (`0x00557E87`) and out on the confirm (`0x00558689`); `0x00558C40` copies it to `0x02CA8FE0` (`0x00558CAB`) |
| `+0x0F0` | `void*` | wheelPart2 | the `0xF0`-byte part with procedure `0x0055A340`, which draws at the angle `+0x34C`: built by `0x00557430` on construction (`0x005581CA`, `0x0055748B`), closed by `0x00557400` on command `0x8002` (`0x00557409`-`0x0055741A`); faded in at stage 4 (`0x00557EA6`) and out on the confirm (`0x005586A8`) |
| `+0x0F8` | `u8[72]` | gap0F8 | read and written by no function; nothing fixes its width |
| `+0x140` | `void*` | atlasC2 | the member picker's `+0xF0`, the lic_8_c2 label the board screen stores there (`0x005616FE`-`0x00561738`), copied through the window's `+0xC0` on construction (`0x00557FF7`-`0x00558005`); the pictures part copies it to its `+0xC8` when built (`0x005579D2`) |
| `+0x148` | `void*` | atlasC3 | the member picker's `+0xF8`, the lic_8_c3 label (`0x0056175E`-`0x00561765`), copied on construction (`0x0055800C`-`0x0055801A`); the pictures part copies it to its `+0xD0` (`0x005579E0`) |
| `+0x150` | `void*` | backAtlas | the member picker's `+0x100`, the lic_bk label (`0x0056169E`-`0x005616A8`), copied on construction (`0x00558021`-`0x0055802F`); the name part copies it to its `+0xE0` (`0x00556986`) |
| `+0x158` | `u32` | turnBits | the wheel's turn: bit `0x1` a turn is running and the bits under mask `0x3C` its curve, set to curve 1 by `0x00558A10` (`0x00558A84`-`0x00558A8B`); `0x00558AF0` steps while the bits under mask `0x3` are set, passing the bits under mask `0x3C` to `0x00248F40`, and clears the bits under mask `0x3` when the turn is done (`0x00558AF9`-`0x00558B3E`) |
| `+0x15C` | `i16` | turnFrom | the angle in degrees when the turn started, the low word of `+0x350` (`0x00558A98`, `0x00558AB8`); `0x00558AF0` adds the turned part of `+0x160` to it (`0x00558B35`, `0x00558B58`) |
| `+0x15E` | `i16` | turnTo | the board the wheel turns to: the shown board on construction (`0x00558135`) and each turn (`0x00558AB1`); `0x00558A10` does nothing when asked for the same board (`0x00558A30`) and turns the short way, through 360, when the boards are 0 and 11 (`0x00558A4F`-`0x00558A7E`) |
| `+0x160` | `i16` | turnBy | the degrees to turn, the board x 30 less `+0x15C` (`0x00558AA5`-`0x00558AC4`); `0x00558AF0` adds it times the curve's 0 to 1 to `+0x15C` (`0x00558B2E`, `0x00558B4D`) |
| `+0x162` | `i16` | turn162 | set to 0 by `0x00558A10` (`0x00558ACB`); no function reads it |
| `+0x164` | `u32` | turnFrames | the turn's length in frames, `0x00558A10`'s fourth argument (`0x00558AAB`): 12 from the turn command (`0x00558521`); passed to `0x00248F40` (`0x00558B12`) |
| `+0x168` | `u32` | turnStart | the frame counter `0x0208F570` when the turn started (`0x00558A92`-`0x00558A9F`); `0x00558AF0` passes the frames since then to `0x00248F40` (`0x00558B04`-`0x00558B0B`) |
| `+0x16C` | `u8[480]` | holders | twelve BoardHolders records, one per board (above): `0x005587E0` clears all `0x1E0` bytes and lists in them, for the first six of the nine roster slots `0x00282FA0` accepts that hold a first board, the member under its first and its second board (`0x00558800`-`0x00558898`); called on construction and at stage 4 (`0x005580DB`, `0x00557E6E`). The part `0x0055A340` reads the records through its `+0xD8` to place the members' marks around the wheel (`0x0055A3E0`, `0x0055A4D6`-`0x0055A4E9`) |
| `+0x34C` | `f32` | angle | the wheel's angle in radians, (360 - `+0x350`) / 180 x pi, written by `0x00558AF0` every tick (`0x00558B7B`-`0x00558B9D`); the parts `0x005565E0`, `0x005569F0` and `0x0055A340` draw by it (`0x00556629`, `0x00556712`, `0x00556B58`, `0x0055A392`, `0x0055A48F`) |
| `+0x350` | `i32` | degrees | the wheel's angle in degrees, 30 a board: the shown board x 30 on construction, moved by 360 when the boards are 0 and 11 (`0x00558132`-`0x00558169`, `0x00558A67`-`0x00558A7E`); stepped to `+0x15C` + `+0x160` x t during a turn and to the end when it finishes (`0x00558B45`, `0x00558B75`) |
| `+0x354` | `u32` | member | the member's roster slot: the window's `+0xD8` on construction (`0x00557FEB`-`0x00557FF1`), [`0x0209AC30`] + `0xDE0` on a member switch (`0x00558775`-`0x00558783`); `0x00282DF0` resolves it for the member's boards (`0x005580E9`, `0x00558434`, `0x005585D9`, `0x005588E1`) |
| `+0x358` | `i8` | board | the board shown, 0-11: the member's active board `0x003236B0`, or the window's `+0xDC` when `+0x388` bit `0x2` is set, 0 for no board (`0x005580E0`-`0x00558122`); `0x00557B90` steps it by one with the two directions, wrapping between 11 and 0, and posts the turn command `0x8000` (`0x00557C49`-`0x00557CB1`); `0x00556EC0` builds the description box for it (`0x00556EE2`); stage 4 sets its bit in `+0x364` (`0x00557E2D`); the confirm stores it (`0x00558637`-`0x00558652`) |
| `+0x359` | `u8[3]` | gap359 | read and written by no function; nothing fixes its width |
| `+0x35C` | `i32` | centreX | the wheel centre's x, half the screen width `0x01E0C1D8` (`0x0055816F`-`0x00558186`); the parts are placed and the effects started at it (`0x005581AC`-`0x005581F1`, `0x0055898F`, `0x005585F0`, `0x0055890B`) |
| `+0x360` | `i32` | centreY | the wheel centre's y, half the screen height `0x01E0C1DC` less `0x17` (`0x0055817F`-`0x005581A6`); the parts sit `0x28`, `0x2A` and `0x2B` above it (`0x005581A2`-`0x005581C1`) |
| `+0x364` | `u32` | boardsHeld | one bit per board: on construction the first and second boards of the nine roster slots `0x00282FA0` accepts (`0x00558081`-`0x005580D6`), and at stage 4 the board just chosen (`0x00557E2D`-`0x00557E41`); the wheel part tests each board's bit to pick the board's picture (`0x00556763`) |
| `+0x368` | `u32` | hintEffect | the effect `0x005588C0` starts below the wheel, `0x1C` while the member has no first board and `0x1F` once it has one, after stopping the old one (`0x005588D2`-`0x00558940`); stopped on closing (`0x0055830C`-`0x0055831B`) and after the confirm (`0x005586C7`-`0x005586D8`) |
| `+0x36C` | `u32` | confirmEffect | the effect `0x1B` the confirm starts at the wheel centre (`0x005585E4`-`0x00558601`); stage 4 waits while `0x003B2CE0` reports it running, then stops it and clears this (`0x00557E1A`-`0x00557E57`) |
| `+0x370` | `u32` | boardEffect | the effect 2 + board at the wheel centre, one above it: started on construction (`0x00558217`-`0x00558244`) and replaced on every turn by `0x00558960` (`0x0055897A`-`0x005589AD`) |
| `+0x374` | `u32` | turnEffect | the effect `0x00558960` starts on every turn, `0x1D` or `0x1A` by the turn command's direction (`0x005589B7`-`0x005589EB`); stopped on closing (`0x005582F5`-`0x00558306`) |
| `+0x378` | `u32` | centreEffect | the effect `0x1E` at the wheel centre, started on construction (`0x005581DC`-`0x00558208`) |
| `+0x37C` | `u8` | cuesRunning | 1 while the confirm's three cues play, set with stage 4 by one word store (`0x00558607`); the tick waits each cue's delay `+0x380` and plays its cue `+0x383` (`0x00557F5E`-`0x00557FA2`), and clears this after the third (`0x00557FAD`-`0x00557FBA`) |
| `+0x37D` | `u8` | stage | the opening stage (`0x00557DF0`): 0 first tick: 1 with a delay of `0x10` frames when the save-wide flag `0xBB` is clear (`0x00557F3E`-`0x00557F4C`), else 2; 1 waits the delay, sets flag `0xBB` and opens message `0x18` (`0x00557EFA`-`0x00557F30`), then 3; 2 builds the member panel and description box (`0x00557ED2`-`0x00557EF1`), then 3; 3 idle; 4 after the confirm: waits for the confirm effect, then marks the board and fades the parts in (`0x00557E1A`-`0x00557EC8`), then 3. Command `0x11D` with `0x18` sets 2 (`0x00558707`) |
| `+0x37E` | `u8` | stageDelay | frames left at stage 1, `0x10` from the word store (`0x00557F4C`); counted down by the tick (`0x00557EFA`-`0x00557F07`) |
| `+0x37F` | `u8` | cueIndex | the cue playing, 0-2: 0 on the confirm (`0x0055863E`), raised after each cue (`0x00557FA7`-`0x00557FAD`) |
| `+0x380` | `u8` | cueDelay0 | frames before the first cue, `0x40` (`0x00558620` with `+0x381`); counted down by the tick (`0x00557F73`-`0x00557F81`) |
| `+0x381` | `u8` | cueDelay1 | frames before the second cue, `0x18` (`0x00558620`) |
| `+0x382` | `u8` | cueDelay2 | frames before the third cue, `0x38` (`0x00558629`) |
| `+0x383` | `u8` | cue0 | the first cue, sound `0x45` (`0x00558610` with `+0x384`), played through `0x00249C60` (`0x00557F9A`-`0x00557FA2`) |
| `+0x384` | `u8` | cue1 | the second cue, sound `0x4A` (`0x00558610`) |
| `+0x385` | `u8` | cue2 | the third cue, sound `0x6B` (`0x00558619`) |
| `+0x386` | `u8[2]` | gap386 | read and written by no function; nothing fixes its width |
| `+0x388` | `u32` | flags | bit `0x1`: input is held: set on construction (`0x00558235`), by a step (`0x00557CDD`) and when the confirm question opens (`0x00558475`, `0x005584E1`), cleared at stages 2 and 4 (`0x00557E4C`, `0x00557EEA`) and by the answer No (`0x005586EE`); the input turn does nothing while it is set (`0x00558261`). Bit `0x2`: start at the window's board: the window's `+0xE0` bit `0x2` (`0x00558036`-`0x0055804C`), tested at `0x005580E0`. Bit `0x4`: the member has no first board, so the confirm stores a first board through `0x00323740` rather than a second through `0x003236F0` (`0x00558475`, `0x005584DE`, `0x00558630`-`0x00558652`) |
| `+0x38C` | `u8[4]` | tail38C | read and written by no function; nothing fixes its width |

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
- One purchase animates at most 32 changed squares; a square past the 32nd is neither listed nor updated and keeps
  its old look until a later fill lists it or, without the collect bit, copies its state (`0x0055B380`-`0x0055B3A6`).

## Related

- [License Board](../Items-Equipment-Shops-And-Licenses/license-board.md) - the board file and the two board slots.
- [Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md) - the node records and what obtaining one does.
- [Dialogs](dialogs.md) - the description box and the confirm and notice boxes.
- [Menus](menus.md) - the Licenses entry.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00202C70` is called by `0x003F1E90`; `0x002B58B0` is called by `0x0023A570`; `0x0036A100` is called by
  `0x00330310`, `0x003306E0`.
- Actor entity: those functions are documented on [hud](hud.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- Core runtime: `0x0022A4B0` is called by `0x0017D4C0`; `0x00244DD0` calls `0x00229DF0`, `0x00229E70`, `0x00229EA0`; `0x002465F0`
  calls `0x001EDDA0`; those functions are documented on
  [game application](../Engine-Core/game-application.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [global state accessors](../Engine-Core/global-state-accessors.md).
- Movement: `0x00202C70` is called by `0x00230790`, `0x00338490`; those functions are documented on
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [bestiary](../Enemy-Spawning/bestiary.md).
- Save load settings: `0x00249210` is called by `0x00582790`; those functions are documented on
  [mrp menu resource packages](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md).
- World area: `0x0036A100` is called by `0x00267930`, `0x003319D0`, `0x003EA820`; those functions are documented on
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [item and ability ids](../Engine-Core/item-and-ability-ids.md).
