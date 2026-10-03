# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-vp8-codec-interface-and-its-control--ee-1003-4)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VP8-CODEC-INTERFACE-AND-ITS-CONTR-EEA2E` · Package: `_index/candidates/opus-the-vp8-codec-interface-and-its-control--ee-1003-4/` · Page: `23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md` (commit b0c7c5a57)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply`, from the package folder -> `VERIFY 8 functions, 40 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 8 rows, 40 anchors; rejected 0, skipped 0, missing 5 (`001260E7`, `001263AD`, `00126E10`, `00127104`, `0017B010`, not rowed). All 8 sentences and anchor lists are present verbatim on the page at HEAD.
- Semantic pass: **every row** read clause by clause against a full linear capstone decode of the certified image (SHA256 73461D08...); all 8 bodies decode exactly over their function-list extents. Stack arguments located from each prologue (pushes + frame): argument 5/6 at `[rsp+0x290/0x298]` (`00172CE0`, `00172F00`, `00173040`), `[rsp+0x510/0x518]` (`00172DC0`), `[rsp+0x2C0/0x2C8]` (`00173180`), `[rsp+0x180/0x188]` (`00173270`, `00173360`), `[rsp+0xB0/0xB8]` (`00173450`). The cookie is qword `01F44830` (.data) `xor rsp`, checked by `call 00808C40` in all 8.
  - `00172CE0` exact, branch-free: `00148420(r11 - movsxd(2*edx), rsp+0x40, edx, 1, [rsp+0x20]=9, [0x28]=8, [0x30]=03001AD0 + 0x60*movsxd(r8d))` then `001484DB(rsp+0x50, arg5, arg6, 8, 4, 4, 4, 03001AD0 + 0x60*movsxd(r9d))`.
  - `00172DC0` exact: `test r8d` -> 0 path `0012608C(.., rsp+0x40, edx, 0x15, 0x20)` then the shared `00125BD1(rsp+0x80, arg5, arg6, 0x20, 0x10, 0x10, arg6, y)`; both non-zero `0012595A(.., 1, 0x15, 0x20, x)` then the same `00125BD1`; `r8d` != 0 with `r9d` = 0 only `00125E07(rcx, edx, arg5, arg6, 0x10, x)` and jumps past `00125BD1`.
  - `00172F00` / `00173040` exact: both non-zero `00125850(.., 1, 0xD|9, 0x10, x)` then `00125B02(rsp+0x60, arg5, arg6, 0x10, 8, 8|4, arg6, y)`; only `r8d` `00125D01(rcx, edx, arg5, arg6, 8|4, x)`; `r8d` = 0 `00125FA7(rcx - 2*edx, edx, arg5, arg6, 8|4, y)` with no `r9d` test on that path.
  - `00173180` / `00173270` / `00173360` exact: four arms on `r8d`/`r9d` (`test r8d` then `test ebx` on both sides); the first callee pairs `001266C9`/`0012696A` (0x10, 0x15), `00126550`/`00126B8B` (8, 0xD, second 8) and (8, 9, second 4); the both-zero arm calls `001488D0`, `001481D0`, `0014824F` with `r8` = arg5 and `r9d` = arg6 set before the `r9d` test. The sixth argument (`[rsp+0x28]`) is `r8d` for the first callee and `ebx` = `r9d` for the second, as stated.
  - `00173450` exact: `movsxd r11, edx` and `movsxd rsi, [rsp+0xB8]` (sign-extended, as stated); arms `001267FA`/`00126CF9` with (4, 9) and (4, 4); both-zero arm is the inline 4x4 byte copy from `rcx` (row step `r11`) to arg5 (row step `rsi`), 16 `movzx`/`mov` pairs ending `001735A8`.
  - Anchors: all 40 are instruction boundaries strictly inside their bodies and decode to the recorded mnemonics.
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
