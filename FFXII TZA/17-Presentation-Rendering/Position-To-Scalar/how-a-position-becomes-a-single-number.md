---
system: How a position becomes a single number — the presentation layer's busiest undocumented node
category: 17-Presentation-Rendering
status: AUDITED — static; all 76 call sites use the node's output as a modulate (section 13, 2026-09-19: 68 by colour multiply, 8 by alpha / 128); the live readings of sections 5-7 are title-screen only and were not re-made; lane 1 is Y, the up axis (cross-reference 2026-09-18), so mode 2 measures ground-plane distance
owner_layer: Presentation — from the ledger's own tag, not inferred from callers
evidence_tier: 1
level: L1
readiness: SIGNATURE RESOLVED
confidence: HIGH
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 84 addresses cited - 23 data, 26 entry, 35 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-position-to-scalar-pass-1 - the open checklist item is re-derived by an instruction-level diff and holds (the only third difference is the jmp the second arm gets by fall-through, and both arms load the same two globals); CORRECTED: 002F1FDC is mode 2 and 002F2018 is mode 1, not case 1 and case 0, and the zeroed component is LANE 1 of the stash before the transform and of the point after it, not w - so mode 2's distance drops that lane; the 75 callers, the five body sizes and the BSS claim all reproduce, the caller range starting at 00442550 rather than 004427D0. The game was NOT launched and no live reading was re-made
  crossref_clean: true
  reopened_count: 0
---

# How a position becomes a single number

## 1. What the player sees

Nothing on its own — and this page says so up front rather than inventing a story. What the *engine*
does with a number derived from a position is decide things a player feels without naming: which of
two things is drawn in front, how large something appears, whether a distant effect is worth drawing
at all. **Seventy-five places in the presentation layer ask this one function to turn a position into
a scalar.** What each of them then does with that scalar is **not established here**, and this page
does not pretend otherwise.

## 2. Why this function

A whole-binary ranking of functions **no document cites**, by distinct **non-EH** callers, and
excluding the eight-byte accessors that crowd the top:

| entry | body | distinct non-EH callers | ledger owner |
|---|---:|---:|---|
| `002F1F40` | **1,510 B** | **75** | `Presentation.SingleOwnerReferencedSupport` |

**It is the largest uncited high-connectivity node left in the binary.**
`check_already_answered.py` reported no coverage for the function, and — checking the *state* it
touches and not only the function, which is the discipline this session had to learn twice — only two
of its globals appear anywhere: `02EBF278` in the authored-data-table registry, and `02F97348` in
`UNEXPLAINED-GLOBALS.md`.

## 3. Three modes, chosen by an integer

The body opens on a small switch. Two arms transform a point; a third takes a different route
entirely.

```c
switch (mode) {
case 2:                                     /* 002F1FDC - mode 2, not 1 (§11) */
    stash   = *(vec4 *)02AED5F0;            /* a constant, §4 */
    point   = *(vec4 *)rdx;                 /* the caller's position */
    stash[1] = 0;                           /* this arm only, BEFORE the transform (§11) */
    SetWorkbenchMatrix(02AEEA20);           /* 0039AF70 */
    TransformPointByWorkbenchMatrix(&point, &point);   /* 00398F90, in place */
    point[1] = 0;                           /* this arm only, AFTER the transform (§11) */
    break;
case 1:                                     /* 002F2018 — identical, without the two zeroings */
    ...
case 0:                                     /* 002F2056 — and anything else skips the block */
    0039B550(02AEECB0);
    scalar = (float)0039ABF0(rsi);
    break;
}
/* the two transform arms then converge: */
scalar = 002F1D90(&point, &stash);          /* two vec4 in, one float out */
```

**The two transform arms differ in exactly two instructions** — `mov dword [rbp-0x15], 0` before and
`mov dword [rbp-5], 0` after — so one arm zeroes **lane 1** of the stashed constant and **lane 1 of
the transformed point**, and the other does not. That is the whole difference between **mode 1 and
mode 2**, and because both operands lose the same lane, **mode 2's distance is measured with that
component dropped** (§11).

## 4. Everything it reads ships as zero

Every global on these paths is **past `SizeOfRawData`** — BSS, zeroed by the loader:

`02AEEA20`, `02AED5F0`, `02AEECB0`, `02F97348`, `020926E8`.

