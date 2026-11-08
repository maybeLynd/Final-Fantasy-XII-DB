---
title: "Vibration: the pad vibration that scenes and effects play, the request slots and their steps, the Vibration Function setting, and how the levels reach an XInput or Steam pad"
kind: "system"
category: "Controls and input"
addresses: "0x02EC0B80, 0x0035B2F0, 0x0035B580, 0x0035B650, 0x0035AF20, 0x0035AE30, 0x0035FED0, 0x0035F590, 0x0035F690, 0x001E1120, 0x007A2140, 0x0035B1A0"
---

## What the player sees

- Some scenes and effects make the pad vibrate; the Config option Vibration Function turns it off.
- Only a pad that was the last device used vibrates: after a key or mouse press the pad stays still until one of
  its buttons or sticks is used again.
- A vibration that goes on for a long time fades out, stays off for a while, and comes back.
- An Xbox-style pad and a Steam controller vibrate; other pads do not.

A scene's script plays one of the 11 patterns in `common/eventvib.bin` with `vibplay`, and an effect sequence can
start a pattern too. Each frame the game turns every playing pattern into a motor strength, which reaches the pad only
while Vibration Function is on and the pad was the last device used.

## How it works

### The request slots

Vibration requests live in 32 slots of `0x20` bytes at `0x02EC0B80`. `0x0035B270`, run once from `0x0022A0B0`
(`0x0022A429`), chains every slot into the free list `0x02EC0B60`, empties the playing list `0x02EC0B61` (`0xFF`), clears
the eight recorded handles `0x022C8030`, the pattern table `0x02EC0B68` and the pause mask `0x02EC0B40`, and sets the output
switch `0x02EC0B3C` to 1 (`0x0035B2D5`-`0x0035B2DC`). No other instruction writes `0x02EC0B3C`.

A handle is the slot's generation times 256 plus the slot number plus 1 (`0x0035B2F0`). Every function that takes
a handle first compares the generation, so a stale handle does nothing:

- `0x0035B240(handle)` returns the slot's state, or 0 for a stale handle.
- `0x0035B550(handle, strength)` sets the strength.
- `0x0035B1A0(handle)` frees the slot: it unlinks it from the playing list, raises the generation, puts it at the
  head of the free list and clears its state and pattern.

### Starting a vibration

1. `0x0035B2F0(pattern, channel)` takes the head of the free list when its state is 0: state 1, strength 1.0, track 1
   at pair 0 and track 2 at the pair the pattern's first `u16` names, and links it into the playing list.
   - With the free list empty (`0x02EC0B60` is `0xFF`) or its head's state not 0 it takes no slot and returns 0
     (`0x0035B30C`-`0x0035B31D`).
   - Otherwise the slot's next byte becomes the free list's head, the slot goes to the front of the playing list
     `0x02EC0B61`, the pattern pointer goes to `+0x08`, both frame bytes `+0x18` and `+0x19` are zeroed and the channel
     is stored at `+0x1A` (`0x0035B31F`-`0x0035B371`). It returns the handle, generation × 256 + slot + 1.
2. `0x0035B580(handle, mask)` starts a slot in state 1: it keeps the mask and moves to state 2, or straight to state 4
   when the mask shares a bit with the pause mask `0x02EC0B40` (`0x0035B5AB`).
   - The slot is the handle's low byte minus 1 (`0x0035B580`-`0x0035B595`). It stores the mask byte at `+0x1C` and
     returns 1 (`0x0035B5BB`-`0x0035B5C6`); the pause test is a byte test of the mask against the low byte of
     `0x02EC0B40`. A stale handle (word `+2` not `handle >> 8`) or a slot not in state 1 is left as it is and the
     call returns 0 (`0x0035B598`-`0x0035B5A9`).
3. `0x0035B650(index, mask)` does both for pattern `index` of the loaded table on channel 0, when the index is below
   the table's count and one of the eight entries at `0x022C8030` is empty, and records the handle there.
   - It returns when the table pointer `0x02EC0B68` is null, when the `u32` count at the table's `+4` is not above the
     index (unsigned), or when all eight entries hold a handle (`0x0035B663`-`0x0035B6B1`).
   - Otherwise it calls `0x0035B2F0(0x0020E600(table[+8 + 4 × index]), 0)` and stores the returned handle in the first
     empty entry (`0x0035B6B2`-`0x0035B6D1`).
   - It arms the slot inline, the way `0x0035B580` does: when the slot's generation word `+2` equals `handle >> 8`
     and its state `+1` is 1, it stores the mask at `+0x1C` and sets state 2, or 4 when the mask shares a bit
     with `0x02EC0B40` (`0x0035B6C5`-`0x0035B707`).
   - A returned handle of 0 (an empty free list or a busy head slot) leaves the entry 0, and the arming test then
     reads the generation word at `0x202EC0B62`, slot index `0xFFFFFFFF` zero-extended (`0x0035B6C5`-`0x0035B6E1`).

