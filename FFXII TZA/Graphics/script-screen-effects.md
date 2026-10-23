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

- The targets come from a pool kept by `0x001B6C40()`: `0x001B66F0` finds the 0xA8-byte pool for the width,
  height and format (`0x02CF7480`), creating it with `0x001B6560` when missing, and `0x001B67F0` takes a free
  target from it or makes a new one (`0x001EE040`). `0x00182CA0` hands a target back through `0x001B68D0`,
  which finds its pool by the texture's width `+0x28`, height `+0x2C` and format (its first qword) and returns it (`0x001B6990`).

- The per-frame driver `0x0024D540` calls the three per-frame bodies with the draw index, 0 or 1,
  only while the main-loop state `0x00229EA0()` is 2 or 6 (`0x0024D6AA`-`0x0024D6B7`). The field frame
  `0x0022A770` is state 2 ([frame update order](../Engine-Core/frame-update-order.md)).

Each frame the bodies queue descriptors in the screen-effect pool of
[screen fades](screen-fades.md). Every handler returns 1 (keep) unless the descriptor's byte
`+0x1D` names the draw in progress (`0x00358320`). Three steps recur:

1. Kind 3 copies the finished scene into a target.
2. Kind 4 (`0x00375B90`) binds an image to a block address of the emulated GS memory, the low 14
   bits of its qword `+0x30` (`0x2A00` on this page): with `+0x1C` bit 0 it uploads the image at
   `+0x20`, binds the texture at `+0x50` to that address (`0x002D7E00`), and with bit 1 uploads the
   palette at `+0x28`.
3. Quads of kinds 2, 5, 6, 7 and `0x0D` sample that address.

The pool releases a descriptor when its handler returns 0: kind 4 does so once drawn when `+0x1C`
bit 3 is set, kinds 2, 6 and `0x0D` when bit 6 is set. Every descriptor this page builds sets its
bit, so an effect redraws only while its per-frame body keeps queueing, and stops the frame after
its flag bit drops.

### Cut-in

`cutinplay` (`0x003DF8F0`) passes the staging block `0x02B59D20` to `0x0024CF50`, which copies its 0x24
bytes to `0x02092640` and, only when bit 3 of the flag word is clear, allocates the target
`0x02092638` and raises bit 3. A second play replaces the parameters and keeps the target.
`cutinclear` (`0x003DF8E0` → `0x0024CEB0`) zeroes the type byte, releases the target and every
recorded handle, and drops bit 3.

The parameter verbs only write the staging block (layout below): `cutintype` (`0x0313`, `0x003DF9F0`),
`cutinlinefade` (`0x0314`, `0x003DF990`), `cutinpos` (`0x0315`, `0x003DF9C0`), `cutinuv` (`0x0318`,
`0x003DFA30`), `cutincolor` (`0x0319`, `0x003DF950`) and `cutinlinecolor` (`0x031A`, `0x003DF970`).

`0x0024CBE0` draws nothing while the live type byte is 0. In draw 0 it switches the draw mask bits
0-6 on for both draws and queues a kind-3 capture of the scene into `0x02092638` (stage 7,
`0x40703`). In draw 1 it queues a kind-4 bind of that target and calls `0x003AA6B0`, which queues
two kind-`0x0D` quads in stage 5:

- the picture: the block's position, rotation and colour, with texture coordinates from `(u, v)`
  to `(u + 1, v + 0.875)`, 448 over 512;
- for types 2, 3 and 4, the line: one of three line images built into the executable
  (`0x01EFD4A0`, `0x01EFD930`, `0x01EFDDC0`, each an indexed image and a 256-colour palette), made into
  textures once (`0x02B3F470`, `0x02B3F488`) and bound by a second kind 4, drawn with the line colour,
  the negated line width and a span of ±73 about its centre. Type 1 stops after the picture.

### Motion blur

