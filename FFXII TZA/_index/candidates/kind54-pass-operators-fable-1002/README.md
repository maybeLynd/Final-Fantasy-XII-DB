# Kind-`0x54` per-pass UV operators and the triangle clipper `00521450` (FABLE, 2026-10-02)

The question comes from [effect-mesh-records-kind-54.md](../../../17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md)
§8, which ends the SD-140 answer with: "What stays open is the uncharacterised pass operators
(`0043E7B0`/`00434630`/`00434760`/`00396F20`/`00394B70`/`0043E840`) and the clipper `00521450` itself." The SD-140
record is [sd140-vertex-prep-kernel-0930](../sd140-vertex-prep-kernel-0930/README.md).

**Answer.** All seven are now read, and each is execution-proven against the shipped bodies.

- **The six operators.** They act on one per-corner float pair, the texture coordinate (UV), between the `+0x2C` copy
  and the ST step.
  - `00396F20` gathers a pair from the per-normal table.
  - `00394B70` adds a screen-position term.
  - `0043E7B0` swaps the two halves of the pair.
  - `00434630` applies `offset + uv·scale`.
  - `00434760` applies `offset + uv·scale` and then swaps.
  - `0043E840` scales the pair about 0.5.
- **The clipper `00521450`.** It is a homogeneous-space Sutherland–Hodgman triangle clipper against
  `|x|, |y|, |z| ≤ |w|`. It interpolates every field of the vertex linearly, and it returns the clipped polygon's
  vertex count. A count of 0 drops the triangle.

The checker is `k54_ops.py`. Its output, [`k54_ops.out`](k54_ops.out), ends `CHECKS 34  FAILS 0`. It uses no stubs.

## Instruments

- **Static.** `txt(addr)` compares the exact capstone text at every cited site, and `ripref(addr)` resolves
  rip-relative operands.
- **Raw rel32 index (A0).** A scan of every `E8` / `E9` / `0F 8x` in each executable section finds every direct site
  into the seven functions and into `00521BB0`. It finds only `call`s, and it agrees with `retool.py callers`, which
  also finds no rip-relative reference to any of them. Indirect calls are not covered by this scan.
- **Execution.** This uses SD-140's Unicorn harness `sd140_emu.py`, imported from the sibling folder rather than
  copied.
  - The local `call()` enters each function with `rsp ≡ 8 (mod 16)`, as a real `call` leaves it. This keeps the
    clipper's `movaps` spills aligned.
  - Each **E** check compares the native output with a float32 Python model over seeded trials (`random.Random(54)`).
    **The model is the claim and the native run is the control.**
  - Each **N** check scores a deliberately wrong expectation against the same native outputs. It passes only if that
    expectation is rejected.

## Controls

- **P1 (positive, execution).** This harness recovers SD-140's established kernel formula. `00432300` gives
  `min(255, e·c >> 7)` on 972 bytes, and the `>> 8` rival misses 960 of them.
- **P2 (positive, static).** The reader recovers call sites that the published record already cites:
  - SD-140 A7's clip call `004392AE call 0x521450`, with its `00431D30` / `003AFDD0` carriers;
  - BI-3b's `00435AF6 mov ecx, dword ptr [rsi + 0x174]` before the `00396F20` call at `00435B15`.
- **N1–N7 (wrong expectations that must fail).** Each one fails:
  - N1: a plain copy for `0043E7B0` differs in 40 of 40 trials.
  - N2: exchanging the offset and scale roles in `00434630` gives 388 misses.
  - N3: `00434760` without the swap gives 406 misses.
  - N4: `00396F20` copying the entry's second qword gives 685 misses.
  - N5: `00394B70` overwriting the pair gives 375 misses, and X feeding `v` gives 375 misses.
  - N6: `0043E840 = u·a` gives 578 misses, and a re-centring `+0.5` gives 578 misses.
  - N7: four clipper rivals are rejected. A clipper that always returns 3 (or only flags the triangle) differs in 330
    trials. Using `t = d1/(d0+d1)` differs in 296. A `2|w|` guard band differs in 241. Signed-`w` outcodes differ
    in 63.
- **E7 sensitivity.** The clipper check is bit-exact. Dropping only the colour lanes' ×10000 / ×0.0001 scaling from
  the model already makes it differ in 273 of 400 trials.