| Starter | What it plays |
|---|---|
| verb `vibplay` `0x23D`, handler `0x0034AC30` | `0x0035B650(pattern, 2)` through `0x00379F20`, unless `0x00267310` answers non-zero for the actor's byte `+0x15` |
| verb `vibstop` `0x23E`, handler `0x0034B0F0` | frees the eight recorded handles (`0x0035B460`) |
| `0x0034B3C0` | answers whether a recorded handle is playing or paused (`0x0035B380`), or frees them when `0x00267310` answers non-zero |
| effect sequence element of kind 3 (`0x004FF2C0`) | `0x005372D0`: on the element's frame, with fewer than four running, `0x0035B2F0(pattern, 0)` and `0x0035B580(handle, 1)`, strength `0x00537410`'s answer over 127 |

Each frame `0x0046E990` and `0x0046EDD0` set the strength of a sequence's running vibrations again from `0x00537410` and
free those that have stopped; `0x0046EE70` frees all of a sequence's vibrations.

### Stepping

`0x0035AF20` turns the time into whole steps; the field frame calls it at `0x0022A955`, `0x0022AC7A` and `0x0022ADDE`, the
menu frame `0x0022B8C0` at `0x0022BAB9`, the capture-backed frame `0x0022BC20` at `0x0022BD0F`, and the two capture states
`0x0022AF50` and `0x0022B000` at `0x0022AF96` and `0x0022B030`:

```python
accumulator 0x022C8050 += 10000 * [0x01DFE0BC]
steps = accumulator / 10000, run in one pass
accumulator = accumulator % 10000
```

With less than 10,000 in the accumulator it returns before any pass, and the levels keep their last values
(`0x0035AF53`-`0x0035AF5A`). The pass clears the levels `0x02EC0B50` (two channels of two `i32`, track 1 then track 2)
once (`0x0035AFAB`), then steps each playing slot whose mask shares no bit with `0x02EC0B40`, running all of one
slot's steps before the next slot's; a step changes only a slot in state 2 (`0x0035AFF0`). A track's pair k is
`{duration, level}` at `+4 + 2k`, and the next pair's level is its end:

```python
level = int(start + (end - start) * frame / duration) * strength    (integer division, then the f32 strength)
```

The larger of that and the level already there is kept, the frame counts up, and at the duration the track moves
to the next pair. A pair with duration 0 ends its track, and a slot whose two tracks have both ended goes to state
4.

### Pausing

- `0x0035B4B0(mask)` adds the bits to `0x02EC0B40` and moves every playing slot whose mask shares a bit to state 3.
- `0x0035B510(mask)` removes the bits and moves every slot in state 3 back to 2, whatever its mask.
- `0x00226280` calls `0x0035B4B0(5)` when bit `0x20000000` of the flags it combines is clear and `0x0035B510(0xFF)` otherwise
  (`0x002264AE`, `0x002264B7`).

So `vibplay`'s mask 2 is never paused, and an effect's mask 1 is.

### Output to the pad channel

`0x0035AE30` runs after the stepping. With the switch `0x02EC0B3C` on it calls `0x0035FED0(channel, 1, track 1 level)` and
`0x0035FED0(channel, 0, track 2 level)` for channels 0 and 1, and with it off it sends zeros (`0x0035AE41`-`0x0035AE95`).
It then frees with `0x0035B1A0` every non-zero recorded handle whose slot is in state 4 and still carries the
handle's generation (word `+2` equal to `handle >> 8`), and clears its entry (`0x0035AEA1`-`0x0035AEE2`); a handle
whose slot's generation has moved on stays recorded.

`0x0035FED0(channel, actuator, level)` stores the level byte at `+0x06 + actuator` of the channel record `0x022CAE90`
(`0x294` bytes each) and the vsync count `0x022CA5E0` at `+0x1C + 4 × actuator`. The two capture frames, the full
menu frame and the capture-backed frame first clear the four levels with `0x0035AF10` (`0x0022AF63`, `0x0022B009`,
`0x0022BA0B`, `0x0022BCB7`).

