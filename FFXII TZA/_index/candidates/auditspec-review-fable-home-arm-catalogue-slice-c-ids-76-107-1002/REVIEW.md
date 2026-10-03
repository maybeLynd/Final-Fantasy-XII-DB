# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-arm-catalogue-slice-c-ids-76-107-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ARM-CATALOGUE-SLICE-C-IDS-76-107` · Package: `_index/candidates/fable-home-arm-catalogue-slice-c-ids-76-107-1002/` · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-C-ids-76-107.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 3 functions, 14 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 3 rows, 14 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 3 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `001C2D10`: the constants resolve to 1.65 (`008F9DD0` = 0x3FD33333) and 2.0 (`01CEBC08` = 0x40000000).
- `001C2D50`: `cmp rcx(+8), [r9+0x10]` / `jae` is an unsigned compare; `+8` advances by 0x230 before the null test; the tail-jump at `001C2D99` passes `r9` (the incoming `rcx`), the old `+8` and the incoming `rdx`.
- `001EE5D0`: c and d are `[rsp+0x28]` and `[rsp+0x30]` with no prologue, so they are the 5th and 6th arguments. `comiss xmm3(c/d), xmm2(r8d/r9d)` / `jbe` takes the else arm, unordered included. Both arms halve with `cdq; sub eax, edx; sar eax, 1` (signed, truncating) and then `neg` on a negative result, so the stored value is the absolute value.
- Host: `001C2980` is the page's two-float setter, and `00187950` is the reader of the camera-override fields in the page's answered item.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
