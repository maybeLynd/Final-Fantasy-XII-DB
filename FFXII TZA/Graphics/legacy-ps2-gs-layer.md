---
title: "Legacy PS2 GS layer: the GS memory model, the map texture slot rebuild and the VU register leftovers"
kind: "system"
category: "Graphics"
summary: "What the remaster keeps of the PlayStation 2 Graphics Synthesizer model outside the VIF1 / VU1 emulation: the 512 x 448 surface seed and its three reserved surfaces, the GS page geometry of 003A1E50, the 4 MiB local-memory budget, the rebuild that gives the bound map's multiply used textures compact slots when the weather slot changes or a map is bound, the per-pass reset of those slots, the GS image-transfer registers, and the VU register words that recompiled microprograms use for Q and vf00."
addresses: "0036D280, 0036D2F0, 022D8EAC, 022D8EB4, 022D8EA8, 003A1E50, 00466190, 00466220, 00467AA0, 00467AD0, 00467B00, 00467B10, 002F7380, 0026E290, 0026E8D0, 0209A670, 0209A6E8, 0209A708, 002F4520, 00244200, 004B9870, 01E02830, 02064B00"
---

## What the player sees

Nothing directly. The PC renderer draws at the display resolution, but a layer of the
PlayStation 2 code still runs underneath it with the console's numbers: a 512 × 448 frame, a
4 MiB Graphics Synthesizer local memory of 8 KiB pages, and a texture budget computed against
it. When a field's weather slot changes or a map is bound, the game recounts which of the map's textures are used
more than once and gives as many of them as fit in that budget a compact slot.

The VIF1 packet decoder, the recompiled VU1 microprograms and the GS replay are on
[PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md); this page covers
the rest of the GS model.

## How it works

### The surfaces

`0036D280` seeds the GS globals: width `022D8EAC` = `0x200`, `022D8EB0` = `0x200`, height
`022D8EB4` = `0x1C0`, frame index `022D8EA8` = 0, the clear colour `022D8ED8` = 0 with its switch
`022D8EDC` = 1, and `022D8EE0` = 1. Those stores at `0036D286`, `0036D2A3`, `0036D2AD` and
`0036D290` are the only stores that name the three dimension words and the frame index.

`0036D2F0` then computes the pages per surface, `(width × height) >> 11` = 112 GS pages of 2,048
words, into `022D8EB8` (`0036D393`), fills the two 0x28-byte display records at `022D8E50` and
`022D8E78`, and points `022D8EA0` at the first. The GS register batch `0036D400` places the colour
surface at page `index × 112` with PSM 0 and the Z surface at page 224 with bit 24 set
([graphics thread handshake](graphics-thread-handshake.md)). With the index at 0 the frame uses
surfaces 0 and 2 of the three the budget reserves.

### GS page geometry

`003A1E50(width, height, psm)` returns a texture's footprint in 32-bit words, rounded up to whole
GS pages. It indexes the 43-byte table `003A1EF0` with `psm − 2`; an index above `0x2A`, which
includes PSM 0 and 1 through the unsigned compare at `003A1E68`, takes the default class. The
class picks an arm from `003A1EE0`:

| Class | PSMs | Width align | Height align | Divisor | Smallest footprint |
|---|---|---:|---:|---:|---:|
| default (`003A1EBA`) | all others, including `0x00`, `0x01` | 64 | 32 | 1 | 2,048 words |
| 0 (`003A1E96`) | `0x02`, `0x0A` | 64 | 64 | 2 | 2,048 words |
| 1 (`003A1E9E`) | `0x13`, `0x1B` | 128 | 64 | 4 | 2,048 words |
| 2 (`003A1EAD`) | `0x14`, `0x24`, `0x2C` | 128 | 128 | 8 | 2,048 words |

These are the GS page sizes of the 32-, 16-, 8- and 4-bit pixel formats. `00466190(bank, index)`
sums `003A1E50` over a texture record's mip levels, halving width and height each level, with the
level count at `+0x05` capped at 7 (`004661C5`–`004661CC`). `00466220(record)` returns 1 exactly for
PSMs `0x14`, `0x24` and `0x2C`: `(psm − 0x14) & 0xE7` must be 0 and `psm` must not be `0x1C`.

### The budget

`00467AD0` stores `0x4000` at `02CA5FF0` and the reservation `(width × height × 3) >> 6` at
`02CA5FF4`: 10,752 blocks of 64 words. `00467AA0` returns the budget

