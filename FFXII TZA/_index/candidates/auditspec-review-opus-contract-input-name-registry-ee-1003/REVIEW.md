# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-contract-input-name-registry-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-INPUT-NAME-REGISTRY-EE-1003` · Package: `_index/candidates/opus-contract-input-name-registry-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 8 rows (40 anchors) were read clause by clause against the bytes. The package has fewer than 15 rows, so every row was checked. No defect was found.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `interior_applier.py` without `--apply` only verifies. It was run in place with `-B` under the analysis venv python: `VERIFY 8 functions, 40 anchors` / `ALREADY` / `FAILS 0`, exit 0. This is identical to the committed `.out`. The run left the package and the page unchanged.
- **Page text.** Each row's `text` occurs exactly once on the live CONTRACT page, in the row for its function.
- **Overlap.** Five rows (`008760A0`, `00876490`, `008768A0`, `00876D80`, `00879670`) carry the same sentences as the sibling package `opus-the-input-name-registry-and-channel-alia-ee-1003`. They were verified there in full: see `_index/candidates/auditspec-review-opus-the-input-name-registry-and-channel-alia-ee-1003/REVIEW.md` for the clause-by-clause addresses. They were re-checked here against the same disassembly. **Exact.**
- **Method for the three new rows.** Each was disassembled with `disr.py` (extent 0x84, which ends at a `ret`, with no jump table). It was then compared instruction by instruction with `008760A0`, with every rip target masked and branch targets made entry-relative.
  - `006D9680`: **exact.** The masked body is identical to `008760A0` in 40 of 40 instructions. The head is qword `02EA06D8`, loaded at `006D969D` and stored at `006D96EA`.
    - The null-name test is `jne` at `006D968E`; the null path returns `lea eax,[r10+0x11]` = 0x11.
    - The byte compare is `sub` at `006D96C8`, over `[node+8]` against the name, stopping at the name's terminating zero.
    - An equal string exits by `je` at `006D96D5` to `mov eax,0x12`.
    - The old head is stored to `[rcx+0x10]` at `006D96E0` (r11 = the incoming rcx), then rcx is stored to the head and 0 is returned.
  - `006D9A70`: **exact.** The body is identical. The head is `02EA0748` (`006D9A8D` / `006D9ADA`), and the anchors are at +0E/+48/+55/+60/+6A.
  - `00877060`: **exact.** The body is identical. The head is `02EB8428` (`0087707D` / `008770CA`), and the anchors are at +0E/+48/+55/+60/+6A.
- **Anchors.** All 40 are instruction boundaries carrying the recorded mnemonics. Each lies on the clause it supports. The insert rows use the same five clause positions in each member. The array rows anchor the count compare, the allocation call, the failed-allocation branch, the free call and the fill store.

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing.

Note (non-blocking): the lists at `02EA06D8` and `02EA0748` sit in a different range from the `02EB8xxx` heads. These rows state only the head each body reads and writes; which registry each list holds is page prose and was not part of this check.
