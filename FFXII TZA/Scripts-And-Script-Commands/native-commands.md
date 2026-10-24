---
title: "Native commands: the five command tables, the begin, poll and result callbacks, the phase byte, and how a durative verb waits"
kind: "system"
category: "Scripts and script commands"
addresses: "0x002621D0, 0x003DC2D0, 0x003DC270, 0x003DC240, 0x003DC2A0, 0x02B57EF0, 0x01EED700, 0x01F281B0, 0x01F29418, 0x01F29440, 0x01F26720, 0x0016D6A0, 0x005C5230, 0x0034CF90, 0x0034DCC0, 0x00265880, 0x0034C290, 0x0034C570, 0x00353E20, 0x00353A10, 0x0033F4C0, 0x00267310, 0x02099011, 0x0026A5B0, 0x00360710, 0x00360A50, 0x0034ECF0, 0x0026B4E0, 0x0026B4C0, 0x0050D660, 0x0025C0F0, 0x0025C130, 0x0026BE50, 0x0026BE90, 0x02099DE8, 0x0209A2A0, 0x0036E290, 0x002E7080, 0x0036DFC0, 0x0036E500, 0x022D94B0"
---

## What the player sees

Some verbs act at once: set a flag, give an item, move an actor to a point. Others take time:
`wait` counts frames, `move` walks a character to a spot, `camerasync` holds the script until the
camera finishes, `eventsync` until a scene ends. While a durative verb runs, the script that issued
it stands still and everything else in the zone keeps going. Skipping a cutscene ends those waits
early. This page is the machinery that gives every verb those two shapes.

## How it works

### The lifecycle

`0x002621D0(manager, actor, stack, id, waitSlot)` runs one verb call. It splits the id into family
and command, fetches the poll callback, and resolves the target: the issuer when the wait slot's
`+8` equals the issuer's own ordinal word, otherwise the actor `0x00358940` finds for that ordinal.
Then it reads the phase byte `+0x15`:

- phase 0: clear the result word `+0xC`, call `begin(issuer, target, scratch, stack, manager)` if
  the table has one, then fall through to the poll;
- phase 1: fall through to the poll;
- phase 2 or more: skip straight to the result stage.

The poll, when present, is called as `poll(issuer, target, scratch)`; when absent, a local zeroed
at entry stands in. An odd return sets the phase to 1 and returns 1: the verb is still running,
and the interpreter re-fetches the same call next frame. Otherwise the result stage runs
`result(issuer, target, scratch, stack)` when present, and pushes one value by the phase the
result wrote: 2 pushes the int at `+0xC`, 3 or more the float, 0 or 1 an int 0, and a null result
callback pushes an int 0 directly. The phase byte is reset to 0 and the call returns 0.

So the three callbacks are one fall-through, not three frames. A verb with only a result completes
on its first invocation; a verb with a poll completes on the first invocation whose poll returns
even. Phases 2 and 3 live only between the result callback's write and the push a few instructions
later; on entry the byte is only ever 0 or 1.

### The five tables

`0x003DC2D0` fills the sixteen family pointers at `0x02B57EF0` with the default table and then
installs four. Each table is a signed count, four zero bytes, and 32-byte records of begin, poll,
an unused null and result. Read from the shipping executable:

| Table | Commands | begin | poll | result | result only | begin without poll | poll without begin | all three | empty |
|---|---|---|---|---|---|---|---|---|---|
| family 0 `0x01EED700` | 1,496 | 277 | 230 | 1,234 | 1,189 | 74 | 27 | 43 | 3 |
| family 3 `0x01F281B0` | 147 | 6 | 4 | 143 | 141 | 2 | 0 | 2 | 0 |
| family 5 `0x01F29418` | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| family 7 `0x01F29440` | 104 | 27 | 30 | 74 | 74 | 0 | 3 | 0 | 0 |
| default `0x01F26720` | 212 | 25 | 25 | 200 | 185 | 1 | 1 | 14 | 1 |
| all | 1,960 | 336 | 290 | 1,651 | 1,589 | 77 | 31 | 59 | 4 |

The counts include the `ret` stub `0x0016D6A0`, which fills 9 begin slots (`0x0206`, `0x0209`,
`0x0372` to `0x0374`, `0x04AE`, `0x3020` and `0x20D3`, each paired with the poll `0x005C5230` that
returns 0, and `0x03BD` `moveblurfadesync`, whose poll `0x00345100` is live and waits on
`0x003DE150`) and 25 result slots (`0x0056`, `0x00A3`, `0x00C0`, `0x02BF`, `0x03BD`,
`0x04AC`, `0x05C7`, `0x3001`, `0x3003`, `0x3025`, `0x3037`, `0x3054` to `0x305A`, and seven
debug verbs).

The four empty records are `setnorecovertelepostatus` (`0x0330`),
`battlemembersync` (`0x0356`), `restartbattle` (`0x03B0`) and `debug_meswin_3e` (`0x203E`): they
complete at once and push 0.

