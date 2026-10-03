# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-gambit-evaluation-and-enmity-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-GAMBIT-EVALUATION-AND-ENMITY-1002` · Package: `_index/candidates/fable-home-gambit-evaluation-and-enmity-1002/` · Page: `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 4 functions, 16 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 4 rows, 16 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 4 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- All four texts are exact. `003A7950`: `[t+8+k*8]` is null-tested; `00333C00` and then `003697F0` run on it; `t` is re-read for the zero store and again for `dec dword [t]`; the return is `rcx+2`. `003A7A50`: 0x10+0x10+8+4 = 0x2C bytes from `rcx+4` into `003A78A0(byte rcx+1)`, then `00333C80(buf, 0)`, returning `rcx+0xA4`. `003A7AA0`: returns `rcx+3`. `003A92B0`: returns `rcx+2`.
- Sites: `003ED8A0 + 0x135/0x142/0x1C7/0x1D1` are the `003ED9D5`/`003ED9E2`/`003EDA67`/`003EDA71` arms of `003ED8A0`'s opcode switch (`sub r8d, 0xC0` ...).
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **All four rows (`003A7950`, `003A7A50`, `003A7AA0`, `003A92B0`, entered from `003ED8A0`): host-fit defect.** The page cites `003ED8A0` once, in its Presentation boundary line, and only as a caller of `003829D0` (*"`003829D0` ... is called by `CameraSystem_SelectAndPublishActiveView` `00259820` and `003ED8A0`"*). Other pages read `003ED8A0` as the effect-file data parse. Its opcode arms (`sub r8d, 0xC0` ...) reach these bodies. `003A7950` and `003A7AA0` index the `02EBEFA8` slot table; `003A7A50` fills a buffer from `003A78A0` and passes it to `00333C80`; `003A92B0` forwards to `003A9160`. None of that is gambit evaluation or enmity, and the section heading (*"called from this page's functions"*) is false for every row.
  - **Repair:** withdraw this package (and the section already on the page: the applier prints `ALREADY`), and re-home the four rows unchanged on `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`, which reads `003ED8A0` as the EFX data parse (five citations).
