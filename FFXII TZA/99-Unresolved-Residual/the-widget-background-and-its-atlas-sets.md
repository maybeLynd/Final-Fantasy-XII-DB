---
system: The widget background and its atlas sets
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: CodeDomain:Presentation.Widget
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
  last_pass_state: residual-cluster-5-repos-55
  crossref_clean: true
  reopened_count: 0
---

# The widget background and its atlas sets

**`00245170` and `002455A0` are the two background drawers** the
[widget tree draw pass](the-widget-tree-draw-pass.md) picks between on flag bit 8. **Both draw a
textured nine-patch from a shared atlas**; the second draws three of them, stacked.

**Cluster 5 is closed — all five members read**, `002DA2D0` last (§6b).

> **The first draft of this document opened by claiming the cluster was closed** while a member was
> still unread, three paragraphs above its own admission of that. It was corrected to *four of five*
> and has now been earned back. **A summary written before the limits section will contradict it**,
> and the check that caught it was reading the document top to bottom rather than trusting what it
> had just been written to say.

## 1. What the player sees

**The panel behind a menu is nine pieces of one texture.** Corners keep their size, edges stretch,
the middle fills — the same construction as the [gradient nine-patch](the-nine-patch-window-frame.md),
but sampling an authored image instead of a colour ramp.

**The richer of the two draws the panel three times over:**

- **a drop shadow, offset nine pixels down and right**, flat grey;
- **the panel itself**, tinted by a four-corner gradient;
- **a cap on top**, which **swaps to a shorter variant when the widget is too short to fit it.**

> **That last one is a real authored behaviour a modder can hit.** Shrink a widget below the cap's
> own height and the game does not squash the cap — **it substitutes a different nine-patch set.**

## 2. One nine-patch, nine consecutive atlas entries

Both functions share the loop:

```c
for (row = 0; row < 3; row++)
  for (col = 0; col < 3; col++) {
      entry = set + (row * 3 + col) * 8;        // nine 8-byte entries, consecutive
      u = entry[4] & 0xFFF;  v = (entry[4] >> 12) & 0xFFF;
      w = (col == 1) ? middle_w : u;            // the centre column stretches
      h = (row == 1) ? middle_h : v;
      FUN_002da7c0(dst, ctx, colours, packed_descriptor);
  }
```

**The middle extents come from the widget's own size minus the two fixed edges:**

```c
middle_w = node[+0x9C] - entry[2].u - entry[0].u + node[+0xA6];
middle_h = node[+0x9E] - entry[6].v - entry[0].v + node[+0xA7];
```

**and a cell with a non-positive middle extent is skipped**, so a widget narrower than its own border
simply loses its middle column rather than drawing it inside out.

## 3. The descriptor, and the two fields that looked dead

Each cell packs its source rectangle into the 64-bit value `002DA7C0` takes:

```c
descriptor = ((((v1 << 10 | v0) << 10 | u1) << 10 | u0) << 4) | 10;
```

| bits | field |
|---|---|
| 0–3 | tag, always `10` |
| 4–13 | `u0` — read by `002DA7C0` as `(d >> 4) & 0x3FF` |
| 14–23 | `u1` — read as `(d >> 0xE) & 0x3FF` |
| 24–33 | `v0` — extracted as `(d >> 0x18) & 0x3FF` |
| 34–43 | `v1` — extracted as `(d >> 0x22) & 0x3FF` |

> **[The widget tree draw pass](the-widget-tree-draw-pass.md) §6 reported the last two as extracted
> and then unused, and asked whether they were dead.** They are not: **they are the `v` pair of the
> same source rectangle**, and the producer here packs all four symmetrically. **The consumer of the
> `v` pair is still not visible in the decompilation** — but "dead" is now excluded, and that is a
> question answered by reading the *producer* rather than staring harder at the consumer.

## 4. The atlas holds several nine-patch sets

The index is two-level, as established in [the blinking icon](the-blinking-icon-and-its-atlas.md),
but the four call sites use **four different offsets from the same base**:

```c
set_index = *(ushort *)(atlas + 0x44 + atlas[0x44] * 2 + k);   // k = 0, 2, 6, 10
```

| `k` | used by |
|---:|---|
| 0 | `00245170`'s only pass, and `002455A0`'s third pass |
| 2 | `002455A0`'s main body |
| 6 | `002455A0`'s drop shadow |
| 10 | the **short-widget substitute** for the third pass |

> **So `+0x44` does not point at one index — it points at an array of nine-patch set ids**, and the
> UI picks among them by role. **The icon document read the same structure and saw only element 0**,
> because an icon needs one sprite and a panel needs four sets.

## 5. The colour tables decode exactly

`002455A0` fills four corner colours per cell from one of two authored tables, chosen by **flag bit
26**:

**`00915208` — 3 rows × 4 selectors, bit 26 clear:**

