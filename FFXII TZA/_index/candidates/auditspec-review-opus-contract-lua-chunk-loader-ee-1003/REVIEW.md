# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-lua-chunk-loader-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-LUA-CHUNK-LOADER-EE-1003-01618` · Package: `_index/candidates/opus-contract-lua-chunk-loader-ee-1003/` · Page: `23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md` (commit 6a9eb7555; reviewed at HEAD e8b1a961a, package and page unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so I read it clause by clause against the full listing. All 5 anchors are correct and every clause holds.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0.
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `008242A0` correct.
    - The 5th argument is `[rsp+0x50]` after `push rbx` + `sub 0x20` (`008242A6`); it goes to dword `[rdx]`.
    - Then byte `+0x68` = 0x2E (`008242AF`), `+0x38` = `rcx` (`L`), dword `+0x20` = 0x11E (`008242B7`), `+0x40` = `r8`, `+0x30` = 0, dwords `+4`/`+8` = 1, `+0x58` = `r9`.
    - `0081EF90(rcx = L, 01CCB6BC '_ENV')` (`008242E3`), result to `+0x60`, then `or byte [rax+9], 0x20` (`008242F2`).
    - Buffer: `rdx = [ls+0x48]`, then `00823670(L, [buf], [buf+0x10], r9d = 0x20)` (`00824305`). Its result goes to `[buf]` and 0x20 to `[buf+0x10]`, with the buffer re-read from `[ls+0x48]`. No value is returned.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `008242A0` is a member of `Lua 5.2.1 library` (letter C), which `23-Third-Party-Libraries/third-party-middleware-inventory.md` declares, not this page. It is not in scope here, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title says "cloud-drafted", while its first paragraph and `rows.json` `session` name `local-ee-drafter` (a local agent, no cloud credit). It is a wording inconsistency only.
