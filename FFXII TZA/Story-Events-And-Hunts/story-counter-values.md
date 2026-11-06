---
title: "Story counter values: every value the shipped scripts write to the main story counter, and the scripts and functions that write it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00265270, 0x0026CAF8, 0x02098E58, 0x002EF2B0"
---

## What it lists

The main story counter is the signed 16-bit word at the start of the save payload. Script variable slot 0 is bound to
the payload base (`0x0026CAF8`-`0x0026CAFD`, through the slot pointer `0x02098E58` and `0x002EF2B0`), and the native reader
is `FieldData_GetVariable0` (`0x00265270`). [Story flags](story-flags.md) shows the menus and map groups it unlocks.

The `unlocks` column gives what is gated on the counter reaching each value, placed on the lowest value here at or
above the gate's threshold, with `(at least N)` when the two differ: the shop lists whose condition is story progress
go on sale ([shops](../Items-Equipment-Shops-And-Licenses/shops.md), compared as at least the threshold at
`0x002FADF3`-`0x002FAE0D`), and Clan Primer entries unlock ([Clan Primer entries](../Menus-And-HUD/clan-primer-entries.md)).

It also gives the story schedule records of `mapjumpgroupflagrom.bin` that turn true or false there ([Story
flags](story-flags.md), reader `0x00377970`), and each scene read, `eventread` or `eventread_e8`, whose guard compares
the counter with a literal: the read needs the counter at least, below or at the value, and the rest of its guard
still applies. A scene's name is the `scene` of the area scene table row with that `event_id`.

It names the hunts posted from the value, on the clan boards or on Montblanc's list of marks, with the clan rank each
needs ([hunts](hunts.md), `posted`), and the airship routes that open, with the fare ([chocobos and
airships](../World-Areas-And-Travel/chocobos-and-airships.md)).

