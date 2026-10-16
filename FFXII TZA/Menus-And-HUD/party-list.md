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

`0029BE50` is the list widget, `B68`<sub>h</sub> bytes, built by `002964D0` when the party has a member (`0035BB60`) and kept at
`[0209BE80] + 10F78h` ([HUD](hud.md)). `0028FD70` builds it, and the widget `0029BC80` at `+10FC8`<sub>h</sub> beside it
(`00296AA0`). On a chocobo ride (`00303EC0`) it closes both, and while action policy bit 10 is set it closes the list
and shows the widget `0029C530` at `[0209C300]` instead (`00297100`). `00290E10` closes the list and `00296A70` the widget beside it;
`002970C0` closes `[0209C300]`. Each close first sets bit 16 of the widget's `+40`<sub>h</sub> when `002544B0` answers 1.

On message 1 the list reads its layout, layout record `15`<sub>h</sub>, takes the member count from `022C8064`, the leader's
index from `022C8074` (`0035BAE0`), and builds the header `0029B700` at `+B38`<sub>h</sub> (`0029BEAB`-`0029BF2A`).
`00296450` gives the y position of the first row from the header's layout.

### Building the rows

Each frame (message 2) the list checks the member count. When it changed it releases its rows and bars, clears the
four member cells (`0028F830`), and sets bit 6 of `+B4A`<sub>h</sub>; once they are gone it rebuilds through `0029BB40`
(`0029C124`, `0029C134`):

1. A member record with a type and a handle gets a row kind in `+B44h + i`: 2 for flag bit 1 (types 7-25), 3 for
   flag bit 2 (types 27-39), 1 otherwise.
2. A waiting kind builds the `160`<sub>h</sub>-byte row `0029A0A0` at `+240h + i x 160h`, with the list at its `+120`<sub>h</sub>
   (`0029BBD3`).
3. Once the list has finished opening, it builds one `D8`<sub>h</sub>-byte action bar `00299090` per member at
   `+7C0h + i x D8h` and sets `+B4A`<sub>h</sub> bit 4 (`0029C374`-`0029C38C`).

The member records are the `C0`<sub>h</sub>-byte records at `022C8080 + i x C0h` (`0035BB20`), described on
[Party member status record](../Characters-And-Objects/party-member-status-record.md).

### What a row shows

A row draws the parts in [Battle menu](battle-menu.md) (name, HP, HP gauge, maximum HP, MP and MP bars) and also:

- the name from `00296600(type)` when the type has one, else the record's name (`00297F60`): types 0-6 are
  "Vaan", "Ashe", "Fran", "Balthier", "Basch", "Penelo" and "Reks" (`009161F0`), 7-16 the guests from "Amalia" to
  "Reddas" (`00916200`), 27-39 the Espers from "Belias" to "Zodiark" (`00916218`);
- one of three HP frames by digit count: `00297710` takes the larger of HP and the cap `+28`<sub>h</sub>, below 100, below
  1000 or 1000 and above;
- one of three MP frames by the bar count `+87`<sub>h</sub>, 1 to 3, or none for 0 (`00297880`); rows of kind 3 draw no MP;
- the status mark and name (`00297FE0`), and the summon gauge on the summoner's row (`0029B1C0`), below.

### Row effects

A row's flag word `+D8`<sub>h</sub> (`+318h + i x 160h` in the list) drives its effects:

| Bit | Effect |
|---:|---|
| `0` | the row takes part in a pick mode; the list's draw hook `+B28`<sub>h</sub> may then draw the hand cursor on it (`0029A19C`, `002426F0`) |
| `1` | the row is refused in a pick mode; its alpha is halved |
| `2` | the cursor is on the row; its alpha pulses, `00296FB0(32, 128, 0)` (`0029A25C`), and a pointer is drawn (`0029A1EA`) |
| `3` | the row is closing |
| `4` | a status pulse: alpha follows the track `009162B0` over `+110`<sub>h</sub> (`0029A223`), 16 a frame (`00299890`) |
| `5`, `6` | an HP or MP flash, below |
| `7` | nodes 0-2 fade out over 8 frames, and back in once it clears (`00298130`) |

`00296FB0(amplitude, base, phase)` is `base + amplitude x sin((frame x rate - phase) x pi / 15)`, with the rate 1, or
one over the speed steps while the game runs at speed (`00229DF0`, `00229E70`). A row whose shown status has flag
bit 1 at `+25`<sub>h</sub> is also drawn at half alpha (`0029A267`).

