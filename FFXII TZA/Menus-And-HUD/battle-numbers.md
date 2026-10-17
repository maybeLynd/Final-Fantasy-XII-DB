---
title: "Battle numbers: the damage, healing and MP numbers, the reaction pictures and the status words that rise over units"
kind: "system"
category: "Menus and HUD"
addresses: "003BBD00, 00506700, 00505500, 003BBA60, 003BBB60, 00505560, 00505570, 00505E00"
---

## What the player sees

When a unit takes damage, is healed or loses MP, a number pops up over it, each digit bouncing up one after the
other before the number fades. Some results show a small picture instead, and a status taking hold shows its name.
Several popups on the same unit at once are spread apart. Popups far from the camera are drawn smaller and vanish
beyond a set distance.

## How it works

### The popup ring

The popups live in a ring of 64 records of `50`<sub>h</sub> bytes at `[02B457D0]`; the byte `02B443C0` is the next slot.
`003BBD00(request)` posts one and returns the slot with bit 5 set, or `FF`<sub>h</sub> when it refuses:

1. it refuses when the ring is absent, when the next slot is still in use, and for a status word whose record
   `0035D330(1Ah, status)` has `+24`<sub>h</sub> = `-1`;
2. it notes the spread positions held by the owner's popups younger than 30 frames (256 for a word) and takes
   position 0 when it is free; otherwise 2 when 1 is held and 2 is free, 4 when 3 is held and 4 is free, 1 when
   only 3 is held, 3 when only 1 is held, and 1 or 3 at random (`rand`) in every other case;
3. it flashes the owner's party row (`0028FBE0`; [Party list](party-list.md));
4. for a status word it pushes the owner's other words on (their step `+3A`<sub>h</sub> grows by 3) and delays the new one
   until 3 frames after the latest (`+44`<sub>h</sub>);
5. `00506700` fills the record, and the spread offset `+14`<sub>h</sub>/`+18`<sub>h</sub> is the position's pair at `00D11600` times a
   random factor `1 + (rand() & 31) / 32`.

| Position | Offset |
|---:|---|
| 0 | 0, 0 |
| 1 | -16, -16 |
| 2 | 16, 16 |
| 3 | 16, -16 |
| 4 | -16, 16 |

### The three kinds

`00506700(popup, request)` zeroes the record, stores the owner (`+00`<sub>h</sub>) and its handle (`003589B0`, `+08`<sub>h</sub>),
sets the step `+3A`<sub>h</sub> to 1 and the kind `+3C`<sub>h</sub> from the request's byte `+0C`<sub>h</sub>:

| Kind | Posted by | Record |
|---:|---|---|
| 0, number | `003283D0(unit, amount, isHeal, b)` for HP ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)) and MP ([MP](../Status-Effects-And-KO/mp.md)) | the digits of the absolute amount (`003EFD00`) at `+40`<sub>h</sub>, their count `+3F`<sub>h</sub>, the atlas `battle_4_c` (`0024A5A0`), the colour `002DD7E0(00D227A8[colour])` at `+0C`<sub>h</sub> and its palette `002DD7B0` at `+3D`<sub>h</sub> |
| 1, picture | `00328480(unit, frame)`, from the result reactions `00307300` (frames 0, 2, 4 and 5) and the auto-attack start `00312FA0` (frame 3) | the frame `+3F`<sub>h</sub>, the atlas `battle_4_p`, two colours from the byte pairs at `00D22780` |
| 2, status word | `003284D0(unit, status)` ([Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md)) | step 3, the status's name (`002B58B0` of the record's `+18`<sub>h</sub>) laid out by `002B3050`, palette 4, and the colour by the record's `+25`<sub>h</sub>: bit 1 colour 1, bit 2 `12`<sub>h</sub>, bit 3 `B6`<sub>h</sub>, bit 4 `F3`<sub>h</sub>, else grey `80808080`<sub>h</sub> |

### Number colours

`003283D0` picks the colour slot from `01EED300[(isHeal x 2 | b) + side]`, where `side` is 4 when the unit's
`+698`<sub>h</sub> record is absent or its byte `+5` is set and `00263C20` does not return 3, and 0 otherwise. The slot
names an entry of the menu colour table through `00D227A8`:

| `isHeal`, `b` | side 0 slot | colour | side 4 slot | colour |
|---|---:|---|---:|---|
| damage, 0 | 2 | `11`<sub>h</sub> | 6 | `12`<sub>h</sub> |
| damage, 1 | 4 | `11`<sub>h</sub> | 8 | `12`<sub>h</sub> |
| heal, 0 | 1 | `13`<sub>h</sub> | 5 | `13`<sub>h</sub> |
| heal, 1 | 3 | `13`<sub>h</sub> | 7 | `13`<sub>h</sub> |

### Ageing

