# DynGeoFontTextSpecial instances: +0xD0..+0x15B is the layer fill cursors and four shared setters' fields (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` DynGeoFontTextSpecialInstance, DynGeoFontTextSpecialFinalInstance and
DynGeoFontTextSpecialShadowInstance `+0xD0`. Each carried `unobservedSpan00D0` (144, 160 and 152 bytes) with the note
"nothing read here touches it". The Final row added "the extra bytes are not located".

**Why the census saw nothing.**
- `+0xD0` is indexed (`[this + i*4 + 0xD0]`), which a displacement census cannot see.
- The plain class's route has no vtable seed.

**Result** (`dyngeo_setters.py`, V1–V5):
- **The vtables share five slots (V1).** The three 12-slot vtables have the same slots 1, 3, 7, 8 and 9, so `rcx` at
  those entries is the instance.
- **The setters (V2):**
  - slot 7 stores a qword at `+0xF8`;
  - slot 8 stores a qword at `+0x100`;
  - slot 9 copies five dwords to `+0x108`;
  - slot 3 copies sixteen dwords to `+0x11C`.
- **Read-back (V3).** Slot 1 reads `+0xF8`, `+0x100` and `+0x108..+0x118` back.
- **`+0xD0` is layer i's fill cursor (V5).** The shared slot 6 reads it, compares it with `layerCount[i]` at `+0xA8`
  and increments it. This is the table on the dyngeo page (`16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`,
  BC-3). The store already carried the three arrays before it (`layerSource`, `layerVertices`, `layerCount`) and had
  left this one as unobserved.
- **`+0x11C` is the page's 4×4 matrix (BC-5).** The Final class's slot 6 applies it to every vertex, with a divide
  by w.

**New tiling, per type:**
- `layerFillCursor` `uint32[10]`;
- `qwordF8`, `qword100`;
- `block108` `uint32[5]`;
- `matrix11C` `float[16]`;
- the class's own unobserved tail from `+0x15C`: 4, 20 or 12 bytes.

**Regression.** V4 fails on the pre-fix store and passes after `Tools/work/OPUS/dyngeo/patch_store.py`. That was tested
on a copy, where `types_index.py --validate` reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` the three types' `+0xD0` rows | re-tiled; the old row quoted in the first new row's evidence | revised-here |
| `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md` (BC-3 table `+0xD0 + 4·i`; BC-5 matrix `+0x11C..+0x158`) | the store now matches the page | agrees |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | the Final and Shadow `+0xD0` rows are closed | agrees |

Run receipt: executed at bbd3af82a - `dyngeo_setters.py` V1–V3, V5 PASS; V4 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