```
row 0:  0 0 0 0
row 1:  0 0 2 2
row 2:  2 2 2 2
```

**`00915218` — 9 cells × 4 selectors, bit 26 set**, indexed `col * 3 + row`:

```
col 0:  0 0 0 0 | 0 0 2 2 | 2 2 2 2
col 1:  0 1 0 1 | 0 1 2 3 | 2 3 2 3
col 2:  1 1 1 1 | 1 1 3 3 | 3 3 3 3
```

> **Read as corner ids `0 = top-left, 1 = top-right, 2 = bottom-left, 3 = bottom-right`, the second
> table is a bilinear sample of a four-corner gradient across nine cells** — corner cells take one
> colour, edge cells two, **and the centre cell takes all four in order.** The first table uses only
> `0` and `2`, which is the same construction collapsed to a **vertical-only** gradient.
>
> **The tables are not a lookup that had to be guessed at: they reproduce the arithmetic.** That is
> what makes the reading safe — a wrong assignment of the four ids would not produce `0 1 2 3` in the
> centre cell and constant corners everywhere else.

**Each selector is added to a per-style base** — `002DD7E0(style * 4 + 0x2C + selector)` — so a
widget's style index picks a block of four colours and the table picks among them.

## 6. `00245170` versus `002455A0`

| | `00245170` (bit 8 clear) | `002455A0` (bit 8 set) |
|---|---|---|
| passes | **one** | **three** |
| atlas | `0208EAA0`, or `0208EAB0` on flag bit 22 | `0208EA98` only |
| colour | one flat value, `0x80808080` when style < 2 | **per-cell from the two tables of §5** |
| shadow | none | **a pass offset `+9` on both axes** |
| primitive | `002DA7C0` | `002DA7C0` twice, then **`002DA2D0`** |
| size fallback | none | **swaps the atlas set when the widget is shorter than the cap** |

**This is the third one-routine-and-its-richer-variant pair in this subsystem**, after the two icon
drawers and the two nine-patch dispatchers. **The widget-tree document raised it as a pattern to
falsify first; it survived.**

> **What distinguishes this instance is that the variant is not a specialisation — it is a
> composition.** The icon twins differ in six measured details; these two differ in *how many times
> the same nine-patch runs*. **Calling both "one routine and its variant" flattens a real
> difference**, and the pattern should be stated as *the subsystem reuses whole passes*, not as
> *the subsystem duplicates functions.*

## 6b. The two primitives differ by one texel

`002DA2D0` is `002DA7C0` with three changes, and one of them is a convention:

| | `002DA7C0` | `002DA2D0` |
|---|---|---|
| descriptor | **passed in** by the caller (§3) | **built internally** from the source rect |
| far edges | `u0 + w`, `v0 + h` — **exclusive** | `u0 + w - 1`, `v0 + h - 1` — **inclusive** |
| unpack mode | `descriptor & 3` | the literal **`2`** |
| per-vertex flags | not written | **written into all four vertices** |

```asm
002DA302  movsx r14, word ptr [r9]        ; u0   -- signed loads
002DA309  movsx esi, word ptr [r9 + 0x6]  ; h
002DA30E  movsx edi, word ptr [r9 + 0x4]  ; w
002DA313  add   esi, r15d                 ; v0 + h
002DA31D  add   edi, r14d                 ; u0 + w
002DA337  lea   ebx, [rdi + -0x1]         ; u1 = u0 + w - 1   <- the inclusive edge
002DA34B  mov   qword ptr [rdx + 0x8], 0x8
002DA357  lea   eax, [rsi + -0x1]         ; v1 = v0 + h - 1   <- and the other
002DA35D  shl   rcx, 0xa
002DA361  or    rcx, r15
002DA367  shl   rcx, 0xa                  ; the 10-bit packing
002DA36B  or    rcx, rax
```

> **Two source-rectangle conventions live in one subsystem**, and they differ by exactly one texel on
> each far edge. **A mod that copies coordinates from a `002DA7C0` call site into a `002DA2D0` one —
> or the reverse — is off by one**, which is the sort of error that shows as a hairline seam rather
> than as anything obviously broken.

**The filtering rule is identical in both** — `src.w != dst.w || src.h != dst.h` sets bit 1 — so the
[widget tree draw pass](the-widget-tree-draw-pass.md) §6 finding holds across the pair rather than
in one primitive.

