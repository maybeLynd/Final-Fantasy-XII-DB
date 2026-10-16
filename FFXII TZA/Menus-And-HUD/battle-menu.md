---
title: "Battle menu: the command lists, the party HP and MP list, the help line, the boss and overhead gauges, and how a chosen command is issued"
kind: "system"
category: "Menus and HUD"
addresses: "00279E20, 00276D30, 002778C0, 0027E050, 0027C3D0, 00311B20, 0029BE50, 002C8310"
---

## What the player sees

- The battle menu lists Attack, Magicks & Technicks, Mist (or Dismiss while an Esper is out), Gambits and Items.
- Choosing a list opens the next one, such as the five magick schools, and choosing an action asks for a target.
- Greyed commands explain themselves on the help line, for example "Silenced: Cannot use magicks."
- The party list shows each member's name, HP and MP; a boss shows a gauge at the top, and units carry HP gauges
  above their heads.

## How it works

### The widgets

| Object | Size | Procedure | Built by |
|---|---|---|---|
| manager | `0x61F0` | `00279E20` | `00276650` (`002766D1`), from `00290CF0` into `[0209BE80] + 0xAB30` |
| panel, two slots | `0x3010` | `00276D30` | manager message 2 (`0027A402`) |
| list widget | `0x2DC0` | `002778C0` | panel message 1 (`00276DD3`) |
| list page, two | `0x1620` | `0027AD70` | list widget message 1 (`002779DB`, `00277A08`) |
| target category tabs | `0xD0` | `0027C870` | manager message 2 (`0027A12F`) |
| Dismiss confirmation | `0x4A0` | `0027AA70` | manager message 2 (`0027A369`) |

The menu is requested through router ids 1 and 4 ([Menus](menus.md)): `0035D660` calls `0028FD50`, and the HUD frame
`0028E290` builds the manager through `00290CF0` (`0028E480`). The manager starts with list kind 1, the top commands,
and keeps a stack of the lists opened in the cursor block at `[0209BE80] + 0xAA60` (`00290D88`).

Each widget dispatches through its own tables: the manager answers 21 messages (`0027AA38`, `0027A9E0`), the panel 10
(`00277880`, `00277854`) and the list widget 14 (`00279D98`, `00279D60`).

### Lists

`0027E050` turns a menu kind into a list code for the list builder `0031EB20` and installs the row painter, and
`0027D480` writes the title:

| Kind | List | Title |
|---:|---|---|
| `1` | top commands, list 6 | none |
| `2` | Magicks & Technicks, list 8 | "Magicks & Technicks" |
| `3` | Mist, list 9 | "Mist" |
| `4` | items, list `0xB` | "Items" |
| `6`, `7` | Summon and Quickening actions, list `0xB` | "Summon", "Quickening" |
| `10`-`14` | the magicks of one school, list `0xB` | "White Magicks" to "Arcane Magicks" |
| `15` | technicks, list `0xB` | "Technicks" |
| `0x10`-`0x13` | a target list, codes `0x10`, `0xD`, `0xF`, `0x1C` (`01E0C398`) | the action's name |

The command lists are `{flag, id}` pairs (`0031EB88`-`0031EBEC`):

| List | Table | Rows |
|---:|---|---|
| `6` | `00D10650` | Attack, Magicks & Technicks, Mist, Dismiss, Gambits, Items |
| `8` | `00D10680` | White, Black, Time, Green and Arcane Magicks, Technicks |
| `9` | `00D1065C` | Summon, Quickening |

Mist is listed only while `003135C0` is 0, and Dismiss only while it is 1 ([Command availability](../Battle-Actions/command-availability.md)),
so the top list shows one of the two. Each row is checked with `00318CD0`, which leaves it out, greys it with a reason,
or lists it (`0031ECA3`-`0031ED3D`). An action list keeps the actions of the list's kind byte `+0x1E` (and school
`+0x2C & 7`) that the member owns and has left (`00317BC0`), with their MP, Mist charge or item count.

### Row painters

`0027E050` installs one painter per list (`0027E2F0`):

