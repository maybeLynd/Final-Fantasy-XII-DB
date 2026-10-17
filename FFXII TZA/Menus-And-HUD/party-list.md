---
title: "Party list: the member rows on the HUD, the rolling HP and MP numbers, the action bar, the status mark, choosing a new leader and picking a member as a target"
kind: "system"
category: "Menus and HUD"
addresses: "0029BE50, 0029A0A0, 00299090, 002986E0, 00297C10, 002973E0, 00271960, 00272F80, 00296BE0, 00297170, 0029B870, 00297640"
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

`0029BE50` is the list widget, `0xB68` bytes, built by `002964D0` when the party has a member (`0035BB60`) and kept at
`[0209BE80] + 0x10F78` ([HUD](hud.md)). `0028FD70` builds it, and the widget `0029BC80` at `+0x10FC8` beside it
(`00296AA0`). On a chocobo ride (`00303EC0`) it closes both, and while action policy bit 10 is set it closes the list
and shows the widget `0029C530` at `[0209C300]` instead (`00297100`). `00290E10` closes the list and `00296A70` the widget beside it;
`002970C0` closes `[0209C300]`. Each close first sets bit 16 of the widget's `+0x40` when `002544B0` answers 1.

`0028FD70` also calls `003CA1E0` (`0028FD99`), which, when the object at `[02B47758]` exists, clears bit 1 and sets
bit 0 of its `+0xA90`.

On message 1 the list reads its layout, layout record `0x15`, takes the member count from `022C8064`, the leader's
index from `022C8074` (`0035BAE0`), and builds the header `0029B700` at `+0xB38` (`0029BEAB`-`0029BF2A`).
`00296450` gives the y position of the first row from the header's layout.

### Building the rows

Each frame (message 2) the list checks the member count. When it changed it releases its rows and bars, clears the
four member cells (`0028F830`), and sets bit 6 of `+0xB4A`; once they are gone it rebuilds through `0029BB40`
(`0029C124`, `0029C134`):

1. A member record with a type and a handle gets a row kind in `+0xB44 + i`: 2 for flag bit 1 (types 7-25), 3 for
   flag bit 2 (types 27-39), 1 otherwise.
2. A waiting kind builds the `0x160`-byte row `0029A0A0` at `+0x240 + i x 0x160`, with the list at its `+0x120`
   (`0029BBD3`).
3. Once the list has finished opening, it builds one `0xD8`-byte action bar `00299090` per member at
   `+0x7C0 + i x 0xD8` and sets `+0xB4A` bit 4 (`0029C374`-`0029C38C`).

The member records are the `0xC0`-byte records at `022C8080 + i x 0xC0` (`0035BB20`), described on
[Party member status record](../Characters-And-Objects/party-member-status-record.md).
`0035BB00(i)` returns record i's actor handle, the dword at `022C8084 + i x 0xC0`.

`0035BB70`, run by the field set-up `00253A30` (`00253A3E`) and the teardown `003C5E50` (`003C5EA7`), clears the
whole `0x348`-byte block from `022C8060`, keeps only the bits `0xFFFC02EC` of the mode word `022C83E8`, runs
`002419B0(1)`, closes the leader-choice window in `022CA428` and the window `0035E070` keeps in `022CA430`
(`00244F00`), and ends in `002A1E90`, which closes the widget in `[0209C4C8]`.

`0035D570(unit)` returns 1 when the unit's handle is one of the `[022C83F0]` words at `022C83F8`; the overhead
gauge `002C6F70` gives a unit an entry when `00273320(unit)` is not negative or `0035D570(unit)` is 1.

### What a row shows

A row draws the parts in [Battle menu](battle-menu.md) (name, HP, HP gauge, maximum HP, MP and MP bars) and also:

- the name from `00296600(type)` when the type has one, else the record's name (`00297F60`): types 0-6 are
  "Vaan", "Ashe", "Fran", "Balthier", "Basch", "Penelo" and "Reks" (`009161F0`), 7-16 the guests from "Amalia" to
  "Reddas" (`00916200`), 27-39 the Espers from "Belias" to "Zodiark" (`00916218`);
- one of three HP frames by digit count: `00297710` takes the larger of HP and the cap `+0x28`, below 100, below
  1000 or 1000 and above;
- one of three MP frames by the bar count `+0x87`, 1 to 3, or none for 0 (`00297880`); rows of kind 3 draw no MP;
- the status mark and name (`00297FE0`), and the summon gauge on the summoner's row (`0029B1C0`), below.

### Row effects

A row's flag word `+0xD8` (`+0x318 + i x 0x160` in the list) drives its effects:

| Bit | Effect |
|---:|---|
| `0` | the row takes part in a pick mode; the list's draw hook `+0xB28` may then draw the hand cursor on it (`0029A19C`, `002426F0`) |
| `1` | the row is refused in a pick mode; its widget's brightness `+0x5A` becomes `+0x5A >> 1` (`0029A247`-`0029A24B`) |
| `2` | the cursor is on the row; its brightness `+0x5A` pulses, `00296FB0(32, 128, 0)` (`0029A25C`-`0029A264`), and a pointer is drawn (`0029A1EA`) |
| `3` | the row is closing |
| `4` | a status pulse: brightness `+0x5A` and alpha `+0x58` follow the track `009162B0` over `+0x110` (`0029A223`-`0029A23D`), 16 a frame (`00299890`) |
| `5`, `6` | an HP or MP flash, below |
| `7` | nodes 0-2 fade out over 8 frames, and back in once it clears (`00298130`) |

`00296FB0(amplitude, base, phase)` is `base + amplitude x sin((frame x rate - phase) x pi / 15)`, with the rate 1, or
one over the speed steps while the game runs at speed (`00229DF0`, `00229E70`). A row whose shown status has flag
bit 1 at `+0x25` is also drawn at half brightness (`+0x5A`, `0029A267`-`0029A282`).

### Flashes

`0028FBE0(popup)`, run for every battle number the popup queue `003BBD00` adds (`003BBE6C`), flashes the member's row
by the popup's kind byte `+0x0D`:

| Kind | Flash |
|---|---|
| `1`, `5` | HP: bit 5, `00297040(list, handle, 0)` |
| `3`, `7` | MP: bit 6, `00297040(list, handle, 1)`, not on a row of kind 3 |
| `2`, `6` | status pulse: bit 4, `00296E90` |

`002994E0` draws the HP flash as a highlight sprite round the union of the HP digit nodes (`00271DB0`), as wide as
the digit frame plus 24 for each node past the first (`002998D0`). For the draw it sets the widget's
`+0x58 = (+0x58 x a) >> 7` and `+0x5A = (+0x5A x b) >> 7`, `a` and `b` the bytes `+6` and `+7` of the three-key track
`009162D8` at time `+0x114`, and restores both afterwards (`0029957C`-`002995BF`).

`002996E0` does the same round the MP frame with the time `+0x116`. Each time steps `t += 8` a frame; above 255 it
goes back to 0 and the flash bit clears (`0029A467`-`0029A4AD`).

`00271AB0(out, keys, n, t)` evaluates a track of `n` 12-byte keys (`s16` `+0`, `s16` `+2`, `u16` time `+4`, bytes
`+6`, `+7`, `s16` ease `+8`, `s16` `+10`). It takes the first pair with `time[k] <= t < time[k+1]`, else the last
pair, and with `d = t - time[k]` and `span = time[k+1] - time[k]` sets `f = d x 256 / span`, or
`int(256 sin(pi/2 x d / span))` for ease 1 in key `k+1`, or `256 - int(256 sin(pi/2 x (span - d) / span))` for ease 2.
Each field is `v[k] + (v[k+1] - v[k]) x f / 256`, truncated (`00271AB0`-`00271CA9`).

