---
system: Cut-in, motion blur and soft focus - the three script-driven screen effects
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every body named on this page disassembled and read whole - the three play bodies, the three clear bodies, the forced fade end,
    the three per-frame bodies and the two descriptor builders under them, the kind-4 descriptor handler, the two staging blocks' setters, the fade
    task's two callbacks and the sixteen verb handlers that are not bare thunks; accesses to the flag word and to the
    three state blocks found by rip-relative sweep; callers found by raw call and jump sweep; the twenty-four verbs
    joined to their handlers through scriptvm-verb-table.tsv and counted in the 1,114 decompiled us scripts
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-cutin-blur-softfocus-falsification-pass-1
  note: written by FABLE; static throughout - nothing on this page was observed in a running game; pending first review
---

# Cut-in, motion blur and soft focus

Twenty-four script verbs - `cutin*`, `moveblur*` and `setsoftfocusmode` - drive one small native module that draws
**over the finished scene**: it captures the frame into a render target and draws it back, changed. The module was
first met from the other side, as four of the nine routines that write
[the frame's draw-pass mask](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md); this page is
the module itself.

## 1. What the player sees, and what the scripts actually use

Counted in the shipped `us` scripts ([screen_effect_census.py](members/screen_effect_census.py),
[screen-effect-census.tsv](members/screen-effect-census.tsv); 13,905 calls, the parsed count equal to a plain substring
count):

- **Motion blur is, in practice, one idiom used 2,304 times in 264 scripts**: `seteventtimestop(1);
  moveblurcaptureonce(); movebluraplpha(1); moveblurfade(15); moveblurfadesync();` - then a message window - then
  `moveblurclearfade(15); moveblurfadesync();`. The scripts that carry it are the ones that show the *obtained*
  message (`additemmes(g_com_set_get_label, 1)` and its window variant). With the capture-once flag and a strength of
  exactly 1.0 the module takes the path of section 4 that **stops drawing the scene altogether and redraws one captured
  frame** - so the idiom is a fifteen-frame transition into a held picture behind the message, and back. What the held
  picture looks like (how blurred, how dark) was not observed; that is a question for a running game.
  One script (`nal_c0200`) uses the unfaded pair `moveblurplay()` / `moveblurclear()` for the same purpose, and one
  (`mic_b0601`) calls `moveblurclearfade(10)`.
- **Cut-in** is used five times in four scripts (`bhm_b0101`, `bhm_y0100`, `dgl_g0101`, `slm_z0100`), always as
  `cutinrotate(angle); cutinlinewidth(0); cutinlinefade(1); cutinplay();` and later `cutinclear()`. `cutinpos` is used
  once. **A line width of 0 and a faded line colour in every use**: whatever the lines are, the shipped cut-ins ask for
  them at zero width.
- **Soft focus is never turned on.** All 52 calls of `setsoftfocusmode`, in 49 scripts, pass `(0, 0, 0, 0)` - *off*. The
  turn-on body has exactly one caller, the verb's service, and that service's only other callers pass zeros (section
  5a), so in the shipped `us` scripts the effect has no way to start.
  Scripts switch off something that nothing switched on; the likeliest reading is a defensive reset inherited from
  a template, and that is inference.
- **Nine of the twenty-four verbs have no call at all**: `cutintype`, `cutinuv`, `cutincolor`, `cutinlinecolor`,
  `resetcutinparam`, `moveblurcluttype`, `moveblurnoisetype`, `moveblurscreentype`, `resetmoveblurparam`; two more,
  `moveblurplay` and `moveblurpresettype`, have one call each. Every cut-in the game shows is
  therefore type 2 with the default colours, and every motion blur but one is preset 1 with the first built-in mask -
  the defaults, which the engine itself restores at every area change (section 5a).

## 2. The shape all three share

| | cut-in | motion blur | soft focus |
|---|---|---|---|
| script staging block | `02B59D20` (0x24 B) | `02B58C38` (12 B) | none - arguments go straight in |
| live state block | `02092640` (0x24 B), target `02092638`, five handles `02092664` | `02092678` (12 B), targets `02092688` / `02092690` / `02092698`, eight handles `020926A0` | `020925F0` (0x30 B): parameters, target `02092620`, three handles `02092600` |
| bit of the flag word `020926E4` | 3 | 4 (playing), 5 (capture on the next frame) | 0 |
| play | `0024CF50` (158 B) | `0024EC00` (329 B) | `0024FAE0` (175 B) |
| clear | `0024CEB0` (160 B) | `0024EB20` (219 B) | `0024FA40` (155 B) |
| per-frame body | `0024CBE0` (715 B) -> `003AA6B0` (927 B) | `0024EA10` (270 B) -> `003AAA50` (2,736 B) | `003AB500` (698 B) |

**Staging, then play.** The parameter verbs only write the staging block. *Play* copies the block into the live state,
releases any render target the effect still holds, allocates new ones, zeroes the effect's handle array and raises the
effect's bit. *Clear* releases the targets, drops the bit, releases any handle still recorded and ends in a tail jump to
`0024C7C0` (172 B), which writes the ordinary pass mask back - draw 0 with bits 0-6 on, draw 1 with everything off.

**Render targets are released late.** A target being dropped is not freed on the spot: its pointer is appended to a
256-entry list at `02091950` (count `0209216A`) and freed by the list's owner; only when the list is full is it
released at once. Every play and clear body carries that same inline sequence.

**The size arguments are dead.** Each play body hands the target allocator two scale factors - 1/8 for soft focus, 1.0
for the cut-in, 1/2 or 1.0 and then 1/4 for motion blur, the pyramid a blur would want. The allocator's first
instruction after its prologue is a call, it never reads either argument register, and it always asks for
*device width x (device height x 512 / 448)*. **On this build every one of these targets is full size**; the
fractions are what is left of an older renderer. (Static, from the allocator's body; by role, not named here, because
it is a shared graphics helper.)

**Every frame, the effect queues its drawing again.** The per-frame bodies are called from the per-frame effect driver
`0024D540`, only while the frame-mode byte is 2 or 6, and with that driver's argument - **which draw of the frame this
is**, 0 or 1. They build *screen-effect descriptors* and queue them in the 32-entry pool that
[the screen-fade page](../Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md) describes. **The pass walker
releases a descriptor when its handler returns 0** (`00375633`), and every handler returns 1 when it is not its pass's
turn. Whether a drawn descriptor then returns 0 is a flag in its byte `+0x1C`: **kind 4 is one-shot when bit 3 is set,
kinds 2, 6 and 0x0D when bit 6 is set** (the last instructions of `00375B90`, `003745C0`, `00374280`, `00375280`), and
every descriptor of those kinds built on this page sets its bit. The returns of kinds 3, 5 and 7 were not read. That
is why the handle arrays are overwritten every frame without a release, and why an effect stops the frame after its
bit drops. Descriptor byte `+0` is the kind (the frame page's section 2.7 lists the kinds' handlers), the low nibble
of `+1` the pass it is drawn in, `+2` a class that a byte table can switch off.

**Kind 4 does not draw; it installs a texture.** `00375B90` (500 B), read whole, treats the descriptor's qword `+0x30`
as a PS2-style texture register - a block address in its low 14 bits (`0x2A00` in every descriptor here), a pixel
format, log2 width and height, and a palette address from bit 37 - uploads the image at `+0x20` (and the palette at
`+0x28`) to that address of the emulated video memory when flag bits 0 and 1 of `+0x1C` ask for it, and, when `+0x50`
holds a texture, hands the block address and *that texture* to the keeper of the block-address table at `0209E6C0`
(0x30-byte entries; the keeper itself was not read, so *installs* is the reading of this call, not of the table). So
the pattern on this page is always
the same three steps: **capture the scene into a target (kind 3), declare the target to be the texture at `0x2A00`
(kind 4), draw quads that sample `0x2A00` (kinds 2, 5, 6, 7, 0x0D).**

## 3. The cut-in

**Staging block `02B59D20`** - and, after `cutinplay`, the live copy at `02092640` with the same offsets:

| offset | verb | meaning | `resetcutinparam` |
|---|---|---|---|
| `+0` byte | `cutintype(n)` (`003DF9F0`, 64 B) | type: `n` = 0..4 stored as is, anything else 2. **Type 0 is "no cut-in"**: the per-frame body returns at once while this byte is 0 | 2 |
| `+1` bit 0 | `cutinlinefade(flag)` (`003DF990`) | clears the alpha of the second copy of the line colour | 0 |
| `+4`, `+8` | `cutinpos(x, y)` (`003DF9C0`) | position | 0, 0 |
| `+0xC` | `cutinrotate(angle)` (`003DF9E0`) | rotation, radians (the literal values in the scripts are 0.524, 0.698 and -1.65: 30, 40 and about -94.5 degrees) | 0 |
| `+0x10` | `cutinlinewidth(w)` (`003DF9B0`) | line width | 2.0 |
| `+0x14`, `+0x18` | `cutinuv(u, v)` (`003DFA30`) | origin of the picture's texture rectangle | 0, 0 |
| `+0x1C` | `cutincolor(a, b, c, d)` (`003DF950`) | four bytes in argument order - the picture's colour | `80 80 80 80` |
| `+0x20` | `cutinlinecolor(a, b, c, d)` (`003DF970`) | four bytes in argument order - the line colour | `00 00 00 80` |

`resetcutinparam` is `003DF900` (79 B) and `cutinplay` is `003DF8F0`, which passes the staging block to `0024CF50`.
**Play only allocates if the effect is not already up** (bit 3 tested first): a second `cutinplay` replaces the
parameters and keeps the target.

**Per frame (`0024CBE0`).** *In draw 0* it sets the pass mask - draw 0 bits 0-6 on and **draw 1 bits 0-7 on too**, with
the mask block's capture byte raised - and queues a kind-3 descriptor (pass 7, class 4) whose target is `02092638`: the
finished scene is captured. *In draw 1* it queues a kind-4 descriptor (pass 5, class 4) that installs the captured
picture as the texture, then hands `003AA6B0` a request built from the live block, and stores the three handles that come back.

**`003AA6B0`** queues kind-0x0D descriptors (pass 5, class 5). The first is the picture: the position, rotation and
colour of the block, with a texture rectangle from `(u, v)` to `(u + 1, v + 0.875)` - 448 / 512 again. **Type 1 stops
there** - a picture with no lines. Type 0 draws the second quad from the capture itself. **Types 2, 3 and 4 use one of
three line textures embedded in the executable** (`01EFD4A0`, `01EFD930`, `01EFDDC0`; each a small header giving the
offsets and log2 sizes of an indexed image and its 256-entry palette), created on first use into `02B3F470[i]` and
`02B3F488[i]` and installed by a second kind-4 descriptor. The second quad carries the line colour, the negated line width, and
- for every type but 0 - a span of `-73 .. +73` about its centre.

## 4. Motion blur

**Staging block `02B58C38`**, copied by play to `02092678`:

| offset | verb | meaning | `resetmoveblurparam` |
|---|---|---|---|
| `+0` byte | `moveblurpresettype(n)` (`003DE400`) | preset: `n` = 1 -> 2, 2 -> 3, anything else 1. Chooses one of three constant sets in `003AAA50` | 1 |
| `+1` byte | `moveblurcluttype(n)` (`003DE360`, 51 B) | mask: `n` = 1 -> 2, 2 -> 3, 3 -> 0, anything else 1. 1-3 are three 256-entry tables embedded at `01EFACA0`, `01EFB0A0`, `01EFB4A0` (created once into `02B3F420..30`); 0 means a caller-supplied table, which no path here supplies | 1 |
| `+2` byte | `moveblurnoisetype(n)` (`003DE3A0`, 51 B) | 0..3 stored as is, anything else 0. **Copied into the request and never read by `003AAA50`** | 0 |
| `+3` byte | `moveblurscreentype(n)` (`003DE430`) | `n` = 1 -> 2, anything else 1. Play returns *without raising the bit* for any other stored value; the builder uses the pair of thresholds `0x200` / `0x1C0` for 2 and `0x100` / `0xE0` for 1 | 1 |
| `+4` bit 0 | `moveblurcaptureonce()` (`003DE3E0`, an unlisted 23-byte body; the verb passes 1) | capture only on the first frame | 0 |
| `+8` float | `movebluraplpha(a)` (`003DE350`) - the verb's name is spelt that way in the table | strength | 0.5 |

**Play (`0024EC00`)** clears bit 4, stores the twelve bytes, releases both targets, allocates two, raises bit 5 and
zeroes the eight handles, then raises bit 4 again. *My first note on this module said the setter of bit 4 was not
traced; it is the play body's own last store (`0024ED38`).* The branch that would skip the reallocation when the effect
is already playing (`0024EC34`) tests bit 4 in a register **from which the same bit was cleared three instructions
earlier**, so it is never taken: every play reallocates. That the skip was the intent is inference.

**Clear (`0024EB20`) has its handle test inverted.** The cut-in and soft-focus clears release each recorded handle
that is *non-zero*. This one compares each of its eight handles with zero and **jumps past the release when the handle
is non-zero** (`0024EBD0`-`0024EBD6`), calling the release only with a zero. For the kinds whose return was read it does no
harm - they are released by the walker once drawn (section 2) - and for kinds 5 and 7 that was not checked. A
reimplementation should not copy the test as though it were a rule.

**Per frame (`0024EA10`)**, in draw 0 only and only with bit 4 up: builds the request - preset, mask, noise, screen
type, strength, the two targets - and decides the request's **capture flag**: 1 if bit 5 is up (which it then clears),
otherwise 1 unless the capture-once bit is set. It calls `003AAA50` and keeps the eight handles.

**`003AAA50`, read whole.** With the capture flag up it moves the menu out of the first draw (draw 0 bit 4 on, bit 3
off) and always turns bits 3 and 4 on for draw 1. **With the capture flag down it writes 1 to `01FD4A70`, and
`MainLoop_Draw` answers that dword by returning before it draws anything** (`0022B196`; it zeroes the dword and sets
`02064AE4`). *That is the held picture of section 1: while capture-once holds, the scene is not drawn at all.* Then:

- **Strength exactly 1.0, capture flag down, and a third target (`02092698`) present**: that target installed (kind 4)
  and one kind-2 quad, and nothing else - the cheap path, a stored frame shown as it is. The third target is made at
  the *end* of the first call that finds strength 1.0 and the flag down, by capturing into a newly allocated target
  (kind 3). Any other strength releases the third target.
- **Otherwise**: capture into the first target (kind 3, only with the flag up), a kind 4 installing it together with
  the chosen mask table as its palette, the same pair again for the second target, and then three descriptors of kinds 5, 7 and 6 whose
  constants depend on the preset - preset 1: `150`, `0.7`, `0.5`, then `strength x 0.2`, `350`; preset 2: `30`, `-20`,
  `200`, `0.8`, `0.75`, then the same closing pair; preset 3: the strength, then `strength x 0.2`, `400`, `0.5`. *What
  each constant means to the kind's handler was not read*; the handlers are the frame page's.

**Fading (`moveblurfade(frames)`, `moveblurclearfade(frames)`, `moveblurfadesync()`).** Both fade verbs scale the frame
count by the frame-rate word; **a result of 0 plays (`003DE2A0`, 98 B) or clears (`003DE240`, 91 B) at once**.
Otherwise, if no fade is running, they take a scheduled-task record, remember it at `02B58C48`, and give it a tick
callback `003DE160` (129 B), an end callback `003DE1F0` (22 B), the duration, and a direction at `+0x28` - 0 in, 1 out.
**A second fade asked for while one runs is dropped.** Each tick copies the staging block, replaces its strength by
`staged strength x t / duration` (or `x (1 - t / duration)` going out) and calls *play* with it - so during a fade the
targets are reallocated and bit 5 raised every tick, and the scene is captured afresh each frame; capture-once only
starts to hold when the fade has ended. The end callback zeroes `02B58C48` and, going out, tail-jumps to the clear.
`moveblurfadesync` is a waiting verb whose poll (`00345100`, 31 B) reports *busy* while `02B58C48` is non-zero
(`003DE150`). *My first note said `moveblurclearfade` reaches the clear body; it does, but directly only for a
zero-frame fade, and otherwise through this task.*

## 5. Soft focus

`setsoftfocusmode(on, mode, b, amount)` - handler `0034FA00` (97 B) pops the float, then three integers, and
tail-jumps to the service `0036E810` (104 B). With `on` = 0 it calls the clear. Otherwise it builds the parameter block
- byte `+0` = 2 if `mode` is 1, else 1; byte `+1` = `b`; float `+4` = `amount` - and calls play, which copies the block,
allocates the target, **drops bit 0 again if the allocation failed**, and forces byte `+2` to 4.

**Per frame (`003AB500`)**, draw 0 only. Byte `+2` picks a size word - 4 -> `0x40`, 3 -> `0x80`, 2 -> `0x100` - and
since play always stores 4 and nothing else writes the byte, it is always `0x40`. The mask: draw 0 everything but the
menu (bit 3 off), draw 1 only the menu and the queued-effect passes (bits 3 and 4). Three descriptors: kind 3 capturing
into the target (pass 7, class 5, carrying bytes `+0` and `+1` of the block), kind 4 installing it with the size word in
its register, and a kind-2 quad carrying `amount` and the neutral colour `80 80 80 80`. **So the world is blurred and the
menu stays sharp** - which is what the mask was for. No shipped `us` script ever gets here (section 1).

## 5a. Who else resets and ends them

A raw call and jump sweep over the resets, the clears and the fade's forced end:

- **Both staging resets run natively at every area change** - the area unload and the area initialiser each call
  `resetcutinparam`'s body and then `resetmoveblurparam`'s, back to back. That is why no script needs the two reset
  verbs, and why a script's parameter verbs do not leak into the next area.
- **`003DE210` (40 B) ends a running blur fade by force**: it sets the task's progress to its duration and its
  direction to *out*, forgets the task, and tail-jumps to the blur clear. Its three callers are the area unload, the
  cutscene skip's cleanup step (the one that also frees the seven fade layers -
  [the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md), `EX-8`) and one
  further body not read.
