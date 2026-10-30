---
title: "Menus: how a menu screen is asked for and opened, the one-slot mailbox, the refusals that keep a menu shut, and what a menu hands back"
kind: "system"
category: "Menus and HUD"
addresses: "0x00254B50, 0x0215F1A0, 0x002E1B10, 0x002E1A60, 0x002E0DA0, 0x002E09A0, 0x00280A00, 0x0027FB70"
---

## What the player sees

- Triangle opens the main menu: Party, Status, Licenses, Equip, World Map, Inventory, Gambits, Clan Primer and Config.
- Talking to a save crystal, a shopkeeper or a notice board opens its own screen.
- Menus stay shut during scenes and while another menu is open.
- When every member of the party has fallen, a notice appears, and then the main menu opens to reform the party.

## How it works

### The router

`0x00254B50(request, parameter, flag)` opens a menu (`0x00254B50`-`0x00254C40`):

1. It keeps the low 15 bits as the id (`0x00254B69`).
2. It refuses while the request latch `0x02092734` is 1 (`0x00254B71`).
3. It refuses when the combined action policy has a bit whose word in `0x01E0C2C0` holds the id (`0x00254B80`-`0x00254BC1`);
   that can refuse ids 1, 2, 3, 5, 14 and 21 ([Action availability](../Controls-And-Input/action-availability.md)).
4. It closes what is open (`0x0017E7D0`, `0x0035DA80`, `0x003C8990`) and dispatches through the byte map `0x00254C70`
   (`0x00254BD6`-`0x00254BF9`). The same three calls are `0x00254FC0`, which `0x0026C3E0` runs (`0x0026C4EC`).

### The requests

| Id | Route | Opens |
|---:|---|---|
| `1`, `4` | `0x0035D660`, after its own refusals (`0x0035D66D`, `0x0035D67B`) | the command menu, widget procedure `0x00279E20` |
| `2` | generic; parameter 0 builds `0x00280D20` (`0x0027FC9C`) | the main menu, procedure `0x00280DE0` |
| `3` | `0x0035D980` | choosing the party leader: "Select a new party leader." (`menu_message.bin` `0x86E`) |
| `5` | `0x003C87B0` | the field target cycle |
| `6` | generic, `0x0027F8DB`-`0x0027F984` | the save crystal's save and load menu, `0x00583930` |
| `10` | generic, `0x0057B800(parameter)` (`0x0027FCC2`-`0x0027FCDA`) | a shop; the parameter is the shop |
| `11` | generic, `0x003EF750` (`0x0027FFB5`-`0x0027FFC3`) | game over, procedure `0x003EF830` |
| `12` | `0x0028E970` | the special-attack window, procedure `0x002D5EB0` |
| `15` | generic, `0x0027FA11` | the world map with the title "Airship Route" (`help_menu.bin` `0xC04`) |
| `17` | generic, `0x0027F98E` | the world map with the title "Choose your destination." (`0xC03`) and the confirm "Fly to ...?" (`menu_message.bin` `0x7FF`) |
| `18` | generic, `0x0027F99D` | the world map with no title |
| `19` | generic, `0x0037FF80(parameter)` (`0x0027F9AF`) | the notice board's list |
| `22` | generic | by parameter, below |
| `24` | `0x0035D080` | the notice "All members of the party have fallen. ..." (`0x86F`), then the main menu |

The generic route `0x00280A00` refuses while a menu widget sits at the root's `+0xC0` or `+0xB8` (`0x00280A1A`-`0x00280A30`).
Otherwise it sets the request word and latch through `0x00252B40(id, 1)` and builds the two widgets `0x0027FB70` and
`0x00280140`, which open the screen by id.

### Ids 2 and 22 with a parameter

`0x002E1A60` turns selector 6's parameter 0, 1 and 2 into `0x40`, `0x41` and `0x42` (`0x002E1A7B`-`0x002E1AA1`):

| Parameter | Opens |
|---|---|
| 1-`0x20` | the world map, "Airship Route", with the parameter as the route |
| `0x21`-`0x3F`, and 0 for id 22 | the location map (`0x0027F9E3`-`0x0027F9EC`) |
| `0x40` | the main menu on Gambits, with the help "Change the conditions under which an action is performed..." (`0x002D7070`) |
| `0x41` | the main menu on Licenses |
| `0x42` | the map command tutorial (`0x0027FE7E`, `0x0027F9F3`-`0x0027FA05`) |

### The mailbox

The mailbox at `0x0215F1A0` holds one request:

| Cell | Holds |
|---|---|
| `+0x0` `u8` | pending |
| `+0x1` `u8` | blocked: every post refuses while it is set |
| `+0x4` `u32` | the id |
| `+0x8` `u32` | the parameter |

`0x0215F1AE` and `0x0215F1AF`, next to the mailbox, are two separate flags. The menu close `0x002E1BA0` sets both.
`0x002E0650` clears `0x0215F1AE` and `0x002E0F80` reads it: `openfullscreenmenu_48d` clears it when it starts
(`0x0034631C`) and polls it until a menu closes (`0x00352E04`). `0x002E0660` clears `0x0215F1AF` for
`clear_callpartymenu_status` (`0x00357440`), and `0x002E0F90` reads it for `is_callpartymenu_status` (`0x0033F239`).

