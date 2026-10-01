---
system: Drawing one coloured rectangle
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
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
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
  last_pass_state: residual-walk-repos-55
  crossref_clean: true
  reopened_count: 0
---

# Drawing one coloured rectangle

**`002DBDD0` is the primitive.** Residual when surveyed — classified at GN161 `Presentation.Primitive.TintedRectangleQuadEmit` — **seven callers**, and every one of them wants the same
thing: a rectangle in screen coordinates, tinted by the drawing context's own colour and brightness.

**It emits the rectangle twice, through two different back-ends**, and that duality is the most
interesting thing in it.

## 1. What the player sees

**Every flat coloured box in the game.** The panel behind a menu, the bar of a gauge, the backing of
an icon — anything that is a rectangle rather than a picture goes through here.

**What a modder gets from this is the tint rule.** A rectangle is never drawn in its own colour: it
is drawn in the **context's** colour, scaled by the **context's** brightness, and the scale is a
divide by 128. **Changing the colour of a box means changing the context that draws it, not the
box.**

## 2. The rectangle

The caller passes `short[4]` — `x`, `y`, `w`, `h` — and the function expands it to four corners:

```c
p0 = (x,     y    )      // local_158 / local_154
p1 = (x + w, y    )      // local_148 / local_144
p2 = (x,     y + h)      // local_138 / local_134
p3 = (x + w, y + h)      // local_128 / local_124
```

Each corner is a **four-float record** — the two coordinates, then `0.0` and `1.0f` — so the block
handed on is four `(x, y, 0, 1)` points.

## 3. The tint, and what it confirms

```c
uint c   = context[0x90..0x93];          // RGBA, one byte each
int  br  = (short)context[0x5A];         // brightness
int  a   = (short)context[0x58];         // a second scale, for the fourth byte only
context[0x94] = ((c.r * br) >> 7)
              | ((c.g * br) >> 7) << 8
              | ((c.b * br) >> 7) << 16
              | ((c.a * a ) >> 7) << 24;
```

**Read at instruction level**, and the register reload is the whole point:

```asm
002DBEB4  movsx ecx, word ptr [rbx + 0x5a]      ; brightness
002DBEB8  movzx eax, byte ptr [rbx + 0x90]
002DBEBF  imul  eax, ecx
002DBEC2  sar   eax, 0x7                        ; R
002DBEC9  movzx eax, byte ptr [rbx + 0x91]
002DBED3  sar   eax, 0x7                        ; G
002DBEDA  movzx eax, byte ptr [rbx + 0x92]
002DBEE4  movsx ecx, word ptr [rbx + 0x58]      ; <- ecx RELOADED, a different field
002DBEE8  sar   eax, 0x7                        ; B, still on the old ecx
002DBEEF  movzx eax, byte ptr [rbx + 0x93]
002DBEF6  imul  ecx, eax
002DBEF9  sar   ecx, 0x7                        ; A, on +0x58
002DBF0E  mov   dword ptr [rbx + 0x94], eax     ; the packed result
```

**Three channels are scaled by `+0x5A` and the fourth by `+0x58`**, all with `>> 7` — a divide by
**128**, the same 1/128 fixed point the text renderer uses.

> **The shift is `SAR`, not `SHR`.** The brightness is loaded with `movsx` and shifted
> arithmetically, so **a negative brightness produces a negative channel** rather than a large
> positive one. Nothing here clamps it.

> **This settles two readings elsewhere from the consumer side.** The
> [blinking icon](the-blinking-icon-and-its-atlas.md) document calls `context + 0x5A` *brightness*
> and `context + 0x90` *a colour*; here they are multiplied together channel-by-channel and stored
> as one RGBA dword. **Neither document inferred it from the other** — the icon reading came from
> what writes those fields, this one from what consumes them.

**And the alpha having its own scale is not cosmetic.** A caller can dim a rectangle's colour while
leaving its opacity alone, or the reverse, because the two scales are different fields.

## 4. Two back-ends, one rectangle

**First, a render-command block** written into a cursor at `local_1a0` and advanced by `0x90` bytes:

| word | value |
|---|---|
| 0 | `0x1000000000000003` |
| 1 | `0xE` |
| 2 | `context[0x80]` — the same handle the icon writes as `0x1001` |
| 3 | `0x47` |
| 4 | `context[0x78]` — the icon writes `0x44` here |
| 5 | `0x42` |
| 6 | the tinted colour |
| 7 | `1` |
| 8 | `0x1022400000008004` — the literal at `002DBFAB` |
| 9 | `4` — the vertex count |
| 10–17 | four 16-byte vertices: `(x, y)`, then `context[0x70]`, then `0` |

