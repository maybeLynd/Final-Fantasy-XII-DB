[Home](../../README.md) / [Menus and HUD](README.md) / Status and Equip screen

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Status and Equip screen: the panes of each, the buttons, where the numbers come from, moving to another member, and the way from Equip to a worn piece | system | Menus and HUD | Menu screens | The Party Menu's Status and Equip entries, one screen procedure with a mode bit: what each mode builds (the status list, the stat panel, the member panel, the member row with experience and LP, the Equip commands, the slot pane and the equipment list), the buttons and their masks, the records each number is read from, stepping to another member and the refresh it runs, the ammunition rule that holds the player on a member, what closes the screen, and the path from the Equip command to the setter. | 0x002C2320, 0x002C2280, 0x002C2C50, 0x002C59D0, 0x002C1E20, 0x002C1000, 0x003FF360, 0x003FDFE0, 0x002C1A80 |

## What the player sees

Status and Equip open from the Party Menu on the member last shown. Both screens show the party's members down the
side, the member's stats (Attack Power to Speed) and, at the bottom, the member's row with experience, the points to
the next level and LP. Status adds the member's status effects as a list with a description of the one under the
cursor. Equip adds four commands, Equip, Remove, Remove All and Optimize, and a pane with the five slots Weapon,
Off-hand, Helm, Armor and Accessory.

L1 and R1, and Left and Right while the command list or the slot pane has the cursor, step to the previous or next
member; at either end only a fresh press wraps round. Status lists every member, guests included; Equip lists only
the six main characters. On Equip, a member holding a weapon that needs ammunition and wearing none cannot be left:
stepping away or backing out plays sound `0x25` and shows a notice. After choosing such a weapon the game asks for
ammunition, and confirming that notice opens the Off-hand list.

Choosing Equip, then a slot, then a piece wears it through the same setter the rest of the game uses
([Equipping an item](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md)).

## How it works

### Opening the screen

The entry dispatcher `0x00281ED0` sends both entries to one opener (`0x0028224D`-`0x0028225A`, call `0x002822A9`):

1. It reads the member the screen last showed, `0x002526F0(6, 4, 1)` (`0x0028221C`-`0x00282226`), and passes it to
   `0x00282650(&member, entry)`.
2. On every entry a negative member becomes 0, stored back with `0x002527B0(6, 4, 0)` (`0x00282656`-`0x00282658`,
   `0x002826C9`-`0x002826DA`). For Licenses `0x4B5` and Equip `0x4B6` only, a member that is empty, a guest (record flag
   `0x2`) or of type above 5 is replaced by the first of the nine member slots that is none of these, or by 0 when no
   slot is, stored back the same way (`0x00282669`-`0x002826EB`). Status `0x4B4` keeps any other member.
3. `0x002C2280(member, row)` builds the `0x170`-byte screen with procedure `0x002C2320` (`0x002C22B1`-`0x002C22CD`) unless
   one is already open at `[0x0209AC30] + 0x140` (`0x002C229A`). The dispatcher then closes the Party Menu's member
   list `+0xF8` (`0x002822B5`-`0x002822C1`).

On message 1 the screen stores itself at `+0x140`, the Party Menu row at `+0x158` and its entry id at `+0x160`,
makes the member current through `0x00285F20` (which writes `+0xDE0` and refills the five slot rows with `0x0027F210`),
and sets bit `0x1` of `+0x168` for Equip, `0x4B6` (`0x002C235C`-`0x002C239D`). Every later branch on the mode tests
that bit or compares `+0x160` with `0x4B4`.

### What each mode builds

