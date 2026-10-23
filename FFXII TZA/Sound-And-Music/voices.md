---
title: "Voices: the voice packs a cutscene loads, the sixty-four voice slots, the English or Japanese choice, and the verbs that play, stop and pan a line"
kind: "system"
category: "Sound and music"
addresses: "0x02B5D0B0, 0x003EA0D0, 0x003E9F80, 0x003E9C10, 0x003E9780, 0x003581B0, 0x002DDE20, 0x002DF690"
---

## What the player sees

- Cutscenes speak in English or Japanese, by the Config setting.
- A line plays when its scene reaches it and can be panned left or right as the speaker moves.
- The Voice volume row sets how loud the lines are.
- Field maps play no cutscene voice; battle shouts come from the battle-voice banks ([Sound banks](sound-banks.md)).

## How it works

### The slots

The voice slots are 64 records of `0x40` bytes at `0x02B5D0B0`, global to every script (`0x003E9B10` builds them).
Slot `k` always holds sub-file `k` of the calling event's pack:

| Field offset | Holds |
|---|---|
| `+0x00` | the slot's own number, the pack sub-file it loads |
| `+0x04` | the state: 0 free, 1 parked, 2 loading, 3 ready, 4 freed while loading, 5 one of two tables delivered |
| `+0x05` | the event manager that loaded it |
| `+0x20`, `+0x28` | the loaded `.vpcjp` and `.vpc` sub-files |
| `+0x30` | the table in use, chosen by the language |

### The packs

`0x003E9F80` loads a slot only for event managers 1-3: `0x0032F360` refuses managers 4 and up, and manager 0 answers -1
because `0x0032FCA0` loads it as kind 5 and blanks its directory (`0x0032FFAA`, `0x0032FFFC`), so field maps load no voice
pack. The event's pack directories, `0x208` bytes each, are read by `0x0032FCA0` (`0x0032FF3A`-`0x0032FFE2`):

- kind 8, `plan_master\<language>\event\...\<event>.vpc`, into `0x022C6EE8`;
- kind 37, the `.vpcjp`, into `0x022C6EC0`.

Both tables of a slot are always loaded (`0x003EA0D0`); the language only chooses which one the verbs use. Kind 37 comes
from the `in` folder, or the `ch` folder for the Korean and Chinese builds (`0x002DFE74`).

### The language

`0x002DDE20` answers bit 10 of the options record `*0x0215E6E0 + 4`. Clear plays the `.vpc` and set plays the `.vpcjp`
(`0x002DEBB0`). Options command `0x10` writes the bit (`0x002DE2F0`, `0x002DE2FD`); a new options record sets it for the
Japanese, Korean and Chinese builds (`0x002DDF24`-`0x002DDF55`).

### The cue word

A script names a line as `slot << 24 | index`. `0x003E9C10` plays it only when the slot is ready and the index is below
its table's count (`0x003E9C10`). It opens a stream on the stream controller (`0x002DF660`) and stores the volume, pan and
a pending bit in the cue entry.

| Cue entry field | Holds |
|---|---|
| `+0x08` bits 0-23 | the bank's offset |
| `+0x08` bits 24-30 | the volume, 0-127 |
| `+0x08` bit 31 | pending start |
| `+0x0C` bits 0-23, byte `+0x0F` | the bank's size, the pan |
| `+0x10`, `+0x14` | the stream id, the load handle |

### Starting a line

`0x003E9780` runs at the end of the request pump `0x0032E070` (`0x0032E2AA`). For each ready slot and each cue with a stream:

1. When its load request is done, the pending bit is set and the main loop is in mode 2 (`0x02064AD3`), it starts the
   stream with `0x002DF680(stream, pan, volume)` (`0x003E980B`-`0x003E9832`).
2. When the stream has stopped sounding, it clears the cue (`0x003E985C`-`0x003E9864`).

A line asked for again while it still plays is not restarted: no new stream is opened and the pending bit is dropped
when the old one ends.

### The verbs

