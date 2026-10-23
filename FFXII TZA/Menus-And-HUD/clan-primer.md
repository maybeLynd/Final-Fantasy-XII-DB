---
title: "Clan Primer: the Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages, how entries unlock, and the monster viewer"
kind: "system"
category: "Menus and HUD"
addresses: "0x00574CB0, 0x00574E80, 0x0056F810, 0x00571A50, 0x005701B0, 0x005771F0, 0x00577550, 0x001846F0"
---

## What the player sees

- Once "Clan Primer has been added to the Party Menu.", the Party Menu's Clan Primer command opens a list of
  categories: Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips.
- Each category lists entries; new ones carry a badge until they are read.
- A Bestiary entry shows the monster turning in a viewer that the stick rotates, with more of its text appearing as
  more of that monster are defeated.
- Sky Pirate's Den shows a statue for each title the clan has earned.

## How it works

### Opening

The Party Menu command is `0x4BC`, "Clan Primer" in `menu_command.bin`. The Party Menu's handler `0x00281ED0` closes
itself and calls the opener `0x00574CB0` (`0x0028239B`), which creates the back panel `0x00574E80` and publishes it at
`0x02CA9718`. The back panel builds the screen:

1. id 1 requests the background `HandBack_c.tm2` (kind-7 resource `0xCE`), `Hand_4_c.tm2` (`0xCD`) and
   `Party_Book.mrp` (`0xCC`), and installs the data manager `0x005771F0` (`0x00574FAE`).
2. id 14 sets the title, `0x002F9860(0x4BC)` (`0x00574E00`), and installs the category list `0x0056F810` (`0x00574D00`).
3. id 16 installs the mid pane `0x0056EF60`, which hosts the chosen category's pages.

A second opener, `0x00575580` (from `0x002814E0`), reopens the Clan Primer straight into Hunts from a 16-byte resume record
at `0x0209AC30 + 0x3E8`: it sets back-panel bit `0x40`, and `0x00574D00` then posts kind 6 to itself. On close
(`0x00575498`) the screen returns to the Party Menu through `0x002814E0(0x4BC)` unless back-panel bit `0x20` asks it to
leave without returning.

### Categories

`0x0056F810` builds its rows from the four 6-byte records at `0x00D23688`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | label | category label |
| `+0x02` | `u16` | help | help line |
| `+0x04` | `u8` | kind | page kind |
| `+0x05` | `u8` | b5 | 1, or 2 for Traveler's Tips |

The shipped records:

| Row | Category | Help | Kind | Shown when (`0x0056F750`) |
|---|---|---|---|---|
| `0` | Hunts (`0x1B5F`) | "Hunt information and progress." | `6` | the Hunts sync passes, story window 11 is open (`0x0032A8A0(0x400B)`, entry 11 of the story schedule `0x00377970`) and a hunt is listed |
| `1` | Bestiary (`0x1B5C`) | "Insights on foes you have defeated." | `5` | the Bestiary sync passes, story window 11 is open and an entry is unlocked |
| `2` | Sky Pirate's Den (`0x1B5D`) | "What will it take to fill the den?" | `7` | story window 11 is open |
| `3` | Traveler's Tips (`0x1B5E`) | "Hints for the wary adventurer." | `4` | the Traveler's Tips sync passes and an entry is unlocked |

The labels and help lines are in `penelosdiary` and `help_penelosdiary`. A row carries the new-entry badge when fewer
entries are read than unlocked (`0x0056FAD0`). Confirming posts the kind to the back panel, which hands it to the mid
pane (`0x00575480`, `0x0056F2A0`). Each page's title is `0x002F9860([0x00D236A0 + 6 x kind])`.

### Pages

The mid pane installs the page for the kind (`0x0056EE10`):

| Kind | Page | Data |
|---|---|---|
| 4 Traveler's Tips | family index `0x00571A50`, then the entry page `0x005701B0` | family `tutorial` |
| 5 Bestiary | the same, two columns, with the backdrop `HandBack2_c.tm2` (`0xD0`), the count pane `0x00570530` and the monster viewer | family `monster` |
| 6 Hunts | hunt list `0x00579AF0` | `menuquest.dat`, group 1 |
| 7 Sky Pirate's Den | `0x00572E10` | `menuhandbook_order.bin`, `Medal_c.tm2` (`0xCF`) |

Four more families, `story`, `world`, `person` and `knowledge`, ship with data, but their titles (`0x1B58`-`0x1B5B`) are
empty and no category row names them; the resume path posts only kind 6. That scope is the senders of the category
command read in `0x0056F810` and `0x00574D00`.

