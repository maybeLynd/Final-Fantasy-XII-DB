---
title: "Effect file loading: the battle effect slots, the loaded-file queue, filing, sharing and releasing, and the battle effect program's state"
kind: "system"
category: "Graphics"
addresses: "0x0024B270, 0x00258D70, 0x002F2D60"
---

## What the player sees

Before an effect can play, its file is read from the archive. Battle effects are read into a small
set of slots, and other effects into a queue of loaded files that are kept while something uses them.

## How it works

### Battle effect files

Kind-1 effects come from 48 slots of `0x38` bytes at `0x02EC32E0`, chained by `0x002FC200` into a free
list `0x02EC3D70`; the active list runs from `0x02EC3D60` to `0x02EC3D68` through `+0x28` and `+0x30`.

`BattleEffectSlot` (`0x38` bytes, offsets from the start of the 0x02EC32E0):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle | bits 0-5 the slot, `0x10000000` the kind |
| `+0x08` | `void*` | context | the type-1 context |
| `+0x10` | `void*` | instance the instance playing it |  |
| `+0x18` | `u32` | request | the file request |
| `+0x1C` | `u32` | size | the file size |
| `+0x20` | `u16` | number | the effect number |
| `+0x23` | `u8` | state | low nibble: 1 wanted, 2 reading, 3 read, 4 freeing, 5 ready, 6 playing |
| `+0x28` | `void*` | next |  |
| `+0x30` | `void*` | previous |  |

`0x002FCF00`, each simulation step from `0x00258D70`, walks the active list:

- state 1 runs `0x002FC860` unless a read already runs (`0x02EC3D7C`, or the loaded-file queue's
  `0x02EBEBE4`). It asks the file size in class `0x0B`, or `0x26` when `0x002DEBB0()` is 0
  (`0x0032E400`); a missing number `0x78`–`0x89` falls back to `0x78`, `0x8A`–`0x99` to `0x8A`, and
  any other to 0. It queues the read (`0x0032E620`) and sets state 2.
- the read's completion `0x002FC830(handle)`: when the handle's low six bits name a slot below 48 whose word
  `+0x00` is the handle, it sets the state's low nibble to 3 (`0x002FC830`-`0x002FC854`).
- the size cache: `0x002FCFF0` (through the stub `0x0036DDB0`) asks the size of all 512 numbers once, keeps them
  at `0x02EC19C0` (8 bytes each) and sets `0x02EC3D7D`; the reset `0x002FC200` clears it (`0x002FC2FF`). While it is
  set, state 1 takes the size from the cache (`0x002FC8AD`), and a missing number falls back to entry 0, not
  to the `0x78` and `0x8A` ranges;
- state 3 builds the context (`0x002FC4A0`);
- state 4 waits until the request is gone (`0x0032E4D0`), then returns the slot to the free list
  (`0x002FC350`) and clears `0x02EC3D7C`;
- state 6 adds 1 to the instance's frame word `+0x3A2`.

`0x002FCCC0(owner, targets, count, handle)` plays a slot in state 5. It sums the 5-bit weights of
the active slots' numbers (`0x02EC19C4`, filled from the 401 bytes at `0x01EEBB10`), ends numbered
requests until `36 − sum` are left (`0x003AFFB0`), and makes an instance (`0x0024B270`): kind 1, the
handle at `+4`, the owner at `+0x08`, the targets at `+0x10` with the count in `+0x372`, the
slot's context at `+0x340`, `+0x3AC` = 1 and the number at `+0x3AE`. It sets state 6 and returns
the handle, or 0.

`0x002EAD00(owner, count, targets, handle)` returns 0 for no targets; otherwise it counts
`0x02CA4EDC` up (`0x0042FCB0`) and plays through `0x002FCCC0`. Its caller `0x00319E40(unit)` gathers the
ids of the unit's targets (list `+0x780`, count `+0x77C`) whose actors exist and plays on them the
handle `0x0030CA50` reads for the unit: entry `+0x695` of the 32 entries of `0x30` bytes at
`0x022C17D0`, its dword `+4`.

- `0x003B1180(targets, n)` selects instances the same way and sets bit `0x2` of their `+0x368`;
  `0x003B1130` clears that bit on every request's instance.
- `0x003B0220(instance)`, from the free-list drain, finds the request holding the instance, moves the
  later entries down and clears the last; `0x003B0770(handle)` does the same by handle after ending the
  instance (`0x0024EE60`). `0x00319E30(handle)` ignores 0 and −1 and tail-jumps to `0x003B0770` otherwise;
  the battle unit code `0x00300E40` and `0x00301140` pass it the unit's `+0x74`.

### Loaded effect files

