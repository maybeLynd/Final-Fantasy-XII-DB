---
title: "File size tables: the per-language .fst that sizes every file by resource kind and id"
kind: "format"
category: "Game files and data tables"
addresses: "0x002DF9A0, 0x02EC3EE0, 0x002DF960, 0x0032E400, 0x0032EB40, 0x002DF780, 0x0215F000, 0x01E88B00, 0x00B56AC8, 0x0032FCA0, 0x0024AC30, 0x022C51F0, 0x0032EA90, 0x0046DE50, 0x0032EC20, 0x0046E050, 0x0046DE80, 0x0046DD50, 0x00536F30, 0x00536DD0"
---

## What the player sees

Nothing directly. Every file the game loads by kind and number, from a map's script to a menu image, is
sized from this table before it is read; a file the table marks absent is never read, and a missing or
short table stops the game at start-up.

## Where it comes from

Twelve files ship loose in the install's `FileSizeTables` folder, one per language:
`FileSizeTable_{JP,US,FR,DE,IT,ES,UK,KR,CH,ASIA,IN,CN}.fst`.

`ResourcePath_Init` (`0x002DF9A0`), called
once at boot, builds the name with
 `sprintf("%sFileSizeTables/FileSizeTable_%s.fst", "../", name)`,
where `name` is the language's entry in the twelve-string table at `0x01E88B00`
(`JP US FR DE IT ES UK KR CH ASIA IN CN`, indexed by the language id it receives), opens it with
`fopen(…, "rb")` and reads all 820,000 bytes into `0x02EC3EE0` with one `fread`. The working folder is
the executable's `x64`, so `../` is the install root.

## Layouts

All multi-byte fields are little-endian.

```python
FileSizeTable  820,000 bytes, no header
+0x00000  u32[41 * 5000]  size[kind * 5000 + id] in bytes; 0xFFFFFFFF = no file for (kind, id)
```

The kind count and the id stride live only in the readers (`kind × 5000 + id`). The 41 kinds are the 41
path-array pointers at `0x0215F000 + kind × 8` that `0x002DF9A0` installs, and an id is the position in the
kind's path array, so `size[kind][id]` is the size of the file that array names at that position. Seven
kinds (1, 2, 5, 7, 8, 9, 12) take a per-language array. For KR, CH and CN, kinds 21, 26 and 37 (the
`.ard`, `.nmb` and event `.ebp` arrays) are replaced too (`0x01E0CFA0`, `0x01EAE0D0`, `0x01EA4D00`); JP,
ASIA and IN keep the shared arrays.

The table is used as loaded. `0x002DF9A0` reads the file into `0x02EC3EE0` as one item of `0xC8320` bytes
(`0x002E0432`-`0x002E0444`); a count other than 1 takes its error path (`0x002E044D`). Only two other instructions
name the array, and both read it: `0x002DF960` returns `size[kind × 5000 + id]` (`0x002DF977`), and `0x002DF780` tests an
entry for −1 (`0x002DF7B0`). Nothing converts, relocates or writes it after the read.

## Shipped data

| Fact | Value |
|---|---|
| files | 12, each exactly 820,000 bytes; 10 distinct contents (JP, ASIA and IN are identical) |
| first dword | 57: kind 0, id 0, `PS2Data\cdi\in\system.cnf` |
| US table | 31 of 41 kinds populated, 10,521 entries; no zero sizes |
| empty kinds | 3, 6, 17, 18, 27, 29, 31, 35, 36, 40 |
| ASIA against US | entries differ in kinds 1 (23), 2 (27), 5 (533), 7 (34), 8 (181), 9 (1) and 12 (130) |

Populated kinds in the US table, with the first sized path of each kind's array:

| Kind | Entries | Largest id | Sizes (bytes) | First sized path |
|---:|---:|---:|---|---|
| 0 | 1 | 0 | 57 | `PS2Data\cdi\in\system.cnf` |
| 1 | 24 | 132 | 2,370 – 57,864 | per-language mixed files (`sound\se\map\position_map\spp\env\env99.spp`, `image\ff12\us\bin\planmapname.bin`) |
| 2 | 81 | 82 | 27 – 281,128 | `image\FF12\test_battle\in\BinaryFile\WepJob_Matrix.bin` |
| 4 | 550 | 775 | 192 – 8,054,336 | `plan_master\map_ctrl\ous01\ous0100\bin\ous0100.mpk` |
| 5 | 896 | 3,933 | 1,216 – 985,088 | `plan_master\us\plan_map\ttl_a\ttl_a01\global\ttl_a01.ebp` |
| 7 | 536 | 1,178 | 16 – 11,544,192 | `image\FF12\myoshiok\in\Bin_Menu\fontcolor.bin` |
| 8 | 1,080 | 2,963 | 896 – 5,238,784 | `plan_master\us\event\nal_a\nal_a0100\nal_a0100.ebp` |
| 9 | 26 | 42 | 26 – 37,545 | `image\ff12\common\test_map_ref.bin` |
| 10 | 2 | 1 | 106,672 – 1,017,904 | `effect_finish\jp\common\c_all.efx` |
| 11 | 366 | 396 | 21,632 – 969,536 | `effect_finish\jp\magic\m0000.efx` |
| 12 | 532 | 883 | 3,520 – 25,310,800 | `effect_finish\jp\event\e0000.efx` |
| 13 | 103 | 206 | 8,192 – 425,984 | `obj_finish\in\gadget\g0001.cm` |
| 14 | 143 | 550 | 139,264 – 1,064,960 | `obj_finish\in\chara\c10\c1004\c1004.cm` |
| 15 | 47 | 47 | 32,768 – 229,376 | `obj_finish\in\high\c10\c1004\hc1004_01.cm` |
| 16 | 326 | 326 | 7,168 – 131,072 | `obj_finish\in\weapon\w2002.cm` |
| 19 | 691 | 4,350 | 4,096 – 1,900,544 | `obj_finish\in\npc\n10\n1059\n1059.cm` |
| 20 | 80 | 86 | 24,576 – 327,680 | `obj_finish\in\high\n10\n1018\hn1018_11.cm` |
| 21 | 166 | 640 | 224 – 35,632 | `plan_master\in\plan_map\nal_a\area\nal_a.ard` |
| 22 | 17 | 34 | 24,576 – 716,800 | `obj_finish\in\bg_obj\b00\b0001\b0001.cm` |
| 23 | 78 | 627 | 81,920 – 1,753,088 | `obj_finish\in\summon\s0002\s0002.cm` |
| 24 | 5 | 4 | 180,224 – 393,216 | `obj_finish\in\high\s00\s0003\hs0003_01.cm` |
| 25 | 17 | 16 | 34,816 – 57,344 | `obj_finish\in\treasure\t0004.cm` |
| 26 | 166 | 320 | 8 – 162 | `plan_master\in\plan_map\nal_a\area\nal_a.nmb` |
| 28 | 43 | 95 | 228 – 94,356 | `movie_finish\us\OPN.mh` |
| 30 | 1,969 | 2,315 | 1,408 – 130,208 | `obj_finish\in\chara\c10\c1004\c1004_10_3000.ca` |
| 32 | 248 | 317 | 708 – 24,968 | `sound\se\block\se000.seb` |
| 33 | 64 | 63 | 59,456 – 100,336 | `sound\shout\us\shout00\shout00.win.sab` |
| 34 | 754 | 2,785 | 4,096 – 2,752,512 | `obj_finish\in\monster\m10\m1002\m1002.cm` |
| 37 | 1,080 | 2,963 | 896 – 5,238,784 | `plan_master\in\event\nal_a\nal_a0100\nal_a0100.ebp` |
| 38 | 366 | 396 | 21,632 – 1,001,792 | `effect_finish\jp\magic\m0000.efx` |
| 39 | 64 | 63 | 56,384 – 85,312 | `sound\shout\jp\shout00\shout00.win.sab` |

