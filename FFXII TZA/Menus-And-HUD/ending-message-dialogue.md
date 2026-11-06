---
title: "Ending message dialogue: every line and caption of the Ending message scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[ending-message-dialogue.tsv](ending-message-dialogue.tsv) has one row per string of sections 2 and 3 of the Ending message scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 32 rows from 1 scene script under `event/`. Every row is a line of section 2; the scripts carry no section 3 caption ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and
  give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- `fieldsign` changes nothing when `0x002642C0` finds no sign record (`0x00355A2E`), and gives the actor the empty
  string at `0x02F8F2A0` instead of a caption when the record's word `+0x0A` is negative (`0x00355A90`-`0x00355AD0`).
- The `lines` column of [`ending-message-scripts.tsv`](../Story-Events-And-Hunts/ending-message-scripts.tsv), the table of [Ending message scripts](../Story-Events-And-Hunts/ending-message-scripts.md), names section 2 rows by the same key: 31 of its rows name 31 of the 32 section 2 rows here.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table |
|---|---|---:|---:|---:|
| `msg_z0001` | scene | 32 | 0 | 31 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 32 rows.

Empty strings per tree: `us` 1, `de` 1, `es` 1, `fr` 1, `it` 1. No `in`, `kr`, `cn` or `ch` string is empty.

1 row is empty in all five of `us`, `de`, `es`, `fr` and `it`: it holds only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 30 | 30 | 30 | 30 |
| `fontex_expand` | 2 | 2 | 2 | 2 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

No string of these scripts holds a choice list.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `msg_z0001` 2/10, a line drawn with the alternate font. `us`: `{alt-font}{speed:8180}{center:8180}{line}You called, my lord?`; `in`: `{spacing:8180}{alt-font}{speed:8180}お呼びですか？`.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script file under `plan_master/<language>/`: `plan_map/...` for a zone script, `event/...` for a scene script |
| `section` | `2` for a line of the message bank, `3` for a caption |
| `id` | the entry number in that section, from 0: the text id a verb passes |
| `us` to `ch` | the string in that language tree, decoded with the tree's font |
| `missing` | the languages whose tree has no string at this key (no such script, or a shorter section), comma-separated; empty when all nine have one |
| `same_bytes` | the groups of languages whose string bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more, and the languages in `missing` take no part |
| `shown_when` | when the game shows the line, in game terms: what starts the function that prints it (a talk, a touch, a scene's start, a request from another function with that function's own start, a slot change), then the tests the printing step runs under, each with its line in the script's decompiled listing; several printing steps are joined with "or". A value the scripts save is named by its label in [saved-value-stores.tsv](../World-Areas-And-Travel/saved-value-stores.tsv), whose rows give each store of it with its own condition. `-` on a caption (section 3): a caption is not shown by a message verb; the field sign verbs give it to an actor as its name text |

An empty cell under a language not in `missing` is an empty string.

## Data

| Fact | Value |
|---|---|
| rows | 32: 32 in section 2, 0 in section 3 |
| scripts | 1: 0 zone, 1 scene |
| strings per tree | `us` 32, `de` 32, `es` 32, `fr` 32, `it` 32, `in` 32, `kr` 32, `cn` 32, `ch` 32 |
| non-empty strings per tree | `us` 31, `de` 31, `es` 31, `fr` 31, `it` 31, `in` 32, `kr` 32, `cn` 32, `ch` 32 |
| strings with `{alt-font}` | `us` 30, `de` 30, `es` 30, `fr` 30, `it` 30, `in` 30, `kr` 30, `cn` 30, `ch` 30 |
| strings with a choice list | `us` 0, `de` 0, `es` 0, `fr` 0, `it` 0, `in` 0, `kr` 0, `cn` 0, `ch` 0 |
| section 2 rows the scripts table names | 31 |

## Related

- [Ending message scripts](../Story-Events-And-Hunts/ending-message-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Ending message scenes](../Story-Events-And-Hunts/ending-message-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
