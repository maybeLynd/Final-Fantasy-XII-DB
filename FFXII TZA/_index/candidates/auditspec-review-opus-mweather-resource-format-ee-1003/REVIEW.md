# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-mweather-resource-format-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MWEATHER-RESOURCE-FORMAT-EE-1003-E2321` · Package: `_index/candidates/opus-mweather-resource-format-ee-1003/` · Page: `03-World-Area-Field/Weather/mweather-resource-format.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 2 functions, 10 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 2 row(s), 10 anchors; rejected 0, missing 0; the README's count sentence matches.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `0046D160` exact: `xmm1 / 6.28319` (`01CEBC78`), `s` = table `01F004E0`[trunc(u*32768) & 0x7FFF], `k` = table[(0x2000 - trunc(u*-32768)) & 0x7FFF]; identity copy `00202C70(m, 01F204E0)`; `k` to `+0x14`/`+0x28`, `s` to `+0x18`, `s` XOR `01CEBDA0` to `+0x24`.
  - `0046D200` exact: the same table reads; `k` to `+0`/`+0x28`, -`s` to `+8`, `s` to `+0x20`.
- Advisory, not a defect: the README title says "cloud-drafted" while the drafting session it names is a local agent.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
