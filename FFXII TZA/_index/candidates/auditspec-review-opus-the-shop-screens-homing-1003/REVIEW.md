# SWE2-AUDIT-SPEC review: OPUS homed bodies (opus-the-shop-screens-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SHOP-SCREENS-HOMING-1003` · Package: `_index/candidates/opus-the-shop-screens-homing-1003/` · Page: `16-UI/Shop-Screens/the-shop-screens.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh, verify mode (no `--apply`) -> `VERIFY 17 functions, 77 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 17 rows (mode `homing`), 77 anchors; rejected 0, skipped 0, missing 0.
- Homing property: every one of the 17 functions is listed in `fable-homing-stream-1003/callee-host-bodies.tsv` with this page among its hosts, is not cited anywhere on the page above the homed section, and its sentence names at least one callee that the page cites above that section (e.g. `00314D40` for the eight small wrappers, `0057FB00` for `0057F8C0`, `002432B0`/`005C5230` for the two dispatchers).
- Semantic pass: **all 17 rows** read clause by clause against `disr.py` output of the certified image. All exact. Points checked specifically:
  - `002947F0`: "fifth (stack) argument" is `dword [rsp+0x50]` after `push rdi` + `sub rsp,0x20` = entry `[rsp+0x28]`; `0017D2E0(r9, rcx, result)` (rcx = saved r9, rdx = saved rcx); `cmp eax,0x200 / jb` skips, so `0x200` or more unsigned calls `0016D6A0(0x20000)`; returns 1 on both paths.
  - `002CCA40` (OPUS correction): the loop bound is `ebp` = `00252FA0(4)` (`002CCA5A`, `cmp ebx,ebp` at `002CCAD3`); `test/jg` is signed; `0xffff` ids skip; `+0x38` compared with incoming `ecx` (r15d), id with incoming `edx` (r14d), `+0x20` with `jg` (signed). Correction confirmed.
  - The eight `00314D40(1)` wrappers (`00342F50` .. `00357300`): each branch polarity read (`jne`/`je` after `test eax,eax`; `lea ecx,[rax+1]` = 1 on the zero path); `00357300` `dec eax; cmp eax,2; ja` = result not 1..3, unsigned, as stated.
  - `003C95C0`: case chain 1/2/3/0xe/0xf from the `sub` ladder, default tail-jumps `005C5230(rcx)`; case 2 table loads (`+0xc1` from image base + `0xbf1720`, `+0xc2` from `+0xbf1728`, indexed by the old `+0xc1`), `neg/sbb/and 7` gives +7 for `+0xc3` = 1 (new `+0xc1` = 3) and +0 for 4; case 3 divisions: `0x55555556` = /3, `0x66666667` with `sar 2` = /10 and with `sar 1` = /5, signed with the sign-bit add, low bytes stored as words; default `0x80, 0x80`.
  - `003FCFE0` / `003FDDE0`: E = `[rcx+0xe0]` + `movsxd(r9d)`*0x20; the bit `0x1` clear in `003FCFE0` is on `[[rdx+0x10]]` (`003FD0E9`) but in `003FDDE0` on `D` (`003FDEF0`), and both sentences say so; the else-path early store of `s` at `D+0x24` (`003FD088`/`003FDE8D`) is overwritten by the `002DD7E0(2 or 0)` store and is not claimed; `0029FF60` stack args are dword `[rsp+0x20]` = 0 and qword `[rsp+0x28]` = 0; `003FCAD0(rdx, E, 5, 0xa)` from `lea r8d,[r9-5]`.
  - `003FD1D0` (OPUS correction): `003FD27D` loads `rax` = qword `+0x18` of qword `+0x20` of `[rcx+0x60]`, stores it at `+0xc0`, and `003FD28F` stores `003FCFE0` at `[rax+0x120]`, the object that qword points to. Correction confirmed. Case 0x12 (`cmp ecx,6` after `-1-0xb`) returns 0; case 0xc null checks on `rcx`, `[rcx+0x10]` and the pointer.
  - `003FF1F0`: `neg r14d / sbb / and 5` = 5 only when replaced; the `002DD7E0(4)` overwrite keys on `k` = `0xff`, whichever path set it; R = `0035D330(1, w << 0x10)` (ecx = r14d = 1).
  - `0053EEA0`: cases 1/2/0x10 (`cmp r8d,0xe` after two `sub 1`), loop `00365570(7..0xc)` from `ebx` 0..5.
  - `0057F8C0`: `cmovne edx,ebx` gives 0 only when byte `+0xea` is 0 and record dword `+4` is non-zero; `cmovb` after `cmp r14d,0xc7` is an unsigned cap; `00393160` args `(rdx,4,3,9,m)` and `(rdx,1,3,9,m)` from the `lea` forms.
- Limits hold: body statements only, static evidence; a local draft plus OPUS's re-read is not independent review, this record is.
