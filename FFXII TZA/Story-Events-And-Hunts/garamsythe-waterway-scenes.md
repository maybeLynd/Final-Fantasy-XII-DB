---
title: "Garamsythe Waterway scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

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
  `grm_f0101` holds one empty entry, the others none.
- `grm_f0101` holds a switch on the current field (`nowmap`) that gives the Esper of that field when the party does
  not hold it; in No. 1 Cloaca (field 342) that is Cúchulainn (`0xC016`, [Quickening and Esper
  list](../Battle-Actions/quickening-and-esper-list.md)).
- `grm_f0101`: in the Cloister of Flame (field 415) its switch gives Belias (`0xC012`) together with SecondJob
  (`0xC01F`), the presence bit of the Second Board ([Scene rewards](scene-rewards.md)).
- `grm_d0100` and `grm_d0102` are loaded together for the fight in Overflow Cloaca (field 329). `grm_d0100` holds only
  the Japanese choice list `もう一度？` (`もう一度` / `やめる`); `grm_d0102` holds "Stand where you are!" and "Now is not the
  time." after "View scene again?" (Yes / No), and 285 follows the fight.
- `grm_g0101` and `grm_g0100`, loaded in Overflow Cloaca (field 1145) below story counter 27, frame the fight with the
  rats ("Vaan! Hurry it up or they'll find us!" ... "Time to clean house."; "Wow, Vaan. You got 'em all yourself?" ...
  "If Migelo finds out we've been down here, he'll tan our hides."); 33 follows.
- No scene gives an item other than the Espers of `grm_f0101`; the party changes only in the loading functions.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Garamsythe Waterway scripts](garamsythe-waterway-scripts.md)): its actors, camera shots, motions, effects, music and loads. An entry that the `us` tree ships in Japanese gets an English sentence
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

## Related

- [Garamsythe Waterway scripts](garamsythe-waterway-scripts.md) - every observable function of the same scripts.
- [Location title scenes](titles-scenes.md) - the location titles fields load on the first arrival.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
