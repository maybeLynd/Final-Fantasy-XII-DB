---
title: "Dreadnought Leviathan scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [dreadnought-leviathan-scenes.tsv](dreadnought-leviathan-scenes.tsv) has one row per scene script of the
Dreadnought Leviathan under `plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`)
and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`,
which `0x0032FCA0` reads from index `4n` of the event file table ([event
scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `rsn_a0100` | `283` | Port Launch | 15 | - |
| `rsn_a0101` | `288` | Port Launch | 11 | `rsn_a0102` (event `285`) |
| `rsn_a0102` | `285` | Port Launch | 11 | story counter 1090, then the Aerodrome (Bhujerba), field `791` |
| `rsn_b0100` | `287` | Port Section | 23 | - |
| `rsn_b0180` | `703` | Port Section | 7 | - |
| `rsn_d0100` | `280` | Central Brig Access | 1 | `pos_z0000` (event `427`), then story counter 966 |
| `rsn_d0180` | `704` | Central Brig Access | 6 | - |
| `rsn_y0100` | `284` | Brig No. 1 | 10 | - |
| `rsn_z0100` | `282` | Bridge | 37 | story counter 890, then Port Launch, field `552` |
| `rsn_z0101` | `289` | Bridge | 34 | story counter 1460, then Battle Launch (Light Cruiser Shiva), field `872` |
| `rsn_z0200` | `279` | Battle Launch | 30 | `rsn_z0201` (event `286`) |
| `rsn_z0201` | `286` | Battle Launch | 24 | story counter 1520, then `alc_z02` (Archades), field `867` |

### What the scenes give

- `rsn_z0100`, loaded on the Bridge from story counter 830 below 890, opens with "View scene again?" (Yes / No) and
  holds the prisoners brought to the bridge ("The prisoners, my lord." ... "I will not play puppet to Vayne."), the
  Dusk Shard ("It is your birthright: the Dusk Shard.") and the Stone ("Splendid! You've brought the Stone with you!
  This spares us a great deal of trouble." ... "Take them away. Lady Ashe is to be quartered separately.").
- `rsn_a0100`, in Port Launch from 890 below 920, holds "So you were carrying it all along. The Fates jest." ... "I'm
  getting her out. I need your help." / "Of course."; it gives the item Leviathan and shows "Your location map for
  this area is complete!"
- `rsn_b0180`, in Port Section from 920 below 930, opens with "View scene again?" (Yes / No) and holds the warning
  "See that red web of light spanning the passageway?" ... "Break one of those beams and an alarm will sound,
  summoning the guard."
- `rsn_d0100`, in Central Brig Access from 930 below 966, holds one line: "Fear not their numbers! Take down the
  leaders, and the others will follow!"; `pos_z0000` follows the fight.
- `rsn_y0100`, in Brig No. 1 below 970, holds "You are unharmed." / "Vossler! I—" ... "We will talk later."
- `rsn_d0180`, in Central Brig Access from 970 below 990, holds "Majesty. We will cut you a path." / "I will not place
  my trust in the sword of a traitor!" ... "We must make her confront the reality of our plight."
- `rsn_b0100`, in Port Section from 990 below 1000, holds "Vaan!" ... "You are Captain Azelas. You will follow me."
  ... "That you and Captain Ronsenburg were made to appear dead..." ... "Penelo, for you." / "May it bring you good
  fortune."; it gives the Manufacted Nethicite.
- `rsn_a0101` and `rsn_a0102` are loaded together in Port Launch. `rsn_a0101` holds "Such a great shame." ... "You
  know nothing of my father!", `rsn_a0102` the escape ("We've secured an Atomos. Come!" ... "Had we gone too fast,
  they'd have noticed."). The story counter value 1090 is written with `rsn_a0102`.
- `rsn_z0101`, on the Bridge from 1450 below 1452, holds "Such a tremendous honor to again be graced with your
  presence, Majesty." ... "Majesty, he speaks of the Dawn Shard. That is the nethicite." ... "Captain Azelas, take
  them to Shiva."
- `rsn_z0200` and `rsn_z0201` are loaded together in Battle Launch. `rsn_z0200` holds the test of the Stone
  ("Sixty-eight hundred, sixty-nine hundred, seven thousand!" ... "Why do this, Basch? This struggle is futile. You
  must know where it leads!").
- `rsn_z0201` holds "I can serve her no more. You must take up my charge." and the Leviathan's fall ("The nethicite's
  draining the ship's power!" ... "I think it's the Dawn Shard!"). The story counter value 1520 is written with it,
  and `alc_z02` (Archades) follows.
- No other scene gives an item, and no scene sets a story flag.

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
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Dreadnought Leviathan scripts](dreadnought-leviathan-scripts.md) - every observable function of the same scripts.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