- **The effect system's teardown `0024E910` (256 B) ends in the blur clear and then the cut-in clear** (`0024EA02`,
  `0024EA0B`); the area unload calls it. *Corrected 2026-09-19: this bullet first said only the tail was read while
  anchoring the body; it was read whole, and this is all of it.* It calls one reset, releases every element of the list
  headed at `020910A8` (next pointer at `+8`) and zeroes the head, calls five more sub-pool resets, writes the mask
  `0x3FF` to `02092160` and runs the two walks the time stop's *back to 1.0* arm runs, clears bit 0 of `02EBEF68`, **bits
  10 and 11 of the flag word**, the low three bits of `02F8F29E` and bit 0 of `02EBDBBC`, calls one more reset with 0,
  and then - if **bit 6 of the flag word** is up - drops it and releases, through the same late-release list, **a fourth
  render target at `020926D0`** that none of the three effects of this page owns (`0024E9A9`-`0024E9F7`). What the
  resets it calls do, and whose target that is, were not read.
- **Soft focus is switched off by the area unload, twice.** The soft-focus clear has one caller, the verb's service
  `0036E810`, and the teardown does not reach it - but the area unload calls that service itself, twice,
  both times with `(0, 0, 0, 0)`. So the service has three callers and **only the script verb can
  pass a non-zero first argument**; with section 1, nothing shipped turns the effect on.

