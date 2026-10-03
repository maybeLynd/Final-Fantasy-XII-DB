# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-lua-loader-and-what-it-accepts-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-LUA-LOADER-AND-WHAT-IT-ACCEPTS-CL-40D13` · Package: `_index/candidates/opus-the-lua-loader-and-what-it-accepts-cloudint-1003/` · Page: `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md` (commit 890844135)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `005928F0` exact: `c` = byte `r8+0xc`, `a` = dword `[[r9+8]+8]` (`r11d`), `b` = dword `[[r9+0x10]+0x48]` (`r9d`); source `rcx += c ? a : b` (`eax`=`b`, `00592920 cmovne eax, r11d`), destination `rdx += c ? b : a` (`0059292A cmovne r11d, r9d` after a second `test r10b`); count dword `[r8]`, zero skips (`test r8d; je`); loop `movsx eax, byte [rcx]` / `mov word [rdx], ax` (`00592940`/`00592946`), steps dword `r8+4` (`ebx`) and `r8+8` (`edi`), `sub r8,1; jne` (`00592950`).
  - `00595C00` exact: the same prologue and selection (`00595C30`/`00595C3A` `cmovne`), loop `movzx eax, byte [rcx]` / `mov byte [rdx], al` (`00595C50`/`00595C56`), same steps, `jne` at `00595C5F`.
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
