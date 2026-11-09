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

The initialiser (`0x003DB580(actor, channels, entries)`) stores the two counts and links all entries into a free
list headed at `+0x60` (entry 0, `0x003DB62F`), giving every entry function word 0, requester ordinal `0x8000` and
mode and state 0 (`0x003DB5B3`, `0x003DB5C7`). It sets the detached-list head `+0x61` to `0xFF`, every channel head
(`+0x94`) and tail (`+0x8C`) to `0xFF`, and clears the busy mask `+6`, both channel marks `+0x24` and `+0x26` (one
dword store, `0x003DB59B`) and the flags byte `+0x63` (`0x003DB626`).

Each channel also has a `0x28`-byte wait slot at
`[actor + 0xA8] + channel × 0x28`, which holds the program counter and the wait state of whatever
runs on that channel.

### Filing from a script

Nine opcodes file a request: `REQ`, `FREQ`, `TREQ` and their `SW` and `EW` forms (`0x21` to
`0x29`). All reach `0x00268850` through one of two submit tails (`0x0025F7D0`, `0x002602E1`) with two
immediates: the kind (`R` 0, `F` 2, `T` 4) and the mode (plain 1, `SW` 2, `EW` 3).

The handler pops the function id, then the target actor, then the channel, each pop lowering the stack count; an
integer is taken as it is, a float `f` is truncated toward zero, `f < 0 ? ceil(f) : floor(f)` (`cvttss2si`
at `0x00268901`, `0x00268917`, `0x0026892B`), an empty stack yields 0, and a value with any other type tag yields 0 after
a call of `0x008620C0` (`0x002688A8`), which jumps to the bare `ret 0` stub `0x0016D6A0` and so does nothing. Bit
`0x8000` set in the function id or the target refuses with 0 (`0x00268944`) before the program counter or a
descriptor is written.

With bit `0x4000` set in the target word, its high half (arithmetic shift) names the manager and its whole low
word, bit `0x4000` included, is the index (`0x002689CB`-`0x002689D0`). With the bit clear the word is the index in the
requester's own manager (`[slot + 0x28]`). `0x003587C0` resolves the index against the manager's pool without
masking it (null pool, negative index or index at or above the count give null, `0x003587D2`-`0x003587DD`).

The handler then
advances the requester's program counter past the instruction and stores it back into the wait
slot, builds the descriptor (kind, mode, channel low byte, the requester's own wait slot, the
function id's low word, its own ordinal and manager, its return offset relative to its bytecode
base, and the flags byte 1, `0x002689C0`), and submits.

A null target sets the result 3 (`0x00268A3B`) and then reads the byte at address `0x10` through the null pointer
to decrement it when it is non-zero (`0x00268A40`), as the shipped code is written. That address lies in the first
64 KB of the process, which is never mapped, so the read faults and this path never returns 3.

Two insert paths exist. When the requester's `+2` is 1 (an actor past the image's type-0 count,
so not a director) and it has no outstanding requests (`+0x10` = 0), `0x003DB790` files the entry in
run state 1; otherwise `0x003DBAE0` files it in state 2.

When the filing returns 1 and the target is a different actor (`0x003DBB08`, `0x003DBB0D`), `0x003DBAE0` first tests
the target's `+0x63` once (`0x003DBB12`): when that byte is non-zero, every entry of the target in run state 1
becomes state 2 (all `+0x89` entries, `0x003DBB18`-`0x003DBB40`). Then, either way, it re-runs the target's selection
(`0x003DBB45`) and sets the flag byte `+0x63 >>= 1` (`0x003DBB4A`). `0x003DBAE0` returns the filing's result.

A result of 1 sets bit *channel* of the target's `+0x26` word and calls `0x0025B580`, which calls
the exit-trap stub `0x008620C0` when the highest bit of `+0x26` lies above the highest bit of a
non-zero `+0x24` (`0x0025B5E4`-`0x0025B5F2`) and otherwise does nothing. `0x008620C0` only jumps to the bare `ret 0`
stub `0x0016D6A0` (`0x008620C9`), so `0x0025B580` writes nothing on either path. Any other result decrements the
target's `+0x10` when it is non-zero (`0x00268A44`).

`SW` and `EW` then park the requester as wait kind 4 when the filing returns 1 (`0x002602E6`-`0x002602EE`); on any
other result the requester is not parked (`0x002602E8`).

`PREQ`, `PREQSW` and `PREQEW` (`0x2A` to `0x2C`) share one handler that pops three values and
files nothing.

