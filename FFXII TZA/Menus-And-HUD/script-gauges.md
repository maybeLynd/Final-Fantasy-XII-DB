---
title: "Script gauges: the counter and timer gauge an event opens, the verbs that set it, and the counter it shares with the boss gauge"
kind: "system"
category: "Menus and HUD"
addresses: "0x00408300, 0x00406E80, 0x00407F90, 0x004073B0, 0x00408140, 0x00407720, 0x00407290, 0x004076B0"
---

## What the player sees

Some events show a gauge on the field screen: a count of things gathered or a timer counting up or down.
The event can colour it, give it warning thresholds and move it toward a new value over a few frames. It
hides with the rest of the HUD and comes back when the HUD returns. The boss gauge at the top of a boss fight
is built from the same counter.

## How it works

### Opening the gauge

The verb `initgauge` (`0x0034DC70`) passes its kind to `0x003E9020`, which closes a gauge already open
(`0x00408200`), stores the default colours at `0x02B5D098`-`0x02B5D0A4` and calls `0x00408300(type)`:

| `initgauge` kind | type | child |
|---|---|---|
| 1 | 1 | timer, procedure `0x004079A0`, layout `0x0051EDC0(1)` |
| 2 | 2 | timer, procedure `0x004079A0`, layout `0x0051EDC0(2)` |
| 3 | 4 | no child |
| other | 0 | counter, procedure `0x00407590`, layout `0x0051EDC0(0)` |

`0x00408300` creates the gauge window `0x00406E80` (0xE8 bytes) only while `0x02B62D80` is null. On creation the
window stores itself in `0x02B62D80`, builds the child (0x278 or 0x1F8 bytes) at `+0xC0` and loads the layout's
pictures into the list at `+0xD8` (`0x0024A440`). For type 4 it builds no child and reads the layout record
through a null pointer (`0x00407018`-`0x0040701F`).

`0x00407F90(counter)` gives a new counter its defaults: flags `+0xD8` = `0x10`, maximum `+0xE0` = 100, value 0,
the colours `0x805A5A20`, `0x80276742`, `0x80206266` and `0x800A2A7E` at `+0xF8`-`+0x104`, and the widgets it
draws with at `+0xC8` and `+0xD0`, which depend on the mode byte `+0xC0`.

### The verbs

Each verb's handler reaches the child of `[0x02B62D80]` through a chain of jump stubs (the table gives the handler
and the body), and every verb that changes the gauge does nothing while the window's `+0xC8` bit `0x2` is set:

| Verb | Body | Effect |
|---|---|---|
| `setgaugecountermax`, `setgaugetimermax`, `setgaugeracemax` | `0x00347F20` → `0x00408830` → `0x004073B0` | sets the maximum `+0xE0` (times 60 for a timer) and the thresholds to a quarter, a half and three quarters of it, `+0xF0` to the maximum |
| `setgaugecounter` | `0x0034EA90` → `0x004085B0` | sets the value of a counter (mode 0) and redraws it |
| `setgaugetimer` | `0x0034ED90` → `0x004088D0` | sets the value of a timer (mode 1) in seconds, stored times 60 |
| `changegaugecounterbyratio` | `0x003502C0` → `0x004084C0` → `0x00407290` | moves the value toward the target over a ramp |
| `changegaugecounterbyframe` | `0x0034FDE0` → `0x003E8EC0` → `0x00408450` | moves the value toward the target over a ramp of `+0x108` frames, 1 when that is 0 (`0x004084A1`); it sets the ramp fields itself, as `0x00407240` does. A new counter has `+0x108` = 0 (`0x00407FC8`), so unless `setgaugechangeframe` sets it the value reaches the target on the counter's next step (`0x004076C6`) |
| `setgaugechangeratio` | `0x0034F7C0` → `0x003E8F40` → `0x00408520` | stores the ramp rate: argument 1 at `+0x10C`, argument 2 at `+0x110` (`0x00408549`, `0x0040854F`) |
| `setgaugechangeframe` | `0x0034F360` → `0x003E8F30` → `0x004084F0` | stores twice the argument as the word `+0x108` (`0x0034F36C`, `0x00408516`) |
| `setgaugecountercondition`, `setgaugetimercondition`, `setgaugeracecondition` | `0x003514F0` → `0x00408560` → `0x00407300` | sets the three thresholds |
| `setgaugecountertype`, `setgaugetimertype`, `setgaugeracetype` | `0x00354190` → `0x003E8F70` → `0x00408A20` | sets the type `+0xDC`; `0x003E8F70` keeps 1 to 4 and turns any other value into 0 (`0x003E8F84`); `0x00408A20` sets bit `0x2000000` of the `+0xD0` widget's `+0x20` for types 2 and 4 (`0x00408A79`) and clears it for 1 and 3 (`0x00408A88`) |
| `setgaugecolor` | `0x00357270` → `0x00408780` | sets the four colours |
| `setgaugehidestatus` | `0x0034C150` → `0x002E1BB0` → `0x004087E0` | sets the child's `+0x40` bit `0x100000` for 2 and clears it for 0 and 1 (`0x002E1BB0` turns any other value into 0), see Pause, hide and restore |
| `startgaugetimer` | `0x00351F10` → `0x00408AD0` | clears the window's `+0xC8` bit `0x4`, so the timer counts again |
| `stopgaugetimer` | `0x003521F0` → `0x004083B0` | sets the window's `+0xC8` bit `0x4` |
| `resetgaugetimer` | `0x00351C80` → `0x004083E0` | see below |
| `gaugepadding0` | `0x00352660` → `0x00408860` | sets the child's `+0xD8` bit `0x2` from bit `0x1` of the argument; with it set and `+0x130` bit `0x1` set, the timer text `0x00407720` writes format `0x4B3E` instead of `0x4B3D` |
| `getgaugecounter` | `0x00353D70` → `0x00408250` | returns a counter's value `+0xE4` (mode 0), -1 with no counter |
| `getgaugetimer` | `0x003539E0` → `0x00408280` | returns a timer's value `+0xE4` (mode 1) in seconds, rounded up for a non-zero argument and down for 0, -1 with no timer |

### Value, ramps and thresholds

`0x00408140(counter, v)` stops a running ramp, stores `v` at `+0xE4` and redraws by mode: 0 through `0x00407450`,
1 through `0x00407720`, 3 through `0x00225580` on the value widget, with `v` less the maximum once it passes the
maximum. A ramp lives at `+0x114`-`+0x128` and is stepped once per frame by `0x004076B0`:

```python
elapsed = elapsed + 1
value = start + delta * elapsed / length      while elapsed < length
value = start + delta, length = 0             at the end; 0x004076B0 returns -1 when length is 0
```

- `0x00407290(counter, target)` starts a ramp of `|target - value| x [+0x10C] / [+0x110]` frames, at least 1,
  and only when `+0x110` is not 0.
- `0x00407240(counter, target)` starts a ramp of `+0x108` frames, or 1 when that is 0; its only caller is
  the boss gauge's bar (`0x00406552`). `changegaugecounterbyframe` (`0x00408450`) starts the same ramp with its own
  copy of these stores.
- The counter child steps its ramp only while the window's `+0xC8` bits `0x4` and `0x8` are both clear
  (`0x00407631`-`0x00407639`).

`0x00407300(counter, a, b, c)` sets `a = a x 60`, `b = b x 60` and `c = c x 60` when the mode byte `+0xC0` is 1,
a timer (`0x0040730C`-`0x0040731C`), and stores them at `+0xEA`,
`+0xEC` and `+0xEE`: in that order for types 1 and 3, in reverse order for types 2 and 4, and not at all for
type 0. A `-1` keeps a threshold. `0x00408A20(type)` stores the type and sets bit `0x2000000` of the value widget's
`+0x20` for types 2 and 4, clearing it for 1 and 3. `0x00408780(c0, c1, c2, c3)` stores the colours, `-1`
keeping one.

### The timer text

`0x00407720(counter)` writes the timer's value, in frames at 60 per second, into the text at `+0x134`
(`0x002B4090`) and hands it to the label widget:

| Flags | Format id | Shown as |
|---|---|---|
| `+0x130` bit `0x1` clear | `0x4B3C` | hours (value / 216,000), minutes, seconds and hundredths; above 9 hours it shows 99, 59, 59, 99 |
| `+0x130` bit `0x1` set, `+0xD8` bit `0x2` clear | `0x4B3D` | seconds `value / 60` and the hundredths below; when the seconds exceed 999 it shows 999 and 99 (`0x00407774`-`0x004077B5`) |
| `+0x130` bit `0x1` set, `+0xD8` bit `0x2` set | `0x4B3E` | the same |

