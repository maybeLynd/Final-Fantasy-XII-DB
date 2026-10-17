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

The popups live in a ring of 64 records of 0x50 bytes at `[02B457D0]`; the byte `02B443C0` is the next slot.
`003BBCD0`, from the field set-up `00253A30` (`00253A39`), points `02B457D0` at the block `02B443D0` and clears its
`0x1400` bytes; `003BBB30`, from `0028E190` (`0028E1BE`), does the same after `0028FB60`.
`003BBD00(request)` posts one and returns the slot with bit 5 set, or `0xFF` when it refuses:

1. it refuses when the ring is absent, when the next slot is still in use, and for a status word whose record
   `0035D330(0x1A, status)` has `+0x24` = `-1`;
2. it notes the spread positions held by the owner's popups younger than 30 frames (256 for a word) and takes
   position 0 when it is free; otherwise 2 when 1 is held and 2 is free, 4 when 3 is held and 4 is free, 1 when
   only 3 is held, 3 when only 1 is held, and 1 or 3 at random (`rand`) in every other case;
3. it flashes the owner's party row (`0028FBE0`; [Party list](party-list.md));
4. for a status word it pushes the owner's other words on (their step `+0x3A` grows by 3) and delays the new one
   until 3 frames after the latest (`+0x44`);
5. `00506700` fills the record, and the spread offset `+0x14`/`+0x18` is the position's pair at `00D11600` times a
   random factor `1 + (rand() & 31) / 32`.

| Position | Offset |
|---:|---|
| 0 | 0, 0 |
| 1 | -16, -16 |
| 2 | 16, 16 |
| 3 | 16, -16 |
| 4 | -16, 16 |

### The three kinds

`00506700(popup, request)` zeroes the record, stores the owner (`+0x00`) and its handle (`003589B0`, `+0x08`),
sets the step `+0x3A` to 1 and the kind `+0x3C` from the request's byte `+0x0C`:

| Kind | Posted by | Record |
|---:|---|---|
| 0, number | `003283D0(unit, amount, isHeal, b)` for HP ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)) and MP ([MP](../Status-Effects-And-KO/mp.md)) | the digits of the absolute amount (`003EFD00`) at `+0x40`, their count `+0x3F`, the atlas `battle_4_c` (`0024A5A0`), the colour `002DD7E0(00D227A8[colour])` at `+0x0C` and its palette `002DD7B0` at `+0x3D` |
| 1, picture | `00328480(unit, frame)`, from the result reactions `00307300` (frames 0, 2, 4 and 5) and the auto-attack start `00312FA0` (frame 3) | the frame `+0x3F`, the atlas `battle_4_p`, two colours from the byte pairs at `00D22780` |
| 2, status word | `003284D0(unit, status)` ([Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md)) | step 3, the status's name (`002B58B0` of the record's `+0x18`) laid out by `002B3050`, palette 4, and the colour by the record's `+0x25`: bit 1 colour 1, bit 2 `0x12`, bit 3 `0xB6`, bit 4 `0xF3`, else grey `0x80808080` |

### Number colours

`003283D0` picks the colour slot from `01EED300[(isHeal x 2 | b) + side]`, where `side` is 4 when the unit's
`+0x698` record is absent or its byte `+5` is set and `00263C20` does not return 3, and 0 otherwise. The slot
names an entry of the menu colour table through `00D227A8`:

| `isHeal`, `b` | side 0 slot | colour | side 4 slot | colour |
|---|---:|---|---:|---|
| damage, 0 | 2 | `0x11` | 6 | `0x12` |
| damage, 1 | 4 | `0x11` | 8 | `0x12` |
| heal, 0 | 1 | `0x13` | 5 | `0x13` |
| heal, 1 | 3 | `0x13` | 7 | `0x13` |

### Ageing

`003BBA60` runs once per 60 fps tick from the subsystem pump ([Subsystem update flags](../Engine-Core/subsystem-update-flags.md)).
While bit 1 of the update word `01EFE31C` is set (`003BBF90`, from `002547C0`), it steps each live popup with
`00505500` and frees it when that returns 1:

- a number or picture adds its step `+0x3A` to its age `+0x38` and ends past age 37;
- a status word first waits out its delay `+0x44`, then ages by 6 a frame up to 128 and by its step after that,
  ending past 256.

The same call moves the layer's alpha `01EFE320` by 0.2 toward 1.0 while bit 1 of `01EFE31D` is set and toward 0
otherwise.

### Drawing

`003BBB60` draws nothing while the layer's alpha is 0 and `01EFE31D` bit 1 is clear. Otherwise it walks the ring from
the newest popup: status words through `0028A090` into the screen-space list (`003F1520`, `003F1530`), numbers and
pictures through `00505560`, which jumps on the kind `+0x3C` to `00505E00` (0, a number) or `00505570` (1, a
picture). It ends with `0028EE10`.

### Numbers on screen

`00505E00(popup, alpha)` draws one number:

1. The opacity is `age x 32` up to age 30 and `668 - 18 x age` after, times the layer's alpha, clamped to 0-128.
2. The position is the owner's (`003588B0`, `002EA0E0`), or the last one kept at `+0x20` when the owner is gone.
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

1. The opacity is `age x 16` up to age 30. After that it is the colour's alpha byte `+0x0F` less
   `(((a - a/7) / 2 + a/7) / 4) x (age - 30)`, 18 a frame for `a` = 128, and it never rises above that alpha byte.
2. The size is `6 / distance + 0.3` clamped to 0.8-1.2, times the scale `00D22800[min(age, 17)]` (18 floats, 1.8
   falling to 1.0).
3. The height comes from `00D227E8[min(age + 4, 17)]`.
4. Its four corners alternate the two colours.

## Layouts

`BattlePopup` (`0x50` bytes, offsets from the start of the [02B457D0]+i*0x50):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | owner | the unit; 0 for a free slot |
| `+0x08` | `u32` | handle | `003589B0` of the owner |
| `+0x0C` | `u32` | colour | menu colour table entry (`002DD7E0`) |
| `+0x10` | `u32` | colour2 | second colour of a picture |
| `+0x14` | `f32` | offsetX | spread offset |
| `+0x18` | `f32` | offsetY | spread offset |
| `+0x20` | `f32[3]` | position | last owner position |
| `+0x30` | `void*` | atlas | battle_4_c, battle_4_p or the status text |
| `+0x38` | `i16` | age | frames shown |
| `+0x3A` | `i16` | step | age added per frame |
| `+0x3C` | `u8` | kind | 0 number, 1 picture, 2 status word |
| `+0x3D` | `u8` | palette | `002DD7B0` of the colour; 4 for a status word |
| `+0x3E` | `u8` | spread | position 0 to 4 |
| `+0x3F` | `u8` | count | digits, picture frame or status |
| `+0x40` | `char[8]` | text | kind 0: the digits; kind 2: `002B3050` writes +`0x40` and +`0x42` and +`0x44` is the delay |

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
