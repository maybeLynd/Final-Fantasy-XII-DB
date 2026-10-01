# V121 GN — READ-ONLY FOLLOW-UP / SEMANTIC REFINEMENT — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Intended physical parent:** GM160 recovery-transfer GZF  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Fencing and accounting

This follow-up refines the two GN read-only candidates previously preserved in:

`V121_GN_READ_ONLY_PROPOSED_ROWS_2026-08-31.md`

It does **not** mutate the GM160 recovery-transfer GZF. The physical GM160 GZF is not exposed in the current execution filesystem, so exact-current-parent enrichment, mutation, whole-project diff, closed-file packing and fresh-reopen certification cannot honestly be claimed here.

The official persistence-certified state therefore remains unchanged:

- internal functions: **38,161**
- explicitly accounted: **38,001**
- unresolved: **160**
- explicit coverage: **99.58072%**
- cross-layer overlap: **0**
- certified current residual address-list SHA-256: `fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a`

The two functions below are the only GM160 unresolved functions known from the certified hard-residual scan to have direct PrimaryOwner references. Those owner references are not used as semantic proof.

No PE `.pdata`, `.xdata`, unwind, EH or IP-to-state metadata is used as semantic evidence.

---

# 1. Refined GN row — `00313A00`

## Proposed V121 CodeDomain name

`InputGameplay.FieldBattleOperationInhibitMaskReconciliation`

**Previous conservative name:**  
`Runtime.ControlPolicy.FieldBattleOperationInhibitMaskReconciliation`

**Complete body:** 289 bytes  
**Exact authorized-EXE body SHA-256:**  
`c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246`

## 1.1 Exact mask mechanics

The complete body reconciles row 2 of a central 16-row × 32-bit inhibition/policy mask.

The exact sibling primitives establish bit direction:

- `002E1C20(row, bit)` — sets the requested bit in the selected row.
- `002E1CA0(row, bit)` — clears the requested bit in the selected row.
- `002E0FA0()` — OR-reduces all 16 rows into the effective aggregate mask.

`00313A00` explicitly reconciles row-2 bits:

`0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 20`

Most of these bits are selected according to whether global `02089350` is non-null.

Persisted V120 authority independently identifies `02089350` as the **CombatAction current-selected-BattleUnit state**, published by `00313DB0` and reset by WorldAreaField initialization. That establishes the input state but does **not** transfer CombatAction ownership to this function.

Bit 10 is selected independently from `00377C20`. The exact `00377C20` body resolves the current indexed field record and returns the high bit of a two-byte field. Canonical V120 places that helper in **WorldAreaField**. The authored/designer-facing meaning of that field bit remains intentionally unnamed.

Bit 1 additionally depends on `00253B90`. Its complete exact body is only a global-null predicate:

- zero return register;
- compare dword `01E0C2B8` against zero;
- set result when equal;
- return.

No designer-facing meaning is inferred for `01E0C2B8`.

When there is no selected BattleUnit and shared runtime/gameplay flag `02089340 & 0x40` is clear, the tail also derives a local gate value and reconciles a separate bit-5 gate through `002E1C40`.

## 1.2 Why the refined domain is InputGameplay

The earlier GN proposal conservatively called this a generic runtime control-policy reconciler. Later exact-current and canonical V120 evidence narrows the consumer domain.

Canonical V120 independently reconstructs:

`00253C70` — `InputGameplay_ArbitrateDigitalInputAndModalState`

- complete body: **1,599 bytes**
- exact-current body SHA-256: `e6309cd50d266650fbb78a725a5aaaefb69c656a51dffc87c8299f30c15fa093`
- canonical category: **FFXII.Input**

The aggregate mask reader `002E0FA0` is also preserved as an Input boundary/support mechanism. Its direct consumers repeatedly test individual aggregate bits as gameplay/input eligibility gates. Observed exact-body consumers include tests of bits 0, 4, 6, 9, 10, 18 and 21 across gameplay, UI and Presentation-facing paths.

