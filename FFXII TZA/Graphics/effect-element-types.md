---
title: "Effect element types: the handlers of every element type, what the verified types draw or change, and the kind-0x54 mesh record"
kind: "system"
category: "Graphics"
addresses: "002F2D60, 002F2530, 00500470, 00442550, 0039C550, 004427D0, 0039C4C0, 0039D890, 0039D970, 0039D5A0, 0039D6C0, 01EFAC20, 02AEE900, 02AEE908, 004490D0, 00501A50, 00502280, 00502EA0, 004434D0, 00444340, 00449AB0, 004355D0, 00377190, 02ADBFE0, 00377230, 004640A0, 003AB960, 0047BE20, 003D7FF0, 00465690, 00465CD0, 003D92C0, 02092628, 00436D00, 003AA280"
---

## What the player sees

Each piece of an effect has a type that decides what it is: a dot of light, a streak, an animated
sprite, a textured ring or dome, a model mesh, a trail of sprites, or something that draws nothing
itself but changes the scene, such as a light on the characters or a colour change on chosen
characters. The type is authored in the effect file, one byte per element definition.

## How it works

### Where the type comes from

An element definition is an `0xA00` record; its header byte `+0x0E` is the type, copied to the
definition's `+0x44` by `003A9A70` and to the element's byte `+0` at birth by `002F2D60`
(`002F30F2`–`002F30F6`). How the five method tables dispatch on it, and when each method runs, is on
[effect element runtime](effect-element-runtime.md); the record grammar is on
[effect files](effect-files-efx-efb.md).

The tables give 65 types an arm, with 248 distinct handlers. Types `0x00`–`0x0A`, `0x40`, `0x41`,
`0x60`–`0x67`, `0x80`–`0x97`, `0xA0`–`0xA2`, `0xA5`, `0xD0` and `0xD1`, except `0x09`, `0x63`, `0x64`
and `0x93`, are main-range types (47);
`0x42`, `0x68`–`0x74` and `0xA3`–`0xAB` are reached only through the sub-range tables (18). The
full decode is in `effect-element-types-effect-type-methods.tsv`.

Every birth method except `0x70`'s calls the base birth `002F2D60`, and every update method except
`0x70`'s calls the base update `002F2530`. Most updates add a type tail: type 1's `004424E0` is
`002F2530` then `00442600`. Types `0x41` and `0xD0` share `00464F10`, a jump to the base alone. The
tails end in the cull, release and spawn fork of the runtime page. The base setup is `00500470`.

In the tables below "Authored" is the number of `0xA00` definitions of the type over every shipped
stream, then the number of archive files holding them; a sub-range type's handlers are its
sub-range ones.

