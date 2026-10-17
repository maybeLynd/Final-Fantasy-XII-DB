---
title: "Script gauges: the counter and timer gauge an event opens, the verbs that set it, and the counter it shares with the boss gauge"
kind: "system"
category: "Menus and HUD"
addresses: "00408300, 00406E80, 00407F90, 004073B0, 00408140, 00407720, 00407290, 004076B0"
---

## What the player sees

Some events show a gauge on the field screen: a count of things gathered or a timer counting up or down.
The event can colour it, give it warning thresholds and move it toward a new value over a few frames. It
hides with the rest of the HUD and comes back when the HUD returns. The boss gauge at the top of a boss fight
is built from the same counter.

## How it works

### Opening the gauge

The verb `initgauge` (`0034DC70`) passes its kind to `003E9020`, which closes a gauge already open
(`00408200`), stores the default colours at `02B5D098`-`02B5D0A4` and calls `00408300(type)`:

| `initgauge` kind | type | child |
|---|---|---|
| 1 | 1 | timer, procedure `004079A0`, layout `0051EDC0(1)` |
| 2 | 2 | timer, procedure `004079A0`, layout `0051EDC0(2)` |
| 3 | 4 | none |
| other | 0 | counter, procedure `00407590`, layout `0051EDC0(0)` |

`00408300` creates the gauge window `00406E80` (`E8`<sub>h</sub> bytes) only while `02B62D80` is null. On creation the
window stores itself in `02B62D80`, builds the child (`278`<sub>h</sub> or `1F8`<sub>h</sub> bytes) at `+C0`<sub>h</sub> and loads the layout's
pictures into the list at `+D8`<sub>h</sub> (`0024A440`). For type 4 it builds no child and reads the layout record
through a null pointer (`00407018`-`0040701F`).

`00407F90(counter)` gives a new counter its defaults: flags `+D8`<sub>h</sub> = `10`<sub>h</sub>, maximum `+E0`<sub>h</sub> = 100, value 0,
the colours `805A5A20`<sub>h</sub>, `80276742`<sub>h</sub>, `80206266`<sub>h</sub> and `800A2A7E`<sub>h</sub> at `+F8`<sub>h</sub>-`+104`<sub>h</sub>, and the widgets it
draws with at `+C8`<sub>h</sub> and `+D0`<sub>h</sub>, which depend on the mode byte `+C0`<sub>h</sub>.

### The verbs

Each verb reaches the child of `[02B62D80]` through a one-jump stub, and does nothing while the window's
`+C8`<sub>h</sub> bit 1 is set:

| Verb | Body | Effect |
|---|---|---|
| `setgaugecountermax`, `setgaugetimermax`, `setgaugeracemax` | `00347F20` → `00408830` → `004073B0` | sets the maximum `+E0`<sub>h</sub> (times 60 for a timer) and the thresholds to a quarter, a half and three quarters of it, `+F0`<sub>h</sub> to the maximum |
| `setgaugecounter` | `0034EA90` → `004085B0` | sets the value of a counter (mode 0) and redraws it |
| `setgaugetimer` | `0034ED90` → `004088D0` | sets the value of a timer (mode 1) in seconds, stored times 60 |
| `changegaugecounterbyratio` | `003502C0` → `004084C0` → `00407290` | moves the value toward the target over a ramp |
| `setgaugecountercondition`, `setgaugetimercondition`, `setgaugeracecondition` | `003514F0` → `00408560` → `00407300` | sets the three thresholds |
| `setgaugecountertype`, `setgaugetimertype`, `setgaugeracetype` | `00354190` → `00408A20` | sets the type `+DC`<sub>h</sub> |
| `setgaugecolor` | `00357270` → `00408780` | sets the four colours |
| `stopgaugetimer` | `003521F0` → `004083B0` | sets the window's `+C8`<sub>h</sub> bit 2 |
| `resetgaugetimer` | `00351C80` → `004083E0` | see below |

### Value, ramps and thresholds

`00408140(counter, v)` stops a running ramp, stores `v` at `+E4`<sub>h</sub> and redraws by mode: 0 through `00407450`,
1 through `00407720`, 3 through `00225580` on the value widget, with `v` less the maximum once it passes the
maximum. A ramp lives at `+114`<sub>h</sub>-`+128`<sub>h</sub> and is stepped once per frame by `004076B0`:

```python
elapsed = elapsed + 1
value = start + delta * elapsed / length      while elapsed < length
value = start + delta, length = 0             at the end; 004076B0 returns -1 when length is 0
```

- `00407290(counter, target)` starts a ramp of `|target - value| x [+10Ch] / [+110h]` frames, at least 1,
  and only when `+110`<sub>h</sub> is not 0.
- `00407240(counter, target)` starts a ramp of `+108`<sub>h</sub> frames, or 1 when that is 0; its only caller is
  the boss gauge's bar (`00406552`).
- The counter child steps its ramp only while the window's `+C8`<sub>h</sub> bits 2 and 3 are both clear
  (`00407631`-`00407639`).

`00407300(counter, a, b, c)` sets `a = a x 60`, `b = b x 60` and `c = c x 60` when the mode byte `+C0`<sub>h</sub> is 1,
a timer (`0040730C`-`0040731C`), and stores them at `+EA`<sub>h</sub>,
`+EC`<sub>h</sub> and `+EE`<sub>h</sub>: in that order for types 1 and 3, in reverse order for types 2 and 4, and not at all for
type 0. A `-1` keeps a threshold. `00408A20(type)` stores the type and sets bit 25 of the value widget's
`+20`<sub>h</sub> for types 2 and 4, clearing it for 1 and 3. `00408780(c0, c1, c2, c3)` stores the colours, `-1`
keeping one.

### The timer text

`00407720(counter)` writes the timer's value, in frames at 60 per second, into the text at `+134`<sub>h</sub>
(`002B4090`) and hands it to the label widget:

| Flags | Format id | Shown as |
|---|---|---|
| `+130`<sub>h</sub> bit 0 clear | `4B3C`<sub>h</sub> | hours (value / 216,000), minutes, seconds and hundredths; above 9 hours it shows 99, 59, 59, 99 |
| `+130`<sub>h</sub> bit 0 set, `+D8`<sub>h</sub> bit 1 clear | `4B3D`<sub>h</sub> | seconds `value / 60` and the hundredths below; when the seconds exceed 999 it shows 999 and 99 (`00407774`-`004077B5`) |
| `+130`<sub>h</sub> bit 0 set, `+D8`<sub>h</sub> bit 1 set | `4B3E`<sub>h</sub> | the same |

The hundredths are `(value mod 60) x 100 / 60`.

### `resetgaugetimer`

`004083E0` takes the child of `[02B62D80]` when its mode is 1 and then acts only when that is null: it reads
the type byte from the absolute address `DC`<sub>h</sub> (`0040841E`) and would store 0 or the maximum at `E4`<sub>h</sub>. With a
timer open the verb therefore changes nothing, and with none open it reads unmapped memory. The shipped US
scripts never call it (`us_calls` 0 in the [verb table](../Scripts-And-Script-Commands/verb-table.md)).

`00407150(window, on)`, reached through `004088A0`, `004088B0` and `00408190`, is the working reset: on a
change of the window's `+C8`<sub>h</sub> bit 1 it ends a counter's ramp at its target, or sets a timer to its maximum
for type 1 and to 0 for the others.

### Pause, hide and restore

