---
title: "Save data fields: the regions of the save payload, who writes and reads each, and the access table"
kind: "reference"
category: "Saving, loading and settings"
addresses: "002EF2B0, 002EF2D0, 00253970, 00253A80, 00229B40, 005843E0, 00584580, 005844A0, 00233440, 00233550, 0025D8E0, 00269A20, 002EF3C0, 002EF410, 00238A80, 00233C10, 002370C0, 00583D60"
---

## What it lists

The save image is `56690`<sub>h</sub> bytes: a `200`<sub>h</sub>-byte header (see the [save file format page](save-file-format.md))
followed by the `56490`<sub>h</sub>-byte persistent payload. `002EF2B0` returns the payload's address as
`002EF640() + 200h`, and every offset on this page is relative to that payload. An instruction that
works on the whole buffer shows an offset `200`<sub>h</sub> larger: `00229B40`'s `+4E68C`<sub>h</sub> is payload `+4E48C`<sub>h</sub>,
and `002EF390`'s `+C00`<sub>h</sub> is payload `+A00`<sub>h</sub>.

The table below lists the payload's regions with the functions that write and read each one. The
companion table [`save-data-fields.tsv`](save-data-fields.tsv) holds every access that reaches the
payload directly through the buffer getters, or through a pointer those functions pass on, with its
instruction text checked against the executable.

### The regions

