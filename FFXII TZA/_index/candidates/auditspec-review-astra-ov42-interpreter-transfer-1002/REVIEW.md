# SWE2-AUDIT-SPEC review: ASTRA OV-42 queue/interpreter transfer

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; independent of ASTRA and FABLE) ·
2026-10-03 · Task: `ASTRA-REQ-SPEC-OV42-QUEUE-INTERPRETER-TRANSFER-1002` · Package:
`_experiments/evidence/ov42-interpreter-transfer/` (publisher commit `76dfc5dc6`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped as the package states. These are conditional transfer and arithmetic predictions. They establish no
same-cell binding, no actual declarations or kind, no valid four writable bytes, no stack or lifetime facts and no
natural command.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`00309C00`**: reads DWORD `022C2178` and returns 0 when it is -1. Otherwise, when `rdx` is non-null, it does a
  raw `mov dword [rdx],eax` (`00309C13`). There is no tag and no typed POPV store, so the 4-byte destination
  premise is real. It then sets `022C2178` = -1 and returns 1.
- **`00267FC0` (PUSHV)**: the width comes from `record bits 28..31` through a 6-entry image-base-relative table at
  `002680E8`, decoded from the image. The arms in order are u8 (`movzx byte`), s8 (`movsx byte`), u16, s16, s32
  (dword) and f32 (`movss`).
  - The kind comes from the separate word `[rbp-2Ch]`: kind 1 writes tag 1 and copies the payload DWORD to `+184h`;
    kind 2 writes tag 2.
  - Both arms refuse at depth ≥ 3Fh, which gives the "0–62 before a successful PUSHV" premise.
- **`00267E10`**:
  - depth ≤ 0 returns 0;
  - otherwise it decrements the depth and reads the tag: tag 1 is an exact `mov eax,[+184h]`, tag 2 is
    `cvttss2si`;
  - any other tag calls `008620C0(1)` and then reaches the zero return only if that handler returns normally.
- **`00348870`**: first pop → `ebx`, second pop → `eax`, then `edx=ebx`, `ecx=eax` into `0030EEA0`.
- **`0030EEA0`**: `cmp edx,-1` maps to `0FFFFh`, otherwise `add bx,0D0h`. Only `bx` (low 16) is used afterwards
  (`movzx r8d,bx`, `mov [rax+758h],bx`). So the low 16 bits plus a non-sentinel DWORD are sufficient, exactly as
  stated.
- **Arithmetic, recomputed:**
  - 511..534 − D0h = 303..326;
  - masked to u8 that is 47..70, which decodes to 255..278;
  - `0x0000012F` is a positive binary32 subnormal, so `cvttss2si` gives 0, which decodes to 208;
  - s16 can only produce -1 at low16 `FFFF`, which is the unavailable word `CF`.

## SWE2-AUDIT-SPEC reproduction (disposable copy, run from the repository root)

- `prove.py` (proof-02, current driver `9056e01f`) re-run: exit 0, stdout identical, output **byte-identical** to
  `result-02.json`.
- `control.py` (control-01, `355c3b82`) re-run: exit 0, stdout identical. The three actual upstream refusals
  (missing capture receipt, failed upstream capture, missing historical observations) all exit 1 with no result.

## SWE2-AUDIT-SPEC limits (unchanged)

- EXP013's 14 isolated calls are retained, not credited.
- MXCSR exception masking is not proven.
- The resolver/same-cell binding and the authored descriptor dataflow are the next discriminator.
