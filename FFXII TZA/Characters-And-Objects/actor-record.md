---
title: "Actor record: the record every field actor is driven through, its pool, its classes, its sub-objects and its lifetime"
kind: "system"
category: "Characters and objects"
addresses: "002679F0, 00266530, 00266AD0, 00266BD0, 003DB580, 003DB550, 003DBF60, 003DB2A0, 003DB640, 00358940, 0025B070, 002628B0, 003697F0, 00265020, 00263C20, 003589B0, 002659D0, 00269FC0, 0026BED0, 0026B480, 0026AD90, 0026AB50, 0026A140, 0026AD40, 00269EE0, 00269F60, 00265060, 002638F0, 002E9BE0, 002638C0, 00269DD0, 003EC5F0, 003EC690, 003DC710, 003605A0, 003E9970, 003B6C20, 003DEE10, 003DEC90, 0036DE70, 0036E080, 002A7A40, 002E2300, 00368AA0, 003EBD70, 003604D0, 0025A280, 002E63D0, 003EA200, 003E9100, 002E1630, 0036A280, 002E06F0, 0035AB50, 002ECBE0, 002EBDE0, 002697A0"
---

## What the player sees

Every townsperson, door, trigger line, party member and monster in a field is one record owned by
one of the five actor managers. When a field or a scene loads, the manager's script payload says
how many actors of each kind it brings, the records are carved out of one block, and each is set up
with its script entry, its position and steering state and its slots for resource requests and
waits. The record stays alive until the manager unloads, when the block is freed; the handle code
carries makes a stale reference fail instead of pointing at the wrong actor.

## How it works

### The pool

`002679F0(slot)` builds a manager's record pool from its bound payload (`[slot + 00h]`) and the
record count at `+20`<sub>h</sub> ([actor managers](actor-managers.md)):

1. the payload's table at payload `+[14h]` holds a `u16` count of sequences followed by a `u16`
   per sequence; the pool's payload size is the sum over sequences of the descriptor's size,
   rounded up to 16, times that count;
2. the header is `(count * 8 + 17h) & ~Fh` bytes and is allocated twice over: the block is
   `2 * header + payload` bytes from the allocator at `[slot + 88h]`, zeroed, with the count at
   `+00`<sub>h</sub>; `[slot + 1F0h]` keeps `block + header`;
3. records are carved from `block + 2 * header` in sequence order; the pointer table at `block + 8`
   receives each, and each record's byte `+03`<sub>h</sub> becomes `(class << 5) | sequence`; the slot's
   per-class counts at `+1D0`<sub>h</sub> (four `u16`) are added up and their running offsets written to
   `+1D8`<sub>h</sub>;
4. `00266530(slot, block, i)` initialises every record.

`0046BA50(m)` returns `[slot + 1F0h]` of manager `m` (`00263FF0`) when the slot's `+10`<sub>h</sub> bit 0 is set, and
otherwise an empty table at `02CA6050`, whose count it zeroes; render and effect code walks records through it
(`0031F607`, `0035E644`, `00465344`, `00465A84`).

`00358940(slot, ordinal)` returns `[block + 8 + ordinal * 8]` for an ordinal below the count. The
descriptor table at `01E0C328` has eight entries of `{u8 class, u8 sub, u16 size}`:

| Sequence | Class | Sub | Size | Movement context | Secondary context | Resource entries | Wait slots |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | `328`<sub>h</sub> | none | none | `+288`, 10 | `+1E8`<sub>h</sub>, 8 |
| 1 | 1 | 0 | `3A8`<sub>h</sub> | `+120`<sub>h</sub> | none | `+416`, 10 | `+268`<sub>h</sub>, 8 |
| 2 | 1 | 1 | `330`<sub>h</sub> | `+120`<sub>h</sub> | none | `+416`, 8 | `+240`<sub>h</sub>, 6 |
| 3 | 2 | 0 | `348`<sub>h</sub> | `+120`<sub>h</sub> | none | `+320`, 10 | `+208`<sub>h</sub>, 8 |
| 4 | 2 | 1 | `2D0`<sub>h</sub> | `+120`<sub>h</sub> | none | `+320`, 8 | `+1E0`<sub>h</sub>, 6 |
| 5 | 3 | 0 | `6E0`<sub>h</sub> | `+120`<sub>h</sub> | `+350`<sub>h</sub> | `+1240`, 10 | `+5A0`<sub>h</sub>, 8 |
| 6 | 3 | 0 | `6E0`<sub>h</sub> | `+120`<sub>h</sub> | `+350`<sub>h</sub> | `+1240`, 10 | `+5A0`<sub>h</sub>, 8 |
| 7 | 3 | 1 | `668`<sub>h</sub> | `+120`<sub>h</sub> | `+350`<sub>h</sub> | `+1240`, 8 | `+578`<sub>h</sub>, 6 |

