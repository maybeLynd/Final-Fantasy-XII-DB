---
title: "Presentation entries: the reference container, how an entry picks its track, the choice selectors and the per-entry update"
kind: "system"
category: "Graphics"
addresses: "0x004269A0, 0x0051F240, 0x0051F080, 0x0051F410, 0x0051F190, 0x0051BA40, 0x0051BA80, 0x0051B9F0, 0x0051B970, 0x0041CD30, 0x0041CFC0, 0x0041C9A0, 0x00417920, 0x00417110"
---

## What the player sees

A character's motion stream is played by its presentation entries: each picks the track to play, such as the
walking, running or stopping gait the locomotion selector chooses, or a track chosen by which way the character
faces, and advances it every frame.

## How it works

### The presentation-entry reference container

The container at root `+0x160` maps an entry id to a `0x3A0`-byte presentation entry. A node is `0x30`
bytes: `+0x00` state (bit `0x1` used, bit `0x2` refresh on lookup), `+0x04` id, `+0x08` / `+0x0C` previous and
next id, `+0x10` source, `+0x18` cached pointer, `+0x20` 32-bit offset.

- `0x0051F240(container, id)` takes the table by the container's mode (`+0x04` low two bits: 1 direct,
  0 through `0x003AB7F0`, anything else returns 0), indexes it by `id & 0xFFFF`, and when node bit `0x2` is
  set rebuilds `+0x18` as `(i64)(i32)(0x003AB7F0(source) + offset)`, the sign-extended 32-bit sum of the resolved
  source and the offset (`0x0051F2A3`-`0x0051F2B7`).
- `0x0051F240` returns the node's `+0x18` (`0x0051F2BB`) without testing the used bit or the id's high half, and
  0 when the node address is 0 (`0x0051F291`).
- `0x0051F080` admits: `0x0051F410` takes the cursor slot, the id is `slot | 0x10000`, and the node joins
  the active list. The high half never changes, so a reused slot gets the same id.
- `0x0051F080(container, source, offset, flags)` returns a negative result of `0x0051F410` as it is
  (`0x0051F0A8`). Otherwise it sets node bit `0x1`, and bit `0x2` when `flags` has bit `0x2`
  (`0x0051F0F3`-`0x0051F0FC`), stores the id at `+0x04`, `source` at `+0x10`, `offset` at `+0x20` and the
  pointer `(i64)(i32)(0x003AB7F0(source) + offset)` at `+0x18` (`0x0051F0FF`-`0x0051F121`), appends the id
  (`0x0051F380`) and returns it (`0x0051F12A`).
- `0x0051F410(container)` returns −10 when the used count `+0x14` has reached the capacity `+0x10`
  (`0x0051F423`). Otherwise it counts the node in (`0x0051F438`) and returns the cursor `+0x18`, after moving the
  cursor on to the next node whose state dword is 0, wrapping at the capacity (`0x0051F490`-`0x0051F4B1`), or to
  0 when the container is now full (`0x0051F441`).

- The container's own list helpers: `0x0051F2F0`, run by the initialiser `0x0051F170`, clears every node
  (state 0, id and links −1, source, pointer and offset 0); `0x0051F380`, run by `0x0051F080`, appends
  an id at the tail (head `+0x1C`, tail `+0x20`); `0x0051F4C0`, run by `0x0051F190`, unlinks one; and
  `0x0051F150`, used by `0x0051BA80`, returns the cursor `+0x18` while the used count `+0x14` is below
  the capacity `+0x10`, else −10.

- `0x0051BA80(container, id, source, offset, …)` builds a payload on the stack (`0x0041CB90`, `0x0041D220`),
  admits a node when `id` is -1, copies the payload in, rebuilds its pointers (`0x0041CA70`) and writes the
  id into its first dword; if the payload build fails it releases the existing entry and returns -1.
- With `id` -1 `0x0051BA80` returns -1 before the build when `0x0051F150` is negative (`0x0051BAB3`-`0x0051BABF`) and
  after it when `0x0051F080` is (`0x0051BAFC`). The release on a failed build is `0x0041CF00` and then `0x0051F190` of the
  id in the entry's first dword, read before the reset; with `id` -1 a failed build releases nothing
  (`0x0051BB8F`-`0x0051BBB2`).
