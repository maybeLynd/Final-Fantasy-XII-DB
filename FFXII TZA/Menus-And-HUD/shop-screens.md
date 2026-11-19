[Home](../../README.md) / [Menus and HUD](README.md) / Shop screens

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Shop screens: Buy, Sell and Bazaar, the tabs and rows each shows, the price paid, and how a trade reaches the inventory | system | Menus and HUD | Menu screens | How a shop opens from a script, the Buy, Sell and Bazaar command rows and when Sell and Bazaar are greyed, the tabs each mode shows and how empty tabs drop out, how the rows and prices are built (the buy price as listed, half of it on a sale), the refusals, the quantity window, the trade commit and its gil roll, the new bazaar goods notice, and the equip offer and bazaar grant window after a purchase. | 0x0057B800, 0x0057B890, 0x0057BD40, 0x0056DD50, 0x0057CF20, 0x0056D370, 0x0056E700, 0x0057A620 |

## What the player sees

- Talking to a shopkeeper opens the shop's name with three choices: Buy, Sell and Bazaar.
- Sell is greyed with "You possess no saleable items." and Bazaar with "No bazaar goods currently available." when
  there is nothing to show.
- Each choice opens tabs such as WEAPONS, ARMOR and LOOT; a tab with nothing in it is left out.
- Picking a row opens a quantity window, and confirming again makes the trade; the gil total rolls to its new value.
- After buying equipment the shop asks "Equip your purchase now?"; after a bazaar purchase it shows what the good
  gave.

A shop's script opens the screen with only the shop's number. Buy rows come from that shop's current goods list, Sell
rows from the party's inventory and Bazaar rows from the shop's bazaar list; each sale of loot is counted toward the
bazaar.

## How it works

### Opening a shop

A script opens a shop with `openfullscreenmenu_48d(2, shop)`, menu request 10 ([Menus](menus.md)). The request's
screen calls `0x0057B800(shop)`¹, which creates the command list `0x0057B890`. The shop number is the only
argument; the mode is chosen inside the screen. The title is the shop's name, `0x002FAE40(shop)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0027FCDA` |
| ² | `0x0057B98F`-`0x0057B9C1` |

</details>

`0x0057B800` builds the window with the record `{0, shop, 0}`¹. For a shop number of 0 or more
it first calls `0x002C99A0([0x01E0C3B8], [0x01E0C3BC], 1)` and sets bit `0x80` of `+0x38` in the `icons_c` picture entry
that `0x0024A5A0` finds by name²; a negative number skips both³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057B818`-`0x0057B872` |
| ² | `0x0057B82D`-`0x0057B855` |
| ³ | `0x0057B829`-`0x0057B82B` |

</details>

### The window's memory

The shop window takes two blocks:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The window itself, a `0x268`-byte (616-byte) widget that `0x0057B800` builds with procedure `0x0057B890`. It ends with 128 bazaar ids, `u16` at `+0x168`-`+0x267`, indexes 0 to 127. | `0x0057B866`-`0x0057B872` |
| 2 | A `0x7D0`-byte (2,000-byte) block that message 1 takes from arena 2 (`0x002497E0(2, 0x7D0)`, `0x0057B8DC`-`0x0057B906`) and keeps at `+0x160`. It holds 1,000 ids, indexes 0 to 999. Message 18 frees it. | `0x003697F0`, `0x0057BCAC`-`0x0057BCB8` |

`0x002497E0(arena, size)` selects the arena¹, allocates² and restores the arena³.
The tab rows are a third, per-tab block: `0x0057CDD0(n)` takes `n x 0x20` bytes from the same arena and zeroes them.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036C1D0` |
| ² | `0x0036A100` |
| ³ | `0x0036C140` |

</details>

The two id arrays are filled by `0x002FA920`, which writes one id per good and takes no length:

- `0x0057B6F0`, the new-goods check, lists the shop's bazaar goods on offer into `+0x168` (mode 2, `0x0057B721`-`0x0057B736`).
  Mode 2 walks every row of the bazaar table `[0x02EBF058]`¹, 128 in every shipped
  `battle_pack.bin`, so the array is exactly as long as the table.
- `0x0057B500`, which the window sizer `0x0057BEE0` runs for every tab², lists a Buy tab's goods (mode 1,
  category byte `0x00D238F8 + tab`) or the bazaar's (mode 2, `0x00D23901 + tab`) into the block at `+0x160`
 ³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FA9E0`-`0x002FAA1C` |
| ² | `0x0057BF50` |
| ³ | `0x0057B5E9`-`0x0057B617` |

</details>

No other instruction reads or writes the shop window's `+0x160` or `+0x168`. The block pointer at `+0x160` is
stored by message 1¹, passed to `0x002FA920` and copied into the tab row by `0x0057B500`² and freed by message 18³; the ids from `+0x168` are written by `0x002FA920`⁴ and
read back only by `0x0057B6F0`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057B90B` |
| ² | `0x0057B610`, `0x0057B61C` |
| ³ | `0x0057BCAC` |
| ⁴ | `0x002FAA10` |
| ⁵ | `0x0057B740`, `0x0057B74C` |

</details>

### The command rows

`0x0057B400` builds three rows¹, and `0x0057BD40` sets whether each is offered:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057B426`-`0x0057B44E` |

</details>

| Row | Label (`menu_command.bin`) | Help | Help when greyed |
|---|---|---|---|
| `0` | Buy (`0x48B`) | "Purchase goods." (`0xC67`) | never greyed (`0x0057BE1E`) |
| `1` | Sell (`0x48C`) | "Selling loot can make new bazaar goods available for purchase." (`0xC68`) | "You possess no saleable items." (`0xCAB`) |
| `2` | Bazaar (`0x48D`) | "Purchase bazaar goods." (`0xC69`) | "No bazaar goods currently available." (`0xCAC`) |

Sell is offered when any Sell tab has goods and Bazaar when the bazaar list has any, through `0x0056E880`. A greyed row
refuses the choice¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057C070` |

</details>

