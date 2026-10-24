---
title: "Party list: the member rows on the HUD, the rolling HP and MP numbers, the action bar, the status mark, choosing a new leader and picking a member as a target"
kind: "system"
category: "Menus and HUD"
addresses: "0x0029BE50, 0x0029A0A0, 0x00299090, 0x002986E0, 0x00297C10, 0x002973E0, 0x00271960, 0x00272F80, 0x00296BE0, 0x00297170, 0x0029B870, 0x00297640"
---

## What the player sees

- The party list shows one row per party member, guest and Esper: the name, HP, and MP for members and guests.
- When HP or MP changes the number rolls to the new value instead of jumping, and the row flashes when a damage or
  healing number pops up.
- A status mark and its name cycle through the member's statuses one at a time.
- Beside each row a bar fills while the member charges an action, with the action's name, and flashes when it is full.
- Pressing Up or Down in the field opens "Select a new party leader." and moves a cursor over the rows; in battle the
  same rows serve as the cursor when a command targets a party member.

## How it works

### The list and its rows

`0x0029BE50` is the list widget, `0xB68` bytes, built by `0x002964D0` when the party has a member (`0x0035BB60`) and kept at
`[0x0209BE80] + 0x10F78` ([HUD](hud.md)). `0x0028FD70` builds it, and the widget `0x0029BC80` at `+0x10FC8` beside it
(`0x00296AA0`).

On a chocobo ride (`0x00303EC0`) it closes both, and while action policy bit `0x400` is set it closes the list
and shows the widget `0x0029C530` at `[0x0209C300]` instead (`0x00297100`). `0x00290E10` closes the list and `0x00296A70` the widget beside it;
`0x002970C0` closes `[0x0209C300]`. Each close first sets bit `0x10000` of the widget's `+0x40` when `0x002544B0` answers 1.

`0x0028FD70` also calls `0x003CA1E0` (`0x0028FD99`), which, when the object at `[0x02B47758]` exists, clears bit `0x2` and sets
bit `0x1` of its `+0xA90`.

On message 1 the list reads its layout, layout record `0x15`, takes the member count from `0x022C8064`, the leader's
index from `0x022C8074` (`0x0035BAE0`), and builds the header `0x0029B700` at `+0xB38` (`0x0029BEAB`-`0x0029BF2A`).
`0x00296450` gives the y position of the first row from the header's layout.

### Building the rows

Each frame (message 2) the list checks the member count. When it changed it releases its rows and bars, clears the
four member cells (`0x0028F830`), and sets bit `0x40` of `+0xB4A`; once they are gone it rebuilds through `0x0029BB40`
(`0x0029C124`, `0x0029C134`):

1. A member record with a type and a handle gets a row kind in `+0xB44 + i`: 2 for flag bit `0x2` (types 7-25), 3 for
   flag bit `0x4` (types 27-39), 1 otherwise.
2. A waiting kind builds the `0x160`-byte row `0x0029A0A0` at `+0x240 + i x 0x160`, with the list at its `+0x120`
   (`0x0029BBD3`).
3. Once the list has finished opening, it builds one `0xD8`-byte action bar `0x00299090` per member at
   `+0x7C0 + i x 0xD8` and sets `+0xB4A` bit `0x10` (`0x0029C374`-`0x0029C38C`).

The member records are the `0xC0`-byte records at `0x022C8080 + i x 0xC0` (`0x0035BB20`), described on
[Party member status record](../Characters-And-Objects/party-member-status-record.md).
`0x0035BB00(i)` returns record i's actor handle, the dword at `0x022C8084 + i x 0xC0`.

`0x0035BB70`, run by the field set-up `0x00253A30` (`0x00253A3E`) and the teardown `0x003C5E50` (`0x003C5EA7`), clears the
whole `0x348`-byte block from `0x022C8060`, keeps only the bits `0xFFFC02EC` of the mode word `0x022C83E8`, runs
`0x002419B0()`, closes the leader-choice window in `0x022CA428` and the window `0x0035E070` keeps in `0x022CA430`
(`0x00244F00`), and ends in `0x002A1E90`, which closes the widget in `[0x0209C4C8]`.

`0x0035D570(unit)` returns 1 when the unit's handle is one of the `[0x022C83F0]` words at `0x022C83F8`; the overhead
gauge `0x002C6F70` gives a unit an entry when `0x00273320(unit)` is not negative or `0x0035D570(unit)` is 1.

### What a row shows

A row draws the parts in [Battle menu](battle-menu.md) (name, HP, HP gauge, maximum HP, MP and MP bars) and also:

- the name from `0x00296600(type)` when the type has one, else the record's name (`0x00297F60`): types 0-6 are
  "Vaan", "Ashe", "Fran", "Balthier", "Basch", "Penelo" and "Reks" (`0x009161F0`), 7-16 the guests from "Amalia" to
  "Reddas" (`0x00916200`), 27-39 the Espers from "Belias" to "Zodiark" (`0x00916218`);
- one of three HP frames by digit count: `0x00297710` takes the larger of HP and the cap `+0x28`, below 100, below
  1000 or 1000 and above;
- one of three MP frames by the bar count `+0x87`, 1 to 3, or none for 0 (`0x00297880`); rows of kind 3 draw no MP;
- the status mark and name (`0x00297FE0`), and the summon gauge on the summoner's row (`0x0029B1C0`), below.

### Row effects

A row's flag word `+0xD8` (`+0x318 + i x 0x160` in the list) drives its effects:

| Bit | Effect |
|---:|---|
| `0` | the row takes part in a pick mode; the list's draw hook `+0xB28` may then draw the hand cursor on it (`0x0029A19C`, `0x002426F0`) |
| `1` | the row is refused in a pick mode; its widget's brightness `+0x5A` becomes `+0x5A >> 1` (`0x0029A247`-`0x0029A24B`) |
| `2` | the cursor is on the row; its brightness `+0x5A` pulses, `0x00296FB0(32, 128, 0)` (`0x0029A25C`-`0x0029A264`), and a pointer is drawn (`0x0029A1EA`) |
| `3` | the row is closing |
| `4` | a status pulse: brightness `+0x5A` and alpha `+0x58` follow the track `0x009162B0` over `+0x110` (`0x0029A223`-`0x0029A23D`), 16 a frame (`0x00299890`) |
| `5`, `6` | an HP or MP flash, below |
| `7` | nodes 0-2 fade out over 8 frames, and back in once it clears (`0x00298130`) |

