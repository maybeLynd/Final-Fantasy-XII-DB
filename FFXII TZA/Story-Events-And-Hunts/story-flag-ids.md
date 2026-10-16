---
title: "Story flag ids: every flag id the shipped scripts set, release or test, by bank, with the scripts that touch it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0032AB60, 0032A8A0, 0032ABF0, 0032ADF0, 0032AAD0, 00377970"
---

## What it lists

The table has one row per bank and flag id that a script under `plan_master/us` passes to a flag verb. The banks,
their accessors and what each holds are on [Story flags](story-flags.md).

### How a call is read

A call's id is the instruction just before the verb call in the ff12-script listing of each script: `PUSHII` or
`PUSHI` is a literal, anything else is computed. The scripts make 13,098 flag-verb calls:

| Verb | Bank | Calls |
|---|---|---:|
| `setmapjumpgroupflag` `430`<sub>h</sub> | Primary | 4,625 |
| `releasemapjumpgroupflag` `431`<sub>h</sub> | Primary | 4,610 |
| `ismapjumpgroupflag` `432`<sub>h</sub> | Primary | 3,667 |
| `settalknpcname` `399`<sub>h</sub> | Bank2048 | 57 |
| `releasetalknpcname` `39A`<sub>h</sub> | Bank2048 | 79 |
| `istalknpcname` `39B`<sub>h</sub> | Bank2048 | 1 |
| `settreasureflag` `3F1`<sub>h</sub> | Bank512, second half | 26 |
| `releasetreasureflag` `3F2`<sub>h</sub> | Bank512, second half | 7 |
| `istreasureflag` `3F5`<sub>h</sub> | Bank512, second half | 26 |

No script calls `setnaviicon`, `clearnaviicon`, `isnaviicon`, the three treasure-battle verbs or the six airship
verbs `setshutoralappear` to `isshutoralenable`.

Nine calls have a computed id:

- `ismapjumpgroupflag` twice in `hne_e01` `ギミック`;
- `settalknpcname` in the `talk` function of the clan board `掲示板` in `alc_f04`, `byu_a18`, `fon_b01`, `nac_a02`,
  `rbn_a16` and `var_a14`, and of Montblanc `モンブラン` in `rbn_a14`.

### What the ids show

- Primary: 328 flag ids, from `2`<sub>h</sub> to `166`<sub>h</sub>, and the two schedule ids below. 250 of the flag ids are set but never
  tested by a script; the game's own readers of the gate `0032A8A0` are listed on [Story flags](story-flags.md).
- The schedule ids `4022`<sub>h</sub> and `402A`<sub>h</sub> are tested only. They read story schedule records `22`<sub>h</sub>, true from story
  counter 5,150, and `2A`<sub>h</sub>, true from 1,540, through `00377970`.
- Bank2048: 58 name ids, 23 of them named only by the developer menus; the one test is id `F0`<sub>h</sub> in `sav_b01`.
- Bank512, second half: 26 ids, `0`<sub>h</sub>-`21`<sub>h</sub>, each set once and tested once by shipping scripts; the seven releases
  are in the developer scripts.
- Seven ids of the new-game list `mapjumpgroupinit.bin` appear in no script: 0, `56`<sub>h</sub>, `65`<sub>h</sub>, `66`<sub>h</sub>, `10B`<sub>h</sub>,
  `148`<sub>h</sub> and `14B`<sub>h</sub>.

## Columns

| Column | Meaning |
|---|---|
| `bank` | the flag bank, named as on [Story flags](story-flags.md) |
| `id` | the flag id |
| `new_game` | `yes` when `mapjumpgroupinit.bin` sets it on a new game |
| `set`, `release`, `test` | how many times shipping scripts set, release and test it |
| `set_in`, `release_in`, `tested_in` | the shipping scripts that do so |
| `developer_only` | `yes` when only the developer scripts `evt_t*` name it |
| `explanation` | what the flag opens or records, in English, then the maps whose scripts set or test it, as map name (region): see below |

### Where the explanations come from

- **Primary.** Every story gate in the shipped `us` map files that names the id: the location map
  (`menumap_location.bin`: zones, exit markers and links), the map directory and guide schedule
  (`menumap_common.bin`), the guide lines (`menumap_guide*.bin`) and the icons of each zone script's section 4
  ([navigation icons](../EBP-Script-Files/ebp-navigation-icons.md)).
- **Gate readers.** They are on [map menu files](../Game-Files-And-Data-Tables/menu-map-files.md).
- **Two script flags.** Id `73`<sub>h</sub> is the chocobo riding flag, and the aerodrome counter scripts set `5E`<sub>h</sub> before
  the airship-deck and attack jumps ([chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md)).
- **Schedule ids.** `4022`<sub>h</sub> and `402A`<sub>h</sub> read records `22`<sub>h</sub> and `2A`<sub>h</sub> of `mapjumpgroupflagrom.bin`, each a
  one-value record (5,150 and 1,540), as [Story flags](story-flags.md) describes the reader `00377970`.
- **Bank2048.** The name pair the id selects in `us` `npcdic.bin`, entries `2 × id` and `2 × id + 1`
  ([NPC names](../Characters-And-Objects/npc-names.md)).
- **Places.** Each script in `set_in` and `tested_in` is the field whose entry in the `us` zone path table
  (`01EE23A0`) names it, with the area name from `planmapname.bin` and the region from `map_ref.bin`.

## Related

- [Story flags](story-flags.md) - the banks, the gate and the story schedule.
- [Story counter values](story-counter-values.md) - the counter the schedule compares against.