The hundredths are `(value mod 60) x 100 / 60`.

### `resetgaugetimer`

`0x004083E0` takes the child of `[0x02B62D80]` when its mode is 1 and then acts only when that is null: it reads
the type byte from the absolute address `0xDC` (`0x0040841E`) and would store 0 or the maximum at `0xE4`. With a
timer open the verb therefore changes nothing, and with no timer open it reads unmapped memory. The shipped US
scripts never call it (`us_calls` 0 in the [verb table](../Scripts-And-Script-Commands/verb-table.md)).

`0x00407150(window, on)`, reached through `0x004088A0`, `0x004088B0` and `0x00408190`, is the working reset: on a
change of the window's `+0xC8` bit `0x2` it ends a counter's ramp at its target, or sets a timer to its maximum
for type 1 and to 0 for the others.

### Pause, hide and restore

- The byte `0x0215F1B3` is a mask of pause reasons ([Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).
  Whenever it is written, `0x00404D70` (non-zero) or `0x00404DC0` (zero) sets or clears bit `0x8` of the gauge
  window's `+0xC8` and bit `0x80` of the boss gauge's `+0xC8` (`0x002E0D67`, `0x002E15A3`, `0x002E24B7`-`0x002E24F8`),
  skipping a gauge whose `+0xC8` bit `0x2` (script) or bit `0x20` (boss) is set.
- The HUD switch hides the message windows through `0x0035D0E0` and shows them through `0x0035D1B0`
  ([HUD](hud.md)). `0x0035D0E0` also runs `0x004082D0`, which starts the gauge child's closing run with the
  message at `0x01E0C0F8` unless the child's `+0x40` bit `0x100000` is set (`0x004082E8`): `setgaugehidestatus(2)` sets
  that bit and 0 or 1 clears it, so with 2 the gauge stays on screen while the HUD is hidden.
- `0x0035D1B0` runs `0x00408AA0`, which restarts its opening run with message 14
  (`0x01E0C0E0`) when the script has the gauge shown (`+0xD8` bit `0x4` set and bit `0x8` clear, the state
  `setgaugeshowstatus(1)` leaves, `0x00408399`-`0x0040839F`; `0x004082D0` closes the child without touching these bits, so
  after the HUD hide such a child is closed). Both set the run speed `+0xB8` to `1 / 0x00229E70()` when `0x00229DF0` is
  non-zero and `0x00229EA0` returns 2.

### Placing the gauge

`0x00407B70` reads the positions of two layout children of the window (`0x00394690`), the second named by its third
argument. When `0x003C5FB0` (the
minimap status test of [Map screens](map-screens.md)) returns 0 it takes the second, calls `0x002E04E0(6)` and
moves every widget under the root `[0x0208EA28]` whose `+0x44` bits `0x80000` and `0x100000` are `0x100000` by the difference,
from its base `+0x54`/`+0x56` (`0x00407C90` walks the tree through `+0x18` and `+0x20`). The window's widget
`+0xC8` gets the chosen position at `+0x98`/`+0x9A`.

### The challenges

[script-gauges-challenges.tsv](script-gauges-challenges.tsv) has 13 rows, one for each challenge listed below that the `us`
scripts hold: what the player does, where, from when, the limits the script passes, the reward and what a failure does.
The census reads the 1,114 `us` listings that decode (`evt_t0020.ebp` has no `EBP2` header and no listing).
`initgauge` is called 268 times in 99 of them: 55 fields of The Great Crystal, 14 of Bhujerba, 12 of Barheim Passage,
8 of the Dreadnought Leviathan, 8 of Giza Plains, the scene `sav_c0280` and the developer event `evt_t0083`.

Counters the player fills: the rumour of Basch in Bhujerba rises with every listener and falls by itself; the
Shadestone in Giza Plains charges at the dark crystals until the Sunstone is made. Barheim Passage's power is a counter
the player keeps up: gates cost 30, Battery Mimics drain it, and at 30 or less the passage goes dark.

Timers: Zalera must fall within 300 seconds, the Leviathan's alarm stays off for 60, and the Great Crystal's devices
hold their barriers open for 72 to 288 seconds by room. The Demon Wall's two fights show a race marker
(`setgaugeraceiconshowstatus(4, 1)`) as the wall walks down the hall.

Challenges without a gauge: slipping past the guards of the Royal Palace, the spot-the-difference game of the Nalbina
Stockade (which no talk in its script opens), fishing with Ruksel on the Nebra, the Hunt Club's trophy contest ([Quests](../Story-Events-And-Hunts/quests.md),
quest 71), the miner's stash in the Henne Mines and the chops Vaan earns in Archades by carrying the townsfolk's
tales to one another. Trial Mode has its own rows on [Trial Mode
scripts](../Story-Events-And-Hunts/trial-mode-scripts.md).