```
budget = (0x1007FF - 3 * width * height - [02CA6008] - [02CA6004]) & 0xFFFFF800
```

that is, the 4 MiB memory (`0x100000` words) less three 512 × 448 surfaces at 4 bytes per pixel,
less the two totals the rebuild publishes, rounded up to a whole page. With both totals at 0 it is
360,448 words: 1.375 MiB, 176 pages. The surface size is fixed, so the budget does not depend on
the display resolution.

### When the rebuild runs

The bound map is the object at `0209A670` ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)).
`0026E8D0(slot)`, the weather rebind ([weather](../World-Areas-And-Travel/weather.md)), stores the slot
at `0209A6E8` and sets the dirty word `0209A708` (`0026E8E7`); `0026E960` sets it too when a map
is bound (`0026E9B0`). These are its only two non-zero stores; the reset `0026E1D0` clears it. The stores of 1 at
`0026E221` and `0026E9A6` go to the neighbouring word `0209A6FC`.

The draw's pass-bit-0 block calls `0036F430` and `0036F450`, which call `0026E290` with 0 and 1.
While a map is bound and its `+0x120` is non-zero, `0026E290` runs `002F7380(map, [0209A668])` when
the dirty word is set and then clears it (`0026E2C4`, `0026E2C9`), and then calls the map's
`+0x130` handler with the pass. That handler is `002F4520`, installed by the map set-up
`002F6AB0` (`002F6B43`); it starts by setting `+0x00` of every slot record to 0 and `+0x20` to
`0xFF` (`002F45F0`–`002F4617`).

### The slot rebuild

`002F7380(map)` works on the map's texture records (a bank at `[+0x150]`: count at `+0x00`,
0x60-byte records from `[+0x08]`) and its instance records (`[+0x178]`, 0x30 bytes, count `+0x174`):

1. free the old slot table at `+0x218` (`003EC8A0`) and copy the bank's count to `+0x224`;
2. for every texture record: track the largest mip-chain footprint (`00466190`, `002F7436`–`002F743B`),
   add 1 for a 4-bit record or 4 for any other to a second total (`002F744A`–`002F7455`), and set
   the word `+0x0E` to 0 (`002F7445`);
3. publish the largest footprint to `02CA6004` (`00467B10`) and the total to `02CA6008`
   (`00467B00`), then take the budget from `00467AA0`;
4. for every instance record whose flag word `+0x0C` has bit `23 + slot` set (`002F738E`–`002F7397`,
   `002F74C9`) and whose texture index `+0x04` is at most `0x3FFF`: unless the record repeats the
   previous one's texture index and byte `+0x1D`, increment `+0x0E` of that texture record and of
   every following record whose `+0x0C` word is non-zero (`002F7500`–`002F753D`);
5. walk the texture records in bank order: a record counted more than once is admitted when the
   running total plus its footprint stays below the budget (`002F75A2`), and gets the next slot
   number in `+0x0E`; every other record gets `0xFFFF` (`002F75B0`). A record that does not fit is
   skipped and the walk goes on, so a smaller record later in the bank can still be admitted;
6. with any admitted, store the count at `+0x228`, allocate `count × 40` bytes (`003EC8D0(6, …)`)
   at `+0x218`, and zero `+0x00`, `+0x08`, `+0x10`, `+0x18` and the byte `+0x20` of each record
   (`002F760B`–`002F761F`).

### GS image transfers

`00244200`, called from `002D2DB0`, writes GS register records for image transfers: BITBLTBUF
`0x50`, TRXPOS `0x51`, TRXREG `0x52` and TRXDIR `0x53` (`002442D2`–`00244332`), then TRXPOS, TRXREG
and TRXDIR again (`00244355`–`0024439C`). It reads the frame index and the height to place the
transfer. The GS replay honours none of these four registers.

### VU register words outside VU memory

Recompiled VU1 microprograms keep VU registers in fixed globals next to the emulated VU memory
`02064E30`:

- `02064B00` is a scratch cell shared by many recompiled programs from `0047xxxx` to `0054xxxx`, and
  by a few effect routines (`002F05F8`).
- One of its writers is the division helper `004B9870`, which stores `a / b`, or
  `0x7F7FFFFF` (`00900360`, the largest float) when `b` is 0. The programs `004B1190` and `004C8320`
  load its address six times each and pass it to `004B9870` four times (`004B7C31`, `004B7CE4`,
  `004B895F`, `004B8A12`): for those two programs it plays the VU's Q register.
