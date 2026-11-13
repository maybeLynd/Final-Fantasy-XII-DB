---
title: "Hunts: every hunt with its name, petitioner, row picture, record text, the progress that shows each part and when its row is marked done"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x0037E5B0, 0x002F9920, 0x0037EFC0, 0x0037E8D0, 0x0037EF70, 0x0037EE10, 0x00578450, 0x00577C30, 0x003FFB00, 0x002639E0"
---

## What it lists

[`hunts.tsv`](hunts.tsv) holds one line for each of the 45 hunts, group 1 of `menuquest.dat`, quest ids 128 to 172, with the
text the Clan Primer's Hunts page shows for them. The formats and the code that reads each field are on
[Quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md); this page is the shipped content of
the `us` files.

Each hunt's record is the bill, the accepted hunt with where the mark is, the defeat and the report. Hunts 133,
167 and 168 have a fifth part: 133 and 168 a closing line after the report, 167 a chase before the defeat. The
row is marked done at the part that reports the mark defeated, or for hunt 163 trapped in the urn: the `.lst`
threshold is 3, and 4 for hunt 167.

A hunt's page in the Clan Primer grows as its scripts raise the hunt's progress number in the save. A table in
`menuquest01.bin` says how many parts of its text show at each progress value, and the row is marked done once as many
parts show as the threshold in `menuquest.lst`.

The files hold no item or gil field. The record files carry text, a
picture, a threshold, the progress table and the map chunks only (the layouts on
[Quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md)).

### The reward

Every hunt's reward is the package of its selector, `0xA000` + the quest id ([Reward selector list](../Rewards-EXP-Gil-And-Loot/reward-selector-list.md)). The report script calls `questresultwindow(quest)`, which opens the result window and grants the package at once ([Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), "The quest result window").

The `us` zone scripts make 56 such calls, with the quest id written in the call for 43 hunts. Montblanc's talk in The Clan Hall (`rbn_a14`) stores 167 or 170 and passes the stored id for those two. Hunt 153 is reported in any of the five aerodromes, and hunt 132 in Lhusu Square (Bhujerba) or The Chosen Path (Tchita Uplands).

### The mark

The `mark` column joins each mark to its [Bestiary](../Enemy-Spawning/bestiary.md) rows and their placements by name. 38 hunts have a step labelled with the mark, and its `location` word is the field id of a map zone, which the location map looks up among its zones (`0x003BC160`, `0x003C0380`; [Map menu files](../Game-Files-And-Data-Tables/menu-map-files.md), lmap `fieldId`).

Seven hunts have no such step. The five steps of 153 carry location 0. The one step of 159, 167, 169, 170, 171 and 172 is labelled Montblanc, Rikken or Whitecap Wench, and the hunt map marks that step's zone. Their marks are the foes their record names; hunt 172's Belito is a ruse, and the foe is Ba'Gamnan.

### The key item a mark leaves

Ten marks leave a key item when they fall. The hunt watcher of the mark's map stores the item's id while the
mark's battle word is 1, requests the key-item screen, which gives the item, and then writes the hunt's stage.
[`hunt-key-items.tsv`](hunt-key-items.tsv) lists the ten with the listing lines, the step that later takes the
item and what the item is used for:

- the Cactus Flower (hunt 130), Broken Key (133), Serpentwyne Must (136) and Errmonea Leaf (137);
- the Ring of the Toad (138), Rabbit's Tail (141), Viera Rucksack (148) and Rusted Scrap of Armor (149);
- the Ring of the Light (158) and Stolen Articles (162).

Nine of the ten watchers are actors named `wanted_kansi`; the Cactus Flower's is `花サボ監督` of `dst_a02`. The
`us` zone scripts hold 35 actors named `wanted_kansi`, and the other 26 store no item.

| Column | Meaning |
|---|---|
| `hunt`, `hunt_name` | the quest id and name, as in `hunts.tsv` |
| `item`, `item_name` | the key item's id and name ([key items](../Items-Equipment-Shops-And-Licenses/key-item-list.md)) |
| `given` | the watcher's script, the battle word it tests, the lines of the test, the store and the screen request, and the line of the screen's `additemmes` |
| `hunt_stage` | the stage the watcher then writes with `setquestscenarioflag`, and its line |
| `taken_by` | the script steps that take the item with `subitem` ([scene rewards](scene-rewards.md)), or `-`; the developer script `evt_t0090` also takes three of them and is left out, as on that page |
| `used_for` | the item's use, as the key item list gives it |

