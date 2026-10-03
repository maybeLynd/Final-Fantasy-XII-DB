# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PScripting module (opus-member-modules-registered-before-main-phyre-pscripting-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-PHYRE` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-pscripting-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 399ce7caf)

**Which record this is.** The task id is truncated. It is shared by the pgameplay, pgeometry-1, pgeometry-2 and pscripting records, and the board kept only one entry. That entry's `target` is `_index/candidates/opus-member-modules-registered-before-main-phyre-pscripting-module-1/` and it asks about 19 F dispositions, the pscripting row count. This record reviews pscripting. The other three records are covered by the superseding review `auditspec-review-opus-phyre-members-399ce7caf`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 19 functions, 91 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 19 rows, mode `member`, family `Phyre PScripting module`; rejected 3 (`00682E30`, `006853C0`, `00685560`: not entry-only frontier functions, none applied), skipped 0, missing 0. 1 correction (`00685DB0`).
- The correction is confirmed at the bytes. `00685EFC` reads `dword [rsi+0x60]` and `00685F26` reads `dword [rsi+0x48]`, with `rsi` = `rcx`, so the offsets are relative to `rcx`. `00685F1A` frees the `+0x60/+0x68` pair with `00584730`, and `00685F45` calls `00682D90(qword, count AND 0x7FFFFFFF)` for the `+0x48/+0x50` pair. The row now says this, and says that a pair is zeroed only when its count is non-zero (`je 00685F26` / `je 00685F51`).
- Semantic pass: **all 19 rows** checked against `disr.py` output of the certified image. 16 were read in full, clause by clause. The three siblings of `00683CA0` (`00683D30`, `00683E50`, `00683EE0`) were compared by their branch, call and constant lines (02E41070 / 02E41170 / 02E41470). All 19 are exact:
  - `006817D0`, `00681910`: the free gates (`not al; test al,1` on the pointer, and on bit 31 of the count). The final `00584730(qword [rcx+0x18])` in `006817D0` and `001C2720(...)` in `00681910` have no null test, as the rows state.
  - `00681A00`: `001EAD40(destination slot, qword - (byte & 1))`, skipped when source equals destination.
  - `00681B40` (`00809950` = `free`, size 0x28), `00683AF0`.
  - `00683040`: the strings resolve as stated. 00D24050 is "...was not a Phyre Object...", 00D240B0 is "...was of type "%s" when...", 00D23FF0 is PhyreScripting.inl, and 00D70360 is `PObjectAccessor<class Phyre::PBase &>::Get`. Lines 0x8D/0x8F. The `+0x78` walk starts at `b` itself.
  - `00683CA0`/`00683F70`: 00D6FDE0 = "PhyreObject". `cmove rcx,rdx` gives 0 for a null `rdx`.
  - `006846C0`: fifth argument `[rsp+0x70]` and seventh `[rsp+0x80]` (five pushes + 0x20). `p` = the sixth argument via `cmova` against 1 (unsigned, so "below 2" gives 1). The refill and 0xD path. The increment loop and the stores to `e`.
  - `00684830`: argument re-packing `[rsp+0x70]` -> sixth.
  - `006856E0`: `lea eax,[r10-2]; cmp eax,0xfe; ja` admits 2..0x100. `lim` = 0x100 - (0x100 mod p). A strict `jae` skip keeps the earliest phase on a tie.
  - `00685980`, `00685B30`: `Sleep(1)` wait on 3. The call result is returned only when non-zero.
  - `00685C10`: empty `r9` -> null via `cmove`. The 02E41050 test is taken once (`setne r12b`). The `add word, 0xFFFF` decrement loop. Return 0 / 0x13.
  - `00685DB0`: the cursor loop uses `test eax,eax; je` (advance on 0), then `cmp eax,r9d; jns` (stop at a non-negative difference). "Below dword 02E41060 (signed difference)" is exact. The exit uses the `dl` progress flag or the cursor reaching `b+0x40`, which is re-read each pass.
  - `00685F60`.
- Advisory, not a defect: "at most 1" in `00685980` and `00685B30` is an unsigned test (`cmp eax,1; ja`). The rows claim no signedness, and the dword is a state value that is set to 3. OPUS may add "(unsigned)" in a later pass.
- Limits hold: these are body statements and static evidence only. The drafting agent, the second local reader and OPUS's re-read are not independent review; this record is.
- Batch-wide sentence, not this record's rows: the README's "262 stood, 10 clauses in 8 functions were corrected" (shared by all 11 records of 399ce7caf) does not match the `rows.json` corrections, which total 12 entries in 10 functions across the 11 records. The narrowing is recorded once, in `auditspec-review-opus-phyre-members-399ce7caf`.