**Then the same rectangle again through a second interface** — `00181560`, `00181910(context[0x80])`,
`001816B0(context[0x78])`, `00181870(3)`, `00181930(1,1,0,0)`, a four-times-unrolled colour fill, and
`00181460(&points, 4)` followed by `00181330()`.

> **The two paths carry the same two state handles**, `context + 0x78` and `context + 0x80`, into
> different shapes: **as literal words in a command list, and as arguments to setter functions.**
> That is what a retained legacy command stream alongside a modern API looks like.

**Between them, `00202B70` runs twice** — once per diagonal corner pair — and each result is divided
by the `w` the call fills in. **A perspective divide**, applied to two of the four corners.

### Read 2026-09-18 (FABLE): what the two back-ends are, and which one draws

**The first block is a PS2 GS packet, and its words decode.** `0x1000000000000003` with `0xE` beside it is a GIF tag of three address+data writes: register `0x47` (TEST_1) from `context + 0x80`, register `0x42` (ALPHA_1) from `context + 0x78`, and register `1` (RGBAQ) from the tinted colour. `0x1022400000008004` is a GIF tag with NLOOP 4, end-of-packet and a PRIM of triangle strip, flat shaded, alpha blending on, texturing off; **the `4` beside it is the register list - XYZF2 - not a vertex count**, which is the tag's own NLOOP. So `context + 0x78` and `+0x80` are a blend setting and an alpha-test setting in GS terms, and the second interface hands the same two values to its two state setters. **Where the first block goes:** its submit path ends in the three publishers read on [the handshake page](../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md) (UQ-211), which store an address, a count and `0x100` into one cell and hand the buffer to nothing; the staging pointer they copy through has no reader but themselves, and every function that references the ring descriptors writes to them. Within what was read, nothing consumes it.

**The second interface is an immediate-mode batcher on the singleton `[01F811E8]`, and it is the one that ends in a draw object.** Each of the seven is a thin wrapper that fetches the singleton (`001B1C00`) and forwards: `00181560` begins (it clears `0x178` bytes of state at `+0x3930` and sets the current colour to `0x80, 0x80, 0x80, 0x80`, `001B1932`..`001B1950`); `001816F0(r, g, b, a)` stores the current colour at `+0x3A4C`..`+0x3A58`; `00181910` and `001816B0` forward the two state handles; `00181870` and `00181930` forward a mode and four small integers; `00181460(points, n)` turns a strip into a list - for each of the `n - 2` triangles it appends three 0x30-byte vertices (`001814A0`..`001814B2`) - into the current one of 64 batches of `0x58` bytes at `+0x2328` (index `+0x3928`), each batch owning a growable run of 0x30-byte vertices at `+0x38`; and `00181330` flushes: for every batch up to the current index it takes `0x238` bytes from the ring arena at `[01F7F4C0]`, constructs an object whose vtable's RTTI is **`DynGeoTextureInstance`** (`001B042A`..`001B0456`), and drives it through its virtual interface - first the vertex count, `(end - begin) / 0x30`, then the batch's two leading qwords when the first is non-null (`001B048C`..`001B04D0`) - the family set out on [the DynGeo page](../16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md).

**So the rectangle is described twice and drawn once.** The PS2 description is still assembled, faithfully enough to decode, and then abandoned at a register kick with no hardware behind it; the batcher is the live path. Static. *Bound:* 'nothing consumes it' rests on rip-relative reference censuses of the ring descriptors, the staging pointer and the kick cell, not on a proof over every pointer in the process.

## 5. A call the decompilation renders as a no-op

```c
_guard_check_icall(&local_118, param_1, &local_158, 4);
```

**`0016D6A0` is a three-byte `ret`** — the address `/OPT:ICF` folded roughly 273 empty bodies onto,
and the one the disabled CFG stub occupies (register question BQ-27). Taken literally this call does
nothing.

**But `local_118`, `local_108`, `local_f8` and `local_e8` are read immediately afterwards** as the
four transformed points and written into the vertex records. **Something wrote them.**

