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

`0x003B29B0(file)` clears all 64 records and the id counter `0x02EBE5C0`, frees every effect instance and context of type
4 (`0x0024C460(4)`, `0x0024C550(4)`), builds an `0x890`-byte context template with type byte 4 (`0x0024B3A0`) and parses the
screen's effect file into it (`0x003EDAD0`), with the file's `+0x0C` as the size (`0x003B2A6F`).

Clearing a record zeroes its id `+0x00`, instance `+0x08` and kind `+0x1C` and clears bit `0x1` of its flags `+0x20`;
`x`, `y` and `z` are kept (`0x003B29E0`–`0x003B2A20`). The whole body runs with arena 2 selected, taken twice and popped
twice (`0x003B29C8`, `0x003B2A44`, `0x003B2A7A`, `0x003B2A8F`). The context's word `+0x24` is 0, and the parse follows the
build without testing it: `0x0024B3A0` answers null only for a null template, and it makes the new context current
itself (`0x0024B477`).

`0x0024C460(type)` frees each instance on the list `0x020910F0[type]`; `0x0024C550(type)` first clears the type's owner
table for types 1 and 5 to 9 and goes straight on for types 2 to 4 and any type outside 1 to 9
(`0x0024C569`–`0x0024C594`), then frees each context on `0x020910A0[type]` and then the instances. Type 4 is the menus' own:
the other context builds use 1, 2, 3, 5 and 7 ([Effect files](effect-files-efx-efb.md)).

`0x0024C460(type)` treats each instance on `0x020910F0[type]` the way `0x0024EEE0` does. It makes the instance current
(`0x02F97348`), points `0x02EBEF98`, `0x02EBEFB0` and `0x02EBEF88` at its `+0x120`, `+0x130` and `+0x1B8` for the releases of
its path objects, players and emitters (`0x003A81E0`, `0x003A72E0`, `0x003A8D70`), queues its render target `+0x380` at
`0x02091950` (released at once by `0x00182CA0` when 256 are queued) and frees its block (`0x003697F0`)
(`0x0024C4A0`-`0x0024C51B`). It then clears the list head (`0x0024C531`).

`0x0024C460` does not call `0x003B2930`, so it leaves the registry records as they are; `0x003B29B0`, `0x003B2B40` and
`0x003B28F0` clear the records themselves.

Two lighter resets exist. `0x003B2B40` does the same clearing without loading a file, and `0x003B28F0` frees the type-4
instances and zeroes each record's id and instance without touching the counter.

### Spawning

`0x003B2D80(x, y, z, kind)` works under arena 2 (`0x0036C1D0(2, 10)` at `0x003B2DBF`, `0x0036C140` on both exits at
`0x003B2E4B` and `0x003B2F40`):

1. It increments `0x02EBE5C0`, so even a spawn that then fails uses up an id.
2. It makes the id `(counter & 0x0FFFFFFF) | 0x40000000` (`0x003B2DF6`-`0x003B2E04`) and then looks for the loaded
   type-4 context with `0x0024F610`, keyed by type byte 4 and word 0 (`0x003B2DFF`, `0x003B2E0D`), the key `0x003B29B0`
   builds the context from (`0x003B2A60`, `0x003B2A65`). Without one it returns 0 (`0x003B2E1D`).
3. It creates an instance (`0x0024B270`) from an `0x3B0`-byte request with word `0x104` and the id. The request is
   zeroed first (`0x00861EC0` at `0x003B2DD4`), and a null instance returns 0 (`0x003B2E32`).
4. It takes a free record (`0x003B2BC0`). When all 64 are in use, `0x003B2BC0` frees the oldest record's instance
   (`0x0024EE60`), shifts the table down one record and returns the last one, `0x02EBE598` (`0x003B2C92`), so a spawn never
   fails for lack of room. The arm that frees the instance when no record comes back (`0x003B2E3E`-`0x003B2E46`) is
   never taken.
5. It stores the id, the instance and the four arguments in the record and clears bit `0x1` of its flags `+0x20`
   (`0x003B2E7E`-`0x003B2E9B`). A kind of `0x13` adds 2.45 to the instance's `+0x304` (`0x003B2E9E`-`0x003B2EBA`).