### Types 0x00 to 0x0A

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x00` | `002F2D60` | `002F2530` | - | `00500470` | - | 1,446 / 458 |
| `0x01` | `00442520` | `004424E0` | `00442550` | `00538A60` | - | 476 / 370 |
| `0x02` | `00448DE0` | `00448D70` | `004490D0` | `00538AB0` | - | 7,523 / 1,141 |
| `0x03` | `004427A0` | `00442760` | `004427D0` | `00538B80` | - | none |
| `0x04` | `00445310` | `004452D0` | `004453D0` | `00538C80` | - | 173 / 81 |
| `0x05` | `00449970` | `00449930` | `00449AB0` | `00538DB0` | - | 5,204 / 1,115 |
| `0x06` | `00446F60` | `00446F20` | `00447020` | `00538EB0` | - | 25 / 9 |
| `0x07` | `00447E10` | `00447DD0` | `00447ED0` | `00538EB0` | - | none |
| `0x08` | `0044A5F0` | `0044A5B0` | `0044A620` | `00539030` | - | none |
| `0x0A` | `0044BA80` | `0044BA40` | `0044BAC0` | `00539170` | - | 40 / 39 |

- `0x00` has no draw method: it moves and fires spawn slots only.
- `0x01` is a point. Its draw sets `02AEE908` to the integer track at definition `+0x30` and
  `02AEE900` to definition byte `+0x49 >> 5`, then calls `0039C550` (`004425B2`–`004425E8`), which
  projects the point and emits a one-vertex `GiPrim` (kind 0 in the blended emitter, `0039DA7A`).
- `0x03` is a line: its draw calls `0039C4C0` (`004427D0`), which projects both ends, drops the line
  when either end is rejected, and emits a two-vertex `GiPrim` of kind 1 (`0039C4EB`–`0039C52B`,
  `0039D769`, `0039D83C`).
- `0x02` and `0x0A` draw sprite frames through `00501A50` and `00502280` (`004490D0`, `0044BAC0`).
  Both frame drawers pick a row of a kind-`0x50` record with `00502EA0`.
- `0x04`, `0x06` and `0x07` share the grid emitters `004434D0` and `00444340`, which all three draws
  call.
- `0x05` draws a mesh; see "Type 0x05 and the mesh record" below.
- `0x06` and `0x07` share one setup, `00538EB0`.

### The point and line blend modes

`02AEE900`, definition byte `+0x49` bits 5–7, picks the emitter. Mode 0 builds the primitive and
submits it at once (`0039D890` for a point, `0039D5A0` for a line). Modes 1 to 7 append a draw-list
entry first and set the primitive's blend word: `01EFAC20[mode]`, or in mode 6 the `+0x30` track
value from `02AEE908` (`0039DA89`–`0039DAAC`, `0039D859`–`0039D875`).

| Mode | Blend word |
|---:|---|
| 0 | none: the immediate emitter |
| 1 | `0x48` |
| 2 | `0x42` |
| 3 | `0x44` |
| 4 | `0x49` |
| 5 | `0x46` |
| 6 | the `+0x30` track value |
| 7 | `4` |

### Sprite rows: 00502EA0

`00502EA0(record, index, mode)` returns the index-th row, among the rows of `0x90` bytes from
record `+0x10` whose byte `+0x70` has bit 0 set. Mode 0 first clamps the index to `[+0x3C] − 1`,
mode 1 takes it modulo `[+0x3C]`, mode 2 accepts it up to the row count `+0x38`, and any other mode
returns 0; no match returns 0 (`00502EA0`–`00502F21`).

### Type 0x05 and the mesh record

`00449AB0` draws one mesh. When definition byte `+0x590` has bit 4 clear, the mesh index `+0x294`
is the integer part of the float track at definition `+0x190`, or 0 when that is not positive or
not below 32 (`00449DA7`–`00449DF9`). It publishes the blend pair as the point does and passes the
handle `[definition + 0x5A0 + index × 4]`, decoded, to the model composer `004355D0`
(`0044A11C`–`0044A15B`). The handles are kind-`0x54` records.

### Types 0x40 to 0x42

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x40` | `00463FF0` | `00463FB0` | `00464090` | `0053AAC0` | `00464050` | 2,254 / 744 |
| `0x41` | `00464B30` | `00464F10` | `00464BC0` | `0053AB10` | `00464B80` | 425 / 310 |
| `0x42` (sub) | `0047BE20` | `0047BDA0` | `0047BFA0` | `0050C450` | `0047BF70` | 613 / 350 |

These types, with `0xD0`, act on the scene instead of drawing. Their births register the element in
the 128-slot registry at `02ADBFE0` (`0x20` bytes a slot, handle `serial << 8 | slot`, element at
`+8`) through `00377190`, whose only callers are those four births. Their draw methods only set a
bit: `00464090` sets bit `0x2` of `+0x248`, `00464BC0` bit `0x1` of `+0x23C`.

