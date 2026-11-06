---
title: "Story progress: the main story counter at the start of the save, the script variables that live in the save, and how scenes move the story on"
kind: "system"
category: "Story, events and hunts"
addresses: "0x002625E7, 0x002626A8, 0x0026CAF8, 0x002EF2B0, 0x00265270, 0x02098E58"
---

## What the player sees

- In normal play the story moves forward one scene at a time: the zone scripts start most scenes behind a test of the
  story counter, so a scene that has played is passed over, and towns, people and menus change after it.
- The counter itself keeps no order. Each script write stores its value whatever the counter held, so a script that
  writes an earlier value moves the story back (How scenes move it on, below).
- Loading a save puts every scene, talk and menu back where the story stood.

## How it works

### Script variables

A script names a variable by a descriptor: a class in the top bits and an offset in the low 24 bits. The resolver
picks the base for the class through the jump table at `0x002626A8` (`0x002625EA`-`0x00262603`) and adds the offset
(`0x00262639`-`0x00262641`):

| Class | Base | Set at |
|---:|---|---|
| `0` | the save payload, actor manager `+0x48` (`0x00262605`) | `0x0026CAF8`-`0x0026CAFD` |
| `1` | actor manager `+0x40` (`0x0026260B`) | - |
| `2` | the address the callback at `+0x98` returns (`0x00262611`-`0x00262617`) | - |
| `3` | the script image plus its own `+0x40` word (`0x00262633`-`0x00262636`) | - |
| `4` | actor manager `+0x58` (`0x00262627`) | - |
| `5` | actor manager `+0x60` (`0x0026262D`) | - |

Class 0 is the save payload itself: `0x002EF2B0` returns the active save buffer plus `0x200` (`0x002EF2B4`-`0x002EF2B9`), and
the actor manager keeps that pointer at `+0x48` when it binds the loaded definitions (`0x0026CAF8`-`0x0026CAFD`). So a
class-0 variable at offset *n* is payload byte *n*, read and written on every access with no copy.

### The story counter

The main story counter is the 16-bit word at payload `+0x0`, class 0 offset 0. 513 scripts declare it alone and 193
declare a 256-word array that starts at the same byte ([Story counter values](story-counter-values.md)).

`0x00265270` is the native reader: while bit `0x1` of `0x02098E20` is set and the payload pointer `0x02098E58`, the
`+0x48` pointer of the slot-0 actor manager at `0x02098E10` stored at `0x0026CAFD`, is not null, it returns the word it
points at, zero-extended, else 0 (`0x00265270`-`0x0026528B`). 24 call sites in 22 functions read it, among them the
story schedule `0x00377970` (`0x003779A4`), the input arbiter (`0x00253DD1`) and the music table reader (`0x003EAA78`).

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

The order comes from those tests, not from the store. `POPV` (`0x00267E60`) pops the value and stores it through
`0x0026D530` (`0x00267F37`), whose signed 16-bit arm clamps it, `w = v < -32767 ? -32767 : v > 32768 ? 32768 : v`
(-32,767 to 32,768, `0x0026D5C7`-`0x0026D5DF`; 32,768 is stored as the word `0x8000`), and writes the word without
reading the old one (`0x0026D5C4`-`0x0026D5E3`). A write of a value below the counter's lowers it, and a write in item
3 runs whenever its function runs, whatever the counter holds.

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