The family index lists rows of three types, blank, entry and group caption (`0x00571A50`, `0x00571710`, `0x00576A50`).
Confirming an entry opens the entry page through `0x0056EC10`. The cursor of each page is saved in bank 6 (`0x002527B0`).

`0x005742D0` is the content page under the entry page. `0x00570080` installs it (`0x005700EB`) as a `0x8068`-byte task
(`0x005700F6`) through `0x00244F50` (`0x00570116`) and passes no menu id. The Clan Primer's `menu_command.bin` id `0x4BC` is an
immediate at four sites in `.text`: the title call (`0x00574E18`), the return to the Party Menu (`0x005754EE`) and the
menu task `0x00281AE0` (`0x00281B1B`, and `0x00281C72`, which passes it to `0x002CD3C0`). The content page draws a frame
through `0x00573F40(page)` (`0x005746C5`) when its byte `+0x8060` is 2 or 5 and up and it has rows (`+0xE0`).

`0x00573F40` draws a box through `0x00392A00(+0x38, rect, ...)` with `0x002DD7E0(0xF6)` in all four colour slots, at
x = `[+0xE0] + 0x98` plus the layout's `+0x0C` - 8 and y = the layout's `+0x10` + 16, 8 x 8 wide, as high as
`min(+0x8063, rows) x the row height + 16`, where rows = `(word +0x9E - +0x13C - 1 + word +0x100) / word +0x100` of
`[+0xE0]` and the row height is `+0x0A` of the record `0x0020E600` gives for `[[[+0x60]]] + 0x0C`.

### The family index rows

`0x00571F60(page)` builds the index rows for the page's kind (`+0xE8`) after updating the unlocks (`0x00577550`). Each row
is a word at `+0xF0`: bits 0-3 the type (0 blank, 1 entry, 2 group caption), bits 4-13 the entry or group, bit 14 set
for an entry not fully read, bit 15 for the right column of the Bestiary's two. `0x00570930(page, entry)` appends an
entry row (the read test is `0x00576D20`). The Bestiary keeps its captions on the left by padding with blanks.