- `01E02830` holds `(0, 0, 0, 1.0)`, the fixed contents of the VU's register vf00. `004B1190` loads
  its address 17 times as the second operand of its lane helpers, which include `004B9D80`,
  `004B9E60` and `004B9A10`.
- `004ADD10`, another installed program, reads VU memory cells directly through `02064E30`.

## Layouts

Texture record (map +`0x150` bank, from [+`0x08`]), `0x60` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | psm | GS pixel format |
| `05` | `u8` | levels | capped at 7 by `00466190` |
| `06` | `u16` | width | halved per level |
| `08` | `u16` | height | halved per level |
| `0C` | `u16` | continues | non-zero: counted with the record before it |
| `0E` | `i16` | count, then slot | reference count during step 4; slot or `0xFFFF` after step 5 |

Instance record (map +`0x178`, tag 30 of the map pack), `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `02` | `i16` | placement row | read by `003A6FC0` |
| `04` | `u16` | texture record index |  |
| `0C` | `u32` | flags | bit 23 + slot: present for that weather slot |
| `1D` | `u8` | sub-index | a repeat of the previous index and sub-index is not counted again |

Slot record (map +`0x218`, count +`0x228`), `0x28` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u64` | cleared at allocation and by 002F4520 every pass |  |
| `08` | `u64` | cleared at allocation |  |
| `10` | `u64` | cleared at allocation |  |
| `18` | `u64` | cleared at allocation |  |
| `20` | `u8` | 0 at allocation, 0xFF from 002F4520 every pass |  |
| `21` | `-` | never written |  |

```
GS model constants
memory     0x100000 words   4 MiB
page       0x800 words      8 KiB, the budget's rounding unit
block      0x40 words       256 bytes, the unit of 02CA5FF4
surface    512 x 448 x 4 B  112 pages; three reserved = 688,128 words
```

Access tables beside this page:

| Subject | Table |
|---|---|
| the bound map's fields | `legacy-ps2-gs-layer-legacy-ps2gs-texture-context-accesses.tsv` |
| texture records | `legacy-ps2-gs-layer-legacy-ps-2-gs-source-texture-record-accesses.tsv` |
| instance records | `legacy-ps2-gs-layer-legacy-ps-2-gs-reference-descriptor-accesses.tsv` |
| slot records | `legacy-ps2-gs-layer-legacy-ps-2-gs-derived-slot-record-accesses.tsv` |
| `02064B00` | `legacy-ps2-gs-layer-vu1-register-bank-02064b00-accesses.tsv` |
| `01E02830` | `legacy-ps2-gs-layer-vu-1c-onstant-vector-01e02830-accesses.tsv` |
| `02064E30` | `legacy-ps2-gs-layer-vu-1da-ta-memory-02064e30-accesses.tsv` |

## State

| Address | What |
|---|---|
| `022D8EAC`, `022D8EB0`, `022D8EB4` | the 512 × 448 GS frame |
| `022D8EA8`, `022D8EB8` | frame index and pages per surface |
| `02CA5FF0`, `02CA5FF4` | `0x4000` and the reservation in blocks |
| `02CA6004`, `02CA6008` | the rebuild's largest footprint and weighted count |
| `0209A670`, `0209A6E8`, `0209A708` | bound map, weather slot, dirty word |

## Modding notes

- The texture budget is the same on every machine: 176 GS pages less the rebuild's two totals,
  rounded up to a page.
- A texture used by only one instance record never gets a slot, whatever the budget.
- Admission follows the bank order of the texture records; moving a large texture later in the bank
  lets smaller ones before it in.
- To refresh the slots, change the weather slot through `0026E8D0`; the next draw rebuilds. Calling
  `002F7380` directly skips the dirty bookkeeping.
- Bytes `+0x21` to `+0x27` of a slot record are never initialised; do not read them.

## Related

- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the VIF1 decoder, the microprograms, VU memory and the GS replay.
- [Graphics thread handshake](graphics-thread-handshake.md): the GS register batch that uses the surfaces.
- [Weather](../World-Areas-And-Travel/weather.md): the slot change that marks the map dirty.
- [MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md): the map sections the texture and instance records come from.
- [Gi render commands](gi-render-commands.md): `GiPolyGT4T`'s texture-descriptor lookup.