### Filing from the engine

The engine files requests by **entry slot**, not by function id. Slot *n* of an actor names a
function through the cache word `actor + 0xC8 + 2n`, or, when that word is `0xFFFF`, through the
image's special-function footer at `table + 2 + 2n` (`0x002652D0`; slots above 17 give no function, and
slot 14 reads slot 7 when the image's version word is below 6).

The footer's `table` is the image plus the dword at `+0x18` of the actor's directory entry `[actor + 0x40]`
(`0x00265319`-`0x0026532F`), and a slot at or above its signed count word `table + 0` gives no function either
(`0x0026533A`); `0x002652D0` gives no function as the value -1 (`0x002652DD`, `0x0026534E`).

The shipped scripts declare the
slots as 1 `main`, 2 `talk`, 3 `touch`, 4 `touchon`, 5 `touchoff`, 6 `across`, 7 `spawn`,
8 `fieldsign1`, 9 `initevent`, 11 `parameter`, 12 `mapjump`, 13 `fieldsign2`, 14 `respawn`,
16 `talkhold`, 17 `talkterm`.

A filer that tests the actor's arming mask `+0x1C` files slot *n* only while its bit *n* is set;
`0x0025B600` files `mapjump` without testing it, and no sequence seeds bit `0x1000` (slot 12). `0x00266BD0` seeds it by
sequence type: 0 no slots; 1 and 2 `0x38` (touch, touchon, touchoff); 3 and 4 `0x40` (across); 5 and
6 `0x30004` (talk, talkhold, talkterm); 7 `0x34C85` (slots 0, 2, 7, 10, 11, 14, 16 and 17). A sequence above 7
(the low five bits of `+0x03`) leaves the mask unwritten (`0x00266BDE`).

The verbs `reqenable` (`0x0026B4A0`) and `reqdisable` (`0x0025D5E0`) set
and clear one bit; `reqdisable` refuses slots 4 and 5 while `+0x0C` bit `0x20` marks a stop zone, and
for slot 16 clears `+0x0B` bit `0x4` and runs `0x00262740`, for 17 runs `0x002626C0`.

Every engine filing goes through `0x003DBB60(actor, channel, function, mode, flag)` or its
two-actor twin `0x003DBBF0(actor, requester, …)`. Both build the descriptor with requester ordinal
`0x8000` and mode byte 1 (`0x003DBBC9`, `0x003DBC58`), so an engine filing never posts a start or end notification;
they map mode 1 to kind 0, mode 3 to kind 2 and any other mode to itself with flag bit `0x1` set,
and store `flag << 1` in the flags byte. The descriptor's wait slot, manager and return offset are left unwritten.

`0x003DBB60` files in state 1 and returns the admission result; `0x003DBBF0` files in state 2
and re-selects when the requester differs, exactly as the script path does: only after a result of 1, with the
promotion only while `+0x63` is non-zero (`0x003DBC7F`-`0x003DBCC1`). Given a null requester, `0x003DBBF0` files in
state 1 and does not re-select (`0x003DBC68`, `0x003DBCD6`).

