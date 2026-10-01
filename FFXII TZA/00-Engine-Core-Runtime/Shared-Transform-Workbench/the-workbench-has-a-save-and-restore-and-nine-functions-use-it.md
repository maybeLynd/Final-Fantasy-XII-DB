---
system: The workbench has a save and restore — and nine functions use it
category: 00-Engine-Core-Runtime
owner_layer: none — the pair carries no ledger owner, and a caller is not evidence of one
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
status: AUDITED — the nine users placed (UQ-41), the lanes' signed ceiling (UQ-42) and the computation's meaning (UQ-43) all answered 2026-09-17
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 62 addresses cited - 12 data, 13 entry, 36 interior, 1 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-workbench-save-restore-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The workbench has a save and restore — and nine functions use it

## 1. What the player sees

Everything FFXII draws or hears passes through one shared scratch area — a workbench where
positions, orientations and colours get combined before anything reaches the screen or the
speakers. [The workbench document](the-shared-transform-workbench.md) establishes that nobody owns
it: code writes its numbers in, calls a shared routine, reads the answer out, and leaves whatever it
left.

**That is true of almost every user of it, and it is not true of nine of them.** Nine functions
borrow a slot, put the original contents back before returning, and use an engine-provided pair of
helpers to do it. For anyone hooking this area, that is the difference between a scribble that
persists and one that vanishes the moment the function returns.

## 2. The correction

> [The workbench document](the-shared-transform-workbench.md) §6 tells a modder:
> *"Treat the workbench as caller-saved. Anything you write there is visible to the next user and
> **nothing restores it**. Write your operands, take your result, and assume the area is clobbered."*
>
> **The first two sentences of that advice are right and the third clause is wrong.** There is an
> explicit save/restore pair in the image, nine functions call it, and it restores exactly the rows
> they name.

The advice's *conclusion* survives — you still cannot assume the area is intact, because 240 of the
249 functions that write it restore nothing. What changes is that **"nothing restores it" is not a
property of the area**; it is a property of most of its users.

## 3. The pair, read in full

### Save — `0036D930`, 89 bytes

```asm
0036D930  mov  [rsp+0x08], ecx          ; count
0036D934  mov  [rsp+0x10], rdx          ; p1  -- the register home area, so this is VARIADIC
0036D93E  mov  [rsp+0x18], r8           ; p2
0036D943  mov  [rsp+0x20], r9           ; p3
0036D948  test ecx, ecx / je            ; count 0 -> just record it
0036D953  lea  r9, [02EC0800]           ; the saved VALUES
0036D95A  lea  r8, [02EC0A00]           ; the saved POINTERS
0036D961  mov  rax, [rdx+8]             ;   the i-th pointer, walked off the home area
0036D969  mov  [r8], rax                ;   remember where it came from
0036D974  movups xmm0, [rax]            ;   the 16 bytes there
0036D977  movups [r9-0x10], xmm0        ;   remember what was in it
0036D97C  sub  r10, 1 / jne             ; loop
0036D982  mov  [022D8F08], ecx          ; the DEPTH
```

### Restore — `0036D8E0`, 66 bytes

```asm
0036D8E6  cmp  [022D8F08], edx / jbe    ; for i < depth
0036D8FE  mov  rax, [imagebase + rax*8 + 0x2DA0A00]      ; -> 02EC0A00[i], the pointer
0036D906  movups xmm0, [imagebase + rcx*8 + 0x2DA0800]   ; -> 02EC0800[i], the value
0036D90F  movups [rax], xmm0            ;   put it back
0036D91A  mov  [022D8F08], r8d          ; depth = 0
```

*Order inside Save (2026-09-28, FABLE, Claude Opus 5.5; re-read from the bytes, on ASTRA's
[save-pointer-record-alias](../../_experiments/evidence/save-pointer-record-alias-byte-preserved/raw/README.md)).*
For each item, `Save` writes the pointer record (`0036D969`) **before** it loads the target's 16 bytes (`0036D974`), and
then it stores them (`0036D977`). So the snapshot is taken at that load, after the earlier writes of the same `Save`,
and it is not necessarily the target's state on entry.
- A target whose 16 bytes cover its own pointer slot is snapshotted with its first eight bytes already replaced by its
  own address. An immediate `Restore` writes that altered snapshot back. ASTRA's source calculation uses count 1,
  target `02EC0A00`.