### Flashes

`0028FBE0(popup)`, run for every battle number the popup queue `003BBD00` adds (`003BBE6C`), flashes the member's row
by the popup's kind byte `+0D`<sub>h</sub>:

| Kind | Flash |
|---|---|
| `1`, `5` | HP: bit 5, `00297040(list, handle, 0)` |
| `3`, `7` | MP: bit 6, `00297040(list, handle, 1)`, not on a row of kind 3 |
| `2`, `6` | status pulse: bit 4, `00296E90` |

`002994E0` draws the HP flash as a highlight sprite round the union of the HP digit nodes (`00271DB0`), as wide as
the digit frame plus 24 for each node past the first (`002998D0`), scaled by the track `009162D8` over `+114`<sub>h</sub>;
`002996E0` does the same round the MP frame over `+116`<sub>h</sub>. Each advances 8 a frame and ends at 256
(`0029A467`-`0029A4AD`).

### Rolling numbers

HP and MP roll through counters, `58`<sub>h</sub>-byte records, two per member at `0209BF40 + i x C0h` and two for the target
window at `0209C240`. `00297C10(record)` finds the pair holding the record's handle or takes a free one, sets it up
with `003F89C0` and the callbacks `0029B7D0` (HP) and `0029B810` (MP), and registers both in the HUD's counter list
`+80`<sub>h</sub> (`003F8A50`). `002962D0` unregisters pairs whose handle no longer resolves (`002732E0`, `003F8A30`), and
`00296360(record, on)` does the same for the target window's pair (from `002C0870`).

`0028F1F0(handle, old, new, mp)` starts a roll: it finds the member's pair (`00296280`), or the target window's pair
when its handle matches, and sends the HP or MP counter message 1 (`003F8980`). The HP callback passes the maximum
`+24`<sub>h</sub>, the MP callback the capacity `+30`<sub>h</sub> times the bar count `+87`<sub>h</sub> (`0029B7D0`, `0029B810`).

### How a roll moves

`002973E0(counter, from, max, to)` starts it:

1. A counter at rest starts from the old value (`002726C0`); a running one starts from the value it shows
   (`00271960`, `00272730`).
2. The path keeps from and to in 1/16 units and three points between, at `94`<sub>h</sub>, `D4`<sub>h</sub> and `F3`<sub>h</sub> of 256 of the way.
3. Its length is the change times 100 over the maximum, between 10 and 50 frames (`002727C0`, step `400`<sub>h</sub> / frames);
   a change of 1 or less puts the counter at rest at once.

Each HUD frame group 2 steps every registered counter (`003F8B40`): `00272710` advances the step and `00271960` gives
the shown value. The five points are from, the three between, and to, one quarter apart:

- over the first three quarters the value follows a cubic spline through them (`00270260`): the first segment uses
  the basis at `009157B0`, the next two the Catmull-Rom basis at `009157F0` with four points from `00276220`, both
  halved by `00915870`;
- over the last quarter it moves in a straight line from the third point between to the target.

The row shows the counter's value at `+50`<sub>h</sub> while it runs, and the record's value at rest (`0029A4CE`, `0029A5FD`).

### The status mark

`00297FE0(row, record)` copies the status presence word `+44`<sub>h</sub> into the row's status record at `+F0`<sub>h</sub> and steps it
with `00272F80(+F0h, 30, 0)`. With n statuses to show, each shows for `max(36 - 6n, 12)` frames in display order,
after a blank of `ceil(30 / that)` periods (`00272F80`). The mark shows the status's sprite and its name, text
`46B7`<sub>h</sub> plus the status, such as "KO" (`46B7`<sub>h</sub>) or "Stone" (`46B8`<sub>h</sub>), in colour 5 when the status has flag bit 0
at `+25`<sub>h</sub> and 4 otherwise.

The display orders are four tables of pointers to copies of the 32 status rows, class `1A`<sub>h</sub>, that `00273BA0` builds
at `022C8B08 + 1500h`, `+1600`<sub>h</sub>, `+1700`<sub>h</sub> and `+1800`<sub>h</sub> (`0035D490`):

