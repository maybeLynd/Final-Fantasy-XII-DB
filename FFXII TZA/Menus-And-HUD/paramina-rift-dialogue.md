---
title: "Paramina Rift dialogue: every line and caption of the Paramina Rift scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[paramina-rift-dialogue.tsv](paramina-rift-dialogue.tsv) has one row per string of sections 2 and 3 of the Paramina Rift scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 109 rows from 6 zone scripts under `plan_map/` and 1 scene script under `event/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `paramina-rift-scripts.tsv`, the table of [Paramina Rift scripts](../Story-Events-And-Hunts/paramina-rift-scripts.md), names section 2 rows by the same key: 19 of its rows name 54 of the 109 section 2 rows here.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table |
|---|---|---:|---:|---:|
| `pbc_a0300` | scene | 8 | 0 | 7 |
| `pbc_a01` | zone | 53 | 0 | 28 |
| `pbc_a03` | zone | 1 | 0 | 1 |
| `pbc_b01` | zone | 6 | 0 | 5 |
| `pbc_c01` | zone | 38 | 0 | 13 |
| `pbc_c02` | zone | 1 | 0 | 0 |
| `pbc_c03` | zone | 2 | 0 | 0 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 109 rows.

Empty strings per tree: `us` 6, `de` 6, `es` 6, `fr` 6, `it` 6. No `in`, `kr`, `cn` or `ch` string is empty.

6 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `pbc_a0300` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 7 | 7 | 7 | 7 |
| `fontex_expand` | 102 | 102 | 102 | 102 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

27 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 16 with 2, 5 with 3, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 27, `de` 27, `es` 27, `fr` 27, `it` 27, `in` 27, `kr` 27, `cn` 27, `ch` 27.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `pbc_a01` 2/13, a line with a line break (`{line}`). `us`: `{actor-name:8180}{line}{speed:8180}A strong Mist prevents saving.`; `in`: `{spacing:8181}{actor-name:8180}{line}{speed:8180}ミストの干渉により、セーブすることはできません。`.
- `pbc_a0300` 2/5, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}You sound sure of yourself.`; `in`: `{spacing:8180}{speed:8180}{alt-font}たいした自信だな`.
- `pbc_a01` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script file under `plan_master/<language>/`: `plan_map/...` for a zone script, `event/...` for a scene script |
| `section` | `2` for a line of the message bank, `3` for a caption |
| `id` | the entry number in that section, from 0: the text id a verb passes |
| `us` to `ch` | the string in that language tree, decoded with the tree's font |
| `missing` | the languages whose tree has no string at this key (no such script, or a shorter section), comma-separated; empty when all nine have one |
| `same_bytes` | the groups of languages whose string bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more, and the languages in `missing` take no part |

An empty cell under a language not in `missing` is an empty string.

## Data

| Fact | Value |
|---|---|
| rows | 109: 109 in section 2, 0 in section 3 |
| scripts | 7: 6 zone, 1 scene |
| strings per tree | `us` 109, `de` 109, `es` 109, `fr` 109, `it` 109, `in` 109, `kr` 109, `cn` 109, `ch` 109 |
| non-empty strings per tree | `us` 103, `de` 103, `es` 103, `fr` 103, `it` 103, `in` 109, `kr` 109, `cn` 109, `ch` 109 |
| strings with `{alt-font}` | `us` 7, `de` 7, `es` 7, `fr` 7, `it` 7, `in` 7, `kr` 7, `cn` 7, `ch` 7 |
| strings with a choice list | `us` 27, `de` 27, `es` 27, `fr` 27, `it` 27, `in` 27, `kr` 27, `cn` 27, `ch` 27 |
| section 2 rows the scripts table names | 54 |

## Related

- [Paramina Rift scripts](../Story-Events-And-Hunts/paramina-rift-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Paramina Rift scenes](../Story-Events-And-Hunts/paramina-rift-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