`0x00296FB0(amplitude, base, phase)` is `base + amplitude x sin((frame x rate - phase) x pi / 15)`, with the rate 1, or
one over the speed steps while the game runs at speed (`0x00229DF0`, `0x00229E70`). A row whose shown status has flag
bit `0x2` at `+0x25` is also drawn at half brightness (`+0x5A`, `0x0029A267`-`0x0029A282`).

### Flashes

`0x0028FBE0(popup)`, run for every battle number the popup queue `0x003BBD00` adds (`0x003BBE6C`), flashes the member's row
by the popup's kind byte `+0x0D`:

| Kind | Flash |
|---|---|
| `1`, `5` | HP: bit `0x20`, `0x00297040(list, handle, 0)` |
| `3`, `7` | MP: bit `0x40`, `0x00297040(list, handle, 1)`, not on a row of kind 3 |
| `2`, `6` | status pulse: bit `0x10`, `0x00296E90` |

`0x002994E0` draws the HP flash as a highlight sprite round the union of the HP digit nodes (`0x00271DB0`), as wide as
the digit frame plus 24 for each node past the first (`0x002998D0`). For the draw it sets the widget's
`+0x58 = (+0x58 x a) >> 7` and `+0x5A = (+0x5A x b) >> 7`, `a` and `b` the bytes `+6` and `+7` of the three-key track
`0x009162D8` at time `+0x114`, and restores both afterwards (`0x0029957C`-`0x002995BF`).

`0x002996E0` does the same round the MP frame with the time `+0x116`. Each time steps `t += 8` a frame; above 255 it
goes back to 0 and the flash bit clears (`0x0029A467`-`0x0029A4AD`).

`0x00271AB0(out, keys, n, t)` evaluates a track of `n` 12-byte keys (`s16` `+0`, `s16` `+2`, `u16` time `+4`, bytes
`+6`, `+7`, `s16` ease `+8`, `s16` `+10`). It takes the first pair with `time[k] <= t < time[k+1]`, else the last
pair, and with `d = t - time[k]` and `span = time[k+1] - time[k]` sets `f = d x 256 / span`, or
`int(256 sin(pi/2 x d / span))` for ease 1 in key `k+1`, or `256 - int(256 sin(pi/2 x (span - d) / span))` for ease 2.
Each field is `v[k] + (v[k+1] - v[k]) x f / 256`, truncated (`0x00271AB0`-`0x00271CA9`).

### Rolling numbers

HP and MP roll through counters, `0x58`-byte records, two per member at `0x0209BF40 + i x 0xC0` and two for the target
window at `0x0209C240`. `0x00297C10(record)` finds the pair holding the record's handle or takes a free one, sets it up
with `0x003F89C0` and the callbacks `0x0029B7D0` (HP) and `0x0029B810` (MP), and registers both in the HUD's counter list
`+0x80` (`0x003F8A50`). `0x002962D0` unregisters pairs whose handle no longer resolves (`0x002732E0`, `0x003F8A30`), and
`0x00296360(record, handle)` does the same for the target window's pair (from `0x002C0870`).

`0x003F8A30(list, node)` first moves the list head on to the node's next (`+0x28`) when the node is the head, then
runs `0x003F8BF0(node)` (`0x003F8A42`): it calls the node's callback `+0x38` with 5, links its previous `+0x30` and next
`+0x28` neighbours to each other, clears both links and the word `+0x26`, and calls the callback again with 6.

`0x0028F1F0(handle, old, new, mp)`, called by the HP write `0x00300530` (`0x003006E7`,
[HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)) and the MP write `0x00300CE0` (`0x00300DD3`,
[MP](../Status-Effects-And-KO/mp.md)), starts a roll: it finds the member's pair (`0x00296280`), or the target window's pair
when its handle matches, and sends the HP or MP counter message 1 (`0x003F8980`). The HP callback passes the maximum
`+0x24`, the MP callback the capacity `+0x30` times the bar count `+0x87` (`0x0029B7D0`, `0x0029B810`).

### How a roll moves

`0x002973E0(counter, from, max, to)` starts it:

1. A counter at rest starts from the old value (`0x002726C0`); a running one starts from the value it shows
   (`0x00271960`, `0x00272730`).
2. The path keeps from and to in 1/16 units and three points between, at `0x94`, `0xD4` and `0xF3` of 256 of the way.
3. Its length is the change times 100 over the maximum, between 10 and 50 frames (`0x002727C0`, step `0x400` / frames);
   a change of 1 or less puts the counter at rest at once.

Each HUD frame group 2 steps every registered counter (`0x003F8B40`): `0x00272710` advances the step and `0x00271960` gives
the shown value. The five points are from, the three between, and to, one quarter apart:

