# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-derived-call-signatures-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-DERIVED-CALL-SIGNATURES-EE-1003-5E6A8` · Package: `_index/candidates/opus-derived-call-signatures-ee-1003/` (reviewed at HEAD `a028be1b9`) · Page: `00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row. It was read clause by clause against a raw capstone decode of the certified image. This session checked the image hash: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. The row holds as written, including the OPUS correction (both dword groups are now stated as signed and the two bytes as zero-extended). No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0` and exited 0. The row is already in the page block `## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)`, line 382 (heading at line 378).
- **Counts.** 1 row, 5 anchors. The listing (`0079D730`-`0079D84B`, function-table size 0x11C) ends in `ret` at `0079D84B`, followed by the jump-table data.
- **Constants and table read from the image.**
  - `008C5B40` is the float 255.0 and `00D6B968` is the float 1023.0.
  - The dword table at `0079D84C` (image base + 0x67D84C) has 18 entries, each + 0x120000: [0]-[5] `0079D752`, `0079D766`, `0079D77A`, `0079D78E`, `0079D7A2`, `0079D7B6`; [6]-[9] `0079D7CA`, `0079D7DE`, `0079D7F2`, `0079D806`; [10]-[15] all `0079D848`; [16] `0079D831`; [17] `0079D81A`.

Per row:

- **`0079D730`**: exact.
  - `0079D730`/`0079D732`/`0079D735`: `dec edx`, `cmp edx,0x11`, `ja 0079D848`, so `k` - 1 above 0x11 unsigned (including `k` = 0) takes the 0.0 arm.
  - `0079D73B`-`0079D750`: `movsxd`, the image-base `lea`, the table load at +0x67D84C, then `jmp rdx`.
  - `k` 1-6 (table [0]-[5]): `movd` + `cvtdq2ps` of dwords +0x414, +0x420, +0x42C, +0x418, +0x424, +0x430, each `divss` by `008C5B40` (255.0), e.g. `0079D75D`.
  - `k` 7-10 (table [6]-[9]): `movd` + `cvtdq2ps` of dwords +0x41C, +0x428, +0x434, +0x438, each `divss` by `00D6B968` (1023.0), e.g. `0079D7D5`. `cvtdq2ps` is a signed int32 conversion, so "signed" holds for both groups.
  - `k` 17 (table [16], `0079D831`): `movzx eax, byte [rcx+0x44D]`, `divss` by 255.0 at `0079D83F`. `k` 18 (table [17], `0079D81A`): `movzx` byte +0x44E, `divss` by 255.0 at `0079D828`.
  - `k` 11-16 (table [10]-[15]) go to `0079D848` `xorps xmm0,xmm0` / `ret`. Every result returns in `xmm0`.

**1 of 1 exact.** All 5 anchors were checked.

## SWE2-AUDIT-SPEC limits

- Body statements were checked against the bytes. Meanings were not reviewed.
- The row names no callee; no callee behaviour was needed.
- README.md records 1 function as missing (`0085DDE0`). It is outside this review.
- This review is a non-author read. It does not replace a live check of any behaviour.
