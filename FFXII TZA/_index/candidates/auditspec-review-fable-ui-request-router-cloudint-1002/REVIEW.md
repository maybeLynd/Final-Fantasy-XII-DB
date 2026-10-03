# SWE2-AUDIT-SPEC review: FABLE interior rows (fable-ui-request-router-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-UI-REQUEST-ROUTER-CLOUDINT-1002` · Package: `_index/candidates/fable-ui-request-router-cloudint-1002/` · Page: `16-UI/Request-Router/ui-request-router.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 8 functions, 38 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 8 rows, 38 anchors; mechanically rejected 0, skipped 0, missing 0. Each row's sentence appears verbatim in the page's interior-citation section.
- Semantic pass: **all 8 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call and jump offset, argument register, compare signedness and branch polarity was checked. The task asks for at least 15 rows or all; the package has 8, so all were read.
- `001986E0`: `movsx edx, byte [rcx+0x3A]; shr eax, 2; test al, 1; je` tests bit 2; on the set path `and dl, 0xFB`, `mov byte [rcx+0x3B], 1`, `mov byte [rcx+0x3A], dl`; the clear path goes straight to `ret`.
- `0020E5C0`: the incoming `rcx`/`rdx`/`r8` are saved in `rsi`/`rdi`/`rbx` without being changed before `call` at `0020E5D8`. Afterwards `rcx = rax`, `rdx = rsi`, `r8 = rdi`, `r9 = rbx`, then `jmp` at `0020E5F8` (+0x38).
- `0024AB30`: `cmp dword [02091094], 0; je` return; `call` at +0xD; `cmp eax, 4; je` return; `mov ecx, 0x80000` then `jmp` at +0x20.
- `00290780`: `test ecx, ecx; je` takes the 0 arm, `cmp ecx, 1; jne` returns. The 1 arm reads `[0209BE80]+0x10FB0`, returns on null, calls at +0x20, re-reads `0209BE80` at `002907A5`, stores qword 0 at `+0x10FB0`, and tail-jumps at +0x3B. The 0 arm reads the same qword, returns on null, and otherwise tail-jumps at +0x57 with it in `rcx`. FABLE's re-read correction is in the text.
- `002E0E30`: the call is at +0x4. `cmp eax, 0x13; ja 002E0F15` (`xor eax, eax`) is unsigned. The table at `00120000 + 0x1C0F1C` = `002E0F1C` was read from the image: slots 0-7 go to `mov eax, 1..8`, slot 8 goes to `002E0F15 xor eax, eax`, slots 9-0x11 go to `mov eax, 9..0x11`, slot 0x12 goes to `002E0F0B mov eax, 0x13`, and slot 0x13 goes to `002E0F01 mov eax, 0x12`. That is exactly the stated mapping, including the 8-to-0 slot and the 0x12/0x13 swap.
- `0035BAA0`: `cmp ecx, [022C8070]` precedes `mov ebx, ecx; je` return. The first call at +0x10 sees the untouched incoming `rcx`, the second call at +0x18 gets `movzx ecx, bl`, and `xor ecx, ecx` comes before the `jmp` at +0x24.
- `00428F30`: the base `[022C6F28]` is loaded once into `rdi`, and the start index is `[rdi+0x48800]` (`cmp ebx, -1; je` exits). Each pass forms `movsxd` index `* 0x740 + rdi`, loads the next index with `movsx ebx, word [rcx+4]`, adds `0x5F0`, calls at +0x38, and loops on `cmp ebx, -1; jne`.
- `0046D0A0`: the three `jne` exits are `byte [rcx] == 1`, `byte [rcx+7] == 0` and `word [rcx+0x1C] == 6`. Then `mov ecx, [rcx+0x18]; test ecx, ecx; jg 002DF690` at +0x17 is the signed > 0 conditional tail jump, and the fall-through is `ret`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