| Filer | Slot, channel, mode | Fires when |
|---|---|---|
| `0x00266530` | slot 15, the actor's function 0 and 9 `initevent` on the top channel, then 1 `main` on channel 0, all mode 2 | the record is initialised; the first three raise `+0x10` by one each; slot 15 only for images with version word 10 or more |
| `0x0025C230` | 3 `touch` ch 3 / 8 `fieldsign1` ch 3 / 13 `fieldsign2` ch 6, mode 1; 4 `touchon` ch 4 and 5 `touchoff` ch 2, mode 0 | a class-3 actor whose record box contains a party actor (`0x003DA5A0`); the on and off edges of the contact mask at record `+0x100` |
| `0x0025C830` | the same slots at the same channels | a class-1 trigger record with `+0x5D` bit `0x1` placed and bit `0x2` (outer box) or bit `0x4` (inner box) set; `touchon` with flag 2 raises a stop zone |
| `0x0025BAD0` | 16 `talkhold` ch 6 (ch 4 for type 7), mode 1, flag 5 | the focus actor stands in the talk box of a talk-armed actor; the actor is also registered as the talk candidate at `0x0209A2B4` |
| `0x00268D10` | 2 `talk` or 10 (the slot at `0x0209A2BC`), ch 7, mode 0, flag 1 for slot 2 and 0 for any other, through `0x003DBBF0` with the record as its own requester (state 2, no re-selection) | the talk button gate `0x0026DFB0` passes for the registered candidate (`0x0026DFB0(1)`, `0x00268D24`), the candidate's manager slot `0x0209A2B4` is not negative and that manager is live (`+0x10` bit `0x1`, `0x00268D4F`), `+0x1C` bit `0x4` is set for slot 2 (`0x00268DA2`) or bit `0x400` for any other slot (`0x00268DAC`), and `+0x18` is not 1 (`0x00268DB7`); a filed slot 2 with the count `0x02099DB4` at 0 or below (`0x00268DDE`) sets `+0x0B` bit `0x8`, runs `0x00268EA0`, runs the selection `0x003DB6E0` at once (`0x00268DF9`) and takes action availability row 3 (`0x002E1CD0(0, 3)`), then sets `0x02099DE5` to 1, sets `0x02099DE7` to 1 when `0x00377700()` is 0 and to 0 otherwise, and runs `0x00263480(record, 2)` when `+0x0C` bit `0x80` is set, else `0x00263480(record, 1)` (`0x00268E30`); every resolved candidate then runs `0x00317E60` (`0x00268E35`), clears the talk request byte `0x0209A2C4` (`0x00268E41`) and, with `+0x1C` bit `0x2000` set and a name whose first byte is not 0 (`0x00263990`, `0x00268E58`), passes the name to `0x003DF760` (`0x00268E7F`); a candidate ordinal that resolves to no record makes the bit test at `0x00268E3A` read address `0x1C`, which faults |
| `0x00268EA0` | 16 `talkhold` ch 6/4 mode 1 flag 5; 17 `talkterm` ch 5 (3 for type 7) mode 2 flag 4; both through `0x003DBBF0` with the record as its own requester (state 2, no re-selection) | the talk countdown `+0x118` is re-armed: `talkhold` is filed when `+0x1C` bit `0x10000` is set and slot 16 names a function (`0x00268F2B`, `0x00268FB8`), `talkterm` when bit `0x20000` is set and slot 17 names one (`0x00268EDC`, `0x00268FF7`), neither while `+0x18` is 1 (`0x00268FD7`, `0x00269011`); with bit `0x10000` set and either a slot-16 function or `+0x18` at 1, `+0x0B` bit `0x4` is set and `+0x118` = the word `+0x11A` (`0x00268F7D`, `0x00268F81`), otherwise bit `0x4` is cleared and `+0x118` = 0 (`0x00268F8A`, `0x00268F8E`); a set `+0x0B` bit `0x8` clears `+0x0B` bit `0x10` (`0x00268F9E`), and `0x002626C0` and `0x00262740` run on every call before the filings (`0x00268FA6`, `0x00268FAE`) |
| `0x0025B2E0` | 6 `across` ch 5, mode 0 | a party actor's last move crosses the type-2 line record (`0x003A17D0`): for each of the four roster pointers `0x0209A1F0` to `0x0209A208` that is not null (`0x0025B323`), for which `0x002EA6A0` returns non-zero (`0x0025B334`), whose movement context `+0xB8` has a non-zero squared XZ distance between its positions `+0x00` and `+0x10` (`0x003A1960`, `0x0025B34F`) and for which `0x003A17D0` returns non-zero (`0x0025B36A`), the actor's slot 6 function (cache word `+0xD4`, else footer entry 6 when the footer's count is above 6, `0x0025B36C`-`0x0025B39A`) is filed when it is not negative and `+0x18` is not 1 (`0x0025B3A6`, `0x0025B3AB`), one filing per crossing member; its only caller `0x0025B250` runs it for each actor from `+0x1DC` to `+0x1DC + +0x1D4 - 1` of a live manager with `+0x14` bit `0x20`, `+0x08` bit `0x1` and `+0x1C` bit `0x40` set (`0x0025B26A`-`0x0025B2AA`) |
| `0x0025B600` | 12 `mapjump` ch 6, mode 0, without testing the arming mask | the focus actor's collision record names a map-exit owner in `0x0209A210` and `0x003B7730` allows it: the focus actor `0x003588B0(0x003590D0())` is not null (`0x0025B615`), `0x003B7730()` is non-zero (`0x0025B625`), its secondary context `+0xC0`, when present, has `+0x14F` bit `0x1` clear and a collision record `+0x138` (`0x0025B637`, `0x0025B644`), its `+0x09` bit `0x1` and `+0x08` bit `0x2` are set (`0x0025B652`, `0x0025B65C`), `0x00265680()` is non-zero (`0x0025B66B`), the secondary context and its collision record exist (`0x0025B67F`, `0x0025B68F`), the record's owner word `+0x88` is not 0 (`0x0025B6A0`) and the pointer `0x0209A210 + owner × 8` is not null (`0x0025B6B8`); a slot 12 function that is not negative (cache word `+0xE0`, else footer entry 12 when the count is above 12, `0x0025B6C7`-`0x0025B6F8`) is filed after `0x002678C0()` runs (`0x0025B70B`), and an owner whose `+0x18` is 1 runs `0x002678C0()` and files nothing (`0x0025B6C3`, `0x0025B714`); the drive pass `0x0025D9E0` calls it only when its slot index is 0 (`0x0025DECB`) |
| `0x00269860` | 7 `spawn` (mode argument non-zero) or 14 `respawn` ch 2, mode 0, then `0x00269640` | the scripts-live byte `0x02099DE1` is set (else it returns 0, `0x00269876`) and the record is not null (else it returns 0, `0x00269888`); `spawn` needs `+0x1C` bit `0x80` (`0x002698AC`) and reads cache word `+0xD6`, else footer entry 7; `respawn` needs bit `0x4000` (`0x00269910`) and reads slot 7 instead of 14 when the image's version word is below 6 (`0x0026994D`); a negative function or a record whose `+0x18` is 1 files nothing (`0x00269995`, `0x0026999B`); `0x00269640` runs whenever the byte is set and the record is not null, and its result is returned (`0x002699B3`) |
| `0x00269640` | slot 0 on channel 1, then 11 `parameter` on channel 0, mode 0 | the scripts-live byte `0x02099DE1` is set (else it returns 0, `0x00269650`), and bits `0x1` and `0x800` of the mask (`0x00269699`, `0x00269705`); each slot's function is the cache word (`+0xC8`, `+0xDE`), else the footer entry when the footer's count is above the slot (`0x002696D0`, `0x00269737`), a negative function files nothing, and a record whose `+0x18` is 1 files neither (`0x002696ED`, `0x00269750`); it returns 1 when bit `0x1` is set and 0 otherwise (`0x00269770`); no shipped script names a function for slot 0: its footer entry is -1 in all 237,662 actors of the 10,036 version-11 images, and the 16,956 `REQCHG` of the listings re-point slots 2 to 5, 16 and 17 only |
| `0x00266C50` | every function of the image's `+0x58` list on the actor its `+0x50` word names, top channel, mode 2 | the manager's image is started (`0x0026CEBC`, in `0x0026CE60`); a negative `+0x50` word or a zero `+0x58` offset files nothing (`0x00266C65`, `0x00266C92`) and each negative function of the list is skipped (`0x00266CB9`); when the `+0x50` word names no record (`0x00358940` gives null), the first function that is not negative makes it read the channel count at address `0x88` (`0x00266CBB`), which faults |
| `0x00268B10` | each `(actor, function)` pair of a list in the image's `+0x30` table, mode 0 | a scripted group request; a flag marks `+0x24` bit *channel* and raises `+0x10` on the target; a list index at or above the table's count files nothing (`0x00268B4B`); a requester whose `+2` is 1 with `+0x10` = 0 files through `0x003DBB60` (state 1), any other through `0x003DBBF0` (state 2, re-selecting a target that differs from it) (`0x00268B74`-`0x00268B86`); a pair whose actor's `+0x18` is 1 is skipped (`0x00268BBE`, `0x00268C60`); after a filing that returns 1, the flag marks only when the target's manager has `+0x10` at `0x80` or above or `+0x11` bit `0x2` set, and then also sets that bit (`0x00268BF8`-`0x00268C0B`), and a target whose `+0x10` is then non-zero gets `+0x26` bit *channel* and a call of `0x0025B580` (`0x00268C0F`-`0x00268C1C`); an ordinal that resolves to no record makes the test at `0x00268BBE` (or `0x00268C60`) read address `0x18`, which faults |
| `0x00269BA0` | slot *n* on one actor, mode 0 | bit *n* or the force argument; `0x00269BA0(slot, ordinal, channel, n, force)` is reached only by the tail jump at `0x00269ABD` in `0x00269A90`, which passes an `n` below 18 and an ordinal from 0 to below the live manager's record count `+0x20`; it returns 3 without filing when bit *n* of `+0x1C` is clear and the force argument is not 1 (`0x00269BCD`), when the record's `+0x18` is 1 (`0x00269BD4`, `0x00269BEF`) or when `0x002652D0` gives function 0 (`0x00269BED`); otherwise it files on the given channel with flag 1 for slot 2 and 0 for any other (`0x00269BFB`-`0x00269C0D`) and returns the admission result, so a slot that names no function (-1) reaches admission as function `0xFFFF`; a null record from `0x00358940` makes it read address `0x1C` (`0x00269BC5`), which faults |
| `0x00269AD0` | slot *n* on every record of one manager, on the given channel, mode 0, flag 1 for slot 2 and 0 for any other | an `n` below 18 (`0x00269AD0`) and a live manager (`+0x10` bit `0x1`, `0x00269B0A`): each record 0 to `+0x20` - 1 is filed when bit *n* of its `+0x1C` is set (`0x00269B34`), its `+0x18` is not 1 (`0x00269B39`, `0x00269B52`) and `0x002652D0` gives a function other than 0 (`0x00269B4D`); a null record from `0x00358940` makes it read address `0x1C` (`0x00269B31`), which faults |

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
when the channel was idle, sets the channel's busy bit and `+0x63` bit `0x2` (re-select). A descriptor
whose mode byte is 4 is instead pushed on the detached list at `+0x61` without touching the
channel state: that is how notifications travel.

### Selection and start

Requests filed in state 1 (every `0x003DBB60` filing, and a `0x003DBBF0` filing with a null requester) wait for
`0x003DB1F0`, which the script step `0x00314020` runs for every manager after each drive pass (the manager initialisation `0x0026CE60` also runs it once, `0x0026D365`). It works only on a live manager
(`+0x10` bit `0x1`, `0x003DB1FE`): for every actor whose `+0x63` is non-zero every state-1 entry becomes state 2
(`0x003DB222`-`0x003DB250`), then for every actor the selection runs and `+0x63 >>= 1` (`0x003DB25A`).

The step repeats up to sixteen times a frame, later rounds only for managers whose byte `0x02099011 + manager × 0x288`
is set (`0x00267310`), so a request a touch files runs within the frame. A script's request on another actor is promoted
at once by `0x003DBAE0`.

`0x003DB6E0` runs whenever `+0x63` is non-zero: it walks the channels from the highest down, and on
each follows the chain from the head, skipping entries in state 1. The first other entry wins:
its channel becomes the current wait slot `+0x11`, a state-2 entry is started through `0x003DBDC0`,
the index is stored at `+0x62` and `+0x14` bit `0x40` (idle) is cleared. Nothing runnable sets the idle
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
function 0, requester `0x8000` and flags byte 1, filed in state 1 on the **requester** through `0x003DBCF0` with the
requester's own return offset (the entry's `+0xC`) carried along (`0x003DBE27`-`0x003DBE5F`, `0x003DC0EA`-`0x003DC122`).
Mode 2 posts it from `0x003DBDC0` when the target entry starts,
before any target bytecode runs; mode 3 posts it from `0x003DC0D0` when the entry is removed.

