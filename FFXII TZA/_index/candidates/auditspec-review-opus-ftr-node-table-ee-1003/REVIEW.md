# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-ftr-node-table-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-FTR-NODE-TABLE-EE-1003-FC915` · Package: `_index/candidates/opus-ftr-node-table-ee-1003/` · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md` (commit 6a9eb7555; reviewed at HEAD e60842fa0, package and page unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so I read it clause by clause against the full listing. All 5 anchors are correct and every clause holds.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0.
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disw.py` output of the certified image (SHA256 73461D08...):
  - `00800000` correct.
    - First range: `rbx = [o]`, `rsi = [o+8]`, with the loop skipped when they are equal. Each qword `p` is tested with `test rdi` / `je` (null skipped), then `00210EB0([p+8])` (`00800034`) and `00809950(p, 0x18)` (`00800041`).
    - Then `00210EB0([o])` (`0080004E`).
    - Second range `[o+0x10]..[o+0x18]`: null `p` is skipped, then `00210EB0` on `[p+8]`, `[p+0x18]` and `[p+0x28]` (`00800082`), and `00809950(p, 0x50)` (`0080008F`).
    - It ends with `jmp 00210EB0` with `rcx = [o+0x10]` (`008000B2`), a tail jump.
    - The body contains no store to memory (only register loads and the saved-register spills), so "no pointer it frees is cleared" holds.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `00800000` is a member of `libwebm mkvparser` (letter C), which `23-Third-Party-Libraries/third-party-middleware-inventory.md` declares, not this page. It is not in scope here, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title says "cloud-drafted", while its first paragraph and `rows.json` `session` name `local-ee-drafter` (a local agent, no cloud credit). It is a wording inconsistency only.
