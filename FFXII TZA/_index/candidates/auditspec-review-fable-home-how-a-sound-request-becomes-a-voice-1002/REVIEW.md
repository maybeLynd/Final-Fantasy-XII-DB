# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-a-sound-request-becomes-a-voice-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-A-SOUND-REQUEST-BECOMES-A-VOI` · Package: `_index/candidates/fable-home-how-a-sound-request-becomes-a-voice-1002/` · Page: `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 7 functions, 31 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 7 rows, 31 anchors; mechanically rejected 4, skipped 0, missing 0 (README; FABLE's two corrections are in the staged text).
- Semantic pass: **all 7 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved). Every call offset, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body: `00203D39` call, `00205A1B` call, `00206637` jmp, `001DBAF5` jmp, `001DBCF7` jmp, `001DC275` jmp, `00210A43` jmp. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002033C0`: three qword zeroes, `sub rsi, rdx; je` on a zero length (with `rax = 0`). Then `001DF990(rcx, len)` at +0x41, result to `[rcx]`/`[rcx+8]` and result+len to `[rcx+0x10]`. Then the import `[008C2A40](result, incoming rdx, len)` at +0x64. Then `lea rax, [rsi+rbx]` to `[rcx+8]` and the return. Exact.
- `00207F50` and `002081A0`: `test r8b/dl, 8` and `0x10` are bits 3 and 4. `sub al, 0x28; cmp al, 1; jbe` is 0x28/0x29. `sub al, 0x7B; test al, 0xFD; jne` is 0x7B/0x7D. The end checks are `cmp ...; je` equalities. `inc qword [rcx]` runs on every path where `[rcx] != [rcx+0x10]`. `00207F50`: `cmp [rcx+0x7C], edx; je`, else `[008C2430](r8d)` then `int3`, and both surviving paths tail-jump `00209530`. `002081A0`: `002085B0` zero `al` gives `xor al, al`. Otherwise `movsx` `+0x78` goes to `+0x74`, then `00209530`, then `mov al, 1`. Exact.
- `002109F0`: `cmp [rcx+0x30], r8d; je` / `test edx, edx; js` (signed) / `test r9d, r9d; je` gate `00218DC0([rcx], edx, r8d, r9d)` at +0x22. Both exits store `ebx = r8d` to `+0x30`. Exact.
- `00210A90`: `0021B2F0([rcx+0x10], edx)` at +0x13; on zero `al`, `0021B2F0([rcx+8], edx)` at +0x26; `test r8b, r8b; setne al`. Exact.
- `00211220`: `rcx = [rcx+0x18]`, `movzx r9d, r9b`, `jmp 0021D640` at +0x8. Exact.
- `00218E20`: head `rcx+8`. Empty when `[rcx+8] == rcx+8`. Each node's `[+0x10]` object is tested `edx == -1` first, then `[obj+0x50] == edx`. A hit goes to `jmp 00222B20` (+0x27) with `rcx` = object. The walk follows `[node+0]` back to the head and falls to `ret`. Exact.
- Host: the page reads `00203CB0` (L2344, string-assign arm), `00205890` (SWE2-EC7-52, L1955), `00206430` (L2308, C-escape decoder) as its bodies. `001DBAC0` is the `Audio_SetMode` tail target (L1850). `001DBCE0` is the sound-handle forward of `002DEE80` (L1835). `001DC240` is the stream pan setter (L939 answer). `00210A40` is the `MusicAudioController` forward (L328, L1031). All seven fit.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- Outside this package (not a condition of the verdict): the page's existing `00208CF0` line (L2234) still says *"`byte[rcx + 0x80]` bit 8 (0x28/0x29 exempt) or bit 0x10"*. That is the same mask-as-bit-number wording FABLE corrected in these rows: the tests are bits 3 and 4 (masks 8 and 0x10) of a dword. A separate correction should fix that line.