## 6. Behaviour a reimplementation must keep

- Parameter verbs change nothing on screen until the next *play*; for motion blur a fade tick is a play.
- `cutintype(0)` leaves the cut-in allocated and up but draws nothing; the same block with type 1 draws the picture
  without lines.
- A `moveblurscreentype` byte other than 1 or 2 cannot be staged by script; if one were, play would leave the effect
  off with its old targets released.
- A fade requested during a fade is ignored, and `moveblurfadesync` then waits for the *first* one.
- With capture-once and no fade running, the scene draw is skipped entirely each frame - anything that must keep
  animating behind the message does not.
- The effects run only in frame modes 2 and 6.
- An area change restores both staging blocks to their defaults and clears the blur and the cut-in; a skipped cutscene
  clears the blur.

## 7. What is not known

- What the kinds 2, 5, 6, 7 and 0x0D draw with the fields these bodies fill - of the handlers only kind 4's was read
  whole and the others' last instructions, so "blur", "lines" and "picture" are the verbs' words, not a reading of
  the drawing.
- What the three embedded mask tables and the three line textures contain.
- Why the driver `0024D540` is called with 0 from the menu frame and the capture-backed frame as well as by
  `MainLoop_Draw` with the draw index; its first half, which walks the effect-instance list, belongs to the effect
  pages and was not re-read for this one.
