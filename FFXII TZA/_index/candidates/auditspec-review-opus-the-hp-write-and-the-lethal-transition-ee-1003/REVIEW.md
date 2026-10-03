# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-hp-write-and-the-lethal-transition-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-HP-WRITE-AND-THE-LETHAL-TRANSITIO-D38C9` · Package: `_index/candidates/opus-the-hp-write-and-the-lethal-transition-ee-1003/` · Page: `08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md` (commit b0c7c5a57)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row and every callee whose inputs or result the row names** read against raw capstone output of the certified image (SHA256 73461D08...):
  - `00345C20` exact: six `00267DB0(r9)` calls (`rbx` = `r9` reloaded into `rcx` before each); stores to stack `+0x28/+0x24/+0x20` then `+0x38/+0x34/+0x30`; `+0x2C` and `+0x3C` are never written (the cookie sits at `+0x40`); `003A1920(rcx=&A=+0x30, rdx=&B=+0x20)` (`00345C9D`), `movaps xmm1, xmm0`, `0026B4C0(rcx = incoming rcx)` (`00345CA8`); cookie `01F44830` / `00808C40`.
  - Callees: `003A1920` reads three floats of each block and returns a float in `xmm0` (squared distance, tail-jump `00861F14`); `0026B4C0` reads `rcx` and stores `xmm1`; `00808C40` does not touch `rax`, so "returns with `rax` as that call left it" holds; `00267DB0` reads `[rcx]`.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
