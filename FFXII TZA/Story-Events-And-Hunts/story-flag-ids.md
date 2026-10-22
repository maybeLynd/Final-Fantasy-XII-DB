---
title: "Story flag ids: every flag id the shipped scripts set, release or test, by bank, with the scripts that touch it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x0032AB60, 0x0032A8A0, 0x0032ABF0, 0x0032ADF0, 0x0032AAD0, 0x00377970"
---

## What it lists

The table has one row per bank and flag id that a script under `plan_master/us` passes to a flag verb. The banks,
their accessors and what each holds are on [Story flags](story-flags.md).

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

### What the ids show

- Primary: 328 flag ids, from `0x2` to `0x166`, and the two schedule ids below. 250 of the flag ids are set but never
  tested by a script; the game's own readers of the gate `0x0032A8A0` are listed on [Story flags](story-flags.md).
- The schedule ids `0x4022` and `0x402A` are tested only. They read story schedule records `0x22`, true from story
  counter 5,150, and `0x2A`, true from 1,540, through `0x00377970`.
- Bank2048: 58 name ids, 23 of them named only by the developer menus; the one test is id `0xF0` in `sav_b01`.
- Bank512, second half: 26 ids, `0x0`-`0x21`, each set once and tested once by shipping scripts; the seven releases
  are in the developer scripts.
- Seven ids of the new-game list `mapjumpgroupinit.bin` appear in no script: 0, `0x56`, `0x65`, `0x66`, `0x10B`,
  `0x148` and `0x14B`.

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
