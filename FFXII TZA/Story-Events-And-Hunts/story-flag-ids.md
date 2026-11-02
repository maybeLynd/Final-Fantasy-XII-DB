---
title: "Story flag ids: every flag id the US scripts set, release or test, by bank, with the scripts that touch it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x0032AB60, 0x0032A8A0, 0x0032ABF0, 0x0032ADF0, 0x0032AAD0, 0x00377970"
---

## What it lists

The table has one row per bank and flag id that a script under `plan_master/us` passes to a flag verb. The banks,
their accessors and what each holds are on [Story flags](story-flags.md). The developer menu `bin/mapctrl` also
sets Primary ids 155, 156, 196 and 197 (lines 2516-2517 and 2557-2558) and releases them (2655-2656 and
2696-2697), in the `in` and `ch` trees; no `us` script names them.

### How a call is read

A call's id is the instruction just before the verb call in the ff12-script listing of each script: `PUSHII` or
`PUSHI` is a literal, anything else is computed. The scripts make 13,098 flag-verb calls:

| Verb | Bank | Calls |
|---|---|---:|
| `setmapjumpgroupflag` `0x430` | Primary | 4,625 |
| `releasemapjumpgroupflag` `0x431` | Primary | 4,610 |
| `ismapjumpgroupflag` `0x432` | Primary | 3,667 |
| `settalknpcname` `0x399` | Bank2048 | 57 |
| `releasetalknpcname` `0x39A` | Bank2048 | 79 |
| `istalknpcname` `0x39B` | Bank2048 | 1 |
| `settreasureflag` `0x3F1` | Bank512, second half | 26 |
| `releasetreasureflag` `0x3F2` | Bank512, second half | 7 |
| `istreasureflag` `0x3F5` | Bank512, second half | 26 |

No script calls `setnaviicon`, `clearnaviicon`, `isnaviicon`, the three treasure-battle verbs or the six airship
verbs `setshutoralappear` to `isshutoralenable`.

Nine calls have a computed id:

- `ismapjumpgroupflag` twice in `hne_e01` `ギミック`;
- `settalknpcname` in the `talk` function of the clan board `掲示板` in `alc_f04`, `byu_a18`, `fon_b01`, `nac_a02`,
  `rbn_a16` and `var_a14`, and of Montblanc `モンブラン` in `rbn_a14`.

The `hne_e01` id is `0x15C && (g_com_マップ通行制限フラグ[1] & 0x1)` (`OPLAND` in `扉開く` and `扉開くＥＶ`): a logical and, so the call
tests id 1 while bit `0x1` of that byte is set and id 0 while it is clear, and the door sets `0x15C` when the tested
id is clear. Id 0 is on the new-game list; no script sets id 1.

The seven `settalknpcname` ids are slots of a name array that the same function fills with literals. On the six clan
boards, which share one array, slot n is the petitioner of quest 129 + n, set when the player takes that posted hunt,
just before `setquestorder`; at Montblanc slot n is quest 160 + n, set when the player says yes to it. The boards
reach 31 ids and Montblanc 10; each is a row of the table, with the call in `computed_set`:

| Caller | Slot | Quest | Hunt | Id | Name before | Name after |
|---|---:|---:|---|---|---|---|
| clan boards | 0 | 129 | Wolf in the Waste | `0x7B` | Rabanastran | Gatsly |
| clan boards | 1 | 130 | Dalmasca's Desert Bloom | `0x115` | Dantro | Dantro |
| clan boards | 2 | 131 | Waterway Haunting | `0x26D` | Caring Woman | Milha |
| clan boards | 3 | 132 | Marauder in the Mines | `0x18E` | Lhusu Parivir | Aekom |
| clan boards | 4 | 133 | Lost in the Pudding | `0x2E8` | Sorbet | Sorbet |
| clan boards | 5 | 134 | For Whom the Wyrm Tolls | `0x247` | Rabanastran | Balzac |
| clan boards | 6 | 135 | A Scream from the Sky | `0x10` | Imperial | Sherral |
| clan boards | 7 | 136 | A Tingling Toast | `0x4B` | Tavernmaster | Tavernmaster |
| clan boards | 8 | 137 | The Defense of Ozmone Plain | `0x1A2` | Garif Elder | Low-chief Sugumu |
| clan boards | 9 | 138 | A Ring in the Rain | `0xE9` | Quiet Man | Sadeen |
| clan boards | 10 | 139 | The Dead Ought Sleep Forever | `0x19D` | Great-chief Uball-Ka | Great-chief Uball-Ka |
| clan boards | 11 | 140 | Befoulment of the Beast | `0x1DA` | Kiltias | Kiltias |
| clan boards | 12 | 141 | A Chase Through the Woods | `0x200` | Viera Maiden | Nera |
| clan boards | 13 | 142 | The Mine Flayer | `0x1A4` | Garif Warrior | Warrior Guromu |
| clan boards | 14 | 143 | The Deserter's Revenge | `0x105` | No. 381 | No. 381 |
| clan boards | 15 | 144 | Trouble in the Hills | `0x2D6` | Burrogh | Burrogh |
| clan boards | 16 | 145 | Adding Insult to Injury | `0x2B3` | Morgen | Morgen |
| clan boards | 17 | 146 | Rodeo to the Death | `0x2F2` | Caravaner | Va'Kansa |
| clan boards | 18 | 147 | Shelled Obstruction | `0x3B9` | Archadian Ardent | Homesick Man |
| clan boards | 19 | 148 | Get My Stuff Back! | `0x341` | Viera Wayfarer | Viera Wayfarer |
| clan boards | 20 | 149 | Old Legends, Decaying Bonds | `0x3C5` | Archadian Vulgar | Fermon |
| clan boards | 21 | 150 | The Things We Do... | `0x3A5` | Archadian Ardent | Insecure Seeq |
| clan boards | 22 | 151 | The Creature Collector | `0x2B2` | Barrong | Barrong |
| clan boards | 23 | 152 | Dead City Watch | `0x2B4` | Popol | Popol |
| clan boards | 24 | 153 | Visitor on Deck | `0x2DA` | Son | Son |
| clan boards | 25 | 154 | The Child Snatcher | `0x191` | Miners' Ender Boy | Miclio |
| clan boards | 26 | 155 | The Black Sorcerer | `0x1DE` | Acolyte | Acolyte |
| clan boards | 27 | 156 | A Wild Stench | `0x202` | Warder-apprentice | Rena |
| clan boards | 28 | 157 | Paying for the Past | `0x1A0` | War-chief Supinelu | War-chief Supinelu |
| clan boards | 29 | 158 | Wyrm Wrath's Renewal | `0x1DC` | Ieeha | Ieeha |
| clan boards | 30 | 159 | Who's the Strongest!? | `0x2E4` | Rikken | Rikken |
| Montblanc | 0 | 160 | Little Love on the Big Plains | `0xDF` | Nomad | Dania |
| Montblanc | 1 | 161 | The Cry of Its Power | `0x18C` | Pilika | Pilika |
| Montblanc | 2 | 162 | Crime and Punishment | `0x246` | Contrite Thief | Contrite Thief |
| Montblanc | 3 | 163 | Paradise Risen | `0xE7` | Nomad | Nanau |
| Montblanc | 4 | 164 | Paramina Run | `0x34` | Gurdy | Gurdy |
| Montblanc | 5 | 165 | Antlion Infestation | `0x171` | Niray | Niray |
| Montblanc | 6 | 166 | Carrot Stalk | `0x2B5` | Zammadria | Zammadria |
| Montblanc | 7 | 167 | Battle on the Big Bridge | `0x2CD` | Montblanc | Montblanc |
| Montblanc | 8 | 168 | Truth Shrouded in Mist | `0x273` | Refugee | Koqmihn |
| Montblanc | 9 | 169 | Fishy Dreams | `0x342` | Whitecap Wench | Whitecap Wench |
| Montblanc | 10 | 170 | God or Devil? | `0x2CD` | Montblanc | Montblanc |
| Montblanc | 11 | 171 | Farewell to a Legend | `0x2CD` | Montblanc | Montblanc |
| Montblanc | 12 | 172 | A Dark Rumor | `0x2CD` | Montblanc | Montblanc |

### What the ids show

- Primary: 328 flag ids, from `0x2` to `0x166`, and the two schedule ids below. 250 of the flag ids are set but never
  tested by a script; the game's own readers of the gate `0x0032A8A0` are listed on [Story flags](story-flags.md).
- The schedule ids `0x4022` and `0x402A` are tested only. They read story schedule records `0x22`, true from story
  counter 5,150, and `0x2A`, true from 1,540, through `0x00377970`.
- Bank2048: 93 name ids. 58 are passed as a literal, 23 of them only by the developer menus, and 35 are reached
  only through the name arrays above; the one test is id `0xF0` in `sav_b01`. The table has 449 rows.
- Bank512, second half: 26 ids, `0x0`-`0x21`, each set once and tested once by shipping scripts; the seven releases
  are in the developer scripts.
- Seven ids of the new-game list `mapjumpgroupinit.bin` appear as no literal id in any script: 0, `0x56`, `0x65`,
  `0x66`, `0x10B`, `0x148` and `0x14B`; id 0 is the one the `hne_e01` test above reads while its bit is clear.

