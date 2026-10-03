# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-the-shop-table-and-its-stock-gates-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-SHOP-TABLE-AND-ITS-STOCK-GATES-HOM` · Package: `_index/candidates/fable-the-shop-table-and-its-stock-gates-homing-1003/` · Page: `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md` (commit `c29c5b85e`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the certified image (SHA256 73461D08...); every relative call (`fn`+0xNN) resolved to its target:
  - `0027F030` exact on every path: `r9d` == 0 arm (`[rsp+0x60]` != 1, `002CCA10(r8d)`, `002CA430(edx)`, `002CCA40(v, word [0209AC30]+0xD68)` == 0 -> 4 via `lea edi, [rbp+4]` with `rbp` = 0); `r9d` == 1 arm (`002CCA00(r8d)`; b = byte `+0xD6B`; `002CCA00(b)` -> `cmove` keeps 0 when `r8d` == b else 4; `002CCA30(b)` non-zero -> 4; `t` = `002CA430(word +0xD48)`, `002CCA00(t)` zero or `t` != `r8d` -> 4); `00317B70(movzx cl, movzx dx, r9d, fifth)` zero ORs 1.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
