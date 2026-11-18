[Home](../../README.md) / [Story, events and hunts](README.md) / Bhujerba scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Bhujerba scenes: each story scene with its dialogue, story counter values and what follows | reference | Story, events and hunts | Scenes and scripts by area / Bhujerba and the Leviathan | The scene scripts of Bhujerba: the zone function that loads each one, every line it holds in the game's own words, the story counter values written with it, and what follows. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00 |

## What it lists

The table [bhujerba-scenes.tsv](bhujerba-scenes.tsv) has one row per scene script of Bhujerba under
`plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`,
`0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index
`4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `byu_a0100` | `271` | Travica Way | 21 | - |
| `byu_a0400` | `272` | Lhusu Square | 30 | - |
| `byu_a0480` | `705` | Lhusu Square | 4 | - |
| `byu_a0481` | `725` | Lhusu Square | 14 | - |
| `byu_a1880` | `265` | The Cloudborne | 20 | `byu_x01`, field `914` (at story counter 710); story counter 730 (at 720) |
| `byu_b0100` | `276` | Aerodrome | 19 | story counter 1095 and 1100 |
| `byu_b0101` | `278` | Aerodrome | 9 | story counter 546 |
| `byu_w0100` | `277` | field 912 (`byu_w01`) | 38 | story counter 1130, then `alc_z01` (Archades), field `866` |
| `byu_x0100` | `275` | field 914 (`byu_x01`) | 26 | story counter 720, then The Cloudborne, field `820` |
| `byu_y0100` | `273` | field 864 (`byu_y01`) | 30 | story counter 800, then `rbn_x01` (Rabanastre), field `860` |
| `byu_y0101` | `274` | field 864 (`byu_y01`) | 28 | story counter 1120, then `byu_w01`, field `912` |
| `byu_z0100` | `270` | field 862 (`byu_z01`) | 15 | story counter 490 and 520, then the Aerodrome, field `791` |
| `byu_z9900` | `606` | every town field: Travica Way, Cloudborne Row, Miners' End, Lhusu Square, Khus Skygrounds, Kaff Terrace, Targe's Arms, Rithil's Protectives, Mait's Magicks, Clio's Technicks, Bashketi's Gambits, The Staras Residence, The Cloudborne and the Aerodrome | 0 | - |

### What the scenes give

- `byu_z0100`, loaded in field 862 at story counter 460, holds "You've seen to her feeding, yes?" ... "She makes
  straight for the Skycity of Bhujerba!" ... "As for you! We need Balthier alive! His corpse fetches but half the
  bounty!"
- `byu_b0101`, in the Aerodrome at 520, opens with "View scene again?" (Yes / No) and holds "No good. He's not here."
  / "Keep searching!" ... "You're a dead man. Don't forget it."
- `byu_a0100`, in Travica Way at 546, opens with "View scene again?" (Yes / No) and holds "The Lhusu Mines are just up
  ahead." ... "Then please, allow me to accompany you." ... "I'm Lamont."
- `byu_a0480`, in Lhusu Square below 580, holds "The Lhusu Mines: one of the richest veins in Ivalice." ... "Well,
  shall we proceed?"
- `byu_a0400`, in Lhusu Square from 658 to 670, opens with "View scene again?" (Yes / No) and holds "I see you've been
  out walking without the company of your cortege..." ... "Larsa Ferrinas Solidor."
- `byu_a0481`, in Lhusu Square at 680, holds "Marquis Ondore announced my execution 2 years ago." ... "Nothin' to it!
  I'll just go around town spreading the word. How 'bout this?" ... "That certainly qualifies as a clamor."
- `byu_a1880`, in The Cloudborne at 710 and 720, holds "This is the one, Havharo. Says he's Captain Basch he does."
  ... "So Basch fon Ronsenburg does yet live." The story counter values 710, 720 and 730 are written with it.
- `byu_x0100`, in field 914 at 710, holds "So Vaan really is all right." ... "Vayne Solidor, the Consul, is my
  brother." ... "He frightens me."
- `byu_y0100`, in field 864 at 730, opens with "View scene again?" (Yes / No) and holds "Sir Basch fon Ronsenburg."
  ... "A leader of the Resistance has fallen into Imperial hands." / "A woman by the name of Amalia."
- `byu_b0100`, in the Aerodrome at 1090, holds "Balthier, your handkerchief. I thought you might want it back." ... "I
  have played the fool!"
- `byu_y0101`, in field 864 at 1100, holds "When Vossler learned my father had been killed..." ... "Bhujerba must
  stand with us."
- `byu_w0100`, in field 912 at 1120, holds "What are you doing?" / "This is Balthier's ship." / "I'm going to retrieve
  the Dawn Shard. It's the proof that I need."
- `byu_z9900` (event 606) holds no line. Every town field's `オレバッシュ監督.init` loads it while the rumour runs, and the
  Aerodrome's `常駐監督.main` loads it too.
- No scene gives an item, changes the party or sets a story flag.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Bhujerba scripts](bhujerba-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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

- [Bhujerba scripts](bhujerba-scripts.md) - every observable function of the same scripts.
- [Aerodrome airship scenes](aerodrome-airship-scenes.md) - the scene the Aerodrome loads after `byu_b0100`'s function.
- [Story counter values](story-counter-values.md) - what each counter value marks.

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
