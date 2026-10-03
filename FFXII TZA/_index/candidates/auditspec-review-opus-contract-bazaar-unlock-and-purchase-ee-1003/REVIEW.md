# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-bazaar-unlock-and-purchase-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-BAZAAR-UNLOCK-AND-PURCHASE-E-FE2DA` · Package: `_index/candidates/opus-contract-bazaar-unlock-and-purchase-ee-1003/` · Page: `12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md` (commit 6a9eb7555; reviewed at HEAD e8b1a961a, package and page unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so I read it clause by clause against the full listing. All 5 anchors are correct and every clause holds, including the loop bounds and the exit condition.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0.
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `002534C0` correct.
    - Index clamp: `cmp ecx, 0xb` / `jbe` (unsigned "above") is done twice. Each time `0016D6A0(0x200)` is called and the index is replaced by 0 (`002534DE`/`002534E3` for `e`, `002534FC`/`00253501` for `c`).
    - Pointers: `e` = `02092760 + 8*i`, `c` = `[020927C0] + 4*i`, and the count dword is `[c+0x47B8]`. `w` = `0020E600(dword [e+4])` (`0025351A`).
    - Outer loop: entry is gated by `cmp [c], 0` / `jle` (signed). Each pass does `cmp word [w+2j], 0xFFFF` (`00253544`), `inc edi` and `cmp edi, [c]` / `jl` (signed).
    - On a hole: `0020E600` is called again (re-decode), and the scan runs from `j+1` while `ebx < [c]` (`jl`). The first non-0xFFFF word is moved to the old-pointer slot `w[j]` (`0025357C`) and 0xFFFF is written in its place.
    - Exit: `cmp ebx, [c]` / `je` (`00253583`). That fires only when no word was found (`ebx` reached the count, which also covers `j+1 >= count`). It then stores `j` to `[c]` (`0025359F`) and returns. No value is returned.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `002534C0` belongs to no accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- `0016D6A0` is a bare `ret 0` (the image names it `_guard_check_icall`), so the `0016D6A0(0x200)` calls the row names have no effect. The row is accurate as written, but a reader may take the call for a real check.
- The README title says "cloud-drafted", while its first paragraph and `rows.json` `session` name `local-ee-drafter` (a local agent, no cloud credit). It is a wording inconsistency only.