`00266AD0(record)` plants the pointers from the sequence in `+03h & 1Fh`: `+B8`<sub>h</sub> = the movement
context, `+C0`<sub>h</sub> = the secondary context, `+A0`<sub>h</sub> = the resource entry pool, `+A8`<sub>h</sub> = `+A0`<sub>h</sub> plus
`C8`<sub>h</sub>, or `A0`<sub>h</sub> when the descriptor's `sub` is 1. The resource entries are 20 bytes each and the
wait slots 40, so the wait slots end exactly at the record's size on every row.

### The class byte

Bits 5-7 of `+03`<sub>h</sub> are the class and bits 0-4 the sequence. The movement code accepts class 3
(`+03h & E0h == 60h`); the position read `00265020` accepts classes 1 and 3; the `setline` verb
writes class 2 ([battle units](battle-units.md)). `00266BD0` seeds the flag dword `+1C`<sub>h</sub> by
sequence: 0 for sequence 0, `38`<sub>h</sub> for 1 and 2, `40`<sub>h</sub> for 3 and 4, `30004`<sub>h</sub> for 5 and 6, `34C85`<sub>h</sub>
for 7, and sets `+14`<sub>h</sub> bit 7 (battle-unit eligible) for sequences 5 and 7. A separate nibble, bits
0-3 of `+0E`<sub>h</sub>, is what `00263C20` returns as the actor class nibble.

### The initialiser

`00266530(slot, block, i)` fills record `i` on a zeroed block:

1. it clears `+14`<sub>h</sub> bit 7, zeroes `+EC`<sub>h</sub> and sets `+F5`<sub>h</sub> to `FF`<sub>h</sub>, picks the counts (8 wait
   slots and 10 resource entries, or 6 and 8 for a `sub` of 1), plants the pointers (`00266AD0`) and
   seeds `+1C`<sub>h</sub> and `+14`<sub>h</sub> bit 7 (`00266BD0`);
2. it writes `+00`<sub>h</sub> = `i`, `+10`<sub>h</sub> = 0, `+12`<sub>h</sub> = `FF`<sub>h</sub>, `+15`<sub>h</sub> = the slot index, `+16`<sub>h</sub> = 1,
   `+118`<sub>h</sub> = `3C0000`<sub>h</sub>, `+102`<sub>h</sub> = `FFFF`<sub>h</sub>, `+04`<sub>h</sub> = `FF00`<sub>h</sub>, `+20`<sub>h</sub> = `FF`<sub>h</sub>, and `+F8`<sub>h</sub> =
   the empty string at `02F8F2A0`, whose own byte it writes 0;
3. it writes `+100`<sub>h</sub> = 0, `+18`<sub>h</sub> = `FFFF0000`<sub>h</sub>, `+104`<sub>h</sub> = `FFFF`<sub>h</sub>, `+106`<sub>h</sub> = 0, `+0F`<sub>h</sub> = 0,
   `+21`<sub>h</sub> = 0, `+0A`<sub>h</sub> = 0, the entry-group word `+F6`<sub>h</sub> = 0, and zeroes `+28`<sub>h</sub>, `+30`<sub>h</sub>, `+38`<sub>h</sub>,
   `+10C`<sub>h</sub> and `+114`<sub>h</sub>;
4. it sets the flag bytes: `+14`<sub>h</sub> = `(old & B0h) | 30h`, `+0D`<sub>h</sub> = `(old & A2h) | 82h` and
   `+08`<sub>h</sub> = `(old & 9Fh) | 11h` on manager 0 (`(old & 22h) | 2` and `(old & 8Fh) | 1` elsewhere),
   then `+0D`<sub>h</sub> bit 5 and `+08`<sub>h</sub> bit 7 cleared, `+0B`<sub>h</sub> &= `C0`<sub>h</sub>, `+0C`<sub>h</sub> = `(old & 71h) | 8` then
   bits 4-6 cleared, `+09`<sub>h</sub> bits 5 and 7 cleared, `+13`<sub>h</sub> &= `3C`<sub>h</sub>, `+0E`<sub>h</sub> |= `F0`<sub>h</sub> then `&= F0h`,
   and for class 3 `+1C`<sub>h</sub> bits 8 and 13 cleared;
