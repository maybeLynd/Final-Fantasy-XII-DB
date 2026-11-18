[Home](../../README.md) / [Story, events and hunts](README.md) / Mt Bur-Omisace scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Mt Bur-Omisace scenes: each story scene with its dialogue, story counter values and what follows | reference | Story, events and hunts | Scenes and scripts by area / Paramina Rift and Mt Bur-Omisace | The five scene scripts of Mt Bur-Omisace: the zone function that loads each one, every line it holds in the game's own words, the story counter values written with it, and the scene or map that follows. | 0x00351880, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00 |

## What it lists

The table [mt-bur-omisace-scenes.tsv](mt-bur-omisace-scenes.tsv) has one row per scene script of Mt Bur-Omisace under
`plan_master/us/event`. The zone scripts load them with `eventread_e8` (`0x0E8`, `0x00351880`); its end handler
`0x003522C0` queues the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `bul_a0100` | `193` | Hall of the Light, field `736` | 45 | - |
| `bul_a0101` | `194` | Hall of the Light, field `736` | 38 | story counter 2010 and 2050 |
| `bul_a0200` | `195` | Hall of the Light, field `737` | 24 | scene `bul_a0201` |
| `bul_a0201` | `196` | Hall of the Light, field `737` | 29 | story counter 2300, 2350 and 3000, then the Temple Grounds, field `738`; from the first load site, scene `bul_a0200` |
| `bul_a0380` | `740` | Temple Grounds | 9 | story counter 3050 and 1986 |

### The scenes

- `bul_a0100` is the audience with Anastasis ("Anastasis, Your Grace, I am Ashelia—"), and `bul_a0101` continues it
  ("Let us suppose you approach the Empire with a peaceful resolution."); after `bul_a0101` the loading function
  writes 2010 and 2050.
- `bul_a0200` opens with two choice lists, where to start the scene ("From the beginning.", "From Bergan's "No. No
  the power..."") and "View scene again?", and then shows Judge Bergan ("You will surrender it to me.").
- `bul_a0201` follows the battle ("Wait—what about Larsa? / Gone. Spirited away by Judge Gabranth."); the loading
  function then writes 2300, 2350 and 3000 and jumps to the Temple Grounds.
- `bul_a0380` is the decision to cross into Archadia ("We'll cross into Archadia in the Salikawood.").
- None of the scenes gives items or party members by a literal id; the item helper of `bul_a0101` gives items held
  in script variables ([Mt Bur-Omisace scripts](mt-bur-omisace-scripts.md)).

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump` (`0x00354D00`) count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first. A scene loaded from two places of the function has the follower of
each place.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread_e8` call names the event |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / ` |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Mt Bur-Omisace scripts](mt-bur-omisace-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
- [Boss fights](../Battle-Actions/boss-fights.md) - the boss gauge and foe removal around the Judge Bergan battle.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 25 calls with 6 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | calls | `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0` |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00354D00` | calls | `0x00229EA0` |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | calls | `0x002DF980`, `0x0032E400`, `0x0032E620` |
| `0x00351880` | calls | `0x001D6A70` |

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x00264D60` | is called by | `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0` |
| `0x00348DF0` | calls | `0x00267E10` |
| `0x00348DF0` | is called by | `0x00349800` |
| `0x00351880` | calls | `0x00267E10` |
| `0x00354D00` | calls | `0x00267E10` |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [force fight mode](../Engine-Core/force-fight-mode.md))

**World, areas and travel** (explained on [debug menu](../Engine-Core/debug-menu.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | is called by | `0x0032FC30` |
| `0x003522C0` | calls | `0x0032FC30` |

</details>
