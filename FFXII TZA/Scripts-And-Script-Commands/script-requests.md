---
title: "Script requests: how a script function is filed on an actor's channels, selected, started, waited on and retired"
kind: "system"
category: "Scripts and script commands"
addresses: "0x00268850, 0x003DBB60, 0x003DBBF0, 0x003DBAE0, 0x003DB790, 0x003DBCF0, 0x003DB7A0, 0x003DB6E0, 0x003DBDC0, 0x003DB2A0, 0x003DB420, 0x003DC050, 0x003DBF60, 0x003DC0D0, 0x003DC1B0, 0x003DB580, 0x003587C0, 0x00358A00, 0x002652D0, 0x00266BD0, 0x0026B4A0, 0x0025D5E0, 0x0025C230, 0x0025C830, 0x0025BAD0, 0x00268D10, 0x0025B600, 0x0025B2E0, 0x00269640, 0x00269860, 0x00268EA0, 0x00266C50, 0x00268B10, 0x00269BA0, 0x00266530, 0x0025DF00, 0x00263230, 0x00263050, 0x0025B500, 0x01E0C328, 0x00314020, 0x003DB1F0, 0x00267310"
---

## What the player sees

A door that opens on approach, a townsperson who answers the talk button, a monster that wakes when
the party crosses a line, a cutscene that one director script starts on another: every scripted
action is a request. Something, a script or the engine, asks an actor to run one of its functions.
The actor keeps a short list of such requests, ranks them by channel, runs the most urgent, and
tells the requester when it has started or finished. When two things happen at once, the channel
numbers below decide which the player sees first.

## How it works

### The entry pool

Every script-bearing actor record carries a small pool of request entries, built by `0x003DB580` when
the record is initialised (`0x00266530`). The pool size depends on the actor's sequence type through
byte `0x01E0C329 + type × 4`: types 2, 4 and 7 get six channels and eight entries, types 0, 1, 3, 5
and 6 get eight channels and ten entries. The counts sit at `+0x88` (channels) and `+0x89`
(entries).

An entry is `0x14` bytes in the array at `[actor + 0xA0]`: `+0` next, `+1` previous, `+2` channel,
`+3` the requester's wait slot, `+4` function id, `+6` requester ordinal (`0x8000` for an engine
filing), `+8` requester manager, `+0xC` the requester's return offset, `+0x10` mode, `+0x11` run
state, `+0x12` flags.

The initialiser links all entries into a free list headed at `+0x60`, sets
the detached-list head `+0x61` to `0xFF`, every channel head (`+0x94`) and tail (`+0x8C`) to
`0xFF`, and clears the busy mask `+6`. Each channel also has a `0x28`-byte wait slot at
`[actor + 0xA8] + channel × 0x28`, which holds the program counter and the wait state of whatever
runs on that channel.

### Filing from a script

Nine opcodes file a request: `REQ`, `FREQ`, `TREQ` and their `SW` and `EW` forms (`0x21` to
`0x29`). All reach `0x00268850` through one of two submit tails (`0x0025F7D0`, `0x002602E1`) with two
immediates: the kind (`R` 0, `F` 2, `T` 4) and the mode (plain 1, `SW` 2, `EW` 3). The handler pops
the function id, then the target actor, then the channel; a float is truncated, an empty stack
yields 0. Bit 15 set in the function id or the target refuses with 0 before anything is written.

The target word is either `(manager << 16) | ordinal` when bit 14 is set, or an ordinal in the
requester's own manager (`[slot + 0x28]`); `0x003587C0` resolves it against the manager's pool
(null pool, negative ordinal or ordinal at or above the count give null).

The handler then
advances the requester's program counter past the instruction and stores it back into the wait
slot, builds the descriptor (kind, mode, channel low byte, the requester's own wait slot, the
function id's low word, its own ordinal and manager, and its return offset relative to its bytecode
base), and submits. A null target returns 3, but only after reading the byte at address `0x10`
through the null pointer and decrementing it when it is non-zero, as the shipped code is written.

