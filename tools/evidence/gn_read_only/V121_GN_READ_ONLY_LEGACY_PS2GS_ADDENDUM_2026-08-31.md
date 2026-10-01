# V121 GN — READ-ONLY LEGACY PS2 GS ADDENDUM — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Intended mutation parent:** GM160 recovery-transfer GZF  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Purpose / fencing

This addendum extends the existing GN read-only evidence for unresolved function:

`002F7380`

It records stronger exact-executable proof that the routine is part of FFXII's retained **PlayStation 2 Graphics Synthesizer (GS) texture/local-memory compatibility layer**.

It does **not** mutate the GM160 recovery-transfer GZF. The physical recovery-transfer GZF is still not exposed in the current execution filesystem, so no exact-current-parent mutation, whole-project diff, `PACK_PASS`, or fresh-reopen certification is claimed.

Official persistence-certified state remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

The handoff's certified residual SHA remains:

`fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a`

---

# 1. Refined proposed row

## `002F7380`

### Strongest current read-only CodeDomain proposal

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Previous conservative forms were:

- `Presentation.Rendering.ImageMipStorageBudgetAndReferenceSlotTableRebuild`
- `Presentation.LegacyPS2GS.ImageMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

The new `TextureMip` wording is justified by exact PSM classification plus per-record mip-chain traversal; it is not merely an external architecture guess.

---

# 2. Exact PSM-family classifier — `00466220`

`00466220` is a 25-byte leaf helper.

**Exact code-byte SHA-256:**  
`98e5090ed1391efb7669635a776e4ae4251a1f6d35d72f5d164e06359625b864`

Exact logic:

```text
format = record[0]
result = 0

tmp = format - 0x14
if ((tmp & 0xE7) != 0):
    return 0

if (format != 0x1C):
    return 1

return 0
```

The accepted values are therefore **exactly**:

- `0x14`
- `0x24`
- `0x2C`

No other byte values pass.

Independent PS2 SDK documentation identifies those literal values as:

- `0x14` — `GS_PSM_4` — 4-bit palettized
- `0x24` — `GS_PSM_4HL`
- `0x2C` — `GS_PSM_4HH`

Thus this FFXII helper is mechanically a classifier for the **GS 4-bit indexed texture PSM family**.

Inside `002F7380`, this classifier controls a per-image accounting contribution:

- accepted 4-bit GS texture formats contribute **1**
- other source-image formats contribute **4**

The exact authored purpose of this 1-versus-4 accounting factor is **not** yet established. It must not be renamed as CLUT count, block count, bandwidth, palette size, or another designer-facing metric without further proof.

---

# 3. Internal GS page geometry — `003A1E50`

`00466190` computes each source texture's complete mip-chain storage by repeatedly calling `003A1E50(width, height, format)` while halving both dimensions.

The executable's exception range truncates this helper too early for semantic use. Complete control-flow reconstruction from the executable shows:

- executable code: `003A1E50..003A1EDF`
- exact code length: **144 bytes**
- exact code-byte SHA-256:  
  `b5ee1026b95353aab9cb2f65fc6cfe0538dc43595f8b5ccf308530931a2cf8a1`

The helper uses:
- a four-target jump table at `003A1EE0`
- a 43-byte PSM dispatch table at `003A1EF0`

Exact jump-table SHA-256:
`a5e5bb0ac6cdc19113f908809d8745d9fc180958428a23e9fa9668ed206c2fde`

Exact 43-byte dispatch-table SHA-256:
`5c3b19613a65f2fe5f4a95db9693058a9426b5b4e48c90fba304fd4729ee6f8c`

## 3.1 Dispatch classes

The four exact target classes are:

### Class A — target `003A1EBA`
Initial geometry:
- first alignment: `0x20`
- second alignment: `0x40`
- divisor: `1`

Minimum page-sized result:
`32 * 64 / 1 = 2048` 32-bit words

### Class B — target `003A1E96`
Geometry becomes:
- first alignment: `0x40`
- second alignment: `0x40`
- divisor: `2`

Minimum page-sized result:
`64 * 64 / 2 = 2048` 32-bit words

### Class C — target `003A1E9E`
Geometry becomes:
- first alignment: `0x40`
- second alignment: `0x80`
- divisor: `4`

Minimum page-sized result:
`64 * 128 / 4 = 2048` 32-bit words

### Class D — target `003A1EAD`
Geometry becomes:
- first alignment: `0x80`
- second alignment: `0x80`
- divisor: `8`

Minimum page-sized result:
`128 * 128 / 8 = 2048` 32-bit words

All four classes therefore produce a minimum allocation unit of:

**2048 32-bit words = 8192 bytes = 8 KiB**

This is not inferred from exception metadata. It is direct arithmetic in the executable's complete control flow.

---

# 4. Literal PSM mapping encoded by FFXII

The dispatch-table index is:

`format - 2`

The exact executable table maps these notable literal formats:

| Literal format | Internal geometry class | Resulting minimum page | PS2 SDK identity |
|---|---|---:|---|
| `0x02` | 64×64 / 2 | 0x800 words | GS 16-bit |
| `0x0A` | 64×64 / 2 | 0x800 words | GS 16S |
| `0x13` | 64×128 / 4 | 0x800 words | GS 8-bit indexed |
| `0x14` | 128×128 / 8 | 0x800 words | GS 4-bit indexed |
| `0x1B` | 64×128 / 4 | 0x800 words | GS 8H |
| `0x24` | 128×128 / 8 | 0x800 words | GS 4HL |
| `0x2C` | 128×128 / 8 | 0x800 words | GS 4HH |

All un-specialized values in the supported switch range use the default 32×64 / 1 geometry.

This is a very strong internal fingerprint of **GS pixel-storage page geometry**.

The external PS2 SDK PSM constants match the same literal values exactly, but the classification decision rests on the FFXII executable's own dispatch/arithmetic.

---

# 5. GS arena capacity and page quantum

The exact Presentation helper `00467AA0` remains:

- length: **41 bytes**
- SHA-256:  
  `d77d46230de07f6632d0fa11543e69cb682b6ba0ca502da1dca0d59d54ab96df`

Its exact arithmetic is:

```text
used =
    3 * (globalWidth * globalHeight)
    + runtimeTotalA
    + runtimeTotalB

