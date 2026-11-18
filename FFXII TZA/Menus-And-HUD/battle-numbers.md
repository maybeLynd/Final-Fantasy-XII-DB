[Home](../../README.md) / [Menus and HUD](README.md) / Battle numbers

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Battle numbers: the damage, healing and MP numbers, the reaction pictures and the status words that rise over units | system | Menus and HUD | Battle HUD | The numbers and words that pop up over a unit in battle: the 64-entry popup ring, the three popup kinds and who posts each, how overlapping popups are spread, the colour a number takes, how digits bounce and fade, how distance shrinks and hides them, the shared fade of the whole layer, and the record each popup keeps. | 0x003BBD00, 0x00506700, 0x00505500, 0x003BBA60, 0x003BBB60, 0x00505560, 0x00505570, 0x00505E00 |

## What the player sees

When a unit takes damage, is healed or loses MP, a number pops up over it, each digit bouncing up one after the
other before the number fades. Some results show a small picture instead, and a status taking hold shows its name.
Several popups on the same unit at once are spread apart. Popups far from the camera are drawn smaller and vanish
beyond a set distance.

The battle's HP and MP code posts each number popup, drawn as digit pictures from the `battle_4_c` atlas; the result
reactions post picture popups from `battle_4_p`, and a status taking hold posts a popup that writes the status's name.
A number popup with a non-zero amount and colour slot 1-3 or 5-7 can also flash its owner's row in the
party list.

## How it works

### The popup ring

The popups live in a ring of 64 records of 0x50 bytes at `[0x02B457D0]`; the byte `0x02B443C0` is the next slot.
`0x003BBCD0`, from the field set-up `0x00253A30`¹, points `0x02B457D0` at the block `0x02B443D0` and clears its
`0x1400` bytes; `0x003BBB30`, from `0x0028E190`², does the same after `0x0028FB60`.
`0x003BBD00(request)` posts one and returns the slot with bit `0x20` set, or `0xFF` when it refuses:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00253A39` |
| ² | `0x0028E1BE` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | it refuses when the ring is absent, when the next slot is still in use, and for a status word whose record `0x0035D330(0x1A, status)` has `+0x24` = `-1`; |   |
| 2 | it notes the spread positions held by the owner's popups younger than 30 frames (256 for a word) and takes position 0 when it is free; otherwise 2 when 1 is held and 2 is free, 4 when 3 is held and 4 is free, 1 when only 3 is held, 3 when only 1 is held, and 1 or 3 at random (`rand`) in every other case; |   |
| 3 | for a number with a non-zero amount and colour slot 1-3 or 5-7 it flashes the owner's party row (`0x0028FBE0` returns for the other kinds and a zero amount, an owner with no row or no list and the other slots (`0x0028FC31`, table `0x0028FC8C`), and slots 3 and 7 skip a row of kind 3; [Party list](party-list.md)); | `0x0028FBE6`-`0x0028FBF7`<br>`0x0028FC16`, `0x0028FC29`<br>`0x0029706D` |
| 4 | for a status word it pushes every live status word in the ring on, whatever its owner (their step `+0x3A` grows by 3, `0x003BBEC0`), and delays the new one until 3 frames after the latest delay `+0x44` among the owner's words not yet shown (age `+0x38` at most 0, `0x003BBECA`); with none it is not delayed; |   |
| 5 | `0x00506700` fills the record, and the spread offset `+0x14`/`+0x18` is the position's pair at `0x00D11600` times a random factor `1 + (rand() & 31) / 32`. |   |

| Position | Offset |
|---:|---|
| 0 | 0, 0 |
| 1 | -16, -16 |
| 2 | 16, 16 |
| 3 | 16, -16 |
| 4 | -16, 16 |

### The three kinds

`0x00506700(popup, request)` zeroes the record, stores the owner (`+0x00`) and its handle (`0x003589B0`, `+0x08`),
sets the step `+0x3A` to 1 and the kind `+0x3C` from the request's byte `+0x0C`:

| Kind | Posted by | Record |
|---:|---|---|
| 0, number | `0x003283D0(unit, amount, isHeal, b)` for HP ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)) and MP ([MP](../Status-Effects-And-KO/mp.md)) | the digits of the absolute amount (`0x003EFD00`) at `+0x40`, their count `+0x3F`, the atlas `battle_4_c` (`0x0024A5A0`), the colour `0x002DD7E0(0x00D227A8[colour])` at `+0x0C` and its palette `0x002DD7B0` at `+0x3D` |
| 1, picture | `0x00328480(unit, frame)`, from the result reactions `0x00307300` (frames 0, 2, 4 and 5) and the auto-attack start `0x00312FA0` (frame 3) | the frame `+0x3F`, the atlas `battle_4_p`, two colours from the byte pairs at `0x00D22780` |
| 2, status word | `0x003284D0(unit, status)` ([Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md)) | step 3, the status's name (`0x002B58B0` of the record's `+0x18`) laid out by `0x002B3050`, palette 4, and the colour by the record's `+0x25`: bit `0x2` colour 1, bit `0x4` `0x12`, bit `0x8` `0xB6`, bit `0x10` `0xF3`, else grey `0x80808080` |

Where `0x00506700` takes each field from:

- a number's amount is the request's dword `+0x08`¹, and its colour slot the request's byte `+0x0D`
 ²;
- a picture's frame is the request's byte `+0x08`, and its two colours go to `+0x0C` and `+0x10`
 ³;
- a status word reads the record `0x0035D330(0x1A, status)`, the status from the request's `+0x08`⁴, keeps
  the status's low byte at `+0x3F`, stores 0 at `+0x44`, and `0x002B3050` lays the name out into `+0x40` and `+0x42`
 ⁵;
- the atlas or the name is stored at `+0x30`⁶;
- a request of any other kind gets only the fields every kind gets⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00506834` |
| ² | `0x00506874`, `0x00506888` |
| ³ | `0x005067EA`-`0x0050682F` |
| ⁴ | `0x00506760` |
| ⁵ | `0x00506779`-`0x005067E0` |
| ⁶ | `0x005067FD`, `0x00506869`, `0x00506790` |
| ⁷ | `0x0050675A` |

