---
title: "Script screen effects: cut-in, motion blur, soft focus and the screen blur sprites"
kind: "system"
category: "Graphics"
addresses: "020926E4, 0024D540, 00182B40, 02B59D20, 02092640, 0024CF50, 0024CEB0, 0024CBE0, 003AA6B0, 02B58C38, 02092678, 0024EC00, 0024EB20, 0024EA10, 003AAA50, 003DE160, 003DE210, 0036E810, 0024FAE0, 0024FA40, 003AB500, 00375B90, 02B58A80, 003DDF90, 0024E910"
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
  effect's bit in the flag word `020926E4`; clear releases the targets, drops the bit and ends in
  `0024C7C0`, which writes the ordinary draw mask back.
- A released target is appended to a 256-entry list at `02091950` (count `0209216A`) and freed
  later; only a full list frees it at once (`00182CA0`).
- The target allocator `00182B40` ignores its two scale arguments. It always asks for the render
  width by the render height × 512 / 448 (`00186AA0`, `00186A90`), so every target is full size.

- The targets come from a pool kept by `001B6C40()`: `001B66F0` finds the `A8`<sub>h</sub>-byte pool for the width,
  height and format (`02CF7480`), creating it with `001B6560` when missing, and `001B67F0` takes a free
  target from it or makes a new one (`001EE040`). `00182CA0` hands a target back through `001B68D0`,
  which finds its pool by the texture's width `+28`<sub>h</sub>, height `+2C`<sub>h</sub> and format (its first qword) and returns it (`001B6990`).

- The per-frame driver `0024D540` calls the three per-frame bodies with the draw index, 0 or 1,
  only while the main-loop state `00229EA0()` is 2 or 6 (`0024D6AA`-`0024D6B7`). The field frame
  `0022A770` is state 2 ([frame update order](../Engine-Core/frame-update-order.md)).

Each frame the bodies queue descriptors in the screen-effect pool of
[screen fades](screen-fades.md). Every handler returns 1 (keep) unless the descriptor's byte
`+1D`<sub>h</sub> names the draw in progress (`00358320`). Three steps recur:

1. Kind 3 copies the finished scene into a target.
2. Kind 4 (`00375B90`) binds an image to a block address of the emulated GS memory, the low 14
   bits of its qword `+30`<sub>h</sub> (`2A00`<sub>h</sub> on this page): with `+1C`<sub>h</sub> bit 0 it uploads the image at
   `+20`<sub>h</sub>, binds the texture at `+50`<sub>h</sub> to that address (`002D7E00`), and with bit 1 uploads the
   palette at `+28`<sub>h</sub>.
3. Quads of kinds 2, 5, 6, 7 and `0D`<sub>h</sub> sample that address.

The pool releases a descriptor when its handler returns 0: kind 4 does so once drawn when `+1C`<sub>h</sub>
bit 3 is set, kinds 2, 6 and `0D`<sub>h</sub> when bit 6 is set. Every descriptor this page builds sets its
bit, so an effect redraws only while its per-frame body keeps queueing, and stops the frame after
its flag bit drops.

### Cut-in

`cutinplay` (`003DF8F0`) passes the staging block `02B59D20` to `0024CF50`, which copies its `24`<sub>h</sub>
bytes to `02092640` and, only when bit 3 of the flag word is clear, allocates the target
`02092638` and raises bit 3. A second play replaces the parameters and keeps the target.
`cutinclear` (`003DF8E0` → `0024CEB0`) zeroes the type byte, releases the target and every
recorded handle, and drops bit 3.

The parameter verbs only write the staging block (layout below): `cutintype` (`0313`<sub>h</sub>, `003DF9F0`),
`cutinlinefade` (`0314`<sub>h</sub>, `003DF990`), `cutinpos` (`0315`<sub>h</sub>, `003DF9C0`), `cutinuv` (`0318`<sub>h</sub>,
`003DFA30`), `cutincolor` (`0319`<sub>h</sub>, `003DF950`) and `cutinlinecolor` (`031A`<sub>h</sub>, `003DF970`).

`0024CBE0` draws nothing while the live type byte is 0. In draw 0 it switches the draw mask bits
0-6 on for both draws and queues a kind-3 capture of the scene into `02092638` (stage 7,
`40703`<sub>h</sub>). In draw 1 it queues a kind-4 bind of that target and calls `003AA6B0`, which queues
two kind-`0D`<sub>h</sub> quads in stage 5:

- the picture: the block's position, rotation and colour, with texture coordinates from `(u, v)`
  to `(u + 1, v + 0.875)`, 448 over 512;
- for types 2, 3 and 4, the line: one of three line images built into the executable
  (`01EFD4A0`, `01EFD930`, `01EFDDC0`, each an indexed image and a 256-colour palette), made into
  textures once (`02B3F470`, `02B3F488`) and bound by a second kind 4, drawn with the line colour,
  the negated line width and a span of ±73 about its centre. Type 1 stops after the picture.

### Motion blur

`moveblurplay` (`003DE310`) passes the staging block `02B58C38` to `0024EC00`, which clears bit 4,
copies the 12 bytes to `02092678`, and releases both targets. With screen type 1 or 2 it allocates
two targets (`02092688`, `02092690`), raises bits 4 and 5 and zeroes the eight handles; with any
other screen type it returns with bit 4 clear. `moveblurclear` (`003DE140` → `0024EB20`) releases
both targets and drops bit 4. Its handle loop calls the release only for handles that are 0, which
releases nothing; the descriptors leave the pool on their own.

The four type verbs write the staging block with the mappings of the layout below:
`moveblurpresettype` (`031E`<sub>h</sub>, `003DE400`) byte `+00`<sub>h</sub>, `moveblurcluttype` (`031F`<sub>h</sub>, `003DE360`)
`+01`<sub>h</sub>, `moveblurnoisetype` (`0320`<sub>h</sub>, `003DE3A0`) `+02`<sub>h</sub> and `moveblurscreentype` (`0321`<sub>h</sub>,
`003DE430`) `+03`<sub>h</sub>.

`0024EA10`, in draw 0 with bit 4 up, builds the request for `003AAA50` with a capture flag: 1 when
bit 5 is up (and clears bit 5), otherwise 1 unless the capture-once bit is set. With the flag down,
`003AAA50` writes 1 to `01FD4A70`, and the scene draw `0022B0B0` answers by returning before it
draws (`0022B196`), so the scene is not drawn at all.

- Strength exactly 1.0, flag down and a third target `02092698` present: one kind-4 bind of that
  target and one kind-2 quad, the stored frame shown as it is. The third target is captured at the
  end of the first call that finds strength 1.0 and the flag down; any other strength releases it.
- Otherwise: a capture into the first target when the flag is up, kind-4 binds of both targets
  with the chosen mask table as palette, and three quads of kinds 5, 7 and 6 whose constants come
  from the preset.

`moveblurfade(frames)` (`003DE2A0`) and `moveblurclearfade(frames)` (`003DE240`) scale the frames
by the time base (`00265860`). A result of 0 plays or clears at once. Otherwise, when no blur fade
is running, they take a task record, keep it at `02B58C48` and give it the tick `003DE160`, the
end `003DE1F0`, the duration and a direction at `+28`<sub>h</sub> (0 in, 1 out); a fade asked for while one
runs is dropped.

Each tick plays a copy of the staging block whose strength is
`strength × t / duration`, or `× (1 − t / duration)` going out, so the scene is captured afresh
every tick until the fade ends. The end clears `02B58C48` and, going out, tail-jumps to the clear.
`moveblurfadesync` waits while `02B58C48` is non-zero (poll `00345100`, `003DE150`).

### Object motion blur

The five `objmblur*` verbs keep a `18`<sub>h</sub>-byte block at `02B58C20` and never draw anything:

- `objmblurlimitalpha(a)` (`01C5`<sub>h</sub>, `003DE460`) stores `a`, truncated, in byte `+01`<sub>h</sub>;
- `objmblurcolor(r, g, b)` (`01C6`<sub>h</sub>, `003DE450`) stores the three bytes at `+04`<sub>h</sub> to `+06`<sub>h</sub> and
  `80`<sub>h</sub> at `+07`<sub>h</sub>;
- `objmblurpower(p)` (`01C7`<sub>h</sub>, `003DE470`) stores the float at `+08`<sub>h</sub>;
- `objmblurplay(n)` (`01C3`<sub>h</sub>, `003DE480`) stores `n` in byte `+00`<sub>h</sub>, passes the block to the bare
  `ret` at `0016D6A0`, and resets it: zero, except `80`<sub>h</sub> at `+07`<sub>h</sub>;
