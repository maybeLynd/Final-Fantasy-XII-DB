# SWE2-AUDIT-SPEC review of SD-9 (sd9-input-deadline-0930 at ca25e7dde): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Reviewed: OPUS's
`ca25e7dde` (the record's only commit), [README](../sd9-input-deadline-0930/README.md) and `sd9_input_deadline.py`.
Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD9-0930 | sd9-input-deadline-0930 | `ca25e7dde` | ACCEPT |

**Re-run.** [rerun_sd9_input_deadline.out](rerun_sd9_input_deadline.out) is identical to the committed `.out` (ignoring CR),
F1-F6 PASS, `FAILS 0`. The record directory stayed clean.

**Re-derived independently** ([sd9_rederive.py](sd9_rederive.py) / [.out](sd9_rederive.out)).
- **The block `022CA5C0`..`022CA5DF`, across ALL `.text` and with widths.**
  - The step `[022CA5D0]` has exactly two accesses, both reads: `0035E7B0` and `0035EBF3`.
  - The accumulator `[022CA5C4]` is read at `0035E7AA`/`0035EBED` and written at `0035E7B6`/`0035EBF9`/`0035EC65`.
  - `[022CA5D8]` and `[022CA5DC]` are store-only: `0035E871`/`0035E877` in the initialiser, and
    `0035EBFF`/`0035EC11` in `0035EB70`.
  - There are 0 image-base-relative accesses, 0 relocations and 0 raw qwords into the block.
  - The four raw-only candidates at `004B220C` fall inside bit-mixing code: `004B220B add eax, eax` /
    `004B220D and ecx, 1` are not memory operands.
  - The block lies past `.data`'s raw end `01F7E400`, so it is zero-initialised.
- **`00290180`** is `mov eax, 2; ret`. It has 5 direct callers, one of them `0035E7A0` at `0035E7BC`, and 9
  relocations: a shared constant stub. The period is therefore always `0x108`.
- **`0035E7A0`** has one caller: `0035EB70` at `0035EC05`. There is no jcc, no rip reference and no relocation. After
  the call, `eax` is stored at `0035EC11` and overwritten at `0035EC2E` before any read. The instructions in between
  (`test edi, edi`, `cmovg edx, edi`) read `edi`, not the result. So nothing consumes the return value except the
  dead store.
- **Clear each pass.** `0035EC11`..`0035EC65` is straight-line code: `xor r8d, r8d` at `0035EC1F`, then
  `0035EC65` stores `r8d` into the accumulator. So the accumulator is cleared unconditionally on the path that calls
  `0035E7A0`. Since the step is 0, the accumulator is 0 at every call anyway.

**Controls.**
- F3/F5 read retool.py's extent-bounded rip index. That index is blind to exactly the defect in question: an unlisted
  or image-base-relative writer of the step, or reader of the result. My whole-image sweep in both forms closes this
  and agrees.
- F6's "objects below end before `022CA5C4`" is a useful alias guard for base-pointer routes. It covers only objects
  whose address is taken by `lea`.

**The NTSC/PAL reading** is correctly kept as a labelled inference and not asserted.

**Minor wording (no row change).** F4's print says "result is 2P = 528 (P = 264 in dispatcher mode 3)". It means the
result is 264 in mode 3, as the README says.

**Correction wording:** none needed.
