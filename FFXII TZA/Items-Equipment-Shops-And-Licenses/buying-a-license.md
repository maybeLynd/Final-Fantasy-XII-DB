---
title: "Buying a license: the steps from the Licenses menu to the owned square and the lit neighbours"
kind: "operation"
category: "Items, equipment, shops and licenses"
addresses: "0x00560910, 0x0055BFF0, 0x00323600, 0x0055A1F0, 0x0055D978, 0x003235C0, 0x00323910, 0x00323D10, 0x0030FED0, 0x0055F3E0, 0x0055DD70"
---

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
3. **The detail panel.** Confirm on a square opens its panel (`0x0055A1F0`) with the name, the LP cost and up to eight
   contents ([License Board screen](../Menus-And-HUD/license-board-screen.md#obtaining-a-license),
   [License Board screen](../Menus-And-HUD/license-board-screen.md#detail-panel-and-member-switch)).
4. **The take request.** Confirm again sends take-square to the view: an owned square or one not obtainable yet plays
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
7. **The refusal test.** The setter first asks `0x00323D10`, which must answer 0
   ([licenses](licenses.md#why-a-square-is-refused)).
8. **The LP and the bit.** The node's cost is taken from the member's LP, kept between 0 and 99,999, and the owned
   bit is set ([licenses](licenses.md#buying-a-square), [licenses](licenses.md#the-test)).
9. **Quickenings and Mist.** A Quickening square grants the member's next Quickening, and the MP bars rise with the
   Quickening squares owned or the Esper's Mist charges, at most 3
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