- with the step below `0x400`, `u = step / 256`, `i = int(u)`, `t = u - i` and the points `P0`-`P4` in that order,
  over the first three quarters the value follows a spline through them (`0x00271960`, `0x00270260`). Segment 0 is
  `0.5 x ((P0 - 2 P1 + P2) t^2 + (4 P1 - 3 P0 - P2) t)`, 0 at `t = 0` and `P1 - P0` at `t = 1` (the basis at
  `0x009157B0`; its constant term multiplies the point matrix's first row, which `0x00270260` makes zero at `0x0027034F`);
- segments 1 and 2 are the Catmull-Rom `0.5 x ((3 P[i] - P[i-1] - 3 P[i+1] + P[i+2]) t^3 + (2 P[i-1] - 5 P[i] +
  4 P[i+1] - P[i+2]) t^2 + (P[i+1] - P[i-1]) t + 2 P[i])` (the basis at `0x009157F0`, points from `0x00276220`), the
  0.5 being the vector at `0x00915870`;
- over the last quarter it moves in a straight line, `P3 + (P4 - P3) x (u - 3)`, from the third point between to the
  target. The shown value is `int(x) >> 4` (`0x00271960`).

The row shows the counter's value at `+0x50` while it runs, and the record's value at rest (`0x0029A4CE`, `0x0029A5FD`).

### The status mark

`0x00297FE0(row, record)` copies the status presence word `+0x44` into the row's status record at `+0xF0` and steps it
with `0x00272F80(+0xF0, 30, 0)`. With n statuses to show, each shows for `max(36 - 6n, 12)` frames in display order,
after a blank of `ceil(30 / that)` periods (`0x00272F80`). The mark shows the status's sprite and its name, text
`0x46B7` plus the status, such as "KO" (`0x46B7`) or "Stone" (`0x46B8`), in colour 5 when the status has flag bit `0x1`
at `+0x25` and 4 otherwise.

The display orders are four tables of pointers to copies of the 32 status rows, class `0x1A`, that `0x00273BA0` builds
at `0x022C8B08 + 0x1500`, `+0x1600`, `+0x1700` and `+0x1800` (`0x0035D490`):

- `0x00273410(order)` returns a table and `0x00273380(mask, order)` the first status of the mask in it;
- a status counts in order 0, 1, 2 or 3 only when its byte `+0x21`, `+0x23`, `+0x22` or `+0x24` is not -1
  (`0x00275E40`), and in order 2 also when `0x003178C0` passes it for the unit;
- `0x00273160(out, flags, unit)` returns the first status of a unit in order 1 and its flag bits, for the overhead
  gauge `0x002C6F70`.

`0x00273BA0` builds each order as a list of 4-byte entries (`0x00273C63`-`0x00273DB8`), and the Party Menu's member rows
(`0x00284030`) and the Status pane (`0x002C573E`) make the same list for one unit's statuses:

1. The member rows and the Status pane first fill n entries with `0xFEFE` (`0x002D0280(list, n)`).
2. `0x002D02C0(list, n, mask, order)` writes, for each status of the mask below n, its number, its byte for the order
   (`+0x20`-`+0x24` of its class `0x1A` record) and bit `0x1` of its `+0x25`, and answers how many have a byte other than
   `0xFF`.
3. `0x002D03B0(list, n)` sorts them by that byte, highest first (`0x00249CE0` with the comparator `0x002D0270`).

`0x002D02A0(entry, mask)` answers whether an entry is a real status with a byte and set in a mask. The member row shows
at most 11 entries and skips status `0x1D` (`0x00284058`-`0x00284070`).

The Status pane `0x002C59D0` keeps 32 such entries at `+0xC8` and its mask at `+0x148`:

- `0x002C5810(pane, dir)` moves the pane's cursor `+0x14D` to the next entry that passes `0x002D02A0`: dir 0 and 1
  step back and forward, 2 and 3 by the list's column count (`+0xEC`), wrapping round the 32 entries. It
  answers 1 when the cursor moved. `0x002C5EC0(pane, dir)` answers whether such a move finds an entry without
  wrapping.
- `0x002C5900(pane, row, ..., i)` is the row painter the pane installs (`0x002C5A7F`). For an empty entry it hides
  both of the row's elements; otherwise it gives the first the status's sprite cell and the second the text at
  `+0x18` of the status's class `0x1A` record (`0x002B58B0`), in colour 4 when the entry's third byte is set and
  5 otherwise (`0x002DD7E0`).
- `0x002C5660()` returns the widest text at `+0x10` of those records (`0x002B3050`) among the statuses that the
  nine party records hold (`0x00282DF0`: `+0x60` not negative, the mask `+0x44`).

The HP number's colour comes from the statuses present, in order 0 (`0x00271FB0`, `0x00297D62`): colour `0xB5` when one
has bit `0x10` at `+0x25` and `0xB6` for bit `0x8`, pulsing by `128 + 32 x sin(frame x pi / 30)` (`0x00271EF0`); a status with
bit `0x2` at `+0x25` halves each channel, `c x 0x40 >> 7` in place of `c x 0x80 >> 7` (`0x00297D67`-`0x00297DAE`).

### The summon gauge

While an Esper is out (`0x003135C0`), the row of the member whose type equals the summon block's `+0x2C` (`0x003200A0`,
`[0x02EBF190] + 0x5AD4`) shows the summon node and `0x0029B1C0(row, left, total)` draws it as five segments from the
summon timer `+0x5AD8` and its length `+0x5ADC` (`0x0029A39D`-`0x0029A407`). Lit segments pulse with
`sin(frame x pi / 60)`; the segment being used up fades by the time left in it, the first never below `0x20`.

`0x0029B490(row, on)` steps a six-frame mark through the frames `4`, `0x16`, `0x17`, `0x18`, `0x19` and `5` while the
record's flag bit `0x20000` is set and back while it is clear (`0x0029A5D9`). `0x0029AFE0` pulses node `0xB8`'s
brightness between `0x80` and `0xFF` while flag bit `0x80` is set.

### The action bar

The bar `0x00299090` keeps its state in the member's `0x20`-byte cell (`0x0028F830`), cleared when the member's type
changes. It shows while the record's flag bit `0x200` is set or its action id `+0x5C` or issued command `+0x5E` is below
`0x4000`, and flag bit `0x40` is clear; otherwise it closes once its count `+0xCA` passes 3. Each frame
`0x002986E0(bar, record)`:

1. shows the action's name (class `0x14`, `0x0029FB50`) once flag bit `0x2000` is set and the id changed;
2. fills to `pct = +0x3C x 100 / +0x40` percent, a maximum of 0 counting as 100 (`0x00298BD0`-`0x00298BD5`), or 100
   with flag bit `0x1000`;