`0x002E1B10(id, parameter)` posts; for id 2 it also refuses on policy bit `0x1` (`0x002E1B27`-`0x002E1B33`). A second post before
delivery overwrites the first and still answers 1 (`0x002E1B35`-`0x002E1B47`).

| Poster | Posts |
|---|---|
| the input arbiter | id 2 on Triangle (`0x00253D78`); id 2 on Select and L3 with `0x21`, the location map (`0x00253EE6`, `0x00253F53`), or, once story flag `0x5E` is set, with `0x00264640(2)` (`0x00253F44`) |
| `0x0035C81E` | id 11, game over |
| `0x0035D750` | id 2, after the party-fallen notice |
| `0x002E1A60` | a script selector, below |
| `0x002E1AE0` | id 12 |

The router is also called directly, without the mailbox:

| Caller | Id | Site |
|---|---:|---|
| the input arbiter | `1`, `3` | `0x002541C7`, `0x002540D2` |
| `0x0035BC50`, when a member cannot lead | `3` | `0x0035BF2F`, through `0x00254B40` |
| `0x0035C7B0`, the party-fallen check | `24` | `0x0035C7FF`, through `0x00254B40` |
| the target cycle widget `0x003C8B70` | `1` | `0x003C8F65`, through `0x00254B40` |

`0x00254B40(id)` is `0x00254B50(id, 0, 0)`. The arbiter also runs request 5's route itself (`0x00254044`).

### The script verbs

`0x002E0DA0` turns a script selector into an id, keeping bit `0x8000` (`0x002E0DA6`-`0x002E0E00`):

| Selector | 0 | 1 | 2 | 3 | 4 | 5 | 6 | above 6 |
|---|---|---|---|---|---|---|---|---|
| Id | 17 | 18 | 10 | 15 | 19 | 6 | 22 | 2 |

| Verb | Id | Does | Scripts |
|---|---|---|---|
| `openfullscreenmenu_48d` | `0x48D` | posts a selector and parameter, sets blocked and waits until a menu closes (`0x003462D0`, `0x00352E00`) | 1,274 calls |
| `openfullscreenmenu` | `0x472` | posts the same, without waiting | none |
| `openspattackwindow` | `0x2A8` | posts id 12 | 1 |
| `spattackwindowsync` | `0x2A9` | waits on the special-attack window | 1 |
| `tutorial_sync_partymenu` | `0x3A6` | waits until the next menu closes | none |
| `clear_callpartymenu_status`, `is_callpartymenu_status` | `0x561`, `0x562` | clear and read the flag `0x0215F1AF` | 1 each |

Six more verbs read or set menu state through helpers of their own:

| Verb | Id | Helper | Does |
|---|---|---|---|
| `spattackwindowsync` | `0x2A9` | `0x002E1660` | keeps waiting while `0x0028F7C0` answers 1 or 2; it answers 3 with no special-attack window at `[0x0209BE80] + 0x10FB0`, or when the window's `+0x752` is 1 or bit `0x1` of its `+0x749` is set, and 1 otherwise |
| `open_interventionmenu`, `close_interventionmenu` | `0x455`, `0x456` | `0x0033F860`, `0x002E22F0`, `0x0035D030` | both run the same result handler: `0x0028E940(1)` stores id 1 at `[0x0209BE80] + 0x10F60` and sets bits `0x10` and `0x400` of `+0x10F68`, then sound 4 plays (`0x00249C60`) |
| `get_interventionmenu_status` | `0x457` | `0x002E2340` | 0 without the battle menu (`[0x0209BE80] + 0xAB30`, refused by bit `0x2000` of `+0x10F68`), otherwise 1 with bit `0x10` of `+0x10F68` set and 2 without (`0x0028F6A0`) |
| `get_interventionmenu_commandstatus` | `0x45A` | `0x002E2320`, `0x002E0E30` | the battle menu's current command (`0x002767C0`, through `0x0028F5F0`) plus 1 for 0-7, the same value for 9-17, 18 and 19 swapped, and 0 for any other |
| `setpartymenustatus` | `0x45F` | `0x002E23E0`, `0x002E13C0` | sets or clears one flag of the byte array at `[0x020927C0] + 0x32C4` (`0x00254E00`; flag n is bit `1 << (n & 7)` of byte `n >> 3`): kinds 0-7 give flags 0, 1, 9 and `0x12`-`0x16`, kind 9 flag `0x1E` (Config's Battle Mode row), any other flag `0x1D` (the main menu's Config entry, `0x002CDBF4`) |

`show_escapingwindow` (`0x458`) jumps from `0x002E2310` to the return stub `0x0016D6A0` and does nothing. Flags
`0x1E`-`0x23` of the same array lock Config rows ([Config screen](config-screen.md)). `setmenudisablestatus` (`0x3A5`) sets or clears bit n of
`0x0215F1C4` through `0x002E1BE0`, one of the 16 words `0x002E0FA0` ORs together; `0x002E12E0` passes 0-18 and turns any other value into -1, which is refused.