The default table is family 2's: `0x2000` to `0x20D3` are the debug verbs, with real bodies
(`0x2000`'s begin `0x0050D660` pops a value and binds a model), and the other eleven families alias
it. Family 5's one command `0x5000` has a begin and a poll and no result.

### Instantaneous and durative

A verb is instantaneous when its record has no begin and no poll: 1,589 of the 1,960, and every
one of them completes inside the call that issued it. A verb with a begin or a poll is durative in
shape, but 77 of them have a begin and no poll, so they also finish on the first call: the begin
does the work and the absent poll reads as finished. Only the 290 with a poll can hold a script,
and only while that poll returns odd.

The scratch block `+0x18` of the wait slot is what carries a durative verb across frames: the
begin writes it, the poll reads it.

`wait` (`0x0000`) is the plainest case: its begin `0x0034CF90`
pops the frame count and stores it in the first scratch dword, scaled by `0x00265880` (× the frame
multiplier `0x01DFE0B4`, 1 in this build, unless `0x001EDDA0` is set; counts below 2 pass unscaled
while `0x001EDC80` is 0). The raw count is stored instead under any of four gates: `0x022C7F84` set,
`0x001EC5E0` for manager 3, `0x001ED130` with `0x001EC5C0` clear for managers 1 and 2, or the three
field ids `0x001ED180` names. Its poll `0x0034DCC0` decrements the word and finishes when it goes
below zero.

`0x001ED180` holds while the loaded map `0x00314910()` is `0x2F4`, `0x2E9` or `0x27B` and `0x001EC560`,
`0x00265760` and `0x002E0540` all answer 0 ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

### The sync verbs

`camerasync` (`0x0079`), `effectsync` (`0x00DE`) and `effectreadsync` (`0x00DC`) share the begin
`0x0034C290`, which pushes a literal 0, pops it back and stores it in the scratch word: the verbs
take no argument because the handler supplies one. `fadesync` (`0x00B9`, `0x0033F4C0`) is the same
three lines plus a call to `0x00183070`.

`eventsync` (`0x00ED`) and `eventreadsync` (`0x00E9`) share
`0x00353E20`, the zero-operand twin of `0x00353A10` (the begin of `eventreadsync_ea` `0x00EA` and
`eventsync_ee` `0x00EE`): both add 1 to the popped value and clamp to 1 to 3, so the argument-less
forms always store 1.

The poll then uses the word as a selector. `camerasync`'s poll `0x0034C570` asks `0x003DA1A0(index,
word)` whether that camera channel is still busy, with the index of the current manager (the slot
`0x02099D70` points at, `+0x28`), and, if so, stays running unless the skip mask of the issuer's
manager (its `+0x15`) says otherwise.

### Signal waits

`effecttotalsignalsync(n)` (`0x029F`) and `motiontotalsignalsync(n)` (`0x02B7`) wait for a
numbered signal. Both use the begin `0x003567F0`, which pops `n` into the scratch word. The poll
`0x0034AA70` tests bit `n` of the eight bytes at `0x02099DE8` through `0x0025C0F0`, and `0x0034B310` tests
bit `n` of `0x0209A2A0` through `0x0025C130`. While the bit is clear the poll returns 1 and the script
waits; once it is set the poll clears it (`0x0026BE50` or `0x0026BE90` with 0) and the verb finishes,
so one signal releases one waiter. Neither poll reads the skip mask.

`0x0036E290(handle, &n)`, which `0x0036E310` installs as entry 0 of the effect callback table
`0x02091140` (`0x0024F780` stores it), raises the effect signals: it sets bit `n` of `0x02099DE8` with
`0x0026BE50(n, 1)` and, when the handle is a script effect handle, the same bit in that effect slot's
own signal bytes. The motion signals have one writer, `0x002E7080`, which `0x002EA320` (run by the boot `0x00266D10`) and `0x002EA5F0` (run by `0x002368D0`)
install as entry `0x26` of the motion callback table `0x02CA4410` (`0x0041D6C0` stores it): it calls
`0x0026BE90(0, 1)`, so a motion only ever raises bit `0x1`.

`effectsignalsync(slot, n)` (`0x026A`) waits on one effect slot's bytes instead. Its begin
`0x00354CB0` pops `n` and the slot and stores the slot's handle, the first dword of record `0x022D94B0
+ slot × 0x18` read by `0x0036E500` (slot clamped to 31, a negative slot reading slot 0), with `n`.
The poll `0x00355160` finishes at once on a zero handle and otherwise keeps the script waiting while
`0x0036DFC0(handle, n)` returns 0 and the issuer's manager has a clear skip mask.

`0x0036DFC0` decodes the slot with `0x003B24A0`, which accepts only a handle whose top nibble is 7 and
takes the slot from bits `0xFC0` (any other handle returns 1 at once). It then tests bit `n` of
the bytes at `+0x10` of that slot's record, and returns 1 and clears the bit only when it is set.

### The skip mask

`0x00267310(manager)` reads byte `0x02099011 + manager × 0x288`, the manager slot's `+0x201`, and
72 sites call it. `0x0026A5B0(manager, set, bit)` sets or clears one bit of it: the verb `skipexec`
(`0x0539`, `0x0034ECF0`) pops a bit index and calls `0x00360710`, which sets the bit at the end of its
skip bookkeeping (after `0x003601B0(0xF)` and the rest, among them `0x002DEDD0`, which stores the current track's
point, [music](../Sound-And-Music/music.md)), and `0x00360A50` clears it when the skip
ends.

A poll that tests the mask ends its wait when the
byte is non-zero: `wait` forces its countdown to 0, `camerasync` reports finished, `effectsync`
cancels its effect first. Polls that do not test it keep waiting through a skip.

### Shared handlers

Callbacks are shared freely: the 336 begin slots are served by 236 distinct functions (the stub
aside), the 290 poll slots by 159, and the 1,651 result slots by 1,491. `move` (`0x005D`) and
`movesync` (`0x003D`) share the poll `0x00356A90`; `move` adds the begin `0x003488B0` that reads the
destination. Editing one shared body edits every verb that points at it.

## Layouts

The callbacks are called as `begin(issuer, target, scratch, stack, manager)`, `poll(issuer, target,
scratch)`, where an odd return means still running, and `result(issuer, target, scratch, stack)`.

Globals:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2B57EF0` | `CommandTable*[16]` | families | `0x003DC2D0` writes `0x01F26720` to all, then `0x01EED700`, `0x01F281B0`, `0x01F29418` and `0x01F29440` to families 0, 3, 5 and 7: `0x02B57EF0`, `0x02B57F08`, `0x02B57F18` and `0x02B57F28` (`0x003DC2F7`, `0x003DC305`, `0x003DC313`, `0x003DC321`) |
| `+0x2099011` | `u8` | skipMask | manager slot `+0x201`, at `+ manager × 0x288`; one bit per skip index |
| `+0x2099DE8` | `u8[8]` | effectSignals | effect total signals, one bit per signal number |
| `+0x209A2A0` | `u8[8]` | motionSignals | motion total signals |
| `+0x22D94B0` | `EffectSlot[32]` | effectSlots | script effect slots, stride `0x18` |