5. it binds the script entry: `+02`<sub>h</sub> = 1, or 2 while `i` is below the payload's count word at
   `+[14h] + 2`; `+40`<sub>h</sub> = the entry at payload `+[18h] + 4 + i * 20h` (`30`<sub>h</sub> when the payload's
   word `+0` is 8 or more); `+48`<sub>h</sub> and `+50`<sub>h</sub> = payload + the resolved dwords at entry `+10`<sub>h</sub> and
   `+14`<sub>h</sub>, `+58`<sub>h</sub> = payload + entry `+08`<sub>h</sub>;
6. a tagged entry (byte `+06`<sub>h</sub> negative and not `FF`<sub>h</sub>) registers the record in the pointer
   table at `0209A1F0` by its low 7 bits (`[120000h + rax * 8 + 1F7A1F0h]`, `00266758`-`0026677C`):
   tags 0-3 are the party roster entries the field runtime walks ([field runtime](field-runtime.md)),
   and tags 4 and above the sixteen pointers from `0209A210` that `0026CE60` clears on slot 0;
7. the record that held a tag below 4 is evicted (`+12`<sub>h</sub> = `FF`<sub>h</sub>, `+0F`<sub>h</sub> = 3), and the new
   record gets `+12`<sub>h</sub> = the tag and `+0F`<sub>h</sub> = 2 for tags 0-3, 3 above;
8. it builds the resource entry free list (`003DB580`) and clears bytes `+00`<sub>h</sub>-`+16`<sub>h</sub> of the
   first `+88`<sub>h</sub> (channel count) wait slots, which covers every slot only because the two counts
   are both 8 or both 6;
9. it runs the movement defaults `00265FF0(record, [+B8h])` and `00265B60`. `00265FF0` resets the
   context for the record's class and writes the class nibble: `+0E`<sub>h</sub> = `(old & B4h) | 4` for
   class 1, `(old & F5h) | 5` and `+0F`<sub>h</sub> = 3 for class 3, ending with `0026D6F0(record, 0.0, 2)`;
10. it resets the secondary context (`+138`<sub>h</sub> = 0, `+148`<sub>h</sub> = 1.0, `+14E`<sub>h</sub> = 1, `+140`<sub>h</sub> and
   `+144`<sub>h</sub> = 0 with `00268380`), fills the eighteen words `+C8`<sub>h</sub>-`+EB`<sub>h</sub> with `FFFF`<sub>h</sub>, and for a
   tagged entry with a secondary context sets its `+152`<sub>h</sub> = 0 and runs `002681E0`;
11. it issues the initial resource requests through `003DBB60(record, channel, id, 2, 0)`, counting
   each request on the last channel in `+10`<sub>h</sub>. On channel `channels - 1` it issues the `+20`<sub>h</sub> id
   (only when the payload word `+0` is 10 or more; from `+E6`<sub>h</sub>, else the entry row's word `+20`<sub>h</sub>
   when the row's count is 16 or more), then id 0, then the `+14`<sub>h</sub> id (`+DA`<sub>h</sub>, else row `+14`<sub>h</sub>
   when the count is over 9);
12. on channel 0 it issues the `+04`<sub>h</sub> id (`+CA`<sub>h</sub>, else row `+04`<sub>h</sub> when the count is over 1), not
   counted. An id of -1 or an absent row word issues nothing;
13. for a class-3 actor it sets `+1C`<sub>h</sub> bit 2 from the `+06`<sub>h</sub> id (`+CC`<sub>h</sub>, else row `+06`<sub>h</sub> when
   the count is over 2), running `00268EA0` when `+0B`<sub>h</sub> bit 3 is set, else clears bit 2; then bit 10
   from the `+16`<sub>h</sub> id (`+DC`<sub>h</sub>, else row `+16`<sub>h</sub> when the count is over 10) with the same call, and
   setting bit 10 clears bit 2 again; else clears bit 10. It ends with `003DB280(record)`.

### The resource entry lists

