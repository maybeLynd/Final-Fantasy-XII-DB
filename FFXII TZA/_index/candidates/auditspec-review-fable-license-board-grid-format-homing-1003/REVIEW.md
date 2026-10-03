# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-license-board-grid-format-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-LICENSE-BOARD-GRID-FORMAT-HOMING-1003` · Package: `_index/candidates/fable-license-board-grid-format-homing-1003/` · Page: `12-Items-Equipment-Shops-License/license-board-grid-format.md` (commit b7c6eb07d)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...), call offsets resolved:
  - `003FCAD0` exact, clause by clause: the reset loop (word 7, bit 0 cleared, byte `+0x3F` -> `+0x39`, signed `jg`/`jle`); the `0xFFFF` return; i 0..8 with `00282DF0` at `+0x82` and `00282FA0` at `+0x8D`; the entry index `min(r8d+i, r9d)` (`cmovle`, `r15` advanced every iteration); `0035D330(1, w << 16)` at `+0xBD` and `f` = low byte of `00282F10(w, s)` at `+0xCD`; kinds 8/9 store word 8 and byte `+0x47`; kind 6 with `f` non-zero tests `003FC900` on the two selectors (`+0x153`, `+0x15F`) and stores word 9 / byte `+0x4F` or word 8 / byte `+0x47`; the 5-word search at `s+0x9A` (stride 4); `j` = `002C9B30(movsx word s+0x60, 5)` + 1 at `+0xFE` stored as word `+0xA` with byte `+7` of entry `j`.
- Limits hold: body statements only, static evidence; the draft and FABLE's re-read are not independent review, this record is.