- `0x00571900` paints a row: a blank or caption row through `0x005722E0` and `0x005723C0` (which show or hide up to six and
  four of the row's nodes) and the caption's text (`0x00576A50`), an entry through `0x00571710` (`0x005760A0`).
- `0x005709E0(page, forward)` finds the first entry of the next group, or of the current group's start going back;
  `0x005713C0` jumps there on the buttons of mask `0xC50` (Traveler's Tips) or `0xCF0` (Bestiary), `0x400` back and
  `0x800` on, stepping the list (`0x002D3BA0`) until the cursor reaches it.
- `0x005715E0` runs one list step and reports when the cursor lands on an entry row.
- `0x00576D20(kind, entry)` answers whether an entry is fully read: the family's read bit (`0x003156E0`) or, for the
  Bestiary, every unlocked slot of the seven read (`0x00576E30`, `0x00315670`; the loop runs 0-7, and slot 7 is the
  mode marker `0x00576860` returns, not a text). `0x005779E0(kind)` marks a family seen
  (`0x00315B50` of `0x00D23750[kind]`).

### The entry page

- `0x00573BE0(page, n)` lays out page `n` of the entry's text from the text bundle (`0x005766B0`): for the Bestiary it
  splits off the title before code 3 (`0x002B39A0`), then breaks the text into lines (`0x002B5240`, `0x002B5390`), keeping
  each line's start, colour, width and flags at `+0x41E0`.
- `0x00574160` paints one text line into `+0x4120`, with the line's colour code first (`0x002AB870`) and right-aligned
  when its flag says so; `0x00574080` and `0x00574770` size the page from the layout.
- `0x0056FEA0` closes the entry page and its two panes, and `0x00577A00` records the current pane on the data manager.
- `0x00574A90(kind)` sets the current-entry pane's title, `0x002F9860([0x00D236A0 + 6 x kind])`.

### The back panel

- `0x0056ECC0(pane, event)` saves the page's place in bank 6 (`0x002527B0(6, 0x18, state)`, `0x00252610(6, [0x00D236A4 + 6 x
  kind], 1)`) when a page opens (7), closes (8, which also restores the title through `0x00574A90`), loses its help window
  (11, `0x002CCB10`) or ends (15).
- `0x0056F470` draws the clan rank (`0x00315390`, name `0x003153F0`) and the counter `0x003166F0(0x11)`, capped at 99,999,999.
- `0x005704A0` frees the back panel's help window `+0x110`; `0x005749B0` closes its pane `+0x100`; `0x005755D0(on)` shows
  or hides the atlases `icons_c` and `navi_Load`.

### Sky Pirate's Den

`0x00572BD0(page, direction)` picks the statue nearest the current one in a direction (0 up, 1 down, 2 left, 3 right),
by the distance `0x003BD6F0` weighted by `0x01F2CB50 + 16 x direction`; `0x005733F0` puts the cursor on it (`0x00368360`), and
`0x00572890` opens the statue's help window (`0x002CCCA0(0x00D236E0, 200)`, `0x002CD150(0x37)`).

### The hunt list

The hunt host `[0x02CA9748]` (`0x00579AF0`) shows two lists, open and cleared:

- `0x00579FA0(list)` counts the list's hunts from `0x0037E760(list, 4)`, `(list, 2)` and `(list, 0)`
  ([Quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md)); `0x005791B0(host, row)` gives a row's
  quest through `0x0037EAA0` and `0x0037E5B0`, counting cleared lists from the bottom.
- `0x005792F0` paints a row (`0x00577C30`), or "no hunts" `0x868`/`0x869` for an empty list; `0x00579230` gives a row's
  position, and `0x00577E10` slides the cursor marker there over 200 ms (`0x002468A0`).
- `0x005780D0(row)` selects a row and fills the detail pane (`0x00577C30`, `0x00D23888`); `0x00578860(host, list)` switches
  between the two lists; `0x005790D0` closes the panes.
- `0x00578120(text, parts)` splits a hunt text at code 2 and counts the parts.
- `0x00578F50` keeps the host's place at `+0x130`-`+0x13F` (the lists, rows and selection) and sets `+0xD0` bit 3.

### The data manager

`0x005771F0`, at `0x02CA9738`, loads what the pages show:

1. `0x00576F50` binds the six families' unlock tables, `menuhandbook_<family>.dat` (kind-7 id `[0x00D23740 + 2 x kind] + 1`),
   and `menuquest.dat` (`0x128`).
2. It runs three load slots (`0x00575870`), each loading kind-7 id `[0x00D23740 + 2 x kind]` plus an offset (`0x00575C30`):
   slot 0 the family catalog, slot 1 the entry's text bundle, slot 2 its picture bundle.
3. A text bundle may carry its own glyph sheet (an i32 at `+0x0C` other than -1). `0x00575710` registers the sheet
   (`0x0039BEC0`), and for Traveler's Tips and the Bestiary also registers it as a font (`0x0017FBC0(6)`; `0x0017FA90`,
   `0x0017F790`). The `story`, `world`, `person` and `knowledge` bundles carry a sheet in every language; the Bestiary
   and Traveler's Tips bundles carry one only in `kr`, `ch`, `cn` and `in`.
4. Slot 2 makes the entry's picture into the image label `hb_tex` (`0x00575B80`). The Traveler's Tips page never asks
   for a picture (`0x00575B80` skips kind 4), so its eight picture files ship unused.
5. A request to a busy slot waits in its queue (`0x00575A50`). Each slot reports to the back panel when its content is
   ready or freed.

The slots are at `+0x108`, `+0x110` and `+0x118` of `[0x02CA9738]`, each with a state byte `+0xC9` (1 ready, 2 and 3
busy):

- `0x005766B0` and `0x00576C70` return the text and picture bundles (`+0xF8`) of slots 1 and 2 when ready, and
  `0x005766E0(i)` the bundle word `+4` of catalog record `i` of slot 0; `0x00576DA0` answers whether any slot is busy.
- `0x00577880(entry)` asks slot 0 for a load (`0x00575A50`) unless the manager is closing (`+0x100` bit 6); `0x005776D0`
  cancels every slot (busy ones are marked 3, idle ones reset by `0x00575640`) and sets bit 6; `0x00575F10` releases every
  slot the same way and sets bit 3.
- `0x00575A10(slot)` frees a slot's content `+0xF8` (`0x0024A680`) and resets its id `+0xD0` to `0xFFFF`.
- `0x005777C0(manager)` tears down: it unregisters the glyph sheets (`0x002F83E0(7)`, `0x002F83E0(8)`) and frees the six
  bound tables and `+0xF8`.
- `0x005770A0(widget, v)` and `0x00577180` send message 16 to a widget, the latter after re-attaching it; `0x00577BD0` sends
  it to `[0x02CA9730]`.

A catalog record is 12 bytes (below), with text -1 for none (`0x00575D10`,
`0x005778F0`, `0x005760A0`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | text | entry text, -1 for none |
| `+0x04` | `u16` | group | group |
| `+0x06` | `u16` | bundle | text bundle |
| `+0x08` | `u16` | picturePage | picture page |
| `+0x0A` | `u8` | flag | flag |

### Unlocks

Per kind, `0x00576550` counts the unlocked entries, `0x00576920` the fully read ones, and `0x00577550(kind)` brings the unlock
state up to date.

#### Traveler's Tips and the other families

An entry's unlock bit is at save `+0x32CC` and its read bit at `+0x330C`, at the family's offset from `0x00D10630`
(`0x003154B0`, `0x003156E0`). `0x00577550` recomputes each unlock bit from the family's unlock record (`0x00575E80`, 8 bytes);
every field that is not all ones (`0xFF`, or `0xFFFF` for the words) must hold (`0x00575E8C`, `0x00575EA9`, `0x00575EC7`):

| Field | Test |
|---|---|
| `u8 a`, `u8 b` | `0x00315470(a) == b` |
| `u8 c` | `0x00315620(c) != 0` |
| `u16 +4` | story flag `0x0032A8A0(flag)` |
| `u16 +6` | the story counter (`0x00265270`) >= value |

#### Bestiary

A monster's entry unlocks by a rule in `menuhandbook.bin` section 1 (`0x003154B0(6, i)`): rule type 0 unlocks it at a story
counter value, type 1 when another monster has been defeated, and with no rule when this monster has been defeated
(kill count at save `+0x3404 + i`, `0x00315420`).

Each entry has seven text slots, whose unlock is worked out each time the entry is shown and never saved (`0x00576E30`). The unlock record is
16 bytes, seven `u16` values and a mode word at `+0x0E` (`0x00576860`):

| Mode | A slot unlocks when |
|---|---|
| `0` | this monster's kill count reaches the slot's value |
| `1` | the story counter reaches the slot's value |
| `2` | this monster or the monster the slot names has been defeated |

The read marks are save `+0x3604 + i`, one bit per slot (`0x00315670`, `0x00315AD0`). `0x00577550(5)` sets the marks of empty
slots, so an entry counts as read when every unlocked slot has been viewed. The entry shows the kill count (`0x005760A0`).

#### Hunts

`menuquest.dat` holds 8-byte records (below); group 1 (`key & 0xFF`) is the 45 hunts, quest ids `0x80`-`0xAC`.
A hunt is listed when `0x0046B1A0(quest)` or `0x0046B240(quest)` is true (`0x00576550(6)`), and read marks are at save
`+0x33F4`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | text | title text id |
| `+0x04` | `u32` | key | group in bits 0-7, quest id in bits 8-17 |

#### Sky Pirate's Den

A statue is awarded by bit `i` at save `+0x3844` and read at `+0x3848` (`0x003154B0(7, i)`). The back panel re-checks the
awards with `0x00577550(7)` (`0x005750AF`, `0x00316930`). `0x00572920` lays out one group per awarded statue from
`menuhandbook_order.bin`.

### The monster viewer

1. The entry page passes the Bestiary entry number to `0x001846F0` (`0x0057025A`), which saves and clears `0x02CB8138` and
   calls `0x001EB7B0`.
2. `0x001EB9C0` reads entry `MonsterId<n>` of `monstergallery.json` through `0x001C6320` and, for a new model, requests it with
   `0x002EE9C0` (`0x001EBA05`).
3. The loader `0x002EE430` loads the body, then weapon 0 and weapon 1, then the motion set chosen by weapon 0
   (`0x003203B0`), and marks each part's render record `+0x6E0 = 1`.
4. Each frame, `0x001EC060` turns the model from the stick (`0x00249860`, `0x00249880`): the yaw wraps from 0 to 360 and the
   pitch stays between -15 and 30 degrees. It turns vectors with `0x001EB3D0`, a vector times the upper 3 x 3 of a
   matrix (`0x001EC3DC`).
5. `0x00477F20` draws a record with `+0x6E0` set only in frame mode 3 (`0x00229EA0`), and every other record only outside
   it, so the model appears only in the menu.
6. Closing the entry (`0x001846B0`, `0x00570355`) frees the model and restores `0x02CB8138`.

The loader settles a request with `0x002EED80` (`0x002EE975`), only on a pass where `0x0216420C` is 1, which it clears:

- with a model shown (`0x0216423C` = 1) and `0x00181DD0()` answering 0, it releases it (`0x002EEB20([0x02164238])`) and clears
  the request flag `0x02164208`;
- with a request (`0x02164208` = 1) for another model (`0x02164240` not equal to `0x02164210`), it releases the shown one,
  copies the request (`0x02164240`-`0x0216426C`) over the current values (`0x02164210`-`0x0216423C`), sets `0x01EEBAA8` to 0 and
  clears the flag;
- otherwise, with a model shown, it calls `0x00181DF0` with entry `[0x02164238]` of `0x01EEBAB0`.

The viewer is the `0x2E0`-byte object `[0x01F82E18]`, built on first use by `0x001EBA40`. When the entry page opens it,
`0x00181D50` and `0x00181D80` take two screen-sized render targets from the pool `[0x01F81210]` (`0x00182BE0(1.0, 1.0)`)
into viewer `+0x270` and `+0x278` (`0x0057025F`, `0x00570264`); `0x00181B90` and `0x00181BD0` hand them back when it
closes (`0x0057032C`, `0x00570350`).

`0x001C6320` passes the entry's keys on to the viewer:

- `monsterWeaponIndex` and `monsterWeaponIndex2` to `0x001EBBF0` as weapons 0 and 1: the index goes to
  `+0x124 + 4 x slot` and the count `slot + 1` to `+0x12C`, or the count is 0 when the index is 0;
- `motionIndex` to `0x001EBC20`, which keeps it modulo 80 at `+0x224`;
- `cameraFov` to `0x001EBA90` (`+0x250`, `+0x110`);
- the ambient light and the two lights, colours and directions, in one `0xD0`-byte block to `0x001EBB70`, which copies
  it to `+0x144` (`0x001C694D`);
- `eyeVfxZBias` (`0x008FB498`) to `0x002F1690` (`0x001C659B`), which stores the value less 1000.0 at `0x022BDEBC`.

## Layouts

### The back panel's fields

The back panel is the `0x130`-byte widget with procedure `0x00574E80` that publishes itself at `0x02CA9718` (Opening above).

```struct PrimerBackPanel base=record size=0x130
+0x00    u8[192]         header                 the widget header, written by the constructor 0x002465F0 (Widgets, The
                                                header); procedure 0x00574E80