The pool at `+A0`<sub>h</sub> holds the record's 20-byte resource entries, linked by index: `003DB580` chains
them (`+00`<sub>h</sub> next, `+01`<sub>h</sub> previous, `+04`<sub>h</sub> = `80000000`<sub>h</sub>, `+10`<sub>h</sub> = 0), sets the counts `+88`<sub>h</sub>
(channels) and `+89`<sub>h</sub> (entries), the free-list head `+60`<sub>h</sub> = 0 and the detached head `+61`<sub>h</sub> =
`FF`<sub>h</sub>, the channel heads `+94`<sub>h</sub> and tails `+8C`<sub>h</sub> to `FF`<sub>h</sub>, and clears the masks `+06`<sub>h</sub> and
`+24`<sub>h</sub>. `003DB550(record, index)` returns `[+A0h] + index * 14h`, null for `FF`<sub>h</sub>.

- `003DBF60(record, id, class)` walks every channel whose bit in `+06`<sub>h</sub> is set, from its head,
  returning the first entry whose `+04`<sub>h</sub> word equals `id` or whose `+12h >> 1` equals `class`
  (either filter may be -1), bounded by the entry count; `FF`<sub>h</sub> when none.
- `003DB640(record, channel)` tests bit `channel` of `+06`<sub>h</sub>.
- `003DB2A0(record, index)` removes an entry. An entry in state 4 (`+10`<sub>h</sub>) or with a negative
  channel byte `+02`<sub>h</sub> is on the detached list at `+61`<sub>h</sub>, otherwise on its channel's list at
  `+94h[channel]`. The remover:
  1. unlinks it (`003DC1B0`);
  2. on a channel list, notifies the end of a mode-3 request whose `+06`<sub>h</sub> is not `8000`<sub>h</sub>
     (`003DC0D0`), notifies by class (`00263050`) when `+12`<sub>h</sub> is 2 or more, fixes the head and tail,
     and clears bit `channel` of `+06`<sub>h</sub>, `+24`<sub>h</sub> and `+26`<sub>h</sub> when the channel empties;
  3. pushes the entry on the free list (`003DB650`), sets `+63`<sub>h</sub> bit 1 and makes it the head.

`002697A0(record)` re-issues a record's standing requests. It removes the first entry with a
non-zero byte `+11`<sub>h</sub> from channel 1 and then from channel 0 (`003DB420(record, channel, 3)`, which
walks only that channel and only when its bit in `+06`<sub>h</sub> is set), then runs `00269640`.