`0x0035FED0` first clamps the actuator to 0-1, a negative one to 0 and one above 1 to 1 (`0x0035FED4`-`0x0035FEE3`), and
stores nothing for a channel of 2 or more, a signed test (`0x0035FEE6`). The count it stores is the low 32 bits of
the qword `0x0035E810` returns, `[0x022CA5E0]` (`0x0035FF11`, `0x0035FF16`).

### From the channel to the pad

On every poll `0x0035F420` calls `0x0035F590` (`0x0035F548`):

1. With the channel's flag bit `0x4` set, the large value is the envelope `+0x16` times the actuator-1 level `+0x07`,
   shifted right 14, and the small value is bit `0x200000` of the envelope `+0x16` times the actuator-0 level `+0x06`
   (`0x0035F61B`-`0x0035F639`: multiplied, shifted right 14, then right 7, then masked with 1); without it both are 0.
   - As expressions, with `/` a signed division rounding toward zero (`cdq`, `and edx, 0x3fff`, `add eax, edx`,
     `sar eax, 0xe`): `large = (+0x16 × +0x07) / 16384` (`0x0035F5E3`-`0x0035F5F7`) and
     `small = ((+0x16 × +0x06) / 16384 >> 7) & 1` (`0x0035F61B`-`0x0035F637`), each stored as a byte (`0x0035F5FA`,
     `0x0035F639`).
2. It hands them through `0x008628F0` to `0x001E1120(pad +0x02, small, large)`, and sets flag bit `0x10` when either
   level it read is non-zero. `0x0035FCA0` clears bit `0x10` before each poll (`0x0035FCE8`).
   - Each value is computed only under its bit of the first byte the third argument points to, bit `0x2` the
     large and bit `0x1` the small; with neither bit set nothing is handed over and bit `0x10` is not set
     (`0x0035F5D7`, `0x0035F60F`, `0x0035F64B`).
   - The only caller, `0x0035F420`, passes `0x022CB640` (`0x0035F53C`), whose first dword `0x00862660` sets to
     `0xFFFFFFFF` earlier in the same poll (`0x0035F44A`-`0x0035F456`), so both values are computed and handed over
     on every poll.
   - The levels are read only with flag bit `0x4` of byte `+0x09` (`0x0035F5DD`, `0x0035F615`), so with it clear bit
     `0x10` is never set (`0x0035F672`-`0x0035F676`).
3. `0x001E1120` sends zeros instead unless the input manager's last-device byte `+0x38` says the pad was used last
   (`0x00197780`) and `0x00228480` answers 0 (`0x001E1148`-`0x001E116F`).
   - It also sends zeros when `0x00198790` returns no input manager (`0x001E113E`). Either way it tail-jumps to
     `0x00198E80(input manager, pad, small, large)` (`0x001E1172`-`0x001E1186`), which looks the pad up itself and does
     not use the manager argument (`0x00198E97`-`0x00198EA5`).
4. `0x00198E80` takes the n-th registered controller of kind 2 (`0x0079D620`, `0x00796FC0(2, n)`) and `0x007A1080` stores the
   large value at `+0x98`, the small one at `+0x99` and 1 at `+0x9A`.

The XInput pad's update `0x007A2140` passes `+0x98` / 255 × 65535 as the left motor and 65535 or 0 for a
non-zero or zero `+0x99` as the right motor to `XInputSetState` (`0x007A21C5`-`0x007A2224`). The Steam controller's update
`0x007A1CD0` calls slot `0x88` of the Steam controller interface `0x02EA9508` with `+0x98` × 256 and `+0x99` × 256.

The DirectInput controller gets vtable `0x01CB2638` from its constructor `0x00792AB0` (`0x00792AC8`), and none of its
methods (`0x00794280`, `0x00290180`, `0x00799F40`, `0x0079D670`, `0x0079D730` and the update `0x007A1A50`) reads `+0x98` or
`+0x99`. Its update and `0x007A15A0` call only `Poll`, `Acquire` and `GetDeviceState` on the device and
`GetDeviceStatus` on DirectInput (`0x007A1A97`, `0x007A1AA7`, `0x007A1ADB`, `0x007A1698`), so a DirectInput pad gets no
vibration.

### The Vibration Function setting

The Config option Vibration Function is bit `0x2000` of the options word `*0x0215E6E0`. `0x002DE080` stores it from the Config
screen (`0x00240865`) and `0x002DDA30` applies it when the options are loaded; both pass it to `0x0035FF30(0, bit)`,
which sets or clears flag bit `0x4` of channel 0 (`0x002DDAA4`). `0x0035FF30` has no other caller, so nothing sets that bit
for channel 1.

