# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-cut-in-motion-blur-and-soft-focus-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CUT-IN-MOTION-BLUR-AND-SOFT-FOCUS` · Package: `_index/candidates/fable-home-cut-in-motion-blur-and-soft-focus-1002/` · Page: `17-Presentation-Rendering/Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 9 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 2 rows, 9 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 2 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `003B26D0`: the records run `02EBE5E0`..`02EBEBE0` (0x600 / 0x30 = 32). It returns at the first record whose dword `+0` is zero (`003B26EC je` to the epilogue) and calls `003B18E0` only when `test byte [rbx+0x20], 1` is clear.
- `003B3E40`: the dwords run `02EBCC84`..`02EBCD84` with an 8-byte step (32 iterations). The `002DF0F0(d, 0)` call is gated on `byte [d-4] != 0`; the three zero stores run on every iteration.
- Host: `0024E910` is the teardown the page reads. `003B3D20` is Audio-filed, but the page gives it a section of its own (*"SWE2-EC7-46 update - `003B3D20`"*, with its `002DF0F0` call anchored), and no other page treats it as its subject, so homing its callee here is acceptable.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