While
`02099DE1` is set, `00269640` issues on channel 1 the `+C8`<sub>h</sub> id (the payload row's word `+02`<sub>h</sub>
when `+C8`<sub>h</sub> is `FFFF`<sub>h</sub> and the row's count is positive) when `+1C`<sub>h</sub> bit 0 is set, and on channel
0 the `+DE`<sub>h</sub> id (row word `+18`<sub>h</sub> when the count exceeds 11) when `+1C`<sub>h</sub> bit 11 is set, both
through `003DBB60(record, channel, id, 0, 0)`. A record whose `+18`<sub>h</sub> is 1 issues neither.

### The handle

A record is named outside its manager by the handle `003589B0` encodes from `+00`<sub>h</sub> (the index),
`+15`<sub>h</sub> (the manager) and `+16`<sub>h</sub> (the discriminator, seeded 1 by the initialiser and advanced by
`002659D0` through 1-2047 on a definition change); the resolver `003588B0` checks all three against the live record ([battle
units](battle-units.md)).

### The verb accessors

Script verbs reach a record's own bytes, its secondary context `[+C0h]` and a few globals through
small accessors. Each takes the calling actor unless the row says otherwise:

| Verb | Id | Accessor | What it does |
|---|---|---|---|
| `settargetliststatus(v)` | `053A`<sub>h</sub> | `00269FC0` | `+0E`<sub>h</sub> bit 6 = `v != 0` |
| `setnochecktouchheightflag(v)` | `020F`<sub>h</sub> | `0026BED0` | `+08`<sub>h</sub> bit 7 = `v != 0` |
| `fieldsign` | `0176`<sub>h</sub> | `0026B480` | class 1 only: `+0D`<sub>h</sub> bit 3 = bit 0 of the value the verb passes |
| `setmapjumpgroup(i)` | `011E`<sub>h</sub> | `0026AD90` | stores the actor in `0209A210[i]`, `i` capped at 15 and a negative `i` taken as 0 |
| `set_force_char_nearfade(v)` | `0552`<sub>h</sub> | `0026AB50(1, v)` | the globals `02099DA4` = 1 and `02099DA5` = `v` |
| `attachinfo(i, ref)` | `01C8`<sub>h</sub> | `0026A140` | secondary `+120h + i * 8` = the address `002650B0` resolves `ref` to through the current slot's homes, and secondary `+14F`<sub>h</sub> bit 2 set |
| `setambient(r, g, b)`, `resetambient` | `0116`<sub>h</sub>, `0117`<sub>h</sub> | `0026AD40` | secondary `+151`<sub>h</sub> bit 4 set, the colour handed to `0026A420`; `resetambient` passes the colour `00379900` returns and clears the bit again |
| `fetchambient`, `fetchambient_4e1(x, y, z)` | `04E0`<sub>h</sub>, `04E1`<sub>h</sub> | `0026AD40` | the same bit set, then `002E49B0(actor, 0)` or `002E49B0(actor, {x, y, z, 1.0})` |
| `set_ignore_hitgroup(v)` | `0503`<sub>h</sub> | `00269EE0` | byte `+119`<sub>h</sub> of the collision body at secondary `+138`<sub>h</sub> = `v` |
| `unkCall_5d0(v)` | `05D0`<sub>h</sub> | `00269F60` | through the render record the secondary context's `+00`<sub>h</sub> names (`003EC200`), dword `+738`<sub>h</sub> = `v`, with the debug print `set root bone physical` |

The distance verbs `distance3d`, `distance`, `distance_290`, `distance3d_291` (`028E`<sub>h</sub>-`0291`<sub>h</sub>) and
`isrange`, `isrange_296` (`0295`<sub>h</sub>, `0296`<sub>h</sub>) read positions through `00265060(actor)`, which
returns the movement context of a class-1 or class-3 actor and the static block `02099DC0` for any
other actor or a null one. `002638F0` returns secondary `+140`<sub>h</sub> (0 without a context), and
`002E9BE0` the signed secondary byte `+13`<sub>h</sub> (-1 without an actor or a context).

The common effect verbs keep one effect job per actor in the movement context: `002638C0` reads it
and `00269DD0` writes it, at `+74`<sub>h</sub> for class 1 and `+220`<sub>h</sub> for class 3 (other classes read 0 and
write nothing):

- `charcommoneffectplay(v)` (`0465`<sub>h</sub>, `00342A80`) ends a running job (`0024CFF0`) and zeroes it,
  pushes -1, `v` and 5, runs the nested verb `00357620`, and stores the integer result of the
  current wait slot (`002651A0`, which also sets that slot's command phase to 2) as the new job;
- `charcommoneffecttrigger(v)` (`0466`<sub>h</sub>, `00343080`) passes `v` to the job (`0024FE30`);
- `charcommoneffectstop` (`0467`<sub>h</sub>, `003433A0`) ends the job and zeroes it, as the release below does.

### Release

A manager's teardown `002628B0` runs in two phases.

1. `0025B070(slot)` is the semantic cleanup, run for every slot but 4. For the class-1 and
   class-3 records (the ranges
   `+1DA`<sub>h</sub>/`+1D2`<sub>h</sub> and `+1DE`<sub>h</sub>/`+1D6`<sub>h</sub>) it ends the movement context's `+74`<sub>h</sub> or `+220`<sub>h</sub> job
   (`0024CFF0`) and zeroes it.
2. For the class-3 range it also runs `002693D0(record, 1)`, the per-`+04`<sub>h</sub> teardown (`002E3AF0`,
   `003DE5F0` or `002E3D00` for 1, 2 or 3) and sets the `+04`<sub>h</sub> word to `FF00`<sub>h</sub>; then for every
   record with `+14`<sub>h</sub> bit 7 and a unit at `+30`<sub>h</sub> it releases the unit (`00234200`) and runs
   `002EB780`.
3. The owning release: the block at `[slot + 08h]` is freed with `003697F0`, the pointer nulled,
   the slot's `+10`<sub>h</sub> bit 0 and `+200`<sub>h</sub> bit 2 cleared and `+13`<sub>h</sub> zeroed (`00262D96`-`00262DB3`).
4. The slot's `+00`<sub>h</sub>, `+30`<sub>h</sub>, `+E8`<sub>h</sub>, `+1E0`<sub>h</sub> and `+1FC`<sub>h</sub> are zeroed and `+17`<sub>h</sub> bit 3 is
   cleared; the live-slot totals `02099DB4`/`02099DB8` and the flag `02099DA1` are recomputed over
   slots 0-2; the slot's `+108`<sub>h</sub> callback is called once with the slot and then nulled.

Every record address and interior pointer is valid only until that release.

### What else the teardown resets

Besides the record pool, `002628B0(slot)` resets state that other systems keep per manager slot,
and on slot 0 state that belongs to the field. Among its calls, in order:

| Call | Runs for | What it clears |
|---|---|---|
| `003EC5F0` | slot 0 | calls `003EB6C0(i)` for `i` = 0-15, each only while `00377C20()` is 0 |
| `003EC690` | slot 0 | releases the trap marker resource `02B5EC94` (`002EBD60(id, 0)`, `002E3DC0`) and zeroes it ([traps](../World-Areas-And-Travel/traps.md)) |
| `003DC710` | slots 0 and 3 | each of the 16 entries of `14`<sub>h</sub> bytes at `02B57F74` with state byte `+02`<sub>h</sub> = 3, byte `+03`<sub>h</sub> = 0 and word `+00`<sub>h</sub> = 0 gets `+10`<sub>h</sub> added to its dword `+04`<sub>h</sub> (`byte +0Fh \| 10h` when bits 4-19 come out 0), state 4, and `02B58170` = 1 |
| `003605A0(slot)` | a bound slot | the slot's eight skip entries at `022CB730 + slot * 80h` (byte `+0` = index, `+1` = slot, `+2` and qword `+8` = 0) and its armed and executed masks `022CB9C0` and `022CB9D8` ([cutscenes](../Scripts-And-Script-Commands/cutscenes-and-the-world-lock.md)) |
| `003E9970(slot)` | a bound slot | stops (`003E98B0(i)`) each of the 64 voice slots at `02B5D0B0` whose byte `+05`<sub>h</sub> is the slot ([voices](../Sound-And-Music/voices.md)) |
| `003B6C20` | a bound slot | the summon group's requested count `02EBCC60`, its 32 handles at `02EBCBE0`, the unique count `02EBCBC0`, the leader handle `02EBCC70`, the 32 bytes `02EBCA80`-`02EBCA9F` and the dword `02EBCAA0` |
| `003DEE10(slot)` | a bound slot, twice | the slot's eight event-sound entries at `02B59360 + (slot * 8 + i) * 38h`, below |
| `0036DE70(slot)` | a bound slot | each of the 32 script effect slots at `022D94B0` whose byte `+08`<sub>h</sub> is the slot and whose word `+04`<sub>h</sub> has a bit other than bit 2 gets word `+04`<sub>h</sub> = 4 and, when `003B24C0` returns 0 for its handle `+00`<sub>h</sub>, `003B18E0(handle)` ([native commands](../Scripts-And-Script-Commands/native-commands.md)) |
| `0036E080(slot)` | a bound slot | zeroes every dword of the three 64-dword tables `022D97B0`, `022D98B0` and `022D99B0` whose bits 16-19 are the slot |
| `003E91D0` | a bound slot | when slot `+B8`<sub>h</sub> is set: `002A7A40(slot +C0h)` clears bit 0 of `0209C510 + i * 20h` and runs `0024A680(qword 0209C518 + i * 20h, 0)`; then `+B8`<sub>h</sub> = 0 |
| `002E2300(0)` | a bound slot | jumps to the `ret` stub `0016D6A0` |
| `00368AA0(3, 1)` | slot 0 | clears bit 3 of `02EC0B39` (`00368AA0(bit, on)` clears the bit for a non-zero `on` and sets it otherwise; the movie verbs and `setflickerfreemode` also call it) |
| direct stores | slot 0 | `02099DA4` and `02099DA5`, the pair `set_force_char_nearfade` writes, = 0 |
| `003EBD70` | slot 0 | `02B5EC60` = 0, frees the block `02B5EC68` and zeroes `02B5EC70`-`02B5EC8F` |
| `003604D0` | slot 0, when `003603C0()` is non-zero | every slot's skip entries and masks, as `003605A0` does for one, and `022CB9BC` = 0 |
| `0025A280(2, 0)` | slot 0 | dword `020973F0 + 2 * 110h + 4` = 0 and, when it was not 0, dword `02098570 + 4` = 0 |
| `002E63D0` | slot 0 | the keep bit 4 of `+19`<sub>h</sub> in all 128 binding entries ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)) |
| `003EA200` | slot 0 | with the expanded voice memory `02B5E0B0` held: stops each voice slot whose byte `+07`<sub>h</sub> is 12 and whose state byte `+04`<sub>h</sub> is 2, 3 or 4 (`0032E520(0)` first for 2 and 4), runs `0036D160(Ch)` and frees the block |
| `003E9100` | slot 0 | `00408200` when `02B5D090` is set, then `02B5D090` = 0 |
| `002E1630` | slot 0 | returns -1 when `00290180()` is 0, 1 when it is 2 and 0 otherwise; a non-zero value triggers a checked indirect call |
| `0036A280` | slot 0 | writes 0-14 into the 15 bytes at `022D89A8` |
| `002E06F0` | slot 0 | the 8 records of `68`<sub>h</sub> bytes at `0215F200`: a live one (qword `+00`<sub>h</sub> set) runs `002A2720`, gets dword `+08`<sub>h</sub> = 6, and `002F1C50` when its byte `+40`<sub>h</sub> is -1; every byte `+40`<sub>h</sub> becomes `FE`<sub>h</sub> |
| `0035AB50(0)` | slots 1-3 | slot 0's model list, below |

