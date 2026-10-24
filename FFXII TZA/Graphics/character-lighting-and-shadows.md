---
title: "How a character is lit: the light inputs, the shadow casters and the shadow pool"
kind: "system"
category: "Graphics"
addresses: "0x02B3F528, 0x02B3F508, 0x003AB960, 0x003ABD00, 0x003ABD50, 0x003ACC10, 0x003ACAA0, 0x003AD540, 0x003AE0E0, 0x003AD830, 0x003AE4C0, 0x003ADC40, 0x003AED20, 0x002E8610, 0x02CA8110, 0x004FD4B0, 0x001F9B20, 0x006C0EB0, 0x006C15D0, 0x01F2EDC8, 0x02B40528, 0x003B6890, 0x003B56D0, 0x003B6000, 0x003B6900, 0x003B6B80, 0x003B5980, 0x02B3F570, 0x003AF340, 0x003AFBE0, 0x003AFD00, 0x003E73B0, 0x00426340, 0x002E8950, 0x002E89B0, 0x002E88A0, 0x002E8900"
---

## What the player sees

Every character is lit on its own. A light can be meant for one character only (a status tint), for
everyone but one character, for a group of characters, or anchored to the camera so it always falls
from the viewer's side. Ambient light is a contest: the highest-priority ambient wins, unless the
winner is of the additive sort, in which case the character gets the sum of the additive ambients. The
shader receives at most six directional lights. Each character also has a shadow whose strength fades
with the distance from the camera, and scripts can fix that strength or the shadow's alpha.

## How it works

### The light pool

Lights live in a pool of 128 entries of `0x70` bytes at `[0x02B3F528]`. `0x003AB960(request)` takes the
first free entry, makes its handle `counter << 8 | index` (the counter `0x02B3F504` wraps after
`0xFFFFFF`), copies the `0x50`-byte request to entry `+0x20`, and appends the entry to the list whose
head is `0x02B3F508` and tail `0x02B3F510` (previous at `+0x08`, next at `+0x10`). `0x003ABD00(handle)`
returns the request block when the handle still matches.

For the falloff kinds the create routine stores `1 / range²` from the range at request `+0x0C`: at
request `+0x30` for kinds 2 and 5, `+0x40` for kind 3, `+0x48` for kind 4. Kind 4 also gets
`1 / (+0x40 − +0x44)` at `+0x4C`, and kind 5 a squared length, a dot product and a reciprocal from its
two vectors.

`0x003ABD20` returns the request block of the first light on the list whose scope byte (request
`+0x03`) is 5, or null; `0x002F4520` uses it. The mask `0x02B3F520` that the light walk tests is set and
cleared bit by bit through `0x003ACA60` and `0x003ACA70`: `0x0036FBB0` sets bit `0x8` when it loads the
five multipliers at `0x0209A3C0`–`0x0209A3D8` from the 10-byte rows at `0x02AD9B60`, and clears it when it
resets them to 1.0.

### Choosing a character's lights

`0x003ACC10(list, out, colour scale, out ambient, record, id, placement)` walks the list. It skips a light
when `(request +7 >> 2) & (0x02B3F501 | 0x02B3F520)` is non-zero or bit `0x1` of `+7` is set. Then the scope:

| Scope `+3` | Sub `+4` | The light is taken when |
|---:|---:|---|
| 1 | 2 | there is a record and the target is this character's id |
| 1 | 8 | there is a record and the target is not this id |
| 1 | 9 | there is a record; the light is re-aimed from the camera first |
| 1 | other | always |
| 2 | 3, 4, 5 | there is a record and `0x0024E2F0` (3), `0x0024E6D0` (4) or either (5) accepts the target |
| 4 | | there is no record and the target is the id |
| 5 | | never |
| 0, 3, 6 and up | | always |

The camera-anchored light (scope 1, sub 9) gets its float at entry `+0x3C` from byte `+0x112` of the
character's object (`0x003E56C0`: 1 gives 0, 2 gives 0.25, 3 gives 0.5, anything else 1.0), and its
direction from the camera position `0x02AEDF20` to the character, normalised and turned by the pair at
request `+0x40` / `+0x44`.

By type (request `+0`):

- 6, ambient: subtype 5 makes it the multiplier for the final ambient; otherwise `0x003ACAA0` evaluates
  it, scaled by `0x02B3F51C` while `0x02B3F503` is set, then the character's ambient mode applies, an
  additive light (bit `0x1` of `+7` clear) joins the running sum, and a higher priority (`+1`), or equal
  priority and greater strength, makes it the winner.
