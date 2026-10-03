# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-element-types-00-0a-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-ELEMENT-TYPES-00-0A-1002` · Package: `_index/candidates/fable-home-the-element-types-00-0a-1002/` · Page: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 3 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 3 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image. The entered_from site was disassembled and confirmed as a direct call to the body. Host fit was checked against every citation of the caller on the page outside the homed section. The body's address had no page citation at the package's commit parent.
- `00180100` (32 B): `call 001D50D0` (`+0x4`, the lazily created singleton `[01F81428]`) / `mov rcx, rax` / `call 001CD0D0` (`+0xC`, which returns dword `rcx+0xAC0`) / `cmp eax, 2; setne cl` / return `ecx`. "Returns 1 when that second call's `eax` is not 2, else 0" is exact.
- Site: `004355D0` + 0x38 = `00435608 call 0x180100`, confirmed (after `0024E410` returns non-zero).
- Host: the page's type table (L378) names `004355D0` as the type-`0x05` primitive, "model composer `004355D0` - a resource mesh". The caller is the renderer of one of this page's own element types, not a boundary mention, so the body fits.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