threshold =
    (0x1007FF - used) & 0xFFFFF800
```

This is best described carefully as:

**an 0x800-word-aligned remaining threshold derived from a 0x100000-word arena**

rather than loosely saying it simply “rounds the remaining capacity down.”

Because the internal GS sizing helper uses 32-bit-word units:

- `0x100000` words × 4 bytes = **4,194,304 bytes = 4 MiB**
- `0x800` words × 4 bytes = **8,192 bytes = 8 KiB**

The same executable therefore independently contains:

- an effective **4 MiB** image-memory arena;
- an **8 KiB** page/alignment quantum;
- literal GS PSM codes;
- exact GS per-PSM page geometry;
- literal GS image-transfer register IDs in sibling Presentation code.

This combination closes the mechanism-level identification as the retained **PS2 GS local-memory compatibility model**.

The exact identities of the three `width*height` reserved full-resolution surfaces remain unproven and are intentionally unnamed.

---

# 6. Existing internal GS transfer evidence

The existing GN follow-up already records two exact current-binary bodies tied to the same Presentation graphics state:

## `00244200`
- 455 bytes
- SHA-256:
  `da2156bb0ea503ce9cdfbbeb8def363acbc62f65c541d7d3249a078bf78fb49c`

It emits register IDs:

`0x50 → 0x51 → 0x52 → 0x53`

around the same legacy render-state family.

## `0039D200`
- 484 bytes
- SHA-256:
  `68dbc084f1cd3dec2ea807177902bcdc750167ceffbac6f58f45a5b8cdaa2652`

It consumes the same extent state, encodes width/height-like fields, computes a width/64 quantity, and manipulates 14-bit graphics-address fields.

Canonical V120 also independently promoted sibling `003A22A0` as a Presentation graphics-transfer command owner using the same transfer-register sequence.

PS2 SDK independently identifies:

- `0x50` = `BITBLTBUF`
- `0x51` = `TRXPOS`
- `0x52` = `TRXREG`
- `0x53` = `TRXDIR`

This is corroboration for the already-established executable family.

---

# 7. What `002F7380` now means mechanically

The strongest complete mechanism reconstruction is:

1. inspect the current legacy GS source-texture record bank;
2. compute each texture's complete mip-chain local-memory footprint using exact GS PSM page geometry;
3. compute aggregate budgeting metrics, including a special 1-versus-4 factor for the GS PSMT4/4HL/4HH family;
4. obtain the remaining 0x800-word-aligned threshold inside the effective 0x100000-word GS arena after fixed/runtime reservations;
5. traverse selected 0x30-byte reference descriptors and count how many live references reach each texture;
6. ignore textures referenced at most once;
7. for multiply referenced textures, admit the complete mip chain only while the cumulative accepted storage remains **strictly below** the threshold;
8. assign consecutive compact slot indices to admitted textures;
9. assign `-1` to rejected/unselected textures;
10. allocate and clear one **40-byte derived slot record** for each admitted texture.

This is a **legacy GS texture-mip local-memory admission and slot-table rebuild**.

It is not generic bookkeeping.

---

# 8. Cross-subsystem trigger remains separate from mechanism ownership

The trigger path remains:

`persisted/runtime selector`
→ `Movement resource-bank publication`
→ `Movement dirty transition`
→ `002F7380`
→ `LegacyPS2GS texture/local-memory table rebuild`

The Movement callback/dirty path is a trigger.

The complete body plus Presentation-local GS storage machinery establishes the callee's mechanism domain.

Do not infer:
- Movement ownership;
- Save/Load ownership;
- modern D3D11 GPU residency;
- network/multiplayer ownership.

---

# 9. Current proposed row after this addendum

**Address:** `002F7380`

**Read-only proposed CodeDomain:**

`Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

**Confidence:** strong mechanism-level semantic proposal.

This proposal still requires the physical GM160 recovery-transfer GZF before it may be applied.

Required later gate:
- fresh import exact parent;
- reproduce certified 160-current state;
- verify address is still unresolved;
- exact-current Ghidra body fence;
- exact expected-count mutation;
- complete immutable-drift diff;
- closed-file `PACK_PASS`;
- independent fresh reopen;
- regenerated post-mutation residual.

Until then:
**applied rows = 0**.