- 7: the character's own list, fetched from record `+0x108` (`0x0037AD40`). Its entries use scope 1 sub 2
  (id match) and scope 3 with the character's group bits (`0x003AED20`: record `+0x28C`; sub 7 needs a
  shared bit, sub 6 none). Ambients are handled as above with the light scale off; the rest are taken.
- anything else is a directional kind and goes to the output list.

At the end the base ambient is the winner's colour, or the additive sum when the winner was additive;
it is multiplied by the multiplier and its alpha set to 1.0.

### The character's own adjustments

- Ambient mode, record byte `+0x5E0`: 1 blends each ambient toward the record's colour `+0x5D0` by
  `+0x5DC` (for additive ones, once on their sum at the end); 2 multiplies by `+0x5DC`. A light with
  request `+5` bit 4 is exempt.
- Light scale: the gather copies record `+0x5EC` to `0x02B3F518`; while `0x02B3F502` is set it multiplies the
  colour and strength of every light whose `+5` is below `0x80`.
- Group bits: `0x002E8610(actor, group, on)` sets or clears bit `group & 31` of the record's `+0x28C`.
  The verbs `setlightgroup` (`0x224`, `0x003404F0`) and `clearlightgroup` (`0x225`) reach it
  ([verb table](../Scripts-And-Script-Commands/verb-table.md)).

### Evaluating a light

`0x003ACAA0` forms an ambient colour by subtype, with `c` the light's colour and `s` the caller's scale:
0 or above 4 gives `c`; 1 gives `s`; 2 gives `c × s.w`; 3 gives `s × s.w`; 4 gives `c × s` per channel.
The strength is `0.299|r| + 0.587|g| + 0.114|b|` of `c`.

| Kind | Body | Shape |
|---:|---|---|
| 1 | `0x003AD540` | directional; the direction at request `+0x30`, as given or through the installed matrix |
| 2 | `0x003AE0E0` | point: colour × `1 − d² × k`, zero at or past the range |
| 3 | `0x003AD830` | point cut by a plane: zero when the light-to-character vector has a non-positive dot with the axis at `+0x30` |
| 4 | `0x003AE4C0` | spot: falloff × `min(1, (cos − [+0x44]) × [+0x4C])` |
| 5 | `0x003ADC40` | segment: the closest point on the segment, clamped to its ends, then a point light |

### The six-light block

`0x003ABD50(record, block, matrix 1, matrix 2, colour scale, use scale)` clears a `0xE0`-byte block,
sets `+0xD0` to -1, copies the record's light scale and calls the selector with the ambient written to
`+0xC0`. It sorts the chosen lights (`0x003AEBC0`), evaluates each with the first matrix when its `+5`
bits 1-3 are clear and the second otherwise, and at the end of each run of equal priority, highest
first, sorts the run's lit lights by strength (`0x003AE9C0`).

It writes up to six: directions negated and normalised, stored by component (x of lights 0-2 at `+0x00`, y at
`+0x10`, z at `+0x20`; lights 3-5 at `+0x30`..`+0x50`), colours at `+0x60 + 16i`, and the index of a
camera-anchored light at `+0xD0`. A direction too short after normalising becomes (0, -1, 0).

The model instance's draw setup `0x004FD4B0` calls it with the instance's record (`+0xF8`), matrices
(`+0xE8`, `+0xF0`) and colour (`+0x90`) into the global block `0x02CA8110`, then scales the ambient: rgb
by instance `+0xA0`..`+0xA8`, alpha by `+0xAC × (+0xB0 / 4096)` and, with `+0x244` bit `0x1`, by `+0x248`.
That is how a character's fade and script colour reach its lighting ([character fades](character-fades.md)).

### The installed light matrix

