# SD-65: no shipped class takes the dynamic route, and every file-declared member is registered statically (OPUS, 2026-09-30)

Register row SD-65 was registered by SWE2-DATA ([the-file-schema-against-the-runtime-schema.md](../../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
section 7). It asks two things:
- which shipped classes take the load-time dynamic-member route (`00632B30`);
- whether a file declares members for a class this build does not register statically.

This record combines image reads with a census of the shipped data (tier 9). There are three scripts:

| script | reads | output | result |
|---|---|---|---|
| `sd65_loader.py` | the certified image | `sd65_loader.out` | `FAILS 0` |
| `sd65_census.py` | every `.phyre` namespace in `FFXII_TZA.vbf` (35,984 files) | `sd65_census.out` / `.json` | controls PASS |
| `sd65_members.py` | the image and the VBF | `sd65_members.out` | `FAILS 0` |

## The answer (OPUS)

**Part 1: none.** The route is opt-in per class, through bit 0 of the file class record's `w7`, and no shipped file
sets it.

- **L1: one path.** `00632B30` (`PClassDataMemberDynamic`) is called only from `006393A0` (at `0063942C`).
  `006393A0` is called only from the cluster loader `0059AC00` (at `0059AEA7`).
- **L2: the class pass.** For each 0x30-byte class entry, the loader checks two things: the entry has no native
  descriptor (`+0x10 == 0`), and the file class record (`+8`) has bit 0 of `+0x1C` set. If both hold, the loader:
  - reads the record's `+0` as a 1-based super-class index;
  - builds a 0x140-byte dynamic descriptor (`00632E80`) under that super class.

  The error strings name the operation: "Unable to find super class %d (of %d) when creating dynamic class '%s'",
  "Invalid super class …" and "Namespace already includes the specified class …".
- **L3.** A flagged class that is still without a descriptor fails the load with `0x13`.
- **L4: the member pass.** It runs only for classes that have a descriptor, bit 0 of `+0x1C` and a non-zero `+0x0C`
  member count. Each 0x38-byte member entry with no native member gets a dynamic one through `006393A0`. The flag
  passed is bit 1 of the file member record's `+0x10`, the w4 "object pointer" bit. An unresolved type logs
  'Type not found for "%s::%s"'.
- **Record words.** The record offsets the loader reads are the published namespace words:
  - class record `+0x00` w0, the parent index (already `CX-2`), `+0x0C` w3, the member count, and `+0x1C` w7;
  - member record `+0x10` w4.

  That the entry's `+8` points at the file record is read from these offset matches and from the super-class
  strings. The entry builder itself is not read.
- **The corpus (`sd65_census.py`).** It covers 35,984 files, 177 class names and 684,244 class records.
  - **w7 bit 0 is set in 0 records.** The w7 values are 0, 2, 8, 12, 20, 32, 34 and 40.
  - **Correction.** The namespace page lists w7's values as "0, 8, 32, 2, 12, 34, 40 corpus-wide". The census also
    finds 20, in 5 records.
  - **Consequences.** No shipped class is built as a dynamic class, and no shipped member is added through
    `00632B30`. The `0x13` failure cannot fire on shipped data. w0 is in range in every record, and the parents it
    names are coherent: `PMeshInstanceSegmentContext` → `PMeshSegmentContext` and `PModifierNetworkDynamicMesh` →
    `PDynamicMesh`.

**Part 2: no.** Every member a shipped file declares has a static registration in this build.

- **What is counted.** The 154 classes that declare members give 527 distinct (class, member) pairs (from the
  distinct member lists). All 527 resolve to a call through one of the five member routes that passes the member's
  name in `r9`.
- **The three call forms.** The class is tied to the call in one of three ways:
  - **D:** `rdx` is one of the class's descriptor globals. A global counts as the class's when it is passed in `rcx`
    to a function that references the class name.
  - **S:** the call sits in a function that itself references the class name. This covers the struct and matrix
    types: `D3D11_DEPTH_STENCILOP_DESC` through `00632BE0`, and `Matrix4`, `PMatrix4`, `PMatrix4x3` and `Vector3`
    through `00632A70`.
  - **T:** for `PArray<T>` / `PSharray<T>`, the call sits in the registrar the field schema lists for that
    instantiation. There the descriptor arrives in a register (`mov rdx, rsi`). The element type is decoded from
    the schema's mangled class column.
- **Controls.** `PClusterHeaderBase::m_size` and `PLight::m_color`, both schema rows, resolve.
- **The 14 classes with no row in `phyre-field-schema.tsv`.** All 22 of their pairs are registered. The table below
  shows where.

| class | member(s) | route |
|---|---|---|
| `PString` | `m_buffer` | array `006A734E` |
| `PMaterialSet` | `m_materials` | array `006665F9` |
| `PMeshInstanceSegmentContext` | `m_streamBindings` | array `005E6860` |
| `PNodeContext` | `m_packedSwitches` | array `005E6CCB` |
| `PShaderPassParameterLocationTypesConstantBuffer` | `m_parameterLocations` | array `005EA2C0` |
| `PStreamInputLayoutD3D11` | `m_streams` | array `006186B6` |
| `PAnimationSet` | 3 | array, in `005B1900` |
| `PModifierNetworkDynamicMesh` | 4 | array, in `006BC750` |
| `PModifierNetworkDynamicMeshInstance` | `m_modifierNetworkInstances` | array `005E6BE0` |
| `D3D11_DEPTH_STENCILOP_DESC` | 4 | `00632BE0`, in `006143B0` |
| `Matrix4` / `PMatrix4` / `PMatrix4x3` / `Vector3` | `m_elements` | `00632A70` |

The first five rows are CL-1's "five array holders, one array member each". This record ties each holder's member to
the member its files declare.

**For modding:** a `.phyre` file cannot add classes or members to this build unless it sets w7 bit 0, and none of
the shipped ones does. Every member the shipped files describe is a member the engine already knows.

## Limits (OPUS)

- **The join's forms S and T match by function and name.** A registrar function that registered the same member name
  for two classes would satisfy S or T for both. No such case is known, but it is not excluded.
- **Other w7 bits.** Only bit 0 is read here. Bits 1 to 5 (values 2, 8, 12, 20, 32, 34, 40) stay unexplained.
- **The entry layout.** The 0x30-byte class entry and the 0x38-byte member entry are read only at the offsets
  above. Their builder is not traced.
- **Scope.** The census reads the shipped archive. A mod file could set bit 0, and this record says what the loader
  would then do, not that it was run.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's
page. The w7 value list on the namespace page is DATA/FABLE-owned; a restatement request goes with this record.
