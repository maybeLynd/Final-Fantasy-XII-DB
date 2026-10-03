# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-music-control-file-and-the-bgm-strea-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-MUSIC-CONTROL-FILE-AND-THE-BGM-ST-61D71` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-the-music-control-file-and-the-bgm-strea-cloudint-1003/` · Page: `18-Audio/the-music-control-file-and-the-bgm-stream.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 9 functions, 34 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 9 rows, 34 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- **Package choice.** `tasks_C2.tsv` names the `-ee-1003` package for this task, but the board question (`9 cloud-drafted, OPUS-verified interior citations ... at e63502b10`) matches this `-cloudint-1003` package (`session: opus-self`, 9 rows). The `-ee-1003` package has 3 rows and already has its own review (`auditspec-review-opus-the-music-control-file-and-the-bgm-strea-ee-1003/`). This record reviews the package the board asks about.
- Semantic pass: **all 9 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 9, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `00220D40`: the three calls in order (`005CD4F0`/`005CD820` on `rcx+0x350`, `00220600` on `rcx+0x1d0`); `rbx` keeps the `00220600` result across `005CD820` and is returned.
  - `0032E780`: `test edx, edx; jns` (signed). On the call path `[rsp+0x60]` after `sub rsp, 0x38` is the entry's `[rsp+0x28]`, the fifth argument, re-stored at `[rsp+0x20]`; dword `[rsp+0x28]` = 0 is the sixth.
  - `003EB010`: the `je` on qword `02B5E0E8` == 0 returns at once; `003EAD10` gets the address `02B5E0E0` (`lea`) and `003697F0` the qword value at `02B5E0E8`; then the qword and dword `02B5E0F0` are zeroed.
  - `003EB0A0` / `003EB150`: polarity checked (`je` on byte `02B5E111` == 0; `cmove ecx, edx` replaces the byte by 6 only when it is 5; the byte is stored back on both arms).
  - `002255B0`, `00225CC0`, `00354690`, `003557C0`: exact (operand widths, argument registers, tail jumps).
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