</details>

### Number colours

`0x003283D0(unit, amount, isHeal, b)` (167 bytes) posts nothing unless `0x002FA3B0(actor)` answers non-zero, `actor` being
the unit's `+0x10`: the actor must be less than 24.0 units from the party leader, measured with the height zeroed, or
from the leader position last stored at `0x01EEBB00` when there is no leader¹; a null actor
answers 0², and an actor of a kind other than 1 or 3, or a leader whose `+0x10` object is null or of such
a kind, counts as (0, 0, 0)³. `0x002FA3B0` is told on [Battle
log](../Battle-Actions/battle-log.md).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003283E6`-`0x003283F6` |
| ² | `0x002FA3CB` |
| ³ | `0x00265052`-`0x0026505C` |

</details>

`0x003283D0` then fills a request on its stack with the actor at `+0x00`, the absolute value of `amount` as the dword
`+0x08`¹, the kind 0 at byte `+0x0C` and the colour slot at byte `+0x0D`, and posts it with
`0x003BBD00(request)`, returning that call's answer²; when `0x002FA3B0` answers 0 it posts nothing
and returns that 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032840C`-`0x00328418` |
| ² | `0x00328408`-`0x00328476` |
| ³ | `0x003283F4`-`0x00328407` |

</details>

`0x003283D0` picks the colour slot from `0x01EED300[(isHeal x 2 | b) + side]`, where `side` is 4 when the unit's `+0x698`
record is absent or its byte `+5` is set and `0x00263C20(actor)` does not return 3, and 0 otherwise¹. The slot names an entry of the menu colour table through `0x00D227A8`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032841C`-`0x00328455` |

</details>

| `isHeal`, `b` | side 0 slot | colour | side 4 slot | colour |
|---|---:|---|---:|---|
| damage, 0 | 2 | `0x11` | 6 | `0x12` |
| damage, 1 | 4 | `0x11` | 8 | `0x12` |
| heal, 0 | 1 | `0x13` | 5 | `0x13` |
| heal, 1 | 3 | `0x13` | 7 | `0x13` |

### Ageing

`0x003BBA60` runs once per 60 fps tick from the subsystem pump
([Subsystem update flags](../Engine-Core/subsystem-update-flags.md)).
With no ring `[0x02B457D0]` it does nothing, the alpha included¹.
While bit `0x2` of the update word `0x01EFE31C` is set (`0x003BBF90`, from `0x002547C0`), it steps each live popup with
`0x00505500` and frees it when that returns 1:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BBA64`-`0x003BBA6E` |

