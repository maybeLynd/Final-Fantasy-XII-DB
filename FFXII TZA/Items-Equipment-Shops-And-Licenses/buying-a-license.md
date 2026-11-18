[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Buying a license

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Buying a license: the steps from the Licenses menu to the owned square and the lit neighbours | operation | Items, equipment, shops and licenses | Licenses | The order in which the game sells a License Board square: the member pick and the board or the chooser, the grid and each square's answer, the detail panel, the take request and its refusals, the question for the square's rule, the purchase that charges the LP and sets the owned bit, the Quickening and Mist effects, the stats rebuild, and the screen's pan, light-up, sweep and notices; with the refused, unique and Second Board cases, each step linked to the page that explains it. | 0x00560910, 0x0055BFF0, 0x00323600, 0x0055A1F0, 0x0055D978, 0x003235C0, 0x00323910, 0x00323D10, 0x0030FED0, 0x0055F3E0, 0x0055DD70 |

## What the player sees

In Licenses the player picks a character and moves over the board. Confirm shows a square's name, cost and
contents; confirm again asks to obtain it. After yes, the License Points drop, the square lights, the squares
next to it light one after another, and a notice may announce a new Esper, a new Mist ability or the Second Board.

## Steps

1. **The member pick.** The member-pick widget `0x00560910` opens the board screen for a member with a board, or the
   board chooser for one without ([License Board screen](../Menus-And-HUD/license-board-screen.md#opening),
   [License Board screen](../Menus-And-HUD/license-board-screen.md#the-board-chooser),
   [menu screens](../Menus-And-HUD/menu-screens.md)).
2. **The grid.** The fill `0x0055BFF0` reads each board cell and its license node, and asks `0x00323600` for the
   member's answer for the node, which picks the square's state
   ([License Board screen](../Menus-And-HUD/license-board-screen.md#building-the-grid),
   [License Board screen](../Menus-And-HUD/license-board-screen.md#square-states), [License Board](license-board.md)).
3. **The detail panel.** Confirm on a square opens its panel (`0x0055A1F0`): the current one of the four detail
   panes is filled for the cursor square with the name, the LP cost and up to eight contents and opened, and the
   other three are closed (`0x0055A23C`-`0x0055A30D`)
   ([License Board screen](../Menus-And-HUD/license-board-screen.md#obtaining-a-license),
   [License Board screen](../Menus-And-HUD/license-board-screen.md#detail-panel-and-member-switch)).
4. **The take request.** Confirm again sends take-square to the view. The owned Second Board square opens the
   second-board chooser for a member with none; any other owned square, or one not obtainable yet, plays
   sound 5, an obtainable square the member cannot afford shows "Insufficient license points.", and an affordable one
   asks the question ([License Board screen](../Menus-And-HUD/license-board-screen.md#obtaining-a-license)).
5. **The question.** The text follows the square's rule: one character only, up to three Quickenings, one character
   per Esper, the Second Board, or a plain "Obtain {name}?"
   ([License Board screen](../Menus-And-HUD/license-board-screen.md#obtaining-a-license),
   [licenses](licenses.md#why-a-square-is-refused)).
6. **The purchase.** Yes reaches `0x0055D978`, which records the node in bank 8 and calls `0x003235C0(row, node, 1)`;
   that calls the setter `0x00323910` with `flags` 0, so the LP is charged
   ([License Board screen](../Menus-And-HUD/license-board-screen.md#obtaining-a-license),
   [licenses](licenses.md#buying-a-square)).
   - The record `0x003235C0` gives the setter is `[0x02EBF190] + 8 + row × 0x1C8`, or null for a row above `0x27`,
     which the setter refuses; its third argument goes through as `set` (`0x003235C0`-`0x003235F0`).
7. **The refusal test.** After its checks of the record and the node, the setter asks `0x00323D10`, which must
   answer 0 ([licenses](licenses.md#buying-a-square), [licenses](licenses.md#why-a-square-is-refused)).
8. **The LP and the bit.** The node's cost is taken from the member's LP, kept between 0 and 99,999, and the owned
   bit is set ([licenses](licenses.md#buying-a-square), [licenses](licenses.md#the-test)).
9. **Quickenings and Mist.** A Quickening square grants the member's next Quickening, and the MP bars, the number
   of Mist charges the member can hold, rise when lower to the Quickening squares owned or the Esper's Mist
   charges, at most 3
   ([licenses](licenses.md#buying-a-square), [licenses](licenses.md#quickenings)).
10. **The stats.** `0x0030FED0(record, 0x97)` rebuilds the stats and augments
    ([licenses](licenses.md#buying-a-square), [augments](../Damage-And-Battle-Formulas/augments.md#the-rebuild)).
11. **The screen.** `0x0055F3E0` pans to the square, lights it, runs the change sweep `0x0055DD70`, waits for the
    transitions and shows the notices ([License Board screen](../Menus-And-HUD/license-board-screen.md#obtaining-a-license),
    [License Board screen](../Menus-And-HUD/license-board-screen.md#the-change-sweep)).

## Outcomes

- **A square another character owns** under the one-character rules, a fourth Quickening, or an Esper square
  whose Esper is not present is refused by `0x00323D10` with its reason
  ([licenses](licenses.md#why-a-square-is-refused)).
- **The Second Board square** ends with the chooser opening for the member's second board
  ([License Board screen](../Menus-And-HUD/license-board-screen.md#obtaining-a-license)).
- **In preview** obtaining a square is refused with sound 5
  ([License Board screen](../Menus-And-HUD/license-board-screen.md#preview)).
- **A newly reachable square past the 32nd** in one sweep keeps its old look until the next sweep
  ([License Board screen](../Menus-And-HUD/license-board-screen.md#the-change-sweep)).
- **Node 229, Brawler,** also refreshes the unit's held model and cancels its current action
  ([licenses](licenses.md#buying-a-square)).
- **An equipment license** lets the piece pass the license step of equipping
  ([equipping an item](equipping-an-item.md), [licenses](licenses.md#the-test)).

## Related

- [Licenses](licenses.md): the test, buying, refusals and resetting the boards.
- [License Board screen](../Menus-And-HUD/license-board-screen.md): the screen in full.
- [License Board](license-board.md): the board files and their squares.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat action: `0x0030FED0` is called by `0x002FDDA0`; `0x00323910` calls `0x00308FF0`; those functions are documented on
  [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md),
  [action definition row](../Battle-Actions/action-definition-row.md).
- Combat formula: `0x0030FED0` calls `0x002FEF30`, `0x0031B860`; `0x0030FED0` is called by `0x003112F0`; `0x00323910` calls
  `0x0031B860`; `0x00323910` is called by `0x0023AC80`.
- Combat formula: those functions are documented on [force fight mode](../Engine-Core/force-fight-mode.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md),
  [traps](../World-Areas-And-Travel/traps.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md).
- Gameplay: `0x0030FED0` calls `0x00322C50`; `0x00323910` calls `0x00322C50`; `0x00323D10` calls `0x0030B0E0`, `0x00322C50`; those
  functions are documented on [identifier spaces](../Engine-Core/identifier-spaces.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Input: `0x0055F3E0` calls `0x002D6620`; those functions are documented on [controls](../Controls-And-Input/controls.md).
- Party: `0x0030FED0` is called by `0x00328BD0`; those functions are documented on
  [party control modes](../Engine-Core/party-control-modes.md).
- Resource: `0x00560910` calls `0x00249580`, `0x0024A5A0`; those functions are documented on
  [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md).
- Rewards progression economy: `0x0030FED0` is called by `0x0030C470`, `0x0030C650`; those functions are documented on
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Spawn encounter lifecycle: `0x0030FED0` is called by `0x0023A410`; those functions are documented on
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md).
- Status periodic terminal: `0x0030FED0` calls `0x0030E130`, `0x0030E360`; `0x0030FED0` is called by `0x0030E130`, `0x0030E360`,
  `0x0030E8F0`, `0x0030F690`; `0x00323910` calls `0x0030FED0`.
- Status periodic terminal: those functions are documented on
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [battle orders](../Battle-Actions/battle-orders.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- UI: `0x0055A1F0` calls `0x00559E30`; `0x0055A1F0` is called by `0x0055A180`; `0x0055BFF0` calls `0x0055DEA0`, `0x0055E090`,
  `0x0055E230`, `0x0055E3F0`; `0x0055BFF0` is called by `0x0055B560`; `0x0055F3E0` calls `0x005597C0`, `0x0055A180`, `0x0055B2B0`,
  `0x0055B960`, `0x0055EF10`, `0x00561800`, `0x00561F20`; `0x00560910` calls `0x002814E0`, `0x00285F20`, `0x00291D70`, `0x00291D80`,
  `0x00558F20`, `0x00561300`.
- UI: those functions are documented on [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md),
  [license board screen](../Menus-And-HUD/license-board-screen.md), [clan primer](../Menus-And-HUD/clan-primer.md),
  [menu screens](../Menus-And-HUD/menu-screens.md), [stats](../Damage-And-Battle-Formulas/stats.md).

---

[← Licenses](licenses.md)
