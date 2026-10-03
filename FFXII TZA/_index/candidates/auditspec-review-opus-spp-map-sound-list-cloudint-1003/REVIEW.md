# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-spp-map-sound-list-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SPP-MAP-SOUND-LIST-CLOUDINT-1003-30693` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-spp-map-sound-list-cloudint-1003/` · Page: `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 2 rows, 10 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 2 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 2, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `00363410`: for `c` != 0, `movzx` byte `022CBB2D` is compared with the full `ecx`. Equal goes to the store-only path at `00363475`; otherwise `00363840()` runs and the byte is stored. For `c` = 0: dword `022CBA70` != 0 and `edx` > 0 (`jle`, signed) calls `002DF190(dword 022CBA7C, edx)`. `edx` <= 0 calls `002DF0F0(0, dword 022CBA7C)`. `022CBA70` = 0 does the same, but `je` skips it when `022CBA7C` is 0. All four paths end by zeroing `022CBA70` and storing `bl` = 0 at `022CBB2D`. Exact.
  - `003DF550`: `ecx`/`edx` = `movsx` words `+0x2c`/`+0x2e`, `r8` = qword `+0x18`, `r9d` = dword `+0x30`, fifth argument `&s` (`s` = `[rsp+0x30]`). `s+0` = dword `+0x34`, `s+8` = `ebx` (low dword of `rcx`), `s+0x10` = `003DF2C0`, `s+0x18` = 0. Byte 3 is stored at `+0x10` after the call. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
