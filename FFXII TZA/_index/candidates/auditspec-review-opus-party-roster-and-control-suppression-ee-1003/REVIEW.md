# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-party-roster-and-control-suppression-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PARTY-ROSTER-AND-CONTROL-SUPPRESSION-16BFC` · Package: `_index/candidates/opus-party-roster-and-control-suppression-ee-1003/` · Page: `11-Party/party-roster-and-control-suppression.md` (commit 6a9eb7555; reviewed at HEAD e60842fa0, package and page unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so I read it clause by clause against the full listing. All 5 anchors are correct. Every clause holds, including both points of OPUS's correction: nothing is written back to `t`, and a zero count skips the loop.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0.
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 1 (`007A05D0`).
- Semantic pass: **every row** read clause by clause against `disw.py` / `disr.py` output of the certified image (SHA256 73461D08...):
  - `007A05D0` correct.
    - Setup: `s` = `[rsp+0x80]` and `00615BC0(&s)` (`007A05F3`). `00624960(00624670(&s), &a = rsp+0x88, &b = rsp+0x90, &c = rsp+0x98)`.
    - Unchanged size: `+0xD24 == a` and `+0xD28 == b` -> `007A0790`, which is `001825A0()` and `esi = 0`.
    - `r = 006278B0(00624670(&s), +0xD24, +0xD28)` (`007A0663`); non-zero -> return `r`.
    - Log: `005CDAA0(ecx = 2, 01CB3160 '======== Call resize w = %d,h = %d =======\n', +0xD24, +0xD28)`.
    - `r = 0060F6B0(rcx+0xE8, 0, 0, r9d = +0xD24, [rsp+0x20] = +0xD28, [rsp+0x28] = 0)` (`007A06B0`; the 5th and 6th arguments); non-zero -> return.
    - Loop entry: `test [+0xDB8], 0x7FFFFFFF` / `jbe` (`007A06CB`). `test` clears CF, so this branches exactly when the masked count is 0.
    - Per item, `t = [[rcx+0xDC0] + 8i]`. Only when `[t+0x2C]` and `[t+0x30]` are both non-zero are the four values scaled: `imul` (low 32 bits) then `div` (unsigned) by `a` or `b` (`007A070A`). `+0x24`/`+0x2C` scale by `+0xD24`, `+0x28`/`+0x30` by `+0xD28`. All of this happens in registers; nothing is stored to `t`.
    - `007A10A0(t, x, y, w, [rsp+0x20] = h)` (`007A0760`), then `t` is re-read and `call [vt+0x20]`; non-zero -> return it.
    - Loop end: `btr eax, 0x1f` / `cmp` / `jb` (unsigned).
    - Every exit goes through `00616700(&s)` (`007A079F`) before `eax = esi`.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match. The one **OPUS corrections** bullet matches `rows.json` `corrections`, and the row text reflects both points.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `007A05D0` is a member of `Phyre PFramework module` (letter C), which `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` declares, not this page. It is not in scope here, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title says "cloud-drafted", while its first paragraph and `rows.json` `session` name `local-ee-drafter` (a local agent, no cloud credit). It is a wording inconsistency only.