Two insert paths exist. When the requester's `+2` is 1 (an actor past the image's type-0 count,
so not a director) and it has no outstanding requests (`+0x10` = 0), `0x003DB790` files the entry in
run state 1; otherwise `0x003DBAE0` files it in state 2 and, when the target is a different actor,
promotes every state-1 entry of the target to 2, re-runs the target's selection and sets its flag
byte `+0x63 >>= 1` (`0x003DBB4A`).

A result of 1 sets bit *channel* of the target's `+0x26` word and calls `0x0025B580`, which calls
the exit-trap stub `0x008620C0` when the highest bit of `+0x26` lies above the highest bit of a
non-zero `+0x24` and otherwise does nothing. Any other result decrements the target's `+0x10`.
`SW` and `EW` then park the requester as wait kind 4.

`PREQ`, `PREQSW` and `PREQEW` (`0x2A` to `0x2C`) share one handler that pops three values and
files nothing.

### Filing from the engine

The engine files requests by **entry slot**, not by function id. Slot *n* of an actor names a
function through the cache word `actor + 0xC8 + 2n`, or, when that word is `0xFFFF`, through the
image's special-function footer at `table + 2 + 2n` (`0x002652D0`; slots above 17 give none, and
slot 14 reads slot 7 when the image's version word is below 6). The shipped scripts declare the
slots as 1 `main`, 2 `talk`, 3 `touch`, 4 `touchon`, 5 `touchoff`, 6 `across`, 7 `spawn`,
8 `fieldsign1`, 9 `initevent`, 11 `parameter`, 12 `mapjump`, 13 `fieldsign2`, 14 `respawn`,
16 `talkhold`, 17 `talkterm`.

Whether a slot may be filed is bit *n* of the actor's arming mask `+0x1C`. `0x00266BD0` seeds it by
sequence type: 0 none; 1 and 2 `0x38` (touch, touchon, touchoff); 3 and 4 `0x40` (across); 5 and
6 `0x30004` (talk, talkhold, talkterm); 7 `0x34C85` (slots 0, 2, 7, 10, 11, 14, 16 and 17). The verbs `reqenable` (`0x0026B4A0`) and `reqdisable` (`0x0025D5E0`) set
and clear one bit; `reqdisable` refuses slots 4 and 5 while `+0x0C` bit 5 marks a stop zone, and
for slot 16 clears `+0x0B` bit 2 and runs `0x00262740`, for 17 runs `0x002626C0`.

Every engine filing goes through `0x003DBB60(actor, channel, function, mode, flag)` or its
two-actor twin `0x003DBBF0(actor, requester, …)`. Both build the descriptor with requester ordinal
`0x8000`, map mode 1 to kind 0, mode 3 to kind 2 and any other mode to itself with flag bit 0 set,
and store `flag << 1` in the flags byte. `0x003DBB60` files in state 1; `0x003DBBF0` files in state 2
and re-selects when the requester differs, exactly as the script path does.

