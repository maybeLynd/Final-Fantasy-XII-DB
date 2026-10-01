# Affected-consumer check — UQ-156 map picture and the `+0x5C` byte (FABLE, Claude Opus 5.5, 2026-09-26)

FABLE's 2026-09-25 arm-4 reading made two statements that a full read of the arm and of `00404230` does not support.

- **"it runs `00404230` and `004043B0` over the array".** `00404230` is not given the element array. It takes the
  page's `+0x38` draw record and the map data's `+0x10` texture, and draws the map picture as one textured quad. Its GS
  register records are `TEX0_1` / `TEX1_1` / `CLAMP_1` / `TEST_1`. Only `004043B0` walks the array. The call does sit
  inside the array-exists branch, so the picture is drawn only while the array exists.
- **"So the drawn layer follows where that character stands" (marked inferred).** The byte stored at `002B8872` is
  read only from the map data's `+8` atlas. The atlas header's `word[+0x44]` picks the entry, and the slice has no
  float input, so the character's projected position does not choose it. The byte is a palette bank:
  `00404230` adds four times it into `TEX0`'s palette base. The picture itself is drawn with bank 1, which both arms
  force around the call.

**Regression, run by FABLE 2026-09-26:** `_index/candidates/uq156-arm-readings/map_picture.py`, 23 checks, FAILS 0.
- It checks the tag order and values, the `TEX0` composition and the quad emit, with a known positive (`005520F0`, the
  same four tags, documented on the NPC-name page) and a planted negative (`004043B0`, no tag records).
- It checks both arms' call shape: the record in `rcx`, the `+0x10` texture as the sixth argument, bank forced to 1
  before the call and restored after the line pass.
- It checks the `002B8872` slice: its loads, no xmm register, the store; and that `rdi` there is still the draw record,
  since `002B86DD` is the single entry and nothing on that path writes `rdi`.

| consumer | state |
|---|---|
| `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md`, arm-4 skeleton step 3 | revised-here (clause struck, picture bullet added) |
| the same page, the track map's `002B8872` bullet | revised-here ("layer byte" and the inferred sentence struck, corrected reading added) |
| `_index/OPEN-QUESTIONS.md` UQ-156 row (the same two statements, restated) | revised-here (struck the same way, narrowing added) |
| `16-UI/Widget-Object-Model/CONTRACT-widget-object.md` `+0x38` = the node's live draw record | agrees (the page's `+0x38` object is that record) |
| `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`, `00244070` tree-entry decode | agrees (same entry format; that decode adds into `+0x5C`, this site stores) |
| `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md`, `00272590` | agrees (the tagged-block emit `00404230` runs) |
| `16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md`, `00271050` | agrees (the packet header write `00404230` runs) |
| `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`, `00403640` callee list | agrees (lists `00404230` as a callee only) |
| `_index/AUDIT-LOG.md`, `_index/_inbox/*` | history; the two phrases do not occur there (grepped 2026-09-26) |
