# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-how-a-sound-fades-the-ramp-and-its-six-c-ee-1003-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-A-SOUND-FADES-THE-RAMP-AND-ITS-SI-9366A` · Package: `_index/candidates/opus-how-a-sound-fades-the-ramp-and-its-six-c-ee-1003-3/` · Page: `18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. The row was read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...):
  - `007A7010` exact (also read in full for `auditspec-review-opus-audio-bank-and-controller-family-ee-1003`; this row agrees): null `q` -> 0; `cmp al, 2`, `lea ecx, [rax-8]` / `cmp cl, 1` / `jbe` for 8 and 9, `cmp al, 7`; kind 7: `007BC2A0` lock, `EnterCriticalSection` (`008C20B8`), `007BC2B0(&q)`, virtual `+0x10`, `LeaveCriticalSection` (`008C20C0`) on every path, 1 and 3 returned as is, else 2, null/0 -> 0; kinds 2/8/9: `007B44B0`/`007B44C0`, `007B7950`/`007B77E0`, `007B8050`/`007B7FD0`, virtual `+0xA8` (`007A71A8`), 4 -> 3 through `sete` (`007A71C9`); other kinds 0.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
