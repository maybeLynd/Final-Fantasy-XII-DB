---
title: "Hunts: every hunt with its name, petitioner, row picture, record text, the progress that shows each part and when its row is marked done"
kind: "reference"
category: "Story, events and hunts"
addresses: "0037E5B0, 002F9920, 0037EFC0, 0037E8D0, 0037EF70, 0037EE10, 00578450, 00577C30, 003FFB00, 002639E0"
---

## What it lists

`hunts.tsv` holds one line for each of the 45 hunts, group 1 of `menuquest.dat`, quest ids 128 to 172, with the
text the Clan Primer's Hunts page shows for them. The formats and the code that reads each field are on
[Quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md); this page is the shipped content of
the `us` files.

Each hunt's record is the bill, the accepted hunt with where the mark is, the defeat and the report. Hunts 133,
167 and 168 have a fifth part: 133 and 168 a closing line after the report, 167 a chase before the defeat. The
row is marked done at the part that reports the mark defeated, or for hunt 163 trapped in the urn: the `.lst`
threshold is 3, and 4 for hunt 167.

The files hold no item or gil field, so the table has no reward column. The record files carry text, a
picture, a threshold, the progress table and the map chunks only (the layouts on
[Quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md)); a hunt's reward is given by a
script call to one of the item and gil verbs that [Scene rewards](scene-rewards.md) describes.

### How it is built

`Database/Tools/catalogues/hunts.py`, with the shared readers in `ffxii_text.py`:

1. the 66 records of `menuquest.dat` from `+0x0C`; a hunt is a record whose key byte 0 is 1 (`0037E5B0`), and its
   position is the number of earlier group-1 records (`0037E5B0`, `0037EE10`);
2. the name through `002F9920`: text group `id / 10000` (21, `questtitle`), the row whose id equals the record's
   text id;
3. the first `menuquest.lst` entry with the quest id: the petitioner line and the low nibble of `+0x04`
   (`0037EFC0`, `0037E5B0`);
4. the hunt's record in `menuquest01.bin` at `0x10 + 20 x position`, section 2 at `sectionAt[2] + item[2]`
   (`0037E8D0`), cut at each `0x03` into at most 12 parts (`00578450`);
5. the position's 28-byte section-5 row: value `k` is the number of parts shown while the progress byte divided by
   5 is `k` (`0037EF70`, `0037EE10`);
6. each code `0F 38` in the text replaced by the name it stands for: `003FFB00` turns its payload into a name id
   and the text interpreter (`002ADDAA`) takes the name from `002639E0`, entry `2 x id` of `npcdic.bin`, or
   `2 x id + 1` once persistent flag `id` is set ([NPC names](../Characters-And-Objects/npc-names.md));
7. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

The record text inserts two names this way, id 46 "Tomaj" (hunt 128) and id 726 "Burrogh" (hunt 144), and both
strings of each pair are the same, so the flag changes nothing in these texts.

### Checks

- `menuquest.dat` holds 66 records, 45 of them in group 1, and `menuquest01.bin`'s section 0 starts at
  `16 + 20 x 45` and its section 5 ends at the file's end; the TSV has 45 data lines, one per quest id 128-172.
- Every hunt has as many parts as the largest value of its progress row: 4 parts for 42 hunts and 5 for 133, 167
  and 168. Every progress row is non-decreasing, and sections 0 and 1 are empty for every hunt.
- Two runs over the same files give byte-identical output.
- No text field keeps an undecoded `{hh}` byte.
- Hunt 128 compared with its scripts: `rbn_a16` sets its progress to 30 (`setquestscenarioflag`, verb `0x2B3`,
  handler `00351140`, at script-section offset `0x1D224`), which shows two parts, the bill and the accepted hunt, and to 70
  with the clear (`setquestclear` at `0x1DA5E`), which shows all four.
- Hunt 147 compared with its scripts: the actor `HUNT07` in `alc_f03` sets 50 (`0x27B8E`), two parts, and with the
  clear 150 (`0x27D02`), all four; the row is marked done from 100, the defeat part.
- Hunt 172 is record 59 and position 40, between 167 and 168, so its text is the 41st record of
  `menuquest01.bin`.

## Columns

| Column | Meaning | Read by |
|---|---|---|
| `quest` | the quest id, key bits 8-17 | `0037E5B0`, `0037EE10` |
| `record`, `position` | the record's index in `menuquest.dat` and its position among the group's records | `0037E5B0`, `0037EE10` |
| `group` | key bits 0-7, 1 for every hunt | `0037EAA0`, `00577C30` |
| `name` | the name text, record `+0x00` | `002F9920` from `0037E5B0` |
| `picture` | key bits 20-27 | `0037E5B0` |
| `picture_sheet`, `picture_cell` | the sheet `2 x (picture / 24)`, plus 1 once done, and the cell `picture % 24` | `00577C30` |
| `petitioner` | the `.lst` line, petitioner and town | `0037EFC0`, `0037E5B0` |
| `threshold` | the `.lst` threshold, the low nibble of `+0x04`: the row is done once this many parts show | `0037E5B0`, `00577C30` |
| `parts` | the parts of the section-2 text | `00578450` |
| `part_from` | for each part, the lowest progress byte at which it shows | `0037EF70`, `00578450` |
| `done_from` | the lowest progress byte at which the row is marked done | `0037EE10`, `00577C30` |
| `part_1`-`part_5` | the text of each part; `0x02` line breaks become spaces | `0037E8D0`, `00578450` |
| `explanation` | a one-line summary: the name, the petitioner, the progress of each part and of the done mark | |

The progress byte is the quest's scenario byte, save `+0x1064 + quest` (`0046B180`), set by the scripts'
`setquestscenarioflag` ([Quests](quests.md)).

## Related

- [Quest menu files: the menuquest list, petitioner strings and per-group detail tables, how they are read, and what each field shows](../Game-Files-And-Data-Tables/quest-menu-files.md)
- [Clan Primer: the Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages, how entries unlock, and the monster viewer](../Menus-And-HUD/clan-primer.md)
- [Quests: the ordered and cleared state each quest keeps in the save, its progress byte and word, the verbs that change them, and the bug that clears the wrong ordered bit](quests.md)
- [Scene rewards: every item and gil amount the story scripts give or take, by script and function, and how each item is chosen](scene-rewards.md)
- [NPC names: the npcdic.bin name pairs, the actor's name id, and the story flag that swaps a name](../Characters-And-Objects/npc-names.md)
