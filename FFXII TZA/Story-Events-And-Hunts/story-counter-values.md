---
title: "Story counter values: every value the shipped scripts write to the main story counter, and the scripts and functions that write it"
kind: "reference"
category: "Story, events and hunts"
summary: "Each of the 313 values the us scripts assign to the main story counter, with the shipping scripts, actors and functions that write it and the counter test that guards each write, the writes in code no path reaches, the writes made only by the developer menus, and how the census found every write."
addresses: "00265270, 0026CAF8, 02098E58, 002EF2B0"
---

## What it lists

The main story counter is the signed 16-bit word at the start of the save payload. Script variable slot 0 is bound to
the payload base (`0026CAF8`-`0026CAFD`, through the slot pointer `02098E58` and `002EF2B0`), and the native reader
is `FieldData_GetVariable0` (`00265270`). [Story flags](story-flags.md) shows the menus and map groups it unlocks.

The table lists every value a script writes to it, from the 1,114 `us` scripts under `plan_master/us` that decode;
`evt_t0020` has no `EBP2` header and holds no code.

### How a write is found

A script names the counter through the variable descriptor `0x30000000`, class 0, offset 0, a signed 16-bit value,
in its descriptor table (header `+0x28`). 513 scripts declare it as a variable of its own.

1. Every write is `PUSHII <value>` followed by `POPV <counter>`: 1,759 writes, and no write takes a value that is not
   a literal.
2. No script pushes a reference to the counter with `PUSHP`, so no verb writes it through a reference.
3. 193 scripts also declare the 256-word array that starts at the same offset. They write only its elements 2 and 3,
   136 times, never element 0.
4. A byte search for each write pattern finds 1,759 at an instruction start and none inside another instruction.

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

Actor and function names are the ones the scripts carry.

## Related

- [Story flags](story-flags.md) - the menus and map groups the counter unlocks, and the save payload it starts.
- [Quests](quests.md) - the quest state kept beside the flag banks.
- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the payload's first `0x200` bytes, the script word
  bank the counter opens.
- [Script bytecode](../EBP-Script-Files/ebp-script-image.md) - `PUSHII`, `POPV`
  and the jump opcodes.