`00377230` walks the registry from `MainLoop_Draw` (`0022B268`) and the menu frame (`0022B940`),
checks visibility with the group gate and the per-instance gate (`00377292`–`003772A2`), and calls
the type's apply body: `004640A0` (`0x40`), `00464BD0` (`0x41`), `0047BD30` (`0x42`) and `00465690`
(`0xD0`) (`003772EA`–`00377336`).

- `0x40` makes a light. `004640A0` fills a request and creates it with `003AB960` the first time,
  keeping the handle at `+0x244`, and updates it with `003AC920` afterwards (`00464387`–`004643A0`).
  Definition byte `+0x120` picks the request word: 1 gives `0x8001`, 2 gives `0x8006`, anything else
  `0x8002` (`004640C3`–`0046410A`). The pool is on [character lighting](character-lighting-and-shadows.md).
- `0x41`'s apply keeps a record in the 64-entry pool of `0x60`-byte records at `[02B404E0]` through
  `003B4160`.
- `0x42`'s birth reads three floats at definition `+0x124`, `+0x128` and `+0x12C` and the track group
  at `+0x80`, and takes a slot in the 32-entry, `0x60`-byte pool at `02B4D7D0` through `003D7FF0`
  (`0047BE64`–`0047BF08`).

### Types 0x60 to 0x74

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x60` | `0045BF50` | `0045BF10` | `0045BFB0` | `0053A120` | - | 84 / 22 |
| `0x61` | `0045C920` | `0045C8E0` | `0045C980` | `0053A060` | - | 9 / 7 |
| `0x62` | `0045D290` | `0045D250` | `0045D2F0` | `0053A120` | - | 2 / 2 |
| `0x65` | `0045DCA0` | `0045DC60` | `0045DD10` | `0053A1E0` | - | 169 / 44 |
| `0x66` | `0045E8C0` | `0045E880` | `0045E930` | `0053A3B0` | - | 414 / 123 |
| `0x67` | `0045FD50` | `0045FD10` | `00460170` | `0053A5D0` | `00460120` | 364 / 207 |
| `0x68` (sub) | `00522AB0` | `00522A70` | `00522D80` | `0054EB40` | - | 162 / 83 |
| `0x69` (sub) | `00523C30` | `00523BF0` | `00523D30` | `0054ED10` | - | 58 / 22 |
| `0x6A` (sub) | `00525D50` | `00525D10` | `00526080` | `0054F070` | `00526040` | 395 / 210 |
| `0x6B` (sub) | `00529200` | `005291C0` | `005294F0` | `0054F7C0` | `005294B0` | 258 / 117 |
| `0x70` (sub) | `0053DD10` | `005C5230` | `0016D6A0` | `0054F270` | `0016D6A0` | none |
| `0x71` (sub) | `0052A130` | `0052A0F0` | `0052A360` | `0054F9B0` | `0052A340` | 28 / 12 |
| `0x72` (sub) | `0052ADF0` | `0052ADB0` | `0052B080` | `0054FBE0` | `0052B060` | 89 / 47 |
| `0x73` (sub) | `0052D3B0` | `0052D370` | `0052D920` | `0054FFF0` | `0052D8E0` | 14 / 8 |
| `0x74` (sub) | `0052E430` | `0052E3F0` | `0052EA90` | `00550200` | `0052EA50` | 4 / 3 |

- `0x60` and `0x62` share the setup `0053A120`.
- `0x70` does nothing at run time: its birth `0053DD10` returns 1, its update `005C5230` returns 0,
  and its draw and release are the bare `ret 0` at `0016D6A0`. Only its setup reads the record.
- `0x67`, `0x68`, `0x6A`, `0x6B`, `0x71`, `0x73` and `0x74` update on even frames only in the
  half-rate cadence (the base update's bit set `0x341B`, on the runtime page).
- `0x63`, `0x64` and `0x6C`–`0x6F` have no arm in any table.

### Types 0x80 to 0x97

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0x80` | `0044CC10` | `00450480` | `0044CC50` | `00539320` | - | 875 / 381 |
| `0x81` | `0044D460` | `0044D420` | `0044D4A0` | `00539270` | - | none |
| `0x82` | `0044CC10` | `00450480` | `0044DD00` | `00539320` | - | 617 / 161 |
| `0x83` | `0044CC10` | `00450480` | `0044E530` | `00539320` | - | 80 / 48 |
| `0x84` | `0044ED90` | `0044ED50` | `0044EDD0` | `00539980` | - | 1,972 / 501 |
| `0x85` | `0044F930` | `0044F8F0` | `0044F970` | `005393B0` | - | 78 / 42 |
| `0x86` | `004504C0` | `00450480` | `00450550` | `005394A0` | - | 115 / 87 |
| `0x87` | `00451140` | `00450480` | `00451180` | `00539560` | - | 175 / 54 |
| `0x88` | `00451890` | `00451850` | `004518D0` | `00539610` | - | 41 / 31 |
| `0x89` | `004524C0` | `00452480` | `00452540` | `00539740` | - | 36 / 8 |
| `0x8A` | `00453110` | `004530D0` | `00453150` | `00539870` | - | none |
| `0x8B` | `004548F0` | `004548B0` | `00454930` | `00539A60` | - | 1 / 1 |
| `0x8C` | `00455390` | `0045B260` | `00455540` | `00539B30` | - | 7,509 / 910 |
| `0x8D` | `00455D70` | `00455D30` | `00455DB0` | `00539C10` | - | 1,170 / 553 |
| `0x8E` | `004566E0` | `004566A0` | `00456720` | `00539CF0` | - | 136 / 74 |
| `0x8F` | `00457E10` | `00456EF0` | `00456F30` | `00539DA0` | - | 1,663 / 383 |
| `0x90` | `00457E10` | `00456EF0` | `00457FE0` | `00539DA0` | - | 765 / 313 |
| `0x91` | `00459420` | `004593E0` | `004595C0` | `00539E90` | - | 12 / 7 |
| `0x92` | `0045A050` | `0045A010` | `0045A200` | `00539E90` | - | 84 / 45 |
| `0x94` | `00455390` | `0045B260` | `0045AEE0` | `00539B30` | - | 2,344 / 387 |
| `0x95` | `00455390` | `0045B260` | `0045B2A0` | `00539B30` | - | 456 / 226 |
| `0x96` | `00453CB0` | `00453C70` | `00453CF0` | `00539980` | - | 268 / 75 |
| `0x97` | `00455390` | `0045B260` | `0045BAD0` | `00539F80` | - | none |

