# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-how-a-sound-fades-the-ramp-and-its-six-c-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-A-SOUND-FADES-THE-RAMP-AND-ITS-SI-90911` · Package: `_index/candidates/opus-how-a-sound-fades-the-ramp-and-its-six-c-ee-1003-2/` · Page: `18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md` (commit b0c7c5a57)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors; rejected 0, missing 1.
- Semantic pass: **every row and every callee whose inputs or result the row names** read against raw capstone output of the certified image (SHA256 73461D08...):
  - `007BDBB0` exact: virtual `[[rcx]+0x130]` (`007BDBD6`), `al` != 0 -> `v` = 0, else float `+0xC` of qword `[rcx+0x30]` (`007BDBEE`); `rbx` = `rcx+0xB8` = record `rcx+0x90` + 0x28, four iterations stepping 0x40; a/b/c/d/dword/qword at record `+0/+4/+8/+0xC/+0x14/+0x30` (`rbx-0x28/-0x24/-0x20/-0x1C/-0x14/+8`); `ucomiss d,0` / `jne` sends d == 0 **and** unordered to b (`007BDC1C`, `007BDC92`); `comiss a,b` / `jbe` (`007BDC34`) takes the a > b ordered arm `007AE260(rbx, 1.0 - c/d) * (a - b) + b` and otherwise `007AE260(rbx, c/d) * (b - a) + a`; null qword: `007A9E50(c/d, dword +0x14) * (b - a) + a` (`007BDCAB`); `mulss xmm7, [rsi+0x64]` (`007BDCD8`). 1.0 = `01CEBBA8` (read: 1.0).
  - Callees take what the row says they take: `007AE260` reads `[rcx+8]` and `xmm1` (clamped to [0, 1]); `007A9E50` reads `xmm0` and selects on `edx` <= 5 through a jump table - the six curves of the page title.
- Advisory, not a defect: `rows.json` lists `007A7010` as missing; it is not a row of this package (it was rowed and reviewed in `auditspec-review-opus-audio-bank-and-controller-family-ee-1003`), so nothing is lost.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