### Rolling numbers

HP and MP roll through counters, `0x58`-byte records, two per member at `0209BF40 + i x 0xC0` and two for the target
window at `0209C240`. `00297C10(record)` finds the pair holding the record's handle or takes a free one, sets it up
with `003F89C0` and the callbacks `0029B7D0` (HP) and `0029B810` (MP), and registers both in the HUD's counter list
`+0x80` (`003F8A50`). `002962D0` unregisters pairs whose handle no longer resolves (`002732E0`, `003F8A30`), and
`00296360(record, on)` does the same for the target window's pair (from `002C0870`).

`003F8A30(list, node)` first moves the list head on to the node's next (`+0x28`) when the node is the head, then
runs `003F8BF0(node)` (`003F8A42`): it calls the node's callback `+0x38` with 5, links its previous `+0x30` and next
`+0x28` neighbours to each other, clears both links and the word `+0x26`, and calls the callback again with 6.

`0028F1F0(handle, old, new, mp)`, called by the HP write `00300530` (`003006E7`,
[HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)) and the MP write `00300CE0` (`00300DD3`,
[MP](../Status-Effects-And-KO/mp.md)), starts a roll: it finds the member's pair (`00296280`), or the target window's pair
when its handle matches, and sends the HP or MP counter message 1 (`003F8980`). The HP callback passes the maximum
`+0x24`, the MP callback the capacity `+0x30` times the bar count `+0x87` (`0029B7D0`, `0029B810`).

### How a roll moves

`002973E0(counter, from, max, to)` starts it:

1. A counter at rest starts from the old value (`002726C0`); a running one starts from the value it shows
   (`00271960`, `00272730`).
2. The path keeps from and to in 1/16 units and three points between, at `0x94`, `0xD4` and `0xF3` of 256 of the way.
3. Its length is the change times 100 over the maximum, between 10 and 50 frames (`002727C0`, step `0x400` / frames);
   a change of 1 or less puts the counter at rest at once.

Each HUD frame group 2 steps every registered counter (`003F8B40`): `00272710` advances the step and `00271960` gives
the shown value. The five points are from, the three between, and to, one quarter apart:

- with the step below `0x400`, `u = step / 256`, `i = int(u)`, `t = u - i` and the points `P0`-`P4` in that order,
  over the first three quarters the value follows a spline through them (`00271960`, `00270260`). Segment 0 is
  `0.5 x ((P0 - 2 P1 + P2) t^2 + (4 P1 - 3 P0 - P2) t)`, 0 at `t = 0` and `P1 - P0` at `t = 1` (the basis at
  `009157B0`; its constant term multiplies the point matrix's first row, which `00270260` makes zero at `0027034F`);
- segments 1 and 2 are the Catmull-Rom `0.5 x ((3 P[i] - P[i-1] - 3 P[i+1] + P[i+2]) t^3 + (2 P[i-1] - 5 P[i] +
  4 P[i+1] - P[i+2]) t^2 + (P[i+1] - P[i-1]) t + 2 P[i])` (the basis at `009157F0`, points from `00276220`), the
  0.5 being the vector at `00915870`;
- over the last quarter it moves in a straight line, `P3 + (P4 - P3) x (u - 3)`, from the third point between to the
  target. The shown value is `int(x) >> 4` (`00271960`).

The row shows the counter's value at `+0x50` while it runs, and the record's value at rest (`0029A4CE`, `0029A5FD`).

### The status mark

`00297FE0(row, record)` copies the status presence word `+0x44` into the row's status record at `+0xF0` and steps it
with `00272F80(+0xF0, 30, 0)`. With n statuses to show, each shows for `max(36 - 6n, 12)` frames in display order,
after a blank of `ceil(30 / that)` periods (`00272F80`). The mark shows the status's sprite and its name, text
`0x46B7` plus the status, such as "KO" (`0x46B7`) or "Stone" (`0x46B8`), in colour 5 when the status has flag bit 0
at `+0x25` and 4 otherwise.

The display orders are four tables of pointers to copies of the 32 status rows, class `0x1A`, that `00273BA0` builds
at `022C8B08 + 0x1500`, `+0x1600`, `+0x1700` and `+0x1800` (`0035D490`):

- `00273410(order)` returns a table and `00273380(mask, order)` the first status of the mask in it;
- a status counts in order 0, 1, 2 or 3 only when its byte `+0x21`, `+0x23`, `+0x22` or `+0x24` is not -1
  (`00275E40`), and in order 2 also when `003178C0` passes it for the unit;
- `00273160(out, flags, unit)` returns the first status of a unit in order 1 and its flag bits, for the overhead
  gauge `002C6F70`.

`00273BA0` builds each order as a list of 4-byte entries (`00273C63`-`00273DB8`), and the Party Menu's member rows
(`00284030`) and the Status pane (`002C573E`) make the same list for one unit's statuses:

1. The member rows and the Status pane first fill n entries with `0xFEFE` (`002D0280(list, n)`).
2. `002D02C0(list, n, mask, order)` writes, for each status of the mask below n, its number, its byte for the order
   (`+0x20`-`+0x24` of its class `0x1A` record) and bit 0 of its `+0x25`, and answers how many have a byte other than
   `0xFF`.
3. `002D03B0(list, n)` sorts them by that byte, highest first (`00249CE0` with the comparator `002D0270`).

`002D02A0(entry, mask)` answers whether an entry is a real status with a byte and set in a mask. The member row shows
at most 11 entries and skips status `0x1D` (`00284058`-`00284070`).

The Status pane `002C59D0` keeps 32 such entries at `+0xC8` and its mask at `+0x148`:

- `002C5810(pane, dir)` moves the pane's cursor `+0x14D` to the next entry that passes `002D02A0`: dir 0 and 1
  step back and forward, 2 and 3 by the list's column count (`+0xEC`), wrapping round the 32 entries. It
  answers 1 when the cursor moved. `002C5EC0(pane, dir)` answers whether such a move finds an entry without
  wrapping.
- `002C5900(pane, row, ..., i)` is the row painter the pane installs (`002C5A7F`). For an empty entry it hides
  both of the row's elements; otherwise it gives the first the status's sprite cell and the second the text at
  `+0x18` of the status's class `0x1A` record (`002B58B0`), in colour 4 when the entry's third byte is set and
  5 otherwise (`002DD7E0`).
- `002C5660()` returns the widest text at `+0x10` of those records (`002B3050`) among the statuses that the
  nine party records hold (`00282DF0`: `+0x60` not negative, the mask `+0x44`).

The HP number's colour comes from the statuses present, in order 0 (`00271FB0`, `00297D62`): colour `0xB5` when one
has bit 4 at `+0x25` and `0xB6` for bit 3, pulsing by `128 + 32 x sin(frame x pi / 30)` (`00271EF0`); a status with
bit 1 at `+0x25` halves each channel, `c x 0x40 >> 7` in place of `c x 0x80 >> 7` (`00297D67`-`00297DAE`).

### The summon gauge

While an Esper is out (`003135C0`), the row of the member whose type equals the summon block's `+0x2C` (`003200A0`,
`[02EBF190] + 0x5AD4`) shows the summon node and `0029B1C0(row, left, total)` draws it as five segments from the
summon timer `+0x5AD8` and its length `+0x5ADC` (`0029A39D`-`0029A407`). Lit segments pulse with
`sin(frame x pi / 60)`; the segment being used up fades by the time left in it, the first never below `0x20`.

`0029B490(row, on)` steps a six-frame mark through the frames `4`, `0x16`, `0x17`, `0x18`, `0x19` and `5` while the
record's flag bit 17 is set and back while it is clear (`0029A5D9`). `0029AFE0` pulses node `0xB8`'s
brightness between `0x80` and `0xFF` while flag bit 7 is set.

