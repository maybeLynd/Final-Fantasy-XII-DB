---
title: "Archades scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Archades under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `alc_a0100` | `307` | Tsenoble | 7 | - |
| `alc_a0280` | `731` | Nilbasse | 18 | - |
| `alc_b0400` | `306` | Trant | 20 | story counter 3250 |
| `alc_c0180` | `732` | Tsenoble | 15 | - |
| `alc_z0100` | `300` | `alc_z01` | 36 | story counter 1180, then The Western Divide (Dalmasca Westersand) |
| `alc_z0101` | `301` | `alc_z01`, `alc_z04` | 46 | story counter 1660, then Sunlit Path (Ozmone Plain) |
| `alc_z0102` | `303` | `alc_z01` | 16 | story counter 1976, then Freezing Gorge (Paramina Rift) |
| `alc_z0103` | `304` | `alc_z01`, `alc_z03` | 45 | story counter 5020, then Gate of Wind (Giruvegan) |
| `alc_z0104` | `305` | `alc_z01` | 35 | story counter 2000, then Hall of the Light (Mt Bur-Omisace) |
| `alc_z0200` | `302` | `alc_z02` | 29 | story counter 1550, then The Muted Scarp (Nabreus Deadlands) |

### What the scenes give

- No scene row lists an item or a party change.
- `alc_b0400`, loaded in Trant, is followed by story counter 3250, after slipping into the imperial capital ([story
  counter values](story-counter-values.md)): Vaan looks over the city ("I'm just checking out the city.") and Larsa
  is remembered ("Hey, Larsa's here in the city, isn't he?").
- `alc_a0280`, loaded in Nilbasse: the cab asks for a chop or coin, and Jules brings a message from Balthier, who
  waits in Central. `alc_a0100`, loaded in Tsenoble: "The complices of the Senate have been quelled, Your Honor."
  `alc_c0180`, loaded in Tsenoble: Jules has had the party collect chops while a squad of Judges was sent to Draklor.
- The court scenes, all loaded in `alc_z01` to `alc_z04`: `alc_z0100` is followed by 1180, after Emperor Gramis, and
  the jump to The Western Divide (Dalmasca Westersand); `alc_z0200` by 1550, after the Senate, and The Muted Scarp
  (Nabreus Deadlands).
- `alc_z0101` is followed by 1660, after the judge master, and Sunlit Path (Ozmone Plain); `alc_z0102` by 1976, after
  Gramis and Vayne, and Freezing Gorge (Paramina Rift); `alc_z0104` by 2000, after the emperor's assassination, and
  Hall of the Light (Mt Bur-Omisace); `alc_z0103` by 5020, after law and order, and Gate of Wind (Giruvegan).
- `alc_z0100`: Doctor Cid's funds from Lord Vayne, the fall of Nabudis, and Gramis's successor. `alc_z0200`: the
  Rozarrian host and the loss of the Leviathan. `alc_z0101`: the Judges speak of Lord Vayne and of Judge Zecht, gone
  since Nabudis. `alc_z0102`: "It is my idea of necessity." `alc_z0104`: the Senate's chairman Gregoroth confesses to
  the poisoning. `alc_z0103`: Larsa asks that Dalmasca's sovereignty be restored.
- Several scenes begin with a replay choice list ("View scene again?", "Select playback start point:", "Replay?").

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
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Archades scripts](archades-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
- [Nabreus Deadlands scenes](nabreus-deadlands-scenes.md) - where `alc_z0200` leads.

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
- Script VM: those functions are documented on [archades scripts](archades-scripts.md),
  [ebp text sections](../EBP-Script-Files/ebp-text-sections.md),
  [npc names](../Characters-And-Objects/npc-names.md),
  [force fight mode](../Engine-Core/force-fight-mode.md); and on
  [native commands](../Scripts-And-Script-Commands/native-commands.md).
- World area: `0x0032FCA0` is called by `0x0032FC30`; `0x003522C0` calls `0x0032FC30`; `0x00353080` calls `0x0032FC30`; those
  functions are documented on [debug menu](../Engine-Core/debug-menu.md).
