---
system: The nine-patch window frame
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Presentation.Primitive
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0028BB50, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
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
  last_pass_state: residual-cluster-4-repos-55
  crossref_clean: true
  reopened_count: 0
---

# The nine-patch window frame

**The 158 survey's residual cluster 4 — `002DC290`, `002DC7F0`, `00392A10`, `00392CE0`, 4,853 bytes, all four classified at GN161 into `Presentation.Primitive.*` — is one
mechanism: how the game draws a resizable box with a border and a colour gradient.**

All four are read here. **The clustering held again**, as it did for cluster 3.

## 1. What the player sees

**Every window in the game is nine rectangles.** A menu panel, a dialogue box, a gauge backing: the
four corners keep their size, the four edges stretch along one axis, and the middle stretches both
ways. **That is why a window can be any size and its border never distorts.**

**Two things beyond that are worth a modder's attention.**

**The colour is a gradient across the whole window, not per patch.** Four corner colours are given
once; each of the nine cells gets the four colours *it* would have at its own corners, interpolated
from them. **A window is one gradient that happens to be cut into nine pieces.**

**And medium-sized cells are subdivided again.** A cell between **8 and 47 pixels** on the axis being
drawn is split into two quads through its centre, with a blended colour at the split. Smaller and
larger cells are not. **The gradient in a mid-size border is smoother than the same gradient in a
large one**, because it has an extra vertex in the middle.

## 2. The geometry

The caller passes a `short[8]`:

| index | meaning |
|---:|---|
| 0, 1 | `x`, `y` |
| 2, 3 | `w`, `h` |
| 4, 5 | **left** and **right** border widths |
| 6, 7 | **top** and **bottom** border heights |

and the middle sizes are derived:

```c
columns = { left, w - right - left, right };     // 00392CE0
rows    = { top,  h - bottom - top,  bottom };
```

**Nothing clamps these.** A window narrower than `left + right` gives a negative middle column, and
the code carries it into the draw rather than rejecting it.

**Cells of zero size are skipped** — both loops test the extent before drawing, so a border of zero
costs nothing.

## 3. Two dispatchers, and a runtime choice between them

`00392A10` asks `002DD4B0()` first:

```c
if (FUN_002dd4b0() == 0) { FUN_00392ce0(ctx, rect, colours); return; }   // the simple path
FUN_002dd1e0(&scratch, ctx);                                            // otherwise
... three loops calling 002DC7F0 ...
FUN_002dd090(&scratch, ctx);
```

**Each of the three row loops runs three cells**, read at instruction level:

```asm
00392BE4  call 0x002DC7F0            ; one cell
00392BED  add  rbx, 0x4              ; next column
00392BF1  cmp  rbx, 0xc              ; 3 columns x 4 bytes
00392BF5  jl   0x00392BA0
00392BF7  add  r15d, r14d            ; advance y by this row's height
```

**So `00392CE0` is not a caller of `00392A10` or a helper of it — it is the fallback**, chosen at
runtime by a predicate this document does not resolve. **The two dispatchers draw the same nine
cells through different primitives**: `00392CE0` through `002DC290`, `00392A10` through `002DC7F0`.

~~**And `00392A10` has no callers at all** — one of the fifteen no-caller entries the survey listed in~~
~~[the unresolved 158](the-unresolved-158.md).~~ Its own fallback `00392CE0` has exactly one.