| Part | Status `0x4B4` | Equip `0x4B6` |
|---|---|---|
| The command list `+0x150` (`0x002C9BF0`, row height `mCommandMenuStrHeight`) with four rows in the set at `+0xC0` | not built | Equip `0x400`, Remove `0x404`, Remove All `0x401`, Optimize `0x402` (`0x002C23B7`-`0x002C2436`) |
| The description window `0x00292FA0(n)`, kept at `+0x2F8` | n = 4 | n = 2 (`0x002C2491`-`0x002C24A1`) |
| The stat panel `0x003FE410(1)`, [Menu screens](menu-screens.md#the-equip-screens-stat-panel) | built | built (`0x002C24BA`) |
| The member-record panel `0x002CBED0(screen == Status)`, [Menu screens](menu-screens.md#the-member-record-panel) | build word 8: every member | build word 0: main characters only (`0x002C24BF`-`0x002C24CE`) |
| The bottom pane `0x002C1DA0(screen != Status)` | flag 0 | flag 1 (`0x002C24D3`-`0x002C24E3`) |
| On message 14, when the opening run starts | the status pane `0x002C59D0`, once (`0x002C268B`-`0x002C26CC`) | the slot pane `0x003FF160(row, help)` for the cursor row (`0x002C25F6`-`0x002C267F`) |
| On message 19, when the run has finished | focus moves to the status pane (`0x002C26E1`-`0x002C26F8`) | the list's `+0xE0` gets bit `0x200000` (`0x002C2704`-`0x002C270B`) |

Both modes then refresh for the current member (`0x002C2C50(-1)`, `0x002C24EB`), lay the black bands with
`ListHelpBlackBandH` (`0x002C2503`) and take the focus (`0x002C250B`).

The build word reaches the member-record panel as `+0x10` of its creation record (`0x002CBF00`-`0x002CBF09`), and the
panel writes the inverse of its bit `0x8` into bit `0x10` of the menu block's `+0xD3C` (`0x002CC07E`-`0x002CC097`).
With that bit clear, as on Status, the member steps `0x0027ED10` and `0x0027F360` and the panel's own counts accept any
member with a type of 0 or more; with it set, as on Equip, they also skip flag `0x2` and types above 5
(`0x0027ED47`-`0x0027ED63`, `0x002CC6FF`-`0x002CC712`, [Menu screens](menu-screens.md#command-rows-and-first-visits)).

The row texts are `menu_command.bin` 24 Equip, 28 Remove, 25 Remove All and 26 Optimize; their help lines
(`0x002CD3C0(id, help)` keeps the name at `+0x10` and the help at `+0x18` of the row, `0x002CD3F1`-`0x002CD403`):

| Row | Help | Line (`help_menu.bin`) |
|---|---|---|
| Equip `0x400` | `0xBE3` | 43, "Change character's equipment." |
| Remove `0x404` | `0xBE7` | 47, "Remove a specific piece of equipment." |
| Remove All `0x401` | `0xBE4` | 44, "Remove all equipment." |
| Optimize `0x402` | `0xBE5` | 45, "Equip the best available weapon and armor." |

### The screen's messages

The switch at `0x002C25C5` takes messages 9 to 19 through the table `0x002C2C18`; 1, 8 and `0x11F` (`0x002C2592`) are
tested before it, and the `0x11F` handler sits after it ([Widget messages](widget-messages.md)):

| Message | Status | Equip |
|---|---|---|
| 1, construct | the parts above | the parts above |
| 8, focus gained | `+0x164` = -1, then `0x002CC2A0` places the panel's rows | the same, after showing the cursor row's help (`0x00291D80`) and sending itself `0x11F` `0x8000` (`0x002C2517`-`0x002C2586`) |
| 9, focus lost | nothing | sends itself `0x11F` `0x8001` (`0x002C271C`-`0x002C2734`) |
| 10, input turn | `0x002C2923`, below | `0x002C2923`, below |
| 12, command | `0x8002` closes the screen | `0x8000`, `0x8001`, `0x8002`, below |
| 14, run started | builds the status pane | builds the slot pane |
| 18, destroyed | returns to the Party Menu, `0x002814E0(+0x160)`, and clears `+0x140` (`0x002C25C7`-`0x002C25DB`) | the same |
| 19, run finished | focuses the status pane | list bit `0x200000` |
| `0x11F` `0x8000` | | the list gets bit `0x200000`, every row loses bit `0x2` (`0x002CA010(set, -1, 0)`), the rows are coloured, and `+0x168` gets bit `0x4` (`0x002C2B59`-`0x002C2BE4`) |
| `0x11F` `0x8001` | | the list loses bit `0x200000`, every row takes colour 3, the chosen row `+0x164` gets bit `0x2` and colour 0, and `+0x168` loses bit `0x4` (`0x002C2ABB`-`0x002C2B4B`) |

`0x002C9EB0(widget, a, b)` builds message `0x11F` with `a` at `+8` and `b` at `+0x10` and calls the widget's
procedure with it (`0x002C9ED3`-`0x002C9EED`). Bit `0x4` of `+0x168` is therefore set while the command list has the
focus.

When the rows are coloured, a row whose `0x002CDAE0(id)` answers non-zero is drawn in colour 2, and so are Remove All
and Remove when `0x0027F150` answers 1, that is when each of the five slot words at `+0xD48` is empty `0xFFFF` or
Unarmed `0x1000` (`0x0027F159`-`0x0027F18C`); the others are colour 0 (`0x002C2B9A`-`0x002C2BC4`).

`0x002CDAE0` tests a flag of the byte array at `[0x020927C0] + 0x32C4` (`0x00254DD0`): flag 3 for Equip, 4 for Remove,
5 for Remove All and 6 for Optimize (`0x002CDB04`, `0x002CDD60`, `0x002CDC09`-`0x002CDC5C`). The script verb
`setpartymenustatus` writes flags 0, 1, 9, `0x12`-`0x16`, `0x1D` and `0x1E` ([Menus](menus.md)), none of these four.

### The buttons

The input turn reads held `0x02F97368`, pressed `0x02F9736A` and repeat `0x02F9736C` of set 0; bit i is Select, L3, R3,
Start, Up, Right, Down, Left, L2, R2, L1, R1, Triangle, Circle, Cross, Square ([Controls](../Controls-And-Input/controls.md)).

| Where | Press | Does |
|---|---|---|
| any, while `0x00368240` answers 2 | | nothing, except that the slot pane's turn first shows its grid (`0x002D45C0(grid, 1)`, bit `0x8000000` of the grid's `+0xE0` and `0x002445C0`; `0x003FF400`-`0x003FF416`) (`0x002C293B`-`0x002C2942`, `0x003FF41B`-`0x003FF422`) |
| the screen, Equip | the turn after the slot pane was cancelled | nothing: `+0x168` bit `0x8`, set by `0x002C22F0` from the pane's cancel (`0x003FF74D`), is cleared instead (`0x002C2960`-`0x002C296D`) |
| the screen, the slot pane, the list | Square `0x8000` | the Party Menu's member pages, below |
| the status pane | confirm `0x01E0C2A0` or Square | the same pages (`0x002C5B3A`-`0x002C5B4E`) |
| the screen (Equip) and the slot pane | any of L1, R1, Left, Right (`0xCA0`) while the ammunition test fails | sound `0x25` and notice case 0, and no step (`0x002C29BB`-`0x002C29F4`, `0x003FF48D`-`0x003FF4C6`) |
| the screen and the slot pane | R1 `0x800` or Right `0x20`, alone among the four and on the repeat word | the next member, `0x002C2240(slot)`; when the current member is the last in the panel (`0x002CC630`), only a fresh press of R1 or Right (`0x820`) (`0x002C2A06`-`0x002C2A4E`, `0x003FF4D0`-`0x003FF509`) |
| the screen and the slot pane | L1 `0x400` or Left `0x80` | the previous member, `0x002C2200(slot)`, with the first-member test `0x002CBC20` and a fresh press `0x480` (`0x002C2A12`-`0x002C2A72`, `0x003FF50B`-`0x003FF539`) |
| the status pane | R1 or L1 (`0xC00`) | the same steps with the same end tests (`0x002C5B6C`-`0x002C5BCD`) |
| the status pane | Left, Right, Up, Down | moves among the statuses, below |
| the list | L1 or Left, R1 or Right | the previous or next tab when the list has more than one (`0x003FDBAC`-`0x003FDC57`) |
| the command list, the slot pane's grid, the list, the status list | Up, Down, confirm, cancel | the list itself (`0x002D3900`): confirm posts `0x8001`, cancel `0x01E0C2A4` posts `0x8002` (`0x002D4294`-`0x002D42A9`) |

A list plays its byte `+0xFC` as the sound after a confirm its owner accepted, 2 when it is 0, none for -1
(`0x002D4114`-`0x002D4154`). A confirm its owner refused, or one on a row past the list's count, plays byte `+0xFD` the
same way, 5 when it is 0 (`0x002D40ED`, `0x002D410E`, `0x002D4255`-`0x002D426C`). A cancel plays byte `+0xFE` the same
way, 3 when it is 0 (`0x002D42AE`-`0x002D42D6`; the 3 is set at `0x002D4030` or `0x002D4229`). The screen sets the confirm
and cancel sounds for each command, below.

### The Party Menu's member pages

`0x002C1A80(record, pressed, extra, held, repeat)` runs before every other button. It does nothing and answers 0 while
`0x00264150`, the byte at `0x0209A2A9`, is not 0 (`0x002C1A97`-`0x002C1AB1`), and keeps its page at `+0xDE7`
([Menu screens](menu-screens.md)):

1. Page 0 (`0x002C1ACB`), only while the menu block's `+0x118`, the Party Menu's name panel, exists and `+0x290` is
   empty (`0x002C1C1D`-`0x002C1C2F`): a press of Square or `extra` plays sound `0x38`, opens the name panel and the list
   panel `+0x120` (`0x002C19E0`, `0x002C3C10`) and goes to page 1 (`0x002C1C31`-`0x002C1C58`).
2. Page 1: the list panel's own buttons first (`0x002C2F90`); then Square, confirm or `extra` plays sound `0x38`,
   closes the list panel, opens the four-pane panel `+0x128` (`0x002C5480`) and goes to page 2 (`0x002C1AE4`-`0x002C1B3A`).
3. Page 2: the four-pane panel's buttons (`0x002C4220`); then Square, confirm or `extra` closes every panel with sound 3
   (`0x002C1B4B`-`0x002C1B77`).
4. On page 1 or 2, cancel closes the three panels with sound 3 and returns to page 0 (`0x002C1B8D`-`0x002C1C13`); L1 and
   R1 on the repeat word step the member inside them (`0x002C12B0`, `0x002C1320`; `0x002C1C66`-`0x002C1C8B`).

While the page is not 0 it answers non-zero (`0x002C1C97`-`0x002C1CA0`), and the caller hides its cursor and does
nothing else that turn (`0x002C29A2`-`0x002C29B6`, `0x002C5B53`-`0x002C5B65`).

### The status pane

`0x002C59D0` is a `0x150`-byte widget from record 2 of layout unit 7 (`0x002C5A0B`-`0x002C5A23`), kept at the menu
block's `+0x110`. Its list is node 3's list (`0x002C5A73`-`0x002C5A86`), drawn by `0x002C5900`. On message 1 it fills the
entries (`0x002C56F0`), hides node 4 when the member has a status (`0x002C5AAA`-`0x002C5ABB`) and sizes the description to
the widest status name of the party (`0x002C5660`, `0x002C5AC6`).

`0x002C56F0` reads the member through `0x00282DF0(+0xDE0)`, the copy at `[0x0209AC30] + 0x408` that `0x00283270` builds
([Party member status record](../Characters-And-Objects/party-member-status-record.md)):

1. It fills 32 entries with the statuses in the member's mask `+0x44` and keeps how many have an order byte at
   `+0x14C` (`0x002C573E`-`0x002C57C3`).
2. It fills them again with a mask chosen by the language test `0x00254A10`: when that is false, or `0x00264150` is
   non-zero, the member's mask; otherwise all 32 statuses (`0x002C5707`-`0x002C5791`). It then sorts them by their order
   byte (`0x002D03B0`) and keeps the member's mask at `+0x148`.
3. With the language test false it sizes the list to the count, at least 1 (`0x002C57C9`-`0x002C57EC`); with it true
   the list has 32 rows (`0x002C5AD8`-`0x002C5AF0`), and a row whose status the member lacks is hidden, so each status
   keeps its place.

The entries, the row painter and the cursor step `0x002C5810` are on [Party list](party-list.md). A row shows the
status's icon and its name, text `+0x18` of its class `0x1A` record (`0x002C5951`-`0x002C59B8`).

| Message | Does |
|---|---|
| 8, focus gained | puts the cursor `+0x14D` on the first status shown, shows the list and calls `0x002CB7F0(1)` (`0x002C5D0F`-`0x002C5D74`) |
| 9, focus lost | closes the description box and hides the cursor (`0x002C5D80`-`0x002C5D92`) |
| 10, input turn | the member pages, L1 and R1, then the arrows (`0x002C5B01`-`0x002C5D03`) |
| 12 `0x8000` | the description of the status under the cursor, `0x00293110(14, status)`, or `0x00293110(0, 0)` for an empty row (`0x002C5DD6`-`0x002C5E39`) |
| 12 `0x8002` | posts `0x8002` to the screen `[0x0209AC30] + 0x140` (`0x002C5DB4`-`0x002C5DCA`) |
| 18 | clears `+0x110` (`0x002C5E42`-`0x002C5E4B`) |

The arrows move the cursor only with the language test true and more than one status (`0x002C5C37`-`0x002C5C4B`):
Left, Right, Up and Down are `0x002C5810` directions 0, 1, 2 and 3. A move that needs no wrap (`0x002C5EC0`) runs on the
repeat word; a wrap needs a fresh press. A move plays sound 1 and moves the list (`0x002C5CD5`-`0x002C5CF7`). After a
member step the cursor goes back to the first status shown and the turn ends (`0x002C5BD6`-`0x002C5C25`). In every other
case, after a move too, the list then runs the turn (`0x002C5CFC`-`0x002C5D03`).

### The bottom pane: the member's row, experience and LP

`0x002C1DA0(flag)` builds the `0xD8`-byte pane `0x002C1E20` at `+0x130` from record 2 of layout unit 6, at
`StatusAloneBottomX` and `StatusAloneBottomY` ([Screen layouts](screen-layouts.tsv)), moves its seven nodes down by
3 and keeps the flag at `+0xD0` (`0x002C1E6D`-`0x002C1FCB`). `0x002C1FF0` rebuilds its contents for the current member:

- the Party Menu's member row `0x00283BB0` with its child `0x00284450`, given the flag as its construct `b`
  (`0x002C202F`-`0x002C20DE`), filled by `0x00283E40`, with nodes 0, 1, 2 and 3 set to 0.75 of their widths and node 5
  to 0.75 of its width less 2 (`0x0028484B`) by `0x002847C0` ([Menu screens](menu-screens.md)); the row keeps the flag
  at `+0xF8` (`0x00283DFE`) and, with it set, as on Equip, skips its status icons (`0x0028401B`-`0x002840B0`);
- the experience panel `0x002C1000` from record 15 of layout unit 6 (`0x002C219E`-`0x002C21D4`).

`0x002C1000` reads the member's experience `+0x90`, points to the next level `+0x94` and LP `+0xB0`, shows -1 as 0
and caps them at 99,999,999, 999,999 and 99,999 (`0x002C107A`-`0x002C1105`). Experience goes to node 6 and the points to
the next level to node 7 (`0x002C1132`, `0x002C118C`, `0x002C121F`). Then:

- for a guest (type 0 or more and flag `0x2`) node 4 shows `menu_command.bin` 3, "-", in colour 2, and no LP is
  written (`0x002C113C`-`0x002C11C3`);
- for anyone else node 4 is hidden, and LP (node 5) and node 3 are shown only while `0x00283730(0x4B5)` answers bit
  `0x1`, the Licenses entry's story flag `0x4006` ([Story flags](../Story-Events-And-Hunts/story-flags.md);
  `0x002C1224`-`0x002C1289`).

The member row also carries the previewed and current max HP and MP that the stat panel's refreshers write
([Menu screens](menu-screens.md#the-equip-screens-stat-panel)), in colour 5 when the preview is higher and 4
otherwise (`0x00283BFE`-`0x00283C92`).

### Where the numbers come from

| What | Read from |
|---|---|
| the statuses and their order | the member copy's `+0x44` and the class `0x1A` records (`0x002C56F0`) |
| experience, next level, LP | the member copy's `+0x90`, `+0x94`, `+0xB0` (`0x002C1000`) |
| the nine stats | the stat panel's comparisons, as worn on Status (`0x003FEAD0(0)`, `0x002C2CF1`-`0x002C2CF8`) and previewed on Equip ([Stats](../Damage-And-Battle-Formulas/stats.md)) |
| the slot names | `menu_expansion.bin` `0x4A99`, `0x4A9A`, `0x4A9C`, `0x4A9D`, `0x4A9E` (`0x003FF67D`-`0x003FF6C3`) |
| the pieces in the slots | the five slot words at the menu block's `+0xD48`, `0x20` bytes apart, filled by `0x0027F210` ([Menu screens](menu-screens.md)) |
| the list of pieces | the inventory rows of the slot's tab ([Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md#the-equip-screen)) |
| the description box | kind 14 and the status on Status; on Equip `0x00292F60(slot)` for the slot pane (`0x003FF920`) and word `+2` of the slot's record at `0x00D23988` for the list, 1, 3, 4, 4, 5 (`0x003FE2C1`-`0x003FE2D5`) ([Inventory screen](inventory-screen.md#the-description-box)) |

### Moving to another member

`0x002C2200(slot)` steps back with `0x0027ED10` and `0x002C2240(slot)` forward with `0x0027F360`; on a move each plays
sound `0x51` and refreshes with `0x002C2C50(slot)` (`0x002C220C`-`0x002C2222`, `0x002C224C`-`0x002C2262`).

The argument is the slot passed on to `0x003FE720`, which reads it for Remove `0x404` only (`0x003FE751`-`0x003FE75D`). The
screen passes -1 (`0x002C2A33`, `0x002C2A46`, `0x002C2A6F`), and the slot pane the cell under its cursor, (`+0xF2` +
`+0xF4`) x `+0xEC` + `+0xEE` + `+0xED` of its grid (`0x003FF3D4`-`0x003FF3FE`; `0x003FF4F0`, `0x003FF502`, `0x003FF537`).

The steps write
the new member to `+0xDE0`, refill the slot rows with `0x0027F210` and set the step arrow `+0xDE9` to 2 or 1
(`0x0027ED71`-`0x0027ED87`, `0x0027F3FF`-`0x0027F416`).

`0x002C2C50(slot)` refreshes:

1. the status pane, when it exists: its entries again (`0x002C56F0`), and node 4 shown only for a member without
   status (`0x002C2C63`-`0x002C2C92`);
2. the bottom pane's row and experience panel (`0x002C1FF0`);
3. the stats: on Status `0x003FEAD0(0)`; on Equip `0x003FE720(command, slot)` for the command under the list's cursor;
   while the list has the focus `slot` is replaced by -1 and `0x11F` `0x8000` recolours the rows after it
   (`0x002C2CD0`-`0x002C2D6D`);
4. the member panel's rows (`0x002CC2A0`);
5. the remembered member, `0x002527B0(6, 4, member)` (`0x002C2CA7`-`0x002C2CC8`), which the next opening reads.

From the slot pane a step also re-shows the description of the slot under its cursor (`0x003FF53E`-`0x003FF545`).

### The Equip commands

Message 12 of the screen:

- `0x8000`, the cursor moved (`0x002C28FC`-`0x002C2917`): the slot pane, when it exists, keeps the row's id at `+0x178`
  and its help at `+0x180` (`0x003FF9F0`); the help line shows the row's help (`0x00291D80`); and `0x003FE720(id, -1)`
  previews the command: every slot empty for Remove All, the Optimise set for Optimize, and the worn set otherwise
  ([Menu screens](menu-screens.md#the-equip-screens-stat-panel)).
- `0x8001`, confirm (`0x002C2834`-`0x002C28F5`): a row whose colour is not 0 is refused (answer 1). Otherwise the id goes
  to `+0x164`, and:
  - Equip and Remove set the confirm sound 2, put the slot pane's cursor on the Weapon row and give it the focus
    (`0x003FF9A0`);
  - Remove All and Optimize send the slot pane message `0x11D` with the id and 1, recolour the rows, and set the
    confirm sound `0x19` for Remove All and `0x4F` for Optimize. On `0x11D` the pane runs `0x0031A300(member, 1)` for
    Remove All or `0x002F9F20` and `0x0031A710(member, set, 1)` for Optimize, then refreshes the menu records and rows
    (`0x003FE3A0`, `0x00283840(1)`) (`0x003FF7F4`-`0x003FF890`).
- `0x8002`, cancel: on Equip it runs the ammunition test first, below; then it closes the screen.

### The slot pane and the list: from Equip to a worn piece

The slot pane `0x003FF360` (`0x190` bytes) is built by `0x003FF160(command, help)` (`0x003FF19C`-`0x003FF1CA`) from record 3
of layout unit 7. Its grid `+0x170` has 5 rows painted by `0x003FF1F0`, its set the five slots, each with help `0xCC9`,
"Change equipment." (`0x003FF59D`-`0x003FF6E0`). The rows' painter is on
[Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md#the-equip-screen).

| Message | Does |
|---|---|
| 8, focus gained | shows the grid and posts its cursor, so `0x8000` follows (`0x003FF560`-`0x003FF593`) |
| 10, input turn | first shows the grid as message 8 does, `0x002D45C0(grid, 1)`, bit `0x8000000` of the grid's `+0xE0` and `0x002445C0` (`0x003FF400`-`0x003FF416`); then nothing more while `0x00368240` answers 2 (`0x003FF41B`-`0x003FF422`) or a notice is open (its owner's `+0x40` bit `0x80000`, `0x002CE4DC`; `0x003FF428`-`0x003FF431`); else the member pages (`0x002C1A80`): when they answer non-zero it undoes those three steps, `0x002D45C0(grid, 0)`, bit `0x8000000` cleared and `0x002445C0`, and stops (`0x003FF437`-`0x003FF488`); otherwise the ammunition test, the member steps, then the grid (`0x003FF48D`-`0x003FF556`) |
| 12 `0x8000` | the preview for the command and this slot (`0x002C2CD0(slot)`), and the slot's description and the command's help (`0x003FF920`) (`0x003FF76F`-`0x003FF77A`) |
| 12 `0x8001` | `0x003FF040(pane, slot)` |
| 12 `0x8002` | calls `0x003FE6E0`, clears the warnings `+0xDE2`, `+0xDE3`, calls `0x00291D70(0)`, closes the description (`0x00293110(0, 0)`), clears bit `0x8000000` of the grid's `+0xE0` and calls `0x002445C0`, sets the screen's skip bit and gives up the focus (`0x003FF706`-`0x003FF755`) |
| 18 | clears `+0x108` (`0x003FF8DD`-`0x003FF8E4`) |
| 19 | the ammunition request, below (`0x003FF892`-`0x003FF8D6`) |
| `0x11D` | Remove All, Optimize, or the ammunition request's answer (`0x003FF7AB`-`0x003FF7E1`) |

`0x003FF040(pane, slot)`:

- For Equip (`+0x178` = `0x400`) it sets the grid's confirm sound 2 and opens the list, `0x003FDA20(slot, +0x18A)`
  (`0x003FF084`-`0x003FF0A2`).
- For Remove, a slot holding nothing or Unarmed answers 1; any other piece is taken off with
  `0x003FFA20(slot, 0xFFFF)` (`0x003FF0B9`-`0x003FF0FC`).

`0x003FDA20` builds the `0x188`-byte list `0x003FDFE0` at `+0x150`, closes the slot pane (`0x00244DD0`), shows the slot
name and its piece (`0x003FEDC0`, `0x003FEE40` with `0x0027F1A0`), moves the bottom pane to `StatusAloneTopX`,
`StatusAloneTopY` and fades its experience panel out (`0x002C1D30`), and focuses the list (`0x003FDA35`-`0x003FDAB6`).
The list's message 1 builds its rows with `0x003FD860` for the Off-hand slot and `0x003FD6B0` for the others
(`0x003FE30B`-`0x003FE324`).

The list's message 12 first remembers the row under the cursor for its tab and the tab for the slot
(`0x002527B0(8, ...)`, `0x003FE07E`-`0x003FE0D9`), then:

- `0x8000`: the five slot words with this row's id in the list's slot `+0x17E` go to `0x003FEAD0` as the preview
  candidate, the help window takes `0xCC9` and any warning (`0x002CA490`, [Stats](../Damage-And-Battle-Formulas/stats.md)), and
  the description box shows the piece (`0x003FE1EC`-`0x003FE2D5`);
- `0x8001`: with no rows, or a piece that `0x003FCA70` marks (`0x0027F030`, refused or the wrong ammunition), it answers
  1 and nothing happens; otherwise `0x003FFA20(slot, id)` wears it, the list closes with `0x003FD2C0(id)` and the confirm
  sound is `0x18` (`0x003FE198`-`0x003FE1E0`);
- `0x8002`: the Off-hand rule below, or `0x003FD2C0(0xFFFF)` (`0x003FE102`-`0x003FE18E`).

`0x003FFA20` is step 2 of [Equipping an item](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md): it calls
`0x0031A510(member, slot, id, 1)` and refreshes the menu (`0x003FFA2A`-`0x003FFAA0`). `0x003FD2C0(id)` closes the list,
stores `id` at the slot pane's `+0x188`, opens the pane again, releases the slot name, reopens the member panel
(`0x002CC760`) and moves the bottom pane back with `0x002C1CC0` (`0x003FD2C0`-`0x003FD356`).

### The ammunition rule

`0x003231F0(type, 0)` tests the member's worn set (`+0x50` of the record `[0x02EBF190] + 8 + type x 0x1C8`): it answers
`0x25` for an empty weapon slot, `0x26` when `0x0031EA90` gives 4 for the weapon and the off-hand is empty or its
ammunition's byte `+9` differs from the weapon's `+0x11`, and 0 otherwise (`0x003231F9`-`0x00323331`).

- While it answers non-zero on Equip, holding L1, R1, Left or Right, or the screen's cancel, plays sound `0x25` and
  shows notice case 0, and the member stays (`0x002C29C3`-`0x002C29F4`, `0x002C277B`-`0x002C27CD`). The cancel also sets the
  list's cancel sound to none (`0x002C27B7`). Notice case 0 is `help_menu.bin` 319 (`0x002CE50E`, `0x002CE68F`), which
  holds an empty line in English and Italian and "Bitte die entsprechende Munition wählen." in German.
- When the slot pane's run finishes after the list closed on a piece (`+0x188` not `0xFFFF`), the Off-hand word
  `+0xD68` is empty and the piece's class is an ammunition weapon (`0x002CCA10`), it shows notice case 1, "Please equip
  appropriate ammunition." (`help_menu.bin` 46, `0x002CE51D`) (`0x003FF892`-`0x003FF8D6`).
- Confirming that notice sends the pane `0x11D` with 1 and -2 (`0x002CE413`-`0x002CE459`); the pane then sets `+0x18A`
  to 1, moves its cursor to the Off-hand row and confirms it, which opens the Off-hand list (`0x003FF7AF`-`0x003FF7E1`).
- In the Off-hand list, cancel is refused with sound 5 while the weapon is an ammunition weapon and the off-hand row
  is empty or holds no ammunition (`0x002CCA00`) (`0x003FE102`-`0x003FE174`).

### Closing

Cancel reaches the screen as `0x8002`: from the status pane on Status, from the command list on Equip, where the
ammunition test runs first. The screen then closes itself and its parts: the stat panel, the screen title `+0x2D8`,
the bottom pane, the member panel, the bands, the description window, the status pane and the slot pane
(`0x002C27D7`-`0x002C2828`). Its message 18 then returns to the Party Menu with its entry id (`0x002C25C7`).

## Layouts

`StatusEquipScreen` (`0x170` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header (widgets.md) |
| `+0x0C0` | `i16` | rowCount | the command set: the count (`0x002CD4D0`, `0x002CD3C0`) |
| `+0x0C8` | `void*` | rows | the command set's rows, pointing at `+0xD0` (`0x002CD4EB`) |
| `+0x0D0` | `u8[128]` | rowData | four `0x20`-byte rows: id `+0x00`, name `+0x10`, help `+0x18` (`0x002CD3F1`-`0x002CD403`) |
| `+0x150` | `void*` | list | the command list `0x002C9BF0` (`0x002C2436`); Equip only |
| `+0x158` | `void*` | openRow | the Party Menu row the opener was given (`0x002C236E`) |
| `+0x160` | `i32` | entry | the row's id, `0x4B4` or `0x4B6` (`0x002C2377`) |
| `+0x164` | `i32` | chosen | the confirmed command (`0x002C284B`), -1 on focus (`0x002C251E`) |
| `+0x168` | `u32` | flags | bit `0x1` Equip (`0x002C239D`); bit `0x4` the command list has the focus (`0x002C2BE4`, `0x002C2B4B`); bit `0x8` skip one input turn (`0x002C230B`, `0x002C296D`) |

`StatusPane` (`0x150` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header (widgets.md) |
| `+0x0C0` | `void*` | list | node 3's list (`0x002C5A86`) |
| `+0x0C8` | `u8[128]` | entries | 32 four-byte status entries (party-list.md; `0x002C573E`) |
| `+0x148` | `u32` | mask | the member's status mask `+0x44` (`0x002C57BD`) |
| `+0x14C` | `u8` | count | the statuses with an order byte (`0x002C57C3`) |
| `+0x14D` | `i8` | cursor | the entry under the cursor (`0x002C58CF`, `0x002C5BD6`) |

`EquipSlotPane` (`0x190` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header (widgets.md) |
| `+0x0C0` | `u8[16]` | set | the slot set: the count and a pointer to `+0xD0` (`0x003FF678`) |
| `+0x0D0` | `u8[160]` | rowData | five `0x20`-byte rows, Weapon to Accessory, help `0xCC9` (`0x003FF67D`-`0x003FF6C3`) |
| `+0x170` | `void*` | grid | the five-row grid (`0x003FF635`) |
| `+0x178` | `i32` | command | the command under the screen's cursor (`0x003FF5A5`, `0x003FFA03`) |
| `+0x180` | `void*` | help | that command's help text (`0x003FF5C3`, `0x003FFA18`) |
| `+0x188` | `u16` | picked | the id the list closed on, `0xFFFF` on cancel (`0x003FF5B8`, `0x003FD301`) |
| `+0x18A` | `i16` | listFlag | 1 for the ammunition request (`0x003FF7CA`), passed to the list and cleared (`0x003FF04F`-`0x003FF05E`) |

## Modding notes

- The Status screen walks guests because the member panel clears `+0xD3C` bit `0x10` for build word 8; a build
  word of 0 from `0x002C24BF`-`0x002C24CB` would limit Status's steps and panel to the six main characters, while the
  opener's `0x00282650` check covers only Licenses and Equip.
- The four Equip commands can be greyed by flags 3 to 6 of the byte array at `[0x020927C0] + 0x32C4`; a greyed row is
  refused on confirm (`0x002C2834`-`0x002C2847`).
- Notice case 0 carries no English text (`help_menu.bin` 319), so the ammunition refusal on stepping or backing out
  shows an empty line in English; giving that line text fixes it without code.
- The status list keeps fixed places only under the language test (`0x00254A10`); otherwise it lists the member's
  statuses one after another.

## Related

- [Menu screens](menu-screens.md): the Party Menu's entries, the command rows, the member-record panel, the stat panel
  and the menu block.
- [Party list](party-list.md): the status entries, the row painter and the cursor step.
- [Equipping an item](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) and
  [Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md): the setter, the list marks and the slot rows.
- [Party member status record](../Characters-And-Objects/party-member-status-record.md): the member copies the screen reads.
- [Inventory screen](inventory-screen.md): the tab steps and the description box.
- [Dialogs](dialogs.md): the notice.
- [Controls](../Controls-And-Input/controls.md): the button words and masks.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 71 calls with 23 other topics</summary>

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x0031A300` | calls | `0x00236820` |

**Sound and music** (explained on [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md))

| Function | | Functions |
|---|---|---|
| `0x002814E0` | calls | `0x002DEE50` |

**Enemy AI and gambits** (explained on [gambits](../Enemy-AI-And-Gambits/gambits.md), [glossary](../Engine-Core/glossary.md))

| Function | | Functions |
|---|---|---|
| `0x00283270` | calls | `0x00327BE0` |
| `0x0031EA90` | is called by | `0x00301AD0` |

**Damage and battle formulas** (explained on [subsystem update flags](../Engine-Core/subsystem-update-flags.md), [native limits](../Engine-Core/native-limits.md))

| Function | | Functions |
|---|---|---|
| `0x002F9F20` | calls | `0x00320AB0` |
| `0x0031A510` | calls | `0x0031B860` |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md), [global state accessors](../Engine-Core/global-state-accessors.md), [startup constants](../Engine-Core/startup-constants.md))

| Function | | Functions |
|---|---|---|
| `0x00244DD0` | calls | `0x00229DF0`, `0x00229E70`, `0x00229EA0` |
| `0x00254A10` | calls | `0x00229E40` |

**Gameplay** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md), [steal](../Damage-And-Battle-Formulas/steal.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md))

| Function | | Functions |
|---|---|---|
| `0x0031A510` | calls | `0x00322C50` |
| `0x0031EA90` | calls | `0x0031E9F0` |
| `0x003231F0` | calls | `0x0031EA90` |

**Controls and input** (explained on [menu lists](menu-lists.md), [controls](../Controls-And-Input/controls.md))

| Function | | Functions |
|---|---|---|
| `0x002814E0` | calls | `0x001E0F20` |
| `0x002C2F90` | calls | `0x001E0A10` |
| `0x002C4220` | calls | `0x001E0A10` |
| `0x002D3900` | calls | `0x001E0A10`, `0x001E0E30` |

**Items, equipment, shops and licenses**

| Function | | Functions |
|---|---|---|
| `0x0027F030` | calls | `0x00317B70` |
| `0x00283E40` | calls | `0x00323630`, `0x00323670`, `0x003236B0` |
| `0x002C2320` | calls | `0x003231F0` |
| `0x002F9F20` | calls | `0x002F7A10`, `0x002F7EC0`, `0x00317B20` |
| `0x0031A300` | calls | `0x0031A510` |
| `0x0031A300` | is called by | `0x0030FBE0` |
| `0x0031A510` | calls | `0x0030C410`, `0x0030F9A0`, `0x00317930`, `0x00318B40` |
| `0x0031A510` | is called by | `0x0031A300`, `0x0031A710` |

**Items, equipment, shops and licenses**

| Function | | Functions |
|---|---|---|
| `0x0031A710` | calls | `0x0031A510` |
| `0x0031A710` | is called by | `0x0030FAA0` |
| `0x0031EA90` | is called by | `0x00309480`, `0x003231F0` |
| `0x003FE720` | calls | `0x002F9F20`, `0x0030A4E0` |
| `0x003FEAD0` | calls | `0x0030A4E0` |
| `0x003FF360` | calls | `0x002F9F20`, `0x0031A300`, `0x0031A710`, `0x003231F0` |
| `0x003FFA20` | calls | `0x0031A510` |

**Items, equipment, shops and licenses** (explained on [equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md), [license board screen](license-board-screen.md), [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md), [equipment row](../Items-Equipment-Shops-And-Licenses/equipment-row.md))

**Items, equipment, shops and licenses** (explained on [equipment](../Items-Equipment-Shops-And-Licenses/equipment.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party table](../Party/party-table.md), [stats](../Damage-And-Battle-Formulas/stats.md))

**Movement and pathfinding** (explained on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md))

| Function | | Functions |
|---|---|---|
| `0x0031EA90` | is called by | `0x003343D0` |

**Party** (explained on [party control modes](../Engine-Core/party-control-modes.md))

| Function | | Functions |
|---|---|---|
| `0x00283270` | is called by | `0x00328BD0` |

**Steam and achievements** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00283270` | is called by | `0x00316930` |

**Graphics**

| Function | | Functions |
|---|---|---|
| `0x00244DD0` | is called by | `0x00579420` |
| `0x002526F0` | is called by | `0x00579420` |
| `0x002527B0` | is called by | `0x00579420` |
| `0x00254A10` | is called by | `0x002B0280`, `0x002D2DB0` |
| `0x00264150` | is called by | `0x002BAF80` |
| `0x002D3900` | is called by | `0x00578450`, `0x00579420` |
| `0x00368240` | is called by | `0x002D2DB0` |

**Graphics** (explained on [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md), [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md), [frame update order](../Engine-Core/frame-update-order.md))

**Game files and data tables** (explained on [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md))

| Function | | Functions |
|---|---|---|
| `0x002814E0` | calls | `0x0024A5A0` |

**Rewards: EXP, LP, gil and loot** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

| Function | | Functions |
|---|---|---|
| `0x00264150` | is called by | `0x002F90C0` |

**Saving, loading and settings**

| Function | | Functions |
|---|---|---|
| `0x00244DD0` | is called by | `0x00583040` |
| `0x00254A10` | is called by | `0x005832B0` |
| `0x002814E0` | is called by | `0x00582860` |
| `0x00282DF0` | is called by | `0x00583D60` |
| `0x00283270` | is called by | `0x00582860`, `0x005844A0` |

**Saving, loading and settings** (explained on [saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md), [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md), [game application](../Engine-Core/game-application.md), [native limits](../Engine-Core/native-limits.md))

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x00264150` | is called by | `0x0050CC30` |

**Story, events and hunts** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

| Function | | Functions |
|---|---|---|
| `0x00283730` | calls | `0x0032A8A0` |
| `0x00283E40` | calls | `0x0032A8A0` |
| `0x002CDAE0` | calls | `0x0032A8A0` |

**World, areas and travel** (explained on [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md))

| Function | | Functions |
|---|---|---|
| `0x00264150` | is called by | `0x0057FB00` |

</details>