+0xC0    u32             flags                  0 on construction, 0x40 when the creation record carries a resume
                                                record (0x00574F2A-0x00574F3C). Bit 0: the screen has opened, once the mid
                                                pane exists (bit 1) and the data manager has loaded (bit 2)
                                                (0x00575038-0x005750B4). Bit 1: the mid pane +0xF8 is built (0x0057502A).
                                                Bit 2: the data manager reported 1 (message 16 with 1, 0x00574FE5). Bit
                                                3: the data manager reported 2, it is gone (0x00574FDC); the tick then
                                                closes the panel and sets bit 4 (0x00575144-0x0057516F). Bit 5: leave
                                                without returning to the Party Menu: set by the mid pane on its
                                                command 0xE with 0x12 (0x0056F0AC); children are then destroyed outright
                                                (0x00575244, 0x00575267, 0x0057533B, 0x005749C7, 0x00574A3E, 0x0056F176) and the
                                                release continues at 0x00579AE0 instead of 0x002814E0(0x4BC)
                                                (0x005754C8-0x005754EE). Bit 6: open straight into Hunts: 0x00574D00 posts
                                                kind 6 (0x00574D92), the opening skips 0x002CC960 (0x00575065), 0x0056EE10
                                                builds the hunt list from +0xC8 (0x0056EEC2); the mid pane clears it
                                                after its first pass (0x0056F048-0x0056F059)
