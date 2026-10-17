---
title: "Clan Primer: the Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages, how entries unlock, and the monster viewer"
kind: "system"
category: "Menus and HUD"
addresses: "00574CB0, 00574E80, 0056F810, 00571A50, 005701B0, 005771F0, 00577550, 001846F0"
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

The Party Menu command is `4BC`<sub>h</sub>, "Clan Primer" in `menu_command.bin`. The Party Menu's handler `00281ED0` closes
itself and calls the opener `00574CB0` (`0028239B`), which creates the back panel `00574E80` and publishes it at
`02CA9718`. The back panel builds the screen:

1. id 1 requests the background `HandBack_c.tm2` (kind-7 resource `CE`<sub>h</sub>), `Hand_4_c.tm2` (`CD`<sub>h</sub>) and
   `Party_Book.mrp` (`CC`<sub>h</sub>), and installs the data manager `005771F0` (`00574FAE`).
2. id 14 sets the title, `002F9860(4BCh)` (`00574E00`), and installs the category list `0056F810` (`00574D00`).
3. id 16 installs the mid pane `0056EF60`, which hosts the chosen category's pages.

A second opener, `00575580` (from `002814E0`), reopens the Clan Primer straight into Hunts from a 16-byte resume record
at `0209AC30 + 3E8h`: it sets back-panel bit `40`<sub>h</sub>, and `00574D00` then posts kind 6 to itself. On close
(`00575498`) the screen returns to the Party Menu through `002814E0(4BCh)` unless back-panel bit `20`<sub>h</sub> asks it to
leave without returning.

### Categories

`0056F810` builds its rows from the four 6-byte records at `00D23688`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | label | category label |
| `02`<sub>h</sub> | `u16` | help | help line |
| `04`<sub>h</sub> | `u8` | kind | page kind |
| `05`<sub>h</sub> | `u8` | b5 | 1, or 2 for Traveler's Tips |

The shipped records:

| Row | Category | Help | Kind | Shown when (`0056F750`) |
|---|---|---|---|---|
| `0` | Hunts (`1B5F`<sub>h</sub>) | "Hunt information and progress." | `6` | the Hunts sync passes, story window 11 is open (`0032A8A0(400Bh)`, entry 11 of the story schedule `00377970`) and a hunt is listed |
| `1` | Bestiary (`1B5C`<sub>h</sub>) | "Insights on foes you have defeated." | `5` | the Bestiary sync passes, story window 11 is open and an entry is unlocked |
| `2` | Sky Pirate's Den (`1B5D`<sub>h</sub>) | "What will it take to fill the den?" | `7` | story window 11 is open |
| `3` | Traveler's Tips (`1B5E`<sub>h</sub>) | "Hints for the wary adventurer." | `4` | the Traveler's Tips sync passes and an entry is unlocked |

The labels and help lines are in `penelosdiary` and `help_penelosdiary`. A row carries the new-entry badge when fewer
entries are read than unlocked (`0056FAD0`). Confirming posts the kind to the back panel, which hands it to the mid
pane (`00575480`, `0056F2A0`). Each page's title is `002F9860([00D236A0 + 6 x kind])`.

### Pages

The mid pane installs the page for the kind (`0056EE10`):

| Kind | Page | Data |
|---|---|---|
| 4 Traveler's Tips | family index `00571A50`, then the entry page `005701B0` | family `tutorial` |
| 5 Bestiary | the same, two columns, with the backdrop `HandBack2_c.tm2` (`D0`<sub>h</sub>), the count pane `00570530` and the monster viewer | family `monster` |
| 6 Hunts | hunt list `00579AF0` | `menuquest.dat`, group 1 |
| 7 Sky Pirate's Den | `00572E10` | `menuhandbook_order.bin`, `Medal_c.tm2` (`CF`<sub>h</sub>) |

Four more families, `story`, `world`, `person` and `knowledge`, ship with data, but their titles (`1B58`<sub>h</sub>-`1B5B`<sub>h</sub>) are
empty and no category row names them; the resume path posts only kind 6. That scope is the senders of the category
command read in `0056F810` and `00574D00`.