### The fade-out

`0x0035F690` runs after each poll of the channel (`0x0035FD8D`) and moves the envelope `+0x16` between 0 and `0x4000` by
the step `+0x18`:

| While | Count | What happens |
|---|---|---|
| vibrating (flag bit `0x10`) | `+0x12` past `0x6DF` (1759 polls) | the step becomes -546: the envelope falls |
| vibrating | `+0x12` at most `0x6FE` | `+0x14` and `+0x10` are set to 0 (`0x0035F6FD`, `0x0035F73C`) |
| vibrating | `+0x12` past `0x6FE` (1790 polls) | the envelope is held at 0 while `+0x10` counts: one dword store at `+0x16` zeroes the envelope and the step (`0x0035F6D5`), `+0x12` is held at `0x6FE` (`0x0035F6D1`) and `+0x14` counts with `+0x10`, up to `0xB4` (`0x0035F6C4`-`0x0035F6DF`) |
| vibrating | `+0x10` past `0xB3` (180 polls) | the step becomes +546 and the counts restart: one dword store zeroes `+0x10` and `+0x12`, and `+0x14` is set to 0 (`0x0035F6E9`-`0x0035F6F6`) |
| not vibrating | `+0x14` below `0xB4` | a non-zero `+0x12` goes on counting, up to `0x6FE` (`0x0035F704`-`0x0035F71E`), and the step is kept, so a falling envelope goes on falling; only 180 polls without vibration restart the fade timing |
| not vibrating | `+0x14` reaches `0xB4` (180 polls) | the envelope returns to `0x4000` and `+0x12` to 0; the same stores set the step to 0 and `+0x14` to `0xB4`, and `+0x10` is set to 0 (`0x0035F731`-`0x0035F73C`) |

Every poll then adds the step to the envelope and keeps the sum between 0 and `0x4000` (`0x0035F741`-`0x0035F757`).

## Layouts

A request slot is `0x20` bytes; the 32 slots sit at `0x02EC0B80`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | next | the next slot in the free or playing list; `0xFF` ends it |
| `+0x01` | `u8` | state | 0 free, 1 taken, 2 playing, 3 paused, 4 finished |
| `+0x02` | `u16` | generation | raised by every free (`0x0035B1A0`) |
| `+0x08` | `u8*` | pattern | the pattern record |
| `+0x10` | `f32` | strength | 1.0 when taken; set by `0x0035B550` |
| `+0x14` | `u16` | step1 | track 1's pair |
| `+0x16` | `u16` | step2 | track 2's pair |
| `+0x18` | `u8` | frame1 | steps into track 1's pair |
| `+0x19` | `u8` | frame2 | steps into track 2's pair |
| `+0x1A` | `i16` | channel | the level pair it writes |
| `+0x1C` | `u8` | mask | the pause bits it answers to |

## Shipped data

`common/eventvib.bin` holds 11 patterns. In every one track 2 starts at pair 2, whose duration is 0, so only track 1
plays:

| Patterns | Duration in steps | Level |
|---|---:|---|
| 0, 3 | 15, 35 | 120 |
| 1 | 15 | 155 rising to 160 |
| 4 | 35 | 160 |
| 2, 5 | 15, 35 | 230 |
| 6, 7 | 15, 35 | 255 |
| 8, 9, 10 | 5 | 140, 180, 255 |

## State

