[Home](../../README.md) / [Story, events and hunts](README.md) / Garamsythe Waterway scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Garamsythe Waterway scenes: each story scene with its dialogue, story counter values and what follows | reference | Story, events and hunts | Scenes and scripts by area / Rabanastre and Giza Plains | The scene scripts of the Garamsythe Waterway: the zone function that loads each one, every line it holds in the game's own words, the story counter values written with it, and what follows. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00 |

## What it lists

The table [garamsythe-waterway-scenes.tsv](garamsythe-waterway-scenes.tsv) has one row per scene script of the
Garamsythe Waterway under `plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`)
and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`,
which `0x0032FCA0` reads from index `4n` of the event file table ([event
scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `grm_a0200` | `237` | East Waterway Control, field 312 | 5 | story counter 180, then South Sprawl (Lowtown), field `702` |
| `grm_a0380` | `715` | North Spur Sluiceway | 0 | - |
| `grm_a0400` | `317` | East Spur Stairs | 22 | - |
| `grm_a0401` | `318` | East Spur Stairs | 7 | - |
| `grm_a0480` | `738` | East Spur Stairs | 9 | - |
| `grm_b0200` | `319` | East Sluice Control, field 319 | 7 | `grm_b0202` (event `238`) |
| `grm_b0202` | `238` | East Sluice Control, field 319 | 25 | - |
| `grm_b0280` | `716` | East Sluice Control, field 319 | 14 | - |
| `grm_c0100` | `310` | Southern Sluiceway, field 326 | 0 | `grm_c0101` (event `311`) |
| `grm_c0101` | `311` | Southern Sluiceway, field 326 | 0 | - |
| `grm_d0100` | `312` | Overflow Cloaca, field 329 | 1 | `grm_d0102` (event `236`) |
| `grm_d0102` | `236` | Overflow Cloaca, field 329 | 3 | story counter 285, then North Sprawl (Lowtown), field `701` |
| `grm_f0100` | `314` | No. 1 Cloaca | 0 | `grm_f0101` (event `315`) |
| `grm_f0101` | `315` | No. 1 Cloaca | 1 | - |
| `grm_g0100` | `235` | Overflow Cloaca, field 1145 | 11 | story counter 33, then Muthru Bazaar (Rabanastre), field `290` |
| `grm_g0101` | `267` | Overflow Cloaca, field 1145 | 4 | `grm_g0100` (event `235`) |

### What the scenes give

- `grm_a0200`, in East Waterway Control (field 312) at story counter 175, holds the insurgents' report ("Squads 3
  through 6 are in place. They stand ready." ... "By nightfall, we must ensure all our men are in place."); its first
  entry is "View scene again?" (Yes / No), and 180 follows it.
- `grm_a0380`, loaded in North Spur Sluiceway from story counter 180 to 189, holds no text.
- `grm_a0400`, in East Spur Stairs, holds the meeting with Balthier and Fran ("What happened?" ... "Myself, Fran, and
  you. We're working together now." ... "The thought never crossed my mind."); its director shows system message 66,
  "[value] and [value] join the party!", which the game fills with Balthier and Fran.
- `grm_a0401`, played at the first talk with the bodies in East Spur Stairs, holds the talk of the insurgents
  ("Insurgents. Most like they thought to take advantage of a lax watch while the fete's on..." ... "If a dungeon's
  waiting for us at the end of the night, it had best have a change of wardrobe.").
- `grm_a0480`, in East Spur Stairs from story counter 235 to 243, holds Balthier's talk on gambits ("As I thought. You
  don't know much about gambits yet, do you?") and the system messages "Gambits has been added to the Party Menu." and
  "Party has been added to the Party Menu."; its first entry is "View scene again?" (Yes / No).
- `grm_b0200` and `grm_b0202` are loaded together for the fight in East Sluice Control (field 319). `grm_b0200` holds
  the insurgents' calls ("Close ranks! Bring her down!" ... "And our troubles with them."), `grm_b0202` the meeting
  with Amalia ("What's your name?" / "Amalia." ... "You should come with us. Better than being by yourself.").
- `grm_b0280`, in East Sluice Control (field 319), holds Amalia's terms ("I shall accompany you until we find my
  companions." / "No longer." ... "Well, what are we waiting for?"); its director shows system message 48, "[value]
  joins the party as a guest!", which the game fills with Amalia.
- `grm_c0100` and `grm_c0101` (Southern Sluiceway, field 326) and `grm_f0100` and `grm_f0101` (No. 1 Cloaca) are
  loaded in pairs when the fight begins, and `pos_z0000` follows each fight. They hold no text of their own:
  `grm_f0101` holds one empty entry, the others no entry.
- `grm_f0101` holds a switch on the current field (`nowmap`) that gives the Esper of that field when the party does
  not hold it; in No. 1 Cloaca (field 342) that is Cúchulainn (`0xC016`, [Quickening and Esper
  list](../Battle-Actions/quickening-and-esper-list.md)).
- `grm_f0101`: in the Cloister of Flame (field 415) its switch gives Belias (`0xC012`) together with SecondJob
  (`0xC01F`), the presence bit of the Second Board ([Scene rewards](scene-rewards.md)).
- `grm_d0100` and `grm_d0102` are loaded together for the fight in Overflow Cloaca (field 329). `grm_d0100` holds only
  the Japanese choice list `もう一度？` (`もう一度` / `やめる`); `grm_d0102` holds "Stand where you are!" and "Now is not the
  time." after "View scene again?" (Yes / No), and 285 follows the fight.
- `grm_g0101` and `grm_g0100`, loaded in Overflow Cloaca (field 1145) below story counter 27, frame the fight with the
  rats ("Vaan! Hurry it up or they'll find us!" ... "One...two...three more. Right. Time to clean house."; "Wow, Vaan.
  You got 'em all yourself?" ... "If Migelo finds out we've been down here, he'll tan our hides."); 33 follows.
- No scene gives an item other than the Espers of `grm_f0101`; the party changes only in the loading functions.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes`¹, which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00348DF0` |

</details>

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Garamsythe Waterway scripts](garamsythe-waterway-scripts.md)): its actors, camera shots, motions, effects, music and loads. An entry that the `us` tree ships in Japanese gets an English sentence
first; the entry follows after `Authored text`, with its English in brackets.

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump`¹ count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00354D00` |

</details>

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

- [Garamsythe Waterway scripts](garamsythe-waterway-scripts.md) - every observable function of the same scripts.
- [Location title scenes](titles-scenes.md) - the location titles fields load on the first arrival.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 29 calls with 6 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00229EA0`](../Graphics/effect-drawing.md) (on effect drawing) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264D60`](../Menus-And-HUD/aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x00352A50`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00352EC0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003534F0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00356B70`](../Characters-And-Objects/npc-names.md) (on npc names)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | is called by | [`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**World, areas and travel** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | is called by | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x003522C0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x00353080`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |

</details>