`moveblurplay` (`0x003DE310`) passes the staging block `0x02B58C38` to `0x0024EC00`, which clears bit 4,
copies the 12 bytes to `0x02092678`, and releases both targets. With screen type 1 or 2 it allocates
two targets (`0x02092688`, `0x02092690`), raises bits 4 and 5 and zeroes the eight handles; with any
other screen type it returns with bit 4 clear. `moveblurclear` (`0x003DE140` → `0x0024EB20`) releases
both targets and drops bit 4. Its handle loop calls the release only for handles that are 0, which
releases nothing; the descriptors leave the pool on their own.

The four type verbs write the staging block with the mappings of the layout below:
`moveblurpresettype` (`0x031E`, `0x003DE400`) byte `+0x00`, `moveblurcluttype` (`0x031F`, `0x003DE360`)
`+0x01`, `moveblurnoisetype` (`0x0320`, `0x003DE3A0`) `+0x02` and `moveblurscreentype` (`0x0321`,
`0x003DE430`) `+0x03`.

`0x0024EA10`, in draw 0 with bit 4 up, builds the request for `0x003AAA50` with a capture flag: 1 when
bit 5 is up (and clears bit 5), otherwise 1 unless the capture-once bit is set. With the flag down,
`0x003AAA50` writes 1 to `0x01FD4A70`, and the scene draw `0x0022B0B0` answers by returning before it
draws (`0x0022B196`), so the scene is not drawn at all.

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

The area initialiser `0x00266D10` resets the block with the same defaults through `0x003DDD10`, which
also resets the four blur sprites, the motion blur staging block and the blur fade task `0x02B58C48`.

### Soft focus

`setsoftfocusmode(on, mode, b, amount)` (`0x02AE`, handler `0x0034FA00`) calls `0x0036E810`. With
`on` at 0 it calls the clear `0x0024FA40`. Otherwise it builds byte `+0` = 2 when `mode` is 1, else
1, byte `+1` = `b` and float `+4` = `amount`, and calls `0x0024FAE0`: bit 0 up, the block copied to
`0x020925F0`, a target allocated at `0x02092620` (a failed allocation drops bit 0 again) and byte
`+2` forced to 4.

`0x003AB500` runs in draw 0 when bit 0 is up (`0x0024D6C9`). Byte `+2` picks a size word, 4 → `0x40`,
3 → `0x80`, 2 → `0x100`; since play always stores 4, it is `0x40`. It sets the draw mask so draw 0
draws everything but the menu (bit 3) and draw 1 only bits 3 and 4, then queues a capture (stage 7,
`0x50703`), a bind with the size word, and a kind-2 quad with `amount` and colour `80 80 80 80`.

### The mode-screen backdrop

When a mode screen such as game over opens, the last field picture stays behind it. `0x00251D90(type,
fadeIn, fadeOut)` creates the backdrop, a 0x140-byte widget with the message procedure `0x002509D0`, unless
one exists ([game over](../World-Areas-And-Travel/game-over.md) calls it with 1, 60, 120). Its create arm
stores it at `0x020927F0`, the type at `+0xE4`, the two frame counts at `+0x120` and `+0x122`, progress 0 at
`+0x110` and state 1 at `+0xE6`.

- Types 0 and 1 take the first picture of the TIM2 at `[0x0209AC30] + 0x388` (`0x0024A9E0`) and a palette
  from `[0x0209AC30] + 0x390` (type 0) or `+ 0x3A8` (type 1). The picture's texture `0x0209AC38` (`0x00184140`)
  and palette texture `0x0209AC40` (`0x001837A0`) are made once and kept.
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
| 4 | `0.6 + 0.4 ×` a random value (`0x003A1D30`) |
| 5 | `0.4 + 0.3 sin(πt/2) + 0.3 t` |
| other | `t` |

`0x00251D20()` returns the state, or 2 when `+0xE8` bit 0 is clear; `0x00251D50()` returns 1 when there is no
backdrop or its state is 0, 6 or 8. `0x00251EE0` sets the fade-out frames. `0x00250E90(palette)` swaps in
another palette (`+0x40` past its header) through `0x00183760`, or, for types other than 2 and 3, restores
type 0's palette.

