---
title: "Tomb of Raithwall scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [tomb-of-raithwall-scenes.tsv](tomb-of-raithwall-scenes.tsv) has one row per scene script of The Tomb of
Raithwall under `plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`) and
`eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which
`0x0032FCA0` reads from index `4n` of the event file table ([event
scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `rwg_a0100` | `338` | Valley of the Dead | 23 | - |
| `rwg_a0180` | `346` | Valley of the Dead | 0 | `rwg_a0181` (event `347`) |
| `rwg_a0181` | `347` | Valley of the Dead | 1 | `pos_z0000` (event `427`) |
| `rwg_b0100` | `330` | Hall of the Destroyer | 1 | `rwg_b0102` (event `332`) |
| `rwg_b0101` | `331` | Hall of the Destroyer | 1 | - |
| `rwg_b0102` | `332` | Hall of the Destroyer | 0 | - |
| `rwg_b0103` | `324` | Hall of the Destroyer | 3 | - |
| `rwg_b0200` | `333` | Hall of the Sentinel | 1 | `rwg_b0202` (event `335`) |
| `rwg_b0201` | `334` | Hall of the Sentinel | 1 | - |
| `rwg_b0202` | `335` | Hall of the Sentinel | 0 | - |
| `rwg_c0100` | `322` | Royal Passage | 12 | - |
| `rwg_d0100` | `336` | Cloister of Flame | 0 | `rwg_d0101` (event `337`) |
| `rwg_d0101` | `337` | Cloister of Flame | 13 | - |
| `rwg_d0102` | `323` | Cloister of Flame | 9 | - |
| `rwg_e0100` | `339` | Chamber of First Light | 6 | - |

### What the scenes give

- `rwg_a0100`, played in the Valley of the Dead after the Garuda fight, holds the history of King Raithwall and his
  relics ("Raithwall left three relics signifying descent from the Dynast-King." ... "The last of these relics was the
  Dawn Shard."); its first entry is the choice "View scene again?" (Yes / No).
- `rwg_a0180` and `rwg_a0181` are loaded together when the Garuda fight begins, and `pos_z0000` follows the fight.
  `rwg_a0181` holds only the Japanese choice list `もう一度？` (`もう一度` / `やめる`).
- `rwg_b0100` ("Fight or run, we better decide fast!") and `rwg_b0102` are loaded together for the first Demon Wall
  fight, in Hall of the Destroyer, and `rwg_b0200` ("The wall comes. We must be quick! Together we can bring it
  down!") and `rwg_b0202` for the second, in Hall of the Sentinel. `rwg_b0101` and `rwg_b0201`, loaded by the fight
  functions, hold only the Japanese choice list `リプレイ？` (`する` / `しない`).
- `rwg_b0103`, in Hall of the Destroyer below story counter 1364, holds the talk of the devices ("What was that
  thing?" ... "The finer points of their operation elude me, but they're handy all the same. What more need a sky
  pirate know?").
- `rwg_c0100`, in Royal Passage at 1372, holds the talk at the plundered tomb ("It wounds me to look on as they
  pillage so solemn a place." ... "I can hear its call.").
- `rwg_d0102`, in the Cloister of Flame, holds the talk of the Mist ("Fog? Underground?" / "Not fog—Mist."); its first
  entry is the Japanese choice list `プレイ？` (`左VER` / `右VER` / `イベント飛ばす`).
- `rwg_d0100` and `rwg_d0101` are loaded together when the Belias fight begins. `rwg_d0101` holds the talk of the
  Dynast-King's Esper ("Not so. The Esper is the Dynast-King's treasure.").
- `rwg_d0101` holds a switch on the current field (`nowmap`) that gives the Esper of that field when the party does
  not hold it; in the Cloister of Flame (field 415) that is Belias (`0xC012`, [Quickening and Esper
  list](../Battle-Actions/quickening-and-esper-list.md)), given together with SecondJob (`0xC01F`), the presence
  bit of the Second Board ([Scene rewards](scene-rewards.md)).
- `rwg_e0100`, in the Chamber of First Light below 1390, gives the Dawn Shard from its own functions
  (`DIRECTOR.EV_e0118`) and holds the lines "Rasler..." / "You will be avenged."
- No scene changes the party.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Tomb of Raithwall scripts](tomb-of-raithwall-scripts.md)): its actors, camera shots, motions, effects, music and loads. An entry that the `us` tree ships in Japanese gets an English sentence
first; the entry follows after `Authored text`, with its English in brackets.

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump` (`0x00354D00`) count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)`; a scene with no non-empty entry: one sentence of what its script does; an entry the `us` tree ships in Japanese: an English sentence, then `Authored text (<its English>): ` and the entry |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Tomb of Raithwall scripts](tomb-of-raithwall-scripts.md) - every observable function of the same scripts.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032FCA0` calls `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- Core runtime: `0x00354D00` calls `0x00229EA0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Resource: `0x0032FCA0` calls `0x002DF980`, `0x0032E400`, `0x0032E620`; `0x00351880` calls `0x001D6A70`; `0x003529E0` calls
  `0x001D6A70`; those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md),
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
- Script VM: `0x00264D60` is called by `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`,
  `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0`; `0x00348DF0` calls `0x00267E10`; `0x00348DF0` is called by `0x00349800`;
  `0x00351880` calls `0x00267E10`; `0x003529E0` calls `0x00267E10`, `0x00267F90`; `0x00354D00` calls `0x00267E10`.
- Script VM: those functions are documented on [archades scenes](archades-scenes.md),
  [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md),
  [npc names](../Characters-And-Objects/npc-names.md),
  [force fight mode](../Engine-Core/force-fight-mode.md); and on
  [native commands](../Scripts-And-Script-Commands/native-commands.md).
- World area: `0x0032FCA0` is called by `0x0032FC30`; `0x003522C0` calls `0x0032FC30`; `0x00353080` calls `0x0032FC30`; those
  functions are documented on [debug menu](../Engine-Core/debug-menu.md).
