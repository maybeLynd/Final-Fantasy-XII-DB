# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-class-descriptor-and-metadata-system-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CLASS-DESCRIPTOR-AND-METADATA-SYSTEM-AB50C` · Package: `_index/candidates/opus-class-descriptor-and-metadata-system-ee-1003/` · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The narrowing is one width, on row `00631A60`. Field `+0x20` is cleared as a dword, not a qword, so bytes `+0x24`..`+0x27` are never written. Row `006458A0`, including OPUS's correction, is exact.

## SWE2-AUDIT-SPEC narrowing

- **`00631A60`.** Replace

  > zeroes `+0x20`, `+0x28`, `+0x40`, `+0x48` and `+0xC0` to `+0xE0`

  with

  > zeroes the dword `+0x20` (bytes `+0x24`..`+0x27` are not written) and the qwords `+0x28`, `+0x40`, `+0x48` and `+0xC0` to `+0xE0`

  Site: `00631AC0 lea rax, [rbx+8]` / `00631ACF mov dword ptr [rax+0x18], ebp`, which is `rbx+0x20` written with a 4-byte store, followed by `00631AD2 mov qword ptr [rax+0x20], rbp`, which is `rbx+0x28`. No other store in the body reaches `+0x24`. The anchors are unchanged.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against a full linear decode of the certified image (SHA256 73461D08..., capstone, function-list extents):
  - `00631A60` (474 B). The epoch is dword `[[gs:0x58] + [02EAED3C]*8 + 4]`. `00631AA9 cmp [02CF94EC], eax` / `jg` (signed) branches to `008092FC(&guard)` (`00631BCD`); then `cmp [02CF94EC], -1` / `jne`. The static record: `01F2E330`/`01F2E338` <- `01F2E330`, `01F2E340`/`01F2E348` <- `01F2E340`, `01F2E358`/`01F2E360` <- `01F2E358`, dword `01F2E350` <- 0, all .data. `00808B90(008AF490)` (`00631C24`), `0080929C(&guard)`. Body: self-links at `+8`/`+0x10`/`+0x18` (three qwords from `rbx+8`), `+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0`, `+0xB0`. Zeroed: dword `+0x20` (see the narrowing), qwords `+0x28`, `+0x40`, `+0x48`, `+0xC0`..`+0xE0`. `+0x30` <- `00D569B8` (.rdata). Dwords `+0x38` = 0x60 (`00631AED`) and `+0x3C` = 8. `+0x70` <- `01F2E330`, `+0x78` <- `rdx`. `+0xE8` <- dword `[02CF8260]`, then `inc dword [02CF8260]` (`00631B87`). `+0xF0` <- `r8d`. Qword `+0xF4` and dword `+0xFC` <- 0, which is `+0xF4`..`+0xFF`. `+0xEC` <- -1. `[rbx]` <- `00D581C0` at `00631B09`, then `00D56A38` at `00631B8D`. Returns `rbx`.
  - `006458A0` exact (800 B). `006461B0(rcx)` (`006458C0`); `[rbx]` <- `00D61EA0`. Loop: `edx` = 0x80, stride 0x80 from `rbx+0x50`, `sub rdx, 1` / `jne` (`00645977`). I resolved the overlapping qword and dword stores of each entry in order. The final layout is: 1.0 at `+4`, `+0xC`, `+0x18`, `+0x30`, `+0x34`, `+0x38`, `+0x3C`, `+0x60`, `+0x6C`; 50.0 (0x42480000) at `+0x54` (`00645938`); 100.0 at `+0x58`; 0x7F7FFFFF at `+0x70`; zero everywhere else. `+0x2C` is written 1.0 and then 0, and `+0xC` is written 0 and then 1.0. The unrolled tail at `+0x4050`..`+0x40CF` resolves to the same layout. Then 0x3E4CCCCD (0.2) at `+0x40D0`/`+0x40D4`/`+0x40D8`. 1.0 at `+0x40DC`, `+0x40EC`, `+0x40FC`, `+0x4104`, `+0x4108`, `+0x410C`; 100.0 at `+0x40F0`; 20.0 (0x41A00000) at `+0x40F4`. The other dwords up to `+0x412F` are zero (the high halves of the qword stores, plus `+0x40E4`, `+0x4114`, `+0x4118`..`+0x412F`), so the correction is borne out. `00615CD0(rbx+0x4130)` (`00645AEF`). Qwords `+0x4158`..`+0x41C8` are zero; byte `+0x41D0` = 1. Five writes each re-read dword `[member+0x1C]`, `shr 7` / `test al, 1` / `jne` (bit 0x80): bytes `+0`..`+3` = 1, 1, 2, 2, then `or ecx, 0x40` (`00645BA7`). Returns `rbx`.
  - Anchors: all ten are instruction boundaries strictly inside their bodies and decode to the recorded mnemonics.
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
