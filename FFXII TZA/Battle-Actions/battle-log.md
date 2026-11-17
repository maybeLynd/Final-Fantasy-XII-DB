---
title: "Battle log: which result posts which battle message, the repeat limit and the 24-unit visibility rule"
kind: "system"
category: "Battle actions"
addresses: "0x00385BA0, 0x00469EC0, 0x0046AB10, 0x00469570, 0x002FA3B0, 0x005369C0"
---

## What the player sees

The battle log shows short lines about what just happened: a technick that failed and why, a poach,
an item used on a party member, a status cured, a steal, a level gained. Each line is one row of the
battle message table ([Battle message list](battle-message-list.md)).

- **Far-away fights are quiet.** A line about units more than 24 units from the party leader is
  dropped, unless the message is one of the always-shown ones.
- **No repeats.** Some messages (action cancelled, out of range, the magick field lines) are not
  repeated for the same unit while an earlier copy is less than 450 frames old (450 clock ticks at
  30 fps, 900 at 60) and is still among the last ten messages posted. A dropped repeat does not
  restart the wait.
- **Healing off the field.** Using an item on a party member who is not on the field gives the menu's
  lines - HP or MP partially or fully restored, regains consciousness, status cured - and the reserve
  members' lines for party-wide items.

Each line starts from an action's result, and the game picks the message row from what the result holds. It then fills
the row's blanks with the names of the units involved and with the amount, status, item, level or action from that
result.

## How it works

### Where the messages come from

