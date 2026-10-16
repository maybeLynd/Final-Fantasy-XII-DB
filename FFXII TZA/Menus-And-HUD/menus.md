---
title: "Menus: how a menu screen is asked for and opened, the one-slot mailbox, the refusals that keep a menu shut, and what a menu hands back"
kind: "system"
category: "Menus and HUD"
addresses: "00254B50, 0215F1A0, 002E1B10, 002E1A60, 002E0DA0, 002E09A0, 00280A00, 0027FB70"
---

## What the player sees

- Triangle opens the main menu: Party, Status, Licenses, Equip, World Map, Inventory, Gambits, Clan Primer and Config.
- Talking to a save crystal, a shopkeeper or a notice board opens its own screen.
- Menus stay shut during scenes and while another menu is open.
- When every member of the party has fallen, a notice appears, and then the main menu opens to reform the party.

## How it works

### The router

`00254B50(request, parameter, flag)` opens a menu (`00254B50`-`00254C40`):

1. It keeps the low 15 bits as the id (`00254B69`).
2. It refuses while the request latch `02092734` is 1 (`00254B71`).
3. It refuses when the combined action policy has a bit whose word in `01E0C2C0` holds the id (`00254B80`-`00254BC1`);
   that can refuse ids 1, 2, 3, 5, 14 and 21 ([Action availability](../Controls-And-Input/action-availability.md)).
4. It closes what is open (`0017E7D0`, `0035DA80`, `003C8990`) and dispatches through the byte map `00254C70`
   (`00254BD6`-`00254BF9`).

### The requests

| Id | Route | Opens |
|---:|---|---|
| `1`, `4` | `0035D660`, after its own refusals (`0035D66D`, `0035D67B`) | the command menu, widget procedure `00279E20` |
| `2` | generic; parameter 0 builds `00280D20` (`0027FC9C`) | the main menu, procedure `00280DE0` |
| `3` | `0035D980` | choosing the party leader: "Select a new party leader." (`menu_message.bin` `86E`<sub>h</sub>) |
| `5` | `003C87B0` | the field target cycle |
| `6` | generic, `0027F8DB`-`0027F984` | the save crystal's save and load menu, `00583930` |
| `10` | generic, `0057B800(parameter)` (`0027FCC2`-`0027FCDA`) | a shop; the parameter is the shop |
| `11` | generic, `003EF750` (`0027FFB5`-`0027FFC3`) | game over, procedure `003EF830` |
| `12` | `0028E970` | the special-attack window, procedure `002D5EB0` |
| `15` | generic, `0027FA11` | the world map with the title "Airship Route" (`help_menu.bin` `C04`<sub>h</sub>) |
| `17` | generic, `0027F98E` | the world map with the title "Choose your destination." (`C03`<sub>h</sub>) and the confirm "Fly to ...?" (`menu_message.bin` `7FF`<sub>h</sub>) |
| `18` | generic, `0027F99D` | the world map with no title |
| `19` | generic, `0037FF80(parameter)` (`0027F9AF`) | the notice board's list |
| `22` | generic | by parameter, below |
| `24` | `0035D080` | the notice "All members of the party have fallen. ..." (`86F`<sub>h</sub>), then the main menu |

The generic route `00280A00` refuses while a menu widget sits at the root's `+C0`<sub>h</sub> or `+B8`<sub>h</sub> (`00280A1A`-`00280A30`).
Otherwise it sets the request word and latch through `00252B40(id, 1)` and builds the two widgets `0027FB70` and
`00280140`, which open the screen by id.

### Ids 2 and 22 with a parameter

`002E1A60` turns selector 6's parameter 0, 1 and 2 into `40`<sub>h</sub>, `41`<sub>h</sub> and `42`<sub>h</sub> (`002E1A7B`-`002E1AA1`):

| Parameter | Opens |
|---|---|
| 1-`20`<sub>h</sub> | the world map, "Airship Route", with the parameter as the route |
| `21`<sub>h</sub>-`3F`<sub>h</sub>, and 0 for id 22 | the location map (`0027F9E3`-`0027F9EC`) |
| `40`<sub>h</sub> | the main menu on Gambits, with the help "Change the conditions under which an action is performed..." (`002D7070`) |
| `41`<sub>h</sub> | the main menu on Licenses |
| `42`<sub>h</sub> | the map command tutorial (`0027FE7E`, `0027F9F3`-`0027FA05`) |

### The mailbox

The mailbox at `0215F1A0` holds one request:

| Cell | Holds |
|---|---|
| `+0`<sub>h</sub> `u8` | pending |
| `+1`<sub>h</sub> `u8` | blocked: every post refuses while it is set |
| `+4`<sub>h</sub> `u32` | the id |
| `+8`<sub>h</sub> `u32` | the parameter |
| `+E`<sub>h</sub> `u8` | set when a menu closes |
| `+F`<sub>h</sub> `u8` | set when a menu closes; read by `is_callpartymenu_status` |

`002E1B10(id, parameter)` posts; for id 2 it also refuses on policy bit 0 (`002E1B27`-`002E1B33`). A second post before
delivery overwrites the first and still answers 1 (`002E1B35`-`002E1B47`).

| Poster | Posts |
|---|---|
| the input arbiter | id 2 on Triangle (`00253D78`); id 2 on Select and L3 with `21`<sub>h</sub>, the location map (`00253EE6`, `00253F53`), or, once story flag `5E`<sub>h</sub> is set, with `00264640(2)` (`00253F44`) |
| `0035C81E` | id 11, game over |
| `0035D750` | id 2, after the party-fallen notice |
| `002E1A60` | a script selector, below |
| `002E1AE0` | id 12 |

The router is also called directly, without the mailbox:

| Caller | Id | Site |
|---|---:|---|
| the input arbiter | `1`, `3` | `002541C7`, `002540D2` |
| `0035BC50`, when a member cannot lead | `3` | `0035BF2F`, through `00254B40` |
| `0035C7B0`, the party-fallen check | `24` | `0035C7FF`, through `00254B40` |
| the target cycle widget `003C8B70` | `1` | `003C8F65`, through `00254B40` |

`00254B40(id)` is `00254B50(id, 0, 0)`. The arbiter also runs request 5's route itself (`00254044`).

### The script verbs

`002E0DA0` turns a script selector into an id, keeping bit 15 (`002E0DA6`-`002E0E00`):

| Selector | 0 | 1 | 2 | 3 | 4 | 5 | 6 | above 6 |
|---|---|---|---|---|---|---|---|---|
| Id | 17 | 18 | 10 | 15 | 19 | 6 | 22 | 2 |

| Verb | Id | Does | Scripts |
|---|---|---|---|
| `openfullscreenmenu_48d` | `48D`<sub>h</sub> | posts a selector and parameter, sets blocked and waits until a menu closes (`003462D0`, `00352E00`) | 1,274 calls |
| `openfullscreenmenu` | `472`<sub>h</sub> | posts the same, without waiting | none |
| `openspattackwindow` | `2A8`<sub>h</sub> | posts id 12 | 1 |
| `spattackwindowsync` | `2A9`<sub>h</sub> | waits on the special-attack window | 1 |
| `tutorial_sync_partymenu` | `3A6`<sub>h</sub> | waits until the next menu closes | none |
| `clear_callpartymenu_status`, `is_callpartymenu_status` | `561`<sub>h</sub>, `562`<sub>h</sub> | clear and read mailbox `+F`<sub>h</sub> | 1 each |

Four more verbs read or set menu state through helpers of their own:

| Verb | Id | Helper | Does |
|---|---|---|---|
| `spattackwindowsync` | `2A9`<sub>h</sub> | `002E1660` | keeps waiting while `0028F7C0` answers 1 or 2; it answers 3 with no special-attack window at `[0209BE80] + 10FB0h`, or when the window's `+752`<sub>h</sub> is 1 or bit 0 of its `+749`<sub>h</sub> is set, and 1 otherwise |
| `get_interventionmenu_status` | `457`<sub>h</sub> | `002E2340` | 0 without the battle menu (`[0209BE80] + AB30h`, refused by bit 13 of `+10F68`<sub>h</sub>), otherwise 1 with bit 4 of `+10F68`<sub>h</sub> set and 2 without (`0028F6A0`) |
| `get_interventionmenu_commandstatus` | `45A`<sub>h</sub> | `002E2320`, `002E0E30` | the battle menu's current command (`002767C0`, through `0028F5F0`) plus 1 for 0-7, the same value for 9-17, 18 and 19 swapped, and 0 for any other |
| `setpartymenustatus` | `45F`<sub>h</sub> | `002E23E0`, `002E13C0` | sets or clears one bit of `[020927C0] + 32C4h` (`00254E00`): kinds 0-7 give bits 0, 1, 9 and `12`<sub>h</sub>-`16`<sub>h</sub>, kind 9 bit `1E`<sub>h</sub>, any other `1D`<sub>h</sub> |

