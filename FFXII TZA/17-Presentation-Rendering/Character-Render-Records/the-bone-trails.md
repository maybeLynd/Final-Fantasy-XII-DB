---
system: Bone trails - the sixteen-sample base-and-tip histories a model's FCP section 4 asks for, from the authored command that switches them on to the VU1 program they are handed to
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the pool's eight routines (0051C270 init, 0051CC30 create, 0051CC10 switch off, 0051BC10 release,
    0051CDC0 opacity, 0051C3C0 per-frame update, 0051BC70 draw) and the path into them (00520160, 00425E70, 003E6770,
    00422170, 003711D0) disassembled from the authority image and read whole, 2026-09-19; whole-image displacement and
    RIP sweeps for the record byte +0x3D0 and the pool header 02CA8400..02CA8404; the descriptor format the code
    implies then parsed out of all 216 FCP blocks that have a section 4 in an extracted copy of the game
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-bone-trails-falsification-pass-1
  note: written by FABLE. Grew out of correcting my own "pool 02CA8420 byte +5 has no reader" on the time-stop page.
    Static plus one data census. NOT read - the VU1 microprogram 0053F490 (5,417 B) that turns the histories into
    geometry, so the on-screen shape is an inference and is labelled as one (but its PLACEMENT is now
    established, 2026-09-20 FABLE: it is taken by address exactly once in the image, at 0051C147, as the
    r8 handler of the 0x488-byte render command registered through 003A35E0, and the registering function
    0051BC70 is reached by a tail jump from RenderResourceRoot_RunPhase2ModelInstancePass 0041E4D0 - so it
    is on the live model-instance phase-2 path, NOT the abandoned PS2 packet cluster; and the
    append-versus-drain question that wording left open is ANSWERED, 2026-09-20 FABLE - 001DB840 ends in 001FB840,
    which tail-jumps the command's vtable slot 0, so the packet is interpreted and the microprogram is CALLED inside
    the registrar, while only the GS replay is deferred, and the trail's own template carries the MSCALF that calls it
    - section 5a); the sibling sampler 003712C0; the three
    callers of the immediate release. Pending first review
---

# Bone trails

A model can ask, in **section 4 of its FCP block** ([the FCP block](../Model-And-Motion-Formats/fcp-character-parameter-block.md)),
for up to four **trails**: each names one bone, and while the trail is on the engine records where that bone's **base**
and **tip** were on each of the last sixteen samples, together with a smoothed direction of travel and two speed
figures, and hands the lot to a legacy vertex program every frame. 202 of the 216 models that carry a section 4 are
weapons, and in 178 of those the bone is bone 2 - the blade. Trails are switched on and off by an **authored
presentation command**, fade in over two steps and out over five, and free themselves when they have faded out.

What the vertex program draws from the histories was **not read** (section 5). Everything the C side does says
"a textured strip laid through the base and tip points, sixteen samples long" - two points per sample, a parameter of
32, one 64 x 64 image, an opacity - but that sentence is an inference and nothing below depends on it.

## 1. The descriptor - FCP section 4

`003E6770` finds the section through the payload's offset word `+8`, reads a `u32` count, caps it at four, and walks
`0x50`-byte descriptors from `+0x10`. The create routine copies a descriptor whole into the entry's `+0x370`, so the
entry's tail **is** the descriptor:

| descriptor | entry | what reads it |
|---|---|---|
| `+0x00` u8 | `+0x370` | draw, `0051BE6A`: non-zero = use the image that follows the descriptors instead of the engine's own |
| `+0x02` u16 | `+0x372` | the bone sampled (`0051C504`, `0051CD4C`) |
| `+0x04` u16 | `+0x374` | **written at run time** by the builder: the owning render record's index (`-1` = none) |
| `+0x08` f32 | `+0x378` | uploaded as a program parameter |
| `+0x0C` f32 | `+0x37C` | copied to entry `+0x14` on every update (`0051CA67`) and uploaded |
| `+0x10` 4 x f32[4] | `+0x380`..`+0x3BF` | uploaded as four vector parameters |

**What the files hold** (`census.py`, all 216 blocks, 238 descriptors): the own-image byte is **0 in every
descriptor**, so the branch that binds a model-supplied image is never taken by shipped data and the section is, in all
216 blocks, the last thing in the payload with nothing after it; word `+4` is 0 in every file; float `+8` is 1.0 in
all 238; float `+0xC` is 2.0 in 235 (2.4, 2.6 and 3.0 once each); the four vectors are zero in all 238. So in shipped
data a descriptor says one thing: **which bone**. Bones: 2 in 202 descriptors, 3 in 20, 4 in 3, and 0, 20, 41-44 and
54 in the rest. By folder: weapon 202 blocks, gadget 9, summon 4 (two of them with four trails, on bones 41-44),
monster 1.

