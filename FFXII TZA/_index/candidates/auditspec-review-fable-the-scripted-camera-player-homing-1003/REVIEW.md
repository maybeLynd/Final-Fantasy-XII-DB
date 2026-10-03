# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-the-scripted-camera-player-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-SCRIPTED-CAMERA-PLAYER-HOMING-1003` · Package: `_index/candidates/fable-the-scripted-camera-player-homing-1003/` · Page: `17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md` (commit `c29c5b85e`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 5 functions, 24 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 5 row(s), 24 anchors. **Every row** read clause by clause against raw capstone output of the certified image (SHA256 73461D08...); every relative call (`fn`+0xNN) resolved to its target:
  - `002565C0` exact: `jp`/`jne` pairs make unordered unequal; `atan2f` (`00861F02`) of the two differences; constants read from the image: `00915610` = 0.3926991, `01CEBC78` = 6.283185, `00915624` = -6.283185, `00915614` = 0.7853982; the `comiss`/`jbe` polarities give 'below 0' and 'above 6.283185' as stated; `cvttss2si` of the quotient.
  - `0027B3B0` exact: buffers at `rsp+0x30` (A), `rsp+0x20` (B), `rsp+0x40` (C) zeroed through `r11`; `002E9D10(ecx, A)`, `002E9D10(edx, B)`, `00203080(C, A, B)`, `002703F0(C)`; cookie `01F44830` / `00808C40`.
  - `00373380` exact: every guard, the `0020E600` / `0x290`-stride walks over `+0x84`/`+0x88`/`+0x8A`, `0020E620(0)` to `+0x278` and word -1 to `+0x27C`; the unconditional -1 to dword `rcx+8` and word `rcx+0x14`; `0046D110(Q+0x1F0)`; `and 0xfffd` on `+0x280`; `00409270(T, movsx [+0x27E])`, the `0xfff000` all-set test giving -1, else `>> 0xc & 0xfff` to `+0x270`; word -1 to `+0x276`.
  - `0042D9C0` exact: `00421D70(rcx, word [rdx+0x1C])`; `cmp cx, ax` against 0xffff; three stores; `rax` untouched afterwards.
  - `0050D540` exact: `00377DB0` with registers untouched; non-zero -> 0; else `00314D40(1)` and 1.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
