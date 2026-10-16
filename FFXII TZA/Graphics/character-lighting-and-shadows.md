---
title: "How a character is lit: the light inputs, the shadow casters and the shadow pool"
kind: "system"
category: "Graphics"
addresses: "02B3F528, 02B3F508, 003AB960, 003ABD00, 003ABD50, 003ACC10, 003ACAA0, 003AD540, 003AE0E0, 003AD830, 003AE4C0, 003ADC40, 003AED20, 002E8610, 02CA8110, 004FD4B0, 001F9B20, 006C0EB0, 006C15D0, 01F2EDC8, 02B40528, 003B6890, 003B56D0, 003B6000, 003B6900, 003B6B80, 003B5980, 02B3F570, 003AF340, 003AFBE0, 003AFD00, 003E73B0, 00426340, 002E8950, 002E89B0, 002E88A0, 002E8900"
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

Lights live in a pool of 128 entries of `70`<sub>h</sub> bytes at `[02B3F528]`. `003AB960(request)` takes the
first free entry, makes its handle `counter << 8 | index` (the counter `02B3F504` wraps after
`FFFFFF`<sub>h</sub>), copies the `50`<sub>h</sub>-byte request to entry `+20`<sub>h</sub>, and appends the entry to the list whose
head is `02B3F508` and tail `02B3F510` (previous at `+08`<sub>h</sub>, next at `+10`<sub>h</sub>). `003ABD00(handle)`
returns the request block when the handle still matches.

For the falloff kinds the create routine stores `1 / range²` from the range at request `+0C`<sub>h</sub>: at
request `+30`<sub>h</sub> for kinds 2 and 5, `+40`<sub>h</sub> for kind 3, `+48`<sub>h</sub> for kind 4. Kind 4 also gets
`1 / (+40h − +44h)` at `+4C`<sub>h</sub>, and kind 5 a squared length, a dot product and a reciprocal from its
two vectors.

`003ABD20` returns the request block of the first light on the list whose scope byte (request
`+03`<sub>h</sub>) is 5, or null; `002F4520` uses it. The mask `02B3F520` that the light walk tests is set and
cleared bit by bit through `003ACA60` and `003ACA70`: `0036FBB0` sets bit `8`<sub>h</sub> when it loads the
five multipliers at `0209A3C0`–`0209A3D8` from the 10-byte rows at `02AD9B60`, and clears it when it
resets them to 1.0.

### Choosing a character's lights

`003ACC10(list, out, colour scale, out ambient, record, id, placement)` walks the list. It skips a light
when `(request +7 >> 2) & (02B3F501 | 02B3F520)` is non-zero or bit 1 of `+7` is set. Then the scope:

| Scope `+3` | Sub `+4` | The light is taken when |
|---:|---:|---|
| 1 | 2 | there is a record and the target is this character's id |
| 1 | 8 | there is a record and the target is not this id |
| 1 | 9 | there is a record; the light is re-aimed from the camera first |
| 1 | other | always |
| 2 | 3, 4, 5 | there is a record and `0024E2F0` (3), `0024E6D0` (4) or either (5) accepts the target |
| 4 | | there is no record and the target is the id |
| 5 | | never |
| 0, 3, 6 and up | | always |

The camera-anchored light (scope 1, sub 9) gets its float at entry `+3C`<sub>h</sub> from byte `+112`<sub>h</sub> of the
character's object (`003E56C0`: 1 gives 0, 2 gives 0.25, 3 gives 0.5, anything else 1.0), and its
direction from the camera position `02AEDF20` to the character, normalised and turned by the pair at
request `+40`<sub>h</sub> / `+44`<sub>h</sub>.

By type (request `+0`):

- 6, ambient: subtype 5 makes it the multiplier for the final ambient; otherwise `003ACAA0` evaluates
  it, scaled by `02B3F51C` while `02B3F503` is set, then the character's ambient mode applies, an
  additive light (bit 0 of `+7` clear) joins the running sum, and a higher priority (`+1`), or equal
  priority and greater strength, makes it the winner.