## 7. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Are the nine atlas entries really consecutive? | `set + (row * 3 + col) * 8` with no indirection between. **Nine entries, eight bytes each, in order.** |
| Is `+9` really a shadow offset, or a coincidence of two constants? | Both axes take `node[+0xA6] + 9` and `node[+0xA7] + 9` where the other two passes take the same fields without the addend. **Same constant, both axes, one pass.** |
| Do the colour tables really encode a bilinear gradient? | The centre cell of the 9-entry table is `0 1 2 3` — **all four ids, in order** — and the four corner cells are constant. **No other assignment of ids to corners produces that.** |
| Is the third pass's swap really about size? | The guard is `available_height < (entry[+0x1C] >> 12) & 0xFFF` — **the widget's remaining height against the entry's own v extent** — and the branch loads a different set id. |
| Is the `-1` in `002DA2D0` a real convention difference or a decompiler artifact? | **Two separate `lea reg, [reg - 1]` instructions** at `002DA337` and `002DA357`, one per axis, in the instruction stream — plus a third occurrence in the `00181890(1, 2, u0, u1 - 1)` call. `002DA7C0`'s callers show none. |
| Are the source-rect fields signed? | All three loads are `movsx` (`002DA302`, `002DA309`, `002DA30E`). **Signed**, which matters because a negative extent is what the nine-patch document's corner flip relies on. |
| Could `002455A0` be calling `00245170` rather than repeating it? | Neither appears in the other's call edges. **`002455A0` contains its own three loops.** |
| Is `+0x44` an array or did this document mis-read one index four ways? | Four call sites use `+0x44`, `+0x46`, `+0x4A` and `+0x4E` against the same computed base. **Four distinct displacements, one base expression.** |

## 8. What this document does not claim

What the three atlases `0208EA98`, `0208EAA0` and `0208EAB0` contain, or what flag bit 22 selects
between the latter two. What `002DAC70`, `002DAF30`, `002DD4B0` and `002DD7B0` do — `002DD7B0` is
called with the same style-derived index as the palette and its result is used as a **bit**, so it is
some per-style boolean, and that is as far as this goes. What the style index at `node + 0xA3`
enumerates. **Why the two primitives use different edge conventions** — §6b establishes that they do, not why.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE, 61 edges.** Cited background functions are called by Presentation bodies of 2,232 bytes (7), 927 bytes (6), 926 bytes (4), 783 bytes (3) and 1,967 bytes (2). They call Presentation bodies of 1,193 and 1,262 bytes and `RenderCommand_SubmitCurrentBufferAndSwap`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — CLIENT.** `FUN_00581930`, owned by that layer, calls `002DD7E0` on this page. That caller is a 110-byte step that asks for message `0xD1`, then stores its argument into `dword[+0xD8]` and hands `[+0xF0]` on; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## Interior citation — frontier hub `00181890` (2026-09-18, SWE2-EC7)

`00181890` — 92 B, 6 A-measured callers; the argument adapter in front of `001B22F0`.
Interior verified: `001B1C00()` supplies the shared row source (`001818AE`), the caller's
four args become `rdx/r8d/r9d` and three stack slots repack the caller's stack args
(`001818B9`–`001818CE`), and the `call 001B22F0` at [`001818D2`](../_index/ADDRESS-INDEX.md) runs the real
draw. Pure marshalling — no state touched.

**CoreRuntimeScheduling — CROSSING.** `0017D4C0`, owned by that layer (the startup/input-category
parse dispatcher on [the per-frame gate page](../00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md)),
calls `001B1C00` — the shared row-source getter this adapter consults — and Resource's
`001DB1E0`/`001A11B0` on its resource-loading leg (already itemised on that page). The
crossing is that layer's parse path asking for the same row table, not this page owning
anything there.


### Interior citation — frontier hub `002DAF30` (2026-09-18, SWE2-EC7)

`002DAF30` — 324 B, 7 callers: the `0215E6D0`-gated quad-vec4 stage named in
§-open list. `02EBEFF0` x3 strides the `02EBEFC0` table (the `00248EB0` idiom,
`+0x20` variant); four `movups` lanes copy `rdx`'s 64 B into the `022D8F30..60`
globals and onto the cursor record at
[`002DAF74`](../_index/ADDRESS-INDEX.md), cursor advancing `0x40`; then
`[rdx+0x88]` plus a `0x14` tag append the trailer record. A matrix publish
into the shared block the readers poll.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**CoreRuntimeScheduling — MECHANICAL, 7 edges.** `0017D4C0` calls `001A14E0`, `001DB500`, `0022A0B0`; `0017D4C0` is called by `0017D000`; `001A11B0` is called by `0017D4C0`; `001B1C00` is called by `0017D4C0`; `001DB1E0` is called by `0017D4C0`.

**Input — MECHANICAL, 1 edge.** `0017D4C0` calls `InputManager_CreateSingleton` (`00198750`).

**Resource — MECHANICAL, 3 edges.** `0017D4C0` calls `001A11B0`, `001DB1E0`; `001A11B0` calls `0019F620`.

**UI — MECHANICAL, 24 edges.** `002DD7E0` is called by `00280DE0`, `0028B140`, `002986E0`, `002A86A0` and 16 more; `00181890` is called by `002A0440`, `002D8D40`, `002D9380`; `00248EB0` is called by `002A0440`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