### The action bar

The bar `00299090` keeps its state in the member's `0x20`-byte cell (`0028F830`), cleared when the member's type
changes. It shows while the record's flag bit 9 is set or its action id `+0x5C` or issued command `+0x5E` is below
`0x4000`, and flag bit 6 is clear; otherwise it closes once its count `+0xCA` passes 3. Each frame
`002986E0(bar, record)`:

1. shows the action's name (class `0x14`, `0029FB50`) once flag bit 13 is set and the id changed;
2. fills to `pct = +0x3C x 100 / +0x40` percent, a maximum of 0 counting as 100 (`00298BD0`-`00298BD5`), or 100
   with flag bit 12;
3. on reaching 100 flashes for 8 frames with `sin(t x pi / 15)` (state 1), then fades out by 16 a frame (state 2);
4. blends two colour pairs from `002DD7E0`, each channel `c0 + (c1 - c0) x f / 256` (`002752E0`), and cycles a
   four-key colour track (`00274870`, `00271E50`) while `00226BA0` answers 0:
   - filling (state 0): `f = pct x 256 / 100`, colour `0x7A` to `0x7B` and `0x7E` to `0x7F` (`00298F9B`, `00298FB0`);
   - flashing (state 1): `f = 128 + int(128 sin((frame - start) x pi / 15))`, `start` the frame stored at cell `+0x0C`, `0x7B` to `0x7C` and `0x7F` to `0x80`
     (`00298E0A`, `00298E23`);
   - fading (state 2): `f` the fade count, which steps by 16 to 256, `0x7C` to `0x7D` and `0x80` to `0x7E`
     (`00298C4C`-`00298CC1`).

`00297290` fades the bar's frame in and out by 16 a step (tracks on the stack, `00271AB0`).

### Choosing a new leader

Request 3 ([Menus](menus.md)) reaches `00290500(1)`, which runs `00296BE0(list, 1)`:

1. A list already in pick mode 2 refuses; otherwise the mode `+0xB49` becomes 1 with the handler `00297640`.
2. `00299BD0` offers each row whose member has a handle, is not KO (flag bit 0), has flag bit 6 clear and passes
   `002739D0`; the others are refused.
3. The cursor starts on the leader, or the next offered row (`00296D96`, `00296DA7`).
4. The header closes, the overlay `0029C9D0` opens over the rows, and the list takes the focus (`002470D0`).

`00296BE0(list, 0)` undoes it: the header reopens, the focus is given up, the overlay closes and every row loses
bits 0, 1, 2 and 7.

### The buttons

In either mode the list's input turn runs `0029B870` and keeps the answer at `+0xB43` (`00296570`). The first turn
only plays sound 4 (`0029BFB5`). Each press is offered to the handler `+0xB20`, which may refuse it (`0029B790`):

| Press | Answer |
|---|---|
| cancel (`01E0C2A4`) | `3` |
| Square | `8` |
| Left or Right | `6` |
| confirm (`01E0C2A0`) | `2` |
| L1, R1 | `4`, `5` |
| Up, Down, a wheel notch | moves to the next offered row, 1; at an end, 7 |

Up and Down wrap on a new press and stop at the ends on a repeat (`002975B0`); the wheel counts as a repeat
(`001E0A10`, `001E0E30`).

### The leader handler

`00297640(list, answer, member, row)` decides for mode 1:

| Answer | Result |
|---|---|
| 1, moved | the target window shows the member (`0029B440`) and sound 1 plays |
| 2, confirm | sound `0x15` on an offered row; sound 5 and a refusal on a refused one |
| 3, cancel | allowed with sound 3 when the current leader can still lead (`00299B90`, `0035BC30`); else sound 5 |
| `6` | sound 5, refused |
| `4`, `5`, `7`, `8` | refused |