`003BBA60` runs once per 60 fps tick from the subsystem pump ([Subsystem update flags](../Engine-Core/subsystem-update-flags.md)).
While bit 1 of the update word `01EFE31C` is set (`003BBF90`, from `002547C0`), it steps each live popup with
`00505500` and frees it when that returns 1:

- a number or picture adds its step `+3A`<sub>h</sub> to its age `+38`<sub>h</sub> and ends past age 37;
- a status word first waits out its delay `+44`<sub>h</sub>, then ages by 6 a frame up to 128 and by its step after that,
  ending past 256.

The same call moves the layer's alpha `01EFE320` by 0.2 toward 1.0 while bit 1 of `01EFE31D` is set and toward 0
otherwise.

### Drawing

`003BBB60` draws nothing while the layer's alpha is 0 and `01EFE31D` bit 1 is clear. Otherwise it walks the ring from
the newest popup: status words through `0028A090` into the screen-space list (`003F1520`, `003F1530`), numbers and
pictures through `00505560`, which jumps on the kind `+3C`<sub>h</sub> to `00505E00` (0, a number) or `00505570` (1, a
picture). It ends with `0028EE10`.

### Numbers on screen

`00505E00(popup, alpha)` draws one number:

1. The opacity is `age x 32` up to age 30 and `668 - 18 x age` after, times the layer's alpha, clamped to 0-128.
2. The position is the owner's (`003588B0`, `002EA0E0`), or the last one kept at `+20`<sub>h</sub> when the owner is gone.
3. Beyond 30 units from the camera `02AED5F0` the opacity falls by `1 - (distance - 30)`, so the number is gone past
   31 units.
4. The spread scale is `8 / distance` clamped to 0.2-1.8 and the digit size `6 / distance + 0.3` clamped to 0.8-1.8,
   both times `00254A00` when `002DDC50` holds.
5. Digit `i` is raised by `00D227D0[clamp(age - i, 0, 17)]`, so each digit bounces one frame after the one before,
   and the next digit is placed 12 times the size to the right.

```
00D227D0  0 2 10 18 25 30 32 30 25 18 10 2 0 -2 -4 -2 -1 0
```

`00505570` draws a picture with one sprite:

1. The opacity is `age x 16` up to age 30. After that it is the colour's alpha byte `+0F`<sub>h</sub> less
   `(((a - a/7) / 2 + a/7) / 4) x (age - 30)`, 18 a frame for `a` = 128, and it never rises above that alpha byte.
2. The size is `6 / distance + 0.3` clamped to 0.8-1.2, times the scale `00D22800[min(age, 17)]` (18 floats, 1.8
   falling to 1.0).
3. The height comes from `00D227E8[min(age + 4, 17)]`.
4. Its four corners alternate the two colours.

## Layouts

`BattlePopup` (`50`<sub>h</sub> bytes, offsets from the start of the [02B457D0]+i*`50`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | owner | the unit; 0 for a free slot |
| `08`<sub>h</sub> | `u32` | handle | `003589B0` of the owner |
| `0C`<sub>h</sub> | `u32` | colour | menu colour table entry (`002DD7E0`) |
| `10`<sub>h</sub> | `u32` | colour2 | second colour of a picture |
| `14`<sub>h</sub> | `f32` | offsetX | spread offset |
| `18`<sub>h</sub> | `f32` | offsetY | spread offset |
| `20`<sub>h</sub> | `f32[3]` | position | last owner position |
| `30`<sub>h</sub> | `void*` | atlas | battle_4_c, battle_4_p or the status text |
| `38`<sub>h</sub> | `i16` | age | frames shown |
| `3A`<sub>h</sub> | `i16` | step | age added per frame |
| `3C`<sub>h</sub> | `u8` | kind | 0 number, 1 picture, 2 status word |
| `3D`<sub>h</sub> | `u8` | palette | `002DD7B0` of the colour; 4 for a status word |
| `3E`<sub>h</sub> | `u8` | spread | position 0 to 4 |
| `3F`<sub>h</sub> | `u8` | count | digits, picture frame or status |
| `40`<sub>h</sub> | `char[8]` | text | kind 0: the digits; kind 2: `002B3050` writes +`40`<sub>h</sub> and +`42`<sub>h</sub> and +`44`<sub>h</sub> is the delay |

## Modding notes

- A number or picture lasts 38 frames at step 1; a status word takes 22 frames after its delay to reach
  age 132, then grows by its step until it passes 256.
- Popups beyond 31 units from the camera are not drawn at all.
- The ring holds 64 popups; a post is refused while the next slot is still showing.

## Related

- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md): the hit and heal numbers.
- [MP](../Status-Effects-And-KO/mp.md): the MP numbers.
- [Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md): the status words.
- [Party list](party-list.md): the row flash each popup starts.
- [Subsystem update flags](../Engine-Core/subsystem-update-flags.md): the pump that ages them.