A second queue at `0x02EBE5E0` holds 32 entries of `0x30` bytes, each an effect file loaded into its
own type-7 context: `+0x00` id, `+0x04` file number, `+0x08` context, `+0x10` instance, `+0x18`
file request, `+0x1C` state, `+0x20` flags, `+0x28` buffer. Only one load runs at a time
(`0x02EBEBE4`). `0x003B25D0`, each simulation step from `0x00258D70`, moves them on:

- state 1 (`0x003B2310`) maps the file number (bit `0x1000` to `0x200 +`, bit `0x2000` to `0x240 +`,
  bit `0x8000` to `0x1FF`, `0xC3` to `0x1FE` when `0x002DEBB0` returns 0), requests the file in class
  `0x0C` (`0x0032E400`, `0x0032E620`) with the completion `0x003B22D0`, which sets state 3, and sets
  state 2;
- state 3 (`0x003B2220`) builds a type-7 context for the id (`0x0024B3A0`), parses the buffer
  (`0x003EDAD0`), copies the high nibble of the first `0x600` record's `+0x16` into the context's
  byte `+2`, and sets state 5;
- state 4 waits until the request is gone (`0x0032E4D0`), then removes the entry and closes the gap.
  `0x003B21E0` clears an entry's id and state when its request is already gone.

`0x003B2830(id, n)`, for `n` of 1 to 10, calls `0x0024FE70(instance, n)` for the entry's instance and
puts `n` in the low nibble of its word `+0x378`. `0x003B27A0(id, n)`, for `n` of 0 to 10, makes the
instance current and passes its `+0x130` block to `0x003339C0` with `n`. `0x003B1560(flag)` clears bit 0
of `+0x20` in every entry when `flag` is 0, and otherwise passes each entry with the bit to
`0x003B18E0`; no code calls it.

### Filing, sharing and releasing a loaded file

`0x003B1A80(file, tag)` files a load with arena 8 selected. It takes the first entry whose id is 0,
returning 0 when all 32 are taken, and gives it the id `0x70000000 | (serial & 0xFFFF) << 12 | (tag &
0x3F) << 6`, the serial counting up at `0x02EBEBE0`. It stores the file number at `+0x04` and clears
the context, the state, the buffer and flag bits 0 and 1. When another entry with the same file is in
state 5 or 6, the new entry takes that entry's context and starts in state 5;
otherwise `0x003B2310` starts the read, and a refused read clears the entry and returns 0.

`0x003B1BA0(owner, targets, count, id, n)` plays an entry. With `n` 0 it needs state 5: it makes a
kind-7 instance on the entry's context (`0x0024B270`), records it at `+0x10`, sets state 6 and copies
flag bit 1 into the instance's hold bit `0x40` of `+0x368`. With `n` non-zero it needs state 5 or
later and only passes `n` to `0x0024FE70` for the existing instance, putting `n` in the low nibble of
`+0x378`. `0x003B2470(id)` returns an entry's instance.

`0x003B18E0(id)` releases one entry by its state, with arena 8 selected:

| State | Release |
|---:|---|
| 1 | the id and state are cleared and the entry removed |
| 2 | the read is cancelled (`0x0032E590`) and the entry goes to state 4 while the request is still queued (`0x0032E4D0`) or `0x0032E520(1)` holds; otherwise as state 3 |
| 3 | `0x003B21E0` clears the entry, the load-running flag `0x02EBEBE4` drops, and the entry is removed |
| 5 | the context is freed (`0x0024F410`) unless another entry for the file in state 5 or 6 holds it (`0x003B2710`); then as state 1 |
| 6 | the instance goes to the free list and the entry to state 7 |
| 4, 7 | nothing |

A removed entry closes the gap and the last entry's id `0x02EBEBB0` is cleared. `0x003B1710(spare)`
applies the same release to every entry, skipping those with flag bit 0 when `spare` is non-zero,
and ends a removed entry's instance (`0x0024EE60`). `0x003B15C0(instance)`, from the free-list drain,
removes the entry whose instance is freed, freeing its context only when no other entry for the
same file in state 5 or 6 has one.

Flag bit 0 keeps a file across an area change. `effectkeepmapjump(slot, b)` (`0x02C5`, `0x0036E9B0`)
writes it through `0x003B2750(id, b)`, and the flag is read by `0x003B24C0(id)`; both accept only an id
whose top nibble is 7. The ordinary area unload runs only `0x0024E910`, whose `0x003B26D0` spares kept
files. When `0x022CB726` is set, as after the title-return reset `0x003601D0`, the unload first runs
`0x0036DF30`, which calls `0x003B1710(0)` and releases every file.

## State

### Placing the target actor

Opcodes `0x39` and `0x3A` of the battle effect program `0x003B8670` (index bytes `0x003B994C`, offsets `0x003B9854`) move
the current instance's slot-0 target actor (`0x003A6D90(0)`, `0x003588B0`). The first of them in an instance runs
`0x0024B6F0`, which, when the target exists, saves the actor's position, facing and two more values at
`0x020921A0`-`0x020921BC` and sets the instance's `+0x368` bit `0x100`. When the instance's players are torn down, `0x0024C870` puts them back
(`0x003A73D7`).

