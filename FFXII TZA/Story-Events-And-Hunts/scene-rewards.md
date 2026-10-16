---
title: "Scene rewards: every item and gil amount the story scripts give or take, by script and function, and how each item is chosen"
kind: "reference"
category: "Story, events and hunts"
addresses: "00345080, 003449A0, 0034A6D0, 0034B1E0, 00346930, 00346E30, 003459C0, 00345520, 0032A810"
---

## What it lists

The table has one row for every give or take in the shipping scripts under `plan_master/us`: 5,198 rows in 355
scripts. Item ids are the encoded ids of [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md), so a
reward package (`9XXXh`) gives its gil and items together.

### The verbs

| Verb | Id | Arguments | What it does | Rows |
|---|---|---|---|---:|
| `additemmes` | `480`<sub>h</sub> | item, count | opens the "obtained" window (`0034A6D0`), waits for it to close, then adds the item (`0034B1E0`) | 2,486 |
| `additem_47f` | `47F`<sub>h</sub> | item, count, window | adds the item, opening the window first when the third argument is non-zero (`003449A0`) | 2,123 |
| `additem` | `2E5`<sub>h</sub> | item, count | opens the window and adds the item (`00345080`) | 220 |
| `subitem` | `2F2`<sub>h</sub> | item, count | takes the count away (`003459C0`) | 284 |
| `setitemnum` | `55C`<sub>h</sub> | item, count | sets the count held (`00345520`) | 5 |
| `addgill` | `2E7`<sub>h</sub> | amount | adds gil (`00346930`) | 17 |
| `subgill` | `2E8`<sub>h</sub> | amount | takes gil (`00346E30`) | 63 |

Every item verb goes through `0032A810` or `0032A830`, which call the inventory change `00300B80` or `00300BA0` and
floor the count they return at 0 (`0032A81C`-`0032A820`, `0032A83C`-`0032A840`); the gil verbs go through
`0032A7F0`.

### Where the item comes from

| Source | Rows |
|---|---:|
| written in the call | 4,942 |
| stored by the caller before it requests a shared give routine | 168 |
| one of the values set earlier in the same script | 4 |
| an element of a script table | 4 |
| none: a gil row | 80 |

The four set rows are Montblanc's talk in `rbn_a14`, which gives one of the packages `902F`<sub>h</sub>-`9036`<sub>h</sub>. The four
table rows are three `subitem` calls in `fon_b01` and one `additemmes` there.

### The shared give routines

230 shipping scripts carry a copy of a shared routine actor that gives, `イベント特殊効果画面`, or its variants `_EV`
and `_RRP`. A
routine function shows the "obtained" window and gives the value of one variable: one of three script globals at
`C88`<sub>h</sub>, `C8C`<sub>h</sub> and `CF0`<sub>h</sub>, or a variable of the script itself. A caller stores the item in that variable and
then requests the routine function.

1. The routine copies hold 2,072 give calls. These are not rows; a copy gives nothing until a caller requests it.
2. 164 requests in shipping scripts reach a routine function that gives, and each becomes a row for every give in
   that function: 168 rows, with the routine in the `through` column.
3. 154 of those items are a literal stored just before the request. The other 14 come from the requesting actor's
   own table, for the map vendors and a few others.
4. The three globals are stored 249 times. 191 stores lead to a routine that gives. The other 58 lead to
   `システムメッセージ表示` and `システムメッセージ表示_FADE付`, which show the value as a message id, not an item.

### Scope

The rows are every call in a shipping script outside the routine copies; a talk or event function gives only
when its scene runs it. The
developer scripts `evt_t*` hold 957 more calls, which are not rows.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `actor` | the actor that makes the call, or that requests the routine |
| `function` | its function |
| `verb` | the verb, from the table above |
| `item` | the item id; `gil` for a gil row; `-` when it comes from a table; several ids separated by `/` for a set |
| `item_name` | the item's name; for a reward package, the gil and items it holds |
| `count` | the count or gil amount, or the expression that computes it |
| `item_source` | where the item comes from, as in the table above |
| `through` | for a routine give, the routine actor and function the caller requested; otherwise `-` |

Actor and function names are the ones the scripts carry.

## Related

- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) - the encoded item ids and what adding one does.
- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md) - the gil total the gil verbs change.
- [Story counter values](story-counter-values.md) - the story points the same scenes set.