### When a bill is posted

The clan boards in The Sandsea (Rabanastre), Jajim Bazaar (Nalbina Town), The Cloudborne (Bhujerba), Hunters' Camp (Phon Coast), The Whitecap (Balfonheim Port) and Granch's Requisites (Archades) run one talk (`掲示板.talk` in `rbn_a16`, `nac_a02`, `byu_a18`, `fon_b01`, `var_a14` and `alc_f04`). It posts hunts 129 to 159 in order: story progress sets how many the board shows, 2 from 105 up to all 31 from 6,100, and each needs its own clan rank. A bill shows while its hunt is neither ordered nor cleared; taking it orders the hunt (`setquestorder(quest, 1)`).

Montblanc's talk in The Clan Hall (Rabanastre) (`rbn_a14`) offers hunts 160 to 171 the same way, 2 from 350 up to all 12 from 6,100, and hunt 172 from 4,100 once three of hunts 160-171 are cleared, 164 among them. Hunts 167, 168 and 171 also wait on defeated marks. Hunt 128 is not posted: the scene at the board in The Sandsea orders it at the start of the first hunt. The `posted` column gives each hunt's tests.

### Where the values come from

Each line is read from the shipped files in these steps:

1. the 66 records of `menuquest.dat` from `+0x0C`; a hunt is a record whose key byte 0 is 1 (`0x0037E5B0`), and its
   position is the number of earlier group-1 records (`0x0037E5B0`, `0x0037EE10`);
2. the name through `0x002F9920`: text group `id / 10000` (21, `questtitle`), the row whose id equals the record's
   text id;
3. the first `menuquest.lst` entry with the quest id: the petitioner line and the low nibble of `+0x04`
   (`0x0037EFC0`, `0x0037E5B0`);
4. the hunt's record in `menuquest01.bin` at `0x10 + 20 x position`, section 2 at `sectionAt[2] + item[2]`
   (`0x0037E8D0`), cut at each `0x03` into at most 12 parts (`0x00578450`);
5. the position's 28-byte section-5 row: value `k` is the number of parts shown while the progress byte divided by
   5 is `k` (`0x0037EF70`, `0x0037EE10`);
6. each code `0F 38` in the text replaced by the name it stands for: `0x003FFB00` turns its payload into a name id
   and the text interpreter (`0x002ADDAA`) takes the name from `0x002639E0`, entry `2 x id` of `npcdic.bin`, or
   `2 x id + 1` once story flag `id` of Bank2048 is set ([NPC names](../Characters-And-Objects/npc-names.md));
7. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

`0x003FFB00(code, out)` is given the code's `0x38` byte (`0x002B52DB`) and returns 3 or 4, the bytes it reads from
there. When bits `0x7` of the first payload byte are clear, the id is the signed byte that starts record
`p1 & 0x7F` of `0x0039BA00`, `p1` being the second payload byte, and it returns 3 (`0x003FFB47`-`0x003FFB59`).

Otherwise the id is `(p1 & 0x7F) << 8` ORed with `p2 & 0x7F`, `p2` being the third payload byte, with `0x8000` for
bit `0x40` of the first payload byte and `0x80` for its bit `0x20` (`0x003FFB0F`-`0x003FFB3F`, `0x003FFB5E`-`0x003FFB72`);
bit `0x80` of the first byte is dropped, and it returns 4. The text interpreter reads the id as a signed 16-bit
word (`0x002ADDA0`).

The record text inserts two names this way, id 46 "Tomaj" (hunt 128) and id 726 "Burrogh" (hunt 144), and both
strings of each pair are the same, so the flag changes nothing in these texts.

### Properties of the shipped files

- `menuquest.dat` holds 66 records, 45 of them in group 1, and `menuquest01.bin`'s section 0 starts at
  `16 + 20 x 45` and its section 5 ends at the file's end; the TSV has one line per quest id 128-172.
- Every hunt has as many parts as the largest value of its progress row: 4 parts for 42 hunts and 5 for 133, 167
  and 168. Every progress row is non-decreasing, and sections 0 and 1 are empty for every hunt.
- Hunt 128 in its scripts: `rbn_a16` sets its progress to 30 (`setquestscenarioflag`, verb `0x2B3`,
  handler `0x00351140`, at script-section offset `0x1D224`), which shows two parts, the bill and the accepted hunt, and to 70
  with the clear (`setquestclear` at `0x1DA5E`), which shows all four.
