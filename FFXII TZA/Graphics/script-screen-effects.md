---
title: "Script screen effects: cut-in, motion blur, soft focus and the screen blur sprites"
kind: "system"
category: "Graphics"
addresses: "0x020926E4, 0x0024D540, 0x00182B40, 0x02B59D20, 0x02092640, 0x0024CF50, 0x0024CEB0, 0x0024CBE0, 0x003AA6B0, 0x02B58C38, 0x02092678, 0x0024EC00, 0x0024EB20, 0x0024EA10, 0x003AAA50, 0x003DE160, 0x003DE210, 0x0036E810, 0x0024FAE0, 0x0024FA40, 0x003AB500, 0x00375B90, 0x02B58A80, 0x003DDF90, 0x0024E910"
---

## What the player sees

- When a chest or a reward shows the "obtained" message, the picture behind the window settles
  into a still frame over fifteen frames and comes back the same way after the window closes. That
  is the motion blur effect at full strength with one capture: 2,304 of its uses follow this one
  pattern.
- A handful of story scenes show a rotated cut-in picture of the frame.
- Many event scripts lay up to four offset, scaled, rotated and translucent sprites over the
  picture with the `blur*` verbs.
- Soft focus, which blurs the world and keeps the menu sharp, is never turned on by a shipped
  script.

## How it works

### The shared machinery

Cut-in, motion blur and soft focus follow one pattern:

- Parameter verbs write a staging block; play copies it into the live block, releases any render
  target the effect holds, allocates new ones, zeroes the effect's descriptor handles and raises the
  effect's bit in the flag word `0x020926E4`; clear releases the targets, drops the bit and ends in
  `0x0024C7C0`, which writes the ordinary draw mask back.
- A released target is appended to a 256-entry list at `0x02091950` (count `0x0209216A`) and freed
  later; only a full list frees it at once (`0x00182CA0`).
- The users read a target through `0x00182B20(target)`, which returns its texture `+0x00` while the byte `+0x08`
  is 0 and 0 otherwise (`0x0024B7B0`, `0x0024CBE0`, `0x002512B0`, `0x003756B0`, `0x003AAA50`, `0x003AB500` among them).
- The target allocator `0x00182B40` ignores its two scale arguments. It always asks for the render
  width by the render height × 512 / 448 (`0x00186AA0`, `0x00186A90`), so every target is full size.
- `0x00182B40` returns 0 and asks for nothing when `0x001B6C40()` or `0x00189120()` returns 0 (`0x00182B4C`,
  `0x00182B5A`). Otherwise the height is `h × 512.0 / 448.0`, truncated toward zero, for the render height
  `h` (`0x008C5B48`, `0x008C5B44`, `0x00182BA2`); the request also names the format `0x02CF7480` (`0x00182BAA`), and
  `0x00182B40` returns what `0x001B66F0` returns (`0x00182BCE`).

- The targets come from a pool kept by `0x001B6C40()`: `0x001B66F0` finds the 0xA8-byte pool for the width,
  height and format (`0x02CF7480`), creating it with `0x001B6560` when missing, and `0x001B67F0` takes a free
  target from it or makes a new one (`0x001EE040`). `0x00182CA0` hands a target back through `0x001B68D0`,
  which finds its pool by the texture's width `+0x28`, height `+0x2C` and format (its first qword) and returns it (`0x001B6990`).

- The per-frame driver `0x0024D540` calls its per-frame bodies
  only while the main-loop state `0x00229EA0()` is 2 or 6 (`0x0024D6AA`-`0x0024D6B7`). The field frame
  `0x0022A770` is state 2 ([frame update order](../Engine-Core/frame-update-order.md)).
- In order they are `0x0024BFD0`, `0x0024B7B0`, the soft focus `0x003AB500` with its block `0x020925F0` in draw 0 while
  bit `0x1` of `0x020926E4` is up, the screen capture `0x0024DEE0`, the cut-in `0x0024CBE0` and the motion blur
  `0x0024EA10` (`0x0024D6B9`-`0x0024D6F6`); every one but `0x003AB500` takes the draw index, 0 or 1.

Each frame the bodies queue descriptors in the screen-effect pool of
[screen fades](screen-fades.md). Every handler but kind 1's returns 1 (keep) unless the descriptor's draw
byte names the draw in progress (`0x00358320`): byte `+0x1D` for kinds 2, 4, 6, `0x0C` and `0x0D`, `+0x1E`
for kind 7, and `+0x1F` for kinds 3, 5 and `0x0B` (`0x003745CE`, `0x00375BAF`, `0x0037428E`, `0x00376094`,
`0x003752AE`; `0x00374E3E`; `0x00374A37`, `0x00375D9E`, `0x00376248`). Three steps recur:

1. Kind 3 copies the finished scene into a target.
2. Kind 4 (`0x00375B90`) binds an image to a block address of the emulated GS memory, the low 14 bits of its qword
   `+0x30` (`0x2A00` on this page): with `+0x1C` bit `0x1` it uploads the image at `+0x20` and binds the texture at
   `+0x50`, when there is one, to that address (`0x002D7E00`), and with bit `0x2`, when bits `0x3F00000` of `+0x30` hold
   more than `0x200000`, it uploads the palette at `+0x28`.
3. Quads of kinds 2, 5, 6, 7 and `0x0D` sample that address.

The pool releases a descriptor when its handler returns 0: kind 4 does so once drawn when `+0x1C`
bit `0x8` is set, kinds 2, 6 and `0x0D` when bit `0x40` is set. Every descriptor this page builds sets its
bit, so an effect redraws only while its per-frame body keeps queueing, and stops the frame after
its flag bit drops.

Kind 4 reads its qword `+0x30`, here `q`, as fields: the address `q & 0x3FFF` (`0x00375C12`), the format
`(q >> 20) & 0x3F` (`0x00375C18`-`0x00375C21`), and a width and height of `1 << n` for `n` the four bits
`(q >> 26) & 0xF` and `(q >> 30) & 0xF`, through `0x002D7F20(n)`, which returns `1 << n` for `n` up to 10 and
0 above (`0x00375C34`-`0x00375C55`). With `+0x1C` bit `0x10` the image goes up at a fixed 512 × 448 instead
(`0x00375BF7`-`0x00375C2D`).

Each upload is `0x003A22A0` followed by `0x003A1DB0` (`0x00375C2D`, `0x00375C84`, `0x00375CA8`), and the texture
`+0x50` is bound only when it is not 0 (`0x00375C92`). The palette goes up only when the format is above 2,
`(q & 0x3F00000) > 0x200000`, and bit `0x2` is set (`0x00375CAD`-`0x00375CCA`): at the address
`(q >> 37) & 0x3FFF` in the format `(q >> 51) & 0xF`, 16 × 16 entries with bit `0x4`, else 8 × 2
(`0x00375CD6`-`0x00375D3F`). Unless that address is 0 or `0xE00`, the palette texture `+0x58` then goes to
`0x002D7D50` with `q` (`0x00375D44`-`0x00375D65`).

### Cut-in

`cutinplay` (`0x003DF8F0`) passes the staging block `0x02B59D20` to `0x0024CF50`, which copies its 0x24
bytes to `0x02092640` and, only when bit `0x8` of the flag word is clear, allocates the target
`0x02092638` and raises bit `0x8`. A second play replaces the parameters and keeps the target.
`cutinclear` (`0x003DF8E0` → `0x0024CEB0`) zeroes the type byte, releases the target and every
recorded handle, and drops bit `0x8`.

The copy comes first on every play (`0x0024CF5B`-`0x0024CF73`). With bit `0x8` clear, `0x0024CF50` hands back
a target still held at `0x02092638` (`0x0024CF7B`-`0x0024CFAD`) and calls `0x00182B40(1.0, 1.0)` (`0x0024CFBF`). It
raises bit `0x8` and stores the result whatever `0x00182B40` returns (`0x0024CFC4`, `0x0024CFCC`), so a failed
allocation leaves the bit up with a target of 0.

`0x0024CEB0` also zeroes `0x02092638` (`0x0024CF0F`) and calls `0x003587B0(0)` (`0x0024CF16`), which stores 0 in
the pass-mask byte `0x022C7F99`, byte `+9` of [Phyre frame](../PhyreEngine/the-frame.md).

The parameter verbs only write the staging block (layout below): `cutintype` (`0x0313`, `0x003DF9F0`),
`cutinlinefade` (`0x0314`, `0x003DF990`), `cutinpos` (`0x0315`, `0x003DF9C0`), `cutinuv` (`0x0318`,
`0x003DFA30`), `cutincolor` (`0x0319`, `0x003DF950`) and `cutinlinecolor` (`0x031A`, `0x003DF970`).

`0x0024CBE0` draws nothing while the live type byte is 0. In draw 0 it switches the draw mask bits under mask `0x7F` on
for draw 0 and under `0xFF` on for draw 1, sets byte `0x022C7F99` to 1 and queues a kind-3 capture of the scene into
`0x02092638` (stage 7, `0x40703`). In draw 1 it queues a kind-4 bind of that target and calls `0x003AA6B0`, which queues
two kind-`0x0D` quads in stage 5:

- the picture: the block's position, rotation and colour, with texture coordinates from `(u, v)`
  to `(u + 1, v + 0.875)`, 448 over 512;
- for types 2, 3 and 4, the line: one of three line images built into the executable
  (`0x01EFD4A0`, `0x01EFD930`, `0x01EFDDC0`, each an indexed image and a 256-colour palette), made into
  textures once (`0x02B3F470`, `0x02B3F488`) and bound by a second kind 4, drawn with the line colour,
  the negated line width and a span of ±73 about its centre. Type 1 stops after the picture.

The draws read the live block's line width `0x02092650` (`+0x10`, `0x0024CD13`) and line colour `0x02092660`
(`+0x20`, `0x0024CCC3`). After the block they keep five handles from `0x00375900`:

- `0x02092664`, draw 0's capture (`0x0024CE90`);
- `0x02092668`, draw 1's bind (`0x0024CC8B`);
- `0x0209266C`, `0x02092670` and `0x02092674`, the three handles `0x003AA6B0` leaves in its parameter block at `+0x50`,
  `+0x54` and `+0x58` (`0x0024CD55`-`0x0024CD67`).

`0x0024CF50` zeroes all five when it allocates the target (`0x0024CFD5`-`0x0024CFE3`). `cutinclear`'s `0x0024CEB0`
releases each that is not 0 through `0x00375470` and zeroes it (`0x0024CF1B`-`0x0024CF3A`).

### Motion blur

`moveblurplay` (`0x003DE310`) passes the staging block `0x02B58C38` to `0x0024EC00`, which clears bit `0x10`,
copies the 12 bytes to `0x02092678`, and releases both targets. With screen type 1 or 2 it allocates
two targets (`0x02092688`, `0x02092690`), raises bits `0x10` and `0x20` and zeroes the eight handles; with any
other screen type it returns with bit `0x10` clear. `moveblurclear` (`0x003DE140` → `0x0024EB20`) releases
both targets and drops bit `0x10`. Its handle loop calls the release only for handles that are 0, which
releases nothing; the descriptors leave the pool on their own.

On that other path `0x0024EC00` leaves `0x02092688` and `0x02092690` holding the targets it has just handed
back: only the allocation path stores them (`0x0024ECFC`, `0x0024ED13`). The float arguments it passes to
`0x00182B40`, 0.5 for screen type 1 or 1.0 for type 2 and 0.25 for the second target (`0x01CEBB70`,
`0x01CEBBA8`, `0x01CEBB68`), are ignored there. Neither `0x0024EC00` nor `0x0024EB20` names the third target
`0x02092698`, so the clear leaves it held, and `0x0024EB20` leaves bit `0x20` as it is (`0x0024EBB0`).

The four type verbs write the staging block with the mappings of the layout below:
`moveblurpresettype` (`0x031E`, `0x003DE400`) byte `+0x00`, `moveblurcluttype` (`0x031F`, `0x003DE360`)
`+0x01`, `moveblurnoisetype` (`0x0320`, `0x003DE3A0`) `+0x02` and `moveblurscreentype` (`0x0321`,
`0x003DE430`) `+0x03`.

`0x0024EA10`, in draw 0 with bit `0x10` up, builds the request for `0x003AAA50` with a capture flag: 1 when
bit `0x20` is up (and clears bit `0x20`), otherwise 1 unless the capture-once bit is set. With the flag down,
`0x003AAA50` writes 1 to `0x01FD4A70`, and the scene draw `0x0022B0B0` answers by returning before it
draws (`0x0022B196`), so the scene is not drawn at all.

The mask byte picks the blur's colour table. The first time `0x003AAA50` runs, `0x02B3F4A0` is 0: it makes three
palette textures with `0x001837A0(table, 0x100, 1)` from the 256-entry tables `0x01EFACA0`, `0x01EFB0A0` and
`0x01EFB4A0` (`0x400` bytes each), keeps them at `0x02B3F420`, `0x02B3F428` and `0x02B3F430`, and sets `0x02B3F4A0` to 1
(`0x003AAC04`-`0x003AAC68`). Masks 1, 2 and 3 use them in that order. Mask 0 uses no palette: the texture is 0 and
the table is the request's `+0x28`, which `0x0024EA10` leaves 0 (`0x003AAC72`-`0x003AACC3`).