Both find the requester with `0x003587C0` from the entry's manager `+8` and ordinal `+6` and post nothing when it
gives null (`0x003DBE25`, `0x003DC0E8`). Both
ignore the result, so a requester with no free entry misses its notification.

`0x003DC0D0(actor, entry)` ignores the actor. It resolves the requester from the entry's manager `+8` and ordinal
`+6` through `0x003587C0` and posts nothing when that gives null (`0x003DC0E0`-`0x003DC0E8`). Its descriptor takes the
channel from the entry's `+3`, the manager from `+8` and the return offset from `+0xC`, and carries flags 1
(`0x003DC0EA`-`0x003DC11D`), below the 2 that makes `0x003DB2A0` call `0x00263050` on removal. It leaves the
descriptor's wait-slot byte `+3` unwritten, so the filed entry copies whatever the stack held there, and files
in run state 1 (`0x003DC0F7`, `0x003DC122`).

The requester parked as wait kind 4 is resumed by the driver `0x0025DF00`: `0x003DC050` scans the
detached list for an entry whose channel equals the requester's current wait slot and whose
`+0xC` equals the requester's saved program counter minus its bytecode base; a match is removed
through `0x003DB2A0` and the wait kind returns to 1 in the same driver pass.

`0x003DC050(actor, channel, offset)` starts at the detached head `+0x61` and follows each entry's `+0`
(`0x003DC09B`), testing `+0xC` against the offset and then the signed channel byte `+2` (`0x003DC083`-`0x003DC094`).
It returns the first match's index, or `0xFF` at the end of the list or once it has tested `[+0x89] + 2`
entries, more than the pool holds (`0x003DC096`-`0x003DC0AB`); on `0xFF` the requester stays parked.

