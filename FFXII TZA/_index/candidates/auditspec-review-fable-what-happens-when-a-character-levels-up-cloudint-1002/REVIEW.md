# SWE2-AUDIT-SPEC review: FABLE interior rows (fable-what-happens-when-a-character-levels-up-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-WHAT-HAPPENS-WHEN-A-CHARACTER-LEVELS-U` · Package: `_index/candidates/fable-what-happens-when-a-character-levels-up-cloudint-1002/` · Page: `13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 5 functions, 17 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 5 rows, 17 anchors; mechanically rejected 0, skipped 0, missing 0. Each row's sentence appears verbatim in the page's interior-citation section.
- Semantic pass: **all 5 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved). Every offset, operand width, loop bound and save/restore was checked. The task asks for at least 15 rows or all; the package has 5, so all were read.
- `00290610`: `mov rax, [0209BE80]; and dword [rax+0x10F68], 0xFFFFDFFF; ret` clears bit 13 (0x2000).
- `003A72A0`: `rdi = [02EBEFB0]`, `ecx = 0x10`, `rep stosq` with `rax = 0` zeroes 0x80 bytes. The pointer is then reloaded before each of the two `edx = 0` dword stores at `+0x80` and `+0x84`. `rdi` is saved in its home slot `[rsp+8]` and restored at `003A72BF`.
- `003A8000`: `rcx = 0` is stored as qwords at `[02EBEF98]+0` and `[02EBEF98]+8`, with the pointer reloaded between the stores.
- `003A8900`: there are qword zeroes at `+0x8` and `+0x10`, then a dword zero at `+0x0`, with the pointer reloaded before every store, including inside the loop (`003A8930`). The loop runs `rax` from 0x18, `add rax, 8; cmp rax, 0x118; jl`, and stores `0xFFFFFFFF` at offsets 0x18..0x110: (0x110 - 0x18) / 8 + 1 = 32 stores.
- `0046F330`: `mov dword [rcx], 0xC0000000`, `rbx = rcx+0x20`, `edi = 0xC0`. Each pass does `xor ecx, ecx; call 0020E620; mov [rbx], eax; rbx += 4; sub rdi, 1; jne`, which is 192 calls, the last store at 0x20 + 4 * 191 = 0x31C. `rbx` is saved in its home slot and `rdi` is pushed, and both are restored.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
