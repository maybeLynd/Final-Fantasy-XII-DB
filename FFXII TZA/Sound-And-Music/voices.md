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

The voice slots are 64 records of `40`<sub>h</sub> bytes at `02B5D0B0`, global to every script (`003E9B10` builds them).
Slot `k` always holds sub-file `k` of the calling event's pack:

| Field offset | Holds |
|---|---|
| `00`<sub>h</sub> | the slot's own number, the pack sub-file it loads |
| `04`<sub>h</sub> | the state: 0 free, 1 parked, 2 loading, 3 ready, 4 freed while loading, 5 one of two tables delivered |
| `05`<sub>h</sub> | the event manager that loaded it |
| `20`<sub>h</sub>, `28`<sub>h</sub> | the loaded `.vpcjp` and `.vpc` sub-files |
| `30`<sub>h</sub> | the table in use, chosen by the language |

### The packs

`003E9F80` loads a slot only for event managers 1-3: `0032F360` refuses managers 4 and up, and manager 0 answers -1
because `0032FCA0` loads it as kind 5 and blanks its directory (`0032FFAA`, `0032FFFC`), so field maps load no voice
pack. The event's pack directories, `208`<sub>h</sub> bytes each, are read by `0032FCA0` (`0032FF3A`-`0032FFE2`):

- kind 8, `plan_master\<language>\event\...\<event>.vpc`, into `022C6EE8`;
- kind 37, the `.vpcjp`, into `022C6EC0`.

Both tables of a slot are always loaded (`003EA0D0`); the language only chooses which one the verbs use. Kind 37 comes
from the `in` folder, or the `ch` folder for the Korean and Chinese builds (`002DFE74`).

### The language

`002DDE20` answers bit 10 of the options record `*0215E6E0 + 4`. Clear plays the `.vpc` and set plays the `.vpcjp`
(`002DEBB0`). Options command `10`<sub>h</sub> writes the bit (`002DE2F0`, `002DE2FD`); a new options record sets it for the
Japanese, Korean and Chinese builds (`002DDF24`-`002DDF55`).

### The cue word

A script names a line as `slot << 24 | index`. `003E9C10` plays it only when the slot is ready and the index is below
its table's count (`003E9C10`). It opens a stream on the stream controller (`002DF660`) and stores the volume, pan and
a pending bit in the cue entry.

| Cue entry field | Holds |
|---|---|
| `+08`<sub>h</sub> bits 0-23 | the bank's offset |
| `+08`<sub>h</sub> bits 24-30 | the volume, 0-127 |
| `+08`<sub>h</sub> bit 31 | pending start |
| `+0C`<sub>h</sub> bits 0-23, byte `+0F`<sub>h</sub> | the bank's size, the pan |
| `+10`<sub>h</sub>, `+14`<sub>h</sub> | the stream id, the load handle |

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
| `voiceread(slot)` | `085`<sub>h</sub> | loads a slot (`0034EE40`) | 389 |
| `voiceread_20a(slot, flag)` | `20A`<sub>h</sub> | the same with a choice of allocator | 171 |
| `voicereadsync(slot)` | `086`<sub>h</sub> | waits while loading | 552 |
| `voiceplay(cue)` | `087`<sub>h</sub> | plays at pan `40`<sub>h</sub>, volume `7F`<sub>h</sub> | 262 |
| `voiceplay_b5(cue, pan, volume)` | `0B5`<sub>h</sub> | plays with pan and volume | 9 |
| `voiceplay_28b(speaker, cue)` | `28B`<sub>h</sub> | plays at pan `40`<sub>h</sub>, volume `7F`<sub>h</sub> | 2,218 |
| `voiceplay_28c(speaker, cue, pan, volume)` | `28C`<sub>h</sub> | plays with pan and volume | 42 |
| `voicestandby(cue)` | `28D`<sub>h</sub> | opens the stream without starting it | 1,965 |
| `voicestop(cue)` | `088`<sub>h</sub> | waits for the load, then closes the stream (`003EA2C0`) | 41 |
| `voicesync(cue)` | `089`<sub>h</sub> | waits while the line plays | 387 |
| `voicedispose(slot)` | `08C`<sub>h</sub> | stops every line of the slot and frees it | 628, and 11 in field maps |
| `voicepan(cue, pan)`, `voicechangepan(cue, frames, pan)` | `0B1`<sub>h</sub>, `0B4`<sub>h</sub> | pan, at once or over frames, once the line has started | 10, 8 |
| `voicevolume(cue, volume)`, `voicechangevolume(cue, frames, volume)` | `0B2`<sub>h</sub>, `0B3`<sub>h</sub> | volume, likewise | 0, 1 |
| `voicestopall` | `580`<sub>h</sub> | stops every voice and every battle shout (`002DF690(-1)`) | 2, and 1,522 in field maps |
| `setexpandvoicememory(heap, size)` | `395`<sub>h</sub> | a larger voice heap (`003E9AA0`) | 2 |

