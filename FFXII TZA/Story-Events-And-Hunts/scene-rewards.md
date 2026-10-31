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

### Sellers, fees and refunds

The 14 map sellers keep the maps they sell in one array and the prices in another, filled from price ids with
`getprice` ([Price list](../Rewards-EXP-Gil-And-Loot/price-list.md)) when the talk starts. The player picks a
map, `subgill` takes the price at the same index, and the map goes into `0xC88` before the request (alc_b06
`地図屋.talk` :1470-1473, :1559, :1566). A seller's `additemmes` row lists all its maps, its `subgill` row the price
of each.

Other takes and gives read a value the script sets:

- Gurdy (`ガーディ`, `NPC_MOG_GARDY`, `talk_gardy`) charges a chocobo hire fee, one price id per place: "Welcome to
  the chocobo stables. Only [value] gil should you wish to hire one, kupo!" (var_a01 `NPC_MOG_GARDY.talk`
  :4508-4571).
- The Chopmaster (`NPC_GUILD`) of the five Archades shops sells a Pinewood Chop for 20,000 gil (alc_b05
  `NPC_GUILD.talk` :1286-1306).
- Jules asks a fee in two scenes: 1,500 gil in ald_a0180 (`ジュール登場2` :158-175) and 2,500 gil in alc_a0280
  (`タクシーの乗り方2` :137-151), where the Cab Attendant has just asked 1,000,000 gil for a ride without a chop
  (:108). Each fee is taken when the scene returns to the map (ald_a01 :4810, :5257; alc_f01 :8073, :8391).
- The Hunters' Camp Outfitters (`二級男11`) sells 31 reward packages, each once and at its own price, opened by the
  trophies given to the three Bangaa brothers (fon_b01 :12951-13131). The brothers (`バンガ05`, `バンガ13`,
  `バンガ15`) offer to take each trophy the player holds, in the order of one 30-trophy table (:9086, :9312-9351).
- Bhujerba's Madhu buyer (`NPC01`) and South Bank Village's fish buyer pay before they ask: a reward package adds the
  gil (`0x908B`, 1,000 gil; `0x907D`-`0x907F`, 10, 100 and 200 gil a fish), and `subgill` takes back the gil it
  added when the player declines (byu_a01 :9019-9091, dst_b01 :17410-17457).
- At 99,998,999 gil or more (99,990,009 for the fish) those buyers skip the package, and an accepted sale adds the
  gil with `addgill`.
- A Pharos orb (`o_tama`) gives 3 Black Orbs per point of its count, at most 9,999. The count starts at 1, each
  lesser orb (`tama01`-`tama05`) left untaken for its 270 frames adds 1 through `o_tama.map_bright`, and the gift
  sets it back to 1 (rbl_b01 :929-931, :1471, :1522-1592, :2042-2063).

### Scope

The rows are every call in a shipping script outside the routine copies; a talk or event function gives only
when its scene runs it. The
developer scripts `evt_t*` hold 957 more calls, which are not rows.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `actor` | the actor that makes the call, or that requests the routine |
| `actor_name` | the actor's name tag in game, from its name pair in [NPC names](../Characters-And-Objects/npc-names.md) (`npc-names-maps.tsv`): `first / second` when the tag changes once the player has talked to the character, pairs separated by `; ` when the script gives the actor more than one; `-` for an actor with no name pair, such as the directors (`監督`, `トライアル監督`) and the touch areas (`魂レクト`) |
| `function` | its function |
| `verb` | the verb, from the table above |
| `item` | the item id; `gil` for a gil row; several ids separated by `/` for a set, a seller's list or a table |
| `item_name` | the item's name; for a reward package, the gil and items it holds |
| `count` | the count or gil amount, or the rule that sets it: a price with its price id, a fee, a refund, every one the player holds, or a game counter with its global and the lines that change it |
| `item_source` | where the item comes from, as in the table above, and for a seller or a table what is chosen |
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
