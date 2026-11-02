---
title: "Rabanastre scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [rabanastre-scenes.tsv](rabanastre-scenes.tsv) has one row per scene script of Rabanastre under
`plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`,
`0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index
`4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `rbn_a0100` | `107` | North End | 25 | - |
| `rbn_a0200` | `100` | Muthru Bazaar | 12 | - |
| `rbn_a0300` | `101` | East End | 26 | - |
| `rbn_a0380` | `709` | East End | 16 | - |
| `rbn_a0381` | `711` | East End | 13 | - |
| `rbn_a0382` | `726` | Muthru Bazaar | 10 | - |
| `rbn_a0480` | `721` | Southern Plaza | 13 | - |
| `rbn_a0980` | `707` | Migelo's Sundries | 15 | - |
| `rbn_a1300` | `120` | Samalzalam Manor | 42 | story counter 1570, then Muthru Bazaar (Rabanastre), field `290` |
| `rbn_a1600` | `109` | The Sandsea | 22 | - |
| `rbn_a1601` | `119` | The Sandsea | 17 | - |
| `rbn_a1700` | `108` | Eastgate, Southgate and Westgate | 17 | - |
| `rbn_a1701` | `118` | Eastgate | 38 | - |
| `rbn_x0100` | `106` | field 860 (`rbn_x01`) | 21 | story counter 830, then Bridge (Dreadnought Leviathan), field `871` |
| `rbn_y0100` | `104` | field 910 (`rbn_y01`) | 66 | story counter 95 and 100, then North End (Rabanastre), field `289` |
| `rbn_z0100` | `102` | field 50 (`rbn_z01`) | 6 | story counter 301, then Stockade (Nalbina Dungeons), field `48` |

### What the scenes give

- `rbn_y0100`, played in field 910 from story counter 25 to 90, holds Vayne's arrival ("Is Rabanastre to your liking,
  my lord?" ... "Why don't you call me Vayne?" ... "We will have order!"); its first entry is "View scene again?" (Yes
  / No), and 95 and 100 follow it.
- `rbn_a0100`, in the North End at 100, holds Vaan and Penelo's talk ("Vaan! You haven't heard a single word I've
  said, have you." ... "All hail Vaan, sky pirate of Dalmasca!" ... "Time to pay Old Dalan a visit."); its first entry
  is "View scene again?" (Yes / No), and 105 follows it.
- `rbn_z0100`, in field 50 up to story counter 290, holds Penelo's words to Reks ("I brought you some of those flowers
  you like: Galbana lilies. Remember?" ... "Captain Basch must have tricked you into it!"); 301 and the Stockade
  follow it.
- `rbn_a0200`, in Muthru Bazaar at 33, holds the theft ("Huh? What'd you say?" ... "What? My pouch! It's gone!" / "The
  boy!"); 35 follows it.
- `rbn_a0300`, in East End at 35, holds Penelo's scolding ("Hey, that's mine!" ... "One of these days I'll fly an
  airship of my own." ... "He wanted you to drop by his place.").
- `rbn_a0380`, loaded in East End at 40, holds Migelo's errand ("Ah, Vaan, I was waiting." ... "I want you to run over
  to the Sandsea and fetch Kytes back! What do you say?"); 45 follows it.
- `rbn_a1601`, in The Sandsea at 45 or below, holds Tomaj's bill ("Got some nastiness out there in the Estersand
  what's stopping our couriers..." ... "That's right! Vaan, you should give it a shot!").
- `rbn_a0480`, in the Southern Plaza from 50 to 65, holds the writ at the gate ("You there! Let's see some papers,
  boy." ... "I got the writ of transit right here. See? Signed: Migelo." ... "Right! Gates are closed after this!");
  68 follows it.
- `rbn_a1701`, in Eastgate at 78, holds the closing of the gate ("How come you let these chocobos through the gate and
  not us?" ... "This gate's closed until the ceremony's over, do you hear?" ... "Open the gate!"); 80 and 85 follow
  it.
- `rbn_a1700`, in the gate the party reaches at 343, holds the return with Basch ("I'd avoid crowds, if I were you. In
  this town you're still a traitor, you know." ... "She'd be at Migelo's place this time of day."); 350 follows it.
- `rbn_a0980`, in Migelo's Sundries from 343 below 375, holds Kytes's welcome ("Vaan, is it really you? I heard you
  got took off to Nalbina!" ... "Tell you what. I'll go see him for you."); its first entry is "View scene again?"
  (Yes / No).
- `rbn_a0381`, in East End at 390, holds Vaan's talk with Basch ("A lot of kids lost their parents in the war." ...
  "My brother trusted you. And he was right."); 400 follows it.
- `rbn_a1600`, in The Sandsea at 400, holds the news of Penelo ("Oh, Vaan! They've taken Penelo!" ... "Come to the
  Bhujerba mines, it said." ... "Make yourselves ready. We leave soon."); 420 follows it.
- `rbn_x0100`, in field 860 from 1 to 800, holds Vayne's talk ("Now, I'm expecting Doctor Cid. You may leave." ...
  "They are welcome to try."); 830 and the Bridge follow it.
- `rbn_a1300`, in Samalzalam Manor below 1570, holds the talk of the Dawn Shard ("So it was the Dawn Shard that
  brought down the Imperial fleet." ... "The garif may know."); 1570 and Muthru Bazaar follow it.
- `rbn_a0382`, in Muthru Bazaar at 1570, holds the way south ("The garif are said to dwell in Kerwon." ... "Man cannot
  live by resolve alone, Princess."); 1580 follows it.
- No scene gives an item or changes the party.

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

- [Rabanastre scripts](rabanastre-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Dreadnought Leviathan scenes](dreadnought-leviathan-scenes.md) - the Bridge, where `rbn_x0100` leads.
- [Nalbina Dungeons scenes](nalbina-dungeons-scenes.md) - the Stockade, where `rbn_z0100` leads.
