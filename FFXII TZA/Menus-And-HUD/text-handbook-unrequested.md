---
title: "Unrequested handbook text: the story, world, person and knowledge books no Clan Primer page opens"
kind: "reference"
category: "Menus and HUD"
addresses: "0x0056F810, 0x00D23688, 0x00575710, 0x0039BEC0"
---

## What it lists

[text-handbook-unrequested.tsv](text-handbook-unrequested.tsv) has one row per text slot of the handbook families
`story`, `world`, `person` and `knowledge`: 328 rows. Every language tree ships these bundles with the same bytes,
Japanese text, so the table gives each slot once, in the `in` column, decoded with the Japanese font. The bundle
layout is on [Handbook files](../Game-Files-And-Data-Tables/handbook-files.md).

No Clan Primer page opens these families. The category list `0x0056F810` builds its rows from the four records at
`0x00D23688`, which name families 6, 5, 7 and 4 (Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips); the four
families' titles, `0x1B58` to `0x1B5B`, are empty strings ([Clan Primer](clan-primer.md)).

### Reading the text

Each bundle carries its own glyph sheet in every language. `0x00575710` registers such a sheet as a glyph sheet only
(`0x0039BEC0`), without the font id and name that Traveler's Tips and Bestiary sheets get. A two-byte code at or above
the expansion lead byte is written `{exp:0xN}`, 1,842 in all. `{line}` ends a line and `{blank}` is a blank, as in
the Bestiary text ([Clan Primer text](text-handbook.md)).

| Row | `in` |
|---|---|
| `person` 0, slot 0 | `旧ダルマスカ王国の首都ラバナスタに{exp:0x0}らす少年。１７{exp:0x1}。{line}２年前の戦{exp:0x2}で{exp:0x3}一の肉{exp:0x4}である兄を{exp:0x5}くして以後、天{exp:0x6}{exp:0x7}独となる。{line}明るく前{exp:0x8}きな性格で、同じように戦{exp:0x2}によって家族を失った少年少女たちから頼りにされている。{line}空賊にあこがれており、いつの日か飛空艇で大空を自{exp:0x9}に飛び回ることを{exp:0xA}見ている。` |
| `world` 0, slot 0 | `バレンディア、オーダリア、ケルオンの３大陸により構成される世界。{exp:0x0}かな自然と季候に{exp:0x1}まれている。各地域の気候帯は大気中のミスト{exp:0x2}度と密接な{exp:0x3}{exp:0x4}がある。{line}イヴァリースにはさまざまな種族が生活し、文化{exp:0x5}を形成している。その中でもっとも{exp:0x6}力を持っているのはヒュム族で、世界はヒュム族を中心に動いている。` |

## Columns

| Column | Meaning |
|---|---|
| `book` | the handbook family: `story`, `world`, `person` or `knowledge` |
| `record` | the entry number, counted across the family's bundles from 0 |
| `slot` | the text slot of the entry, from 0 |
| `in` | the slot's text, decoded with the Japanese font; every tree holds the same bytes |
| `missing` | empty in every row |
| `same_bytes` | empty in every row: there is one language column |
| `files` | the bundle holding the entry, as `story000` |

## Data

| Family | Entries | Text slots | Bundles |
|---|---:|---:|---|
| `story` | 69 | 69 | `story000` |
| `world` | 74 | 102 (46 entries with one slot, 28 with two) | `world000` |
| `person` | 57 | 57 | `person000` |
| `knowledge` | 100 | 100 | `knowledge000` (88 slots), `knowledge001` (12 slots) |

## Related

- [Handbook files](../Game-Files-And-Data-Tables/handbook-files.md) - the `hdat` bundle layout and the six
  families.
- [Clan Primer](clan-primer.md) - the categories the Clan Primer lists.
- [Clan Primer text](text-handbook.md) - the Bestiary and Traveler's Tips text.
- [Text codes](text-codes.md) - the text codes and their placeholders.