| Painter | Lists | Draws |
|---|---|---|
| `00276BE0` | top commands, Mist | the command labels |
| `0027D240` | the magick schools, kind 2 | the label word of the school row (class `0x18`) when flag bit 2 is set, of the command row (class `0x15`) otherwise |
| `0027CE70` | the action lists, kinds 4-8, 10-15 and 20 | the action rows |
| `0027BC10` | kind 9, list `0x18` | the name of a class 1 row, or Remove (`menu_command.bin` `0x404`) for the id -1, with byte `+0x15EF` set to 6 for the row equal to `+0x1538` |
| `0027D5C0` | target list `0xF` | the name of the row's id through `0031C5D0` |
| `0027E530` | the other target lists | the unit's name (`00272CB0`) and, when `00272C80` gives a number, that number after it |

A row whose greyed flag is set is drawn at alpha `0x40`. An empty list draws one row with alpha `96 + 32 x sin(t x pi / 30)`
of the frame counter: "No Available Targets" (`menu_message.bin` `0x7D1`) for a target list, and `0x7D2`, empty in the
shipped text, for the others (`0027D24A`-`0027D25E`, `0027BC1A`-`0027BC29`).

### Names and help

The labels and help come from the battle command table, class `0x15` (21 rows), and the magick schools, class `0x18`
(5 rows): word `+2` is the label and word `+0` the help line (`0031DC54`-`0031DCEC`).

| Command | Help (`help_menu.bin`) |
|---|---|
| Attack | "Attack with weapon in hand." (`0xBB8`) |
| Technicks | "Special actions that cost no MP." (`0xBBA`) |
| Items | "Use items from your inventory." (`0xBBB`) |
| Summon | "Summon an Esper to fight at your side." (`0xBBD`) |
| Quickening | "Perform powerful attacks." (`0xBBE`) |
| Gambits | "Toggle character gambits ON/OFF." (`0xBBF`) |
| Dismiss | "Release a summoned Esper." (`0xBC1`) |
| Magicks & Technicks | "Use magicks and technicks." (`0xBC4`) |
| Mist | "Perform an action expending Mist Charges." (`0xBC5`) |
| the five schools | `0xBC7`-`0xBCB`, for example "Offensive magicks for dealing damage." |

### Input

The list widget reads the pressed word ([Controls](../Controls-And-Input/controls.md), `00277ACD`):

- Square closes the menu in every state (`00277ADE`-`00277B15`).
- Outside a target list, left and right step to the previous or next party member when more than one is in the party
  (`00277BFF`, `0027C280`).
- In a target list, L1 and R1 step the target category (`0027B430`, `0027C730`) among the tabs the manager allows.
- The row cursor, confirm and cancel come from the page's list, which posts `0x8000`, `0x8001` and `0x8002` to the list
  widget in the convention of [Dialogs](dialogs.md).

### Target tabs

The tab strip `0027C870` shows one tab per target list the action allows.
`00276960(tabs, actor, action, kind, show, mask, ...)` sets it up from the mask:

1. Mask bits 1, 2, 8 and 4 enable tabs 0 to 3, the strip's child nodes 2 to 5 (tables `00915BE0` and `00915BF0`,
   `00276A19`-`00276A60`).
2. Bit 8 is dropped when target list `0xF` has no row (`0027B090`), and bit 4 when list `0x1C` has none left after
   filtering (`0027AF80`).
3. A disabled tab's four corner alphas are set to 0; an enabled tab is placed at `0027B290(tabs, mask, i)` and fades
   in by `0x18` per call.
4. The strip is centred from its total width `0027B120`, and its side nodes 6 and 7 are shown only when two or more
   tabs are enabled (mask not 1, 2, 4 or 8).

The filter skips, for filter 1, rows with flag bit 1 and units whose status words hold KO, Stone or bit 31
(`00273710`, mask `0x80000003`), and for every filter units whose byte `+0x0A` (`002647E0`) has bit 2 (filter 0) or bit 0
(otherwise). `0027B5A0` and `0027B6C0` make the same two checks from a saved request when L1 or R1 is pressed
(`0027C730`), and `0027BB70` applies the filter to a page's rows in place, keeping the count at `+0x40`.

