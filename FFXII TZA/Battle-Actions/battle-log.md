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
  repeated for the same unit while an earlier copy is less than 450 clock ticks old.
- **Healing off the field.** Using an item on a party member who is not on the field gives the menu's
  lines - HP or MP partially or fully restored, regains consciousness, status cured - and the reserve
  members' lines for party-wide items.

## How it works

### Where the messages come from

The result applier's first step, `0x00385BA0`, calls `0x00469EC0(actionId, sourceStats, targetStats,
result)` when the result's byte `+0x1C` is 1, with the action id from the formula scratch word
`0x02AEDFD4` (`0x00385C6F`-`0x00385C85`). Seventeen other functions post messages directly through the same
poster `0x0046AB10`: `0x004697C0`, `0x004698C0`, `0x00469A50`, `0x00469AF0`, `0x00469BB0`, `0x00469C00`, `0x00469E30`,
`0x00469E80`, `0x0046A630`, `0x0046A690`, `0x0046A6E0`, `0x0046A720`, `0x0046A790`, `0x0046A800`, `0x0046A870`,
`0x0046A9D0` and `0x0046AA70` (48 call sites in all).

### The event context

`0x00469EC0` (1,904 bytes) builds the context it hands to every post (`0x00469ED8`-`0x00469F37`):

| Context offset | Holds |
|---|---|
| `+0x00` / `+0x08` | source and target stats records |
| `+0x10` | the result's `+0x08` (gil) |
| `+0x14` | the magnitude of the result's HP value `+0x24` |
| `+0x18` | a status number (cure and fade lines) |
| `+0x1C` | the source's level byte `+0x1C2` (0 without a source) |
| `+0x20` | the result's poach item `+0x38` |
| `+0x28` | the action id |

### Technick notices

The dispatcher first posts, for the source, one notice per bit of the result's `+0x140`
(`0x00469F68`-`0x00469FDB`):

| Bit of `+0x140` | Event |
|---:|---:|
| 8 | `0x36` |
| 9 | `0x38` |
| 11 | `0x3A` |
| 10 | `0x3D` |

### Targets without a battle unit

When the target stats record has no battle unit (`0x0031B860` returns 0), the dispatcher uses the
menu-style lines (`0x00469FFF`-`0x0046A3BF`). A failed result (kind byte `+0x04` = 6) posts `0x1D` only
when the target is the source's current target (`+0x710` through `0x00320A70`, or `+0x6B9` through
`0x00320A40` on the stats-record path), and nothing else.

For the source's current target, actions `0`/`4`, `0x0B`, `0x0D`, `0x0E`, `0x10` and `0x67` post
`0x1E`, `0x1F`, `0x20`, `0x21`, `0x22` and `0x23`; those actions post nothing for any other target.
For other actions:

1. Bit 0 of the remove mask `+0x58` (KO removed) posts `0x1C`.
2. Otherwise, with HP and MP present (`+0x2C & 0x4100`), both at or above their caps, and the
   target having MP at all (bytes `+0x6C`/`+0x7C` not negative and `+0x28` not 0), `0x17`.
3. Otherwise HP present (`+0x2C & 0x500` both set) posts `0x14` (at the cap) or `0x13`, and MP
   present (`0x14000`) posts `0x16`, `0x15`, or `0x1D` when the target has no MP (bytes `+0x6C`/`+0x7C`
   negative or `+0x28` = 0).
4. The removed statuses other than 0 and 29 are counted by bit 13 of the word at `+6` of their row in
   the status table `0x02EBF118`: one with the bit posts `0x18`, several `0x19`; one without posts
   `0x1A`, several `0x1B`.

### Targets with a battle unit

For a target with a battle unit, a failed Steal (action `0xA9`, kind 6) posts `0x33` when bit 23 of
`+0x2C` is set and `0x34` otherwise. For a resolved result (kind 0) whose action kind `+0x1E` is 2
(Technicks) or 7 (Foecraft), the action id picks the event (`0x0046A3FF`-`0x0046A5F9`):

| Action ids | Events |
|---|---|
| `0xA1`, `0xA2` | `0x27`, `0x28` |
| `0xA6`, `0xA7` | `0x29`, `0x2A` |
| `0xAB`, `0xAC` | `0x2B`, `0x2C` |
| `0xA9` | the stolen-goods lines (`0x0046A870`) |
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
3. For a row with bit 0 of byte `+4`, it drops it when one of the ten 0x20-byte ring entries at
   `0x02EBB560` (event `u16` at `+0`, tick at `+4`, stats at `+8`) holds the same event and stats and
   its tick plus `450 * [0x01DFE0B4]` is still ahead of `0x0032A150()` (`0x0046ABB3`-`0x0046ABF5`).
4. It records `{event, tick, stats}` in the ring entry `[0x02EBB54C]`, advances that index modulo 10,
   and calls `0x005369C0(stats, event, context)` (`0x0046AC00`-`0x0046AC66`).

The area initialisation `0x002342F0` empties the ring through `0x0033A380` (`0x00234463`), which calls
`0x004696A0` (`0x0033A3B0`): every entry's event becomes `0xFFFF`, its tick, stats and word `+0x18` 0,
and the index `0x02EBB54C` 0 (`0x004696A0`-`0x004697BB`).

### The visibility filter

`0x00469570(event, source, target)` returns 1 at once when byte `+3` of the event's row has bit 7
(`0x004695F9`). Otherwise it returns `0x002FA3B0` for the source's actor, or for the target's when the
source has no unit, and 1 when neither has one. `0x002FA3B0(actor)` is true when the actor is less than
24.0 (`0x008F3128`) units from the party leader, measured with height zeroed (`0x003A1920`); with no leader
it uses the leader position last stored at `0x01EEBB00` (`0x002FA3E2`-`0x002FA451`).

### Building the line

`0x005369C0(stats, event, context)` (1,000 bytes) fills four 16-byte argument slots from the row's
bytes `+0`, `+1`, `+2` and `+5` (`0x00536A51`-`0x00536BBC`):

| Slot kind | Argument |
|---:|---|
| 1, 2 | the source's or the target's name (`0x00536310`) and a byte from its actor (`0x00263A10`) |
| 3, 4, 5, 6, 7, 8, 9 | the context dword at `+0x10`, `+0x14`, `+0x18`, `+0x1C`, `+0x20`, `+0x28`, `+0x24` |

It passes bits 2-6 of row byte `+3` as a category (`0x00536C6F`), marks events `0x24` and `0x25`, and
hands the request to the formatter `0x00536410` and the poster `0x0035B990`. `0x00536410` turns kind 5
into a status name, kind 7 into an item name or a number (`0xE000` + n), and kind 8 into an action
name; kind 4 is formatted through a sub-template taken from the message table's text heap
(`0x002B4090`).

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

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | slot0 | argument kind of slot 0 (`0x005369C0`, `0x00536410`) |
| `+0x01` | `u8` | slot1 | argument kind of slot 1 |
| `+0x02` | `u8` | slot2 | argument kind of slot 2 |
| `+0x03` | `u8` | flags3 | bit 7: always shown (`0x00469570`); bits 2-6: category (`0x005369C0`); bits 0-1 dropped by `0x005369C0` |
| `+0x04` | `u8` | flags4 | bit 0: repeat-limited (`0x0046AB10`) |
| `+0x05` | `u8` | slot3 | argument kind of slot 3 |
| `+0x06` | `u16` | zero6 | 0 in every shipped row |

## Related

- [Battle message list](battle-message-list.md) - every row of the table with its text.
- [Action results](action-results.md) - the record the dispatcher reads.
- [Target selection](target-selection.md) - the same 24-unit distance used for targets.