All paths begin `PS2Data\`. Kind 5 holds each area's script set, three files per area: id `3a` its
global `.ebp`, `3a + 1` its `.mot` and `3a + 2` its `.fpk`. The area loader `0x0032FCA0` asks for kind
5, index `area × 3`, for area slot 0 (and slots above 4), kind 8 with index `area × 4` for slots 1 to
3, and kind 1 with index `area + 0x6B` for slot 4.

Of the ten empty kinds, six (3, 17, 18, 29, 36, 40) point at runtime slots rather than path arrays.
Four have arrays the table never sizes: kind 6 (`image\FF12\isowaki\ousi00.bin` and `dummy.bin`
entries), 27 (`sound\wave\wave0000.wd` onward), 31 (`sound\music\data\music000.bgm` onward) and 35
(`c:\image\ff12\overlay\in\ff12menuoverlay_00_debug.bin` onward). `0x0024AC30` requests kind 35, index
`n + 7`, with the `−1` size it reads; the read issuer refuses it and the queue then reports it delivered
with nothing read. No call site of `0x0032E620` passes kind 6, 27 or 31.

## Loader behaviour

- **Boot.** A failed `fopen` or a short `fread` prints through the CRT and then writes to address 0, a
  deliberate crash.
- **The size.** `0x002DF960(kind, id)` returns `size[kind][id]`. The request builder's size `0x0032E400`
  returns −1 for kind `0xFF`, consults a per-kind override pointer at `0x022C51F0` first (which only
  `0x0032EA90`'s zero-clear writes, so it is always null), and otherwise rounds a positive table size up
  to a multiple of 64.
- **The staged head read.** `0x0032EB40(slot, kind, id)` takes the same size and, when it is above
  `0x800`, requests only the first 2 KB into `0x022C5C00 + slot × 0x800`.
- **The read.** The read issuer `0x002DF780(kind, id, dest, bytes, offset)` does nothing for an entry of
  −1 and leaves the read status `0x0215EFF4` as the previous read left it; otherwise it takes the path at
  the kind's array position and reads it through the file cache or the archive (`0x001D6D90` and
  `0x001D6FB0` set the status to −1 when they issue).
- **A refused request.** The queue completes it with the
  previous read's status, normally as delivered, with the destination untouched.
- **No bounds checks.** Neither reader tests the kind or the id against 41 or 5,000.

### Behind the staged head read

`0x0032EB40` first clears read-layer slot `slot` (`0x0046DE50`: its destination `+0x10`) and gives its request the
word `slot << 24 | kind << 16 | id` and the delivery callback `0x0032EC20`, which unpacks that word into
`0x0046E050(slot, kind, id, dest)`. That fills one of two `0xA0`-byte slots at `0x02CA6070`: the kind, the
destination, and a sector that `0x0046DE80(kind, id)` computes from a sector directory at
`0x02EBA508`.

Nothing writes `0x02EBA508`, which is 0 in the image, so the sector is always 0. The read layer's tick
`0x0046DD50` acts only in its states 1 to 4, and its state `0x02CA6068` is 0 in the image and written only by
the tick itself (to 0, 3 and 4), so the tick never leaves state 0.

The expansion the tick would hand to `0x00369050` therefore never runs: `0x00536F30` reads a header (12
bytes when byte 3 is `d`, else 16; the size in the low 25 bits of `+8`) and by the low two bits of `+4`
copies the data, expands it with `0x00536DD0`, or with `0x00537030`. In `0x00536DD0` an even control byte b
copies `b >> 1` literal bytes, and an odd one with the next byte copies `(next >> 4) + 3` bytes from
`((word >> 1) & 0x7FF) + 1` bytes back.

## Modding notes

- The path comes from the executable's static array for the kind, so only ids that already have a path
  can be sized; adding a file needs a new entry in that array as well. An id past the array's end is
  read past it, since nothing checks the bounds.
- A path whose size entry is −1 is never read, and its requester is told it was delivered.
- The table must stay exactly 820,000 bytes; a shorter file stops the game at boot.
- JP, ASIA and IN share one table, so an edit for one of them belongs in all three.

## Related

- [File requests and the read queue](file-requests-and-the-read-queue.md): where the size becomes a request's byte count.
- [Bigfile archive](bigfile-archive.md): where the named files are read from.
- [Area .nmb index](ard-area-battle-data.md): the kind 26 files and the table of path arrays.
