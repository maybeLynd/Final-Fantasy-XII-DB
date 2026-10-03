# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-character-render-object-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CHARACTER-RENDER-OBJECT-HOMING-1003` · Package: `_index/candidates/fable-character-render-object-homing-1003/` · Page: `17-Presentation-Rendering/Character-Rendering/character-render-object.md` (commit eea05327e; reviewed at HEAD f8b2904c0, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 3 functions, 15 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 3 rows and 15 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. All 3 rows are on the page at lines 1296–1298 (heading at line 1290), byte for byte.
- Semantic pass: **every row** was read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`001E5370`: exact.**
    - n is computed with the `0x2aaaaaaaaaaaaaab` multiply / `sar 2` / sign fix, a signed /0x18 (`001E53A8`).
    - `cmp edi, edx` / `jbe` is an unsigned 32-bit "at most n" (`001E53BB`). That path calls `001E3D80(rcx, [rcx] + rdi*0x18, [rcx+8])` (`001E5411`, `rdi` zero-extended from `edx`).
    - Otherwise: +0x52 (`00212C20` on `rsp+0x28`); then +0x81 (`001E53F1`) with `rcx`, `[rcx+8]`, `edx - n` and `r9` = that result; then +0x8C (`001E53FC`) on the same local.
  - **`001F4C50`: exact.**
    - Three zeroed qwords, then `001EDF00(rcx+0x18, 008C5F58)` (`001F4C88`).
    - For B = `rcx+0x20` the stack slot is `rsp+0x90`; for B = `rcx+0x58` it is `rsp+0x98`, each named with `008F3CB0`. Each B gets `[B+8..B+0x20]` = 0 and dword `B+0x28` = 0, then `001EDF00(B+0x30, rax)` (`001F4CD2` side). Then `[B+8]` = `[B+0x10]` = `B+8`, and `B+0x18`, byte `B+0x20` and dword `B+0x28` = 0.
    - Then `001F8A70(rcx, edx)` (`001F4D3D`), and a loop of `edx` iterations (`001F4D81`) calling +0x124 (`001F4D74`, `00199DB0`) with `rbp` = `rcx+0x20`, `rsp+0x28` → `rcx+0x58`, `rsp+0x90` → `[rcx] + i*0x18`, and `r9b` = byte `[rsp+0x88]`.
    - `[rsp+0x88]` is the entry `rsp+0x10`, the `rdx` home slot. The body writes only `[rsp+8]`, `+0x90` and `+0x98` of its home area, so "never writes" holds.
  - **`0042E130`: exact.**
    - `00426220(rcx, [rdx+8])` (`0042E13D`), and a non-zero result returns it (`0042E144`).
    - Otherwise `cmp word [rcx+0x3fa], 0x1000` / `jae` skips the +0x27 call (`0041FC80`, `0042E157`). So the call runs below 0x1000, unsigned.
    - Then the tail jump at +0x34 (`00423A10`, `0042E164`).
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