Both it (`0x00250ED7`) and the backdrop's procedure `0x002509D0` (`0x00250C26`, with `+0xF8`) go
through `0x002553C0(palette)`. It creates the palette texture `0x0209AC48` with `0x00183760(palette, 0x100, 1)` when there
is none, and otherwise rewrites it through `0x00183640` with the same arguments.

### The screen blur sprites

The `blur*` verbs drive four sprite records of 0x68 bytes at `0x02B58A80`, index 0 to 3: a handle at
`+0x00` and a 0x58-byte kind-2 descriptor at `+0x10`. Each setter clamps the index into 0..3. The
original verbs `0x00C5`-`0x00CE` use index 0; the forms `0x0548`-`0x0551` pop the index as their
first argument.

| Verb | Body | Writes (descriptor offsets) |
|---|---|---|
| `blurplay` | `0x003DDF90` | files the descriptor, keeps the handle, resets the descriptor to the defaults |
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

Flags 3 leaves bit 6 clear, so a submitted sprite stays in the pool until `blurstop` or a reset.
The kind-2 handler `0x003745C0` multiplies the x offset by the 16:9 factor of
[screen mode and aspect](screen-mode-and-aspect.md). `0x003DE0A0` releases all four; the cutscene
skip paths `0x00360710`, `0x003601D0`, `0x00360A50` and `0x003600D0` call it.

### Area changes and skips

- The area unload `0x002628B0` and the area initialiser `0x00266D10` both call the cut-in reset
  `0x003DF900` and the motion blur reset `0x003DE320`, so no script needs `resetcutinparam` or
  `resetmoveblurparam`.
- `0x003DE210` ends a running blur fade (progress set to its duration, direction out), forgets the
  task and clears the blur. The unload, `0x003601D0` and `0x003600D0` call it.
- The effect teardown `0x0024E910` ends in the blur clear and the cut-in clear (`0x0024EA02`,
  `0x0024EA0B`); the unload and `0x003601D0` call it.
- The unload calls `0x0036E810` twice with all zeros, turning soft focus off.

### Crossfade

`crossfade(flags, mode, frames)` (`0x016F`, `0x00353260`) dissolves a still of the picture into the
live scene. Unless the issuer's manager is skipping it calls `0x002F1A90(flags, mode, frames)`, which
acts when `frames` is positive or flag bit 1 is set:

- With no crossfade running it makes the task `[0x022BE7C8]` (`0x002F16B0`) with the per-frame body
  `0x002F18D0` and the end `0x002F1950`, and keeps the flags at `+0x28`, the mode at `+0x38` and the
  length `frames × [0x01DFE0B4]` (`frames` alone when `0x001EDDA0()` is non-zero) at `+0x04`. Flag bit 1
  adds one frame to the length.
- It then captures the picture: `0x00374D40(0, mode, 1)`, or, with flag bit 2, `0x00374D40(0, mode, 2)`
  after a set of pass-mask calls (`0x003587B0(1)`, `0x00358720`, `0x00358640(1)` and others); `+0x30`
  records which.
- With a crossfade already running, flag bit 0 replaces its flags and restarts the length.

`0x00374D40(p, mode, q)` works only for a mode of 1 to 4. It takes a screen-size target once
(`0x00182B40`, kept at `0x02ADB6D0` with the mode at `0x02ADB6D8`) and files a kind-3 descriptor, stage 7,
class 5, with bytes `+0x1C` = 1, `+0x1D` = mode, `+0x1E` = `q` and `+0x1F` = `p`, the target at
`+0x28` and `+0x40`; its handle goes to `0x02EC07F0`.

Each frame `0x002F18D0` re-captures when flag bit 2 is set and calls `0x003756B0(+0x30, alpha)` with
`alpha = (L − c) / L × 255`, with `L` the length plus `[0x01DFE0B4]` and `c` the task's word `+0x00`,
so the still fades out as `c` grows; it also sets
byte `+0xD18` of the render manager (`0x00182610(1)`). `0x003756B0` files two descriptors while a target
and a mode exist:

- a kind-4 descriptor binding the target to the emulated GS memory, with a bind word that depends on
  the mode and, for modes 3 and 4, a palette at `0x02ADB720` or `0x02ADB6E0` (handle `0x02EC07F4`);
- a kind-2 quad, stage 5, class 1, priority 1, colour `0x80808080` with alpha `alpha / 255`
  (handle `0x02EC07F8`).

The end `0x002F1950` runs `0x00375F80`, which hands the target back (`0x0024B240`) and removes the three
descriptors from the pool, undoes the pass-mask calls for flag bit 2, clears `[0x022BE7C8]` and byte
`+0xD18` (`0x00182610(0)`). `0x0024B240(target)` appends a released target to the list `0x02091950` while
its count `0x0209216A` is below 256 and otherwise frees it at once (`0x001B68D0`).

### Screen capture

`setcapturescreenmode(on)` (`0x02DF`, `0x00340B90`) keeps a still of the picture in a target. A non-zero
argument runs `0x0024E0F0`: it sets the two-bit capture mode in bits 1-2 of `0x020926E4` to 1, hands back
any target at `0x020926D8` and takes a full-size one (`0x00182B40`), clears the handle `0x020926E0`, and
drops the mode again when no target came back. Zero runs `0x0024E070`, which clears the mode, hands the
target back and removes the descriptor `0x020926E0` (`0x00375470`).

The per-frame driver `0x0024D540` calls `0x0024DEE0(draw)` (`0x0024D6E6`), which acts in draw 0 only:

1. In mode 1 it files a kind-3 descriptor (`0x00375900`) with bytes `+0x1C` = 1, `+0x1D` = 1,
   `+0x1E` = 2 and the target at `+0x38`, keeps its handle in `0x020926E0` and moves to mode 2
   (`0x0024DFCE`-`0x0024E045`).
2. In mode 2 it files each frame a kind-4 descriptor that binds the target's texture
   (`0x00182B20`, at `+0x50`) with `+0x1C` = `0x19`; the block address in its qword `+0x30` is bits 0-8
   of the dword at `0x022D8E60 + 0x28 × [0x022D8EA8]`, shifted left by 5 (`0x0024DF2E`-`0x0024DFC6`).

## Layouts

```
Flag word 0x020926E4 (bits this page uses)
bit 0  soft focus up
bits 1-2  screen capture mode: 0 off, 1 capture on the next draw 0, 2 bound each frame
bit 3  cut-in up
bit 4  motion blur up
bit 5  motion blur: capture on the next frame
```