It lists, by region, the exits whose condition compares the counter with a literal ([script calls in every
script](script-censuses.md); each exit's row gives the whole condition) and the monsters placed only when the counter
passes a test ([enemy spawning](../Enemy-Spawning/enemy-spawning.md)), each with its test.

The table lists every value a script writes to it, from the 1,114 `us` scripts under `plan_master/us` that decode;
`evt_t0020` has no `EBP2` header and holds no code.

### How scripts write the counter

A script names the counter through the variable descriptor `0x30000000`, class 0, offset 0, a signed 16-bit value,
in its descriptor table (header `+0x28`). 513 scripts declare it as a variable of its own.

1. Every write is `PUSHII <value>` followed by `POPV <counter>`: 1,759 writes, and no write takes a value that is not
   a literal.
2. No script pushes a reference to the counter with `PUSHP`, so no verb writes it through a reference.
3. 193 scripts also declare the 256-word array that starts at the same offset. They write only its elements 2 and 3,
   136 times, never element 0.

### Where the writes are

| Scope | Writes | Scripts |
|---|---:|---:|
| shipping scripts, reached from a function entry | 268 | 156 |
| shipping scripts, in code no path reaches | 93 | 7 |
| developer menus, the `evt_t` scripts | 1,398 | 9 |

A write is reached when a walk from any function entry of its actor gets to it through fall-through and jump-table
targets, stopping at returns and at unconditional jumps (`0x51`, `0x5A`). The nine developer scripts are
`evt_t0081`-`evt_t0085`, `evt_t0090`, `evt_t0096`, `evt_t0500` and `evt_t0505`, whose actors are debug menus; 781
of their writes are in `evt_t0505`.

### The values

The scripts write 313 distinct values, from 0 to 11,000:

- 221 values are written by reached shipping code, from 13, by `naf_a01` `常駐監督.main`, to 7,150, by `bhm_d01`
  `ボス監督.main`. No reached shipping write is below 13.
- 4 values, 670, 1,210, 1,540 and 11,000, are written only in shipping code no path reaches.
- 88 values are written only by the developer menus, among them the two below 13, 0 and 10.

### The board ladder no path reaches

The clan board's `掲示板.talk` in `alc_f04`, `byu_a18`, `fon_b01`, `nac_a02`, `rbn_a16` and `var_a14`, and
Montblanc's `モンブラン.talk` in `rbn_a14`, hold a ladder that writes 290, 350, 670, 1,210, 1,540, 1,950, 1,982,
3,000, 3,250, 4,100, 5,150, 6,100 and 11,000; Montblanc's leaves out 670, 1,950 and 3,250 and repeats 5,150, 6,100
and 11,000.

An unconditional jump passes over the ladder (actor code offsets `alc_f04` `+0x453` to `+0x522`, `rbn_a14`
`+0x15A2` to `+0x1671`), and no instruction names its dispatcher's jump-table entry. So 91 of
the 93 unreached writes are this ladder. The other two, 710 and 720, are a choice menu in `byu_a18`
`配置監督.main`, which jumps over it at its first instruction.

### Guards

130 of the 268 reached shipping writes have a counter compare-and-jump, or a switch on the counter, before them in
the same function's bytecode. 125 lie inside such a test's branch: after the compare's conditional jump and before
that jump's target, or at or after a switch case's target. That is a control-flow property of the bytecode walk, and the `set_by` column
gives the test. The other writes are in functions that do
not test the counter, such as `touch`, `touchon` and named event functions, which their callers start.

## Columns

| Column | Meaning |
|---|---|
| `value` | the value written |
| `shipping_writes` | writes in shipping scripts that a path reaches |
| `set_by` | each such write as `script actor.function`, with `(when <test>)` for the counter test whose branch holds it, and `xN` for N writes in one function |
| `unreachable_writes` | writes in shipping code no path reaches |
| `unreachable_in` | where those writes are, as `script actor.function` |
| `developer_writes` | writes in the `evt_t` developer scripts |
| `developer_scripts` | those scripts, with `xN` for N writes |
| `explanation` | what the value marks, in English: the developers' name for it from the `evt_t0505` scenario menu (below), translated, then the maps whose scripts write it, as map name (region) from `planmapname.bin`; for the two values with neither, 1899 and 4090, the developer menu that sets it and the value it precedes |
| `developer_name` | the developers' own name for the value: each `SF_` line of the `evt_t0505` scenario menu that writes it, in menu order, `;` between lines; `-` for the values the menu has no line for |
| `unlocks` | what opens or changes when the counter reaches the value: shop lists on sale, Clan Primer entries, story schedule records turning true or false, scene reads that need the counter at least, below or at it, hunts posted, airship routes opening, and the exits and monster placements whose condition tests the counter; `-` when nothing opens or changes |

### The developers' names

The developer script `evt_t0505` carries a menu, `SCENARIO FLAG ONLY`, in its message bank (section 2, messages
30-50, 20 pages). Each of its 400 lines is `[value] SF_<name>`, and choosing a line writes that value: the
menu's first 400 counter writes carry the 400 line values in line order, and 13 more writes have no line. The
names cover 310 of the 313 values.

- `終了` ("after") names the value written once a scene has played: `SF_レモラバトル終了`, 18, is "after the
  Remora battle"; `開始` ("start of") opens a longer stretch.
- `シナリオ段階N` marks the start and end of eleven scenario stages; `MS_` lines name map unlocks.
- Proper names are the English the game ships for the same Japanese word: the `us` line in the slot of its `in`
  line, in the word banks, `planmapname.bin`, `npcdic.bin`, the text groups and the
  scripts' message banks. A name with no shipped English is left out of `explanation`, which describes the scene without it; `developer_name` keeps the menu line itself.
- Place words are the shipped area and region names of `planmapname.bin` and battle word bank 12.
- Value 70 is the one case where the developers' word is the shipped name of a different monster:
  `キラートマト` is Deadly Nightshade in word bank 8, but `dst_a01` writes 70 during the first hunt, between 65
  and 75, and that hunt's target is the Rogue Tomato (`はぐれトマト`, bank 8 slot 94). The row says Rogue Tomato.
- Where a value has two lines that differ only in an older and a newer name for one character, it keeps the
  line with the shipped name.

The map names come from the field each writing script loads as: the script's field id in the `us` zone path
table (`0x01EE23A0`), the area name at that id in `planmapname.bin`, and the region from the field's group word in
`map_ref.bin`.

Actor and function names are the ones the scripts carry.

## Related

- [Story flags](story-flags.md) - the menus and map groups the counter unlocks, and the save payload it starts.
- [Quests](quests.md) - the quest state kept beside the flag banks.
- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the payload's first `0x200` bytes, the script word
  bank the counter opens.
- [Script bytecode](../EBP-Script-Files/ebp-script-image.md) - `PUSHII`, `POPV`
  and the jump opcodes.
