# Consumer check: 23-ThirdParty contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-23-VALUES-1002. A cloud session mapped `23-Third-Party-Libraries/` from a text snapshot
(report `cloud-reports/re-readiness/23-thirdparty.md` in maybeLynd/Final-Fantasy-XII-DB). Its 35 value items and its
stale and banner items were page-text only. A local read-only pass decided them at the shipping image, and OPUS
re-checked a sample (`thirdparty_check.py`).

Corrected at the bytes:
- The checker reads 17 bytes and compares 18 (`0082E490+0x3C` sets the read length 0x11).
- `0016EFF0` has four return values, not three (`0016EFF0+0x20` returns 1).
- No handler is branched to. The second "reference" to `0016EFF0` is a misaligned byte inside `0016EEC0`.
- The ImGui context is `02EA58C0` (`00169620+0x4`).
- An EASTL string object is 0x20 bytes, with the allocator at +0x18 (the static object at `01FD40D8`, built by
  `001600D0`). An empty string's begin and end are `02EBA2E0` and its capacity end is `02EBA2E1`.
- The CRI decoder banner is Ver.2.05.00 at `01CBA5D1`, and the copyright string is at `01CBA610`.
- libvorbis is reached (`001B7F30+0xF9`).
- There is one Yebis/PPFX package, so there are two post-processing systems, not three.
- The image holds 29 source paths; 6 of the 12 copies are referenced.
- `EnableYebis` is a JSON configuration key (`001C3D50+0x627`).

The pass drafted 89 strike edits (`apply_23thirdparty.py`). OPUS applies the 71 on its own lines across seven pages
(`apply_by_owner.py OPUS`). The rest are routed:
- 10 go to SWE2-EC7: the PPFX source-map page, which SWE2-EC7 leads, and its lines on three pages.
- 8 go to FABLE, on FABLE's lines.

No census TSV is edited. In `members/libvpx-vp8-decoder-uc1.tsv`, the `refs` value 2 for `0016EFF0` counts the
misaligned byte match, so a regeneration is requested from SWE2-DATA.

SWE2-CONTRACT's ACTIVE `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929` names the inventory and EASTL pages. Neither page
is held for it: its checkpoint says no residue remains in scope, and both pages have left PARTIAL.

- **Affected:** 23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md, 23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md, 23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md, 23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md, 23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md, 23-Third-Party-Libraries/README.md, 23-Third-Party-Libraries/third-party-middleware-inventory.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the seven OPUS-led 23 pages (OPUS lines) | revised-here |
  | the PPFX source map and SWE2-EC7's lines on the inventory, EASTL and Bullet pages | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 10 edits) |
  | FABLE's lines on the inventory, EASTL and Bullet pages | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 8 edits) |
  | `members/libvpx-vp8-decoder-uc1.tsv` (`refs` of `0016EFF0`) | routed-to-SWE2-DATA (regenerate request) |
  | RE repo `docs/readiness/23-thirdparty.md` | routed-to-OPUS (filed after this publish, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-thirdparty-readiness-fixes-1002/thirdparty_check.py, verified at 73a856c52: 5 instructions decode as cited and 2 strings read as cited, FAILS 0 ([`thirdparty_check.out`](thirdparty_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (71), FAILS 0.

**Pass-22 neighbours (2026-10-02, OPUS).** `check_publish_neighbours.py` refused the first form of these edits. Some corrections cited another layer's function by address, and that adds an unaccounted crossing. Those functions are now named by role or by their ledger name on the page, with the offset kept. The applier's `ROLE_NAMES` pass makes the same change to its NEW text, so re-runs stay idempotent. The full deciding addresses remain in the applier's comments and in this record. `Tools/work/OPUS/nb_page.py` shows no new hit.
