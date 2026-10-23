---
title: "Opening the main menu: the steps from Triangle to the open menu, and back when it closes"
kind: "operation"
category: "Menus and HUD"
addresses: "0x002E1B10, 0x002E09A0, 0x00254B50, 0x00280A00, 0x00252B40, 0x00280D20, 0x00280DE0, 0x00246AD0, 0x00281ED0, 0x002E1BA0"
---

## What the player sees

Triangle in the field opens the main menu. Its entries open their screens, and closing the menu returns to the
field. During scenes and while another menu is open, Triangle
does nothing.

## Steps

1. **The post.** On Triangle the input arbiter posts id 2 to the mailbox with `0x002E1B10`, which refuses while the
   mailbox is blocked or policy bit 0 is set ([menus](menus.md#the-mailbox),
   [action availability](../Controls-And-Input/action-availability.md#the-combined-mask)).
2. **The delivery.** Once per world tick the drain `0x002E09A0` takes the request: it throws it away while manager
   slot 0 is not ready, drops id 2 when `0x0037B330` answers non-zero or policy bit 0 or 3 is set, and waits while a
   party record is busy ([menus](menus.md#delivery)).
3. **The router.** `0x00254B50` refuses while the request latch is set or when the combined action policy blocks the
   id, then closes what is open and dispatches by id ([menus](menus.md#the-router),
   [action availability](../Controls-And-Input/action-availability.md#what-each-bit-blocks)).
4. **The generic route.** `0x00280A00` refuses while a menu widget sits at the root, sets the request word and latch
   (`0x00252B40(2, 1)`) and builds the two widgets that open the screen by id ([menus](menus.md#the-requests)).
5. **The main menu.** Parameter 0 builds `0x00280D20`, the main menu procedure `0x00280DE0`
   ([menus](menus.md#the-requests),
   [menu screens](menu-screens.md#the-party-menu-and-its-entries), [widgets](widgets.md#construction)).
6. **The opening run.** `0x00280D20` installs the menu's descriptor (`0x00247570`) and opens it under the root through
   `0x00246AC0`, which hands it to `0x00246AD0`: the widget is attached, its forward run starts and message 14 is sent
   ([widgets](widgets.md#the-tree), [widgets](widgets.md#opening-and-closing-runs), [widget messages](widget-messages.md)).
7. **While it is open.** The drain sets action-policy row 7 to `0x100203` and the main loop to mode 4, which
   captures the screen once and becomes mode 3, waiting each frame for the menu to close
   ([menus](menus.md#while-a-menu-is-open)).
8. **An entry.** The entry dispatcher `0x00281ED0` opens each entry's screen by its `menu_command.bin` id
   ([menu screens](menu-screens.md#the-party-menu-and-its-entries)).
9. **The close.** When the menu closes, the loop returns to mode 2, sets mailbox `+0xE` and `+0xF` (`0x002E1BA0`) and
   clears row 7 ([menus](menus.md#while-a-menu-is-open), [menus](menus.md#what-a-menu-hands-back)).

## Outcomes

- **A second post before delivery** overwrites the first and still answers 1 ([menus](menus.md#the-mailbox)).
- **A request the router refuses** is still cleared by the drain, so it is lost, not retried
  ([menus](menus.md#delivery)).
- **While a menu is open** the router refuses ids 1, 2, 3, 5 and 14 ([menus](menus.md#while-a-menu-is-open)).
- **A script** opens full-screen menus through `openfullscreenmenu_48d`, which posts, blocks the mailbox and waits
  until a menu closes ([menus](menus.md#the-script-verbs)).
- **A script mask close** or the area unload also closes the main menu ([menus](menus.md#while-a-menu-is-open)).
- **When the whole party has fallen** id 24 shows the notice and then opens the main menu
  ([menus](menus.md#the-requests)).

## Related

- [Menus](menus.md): the router, the mailbox and delivery in full.
- [Menu screens](menu-screens.md): every screen and widget procedure.
- [Widgets](widgets.md): how a menu element is built, opened and closed.
