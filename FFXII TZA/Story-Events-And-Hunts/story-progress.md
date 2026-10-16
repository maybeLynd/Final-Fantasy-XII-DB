---
title: "Story progress: the main story counter at the start of the save, the script variables that live in the save, and how scenes move the story on"
kind: "system"
category: "Story, events and hunts"
summary: "Where the story stands and how it moves: the six classes of script variable and the one that is the save payload itself, read and written live, the main story counter as the payload's first word, the native code that reads it, how zone director scripts raise it behind a test of its current value, the values only the developer menus set, and where the flags and quests that sit beside it are described."
addresses: "002625E7, 002626A8, 0026CAF8, 002EF2B0, 00265270, 02098E58"
---

## What the player sees

- The story moves forward one scene at a time and never back: a scene that has played does not play again, and towns,
  people and menus change after it.
- Loading a save puts every scene, talk and menu back where the story stood.

## How it works

### Script variables

A script names a variable by a descriptor: a class in the top bits and an offset in the low 24 bits. The resolver
picks the base for the class through the jump table at `002626A8` (`002625EA`-`00262603`) and adds the offset
(`00262639`-`00262641`):

| Class | Base | Set at |
|---:|---|---|
| `0` | the save payload, actor manager `+0x48` (`00262605`) | `0026CAF8`-`0026CAFD` |
| `1` | actor manager `+0x40` (`0026260B`) | - |
| `2` | the address the callback at `+0x98` returns (`00262611`-`00262617`) | - |
| `3` | the script image plus its own `+0x40` word (`00262633`-`00262636`) | - |
| `4` | actor manager `+0x58` (`00262627`) | - |
| `5` | actor manager `+0x60` (`0026262D`) | - |

Class 0 is the save payload itself: `002EF2B0` returns the active save buffer plus `0x200` (`002EF2B4`-`002EF2B9`), and
the actor manager keeps that pointer at `+0x48` when it binds the loaded definitions (`0026CAF8`-`0026CAFD`). So a
class-0 variable at offset *n* is payload byte *n*, read and written on every access with no copy.

### The story counter

The main story counter is the 16-bit word at payload `+0x0`, class 0 offset 0. 513 scripts declare it alone and 193
declare a 256-word array that starts at the same byte ([Story counter values](story-counter-values.md)).

`00265270` is the native reader: while bit 0 of `02098E20` is set and the payload pointer `02098E58`, the `+0x48`
word of the slot-0 actor manager at `02098E10` stored at `0026CAFD`, is not null, it returns that word, else 0 (`00265270`-`0026528B`). 24 call sites in 22 functions read it, among them the
story schedule `00377970` (`003779A4`), the input arbiter (`00253DD1`) and the music table reader (`003EAA78`).

### How scenes move it on

Every script write is a literal, and 268 writes in shipping scripts are reachable:

1. Most are in a zone's director actor, such as `常駐監督` (81 writes), `イベント管理` (31) or `EventDirector` (25),
   most often in its `main` function.
2. 125 lie inside the branch of a test of the counter's current value: an `if`, as in `alc_c01` `EventDirector.main`
   writing 3,260 when the counter is below 3,260, or a case of a switch on it (68).
3. The rest are in functions that do not test it, mostly `touch`, `touchon` and named event functions, which their
   callers start.

The first value a shipping script writes is 13 (`naf_a01` `常駐監督.main`) and the last 7,150 (`bhm_d01`
`ボス監督.main`).

### Values only the developer menus set

The developer scripts `evt_t*` write 88 values no shipping script writes, reachable or not, among them 0 and 10. The clan board ladder
that writes 11,000 is in code no path reaches. So a counter outside the shipping values comes from a developer menu, an
edited save or native code.

### Flags and quests

The flag banks the story sets are on [Story flags](story-flags.md), with every id the scripts use on
[Story flag ids](story-flag-ids.md). The quest bits that follow the counter in the payload are on [Quests](quests.md).

## Modding notes

- Writing payload `+0x0` moves the story: every script and native reader sees the new value at its next access.
- A script cannot hold a reference to the counter: no script pushes it with `PUSHP`.
- The menus and map groups the counter unlocks are the story schedule in `mapjumpgroupflagrom.bin`
  ([Story flags](story-flags.md)).

## Related

- [Story counter values](story-counter-values.md) - every value written, by script.
- [Story flags](story-flags.md) - the flag banks and the story schedule.
- [Quests](quests.md) - the quest state.
- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the payload layout.
