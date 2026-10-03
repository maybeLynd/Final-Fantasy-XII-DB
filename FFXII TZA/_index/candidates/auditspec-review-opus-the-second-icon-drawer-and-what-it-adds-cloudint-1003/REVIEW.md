# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-second-icon-drawer-and-what-it-adds-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SECOND-ICON-DRAWER-AND-WHAT-IT-AD-7043E` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-the-second-icon-drawer-and-what-it-adds-cloudint-1003/` · Page: `99-Unresolved-Residual/the-second-icon-drawer-and-what-it-adds.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 2 functions, 9 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 2 rows, 9 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 2 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 2, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `00181800`: the stack slots after `sub rsp, 0x50` are `[rsp+0x20]` = 0, `+0x28` = `ebx` (incoming `r9d`), `+0x30` = 0, `+0x38` = 1, `+0x40` = 1 and `+0x48` = 0, i.e. arguments 5..10 = `0, r9d, 0, 1, 1, 0`. Registers: `rcx` = `001B1C00()`, `edx` = incoming `ecx`, `r8d` = incoming `edx`, `r9` = incoming `r8`. Exact. The label "core runtime object fetch" is not a body statement: `001B1C00` is `mov rax, [01F811E8]; ret`, which other pages describe as the global draw context or renderer batch singleton. The label follows this page's CoreRuntimeScheduling layer line, and nothing on the page depends on it. This is noted, not a defect.
  - `00272310`: `00246480(rcx, &t)` (`t` = `[rsp+0x20]`), qword `t` stored to `[rdx]`, `rcx` null-tested, then the chain through `[node+0x10]` with two 16-bit `add`s to `[rdx]`/`[rdx+2]`; the cookie is present. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
