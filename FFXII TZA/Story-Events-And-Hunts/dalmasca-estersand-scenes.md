---
title: "Dalmasca Estersand scenes: each story scene with its dialogue, rewards, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Dalmasca Estersand under `plan_master/us/event` that an event id names,
and one for the developer script `dst_z9900`, which no event id names. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `dst_a0180` | `122` | The Stepping | 0 | scene `dst_a0181` |
| `dst_a0181` | `724` | The Stepping | 4 | story counter 70, 75 and 78, then scene `ttl_z0003` |
| `dst_a0580` | `710` | Passage Entrance | 6 | story counter 343 |
| `dst_b0100` | `121` | South Bank Village, North Bank Village | 85 | North Bank Village (Dalmasca Estersand) or South Bank Village (Dalmasca Estersand) |
| `dst_z9900` | - | no event id | 0 | - |

### What the scenes give

- `dst_a0181` gives the Galbana Lilies; the Rogue Tomato watcher that loads it writes 70 (after the Rogue Tomato
  battle), 75 (after the first hunt) and 78 (after the Galbana Lilies)
  ([story counter values](story-counter-values.md), [scene rewards](scene-rewards.md)).
- `dst_b0100` is the boat across the Nebra with its fishing game: it gives the catch (Common Fish, Delicious Fish,
  Nebra Succulent, Empty Bottle), the Blue, Green, Red, Yellow and Black Bottles, the Cactoid Compact, the
  Cactoid Commendation and reward packages from a Hi-Potion to Lu Shang's Badge. Each village's `NPC01.talk`
  loads it and then jumps to the other village.
- `dst_a0580` is followed by story counter 343, the arrival in Dalmasca Estersand.
- `dst_a0180` holds no text.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Dalmasca Estersand scripts](dalmasca-estersand-scripts.md)): its actors, camera shots, motions, effects, music and loads.

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump` (`0x00354D00`) count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it; `-` for `dst_z9900` |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event; for `dst_z9900`, that it has no event id |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Dalmasca Estersand scripts](dalmasca-estersand-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
