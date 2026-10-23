---
title: "Menu effects: the 64-record registry that menu screens use to spawn, place and remove effects by id"
kind: "system"
category: "Graphics"
addresses: "0x02EBDBC0, 0x02EBE5C0, 0x003B29B0, 0x003B2B40, 0x003B28F0, 0x003B2D80, 0x003B2BC0, 0x003B2AA0, 0x003B2930, 0x003B2CA0, 0x003B2CE0, 0x003B2F50, 0x0024C460, 0x0024C550, 0x0024F610, 0x0024B270, 0x0024FCF0, 0x0039B620, 0x0039B550"
---

## What the player sees

Sparkles and flashes on menu screens: the effect when a license is obtained and the neighbouring squares light up on
the [License Board](../Menus-And-HUD/license-board-screen.md), and the effects on the statues of the Sky Pirate's Den in the
[Clan Primer](../Menus-And-HUD/clan-primer.md). They appear and disappear as the player moves through the screen.

## How it works

### Loading the menu context

`0x003B29B0(file)` clears all 64 records and the id counter `0x02EBE5C0`, frees every effect instance and context of type 4
(`0x0024C460(4)`, `0x0024C550(4)`), builds an `0x890`-byte context template with type byte 4 (`0x0024B3A0`) and parses the
screen's effect file into it (`0x003EDAD0`). `0x0024C460(type)` frees each instance on the list `0x020910F0[type]`;
`0x0024C550(type)` frees each context on `0x020910A0[type]` and then the instances. Type 4 is the menus' own: the other
context builds use 1, 2, 3, 5 and 7 ([Effect files](effect-files-efx-efb.md)).

Two lighter resets exist. `0x003B2B40` does the same clearing without loading a file, and `0x003B28F0` frees the type-4
instances and zeroes each record's id and instance without touching the counter.

### Spawning

`0x003B2D80(x, y, z, kind)`:

1. It increments `0x02EBE5C0`, so even a spawn that then fails uses up an id.
2. It finds the loaded type-4 context (`0x0024F610`); without one it returns 0. Otherwise it makes the id
   `(counter & 0x0FFFFFFF) | 0x40000000`.
3. It creates an instance (`0x0024B270`) from an `0x3B0`-byte request with word `0x104` and the id.
4. It takes a free record (`0x003B2BC0`). When all 64 are in use, `0x003B2BC0` frees the oldest record's instance
   (`0x0024EE60`), shifts the table down one record and returns the last one, so a spawn never fails for lack of room.
5. It stores the id, the instance and the four arguments in the record, and sets up the instance: `+0x320`-`+0x328` = 1.0,
   `+0x330` = `0x80808080`, `+0x340` = the context, `+0x370` = `0x102`, `+0x373` = `kind`, `+0x39C` = 1.0, and flag bits
   in `+0x368`, `+0x36A` and `+0x378`. A kind of `0x13` adds 2.45 to the instance's `+0x304`.
6. It returns the id.

No registry routine reads `+0x10`-`+0x1C` back, and callers only ever hold ids.

### Removing

- `0x003B2AA0(id)` finds the record, frees its instance (`0x0024EE60`), moves the later records down and clears the last
  record's id.
- `0x003B2930(instance)` does the same compaction for the record holding that instance without freeing it. The effect
  system calls it from `0x0024B580` and `0x0024B9B0` when it frees an instance itself.

### Setting a depth offset

`0x003B2F50(id, value)` writes `value` to the instance's `+0x338`. `0x0024FCF0` publishes `+0x338` to `0x02AEE7F4` when it
makes the instance current; `0x0039B620(n)` stores `n + [0x02AEE7F4]` at `0x02AEE7F0`; and `0x0039B550` adds `0x02AEE7F0`,
converted to float, to the third component of the translation of every matrix it installs, as does `0x0039AFA0`. The
value is a depth offset for the instance's elements. For other instances the effect build `0x0026F470` copies it from
the effect file.

