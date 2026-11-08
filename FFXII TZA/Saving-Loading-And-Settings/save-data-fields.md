---
title: "Save data fields: the regions of the save payload, who writes and reads each, and the access table"
kind: "reference"
category: "Saving, loading and settings"
addresses: "0x002EF2B0, 0x002EF2D0, 0x00253970, 0x00253A80, 0x00229B40, 0x005843E0, 0x00584580, 0x005844A0, 0x00233440, 0x00233550, 0x0025D8E0, 0x00269A20, 0x002EF3C0, 0x002EF410, 0x00238A80, 0x00233C10, 0x002370C0, 0x00583D60"
---

## What it lists

The save image is `0x56690` bytes: a `0x200`-byte header (see the [save file format page](save-file-format.md))
followed by the `0x56490`-byte persistent payload. `0x002EF2B0` returns the payload's address as
`0x002EF640() + 0x200`, and every offset on this page is relative to that payload. An instruction that
works on the whole buffer shows an offset `0x200` larger: `0x00229B40`'s `+0x4E68C` is payload `+0x4E48C`,
and `0x002EF390`'s `+0xC00` is payload `+0xA00`.

The table below lists the payload's regions with the functions that write and read each one. The
companion table [`save-data-fields.tsv`](save-data-fields.tsv) holds every access to the payload: through the
buffer getters `0x002EF640` and `0x002EF2B0` and the pointers passed on from them, through the block pointers
`0x02EBF190` and `0x020927C0`, directly at the buffer `0x02164280`, and the block moves (the clears, the copies and the
slot file's read and write).

The payload is one block the game keeps in memory and uses while playing: the quest bits, the story flags, the
zone-change record, the spawn records and the party data all live inside it. A save writes the whole block to the slot
file, and a load reads it back in one piece.

### The regions

| Payload offset | Size | Region | Written by | Read by |
|---|---|---|---|---|
| `+0x00000` | 353424 | the whole payload, moved as one block with the header | `0x002EF5F0` and `0x002EF650` clear the image; the load's read (`0x00580EB0`, kind 9) fills it from the slot file | `0x002EF570` copies the image to the backup `0x022676C0`; the autosave write (`0x0057E310`, kind 8) sends it to the slot file |
| `+0x00000` | 512 | script operand bank, `i16[256]`, reached through the slot pointer `0x02098E58` that `0x0026C8C0` sets to `0x002EF2B0()` | `0x0026ABA0`; `0x002EF2D0` clears the first `0x1538` bytes | `0x00264640` |
| `+0x00200` | 3584 | the script-global variable space up to the quest arrays, addressed by the scripts' own descriptors ([the storage-class page](../Scripts-And-Script-Commands/script-variables.md)) | scripts | `0x002EF390` tests `+0xA00 + i == 1` |
| `+0x01000` | 32 | quest ordered bits, one per quest id | `0x0046B3F0` (`setquestorder`); `0x0046B290` also clears a bit here, but of quest `id & 7` (it re-splits the bit index at `0x0046B2EF`), so only quests 0-7 are un-ordered that way | `0x0046B240` (`isquestorder`), `0x0046B0F0` (the count) |
| `+0x01020` | 32 | quest cleared bits | `0x0046B290` (`setquestclear`) | `0x0046B1A0` (`isquestclear`), `0x0046B020` (the count) |
| `+0x01040` | 4 | a counter of `setquestclear` calls with a non-zero value, incremented while below `0xFFFF` | `0x0046B290` | `0x0046B0B0` (`getquestcleartotal`) |
| `+0x01044` | 32 | the zone transition record ([zone changes page](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) | the writers listed under the record below | the readers listed under the record below |
| `+0x01064` | 256 | quest scenario flag, `u8` per quest id | `0x0046B490` (`setquestscenarioflag`) | `0x0046B180` (`getquestscenarioflag`) |
| `+0x01164` | 512 | `u16` per quest id: the field id (`0x003148F0()`) when the quest was first ordered | `0x0046B3F0`, `0x0046B350` | `0x0046B0D0` |
| `+0x01364` | 32 | quest ok bits | `0x0046B380` (`setquestok`) | `0x0046B1F0` (`isquestok`) |
| `+0x01384` | 8 | story flag bank Bank64A, 64 bits ([Story flags](../Story-Events-And-Hunts/story-flags.md)) | `0x0032AC70` | `0x0032A9A0` |
| `+0x0138C` | 8 | story flag bank Bank64B, 64 bits | `0x0032ACF0` | `0x0032AA00` |
| `+0x013B4` | 256 | story flag bank Bank2048, 2048 bits | `0x0032ABF0` | `0x0032A930` |
| `+0x014B4` | 64 | story flag bank Bank512, 512 bits: ids 0-255 in the first 32 bytes, ids 256-511 in the next | `0x0032AD70`, `0x0032ADF0` | `0x0032AA60`, `0x0032AAD0` |
| `+0x014F4` | 64 | the primary story flag bank, ids 2-511 | `0x0032AB60` | `0x0032A8A0` |
| `+0x01534` | 1 | the music track override, used while `+0x1063` bit `0x40` is set | `0x0026A720`, `0x002628B0` | `0x0026DE20`, `0x0025D9E0`, `0x00261F90` |
| `+0x01535` | 1 | a byte the options apply `0x002DDA30` writes as 1 and the verb handler `0x0050D180` writes from its operand, through `0x002EF370` | `0x002EF370` | |
| `+0x02000` | 24576 | a copy of the party block's first `0x6000` bytes | `0x00229B40`, `0x005844A0` | `0x00235AF0`; `0x002EF4A0` copies the span out to `0x021B290C` |
| `+0x08000` | 18456 | the image-backed state block, `*(0x020927C0)` | see its table below | |
| `+0x0E000` | 4 | the plain CRC of image `+0x8`-`+0xE1FF` (`0x003BB220`), whose complement the header carries at `+0x00`; computed over the active buffer `0x002EF640()` but stored into the buffer `0x00583D60`'s third argument selects (the staging buffer when it is not 0, as `0x003145E0` passes through `0x005844A0`) | `0x00583D60` | |
| `+0x0E040` | 512 | group persistent bank A, a copy of `0x02099FF0` | `0x0025D8E0` from `0x00229B40` and `0x00584580` | `0x00269A20` from `0x005843E0` and `0x00584210`; `0x005844A0`; `0x002EF7C0` copies the bank out to `0x021C8B80` |
| `+0x0E240` | 131088 | spawn-keep image A | `0x00233440` from `0x00229B40` and `0x00584580` | `0x00233550` from `0x005843E0`; `0x002EF740` copies `0x20000` bytes out to `0x021C8D80` |
| `+0x2E250` | 512 | group persistent bank B | `0x0025D8E0` from `0x00229B40` (`0x00229CCA`-`0x00229CD1`, when its argument is non-zero; bank A when it is 0) and `0x00584580` (`0x005845CE`-`0x005845D5`, when `0x00236760()` is non-zero; bank A when it is 0) | `0x00269A20` from `0x005843E0` (`0x0058444B`-`0x00584452`); `0x00229B40` writes this bank through `0x0025D8E0` and does not read it |
| `+0x2E450` | 131088 | spawn-keep image B | `0x00233440` from `0x00229B40` (`0x00229CD6`, `0x00229CF2`, when its argument is non-zero; image A when it is 0) and `0x00584580` (`0x005845DA`-`0x005845E1`, in the same branch as bank B) | `0x00233550` from `0x005843E0` (`0x00584457`-`0x0058445E`, after bank B); `0x00229B40` writes this image through `0x00233440` and does not read it |
| `+0x4E460` | 44 | the save-transition metadata record | `0x002EF540` (run by `0x00229B40` on the staging buffer's record, `0x00229CF7`-`0x00229CFE`), `0x002EF3C0`, `0x002EF510`, `0x00584580`, `0x003145E0` | `0x002EF410`, `0x005843E0`, `0x00584210`; `0x00229B40` reads no byte of it, since its copies end at payload `+0xE040` and start again at `+0x4E48C` |
| `+0x4E48C` | 29712 | the party block, `*(0x02EBF190)` ([its field map](../Party/party-data.md)) | bound by `0x00238A80` and `0x00233C10`, cleared whole by `0x002370C0`; its accesses through `0x02EBF190` are on [Party data](../Party/party-data.md) | the same page |

Each spawn-keep image is preceded by its group bank, so pair A and pair B are two `0x20210`-byte
blocks at `+0xE040` and `+0x2E250`, and `0x005844A0` clears both pairs with one `memset` of `0x40420` bytes
when its fourth argument is 0 and its fifth is 0.

`0x005844A0` first calls `0x00283270(1)` and the header finaliser `0x00583D60(0, 0, d)`, with `d` its fourth
argument (`0x005844AA`-`0x005844BE`). With `d` not 0 it neither clears the pairs nor touches the record
(`0x005844C3`-`0x005844CC`). With `d` 0 and the fifth argument not 0 it runs `0x002EF510` on the record at payload
`+0x4E460` instead of the clear (`0x005844F0`-`0x005844F7`).

Then, when the first byte of the party block in the active buffer (payload `+0x4E48C`) is not 0, it runs
`0x00234ED0` and copies the block's first `0x6000` bytes to payload `+0x2000` of the active buffer, `0xC0` passes of
`0x80` bytes (`0x005844FC`-`0x00584572`); with that byte 0 it returns without the copy (`0x0058450E`).

## Columns

The companion table has one row per access site:

| Column | Meaning |
|---|---|
| `offset` | the payload-relative offset the instruction reaches |
| `region` | the region from the table above that contains the offset |
| `function` | the function containing the instruction |
| `site` | the instruction's address |
| `kind` | `r` read, `w` write, `rw` read-modify-write, `addr` the address is formed (`lea`) and passed on, `set` a clear over the span the instruction cell gives, `copy` a block move whose length and other end the instruction cell gives, `range` a span whose own table the instruction cell names |
| `instruction` | the instruction text, as disassembled from the executable |
| `via` | empty when the function computes the address from the buffer getter `0x002EF640` or `0x002EF2B0` itself; `argN from F at S` when the pointer came in as argument N (0 = `rcx`, 1 = `rdx`, 2 = `r8`, 3 = `r9`) from the caller F at the call site S, `argN+0xK` when it came in offset by K; `0x02EBF190` or `0x020927C0` when the function loads that block pointer; `0x02164280` for a direct reference to the buffer; `file kind 8` and `file kind 9` for the slot file's write and read |
| `note` | what the access does, where the instruction alone does not show it (a bulk copy or clear and its size) |

The party block's accesses through `0x02EBF190` are not repeated here: the table carries one `range` row for the
block, and [the block's field map](../Party/party-data.md) lists them field by field; the copies and clears that reach
it from the buffer are on that page too.

## Data

### The span a new game clears

`0x002EF2D0` zeroes the first `0x1538` bytes of the payload and `0x002EF290` returns that length for the
header's `+0x5C`. The span holds the operand bank, the script globals, the quest arrays, the zone
transition record, the flag banks and the music override; the last two bytes, `+0x1536` and
`+0x1537`, have no access in the table.

### The zone transition record

The record at `+0x1044` is written by `0x003145E0` when a zone change is staged and reset by
`0x00314970`:

Struct ZoneTransitionRecord base=payload+`0x1044` size=`0x20`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | destinationField | the field being entered; also `0x01EED064` (`0x003145E0`) |
| `+0x04` | `i32` | destinationEntrance | the entrance index (`0x003145E0`, `0x00314D80`) |
| `+0x08` | `i32` | previousField | the old destinationField (`0x003145E0`) |
| `+0x0C` | `i32` | previousEntrance | the old destinationEntrance (`0x003145E0`) |
| `+0x10` | `u32` | mode | the mode argument (`0x003145E0`, `0x00314DA0`) |
| `+0x14` | `i32` | persistenceGroup | `0x00264F90`(destinationField) (`0x003145E0`) |
| `+0x18` | `i32` | transitionField | destinationField again; `0x00314530` copies it on restore (`0x003145E0`) |
| `+0x1C` | `u8` | runtimeParameter | 0 to 2, set by `0x0026D910` while initState is 0, passed to `0x00180620` |
| `+0x1D` | `u8` | initState | 1 from `0x00268320` and `0x0026D8F0`, cleared by `0x0026D910` |
| `+0x1E` | `u8` | flags1 | bit `0x20` cleared by `0x003145E0`, set by `0x00314530` |
| `+0x1F` | `u8` | flags2 | bit `0x40`: the music override at `+0x1534` is in force (`0x0026A720`, `0x0026DE20`) |

With load mode 3 and the header's flag bit `0x1` clear, `0x00584210` copies the five dwords `+0x1044` to
`+0x1057` into the header's `+0x80` to `+0x93` (`0x0058427B`-`0x005842B1`), zeroes `destinationEntrance`
(`0x005842B7`) and stores `0x483` as `destinationField` through `0x00314DC0` (`0x005842D7`-`0x005842DF`); in
any other mode with the flag set it copies them back (`0x00584325`-`0x00584362`) (see the
[save file format page](save-file-format.md)).

The record's writers are `0x003145E0`, `0x00314970`, `0x00314530`, `0x0026D910`, `0x0026A720`, `0x002628B0`, `0x00268320`,
`0x0026D8F0`, `0x00280140`, `0x00584210` and the field setters `0x003149E0`, `0x00314A00`, `0x00314B80`, `0x00314BB0`, `0x00314BE0`,
`0x00314C40`, `0x00314C70`, `0x00314CA0`, `0x00314CD0`, `0x00314D00`, `0x00314D80`, `0x00314DA0` and `0x00314DC0`.

Its readers are
`0x003148F0`, `0x00314870`, `0x00314850`, `0x003148D0`, `0x003148B0`, `0x00314910`, `0x00314530`, `0x003145E0`, `0x0026D910`, `0x0026DB30`,
`0x0026DE20`, `0x0025ACA0`, `0x0025D9E0`, `0x00261F90`, `0x002620E0`, `0x00265920`, `0x00584210` and the field getters `0x00314A60`,
`0x00314A80`, `0x00314AA0`, `0x00314AC0`, `0x00314AE0`, `0x00314B00`, `0x00314B20`, `0x00314B40` and `0x00314B60`.

### The image-backed state block

`0x00253970` binds `0x02092758` to the image itself, the header (`0x0025397E`), and `0x020927C0` to image `+0x8200`,
payload `+0x8000` (`0x00253990`), both from the active buffer `0x002EF640()`, and `0x00253A80` initialises the
block in four steps:

1. it zeroes the `0x58` header bytes at `[0x02092758]` (`0x00253A86`-`0x00253A93`) and all `0x4818` bytes of the
   block at `[0x020927C0]` (`0x00253A98`-`0x00253AA7`);
2. it writes six header dwords at `+0x58`-`+0x6C`: `0x20050223` from `0x002EF2A0`, `0x1538` from
   `0x002EF290`, the party block's magic `0x05071901` from `0x00235E90` and its size `0x7410` from
   `0x00235E80`, then the block magic `0x0131F3EA` and its size `0x4818`, into the header of the active buffer
   `0x002EF640()` (`0x00253AAC`-`0x00253AFB`);
3. it runs `0x00253240(i, 1)` for the twelve classes, `i` from 0 to 11 (`0x00253B02`-`0x00253B13`), keeps only bit
   `0x1` of byte `+0x3244` and clears bit `0x1` of byte `+0x3245` (`0x00253B1C`, `0x00253B23`), and installs the
   in-game options defaults with `0x002DDE60` (`0x00253B2A`, [Game settings](game-settings.md));
4. it zeroes `+0x30` for 500 bytes, `+0x3244` for `0x80`, `+0x32C4` for 8 and `+0x224` for `0x3020`.
   It calls the empty `0x0016D6A0` before the last, which is a tail jump to `memset` (`0x00253B36`-`0x00253B84`).

Offsets in this table are block offsets; add `0x8000` for the payload offset.

| Block offset | Size | Content | Written by | Read by |
|---|---|---|---|---|
| `+0x0008` | 40 | the in-game options record `0x0215E6E0` ([game settings page](game-settings.md)) | `0x002DDE60` | the option getters |
| `+0x0030` | 64 | `u16[32]`, class 6 of the typed store, index clamped to 31 | `0x002527B0`, cleared by `0x00252610` | `0x002526F0` |
| `+0x0070` | 32 | `u8[32]`, class 7 | `0x002527B0`, `0x00252610` | `0x002526F0` |
| `+0x0090` | 404 | `u32[101]`, class 8, index clamped to 100 | `0x002527B0`, `0x00252610` | `0x002526F0` |
| `+0x0224` | 12320 | navigation-map exploration bitmaps: 385 entries of 32 bytes, indexed by `0x003779F0(field)` ([area flags page](../World-Areas-And-Travel/area-flags-navimapdata.md)) | `0x003C60F0`, `0x003C8670`, `0x003C5E50` copy the live block `0x02B45978` in | `0x002551B0` |
| `+0x3244` | 128 | a bit set indexed by a `u16`, entry n at bit value `1 << (n & 7)` of byte n >> 3 (`0x00252D40`). Entries 1-8 are the inventory category bits, set when a category's derived list is non-empty (`0x002CD650`) and cleared together by `0x00253480` after it runs `0x00253240` for lists 0-11 (`0x002534AA`, `0x002534B1`); `0x002CD510` sets 13 entries between 42 and 58 (`0x002CD519`-`0x002CD635`) | `0x00252D40`; zeroed by `0x00253A80` (`0x00253B47`-`0x00253B56`) | `0x00252D10` |
| `+0x32C4` | 8 | a bit set indexed by a `u16` | `0x00254E00` | `0x00254DD0` |
| `+0x32CC` | 62 | Clan Primer family A bits for tabs 0-4 (bases at `0x00D10630`, counts at `0x00D10640`) | `0x00315910` | `0x003154B0` |
| `+0x330C` | 62 | Clan Primer family B bits for tabs 0-4 | `0x00315B50` | `0x003156E0`, `0x00315B50` |
| `+0x334C` | 32 | a 256-bit set | `0x00315A20` | `0x00315620`, `0x00315A20` |
| `+0x336C` | 128 | 256 four-bit values, low nibble for even ids | `0x00315CD0` | `0x00315470`, `0x00315CD0` |
| `+0x33F4` | 6 | tab 6 (category 5) bits, 48 entries | `0x00315B50` | `0x003156E0`, `0x00315B50` |
| `+0x3404` | 512 | bestiary defeat count per entry, stored as count + 1 | `0x00315820` (`0x0031588E`, the count), `0x00315A90` (`0x00315AB7`, 1), `0x00316930` (`0x00316A0C`, 2) | `0x00315420`, `0x00315820`, `0x00315A90`, `0x00316930` |
| `+0x3604` | 512 | bestiary page-viewed bits, 8 per entry | `0x00315AD0`, `0x00315B50` | `0x00315670`, `0x003156E0`, `0x00315AD0`, `0x00315B50` |
| `+0x3844` | 4 | tab 7 family A, 30 bits: the achievements already fired ([achievement page](../Steam-And-Achievements/achievements.md)) | `0x00315910`, `0x00315E90` (`0x00316069`), `0x00316A50` (`0x00316ADB`, `0x00316B38`) | `0x003154B0`, `0x00315E90`, `0x00316A50` |
| `+0x3848` | 4 | tab 7 family B, 30 bits | `0x00315B50` | `0x003156E0`, `0x00315B50` |
| `+0x3868` | 4 | the points `0x00315390` ranks 1-12 against the rank table below | `0x00316BF0`, the counter store, for counter kind 17 (`0x384C` plus the kind's row offset, `0x00316C04`) | `0x00315390`, whose rank `0x00583D60` writes to the header's `+0x44` |
| `+0x47B8` | 48 | `i32[12]`: the entry count of each class's derived inventory list | `0x00252E60` | `0x00252F70` |
| `+0x47E8` | 8 | the play clock's block copy: `0x00254CC0` adds each frame's delta and resets it to 0 past `0xFFFFFFFF80BEFBFF`; `0x002542B0` reads it back as hours modulo 9999, minutes and seconds | `0x00254CC0`, `0x00255040` | `0x002542B0` |

### The rank table

`0x00315390` walks the twelve eight-byte rows at `0x00D105D0`-`0x00D1062F` (`{u32 points, u8 a, u8 b, u16
text}`) from the last and returns the first row whose three thresholds are all met, as a rank 1-12;
`a` is compared with `0x00316480()` and `b` with `0x00316670()`, and the loop returns 1 when no row above
the first is met.

| Rank | Points | `a` | `b` | Text id |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | `0x4DC` |
| 2 | 700 | 2 | 0 | `0x4DD` |
| 3 | 8,000 | 4 | 0 | `0x4DE` |
| 4 | 20,000 | 8 | 0 | `0x4DF` |
| 5 | 30,000 | 10 | 0 | `0x4E0` |
| 6 | 40,000 | 12 | 0 | `0x4E1` |
| 7 | 100,000 | 14 | 0 | `0x4E2` |
| 8 | 200,000 | 16 | 0 | `0x4E3` |
| 9 | 250,000 | 24 | 0 | `0x4E4` |
| 10 | 300,000 | 28 | 0 | `0x4E5` |
| 11 | 500,000 | 32 | 0 | `0x4E6` |
| 12 | 1,000,000 | 44 | 30 | `0x4E7` |

### The spawn-keep images and group banks

A group bank is the `0x200` bytes at `0x02099FF0`: `0x0025D8E0` copies them out in four `0x80`-byte passes
and `0x00269A20` copies them back. A spawn-keep image is `0x20010` bytes, laid out by `0x00233440`
([spawn placement page](../Enemy-Spawning/enemy-spawning.md)):

Struct SpawnKeepImage base=payload+`0xE240` size=`0x20010`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00000` | `u16` | fieldIdA | `0x02089372` (`0x00233440` writes, `0x00233550` restores) |
| `+0x00002` | `u16` | fieldIdB | `0x02089370` |
| `+0x00010` | `u8[65536]` | bank2 | the 64 entries of `0x250` bytes at [`0x0208E698`]; `0x9400` bytes copied, the rest zero |
| `+0x10010` | `u8[65536]` | bank1 | the 64 entries at [`0x0208E690`]; written on save, not restored |

`0x00233440` zeroes the image first and copies the banks in `0x128` passes of `0x80` bytes; `0x00233550`
restores bank 2 and the two field ids only. `0x00233440` skips a bank whose pointer is null, so its part of the
image stays zero (`0x00233466`, `0x002334CD`), and stores the two field ids either way (`0x00233529`-`0x0023353A`);
`0x00233550` skips the copy when the bank 2 pointer is null and still restores the two field ids (`0x0023355A`,
`0x002335B9`-`0x002335C7`).

Before it reaches the pair, `0x00229B40` copies the header and the payload up to the first group bank
(`0xE240` bytes: `0x1C4` passes of `0x80` and a `0x40`-byte tail) and the first `0x8000` bytes of the
party block from the active buffer `0x002EF640()` to the staging buffer `0x002EF620()`.

The party block part goes first (`0x00229BE4`-`0x00229C41`) and the `0xE240` bytes after it (`0x00229C43`-`0x00229CC2`).
Before both, `0x00229B40` runs `0x00234ED0` (`0x00229B71`) and copies the block's first `0x6000` bytes to payload
`+0x2000` of the active buffer, `0xC0` passes of `0x80` bytes (`0x00229B7B`-`0x00229BE2`), so the staging copy carries
that fresh copy. The `0x8000` bytes run `0xBF0` bytes past the `0x7410`-byte block, to image `+0x5668C`.

`0x002EF620` returns the fixed buffer `0x021BA940`, so the null test at `0x00229B57` never ends the capture early. The
two `0x0016D6A0(0)` calls (`0x00229B6C`, `0x00229D05`) reach a `ret 0` stub.

Which pair is used depends on bit `0x1000` of the party block's flag dword (`0x00236760`, set and
cleared by `0x0023A390`); `0x00229B40` takes the bit as its argument from its only caller `0x003145E0`
(`0x003147BB`):

| Bit `0x1000` | Capture (`0x00229B40`, `0x00584580`) | Restore (`0x005843E0`) |
|---|---|---|
| clear | bank A at `+0xE040`, image A at `+0xE240`, then the metadata record | the record, bank A, image A |
| set | bank B at `+0x2E250`, image B at `+0x2E450`, then `0x002EF510` on the record (`0x00584580`); `0x00229B40` runs `0x002EF540` on the record on this path too, as on the clear path (`0x00229CF7`-`0x00229CFE`) | bank B and image B when the load mode `0x00394450()` is not 3 or the header's `+0x57` bit `0x1` is set; then bit `0x2` of the block's `+0x5B04` is cleared |

`0x00584580` captures into the staging buffer `0x002EF620()` (`0x00584586`) and on both paths stores `0x0208D455`,
sign-extended, as the record's `+0x00` (`0x005845BB`-`0x005845C2`, `0x005845FC`-`0x00584603`). With bit `0x1000` set it
also runs `0x002EF7C0` and `0x002EF740` (`0x005845F2`, `0x005845F7`), which copy the active buffer's bank A (`0x200`
bytes, payload `+0xE040`) and `0x20000` bytes of its image A (payload `+0xE240`) to `0x021C8B80` and `0x021C8D80`.

`0x00584210` imports bank A again on the restore path, and `0x005843E0` ends by copying the record's first
byte to `0x0208D455`.

### The save-transition metadata record

Struct SaveTransitionRecord base=payload+`0x4E460` size=`0x2C`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | mode | `0x0208D455` as a dword (`0x00584580`) |
| `+0x04` | `u32` | stamp | `0x021B28E4` (`0x002EF3C0`); `0x003145E0` writes the destination field here (`0x00314731`) when bit `0x1000` is clear and the field is not 12, and `0x00584580`'s `0x002EF3C0` overwrites it unless `0x003145E0` returned early |
| `+0x08` | `u8[16]` | blockA | party block `+0x5AE0`-`+0x5AEF` (`0x002EF3C0`) |
| `+0x18` | `u8[16]` | blockB | party block `+0x5AD0`-`+0x5ADF` (`0x002EF3C0`, `0x002EF510`) |
| `+0x28` | `u32` | flags | party block `+0x5B04` (`0x002EF3C0`); `0x002EF510` sets bit `0x1` from bit `0x2` of `+0x18` |

`0x002EF540` fills the whole record from the `0x2C` bytes at `0x021B28E0` during `0x00229B40`. The restore
`0x002EF410` copies `+0x08` to block `+0x5AE0` and `+0x28` to `+0x5B04`; when bit `0x2` of `+0x18` is set it
also restores `+0x5AD0` and calls `0x003139D0(+0x20)`; when bit `0x1` of `+0x08` is set it calls
`0x00304790(+0x0C)` and `0x003047C0(+0x10)` and rewrites `+0x5B04` with bit `0x2` set and bit `0x1` clear.

### The party block

`0x00238A80` and `0x00233C10` bind `0x02EBF190` to image `+0x4E68C`, payload `+0x4E48C`, `0x00233C10` only while the
pointer is null (`0x00233C20`-`0x00233C33`), and with the pointer set `0x00233C10`
checks the magic `0x05071901` at `+0x00` (`0x00233C4D`). The block's interior is the
[party block field map](../Party/party-data.md); what
the save layer itself does to it:

- `0x002370C0` resets the block: all `0x7410` bytes zeroed, the magic written, the words
  `+0x5A48`-`+0x5A58` set to `0xFFFF` and the dwords `+0x5AC8` and `+0x5ACC` cleared.
  - It also clears the inventory counts and empties the twelve inventory lists of `[0x020927C0]` (`0x003047F0`
    at `0x002370E5`, ending in `0x00253480`: each list filled with `0xFFFF` and its count zeroed through
    `0x00253240(i, 1)`, the category bits of `+0x3244` other than bit `0x1` and bit `0x1` of `+0x3245` cleared).
- Both binders then call `0x0030B6A0`, which rebases the descriptor table at `0x01EEBCC0` (fifteen rows
  of `0x58` bytes outside the image: each non-zero offset at `+0x00`, `+0x18` and `+0x28` becomes the
  32-bit truncated sum of the block's address and the offset at `+0x08`, `+0x20` and `+0x30`, and
  `+0x40` the running total of the `+0x3C` sizes), zeroes the `0x200` bytes at block `+0x57C8` and
  clears the low three bits of the 128 bytes at `+0x59C8`.
- Before a capture, `0x00234ED0` (called by `0x00229B40` at `0x00229B71` and by `0x005844A0` at `0x00584510`)
  copies each of the 40 members' selected gambit bank, `+0x5B10 + (3k + [+0x7370 + 4k]) * 0x34`, to
  `+0x90 + k * 0x1C8`. On load, when the saved block differs from the live one, `0x00235AF0` copies it
  back as the member's bank 0 and sets the selected bank to 0 ([save file format](save-file-format.md)).
- Bits `0x1000` (Trial Mode stash), `0x2000` (New Game+) and `0x4000` (New Game-) of the flag dword at `+0x04`
  are read by `0x00236760`, `0x00236740` and `0x00236780` and set in the header's `+0x57` bits `0x1`, `0x2` and `0x4` by
  `0x00583D60` with `or`, which never clears them (`0x00583F63`-`0x00583F7D`; [New Game+ and New
  Game-](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)).

## Related

- [Save file format](save-file-format.md): the container, the header and the four buffers.
- [Saving and loading](saving-and-loading.md): when the payload is captured, written and restored.
- [Game settings](game-settings.md): the options record inside the image-backed block.
- [Zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md): the transition record's users.
- [Spawn placement and retirement](../Enemy-Spawning/enemy-spawning.md): the spawn-keep entries.
- [Story flags](../Story-Events-And-Hunts/story-flags.md): the flag banks and their accessors.
- [The party block field map](../Party/party-data.md).
- [Steam integration and achievement catalogue](../Steam-And-Achievements/achievements.md).
- [`image-backed-state-block-accesses.tsv`](image-backed-state-block-accesses.tsv): every access to the
  image-backed state block through its pointer `[0x020927C0]`, one row per instruction (32 rows).
- [`save-payload-accesses.tsv`](save-payload-accesses.tsv): every access to the payload, one row per
  instruction, with the way the payload's address reached it (1,721 rows).
- [`spawn-keep-image-accesses.tsv`](spawn-keep-image-accesses.tsv): every access to the spawn-keep image at
  payload `+0xE240`, by its offset in the image (37 rows).

[`save-payload-accesses.tsv`](save-payload-accesses.tsv) and [`save-data-fields.tsv`](save-data-fields.tsv) overlap:
409 rows of each are the same accesses (site, offset, kind and instruction). The access table's other 1,312 rows
reach the party block (`+0x4E48C` to `+0x5589B`, 1,117 sites), which the companion table gives as one `range` row.
The companion table's other 15 rows are ten block moves (six at the buffer `0x02164280`, four through the slot file)
and five reads at `0x02164280`, which the access table does not follow.

In these access tables, `function`, `name` and `site` give the function, its name and the instruction's address,
`disp` the offset the instruction reaches from the start of the block, the payload or the spawn-keep image, `kind` a
read (`r`), a write (`w`), both (`rw`) or the address taken (`addr`), and `instruction` the instruction itself.
`route` says how the address reached the instruction:

- `gptr 0x020927C0`: the block reached through the pointer stored at `0x020927C0`;
- `seed`: the function reaches the payload itself, not through an argument; `argN+0xK<F@S`: the payload's address
  plus K came in as argument N (0 = `rcx`, 1 = `rdx`, 2 = `r8`, 3 = `r9`) from F's call at S;
- `embed SavePayload+0xE240`: the spawn-keep image at payload `+0xE240`.

In the payload table, `note` is `idx` where the instruction adds an index register, so `disp` is the offset at index
0.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Story event quest hunt: `0x00314910` is called by `0x001ED240`; those functions are documented on
  [model effects and motion commands](../Graphics/model-effects-and-motion-commands.md).