## Where the operators sit in a pass

The setting is the three draw paths `004355D0` (inline), `00437130` and `00438860`. For each pass `p`, after the
colour stage that SD-140 read, the UV goes through the steps below. The step order and the operands are static (A1–A5).
`004355D0` is the reference; `00437130` and `00438860` repeat the ladder (A5).

The staging slots follow SD-140's layout (A1):

- `[rsp+0x78]` is the **prepared UV**, the `+0x2C` copy or blend.
- `[rsp+0x50]` is the **per-pass UV′**.
- `[rsp+0x58]` is the lit per-normal table **L**.
- `r14` holds the screen vertices.

The steps:

1. **Source (pass byte `+0x1B0+p`, `004359E5`).**
   - **0, or 5 and above:** the source is the prepared UV (`00435A0A mov rdi, r9`).
   - **1 to 4:** L is refilled with a pass matrix (`02AEEA20` for values 1 and 3, `02AEEBF0` for 2 and 4). The refill
     runs through `00395CF0` / `00395780` for value 1, `003962F0` for value 2, and `00396A30` / `00396560` for values 3
     and 4. **`00396F20` then writes `UV′[k] = L[n_k].xy`**, where `n_k` is corner `k`'s `+0x174` normal index; the
     count is `+0x18` (`00435B15`, `00435BF4`).
   - **Value 2 only:** **`00394B70` then adds a screen-position term** from corner `k`'s `+0x170` screen vertex; the
     count is `+0x1A` (`00435B37`).
2. **Operator (pass byte `+0x1AC+p`, `00435BFE`).** Each operator reads the current source and writes UV′, with count
   `+0x1A`.
   - **1:** `0043E7B0` swaps (`00435C79`).
   - **2:** `00434630` applies `offset + uv·scale` with the 16-byte block `param + 0x150 + 16p` (`00435C5D`).
   - **3:** `00434760` applies the same block and then swaps (`00435C32`).
   - **Any other value:** no operator runs.
3. **Centre scale (`param + 0x1F2`, `00435C8D`).**
   - **Bit 0:** `0043E840` runs with the pass pair `param + 0x50 + 8p`, and that pair is then overwritten with
     (0.5, 0.5) (`00435CC5` / `00435CCD`).
   - **Bit 0 clear, bit 1 set:** `0043E840` runs with `(w, w)`, where `w = param + 0x1EC` (`00435CE7`–`00435CFA`).
     0.5 (from `01CEBB70`) is then added to each half of the pass pair (`00435D67` / `00435D6B`).
   - **Pass mode byte `+0x130+p` = 4, bit 0 clear, `004355D0` only:** the pair first becomes `(x / 1.15, y · 1.15)`
     (`00435D45` / `00435D49`, constant `00D1247C`). This happens before the bit-1 `+0.5`, or alone when bit 1 is also
     clear. The gate `0053DD10` is `mov eax, 1; ret` (A4b), so whenever mode 4 is reached the rewrite always runs.
     `00437130` and `00438860` have the 0.5 steps but not the 1.15 rewrite (A5).
4. **ST step.** This is SD-140 E5 / E7: `S, T = (uv + pass pair)·Q`, and the builders divide back by `Q`. On the clip
   path the UV′ pair is carried through the clipper as the vertex's `+0x20` qword first (A6).

Two facts follow from the operands:

- **No pass writes the prepared UV.** Every operator writes UV′ (A2–A4). `0043E840` runs in place only when its source
  is already UV′ (`00435CA1 cmp rdi, [rsp+0x78]`). So each pass starts again from the same `+0x2C` data.
- **The operators count with `+0x1A`, while the gather counts with `+0x18`.** The census has `+0x18 == +0x1A` in every
  record.

## Per function

### `0043E7B0`: per-pair swap — **READ**

- **Evidence.** The loop at `0043E7D0`–`0043E839` loads the source qword into the scratch cell `022D8F90`. It stores
  the low dword at `dst+4` (`0043E7F4`) and the high dword at `dst+0` (`0043E826`). The counter is `022D94A0`.