3. on reaching 100 flashes for 8 frames with `sin(t x pi / 15)` (state 1), then fades out by 16 a frame (state 2);
4. blends two colour pairs from `0x002DD7E0`, each channel `c0 + (c1 - c0) x f / 256` (`0x002752E0`), and cycles a
   four-key colour track (`0x00274870`, `0x00271E50`) while `0x00226BA0` answers 0:
   - filling (state 0): `f = pct x 256 / 100`, colour `0x7A` to `0x7B` and `0x7E` to `0x7F` (`0x00298F9B`, `0x00298FB0`);
   - flashing (state 1): `f = 128 + int(128 sin((frame - start) x pi / 15))`, `start` the frame stored at cell `+0x0C`, `0x7B` to `0x7C` and `0x7F` to `0x80`
     (`0x00298E0A`, `0x00298E23`);
   - fading (state 2): `f` the fade count, which steps by 16 to 256, `0x7C` to `0x7D` and `0x80` to `0x7E`
     (`0x00298C4C`-`0x00298CC1`).

`0x00297290` fades the bar's frame in and out by 16 a step (tracks on the stack, `0x00271AB0`).

### Choosing a new leader

Request 3 ([Menus](menus.md)) reaches `0x00290500(1)`, which runs `0x00296BE0(list, 1)`:

1. A list already in pick mode 2 refuses; otherwise the mode `+0xB49` becomes 1 with the handler `0x00297640`.
2. `0x00299BD0` offers each row whose member has a handle, is not KO (flag bit `0x1`), has flag bit `0x40` clear and passes
   `0x002739D0`; the others are refused.
3. The cursor starts on the leader, or the next offered row (`0x00296D96`, `0x00296DA7`).
4. The header closes, the overlay `0x0029C9D0` opens over the rows, and the list takes the focus (`0x002470D0`).

`0x00296BE0(list, 0)` undoes it: the header reopens, the focus is given up, the overlay closes and every row loses
bits `0x1`, `0x2`, `0x4` and `0x80`.

### The buttons

In either mode the list's input turn runs `0x0029B870` and keeps the answer at `+0xB43` (`0x00296570`). The first turn
only plays sound 4 (`0x0029BFB5`). Each press is offered to the handler `+0xB20`, which may refuse it (`0x0029B790`):

| Press | Answer |
|---|---|
| cancel (`0x01E0C2A4`) | `3` |
| Square | `8` |
| Left or Right | `6` |
| confirm (`0x01E0C2A0`) | `2` |
| L1, R1 | `4`, `5` |
| Up, Down, a wheel notch | moves to the next offered row, 1; at an end, 7 |

Up and Down wrap on a new press and stop at the ends on a repeat (`0x002975B0`); the wheel counts as a repeat
(`0x001E0A10`, `0x001E0E30`).

### The leader handler

`0x00297640(list, answer, member, row)` decides for mode 1:

| Answer | Result |
|---|---|
| 1, moved | the target window shows the member (`0x0029B440`) and sound 1 plays |
| 2, confirm | sound `0x15` on an offered row; sound 5 and a refusal on a refused one |
| 3, cancel | allowed with sound 3 when the current leader can still lead (`0x00299B90`, `0x0035BC30`); else sound 5 |
| `6` | sound 5, refused |
| `4`, `5`, `7`, `8` | refused |

An allowed confirm makes the row's member the leader (`0x0035BAA0` with its type), then `0x0035C100(1)`, `0x0035DA80`,
`0x003C93E0(0)`, `0x0035C080` and `0x0035C050(0)` (`0x0029C008`-`0x0029C033`); an allowed cancel closes the mode through
`0x0035D8D0` (`0x0029C04C`-`0x0029C058`).

### Picking a party member as a target

The battle menu turns the list into its cursor for a target list of party members through `0x002904D0(page, start)`,
which runs `0x00297170`:

1. In mode 1 it refuses. Otherwise `+0xB50` points at the target page, `0x0029AEF0` offers the rows whose member is on
   the page and refuses the others and those whose entry has flag bit `0x2`, the greyed bit, and `0x0029AE50` puts the
   cursor on entry `start`.
2. The list takes the focus with mode 2 (`0x002470D0`).
3. `0x002904D0(0, 0)` ends it: the frame at `+0x180` closes, the focus is given up and the marks are cleared.

The menu works the list through small calls:

| Call | Does |
|---|---|
| `0x00290590(page)` | refreshes the offered rows (`0x00296A10`) |
| `0x00290490` | the page entry under the cursor, or -1 (`0x00296580`) |
| `0x00290520`, `0x002905B0` | read and set the last answer `+0xB43` (`0x00296570`) |
| `0x00290470` | 3 when there is no list |
| `0x002969F0(list, handler, context)`, `0x002969E0(list, hook)` | set the handler `+0xB20` with its context `+0xB30`, and the draw hook `+0xB28` |
| `0x00296ED0(list, on)` | sets bit `0x100` of `+0xB4A`, which opens the frame `0x0029C770` round the rows; off clears the row marks |
| `0x00296E00(list, handle)` | writes 3 into the member's cell `+0x1A` |

The frame and the leader-mode overlay `0x0029C9D0` take their box from `0x002974E0`: the first row of kind 1, stretched
over the height of all rows.

`0x0029B120(list, row)` raises one row and its bar above the others (priorities 2 and 3 against 4 and 5), for the
moving pointer `0x0029C850`.

## Layouts

The counter record, `0x58` bytes, two per member at `0x0209BF40`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | from | start value x 16 |
| `+0x04` | `i32` | to | target value x 16 |
| `+0x08` | `i32[3]` | points | the three points between |
| `+0x14` | `i16` | t | progress, 0 to `0x400` |
| `+0x16` | `i16` | step | `0x400` / length in frames |
| `+0x26` | `u16` | flags | bit `0x1` at rest, bit `0x2` registered |
| `+0x28` | `CounterRecord*` | next | in the HUD's list |
| `+0x30` | `CounterRecord*` | prev | |
| `+0x38` | `fn*` | callback | messages 0 to 6 |
| `+0x48` | `PartyMemberStatusRecord*` | record | the member |
| `+0x50` | `i32` | shown | the value drawn |

