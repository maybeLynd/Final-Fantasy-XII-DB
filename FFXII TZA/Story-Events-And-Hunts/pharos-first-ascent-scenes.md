---
title: "Pharos - First Ascent scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Pharos - First Ascent under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `rbl_c0100` | `376` | Dunes of Profaning Wind | 0 | scene `rbl_c0101` |
| `rbl_c0101` | `377` | Dunes of Profaning Wind | 0 | scene `rbl_c0100` |
| `rbl_f0100` | `392` | Marsh of Profaning Wind | 0 | scene `rbl_f0101` |
| `rbl_f0101` | `126` | Marsh of Profaning Wind | 0 | scene `rbl_f0100` |
| `rbl_g0200` | `129` | Penumbra - North | 0 | scene `rbl_g0201` |
| `rbl_g0201` | `136` | Penumbra - North | 0 | scene `rbl_g0200` or scene `pos_z0000` |
| `rbl_j0100` | `127` | Cleft of Profaning Wind | 0 | scene `rbl_j0101` |
| `rbl_j0101` | `128` | Cleft of Profaning Wind | 0 | scene `rbl_j0100` or scene `pos_z0000` |
| `rbl_n0200` | `378` | Spire Ravel - 2nd Flight | 0 | - |
| `rbl_q0100` | `379` | Empyrean Ravel | 15 | - |

### What the scenes give

- No scene row lists an item, a party change or a story counter value.
- `rbl_c0100` and `rbl_c0101` (Dunes of Profaning Wind), `rbl_f0100` and `rbl_f0101` (Marsh of Profaning Wind),
  `rbl_j0100` and `rbl_j0101` (Cleft of Profaning Wind) and `rbl_g0200` and `rbl_g0201` (Penumbra - North) are the
  scenes of the fights there and have no section 2 entries; `常駐ディレクター.main` loads each pair in turn, and in the Cleft
  and Penumbra - North then `pos_z0000`.
- `rbl_n0200`, loaded in Spire Ravel - 2nd Flight, has no section 2 entries.
- `rbl_q0100`, loaded in Empyrean Ravel below story counter 5,370 ([story counter
  values](story-counter-values.md)): "The din of the Mist grows greater. The Sun-cryst must be near." "I wonder if
  she'll really do it. Take revenge against the Empire." "The past can bind a man as surely as irons."

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Pharos - First Ascent scripts](pharos-first-ascent-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Pharos - First Ascent scripts](pharos-first-ascent-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
- [Pharos - Third Ascent scenes](pharos-third-ascent-scenes.md) - the scenes of the Womb of the Sun-cryst and Heaven's
  Challenge.
