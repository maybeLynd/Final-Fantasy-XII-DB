---
title: "Lowtown dialogue: every line and caption of the Lowtown scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[lowtown-dialogue.tsv](lowtown-dialogue.tsv) has one row per string of sections 2 and 3 of the Lowtown scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 529 rows from 4 zone scripts under `plan_map/` and 7 scene scripts under `event/`. Section 2 holds the lines (512 rows) and section 3 the captions (17 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `lowtown-scripts.tsv`, the table of [Lowtown scripts](../Story-Events-And-Hunts/lowtown-scripts.md), names section 2 rows by the same key: 161 of its rows name 502 of the 512 section 2 rows here.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table |
|---|---|---:|---:|---:|
| `slm_a0100` | scene | 21 | 0 | 20 |
| `slm_a0101` | scene | 15 | 0 | 15 |
| `slm_a0280` | scene | 14 | 0 | 14 |
| `slm_a0300` | scene | 21 | 0 | 21 |
| `slm_a0380` | scene | 26 | 0 | 26 |
| `slm_a0381` | scene | 20 | 0 | 20 |
| `slm_z0100` | scene | 26 | 0 | 25 |
| `slm_a01` | zone | 181 | 10 | 178 |
| `slm_a02` | zone | 97 | 5 | 96 |
| `slm_a03` | zone | 74 | 1 | 72 |
| `slm_a04` | zone | 17 | 1 | 15 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 529 rows.

Empty strings per tree: `us` 9, `de` 9, `es` 9, `fr` 9, `it` 9. No `in`, `kr`, `cn` or `ch` string is empty.

9 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only control codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows that carry `{alt-font}` in some trees only:

- `slm_a0380` 2/18: in `us`, `de`, `es`, `fr` and `it`, not in `in`, `kr`, `cn` and `ch`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 137 | 137 | 137 | 137 |
| `fontex_expand` | 392 | 392 | 392 | 392 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)).

### Choice lists

19 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 17 with 2, 2 with 3.

Strings with a choice list per tree: `us` 19, `de` 19, `es` 19, `fr` 19, `it` 19, `in` 19, `kr` 19, `cn` 19, `ch` 19.

### Reading the text

Each cell is the string decoded with its tree's font. Control codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `slm_a01` 2/51, a line with a line break (`{line}`). `us`: `{instant:8181}Storehouse No. 5{line}The door is locked.`; `in`: `{spacing:8181}{instant:8181}５番倉庫{line}カギがかかっている……。`.
- `slm_z0100` 2/22, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}Listen to me, Basch.`; `in`: `{spacing:8180}{speed:8180}{alt-font}忘れるな{blank}バッシュ`.
- `slm_a0100` 2/0, a line that ends in a choice list. `us`: `{speed:8180}View scene again?{line}{choice:2}[Yes|No]`; `in`: `{spacing:8181}{speed:8180}Replay？{line}{choice:2}[yes|no]`.
- `slm_a01` 3/0, a caption. `us`: `Streets of Rabanastre`; `de`: `Treppe zur Oberstadt`; `in`: `{spacing:8181}上層への階段`.

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
| rows | 529: 512 in section 2, 17 in section 3 |
| scripts | 11: 4 zone, 7 scene |
| strings per tree | `us` 529, `de` 529, `es` 529, `fr` 529, `it` 529, `in` 529, `kr` 529, `cn` 529, `ch` 529 |
| non-empty strings per tree | `us` 520, `de` 520, `es` 520, `fr` 520, `it` 520, `in` 529, `kr` 529, `cn` 529, `ch` 529 |
| strings with `{alt-font}` | `us` 138, `de` 138, `es` 138, `fr` 138, `it` 138, `in` 137, `kr` 137, `cn` 137, `ch` 137 |
| strings with a choice list | `us` 19, `de` 19, `es` 19, `fr` 19, `it` 19, `in` 19, `kr` 19, `cn` 19, `ch` 19 |
| section 2 rows the scripts table names | 502 |

## Related

- [Lowtown scripts](../Story-Events-And-Hunts/lowtown-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Lowtown scenes](../Story-Events-And-Hunts/lowtown-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every control code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