**So the image cannot say what transform this installs.** Checking an "image default" against
`SizeOfRawData` rather than the section's virtual range is what makes that a fact instead of a
misread; reading the file at those addresses returns whatever follows on disk.

## 5. What the running game holds there

The retail build was launched (clean install, authority hash, base control passed) and these were
read across 30 samples, with a liveness control showing **4,114 bytes moving across 3 MB in ~3 s** —
so a stable value below is a real negative rather than a dead reader.

### The matrix it installs is the identity

```text
02AEEA20    [ 1  0 -0  0 ]
            [-0  1  0  0 ]
            [ 0 -0  1  0 ]
            [ 0  0  0  1 ]
```

**Stable across all 30 samples.** With the identity installed, `TransformPointByWorkbenchMatrix`
computes `out = in` — the arithmetic is a **no-op**.

> **Then why call it?** Because that function is not only arithmetic: it **deposits**. It copies the
> input to `022D9300` and the result to `022D8F90` and `022D9310`, as
> [the workbench's two primitives](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)
> §3 establishes. **On this path the call publishes the point into the shared workbench**, and the
> multiply is incidental.
>
> **This is bounded to what was observed.** `02AEEA20` is BSS and something writes the identity into
> it; whether it holds a different matrix in other game states was **not** tested, and the
> observation is from the title screen.

### The third arm's matrix is a perspective projection with a viewport folded in

```text
02AEECB0    [ -384.76      -0.0        0.0        -0.0 ]
            [    0.0     -624.44      -0.0         0.0 ]
            [ 2048.0     2048.0     -652.5         1.0 ]
            [    0.0        0.0   1677684.5        0.0 ]
```

**Row 2 column 3 is `1.0` and row 3 column 3 is `0.0`.** In the row-vector convention this workbench
uses, that is the signature of a **perspective** transform: the output `w` becomes a function of the
input `z`, which is what a perspective divide later consumes. An affine world or view matrix has
`[0,0,0,1]` in that column instead.

The `2048, 2048` in row 2 are the shape of a **viewport offset folded into the same matrix** — half
of 4096. **What surface is 4096 wide is not established**, and no claim is made about it.

### The singleton is live and the multiplier is zero

`02F97348` held `0x7A1553C0` — a non-null heap pointer, stable across all samples. The function
dereferences it **seven times**. `020926E8`, used as a `mulss` operand near the end, read **0.0**.

## 6. This sharpens `BI-9`, from a second direction

`BI-9` asks what the workbench matrix at `022D91B0` *is*. Two launches of the game now give two
**different** leftover values:

| launch | row 0 | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| first | `[0,0,0,0]` | `[0,0,1,0]` | `[0,0,0,-1]` | `[0,0,0,1]` |
| second | `[0,0,0,0]` | `[0,1,0,0]` | `[0,0,-1,0]` | `[0,0,0,1]` |

**Both are degenerate — row 0 is all zeros — and they are not the same.** A matrix the engine
maintained as *the* world, view or projection transform would not differ this way between two idle
title screens. Together with this function installing the **identity** into it, the evidence points
at a **slot each caller fills for its own use**, not a persistent engine transform. `BI-9` is not
answered — the in-world observation is still the one that would settle it — but the "maintained
transform" reading is now doubly disfavoured.

## 7. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `002F1F40` | the position-to-scalar node | 1,510 B | **75** non-EH callers; the mode switch |
| `002F1D90` | `Workbench_DistanceBetweenPoints` | 289 B | **read 2026-09-12 (§10)** — locks the workbench, `|b − a|` (squares summed, `sqrtf` `00861F14`), unlocks; the converging arms' distance |
| `0039AF70` | `SetWorkbenchMatrix` | 44 B | installs `02AEEA20` into `022D91B0` |
| `00398F90` | the point transform | 377 B | called for its **deposits** on this path |
| `0039B550`, `0039ABF0` | the third arm — `Workbench_InstallMatrix4x4` / `Workbench_TransformPointReturnW` | 195 / 489 B | **read 2026-09-12 (§10)** — install a 4×4 into `022D91B0`; transform the point and return lane 3 (`w`, the projective depth) |
| `02AEEA20` | the installed matrix | 64 B | BSS; **identity** at runtime |
| `02AED5F0` | the stashed constant | 16 B | BSS; `[0, 0, 0, 2.0]` at runtime |
| `02AEECB0` | a projection × viewport matrix | 64 B | BSS; §5 |
| `02F97348` | the singleton | 8 B | BSS; non-null, dereferenced 7× |
| `022C6F28` | the character render record array | — | read; documented in [character render object](../Character-Rendering/character-render-object.md) |
| `02EBF278` | authored-data table | — | in the [authored-data table registry](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) |

## 10. Extension 2026-09-12 — the scalar is the object's distance from the viewer, and the node is the distance-fade colour (PS-1)

`002F1F40(actor /*rcx*/, position /*rdx*/, out /*r8*/)` writes one **dword colour** — initialised to
`0x80808080` (`002F1F98`), the neutral modulate — and everything after the mode switch computes
**its byte 3, an alpha in `0 … 255`, from the scalar**. The scalar is a distance:

- it reads a **fade record** `rdi` = the singleton's block `[02F97348] + 0x2F0`, or, when that
  block's first byte is `0xFF`, the actor's presentation record `+0x50` (`[actor + 0x20] + 0x50`,
  `002F1F89`–`002F1F94`). Presentation kinds `≥ 0xA0` and `0x40` (`[+0x44]`) skip the fade
  (`002F1FA9`–`002F1FB3`).
- **byte `+1` of the record is the distance mode**: `0` = install the projection×viewport matrix
  `02AEECB0` and take the transformed point's `w` (`0039B550` → `0039ABF0`, the projective depth —
  `PS-2`'s matrix is this one); `1` / `2` = transform the point by the workbench matrix `02AEEA20`
  (`0039AF70` → `00398F90`; **mode 2** — not mode 1 — zeroes **lane 1**, of the stash before and of
  the transformed point after, §11) and take **`Workbench_DistanceBetweenPoints`**
  from the stashed vector `02AED5F0` (`002F1D90`: lock, difference, sum of squares, `sqrtf`, unlock).
- **byte `+0` is the fade kind**: `1` → alpha from the near/far word pair `+6` / `+0xA` with floor
  byte `+3` (`002F2291`–`002F22FA`); `2` → pair `+4` / `+8` with floor `+2` (`002F2220`); `4` → both
  pairs, keeping the smaller alpha (`002F2099`–`002F217C`); `3` → the global timed fade
  (`003ED0E0`, from the timer block `02EBB7E4`–`02EBB7EF`) scaled by the record's float `+0xC`, then
  the depth path again (`002F2184`–`002F221B`). Each arm is `clamp((far − d) / (far − near) × 255,
  floor, 256) × 0.5`, truncated — so the alpha range is `0 … 128` and a `near == far` pair yields
  `0x80`.
- then the singleton's flag word `+0x368` applies modifiers: bit 3 blends the colour through
  `0026EE00` with ~~the singleton's colour at `+0x398` (or `+0x334` for kind `0x40`)~~ *(reversed; corrected
  2026-09-19, section 12: `+0x398` for kind `0x40`, `+0x334` for every other kind - and the "singleton" is the
  effect container being drawn)*; bit 10 scales
  the alpha by the table `02EBF278[byte +0x377]`; bits 12 / 13 scale it by `+0x35C` when the actor's
  `+0x208` equals (or differs from) `+0x37C`; bits 4, 5 and 2 apply further per-record factors
  through `003A3FD0` / `0041E590` / `0042FB20`, `003E7DE0` and the global scale `020926E8`
  (`002F2424`–`002F2509`; the three callees are not read here).