- A disjoint target keeps its entry bytes, and so does the value-slot self-copy (`02EC0800`).
- The contract states the resulting rule as its Precondition 3
  ([CONTRACT-transform-workbench-save-restore.md](../CONTRACT-transform-workbench-save-restore.md) §4).
- Whether any caller passes such a target is not established.

**The depth counter lives at `022D8F08` — inside the workbench itself**, eight bytes into the region
[the workbench document](the-shared-transform-workbench.md) §2.1 bounds at `022D8F00`–`022D9500`.
The saved pointers and values live outside it, at `02EC0A00` and `02EC0800`.

> **It is a stack with a depth of one.** `Save` **assigns** the count rather than adding to it and
> `Restore` zeroes it, so a nested save loses the outer frame. Nothing observed nests — but nothing
> prevents it either, and a hook that calls `Save` around a function that already does would drop
> the outer save silently.

## 4. Nine functions, and four of them are invisible to a call scan

| instrument | `Save` `0036D930` | `Restore` `0036D8E0` | control |
|---|---:|---:|---|
| `E8 call` | **9** | **5** | `001DE4F0` → 1 |
| `E9 jmp` | **0** | **4** | `001D1660` → 1 |

**Four of the nine restores are tail-jumps** — `0026F413`, `003AFFAB`, `00431F0A`, `0046242E` — the
natural shape for a helper called last. **A call-only query finds five of nine and reports a leak
that is not there.**

The nine callers are the same nine functions on both sides, with **no function saving without
restoring and none restoring without saving**:

| function | bytes | saves | restores |
|---|---:|---|---|
| `0044BAC0` | 3,461 | `0044C43E` | `0044C4C3` |
| `0026EE00` | 1,560 | `0026EE2C` | `0026F413` *(tail)* |
| `0042FDB0` | 1,470 | `004300F9` | `0043035E` |
| `003AFDD0` | 480 | `003AFDEC` | `003AFFAB` *(tail)* |
| `00431D30` | 479 | `00431D4C` | `00431F0A` *(tail)* |
| `00462260` | 467 | `0046227C` | `0046242E` *(tail)* |
| `003D8E50` | 418 | `003D8E78` | `003D8FE2` |
| `002F1D90` | 289 | `002F1DAC` | `002F1E9B` |
| `002F1CE0` | 174 | `002F1CF5` | `002F1D7D` |

**Nine of the 249 functions that write the workbench — 3.6 %.** The other 240 leave what they wrote.

## 5. Only two rows are ever protected

Decoding the argument setup at each of the nine `Save` sites:

| row saved | callers |
|---|---:|
| `022D8F30` | **5** |
| `022D8F90` | **3** |
| two rows, both passed in registers | 1 — `0042FDB0`, `count = 2` |

Eight of the nine save **one** row and one saves two. **`022D8F30` and `022D8F90` are the only two
addresses that anything in this image bothers to protect**, which makes them the workbench's
contended slots rather than merely two of its 46 sixteen-byte rows.

## 6. A worked user: `0026EE00`, 1,560 bytes, 104 callers

Chosen because it was the largest function in the database that no document cited (`EL-1`), and it
turned out to be the clearest example of the workbench's memory calling convention.

```c
void FUN_0026EE00(int32_t *out /*rcx*/, const int32_t *a /*rdx*/, const int32_t *b /*r8*/);
```

Of every global it touches, **exactly one is read and never written: `022D8F10`, read 16 bytes
wide, once.** Everything else in the workbench that it reads, it wrote first.

> **That is the memory calling convention caught in the act.** `022D8F10` is an *operand the caller
> must have left there*. A reader tracing arguments through registers sees three pointers; the
> fourth argument arrives through memory, and nothing in the signature says so.

It saves `022D8F30`, computes through `022D8F90`, `022D8FA0`, `022D8FC0` and a second scratch block
at `022D9110`–`022D912C`, reads its answer back out of `022D8F30`, stores it through `out`, and
tail-jumps to `Restore`.