+0xC4    u8              kind                   the category kind posted by command 0x8001 (0x00575424-0x00575428): 4
                                                Traveler's Tips, 5 Bestiary, 6 Hunts, 7 Sky Pirate's Den; handed to
                                                the mid pane with 0x0056F2A0 (0x00575456-0x00575480)
+0xC5    u8[3]           gap0C5                 read and written by no function; nothing fixes its width
+0xC8    u8[16]          resumeRecord           the 16-byte resume record the creation record points to, copied whole
                                                (0x00574F39-0x00574F46); 0x00575580 passes 0x0209AC30 + 0x3E8. With bit 6 set,
                                                0x0056EE10 hands it to 0x00579A40 (0x0056EEC2-0x0056EED2), which builds the
                                                hunt list 0x00579AF0 from its dwords +0x00 and +0x04, byte +0x08, bits
                                                11-18 of the dword +0x08 and bytes +0x0C-+0x0F (0x00579A71-0x00579AB1)
+0xD8    ptr             categoryList           the 0x178-byte category list with procedure 0x0056F810 that 0x00574D00
                                                builds from Party_Book.mrp (0x00574D4E) and opens under its parent
                                                unless bit 6 is set (0x00574DB0); opened again by command 0xF with 6
                                                (0x005752F3); asked to close by command 0x8002 with 3 (0x005753FC) and by
                                                destroy; cleared by command 0x12 with 3 (0x0057523D); 0 on construction
                                                (0x00574EF2)
