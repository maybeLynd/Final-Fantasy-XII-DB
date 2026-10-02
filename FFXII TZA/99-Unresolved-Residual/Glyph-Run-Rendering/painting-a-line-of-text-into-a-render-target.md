---
system: Painting a line of text into a render target
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Presentation.Text
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001E9D20`, `002AF960`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: pair-frontier-repos-55
  crossref_clean: true
  reopened_count: 0
---

# Painting a line of text into a render target

**A pair-census row: `+0x2348`, two sites, two functions, two documents, neither citing the other.**
`001E8070` is the glyph emitter (a row in
[how-a-line-of-text-becomes-glyph-quads](how-a-line-of-text-becomes-glyph-quads.md), named by the
string `fontclut_%d` and never opened). `001E8580` was **the sixth-largest of the 158 unresolved
residuals** at survey date, 3,572 bytes — classified at GN161 `Presentation.Text.GlyphBatchFlushAndOffscreenTextTargetComposite`.

Reading the two together resolves the residual and produces a mechanism neither function states.

**The object both operate on is a singleton.** `001E8580`'s only caller is `0017F850`, which is
**the function the string `"display : draw Font"` names** — the string the residual survey found one
call below four unclassified font routines:

```c
void FUN_0017f850(void) {              // 0017F850
    FUN_001eb150("display : draw Font");   // profiler scope in
    ctx = FUN_001b5fa0();                  // 001B5FA0: return DAT_01F811F8
    FUN_001e8580(ctx);
    FUN_001eb110();                        // scope out
}
```

**`001B5FA0` is a one-line accessor returning the global at `01F811F8`.** Everything below —
the batch array at `+0x70`, the matrix at `+0xE30`, the palettes at `+0x1358`, the target ladder
slots at `+0x13C0`, the target cache at `+0x1500`, the records at `+0x2320` — is inside **one
object, reached from one pointer, drawn once per frame under a named profiler scope.**

## 1. What the player sees

**A line of FFXII text is often not drawn onto the screen at all. It is drawn onto its own private
picture first, and the picture is then stamped onto the screen as one rectangle.**

The game keeps **ten blank pictures in ten sizes** — from a 50×60 stub big enough for a damage
number, up to a full 1920×1080 sheet — and before it paints a line it measures the line and takes
**the smallest picture the line fits inside.**

**Why the game bothers is visible the moment text fades.** If a fading line were drawn letter by
letter at 40 % opacity, every place where two letters' soft edges overlap would go *darker* than the
letters themselves, and the line would come apart into its characters as it faded. Painted opaque
onto its own sheet and faded once, **the line fades as a line.** That is exactly the branch this
document's shared byte selects: with it set, the glyphs go down at flat palette opacity and the
run's fade is applied a single time, to the finished rectangle.

**And the ladder has a top rung, which is a real modding limit.** A line that will not fit the
largest sheet prints, on the developer console:

> `Font Paint Size is Bigger than Biggest Render Target!`

and is painted into the 1920×1080 sheet anyway. **A mod that enlarges the font, widens a window, or
lengthens an authored line past the full-screen sheet does not fail quietly — the engine says so and
then over-runs the largest target.**

## 2. The ladder: ten render targets, at `009018F0`

`001E97B0` is the chooser. It is **called from exactly one place in the image** — `001E8642`, inside
`001E8580`.

```c
box_w = record[+0x2330] - record[+0x2328];      // maxX - minX
box_h = record[+0x2334] - record[+0x232C];      // maxY - minY
i = 0;
while (table[i].w <= box_w || table[i].h <= box_h) {
    if (++i > 9) { FUN_0017d280("Font Paint Size is Bigger than Biggest Render Target! \n");
                   return 9; }
}
return i;                                        // 001E97B0
```

**The table is 10 pairs of `int32` at `009018F0`**, read as `[i*8]` = width, `[i*8+4]` = height:

| i | width | height |
|---:|---:|---:|
| 0 | 50 | 60 |
| 1 | 100 | 60 |
| 2 | 150 | 60 |
| 3 | 200 | 60 |
| 4 | 360 | 60 |
| 5 | 960 | 60 |
| 6 | 1920 | 108 |
| 7 | 1920 | 220 |
| 8 | 1920 | 540 |
| 9 | 1920 | 1080 |

> **Six single-line rungs at 60 pixels tall, then four full-width rungs of growing height.** The
> ladder is not a geometric progression — it is **an authored guess about the shapes text actually
> takes**: short tags, then lines, then paragraphs.

**The test is strictly greater.** A box exactly 200 × 60 does *not* fit rung 3; `<=` advances. And
the overflow return is **9, not an error** — the caller cannot distinguish "fits the biggest" from
"did not fit anything", because both return 9.

**The chosen index selects a target object** at `param_1 + 0x13C0 + i*0x20` — the `lea rbx, [r15 +
0x9e]; shl rbx, 5; add rbx, r14` at `001E8664`–`001E866F`, which is `(i + 0x9E) * 0x20 + base`.

## 3. The 44-byte record the two functions share

**Base `param_1 + 0x2320`, stride `0x2C`, indexed by the `int` at `param_1 + 0x20`, and there are
exactly two of them** — `001E9159` adds `0x2C`, `001E915D` compares the counter against 2, and the
initialiser at `001E7396` starts its two-iteration loop at `+0x2320`.

> **CORRECTED 2026-09-03, same session.** This document first gave the base as `+0x2324`. Every
> field address below is unchanged — `001E8070` computes `idx*0x2C + 0x2324 + base` and that
> arithmetic is right — but the record **starts four bytes earlier**, at a dword this document had
> not seen, and the tail is **two** spare bytes rather than six. **The record was described from its
> busiest field outward instead of from its own beginning**, which is what reading only the two
> functions that use it will do.

| record | absolute (index 0) | width | what the code does with it |
|---|---|---|---|
| `+0x00` | `+0x2320` | dword | **zeroed at init** (`001E73A0`); read and written by `001E9D20` (`001E9DF4`, `001E9E2A`). **Neither function in this pair touches it.** |
| `+0x04` | `+0x2324` | byte | **set to 1 by every emitted vertex** (`001E83A3`); cleared by the flush (`001E9122`) |
| `+0x08` | `+0x2328` | float | **min X** — reset to **1920.0** (`001E9128`) |
| `+0x0C` | `+0x232C` | float | **min Y** — reset to **1080.0** (`001E9131`) |
| `+0x10` | `+0x2330` | float | **max X** — reset to 0.0 |
| `+0x14` | `+0x2334` | float | **max Y** — reset to 0.0 (`001E913A`) |
| `+0x18` | `+0x2338` | float | **origin X** — same value as min X, reset to **0.0** |
| `+0x1C` | `+0x233C` | float | **origin Y** — same value as min Y, reset to 0.0 (`001E9143`) |
| `+0x20` | `+0x2340` | float | the run's **first** alpha — **not reset by the flush**; set to `1.0f` by the begin |
| `+0x24` | `+0x2344` | float | the run's **latest** alpha — **not reset by the flush**; set to `1.0f` by the begin |
| `+0x28` | `+0x2348` | byte | **paint offscreen** (the pair-census row) — **initialised to 1** |
| `+0x29` | `+0x2349` | byte | **seed the first alpha** — **initialised to 1**, then read and cleared by the emitter |
| `+0x2A`–`+0x2B` | `+0x234A`–`+0x234B` | 2 B | untouched by anything found |

### The initialiser, which neither function contains

`001E71B0` builds both records in a two-iteration loop. **It is not the only place their starting
values come from** — the per-frame begin below runs the same reset — but it is the first:

```asm
001E7391  mov   ecx, 0x2                            ; two records
001E7396  lea   rax, [r14 + 0x2320]                 ; the true record base
001E73A0  mov   dword ptr [rax], esi                ; +0x2320 = 0
001E73BC  mov   dword ptr [rax + 0x20], 0x3f800000  ; +0x2340 = 1.0f
001E73C3  mov   dword ptr [rax + 0x24], 0x3f800000  ; +0x2344 = 1.0f
001E73CA  mov   word  ptr [rax + 0x28], 0x0101      ; +0x2348 = 1 AND +0x2349 = 1
001E73D0  lea   rax, [rax + 0x2c]
001E73D8  jnz   0x001E73A0
001E73DA  mov   word  ptr [r14 + 0x2378], cx        ; cx == 0: +0x2378 = 0 AND +0x2379 = 0
```

### And the per-frame begin, which re-arms what the initialiser armed

**`001E9920` is the begin**, reached through the wrapper `0017FA10`:

```c
void FUN_0017fa10(a, b, offscreen) {        // 0017FA10
    FUN_001e9920(FUN_001b5fa0(), a, b, offscreen);
}
```

It runs the same two-record loop, and **rebuilds every field the initialiser set**: `+0x2320 = 0`,
`+0x2324 = 0`, `+0x2328 = 1920.0`, `+0x232C = 1080.0`, `+0x2330`–`+0x233C` zeroed, `+0x2340` and
`+0x2344` back to `1.0f`, **`+0x2348` from its fourth argument**, and **`+0x2349` back to `1`**.
It also resets the batch cursors, sets `+0x1390`/`+0x1398` from its two handles, and puts the four
per-corner multipliers at `+0x137C` back to `1.0f`.

> **So the initialiser is not special — `001E9920` is the same reset run every frame**, and the
> record's starting values are the *begin's* values, not the constructor's.

**Who calls it settles the residual cluster with a call edge instead of a string.** ~~Eleven sites in~~
~~seven functions~~ Twelve sites in eight functions *(corrected 2026-10-02, OPUS: rel32 sweep; the kind-1 column-2 drawer and `002AAE40` call it too, at +0x3FD of the kind-1 column-2 drawer and at `002AAE40`+0x52C)*, and **three of them were on the 158 list**: `002AC5F0` (7,489 B — ~~still residual,~~
~~the largest unclassified function in the game~~ classified at GN162 as `UI.Text.ControlCodeInterpreter` *(answered: see the dispatch-table page §1; 2026-10-02, OPUS)*), `003649A0` (3,020 B — GN161 `Presentation.Text.GlyphRunTexturedQuadEmissionAndPenAdvance`) and `002AF960` (1,117 B — GN161 `UI.Text.GlyphRunPositioner`), plus `002A9F00`,
`002B0280` and `002D28E0`.

> **Corrected 2026-09-14 (OPUS): two of the three, against today's list.** The residual list has
> gone **158 → 139** and `003649A0` is no longer on it — the certified parent classified it
> `Presentation.Text.GlyphRunTexturedQuadEmissionAndPenAdvance`. `002AC5F0` and `002AF960` remain.
> **The call evidence is unaffected**: eleven sites in seven functions, and the argument this
> paragraph makes — that a call edge settles the cluster where a string could not — is strengthened
> rather than weakened by one of the three since being classified into that very cluster.

**The flag is a literal `1` at three of the four sites read**, and the constant is not written as one:

```asm
002AC7EC  call 0x0017F850             ; draw what the last frame accumulated
002AC7F1  mov  rcx, qword ptr [r14 + 0xb8]
002AC7F8  mov  edx, 0x44
002AC7FD  lea  r8d, [rdx + -0x43]     ; 0x44 - 0x43 = 1  <- the offscreen flag
002AC801  call 0x0017FA10             ; then begin the next
```

**`lea r8d, [rdx - 0x43]` materialises `1` by arithmetic on another argument**, so a search for
`mov r8d, 1` finds nothing. **A fifth way a constant hides**, after the four in §7.

**`edx` is `0x44` at every site read**, landing in `+0x1390`; `rcx` lands in `+0x1398` and is a
pointer at three sites but the **immediate `0x3001`** at `00364A46` — **so `+0x1398` is a handle,
not necessarily an address.** The fourth site also leaves `r8d` carrying a runtime value rather than
a constant, **so the flag is not always `1`.**

**Draw precedes begin** at these sites — `0017F850` then `0017FA10` — which is what an immediate-mode
text layer that presents last frame's accumulation looks like.

**The fourth site is the only one that decides, and what it decides on is a small enumeration:**

```asm
00364A20  lea  eax, [r8 + 0x1]     ; r8 = this function's own mode argument
00364A24  cmp  eax, 0x1            ;   r8 == 0 ?
00364A27  jz   0x00364A36
00364A29  add  eax, -0x4           ;   eax = r8 - 3
00364A2C  cmp  eax, 0x1
00364A2F  jbe  0x00364A36          ;   r8 in {3, 4} ?
00364A31  xor  r8d, r8d            ; no  -> offscreen = 0
00364A36  mov  r8d, 0x1            ; yes -> offscreen = 1
```

> **Offscreen painting is selected when the caller's mode is `0`, `3` or `4`, and not otherwise** —
> a `switch` whose three cases share one arm, compiled into two comparisons. **This is the only
> evidence in the database about *when* the engine chooses to paint text to a texture**, and it says
> the choice is made per text-drawing mode by `003649A0`, a 3,020-byte function (residual when surveyed; GN161 `Presentation.Text.GlyphRunTexturedQuadEmissionAndPenAdvance`) with a single caller
> (`002DD5D0`).

**A contradiction was reported here and it has been withdrawn.** The claim was that `+0x1398`
receives *"a pointer at three sites and the constant `0x3001` at a fourth"*, and that one of the
four readings had to be wrong.

> **Nothing said any of them was a pointer.** Three sites do `mov rcx, qword ptr [r14 + 0xb8]` — a
> **64-bit load from a field**, which says the value is 64 bits wide and nothing whatever about what
> it means. **I inferred "pointer" from "qword", and a qword load is not evidence of a pointer.**

**The argument mapping was verified rather than assumed**, and it holds: `0017FA1F`–`0017FA35` moves
the caller's first argument into `rdx` and its second into `r8`, and `001E9A04` stores the first into
`+0x1398`. **So `+0x1398` really does receive `0x3001` at one site and a field value at three.**

**That is not a contradiction — it is a 64-bit handle supplied two ways**, as a literal in one caller
and out of a field in the others. `0x3001` sits below the image base so it is certainly not a code or
data address, and **the three field reads were never shown to be addresses either.**

**What the field holds is not established.** Both it and `+0x1390` are stored verbatim into the draw
object at `+0x30` and `+0x38` (`002134A0`, `00213550`) and this document does not follow them further.

> **The strangeness of the result was the tell that my reading was wrong, not a finding about the
> engine** — the second time tonight, and this time it took one tick rather than one hour.

**Three things fall out of five instructions.**

**Offscreen painting is the default, not the special case.** `+0x2348` starts at **1**. This
document's §4 and §5 present the offscreen path as the branch that has to be selected; **it is the
branch that has to be turned off.**

**The alpha pair starts at `1.0f`, and that is why the flush never resets it.** `001E9122`–`001E9143`
deliberately stop short of `+0x2340`; ~~the values are seeded once at construction and thereafter only~~
~~ever carry a run's own alphas.~~ *(answered: see the begin re-seeds them each frame, and the falsification row "An earlier version of this row"; 2026-10-02, OPUS)*

**`+0x2378` and `+0x2379` are cleared together by one `word` store**, so at construction the flush
takes the *flush-and-forget* path of §5 ~~and the suspend flag is off~~ *(answered: see "CORRECTED — `+0x2379` is not a suspend flag" below; 2026-10-02, OPUS)*.

**`+0x2378` is a different byte from `+0x2348` and nothing established here sets it.** The begin
above sets the **per-record** flag; `+0x2378` is the **outer gate**, and until it is non-zero the
flush never reaches a record at all. Its only dedicated setter is the seven-byte
`001E9F30  mov byte ptr [rcx + 0x2378], dl; ret`, with a matching getter at
`001E9A20  movzx eax, byte ptr [rcx + 0x2378]; ret`.

> **`001E9F30` has no references of any kind — not a call, not a vtable slot.** It is also **not
> inside any function Ghidra has defined**, which is why the instruction search in §7 reported
> `+0x2378` as having *one site image-wide* while this very setter writes it.
>
> **A search over defined instructions cannot see undefined bytes** — a sixth blindness, and the one
> that matters most here, because it means **the absence of a setter for `+0x2378` is not
> established.** This document does not claim the offscreen path is unreachable. It claims **no route
> to it was found.**

### The inverted box, and the second copy of the minimum

**`+0x2328` and `+0x232C` are reset to the screen size and `+0x2330`/`+0x2334` to zero** — the
textbook inverted-bounds initialisation, where the *first* value written always wins both
comparisons. The comparisons are at `001E83BC`, `001E83EC` (minima) and `001E8415`, `001E8430`
(maxima), each a `comiss` + `jbe` guarding one `movss`.

**`+0x2338`/`+0x233C` are written with the same value at the same moment as the minima** —
`001E83D2` sits inside the min-X branch, `001E8408` inside the min-Y branch — **so they always
agree with the minima after any glyph is emitted.**

> **They differ only in what they hold when nothing was emitted: `(0, 0)` rather than
> `(1920, 1080)`.** That is the whole reason for the duplicate — the origin is used as a
> *translation* and must be zero for an empty run, while the minimum is used as a *comparand* and
> must be the screen extent.

### The two alphas

`001E84C6` tests `+0x2349`. On the glyph where it is set, **both** `+0x2340` and `+0x2344` are
written (`001E8523`) and the flag is cleared (`001E84D0`); on every later glyph **only** `+0x2344`
is written (`001E8547`). The stored value is `(int)[param_2 + 0x8C] × (1/128) × [param_1 + 0x137C]`.

**So the pair is "the alpha the run started at" and "the alpha the run is at now"** — and they are
the last two arguments of the composite draw in §5.

## 4. The byte itself: `+0x2348`, read on both sides

**On the emitting side** (`001E826A`), the byte chooses how a vertex's alpha is built:

```asm
001E826A  cmp   byte ptr [rcx + rbx*0x1 + 0x2348], 0
001E827B  jz    0x001E8293
; NON-ZERO -> flat: palette alpha only
001E827D  mov   eax, dword ptr [r15 + 0x20]     ; the fontclut entry's alpha
001E8281  cvtsi2ss xmm0, rax
001E8286  mulss xmm0, xmm8                      ; * 1/128
; ZERO -> folded: per-corner value x per-corner multiplier x palette alpha
001E8297  movd  xmm1, dword ptr [r13 + rax*0x4 + -0x12f0]   ; [param_2 + 0x8C + k*4]
001E82A8  mulss xmm1, xmm8                      ; * 1/128
001E82AD  mulss xmm1, dword ptr [rbx + rax*0x4] ; [param_1 + 0x137C + k*4]
001E82BB  mulss xmm1, xmm0                      ; * the fontclut alpha
```

**On the flushing side** (`001E8654`), the same byte chooses the whole drawing strategy:

```asm
001E861C  lea   r12, [r14 + 0x2348]        ; the record pointer for this pass
001E8631  cmp   byte ptr [r12 + -0x24], 0  ; did anything get emitted?
001E8637  jz    0x001E9122                 ; no -> straight to the reset
001E8642  call  0x001E97B0                 ; choose a rung of the ladder
001E8654  cmp   byte ptr [r12], 0
001E8659  jz    0x001E8F53                 ; ZERO -> draw where the glyphs already are
001E865F  call  0x001FBE50                 ; NON-ZERO -> push a render target and paint
```

> **One byte, two functions, and the two readings are the same decision seen from opposite ends.**
> Set it, and the emitter stops applying the run's fade per glyph *because* the flusher is going to
> apply it once to the finished rectangle. Clear it, and the emitter must fold the fade into every
> vertex *because* there is no rectangle to fade later.
>
> **Neither function contains the other half.** From inside `001E8070` the byte looks like a shading
> option; from inside `001E8580` it looks like a rendering mode. **It is one design and the address
> is the only thing that says so.**

## 5. The three paths through the flush

`001E85ED` tests `+0x2379`. Non-zero and the function does nothing.

> **CORRECTED — `+0x2379` is not a suspend flag.** This document first called it one, on the strength
> of this single test. **Four functions read it and they do not agree with that reading:**
>
> | reader | behaviour when `+0x2379` is non-zero |
> |---|---|
> | `001E8580` (flush) | returns immediately |
> | `001E9920` (begin) | skips the entire reset |
> | `001E9C80` (transform) | **refuses the new matrix** |
> | `001E9D20` (font select) | **does more work, not less** — claims a per-owner record (§5b) |
>
> **A flag that makes three functions do nothing and a fourth do something extra is a mode
> selector, not a suspend.** In the zero mode there is one shared record driven by frame-level
> begin/flush; in the non-zero mode records are **claimed by owner id** and the frame-level
> operations stand aside. **Reading one function gave a name that three others contradict** — and
> the name was in this document for an hour before the fourth reader was opened.

`001E85FD` tests `+0x2378`, and everything below hangs off it.

### `+0x2378 == 0` — flush and forget (`001E9175`)

**31 batches** (`001E9179  mov r12d, 0x1F`), each `0x38` bytes, walked from `param_1 + 0x70`. For
each non-empty batch: allocate a `0x98`-byte draw object, hand it the batch's two handles, the
shared render parameters at `+0x1390`/`+0x1398`/`+0x13A0`, the **4×4 matrix at `+0xE30` verbatim**,
then push every `0x3C`-byte vertex. Then `cursor = begin` and the batch is zeroed.

**The record fields in §3 are neither read nor reset on this path.**

### `+0x2378 != 0`, `+0x2348 == 0` — draw in place (`001E8F53`)

A `0x170`-byte draw object, the same matrix from `+0xE30` **unmodified**, no render target pushed.
The chosen ladder index is computed but the byte handed to `FUN_00214700` is the (zero) `+0x2348`.

### `+0x2378 != 0`, `+0x2348 != 0` — paint offscreen, then composite

Three blocks, in order:

1. **Pass one.** Push the ladder target (`001E865F`–`001E8672`, mode `3`), allocate a `0x168`-byte
   object, tell it the rung index, give it the origin `(+0x2338, +0x233C)` in place of a matrix,
   and push every vertex with the flag argument **`1`**.
2. **Pass two.** `001E96A0` scans **64 slots of `0x38` bytes** at `param_1 + 0x1500` for a target
   matching four dwords carried out of the last vertex plus the rung index. The same 31 batches are
   pushed again with the flag argument **`0`**. **If the scan returns null the function returns
   immediately** — the second record is never flushed *and never reset*.
3. **Composite.** Push `param_1 + 0x2300` (mode `1`, not `3`), build a transform whose translation
   column is the origin, emit **four vertices**, and call:

```asm
001E8EF0  movss xmm2, [r12 + -0x1c]   ; minY
001E8EF7  subss xmm2, [r12 + -0xc]    ;      - originY
001E8EFE  movss xmm1, [r12 + -0x20]   ; minX
001E8F05  subss xmm1, [r12 + -0x10]   ;      - originX
001E8F0C  movss xmm0, [r12 + -0x4]    ; +0x2344 - the run's LATEST alpha
001E8F19  movss xmm4, [r12 + -0x8]    ; +0x2340 - the run's FIRST alpha
001E8F26  movss xmm0, [0x01CEBBA8]    ; 1.0f, passed three times
001E8F49  call  0x00214930
```

**`00214930` has exactly one call site in the image**, and it is this one.

> **The box is handed over relative to the origin, because the transform has already translated by
> it.** `minX − originX` is **zero** whenever anything was drawn — the two fields hold the same
> number — and is `minX` itself when nothing was, since the origin resets to zero and the minimum
> to 1920.

## 5b. Three of this document's open questions, closed from the other side

`001E9D20` — the selection routine, read and written up by `repos-78` in
[choosing-the-render-target-for-a-text-run](choosing-the-render-target-for-a-text-run.md) — answers
three things this document had listed as unestablished. **Summarised here, not re-derived:**

| this document asked | the selection routine answers |
|---|---|
| what `+0x2320` holds | **the owner's key.** The slot is claimed first-free-or-already-mine over the two records; **a slot holding `0` is free**, which is exactly what the initialiser writes. |
| what sets the record index at `param_1 + 0x20` | **this function does**, to the claimed slot — or to `0` on the path that does not claim. |
| why the group stride is `0x700` when only 31 batches are walked | **the batch index is the font size, `1 ≤ n ≤ 31`**, so slot 0 of each group of 32 is unused by construction. |

**And the batch address closes the matrix from the other end.** The open batch is
`state + 0x30 + (slot*32 + n)*0x38`. Two slots × 32 × `0x38` = `0xE00`, and **`0x30 + 0xE00 =
0xE30`** — the address of the 4×4 transform in §5. **The matrix begins exactly where the batch array
stops**, which neither document was looking for.

> **One caution carried over from that reading, and it is not an edge case.** When both slots are
> taken the request is **not refused** — the overflow path reuses slot 1. **And nothing ever frees a
> slot:** `repos-78` searched both ways the array can be reached — two functions take a `lea` to
> `+0x2320`, one write exists at that displacement including indexed forms, and the materialised
> pointer escapes to no callee in either function. **The initialiser writes `0`, the selector writes
> a key, nothing writes it back.**
>
> **So the first two distinct owners take a slot each and every owner from the third onward shares
> slot 1**, every frame, until the record is rebuilt — and the bounding box in §3 is then accumulated
> across all of them. **That is the steady state, not a busy-frame hazard.**

## 6. The vertex, and why there are six of them per glyph

`001E8070`'s loop is **2 × 3**, with the corner index `i + j`: **corners 0,1,2 then 1,2,3** — the
standard two-triangle quad. The record appended is **`0x3C` bytes**, and the append is inline
(`cursor` at `+0x20`, capacity at `+0x28` of the open batch at `param_1 + 0x10`), falling back to
`001E7A20` when the batch is full.

- **`u = x / texture_width`, `v = (texture_height − y) / texture_height`** — V is flipped.
- **Screen X and Y** come from two parallel four-float arrays in the glyph record, `param_2 + 0x1C`
  and `param_2 + 0x2C`; these are the two values the bounding box tracks.
- **Colour channels** are `fontclut_channel × per_corner_value × (1/128) / 255.0`, six of them plus
  the alpha of §4 plus one further scalar.
- **`param_1 + 0x137C` is four per-corner float multipliers reset to `1.0` after every glyph** — two
  `qword` stores of `0x3F8000003F800000` at the tail of the function.

**The palette is `fontclut_%d` and there are 28 of them**: the entry is fetched by
`FUN_001E94E0(param_1, [param_2 + 0x9C] % 0x1C)`, with a fixed entry at `param_1 + 0x1358` when the
index is negative.

## 7. What the displacement census could not see, proven inside this pair

**The offset census behind the pair frontier** (`Tools/work/h78/struct_offset_refs_clean.tsv`)
records 17 sites across this record. **More exist, and two different encodings hide them.**

| field | rows in the census | sites this document cites | what the census cannot see |
|---|---:|---:|---|
| `+0x2324` | 1 — `001E83A3` | 2 | the clear at `001E9122`, written as `[r12 - 0x24]` |
| `+0x233C` | **0** | 2 | **both of them** — `001E8408` and `001E9143` |
| `+0x2348` | 2 — `001E826A`, `001E861C` | 3 | the mode test at `001E8654`, written as `[r12]` |
| `+0x2340` / `+0x2344` | 3, all writes | 5 | the two reads at `001E8F19` / `001E8F0C` |

**Two distinct causes, and only the first is the obvious one.**

**A base pointer.** `001E861C  lea r12, [r14 + 0x2348]`, and every access below it reads
`[r12 - 0x24]` or `[r12]`. The whole of `001E8580`'s traffic on this record is invisible: the census
holds **three** rows for that function's record fields, all from the two instructions above the
`lea`.

**An offset folded into an index computation.** `001E8408` stores to `+0x233C` and the instruction
contains no displacement at all:

```asm
001E83FA  movsxd rax, dword ptr [rbx + 0x20]   ; the record index
001E83FE  add    rax, 0xcd                     ; 0xCD * 0x2C = 0x233C
001E8404  imul   rax, rax, 0x2c
001E8408  movss  dword ptr [rax + rbx*0x1], xmm7
```

**The compiler folded the field offset into the index constant**, and `+0x233C` consequently has
**zero rows in a census of 21,999.** It is not undercounted; it is absent.

**A wide store credited to one field.** `001E73DA  mov word ptr [r14 + 0x2378], cx` writes **two**
bytes. The census holds `001E71B0 / 0x2378 / write` and **no row at all for `+0x2379`** — the same
instruction, the same cycle, one field recorded.

> **The pair frontier found this row because one side still used the long form.** Had both sides
> taken the pointer first, the field would have no rows at all and the join would not exist to find.

**A census over an array reports the element, not the array.** The two records are addressed as
`base + index*0x2C + field`, so **every access to record 1 is recorded at record 0's displacement.**
Measured by `repos-78`: **11 named offsets in `[0x2320, 0x234C)` and none at all in
`[0x234C, 0x2378)`** — not because the second record is unused, but because it **has no distinct
displacement to be named by.**

> **The other modes lose a field. This one loses every element after the first** — and it is the
> mistake one level up from this document's own `+0x2324` error. *"This field has 11 touchers"* is
> right; *"this record is 11 fields"* is not.

**So "no writer found" is not a finding here, and this document does not report one.** `+0x2349`
had **no writer that ARMS it** when this was first published — `001E84D0` clears it and was always
visible. **The arming writer was found forty minutes later** at `001E73CA`, as the high byte of a
`word` store through a register base, and a second one at `001E9920`.

> **An earlier summary of this section said `+0x2349` had "no writer at any displacement", which is
> false** — the clear was in the census the whole time. **The claim that was worth making was the
> narrow one**, and the wide restatement of it was wrong in the direction that flatters the finding.

## 8. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `009018F0` really a table of render-target sizes, or something the loop merely walks? | The string it guards names them: **`"Font Paint Size is Bigger than Biggest Render Target!"`**, and the returned index selects an object at `(i + 0x9E) × 0x20 + base` that is then pushed with `FUN_0018AFF0`. |
| Are there ten rungs, or was the bound read off the wrong side of the increment? | The guard is `if (++i > 9) return 9` — the loop can return **0 through 9**, and the last rung read at `009018F0 + 9*8` is `1920 × 1080`. **Ten.** |
| Are `1920.0` and `1080.0` really a screen size, or a coincidence of two float constants? | `0x44F00000` and `0x44870000` at `001E9128`/`001E9131` are exactly the width and height of **the last rung of the table** — an independent occurrence of the same two numbers in a different form. |
| Is `+0x2338` a separate field or the decompiler splitting one? | Two distinct `movss` at two distinct addresses (`001E83C1` for `+0x2328`, `001E83D2` for `+0x2338`) with **different reset constants** in the flush. Separate. |
| Is `+0x2340` the run's first alpha, or its previous one? | It is written **only** in the branch that clears `+0x2349` (`001E84D0`–`001E8523`), which cannot run twice without something re-arming `+0x2349`. **`001E9920` re-arms it every begin**, so `+0x2340` is the first alpha *of each frame's run*. **An earlier version of this row concluded it was written once ever and never again**, on the strength of having found only the constructor's arm at `001E73CA`; the begin was one caller away. **The strange result was the tell that the search was incomplete, not a finding.** |
| Does the begin's flag settle whether the offscreen path runs? | **No, and conflating the two bytes would be the easy error.** `001E9920` sets the **per-record** `+0x2348`; `+0x2378` is the **outer gate** the flush branches on first, and nothing found here sets it. |
| Does the emitting side's branch really correspond to the flushing side's? | **Same byte, same base, same stride, same index register (`[RBX + 0x20]` in one, the `lea` at `001E861C` in the other).** The *correspondence of meaning* is inference from what each branch does; the *identity of the field* is not. |
| Could the "two records" be a loop bound the decompiler guessed? | `001E915D  cmp ecx, 0x2` / `001E916A  jl 001E8631`, with `001E9159  add r12, 0x2c`. **Two, in the instruction stream.** |
| Is the null return from `001E96A0` really abandoning the loop? | It is a `return`, not a `break`: the second record's flush and its reset are both skipped. **What the consequence is on screen is not established** — only that the reset does not run. |

## 9. What this document does not claim

What `param_1 + 0x2300` is, or what the mode arguments `1` and `3` to `FUN_001FBD80` select. What
the 64 slots at `param_1 + 0x1500` cache, or what the four dwords keying them mean. What the
flag argument `1` versus `0` distinguishes between the two offscreen passes. **Whether anything sets
`+0x2378` at all** — the dedicated setter `001E9F30` has no direct caller, and no route to the
offscreen path was found. **This was first written as "what calls `001E9F30`", which presumes
something does**; after §7's undefined-code finding that presumption is not available. What the third float of each vertex holds — the
decompilation leaves that slot unassigned and it was **not** resolved.

**Three questions that stood here have been closed and moved to §5b**, by a reading of `001E9D20`
this document's author did not perform: what `+0x2320` holds, what sets the record index, and why
the group stride leaves one batch slot unused.

## 10. Why this document exists

**`001E8580` was residual #6 by size and marked unread. `001E8070` was a row in a table, named by a
string, never opened.** The only thing connecting them was a shared displacement with two sites.

**What fell out was the ladder, the inverted box, the duplicated minimum, and a fade that is applied
once instead of per letter** — and a demonstration, inside the pair itself, that the instrument
which found the row **undercounts every field whose address is taken into a register.**

**Both functions are on the residual list** (lines 13 and 14 of `residual_addrs.txt`), so the read
closes two of the 154. **Ledger rows are authored and staged** at
`Tools/work/pending/repos55_text_target_pre.tsv` — `Presentation.Text.
GlyphQuadVertexEmissionAndLineBoundsAccumulation` and `Presentation.Text.
GlyphBatchFlushAndOffscreenTextTargetComposite` — and are **not applied**, because
`Apply-GfzBatch.ps1` requires the project unlocked and it is open to the analysis server. **The
score therefore still reads 154 unresolved** *(answered: see the correction above, 158 → 139, and the-unresolved-158.md: 30 at GN161; 2026-10-02, OPUS)*; that is a staging state, not a claim about the code.

*(Pass 22 adjacency, 2026-09-14: the paint path crosses out through shared helpers — `001E9A20`
is called by **resource** `001B58E0`, `001E8070` calls **audio** `00225690`, and `002134A0` is
called by **actor** `00234480` (3 edges). The paint pass is reached from resource-loading and
actor contexts through shared accessors; adjacency, not ownership.)*

*(Pass 22 live-graph completion, 2026-09-15: the shared `Audio` accessor `00225690` cited
above is itself called by `Platform` bodies `0061F200`/`006209C0`/`0061F710`/`006239C0` (4
edges) — platform code consumes the same accessor family the paint path uses.)*

## The `001E8580` exclusive subtree — the vertex pipeline behind the flush (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns `001E8580` **21 frontier functions** — the helper family the
flush drives. Every member body was disassembled from the shipping image (2026-09-15). Eighteen are
called by the root directly; `00212E30` and `002130C0` sit under `001E96A0`, and `002145A0` under
`00214930`. Two helpers (`001E97B0`, `001E96A0`) are already described in §2 and §5; the roles below
are instruction-level and consistent with those sections.

| cluster | members | role |
|---|---|---|
| rung and slot cache | `001E97B0` (134 B — the ten-rung `009018F0` chooser of §2: compares `+0x2330−+0x2328` and `+0x2334−+0x232C` against each `{w,h}` pair, falls back to rung 9 after the `"Font Paint Size…"` guard `0017D280`), `001E96A0` (210 B — the §5 scan of the **64-slot, stride-`0x38` cache at `+0x1500`**: on a free slot (`+0x20 == 0`) it asks `00212E30` whether the parameters match; on an occupied one it calls the slot's `vtable[+0x18]` then `002130C0`), `00212E30` (53 B — strict equality of four floats `+0x24`–`+0x30` plus dword `+0x18` — the slot's same-parameter test), `002130C0` (31 B — stores the four parameters and clears `+0x20`, marking the slot free-for-reuse) | chooses the render-target rung, then finds-or-arms the per-run slot that owns it |
| object constructors — three sibling classes, one shared layout | `002130E0` (44 B — vtable `00906DC8`, RTTI `01CF0338`; zeroes `+0x08`–`+0x38`), `002138C0` (159 B — vtable `00906EB8`, RTTI `01CF04C0`), `00213960` (158 B — vtable `00906F20`, RTTI `01CF0548`), `00213A00` (159 B — vtable `00906E50`, RTTI `01CF0438`; **one of three classes the root calls** — corrected 2026-09-22 (SWE2-FRONTIER) on FABLE's six-site sweep: the root's text flush `001E8580` calls all three constructors at four sites — `00213A00` twice (`001E86BB`/`001E88C4`, the `0x168` Shadow), `00213960` once (`001E8A7D`, `0x168` ShadowFinal) and `002138C0` once (`001E8F84`, `0x170` Final) — and no site anywhere stamps `00906DE8`, so the plain instance is a base/reset target only) | the three `0x168`-class ctors share a body shape: `memset(+8, 0xF0)`, three `1.0f` vec4s at `+0x11C`/`+0x130`/`+0x144`, `+0x158 = 1.0f`; they differ at the tail — `002138C0` sets byte `+0x168 = 1`, `00213960` zeroes dword `+0x160`, `00213A00` zeroes qword `+0x160` |
| field loads and setters | `002134B0` (111 B — copies **16 dwords** `rdx` → `+0x54`–`+0x90`, the transform block `00213570` consumes), `00213520` (24 B — 4 dwords → `+0x40`–`+0x4C`), `00213550` (5 B — `+0x38 = rdx`), `00214700` (7 B — `+0x168` byte), `002147A0` (7 B — `+0x160` dword), `00214B10` (17 B — `+0x160`/`+0x164` float pair) | plain stores; note `+0x160` is a **float position** for the `00213E30`/`00214B10` class and a **resource index** for the `002147A0`/`002148F0`/`00214930` sibling — same offset, two classes |
| resource binding | `002147B0` (121 B — `+0x108 = 0`, then registry `00189120` → `00186800(edx)` twice: `+0x28` → `+0x110`, `+0x2C` → `+0x114`, and `+0x118 = 0` — binds the atlas dims `00213E30` recentres on), `002148F0` (61 B — same registry lookup keyed on `+0x160`, stores the record's `[rax]` to `+8`, or 0 when the record's `+8` flag is set) | both reach the resource registry through `00189120`/`00186800`; the same `+0x28`/`+0x2C` pair `00214930` reads as texture dims |
| vertex pipeline | `002145A0` (329 B — the shared transform: `{x,y}` through the `+0x11C`/`+0x12C`/`+0x13C` row vectors plus `+0x14C`/`+0x150`/`+0x158` translations, `w`-divide, `001B1620`-gated viewport constants `008C5B5C`/`008C5B48` (x) and `008C5B58`/`008C5B44` (y), NDC→pixel write to both out pointers), `00213570` (764 B — same transform against the `+0x54`–`+0x90` block, then appends a **48-byte vertex** at index `+0x2C` into **both** arrays `+0x18` and `+0x20`, bounded by `+0x28`), `00213E30` (342 B — recentres x/y on `+0x160`/`+0x164` minus half of `+0x110`/`+0x114`, normalizes (y negated ×2), appends the same 48-byte record into per-index array `[rbx*8+0x58]` at count `[rbx*4+0xD0]`, bounded by `[rbx*4+0xA8]`; `r9b` picks white `1,1,1,1` over the copied colour), `00214930` (466 B — the §5 quad emitter: resolves `+0x160`'s record for dims `+0x28`/`+0x2C`, then a four-corner loop writes stride-`0x30` vertices at `[+0x58]+0x24` — UV = corner ÷ dims, position through `002145A0`, colour `1,1,1,1`, and a corner-conditional w term), `00213870` (75 B — allocates two `count×48` vertex buffers through `01F7F4C0`/`001A1470` into `+0x18`/`+0x20`, stores the count at `+0x28`) | the geometry half of the flush: transform, then append — one emitter writes paired buffers, one writes per-index arrays, one emits a textured quad |

Interior citations — one instruction each, verified inside the declared extents:

| body | interior cite | what is there |
|---|---|---|
| `001E96A0` | `001E96F0` | `cmp byte ptr [rbx + 0x20], 0` — the free-slot test in the 64-entry scan |
| `001E97B0` | `001E97E0` | `movd xmm0, [rax-4]; cvtdq2ps` — loading the rung's width for the `comiss` |
| `00212E30` | `00212E56` | `mov eax, [rcx + 0x18]` then compare — the dword half of the match test |
| `002130C0` | `002130DA` | `mov byte ptr [rcx + 0x20], 0` — the slot freed after its params are stored |
| `002130E0` | `002130E7` | `mov [rcx], rax` — vtable `00906DC8` installed |
| `002134B0` | `002134F4` | `mov [rcx + 0x80], eax` — dword 12 of the 16-dword transform copy |
| `00213520` | `0021352B` | `mov eax, [rdx + 8]; mov [rcx + 0x48], eax` — middle of the 4-dword copy |
| `00213550` | `00213550` | `mov [rcx + 0x38], rdx` — the whole body |
| `00213570` | `00213623` | `divss xmm7, xmm9` — the w-divide before the NDC→pixel map |
| `00213870` | `00213883` | `lea edx, [rdx + rdx*2]; shl edx, 4` — `count × 48` computed for the allocation |
| `002138C0` | `0021394D` | `mov byte ptr [rbx + 0x168], 1` — this class's distinguishing tail store |
| `00213960` | `002139ED` | `mov dword ptr [rbx + 0x160], edi` — the sibling class's `+0x160` dword zero |
| `00213A00` | `00213A8D` | `mov qword ptr [rbx + 0x160], rdi` — the root's class, `+0x160` qword zero |
| `00213E30` | `00213F20` | `mov dword ptr [rdx + rcx*8 + 0x10], 0x3f800000` — the white-colour arm of the record write |
| `002145A0` | `00214662` | `divss xmm7, xmm9` — the same w-divide in the shared transform |
| `00214700` | `00214700` | `mov byte ptr [rcx + 0x168], dl` — the whole body |
| `002147A0` | `002147A0` | `mov dword ptr [rcx + 0x160], edx` — the whole body |
| `002147B0` | `002147E9` | `mov [rbx + 0x110], eax` — the first bound dim landing |
| `002148F0` | `00214915` | `mov [rbx + 8], rax` — the resolved record pointer stored |
| `00214930` | `00214A59` | `movss [rbx - 4], xmm0` — the U coordinate after the divide by texture width |
| `00214B10` | `00214B10` | `movss [rcx + 0x160], xmm1` — the position write `00213E30` recentres on |

Read together, the subtree is the flush's draw machinery: pick a rung, find the slot, bind the
atlas, then transform-and-append vertices — which is why `001E8580` reads as a *text* function to
its callers while spending most of its body in geometry.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Script_VM_Native_Bridge — CLIENT, fan-in of 24 edges.** An 85-byte function this page cites is called by small script-bridge bodies (42 to 133 bytes).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — CLIENT.** `MainLoop_UpdateAndRenderFrame`, owned by that layer, calls `001FBD80` on this page. That caller is the frame body: it claims slot `3`, runs a fixed startup chain, and zeroes `[01FD4A74]` before the frame proper begins; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — MIXED (7 edges).** `00796FC0`, owned by that layer, is *called by* `0079A430` — this page's
painter descends into the input layer for its input-state read; and `0079E3D0`/`007A2440` (Input)
call `0079A430`/`0079AF20` — the same painters reached from the input side when the painting runs
under input-driven frames. Consultation both directions, no shared ownership. Read from `edges.tsv`
2026-09-17 (SWE2-FRONTIER).

**Application — CLIENT (1 edge).** `001867B0`, cited on this page as the object-model sibling of
`00186800`, is called by `001A97F0` in that layer — the application side reaches the same indexed
fetch. The crossing is that the layer consults the shared helper, not that this page owns anything
in it. Read from `edges.tsv` 2026-09-19 (SWE2-EC7).


**Platform — CLIENT (SWE2-EC7-156, 12 edges).** `0061F200`/`0061F710`/`006209C0`/`006239C0` call this page's `00225690`; batch-121's `001E6FD0` EASTL helpers share the pattern — platform code consults the glyph helpers, not a shared responsibility.


**Developer — SERVICE (SWE2-EC7-161, 3 edges).** `001C76E0` — the `mClutIndex` parameter
binder this page measured — calls `00200B80`/`00200BE0`, which are also reached from
Developer-layer bodies `001C2F50`/`001C6320` — the binder shares the console's parameter
helpers. Mechanical fan-in.

## The `001E8070` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`001E8070` — the glyph emitter this page maps — additionally shows:
`dword[rdx+0x9C]` element count read (`001E808A`), magic-divide
`0x92492493` (÷7, `001E809B`), `001E94E0` element resolve → `r15`
(`001E80B8`), float constant `008C5B34` (`001E80CD`), counter seed
`0x4DF` (`001E80FA`), `00225690` on `qword[rbx]` (`001E815E`).

| member | role | interior |
| --- | --- | --- |
| `001E7A20` (610 B) | `0x38`-stride vector insert — `r9=[rcx+8]` end check vs `[rcx+0x10]` (`001E7A35`), `rbx` bounds vs `rdx`/`r9` (`001E7A3F`/`001E7A44`), element moves `dword[r9-4]` → `[r9+0x38]` (`001E7A7B`/`001E7A7F`) | [`001E7A7B`](../../_index/ADDRESS-INDEX.md) |
| `0079E3C0` (4 B) | dword getter — `eax = dword[rcx+0x28]; ret` | [`0079E3C0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001E94E0`, `00225690`. The
`0079E3D0` body (`0079A430`/`0079AF20` calls) is a sibling, not a
member.

## SWE2-EC7-40 update (2026-09-19) - `0079AF20`

`0079AF20` (389 B) is a glyph-painter body - `01F401E8`, five vcalls only. Interior anchor `0079AF86` (the first vcall).

## SWE2-EC7-43 update (2026-09-19) - `0079A430`

`0079A430` (285 B) is a glyph-painter body - `00796FC0` single call (the input-layer callee the page names). Interior anchor `0079A43D` (the `00796FC0` call).

## SWE2-EC7-61 update (2026-09-19) - `001E94E0`

`001E94E0` (153 B) is the `001E94E0(painter, index)` body the painter page names - `0019C5D0`/`001C5F20`/`00808C40` plus `00901978`/`01F44830` and the `"fontclut_%d"` literal. Interior anchor `001E9533` (a `0019C5D0` call).


## SWE2-EC7-69 update (2026-09-19) - `00186800` registry indexed fetch measured

`00186800` (24 B) measured - **the page's registry-fetch claim is exact**:
`edx < 0xA` indexes `qword[rcx + rdx*8 + 0xB90]`; `edx >= 0xA` returns the
`[+0xBD8]` default slot. Call-free; the same `+0xB90`-table/`+0xBD8`-default
shape as `001867B0` on the object-model side.
Interior anchor `00186807` (the `rcx + rax*8 + 0xB90` indexed load).

## SWE2-EC7-102 update (2026-09-20) - `002B2970` measured

`002B2970` (728 B) is the measure-with-scratch-swap
`002AC5F0`, `002B27E0`, `002B2880` and `002B28B0`
call: `rbx`'s `0xD0` text record is copied to
`rbp+0x50`, `0209CC40`'s `+0x10C8`/`+0x10D8`/`+0x10E8`/
`+0x10FF`/`+0x10FC` fields and `0209CC48` are saved,
a small `{3, ...}` record is installed at `+0x10C8`
with the fields zeroed, and `002B2150` runs. When the
`comiss` zero-check fails, `0039C4A0` keyed on
`(dword[rbx+0x44] >> 0xB) & 1` fetches a record whose
`[rax] >> 9 & 0x1F` becomes the float stored to
`+0x10E8`; the record is then copied to `rbp-0x80`
and `002AF340` measures it into `rsp+0x70`/`+0x74`,
which land in the `rsi`/`r14` out-pairs before every
swapped field is restored - the canonical
`0xD0`-record extent query the paint arms run.
Interior anchor `002B2BBE` (the `002AF340`
call).

## SWE2-EC7-110 update (2026-09-20) - `001C5F20` measured

`001C5F20` (718 B) is the
FontCluts JSON loader
`001E94E0` and `001E98A0`
run. The `01DF6E48` byte must
be set (or `01F81282` already
armed) before `00200BE0(
01F81378)` takes the JSON
cache lock; a failed lock
jumps straight to the
`001C76E0` tail. Inside, two
EASTL strings build through
`001EDF00` allocators and the
`008C2A40` memcpy IAT:
`"JsonData/FontCluts/"` (0x13
bytes, `008F9EA8`) prefixes a
strlen-scanned copy of the
`r14` name, and `001B31E0`
appends `".json"` before
`001A52A0` concatenates into
the path buffer. Both strings
free through `vtable[+0x18]`
in reverse order, `00200BF0`
releases `01F81378`, and the
`001C76E0` tail runs
unconditionally.
Interior anchor `001C5FA6`
(the `"JsonData/FontCluts/"`
prefix load).

## SWE2-EC7-114 update (2026-09-21) - `007A3150` / `007A0410` measured

`007A3150` (162 B) is the
probe loop `007A2440` runs
over `0x12` objects at
`+0x88 + i*8`: each live
object first takes up to 4
rounds of `0079D320(this,
index, i)` against `xmm0 ==
0.0`, then up to `0x11`
rounds of its
`vtable[+0x18]` with
`edx = j + 0xB`; the first
object passing either test
gets `vtable[+0x30]`
invoked and the result
parked at `dword[+0x10]` -
a two-stage eligibility
scan over a fixed 18-slot
table.
Interior anchor `007A31A9`
(the `+0x18` probe call).

`007A0410` (220 B) is the
cursor-centre step
`007A2440` runs: IAT
`008C28D0` on `02EA5248`
fills a rect, the midpoints
`esi`/`edi` are computed,
four `008C29B0` reads at
`0x4C..0x4F` return bounds,
and only when they bracket
the centre does
`008C28B8(esi, edi)` run
with `dword[+0x178]`/
`[+0x17C]` latching the
position - a bounds-checked
centre write.
Interior anchor `007A04B4`
(the `008C28B8` call).

## SWE2-EC7-115 update (2026-09-21) - `0079D320` / `0079D1D0` / `0079C6C0` measured

`0079D320` (271 B) is the
float probe `007A3150`
calls per `+0x88`-table
entry: `r11` = object i,
its `+0x58`/`+0x60`/`+0x68`/
`+0x70` members load, and a
four-way `edx` dispatch
compares `|member.+0x28|`
against `member.+0x24`
(cvtps2pd + `abs` mask
`01CEBD80` + cvtpd2ps) to
pick a neighbour's `+0x24`
into `xmm1`; then
`xmm3 = [r11+rbx*8+0x58]
.+0x28` and the return is
`xmm3` when `xmm1 > |xmm3|`,
else 0 - a directional
threshold pick per control
index.
Interior anchor `0079D373`
(the `edx == 3` float load).

`0079D1D0` (327 B) is the
aggregate variant `00197160`
calls: the same four-member
threshold reads, but it
walks all `0x12` `+0x88`
entries accumulating into
`xmm3` and early-exits on
the first nonzero pick -
the scan `007A3150`'s
per-entry call mirrors.
Interior anchor `0079D23B`
(the `edx == 3` load).

`0079C6C0` (105 B) is the
vtable variant over the same
`+0x88` table: for each live
entry, `edx` in `{0x11,
0x12}` routes to
`vtable[+0x20]` and the
`ucomiss` on its float
result decides - the
first nonzero answer wins.
Interior anchor `0079C6FD`
(the `vtable[+0x20]` call).

`001E6FD0` (467 B) is the render-list builder `001E71B0` calls: `001EDF00` name-tags an `EASTL vector` at `rcx` and an `EASTL set` on the stack, zeroes the qword triples, then `00199DB0`/`001E7D30`/`005CC8A0`/`005CD0A0` grow and fill under a `0xFFFFFFFFFFFFFFFE` scope-guard - the glyph pass's container setup.

Interior anchor `001E7018` (function `001E6FD0`).

`001C76E0` (357 B) is the parameter binder `001C5F20` calls: `001FF740("mClutIndex", 01F81378)` + `00200BE0` gate the pass, then repeated `001FF740`/`00200B80` pairs bind each parameter through `001B5FA0`/`001E94E0` - the glyph pass's shader-constant sweep.

Interior anchor `001C76F2` (function `001C76E0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Save_Load_Settings — MECHANICAL, 2 edges.** `0017D280` is called by `GameSettingConfig_ParseText` (`001DE5D0`), `GameSettingConfig_ParseOneSettingValue` (`001DF350`).

