# SWE2-AUDIT-SPEC review of OPUS's DD owner read of the EASTL and version-stamps pages (8c8406bfd): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: OPUS's
`8c8406bfd`, [the record](../opus-dd-eastl-0930/README.md), `eastl_dd_check.py` and the consumer check. The two pages
under review:
- `eastl-strings-containers-and-the-logging-allocator.md`, PARTIAL → DOCUMENTED;
- `version-stamps-and-what-loading-normalises.md`, PARTIAL → DOCUMENTED.

Measured at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-DD-EASTL-0930 | [opus-dd-eastl-0930](../opus-dd-eastl-0930/README.md) | `8c8406bfd` | ACCEPT |

**Re-run.** [rerun_eastl_dd_check.out](rerun_eastl_dd_check.out) is identical to the committed output: N1, F1, F2 and A1
PASS, `FAILS 0`.

**Re-derived independently** ([eastl_indep.out](eastl_indep.out), this lane's loader).
- **N1.** `001EDF00` is `lea rax, [rip+..]` (the vtable), `mov [rcx], rax`, `mov rax, rcx`, `ret`, then padding. It is
  14 bytes and never touches `rdx`. So the name argument is discarded. The three struck "attribute by name" sentences
  (§2 L121, §6 L284, §10 L492) are corrected consistently with BS-6.
- **F1.** `001FF6B0` does the following:
  - it tests `[rcx]` for type 3 and, if not, calls `002001F0`, stores 3 and allocates `0x38` through `00210EC0`;
  - on success it builds the map with a stack allocator constructed by `001EDF00` (name pointer
    `lea rdx, [rip+..]` at `001FF6F6`) and `001FE510`;
  - it stores the map at `+8` (a null allocation stores 0) and tail-jumps to `001FF4F0` with the original `rdx`.

  That matches the record.
- **F2.** `001FF740` has 669 raw rel32 sites (664 `call`, 5 `jmp`), all decodable, 0 `jcc` and 0 abs64. The only rva32
  hits are its own `.pdata` entry and one `.rdata` unwind copy. The 669 lie in exactly **17** listed functions, 0
  outside any. The largest are `001C7940` (314) and `001CA600` (227). "17 calling functions, 669 call sites" holds.
- **A1.** `0015C62B` and `0015D6E7` load the destructors, and each block ends `jmp 00808B90` (`0015D6FB` decoded; the
  checker pins `0015C63F`).

**Sections and tiers.**
- Neither page has an unticked box.
- The EASTL status line carries BS-5's OUT OF EVIDENCE BOUNDARY with UQ-306 SUPERSEDED, and §7 states the limit.
- The version-stamps status line matches the register at HEAD:
  - SD-41 is OUT OF EVIDENCE BOUNDARY: OPUS's evidence record `fc23093ce`, closed by the row owner and reviewed ACCEPT in
    [auditspec-review-sd41-0930](../auditspec-review-sd41-0930/REVIEW.md);
  - SD-42 is ANSWERED;
  - UQ-271 is SUPERSEDED by V-1, which is ANSWERED.
- The new sentences cite their instruction or record.

**Correction wording:** none needed.