The list widget `0x0029BE50`, `0xB68` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xB20` | `fn*` | pressHandler | the handler each press is offered to (The buttons): `0x0029B790` and `0x0029B870` call it with the context `+0xB30`, the answer and the byte `+0xB48` (`0x0029B7AA`-`0x0029B7B9`, `0x0029B899`-`0x0029B8BC`), and a return of 0 refuses the press; with no handler every press is taken (`0x0029B79E`-`0x0029B7A0`). `0x002969F0` sets it with its context (`0x002969F5`, `0x002969FC`): the battle menu installs `0x0027E3E0` (`0x00279C12`-`0x00279C1C`) and clears it with 0 (`0x00276E9E`, `0x00278F52`, `0x00279C3C`, `0x0027A88C`) |

The row widget `0x0029A0A0`, `0x160` bytes, four at the list's `+0x240`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0DC` | `u8` | hpFrame | the HP frame in use (What a row shows): 1 for values below 100, 2 below 1000, 3 for 1000 and above, of the larger of HP and the cap `+0x28`; `0x00297710` stores it (`0x00297751`) and swaps the frame's nodes only when it changes (`0x0029773E`-`0x00297747`). The HP digit draws `0x00297D10` and `0x00297E70` take their digit node from the tables `0x00916300` and `0x00916308` by it and draw frame + 1 digits (`0x00297DC3`-`0x00297DE8`, `0x00297E89`-`0x00297E9F`, `0x00297F1D`), and the HP flash `0x002994E0` picks its nodes by it (`0x00299522`) |
| `+0x0F0` | `u8[24]` | statusCycle | the status cycle record, below; `0x00297FE0` passes `+0xF0` to `0x00272F80` (`0x00298014`, `0x00298036`) |
| `+0x112` | `i16` | dimFade | the fade of nodes 0-2 for flag bit `0x80` (Row effects): `0x00298130` adds `0x20` a frame up to `0x100` while the bit is set and takes `0x20` off down to 0 once it is clear (`0x00298145`-`0x0029817A`), then gives the alpha of each of the four corner colours of nodes 0-2 the value `a x (0x100 - t) / 256` (`0x00298182`-`0x00298241`) |
| `+0x118` | `i16` | noStatusNode | 4: the node of the child layout at node `+0xE0` that is drawn (its `+0x08` bit `0x1`) only while no status is shown, `+0x100` = 0 (`0x0029A982`-`0x0029A9A7`, `0x0029ABAE`-`0x0029ABD7`); `0x00297880`, choosing the MP frame, writes it with `+0x11A` as the dword `0x10004` (`0x00297A6A`, `0x00297B5A`) |
| `+0x11A` | `i16` | mpDigitNode | 1: the node of the same child layout that `0x0029A8E0` draws the MP number into as three digits when it differs from `+0x138` (`0x0029A904`-`0x0029A925`), and the first of the nodes n, n + 1 and n + 2 round which `0x002996E0` draws the MP flash (`0x0029972B`-`0x0029975E`, `0x002997A9`) |
| `+0x128` | `i32` | markStep | the step of the six-frame mark of `0x0029B490` (The summon gauge): 1 more each call up to 11 while the record's flag bit `0x20000` is set, 1 less down to 0 while it is clear (`0x0029B4F1`-`0x0029B51D`); the frame shown is entry step / 2 of the six, written to node 0 of the child layout at node `+0xE0` (`0x0029B523`-`0x0029B535`) |
| `+0x148` | `u32[3]` | mpBarLevel | one level per MP bar, 0 to `0x100`: each draw `0x0029A930` adds 16 to bar i's while i is below the charges `+0x86` and takes 16 off otherwise (`0x0029ACD0`-`0x0029ACEC`), and colours the bar from its three-key track at that level (`0x00271AB0` at `0x0029AD1C`, `0x0029AD21`-`0x0029ADF4`); the loop runs over the bar count `+0x87`, 1 to 3 (`0x0029AB51`-`0x0029AB8F`, `0x0029ADF9`-`0x0029AE09`) |

The status cycle record at the row's `+0xF0`, stepped by `0x00272F80(record, 30, 0, 0, 0)` (`0x00272F60`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | mask | statuses to show: the member's status presence word `+0x44`, copied in each frame by `0x00297FE0` (`0x0029802A`) |
| `+0x04` | `u32` | counted | the mask at the last count: when the mask differs from it and either nothing was counted or the period has moved on, `0x00272F80` stores the mask here, counts again and sets `+0x08` to -1 (`0x0027302D`-`0x0027305C`) |
| `+0x08` | `i16` | shown | the period being shown, from the frame counter `0x0208F570` (`0x00273012`-`0x0027302A`, stored at `0x00273099`); -1 after a count (`0x00273058`), 0 when nothing counts (`0x00273067`) |
| `+0x0A` | `i16` | count | statuses counted (`0x00275E40`, stored at `0x00273051`); it sets each status's period, `max(36 - 6n, 12)` frames (`0x00272FC0`-`0x00273000`), and 0 shows nothing (`0x00273061`) |
| `+0x10` | `void*` | status | the status row shown, or 0: the n-th counted status of the mask in the order once the blank periods have passed (`0x002730A3`-`0x0027314B`), 0 during them and when nothing counts (`0x0027306B`); `0x00297FE0` shows its text `0x46B7` plus `+0x98` and its colour from `+0x25` bit `0x1` (`0x0029803B`-`0x002980B8`), and answers 1 when a mark appeared or went (`0x00298020`, `0x0029804C`) |

### The gil window

The gil window is the `0xF8`-byte widget at `0x0209C4C8` with procedure `0x002A1FB0`; the script verb `fs_foodwinopen` opens it through `0x002A1D40`, and `gillwinstart` and the shop's trade (`0x0056D4D9`) start its count through `0x002A1DC0`.