| Filer | Slot, channel, mode | Fires when |
|---|---|---|
| `0x00266530` | slot 15, the actor's function 0 and 9 `initevent` on the top channel, then 1 `main` on channel 0, all mode 2 | the record is initialised; the first three raise `+0x10` by one each; slot 15 only for images with version word 10 or more |
| `0x0025C230` | 3 `touch` ch 3 / 8 `fieldsign1` ch 3 / 13 `fieldsign2` ch 6, mode 1; 4 `touchon` ch 4 and 5 `touchoff` ch 2, mode 0 | a class-3 actor whose record box contains a party actor (`0x003DA5A0`); the on and off edges of the contact mask at record `+0x100` |
| `0x0025C830` | the same slots at the same channels | a class-1 trigger record with `+0x5D` bit 0 placed and bit 1 (outer box) or bit 2 (inner box) set; `touchon` with flag 2 raises a stop zone |
| `0x0025BAD0` | 16 `talkhold` ch 6 (ch 4 for type 7), mode 1, flag 5 | the focus actor stands in the talk box of a talk-armed actor; the actor is also registered as the talk candidate at `0x0209A2B4` |
| `0x00268D10` | 2 `talk` or 10, ch 7, mode 0 | the talk button gate `0x0026DFB0` passes for the registered candidate; a filed slot 2 sets `+0x0B` bit 3, runs `0x00268EA0` and takes capability row 3 |
| `0x00268EA0` | 16 `talkhold` ch 6/4 mode 1 flag 5; 17 `talkterm` ch 5 (3 for type 7) mode 2 flag 4 | the talk countdown `+0x118` is re-armed |
| `0x0025B2E0` | 6 `across` ch 5, mode 0 | a party actor's last move crosses the type-2 line record (`0x003A17D0`) |
| `0x0025B600` | 12 `mapjump` ch 6, mode 0 | the focus actor's collision record names a map-exit owner in `0x0209A210` and `0x003B7730` allows it |
| `0x00269860` | 7 `spawn` (mode argument non-zero) or 14 `respawn` ch 2, mode 0, then `0x00269640` | the scripts-live byte `0x02099DE1` is set |
| `0x00269640` | slot 0 on channel 1, then 11 `parameter` on channel 0, mode 0 | bits 0 and 11 of the mask; no shipped script declares slot 0, so only `parameter` is filed |
| `0x00266C50` | every function of the image's `+0x58` list on the actor its `+0x50` word names, top channel, mode 2 | the manager's image is started |
| `0x00268B10` | each `(actor, function)` pair of a list in the image's `+0x30` table, mode 0 | a scripted group request; a flag marks `+0x24` bit *channel* and raises `+0x10` on the target |
| `0x00269BA0` | slot *n* on one actor, mode 0 | bit *n* or the force argument |

### Admission

`0x003DBCF0(actor, descriptor, state)` refuses with 3 when the function id is at or above the
actor's function count (`[[actor + 0x48]]`), with 2 when the free head `+0x60` is `0xFF`, and
otherwise unlinks the head entry and hands it to `0x003DB7A0`.
The insert clamps the descriptor's signed channel byte `+2` with `ch = (ch >= [+0x88]) ? [+0x88] − 1 : ch`
(`0x003DB7A7`-`0x003DB7C5`), then applies the kind: kind 0 files only when `(([+6] >> ch) & 1) == 0`
(`0x003DB888`-`0x003DB890`); kind 2 always; kind 4 only when no entry on that channel already carries the function
id.

A refused kind relinks the entry at the free head and returns 3; the bytecode address
`0x00263E40` computes on that path is discarded.

A filed entry is copied from the descriptor, appended at the channel's tail, becomes the head
when the channel was idle, sets the channel's busy bit and `+0x63` bit 1 (re-select). A descriptor
whose mode byte is 4 is instead pushed on the detached list at `+0x61` without touching the
channel state: that is how notifications travel.

### Selection and start

Engine filings enter in state 1 and wait for `0x003DB1F0`, which the script step `0x00314020` runs
for every manager after each drive pass: every state-1 entry of every actor becomes state 2, then
the selection runs and `+0x63 >>= 1` (`0x003DB25A`). The step repeats up to sixteen times a frame, later
rounds only for managers whose byte `0x02099011 + manager × 0x288` is set (`0x00267310`), so a request
a touch files runs within the frame. A script's request on another actor is promoted at once by
`0x003DBAE0`.

`0x003DB6E0` runs whenever `+0x63` is non-zero: it walks the channels from the highest down, and on
each follows the chain from the head, skipping entries in state 1. The first other entry wins:
its channel becomes the current wait slot `+0x11`, a state-2 entry is started through `0x003DBDC0`,
the index is stored at `+0x62` and `+0x14` bit 6 (idle) is cleared. Nothing runnable sets the idle
bit. So higher channels pre-empt lower ones, and within a channel requests run in filing order.

