---
system: The nine-patch box renderer that is never called   # <- corrected 2026-10-02, OPUS: it is reached through 00392A00+0x5 (REFUTED box)
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Presentation.UI
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0020AC30, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  residual_sha256: c5d4b7f7fb1ffbf0c3f54c671bb0af02b0513901af634c5ca755333ce3d338ff
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
---

# The nine-patch box renderer (`00392A10`) that is never called

> # ⚠ REFUTED 2026-09-16 (FABLE) — the falsifier this page named has occurred, on route 2
>
> **`00392A10` is reachable by a static route.** This page's *"What would falsify this"* says: *any
> of the five returning a hit*. Route 2 returns one once its enumeration is completed.
>
> **Route 2 decoded "every `E8`/`E9` in `.text`". The branch into this function is neither.**
>
> ```
> 00392A00  66 83 79 58 00     cmp word ptr [rcx + 0x58], 0
> 00392A05  0f 85 05 00 00 00  jne 00392A10
> 00392A0B  c3                 ret
> ```
>
> `00392A00` is a **listed twelve-byte function**, separated from `00392A10` by `int3` padding, and
> `00392A10` opens with a full prologue — so this is a genuine **cross-function conditional tail
> jump**, the shape MSVC emits for *"if the record is empty, return; otherwise run the body"*. It is
> a relative branch into the function, and it belongs to route 2's class; only the **encoding**
> `0F 8x rel32` was outside the enumeration.
>
> **And the guard is called four times, by ordinary `E8` calls:**
>
> | call site | inside | owner |
> |---|---|---|
> | `002A62EE` | `002A6190` (2,043 B) | — |
> | `002C0967` | `002C0870` (716 B) | **UI** |
> | `002C0E5E` | `002C0BE0` (752 B) | **UI** |
> | `00574056` | `00573F40` (317 B) | — |
>
> **So the island is not dead.** `00392A10` runs whenever one of those four passes a record whose
> `word +0x58` is non-zero — and with it `002DC7F0`, `00392CE0`, `002DD1E0` and `002DD090`, which
> this page shows are reachable only through it. **The title of this file is wrong**, and it is left
> in place rather than renamed so that anyone who has cited it finds this box.
>
> ## What this page got right, and it is most of it
>
> **Routes 3, 4 and 5 stand and are untouched.** The address is not materialised by a `LEA`, is not
> stored anywhere in the file, and no `FF 25` thunk can reach it — all true, all measured with
> controls, and **all irrelevant to a relative branch**, which needs no materialised address. The
> `.pdata`/RVA correction stands. The note that routes 4 and 5 are not independent stands.
>
> **And the insistence on controls is why this was findable.** Every scan here proves it can find
> what it looks for, so the gap could not be in the execution — it had to be in the *enumeration*,
> which is where it was. A page whose scans had no controls would have left the question
> unanswerable rather than merely open.
>
> ## The general form, measured
>
> A **conditional near jump is a relative-branch encoding that reachability censuses in this database
> do not sweep.** Corpus-wide, against the 38,161 entries in the function list, swept over raw
> `.text` without function boundaries: **16,908** entries are targeted by `E8`, **4,632** by `E9`,
> and **115** by `0F 8x` — of which **42 are targeted by no `E8` and no `E9` at all**, holding
> **23,944 bytes**.
>
> *(The `E9` and `0F 8x` figures were **4,848** and **118** when first published; corrected
> 2026-09-16 (FABLE). Sweeping raw `.text` without function boundaries is what the sentence
> above says it does, and that sweep necessarily decodes the **data and padding between
> functions** as though they were instructions, inventing branches that are not code. The
> re-measurement decodes each of the **38,161 listed bodies from its own entry address**,
> which cannot stray outside a body. **The load-bearing figures do not move at all** —
> 16,908 call targets, **42** orphans and **23,944** bytes are identical under both methods,
> and both controls — the `EE-12` handler named below and this renderer — are still in the orphan set.
> So the fourth-route argument is unaffected; only two context counts were inflated, by 216
> and 3.)* This renderer is one of the 42. So are
> `SaveloadManager_ParseDisableAutosaveList` (2,028 B) and `BattleUnit_HandleActionTimelineEvent`
> (1,215 B), the latter being the `EE-12` handler refuted the same day by the same omission.
>
> *Controls for that measurement:* the three `EE-12` handlers all land in the 42, which is what
> validated it.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

*Added 2026-09-16 (FABLE) in the same edit as the refutation above, because naming the four callers
is what pulled these in. Each far end is characterised without naming its own callees, per the
2026-09-16 refinement of the crossing rule.*

**ActorEntity — SERVICE.** `002C0870`, one of the four callers named above, calls a **32-byte**
ActorEntity body. What it reaches resolves a packed actor handle and then asks one question of the
result: it returns `1` exactly when a class nibble equals **5**, and `0` otherwise. A one-bit
predicate, nothing more.

**Audio — SERVICE.** `002A6190`, another of the four, calls a **51-byte** Audio body. It is a guarded
forward: it returns immediately when the dword at `02091098` is non-zero, otherwise resolves an id
and gives up on `-1`, and only then forwards with a literal `0x40` and `0x7F`.

**CoreRuntimeScheduling — SERVICE.** `002A6190` also calls a **40-byte** scheduling body, and that
one has no callees at all. It reads two globals — `01F82E38` and `01DFE0C0` — and returns a
**boolean**: `1` when both are set, the complement of the second when the first is set and the second
is not, and `0` when the first is clear.

**In all three the crossing is that a caller of the nine-patch guard consults another layer's
helper, not that this page owns anything in those layers.** None of them is on the path into
`00392A10`; they are the ordinary business of functions that happen also to call `00392A00`.


> `00392A10` is the only function in `FFXII_TZA.exe` that a repaired reference census can find
> **no route to at all**. It is the root of a five-function, 4,090-byte island that draws a
> resizable bordered box with a colour gradient — complete, coherent, and dead.

---

## 1. What the player sees

**Nothing. That is the finding, and for once it is a fact about the game rather than about our
tools.**