Before it evaluates each light, `0x003ABD50` copies its first matrix (light `+5` bits `0xE` clear) or its second into the
64 bytes `0x02B3F4B0`-`0x02B3F4EF` (`0x003ABE86`-`0x003ABEDD`); `0x003AC110` copies its matrix the same way (`0x003AC470`-`0x003AC49C`).
The light bodies read it element by element: the directional body `0x003AD540` turns the direction by rows 0 to 2,
and the point, plane, segment and spot bodies also take row 3.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B3F4B0` | `f32[4]` | 0 (zero-filled tail of `.data`) | row 0 of the light matrix | `0x003ABD50` (`0x003ABE91`, `0x003ABEB9`); `0x003AC110` (`0x003AC47B`) | `0x003AD540` (`0x003AD722`, `0x003AD770`, `0x003AD797`); `0x003AD830` (`0x003AD9C8`, `0x003ADA06`, `0x003ADA41`); `0x003ADC40` (`0x003ADECA`, `0x003ADF05`, `0x003ADF3D`); `0x003AE0E0` (`0x003AE274`, `0x003AE2B2`, `0x003AE2ED`); `0x003AE4C0` (`0x003AE674`, `0x003AE6B3`, `0x003AE6EF`) |
| `0x02B3F4C0` | `f32[4]` | 0 (zero-filled tail of `.data`) | row 1 of the light matrix | `0x003ABD50` (`0x003ABE9C`, `0x003ABEC5`); `0x003AC110` (`0x003AC486`) | `0x003AD540` (`0x003AD72F`, `0x003AD756`, `0x003AD78A`); `0x003AD830` (`0x003AD9D8`, `0x003ADA13`, `0x003ADA4E`); `0x003ADC40` (`0x003ADED5`, `0x003ADF0D`, `0x003ADF45`); `0x003AE0E0` (`0x003AE284`, `0x003AE2BF`, `0x003AE2FA`); `0x003AE4C0` (`0x003AE685`, `0x003AE6C0`, `0x003AE6FC`) |
| `0x02B3F4D0` | `f32[4]` | 0 (zero-filled tail of `.data`) | row 2 of the light matrix | `0x003ABD50` (`0x003ABEA7`, `0x003ABED1`); `0x003AC110` (`0x003AC491`) | `0x003AD540` (`0x003AD73C`, `0x003AD763`, `0x003AD7A4`); `0x003AD830` (`0x003AD9E9`, `0x003ADA24`, `0x003ADA5F`); `0x003ADC40` (`0x003ADEE9`, `0x003ADF21`, `0x003ADF59`); `0x003AE0E0` (`0x003AE295`, `0x003AE2D0`, `0x003AE30B`); `0x003AE4C0` (`0x003AE696`, `0x003AE6D1`, `0x003AE70D`) |
| `0x02B3F4E0` | `f32[4]` | 0 (zero-filled tail of `.data`) | row 3 of the light matrix | `0x003ABD50` (`0x003ABEDD`); `0x003AC110` (`0x003AC49C`) | `0x003AD830` (`0x003AD98D`, `0x003AD99F`, `0x003AD9B1`); `0x003ADC40` (`0x003ADD9F`, `0x003ADDAC`, `0x003ADDBA`, `0x003ADDF7`, `0x003ADE07`, `0x003ADEA3`, `0x003ADEB4`); `0x003AE0E0` (`0x003AE239`, `0x003AE24B`, `0x003AE25D`); `0x003AE4C0` (`0x003AE63A`, `0x003AE64B`, `0x003AE65D`) |

### The map's character-light settings

Render-object slot 8, `0x001F9B20(object, block, f)`, copies the block into every part record's
`lichtAmbient`, `lichtDir1`-`6`, `lichtColor1`-`6` and `sunIndex` (the `+0xD0` index when it is -1 to 5).
Unless the settings flag at `0x001EBA40()` `+0x118` is set:

- the ambient becomes `rgb × mMapChrAmbientIntensity + mMapChrAmbientOffset` (`0x01F82ED8`, `0x01F82EE8`);
- each light's colour is multiplied by `mMapChrDirLightColorIntensity` (`0x01F82EF8`);
- when `0x001EC560()` is 0, a light within the upward threshold of straight up (`0x01DFE198` degrees; the
  test is skipped above 89) is also multiplied by `0x01DFE19C`; both are the `mMapChrUpwardDirLight*`
  settings.

The settings are listed on [graphics settings](../Engine-Core/graphics-settings.md).

### Event lights

An event script can hold up to 16 lights of its own in entries of `0x70` bytes at `0x02B58C50`. Each
entry keeps a copy of its light request; the light itself lives in the pool. Every verb takes the
entry index first.

`EventLight` (`0x70` bytes, offsets from the start of the 0x02B58C50+0x70*n):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle | the pool handle, 0 for none |
| `+0x04` | `u8` | manager | the manager byte of the bindl issuer |
| `+0x05` | `u8` | focus | 1 follows the party focus |
| `+0x08` | `void*` | binder | the actor that ran bindl |
| `+0x10` | `void*` | followed | the actor of seteventlightactor |
| `+0x20` | `u8[80]` | request | copy of the light request |

The defaults of the copy are type 2, priority `0xC0`, scope 1 sub-kind 1, bit `0x1` of `+0x05` set,
range 10.0, colour (1, 1, 1, 0), position w 1.0 and direction (1, 1, 1, 1).

- `bindl(n, kind)` (`0x0136`, `0x003DE4C0`) unbinds whatever the calling actor held (`0x0025AB30`),
  releases the entry's old light (`0x003ABCA0`), and files a new one (`0x003AB960`) from the entry's
  request with type 2 for `kind` 1, 4 for `kind` 2 and 1 otherwise. It keeps the handle, the issuer's
  manager byte and the actor, marks the actor bound (its `+0x04` = 2, `+0x05` = `n`) and then resets
  the entry's copy to the defaults.
- `seteventlighttype(n, type)` (`0x0138`, `0x003DE7E0`) resets the copy to the defaults with that type
  byte; type 4 also gets the cone cosines `cos(π/8)` and `cos(π/4)` at request `+0x40` and `+0x44`.
- `seteventlightall(n)` (`0x0139`, `0x003DE970`) sets scope sub-kind 1 and drops the followed actor;
  `seteventlightactor(n, id)` (`0x0137`, `0x003DEA20`) sets sub-kind 2 and follows the actor `id`
  names (`0x003587C0`), or the party focus for a negative `id`.
- `seteventlightcolor(n, r, g, b)` (`0x013A`, `0x003DE9B0`) stores the colour with alpha 0;
  `seteventlightdir(n, a, b)` (`0x013C`, `0x003DEA70`) turns the unit z vector by the two angles,
  normalises it (`0x003A1890`) and stores it at request `+0x30`.
- `seteventlightrange(n, r)` (`0x013B`, `0x003DEAC0`), only for an entry with a type, stores `r` at
  request `+0x0C` and clears bit `0x1` of `+0x05`; a negative `r` sets the bit and stores 1.0 instead.
- `seteventlightcorn(n, inner, outer)` (`0x0144`, `0x003DE8A0`) stores `cos(inner)` and `cos(outer)` at
  request `+0x40` and `+0x44`, with `inner` at least 0 and `outer` at least `inner`.

The colour, direction, range and cone setters also write the live request when the entry has a
light and a bound actor, the last two through `0x003AC920`. Each frame `0x003DE640` (from `0x00314020`)
sets every live light's target `+0x08` to the record index of the followed actor (`0x002E97B0`) and,
when the binding actor's class bits (`+0x03 & 0xE0`) are `0x60`, its position `+0x20` from that actor
(`0x00265020`), with w = 1.0.

`0x0025AB30` undoes a binding by the actor's kind byte `+0x04`: kind 2 runs `0x003DE5F0`, which releases
the light and clears the entry's handle, actor and focus flag; kinds 1 and 3 run `0x002E3AF0` and
`0x002E3D00`. The area initialiser `0x00266D10` resets all 16 entries through `0x003DE710`.

### Script ambient colours

The map draw `0x002F4520` takes its ambient from `0x0209A3B0` (`0x002F4688`), which `0x0026E1A0` rebuilds once
a frame (from `0x0036F410`) as the product, component by component, of four colours: the map's
ambient `0x0209A370`, the scene colour `0x0209A380` (copied from `0x020926C0` by `0x003769E0`), the script
colour `0x0209A390` and the summon-colour multiplier `0x0209A3C0`. `0x0026E1D0` resets the scene colour,
the script colour and the product to 1.0.

- `setmapambient(r, g, b, a)` (`0x0104`, `0x00379080`) stores the script colour and also writes
  `r, g, b` into the ambient of all five light groups (`0x02EBF460 + 0x50 × g`, `0x002ECE40`);
  `setmapambient_maponly` (`0x050A`, `0x00379110`) stores only the script colour.
- Their three-argument forms (`0x0105`, `0x050B`) push 1.0 as `a`; `resetmapambient` (`0x0106`,
  `0x00346D20`) stores 1.0 four times through `0x00379080`. The map teardown `0x00378230` resets it too.
- Unless `0x02ADD0E9` is set, both setters then refresh light group 0 with its current state:
  `0x003DE920(0, 0x003DE700(0), 0)`, where `0x003DE700(g)` reads bit `g` of the group mask `0x02B59350`.

### The shadow caster

`PShadowCaster` is a reflected Phyre class (`0x006C15D0` registers `m_light` at `+0x00`,
`m_shadowCasterType` at `+0x08`, `m_splits` at `+0x10`, `m_zbias` at `+0x50`). Its constructor
`0x006C0EB0` sets `m_shadowCasterType` to the first value record of `PShadowCasterType` at `0x01F2EDC8`,
named `NoShadow` (the next are `PCFShadowMap` and `CascadedShadowMap`), `m_splits` empty, `m_zbias`
1.0e-5, and initialises the state block at `+0x58` (`0x005DC400`, then bytes 1, 1, 2, 2 and `+0x74` bit `0x40`).

### The two shadow pools

A render record holds up to two shadow entries, chosen by its shadow kind (record `+0xC0` bits 3-4).
`0x00427DE0` sets the kind from `(+0x304 >> 12) & 3` through `0x003E73B0` when `+0x290` bit `0x400000` is set;
kind 1 takes a second-pool entry and kind 0 frees it, and the handle is copied to the presentation
entry's `+0x360`.

| | First pool | Second pool |
|---|---|---|
| Storage | 160 entries of `0xE0` at `[0x02B40528]` (`0x003B6890`) | 32 entries of `0x70` at `0x02B3F570` (`0x003AFCD0`) |
| Taken by | `0x003B56D0(record id)` at promotion, into `+0x114` | `0x003AF340(record id)`, into `+0x118`; needs the model's `@FCP` shadow block (`0x003E6E40`) |
| Handle | counter `0x02B40520` << 8 \| slot, checked at entry `+0x10` | counter `0x02B3F550` << 8 \| slot, checked at entry `+0x04` |
| Freed by | `0x003B6000` | `0x003AFBE0` |
| Mode | byte `+0x41`, `0x003B6900(handle, v)` = `(v >> 2 & old) \| (v & 3)` | low nibble of `+0x20`, `0x003AFD00` |
| Stored value | - | 16 bytes at `0x02B3F560`, copied in by `0x003AFD40` (called from `0x00378120` and `0x00379610`; the map pack's tag-11 colour); no code reads it back |

A first-pool entry keeps the owner's index at `+0x04`, its strength at `+0x14` (1.0) and two bones,
`+0x3C` and `+0x3E`, from the model's special bones `0x104` and `0x106` (`0x003E5AD0`).

The anchor in use is the word `+0x38`. `0x003B5CE0(handle, b, x, y)` keeps the previous base offset
`+0x48`, `+0x4C` at `+0x30`, `+0x34` and the previous anchor at `+0x3A`, stores the new base offset
and sets the anchor to `+0x3C` for `b` = 0 or `+0x3E` otherwise. `0x003B6BD0(handle, v)` stores the
offset multiplier `+0x44` and `0x003B6BB0(handle, v)` the float `+0x2C`; `0x0042D050` calls both.

`0x003B67F0(handle)`, from `0x003723B0`, puts the four ramp channels back to neutral (offset 0, extent
scales 1, rotation 0, strength 1) and clears their steps and counters, the cross-fade and the values
last built.

When the authored motion command `0x09` (`0x00417F40`) starts a motion whose header carries a
character block of kind 1, it passes the block to `0x003B5E20(handle, block)` and its anchor choice and
base offset (`+0xA8`, `+0xA0`, `+0xA4` of the header) to `0x003B5CE0`. `0x003B5E20` keeps a motion's
shadow overrides in the slot, flagged in byte `+0x40`:

- first, for each override flagged by the previous motion, it writes the kept value into the channel
  and its cross-fade copy and clears a counter: bit `0x2` the offset (`+0xA0`, `+0xA4`; counter `+0x00`),
  bit `0x4` the rotation (`+0xB0`; counter `+0x03`, the strength's), bit `0x8` the extent scales (`+0xA8`,
  `+0xAC`; counter `+0x02`), and bit `0x10` the base offset (`+0xB4`, `+0xB8` into `+0x48`, `+0x4C`);
- then, when the block's word `+0x32` is non-zero, it keeps the new values (block `+0x4C`, `+0x50`;
  `+0x10`, `+0x54`; `+0x58`, `+0x5C`; the rotation as `(word >> 6)` degrees) and copies the word's
  bits `0x1`, `0x2`, `0x8`, `0x4`, `0x10` and `0x20` into the flags' bits 1 to 6; it ends by clearing the four counters.

### Each frame

`0x00426420` runs `0x00426340` on every active record while tail `+0x42` is 1 and `+0x43` is 0:

1. it puts both entries in their off state (`0x003B6900(h, 6)`, `0x003AFD00(h, 0)`);
2. it stops unless `+0x284` bits `0x4`, `0x40`, `0x80` and `0x1000` are set, the record has no parent and `+0x2AE` bit `0x2`
   is clear;
3. kind 0 with a first-pool entry: `0x003B6900(h, 4)`, then the strength (`0x003B6B80`) is record `+0x27C`
   when `+0xC0` bit `0x2` is set, otherwise `0x003B5980(h)`;
4. kind 1 with a second-pool entry: `0x003AFD00(h, 1)`.

`0x003B5980` measures the distance `d` from the entry's bone (`0x00421FF0`) to the camera position
`0x02AEDF20` and returns `clamp(1 − (clamp(d, near, far) − near) × k, 0, 1)`, with `near`, `far` and `k`
at `+0x20`, `+0x24` and `+0x2C` of the model's `@FCP` block (`0x003E6F70`). The 1 and the zero bias inside the
inner clamp are the cells `0x01EF93FC` (1.0) and `0x01EF93F0` (0.0), which `0x0036D990` sets at boot.

`0x003AF460`, from the character pass `0x00426090`, advances the second pool's ramps: for each of the 32
entries with a handle it counts down five counters (`+0x1C`, `+0x1D`, `+0x1E`, `+0x54`, `+0x55`) and,
while one is non-zero, adds its step to its value (`+0x24` by `+0x2C`, `+0x28` by `+0x30`, `+0x34` by
`+0x38`, `+0x3C` by `+0x48`, `+0x44` by `+0x4C`).

### The shadow verbs

- `setshadowlod` (`0x286`, `0x00342CF0`): `0x002E8950(actor, 1)` sets `+0xC0` bit `0x2` and `0x002E89B0` stores
  the value, clamped to 0..1, at `+0x27C`. `clearshadowlod` (`0x287`) clears the bit.
- `setshadowalpha` (`0x284`, `0x00342410`): `0x002E88A0(actor, 1)` sets `+0xC0` bit `0x4` and `0x002E8900` stores
  the value at `+0x274`. `clearshadowalpha` (`0x285`) clears the bit.

Each finds the record through the actor's `+0xC0` context, whose first word is the record index. Every
access to the two structures found is in [the shadow caster](character-lighting-and-shadows-pshadow-caster-accesses.tsv)
and [second pool](character-lighting-and-shadows-shadow-pool-v2-slot-accesses.tsv) tables.

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PShadowCaster` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x20` | `u8[48]` | bytes20 | `+0x20` to `+0x4F`; no registered member covers it (`0x006C0D50` registers the `0x80`-byte class at `0x006C0DA0`) |

### Light requests and shadow records

The structures below are the ones the mechanisms above use.

A light request (entry `+0x20`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | type: 1-5 directional kinds, 6 ambient, 7 the character's own list |  |
| `+0x01` | `u8` | priority |  |
| `+0x02` | `u8` | subtype (ambient colour form; 5 = multiplier) |  |
| `+0x03` | `u8` | scope |  |
| `+0x04` | `u8` | scope sub-kind |  |
| `+0x05` | `u8` | bit 0x10 no ambient mode; bits 1-3 matrix; 0x80 and up no light scale |  |
| `+0x07` | `u8` | bit 0x1 exclusive (not additive); bit 0x2 skip; bits 2-7 class |  |
| `+0x08` | `u32` | target: id, handle or group mask |  |
| `+0x0C` | `f32` | range |  |
| `+0x10` | `f32[4]` | colour |  |
| `+0x20` | `...` | kind data (position, axis, cone, segment end) |  |

## Modding notes

- The cap is six directional lights per character after priority; a seventh never reaches the shader.
- An exclusive ambient of the highest priority silences every other ambient on that character.
- Group numbers wrap at 32: group 32 is bit `0x1` again.

## Related

- [CharacterRenderObject](character-render-object.md): slot 8 and the part records.
- [Character render records](character-render-records.md): the record fields and promotion.
- [Character fades](character-fades.md): the instance fields that scale the ambient.
- [Character status visuals](character-status-visuals.md): the status lights.
- [Graphics settings](../Engine-Core/graphics-settings.md): `mMapChr*` and the shadow object.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the light-group and shadow verbs.