The aggregate reader itself:

1. ORs the 16 policy rows into one effective mask;
2. applies a separate runtime predicate;
3. conditionally clears effective bit 19 before returning the final mask.

This is therefore not a save-state bitset or a local CombatAction flag bank. It is a centralized **InputGameplay operation-inhibition policy** assembled from multiple engine-state contributors.

`00313A00` specifically publishes the selected-BattleUnit/current-field contribution into row 2.

## 1.3 Refined decision

**STRONG READ-ONLY PROPOSAL.**

`00313A00` is best described as:

`InputGameplay.FieldBattleOperationInhibitMaskReconciliation`

It reconciles the field/battle contribution to the engine-wide InputGameplay inhibition mask from:

- current selected BattleUnit state;
- current field-record policy;
- an additional global-null predicate;
- shared gameplay flags.

### Explicit negative boundaries

Do not claim:

- CombatAction PrimaryOwner merely because current-selected-BattleUnit is an input;
- WorldAreaField PrimaryOwner merely because a field predicate is an input;
- exact player-facing action names for bits 0/1/2/.../20;
- exact meaning of `01E0C2B8`;
- save/load semantics.

This is a V121 **CodeDomain** proposal only.

---

# 2. Refined GN row — `002F7380`

## Proposed V121 CodeDomain name