Every menu panel, dialogue frame and gauge surround in FFXII is a box that has to work at any size:
the corners must stay crisp while the edges and the middle stretch to fit. The standard way to do
that is to cut the box art into nine pieces — four corners, four edges, one centre — and stretch
only the middle row and middle column. This code does exactly that, and tints each of the nine
pieces by blending four colours set at the box's corners, so the finished panel carries a smooth
gradient rather than a flat fill.

**~~It is never invoked.~~** *(answered: see the REFUTED box at the top — `00392A00` is `cmp word [rcx+0x58], 0` then `jne 00392A10` at `00392A00`+0x5, and `00392A00` has four callers; 2026-10-02, OPUS)* ~~Nothing in the shipping executable calls it,~~ mentions its address, or
stores a pointer to it. Whatever menu style it was written for, the game you can buy does not use
it — the boxes you actually see are drawn by a different, simpler routine that this code was
evidently meant to replace.

So the honest player-facing statement is: **this is a finished feature that did not ship.** A
modder cannot change how FFXII's windows look by editing it, because the game never runs it — but
it is the clearest surviving description of how the engine's authors intended resizable panels to
be drawn, and it is a working implementation of an effect the shipping code does not have.

### Why this one function mattered enough to read

The residual — the functions carrying no classification — was described by this category as code
whose evidence had run out. A [repaired reference census](../Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
found that **156 of the 158 have an admissible incoming reference after all**, and that the barrier
had been the census rather than the evidence. Two functions survived that repair with nothing.

**The other of the two, `0020AC30`, has since proved reachable** — through a five-byte `JMP` thunk
that a call-graph census cannot see, documented in
[cutscene name slots](../Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md).
The corrected figure is **~~1 of 158, not 2~~ 0 of 158** *(answered: see the REFUTED box above; 2026-10-02, OPUS)*, and ~~`00392A10` is that one:~~ no caller, no code
reference, no data slot, no string, and no thunk. It is the single place in the binary where "we
cannot explain this" was still a statement about the binary.

It is explained now, and the answer is that nothing calls it.

---

## 2. Native mechanism

### The island

```
00392A10   707 B   nine-patch box renderer          <- NOTHING reaches this   <- corrected 2026-10-02, OPUS: reached by jne from 00392A00+0x5, whose four callers are live (REFUTED box)
   |
   +-> 002DD1E0   268 B   open the batch             sole caller: 00392A10
   +-> 002DC7F0  2194 B   draw one cell              sole caller: 00392A10
   +-> 00392CE0   589 B   single-quad fallback       sole caller: 00392A10
   |      \-> 002DC290  1363 B  the LIVE cell drawer  (11 other callers - not dead)   <- corrected 2026-10-02, OPUS: 10 other callers (11 functions, 17 rel32 sites, with 00392CE0)
   +-> 002DD090   332 B   close the batch            sole caller: 00392A10
   +-> 002DD4B0     7 B   a static global getter     (10 other callers - not dead)   <- corrected 2026-10-02, OPUS: 9 other callers (10 functions with 00392A10)
```

**Four functions are reachable only through `00392A10`.** If it is dead they are dead, and that is
**4,090 bytes** of unreachable code — 3,490 of it unclassified and inside the residual.

Two callees are *not* dead: `002DC290`, the cell drawer the rest of the engine actually uses, and
`002DD4B0`, a shared getter. The dead code calls live code; nothing live calls the dead code.

### The geometry

The second argument is a `short *` describing the box, and the routine derives a 3×3 grid from it:

```c
left   = rect[4];                         // fixed left column
right  = rect[5];                         // fixed right column
middle = rect[2] - right - left;          // stretched centre column = width - left - right

top    = rect[6];                         // fixed top row
bottom = rect[7];                         // fixed bottom row
centre = rect[3] - bottom - top;          // stretched centre row = height - top - bottom
```

`rect[0]`/`rect[1]` are the origin and `rect[2]`/`rect[3]` the overall size. **That is the
nine-patch contract exactly**: four fixed corner extents, everything else derived, so the corners
never scale.

Each of the three rows is drawn only if its height is non-zero, and within a row each of the three
columns only if its width is non-zero — so a box with no top border simply omits that row rather
than drawing a zero-height cell.

### The colour gradient

The third argument is four 32-bit colours — the four corners of the box. They are masked to 24 bits
and expanded into a sixteen-entry grid:

```c
c[0]  = colour[0] & 0xFFFFFF;   c[1]  = c[0];   c[4]  = c[0];   // top-left    corner region
c[2]  = colour[1] & 0xFFFFFF;   c[3]  = c[2];   c[7]  = c[2];   // top-right   corner region
c[8]  = colour[2] & 0xFFFFFF;   c[12] = c[8];   c[13] = c[8];   // bottom-left corner region
c[11] = colour[3] & 0xFFFFFF;   c[14] = c[11];  c[15] = c[11];  // bottom-right corner region
```

Each cell then takes four entries out of that grid at its own row/column offset, so **every cell
receives its own four vertex colours** and the nine cells together form one continuous bilinear
gradient across the whole box. The masking to `0xFFFFFF` drops the top byte; the alpha byte is
consumed separately by the fallback path (§ below).

The cell drawer blends them where a corner needs a single colour, by successive halving:

```c
blended = (a + (b + (c + (d >> 24) >> 1) >> 1) >> 1);   // per channel   <- corrected 2026-10-02, OPUS: blended = (((c0 + c1) >> 1) + c2 >> 1) + c3 >> 1 per byte, no >> 24 term (002DC7F0+0x253..+0x305; UQ-353 replay below)
```

### The two paths

```c
if (FUN_002dd4b0() == 0)
        FUN_00392ce0(ctx, rect, colours);      // ONE gradient quad, no slicing   <- corrected 2026-10-02, OPUS: nine slices - a 3 x 3 loop (00392CE0+0x1B6, +0x1C6) calling 002DC290 per non-empty cell (+0x193)
else {
        FUN_002dd1e0(batch, ctx);              // open
        ... nine cells via FUN_002dc7f0 ...
        FUN_002dd090(batch, ctx);              // close
}
```

`002DD4B0` is a 7-byte static global getter with ~~ten callers elsewhere~~ nine callers elsewhere *(corrected 2026-10-02, OPUS: ten functions call it, `00392A10` included)*, so it is a **mode flag read
from a global**, not a computed decision. The fallback `00392CE0` ~~builds a single quad — four~~
~~corner positions and the same four colours, arranged 2×2 — and hands it~~ walks the nine cells in a 3 × 3 loop and hands each non-empty one *(corrected 2026-10-02, OPUS: loop bounds at `00392CE0`+0x1B6 and +0x1C6, the `002DC290` call at +0x193, cells (0,0) and (2,2) special-cased at +0x1F7; the nine-patch window frame page's reading)* to `002DC290`, the live
cell drawer. **So the dead code's own fallback path routes into live code**, which is why the
fallback looks ordinary while the nine-slice path does not.

### The per-cell flag

Each cell passes a flag of `0`, `4` or `8` as the eighth argument:

```c
// top row:     4 for the first cell, else 0
// middle row:  always 0
// bottom row:  4 when the cell index is 2, else 0
//              except: when the cell is not the middle column and both the cell width and the
//              row height are within 8..47, the flag becomes 8 (0 for cell index 1)
```

The cell drawer branches on `flags & 4` and `flags & 8`, and the `& 8` branch is the one that
performs the four-colour blend above. Written out, the exact gate is:

```c
if (col != 1 && (cellWidth - 8) <= 0x27 && (rowHeight - 8) <= 0x27)
        flag = (colIndex == 1) ? 0 : 8;
else
        flag = (colIndex == 2) ? 4 : 0;
```

`(x - 8) <= 0x27` unsigned is the range **8 to 47 inclusive** — a size band, so small corner cells
are drawn differently from large ones.

---

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00392A10` | `UiBox_DrawNinePatchGradient` | 707 B | **classified GN161** `Presentation.Primitive.NinePatchWindowDispatch`. The root. Derives the 3×3 grid, expands the corner colours, draws nine cells |
| `002DC7F0` | `UiBox_DrawGradientCell` | 2194 B | **classified GN161** `Presentation.Primitive.SplittingPatchQuadEmit`. One cell: four vertex colours, corner blend, size-banded styling |
| `00392CE0` | `UiBox_DrawSingleQuadFallback` | 589 B | **classified GN161** `Presentation.Primitive.NinePatchWindowFallback`. The un-sliced path: ~~one gradient quad~~ nine `002DC290` slices *(corrected 2026-10-02, OPUS: `00392CE0`+0x193 inside the 3 × 3 loop)* |
| `002DD1E0` | — | 268 B | Opens the draw batch. Sole caller `00392A10` |
| `002DD090` | — | 332 B | Closes the draw batch. Sole caller `00392A10` |
| `002DC290` | — | 1363 B | The **live** cell drawer, ~~11 other callers~~ 10 other callers, 11 in all with `00392CE0` *(corrected 2026-10-02, OPUS: rel32 sweep: 17 sites in 11 functions)* — not dead |
| `002DD4B0` | — | 7 B | Static global getter selecting the two paths, ~~10 other callers~~ 9 other callers *(corrected 2026-10-02, OPUS: 10 rel32 sites in 10 functions, `00392A10`+0xD4 among them)* — not dead |
| `002D6990` | `ThreeByThreeAtlasPatchGeometryBuild` | 783 B | A **different, live** 3×3 system — see §5 |

Addresses are Ghidra image base `0x00120000`.

---

## 4. Data structures and formulas

```
BoxRect  (short *, the second argument)
  +0x00  s16  originX
  +0x02  s16  originY
  +0x04  s16  totalWidth
  +0x06  s16  totalHeight
  +0x08  s16  leftColumnWidth      fixed, never stretched
  +0x0A  s16  rightColumnWidth     fixed, never stretched
  +0x0C  s16  topRowHeight         fixed, never stretched
  +0x0E  s16  bottomRowHeight      fixed, never stretched

CornerColours  (uint *, the third argument) - four 32-bit colours
  +0x00  u32  topLeft       byte 3 is alpha, read separately by the fallback
  +0x04  u32  topRight
  +0x08  u32  bottomLeft
  +0x0C  u32  bottomRight
```

**The grid derivation, in full:**

```c
colWidth[0] = rect->leftColumnWidth;
colWidth[2] = rect->rightColumnWidth;
colWidth[1] = rect->totalWidth  - colWidth[2] - colWidth[0];

rowHeight[0] = rect->topRowHeight;
rowHeight[2] = rect->bottomRowHeight;
rowHeight[1] = rect->totalHeight - rowHeight[2] - rowHeight[0];

// cells are emitted row by row; x resets to rect->originX at the start of each row
y = rect->originY;
for (row = 0; row < 3; row++) {
    if (rowHeight[row] == 0) continue;          // an absent row is skipped entirely
    x = rect->originX;
    for (col = 0; col < 3; col++) {
        if (colWidth[col] == 0) continue;
        drawCell(x, y, colWidth[col], rowHeight[row], fourColoursFor(row, col), flag);
        x += colWidth[col];
    }
    y += rowHeight[row];
}
```

**The corner-colour expansion** (the sixteen-entry grid the cells index into):

```c
g[0] = g[1] = g[4]  = colour[0] & 0xFFFFFF;     // top-left
g[2] = g[3] = g[7]  = colour[1] & 0xFFFFFF;     // top-right
g[8] = g[12] = g[13] = colour[2] & 0xFFFFFF;    // bottom-left
g[11] = g[14] = g[15] = colour[3] & 0xFFFFFF;   // bottom-right
```

Row 0 cells read `g[i]`, `g[i+4]`, `g[i+1]`, `g[i+5]`; row 1 cells read the same window shifted by
four; row 2 by eight. The stride is what makes the four corner colours interpolate across the box.

**The per-channel corner blend** in the cell drawer:

```c
blended_channel = (a + (b + (c + (d >> 24) >> 1) >> 1) >> 1);   <- corrected 2026-10-02, OPUS: (((c0 + c1) >> 1) + c2 >> 1) + c3 >> 1 per byte, weights 1/8, 1/8, 1/4, 1/2 (002DC7F0+0x253..+0x305)
```

---

## 5. Call chain

```
   (nothing)
      |
      v
   00392A10   nine-patch box renderer
      |
      +-> 002DD4B0   read the mode flag            [LIVE, shared]
      |
      +-- flag == 0 --> 00392CE0  single quad
      |                    \-> 002DC290            [LIVE, 11 callers]
      |
      \-- flag != 0 --> 002DD1E0  open batch
                        002DC7F0  draw cell  x9
                        002DD090  close batch
```

**~~Upstream: none.~~** *(answered: see the REFUTED box — `00392A00` is `cmp word [rcx+0x58], 0` then `jne 00392A10` at `00392A00`+0x5, and `00392A00` has four callers; 2026-10-02, OPUS)* ~~Established in §8 by four independent routes.~~

**Downstream:** the fallback path reaches live drawing code; the nine-slice path reaches only its
own cell drawer.

**Do not confuse with `002D6990`, `ThreeByThreeAtlasPatchGeometryBuild`.** That is a *different*
3×3 mechanism, it is **live** (two callers), it carries a recovered Presentation CodeDomain, and it
calls an entirely separate set of helpers (`002DA7C0`, `002DAC70`, `002DAF30`). The engine
therefore has a working 3×3 patch system **and** this dead one. They share an idea and no code.
Nothing here suggests one replaced the other; that is unestablished.

**Do not confuse with the live box drawing path.** `002DC290` draws the boxes the game actually
shows and is reached from eleven callers that have nothing to do with this island.

---

## 6. Modding notes

- **~~Do not patch this expecting a visual change.~~** ~~It is unreachable; edits have no effect.~~ *(answered: see the REFUTED box — it is reachable through `00392A00`; 2026-10-02, OPUS)* This is
  the practical consequence of §8 and the first thing to know about the file.
- **It is, however, a working implementation.** To *use* it, a mod would have to call `00392A10`
  itself with a `BoxRect` and four colours. Every callee it needs is present and intact, and its
  fallback path already routes into live code, so the risk is in the nine-slice path only.
- **`002DD4B0` is a shared global getter with ten other callers.** It is not private to this
  system, so forcing its value to steer the two paths here would affect ten unrelated call sites.
  Pass through `00392A10` instead.
- **Breaks if:** a `BoxRect` gives a `totalWidth` smaller than `left + right`, or a `totalHeight`
  smaller than `top + bottom`. The middle extent is computed by subtraction with **no clamp**, so
  it goes negative and the row/column loop draws with a negative size rather than skipping.
- **Multiplayer / XIIOnline:** irrelevant. Local presentation, never authoritative state, and dead
  besides.

---

## 7. What is not known

- [x] ~~**UQ-351.** **Why it is dead.** Cut feature, a variant for a platform or build configuration that was not
      shipped, or replaced by `002D6990` — nothing here distinguishes them. **PROPOSED-repos9e-14.**~~
      **PREMISE REFUTED 2026-09-16 (FABLE) — by the box at the top of this page, which I added without
      reconciling this section. It is not dead**, so *why is it dead* has no answer to find. The guard
      `00392A00` reaches this body by a conditional near jump and is itself called four times.
      **What survives, and it is a better question:** the guard tests `word [rcx+0x58]` and falls
      through when it is zero, so **what makes that word non-zero is what decides whether this renderer
      ever runs** — and that is unread. *Restated rather than closed:* the row is still open, on that.
      *(~~`UQ-355` keeps its own framing: whether `002D6990` superseded this is still a fair question
      between two live paths, and no longer rests on this one being dead.~~ Superseded later the same day by the
      answer to `UQ-355` below - reconciled 2026-09-19, FABLE.)*
      **`UQ-351` ANSWERED 2026-09-25 (OPUS).**
      **The word is the widget's composed opacity, so this renderer runs for every nine-patch widget that is not fully transparent.**
      - **What the four callers pass.** `rcx` is always `[widget+0x38]`: `002A62DF`; `002C0916` -> `002C0964`; `002C0D5A` -> `002C0E5B`, on message 3's arm `002C0D53`; and `00573F6D`.
      - **That qword is the node's live draw record.** The widget-tree pass `00245E60` stores the address of a 0xA0-byte stack record at `00245EB0` and zeroes the field again at `002463BE`.
      - **The record starts transparent.** `002D8C00` zero-fills the record, then sets `+0x5A` (the RGB scale) to 0x80. So `+0x58`, the alpha scale (the fourth channel of [the rectangle tint](../drawing-one-coloured-rectangle.md)), starts at **0**.
      - **The pass then sets the alpha.**
        - For a root, `+0x58` becomes the node's byte `+0xA0` (`00245EF0`).
        - For a child, it becomes `(parent +0x58 * +0xA0) >> 7`: `00246480` puts `+0xA0` at out `+0x24` (`002464F5`), and `00245F81`-`00245F9C` does the multiply.
        - `+0x5A` composes the same way from `+0xA1` (`00245F38`-`00245F49`).
      - **So it is non-zero by default.** The constructor `002465F0` sets `+0xA0 = 0x80` (1.0) at `0024670A`. Within the pass, the word becomes 0 in two ways:
        - the node or an ancestor has opacity 0;
        - a message-3 handler scales it to 0. Two are read here: `002C0BE0` scales by `+0xEA` when `+0xEC` bit 1 is set, and `002C0B40` scales by `+0xDA`. The other message-3 handlers (28 in [the protocol census](../../16-UI/Widget-Object-Model/the-widget-message-protocol.md)) are not read.
      - **Evidence: STATIC + NATIVE-REPLAY** in [uq351-opus-replay-widget-alpha-guard](../../_index/candidates/uq351-opus-replay-widget-alpha-guard/):
        - the record builder, run over a poisoned buffer;
        - the guard, run both ways;
        - the draw pass, run over a two-node tree on a seven-case grid.
      - **Not read here:** which widgets animate `+0xA0` to 0 at run time.
- [x] ~~**UQ-352.** **What `002DD4B0`'s global is**, and what its ten other callers use it for. Reading it would
      say what the two paths were meant to be selected *by*. **PROPOSED-repos9e-15.**~~ **Answered 2026-09-14 (FABLE):** `002DD4B0` is a 7-byte getter, `mov eax, [0215E6D0]` / `ret`, and `0215E6D0` is **the draw-bracket-open flag** answered under UQ-348: set to 1 only when the bracket-open command `0x10000000` has been submitted, and cleared by the close `0x11000000` ([the cutscene-slot page](../Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md), UQ-348). All ten raw call sites were read at the call:
      - **Eight use it as a gate.**
        - Seven skip their drawing body when the flag is 0 (`test eax, eax` / `je`): `00242CBE`, `00245193`, `002455CD`, `0029E872`, `0029EDB6`, `002D068F` and `003C4198`.
        - `00392AE4` picks the sliced renderer when the flag is set, and the simple one otherwise.
      - **Two turn it into a command word.** At `00248E4E` and `0024A136`, `neg` / `sbb` makes the header dword `+8` equal to `0x11000000` when the bracket is open and 0 when it is not, beside a `0x50000000 | length` word at `+0xC`.
      So the two paths are selected by whether a draw bracket is open, the same question the rest of the UI draw code asks.
- [x] **UQ-353.** **The exact vertex format `002DC7F0` emits.** The body was read for its colour and flag
      handling, not its output records; 2,194 bytes remain only partly read. **PROPOSED-repos9e-16.**
      **UQ-353 ANSWERED 2026-09-26 (OPUS, NATIVE-REPLAY, 5/5).** It emits 0x30-byte `ImmediateVertex` records as
      triangle strips through `00181460(vertices, n)`:
      - `+0x00` x, y, z, w floats: `(v*M).xy / w` for the row vector `(x, y, 0, 1)`, with z 0 and w 1.0;
      - `+0x10` four int32 channels, the colour's bytes 0-3 (`0x80` = 1.0 at flush);
      - `+0x20` u, v in texels (0 here);
      - `+0x28` the flags word, which the per-vertex conversion never reads.
      - The plain quad is one strip TL, BL, TR, BR. The corner-blend path (bit 3) draws two strips around the cell
        centre, whose colour is `(((c0+c1)/2 + c2)/2 + c3)/2`: weighted toward corner 3, not an average.
      - See [`uq353-opus-replay-box-cell-vertex-format/`](../../_index/candidates/uq353-opus-replay-box-cell-vertex-format/).
- [x] **UQ-354.** **Whether the size band 8..47 corresponds to an art asset's corner dimensions.** The gate is
      exact; what makes 8 and 47 the right numbers is not established.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): no. This renderer draws no art, so there is no asset whose corners
      the band could match.**
      - The batch opener `002DD1E0`, which the root calls on the nine-slice path, writes the batch's one GIF tag at
        `002DD294`. It has PRIM `0x4C`: a gouraud, alpha-blended triangle strip with **TME 0**, meaning no texture.
      - Its register list at `002DD2B2` is `0x41414141`, RGBAQ and XYZF2 only, with no ST or UV. The cells carry
        colour and position.
      - The cell drawer `002DC7F0` has no tag of its own, so every cell is drawn under that primitive.
      - The same decoder finds textured tags elsewhere in the UI code, so the flag is visible when it is set.
      - So the band selects the four-colour blend for small corner cells of an untextured gradient box. Why 8 and
        47 is the designer's choice, which is not queued.
      - Control: `_index/candidates/uq354-untextured/uq354_untextured.py` (4 checks, FAILS 0).
- [x] ~~**UQ-355.** Whether `002D6990` superseded this. §5 declines to claim it.~~
      **ANSWERED 2026-09-16 (FABLE) in [OPEN-QUESTIONS.md](../../_index/OPEN-QUESTIONS.md): NO
      — both are live and their callers are disjoint**, this renderer's guard having four
      direct callers to `002D6990`'s two. *Reconciled 2026-09-19 (FABLE): git dates the answer (09:47) after the
      `UQ-351` note above (06:00), so the answer is the later position; box ticked, note updated, register status
      column set to ANSWERED. Re-measured the same day: no conditional-jump site and no address-taking reference to
      either routine, so the two caller sets are complete for static reach.*
      **THE DATA TEST WAS ALSO TRIED, WITH A CONTROL, AND IT DOES NOT DISCRIMINATE (OPUS,
      2026-09-19).** §5 compared the two systems' *callees*; it did not compare their *data*,
      and that is the obvious next test — if the live system reads the globals the dead one
      used, it plausibly took over the job. Collecting every data address each body references,
      instruction-aligned from each function entry: **the island's five functions touch 9
      distinct data addresses, the live 3×3 system's four touch 10, and they share 8.** Taken
      alone that reads as strong support for supersession. **But `002DC290`, the live box drawer
      this section says has "nothing to do with this island", shares the same 8** — a control
      that is supposed to be unrelated scoring identically means the measurement does not
      discriminate. **All eight are documented common infrastructure**, which explains the null
      rather than asserting it: `01F44830` is the stack cookie, which every function with a stack
      array references; `0215E6D0` is the draw-bracket-open flag answered under `UQ-352`/`UQ-348`,
      which eight callers across the UI gate drawing on; `022D8F30`, `022D8F40`, `022D8F50` and
      `022D8F60` are four cells of the emulated-GPR shared scratch block `022D8F30`–`022D8F6F`
      ([shared scratch](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md),
      `UQ-350`); `02EBEFC0` and `02EBEFF0` are the shared transform workbench
      ([the two transform primitives](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)).
      So the overlap is what **any** two presentation functions have in common. Deciding
      supersession needs evidence of a different kind — build order, a cut-content marker, or a
      caller that once reached the dead path — none of which the image carries.
      **Without the control this would have been filed as "8 of 9 addresses shared, supersession
      supported" — and against FABLE's independent answer that is not merely unsupported, it is
      wrong.** *Static. The measurement is recorded so it is not repeated; it narrows nothing,
      because an inconclusive test narrows nothing.*
      *Two instrument notes from the re-run.* The first run collected **RIP-relative references
      only**, and `data_xref_scan.py` warns that this binary addresses globals through an
      image-base register instead; re-running with **both** forms leaves the numbers unchanged,
      because these particular globals are RIP-addressed in these bodies — checked rather than
      assumed. And a data-section filter built on that script's `sections_of` uses **raw** sizes,
      so `.data`'s BSS tail — where `022D8F30` and `02EBEFC0` live — falls outside it and
      the scan reports **one** address per group; the re-run parses `VirtualSize` and asserts
      three known data addresses pass the filter before trusting any absence. *The measurement is `Database/Tools/analysis-kit/gfz-scripts/data_overlap_with_control.py`, which carries these three populations as its worked example and both instrument failures as its self-test.*

---

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The 3×3 grid derivation and the skip-if-zero rule | complete exact-current body of `00392A10` | 1 |
| The corner-colour expansion and the 16-entry grid | same body | 1 |
| The exact per-cell flag gate, including the 8..47 band | same body | 1 |
| Two paths selected by `002DD4B0` | same body | 1 |
| The per-channel corner blend | complete body of `002DC7F0`, `flags & 8` branch | 1 |
| The fallback builds one quad and calls the live drawer | complete body of `00392CE0` | 1 |
| `002DC290` is live with 11 callers; `002DD4B0` live with 10 | call-graph census | 11 |
| `002D6990` is a separate live 3×3 system | its CodeDomain tag and its disjoint callee set | 3 + 11 |

### That nothing reaches it — five independent routes, each controlled

This is the load-bearing claim, so each route was run with a control that could fail.

**1. Call graph.** `00392A10` has zero entries as a callee in `edges.tsv`.

**2. Direct relative `CALL`/`JMP`, from the bytes.** Every `E8`/`E9` in `.text` was decoded and its
target computed. **Zero reach `00392A10`.**
*Control:* the same scan recovers the known edges `00392A10 → 00392CE0` and `00392A10 → 002DC7F0`
(three sites). **PASS** — the scan can find calls into this island when they exist.

**3. Address materialised in code.** Every RIP-relative `LEA` in `.text` was decoded: none targets
it. The `MOV r64, imm64` form was then checked, because the re-census had published it as a blind
spot. **The form occurs 1,413 times in `.text` and not one carries a base relocation**, so none of
them encodes an image address — MSVC under `/DYNAMICBASE` materialises code addresses with
RIP-relative `LEA`. **The published blind spot is empty for this binary.**
*Control:* the matcher fires 1,413 times, so the zero is a measurement and not a silent
non-match. **PASS.** *(The first version of this check required the relocation up front, matched
nothing at all, and would have reported a meaningless zero. Recorded because the vacuous result
looked identical to a real one.)*

**4. The address is not present in the file.** The 8-byte and 4-byte little-endian encodings of
`00392A10` occur **zero times anywhere in the image** — no data slot, no pointer table, no immediate.
The same holds for `00392CE0` and `002DC7F0`.

> **Corrected 2026-09-03 — "no RVA entry" was false as written, and the conclusion is unaffected.**
> This route searched the **VA** encoding only. Searching the **RVA** form (`VA − 0x120000`) finds
> hits for every island member:
>
> | function | RVA | where |
> |---|---|---|
> | `00392A10` | `272A10` | **1** — `.pdata`, `RUNTIME_FUNCTION{Begin=272A10, End=272CD3}` |
> | `00392CE0`, `002DD1E0`, `002DD090` | — | **1 each** — `.pdata` |
> | `002DC7F0` | `1BC7F0` | **4** — one `.pdata`, and **three in `.rdata` at `01D72338`, `01D7235C`, `01D7236C`** |
>
> The three `.rdata` hits are **not** a pointer table. This image has no `.xdata` section, so unwind
> data lives in `.rdata`, and that function's `.pdata` record names its unwind info at RVA `1C522FC`
> — `0x3C` below the first hit. **All three sit inside that function's own unwind block.**
>
> So every RVA reference to the island is `.pdata`, `.xdata` or an unwind record: **the exact classes
> this project bans as evidence**, after a branch lost 182 classifications to them. The right
> statement is **"no *admissible* RVA entry"** — the absence is true *by rule*, not by measurement,
> and the distinction matters because a future reader repeating the search will find hits. Finding
> them and treating them as reachability would be the `.pdata` contamination returning.

**Routes 4 and 5 are not independent.** Route 5 concludes that no data slot can hold the address, and
it reaches that from route 4's byte search rather than from a separate measurement. Its own
contribution — that `FF 25` thunks exist, are found, and read from data slots — is real and
controlled; the step from there to *"therefore none reaches this island"* is route 4's zero. **Four
independent routes and one dependent corollary**, which is still enough, and is what the evidence
supports.

**5. Indirect thunks, added 2026-09-03.** A sibling pass found that `0020AC30` — the other function
published as evidence-free — is in fact reached through a 5-byte `JMP` thunk that a call-graph census
cannot see. Route 2 here is byte-level and would have caught such a thunk, but the *indirect* form
was checked explicitly: `FF 25` (`jmp [rip+disp32]`) occurs **291 times** in `.text`
*(control: the form is present and found, **PASS**)*, and every one of them reads a pointer from a
data slot. The 8-byte encoding of `00392A10` occurs **zero** times anywhere in the file, so **no slot
can hold it and no indirect thunk can reach it.** This finding is stronger than when it was first
published, not weaker.

**What would falsify this:** any of the five returning a hit; or an address computed arithmetically
at run time from a base and an offset, which no compiler emits for a call target and for which
there is no evidence here. **The claim is "unreachable by every static route", and that is what has
been shown — not "provably never executed", which static analysis cannot establish.**

### Provenance of the question

`00392A10` was identified as the last evidence-free function by the reference re-census recorded in
[why the unowned code has no owner §16](../Unowned-Code-Census/why-the-unowned-code-has-no-owner.md),
after that census was repaired in both directions: it had been missing relocated data slots, and it
had been counting an `OR` immediate mask and a duplicate row as code references.

---

## 9. Related

- [`../Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`](../Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
  — §16, the repaired reference census that isolated this function.
- [`../the-unresolved-158.md`](../the-unresolved-158.md) — the residual this belongs to.
- [`../Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`](../Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md)
  — the text drawn *inside* these boxes, and live.
- [`../../16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`](../../16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md)
  — UI geometry that is live.

## 10. Falsification pass 1 — 2026-09-03, by a session with no stake in this document

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`. The two things attacked first
were chosen because of what has failed elsewhere tonight: **an absence claim whose support might be
the wrong kind**, and **a population claim**, which is the shape that broke in three documents today.

### The absence claim survives, with one route's wording corrected

Each of the five routes was re-run and asked *does it test what it appears to test?* Four do. Route 4
appears to test "the address is nowhere in the file"; it actually tested "**the VA encoding** is
nowhere in the file". The RVA form is present for every island member — all of it `.pdata` or unwind
data, all of it inadmissible here. Corrected in §8 above, with the mechanism, because the conclusion
is right and the sentence was not.

Route 5 was also found to depend on route 4 rather than to stand beside it. **The claim is now
"four independent routes and one dependent corollary"**, which the evidence supports and the earlier
count did not.

### The population claim reproduces exactly

| function | body | callers |
|---|---:|---|
| `00392A10` | 707 B | **none** |
| `002DC7F0` | 2,194 B | `00392A10` only |
| `00392CE0` | 589 B | `00392A10` only |
| `002DD090` | 332 B | `00392A10` only |
| `002DD1E0` | 268 B | `00392A10` only |
| | **4,090 B** | claimed 4,090 B |

Sole-caller status holds for all four; the total is exact. The two live callees are confirmed live —
`002DC290` with **11** callers, `002DD4B0` with **10** — so "the dead code calls live code, nothing
live calls the dead code" is measured, not asserted.

### What I tried that failed to break it

- Attacked route 3's `MOV r64, imm64` control expecting a vacuous zero of the kind that has been
  published twice tonight. It is not vacuous: the form fires 1,413 times and the document already
  records that its own first version *was* vacuous and was rebuilt. That is the check working.
- Attacked the byte searches by computing whether three `.rdata` hits could be noise. For a specific
  4-byte value over ~22 M positions the expected false count is about **0.005**, so three hits are
  real structure — which is why they had to be identified rather than dismissed, and they turned out
  to be unwind data.
- Attacked the island arithmetic against the current graph rather than the document's own figures.
- Ran the neighbour check first: 12 cited addresses, six shared with `the-unresolved-158.md` and two
  with the cutscene document. No contradiction in either direction.


## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named these bodies only at their entries. Each interior address was read in the shipping
image; the notes say what the instruction does, not yet the body's full role.

| body | interior cite | what is there |
|---|---|---|
| `002DC7F0` | `002DC8FF` | `call 00202B70` — first of six calls to the same leaf, consistent with this page's dead-renderer reading |
| `002DA7C0` | `002DAA34` | `call 00202B70` — same leaf; body ends through `00181460` + `__security_check_cookie` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **WorldAreaField — CLIENT.** A cited function is called by an 887-byte field body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**StoryEvent — SERVICE.** `0020AC30` on this page calls `FUN_0020a800`, owned by that layer. What it reaches is a 554-byte routine in a `0x100`-byte frame that opens by calling an import through `008C2448`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).


**UI — CLIENT and SERVICE (SWE2-EC7 batch-150).** The `00296360` register/unregister rides the `003F89C0`/`003F8A30`/`003F8A50` registry family and `0028F590` accessor the UI layer shares (`00297C10`/`002962D0` siblings), and the installed callbacks `0029B7D0`/`0029B810` ~~are themselves called by UI's `002973E0`~~ themselves call UI's `002973E0` (at `0029B7EA` and `0029B851`; `002973E0` reaches neither handler) *(corrected 2026-10-03, FABLE, on ASTRA-REQ-FABLE-OV42-GAUGE-BINDING-1003 and SWE2-AUDIT-SPEC's ACCEPT of its evidence; [`fable-ov42-handler-edge-1003`](../../_index/candidates/fable-ov42-handler-edge-1003/README.md))* - registry fan-in around the dead renderer, not a live UI dependency.

### Interior citation — frontier hubs `002DAC70`, `002753F0` (2026-09-18, SWE2-EC7)

`002DAC70` — 690 B, 7 callers: the packet emitter in this family's submit
chain. `([rcx+0x10] - [rcx+8] - 0x20) >> 4` counts the queued packets; the
`0x6C008000 | (count << 0x10)` header lands at `[+0x1C]` beside the
`0x10000000` bracket at [`002DACB9`](../../_index/ADDRESS-INDEX.md); count == 7
flushes through `0016D6A0` + `003A1DB0`
(`RenderCommand_SubmitCurrentBufferAndSwap`), any other count marks
`or [rax-0xA8], 1` pending instead. Sibling of `002DD090`/`002DD350`.

`002753F0` — 68 B, 7 callers (the `002C0BE0` arm above): the recursive
callback-chain walker — invokes `[rcx]`'s vfn, then recurses through the
`[+0x18]`/`[+0x20]` link pair at
[`0027541B`](../../_index/ADDRESS-INDEX.md). Sibling shape of `00275440`, this
variant calling before descending.
## SWE2-EC7-35 update (2026-09-19) - `002D6990`

`002D6990` (783 B) is the ~~dead~~ live nine-patch draw body *(corrected 2026-10-02, OPUS: called by two functions, a bounded-loop caller at its +0x75 and `003C6B70` at +0x72C; UQ-355 keeps it live)* - `0209AC30` bank, `002DAF30`/`002DAC70`/`002DA7C0` draw helpers plus `00808C40`. Interior anchor `002D6AC5` (an `00808C40` call).

## SWE2-EC7-100 update (2026-09-20) - `002BEF70` measured

`002BEF70` (56 B) is the install-and-publish trampoline
`002BE4F0` and `002C0BE0` call: `[rdx+8]`'s first pointer
lands at `+0xC0`, `+0x40` loses bit 7, `002735E0(1)`
resolves the second argument, and the tail `jmp
00247570` publishes - the flag-clear-install-refresh
idiom the renderer's arms share.
Interior anchor `002BEF93` (the `002735E0` call).

`00296360` (232 B) is the register/unregister pair `002C0870` drives: a nonzero `0209C2F0` first unregisters both `0209C240` and `0209C298` entries through `003F8A30` on `0028F590()` and clears the flag; then with `edx` nonzero, `rcx` live and `dword[rcx+4]` nonzero it stores `edx` into `0209C2F0`, registers `0029B7D0`/`0029B810` as the two entries' callbacks through `003F89C0`, re-looks-up both via `003F8A50`, and caches `rcx` at `0209C288`/`0209C2E0`

Interior anchor `002963E7` (function `00296360`).

*Registration does not start a bar update through these two callbacks (FABLE, 2026-10-03, on ASTRA-REQ-FABLE-OV42-REGISTER-EVENT0-1003 after SWE2-AUDIT-SPEC's ACCEPT; record [`fable-ov42-event0-consumption-1003`](../../_index/candidates/fable-ov42-event0-consumption-1003/README.md)):* `003F89C0` zeroes the `0x58`-byte record and then fills it itself - bit 0 of word `+0x26` (`003F89EF`), the fifth-argument callback at `+0x38` (`003F89F4`), the third-argument dword at `+0x40` (`003F89F8`) and the fourth-argument context at `+0x48` (`003F89FB`) - and only then calls a non-null callback synchronously with `rcx` = the record, `edx` = 0 and `r8` = its zero-extended second argument (`003F8A04`-`003F8A0C`). At this event 0 both prescribed handlers return 0 with no bar update: each first reads the qword at `+0x48` of `rcx` (`0029B7D7`, `0029B814`), before any test of `edx`; then `0029B7D0` branches at `0029B7DE` and `0029B810` at `0029B823` (`edx` - 1 is neither 0 nor 1) to `xor eax,eax` / `ret` (`0029B7FB`, `0029B82F`), with no call, no memory write and no use of the loaded context or of `r8`. The bar update is event 1 only (the rows below). The `+0x48` read is unconditional, so a bad record pointer can still fault at event 0. Evidence: ASTRA's [`ov42-register-event0`](../../_experiments/evidence/ov42-register-event0/README.md) (commit `0d55f8417`, a static path proof, nothing executed). Still OPEN: which callback a matched `00297C10` row keeps at `+0x38` (that path skips `003F89C0`), the record's natural initialisation, scheduling, lifetime and the first draw.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Presentation — MECHANICAL, 80 edges.** `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is called by `0024A710`, `002B0280`, `002DB080`, `002DC290` and 12 more; `00181460` is called by `002AFDC0`, `002D9DB0`, `002DA2D0`, `002DA7C0` and 10 more; `002DD4B0` is called by `00245170`, `002455A0`, `0029E840`, `0029ED50` and 3 more; `002DAC70` is called by `00245170`, `002455A0`, `002D0650`, `002D6990` and 1 more; `002DAF30` is called by `00245170`, `002455A0`, `002D0650`, `002D6990` and 1 more; `002DD350` is called by `003C2870`, `003C2E60`, `003C37B0`, `003C4B20` and 1 more; `00245E60` calls `00245170`, `002455A0`, `00245E60`; `002DA7C0` is called by `00245170`, `002455A0`, `002D6990`; `00275440` is called by `002B7B80`, `002BAF80`; `00392A10` calls `002DC7F0`, `00392CE0`; `00181460` calls `001B06D0`; `0020AC30` calls `001C5750`; `00245E60` is called by `00245E60`; `00246480` is called by `00245E60`; `002D6990` calls `002DA7C0`; `002D6990` is called by `003C6B70`; `002D8C00` is called by `00245E60`; `002DAC70` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DC290` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DC290` is called by `00392CE0`; `002DC7F0` is called by `00392A10`; `002DD090` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `002DD090` is called by `00392A10`; `002DD1E0` is called by `00392A10`; `002DD350` calls `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`); `00392CE0` calls `002DC290`; `00392CE0` is called by `00392A10`; `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) calls `GraphicsCommand_PublishCompletedBatchState100` (`0036F360`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-box-renderer-that-is-never-called-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0029B7D0` | 50 B | returns 0 unless `edx` is 1; for 1 calls `002973E0(rcx, dword at r8, dword +0x24 of the object at qword +0x48 of rcx, dword at r8+4)` and returns -1 when that returns 0, else 0 | `0029B7DB`, `0029B7E4`, `0029B7EA`, `0029B7F3`, `0029B7FB` |
| `0029B810` | 82 B | with the object at qword `+0x48` of `rcx`: when `edx` is 2 stores its dword `+0x2C` shifted left by 4 at `+0x4` of `rcx` and returns 0; when `edx` is 1 calls `002973E0(rcx, dword at r8, its dword +0x30 multiplied by its byte +0x87 when that byte is non-zero, dword at r8+4)` and returns -1 when that returns 0, else 0; any other `edx` returns 0 | `0029B81E`, `0029B829`, `0029B82C`, `0029B846`, `0029B851` |
| `002C0B40` | 148 B | switches on the dword at `rdx`: 1 stores the qword pointed to by qword `+0x8` of `rdx` at `+0xC0` of `rcx`, clears bit 7 of dword `+0x40`, calls `00247570(rcx, 002735E0(1))`, stores dword 0x800080 at `+0xD8` and returns 0; 3 scales, on the object at qword `+0x38`, word `+0x5A` by word `+0xD8` and word `+0x58` by word `+0xDA` of `rcx` (signed product shifted right by 7) and returns 0; other values tail-jump `005C5230` with `rcx` and `rdx` as passed in | `002C0B5D`, `002C0B7B`, `002C0B8C`, `002C0BBD`, `002C0BC4` |