`0x003DBDC0` resets the wait slot (`0x0025D460` zeroes its first `0x17` bytes, the scratch beyond
survives), sets the program counter to `[actor + 0x58] + functionTable[id]` (`0x00358A00`, offset 0
when out of range), sets wait kind 1, marks the entry state 3, and when the flags byte `+0x12` is 2 or more calls
`0x00263230(actor, flags >> 1)`, which acts only on the value 1: the world-lock take, which also
raises the manager's lock counter at `+0x1E0` and recomputes `0x02099DB4`, the count the talk gate
`0x0026DFB0` tests.

The talk filer passes flag 1 for slot 2, so talking to an actor takes the lock
when its script starts and no second talk starts while it runs. When the entry's mode is 2 it posts
the start notification first, before the entry is marked started.

### Start-wait and end-wait

A notification is itself a request: a descriptor with kind 2, mode 4, the requester's channel,
function 0 and requester `0x8000`, filed on the **requester** through `0x003DBCF0` with the
requester's own return offset (the entry's `+0xC`) carried along. Mode 2 posts it from `0x003DBDC0` when the target entry starts,
before any target bytecode runs; mode 3 posts it from `0x003DC0D0` when the entry is removed. Both
ignore the result, so a requester with no free entry misses its notification.

The requester parked as wait kind 4 is resumed by the driver `0x0025DF00`: `0x003DC050` scans the
detached list for an entry whose channel equals the requester's current wait slot and whose
`+0xC` equals the requester's saved program counter minus its bytecode base; a match is removed
through `0x003DB2A0` and the wait kind returns to 1 in the same driver pass.

`REQWAIT` (`0x32`)
instead parks as kind 3 on a target entry, cleared when `0x003DBF60` no longer finds that function on
the target; the list waits of kinds 5 and 7 (`0x002674B0`, `0x00267420`) advance a cursor past
satisfied elements and stop at the first live one.

### Return and cancel

`RET` (`0x2D`) and `RETT` remove the running entry through `0x003DB2A0` and re-run the selection.
`REQCANCEL` pops a channel and recycles every channel above it through `0x003DB420` with mode 1,
which leaves a started entry alone; `RETN` and `RETTN` pop a channel and, when it lies below the
current one, recycle the channels above it with mode 0, whatever their state.

`freqcancel`
(verbs `0x4A7` and `0x574` through `0x00352980`; `0x4A8` and `0x575` through `0x00353660` for another
actor) passes mode 4, which also takes any state. The
recycler walks the channels from the top down to the bound and hands each busy channel's first
non-free entry to `0x003DB2A0`; mode 3 limits the walk to one channel.

`0x003DB2A0` removes an entry only when it is the channel head (the detached head for a mode-4
entry). On a mismatch its loop calls `0x003DB550(actor, index)` for the removed index itself and
reloads that entry's `next`, a value that never changes: a non-head entry that is the tail is left
in place (the call returns flags bit 0), and a non-head entry with a successor never leaves the
loop. Every shipped caller passes a head: the recycler hands over a channel's first non-free entry
and `RET` passes the selected index `+0x62`.

It unhooks the entry (`0x003DC1B0`, which clears the run state), posts the end
notification when the mode is 3 and the requester is not `0x8000`, calls `0x00263050(actor,
flags >> 1)` for a flags byte of 2 or more (1 releases the world lock, 3 releases a stop zone
through `0x0025B500`, 4 clears `+0x0B` bit 4 after `0x002EAAA0`).

It then advances the channel head, and when
the channel empties clears its bit in `+6`, `+0x24` and `+0x26`. The entry then goes back on the free
list and `+0x63` bit 1 asks for a re-selection. Its return value is bit 0 of the entry's flags, not
a delivery result.