Cut-in staging `0x02B59D20` / live `0x02092640` (`0x24`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | type | cutintype: 0-4 kept, else 2; 0 draws nothing; reset 2 |
| `+0x01` | `u8` | lineFade | bit 0: cutinlinefade; reset 0 |
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
| `+0x04` | `u8` | flags | bit 0 capture once (moveblurcaptureonce); reset 0 |
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

The backdrop is the `0x140`-byte widget at `0x020927F0` with procedure `0x002509D0` (The mode-screen backdrop above).

```struct ModeScreenBackdrop base=record size=0x140
+0x00    u8[192]         header                 the widget header, written by the constructor 0x002465F0 (Widgets, The
                                                header); procedure 0x002509D0
+0xC0    ptr             captureBuffer          the capture buffer in resource arena 2 that 0x00251010 allocates for
                                                types 0 and 1 (0x002510BC); the stage-7 captures go through it
                                                (0x0025115C, 0x00251206) and 0x00251E00 hands it to 0x0036CAD0 after each
                                                (0x00251E56-0x00251E69); the draw reads it (0x00251599, 0x002516ED, 0x00251CD3);
                                                the teardown frees it with 0x003697F0 (0x002509FF-0x00250A12)
+0xC8    ptr             firstCapture           the first capture target (0x00182B40), made by 0x00251010 (0x002510E8) and
                                                filled by a stage-7 capture (0x0025116F); the draw binds it with the
                                                palette when +0xE8 bit 0 is set (0x00251815); released by the teardown
                                                with 0x00182CA0 (0x00250A19-0x00250A2A)
+0xD0    ptr             secondCapture          the second capture target, made by 0x00251010 (0x002510FD) and captured
                                                into (0x00251215); drawn plainly while the progress is below 1.0
                                                (0x00251628); released by the teardown (0x00250A31-0x00250A42)
+0xD8    ptr             composite              the composite target: 0 from 0x00251010 (0x00251104); at full progress the
                                                draw allocates it and queues a stage-5 capture into it
                                                (0x00251C5D-0x00251C76), and while it exists draws it alone as a kind-2
                                                quad (0x002513A6, 0x0025148F, 0x00251CE6); below full progress it is
                                                released first (0x0025150D-0x00251525); released by the teardown
                                                (0x00250A49-0x00250A5A)
+0xE0    u8[4]           gap0E0                 read and written by no function; nothing fixes its width
+0xE4    i16             type                   the backdrop type 0-3, the creation record's word +0x00
                                                (0x00250A93-0x00250A96): types 0 and 1 use the field picture, 2 and 3 draw
                                                opaque black; read by 0x00250E90, 0x00250F30, 0x00251010, the draw and
                                                0x00251E00 (0x00250EA9, 0x00250F46, 0x0025103A, 0x002512EF, 0x00251E10)
+0xE6    i16             state                  1 created (0x00250A8C), 3 fading in then 4, 5 fading out then 6, 7
                                                pulsing then 8: set by 0x00251010 (0x0025104F, 0x00251241), 0x00250F30
                                                (0x00250F73-0x00250FF7), 0x00250C50 (0x00250C68) and the stepper 0x00250CA0
                                                (0x00250DD8-0x00250DF4); 0x00251D20 and 0x00251D50 report it (0x00251D35,
                                                0x00251D65)
+0xE8    u32             flags                  bit 0 set on creation (0x00250A7B): the capture and its palette are in
                                                use (0x0025123A, 0x002516B2), and 0x00251D20 answers 2 while it is clear
                                                (0x00251D2C); bit 2: hidden, the draw draws nothing (0x002512E2), set or
                                                cleared by 0x00251F00 (0x00251F0C-0x00251F19); bit 3: linear fade-out, set
                                                by 0x00251F20 (0x00251F2C-0x00251F39), cleared on creation (0x00250AB2), read
                                                by the stepper (0x00250D5F)
+0xEC    u8[4]           gapEC                  read and written by no function; nothing fixes its width
+0xF0    u64             zeroF0                 0, stored on creation (0x00250AD2); no function reads it
+0xF8    ptr             overlayPalette         the palette the overlay draws with: [0x0209AC30] + 0x390 + 0x40 for type
                                                0 or + 0x3A8 + 0x40 for type 1 on creation (0x00250B4B, 0x00250BB1),
                                                handed to 0x002553C0 (0x00250C1F); 0x00250E90 swaps it (0x00250ECC, 0x00250EE0);
                                                the draw binds it (0x00251806)
+0x100   ptr             picturePixels          the pixels of the first picture of the TIM2 at [0x0209AC30] + 0x388
                                                (0x0024A9E0), the picture's header plus its word +0x0C
                                                (0x00250B17-0x00250B1E, 0x00250B84); made into the texture 0x0209AC38 once
                                                (0x00250BE3); read by the draw (0x00251A9B)
+0x108   ptr             picturePalette         that picture's palette, past its pixels (0x00250B25-0x00250B32, 0x00250B98);
                                                made into 0x0209AC40 once (0x00250C0C); read by the draw (0x00251BA0)
+0x110   f32             progress               the fade's progress, 0 to 1.0: 0 on creation (0x00250ACC); the stepper
                                                sets it to +0x114 + +0x118 x 0x00248F40(kind, frames, elapsed)
                                                (0x00250E0E-0x00250E23); the draw draws the menu picture at it and makes
                                                the composite at exactly 1.0 (0x0025138F, 0x0025164A, 0x002518CB, 0x00251C01,
                                                0x00251C46); 0x00250E50 and 0x00250F30 start a fade from it (0x00250E5C,
                                                0x00250F92)
+0x114   f32             progressFrom           the progress when the fade started, stored by 0x00250E50 and 0x00250F30
                                                (0x00250E68, 0x00250F9D); read by the stepper (0x00250E1B)
+0x118   f32             progressBy             the change the fade makes, toward 1.0 or 0, stored by 0x00250E50 and
                                                0x00250F30 (0x00250E70, 0x00250FA9); read by the stepper (0x00250E0E)
+0x11C   u32             fadeStart              the frame counter 0x0208F570 when the fade started (0x00250E7E, 0x00250FB7);
                                                0 on creation and when the fade ends (0x00250A9D, 0x00250DB0); the stepper
                                                counts from it (0x00250D13)
+0x120   u16             fadeInFrames           the fade-in length in frames, the creation record's word +0x04
                                                (0x00250AA3-0x00250AA7); used by the stepper in state 3 (0x00250D8F) and as
                                                the overlay's length when the capture starts (0x00251263)
+0x122   u16             fadeOutFrames          the fade-out length, the creation record's word +0x08 (0x00250AAE,
                                                0x00250AC5), set by 0x00251EE0 (0x00251EEC); used in state 5 (0x00250D72) and
                                                for the overlay by 0x00250F30 (0x00250FC9)
+0x124   f32             pulseProgress          the pulse's progress: 0 when 0x00250C50 starts it (0x00250C85), stepped by
                                                0x00250CA0 (0x00250E30); the draw multiplies the pulse strength by it
                                                (0x00251890)
+0x128   u8              strength               25 on creation (0x00250ADF); the kind-5 quad's first strength byte
                                                (0x0025185C-0x00251864)
+0x129   u8              pulseStrength          25 on creation for type 1 (0x00250B0D), then 0x00250C50's first argument
                                                (0x00250C61); the draw adds it times the pulse progress in state 7
                                                (0x00251871-0x00251890)
+0x12A   u16             pulseFrames            the pulse's length, 0x00250C50's second argument (0x00250C7D); read by the
                                                stepper (0x00250D54)
+0x12C   u32             pulseStart             the frame counter when the pulse started (0x00250C70-0x00250C76); 0 on
                                                creation and when the pulse ends (0x00250AD9, 0x00250DCE); the stepper
                                                counts from it (0x00250D1D, 0x00250D4D)
+0x130   f32             overlayAlpha           the overlay's alpha, eased from 0 by the stepper from +0x13C
                                                over +0x13A frames, scaled by +0x134 (0x00250CFD); 0 when 0x00250F30, 0x00251010
                                                or 0x00251EA0 restart it (0x00250FDC, 0x00251271, 0x00251EC7); the draw
                                                multiplies by it (0x00251939)
+0x134   f32             overlayScale           the overlay's scale: 1.0 from 0x00250F30 and 0x00251010 (0x00250FE6,
                                                0x0025127B), 0x00251EA0's first argument (0x00251EB2); read by the draw
                                                (0x00251931)
+0x138   u8              overlayRising          the overlay's direction: 1 from 0x00251010 (0x00251285), 0 from 0x00250F30
                                                (0x00250FF0), 0x00251EA0's third argument (0x00251ED1); the draw tests it
                                                (0x0025192A)
+0x139   u8[1]           gap139                 read and written by no function; nothing fixes its width
+0x13A   u16             overlayFrames          the overlay's length in frames: +0x120 from 0x00251010
                                                (0x0025126A), +0x122 from 0x00250F30 (0x00250FD0), 0x00251EA0's second argument
                                                (0x00251EC0); read by the stepper (0x00250CDF)
+0x13C   u32             overlayStart           the frame counter when the overlay started (0x0025125D, 0x00250FC3,
                                                0x00251EBA); 0 on creation and when it ends (0x00250AE6, 0x00250D09); the
                                                stepper counts from it (0x00250CC1)
```

## Shipped data

Counted in the decompiled `us` scripts (1,114 files); the calls and scripts per verb are in
[the census table](script-screen-effects-screen-effect-census.tsv), and the calls per argument list in
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
