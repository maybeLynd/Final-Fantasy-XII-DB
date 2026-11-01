---
title: "Salikawood dialogue: every line and caption of the Salikawood scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[salikawood-dialogue.tsv](salikawood-dialogue.tsv) has one row per string of sections 2 and 3 of the Salikawood scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 140 rows from 9 zone scripts under `plan_map/`. Section 2 holds the lines (139 rows) and section 3 the captions (1 row) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `salikawood-scripts.tsv`, the table of [Salikawood scripts](../Story-Events-And-Hunts/salikawood-scripts.md), names section 2 rows by the same key: 27 of its rows name 75 of the 139 section 2 rows here. The `quoted_lines` column of its steps table quotes 75 of them, in 102 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `frs_a02` | zone | 12 | 0 | 8 | 8 |
| `frs_a04` | zone | 6 | 0 | 5 | 5 |
| `frs_a05` | zone | 11 | 0 | 9 | 9 |
| `frs_a06` | zone | 40 | 0 | 14 | 14 |
| `frs_b01` | zone | 34 | 0 | 9 | 9 |
| `frs_b02` | zone | 1 | 1 | 1 | 1 |
| `frs_c01` | zone | 2 | 0 | 1 | 1 |
| `frs_c02` | zone | 13 | 0 | 8 | 8 |
| `frs_d01` | zone | 20 | 0 | 20 | 20 |

### Where the languages differ

Every row but one has a string in all nine trees:

- `frs_b02` 3/0 ships only in `in` (`plan_map/frs_b/frs_b02/global/frs_b02.ebp`).

Empty strings per tree: `us` 9, `de` 9, `es` 9, `fr` 9, `it` 9. No `in`, `kr`, `cn` or `ch` string is empty.

9 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `frs_b02` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

No string of these scripts carries `{alt-font}`, so every one takes the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)).

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 1, `de` 1, `es` 1, `fr` 1, `it` 1.

### Choice lists

32 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 21 with 2, 5 with 3, 4 with 11, 2 with 26.

Strings with a choice list per tree: `us` 32, `de` 32, `es` 32, `fr` 32, `it` 32, `in` 32, `kr` 32, `cn` 32, `ch` 32.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `frs_c01` 2/0, a line with a line break (`{line}`). `us`: `{line}{speed:8180}The chocobo refuses to go any further.`; `in`: `{spacing:8181}{line}{speed:8180}チョコボがイヤがっていて、先に進むことができません。`.
- `frs_a06` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.

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
| rows | 140: 139 in section 2, 1 in section 3 |
| scripts | 9: 9 zone, 0 scene |
| strings per tree | `us` 139, `de` 139, `es` 139, `fr` 139, `it` 139, `in` 140, `kr` 139, `cn` 139, `ch` 139 |
| non-empty strings per tree | `us` 130, `de` 130, `es` 130, `fr` 130, `it` 130, `in` 140, `kr` 139, `cn` 139, `ch` 139 |
| strings with `{alt-font}` | `us` 0, `de` 0, `es` 0, `fr` 0, `it` 0, `in` 0, `kr` 0, `cn` 0, `ch` 0 |
| strings with a choice list | `us` 32, `de` 32, `es` 32, `fr` 32, `it` 32, `in` 32, `kr` 32, `cn` 32, `ch` 32 |
| section 2 rows the scripts table names | 75 |
| section 2 rows a step quotes | 75, in 102 steps |

## Related

- [Salikawood scripts](../Story-Events-And-Hunts/salikawood-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Salikawood scenes](../Story-Events-And-Hunts/salikawood-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