- The byte `0215F1B3` is a mask of pause reasons ([Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).
  Whenever it is written, `00404D70` (non-zero) or `00404DC0` (zero) sets or clears bit 3 of the gauge
  window's `+C8`<sub>h</sub> and bit 7 of the boss gauge's `+C8`<sub>h</sub> (`002E0D67`, `002E15A3`, `002E24B7`-`002E24F8`),
  skipping a gauge whose `+C8`<sub>h</sub> bit 1 (script) or bit 5 (boss) is set.
- The HUD switch hides the message windows through `0035D0E0` and shows them through `0035D1B0`
  ([HUD](hud.md)). `0035D0E0` also runs `004082D0`, which starts the gauge child's closing run with the
  message at `01E0C0F8`.
- `0035D1B0` runs `00408AA0`, which restarts its opening run with message 14
  (`01E0C0E0`) when the child is hidden (`+D8`<sub>h</sub> bit 2 set, bit 3 clear). Both set the run speed `+B8`<sub>h</sub>
  to `1 / 00229E70()` when `00229DF0` is non-zero and `00229EA0` returns 2.

### Placing the gauge

`00407B70` reads the positions of two layout children of the window (`00394690`), the second named by its third
argument. When `003C5FB0` (the
minimap status test of [Map screens](map-screens.md)) returns 0 it takes the second, calls `002E04E0(6)` and
moves every widget under the root `[0208EA28]` whose `+44`<sub>h</sub> bits 19 and 20 are `100000`<sub>h</sub> by the difference,
from its base `+54`<sub>h</sub>/`+56`<sub>h</sub> (`00407C90` walks the tree through `+18`<sub>h</sub> and `+20`<sub>h</sub>). The window's widget
`+C8`<sub>h</sub> gets the chosen position at `+98`<sub>h</sub>/`+9A`<sub>h</sub>.

## Layouts

`GaugeCounter` (`1F8`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0C0`<sub>h</sub> | `u8` | mode | 0 counter, 1 timer, 3 drawn by the value widget (`00408140`) |
| `0C8`<sub>h</sub> | `void*` | frame | the frame widget (`00407F90`) |
| `0D0`<sub>h</sub> | `void*` | value | the value widget |
| `0D8`<sub>h</sub> | `u32` | flags | `10`<sub>h</sub> at creation; bit 1 picks format `4B3E`<sub>h</sub>; bit 5 set by `00407150` |
| `0DC`<sub>h</sub> | `u8` | type | 0 to 4 (`00408A20`); 2 and 4 reverse the thresholds |
| `0E0`<sub>h</sub> | `i32` | max | default 100; frames for a timer |
| `0E4`<sub>h</sub> | `i32` | current | the value shown |
| `0EA`<sub>h</sub> | `i16` | cond1 | first threshold |
| `0EC`<sub>h</sub> | `i16` | cond2 | second threshold |
| `0EE`<sub>h</sub> | `i16` | cond3 | third threshold |
| `0F0`<sub>h</sub> | `i16` | limit | the maximum again (`004073B0`) |
| `0F8`<sub>h</sub> | `u32[4]` | colour | four colours (`00408780`) |
| `108`<sub>h</sub> | `i16` | frames | ramp length for `00407240` |
| `10C`<sub>h</sub> | `i32` | ratio_num | ramp frames per unit, numerator (`00407290`) |
| `110`<sub>h</sub> | `i32` | ratio_den | ramp denominator; 0 disables `00407290` |
| `114`<sub>h</sub> | `i32` | elapsed | ramp frames done (`004076B0`) |
| `118`<sub>h</sub> | `i32` | length | ramp length; 0 when no ramp runs |
| `11C`<sub>h</sub> | `i32` | start | ramp start value |
| `120`<sub>h</sub> | `i32` | delta | ramp distance |
| `124`<sub>h</sub> | `i32` | now | ramp result |
| `130`<sub>h</sub> | `u32` | style | bit 0 picks the seconds-only timer format (`00407720`) |
| `134`<sub>h</sub> | `char[64] text` | the formatted timer (00407720) |  |

## Modding notes

- `initgauge 3` leaves the gauge without a child and reads a null layout record; use kinds 0 to 2. No shipped
  script passes 3: the 268 calls in the `us` scripts push the literal kinds 0 (85), 1 (2) and 2 (181)
  (`Database/Tools/analysis-kit/gfz-scripts/script_verb_census.py --verbs 1ABh`, a complete run).
- `resetgaugetimer` does nothing to an open timer; set the timer with `setgaugetimer` instead.
- A timer is limited to 9 hours 59 minutes in the long format and 999.99 seconds in the short one.
- The thresholds default to the quarters of the maximum each time the maximum is set, so set the conditions
  after the maximum.

## Related

- [Battle menu](battle-menu.md): the boss gauge, whose bars use the same counter.
- [HUD](hud.md): the HUD switch and the gauge hide bit.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the gauge verbs.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the mask that pauses the gauges.
- [Widgets](widgets.md): the opening and closing runs.