- **In.** `rcx` is the source pairs, `rdx` the destination, `r8d` the count.
- **Out.** `dst[i] = (src[i].v, src[i].u)`.
- **Execution (E1).** The native output is bit-exact with the model over 40 trials. The loop is a do-while, so a
  count of 0 still swaps one pair; callers pass `+0x1A ≥ 1`.
- **Callers on the kind-`0x54` path.** `00435C79`, `00437746` and `00438F24`, selected by `+0x1AC+p = 1`.
- **Other callers.** `00443C41` and `00444B05` are not on the kind-`0x54` path and were not read.

### `00434630`: per-pair affine — **READ**

- **Evidence.** The block `[r8]` is staged as `022D92F0` = (b0, b1, b2, b3) and `022D9300` = (b2, b3)
  (`0043463D`–`0043468A`). In the loop:
  - `x = b0·1.0 + u·b2` (`0043469F`–`004346D2`), where 1.0 is `01EF93FC`;
  - `y = b1·1.0 + v·b3` (`004346DE`–`0043470A`);
  - the qword is stored at `dst` (`0043473D`).
- **In.** `rcx` is the source, `rdx` the destination, `r8` = `param + 0x150 + 16p`, `r9d` the count.
- **Out.** `(b0 + u·b2, b1 + v·b3)`. The block's first pair is added and its second pair multiplies.
- **Execution (E2).** Bit-exact on 388 pairs.
- **Callers on the kind-`0x54` path.** `00435C5D`, `00437727` and `00438F07`, selected by `+0x1AC+p = 2`.
- **Inference.** That the first pair is a UV scroll and the second a UV tiling scale is a label read from the
  arithmetic. The authored source of `param + 0x150` was not read.

### `00434760`: affine, then swap — **READ**

- **Evidence.** It does the same arithmetic as `00434630` (`0043480F`–`0043487C`). It then stores the x result at
  `dst+4` (`0043489C`) and the y result at `dst+0` (`004348D0`).
- **Out.** `(b1 + v·b3, b0 + u·b2)`.
- **Execution (E3).** Bit-exact on 406 pairs.
- **Callers on the kind-`0x54` path.** `00435C32`, `004376FE` and `00438EE0`, selected by `+0x1AC+p = 3`.

### `00396F20`: gather by normal index — **READ**

- **Evidence.** For each corner, the routine reads a signed 16-bit index from the list (`00396F20`, `00396F92`). It
  forms `index·16 + table` (`00396F5A`–`00396F6D`) and copies that entry's first qword to the destination
  (`00396F7E`, `00396FAC`).
  - The loop ends when the counter equals the cell `022D8F10`, which is 0 in the image (`00396FB0`–`00396FBE`).
  - The table address is truncated to 32 bits (`movsxd r11, ecx`, `cdqe`), so it must lie below 4 GB.
- **In.** `rcx` is L (`[rsp+0x58]`), `rdx` the resolved `+0x174` normal-index list, `r8` UV′, `r9d` = `+0x18`.
- **Out.** `UV′[k] = (L[n_k].x, L[n_k].y)`.
- **Execution (E4).** Bit-exact on 685 corners. Reading the entry's z, w instead is rejected (N4).
- **Callers on the kind-`0x54` path.** There are two per path: `00435B15` / `00435BF4`, `004375E0` / `004376C7` and
  `00438DBA` / `00438EA2`.
- **Open (outside the seven).** What the refill routines `003962F0`, `00396A30`, `00396560`, `00395CF0` and `00395780`
  write into L's x and y. That decides what the gathered UV means; an environment-style mapping from a transformed
  normal is an **inference**.

### `00394B70`: screen-position term — **READ**

- **Evidence.** For each corner, the routine reads `X = u16 [table + 16·idx]` and `Y = u16 [+2]`, converts them, and
  multiplies by 1/16 (`008F30EC`) and by 1/512 (`008C5B30`). It subtracts 3.5 (`00D113E0`) from the X term and 3.5625
  (`00D113E4`) from the Y term, then **adds** both into the destination pair (`00394BD0`–`00394C1A`).
- **Loop shape.** The body is unrolled by four, with a tail at `00394D37`–`00394D8D`. A count below 1 writes nothing.
- **In.** `rcx` is the screen vertices (GS XYZ, `u16` 12.4 per SD-140), `rdx` the resolved `+0x170` position-index
  list, `r8` UV′, `r9d` = `+0x1A`.