- `objmblurclear` (`01C4`<sub>h</sub>) jumps through `0017E7D0` to the same `ret`.

The area initialiser `00266D10` resets the block with the same defaults through `003DDD10`, which
also resets the four blur sprites, the motion blur staging block and the blur fade task `02B58C48`.

### Soft focus

`setsoftfocusmode(on, mode, b, amount)` (`02AE`<sub>h</sub>, handler `0034FA00`) calls `0036E810`. With
`on` at 0 it calls the clear `0024FA40`. Otherwise it builds byte `+0` = 2 when `mode` is 1, else
1, byte `+1` = `b` and float `+4` = `amount`, and calls `0024FAE0`: bit 0 up, the block copied to
`020925F0`, a target allocated at `02092620` (a failed allocation drops bit 0 again) and byte
`+2` forced to 4.

`003AB500` runs in draw 0 when bit 0 is up (`0024D6C9`). Byte `+2` picks a size word, 4 → `40`<sub>h</sub>,
3 → `80`<sub>h</sub>, 2 → `100`<sub>h</sub>; since play always stores 4, it is `40`<sub>h</sub>. It sets the draw mask so draw 0
draws everything but the menu (bit 3) and draw 1 only bits 3 and 4, then queues a capture (stage 7,
`50703`<sub>h</sub>), a bind with the size word, and a kind-2 quad with `amount` and colour `80 80 80 80`.

### The mode-screen backdrop

When a mode screen such as game over opens, the last field picture stays behind it. `00251D90(type,
fadeIn, fadeOut)` creates the backdrop, a `140`<sub>h</sub>-byte widget with the message procedure `002509D0`, unless
one exists ([game over](../World-Areas-And-Travel/game-over.md) calls it with 1, 60, 120). Its create arm
stores it at `020927F0`, the type at `+E4`<sub>h</sub>, the two frame counts at `+120`<sub>h</sub> and `+122`<sub>h</sub>, progress 0 at
`+110`<sub>h</sub> and state 1 at `+E6`<sub>h</sub>.

- Types 0 and 1 take the first picture of the TIM2 at `[0209AC30] + 388h` (`0024A9E0`) and a palette
  from `[0209AC30] + 390h` (type 0) or `+ 3A8h` (type 1). The picture's texture `0209AC38` (`00184140`)
  and palette texture `0209AC40` (`001837A0`) are made once and kept.
- The teardown arm frees the capture buffer `+C0`<sub>h</sub> (`003697F0`), releases the three targets
  `+C8`<sub>h</sub>, `+D0`<sub>h</sub>, `+D8`<sub>h</sub> (`00182CA0`) and clears `020927F0`.

The scene draw `0022B0B0` calls `00251010` (`0022B61C`) to capture. For types 0 and 1 it allocates a
buffer in resource arena 2 (`0036C1D0`, `0036A100`) and two targets (`00182B40`). It queues two stage-7
captures (`50703`<sub>h</sub>) through that buffer into the two targets, starts the fade toward 1.0 (`00250E50`) and
sets state 3. After each stage-7 draw `00251E00` passes the buffer to `0036CAD0`.

The menu frames `0022B8C0` and `0022BC20` draw it each frame with `002512B0`:

1. Nothing is drawn while `+E8`<sub>h</sub> bit `4`<sub>h</sub> is set (`00251F00`). Types 2 and 3 draw one opaque black
   kind-2 quad in stage 5 (colour `00 00 00 80`) and stop.
2. For types 0 and 1, nothing is drawn while `00181DD0()` reports a camera override.
3. At full progress, once the composite target `+D8`<sub>h</sub> exists, it binds that target and draws it as a
   kind-2 quad, and stops. Below full progress the composite is released first.
4. It binds the second capture and draws it plainly while the progress is below 1.0. With `+E8`<sub>h</sub> bit
   `1`<sub>h</sub> set it then binds the first capture with the palette `+F8`<sub>h</sub> and the palette texture `0209AC48`. A kind-5 quad follows with strength bytes 25 and 6 (more in
   state 7), then two kind-7 quads at the overlay alpha and a fifth of it.
5. It binds the menu picture and draws a kind-2 quad in blend 2 (`2502`<sub>h</sub>, subtractive) at the
   progress `+110`<sub>h</sub>.
6. When the progress is exactly 1.0 and no composite exists, it allocates `+D8`<sub>h</sub> and queues a
   stage-5 capture into it (`50503`<sub>h</sub>).