> **CORRECTED 2026-09-16 (OPUS). `00392A10` IS REACHED, and this page was the last to hear it.**
> It was shown reachable in `6e5ffdaf`; this page never learned it and went on asserting the
> opposite in two places. Re-derived here rather than quoted:
>
> ```
> 00392A00  cmp word ptr [rcx + 0x58], 0     a 12-byte guard stub
> 00392A05  jne 00392A10                     conditional TAIL JUMP, out of its own 12 bytes
> 00392A0B  ret
> ```
>
> and `00392A00` has **four ordinary callers**, each verified to be a real instruction
> boundary by decoding its container from that container's own entry: `002A62EE`, `002C0967`
> (`UI`), `002C0E5E` (`UI`), `00574056`. **Two of the four are `UI`-owned**, which is where a
> nine-patch box renderer belongs.
>
> **Why every census here missed it:** none enumerated `0F 8x rel32`, the conditional near jump.
> The same omission produced three other false absences in this database on one day, each on
> its own page and named there. `check_absence_claims.py` now carries a `jcc` instrument,
> controlled on a body no other instrument in it can see, and that is what surfaced these two
> sentences.
>
> **The premise is refuted; the runtime question is not answered.** A static route exists. Whether
> `[rcx+0x58]` is ever non-zero is a runtime question this page cannot settle, so *never called*
> is now an open question rather than a fact. The fallback story below is untouched.
>
> **`UQ-351` ANSWERED 2026-09-25 (OPUS).** The word is `[widget+0x38]`'s **composed opacity**.
> - The draw pass `00245E60` points `+0x38` at a stack record. `002D8C00` fills that record with alpha 0, and
>   the pass then sets the alpha from byte `+0xA0` (default 0x80), times the parent's alpha, `>> 7`.
> - So the box draws unless the widget, or an ancestor, is fully transparent.
> - The full answer is at `UQ-351` in [the box renderer page](Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md).
> - The replay is [`uq351-opus-replay-widget-alpha-guard`](../_index/candidates/uq351-opus-replay-widget-alpha-guard/).

## 4. The corner flip

`00392CE0` has a special case for **two of the nine cells** — the top-left (`row 0, col 0`) and the
bottom-right (`row 2, col 2`):

```c
sStack_c0 = size + x;      // the origin moved to the far edge
sStack_bc = -size;         // and a NEGATIVE width
```

**A negative extent passed to the quad primitive mirrors the patch.** The other seven cells are
drawn from their own origin with a positive size.

> **Two opposite corners drawn mirrored is how a symmetric border is built from one asset** — but
> **which asset, and whether the mirroring is of texture or of gradient, is not established here.**
> The primitive receives only positions and colours.

## 5. `002DC290` — the gradient quad

**It is the sibling of the flat rectangle primitive** in
[drawing one coloured rectangle](drawing-one-coloured-rectangle.md), and the differences are exact:

| | `002DBDD0` (flat) | `002DC290` (gradient) |
|---|---|---|
| colour | **one**, from the context, tinted | **four**, from the caller — 16 bytes |
| first command word | `0x1000000000000003` | **`0x1000000000000002`** |
| the wide constant | `0x1022400000008004` at `002DBFAB` | **`0x2026400000008004` at `002DC4EA`** |
| trailing word | `1` … `4` | **`0x41`** |
| tint delivery (second back-end) | packed into one dword at `context + 0x94` | **`FUN_001816F0(br, br, br, alpha)`** — four separate ints |

**Both take the same two state handles**, `context + 0x78` and `context + 0x80`, and both end in
`00181460(&points, 4)` then `00181330()`.

> **`FUN_001816F0(br, br, br, alpha)` confirms the tint split a third time.** `br` is
> `context + 0x5A` and `alpha` is `context + 0x58` — **three channels from one field and the fourth
> from another**, exactly as the flat primitive's `SAR` sequence showed. **Three independent
> derivations, two functions, one rule.**

**The command block is written into a ring** at `&DAT_02EBEFC8 + DAT_02EBEFF0 * 0x18`, and the ring
pointer is advanced by the bytes written, rounded down to 16. **`DAT_02EBEFF0` is the same index
the text walk reads at `003649F0`** to pick its own buffer.

## 6. `002DC7F0` — the patch that splits itself

Three modes, selected by bits of the flags argument:

| flags | behaviour |
|---|---|
| bit 2 set (`& 4`) | **one quad**, drawn with `flags & ~4` |
| bit 3 set (`& 8`) | **two quads**, split through the patch centre, each with `flags & ~8` |
| neither | **one quad**, flags unchanged |

