---
title: "Nalbina Fortress dialogue: every line and caption of the Nalbina Fortress scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[nalbina-fortress-dialogue.tsv](nalbina-fortress-dialogue.tsv) has one row per string of sections 2 and 3 of the Nalbina Fortress scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 187 rows from 5 zone scripts under `plan_map/` and 5 scene scripts under `event/`. Section 2 holds the lines (184 rows) and section 3 the captions (3 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of [`nalbina-fortress-scripts.tsv`](../Story-Events-And-Hunts/nalbina-fortress-scripts.tsv), the table of [Nalbina Fortress scripts](../Story-Events-And-Hunts/nalbina-fortress-scripts.md), names section 2 rows by the same key: 60 of its rows name 156 of the 184 section 2 rows here. The `quoted_lines` column of its steps table quotes 156 of them, in 213 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `naf_a0100` | scene | 31 | 0 | 31 | 31 |
| `naf_a0201` | scene | 6 | 0 | 6 | 6 |
| `naf_b0100` | scene | 12 | 0 | 12 | 12 |
| `naf_b0400` | scene | 4 | 0 | 4 | 4 |
| `naf_b0401` | scene | 21 | 0 | 21 | 21 |
| `naf_a01` | zone | 68 | 1 | 66 | 66 |
| `naf_a02` | zone | 13 | 0 | 13 | 13 |
| `naf_b01` | zone | 1 | 0 | 1 | 1 |
| `naf_b02` | zone | 26 | 0 | 1 | 1 |
| `naf_b04` | zone | 2 | 2 | 1 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 187 rows.

Empty strings per tree: `us` 11, `de` 11, `es` 12, `fr` 11, `it` 11. No `in`, `kr`, `cn` or `ch` string is empty.

11 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

Empty in some trees only:

- `naf_a0100` 2/25: empty in `es`.

The rows that carry `{alt-font}` in some trees only:

- `naf_a0100` 2/25: in `us`, `de`, `fr`, `it`, `in`, `kr`, `cn` and `ch`; empty in the other trees.
- `naf_a01` 2/53: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.
- `naf_a01` 2/56: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 103 | 103 | 103 | 103 |
| `fontex_expand` | 84 | 84 | 84 | 84 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

11 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 6 with 2, 2 with 3, 2 with 11, 1 with 26.

Strings with a choice list per tree: `us` 11, `de` 11, `es` 11, `fr` 11, `it` 11, `in` 11, `kr` 11, `cn` 11, `ch` 11.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

A code the table writes by its own bytes is the code with those bytes on Text codes: `{0F3D:8181}` is `0F 3D` with the payload `81 81`. Such codes in all nine columns: `{0F3D:...}` 200.

Examples, by script, section and id:

- `naf_a01` 2/33, a line with a line break (`{line}`). `us`: `Basch{line}{0F3D:8185}Now, try opening the gate.`; `in`: `{spacing:8181}バッシュ{line}{0F3D:8185}さあ、その扉を開けてくれ。`.
- `naf_a0100` 2/10, a line drawn with the alternate font. `us`: `{alt-font}{speed:8180}{center:8180}{line}Well, can you stand?`; `in`: `{spacing:8180}{alt-font}{speed:8180}さあ{blank}立ち上がるんだ`.
- `naf_b02` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `naf_a01` 3/0, a caption. `us`: `Iron Gate`; `de`: `Eisenpforte`; `in`: `{spacing:8181}鉄の門扉`.

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
| rows | 187: 184 in section 2, 3 in section 3 |
| scripts | 10: 5 zone, 5 scene |
| strings per tree | `us` 187, `de` 187, `es` 187, `fr` 187, `it` 187, `in` 187, `kr` 187, `cn` 187, `ch` 187 |
| non-empty strings per tree | `us` 176, `de` 176, `es` 175, `fr` 176, `it` 176, `in` 187, `kr` 187, `cn` 187, `ch` 187 |
| strings with `{alt-font}` | `us` 105, `de` 105, `es` 104, `fr` 105, `it` 105, `in` 103, `kr` 103, `cn` 103, `ch` 103 |
| strings with a choice list | `us` 11, `de` 11, `es` 11, `fr` 11, `it` 11, `in` 11, `kr` 11, `cn` 11, `ch` 11 |
| section 2 rows the scripts table names | 156 |
| section 2 rows a step quotes | 156, in 213 steps |

## Related

- [Nalbina Fortress scripts](../Story-Events-And-Hunts/nalbina-fortress-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Nalbina Fortress scenes](../Story-Events-And-Hunts/nalbina-fortress-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
