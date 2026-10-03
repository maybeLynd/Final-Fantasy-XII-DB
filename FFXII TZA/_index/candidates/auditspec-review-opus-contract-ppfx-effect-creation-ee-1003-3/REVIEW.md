# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-ppfx-effect-creation-ee-1003-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-PPFX-EFFECT-CREATION-EE-1003-CE65D` · Package: `_index/candidates/opus-contract-ppfx-effect-creation-ee-1003-3/` · Page: `17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 3 functions, 15 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 3 row(s), 15 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `00715A00` exact: zero dword -> `[d]` = 0, `[d+8]` = `02EA1720`; else dword copy, `movsxd [s+4]` low dword to `[d+4]`, `006DA880([01F3BA68], n+8, 00D99990, 0x9A, 0)`, `[b]` = n and p = b+8 (else 0), `[d+8]` = p, `memcpy` (`00861EBA`) of `movsxd [d]` bytes from `[s+8]`, the terminator at `[[d+8] + movsxd [d]]` with both re-read.
  - `00718350` exact: the `strlen` loop (`007183B0`-`007183B7`); `007153B0(t, n, 0)`; `[t]` = n (not the return), `memcpy` n+1 bytes to `[t+8]` read after the call; the null/zero path frees `[t+8]` - 8 through `006DA8A0([01F3BA68], ...)` unless it is null or `02EA1720`, then zeroes `[t]` and stores `02EA1720`.
  - `00718400` exact: `[t]` == 1 skips to the stores; `jge 2` / `jle 0x100` (signed) select the reallocation; 0x40 to `[t+4]`; `006DA880(..., 0x48, 00D99A08, 0xFB / 00D99A30, 0x11D, 0)`; 0x40 at `[b]`, p = b+8; the old buffer freed unless `02EA1720` or null with `[01F3BA68]` re-read; then `[t]` = 1, c and 0 at `[[t+8]]` / `+1` with `[t+8]` re-read.
  - Strings read from the image: `00D99990`, `00D99A08`, `00D99A30` each = '..\src\GPU\TinyEffect\TFXString.cpp'.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