- `0x0051BA40` releases: it resets the entry (`0x0041CF00`) and clears the node (`0x0051F190`) without
  comparing ids. It finds the entry with `0x0051F240` and does nothing when that returns null (`0x0051BA51`);
  the node it clears is the one the id in the entry's first dword names, read before the reset (`0x0051BA5B`).
- `0x0051F190(container, id)` unlinks the node (`0x0051F4C0`), clears it as the initialiser does (state 0, id
  and links −1, source, pointer and offset 0; `0x0051F1F8`-`0x0051F211`) and lowers the used count `+0x14` to
  `count - 1`; when that reaches 0 it sets the cursor `+0x18` to 0 (`0x0051F215`-`0x0051F21B`).
- `0x0051B9F0` rebuilds every active node's cached pointer (`0x0051F620`) and every payload (`0x0041CA70`).
- `0x0051B970` updates the entries in three walks: entries with `+0x0C` bit `0x1000` set first (`0x0051BBE0`),
  then twice the others (`0x0051BBF0`) with the phase word `0x02CA83F4` at 1 and then 2.
  Each walk is `0x0051F580(container, callback, container)`, both callbacks jump to the per-entry update
  `0x0041C410`, and the phase word goes back to 0 at the end (`0x0051B979`-`0x0051B9C0`).

### How an entry picks its track

An entry plays an authored stream (`+0x368`) made of tracks. It keeps `+0x28` track states of `0xA0`
bytes from `+0x30`; the playing one is `+0x388`. The command handlers are on
[authored presentation commands](authored-presentation-commands.md).