**So the "scalar" is the drawn object's distance from the viewer (projective depth in mode 0,
Euclidean in modes 1–2), and the node is the per-object distance-fade colour**: the 75 call sites
(the draw-side family `0045E930`–`00537410` and `004427D0`) obtain the modulate colour whose alpha
fades an object out between the authored near and far distances. None of depth-ordering, size or
culling is what it feeds; it feeds a colour. What the fade record's kinds mean in authoring terms,
and the three unread modifier callees, are the residue.

## 8. What this document does not establish

- ~~**What the scalar is used for.** Depth, ordering, size and culling are the obvious guesses and
  **none is claimed**. 75 call sites were counted; **none was read**.~~ **Answered 2026-09-12 (§10,
  PS-1): the distance from the viewer, feeding a distance-fade alpha in a modulate colour.**
- ~~**What `002F1D90` computes.**~~ **The distance between two points, through the workbench (§10).**
- ~~**What the third arm does.**~~ **Installs the projection matrix and returns the projective depth (§10).**
- **That `02AEEA20` is always the identity.** Observed at the title screen, stable over 30 samples.
  It is BSS, so something writes it; **what it holds in play was not tested**.
- ~~**What the 4096-wide surface is**, if that is what the `2048, 2048` means.~~ **Answered 2026-09-14 (FABLE, PS-2): the
  PS2 GS primitive coordinate plane.** The engine builds a viewport matrix for it. `004679C0(m, w, h)` writes:
  - `m00 = w/2` and `m11 = −h/2` (`00467A0F`–`00467A26`);
  - row-3 translation **`2048.0, 2048.0`** (`00467A33`, `00467A3A`: `0x45000000`) and `m33 = 1`;
  - `m22` / `m32` map z between the constants `1024.0` and `16,777,215.0` (`0x44800000` / `0x4B7FFBFF` at `+0x4C` /
    `+0x50`, `004679D0`–`00467A62`), a 24-bit Z range.

  `00382910` builds the one at `02AED4A0` with `022D8EAC` × `022D8EB4` = **512 × 448**, the PS2 NTSC frame size
  ([the texture budget page](../Legacy-PS2-GS/texture-mip-local-memory-budget.md)). A second one at `02AED500` is
  2000 × 2000. The camera update `003820C0` builds the perspective projection into `02AEDDF0` (`003CBB30`: `m00 = cot / aspect`,
  `m11 = cot`, `m23 = −1`) and combines it with that viewport into `02AEDD30` through `00217150` (`00382656`–`00382667`).
  `0024C060` then places `02AEDD30` last in `02AEECB0`'s composition (`02AEE960` ← `02AEDD30`, `0024C0C9`–`0024C101`;
  `ComposeTransforms` applies its second argument first, so the order is view `02AEEA20` → `02AEE9E0` → `02AEE960`).
  The projection's `w = ∓z` row is what carries the viewport's `2048, 2048` into row 2, which is where the live read saw
  them. At start-up `0039CD50` also records the same centre (`2048, 2048`, `0039AED0`) and a screen distance of `512`
  (`0039AF20`), in write-only globals. So "4096" is the width of the GS's 12.4 fixed-point drawing plane, whose centre
  2048 the PS2 port kept: the projected points are GS primitive coordinates.