- 7: the character's own list, fetched from record `+108`<sub>h</sub> (`0037AD40`). Its entries use scope 1 sub 2
  (id match) and scope 3 with the character's group bits (`003AED20`: record `+28C`<sub>h</sub>; sub 7 needs a
  shared bit, sub 6 none). Ambients are handled as above with the light scale off; the rest are taken.
- anything else is a directional kind and goes to the output list.

At the end the base ambient is the winner's colour, or the additive sum when the winner was additive;
it is multiplied by the multiplier and its alpha set to 1.0.

### The character's own adjustments

- Ambient mode, record byte `+5E0`<sub>h</sub>: 1 blends each ambient toward the record's colour `+5D0`<sub>h</sub> by
  `+5DC`<sub>h</sub> (for additive ones, once on their sum at the end); 2 multiplies by `+5DC`<sub>h</sub>. A light with
  request `+5` bit 4 is exempt.
- Light scale: the gather copies record `+5EC`<sub>h</sub> to `02B3F518`; while `02B3F502` is set it multiplies the
  colour and strength of every light whose `+5` is below `80`<sub>h</sub>.
- Group bits: `002E8610(actor, group, on)` sets or clears bit `group & 31` of the record's `+28C`<sub>h</sub>.
  The verbs `setlightgroup` (`224`<sub>h</sub>, `003404F0`) and `clearlightgroup` (`225`<sub>h</sub>) reach it
  ([verb table](../Scripts-And-Script-Commands/verb-table.md)).

### Evaluating a light

`003ACAA0` forms an ambient colour by subtype, with `c` the light's colour and `s` the caller's scale:
0 or above 4 gives `c`; 1 gives `s`; 2 gives `c × s.w`; 3 gives `s × s.w`; 4 gives `c × s` per channel.
The strength is `0.299|r| + 0.587|g| + 0.114|b|` of `c`.

| Kind | Body | Shape |
|---:|---|---|
| 1 | `003AD540` | directional; the direction at request `+30`<sub>h</sub>, as given or through the installed matrix |
| 2 | `003AE0E0` | point: colour × `1 − d² × k`, zero at or past the range |
| 3 | `003AD830` | point cut by a plane: zero when the light-to-character vector has a non-positive dot with the axis at `+30`<sub>h</sub> |
| 4 | `003AE4C0` | spot: falloff × `min(1, (cos − [+44h]) × [+4Ch])` |
| 5 | `003ADC40` | segment: the closest point on the segment, clamped to its ends, then a point light |

### The six-light block

`003ABD50(record, block, matrix 1, matrix 2, colour scale, use scale)` clears a `E0`<sub>h</sub>-byte block,
sets `+D0`<sub>h</sub> to -1, copies the record's light scale and calls the selector with the ambient written to
`+C0`<sub>h</sub>. It sorts the chosen lights (`003AEBC0`), evaluates each with the first matrix when its `+5`
bits 1-3 are clear and the second otherwise, and at the end of each run of equal priority, highest
first, sorts the run's lit lights by strength (`003AE9C0`).

It writes up to six: directions negated and normalised, stored by component (x of lights 0-2 at `+00`<sub>h</sub>, y at
`+10`<sub>h</sub>, z at `+20`<sub>h</sub>; lights 3-5 at `+30`<sub>h</sub>..`+50`<sub>h</sub>), colours at `+60h + 16i`, and the index of a
camera-anchored light at `+D0`<sub>h</sub>. A direction too short after normalising becomes (0, -1, 0).

The model instance's draw setup `004FD4B0` calls it with the instance's record (`+F8`<sub>h</sub>), matrices
(`+E8`<sub>h</sub>, `+F0`<sub>h</sub>) and colour (`+90`<sub>h</sub>) into the global block `02CA8110`, then scales the ambient: rgb
by instance `+A0`<sub>h</sub>..`+A8`<sub>h</sub>, alpha by `+ACh × (+B0h / 4096)` and, with `+244`<sub>h</sub> bit 0, by `+248`<sub>h</sub>.
That is how a character's fade and script colour reach its lighting ([character fades](character-fades.md)).

