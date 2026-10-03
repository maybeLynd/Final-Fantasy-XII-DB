# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-measuring-text-by-drawing-it-with-the-ou-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEASURING-TEXT-BY-DRAWING-IT-WITH-THE-3D45F` · Package: `_index/candidates/opus-measuring-text-by-drawing-it-with-the-ou-ee-1003/` · Page: `99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0; mode `ee`, no family (the family-declaring-page rule does not apply).
- Semantic pass: **every row** (1 of 1) read clause by clause against a capstone decode of the certified image (SHA256 73461D08...). The extent is `002B5390`-`002B567B` (747 B = the kit's size). It is six chained .pdata entries that tile it exactly, so the first entry alone (`002B5390`-`002B53C4`) is not the body.
  - `002B5390`, stated exactly:
    - Entry and setup: a null `rcx` gives `xor eax, eax` and then the epilogue. Byte `[o+0x27]` is cleared. `s` = `[o+0x10]`, or `[o]` when that is null. `W` = `cvtdq2ps(movsx word [o+0x24])`. `M` = `rsp+0x30` (`002AC1E0`). Byte `M+0xA6` (`rsp+0xd6`) = `al` of `0039BAD0(rdx or [o+0x18])`. `g` = `[0209CC40]` (.data). `[g+0x10D0]` = `[o+0x28]` and `[g+0x1104]` = byte `M+0x9A` (`rsp+0xca`). Then `002B2150(&M, s, rsp+0x20, rsp+0x24)` and the copy back to `[o+0x28]`.
    - The fit test is `cvttss2si` of both values, `cmp edx, ecx; jg` (signed, truncated). On the fit path it writes `+0x22` = `n`, `+8` = `s`, `+0x26` = `s[n]`, `+0x10` = `s+1+n` or 0, and `+0x27` = 2 / 0 by `cmp [g+0x1104], 0x26; cmove`. `rax` is returned.
    - When `00254A10` returns 0, the same writes follow, with `or sil, 1` into `+0x27`.
    - Loop: it rebuilds `M` and `M+0xA6` each pass (the `g` fields are not re-seeded, and the sentence does not claim they are). The next token comes from `002B1FB0(s+off)`; a 0 result goes to the zero path. The offset is advanced. When `off < strlen(s)` it saves the byte, writes 0 and restores the byte after measuring. Then `comiss w, W; ja` (unordered = fits). A fit copies `[g+0x10D0]` to `[o+0x28]`.
    - Exit at `002B5655`: `or [o+0x27], 1`, then `off -= last len`, `+8` = `s`, `+0x22` = `off`, `+0x26` = `s[off]`, `rsi` = `s+off` when that byte is nonzero, else 0. The value is stored to `+0x10` at `002B561E` and returned.
    - Zero path at `002B55F0`: a null `s` or a 0-length token zeroes `+0x22`, `+0x26`, `+8` and `+0x10`, and returns 0.
  - Anchors `002B5449` call, `002B546E` jg, `002B54B1` call, `002B559A` mov, `002B55C9` ja: all strictly inside the 747-byte extent with those mnemonics.
- Limits hold: body statements only, static evidence. OPUS's re-read is not independent review; this record is.
