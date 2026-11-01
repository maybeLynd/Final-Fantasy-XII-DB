---
title: "Nalbina Town scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x003459C0, 0x00377B60, 0x003778B0, 0x0034ADA0, 0x0034B760, 0x0034BB10"
---

## What it lists

The table [nalbina-town-scripts.tsv](nalbina-town-scripts.tsv) has one row per script function of Nalbina Town that
does something a player can observe. It covers the four zone scripts and the one scene script of the area, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `nac_a01` | zone | West Barbican, field `630` | 46 | 300 | 22 | 5 |
| `nac_a02` | zone | Jajim Bazaar, field `631` | 50 | 320 | 46 | 1 |
| `nac_a03` | zone | West Ward, field `632` | 51 | 381 | 52 | 0 |
| `nac_b01` | zone | Aerodrome, field `800` | 38 | 261 | 30 | 0 |
| `nac_a0300` | scene | event `125` | 24 | 167 | 6 | 0 |

West Barbican carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`.
Jajim Bazaar carries only `イベント特殊効果画面`. Their functions are described once on
[Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map or loads a scene.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scene itself, with its dialogue, is on [Nalbina Town
scenes](nalbina-town-scenes.md).

### What the scripts do

- West Barbican: `監督.main` sets flags `0x0025` and `0x0020`, which open the location map's exits between Nalbina
  Town and the Mosphoran Highwaste and the Dalmasca Estersand.
- West Barbican: the roadblock actor `通行止め監督` turns back a party that slips past the soldiers toward the
  Mosphoran Highwaste ("Imperial army's engaged in a sweep of the Mosphoran Highwaste. No civilians allowed."); the
  soldiers' blocking area is removed only while the story counter is above 1520.
- West Barbican: the same actor's `通行解除イベント再生` shows the soldiers Deweg and Gibbs ("You're not afraid of
  the chocobo, are you, Gibbs?"), and
  `山通行解除.解除` sets flag `0x0144`. Gurdy, the chocobo seller (`NAC_ガーディ.talk_gardy`), sets flag `0x0073`,
  riding a chocobo.
- Jajim Bazaar: the notice board (`掲示板.talk`) shows the hunt bills, and the petitioners Burrogh and Popol
  (`依頼人ブロッホ`, `依頼人ポポル`) talk about their marks, the atomos and the deathscythe ([Hunts](hunts.md)).
- West Ward: `監督.main` writes 300, loads and plays scene `nac_a0300`, writes 301 and jumps to the Stockade
  (Nalbina Dungeons), field `48`, entrance 0. The petitioners Morgen and Barrong talk about the Roblon and Goliath.
- West Ward: Jovy (`ジョニー`) speaks from six `talk_step` functions, and `ロケイベント監督.ジョニーお礼渡す` gives the reward
  package that holds an Elixir and a Knot of Rust. The door `扉.開く` jumps to the Aerodrome, field `800`, entrance 1.
- Aerodrome: the airship counters (`乗船カウンタートーク`) show the boarding lines ("You are now free to board.",
  "you don't have enough gil"), set flag `0x005E` and jump to the Sky Saloon or the Observation Parlour
  (Skyferry) or to the aerodromes of Rabanastre, Nalbina Town, Bhujerba, Archades and Balfonheim Port.
- Aerodrome: `監督.main` and `発着イベント監視.イベント再生とマップジャンプ` load scene `pas_z0000`
  ([Aerodrome airship scene](aerodrome-airship-scenes.md)).
- Aerodrome: the private airship desk (`シュトラール受付.talk_step01`) loads scene `str_z0000`
  ([Strahl scene](strahl-scenes.md)) and jumps to a field held in a variable. Nono talks about the
  Strahl's repair, and the petitioner Zammadria talks about her mark, Carrot.
- West Barbican holds a crystal; what touching it does, the teleport and its Teleport Stone are on
  [Shared zone-script actors](shared-zone-script-actors.md).

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | a question and its choices: the second argument is a section 2 text id (`0x0034B760` and `0x0034BB10` jump to `0x0034ADA0`) |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname` | `0x399` | `0x0034DFA0` | `flags_set` | Bank2048 flag, the name-tag flags ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem_47f`, `additemmes`, `subitem` | `0x47F`, `0x480`, `0x2F2` | `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |

The story counter is the script's global `short` at offset 0, named `シナリオフラグ` in these scripts: every
assignment to it is a write and every comparison a test ([story counter values](story-counter-values.md)).

### The four message verbs reach one window call

The four message verbs all end in `mes` (`0x461`, `0x00348DF0`), which looks the text id up in the issuing script's
section 2 ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)):

1. `amese` (`0x0034A420`) pushes 0, 0, 0 and -1; `amest` (`0x0034A090`) pushes 0; `ames` (`0x00349BF0`) pushes 1. Each then
   jumps to `0x00349800`, the body of `ames_1fe`.
2. `0x00349800` pops two values (`0x00349827`, `0x00349831`), pushes 0 and 0 (`0x0034983D`, `0x00349847`) and then pushes the
   two values back in their original order (`0x00349851`, `0x0034985B`), so the zeros lie beneath them; it jumps to
   `0x00348DF0` (`0x00349884`).
3. `0x00348DF0` pops eight values. The seventh, the script's second argument, is passed with the current field context
   to `0x00264D60` (`0x00348E6A`-`0x00348E74`), the section 2 lookup, which keeps the low 24 bits of the id.

### Speakers, places and scenes