### What it computes, measured by running it

The body is 1,560 bytes of unrolled byte-scatter and packed 16-bit multiplies — a shape that is
readable and a meaning that is not. So the shipped bytes were **executed** under emulation with
controlled inputs, both callees mapped and running as shipped:

```
out_byte[i]  =  min(255,  2 x ((row[i] x arg_byte[i]) mod 256))        for i = 0, 2, 3
```

where `row` is the 16 bytes at `022D8F10` and `arg_byte[i]` is byte `i` of `*a` (and of `*b`).
**Zero disagreements over 168 combinations** — 3 byte positions × 8 row values × 7 argument values.

### SUPERSEDED 2026-09-08 — that is the `b = 0` case of a three-operand rule

`EN-1` asked how the two integer arguments combine. **They multiply**, and the rule is exact:

```
out_byte[i] = min(255,  ( 2 x ((row[i] x (a_byte[i] + b_byte[i])) mod 256)
                          + ((a_byte[i] x b_byte[i]) >> 7) )  mod 512 )

                                                            for i = 0, 2, 3
```

**1,331 of 1,331 combinations agree** — 11 row values × 11 × 11 argument values, exhaustively —
and a **hold-out** of 120 random cases the model was never fitted to agrees **120 of 120** on each
of byte positions 0, 2 and 3.

**The rule above is the special case `b = 0`.** With `b` zero the cross term vanishes and
`2 x ((row x a) mod 256)` never exceeds 510, so the `mod 512` is the identity and the two
expressions are the same. Nothing measured before is contradicted; it was measured with one
argument.

> ### The three pieces, and what each one explains
>
> | piece | what it does |
> |---|---|
> | `row[i] x (a + b) mod 256` | the arguments **enter as a sum** before meeting the row |
> | `x 2` | the 7-bit fixed point, doubling a `0..127` fraction into `0..254` |
> | `((a x b) >> 7)` | **the cross term** — the piece that made two arguments look like they did not add |
> | `mod 512` | a **nine-bit** intermediate, and only then the saturation to 8 bits |
>
> **`EN-1`'s six deviations of `+1`, `+2` and once `+12` are exactly this cross term.**
> `(a x b) >> 7` is 1 when the product reaches 128, 2 at 256, and 12 at 1,536 — small, sporadic,
> and invisible to a model built from one argument at a time.
>
> **And the `mod 512` was the last piece, not the first.** Four placements of the saturation
> (per-term, sum-first, wrapped, saturated) all plateaued at **1,256 of 1,331**, and every one of
> the 75 failures was the same shape: `634 -> 122`, `600 -> 88`, `556 -> 44`. Those are the sum
> **mod 512**. A nine-bit intermediate fits all 1,331.

**The arguments are reduced to bytes first.** `a = 300` behaves exactly as `a = 44`, which is what
`arg_byte[i]` means and is worth stating because a caller passing `int32_t` may not expect it.

