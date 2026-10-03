# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-spatial-audio-object-model-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-SPATIAL-AUDIO-OBJECT-MODEL-10` · Package: `_index/candidates/fable-home-the-spatial-audio-object-model-1002/` · Page: `18-Audio/the-spatial-audio-object-model.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 8 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 2 rows, 8 anchors; mechanically rejected 0, skipped 0, missing 0. Each row's text is on the page verbatim.
- Semantic pass: **both rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved). Every call offset, branch polarity and register move was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `00210BE0`: `mov eax, r8d; test edx, edx; mov edx, eax; mov r8, r9; jne`. The flags come from the incoming `edx` before it is overwritten. Zero falls through to `rcx = [rcx+8]` and `jmp 0021B200` at +0x10; non-zero goes to `rcx = [rcx+0x10]` and `jmp 00219BC0` at +0x19. Exact.
- `002DF280`: `cmp ecx, -1; jne` -> `xor eax, eax; ret`; otherwise `bts ecx, 0x1F` and `jmp 002DEFA0` at +0xC, with no other register touched. Exact.
- Sites: `001DBE00` + 0x35 = `001DBE35 jmp 00210BE0`; `003A0E50` + 0x25 = `003A0E75 jmp 002DF280` (the bit-30-clear arm after `bt ecx, 0x1E; jae`).
- Host: `001DBE00` is one of this page's own functions. It is read at L930 as the tail of the page's `002DEFA0` (SWE2-EC7-75), and it has its own row in the page's FABLE interior-citation section (L981). `003A0E50` is a link in the page's CO-7 descriptor chain (L607), and L614-L615 read its argument swap. `002DF280`'s tail target `002DEFA0` is the gated audio tail that the page measures at L926.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