An allowed confirm makes the row's member the leader (`0035BAA0` with its type), then `0035C100(1)`, `0035DA80`,
`003C93E0(0)`, `0035C080` and `0035C050(0)` (`0029C008`-`0029C033`); an allowed cancel closes the mode through
`0035D8D0` (`0029C04C`-`0029C058`).

### Picking a party member as a target

The battle menu turns the list into its cursor for a target list of party members through `002904D0(page, start)`,
which runs `00297170`:

1. In mode 1 it refuses. Otherwise `+0xB50` points at the target page, `0029AEF0` offers the rows whose member is on
   the page and refuses the others and those whose entry has flag bit 1, the greyed bit, and `0029AE50` puts the
   cursor on entry `start`.
2. The list takes the focus with mode 2 (`002470D0`).
3. `002904D0(0, 0)` ends it: the frame at `+0x180` closes, the focus is given up and the marks are cleared.

The menu works the list through small calls:

| Call | Does |
|---|---|
| `00290590(page)` | refreshes the offered rows (`00296A10`) |
| `00290490` | the page entry under the cursor, or -1 (`00296580`) |
| `00290520`, `002905B0` | read and set the last answer `+0xB43` (`00296570`) |
| `00290470` | 3 when there is no list |
| `002969F0(list, handler, context)`, `002969E0(list, hook)` | set the handler `+0xB20` with its context `+0xB30`, and the draw hook `+0xB28` |
| `00296ED0(list, on)` | sets bit 8 of `+0xB4A`, which opens the frame `0029C770` round the rows; off clears the row marks |
| `00296E00(list, handle)` | writes 3 into the member's cell `+0x1A` |

The frame and the leader-mode overlay `0029C9D0` take their box from `002974E0`: the first row of kind 1, stretched
over the height of all rows.

`0029B120(list, row)` raises one row and its bar above the others (priorities 2 and 3 against 4 and 5), for the
moving pointer `0029C850`.

## Layouts

The counter record, `0x58` bytes, two per member at `0209BF40`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | from | start value x 16 |
| `+0x04` | `i32` | to | target value x 16 |
| `+0x08` | `i32[3]` | points | the three points between |
| `+0x14` | `i16` | t | progress, 0 to `0x400` |
| `+0x16` | `i16` | step | `0x400` / length in frames |
| `+0x26` | `u16` | flags | bit 0 at rest, bit 1 registered |
| `+0x28` | `CounterRecord*` | next | in the HUD's list |
| `+0x30` | `CounterRecord*` | prev | |
| `+0x38` | `fn*` | callback | messages 0 to 6 |
| `+0x48` | `PartyMemberStatusRecord*` | record | the member |
| `+0x50` | `i32` | shown | the value drawn |

The status cycle record at the row's `+0xF0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | mask | statuses to show |
| `+0x04` | `u32` | counted | the mask at the last count |
| `+0x08` | `i16` | shown | the period being shown |
| `+0x0A` | `i16` | count | statuses counted (`00275E40`) |
| `+0x10` | `void*` | status | the status row shown, or 0 |

## Modding notes

- A roll always takes 10 to 50 frames however large the change, in proportion to the change over the maximum.
- More statuses show faster: one shows for 30 frames, two for 24, three for 18, and four or more for 12 each.
- The leader can be changed only to a member who has a handle, is not KO and passes the status check of `002739D0`.
- Kind 3 rows (types 27-39, the Espers) have no MP display.

## Related

- [Battle menu](battle-menu.md) - the row parts and the target lists that drive pick mode.
- [HUD](hud.md) - the object that holds the list and steps the counters.
- [Party member status record](../Characters-And-Objects/party-member-status-record.md) - every field a row reads.
- [Menus](menus.md) - request 3, choosing the leader.
- [Controls](../Controls-And-Input/controls.md) - the button words.
- [Widgets](widgets.md) - focus, priorities and the input turn.
