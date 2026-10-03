# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-contract-phyre-cluster-header-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CONTRACT-PHYRE-CLUSTER-HEADER-HOMING-1` · Package: `_index/candidates/fable-contract-phyre-cluster-header-homing-1003/` · Page: `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md` (commit b35f1958c; reviewed at HEAD 89538d085, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

This is an interior package: it ships `interior_applier.py` and no `homing_applier.py`. Only the sentences were reviewed. It has 4 rows, fewer than 15, so I read all 4 clause by clause against the full listings. All 20 anchors are correct. Every row holds, including the walk direction, which differs between the forward and backward pairs.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 4 functions, 20 anchors`, `ALREADY` and `FAILS 0`, exit 0. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 4 rows, 20 anchors, `mode: homing`; rejected 2 (`001C1A60`, `001C2230`: "not a callee-host homing body (or already explained)"), skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disw.py` / `disr.py` output of the certified image (SHA256 73461D08...):
  - `006305A0` correct.
    - Record at `[rsp+0x20]`: dword 0, dword `[02CF82A8]` (`006305AF`), qword `rcx`, byte 1 (`006305CD`).
    - Block chain: `rsi` starts at `02CF8270` and advances through `[rsi+0x78]` until null.
    - Ring head `rdi = rsi+0x80`. The first link is `[rdi]` (`006305E7`). It exits on `link == head`, a null link, or `link-8 == 0`.
    - Each step is `0063CE80(&record, link-8)` (`00630608`). The next link is `[rbx+8]` = `[link+0]`, which is the forward direction.
  - `006306E0` correct. The record holds dword `[02CF84A8]`, then `lea rax,[rcx+0x30]` / `cmove rax, 0` when `rcx` is null (`00630712`), then byte 1. The chain starts at `02CF8470`. The forward walk is the same as above (`00630727`, `00630748`).
  - `00630BE0` correct. The record is `02CF82A8` / `rcx` / byte 0 (`00630C0D`), with the chain at `02CF8270`. The first link is `[head+8]` (`00630C27`) and the next is `[rbx+0x10]` = `[link+8]` (`00630C4D`), which is the backward direction.
  - `00630D20` correct. The record is `02CF84A8` / (`rcx+0x30` or 0, `cmove` at `00630D51`) / byte 0 (`dl`). The chain is at `02CF8470`, and the walk is backward through `[link+8]` (`00630D67`, `00630D8D`).
- README count sentences checked against `rows.json`: "named 6 F-frontier functions" = 4 rows + 2 rejected. "4 staged with 20 anchors", "Rejected ... 2", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): none of the 4 belongs to an accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