| Verb | Id | Does | Calls in event scripts |
|---|---|---|---:|
| `voiceread(slot)` | `0x085` | loads a slot (`0x0034EE40`) | 389 |
| `voiceread_20a(slot, flag)` | `0x20A` | the same with a choice of allocator | 171 |
| `voicereadsync(slot)` | `0x086` | waits while loading | 552 |
| `voiceplay(cue)` | `0x087` | plays at pan `0x40`, volume `0x7F` | 262 |
| `voiceplay_b5(cue, pan, volume)` | `0x0B5` | plays with pan and volume | 9 |
| `voiceplay_28b(speaker, cue)` | `0x28B` | plays at pan `0x40`, volume `0x7F` | 2,218 |
| `voiceplay_28c(speaker, cue, pan, volume)` | `0x28C` | plays with pan and volume | 42 |
| `voicestandby(cue)` | `0x28D` | opens the stream without starting it | 1,965 |
| `voicestop(cue)` | `0x088` | waits for the load, then closes the stream (`0x003EA2C0`) | 41 |
| `voicesync(cue)` | `0x089` | waits while the line plays | 387 |
| `voicedispose(slot)` | `0x08C` | stops every line of the slot and frees it | 628, and 11 in field maps |
| `voicepan(cue, pan)`, `voicechangepan(cue, frames, pan)` | `0x0B1`, `0x0B4` | pan, at once or over frames, once the line has started | 10, 8 |
| `voicevolume(cue, volume)`, `voicechangevolume(cue, frames, volume)` | `0x0B2`, `0x0B3` | volume, likewise | 0, 1 |
| `voicestopall` | `0x580` | stops every voice and every battle shout (`0x002DF690(-1)`) | 2, and 1,522 in field maps |
| `setexpandvoicememory(heap, size)` | `0x395` | a larger voice heap (`0x003E9AA0`) | 2 |

The speaker argument of `voiceplay_28b` and `voiceplay_28c` has no effect: `0x003EA180` writes only through slot field
`+0x38`, which is always 0.

### Stopping, pan and volume

`0x002DF690(id)` destroys the stream bank with that id, or every one for -1 (`0x0021D840`); only when that finds none
does it go on to the battle-voice banks (`0x0021C870`). Pan and volume go through the sound-effect setters `0x002256F0` and `0x002257E0`
([Sound effects](sound-effects.md)). Every voice bank's sound has category 3, so the Config Voice row scales it
(`0x002DE310`).

Each cue helper first takes the slot's table for the language into `+0x30` (`0x002DEBB0`) and checks the slot is ready
and the index below the count:

- `0x003E9A10(slot, index)` answers 1 while a line is pending, a load handle at cue `+0x14` with bit 31 of `+0x08`,
  and otherwise whether its stream still plays (`0x001DC2C0`); `voicesync` waits on it (`0x003527F0`).
- `0x003E9B80(slot, index)` answers whether the cue holds a load handle, the test `voicepan` and `voicevolume` wait on
  (`0x003537B0`).
- `0x003EA430` and `0x003EA540` pan the cue's stream and set its volume (`0x002DF610`, `0x002DF6A0`), for the results of
  `voicepan` (`0x00352E80`) and `voicevolume` (`0x00353C20`).
- `0x003EA330(slot)` hands every cue's load handle and stream to `0x003EA3E0` and clears its pending bit, stream and
  handle.

`0x003E98B0(slot)` frees a slot: one still loading becomes state 4; a parked or ready one has its lines closed
(`0x003EA330`), both tables and the block at `+0x38` freed, and returns to state 0.

### Lines picked by party member

A set of verbs lets a scene speak a line through whichever party member can say it. `battlevoice_regist_ctrl_data`
`0x46B` (`0x00344000` -> `0x003EBE70`) takes a control table, keeps it at `0x02B5EC60`, allocates a `0x100`-byte block
named `VOICEWK` at `0x02B5EC68` and picks a member for every group into the eight words at `0x02B5EC70`:

1. `0x00321EA0` runs the search `0x00321F10` first with the party test and, when that finds no answer, again without it.
2. `0x00321F10` gives each group in turn one of its candidates, `0xC4` bytes per group with a count at `+0x04` and
   12-byte candidates from `+0x08` whose third word is the member (-1 fits any group), never the same member twice. With the test on, a member must be below 40 and its
   party record at `[0x02EBF190] + 8 + member x 0x1C8` must have none of the bits `0x88000013` in `+0x64` or `+0x3C`.