Each event-sound entry is handled by its state byte `+10`<sub>h</sub>: 1 frees its two blocks `+08`<sub>h</sub> and
`+18`<sub>h</sub>; 5 also releases the block's ids (`002DF050`) and words (`002DEB40`) first; 2, 3 and 4 are
waited out (`00379E30`, `002DEE90`, `0032E520(0)`, `003DEB30`, `0035EA30`) and re-tested. A released
entry gets state 0 and its bit cleared in `02B59C20[slot]`. `003DEC90(slot, i)`, the release the
`eventsounddispose` verb (`0154`<sub>h</sub>) runs, does the same for one entry, except that it hands an
entry in state 1 to `003DEFC0`.

`0035AB50(slot)`, with that slot made current, walks the list of `{name, mask}` pairs the payload's
dword `+80`<sub>h</sub> names: for each name that resolves to a binding entry it clears the entry's `+19`<sub>h</sub>
bit 0 and, for each bit `i` from 1 to 31 set in the mask, releases the hold on lane `i` and then on
lane 0 (`002ECAB0(id, i, 0)`, `002ECAB0(id, 0, 0)`).

The teardown always passes slot 0 to `0035AB50`, after the
keep and hold clears the [area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)
page describes. Slot 0's own unload `0025AFC0` runs the same tail and then `002ECBE0(0)` and
`002EBDE0(0)`, which call `0036C5D0(handle, 0)` on the 32 handles at `+60`<sub>h</sub> of every node of the
list `0215FD68` and on the handle `+10`<sub>h</sub> of every node of the list `0215FD58`.

