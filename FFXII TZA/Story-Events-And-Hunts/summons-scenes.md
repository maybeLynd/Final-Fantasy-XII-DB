---
title: "Summon scenes: the scenes an Esper's summon plays, in sets of three"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00, 0x00306BD0, 0x0032FC30, 0x00309230, 0x00D103B0"
---

## What it lists

The table [summons-scenes.tsv](summons-scenes.tsv) has one row per scene script of the group `sum` under
`plan_master/us/event`, the summon scenes ([graphics settings](../Engine-Core/graphics-settings.md)). No
zone script shares their file-name prefix, so their `next` column is `-`, and no `eventread` or
`eventread_e8` call of the zone and scene scripts names their event ids 40 to 78.

The battle scene step `0x00306BD0` requests them on scene manager 3 through `0x0032FC30` (`0x00306C56`), by the effect id
that `0x00309230` gives for the action: the Esper's summon action, its finishing attack, or Dismiss, for which it takes
the event by the Esper from the table at `0x00D103B0` (Zodiark's 78 is stored at `0x00309266`). The `loaded_by` column
gives each.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `sum_a0000` | `40` | the battle scene step `0x00306BD0`: Belias summoned | 0 | - |
| `sum_a0001` | `41` | the battle scene step `0x00306BD0`: Hellfire | 1 | - |
| `sum_a0002` | `42` | the battle scene step `0x00306BD0`: Belias dismissed | 0 | - |
| `sum_b0000` | `73` | the battle scene step `0x00306BD0`: Ultima summoned | 0 | - |
| `sum_b0001` | `74` | the battle scene step `0x00306BD0`: Eschaton | 0 | - |
| `sum_b0002` | `75` | the battle scene step `0x00306BD0`: Ultima dismissed | 0 | - |
| `sum_c0000` | `67` | the battle scene step `0x00306BD0`: Zeromus summoned | 0 | - |
| `sum_c0001` | `68` | the battle scene step `0x00306BD0`: Big Bang | 1 | - |
| `sum_c0002` | `69` | the battle scene step `0x00306BD0`: Zeromus dismissed | 0 | - |
| `sum_d0000` | `64` | the battle scene step `0x00306BD0`: Chaos summoned | 0 | - |
| `sum_d0001` | `65` | the battle scene step `0x00306BD0`: Tornado | 1 | - |
| `sum_d0002` | `66` | the battle scene step `0x00306BD0`: Chaos dismissed | 0 | - |
| `sum_e0000` | `49` | the battle scene step `0x00306BD0`: Hashmal summoned | 0 | - |
| `sum_e0001` | `50` | the battle scene step `0x00306BD0`: Gaia's Wrath | 0 | - |
| `sum_e0002` | `51` | the battle scene step `0x00306BD0`: Hashmal dismissed | 0 | - |
| `sum_f0000` | `52` | the battle scene step `0x00306BD0`: Cúchulainn summoned | 0 | - |
| `sum_f0001` | `53` | the battle scene step `0x00306BD0`: Blight | 1 | - |
| `sum_f0002` | `54` | the battle scene step `0x00306BD0`: Cúchulainn dismissed | 0 | - |
| `sum_g0000` | `58` | the battle scene step `0x00306BD0`: Zalera summoned | 0 | - |
| `sum_g0001` | `59` | the battle scene step `0x00306BD0`: Condemnation | 0 | - |
| `sum_g0002` | `60` | the battle scene step `0x00306BD0`: Zalera dismissed | 0 | - |
| `sum_h0000` | `46` | the battle scene step `0x00306BD0`: Adrammelech summoned | 0 | - |
| `sum_h0001` | `47` | the battle scene step `0x00306BD0`: Judgment Bolt | 0 | - |
| `sum_h0002` | `48` | the battle scene step `0x00306BD0`: Adrammelech dismissed | 0 | - |
| `sum_i0000` | `55` | the battle scene step `0x00306BD0`: Famfrit summoned | 0 | - |
| `sum_i0001` | `56` | the battle scene step `0x00306BD0`: Tsunami | 0 | - |
| `sum_i0002` | `57` | the battle scene step `0x00306BD0`: Famfrit dismissed | 0 | - |
| `sum_j0000` | `43` | the battle scene step `0x00306BD0`: Mateus summoned | 0 | - |
| `sum_j0001` | `44` | the battle scene step `0x00306BD0`: Frostwave | 1 | - |
| `sum_j0002` | `45` | the battle scene step `0x00306BD0`: Mateus dismissed | 0 | - |
| `sum_k0000` | `61` | the battle scene step `0x00306BD0`: Shemhazai summoned | 0 | - |
| `sum_k0001` | `62` | the battle scene step `0x00306BD0`: Soul Purge | 0 | - |
| `sum_k0002` | `63` | the battle scene step `0x00306BD0`: Shemhazai dismissed | 0 | - |
| `sum_l0000` | `70` | the battle scene step `0x00306BD0`: Exodus summoned | 0 | - |
| `sum_l0001` | `71` | the battle scene step `0x00306BD0`: Meteor | 0 | - |
| `sum_l0002` | `72` | the battle scene step `0x00306BD0`: Exodus dismissed | 0 | - |
| `sum_m0000` | `76` | the battle scene step `0x00306BD0`: Zodiark summoned | 0 | - |
| `sum_m0001` | `77` | the battle scene step `0x00306BD0`: Final Eclipse | 1 | - |
| `sum_m0002` | `78` | the battle scene step `0x00306BD0`: Zodiark dismissed | 0 | - |

### The scenes

- The summon scenes come in thirteen sets of three, `sum_a` to `sum_m`, each a `0000`, `0001` and `0002` scene with
  three consecutive event ids, from `sum_a` (events 40 to 42) to `sum_m` (events 76 to 78).
- Six of the `0001` scenes hold one entry, a replay question: `sum_a0001`, `sum_d0001` and `sum_m0001` ask "Replay？"
  (yes / no), and `sum_c0001`, `sum_f0001` and `sum_j0001` ask `大技再度見ます？` (`見る` / `見ない`). The other 33 scenes hold no
  entries.
- No scene gives an item, sets a flag, writes the story counter or changes the party.
- The scripts table [`summons-scripts.tsv`](summons-scripts.tsv), with the columns of the zone scripts tables,
  has no row: no function of the thirty-nine scripts shows a line, and no step asks the replay questions above.

### Every step

The steps table [`summons-script-steps.tsv`](summons-script-steps.tsv) has one row for each step of every function of
the thirty-nine scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 7,800 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `sum_a0000` | 109 | `sum_g0001` | 371 |
| `sum_a0001` | 432 | `sum_g0002` | 60 |
| `sum_a0002` | 60 | `sum_h0000` | 104 |
| `sum_b0000` | 104 | `sum_h0001` | 379 |
| `sum_b0001` | 339 | `sum_h0002` | 60 |
| `sum_b0002` | 60 | `sum_i0000` | 104 |
| `sum_c0000` | 104 | `sum_i0001` | 339 |
| `sum_c0001` | 580 | `sum_i0002` | 60 |
| `sum_c0002` | 60 | `sum_j0000` | 109 |
| `sum_d0000` | 104 | `sum_j0001` | 546 |
| `sum_d0001` | 345 | `sum_j0002` | 60 |
| `sum_d0002` | 60 | `sum_k0000` | 104 |
| `sum_e0000` | 104 | `sum_k0001` | 381 |
| `sum_e0001` | 714 | `sum_k0002` | 60 |
| `sum_e0002` | 60 | `sum_l0000` | 104 |
| `sum_f0000` | 104 | `sum_l0001` | 346 |
| `sum_f0001` | 523 | `sum_l0002` | 60 |
| `sum_f0002` | 60 | `sum_m0000` | 104 |
| `sum_g0000` | 104 | `sum_m0001` | 363 |
| | | `sum_m0002` | 60 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). None of these scripts carries
one of them, so this table has no `shared template` row.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 7,644 |
| empty | 156 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `sum_j0001` (event `44`), `進行監督.カット１` starts scene cut
1, plays effect slot 10, turns user control off and moves the summon group into summon space. It starts `カメラ.カット１` and
two more requests together, reads model `0x03000000`, motion 1 of `sum_j0001.mot` and three effect files, waits 140
frames and waits for the model and motion. It files `summon.召喚準備` and `summon_weapon_pon.召喚準備`, waiting until each
ends, and waits until `summon.カット１` ends.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the exe step that requests the scene: the battle scene step `0x00306BD0` and the action whose effect id is the event, or for Dismiss, whose effect id is not an event, the event that `0x00309230` takes by the Esper from the table at `0x00D103B0`; with the addresses read |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)`; a scene with no non-empty entry: one sentence of what its script does; an entry the `us` tree ships in Japanese: an English sentence, then `Authored text (<its English>): ` and the entry |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |

The steps table [`summons-script-steps.tsv`](summons-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test` |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test |
| `addresses` | what the arguments name in the game: the actor, model, animation and motion file, effect file, event sound, camera shot, message window, request slot or variable |
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its text codes dropped; `-` for every other step |
| `timing` | the frames, fade lengths and speeds the step uses |
| `sync` | what the step waits for, and for a request whether it waits until the function starts, until it ends or not at all |
| `calls` | the functions a request starts, as `actor.function`; for a `goto` into another function, that function |
| `resolution` | `resolved`; `does not ship:` and the fact; or empty |
| `source` | the page or table that gives the meaning, or the function whose body was read |

The shared steps table [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv) has the same columns from `at`
on, after these:

| Column | Meaning |
|---|---|
| `template` | the template id that the `shared template` rows name |
| `actor`, `function`, `step` | the shared actor, its function and the step number |
| `reference` | the script whose copy of the function the steps were read from, and where the function starts there |

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids,
section 3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other
scripts' copies differ only in these.

## Related

- [Quickenings and summons](../Battle-Actions/quickenings-and-summons.md) - the battle scene a summon plays, one at a time.
- [Graphics settings](../Engine-Core/graphics-settings.md) - the depth of field a summon scene's own file can override.
- [Special move scenes](special-move-scenes.md) - the other battle scene group.
