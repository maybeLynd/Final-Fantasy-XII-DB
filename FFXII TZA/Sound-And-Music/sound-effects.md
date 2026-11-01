---
title: "Sound effects: how a request to play a sound becomes a playing voice, the three volume settings, pan and fades"
kind: "system"
category: "Sound and music"
addresses: "0x002DF220, 0x002DEF40, 0x002DF0F0, 0x002DEE80, 0x00224570, 0x002257E0, 0x002256F0, 0x007A9E50"
---

## What the player sees

- Every menu blip, hit and footstep is a sound effect played from a bank ([Sound banks](sound-banks.md)).
- Some sounds never overlap themselves: a second one fades the first out.
- The Config screen's Volume heading has three rows: Music, Sound Effects and Voice.
- Sounds are placed around the listener on a ring of eight speaker positions, in front or behind.

## How it works

### The play calls

The play calls sit in `0x002DEE80`-`0x002DF530` and reach the audio manager through a forwarder:

| Call | Arguments | Does |
|---|---|---|
| `0x002DF220` | id, pan, volume | plays from a block bank; answers 0 for id -1 (`0x002DF236`-`0x002DF244`), else a play handle |
| `0x002DEF40` | id, pan, volume | answers 0 without playing while `0x022CB726` is set (`0x003603C0`, `0x002DEF56`; [Game over](../World-Areas-And-Travel/game-over.md)); otherwise plays through `0x001DBDB0` from a block bank when id bit `0x80000000` is set and from a six-digit bank when it is clear (`0x002DEF77`-`0x002DEF83`) |
| `0x002DF010` | id | as `0x002DEF40` with pan `0x40` and volume `0x7F` (`0x002DF02B`) |
| `0x002DEE80` | handle | answers whether the sound with that handle still plays |
| `0x002DF0F0` | handle, id | stops the sound with that handle on either side, or every block-bank sound for id -1 |
| `0x002DF170`, `0x002DF190` | handle or id, frames | stops with a fade of `frames / 60` seconds; 0 frames is passed on as 1 (`0x00210DBD`, `0x00210DCD`) |
| `0x002DF150`, `0x002DF1A0` | handle, volume (, frames) | sets the volume, at once or over frames |
| `0x002DEF20` | handle, pan | sets the pan |
| `0x002DF280` | id, position, record | `0x002DEFA0` with bit `0x80000000` set: a block-bank sound placed at the position; 0 for id -1 |
| `0x002DF120` | handle, position | moves a playing placed sound, except while `0x003603C0` answers non-zero |
| `0x002DF1E0` | bank id, frames, volume | sets the volume of every sound of that six-digit bank, at once or over frames |

Volume is masked to 0-127 and pan to a byte before the controller (`0x00210C03`-`0x00210C0C`).

### The gates

1. `0x00249C60(slot)`, `0x00249CA0(slot)` and `0x0024A1A0(handle)` return -1 at once while `0x02091098` is not 0
   (`0x00249C64`); `0x00249FC0` is its only writer. Other callers of `0x002DF220`, such as `0x00271500`, `0x003A0E20` and the
   script verb body `0x00357040`, do not read it.
2. Every play entry answers 0 while the byte `0x022CB726` is set (`0x003603C0`, read at `0x002DF23B`). `0x003601D0` sets it
   after stopping every block-bank sound and releasing every six-digit bank (`0x00360252`-`0x003602A4`); `0x00360110` and
   `0x00360370` clear it.
3. The id builders `0x003A1180`, `0x003A1070` and `0x003A1100` answer -1 when `0x00267330(0)` is non-zero; it reads byte `+0x10`
   of record 0 at `0x02098E10` (`0x00267333`-`0x00267341`).

### The play handle

`0x00212950` counts handles in `0x01FD36B4`, from 1 to `0x7FFFFFFF` and then round again (`0x00212950`-`0x00212965`). The
handle is returned even when no bank owns the id, and is kept in the voice at `+0x18`.

### Which bank

`0x00210C00` sends a block-bank request to `0x0021B5B0` and a six-digit request to `0x00219EA0`:

1. A block bank is the one whose block registry slot `+0x3C` equals `id / 512`; the sound slot is `id & 0x1FF`
   (`0x002245D3`).
2. A six-digit bank is the one whose `+0x38` equals the whole id, and its voice takes slot 0 (`0x002257D0`).

### Starting a block-bank voice

`0x00224570(bank, handle, id, pan, volume)` starts the voice (`0x002245AC`-`0x00224825`):

