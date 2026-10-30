---
title: "Mosphoran Highwaste dialogue: every line and caption of the Mosphoran Highwaste scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[mosphoran-highwaste-dialogue.tsv](mosphoran-highwaste-dialogue.tsv) has one row per string of sections 2 and 3 of the Mosphoran Highwaste scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 151 rows from 8 zone scripts under `plan_map/` and 1 scene script under `event/`. Section 2 holds the lines (143 rows) and section 3 the captions (8 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `mosphoran-highwaste-scripts.tsv`, the table of [Mosphoran Highwaste scripts](../Story-Events-And-Hunts/mosphoran-highwaste-scripts.md), names section 2 rows by the same key: 47 of its rows name 112 of the 143 section 2 rows here. The `quoted_lines` column of its steps table quotes 112 of them, in 157 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `mnt_c0101` | scene | 1 | 0 | 1 | 1 |
| `mnt_a02` | zone | 1 | 0 | 1 | 1 |
| `mnt_b01` | zone | 6 | 0 | 6 | 6 |
| `mnt_b02` | zone | 1 | 0 | 1 | 1 |
| `mnt_b03` | zone | 4 | 0 | 4 | 4 |
| `mnt_b04` | zone | 1 | 1 | 1 | 1 |
| `mnt_b05` | zone | 1 | 0 | 0 | 0 |
| `mnt_c01` | zone | 1 | 0 | 1 | 1 |
| `mnt_d01` | zone | 127 | 7 | 97 | 97 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 151 rows.

Empty strings per tree: `us` 4, `de` 4, `es` 4, `fr` 4, `it` 4. No `in`, `kr`, `cn` or `ch` string is empty.

4 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only control codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `mnt_c01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

No string of these scripts carries `{alt-font}`, so every one takes the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)).

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 1, `de` 1, `es` 1, `fr` 1, `it` 1.

### Choice lists

38 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 30 with 2, 4 with 3, 1 with 7, 2 with 11, 1 with 26.

Strings with a choice list per tree: `us` 38, `de` 38, `es` 38, `fr` 38, `it` 38, `in` 38, `kr` 38, `cn` 38, `ch` 38.

### Reading the text

Each cell is the string decoded with its tree's font. Control codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `mnt_d01` 2/13, a line with a line break (`{line}`). `us`: `{actor-name:8180}{line}{speed:8180}A strong Mist prevents saving.`; `in`: `{spacing:8181}{actor-name:8180}{line}{speed:8180}ミストの干渉により、セーブすることはできません。`.
- `mnt_d01` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `mnt_b04` 3/0, a caption. `us`: `Weathered Rock`; `de`: `Erodierter Felsen`; `in`: `{spacing:8181}風化した岩`.

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
| rows | 151: 143 in section 2, 8 in section 3 |
| scripts | 9: 8 zone, 1 scene |
| strings per tree | `us` 151, `de` 151, `es` 151, `fr` 151, `it` 151, `in` 151, `kr` 151, `cn` 151, `ch` 151 |
| non-empty strings per tree | `us` 147, `de` 147, `es` 147, `fr` 147, `it` 147, `in` 151, `kr` 151, `cn` 151, `ch` 151 |
| strings with `{alt-font}` | `us` 0, `de` 0, `es` 0, `fr` 0, `it` 0, `in` 0, `kr` 0, `cn` 0, `ch` 0 |
| strings with a choice list | `us` 38, `de` 38, `es` 38, `fr` 38, `it` 38, `in` 38, `kr` 38, `cn` 38, `ch` 38 |
| section 2 rows the scripts table names | 112 |
| section 2 rows a step quotes | 112, in 157 steps |

## Related

- [Mosphoran Highwaste scripts](../Story-Events-And-Hunts/mosphoran-highwaste-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Mosphoran Highwaste scenes](../Story-Events-And-Hunts/mosphoran-highwaste-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every control code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