**Byte position 1 does not obey this rule** — 56 of 120 hold-out cases disagree — which is
consistent with §6's separate finding that `row[1]` is not part of the positional family. What it
is instead remains unresolved. *(Resolved 2026-09-17, UQ-42: byte 1 is the high byte of the lanes' signed ceiling, so it is both a multiplicand for lane 1 and the bound for lanes 0..3.)*

> #### A hypothesis that was killed by its own test
>
> The eight `imul` instructions are each fed by **`movsx`** — sign-extended 16-bit operands — and
> the four results are stored back as 16-bit words at `022D8F30`…`3C`. That reading predicts the
> row is **four signed 16-bit lanes**, and therefore that `row[1] >= 0x80` forces `0xFF` because
> byte 1 is lane 0's **high** byte.
>
> **It is wrong.** Setting the high byte of every lane in turn, only byte 1 does it: bytes 3, 5
> and 7 at `0x80` change nothing, and all four at `0x7F` change nothing. **A lane sign bit would
> have fired four times.** The prediction was made, tested immediately, and killed.

> **The two narrowing steps behave differently, and one call shows it.** `row = 127, arg = 3`
> gives `0xFA`, not `0xFF`: the inner product `381` is **truncated** to its low byte `125`, and only
> the outer doubling `250` would have been **saturated** had it exceeded 255. A model that
> saturated at both stages predicts `0xFF` and is wrong on that input.

```
127 x 1 = 127  -> low byte 127 -> x2 = 254 -> 0xFE
127 x 2 = 254  -> low byte 254 -> x2 = 508 -> 0xFF   (saturated)
127 x 3 = 381  -> low byte 125 -> x2 = 250 -> 0xFA   (truncated, then no saturation needed)
 16 x 16 = 256 -> low byte   0 -> x2 =   0 -> 0x00
```

**Bytes 4–15 of the row are inert** — set to `0xFF` individually, none of the twelve changes the
result.

### `row[1]` is not part of that family

**`row[1] >= 0x80` forces all four output bytes to `0xFF`, with both integer arguments zero.**
`0x7F` there does nothing; `0x80`, `0xC0`, `0xFE`, `0xFF` all produce `FFFFFFFF`. The equivalent
byte one lane up, `row[3] = 0x80`, does **not** do this — it obeys the positional rule.

**So it is byte 1 specifically, not a lane's sign bit**, and what it selects is not established.

## 7. Modding notes

- **Two rows are protected and the rest are not.** If you hook one of the nine functions in §4 and
  scribble on `022D8F30` or `022D8F90`, your write is undone on return; if you scribble anywhere
  else in the workbench it persists into the next user, which may be the sound code.
- **The depth counter is at `022D8F30`'s neighbour, `022D8F08`.** Reading it tells you whether a
  save is outstanding. Writing it is how you would break every restore at once.
- **Do not name a target whose 16 bytes cover the counter** *(2026-09-27, FABLE, Claude Opus 5.5; bytes re-read,
  on ASTRA's [workbench-depth-target-alias](../../_experiments/evidence/workbench-depth-target-alias/README.md))*.
  `Save` copies each target before it assigns the depth (`0036D982`), so a target spanning `022D8F08` captures
  the counter while it is still 0. `Restore` writes each item with `movups` (`0036D90F`) and only then
  re-reads the depth for its loop test (`0036D912` / `0036D918`). That target puts the saved 0 back, the loop
  ends early, and every later item stays unrestored. For example, with `022D8F08` first and `022D8F90` second,
  the second is never written back. "No save outstanding" is therefore not enough for Restore's all-items
  postcondition: no target span may overlap the four counter bytes either. The counterexample is a source
  calculation; none of the nine callers in section 4 is shown passing such a target.
- **Do not call `Save` from a hook inside one of the nine.** The depth is assigned, not
  incremented; your save replaces the outer one and the original row is lost.
- **`0026EE00` takes an operand through memory.** Calling it with three pointers and stale contents
  at `022D8F10` computes against whatever the previous caller left.

## 8. What is not known

- [x] ~~**UQ-41.** **What the nine functions are for.** Their callers sit in the Presentation layer, but a caller~~
      is not evidence of ownership and none of the nine carries a ledger owner.
      ***ANSWERED 2026-09-17 (FABLE): the nine are ported VU0-style helpers that use the two contended rows as their own registers, which is why each must save what a caller may hold live.** `0026EE00` is the colour modulate (UQ-43). `003AFDD0(float4 in, u32 out)` truncates the four floats to integers (`cvttps2dq`, `003AFDFB`), interleaves their bytes with the operand row's bytes on the row `022D8F30` (the pack idiom the modulate uses), and returns the four low bytes as one dword through `out` (`003AFF99`..`003AFF9F`): a float4 to byte4 pack without saturation. (The operand row is the one §4 names as read and never written by the modulate; this helper only reads it too.) `00431D30` and `00462260` are byte-identical twins of it (the bodies differ only in their addresses) that start from one sign-extended `int32` instead of four floats (`movsxd rax, [rbx]`). `002F1CE0(vec)` is a 3-vector length: the squares go to `022D92E0`..`022D92F8`, the sum through `sqrtf` (`00861F14`), `[01EF93F0]` is added, the length is left at `022D9198` and the row copied to `022D8F90`, and it returns the length (`002F1CFA`..`002F1D88`). `002F1D90(a, b)` is the distance between two points, `b - a` then the same sum, root and stores, after the `vf00` reset `0036DD80` (`002F1DB1`..`002F1EA6`). `003D8E50(x)` is ~~a random number in `[0, x)`~~ a scaled random number *(corrected 2026-09-28, FABLE, Claude Opus 5.5: `[0, x)` is not guaranteed. A subnormal `x` can return `x` itself, and `x` near FLT_MAX overflows to +infinity; see [the RNG streams page](../../21-RNG-And-Determinism/rng-streams.md), `003D8E50`)*: with `[022D9138]` set it runs the 23-bit recurrence on `01EF93E8` (the shared procedural random of [the authored-randomness page](../../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md)) five rounds, forms a float in `[1, 2)` from the state, and returns `x` times that minus `x` times `[01EF93FC]` (`003D8F44`..`003D8F71`), then runs two more rounds; with the gate clear it uses the constant `[01CEBBA8]` instead (`003D8F36`..`003D8F3C`); zero returns zero without touching the bank (`003D8E5D`..`003D8E6B`). `0042FDB0(record, context)` is the authored-expression evaluator's colour form: it evaluates the record's four operands through `004314E0`, `00431080` and `00431350` (that page's `eval`, operand and `combine`) and packs the results as bytes through the same operand-row interleave. `0044BAC0` is the type-`0x0A` element walk of [the element-types page](../../17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md), which composes through the transform primitive `002F1F40`, the mode adder `0039B620` and the modulate. Every one of them writes `022D8F30` or `022D8F90` for its own arithmetic, the two slots §5 shows are the only ones anything protects, so the pair exists to keep a helper's scratch from corrupting a transform its caller has in flight. Static, the five small bodies read in full, the three large ones by their callees and the pages that own them.*
- [x] ~~**How `0026EE00`'s two integer arguments combine.**~~ **ANSWERED 2026-09-08** — they
      **multiply**, and the cross term is `(a x b) >> 7`. See §6; 1,331 of 1,331 exhaustive plus a
      120-case hold-out on each of bytes 0, 2 and 3. `EN-1`.
- [x] ~~**UQ-42.** **What `row[1] >= 0x80` selects.**~~
      ***ANSWERED 2026-09-17 (FABLE): `row[1]` is the high byte of the signed 16-bit ceiling the function applies to all four output lanes; the ceiling's low byte is forced to `0xFF`.** The code: after the eight lane products, `0026EE00` takes the row's first eight bytes, forces byte 0 to `0xFF` (`movq rax, xmm3; or rax, 0xFF`, `0026F173`..`0026F178`) and stores them at `022D8FC0`; the word shuffles at `0026F1B8`..`0026F2A6` leave that block as eight words, the first four all `row[1]:0xFF` and the last four all `row[3]:row[2]`. The products are shifted right by 7 (`psrlw`, `0026F2A2`, the seven-bit convention of UQ-43) and the loop at `0026F2C0`..`0026F2D6` then does `if (lane >= bound) lane = bound` on each of the eight words with a **signed** compare (`cmp`/`jl`). The returned dword is the low byte of lanes 0..3 (`0026F375`..`0026F3B2`, `0026F3F7`..`0026F3FD`). So with `row[1] = 0` the ceiling is `0x00FF` and a lane saturates at 255, the ordinary colour clamp; with `row[1]` in `1..0x7F` the ceiling is `0x01FF`..`0x7FFF` and only a lane's low byte survives the pack, so 508 comes out as `0xFC`; with `row[1] >= 0x80` the ceiling is negative, every non-negative lane is replaced by it, and its low byte `0xFF` is what packs out, which is the `FFFFFFFF` the probe measured. `row[3]` bounds lanes 4..7, which the returned dword never shows, hence its inertness. Executed through the page's own apparatus (`workbench_probe.py`): `row = {7F, r1, 7F, 7F}`, `a = 2`, `b = 0` gives byte 0 = `FF` for `r1 = 0`, `FC` for `r1` in `{1, 2, 7F}` (the un-saturated 508) and `FFFFFFFF` for `r1` in `{80, FF}`; `a = 1` gives `FE` for `r1` in `{0, 1}`, and `a = 3` gives `FA` for both, as the reading predicts. Which value the nine callers leave in byte 1 of the operand row `022D8F10` is not read here: no rip-relative store writes that row, so the callers fill it through pointers. Static code reading, confirmed by executing the shipped bytes.*
- [x] ~~**UQ-43.** **What the computation means.** The mapping is measured; its purpose is not established.~~
      ***ANSWERED 2026-09-17 (FABLE): colour arithmetic in the PS2 seven-bit convention, applied to the render records' colour words.** The callers show the purpose. `00442600` runs `0026EE00(out = rec+0x240, a = rec+0x240, b = rec+0x1F0)` in place and skips the call when the multiplier dword at `+0x1F0` is `0x80808080` (`004426A9`..`004426C0`), so `0x80` is unity and the `(a x b) >> 7` cross term is the modulate; `004427D0` and `00442550` feed the record's colour dwords `+0x250`/`+0x254` and `+0x240` through it with a stack word as the second operand and destination; `002F1F40` picks `+0x334` or `+0x398` by a mode byte (`002F2312`). The row term `2 x ((row x (a + b)) mod 256)` is the contribution of the operand the caller leaves at `022D8F10`, zero when that row is zero, which is what makes `b = 0x80808080` an identity on `a`. So the function is a colour modulate with an additive row, in the fixed point the PS2 used for vertex and texture colours; what each caller's row operand represents is named only by its position, and the row's byte 1 (UQ-42) stays open. Static, callers read.*
- [x] ~~**UQ-44.** **Whether any path nests a save.** None was observed; the depth counter would not survive one.~~
      **ANSWERED 2026-09-16 (FABLE): NO PATH NESTS A SAVE - and this never needed an observation.** *None was observed* is a statement about looking; nesting is a **reachability** property and the image decides it. **Only the nine can open a save.** `Save` `0036D930` has **exactly nine direct callers, and they are precisely the nine** - no tenth caller exists anywhere in the image. **Eight of the nine reach none of the others at all.** Forward cones, `Save`/`Restore` excluded: `0026EE00`, `003AFDD0`, `00431D30`, `00462260` and `003D8E50` reach **nothing**; `002F1CE0` reaches one function, `002F1D90` two, `0042FDB0` twenty-two - and **none of those cones contains one of the nine.** **The ninth does reach six of them, and that is where the question is decided.** `0044BAC0` (3,461 B) reaches `0026EE00`, `002F1D90`, `003AFDD0`, `003D8E50`, `0042FDB0` and `00431D30`. **But its save window is 133 bytes of straight-line code.** Between `Save` at `0044C43E` and `Restore` at `0044C4C3` there is **no branch and exactly one call - `00861F14 sqrtf`** - the rest being SSE arithmetic that squares three components, sums them and stores the root. **Every one of those six calls lies outside the window.** **So the depth-of-one design is safe as shipped, and it is safe by placement rather than by construction.** That makes §7's warning sharper, not weaker: *do not call `Save` from a hook inside one of the nine* is exactly right, because **a hook would introduce the edge the shipped image happens not to have.** The counter would not survive it. *Which part is body-read and which is graph.* For `0044BAC0` the window is **read in full**, so that arm is complete - an indirect call inside it would have been visible and there is none. For the other eight the claim rests on the **direct-call** graph, so an indirect call from one of them into another of the nine would not appear. **That is the one residue, and it is much smaller than the row.**
- [x] ~~**UQ-45.** **Any runtime observation.** None exists — the emulation runs shipped bytes, not the game.~~
  **SUPERSEDED** (2026-09-14, FABLE; EVIDENCE-STANDARD addendum 2026-09-15bk, kind (c)). Every claim in §9 is tier 1 and
  PROVEN, including the restore, which was shown by executing the shipped pair. No claim on this page waits on an
  observation, and an observation would add nothing to them. A future question that needs one (for example, how often a
  path saves in play) should be filed as its own question.

## 9. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| a save/restore pair exists | `0036D930` and `0036D8E0` read in full (§3) | 1 | PROVEN |
| nine callers each, the same nine | `E8`/`E9` scans with a positive control for each instrument; the two caller sets are identical | 1 | PROVEN |
| four restores are tail-jumps | `0026F413`, `003AFFAB`, `00431F0A`, `0046242E` found by the `E9` instrument, control `001D1660` → 1 | 1 | PROVEN |
| the depth lives at `022D8F08` | `mov [022D8F08], ecx` at `0036D982`, compared at `0036D8E6` | 1 | PROVEN |
| only `022D8F30` and `022D8F90` are protected | argument setup decoded at all nine `Save` sites, RIP displacements resolved with a tool | 1 | PROVEN |
| the workbench IS restored, for those rows | the shipped pair executed under emulation: a 16-byte marker at `022D8F30` survives a call to `0026EE00` and the depth returns to 0 | 1 | PROVEN |
| `022D8F10` is read and never written by `0026EE00` | every RIP-relative operand in its 1,560 bytes classified read/write | 1 | PROVEN |
| `out_byte[i] = min(255, ((2·((row[i]·(a+b)) mod 256)) + ((a·b) >> 7)) mod 512)` | **1,331 of 1,331** exhaustive (11 rows × 11 × 11 arguments) plus **120 of 120** hold-out on each of bytes 0, 2, 3, by executing the shipped bytes; apparatus kept as `workbench_probe.py` | 1 | PROVEN |
| the single-argument form is its `b = 0` case | the cross term vanishes and `mod 512` becomes the identity; 168 earlier combinations reproduced exactly | 1 | PROVEN |
| the two integer arguments simply add | **CONTRADICTED** — they **multiply**: with the row zero, either argument alone gives 0 and the pair gives `min(255, (a·b) >> 7)`. The 6 deviations of `+1`, `+2` and `+12` are exactly that term | 1 | CONTRADICTED |
| the row is four signed 16-bit lanes, so `row[1] >= 0x80` is a lane sign bit | **CONTRADICTED by its own test** — bytes 3, 5 and 7 at `0x80` change nothing; a lane sign bit would have fired four times | 1 | CONTRADICTED |
| what `row[1] >= 0x80` selects | ~~**not established**~~ **the high byte of the signed 16-bit ceiling applied to lanes 0..3, low byte forced `0xFF`** (UQ-42, 2026-09-17): code at `0026F178`, `0026F2C0`..`0026F2D6`, and the probe reproduces `FF`/`FC`/`FFFFFFFF` for `row[1]` = 0 / 1 / `0x80` | 1 | PROVEN |
| what any of it is for | **not established** | — | UNKNOWN |
| any runtime observation | **none exists** | — | UNKNOWN |

## 10. Related

- [The shared transform workbench](the-shared-transform-workbench.md) — the area, its 249 writers, and the §6 note this corrects
- [Why the unowned code has no owner](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md) — the ownership standard applied to functions like these

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

**Every cell of §4's table reproduces**, and so does every count around it.

| claim | measured |
|---|---|
| `Save` `0036D930` **89 B**, `Restore` `0036D8E0` **66 B** | **89** and **66** |
| "nine functions" | **9 call `Save`, 9 call `Restore`** |
| "none saving without restoring and none restoring without saving" | the two sets are **identical** — 9 of 9 do both, neither difference is non-empty |
| the eighteen site addresses | **all eighteen exact**, function for function |
| "four of the nine restores are tail-jumps — `0026F413`, `003AFFAB`, `00431F0A`, `0046242E`" | those **four are `jmp`** and the other five are `call` — no other split |
| "`Restore` zeroes it, so a nested save loses the outer frame" | `0036D91A mov dword ptr [022D8F08], r8d` with `r8d = 0`, and `022D8F08` is the same count `Restore` loops on |

### A census keyed on the globals finds `Save` and misses `Restore`

§3 quotes `Save`'s addressing as `lea r9, [02EC0800]` — a direct rip-relative reference. **`Restore`
does not use that form.** It materialises the image base once and indexes from it:

```asm
0036D8EE  lea   r9, [rip - 0x24d8f5]              ; r9 = 00120000, the image base
0036D8FE  mov   rax, qword ptr [r9 + rax*8 + 0x2da0a00]   ; -> 02EC0A00, the pointers
0036D906  movups xmm0, xmmword ptr [r9 + rcx*8 + 0x2da0800] ; -> 02EC0800, the values
```

A whole-image sweep for operands *resolving* to `02EC0800` / `02EC0A00` returns **one function** —
`0036D930` — because `Restore`'s two accesses are base-plus-displacement and never name the address
in a single operand.

> **So a reader censusing "who touches the saved area" finds the writer and not the reader**, and
> would conclude the save is never read back. The database has met this shape before — *a
> displacement is only an offset when the register holds the base* — and this is the same trap from
> the other side: here the register holds the **image base**, so the displacement is the whole
> address.

**Not claimed:** the "249 functions that write it" and "240 restore nothing" belong to
[the workbench document](the-shared-transform-workbench.md) and were **not** re-derived here — this
pass tested the pair and its nine users. §5's two-protected-rows finding is untouched. Nothing was
executed or observed live.

*(Pass 22 adjacency, 2026-09-14: the console dispatcher `001D1660` this page cites calls
**audio** `002DEBA0`/`001DBB00` and **resource** `002EEEE0` (3 edges) — the shared machinery's
fetch legs, not workbench plumbing.)*

*(Pass 22 live-graph completion, 2026-09-15: the audio callee `002DEBA0` is itself called by
`WorldAreaField` `00314020` (1 edge) — the dispatcher's fetch leg is shared with field code.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: `00314020`'s callees reach `ActorEntity`
(`00263660`, `0025BFB0`, and three more, 5), `Movement` (`0046AFA0`, `003DAA20`, and three
more, 5) and `Party` (`00358C60`, `00358EE0`, 2) — the field-side caller of `002DEBA0` walks
actor, locomotion and party state like every field body.)*

`0044B8C0` (160 B) is the matrix-scalar helper `0044BAC0` runs inside its save window: `[rcx]`'s row stages into `022D92E0`, `xmm3 = splat([01EF93FC]) * row` lands at `022D91A0`, and the `xmm1`-scaled lane products accumulate back through `022D92E4`/`022D92E8`/`022D92EC`/`022D92F0` before the rebuilt row copies back to `[rcx]` - the workbench bank doing double duty as operand scratch

Interior anchor `0044B8E8` (function `0044B8C0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Presentation — CLIENT (438 edges, shared machinery).** The console dispatcher `001D1660` and the fetch leg `001DBB00` this page cites in its pass-22 adjacency notes sit inside a wide presentation fan (`001C7360`, `001C7520`, `001D5120`, `001DBB00`'s own presentation callers) — the shared fetch machinery reaches the rendering layer from many owners, not a workbench-owned relationship.
- **Input — SERVICE (2 edges).** 2 outbound (page-cited `World_UpdateSimulationTick` (00314020) call Input bodies `0036FD90`, `002E09A0`). Substantive edges include `World_UpdateSimulationTick` (00314020) calls `0036FD90`; `World_UpdateSimulationTick` (00314020) calls `002E09A0`.
- **UI — MECHANICAL (1 edge).** 1 UI-side calls into shared helper(s) the page cites (`0036DD80`) - the helpers' general call surface, not a UI relationship of this page's subjects.
- **World — SERVICE (1 edge).** 1 outbound (page-cited `World_UpdateSimulationTick` (00314020) call World bodies `002623A0`). Substantive edges include `World_UpdateSimulationTick` (00314020) calls `002623A0`.
- **WorldAreaField — CLIENT and SERVICE (9 edges).** 7 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `0025BFB0`, `00263660`, `002DEBA0`); 2 outbound (page-cited `World_UpdateSimulationTick` (00314020) call WorldAreaField bodies `BattleSystem_RunFieldFrameOrchestrator` (00234590), `WorldSimulation_ProcessDeferredModeRequest` (0032FC30)). Substantive edges include `0025BFB0` is called by `World_UpdateSimulationTick` (00314020); `00263660` is called by `World_UpdateSimulationTick` (00314020); `002DEBA0` is called by `World_UpdateSimulationTick` (00314020); `World_UpdateSimulationTick` (00314020) calls `BattleSystem_RunFieldFrameOrchestrator` (00234590).
