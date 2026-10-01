# Affected-consumer check: RM-1 close-out (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling:**
- All 215 member registrations are accounted for (see the RM-1 register row).
- The seven Phyre enum members are 4-byte ints (value-type descriptor `01F2E550`).
- The last 11 array registrations are annotated.
- PString +0 is `m_buffer`, an 8-byte tagged pointer.

**Replaced accepted knowledge (all OPUS's own):**
- `PString` `0x0000 1 chars uint8` + `unobservedSpan0001` (2026-09-21, from the `c_str` adapter's first instruction)
  → `0x0000 8 m_buffer char* (tagged: bit 0)`.
  - The whole adapter `006A77F0` loads the qword and subtracts its low bit.
  - Three independent routes agree:
    - the registrar `006A72B0` names `m_buffer`;
    - the packed namespace's pointer attribute on `PString::m_buffer`;
    - the same bit-strip at `0018D270` on `PShaderParameterDefinition::m_name`.
- `PAnimationChannelBase` `m_interp`, `PAnimationChannelTarget` `m_type` and `PPhysicsShapeBase` `m_type`:
  8-byte blob rows → a 4-byte `int (enum)` plus a 4-byte unobserved tail.

**Regression.** Each script refuses the old reading on `--check`:
- `fix_pstring.py` refuses anything but the replaced 1 + 7 pair;
- `fix_enum_width.py` refuses an enum row narrower than 4 or named differently.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` (PString; 7 enum rows; 11 array rows) | revised-here | revised-here |
| `_index/OPEN-QUESTIONS.md` RM-1 | PARTIAL → ANSWERED, prior status kept | revised-here |
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md` (`m_buffer` pointer attribute; enum bit 5) | the evidence used; no change | agrees |

Corrects: _types/fields.tsv

Run receipt: `fix_enum_width.py`, `annotate_arrays.py`, `fix_pstring.py` executed at 75a1b1946 (applied 7, 11, 1; re-runs apply 0).