- Whether any script of another language build turns soft focus on; only `us` was counted.
- Everything about how these look. Nothing here was observed running.

## 8. Where each behaviour is in the bytes

| body | what | anchors |
|---|---|---|
| `0024D540` driver (551 B) | frame-mode gate; soft focus gate on bit 0 and draw 0; the three calls | `0024D6AA`, `0024D6B2`, `0024D6C9`, `0024D6D2`, `0024D6DE`, `0024D6EE`, `0024D6F6` |
| `0024CF50` cut-in play (158 B) | copy; bit 3 test; late release; allocate; raise; zero handles | `0024CF54`, `0024CF79`, `0024CFA9`, `0024CFBF`, `0024CFC4`, `0024CFD5` |
| `0024CEB0` cut-in clear (160 B) | type byte zeroed; bit 3 dropped; capture byte; handle loop; tail jump | `0024CEC6`, `0024CF06`, `0024CF16`, `0024CF2B`, `0024CF4B` |
| `0024CBE0` cut-in frame (715 B) | type test; draw split; blit; request; builder; handles; mask; capture | `0024CBFC`, `0024CC09`, `0024CC11`, `0024CC84`, `0024CCB9`, `0024CD4D`, `0024CD55`, `0024CD72`, `0024CE26`, `0024CE8B` |
| `003AA6B0` cut-in builder (927 B) | rectangle; first quad; type switch; textures made once; line blit; second quad | `003AA70C`, `003AA763`, `003AA777`, `003AA782`, `003AA79E`, `003AA7C0`, `003AA844`, `003AA875`, `003AA89C`, `003AA91D`, `003AA9B4`, `003AA9D1`, `003AAA17` |
| `0024EC00` blur play (329 B) | bit 4 cleared; the dead test; releases; size by screen type; two targets; bits 5 and 4 | `0024EC0D`, `0024EC18`, `0024EC34`, `0024ECBF`, `0024ECD0`, `0024ECEC`, `0024ED03`, `0024ED0F`, `0024ED38` |
| `0024EB20` blur clear (219 B) | releases; bit 4; the inverted handle test; tail jump | `0024EBB5`, `0024EBBC`, `0024EBD0`, `0024EBD2`, `0024EBD6`, `0024EBF6` |
| `0024EA10` blur frame (270 B) | bit 4 and draw 0; request; capture flag from bit 5 or capture-once; builder; handles | `0024EA26`, `0024EA33`, `0024EA54`, `0024EAAE`, `0024EABF`, `0024EAC4`, `0024EAEC`, `0024EAFB` |
| `003AAA50` blur builder (2,736 B) | capture flag and mask or the skip dword; strength 1.0 path; third target released; masks made once; mask select; screen type; captures and blits; kinds 5, 7, 6; presets; third target made | `003AAA88`, `003AAAA6`, `003AAADD`, `003AAAEC`, `003AAB6D`, `003AABEC`, `003AAC04`, `003AAC3F`, `003AAC72`, `003AACC6`, `003AAD40`, `003AADBC`, `003AAE51`, `003AAF21`, `003AAF98`, `003AB050`, `003AB1AE`, `003AB208`, `003AB263`, `003AB2B5`, `003AB327`, `003AB376`, `003AB3CC`, `003AB42C`, `003AB439`, `003AB462`, `003AB4CE` |
| `003DE160` fade tick (129 B) | direction; ratio; strength scaled; play | `003DE173`, `003DE19E`, `003DE1A2`, `003DE1C0`, `003DE1CA` |
| `0024FAE0` soft-focus play (175 B) | bit 0; copy; late release; allocate; failure drops the bit; byte `+2` = 4 | `0024FAE4`, `0024FB13`, `0024FB50`, `0024FB5F`, `0024FB66`, `0024FB83` |
| `0024FA40` soft-focus clear (155 B) | bit 0; late release; three handles; tail jump | `0024FA5B`, `0024FA96`, `0024FAB6`, `0024FAD6` |
| `003AB500` soft-focus frame (698 B) | size word; mask; capture; blit; quad | `003AB525`, `003AB52E`, `003AB555`, `003AB5E6`, `003AB67C`, `003AB683`, `003AB6DC`, `003AB72C`, `003AB777`, `003AB791` |
| `0024C7C0` ordinary mask (172 B) | draw 0 on; draw 1 off | `0024C7CB`, `0024C813`, `0024C81D`, `0024C867` |
| `00375B90` kind-4 handler (500 B) | pass gate; upload by flag bit 0; fixed or log2 size; texture registered; palette upload by bit 1; return from bit 3 | `00375BAF`, `00375BD2`, `00375BF7`, `00375C2D`, `00375C44`, `00375C84`, `00375CA3`, `00375CC6`, `00375D3A`, `00375D65`, `00375D73` |

