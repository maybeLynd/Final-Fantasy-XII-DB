# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-duplicated-function-names-and-how-to-res-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-DUPLICATED-FUNCTION-NAMES-AND-HOW-TO-64904` · Package: `_index/candidates/opus-duplicated-function-names-and-how-to-res-ee-1003/` · Page: `00-Engine-Core-Runtime/duplicated-function-names-and-how-to-resolve-them.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so the row was read clause by clause against the full listing. All 5 anchors are correct and every clause holds.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). Output: `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the package and the page was clean afterwards (HEAD `b5028e7e9`).
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `008087C4` correct (a `scalar_deleting_destructor`, size 0x89). `ebp = edx` (the flag) and `rsi = rcx`. `rdi = [rcx+8]` and `rbx = [[rdi]+0x10]`, and the slot target goes to `00809958` (`_guard_check_icall`, a `jmp` through `008C31C0`) before `call rbx` with `rcx = rdi` (`008087FC`). This call is unconditional. On a null result `je` skips (`00808805`). Otherwise `rbx = [[rax]]` (slot `+0`), `00809958` again, then `call rbx` with `rcx` = the returned object and `edx` = 1 (`0080881E`). `test bpl, 1` (`00808821`) / `je` gates `00809950(rcx = rsi, edx = 0x10)` (`0080882F`; `00809950` is `free`, a `jmp 00210EB0`). `rax = rsi` on the single exit (`00808835`), so the original object is returned on every path.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" all match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only at HEAD `b5028e7e9`; 331 accepted families, 19 in scope): `008087C4` is a member of `MSVC runtime tail` (letter C), which `23-Third-Party-Libraries/third-party-middleware-inventory.md` declares, not this page. It is not in scope here, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title and **Limits** say "cloud-drafted" and "A cloud draft is a pointer", while its first paragraph and `rows.json` `session` name `local-ee-drafter-r4` (a local agent, no cloud credit). It is a wording inconsistency only.