- `0x0041CD30(entry, state, n)` sets up track `n`. It returns at once when the stream `+0x368` is null or `n` is not
  below the stream's track count, dword `+0x0C` (`0x0041CD3E`-`0x0041CD4F`), and walks the headers from stream `+0x30`
  (each header's word `+4` is the distance to the next, added in 32 bits; `0x0041CD61`-`0x0041CD69`).
- The state defaults it writes are `+0x00` and `+0x68` −1, word `+0x04` 0, `+0x08`-`+0x17` 0, dword `+0x18`
  `0x1E0000`, the float `+0x20` 30.0, `+0x48`, `+0x60`, `+0x70` and `+0x78` 0, the words `+0x50` and `+0x52` −1,
  `+0x84`-`+0x93` 0, byte `+0x94` `0xFF` with `+0x95`-`+0x97` 0, and `+0x80` = `n` (`0x0041CD75`-`0x0041CDC8`); with
  entry `+0x0C` bit `0x1000` set the word `+0x96` becomes `0x20` (`0x0041CDCF`-`0x0041CDDD`).
- It makes the track primary (entry `+0x18` / `+0x20`, state flag bit `0x1`, active byte `+0x95` 1) when its kind
  byte, header `+0`, is 1 or the stream has one track (`0x0041CDE4`-`0x0041CE01`). `+0x84` is the header's offset in
  the stream (`0x0041CE1C`).
- Its start cursor `+0x88` is the first sub-record, header `+6`, or the sub-record after a `0xFFFF` marker when
  the track has one among its header byte `+3` sub-records; `+0x90` keeps the marker's offset, else −1, and
  `+0x8C` starts at `+0x88` (`0x0041CE08`-`0x0041CE8A`). Each next sub-record is the word `+2` shifted right by 6 on
  from it, added in 32 bits (`0x0041CE48`-`0x0041CE58`).
- `0x0041CFC0(entry)` resets: it keeps a snapshot of an interrupted transition (`+0x380`, `+0x384`, entry
  `+0x2E8` bit `0x4`), rewinds every state's cursor to its start, and leaves only the primary active.
- `0x0041CFC0` takes the snapshot only when the playing state `+0x388` is set and active (byte `+0x95` = 1) with
  word `+0x96` bit `0x10`, entry `+0x0C` bit `0x1000` is clear and the state's float `+0x98` is at least 0 and
  below 0.99 (`0x008F3110`). It then sets `+0x2E8` bit `0x4` and copies the state's `+0x98` and `+0x9C` to
  `+0x380` and `+0x384` (`0x0041CFC7`-`0x0041D024`), and on every path it clears `+0x388` (`0x0041D030`).
- For each of the `+0x28` states `0x0041CFC0` clears bits `0x84` of word `+0x96`, sets byte `+0x94` to `0xFF`,
  copies bit `0x1` of `+0x96` (the primary flag) into the active byte `+0x95` and the start cursor `+0x88` to
  `+0x8C` (`0x0041D060`-`0x0041D085`).
- It also writes `+0x00` and `+0x68` −1, word `+0x04` 0, `+0x08`, `+0x10`, `+0x48`, `+0x60`, `+0x70` and
  `+0x78` 0, `+0x18` `0x1E0000`, the float `+0x20` 30.0 and the words `+0x50` and `+0x52` −1 in each state
  (`0x0041D08B`-`0x0041D0F6`).
- `0x0041C9A0(entry, n)` hands out a state other than state 0: one already holding track `n` (wiped), else
  the first inactive one. It looks at the states from 1 while below the count `+0x28`
  (`0x0041C9A6`-`0x0041C9F5`); an inactive state, byte `+0x95` = 0, is returned as it is (`0x0041C9E0`), and with
  neither it returns null (`0x0041C9F7`).
- The wipe of `0x0041C9A0` zeroes the state's `0xA0` bytes (`0x00861EC0`, `0x0041CA0A`) and sets `+0x00` and
  `+0x68` to −1, `+0x18` to `0x1E0000`, the float `+0x20` to 30.0, the words `+0x50` and `+0x52` to −1 and
  byte `+0x94` to `0xFF` (`0x0041CA0F`-`0x0041CA5C`).
- Command class `0x01` (`0x00417920`) switches to a track at once (mode 0), only when the current state's
  word is 2 (mode 1), or when entry `+0x0C` bit `0x40` allows (mode 2, otherwise it raises bit `0x80` and waits).
- `0x00417920(command, state, entry)` takes the track from bits `0xFFF0` of the command's word `+2` and the
  mode from its bits `0xF`. It does nothing when the current state already plays the track (`+0x80`,
  `0x00417943`), for modes 3 to 15 (`0x00417967`), or in mode 1 when the current state's word `+0x04` is not 2
  (`0x00417A08`).
- In modes 0 and 1 the state from `0x0041C9A0(entry, track)` gets word `+0x96` bit `0x2`, the track at `+0x80`
  and its start cursor `+0x88` copied to `+0x8C` (`0x00417A0D`-`0x00417A2D`). A current state on track 0 is then
  left as it is (`0x00417A33`); one whose dword `+0x00` is −1 becomes inactive, byte `+0x95` = 0 (`0x00417A66`);
  any other loses word `+0x96` bit `0x4` and gets word `+0x04` = 2 (`0x00417A41`-`0x00417A52`).
- In mode 2 with bit `0x40` the new state gets word `+0x96` bit `0x2` and the track (`0x00417978`-`0x0041798F`),
  entry `+0x0C` loses bits `0x40` and `0x80` (`0x00417995`), and the current state is reset in place: `+0x00`
  and `+0x68` −1, `+0x18` `0x1E0000`, `+0x20` 30.0, the words `+0x50` and `+0x52` −1, word `+0x04`, the
  eight-byte fields `+0x08`, `+0x10`, `+0x48`, `+0x60`, `+0x70`, `+0x78` and byte `+0x95` 0
  (`0x0041799C`-`0x004179D5`).
- Command class `0x0B` (`0x00417110`) asks the selector `[0x02CA4668]` (entry kind `+0x2DC`) for a choice
  and plays `table[choice] + addend` through class `0x01`. A record with `+0x284` bit `0x8000000` and a parent
  reads the parent's cached choice (`+0x4B8`..`+0x4BB` for selector kinds 0, 2, `0x0A`, `0x10`) instead.

### The choice selectors

`0x004269A0` installs the selector table `0x01F000A0` with `0x0041D6E0`: 48 kinds of `0x10` bytes, a
count and a pointer to a handler list, of which `0x00417110` calls the first handler with the stream.
The authored command `0x00` also ends with kind `0x2F`'s handler. Every kind not listed returns 0
(`0x005C5230`); the handlers read the stream's render record `+0x2E0`:

| Kind | Handler | Choice |
|---|---|---|
| `0x00`, `0x0A`, `0x0B` | `0x004223F0`, `0x00422400`, `0x00422410` | jumps to the locomotion selector `0x004256E0` with 0, 1 or 2 |
| `0x01` | `0x00422420` | a counter in byte `+0x40E`: at 0 it draws a random 0–4 (`0x003A6E60(5)`) into `+0x411`, returns it and starts counting at `[0x01DFE0B4]`; at `11 × [0x01DFE0B4]`, when the query `0x0041F2F0(record, 0x20)` reports bit `0x4`, it adds 5 to `+0x411` and returns that; otherwise it counts up to at most 100 and returns −1 |
| `0x02` | `0x00422500` | the byte `+0x410`, chosen once while it is −1 from the bits of `0x0041F2F0(record, 0x30)`: bit `0x2` counts `+0x40E` up (back to `[0x01DFE0B4]` past three times that) and chooses 0; otherwise 1 with bit `0x4`, else 2, and `+0x40E` is cleared |
| `0x04` | `0x00660570` | −1 |
| `0x10` | `0x004225A0` | counts down `+0x412`, armed while it is −1 with `(rand() % (b - a + 1) + a - 1) x [0x01DFE0B4]` for the stream's bytes `a` = `+0x2DD` and `b` = `+0x2DE` (`0x004225C3`-`0x004225F8`), and chooses 1 when it reaches 0, setting it back to −1 |
| `0x20` | `0x00422630` | 0 when the point from `0x0041F2F0(record, 4)` lies within ±90° of the record's heading (`0x00424370`: `atan2` of x and z in the record's own frame), else 1 |
| `0x21` | `0x004226C0` | with `d` the angle from `0x00424370` times 57.295776: 0 for `-60 <= d <= 60`, else 1 for `d > 0` and 2 for `d <= 0`; plus 3 when `0x003A6E60(2)` is non-zero (`0x004226FF`-`0x00422742`) |
| `0x22` | `0x00422760` | 1 when the vertical angle to the point (`0x00424460`) is negative |
| `0x23` | `0x004227D0` | 0 within ±60°, else 2 or 3 by side |
| `0x24` | `0x00422870` | the quarter the point lies in (0 ahead, 1 at 45°–135°, 2 at −45° to −135°, 3 behind) in record byte `+0x2AF`, plus 4 on a random half: with `d` the angle from `0x00424370` times 57.295776, `+0x2AF = -45 <= d <= 45 ? 0 : 45 < d <= 135 ? 1 : -135 <= d < -45 ? 2 : 3`, and the return value is that byte plus 4 when `0x003A6E60(2)` is non-zero (`0x004228AF`-`0x00422929`) |
| `0x25` | `0x00422940` | from the angle to the record that the look controller's source names (`0x003E2CD0`): 0 between −90° and 0°, 1 at −90° or less, 2 above 90°, 3 between 0° and 90°; 0 without a source |
| `0x2F` | `0x00422A10` | clears the word `+0x456` and sets byte `+0x2AF` to −1, returning −1 |

