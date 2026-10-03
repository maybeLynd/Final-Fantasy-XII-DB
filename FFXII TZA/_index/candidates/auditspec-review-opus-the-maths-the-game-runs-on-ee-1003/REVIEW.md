# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-maths-the-game-runs-on-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-MATHS-THE-GAME-RUNS-ON-EE-1003-9F45E` · Package: `_index/candidates/opus-the-maths-the-game-runs-on-ee-1003/` · Page: `24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 2 functions, 10 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 2 row(s), 10 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `0085EA40` exact: F = `0085E740(rcx, edx, q, x)`; the `[t+4i]` == 3 early return (the epilogue's `mov eax, edi` returns i on every path); `00861D30(&v, p)`; the three cross-product components; Q(a) with constants read from the image (`00D22C30` 0.025, `008C5F68` 0.01745329 = pi/180, `00902EF0` 45, `00902438` 360, `00D11670` 40, `009146E4` 5); `sinf`/`cosf` thunks; e = -1; the D tests, the b loop from a - 40 while b <= a, e = k, e = j; the reset to 0 and repeat; D stores 3.
  - `008800C0` exact: the stack reader layout (the dword at +0x18 over a zeroed qword leaves +0x1C = 0); `0017CB40(&b, 8)`; `00880C10(&b, &s, 6)`; 'vorbis' read from `01CEBB50`; all three packet types with their error codes, including 0xFFFFFF7F + 7 = 0xFFFFFF86 on type 1.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
