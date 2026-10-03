# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-the-screen-fade-layers-and-the-movie-fad-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-SCREEN-FADE-LAYERS-AND-THE-MOVIE-F` · Package: `_index/candidates/fable-the-screen-fade-layers-and-the-movie-fad-homing-1003/` · Page: `17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md` (commit `c29c5b85e`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 12 functions, 54 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 12 row(s), 54 anchors. **Every row** read clause by clause against raw capstone output of the certified image (SHA256 73461D08...); every relative call (`fn`+0xNN) resolved to its target:
  - `0024E070` exact: `and 0xfff9` on word `020926E4`; the `0209216A` < 0x100 (`jb`) append to `02091950[n*8]` and increment, else `00182CA0(it)`; `020926D8` zeroed on both paths; `00375470([020926E0])` and zero.
  - `00345600` exact: `jns` on `00267E10(r9)` to `jmp 00360E50`; else `002DEC00()`, `jns` to the same tail, else `jmp 00360D70`.
  - `00346A60` exact: `00264180` with registers untouched, `cmovne` 1; `00264830()` non-zero stores dword 1 to `[r8]`; returns the kept value.
  - `0034AF80` exact: `0035A0C0(00263750(second), first)`, `jmp 0026B4E0(rcx, result)`.
  - `0034D3A0` exact: `00360980(00267E10(r9), byte [rdx+0x15], word [rdx])`, `jmp 00183070`.
  - `003527D0` exact: `003C5DE0(0)`, `jmp 003C58B0`.
  - `0036E640` / `0036E6B0` exact: `0024DE70` result - 2 compared unsigned against 1 (so 2 or 3); `0024E210(ecx, 0)` resp. `(ecx, 3)`; `sete`.
  - `0036E8B0` exact: signed clamp 0..0x1F (`jns` / `cmovg`); `r` = `022D94B0` + index*24; the two 2-or-3 tests; word 3 to `r+4`; `003B1BA0(003B7720(), 003B7750(), 003B7760(), [r], edx as the fifth)` - the reverse order holds; `0024F8D0([r], cmove 3/0)` when `[r]` is non-zero; 1.
  - `0037C3C0` exact: indices 0..3, `00263750(i)`, non-null -> `002E6BB0(it, 1)`.
  - `003DDC50` exact: signed clamp 0..3; `0024CFF0` on a non-zero dword at `02B58A80 + i*0x68`, zeroed; `memset` (`00861EC0`) of 0x58 at `02B58A90 + i*0x68`; dword 0x13602, byte `+0x1C` `and 0xe3` / `or 3`, qword 0 `+0x20`, 1.0 `+0x28`, qword 0x3f800000 `+0x2C`, 0.5 `+0x34`, 0x80ffffff `+0x38`.
  - `00473E60` exact: `00183070` with registers untouched, then `jmp 00182F10` with the saved `ecx`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
