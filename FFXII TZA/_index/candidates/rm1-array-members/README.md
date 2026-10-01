# RM-1 part 1: the array member registrations the field schema never harvested (OPUS, 2026-09-27)

**What this is.** The first part of `RM-1`. OPUS opened RM-1 at `414a737fd`.

**The census** (`check.py`, self-contained: an `E8` scan of `.text`, then argument resolution):
- There are **215** registrations through the array (`00632A10`, 165 sites), fixed-size (`00632A70`, 29) and enum
  (`00632BE0`, 21) member constructors.
- Each site is resolved to its class descriptor, name, offset, a6/a7/a8 and the template vtable the caller installs.
- Each is then classified against `_types/fields.tsv`.

**What changed in the store.**
- **60 array members** (kinds 3/4) sat inside declared gaps in 30 classes: `PMesh`, `PEffect`, `PEffectVariant`,
  `PSceneRenderPass`, `PShader`, `PModifierNetwork`, `PScript`, `PBitmapFont`, … They are carved as 16-byte
  `PArray<T>` / `PSharray<T>` header rows. `carve.py` is idempotent and refuses any member that does not fit one gap.
  - The header layout comes from the shared member-class accessors, which the Phyre package
    (`_experiments/evidence/phyre-array-member-registrations-opus/`) established per instantiation.
  - The element type comes from the installed template vtable. Where that vtable is installed outside the eight
    instructions read, the element is `?` and the kind still comes from a7.
- **`PArray +0x8` is renamed `m_els`, and `PSharray +0x8` is renamed `m_u`.** The templates register those names
  themselves: 60 `PArray<T>` and 9 `PSharray<T>` instantiations register them at offset 8 through `00632A10` with
  a7=2.
- **After the carve** all 96 kind-3/4 registrations with a resolved class land on named rows.

**Still open (RM-1's residue):**
- 26 fixed-size and enum registrations land on named rows but still carry no reflected identity (19 fixed-size,
  7 enum).
- 24 sites have a class descriptor outside the parent-chain map:
  - fixed-size `m_elements` of the matrix/vector templates;
  - `RenderTarget`;
  - 14 D3D11 description-struct enum members (FillMode, CullMode, the stencil and blend ops).
- 36 array members that already had named rows carry no reflected name yet; 25 of them were annotated at
  `414a737fd`.
- What a8 is: it is not the element size for struct elements.

**Part 2 (`carve_d3d11.py`).** 14 D3D11 description-struct enum members and the fixed-size `RenderTarget[8]` are carved
into their structs' declared gaps, tiling each exactly. Builders are bound to structs by the field schema's `class_obj` for
the same builders. For enum members, a7 is the enumeration's highest value (FillMode 3, blend 19, blend op 5).

**Not claimed:** element meanings, and whether the lazy registrars run in a given scene.

**Reproduce:** `python check.py`. It needs the certified EXE and `Tools/work/graph/functions.tsv`, and it rewrites
`harvest.json`. `harvest.py` / `carve.py` are the drivers as run; `harvest.py` read the scratch call graph that
`check.py` replaces with a direct scan.

**Part 3 (`carve_math.py`, `fix_fixed_size.py`, OPUS 2026-09-27).**
- **The nine math templates.** Each registrar passes its class name to `00632C90`: Matrix3, Matrix4, PMatrix4,
  PMatrix4x3, Point3, Quat, Vector2, Vector3 and Vector4. Each one's `m_elements` (float, descriptor `01F2E690`)
  tiles the class's single gap and is carved.
- **The 19 fixed-size registrations on named rows** carry their element type (from the registrar's `r8`) and count
  (a7).
  - Three widths are corrected: `m_parameterStart` and `m_parameterCount` become uint16[4], `m_value` becomes
    float[4], and `PMeshInstanceBounds` `m_min`/`m_size` become float[3] + 4.
  - Eleven rows are retyped.
- **Not changed:** enum widths. a6 is 8 or 16 and not understood.

**Close-out (`fix_enum_width.py`, `annotate_arrays.py`, `fix_pstring.py`, OPUS 2026-09-27).**
- **The seven Phyre enums are 4-byte ints.** Every registrar loads the value-type descriptor `01F2E550` (int).
  a6 is the attribute word: the constructor ORs 0x20, the enum flag, into it. Three 8-byte enum rows are split.
- **The last 11 array registrations carry their identity.**
  - Nine are word 0 of a header the store already splits.
  - Two 16-byte blob rows are retyped.
- **PString +0 is `m_buffer`, an 8-byte tagged pointer.** It is not a 1-byte `chars` field.
- **All 215 registrations are accounted for.** a8 is consistent with element alignment; this is a reading.