`Presentation.LegacyPS2GS.ImageMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

**Previous conservative name:**  
`Presentation.Rendering.ImageMipStorageBudgetAndReferenceSlotTableRebuild`

**Complete body:** 723 bytes  
**Exact authorized-EXE body SHA-256:**  
`15594f6181100f7fa10ac8a770566d60b963e47c93176fd7d7f33152b3ac8583`

## 2.1 Exact source-image and mip-chain mechanics

The complete body destroys and rebuilds a derived table at object offsets `+0x218/+0x228`.

Its source bank uses **0x60-byte records**.

Exact helper `00466190`:

1. selects one 0x60-byte source image record;
2. reads a format-like code;
3. reads a mip-count byte, capped at 7;
4. reads two image dimensions;
5. calls `003A1E50(width, height, format)` for each level;
6. halves both dimensions between levels;
7. sums the complete mip-chain storage footprint.

Canonical V120 independently classifies `003A1E50` as a **pure graphics-format/mip storage-size calculation from dimensions/format**, with no PrimaryOwner credit.

The first pass through `002F7380`:

- computes the maximum single-image mip footprint;
- computes a weighted aggregate image metric;
- clears every record's derived reference/slot field;
- publishes the maximum and aggregate values through the canonical Presentation budget family.

## 2.2 Exact budget equation

The relevant Presentation helper bodies are exact-current-binary identities:

- `00467AA0` — 41 bytes — SHA-256  
  `d77d46230de07f6632d0fa11543e69cb682b6ba0ca502da1dca0d59d54ab96df`
- `00467AD0` — 42 bytes — SHA-256  
  `c058521b6bae9791dacaab042cd9be09db1dca0ceaf556592a056e4bb20d00ea`
- `00467B00` — 7 bytes — SHA-256  
  `5ac6e89921b8831b8b4845494f5600bb9a701091e3aba0ff936a22772e804ee6`
- `00467B10` — 7 bytes — SHA-256  
  `b4e6558740995b6f4f61c9fc8c283aa0d089802dd4ddf18b313352b62f55c509`

`00467AA0` computes the remaining image-memory budget as:

`0x1007FF - 3*(globalWidth*globalHeight) - maxSingleMipChain - weightedImageTotal`

and then rounds the result down with:

`& 0xFFFFF800`

The effective maximum aligned arena is therefore:

`0x100000` storage units

with an allocation/page quantum of:

`0x800` storage units.

Sibling initializer `00467AD0` seeds related arena policy with a `0x4000` baseline and a second quantity derived from the same `3*width*height` product divided by 64.

The exact designer-facing identities of the three reserved full-resolution surfaces are **not** established and are intentionally left unnamed.

## 2.3 Exact reference-count and slot-selection algorithm

`002F7380` then walks **0x30-byte reference descriptors** selected by the current dynamic mask.

For each source image reached directly or through its linked/continuation record, it increments the corresponding image reference count.

The final selection pass is exact:

- reference count `<= 1` → slot index `-1`;
- reference count `> 1` → calculate  
  `runningAcceptedMipStorage + currentFullMipStorage`;
- accept only when that new cumulative amount is **strictly less than** the remaining aligned budget;
- accepted images receive consecutive compact slot indices;
- rejected images receive slot `-1`;
- accepted images advance both running storage and selected-slot count.

When selected-slot count is nonzero, the routine:

- writes the count to `object+0x228`;
- allocates exactly `slot_count * 40` bytes;
- stores the pointer at `object+0x218`;
- zero-initializes every 40-byte slot record.

This is an actual bounded local-memory admission/slot-table rebuild, not a generic sorting or bookkeeping pass.

## 2.4 Why this is specifically the retained Legacy PS2 GS path

The same width/height state is consumed by exact graphics bodies that use the retained PlayStation 2 GS transfer vocabulary.

### Exact current body — `00244200`

- complete body: **455 bytes**
- SHA-256:  
  `da2156bb0ea503ce9cdfbbeb8def363acbc62f65c541d7d3249a078bf78fb49c`

The function reads the same graphics extents, serializes transfer records with register IDs:

`0x50 → 0x51 → 0x52 → 0x53`

and invokes canonical Presentation render-surface publication `0039D0C0`.

### Exact current body — `0039D200`

- complete body: **484 bytes**
- SHA-256:  
  `68dbc084f1cd3dec2ea807177902bcdc750167ceffbac6f58f45a5b8cdaa2652`

This function consumes the same width/height-like pair, encodes `(width-1)` and `(height-1)` into fixed-width command fields, computes `ceil(width/64)`, and manipulates 14-bit graphics-address fields.

### Canonical V120 sibling — `003A22A0`

Canonical V120 independently promoted `003A22A0` as a **Presentation graphics transfer-command owner** because its complete body emits the same `0x50/0x51/0x52/0x53` register sequence and constructs the associated transfer command packets.

That provides internal FFXII evidence that this is a retained legacy graphics-transfer family, not a modern D3D11 texture-cache inference.

## 2.5 External architecture corroboration — not primary proof

External PS2 graphics documentation agrees with the executable's literal command/register pattern:

**PCSX2 `GSRegs.h`**
- `0x50` = `BITBLTBUF`
- `0x51` = `TRXPOS`
- `0x52` = `TRXREG`
- `0x53` = `TRXDIR`

**ps2sdk `libgs.h`**
- `BITBLTBUF` — image-transfer source/destination address and format;
- `TRXPOS` — source/destination transfer coordinates;
- `TRXREG` — transfer width and height;
- `TRXDIR` — transfer direction.

PCSX2's GS constants define:
- GS local/virtual memory size: **4,194,304 bytes (4 MiB)**;
- GS page size: **8,192 bytes (8 KiB)**.

PS2 pixel-storage documentation describes packed GS formats in **32-bit-word storage units**:
- 32-bit format: 1 pixel per 32-bit word;
- 16-bit format: 2 pixels per 32-bit word;
- 8-bit format: 4 pixels per 32-bit word;
- 4-bit format: 8 pixels per 32-bit word.

This external material corroborates, but does not replace, the executable-body evidence.

## 2.6 Storage-unit derivation

The exact `003A1E50` format-size body behaves in the same 32-bit-word unit model:

- the 32-bit path returns an aligned pixel-count-sized quantity;
- lower-bit formats reduce storage by the appropriate packing factor.

Therefore the `00467AA0` constants convert directly:

- `0x100000` 32-bit words  
  = 1,048,576 × 4 bytes  
  = **4 MiB**
- `0x800` 32-bit words  
  = 2,048 × 4 bytes  
  = **8 KiB**

Those values exactly match the PS2 GS local-memory capacity and page size.

The body is therefore managing a **GS-local-memory-compatible image/mip budget** retained inside the PC Presentation compatibility layer.

Its budget reserves:

`3 * width * height`

32-bit-word units for three full-resolution surfaces, then subtracts the two runtime image totals before selecting multiply referenced image mip chains.

The identities of those three surfaces are not proven and must remain unnamed.

## 2.7 Cross-category challenge

`002F7380` is called from a Movement-owned navigation/resource dirty-dispatch path.

However, sealed V120 Movement exit-gate evidence explicitly identifies it as the **Presentation-owned dataset runtime/update side of that callback seam** and retains Movement ownership for the dispatcher/dirty state itself.

The refined LegacyPS2GS classification is based on:

- its complete current body;
- exact image/mip sizing;
- exact Presentation budget-family state;
- exact fixed 4 MiB / 8 KiB word-budget geometry;
- the executable's literal GS transfer-register sequence;
- canonical Presentation graphics-transfer siblings;
- independent external GS architecture corroboration.

It is **not** based on the category of its Movement caller.

## 2.8 Refined decision

**STRONG READ-ONLY PROPOSAL.**

`002F7380` is best described as:

`Presentation.LegacyPS2GS.ImageMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

