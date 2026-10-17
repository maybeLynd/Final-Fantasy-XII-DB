---
title: "Sound effects: how a request to play a sound becomes a playing voice, the three volume settings, pan and fades"
kind: "system"
category: "Sound and music"
addresses: "002DF220, 002DEF40, 002DF0F0, 002DEE80, 00224570, 002257E0, 002256F0, 007A9E50"
---

## What the player sees

- Every menu blip, hit and footstep is a sound effect played from a bank ([Sound banks](sound-banks.md)).
- Some sounds never overlap themselves: a second one fades the first out.
- The Config screen's Volume heading has three rows: Music, Sound Effects and Voice.
- Sounds are placed around the listener on a ring of eight speaker positions, in front or behind.

## How it works

### The play calls

The play calls sit in `002DEE80`-`002DF530` and reach the audio manager through a forwarder:

| Call | Arguments | Does |
|---|---|---|
| `002DF220` | id, pan, volume | plays from a block bank; answers 0 for id -1 (`002DF236`-`002DF244`), else a play handle |
| `002DEF40` | id, pan, volume | answers 0 without playing while `022CB726` is set (`003603C0`, `002DEF56`; [Game over](../World-Areas-And-Travel/game-over.md)); otherwise plays through `001DBDB0` from a block bank when id bit 31 is set and from a six-digit bank when it is clear (`002DEF77`-`002DEF83`) |
| `002DF010` | id | as `002DEF40` with pan `40`<sub>h</sub> and volume `7F`<sub>h</sub> (`002DF02B`) |
| `002DEE80` | handle | answers whether the sound with that handle still plays |
| `002DF0F0` | handle, id | stops the sound with that handle on either side, or every block-bank sound for id -1 |
| `002DF170`, `002DF190` | handle or id, frames | stops with a fade of `frames / 60` seconds |
| `002DF150`, `002DF1A0` | handle, volume (, frames) | sets the volume, at once or over frames |
| `002DEF20` | handle, pan | sets the pan |
| `002DF280` | id, position, record | `002DEFA0` with bit 31 set: a block-bank sound placed at the position; 0 for id -1 |
| `002DF120` | handle, position | moves a playing placed sound, except while `003603C0` answers non-zero |
| `002DF1E0` | bank id, frames, volume | sets the volume of every sound of that six-digit bank, at once or over frames |

Volume is masked to 0-127 and pan to a byte before the controller (`00210C03`-`00210C0C`).

### The gates

1. `00249C60(slot)`, `00249CA0(slot)` and `0024A1A0(handle)` return -1 at once while `02091098` is not 0
   (`00249C64`); `00249FC0` is its only writer. Other callers of `002DF220`, such as `00271500`, `003A0E20` and the
   script verb body `00357040`, do not read it.
2. Every play entry answers 0 while the byte `022CB726` is set (`003603C0`, read at `002DF23B`). `003601D0` sets it
   after stopping every block-bank sound and releasing every six-digit bank (`00360252`-`003602A4`); `00360110` and
   `00360370` clear it.
3. The id builders `003A1180`, `003A1070` and `003A1100` answer -1 when `00267330(0)` is non-zero; it reads byte `+10`<sub>h</sub>
   of record 0 at `02098E10` (`00267333`-`00267341`).

### The play handle

`00212950` counts handles in `01FD36B4`, from 1 to `7FFFFFFF`<sub>h</sub> and then round again (`00212950`-`00212965`). The
handle is returned even when no bank owns the id, and is kept in the voice at `+18`<sub>h</sub>.

### Which bank

`00210C00` sends a block-bank request to `0021B5B0` and a six-digit request to `00219EA0`:

1. A block bank is the one whose registry slot `+3C`<sub>h</sub> equals `id / 512`; the sound slot is `id & 1FFh`
   (`002245D3`).
2. A six-digit bank is the one whose `+38`<sub>h</sub> equals the whole id, and its voice takes slot 0 (`002257D0`).

### Starting a block-bank voice

`00224570(bank, handle, id, pan, volume)` starts the voice (`002245AC`-`00224825`):

1. While the bank is still loading it waits (`002245AC`-`002245C5`).
2. The slot must be in the bank's map, and its sound entry present in the loaded `.sab` (`007A8CF0`,
   `0022463F`-`00224651`).
3. The slot's flag byte decides the rest, below.
4. Otherwise it takes a voice, stores slot `+14`<sub>h</sub>, id with bit 31 set `+24`<sub>h</sub> and handle `+18`<sub>h</sub>, sets pan and volume
   and posts the start to the driver (`007A78B0`, `00224825`).

| Flag bit | Effect |
|---|---|
| 3 (`08`<sub>h</sub>) | not started while slot 7 of the same bank plays, unless this is slot 7 (`00224657`-`0022467E`) |
| 5 (`20`<sub>h</sub>) | before starting, every playing block or six-digit sound whose own slot flags have bit 6 (`40`<sub>h</sub>) is checked: one with the same id fades to the new volume over 4.8 s and the new sound is not started; any other fades out over 4.8 s (`0022468A`-`002246A4`, `00210710`, `002238F0`) |
| 7 (`80`<sub>h</sub>) | a voice already playing this slot is reused with the new pan and volume (`002246E3`-`00224756`) |

