# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-an-animation-makes-a-sound-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-AN-ANIMATION-MAKES-A-SOUND-10` · Package: `_index/candidates/fable-home-how-an-animation-makes-a-sound-1002/` · Page: `18-Audio/how-an-animation-makes-a-sound.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 5 functions, 23 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 5 rows, 23 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 5 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `00360670`: `jle` (signed pointer compare) loop over `022CB9DC`, `022CB9E0`, `022CB9E4`: three dwords, inclusive.
- `0036EC50`: the `ecx == -1` arm reads `[1]` and `[2]` off `edx = 0`, as stated. The image-base form `lea rax,[rip-..]` = `00120000` gives the tables `+0x21B9AE0` = `022D9AE0` (`cl & 0xF0` non-zero) and `+0x21B9AB0` = `022D9AB0`; stride `rcx*3*8` = 0x18; `cmove` adds 2 only when byte `+2` is non-zero.
- `003A0E80`: `ecx == 0` goes to `003A0E99 jmp 002DF690` with `ecx = edx`; `ecx == 1` goes to `003A0E91 jmp 002DF0F0` with `(edx, 0)`; anything else returns.
- `003A10F0`: `shr 30; not; and 1` is bit 30 inverted. `003E7CD0`: 32 entries of 0x150 from `02B59D80`, returning `[entry+0xC0+edx*4]` (`mov eax, edx` zero-extends).
- Host: `002E9D90` (the sample lookup, section 4) and `0046CC70` (the play routine, section 5) are the page's own subjects.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
