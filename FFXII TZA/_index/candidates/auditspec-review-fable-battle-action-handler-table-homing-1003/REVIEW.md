# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-battle-action-handler-table-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-BATTLE-ACTION-HANDLER-TABLE-HOMING-100` · Package: `_index/candidates/fable-battle-action-handler-table-homing-1003/` · Page: `07-Combat-Action/Action-Dispatch/battle-action-handler-table.md` (commit `eea05327e`, reviewed at HEAD `db98e3d59`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

Both rows are right in every clause they state. Each leaves out the first argument of the angle call `003A1BB0`, which is `xmm0`, the float returned by the `00265200` call just before it. `003A1BB0` uses that value: `movaps xmm6, xmm0` (`003A1BB9`), then `subss xmm0, xmm6` after `atan2f` (`003A1BE5`). So the argument list as written is incomplete.

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 795, and both sentences are on the page verbatim.
- **rows.json.** 2 rows, 10 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass.** Both rows were read clause by clause against `disr.py` output of the certified image.
  - `00346780`:
    - `00267E10(r9)` gives `edi`, and `00267DB0(r9)` gives `xmm6`, which is then `mulss` by `[01CEBB70]` (0.5).
    - A = `00265060(rdx)` (`rsi`) and B = `00265060(00264010(edi))` (`rbx`).
    - The call at +0x65 is `00265200(rdx)`.
    - At +0x8B: `xmm1` = `xmm6`, `xmm2` = `[rsi]`, `xmm3` = `[rsi+8]`, `[rsp+0x20]` = `[rbx]` and `[rsp+0x28]` = `[rbx+8]`. `xmm0` is the +0x65 result, which no instruction in between overwrites.
    - The tail at +0xB4 is `jmp 0026B4E0` with `rcx` = `r14` (the incoming `rcx`) and `edx` = the result.
  - `00346EF0`:
    - Three `00267DB0(r9)`: f1 = `xmm8`, f2 = `xmm6`, f3 = `xmm7` ×0.5.
    - B = `00265060(rdx)`. The call at +0x60 is `00265200(rdx)`.
    - At +0x7E: `xmm1` = f3, `xmm2`/`xmm3` = `[rbx]`/`[rbx+8]`, `[rsp+0x20]` = f2, `[rsp+0x28]` = f1, and `xmm0` = the +0x60 result.
    - The tail at +0xA7 is `jmp 0026B4E0`.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing

- `00346780`, replacement wording: "calls `00267E10(r9)` and `00267DB0(r9)`, scaling the float result by 0.5 (`01CEBB70`); takes pointer A = `00265060(rdx)` and pointer B = `00265060(00264010(the 00267E10 result))`; calls `00346780+0x65` with `rdx`, then `00346780+0x8B` with `xmm0` = that call's float result, `xmm1` = the scaled float, `xmm2`/`xmm3` = floats A `+0`/A `+8` and stack arguments B `+0` (first) and B `+8` (second); tail-jumps to `00346780+0xB4` with the incoming `rcx` and that call's result in `edx`"
- `00346EF0`, replacement wording: "calls `00267DB0(r9)` three times (results f1, f2, f3, with f3 scaled by 0.5 (`01CEBB70`)); takes pointer B = `00265060(rdx)`; calls `00346EF0+0x60` with `rdx`, then `00346EF0+0x7E` with `xmm0` = that call's float result, `xmm1` = scaled f3, `xmm2`/`xmm3` = floats B `+0`/B `+8` and stack arguments f2 (first) and f1 (second); tail-jumps to `00346EF0+0xA7` with the incoming `rcx` and that call's result in `edx`"
- The anchors stay as they are.