1. While the bank is still loading it waits (`0x002245AC`-`0x002245C5`).
2. The slot must be in the bank's map, and its sound entry present in the loaded `.sab` (`0x007A8CF0`,
   `0x0022463F`-`0x00224651`).
3. The slot's flag byte decides the rest, below.
4. Otherwise it takes a voice, stores slot `+0x14`, id with bit `0x80000000` set `+0x24` and handle `+0x18`, sets pan and volume
   and posts the start to the driver (`0x007A78B0`, `0x00224825`).

| Flag bit | Effect |
|---|---|
| 3 (`0x08`) | not started while slot 7 of the same bank plays, unless this is slot 7 (`0x00224657`-`0x0022467E`) |
| 5 (`0x20`) | before starting, every playing block or six-digit sound whose own slot flags have bit `0x40` (`0x40`) is checked: one with the same id fades to the new volume over 4.8 s and the new sound is not started; any other fades out over 4.8 s (`0x0022468A`-`0x002246A4`, `0x00210710`, `0x002238F0`) |
| 7 (`0x80`) | a voice already playing this slot is reused with the new pan and volume (`0x002246E3`-`0x00224756`) |

A six-digit bank's start `0x00223190` reads one flag byte for the whole bank, `+0x44`, and a bank with bit `0x20` starts its
voice with a 4.8 s fade in.

### Volume

`0x002257E0(voice, volume, frames)` clamps the volume to 0-127 (`0x002257EC`-`0x0022580A`) and posts
`volume / 127` over `frames / 60` seconds to the driver's `Sound::SetVolume` (`0x007BEAF0`).

The three Config rows are options commands `0x13`, `0x14` and `0x15` (`0x002408F1`, `0x00240902`, `0x00240913`):

| Row | Body | Stored at | Category |
|---|---|---|---:|
| Music | `0x002DE0B0` | options `+0x08` | 1 |
| Sound Effects | `0x002DE290` | options `+0x0A` | 2 |
| Voice | `0x002DE310` | options `+0x0C` | 3 |

Each clamps its value to 0-100, divides it by 100 and ramps its category's volume (`0x00210ED0`, `0x007AA570`). A sound
takes the category named by byte `+6` of its sound header (`0x007BD570`), and the category's volume multiplies its own
(`0x007A9F40`, `0x007AA894`-`0x007AA924`).

### Pan

`0x002256F0(voice, pan, frames)` turns the pan byte into the driver's pan and front-back values
(`0x00225743`-`0x00225783`):

| Pan byte | Driver pan | Front-back |
|---|---|---|
| `0x00`-`0x7F` | `(pan - 0x40) / 128` | +1 |
| `0x80`-`0xFF` | `(0xBF - pan) / 128` | -1 |

The driver turns pan into an angle of `pan * pi`, and a front-back of -1 adds half a turn (`0x007B875B`-`0x007B8769`).
So `0x40` is straight ahead, `0x00` 270 degrees, `0x7F` about 89 degrees, `0xBF` straight behind and `0xFF` 90 degrees:
`0x80`-`0xFF` is the rear half, run the other way. The output count is always 8 (`0x007AF06A`), so the eight-speaker
ring is used. A pan change moves at no more than 5.0 per second (`0x007BE510`).

### Fades

`0x007A9E50(curve, t)` is the fade shape, with six curves from the jump table at `0x007A9F1C`:

| Curve | Shape |
|---:|---|
| 0 | t |
| 1 | 1 - (1 - t²)³ |
| 2 | 1 - (1 - t)² |
| 3 | t² |
| 4 | 2^t - 1 |
| 5 | 2 - 2^(1-t) |

A curve above 5 gives 0 (`0x007A9E5A`). The ramp setter `0x007CA560` has 97 calls:

1. 75 pass curve 0: every method of the driver's `Sound` in `0x007BE0B0`-`0x007BEF30`, among them volume (`0x007BEBF2`),
   pan, pitch and stop, and the category volume ramps (`0x007AA4F0`-`0x007AA570`). So every volume, pan, pitch and stop
   ramp on a voice or a category is linear.
2. The music player reads its curve from its own data, such as byte `+1` of a record (`0x007C3960`, `0x007C5127`,
   `0x007CBCEF`) or byte `+0xC` of a player's parameter block (`0x007E7F3D`).
3. The driver's `Filter` effect picks curves 4 and 5 for its own parameter ramps (`0x007D1840`, `0x007D1A10`).

### Rate-limited ramps

