---
title: "Stilshrine of Miriam scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [stilshrine-of-miriam-scenes.tsv](stilshrine-of-miriam-scenes.tsv) has one row per scene script of the
Stilshrine of Miriam under `plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`)
and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`,
which `0x0032FCA0` reads from index `4n` of the event file table ([event
scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `mrm_c0100` | `360` | Ward of Steel | 0 | `mrm_c0101` (event `361`) |
| `mrm_c0101` | `361` | Ward of Steel | 0 | - |
| `mrm_e0100` | `362` | Hall of Worth | 0 | `mrm_e0101` (event `363`) |
| `mrm_e0101` | `363` | Hall of Worth | 1 | `pos_z0000` (event `427`) |
| `mrm_f0100` | `366` | Vault of the Champion | 18 | Hall of Worth, field `612` |
| `mrm_g0100` | `364` | Throne of Veiled Gods | 0 | `mrm_g0101` (event `365`) |
| `mrm_g0101` | `365` | Throne of Veiled Gods | 1 | - |

### What the scenes give

- `mrm_c0100` and `mrm_c0101` (Ward of Steel), `mrm_e0100` and `mrm_e0101` (Hall of Worth), and `mrm_g0100` and
  `mrm_g0101` (Throne of Veiled Gods) are loaded in pairs when a boss fight begins; the victory pose scene `pos_z0000`
  follows each fight. They hold no text of their own: `mrm_e0101` and `mrm_g0101` hold one empty entry, the others
  none.
- `mrm_e0101` and `mrm_g0101` each hold a switch on the current field (`nowmap`) that gives the Esper of that field
  when the party does not hold it; for their own fields these are Mateus (`0xC013`) in Hall of Worth and Zeromus
  (`0xC01B`) in Throne of Veiled Gods ([Quickening and Esper
  list](../Battle-Actions/quickening-and-esper-list.md)). The scenes table lists every id of the switch.
- `mrm_e0101` and `mrm_g0101`: in the Cloister of Flame (field 415) their switch gives Belias (`0xC012`) together with
  SecondJob (`0xC01F`), the presence bit of the Second Board ([Scene rewards](scene-rewards.md)).
- `mrm_f0100`, loaded in the Vault of the Champion below story counter 2200, holds the talk over the Sword of Kings
  ("This is the sword. The nethicite destroyer." / "Should it find its mark."); touching `イベントレクト` plays it, and the
  zone function then writes 2200 and gives the Sword of Kings ([Stilshrine of Miriam
  scripts](stilshrine-of-miriam-scripts.md)).
- `mrm_f0100`: its first entries are a start-point choice ("From beginning (Cut 01)" / "From Ashe placing Stone (Cut
  13)") and "View scene again?" (Yes / No).
- No scene changes the party.

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)` |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Stilshrine of Miriam scripts](stilshrine-of-miriam-scripts.md) - every observable function of the same scripts.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
