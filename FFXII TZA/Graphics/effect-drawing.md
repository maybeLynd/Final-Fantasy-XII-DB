---
title: "Effect drawing: the six display layers, drawing a group and an element, soft particles and the draw list"
kind: "system"
category: "Graphics"
addresses: "0x020910F0, 0x002F4020, 0x00258EE0, 0x00259030, 0x0024D370, 0x0024D4E0, 0x00441970, 0x02AEE910, 0x02F8F2F8, 0x02F8F2C6, 0x003A3740, 0x003A3A00, 0x0024D540"
---

## What the player sees

Effects are drawn in six passes at fixed points of the frame, so some effects sit behind characters
and others in front of the menu.

## How it works

### The six display layers

`MainLoop_Draw` (`0x0022B0B0`) asks for effects six times through `0x00258EE0(layer)`, each request
bracketed by the engine's marker text. The draw-side order inside a layer comes from the grouped
pass `0x00259030`.

| Layer | Marker | Work |
|---:|---|---|
| 1 | `display VFX [layer : first]` | grouped pass, then `0x0024C640` |
| 2 | `display VFX [layer : after BG]` | the same |
| 3 | `display VFX [layer : TsEffMan_Layer_AfterOBJ]` | no grouped pass: `0x0039D570(0)`, `0x0039D3F0`, a pair of calls chosen on `0x02F8F310` bit 2, then `0x003A3990` |
| 4 | `display VFX [layer : in EFF]` | `0x0039CFF0(0, 0x3C00)`, `0x0036F550` unless `0x00181DD0()` is non-zero, grouped pass, `0x0039CFF0(0, 0x3700)`, `0x0024C640` |
| 5 | `display VFX [layer : after EFF & MENU]` | `0x0036F9F0` unless `0x00181DD0()` is non-zero, then the grouped pass |
| 6 | the same text as 5 | grouped pass |

Every layer request runs between `0x00862C10(0, layer)` and `0x00862C30`. The opening call
(`0x001B2530` on the object `[0x01F7F4D8]`) binds three textures of the render manager to the texture ids
`0xE00`, `0xDFF` and 0, choosing the second set for a layer above 5, stores the pass id at
`+0x90` and the layer without bit `0x10` at `+0x94`, and files a `GiBeginScene` (`0x001FBD80(2)`); the closing call
files a `GiEndScene` (`0x001B2600`).

`0x00862C40`, `0x00862C00` and `0x00862BF0` return those two words; the drain uses them to close and
reopen the bracket around the post-processing block, with `0x10` added to the layer (`0x003A3740`).

`0x00259030(layer)` selects arena 8, calls `0x0024D370(layer, group)` for groups 2, 3, 5, 6, 9, 1, 7 and
4, then drains the draw list (`0x003A3740`) (`0x00259036`–`0x002590C0`). A group is an instance kind.

### Drawing one group

`0x0024D370(layer, group)` takes the list `0x020910F0[group]` and asks the group gate `0x0024D4E0`
(`0x0024D382`–`0x0024D3AF`). The gate refuses group 8; groups 1–4 and 7 need bit `group − 1` in the AND
of `0x02092162`, `0x02092164` and `0x02092166`; group 2 also needs `0x02F8F29E` bit 0 clear and group 5
`0x02EBEF68` bit 0 clear (`0x0024D4E0`–`0x0024D538`).

For each instance the group draw publishes the group at `0x02092700` and skips the instance unless
its `+0x3A8` equals `0x00181DD0()`, the high nibble of its word `+0x378` equals the layer, and the
per-instance gate `0x0024D770(instance, 1)` passes (`0x0024D3C0`–`0x0024D3FC`). It makes the instance
current and walks its emitters through `0x003A72F0` → `0x003A8D80`, which calls `0x00441970` for each
(`0x0024D405`, `0x0024D499`, `0x003A8D84`–`0x003A8DAB`). So an effect's layer is authored in its
instance.

`0x00441970(emitter)` returns when the emitter has no elements. Unless the instance's flag byte
`+0x36A` has bit 0, only emitters whose definition type is `0x40`, `0x41`, `0xA1`, `0xA2`, `0xA5`
or `0xD0` are drawn (`0x0044198E`–`0x004419CE`; the table is
[`effect-element-runtime-effect-kind-441970.tsv`](effect-element-runtime-effect-kind-441970.tsv)). It sets the pass nibble `0x02AEE910`: definition
byte `+0x4C` when `+0x4A` is `0x40` or more, else 8 (`0x004419F5`–`0x00441A0E`).