- `00273410(order)` returns a table and `00273380(mask, order)` the first status of the mask in it;
- a status counts in order 0, 1, 2 or 3 only when its byte `+21`<sub>h</sub>, `+23`<sub>h</sub>, `+22`<sub>h</sub> or `+24`<sub>h</sub> is not -1
  (`00275E40`), and in order 2 also when `003178C0` passes it for the unit;
- `00273160(out, flags, unit)` returns the first status of a unit in order 1 and its flag bits, for the overhead
  gauge `002C6F70`.

The HP number's colour comes from the statuses present, in order 0 (`00271FB0`, `00297D62`): colour `B5`<sub>h</sub> when one
has bit 4 at `+25`<sub>h</sub> and `B6`<sub>h</sub> for bit 3, pulsing by `128 + 32 x sin(frame x pi / 30)` (`00271EF0`); a status with
bit 1 halves it.

### The summon gauge

While an Esper is out (`003135C0`), the row of the member whose type equals the summon block's `+2C`<sub>h</sub> (`003200A0`,
`[02EBF190] + 5AD4h`) shows the summon node and `0029B1C0(row, left, total)` draws it as five segments from the
summon timer `+5AD8`<sub>h</sub> and its length `+5ADC`<sub>h</sub> (`0029A39D`-`0029A407`). Lit segments pulse with
`sin(frame x pi / 60)`; the segment being used up fades by the time left in it, the first never below `20`<sub>h</sub>.

`0029B490(row, on)` steps a six-frame mark through the frames `4`, `16`<sub>h</sub>, `17`<sub>h</sub>, `18`<sub>h</sub>, `19`<sub>h</sub> and `5` while the
record's flag bit 17 is set and back while it is clear (`0029A5D9`). `0029AFE0` pulses node `B8`<sub>h</sub>'s
brightness between `80`<sub>h</sub> and `FF`<sub>h</sub> while flag bit 7 is set.

### The action bar

The bar `00299090` keeps its state in the member's `20`<sub>h</sub>-byte cell (`0028F830`), cleared when the member's type
changes. It shows while the record's flag bit 9 is set or its action id `+5C`<sub>h</sub> or issued command `+5E`<sub>h</sub> is below
`4000`<sub>h</sub>, and flag bit 6 is clear; otherwise it closes once its count `+CA`<sub>h</sub> passes 3. Each frame
`002986E0(bar, record)`:

1. shows the action's name (class `14`<sub>h</sub>, `0029FB50`) once flag bit 13 is set and the id changed;
2. fills to `+3C`<sub>h</sub> / `+40`<sub>h</sub> x 100 percent, or 100 with flag bit 12;
3. on reaching 100 flashes for 8 frames with `sin(t x pi / 15)` (state 1), then fades out by 16 a frame (state 2);
4. blends the bar between the colours `7A`<sub>h</sub>-`7D`<sub>h</sub> and `7E`<sub>h</sub>-`80`<sub>h</sub> (`002DD7E0`) by the percentage
   (`002752E0`), and cycles a four-key colour track (`00274870`, `00271E50`) while `00226BA0` answers 0.

`00297290` fades the bar's frame in and out by 16 a step (tracks on the stack, `00271AB0`).

### Choosing a new leader

Request 3 ([Menus](menus.md)) reaches `00290500(1)`, which runs `00296BE0(list, 1)`:

1. A list already in pick mode 2 refuses; otherwise the mode `+B49`<sub>h</sub> becomes 1 with the handler `00297640`.
2. `00299BD0` offers each row whose member has a handle, is not KO (flag bit 0), has flag bit 6 clear and passes
   `002739D0`; the others are refused.
3. The cursor starts on the leader, or the next offered row (`00296D96`, `00296DA7`).
4. The header closes, the overlay `0029C9D0` opens over the rows, and the list takes the focus (`002470D0`).

`00296BE0(list, 0)` undoes it: the header reopens, the focus is given up, the overlay closes and every row loses
bits 0, 1, 2 and 7.

### The buttons

In either mode the list's input turn runs `0029B870` and keeps the answer at `+B43`<sub>h</sub> (`00296570`). The first turn
only plays sound 4 (`0029BFB5`). Each press is offered to the handler `+B20`<sub>h</sub>, which may refuse it (`0029B790`):

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
| 2, confirm | sound `15`<sub>h</sub> on an offered row; sound 5 and a refusal on a refused one |
| 3, cancel | allowed with sound 3 when the current leader can still lead (`00299B90`, `0035BC30`); else sound 5 |
| `6` | sound 5, refused |
| `4`, `5`, `7`, `8` | refused |