## 9. Related

- [What happens between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) -
  the two draws of a frame, the pass mask these effects write, and the queued-effect kinds.
- [The screen-fade layers](../Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md) - the descriptor pool
  these effects queue into, and the other scripted full-screen effect.

## Cross-subsystem neighbours

**Script VM native bridge - SERVICE.** The sixteen verb handlers named here (`0034FA00`, `00345100` and the
`cutin*` / `moveblur*` handlers behind the staging setters) pop their arguments and tail-jump into this module; the
bridge owns the popping, this page owns what the values mean. The eight verbs whose table entry is a bare thunk are
cited through the verb table and not by address.

**Core runtime scheduling and the frame - SERVICE.** `MainLoop_Draw` (`0022B0B0`) and the two other frame bodies call
the driver `0024D540`; `MainLoop_Draw` also owns the early return that the builder's skip dword `01FD4A70` asks for. The
frame page owns the draw loop and the pass mask; this page owns only what these three effects ask of them.

**Actor / entity - SERVICE.** The area unload, a body filed under ActorEntity and described on
[the world tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) - it is not named
here, because naming it would import every one of its callees - is this module's native reset: it calls
the cut-in staging reset `003DF900` and the blur's beside it, the forced fade end `003DE210`, the effect teardown
`0024E910` and the soft-focus service `0036E810` (section 5a). The unload owns *when* an area's presentation state is
dropped; this page owns what each of those calls does to the three effects. Only the five call sites of the unload were
read, not the unload.

