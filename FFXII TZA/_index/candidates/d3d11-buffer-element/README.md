# The 0x48-byte D3D11 buffer element (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This is board task OPUS-STRUCT-PDATABLOCKBUFFER-D3D11. The control passing is not
acceptance.

**Question.** `PDataBlockBufferD3D11` and `PIndexDataBlockBufferD3D11` (`0x48` each) were one 72-byte unobserved span.
3d95e439c showed they are stored inline in `PSharray m_buffers`. What are their bytes?

**Answer** (`element_check.py`, static, certified EXE). Both element types have the same layout:

| off | width | row | evidence |
|---|---|---|---|
| `+0x00` | 8 | `buffer`: the D3D11 buffer (CreateBuffer's ppBuffer) | E1, E2, E5 |
| `+0x08` | 8 | `shaderResourceView`: from the raw-view creator; null from the dynamic one | E2 |
| `+0x10` | 20 | DISCOVERED: zeroed and copied, no reader found | E3 |
| `+0x24` | 4 | DISCOVERED: never touched | E3 |
| `+0x28` | 8 | `asyncUpdateVtable`: the embedded `TAsyncUpdate<block>` (`00D68DD0` / `00D68DE0`) | E3, E4, E5 |
| `+0x30` | 8 | `asyncUpdateBlock`: the owning data block, written when an update is scheduled | E4, E5 |
| `+0x38` | 4 | `asyncUpdateIndex`: this element's index in `m_buffers` | E4, E5 |
| `+0x3C` | 4 | DISCOVERED: never touched | E3 |
| `+0x40` | 8 | `pendingUploadSource`: the memcpy source of the scheduled update, 0 after creation | E2, E5 |

**The checks:**
- **E1, the device.** `005FD050`, and `00624670` which jumps to it, return the magic static `02CC0410` (R).
  `00625830` runs on R (via `006253D0` ← `0079F4AC` on `00624670`'s return) and calls D3D11CreateDeviceAndSwapChain
  (thunk `0080F2C8`) with ppDevice = R+`0x108` and ppImmediateContext = R+`0x110`.
- **E2, the creators.** `0066F970` / `0066FAB0` / `00670070` / `0066FE20` call the device's vtable+`0x18` (CreateBuffer)
  with ppBuffer = element `+0x00`. `00670070` / `0066FE20` also call vtable+`0x38` (CreateShaderResourceView) with
  ppSRView = element `+0x08`. All four store 0 at `+0x40`.
- **E3, the widths.**
  - The constructors `0065F690` / `0065F340`, the copies `00661720` / `006618A0` / `00672F30` / `00673030`, and the
    assignments `0065F700` / `0065F3E0` all move qwords at `+0`, `+8`, `+0x10`, `+0x18`, `+0x30` and `+0x40`, and
    dwords at `+0x20` and `+0x38`.
  - They install the vtable at `+0x28`; an assignment keeps the destination's own vtable.
  - None of them touches `+0x24` or `+0x3C`.
- **E4, the schedulers.** `00674610` / `006747D0` write the block to element+`0x30` and the index to element+`0x38`, then
  hand element+`0x28` to `0062EB90`.
- **E5, the update.** Slot 0 of the TAsyncUpdate vtable (`00670570` / `00670580`) calls `00670590` / `00670690` with
  rcx = the block and edx = the index. Those functions Map the buffer through R+`0x110`, memcpy (VCRUNTIME140) from
  element `+0x40` for the block's `m_dataSize` (`+0x78` / `+0x70`), and Unmap.
- **S.** Regression: both types carry the rows and still tile `0x48`. S FAILED before the carve.

**What each axis claims:**
- **Physical access:** proven for every named row.
- **Representation:** interface identity comes from the import (D3D11CreateDeviceAndSwapChain), the documented COM slot
  order (ID3D11Device slots 3 and 7; ID3D11DeviceContext slots 14 and 15), and the descriptor shapes. The ctype stays
  `void*`.
- **Meaning:** limited to the lifecycle shown; the buffers' contents are not claimed.

The old whole-instance row's meaning and evidence are kept verbatim in the `+0x10` span row. Neither type is
promoted: three spans stay DISCOVERED - ~~24 bytes in total~~ 28 bytes (20 + 4 + 4; corrected 2026-09-27, OPUS: the commit message and the board note of 274e8decc said 24).

Also revised in the store: both types' `ctor` cells now name the in-place element constructors (`0065F690`, `0065F340`).
No page restates these layouts, so there is no page consumer.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv`, the two element types | 72-byte span carved into 9 rows each | revised-here |
| `_types/types.tsv`, the two element types' `ctor` | element constructor named | revised-here |
| `_types/fields.tsv` `PDataBlockD3D11 +0x20` / `PIndexDataBlockD3D11 +0x18` `m_buffers` | 80-byte PSharray (3d95e439c); `0066F280` / `006718B0` build count = 1 with the element inline, which agrees | agrees |

**Regressions.**
- `types_index.py --validate`: 8216 fields, 0 errors, 0 gaps.
- `check_type_refs.py`: 0 dangling.
- `check_census_widths.py`: 0 disagreements.
- `check_embed_overlap.py`: unchanged. Its one report is the pre-existing BattleStatsRecord ← GambitConfig case.
- `psharray_extent.py` and `plus4_check.py`: FAILS 0.

**Run receipt.** Run verified at 58bd6303f: `element_check.py` E1–E5 and S PASS, FAILS 0. S FAILED before the carve.
