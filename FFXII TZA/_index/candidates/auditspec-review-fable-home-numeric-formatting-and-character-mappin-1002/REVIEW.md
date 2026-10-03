# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-numeric-formatting-and-character-mappin-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-NUMERIC-FORMATTING-AND-CHARACTER` · Package: `_index/candidates/fable-home-numeric-formatting-and-character-mappin-1002/` · Page: `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 8 functions, 32 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 8 rows, 32 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 8 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002476E0`: `test al, al; jns` (bit 7 of `+0x40`), then `bt eax, 8; jb` (bit 8 clear); four byte adds from `rdx+0/2/4/6`.
- `002A4030`: each null test substitutes `r8 = 0` and does not return: a null `rcx` reads `[0+0x18]`, a null `a` adds at `[0x10]`/`[0x9C]`, and a null `b` adds at `[0x10]`/`[0xC]`/`[0x9C]`. That is exactly the stated low-address behaviour.
- `002A5520`: `cmovs` from `01E0C1DC` (currently 0x1C0); `cvttss2si` of `0017F880`'s float, times 5 via `lea eax,[rcx+rcx*4]`; 38.0 at `00902708` = 0x42180000.
- `00574770` (390 B) read in full: `s` is the 8-byte home slot at `rsp+0x30`; the 0x8000/0xFFFF/0xFF sentinels select the `s` fallbacks; the sum `word +0x114 + byte s+7` goes to `+0xE0`'s `+0x9C` and to `+0xC0`'s `+0x9C`; the `+0x8060 == 5` arm uses `dx`/`dy` that are 0 for a sentinel word.
- `0028F750`, `004052A0`, `004052B0` and `005766B0`: exact.
- Host: `002A70B0`, `003EC810`/`003EC830`, `005742D0` (decoded jump table) and `00573BE0` are all read on the page.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