`0027DCA0` moves the strip half way towards its centred position, snapping when it is within 1. `00276830(tabs,
kind)` marks the tab of list kind `0x10`-`0x13`: the other tabs draw one palette further on.

### From a row to an action

Confirm (`0x8001`) runs the classifier `0027C3D0` (`0027841E`), which answers with what comes next:

| Row | Next |
|---|---|
| Attack | the foe list for action `0x96` (`0027C469`) |
| Items, Summon, Quickening, Magicks & Technicks, Mist, a school | that list |
| Gambits | switches the member's gambits on or off at once (`00311AF0`, `0027C512`) and closes |
| Dismiss | the Dismiss confirmation |
| an action | its target list, or the action at once when it needs no target choice |
| a greyed row | refused with sound 5 |

A new list of the same panel is rebuilt in place and pushed on the stack; a target list opens in a new panel. Cancel
pops the stack and closes the menu when it is empty (`002787AF`).

The action is issued through `00311CD0(actor, target, action, 0)` (`00278766`), or `00311B20` for a party-position
target (`0027869B`), which both reach `00311CF0` once ([Action phases](../Battle-Actions/action-phases.md)). The
menu never asks for the whole party (fan-out 0 at all six call sites). Dismiss asks "Dismiss {name}?"
(`menu_message.bin` `0x7D0`, `0027AA70`) and on Yes issues action `0x113` on the Esper (`0027AB01`).

### The help line

The help block is `[0209BE80] + 0x8FA0`, drawn in two alternating windows `002BF690`. `0027B880` fills it on each
cursor move:

- a command row shows its help;
- an action row shows the action's description;
- a greyed row shows its refusal first, through `0027C150`;
- a target row opens the target information window (`002C0870`) instead of text.

`0027C220(page, row)` picks the refusal: in a command list (page kind 6 to 10) a row with flag bit 1 gives its reason
byte `+4`, in an action list (kind 11) a row with flag bit 0 gives its byte `+6`; a positive reason with a row in
`0027C150` becomes that text (`0027C220`-`0027C27E`).

| Refusal | Text (`help_menu.bin`) |
|---:|---|
| `0x7` | "Stopped: Cannot take commands." (`0xC92`) |
| `0x8` | "Sleeping: Cannot take commands." (`0xC94`) |
| `0x9` | "Confused: Cannot take commands." (`0xC95`) |
| `0xA` | "Silenced: Cannot use magicks." (`0xC96`) |
| `0xB` | "Disabled: Cannot take commands." (`0xC93`) |
| `0xC` | "Berserk: Cannot take commands." (`0xC91`) |
| `0xE` | "Magicks forbidden: Cannot use magicks." (`0xC90`) |
| `0x16` | "You cannot attack here." (`0xC8A`) |
| `0x17` | "You cannot use magicks here." (`0xC8B`) |
| `0x18` | "You cannot use technicks here." (`0xC8D`) |
| `0x19` | "You cannot use items here." (`0xC8F`) |
| `0x1A`, `0x1B` | "You cannot summon here." (`0xC98`, `0xC99`) |

The window rises by `HelpMessageMoveY` (`002BF77A`) while the boss gauge is out of its compact state.

### The party list

The party list `0029BE50` (`0xB68` bytes, at `[0209BE80] + 0x10F78`) draws one slot `0029A0A0` per member from the
0xC0-byte party status records ([Party member status record](../Characters-And-Objects/party-member-status-record.md)):

| Element | Drawn by | From |
|---|---|---|
| name | `00297F60` | `+0x10` |
| HP | `00297D10` | `+0x20` |
| HP gauge | `00297E10` | HP against the larger of HP and `+0x28` |
| max HP | `00297E70` | `+0x24` |
| MP | `0029A8E0` | `+0x2C` |
| MP bars | `0029A930` | `+0x38` over `+0x87` bars; the first `+0x86` bars pulse, with sound `0x48` or `0x49` when that count changes |

The battle menu highlights the acting member's slot (`00296AF0`) and clears it (`00296B80`).

