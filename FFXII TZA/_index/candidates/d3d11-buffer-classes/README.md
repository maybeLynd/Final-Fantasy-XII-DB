# PConstantBufferD3D11 and PStructuredBufferD3D11 past their bases (OPUS, 2026-09-27)

**State: PENDING REVIEW.** The deferred-lighting carve owns objects of both classes, and neither class's tail had rows.
The control passing is not acceptance.

| check | observation |
|---|---|
| K0 | Each creation site's constructor issues the same stores as its class descriptor's constructor: `00615550` = `00611D60` (constant buffer), and `00616060` = `006127C0` (structured buffer). |
| K1 | The constant-buffer creator `0061F070` describes a dynamic constant buffer (usage 2, bind 4, CPU write). It reallocates the aligned copy at `+0x10`, then for each element (stride `0x10`, PSharray rule on `+0x18` / `+0x20`) creates the buffer into element `+0x00`, fills GetDesc into the class's `+0x30`, and stores 0 in element `+0x08`. |
| K2 | Constant buffer `+0x48` is the resources-created flag: set to 1 after `0061F070`, cleared by the release `0062B7B0`, and tested by `00625EC0`. |
| K3 | Structured buffer: `0061F200` creates each buffer into element `+0x00` (stride `0x28`) and fills GetDesc into `+0x48`; `0061F710` creates the SRV into `+0x08`; `006209C0` creates the UAV into `+0x10`. |
| K4 | Structured buffer `+0x60` is only ever written 0 (by the constructor and by the release `0062BB40`) and is tested by `00625EF0`. No non-zero writer exists among the structured-buffer functions, so it is **not** called a created flag. The texture and constant-buffer flags each have a proven setter. |
| S | Regression: the rows and element types exist and tile. S FAILED before the carve. |

**Not generalised.** The structured buffer's resize and allocator are shared with PTexture3DD3D11 (identical folded
code). That shows the two elements have the same layout, not that they are the same element type, so each gets its own
declared type.

**Still DISCOVERED:**
- 8 bytes in the constant buffer and 8 in the structured buffer;
- `+0x0C` of the constant-buffer element;
- 16 bytes of the structured-buffer element.

`+0x60`'s meaning stays open. The K4 search covered the functions in `0x5D0000–0x680000` that call the structured-buffer
routines; loaded cluster data and code outside that set were not searched.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` PConstantBufferD3D11 / PStructuredBufferD3D11 | tails carved | revised-here |
| `_types/types.tsv`: both `ctor` cells; ConstantBufferD3D11Element and StructuredBufferD3D11Element added | declared | revised-here |
| the pdeferredlightingd3d11 record | describes `+0x48` / `+0x60` only as the classes' fields | agrees |

**Run receipt.** Run verified at dff7d04ce: `buf_check.py` K0–K4 and S PASS, FAILS 0. S FAILED before the carve.