> **The reading is that this is MSVC's CFG-guarded indirect call** — `call __guard_check_icall_fptr`
> followed by `call rax` — with the decompiler showing the guard and dropping the real call, and
> attributing the guard's arguments to it. **The four output points are produced by an indirect call
> whose target this document has not resolved.**
>
> **CORRECTED 2026-09-18 (FABLE): there is no dropped indirect call.** The function's complete call list is one direct `call 0016D6A0` (`002DBEA5`), `00248EB0`, `00248E10`, `00202B70` twice and the seven second-interface wrappers - no `call` through a register or memory anywhere in the body. `0016D6A0` here is not a guard in front of something: it is the callee, an empty function folded onto the shared `ret 0`. So nothing writes the four output points on this path; they feed only the first back-end's packet, which section 4 shows nobody consumes, while the live path gets its corners from `00202B70`. The same shape, with the same five-argument signature, is on [the glyph page](Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md) under UQ-365.
>
> **What is not claimed is that the transform does nothing.** A literal reading of the decompilation
> says exactly that, and the four values it produces are used four instructions later. **When a
> decompilation says a value comes from a function that returns immediately, the decompilation is
> what is wrong.**

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the input really `x, y, w, h` rather than two corners? | Corners 1 and 3 are `param_2[2] + param_2[0]`, corners 2 and 3 are `param_2[3] + param_2[1]`. **Both later fields are added to the earlier ones**, which is width and height, not a second point. |
| Is `>> 7` really a divide by 128 and not a bit-field extract? | It is applied to the **product** of a colour byte and a signed brightness (`imul` then `sar`, `002DBEBF`–`002DBEC2`), and the result is stored as a byte. **A product then a shift is a fixed-point multiply.** |
| Does the fourth channel really use a different field, or did the decompiler duplicate a variable? | `002DBEE4  movsx ecx, word ptr [rbx + 0x58]` **reloads `ecx` between the third and fourth multiply**, in the instruction stream. Two fields, read four instructions apart. |
| Do three channels really use `+0x5A` and one `+0x58`? | Three `CONCAT` terms take `iVar8`, itself `(short)context[0x5A]`; the fourth takes `(short)context[0x58]` directly. **Four terms, two source fields.** |
| Are the two back-ends really both emitting, or is one a state query? | Both take the **same two handles** and both terminate in a four-element submission — `local_1a0[9] = 4` in the first, `FUN_00181460(&points, 4)` in the second. |
| Could `002DBDD0` be a vertex helper rather than a draw? | It advances a command cursor by `0x90` and calls a submit pair (`00248EB0` … `00248E10`, then `00181460` … `00181330`). **It ends the work rather than handing it on.** |
| Is `0016D6A0` really the folded `ret`? | Its identity is established in the register (BQ-27) and in the exception-handling document; **this document does not re-derive it** and does not rest on it beyond noting the call cannot be what it appears. |

## 7. What this document does not claim

The target of the indirect call in §5. What `00202B70` computes beyond dividing by the `w` it
returns. What the two command words `0x1000000000000003` and `0x1022400000008004` encode. What
`context + 0x70` holds — it becomes the third component of every vertex. ~~Which of the two back-ends
actually reaches the hardware, or whether both do. What `00181330`, `00181460`, `00181560`,
`001816B0`, `00181870`, `00181910` and `00181930` are individually~~ *(read 2026-09-18, end of section 4; what the mode
of `00181870` and the four integers of `00181930` select is still not claimed, and the two command words are decoded there too).*

## 8. Where it sits

Seven callers: `00241D40`, `002B8EE0`, `002BCA70`, `002BCB00`, `002C9120`, `002C9570`, `003C32B0`.
**Three of them — `002B8EE0`, `002BCB00` and this function — were residual cluster 3** in
[the unresolved 158](the-unresolved-158.md), 6,775 bytes total; all three are classified at GN161 (`Presentation.Icon.*`, `Presentation.Primitive.TintedRectangleQuadEmit`). **The cluster is a real call
cluster**: `002B8EE0` calls here twice, and `002BCB00` calls here as well.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named `002BCB00` only at its entry. The interior addresses below were read in the
shipping image.

| body | interior cite | what is there |
|---|---|---|
| `002BCB00` | `002BCE28` | `call sinf` — first of two sine calls; body stores `0209E5D8`/`0209E5DC` and ends through `002DD7E0`/`002DBDD0`, the rectangle draw path |