The `set_when` column gives, for a flag whose shipping set calls are all one call site in an actor's own `init`, `touchon`,
`main` or `talk` function, the actor and its field and the tests that enclose the call there, in the listing's `if`
and `switch` nesting: 60 flags. A set call with no test is made each time that function runs. The `set_conditions`
column gives every shipping set site of each of the 328 Primary flags with a shipping set call, these 60 included,
with the tests around each call.

## Columns

| Column | Meaning |
|---|---|
| `bank` | the flag bank, named as on [Story flags](story-flags.md) |
| `id` | the flag id |
| `new_game` | `yes` when `mapjumpgroupinit.bin` sets it on a new game |
| `set`, `release`, `test` | how many times shipping scripts set, release and test it with a literal id; the computed sets are in `computed_set` |
| `set_in`, `release_in`, `tested_in` | the shipping scripts that do so |
| `developer_only` | `yes` when only the developer scripts `evt_t*` name it |
| `explanation` | what the flag opens or records, in English, then the maps whose scripts set or test it, as map name (region): see below |
| `computed_set` | the script that sets the id through a computed id (the clan boards and Montblanc above), with the hunt; `-` when no script does |
| `set_when` | the one call site that sets the flag, as above, and the tests around it; `-` for the other flags |
| `set_conditions` | every shipping set site of the flag: its place (map name (region), field and script), actor, function and listing line, then the tests around the call in game terms; sites with the same actor, function and tests are one entry. A saved value a test reads is named by its label, whose stores are in [saved-value-stores.tsv](../World-Areas-And-Travel/saved-value-stores.tsv); `-` for a flag with no shipping set call |

### Set sites

[story-flag-set-sites.tsv](story-flag-set-sites.tsv) has one row for each of the 4,625 shipping set sites of the 328
Primary flags with a shipping set call: `flag_id` (as in this table), `map_name` (map name and region), `field`,
`script`, `actor`, `function`, `line` (the listing line), `verb` and `condition` (the tests around the call in game
terms; `always` when the call has no test). The 8 sites of `mic_b07`, a script no zone loads, and the 1 site of
`ttl_z0009`, the scene of the Royal Palace location title, have `-` for the map and the field.

A test of a saved value names the value by a label, such as `the value of alc_b03 file_var_s7_1`, the script and the
variable's name in its listing. [saved-value-stores.tsv](../World-Areas-And-Travel/saved-value-stores.tsv) gives every
store of each label with that store's own condition, so each store is written once and a cell does not repeat it.

### Where the explanations come from

- **Primary.** Every story gate in the shipped `us` map files that names the id: the location map
  (`menumap_location.bin`: zones, exit markers and links), the map directory and guide schedule
  (`menumap_common.bin`), the guide lines (`menumap_guide*.bin`) and the icons of each zone script's section 4
  ([navigation icons](../EBP-Script-Files/ebp-navigation-icons.md)).
- **Gate readers.** They are on [map menu files](../Game-Files-And-Data-Tables/menu-map-files.md).
- **Map lines.** The 16-byte records of the zone script image's `+0x8C` table (`0x00264870`). `0x00264920` passes
  words 0 and 1, a mode word (4 while riding a chocobo, 3 during a summon, else 2) and word 6 to the gate
  ([map screens](../Menus-And-HUD/map-screens.md)). The 4,141 records of the 769 `us` zone images explain 69 flags that the
  sources above leave with only their places, on records a line names by its byte `+0x1D` (`0x0026490E`).
- **What the map-line words do.** The minimap draws a line while word 0 passes (`0x003C35DA`) and the field its
  markers while word 1 passes (`0x003F9BC5`); the mode word picks the line's colours (`0x003C35E1`), and word 6 lets
  the label name the area of word 5 (`0x003F99DE`).
- **Two script flags.** Id `0x73` is the chocobo riding flag, and the aerodrome counter scripts set `0x5E` before
  the airship-deck and attack jumps ([chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md)).
- **Schedule ids.** `0x4022` and `0x402A` read records `0x22` and `0x2A` of `mapjumpgroupflagrom.bin`, each a
  one-value record (5,150 and 1,540), as [Story flags](story-flags.md) describes the reader `0x00377970`.
- **Bank2048.** The name pair the id selects in `us` `npcdic.bin`, entries `2 × id` and `2 × id + 1`
  ([NPC names](../Characters-And-Objects/npc-names.md)).
- **Places.** Each script in `set_in` and `tested_in` is the field whose entry in the `us` zone path table
  (`0x01EE23A0`) names it, with the area name from `planmapname.bin` and the region from `map_ref.bin`.

## Related

- [Story flags](story-flags.md) - the banks, the gate and the story schedule.
- [Story counter values](story-counter-values.md) - the counter the schedule compares against.