The eight recorded handles at `0x022C8030` are `u32`s that `0x0035B270` clears with four 8-byte stores
(`0x0035B2B9`-`0x0035B2CE`). `0x0035B650` records a new handle in the first empty one (`0x0035B692`-`0x0035B6D1`);
`0x0035B460` (`vibstop`) and `0x0035B5D0` free each recorded handle and clear it (`0x0035B480`-`0x0035B48B`,
`0x0035B5F0`-`0x0035B5FB`), `0x0035B5D0`, from `0x00262B99`, then also frees every slot in use (`0x0035B607`-`0x0035B63C`);
`0x0035AE30` frees and clears those in state 4 (`0x0035AEB4`-`0x0035AEE2`); `0x0035B380` reads them (`0x0035B3A0`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C8038` | `u32[2]` | 0 | recorded handles 2 and 3 | `0x0035B270` (`0x0035B2C0`); `0x0035B650` (`0x0035B6D1`); `0x0035B460` (`0x0035B48B`); `0x0035B5D0` (`0x0035B5FB`); `0x0035AE30` (`0x0035AEE2`) | `0x0035B650` (`0x0035B692`); `0x0035B460` (`0x0035B480`); `0x0035B5D0` (`0x0035B5F0`); `0x0035AE30` (`0x0035AEB4`); `0x0035B380` (`0x0035B3A0`) |
| `0x022C8040` | `u32[2]` | 0 | recorded handles 4 and 5 | as for `0x022C8038`, `0x0035B270` at `0x0035B2C7` | as for `0x022C8038` |
| `0x022C8048` | `u32[2]` | 0 | recorded handles 6 and 7 | as for `0x022C8038`, `0x0035B270` at `0x0035B2CE` | as for `0x022C8038` |
| `0x02EC0F60` | `u8` | 0 | slot 31's next byte: `0x0035B270` chains slot i to slot i + 1 and ends the free list here with `0xFF` (`0x0035B288`, `0x0035B29D`); later the list code moves it like any slot's | `0x0035B270` (`0x0035B288`, `0x0035B29D`); `0x0035B1A0` (`0x0035B216`, `0x0035B226`); `0x0035B2F0` (`0x0035B346`) | `0x0035B1A0` (`0x0035B1D0`, `0x0035B1F6`, `0x0035B20E`); `0x0035B2F0` (`0x0035B31F`); `0x0035AF20` (`0x0035B143`) |
| `0x022CB5C0` | `u8` | 0 | the large value `0x0035F590` computes for the pad (actuator 1), 0 without the channel's flag bit `0x4` or without bit `0x2` of the argument byte that `0x022CB600` keeps (`0x0035F5BB`-`0x0035F602`) | `0x0035F590` (`0x0035F5BB`, `0x0035F5FA`, `0x0035F602`) | `0x008628F0`, which hands it to `0x001E1120` as the large value (`0x008628F7`), through the address `0x0035F590` passes (`0x0035F668`) |
| `0x022CB5C1` | `u8` | 0 | the small value, 0 or 1 (`0x0035F60F`-`0x0035F641`) | `0x0035F590` (`0x0035F5BB`, `0x0035F639`, `0x0035F641`) | `0x008628F0` (`0x008628FB`), the same way |
| `0x022CB600` | `u8` | 0 | the byte `0x0035F590`'s third argument points to, `& 3`: bit `0x2` lets the large value be computed and bit `0x1` the small one (`0x0035F5D7`, `0x0035F60F`); stored when either is; `0x0035F590` passes its address to `0x008628F0` (`0x0035F661`), which does not use that argument | `0x0035F590` (`0x0035F5D0`, `0x0035F650`) | no instruction |

No other instruction reaches these globals. The handles' address is taken only by `0x0035AE30`, `0x0035B380`,
`0x0035B460`, `0x0035B5D0` and `0x0035B650`, the slots' by the slot functions above, and the address of `0x022CB5C0` and
`0x022CB600` only by `0x0035F590`. `0x0035AF20` reads the slot bytes by slot number, relative to the image base.

## Modding notes

- A second track in `eventvib.bin` drives the right motor through a two-valued small command: the small value is 1
  only for a level of 128 or more at full envelope. XInput passes 0 or 65535 for it as the right motor, the Steam
  controller 0 or 256 (`0x007A21FC`-`0x007A221F`, `0x007A2099`-`0x007A20D0`). No shipped pattern plays a second track
  (track 2 has duration 0 in all 11, above).
- The table's patterns always play on channel 0, the only channel the Vibration Function setting reaches.
- `0x0035B510` resumes every paused vibration, not only those of the mask it clears.
- The pattern file's layout is on [Small .bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md).

## Related

- [Controls](controls.md) - the channel record, the poll and the last-device byte.
- [Controllers](controllers.md) - the XInput, Steam and DirectInput controllers.
- [Small .bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md) - the `VIB0` file.
- [Config screen](../Menus-And-HUD/config-screen.md) - the Vibration Function row.
- [`vibration-recorded-handles-022c8030-accesses.tsv`](vibration-recorded-handles-022c8030-accesses.tsv) - the
  instructions that reach the eight recorded handles at `0x022C8030` through a pointer that walks them, one row per
  instruction (51 rows).

In this access table, `function`, `name` and `site` give the function, its name and the instruction's address,
`disp` the offset from the handle the pointer has reached (0 in every row), `kind` a read (`r`) or a write (`w`),
`instruction` the instruction itself, and `route` `route-seeded STATIC 0x022C8030 base+0x0`: the handle array at
`0x022C8030`.