The speaker argument of `voiceplay_28b` and `voiceplay_28c` has no effect: `003EA180` writes only through slot field
`+38`<sub>h</sub>, which is always 0.

### Stopping, pan and volume

`002DF690(id)` destroys the stream bank with that id, or every one for -1 (`0021D840`); only when that finds none
does it go on to the battle-voice banks (`0021C870`). Pan and volume go through the sound-effect setters `002256F0` and `002257E0`
([Sound effects](sound-effects.md)). Every voice bank's sound has category 3, so the Config Voice row scales it
(`002DE310`).

Each cue helper first takes the slot's table for the language into `+30`<sub>h</sub> (`002DEBB0`) and checks the slot is ready
and the index below the count:

- `003E9A10(slot, index)` answers 1 while a line is pending, a load handle at cue `+14`<sub>h</sub> with bit 31 of `+08`<sub>h</sub>,
  and otherwise whether its stream still plays (`001DC2C0`); `voicesync` waits on it (`003527F0`).
- `003E9B80(slot, index)` answers whether the cue holds a load handle, the test `voicepan` and `voicevolume` wait on
  (`003537B0`).
- `003EA430` and `003EA540` pan the cue's stream and set its volume (`002DF610`, `002DF6A0`), for the results of
  `voicepan` (`00352E80`) and `voicevolume` (`00353C20`).
- `003EA330(slot)` hands every cue's load handle and stream to `003EA3E0` and clears its pending bit, stream and
  handle.

`003E98B0(slot)` frees a slot: one still loading becomes state 4; a parked or ready one has its lines closed
(`003EA330`), both tables and the block at `+38`<sub>h</sub> freed, and returns to state 0.

### Lines picked by party member

A set of verbs lets a scene speak a line through whichever party member can say it. `battlevoice_regist_ctrl_data`
`46B`<sub>h</sub> (`00344000` -> `003EBE70`) takes a control table, keeps it at `02B5EC60`, allocates a `100`<sub>h</sub>-byte block
named `VOICEWK` at `02B5EC68` and picks a member for every group into the eight words at `02B5EC70`:

1. `00321EA0` runs the search `00321F10` first with the party test and, when that finds no answer, again without it.
2. `00321F10` gives each group in turn one of its candidates, `C4`<sub>h</sub> bytes per group with a count at `+04`<sub>h</sub> and
   12-byte candidates from `+08`<sub>h</sub> whose third word is the member (-1 fits any group), never the same member twice. With the test on, a member must be below 40 and its
   party record at `[02EBF190] + 8 + member x 1C8h` must have none of the bits `88000013`<sub>h</sub> in `+64`<sub>h</sub> or `+3C`<sub>h</sub>.
3. `battlevoice_calc_member` `46D`<sub>h</sub> (`003447E0` -> `003EBD30`) clears the eight picks and runs the search again on
   the kept table.

`battlevoice_regist_message_and_voice` `46E`<sub>h</sub> (`00344BB0` -> `003EBF20`) stores a voice id and a message id in
`VOICEWK` entry `n` when group `g` picked candidate `c`. `mesvgetvoiceid` `490`<sub>h</sub> (`003EBE20`) and `mesvgetmesid` `491`<sub>h</sub>
(`003EBE00`) read entry `n` back, -1 without a block, and `mesvgetfaceid` `49C`<sub>h</sub> (`003EBDC0`) reads the middle word
of the picked candidate of a group.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | "PKFL" |
| `04`<sub>h</sub> | `u32` | count | 64 |
| `08`<sub>h</sub> | `u32[128]` | files | per sub-file an offset then a size; size 0 for none |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | "VSP1" |
| `04`<sub>h</sub> | `u32` | count | cues that follow, 16 bytes each: bank offset, bank size, 0, 0 |

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