**The split point is the centre**: `x + w/2`, `y + h/2`, and `00202B70` — the perspective divide —
is called for the two corners **and the centre**, three times instead of two.

**The colour at the split is a cascaded average of all four corner colours**, per channel:

```c
mid = ((((c0 + c1) >> 1) + c2) >> 1) + c3) >> 1;
```

> **That is not the mean.** Halving at each step weights the last colour most: the contributions are
> **1/8, 1/8, 1/4, 1/2**. **A "blend" that is three shifts deep is a specific choice**, and this
> document reports the weights rather than calling it an average.

## 7. Why 8 to 47

`00392A10` chooses the flag per cell:

```c
if (col == 1 || (uint)(size - 8) > 0x27 || (uint)(axis - 8) > 0x27)
     flags = (index == 2) ? 0 : 4;     // no split
else flags = (index == 1) ? 0 : 8;     // split through the centre
```

**`(uint)(n - 8) > 0x27` is an unsigned range test** meaning `n < 8 || n > 47`. So a cell splits only
when **both** its own size and the axis extent fall in `[8, 47]`, and **never in the middle column**.

> **A cell smaller than 8 pixels gains nothing from an extra vertex, and one larger than 47 is
> presumably better served by the flat interpolation.** That is the reading; the thresholds
> themselves are authored constants and nothing here says what they were tuned against.

## 8. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is this really nine patches, or three rows drawn three times? | `00392CE0` is a **3 × 3 nested loop** over `{left, middle, right}` and `{top, middle, bottom}`, calling the primitive once per iteration with a per-cell rectangle. **Nine calls.** |
| Are the four colours really per-window rather than per-patch? | `00392CE0` builds each cell's four corners from the **same four inputs** (`auStack_98[]` is filled once from `param_3[0..3]` before the loops) and indexes them by cell. **One gradient, sampled nine times.** |
| Is `(uint)(size - 8) > 0x27` really `8..47`? | Unsigned subtraction wraps: `size < 8` gives a huge value, `size > 47` gives `> 0x27`. **The complement is exactly `[8, 47]`.** |
| Is the split colour an average? | Three successive `>> 1` after three adds gives weights **1/8, 1/8, 1/4, 1/2**. **Reported as the weights, not as "an average".** |
| Is `00392CE0` the fallback or the primary? | `00392A10` calls it **and returns** when `002DD4B0()` is zero, then does its own work otherwise. **The call is a tail branch, not a subroutine step.** |
| Could the negative width in §4 be a decompiler sign error? | `sStack_bc = -sVar5` where `sVar5` is the cell size just used positively for the other seven cells. **The negation is explicit and applies to two named cells.** |
| How much of this is anchored to instructions? | **Three of the four members have a zero-byte body in the live program** — only `002DC290` is visible to `search_instructions`, which is how the `002DC4EA` constant was located. `00392A10`'s loop was read with `disassemble_bytes`; **`002DC7F0` and `00392CE0` rest on decompilation alone**, and that is stated rather than implied. |
| Do the two primitives really differ, or is one a wrapper? | Neither calls the other; they differ in the command constants, the colour count and the tint delivery. **Two implementations of one shape.** |

## 9. What this document does not claim

What `002DD4B0` tests, and therefore which of the two paths actually runs. What `002DD1E0` and
`002DD090` set up and tear down around the richer path. What the command constants
`0x1000000000000002`, `0x2026400000008004` and `0x41` encode. What `00202B70` computes. Which
subsystem's windows these are. What asset the mirrored corners in §4 sample — **the primitives
receive positions and colours only, so the mirroring may not be of a texture at all.**

## 10. Cluster 4 is closed

| function | bytes | role |
|---|---:|---|
| `00392A10` | 707 | the dispatcher, ~~**no callers**~~ **reached via the `00392A00` guard stub — see §3** |
| `00392CE0` | 589 | the fallback dispatcher |
| `002DC7F0` | 2,194 | the splitting patch drawer |
| `002DC290` | 1,363 | the gradient quad primitive, **11 callers** |

