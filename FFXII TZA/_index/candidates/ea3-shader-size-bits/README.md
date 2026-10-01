# EA-3: bits 13-15 of `PShaderParameterDefinition.m_bufferLoc.m_size` in the shipped data (OPUS, 2026-09-27)

**Question.** Every engine read of a shader-parameter descriptor's u16 at `+0x12` masks it with `0x1FFF`. The word is
the reflected `m_bufferLoc.m_size`, registered whole and loaded from the asset. What do the shipped assets store in
bits 13-15?

**Discriminator.** Every shipped definition record, located through its own file's packed namespace.

**Driver.** `ea3_census.py`, over `D:/FFXII_TZA_extract` (every `.phyre`: 35,984 files). Result: `result.json`.
Input digest (relative path + md5 of the 2,184 files that carry the class):
`652e5de74296943e0ea2ed9a4ba5cc2a8ae8428aa98b851d2330e9d245929fed`.

| | |
|---|--:|
| `.phyre` files read, none rejected by the namespace controls | 35,984 |
| files carrying `PShaderParameterDefinition` (all content-distinct) | 2,184 |
| definition records | **648,027** |
| records with any of bits 13-15 set | **0** |
| largest low-13 value | 7,680 (`0x1E00`) |
| `PShaderStreamDefinition` records (92 lists), bits 13-15 set | 13,356, **0** |

**Record location.** The class word `w1`'s low 28 bits give a 13-byte packed record in all 2,184 files. `m_bufferLoc`
is at record byte 5 and 4 wide; its class is resolved through the member's type reference (`nTypes` + 1-based class
id, CX-3), not by name. `m_size` is at +2 inside it and 2 wide.

**Controls** (`controls_pass: true`):

- **C1 population.** 2,184 files carry the class, the header-class cluster count from CU-2.
- **C2 sensitivity.** The same loop reads bits 13-15 set in 218,033 records at the high half of
  `m_constantBufferLocation`. That count equals the records whose word is `0xFFFFFFFF`.
- **C3 mutation.** A copy of a real file with one size word's bit 13 set is flagged exactly once.
- **C4 layout.** All 2,184 schemas give one layout, `[13, 5, 4, 2, 9, 4]`.
- **C5 extent.** Every list's `m_objectsSize` is `count × 13` rounded up to even.
  - 339 odd-count lists carry one pad byte.
  - The first case seen was `materialsphere.dae`: 121 records, 1,574 bytes.
  - This is a new file-side representation fact. The earlier ≥ check could not see it.

**Answer.** The shipped assets store 0 in bits 13-15. The `0x1FFF` mask changes no shipped value, and the bits carry no
authored content in this title.

**Not claimed:**
- why the SDK masks the bits;
- descriptors built by code rather than loaded. The row's write-side sweep covers code.

**Prior art.** FABLE's unpublished scratch draft of 2026-09-26 (`Tools/work/FABLE/gg3-scratch/subagent-rows4/EA-3.md`)
reached the same 648,027 / 0 by a different route. It found the bufferLoc class by name and checked extents only as ≥.
This package is an independent reproduction, not a copy of that code.