- Hunt 147 in its scripts: the actor `HUNT07` in `alc_f03` sets 50 (`0x27B8E`), two parts, and with the
  clear 150 (`0x27D02`), all four; the row is marked done from 100, the defeat part.
- Hunt 172 is record 59 and position 40, between 167 and 168, so its text is the 41st record of
  `menuquest01.bin`.

## Columns

| Column | Meaning | Read by |
|---|---|---|
| `quest` | the quest id, key bits `0x3FF00` | `0x0037E5B0`, `0x0037EE10` |
| `record`, `position` | the record's index in `menuquest.dat` and its position among the group's records | `0x0037E5B0`, `0x0037EE10` |
| `group` | key bits under mask `0xFF` for every hunt | `0x0037EAA0`, `0x00577C30` |
| `name` | the name text, record `+0x00` | `0x002F9920` from `0x0037E5B0` |
| `picture` | key bits under mask `0xFF00000` | `0x0037E5B0` |
| `picture_sheet`, `picture_cell` | the sheet `2 x (picture / 24)`, plus 1 once done, and the cell `picture % 24` | `0x00577C30` |
| `petitioner` | the `.lst` line, petitioner and town | `0x0037EFC0`, `0x0037E5B0` |
| `threshold` | the `.lst` threshold, the low nibble of `+0x04`: the row is done once this many parts show | `0x0037E5B0`, `0x00577C30` |
| `parts` | the parts of the section-2 text | `0x00578450` |
| `part_from` | for each part, the lowest progress byte at which it shows | `0x0037EF70`, `0x00578450` |
| `done_from` | the lowest progress byte at which the row is marked done | `0x0037EE10`, `0x00577C30` |
| `part_1`-`part_5` | the text of each part; `0x02` line breaks become spaces | `0x0037E8D0`, `0x00578450` |
| `part_2`, `part_3`, `part_4` | parts 2 to 4, which all 45 hunts have: part 2 opens with `Hunt accepted.` on 42 hunts and tells where the mark is; part 3 tells of the mark's defeat and where to report or take the reward on 42 hunts, all but Paradise Risen (the gil snapper sealed in the urn), Battle on the Big Bridge and A Dark Rumor; part 4 is the report, opening with `Hunt reported` on 40 hunts and `Reward received` on 3 | `0x0037E8D0`, `0x00578450` |
| `explanation` | a one-line summary: the name, the petitioner, the progress of each part and of the done mark; for hunt 165, also the Site 3 and Site 11 Keys its scripts give and the locked gates they open | |
| `mark` | the mark: its bestiary rows with the Clan Primer entry, the maps whose scripts place it with the level, the Trial Mode rows, and the map zone the hunt map marks with its location word and field id, or, for a hunt with no step labelled with the mark, the zone its one step marks or that no step marks one ("The mark" above) | `0x0037EB90`, `0x003BC160` |
| `reward` | the reward package with what it gives, its selector, and the maps whose scripts grant it ("The reward" above) | `0x00344C60`, `0x00290130` |
| `posted` | where the bill is posted and the story progress, clan rank and earlier hunts its talk tests ("When a bill is posted" above) | the scripts' `getclanrank`, `isquestorder`, `isquestclear` and story progress tests |

The progress byte is the quest's scenario byte, save `+0x1064 + quest` (`0x0046B180`), set by the scripts'
`setquestscenarioflag` ([Quests](quests.md)).

## Related

- [Quest menu files: the menuquest list, petitioner strings and per-group detail tables, how they are read, and what each field shows](../Game-Files-And-Data-Tables/quest-menu-files.md)
- [Clan Primer: the Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages, how entries unlock, and the monster viewer](../Menus-And-HUD/clan-primer.md)
- [Quests: the ordered and cleared state each quest keeps in the save, its progress byte and word, the verbs that change them, and the bug that clears the wrong ordered bit](quests.md)
- [Scene rewards: every item and gil amount the story scripts give or take, by script and function, and how each item is chosen](scene-rewards.md)
- [NPC names: the npcdic.bin name pairs, the actor's name id, and the story flag that swaps a name](../Characters-And-Objects/npc-names.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Rewards progression economy: `0x00290130` calls `0x003F4AA0`; those functions are documented on
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
