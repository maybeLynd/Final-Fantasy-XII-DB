[Home](../../README.md) / [Story, events and hunts](README.md) / Sky Fortress Bahamut scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Sky Fortress Bahamut scenes: each story scene with its dialogue, story counter values and what follows | reference | Story, events and hunts | Scenes and scripts by area / Balfonheim, Ridorana and the Bahamut | The scene scripts of the Sky Fortress Bahamut: the zone function that loads each one, every line it holds in the game's own words, the story counter values written with it, and what follows. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00 |

## What it lists

The table [sky-fortress-bahamut-scenes.tsv](sky-fortress-bahamut-scenes.tsv) has one row per scene script of the Sky
Fortress Bahamut under `plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`) and
`eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which
`0x0032FCA0` reads from index `4n` of the event file table ([event
scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `bhm_a0200` | `150` | Catwalk | 23 | - |
| `bhm_a0400` | `141` | Antechamber | 7 | - |
| `bhm_b0100` | `155` | Central Lift | 16 | `bhm_b0101` (event `156`) |
| `bhm_b0101` | `156` | Central Lift | 11 | - |
| `bhm_c0100` | `157` | Central Shaft | 19 | `bhm_c0101` (event `158`) |
| `bhm_c0101` | `158` | Central Shaft | 11 | story counter 6850, 6900 and 7000, then Cannon Superstructure, field `785` |
| `bhm_c0102` | `159` | Central Shaft | 16 | - |
| `bhm_d0100` | `142` | Cannon Superstructure | 12 | `bhm_d0101` (event `151`) |
| `bhm_d0101` | `151` | Cannon Superstructure | 91 | story counter 7100 and 7150, then `msg_z0001` (event `399`) |
| `bhm_y0100` | `153` | field 922 (`bhm_y01`) | 54 | story counter 6400, then Antechamber, field `777` |
| `bhm_y0101` | `154` | field 922 (`bhm_y01`) | 15 | story counter 4050, then `var_z01` (Balfonheim Port), field `918` |
| `bhm_z0100` | `152` | field 924 (`bhm_z01`) | 34 | - |

### What the scenes give

- `bhm_z0100`, loaded in field 924 below story counter 6150, holds Vayne's attack on the Resistance ("Make your target
  the Resistance heavy cruiser." ... "Ships sighted ahead! A score or more! The Resistance fleet, my lord!") and a
  movie's subtitles ("This wind... What could it be?"); its first entry is "View scene again?" (Yes / No).
- `bhm_y0101`, in field 922 below 4050, holds the Resistance fleet setting out ("Squads Flametongue and Ogrenix are
  away! All ships reporting in.") and the dispatch from Naldoa Command ("The sky pirate has left Archadian airspace."
  / "He makes for Balfonheim with the Lady Ashe and her party.").
- `bhm_y0100`, in field 922 below 6300, holds Ashe's call to her uncle ("Uncle, it is I!" / "I'm crossing to the
  Bahamut to stop Vayne!"), Larsa's ("This is Larsa Solidor!") and a movie's subtitles of the sky battle ("May fortune
  favor us all." ... "Then let's dance!").
- `bhm_a0400`, in the Antechamber below 6450, holds the way to Vayne ("Vayne will be in the fortress's command tower."
  ... "If we can get to Vayne, we can put an end to this war.").
- `bhm_a0200`, in Catwalk below 6550, holds the talk of the coming peace ("We just have to clean up here, and then
  Ashe'll be the queen." ... "You got good friends.") and a movie's subtitles ("They hide in the sun!" ... "The line
  is drawn.").
- `bhm_b0100` and `bhm_b0101` are loaded together in the Central Lift. `bhm_b0100` holds the talk of the two brothers
  ("So you have lived." ... "Or is that not answer enough?"), `bhm_b0101` the lines "Have you your fill of this?" ...
  "Know now the despair you have taught me!".
- `bhm_c0100` and `bhm_c0101` are loaded together in Central Shaft. `bhm_c0100` holds Vayne's welcome ("I bid you
  welcome to my sky fortress, the Bahamut." ... "Bold words, child."), its first entry "View scene again?" (Yes / No).
- `bhm_c0101` holds "Your lives are forfeit, and your insurgence with them. Dalmasca will again know order." ... "One
  I gladly pay."; its first entry is "Play scene again?" (From cut 01 / From cut 09 / From cut 16 / No). The story
  counter values 6850, 6900 and 7000 are written with it.
- `bhm_c0102`, loaded in Central Shaft after the first Vayne fight, holds "Ivalice will know a new Dynast-King, and
  Man will keep his own history!" ... "Here I pay my debt." Its first entries are a load test menu ("Perform load
  test?" (No / Yes)) and "View scene again?" with six start points.
- `bhm_d0100` and `bhm_d0101` are loaded together in the Cannon Superstructure. `bhm_d0100` holds the talk of Vayne
  and Venat ("Venat!" ... "History begins anew.").
- `bhm_d0101` holds the ending, 91 entries: the Strahl's escape ("Well? Can we fly?"), the cease-fire ("All units of
  the Archadian army, hold your fire!") and Balthier's call from the Bahamut ("Ah, Vaan!" ... "I'm the leading man.").
  The story counter values 7100 and 7150 are written with it, and the ending message `msg_z0001` follows.
- No scene gives an item or changes the party.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes`¹, which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00348DF0` |

</details>

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump`¹ count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00354D00` |

</details>

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
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Sky Fortress Bahamut scripts](sky-fortress-bahamut-scripts.md) - every observable function of the same scripts.
- [Ending message scenes](ending-message-scenes.md) - the scene that follows `bhm_d0101`.
- [Story counter values](story-counter-values.md) - what each counter value marks.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 29 calls with 6 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00229EA0`](../Graphics/effect-drawing.md) (on effect drawing) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264D60`](../Menus-And-HUD/aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x00352A50`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00352EC0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003534F0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00356B70`](../Characters-And-Objects/npc-names.md) (on npc names)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | is called by | [`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**World, areas and travel** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | is called by | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x003522C0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x00353080`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |

</details>