## 2. Switching a trail on and off

| step | body | what it does |
|---|---|---|
| command | `00520160` (23 B) | authored presentation command `0x11` of bank A ([the handlers](../Authored-Commands/the-authored-presentation-command-handlers.md)): stores the command's byte `+2` in render record `+0x3D0` and raises bit 24 of `+0x294` |
| dirty pass | 00427DE0 at `0042858C` | when bit 24 is up, calls `00425E70(record, byte +0x3D0)` |
| fan-out | `00425E70` (202 B) | applies the state to the record, to its child `+8`, and - through the hierarchy walker with the eight-byte forwarder `0042BDD0` - to the hierarchies under that child's `+8` and `+0xA`. This is how a command addressed to a character reaches the weapon in its hand |
| build / switch off | `003E6770` (276 B) | **on**: if the record's first trail handle (`+0x438`) is `0xFFFF`, creates one entry per descriptor and stores the handles at `+0x438`..`+0x444`. **off**: calls `0051CC10` on each handle and sets the four back to `0xFFFF` |

A whole-image sweep for byte accesses at displacement `0x3D0` finds one writer on a render record, the command handler;
the others are a UI widget of the same size class. A second route switches trails **off** only: 0042F250 (70 B), which
also rewrites three bits of `+0x290`; its callers are the handbook viewer's loader and 003B8260, neither read here.

**Switching off is not release.** `0051CC10` (26 B) only clears the entry's byte `+4`; the entry keeps running and
drawing while it fades, and unlinks itself when the fade reaches zero. The record forgets the handle at once, which is
safe because a handle is `serial << 8 | slot` and every routine that takes one compares it with the entry's own `+0`
first. `0051BC10` (93 B) is the immediate release - handle zeroed, unlinked, count down - with three callers on the
record-teardown side (003E74C0, 0041E860, 004213E0).

## 3. The pool

`0051C270` (265 B), called from the render root's subcontainer init, allocates `0x3C00` bytes - sixteen entries of
`0x3C0` - at `02CA8420`, clears every entry's handle, and zeroes the header: live count `02CA8400` (u16), a flag byte
`02CA8402`, the serial `02CA8404`, list head `02CA8408` and tail `02CA8410`. It also registers the engine's trail image:
a 64 x 64 eight-bit indexed picture with a 256-entry palette, embedded in the executable at `01F2A220`.

`0051CC30` (create, 385 B) takes the first entry whose handle is 0 - none free means no trail, silently - and sets:

| entry | |
|---|---|
| `+0x00` u32 | handle = `serial << 8 | slot`; the serial wraps to 1 above `0xFFFFFF` |
| `+0x04` u8 | **on** (1 at create; `0051CC10` clears it) |
| `+0x05` u8 | flags, 0 at create: bit 0 = do not update, bit 1 = do not draw. System-stop set 3 writes this byte ([the time stop](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md)) |
| `+0x06` u8 | samples held, 1..16 |
| `+0x07` u8 | alternator, flipped every update |
| `+0x08` f32 | owner's opacity, 1.0 at create; `0051CDC0` stores the character's final opacity here each frame ([the fade](how-a-character-fades-the-ten-channels.md)) |
| `+0x0C` f32 | 20.0 at create; no reader found in the pool's own routines |
| `+0x10` f32 | **fade**, 0 at create |
| `+0x14` f32 | the descriptor's `+0xC`, refreshed each update |
| `+0x18`, `+0x20` | previous, next |
| `+0x30` f32[4] x 16 | **tip** history; `w` = a tip speed figure |
| `+0x130` f32[4] x 16 | **base** history; `w` = a base speed figure |
| `+0x230` f32[4] x 16 (+ `0x40` more) | direction history; slot 0's `w` = distance the tip moved in the last sample |
| `+0x330`, `+0x334` f32 | the angle the blade turned between the last two samples (section 4, step 4); `+0x334` is its value when the second sample arrived |

It then takes the first sample and appends the entry to the list.

**The sample.** `00422170` (121 B) resolves the record's model instance and calls `003711D0` (232 B) - or 003712C0,
not read, when the instance's first flag byte has bit 7. `003711D0` refuses a bone index at or beyond the skeleton's
count, copies the bone's world position (`+0xB0`..`+0xBC` of its `0x290`-byte runtime record) out as the **base**, and
builds the **tip** by pushing the point `(length, 0, 0, 1)` through the bone's matrix at `+0x80`, where `length` is
the float at `+0x74` of the bone's `0x4C`-byte definition. A trail therefore runs along the bone's own x axis for the
bone's authored length; nothing in the descriptor sets how long it is.

## 4. The per-frame update - `0051C3C0` (2,128 B)

