---
title: "Clan Primer text: every Bestiary and Traveler's Tips text slot in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x005771F0, 0x00575D10, 0x00576300, 0x00574900, 0x00575710, 0x00575782, 0x00D23770, 0x0017FA90, 0x0017FBC0, 0x00576E30"
---

## What it lists

[text-handbook.tsv](text-handbook.tsv) has one row per text slot of a Bestiary (`monster`) or Traveler's Tips
(`tutorial`) entry, with the text in each of the nine language trees: 1,024 rows, the same in every language. The
text comes from the `hdat` bundles `menuhandbook_monster<NNN>.dat` and `menuhandbook_tutorial000.dat`; their layout
is on [Handbook files](../Game-Files-And-Data-Tables/handbook-files.md). The other four handbook families
ship text that no Clan Primer page opens, listed in [Unrequested handbook text](text-handbook-unrequested.md).

### Who loads and shows it

- The handbook data manager (procedure `0x005771F0`, kept at `0x02CA9738`) loads the open entry's text bundle into
  its slot 1: when an entry page opens (`0x00570280`), `0x005778F0(entry)` calls `0x00575D10` (`0x00577969`).
- `0x00576300` builds the entry's lines from its text slots in order and stops at the first slot `0x00576E30` keeps
  closed, so Bestiary lore appears slot by slot as its thresholds are reached.
- `0x00574900` runs when the entry page shows a line. For the Bestiary, while the line's read mark is clear
  (`0x00576F30`), it sets the mark and runs the line's program; for the other families it runs the program every
  time and marks the entry read on its last line (`0x00577A20`, `0x00577A40`). It draws nothing
  ([Handbook files](../Game-Files-And-Data-Tables/handbook-files.md#entry-text),
  [Clan Primer](clan-primer.md)).

### Glyphs of the Japanese, Korean and Chinese text

In the `in`, `kr`, `cn` and `ch` trees each bundle carries a glyph sheet that `0x00575710` registers when the bundle
loads. A Traveler's Tips sheet becomes font 6 (`0x0017FBC0(6)`). A Bestiary sheet becomes font 7 under the name
`handbook_monster<NNN>.txt`, `NNN` the bundle number: `0x00575782`-`0x005757B3` print the name with the format string at
`0x00D23770` and pass it to `0x0017FA90`.

`0x0017FA90` passes its four arguments, here the bundle number plus 1, 1, the name and 7 (`0x0057579B`-`0x005757B3`), to
`0x001B6350` on the font manager that `0x001B5FB0` returns (`0x0017FAAF`-`0x0017FAC4`), which files a font request keyed by
the name's hash ([Font expansion lists](fonts-expansion-lists.md)).

The font's expansion list is the list of `fontmonster.fex` whose key is the hash of that name
([Font expansion lists](fonts-expansion-lists.md)). This table decodes each such character through the
list of the bundle in the `files` column: 9,440 characters of the Bestiary text (`in` 4,883, `kr` 826, `cn` 1,894,
`ch` 1,837).

Traveler's Tips holds 82 such characters, which this table writes `{exp:0xN}`. No `.fex` file belongs to its font,
and the font's glyph records, `fonttutorial.dat`, are keyed 0 to 31 in `jp`, 0 to 4 in `kr`, 0 to 11 in `cn` and 0
to 13 in `ch`: exactly the values N its `{exp:0xN}` take in the `in`, `kr`, `cn` and `ch` text.

### Reading the text

Each cell is the slot's text decoded with its tree's font, text codes written as placeholders (the `placeholder`
column of [Text codes](text-codes.md)). `{line}` ends a line and `{page}` a page: every Bestiary slot after
slot 0 opens with a heading line and one `{page}`, 624 per language. Slot 0 and the Traveler's Tips text have neither.

| Row | `us` |
|---|---|
| `monster` 0, slot 0 | `Plant{line}Cactus{line}` |
| `monster` 0, slot 1 | `Observations{line}{page}Being a mischievous, mean-{line}spirited beastie, mercifully lack-{line}ing the intelligence to do any real{line}damage.{line}Sproutlings are called cactites.{line}A rare strain is notable for its{line}proclivity to sprout a scarlet{line}blossom; that being seldom seen,{line}of the highest value, and consid-{line}ered a sign of miraculous good{line}fortune by sensitive young lovers{line}with a tolerance for needles.` |
| `tutorial` 8, slot 0 | `Some of the foes you will encounter are fliers, able to{line}soar through the skies, far above the ground below.{line}{line}When facing a flier, use bows, guns, and other ranged{line}weapons, or magicks such as Fire. There are also some{line}melee weapons, such as poles and spears, that can be{line}used to combat a flying foe.{line}{line}When a foe is a flier, the target info will show a {baseline:8183}{symbol:8194}{baseline:8180}{line}icon. Consider yourself warned!` |

In the `in` text of `monster` 0, slot 1, the fourth character, `燥`, which follows the two-character heading,
the `{line}` and `{page}` after it and `乾`, is the two-byte code `18 20`, expansion ordinal 0: the first value
of the `handbook_monster000.txt` list. `{symbol:8194}` draws the flying-foe
symbol; values `818A` to `8191` of the same escape are the eight element symbols.

## Columns

| Column | Meaning |
|---|---|
| `book` | the handbook family: `monster` (Bestiary) or `tutorial` (Traveler's Tips) |
| `record` | the entry number, counted across the family's bundles from 0 |
| `slot` | the text slot of the entry, from 0 |
| `us` to `ch` | the slot's text in that language tree, decoded with the tree's font |
| `missing` | the languages with no text for this slot; empty in every row |
| `same_bytes` | the groups of languages whose text bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more |
| `files` | the bundle holding the entry, as `monster003`; when the bundle differs between languages, `language:bundle` for each language, space-separated |

## Data

| Family | Entries | Slots | Rows |
|---|---:|---|---:|
| `monster` | 384 | slots 0 and 1 in every entry, slot 2 in 220, slots 3 to 6 in 5 | 1,008 |
| `tutorial` | 16 | slot 0 | 16 |

Every language has all 1,024 slots and no empty one. The Bestiary is split into 4 bundles in `us`, `de`, `it` and
`kr`, 5 in `es`, `fr`, `cn` and `ch`, and 11 in `in`, so an entry's bundle number depends on the language; Traveler's
Tips is one bundle everywhere.

## Related

- [Handbook files](../Game-Files-And-Data-Tables/handbook-files.md) - the `hdat` bundle layout, the slots'
  thresholds and the line program.
- [Clan Primer](clan-primer.md) - the Bestiary and Traveler's Tips pages and how entries unlock.
- [Clan Primer entries](clan-primer-entries.md) - the entries in order.
- [Font expansion lists](fonts-expansion-lists.md) and [Fonts](fonts.md) - the expansion lists and font ids.
- [Text codes](text-codes.md) - the text codes and their placeholders.
- [Unrequested handbook text](text-handbook-unrequested.md) - the story, world, person and knowledge books.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Platform online achievements: `0x00576E30` calls `0x00315420`; those functions are documented on
  [jump thunks](../Engine-Core/jump-thunks.md).
- World area: `0x00576E30` calls `0x00265270`; those functions are documented on
  [debug menu](../Engine-Core/debug-menu.md).
