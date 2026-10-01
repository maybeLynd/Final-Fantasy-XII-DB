# SWE2-AUDIT-SEM review — SWE2-EC7's R1 span row "libvpx VP8 decoder object, UC-1 bodies in its span" (4, C) (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `SWE2-EC7-REQ-AUDITSEM-UC1-SPAN-LIBVPX-0929` |
| reviewed | `9e90a97ea` (author **SWE2-EC7**) — [`ec7-uc1-span-rows-0929/README.md`](../ec7-uc1-span-rows-0929/README.md), the row on `third-party-middleware-inventory.md`, `members/libvpx-vp8-decoder-uc1.tsv` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** — and the control map is a documented entry point for test 3 |

## 1. The four tests (SWE2-AUDIT-SEM)

The shared re-runs are in [`../auditsem-review-uc1-span-ppfx-0930/`](../auditsem-review-uc1-span-ppfx-0930/REVIEW.md),
where the replay on a clean extract of `2c840bfe4` is identical.

- **Test 1.** All four bodies lie between the listed members `0016ECE0` and `0016F070`, inside `0016DDD0`–`0017C890`.
- **Test 2.** `select_libvpx.py` admits all 4 (116 → 120). Its interface-table, control-map and DSP-kernel assertions
  hold, and its outbound and inbound controls are byte-identical. The replay agrees.
- **Test 3.** In my hunt (`uc1_own.py` V / `uc1_own2.py` S2), each body's only data reference is one relocated VA64
  cell in the control map, and there is no rel32 or RVA-cell reference. The record's raw index adds a branch to
  `0016EFF0` from inside the span. Callees pass.
- **Test 4.** The note carries "4 UC-1 bodies admitted to frontier 2026-09-28, dispositioned by span 2026-09-29", and
  the members file has 4.

## 2. Is the control map a documented entry point? (SWE2-AUDIT-SEM)

Yes. The data is libvpx's own dispatch structure, read here from the image.
- **The interface table.** It is at `01CDB290`, and its relocated slot `01CDB2B0` points to `01CDB320`.
- **The control map.** `01CDB320` is a `{ctrl_id, fn}` array ending in `{-1, 0}` at `01CDB3D0`. This is libvpx's
  `vpx_codec_ctrl_fn_map_t` list, which `vpx_codec_control` walks by id:

  | id | fn |
  |---|---|
  | 1 | `0016EC20` |
  | 2 | `0016ECE0` |
  | 3 | **`0016EE40`** |
  | 4–7 | `0016EE70` (one function for all four, as in libvpx's debug-option controls) |
  | 0x100 | **`0016EE80`** |
  | 0x101 | **`0016EFF0`** |
  | 0x102 | `0016EEC0` |
  | 0x103 | **`0016F030`** |

- **The bodies match their slots.**
  - `0016EE40` (id 3) sets `+0xF8 = 1` and copies a 12-byte config. That is the set-postproc shape: a flag plus three
    ints.
  - `0016F030` (id 0x103) copies two qwords to `+0x108`/`+0x110`. That is the set-decryptor shape: a callback plus
    its state.

So the four bodies are reached only through libvpx's own control dispatch. The parent row names the map, and the
selector asserts it. That is what test 3 means by the family's documented entry mechanism.
