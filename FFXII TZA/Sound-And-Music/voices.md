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

`0x003EA0D0(manager, slot, allocator)` first frees the slot with `0x003E98B0` (`0x003EA0F0`). A slot that the free leaves
in state 2, 4 or 5 loads nothing, and the call answers 0 (`0x003EA10B`, `0x003EA11B`, `0x003EA163`). Otherwise it frees
it again and loads the `.vpc`, table 1, then the `.vpcjp`, table 0, through `0x003E9F80` (`0x003EA139`, `0x003EA14B`),
and answers 1 when either load answered 1 (`0x003EA150`-`0x003EA15A`).

`0x003E9F80(manager, slot, allocator, table)` first stores the language's table at `+0x30` (`0x003E9FB0`-`0x003E9FC0`).
It answers 0 and loads nothing when the manager's byte `0x022C6D18[m]` is 0 (`0x0032F240`, `0x003E9FCB`) or the size from
`0x0032F360` is 0 or less (`0x003EA013`). Otherwise it selects arena 12, or 2 while the qword `0x02B5E0B0` is 0, through
`0x0036C1D0` (`0x003EA015`-`0x003EA031`). It allocates the size with `0x0036A190` when the allocator argument is not 0 and
with `0x0036A100` when it is 0 (`0x003EA038`-`0x003EA043`); a null block pops the arena (`0x0036C140`) and answers 0
(`0x003EA04E`-`0x003EA055`).

It then zeroes the block (`memset`, `0x003EA061`) and stores the kind word, 37 for the `.vpcjp` and 8 for the `.vpc`,
at `+0x0C` or `+0x0E`, the index from `0x0032F170` plus 3, `index + 3`, at `+0x10`, the block at `+0x20` or `+0x28`,
the size at `+0x14` or `+0x18`, the manager at byte `+0x05` and the arena at byte `+0x07` (`0x003EA066`-`0x003EA08C`).
It pops the arena (`0x003EA090`).

While the manager's skip byte `0x02099011 + manager × 0x288` is set (`0x00267310`), it parks the slot in state 1 and
reads nothing (`0x003EA095`-`0x003EA0A1`); otherwise `0x003E9EF0` files the read (`0x003EA0AD`). Both paths answer 1
(`0x003EA0B2`).

### The language

`0x002DDE20` answers bit `0x400` of the options record `*0x0215E6E0 + 4`. Clear plays the `.vpc` and set plays the `.vpcjp`
(`0x002DEBB0`). Options command `0x10` writes the bit (`0x002DE2F0`, `0x002DE2FD`); a new options record sets it for the
Japanese, Korean and Chinese builds (`0x002DDF24`-`0x002DDF55`).

### The cue word

A script names a line as `slot << 24 | index`. `0x003E9C10` plays it only when the slot is ready and the index is below
its table's count (`0x003E9C10`). It opens a stream on the stream controller (`0x002DF660`) and stores the volume, pan and
a pending bit in the cue entry.

`0x003E9C10(slot, index, pan, volume, start)` first stores the language's table at `+0x30` (`0x003E9C3E`-`0x003E9C4B`).
A negative volume becomes 0 and one above `0x7F` becomes `0x7F` (`0x003E9C4F`-`0x003E9C5E`). Ready means state 3 with
that table non-null, and the index is compared unsigned (`0x003E9C61`-`0x003E9C78`); otherwise it returns with no other
store. For a ready cue it sets the pending bit `0x80000000` of `+0x08` to `start`: 1 from `0x003E9BF0` and 0 from
`0x003EA2A0` (`0x003E9C8C`-`0x003E9CA7`).

It opens the stream only when the cue has no load handle, a non-zero size and no stream yet, and its bank at
`table + offset` starts with `sabf` (`strncmp`, `0x003E9CA3`-`0x003E9CD8`). `0x002DF660` gets the address of the cue's
`+0x10`, the bank and the size, and its result is stored as the load handle `+0x14` (`0x003E9CDA`-`0x003E9CF1`). Every
ready cue then gets the volume in bits `0x7F000000` of `+0x08` and the pan in byte `+0x0F` (`0x003E9CF9`-`0x003E9D09`).

