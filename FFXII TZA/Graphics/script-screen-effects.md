---
title: "Script screen effects: cut-in, motion blur, soft focus and the screen blur sprites"
kind: "system"
category: "Graphics"
summary: "The screen effects scripts start over the finished picture: how the cut-in, motion blur and soft focus capture the frame into a render target and draw it back through the screen-effect pool, their staging blocks, play and clear bodies and per-frame builders, the motion blur fade and the held-frame path behind the item-obtained message, the four screen blur sprites of the blur verbs, what an area change and a cutscene skip reset, and how often the shipped scripts use each verb."
addresses: ["020926E4", "0024D540", "00182B40", "02B59D20", "02092640", "0024CF50", "0024CEB0", "0024CBE0", "003AA6B0", "02B58C38", "02092678", "0024EC00", "0024EB20", "0024EA10", "003AAA50", "003DE160", "003DE210", "0036E810", "0024FAE0", "0024FA40", "003AB500", "00375B90", "02B58A80", "003DDF90", "0024E910"]
---

# Script screen effects: cut-in, motion blur, soft focus and the screen blur sprites

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
- The per-frame driver `0024D540` calls the three per-frame bodies with the draw index, 0 or 1,
  only while the main-loop state `00229EA0()` is 2 or 6 (`0024D6AA`-`0024D6B7`). The field frame
  `0022A770` is state 2 ([frame update order](../Engine-Core/frame-update-order.md)).

Each frame the bodies queue descriptors in the screen-effect pool of
[screen fades](screen-fades.md). Every handler returns 1 (keep) unless the descriptor's byte
`+0x1D` names the draw in progress (`00358320`). Three steps recur:

1. Kind 3 copies the finished scene into a target.
2. Kind 4 (`00375B90`) binds an image to a block address of the emulated GS memory, the low 14
   bits of its qword `+0x30` (`0x2A00` on this page): with `+0x1C` bit 0 it uploads the image at
   `+0x20`, binds the texture at `+0x50` to that address (`002D7E00`), and with bit 1 uploads the
   palette at `+0x28`.
3. Quads of kinds 2, 5, 6, 7 and `0x0D` sample that address.

The pool releases a descriptor when its handler returns 0: kind 4 does so once drawn when `+0x1C`
bit 3 is set, kinds 2, 6 and `0x0D` when bit 6 is set. Every descriptor this page builds sets its
bit, so an effect redraws only while its per-frame body keeps queueing, and stops the frame after
its flag bit drops.

### Cut-in

`cutinplay` (`003DF8F0`) passes the staging block `02B59D20` to `0024CF50`, which copies its 0x24
bytes to `02092640` and, only when bit 3 of the flag word is clear, allocates the target
`02092638` and raises bit 3. A second play replaces the parameters and keeps the target.
`cutinclear` (`003DF8E0` → `0024CEB0`) zeroes the type byte, releases the target and every
recorded handle, and drops bit 3.

`0024CBE0` draws nothing while the live type byte is 0. In draw 0 it switches the draw mask bits
0-6 on for both draws and queues a kind-3 capture of the scene into `02092638` (stage 7,
`0x40703`). In draw 1 it queues a kind-4 bind of that target and calls `003AA6B0`, which queues
two kind-`0x0D` quads in stage 5:

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
end `003DE1F0`, the duration and a direction at `+0x28` (0 in, 1 out); a fade asked for while one
runs is dropped.

Each tick plays a copy of the staging block whose strength is
`strength × t / duration`, or `× (1 − t / duration)` going out, so the scene is captured afresh
every tick until the fade ends. The end clears `02B58C48` and, going out, tail-jumps to the clear.
`moveblurfadesync` waits while `02B58C48` is non-zero (poll `00345100`, `003DE150`).

### Soft focus

`setsoftfocusmode(on, mode, b, amount)` (`0x02AE`, handler `0034FA00`) calls `0036E810`. With
`on` at 0 it calls the clear `0024FA40`. Otherwise it builds byte `+0` = 2 when `mode` is 1, else
1, byte `+1` = `b` and float `+4` = `amount`, and calls `0024FAE0`: bit 0 up, the block copied to
`020925F0`, a target allocated at `02092620` (a failed allocation drops bit 0 again) and byte
`+2` forced to 4.

`003AB500` runs in draw 0 when bit 0 is up (`0024D6C9`). Byte `+2` picks a size word, 4 → `0x40`,
3 → `0x80`, 2 → `0x100`; since play always stores 4, it is `0x40`. It sets the draw mask so draw 0
draws everything but the menu (bit 3) and draw 1 only bits 3 and 4, then queues a capture (stage 7,
`0x50703`), a bind with the size word, and a kind-2 quad with `amount` and colour `80 80 80 80`.