`0x0057BD40(window)` first sets `+0x150` bit `0x2` when `0x0057B6F0` answers non-zero¹. For each
row it takes the row's node `0x002CD420(i)` and asks `0x0056E880(shop, 0xFF, 0)` for row 1 and
`0x0056E880(shop, 0xB, 1)` for row 2².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057BDC9`-`0x0057BDD2` |
| ² | `0x0057BD6E`-`0x0057BD91`, `0x0057BE10`-`0x0057BE3A` |

</details>

While a row is active it only
sets the styles; with no active row an offered row gets its help text and style 0, a greyed one the greyed text and
style 2, the text going to the node's `+0x18` through `0x002F9860`¹. The style's colour
`0x002DD7E0(style)` goes to the node through `0x002C9F20`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057BE5C`-`0x0057BE80` |
| ² | `0x0057BE84`-`0x0057BE90` |

</details>

### New bazaar goods

Each time `0x0057BD40` runs, `0x0057B6F0` looks at every bazaar good the shop lists ([Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md)).
A good whose flag bit `0x4` is clear gets it set (`0x0030B630(id, 1)`, `0x0057B752`), and any such good makes the screen post
"New bazaar goods are now available!" (`0x805`, `0x0057B4A0`) with sound `0x27`. Only goods with bit `0x4` set are listed
under Bazaar¹, and buying a good clears the bit (`0x0030B630(id, 0)`, `0x0056D4C0`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057DC82` |

</details>

### Modes and tabs

Choosing a row runs `0x0056DD50(shop, key)`¹, which makes the mode's screen. The key, from `0x00D23920`, picks
a tab set through `0x00D233A0`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057C101` |

</details>

| Mode | Key | Tab set | Tabs (`menu_expansion.bin`) |
|---|---|---|---|
| Buy | `0x5AF` | 32 (`0x00D23C70`) | WEAPONS, ARMOR, ACCESSORIES, AMMUNITION, ITEMS, TECHNICKS, MAGICKS, LOOT, GAMBIT TARGETS (`0x4AB8`-`0x4AD1`) |
| Sell | `0x5A2` | 19 (`0x00D23CC0`) | WEAPONS, ARMOR, ACCESSORIES, AMMUNITION, ITEMS, LOOT |
| Bazaar | `0x5AE` | 31 (`0x00D23C60`) | Bazaar (`0x48D`) |

Only the Sell key sets the screen's sell bit¹. `0x00564780` keeps a tab only when
`0x0057D620` reports it has goods, so an empty tab never shows. Before the screen opens, `0x0057BEE0` measures every name
the mode can list and sizes the window to the widest.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056DE3D`-`0x0056DE4E` |

</details>

What `0x0056DD50` does, in order¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056DD50`-`0x0056DEB1` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It builds the screen with `0x00564AC0(0, 0x1C0, key, 0x0056E140)`, keeps the shop at `+0x190` and runs `0x00564780(screen, byte +0x192, 0, shop)`. | `0x0056DD66`-`0x0056DD98` |
| 2 | The child `+0xC8` is `0x00567190(owner, n, +0xE8, screen + 0xF0)`: with `0x00254A10` answering 0 the owner is the shop window's child `0x0057B680(0)` and `n` is 6, otherwise `[[0x0209AC30] + 0x48]` and 9; it is attached to the screen. | `0x0056DD9D`-`0x0056DDF6` |
| 3 | It redraws the tab strip and stores at `+0x191` the help kind `0x0056DC30` of the byte `+0xF7`, or of 1 when `+0x180` has no bit of `0x1F0000`. | `0x005674B0`, `0x0056DE1A`<br>`0x0056DE1F`-`0x0056DE43` |
| 4 | The sell bit is `+0x194` bit `0x1`: set for keys `0x597`-`0x59D` and `0x59F`-`0x5A2` and cleared for any other, so of the three keys only `0x5A2` sets it. | `0x0056DE3D`-`0x0056DE65` |
| 5 | It runs `0x0056C950(screen, +0x191, sell bit)`, `0x0056E410(screen)`, `0x0056E5D0(screen, 1)`, `0x002CF890` and `0x002C9490([0x01E0C3DC], [0x01E0C3BC], [0x01E0C3E8])`, and returns the screen. | `0x0056DE6B`-`0x0056DEB1` |

### Rows

`0x005655F0` builds a tab's rows through `0x0057CF20`¹, one 0x20-byte row per good. It gives the shop
number in the high 16 bits and the pane's kind, byte `+0x17F`, in the low 16 bits; on the Buy and Sell screens,
kinds 32 and 19, the kind becomes the tab's category from `0x0057D5E0`, and any other kind goes as it is²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005656A2` |
| ² | `0x00565666`-`0x005656A2` |

</details>

- Buy rows come from the shop's current list, by category (`0x002FAD30`, `0x002FA920` mode 1, `0x0057CFC4`, `0x0057D022`), as
  [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) describes.
- Sell rows come from the party's inventory lists through `0x00D23D00`¹: lists 1 to 4 for
  WEAPONS, ARMOR, ACCESSORIES and AMMUNITION (categories 8 to 11), list 0 for ITEMS (12) and list 11 for LOOT (15).
- The Inventory's rows come through `0x00D23960`², except Abilities, kind 5, which reads
  lists 9 and 8³, and the equipment screen's through `0x00D23988`⁴.
- Bazaar rows come from the shop's bazaar list (`0x002FA920` mode 2, `0x0057D07B`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057D0BA`-`0x0057D0DC` |
| ² | `0x0057D0E9`-`0x0057D103` |
| ³ | `0x0057D26A`-`0x0057D3D9` |
| ⁴ | `0x0057D0A2`-`0x0057D0AD` |

</details>

Each row holds the name, the id, the sellable count, the count owned and the price, filled by `0x0057DED0` (equipment),
`0x0057DAD0` (items, loot and key items), `0x0057DD60` (magicks, technicks and gambits) or `0x0057DC30` (bazaar goods).

`0x0057DAD0(rows, ids, n, class, range, flags)` skips `0xFFFF`¹, looks up each id it keeps
with `0x0035D380(class, id)`² and returns how many ids it keeps³. `0x0057CF20`
gives it class 5, items, for kinds 4, 12 and 24⁴; class 7, loot, for kinds 6, 15 and 27⁵; and class 13, key items, only for kind 7, the
Inventory's Key Items, with the id range of the tab's category⁶. On the shop screens it
fills the ITEMS and LOOT tabs of Buy (24 and 27) and of Sell (12 and 15), and no shop tab lists key items.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057DB41`-`0x0057DB44` |
| ² | `0x0057DB50` |
| ³ | `0x0057DBEC`, `0x0057DC1A` |
| ⁴ | `0x0057D352` |
| ⁵ | `0x0057D411` |
| ⁶ | `0x0057D41B`-`0x0057D48D` |

</details>

`0x0057D620` makes the same three calls with no rows¹, and with no rows
`0x0057DAD0` stores nothing and only counts².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057D908`, `0x0057D9B3`, `0x0057DA2B` |
| ² | `0x0057DB5C`-`0x0057DB5F` |

</details>

A row of `0x0057DAD0` holds the fields below and leaves `+0x14` to `+0x1F` unwritten¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057DB65`-`0x0057DBE0` |

</details>

- `+0x00` the name, `0x002B58B0` of record `+0x18`; `+0x08` the id, record `+6`; `+0x0A` the icon, record `+0x2C`,
  which is the table row's byte `+4` for all three classes¹;
- `+0x10` the price, record `+0x28`: the table row's word `+0xA` for items², word `+0` for loot
 ³ and -1 for key items⁴; its bit `0x80000000` is cleared first⁵;
- flags bit `0x2` stores the price in the low 31 bits of `+0x10`⁶; otherwise bit `0x4`
  stores half of it, shifted right by one⁷, and with bit `0x20` sets bit `0x80000000` when
  that half is 0⁸; with neither bit the dword keeps the 0 of the zeroed rows
 ⁹;
- `+0x0C` the sellable count, record `+0x20` (inventory channel 0), only when flags bit `0x8` is set, and `0xFFFF`
  otherwise¹⁰, and no caller sets bit `0x8`; `+0x0E` the count owned, record `+0x24`
  (inventory channel 1, `0x0057DB9B`-`0x0057DBA2`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031C83E`, `0x0031CBFA`, `0x0031D26B` |
| ² | `0x0031C81A` |
| ³ | `0x0031CBE0` |
| ⁴ | `0x0031D63E` |
| ⁵ | `0x0057DB91`-`0x0057DB9F` |
| ⁶ | `0x0057DBA6`-`0x0057DBB7` |
| ⁷ | `0x0057DBB9`-`0x0057DBCC` |
| ⁸ | `0x0057DBCF`-`0x0057DBE0` |
| ⁹ | `0x0057D118`-`0x0057D134` |
| ¹⁰ | `0x0057DB67`-`0x0057DB76` |

</details>

`0x0057CF20` sets the flags from the kind, so `0x0057DAD0` gets 2 on Buy, 4 for Sell ITEMS, `0x24` for Sell LOOT and 0
in the Inventory:

- 0 for the Inventory's kinds 0 to 7¹;
- 2 for the Buy categories 20 to 27 and 29² and for the Bazaar's kind 31³;
- 4 for the other kinds 8 to 63, the Sell categories among them⁴, with bit `0x20` added for Sell LOOT,
  kind 15⁵;
- `0x10` for the equipment screen's kinds `0x40` to `0x44`, which `0x003FD360` sets as the slot plus `0x40`
 ⁶, at `0x0057CFAE` for kind `0x41` and `0x0057D0B2` for the others;
- bit `0x1` on top, for `0x0057DED0` only: on the AMMUNITION tabs, kinds 11 and 23⁷, and for the second list of kind `0x41`, list 4⁸.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057CF74` |
| ² | `0x0057D02B` |
| ³ | `0x0057D080` |
| ⁴ | `0x0057D0E1` |
| ⁵ | `0x0057D3E7`-`0x0057D3F0` |
| ⁶ | `0x003FD36E`-`0x003FD371` |
| ⁷ | `0x0057D168`-`0x0057D175`, `0x0057D1A1` |
| ⁸ | `0x0057D233` |

</details>

### Prices

| Trade | Price per unit |
|---|---|
| Buy | the good's listed price, query record `+0x28` (`0x0057DBAC`) |
| Sell | half the listed price, rounded down (`sar` at `0x0057DBC2`, `0x0057DFDE`) |

Equipment marked unsellable (record `+0x54`, `0x0057DFBF`) and loot whose half price is 0¹ cannot
be sold. The shop screen applies no other change to a price: the four row fillers and the trade commit use the
listed value, and every write of `+0x28` in the query filler `0x0031C5D0` (14 of them) is a table load, -1 or 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057DBCF`-`0x0057DBDC` |

</details>

### Refusals

`0x0056E700` refuses a choice when:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | buying, the party already owns the most it can hold of the good, so a magick, technick or gambit already owned cannot be bought again; | `0x0056E78F` |
| 2 | buying, one costs more gil than the party has; |   |
| 3 | selling, the good cannot be sold; | `0x0056E71A` |
| 4 | selling, none of the good can be sold. |   |

The most the party can hold is 99 for weapons, armour, accessories, ammunition, items and loot, and 1 for
technicks, magicks and gambits¹. The bazaar goods' entry, 255 (`0xFF`), is not a count: the buy
test skips its owned-count refusal for that value (below). A bazaar good is a bundle that gives its items when
bought ([Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md)), and its quantity stays 1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00D235F8` |

</details>

`0x0056E700(row, state, most)` answers a mask of refusal bits. The list passes its `+0xD8` as the state: byte `+0x00`
bit `0x1` for selling, the quantity `+0x04`, the most the party can hold `+0x06` from `0x00D235F8` and the gil `+0x08`
from `0x00253690`¹. It first stores 0 in `*most` when `most` is given².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056D509`-`0x0056D556` |
| ² | `0x0056E70D`-`0x0056E712` |

</details>

- Selling: bit `0x8` when the price `+0x10` has bit `0x80000000`¹; bit `0x2` when the
  sellable count `+0x0C` is 0, a count of -1 standing for the count owned `+0x0E`². With
  state bit `0x2` it adds bit `0x1` when the count is at most the quantity, and stores the count in `*most`
 ³.
- Buying: bit `0x1` when the count owned is at least the most, a most of `0xFF` skipping this test, so a bazaar good
  is never refused for the count owned⁴; bit `0x4` when the price without bit `0x80000000`
  is above the gil⁵.
- Buying with state bit `0x2`: bit `0x1` when the count owned plus the quantity reaches the most, and bit `0x4` when
  the quantity's price is above the gil. `*most` becomes the largest count the gil pays for, held to the most less
  the count owned, and bit `0x1` is set when the quantity is not below it⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056E71A`-`0x0056E72B` |
| ² | `0x0056E726`-`0x0056E746` |
| ³ | `0x0056E748`-`0x0056E767` |
| ⁴ | `0x0056E770`-`0x0056E794` |
| ⁵ | `0x0056E797`-`0x0056E7AB` |
| ⁶ | `0x0056E7AE`-`0x0056E820` |

</details>

### The quantity window

The first confirm on a row opens the quantity window at 1¹. Weapons, armour,
accessories, ammunition, items and loot take a number; every other kind stays at 1². In the window³:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056D509`-`0x0056D598`, `0x0056C490` |
| ² | `0x00D235E8` |
| ³ | `0x0056CA60` |

</details>

- left and right pick the ones or tens digit;
- up adds to that digit, up to the smaller of what the party can still hold and what the gil pays for;
- down takes away, down to 1;
- with the modifier held, up and down jump to the limit or to 1.

The help line shows "Press ... to buy goods in quantity." (`0xC6C`) or "... to sell goods in quantity." (`0xC6E`)
while a number is being entered¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056C783` |

</details>

### The trade

The second confirm makes the trade at once; there is no yes-or-no box¹. The total is the row's
price times the quantity:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056D450`-`0x0056D504` |

</details>

| Trade | Call | What it changes |
|---|---|---|
| Sell | `0x00310870(id, quantity, total, 0)` (`0x0056D478`) | removes the goods, adds the gil, and counts the sale toward the bazaar (`0x0030B270`) |
| Buy | `0x002FEEB0(id, quantity, total, 0)` (`0x0056D49A`) | adds the goods, takes the gil, and marks the good as bought (`0x0030B180`) |

Each of the two has this one caller. The inventory side is in [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md).
A sale of loot also counts `0x00316A50(0xE, quantity)`, and every purchase counts `0x00316A50(0x13, id)`. Then
`0x002A1DC0` starts the gil total rolling¹, and when it stops the screen goes on to the step below².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056D4D9` |
| ² | `0x0056D5C7` |

</details>

### After the trade

| Trade | Next |
|---|---|
| a bazaar good | the grant window `0x0057A4E0` lists the items the good gave (`0x0057A300`, `0x0057A480`) |
| equipment bought | the equip offer `0x0057A620` (`0x0057A980`); a sale of equipment rebuilds the list |
| anything else | the list is rebuilt with the cursor kept on its row (`0x0056E410`) |

The grant window's list `0x003F4840` (from `shop_new.mrp`, kept at `0x02B5F1F8`) draws its rows through the child
`0x003F4330`, which installs the row painter `0x003F41C0`¹. For row i it reads an item id at `+0xCC + 8i`
and an amount at `+0xD0 + 8i`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003F45AB` |

</details>

- for an id it shows the item's icon (record `+0x2C`, through `0x002FABD0`, `0x003933B0` and `0x0035D380`), its name
 ¹ and the amount²;
- for -1 it shows text `0x7D3` with the amount, formatted into `+0xE4`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002B58B0` |
| ² | `0x0029FF60` |
| ³ | `0x002B4090` |

</details>

### Row painters and the list state

`0x0056D370` installs four row painters¹, each with its own label layout: `0x0056CBC0`²,
`0x0056CD50`³, `0x0056D1B0`⁴ and `0x0056CF10`, which also paints the quantity column⁵. A
painter greys a row (`0x00392FC0`, or `0x00393240` on four labels in `0x0056CF10`):

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056D66E`-`0x0056D6AC` |
| ² | `0x00D23568` |
| ³ | `0x00D23550` |
| ⁴ | `0x00D23538` |
| ⁵ | `0x00D23520` |

</details>

- buying, when its price `+0x10` (low 31 bits) is above the gil¹; in `0x0056CD50` and `0x0056D1B0` also when the
  party already holds one (`+0x0E`), and in `0x0056CF10` when it holds 99;
- selling, when the price word's bit `0x80000000` marks it unsaleable or its sellable count `+0x0C` is 0;
- with the quantity window open, every row but the cursor's.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00253690` |

</details>

`0x0056D870(row, widgets, layout)` paints the common part: the icon frame `+0x0A` (no icon for `-1`), the name and the
price. `0x0056DA80` paints the quantity window's row: the quantity and, when bit `0x4` is set, the price times the
quantity¹. `0x0056D9D0(list, quantity)` stores the quantity at `+0xDC`, sets `+0xE4` bit `0x4` when
`0x0056E700` accepts it (answers 0) and bit `0x8` when it is not 1, and passes both to the list.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0029FF60` |

</details>

### Tabs and the help line

- `0x0057D600(buy)` gives the tab count, 9 when buying and 6 otherwise; `0x0057D5E0(buy, i)` the category of tab `i`,
  from `0x00D23D60` (buy: 20 to 27 and 29) or `0x00D23D6C` (otherwise: 8 to 12 and 15); `0x0057D610` is `0x0057D620` with 0.
- Categories 20, 21 and 22 are the three key-item tables. The row builders `0x0057CF20`¹ and
  `0x0057D620`² pass `0x0057DAD0` an end and a start, and it keeps an id only when
  start <= id < end³: category 20 takes `0x8060`-`0x81FF`, 21 takes `0x8000`-`0x803F` and
  22 takes `0x8040`-`0x805F` ([Key item list](../Items-Equipment-Shops-And-Licenses/key-item-list.md)).
- The category is word `+6` of the tab's entry in the pane's tab list: for `0x0057CF20` from `0x005655F0` and
  `0x00565720`⁴, and for `0x0057D610` from `0x00564780` and `0x003FD360`⁵. `0x0056E880` and `0x0056E9A0` give `0x0057D610` the categories 0, 17, 18 or 24⁶.
- Of the tab lists at `0x01F2CB90` for kinds 0 to 37, only kind 7's, `0x00D23B58`, the Inventory's Key Items, holds a
  key-item category: one tab, id 23, category 20. No list holds 21 or 22. So the Inventory's Key Items lists only
  `0x8060`-`0x81FF`, and the ranges of categories 21 and 22 are used by no tab list.
- `0x0057CE10(category)` returns the category's row table, one of 17 between `0x00D239A0` and `0x00D23A50`; `0x0057CDD0(n)`
  allocates `n` zeroed 0x20-byte rows from arena 2 (`0x002497E0(2, n x 0x20)`, `0x0057CDDC`-`0x0057CDF6`).
- `0x0056DED0(screen)` is the screen's step: the quantity window's input while it is open⁷; otherwise the
  tab switch of the [Inventory screen](inventory-screen.md)⁸, which redraws the tab strip
 ⁹, takes the help kind `0x0056DC30(category)` into `+0x191`, rebuilds the list¹⁰
  and plays sound 10.
- `0x0056DC30` maps categories to help kinds: 0 to `0xB`; 1-4 to 0; 5-8 to 1; 9 to 2; 10 and 27-30 to 3; 11 to 4; 12 and
  31 to 8; 13 to 9; 14 to 10; 15 to 5; 16-21 to 6; 26 to 7; any other to `0xFF`.
- `0x0056E5D0(screen, x)` writes the help line when the mode has goods¹¹: `0xC6B`, or `0xC6D` when selling,
  and the row's description through `0x00293100(0x00D235D8[kind], id << 16)`; for kinds other than 11 it also shows the
  member panel for the id (`0x002CC4F0`, `0x002CC2A0`; [Menu screens](menu-screens.md)). `0x0056E840(kind)` and
  `0x0056E860(kind)` read the bytes at `0x00D235D8` (kinds to 11) and `0x00D235C8` (to 10).
- `0x0057B660(mode)` gives 9 for Buy, 6 for Sell and 1 for Bazaar.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057D420`-`0x0057D45E` |
| ² | `0x0057D9C2`-`0x0057D9FD` |
| ³ | `0x0057DB2C`-`0x0057DB3B` |
| ⁴ | `0x0056568E`, `0x0056577B` |
| ⁵ | `0x00564851`, `0x00564928`, `0x003FD442` |
| ⁶ | `0x0056E8F9`-`0x0056E90E`, `0x0056E9D0`-`0x0056E9F4` |
| ⁷ | `0x0056CA60` |
| ⁸ | `0x00563EC0`, `0x00564300` |
| ⁹ | `0x005674B0` |
| ¹⁰ | `0x0056C950`, `0x0056E410` |
| ¹¹ | `0x0056E880` |

</details>

### Closing the window

- `0x0056C850(list)` closes the quantity window and rebuilds the list¹; with no rows left it

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056E410`, `0x0056C490` |

</details>
clears the help and closes the screen (`+0x194` bit `0x4`, `0x00244F00`). Otherwise it re-attaches the screen when its
state nibble (`+0x7C` mask `0xF`) is 1, and redraws the help¹ when `0x0056E410` moved the cursor off a row
that has gone.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056E5D0` |

</details>
- `0x0056E580(screen, v)` returns from the equip offer¹: it sets `+0x194` bit `0x2` when
  `v` is 0, re-attaches the screen and runs `0x0056C850`.
- `0x0056DD00(screen)` answers whether the screen may close: not while the shop window `[0x02CA9790]` and the part
  `[0x02CA97A0]` exist², always once `+0x194` bit `0x4` is set, and otherwise unless `0x0057A440` reports state 2
  of `0x003F4670`.
- `[0x02CA9790]` is the shop window itself: its message 1 stores it³ and message 18 clears it
 ⁴. `0x0057B680(i)` returns the shop window's child `+0x158` for `i` below 1, and `0x0057B6A0`, a callback of
  the grant window⁵, closes the shop's parts: the list⁶, the panel `[0x02CA9798]`, the help
  lines⁷ and the shop window⁸, returning `0xC`.
- `0x0057C010` is the grant window's other callback; `0x0057A4E0` installs it beside `0x0057B6A0`⁹. It passes the
  name id of the shop byte `+0xC0` of `[0x02CA9790]`¹⁰ through `0x003EABE0` to `0x002CA150(…, 0)`, runs
  `0x002CE7A0(1)` and `0x0056E580([0x02CA9798], 0)`, re-attaches `[0x02CA9790]`¹¹ and returns `0xC`.
- `0x0057CD00(table, id)` returns the index of `id` among the 16-byte entries at `+0x5B8` (count `+0x636`), or 0, for
  the sort strip¹².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057ADCD`, `0x0057AFFA`, `0x0057C04B` |
| ² | `0x0057A960` |
| ³ | `0x0057B8CE` |
| ⁴ | `0x0057BCC2` |
| ⁵ | `0x0057A5C0` |
| ⁶ | `0x002CA110` |
| ⁷ | `0x00291D80`, `0x00293110` |
| ⁸ | `0x0057B6D1`-`0x0057B6DF` |
| ⁹ | `0x0057A5CC` |
| ¹⁰ | `0x002FAE40` |
| ¹¹ | `0x00246AD0` |
| ¹² | `0x005669A5` |

</details>

The equip offer checks each party member¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00317B70` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | When someone can equip it, it asks "Equip your purchase now?" (`0x803`). |   |
| 2 | When the item's class is one of the eight in `0x00D23910`, the ranged weapons and their ammunition, it says instead that the item cannot be equipped at a shop and to use the Equip command in the Party Menu (`0xCF8`, `0x0057AB32`). |   |
| 3 | Yes opens the member picker `0x0057AC10`, "Select a character to equip." (`0xC70`), which calls `0x0031A510` for the member under the cursor at a confirm, only when its countdown byte `+0xC7` is 0, that member can equip the item, a bought copy is left and the member's slot does not already hold it, so at most once per copy bought; a refused confirm plays sound 5. | `0x0057AF18`<br>`0x0057ADE8`-`0x0057AE06`<br>`0x0057AF9B` |

`0x0031A510`, once the seat is accepted¹ and, for an id other than `0xFFFF`, the eligibility test
passes², moves one worn copy from the old piece to the new with `0x0030F9A0` and `0x0030C410`³ before it stores the id (`0x0031A5C8`;
[Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md)); otherwise it returns -1 with no move.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A53C`-`0x0031A55F` |
| ² | `0x0031A59C`-`0x0031A5A3` |
| ³ | `0x0031A5A5`-`0x0031A5BF` |

</details>

After the store, `0x00318B40(…, slot, 1)`¹ can take the other hand's piece off and move its
worn copy too². The picker itself calls none of `0x003008A0`, `0x0030F9A0` and `0x0030C410` directly.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A5C4`-`0x0031A5D5` |
| ² | `0x00318C4A`-`0x00318C79` |

</details>

`0x00D23910` is `u8[8]`, equipment classes: the equipment row's byte `+0x09`, which the class-6 query `0x0035D380(6, id)`
copies to `+0x38` (`0x0031C9BD`-`0x0031C9C1`; [Equipment row](../Items-Equipment-Shops-And-Licenses/equipment-row.md)).
Once a member can equip the item, `0x0057A8B6`-`0x0057A8D3` compares its class with the eight bytes (`edx < 8`), and a
match sets `+0xCC` bit `0x2` and the message above¹. The class names are the game's category table
names ([Equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md)):

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057A8D9` |

</details>

| Class | Name | Named rows | First and last |
|---|---|---|---|
| `0x07` | Bow (2H) | 16 | Shortbow `0x1042`, Dhanusha `0x10C7` |
| `0x08` | Crossbow (2H) | 8 | Bowgun `0x1050`, Tula `0x10B0` |
| `0x09` | Gun (2H) | 12 | Altair `0x1057`, Mithuna `0x10C5` |
| `0x11` | Hand-bomb (2H) | 6 | Hornito `0x109A`, Makara `0x10C3` |
| `0x17` | Arrows | 8 | Onion Arrows `0x1184`, Artemis Arrows `0x118B` |
| `0x18` | Bolts | 8 | Onion Bolts `0x118C`, Grand Bolts `0x1193` |
| `0x19` | Shot | 8 | Onion Shot `0x1194`, Stone Shot `0x119B` |
| `0x1A` | Incendiaries | 8 | Onion Bombs `0x119C`, Castellanos `0x11A3` |

The three bytes after the table, `0x00D23918`, are a separate list that `0x0057B1A0` reads with its own bound of 3¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057B2B4`-`0x0057B2D9` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

### The grant list

The grant list is the `0x130`-byte widget with procedure `0x003F4840` that `0x003F47E0` and `0x003F4DD0` build
and that keeps itself at `0x02B5F1F8`; the grant window `0x0057A4E0` and the quest result window use it.

`GrantList` (`0x130` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x003F4840` |
| `+0x0C0` | `u8` | page | the page on show: 0 no page (the construct message, `0x003F48E1`), 1 the item list (`0x003F47BB`), 2 the second list (`0x003F4747`). `0x003F4690` opens the next page from it (`0x003F46A8`): from 0 the item list when the copied reward record has its gil bit or item pairs, else the second list when it has single items; from 1 the second list when there are single items; otherwise it answers 0 and message 12 (sub-command `0x12`, the page is done) closes the window. Message 12 drops the finished page's child by it (`0x003F49AE`). `0x003F4670` returns it, or 3 when no window exists (`0x003F4682`); the grant window `0x0057A4E0` and `0x0057A440` wait on that, and so does the quest result window `0x003F4E70` for 3 (`0x003F4F56`) |
| `+0x0C1` | `u8[7]` | pad0C1 | read and written by no function; nothing fixes its width |
| `+0x0C8` | `u64` | owner | the creator's first argument, the first qword of the creation record (`0x003F487F`; `0x0057A4E0` passes its rsi); handed to the item list child `0x003F4330` as the first word of its creation record (`0x003F4750`) |
| `+0x0D0` | `u8[16]` | reward00 | bytes `0x00`-`0x0F` of the `0x24`-byte reward record the creator points to (`0x003F488D`): byte `+0x00` bit `0x1` marks gil, word `+0x08` the number of item pairs and word `+0x0A` the number of single items, which `0x003F4690` tests to choose the pages (`0x003F46D4`, `0x003F46D9`, `0x003F46E3`); both children get this copy's address (`0x003F46F7`, `0x003F4768`) |
| `+0x0E0` | `u8[16]` | reward10 | bytes `0x10`-`0x1F` of the copied reward record (`0x003F4898`), read by the two children through the copy's address |
| `+0x0F0` | `u8[4]` | reward20 | bytes `0x20`-`0x23` of the copied reward record (`0x003F48A2`), read by the two children through the copy's address |
| `+0x0F4` | `u8[4]` | pad0F4 | read and written by no function; nothing fixes its width |
| `+0x0F8` | `u8[16]` | callbacks00 | bytes `0x00`-`0x0F` of the `0x18`-byte block the creator's third argument points to, or zero when it is null (`0x003F48B4`, `0x003F48CA`, `0x003F48D1`); the grant window `0x0057A4E0` fills it with a byte at `+0x04`, -1 at `+0x06` and the function `0x0057B6A0` at `+0x08`. Both children get its address (`0x003F470D`, `0x003F476D`) |
| `+0x108` | `void*` | callbacks10 | bytes `0x10`-`0x17` of that block (`0x003F48C0`, `0x003F48D8`): the second function, `0x0057C010` from the grant window `0x0057A4E0` |
| `+0x110` | `void*` | itemList | the item list page, `0x128` bytes with procedure `0x003F4330` (`0x00244F50` at `0x003F47A4`, stored at `0x003F47AC`, opened at `0x003F47B6`); 0 on construction (`0x003F48E8`) and when message 12 finishes page 1 (`0x003F49CC`) |
| `+0x118` | `void*` | secondList | the second page, `0xF0` bytes with procedure `0x003F4060`, for the record's single items (`0x00244F50` at `0x003F4730`, stored at `0x003F4738`); 0 on construction (`0x003F48EF`) and when message 12 finishes page 2 (`0x003F49C1`) |
| `+0x120` | `u32` | ownsPicture | bit `0x1` set when the window loaded its own picture, kind 7 id `0x96` (`0x003F4941`), clear when the caller gave one (`0x003F48FF`); the construct message opens the window at once only without it (`0x003F497A`); the closing message 15 frees the picture only with it (`0x003F49F4`) |
| `+0x124` | `u8[4]` | pad124 | read and written by no function; nothing fixes its width |
| `+0x128` | `void*` | picture | the picture the item list draws with: the caller's (the creator's fourth argument, from `0x0057A4E0`'s [r9 + `0x158`], `0x003F4906`) or the load request kind 7 id `0x96` (`0x00249320`, `0x003F4935`); handed to the item list (`0x003F477E`); freed and cleared by the closing message 15 when owned (`0x003F49FD`-`0x003F4A17`) |

### The shop window

The shop window is the `0x268`-byte widget with procedure `0x0057B890` that `0x0057B800` builds (The window's memory above).

`ShopWindow` (`0x268` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0057B890` |
| `+0x0C0` | `u8` | shop | the shop number, the construct message's argument a (`0x0057B8BD`-`0x0057B8C3`): the title is the shop's name `0x002FAE40`(shop) on opening (message 16, `0x0057B977`) and on return from a trade (`0x0057C01B`); the tab lists `0x0057B500` (`0x0057B5E9`, `0x0057B609`) and the new-goods check `0x0057B6F0` (`0x0057B70A`, `0x0057B71A`) list its goods; `0x0057BD40` asks `0x0056E880` whether rows 1 and 2 are offered for it (`0x0057BE23`); choosing a row opens the trade screen `0x0056DD50`(shop, text) (`0x0057C0F0`); the grant window `0x0057A4E0` reads it (`0x0057A573`) |
| `+0x0C1` | `u8` | savedMenuByte | byte `+0xDE0` of the menu layout block [`0x0209AC30`] when the shop opens (`0x0057B92F`-`0x0057B936`); the construct message then calls `0x00285F20`(0), and message 18 restores the saved value with `0x00285F20` (`0x0057BCA0`) |
| `+0x0C2` | `u8[2]` | pad0C2 | read and written by no function; nothing fixes its width |
| `+0x0C4` | `u8` | activeRow | the command row whose trade screen is open: `0x0057C070` stores the confirmed row (`0x0057C0AA`); `0xFF` for no row (the construct message `0x0057B8F1`, message 8 `0x0057BA83`). While a row is active `0x0057BD40` draws it in style 0 and the other rows in style 3 (`0x0057BE3C`-`0x0057BE57`); message 8 runs `0x002CB8B0` unless it is row 2 (`0x0057BA72`) |
| `+0x0C5` | `u8[3]` | pad0C5 | read and written by no function; nothing fixes its width |
| `+0x0C8` | `i16` | listCursor | the head of the command rows' list state: `0x002CD4D0` sets it to 0, points `+0xD0` at the rows and registers the state at [`0x0209AC30`] + `0x330` (`0x002CD4E5`, called by `0x0057B400` at `0x0057B421`); the command list builder `0x002C9BF0` takes it as the list's row (`0x002C9C79`) |
| `+0x0CA` | `u8[6]` | pad0CA | read and written by no function; nothing fixes its width |
| `+0x0D0` | `void*` | rowsPointer | the address of the three command rows at `+0xD8`, stored by `0x002CD4D0` (`0x002CD4EB`); read for a row's help text (`0x0057B983`, `0x0057BAC9`, `0x0057BB51`) |
| `+0x0D8` | `u8[96]` | rows | the three `0x20`-byte command rows (The command rows above): `0x002CD4D0` clears them (memset `0x60`, `0x002CD4F1`); `0x0057B400` labels them `0x48B`-`0x48D` with help `0xC67`-`0xC69` (`0x002CD3C0`, `0x0057B426`-`0x0057B44E`); `0x0057BD40` puts a row's help text at its `+0x18` (`0x0057BE80`); the cursor message `0x8000` and message 8 show that help (`0x00291D80`, `0x0057BB5C`, `0x0057BAD6`) |
| `+0x138` | `u32[3]` | offered | per command row, whether it is offered: `0x0057BD40` stores 1 for row 0 and `0x0056E880`(shop, ...) for rows 1 and 2 (`0x0057BE1E`-`0x0057BE3A`); `0x0057C070` refuses a confirmed row whose entry is 0 (`0x0057C087`). The construct message clears the three (`0x0057B8E1`, `0x0057B8E8`) |
| `+0x144` | `u8[4]` | pad144 | read and written by no function; nothing fixes its width |
| `+0x148` | `void*` | commandList | the command list widget, built by `0x002C9BF0` from the rows (`0x0057B47B`, stored at `0x0057B483`), 0 at construction (`0x0057B8D5`); message 10 hands it the input (`0x002D3900`, `0x0057BB00`); its `+0xE0` gets bit `0x20000` when a row is chosen (`0x0057C0A3`-`0x0057C0B1`) and loses it on message 8 (`0x0057BAE0`), and gets bit `0x200000` on sub-command `0x12` (`0x0057BB76`) and loses it on `0xF` (`0x0057BBA9`); message 8 reads its cursor to show the row's help (`0x0057BA8F`) |
| `+0x150` | `u32` | flags | bit `0x1`: picture `0x16` was loaded here (`0x0057B7E7`) and message 18 releases it (`0x002F83E0`(`0x16`), `0x0057BC8D`); bit `0x2`: the bazaar has new goods, set by `0x0057BD40` when `0x0057B6F0` finds some (`0x0057BDD2`), which makes message 19 and sub-command `0x12` show them (`0x0057B4A0`, `0x0057BA14`) and is cleared by the answers `0x8100`-`0x8102` (`0x0057BBF9`); bit `0x4`: the window is closing for a trade, set by `0x0057B6A0` (`0x0057B6D8`) and taken by message 19 (`0x0057B9F1`-`0x0057B9FE`); bit `0x8`: set by message 15 (closing begins, `0x0057BC18`), cleared by message 14 (`0x0057B9E2`); bit `0x10`: set by message 20 unless bit `0x4` is set (`0x0057BC52`-`0x0057BC5F`), after which each tick waits for `0x00283980` and destroys the window (`0x0057BA31`-`0x0057BA53`); bit `0x20`: sub-command `0xF`'s argument (`0x0057BB8C`-`0x0057BB9E`), cleared by message 8 (`0x0057BAF1`); message 8 does its work only with bit `0x20` set or bit `0x8` clear (`0x0057BA60`-`0x0057BA6C`). The construct message sets it to 0 (`0x0057B900`) |
| `+0x154` | `u8[4]` | pad154 | read and written by no function; nothing fixes its width |
| `+0x158` | `void*` | picture | the shop's one picture, kind 7 id `0x96` (the list `0x00D238E0`, one entry): `0x0057B780` has `0x003933F0` load it here (`0x0057B792`, `0x00393431`); `0x0057B680` returns it for index 0 (`0x0057B697`); the grant window `0x0057A4E0` (`0x0057A5DD`), the equip offer `0x0057A980` (`0x0057A9B6`) and `0x0057C070` (`0x0057C0D1`) use it; message 18 releases it through `0x003938B0` (`0x0057BC6D`, `0x003938D0`, `0x003938DD`) |
| `+0x160` | `void*` | goodsBlock | the `0x7D0`-byte block of 1,000 good ids taken from arena 2 by the construct message (`0x002497E0`, `0x0057B90B`); `0x0057B500` has `0x002FA920` fill it for each tab and copies it into the tab row (`0x0057B610`, `0x0057B61C`); message 18 frees it (`0x003697F0`, `0x0057BCAC`) |
| `+0x168` | `u16` | bazaarIds | the first of the 128 bazaar good ids at `+0x168`-`+0x267` that the new-goods check `0x0057B6F0` has `0x002FA920` fill (`0x002FAA10`) and reads back (`0x0057B740`, `0x0057B74C`) |
| `+0x16A` | `u8[254]` | bazaarIds2 | ids 1-127 of the same array |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| | |
|---|---|
| shops | 57, opened by 98 `openfullscreenmenu_48d(2, shop)` calls in 44 script files |
| distinct goods sold | 589: 106 weapons, 104 armour, 22 accessories, 16 ammunition, 41 items, 7 technicks, 50 magicks, 2 loot, 241 gambits |
| shops that can show each Buy tab | WEAPONS 16, ARMOR 16, ACCESSORIES 15, AMMUNITION 14, ITEMS 30, TECHNICKS 16, MAGICKS 19, LOOT 2, GAMBIT TARGETS 6 |
| largest stock | shop 7, 241 gambits |

</details>

## Modding notes

- A shop's stock is its lists in the shop table; the screen shows whatever those lists hold for the current story
  point.
- A new Buy tab needs an entry in tab set 32 at `0x00D23C70` and a goods code in `0x00D23D60`.
- The sell price is always half the listed price; changing it means changing the `sar` in the row fillers.
- Raising a kind's limit in `0x00D235F8` lets the party buy more of it at once.
- A bazaar table of more than 128 goods, with more than 128 on offer at once, makes `0x0057B6F0` write past the shop
  window's 616 bytes; a list of more than 1,000 goods for one tab overruns the 2,000-byte block at `+0x160`.

## Related

- [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) - the shop table and which list is current.
- [Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md) - how bazaar goods unlock.
- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) - what a trade writes.
- [Menus](menus.md) - the request that opens the shop.
- [Dialogs](dialogs.md) - the shared boxes.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 9 calls with 4 other topics</summary>

**Engine core** (explained on [global state accessors](../Engine-Core/global-state-accessors.md), [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002465F0`](widgets.md) (on widgets) | calls | [`0x001EDDA0`](../Graphics/effect-lifecycle.md) (on effect lifecycle) |
| [`0x00254A10`](text-string-tables.md) (on text string tables) | calls | [`0x00229E40`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences) |
| [`0x003F4060`](widgets.md) (on widgets) | calls | [`0x001EDEC0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen) |

**Controls and input** (explained on [controls](../Controls-And-Input/controls.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002D3900`](status-and-equip-screen.md) (on status and equip screen) | calls | [`0x001E0A10`](status-and-equip-screen.md) (on status and equip screen)<br>[`0x001E0E30`](../Controls-And-Input/controls.md) (on controls) |

**Saving, loading and settings** (explained on [mrp menu resource packages](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003933F0`](clan-primer.md) (on clan primer) | is called by | [`0x00582790`](../Saving-Loading-And-Settings/saving-and-loading-autosave.md) (on saving and loading autosave) |

**World, areas and travel** (explained on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [frame update order](../Engine-Core/frame-update-order.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0036A100`](../Game-Files-And-Data-Tables/resource-lifecycle.md) (on resource lifecycle) | is called by | [`0x00267930`](../Compiler-And-C-Runtime/memory-and-allocation.md) (on memory and allocation)<br>[`0x003319D0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x003EA820`](../Game-Files-And-Data-Tables/ard-area-battle-data.md) Area ard: load or unload field resource (on ard area battle data) |

</details>