CommandTable:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | count | number of command records |
| `+0x04` | `u32` | zero | always 0 |
| `+0x08` | `Command` | first | record N at `08 + 0x20 × N` |

Command (32 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | begin | begin callback or null |
| `+0x08` | `void*` | poll | poll callback or null |
| `+0x10` | `void*` | unused | always null |
| `+0x18` | `void*` | result | result callback or null |

Wait slot fields used here:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u32` | result | the int, or the float for phase 3, that the call pushes |
| `+0x15` | `u8` | phase | 0 idle, 1 running, 2 int, 3 float |
| `+0x18` | `u8[16]` | scratch | written by the begin, read by the poll |

EffectSlot (`0x18` bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle | the script effect handle |
| `+0x10` | `u8[8]` | signals | per-slot signal bits |

## Shipped data

| Fact | Value |
|---|---|
| commands | 1,960 in five tables |
| instantaneous (no begin, no poll) | 1,589 |
| can hold a script (has a poll) | 290; 59 have all three callbacks |
| begin without poll | 77, finishing on the first call |
| distinct callbacks | begin 236, poll 159, result 1,491; 1,885 functions in all |
| frame multiplier `0x01DFE0B4` | 1 |
| skip-mask readers | 72 call sites of `0x00267310` |

## Operations

Per verb call per frame: one lifecycle pass, at most one begin, one poll and one result. A verb
whose poll returns odd costs one poll per frame until it finishes.

## State

The wait slot's phase byte, result word and scratch block, the family array, the per-manager
skip mask byte, and the two signal bit arrays with the effect slots' signal bytes.

## Modding notes

- To make a verb wait, give it a poll that returns odd while busy; a begin alone finishes at once.
- `wait N` stores N in the scratch word and counts it down once per poll.
- The sync verbs' channel or slot is a constant in a shared begin: changing `0x0034C290` changes
  `camerasync`, `effectsync` and `effectreadsync` together.
- A verb whose poll ignores the skip mask will not end when the player skips a scene.
- An empty record or the stub `0x0016D6A0` is safe to call: the verb completes and pushes 0, except
  `moveblurfadesync`, whose poll is live.

## Related

- [Verb dispatch](verb-dispatch.md): the call opcodes, the accessors and the value stack.
- [Script interpreter](script-interpreter.md): the wait slot and the rewind on a busy call.
- [Script verb table](verb-table.md): every id with its callbacks.