</details>

- a number or picture adds its step `+0x3A` to its age `+0x38` and ends past age 37;
- a status word first waits out its delay `+0x44`, then ages by 6 a frame up to 128 and by its step after that,
  ending past 256.

The same call moves the layer's alpha `0x01EFE320` by 0.2 toward 1.0 while bit `0x2` of `0x01EFE31D` is set and toward 0
otherwise.
A live popup is one whose owner `+0x00` is set, and freeing it stores 0 in the owner and in the handle `+0x08`¹. The alpha is kept between 0 and 1.0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BBA93`, `0x003BBAAE`-`0x003BBAB4` |
| ² | `0x003BBAF9`-`0x003BBB21` |

</details>

### Drawing

`0x003BBB60` draws nothing while the layer's alpha is 0 and `0x01EFE31D` bit `0x2` is clear. Otherwise it walks the ring from
the newest popup: status words through `0x0028A090` into the screen-space list¹, numbers and
pictures through `0x00505560`, which jumps on the kind `+0x3C` to `0x00505E00` (0, a number) or `0x00505570` (1, a
picture). It ends with `0x0028EE10`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003F1520`, `0x003F1530` |

</details>

`0x003BBB60` also draws nothing when there is no ring¹. Its walk visits all 64 slots, from the one before
`0x02B443C0` back to `0x02B443C0`, and skips a slot with no owner². Each status word
writes into the next of 64 `0x130`-byte entries on the stack, advanced by what `0x0028A090` returns³, and the layer's alpha goes to `0x0028A090`, `0x00505560` and `0x0028EE10`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003BBB7F` |
| ² | `0x003BBBC6`-`0x003BBBFC`, `0x003BBC3C` |
| ³ | `0x003BBC04`-`0x003BBC2B` |

</details>

### Numbers on screen

`0x00505E00(popup, alpha)` draws one number:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The opacity is `age x 32` up to age 30 and `668 - 18 x age` after, times the layer's alpha, clamped to 0-128. |   |
| 2 | The position is the owner's, or the last one kept at `+0x20` when the owner is gone. | `0x003588B0`, `0x002EA0E0` |
| 3 | Beyond 30 units from the camera `0x02AED5F0` the opacity falls by `1 - (distance - 30)`, so the number is gone past 31 units. |   |
| 4 | The spread scale is `8 / distance` clamped to 0.2-1.8 and the digit size `6 / distance + 0.3` clamped to 0.8-1.8. The digit size goes to the stack floats `rsp + 0x5C` and `rsp + 0x58` of `0x00505E00`, and half of it to `rsp + 0x54` and `rsp + 0x50`.<br>• When `0x002DDC50()` answers non-zero, the floats `rsp + 0x50`, `rsp + 0x54` and `rsp + 0x5C` are each multiplied by `0x00254A00()`, which returns 0.75; `rsp + 0x58` and the spread scale are not multiplied there. The four floats go as one 16-byte vector to `+0x20` of each digit's draw entry, `0xA0` bytes apart.<br>• `0x002DDC50` answers 1 when `0x0053DD10()` returns 1 and 0 otherwise, and `0x0053DD10` always returns 1, so that test always passes. | `0x00505F92`-`0x00505FF8`<br>`0x00505FFB`-`0x00506015`<br>`0x0050601B`-`0x0050605D`<br>`0x00506167`-`0x0050616C`, `0x005065AA`<br>`0x002DDC54`-`0x002DDC61` |
| 5 | Digit `i` is raised by `0x00D227D0[clamp(age - i, 0, 17)]`, so each digit bounces one frame after the one before, and the next digit is placed 12 times the multiplied size `rsp + 0x5C` to the right. | `0x005065B1`-`0x005065C0` |

```
0x00D227D0  0 2 10 18 25 30 32 30 25 18 10 2 0 -2 -4 -2 -1 0
```