Called once a frame from the render root's presentation update. It walks the **list**, never the pool base - which is
why a scan for references to `02CA8420` does not find it. For each entry:

1. **Frozen?** If bit 0 of `(entry +5 | 02CA8402)` is set, skip the entry entirely (`0051C450`..`0051C45C`). The
   global byte is written only by the init, with 0, in a whole-image RIP sweep, so in practice the test is the entry's
   own byte.
2. **Shift.** On alternate updates - or on every update when the frame limiter's half-rate gate says so (a 27-byte getter of the core runtime, by role) - the sample count
   goes up by one to at most sixteen and the three histories move down one slot (`0051C471`..`0051C4CF`). The
   alternator flips regardless.
3. **Sample** slot 0 afresh (`0051C516`), if the owner record index is valid and the record is live.
4. **Measure.** The distance the tip moved and the distance the base moved since the previous sample; the blade
   direction (tip minus base, normalised, with a `1e-6` floor) now and one sample ago; their dot product, turned into
   the **angle** between them, in radians, by the 16,384-entry arccosine table at `00D12590` indexed by
   `(dot + 1) / 2` (`0046F460`, 75 B; the table reads 3.14159 at its first entry, 1.5708 at its middle, 0 at its
   last), stored at `+0x330`.
5. **Direction.** A unit vector stored in direction slot 0: from the current tip toward a point half-way back along
   the tip's last step, displaced by that step turned a quarter-turn about the axis the blade is swinging around (the
   cross product of the two blade directions, `00202E10`, 115 B) and scaled to `0.2 x tip distance x angle`
   (`0051C92C`..`0051CA5E`). A tangent for the newest sample that bows outward with the swing, not a position.
6. **Speed figures.** `w` of tip slot 0 = `max(tip distance, 0.8 x angle x tip distance)`, and the same for the base
   (`0051CA88`..`0051CAB7`). On the update where the count is exactly 2 these are copied into slot 1 as well, so the
   first segment does not start from zero.
7. **Fade.** While **on**: `fade += 0.5 x step`, capped at 1.0. While off: `fade -= 0.2 x step`, and at or below zero
   the entry **releases itself** - handle zeroed, unlinked, live count down (`0051CB36`..`0051CB6C`). `step` is the
   frame-rate time base `01DFE0BC`, 1.0 at the authored rate: two updates in, five out.

## 5. The draw - `0051BC70` (1,525 B)

The render root's phase-2 model pass ends by jumping here (`0041E4EF`). It first runs **display layer 3** of the effect
system ([the six layers](../Effect-File-Formats/the-six-vfx-display-layers.md)) - so layer-3 effects are drawn
immediately before the trails, inside the same bracket - binds the engine's trail image and palette, copies a
`0x4A0`-byte parameter template from `02CA8A90`, and then for each listed entry:

- **skips it** when bit 1 of `(entry +5 | 02CA8402)` is set, when it holds fewer than two samples, or when its opacity
  `+8` is not above zero (`0051BE40`..`0051BE64`);
- if the descriptor's own-image byte is set, binds the image that follows the owner model's descriptors through
  `003E6D80` - the branch no shipped model takes (section 1);
- copies the three histories (`0x100` bytes each) and a parameter block into the template - `0x20`, the sample count,
  `+0x14`, **`fade x opacity`** (`0051C15A`..`0051C16C`), the descriptor's float `+8` and its four vectors - and
  queues one render command of `0x488` bytes with the VU1 microprogram `0053F490` through the registrar 003A35E0
  ([the VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md)).

**No vertex is built on this side.** The strip, if it is one, is made by the 5,417-byte recompiled vertex program,
which was not read; its first lines convert a count to float and form `1 / (count - 1)`, which is what a program
spreading a texture coordinate along a sample history would do, and is as far as this page goes.

## 5a. The program is called, and the call is in the trail's own packet (FABLE, Claude Opus 5, 2026-09-20)