### Explicit negative boundaries

Do not claim:

- modern D3D11 GPU residency;
- a generic PC GPU texture-memory manager;
- exact designer-facing texture/effect names;
- exact identity of the three reserved full-resolution surfaces;
- Movement ownership;
- a network/multiplayer state seam merely because Movement triggers the rebuild.

This is a retained **legacy PS2 GS-compatible Presentation image-memory budgeting mechanism** inside the PC executable.

---

# 3. GN read-only status after refinement

Strong proposed rows: **2**

1. `00313A00`  
   `InputGameplay.FieldBattleOperationInhibitMaskReconciliation`

2. `002F7380`  
   `Presentation.LegacyPS2GS.ImageMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

Applied rows: **0**

Official certified parent state remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

If, and only if, both rows later pass exact-current-body fencing against a fresh import of the physical GM160 recovery-transfer GZF and the complete mutation/persistence gate, the **prospective** arithmetic would be:

- explicit: **38,003**
- unresolved: **158**
- explicit coverage: **99.58596%**

That prospective state is **not** a current checkpoint and must not be reported as persisted.

---

# 4. Required mutation gate when GM160 becomes physically available

Before applying either row:

1. Verify the actual GM160 recovery-transfer GZF size and SHA-256.
2. Import it into a brand-new writable Ghidra project with auto-analysis disabled.
3. Reproduce:
   - 38,161 functions;
   - 38,001 explicit;
   - 160 unresolved;
   - 99.58072%;
   - overlap 0;
   - deterministic snapshot SHA-256 `d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20`;
   - embedded EXE SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
4. Regenerate the 160-current residual from that fresh parent.
5. Require that `002F7380` and `00313A00` are still unresolved.
6. Recompute exact-current body size/hash for both.
7. Reject either row on any body/classification drift.
8. Build an exact expected-count GN manifest only for passing rows.
9. Apply comments/CodeDomain tags only.
10. Generate a deterministic complete 38,161-function post-state snapshot.
11. Diff against the fresh parent and require:
    - intended functions only;
    - comment/tag additions only;
    - functions added/removed = 0/0;
    - tag removals = 0;
    - body/range/name/prototype/thunk drift = 0;
    - immutable drift = 0.
12. Close the target DomainFile.
13. Pack in a separate headless invocation and require:
    - `open=false`;
    - `busy=false`;
    - `changed=false`;
    - preferably `canSave=false`;
    - explicit `PACK_PASS`.
14. Import the packed GZF into a completely new Ghidra project.
15. Reproduce the deterministic snapshot, ledger, overlap and authorized embedded EXE.
16. Only then claim a persisted GN checkpoint.
17. Regenerate the residual from the fresh post-GN state before continuing.