`show_escapingwindow` (`458`<sub>h</sub>) jumps from `002E2310` to the return stub `0016D6A0` and does nothing. The bits
`1E`<sub>h</sub>-`23`<sub>h</sub> of the same word lock Config rows ([Config screen](config-screen.md)). `setmenudisablestatus` (`3A5`<sub>h</sub>) sets or clears bit n of
`0215F1C4` through `002E1BE0`, one of the 16 words `002E0FA0` ORs together; `002E12E0` passes 0-18 and turns any other value into -1, which is refused.

Selector 5 with bit 15, the save menu, is called 1,148 times; selector 2, the shops, 98 times with 57 shops;
selector 4, the notice board, 8 times; selector 0 with bit 15, the destination map, 18 times. Bit 15 makes the screen
open with no fade (`0027FF6E`-`0027FF77`).

### Delivery

The drain `002E09A0` runs once per world tick:

1. While manager slot 0 is not ready, it throws the request away (`002E0B8B`-`002E0BAA`).
2. A pending id 2 is dropped when `0037B330` answers non-zero or policy bit 0 or 3 is set (`002E0BC0`-`002E0C65`).
3. While a party record is busy or another request word is held, it waits and keeps the request (`002E0C87`-`002E0CC2`).
4. It then tests `00226BA0` and `0053DD10` for ids other than 12, 15, 17, 18 and 19 (`002E0CC9`-`002E0CF3`), but
   `0053DD10` always answers 1, so this never holds a request.
5. It calls the router and clears pending whether or not the router opened anything (`002E0CFC`-`002E0D10`).
6. It always clears blocked (`002E0D3E`).

### While a menu is open

When the router opens a full-screen id, 2, 6, 8-11, 15-19 or 22 (`00253BC0`), the drain sets action-policy row 7 to
`100203`<sub>h</sub> and the main loop's mode to 4 (`002E0D2A`-`002E0D39`). Mode 4 captures the screen once and becomes mode 3,
which waits each frame for the menu to close (`0022BB62`). Then the loop returns to mode 2, sets mailbox `+E`<sub>h</sub> and
`+F`<sub>h</sub> (`002E1BA0`) and clears row 7 (`0022BB81`-`0022BBC5`). While row 7 is set, the router refuses ids 1, 2, 3, 5 and
14.

A script mask close closes the main menu too. `002E2400(fast)`, the body of `maskclose` and `maskclosefast`
([Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)), and the area unload `002E06B0` run
`0029D210`, which closes the widget `0029CF90` at `[0209C380]`, which draws bands at the top and bottom of the frame
(`002DC290`), and the main menu at `[0209C318]`
(`00244F00`). For the fast close, argument 1 or `11`<sub>h</sub>, they close with the default animation descriptor `00915198`,
otherwise with `00916330` (`00247570`).

### What a menu hands back

| Value | Written by | Read by |
|---|---|---|
| the chosen map node's paired value, singleton `+10FAC`<sub>h</sub> | the world map (`002901D0`, `0029020E`) | the script verb's result, for ids 17 and 18 only (`00254710`) |
| mailbox `+E`<sub>h</sub>, `+F`<sub>h</sub> | the menu close (`002E1BA0`) | `openfullscreenmenu_48d`, `tutorial_sync_partymenu`, `is_callpartymenu_status` |
| the main menu's chosen entry, root `+DF8`<sub>h</sub> | `00280DE0` (`002810FC`) | the Equip compares (`00293791`-`00295ACB`) |
| the command menu's chosen member, `+2FE0`<sub>h</sub> | `00278135`, `0027A5A1` | 12 readers, resolved through `002732E0` |

### Ids nothing posts

No shipped code path or script posts ids 4, 7, 8, 9, 13, 14, 16, 20, 21 and 23. The one exception is a developer verb,
body `0050DAB0`, which posts any id its script passes (`0050DAC4`); no script calls it. Ids 15 and 18 are reached only by
selectors 3 and 1, which no script calls.

## Modding notes

- A script opens a screen with `openfullscreenmenu_48d(selector, parameter)`; bit 15 on the selector skips the fade.
- Two posts in one tick keep only the second.
- A request the router refuses during delivery is lost, not retried.
- A selector above 6 with bit 15 set becomes id `8002`<sub>h</sub> and skips the policy-bit-0 test at `002E1AAF`.

## Related

- [Action availability](../Controls-And-Input/action-availability.md) - the policy bits that refuse requests.
- [Controls](../Controls-And-Input/controls.md) - the buttons the arbiter reads.
- [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) - the shop a request 10 opens.