### The map's character-light settings

Render-object slot 8, `001F9B20(object, block, f)`, copies the block into every part record's
`lichtAmbient`, `lichtDir1`-`6`, `lichtColor1`-`6` and `sunIndex` (the `+D0`<sub>h</sub> index when it is -1 to 5).
Unless the settings flag at `001EBA40()` `+118`<sub>h</sub> is set:

- the ambient becomes `rgb × mMapChrAmbientIntensity + mMapChrAmbientOffset` (`01F82ED8`, `01F82EE8`);
- each light's colour is multiplied by `mMapChrDirLightColorIntensity` (`01F82EF8`);
- when `001EC560()` is 0, a light within the upward threshold of straight up (`01DFE198` degrees; the
  test is skipped above 89) is also multiplied by `01DFE19C`; both are the `mMapChrUpwardDirLight*`
  settings.

The settings are listed on [graphics settings](../Engine-Core/graphics-settings.md).

### Event lights

An event script can hold up to 16 lights of its own in entries of `70`<sub>h</sub> bytes at `02B58C50`. Each
entry keeps a copy of its light request; the light itself lives in the pool. Every verb takes the
entry index first.

`EventLight` (`70`<sub>h</sub> bytes, offsets from the start of the 02B58C50+`70`<sub>h</sub>*n):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | handle | the pool handle, 0 for none |
| `04`<sub>h</sub> | `u8` | manager | the manager byte of the bindl issuer |
| `05`<sub>h</sub> | `u8` | focus | 1 follows the party focus |
| `08`<sub>h</sub> | `void*` | binder | the actor that ran bindl |
| `10`<sub>h</sub> | `void*` | followed | the actor of seteventlightactor |
| `20`<sub>h</sub> | `u8[80]` | request | copy of the light request |

The defaults of the copy are type 2, priority `C0`<sub>h</sub>, scope 1 sub-kind 1, bit 0 of `+05`<sub>h</sub> set,
range 10.0, colour (1, 1, 1, 0), position w 1.0 and direction (1, 1, 1, 1).

- `bindl(n, kind)` (`0136`<sub>h</sub>, `003DE4C0`) unbinds whatever the calling actor held (`0025AB30`),
  releases the entry's old light (`003ABCA0`), and files a new one (`003AB960`) from the entry's
  request with type 2 for `kind` 1, 4 for `kind` 2 and 1 otherwise. It keeps the handle, the issuer's
  manager byte and the actor, marks the actor bound (its `+04`<sub>h</sub> = 2, `+05`<sub>h</sub> = `n`) and then resets
  the entry's copy to the defaults.
- `seteventlighttype(n, type)` (`0138`<sub>h</sub>, `003DE7E0`) resets the copy to the defaults with that type
  byte; type 4 also gets the cone cosines `cos(π/8)` and `cos(π/4)` at request `+40`<sub>h</sub> and `+44`<sub>h</sub>.
- `seteventlightall(n)` (`0139`<sub>h</sub>, `003DE970`) sets scope sub-kind 1 and drops the followed actor;
  `seteventlightactor(n, id)` (`0137`<sub>h</sub>, `003DEA20`) sets sub-kind 2 and follows the actor `id`
  names (`003587C0`), or the party focus for a negative `id`.
- `seteventlightcolor(n, r, g, b)` (`013A`<sub>h</sub>, `003DE9B0`) stores the colour with alpha 0;
  `seteventlightdir(n, a, b)` (`013C`<sub>h</sub>, `003DEA70`) turns the unit z vector by the two angles,
  normalises it (`003A1890`) and stores it at request `+30`<sub>h</sub>.
- `seteventlightrange(n, r)` (`013B`<sub>h</sub>, `003DEAC0`), only for an entry with a type, stores `r` at
  request `+0C`<sub>h</sub> and clears bit 0 of `+05`<sub>h</sub>; a negative `r` sets the bit and stores 1.0 instead.