The result applier's first step, `0x00385BA0`, calls `0x00469EC0(actionId, sourceStats, targetStats,
result)` when the result's byte `+0x1C` is 1, with the action id from the formula scratch word
`0x02AEDFD4` (`0x00385C6F`-`0x00385C85`). Seventeen other functions post messages directly through the same poster `0x0046AB10`: `0x004697C0`, `0x004698C0`,
`0x00469A50`, `0x00469AF0`, `0x00469BB0`, `0x00469C00`, `0x00469E30`, `0x00469E80`, `0x0046A630`, `0x0046A690`, `0x0046A6E0`,
`0x0046A720`, `0x0046A790`, `0x0046A800`, `0x0046A870`, `0x0046A9D0` and `0x0046AA70` (38 call sites; with the ten in `0x00469EC0`,
48 in all).

`0x004697C0(stats, action, previous action, kind)` posts through `0x0046AB10(stats, event, context)` with a 48-byte
context, zeroed, that holds the stats record at `+0x00` and the action at `+0x28` (`0x004697D4`-`0x004697FB`). It first
calls `0x002F8E90(stats)` (`0x004697FF`).

When that answers 1, the kind is 4, the previous action is below `0x21F` and the action is `0x4022` or `0x4124`, it
puts the previous action at `+0x28` and posts nothing when the stats record and the action are those it kept at
`0x02CA6028` and `0x02CA6030`; otherwise it keeps them there and posts event 6 unless the previous action is `0x96`
(`0x00469804`-`0x0046985D`, `0x00469894`-`0x004698A1`).

Any other call posts only for an action below `0x21F`; it then calls `0x002F8E90(stats)` again and posts only when that
answers 1 and the action is not `0x96`: event 5 for kind 1, 7 for kind 2 and 6 for kind 3, and nothing for any other
kind (`0x0046985F`-`0x004698A1`). So the kind-0 call of `0x00307BE0` posts nothing, and the kind-1 call of `0x0030AF30`, the
timeout cancel of [Target selection](target-selection.md), can post event 5.

`0x0046A6E0(n)` posts `0x0046AB10(0, 0x5D + n, context)` for the low 16 bits of `n` with a context of 48 zero bytes
(`0x0046A6E7`-`0x0046A70D`).

### The event context

`0x00469EC0` (1,904 bytes) builds the context it hands to every post (`0x00469ED8`-`0x00469F37`):

| Context offset | Holds |
|---|---|
| `+0x00` / `+0x08` | source and target stats records |
| `+0x10` | the result's `+0x08` (gil) |
| `+0x14` | the magnitude of the result's HP value `+0x24`; from the MP lines on, that of its word `+0x2A` (`0x0046A2A6`) |
| `+0x18` | a status number (cure and fade lines) |
| `+0x1C` | the source's level byte `+0x1C2` (0 without a source) |
| `+0x20` | the result's poach item `+0x38` |
| `+0x28` | the action id |

`0x00469EC0` keeps the battle units it looks up at `0x00469F48` and `0x00469F5C` at `0x02EBF188`: the source's, only for a
source whose byte `+0x05` is not 0, and then, for a target that is not null, the target's (`0x00469F3A`-`0x00469F61`). The
look-ups of the source's unit below store it there too; the look-up of the target's unit at `0x00469FF1` is only tested.

### Technick notices

The dispatcher first posts, for the source, one notice per bit of the result's `+0x140`
(`0x00469F68`-`0x00469FDB`):

| Bit of `+0x140` | Event |
|---:|---:|
| `0x100` | `0x36` |
| `0x200` | `0x38` |
| `0x800` | `0x3A` |
| `0x400` | `0x3D` |

### Targets without a battle unit

When the target stats record is not null and has no battle unit (`0x0031B860` returns 0), the dispatcher uses the
menu-style lines (`0x00469FE5`-`0x00469FF9`); a null target takes the path of [Targets with a battle
unit](#targets-with-a-battle-unit).

The source's current target comes from the source's battle unit `0x0031B860(source)`, kept at `0x02EBF188`:
`0x00320A40(byte +0x6B9)` when its byte `+0x6B6` is not 0, else `0x00320A70(dword +0x710)`. Before reading either it looks
the unit up again; finding none it calls `0x00320A40(-1)` on the `+0x6B9` path and has no current target on the `+0x710`
path. With no source unit there is no current target (`0x0046A00A`-`0x0046A07C`, `0x0046A10C`-`0x0046A180`).

A failed result (kind byte `+0x04` = 6) posts `0x1D` only when the target is the source's current target, and nothing
else (`0x00469FFF`-`0x0046A08A`). For any other result the dispatcher first works out the new HP and MP and their caps
(`0x0046A08F`-`0x0046A109`).

The new HP is the result's `+0x24` when bit `0x8` of `+0x2C` is set, else the target's `+0x48` plus it; the new MP is
the result's word `+0x2A` when bit `0x10` is set, else the target's word `+0x4C` plus it. The HP cap is the target's
`+0x48`, raised to 1 when below it, when bit `0x10000` of its dword `+0x64` or `+0x3C` is set; otherwise its `+0x24`,
or `+0x24 * 2` when bit `0x10000000` of those is set. The MP cap is its word `+0x28`, or 0 when byte `+0x6C` or
`+0x7C` is negative.

For the source's current target, actions `0`/`4`, `0x0B`, `0x0D`, `0x0E`, `0x10` and `0x67` post `0x1E`, `0x1F`,
`0x20`, `0x21`, `0x22` and `0x23` (`0x0046A180`-`0x0046A1E5`); those actions post nothing for any other target
(`0x0046A1EA`-`0x0046A202`). For other actions:

1. Bit `0x1` of the remove mask `+0x58` (KO removed) posts `0x1C` with context `+0x18` set to 0
   (`0x0046A208`-`0x0046A216`).
2. Otherwise, with HP or MP present (either bit of `+0x2C & 0x4100`), the new HP and the new MP at or above their caps
   (signed compares), and the target having MP at all (bytes `+0x6C`/`+0x7C` not negative and word `+0x28` not 0),
   `0x17` (`0x0046A21B`-`0x0046A252`).
3. Otherwise HP present (`+0x2C & 0x500` both set) posts `0x14` (the new HP at the cap or above) or `0x13`, with
   context `+0x14` set to the magnitude of `+0x24` (`0x0046A257`-`0x0046A287`). MP present (`0x14000` both set) is a
   separate test, so one result can post both: `0x16` (the new MP at the cap or above), `0x15`, or `0x1D` when the
   target has no MP, with `+0x14` set to the magnitude of word `+0x2A` (`0x0046A28C`-`0x0046A2E4`).
4. After items 1-3, whether or not they posted, the removed statuses of `+0x58` other than 0 and 29 are counted by bit
   `0x2000` of the word at `+6` of their row in the status table `0x02EBF118`, a row worked out as in `0x0046AB10`, at
   address 0 without the table (`0x0046A2E9`-`0x0046A36E`).

Of the counted statuses, one with the bit posts `0x18` with `+0x18` set to that status, several `0x19`; then one
without posts `0x1A` with `+0x18` set to that status, several `0x1B`, so a result can post one line of each group
(`0x0046A370`-`0x0046A3BF`).

### Targets with a battle unit

For a target with a battle unit, and for a null target, a failed Steal (action `0xA9`, kind 6) posts `0x33` when bit
`0x800000` of `+0x2C` is set and `0x34` otherwise (`0x0046A3C4`-`0x0046A3F0`); a result of any kind but 0 ends there
(`0x0046A3F5`-`0x0046A3F9`). For a resolved result (kind 0) whose action row's byte `+0x1E` is 2 (Technicks) or 7
(Foecraft), the action id picks the event (`0x0046A3FF`-`0x0046A5F9`). The row is worked out from the action table
`[0x02EBF138]` as in `0x0046AB10`, once for each of the two tests, and is 0 without the table:

| Action ids | Events |
|---|---|
| `0xA1`, `0xA2` | `0x27`, `0x28` |
| `0xA6`, `0xA7` | `0x29`, `0x2A` |
| `0xAB`, `0xAC` | `0x2B`, `0x2C` |
| `0xA9` | the stolen-goods lines, `0x0046A870(0xA9, source, target, result)` |
| `0xAD`, `0xB2`, `0xA4` | `0x35`, `0x37`, `0x3C` |
| `0x116`, `0x117` | `0x44`, `0x45` |
| `0x13F`, `0x17F`, `0x119` | `0x46`, `0x47`, `0x48` |
| `0x144`, `0x145` | `0x49`, `0x4A` |
| `0x1A1`, `0x1A0`, `0x1A7` | `0x4B`, `0x4C`, `0x4D` |

Action `0xB1` with a target present then posts `0x3B` (`0x0046A5FE`-`0x0046A617`).

### The poster

`0x0046AB10(stats, event, context)` (371 bytes) handles every message:

1. It drops the message when the context's action id is `0x1FF` or above, or when the target's unit
   exists and either `0x02089340` has any of `0x3080` or the target's battle unit (`0x0031B860`) has bit `0x20` of
   byte `+4` (`0x0046AB19`-`0x0046AB56`).
2. It drops it when the visibility filter `0x00469570` returns 0 (`0x0046AB65`).
3. For a row with bit `0x1` of byte `+4`, it drops it when one of the ten 0x20-byte ring entries at
   `0x02EBB560` (event `u16` at `+0`, tick at `+4`, stats at `+8`) holds the same event and stats and
   its tick plus `450 * [0x01DFE0B4]` is still ahead of `0x0032A150()` (`0x0046ABB3`-`0x0046ABF5`).
4. It records `{event, tick, stats}` in the ring entry `[0x02EBB54C]`, advances that index modulo 10,
   so ten later posts of any message overwrite an entry; a message dropped in steps 1-3 records nothing
   (`0x0046ABF5` jumps to the exit `0x0046AC6B`),
   and calls `0x005369C0(stats, event, context)` (`0x0046AC00`-`0x0046AC66`).

The row of step 3 is the event's row of the table of `[0x02EBF018]`: it calls `0x0020E600([0x02EBF018] dword +0xC)` twice,
tests only the first answer for null, and takes the low 32 bits of the second plus the stride word `+8` times the
event, a 32-bit sum (`0x0046AB72`-`0x0046ABAD`). With `[0x02EBF018]` null or a null first answer the row address is 0
(`0x0046AB81`, `0x0046AB8E`, `0x0046ABB1`) and the test at `0x0046ABB3` reads the byte at address 4.

The area initialisation `0x002342F0` empties the ring through `0x0033A380` (`0x00234463`), which calls
`0x004696A0` (`0x0033A3B0`): every entry's event becomes `0xFFFF`, its tick, stats and word `+0x18` 0,
and the index `0x02EBB54C` 0 (`0x004696A0`-`0x004697BB`).

### The visibility filter

`0x00469570(event, source, target)` returns 1 at once when byte `+3` of the event's row has bit `0x80`
(`0x004695F9`); the test is skipped when the table at `0x02EBF018` or its row does not resolve (`0x00469595`-`0x004695C6`).
Otherwise it returns `0x002FA3B0` for the source's actor (the unit's `+0x10`), or for the target's when the
source has no unit or that unit has no actor, and 1 when neither has one (`0x00469603`-`0x00469685`). Each unit it finds
through `0x0031B860` is kept at `[0x02EBF188]` (`0x00469610`, `0x0046962A`, `0x00469651`, `0x0046966B`).

`0x002FA3B0(actor)` returns 0 for a null actor (`0x002FA3CB`); otherwise it is true when the actor is less than
24.0 (`0x008F3128`) units from the party leader, measured with height zeroed (`0x003A1920`); with no leader
it uses the leader position last stored at `0x01EEBB00` (`0x002FA3E2`-`0x002FA451`).

Both positions come through `0x00265020`, which copies an object's position only when the object is not null and its
kind (byte `+3` >> 5) is 1 or 3 (`0x00265020`-`0x00265051`), and stores (0, 0, 0) otherwise (`0x00265052`-`0x0026505C`). A
leader whose `+0x10` object fails that test sets `0x01EEBB00`-`0x01EEBB08` to 0 (`0x002FA405`), and an actor that is not
null but of a kind other than 1 or 3 is measured from (0, 0, 0) (`0x002FA426`).

### Building the line

`0x005369C0(stats, event, context)` (1,000 bytes) first builds a header for the formatter: its word `+0x00` is
`0x00264ED0(0x003148F0())`, and its dword `+0x04` takes the event in bits `0x7FFF` and the low bit of `0x002FA390(stats)` in
bit `0x8000`; the dword store writes bits 16-31 back as the stack held them (`0x005369F0`-`0x00536A45`). It then fills
four 16-byte argument slots after the header from the row's bytes `+0`, `+1`, `+2` and `+5` (`0x00536A51`-`0x00536BBC`);
the row is the event's row of the table `[0x02EBF018]`, worked out as in `0x0046AB10`, and 0 without the table:

| Slot kind | Argument |
|---:|---|
| 1, 2 | the source's or the target's name (`0x00536310`) and a byte from its actor (`0x00263A10`) |
| 3, 4, 5, 6, 7, 8, 9 | the context dword at `+0x10`, `+0x14`, `+0x18`, `+0x1C`, `+0x20`, `+0x28`, `+0x24` |

A slot of kind 1 or 2 gets the name id `0x00536310(record, slot)` at its word `+0x08`, that call's flag going to the
slot's byte `+0x00`. Its byte `+0x01` is `0x00263A10(unit qword +0x10)` for the record's battle unit `0x0031B860(record)`,
kept at `0x02EBF188`, and 0 for a null record, a record whose byte `+0x05` is 0, or one without a unit or actor
(`0x00536B17`-`0x00536B6E`). A kind outside 1-9 gives a dword 0 (`0x00536AFE`-`0x00536B03`, `0x00536BA1`).

`0x005369C0` then zeroes the request for the poster `0x0035B990(request)` and puts 7 in its first dword, calls the
formatter `0x00536410(header, text, 0x180, 1)` for a `0x180`-byte text (`0x00536BC2`-`0x00536C06`), and fills the request:
the text pointer at `+0x28`, -1 at dword `+0x20`, and at words `+0x1A`, `+0x1C` and `+0x30` the context's words
`+0x28`, `+0x14` and `+0x2C` (`0x00536C0B`-`0x00536C31`). It posts the request at the end (`0x00536D74`-`0x00536D79`).

The request's byte `+0x1F` is the category, bits `0x7C` of the row's byte `+3` shifted down by 2 (the byte at address
3 without the table), and events `0x24` and `0x25` set its word `+0x32` to 1 (`0x00536C36`-`0x00536C84`). For a source
that has a battle unit with an actor (`0x0031B860`, kept at `0x02EBF188`; qword `+0x10` not 0), the request's qword
`+0x08` is `0x00536280(name id, flag)` from `0x00536310(source, &flag)`, and its byte `+0x18` the `0x00263A10` byte as for a
slot (`0x00536C89`-`0x00536CF9`).

For the target the request's qword `+0x10` and byte `+0x19` are filled in the same way (`0x00536CFD`-`0x00536D70`).
`0x005369C0` ends with the stack-cookie check `0x00808C40(cookie)` (`0x00536D7E`-`0x00536D88`).

`0x00536410` turns kind 5 into a status name, kind 7 into an item name or a number (`0xE000` + n), and kind 8 into an
action name; kind 4 is formatted through a sub-template taken from the message table's text heap (`0x002B4090`).

The kind 4 sub-template is drawn in two colours chosen by a colour class. `0x00536410` takes the class from
`0x00536190(flag, id)` (`0x00536463`), with the header's dword `+4` split into the flag, bit `0x8000`, and the message id,
the mask `0x7FFF` (`0x00536448`-`0x0053645B`). `0x00536190` reads bits `0x3` of the message row's byte `+3` (`0x005361E2`-`0x005361E6`):

| Bits `0x3` | Class, flag clear | Class, flag set | Sites |
|---:|---:|---:|---|
| `0` | 7 | 7 | `0x005361FD` |
| `1` | 0 | 2 | `0x0053625E`-`0x0053626C` |
| `2` | 1 | 3 | `0x0053623F`-`0x0053624B` |
| `3` | 4 | 5 | `0x00536227`-`0x0053622C` |

`0x00536190` has one more arm, which returns 6 (`0x00536212`), and it is taken when the masked value is 4
(`0x005361F8`-`0x005361FB`), which the mask to bits `0x3` leaves out; so from `0x00536190`'s entry the class is 0-5 or 7.

The kind 4 arm (`0x0053668C`) passes the class to `0x0035D430(class, 0)`, `0x0035D400(class, 0)`, `0x0035D430(class, 1)` and
`0x0035D400(class, 1)` (`0x005366CF`-`0x005366FC`). Each reads entry `2 x class + n` of the byte table `0x00D10C60` and
returns that entry's colour from the menu colour table `0x0215E6C8` (`0x002DD7E0`) or its palette byte (`0x002DD7B0`);
the four values go to `0x002B4090` with the sub-template (`0x00536701`-`0x00536723`).

The table holds `0x18 0x19`, `0x1A 0x1B`, `0x14 0x15`, `0x16 0x17`, `0x1D 0x1D`, `0x1C 0x1C`, `0x1E 0x1E` and
`0x1F 0x1F` for classes 0-7.

The helpers behind those arguments:

- `0x00536310(stats, &flag)` gives the name id. For a unit whose actor has a name id of 0 or more
  (`0x00267410`), it returns the actor's `i16` at `+0x102`, read by `0x00263B40`, and sets `flag`
  (`0x005363A5`-`0x005363D6`); for any other unit, the `u16` at `+8` of its `[+0xE60]` record
  (`0x005363DC`-`0x005363F0`). A stats record with byte `+0x05` = 0 reads word `+0x30` of its row in the
  table `[0x02EBF130]` instead (`0x00536345`-`0x00536388`).
- For kind 7, when the language test `0x00254A10` is true, `0x00536410` takes the item name from
  `0x00309E70(id)` (`0x00536769`-`0x00536777`). That fills a class-1 query record (`0x0031C5D0`) and returns
  its name through `0x002B58B0`, or the empty string `0x01CEB638` when the fill fails
  (`0x00309E70`-`0x00309EB7`).
- `0x0035B990` takes the request's text through `0x00393740` on both of its paths (`0x0035B9CD`,
  `0x0035BA07`). `0x00393740` returns null unless the request's first dword is 7 and its text pointer
  `+0x28` is set; otherwise it copies the text through a 384-byte buffer into the caller's buffer
  (`0x0039375F`-`0x00393795`).

`0x0035B990(request)` reads the text with `0x00393740(request, buffer, 0x180)`. With the request's word `+0x30` not 0 it
only copies the text, `0x00254F30(object + 0x568, text, 0x180)`, to the object `[0x022CA430]`, when there is one, after
zeroing the byte at `[0x022CA430] + 0x568`; nothing is posted (`0x0035B9AB`-`0x0035B9FA`).

Otherwise, when `0x00254A10()` answers 0 and the word `+0x32` is not 0, `0x0035B990` builds a second text with
`0x002B5680(0x180, second buffer, buffer)` and `0x002B3050(0, second buffer, &length, 0)`, which replaces the first unless
its length word plus 4 reaches `0x182`, an unsigned compare (`0x0035B9FF`-`0x0035BA65`).

The text then goes to `0x0028E110(text, byte +0x1F, 0, 0)` (`0x0035BA68`-`0x0035BA75`). Every way out passes the
stack-cookie check `0x00808C40(cookie)` (`0x0035BA82`-`0x0035BA8D`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | slot0 | argument kind of slot 0 (`0x005369C0`, `0x00536410`) |
| `+0x01` | `u8` | slot1 | argument kind of slot 1 |
| `+0x02` | `u8` | slot2 | argument kind of slot 2 |
| `+0x03` | `u8` | flags3 | bit `0x80`: always shown (`0x00469570`); bits `0x7C`: category (`0x005369C0`); bits `0x3` dropped by `0x005369C0` and read by `0x00536190` as the colour class of a kind 4 argument (`0x005361E2`) |
| `+0x04` | `u8` | flags4 | bit `0x1`: repeat-limited (`0x0046AB10`) |
| `+0x05` | `u8` | slot3 | argument kind of slot 3 |
| `+0x06` | `u16` | zero6 | 0 in every shipped row |

## State

### The repeat ring

The ring at `0x02EBB560` holds ten `0x20`-byte entries. `0x004696A0` clears every entry field by field
(`0x004696A0`-`0x004697BB`); the poster `0x0046AB10` reads all ten through the ring's address (`0x0046ABB7`) and writes the
entry the index `0x02EBB54C` names (`0x0046AC00`-`0x0046AC3B`). Every field is 0 in the file (the zero-filled tail of
`.data`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBB580`, `0x02EBB5A0`, `0x02EBB5C0`, `0x02EBB5E0`, `0x02EBB600`, `0x02EBB620`, `0x02EBB640`, `0x02EBB660`, `0x02EBB680` | `u16` each | 0 | `+0x00` of entries 1-9: the event of the message last recorded there; `0xFFFF` when empty | `0x004696A0`, `0xFFFF`; `0x0046AB10`, the event (`0x0046AC0D`, `0x0046AC20`) | `0x0046AB10` (`0x0046ABDA`) |
| `0x02EBB564`, `0x02EBB584`, `0x02EBB5A4`, `0x02EBB5C4`, `0x02EBB5E4`, `0x02EBB604`, `0x02EBB624`, `0x02EBB644`, `0x02EBB664`, `0x02EBB684` | `u32` each | 0 | `+0x04` of entries 0-9: the tick from `0x0032A150` when the message was recorded | `0x004696A0`, 0; `0x0046AB10` (`0x0046AC0D`, `0x0046AC3B`) | `0x0046AB10`, which adds `450 x [0x01DFE0B4]` and compares the sum with the tick now (`0x0046ABF0`) |
| `0x02EBB568`, `0x02EBB588`, `0x02EBB5A8`, `0x02EBB5C8`, `0x02EBB5E8`, `0x02EBB608`, `0x02EBB628`, `0x02EBB648`, `0x02EBB668`, `0x02EBB688` | `void*` each | 0 | `+0x08` of entries 0-9: the stats record the message was about | `0x004696A0`, 0; `0x0046AB10` (`0x0046AC1B`) | `0x0046AB10` (`0x0046ABD4`) |
| `0x02EBB578`, `0x02EBB598`, `0x02EBB5B8`, `0x02EBB5D8`, `0x02EBB5F8`, `0x02EBB618`, `0x02EBB638`, `0x02EBB658`, `0x02EBB678`, `0x02EBB698` | `u16` each | 0 | `+0x18` of entries 0-9: always 0 | `0x004696A0`, a 2-byte 0; `0x0046AB10`, an 8-byte 0 over `+0x18`-`+0x1F` (`0x0046AC16`) | no instruction |