- Strength exactly 1.0, flag down and a third target `0x02092698` present: one kind-4 bind of that
  target and one kind-2 quad, the stored frame shown as it is. The third target is captured at the
  end of the first call that finds strength 1.0 and the flag down; any other strength releases it.
- Otherwise: a capture into the first target when the flag is up, kind-4 binds of both targets
  with the chosen mask table as palette, and three quads of kinds 5, 7 and 6 whose constants come
  from the preset.

`moveblurfade(frames)` (`0x003DE2A0`) and `moveblurclearfade(frames)` (`0x003DE240`) scale the frames
by the time base (`0x00265860`). A result of 0 plays or clears at once. Otherwise, when no blur fade
is running, they take a task record, keep it at `0x02B58C48` and give it the tick `0x003DE160`, the
end `0x003DE1F0`, the duration and a direction at `+0x28` (0 in, 1 out); a fade asked for while one
runs is dropped.

Each tick plays a copy of the staging block whose strength is
`strength × t / duration`, or `× (1 − t / duration)` going out, so the scene is captured afresh
every tick until the fade ends. The end clears `0x02B58C48` and, going out, tail-jumps to the clear.
`moveblurfadesync` waits while `0x02B58C48` is non-zero (poll `0x00345100`, `0x003DE150`).

### Object motion blur

The five `objmblur*` verbs keep a 0x18-byte block at `0x02B58C20` and never draw anything:

- `objmblurlimitalpha(a)` (`0x01C5`, `0x003DE460`) stores `a`, truncated, in byte `+0x01`;
- `objmblurcolor(r, g, b)` (`0x01C6`, `0x003DE450`) stores the three bytes at `+0x04` to `+0x06` and
  `0x80` at `+0x07`;
- `objmblurpower(p)` (`0x01C7`, `0x003DE470`) stores the float at `+0x08`;
- `objmblurplay(n)` (`0x01C3`, `0x003DE480`) stores `n` in byte `+0x00`, passes the block to the bare
  `ret` at `0x0016D6A0`, and resets it: zero, except `0x80` at `+0x07`;
- `objmblurclear` (`0x01C4`) jumps through `0x0017E7D0` to the same `ret`.

The start-up initialiser `0x00266D10` resets the block with the same defaults through `0x003DDD10`, which
also resets the four blur sprites, the motion blur staging block and the blur fade task `0x02B58C48`.

### Soft focus

`setsoftfocusmode(on, mode, b, amount)` (`0x02AE`, handler `0x0034FA00`) calls `0x0036E810`. With
`on` at 0 it calls the clear `0x0024FA40`. Otherwise it builds byte `+0` = 2 when `mode` is 1, else
1, byte `+1` = `b` and float `+4` = `amount`, and calls `0x0024FAE0`: bit `0x1` up, the block copied to
`0x020925F0`, a target allocated at `0x02092620` (a failed allocation drops bit `0x1` again) and byte
`+2` forced to 4.

`0x003AB500` runs in draw 0 when bit `0x1` is up (`0x0024D6C9`). Byte `+2` picks a size word, 4 → `0x40`,
3 → `0x80`, 2 → `0x100`; since play always stores 4, it is `0x40`. It sets the draw mask so draw 0
draws everything but the menu (bit `0x8`) and draw 1 only bits `0x8` and `0x10`, then queues a capture (stage 7,
`0x50703`), a bind with the size word, and a kind-2 quad with `amount` and colour `80 80 80 80`.

### The mode-screen backdrop

When a mode screen such as game over opens, the last field picture stays behind it. `0x00251D90(type,
fadeIn, fadeOut)` creates the backdrop, a 0x140-byte widget with the message procedure `0x002509D0`, unless
one exists ([game over](../World-Areas-And-Travel/game-over.md) calls it with 1, 60, 120). Its create arm
stores it at `0x020927F0`, the type at `+0xE4`, the two frame counts at `+0x120` and `+0x122`, progress 0 at
`+0x110` and state 1 at `+0xE6`.

- Types 0 and 1 take the first picture of the TIM2 at `[0x0209AC30] + 0x388` (`0x0024A9E0`) and a palette
  from `[0x0209AC30] + 0x390` (type 0) or `+ 0x3A8` (type 1). The picture's texture `0x0209AC38` (`0x00184140`)
  and palette texture `0x0209AC40` (`0x001837A0`) are made only while they are null (`0x00250B52`, `0x00250BB8`,
  `0x00250BFB`).
- Those two textures are kept until `0x00280670`, run when the `[0x0209AC30] + 0x3D8` pack is loaded (`0x0028067B`),
  releases them (`0x00183720`) and zeroes them (`0x0028070C`, `0x00280728`).
- The teardown arm frees the capture buffer `+0xC0` (`0x003697F0`), releases the three targets
  `+0xC8`, `+0xD0`, `+0xD8` (`0x00182CA0`) and clears `0x020927F0`.

The scene draw `0x0022B0B0` calls `0x00251010` (`0x0022B61C`) to capture. For types 0 and 1 it allocates a
buffer in resource arena 2 (`0x0036C1D0`, `0x0036A100`) and two targets (`0x00182B40`). It queues two stage-7
captures (`0x50703`) through that buffer into the two targets, starts the fade toward 1.0 (`0x00250E50`) and
sets state 3. After each stage-7 draw `0x00251E00` passes the buffer to `0x0036CAD0`.

The menu frames `0x0022B8C0` and `0x0022BC20` draw it each frame with `0x002512B0`:

1. Nothing is drawn while `+0xE8` bit `0x4` is set (`0x00251F00`). Types 2 and 3 draw one opaque black
   kind-2 quad in stage 5 (colour `00 00 00 80`) and stop.
2. For types 0 and 1, nothing is drawn while `0x00181DD0()` reports a camera override.
3. At full progress, once the composite target `+0xD8` exists, it binds that target and draws it as a
   kind-2 quad, and stops. Below full progress the composite is released first.
4. It binds the second capture and draws it plainly while the progress is below 1.0. With `+0xE8` bit
   `0x1` set it then binds the first capture with the palette `+0xF8` and the palette texture `0x0209AC48`. A kind-5 quad follows with strength bytes 25 and 6 (more in
   state 7), then two kind-7 quads at the overlay alpha and a fifth of it.
5. It binds the menu picture and draws a kind-2 quad in blend 2 (`0x2502`, subtractive) at the
   progress `+0x110`.
6. When the progress is exactly 1.0 and no composite exists, it allocates `+0xD8` and queues a
   stage-5 capture into it (`0x50503`).

`0x00250CA0` (from `0x002506D0`, field frame `0x0022A770`) moves the progress from its start `+0x114` by `+0x118`
along `0x00248F40(kind, frames, elapsed)`, counted on `0x0208F570`. The states are: 3 fading in (kind 1,
`+0x120` frames) then 4; 5 fading out (`+0x122` frames, kind 1, or kind 0 when `+0xE8` bit `0x8` is set
by `0x00251F20`) then 6; 7 a pulse of `+0x129` strength over `+0x12A` frames (`0x00250C50`) then 8.
`0x00250F30` starts the fade-out for types 0, 2, 3 and 4, `0x00251EA0(scale, frames, direction)` restarts the overlay alpha
`+0x130` (eased the same way), and `0x00251E80` destroys the widget.

| `0x00248F40` kind | Value at `t = elapsed / frames` (1.0 once `elapsed ≥ frames`) |
|---|---|
| 1 | `sin(πt/2)` |
| 2 | `1 − sin((t/2 + 1/2)π)` |
| 3 | `0.5 − sin((t + 1/2)π) / 2` |
| 4 | `0.6 + 0.4 √t` (`0x003A1D30` is the square root of the absolute value;`0x00248FC9`-`0x00248FDB`) |
| 5 | `0.4 + 0.3 sin(πt/2) + 0.3 t` |
| other | `t` |

`0x00251D20()` returns the state, or 2 when `+0xE8` bit `0x1` is clear; `0x00251D50()` returns 1 when there is no backdrop
or, with that bit set, when its state is 0, 6 or 8. `0x00251EE0` sets the fade-out frames. `0x00250E90(palette)` swaps in
another palette (`+0x40` past its header), making the 256-entry handle `[0x0209AC48]` through `0x00183760` on first use
and uploading through `0x00183310` after that; with a null argument, for types other than 2 and 3, it restores type 0's
palette in the same way (`0x002553C0`).

Both it (`0x00250ED7`) and the backdrop's procedure `0x002509D0` (`0x00250C26`, with `+0xF8`) go
through `0x002553C0(palette)`. It creates the palette texture `0x0209AC48` with `0x00183760(palette, 0x100, 1)` when there
is no such texture, and otherwise rewrites it through `0x00183640` with the same arguments.

### The screen blur sprites

The `blur*` verbs drive four sprite records of 0x68 bytes at `0x02B58A80`, index 0 to 3: a handle at
`+0x00` and a 0x58-byte kind-2 descriptor at `+0x10`. Each setter clamps the index into 0..3. The
original verbs `0x00C5`-`0x00CE` use index 0; the forms `0x0548`-`0x0551` pop the index as their
first argument.

| Verb | Body | Writes (descriptor offsets) |
|---|---|---|
| `blurplay` | `0x003DDF90` | first releases a handle the record still holds through `0x0024CFF0` and zeroes it (`0x003DDFCF`-`0x003DDFDC`), then files the descriptor (`0x00375900`, `0x003DDFFB`), keeps the handle, resets the descriptor to the defaults (`0x003DE00C`-`0x003DE04D`) |
| `blurstop` | `0x003DE060` | releases the handle; the descriptor stays |
| `bluralpha(a)` | `0x003DDE00` | `+0x34` = `a`; flag nibble 7 when `a` is 0.08 (`0x0090035C`), else 3 |
| `blurcolor(r, g, b, a)` | `0x003DDE50` | `+0x38` colour |
| `bluroffset(x, y)` | `0x003DDEB0` | `+0x20`, `+0x24` |
| `blurscale(x, y)` | `0x003DDF60` | `+0x28`, `+0x2C` |
| `blurrotate(r)` | `0x003DDF20` | `+0x30` |
| `blurlayer(n)` | `0x003DDE80` | low nibble of `+1`, the stage |
| `blurtrans(n)` | `0x003DE110` | high nibble of `+1`, the blend of [screen fades](screen-fades.md) |
| `blurprior(n)` | `0x003DDEE0` | `+3`, the priority |

`blurplay` (`0x00343F10`) submits only when `0x00267310` reports 0 for the script's manager, and
otherwise resets the record without submitting (`0x003DDC50`). The defaults are kind 2, stage 6,
blend 3, class 1, flags 3, offset 0, scale 1.0, rotation 0, alpha 0.5 and colour `0x80FFFFFF`.

Flags 3 leaves bit `0x40` clear, so a submitted sprite stays in the pool until `blurstop` or a reset.
The kind-2 handler `0x003745C0` multiplies the x offset by the 16:9 factor of
[screen mode and aspect](screen-mode-and-aspect.md). `0x003DE0A0` releases all four; the cutscene
skip paths `0x00360710`, `0x003601D0`, `0x00360A50` and `0x003600D0` call it.

### The quad packets

The quads of kinds 2, 5, 6 and 7 are drawn from packet templates of the
[PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md), which the boot hub `0x0037E0F0`
builds. A handler writes the descriptor's values into its template's payload. It then submits the payload through
`0x003A35E0`, with the template's words `+0x08` and `+0x0C` as the VIF words and the payload starting at `+0x18`.

The command build inside that call unpacks the payload into VU memory (`0x0022BFF0`), so quadword `qN` below is the
template's `+0x20 + 16 x N`. Each template ends in A+D pairs that set GS registers by number: `8` `CLAMP_1`, `6`
`TEX0_1`, `0x42` `ALPHA_1`, `0x47` `TEST_1` and, in the shared template, `0` `PRIM`.