- **Out.** `UV′[k] += ((X/16)/512 − 3.5, (Y/16)/512 − 3.5625)`.
- **Execution (E5).** Bit-exact on 375 corners, at counts 1–14 and 0. The overwrite rival and the X→`v` rival are both
  rejected (N5).
- **Callers on the kind-`0x54` path.** `00435B37`, `00437600` and `00438DDD`. It runs only for `+0x1B0+p = 2`, after
  the gather.
- **Inference.** `3.5·512 = 1792 = 2048 − 256` and `3.5625·512 = 1824 = 2048 − 224`. This is consistent with a
  512 × 448 frame centred at GS coordinate 2048, mapped to `u ∈ [0, 1]` and `v ∈ [0, 0.875]`: a screen-space texture
  coordinate added to the gathered one. The frame size is not read here.

### `0043E840`: scale about the centre — **READ**

- **Evidence.**
  - `[r8]` (a, b) is staged at `022D92F0`.
  - The immediate qword at `0043E84D` puts −0.5 in the low dword (the high dword is all ones and unused for the
    output). That −0.5 goes to `022D9300` / `022D9304`.
  - In the loop, `x = −0.5·a + u·a` (`0043E8FF`, `0043E91F`, `0043E93A`) and `y = −0.5·b + v·b` (`0043E90F`,
    `0043E942`, `0043E95A`). The result is stored at `dst` (`0043E98D`).
- **In.** `rcx` is the source, `rdx` the destination (the same as the source when in place), `r8` → (a, b), `r9d` =
  `+0x1A`.
- **Out.** `((u − 0.5)·a, (v − 0.5)·b)`.
- **Execution (E6).** Bit-exact on 578 pairs, half of them in place. The rivals `u·a` and the same result `+0.5` are
  rejected (N6).
- **Callers on the kind-`0x54` path.** There are four per path: `00435CAE` / `00435CC0` / `00435D0C` / `00435D1E`,
  `00437785` / `00437797` / `004377DB` / `004377ED`, and `00438F59` / `00438F77` / `00438FB6` / `00438FC7`.
- **Result with the caller's step 3.**
  - With bit 0, the emitted UV is `(u − 0.5)·a + 0.5`: a zoom about the texture centre by the authored pass pair. The
    pair is consumed as a scale and then overwritten with 0.5 in the parameter block.
  - With bit 1, it is `(u − 0.5)·w + 0.5 + pair`, with `w = param + 0x1EC`. SD-140 reads that field as the two-mesh
    blend weight in `00434CD0`.
  - Both pair rewrites write back into the parameter block. Whether the walk rebuilds the block for every draw was
    **not read**.

### `00521450`: homogeneous triangle clipper — **READ**

**Execution (E7).** The native routine is bit-exact with the model on the returned count and on all four 16-byte fields
of every output vertex, over 400 seeded triangles. The output counts are 0 in 115 trials, 3 in 70, 4 in 116, 5 in 71,
6 in 19 and 7 in 9. The plane table comes back unchanged.

**Inputs.**

- `rcx` is a 4×4 matrix.
- `rdx` is a vertex buffer of three 64-byte vertices. The routine needs `rdx + 0x800` bytes, as two 0x400-byte
  ping-pong halves.

**The 64-byte vertex, as `00438860` fills it (A6).**

| offset | contents |
|---|---|
| `+0` | source-space position, a float4 |
| `+0x10` | colour as four `float(byte)` lanes (`00431D30`) |
| `+0x20` | the corner's per-pass UV′ qword (textured sites) |
| `+0x30` | clip-space position, written by the clipper |

**The matrix.** At the kind-`0x54` sites it is `[rbp+0x30]` in `00438860`, composed in the prologue by `00397910`.
[CONTRACT-transform-primitives](../../../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md) names `00397910`
`ComposeTransforms`. The composition is first over `02AEEA20` and the parameter block, then over `02AEDDF0` (A7).
That the result is the element's world-to-clip matrix is an **inference**; the roles of `02AEDDF0` and `02AEEA20` were
not read here.