Selector 5 with bit `0x8000`, the save menu, is called 1,148 times; selector 2, the shops, 98 times with 57 shops;
selector 4, the notice board, 8 times; selector 0 with bit `0x8000`, the destination map, 18 times. Bit `0x8000` makes the screen
open with no fade (`0x0027FF6D`-`0x0027FF77`).

### Delivery

The drain `0x002E09A0` runs once per world tick:

1. While manager slot 0 is not ready, it throws the request away (`0x002E0B8B`-`0x002E0BAA`).
2. A pending id 2 is dropped when `0x0037B330` answers non-zero or policy bit `0x1` or `0x8` is set (`0x002E0BC0`-`0x002E0C65`).
3. While a party record is busy or another request word is held, it waits and keeps the request (`0x002E0C87`-`0x002E0CC2`).
4. It then tests `0x00226BA0` and `0x0053DD10` for ids other than 12, 15, 17, 18 and 19 (`0x002E0CC9`-`0x002E0CF3`), but
   `0x0053DD10` always answers 1, so this never holds a request.
5. It calls the router and clears pending whether or not the router opened anything (`0x002E0CFC`-`0x002E0D10`).
6. It always clears blocked (`0x002E0D3E`).

### While a menu is open

When the router opens a full-screen id, 2, 6, 8-11, 15-19 or 22 (`0x00253BC0`), the drain sets action-policy row 7 to
`0x100203` and the main loop's mode to 4 (`0x002E0D2A`-`0x002E0D39`). Mode 4 captures the screen once and becomes mode 3,
which waits each frame for the menu to close (`0x0022BB62`). Then the loop returns to mode 2, sets the flags `0x0215F1AE` and
`0x0215F1AF` (`0x002E1BA0`) and clears row 7 (`0x0022BB81`-`0x0022BBC5`). While row 7 is set, the router refuses ids 1, 2, 3, 5 and
14.

A script mask close closes the menu's two band widgets too. `0x002E2400(fast)`, the body of `maskclose` and `maskclosefast`
([Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)), and the area unload `0x002E06B0` run
`0x0029D210`, which closes the widget `0x0029CF90` at `[0x0209C380]`, which draws bands at the top and bottom of the frame
(`0x002DC290`), and the side mask `0x0029D340` at `[0x0209C318]`
(`0x00244F00`). For the fast close, argument 1 or `0x11`, they close with the default animation descriptor `0x00915198`,
otherwise with `0x00916330` (`0x00247570`).

### What a menu hands back

| Value | Written by | Read by |
|---|---|---|
| the chosen map node's paired value, singleton `+0x10FAC` | the world map (`0x002901D0`, `0x0029020E`) | the script verb's result, for ids 17 and 18 only (`0x00254710`) |
| the flags `0x0215F1AE`, `0x0215F1AF` | the menu close (`0x002E1BA0`) | `openfullscreenmenu_48d`, `tutorial_sync_partymenu`, `is_callpartymenu_status` |
| the main menu's chosen entry, root `+0xDF8` | `0x00280DE0` (`0x002810FC`) | the Equip compares (`0x00293791`-`0x00295ACB`) |
| the command menu's chosen member, `+0x2FE0` | `0x00278135`, `0x0027A5A1` | 12 reads (`0x00276FC5`-`0x0027A6D8`); three of them resolve it through `0x002732E0` (`0x00276FCB`, `0x002782BC`, `0x002793BA`) |

### Ids nothing posts

No shipped code path or script posts ids 4, 7, 8, 9, 13, 14, 16, 20, 21 and 23. The one exception is a developer verb,
body `0x0050DAB0`, which posts any id its script passes (`0x0050DAC4`); no script calls it. Ids 15 and 18 are reached only by
selectors 3 and 1, which no script calls.

## State

The script menu host `0x002D70F0`, which `0x002D7070` builds for the parameters `0x40` and `0x41` above,
marks itself open in the global below. The Party Menu's picture loader `0x002CEB40` tests it when it opens: while the
host is open it sets bit `0x200000` of row 1 through `0x002E1C20(1, 21)` (`0x002CEDD4`-`0x002CEDE5`), which blocks the pause
menu ([Action availability](../Controls-And-Input/action-availability.md)).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209E66C` | `u32` | 0 | 1 while the script menu host is open | `0x002D70F0`: 1 on message 1 (`0x002D7361`), 0 on message 15 (`0x002D713A`) | `0x002CEB40`, on message 1 (`0x002CEDD4`) |

No other instruction names `0x0209E66C`.

## Modding notes

- A script opens a screen with `openfullscreenmenu_48d(selector, parameter)`; bit `0x8000` on the selector skips the fade.
- Two posts in one tick keep only the second.
- A request the router refuses during delivery is lost, not retried.
- A selector above 6 with bit `0x8000` set becomes id `0x8002` and skips the policy bit `0x1` test at `0x002E1AAF`.

## Related

- [Action availability](../Controls-And-Input/action-availability.md) - the policy bits that refuse requests.
- [Controls](../Controls-And-Input/controls.md) - the buttons the arbiter reads.
- [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) - the shop a request 10 opens.