`0x00424460(matrix, point)` turns the point into the record's own frame (the matrix at `+0x180`) and
takes `atan2` of its y and z.

### The per-entry update

`0x0041C410(entry)`, from `0x0041D820`, `0x00422EB0`, `0x002EE3E0` and the two walk callbacks `0x0051BBE0` and `0x0051BBF0`
(`0x0051BBE7`, `0x0051BBF7`), runs an entry only when its record's `+0x6E0` is 1 in main-loop state 3 (`0x00229EA0`) or
0 in any other state, the entry's `+0x0C` has
bit `0x2` set and bits `0x40000` and `0x800000` clear, the speed `+0x340` is non-zero, and the status table entry
`0x003E7D10(+0x6A4, 3)` is 0 or the record's `+0xC0` bit `0x40` is clear. In phase 1 of `0x02CA83F4` it runs
only records with `+0x284` bit `0x8000000` and no parent, and in phase 2 it skips those.

- In state word `+0x24` = 1 with `+0x0C` bit `0x8` and `+0x2C8` bit `0x1000` set, it resets the entry
  (`0x0041CFC0`), clears `+0x2C8` bit `0x1000` and `+0x0C` bit `0x200` and, for a positive
  `+0x348`, seeks there (`0x0041D820`) and sets `+0x24` to 0 when `+0x348` equals `+0x34C`, else 1.
  With only `+0x2C8` bit `0x1000` set and `+0x348` not −1 it sets `+0x24` to 2.
