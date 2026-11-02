---
title: "Giruvegan scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [giruvegan-scenes.tsv](giruvegan-scenes.tsv) has one row per scene script of Giruvegan and the Great Crystal
under `plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8`
(`0x0E8`, `0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads
from index `4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `gil_a0100` | `207` | Gate of Earth | 16 | - |
| `gil_a0200` | `143` | Gate of Water | 0 | `gil_a0201` (event `144`) |
| `gil_a0201` | `144` | Gate of Water | 0 | - |
| `gil_c0100` | `208` | The Haalmikah Water-Steps | 8 | - |
| `gil_c0200` | `145` | Gate of Fire | 0 | `gil_c0201` (event `146`) |
| `gil_c0201` | `146` | Gate of Fire | 0 | - |
| `gil_d0100` | `147` | Gate of Wind | 0 | `gil_d0101` (event `148`) |
| `gil_d0101` | `148` | Gate of Wind | 1 | - |
| `gil_d0102` | `229` | Gate of Wind | 8 | - |
| `gil_g1000` | `209` | Crystal Core | 7 | - |
| `gil_h0100` | `149` | Crystal Peak | 0 | `gil_h0101` (event `205`) |
| `gil_h0101` | `205` | Crystal Peak | 1 | - |
| `gil_i1000` | `174` | Dhebon Jilaam Avaa | 0 | `pos_z0000` (event `427`) |
| `gil_z0100` | `206` | Siti Bhrusuna | 70 | story counter 5000, then `alc_z03` (Archades), field `868` |

### What the scenes give

- `gil_a0100`, loaded in Gate of Earth below story counter 4250, holds the arrival in Giruvegan ("On the farthest
  shores of the river of time, shrouded deep in the roiling Mist." ... "It appears Cid has yet to arrive. We'll lie in
  wait for him here." ... "She can see him. Let's follow her."); its first entry is "View scene again?" (Yes / No),
  and 4250 follows it.
- `gil_a0200` and `gil_a0201` (Gate of Water), `gil_c0200` and `gil_c0201` (Gate of Fire), `gil_d0100` and `gil_d0101`
  (Gate of Wind) and `gil_h0100` and `gil_h0101` (Crystal Peak) are loaded in pairs when a boss fight begins. They
  hold no text of their own: `gil_d0101` and `gil_h0101` hold one empty entry, the others no entry.
- `gil_d0101` and `gil_h0101` each hold a switch on the current field (`nowmap`) that gives the Esper of that field
  when the party does not hold it; for their own fields these are Shemhazai (`0xC019`) in Gate of Wind and Ultima
  (`0xC01D`) in Crystal Peak ([Quickening and Esper list](../Battle-Actions/quickening-and-esper-list.md)). The
  scenes table lists every id of the switch.
- `gil_d0101` and `gil_h0101`: in the Cloister of Flame (field 415) their switch gives Belias (`0xC012`) together with
  SecondJob (`0xC01F`), the presence bit of the Second Board ([Scene rewards](scene-rewards.md)).
- `gil_c0100`, in The Haalmikah Water-Steps below story counter 4320, holds the talk on entering ("I can't shake the
  feeling we're somewhere we're not meant to be." / "Yeah, it's exciting." ... "You're sounding more the sky pirate
  every day."); 4320 follows it.
- `gil_d0102`, in Gate of Wind from story counter 5000 to 5099, holds the talk of the Sun-cryst ("In tower on distant
  shore dreams the Sun-cryst." / "Do these words mean aught to you?" ... "You're an expert on pirating now, are
  you?"); 5100 follows it.
- `gil_g1000`, in Crystal Core below story counter 4370, holds the talk at the crystal ("I've never seen this much
  Mist. Are you all right?" ... "You could destroy all of Ivalice." / "If you wished it."); 4370 follows it.
- `gil_i1000`, loaded in Dhebon Jilaam Avaa for the `g_btl_オメガ` fight, holds no text; `pos_z0000` follows the fight.
- `gil_z0100`, in Siti Bhrusuna, holds the Occuria's charge ("We Occuria have chosen you, and you alone." ... "Now
  take this sword, this Treaty-Blade. Occurian seal, mark of your worth.") and the party's talk after it ("He's not
  coming." / "He laid out the bait, and we bit.").
- `gil_z0100`: its first entry is the start-point choice "View scene from:" (Cut 01 / Cut 13 / Cut 29 / Cut 31). It
  gives the Treaty-Blade from its own functions (`Director.main`); the loading function writes 5000 after it and jumps
  to field 868.
- No scene changes the party.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Giruvegan scripts](giruvegan-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)`; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Giruvegan scripts](giruvegan-scripts.md) - every observable function of the same scripts.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