### Other state

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01EEBB04` | `f32` | 0 | the height of the party leader's position kept at `0x01EEBB00` for the visibility filter: `0x002FA3B0` stores the leader's position there, or (0, 0, 0) when the leader's `+0x10` object is null or not of kind 1 or 3 (`0x00265052`-`0x0026505C`), and then zeroes the height | `0x00265020`, through the address (`0x002FA3F7`); `0x002FA3B0` (`0x002FA40A`) | `0x003A1920`, the distance, through the address `0x01EEBB00` (`0x002FA42B`) |
| `0x02CA6028` | `void*` | 0 | the stats record of the last resumed gambit commit for which `0x004697C0` was called with kind 4, a previous action below `0x21F`, action `0x4022` or `0x4124` and `0x002F8E90` answering 1 (`0x004697FF`-`0x0046982A`) | `0x004697C0` (`0x0046984A`) | `0x004697C0` (`0x0046982C`) |
| `0x02CA6030` | `u16` | 0 | that call's action; a call with the same stats record and action posts nothing (`0x0046982C`-`0x00469843`), and any other posts event 6 unless the previous action is `0x96` | `0x004697C0` (`0x00469851`) | `0x004697C0` (`0x0046983C`) |

No other instruction reaches these globals.

## Related

- [Battle message list](battle-message-list.md) - every row of the table with its text.
- [Action results](action-results.md) - the record the dispatcher reads.
- [Target selection](target-selection.md) - the same 24-unit distance used for targets.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x00265020` is called by `0x00362850`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Platform online achievements: `0x003148F0` is called by `0x003160C0`; those functions are documented on
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md).