6. It sets up the instance: `+0x320`-`+0x328` = 1.0, `+0x330` = `0x80808080`, `+0x340` = the context, `+0x370` =
   `0x102`, `+0x373` = `kind`, `+0x39C` = 1.0, and flag bits in `+0x368`, `+0x36A` and `+0x378`: bit `0x1`, bit
   `0x800` and bit `0x100` (`0x003B2EC2`-`0x003B2F36`).
7. The word store `0x102` puts 2 in byte `+0x370` and 1 in byte `+0x371`, and `+0x373` takes the low byte of
   `kind`. It also sets the bytes `+0x2D0`, `+0x2E0` and `+0x2F0` to `0xFF` (`0x003B2F1A`-`0x003B2F2F`).
8. It returns the id (`0x003B2F45`).

No registry routine reads `+0x10`-`+0x1C` back, and callers only ever hold ids.

`0x0024F610(key)` answers 0 for a null key. Otherwise it walks the contexts on `0x020910A0[key byte +0]` through
`+0x08` and returns the first whose word `+4` equals the key's word `+4`, or 0 (`0x0024F613`-`0x0024F63F`).

### Removing

- `0x003B2AA0(id)` finds the record, frees its instance (`0x0024EE60`), moves the later records down and clears the last
  record's id, `0x02EBE598` (`0x003B2B22`; `0x003B2930` clears it at `0x003B299B`).
- `0x003B2930(instance)` does the same compaction for the record holding that instance without freeing it. The effect
  system calls it from `0x0024B580` and `0x0024B9B0` when it frees an instance itself.

### Setting a depth offset

`0x003B2F50(id, value)` writes `value` to the instance's `+0x338`. `0x0024FCF0` publishes `+0x338` to `0x02AEE7F4` when the
instance is made current; `0x0039B620(n)` stores `n + [0x02AEE7F4]` at `0x02AEE7F0`; and `0x0039B550` adds `0x02AEE7F0`,
converted to float, to the third component of the translation of every matrix it installs, as does `0x0039AFA0`. The
value is a depth offset for the instance's elements. For other instances the effect build `0x0026F470` copies it from
the effect file.

`0x003B2F50` scans the records up to the first free one (`0x003B2F63`) and writes only when a record holds `id` and its
instance is set (`0x003B2F7B`); otherwise it changes nothing. `0x0024FCF0(instance)` publishes nothing for a null
instance (`0x0024FCF3`). It is the tail of `0x0024ED80` (`0x0024EDFF`), which publishes the instance at `0x02F97348`, and
`0x0024D050`, `0x0024D540` and `0x003B8260` call it directly (`0x0024D102`, `0x0024D614`, `0x003B8614`). With `+0x338` it
publishes the instance's other draw state
([effect element runtime](effect-element-runtime.md#making-an-instance-current)).

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

In the Sky Pirate's Den, `0x00572920` goes through the thirty descriptors and records each one whose award bit is set
(`0x00576E10`), attaching the layout entries that match it. It spawns one effect for each entry whose byte `+0` is
`0xFE`, with no award test. It then spawns one for each awarded descriptor's own entry and one for each entry attached
to it, at the entry's words `+2` and `+4` with the kind byte `+0x16`, and calls `0x003B2F50(id, (0xFF - entry byte +1) ×
10000)` after each ([Achievements](../Steam-And-Achievements/achievements.md)).

`0x005734C0` and `0x00573690` refresh them when the selection moves: a stored id that is not -1 is removed first, then
the previously selected group is spawned again with kind `+0x16` and the newly selected group with kind `+0x17`.

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
| `+0x20` | `u8` | flags | bit `0x1` cleared on spawn |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02EBE5C0` | `u32` | counter | the last id number handed out |

## State

- `0x02EBDBC0`-`0x02EBE5BF`: the 64 records, kept packed from the start; the first free record ends every scan except
  that of `0x003B2CE0`, which compares the id of all 64 records (`0x003B2CF3`-`0x003B2D00`). Every record past the first
  free one has id 0, so its answer is the same; an id of 0 finds the first free record, whose null instance
  answers 0 (`0x003B2D14`).
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x0024D540` calls `0x003B3D20`; those functions are documented on [effect drawing](effect-drawing.md).