That rule has one exception. While bit `0x400` of `0x020926E4` is set and the current instance is of kind 3, the
nibble is `0x020926F8` + 8 (`0x004419D0`-`0x004419F3`). Opcode `0x3E` of the battle effect program `0x003B8670` sets the bit
and stores its operand byte `+4` in `0x020926F8` (`0x003B9797`-`0x003B97A7`). Opcode `0x3F` clears the bit
(`0x003B97B2`-`0x003B97B7`), and so does the effect teardown `0x0024E910`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x020926F8` | `u8` | 0 (zero-filled tail) | the pass nibble less 8 for kind-3 instances while `0x020926E4` bit `0x400` is set | `0x003B8670`: opcode `0x3E`, its operand byte `+4` (`0x003B97A7`); `0x0024C970`, 0 (its `0x1670`-byte clear from `0x020910A0`, `0x0024C983`) | `0x00441970` (`0x004419E4`) |

It then calls `0x002F4020(element, emitter)` for each element, forward from the head, or backward from
the tail when the emitter record's byte `+0x2C4` has bits 0–1 set (`0x00441A15`–`0x00441A82`).

### Instance flags at draw time

Before the emitter walk, `0x0024D370` reads the instance's flag byte `+0x36A`. With bit 0 set it
records the instance's target `+0x380`, when there is one, for texture id `0x3300` at 256
× 224 (`0x002D7D90`), then calls `0x003AA2E0(0)` and skips the instance when that returns 0. With bit 1
set it files a `GiZNormalOnOff` command with 1 (`0x0039D410`, through `0x00864E00`) and sets bit 0 of
`0x02F8F310`, which makes the drain open with `GiTransNz` instead of `GiTrans` (`0x003A3740`).

### Widescreen and mask-border flags

`0x0024E4B0` classifies the current instance's context while the pass id `+0x90` of `[0x01F7F4D8]` is
0 (`0x00862C40`), by its kind byte and its id word `+4`:

| Context | Ids | Bits |
|---|---|---|
| kind 1 | `0x80` | `0x10` |
| kind 1 | `0x89` | `0x8` |
| kind 1 | `0xD5`–`0xD7`, `0xE2`, `0x17A`, `0x182` | `0x2` |
| kind 7 | `0xB0`, `0x2C0`–`0x373` | `0x1` |
| kind 7 | `0x240`–`0x2BF` | `0x1` for 25 listed ids, `0x4` for `0x289`, `0x3` for `0x28B` and `0x2A3`, `0x2` for the rest |

Any other context gets 0. For each instance it draws, `0x0024D370` calls `0x00183090(1)` after the
emitter walk when the flags have bit `0x2`, which sets `0x01F7F4F8`, one of the flags the mask-border
wrapper `0x0017F6B0` tests; the frame state machine `0x0022A580` clears it each frame (`0x00183090(0)`). `0x0024E640` turns the flags into the widescreen mode the element draws use: 1 for
bit `0x1` or a kind-7 id from `0x200` to `0x23F`, else 2, 3 or 4 for bit `0x4`, `0x8` or `0x10`, else
0.

`0x00184740`, from the frame `0x0022A770`, reads the current instance through `0x0024DE30(&kind, &id,
&frame)`, which returns its bytes `+0x3AC`, `+0x3AE` and `+0x3A2` + 1. While a kind-1 effect
`0x17A` is current and the latch `0x01F7F540` is clear, it sets both; any other current effect
clears `0x01F7F500`, another flag `0x0017F6B0` tests. `0x00182D30` clears the latch.

### Soft particles

`0x0024D140(&factor)` answers whether the current context draws soft particles, for the `GiSprite`
builder `0x008647C0` (`+0xD0` and `+0xD4` of the command) and the VU program packet `0x001DB840`
(`+0x630` and `+0x634`). It answers no with a factor of 0.1 unless the pass id is 0 and the layer
`+0x94` is 4, or 3 or 4 when `0x0017FE10()` (the byte `0x01DF08F4`) is non-zero. Otherwise the kind
picks a table from `softparticle_*.csv` ([standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md)):

| Kind | Key | Table |
|---|---|---|
| 1 | id word `+4` | `0x02F95B40` (`magic`) |
| 2 | the instance's word `+4` against the map's rows | `0x02F8F340` (`softparticle_bg.csv`) |
| 3 | `0x003B33D0(id)` | `0x02F96B40` (`chara`) |
| 5, 6, 9 | the effect number `0x003B0940(handle)` | `0x02F95340` (`common`) |
| 7 | id word `+4` | `0x02F96340` (`event`) |

Kinds 4 and 8 answer no. A table entry answers yes when its byte 0 is set, with the factor its
word `+2` / 100; a bound of 512 entries applies. For kind 2 the answer and factor are the matched
row's bytes `+1` and `+2`.

`0x0024F790`, run by the EFB loader `0x0026FB90`, picks the map's rows: it takes the text after the
backslash of the map-art context's name `+0x241` (`0x00180370`), finds the matching 16-byte record in `0x02F93340`, and
stores its first row in `0x01E0C290` and the row count in `0x02092710` (up to the next record, or to
`0x02092714` for the last). No match stores −1.

### Drawing one element

`0x002F4020` returns when the type byte is outside `[0x022BE7D8]`..`[0x01EEBAE0]`, or when `+0x224` is set
while the cadence test returns 0 (`0x002F402A`–`0x002F405B`). With definition byte `+0x4D` non-zero, a
counter in word `+2` and the cadence test set a skip bit in byte `+1` bit 0, and a set bit skips
the draw (`0x002F4070`–`0x002F40E6`). It stores definition byte `+0x75` at `0x02AEF41C`, calls the type's
draw method, and clears `0x02AEF41C` again (`0x002F40EC`–`0x002F4124`, `0x002F4369`).

The debug console's "Particle Draw Type Range" entries set the bounds through `0x002F1CD0(low,
high)`; they ship as 0 and `0xD1`, so every type draws.

### The draw list

Blended primitives do not draw at once. An emitter appends a `0x28`-byte entry to the list at
`[0x02F8F2F8]`, counted by the word `0x02F8F2C6`; the point emitter `0x0039D970`, for one, writes the
projected depth word as the sort key `+8` and ORs the pass nibble into bits 28–31
(`0x0039D986`–`0x0039DA05`). `0x003A3670` allocates the list, `0x190000` bytes, which is 40,960 entries.

`0x003A3740` drains it. It returns for an empty list, sorts the entries by `+8` (`0x003A3A50`), and for
each entry calls the function at `+0x10` with `+0x00`; without one, it submits the command at
`+0x18` through `0x0020E630(command, 2)`, or with flag bit `0x4` defers it to `0x02AEF420` for layer 3's
`0x003A3990` (`0x003A3744`–`0x003A3908`). It empties the list and keeps the last and peak counts
(`0x003A3929`–`0x003A3973`).

`0x0024D540`, the frame's draw setup, drains once more and then rewinds: `0x003A3A00` resets the packet
cursor `0x02F8F2D0` to the arena base `0x02F8F308`, sets its end `0x02F8F2D8`, and zeroes the count
(`0x0024D556`, `0x0024D55B`, `0x003A3A00`–`0x003A3A42`).

Three other producers copy data into the packet arena behind `0x02F8F2D0` and file an entry for it;
each does nothing when the arena lacks room. `0x003A2C80(callback, data, size, pass, key)`, called
from `0x004781A0`, stores the copy at `+0x00` and the callback at `+0x10`, so the drain calls it with
the copy.

`0x003A3010(data, size, key)` and `0x003A31A0`, called from effect types (`0x0044D4A0`,
`0x00453150`, `0x00460BC0`, `0x00522300`; `0x0045BAE0`), build a GS packet around the data, with the blend
word of the current mode, and file it at `+0x00` with no callback and no command. The drain does
nothing with such an entry: it calls a callback when there is one and otherwise submits only when
`+0x00` is null (`0x003A38BA`–`0x003A38CD`).

## Layouts

Draw-list entry (`0x28`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | callback argument |  |
| `+0x08` | `u32` | sort key; bits 28-31 pass nibble |  |
| `+0x10` | `void*` | callback |  |
| `+0x18` | `void*` | command |  |
| `+0x20` | `u32` | flags |  |

## Operations

Per frame, six layer requests and up to 40 group draws, each walking the drawn
emitters of one group; each blended primitive costs one draw-list entry, and the list holds 40,960.

## State

The pass nibble `0x02AEE910`, the blend pair `0x02AEE900` / `0x02AEE908`, the draw list `0x02F8F2F8` with its
count `0x02F8F2C6`, and the packet cursor `0x02F8F2D0` / `0x02F8F2D8` over `0x02F8F308`.

When `0x003A3740` empties the draw list it stores the count it drained in `0x02F8F2CC` and keeps the larger of that count
and `0x02F8F2CE` in `0x02F8F2CE` (`0x003A3929`-`0x003A3973`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02F8F2CE` | `u16` | 0 (zero-filled tail) | the largest number of entries the draw list has held when drained | `0x003A3740` (`0x003A3973`); `0x003A3670`, 0 (its 4-byte clear of `0x02F8F2CC`, `0x003A36E6`) | `0x003A3740` (`0x003A395E`) |

## Modding notes

- An effect's display layer is the high nibble of its instance word `+0x378`; its group is the
  instance kind. Group 8 is never drawn.
- More than 40,960 blended primitives in one frame overrun the draw list; nothing checks the count.

## Related

- [Effect element runtime](effect-element-runtime.md): instances, emitters, the update and timeline tracks.
- [Effect anchors and targets](effect-anchors-and-targets.md): anchor queries and target slots.
- [Effect file loading](effect-file-loading.md): battle effect slots and the loaded-file queue.
- [Effects on actors and scripts](effects-on-actors-and-scripts.md): numbered effects on actors and script effect slots.
- [Effect element types](effect-element-types.md): what each type does in its methods.
- [Frame update order](../Engine-Core/frame-update-order.md): where the update pass runs.
