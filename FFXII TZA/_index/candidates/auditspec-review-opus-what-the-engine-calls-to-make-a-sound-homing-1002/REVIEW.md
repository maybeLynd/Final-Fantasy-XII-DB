# SWE2-AUDIT-SPEC review: OPUS homing rows (opus-what-the-engine-calls-to-make-a-sound-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-WHAT-THE-ENGINE-CALLS-TO-MAKE-A-SOUND-HOMIN` · Package: `_index/candidates/opus-what-the-engine-calls-to-make-a-sound-homing-1002/` · Page: `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh (verify mode) -> exit 0, `VERIFY 1 functions, 4 anchors / ALREADY / FAILS 0`.
- `rows.json`: 1 row, 4 anchors; rejected 0, missing 0.
- **Entry.** The row states none, and the class file lists no direct callers. The raw census agrees: no branch site reaches the body. Its only reference is the `.data` qword `01EF01A0` = `00347470`, a table entry, which fits "reached by table or pointer dispatch".
- **Host fit.** The body tail-jumps to `003DEC90` and calls `00267E10`, and the page documents both. `002640C0` appears on the page only in the homed row itself. The homing premise holds.
- **Semantic pass, all 1 row (49 B).** Exact.
  - `002640C0` is called with `rcx`/`rdx`/`r8`/`r9` untouched (`rdi = r9` saved first).
  - `00267E10(rdi = incoming r9)`.
  - `0034748D mov ecx, [rbx+0x28]` reads the first result; `edx` = the second result.
  - The epilogue restores `rbx`/`rdi`, then `0034749C jmp 0x3dec90`.