A ramp whose `+0x24` is 1 never moves faster than its rates. When `0x007CA560` gives a ramp a new target it keeps the
duration it was asked for, unless that would beat the rate (`0x007CA5D2`-`0x007CA631`):

```python
if ramp+0x24 == 1:
    if target > current: duration = max(duration, (target - current) / |ramp+0x28|)
    else:                duration = max(duration, (current - target) / |ramp+0x2C|)
```

The driver's `Sound` re-targets its ramp at `+0x3C8` to 0 the same way (`0x007BE207`-`0x007BE26E`). Three places turn the
limit on, and every constructor turns it off (`+0x24` = 0):

| Ramps | Turned on by | Rise `+0x28` | Fall `+0x2C` |
|---|---|---|---|
| a sound's `+0x1B8`, `+0x1E8`, `+0x218` | `Sound` slot 10 `0x007BE510` with its flag set (`0x007BE533`-`0x007BE563`) | 5.0 | 5.0 |
| a sound's curved ramp `+0x88` | `Sound` slot 11 `0x007BEC70` with its flag set (`0x007BEC9F`, `0x007BECA7`) | 5.0 | 5.0 |
| a sound's `+0x248` and `+0x278` | `0x007BDDA0`, when byte `+1` of the sound header's entry is 1 (`0x007BDEB7`, `0x007BDEBC`) | entry `+0x10` | entry `+0x14` |

With the flag clear, slots 10 and 11 set `+0x24` to 0 (`0x007BE579`-`0x007BE585`, `0x007BECBD`), and `0x007BDDA0` does for an
entry whose byte `+1` is not 1 (`0x007BDEC1`). The header's entries are `0x20` bytes from header word `+0x4C`, at most
two, counted by header byte `+0x4E` (`0x007CFF40`). `0x007BFFA0`, which copies a sound into its replacement (`0x007B4C65`),
copies `+0x24`-`+0x2F` of eleven of its ramps (`0x007BFFA0`-`0x007C04E1`).

### Stopping a sound

`0x002DF0F0(handle, 0)` stops the sound with that handle with a 0.1 s fade (`0x00222390`). By id it sends a block-bank
request as `id | 0x80000000` (`0x00210C65`), which `0x0021B640` acts on only for -1, -2 and -4 (`0x0021B647`), so one
block-bank sound cannot be stopped by its id.

`0x002716F0(handle)` stops a handle only when it is not negative and `0x002DEE80` answers that it still plays; its
only caller is the special-attack window `0x002D5EB0` ([Menu screens](../Menus-And-HUD/menu-screens.md)).

### Stopping after a delay

`0x003B3EA0(handle, frames)` starts a fade-out of `frames` (`0x002DF170`) and queues the handle in the first free entry of
32 at `0x02EBCC80`, with a countdown of `frames` plus a quarter of it, at least 2. `0x003B3D20`, run from `0x0024D540`,
counts each entry down and stops its handle at 0 (`0x002DF0F0`), closing the queue up. When `0x003E7DE0` answers non-zero
it instead calls `0x003B3E40`, which stops every queued handle at once and empties the queue.

## Layouts

A ramp, `0x30` bytes with the vtable `0x01CB44A0`. The driver builds them in seven places: a category's two arrays at
`+0x38` and `+0x40` (`0x007AA199`), five in a bus from `+0x38` (`0x007AC5B0`), two in an external source voice at `+0x490`
and `+0x4C0` (`0x007B8D8D`), thirteen in a sound from `+0x188` (`0x007BC978`), seven in a track from `+0x38` (`0x007E7AB7`),
two in each of a track's four `0x70`-byte pairs from `+0x1F8` (`0x007F3DF2`), and two in a sound source object at `+0x48`
and `+0x80` (`0x007EF946`). A sound's four curved ramps from `+0x88` (`0x01CB5A20`, `0x007BC903`) start with one.