**Transform.** `clip = x·M0 + y·M1 + z·M2 + w·M3` for each input `+0` position, stored at `+0x30`
(`00521501`–`005218EB`).

**Outcode.** Each vertex gets six bits from its `+0x30` (`00521950`–`00521A86`), where `|w|` is taken by mask
(`00521981`):

| bit | condition |
|---|---|
| 1 | `x > |w|` |
| 2 | `−|w| > x` |
| 4 | `y > |w|` |
| 8 | `−|w| > y` |
| 0x10 | `z > |w|` |
| 0x20 | `−|w| > z` |

For each edge, the code is `(code_a << 6) | code_b`.

**Planes.** The plane table at `01F2C760` has six 16-byte entries of (sign float, edge mask, axis) (A9):

| order | plane | mask |
|---|---|---|
| 1 | `z ≥ −|w|` | `0x820` |
| 2 | `z ≤ |w|` | `0x410` |
| 3 | `y ≥ −|w|` | `0x208` |
| 4 | `y ≤ |w|` | `0x104` |
| 5 | `x ≥ −|w|` | `0x82` |
| 6 | `x ≤ |w|` | `0x41` |

The loop `r12d = 3 + 3` (`00521793`) runs the six passes. Each pass closes the polygon by copying vertex 0 to the end
(`00521913`), then handles each edge by its masked code (`00521A8C`–`00521B33`):

- **Masked code 0:** keep `a`.
- **Only `b` outside:** keep `a`, then add the split vertex.
- **Only `a` outside:** add the split vertex.
- **Both outside:** drop both.

After six swaps (`00521B40`–`00521B4D`), the result is back at `rdx`. The routine returns the count in `eax`
(`00521B6C`).

**Split (`00521BB0`, called only from `00521B26`).**

- `d = |c[axis] − s·w|` for each end of the edge, and `t = d_a / (d_a + d_b)`.
- The axis is chosen by rotating the scratch lanes `[plane+8]` times. That loop decrements the table's own `+8` field
  and restores it on exit (`0052227D`).
- Position, `+0x20` and clip are each computed as `a + t·(b − a)`.
- Colour gets the same lerp on lanes scaled by 10000.0 (`00902EF4`) and rescaled by 0.0001 (`01CEBB60`) afterwards.
- So **colour and UV are interpolated linearly in clip space**. SD-140 had listed that as an inference; it is now
  execution-proven.

**What it does not do.**

- No plane tests the sign of `w`: the outcodes compare against `|w|`, and the split uses signed `s·w`.
- E8 measures the consequence:
  - When all three corners have `w > 0`, every output vertex lies inside the box.
  - Across the 206 trials with a corner at `w ≤ 0`, 101 output vertices lie outside the box.
- Whether such triangles reach the clipper in play was **not measured**.
- There is no guard band; a 2|w| band is rejected (N7).

**How the caller uses the result (A6, sites `004392AE` and `0043B453`).**

- A count of 0 → the triangle is dropped (`004392B8` / `0043B462 je`).
- Otherwise, for each output vertex:
  - `+0` is re-projected by `0039A150`;
  - `+0x10` is packed back to bytes by `003AFDD0`;
  - `+0x20` is turned into ST by `0039B880`.
- An n-gon builder then emits `count` corners: `0043E440` / `0043D8F0` untextured, `0043DB90` / `0043DF80` textured.
- At these two sites the caller does not read the clipper's `+0x30`.
- All 18 `00438860` sites prepare exactly three corners (`00431D30` ×3 before each call). Quads therefore reach the
  clipper as triangles.

**Callers.**

- On the kind-`0x54` path: the 18 sites in `00438860`, from `004392AE` to `0043D6CD` (A0). They are entered when a
  projected corner comes back zero (SD-140 A7).
- Elsewhere: `00501E91`, `00501FA8`, `00502985` and `00502AE0`, in the authored builds `00501A50` / `00502280`. These
  were not read here.

## Is the page's residue answered?

**Yes for all seven.** Each one's transform, operands, constants and kind-`0x54` call sites are read, and each is
execution-proven, bit-exact, with wrong expectations rejected.

What remains open is outside the seven:

- **What the L-refill routines write into L.** These are `003962F0`, `00396A30`, `00396560`, `00395CF0` and
  `00395780`. It decides what the UVs regenerated for pass byte `+0x1B0` mean.
