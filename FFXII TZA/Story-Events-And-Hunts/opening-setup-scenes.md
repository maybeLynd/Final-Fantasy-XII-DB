---
title: "Opening setup scenes: the event script pre_z0000, how it is requested and what it sets"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of the `pre` group under `plan_master/us/event` that an event id names. Zone
scripts load scenes with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`), which `0x0032FCA0`
reads from index `4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md));
`pre_z0000` is requested by the executable instead.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `pre_z0000` | `212` | the field runtime pass `0x0025D9E0` | 0 | - |

### What the scenes give

- `pre_z0000` holds no text, gives no item, writes no story counter value and makes no story flag call. Its one
  function sets script globals from the story counter and calls `eventdispose` ([Opening setup
  scripts](opening-setup-scripts.md)).
- No `us` script names event 212 in `eventread` or `eventread_e8`, so its `loaded_by` cell names the field runtime
  pass `0x0025D9E0`, which requests it on manager 1 through `0x0032FC30` (`0x0025DAE8`, `0x0025DAED`), and `0x0032F430` preloads it
  once ([EBP script container](../EBP-Script-Files/ebp-script-container.md)).

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Opening setup scripts](opening-setup-scripts.md)): its actors, camera shots, motions, effects, music and loads.

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump` (`0x00354D00`) count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event; for `pre_z0000`, the exe step that requests it |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Opening setup scripts](opening-setup-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