- `seteventlightcorn(n, inner, outer)` (`0144`<sub>h</sub>, `003DE8A0`) stores `cos(inner)` and `cos(outer)` at
  request `+40`<sub>h</sub> and `+44`<sub>h</sub>, with `inner` at least 0 and `outer` at least `inner`.

The colour, direction, range and cone setters also write the live request when the entry has a
light and a bound actor, the last two through `003AC920`. Each frame `003DE640` (from `00314020`)
sets every live light's target `+08`<sub>h</sub> to the record index of the followed actor (`002E97B0`) and,
when the binding actor's class bits (`+03h & E0h`) are `60`<sub>h</sub>, its position `+20`<sub>h</sub> from that actor
(`00265020`), with w = 1.0.

`0025AB30` undoes a binding by the actor's kind byte `+04`<sub>h</sub>: kind 2 runs `003DE5F0`, which releases
the light and clears the entry's handle, actor and focus flag; kinds 1 and 3 run `002E3AF0` and
`002E3D00`. The area initialiser `00266D10` resets all 16 entries through `003DE710`.

### Script ambient colours

The map draw `002F4520` takes its ambient from `0209A3B0` (`002F4688`), which `0026E1A0` rebuilds once
a frame (from `0036F410`) as the product, component by component, of four colours: the map's
ambient `0209A370`, the scene colour `0209A380` (copied from `020926C0` by `003769E0`), the script
colour `0209A390` and the summon-colour multiplier `0209A3C0`. `0026E1D0` resets the scene colour,
the script colour and the product to 1.0.

- `setmapambient(r, g, b, a)` (`0104`<sub>h</sub>, `00379080`) stores the script colour and also writes
  `r, g, b` into the ambient of all five light groups (`02EBF460 + 50h × g`, `002ECE40`);
  `setmapambient_maponly` (`050A`<sub>h</sub>, `00379110`) stores only the script colour.
- Their three-argument forms (`0105`<sub>h</sub>, `050B`<sub>h</sub>) push 1.0 as `a`; `resetmapambient` (`0106`<sub>h</sub>,
  `00346D20`) stores 1.0 four times through `00379080`. The map teardown `00378230` resets it too.
- Unless `02ADD0E9` is set, both setters then refresh light group 0 with its current state:
  `003DE920(0, 003DE700(0), 0)`, where `003DE700(g)` reads bit `g` of the group mask `02B59350`.

### The shadow caster

`PShadowCaster` is a reflected Phyre class (`006C15D0` registers `m_light` at `+00`<sub>h</sub>,
`m_shadowCasterType` at `+08`<sub>h</sub>, `m_splits` at `+10`<sub>h</sub>, `m_zbias` at `+50`<sub>h</sub>). Its constructor
`006C0EB0` sets `m_shadowCasterType` to the first value record of `PShadowCasterType` at `01F2EDC8`,
named `NoShadow` (the next are `PCFShadowMap` and `CascadedShadowMap`), `m_splits` empty, `m_zbias`
1.0e-5, and initialises the state block at `+58`<sub>h</sub> (`005DC400`, then bytes 1, 1, 2, 2 and `+74`<sub>h</sub> bit 6).

### The two shadow pools

A render record holds up to two shadow entries, chosen by its shadow kind (record `+C0`<sub>h</sub> bits 3-4).
`00427DE0` sets the kind from `(+304h >> 12) & 3` through `003E73B0` when `+290`<sub>h</sub> bit 22 is set;
kind 1 takes a second-pool entry and kind 0 frees it, and the handle is copied to the presentation
entry's `+360`<sub>h</sub>.

| | First pool | Second pool |
|---|---|---|
| Storage | 160 entries of `E0`<sub>h</sub> at `[02B40528]` (`003B6890`) | 32 entries of `70`<sub>h</sub> at `02B3F570` (`003AFCD0`) |
| Taken by | `003B56D0(record id)` at promotion, into `+114`<sub>h</sub> | `003AF340(record id)`, into `+118`<sub>h</sub>; needs the model's `@FCP` shadow block (`003E6E40`) |
| Handle | counter `02B40520` << 8 \| slot, checked at entry `+10`<sub>h</sub> | counter `02B3F550` << 8 \| slot, checked at entry `+04`<sub>h</sub> |
| Freed by | `003B6000` | `003AFBE0` |
| Mode | byte `+41`<sub>h</sub>, `003B6900(handle, v)` = `(v >> 2 & old) \| (v & 3)` | low nibble of `+20`<sub>h</sub>, `003AFD00` |

