# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-the-world-tick-and-the-field-frame-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-WORLD-TICK-AND-THE-FIELD-FRAME-HOM` · Package: `_index/candidates/fable-the-world-tick-and-the-field-frame-homing-1003/` · Page: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` (commit b35f1958c; reviewed at HEAD 15ec1ea71, and the page is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 5 functions, 21 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 5 rows and 21 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. The README count sentence ("5 staged with 21 anchors ... 0 ... 0 ... 0") matches. All 5 rows are on the page at lines 2854-2858 (heading at line 2848), byte for byte.
- Homing premise: each body calls a function the page cites.
  - `002DF1E0` → `001DBF00`.
  - `002EC630` → `00426E20`, which leads the heading `SWE2-EC7-72 update - 00426E20`.
  - `003EB190` → `003EB470`, which leads a row.
  - `00473490` and `004734C0` → `00466C40` / `00466BB0`, each of which leads a row.
- Semantic pass: **every row** was read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`002DF1E0`: exact.**
    - `test edx, edx` / `jg` (`002DF1E6`, signed).
    - When `edx <= 0`, the tail jump goes to `001DBF00` with `ecx` = 1, `edx` = 0, `r8d` = the incoming `ecx` and `r9d` = the incoming `r8d` (`002DF1F7`).
    - Otherwise `r9d` = `edx`, and `[rsp+0x20]` = `r8d` (`002DF1FF`). Then `call 001DBFA0` at +0x2C (`002DF20C`) with (1, 0, `ecx`, `edx`, `r8d`), and its `eax` is returned.
  - **`002EC630`: exact.**
    - It returns 0 for a null `rcx` or `cmp dword [rcx], -1` (`002EC639`).
    - It skips for word `0xFFFF` (`002EC641`).
    - It forms `rcx` = `movsx` word * 0x740 (`002EC64B`) + qword `[022C6F28]`. The `je` tests the sum, which is "that pointer is non-null".
    - It tests dword `+0x284` (`002EC65B`), then `call 00426E20` (`002EC664`).
    - Every path past the first guard returns `mov eax, 1`.
  - **`003EB190`: exact.**
    - `cmp ecx, 0x1F` / `ja` (`003EB193`, unsigned), which returns with no work.
    - Slot = `02B5EA20 + movsxd(ecx)*8`. A non-null slot goes to `call 003EB470` (`003EB1C9`), then the slot is cleared (`003EB1CE`).
    - Then `call 003EB250` at +0x52 (`003EB1E2`) with `rcx` = the incoming `rdx`, `edx` = `r8d`, `r8d` = `r9d` and `r9d` = `[rsp+0x50]` (the fifth argument after `push` + `sub 0x20`).
    - The result is stored in the slot (`003EB1F1`) and returned in `rax`.
  - **`00473490`: exact.** It runs `call 00466C40(ecx)` (`0047349D`), keeps the result in `xmm6`, runs `call 00466C80` at +0x17 with the same `ecx` (`004734A7`), then `subss xmm0, xmm6` (`004734AC`): the second minus the first.
  - **`004734C0`: exact.** It runs `call 00466BB0(ecx)` (`004734CD`) into `xmm6` and `call 00466C40(ecx)` (`004734D7`), then `subss xmm6, xmm0` (`004734DC`) and `movaps xmm0, xmm6` (`004734E0`): the first minus the second.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