**Audio - INCIDENTAL.** The driver `0024D540` calls the Audio-filed `003B3D20` in its first half, before the frame-mode
gate. That half was not read for this page and nothing here depends on it.

**Combat AI - MECHANICAL.** The `003B3D20` section cites its callee `003E7DE0`, which the CombatAI-filed `00308610`
also calls. The page consults `003E7DE0` only as `003B3D20`'s callee; the CombatAI caller was not read and nothing
here depends on it.

**Shared graphics helpers - by role.** The render-target allocator, its texture getter and late-release list, the
descriptor queue and its release, the pass-mask setters, the scheduled-task allocator, the frame-count scaler and the
VM pop routines are described by role and not named, because naming a shared leaf imports every one of its callers.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Movement — SERVICE, OUT-OF-SCOPE (1 edge).** `MainLoop_Draw` (`0022B0B0`), cited here as a caller of the paired singleton setter and getter, also calls `00357780`, a 7-byte getter of the dword at `022C7F80`, as one of the conditions for a later draw call. That is the frame's own movement-side check and none of the three screen effects reads it.

**Resource — CLIENT, MECHANICAL (1 edge).** The Resource-filed 597-byte body `001A7A50` calls `00193D50` twice, the lazy singleton getter that allocates and constructs the 0x4A8-byte object at `01F7F5F0` on first use and returns the cached pointer afterwards. It is another client of the same render singleton the setter `001830C0` commits into; the edge is a shared getter, not a screen-effect path.

## SWE2-EC7-46 update (2026-09-19) - `003B3D20`

`003B3D20` (225 B) is the Audio-filed body the `0024D540` driver calls - `002DF0F0`/`003E7DE0`. Interior anchor `003B3D31` (a `002DF0F0` call).

## SWE2-EC7-77 update (2026-09-20) - `00182B20` flagged getter measured