- **The meaning of `mode`.** Three arms are distinguished; what selects them is the caller's, and no
  caller was read.
- ~~**Why `020926E8` is zero**, or what it scales when it is not.~~ **Answered 2026-09-19 (section 12): it is the
  time stop's effect-dimming ramp, and at the title screen nothing had started one.**

## 9. Falsification checklist

- [x] **`02AEEA20` is the identity at runtime.** *Killer:* any non-identity reading. 30 samples, one
      distinct value, against a liveness control of 4,114 moving bytes.
- [x] **Every global on these paths is BSS.** *Killer:* a non-zero image read. `Image.read` returns
      nothing past `SizeOfRawData` for all five.
- [x] **`02AEECB0` has the perspective signature.** *Killer:* `[0,0,0,1]` in column 3. It holds
      `1.0` at row 2 and `0.0` at row 3, which is the opposite.
- [x] **The workbench matrix differs between launches.** *Killer:* two identical readings. Row 1 and
      row 2 differ between the two runs recorded in §6.
- [x] **The two transform arms differ only in two zeroing stores.** *Killer:* any third difference.
      **Re-derived by a tool 2026-09-13 (§11)**: an instruction-level diff of `002F1FDC`–`002F2017`
      against `002F2018`–`002F2043`, with both arms' rip-relative operands resolved, leaves
      exactly `mov dword [rbp-0x15], 0`, `mov dword [rbp-5], 0` and the `jmp 0x2F2044` the first
      arm needs because the second falls through. **Both arms load the same two globals.**

## 11. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. **The game was not launched**: §5's and §6's live readings are left exactly as
observed and none of them is re-tested here. `check_already_answered.py` run on the addresses this
pass touches.)*

### ✔ The open checklist item, re-derived by a tool — and it holds

§9's last line asks for exactly this and says it was not done. An instruction-level diff of
`002F1FDC`–`002F2017` against `002F2018`–`002F2043`, with every rip-relative operand resolved to its
target, gives **12 instructions against 9** and exactly three differences:

```
- mov dword ptr [rbp - 0x15], 0
- mov dword ptr [rbp - 5], 0
- jmp 0x2f2044
```

The two stores are the page's; the third is the **jump the first arm needs because the second falls
through** into the converging code at `002F2044`. **Both arms load the same two globals** — the
`movaps` resolves to `02AED5F0` and the `lea` to `02AEEA20` in each — which a byte-level reading
cannot see, because the displacements differ. **No third semantic difference. The item is ticked.**

### ✖ Corrected: the mode labels are off by one, and the zeroed component is not `w`

The switch reads:

```asm
002F1FC2  movzx ecx, byte ptr [rdi + 1]   ; the distance mode
002F1FC6  test  ecx, ecx / je 002F2056    ; 0 -> the projection arm
002F1FCE  sub   ecx, 1   / je 002F2018    ; 1 -> the arm WITHOUT the zeroing
002F1FD3  cmp   ecx, 1   / jne 002F2072   ; 2 -> falls into the arm WITH it; anything else skips
```

So **`002F1FDC` is mode 2 and `002F2018` is mode 1.** §3 labels them `case 1` and `case 0`, and §10
says *"mode 1 zeroes `w` first"*; it is **mode 2**, and there is no transform arm for a literal mode 0
— mode 0 is the projection arm.

And it is not `w`. `movdqa [rbp-0x19], xmm0` puts the stash at `rbp-0x19`, so **`rbp-0x15` is stash
lane 1**; `movaps [rbp-9], xmm0` puts the point at `rbp-9`, so **`rbp-5` is point lane 1**. The first
store lands **before** the transform, on the stash; the second lands **after** it, on the transformed
point.