- With the record's `+0x4B7` bit `0x10` set it picks the locomotion mode (`0x004255B0`).
- It runs every track state through the walker `0x0041DA90`, then calls `0x0041DD40` on states 1 and up
  until a pass finds no state to act on, sets `+0x0C` bit `0x100`, and copies whether `0x003E7D10(+0x6A4, 3)` is
  non-zero into the record's `+0xC0` bit `0x40`.

`0x004255B0` gives controller 5 (`0x003E4890` → `0x0051A920`) a mode from the record's speed `+0x23C`
(taken as 0 while `+0x62C` bit `0x1` is set or `0x003AEF20(+0x550)` reports): 0 below the walk threshold
`0x003E58B0` (the scale times an `@FCP` value, 0.013333 without one), 2 at or above `+0x420`, and
otherwise 1 when the move direction `+0x244` is within 45° of the facing `+0x124`, 3 from 45° to
135°, 4 from −45° to −135°, and 5 behind.

`0x004256E0(entry, mode)` is the full locomotion selector; motion commands `0x00`, `0x0A` and `0x0B` jump to it with
mode 0, 1 and 2. It reads the entry's render record (`+0x2E0`), takes the speed `+0x23C` as 0 in the same two
cases as `0x004255B0`, and turns headings into degrees wrapped to ±180. The turn is the facing `+0x124` minus
`+0x254`, taken as 0 unless the entry's `+0x31C` top nibble is 2. It picks a state:

| State | When |
|---|---|
| 14 | the actor is asleep: `0x003E7D10(+0x6A4, 4)`, the status-visual record's Sleep dword `+0xD0` |
| 0 | below the walk threshold `0x003E58B0` and the turn is 0 or under `[0x01DFE0BC]` degrees either way |
| 6, 7 | below the walk threshold with a larger turn: 7 when section 9's `+0xA4` (`0x003E5EA0`) is set and the turn times `[0x01DFE0B8]` reaches its `+0xA8` (`0x003E5C90`) in degrees, else 6 |
| 1, 3, 4, 5 | below the run threshold `+0x420`: as `0x004255B0`, 1 within 45° of the facing, 3 from 45° to 135°, 4 from −45° to −135°, 5 behind |
| 2, 10, 9, 11 | at or above `+0x420`: 2, or, when the record has a target record (`0x00512EC0(+0x650)`) and bit `0x20` is set in byte `+0x3C` of the record `0x002ED500(+0x108, 0x1000, out)` fills, the angle to that target (`0x00424370`, `0x00424280`): 2 within 45°, 10 from 45° to 135°, 9 from −45° to −135°, 11 behind |

A model can lack a state. Through `0x004FE2F0` the selector reads one byte per direction from dword `0x30` of the
model's `@FCP` section 9 (ids `0x63070F30`, `0x62070E30`, `0x61070D30`, `0x60070C30`; payload version 7 or later,
else the default 0) and byte 3 of dword `0x2D` (`0x63070B2D`) for state 7, and falls back:

| States | Property | 0 | 1 | 2 or more |
|---|---|---|---|---|
| 1, 2 | `0x63070F30` | 0, and the mode goes to controller 5 (`0x003E4890`) | kept | kept |
| 3, 4 | `0x62070E30` | 0, and the mode goes to controller 5 | 1 | kept |
| 9, 10 | `0x62070E30` | 0 | 2 | kept |
| 5 | `0x61070D30` | 0 | 1 | kept |
| 11 | `0x61070D30` | 2 | 2 | kept |
| 7 | `0x63070B2D` | 0 | 1 | kept |
| 6 | `0x60070C30` | 0 | 1 | 2: 1 when the low six bits of byte `+2` of the actor's resource block (`0x00422D90` of entry `+0x310`, `+0x318`) are below 16; 3 and 5 kept; 4: 1 when those bits are non-zero |