A first-pool entry keeps the owner's index at `+04`<sub>h</sub>, its strength at `+14`<sub>h</sub> (1.0) and two bones,
`+3C`<sub>h</sub> and `+3E`<sub>h</sub>, from the model's special bones `104`<sub>h</sub> and `106`<sub>h</sub> (`003E5AD0`).

The anchor in use is the word `+38`<sub>h</sub>. `003B5CE0(handle, b, x, y)` keeps the previous base offset
`+48`<sub>h</sub>, `+4C`<sub>h</sub> at `+30`<sub>h</sub>, `+34`<sub>h</sub> and the previous anchor at `+3A`<sub>h</sub>, stores the new base offset
and sets the anchor to `+3C`<sub>h</sub> for `b` = 0 or `+3E`<sub>h</sub> otherwise. `003B6BD0(handle, v)` stores the
offset multiplier `+44`<sub>h</sub> and `003B6BB0(handle, v)` the float `+2C`<sub>h</sub>; `0042D050` calls both.

`003B67F0(handle)`, from `003723B0`, puts the four ramp channels back to neutral (offset 0, extent
scales 1, rotation 0, strength 1) and clears their steps and counters, the cross-fade and the values
last built.

When the authored motion command `09`<sub>h</sub> (`00417F40`) starts a motion whose header carries a
character block of kind 1, it passes the block to `003B5E20(handle, block)` and its anchor choice and
base offset (`+A8`<sub>h</sub>, `+A0`<sub>h</sub>, `+A4`<sub>h</sub> of the header) to `003B5CE0`. `003B5E20` keeps a motion's
shadow overrides in the slot, flagged in byte `+40`<sub>h</sub>:

- first, for each override flagged by the previous motion, it writes the kept value into the channel
  and its cross-fade copy and clears a counter: bit 1 the offset (`+A0`<sub>h</sub>, `+A4`<sub>h</sub>; counter `+00`<sub>h</sub>),
  bit 2 the rotation (`+B0`<sub>h</sub>; counter `+03`<sub>h</sub>, the strength's), bit 3 the extent scales (`+A8`<sub>h</sub>,
  `+AC`<sub>h</sub>; counter `+02`<sub>h</sub>), and bit 4 the base offset (`+B4`<sub>h</sub>, `+B8`<sub>h</sub> into `+48`<sub>h</sub>, `+4C`<sub>h</sub>);
- then, when the block's word `+32`<sub>h</sub> is non-zero, it keeps the new values (block `+4C`<sub>h</sub>, `+50`<sub>h</sub>;
  `+10`<sub>h</sub>, `+54`<sub>h</sub>; `+58`<sub>h</sub>, `+5C`<sub>h</sub>; the rotation as `(word >> 6)` degrees) and copies the word's
  bits 0, 1, 3, 2, 4 and 5 into the flags' bits 1 to 6; it ends by clearing the four counters.

### Each frame

`00426420` runs `00426340` on every active record while tail `+42`<sub>h</sub> is 1 and `+43`<sub>h</sub> is 0:

1. it puts both entries in their off state (`003B6900(h, 6)`, `003AFD00(h, 0)`);
2. it stops unless `+284`<sub>h</sub> bits 2, 6, 7 and 12 are set, the record has no parent and `+2AE`<sub>h</sub> bit 1
   is clear;
3. kind 0 with a first-pool entry: `003B6900(h, 4)`, then the strength (`003B6B80`) is record `+27C`<sub>h</sub>
   when `+C0`<sub>h</sub> bit 1 is set, otherwise `003B5980(h)`;
