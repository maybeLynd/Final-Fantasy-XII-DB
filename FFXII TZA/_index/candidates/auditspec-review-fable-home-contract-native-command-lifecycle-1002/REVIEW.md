# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-native-command-lifecycle-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-NATIVE-COMMAND-LIFECYCLE` · Package: `_index/candidates/fable-home-contract-native-command-lifecycle-1002/` · Page: `01-Script-VM-Native-Bridge/CONTRACT-native-command-lifecycle.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `0032A7A0`: `cmp ecx, 5; ja` to return 0. Then `cmp cl, 0x27; jbe` chooses between `[02EBF190] + 8 + cl*0x1C8` and a null base. Then the `+0x1C3`/`+0x1C4` `0xFF` tests: 1 if either differs, 0 if both are `0xFF`.
- Host: `00342560` is the family-0 past-the-end slot that the page reads (L5/N-4).
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`0032A7A0`: the parenthetical describes an unreachable arm as behaviour.** The `cl > 0x27` null-base arm (`0032A7AA xor eax, eax`) can only be reached when `ecx` is above 0x27. The preceding `cmp ecx, 5` / `ja 0032A7DE` has already returned 0 for every such value, so on every path that forms a record, the record is `[02EBF190] + 8 + cl*0x1C8` (a folded, dead gate).
  - **Narrowed wording:** "returns 0 when `ecx` is above 5 (unsigned); otherwise forms the record `qword 02EBF190 + 8 + cl * 0x1C8` and returns 1 when its byte `+0x1C3` or byte `+0x1C4` is not 0xFF, 0 when both are 0xFF (the null-base arm for `cl` above 0x27 at `0032A7AA` is unreachable after the `ecx` check)"