| Cue entry field | Holds |
|---|---|
| `+0x08` bits under mask `0xFFFFFF` | the bank's offset |
| `+0x08` bits `0x7F000000` | the volume, 0-127 |
| `+0x08` bit `0x80000000` | pending start |
| `+0x0C` bits `0xFFFFFF`, byte `+0x0F` | the bank's size, the pan |
| `+0x10`, `+0x14` | the stream id, the load handle |

### Starting a line

`0x003E9780` runs at the end of the request pump `0x0032E070` (`0x0032E2AA`). For each of the 64 slots it first stores
the table the language chooses (`+0x20` or `+0x28`, by `0x002DEBB0`) at `+0x30`, ready or not
(`0x003E97B0`-`0x003E97C2`). A slot counts as ready in state 3 with that table non-null; its cues are the table's
count (`+0x04`, signed, above 0) of 16-byte entries. For each cue with a stream (`+0x10` non-zero, `0x003E97F3`):

1. When it has a load handle (`+0x14` non-zero), the load is done (`0x002DEE90(handle)` answers 0), the pending
   bit is set and the main loop is in mode 2 (`0x00229EA0`: `0x02064AD3`), it starts the stream with
   `0x002DF680(stream, pan, volume)` (`0x003E980B`-`0x003E9832`). It then clears the pending bit and the load handle
   and stores −1 in the slot's dword `+0x08` (`0x003E9837`-`0x003E9844`).
2. With no load handle, when `0x003E9A10(slot, cue)` answers 0 (the stream has stopped sounding, `0x002DF630`), it
   clears the cue: the pending bit and the qword `+0x10`, the stream id with the load handle
   (`0x003E985C`-`0x003E9864`). The offset, volume, size and pan stay.
A line asked for again while it still plays is not restarted: no new stream is opened and the pending bit is dropped
when the old one ends.

### The verbs

| Verb | Id | Does | Calls in event scripts |
|---|---|---|---:|
| `voiceread(slot)` | `0x085` | loads a slot (`0x0034EE40`) | 389 |
| `voiceread_20a(slot, flag)` | `0x20A` | the same with a choice of allocator | 171 |
| `voicereadsync(slot)` | `0x086` | waits while the slot is loading, freed while loading or holds one of its two tables (states 2, 4 and 5; poll `0x0034F770`); in states 0, 1 and 3 it goes on at once, since its test `0x0053DD10` always answers 1 | 552 |
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

`voiceplay_b5` (`0x00351020`), `voiceplay_28b` (`0x00350BC0`), `voiceplay_28c` (`0x00350880`) and `voicestandby`
(`0x00351B60`) push the missing arguments (speaker -1, pan `0x40`, volume `0x7F`) and a start flag, 1, or 0 for
`voicestandby`, and jump to `0x003581B0`. It splits the cue into the slot, `cue >> 24`, and the index, the low 24 bits
(`0x0035820D`-`0x00358218`). A negative speaker becomes the first word of its second argument (`0x0035821F`), and it
calls `0x003EA180` with it (`0x0035822E`).

While the skip byte `0x02099011 + manager × 0x288` of the calling actor's manager (byte `+0x15`, `0x00267310`) is set it
opens nothing (`0x00358233`-`0x0035823F`). Otherwise it calls `0x003E9C10` through `0x003E9BF0` for a start flag of 1 and
through `0x003EA2A0` for 0 (`0x0035824B`-`0x00358257`).

### Stopping, pan and volume

`0x002DF690(id)` destroys the stream bank with that id, or every one for -1 (`0x0021D840`); only when that finds no bank
does it go on to the battle-voice banks (`0x0021C870`). Pan and volume go through the sound-effect setters `0x002256F0` and `0x002257E0`
([Sound effects](sound-effects.md)). Every voice bank's sound has category 3, so the Config Voice row scales it
(`0x002DE310`).

Each cue helper first takes the slot's table for the language into `+0x30` (`0x002DEBB0`) and checks the slot is ready
and the index below the count:

- `0x003E9A10(slot, index)` answers 1 while a line is pending, a load handle at cue `+0x14` with bit `0x80000000` of `+0x08`,
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
   member stats record at `[0x02EBF190] + 8 + member x 0x1C8` must have none of the bits `0x88000013` in `+0x64` or `+0x3C`.
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
| `+0x08` | `u32[128]` | files | per sub-file an offset then a size; size 0 for no sub-file |

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

### Packs and cues

[voices-packs.tsv](voices-packs.tsv) has one row per `.vpc` of the `us` folder, 201 rows, with the size of the same
event's `.vpcjp` beside it; the two files of every event have the same sub-files and cue counts.
[voices-cues.tsv](voices-cues.tsv) has one row per cue the event scripts play: 2,496 cues of 198 events. The us
listings cover 1,114 of the 1,115 `us` scripts: `evt_t0020.ebp` has no `EBP2` header and no listing, and its folder
holds no voice pack.

#### The packs

- `scene`, `place` and the scripts that start each event come from the per-area scene pages
  ([Archades scenes](../Story-Events-And-Hunts/archades-scenes.md) and the others): 200 of the 201 packs
  belong to a scene there. `scene` is the first spoken line of the scene, `place` the page's "Loaded in".
- `0x0032FCA0` reads both packs' directories when the event loads ("The packs" above). 190 packs have the scripts that
  load their event.
- The nine summon scene packs, `sum_d0001` to `sum_m0001`, belong to scenes whose event id no zone or scene script
  names ([Summon scenes](../Story-Events-And-Hunts/summons-scenes.md)), and no zone script names
  `spc_z0000`'s event 210 ([Special move scenes](../Story-Events-And-Hunts/special-move-scenes.md)).
  `spc_z0000`'s pack is 2,048 bytes with no sub-file.
- `evt_t0005` carries a pack but is a developer script with no event id
  ([Developer scripts](../Story-Events-And-Hunts/developer-scripts.md)), so no event load reads it.

#### The cues

- The 4,943 cue words name 2,496 distinct cues, and 2,531 play calls start them: `voiceplay` 262, `voiceplay_b5` 9,
  `voiceplay_28b` 2,218 and `voiceplay_28c` 42. 58 of the 2,554 cues in the packs are named by no cue word.
- `speaker` is the actor whose position among the listing's `actor` declarations the `voiceplay_28b` and
  `voiceplay_28c` argument gives; all 2,260 arguments fall on a declaration. The game name comes from a
  [word bank](../Menus-And-HUD/text-word-bank.md), [NPC names](../Menus-And-HUD/text-npc-names.md) or
  [string table](../Menus-And-HUD/text-string-tables.md) row whose Japanese `in` cell names the actor: 1,029 rows.
- `length` is the cue's sample count over its rate, read in the cue's `sabf` bank: the `mtrl` record (the `mtrl`
  chunk's offset + `0x20`) holds the channels at `+0x04`, the codec at `+0x05`, the rate (`u32`, 48,000 for every cue)
  at `+0x08` and the codec header size (`u32`) at `+0x14`.
- For codec 7 the codec header holds an HCA header; its `fmt` chunk gives the frame count (big-endian `u32` at
  `fmt + 8`); a frame is 1,024 samples, a constant of the HCA format. The four codec 3 cues, cues 0 and 1 of
  `rwg_d0100` sub-file 0 and of `rwg_d0101` sub-file 1, are Ogg Vorbis: the last Ogg page's granule position is the
  sample count.
- 89 cues of the `.vpc` packs, 67 of them played, hold the same two-frame HCA bank: after each frame's `FFFF` sync
  word every byte is 0 but the two-byte checksum, which the HCA format decodes as silence. Their `.vpcjp` cues hold
  7 to 745 frames, so those lines are voiced only in Japanese. Their `length` reads `0.04 s, a silent stub`.

#### How a cue is joined to its line

Each function of the event's listing is run on the `us` build with English voices: `getff12lang` answers 1 and
`unkCall_59c` answers 1 ([verb arguments](../Scripts-And-Script-Commands/verb-arguments.md)), and a variable given a
known value keeps it, so a test or `switch` on known values takes one path. A test that cannot be settled runs every
branch from the same frame, each on its own path.

The clock: `wait(n)` adds n frames (`0x0034CF90`, [native commands](../Scripts-And-Script-Commands/native-commands.md));
`voicesync` of a cue the same path started waits out the cue's length; `sysReqew` parks the requester until the
requested function returns ([script requests](../Scripts-And-Script-Commands/script-requests.md)) and `sysReqwait`
until an earlier request returns, adding that function's length when all its paths return at one frame. Any other
wait starts a new clock.

`sysReq` and `sysReqall` start the requested functions on the requester's clock, three requests deep. A message call
(`amest`, `ames`, `ames_1fe`, `amese`, `aask`, `aaske`, `aask_1ff`) with id `0x01xxxxxx` opens line `xxxxxx` of
section 2 of the event's dialogue table ([Archades dialogue](../Menus-And-HUD/archades-dialogue.md) and the other area
pages); the next message call or `mesclose` closes it.