*(Pass 22 adjacency, 2026-09-14: `00241D40` — the rectangle body — calls `Audio` `00249C60`/
`00249CA0` and the `CoreRuntimeScheduling` yield `001EDEC0` (3 edges), and `00249CA0` is itself
called by `Script_VM_Native_Bridge` `00354EF0` (1). Even a leaf draw call defers to the scheduler
and touches shared accessor families; the crossings are the draw loop's environment, not a second
owner.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — CLIENT (5 edges through 3 of this page's functions).** The Save_Load_Settings layer reaches this page at `00249C60`, `001EDEC0`, `002DD7E0`. `FUN_00581930` is the worked example, read in full - it is a 110-byte step that asks for message `0xD1`, then stores its argument into `dword[+0xD8]` and hands `[+0xF0]` on; **1 of the 5 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction / Gameplay / Movement / Party — OUT-OF-SCOPE (4 edges through `00313DB0`).** `00313DB0` is a CombatAction-layer hub cited below as a caller of `002DEE70`, the `(0,0,-4)` trampoline into `001DBE90` — that call is itself the CombatAction edge the audit counts. Its remaining edges — Gameplay callee `0030D9A0`, Movement caller `00234520`, Party callee `0031B7E0` — are that shared hub's own fan-in/fan-out; the page claims the rectangle draw path, not every layer one of its callers touches. (SWE2-EC7, 2026-09-20.)


**Presentation — CLIENT and SERVICE (SWE2-EC7-169, 279 edges).** `003C6140`'s caller
`003C34E0` and the packet submit `00248EB0`/`00181330` are called from the
presentation layer (`002DBDD0`, `003C2E60`, `00274CB0`, `002AFDC0` among 279 edges),
and `003C34E0` itself calls `003C2870`/`003C6140` — the colour publish rides the
shared submit helpers in both directions.

### Interior citation — frontier hub `00248EB0` (2026-09-18, SWE2-EC7)

`00248EB0` — 41 B, 12 callers: the submit-pair member `002DBDD0` runs.
`02EBEFF0`'s index ×3 strides the `02EBEFC0` table (0x18 records); it writes
the entry pointer to `[rcx]`, `[entry+8]` to `[rcx+8]`, and `[entry+8]+0x10`
to `[rcx+0x10]` ([`00248EC8`](../_index/ADDRESS-INDEX.md)) — a three-cell
cursor publish into the caller's command block.

## SWE2-EC7-63 update (2026-09-19) - `002BCA70`

`002BCA70` (144 B) is a coloured-rectangle caller - `002DBDD0` single call plus `01E0C1D8`/`01E0C1DC`. Interior anchor `002BCAB4` (a `002DBDD0` call).



## SWE2-EC7-64 update (2026-09-19) - `003C32B0`

`003C32B0` (140 B) is a coloured-rectangle caller - `002D8530`/`002DBDD0`/`002DD2F0`/`003C4070` plus `02B457F0`/`02B45820`. Interior anchor `003C32F9` (a `002DBDD0` call).


## SWE2-EC7-75 update (2026-09-19) - `002DD2F0` offset-transform consume measured

`002DD2F0` (90 B) builds a four-word stack vector -
`[rcx+0x50]+[rdx]`, `[rcx+0x52]+[rdx+2]`, `[rdx+4]`, `[rdx+6]` - runs
`00249EE0(rcx+0x48, vec)`, zeroes the qword when that returns 0, then
`00249FD0(vec)` consumes it - the offset-apply the rectangle drawers
share.
Interior anchor `002DD32D` (the `00249EE0` call).

## SWE2-EC7-85 update (2026-09-20) - `00403970` draw-command builder measured

`00403970` (579 B) is the textured-quad command builder the draw
callers run: `[r14+0x28]` bit `0x200` skips the source-rect fold,
else `002551B0`/`003C4AE0`/`00861EC0` fill the name buffer and the
`[[r14+0x40]+0x20]` `+0x14`/`+0x16` words become a /64 fixed-point
rect (with a >>3 arm); `003BEC50`/`003BECA0`/`003BE2D0` resolve the
three resource handles, then ~20 staged args (flags `r11d>>13`,
`ebp>>8`, the rect, the handles, the caller floats) tail into
`00403640(r12, ...)` - stack-cookie framed.
Interior anchor `00403B8A` (the `00403640` call).

## SWE2-EC7-88 update (2026-09-20) - `003C4980` staged 0x40-record pack measured

`003C4980` (293 B) is the bounce-buffer copy the icon callers
run: `00248EB0(&desc)` opens the out record with a
`0`/`0x10000000`/`0x6C080018` header, then each of the two
source records (`rbx` then `rdi`, 0x40 apart in the output) has
its four vec4s staged through `022D8F30`..`022D8F60` and copied
into the destination - a two-block 0x40 pack ending in a tail
`002DD3C0`.
Interior anchor `003C4A95` (the `002DD3C0` tail).

## SWE2-EC7-98 update (2026-09-20) - `002DEE70` measured

`002DEE70` (13 B) is the fixed-arguments trampoline
`00228C70`, `00313DB0` and `00354EF0` call: `ecx = 0`,
`edx = 0`, `r8d = -4`, then tail `jmp 001DBE90` - the
(0,0,-4)-specialization of the shared draw helper.
Interior anchor `002DEE78` (the `001DBE90` tail jmp).

## SWE2-EC7-99 update (2026-09-20) - `002DD550` measured

`002DD550` (113 B) is the slot publish `003C4070` and
`003C4AB0` call: the `02EBEFF0` index picks a 24-stride
`02EBEFC0` entry, `0x10000000` stamps both tag dwords of
the entry's `+8` record, and `0016D6A0` runs twice around
the `and rcx, -0x10` alignment fixup that extends
`[rdi+8]` before `003A1DB0` submits - the same publish
idiom `002D9B00`'s count-8 arm runs.
Interior anchor `002DD584` (the first `0x10000000` store).

## SWE2-EC7-110 update (2026-09-20) - `001B0100` measured

`001B0100` (132 B) is the
slot-array reset `001B0190`,
`001B03D0` and `001B1910`
run: `edx` walks
`0..dword[+0x3928]` bounded
`<= 0x3F`, and each 0x58
record at `rcx + 0x2328 +
edx * 0x58` resets -
`[+0x40]` pulls `[+0x38]`,
`+0`/`+8`/`+0x20`/`+0x1C`/
`+0x28` zero, `+0x10`/`+0x14`/
`+0x2C`/`+0x30` latch 1. A
negative or exhausted count
still writes `+0x3928` = -1,
which is also the early-out
store when `dword[+0x3928]`
started negative.
Interior anchor `001B0112`
(the `cmp edx, 0x3F` slot
bound).

`003C6140` (299 B) is the colour-pair emit `003C34E0` calls: `sword[rdx+0x58]` and `sword[rdx+0x5A]` scale the eight constant bytes at `01EFE370`..`01EFE377` (`imul` + `sar 7` per channel) into two RGBA quads; `00248EB0` consumes the first quad, then both write as four dwords each to `r14`'s `[+0x10]` cursor, advancing it `0x10` twice - the rectangle's per-vertex colour publish.

Interior anchor `003C61F6` (function `003C6140`).

`002B9BE0` (143 B) is the lazy singleton-pair installer for this page's `002BCA70`/`002BC9C0` callers: `0209E600` non-existent goes to `00244F50(0xC0, callback=002BCA70)` then `00246AD0` into the `0208EA20` manager; `0209E5F8` does the same with `002BC9C0`/0xC8 and takes `0209E5F0`'s `+0x190` into its `+0xC0` before registering - the two-slot deferred construction the rectangle family shares.

Interior anchor `002B9BFD` (function `002B9BE0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Input — MECHANICAL, 3 edges.** `00228C70` calls `001E0FB0`, `0035F150`; `00313DB0` calls `00226BE0`.

**InputGameplay — MECHANICAL, 1 edge.** `00313DB0` calls `00313A00`.

**Script_VM_Native_Bridge — MECHANICAL, 2 edges.** `00249CA0` is called by `00354EF0`; `002DEE70` is called by `00354EF0`.

**UI — MECHANICAL, 62 edges.** `002DD7E0` is called by `00280DE0`, `0028B140`, `002986E0`, `002A86A0` and 16 more; `001EDEC0` is called by `00252030`, `00276D30`, `0027C870`, `00299090` and 9 more; `002D9B00` is called by `002435C0`, `00243C00`, `0055AB20`, `0055AE80` and 1 more; `00249EE0` is called by `002D2600`, `002D28E0`, `00367AA0`, `003EE420`; `002D8530` is called by `00243860`, `003EE420`, `005599D0`; `00249FD0` is called by `00243860`, `005599D0`; `002551B0` is called by `003C5410`, `003C5E50`; `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is called by `002AC5F0`, `002AF960`; `00181330` is called by `002A0440`; `00181560` is called by `002A0440`; `001816B0` is called by `002A0440`; `00181870` is called by `002A0440`; `00181910` is called by `002A0440`; `00228C70` calls `0029DBE0`; `00248EB0` is called by `002A0440`; `00249CA0` is called by `00252030`; `002DD2F0` is called by `003EE420`; `003BE2D0` is called by `00402000`; `003C4070` calls `0035D320`.

**WorldAreaField — MECHANICAL, 2 edges.** `00313DB0` calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`); `003C4070` calls `00377780`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