| Column | Meaning |
|---|---|
| `challenge` | the challenge in game terms |
| `place` | the fields, by zone name |
| `scripts` | the script, actor, function and lines |
| `starts_when` | the counter, flag, item or talk that opens it |
| `rules` | what the player does and what counts |
| `limits` | the time, count or track the script sets |
| `reward` | the items or gil given, with [`scene-rewards.tsv`](../Story-Events-And-Hunts/scene-rewards.tsv) |
| `fail` | what happens on failure |
| `gauge` | the gauge verbs it uses |

## Layouts

`GaugeCounter` (`0x1F8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C0` | `u8` | mode | 0 counter, 1 timer, 3 drawn by the value widget (`0x00408140`) |
| `+0x0C8` | `void*` | frame | the frame widget (`0x00407F90`) |
| `+0x0D0` | `void*` | value | the value widget |
| `+0x0D8` | `u32` | flags | `0x10` at creation; bit `0x2` picks format `0x4B3E`; bit `0x20` set by `0x00407150` |
| `+0x0DC` | `u8` | type | 0 to 4 (`0x00408A20`); 2 and 4 reverse the thresholds |
| `+0x0E0` | `i32` | max | default 100; frames for a timer |
| `+0x0E4` | `i32` | current | the value shown |
| `+0x0EA` | `i16` | cond1 | first threshold |
| `+0x0EC` | `i16` | cond2 | second threshold |
| `+0x0EE` | `i16` | cond3 | third threshold |
| `+0x0F0` | `i16` | limit | the maximum again (`0x004073B0`) |
| `+0x0F8` | `u32[4]` | colour | four colours (`0x00408780`) |
| `+0x108` | `i16` | frames | ramp length for `0x00407240` and changegaugecounterbyframe; 0 from `0x00407F90` (`0x00407FC8`); setgaugechangeframe and the boss gauge (`0x0040654B`) write it |
| `+0x10C` | `i32` | ratio_num | ramp frames per unit, numerator (`0x00407290`); setgaugechangeratio argument 1 |
| `+0x110` | `i32` | ratio_den | ramp denominator; 0 disables `0x00407290`; setgaugechangeratio argument 2 |
| `+0x114` | `i32` | elapsed | ramp frames done (`0x004076B0`) |
| `+0x118` | `i32` | length | ramp length; 0 when no ramp runs |
| `+0x11C` | `i32` | start | ramp start value |
| `+0x120` | `i32` | delta | ramp distance |
| `+0x124` | `i32` | now | ramp result |
| `+0x130` | `u32` | style | bit `0x1` picks the seconds-only timer format (`0x00407720`) |
| `+0x134` | `char[64]` | text | the formatted timer (`0x00407720`) |

### The gauge window

The gauge window is the `0xE8`-byte widget at `0x02B62D80` with procedure `0x00406E80` that `0x00408300` creates.

`ScriptGaugeWindow` (`0xE8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00406E80` |
| `+0xC0` | `void*` | gauge | the gauge child the construct message builds for the creation argument (`0x00406FD3`-`0x00407107`): type 0 the `0x278`-byte counter with procedure `0x00407590`, types 1 and 2 the `0x1F8`-byte gauge with procedure `0x004079A0`, any other type no child (0 from `0x00406FB8`). Every gauge verb reaches the child through it (`0x00408190`-`0x00408AAC`: `0x004081A8`, `0x00408210`, `0x0040825C`, `0x0040828C`, `0x004082DC`, `0x00408379`, `0x004083EC`, `0x0040846D`, `0x004084DC`, `0x0040850A`, `0x0040853D`, `0x0040857D`, `0x004085BE`, `0x00408661`, `0x00408719`, `0x0040879A`, `0x004087F3`, `0x0040884C`, `0x00408873`, `0x004088DF`, `0x00408981`, `0x00408A3D`, `0x00408AAC`), and so do `0x00407150` (`0x0040717C`) and the tick (`0x00406F2D`) |
| `+0xC8` | `u32` | flags | bit `0x1`: tested by the tick, which with it set runs `0x00408200` when the child is not open or is in run state 1 or 4 (`0x00406F20`-`0x00406F67`); no instruction sets it. Bit `0x2`: the gauges are off, set and cleared by `0x00407150` (`0x0040715D`-`0x0040718C`); every verb does nothing while it is set (`0x00408372`, `0x00408410`, `0x0040845F`, `0x004084CE`, `0x004084FC`, `0x0040852F`, `0x0040856F`, `0x004085E5`, `0x00408688`, `0x00408740`, `0x0040878C`, `0x004087EC`, `0x0040883E`, `0x0040886C`, `0x00408903`, `0x004089A8`, `0x00408A2F`) and so do the pause and timer stubs. Bit `0x4`: the timer is stopped, set by stopgaugetimer `0x004083B0` (`0x004083C7`) and by `0x00407F90` for its mode-2 child (`0x00408069`), cleared by `0x00408AD0` (`0x00408AE7`). Bit `0x8`: the script pause mask, set by `0x00404D70` (`0x00404D87`) and cleared by `0x00404DC0` (`0x00404DDA`). The counter steps its ramp only while bits `0x4` and `0x8` are clear (`0x0040762B`, `0x00407A35`). 0 at construction (`0x00406FCD`) |
| `+0xCC` | `u8[4]` | pad0CC | read and written by no function; nothing fixes its width |
| `+0xD0` | `void*` | layoutRecord | the gauge's layout record `0x0051EDC0`(0), (1) or (2) by type (`0x00407018`), 0 for the other types (`0x00406FBF`), after which the construct message reads `+0x28` through it (`0x0040701F`); its byte `+0x24` is the picture count and `+0x28` the picture list (`0x00407027`-`0x00407035`) |
| `+0xD8` | `void*` | pictures | the array of `+0xE0` picture handles the construct message allocates (`0x00393590`, `0x00407050`) and fills, one load (`0x0024A440`) for each list entry of type 1 and 0 for the others (`0x00407070`-`0x004070AD`); message 18 releases each (`0x0024A680`) and frees the array (`0x00406EBD`-`0x00406F14`); 0 at construction (`0x00406FC6`) |
| `+0xE0` | `u8` | pictureCount | the number of pictures, byte `+0x24` of the layout record (`0x00407035`); bounds the load and release loops (`0x00407057`, `0x004070B1`, `0x00406ECF`, `0x00406EF7`) |

## State

The gauge verbs keep a small block at `0x02B5D090`: the open byte `0x02B5D090` (set by `0x003E9020`, cleared by `0x003E90E0`
and `0x003E9100`), the kind byte `0x02B5D091`, and the four colours `setgaugecolor` hands to the gauge, `0x02B5D098` to
`0x02B5D0A4`.

`setgaugecolor` (`0x00357270`) pops five values and calls `0x003E9120(i, r, g, b, a)` (`0x003572CB`), which:

- limits `i` to 0..3 (`0x003E9123`-`0x003E9134`);
- packs the four bytes as `r | g << 8 | b << 16 | a << 24` and stores them in entry `i` of the table
  (`0x003E9154`-`0x003E9160`);
- passes all four entries to `0x00408780` (`0x003E9163`-`0x003E917D`).

The gauge's own colours are therefore the table's: the three entries the verb does not name are the ones the last
`initgauge` or `setgaugecolor` left, and an entry packed as `0xFFFFFFFF` (all four values 255) leaves that colour of
the gauge as it was.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B5D091` | `u8` | 0 | the kind `initgauge` was given, its one argument (`0x0034DC79`-`0x0034DC88`), stored before the kind is turned into the type | `0x003E9020` (`0x003E903D`) | no reader (Project notes) |
| `0x02B5D09C` | `u32` | 0 | colour entry 1, the gauge's second colour (`+0xFC`, `0x004087B6`): green 0x80, blue 0x80, alpha 0x80 at every open | `0x003E9020`, `0x80808000` (`0x003E9054`); `0x003E9120` for `i` = 1 (`0x003E9160`) | `0x003E9120` (`0x003E9171`) |
| `0x02B5D0A0` | `u32` | 0 | colour entry 2, the gauge's third colour (`+0x100`, `0x004087C2`): red 0x80, green 0x80, alpha 0x80 at every open | `0x003E9020`, `0x80008080` (`0x003E905E`); `0x003E9120` for `i` = 2 (`0x003E9160`) | `0x003E9120` (`0x003E916A`) |

At every open `0x003E9020` also stores `0x80008000` (green 0x80, alpha 0x80) in entry 0 (`0x003E904A`) and `0x80000080`
(red 0x80, alpha 0x80) in entry 3 (`0x003E9068`); it does not pass them to the gauge, whose counter starts with the
colours `0x00407F90` gives it.

The gauges' records come from a pool of 32 `0x48`-byte records, which `0x003E7DF0` builds at start-up (called
at `0x00266E3D`). It zeroes the 32 records from `0x02B5C780`,
stores `0x20` plus the record's index at `+0x28` and 0 in the byte `+0x2C` (`0x003E7E00`-`0x003E7E38`), then links
records 3 to 30 both ways, `+0x00` to the next record and `+0x08` to the previous one (`0x003E7E50`-`0x003E7E67`).

It closes the chain at both ends: record 2's `+0x00` is record 3 and its `+0x08` is 0, record 31's `+0x08` is record 30
and its `+0x00` is 0. Record 0's `+0x00` points to record 2, so records 2 to 31 hang from record 0 as one list of
30; record 0's `+0x08` and both links of record 1 are 0 (`0x003E7E69`-`0x003E7EAF`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B5C788` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08` of record 0 of the record pool `0x003E7DF0` builds | `0x003E7DF0` (`0x003E7E06` in the clearing loop; 0 at `0x003E7EA1`) | no reader is named here; `0x003E7DF0` forms the pool's addresses at `0x003E7DF3`, `0x003E7E3A`, `0x003E7E69`, `0x003E7E7E` and `0x003E7E8C` |
| `0x02B5C7C8` | `void*` | 0 (zero-filled tail of `.data`) | `+0x00` of pool record 1 | `0x003E7DF0` (`0x003E7E02`; 0 at `0x003E7EAF`) | as above |
| `0x02B5C7D0` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08` of pool record 1 | `0x003E7DF0` (`0x003E7E06`; 0 at `0x003E7EA8`) | as above |
| `0x02B5C810` | `void*` | 0 (zero-filled tail of `.data`) | `+0x00` of pool record 2, the first of the list of 30: record 3 (`0x02B5C858`) | `0x003E7DF0` (`0x003E7E02`; `0x003E7E77`) | as above |
| `0x02B5C818` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08` of pool record 2 | `0x003E7DF0` (`0x003E7E06`; 0 at `0x003E7E70`) | as above |
| `0x02B5D038` | `void*` | 0 (zero-filled tail of `.data`) | `+0x00` of pool record 31, the last of the list | `0x003E7DF0` (`0x003E7E02`; 0 at `0x003E7E9A`) | as above |
| `0x02B5D040` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08` of pool record 31: record 30 (`0x02B5CFF0`) | `0x003E7DF0` (`0x003E7E06`; `0x003E7E85`) | as above |

## Modding notes

- `initgauge 3` leaves the gauge without a child and reads a null layout record; use kinds 0 to 2. No shipped
  script passes 3: the 268 calls in the `us` scripts push the literal kinds 0 (85), 1 (2) and 2 (181).
- `resetgaugetimer` does nothing to an open timer; set the timer with `setgaugetimer` instead.
- The long format shows up to 9:59:59.99 and then a fixed 99:59:59.99 while the value keeps counting; the
  short one stops at 999.99 seconds.
- The thresholds default to the quarters of the maximum each time the maximum is set, so set the conditions
  after the maximum.

## Related

- [Battle menu](battle-menu.md): the boss gauge, whose bars use the same counter.
- [HUD](hud.md): the HUD switch and the gauge hide bit.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the gauge verbs.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the mask that pauses the gauges.
- [Widgets](widgets.md): the opening and closing runs.