+0xE0    ptr             sidePane               the 0xD0-byte pane with procedure 0x0056F550 that 0x00574D00 builds beside
                                                the category list (0x00574D84); opened, closed and cleared with it
                                                (0x00574DC6, 0x00575309, 0x00575408, 0x0057544A); cleared by command 0x12 with
                                                4 (0x0057521F); 0 on construction (0x00574EF9)
+0xE8    ptr             pane570890             the 0xC8-byte widget with procedure 0x00570890 built from Party_Book.mrp
                                                on message 14 (0x005750E3-0x00575102); cleared by command 0x12 with 2,
                                                which closes the mid pane once +0xF0 is gone as well
                                                (0x00575292-0x005752AF); closed by command 0x12 with 3 (0x00575236); the Sky
                                                Pirate's Den page and 0x005738D0 read it (0x00572FBF, 0x00573323, 0x00573911);
                                                0 on construction (0x00574F00)
+0xF0    ptr             pane56EA40             the 0xD8-byte widget with procedure 0x0056EA40 built on message 14 with
                                                the image labels +0x118 (0x0057510E-0x00575136); cleared by command 0x12
                                                with 5, which closes the mid pane once +0xE8 is gone
                                                (0x005751EE-0x00575211); closed by command 0x12 with 3 (0x00575260); read by
                                                0x00572E10 (0x00573043, 0x00573350); 0 on construction (0x00574F07)
+0xF8    ptr             midPane                the 0x100-byte mid pane with procedure 0x0056EF60 that hosts the
                                                category's pages, built when the panel's pictures have loaded
                                                (0x00575009-0x00575031); given the kind by command 0x8001
                                                (0x0057545D-0x00575480) and passed to 0x002CD800 when the screen opens
                                                (0x00575094); cleared by command 0x12 with 6, which releases the data
                                                manager through 0x00575F10 (0x005751D9-0x005751E2); read by 0x00572E10 and
                                                0x005738D0 (0x00573270, 0x0057392B); 0 on construction (0x00574F0E)
+0x100   ptr             titleWidget            the 0xD8-byte title widget 0x00574AD0 that 0x00574A00(text) builds; it
                                                shows the text through list record 0x1A of Party_Book.mrp and stores
                                                itself here (0x00574B35). 0x00574A00, 0x005749B0, the mid pane and command
                                                0xF with 3 close it and clear this (0x00574A32-0x00574A5A,
                                                0x005749BB-0x005749E3, 0x0056F166-0x0056F194, 0x0057532F-0x00575357); 0x00574BA0,
                                                0x005701B0 and 0x00572E10 read it; 0 on construction (0x00574F15)
+0x108   ptr             rankPane               the 0xC0-byte clan rank pane with procedure 0x0056F410, which draws the
                                                rank through 0x0056F470: built by 0x00574E00 while this is 0
                                                (0x00574E2C-0x00574E63) and by command 0xE with 3 through 0x0056F3C0
                                                (0x0057538C-0x005753A2), which opens it (0x005753A9); command 0xF with 3
                                                closes it and clears this (0x0057535E-0x00575375); 0 on construction
                                                (0x00574F1C)
+0x110   ptr             helpWindow             the help window that 0x005704E0, 0x00572890 and 0x00573980 open with
                                                0x002CCCA0 while it is 0 (0x0057050A, 0x005728C7, 0x00573AD1); 0x005704A0 frees
                                                it (0x005704C1) and 0x0056ECC0 closes it with 0x002CCB10 when a page loses
                                                its help window (0x0056ED07-0x0056ED1C), each clearing this; read by
                                                0x005738D0 (0x005738F3); 0 on construction (0x00574F23)
+0x118   ptr             imageLabel0            the image label of HandBack_c.tm2 (kind-7 resource 0xCE), registered
                                                with +0x120 by 0x003934F0 from the table 0x00D23628 when the panel is
                                                built (0x00574F55-0x00574F78) and released by 0x00393900 on destroy
                                                (0x00575498-0x005754A4, 0x00393920); the pane 0x0056EA40 gets the address of
                                                the pair (0x0057510E)
