# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PRendering module part 4 (opus-member-modules-registered-before-main-phyre-prendering-module-4)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-B437C` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-prendering-module-4/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 35 functions, 163 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 35 rows, 163 anchors, mode `member`, family `Phyre PRendering module`. Rejected 0, missing 0, corrections none. Skipped 3, each "too large for one precise sentence": `005FD2A0`, `00607990` and `00608A40`.
- Semantic pass: **15 of 35 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings and imports resolved:
  - `005FCFB0` exact: `0067FFB0(02CE9DA0, edx 0x60, r8d 0x64, r9d 8, [rsp+0x20] = 00D4B590 "PCheckVisibleBoundsJob")`; guard 02CE9DC8; exit routine 008ACDC0.
  - `005FD560` exact: two list passes (`-1`, then 0, 1, …), count to 02CB635C, `0063DE00(02CB6780, count*8, 8)`.
  - `005FDD40` exact: the unlink search starts at `&head` (02E522D0), matches the link field `node+0x10`, writes the node's next into the found link and zeroes the node's link, then continues from the next saved before the search; the tail is `jmp 006803D0` with 02E524B0.
  - `005FE1B0` exact: `cmp ax,cx` on zero-extended words with `jbe`/`jae` (unsigned, "above/below" right); the dwords use `jg`/`setl` (signed, stated as signed).
  - `00606970` exact.
  - `00609BF0` exact. The pointer array is alloca'd through `00808F10`; `qsort` is the import at IAT slot `008C3090` with comparator 005FE1B0. Rounding is `(off + a - 1) AND NOT(a - 1)`. The gap fill tests `word [+2] <= gap` (`ja` skip, unsigned) and `off AND (align - 1) == 0`, and zeroes the slot it fills. The inner loop continues while the gap is non-zero; a full pass restarts only when the `r10b` flag shows the last pass placed one. The offset ends in dword `[rcx+0x10]`; cookie 01F44830, check `00808C40`.
  - `0060C510` exact: the early exit compares `edx` with the full dword `[rcx]`; `cmovb` gives the min; `lea eax,[rsi+0xd]` with `rsi` = 0; the free gate is `!= p` then bit 31 clear, with no null test (the callee `005F0220` tests null itself).
  - `0060C7E0` exact: `005E3600`; free `00584730` gated `!= p`, bit 31 clear, non-null.
  - `0060C900` exact: `005E3750`, same gate.
  - `0060CB40` exact: `005E3A20`; `005F0520(old, dword AND 0x7FFFFFFF)`.
  - `0060CE30`, `0060DEE0` (`movss [rcx+8],xmm1`) and `0060DF50`: exact.
  - `0060E460` exact: the per-element `005DDC60` at stride 0x50, and the stores on both the freeing path and the skip path.
  - `0060E6D0` exact: `and r8w,0x1fff`; `cmp ecx,[r9]; ja` and `cmp dx,4; jb` (both unsigned, "at most" / "at least"); `memcpy` source `lea rdx,[rsp+0x40]` = the `r8d` home slot stored at entry.
- Advisory, not a defect: in `0060C510` / `0060C7E0` / `0060C900` / `0060CB40` the `min` is an unsigned minimum (`cmovb`). With the second operand masked to 31 bits, it differs from a signed minimum only when `edx` has bit 31 set. OPUS may add "(unsigned)" in a later pass.
- Batch-wide sentence (shared by the 7 PRendering records of 83b4566ab): "203 rows … 199 stood, 4 rows were corrected in 6 clauses (signed compares)" matches the records and `verify_prendering_1003.json`, as checked in the part 1 record.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
