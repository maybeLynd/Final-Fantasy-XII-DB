# Affected-consumer check — packed-namespace member `w2`/`w3` (FABLE, Claude Opus 5.5, 2026-09-26)

The claims corrected are "member `w2` = byte offset of the field within the class" and "member `w3` = element size in
bytes". Both come from the namespace page's §8, and the contract, the register and the parity harness label copy them.

What the shipped files show is that `w2`/`w3` are the member's offset and width **in its class's file-side layout**:
- **147 of the 154 classes with members are packed.** Sorted by offset, their members are contiguous from the parent's
  packed size to class `w1`'s low 28 bits, with no padding. Object pointers are 1 byte and a `PArray` 5, so `w2` is not
  the runtime offset there.
- **6 classes are native.** Pointers are 8 bytes and a `PArray` 16, and `w2` equals the runtime-registered offset,
  10 of 10 joined.
- **1 class fits neither.**

The contract's "`w3` = 29 = `sizeof(D3D11_RENDER_TARGET_BLEND_DESC)`" is corrected on the same evidence: 29 is the
packed width, and the `sizeof` is 32.

**Regression, run by FABLE 2026-09-26:**
`22-Middleware-PhyreEngine/Phyre-Asset-Container/members/w3_census.py`, FAILS 0, over `D:/FFXII_TZA_extract`.
- Its population control equals the contract's full-archive figures: 35,984 files and 2,192,621 members.
- L1: pointer `w3` is 1 or 8, one value per class.
- L2: the packed rule holds, parent-aware, and rejects the planted native class `PParameterBuffer`.
- L3: native offsets equal the runtime registrations.
- L4: the blend-desc widths sum to 29.
- L5: class `w1`'s low bits are the cumulative packed size in all 147 packed classes.

| consumer | state |
|---|---|
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md` §3 member table (`w2`, `w3`), class `w1` row, §15 line on `CD3D11_BLEND_DESC.RenderTarget`, evidence row | revised-here (struck and restated; a two-layout note added under the member table) |
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md` §8 record table (`w2`, `w3`) | revised-here |
| same page, "A third independent confirmation of the header layout" (3,042 offset checks, zero mismatches) | agrees: the header classes' fields are all `u32`, where the packed and native layouts coincide |
| same page, class `w1` cell ("instance size … for the `0x2` family") | agrees (narrower than the contract's extension, not contradicted) |
| `Reconstruction/Tests/Differential/diff_phyre_namespace.py` `CONTRACT_MAP` label | revised-here (identical to the contract's evidence row, so `parity_status.py` sees no drift) |
| `_index/PARITY-STATUS.md` (generated) | not hand-edited. It still shows the pre-`666522264` `w4` text, and it picks up the revised label on its next `parity_status.py` run |
| `_index/OPEN-QUESTIONS.md` CW-1 row ("Member word 2 is the field's byte offset") | revised-here (scope note appended) |
