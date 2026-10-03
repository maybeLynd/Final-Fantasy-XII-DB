# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-the-vif1-vu1-layer-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-VIF1-VU1-LAYER-HOMING-1003` · Package: `_index/candidates/fable-the-vif1-vu1-layer-homing-1003/` · Page: `17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md` (commit `c29c5b85e`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the certified image (SHA256 73461D08...); every relative call (`fn`+0xNN) resolved to its target:
  - `001EC000` exact: offsets are `rcx`-relative throughout (`[rdx+8]` = `rcx+0x28`, `[rdx+0x10]` = `rcx+0x30`, `[rdx+0x14]`/`[rdx+0x18]` = `rcx+0x34`/`+0x38`); signed `jge`; `comiss 0, [+0x34]` / `jbe` stores 0 only for a negative value; dword -1 to `+0x30`; qword 0 to `+0x20`; every path ends `jmp 001EB800` except the null early `ret`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