4. kind 1 with a second-pool entry: `003AFD00(h, 1)`.

`003B5980` measures the distance `d` from the entry's bone (`00421FF0`) to the camera position
`02AEDF20` and returns `clamp(1 − (clamp(d, near, far) − near) × k, 0, 1)`, with `near`, `far` and `k`
at `+20`<sub>h</sub>, `+24`<sub>h</sub> and `+2C`<sub>h</sub> of the model's `@FCP` block (`003E6F70`). The 1 and the zero bias inside the
inner clamp are the cells `01EF93FC` (1.0) and `01EF93F0` (0.0), which `0036D990` sets at boot.

`003AF460`, from the character pass `00426090`, advances the second pool's ramps: for each of the 32
entries with a handle it counts down five counters (`+1C`<sub>h</sub>, `+1D`<sub>h</sub>, `+1E`<sub>h</sub>, `+54`<sub>h</sub>, `+55`<sub>h</sub>) and,
while one is non-zero, adds its step to its value (`+24`<sub>h</sub> by `+2C`<sub>h</sub>, `+28`<sub>h</sub> by `+30`<sub>h</sub>, `+34`<sub>h</sub> by
`+38`<sub>h</sub>, `+3C`<sub>h</sub> by `+48`<sub>h</sub>, `+44`<sub>h</sub> by `+4C`<sub>h</sub>).

### The shadow verbs

- `setshadowlod` (`286`<sub>h</sub>, `00342CF0`): `002E8950(actor, 1)` sets `+C0`<sub>h</sub> bit 1 and `002E89B0` stores
  the value, clamped to 0..1, at `+27C`<sub>h</sub>. `clearshadowlod` (`287`<sub>h</sub>) clears the bit.
- `setshadowalpha` (`284`<sub>h</sub>, `00342410`): `002E88A0(actor, 1)` sets `+C0`<sub>h</sub> bit 2 and `002E8900` stores
  the value at `+274`<sub>h</sub>. `clearshadowalpha` (`285`<sub>h</sub>) clears the bit.

Each finds the record through the actor's `+C0`<sub>h</sub> context, whose first word is the record index. Every
access to the two structures found is in [the shadow caster](character-lighting-and-shadows-pshadow-caster-accesses.tsv)
and [second pool](character-lighting-and-shadows-shadow-pool-v2-slot-accesses.tsv) tables.

## Layouts

A light request (entry `+20`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | type: 1-5 directional kinds, 6 ambient, 7 the character's own list |  |
| `01`<sub>h</sub> | `u8` | priority |  |
| `02`<sub>h</sub> | `u8` | subtype (ambient colour form; 5 = multiplier) |  |
| `03`<sub>h</sub> | `u8` | scope |  |
| `04`<sub>h</sub> | `u8` | scope sub-kind |  |
| `05`<sub>h</sub> | `u8` | bit 4 no ambient mode; bits 1-3 matrix; `80`<sub>h</sub> and up no light scale |  |
| `07`<sub>h</sub> | `u8` | bit 0 exclusive (not additive); bit 1 skip; bits 2-7 class |  |
| `08`<sub>h</sub> | `u32` | target: id, handle or group mask |  |
| `0C`<sub>h</sub> | `f32` | range |  |
| `10`<sub>h</sub> | `f32[4]` | colour |  |
| `20`<sub>h</sub> | `...` | kind data (position, axis, cone, segment end) |  |

## Modding notes

- The cap is six directional lights per character after priority; a seventh never reaches the shader.
- An exclusive ambient of the highest priority silences every other ambient on that character.
- Group numbers wrap at 32: group 32 is bit 0 again.

## Related

- [CharacterRenderObject](character-render-object.md): slot 8 and the part records.
- [Character render records](character-render-records.md): the record fields and promotion.
- [Character fades](character-fades.md): the instance fields that scale the ambient.
- [Character status visuals](character-status-visuals.md): the status lights.
- [Graphics settings](../Engine-Core/graphics-settings.md): `mMapChr*` and the shadow object.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the light-group and shadow verbs.