The family index lists rows of three types, blank, entry and group caption (`00571A50`, `00571710`, `00576A50`).
Confirming an entry opens the entry page through `0056EC10`. The cursor of each page is saved in bank 6 (`002527B0`).

### The family index rows

`00571F60(page)` builds the index rows for the page's kind (`+E8`<sub>h</sub>) after updating the unlocks (`00577550`). Each row
is a word at `+F0`<sub>h</sub>: bits 0-3 the type (0 blank, 1 entry, 2 group caption), bits 4-13 the entry or group, bit 14 set
for an entry not fully read, bit 15 for the right column of the Bestiary's two. `00570930(page, entry)` appends an
entry row (the read test is `00576D20`). The Bestiary keeps its captions on the left by padding with blanks.

- `00571900` paints a row: a blank or caption row through `005722E0` and `005723C0` (which show or hide up to six and
  four of the row's nodes) and the caption's text (`00576A50`), an entry through `00571710` (`005760A0`).
- `005709E0(page, forward)` finds the first entry of the next group, or of the current group's start going back;
  `005713C0` jumps there on the buttons of mask `C50`<sub>h</sub> (Traveler's Tips) or `CF0`<sub>h</sub> (Bestiary), `400`<sub>h</sub> back and
  `800`<sub>h</sub> on, stepping the list (`002D3BA0`) until the cursor reaches it.
- `005715E0` runs one list step and reports when the cursor lands on an entry row.
- `00576D20(kind, entry)` answers whether an entry is fully read: the family's read bit (`003156E0`) or, for the
  Bestiary, every unlocked slot of the seven read (`00576E30`, `00315670`; the loop runs 0-7, and slot 7 is the
  mode marker `00576860` returns, not a text). `005779E0(kind)` marks a family seen
  (`00315B50` of `00D23750[kind]`).

### The entry page

- `00573BE0(page, n)` lays out page `n` of the entry's text from the text bundle (`005766B0`): for the Bestiary it
  splits off the title before code 3 (`002B39A0`), then breaks the text into lines (`002B5240`, `002B5390`), keeping
  each line's start, colour, width and flags at `+41E0`<sub>h</sub>.
- `00574160` paints one text line into `+4120`<sub>h</sub>, with the line's colour code first (`002AB870`) and right-aligned
  when its flag says so; `00574080` and `00574770` size the page from the layout.
- `0056FEA0` closes the entry page and its two panes, and `00577A00` records the current pane on the data manager.
- `00574A90(kind)` sets the current-entry pane's title, `002F9860([00D236A0 + 6 x kind])`.

### The back panel

- `0056ECC0(pane, event)` saves the page's place in bank 6 (`002527B0(6, 18h, state)`, `00252610(6, [00D236A4 + 6 x
  kind], 1)`) when a page opens (7), closes (8, which also restores the title through `00574A90`), loses its help window
  (11, `002CCB10`) or ends (15).
- `0056F470` draws the clan rank (`00315390`, name `003153F0`) and the counter `003166F0(11h)`, capped at 99,999,999.
- `005704A0` frees the back panel's help window `+110`<sub>h</sub>; `005749B0` closes its pane `+100`<sub>h</sub>; `005755D0(on)` shows
  or hides the atlases `icons_c` and `navi_Load`.

### Sky Pirate's Den

`00572BD0(page, direction)` picks the statue nearest the current one in a direction (0 up, 1 down, 2 left, 3 right),
by the distance `003BD6F0` weighted by `01F2CB50 + 16 x direction`; `005733F0` puts the cursor on it (`00368360`), and
`00572890` opens the statue's help window (`002CCCA0(00D236E0, 200)`, `002CD150(37h)`).

### The hunt list

The hunt host `[02CA9748]` (`00579AF0`) shows two lists, open and cleared:

- `00579FA0(list)` counts the list's hunts from `0037E760(list, 4)`, `(list, 2)` and `(list, 0)`
  ([Quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md)); `005791B0(host, row)` gives a row's
  quest through `0037EAA0` and `0037E5B0`, counting cleared lists from the bottom.
- `005792F0` paints a row (`00577C30`), or "no hunts" `868`<sub>h</sub>/`869`<sub>h</sub> for an empty list; `00579230` gives a row's
  position, and `00577E10` slides the cursor marker there over 200 ms (`002468A0`).
- `005780D0(row)` selects a row and fills the detail pane (`00577C30`, `00D23888`); `00578860(host, list)` switches
  between the two lists; `005790D0` closes the panes.
- `00578120(text, parts)` splits a hunt text at code 2 and counts the parts.
- `00578F50` keeps the host's place at `+130`<sub>h</sub>-`+13F`<sub>h</sub> (the lists, rows and selection) and sets `+D0`<sub>h</sub> bit 3.

### The data manager

`005771F0`, at `02CA9738`, loads what the pages show:

1. `00576F50` binds the six families' unlock tables, `menuhandbook_<family>.dat` (kind-7 id `[00D23740 + 2 x kind] + 1`),
   and `menuquest.dat` (`128`<sub>h</sub>).
2. It runs three load slots (`00575870`), each loading kind-7 id `[00D23740 + 2 x kind]` plus an offset (`00575C30`):
   slot 0 the family catalog, slot 1 the entry's text bundle, slot 2 its picture bundle.
3. A text bundle may carry its own glyph sheet (an i32 at `+0C`<sub>h</sub> other than -1). `00575710` registers the sheet
   (`0039BEC0`), and for Traveler's Tips and the Bestiary also registers it as a font (`0017FBC0(6)`; `0017FA90`,
   `0017F790`). The `story`, `world`, `person` and `knowledge` bundles carry a sheet in every language; the Bestiary
   and Traveler's Tips bundles carry one only in `kr`, `ch`, `cn` and `in`.
4. Slot 2 makes the entry's picture into the image label `hb_tex` (`00575B80`). The Traveler's Tips page never asks
   for a picture (`00575B80` skips kind 4), so its eight picture files ship unused.
5. A request to a busy slot waits in its queue (`00575A50`). Each slot reports to the back panel when its content is
   ready or freed.

The slots are at `+108`<sub>h</sub>, `+110`<sub>h</sub> and `+118`<sub>h</sub> of `[02CA9738]`, each with a state byte `+C9`<sub>h</sub> (1 ready, 2 and 3
busy):

- `005766B0` and `00576C70` return the text and picture bundles (`+F8`<sub>h</sub>) of slots 1 and 2 when ready, and
  `005766E0(i)` the bundle word `+4` of catalog record `i` of slot 0; `00576DA0` answers whether any slot is busy.
- `00577880(entry)` asks slot 0 for a load (`00575A50`) unless the manager is closing (`+100`<sub>h</sub> bit 6); `005776D0`
  cancels every slot (busy ones are marked 3, idle ones reset by `00575640`) and sets bit 6; `00575F10` releases every
  slot the same way and sets bit 3.
- `00575A10(slot)` frees a slot's content `+F8`<sub>h</sub> (`0024A680`) and resets its id `+D0`<sub>h</sub> to `FFFF`<sub>h</sub>.
- `005777C0(manager)` tears down: it unregisters the glyph sheets (`002F83E0(7)`, `002F83E0(8)`) and frees the six
  bound tables and `+F8`<sub>h</sub>.
- `005770A0(widget, v)` and `00577180` send message 16 to a widget, the latter after re-attaching it; `00577BD0` sends
  it to `[02CA9730]`.

A catalog record is 12 bytes (below), with text -1 for none (`00575D10`,
`005778F0`, `005760A0`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | text | entry text, -1 for none |
| `04`<sub>h</sub> | `u16` | group | group |
| `06`<sub>h</sub> | `u16` | bundle | text bundle |
| `08`<sub>h</sub> | `u16` | picturePage | picture page |
| `0A`<sub>h</sub> | `u8` | flag | flag |

### Unlocks

Per kind, `00576550` counts the unlocked entries, `00576920` the fully read ones, and `00577550(kind)` brings the unlock
state up to date.

#### Traveler's Tips and the other families

An entry's unlock bit is at save `+32CC`<sub>h</sub> and its read bit at `+330C`<sub>h</sub>, at the family's offset from `00D10630`
(`003154B0`, `003156E0`). `00577550` recomputes each unlock bit from the family's unlock record (`00575E80`, 8 bytes);
every field that is not all ones (`FF`<sub>h</sub>, or `FFFF`<sub>h</sub> for the words) must hold (`00575E8C`, `00575EA9`, `00575EC7`):

| Field | Test |
|---|---|
| `u8 a`, `u8 b` | `00315470(a) == b` |
| `u8 c` | `00315620(c) != 0` |
| `u16 +4` | story flag `0032A8A0(flag)` |
| `u16 +6` | the story counter (`00265270`) >= value |

#### Bestiary

A monster's entry unlocks by a rule in `menuhandbook.bin` section 1 (`003154B0(6, i)`): rule type 0 unlocks it at a story
counter value, type 1 when another monster has been defeated, and with no rule when this monster has been defeated
(kill count at save `+3404h + i`, `00315420`).

Each entry has seven text slots, whose unlock is worked out each time the entry is shown and never saved (`00576E30`). The unlock record is
16 bytes, seven `u16` values and a mode word at `+0E`<sub>h</sub> (`00576860`):

| Mode | A slot unlocks when |
|---|---|
| `0` | this monster's kill count reaches the slot's value |
| `1` | the story counter reaches the slot's value |
| `2` | this monster or the monster the slot names has been defeated |

The read marks are save `+3604h + i`, one bit per slot (`00315670`, `00315AD0`). `00577550(5)` sets the marks of empty
slots, so an entry counts as read when every unlocked slot has been viewed. The entry shows the kill count (`005760A0`).

#### Hunts

`menuquest.dat` holds 8-byte records (below); group 1 (`key & FFh`) is the 45 hunts, quest ids `80`<sub>h</sub>-`AC`<sub>h</sub>.
A hunt is listed when `0046B1A0(quest)` or `0046B240(quest)` is true (`00576550(6)`), and read marks are at save
`+33F4`<sub>h</sub>.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | text | title text id |
| `04`<sub>h</sub> | `u32` | key | group in bits 0-7, quest id in bits 8-17 |

#### Sky Pirate's Den

A statue is awarded by bit `i` at save `+3844`<sub>h</sub> and read at `+3848`<sub>h</sub> (`003154B0(7, i)`). The back panel re-checks the
awards with `00577550(7)` (`005750AF`, `00316930`). `00572920` lays out one group per awarded statue from
`menuhandbook_order.bin`.

### The monster viewer

1. The entry page passes the Bestiary entry number to `001846F0` (`0057025A`), which saves and clears `02CB8138` and
   calls `001EB7B0`.
2. `001EB9C0` reads entry `MonsterId<n>` of `monstergallery.json` through `001C6320` and, for a new model, requests it with
   `002EE9C0` (`001EBA05`).
3. The loader `002EE430` loads the body, then weapon 0 and weapon 1, then the motion set chosen by weapon 0
   (`003203B0`), and marks each part's render record `+6E0h = 1`.
4. Each frame, `001EC060` turns the model from the stick (`00249860`, `00249880`): the yaw wraps from 0 to 360 and the
   pitch stays between -15 and 30 degrees. It turns vectors with `001EB3D0`, a vector times the upper 3 x 3 of a
   matrix (`001EC3DC`).
5. `00477F20` draws a record with `+6E0`<sub>h</sub> set only in frame mode 3 (`00229EA0`), and every other record only outside
   it, so the model appears only in the menu.
6. Closing the entry (`001846B0`, `00570355`) frees the model and restores `02CB8138`.

The loader settles a request with `002EED80` (`002EE975`), only on a pass where `0216420C` is 1, which it clears:

- with a model shown (`0216423C` = 1) and `00181DD0()` answering 0, it releases it (`002EEB20([02164238])`) and clears
  the request flag `02164208`;
- with a request (`02164208` = 1) for another model (`02164240` not equal to `02164210`), it releases the shown one,
  copies the request (`02164240`-`0216426C`) over the current values (`02164210`-`0216423C`), sets `01EEBAA8` to 0 and
  clears the flag;
- otherwise, with a model shown, it calls `00181DF0` with entry `[02164238]` of `01EEBAB0`.

The viewer is the `2E0`<sub>h</sub>-byte object `[01F82E18]`, built on first use by `001EBA40`. When the entry page opens it,
`00181D50` and `00181D80` take two screen-sized render targets from the pool `[01F81210]` (`00182BE0(1.0, 1.0)`)
into viewer `+270`<sub>h</sub> and `+278`<sub>h</sub> (`0057025F`, `00570264`); `00181B90` and `00181BD0` hand them back when it
closes (`0057032C`, `00570350`).

`001C6320` passes the entry's keys on to the viewer:

- `monsterWeaponIndex` and `monsterWeaponIndex2` to `001EBBF0` as weapons 0 and 1: the index goes to
  `+124h + 4 x slot` and the count `slot + 1` to `+12C`<sub>h</sub>, or the count is 0 when the index is 0;
- `motionIndex` to `001EBC20`, which keeps it modulo 80 at `+224`<sub>h</sub>;
- `cameraFov` to `001EBA90` (`+250`<sub>h</sub>, `+110`<sub>h</sub>);
- the ambient light and the two lights, colours and directions, in one `D0`<sub>h</sub>-byte block to `001EBB70`, which copies
  it to `+144`<sub>h</sub> (`001C694D`);
- `eyeVfxZBias` (`008FB498`) to `002F1690` (`001C659B`), which stores the value less 1000.0 at `022BDEBC`.

## Shipped data

| Family | Entries | Groups | Unlock limit (`00D23758`) |
|---|---:|---:|---:|
| Traveler's Tips (`tutorial`) | 16 | 4 | 56 |
| Bestiary (`monster`) | 384 | 32 | 512 |
| `story` | 69 | 4 | 160 |
| `world` | 74 | 10 | 96 |
| `person` | 57 | 4 | 64 |
| `knowledge` | 100 | 7 | 120 |

- Bestiary slot modes: 370 entries by kill count, 13 by story counter and 1 by another monster. 192 picture files
  serve the 384 entries, and `monstergallery.json` has 384 entries.
- Hunts: 45 of a limit of 48. Sky Pirate's Den: 30 statues, Balthier to Zodiark (`penelosdiary` `1B68`<sub>h</sub>-`1B85`<sub>h</sub>).
- The kind-7 path table at `01EC73A0` names the `in` copies of `menuhandbook.bin` and `menuhandbook_order.bin` for
  `C8`<sub>h</sub> and `C9`<sub>h</sub>; no `us` path for either is in the image. That `menuhandbook.bin` holds 15 Bestiary rules.

## Modding notes

- An entry's unlock conditions are its record in `menuhandbook_<family>.dat`; a Bestiary slot's threshold is one of the
  seven values of the monster's record.
- Changing one of the four records at `00D23688` to kind 0-3 would show one of the four unused families, whose data
  ships; that row position's other tests still apply. A fifth record is never read (`0056F7EA`).
- The monster shown for an entry is its `MonsterId` record in `monstergallery.json`.

## Related

- [Menus](menus.md) - the Party Menu that opens the Clan Primer.
- [Story progress](../Story-Events-And-Hunts/story-progress.md) - the story counter and windows the unlocks read.
- [Quests](../Story-Events-And-Hunts/quests.md) - the hunts.
- [Hunts](../Story-Events-And-Hunts/hunts.md) - every hunt's name, petitioner and record text as the Hunts page shows them.
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) - where kill counts are kept.
