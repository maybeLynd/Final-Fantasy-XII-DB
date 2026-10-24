---
title: "Lhusu Mines scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Lhusu Mines under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `lus_a0100` | `296` | Shaft Entry | 15 | - |
| `lus_a0180` | `702` | Shaft Entry | 4 | story counter 660 |
| `lus_c0100` | `290` | Tasche Span | 1 | scene `lus_c0102` or scene `lus_c0101` |
| `lus_c0101` | `291` | Tasche Span | 7 | scene `lus_c0102` |
| `lus_c0102` | `292` | Tasche Span | 0 | scene `lus_c0100` or scene `pos_z0000` |
| `lus_e0100` | `293` | Site 7 | 2 | scene `lus_e0102` or scene `lus_e0101` |
| `lus_e0101` | `294` | Site 7 | 5 | scene `lus_e0102` |
| `lus_e0102` | `295` | Site 7 | 0 | scene `lus_e0100` or scene `pos_z0000` |
| `lus_g0100` | `297` | Site 2 | 28 | scene `lus_g0101` |
| `lus_g0101` | `299` | Oltam Span, Transitway 1, Shunia Twinspan, Site 2 | 3 | story counter 660, then scene `lus_g0100` |
| `lus_g0280` | `701` | Oltam Span, Transitway 1, Shunia Twinspan | 0 | story counter 660 |

### What the scenes give

- No scene row lists an item or a party change.
- `lus_a0100`, loaded in Shaft Entry: the purest magicite is diverted, and "Halim Ondore IV, the Marquis of Bhujerba"
  is said to be helping the Resistance.
- `lus_g0100`, loaded in Site 2 (field `933`), is followed by `lus_g0101`: "It's nethicite. Manufacted nethicite."
  "All at the hands of the Draklor Laboratory."
- `lus_g0101`, loaded in Site 2 and in the chase maps, is followed by story counter 660, after the Ba'Gamnan battle
  ([story counter values](story-counter-values.md)), and by `lus_g0100`: "I will have my pound of flesh yet,
  Balthier!" `lus_g0280`, loaded in the chase, has no section 2 entries and is followed by 660. `lus_a0180`, loaded in
  Shaft Entry, is followed by 660: "It would not seem they follow. We've lost them."
- `lus_c0100`, `lus_c0101` and `lus_c0102` (Tasche Span) and `lus_e0100`, `lus_e0101` and `lus_e0102` (Site 7) are the
  two Gilgamesh fights: "Fools! You face the mightiest swordsman in all Ivalice! You face ME! GILGAMESH!" and
  "Gilgamesh fights again!" `lus_c0102` and `lus_e0102` have no section 2 entries; `常駐監督.main` loads each set in turn
  and then `pos_z0000`.
- `lus_a0180` and `lus_g0101` begin with the choice list "View scene again?" (Yes, No).

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / ` |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Lhusu Mines scripts](lhusu-mines-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
