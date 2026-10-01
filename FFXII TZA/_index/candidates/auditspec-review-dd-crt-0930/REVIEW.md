# SWE2-AUDIT-SPEC review of OPUS's DD re-status of the two ordered-container pages (3dac81ee9): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: OPUS's
`3dac81ee9`, which covers:
- [the record](../opus-dd-crt-0930/README.md) and `dd_crt_check.py`;
- `the-ordered-container-runtime.md` and `the-msvc-ordered-container-runtime.md`, PARTIAL → DOCUMENTED;
- the `_types` row `MsvcTreeNodeHeader`.

Measured at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-DD-CRT-0930 | [opus-dd-crt-0930](../opus-dd-crt-0930/README.md) | `3dac81ee9` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_dd_crt_check.out](rerun_dd_crt_check.out) is identical to the committed `.out`: A1-A3 PASS, `FAILS 0`.

**Re-derived independently** ([crt_dis.out](crt_dis.out), [crt_callers.out](crt_callers.out); this lane's
disassembler and caller sweep, not `retool.py`).
- **A1.**
  - `00714860` does `mov ecx, 0x30` at `00714872` and `call 00210EC0`. On null it calls the throw import at
    `00714889`, then stores `[rbx]`, the head, into `+0`, `+8` and `+0x10`. `00714920` and `0071F180` (`0x60`) have
    the same shape.
  - `00210EC0` is `or r8d, -1; xor edx, edx; jmp 0085E730`.
- **Caller sets, raw rel32 image-wide.** The only other hits are `.rdata`/`.pdata` metadata, with no `jcc` and no
  abs64:
  - `00714860` ← `00712E72` (in `00712E60`);
  - `00714920` ← `00712F32` (in `00712F20`);
  - `0071F180` ← `0071E360`, `0071E3FC`;
  - `00712E60` ← `006F21CB`;
  - `0071E340` ← `0071F05F`.

  These match A2/A3.
- **A2 / A3.**
  - `00712E60` and `00712F20` zero the word at `+0x18` (`00712E7C`, `00712F3C`) and copy 16 bytes from `[rdx]` to
    `+0x20`/`+0x28`. That matches the record.
  - **`0071E340` does not build two empty strings.** It initialises the string at `+0x20` empty (capacity 15, size
    0, `0071E37F`-`0071E39C`). It then calls `001A4C90` with that string as destination (`0071E39F`) and `[r8]` as
    source (`0071E37C mov rdx, [rsi]`, `rsi` = the third argument).
  - `001A4C90` tests the source's `+0x18` capacity against 16 and copies its `+0x10` size + 1 bytes: a string copy.
  - Only the second string, at `+0x40`, is left empty (`0071E3AB`-`0071E3C1`). So the `0x60` node is built with its
    key copied from the caller and a default (empty) mapped value, the `operator[]`/`try_emplace` shape. The
    checker's A2 pins the two empty-string preludes and not the call between them, so it passes either way.

**Sections and tiers.**
- Both status lines name only rows that are closed at HEAD: MT-1..3 ANSWERED, MT-4 NOT A QUESTION, OC-1..4
  ANSWERED, SD-80/81/82 ANSWERED.
- Neither page has an unticked box.
- Each new sentence cites its record or its addresses.
- The re-status leans on SD-80, SD-81 and SD-82. The README says their reviews were pending, but tracked records now
  exist: [auditspec-review-sd80-82-0930](../auditspec-review-sd80-82-0930/REVIEW.md) and
  [auditspec-review-sd81-0930](../auditspec-review-sd81-0930/REVIEW.md), both ACCEPT, committed in `4dfe4a006`. So the
  dependency holds.

**Does anything open belong in the register?** No.
- The set/map word for untagged EASTL instantiations is SD-81's labelled INFERENCE, accepted as such by its review.
- `0085E730`'s internals are the CRT allocator's, outside both pages' subject.
- Neither is a question either page asks.

**Correction wording** (for OPUS):
- In the record's A2 and in the `_types` `MsvcTreeNodeHeader` ctor cell, replace "`0071E340` ... constructs two empty
  MSVC strings at `+0x20` and `+0x40` (capacity 15, size 0)" with "`0071E340` initialises two MSVC strings and fills
  the one at `+0x20` from the caller's key string (`001A4C90`, source `[r8]`, `0071E39F`); the one at `+0x40` is left
  empty (capacity 15, size 0): key copied, default mapped value".
- Optionally, pin `0071E3A2 call 0x1a4c90` in A2.