`00250CA0` (from `002506D0`, field frame `0022A770`) moves the progress from its start `+114`<sub>h</sub> by `+118`<sub>h</sub>
along `00248F40(kind, frames, elapsed)`, counted on `0208F570`. The states are: 3 fading in (kind 1,
`+120`<sub>h</sub> frames) then 4; 5 fading out (`+122`<sub>h</sub> frames, kind 1, or kind 0 when `+E8`<sub>h</sub> bit `8`<sub>h</sub> is set
by `00251F20`) then 6; 7 a pulse of `+129`<sub>h</sub> strength over `+12A`<sub>h</sub> frames (`00250C50`) then 8.
`00250F30` starts the fade-out for types 0, 2, 3 and 4, `00251EA0(scale, frames, direction)` restarts the overlay alpha
`+130`<sub>h</sub> (eased the same way), and `00251E80` destroys the widget.

| `00248F40` kind | Value at `t = elapsed / frames` (1.0 once `elapsed ≥ frames`) |
|---|---|
| 1 | `sin(πt/2)` |
| 2 | `1 − sin((t/2 + 1/2)π)` |
| 3 | `0.5 − sin((t + 1/2)π) / 2` |
| 4 | `0.6 + 0.4 ×` a random value (`003A1D30`) |
| 5 | `0.4 + 0.3 sin(πt/2) + 0.3 t` |
| other | `t` |

`00251D20()` returns the state, or 2 when `+E8`<sub>h</sub> bit 0 is clear; `00251D50()` returns 1 when there is no
backdrop or its state is 0, 6 or 8. `00251EE0` sets the fade-out frames. `00250E90(palette)` swaps in
another palette (`+40`<sub>h</sub> past its header) through `00183760`, or, for types other than 2 and 3, restores
type 0's palette.

### The screen blur sprites

The `blur*` verbs drive four sprite records of `68`<sub>h</sub> bytes at `02B58A80`, index 0 to 3: a handle at
`+00`<sub>h</sub> and a `58`<sub>h</sub>-byte kind-2 descriptor at `+10`<sub>h</sub>. Each setter clamps the index into 0..3. The
original verbs `00C5`<sub>h</sub>-`00CE`<sub>h</sub> use index 0; the forms `0548`<sub>h</sub>-`0551`<sub>h</sub> pop the index as their
first argument.

| Verb | Body | Writes (descriptor offsets) |
|---|---|---|
| `blurplay` | `003DDF90` | files the descriptor, keeps the handle, resets the descriptor to the defaults |
| `blurstop` | `003DE060` | releases the handle; the descriptor stays |
| `bluralpha(a)` | `003DDE00` | `+34`<sub>h</sub> = `a`; flag nibble 7 when `a` is 0.08 (`0090035C`), else 3 |
| `blurcolor(r, g, b, a)` | `003DDE50` | `+38`<sub>h</sub> colour |
| `bluroffset(x, y)` | `003DDEB0` | `+20`<sub>h</sub>, `+24`<sub>h</sub> |
| `blurscale(x, y)` | `003DDF60` | `+28`<sub>h</sub>, `+2C`<sub>h</sub> |
| `blurrotate(r)` | `003DDF20` | `+30`<sub>h</sub> |
| `blurlayer(n)` | `003DDE80` | low nibble of `+1`, the stage |
| `blurtrans(n)` | `003DE110` | high nibble of `+1`, the blend of [screen fades](screen-fades.md) |
| `blurprior(n)` | `003DDEE0` | `+3`, the priority |

`blurplay` (`00343F10`) submits only when `00267310` reports 0 for the script's manager, and
otherwise resets the record without submitting (`003DDC50`). The defaults are kind 2, stage 6,
blend 3, class 1, flags 3, offset 0, scale 1.0, rotation 0, alpha 0.5 and colour `80FFFFFF`<sub>h</sub>.

Flags 3 leaves bit 6 clear, so a submitted sprite stays in the pool until `blurstop` or a reset.
The kind-2 handler `003745C0` multiplies the x offset by the 16:9 factor of
[screen mode and aspect](screen-mode-and-aspect.md). `003DE0A0` releases all four; the cutscene
skip paths `00360710`, `003601D0`, `00360A50` and `003600D0` call it.

### Area changes and skips

- The area unload `002628B0` and the area initialiser `00266D10` both call the cut-in reset
  `003DF900` and the motion blur reset `003DE320`, so no script needs `resetcutinparam` or
  `resetmoveblurparam`.
