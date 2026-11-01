---
title: "Henne Mines dialogue: every line and caption of the Henne Mines scripts in all nine languages"
kind: "reference"
category: "Menus and HUD"
addresses: "0x00348DF0, 0x0034ADA0, 0x00264D60, 0x00264D90, 0x00355A00, 0x00357120, 0x002AC825, 0x002AC957, 0x002AD151, 0x001E9D20, 0x001FDD60, 0x00674A00, 0x001B6350"
---

## What it lists

[henne-mines-dialogue.tsv](henne-mines-dialogue.tsv) has one row per string of sections 2 and 3 of the Henne Mines scripts, with the string in each of the nine language trees (`us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch`): 129 rows from 15 zone scripts under `plan_map/` and 3 scene scripts under `event/`. Section 2 holds the lines (90 rows) and section 3 the captions (39 rows) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### How a script finds a row

A row's key is the script, the section and the text id, the entry number in that section:

- `mes` (`0x00348DF0`), which the verbs `ames`, `amese`, `amest` and `ames_1fe` reach, and `aask_1ff` (`0x0034ADA0`) look the text id up in the section 2 of the script that issues them through `0x00264D60`, which keeps the low 24 bits of the id. The field-sign and gauge-label verbs read section 2 the same way.
- `fieldsign` (`0x00355A00`) and `fieldsignmesbyid` (`0x00357120`) read a section 3 caption through `0x00264D90` and give it to the actor as its name text ([NPC names](../Characters-And-Objects/npc-names.md)).
- The `lines` column of `henne-mines-scripts.tsv`, the table of [Henne Mines scripts](../Story-Events-And-Hunts/henne-mines-scripts.md), names section 2 rows by the same key: 43 of its rows name 58 of the 90 section 2 rows here. The `quoted_lines` column of its steps table quotes 58 of them, in 70 steps.

### The scripts

| Script | Kind | Section 2 rows | Section 3 rows | Named in the scripts table | Quoted by a step |
|---|---|---:|---:|---:|---:|
| `hne_a0700` | scene | 9 | 0 | 9 | 9 |
| `hne_b0102` | scene | 22 | 0 | 22 | 22 |
| `hne_e0101` | scene | 1 | 0 | 1 | 1 |
| `hne_a01` | zone | 4 | 5 | 4 | 4 |
| `hne_a02` | zone | 4 | 3 | 4 | 4 |
| `hne_a03` | zone | 3 | 1 | 0 | 0 |
| `hne_a04` | zone | 1 | 2 | 0 | 0 |
| `hne_a05` | zone | 0 | 3 | 0 | 0 |
| `hne_a06` | zone | 0 | 2 | 0 | 0 |
| `hne_a07` | zone | 28 | 1 | 3 | 3 |
| `hne_a08` | zone | 0 | 1 | 0 | 0 |
| `hne_b01` | zone | 2 | 2 | 2 | 2 |
| `hne_c01` | zone | 7 | 3 | 4 | 4 |
| `hne_c02` | zone | 1 | 2 | 1 | 1 |
| `hne_c03` | zone | 1 | 3 | 1 | 1 |
| `hne_c04` | zone | 2 | 7 | 2 | 2 |
| `hne_d01` | zone | 4 | 3 | 4 | 4 |
| `hne_e01` | zone | 1 | 1 | 1 | 1 |

### Where the languages differ

Every script ships in all nine trees with the same number of strings in each, so every row has a string in every language: the `missing` column is empty in all 129 rows.

Empty strings per tree: `us` 9, `de` 9, `es` 9, `fr` 9, `it` 9. No `in`, `kr`, `cn` or `ch` string is empty.

9 rows are empty in all five of `us`, `de`, `es`, `fr` and `it`: all of them hold only text codes in `in`, `kr`, `cn` and `ch`, such as `{spacing:8181}`.

The rows whose `us` to `it` strings hold Japanese text, kana or kanji:

- `hne_b01` 2/0: in `us`, `de`, `es`, `fr` and `it`.
- `hne_e01` 2/0: in `us`, `de`, `es`, `fr` and `it`.

### The alternate font and the expansion lists

`{alt-font}` is the escape `0F 21`, which switches the string to the alternate font record (`0x002AD151`) ([Text codes](text-codes.md)), font 3, `fontex_subtitle` ([Text drawing](text-drawing.md), [Fonts](fonts.md)).

