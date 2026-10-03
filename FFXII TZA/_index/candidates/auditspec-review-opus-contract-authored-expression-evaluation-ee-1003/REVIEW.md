# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-authored-expression-evaluation-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-AUTHORED-EXPRESSION-EVALUATI-48A90` · Package: `_index/candidates/opus-contract-authored-expression-evaluation-ee-1003/` · Page: `02-Resource-And-Asset-Pipeline/Authored-Expressions/CONTRACT-authored-expression-evaluation.md` (commit 6a9eb7555; reviewed at HEAD e60842fa0, package and page unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so I read it clause by clause against the full listing. All 5 anchors are correct. The formula, the parity handling and the store all hold as written.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0.
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `0039B6E0` correct.
    - Registers: `xmm0 = 2t` (`addss xmm0, xmm0`), `xmm3 = a = [rdx]`, `xmm2 = b = [rdx+0x10]`, `xmm1 = 2b`. `xmm7 = b - a`, `xmm3 = a + b - 2t`, and `xmm6 = a - 2b` (`0039B715`) `+ [rdx+0x20]` = `A`.
    - Test: `ucomiss A, 0` (`0039B725`) followed by `jp` and `jne`, both to the general path. Only an ordered equality stores 0x40000000 (2.0) to `[r8]` (`0039B72C`); unordered takes the general path, as stated.
    - General path: `(b-a)^2 - (a+b-2t)*A`, then `sqrtf` through the thunk `00861F14` (`0039B752`), `-(b-a)`, `/A` (`0039B760`), stored to `[rbx = r8]`. No value is returned.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `0039B6E0` is a member of `NativeAdapter.ExplainedCalleeForwarder` (letter B), which `24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md` declares, not this page. It is not in scope here, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title says "cloud-drafted", while its first paragraph and `rows.json` `session` name `local-ee-drafter` (a local agent, no cloud credit). It is a wording inconsistency only.
- `0039B6E0` sits in a family named `ExplainedCalleeForwarder`, but its body is an inline quadratic solve whose only call is `sqrtf`. That membership looks doubtful. It is outside this package's scope.
