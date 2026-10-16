---
title: "Clan Primer: the Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages, how entries unlock, and the monster viewer"
kind: "system"
category: "Menus and HUD"
summary: "How the Clan Primer opens from the Party Menu and straight back into Hunts, its four categories and when each shows, the family index and entry pages, the data manager that loads catalogs, text and pictures, how Traveler's Tips, Bestiary entries and their slots, hunts and Sky Pirate's Den statues unlock, the read marks behind the new-entry badge, and the monster viewer from gallery entry to the turntable drawn only in the menu."
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

The Party Menu command is `0x4BC`, "Clan Primer" in `menu_command.bin`. The Party Menu's handler `00281ED0` closes
itself and calls the opener `00574CB0` (`0028239B`), which creates the back panel `00574E80` and publishes it at
`02CA9718`. The back panel builds the screen:

1. id 1 requests the background `HandBack_c.tm2` (kind-7 resource `0xCE`), `Hand_4_c.tm2` (`0xCD`) and
   `Party_Book.mrp` (`0xCC`), and installs the data manager `005771F0` (`00574FAE`).
2. id 14 sets the title, `002F9860(0x4BC)` (`00574E00`), and installs the category list `0056F810` (`00574D00`).
3. id 16 installs the mid pane `0056EF60`, which hosts the chosen category's pages.

A second opener, `00575580` (from `002814E0`), reopens the Clan Primer straight into Hunts from a 16-byte resume record
at `0209AC30 + 0x3E8`: it sets back-panel bit `0x40`, and `00574D00` then posts kind 6 to itself. On close
(`00575498`) the screen returns to the Party Menu through `002814E0(0x4BC)` unless back-panel bit `0x20` asks it to
leave without returning.

### Categories