The return opcodes' check `0x0025B400` runs the same scan when the current wait slot is in kind 4 (`0x0025B41D`,
`0x0025B435`): a match is removed, the kind set to 1 and 0 returned; no match returns 1, and a slot in another
kind returns 0 without the scan.

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
actor) passes mode 4, which also takes any state; `0x00352980` gives the popped channel itself as the bound
(`0x00352997`), so it also clears that channel, and `0x00353660` the channel plus 1 (`0x0035368C`).

The recycler walks the channels from the top down to the bound and hands each busy channel's first non-free
entry to `0x003DB2A0`; mode 3 limits the walk to one channel.

`0x003DB420(actor, bound, mode)` returns 1 on every path, at once for a null actor (`0x003DB42C`). The bound itself is
walked, a negative bound counts as 0, `bound < 0 ? 0 : bound` (`0x003DB43A`-`0x003DB44F`), the busy test reads the mask
`+6` as it stood on entry (`0x003DB457`, `0x003DB4A9`), and on a channel the free entries are stepped past while the
step `k`, counted from 0, is at most the entry count, `k <= [actor + 0x89]`, so at most the entry count plus one,
`[actor + 0x89] + 1` (`0x003DB4AE`, `0x003DB4CF`, `0x003DB4D8`).

Mode 3 walks only the bound's channel and then acts as mode 0 (`0x003DB466`-`0x003DB470`), and so does mode 4
(`0x003DB484`). Mode 2 hands over an entry unless it is in state 1 (`0x003DB4EE`), and any mode other than 0 to 4
hands over nothing (`0x003DB4EC`).