| Payload offset | Size | Region | Written by | Read by |
|---|---|---|---|---|
| `00000`<sub>h</sub> | 512 | script operand bank, `i16[256]`, reached through the slot pointer `02098E58` that `0026C8C0` sets to `002EF2B0()` | `0026ABA0` | `00264640` |
| `00200`<sub>h</sub> | 3584 | the script-global variable space up to the quest arrays, addressed by the scripts' own descriptors ([the storage-class page](../Scripts-And-Script-Commands/script-variables.md)) | scripts | `002EF390` tests `+A00h + i == 1` |
| `01000`<sub>h</sub> | 32 | quest ordered bits, one per quest id | `0046B3F0` (`setquestorder`); `0046B290` also clears a bit here, but of quest `id & 7` (it re-splits the bit index at `0046B2EF`), so only quests 0-7 are un-ordered that way | `0046B240` (`isquestorder`), `0046B0F0` (the count) |
| `01020`<sub>h</sub> | 32 | quest cleared bits | `0046B290` (`setquestclear`) | `0046B1A0` (`isquestclear`), `0046B020` (the count) |
| `01040`<sub>h</sub> | 4 | a counter of `setquestclear` calls with a non-zero value, incremented while below `FFFF`<sub>h</sub> | `0046B290` | `0046B0B0` (`getquestcleartotal`) |
| `01044`<sub>h</sub> | 32 | the zone transition record ([zone changes page](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) | `003145E0`, `00314970`, `0026D910`, `0026A720` | `003148F0`, `00314870`, `00314850`, `003148D0`, `0026DE20` |
| `01064`<sub>h</sub> | 256 | quest scenario flag, `u8` per quest id | `0046B490` (`setquestscenarioflag`) | `0046B180` (`getquestscenarioflag`) |
| `01164`<sub>h</sub> | 512 | `u16` per quest id: the field id (`003148F0()`) when the quest was first ordered | `0046B3F0`, `0046B350` | `0046B0D0` |
| `01364`<sub>h</sub> | 32 | quest ok bits | `0046B380` (`setquestok`) | `0046B1F0` (`isquestok`) |
| `01384`<sub>h</sub> | 8 | flag bank of 64 bits ([persistent flag banks page](../Story-Events-And-Hunts/story-flags.md)) | `0032AC70` | `0032A9A0` |
| `0138C`<sub>h</sub> | 8 | second flag bank of 64 bits | `0032ACF0` | `0032AA00` |
| `013B4`<sub>h</sub> | 256 | flag bank of 2048 bits | `0032ABF0` | `0032A930` |
| `014B4`<sub>h</sub> | 64 | flag bank of 512 bits: ids 0-255 in the first 32 bytes, ids 256-511 in the next | `0032AD70`, `0032ADF0` | `0032AA60`, `0032AAD0` |
| `014F4`<sub>h</sub> | 64 | the primary flag bank, ids 2-511 | `0032AB60` | `0032A8A0` |
| `01534`<sub>h</sub> | 1 | the music track override, used while `+1063`<sub>h</sub> bit 6 is set | `0026A720` | `0026DE20`, `0025D9E0`, `00261F90` |
| `01535`<sub>h</sub> | 1 | a byte the options apply `002DDA30` writes as 1 and the verb handler `0050D180` writes from its operand, through `002EF370` | `002EF370` | |
| `02000`<sub>h</sub> | 24576 | a copy of the battle-state block's first `6000`<sub>h</sub> bytes | `00229B40`, `005844A0` | `00235AF0` |
| `08000`<sub>h</sub> | 18456 | the image-backed state block, `*(020927C0)` | see its table below | |
| `0E000`<sub>h</sub> | 4 | the plain CRC of image `+8`<sub>h</sub>-`+E1FF`<sub>h</sub> (`003BB220`), whose complement the header carries at `+00`<sub>h</sub>; computed over the active buffer `002EF640()` but stored into the buffer `00583D60`'s third argument selects (the staging buffer when it is not 0, as `003145E0` passes through `005844A0`) | `00583D60` | |
| `0E040`<sub>h</sub> | 512 | group persistent bank A, a copy of `02099FF0` | `0025D8E0` from `00229B40` and `00584580` | `00269A20` from `005843E0` and `00584210` |
| `0E240`<sub>h</sub> | 131088 | spawn-keep image A | `00233440` from `00229B40` and `00584580` | `00233550` from `005843E0` |
| `2E250`<sub>h</sub> | 512 | group persistent bank B | `0025D8E0` | `00269A20` |
| `2E450`<sub>h</sub> | 131088 | spawn-keep image B | `00233440` | `00233550` |
| `4E460`<sub>h</sub> | 44 | the save-transition metadata record | `002EF540`, `002EF3C0`, `002EF510`, `00584580`, `003145E0` | `002EF410`, `005843E0` |
| `4E48C`<sub>h</sub> | 29712 | the battle-state block, `*(02EBF190)` ([its field map](../Party/party-data.md)) | bound by `00238A80` and `00233C10`, reset by `002370C0` | |

Each spawn-keep image is preceded by its group bank, so pair A and pair B are two `20210`<sub>h</sub>-byte
blocks at `+E040`<sub>h</sub> and `+2E250`<sub>h</sub>, and `005844A0` clears both pairs with one `memset` of `40420`<sub>h</sub> bytes
when its fourth argument is 0 and its fifth is 0.

## Columns

The companion table has one row per access site:

| Column | Meaning |
|---|---|
| `offset` | the payload-relative offset the instruction reaches |
| `region` | the region from the table above that contains the offset |
| `function` | the function containing the instruction |
| `site` | the instruction's address |
| `kind` | `r` read, `w` write, `rw` read-modify-write, `addr` the address is formed (`lea`) and passed on |
| `instruction` | the instruction text, as disassembled from the executable |
| `via` | empty when the function computes the address from the buffer getter itself; otherwise the argument register and the caller and call site that passed the pointer in |

Rows inside the battle-state block are listed only when the function reaches the block from the buffer
getter itself; accesses through the block pointer `02EBF190` belong to the block's own field map.

## Data

### The span a new game clears

`002EF2D0` zeroes the first `1538`<sub>h</sub> bytes of the payload and `002EF290` returns that length for the
header's `+5C`<sub>h</sub>. The span holds the operand bank, the script globals, the quest arrays, the zone
transition record, the flag banks and the music override; the last two bytes, `+1536`<sub>h</sub> and
`+1537`<sub>h</sub>, have no access in the table.

### The zone transition record

The record at `+1044`<sub>h</sub> is written by `003145E0` when a zone change is staged and reset by
`00314970`:

Struct ZoneTransitionRecord base=payload+`1044`<sub>h</sub> size=`20`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | destinationField | the field being entered; also `01EED064` (`003145E0`) |
| `04`<sub>h</sub> | `i32` | destinationEntrance | the entrance index (`003145E0`, `00314D80`) |
| `08`<sub>h</sub> | `i32` | previousField | the old destinationField (`003145E0`) |
| `0C`<sub>h</sub> | `i32` | previousEntrance | the old destinationEntrance (`003145E0`) |
| `10`<sub>h</sub> | `u32` | mode | the mode argument (`003145E0`, `00314DA0`) |
| `14`<sub>h</sub> | `i32` | persistenceGroup | `00264F90`(destinationField) (`003145E0`) |
| `18`<sub>h</sub> | `i32` | transitionField | destinationField again; `00314530` copies it on restore (`003145E0`) |
| `1C`<sub>h</sub> | `u8` | runtimeParameter | 0 to 2, set by `0026D910` while initState is 0, passed to `00180620` |
| `1D`<sub>h</sub> | `u8` | initState | 1 from `00268320` and `0026D8F0`, cleared by `0026D910` |
| `1E`<sub>h</sub> | `u8` | flags1 | bit 5 cleared by `003145E0`, set by `00314530` |
| `1F`<sub>h</sub> | `u8` | flags2 | bit 6: the music override at +`1534`<sub>h</sub> is in force (`0026A720`, `0026DE20`) |

`00584210` stashes `+1044`<sub>h</sub>-`+1054`<sub>h</sub> into the header's `+80`<sub>h</sub>-`+90`<sub>h</sub> when a load begins and puts
them back on the restore path (see the [save file format page](save-file-format.md)).

### The image-backed state block

`00253970` binds `020927C0` to image `+8200`<sub>h</sub>, payload `+8000`<sub>h</sub>, and `00253A80` initialises the
block in four steps:

1. it zeroes all `4818`<sub>h</sub> bytes;
2. it writes six header dwords at `+58`<sub>h</sub>-`+6C`<sub>h</sub>: `20050223`<sub>h</sub> from `002EF2A0`, `1538`<sub>h</sub> from
   `002EF290`, the battle-state block's magic `05071901`<sub>h</sub> from `00235E90` and its size `7410`<sub>h</sub> from
   `00235E80`, then the block magic `0131F3EA`<sub>h</sub> and its size `4818`<sub>h</sub>;
3. it runs `00253240` for the twelve classes;
4. it zeroes `+30`<sub>h</sub> for 500 bytes, `+3244`<sub>h</sub> for `80`<sub>h</sub>, `+32C4`<sub>h</sub> for 8 and `+224`<sub>h</sub> for `3020`<sub>h</sub>.

Offsets in this table are block offsets; add `8000`<sub>h</sub> for the payload offset.

| Block offset | Size | Content | Written by | Read by |
|---|---|---|---|---|
| `0008`<sub>h</sub> | 40 | the in-game options record `0215E6E0` ([game settings page](game-settings.md)) | `002DDE60` | the option getters |
| `0030`<sub>h</sub> | 64 | `u16[32]`, class 6 of the typed store, index clamped to 31 | `002527B0`, cleared by `00252610` | `002526F0` |
| `0070`<sub>h</sub> | 32 | `u8[32]`, class 7 | `002527B0`, `00252610` | `002526F0` |
| `0090`<sub>h</sub> | 404 | `u32[101]`, class 8, index clamped to 100 | `002527B0`, `00252610` | `002526F0` |
| `0224`<sub>h</sub> | 12320 | navigation-map exploration bitmaps: 385 entries of 32 bytes, indexed by `003779F0(field)` ([area flags page](../World-Areas-And-Travel/area-flags-navimapdata.md)) | `003C60F0`, `003C8670`, `003C5E50` copy the live block `02B45978` in | `002551B0` |
| `3244`<sub>h</sub> | 1 | inventory category bits 1-8, set when a category's derived list is non-empty | `00252D40` from `002CD650` | `00252D10` |
| `3245`<sub>h</sub> | 1 | a flag byte whose bit 0 `00253480` clears after each `00253240` | `00253480` | |
| `32C4`<sub>h</sub> | 8 | a bit set indexed by a `u16` | `00254E00` | `00254DD0` |
| `32CC`<sub>h</sub> | 62 | Clan Primer family A bits for tabs 0-4 (bases at `00D10630`, counts at `00D10640`) | `00315910` | `003154B0` |
| `330C`<sub>h</sub> | 62 | Clan Primer family B bits for tabs 0-4 | `00315B50` | |
| `334C`<sub>h</sub> | 32 | a 256-bit set | `00315A20` | |
| `336C`<sub>h</sub> | 128 | 256 four-bit values, low nibble for even ids | `00315CD0` | |
| `33F4`<sub>h</sub> | 6 | tab 6 (category 5) bits, 48 entries | `00315B50` | |
| `3404`<sub>h</sub> | 512 | bestiary defeat count per entry, stored as count + 1 | | `00315420`, `003154B0` |
| `3604`<sub>h</sub> | 512 | bestiary page-viewed bits, 8 per entry | `00315B50` | |
| `3844`<sub>h</sub> | 4 | tab 7 family A, 30 bits: the achievements already fired ([achievement page](../Steam-And-Achievements/achievements.md)) | `00315910` | `003154B0` |
| `3848`<sub>h</sub> | 4 | tab 7 family B, 30 bits | `00315B50` | |
| `3868`<sub>h</sub> | 4 | the points `00315390` ranks 1-12 against the rank table below | | `00315390`, whose rank `00583D60` writes to the header's `+44`<sub>h</sub> |
| `47B8`<sub>h</sub> | 48 | `i32[12]`: the entry count of each class's derived inventory list | `00252E60` | `00252F70` |
| `47E8`<sub>h</sub> | 8 | the play clock's block copy: `00254CC0` adds each frame's delta and resets it to 0 past `FFFFFFFF80BEFBFF`<sub>h</sub>; `002542B0` reads it back as hours modulo 9999, minutes and seconds | `00254CC0`, `00255040` | `002542B0` |

### The rank table

`00315390` walks the twelve eight-byte rows at `00D105D0`-`00D1062F` (`{u32 points, u8 a, u8 b, u16
text}`) from the last and returns the first row whose three thresholds are all met, as a rank 1-12;
`a` is compared with `00316480()` and `b` with `00316670()`, and the loop returns 1 when no row above
the first is met.

| Rank | Points | `a` | `b` | Text id |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | `4DC`<sub>h</sub> |
| 2 | 700 | 2 | 0 | `4DD`<sub>h</sub> |
| 3 | 8,000 | 4 | 0 | `4DE`<sub>h</sub> |
| 4 | 20,000 | 8 | 0 | `4DF`<sub>h</sub> |
| 5 | 30,000 | 10 | 0 | `4E0`<sub>h</sub> |
| 6 | 40,000 | 12 | 0 | `4E1`<sub>h</sub> |
| 7 | 100,000 | 14 | 0 | `4E2`<sub>h</sub> |
| 8 | 200,000 | 16 | 0 | `4E3`<sub>h</sub> |
| 9 | 250,000 | 24 | 0 | `4E4`<sub>h</sub> |
| 10 | 300,000 | 28 | 0 | `4E5`<sub>h</sub> |
| 11 | 500,000 | 32 | 0 | `4E6`<sub>h</sub> |
| 12 | 1,000,000 | 44 | 30 | `4E7`<sub>h</sub> |

### The spawn-keep images and group banks

A group bank is the `200`<sub>h</sub> bytes at `02099FF0`: `0025D8E0` copies them out in four `80`<sub>h</sub>-byte passes
and `00269A20` copies them back. A spawn-keep image is `20010`<sub>h</sub> bytes, laid out by `00233440`
([spawn placement page](../Enemy-Spawning/enemy-spawning.md)):

Struct SpawnKeepImage base=payload+`E240`<sub>h</sub> size=`20010`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00000`<sub>h</sub> | `u16` | fieldIdA | `02089372` (`00233440` writes, `00233550` restores) |
| `00002`<sub>h</sub> | `u16` | fieldIdB | `02089370` |
| `00010`<sub>h</sub> | `u8[65536] bank2` | the 64 entries of `250`<sub>h</sub> bytes at [0208E698]; `9400`<sub>h</sub> bytes copied, the rest zero |  |
| `10010`<sub>h</sub> | `u8[65536] bank1` | the 64 entries at [0208E690]; written on save, not restored |  |

`00233440` zeroes the image first and copies the banks in `128`<sub>h</sub> passes of `80`<sub>h</sub> bytes; `00233550`
restores bank 2 and the two field ids only.

Before it reaches the pair, `00229B40` copies the header and the payload up to the first group bank
(`E240`<sub>h</sub> bytes: `1C4`<sub>h</sub> passes of `80`<sub>h</sub> and a `40`<sub>h</sub>-byte tail) and the first `8000`<sub>h</sub> bytes of the
battle-state block from the active buffer `002EF640()` to the staging buffer `002EF620()`.

Which pair is used depends on bit 12 of the battle-state block's flag dword (`00236760`, set and
cleared by `0023A390`); `00229B40` takes the bit as its argument from its only caller `003145E0`
(`003147BB`):

| Bit 12 | Capture (`00229B40`, `00584580`) | Restore (`005843E0`) |
|---|---|---|
| clear | bank A at `+E040`<sub>h</sub>, image A at `+E240`<sub>h</sub>, then the metadata record | the record, bank A, image A |
| set | bank B at `+2E250`<sub>h</sub>, image B at `+2E450`<sub>h</sub>, then `002EF510` on the record | bank B and image B when the load mode `00394450()` is not 3 or the header's `+57`<sub>h</sub> bit 0 is set; then bit 1 of the block's `+5B04`<sub>h</sub> is cleared |

`00584210` imports bank A again on the restore path, and `005843E0` ends by copying the record's first
byte to `0208D455`.

### The save-transition metadata record

Struct SaveTransitionRecord base=payload+`4E460`<sub>h</sub> size=`2C`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | mode | `0208D455` as a dword (`00584580`) |
| `04`<sub>h</sub> | `u32` | stamp | `021B28E4` (`002EF3C0`); `003145E0` writes the destination field here (`00314731`) when bit 12 is clear and the field is not 12, and `00584580`'s `002EF3C0` overwrites it unless `003145E0` returned early |
| `08`<sub>h</sub> | `u8[16]` | blockA | battle-state block +`5AE0`<sub>h</sub>-+`5AEF`<sub>h</sub> (`002EF3C0`) |
| `18`<sub>h</sub> | `u8[16]` | blockB | battle-state block +`5AD0`<sub>h</sub>-+`5ADF`<sub>h</sub> (`002EF3C0`, `002EF510`) |
| `28`<sub>h</sub> | `u32` | flags | battle-state block +`5B04`<sub>h</sub> (`002EF3C0`); `002EF510` sets bit 0 from bit 1 of +`18`<sub>h</sub> |

`002EF540` fills the whole record from the `2C`<sub>h</sub> bytes at `021B28E0` during `00229B40`. The restore
`002EF410` copies `+08`<sub>h</sub> to block `+5AE0`<sub>h</sub> and `+28`<sub>h</sub> to `+5B04`<sub>h</sub>; when bit 1 of `+18`<sub>h</sub> is set it
also restores `+5AD0`<sub>h</sub> and calls `003139D0(+20h)`; when bit 0 of `+08`<sub>h</sub> is set it calls
`00304790(+0Ch)` and `003047C0(+10h)` and rewrites `+5B04`<sub>h</sub> with bit 1 set and bit 0 clear.

### The battle-state block

`00238A80` and `00233C10` bind `02EBF190` to image `+4E68C`<sub>h</sub>, payload `+4E48C`<sub>h</sub>, and `00233C10`
checks the magic `05071901`<sub>h</sub> at `+00`<sub>h</sub>. The block's interior is the
[battle-state block field map](../Party/party-data.md); what
the save layer itself does to it:

- `002370C0` resets the block: all `7410`<sub>h</sub> bytes zeroed, the magic written, the words
  `+5A48`<sub>h</sub>-`+5A58`<sub>h</sub> set to `FFFF`<sub>h</sub> and the dwords `+5AC8`<sub>h</sub> and `+5ACC`<sub>h</sub> cleared.
- Both binders then call `0030B6A0`, which rebases the descriptor table at `01EEBCC0` (fifteen rows
  of `58`<sub>h</sub> bytes outside the image: each non-zero offset at `+00`<sub>h</sub>, `+18`<sub>h</sub> and `+28`<sub>h</sub> becomes the
  32-bit truncated sum of the block's address and the offset at `+08`<sub>h</sub>, `+20`<sub>h</sub> and `+30`<sub>h</sub>, and
  `+40`<sub>h</sub> the running total of the `+3C`<sub>h</sub> sizes), zeroes the `200`<sub>h</sub> bytes at block `+57C8`<sub>h</sub> and
  clears the low three bits of the 128 bytes at `+59C8`<sub>h</sub>.
- Before a capture, `00234ED0` (called by `00229B40` at `00229B71` and by `005844A0` at `00584510`)
  copies each of the 40 members' selected gambit bank, `+5B10h + (3k + [+7370h + 4k]) * 34h`, to
  `+90h + k * 1C8h`. That is where the older block layout keeps it, and where `00235AF0` reads it
  from when it migrates an older block on load.
- Bits 12, 13 and 14 of the flag dword at `+04`<sub>h</sub> are read by `00236760`, `00236740` and `00236780`
  and copied into the header's `+57`<sub>h</sub> by `00583D60`.

## Related

- [Save file format](save-file-format.md): the container, the header and the four buffers.
- [Saving and loading](saving-and-loading.md): when the payload is captured, written and restored.
- [Game settings](game-settings.md): the options record inside the image-backed block.
- [Zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md): the transition record's users.
- [Spawn placement and retirement](../Enemy-Spawning/enemy-spawning.md): the spawn-keep entries.
- [Persistent flag banks](../Story-Events-And-Hunts/story-flags.md): the flag accessors.
- [The battle-state block field map](../Party/party-data.md).
- [Steam integration and achievement catalogue](../Steam-And-Achievements/achievements.md).