- `003DE210` ends a running blur fade (progress set to its duration, direction out), forgets the
  task and clears the blur. The unload, `003601D0` and `003600D0` call it.
- The effect teardown `0024E910` ends in the blur clear and the cut-in clear (`0024EA02`,
  `0024EA0B`); the unload and `003601D0` call it.
- The unload calls `0036E810` twice with all zeros, turning soft focus off.

### Crossfade

`crossfade(flags, mode, frames)` (`016F`<sub>h</sub>, `00353260`) dissolves a still of the picture into the
live scene. Unless the issuer's manager is skipping it calls `002F1A90(flags, mode, frames)`, which
acts when `frames` is positive or flag bit 1 is set:

- With no crossfade running it makes the task `[022BE7C8]` (`002F16B0`) with the per-frame body
  `002F18D0` and the end `002F1950`, and keeps the flags at `+28`<sub>h</sub>, the mode at `+38`<sub>h</sub> and the
  length `frames × [01DFE0B4]` (`frames` alone when `001EDDA0()` is non-zero) at `+04`<sub>h</sub>. Flag bit 1
  adds one frame to the length.
- It then captures the picture: `00374D40(0, mode, 1)`, or, with flag bit 2, `00374D40(0, mode, 2)`
  after a set of pass-mask calls (`003587B0(1)`, `00358720`, `00358640(1)` and others); `+30`<sub>h</sub>
  records which.
- With a crossfade already running, flag bit 0 replaces its flags and restarts the length.

`00374D40(p, mode, q)` works only for a mode of 1 to 4. It takes a screen-size target once
(`00182B40`, kept at `02ADB6D0` with the mode at `02ADB6D8`) and files a kind-3 descriptor, stage 7,
class 5, with bytes `+1C`<sub>h</sub> = 1, `+1D`<sub>h</sub> = mode, `+1E`<sub>h</sub> = `q` and `+1F`<sub>h</sub> = `p`, the target at
`+28`<sub>h</sub> and `+40`<sub>h</sub>; its handle goes to `02EC07F0`.

Each frame `002F18D0` re-captures when flag bit 2 is set and calls `003756B0(+30h, alpha)` with
`alpha = (L − c) / L × 255`, with `L` the length plus `[01DFE0B4]` and `c` the task's word `+00`<sub>h</sub>,
so the still fades out as `c` grows; it also sets
byte `+D18`<sub>h</sub> of the render manager (`00182610(1)`). `003756B0` files two descriptors while a target
and a mode exist:

- a kind-4 descriptor binding the target to the emulated GS memory, with a bind word that depends on
  the mode and, for modes 3 and 4, a palette at `02ADB720` or `02ADB6E0` (handle `02EC07F4`);
- a kind-2 quad, stage 5, class 1, priority 1, colour `80808080`<sub>h</sub> with alpha `alpha / 255`
  (handle `02EC07F8`).

The end `002F1950` runs `00375F80`, which hands the target back (`0024B240`) and removes the three
descriptors from the pool, undoes the pass-mask calls for flag bit 2, clears `[022BE7C8]` and byte
`+D18`<sub>h</sub> (`00182610(0)`). `0024B240(target)` appends a released target to the list `02091950` while
its count `0209216A` is below 256 and otherwise frees it at once (`001B68D0`).

## Layouts

```
Flag word 020926E4 (bits this page uses)
bit 0  soft focus up
bit 3  cut-in up
bit 4  motion blur up
bit 5  motion blur: capture on the next frame
```