- The speaker of a line is the name its window shows. A `{name:P}` header (escape `0F 8`) names pair P in `us`
  `npcdic.bin`, P read as the parser `0x003FFB00` reads it. A plain name before the first line break,
  after `{instant:8181}` or at the start of a zone line, shows that name. An `{actor-name}` header (escape `0F >`)
  shows the name `0x00263990` gives the actor the window speaks for.
- The header's name comes from `0x002639E0`, which three of the five callers of `0x003FFB00` call next
  (`0x002ADDAA`, `0x002B16D4`, `0x002B52EF`): the first name while the pair's name flag is clear, the second once it is set. The
  `speaker` cell gives the second name. The window sets the flag of the pair of the actor it speaks for (next
  item), and `settalknpcname` sets any pair's ([NPC names](../Characters-And-Objects/npc-names.md)).
- The window speaks for the message call's target, the calling actor or the actor an `X.` prefix names: `0x002621D0`
  passes it to the verb, and `0x00348DF0` hands it to `0x002E16B0`. That actor's name is the second name of each pair its
  `setnpcname` calls name; `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- An actor no `setnpcname` or `setshopname` call names keeps the name id `0xFFFF` and the empty text the record set-up
  `0x00266530` writes (`0x0026668B`, `0x0026669B`-`0x002666B4`), so its `{actor-name}` header shows no name; that line reads
  `no name shown`. A system message reads `system message`.
- A line whose text carries no name takes the window actor's `setnpcname` name. Failing that, a scene subtitle
  (centred, or in the subtitle font `{alt-font}`) takes the character the window speaks for.
- Then any line without a name takes the speaker of the voice cue joined to it ([Voices](../Sound-And-Music/voices.md)),
  else the actor of the row's `TAGmes_<actor>_<n>` function, else the actor whose mouth function (`paku_on`,
  `unapaku_on`, `クチウナオン`, `kutipaku_on`, `kutipakuON`) is requested in its window or around the request of its
  function.
- A character's game name is the second name its `setnpcname` gives; else the party member whose model its bind verbs
  name, the `c` entries of the script's [actor manifest](../EBP-Script-Files/ebp-actor-manifest.md) read
  against the `model` column of the [party table](../Party/party-table.md), a main member before a guest; else
  the NPC name or string table row whose `in` cell is the actor's name.
- An actor these steps leave unnamed whose bind verbs name one `n` entry of the manifest takes the name the game
  gives the other actors bound to that `n` model, by these steps or as a voice cue's speaker
  ([Voices](../Sound-And-Music/voices.md)), when they all give one name and two or more actors give it or the bestiary
  gives the same.
- Failing that, it takes the [bestiary](../Enemy-Spawning/bestiary.md) name of that model id (its
  `model_id` cell), when the bestiary gives it one name. A `c` model is left out of these two steps, since the
  bestiary can name a battle alias there: Amalia for Ashe's `c11`.
- Any other line without a name reads `no name shown`, apart from a scene subtitle, which keeps its row's cell `-`. A
  line whose name is `???` reads `???`: the game prints `???` as that speaker's name at that line. A row lists its
  speakers in line order, each once.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`nalbina-town-script-steps.tsv`](nalbina-town-script-steps.tsv) has one row for each step of every
function of the five scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 15,051 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `nac_a01` | 2,626 | `nac_a03` | 3,693 |
| `nac_a02` | 3,677 | `nac_b01` | 3,958 |
| | | `nac_a0300` | 1,097 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Nalbina Town has 39 such rows.

Some actors run another actor's code: `DeathGazeFamily_Mama` in `nac_b01` starts at the same place as
`DeathGazeFamily_Papa` and runs the same functions. Such an actor has one `same code` row naming the actor whose steps
it runs. There are 2 of these rows: 2 in `nac_b01`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 14,992 |
| empty | 57 |
| `does not ship`, with the fact | 2 |

The two `does not ship` rows are `motionread` calls that read an empty entry: entry 2 of `nac_a01.mot` and entry 0 of
`nac_b01.mot`. A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the
arguments as the script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry
what they give for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `nac_a0300` (event `125`), `DIRECTOR.main` hides the
HUD, turns user control off and reads voice slot 0, its eight models (`0x03000000` to `0x03000007`) and motion 1 of
`nac_a0300.mot`, waiting for each. It then files `AD.準備_ad` and the cuts `AD.カット１_ad` to `AD.カット９_ad` (with
`AD.カット５_SUB_ad` after the fifth) one after another, waiting until each ends, and then `AD.終了_ad`. It frees the
motion, the models and the voice slot, and disposes of event manager slots 0 and 1.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown` or `system message`; `-` for a row without a section 2 line, and for a scene row with a subtitle none of those rules names |
| `lines` | the section 2 entries the function passes to the message verbs and the ask verbs |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a Bank2048 flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [nalbina-town-script-list.tsv](nalbina-town-script-list.tsv) holds the first table above, one row
per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`nalbina-town-script-steps.tsv`](nalbina-town-script-steps.tsv) has one row per step:

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

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Nalbina Town scenes](nalbina-town-scenes.md) - the scene these scripts own.
- [Aerodrome airship scene](aerodrome-airship-scenes.md) and [Strahl scene](strahl-scenes.md) - the two scenes the Aerodrome loads.
- [Nalbina Dungeons scripts](nalbina-dungeons-scripts.md) - the Stockade, where West Ward's jump leads.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
- [Hunts](hunts.md) - the marks the petitioners post.