+0x120   ptr             imageLabel1            the image label of Hand_4_c.tm2 (0xCD), the second of the pair
                                                0x003934F0 registers and 0x00393900 releases (0x00393920)
+0x128   ptr             listFile               Party_Book.mrp (kind-7 resource 0xCC), requested by 0x003933F0
                                                (0x00574F7D-0x00574F94, 0x00393431) and released by 0x003938B0 on destroy
                                                (0x005754A9-0x005754B5, 0x003938D0-0x003938DD); the panes take its low 32 bits
                                                as their list file (0x00574D19, 0x00574D5A, 0x00574E36, 0x005750D2, 0x00575396)
                                                and 0x00574AD0 and 0x00574BA0 read it (0x00574B01, 0x00574C4F)
```

### The data manager's fields

The data manager is the `0x120`-byte widget at `0x02CA9738` with procedure `0x005771F0` (The data manager above).

```struct PrimerDataManager base=record size=0x120
+0x00    u8[192]         header                 the widget header, written by the constructor 0x002465F0 (Widgets, The
                                                header); procedure 0x005771F0
+0xC0    ptr             listener               the widget the manager reports to through 0x005770A0 (message 16 with a
                                                value): the creation record's +0x08 (0x0057725A-0x0057725E), replaced by
                                                0x00577A00 (0x00577A0C). Values: 1 when nothing was left to load or the
                                                load finished (0x00577180), 4, 5 and 6 when slot 0, 1 or 2 has its
                                                content (0x005773DD-0x0057740A), 10 when a cancel has finished
                                                (0x00577449-0x00577455), 2 when the manager is destroyed (0x005774B7)
+0xC8    ptr             unlockTable0           the unlock table of kind 0, kind-7 resource 0x229 ([0x00D23740] + 1),
                                                bound by 0x00576F50 when +0x100 bit 2 is set (0x00577010-0x00577038);
                                                0x00577550 reads the table of its kind at +0xC8 + 8 x kind (0x00577660);
                                                freed and cleared by 0x005777C0 (0x00577826-0x00577833); 0 on construction
                                                (0x00577221)
+0xD0    ptr             unlockTable1           the unlock table of kind 1, kind-7 resource 0x295 (0x00D23742 + 1),
                                                bound, read and freed as +0xC8 (0x00577038, 0x00577660, 0x00577833); 0 on
                                                construction (0x0057722A)
+0xD8    ptr             unlockTable2           the unlock table of kind 2, kind-7 resource 0x2CD (0x00D23744 + 1),
                                                bound, read and freed as +0xC8 (0x00577038, 0x00577660, 0x00577833); 0 on
                                                construction (0x00577231)
+0xE0    ptr             unlockTable3           the unlock table of kind 3, kind-7 resource 0x2F5 (0x00D23746 + 1),
                                                bound, read and freed as +0xC8 (0x00577038, 0x00577660, 0x00577833); 0 on
                                                construction (0x00577238)
+0xE8    ptr             unlockTable4           the unlock table of kind 4, Traveler's Tips, kind-7 resource 0x31D
                                                (0x00D23748 + 1), bound, read and freed as +0xC8 (0x00577038, 0x00577660,
                                                0x00577833); 0 on construction (0x0057723F)
+0xF0    ptr             unlockTable5           the Bestiary's unlock table, kind 5, kind-7 resource 0x355 (0x00D2374A +
                                                1), 16-byte records from +0x0C: seven slot values and the mode
                                                word +0x0E that 0x00576860 and 0x005768E0 read (0x00576870, 0x005768EA); bound,
                                                read by 0x00577550 (0x005775C1) and freed as +0xC8; 0 on construction
                                                (0x00577246)
+0xF8    ptr             questTable             menuquest.dat, kind-7 resource 0x128, bound by 0x00576F50 with the six
                                                tables (0x00577041-0x0057707B); the hunt counters 0x00576550, 0x00576920 and
                                                0x00576CA0 read it (0x00576623, 0x00576677, 0x005769BB, 0x00576CD6); freed and
                                                cleared by 0x005777C0 (0x00577847-0x00577862); 0 on construction (0x00577253)
