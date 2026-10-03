# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-fcp-character-parameter-block-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-FCP-CHARACTER-PARAMETER-BLOCK-HOMING-1` · Package: `_index/candidates/fable-fcp-character-parameter-block-homing-1003/` · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md` (commit `eea05327e`, reviewed at HEAD `db98e3d59`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 7 functions, 33 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 814, and every sentence is on the page verbatim.
- **rows.json.** 7 rows, 33 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass.** All 7 rows were read clause by clause against `disr.py` output of the certified image.
  - `00263810`:
    - `and al, 0xE0` / `cmp al, 0x60` / `je` takes the tail `jmp 002E9630`.
    - Otherwise `shr edx, 5` / `sub edx, 1` / `je` reads float `[[rcx+0xB8]+0x68]`, and `cmp edx, 2` (value 3) leads to the `+0xC0 × +0x24` arm. Every other value returns `xorps` 0.0.
    - `0x60 >> 5` = 3, so the value-3 arm is unreachable, as the sentence says.
    - Exact.
  - `00344050`: pop at +0x28 kept in `xmm6`. `0034BE50` gets the restored `rcx`, `rdx`, `r8` and `r9`. The tail is `jmp 0026AC70` with `rcx` = the incoming `rdx` and `xmm1` = the float. Exact.
  - `00349F10` and `00356740`: `002644E0(rdx)` at +0x23, then `00267F60(r9, xmm1)` at +0x2E. `0026A1A0(rdx, 0)` is called twice in `00349F10` and `0026A1A0(rdx, 1)` twice in `00356740`. Tails `jmp 00357BA0` at +0x67 / +0x6D with all four registers restored. Exact.
  - `00356AF0` and `00356F20`: `00267F90(r9, 0x30B)` at +0x28, `002644E0(rdx)` at +0x30, `00267F60` at +0x3B, then `0026A1A0(rdx, 0)` or `(rdx, 1)` twice. Tails at +0x74 / +0x7A. Exact.
  - `003573C0`: pop at +0x29 is v. Then `00267F90(r9, 0x30B)` at +0x38, `00267F90(r9, v)` at +0x42 and `0026A1A0(rdx, 0)` once. The tail at +0x77 is `jmp 00357B10`. Exact.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