A six-digit bank's start `00223190` reads one flag byte for the whole bank, `+44`<sub>h</sub>, and a bank with bit 5 starts its
voice with a 4.8 s fade in.

### Volume

`002257E0(voice, volume, frames)` clamps the volume to 0-127 (`002257EC`-`0022580A`) and posts
`volume / 127` over `frames / 60` seconds to the driver's `Sound::SetVolume` (`007BEAF0`).

The three Config rows are options commands `13`<sub>h</sub>, `14`<sub>h</sub> and `15`<sub>h</sub> (`002408F1`, `00240902`, `00240913`):

| Row | Body | Stored at | Category |
|---|---|---|---:|
| Music | `002DE0B0` | options `+08`<sub>h</sub> | 1 |
| Sound Effects | `002DE290` | options `+0A`<sub>h</sub> | 2 |
| Voice | `002DE310` | options `+0C`<sub>h</sub> | 3 |

Each clamps its value to 0-100, divides it by 100 and ramps its category's volume (`00210ED0`, `007AA570`). A sound
takes the category named by byte `+6` of its sound header (`007BD570`), and the category's volume multiplies its own
(`007A9F40`, `007AA894`-`007AA924`).

### Pan

`002256F0(voice, pan, frames)` turns the pan byte into the driver's pan and front-back values
(`00225743`-`00225783`):

| Pan byte | Driver pan | Front-back |
|---|---|---|
| `00`<sub>h</sub>-`7F`<sub>h</sub> | `(pan - 40h) / 128` | +1 |
| `80`<sub>h</sub>-`FF`<sub>h</sub> | `(BFh - pan) / 128` | -1 |

The driver turns pan into an angle of `pan * pi`, and a front-back of -1 adds half a turn (`007B875B`-`007B8769`).
So `40`<sub>h</sub> is straight ahead, `00`<sub>h</sub> 270 degrees, `7F`<sub>h</sub> about 89 degrees, `BF`<sub>h</sub> straight behind and `FF`<sub>h</sub> 90 degrees:
`80`<sub>h</sub>-`FF`<sub>h</sub> is the rear half, run the other way. The output count is always 8 (`007AF06A`), so the eight-speaker
ring is used. A pan change moves at no more than 5.0 per second (`007BE510`).

### Fades

`007A9E50(curve, t)` is the fade shape, with six curves from the jump table at `007A9F1C`:

| Curve | Shape |
|---:|---|
| 0 | t |
| 1 | 1 - (1 - t²)³ |
| 2 | 1 - (1 - t)² |
| 3 | t² |
| 4 | 2^t - 1 |
| 5 | 2 - 2^(1-t) |

A curve above 5 gives 0 (`007A9E5A`). The ramp setter `007CA560` has 97 calls:

1. 75 pass curve 0: every method of the driver's `Sound` in `007BE0B0`-`007BEF30`, among them volume (`007BEBF2`),
   pan, pitch and stop, and the category volume ramps (`007AA4F0`-`007AA570`). So every volume, pan, pitch and stop
   ramp on a voice or a category is linear.
2. The music player reads its curve from its own data, such as byte `+1` of a record (`007C3960`, `007C5127`,
   `007CBCEF`) or byte `+C`<sub>h</sub> of a player's parameter block (`007E7F3D`).
3. The driver's `Filter` effect picks curves 4 and 5 for its own parameter ramps (`007D1840`, `007D1A10`).

### Stopping a sound

`002DF0F0(handle, 0)` stops the sound with that handle with a 0.1 s fade (`00222390`). By id it sends a block-bank
request as `id | 80000000h` (`00210C65`), which `0021B640` acts on only for -1, -2 and -4 (`0021B647`), so one
block-bank sound cannot be stopped by its id.

`002716F0(handle)` stops a handle only when it is not negative and `002DEE80` answers that it still plays; its
only caller is the special-attack window `002D5EB0` ([Menu screens](../Menus-And-HUD/menu-screens.md)).

### Stopping after a delay

`003B3EA0(handle, frames)` starts a fade-out of `frames` (`002DF170`) and queues the handle in the first free entry of
32 at `02EBCC80`, with a countdown of `frames` plus a quarter of it, at least 2. `003B3D20`, run from `0024D540`,
counts each entry down and stops its handle at 0 (`002DF0F0`), closing the queue up. When `003E7DE0` answers non-zero
it instead calls `003B3E40`, which stops every queued handle at once and empties the queue.

## Modding notes

- A sound's pan byte above `7F`<sub>h</sub> puts it behind the listener.
- Flag bit 5 of a slot cross-fades it over 4.8 s against the playing sounds whose flags have bit 6; bit 3 makes
  it wait for slot 7.
- Changing a voice fade's shape needs a curve argument other than 0 at its `007CA560` call; no data selects it for
  voice volume, pan, pitch or stop ramps.
- Stop a sound by the handle its play call returned.

## Related

- [Sound banks](sound-banks.md) - the bank files and sound ids.
- [Sound engine configuration](sound-engine-config.md) - the categories and the voice pools.
- [Music](music.md) - the area music.
- [Escape Mode](../Controls-And-Input/escape.md) - a sound started and stopped by handle.