- `0x39` stores the operand's floats `+0x04`, `+0x08` and `+0x0C` times 0.01 (`0x008F30E4`) as the position; a first
  use also sets the facing to 0 (`0x003B93FF`-`0x003B944A`).
- `0x3A` stores operand `+0x08` in degrees as radians, `x 2 x π / 360`; a first use also sets the position to 0
  (`0x003B9466`-`0x003B94A4`).

Each then calls `0x0024F9B0`, which, while bit `0x100` is set and the target exists, sets `0x020921B0` to 1, calls
`0x0026A430(actor, 0)`, places the actor at the position (`0x0026AF80`) and turns it to the facing (`0x0026B5A0`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x020925A0` | `f32` | 0 (zero-filled tail) | the x the target actor is placed at | `0x003B8670`: opcode `0x39` (`0x003B9428`), a first opcode `0x3A`, 0 (`0x003B947C`) | `0x0024F9B0` (`0x0024FA10`) |
| `0x020925A4` | `f32` | 0 (zero-filled tail) | its y | `0x003B8670`: opcode `0x39` (`0x003B9439`), a first opcode `0x3A`, 0 (`0x003B947C`) | `0x0024F9B0` (`0x0024FA08`) |
| `0x020925A8` | `f32` | 0 (zero-filled tail) | its z | `0x003B8670`: opcode `0x39` (`0x003B944A`), a first opcode `0x3A`, 0 (`0x003B9487`) | `0x0024F9B0` (`0x0024F9FD`) |
| `0x020925B4` | `f32` | 0 (zero-filled tail) | its facing in radians | `0x003B8670`: opcode `0x3A` (`0x003B94A4`), a first opcode `0x39`, 0 (`0x003B9415`) | `0x0024F9B0` (`0x0024FA1D`) |

### The effect program's light and flag byte

Opcode `0x0B` files a light through `0x003B81A0(1)` (`0x003B973C`) and opcode `0x0A` releases it (`0x003B96AD`-`0x003B96CF`).
When it holds a light, `0x003B81A0` first releases it (`0x003ABCA0`) and clears bits `0x08` and `0x10` of the light
mask `0x02B3F501` (`0x003ACA90`). With 1 it then files a request with bytes `06 FF 00 01`, `+0x04` 1, `+0x07` bit 0 and
(1.0, 1.0, 1.0, 1.0) at `+0x10` (`0x003AB960`, `0x003B81EB`-`0x003B821E`), and sets the two mask bits again (`0x003ACA80`).
The pool and the request are on [Character lighting and shadows](character-lighting-and-shadows.md).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B40538` | `u32` | 0 (zero-filled tail) | the handle of that light, 0 when none; `0x0024D9C0` also releases it through `0x003B81A0(0)` (`0x0024D9DA`) | `0x003B81A0`: 0 (`0x003B81CE`), the handle (`0x003B8228`); `0x003B8670`, 0 (`0x003B96CF`) | `0x003B81A0` (`0x003B81BA`); `0x003B8670` (`0x003B96AD`) |
| `0x020968C8` | `u8` | 0 (zero-filled tail) | flags of the block `0x00259250` resets: each reset clears bits 1 and 3 and sets bits 0 and 2, keeping the rest. No instruction sets bit 4, which opcode `0x03` tests before it sets the target slot's bit in the current instance's `+0x0C` while `+0x378` bit `0x200` is set (`0x003B8814`-`0x003B8937`), so that bit is never set there | `0x00259250` (`0x002592DA`) | `0x00259250` (`0x00259259`); `0x003B8670` (`0x003B891F`) |

No other instruction reaches these six globals: no other RIP-relative, image-base-relative or 32-bit offset reference
names them. The addresses taken in the block that holds `0x020968C8` (`0x02096810` and `0x02096820` by `0x0024C060`,
`0x02096810` by `0x0024FCF0`, `0x02096840` by `0x002F2D60`) reach at most 16 bytes past each, and the one taken near
`0x02B40538`, `0x02B40508` by `0x003B4B60`, reaches `+0x02` and `+0x04` only (`0x003B54C0`).

## Related

- [Effect element runtime](effect-element-runtime.md): instances, emitters, the update and timeline tracks.
- [Effect drawing](effect-drawing.md): the display layers and the draw list.
- [Effect anchors and targets](effect-anchors-and-targets.md): anchor queries and target slots.
- [Effects on actors and scripts](effects-on-actors-and-scripts.md): numbered effects on actors and script effect slots.
- [Effect files](effect-files-efx-efb.md): the chunk streams the records come from.
- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md):
  contexts, instances and their teardown.
- [Character lighting and shadows](character-lighting-and-shadows.md): the light pool the effect program files into.