`0056F810` builds its rows from the four 6-byte records at `00D23688`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16` | label | category label |
| `02` | `u16` | help | help line |
| `04` | `u8` | kind | page kind |
| `05` | `u8` | b5 | 1, or 2 for Traveler's Tips |

The shipped records:

| Row | Category | Help | Kind | Shown when (`0056F750`) |
|---|---|---|---|---|
| `0` | Hunts (`0x1B5F`) | "Hunt information and progress." | `6` | the Hunts sync passes, story window 11 is open (`0032A8A0(0x400B)`, entry 11 of the story schedule `00377970`) and a hunt is listed |
| `1` | Bestiary (`0x1B5C`) | "Insights on foes you have defeated." | `5` | the Bestiary sync passes, story window 11 is open and an entry is unlocked |
| `2` | Sky Pirate's Den (`0x1B5D`) | "What will it take to fill the den?" | `7` | story window 11 is open |
| `3` | Traveler's Tips (`0x1B5E`) | "Hints for the wary adventurer." | `4` | the Traveler's Tips sync passes and an entry is unlocked |

The labels and help lines are in `penelosdiary` and `help_penelosdiary`. A row carries the new-entry badge when fewer
entries are read than unlocked (`0056FAD0`). Confirming posts the kind to the back panel, which hands it to the mid
pane (`00575480`, `0056F2A0`). Each page's title is `002F9860([00D236A0 + 6 x kind])`.

### Pages

The mid pane installs the page for the kind (`0056EE10`):

| Kind | Page | Data |
|---|---|---|
| 4 Traveler's Tips | family index `00571A50`, then the entry page `005701B0` | family `tutorial` |
| 5 Bestiary | the same, two columns, with the backdrop `HandBack2_c.tm2` (`0xD0`), the count pane `00570530` and the monster viewer | family `monster` |
| 6 Hunts | hunt list `00579AF0` | `menuquest.dat`, group 1 |
| 7 Sky Pirate's Den | `00572E10` | `menuhandbook_order.bin`, `Medal_c.tm2` (`0xCF`) |

Four more families, `story`, `world`, `person` and `knowledge`, ship with data, but their titles (`0x1B58`-`0x1B5B`) are
empty and no category row names them; the resume path posts only kind 6. That scope is the senders of the category
command read in `0056F810` and `00574D00`.

The family index lists rows of three types, blank, entry and group caption (`00571A50`, `00571710`, `00576A50`).
Confirming an entry opens the entry page through `0056EC10`. The cursor of each page is saved in bank 6 (`002527B0`).

### The data manager

`005771F0`, at `02CA9738`, loads what the pages show:

1. `00576F50` binds the six families' unlock tables, `menuhandbook_<family>.dat` (kind-7 id `[00D23740 + 2 x kind] + 1`),
   and `menuquest.dat` (`0x128`).
2. It runs three load slots (`00575870`), each loading kind-7 id `[00D23740 + 2 x kind]` plus an offset (`00575C30`):
   slot 0 the family catalog, slot 1 the entry's text bundle, slot 2 its picture bundle.
3. A text bundle may carry its own glyph sheet (an i32 at `+0x0C` other than -1). `00575710` registers the sheet
   (`0039BEC0`), and for Traveler's Tips and the Bestiary also registers it as a font (`0017FBC0(6)`; `0017FA90`,
   `0017F790`). The `story`, `world`, `person` and `knowledge` bundles carry a sheet in every language; the Bestiary
   and Traveler's Tips bundles carry one only in `kr`, `ch`, `cn` and `in`.
4. Slot 2 makes the entry's picture into the image label `hb_tex` (`00575B80`). The Traveler's Tips page never asks
   for a picture (`00575B80` skips kind 4), so its eight picture files ship unused.
5. A request to a busy slot waits in its queue (`00575A50`). Each slot reports to the back panel when its content is
   ready or freed.

A catalog record is 12 bytes (below), with text -1 for none (`00575D10`,
`005778F0`, `005760A0`).

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | text | entry text, -1 for none |
| `04` | `u16` | group | group |
| `06` | `u16` | bundle | text bundle |
| `08` | `u16` | picturePage | picture page |
| `0A` | `u8` | flag | flag |

### Unlocks

Per kind, `00576550` counts the unlocked entries, `00576920` the fully read ones, and `00577550(kind)` brings the unlock
state up to date.

#### Traveler's Tips and the other families

An entry's unlock bit is at save `+0x32CC` and its read bit at `+0x330C`, at the family's offset from `00D10630`
(`003154B0`, `003156E0`). `00577550` recomputes each unlock bit from the family's unlock record (`00575E80`, 8 bytes);
every field that is not all ones (`0xFF`, or `0xFFFF` for the words) must hold (`00575E8C`, `00575EA9`, `00575EC7`):

| Field | Test |
|---|---|
| `u8 a`, `u8 b` | `00315470(a) == b` |
| `u8 c` | `00315620(c) != 0` |
| `u16 +4` | story flag `0032A8A0(flag)` |
| `u16 +6` | the story counter (`00265270`) >= value |

#### Bestiary

A monster's entry unlocks by a rule in `menuhandbook.bin` section 1 (`003154B0(6, i)`): rule type 0 unlocks it at a story
counter value, type 1 when another monster has been defeated, and with no rule when this monster has been defeated
(kill count at save `+0x3404 + i`, `00315420`).

Each entry has seven text slots, whose unlock is worked out each time the entry is shown and never saved (`00576E30`). The unlock record is
16 bytes, seven `u16` values and a mode word at `+0x0E` (`00576860`):

| Mode | A slot unlocks when |
|---|---|
| `0` | this monster's kill count reaches the slot's value |
| `1` | the story counter reaches the slot's value |
| `2` | this monster or the monster the slot names has been defeated |

The read marks are save `+0x3604 + i`, one bit per slot (`00315670`, `00315AD0`). `00577550(5)` sets the marks of empty
slots, so an entry counts as read when every unlocked slot has been viewed. The entry shows the kill count (`005760A0`).

#### Hunts

`menuquest.dat` holds 8-byte records (below); group 1 (`key & 0xFF`) is the 45 hunts, quest ids `0x80`-`0xAC`.
A hunt is listed when `0046B1A0(quest)` or `0046B240(quest)` is true (`00576550(6)`), and read marks are at save
`+0x33F4`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | text | title text id |
| `04` | `u32` | key | group in bits 0-7, quest id in bits 8-17 |

#### Sky Pirate's Den

A statue is awarded by bit `i` at save `+0x3844` and read at `+0x3848` (`003154B0(7, i)`). The back panel re-checks the
awards with `00577550(7)` (`005750AF`, `00316930`). `00572920` lays out one group per awarded statue from
`menuhandbook_order.bin`.

### The monster viewer

1. The entry page passes the Bestiary entry number to `001846F0` (`0057025A`), which saves and clears `02CB8138` and
   calls `001EB7B0`.
2. `001EB9C0` reads entry `MonsterId<n>` of `monstergallery.json` through `001C6320` and, for a new model, requests it with
   `002EE9C0` (`001EBA05`).
3. The loader `002EE430` loads the body, then weapon 0 and weapon 1, then the motion set chosen by weapon 0
   (`003203B0`), and marks each part's render record `+0x6E0 = 1`.
4. Each frame, `001EC060` turns the model from the stick (`00249860`, `00249880`): the yaw wraps from 0 to 360 and the
   pitch stays between -15 and 30 degrees. It turns vectors with `001EB3D0`, a vector times the upper 3 x 3 of a
   matrix (`001EC3DC`).
5. `00477F20` draws a record with `+0x6E0` set only in frame mode 3 (`00229EA0`), and every other record only outside
   it, so the model appears only in the menu.
6. Closing the entry (`001846B0`, `00570355`) frees the model and restores `02CB8138`.

The viewer is the `0x2E0`-byte object `[01F82E18]`, built on first use by `001EBA40`. When the entry page opens it,
`00181D50` and `00181D80` take two screen-sized render targets from the pool `[01F81210]` (`00182BE0(1.0, 1.0)`)
into viewer `+0x270` and `+0x278` (`0057025F`, `00570264`); `00181B90` and `00181BD0` hand them back when it
closes (`0057032C`, `00570350`).

`001C6320` passes the entry's keys on to the viewer:

- `monsterWeaponIndex` and `monsterWeaponIndex2` to `001EBBF0` as weapons 0 and 1: the index goes to
  `+0x124 + 4 x slot` and the count `slot + 1` to `+0x12C`, or the count is 0 when the index is 0;
- `motionIndex` to `001EBC20`, which keeps it modulo 80 at `+0x224`;
- `cameraFov` to `001EBA90` (`+0x250`, `+0x110`);
- the ambient light and the two lights, colours and directions, in one `0xD0`-byte block to `001EBB70`, which copies
  it to `+0x144` (`001C694D`).

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
- Hunts: 45 of a limit of 48. Sky Pirate's Den: 30 statues, Balthier to Zodiark (`penelosdiary` `0x1B68`-`0x1B85`).
- The kind-7 path table at `01EC73A0` names the `in` copies of `menuhandbook.bin` and `menuhandbook_order.bin` for
  `0xC8` and `0xC9`; no `us` path for either is in the image. That `menuhandbook.bin` holds 15 Bestiary rules.

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
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) - where kill counts are kept.