`0x003DB2A0` removes an entry only when it is the channel head (the detached head for a mode-4
entry or one whose channel byte is negative, `0x003DB2F8`-`0x003DB314`). On a mismatch its loop calls
`0x003DB550(actor, index)` for the removed index itself and
reloads that entry's `next`, a value that never changes: a non-head entry that is the tail is left
in place (the call returns flags bit `0x1`), and a non-head entry with a successor never leaves the
loop.

The recycler hands over a channel's first non-free entry, and `RET` and `RETT` pass the selected index `+0x62`
(`0x00261239`, `0x002613DD`). Four callers pass the first entry a search matched, which is the head only when no
entry precedes it on its list: `0x0025B400` (`0x0025B456`) and the driver `0x0025DF00` (`0x0025E0B0`) the detached entry
`0x003DC050` matched, and `0x002626C0` (`0x00262708`) and `0x00262740` (`0x00262788`) the entry with flags `>> 1` of 4 or 5
that `0x003DBEA0` finds on the `talkterm` or `talkhold` channel.

`0x003DB2A0` returns 1 at once for index `0xFF` (`0x003DB2B0`); a null actor makes it read the flags byte at address
`0x12` (`0x003DB2EA`), which faults. When the entry's list head is `0xFF` it removes nothing (`0x003DB320`).

It unhooks the entry (`0x003DC1B0`, which clears the run state). A detached entry then only moves `+0x61` to its
`next` (`0x003DB34F`-`0x003DB35E`) before going back on the free list. A channel entry posts the end
notification when the mode is 3 and the requester is not `0x8000`, calls `0x00263050(actor,
flags >> 1)` for a flags byte of 2 or more (1 releases the world lock once the summed count
`0x02099DB4` is 0 or below, 3 releases a stop zone through `0x0025B500`, 4 clears `+0x0B` bit `0x10`
after `0x002EAAA0` when that bit is set; 2 and every value above 4 return at once, `0x00263066`).

`0x003DC1B0(actor, index)` sets the previous entry's `next` to the entry's `next` (`0x003DC22C`-`0x003DC230`) and the
next entry's `prev` to the entry's `prev` (`0x003DC220`), each only when that link is not `0xFF`. The entry's own
`next` and `prev` stay as they were and the channel head and tail are left to `0x003DB2A0`; it zeroes the run
state `+0x11` (`0x003DC233`) and returns the entry's address.