`00182B20` (18 B) is the flag-gated pointer read: `rcx` non-NULL and
`byte[rcx+8] == 0` returns `[rcx]`; any other input returns 0.
Interior anchor `00182B25` (the `+8` byte test).

## SWE2-EC7-89 update (2026-09-20) - `003B3B50` 32-slot flag sweep measured

`003B3B50` (70 B) is the sweep the screen-effect callers run: 32
0x38-stride slots from `02EBD480` are checked for a tagged key
(`dword & 0xFFFFFC0` nonzero) and a live `+0x10` pointer, and
each hit clears bit 1 of `word[record + 0x368]` - a blanket
flag reset across the table.
Interior anchor `003B3B63` (the tag test).

## SWE2-EC7-90 update (2026-09-20) - `003B1130` 36-slot flag sweep measured

`003B1130` (68 B) is the `02EBEC00` sibling of the `003B3B50`
sweep: ~~36 0x18-stride slots are checked for a keyed `dword` and
a live `+8` record~~ **up to 36 0x18-stride slots are walked, and the walk returns at the first slot whose key
`dword` is zero (`003B1144` → `003B1173`, the `ret`) - unlike `003B3B50`, which skips an empty tag and goes on; a
keyed slot with a live `+8` record is a hit (corrected 2026-09-29, OPUS falsification pass 1, `CON-183`)**, and each hit clears bit 1 of
`word[record + 0x368]` - the same blanket flag reset over the
second table.
Interior anchor `003B1140` (the key test).

## SWE2-EC7-112 update (2026-09-20) - `001830C0` measured

`001830C0` (52 B) is the
paired singleton setter
`0022B0B0` and `0029CF90`
run: `00193D50()` fetches the
object, and only when it is
live do `dword[+0x490]` and
`dword[+0x494]` take `ecx`
and `edx` - a two-field
commit guarded on the
singleton.
Interior anchor `001830DD`
(the `+0x490` store).

`00182490` (77 B) is the
paired out-param getter
`0022B0B0` and `0029CF90`
run beside it: `00189120()`
fetches the object, and when
live ~~a non-null `rdx` gets
`00186AA0(obj)` and a
non-null `rcx` gets
`00186A90(obj)`~~ **a non-null `rcx`
gets `00186AA0(obj)` and a
non-null `rdx` gets
`00186A90(obj)` (`0018249A`..`001824D0`; corrected 2026-09-29, OPUS falsification pass 1, `CON-183`) - `00186AA0` is the
width the render-target allocator reads first** - two
independent reads off the
same singleton.
Interior anchor `001824CB`
(the `00186A90` call).
Both callers' own fan-out is
mechanical and recorded
here: `0022B0B0` reaches the
Movement domain and
`00193D50` takes a Resource
caller - shared-service
edges, not screen-effect
subjects.

`0026FF50` (54 B) is the deferred teardown latch: while `byte[02F8F238]` stands, the body runs `0024C550(2)`, clears `dword[02F8F238]` and `qword[02F8F228]`, and sets `byte[02F8F29D] = 1` - the one-shot screen-effect cleanup gate the cut-in and map-ctrl callers share.

Interior anchor `0026FF62` (function `0026FF50`).

`003B2F90` (225 B) is the bucket-cache sweep `0024E910` runs over the `02EBDB98` list: each node's key low 6 bits index a `0x38`-stride `02EBD480` bucket, and a bucket whose `+0` still matches its node gets `0024EE60` on `[+0x10]`, unlinks from the active list, pushes onto the `02EBDBA0` free head with `+0x28`/`+0x20` relinked, and clears its key to `key & 0xF000003F` plus `+0x10 = 0` - then `0024C460(3)` reaps

Interior anchor `003B2FE0` (function `003B2F90`).

## Falsification pass 1 — 2026-09-29 (OPUS): the three effects survive whole; two appended notes do not

**Attack.** Sections 1 to 5a and the appended notes were turned into checks at their instructions. Every caller set the
page states was re-counted with a raw E8/E9 sweep. The five verb setters' branch ladders were walked for n = 0..6.
Script: `Tools/analysis-kit/gfz-scripts/falsify_cutin_blur_softfocus.py`, output
`falsify_cutin_blur_softfocus.out`, image `73461d08…`, 0 BROKEN, exit 0. The us-script census is carried, not re-run.
Section 7's open items stay open.