**Two clusters closed, two clusterings held.** Cluster 3 was three functions that call each other;
this is four. **In both cases the call-graph grouping was done before any member was opened and it
survived being read** — which is the strongest thing the residual document's structural section has
going for it.

## Interior citation — frontier hub `00181460` (2026-09-18, SWE2-EC7)

`00181460` — 105 B, 9 A-measured callers; the `00181460(&points, 4)` grid fill this page's
draw path runs. Interior verified: outer loop runs `edx-2` rows (`00181466`), inner loop a
fixed 3 columns (`edi = 3` at `00181484`); each cell fetches a source row via `001B1C00()`
at [`00181490`](../_index/ADDRESS-INDEX.md) and `001B06D0(dst, src)` writes it into the destination, which
advances `rbx += 0x30` per column and `rsi += 0x30` per row — a (n-2)x3 stamp of
`0x30`-byte vertex/quad records, exactly the interior ring a nine-patch needs between its
corner rows. The `001B1C00` source-row getter is also run by CoreRuntimeScheduling's
`0017D4C0` — the row source is shared scratch, not nine-patch state. `0017D4C0` itself is a
shared copy/fill routine: it forwards into Input's `00198750` and Save_Load_Settings'
`001C1710`/`001C18A0`/`001C18E0` — mechanical reach, no nine-patch relationship.

## SWE2-EC7-28 update (2026-09-18) — `001B06D0` slot-init + bump cursor

`001B06D0` (198 B) — the `001B06D0(dst, src)` this page names — is the
sibling of `001B22F0` on the same `+0x3928`/`+0x2328`/`0x58` table: if
the indexed slot's `[+0]` is empty it advances the index (`<= 0x3F`),
stamps a template record (`+0x10 = 1`, `qword[+0x14] = 1`, `+0x2C..`
zeroed, `+0x28 = 0`), mirrors `+0x38` to `+0x40`, then bumps the slot
cursor `+0x30` at `[r9+0x40]` bounded by `[r9+0x48]` — the inner
bump-allocator each slot's buffer carries. Interior anchor `001B0766`
(the `+0x30` bump).

## `00181350` is the general batch append, and the slot table proves its own extent (2026-09-19, OPUS)

*Found by a census answering `U-6`: `00181350` is cited by **no page in the database**, while the
machinery on either side of it — `001B1C00`, `001B06D0`, the `+0x2328` table — is documented above.*

**It is the one-dimensional general form of the stamp this page already reads.** §above reads the
nine-patch's 2-D `(n-2)x3` loop, which fetches a source row through `001B1C00()` at
[`00181490`](../_index/ADDRESS-INDEX.md) and advances `rbx += 0x30` per column. `00181350` (56 B) is
the same body with one dimension: `00181350(dst, n)` appends **`n` consecutive `0x30`-byte records**,
calling `001B1C00()` then `001B06D0(that, dst)` and stepping `rbx += 0x30` per iteration
([`00181363`](../_index/ADDRESS-INDEX.md)–[`0018137B`](../_index/ADDRESS-INDEX.md)). A count of zero
returns before touching anything (`test edx, edx / jle` at `00181350`).

**It is a shared Presentation primitive, not nine-patch machinery.** Sixteen callers, **twelve tagged
`CodeDomain.Presentation`** — the map screens `005556A0`, `00555D10`, `005621A0`, `00562A30`, the
shared dialogs `003F3710`, the model/motion path `003F7930` — and four untagged that belong to the
save-image, audio-boundary and transform-workbench pages. Two callers (`003C7EA0`, `004009C0`) are
themselves cited nowhere.

### The 64-entry bound is fixed by the layout, not only by the compare