3. `battlevoice_calc_member` `0x46D` (`0x003447E0` -> `0x003EBD30`) clears the eight picks and runs the search again on
   the kept table.

`battlevoice_regist_message_and_voice` `0x46E` (`0x00344BB0` -> `0x003EBF20`) stores a voice id and a message id in
`VOICEWK` entry `n` when group `g` picked candidate `c`. `mesvgetvoiceid` `0x490` (`0x003EBE20`) and `mesvgetmesid` `0x491`
(`0x003EBE00`) read entry `n` back, -1 without a block, and `mesvgetfaceid` `0x49C` (`0x003EBDC0`) reads the middle word
of the picked candidate of a group.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "PKFL" |
| `+0x04` | `u32` | count | 64 |
| `+0x08` | `u32[128]` | files | per sub-file an offset then a size; size 0 for none |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "VSP1" |
| `+0x04` | `u32` | count | cues that follow, 16 bytes each: bank offset, bank size, 0, 0 |

Each cue's bank is a `sabf` container with one sound ([Sound banks](sound-banks.md)).

## Shipped data

| | |
|---|---|
| language folders | `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us` |
| packs per folder | 201 `.vpc` and 201 `.vpcjp` |
| sub-files and cues per folder | 510 sub-files and 2,554 cues for each extension |
| sub-files used | 0-13; at most 24 cues in one sub-file |
| `.vpcjp` | identical in every folder |
| `.vpc` | identical in every folder, except `var_z0100` and `var_z0102`, which have two versions |
| sound category | 3 in all 5,102 `us` banks; 3 of the 2,554 cues per extension have no bank |

Every one of the 4,943 cue words in the event scripts names a sub-file present in that event's `.vpc` and an index
below its count.

## State

The eight picks at `0x02B5EC70` are one `i32` per group, the candidate the search gave it. `0x003EBD30`, `0x003EBD70`,
`0x003EBE40` and `0x003EBE70` clear them with four 8-byte stores; the search `0x00321F10` writes them by group through the
address `0x003EBD30` and `0x003EBE70` hand to `0x00321EA0` (`0x0032203B`); `mesvgetfaceid` `0x003EBDC0` and
`battlevoice_regist_message_and_voice` `0x003EBF20` read them by group (`0x003EBDD6`, `0x003EBF2A`). `0x003EBD70` also frees
`VOICEWK` (`0x003697F0`) and forgets the control table; `0x003EBE40` forgets both without freeing.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B5EC78` | `i32[2]` | 0 | the picks of groups 2 and 3 | `0x003EBD30` (`0x003EBD40`); `0x003EBD70` (`0x003EBDA4`); `0x003EBE40` (`0x003EBE57`); `0x003EBE70` (`0x003EBEEC`); `0x00321F10` (`0x0032203B`) | `0x003EBDC0` (`0x003EBDD6`); `0x003EBF20` (`0x003EBF2A`) |
| `0x02B5EC80` | `i32[2]` | 0 | the picks of groups 4 and 5 | `0x003EBD30` (`0x003EBD47`); `0x003EBD70` (`0x003EBDAB`); `0x003EBE40` (`0x003EBE5E`); `0x003EBE70` (`0x003EBEF3`); `0x00321F10` (`0x0032203B`) | `0x003EBDC0` (`0x003EBDD6`); `0x003EBF20` (`0x003EBF2A`) |

No other instruction reaches these words. The picks' address is taken by `0x003EBD30`, `0x003EBDC0`, `0x003EBE70` and
`0x003EBF20` only.

## Modding notes

- A line is sub-file `slot`, cue `index` of the event's `.vpc` (English) and `.vpcjp` (Japanese).
- Replace a line by replacing its `sabf` bank inside the cue table and fixing the offsets and the sub-file size.
- Slots are global: an event's `voiceread(k)` replaces whatever slot `k` held.

## Related

- [Sound banks](sound-banks.md) - the `sabf` banks and the battle-voice banks.
- [Sound effects](sound-effects.md) - the pan and volume setters.
