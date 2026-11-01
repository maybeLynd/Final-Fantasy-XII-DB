---
title: "Summon dialogue: every line and caption of the Summon scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[summons-dialogue.tsv](summons-dialogue.tsv) has one row per string of sections 2 and 3 of the Summon scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 6 rows from 6 scene scripts under `event/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- [`summons-scripts.tsv`](../Story-Events-And-Hunts/summons-scripts.tsv), the scripts table of [Summon scenes](../Story-Events-And-Hunts/summons-scenes.md), holds no function row, so it names none of the 6 section 2 rows here, and no step of its steps table quotes one.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `sum_a0001` | scene | 1 | 0 | 0 | 0 |
| `sum_c0001` | scene | 1 | 0 | 0 | 0 |
| `sum_d0001` | scene | 1 | 0 | 0 | 0 |
| `sum_f0001` | scene | 1 | 0 | 0 | 0 |
| `sum_j0001` | scene | 1 | 0 | 0 | 0 |
| `sum_m0001` | scene | 1 | 0 | 0 | 0 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 6 rows.

No string is empty in any tree.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `sum_c0001` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `sum_f0001` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `sum_j0001` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

No string of these scripts carries `{alt-font}`, so every one takes the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)).

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

6 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 6 with 2.

Strings with a choice list per tree: `us` 6, `de` 6, `es` 6, `fr` 6, `it` 6, `in` 6, `kr` 6, `cn` 6, `ch` 6.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `sum_a0001` 2/0, a line that ends in a choice list. `us`: `{speed:8180}Replay？{line}{choice:2}[yes|no]`; `in`: `{spacing:8181}{speed:8180}Replay？{line}{choice:2}[yes|no]`.

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
| rows | 6: 6 in section 2, 0 in section 3 |
| scripts | 6: 0 zone, 6 scene |
| strings per tree | `us` 6, `de` 6, `es` 6, `fr` 6, `it` 6, `in` 6, `kr` 6, `cn` 6, `ch` 6 |
| non-empty strings per tree | `us` 6, `de` 6, `es` 6, `fr` 6, `it` 6, `in` 6, `kr` 6, `cn` 6, `ch` 6 |
| strings with `{alt-font}` | `us` 0, `de` 0, `es` 0, `fr` 0, `it` 0, `in` 0, `kr` 0, `cn` 0, `ch` 0 |
| strings with a choice list | `us` 6, `de` 6, `es` 6, `fr` 6, `it` 6, `in` 6, `kr` 6, `cn` 6, `ch` 6 |
| section 2 rows the scripts table names | 0 |
| section 2 rows a step quotes | 0, in 0 steps |

## Related

- [Summon scenes](../Story-Events-And-Hunts/summons-scenes.md) - the scenes, their text and the scripts that load them.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