> **Both operands of the distance lose the same lane, so mode 2's distance is computed with lane 1
> dropped** — a plane distance rather than a full one. That is a distinction with an authoring
> meaning for a distance fade: fade by how far away something is on the ground, not by how far above
> or below it is. **Which axis lane 1 is, is not established here** *(established by cross-reference 2026-09-18, FABLE: lane 1 is **Y, the up axis** — [the heading page](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) derives `Y = sin(pitch) × speed` and states that Y is up and lane 1 is Y — so mode 2's distance is the ground-plane distance, exactly the authoring meaning guessed below)* — that needs the vector's own
> layout, not this function.
>
> If `02AED5F0` really holds `[0, 0, 0, 2.0]` as §7 records from the live read, **the first store is
> redundant on that value** and only the second bites. Stated conditionally: the live reading is not
> re-made here.

### The static figures reproduce

| claim | measured |
|---|---|
| **75** distinct non-EH callers | **75 distinct functions over 76 `E8` sites**, 0 `E9` — one caller calls it twice |
| body **1,510 B** | **1,510** |
| `002F1D90` 289 B, `0039AF70` 44, `00398F90` 377, `0039B550` 195, `0039ABF0` 489 | **all five exact** |
| every global on these paths is BSS | **all past `SizeOfRawData`** — `.data` raw ends at rva `01E5E400`, virtual at `02E77530`, and `02AEEA20`, `02AED5F0`, `02AEECB0`, `02F97348`, `020926E8` all sit above the raw end. **`02EBF278` and `022C6F28` too**, which §9's item does not cover |

The callers run **`00442550` … `00537410`**. §10 describes them as *"the draw-side family
`0045E930`–`00537410` and `004427D0`"*; the lowest is **`00442550`**, and **57 of the 75** sit below
`0045E930`, in the `0044xxxx`–`0045xxxx` run. The family is the same; its stated bounds are not.

**Not claimed.** Nothing live: §5, §6 and `BI-9` are untouched, and **no reading of `02AEEA20`,
`02AEECB0`, `02F97348` or `020926E8` was re-made.** Which axis lane 1 is. What selects the mode
beyond the fade record's byte `+1`. The three unread modifier callees of §10. Nothing was executed.

## 12. Extension 2026-09-19 (FABLE) - whose colour it is: the node belongs to the effect container being drawn

Section 10 called `[02F97348]` *the singleton*. It is not one object. **It is the effect container currently being
processed**: the per-frame effect driver `0024D540` walks the list headed at `02091108` - slot 3 of the per-class head
array at `020910F0`, eight bytes a class, chained through `+0x348` - and stores each element there before working on it
(`0024D5A0`). `002F1F40` is called while an element of that container is being drawn, so the fade record at `+0x2F0`,
the flag word at `+0x368` and everything below are **fields of the container the element belongs to**. The first byte
of a container is its handle class (that is what `003A3FD0` switches on, below).

**Correction to section 10: the two colours were the wrong way round.** `002F2312` compares the element kind with
`0x40`, loads the address of `+0x398`, and *skips* the load of `+0x334` when the kind **is** `0x40`. So **kind `0x40`
blends with `+0x398` and every other kind with `+0x334`** - the sentence in section 10 said the reverse, and is struck
through there.

**What the two colours are.** They are the two alphas a character writes into its own effect container every frame -
[how a character fades, section 4d](../Character-Render-Records/how-a-character-fades-the-ten-channels.md): `003B30D0`
stores them, forces the three colour bytes of each to `0x80`, and raises this same bit 3 of `+0x368`. `+0x334` follows
the character's distance fade and camera-inside fade; `+0x398` does not. Put together with the top of this function:
**an element of kind `0x40` takes no distance fade of its own (section 10: kinds `0x40` and `>= 0xA0` skip it) and takes
the character alpha that ignores distance; every other kind fades with its own record and with the character.** What
kind `0x40` is in authoring terms was not established.

**The modifier callees section 10 left unread** (all read whole):

| bit of `+0x368` | what happens to the alpha | how |
|---:|---|---|
| 4 | **x the fade of the character the container belongs to**, or 0 if that character is not drawn | `003A3FD0(-1)` (149 B) finds the character: for a container whose first byte is 3 its `+8` is returned as it stands - the render-record index; for first bytes 5, 6 and 9 the container's entry in the slot list is asked, and `+8` is returned as it stands when the entry's byte `+0x11` is 1; in every other case an actor id - `+0x90 + 4n` when `n` is not -1 and that dword is non-zero, else `+8` - is resolved to an index by the id resolver; with bit 9 of `+0x378` up the id is the global `02096A20` instead. (The first bytes 3 and 5 / 6 / 9 match the handle classes of the two pools these containers live in.) Then `0041E590` (30 B) is true when the record's model instance exists with bit 0 of its `+8` up, and `0042FB20` (85 B) returns the record's fade evaluator with selector `0x0B`, divided by 4096 (1.0 for index -1 or a free record) |
| 5 | **forced to 0 while status-error display is denied** | `003E7DE0` (8 B) returns the byte `02B59D71`. Its one writer is `003E7C70` (71 B), which stores its argument there and switches two presentation states with it; that is called with 1 or 0 by the requester set `002EA8B0` (46 B) as its byte `0215FD45` becomes non-zero or zero - the *display-deny* set that [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) section 3.1 names from the `...dispdenystatus` verbs - and with 0 by the actor system's initialiser. That a container carrying bit 5 is therefore a status-ailment display is inference from the latch's name; who sets bit 5 was not traced |
| 2 | **x the global scale `020926E8`** | the scale is a ramp. `0024BFD0` (130 B), called by the effect driver once a frame in draw 0, works only while bit 8 or 9 of the flag word `020926E4` is up: it counts `020926E6` down, adds the step `020926F0` to `020926E8`, and at zero stores the target `020926EC`, clears both bits and, for the bit-9 ramp, runs two finishers. The two setters are the rate arms of [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md), which also put bit 2 on the containers concerned. **So this is how a time stop dims the effects it does not exempt, over a number of frames, and brings them back** - and it answers section 8's question: the value read as zero at the title screen is a ramp that nothing had started. A second body, 857 bytes in the `00332xxx` run, scales by the same global under the same bit |

| body | anchors |
|---|---|
| `003A3FD0` owner of the current container (149 B) | `003A3FE5`, `003A3FF1`, `003A3FF9`, `003A4005`, `003A400F`, `003A4031`, `003A4052` |
| `0024BFD0` global scale ramp (130 B) | `0024BFDE`, `0024BFF8`, `0024BFFF`, `0024C00F`, `0024C02B`, `0024C033`, `0024C046` |

Static. Nothing here was observed running; section 7's live readings are untouched.

*Who sets `[02F97348]` (added 2026-09-19):* the group draw of the VFX layers makes each container current just before
its elements are walked - `0024ED80`, on [the six VFX display layers](../Effect-File-Formats/the-six-vfx-display-layers.md),
section 1a.

## 13. Extension 2026-09-19 (FABLE) - what the callers do with the colour

The page's standing open item is *what each consumer does with the scalar*. Two pieces of evidence, both static.

**A census of every call site** ([fade_node_consumers.py](members/fade_node_consumers.py),
[fade-node-consumers.tsv](members/fade-node-consumers.tsv)): **76 sites in 75 functions**, equal to the figure of section
11. From each site the script decodes forward and records the first later call, giving up after 24 instructions or at
a return.

| first call after the node | sites |
|---|---:|
| the workbench colour multiply `0026EE00` | **67** |
| some other call first | 8 |
| no call within 24 instructions | 1 |

**One consumer read whole - `00442550` (173 B), the smallest.** It returns at once if the element's first byte is
zero. Otherwise it selects the element's texture frame, sets the element's position `w` to 1.0, calls the node with the
element, its position (`+0x230`) and a colour on the stack, **multiplies that colour with the element's own colour at
`+0x240`** through `0026EE00`, and hands the product - with the position - to a routine that projects the point through
`02AEECB0`, clips it, and emits a primitive in that colour.

**So for at least 67 of the 76 sites the node's output is a modulate colour multiplied into the drawn element's own
colour**, which is what section 10 inferred from the node alone.

**The other nine sites, read at the point of use the same day.** `004427D0`'s first call is followed by its second -
the two ends of one element - and both colours are then multiplied into the element's two colours, so it belongs with
the 67. **The remaining eight read only byte 3 of the output and scale a value of their own by `alpha / 128`**: a
colour vector through a vector-scale helper (`004640A0`, `004643D0`, `00464650`), a global intensity (`00461270`), a
field of the element (`00464BD0`), a float register used further down (`00465690`), the scalar handed to a handle
(`0047BD30`), and an integer (`00537410`). Five of them skip the scale when the byte is `0x80`, the neutral value.
**So at every one of the 76 sites the node's output is a modulate - 68 by colour multiply, 8 by alpha scale** - and
the page's one PARTIAL reason is settled. *Only the instructions between the node call and the use were read in those
nine bodies; none of them is anchored here.* What stays open is runtime-only: sections 5 to 7.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleUnit_UpdateCombatFrame`, owned by that layer, calls `003E7DE0` on this page. That caller is the per-unit combat frame step, behind `byte[02089340] & 0x20`: it tests the unit's stats record for bit 4 of the OR-ed `+0x3C`/`+0x64` pair - the **sixth** entry point on that pair - and on the retire path appends `dword[unit+8]` to a **64-entry ring** at `022BE984` whose index at `byte[022BE981]` wraps with `& 0x3F`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `00537410` on this page calls `PartyFocus_GetCurrentPackedActorHandle`, owned by that layer. What it reaches is a seven-byte getter returning the packed handle at `022C7FE0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 5 edges).** Audio bodies share the cited helpers; no audio
relationship to the position-to-scalar projection.

**Movement — SERVICE (SWE2-CONTRACT 2026-09-15, 2 edges).** The projection body `003820C0` calls Movement helpers `00233230` and `0026E500` — the position the page reduces comes through the movement layer's accessors. Small, real.

**CoreRuntimeScheduling — SERVICE (SWE2-CONTRACT 2026-09-15, 4 edges).** The projection body
`003820C0` calls scheduling helpers `00229D20` and `00229D60`; `003CBB30` shares `00229D60` and
`004679C0` shares `00229D20`. Small helper fan-in.
- **ActorEntity - SERVICE (4 edges).** `00465690` reaches bodies filed to ActorEntity: `00263C30`, `00263FF0`, ActorManager_GetRecordByOrdinal (`00358940`), ActorHandle_EncodeRegistryEntry (`003589B0`) - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (2 edges).** `0024C060`, `0024ED80` are called by bodies filed to UI: `0024B9B0` - shared machinery across the layer boundary, no shared ownership.

## SWE2-EC7-58 update (2026-09-19) - `003CBB30`

`003CBB30` (168 B) is the `02AEDDF0` projection-matrix build the camera pages name - `00229D60` single call plus `008F3148`/`01CEBDA0`. Interior anchor `003CBB56` (a `00229D60` call).