The `SWE2-EC7-28` section above reads the table's bound off `cmp r10d, 0x3f`. **It is independently
fixed by where the table ends.** 64 entries x `0x58` = `0x1600`, and **`0x2328 + 0x1600 = 0x3928`** —
exactly the offset of the index dword the same function loads at
[`001B06D2`](../_index/ADDRESS-INDEX.md). The array occupies `+0x2328`..`+0x3927` and its cursor sits
in the first byte past it, so **stride, count and index position each confirm the other two**; a
different count would put the index inside the array or leave a gap. (The same standard the
encoded-id-space and dispatch-table pages use for abutting regions.)

### `001B06D0` never allocates — it only rewinds

Across all 198 bytes, the slot's arena base `+0x38` and limit `+0x48` are **read and never written**:
the base is loaded at [`001B0750`](../_index/ADDRESS-INDEX.md) only to be stored into the cursor
`+0x40`, and the limit is loaded at [`001B0760`](../_index/ADDRESS-INDEX.md) only to be compared.
**So each slot's buffer is bound to it by some other writer and survives the slot's reuse** — the
push path rewinds the cursor to the base, and the append bumps it by `0x30`. An owner reading this
function alone would wrongly conclude the slot owns its storage. **NOT CLAIMED: who installs `+0x38`
and `+0x48`, or where that buffer is allocated.**

### Overflow is handed off, not dropped

When `cursor >= limit` the function does not fail silently: it loads `r8 = src`, pops and
**tail-jumps `001AED50`** with `(rcx = slot+0x38, rdx = cursor, r8 = src)`
([`001B078B`](../_index/ADDRESS-INDEX.md)). `001AED50` appears in this database **only as a table row
in `actor-storage-record-flag-bit-writes.tsv`**, explained by no page. **NOT CLAIMED: what it does** —
grow, flush or discard are all consistent with the call shape, and the corpus has read none of them.
The one thing the tail jump does establish is that the overflow argument is the *source* record, not
the destination, so whatever `001AED50` is, it still has the caller's data.

### The three `movaps` are one record, not three vec4s

The copy at [`001B0773`](../_index/ADDRESS-INDEX.md)–`001B0789` moves `0x30` bytes src→dst as three
16-byte steps at `+0x00`, `+0x10`, `+0x20`. Two consequences, and they pull in opposite directions:

- **`movaps`, not `movups`, on both operands — so the source element and the arena slot are each
  16-byte aligned.** That is an alignment contract a reimplementation has to honour: the caller's
  array of `0x30`-byte records must start 16-aligned, and `0x30` being a multiple of 16 keeps every
  later element aligned. A misaligned buffer faults here rather than running slowly.
- **By this corpus's own rule those three displacements must not be declared as fields.** They are
  steps of a whole-record copy, which `check_copy_displacements.py` (`4b91d0dc1`) exists to catch and
  which this database has already recorded three times under other names. **The record's interior is
  unread**: nothing here says whether it is vertices, a quad, or something else.

A null cursor is also guarded (`test rdx, rdx / je` at `001B076E`), so a slot whose buffer was never
installed skips the copy instead of writing to zero — consistent with the base and limit being
someone else's to set.

## SWE2-EC7-52 update (2026-09-19) - `003F3710`

`003F3710` (1639 B) is the shared-dialogs builder - `002714A0`/`002714E0`/`002714C0` triple plus `00181560`/`00181910`/`001816B0`, `"targetline_p"` string, `02B5F1F4`/`02EBB780`. Interior anchor `003F375C` (a `002714A0` call).

## SWE2-EC7-53 update (2026-09-19) - `001AED50`

`001AED50` (534 B) is a `0x30`-stride vector erase/move helper the nine-patch path tail-jumps - begin/end `[rcx+8]`/`[rcx+0x10]`, overlap `+0x30` adjust, `movaps` triple copy-down, `call [r10+8]`/`call [r9+0x18]` vcalls. Interior anchor `001AED82` (the `movaps` copy-down head).


## SWE2-EC7-53 update (2026-09-19) - `003C7EA0`