## Layouts

Struct ActorRecord size=by sequence (`2D0`<sub>h</sub> to `6E0`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u16` | index | the record's ordinal in its manager |
| `002`<sub>h</sub> | `u8` | entryClass | 1 or 2 from the initialiser |
| `003`<sub>h</sub> | `u8` | classAndSequence bits 5-7 class, bits 0-4 sequence |  |
| `004`<sub>h</sub> | `u16` | definitionState | `FF00`<sub>h</sub> at init and at release |
| `006`<sub>h</sub> | `u16` | channelActiveMask |  |
| `008`<sub>h</sub> | `u8` | flags08 | bit 6 set by the field runtime's roster and record loops |
| `00A`<sub>h</sub> | `u8` | field0A | 0 at init |
| `009`<sub>h</sub> | `u8` | flags09 |  |
| `00B`<sub>h</sub> | `u8` | flags0B |  |
| `00C`<sub>h</sub> | `u8` | flags0C | bit 0 the wait resolver's id match |
| `00D`<sub>h</sub> | `u8` | flags0D | bit 6 set while the +`38`<sub>h</sub> callback runs |
| `00E`<sub>h</sub> | `u8` | flags0E | bits 0-3 the class nibble (`00263C20`): 4 class 1, 5 class 3 (`00265FF0`) |
| `010`<sub>h</sub> | `u8` | pendingRequests | resource requests the initialiser issued; 0 = idle for the field runtime |
| `011`<sub>h</sub> | `i8` | currentWaitSlot |  |
| `012`<sub>h</sub> | `u8` | slotTag | `FF`<sub>h</sub>, or the entry's tag |
| `013`<sub>h</sub> | `u8` | flags13 |  |
| `014`<sub>h</sub> | `u8` | flags14 | bit 4 drive the battle unit, bit 6 settled, bit 7 battle-unit eligible |
| `015`<sub>h</sub> | `u8` | managerIndex |  |
| `016`<sub>h</sub> | `u16` | discriminator | 1 at init |
| `01C`<sub>h</sub> | `u32` | flags1C | seeded by sequence (`00266BD0`) |
| `024`<sub>h</sub> | `u16` | channelMask24 |  |
| `026`<sub>h</sub> | `u16` | channelMask26 |  |
| `030`<sub>h</sub> | `u8*` | battleUnit | `002134A0` |
| `038`<sub>h</sub> | `void* frameCallback` | 00233F70 for a unit-bound record |  |
| `040`<sub>h</sub> | `u8*` | scriptEntry | the payload's entry for this actor |
| `048`<sub>h</sub> | `u8*` | functionTable | payload + entry +`10`<sub>h</sub> |
| `050`<sub>h</sub> | `u8*` | jumpTable | payload + entry +`14`<sub>h</sub> |
| `058`<sub>h</sub> | `u8*` | bytecodeBase | payload + entry +`08`<sub>h</sub> |
| `060`<sub>h</sub> | `u8` | entryFreeListHead |  |
| `061`<sub>h</sub> | `u8` | detachedEntryListHead |  |
| `062`<sub>h</sub> | `u8` | selectedEntryIndex |  |
| `063`<sub>h</sub> | `u8` | entryListFlags |  |
| `064`<sub>h</sub> | `i32[4] vmRegI` | the script VM's integer registers |  |
| `074`<sub>h</sub> | `f32[4] vmRegF` | the script VM's float registers |  |
| `088`<sub>h</sub> | `u8` | channelCount | 8 or 6 |
| `089`<sub>h</sub> | `u8` | entryCount | 10 or 8 |
| `08C`<sub>h</sub> | `u8[8]` | channelTail |  |
| `094`<sub>h</sub> | `u8[8]` | channelHead |  |
| `0A0`<sub>h</sub> | `u8*` | resourceEntries | 20-byte entries |
| `0A8`<sub>h</sub> | `u8*` | waitSlots | 40-byte slots (field runtime page) |
| `0B8`<sub>h</sub> | `u8*` | movementContext | `230`<sub>h</sub> bytes at +`120`<sub>h</sub> |
| `0C0`<sub>h</sub> | `u8*` | secondaryContext `188`<sub>h</sub> bytes at `+350`<sub>h</sub>, class 3 only |  |
| `0C8`<sub>h</sub> | `u16[18] overrides` | `FFFF`<sub>h</sub> at init |  |
| `0F6`<sub>h</sub> | `u16` | entryGroup | 0 at init; stamped by `0026CE60` |
| `0F8`<sub>h</sub> | `u8*` | nameText | the literal name (npc-names page) |
| `100`<sub>h</sub> | `u16` | nameLength |  |
| `102`<sub>h</sub> | `i16` | nameId |  |
| `118`<sub>h</sub> | `u32` | field118 | `3C0000`<sub>h</sub> at init |

Struct ActorResourceEntry size=`14`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | next |  |
| `01`<sub>h</sub> | `u8` | prev |  |
| `02`<sub>h</sub> | `i8` | channel | negative: on the detached list |
| `04`<sub>h</sub> | `u16` | resourceId |  |
| `06`<sub>h</sub> | `u16` | field06 | `8000`<sub>h</sub> when unset |
| `10`<sub>h</sub> | `u8` | state | 3 a request in flight, 4 detached |
| `12`<sub>h</sub> | `u8` | classAndFlag the class in bits 1-7 |  |

## Operations

- The pool is one allocation per manager; the record count, the per-class counts and the carve
  order all come from the payload's sequence table, and the class is stamped before any record is
  initialised.
- Interior pointers (`+A0`<sub>h</sub>, `+A8`<sub>h</sub>, `+B8`<sub>h</sub>, `+C0`<sub>h</sub>) point into the record itself and are valid
  for the life of the block.

## Modding notes

- A script's actor counts set the pool: adding an actor to a scene means adding it to the payload's
  sequence table, which sizes the block.
- Only class-3 records carry a secondary context and can be steered; a class-1 record has a
  position but no steering, a class-2 record is a trigger line.
- Hold a handle, not a record pointer, across a field change: the block is freed at unload.

## Related

- [Actor record fields](actor-record-fields.md): every reached offset and the two contexts' access tables.
- [Actor managers](actor-managers.md): the slot the pool belongs to.
- [Field runtime](field-runtime.md): the wait slots and the drive loops.
- [Battle units](battle-units.md): the unit bound at `+30`<sub>h</sub> and the handle.
- [NPC names](npc-names.md): `+F8`<sub>h</sub> and `+102`<sub>h</sub>.