### Queries

- `0x003B2CE0(id)` returns 0 when the id has no record or instance, and 1 when bit `0x100` of the instance's `+0x378` is
  clear. Otherwise it returns a code from the instance's byte `+0x370`: 0 gives 2; 1 and 2 give 3; 3 gives 5; 4 to 6 give
  4; any other value 1. A fresh spawn (`+0x370` = 2) answers 3.
- `0x003B2CA0(instance)` returns the record holding an instance, or 0. `0x0024D770`, `0x003A4290` and `0x003A56F0` call it.

### Who drives it

| Screen | Load or reset | Spawn, remove, query |
|---|---|---|
| License Board: the chooser window `0x00558FB0` and chooser `0x00557DB0` | `0x003B29B0`, `0x003B2B40` | `0x00557DB0`, `0x005588C0`, `0x00558960` |
| License Board: the board screen `0x00561390` and view `0x0055CD40` | `0x003B29B0`, `0x003B2B40`; `0x003B28F0` from `0x0055CD40` and `0x0055F3E0` | `0x0055CD40`, `0x0055B560`, `0x0055F010` |
| Clan Primer, Sky Pirate's Den: `0x00572E10` and `0x00573980` | `0x003B29B0`; `0x003B28F0`, `0x003B2B40` | `0x00572920`, `0x005734C0`, `0x00573690` |

The License Board keeps the id of a square's effect in the square's `+0x2C`, and `0x0055F010` polls `0x003B2CE0` while it
runs the square transitions ([License Board screen](../Menus-And-HUD/license-board-screen.md)). `0x00557DB0` also polls it.

In the Sky Pirate's Den, `0x00572920` goes through the thirty descriptors and, for each one whose award bit is set
(`0x00576E10`), spawns one effect at the layout entry's words `+2` and `+4` with the kind byte `+0x16`, then calls
`0x003B2F50(id, (0xFF - entry byte +1) × 10000)` ([Achievements](../Steam-And-Achievements/achievements.md)).
`0x005734C0` and `0x00573690` refresh them: a stored id that is not -1 is removed first, then a new one is spawned and set.

## Layouts

Registry record, `0x02EBDBC0` + n × `0x28`, 64 records:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | id | 0 = free; `0x40000000` \| counter |
| `+0x08` | `void*` | instance | the effect instance |
| `+0x10` | `u32` | x | the spawn arguments, stored only |
| `+0x14` | `u32` | y |  |
| `+0x18` | `u32` | z |  |
| `+0x1C` | `u32` | kind |  |
| `+0x20` | `u8` | flags | bit 0 cleared on spawn |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02EBE5C0` | `u32` | counter | the last id number handed out |

## State

- `0x02EBDBC0`-`0x02EBE5BF`: the 64 records, kept packed from the start; the first free record ends every scan.
- `0x02EBE5C0`: the id counter, cleared by `0x003B29B0` and `0x003B2B40`.
- The type-4 context and its instances on the effect lists `0x020910A0[4]` and `0x020910F0[4]`.

## Modding notes

- An id stays valid until its record is removed or evicted; after 64 newer spawns the oldest effect disappears.
- `kind` is stamped into instance `+0x373`; kind `0x13` also starts 2.45 further along at `+0x304`.
- A higher `entry byte +1` in the Sky Pirate's Den layout gives a smaller depth offset.

## Related

- [License Board screen](../Menus-And-HUD/license-board-screen.md): the screen that spawns the license effects.
- [Clan Primer](../Menus-And-HUD/clan-primer.md): the Sky Pirate's Den page.
- [Achievements](../Steam-And-Achievements/achievements.md): the award bits and statues.
- [Effect files](effect-files-efx-efb.md): the effect containers and context types.
- [Effect element runtime](effect-element-runtime.md): how instances are updated.
- [Effect drawing](effect-drawing.md): how they are drawn.
