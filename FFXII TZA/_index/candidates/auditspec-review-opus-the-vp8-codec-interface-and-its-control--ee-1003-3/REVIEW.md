# SWE2-AUDIT-SPEC review: OPUS engine_explained interior citations (opus-the-vp8-codec-interface-and-its-control--ee-1003-3)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VP8-CODEC-INTERFACE-AND-ITS-CONTR-D8CAE` · Package: `_index/candidates/opus-the-vp8-codec-interface-and-its-control--ee-1003-3/` · Page: `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md` (commit 5f91e98be)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The package has 2 rows, fewer than 15, so both were read clause by clause against the bytes. Both rows are correct in every value, offset, width, polarity, callee and anchor (10 anchors). Three things must be narrowed:

- one timing phrase in the `0017B580` row is literally inaccurate;
- the README's opening count is wrong;
- the README names a review step ("rotation helpers") that has no object in this package.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply`. Output: `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`, exit 0. The page block equals `rows.json`, and `git status` on the page and the package was clean afterwards (HEAD f49bb4021).
- `rows.json`: 2 rows, 10 anchors. Rejected 0, skipped 1 (`0017B010`), missing 12, corrections 0.
- Semantic pass: **every row** was read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...). The extent comes from `check_dispositions.load_functions`, and rip targets were resolved to their section.
  - `0017AC50` (953 B), exact.
    - Stack arguments after the 8 pushes and `sub rsp,0x48`: a5..a11 = `[rsp+0xB0..0xE0]`.
    - Split choice:
      - (3, 16) by default.
      - `00174470(d,0x6E)` (`0017AC90`) → (2, 4).
      - `00174470(d,0x6F)` → (`00174470(d,0x96)`, 2).
    - The loop `r13d` < n is signed `jl`.
    - `j` = byte `[base+0x1BBD0B0+16s+k]` (`0017AD0E`). `r10` = `lea [rip-..]` = 00120000, so VA `01CDD0B0`, `.rdata`.
    - L:
      - `test cl,3` / `jne` → `[r12+4j+8]`.
      - Otherwise `cmp byte [r8],9`, which selects between `[r8+4j+0x18]` and `[r8+4]`.
    - A:
      - `test ecx,~3` → `[r12+4j-4]`.
      - Otherwise `cmp byte [r9],9`, which selects between `[r9+4j+0x3C]` and `[r9+4]`.
    - The q index is `sete` (L=A) `|` `cmove` 4 (A=0) `|` `cmove` 2 (L=0), with q = `01CDCFF0` (`.rdata`) + 3*index (`0017AD74`).
    - Three inline boolean reads:
      - The first refills with `cmp [d+0x18],0` / `jge`, the later ones with `jns`, both through `00179ED0`.
      - The split is `((range-1)*p>>8)+1` and the compare is `shl 0x38` / unsigned `jb`.
      - Each read's zero path selects L, A or 0.
    - The new-vector path: 2*`0017A490(d,a7)` (`0017AEE6`) + word `[rsp+0xB8]`, and 2*`0017A490(d,a7+0x13)` + word `[rsp+0xBA]`.
    - The clamp flag uses signed `movsx` with `setl`/`setg` against a10/a11 (low word) and a8/a9 (high word), then `or byte [a5+0xA]`.
    - Store loop: count = byte `01CDCB14`[s], with the list at `01CDCFB0`+16s+count*k (both `.rdata`). Each step writes `[r12+4b+0xC]` (`0017AFB7`).
    - Exit: byte `[a5+8]` = s.
  - `0017B580` (799 B), exact except for the narrowing below.
    - `m` = `[rcx+0x1EB0]` is loaded before `0017A850(rcx)` (`0017B593`).
    - `+0xF8C`=0, and `+0xF90` = `[0x1E74]`<<7 − 0x80 (`0017B5B8`).
    - The row and column loops are signed (`jle`/`jl`). `+0xF84`=0 and `+0xF88` = the saved `[0x1E78]`<<7 − 0x80.
    - Column body:
      - Bytes `+0xF61` and `+0xF60` non-zero: `B(+0xF64)` (refill `0017B661`). Then either 2+`B(+0xF66)` (`add r15b,2`; `0017B717`) or `B(+0xF65)` goes to byte `[m+0xB]`.
      - `+0xF61`=0 and `+0x1E64`=0 → `[m+0xB]`=0 (`0017B783`).
      - `[m+9]` = `B(+0x4447)` when `+0x1E80`≠0, else 0. `[m+3]`=0.
      - `0017A320(rcx,m)` or `0017B010(rcx,m,m)` on `+0x1E64` (`0017B826`).
      - −0x80 on `+0xF84` and `+0xF88`, and `m`+=0x4C.
    - Row end: −0x80 on `+0xF8C` and `+0xF90`, and `m`+=0x4C.
    - The shift table is `01CDC180` (`.rdata`).
- Anchors: all 10 are instruction boundaries strictly inside their function, have the recorded mnemonic, and sit on the clause they are listed for.
- Family-declaring-page rule (SWE2-DATA, `progress.py` `cite_credits` / `family_rule_inputs`, recomputed today):
  - The VP8 page declares no accepted family.
  - Both functions are members of `libvpx VP8 decoder object`, which is declared elsewhere.
  - The base rule applies on this page, and both rows' anchors are strictly interior, so "All 2 rowed functions now measure A" is consistent with the rule in force.
- Missing 12: these are the 12 function-pointer targets that the -2 package's `0016F080` row names at their entry (`001260E7` … `00173450`, all ≥128 B, each cited once on the page). They are entry-only on this page and uncredited. The package does not claim them.
- Limits: body statements only, static evidence. The local draft and OPUS's re-read are not independent review; this record is.

## SWE2-AUDIT-SPEC narrowings

1. `rows.json` row `0017B580` (and so the page row). The column-start dword is read at `0017B5BE`, after the `0017A850` call returns, not at entry. Only `[rcx+0x1EB0]` is read before the call.
   - Old: `dword `[rcx+0x1E78]`*0x80 - 0x80 (read at entry) to dword `+0xF88``
   - New: `dword `[rcx+0x1E78]`*0x80 - 0x80 (read once, after the `0017A850` call, before the row loop) to dword `+0xF88``
2. `README.md`, paragraph 1. The count is wrong. The ingest's targets are 2 rowed + 1 skipped + 12 missing = 15.
   - Old: `The page named 3 F-frontier functions only at their entry.`
   - New: `The page named 15 F-frontier functions only at their entry: the 3 the first pass skipped (`0017AC50`, `0017B010`, `0017B580`) and the 12 function-pointer targets the `0016F080` row (opus-the-vp8-codec-interface-and-its-control--ee-1003-2) names at their entry; this pass drafted the 3, and the 12 stay entry-only (Missing: 12).`
3. `README.md`, paragraph 1. Neither row involves rotation helpers or a named import; the clause is carried over from the MSVC ordered-container package.
   - Old: `read every one of the 2 rows against the disassembly, including the rotation helpers' directions and every named import: all 2 stood.`
   - New: `read every one of the 2 rows against the disassembly, including the inline boolean-decoder reads and every table address: all 2 stood.`
