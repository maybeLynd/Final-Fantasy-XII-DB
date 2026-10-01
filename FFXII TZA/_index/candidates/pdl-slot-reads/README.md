# PDeferredLightingSlot0080: the slot evaluator reads the "unobserved" spans (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` PDeferredLightingSlot0080, seven rows named `unobservedSpan*`: `+0x000`, `+0x008`,
`+0x010`, `+0x01C`, `+0x040`, `+0x05C` and `+0x064`. The 2026-09-25 repair (`s49-opus-replay-lighting-slot-zeros/`)
had shown the constructor writes 0 to them. Their names still said nothing reads them, but the field-access index lists
reads by `0065A960`.

**Result** (`pdl_slot.py`, P1–P3):
- **The receiver is proven (P1).** `00659EC0` hands `0065A960` each slot's address in `r8` (`base + 0x50 + (i << 7)`,
  and `base + 0x4050` for slot 128). `0065A960` keeps it in `rbx`.
- **The evaluator's reads (P2):**
  - floats at `+0x00..+0x2C` and `+0x54..+0x60`;
  - integer dwords at `+0x50` (cmp / mov), `+0x64` (cmp) and `+0x68` (mov);
  - `+0x30` is address-taken.

**New tiling.** Twelve read fields replace six of the rows. `+0x40` keeps a 16-byte unobserved span, since no read was
found there. Every new row keeps the 2026-09-25 lifetime fact: the constructor `006458A0` writes the initial 0
explicitly.

**Regression.** P3 fails on the pre-fix store and passes after `Tools/work/OPUS/pdl/patch_store.py`. That was tested on a
copy, where `types_index.py --validate` reports 0 errors and 0 gaps.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PDeferredLightingSlot0080 (7 rows) | re-cut; the old rows quoted in the first replacement's evidence | revised-here |
| `_index/candidates/s49-opus-replay-lighting-slot-zeros/` (constructor zero writes) | its fact carried onto every new row; its check replays the constructor and does not read fields.tsv | agrees |
| the unobserved-row audit (`Tools/work/OPUS/silent_unobserved.json`) | this type's 7 rows closed | agrees |

Run receipt: executed at bbd3af82a - `pdl_slot.py` P1–P2 PASS; P3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.
