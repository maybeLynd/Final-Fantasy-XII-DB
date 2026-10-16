---
title: "Battle log: which result posts which battle message, the repeat limit and the 24-unit visibility rule"
kind: "system"
category: "Battle actions"
addresses: "00385BA0, 00469EC0, 0046AB10, 00469570, 002FA3B0, 005369C0"
---

## What the player sees

The battle log shows short lines about what just happened: a technick that failed and why, a poach,
an item used on a party member, a status cured, a steal, a level gained. Each line is one row of the
battle message table ([Battle message list](battle-message-list.md)).

- **Far-away fights are quiet.** A line about units more than 24 units from the party leader is
  dropped, unless the message is one of the always-shown ones.
- **No repeats.** Some messages (action cancelled, out of range, the magick field lines) are not
  repeated for the same unit while an earlier copy is less than 450 clock ticks old.
- **Healing off the field.** Using an item on a party member who is not on the field gives the menu's
  lines - HP or MP partially or fully restored, regains consciousness, status cured - and the reserve
  members' lines for party-wide items.

## How it works

### Where the messages come from

The result applier's first step, `00385BA0`, calls `00469EC0(actionId, sourceStats, targetStats,
result)` when the result's byte `+1C`<sub>h</sub> is 1, with the action id from the formula scratch word
`02AEDFD4` (`00385C6F`-`00385C85`). Seventeen other functions post messages directly through the same
poster `0046AB10`: `004697C0`, `004698C0`, `00469A50`, `00469AF0`, `00469BB0`, `00469C00`, `00469E30`,
`00469E80`, `0046A630`, `0046A690`, `0046A6E0`, `0046A720`, `0046A790`, `0046A800`, `0046A870`,
`0046A9D0` and `0046AA70` (48 call sites in all).

### The event context

`00469EC0` (1,904 bytes) builds the context it hands to every post (`00469ED8`-`00469F37`):

| Context offset | Holds |
|---|---|
| `+00`<sub>h</sub> / `+08`<sub>h</sub> | source and target stats records |
| `+10`<sub>h</sub> | the result's `+08`<sub>h</sub> (gil) |
| `+14`<sub>h</sub> | the magnitude of the result's HP value `+24`<sub>h</sub> |
| `+18`<sub>h</sub> | a status number (cure and fade lines) |
| `+1C`<sub>h</sub> | the source's level byte `+1C2`<sub>h</sub> (0 without a source) |
| `+20`<sub>h</sub> | the result's poach item `+38`<sub>h</sub> |
| `+28`<sub>h</sub> | the action id |

### Technick notices

The dispatcher first posts, for the source, one notice per bit of the result's `+140`<sub>h</sub>
(`00469F68`-`00469FDB`):

| Bit of `+140`<sub>h</sub> | Event |
|---:|---:|
| 8 | `36`<sub>h</sub> |
| 9 | `38`<sub>h</sub> |
| 11 | `3A`<sub>h</sub> |
| 10 | `3D`<sub>h</sub> |

### Targets without a battle unit

When the target stats record has no battle unit (`0031B860` returns 0), the dispatcher uses the
menu-style lines (`00469FFF`-`0046A3BF`). A failed result (kind byte `+04`<sub>h</sub> = 6) posts `1D`<sub>h</sub> only
when the target is the source's current target (`+710`<sub>h</sub> through `00320A70`, or `+6B9`<sub>h</sub> through
`00320A40` on the stats-record path), and nothing else.

For the source's current target, actions `0`/`4`, `0B`<sub>h</sub>, `0D`<sub>h</sub>, `0E`<sub>h</sub>, `10`<sub>h</sub> and `67`<sub>h</sub> post
`1E`<sub>h</sub>, `1F`<sub>h</sub>, `20`<sub>h</sub>, `21`<sub>h</sub>, `22`<sub>h</sub> and `23`<sub>h</sub>; those actions post nothing for any other target.
For other actions:

1. Bit 0 of the remove mask `+58`<sub>h</sub> (KO removed) posts `1C`<sub>h</sub>.
2. Otherwise, with HP and MP present (`+2Ch & 4100h`), both at or above their caps, and the
   target having MP at all (bytes `+6C`<sub>h</sub>/`+7C`<sub>h</sub> not negative and `+28`<sub>h</sub> not 0), `17`<sub>h</sub>.
3. Otherwise HP present (`+2Ch & 500h` both set) posts `14`<sub>h</sub> (at the cap) or `13`<sub>h</sub>, and MP
   present (`14000`<sub>h</sub>) posts `16`<sub>h</sub>, `15`<sub>h</sub>, or `1D`<sub>h</sub> when the target has no MP (bytes `+6C`<sub>h</sub>/`+7C`<sub>h</sub>
   negative or `+28`<sub>h</sub> = 0).
4. The removed statuses other than 0 and 29 are counted by bit 13 of the word at `+6` of their row in
   the status table `02EBF118`: one with the bit posts `18`<sub>h</sub>, several `19`<sub>h</sub>; one without posts
   `1A`<sub>h</sub>, several `1B`<sub>h</sub>.

### Targets with a battle unit

For a target with a battle unit, a failed Steal (action `A9`<sub>h</sub>, kind 6) posts `33`<sub>h</sub> when bit 23 of
`+2C`<sub>h</sub> is set and `34`<sub>h</sub> otherwise. For a resolved result (kind 0) whose action kind `+1E`<sub>h</sub> is 2
(Technicks) or 7 (Foecraft), the action id picks the event (`0046A3FF`-`0046A5F9`):

| Action ids | Events |
|---|---|
| `A1`<sub>h</sub>, `A2`<sub>h</sub> | `27`<sub>h</sub>, `28`<sub>h</sub> |
| `A6`<sub>h</sub>, `A7`<sub>h</sub> | `29`<sub>h</sub>, `2A`<sub>h</sub> |
| `AB`<sub>h</sub>, `AC`<sub>h</sub> | `2B`<sub>h</sub>, `2C`<sub>h</sub> |
| `A9`<sub>h</sub> | the stolen-goods lines (`0046A870`) |
| `AD`<sub>h</sub>, `B2`<sub>h</sub>, `A4`<sub>h</sub> | `35`<sub>h</sub>, `37`<sub>h</sub>, `3C`<sub>h</sub> |
| `116`<sub>h</sub>, `117`<sub>h</sub> | `44`<sub>h</sub>, `45`<sub>h</sub> |
| `13F`<sub>h</sub>, `17F`<sub>h</sub>, `119`<sub>h</sub> | `46`<sub>h</sub>, `47`<sub>h</sub>, `48`<sub>h</sub> |
| `144`<sub>h</sub>, `145`<sub>h</sub> | `49`<sub>h</sub>, `4A`<sub>h</sub> |
| `1A1`<sub>h</sub>, `1A0`<sub>h</sub>, `1A7`<sub>h</sub> | `4B`<sub>h</sub>, `4C`<sub>h</sub>, `4D`<sub>h</sub> |

Action `B1`<sub>h</sub> with a target present then posts `3B`<sub>h</sub> (`0046A5FE`-`0046A617`).

### The poster

`0046AB10(stats, event, context)` (371 bytes) handles every message:

1. It drops the message when the context's action id is `1FF`<sub>h</sub> or above, or when the target's unit
   exists and either `02089340` has any of `3080`<sub>h</sub> or the target's battle unit (`0031B860`) has bit `20`<sub>h</sub> of
   byte `+4` (`0046AB19`-`0046AB56`).
2. It drops it when the visibility filter `00469570` returns 0 (`0046AB65`).
3. For a row with bit 0 of byte `+4`, it drops it when one of the ten `20`<sub>h</sub>-byte ring entries at
   `02EBB560` (event `u16` at `+0`, tick at `+4`, stats at `+8`) holds the same event and stats and
   its tick plus `450 * [01DFE0B4]` is still ahead of `0032A150()` (`0046ABB3`-`0046ABF5`).
4. It records `{event, tick, stats}` in the ring entry `[02EBB54C]`, advances that index modulo 10,
   and calls `005369C0(stats, event, context)` (`0046AC00`-`0046AC66`).

The area initialisation `002342F0` empties the ring through `0033A380` (`00234463`), which calls
`004696A0` (`0033A3B0`): every entry's event becomes `FFFF`<sub>h</sub>, its tick, stats and word `+18`<sub>h</sub> 0,
and the index `02EBB54C` 0 (`004696A0`-`004697BB`).

### The visibility filter

`00469570(event, source, target)` returns 1 at once when byte `+3` of the event's row has bit 7
(`004695F9`). Otherwise it returns `002FA3B0` for the source's actor, or for the target's when the
source has no unit, and 1 when neither has one. `002FA3B0(actor)` is true when the actor is less than
24.0 (`008F3128`) units from the party leader, measured with height zeroed (`003A1920`); with no leader
it uses the leader position last stored at `01EEBB00` (`002FA3E2`-`002FA451`).

### Building the line

`005369C0(stats, event, context)` (1,000 bytes) fills four 16-byte argument slots from the row's
bytes `+0`, `+1`, `+2` and `+5` (`00536A51`-`00536BBC`):

| Slot kind | Argument |
|---:|---|
| 1, 2 | the source's or the target's name (`00536310`) and a byte from its actor (`00263A10`) |
| 3, 4, 5, 6, 7, 8, 9 | the context dword at `+10`<sub>h</sub>, `+14`<sub>h</sub>, `+18`<sub>h</sub>, `+1C`<sub>h</sub>, `+20`<sub>h</sub>, `+28`<sub>h</sub>, `+24`<sub>h</sub> |

It passes bits 2-6 of row byte `+3` as a category (`00536C6F`), marks events `24`<sub>h</sub> and `25`<sub>h</sub>, and
hands the request to the formatter `00536410` and the poster `0035B990`. `00536410` turns kind 5
into a status name, kind 7 into an item name or a number (`E000`<sub>h</sub> + n), and kind 8 into an action
name; kind 4 is formatted through a sub-template taken from the message table's text heap
(`002B4090`).

The helpers behind those arguments:

- `00536310(stats, &flag)` gives the name id. For a unit whose actor has a name id of 0 or more
  (`00267410`), it returns the actor's `i16` at `+102`<sub>h</sub>, read by `00263B40`, and sets `flag`
  (`005363A5`-`005363D6`); for any other unit, the `u16` at `+8` of its `[+E60h]` record
  (`005363DC`-`005363F0`). A stats record with byte `+05`<sub>h</sub> = 0 reads word `+30`<sub>h</sub> of its row in the
  table `[02EBF130]` instead (`00536345`-`00536388`).
- For kind 7, when the language test `00254A10` is true, `00536410` takes the item name from
  `00309E70(id)` (`00536769`-`00536777`). That fills a class-1 query record (`0031C5D0`) and returns
  its name through `002B58B0`, or the empty string `01CEB638` when the fill fails
  (`00309E70`-`00309EB7`).
- `0035B990` takes the request's text through `00393740` on both of its paths (`0035B9CD`,
  `0035BA07`). `00393740` returns null unless the request's first dword is 7 and its text pointer
  `+28`<sub>h</sub> is set; otherwise it copies the text through a 384-byte buffer into the caller's buffer
  (`0039375F`-`00393795`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | slot0 | argument kind of slot 0 (`005369C0`, `00536410`) |
| `01`<sub>h</sub> | `u8` | slot1 | argument kind of slot 1 |
| `02`<sub>h</sub> | `u8` | slot2 | argument kind of slot 2 |
| `03`<sub>h</sub> | `u8` | flags3 | bit 7: always shown (`00469570`); bits 2-6: category (`005369C0`); bits 0-1 dropped by `005369C0` |
| `04`<sub>h</sub> | `u8` | flags4 | bit 0: repeat-limited (`0046AB10`) |
| `05`<sub>h</sub> | `u8` | slot3 | argument kind of slot 3 |
| `06`<sub>h</sub> | `u16` | zero6 | 0 in every shipped row |

## Related

- [Battle message list](battle-message-list.md) - every row of the table with its text.
- [Action results](action-results.md) - the record the dispatcher reads.
- [Target selection](target-selection.md) - the same 24-unit distance used for targets.
