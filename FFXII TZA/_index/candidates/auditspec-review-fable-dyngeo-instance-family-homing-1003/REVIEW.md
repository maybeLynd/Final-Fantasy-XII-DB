# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-dyngeo-instance-family-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-DYNGEO-INSTANCE-FAMILY-HOMING-1003` · Package: `_index/candidates/fable-dyngeo-instance-family-homing-1003/` · Page: `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md` (commit eea05327e; reviewed at HEAD f8b2904c0, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 3 functions, 15 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 3 rows and 15 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. All 3 rows are on the page at lines 874–876 (heading at line 868), byte for byte.
- Semantic pass: **every row** was read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`001B6110`: exact.**
    - A null `rcx` returns (`001B6113`).
    - +0x24 is `001FDE60(rcx, rsp+0x28)`, and n = `0019CA80(0019CE20(), [rax])` (+0x2D / +0x38).
    - The L release uses a `jle` (signed) test and a null test (`001B6178`).
    - The list head is n+0x38. `cmp rcx, rbx` / `cmove` stops the walk at the head.
    - The node test walks the chain `[+0x50]` through `+0x78` up to `02CBB900` (`001B61B0`), then `cmp dword [+0x74], 0` / `ja` (unsigned non-zero).
    - The a/q loop: `add r8, rdx` with `edx` = zero-extended dword `p+0x38`, `rax = [rax]`, repeated while `r8 == rax` (`001B6200`).
    - Then `00213540(rdi = incoming rcx, a + dword p+0xF8)` (`001B6212`).
  - **`001B6230`: exact.** It is the same body with `001FDF10` at +0x24 and `00213560` at `001B6332`.
  - **`006C8BF0`: exact.**
    - `006CB2A0` is called with the registers untouched (`006C8C0F`).
    - Then `006DA470` at +0x40 (`006C8C30`), with `rcx = rcx+0x880`, `edx`, and `r8 = [rsp+0x60]`, the entry `rsp+0x28` (5th argument).
    - `r9d = [rsp+0x68]` is the 6th argument as a dword. `[rsp+0x20]` = incoming `r8` and `[rsp+0x28]` = incoming `r9d`.
    - `xor eax, eax` returns 0.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