The menu finds members through the party status records at `0035BB20(i)`, `0x0C0` bytes each, with the handle at
`+0x04`:

- `00273320(handle)` returns the member's position, or -1, and `002737B0(handle)` whether it is in the party.
- `00272EE0(handle)` returns the record's type `+0x60`, or 6 when no record of the first four has the handle.
- `00273460()` returns the handle of the first record with flag bit 2, and `002734B0()` that record.
- `00273800(handle)` returns 1 when the member's record has flag bit 3 clear, that is, when it is in range.

### The boss gauge

The boss gauge `00405310` (manager `00406A60`, `02B62D88`) draws up to two bars from the table at `02EC1380`, which
`0031B690` fills every frame with HP and MP. Only `00328FF0` registers a unit there, always as entry 0
(`0023AA04`), with the class from the spawn row ([Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
The style is one bar for class 1 or 2 and style 2 for class 3 (`00405100`).

### Overhead HP gauges

`002C7660` gives each unit a gauge kind, 0 for a party member, 1 or 2 for other units, and `002C8310` draws it when
the unit's byte `+0x17` bit 1 and the HUD's bit are set. The step is `min(HP, max) x 100 / max >> 2`, 0 to 25
(`002C8398`-`002C83A1`); it picks the frame `00916F08[step]` and a colour between the kind's `Min` and `Max` keys
(`002C5F90`).

| Kind | Layout keys |
|---:|---|
| 0, party | `HpGaugeSide{Min,Max}_{R,G,B,A}` (`01E0CEF8`-`01E0CF14`) |
| `1` | `HpGaugeEnmey{Min,Max}_{R,G,B,A}` (`01E0CED8`-`01E0CEF4`) |
| `2` | `HpGaugeOther{Min,Max}_{R,G,B,A}` (`01E0CF18`-`01E0CF34`) |

### Layout keys

| Part | Keys |
|---|---|
| panel | `BattleMenuLRCursorMoveX` (`002776CB`) |
| list size | `BattleCommandGillTagOffset`, `BattleCommandNumTagWidth`, `BattleCommandScrollTableOffsetX`, `mCommandTitleFontHeight` (`0027DED0`) |
| list page | `mScrollListHeight` (`0027AE79`) |
| command rows | `mGambitPositionOffsetX/Y`, the ON/OFF mark on the Gambits row (`00276BE0`) |
| action rows | `BattleCommandNumPosX`, `BattleCommandMistPosX/Y`, `BattleMistCount0Offset`-`BattleMistCount3Offset`, `BattleMistIconWidth` (`0027CE70`) |
| help line | `HelpMessageMoveY`, `mHelpMessageFontCount` |
| boss gauge | `BossGaugeExColorR/G/B/A` (`0029EA58`-`0029EA6F`) |

The label widths come from a pre-pass, `00273E30`, which scene and action code runs (`00306760`, `00313550`,
`00313840`, `00254A90`) and which writes `022CA408`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16` | id | class `0x15` row, or class `0x18` school when flags bit 2 is set |
| `03` | `u8` | flags | bit 1 greyed, bit 2 school row, bit 3 greyed by `00318CD0` answer 2 |
| `04` | `u8` | reason | refusal shown through `0027C150` |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16` | id | action id (class `0x14`) |
| `02` | `u16` | cost | MP, Mist charges or item count |
| `04` | `u16` | flags | bit 0 greyed, bits 6-9 the targets the action needs |
| `06` | `u8` | reason | `002FFCF0` code from `00317BC0` |

## Modding notes

- The top command list is the six pairs at `00D10650`; reordering them reorders the menu.
- A command's label and help are words `+2` and `+0` of its battle command row.
- A new refusal reason needs a row in `0027C150` to show text.

## Related

- [Command availability](../Battle-Actions/command-availability.md) - which commands and actions are offered.
- [Target selection](../Battle-Actions/target-selection.md) - the target lists.
- [Action phases](../Battle-Actions/action-phases.md) - what happens after an action is issued.
- [Menus](menus.md) - the router ids that open the menu.
- [Gambits screen](gambit-screen.md) - the same on/off switch for a member's gambits.