Over the 1,066 shipped models the forward byte is 0 in 626 (343 of them by default), 1 in 129, 2 in 10 and 3 in
301; the sideways and backward bytes are 0, 1 or 2; the turn byte runs 0 to 5.

The selector then sets the entry's `+0x0C` bit `0x2000`. In mode 1, and in mode 2 when `0x002ED530` answers for the
record's actor (`+0x108`), it times the states with two byte counters in 30 fps frames (`[0x01DFE0B4]`, 1 at 30
fps, 2 at 60):

- Walking (1, 3, 4, 5) counts `+0x456` up to 90 frames, starting it at 30 when the previous state `+0x2A0` was 0.
  Below 3 frames it keeps the previous state, so a change of gait waits a tenth of a second; a previous state 15
  becomes 0.
- Running (2, 9 to 11) counts `+0x457` up to 90 frames.
- Standing (0) after at least 30 frames of running becomes 8, the stop; a previous 8 stays while `0x0041C720`
  reports its motion still on byte `+0x95` = 1. States 0, 6 to 8 and above 11 clear both counters.

`0x002ED530(actor)` is 0 without an actor. While the field is live (the cached copy `0x02099DE0` of `0x00265680`,
which `0x00265760` reads) it is `0x0030BEB0`: for a party-side battle unit (stats `+0x05` = 0) with unit flag bit `0x8`
set, the inverse of unit flag bit `0x800000`, else 0. Otherwise it is bit `0x2` of the presentation record's byte `+0x29`
when its bit `0x1` is set, else 0 (`0x002637D0`).

The state is stored at `+0x2A0`. Mode 0 returns 9 to 11 as 8 to 10 and 14 as 11; mode 1 returns 14 as 12; mode
2 returns every state from 9 one lower, and 8 as 12 and 2 as 11 when `0x002ED530` answers, else 8 as 0. The
return value's low word is the state; its high word is 1 minus a flag that is the record's `+0x418` bit `0x1`, set
for states 0 and 14, and for 6 and 7 whether the turn is positive.

Smaller entry helpers:

- `0x0041D7E0(entry, start, end, limit)` stores the time window `+0x344`, `+0x348`, `+0x34C`, pulling
  `+0x344` down to the limit when both are set and the limit is smaller.
- `0x0041D110(entry)` resets, clears `+0x2C8` bit `0x1000`, seeks to `+0x344` when it is set (with `+0x0C`
  bit `0x10000000` raised around the call) and sets `+0x24` to 1.
- `0x0041D4D0(entry, on)` sets or clears `+0x0C` bit `0x1000`, `+0x33C`, and bit `0x20` of every state's word
  `+0x96`.
- `0x0041CEC0(entry)` calls bank-A slot `0x0C` (`[0x02CA4470]`) with the actor `+0x2C0` and `+0x31C` and
  sets `+0x0C` bit `0x200`, as the walker does at a motion's end.
- `0x0041C970(entry, n)` returns the state playing track `n` (state `+0x80`); `0x0041C720(entry)` returns
  whether the state playing the entry's track `+0x26` has byte `+0x95` equal to 1; `0x0041C6B0(entry)`
  returns `+0x0C` bit `0x8000`. `0x0041C3A0(entry)`, which `0x00423280` reaches by a tail jump (`0x004232B9`),
  returns the word `+0x1A` of the record at `+0x18` as a float (`0x0041C3A0`-`0x0041C3AF`).

- `0x0041C770(entry)`, for `0x00423380`, returns the dword `+0x0C` of the first state after state 0
  whose byte `+0x95` is 1, or 0.

## Layouts

The access tables beside this page list every instruction found touching each structure:

- [the reference container](character-render-records-presentation-entry-reference-container-accesses.tsv).

## State

- A presentation-entry id carries no generation: a stale id names whatever now occupies its slot.

## Related

- [Character render records](character-render-records.md): the record array, its lifecycle and render events.
- [Skeleton entries and bones](skeleton-entries-and-bones.md): the skeleton entries, bones, bone points and ties.
- [Authored presentation commands](authored-presentation-commands.md): the command handlers.
