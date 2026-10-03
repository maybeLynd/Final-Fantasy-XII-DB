# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-bodies-the-list-cuts-short-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-BODIES-THE-LIST-CUTS-SHORT-EE-100-7BAF8` · Package: `_index/candidates/opus-the-bodies-the-list-cuts-short-ee-1003/` · Page: `99-Unresolved-Residual/Unlisted-Code/the-bodies-the-list-cuts-short.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so the row was read clause by clause against the full listing. All 5 anchors are correct and every clause holds.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). Output: `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the package and the page was clean afterwards (HEAD `b5028e7e9`).
- `rows.json`: 1 row, 5 anchors; rejected 1 (`00729920`, two text-gap names), skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `0082A5D0` correct. `inc word [[rcx+0x38]+0x46]` (`0082A5E3`), then `cmp` with `esi` = 0xC8 and `jbe` to the return (`0082A5EF`, unsigned "at most"). `rbx` = `[rcx+0x30]` (the record) is loaded before the compare (`0082A5E7`). Both formats use `rcx` = `rdi` = `[[rbx+0x18]+0x38]` (`0082A5FA`). Location string: `r8d` = dword `[[rbx]+0x68]`; zero -> `01CCCFD8` 'main function' (`0082A60A`), else `0081BFF0(rdi, 01CCCFE8 'function at line %d', r8d)` (`0082A628`). Second format `0081BFF0(rdi, 01CCD000 'too many %s (limit is %d) in %s', r8 = 01CCD068 'C levels', r9d = 0xC8, [rsp+0x20] = string)` (`0082A646`; `[rsp+0x20]` is the 5th argument, the "that string" slot). Last: `00824330(rcx = [rbx+0x18], rdx = result)` (`0082A652`), the last instruction inside the listed size 0x87, so "where the listed range ends" holds.
- README count sentences checked against `rows.json`: "named 2 F-frontier functions" = 1 row + 1 rejected; "1 applied with 5 anchors", "Rejected ... 1", "Skipped ... 0", "Missing: 0" all match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only at HEAD `b5028e7e9`; 331 accepted families, 19 in scope): `0082A5D0` is a member of `Lua 5.2.1 library` (letter C), which `23-Third-Party-Libraries/third-party-middleware-inventory.md` declares, not this page. It is not in scope on this page, so the base rule applies and its interior anchors credit.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures (`check_links`, `check_consistency`, `verify_doc_addresses`) and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title and **Limits** say "cloud-drafted" and "A cloud draft is a pointer", while its first paragraph and `rows.json` `session` name `local-ee-drafter-r4` (a local agent, no cloud credit). It is a wording inconsistency only; no row depends on it.
