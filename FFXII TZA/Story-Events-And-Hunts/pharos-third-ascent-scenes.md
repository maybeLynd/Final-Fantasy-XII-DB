[Home](../../README.md) / [Story, events and hunts](README.md) / Pharos - Third Ascent scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Pharos - Third Ascent scenes: each story scene with its dialogue, Espers, story counter values and what follows | reference | Story, events and hunts | Scenes and scripts by area / Balfonheim, Ridorana and the Bahamut | The nine scene scripts of the dgl group, the Womb of the Sun-cryst and Heaven's Challenge, that zone scripts load: the zone function that loads each one, every line it holds in the game's own words, the Esper it gives, the story counter values written with it, and the scene or map that follows. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00 |

## What it lists

The table has one row per scene script of Pharos - Third Ascent under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `dgl_a0100` | `383` | The Bounds of Truth (Pharos - Second Ascent) | 0 | - |
| `dgl_a0101` | `384` | The Bounds of Truth (Pharos - Second Ascent) | 0 | - |
| `dgl_f0100` | `385` | Womb of the Sun-cryst | 8 | - |
| `dgl_g0100` | `386` | Womb of the Sun-cryst | 63 | scene `dgl_g0101` |
| `dgl_g0101` | `387` | Womb of the Sun-cryst | 35 | story counter 5470, then scene `dgl_g0103` |
| `dgl_g0102` | `388` | Womb of the Sun-cryst | 30 | story counter 5600, 5650 and 6000, then Saccio Lane (Balfonheim Port) |
| `dgl_g0103` | `389` | Womb of the Sun-cryst | 7 | story counter 5500 and 5550, then scene `dgl_g0102` |
| `dgl_h0100` | `380` | Heaven's Challenge | 0 | scene `dgl_h0101` |
| `dgl_h0101` | `381` | Heaven's Challenge | 0 | scene `dgl_h0100` or scene `pos_z0000` |

### What the scenes give

- `dgl_a0100` and `dgl_a0101` have no section 2 entries. They are loaded in The Bounds of Truth (Pharos - Second
  Ascent) by `rbl_j02`'s `SAKIYOMI_ev_dgl_a0100` and `SAKIYOMI_ev_dgl_a0101` ([Pharos - First Ascent
  scripts](pharos-first-ascent-scripts.md)).
- `dgl_f0100`, loaded in Womb of the Sun-cryst (field `666`): "So this is the Sun-cryst. King Raithwall stood here.
  With this sword he cut the Sun-cryst..." Vaan asks whether Ashe will use the sword to destroy it.
- `dgl_g0100`, loaded in Womb of the Sun-cryst (field `668`), is followed by `dgl_g0101`: after "Lord Rasler!?" a
  voice urges "The Cryst is a blade. It was meant for you. Wield it! Avenge your father!", and another owns that it
  wore Basch's face and cut down the Life of Dalmasca. It begins with six choice lists of a scene test menu ("Perform
  read test?", "View scene from:").
- `dgl_g0101` is followed by story counter 5470, after the last nethicite ([story counter
  values](story-counter-values.md)), and by `dgl_g0103`: Gabranth is dismissed from Larsa's service, and Venat and
  the Occuria are named ("The Occuria give men power as a master feeds his dog: it is meant to tame us.").
- `dgl_g0103` gives Famfrit on field `668`. Its five lines, shown by its functions `m001` to `m005`, read "Behold the
  manufacted nethicite... the fruit of our power and knowledge! See what the Stone of Man is capable of! Witness its
  power with your own eyes! Famfrit! To me!"
- `dgl_g0103` is followed by story counter 5500, after the Judge Gabranth battle, and 5550, after Cid's ambition, and
  by `dgl_g0102`. Its first entry is a choice list of cut names that ends "Close debug menu".
- `dgl_g0102` is followed by story counter 5600, after the Famfrit battle; 5650, after the Sun-cryst runs wild; and
  6000, after Vaan on the ship; then by the jump to Saccio Lane (Balfonheim Port), field `826`: "The Sun-cryst
  bursts.", and the line "For Nabudis." is followed by "Reddas?" and "Reddas, no!"
- `dgl_h0100` and `dgl_h0101` open and close the fight in Heaven's Challenge and have no section 2 entries; `監督.main`
  loads them in turn and then `pos_z0000`. `dgl_h0101` gives Hashmal on field `670`.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Pharos - Third Ascent scripts](pharos-third-ascent-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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

- [Pharos - Third Ascent scripts](pharos-third-ascent-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
- [Pharos - First Ascent scenes](pharos-first-ascent-scenes.md) - the scenes of the lower Pharos.
- [Balfonheim Port scenes](balfonheim-port-scenes.md) - the scenes of Balfonheim Port, where `dgl_g0102` leads.

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
