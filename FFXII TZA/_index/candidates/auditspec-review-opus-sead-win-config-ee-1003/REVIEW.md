# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-sead-win-config-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SEAD-WIN-CONFIG-EE-1003` · Package: `_index/candidates/opus-sead-win-config-ee-1003/` · Page: `18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh, verify only (no `--apply`): exit 0, `VERIFY 47 functions, 235 anchors` / `ALREADY` / `FAILS 0`.
- `rows.json`: 47 rows, 235 anchors. README reports 0 rejected and 0 missing.
- Semantic pass: **16 of 47 rows** read clause by clause against the resolved disassembly of the certified image (SHA256 `73461D08...21F8`, rip targets resolved by `disr.py`). The sample covers every function named in OPUS's correction list except the remaining family siblings, plus the longest conditional bodies. Import slots were resolved from the IAT (`008C20B8/C0` Enter/LeaveCriticalSection, `008C2120` OutputDebugStringA, `008C22F0` InitializeSRWLock). The log strings (`01CB4568`, `01CB4B10`, `01CB4B58`, `01CB4C98`, `01CB4CD8`) and the constants (`00900320` = four 1.0f; tags `bus `/`ctgl`) were read from the image.
  - `00220DE0` (corrected): early exit on byte `+0x90` / zero `edx`; `rsp+0x50` is the `rcx` home slot (two pushes + `sub 0x38`), read once before the loop writes it; step 0xA; `sete` of the re-read byte. Exact.
  - `00220E80` (sibling): same form, `00221390`, step 0x30. Exact.
  - `007ADBB0` (sibling): `ctgl` = `63 74 67 6C`; unsigned `jb` entry loop; vtable `01CB4280`; `[rdx+8]` = 0 on miss. Exact. `007AD9A0` (`bus `, `01CB47F0`) also exact.
  - `007AA110` (corrected): `jb` 2 / `jae` 1 / 0 select; `+0x78` = r9d+1, `+0x7C` = 2; `ecx` = r15+9 = 8; element writes at `+0`/`+8`/`+0x10`/`+0x1C`/`+0x20`/`+0x24` only (dword +0x18 and qword +0x28 are not written, as OPUS corrected); second pass `-0x28..-0xC` relative to the advanced `rdx` = `+8/+0xC/+0x14/+0x1C/+0x20/+0x24`; signed `jle` on word `[h+4]`. Exact.
  - `007B4A70` (both corrections): `cmovns rbx, rdi` advances only on non-negative `007B2880`, and the failure path re-enters at `007B4CF9` with `rbx` unchanged; `007B2F70` arguments are r9 = `rsp+0x40` (the copy of `[s+0x10]`), stack +0x20/+0x28/+0x30 = `o+0x38`/`o+0x40`/slot `+0x118`; the list store is gated by signed `jle` against dword `02EAD548` and by bit 1 of element `+0x1C`. Exact.
  - `007B1AB0`: overlap test is unsigned (`jae` / `ja`); the fifth argument is `[rsp+0x1F0]` (5 pushes + `0x1A0` frame); least-`+0xC` slot choice uses a signed strict `jge` skip, so the first minimum wins; request fields `+0x30..+0x5C` are as listed. Exact.
  - `007B2CB0`: fifth/sixth arguments at `[rsp+0x1C0]`/`[rsp+0x1C8]` (6 pushes + `0x168`); `007B2F70` gets r8 = copy of `[rcx]`, r9 = copy of `[rdx]`. Failure zeroes `[rcx]`. `007E2880` is called only on a zero `al` from slot `+0x130`. Exact.
  - `007AF380`: pops from free head `+0x18` and links at head `+0x20`; the empty case also sets tail `+0x28`; `or [n+0x1C],1`, `inc [rcx+0xC]`, optional `[rdx]` store. Exact.
  - `007BE0B0`: `007CA560(rcx+0x108, 1.0, xmm1, 0, 0)`; both evaluations equal `v`; the negative branch `-(v/|+0x3F0|)`; the raise is taken on `comiss xmm7, xmm2` / `jae` skip (stores when `v` < candidate); the re-evaluation passes `edx` = 0 (the field was just zeroed); `cmovs` clamp of `+0x50`. Exact.
  - `007CA650`, `007E9E60` (corrected): `rdx` = `rsp+0x50` holding `[s+0x10]`; fifth = qword 0, sixth = slot `+0x118` result; `js` early return of `007E8890`. Exact.
  - `007D85E0` (corrected): six records as listed (first `+0xC` = `0xC0C00000`); `007AD460(0x10, 0x20, 2)`; ramp → `mulss 0.115129` → `expf` (`00861FAA`) for `+0x18/+0x78/+0xA8` only. Exact.
  - `007D9530` (corrected): `007AED00` called at `007D9584` and `007D95A4`; `1/r`, `r*0.5`, `h*k0`, `-log10f(h/k)`. Exact.
  - `007DAAB0` (corrected): the 8-iteration loop zeroes dwords `+0x54..+0x73` and 0x100 bytes `+0x74..+0x173`; four constants; `+0x4C` = `1/r * +0x48 * 2pi`. Exact.
  - `007DDED0` (corrected): descriptor layout `rsp+0x20..+0x44`; second block via `007DD2B0`, whose return goes to `02EAE0C0`; each negative `007DE8D0` calls slot `+0` with `edx` = 1, zeroes its global and returns -1. Exact.
- Non-blocking note: in `007B4A70`, the closing clause ("moves to qword node `+0x10` only while bit `0x1` ... is set") applies to the non-state-3 paths. The state-3 path advances on the `cmovns` regardless of that bit, which the row's own parenthetical already states. No change required.
- Limits hold: body statements only, static evidence. A cloud/local draft plus OPUS's re-read is not independent review; this record is. 31 rows were not read by this reviewer.