`003C7EA0` (434 B) is a nine-patch body (one of the two callers the page names) - `00181350`/`00202B70`/`00202C90`/`00202CA0`/`00808C40` plus `00D116A0` rdata. Interior anchor `003C7EFB` (a `00202B70` call).

## SWE2-EC7-55 update (2026-09-19) - `004009C0`

`004009C0` (244 B) is one of the two callers the nine-patch page names - `00181350`/`00181460` plus `02B5FD70`/`02B62D70`. Interior anchor `004009D5` (a `00181460` call).


## SWE2-EC7-76 update (2026-09-19) - `00271100` packet header write measured

`00271100` (49 B) is the packet-header writer: element `[rcx+0x20]`
gets `+0xC = (([rcx+0x10] - [rcx+0x20] - 0x10) >> 4) << 16 |
0x6C008000` and `+0`/`+4`/`+8` = `0x10000000` - the constant-tag
header the nine-patch drawers emit.
Interior anchor `00271113` (the `or edx, 0x6C008000`).

## SWE2-EC7-103 update (2026-09-20) - `002754E0` measured

`002754E0` (97 B) is the four-component lerp
`0028BB50`, `003F6BB0` and `005621A0` call: for
each `0`/`4`/`8`/`0xC` lane,
`[rcx + i] = [rdx + i] + ([r8 + i] - [rdx + i]) *
xmm3` - the vec4 interpolate the frame arms share.
Interior anchor `002754E9` (the first
`mulss`).

`002A7720` (552 B) is the mode-step `002A6190` calls: `[rbx+0x3E8]` bits 8-10 dispatch 0/1/2, each arm requires `01E0CDC8` and `[rbx+0x80]` bits 0/1 clear, mode 1 rewrites the field `& 0xFFFFF8FF` and calls `002A3DF0(rbx, 0x50)` after copying `0209C988`->`0209C980`, mode 2 does `btr 0xA; or 0x300` and tail-jumps `002A3DF0(rbx, ecx+1, edx=0x50)` - the window's mode transition.

Interior anchor `002A7783` (function `002A7720`).

`002A3DF0` (352 B) is the size differ `002A7720` calls: `0209C610` global record, `002DD7E0` fetches the `0x67`/`0x69` string then `0x68`/`0x6A` by the `ecx` arm, `[rbx + 0xC8]`/`[+0xCC]` are compared and the byte deltas written to `[rbx + 0xD4]` - the frame's string-width refresh.