A cue is joined to the first that applies, rule 5 being checked first:

1. the line the playing function has on screen when it plays the cue: 128 cues;
2. the one line of a function the playing function requested just before, without waiting for it: 6;
3. the playing function's next line, opened within 10 frames with no request or wait for one between: 204;
4. on the clock of a function that reaches the play, the one line on screen when the cue starts (1,154), or else the
   one line that opens within 10 frames after it (89), which is also taken when the line on screen at the start
   closes within those 10 frames; every function that reaches the play gives the same line;
5. a cue that starts more than 10 frames before its own line: the one line opened while the cue plays whose speaker
   the listing names as the cue's. The line opens while an earlier speaker's line is still on screen (2), or no
   line is on screen when the cue starts and the line opens 12 to 56 frames later (18).

The listing names a line's speaker by a mouth call, `setkutipakustatus(1)` on the speaker's actor, made directly or
through a function such as `talking` or `くちパクON`, that has the speaker's mouth open when the line opens or within
10 frames after, or by a `TAGmes_` function named for the speaker.

Ten cues were read at the listing with the lines' text:

- Seven start before their own line in a listing that names no speaker for it: `bhm_a0200` sub-file 2 cue 4,
  `byu_y0101` sub-file 3 cue 1, `rbn_a1701` sub-file 3 cue 2, `rsn_a0102` sub-file 0 cue 3,
  `rsn_b0100` sub-file 2 cue 5, `rsn_b0100` sub-file 3 cue 1 and `rsn_y0100` sub-file 0 cue 6; each joins the one line
  of its speaker opened while it plays, 15 to 43 frames after it starts;
- Three are reactions inside another speaker's line that outlast the line, so the reaction clause below does not reach
  them, and keep no line: `alc_b0400` sub-file 1 cue 10, by 5 frames, `dgl_g0101` sub-file 0 cue 7, by 4 frames or
  more, and `rbn_y0100` sub-file 4 cue 6, by 27 frames.

A cue these rules reach keeps no line when:

- its `.vpc` bank is the silent stub (17 cues);
- it is a reaction inside another speaker's line: it starts and ends while one line is on screen, and the cue joined
  to that line, of another speaker, plays from before it starts until after it ends (12). A cue whose play call
  names no speaker counts as the speaker its sound code gives: on `dor_c1200` line 3, Reddas's cue 11 of sub-file 0
  plays inside cue 10, `ve175_010Cd`, Doctor Cid's;
- it is a crowd track: its `sound` is a `ga` bank of the 1xx series, which carries no speaker's code (10);
- a cue of another speaker reaches the same line and the line is not a subtitle of two speakers, which starts `- `
  (44);
- the listing gives the line to another speaker (2): `ene_a0200` sub-file 2 cue 7, Vossler's, starts on line
  36, which `TAGmes_ASHE_19` shows between `ASHE::unapaku_on` and `unapaku_off`, and `bul_a0201` sub-file 0 cue 5,
  Penelo's, starts on line 1, which `TAGmes_BALFLAIR_1_02` shows, 4 frames before it closes.