`GilWindow` (`0xF8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x002A1FB0` |
| `+0xC0` | `u32` | countFlags | bit `0x1` (with bit `0x2` tested as the pair 3): a gil count is running, set by `0x002A1DC0` (`0x002A1E47`-`0x002A1E60`), which also clears bits `0x3E` and so picks curve 0 in bits 2-5; the tick clears bits `0x3` when the count ends (`0x002A238A`) and passes bits `0x3C` to `0x00248F40` as the curve (`0x002A231F`-`0x002A2344`). `0x002A1DC0` refuses a new count (`0x002A1DE6`) and the idle test `0x002A2620` answers 0 (`0x002A262C`) while bits `0x3` are set |
| `+0xC4` | `i32` | countFrom | the gil shown when the count started: `0x002A1DC0` copies the shown amount `+0xEC` (`0x002A1E41`); the tick shows countFrom + countBy x t (`0x002A2352`-`0x002A2380`) and countFrom + countBy at the end (`0x002A2391`) |
| `+0xC8` | `i32` | countBy | the gil change being counted: `0x002A1DC0` stores the change `0x002524C0` allows, the request clamped so the total stays within 0-99,999,999 (`0x002A1E5A`); read by the tick (`0x002A2349`) |
| `+0xCC` | `u32` | countFrames | the count's length in frames: `0x002A1DC0` sets `0x15`, 21 frames (`0x002A1E72`); the tick passes it to `0x00248F40` (`0x002A2338`) |
| `+0xD0` | `u32` | countStart | the frame counter `0x0208F570` when the count started, stored by `0x002A1DC0` (`0x002A1E6C`); the tick passes the frames since then to `0x00248F40` (`0x002A2331`) |
| `+0xD4` | `u8[4]` | pad0D4 | read and written by no function; nothing fixes its width |
| `+0xD8` | `void*` | limitDialog | the message window state 3 opens with message `0x856` through `0x00241C90` (`0x002A2234`-`0x002A2296`); state 4 waits until it is 0 (`0x002A220E`). The command message 12 sets it to 0 (`0x002A21AB`) and state 4 clears it again (`0x002A2228`) |
| `+0xE0` | `void*` | layoutBlock | the layout block the window places itself from: the creation record's first qword (`0x002A257F`), or the menu layout block [`0x0209AC30`] + `0x90` when that is 0 (`0x002A25B3`-`0x002A25C1`); the opening and the tick resolve its `+0x20` (`0x0020E600`) and read entry `+0xE8`'s x, y, width and height (`0x002A207B`-`0x002A20CC`, `0x002A24FD`-`0x002A2527`) |
| `+0xE8` | `i16` | layoutEntry | the 20-byte entry of the layout block the window uses: from the creation record's `+0x08` (`0x002A258A`), 0 with the default block (`0x002A25CA`); read at `0x002A208A` and `0x002A2504` |
| `+0xEA` | `u16` | mode | from the creation record's `+0x0A` (`0x002A2575`; 3 from fs_foodwinopen's creator `0x002A1D40`). Mode 1 makes the tick show the party's gil, GameState_GetGil `0x00253690`, every tick (`0x002A21CA`-`0x002A21D9`); mode 3 picks the frame `0x00916408` over `0x00916430` (`0x002A20FB`); any other mode hides layout items 0 and 3 by clearing bit `0x1` of their `+0x08` (`0x002A211D`-`0x002A213A`) |
| `+0xEC` | `i32` | shown | the gil amount drawn: from the creation record's `+0x0C` (`0x002A256B`), the opening value `0x002A1D40` passes; mode 1 refreshes it each tick (`0x002A21D9`); a count moves it (`0x002A2380`, `0x002A2394`). The tick draws it as 8 digits in layout item 6 (`0x0029F6E0`, `0x002A23B7`, `0x002A23DC`); `0x002A1DC0` tests it plus the change against 99,999,999 and starts the count from it (`0x002A1DF3`, `0x002A1E3B`) |
| `+0xF0` | `i16` | pauseFrames | frames left after a count: state 2 sets 24 (`0x002A22B5`); state 1 plays sound `0x1A` (`0x00249C60`) and `0x0024A1A0`([`0x01E0CDCC`]) at 20 (`0x002A22C1`) and counts it down (`0x002A22E0`, `0x002A22E7`); state 4 sets it to 0 with the state and overflow bytes in one dword store of `0xFF0000` (`0x002A221E`) |
| `+0xF2` | `i8` | state | the count's state: 0 counting (set by `0x002A1DC0`, `0x002A1E50`), 2 count done (`0x002A1E2E` when the allowed change is 0, `0x002A239A` at the end), 1 pausing (`0x002A22AE`), 3 the limit message is due (`0x002A2313`), 4 waiting for it (`0x002A229D`; the command message 12 also sets 4, `0x002A21A4`), -1 idle (`0x002A2300`, `0x002A221E`, and the construct message's word store `0xFF`, `0x002A25A5`). The tick dispatches on it (`0x002A21DF`); the idle test `0x002A2620` answers 1 only for -1 (`0x002A2638`) |
| `+0xF3` | `u8` | overLimit | 1 when the shown gil plus the requested change passes 99,999,999, else 0: `0x002A1DC0` (`0x002A1DFF`-`0x002A1E1A`); after the pause the tick goes to state 3, the limit message, when it is set, and to idle otherwise (`0x002A22F5`). Set to 0 by the construct message (`0x002A25A5`) and by state 4 (`0x002A221E`) |
| `+0xF4` | `u8` | caption | from the creation record's `+0x10` (`0x002A2595`; 2 from `0x002A1D40`): non-zero hides layout item 14 and puts message `0x4B55` (for 1) or `0x4B56` (otherwise) in item 5 (`0x002A213E`-`0x002A217E`), and lets the tick slide the window back to its layout y (`0x002A24D4`); `0x002A1DC0` refuses a count while it is non-zero (`0x002A1DD9`) |
| `+0xF5` | `u8` | placedUnderMask | 1 once the window has been put under the conversation window's mask widget [`0x0209C610`]: set when the window opens with that widget present (`0x002A206F`) and by the tick's first placement under it (`0x002A243E`, `0x002A2457`); while it is 1 the tick slides the window to the mask's y less the window's height (`0x002A246A`-`0x002A24AB`) |
| `+0xF6` | `u8` | maskHold | set to 1 every tick the mask widget [`0x0209C610`] exists (`0x002A24B0`); once the mask is gone the tick counts it down (`0x002A24BC`-`0x002A24C9`) and slides the window back to its layout y only after it is 0 |
| `+0xF7` | `u8` | bottomAnchor | from the creation record's `+0x11` (`0x002A259F`; 0 from `0x002A1D40`): non-zero places the window at the screen height `0x1C0` less its height less `0x002C9430`(`0x81`) plus 12 when it opens (`0x002A209F`-`0x002A20F4`), and with `0x002C9430`(1) each tick while it is not running (`0x002A23EB`-`0x002A2426`) |