+0x100   u32             flags                  bit 0: the opening run has started (message 14 deactivates the manager
                                                and sets it, 0x005772FC-0x00577306); loads finishing afterwards are not
                                                reported (0x005772D7). Bit 1: the tables are loading: set when they are
                                                requested (0x0057706F), cleared when the batch arrives (0x005772E3);
                                                0x00576550, 0x00576920, 0x00576CA0 and 0x00577550 answer 0 while it is set
                                                (0x0057661A, 0x005769B2, 0x00576CCD, 0x00577567). Bit 2: bind the tables, set
                                                from a non-zero first byte of the creation record (0x00577265-0x0057727D);
                                                0x005777C0 frees them and clears it (0x00577800-0x00577840). Bits 4 and 5:
                                                glyph sheet 7 or 8 was missing and is loaded and later released by the
                                                manager (0x00576F67, 0x00576F7C, 0x005777CF-0x005777F9). Bit 3: release
                                                requested by 0x00575F10 (0x00575F24); the tick then tears down and closes
                                                once the three slots are gone (0x00577315-0x0057736D). Bit 6: cancelling,
                                                set by 0x005776D0 (0x005776F5), which refuses new loads in 0x00577880
                                                (0x00577893) and 0x005778F0 (0x0057790D); cleared after report 10
                                                (0x0057745A). Bits 7-9: slot 0, 1 or 2 is idle after a cancel (command
                                                0x10 with 3, 4 or 5, 0x00577411-0x00577429; 0x005776D0 clears all three); a
                                                load request to the slot clears its bit (0x005778B2, 0x00575D8B, 0x00575E2C)
+0x104   u8[4]           gap104                 read and written by no function; nothing fixes its width
+0x108   ptr             slot0                  load slot 0, the family catalog, built by 0x00575810(0, manager)
                                                (0x0057728B); 0 when the slot reports itself freed (command 0x12 with 0,
                                                0x005774A8); read by 0x005771F0 (0x005773A2), 0x00575D10, 0x00575DD0, 0x00575F10,
                                                0x00576030, 0x005760A0, 0x00576300, 0x005766E0, 0x00576740, 0x00576A50, 0x00576DA0,
                                                0x005776D0, 0x00577880 and 0x005778F0
+0x110   ptr             slot1                  load slot 1, the entry's text bundle, built by 0x00575810(1, manager)
                                                (0x0057729C); 0 when it reports itself freed (0x00577497); read by
                                                0x00575D10, 0x00575F10, 0x00576300, 0x005766B0, 0x00576DA0, 0x005776D0 and
                                                0x00577A40
+0x118   ptr             slot2                  load slot 2, the entry's picture bundle, built by 0x00575810(2, manager)
                                                (0x005772AD); 0 when it reports itself freed (0x00577486); when slot 0's
                                                catalog is ready the manager sets its +0xCA to the catalog's
                                                word +0x14 plus 2 (0x005773CB-0x005773D6); read by 0x00575DD0, 0x00575F10,
                                                0x00576C70, 0x00576DA0 and 0x005776D0
```

## Shipped data

| Family | Entries | Groups | Unlock limit (`0x00D23758`) |
|---|---:|---:|---:|
| Traveler's Tips (`tutorial`) | 16 | 4 | 56 |
| Bestiary (`monster`) | 384 | 32 | 512 |
| `story` | 69 | 4 | 160 |
| `world` | 74 | 10 | 96 |
| `person` | 57 | 4 | 64 |
| `knowledge` | 100 | 7 | 120 |

- Bestiary slot modes: 370 entries by kill count, 13 by story counter and 1 by another monster. 192 picture files
  serve the 384 entries, and `monstergallery.json` has 384 entries.
- Hunts: 45 of a limit of 48. Sky Pirate's Den: 30 statues, Balthier to Zodiark (`penelosdiary` `0x1B68`-`0x1B85`).
- The kind-7 path table at `0x01EC73A0` names the `in` copies of `menuhandbook.bin` and `menuhandbook_order.bin` for
  `0xC8` and `0xC9`; no `us` path for either is in the image. That `menuhandbook.bin` holds 15 Bestiary rules.

## Modding notes

- An entry's unlock conditions are its record in `menuhandbook_<family>.dat`; a Bestiary slot's threshold is one of the
  seven values of the monster's record.
- Changing one of the four records at `0x00D23688` to kind 0-3 would show one of the four unused families, whose data
  ships; that row position's other tests still apply. A fifth record is never read (`0x0056F7EA`).
- The monster shown for an entry is its `MonsterId` record in `monstergallery.json`.

## Related

- [Menus](menus.md) - the Party Menu that opens the Clan Primer.
- [Story progress](../Story-Events-And-Hunts/story-progress.md) - the story counter and windows the unlocks read.
- [Quests](../Story-Events-And-Hunts/quests.md) - the hunts.
- [Hunts](../Story-Events-And-Hunts/hunts.md) - every hunt's name, petitioner and record text as the Hunts page shows them.
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) - where kill counts are kept.
