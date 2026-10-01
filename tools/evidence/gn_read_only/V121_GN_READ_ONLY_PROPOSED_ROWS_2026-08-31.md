# V121 GN — READ-ONLY PROPOSED ROWS — 2026-08-31

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Parent authority intended for later mutation:** GM160 recovery transfer  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## Important fencing

These rows were derived from complete-body analysis of the exact authorized executable plus persisted V120/V121 semantic evidence. They have **not** been applied to the GM160 recovery-transfer GZF because that physical GZF payload is not exposed in the current execution filesystem.

Therefore:
- no V121 CodeDomain count change is claimed;
- no unresolved-count change is claimed;
- no GN checkpoint exists;
- no persistence certification exists;
- the official certified state remains **38,001 explicit / 160 unresolved / 99.58072% / overlap 0**;
- before any later mutation, fresh-import the actual GM160 recovery-transfer GZF, reproduce its certified ledger/snapshot/residual, and exact-current-body fence these rows again.

No PE `.pdata`, `.xdata`, unwind, EH/IP-to-state metadata, or owner adjacency is used as semantic proof below.

---

## Proposed row 1

### `00313A00`
**Proposed CodeDomain name:**  
`Runtime.ControlPolicy.FieldBattleOperationInhibitMaskReconciliation`

**Complete body:** 289 bytes  
**Exact authorized-EXE body SHA-256:**  
`c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246`

### Mechanism proof

The complete body rebuilds row 2 of a central 16-row × 32-bit operation/control mask using exact sibling primitives:
- `002E1C20(row, bit)` sets the selected row bit;
- `002E1CA0(row, bit)` clears the selected row bit;
- aggregate reader `002E0FA0` OR-reduces the 16 rows into one effective mask.

`00313A00` explicitly reconciles row-2 bits:
`0,1,2,3,4,5,6,7,8,10,11,12,20`.

Most of those bits mirror whether global `02089350` is non-null. Persisted V120 authority identifies `02089350` as the **CombatAction current-selected-BattleUnit state**, owned by `00313DB0` and reset by WorldAreaField initialization; this is input evidence, not ownership inheritance.

Bit 1 additionally depends on the exact predicate at `00253B90`.

Bit 10 is selected independently from the return of `00377C20`. The exact `00377C20` body resolves the current indexed field record and returns the high bit of a two-byte value; canonical V120 places that helper in **WorldAreaField**. The authored designer meaning of that field bit is intentionally not guessed.

When no selected BattleUnit exists and shared runtime/gameplay flag `02089340 & 0x40` is clear, the routine also derives a local gate value. Its tail jumps to `002E1C40(..., bit=5)`, reconciling a separate gate bit.

Direct call contexts include:
- the high-level field-frame/battle orchestration path; and
- the `00313DB0` transaction when current-selected-BattleUnit state is installed/cleared.

### Decision

**PROPOSED.** Complete-body mechanics now resolve the previously protected mixed CombatAction/WorldAreaField hold as a shared field/battle **operation/control inhibition-mask reconciliation** service.

Do **not** assign CombatAction or WorldAreaField PrimaryOwner from the input state/callers. This is a V121 CodeDomain proposal only.

---

## Proposed row 2

### `002F7380`
**Proposed CodeDomain name:**  
`Presentation.Rendering.ImageMipStorageBudgetAndReferenceSlotTableRebuild`

**Complete body:** 723 bytes  
**Exact authorized-EXE body SHA-256:**  
`15594f6181100f7fa10ac8a770566d60b963e47c93176fd7d7f33152b3ac8583`

### Mechanism proof

The complete body tears down and rebuilds a derived table at object offsets `+0x218/+0x228`.

The source record bank is 0x60 bytes per record. Exact helper `00466190`:
- indexes one 0x60-byte source record;
- reads a format-like byte;
- reads a mip-count byte capped at 7;
- reads two dimensions;
- repeatedly calls `003A1E50(width, height, format)`;
- halves both dimensions for each successive level;
- sums the resulting per-level storage sizes.

Independent sealed V120 evidence already classifies `003A1E50` as a **pure graphics-format/mip storage-size calculation from dimensions/format**, whose sole caller iterates image mip records and sums their computed sizes.

The first pass:
- computes a maximum single-image mip footprint;
- computes a weighted aggregate record metric;
- clears each record's derived reference/slot field.

It publishes the maximum/aggregate metrics through `00467B10` and `00467B00`, then obtains a remaining budget from canonical Presentation helper `00467AA0`. That helper computes a fixed-capacity remainder and aligns the result down to an **0x800-byte boundary**.

The routine then walks 0x30-byte reference descriptors selected by the current dynamic mask and increments per-image reference counts, including linked/continuation image records.

The final image pass is exact:
- records with reference count <= 1 receive slot `-1`;
- for records with reference count > 1, it computes `running_selected_mip_bytes + current_full_mip_bytes`;
- the record receives the next compact slot index only when that new cumulative total is **strictly less than** the computed aligned budget;
- accepted records advance the cumulative selected-mip total and compact slot count;
- rejected records receive slot `-1`.

If at least one image is selected, the routine:
- writes selected-slot count at `+0x228`;
- allocates exactly `slot_count * 40` bytes into `+0x218`;
- zero-initializes each 40-byte table record.

### Cross-category challenge

Its sole direct caller is inside the Movement-owned navigation/resource dirty dispatcher. However, sealed V120 Movement exit-gate evidence explicitly identified `002F7380` as the **Presentation-owned dataset runtime/update side of that callback seam**, while retaining Movement ownership for the dispatcher/dirty state itself.

The image/mip helpers `00466190`, `00466220`, and `003A1E50` are support/boundary mechanisms and do not confer PrimaryOwner. Conversely, the budget helpers `00467AA0`, `00467B00`, and `00467B10` have canonical V120 Presentation ownership. The proposed V121 name follows the complete body and independent dataset-family evidence, not caller adjacency.

### Decision

**PROPOSED.** The previously protected hold is now mechanically resolved as a **Presentation image/mip storage-budget and multi-reference compact-slot table rebuild**.

“GPU residency”, exact texture-memory tier, exact visual asset type, and designer-facing record names are intentionally **not** claimed because the current proof does not require them.

---

# GN read-only result

Strong proposed rows: **2**
- `00313A00` — `Runtime.ControlPolicy.FieldBattleOperationInhibitMaskReconciliation`
- `002F7380` — `Presentation.Rendering.ImageMipStorageBudgetAndReferenceSlotTableRebuild`

Applied rows: **0**

Certified parent ledger remains unchanged:
- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

## Required next mutation gate

Only when the actual GM160 recovery-transfer GZF is physically accessible:

1. verify GZF hash/size;
2. fresh-import into a new Ghidra project;
3. reproduce the certified GM160 snapshot, ledger, overlap, embedded EXE and 160-current residual;
4. regenerate evidence rather than relying on stale residual files;
5. verify both proposed functions are still unresolved and exact-current bodies match the hashes above;
6. exact-current-body enrich these rows;
7. apply only passing rows with exact expected count;
8. generate whole-project deterministic post-GN snapshot/diff;
9. require only intended comments/tags, zero function additions/removals, zero tag removals and zero immutable drift;
10. close the DomainFile, pack in a separate invocation with explicit `PACK_PASS`, and fresh-import/reproduce before any persistence claim.

