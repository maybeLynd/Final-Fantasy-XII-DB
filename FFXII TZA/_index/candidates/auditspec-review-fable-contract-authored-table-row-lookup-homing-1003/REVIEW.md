# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-contract-authored-table-row-lookup-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CONTRACT-AUTHORED-TABLE-ROW-LOOKUP-HOM` · Package: `_index/candidates/fable-contract-authored-table-row-lookup-homing-1003/` · Page: `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md` (commit b35f1958c; reviewed at HEAD 89538d085, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

This is an interior package: it ships `interior_applier.py` and no `homing_applier.py`. Only the sentences were reviewed, with no host-fit check. It has 1 row, fewer than 15, so I read it clause by clause against the full listing. All 5 anchors are correct. The sentence holds as written, including FABLE's correction about the return value.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 1 row, 5 anchors, `mode: homing`; rejected 0, skipped 0, missing 0, corrections 1 (`0019CD40`).
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `0019CD40` correct.
    - Count: `([rcx+8] - [rcx]) / 0x18`, computed with the multiply by `0x2AAAAAAAAAAAAAAB`, `sar 2` and the sign fix-up (`0019CD60`).
    - `cmp r11d, edx` / `jbe` (`0019CD77`): `edx` above the count, unsigned, takes the call. The call is `0020BB10(rcx, [rcx+8], edx - count, r9 = &{0,0,0})`, with the three stack qwords at `[rsp+0x20..0x30]` zeroed (`0019CD98`), and its `rax` is returned.
    - Otherwise: target = `[rcx] + edx*0x18` (`lea rdx,[r9+rcx*8]` at `0019CDB1`, with `rcx = 3*edx`). `(end - target) * 0xD555555555555555` (the negated reciprocal) is a signed element count. `rax` = that count `*0x18` is added to `[rbx+8]` (`0019CDD1`), which moves the end to the target, and `rax` is returned (`0019CDDA`). That last point is the corrected clause, and it holds.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 staged with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match. The one **FABLE corrections** bullet matches `rows.json` `corrections`, and the row's current text is its `now` value.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `0019CD40` belongs to no accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