Section 5 said the draw "queues one render command"; the audit note asked whether that command is ever consumed. **It
is, and the microprogram runs inside `0051BC70` itself**, because `001DB840` ends in `001FB840`, which tail-jumps the
command's vtable slot 0 — `001DB550`, the VIF1 interpreter
([the VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.1c). Only the replay of the resulting GS packets is
deferred, to the render pass list `00187950`.

**The `0x4A0`-byte template is a VIF1 packet, and `005409C0` builds it once.** The pool's init `0051C270` calls
`005409C0(02CA8A90)` at `0051C2F3`; that routine memsets `0x4A0` bytes and then writes named fields — and the fields at
the boundaries are VIF command words, whose code is the **top byte**:

Each is one 32-bit VIF1 code word — the command in the top byte, its fields below, exactly as the interpreter
`0022C970` reads them — and the table gives the code, the fields and the `005409C0` store that writes it:

| template offset | VIF1 code | fields | what it is | the store |
|---|---|---|---|---|
| `+0x08` | `0x03` BASE | 0 | the word the draw passes as the registrar's **first** argument (`0051C14E`) | `005409D6` |
| `+0x0C` | `0x02` OFFSET | 0 | the **second** argument (`0051C143`) | `005409DF` |
| `+0x18` | `0x01` STCYCL | CL 4, WL 4 | the first word of the `0x488`-byte payload (`0051C13E`) | `005409E6` |
| `+0x1C` | `0x6C` UNPACK | NUM `0x45`, ADDR 0 | the first unpack of the parameter block | `005409ED` |
| `+0x424` | `0x10` FLUSHE | 0 | | `00540B71` |
| `+0x470` | `0x15` **MSCALF** | address 0 | **the call into the microprogram** | `00540BD4` |
| `+0x474` | `0x11` FLUSH | 0 | | `00540BDE` |
| `+0x47C` | `0x50` DIRECT | count 1 | one `0x10`-byte GIF packet follows | `00540BE9` |
| `+0x490` | `0x13` FLUSHA | 0 | | `00540C05` |

The three arguments line up exactly: `0x18 + 0x488 = 0x4A0`, so the payload the draw hands the registrar is the template
**from `+0x18` to its end**, and the two words before it are the BASE/OFFSET pair the registrar sends as its own chunk.
`001DB840`'s MPG chunk installs `0053F490` at VU address 0, and the MSCALF at `+0x470` — address field 0 — is what calls
it.

**So the trail histories do reach the vertex program, every frame a trail is visible**, and the only thing still
unread is what the program computes from them. The inference in section 5 about a textured strip is unchanged and is
still an inference.

**One neighbour of that drain crosses a layer line.** The render pass list `00187950` also calls the singleton getter
pair `00182E80` / `00182EB0`, which the function list still tags **Audio**
([the ownership boundary](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md)
already rows them as a reclassify pair). Each tests the framework singleton, forwards it to a four-byte field reader
when it exists, and otherwise returns a constant — `0x438` and `0x780`, 1080 and 1920 — so the pair reads like
**display height and width**, and the Audio tag like an ownership artefact rather than a sound path. *That last step is
an inference from the two constants; the ownership page reads the same fallbacks as IDs.*

### 5b. `0053F490` mapped, not read — where its loop is and what it iterates over (FABLE, Claude Opus 5, 2026-09-20)

*A structural map only. It says where to start in 5,417 bytes and what the main loop runs over; it does **not**
say what the program draws, and section 5's inference about a textured strip is unchanged.*

**Everything it touches is the emulated VU machine.** The prologue loads the VU memory base **once** —
`0053F4B6  lea r14, [rip + …]` → `02064E30` — and every data access is `[index + r14]` with the index shifted
left by four, the VI-style addressing
[the VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.2 documents. **A rip-relative census cannot
see that traffic**: all **143** of the body's rip-relative writes land in `02064B00`–`02064DE8`, the *register
bank*, not in VU memory. It makes only two external calls, both to `0022CC20`, fifteen bytes that are ~~a VU status clear~~ a **constant-vector restore**: it stores
(0, 0, 0, 1.0) from `008C5FD0` into `01E02830`, the vector that the translated VU1 microprograms read lane by lane
(OPUS counts about 65; the VU `vf00` reading is an inference). The VU status word `02064DEC` is set only by
`0022CC30` / `0022CC40`. *(Corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 282.)*

**Three loops, and one of them is the body.**

| back edge | span | what it is |
|---|---:|---|
| `0053F930` ← `0053F94D` | 29 B | a setup loop |
| `0053FAE0` ← `0053FB48` | 104 B | an inner loop with an unconditional back edge |
| **`0053FAD0` ← `005408F0`** | **3,616 B** | **the main loop — two thirds of the function** |

The main loop is a countdown on a 16-bit VI register, mirrored into the bank cell `02064DD4` at its head
(`0053FAD0  dec dx`; `005408ED  test dx, dx / jg`).

**And its trip count is data, not a constant.** `0053F995` is `movzx edx, word ptr [r9 + r14 + 8]` — the count
is read **out of the uploaded parameter block**, from the `+8` half of one quadword. *So the program runs once
per uploaded sample, and section 5's sixteen is the value the C side writes rather than anything baked into the
program.*

**Where its output goes.** Quadword stores through the same base inside the main loop — `005407C2`, `005407F3`,
`0054080F`, `00540829`, `00540861`, `0054086D` — each `movups [index + r14], xmm`, with two separate `+0xC`
dword writes (`00540878`, `0054087D`) setting the fourth component, and a three-store epilogue after the loop
(`00540932`, `0054094E`, `00540955`). **Eighteen 16-bit bank cells** serve as its indices, in two groups:
`02064B0C`–`02064B16` in the prologue and `02064DB0`–`02064DE8` in the main loop.

**What a reader gets from this:** start at `0053FAD0`, read one iteration, and the six quadword stores in it are
the per-sample output. **What is still unknown is what those quadwords mean** — which is `UQ-213` for this
program, and the reason section 5's strip remains an inference.

### 5c. One iteration, read — six cells, and a conditional fourth component on the last two (FABLE, same day)

*The bounded read §5b set up. It does not name the GS registers, so `UQ-213` stays open; what it adds is the
**shape** of a sample's output.*

**The six stores land in one contiguous group of cells**, addressed from two running indices — a cell base in
`rsi` and a byte index in `r8d` — each scaled by `shl …, 4`:

| store | cell |
|---|---|
| `005407C2` | `r8d` |
| `005407F3` | `rsi + 3` |
| `0054080F` | `r8d + 0x10` |
| `00540829` | `rsi + 4` |
| `00540861` | `rsi + 2` |
| `0054086D` | `rsi + 5` |

So an iteration fills **`rsi+2` … `rsi+5` plus a pair at `r8` and `r8 + 0x10`** — four cells in one run and two
in another, which is the arrangement a per-sample vertex group has when its positions and its attributes live in
different areas of VU memory.

**The values are VF registers, not constants.** The `movups xmm0, [rip + …]` immediately before three of the
stores read `02064BC0`, `02064BD0` and `02064C10` — addresses **inside the register bank**, not `.rdata`. *A
reader who decodes those sixteen bytes from the file image gets padding and a meaningless float*; they are
whole-VF reads, and their contents only exist at run time.

**And the last two cells get a conditional fourth component:**

```asm
00540872  cmp  r12w, r15w
00540876  je   00540882          ; equal -> skip both writes
00540878  mov  dword ptr [rdx + r14 + 0xc], eax
0054087D  mov  dword ptr [r8  + r14 + 0xc], eax
```

`r12w` is advanced inside the iteration (`005407A5  add r12w, r9w`) and `r15w` is its limit, so **the write
happens on every sample except the one where the counter reaches the limit.** *The fourth component of a
quadword is where a PS2 vertex carries its ADC / skip flag, so "set a flag on these two cells for every sample
but one" has the shape of a strip that suppresses one segment — which would be the join between the two ends
section 5 infers.* **That last sentence is a reading of the shape, not a derivation**: nothing here decodes the
GIF tag that would say which component is which.

**Still not claimed:** which GS register each cell carries, and therefore what is drawn. That is `UQ-213`.

### 5d. The program builds its own GIF tag — which makes the register list statically readable (FABLE, same day)

*The step that turns `UQ-213` for this program from "read a 5,417-byte float body" into "decode sixteen bytes of
`005409C0`'s template".*

**The packet does not describe the vertices.** The trail template's `DIRECT` at `+0x47C` carries one quadword,
and `005409C0` writes it as `qword[+0x480] = 0x8000` with `+0x488` left zero — `NLOOP = 0`, `EOP = 1`, every
other field zero. **That is an empty terminator**, exactly the shape
[the VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.4a reports for 28 of the 29 `DIRECT` payloads
in the whole template census. *So nothing in the packet says what the cells mean.*

**The program writes the tag itself, in its epilogue, once the loop has finished counting:**

```asm
00540905  movups xmm1, xmmword ptr [rax + r14]  ; a cell the template supplied
0054090A  mov    eax, 0xFFFF8000
0054090F  add    cx, ax                         ; 16-bit: sets bit 15 of the count
00540919  movzx  edx, cx
00540932  mov    dword ptr [r9 + r14], edx      ; tag +0 : NLOOP = count, EOP = 1
0054094E  movsd  qword ptr [r9 + r14 + 4], xmm0 ; tag +4 .. +B
00540955  movd   dword ptr [r9 + r14 + 0xc], xmm1 ; tag +C .. +F, from psrldq xmm1, 0xC
```

Bit 15 of a GIF tag's first dword is **EOP** and bits 0–14 are **NLOOP**, so `count | 0x8000` is a tag that ends
the packet after however many items the main loop emitted. *The program counts its own output and stamps the
count into the tag* — which is why the loop's trip count could be data (§5b) without anything downstream needing
to know it.

**And the rest of the tag is copied, not computed.** The upper twelve bytes come from `xmm0` and from `xmm1`,
and `xmm1` was loaded at `00540905` **out of a VU cell** — one of the twenty-seven the template's
`UNPACK V4-32 num=27` at `+0x1C` uploads from `005409C0`'s own bytes. **So the `PRIM`, `FLG`, `NREG` and `REGS`
fields — the descriptor list that names every cell — are authored data sitting in the template, not values the
program derives.**

> **That is the whole of `UQ-213` for this program, reduced to a static read.** Find which of cells 0–26 `rax`
> selects at `00540905`, take those sixteen bytes out of `005409C0`'s stores, and the `REGS` nibbles name each
> quadword the iteration writes — at which point §5's strip stops being an inference.

### 5e. The tag decoded — a textured alpha-blended triangle strip, two vertices a sample (FABLE, same day)

**The cell is 0.** `00540905`'s index comes from `[rsp + 0x70]`, written once at `0053F7E1` from `r15d`, which
`0053F7D6` loads from the bank cell **`02064B0C`** — and an image-wide sweep of that cell finds **470 references
and not one write**. Nothing in the program writes it either. So the tag is built from **VU cell 0**, which the
template's `UNPACK V4-32 num=27 addr=0` fills from `005409C0`'s bytes at `+0x20`:

```
+0x20  0x00008000   +0x24  0x602E4000   +0x28  0x00412412   +0x2C  0x00008000
```

**Decoded as a PS2 GIF tag** (the decoder was run with the template's own `DIRECT` payload as a control, which it
reports as the empty terminator the [VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.4a independently found):

| field | value |
|---|---|
| `NLOOP` | 0 in the template — **the program stamps the real count**, §5d |
| `EOP` | 1 |
| `PRE` / `PRIM` | 1 / `0x05C` |
| `FLG` | 0 — **PACKED** |
| `NREG` | **6** |
| `REGS` | **ST, RGBAQ, XYZF2, ST, RGBAQ, XYZF2** |

`PRIM 0x05C` is **type 4 — TRIANGLE_STRIP** — with **IIP** (Gouraud), **TME** (textured) and **ABE** (alpha
blended) set, and FGE, AA1, FST and CTXT clear.

> **So section 1's sentence is no longer an inference.** The trail is drawn as a **textured, Gouraud-shaded,
> alpha-blended triangle strip**, and each loop iteration emits **two vertices, each as ST + RGBAQ + XYZF2** —
> the base and the tip of one sample, which is exactly the pair the C side records per sample (§2).

**Two independent checks make this more than a plausible decode.** `NREG = 6` matches the **six quadword stores
per iteration** counted in §5c from the disassembly alone, by a different route; and the register triple repeated
twice matches the two-points-per-sample structure the C side was already known to record. *Neither fact was used
to produce the decode.*

**And it names §5c's conditional write.** The fourth component of a `XYZF2` quadword carries **F and the ADC
bit**, and the two cells that receive the conditional `+0xC` dword are the two `XYZF2` cells — so
"write a flag into these two on every sample but one" is **setting ADC on a vertex pair**, the GS's per-vertex
skip. *Which vertex is skipped, and why that one, is not read here.*

**What remains for `UQ-213` on this program:** the meaning of the per-vertex values themselves — what the `ST`
pair spans and how `RGBAQ` combines the fade with the authored colour — and the other 46 microprograms, whose
tags are readable the same way: **the register list is in the template, not in the program.**

**Not read here:** `0053F490` itself; the rest of the template's `0x4A0` bytes (the `+0x348`–`+0x3F8` float block
`005409C0` fills, and the GIF packet after the DIRECT); what the DIRECT packet sets.

## 6. What a reimplementation must keep

- Trails are **per model, per bone, from data**: FCP section 4, at most four, sixteen in the world at once; a
  seventeenth request is dropped silently.
- A character-level command reaches the **weapon** through the record hierarchy, not through the weapon's own state.
- Off means **fade out over five steps, then free**; the owner may already have dropped the handle.
- Length comes from the **bone definition**, direction from the bone's x axis.
- Sampling is at **half the update rate** unless the frame-rate gate says otherwise; the histories are sixteen
  *samples*, not sixteen frames.
- System-stop set 3 freezes the histories (bit 0) without hiding them; bit 1 hides without freezing.
- The trail's alpha is `fade x owner opacity`, so a fading character takes its trail with it.

## Evidence

| body | interior anchors |
|---|---|
| `0051C3C0` update (2,128 B) | `0051C450`, `0051C45C`, `0051C471`, `0051C4A0`, `0051C4CF`, `0051C4DB`, `0051C516`, `0051C593`, `0051C59C`, `0051C5E9`, `0051C64D`, `0051C745`, `0051C74D`, `0051C769`, `0051C8CF`, `0051C92C`, `0051CA4E`, `0051CA67`, `0051CA88`, `0051CAB7`, `0051CAC0`, `0051CAF6`, `0051CB04`, `0051CB36`, `0051CB6C` |
| `0051BC70` draw (1,525 B) | `0051BC9E`, `0051BCB8`, `0051BD1E`, `0051BD6E`, `0051BD73`, `0051BD80`, `0051BDE6`, `0051BE40`, `0051BE4A`, `0051BE52`, `0051BE64`, `0051BE6A`, `0051BEAD`, `0051BF09`, `0051BF4A`, `0051BFE5`, `0051BFF9`, `0051C139`, `0051C147`, `0051C15A`, `0051C164`, `0051C208`, `0051C20D`, `0051C23D` |
| `0051CC30` create (385 B) | `0051CC45`, `0051CC64`, `0051CC79`, `0051CC8F`, `0051CC9C`, `0051CCB3`, `0051CCBF`, `0051CCF6`, `0051CD23`, `0051CD5E`, `0051CD63`, `0051CD77` |
| `0051C270` init (265 B) | `0051C2B5`, `0051C2E0`, `0051C2F3`, `0051C310`, `0051C31A`, `0051C341`, `0051C353`, `0051C35E`, `0051C365` |
| `003E6770` build / switch off (276 B) | `003E677C`, `003E679E`, `003E67AE`, `003E67E2`, `003E67E9`, `003E6823`, `003E685A` |
| `00425E70` fan-out (202 B) | `00425E89`, `00425EB7`, `00425EBC`, `00425EDF`, `00425EF3`, `00425EFA`, `00425F0E` |
| `003711D0` base and tip (232 B) | `003711EB`, `00371215`, `00371221`, `00371232`, `0037123C`, `00371248`, `00371276`, `00371288`, `00371293` |

Under 128 bytes, read whole: `00520160`, `0051CC10`, `0051BC10`, `0051CDC0`, `00422170`, `0046F460`, `00202E10`, `0042BDD0`.

Data: [`census.py`](../../_experiments/evidence/fcp-section4-trail-descriptors/census.py) and its
[output](../../_experiments/evidence/fcp-section4-trail-descriptors/census.out.txt) - 1,066 FCP blocks, 216 with a
section 4, 238 descriptors, every structural prediction holding.

## Cross-subsystem neighbours

**Effect system - SEQUENCE.** The draw opens by running the effect system's display layer 3 and only then draws the
trails; the two share the bracket and the order is fixed. The effect side is described on its own page and only
called here.

**Legacy PS2 graphics layer - SERVICE.** The trail image registration, the two image binds per draw, the buffer
submit and the microprogram registrar are the VIF1 / GS emulation's services, used as every legacy draw uses them; the
microprogram itself belongs to that layer's unread frontier.

**Core runtime - SERVICE.** The frame-rate gate and the time base `01DFE0BC` are the frame limiter's; read by value.

**Resource - SERVICE.** The sampler `00422170` resolves the record's model instance through the resource table's
entry-by-index getter (002ED570); a shared lookup, used by value.

**Movement, Gameplay - SHARED HELPER.** The cross product `00202E10` and the arccosine lookup `0046F460` are general
vector helpers with callers in the Movement and Gameplay layers. Naming them imports those edges; nothing about trails crosses into either layer.

**Actor - CLIENT.** The off-only route 0042F250 has a caller filed under the Actor layer (002E35B0) besides the two
named in section 2; none of the three was read, and the edge is recorded because naming the route imports it.

**System-stop registry - CONTROL.** Set 3 writes the entry flag byte `+5`; this page is the reader that the registry
page's 2026-09-17 answer said did not exist.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — MECHANICAL (3 edges).** The render pass list `00187950` calls `00182E80`, and the getter pair `00182E80` / `00182EB0` tail-jump to the four-byte field readers `002256A0` (returns the dword at `+0x14`) and `00225680` (the dword at `+0x10`) when the framework singleton exists, falling back to `0x438` and `0x780` otherwise. All four bodies are filed to Audio, but what they do is read two dwords of the framework singleton with 1080/1920 fallbacks, as section 5a says; the edges are that display-size read, and no sound path is involved.

**UI — CLIENT, MECHANICAL (1 edge).** The UI body `005512B0` (858 B) calls the 115-byte cross product `00202E10` that the trail update uses for its blade normal. It is another caller of a general vector helper; nothing about trails crosses into the UI.

## SWE2-EC7-82 update (2026-09-20) - `0051BC10` slot release measured

`0051BC10` (93 B) is the `cl`-indexed release the bone-trail callers
run: `cl * 0x3C0` into the `02A48F40` slot table, and when
`dword[slot]` matches `ecx` the slot clears to 0, the global count
`02A48F04` decrements, and the slot unlinks from the `+0x18`/`+0x20`
doubly-linked chain (head/tail at `02A48EF4`/`02A48F08` updated when
it is an end).
Interior anchor `0051BC13` (the `imul` slot index).

## SWE2-EC7-84 update (2026-09-20) - `00422170` flag dispatch measured

`00422170` (121 B) is the `[rax+0xD98]`-path fetch the trail callers
share with `00421FF0`: `[rcx+0x18]` != -1 gates `0020E600([rcx+0x10])`
then `002ED570(edx)` on `[rax+0xD98]`; a live record dispatches on
its byte `& 0x80` - `003712C0` when set, `003711D0` when clear -
with `edx`/`r8`/`r9` passed through, 0 on dead paths.
Interior anchor `004221C4` (the `003712C0` arm).

`003E7210` (414 B) is the record-table scan `00427DE0` calls: `003E55B0` resolves, `r8d == 0xFFFF` selects the `[rsi+0x400]` table whose `word[+0xA]` counts entries (`+r8d` bounds the walk), and `00504D30` runs per element - the trail's bounded table pass.

Interior anchor `003E7227` (function `003E7210`).

`004295E0` (382 B) is the flag decode `00427DE0` calls: `dword[rcx + 0x304]` bits 17/18/19 are extracted to stack flags, `word[rcx] == 0xFFFF` returns early, `movsx` sign-extends the index, `003E55B0` resolves twice and `0042EF90` runs twice - the render record's bit-field arm.

Interior anchor `00429647` (function `004295E0`).

`0042B270` (496 B) is the three-float bone-chain setter `00427DE0` calls for mode words `[rbx+0x3C4]` in 0..4: it resolves the `00422D50` object's `+0x310`/`+0x318`-counted section through `00409F50`, locates the `'@FMN'` block (`00409A30` on tag `0x4E4D4640` with byte `+1` patched to `0x6E` over a copy of `[rsi+0x10]`), and reads the mode-selected stride-6 element's `+0xC0`/`+0xC2`/`+0xC4` words -1-biased as the float triple; the `word[rbx]`-indexed `0x740`-stride record at `022C6F28` receives it via `00424010` when `00426220` passes, the `+8`-linked next record gets the same triple, and each `+8`/`+0xA` continuation walks `0042EF90` with the `0042E440` callback - the bone-trail default-position write.

Interior anchor `0042B387` (function `0042B270`).

`0042A390` (482 B) is `0042B270`'s sibling variant `00427DE0` runs on the alternate path: the same `00422D50`/`00409F50`/`@FMN`/`004096C0` machinery, the same two-link `022C6F28` chain and the same `0042EF90`/`0042E440` continuation walk, but the triple's first float comes from `[rbx+0x3C0]` verbatim and only the element's `+0xC2`/`+0xC4` words (-1-biased) supply the other two - the `+0xC0` slot is left to the caller's own field.

Interior anchor `0042A4A3` (function `0042A390`).

`00424010` (39 B) is the slot-tail setter the bone/effect build paths `0042A390`, `0042B270` and `0042B130` share: it stores the caller's three floats at `+0x2B0`/`+0x2B4`/`+0x2B8`, clears flag bit 1 of byte `+0x4B7` (`& 0xFD`) and zeroes the `+0x4B6` marker byte - no allocation, no dispatch.

Interior anchor `00424027` (function `00424010`).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** Sections 2 to 5a's structural claims became checks at their instructions and data. Script:
`Tools/analysis-kit/gfz-scripts/falsify_bone_trails.py`, output `falsify_bone_trails.out`, image `73461d08…`, 0 BROKEN,
exit 0. Carried:
- section 1's file census (`census.py`, 216 blocks);
- section 4's per-step arithmetic;
- the unread VU1 program's geometry, which the page itself labels an inference.

| # | Clause attacked | Result |
|---|---|---|
| B0 | sizes | **survives**: all fourteen |
| B1 | section 3 | **survives**: `0x3C00` allocated at `02CA8420`; the header `02CA8400`..`02CA8410` zeroed; the image at `01F2A220` referenced |
| B2 | section 2 | **survives**: the command stores `+0x3D0` and ORs bit 24 into `+0x294`; switch-off clears only byte `+4`; the builder tests the dword handle at `+0x438` against `0xFFFF`, caps the count at 4 (`cmova`), and steps `0x50` |
| B3 | section 4 | **survives**: the freeze test reads `02CA8402`; the time base `01DFE0BC`; the arccosine table at `00D12590` reads π, π/2 and 0 at its first, middle and last entries |
| B4 | sections 5, 5a | **survives**: the template `02CA8A90`; `0053F490`'s address taken once, at `0051C147`; the phase-2 tail-jump at `0041E4EF`; the VIF top bytes `0x03`, `0x02`, `0x01`, `0x6C`, `0x10` at the five cited stores |

No correction.
