# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-script-to-native-calling-convention-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SCRIPT-TO-NATIVE-CALLING-CONVENTI-7C7D0` · Package: `_index/candidates/opus-the-script-to-native-calling-convention-ee-1003/` · Page: `01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md` (commit 6a9eb7555; reviewed at HEAD e8b1a961a, package and page unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so I read it clause by clause against the full listing. All 5 anchors are correct and every clause holds.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0.
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `00348330` correct. `rdi = r9`, `rbp = rcx`, and `b` = `002640C0()` (`0034834A`). `x` = `002650B0(b, rbp, 00267E10(rdi))` (`00348355`, `00348363`), then `y` the same way through the same `rdi` (`0034836E`, `0034837C`). `r` = `00309C00(rcx = y, rdx = x)` (`0034838A`).
    - The four stores are `[01EF9208] = [01EF920C]` (`00348397`), `[01EF9210] = [01EF9214]`, `[01EF920C] = dword [y]` and `[01EF9214] = dword [x]` (`003483B3`).
    - It ends with `jmp 0026B4E0` with `rcx = rbp` and `edx = r` (`003483D0`), a tail jump, not a call.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `00348330` belongs to no accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title says "cloud-drafted", while its first paragraph and `rows.json` `session` name `local-ee-drafter` (a local agent, no cloud credit). It is a wording inconsistency only.
