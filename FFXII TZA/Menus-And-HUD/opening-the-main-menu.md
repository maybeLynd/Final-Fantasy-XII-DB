[Home](../../README.md) / [Menus and HUD](README.md) / Opening the main menu

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Opening the main menu: the steps from Triangle to the open menu, and back when it closes | operation | Menus and HUD | How menus work | The order in which the game opens the main menu: the post to the one-slot mailbox, the once-a-tick delivery and its drops, the router's refusals and the close of what is open, the generic route and its widgets, the main menu's build and opening run, the main loop's capture and wait while the menu is open, an entry's screen, and the close that hands back to the field; with the refused, overwritten and scripted cases, each step linked to the page that explains it. | 0x002E1B10, 0x002E09A0, 0x00254B50, 0x00280A00, 0x00252B40, 0x00280D20, 0x00280DE0, 0x00246AD0, 0x00281ED0, 0x002E1BA0 |

## What the player sees

Triangle in the field opens the main menu. Its entries open their screens, and closing the menu returns to the
field. During scenes and while another menu is open, Triangle
does nothing.

## Steps

1. **The post.** On Triangle the input arbiter posts id 2 to the mailbox with `0x002E1B10`, which refuses while the
   mailbox is blocked or availability bit `0x1` is set ([menus](menus.md#the-mailbox),
   [action availability](../Controls-And-Input/action-availability.md#the-combined-mask)).
2. **The delivery.** Once per world tick the drain `0x002E09A0` takes the request: it throws it away while manager
   slot 0 is not ready, drops id 2 when `0x0037B330` answers non-zero or availability bit `0x1` or `0x8` is set, and waits while a
   party record is busy ([menus](menus.md#delivery)).
3. **The router.** `0x00254B50` refuses while the request latch is set or when the combined action availability mask blocks the
   id, then closes what is open and dispatches by id ([menus](menus.md#the-router),
   [action availability](../Controls-And-Input/action-availability.md#what-each-bit-blocks)).
4. **The generic route.** `0x00280A00` refuses while a menu widget sits at the root, sets the request word and latch
   (`0x00252B40(2, 1)`) and builds the two widgets that open the screen by id ([menus](menus.md#the-requests)).
5. **The main menu.** Parameter 0 builds `0x00280D20`, the main menu procedure `0x00280DE0`
   ([menus](menus.md#the-requests),
   [menu screens](menu-screens.md#the-party-menu-and-its-entries), [widgets](widgets.md#construction)).
6. **The opening run.** `0x00280D20` builds the main menu, `0x288` bytes, only while the root's `+0xD8` is 0, which the
   menu sets to itself on message 1 (`0x00280D3A`-`0x00280D6D`, `0x00281B23`), and calls `0x002C99A0([0x01E0C3B8],
   [0x01E0C3BC], 1)`, which runs the band builder `0x002C99E0` (`0x00280D72`-`0x00280D84`,
   [menu screens](menu-screens.md)).
   - The descriptor `0x00915C10` (`0x00247570`) and the opening through `0x00246AC0` belong to the side mask `0x0029D340` at
     `[0x0209C318]`, a `0xC0`-byte widget built the first time (`0x00280D89`-`0x00280DC6`). On every run, not only the
     first, `0x00246AC0` hands it to `0x00246AD0` (`0x00280D93`, `0x00280DC6`)
     ([widgets](widgets.md#the-tree), [widgets](widgets.md#opening-and-closing-runs),
     [widget messages](widget-messages.md)).
     - `0x00246AD0` attaches it when it has no parent (`0x00246AE5`). In run state 0 or 1 it starts its forward run
       and sends message 14; in state 4 it reverses the closing run and sends message 14; in states 2, 3 and
       5-15 it starts no run and sends no message (`0x00246B5C`-`0x00246B6C`).
   - The main menu opens itself under the root with `0x00246AD0` on message 16, sent when its resources have loaded
     (`0x00280E62`-`0x00280EA7`).
7. **While it is open.** The drain sets action availability row 7 to `0x100203` and the main loop to mode 4, which
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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 17 calls with 8 other topics</summary>

**Characters and objects** (explained on [debug menu](../Engine-Core/debug-menu.md))

| Function | | Functions |
|---|---|---|
| `0x002E09A0` | calls | `0x00263FF0` |

**Sound and music** (explained on [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md))

| Function | | Functions |
|---|---|---|
| `0x00280DE0` | calls | `0x002DEE50` |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x002E09A0` | calls | `0x00229F00` |
| `0x002E1BA0` | is called by | `0x0022B8C0` |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00254B50` | is called by | `0x00253C70`, `0x002E09A0` |
| `0x002E09A0` | calls | `0x00248F00` |
| `0x002E1B10` | is called by | `0x00253C70` |
| `0x0037B330` | is called by | `0x002E09A0` |

**Graphics** (explained on [frame update order](../Engine-Core/frame-update-order.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md))

| Function | | Functions |
|---|---|---|
| `0x00246AC0` | is called by | `0x002B7B80`, `0x002BAF80` |
| `0x0029D340` | calls | `0x002DC290` |
| `0x0037B330` | is called by | `0x003DD4C0` |

**Game files and data tables** (explained on [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

| Function | | Functions |
|---|---|---|
| `0x00280DE0` | calls | `0x0024A5A0` |
| `0x0037B330` | is called by | `0x0024AC30` |

**Scripts and script commands** (explained on [menus](menus.md))

| Function | | Functions |
|---|---|---|
| `0x002E1B10` | is called by | `0x0050DAB0` |

**World, areas and travel** (explained on [debug logging](../Engine-Core/debug-logging.md))

| Function | | Functions |
|---|---|---|
| `0x002E09A0` | is called by | `0x00314020` |

</details>

---

[Menus →](menus.md)