| # | Clause attacked | Result |
|---|---|---|
| Z10 | SWE2-EC7-90: `003B1130` "36 0x18-stride slots are checked" | **refuted** (`CON-183`). A zero key jumps to the `ret`, so the walk ends at the first empty slot |
| Z11 | SWE2-EC7-112: `00182490` "a non-null `rdx` gets `00186AA0(obj)` and a non-null `rcx` gets `00186A90(obj)`" | **refuted** (`CON-183`). The reverse is true: `rcx` gets `00186AA0` (the width) and `rdx` gets `00186A90` |
| Z0 | sizes | **survives**: all 35; `003DE3E0` is unlisted, as the page says |
| Z1 | the caller sets | **survives**: the driver's three callers, its three per-frame calls, the soft-focus service's three callers, the forced end's three, and the reset's area-unload, initialiser and verb callers |
| Z2 | the frame-mode gate | **survives**: `(mode − 2) & ~4 == 0` admits modes 2 and 6 only |
| Z3 | late release; dead size arguments | **survives**: a 256-entry list. The allocator's first act is a call, `xmm0` is overwritten before any read and `xmm1` is never read; height × 512 / 448 |
| Z4 | the one-shot returns | **survives**: kind 4 returns `!bit 3`, the other three handlers `!bit 6`; the walker releases on 0 |
| Z5 | the verb setters | **survives**: all five mappings, n = 0..6 |
| Z6 | blur play's dead test, blur clear's inverted test, the skip dword | **survives**: all three exactly as described |
| Z7 | the soft-focus service and play | **survives** |
| Z8 | the teardown tail, the fade poll, the cut-in constants | **survives** |
| Z9 | the other notes | **survives**: `003B3B50`, `00182B20`, `001830C0`, `0026FF50`, `003B2F90` |

Corrected in place: the two notes. The consumer record is
`_index/candidates/cutin-blur-softfocus-falsification-pass-1-0929/`.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-cut-in-motion-blur-and-soft-focus-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003DE240` | 91 B | takes `n = 00265860()`; when `n` is 0 tail-jumps `0024EB20`; otherwise, when qword `02B58C48` is null, stores `002F16B0()` there and writes into that record qword `+0x10` = `003DE160`, qword `+8` = `003DE1F0`, dword `+4` = `n`, dword `+0x28` = 1 and byte `+0x20` = 0, and when it is non-null returns untouched | `003DE24F`, `003DE256`, `003DE25B`, `003DE271`, `003DE28A` |
| `003DE2A0` | 98 B | takes `n = 00265860()`; when `n` is 0 tail-jumps `0024EC00` with `rcx` = `02B58C38`; otherwise, when qword `02B58C48` is null, stores `002F16B0()` there and writes into that record qword `+0x10` = `003DE160`, qword `+8` = `003DE1F0`, dword `+4` = `n`, dword `+0x28` = 0 and byte `+0x20` = 0, and when it is non-null returns untouched | `003DE2B1`, `003DE2BD`, `003DE2C2`, `003DE2D8`, `003DE2F1` |
| `003DE360` | 51 B | stores into byte `02B58C39` a value chosen by `ecx`: 1 maps to 2, 2 to 3, 3 to 0, and 0 or any other value to 1 | `003DE36E`, `003DE373`, `003DE37B`, `003DE383`, `003DE38B` |
| `003DE3A0` | 51 B | stores into byte `02B58C3A` a value chosen by `ecx`: 0 to 3 are stored as they are and any other value stores 0 | `003DE3AE`, `003DE3B3`, `003DE3BB`, `003DE3C3`, `003DE3CB` |
| `003DE400` | 38 B | stores into byte `02B58C38` a value chosen by `ecx`: 1 maps to 2, 2 to 3, and 0 or any other value to 1 | `003DE409`, `003DE40E`, `003DE416`, `003DE41E` |
| `003DE430` | 24 B | when `ecx` is non-zero stores 2 in byte `02B58C3B` and keeps it when `ecx` is 1; any other value (including 0) ends with 1 stored there | `003DE432`, `003DE434`, `003DE43E`, `003DE440` |
| `003DF950` | 27 B | stores `cl`, `dl`, `r8b` and `r9b` in the bytes `02B59D3C`, `02B59D3D`, `02B59D3E` and `02B59D3F` | `003DF956`, `003DF95C`, `003DF963` |
| `003DF970` | 27 B | stores `cl`, `dl`, `r8b` and `r9b` in the bytes `02B59D40`, `02B59D41`, `02B59D42` and `02B59D43` | `003DF976`, `003DF97C`, `003DF983` |
| `003DF990` | 23 B | replaces bit 0 of byte `02B59D21` with 1 when `ecx` is non-zero and 0 when it is 0, keeping the other bits (old byte AND `0xFE`, OR the `setne` result) | `003DF997`, `003DF999`, `003DF99C`, `003DF99E`, `003DF9A0` |
| `003DF9C0` | 17 B | stores the float `xmm0` in dword `02B59D24` and the float `xmm1` in dword `02B59D28` | `003DF9C8` |
| `003DF9F0` | 64 B | stores into byte `02B59D20` a value chosen by `ecx`: 0 to 4 are stored as they are and any other value stores 2 | `003DFA03`, `003DFA08`, `003DFA18`, `003DFA20`, `003DFA28` |
| `003DFA30` | 17 B | stores the float `xmm0` in dword `02B59D34` and the float `xmm1` in dword `02B59D38` | `003DFA38` |
