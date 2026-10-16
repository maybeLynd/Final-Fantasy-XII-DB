---
title: "Voices: the voice packs a cutscene loads, the sixty-four voice slots, the English or Japanese choice, and the verbs that play, stop and pan a line"
kind: "system"
category: "Sound and music"
addresses: "02B5D0B0, 003EA0D0, 003E9F80, 003E9C10, 003E9780, 003581B0, 002DDE20, 002DF690"
---

## What the player sees

- Cutscenes speak in English or Japanese, by the Config setting.
- A line plays when its scene reaches it and can be panned left or right as the speaker moves.
- The Voice volume row sets how loud the lines are.
- Field maps play no cutscene voice; battle shouts come from the battle-voice banks ([Sound banks](sound-banks.md)).

## How it works

### The slots

The voice slots are 64 records of `0x40` bytes at `02B5D0B0`, global to every script (`003E9B10` builds them).
Slot `k` always holds sub-file `k` of the calling event's pack:

| Field | Holds |
|---|---|
| `+0x00` | the slot's own number, the pack sub-file it loads |
| `+0x04` | the state: 0 free, 1 parked, 2 loading, 3 ready, 4 freed while loading, 5 one of two tables delivered |
| `+0x05` | the event manager that loaded it |
| `+0x20`, `+0x28` | the loaded `.vpcjp` and `.vpc` sub-files |
| `+0x30` | the table in use, chosen by the language |

### The packs

`003E9F80` loads a slot only for event managers 1-3: `0032F360` refuses managers 4 and up, and manager 0 answers -1
because `0032FCA0` loads it as kind 5 and blanks its directory (`0032FFAA`, `0032FFFC`), so field maps load no voice
pack. The event's pack directories, `0x208` bytes each, are read by `0032FCA0` (`0032FF3A`-`0032FFE2`):

- kind 8, `plan_master\<language>\event\...\<event>.vpc`, into `022C6EE8`;
- kind 37, the `.vpcjp`, into `022C6EC0`.

Both tables of a slot are always loaded (`003EA0D0`); the language only chooses which one the verbs use. Kind 37 comes
from the `in` folder, or the `ch` folder for the Korean and Chinese builds (`002DFE74`).

### The language

`002DDE20` answers bit 10 of the options record `*0215E6E0 + 4`. Clear plays the `.vpc` and set plays the `.vpcjp`
(`002DEBB0`). Options command `0x10` writes the bit (`002DE2F0`, `002DE2FD`); a new options record sets it for the
Japanese, Korean and Chinese builds (`002DDF24`-`002DDF55`).

### The cue word

A script names a line as `slot << 24 | index`. `003E9C10` plays it only when the slot is ready and the index is below
its table's count (`003E9C10`). It opens a stream on the stream controller (`002DF660`) and stores the volume, pan and
a pending bit in the cue entry.

| Cue entry field | Holds |
|---|---|
| `+0x08` bits 0-23 | the bank's offset |
| `+0x08` bits 24-30 | the volume, 0-127 |
| `+0x08` bit 31 | pending start |
| `+0x0C` bits 0-23, byte `+0x0F` | the bank's size, the pan |
| `+0x10`, `+0x14` | the stream id, the load handle |

### Starting a line

`003E9780` runs at the end of the request pump `0032E070` (`0032E2AA`). For each ready slot and each cue with a stream:

1. When its load request is done, the pending bit is set and the main loop is in mode 2 (`02064AD3`), it starts the
   stream with `002DF680(stream, pan, volume)` (`003E980B`-`003E9832`).
2. When the stream has stopped sounding, it clears the cue (`003E985C`-`003E9864`).

A line asked for again while it still plays is not restarted: no new stream is opened and the pending bit is dropped
when the old one ends.

### The verbs

| Verb | Id | Does | Calls in event scripts |
|---|---|---|---:|
| `voiceread(slot)` | `0x085` | loads a slot (`0034EE40`) | 389 |
| `voiceread_20a(slot, flag)` | `0x20A` | the same with a choice of allocator | 171 |
| `voicereadsync(slot)` | `0x086` | waits while loading | 552 |
| `voiceplay(cue)` | `0x087` | plays at pan `0x40`, volume `0x7F` | 262 |
| `voiceplay_b5(cue, pan, volume)` | `0x0B5` | plays with pan and volume | 9 |
| `voiceplay_28b(speaker, cue)` | `0x28B` | plays at pan `0x40`, volume `0x7F` | 2,218 |
| `voiceplay_28c(speaker, cue, pan, volume)` | `0x28C` | plays with pan and volume | 42 |
| `voicestandby(cue)` | `0x28D` | opens the stream without starting it | 1,965 |
| `voicestop(cue)` | `0x088` | waits for the load, then closes the stream (`003EA2C0`) | 41 |
| `voicesync(cue)` | `0x089` | waits while the line plays | 387 |
| `voicedispose(slot)` | `0x08C` | stops every line of the slot and frees it | 628, and 11 in field maps |
| `voicepan(cue, pan)`, `voicechangepan(cue, frames, pan)` | `0x0B1`, `0x0B4` | pan, at once or over frames, once the line has started | 10, 8 |
| `voicevolume(cue, volume)`, `voicechangevolume(cue, frames, volume)` | `0x0B2`, `0x0B3` | volume, likewise | 0, 1 |
| `voicestopall` | `0x580` | stops every voice and every battle shout (`002DF690(-1)`) | 2, and 1,522 in field maps |
| `setexpandvoicememory(heap, size)` | `0x395` | a larger voice heap (`003E9AA0`) | 2 |

The speaker argument of `voiceplay_28b` and `voiceplay_28c` has no effect: `003EA180` writes only through slot field
`+0x38`, which is always 0.

### Stopping, pan and volume

`002DF690(id)` destroys the stream bank with that id, or every one for -1 (`0021D840`); only when that finds none
does it go on to the battle-voice banks (`0021C870`). Pan and volume go through the sound-effect setters `002256F0` and `002257E0`
([Sound effects](sound-effects.md)). Every voice bank's sound has category 3, so the Config Voice row scales it
(`002DE310`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | magic | "PKFL" |
| `04` | `u32` | count | 64 |
| `08` | `u32[128]` | files | per sub-file an offset then a size; size 0 for none |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | magic | "VSP1" |
| `04` | `u32` | count | cues that follow, 16 bytes each: bank offset, bank size, 0, 0 |

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

## Modding notes

- A line is sub-file `slot`, cue `index` of the event's `.vpc` (English) and `.vpcjp` (Japanese).
- Replace a line by replacing its `sabf` bank inside the cue table and fixing the offsets and the sub-file size.
- Slots are global: an event's `voiceread(k)` replaces whatever slot `k` held.

## Related

- [Sound banks](sound-banks.md) - the `sabf` banks and the battle-voice banks.
- [Sound effects](sound-effects.md) - the pan and volume setters.