`REQCHG` (`0x34`, `0x0025AF60`) writes a cache word: slot below 18, target by the same encoding as a
request, refused when bit 15 of the target or of the value is set, value stored at
`actor + 0xC8 + 2 × slot`, so a script can re-point an entry slot at another function.

## Layouts

```
actor record   +6 u16 busy channels, +0x10 u8 outstanding requests, +0x11 s8 current wait slot,
               +0x1C u32 arming mask (bit n = slot n), +0x24/+0x26 u16 channel marks,
               +0x60 u8 free head, +0x61 u8 detached head, +0x62 u8 selected entry, +0x63 u8 flags,
               +0x88 u8 channels, +0x89 u8 entries, +0x8C u8 tail[8], +0x94 u8 head[8],
               +0xA0 entry array, +0xA8 wait-slot array, +0xC8 u16 slot cache[18]
entry (0x14)   +0 next, +1 prev, +2 channel, +3 requester wait slot, +4 u16 function, +6 u16 requester ordinal,
               +8 u32 requester manager, +0xC u32 requester return offset, +0x10 mode, +0x11 state, +0x12 flags
descriptor     +0 kind, +1 mode, +2 channel, +3 wait slot, +4 u16 function, +6 u16 ordinal, +8 flags,
               +0xC u32 manager, +0x10 u32 return offset
wait slot      +0 pc, +8 X, +0xC Y, +0x14 kind, +0x15 phase, +0x16 serviced, +0x18.. wait operands
pool table     0x01E0C328: 8 rows of {u8 class, u8 small pool, u16}; small pool = 6 channels, 8 entries
```

## Shipped data

| Fact | Value |
|---|---|
| request opcodes | 9 filing, 3 inert (`PREQ…`), `REQWAIT`, `PREQWAIT`, `REQCHG`, `REQCANCEL` |
| engine filing sites | 24 calls of `0x003DBB60` across 13 functions |
| entry run states | 0 free, 1 filed and not selectable, 2 runnable, 3 started |
| admission results | 1 filed, 2 no free entry, 3 refused |
| wait kinds | 1 and 2 interpreter, 3 entry gone, 4 notification, 5 list of entries, 6 channel clear, 7 list of channels |

## Operations

Per frame, up to sixteen rounds of: the drive pass `0x0025D9E0` per manager (the driver `0x0025DF00`
per actor; the contact, line and talk evaluators only while the manager's state byte `0x02098E20`
has bit 7 clear), the talk filer `0x00268D10` in round 0, then `0x003DB1F0` per manager (promote,
select). The step's second mode (argument 1) runs one round over managers 3 and 4 only, drive
pass and promotion per manager, without the talk filer. Per filing: admission, insert, optional
immediate re-selection. Per `RET`: unhook, notify, free, re-select.

## State

The entry pool, channel heads and tails, the busy mask, the detached list, the wait slots and the
arming mask of every actor record, and the talk candidate at `0x0209A2B4` to `0x0209A2BC`.

## Modding notes

- A script's `REQ` channel is the only priority: a higher channel pre-empts a running lower one at
  the next selection. Channels at or above the actor's count collapse onto the top channel.
- `REQ` (kind 0) is dropped when the channel is busy; use `FREQ` to queue behind the running
  function, `TREQ` to file once.
- `REQEW` resumes when the target's entry is removed, which a cancel can do as well as `RET`.
- An actor with every entry in use silently drops both new requests and the notifications it is
  owed; the pool is eight or ten entries.
- `reqenable` and `reqdisable` gate the engine's own filings without touching the script.

## Related

- [Script interpreter](script-interpreter.md): the opcodes and the wait slot.
- [The world lock](cutscenes-and-the-world-lock.md): what the start flag takes.
- [Actor record](../Characters-And-Objects/actor-record.md): the fields around the pool.
- [Script name bindings](script-name-bindings.md): the special-function footer.