### The location panel

The location panel is the `0xF0`-byte widget at `0x0209C300` with procedure `0x0029C530` that `0x00297100` shows instead
of the list (The list and its rows above). On message 1 it decodes record `0x14` of the layout file at
`[0x0209AC30] + 8` into its `+0x50` (`0x002432B0`, `0x0029C589`-`0x0029C5B5`) and fills three nodes:

- node 3, the name of the field's region (`0x003778B0`): of the transition field when gate `0x5E` answers non-zero,
  of the current field otherwise (`0x0029C602`-`0x0029C64A`);
- node 4, the area name of the current field (`0x00377B60`, `0x0029C65A`-`0x0029C679`);
- node 5, the frame `0x002543D0` gives for the field's group (`0x0029C699`-`0x0029C6A6`).

It keeps a copy of the two text nodes' colour and rectangle, which nothing reads back.

`LocationPanel` (`0xF0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0029C530` |
| `+0xC0` | `u32` | regionTextColour | the colour (`+0x24`) of node 3, the text node that gets the region name, copied on message 1 (`0x0029C6C1`-`0x0029C6C9`); no instruction reads it back |
| `+0xC4` | `i16` | regionTextX | node 3's x (`+0x0C`), copied on message 1 (`0x0029C6CF`-`0x0029C6D3`); no instruction reads it back |
| `+0xC6` | `i16` | regionTextY | node 3's y (`+0x0E`), copied on message 1 (`0x0029C6DA`-`0x0029C6DE`); no instruction reads it back |
| `+0xC8` | `u16` | regionTextWidth | node 3's width (`+0x10`), copied on message 1 (`0x0029C6E5`-`0x0029C6E9`); no instruction reads it back |
| `+0xCA` | `u16` | regionTextHeight | node 3's height (`+0x12`), copied on message 1 (`0x0029C6F0`-`0x0029C6F4`); no instruction reads it back |
| `+0xCC` | `u8[4]` | pad0CC | accessed by no instruction of the procedure or of the cell's two readers; nothing fixes its width |
| `+0xD0` | `u32` | areaTextColour | the colour (`+0x24`) of node 4, the text node that gets the area name, copied on message 1 (`0x0029C6FB`-`0x0029C706`); no instruction reads it back |
| `+0xD4` | `i16` | areaTextX | node 4's x (`+0x0C`), copied on message 1 (`0x0029C70C`-`0x0029C710`); no instruction reads it back |
| `+0xD6` | `i16` | areaTextY | node 4's y (`+0x0E`), copied on message 1 (`0x0029C717`-`0x0029C71B`); no instruction reads it back |
| `+0xD8` | `u16` | areaTextWidth | node 4's width (`+0x10`), copied on message 1 (`0x0029C722`-`0x0029C726`); no instruction reads it back |
| `+0xDA` | `u16` | areaTextHeight | node 4's height (`+0x12`), copied on message 1 (`0x0029C72D`-`0x0029C734`); no instruction reads it back |
| `+0xDC` | `u8[4]` | pad0DC | accessed by no instruction of the procedure or of the cell's two readers; nothing fixes its width |
| `+0xE0` | `u16` | word0E0 | set to 0 at the end of message 1 (`0x0029C755`); no instruction reads it |
| `+0xE2` | `u8[4]` | pad0E2 | accessed by no instruction of the procedure or of the cell's two readers; nothing fixes its width |
| `+0xE6` | `u16` | runBits | bit `0x8` is set when the opening run starts (message 14, `0x0029C579`) and bit `0x4` when closing begins (message 15, `0x0029C569`); `0x00297100` clears bits 0-1 when it finds the panel already built (`0x00297132`-`0x00297137`). No instruction tests the word |
| `+0xE8` | `u8[8]` | pad0E8 | accessed by no instruction of the procedure or of the cell's two readers; nothing fixes its width |

## State

The target window's pair of counters is the two `0x58`-byte records `0x0209C240` (HP) and `0x0209C298` (MP). The
handle that matches a unit to it sits where a member's pair keeps its handle, at `+0xB0` from the pair
(`0x002962C0` returns `0x0209C240`).

`0x00296360(record, handle)`, from `0x002C0870`, first unregisters both records when a
handle is held (`0x0029636A`-`0x002963A0`); with a non-zero handle and a record whose `+0x04` is not 0 it stores the
handle and sets both records up again (`0x002963AA`-`0x00296436`). `0x00296260`, from `0x0028F327` and `0x0028F8E3`, zeroes
the `0xC0` bytes from `0x0209C240` (`0x0029626F`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209C288` | `void*` | 0 | the HP counter's context `+0x48`: the record `0x00296360` was given | `0x003F89C0`, which zeroes the record and stores its fourth argument (`0x003F89E5`, `0x003F89FB`), from `0x00296360` (`0x002963E2`); `0x00296360` (`0x0029642F`); `0x00296260`, 0 (`0x0029626F`) | `0x0029B7D0`, the HP callback, through the counter it is called with (`0x0029B7D7`) |
| `0x0209C2E0` | `void*` | 0 | the MP counter's context `+0x48`, the same record | `0x003F89C0` as above, from `0x00296360` (`0x00296402`); `0x00296360` (`0x00296436`); `0x00296260`, 0 (`0x0029626F`) | `0x0029B810`, the MP callback, the same way (`0x0029B814`) |
| `0x0209C2F0` | `u32` | 0 | the handle of the unit whose HP and MP the target window rolls, 0 for none | `0x00296360`: 0 (`0x002963A0`), the handle (`0x002963C8`); `0x00296260`, 0 (`0x0029626F`) | `0x00296360` (`0x0029636A`); through the address `0x002962C0` returns: `0x0028F1F0` (`0x0028F21D`), which starts the window's roll when the changed unit's handle matches, and `0x002C0400` (`0x002C0449`) |

No other instruction reaches these three. The two records' addresses are taken by `0x00296260`, `0x00296360` and
`0x002962C0` only.

### The rebuild's counts and lists

`0x0035BC50(arg)` rebuilds the party block `0x022C8060` from the four party members (`0x00320040`, `0x0035BDB0`-`0x0035BE69`).
It first clears the member count `0x022C8064` and the next six bytes with one 8-byte store (`0x0035BD6D`). A member is
listed when its type `+0x60` is not negative and its handle `+0x04` is not 0. The block is also cleared whole by
`0x0035BB70` (`0x348` bytes, `0x0035BB85`) and `0x0035C560` (`0x23C8` bytes, `0x0035C573`).

The rebuild also builds two lists with the list builder `0x0031EB20`
([Target selection](../Battle-Actions/target-selection.md)): code `0x1A` into `0x022C83F0` (count) and `0x022C83F8`
(entries), and code `0x14`, the living party-side units, into `0x022C8478` and `0x022C8480`, keeping only the units
`0x00273800` passes (`0x0035BFC0`-`0x0035BFFE`). It copies each list header's default entry `+0x44` into the word after
the count. `0x0031EB20` sets that entry to -1 on entry (`0x0031EB46`) and changes it only in its unit-slot walk for codes
`0xC`-`0x10` (`0x0031F402`), so for these two codes it stays -1.

With `arg` not 0, the rebuild opens the leader choice (request 3) by itself when all of these hold
(`0x0035BEC1`-`0x0035BF2F`): `0x022C8068` is not 0, the leader's record has flag bit `0x40`, some listed member has flag bits `0x2`,
2 and 6 clear, block bit `0x4` is clear, a listed member has flag bit `0x1`, and `0x02092730` is 0. A refused request clears the
two bits it set (`0x0035BF38`, `0x0035BF3F`). None of this runs when bit `0x8` of `0x022C83E8` is set and `0x00303EC0()`
answers non-zero; the rebuild then calls `0x002547D0(1)` instead (`0x0035BE98`-`0x0035BEBC`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C8066` | `u16` | 0 | the number of listed members whose flag bit `0x2` is clear (not types 7-25); a member with bit `0x2` instead puts its type in `0x022C8076` | `0x0035BC50`: 0 in the 8-byte store (`0x0035BD6D`), the count (`0x0035BE42`); `0x0035BB70`, `0x0035C560`, the block cleared | `0x0035BC50`, its own increment (`0x0035BE42`) |
| `0x022C8068` | `u32` | 0 | the number of listed members whose flag bit `0x40` is clear, bit `0x40` clear being one of the leader choice's tests for a row (`0x00299BD0`) | `0x0035BC50`: 0 in the 8-byte store (`0x0035BD6D`), the count (`0x0035BDEF`); `0x0035BB70`, `0x0035C560` | `0x0035BC50` (`0x0035BDEF`; `0x0035BEC7`, where 0 skips the leader choice) |
| `0x022C8070` | `u32` | 0 | the party leader's type, the byte at battle block `+0x5AA4` (`0x003271D0`), copied at each rebuild | `0x0035BC50` (`0x0035BD7C`); `0x0035BB70`, `0x0035C560` | `0x0035BC50` (`0x0035BE2A`, which finds the leader's record); `0x0035BAA0(type)` (`0x0035BAA6`), which does nothing for the type already stored and otherwise writes the new type to `+0x5AA4` (`0x00327850`) and rebuilds with `0x0035BC50(0)` |
| `0x022C83F4` | `i32` | 0 | list `0x1A`'s default entry, -1 after every rebuild | `0x0035BC50` (`0x0035BCDB`); `0x0035C560` | no instruction names it |
| `0x022C847C` | `i32` | 0 | list `0x14`'s default entry, -1 after every rebuild | `0x0035BC50` (`0x0035BF6E`); `0x0035C560` | no instruction names it |

No other instruction names these five. The block's address is also returned by `0x0035D320` (21 call sites) and
passed to `0x0035E5F0` by `0x0035D070`; the code at each call reads the block's `+0x0C`, `+0x14` and `+0x18` and the
member records, and `0x0035E5F0` writes from `+0x4A0` on.

## Modding notes

- A roll always takes 10 to 50 frames however large the change, in proportion to the change over the maximum.
- More statuses show faster: one shows for 30 frames, two for 24, three for 18, and four or more for 12 each.
- The leader can be changed only to a member who has a handle, is not KO and passes the status check of `0x002739D0`.
- Kind 3 rows (types 27-39, the Espers) have no MP display.

## Related

- [Battle menu](battle-menu.md) - the row parts and the target lists that drive pick mode.
- [HUD](hud.md) - the object that holds the list and steps the counters.
- [Party member status record](../Characters-And-Objects/party-member-status-record.md) - every field a row reads.
- [Menus](menus.md) - request 3, choosing the leader.
- [Controls](../Controls-And-Input/controls.md) - the button words.
- [Widgets](widgets.md) - focus, priorities and the input turn.