- **The roles of the two clip-matrix globals.**
- **Whether `w ≤ 0` triangles reach the clipper in play.**
- **Whether the walk rebuilds the pass pair after the `+0x1F2` write-back.**

## Proposed replacement sentence (page §8)

Replace "What stays open is the uncharacterised pass operators
(`0043E7B0`/`00434630`/`00434760`/`00396F20`/`00394B70`/`0043E840`) and the clipper `00521450` itself." with:

The text below is Markdown source to paste into the page. Its link is relative to the page's folder
(`17-Presentation-Rendering/Effect-File-Formats/`), so it is shown here as source rather than as a live link.

```markdown
The pass operators are read and execution-proven (FABLE, 2026-10-02,
kind54-pass-operators-fable-1002 (`_index/candidates/kind54-pass-operators-fable-1002/`)). Each one
writes the per-pass UV copy, never the prepared one.

- Pass byte `+0x1B0` can replace the UV with the first two floats of the lit per-normal table at each corner's normal
  index (`00396F20`). For value 2 it also adds a screen-position term `((X/16)/512 − 3.5, (Y/16)/512 − 3.5625)`
  (`00394B70`).
- Byte `+0x1AC` then swaps the pair (`0043E7B0`), applies `offset + uv·scale` from `param + 0x150 + 16p` (`00434630`),
  or does both (`00434760`).
- `param + 0x1F2` bits 0 and 1 scale the pair about 0.5 (`0043E840`). The scale is the pass pair (which is then reset
  to 0.5) or `param + 0x1EC`.

The clipper `00521450` clips each triangle in homogeneous space against `|x|, |y|, |z| ≤ |w|`, using six planes
(Sutherland–Hodgman). It interpolates position, colour, UV and clip position linearly and returns the polygon's vertex
count. A count of 0 drops the triangle; any other count is re-projected and emitted as an n-gon.

What stays open is what the lighting routines write into the per-normal table, which decides what the regenerated UVs
mean.
```

## Contradictions with published text (reported, not edited)

- **X1.** [the-two-transform-primitives.md](../../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)
  describes these bodies by their scratch traffic and gives them the wrong roles:
  - "SWE2-EC7-83 update": `0043E7B0` is "a counted copy driving the global ring", and `00434760` / `00434630` are
    "bank-transform" passes.
  - The later blocks call `0043E840` "a call-free publish of the workbench header", `00396F20` an "index scatter" and
    `00394B70` "the weight scatter".

  That section also cites `02EB87xx`–`02EB94xx` cells. **The bodies address `022D8F90` / `022D92F0` / `022D94A0`
  (X1).** By E1–E6 they are a swap, an affine map, an affine map with a swap, a centre scale, a gather and a
  screen-term add.
- **X2.** [how-an-authored-number-gets-its-randomness.md](../../../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md),
  "SWE2-EC7-83 update", calls `00521450` "call-free … a pure-SSE 4x4 transform fold with no calls". **It calls
  `00521BB0` at `00521B26` (X2, A0).** The 4×4 transform is only its prologue; the body is the six-plane clipper (E7).
- **Agreement.** [clamping-a-point-into-a-volume.md](../../../06-Movement-And-Navigation/clamping-a-point-into-a-volume.md)
  describes `00521BB0` as blending "two 64-byte records into a third", with the weight "a ratio of one component of two
  vectors" chosen by lane rotation. That matches E7's split, `t = d_a / (d_a + d_b)` on the plane's axis.
- **SD-140 record.** "The clipper `00521450` itself was not executed. That it interpolates both linearly is
  inference." It is now executed, and the interpolation is linear (E7).

## Files

- `k54_ops.py` is the checker: S1, P1–P2, A0–A9, K1–K3, E1–E8, N1–N7 and X1–X2. It needs `unicorn`, `pefile`,
  `numpy`, `retool.py` and SD-140's `sd140_emu.py`, plus the certified image at `Database/Tools/work/exe/FFXII_TZA.exe`.
- [`k54_ops.out`](k54_ops.out) is its output, ending `CHECKS 34  FAILS 0`.

Reproduce with `python -B k54_ops.py`.

run: k54_ops.py at 5eacddf63