An index of `0xFF` or a null actor gives `0x003DC1B0` a null entry (`0x003DC1D7`), and its read of byte `+1` there
(`0x003DC1DA`), address 1, faults. `0x003DB2A0` passes neither: it returns 1 for `0xFF` (`0x003DB2B0`-`0x003DB2B8`),
and with a null actor it faults on its own read of the entry's flags (`0x003DB2EA`) before its call (`0x003DB346`).

It then advances the channel head, and when
the channel empties clears its bit in `+6`, `+0x24` and `+0x26`; a channel tail that was the entry moves to the
entry's `prev` (`0x003DB3D1`-`0x003DB3E0`). The entry then goes back on the free
list and `+0x63` bit `0x2` asks for a re-selection. Its return value is bit `0x1` of the entry's flags, not
a delivery result.

`REQCHG` (`0x34`, `0x0025AF60`) writes a cache word: slot below 18, target by the same encoding as a
request, refused when bit `0x8000` of the target or of the value is set, value stored at
`actor + 0xC8 + 2 × slot`, so a script can re-point an entry slot at another function.

## Layouts

Actor record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x06` | `u16` |  | busy channels |
| `+0x10` | `u8` |  | outstanding requests |
| `+0x11` | `i8` |  | current wait slot |
| `+0x1C` | `u32` | arming mask | bit n = slot n |
| `+0x24` | `u16` | channel marks | one of the two channel marks |
| `+0x26` | `u16` | channel marks | one of the two channel marks |
| `+0x60` | `u8` |  | free head |
| `+0x61` | `u8` |  | detached head |
| `+0x62` | `u8` |  | selected entry |
| `+0x63` | `u8` | flags |  |
| `+0x88` | `u8` | channels |  |
| `+0x89` | `u8` | entries |  |
| `+0x8C` | `u8[8]` | tail |  |
| `+0x94` | `u8[8]` | head |  |
| `+0xA0` | `...` |  | entry array |
| `+0xA8` | `...` |  | wait-slot array |
| `+0xC8` | `u16[18]` |  | slot cache |

Entry (`0x14`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | next |  |
| `+0x01` | `...` | prev |  |
| `+0x02` | `...` | channel |  |
| `+0x03` | `...` |  | requester wait slot |
| `+0x04` | `u16` | function |  |
| `+0x06` | `u16` |  | requester ordinal |
| `+0x08` | `u32` |  | requester manager |
| `+0x0C` | `u32` |  | requester return offset |
| `+0x10` | `...` | mode |  |
| `+0x11` | `...` | state |  |
| `+0x12` | `...` | flags |  |

Descriptor:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | kind |  |
| `+0x01` | `...` | mode |  |
| `+0x02` | `...` | channel |  |
| `+0x03` | `...` |  | wait slot |
| `+0x04` | `u16` | function |  |
| `+0x06` | `u16` | ordinal |  |
| `+0x08` | `...` | flags |  |
| `+0x0C` | `u32` | manager |  |
| `+0x10` | `u32` |  | return offset |

Wait slot:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | pc |  |
| `+0x08` | `...` | X |  |
| `+0x0C` | `...` | Y |  |
| `+0x14` | `...` | kind |  |
| `+0x15` | `...` | phase |  |
| `+0x16` | `...` | serviced |  |
| `+0x18` | `...` | wait operands | from `+0x18` on |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01E0C328` | `...` | pool table | 8 rows of {u8 class, u8 small pool, u16}; small pool = 6 channels, 8 entries |

## Shipped data

| Fact | Value |
|---|---|
| request opcodes | 9 filing, 3 inert (`PREQ…`), `REQWAIT`, `PREQWAIT`, `REQCHG`, `REQCANCEL` |
| engine filing sites | 23 calls of `0x003DBB60` across 12 functions: `0x0025B2E0`, `0x0025B600`, `0x0025BAD0`, `0x0025C230` (4), `0x0025C830` (5), `0x00266530` (4), `0x00266C50`, `0x00268B10`, `0x00269640` (2), `0x00269860`, `0x00269AD0` and `0x00269BA0`; and 4 calls of `0x003DBBF0` through its thunk `0x003DBBE0`, in `0x00268B10`, `0x00268D10` and `0x00268EA0` (2) |
| entry run states | 0 free, 1 filed and not selectable, 2 runnable, 3 started |
| admission results | 1 filed, 2 no free entry, 3 refused |
| wait kinds | 1 and 2 interpreter, 3 entry gone, 4 notification, 5 list of entries, 6 channel clear, 7 list of channels |

## Operations

