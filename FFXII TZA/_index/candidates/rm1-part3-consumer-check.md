# Affected-consumer check: RM-1 part 3, the fixed-size member widths (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (scripts `_index/candidates/rm1-array-members/carve_math.py` and `fix_fixed_size.py`, both idempotent
and `--check`able):
- **Nine math templates.** Their `m_elements` are bound by the name string each registrar passes to `00632C90`, and
  carved into single gaps they tile exactly.
- **19 fixed-size registrations.** Each is given its element type, from the descriptor the registrar loads into `r8`
  (named by the field schema's own `type_obj`), and its count, a7.

**Replaced accepted knowledge (OPUS's own 2026-09-19 signature pass, which recorded the element type as the member):**
- `PShaderPassParameterLocationTypesBase` `m_parameterStart`/`m_parameterCount`: `uint16` (2 B) + a 6-byte
  unobserved span each → `uint16[4]` (8 B). Independently stated by the packed namespace's `PUInt16
  m_parameterStart[4]` (w5 = 4).
- `PAnimationConstantChannel.m_value`: `float` + 12 unobserved → `float[4]`.
- `PMeshInstanceBounds` `m_min`/`m_size`: 16-byte blobs → `float[3]` + a 4-byte unobserved tail.

**Regression.** `fix_fixed_size.py --check` refuses the old reading: a narrow row without a closing unobserved span, or
a row named differently from its registration. `carve_math.py --check` refuses a class whose gap is not count × 4.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` (9 math rows carved, 17 fixed-size rows widened, split or retyped) | revised-here | revised-here |
| `_index/OPEN-QUESTIONS.md` RM-1 | part 3 appended, residue restated | revised-here |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv` | records the element type only (its `type` column); no count column. Unchanged; the store carries the count | agrees |

Corrects: _types/fields.tsv

Run receipt: `carve_math.py` and `fix_fixed_size.py` executed at 64b63b044 (carved 9; applied 17; re-runs apply 0).