`0x002EA0E0(id, out)` asks `0x003588B0(id)` for the actor again. With an actor whose slot pointer
`+0xC0` is not null and whose slot's first dword is not -1, it takes the slot's first word,
sign-extended¹, as an index into the `0x740`-byte render records at `[0x022C6F28]`; for a
record whose dword `+0x284` is not 0 it calls `0x003E5910(record, out)` and then stores 1.0 in
`out + 0xC`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EA10D` |
| ² | `0x002EA0E9`-`0x002EA132` |

</details>

For an index word of `0xFFFF`, a record address of 0 or a `+0x284` of 0, `0x002EA0E0` stores only the 1.0
and leaves the first three floats as they were¹. With no actor, no
slot or a first dword of -1 it stores 0, 0, 0 and 1.0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EA107`-`0x002EA128`, `0x002EA147` |
| ² | `0x002EA13F`-`0x002EA147` |

</details>

`0x00505570` draws a picture with one sprite:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The opacity is `age x 16` up to age 30. After that it is the colour's alpha byte `+0x0F` less `(((a - a/7) / 2 + a/7) / 4) x (age - 30)`, 18 a frame for `a` = 128, and it never rises above that alpha byte. |   |
| 2 | The size is `6 / distance + 0.3` clamped to 0.8-1.2, times a scale from the 18 floats at `0x00D22800`: x uses index `min(age, 17)` and y and z use `min(age + 4, 17)`. The floats are 1.8, 1.7, 1.6, 1.5, 1.4, 1.35, 1.3, 1.25, 1.2, 1.15, 1.1, 1.05, then 1.0 for indices 12 to 17. | `0x00505620`, `0x00505641`, `0x005057F0`, `0x00505815` |
| 3 | The height comes from `0x00D227E8[min(age + 4, 17)]`, 18 signed bytes: 0, 2, 10, 18, 25, 30, 32, 30, 25, 18, 10, 2, 1, then 0 for indices 13 to 17. | `0x00505800` |
| 4 | Its four corners alternate the two colours. |   |

## Layouts

<details>
<summary>Show the memory layouts</summary>

`BattlePopup` (`0x50` bytes, offsets from the start of the [0x02B457D0]+i*0x50):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | owner | the unit; 0 for a free slot |
| `+0x08` | `u32` | handle | `0x003589B0` of the owner |
| `+0x0C` | `u32` | colour | menu colour table entry (`0x002DD7E0`) |
| `+0x10` | `u32` | colour2 | second colour of a picture |
| `+0x14` | `f32` | offsetX | spread offset |
| `+0x18` | `f32` | offsetY | spread offset |
| `+0x20` | `f32[3]` | position | last owner position |
| `+0x30` | `void*` | atlas | battle_4_c, battle_4_p or the status text |
| `+0x38` | `i16` | age | frames shown |
| `+0x3A` | `i16` | step | age added per frame |
| `+0x3C` | `u8` | kind | 0 number, 1 picture, 2 status word |
| `+0x3D` | `u8` | palette | `0x002DD7B0` of the colour; 4 for a status word |
| `+0x3E` | `u8` | spread | position 0 to 4 |
| `+0x3F` | `u8` | count | digits, picture frame or status |
| `+0x40` | `char[8]` | text | kind 0: the digits; kind 2: `0x002B3050` writes `+0x40` and `+0x42` and `+0x44` is the delay |

</details>

## Modding notes

- A number or picture lasts 38 frames at step 1; a status word takes 22 frames after its delay to reach
  age 132, then grows by its step until it passes 256.
- Popups beyond 31 units from the camera are not drawn at all.
- The ring holds 64 popups; a post is refused while the next slot is still showing.

## Related

- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md): the hit and heal numbers.
- [MP](../Status-Effects-And-KO/mp.md): the MP numbers.
- [Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md): the status words.
- [Party list](party-list.md): the row flash a number popup starts.
- [Subsystem update flags](../Engine-Core/subsystem-update-flags.md): the pump that ages them.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 5 calls with 2 other topics</summary>

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0053DD10`](../Scripts-And-Script-Commands/event-scenes.md) Input device: query availability state always1 (on event scenes) | is called by | [`0x0022B6E0`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |

**Controls and input** (explained on [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0053DD10`](../Scripts-And-Script-Commands/event-scenes.md) Input device: query availability state always1 (on event scenes) | is called by | [`0x002E09A0`](menus.md) (on menus)<br>[`0x0035FCA0`](../Controls-And-Input/vibration.md) (on vibration)<br>[`0x0035FDD0`](../Controls-And-Input/controls.md) (on controls)<br>[`0x0046DD50`](../Game-Files-And-Data-Tables/file-size-tables-fst.md) (on file size tables fst) |

</details>