`AudioParameterRamp` (`0x30` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x01CB44A0`, written by the seven builders (e.g. `0x007AA1C0`) |
| `+0x08` | `f32` | start | the value the ramp moves from |
| `+0x0C` | `f32` | target | the value it moves to, and the value outright when duration is 0 |
| `+0x10` | `f32` | elapsed | the time so far |
| `+0x14` | `f32` | duration | the ramp's length; exactly 0 snaps to the target |
| `+0x18` | `u8[4]` | pad18 | copied with a sound by `0x007BFFA0` (e.g. `0x007BFFFA`); no other access |
| `+0x1C` | `i32` | curve | the fade curve 0-5 of `0x007A9E50` |
| `+0x20` | `u8` | active | 1 while the ramp runs; `0x007CA560` sets it (`0x007CA5EB`) |
| `+0x21` | `u8[3]` | pad21 | read and written by no function; nothing fixes its width |
| `+0x24` | `u32` | limited | 1: the ramp keeps to its rise and fall rates (read `0x007CA5D2`, `0x007BE207`); set to 1 by `0x007BE510` (`0x007BE533`), `0x007BEC70` (`0x007BEC9F`) and `0x007BDDA0` (`0x007BDEB7`); 0 from every builder (e.g. `0x007AA1D2`, `0x007AC611`, `0x007BC9D2`, `0x007E7B43`, `0x007EF9D1`, `0x007F3E0D`, `0x007B8DDC`) and from `0x007BE579`-`0x007BE585`, `0x007BECBD`, `0x007BDEC1`, `0x007C0531`, `0x007C055B`-`0x007C05A4` |
| `+0x28` | `f32` | riseRate | the most the value may rise per second when limited: duration is at least the rise over this (`0x007CA5F6`, `0x007BE23A`); 5.0 from `0x007BE510` (`0x007BE533`) and `0x007BEC70` (`0x007BEC9F`); the header entry's `+0x10` from `0x007BDDA0` (`0x007BDEB7`); copied by `0x007BFFA0` |
| `+0x2C` | `f32` | fallRate | the most the value may fall per second when limited (`0x007CA617`, `0x007BE256`); 5.0 from `0x007BE510` (`0x007BE547`, `0x007BE555`, `0x007BE563`) and `0x007BEC70` (`0x007BECA7`); the header entry's `+0x14` from `0x007BDDA0` (`0x007BDEBC`); copied by `0x007BFFA0` |

## State

The delayed-stop queue is 32 entries of 8 bytes from `0x02EBCC80`: a byte that marks the entry used at `+0`, the
countdown in frames (`u16`) at `+2` and the sound handle (`u32`) at `+4`. When an entry's countdown ends,
`0x003B3D20` moves every later entry down one, so the last entry is read as the source of the move, and empties the last
(`0x003B3D88`-`0x003B3DD2`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBCD78` | `u8` | 0 | the last entry's used byte | `0x003B3D20`, 0 (`0x003B3DC4`); `0x003B3E10`, 0 (`0x003B3E20`); `0x003B3E40`, 0 (`0x003B3E6F`); `0x003B3EA0`, 1 (`0x003B3EDD`) | `0x003B3D20` (`0x003B3D73`, and as the source of the move at `0x003B3DB0`); `0x003B3E40` (`0x003B3E60`); `0x003B3EA0` (`0x003B3EC1`) |
| `0x02EBCD7A` | `u16` | 0 | the last entry's countdown | `0x003B3D20`: 1 less each frame (`0x003B3D79`), 0 (`0x003B3DCB`); `0x003B3E10` (`0x003B3E23`); `0x003B3E40` (`0x003B3E73`); `0x003B3EA0` (`0x003B3EFB`) | `0x003B3D20` (`0x003B3D79`, `0x003B3DB0`) |
| `0x02EBCD7C` | `u32` | 0 | the last entry's sound handle | `0x003B3D20`, 0 (`0x003B3DD2`); `0x003B3E10` (`0x003B3E27`); `0x003B3E40` (`0x003B3E77`); `0x003B3EA0` (`0x003B3EE2`) | `0x003B3D20`, which stops it (`0x003B3D7E`, `0x003B3DB0`); `0x003B3E40` (`0x003B3E66`) |

No other instruction reaches these three. The queue's addresses are taken by `0x003B3D20`, `0x003B3E10`, `0x003B3E40` and
`0x003B3EA0` only.

## Modding notes

- A sound's pan byte above `0x7F` puts it behind the listener.
- Flag bit `0x20` of a slot cross-fades it over 4.8 s against the playing sounds whose flags have bit `0x40`; bit `0x8` makes
  it wait for slot 7.
- Changing a voice fade's shape needs a curve argument other than 0 at its `0x007CA560` call; no data selects it for
  voice volume, pan, pitch or stop ramps.
- Stop a sound by the handle its play call returned.

## Related

- [Sound banks](sound-banks.md) - the bank files and sound ids.
- [Sound engine configuration](sound-engine-config.md) - the categories and the voice pools.
- [Music](music.md) - the area music.
- [Escape Mode](../Controls-And-Input/escape.md) - a sound started and stopped by handle.