Per frame, up to sixteen rounds of: the drive pass `0x0025D9E0` per manager (the driver `0x0025DF00`
per actor; the contact, line and talk evaluators only while the manager's state byte `0x02098E20`
has bit `0x80` clear), the talk filer `0x00268D10` in round 0, then `0x003DB1F0` per manager (promote,
select). The step's second mode (argument 1) runs one round over managers 3 and 4 only, drive
pass and promotion per manager, without the talk filer. Per filing: admission, insert, optional
immediate re-selection. Per `RET`: unhook, notify, free, re-select.

## State

The entry pool, channel heads and tails, the busy mask, the detached list, the wait slots and the
arming mask of every actor record, and the talk candidate at `0x0209A2B4` to `0x0209A2BC`.

`0x0209A2B8` is the candidate's record index, the record's `u16` at `+0x000`, beside its manager slot `0x0209A2B4`. The talk
tests `0x0025BAD0` (`0x0025BDD1`) and `0x0025BE50` (`0x0025BF76`) set it, and so does `0x0025AAD0` (`0x0025AAF2`) when its first
argument is 0; `0x0025D650` (`0x0025D66A`) and the boot `0x00266D10` (`0x002670F8`) set it to -1. The talk filer `0x00268D10` passes it to `0x00358940` (`0x00268D58`), and
`0x00268650` passes it to `0x003587C0` (`0x00268668`).

The talk button gate `0x0026DFB0(1)`, which the talk filer runs first (`0x00268D1D`), passes only when the count
`0x02099DB4` is 0 and the four bytes at `0x0209A2C4` are all 1 (`0x0026E012`-`0x0026E044`). Byte 0 is the talk request:
`0x0026BC60(1)` sets it on the confirm press (`0x0025415A`, in `0x00253C70`) and for the developer verb `debug_talkrequire`
(`0x0050DF60`), and `0x0025AAD0` sets it with the candidate (`0x0025AB15`).

The filer clears it on every run in which the gate passes, the candidate's manager is live and its record
resolves, whether or not it files the talk (`0x00268E41`), as `0x0025D650` does (`0x0025D674`).

Byte 1 is the control lock's bit `0x2` inverted (`0x0026BD40`, [Party leader](../Party/party-leader.md)); byte 2 is 0
while the event lock stands (`0x00307140` through `0x0026BD20`, `0x003071F2`); byte 3 stays 1. The boot sets bytes 1-3 to 1
and byte 0 to 0 (`0x002670D7`, `0x002670DD`), and the manager unload `0x002628B0` sets bytes 1-3 to 1 again
(`0x00262C52`-`0x00262C70`), as the manager bind `0x0026C8C0` does (`0x0026CD80`-`0x0026CD94`).

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
- [World lock](world-lock.md): what the start flag takes.
- [Actor record](../Characters-And-Objects/actor-record.md): the fields around the pool.
- [Script name bindings](script-name-bindings.md): the special-function footer.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Rewards progression economy: `0x003A1960` is called by `0x00319850`; those functions are documented on
  [loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md).
- Spawn encounter lifecycle: `0x00307140` is called by `0x00306F00`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Status periodic terminal: `0x00265680` is called by `0x00310DB0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Story event quest hunt: `0x00253C70` calls `0x0032A8A0`; `0x00263990` calls `0x0032A930`; `0x0026C8C0` calls `0x00377440`; those
  functions are documented on [identifier spaces](../Engine-Core/identifier-spaces.md),
  [actor managers](../Characters-And-Objects/actor-managers.md).
- UI: `0x00253C70` calls `0x00254B50`, `0x0028F970`, `0x003669D0`, `0x003C87B0`, `0x003C8990`; `0x00263990` is called by `0x002AC5F0`;
  `0x00265680` is called by `0x00279E20`; `0x002678C0` calls `0x002509A0`; `0x0026CE60` calls `0x00253A30`; `0x003590D0` is called
  by `0x00299BD0`, `0x002C7660`.
- UI: those functions are documented on [identifier spaces](../Engine-Core/identifier-spaces.md),
  [game over](../World-Areas-And-Travel/game-over.md), [controls](../Controls-And-Input/controls.md),
  [augments](../Damage-And-Battle-Formulas/augments.md),
  [tutorial battle commands](../Battle-Actions/tutorial-battle-commands.md).
- UI: and on [frame update order](../Engine-Core/frame-update-order.md),
  [actor managers](../Characters-And-Objects/actor-managers.md), [party list](../Menus-And-HUD/party-list.md),
  [battle units](../Characters-And-Objects/battle-units.md).