An allowed confirm makes the row's member the leader (`0035BAA0` with its type), then `0035C100(1)`, `0035DA80`,
`003C93E0(0)`, `0035C080` and `0035C050(0)` (`0029C008`-`0029C033`); an allowed cancel closes the mode through
`0035D8D0` (`0029C04C`-`0029C058`).

### Picking a party member as a target

The battle menu turns the list into its cursor for a target list of party members through `002904D0(page, start)`,
which runs `00297170`:

1. In mode 1 it refuses. Otherwise `+B50`<sub>h</sub> points at the target page, `0029AEF0` offers the rows whose member is on
   the page and refuses the others and those whose entry has flag bit 1, the greyed bit, and `0029AE50` puts the
   cursor on entry `start`.
2. The list takes the focus with mode 2 (`002470D0`).
3. `002904D0(0, 0)` ends it: the frame at `+180`<sub>h</sub> closes, the focus is given up and the marks are cleared.

The menu works the list through small calls:

| Call | Does |
|---|---|
| `00290590(page)` | refreshes the offered rows (`00296A10`) |
| `00290490` | the page entry under the cursor, or -1 (`00296580`) |
| `00290520`, `002905B0` | read and set the last answer `+B43`<sub>h</sub> (`00296570`) |
| `00290470` | 3 when there is no list |
| `002969F0(list, handler, context)`, `002969E0(list, hook)` | set the handler `+B20`<sub>h</sub> with its context `+B30`<sub>h</sub>, and the draw hook `+B28`<sub>h</sub> |
| `00296ED0(list, on)` | sets bit 8 of `+B4A`<sub>h</sub>, which opens the frame `0029C770` round the rows; off clears the row marks |
| `00296E00(list, handle)` | writes 3 into the member's cell `+1A`<sub>h</sub> |

The frame and the leader-mode overlay `0029C9D0` take their box from `002974E0`: the first row of kind 1, stretched
over the height of all rows.

`0029B120(list, row)` raises one row and its bar above the others (priorities 2 and 3 against 4 and 5), for the
moving pointer `0029C850`.

## Layouts

The counter record, `58`<sub>h</sub> bytes, two per member at `0209BF40`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | from | start value x 16 |
| `04`<sub>h</sub> | `i32` | to | target value x 16 |
| `08`<sub>h</sub> | `i32[3]` | points | the three points between |
| `14`<sub>h</sub> | `i16` | t | progress, 0 to `400`<sub>h</sub> |
| `16`<sub>h</sub> | `i16` | step | `400`<sub>h</sub> / length in frames |
| `26`<sub>h</sub> | `u16` | flags | bit 0 at rest, bit 1 registered |
| `28`<sub>h</sub> | `CounterRecord*` | next | in the HUD's list |
| `30`<sub>h</sub> | `CounterRecord*` | prev | |
| `38`<sub>h</sub> | `fn*` | callback | messages 0 to 6 |
| `48`<sub>h</sub> | `PartyMemberStatusRecord*` | record | the member |
| `50`<sub>h</sub> | `i32` | shown | the value drawn |

The status cycle record at the row's `+F0`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | mask | statuses to show |
| `04`<sub>h</sub> | `u32` | counted | the mask at the last count |
| `08`<sub>h</sub> | `i16` | shown | the period being shown |
| `0A`<sub>h</sub> | `i16` | count | statuses counted (`00275E40`) |
| `10`<sub>h</sub> | `void*` | status | the status row shown, or 0 |

## Modding notes

- A roll always takes 10 to 50 frames however large the change, in proportion to the change over the maximum.
- More statuses show faster: six or more get 12 frames each.
- The leader can be changed only to a member who has a handle, is not KO and passes the status check of `002739D0`.
- Kind 3 rows (types 27-39, the Espers) have no MP display.

## Related

- [Battle menu](battle-menu.md) - the row parts and the target lists that drive pick mode.
- [HUD](hud.md) - the object that holds the list and steps the counters.
- [Party member status record](../Characters-And-Objects/party-member-status-record.md) - every field a row reads.
- [Menus](menus.md) - request 3, choosing the leader.
- [Controls](../Controls-And-Input/controls.md) - the button words.
- [Widgets](widgets.md) - focus, priorities and the input turn.
</content>
</invoke>