### The screen blur sprites

The `blur*` verbs drive four sprite records of 0x68 bytes at `02B58A80`, index 0 to 3: a handle at
`+0x00` and a 0x58-byte kind-2 descriptor at `+0x10`. Each setter clamps the index into 0..3. The
original verbs `0x00C5`-`0x00CE` use index 0; the forms `0x0548`-`0x0551` pop the index as their
first argument.

| Verb | Body | Writes (descriptor offsets) |
|---|---|---|
| `blurplay` | `003DDF90` | files the descriptor, keeps the handle, resets the descriptor to the defaults |
| `blurstop` | `003DE060` | releases the handle; the descriptor stays |
| `bluralpha(a)` | `003DDE00` | `+0x34` = `a`; flag nibble 7 when `a` is 0.08 (`0090035C`), else 3 |
| `blurcolor(r, g, b, a)` | `003DDE50` | `+0x38` colour |
| `bluroffset(x, y)` | `003DDEB0` | `+0x20`, `+0x24` |
| `blurscale(x, y)` | `003DDF60` | `+0x28`, `+0x2C` |
| `blurrotate(r)` | `003DDF20` | `+0x30` |
| `blurlayer(n)` | `003DDE80` | low nibble of `+1`, the stage |
| `blurtrans(n)` | `003DE110` | high nibble of `+1`, the blend of [screen fades](screen-fades.md) |
| `blurprior(n)` | `003DDEE0` | `+3`, the priority |

`blurplay` (`00343F10`) submits only when `00267310` reports 0 for the script's manager, and
otherwise resets the record without submitting (`003DDC50`). The defaults are kind 2, stage 6,
blend 3, class 1, flags 3, offset 0, scale 1.0, rotation 0, alpha 0.5 and colour `0x80FFFFFF`.

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

## Layouts

```
Flag word 020926E4 (bits this page uses)
bit 0  soft focus up
bit 3  cut-in up
bit 4  motion blur up
bit 5  motion blur: capture on the next frame
```

```
Cut-in staging 02B59D20 / live 02092640 (0x24)
+0x00  u8      type        cutintype: 0-4 kept, else 2; 0 draws nothing; reset 2
+0x01  u8      lineFade    bit 0: cutinlinefade; reset 0
+0x04  f32     x           cutinpos; reset 0
+0x08  f32     y           cutinpos; reset 0
+0x0C  f32     rotation    cutinrotate, radians; reset 0
+0x10  f32     lineWidth   cutinlinewidth; reset 2.0
+0x14  f32     u           cutinuv; reset 0
+0x18  f32     v           cutinuv; reset 0
+0x1C  u8[4]   colour      cutincolor; reset 80 80 80 80
+0x20  u8[4]   lineColour  cutinlinecolor; reset 00 00 00 80
```

```
Motion blur staging 02B58C38 / live 02092678 (0x0C)
+0x00  u8      preset      moveblurpresettype: 1->2, 2->3, else 1; reset 1
+0x01  u8      mask        moveblurcluttype: 1->2, 2->3, 3->0, else 1; reset 1
+0x02  u8      noise       moveblurnoisetype: 0-3 kept, else 0; reset 0; the builder ignores it
+0x03  u8      screenType  moveblurscreentype: 1->2, else 1; reset 1
+0x04  u8      flags       bit 0 capture once (moveblurcaptureonce); reset 0
+0x08  f32     strength    movebluraplpha; reset 0.5
```

```
Soft focus live block 020925F0
+0x00  u8      mode        1, or 2 for mode 1
+0x01  u8      b           the third argument
+0x02  u8      size        always 4
+0x04  f32     amount
+0x08  ptr     target      copy of 02092620
+0x10  u32[3]  handles
```

```
Screen blur sprite 02B58A80 + index x 0x68
+0x00  u32     handle
+0x10  u8      kind        2
+0x11  u8      stageBlend  low nibble stage (6), high nibble blend (3)
+0x12  u8      class       1
+0x13  u8      priority    0
+0x2C  u8      flags       low nibble 3, or 7 for alpha 0.08
+0x30  f32     offsetX
+0x34  f32     offsetY
+0x38  f32     scaleX      1.0
+0x3C  f32     scaleY      1.0
+0x40  f32     rotation    0
+0x44  f32     alpha       0.5
+0x48  u8[4]   colour      FF FF FF 80
```

## Shipped data

Counted in the decompiled `us` scripts (1,114 files); the calls and scripts per verb are in
[the census table](script-screen-effects-screen-effect-census.tsv):

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