**UI — MECHANICAL, 38 edges.** `0017F850` is called by `002AC5F0`, `002AF960`, `002D28E0`; `0017FA10` is called by `002AC5F0`, `002AF960`, `002D28E0`; `002B2150` is called by `002AC5F0`, `002AF340`, `002AF960`; `002D28E0` calls `002435C0`, `00243860`, `00243C00`; `002A9F00` is called by `002AC5F0`, `002AE610`; `002AC5F0` calls `002AE610`, `002B2150`; `002AC5F0` is called by `002AF340`, `002B2150`; `002AF340` calls `002AC5F0`, `002B2150`; `002AF960` is called by `002A4430`, `002A4830`; `002B0280` calls `002AE610`, `002B2150`; `002B0280` is called by `00243860`, `002A86A0`; `002B2970` calls `002AF340`, `002B2150`; `0039C4A0` is called by `002AC5F0`, `002AE610`; `001867B0` is called by `0018EEE0`; `001A1470` is called by `0018EEE0`; `002A9F00` calls `002AC5F0`; `002AF340` is called by `002ABB20`; `002AF960` calls `002B2150`; `002B2150` calls `002AC5F0`; `002B2880` is called by `002A4830`; `002B2970` is called by `002AC5F0`.

**WorldAreaField — MECHANICAL, 1 edge.** `0017D280` is called by `World_UpdateSimulationTick` (`00314020`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
