# SWE2-AUDIT-SPEC review: FABLE interior rows (fable-keymap-ini-file-format-and-default-contr-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-KEYMAP-INI-FILE-FORMAT-AND-DEFAULT-CON` · Package: `_index/candidates/fable-keymap-ini-file-format-and-default-contr-cloudint-1002/` · Page: `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 5 functions, 25 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 5 rows, 25 anchors; mechanically rejected 0, skipped 0, missing 0. Each row's sentence appears verbatim in the page's interior-citation section.
- Semantic pass: **all 5 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved, constants peeked). Every offset, operand width, compare signedness and branch polarity was checked. The task asks for at least 15 rows or all; the package has 5, so all were read.
- `00198670`: `movsx edx, byte [rcx+0x3A]; shr eax, 2; test al, 1; jne ret` makes the write path the bit-2-clear one. That path does `or dl, 4`, then `mov byte [rcx+0x3B], 1`, then `mov byte [rcx+0x3A], dl`.
- `001D8520`: the step is `01CEBBA8` (f32 1.0) when `00184950` returns 2 (`cmp eax, 2; jne`), else `01CEBB70` (f32 0.5). The sum is stored to `+0x60` (`001D8558`) between `comiss sum, [008C5B40]` (255.0) and the `jb`, and `movss` leaves the flags alone. On not-below, `+0x64` gets the immediate `0xC0C00000` (f32 -6.0) and `+0x60` = 255.0 - step. Otherwise `comiss [00900380] (63.0), sum; jb` returns when 63.0 < sum. When 63.0 >= sum, `+0x64` gets `0x40C00000` (f32 6.0) and `+0x60` = step + 63.0.
- `0024B0C0`: `B = [rcx+0x20] + 0x30`. `mov eax, edx; shr rax, 8` is a logical shift of the zero-extended `edx`. The first `movzx` word is at `B+0x14+rax*2`; `movzx eax, dl` is added to it; the second `movzx` word is at `B+0x14+rcx*2`. Then `movsxd rax, r8d` is added, and the return is `lea rax, [B + word[B+0x10] + rdx*8]`.
- `00797EE0` / `00797F20`: there are null exits on `rcx`, on `rdx` and on `[[rcx+0xDF8]+0x118]`. `movsx rax, byte [rdx]; and eax, 0x7F` indexes `01F3DA30`, then `movzx`, `sub rax, 0x1C`, `mov eax, eax` (zero-extended 32-bit result). The store is `mov byte [rax+rcx+0x30], 1` (respectively `0`) with `rcx` = the `+0x118` qword, as FABLE's re-read correction says. Every path ends with `xor eax, eax`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