In the `in`, `kr`, `cn` and `ch` trees the expansion codes of a string draw their glyphs from the expansion list keyed by `0x00674A00` of the script's path, `event\<folder>\<name>` or `plan_map\<folder>\<name>` (`0x001B6350`): `0x001E9D20` binds the running font's list for that key, which `0x001FDD60` finds in the font's map `+0xA8` ([Fonts](fonts.md), Expansion lists).

A string that carries `{alt-font}` therefore takes the list of `fontex_subtitle`, and every other string the list of `fontex_expand` ([Font expansion lists](fonts-expansion-lists.md)). Non-empty strings per list:

| List | `in` | `kr` | `cn` | `ch` |
|---|---:|---:|---:|---:|
| `fontex_subtitle` (with `{alt-font}`) | 31 | 31 | 31 | 31 |
| `fontex_expand` | 98 | 98 | 98 | 98 |

No cell of the `in`, `kr`, `cn` or `ch` columns holds `{exp:...}`: every expansion code there has a glyph in its list. No `us` font asks for a `.fex`, so in the `us` to `it` columns `{alt-font}` changes the font only ([Fonts](fonts.md)); the table writes an expansion code there as `{exp:0xN}`, N its ordinal: `us` 2, `de` 2, `es` 2, `fr` 2, `it` 2.

### Choice lists

18 `us` strings end in a choice list, `{choice:n}[a|b|...]` with its n options between the brackets: token `0x0E` (`0x002AC825`) ([Text codes](text-codes.md), Choice lists). Options per list in `us`: 11 with 2, 4 with 3, 2 with 11, 1 with 26.

Strings with a choice list per tree: `us` 18, `de` 18, `es` 18, `fr` 18, `it` 18, `in` 18, `kr` 18, `cn` 18, `ch` 18.

### Reading the text

Each cell is the string decoded with its tree's font. Text codes are written as placeholders, `{name}` or `{name:payload}` with the payload bytes in hex; [Text codes](text-codes.md) gives each code. A backslash comes before a literal backslash, brace, square bracket or bar of the game text.

Examples, by script, section and id:

- `hne_a01` 2/1, a line with a line break (`{line}`). `us`: `{speed:8180}{line}You hear a gate move deep within the mine.`; `in`: `{spacing:8181}{speed:8180}{line}坑道の奥から、フェンスの開閉する音が聞こえた。`.
- `hne_b0102` 2/13, a line drawn with the alternate font. `us`: `{speed:8180}{alt-font}{center:8180}{line}Manufacted nethicite.`; `in`: `{spacing:8180}{speed:8180}{alt-font}─{advance:8098}─人造破魔石`.
- `hne_a07` 2/16, a line that ends in a choice list. `us`: `{speed:8180}Save or load?{line}{choice:3}[Cancel|Load|Save]`; `in`: `{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]`.
- `hne_a01` 3/0, a caption. `us`: `Ore Separation`; `de`: `Veredlungsstätten-Tor`; `in`: `{spacing:8181}分別作業場への扉`.

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
| rows | 129: 90 in section 2, 39 in section 3 |
| scripts | 18: 15 zone, 3 scene |
| strings per tree | `us` 129, `de` 129, `es` 129, `fr` 129, `it` 129, `in` 129, `kr` 129, `cn` 129, `ch` 129 |
| non-empty strings per tree | `us` 120, `de` 120, `es` 120, `fr` 120, `it` 120, `in` 129, `kr` 129, `cn` 129, `ch` 129 |
| strings with `{alt-font}` | `us` 31, `de` 31, `es` 31, `fr` 31, `it` 31, `in` 31, `kr` 31, `cn` 31, `ch` 31 |
| strings with a choice list | `us` 18, `de` 18, `es` 18, `fr` 18, `it` 18, `in` 18, `kr` 18, `cn` 18, `ch` 18 |
| section 2 rows the scripts table names | 58 |
| section 2 rows a step quotes | 58, in 70 steps |

## Related

- [Henne Mines scripts](../Story-Events-And-Hunts/henne-mines-scripts.md) - what each function of these scripts shows, with the text ids of its lines.
- [Henne Mines scenes](../Story-Events-And-Hunts/henne-mines-scenes.md) - the scenes these scripts load.
- [EBP text sections](../EBP-Script-Files/ebp-text-sections.md) - the layout of sections 2 and 3, the lookups and the verbs that read them.
- [Text codes](text-codes.md) - every text code and the choice list.
- [Fonts](fonts.md) - how a character code becomes a glyph, and the expansion lists.
- [Font expansion lists](fonts-expansion-lists.md) - every list with the script path it belongs to.
- [Message windows](message-windows.md) - the window a line is shown in.
- [NPC names](../Characters-And-Objects/npc-names.md) - the name text a caption becomes.
