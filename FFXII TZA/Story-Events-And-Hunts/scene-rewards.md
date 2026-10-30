---
title: "Scene rewards: every item and gil amount the story scripts give or take, by script and function, and how each item is chosen"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00345080, 0x003449A0, 0x0034A6D0, 0x0034B1E0, 0x00346930, 0x00346E30, 0x003459C0, 0x00345520, 0x0032A810"
---

## What it lists

The table has one row for every give or take call in the shipping scripts under `plan_master/us`: 5,198 rows in 355
scripts. 891 of them, in the Trial Mode scripts, are calls that never run (see [Where a script is](#where-a-script-is)). Item ids are the encoded ids of [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md), so a
reward package (`0x9xxx`) gives its gil and items together.

### The verbs

| Verb | Id | Arguments | What it does | Rows |
|---|---|---|---|---:|
| `additemmes` | `0x480` | item, count | opens the "obtained" window (`0x0034A6D0`), waits for it to close, then adds the item (`0x0034B1E0`) | 2,486 |
| `additem_47f` | `0x47F` | item, count, window | adds the item, opening the window first when the third argument is non-zero (`0x003449A0`) | 2,123 |
| `additem` | `0x2E5` | item, count | opens the window and adds the item (`0x00345080`) | 220 |
| `subitem` | `0x2F2` | item, count | takes the count away (`0x003459C0`) | 284 |
| `setitemnum` | `0x55C` | item, count | sets the count held (`0x00345520`) | 5 |
| `addgill` | `0x2E7` | amount | adds gil (`0x00346930`) | 17 |
| `subgill` | `0x2E8` | amount | takes gil (`0x00346E30`) | 63 |

Every item verb goes through `0x0032A810` or `0x0032A830`, which call the inventory change `0x00300B80` or `0x00300BA0` and
floor the count they return at 0 (`0x0032A81C`-`0x0032A820`, `0x0032A83C`-`0x0032A840`); the gil verbs go through
`0x0032A7F0`.

### Where the item comes from

| Source | Rows |
|---|---:|
| written in the call | 4,942 |
| stored by the caller before it requests a shared give routine | 168 |
| one of the values set earlier in the same script | 4 |
| an element of a script table | 4 |
| none: a gil row | 80 |

The four set rows are Montblanc's talk in `rbn_a14`, which gives one of the 31 packages `0x902F`-`0x904D`. The four
table rows are three `subitem` calls in `fon_b01` and one `additemmes` there.

### The shared give routines

231 shipping scripts carry a copy of a shared routine actor that gives, `イベント特殊効果画面`, or its variants `_EV`
and `_RRP`. A
routine function shows the "obtained" window and gives the value of one variable: one of three script globals at
`0xC88`, `0xC8C` and `0xCF0`, or a variable of the script itself. A caller stores the item in that variable and
then requests the routine function.

1. The routine copies hold 2,072 give calls. These are not rows; a copy gives nothing until a caller requests it.
2. 164 requests in shipping scripts reach a routine function that gives, and each becomes a row for every give in
   that function: 168 rows, with the routine in the `through` column.
3. 154 of those items are a literal stored just before the request. The other 14 come from the requesting actor's
   own table: the map vendors (地図屋) of alc_b06, ald_a02, fon_b01, glf_a01, mnt_d01, rbn_a04, var_a01 and
   vic_a03, NPC01 of bul_b02, byu_a01, byu_a04, dst_b01 and dst_b02, and ５０ナッツ of sav_b01.
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
| `explanation` | where the give or take happens, as map name (region): see below; a give reads "Given in", a take (`subitem`, `subgill`) "Taken in"; a Trial Mode reward reads "Given after Stage N" or "Never given from this script" |

### Where a script is

- A zone script is the field whose entry in the `us` zone path table (`0x01EE23A0`, three paths per field id)
  names it. The map name is the area name at that field id in `planmapname.bin`, and the region the name at the
  field's group word in `map_ref.bin`. A name that is only a zone code is left out and the region kept.
- An event script is the scene of every zone script that loads it with `eventread` (`0x0E7`) or `eventread_e8`
  (`0x0E8`) and a literal id; the id names the event through the `us` event path table, four paths per id.
- `mic_b07` has no field id in the path table, so no map loads it.
- Each of the hundred Trial Mode scripts `tri_*` holds all nine reward calls (`additemmes`, packages `0x9123` to
  `0x912B`), each under its own test that the loaded field is that of stage 10, 20, ... or 90 (`nowmap() == 0x048f`
  and so on) ([Trial Mode scripts](trial-mode-scripts.md)).
- So of the 900 rows only 9 give: the call in the script of stages 10, 20, ... 90 whose field matches. The other 891
  never run, and their explanation says which stage's script gives that package.

Actor and function names are the ones the scripts carry.

## Related

- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) - the encoded item ids and what adding one does.
- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md) - the gil total the gil verbs change.
- [Story counter values](story-counter-values.md) - the story points the same scenes set.