Kind 7, `0x00374E30`, uses the template `0x02AE8BE0` (builder `0x0047A800`, microprogram `0x00479650`) and submits `0xF8`
bytes from `0x02AE8BF8` (`0x00374FB0`-`0x00374FB8`). It draws only when the descriptor's byte `+0x1E` names the draw in
progress (`0x00374E39`-`0x00374E44`). After drawing it keeps the descriptor while byte `+0x1C` is 0 and releases it
otherwise (`0x00374FBD`-`0x00374FC2`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AE8C20` | `u32` | 0 (zero-filled tail) | `q2.x` of the unpacked data: the descriptor's byte `+0x1D`; 1 at boot | `0x0047A800` at boot, 1 (`0x0047A87A`); `0x00374E30`, the descriptor's byte `+0x1D` (`0x00374E6F`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C24` | `u32` | 0 (zero-filled tail) | `q2.y` of the unpacked data: the descriptor's byte `+0x1F`; `0x14` at boot | `0x0047A800` at boot, `0x14` (`0x0047A881`, 8 bytes); `0x00374E30`, the descriptor's byte `+0x1F` (`0x00374E79`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C28` | `f32` | 0 (zero-filled tail) | `q2.z` of the unpacked data: 1.0; 0 at boot | `0x0047A800` at boot, 0 (`0x0047A881`); `0x00374E30`, 1.0 (`0x00374EB0`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C2C` | `f32` | 0 (zero-filled tail) | `q2.w` of the unpacked data: the descriptor's float `+0x30`; the bits `0x00008000` at boot | `0x0047A800` at boot, the bits `0x00008000` (`0x0047A8AE`); `0x00374E30`, the descriptor's float `+0x30` (`0x00374EBF`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C30` | `f32` | 0 (zero-filled tail) | `q3.x` of the unpacked data: the descriptor's float `+0x2C`; 140.0 at boot | `0x0047A800` at boot, 140.0 (`0x0047A889`); `0x00374E30`, the descriptor's float `+0x2C` (`0x00374E84`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C34` | `f32` | 0 (zero-filled tail) | `q3.y` of the unpacked data: 1.0; 1.0 at boot | `0x0047A800` at boot, 1.0 (`0x0047A890`, 8 bytes); `0x00374E30`, 1.0 (`0x00374E8C`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C38` | `f32` | 0 (zero-filled tail) | `q3.z` of the unpacked data: the descriptor's float `+0x34`; 0 at boot | `0x0047A800` at boot, 0 (`0x0047A890`); `0x00374E30`, the descriptor's float `+0x34` (`0x00374E9B`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C3C` | `f32` | 0 (zero-filled tail) | `q3.w` of the unpacked data: the descriptor's float `+0x38`; 0.7 at boot | `0x0047A800` at boot, 0.7 (`0x0047A898`, 8 bytes); `0x00374E30`, the descriptor's float `+0x38` (`0x00374EA8`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C40` | `f32` | 0 (zero-filled tail) | `q4.x` of the unpacked data: the descriptor's float `+0x20`; 0 at boot | `0x0047A800` at boot, 0 (`0x0047A898`); `0x00374E30`, the descriptor's float `+0x20` (`0x00374ECC`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C44` | `f32` | 0 (zero-filled tail) | `q4.y` of the unpacked data: the descriptor's float `+0x24`; 0 at boot | `0x0047A800` at boot, 0 (`0x0047A8B3`); `0x00374E30`, the descriptor's float `+0x24` (`0x00374ED9`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C4C` | `f32` | 0 (zero-filled tail) | `q4.w` of the unpacked data: the descriptor's float `+0x28`; 1.0 at boot | `0x0047A800` at boot, 1.0 (`0x0047A8BD`); `0x00374E30`, the descriptor's float `+0x28` (`0x00374EE6`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C50` | `u32` | 0 (zero-filled tail) | `q5.x` of the unpacked data: the descriptor's byte `+0x3C`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8C4`, 8 bytes); `0x00374E30`, the descriptor's byte `+0x3C` (`0x00374EF2`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C54` | `u32` | 0 (zero-filled tail) | `q5.y` of the unpacked data: the descriptor's byte `+0x3D`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8C4`); `0x00374E30`, the descriptor's byte `+0x3D` (`0x00374EFC`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C58` | `u32` | 0 (zero-filled tail) | `q5.z` of the unpacked data: the descriptor's byte `+0x3E`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8C8`, 8 bytes); `0x00374E30`, the descriptor's byte `+0x3E` (`0x00374F06`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C5C` | `u32` | 0 (zero-filled tail) | `q5.w` of the unpacked data: the descriptor's byte `+0x3F`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8C8`); `0x00374E30`, the descriptor's byte `+0x3F` (`0x00374F10`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C60` | `u32` | 0 (zero-filled tail) | `q6.x` of the unpacked data: the descriptor's byte `+0x40`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8CC`); `0x00374E30`, the descriptor's byte `+0x40` (`0x00374F1A`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C64` | `u32` | 0 (zero-filled tail) | `q6.y` of the unpacked data: the descriptor's byte `+0x41`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8D6`); `0x00374E30`, the descriptor's byte `+0x41` (`0x00374F24`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C68` | `u32` | 0 (zero-filled tail) | `q6.z` of the unpacked data: the descriptor's byte `+0x42`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8E0`); `0x00374E30`, the descriptor's byte `+0x42` (`0x00374F2E`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C6C` | `u32` | 0 (zero-filled tail) | `q6.w` of the unpacked data: the descriptor's byte `+0x43`; `0x60` at boot | `0x0047A800` at boot, `0x60` (`0x0047A8EA`); `0x00374E30`, the descriptor's byte `+0x43` (`0x00374F38`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C70` | `u32` | 0 (zero-filled tail) | `q7.x` of the unpacked data: the descriptor's byte `+0x44`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8F4`); `0x00374E30`, the descriptor's byte `+0x44` (`0x00374F42`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C74` | `u32` | 0 (zero-filled tail) | `q7.y` of the unpacked data: the descriptor's byte `+0x45`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A8FE`); `0x00374E30`, the descriptor's byte `+0x45` (`0x00374F4C`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C78` | `u32` | 0 (zero-filled tail) | `q7.z` of the unpacked data: the descriptor's byte `+0x46`; `0x80` at boot | `0x0047A800` at boot, `0x80` (`0x0047A908`, 8 bytes); `0x00374E30`, the descriptor's byte `+0x46` (`0x00374F56`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C7C` | `u32` | 0 (zero-filled tail) | `q7.w` of the unpacked data: the descriptor's byte `+0x47`; 0 at boot | `0x0047A800` at boot, 0 (`0x0047A908`); `0x00374E30`, the descriptor's byte `+0x47` (`0x00374F60`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C80` | `f32` | 0 (zero-filled tail) | `q8.x` of the unpacked data: the descriptor's float `+0x48`; 0 at boot | `0x0047A800` at boot, 0 (`0x0047A913`, 8 bytes); `0x00374E30`, the descriptor's float `+0x48` (`0x00374F6B`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C84` | `f32` | 0 (zero-filled tail) | `q8.y` of the unpacked data: the descriptor's float `+0x4C`; 0 at boot | `0x0047A800` at boot, 0 (`0x0047A913`); `0x00374E30`, the descriptor's float `+0x4C` (`0x00374F78`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C88` | `f32` | 0 (zero-filled tail) | `q8.z` of the unpacked data: the descriptor's float `+0x50`; 1.0 at boot | `0x0047A800` at boot, 1.0 (`0x0047A91A`); `0x00374E30`, the descriptor's float `+0x50` (`0x00374F85`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8C8C` | `f32` | 0 (zero-filled tail) | `q8.w` of the unpacked data: the descriptor's float `+0x54`; 1.0 at boot | `0x0047A800` at boot, 1.0 (`0x0047A924`); `0x00374E30`, the descriptor's float `+0x54` (`0x00374F92`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8CB0` | `u64` | 0 (zero-filled tail) | the `TEX0_1` value of the A+D pair: the descriptor's qword `+0x58`; 0 at boot | `0x0047A800` at boot, 0 (`0x0047A95F`); `0x00374E30`, the descriptor's qword `+0x58` (`0x00374F9E`) | `0x0022BFF0` during the submit at `0x00374FB8` |
| `0x02AE8CC0` | `u64` | 0 (zero-filled tail) | the `ALPHA_1` value of the A+D pair: the descriptor's qword `+0x60`; `0x44` at boot | `0x0047A800` at boot, `0x44` (`0x0047A971`); `0x00374E30`, the descriptor's qword `+0x60` (`0x00374FA9`) | `0x0022BFF0` during the submit at `0x00374FB8` |

Kind 5, `0x00375D90`, uses the template `0x02AE9510` (builder `0x004791E0`, microprogram `0x00478280`) and submits `0xD8`
bytes from `0x02AE9528` (`0x00375EA0`-`0x00375EA8`). Its draw byte is `+0x1F` (`0x00375D99`-`0x00375DA4`), and it keeps the
descriptor while byte `+0x1E` is 0 (`0x00375EAD`-`0x00375EB2`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AE954C` | `f32` | 0 (zero-filled tail) | `q1.w` of the unpacked data: the descriptor's float `+0x28`; 0 at boot | `0x004791E0` at boot, 0 (`0x00479248`, 8 bytes); `0x00375D90`, the descriptor's float `+0x28` (`0x00375E82`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9558` | `f32` | 0 (zero-filled tail) | `q2.z` of the unpacked data: the descriptor's float `+0x20`; 0.15 at boot | `0x004791E0` at boot, 0.15 (`0x0047925E`); `0x00375D90`, the descriptor's float `+0x20` (`0x00375DD0`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE955C` | `f32` | 0 (zero-filled tail) | `q2.w` of the unpacked data: the descriptor's float `+0x24`; 1.0 at boot | `0x004791E0` at boot, 1.0 (`0x00479265`); `0x00375D90`, the descriptor's float `+0x24` (`0x00375DDD`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9568` | `i32` | 0 (zero-filled tail) | `q3.z` of the unpacked data: the descriptor's signed byte `+0x1C`; `0x2D` at boot | `0x004791E0` at boot, `0x2D` (`0x0047927A`); `0x00375D90`, the descriptor's signed byte `+0x1C` (`0x00375DE9`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE956C` | `i32` | 0 (zero-filled tail) | `q3.w` of the unpacked data: the descriptor's signed byte `+0x1D`; 5 at boot | `0x004791E0` at boot, 5 (`0x00479281`, 8 bytes); `0x00375D90`, the descriptor's signed byte `+0x1D` (`0x00375DF3`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9570` | `f32` | 0 (zero-filled tail) | `q4.x` of the unpacked data: the descriptor's float `+0x34`; 0 at boot | `0x004791E0` at boot, 0 (`0x00479281`); `0x00375D90`, the descriptor's float `+0x34` (`0x00375E4E`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9574` | `f32` | 0 (zero-filled tail) | `q4.y` of the unpacked data: the descriptor's float `+0x38`; 0 at boot | `0x004791E0` at boot, 0 (`0x00479289`); `0x00375D90`, the descriptor's float `+0x38` (`0x00375E5B`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9578` | `f32` | 0 (zero-filled tail) | `q4.z` of the unpacked data: the descriptor's float `+0x3C`; 1.0 at boot | `0x004791E0` at boot, 1.0 (`0x0047928C`); `0x00375D90`, the descriptor's float `+0x3C` (`0x00375E68`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE957C` | `f32` | 0 (zero-filled tail) | `q4.w` of the unpacked data: the descriptor's float `+0x40`; 1.0 at boot | `0x004791E0` at boot, 1.0 (`0x00479293`); `0x00375D90`, the descriptor's float `+0x40` (`0x00375E75`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9580` | `u32` | 0 (zero-filled tail) | `q5.x` of the unpacked data: the descriptor's byte `+0x2C`; `0x80` at boot | `0x004791E0` at boot, `0x80` (`0x0047929A`); `0x00375D90`, the descriptor's byte `+0x2C` (`0x00375DFD`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9584` | `u32` | 0 (zero-filled tail) | `q5.y` of the unpacked data: the descriptor's byte `+0x2D`; `0x80` at boot | `0x004791E0` at boot, `0x80` (`0x004792A1`); `0x00375D90`, the descriptor's byte `+0x2D` (`0x00375E07`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9588` | `u32` | 0 (zero-filled tail) | `q5.z` of the unpacked data: the descriptor's byte `+0x2E`; `0x80` at boot | `0x004791E0` at boot, `0x80` (`0x004792A8`); `0x00375D90`, the descriptor's byte `+0x2E` (`0x00375E11`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE958C` | `u32` | 0 (zero-filled tail) | `q5.w` of the unpacked data: the descriptor's byte `+0x2F`; `0x40` at boot | `0x004791E0` at boot, `0x40` (`0x004792AF`); `0x00375D90`, the descriptor's byte `+0x2F` (`0x00375E1B`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9590` | `u32` | 0 (zero-filled tail) | `q6.x` of the unpacked data: the descriptor's byte `+0x30`; `0x80` at boot | `0x004791E0` at boot, `0x80` (`0x004792B6`); `0x00375D90`, the descriptor's byte `+0x30` (`0x00375E25`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9594` | `u32` | 0 (zero-filled tail) | `q6.y` of the unpacked data: the descriptor's byte `+0x31`; `0x80` at boot | `0x004791E0` at boot, `0x80` (`0x004792C0`); `0x00375D90`, the descriptor's byte `+0x31` (`0x00375E2F`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE9598` | `u32` | 0 (zero-filled tail) | `q6.z` of the unpacked data: the descriptor's byte `+0x32`; `0x80` at boot | `0x004791E0` at boot, `0x80` (`0x004792CA`); `0x00375D90`, the descriptor's byte `+0x32` (`0x00375E39`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE959C` | `u32` | 0 (zero-filled tail) | `q6.w` of the unpacked data: the descriptor's byte `+0x33`; 8 at boot | `0x004791E0` at boot, 8 (`0x004792D4`); `0x00375D90`, the descriptor's byte `+0x33` (`0x00375E43`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE95C0` | `u64` | 0 (zero-filled tail) | the `TEX0_1` value of the A+D pair: the descriptor's qword `+0x48`; 0 at boot | `0x004791E0` at boot, 0 (`0x0047930F`); `0x00375D90`, the descriptor's qword `+0x48` (`0x00375E8E`) | `0x0022BFF0` during the submit at `0x00375EA8` |
| `0x02AE95D0` | `u64` | 0 (zero-filled tail) | the `ALPHA_1` value of the A+D pair: the descriptor's qword `+0x50`; `0x44` at boot | `0x004791E0` at boot, `0x44` (`0x00479321`); `0x00375D90`, the descriptor's qword `+0x50` (`0x00375E99`) | `0x0022BFF0` during the submit at `0x00375EA8` |

Kinds 2 (`0x003745C0`) and 6 (`0x00374280`) share the template `0x02AE9600` (builder `0x00476C80`, microprogram `0x004758E0`).
The VIF page reads that template end to end. They submit `0x438` bytes from `0x02AE9618`. The template holds four
quad blocks of `0xF0` bytes at `+0x40`, `+0x130`, `+0x220` and `+0x310`, each ending in its own A+D pairs. Both
handlers draw only when the descriptor's byte `+0x1D` names the draw in progress. They fill block 0 and set the
first word of blocks 1-3 to 0 (`0x003742A1`-`0x003742BF`, `0x003745E1`-`0x003745FF`). The low nibble of the descriptor's
byte `+0x1C` picks the mode:

- 0 releases the descriptor without drawing.
- 1 draws a 256 x 224 quad without texture (`PRIM` `0x4D`).
- 2 samples the texture whose `TEX0_1` value is the descriptor's `+0x48`.
- 3 to 6 sample the surface entry `0x02AEECF0` + 16 x (mode - 3) of the
  [legacy GS layer](legacy-ps2-gs-layer.md) (`0x00374698`-`0x003746A8`). Kind 2's mode 7 samples entry 0: it first
  sets that entry's base bits `0x3FFF` to `0xDFF` (`0x0037467C`-`0x0037468F`) and then reads it (`0x003746AB`).
- Higher modes keep the block's size, texture, blend and switch words from the last draw that set them.

Whatever the mode, block 0 then takes the descriptor's offset (`+0x20`, `+0x24`), scale (`+0x28`, `+0x2C`), alpha
(`+0x34`), rotation (`+0x30`) and colour bytes from `+0x38`.
Kind 2 scales the x offset by the 16:9 factor: `x = [+0x20] × 0x0017FFD0()` into `0x02AE9650` (`0x00374781`-`0x003747B6`).

The four corner colours come from `+0x38`-`+0x47` when bit `0x10` of `+0x1C` is set; otherwise all four
copy corner 0 (`0x00374545`-`0x0037455C`, `0x003748BE`-`0x003748D5`). The handlers release the descriptor once drawn when
bit `0x40` of `+0x1C` is set (`0x003745A2`-`0x003745AE`, `0x0037490F`-`0x0037491B`). These are the fields of the blur sprite's
descriptor above, whose flags give mode 3.

The summon tint also fills this template: `0x0036F9F0`, and its layered form `0x0036F550`
([small binary tables](../Game-Files-And-Data-Tables/small-bin-tables.md)). So do the element draws of types
`0xA2` (`0x00462540`) and `0xA5` (`0x00463460`) ([effect element types](effect-element-types.md)).

`0x0036F550` copies
block 0 over blocks 1-3 (`0x0036F70D`-`0x0036F8D9`) and then changes each copy. The two element draws fill all four
blocks, one per pass of a loop (`0x004626D0`-`0x00462FA1`, `0x004635B0`-`0x004637E2`). They write each block's colours
through `0x00462260` (`0x00462421`) and submit through `0x003A34D0` (`0x00463004`, `0x00463C93`).

In its copies `0x0036F550` rewrites three words of each block from the summon tint table's tail (`0x02AD9B60`,
[small binary tables](../Game-Files-And-Data-Tables/small-bin-tables.md)): the depth word `+0x08` and the
offsets `+0x10` and `+0x14`. With a the `u32` at `+0x290`, s the size factor at `+0x288` (`0x0036F7AA`) and t
the difference of the `u32` at `+0x294` and a, divided by 3 and rounded toward zero, `t = ([+0x294] - a) / 3`
(a signed division, `0x0036F6E1`-`0x0036F6F6`), block k's depth word is `((0xFFFF - a - k * t) << 12) | 0xFF0`:

- block 0: `0x02AE9648` (`0x0036F90A`); offsets s at `0x02AE9650` and `0x02AE9654` (`0x0036F8E4`, `0x0036F8EF`);
- block 1: `0x02AE9738` (`0x0036F940`); offsets -0.9 x s (`0x00D10FB0`) at `0x02AE9740` and `0x02AE9744` (`0x0036F912`, `0x0036F91A`);
- block 2: `0x02AE9828` (`0x0036F96D`); 0.8 x s (`0x008F3108`) at `0x02AE9830` (`0x0036F963`) and -0.8 x s (`0x00D10FAC`) at
  `0x02AE9834` (`0x0036F98C`);
- block 3: `0x02AE9918` (`0x0036F9A5`); -0.7 x s (`0x00D108F4`) at `0x02AE9920` (`0x0036F99D`) and 0.7 x s (`0x008F3104`) at
  `0x02AE9924` (`0x0036F9AB`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02AE9628` | `f32` | 0 (zero-filled tail) | `q0.z`: 257.0 (`0x00D1110C`) from kinds 2 and 6, 512.0 from the summon tint; 260.0 at boot | `0x0036F550` (`0x0036F5C6`); `0x0036F9F0` (`0x0036FA77`); `0x00374280` (`0x003742AB`); `0x003745C0` (`0x003745EB`); `0x00476C80` at boot (`0x00476CE0`) | `0x0022BFF0` during each submit |
| `0x02AE962C` | `f32` | 0 (zero-filled tail) | `q0.w`: 512.0 from the summon tint, 228.0 at boot | `0x0036F550` (`0x0036F5D0`); `0x0036F9F0` (`0x0036FA81`); `0x00476C80` at boot (`0x00476CEA`, an 8-byte store of 228.0 and 0) | `0x0022BFF0` during each submit |
| `0x02AE9640` | `u32` | 0 (zero-filled tail) | block 0 `+0x00` (`q2.x`): 1 when the writer fills block 0, 0 when it leaves it out; 0 at boot | `0x0036F550` (`0x0036F5DA`); `0x0036F9F0` (`0x0036FA8B`); `0x00374280` (`0x00374325`, `0x00374397`, `0x003743ED`); `0x003745C0` (`0x00374665`, `0x003746FB`, `0x00374753`); `0x00462540` (`0x004626EE`, `0x004626FD`, `0x00462781`, `0x00462936`, `0x00462941`, `0x00462A00`); `0x00463460` (`0x004635D3`, `0x004635E2`, `0x0046365D`, `0x004637C1`, `0x00463823`, `0x004638E2`); `0x00476C80` at boot (`0x00476D01`) | `0x0036F550` (`0x0036F70D`, `0x0036F79E`, `0x0036F84C`); `0x0022BFF0` during each submit |
| `0x02AE9644` | `u32` | 0 (zero-filled tail) | block 0 `+0x04`: the descriptor's `+0x1C` bit `0x20` (kinds 2 and 6), 1 from the summon tint; 0 at boot | `0x0036F550` (`0x0036F5F8`); `0x0036F9F0` (`0x0036FA9F`); `0x00374280` (`0x00374463`); `0x003745C0` (`0x003747E2`); `0x00476C80` at boot (`0x00476D01`) | `0x0036F550` (`0x0036F70D`, `0x0036F79E`, `0x0036F84C`); `0x0022BFF0` during each submit |
| `0x02AE9648` | `u32` | 0 (zero-filled tail) | block 0 `+0x08`: `0x0FFFFFF0` from kinds 2 and 6 and the plain tint, `((0xFFFF - [0x02AD9DF0]) << 12) + 0xFF0` from the layered tint; `0x00FFFFFF` at boot | `0x0036F550` (`0x0036F90A`); `0x0036F9F0` (`0x0036FA95`); `0x00374280` (`0x00374435`); `0x003745C0` (`0x0037479B`); `0x00462540` (`0x00462B0B`); `0x00463460` (`0x004639BB`); `0x00476C80` at boot (`0x00476D05`) | `0x0036F550` (`0x0036F70D`, `0x0036F79E`, `0x0036F84C`); `0x0022BFF0` during each submit |
| `0x02AE9654` | `f32` | 0 (zero-filled tail) | block 0 `+0x14`: the y offset, the descriptor's `+0x24` (kinds 2 and 6); 0 at boot | `0x0036F550` (`0x0036F8EF`); `0x0036F9F0` (`0x0036FA60`); `0x00374280` (`0x0037442D`); `0x003745C0` (`0x00374793`); `0x00462540` (`0x00462B00`, `0x00462C20`, `0x00462D16`, `0x00462DE5`); `0x00463460` (`0x0046398C`, `0x00463A9B`); `0x00476C80` at boot (`0x00476D0C`) | `0x0036F550` (`0x0036F716`, `0x0036F7BD`, `0x0036F85C`); `0x00462540` (`0x00462C18`, `0x00462D0E`, `0x00462DD1`); `0x00463460` (`0x00463A87`); `0x0022BFF0` during each submit |
| `0x02AE9658` | `f32` | 0 (zero-filled tail) | block 0 `+0x18`: the quad's width, 256.0 (`0x00915A00`) in modes 1 to 6; 256.0 at boot | `0x0036F550` (`0x0036F58A`); `0x0036F9F0` (`0x0036FA1A`); `0x00374280` (`0x00374307`, `0x00374377`, `0x003743DD`); `0x003745C0` (`0x00374647`, `0x003746E3`, `0x00374743`); `0x00462540` (`0x00462703`, `0x004627D1`, `0x00462815`, `0x0046286A`, `0x0046288F`, `0x00462958`, `0x00462A06`, `0x00462E28`, `0x00462E6F`); `0x00463460` (`0x004635E8`, `0x0046369E`, `0x004636F3`, `0x00463718`, `0x0046383A`, `0x004638E8`, `0x00463ACE`); `0x00476C80` at boot (`0x00476D10`) | `0x0036F550` (`0x0036F716`, `0x0036F7BD`, `0x0036F85C`); `0x00462540` (`0x00462D90`, `0x00462DFA`, `0x00462E5F`); `0x00463460` (`0x00463A43`, `0x00463AAC`); `0x0022BFF0` during each submit |
| `0x02AE965C` | `f32` | 0 (zero-filled tail) | block 0 `+0x1C`: the quad's height, 224.0 (`0x008F313C`) in modes 1 to 6; 224.0 at boot | `0x0036F550` (`0x0036F59C`); `0x0036F9F0` (`0x0036FA3E`); `0x00374280` (`0x0037431D`, `0x00374387`, `0x003743E5`); `0x003745C0` (`0x0037465D`, `0x003746F3`, `0x0037474B`); `0x00462540` (`0x0046270D`, `0x004627B3`, `0x004628AB`, `0x00462972`, `0x00462A10`); `0x00463460` (`0x004635F2`, `0x0046373F`, `0x00463854`, `0x004638F2`); `0x00476C80` at boot (`0x00476D17`) | `0x0036F550` (`0x0036F716`, `0x0036F7BD`, `0x0036F85C`); `0x00462540` (`0x00462D9E`); `0x00463460` (`0x00463A59`); `0x0022BFF0` during each submit |
| `0x02AE966C` | `f32` | 0 (zero-filled tail) | block 0 `+0x2C`: the rotation, the descriptor's `+0x30` (kinds 2 and 6), 0 from the tint; 0 at boot | `0x0036F550` (`0x0036F5BE`); `0x0036F9F0` (`0x0036FAA9`); `0x00374280` (`0x0037447B`); `0x003745C0` (`0x003747FA`); `0x00462540` (`0x00462B77`); `0x00463460` (`0x00463A12`); `0x00476C80` at boot (`0x00476D2C`) | `0x0036F550` (`0x0036F71F`, `0x0036F7C6`, `0x0036F865`); `0x0022BFF0` during each submit |
| `0x02AE9670` | `f32` | 0 (zero-filled tail) | block 0 `+0x30`: the descriptor's `+0x60` (kind 6), 1.0 (kind 2 and the tint); 1.0 at boot | `0x0036F550` (`0x0036F602`); `0x0036F9F0` (`0x0036FAB4`); `0x00374280` (`0x00374488`); `0x003745C0` (`0x00374802`); `0x00462540` (`0x00462BAC`, `0x00462C39`, `0x00462D38`, `0x00462D83`); `0x00463460` (`0x00463A35`); `0x00476C80` at boot (`0x00476D34`) | `0x0036F550` (`0x0036F728`, `0x0036F7CF`, `0x0036F86E`); `0x00462540` (`0x00462C34`, `0x00462D76`); `0x0022BFF0` during each submit |
| `0x02AE9674` | `f32` | 0 (zero-filled tail) | block 0 `+0x34`: the descriptor's `+0x64` (kind 6), 1.0 (kind 2 and the tint); 1.0 at boot | `0x0036F550` (`0x0036F60C`); `0x0036F9F0` (`0x0036FABE`); `0x00374280` (`0x00374495`); `0x003745C0` (`0x0037480C`); `0x00462540` (`0x00462BA7`); `0x00463460` (`0x00463A3E`); `0x00476C80` at boot (`0x00476D3B`) | `0x0036F550` (`0x0036F728`, `0x0036F7CF`, `0x0036F86E`); `0x0022BFF0` during each submit |
| `0x02AE9680` | `f32` | 0 (zero-filled tail) | block 0 `+0x40`, the first of four floats that are (0, 0, 1.0, 0.875) in the texture modes (`0x00D10FC0`); 0 at boot | `0x0036F550` (`0x0036F5A7`); `0x0036F9F0` (`0x0036FA29`); `0x00374280` (`0x00374316`, `0x003743A1`); `0x003745C0` (`0x00374656`, `0x00374705`); `0x00462540` (`0x004628BC`, `0x0046297D`, `0x00462A1A`, `0x00462F52`); `0x00463460` (`0x00463747`, `0x0046385F`, `0x004638FC`, `0x00463C2C`); `0x00476C80` at boot (`0x00476D43`) | `0x0036F550` (`0x0036F731`, `0x0036F7D8`, `0x0036F877`); `0x00462540` (`0x00462F3B`); `0x00463460` (`0x00463C15`); `0x0022BFF0` during each submit |
| `0x02AE9688` | `f32` | 0 (zero-filled tail) | block 0 `+0x48`, the third of those floats: 1.0; 1.0 at boot | `0x0036F550` (`0x0036F5A7`); `0x0036F9F0` (`0x0036FA29`); `0x00374280` (`0x00374316`, `0x003743AC`); `0x003745C0` (`0x00374656`, `0x00374718`); `0x00462540` (`0x004628B5`, `0x00462989`, `0x00462A28`, `0x00462F57`); `0x00463460` (`0x0046374F`, `0x0046386B`, `0x0046390A`, `0x00463C31`); `0x00476C80` at boot (`0x00476D4A`) | `0x0036F550` (`0x0036F731`, `0x0036F7D8`, `0x0036F877`); `0x00462540` (`0x00462F40`); `0x00463460` (`0x00463C1A`); `0x0022BFF0` during each submit |
| `0x02AE968C` | `f32` | 0 (zero-filled tail) | block 0 `+0x4C`, the fourth: 0.875; 1.0 at boot | `0x0036F550` (`0x0036F5A7`); `0x0036F9F0` (`0x0036FA29`); `0x00374280` (`0x00374316`, `0x003743B4`); `0x003745C0` (`0x00374656`, `0x00374710`); `0x00462540` (`0x004628CB`, `0x0046298F`, `0x00462A2F`, `0x00462F61`); `0x00463460` (`0x00463756`, `0x00463871`, `0x00463911`, `0x00463C3B`); `0x00476C80` at boot (`0x00476D51`) | `0x0036F550` (`0x0036F731`, `0x0036F7D8`, `0x0036F877`); `0x00462540` (`0x00462F4D`); `0x00463460` (`0x00463C27`); `0x0022BFF0` during each submit |
| `0x02AE9694` | `u32` | 0 (zero-filled tail) | corner colour 0, green: the descriptor's byte `+0x39` (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F65C`); `0x0036F9F0` (`0x0036FAFC`); `0x00374280` (`0x003744AB`); `0x003745C0` (`0x00374824`); `0x00476C80` at boot (`0x00476D58`); `0x00462260` (`0x00462421`, called by `0x00462540` at `0x00462ECE`, `0x00463460` at `0x00463B2B`) | `0x0036F550` (`0x0036F73D`, `0x0036F7E4`, `0x0036F883`); `0x00374280` (`0x00374545`); `0x003745C0` (`0x003748BE`); `0x00462540` (`0x00462ED3`); `0x0022BFF0` during each submit |
| `0x02AE9698` | `u32` | 0 (zero-filled tail) | corner colour 0, blue: the descriptor's byte `+0x3A` (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F684`); `0x0036F9F0` (`0x0036FB19`); `0x00374280` (`0x003744B5`); `0x003745C0` (`0x0037482E`); `0x00476C80` at boot (`0x00476D5C`); `0x00462260` (`0x00462421`, called by `0x00462540` at `0x00462ECE`, `0x00463460` at `0x00463B2B`) | `0x0036F550` (`0x0036F73D`, `0x0036F7E4`, `0x0036F883`); `0x00374280` (`0x00374545`); `0x003745C0` (`0x003748BE`); `0x00462540` (`0x00462ED3`); `0x0022BFF0` during each submit |
| `0x02AE969C` | `u32` | 0 (zero-filled tail) | corner colour 0, alpha: the descriptor's byte `+0x3B` (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F6AC`); `0x0036F9F0` (`0x0036FB36`); `0x00374280` (`0x003744BF`); `0x003745C0` (`0x00374838`); `0x00476C80` at boot (`0x00476D5C`); `0x00462260` (`0x00462421`, called by `0x00462540` at `0x00462ECE`, `0x00463460` at `0x00463B2B`) | `0x0036F550` (`0x0036F73D`, `0x0036F7E4`, `0x0036F883`); `0x00374280` (`0x00374545`); `0x003745C0` (`0x003748BE`); `0x00462540` (`0x00462ED3`); `0x0022BFF0` during each submit |
| `0x02AE96A0` | `u32` | 0 (zero-filled tail) | corner colour 1, red: the descriptor's byte `+0x3C` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F62A`); `0x0036F9F0` (`0x0036FAD9`); `0x00374280` (`0x003744CF`, `0x0037454C`); `0x003745C0` (`0x00374848`, `0x003748C5`); `0x00462540` (`0x00462EE7`); `0x00476C80` at boot (`0x00476D60`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463B93`) | `0x0036F550` (`0x0036F749`, `0x0036F7F0`, `0x0036F88F`); `0x0022BFF0` during each submit |
| `0x02AE96A4` | `u32` | 0 (zero-filled tail) | corner colour 1, green: the descriptor's byte `+0x3D` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F652`); `0x0036F9F0` (`0x0036FAF6`); `0x00374280` (`0x0037454C`, `0x003744D9`); `0x003745C0` (`0x003748C5`, `0x00374852`); `0x00462540` (`0x00462EE7`); `0x00476C80` at boot (`0x00476D60`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463B93`) | `0x0036F550` (`0x0036F749`, `0x0036F7F0`, `0x0036F88F`); `0x0022BFF0` during each submit |
| `0x02AE96A8` | `u32` | 0 (zero-filled tail) | corner colour 1, blue: the descriptor's byte `+0x3E` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F67A`); `0x0036F9F0` (`0x0036FB13`); `0x00374280` (`0x0037454C`, `0x003744E3`); `0x003745C0` (`0x003748C5`, `0x0037485C`); `0x00462540` (`0x00462EE7`); `0x00476C80` at boot (`0x00476D64`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463B93`) | `0x0036F550` (`0x0036F749`, `0x0036F7F0`, `0x0036F88F`); `0x0022BFF0` during each submit |
| `0x02AE96AC` | `u32` | 0 (zero-filled tail) | corner colour 1, alpha: the descriptor's byte `+0x3F` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F6A2`); `0x0036F9F0` (`0x0036FB30`); `0x00374280` (`0x0037454C`, `0x003744ED`); `0x003745C0` (`0x003748C5`, `0x00374866`); `0x00462540` (`0x00462EE7`); `0x00476C80` at boot (`0x00476D64`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463B93`) | `0x0036F550` (`0x0036F749`, `0x0036F7F0`, `0x0036F88F`); `0x0022BFF0` during each submit |
| `0x02AE96B0` | `u32` | 0 (zero-filled tail) | corner colour 2, red: the descriptor's byte `+0x40` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F620`); `0x0036F9F0` (`0x0036FAD3`); `0x00374280` (`0x003744F7`, `0x00374554`); `0x003745C0` (`0x00374870`, `0x003748CD`); `0x00462540` (`0x00462EEE`); `0x00476C80` at boot (`0x00476D68`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463BC7`) | `0x0036F550` (`0x0036F755`, `0x0036F7FC`, `0x0036F89B`); `0x0022BFF0` during each submit |
| `0x02AE96B4` | `u32` | 0 (zero-filled tail) | corner colour 2, green: the descriptor's byte `+0x41` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F648`); `0x0036F9F0` (`0x0036FAF0`); `0x00374280` (`0x00374554`, `0x00374501`); `0x003745C0` (`0x003748CD`, `0x0037487A`); `0x00462540` (`0x00462EEE`); `0x00476C80` at boot (`0x00476D68`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463BC7`) | `0x0036F550` (`0x0036F755`, `0x0036F7FC`, `0x0036F89B`); `0x0022BFF0` during each submit |
| `0x02AE96B8` | `u32` | 0 (zero-filled tail) | corner colour 2, blue: the descriptor's byte `+0x42` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F670`); `0x0036F9F0` (`0x0036FB0D`); `0x00374280` (`0x00374554`, `0x0037450B`); `0x003745C0` (`0x003748CD`, `0x00374884`); `0x00462540` (`0x00462EEE`); `0x00476C80` at boot (`0x00476D6C`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463BC7`) | `0x0036F550` (`0x0036F755`, `0x0036F7FC`, `0x0036F89B`); `0x0022BFF0` during each submit |
| `0x02AE96BC` | `u32` | 0 (zero-filled tail) | corner colour 2, alpha: the descriptor's byte `+0x43` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F698`); `0x0036F9F0` (`0x0036FB2A`); `0x00374280` (`0x00374554`, `0x00374515`); `0x003745C0` (`0x003748CD`, `0x0037488E`); `0x00462540` (`0x00462EEE`); `0x00476C80` at boot (`0x00476D6C`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463BC7`) | `0x0036F550` (`0x0036F755`, `0x0036F7FC`, `0x0036F89B`); `0x0022BFF0` during each submit |
| `0x02AE96C0` | `u32` | 0 (zero-filled tail) | corner colour 3, red: the descriptor's byte `+0x44` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F616`); `0x0036F9F0` (`0x0036FACD`); `0x00374280` (`0x0037451F`, `0x0037455C`); `0x003745C0` (`0x00374898`, `0x003748D5`); `0x00462540` (`0x00462EF2`); `0x00476C80` at boot (`0x00476D70`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463B5F`) | `0x0036F550` (`0x0036F761`, `0x0036F808`, `0x0036F8A7`); `0x0022BFF0` during each submit |
| `0x02AE96C4` | `u32` | 0 (zero-filled tail) | corner colour 3, green: the descriptor's byte `+0x45` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F63E`); `0x0036F9F0` (`0x0036FAEA`); `0x00374280` (`0x0037455C`, `0x00374529`); `0x003745C0` (`0x003748D5`, `0x003748A2`); `0x00462540` (`0x00462EF2`); `0x00476C80` at boot (`0x00476D70`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463B5F`) | `0x0036F550` (`0x0036F761`, `0x0036F808`, `0x0036F8A7`); `0x0022BFF0` during each submit |
| `0x02AE96C8` | `u32` | 0 (zero-filled tail) | corner colour 3, blue: the descriptor's byte `+0x46` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F666`); `0x0036F9F0` (`0x0036FB07`); `0x00374280` (`0x0037455C`, `0x00374533`); `0x003745C0` (`0x003748D5`, `0x003748AC`); `0x00462540` (`0x00462EF2`); `0x00476C80` at boot (`0x00476D74`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463B5F`) | `0x0036F550` (`0x0036F761`, `0x0036F808`, `0x0036F8A7`); `0x0022BFF0` during each submit |
| `0x02AE96CC` | `u32` | 0 (zero-filled tail) | corner colour 3, alpha: the descriptor's byte `+0x47` with `+0x1C` bit `0x10` set, else corner 0's copy (kinds 2 and 6); `0x80` from the tint; `0x80` at boot | `0x0036F550` (`0x0036F68E`); `0x0036F9F0` (`0x0036FB24`); `0x00374280` (`0x0037455C`, `0x0037453D`); `0x003745C0` (`0x003748D5`, `0x003748B6`); `0x00462540` (`0x00462EF2`); `0x00476C80` at boot (`0x00476D74`); `0x00462260` (`0x00462421`, called by `0x00463460` at `0x00463B5F`) | `0x0036F550` (`0x0036F761`, `0x0036F808`, `0x0036F8A7`); `0x0022BFF0` during each submit |
| `0x02AE96E0` | `u64` | 0 (zero-filled tail) | the `CLAMP_1` value of block 0's A+D pairs: 5, or the descriptor's `+0x50` in kind 6's mode 2; 0 at boot | `0x0036F550` (`0x0036F6B6`); `0x0036F9F0` (`0x0036FB4A`); `0x00374280` (`0x00374336`, `0x003743C0`); `0x003745C0` (`0x003746AE`, `0x00374722`); `0x00462540` (`0x004628D2`, `0x00462999`, `0x00462A3E`); `0x00463460` (`0x0046375D`, `0x0046387B`, `0x00463920`); `0x00476C80` at boot (`0x00476D9A`) | `0x0036F550` (`0x0036F76F`, `0x0036F816`, `0x0036F8B5`); `0x0022BFF0` during each submit |
| `0x02AE96F0` | `u64` | 0 (zero-filled tail) | the `TEX0_1` value: a surface entry `0x02AEECF0` + 16 x (mode - 3) in modes 3 to 6 and entry 0 in kind 2's mode 7, the descriptor's `+0x48` in mode 2, `[0x02AEECF0]` from the plain tint, `[0x02AEED10]` from the layered tint; 0 at boot | `0x0036F550` (`0x0036F6FF`); `0x0036F9F0` (`0x0036FB43`); `0x00374280` (`0x0037434D`); `0x003745C0` (`0x003746B9`); `0x00462540` (`0x004628DA`, `0x00462996`, `0x00462A46`); `0x00463460` (`0x00463765`, `0x00463878`, `0x00463928`); `0x00476C80` at boot (`0x00476DAC`) | `0x0036F550` (`0x0036F777`, `0x0036F81E`, `0x0036F8BD`); `0x0022BFF0` during each submit |
| `0x02AE9700` | `u64` | 0 (zero-filled tail) | the `ALPHA_1` value: the blend word `0x01EFAC20[byte +1 >> 4]` of [screen fades](screen-fades.md) (kinds 2 and 6), `0x44` from the tint; 0 at boot | `0x0036F550` (`0x0036F6C1`); `0x0036F9F0` (`0x0036FB55`); `0x00374280` (`0x00374414`); `0x003745C0` (`0x0037477A`); `0x00462540` (`0x0046272B`, `0x004628F9`, `0x00462A64`); `0x00463460` (`0x00463610`, `0x00463784`, `0x00463946`); `0x00476C80` at boot (`0x00476DBE`) | `0x0036F550` (`0x0036F77F`, `0x0036F826`, `0x0036F8C5`); `0x0022BFF0` during each submit |
| `0x02AE9710` | `u64` | 0 (zero-filled tail) | the `TEST_1` value: the descriptor's `+0x58`, or `0x1001` when that is 0 (kind 6), `0x1001` (kind 2, plain tint), `0x51001` (layered tint); 0 at boot | `0x0036F550` (`0x0036F6CC`); `0x0036F9F0` (`0x0036FB60`); `0x00374280` (`0x00374596`); `0x003745C0` (`0x003748F7`); `0x00462540` (`0x00462F68`, `0x00462F72`); `0x00463460` (`0x00463C42`, `0x00463C4F`); `0x00476C80` at boot (`0x00476DD0`) | `0x0036F550` (`0x0036F787`, `0x0036F82E`, `0x0036F8CD`); `0x0022BFF0` during each submit |
| `0x02AE9720` | `u32` | 0 (zero-filled tail) | the `PRIM` value: `0x5D`, or `0x4D` (bit `0x10`, texturing, clear) in mode 1; `0x5D` at boot | `0x0036F550` (`0x0036F6D7`); `0x0036F9F0` (`0x0036FB6B`); `0x00374280` (`0x00374358`, `0x003743FB`); `0x003745C0` (`0x003746C4`, `0x00374761`); `0x00462540` (`0x0046272F`, `0x004628FD`, `0x00462A68`); `0x00463460` (`0x00463614`, `0x00463788`, `0x0046394A`); `0x00476C80` at boot (`0x00476DE2`) | `0x0036F550` (`0x0036F78F`, `0x0036F836`, `0x0036F8D5`); `0x0022BFF0` during each submit |
| `0x02AE9730` | `u32` | 0 (zero-filled tail) | block 1 `+0x00`: 0 from kinds 2 and 6 and the plain tint, block 0's word from the layered tint's copy; 0 at boot | `0x0036F9F0` (`0x0036FA4E`); `0x00374280` (`0x003742B3`); `0x003745C0` (`0x003745F3`); `0x00462540` (`0x004626EE`, `0x004626FD`, `0x00462781`, `0x00462936`, `0x00462941`, `0x00462A00`); `0x00463460` (`0x004635D3`, `0x004635E2`, `0x0046365D`, `0x004637C1`, `0x00463823`, `0x004638E2`); `0x00476C80` at boot (`0x00476D01`); `0x0036F550` (`0x0036F712`) | `0x0022BFF0` during each submit |
| `0x02AE9820` | `u32` | 0 (zero-filled tail) | block 2 `+0x00`, set as block 1's; 0 at boot | `0x0036F9F0` (`0x0036FA54`); `0x00374280` (`0x003742B9`); `0x003745C0` (`0x003745F9`); `0x00462540` (`0x004626EE`, `0x004626FD`, `0x00462781`, `0x00462936`, `0x00462941`, `0x00462A00`); `0x00463460` (`0x004635D3`, `0x004635E2`, `0x0046365D`, `0x004637C1`, `0x00463823`, `0x004638E2`); `0x00476C80` at boot (`0x00476D01`); `0x0036F550` (`0x0036F7B9`) | `0x0022BFF0` during each submit |
| `0x02AE9910` | `u32` | 0 (zero-filled tail) | block 3 `+0x00`, set as block 1's; 0 at boot | `0x0036F9F0` (`0x0036FA5A`); `0x00374280` (`0x003742BF`); `0x003745C0` (`0x003745FF`); `0x00462540` (`0x004626EE`, `0x004626FD`, `0x00462781`, `0x00462936`, `0x00462941`, `0x00462A00`); `0x00463460` (`0x004635D3`, `0x004635E2`, `0x0046365D`, `0x004637C1`, `0x00463823`, `0x004638E2`); `0x00476C80` at boot (`0x00476D01`); `0x0036F550` (`0x0036F858`) | `0x0022BFF0` during each submit |

### Area changes and skips

- The area unload `0x002628B0` and the start-up initialiser `0x00266D10` both call the cut-in reset
  `0x003DF900` and the motion blur reset `0x003DE320`, so no script needs `resetcutinparam` or
  `resetmoveblurparam`.
- `0x003DE210` ends a running blur fade (progress set to its duration, direction out), forgets the
  task and clears the blur. The unload, `0x003601D0` and `0x003600D0` call it.
- The effect teardown `0x0024E910` ends in the blur clear and the cut-in clear (`0x0024EA02`,
  `0x0024EA0B`); the unload and `0x003601D0` call it. Before them it clears bits `0x400` and `0x800` of `0x020926E4`
  (`0x0024E98D`) and, when bit `0x40` is set, clears that bit and hands the target `0x020926D0` back: appended to
  `0x02091950` while the count `0x0209216A` is below 256, else freed at once (`0x00182CA0`), and `0x020926D0` is zeroed
  (`0x0024E9A9`–`0x0024E9F7`).
- The unload calls `0x0036E810` twice with all zeros, turning soft focus off.

### Crossfade

`crossfade(flags, mode, frames)` (`0x016F`, `0x00353260`) dissolves a still of the picture into the
live scene. Unless the issuer's manager is skipping it calls `0x002F1A90(flags, mode, frames)`, which
acts when `frames` is positive or flag bit `0x2` is set:

- With no crossfade running it makes the scheduled task ([frame update order](../Engine-Core/frame-update-order.md)) `[0x022BE7C8]` (`0x002F16B0`) with the per-frame body
  `0x002F18D0` and the end `0x002F1950`, and keeps the flags at `+0x28`, the mode at `+0x38` and the
  length `frames × [0x01DFE0B4]` (`frames` alone when `0x001EDDA0()` is non-zero) at `+0x04`. Flag bit `0x2`
  adds one frame to the length.
- It then captures the picture: `0x00374D40(0, mode, 1)`, or, with flag bit `0x4`, `0x00374D40(0, mode, 2)`
  after a set of pass-mask calls (`0x003587B0(1)`, `0x00358720`, `0x00358640(1)` and others); `+0x30`
  records which.
- With a crossfade already running, flag bit `0x1` replaces its flags and restarts the length.

`0x00374D40(p, mode, q)` works only for a mode of 1 to 4. It takes a screen-size target once (`0x00182B40`, kept at
`0x02ADB6D0` with the mode at `0x02ADB6D8`) and files a kind-3 descriptor, stage 7, class 5, with bytes `+0x1C` = 1,
`+0x1D` = mode, `+0x1E` = `q` and `+0x1F` = `p`, the target at `+0x20` and `+0x38`; its handle goes to `0x02EC07F0`.

Each frame `0x002F18D0` re-captures when flag bit `0x4` is set and calls `0x003756B0(+0x30, alpha)` with `alpha = (L − c)
/ L × 255`, with `L` the length plus `[0x01DFE0B4]` and `c` the task's dword `+0x00`, so the still fades out as `c`
grows; it also sets byte `+0xD18` of the render manager (`0x00182610(1)`). `0x003756B0` files two descriptors while a
target and a mode exist:

- a kind-4 descriptor binding the target to the emulated GS memory, with a bind word that depends on
  the mode and, for modes 3 and 4, a palette at `0x02ADB720` or `0x02ADB6E0` (handle `0x02EC07F4`);
- a kind-2 quad, stage 5, class 1, priority 1, colour `0x80808080` with alpha `alpha / 255`
  (handle `0x02EC07F8`).

The end `0x002F1950` runs `0x00375F80`, which hands the target back (`0x0024B240`) and removes the three
descriptors from the pool, undoes the pass-mask calls for flag bit `0x4`, clears `[0x022BE7C8]` and byte
`+0xD18` (`0x00182610(0)`). `0x0024B240(target)` appends a released target to the list `0x02091950` while
its count `0x0209216A` is below 256 and otherwise frees it at once (`0x001B68D0`).

### Screen capture

`setcapturescreenmode(on)` (`0x02DF`, `0x00340B90`) keeps a still of the picture in a target. A non-zero
argument runs `0x0024E0F0`: it sets the two-bit capture mode, the bits under mask `0x6` of `0x020926E4`, to
1, hands back any target at `0x020926D8` and takes a full-size one (`0x00182B40`), clears the handle `0x020926E0`, and
drops the mode again when no target came back. Zero runs `0x0024E070`, which clears the mode, hands the
target back and removes the descriptor `0x020926E0` (`0x00375470`).

The per-frame driver `0x0024D540` calls `0x0024DEE0(draw)` (`0x0024D6E6`), which acts in draw 0 only:

1. In mode 1 it files a kind-3 descriptor (`0x00375900`) with bytes `+0x1C` = 1, `+0x1D` = 1,
   `+0x1E` = 2 and the target at `+0x38`, keeps its handle in `0x020926E0` and moves to mode 2
   (`0x0024DFCE`-`0x0024E045`).
2. In mode 2 it files each frame a kind-4 descriptor that binds the target's texture
   (`0x00182B20`, at `+0x50`) with `+0x1C` = `0x19`; the block address in its qword `+0x30` is the bits under mask `0x1FF`
   of the dword at `0x022D8E60 + 0x28 × [0x022D8EA8]`, shifted left by 5 (`0x0024DF2E`-`0x0024DFC6`).

## Layouts

```
Flag word 0x020926E4 (bits this page uses)
bit 0x1  soft focus up
mask 0x6  screen capture mode: 0 off, 1 capture on the next draw 0, 2 bound each frame
bit 0x8  cut-in up
bit 0x10  motion blur up
bit 0x20  motion blur: capture on the next frame
```

Cut-in staging `0x02B59D20` / live `0x02092640` (`0x24`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | type | cutintype: 0-4 kept, else 2; 0 draws nothing; reset 2 |
| `+0x01` | `u8` | lineFade | bit `0x1`: cutinlinefade; reset 0 |
| `+0x04` | `f32` | x | cutinpos; reset 0 |
| `+0x08` | `f32` | y | cutinpos; reset 0 |
| `+0x0C` | `f32` | rotation | cutinrotate, radians; reset 0 |
| `+0x10` | `f32` | lineWidth | cutinlinewidth; reset 2.0 |
| `+0x14` | `f32` | u | cutinuv; reset 0 |
| `+0x18` | `f32` | v | cutinuv; reset 0 |
| `+0x1C` | `u8[4]` | colour | cutincolor; reset 80 80 80 80 |
| `+0x20` | `u8[4]` | lineColour | cutinlinecolor; reset 00 00 00 80 |

Motion blur staging `0x02B58C38` / live `0x02092678` (`0x0C`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | preset | moveblurpresettype: 1->2, 2->3, else 1; reset 1 |
| `+0x01` | `u8` | mask | moveblurcluttype: 1->2, 2->3, 3->0, else 1; reset 1 |
| `+0x02` | `u8` | noise | moveblurnoisetype: 0-3 kept, else 0; reset 0; the builder ignores it |
| `+0x03` | `u8` | screenType | moveblurscreentype: 1->2, else 1; reset 1 |
| `+0x04` | `u8` | flags | bit `0x1` capture once (moveblurcaptureonce); reset 0 |
| `+0x08` | `f32` | strength | movebluraplpha; reset 0.5 |

Soft focus live block `0x020925F0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | mode | 1, or 2 for mode 1 |
| `+0x01` | `u8` | b | the third argument |
| `+0x02` | `u8` | size | always 4 |
| `+0x04` | `f32` | amount |  |
| `+0x08` | `void*` | target | copy of `0x02092620` |
| `+0x10` | `u32[3]` | handles |  |

Screen blur sprite `0x02B58A80` + index x `0x68`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | handle |  |
| `+0x10` | `u8` | kind | 2 |
| `+0x11` | `u8` | stageBlend | low nibble stage (6), high nibble blend (3) |
| `+0x12` | `u8` | class | 1 |
| `+0x13` | `u8` | priority | 0 |
| `+0x2C` | `u8` | flags | low nibble 3, or 7 for alpha 0.08 |
| `+0x30` | `f32` | offsetX |  |
| `+0x34` | `f32` | offsetY |  |
| `+0x38` | `f32` | scaleX | 1.0 |
| `+0x3C` | `f32` | scaleY | 1.0 |
| `+0x40` | `f32` | rotation | 0 |
| `+0x44` | `f32` | alpha | 0.5 |
| `+0x48` | `u8[4]` | colour | FF FF FF 80 |

### The mode-screen backdrop's fields

The backdrop is the `0x140`-byte widget kept at `0x020927F0` with procedure `0x002509D0` (The mode-screen backdrop above).

`ModeScreenBackdrop` (`0x140` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x002509D0` |
| `+0x0C0` | `void*` | captureBuffer | the capture buffer in resource arena 2 that `0x00251010` allocates for types 0 and 1 (`0x002510BC`); the stage-7 captures go through it (`0x0025115C`, `0x00251206`) and `0x00251E00` hands it to `0x0036CAD0` after each (`0x00251E56`-`0x00251E69`); the draw reads it (`0x00251599`, `0x002516ED`, `0x00251CD3`); the teardown frees it with `0x003697F0` (`0x002509FF`-`0x00250A12`) |
| `+0x0C8` | `void*` | firstCapture | the first capture target (`0x00182B40`), made by `0x00251010` (`0x002510E8`) and filled by a stage-7 capture (`0x0025116F`); the draw binds it with the palette when `+0xE8` bit `0x1` is set (`0x00251815`); released by the teardown with `0x00182CA0` (`0x00250A19`-`0x00250A2A`) |
| `+0x0D0` | `void*` | secondCapture | the second capture target, made by `0x00251010` (`0x002510FD`) and captured into (`0x00251215`); drawn plainly while the progress is below 1.0 (`0x00251628`); released by the teardown (`0x00250A31`-`0x00250A42`) |
| `+0x0D8` | `void*` | composite | the composite target: 0 from `0x00251010` (`0x00251104`); at full progress the draw allocates it and queues a stage-5 capture into it (`0x00251C5D`-`0x00251C76`), and while it exists draws it alone as a kind-2 quad (`0x002513A6`, `0x0025148F`, `0x00251CE6`); below full progress it is released first (`0x0025150D`-`0x00251525`); released by the teardown (`0x00250A49`-`0x00250A5A`) |
| `+0x0E0` | `u8[4]` | gap0E0 | read and written by no function; nothing fixes its width |
| `+0x0E4` | `i16` | type | the backdrop type 0-3, the creation record's word `+0x00` (`0x00250A93`-`0x00250A96`): types 0 and 1 use the field picture, 2 and 3 draw opaque black; read by `0x00250E90`, `0x00250F30`, `0x00251010`, the draw and `0x00251E00` (`0x00250EA9`, `0x00250F46`, `0x0025103A`, `0x002512EF`, `0x00251E10`) |
| `+0x0E6` | `i16` | state | 1 created (`0x00250A8C`), 3 fading in then 4, 5 fading out then 6, 7 pulsing then 8: set by `0x00251010` (`0x0025104F`, `0x00251241`), `0x00250F30` (`0x00250F73`-`0x00250FF7`), `0x00250C50` (`0x00250C68`) and the stepper `0x00250CA0` (`0x00250DD8`-`0x00250DF4`); `0x00251D20` and `0x00251D50` report it (`0x00251D35`, `0x00251D65`) |
| `+0x0E8` | `u32` | flags | bit `0x1` set on creation (`0x00250A7B`): the capture and its palette are in use (`0x0025123A`, `0x002516B2`), and `0x00251D20` answers 2 while it is clear (`0x00251D2C`); bit `0x4`: hidden, the draw draws nothing (`0x002512E2`), set or cleared by `0x00251F00` (`0x00251F0C`-`0x00251F19`); bit `0x8`: linear fade-out, set by `0x00251F20` (`0x00251F2C`-`0x00251F39`), cleared on creation (`0x00250AB2`), read by the stepper (`0x00250D5F`) |
| `+0x0EC` | `u8[4]` | gapEC | read and written by no function; nothing fixes its width |
| `+0x0F0` | `u64` | zeroF0 | 0, stored on creation (`0x00250AD2`); no function reads it |
| `+0x0F8` | `void*` | overlayPalette | the palette the overlay draws with: [`0x0209AC30`] + `0x390` + `0x40` for type 0 or + `0x3A8` + `0x40` for type 1 on creation (`0x00250B4B`, `0x00250BB1`), handed to `0x002553C0` (`0x00250C1F`); `0x00250E90` swaps it (`0x00250ECC`, `0x00250EE0`); the draw binds it (`0x00251806`) |
| `+0x100` | `void*` | picturePixels | the pixels of the first picture of the TIM2 at [`0x0209AC30`] + `0x388` (`0x0024A9E0`), the picture's header plus its word `+0x0C` (`0x00250B17`-`0x00250B1E`, `0x00250B84`); made into the texture `0x0209AC38` while it is null (`0x00250B52`, `0x00250BB8`) (`0x00250BE3`); read by the draw (`0x00251A9B`) |
| `+0x108` | `void*` | picturePalette | that picture's palette, past its pixels (`0x00250B25`-`0x00250B32`, `0x00250B98`); made into `0x0209AC40` while it is null (`0x00250BFB`, `0x00250C0C`); read by the draw (`0x00251BA0`) |
| `+0x110` | `f32` | progress | the fade's progress, 0 to 1.0: 0 on creation (`0x00250ACC`); the stepper sets it to `+0x114` + `+0x118` x `0x00248F40`(kind, frames, elapsed) (`0x00250E0E`-`0x00250E23`); the draw draws the menu picture at it and makes the composite at exactly 1.0 (`0x0025138F`, `0x0025164A`, `0x002518CB`, `0x00251C01`, `0x00251C46`); `0x00250E50` and `0x00250F30` start a fade from it (`0x00250E5C`, `0x00250F92`) |
| `+0x114` | `f32` | progressFrom | the progress when the fade started, stored by `0x00250E50` and `0x00250F30` (`0x00250E68`, `0x00250F9D`); read by the stepper (`0x00250E1B`) |
| `+0x118` | `f32` | progressBy | the change the fade makes, toward 1.0 or 0, stored by `0x00250E50` and `0x00250F30` (`0x00250E70`, `0x00250FA9`); read by the stepper (`0x00250E0E`) |
| `+0x11C` | `u32` | fadeStart | the frame counter `0x0208F570` when the fade started (`0x00250E7E`, `0x00250FB7`); 0 on creation and when the fade ends (`0x00250A9D`, `0x00250DB0`); the stepper counts from it (`0x00250D13`) |
| `+0x120` | `u16` | fadeInFrames | the fade-in length in frames, the creation record's word `+0x04` (`0x00250AA3`-`0x00250AA7`); used by the stepper in state 3 (`0x00250D8F`) and as the overlay's length when the capture starts (`0x00251263`) |
| `+0x122` | `u16` | fadeOutFrames | the fade-out length, the creation record's word `+0x08` (`0x00250AAE`, `0x00250AC5`), set by `0x00251EE0` (`0x00251EEC`); used in state 5 (`0x00250D72`) and for the overlay by `0x00250F30` (`0x00250FC9`) |
| `+0x124` | `f32` | pulseProgress | the pulse's progress: 0 when `0x00250C50` starts it (`0x00250C85`), stepped by `0x00250CA0` (`0x00250E30`); the draw multiplies the pulse strength by it (`0x00251890`) |
| `+0x128` | `u8` | strength | 25 on creation (`0x00250ADF`); the kind-5 quad's first strength byte (`0x0025185C`-`0x00251864`) |
| `+0x129` | `u8` | pulseStrength | 25 on creation for type 1 (`0x00250B0D`), then `0x00250C50`'s first argument (`0x00250C61`); the draw adds it times the pulse progress in state 7 (`0x00251871`-`0x00251890`) |
| `+0x12A` | `u16` | pulseFrames | the pulse's length, `0x00250C50`'s second argument (`0x00250C7D`); read by the stepper (`0x00250D54`) |
| `+0x12C` | `u32` | pulseStart | the frame counter when the pulse started (`0x00250C70`-`0x00250C76`); 0 on creation and when the pulse ends (`0x00250AD9`, `0x00250DCE`); the stepper counts from it (`0x00250D1D`, `0x00250D4D`) |
| `+0x130` | `f32` | overlayAlpha | the overlay's alpha, eased from 0 by the stepper from `+0x13C` over `+0x13A` frames, scaled by `+0x134` (`0x00250CFD`); 0 when `0x00250F30`, `0x00251010` or `0x00251EA0` restart it (`0x00250FDC`, `0x00251271`, `0x00251EC7`); the draw multiplies by it (`0x00251939`) |
| `+0x134` | `f32` | overlayScale | the overlay's scale: 1.0 from `0x00250F30` and `0x00251010` (`0x00250FE6`, `0x0025127B`), `0x00251EA0`'s first argument (`0x00251EB2`); read by the draw (`0x00251931`) |
| `+0x138` | `u8` | overlayRising | the overlay's direction: 1 from `0x00251010` (`0x00251285`), 0 from `0x00250F30` (`0x00250FF0`), `0x00251EA0`'s third argument (`0x00251ED1`); the draw tests it (`0x0025192A`) |
| `+0x139` | `u8[1]` | gap139 | read and written by no function; nothing fixes its width |
| `+0x13A` | `u16` | overlayFrames | the overlay's length in frames: `+0x120` from `0x00251010` (`0x0025126A`), `+0x122` from `0x00250F30` (`0x00250FD0`), `0x00251EA0`'s second argument (`0x00251EC0`); read by the stepper (`0x00250CDF`) |
| `+0x13C` | `u32` | overlayStart | the frame counter when the overlay started (`0x0025125D`, `0x00250FC3`, `0x00251EBA`); 0 on creation and when it ends (`0x00250AE6`, `0x00250D09`); the stepper counts from it (`0x00250CC1`) |

## Shipped data

Counted in the decompiled `us` scripts (1,114 files); the calls and scripts per verb are in
[the table of calls](script-screen-effects-screen-effect-census.tsv), and the calls per argument list in
[the arguments table](script-screen-effects-screen-effect-arguments.tsv):

| Fact | Value |
|---|---|
| obtained-message pattern | `moveblurcaptureonce` 2,305; `movebluraplpha(1)` 2,304; `moveblurfade(15)` 2,304; `moveblurclearfade(15)` 2,305 and `(10)` once; `moveblurfadesync` 4,609; in 264 scripts |
| `moveblurplay`, `moveblurclear`, `moveblurpresettype(1)` | 1 call each |
| other motion blur verbs | `moveblurcluttype`, `moveblurnoisetype`, `moveblurscreentype`, `resetmoveblurparam`: no calls |
| cut-in | `cutinplay` 5 calls in 4 scripts; `cutinrotate`, `cutinlinewidth(0)`, `cutinlinefade(1)`, `cutinclear` 4 each; `cutinpos` 1 |
| cut-in verbs with no calls | `cutintype`, `cutinuv`, `cutincolor`, `cutinlinecolor`, `resetcutinparam` |
| cut-in angles | 0.5236, 0.6981 and −1.65 radians |
| `setsoftfocusmode` | 52 calls in 49 scripts, all `(0, 0, 0, 0)` |
| `blurplay` / `blurstop` | 1,651 in 250 scripts / 2,428 in 324 |
| `bluralpha` | 1,713 calls; the commonest value 0.08 (331 calls) |
| `blurlayer` | 1,031 calls, all stage 5 |
| `blurtrans` | 415 calls, all blend 3 |
| `blurprior` | no calls |

## State

Every global below is 0 at load (the zero-filled tail of `.data`). The boot set-up `0x0024C970` clears `0x1670` bytes
from `0x020910A0` (`0x0024C983`), which covers the live blocks from `0x020925F0` to `0x020926BF`.

### The live blocks

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x020925F2` | `u8` | 0 | the soft focus block's size byte `+0x02`: always 4, which makes `0x003AB500` work at `0x40` (3 would give `0x80`, 2 `0x100`, any other value 0; `0x003AB525`-`0x003AB54B`) | `0x0024FAE0`, 4 (`0x0024FB83`), after its 16-byte copy over `0x020925F0`-`0x020925FF` (`0x0024FAEF`); `0x0024C970` (`0x0024CA87`, 8 bytes over `0x020925F0`-`0x020925F7`) | `0x003AB500` (`0x003AB525`, `0x003AB61D`), which `0x0024D540` hands the block (`0x0024D6D7`) |
| `0x020925F8` | `void*` | 0 | `+0x08`, the target: after the copy `0x0024FAE0` stores the target it allocates (also kept at `0x02092620`; 0 when the allocation fails) | `0x0024FAE0` (`0x0024FAEF`, 16 bytes; `0x0024FB6F`); `0x0024C970`, 0 (`0x0024C983`; `0x0024CA8E`) | `0x003AB500` (`0x003AB625`, `0x003AB699`), through the block address `0x0024D540` passes (`0x0024D6D7`) |
| `0x02092600` | `u32` | 0 | `+0x10`, the first of three handles that `0x003AB500` stores (`+0x10`, `+0x14`, `+0x18`); the clear `0x0024FA40` releases each non-zero handle (`0x00375470`) and zeroes it | `0x0024FAE0` (`0x0024FAFA`, 16 bytes; `0x0024FB76`, 0, 8 bytes with `+0x14`); `0x003AB500` (`0x003AB683`); `0x0024FA40`, 0 (`0x0024FABB`); `0x0024C970`, 0 (`0x0024C983`; `0x0024CA95`, 8 bytes with `+0x14`) | `0x0024FA40` (`0x0024FAB0`) |
| `0x02092608` | `u32` | 0 | `+0x18`, the third handle | `0x0024FAE0` (`0x0024FAFA`, 16 bytes; `0x0024FB7D`, 0); `0x003AB500` (`0x003AB796`); `0x0024FA40`, 0 (`0x0024FABB`); `0x0024C970`, 0 (`0x0024C983`; `0x0024CA9C`, 8 bytes with `+0x1C`) | `0x0024FA40` (`0x0024FAB0`) |
| `0x02092610` | `u64` | 0 | `+0x20`, copied from the caller's block by the third 16-byte store. `0x0036E810` builds only bytes `+0`, `+1` and the float `+4` of that block on its stack, so `+0x20` to `+0x2F` receive stack bytes it never wrote | `0x0024FAE0` (`0x0024FB0C`); `0x0024C970`, 0 (`0x0024C983`; `0x0024CAA3`) | no instruction names it |
| `0x02092618` | `u64` | 0 | `+0x28`, the same | `0x0024FAE0` (`0x0024FB0C`); `0x0024C970`, 0 (`0x0024C983`; `0x0024CAAA`) | no instruction names it |
| `0x02092680` | `f32` | 0 | the live motion blur strength `+0x08` | `0x0024EC00` (`0x0024EC2E`) | `0x0024EA10` (`0x0024EA5B`) |
| `0x020926A0` | `u32` | 0 | motion blur descriptor handle 0 of eight (`0x020926A0` to `0x020926BC`) | `0x0024EA10` (`0x0024EAFB`, 16 bytes over handles 0 to 3, from the request `0x003AAA50` filled); `0x0024EC00`, 0 (`0x0024ED1C`, 8 bytes over handles 0 and 1); `0x0024EB20`, 0 (`0x0024EBDB`) | `0x0024EB20` (`0x0024EBD0`) |
| `0x020926A8` | `u32` | 0 | handle 2 | `0x0024EA10` (`0x0024EAFB`); `0x0024EC00`, 0 (`0x0024ED23`, 8 bytes over handles 2 and 3); `0x0024EB20`, 0 (`0x0024EBDB`) | `0x0024EB20` (`0x0024EBD0`) |
| `0x020926B0` | `u32` | 0 | handle 4 | `0x0024EA10` (`0x0024EB02`, 16 bytes over handles 4 to 7); `0x0024EC00`, 0 (`0x0024ED2A`, 8 bytes over handles 4 and 5); `0x0024EB20`, 0 (`0x0024EBDB`) | `0x0024EB20` (`0x0024EBD0`) |
| `0x020926B8` | `u32` | 0 | handle 6 | `0x0024EA10` (`0x0024EB02`); `0x0024EC00`, 0 (`0x0024ED31`, 8 bytes over handles 6 and 7); `0x0024EB20`, 0 (`0x0024EBDB`) | `0x0024EB20` (`0x0024EBD0`) |

`0x0024EB20` walks the eight handles from `0x020926A0` (`0x0024EBA9`-`0x0024EBE5`): it calls the release `0x00375470` for a
handle of 0 and stores 0.

### The staging blocks

The cut-in staging block `0x02B59D20` is reset by `0x003DF900` (from the area changes `0x002628B0` and `0x00266D10`) and read
only as a whole: `cutinplay` (`0x003DF8F0`) passes it to `0x0024CF50`, which loads `+0x00` to `+0x0F` (`0x0024CF5B`),
`+0x10` to `+0x1F` (`0x0024CF65`) and `+0x20` to `+0x23` (`0x0024CF70`) into the live block `0x02092640`.

| Global | Field | Type | Meaning | Set by |
|---|---|---|---|---|
| `0x02B59D21` | `+0x01` | `u8` | the line fade bit; `0x003DF990` also reads it (`0x003DF990`) to keep its other bits | `0x003DF900` (`0x003DF909`, 8 bytes over `+0x00` to `+0x07`, then bit `0x1` cleared at `0x003DF910`); `0x003DF990` (`0x003DF9A0`) |
| `0x02B59D24` | `+0x04` | `f32` | x | `0x003DF900` (`0x003DF909`; `0x003DF92C`, 16 bytes over `+0x04` to `+0x13`); `0x003DF9C0` (`0x003DF9C0`) |
| `0x02B59D28` | `+0x08` | `f32` | y | `0x003DF900` (`0x003DF92C`); `0x003DF9C0` (`0x003DF9C8`) |
| `0x02B59D2C` | `+0x0C` | `f32` | the rotation in radians, 0 after a reset | `0x003DF900` (`0x003DF92C`); `0x003DF9E0` (`0x003DF9E0`), from `cutinrotate` (`0x00355120`, `0x00355130`) |
| `0x02B59D30` | `+0x10` | `f32` | the line width, 2.0 after a reset (the fourth float of `0x00D117A0`) | `0x003DF900` (`0x003DF917`, 8 bytes over `+0x10` to `+0x17`; `0x003DF92C`); `0x003DF9B0` (`0x003DF9B0`) |
| `0x02B59D34` | `+0x14` | `f32` | u | `0x003DF900` (`0x003DF917`; `0x003DF933`, 8 bytes over `+0x14` to `+0x1B`); `0x003DFA30` (`0x003DFA30`) |
| `0x02B59D38` | `+0x18` | `f32` | v | `0x003DF900` (`0x003DF91E`, 8 bytes over `+0x18` to `+0x1F`; `0x003DF933`); `0x003DFA30` (`0x003DFA38`) |
| `0x02B59D3C` | `+0x1C` | `u8` | colour byte 0, `0x80` after a reset | `0x003DF900` (`0x003DF91E`; `0x003DF93A`, `0x80808080` over `+0x1C` to `+0x1F`); `0x003DF950`, its first argument (`0x003DF950`) |
| `0x02B59D3D` | `+0x1D` | `u8` | colour byte 1, `0x80` after a reset | `0x003DF900` (`0x003DF91E`, `0x003DF93A`); `0x003DF950`, its second argument (`0x003DF956`) |
| `0x02B59D3E` | `+0x1E` | `u8` | colour byte 2, `0x80` after a reset | `0x003DF900` (`0x003DF91E`, `0x003DF93A`); `0x003DF950`, its third argument (`0x003DF95C`) |
| `0x02B59D3F` | `+0x1F` | `u8` | colour byte 3, `0x80` after a reset | `0x003DF900` (`0x003DF91E`, `0x003DF93A`); `0x003DF950`, its fourth argument (`0x003DF963`) |
| `0x02B59D40` | `+0x20` | `u8` | line colour byte 0, 0 after a reset | `0x003DF900` (`0x003DF944`, `0x80000000` over `+0x20` to `+0x23`); `0x003DF970`, its first argument (`0x003DF970`) |
| `0x02B59D41` | `+0x21` | `u8` | line colour byte 1, 0 after a reset | `0x003DF900` (`0x003DF944`); `0x003DF970`, its second argument (`0x003DF976`) |
| `0x02B59D42` | `+0x22` | `u8` | line colour byte 2, 0 after a reset | `0x003DF900` (`0x003DF944`); `0x003DF970`, its third argument (`0x003DF97C`) |
| `0x02B59D43` | `+0x23` | `u8` | line colour byte 3, `0x80` after a reset | `0x003DF900` (`0x003DF944`); `0x003DF970`, its fourth argument (`0x003DF983`) |

The motion blur staging block `0x02B58C38` is reset to the bytes 1, 1, 0, 1 (`0x01000101`) by `0x003DDD10` (`0x003DDDBF`,
8 bytes over `+0x00` to `+0x07`, then `0x003DDDD9`) and by `0x003DE320` (`0x003DE32A`, `0x003DE331`). It is read as 8 bytes
by `0x0024EC00` (`0x0024EC1F`), which `moveblurplay` (`0x003DE310`) and `moveblurfade` with a result of 0 (`0x003DE2B1`)
hand the block, and by the fade tick `0x003DE160` (`0x003DE177`) for its copy.

| Global | Field | Type | Meaning | Set by |
|---|---|---|---|---|
| `0x02B58C39` | `+0x01` | `u8` | the mask: 1 after a reset | `0x003DDD10`, `0x003DE320`; `0x003DE360`: 0 (`0x003DE373`), 3 (`0x003DE37B`), 2 (`0x003DE383`), 1 (`0x003DE38B`) |
| `0x02B58C3A` | `+0x02` | `u8` | the noise type: 0 after a reset | `0x003DDD10`, `0x003DE320`; `0x003DE3A0`: 3 (`0x003DE3B3`), 2 (`0x003DE3BB`), 1 (`0x003DE3C3`), 0 (`0x003DE3CB`) |
| `0x02B58C3B` | `+0x03` | `u8` | the screen type: 1 after a reset | `0x003DDD10`, `0x003DE320`; `0x003DE430`: 2 (`0x003DE434`), 1 (`0x003DE440`) |
| `0x02B58C40` | `+0x08` | `f32` | the strength: 0.5 after a reset; `0x0024EC00` copies it to the live `0x02092680` (`0x0024EC2B`) and the fade tick `0x003DE160` reads it (`0x003DE183`, `0x003DE1B3`) | `0x003DDD10` (`0x003DDDE3`, 0.5 from `0x01CEBB70` at `0x003DDD9F`); `0x003DE320` (`0x003DE33B`); `movebluraplpha` (`0x0322`, `0x0033FEA0`) through `0x003DE350` (`0x003DE350`, from `0x0033FEB0`) |

The object motion blur block `0x02B58C20` is reset to zero with `0x80` at `+0x07` by `0x003DDD10` (`0x003DDDB8`, `0x003DDDD2`,
`0x003DDDEB`, `0x003DDDF2`) and by `objmblurplay` (`0x003DE480`: `0x003DE498`, `0x003DE49F`, `0x003DE4A6`, `0x003DE4AD`), each an
8-byte store over `+0x00`, `+0x08` or `+0x10` and a byte store at `+0x07`. Its only address goes to the bare `ret`
`0x0016D6A0` (`0x003DE48A`, `0x003DE491`), and no instruction reads its fields:

| Global | Field | Type | Meaning | Set by |
|---|---|---|---|---|
| `0x02B58C21` | `+0x01` | `u8` | the limit alpha, the argument truncated: `cvttss2si rax, xmm0`, the low byte stored (`0x003DE460`-`0x003DE465`) | `0x003DE460` (`0x003DE465`); `0x003DDD10` (`0x003DDDB8`); `0x003DE480` (`0x003DE498`) |
| `0x02B58C24` | `+0x04` | `u8` | colour byte 0 | `0x003DE450` (`0x003DE452`, a 4-byte copy of its argument's dword over `+0x04` to `+0x07`); `0x003DDD10` (`0x003DDDB8`); `0x003DE480` (`0x003DE498`) |
| `0x02B58C27` | `+0x07` | `u8` | `0x80` after every store | `0x003DE450` (`0x003DE452`, then `0x80` at `0x003DE458`); `0x003DDD10` (`0x003DDDB8`, then `0x80` at `0x003DDDD2`); `0x003DE480` (`0x003DE498`, then `0x80` at `0x003DE49F`) |
| `0x02B58C28` | `+0x08` | `f32` | the power | `0x003DE470` (`0x003DE470`); `0x003DDD10`, 0 (`0x003DDDEB`, 8 bytes over `+0x08` to `+0x0F`); `0x003DE480`, 0 (`0x003DE4A6`) |
| `0x02B58C30` | `+0x10` | `u8[8]` | zero after every reset; nothing fixes its width | `0x003DDD10` (`0x003DDDF2`, 8 bytes); `0x003DE480` (`0x003DE4AD`, 8 bytes) |

## Modding notes

- Parameter verbs change nothing until the next play; during a motion blur fade every tick is a
  play.
- With capture-once and no fade running, the scene draw is skipped each frame, so nothing behind
  the held picture animates.
- The three effects run only in main-loop states 2 and 6.
- An area change restores both staging blocks and clears the cut-in and the motion blur; a
  skipped cutscene clears the blur sprites and ends a blur fade.
- `blurlayer(5)` puts a sprite in stage 5, under stage-6 fades; the default stage 6 draws among them
  by priority.

## Related

- [Screen fades](screen-fades.md): the screen-effect pool, stages, priorities and blends.
- [Screen mode and aspect](screen-mode-and-aspect.md): the 16:9 factor the sprites use.
- [Phyre frame](../PhyreEngine/the-frame.md): the two draws, the draw mask these
  effects write and the early return on `0x01FD4A70`.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the effect verbs.
- [Frame update order](../Engine-Core/frame-update-order.md): the main-loop states.