Cut-in staging `02B59D20` / live `02092640` (`24`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | type | cutintype: 0-4 kept, else 2; 0 draws nothing; reset 2 |
| `01`<sub>h</sub> | `u8` | lineFade | bit 0: cutinlinefade; reset 0 |
| `04`<sub>h</sub> | `f32` | x | cutinpos; reset 0 |
| `08`<sub>h</sub> | `f32` | y | cutinpos; reset 0 |
| `0C`<sub>h</sub> | `f32` | rotation | cutinrotate, radians; reset 0 |
| `10`<sub>h</sub> | `f32` | lineWidth | cutinlinewidth; reset 2.0 |
| `14`<sub>h</sub> | `f32` | u | cutinuv; reset 0 |
| `18`<sub>h</sub> | `f32` | v | cutinuv; reset 0 |
| `1C`<sub>h</sub> | `u8[4]` | colour | cutincolor; reset 80 80 80 80 |
| `20`<sub>h</sub> | `u8[4]` | lineColour | cutinlinecolor; reset 00 00 00 80 |

Motion blur staging `02B58C38` / live `02092678` (`0C`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | preset | moveblurpresettype: 1->2, 2->3, else 1; reset 1 |
| `01`<sub>h</sub> | `u8` | mask | moveblurcluttype: 1->2, 2->3, 3->0, else 1; reset 1 |
| `02`<sub>h</sub> | `u8` | noise | moveblurnoisetype: 0-3 kept, else 0; reset 0; the builder ignores it |
| `03`<sub>h</sub> | `u8` | screenType | moveblurscreentype: 1->2, else 1; reset 1 |
| `04`<sub>h</sub> | `u8` | flags | bit 0 capture once (moveblurcaptureonce); reset 0 |
| `08`<sub>h</sub> | `f32` | strength | movebluraplpha; reset 0.5 |

Soft focus live block `020925F0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | mode | 1, or 2 for mode 1 |
| `01`<sub>h</sub> | `u8` | b | the third argument |
| `02`<sub>h</sub> | `u8` | size | always 4 |
| `04`<sub>h</sub> | `f32` | amount |  |
| `08`<sub>h</sub> | `void*` | target | copy of `02092620` |
| `10`<sub>h</sub> | `u32[3]` | handles |  |

Screen blur sprite `02B58A80` + index x `68`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | handle |  |
| `10`<sub>h</sub> | `u8` | kind | 2 |
| `11`<sub>h</sub> | `u8` | stageBlend | low nibble stage (6), high nibble blend (3) |
| `12`<sub>h</sub> | `u8` | class | 1 |
| `13`<sub>h</sub> | `u8` | priority | 0 |
| `2C`<sub>h</sub> | `u8` | flags | low nibble 3, or 7 for alpha 0.08 |
| `30`<sub>h</sub> | `f32` | offsetX |  |
| `34`<sub>h</sub> | `f32` | offsetY |  |
| `38`<sub>h</sub> | `f32` | scaleX | 1.0 |
| `3C`<sub>h</sub> | `f32` | scaleY | 1.0 |
| `40`<sub>h</sub> | `f32` | rotation | 0 |
| `44`<sub>h</sub> | `f32` | alpha | 0.5 |
| `48`<sub>h</sub> | `u8[4]` | colour | FF FF FF 80 |

Mode-screen backdrop ([`020927F0`]), `140`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `0C0`<sub>h</sub> | `void*` | capture buffer | arena 2 |
| `0C8`<sub>h</sub> | `void*` | first target | +`0D0`<sub>h</sub> second target, +`0D8`<sub>h</sub> composite |
| `0E4`<sub>h</sub> | `i16` | type | 0-3 |
| `0E6`<sub>h</sub> | `i16` | state | 1 created, 3-4 in, 5-6 out, 7-8 pulse |
| `0E8`<sub>h</sub> | `u32` | flags | bit `1`<sub>h</sub> set on create, `4`<sub>h</sub> hidden, `8`<sub>h</sub> linear fade-out |
| `0F8`<sub>h</sub> | `void*` | overlay palette |  |
| `100`<sub>h</sub> | `void*` | picture pixels | +`108`<sub>h</sub> picture palette |
| `110`<sub>h</sub> | `f32` | progress | +`114`<sub>h</sub> start, +`118`<sub>h</sub> span, +`11C`<sub>h</sub> start frame |
| `120`<sub>h</sub> | `u16` | fade-in frames | +`122`<sub>h</sub> fade-out frames |
| `124`<sub>h</sub> | `f32` | pulse progress | +`128`<sub>h</sub> u8 25, +`129`<sub>h</sub> u8 pulse strength, +`12A`<sub>h</sub> u16 pulse frames |
| `12C`<sub>h</sub> | `u32` | pulse start frame |  |
| `130`<sub>h</sub> | `f32` | overlay alpha | +`134`<sub>h</sub> scale, +`138`<sub>h</sub> u8 direction, +`13A`<sub>h</sub> u16 frames, +`13C`<sub>h</sub> start |

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
  effects write and the early return on `01FD4A70`.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the effect verbs.
- [Frame update order](../Engine-Core/frame-update-order.md): the main-loop states.