The band shares handlers across types, so a type here often selects a variant rather than a class:

- `0x80`, `0x82` and `0x83` share birth, update and setup and differ in their draw.
- `0x86` and `0x87` also use the update `00450480`.
- `0x8C`, `0x94`, `0x95` and `0x97` share birth and update; the first three also share the setup.
- `0x8F` and `0x90` share birth, update and setup; `0x91` and `0x92` share the setup; `0x84` and
  `0x96` share the setup.
- `0x93` and `0x98`–`0x9F` have no arm.

### Types 0xA0 to 0xAB

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0xA0` | `00460B80` | `00460B40` | `00460BC0` | `0053A6F0` | - | none |
| `0xA1` | `00461090` | `00461050` | `00461270` | `0053A790` | `00461250` | 504 / 343 |
| `0xA2` | `00462480` | `00462440` | `00462540` | `0053A840` | - | 6,303 / 2,018 |
| `0xA3` (sub) | `00524800` | `005247C0` | `00524A50` | `0054EE70` | `00524A10` | 447 / 131 |
| `0xA4` (sub) | `005222D0` | `00522290` | `00522300` | `0054EA70` | - | none |
| `0xA5` | `004633A0` | `00463360` | `00463460` | `0053A900` | - | 36 / 20 |
| `0xA6` (sub) | `00524D70` | `00524D30` | `00524E30` | `0054EED0` | - | 359 / 178 |
| `0xA7` (sub) | `005269B0` | `00526970` | `00526A10` | `0054F1B0` | - | 14 / 14 |
| `0xA8` (sub) | `00527110` | `005270D0` | `005271D0` | `0054F350` | - | 367 / 159 |
| `0xA9` (sub) | `00528090` | `00528050` | `00528150` | `0054F520` | - | none |
| `0xAA` (sub) | `00528AF0` | `00528AB0` | `00528B50` | `0054F700` | - | 3 / 3 |
| `0xAB` (sub) | `0052BFB0` | `0052BF70` | `0052C070` | `0054FE00` | - | 7 / 4 |

`0xA1`, `0xA2` and `0xA5` are, with `0x40`, `0x41` and `0xD0`, the definition types whose emitters
are drawn even when the instance's flag byte `+0x36A` bit 0 is clear (the runtime page).

### Types 0xD0 and 0xD1

| Type | Birth | Update | Draw | Setup | Release | Authored |
|---|---|---|---|---|---|---|
| `0xD0` | `00464F20` | `00464F10` | `00465680` | `0053A9D0` | `00465120` | 1,437 / 544 |
| `0xD1` | `003D9040` | `003D9000` | `0016D6A0` | `0053AA30` | `003D90C0` | 765 / 406 |

- `0xD0` changes how chosen characters look. Its apply `00465690` works from the flag word `+0x232`
  (`004656DB`); one branch scales the scene colour `020926C0` (`00465784`–`0046578F`), and it passes
  each chosen character to `00465CD0`, which it calls from eight sites. `0xD0` and `0x41` share the
  update `00464F10`.
- `0xD1` draws nothing (its draw is `0016D6A0`). Its update tail `003D92C0` publishes the element at
  `02092628` (`003D9698`); `00258B90`, which the field frame runs with its camera work
  ([frame update order](../Engine-Core/frame-update-order.md)), copies it into the block at
  `02096FA0` and clears the pointer (`00258C3B`–`00258D4D`).

### The kind-0x54 mesh record

A mesh is an `0xB00` record of kind `0x54`: a `0x190`-byte object built by `004354E0` and loaded by
`00436D00(object, payload)`, which first calls the kind's destroy body `004352C0` (`00436D20`). The loader copies each array into a new block unless the object's `+0x18C` has bit
`0x8`, in which case it keeps a pointer into the stream (`00436D98`–`00436DDE`).

The id bytes name kind-`0x52` texture records: each is resolved through
`003AA280(key, 0x52, id)` with the record's own key word, into the handle array at `+0x184`
(`004370B8`–`004370FE`).

## Layouts

Kind-`0x54` payload (from `00436D00`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | flags: bits 0-2 -> object +0x18C; bit 0 adds the index lists |  |
| `02` | `u16` | triangles | -> +`0x10` |
| `04` | `u16` | quads | -> +`0x12` |
| `06` | `u16` | positions | -> +`0x14`, array +`0x20`, 16 bytes each, w set to 1.0 |
| `08` | `u16` | vectors | -> +`0x16`, array +`0x24`, 16 bytes each |
| `0A` | `u16` | 4-byte entries | -> +`0x18`, array +`0x28` |
| `0C` | `u16` | 8-byte entries | -> +`0x1A`, array +`0x2C` |
| `0E` | `u16` | id bytes | -> +`0x1C`, ids +`0x180`, handles +`0x184` (8 bytes each) |
| `10` | `u16` | 20-byte records | -> +`0x1E`, copied inline to +`0x30` |
| `12` | `positions,` | vectors, | 4-byte, 8-byte and 20-byte arrays in that order; with flags bit 0, two index lists of 6 x triangles + 8 x quads bytes (+`0x170`, +`0x174`); then one byte per triangle and quad (+`0x188`); then the id bytes |

Element fields the verified draws read:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `044` | `i32` | track frame, the time every track is sampled at |  |
| `1F0` | `u32` | colour |  |
| `230` | `vec` | point 1 (types 0x01, 0x03); +0x240 point 2 (0x03) |  |
| `294` | `i32` | mesh index (0x05) |  |

Definition fields the verified draws read:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `030` | `blend` | track | (mode 6) and alpha percent |
| `044` | `u8` | element type |  |
| `049` | `u8` | bits 5-7 blend mode |  |
| `190` | `mesh-index` | track | (`0x05`); +`0x590` u8 bit 4 mesh-index mode; +`0x5A0` u32[32] mesh handles |

## Shipped data

| Fact | Value |
|---|---|
| element definitions | 48,868 `0xA00` records over 4,229 streams, 55 distinct types |
| types with code and no shipped definition | `0x03`, `0x07`, `0x08`, `0x70`, `0x81`, `0x8A`, `0x97`, `0xA0`, `0xA4`, `0xA9` |
| most used | `0x02` 7,523; `0x8C` 7,509; `0xA2` 6,303; `0x05` 5,204; `0x94` 2,344; `0x40` 2,254 |
| used once | `0x8B` |
| kind-`0x54` records | 2,733; flags `0x07` and key 0 in all; slot bytes 1 to 15 and 20 |
| kind-`0x54` sizes | the layout above plus 0 to 15 bytes of padding fills every record's chunk |
| kind-`0x54` arrays | 20-byte count 0 in all; 8-byte count equal to the 4-byte count in all |
| kind-`0x54` id bytes | 0 in 2,275 records, 1 in 444, 2 in 14; all 472 name a kind-`0x52` record of key 0 in the same stream |
| type-`0x05` definitions | 5,204; mesh slots filled at `+0x570`: one in 4,304, two in 898, three in 1, none in 1 |
| type-`0x05` mesh ids | all 6,103 equal the slot byte of a kind-`0x54` record in the same stream |

The per-type counts are in `effect-element-types-type_census.tsv`, which matches this census row
for row. `effect-element-types-effect-type-authored-usage.tsv` is an earlier, smaller census whose
counts this page supersedes. `effect-element-types-effect-mesh-54-records.tsv` (2,252 rows) and
`effect-element-types-effect-mesh-54-element05.tsv` (5,164 rows) list the mesh records and type-`0x05`
definitions of the `.efx` files one per row.

## Operations

One base update and one type tail per live element per simulation step; one draw call per drawn
element per frame; one apply per registered element (`0x40`, `0x41`, `0x42`, `0xD0`) per drawn
frame.

## State

The registry `02ADBFE0` (128 slots), the light pool behind `003AB960`, the pools at `[02B404E0]` and
`02B4D7D0`, the blend pair `02AEE900` / `02AEE908`, and the published element `02092628`.

## Modding notes

- A definition's type byte decides everything; a type without an arm in a table gets no behaviour
  for that method, and a draw arm that is `0016D6A0` draws nothing.
- Point and line blending comes from definition byte `+0x49` bits 5–7; mode 6 takes the blend word
  from the `+0x30` track, so that track then serves as both alpha percent and blend.
- A type-`0x05` mesh index of 32 or more falls back to 0, and its definition holds 32 handles.
- The registry holds 128 elements of types `0x40`, `0x41`, `0x42` and `0xD0`; `00377190` returns 0
  when it is full.

## Related

- [Effect element runtime](effect-element-runtime.md): the method tables, birth, update, release and
  the draw passes.
- [Effect files](effect-files-efx-efb.md): the `0xA00` and `0xB00` records.
- [Character lighting and shadows](character-lighting-and-shadows.md): the light pool `0x40` uses.
- [Authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md): the tracks
  every type samples.
- [PS2 VIF1 / VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the packet path
  many draw methods end in.