Interior anchor `002A3E1A` (function `002A3DF0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7, batch 127)

**Presentation — CLIENT (SWE2-EC7-162, 277 edges).** The frame's subjects are consulted by the
Presentation layer (`00181330` calls `001B03D0`; `00274CB0`/`002AFDC0`/`002DBxxx` call it back) -
the nine-patch painter feeds presentation rows; consultation both directions, no shared
ownership.

**Save_Load_Settings — SERVICE (SWE2-EC7-162, 6 edges).** `0017D4C0` calls `001C1710`/
`001C18A0`/`001C18E0` on that layer - the frame's helpers reach settings-layer bodies;
mechanical consultation.

**UI — CLIENT (SWE2-EC7-162, 51 edges).** `002A0440` and the UI layer call this page's subjects
(`00181330`, `00181560`, `001816B0`, `00181910`, +47 more) - the frame is consulted by UI,
not shared with it.

**CoreRuntimeScheduling — SERVICE (SWE2-EC7, batch 159, 12 edges).** `0017D4C0`, the frame's
shared helper, also reaches `001A14E0`/`001DB500`/`0022A0B0` on that layer - the window
blink machinery consults core scheduling; mechanical consultation, no shared ownership.

**Input — SERVICE (SWE2-EC7, batch 165, 3 edges).** `0017D4C0` calls `00198750`, which calls
`00195060`, and the flag predicate `0032A8A0` this page's `002A3F90` section cites is itself
reached from `00253C70` on that layer - shared-helper fan-in, no Input relationship to the
frame.

**Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7, batch 165, 1 edge).** The same `0032A8A0`
predicate is reached from `0034E0B0` on that layer; shared-helper fan-in, no Script_VM
relationship to the frame.

**Story_Event_Quest_Hunt — MECHANICAL (SWE2-EC7, batch 165, 1 edge).** `0032A8A0` calls
`00377970` on that layer; shared-helper fan-out, no Story_Event relationship to the frame.


`002A40B0` (184 B) is the two-phase blink timer `002A7720` ticks for the frame's flash state: phase byte `[rbx+0x3D6]` selects the lane - phase 0 clears `[+0x3DA]` and counts the `+0x3D8` word against `0x28 / 00248F20()`, expiry arming phase 1 and seeding the counter `0x40000`; phase 1 writes `+0x3DA = 4` and counts against `8 / 00248F20()`, expiry clearing phase and counter back to zero

Interior anchor `002A40EA` (function `002A40B0`).

`002A7ED0` (158 B) is the mode classifier `002A6190` calls: `[rcx+0x3E8] & 0x700 == 0x300` returns `4` outright; otherwise a negative `[+0x17E]` byte admits a `edx`-decode where modes `1`/`3` fold to the same arm, `[r8+0x15A]` nonzero bumps the answer to `4`, and the remaining lanes return `1`/`2`

Interior anchor `002A7EF7` (function `002A7ED0`).

`002A8410` (157 B) is the three-slot normalize `002A6190` runs when `[rcx+0x3E8]` bit `0x1000` is set: it walks three entries of the `0209CC18` list, and for each node whose `[rbx+0x7C]` low-nibble class is neither `1` nor `4` it rewrites the field `(edx & 0x3FF) | 0x19064C00`, then runs `00247570(rbx, 00916490)` and `00244DD0(rbx)` on it

Interior anchor `002A8482` (function `002A8410`).

`002A3F90` (156 B) is the gated row sweep `002A6190` runs on the window record: skipped when `0032A8A0(0x6F)` is set or `0036D830()` is nonzero or `byte[+0x3F3]` is negative; else the `[+0x3F8]` array's `word[+0x3F0]` entries at `0x60` stride each get `002A7AD0`, the results or-accumulate, and when all returned zero `byte[+0x3F3]` loses its `0x1C` bits before the `002A5BC0` tail.

Interior anchor `002A3FE7` (function `002A3F90`).

`002A7AD0` (404 B) is the per-node animator `002A3F90` runs on each `0x60` row of `[+0x3F8]`: three gated phases on `byte[+8]` - bit `0x04` runs the `+0x2D` counter against `+0x2E`/`+0x2F`/`+0x2C` (decrement-to-clear, `word[+0x16]` advance, `002A7A60` callback); bit `0x10` ramps `word[+0x58]` through `00248F40` toward 1.0f and writes the lerped pair `+0x24`/`+0x28` from `+0x48`/`+0x50` scaled by `+0x4C`/`+0x54`; bit `0x08` ramps `+0x40` the same way and writes scaled bytes `+0x20`/`+0x21` from `word[+0x38]`/`+0x3A` + `byte[+0x34]`/`+0x35` - phase bits self-clear on completion.

Interior anchor `002A7B4F` (function `002A7AD0`).

`002A5BC0` (255 B) is the row reorder `002A3F90` tail-calls: when `byte[+0x3F2]` is set it insertion-sorts the `word[+0x3F0]`-length index array at `[+0x400]` by the `+0xE` priority byte of each `0x60` record in `[+0x3F8]` (descending - each new index sinks left while the prior rows' priorities are smaller), then clears `+0x3F2` and `+0x3F3` bit `0x20` - the z-order restack the row sweep kicks off.

Interior anchor `002A5C69` (function `002A5BC0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**ActorEntity — MECHANICAL, 2 edges.** `0028BB50` calls `002713E0`; `003F6BB0` calls `002713E0`.

**Resource — MECHANICAL, 3 edges.** `0017D4C0` calls `001A11B0`, `001DB1E0`; `003F3710` calls `0024A5A0`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
