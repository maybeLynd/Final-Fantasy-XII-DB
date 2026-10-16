---
title: "Menu screens: every menu widget procedure, the screen it belongs to, what installs it and the resources it loads"
kind: "reference"
category: "Menus and HUD"
addresses: "00280DE0, 00281ED0, 0027FB70, 0027F5D0, 00254B50, 00280980, 00244F50, 00245000"
---

## What it lists

`menu-screens.tsv` has one row per widget procedure, 267 in all. They are every procedure the image passes to the
widget constructors `00244F50`, `00245000` and `002465F0` ([Widgets](widgets.md)): 299 construction sites, of which
296 load the procedure with a `lea` and three are the constructors' own calls and the forwarder `00564AC0`. Each
procedure is tied to a screen by walking its installers up to a Party Menu entry or a menu request.

### The Party Menu and its entries

The Party Menu is `00280DE0` ("Party Menu", `menu_command.bin` `554`<sub>h</sub>, the control label at `00915DD0`), built by
`00280D20` for menu request 2 ([Menus](menus.md)). Its entry dispatcher `00281ED0` (`002811DC`) opens each entry by
its `menu_command.bin` id:

| Entry | Opener (site in `00281ED0`) | Screen procedure | Page |
|---|---|---|---|
| Party `4B3`<sub>h</sub> | posts `8001`<sub>h</sub> to its member list | `00280DE0`, list `00285290` | |
| Status `4B4`<sub>h</sub>, Equip `4B6`<sub>h</sub> | `002C2280` (`002822A9`) | `002C2320` | |
| Licenses `4B5`<sub>h</sub> | `005601B0` (`002823C5`) | `00560910` | [License Board screen](license-board-screen.md) |
| World Map `4B7`<sub>h</sub> | `0028E790` (`002823B8`) | `00552250` | [Map screens](map-screens.md) |
| Inventory `4B8`<sub>h</sub> | `00565DD0` (`00282127`) | `00565E00` | [Widgets](widgets.md) |
| Gambits `4B9`<sub>h</sub> | `00568B30` (`00282264`) | `005691E0` | [Gambits screen](gambit-screen.md) |
| Clan Primer `4BC`<sub>h</sub> | `00574CB0` (`0028239B`) | `00574E80` | [Clan Primer](clan-primer.md) |
| Config `4BE`<sub>h</sub> | `00240680` (`0028217D`) | `0023FBE0` | [Config screen](config-screen.md) |
| Graphics Settings `503`<sub>h</sub> | `0023BCC0` (`00282186`) | `0023BD40` | [Config screen](config-screen.md) |
| Controls `504`<sub>h</sub> | `0023CC90` (`0028218F`) | `0023CE10` | [Config screen](config-screen.md) |
| Quit `505`<sub>h</sub> | `0027EBC0` (`00282196`) | `0027EA70` | |
| Parameter Settings `53A`<sub>h</sub> | `00240D60` (`002821B8`) | `00240AD0` | |

Status and Equip share one screen procedure, `002C2320`, which hosts the equipment pane `003FF360`, its list
`003FDFE0` ("Change equipment.", `CC9`<sub>h</sub>) and the slot names Weapon, Off-hand, Helm, Armor and Accessory
(`menu_expansion.bin` `4A99`<sub>h</sub>, `4A9A`<sub>h</sub>, `4A9C`<sub>h</sub>-`4A9E`<sub>h</sub>, `003FEE40`).

### Screens opened by menu requests

The generic request host `0027FB70` (built by `00280A00` for the router `00254B50`, `00254C39`) and its dispatcher
`0027F5D0` open the rest:

| Screen | Procedure | Opened through |
|---|---|---|
| Party Menu | `00280DE0` | `00280D20` (`0027FCAE`) |
| shop: Buy, Sell, Bazaar | `0057B890` | `0057B800` (`0027FCDA`); [Shop screens](shop-screens.md) |
| game over | `003EF830` | `003EF750` (`0027FFC3`) |
| the script menu host | `002D70F0` | `002D7070` (`0027FE8C`) |
| Save, Load (`menu_message.bin` `870`<sub>h</sub>, `871`<sub>h</sub>) | `00582860` | `00583930` (`0027F984`) |
| the notice board list | `0037E350` | `0037FF80` (`0027F9AF`) |
| World Map | `00552250` | `0028E790` (`0027FA2C`) |
| location map | `002BA700` | `0028E660` (`0027F6AF`, `0027F9EC`) |
| Battle Menu (`553`<sub>h</sub>) | `00279E20` | `00276650`, from the HUD frame (`00290DC0`); [Battle menu](battle-menu.md) |
| the special-attack window | `002D5EB0` | `002D5030`, from `0028E970` (`00254C18`) |
| party leader choice, "Select a new party leader." (`86E`<sub>h</sub>) | `0035D6B0` | `0035D080` (`00254C26`) |

### Screens and their procedures

| Screen | Procedures |
|---:|---:|
| Party Menu | 11 |
| Status and Equip | 10 |
| Licenses | 17 |
| World Map | 7 |
| Inventory | 5 |
| Gambits | 5 |
| Clan Primer, with its Hunts and Sky Pirate's Den pages | 19, 5 and 3 |
| Config, Graphics Settings, Controls | 10, 3 and 3 |
| Quit, Parameter Settings | 1 each |
| Battle Menu | 6 |
| Save and Load | 11 |
| shop | 6 |
| location map, map overlay | 7 and 3 |
| party leader choice | 1 |
| game over, special-attack window, notice board list | 5, 4 and 1 |

144 procedures belong to a screen. The other 123 belong to none: the field HUD and its children (root `00253780`),
the party HP and MP list, the help line and target window, the message windows, the shared dialogs, list rows, the
title screen, the logos, the screen mask, the NG signal and the shared backgrounds and captions. Several are shared by
many screens, for example the list item `00292390` (11 owners) and the layout item `0029E7D0`, which the layout decoder
`002432B0` installs for every screen.

### Resources

A procedure's layout comes from `mrppack_ys.bin`: `00280980` relocates its 23 units into `[0209AC30] + 8 x unit`
(`00280980`-`002809DE`), and `002432B0` reads a record of a unit. The table gives layouts as unit and record. Files are
named from the resource path table `01EC73A0`, and images by the label the code passes to `0024A5A0`.

Some screens also load text groups ([Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)).
`002F8040(g)` answers whether group g is resident (`02EC3D80`). The gambit editor's `00292210` adds groups 10 and 16
to its resource batch when they are not (`002491B0`), and `002922F0`, run by the gambit editor (`00569236`), the Inventory (`00566217`), the
shop (`0057BC88`) and `00560910` (`0056098E`), releases each resident group through `002F83E0`: 17 unless `[02CA8F94]` is set, 10, 20 and 14
unless `[02CA96D4]` is set, and 16.

## Columns

| Column | Meaning |
|---|---|
| `procedure` | the widget procedure |
| `size` | the procedure's code size in bytes |
| `installer` | the functions that construct it |
| `install site` | the `lea` of the procedure and the constructor call |
| `parent` | the widget procedures above the installer, `shared: n parents` for more than three, or `none (top)` |
| `screen` | the screen it belongs to, or `no screen` |
| `screen text id` | the shipped text that names that screen |
| `resources` | layout records (`mrppack_ys` unit and record), files and image labels it loads |
| `page` | the final page that documents it, if any |
| `role (from the body or a page)` | what the procedure does |

## Related

- [Menus](menus.md) - the requests and the router.
- [Widgets](widgets.md) - how the procedures are constructed.
- [Widget messages](widget-messages.md) - the messages they answer.
