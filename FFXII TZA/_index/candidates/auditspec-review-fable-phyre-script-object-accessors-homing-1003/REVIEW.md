# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-phyre-script-object-accessors-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-PHYRE-SCRIPT-OBJECT-ACCESSORS-HOMING-1` · Package: `_index/candidates/fable-phyre-script-object-accessors-homing-1003/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md` (commit b7c6eb07d; reviewed at HEAD 431017e52, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 32 rows, all small accessor bodies (36 to 133 bytes). I read all 32 clause by clause against the full listings, more than the 15 required. All 147 anchors are correct and every row holds as written.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 32 functions, 147 anchors`, `ALREADY` and `FAILS 0`, exit 0. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 32 rows, 147 anchors, `mode: homing`; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read against `disr.py` output of the certified image (SHA256 73461D08...). The points that needed care:
  - `005CC4E0`: the 5th argument is `[rsp+0x50]` after `push rsi` + `sub 0x20` (`005CC4FB`). `add qword [rax], 8` (`005CC508`), then `edx` = dword `[new-8]` and `call [rcx+8]` with `rcx` = the incoming `rdx`. `005A6670()` is called with no argument set up (`005CC51D`) and compared with the incoming `r8` (`005CC522`, `jne` -> 0). The success path stores `[r9+8]` = the result dword, zeroes `[r9]` and returns 1. Null `rdx` returns 0.
  - `005FFB10`: `+0x1d` = `005FFB2D` -> `00683B10(rdx)` = `A`. `B` = `00811470(rdx, -1, 0)`, then `00811130(rdx, -2)` and `005F86B0(rdx)`. On non-null it calls `call [rdi+8]` with (result, `edx` = `ebp` = `B`, `r8` = `A`). It returns 0 on both paths.
  - `0063C220` / `0063C270` / `0063C2C0` / `0063C400`: each stores `bl` / `bx` / `ebx` / `rbx` (the `00811470` result) to `[r8]` after `00811130(rdx, -2)`. `0063C3B0`: `[rsp+0x20]` = result and `[rsp+0x28]` = 0, then `movdqa [rdi]` (an aligned 16-byte store).
  - `0063D200` / `0063D240`: `0080F420(rdx, 1)`, then `xmm1` = `movss [r8]` or `movsd [r8]` + `cvtpd2ps`, and `jmp 00810640` with `rcx` = `rdx` (a tail jump, not a call).
  - `006A76E0`, `006A8DF0`, `006A8E50`, `006AB030`, `006AF060`, `006B38C0`, `006B5310`, `006B5360`, `006B5460`, `006B54E0`, `0079A770`, `0079A8B0`, `0079AB20`, `0079AB80`: the null-lookup exit returns the lookup's own `rax`, which is 0, so "returns 0" holds. Each success path ends with `mov eax, 1`.
    - Value forms checked: `movzx ebx, al` (`006A8E1B`, `006A8E8E`). `add rax, 0x30` only when non-null (`006AB056`/`006AB058`). `movsxd rbx, eax` (`0079A79B`, sign-extended). `mov edx, ebx` (`0079AB56`, zero-extended). `cvtsd2ss` (`0079A8EE`). `xmm0` passed unchanged (`0079ABBC`).
    - `rcx` = `result + movsxd [rcx+0x10]` (signed) for the `006B5xxx` and `0079ABxx` rows. The globals are `02CF8470`, `02E4D630`, `02E518D0` (with `result+8`) and `02E404B0`.
    - The `006B5460` / `006B54E0` null-result arm is `0080F420(rdx, 1)` + `00810620(rdx)`, which also returns 1.
  - `006A8D90` / `006C7580`: `+0x1b` -> `008113D0(rdx, -1)` (`r8` not loaded), `setne sil`, `00811130(rdx, -2)`, the lookup, and `call [rdi+8]` with `edx` = `movzx sil`. They return 0.
  - `006ACF30` / `006AD7A0`: `+0x29` -> `0018A4A0(r8+8, P+8 or 0)`. The dwords `+0xC8`, `+0xD0` (and `+0xD4`) are read from `P` unconditionally, so a null `P` is not checked, as the row says. Each returns the last copied dword in `eax`.
  - `006BFDE0`: `00811640(rdx, -1, 0)` -> `xmm6`, then `00811130`, `006BFB10`, and `call [rdi+8]` with `xmm1` = `xmm6`. It returns 0.
  - `006C4AC0`: `006C6D60` -> `P` with no null test. `[r8]` = `[P]`, `00646C00(r8+8, P+8)`, dwords `+0x18`/`+0x1C` copied, then `+0x49` = `006C4B09` `jmp 006C54D0` with (`r8+0x20`, `P+0x20`).
  - `007913D0`: `+0x26` = `007913F6` -> `007938F0(r8+8, P+8)`. Byte `+0x50` is copied, and `eax` = `movzx` of it.
  - `006B5560`, `0079ABF0`: a single conditional pointer call, then `xor eax, eax`.
- README count sentences checked against `rows.json`: "named 32 F-frontier functions", "32 staged with 147 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): none of the 32 belongs to an accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