Where cues of two speakers reach one line and the listing opens one speaker's mouth with it, within 10 frames of
the line's opening, that speaker's cue keeps the line: Balthier's on `rbn_a1600` line 1, opened after
`バルフレア::クチウナオン`, and on `byu_a1880` line 6, whose `TAGmes_BALFLAIR_6` requests `BALFLAIR::paku_on`.

The `sound` column gives each cue's sound name, the name of its bank in the `.vpc`, which carries a speaker code.
Where that code is another character's than the `speaker`'s, the cue is played through another actor's slot: 28 cues,
among them Ondore's and Ashe's voices (`ve277_012od`, `ve277_013od`, `ve277_015AS`) on Balthier's slot in `byu_w0100`,
where Balthier speaks through a voice device, and `dor_b0101` sub-file 5 cue 0, Balthier's `ve177_018BF`, on Doctor
Cid's slot.

That joins 1,608 cues. The other 888 have no line on their clock when they start (409), share their
clock with no message call (388), start while two or three lines are on screen (3), or keep no line by the
rules above (88). In `nal_d0100`, `ボイス.発音` (line 1232) plays cues 1 and 2 of sub-file 0 in scene 4
(`startscene(file_var_s0_2)`), Balthier's cue, a silent stub, and Vaan's 1.56-second cue, and `メッセージ.表示`
(line 945), which shows the scenes' lines, has no case for scene 4.

A play that no path reaches with English voices is followed again with `getff12lang` answering 0, Japanese voices.
One cue is played on that path alone, `rbn_a0200` sub-file 0 cue 13 (`ボイス.なんだと！？`, line 628); its `length` is
the `.vpcjp` cue's.

#### Columns

Columns of [voices-packs.tsv](voices-packs.tsv):

| Column | Meaning |
|---|---|
| `event` | the event script, by its file name; the pack is `<event>.vpc` in the script's folder |
| `event_id` | the event id from the scene page; `-` for the developer script `evt_t0005` |
| `scene` | the scene's first spoken line, in quotes, from the scene page's synopsis; for a scene with no spoken line, what it holds instead; for a summon scene, its set and event ids |
| `place` | where the scene is loaded, the scene page's "Loaded in", a map code given with its map or region name |
| `sub_files` | the sub-files the `.vpc` holds |
| `cues` | its cues, over all sub-files |
| `bytes_us` | the size of the `us` `.vpc` |
| `bytes_jp` | the size of the `.vpcjp` |
| `loaded_by` | `0x0032FCA0` reading the pack at the event's load (kind 8 `.vpc`, kind 37 `.vpcjp`), then the zone scripts and functions that load the event, from the scene page |

Columns of [voices-cues.tsv](voices-cues.tsv):

| Column | Meaning |
|---|---|
| `event` | the event script |
| `sub_file` | the sub-file, the slot of the cue word (`slot << 24`) |
| `index` | the cue's index in the sub-file |
| `function` | the actor and function that play the cue; two, for the 11 cues two functions play, separated by ` / ` |
| `speaker` | the game name with the actor's name in brackets; the actor's name alone where the text tables give no game name; `-` for `voiceplay` and `voiceplay_b5`, which name no speaker |
| `sound` | the cue's sound name, the name of its bank in the `us` `.vpc`, verbatim; it carries a speaker code, `ga` for a crowd track (see "How a cue is joined to its line") |
| `line_index` | the joined line, its id in section 2 of the event's dialogue table; `-` when no line is joined |
| `line` | the joined line's `us` text, its text codes dropped and each line break a space; `-` when no line is joined |
| `length` | the cue's length in seconds, from the `.vpc` (the `.vpcjp` for the one cue played only with Japanese voices); `0.04 s, a silent stub` for the 67 cues whose `.vpc` bank is the silent stub |
| `join` | how the line was joined, or why it was not: what the cue's clock holds, a silent stub, or a line of another speaker |

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
